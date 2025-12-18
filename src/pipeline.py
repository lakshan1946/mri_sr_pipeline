import os
import ants
import yaml
from.normalize import IntensityNormalizer
from.degradation import DegradationSimulator
from.utils import setup_logger

class MRIPreprocessingPipeline:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.cfg = yaml.safe_load(f)
        
        self.logger = setup_logger('preproc', 'pipeline.log')
        
        # Load Template
        self.logger.info(f"Loading Template: {self.cfg['paths']['template_path']}")
        self.mni_template = ants.image_read(self.cfg['paths']['template_path'])
        
        # Initialize Modules
        self.normalizer = IntensityNormalizer(
            method=self.cfg['preprocessing']['normalization']['method']
        )
        self.degrader = DegradationSimulator(
            target_z_spacing=self.cfg['simulation']['target_resolution_z']
        )
        
        # Prepare Output Dirs
        self.hr_dir = os.path.join(self.cfg['paths']['output_dir'], "HR")
        self.lr_dir = os.path.join(self.cfg['paths']['output_dir'], "LR")
        os.makedirs(self.hr_dir, exist_ok=True)
        os.makedirs(self.lr_dir, exist_ok=True)

        # Intermediate Outputs
        self.save_intermediates = self.cfg.get('pipeline_options', {}).get('save_intermediates', False)
        self.intermediate_dir = self.cfg['paths'].get('intermediate_dir', os.path.join(self.cfg['paths']['output_dir'], "intermediate"))
        if self.save_intermediates:
            os.makedirs(self.intermediate_dir, exist_ok=True)

    def _save_intermediate(self, image, subject_filename, step_suffix):
        if not self.save_intermediates:
            return
            
        # Strip extension for folder name
        base_name = subject_filename.replace('.nii.gz', '').replace('.nii', '')
        
        # Create subject specific folder
        subject_dir = os.path.join(self.intermediate_dir, base_name)
        os.makedirs(subject_dir, exist_ok=True)
        
        out_path = os.path.join(subject_dir, f"{base_name}_{step_suffix}.nii.gz")
        ants.image_write(image, out_path)
        self.logger.info(f"Saved intermediate: {step_suffix}")

    def process_subject(self, nifti_path):
        filename = os.path.basename(nifti_path)
        self.logger.info(f"Starting subject: {filename}")

        try:
            # 1. Load Image
            raw_img = ants.image_read(nifti_path)
            
            # 2. Reorient to Standard System (RAS/LPI)
            # This is vital. If the image is stored as PSR (Posterior-Superior-Right),
            # registration will fail catastrophically. We force RAI/LPI matching the template.
            # Note: Check your MNI template orientation. Standard MNI is often LPI or RAI.
            raw_img = ants.reorient_image2(raw_img, orientation='RAI') 
            self._save_intermediate(raw_img, filename, '01_reoriented') 

            # 3. N4 Bias Field Correction
            # We correct *before* registration to aid the registration metric (Mutual Information).
            if self.cfg['preprocessing']['bias_correction']['enabled']:
                self.logger.info("Applying N4 Bias Correction...")
                # Calculate mask for N4 (otsu thresholding often works for T1)
                mask = ants.get_mask(raw_img)
                n4_img = ants.n4_bias_field_correction(
                    raw_img, 
                    mask=mask,
                    shrink_factor=self.cfg['preprocessing']['bias_correction']['shrink_factor'],
                    convergence={'iters': self.cfg['preprocessing']['bias_correction']['convergence'], 
                                 'tol': float(self.cfg['preprocessing']['bias_correction']['tolerance'])}
                )
            else:
                n4_img = raw_img
            
            self._save_intermediate(n4_img, filename, '02_bias_corrected')

            # 4. Registration to MNI152
            reg_type = self.cfg['preprocessing']['registration']['type']
            self.logger.info(f"Registering to MNI152 ({reg_type})...")
            # type_of_transform defined in config
            reg = ants.registration(
                fixed=self.mni_template, 
                moving=n4_img, 
                type_of_transform=self.cfg['preprocessing']['registration']['type']
            )
            hr_aligned = reg['warpedmovout']
            self._save_intermediate(hr_aligned, filename, '03_registered')

            # 5. Intensity Normalization (WhiteStripe)
            # Normalization is done on the aligned image to ensure the histogram
            # represents the canonical brain space (less background noise).
            self.logger.info("Applying WhiteStripe Normalization...")
            hr_norm = self.normalizer.apply(hr_aligned)
            self._save_intermediate(hr_norm, filename, '04_normalized')

            # 6. Generate Paired LR Data (Simulation)
            self.logger.info("Simulating LR degradation...")
            lr_upsampled = self.degrader.simulate_thick_slices(hr_norm)
            self._save_intermediate(lr_upsampled, filename, '05_degraded')

            # 7. Save Pairs
            ants.image_write(hr_norm, os.path.join(self.hr_dir, filename))
            ants.image_write(lr_upsampled, os.path.join(self.lr_dir, filename))
            
            self.logger.info(f"Successfully processed {filename}")

        except Exception as e:
            self.logger.error(f"Failed to process {filename}: {str(e)}")

    def run_batch(self):
        input_dir = self.cfg['paths']['input_dir']
        files = [f for f in os.listdir(input_dir) if f.endswith(('.nii.gz', '.nii'))]
        
        self.logger.info(f"Found {len(files)} files to process.")
        for f in files:
            self.process_subject(os.path.join(input_dir, f))