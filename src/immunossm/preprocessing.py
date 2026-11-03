"""Leakage-aware temporal harmonization and biomarker decay imputation."""
import numpy as np
import pandas as pd

class TemporalPreprocessor:
    def __init__(self, patient_key, time_key, vital_cols, biomarker_cols,
                 intervention_cols, decay_rates):
        self.patient_key = patient_key
        self.time_key = time_key
        self.vital_cols = list(vital_cols)
        self.biomarker_cols = list(biomarker_cols)
        self.intervention_cols = list(intervention_cols)
        self.decay_rates = decay_rates
        self.medians_ = None
        self.means_ = None
        self.stds_ = None

    def fit(self, frame):
        features = self.vital_cols + self.biomarker_cols + self.intervention_cols
        self.medians_ = frame[features].median()
        self.means_ = frame[features].mean()
        self.stds_ = frame[features].std().replace(0, 1).fillna(1)
        return self

    def transform(self, frame):
        if self.medians_ is None:
            raise RuntimeError("Fit preprocessing on the training partition first.")
        data = frame.sort_values([self.patient_key, self.time_key]).copy()
        for column in self.vital_cols:
            data[column] = data.groupby(self.patient_key)[column].ffill()
            data[column] = data[column].fillna(self.medians_[column])
        for column in self.biomarker_cols:
            if column not in self.decay_rates:
                raise KeyError(f"Missing configured decay rate for biomarker: {column}")
            rate = self.decay_rates[column]
            if not isinstance(rate, (int, float)):
                raise TypeError(f"Decay rate for {column} must be numeric in runtime config.")
            data[column] = self._decay_impute(data, column, rate)
        for column in self.intervention_cols:
            data[column] = data[column].fillna(0)
        features = self.vital_cols + self.biomarker_cols + self.intervention_cols
        data[features] = (data[features] - self.means_) / self.stds_
        return data

    def _decay_impute(self, frame, column, rate):
        result = frame[column].copy()
        for _, indexes in frame.groupby(self.patient_key).groups.items():
            last_value = np.nan
            last_time = None
            for idx in indexes:
                current = frame.at[idx, column]
                current_time = frame.at[idx, self.time_key]
                if pd.notna(current):
                    last_value, last_time = current, current_time
                elif last_value is not None and last_time is not None:
                    difference = current_time - last_time
                    elapsed = (difference.total_seconds() if hasattr(difference, "total_seconds")
                               else float(difference))
                    result.at[idx] = last_value * np.exp(-rate * elapsed)
                else:
                    result.at[idx] = self.medians_[column]
        return result
