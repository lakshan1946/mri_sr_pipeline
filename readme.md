# 📘 Project Documentation: 3D MRI Super-Resolution Pipeline

This pipeline is designed to transform raw, heterogeneous MRI scans into paired **High-Resolution (HR)** and **Low-Resolution (LR)** tensors suitable for training advanced generative models like WGAN-GP or Swin UNETR.

---

## 1. System Architecture

The pipeline operates on the principle of **Physics-Informed Degradation**. We do not simply downsample images; we mathematically simulate the MRI acquisition process to create realistic Low-Resolution inputs.

### The Workflow

1.  **Ingestion:** Load raw NIfTI files (`.nii.gz`).
2.  **Brain Extraction (HD-BET):** Removes non-brain tissue (skull stripping).
3.  **Standardization:**
    *   **Reorientation:** Align voxel axes to a standard neurological orientation (RAI/LPI).
4.  **Physics Simulation (Degradation):**
    *   We generate multiple LR variants from the raw data *before* other processing to preserve realistic artifacts.
    *   **Thick Slices (PVE):** Simulates slice averaging via Slab Integration (not just Gaussian blur).
    *   **Inter-Slice Gaps:** Simulates loss of information between slices.
    *   **Low In-Plane Resolution:** Simulates K-space truncation (Gibbs ringing).
5.  **Refinement (Applied to both HR and LR):**
    *   **Bias Correction:** Remove scanner-induced intensity inhomogeneity (N4ITK).
    *   **Normalization:** Intensity normalization (WhiteStripe or Z-Score) to standard scales.
6.  **Registration:** 
    *   Rigidly align the HR brain to the **MNI152 Template**.
    *   Register the LR variants to the *registered HR* image, ensuring perfect pixel-wise alignment (Paired Data) while maintaining the degradation characteristics.

---

## 2. Configuration (`configs/config.yaml`)

The pipeline is fully configurable. The simulation section supports creating multiple synthetic datasets in one run.

```yaml
preprocessing:
  brain_extraction:
    enabled: true
    device: "cpu"  # Options: cuda, cpu, mps
    disable_tta: true  # Disable for speed
  
  normalization:
    method: "whitestripe" # Options: whitestripe, zscore

simulation:
  # 1. Thick Slice Simulation (e.g., Clinical scans)
  thick_slices:
    - 3.0 # Generates 3mm thick slices
    - 4.0 # Generates 4mm thick slices

  # 2. Slice Gap Simulation (e.g., Fast spin echo)
  inter_slice_gap:
    - thickness: 3.0
      gap: 1.0 # 3mm slice + 1mm gap
    - thickness: 3.0
      gap: 0.5 # 3mm slice + 0.5mm gap

  # 3. Low In-Plane Resolution (e.g., Quick scouts)
  in_plane_resolution:
    - 2 # Downsample factor of 2 (K-space truncation)
```

## 3. Environment Setup Guide

**Critical Note on Dependencies:** Medical imaging libraries (ANTs) rely on C++ backends that are sensitive to Python versions. As of 2025, **Python 3.10** is the most stable version for `antspyx` wheels.

### Step-by-Step Conda Setup

```bash
# 1. Create a clean environment with Python 3.10
conda create -n mri_sr_env python=3.10 -y
conda activate mri_sr_env

# 2. Install PyTorch ecosystem
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia

# 3. Install Core Scientific Stack
conda install numpy scipy pandas scikit-learn matplotlib pyyaml -y

# 4. Install ANTsPy (Advanced Normalization Tools)
pip install antspyx

# 5. Install Intensity-Normalization
pip install "intensity-normalization[ants]"

# 6. Install MONAI
pip install "monai[nibabel,tqdm]" simpleitk

# 7. Install Brain Extraction Tool (HD-BET)
pip install HD-BET
```

## 4. Usage

Run the pipeline using the provided entry point:

```bash
conda activate mri_sr_env
python main.py --config ./configs/config.yaml
```

**Outputs:**
- `data/processed/HR`: High-resolution registered images.
- `data/processed/LR`: Paired Low-resolution images (suffixed with degradation type, e.g., `_thick_3mm.nii.gz`).
