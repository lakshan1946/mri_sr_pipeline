import ants
import math

class DegradationSimulator:
    def __init__(self, target_z_spacing=5.0):
        self.target_z = target_z_spacing

    def simulate_thick_slices(self, hr_image: ants.ANTsImage) -> ants.ANTsImage:
        """
        Simulates an LR anisotropic acquisition from an HR isotropic image.
        
        Process:
        1. Anisotropic Gaussian Blur (Z-axis only) -> Mimics slice profile.
        2. Downsample (Decimation) -> Mimics thick slice acquisition.
        3. Upsample (BSpline) -> Restores grid size for WGAN input.
        """
        # 1. Calculate Downsampling Factor k
        # We assume the image is oriented (x, y, z).
        # We check the spacing to be sure.
        source_spacing = hr_image.spacing
        k_factor = self.target_z / source_spacing[2] 
        
        if k_factor <= 1.0:
            print("Warning: Target resolution is finer than source. No degradation applied.")
            return hr_image

        # 2. Calculate Sigma for Gaussian Blur
        # Formula: sigma = k / (2 * sqrt(2 * ln(2))) approx k / 2.355
        # This relationship relates the FWHM of the Gaussian to the slice thickness.
        fwhm_factor = 2 * math.sqrt(2 * math.log(2))
        sigma_z = k_factor / fwhm_factor
        
        # Define anisotropic sigma:
        sigmas = [0.0, 0.0, sigma_z] 
        
        # 3. Apply Anisotropic Gaussian Smoothing
        # sigma_in_physical_coordinates=False means sigma is in voxels, which fits our k derivation
        blurred_hr = ants.smooth_image(hr_image, sigma=sigmas, sigma_in_physical_coordinates=False)
        
        # 4. Downsample (Decimation)
        # We create a target spacing that is [1mm, 1mm, 5mm]
        target_spacing = list(source_spacing)
        target_spacing[2] = self.target_z
        
        # Resample to the coarse grid (Linear interpolation is sufficient for downsampling)
        lr_image = ants.resample_image(blurred_hr, target_spacing, use_voxels=False, interp_type=0)
        
        # 5. Upsample back to Original Grid
        # The WGAN generator takes a volume of size and outputs.
        # Therefore, we must upsample the LR data back to the HR dimensions.
        # We use BSpline (interp_type=4) to give the model a smooth starting point,
        # avoiding the blocky "staircase" artifacts of nearest neighbor.
        upsampled_lr = ants.resample_image_to_target(
            lr_image, 
            hr_image, 
            interp_type=4 # 4 = BSpline
        )
        
        return upsampled_lr