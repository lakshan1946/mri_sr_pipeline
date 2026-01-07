
import os
import sys
import shutil

# Ensure src is in path

from src.pipeline import MRIPreprocessingPipeline

def verify():
    print("Starting verification...")
    
    config_path = 'configs/config.yaml'
    pipeline = MRIPreprocessingPipeline(config_path)
    
    # Test file
    test_file = 'data/raw/subject-01.nii.gz'
    if not os.path.exists(test_file):
        print(f"Test file not found: {test_file}")
        sys.exit(1)
        
    # Clean previous output for this subject if exists
    filename = os.path.basename(test_file)
    basename = filename.replace('.nii.gz', '').replace('.nii', '')
    
    out_hr = os.path.join('data/processed/HR', filename)
    out_lr = os.path.join('data/processed/LR', filename)
    intermediate_dir = os.path.join('data/processed/intermediate', basename)
    
    if os.path.exists(out_hr): os.remove(out_hr)
    if os.path.exists(out_lr): os.remove(out_lr)
    if os.path.exists(intermediate_dir): shutil.rmtree(intermediate_dir)
    
    print(f"Processing {test_file}...")
    try:
        pipeline.process_subject(test_file)
    except Exception as e:
        print(f"Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
        
    # Check outputs
    missing = []
    if not os.path.exists(out_hr): missing.append(out_hr)
    if not os.path.exists(out_lr): missing.append(out_lr)
    
    # Check intermediates
    expected_intermediates = [
        '01_raw_reoriented',
        '02_lr_raw',
        '03_hr_n4', '03_lr_n4',
        '04_hr_norm', '04_lr_norm',
        '05_hr_registered_mni', '05_lr_registered_mni'
    ]
    
    for suffix in expected_intermediates:
        path = os.path.join(intermediate_dir, f"{basename}_{suffix}.nii.gz")
        if not os.path.exists(path):
            missing.append(path)
            
    if missing:
        print("FAILED: Missing files:")
        for m in missing:
            print(f"  - {m}")
        sys.exit(1)
    else:
        print("SUCCESS: All files generated.")
        print(f"Checked {len(expected_intermediates)} intermediates and final pairs.")

if __name__ == "__main__":
    verify()
