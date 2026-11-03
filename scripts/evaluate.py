import argparse
from pathlib import Path
import torch

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--data", required=True)
    args = parser.parse_args()
    checkpoint = Path(args.checkpoint)
    if not checkpoint.exists():
        raise FileNotFoundError(checkpoint)
    print("Checkpoint found. Implement endpoint-specific evaluation using held-out patient groups.")
    print("Do not tune thresholds or select checkpoints using the test/external-validation set.")
if __name__ == "__main__":
    main()
