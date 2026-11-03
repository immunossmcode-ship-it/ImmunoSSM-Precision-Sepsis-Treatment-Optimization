# Data access and handling

MIMIC-IV and eICU-CRD are controlled-access clinical datasets. Obtain access directly from PhysioNet and comply with each dataset's credentialing, training, and data-use requirements. This repository does not redistribute either dataset.

## Local workflow

1. Obtain approved access independently.
2. Download/use the database only through the authorized route.
3. Map the source schema and item identifiers to the manuscript's variables.
4. Execute local cohort extraction SQL implementing the manuscript's exact inclusion/exclusion and index-time rules.
5. Export a local patient-time table conforming to the configured data contract.
6. Keep raw and derived patient-level files outside version control.

The manuscript-specific SQL, item identifiers, and endpoint construction are not fully inferable from generic table names alone. Complete them against the database release and the study's original extraction scripts; do not substitute guessed mappings.
