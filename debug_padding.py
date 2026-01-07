
import ants
import numpy as np
import os

def check_padding():
    print("Checking ANTsPy padding behavior...")
    
    
    # Check subject file INDEPENDENTLY of the synthetic test
    path = 'data/processed/intermediate/subject-01/subject-01_04_hr_norm.nii.gz'
    if os.path.exists(path):
        print(f"\nExamining subject file: {path}")
        real_img = ants.image_read(path)
        arr = real_img.numpy()
        print(f"Min: {arr.min()}, Max: {arr.max()}, Mean: {arr.mean()}")
        
        # Check corners to see if "background" is actually 0
        corners = [
            arr[0,0,0], arr[-1,0,0], arr[0,-1,0], arr[0,0,-1]
        ]
        print(f"Corner values (Background?): {corners}")
        
    # Create synthetic test
    data = np.zeros((100, 100)).astype('float32') # Float32 for precision
    data[30:70, 30:70] = 100
    img = ants.from_numpy(data)
    
    # Save transform to disk to avoid TypeError
    tx = ants.create_ants_transform(
        transform_type="Euler2DTransform",
        center=np.array([50, 50]),
        parameters=np.array([0.785])
    )
    tx_path = 'temp_tx.mat'
    ants.write_transform(tx, tx_path)
    
    # Test 1: No default value
    out_default = ants.apply_transforms(fixed=img, moving=img, transformlist=[tx_path])

    u, c = np.unique(out_default.numpy(), return_counts=True)
    print(f"\nTest 1 (No Args): Values in corner (0,0): {out_default[0,0]}")
    # print(f"Unique values: {dict(zip(u, c))}")
    
    # Test 2: defaultvalue=0
    try:
        out_0 = ants.apply_transforms(fixed=img, moving=img, transformlist=[tx], defaultvalue=0)
        print(f"Test 2 (defaultvalue=0): Values in corner (0,0): {out_0[0,0]}")
    except Exception as e:
        print(f"Test 2 Failed: {e}")

    # Test 3: defaultvalue=50
    try:
        out_50 = ants.apply_transforms(fixed=img, moving=img, transformlist=[tx], defaultvalue=50)
        print(f"Test 3 (defaultvalue=50): Values in corner (0,0): {out_50[0,0]}")
    except Exception as e:
        print(f"Test 3 Failed: {e}")
        
    # Check subject file if exists
    path = 'data/processed/intermediate/subject-01/subject-01_04_hr_norm.nii.gz'
    if os.path.exists(path):
        print(f"\nExamining subject file: {path}")
        real_img = ants.image_read(path)
        arr = real_img.numpy()
        print(f"Min: {arr.min()}, Max: {arr.max()}, Mean: {arr.mean()}")
        
        # Check corners
        corners = [
            arr[0,0,0], arr[-1,0,0], arr[0,-1,0], arr[0,0,-1]
        ]
        print(f"Corner values (Background?): {corners}")

if __name__ == "__main__":
    check_padding()
