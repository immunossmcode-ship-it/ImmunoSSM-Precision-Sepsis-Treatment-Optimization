import argparse
from pathlib import Path
import pandas as pd
import yaml
from immunossm.cohort_extraction import load_extracted_cohort, validate_cohort_contract

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    config = yaml.safe_load(Path(args.config).read_text())
    source = config["source"]["local_extract_path"]
    frame = load_extracted_cohort(source)
    modalities = config["modalities"]
    features = sum((modalities[key] for key in ("vital_signs", "biomarkers", "interventions")), [])
    validate_cohort_contract(frame, config["keys"]["patient"], config["keys"]["timestamp"], features)
    print("Validated source extract. Implement and document the manuscript-specific cohort SQL,")
    print("index-time rules, temporal aggregation, and endpoint construction before modelling.")
    print(f"Rows available in local extract: {len(frame)}")
if __name__ == "__main__":
    main()
