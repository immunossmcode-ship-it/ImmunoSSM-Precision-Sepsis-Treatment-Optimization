# Implementation workflow

Follow the numbered research procedure in the repository README and the module-specific requirements in `IMPLEMENTATION_STATUS.md`.

The code is organized as a staged pipeline:
1. Authorized cohort extraction and variable harmonization.
2. Leakage-controlled temporal preprocessing.
3. MIRM multimodal encoding and gated fusion.
4. HiPPO-initialized PSTE temporal representation.
5. SCIG structure learning and SIPTW diagnostics.
6. CTS conditional counterfactual trajectory generation.
7. PTON conservative offline policy learning.
8. Joint optimization and held-out evaluation.

The scripts are workflow entry points, not proof that all stages are fully connected. Complete and test each study-specific adapter and estimator before running the end-to-end experiment.
