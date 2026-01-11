# MRI Histogram Visualization Guide

## Overview

The `src/visualization.py` module provides functions to visualize intensity distributions of MRI scans (.nii.gz files) using histograms. This is useful for:

- Understanding intensity distributions in MRI data
- Quality control and validation
- Comparing pre-processing vs post-processing results
- Analyzing the effects of different degradation simulations
- Identifying potential artifacts or normalization issues

## Functions

### 1. `show_mri_histogram()`

Display the intensity distribution of a single MRI scan.

**Parameters:**
- `input_file` (str or Path): Path to the .nii.gz MRI file
- `bins` (int, optional): Number of histogram bins (default: 100)
- `title` (str, optional): Custom plot title (default: uses filename)
- `save_path` (str or Path, optional): Path to save the image (default: None - displays only)
- `figsize` (tuple, optional): Figure size in inches (default: (12, 6))

**Returns:**
- Dictionary containing statistics: `mean`, `std`, `min`, `max`, `median`, `data`, `total_voxels`, `non_zero_voxels`

**Example:**
```python
from src.visualization import show_mri_histogram

# Basic usage
stats = show_mri_histogram('data/raw/scan.nii.gz')

# With custom parameters
stats = show_mri_histogram(
    input_file='data/processed/HR/scan.nii.gz',
    bins=150,
    title='My Custom Title',
    save_path='results/my_histogram.png'
)

# Access statistics
print(f"Mean intensity: {stats['mean']:.2f}")
print(f"Standard deviation: {stats['std']:.2f}")
```

### 2. `compare_mri_histograms()`

Compare intensity distributions of multiple MRI scans in a single plot.

**Parameters:**
- `file_list` (list): List of paths to .nii.gz MRI files
- `labels` (list, optional): Labels for each file (default: uses filenames)
- `bins` (int, optional): Number of histogram bins (default: 100)
- `title` (str, optional): Plot title (default: "MRI Comparison")
- `save_path` (str or Path, optional): Path to save the image (default: None)

**Returns:**
- Dictionary with statistics for each file

**Example:**
```python
from src.visualization import compare_mri_histograms

# Compare two scans
files = [
    'data/processed/HR/scan.nii.gz',
    'data/processed/LR/scan_degraded.nii.gz'
]

stats = compare_mri_histograms(
    file_list=files,
    labels=['Original', 'Degraded'],
    title='Before vs After Degradation',
    save_path='results/comparison.png'
)
```

## Usage in mri_sr_env

Make sure to activate the conda environment before running:

```bash
# Activate environment
conda activate mri_sr_env

# Run test script
python test_histogram.py

# Or run examples
python examples/visualize_mri_histogram.py
```

## Output Description

### Histogram Plot

The `show_mri_histogram()` function creates a two-panel figure:

1. **Left Panel - Histogram:**
   - Shows frequency distribution of intensity values
   - Red dashed line: Mean intensity
   - Green dashed line: Median intensity
   - Only includes non-zero voxels (background excluded)

2. **Right Panel - Box Plot:**
   - Visualizes distribution quartiles
   - Shows outliers
   - Red line indicates median

3. **Statistics Box:**
   - Displays computed statistics on the right side
   - Shows total and non-zero voxel counts

### Comparison Plot

The `compare_mri_histograms()` function creates an overlapping histogram showing multiple scans with different colors for easy comparison.

## Key Features

### Automatic Background Removal
Both functions automatically exclude zero-intensity voxels (typically background) for more meaningful visualization of actual tissue intensities.

### High-Quality Output
- 300 DPI resolution when saving
- Clean, professional styling
- Customizable figure sizes

### Statistical Analysis
Get detailed statistics including:
- Mean, median, standard deviation
- Min/max values
- Total voxel count
- Non-zero voxel count and percentage

## Common Use Cases

### 1. Quality Control
```python
# Check if normalization worked correctly
show_mri_histogram(
    'data/processed/intermediate/subject/scan_04_hr_norm.nii.gz',
    title='After Normalization - QC'
)
```

### 2. Pipeline Validation
```python
# Compare before and after preprocessing
files = [
    'data/raw/scan.nii.gz',
    'data/processed/HR/scan.nii.gz'
]
compare_mri_histograms(files, labels=['Raw', 'Processed'])
```

### 3. Degradation Analysis
```python
# Compare different degradation levels
files = [
    'data/processed/HR/scan.nii.gz',
    'data/processed/LR/scan_thick_3mm.nii.gz',
    'data/processed/LR/scan_thick_5mm.nii.gz'
]
compare_mri_histograms(
    files, 
    labels=['Original', '3mm thick', '5mm thick'],
    title='Slice Thickness Effects'
)
```

## Tips

1. **Choose appropriate bin counts:** 
   - Use 50-100 bins for general visualization
   - Use 150+ bins for detailed analysis
   - Fewer bins (25-50) for comparison plots

2. **Always save important visualizations:**
   ```python
   show_mri_histogram(file, save_path='results/important_result.png')
   ```

3. **Use meaningful labels** when comparing multiple scans

4. **Check statistics programmatically:**
   ```python
   stats = show_mri_histogram(file)
   if stats['mean'] < expected_threshold:
       print("Warning: Unexpected mean intensity!")
   ```

## Dependencies

The visualization module requires:
- `numpy`
- `matplotlib`
- `nibabel`
- `pathlib` (standard library)

All dependencies should already be installed in the `mri_sr_env` conda environment.
