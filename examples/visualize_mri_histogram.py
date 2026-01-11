"""
Example script demonstrating various ways to use the MRI histogram visualization functions.

This module provides examples for:
1. Simple histogram display
2. Saving histograms to disk
3. Comparing multiple MRI scans
4. Analyzing different processing stages
"""

from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.visualization import show_mri_histogram, compare_mri_histograms


def example_1_basic_histogram():
    """Example 1: Display a basic histogram for a single MRI scan."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Histogram Display")
    print("="*60)
    
    # Use the raw MRI scan
    mri_file = Path("data/raw/100206_3T_T2w_SPC1.nii.gz")
    
    if mri_file.exists():
        stats = show_mri_histogram(
            input_file=mri_file,
            bins=100,
            title="Raw MRI Scan - Intensity Distribution"
        )
        
        # Access the returned statistics
        print(f"\nReturned statistics object allows programmatic access:")
        print(f"  - Mean: {stats['mean']:.2f}")
        print(f"  - Std:  {stats['std']:.2f}")
    else:
        print(f"File not found: {mri_file}")


def example_2_save_histogram():
    """Example 2: Save histogram to a file."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Save Histogram to File")
    print("="*60)
    
    mri_file = Path("data/processed/HR/100206_3T_T2w_SPC1.nii.gz")
    output_dir = Path("results/visualizations")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if mri_file.exists():
        stats = show_mri_histogram(
            input_file=mri_file,
            bins=150,
            title="High-Resolution MRI - Processed",
            save_path=output_dir / "hr_histogram.png"
        )
        print(f"\n[SUCCESS] Histogram saved successfully!")
    else:
        print(f"File not found: {mri_file}")


def example_3_compare_lr_vs_hr():
    """Example 3: Compare Low-Resolution vs High-Resolution scans."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Compare LR vs HR Scans")
    print("="*60)
    
    hr_file = Path("data/processed/HR/100206_3T_T2w_SPC1.nii.gz")
    lr_file = Path("data/processed/LR/100206_3T_T2w_SPC1_thick_3mm.nii.gz")
    
    if hr_file.exists() and lr_file.exists():
        stats = compare_mri_histograms(
            file_list=[hr_file, lr_file],
            labels=["High Resolution", "Low Resolution (3mm thick)"],
            bins=100,
            title="HR vs LR Intensity Distribution Comparison",
            save_path="results/visualizations/hr_vs_lr_comparison.png"
        )
        
        print("\nComparison Results:")
        for label, stat_dict in stats.items():
            print(f"\n{label}:")
            print(f"  Mean:   {stat_dict['mean']:.2f}")
            print(f"  Std:    {stat_dict['std']:.2f}")
            print(f"  Median: {stat_dict['median']:.2f}")
    else:
        print("One or more files not found!")


def example_4_processing_pipeline_stages():
    """Example 4: Compare different processing stages."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Compare Processing Pipeline Stages")
    print("="*60)
    
    # Compare different stages of the same scan
    subject = "100206_3T_T2w_SPC1"
    intermediate_dir = Path(f"data/processed/intermediate/{subject}")
    
    stages = {
        "Brain Extracted": f"{subject}_00_brain_extracted.nii.gz",
        "Reoriented": f"{subject}_01_raw_reoriented.nii.gz",
        "N4 Corrected": f"{subject}_03_hr_n4.nii.gz",
        "Normalized": f"{subject}_04_hr_norm.nii.gz",
    }
    
    file_list = []
    labels = []
    
    for label, filename in stages.items():
        filepath = intermediate_dir / filename
        if filepath.exists():
            file_list.append(filepath)
            labels.append(label)
    
    if len(file_list) > 1:
        stats = compare_mri_histograms(
            file_list=file_list,
            labels=labels,
            bins=100,
            title="MRI Processing Pipeline - Intensity Changes Across Stages",
            save_path="results/visualizations/pipeline_stages_comparison.png"
        )
        
        print(f"\n[SUCCESS] Compared {len(file_list)} processing stages")
    else:
        print("Intermediate files not found!")


def example_5_multiple_degradations():
    """Example 5: Compare different degradation types."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Compare Different Degradation Types")
    print("="*60)
    
    lr_dir = Path("data/processed/LR")
    
    degradations = {
        "Original HR": Path("data/processed/HR/100206_3T_T2w_SPC1.nii.gz"),
        "Thick Slice (3mm)": lr_dir / "100206_3T_T2w_SPC1_thick_3mm.nii.gz",
        "Thick Slice (5mm)": lr_dir / "100206_3T_T2w_SPC1_thick_5mm.nii.gz",
        "In-plane DS 1": lr_dir / "100206_3T_T2w_SPC1_inplane_ds1.nii.gz",
    }
    
    file_list = []
    labels = []
    
    for label, filepath in degradations.items():
        if filepath.exists():
            file_list.append(filepath)
            labels.append(label)
    
    if len(file_list) > 1:
        stats = compare_mri_histograms(
            file_list=file_list,
            labels=labels,
            bins=100,
            title="Degradation Effects on Intensity Distribution",
            save_path="results/visualizations/degradation_comparison.png"
        )
        
        print(f"\n[SUCCESS] Compared {len(file_list)} degradation types")
    else:
        print("LR files not found!")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("MRI HISTOGRAM VISUALIZATION EXAMPLES")
    print("="*60)
    
    # Create results directory
    Path("results/visualizations").mkdir(parents=True, exist_ok=True)
    
    # Run examples
    example_1_basic_histogram()
    example_2_save_histogram()
    example_3_compare_lr_vs_hr()
    example_4_processing_pipeline_stages()
    example_5_multiple_degradations()
    
    print("\n" + "="*60)
    print("ALL EXAMPLES COMPLETED!")
    print("="*60)
    print("\nCheck the 'results/visualizations' folder for saved images.")


if __name__ == "__main__":
    main()
