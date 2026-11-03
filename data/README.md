# Data directory

Do not commit MIMIC-IV, eICU-CRD, patient-level extracts, or derived patient-level trajectories.

Store locally:
- licensed source extracts;
- intermediate patient-time tables;
- train/validation/test partitions;
- model outputs and checkpoints.

These paths are excluded by `.gitignore`. Share only data dictionaries, extraction SQL templates, and synthetic unit-test fixtures that contain no real patient information.
