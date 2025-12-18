# train_loader.py
import os
import glob
from monai.data import CacheDataset, DataLoader
from monai.transforms import (
    Compose,
    LoadImaged,
    EnsureChannelFirstd,
    RandSpatialCropd,
    RandFlipd,
    RandRotate90d,
    EnsureTyped,
    NormalizeIntensityd 
)

def get_dataloader(data_dir, batch_size=4, patch_size=(96, 96, 96), num_workers=4):
    """
    Constructs a high-performance MONAI DataLoader for WGAN training.
    """
    # 1. Gather file paths
    # We assume filenames match exactly between HR and LR folders
    hr_images = sorted(glob.glob(os.path.join(data_dir, "HR", "*.nii.gz")))
    lr_images = sorted(glob.glob(os.path.join(data_dir, "LR", "*.nii.gz")))
    
    data_dicts =
    
    # 2. Define Transforms Pipeline
    train_transforms = Compose(),
        
        # Add channel dimension: (D, H, W) -> (C, D, H, W). C=1 for T1w.
        EnsureChannelFirstd(keys=), 
        
        # Patch Extraction
        # Extract 96^3 patches. If image is smaller, it pads automatically (if config allowed)
        # random_size=False ensures fixed patch size.
        RandSpatialCropd(
            keys=,
            roi_size=patch_size,
            random_size=False
        ),
        
        # Data Augmentation
        # Crucial for GANs to prevent overfitting.
        # We perform rigid augmentations (Flip/Rotate) to preserve anatomy.
        # Note: We do NOT use elastic deformations here as they might introduce 
        # non-physical distortions that confuse the Super-Resolution task.
        RandFlipd(keys=, prob=0.5, spatial_axis=0),
        RandFlipd(keys=, prob=0.5, spatial_axis=1),
        RandFlipd(keys=, prob=0.5, spatial_axis=2),
        RandRotate90d(keys=, prob=0.25, spatial_axes=(0, 1)),
        
        # Final Tensor Conversion
        EnsureTyped(keys=, dtype="float32")
    ])
    
    # 3. CacheDataset
    # This loads all NIfTI files into RAM (if cache_rate=1.0).
    # This removes disk I/O bottlenecks during training.
    # For massive datasets (HCP), adjust cache_rate or use PersistentDataset (disk cache).
    ds = CacheDataset(
        data=data_dicts, 
        transform=train_transforms, 
        cache_rate=1.0, 
        num_workers=num_workers
    )
    
    loader = DataLoader(
        ds, 
        batch_size=batch_size, 
        shuffle=True, 
        num_workers=num_workers,
        pin_memory=True # Faster transfer to GPU
    )
    
    return loader