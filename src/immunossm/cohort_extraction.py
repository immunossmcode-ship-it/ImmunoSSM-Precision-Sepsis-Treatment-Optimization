"""Database-specific cohort extraction adapter.

The manuscript defines the cohort rules, but exact SQL item identifiers and
schema mappings depend on the licensed database release and local extract.
This module deliberately avoids inventing SQL mappings.
"""
from pathlib import Path

def load_extracted_cohort(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Expected locally extracted cohort file: {path}")
    if path.suffix.lower() == ".parquet":
        import pandas as pd
        return pd.read_parquet(path)
    if path.suffix.lower() == ".csv":
        import pandas as pd
        return pd.read_csv(path)
    raise ValueError("Use a supported tabular extract (CSV or Parquet).")

def validate_cohort_contract(frame, patient_key, time_key, required_columns):
    required = {patient_key, time_key, *required_columns}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Cohort extract is missing configured columns: {sorted(missing)}")
    if frame[patient_key].isna().any() or frame[time_key].isna().any():
        raise ValueError("Patient key and time must be present.")
    return frame
