# ImmunoSSM: Research Implementation Repository

This repository organizes the proposed **ImmunoSSM** research workflow described in the R2 manuscript:

*ImmunoSSM: A HiPPO-Initialized Persistent State-Space Framework with Causal Immunodynamic Trajectory Learning for Precision Sepsis Treatment Optimization.*

It provides code modules, configuration templates, data-access guidance, and workflow entry points. It does **not** contain patient data, trained model weights, fabricated experimental outputs, or precomputed performance claims. It must not be described as a complete validated reproduction until all items in `IMPLEMENTATION_STATUS.md` are completed and independently tested.

## Proposed research procedure

1. **Access and cohort construction:** Obtain authorized MIMIC-IV v2.2 and eICU-CRD v2.0 access. Apply the manuscript's Sepsis-3 cohort criteria and exclusions. Implement and document database-specific SQL and item mappings locally.
2. **Temporal harmonization:** Establish the index time and hourly observation sequence over the manuscript-defined observation horizon. Keep patient/admission grouping intact.
3. **Leakage-controlled preprocessing:** Derive imputation priors, biomarker decay initialization, feature normalization, treatment quantiles, and other fitted preprocessing statistics from the relevant MIMIC-IV training fold only. Freeze those statistics for validation and external eICU-CRD application.
4. **MIRM representation:** Encode vital signs, irregularly observed biomarkers with freshness/confidence information, and intervention events in separate streams. Apply gated cross-modal fusion to obtain the unified representation.
5. **PSTE temporal modelling:** Initialize the state transition using HiPPO-LegS; apply learnable persistence gates, adaptive zero-order-hold discretization, FFT-based sequence computation, and input-dependent selective modulation as specified in the manuscript.
6. **SCIG causal structure:** Learn the constrained graph using the manuscript's PC/conditional-independence and BIC procedure. Estimate treatment propensities and stabilized inverse-probability weights. Assess positivity, overlap, weight behavior, and post-weighting balance.
7. **CTS counterfactual synthesis:** Fit the conditional masked autoregressive flow using the manuscript's weighting and training objective. Generate counterfactual trajectories for the specified treatment contrasts and estimate individualized treatment effects.
8. **PTON policy learning:** Construct the vasopressor, fluid, and antimicrobial action domains from development data. Train the behavior policy and conservative doubly robust offline policy objective with the stated KL constraint.
9. **Joint optimization:** Train the specified prediction, trajectory, propensity, counterfactual, and policy-related objectives using the manuscript's training protocol. Select hyperparameters using training/validation data only.
10. **Evaluation:** Conduct the internal MIMIC-IV development evaluation and the independent eICU-CRD external evaluation. Report only metrics computed by actually running the validated pipeline; this repository supplies no experimental results.

## Manuscript-grounded settings

Settings explicitly stated in the R2 manuscript are recorded in `configs/`. Settings not legible, fully specified, or operationally defined in the supplied manuscript are left as `null` and must be obtained from the authors' verified implementation. Do not infer or fabricate them.

The R2 text describes five-fold MIMIC-IV cross-validation and also mentions a 70:10:20 split in a baseline-evaluation passage. These are not silently merged: see `configs/evaluation_config.yaml` and confirm their intended separate roles before experiments.

## Repository layout

```text
configs/       Study and model configuration templates
data/          Data-access and local-data instructions (no patient data)
docs/          Architecture, implementation, data-access documentation
scripts/       Cohort preparation, training, evaluation, inference entry points
src/           Modular ImmunoSSM source code
tests/         Basic software-contract tests
```

## Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Data protection

MIMIC-IV and eICU-CRD are controlled-access resources. This repository does not redistribute either dataset. Store authorized extracts outside version control and never commit patient-level records, identifiers, credentials, or access tokens.

## Implementation status and scientific boundaries

Read `IMPLEMENTATION_STATUS.md` before running experiments. Some modules are scaffolds and require completion: database-specific cohort extraction, full PC/BIC graph discovery, complete conditional autoregressive flow training, doubly robust policy estimation, and end-to-end multi-task training/evaluation. The code is a research workflow starting point, not a validated clinical decision system.

All causal estimates are conditional on the assumptions and limitations stated in the manuscript, including consistency, positivity, and sequential ignorability. Outputs are retrospective research estimates and must not be used as clinical treatment instructions.
