import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    if not Path(args.checkpoint).exists():
        raise FileNotFoundError(args.checkpoint)
    if not Path(args.input).exists():
        raise FileNotFoundError(args.input)
    print("Input and checkpoint located. Connect the same fitted preprocessing state")
    print("and model input contract used during training.")
    print("Outputs are research estimates, not clinical treatment instructions.")
if __name__ == "__main__":
    main()
