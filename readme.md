This pipeline is designed to transform raw, heterogeneous MRI scans into paired **High-Resolution (HR)** and **Low-Resolution (LR)** tensors suitable for training advanced generative models like WGAN-GP or Swin UNETR.

---

# 📘 Project Documentation: 3D MRI Super-Resolution Pipeline

## 1. System Architecture

The pipeline operates on the principle of  **Physics-Informed Degradation** . We do not simply downsample images; we mathematically simulate the MRI acquisition process (Partial Volume Effect) to create realistic Low-Resolution inputs.

### The Workflow

1. **Ingestion:** Load raw NIfTI files (`.nii.gz`).
2. **Standardization:**
   * **Reorientation:** Align voxel axes to a standard neurological orientation (RAI/LPI).
   * **Bias Correction:** Remove scanner-induced intensity inhomogeneity (N4ITK).
3. **Registration:** Rigidly align the brain to the  **MNI152 Template** . This standardizes head position without altering patient-specific anatomy.
4. **Normalization (WhiteStripe):** A biological normalization technique that maps "Normal Appearing White Matter" (NAWM) to a fixed intensity value (1.0), ensuring statistical consistency across patients.
5. **Physics Simulation (The "Thick Slice" Model):**
   * Apply **Anisotropic Gaussian Blurring** along the slice-select axis (Z-axis).
   * Downsample to the target slice thickness (e.g., 5mm).
   * Upsample (B-Spline) back to the HR grid to create the paired LR input.
6. **Tensor Formatting:** Convert processed pairs into 3D patches for Deep Learning using MONAI.

---

## 2. Environment Setup Guide

**Critical Note on Dependencies:** Medical imaging libraries (ANTs) rely on C++ backends that are sensitive to Python versions. As of 2025, **Python 3.10** is the most stable version for `antspyx` wheels. Newer versions (3.11+) often require manual compilation.

### Step-by-Step Conda Setup

**Bash**

```
# 1. Create a clean environment with Python 3.10 (Standard for Medical AI)
conda create -n mri_sr_env python=3.10 -y
conda activate mri_sr_env

# 2. Install PyTorch ecosystem (Check your CUDA version, e.g., 11.8 or 12.x)
# We install this FIRST to ensure GPU support is correctly linked.
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia

# 3. Install Core Scientific Stack
conda install numpy scipy pandas scikit-learn matplotlib pyyaml -y

# 4. Install ANTsPy (Advanced Normalization Tools)
# We use pip because ANTsPy wheels are best maintained on PyPI.
pip install antspyx

# 5. Install Intensity-Normalization
# The [ants] extra ensures compatibility with ANTs images.
pip install "intensity-normalization[ants]"

# 6. Install MONAI (Medical Open Network for AI)
# Used for high-performance data loading and patch extraction.
pip install "monai[nibabel,tqdm]" simpleitk
```
