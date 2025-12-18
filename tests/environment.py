import ants
import torch
import monai
import numpy as np
import sys

print(f"Environment Verification:")
print(f"-------------------------")
print(f"Python: {sys.version}")
print(f"ANTsPy: {ants.__version__} (Backend: ITK)")
print(f"PyTorch: {torch.__version__} (CUDA: {torch.cuda.is_available()})")
print(f"MONAI: {monai.__version__}")
print(f"NumPy: {np.__version__}")

# Simple test of ANTsPy-NumPy interoperability
try:
    img = ants.image_read(ants.get_ants_data('r16'))
    arr = img.numpy()
    print("SUCCESS: ANTsPy I/O and NumPy conversion operational.")
except Exception as e:
    print(f"FAILURE: {e}")