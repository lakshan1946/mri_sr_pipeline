"""
Test script for MRI histogram visualization.
This script demonstrates how to use the show_mri_histogram function.
"""

from src.visualization import show_mri_histogram, compare_mri_histograms
from pathlib import Path


def main():
    # Example 1: Display histogram for a single MRI scan
    # Replace this path with your actual .nii.gz file path
    mri_file = "data/your_scan.nii.gz"  # UPDATE THIS PATH
    
    # Check if you have any data files
    data_dir = Path("data")
    if data_dir.exists():
        # Find all .nii.gz files in the data directory
        nii_files = list(data_dir.rglob("*.nii.gz"))
        
        if nii_files:
            print(f"Found {len(nii_files)} .nii.gz files in data directory")
            
            # Use the first file found
            mri_file = nii_files[0]
            print(f"\nAnalyzing: {mri_file}")
            
            # Display histogram
            stats = show_mri_histogram(
                input_file=mri_file,
                bins=100,
                title=None,  # Will use filename as title
                save_path=None  # Set to a path if you want to save the image
            )
            
            # You can also save the histogram
            # save_path = "results/histogram.png"
            # stats = show_mri_histogram(mri_file, save_path=save_path)
            
            # Example 2: Compare multiple scans (if you have more than one)
            if len(nii_files) > 1:
                print("\n" + "="*50)
                print("Comparing multiple scans...")
                print("="*50)
                
                # Compare first 3 files (or fewer if less available)
                files_to_compare = nii_files[:min(3, len(nii_files))]
                
                compare_stats = compare_mri_histograms(
                    file_list=files_to_compare,
                    labels=[f"Scan {i+1}" for i in range(len(files_to_compare))],
                    title="MRI Scan Comparison"
                )
                
                print("\nComparison Statistics:")
                for label, stats in compare_stats.items():
                    print(f"{label}: Mean={stats['mean']:.2f}, Std={stats['std']:.2f}")
        else:
            print("No .nii.gz files found in data directory!")
            print("Please add your MRI scan files to the 'data' folder or update the path in this script.")
    else:
        print("Data directory not found!")
        print("Please create a 'data' folder and add your .nii.gz MRI scan files there,")
        print("or update the mri_file path in this script.")


if __name__ == "__main__":
    main()
