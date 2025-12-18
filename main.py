# main.py
from src.pipeline import MRIPreprocessingPipeline
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MRI Super-Resolution Preprocessing")
    parser.add_argument("--config", type=str, default="./configs/config.yaml", help="Path to config")
    args = parser.parse_args()

    # Instantiate and Run
    pipeline = MRIPreprocessingPipeline(args.config)
    pipeline.run_batch()
    
    print("Pipeline complete. Data ready for WGAN training.")