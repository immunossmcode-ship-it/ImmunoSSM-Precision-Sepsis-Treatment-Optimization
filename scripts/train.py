import argparse
from pathlib import Path
import torch
import yaml
from immunossm.model import ImmunoSSM

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="Prepared training data path")
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    config = yaml.safe_load(Path(args.config).read_text())
    model = ImmunoSSM(config)
    print(model)
    print("Model constructed. Connect the validated patient-trajectory Dataset/DataLoader,")
    print("configured multi-task targets, optimizer, scheduler, and validation-only selection.")
    print("No training or performance claim is made by this initialization script.")
if __name__ == "__main__":
    main()
