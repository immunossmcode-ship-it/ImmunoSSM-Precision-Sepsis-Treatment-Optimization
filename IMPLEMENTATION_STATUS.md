# Implementation status and reproducibility boundary

## Purpose

This repository encodes the proposed ImmunoSSM research procedure and provides a modular starting point for implementation. It does not claim that every method in the manuscript is already implemented end to end.

## Components represented in the source tree

- MIRM stream encoders and gated fusion interfaces
- HiPPO-LegS matrix construction and persistent state-space module scaffold
- Temporal preprocessing utilities
- SCIG graph container and stabilized IPTW utility
- Conditional flow building block
- PTON policy-network scaffold and policy regularization utilities
- Data preparation, training, evaluation, and inference entry points

## Work required before claiming a complete reproduction

- Implement and validate exact MIMIC-IV/eICU-CRD SQL, item identifiers, variable harmonization, and cohort flow.
- Verify all 47 channel definitions, temporal aggregation, missingness handling, outcome definitions, and intervention timing.
- Complete the manuscript-specific biomarker exponential-decay initialization and freshness calculation.
- Complete and test the specified intervention temporal encoding and exact gated-fusion formulation.
- Verify HiPPO-LegS matrix convention and implement the full persistence-gate, adaptive ZOH, FFT, and selective-modulation formulation.
- Implement the full PC algorithm, conditional-independence procedure, BIC selection, and clinical graph constraints.
- Implement treatment-specific propensity models, stabilization, truncation, overlap, and balance diagnostics.
- Implement the complete conditional masked autoregressive flow and its manuscript-defined weighted objective.
- Implement the full doubly robust policy estimator, value/action-value learning, behavior cloning, KL constraint, and action discretization.
- Connect the full multi-task training loop, validation-only hyperparameter selection, checkpointing, and patient-level evaluation.
- Add tests for every module and run the full pipeline on authorized data.

## No fabricated results

No manuscript performance numbers, synthetic performance tables, patient-level examples, or trained weights are included as repository outputs. Test fixtures, where used, are software-only and must never be presented as clinical or experimental observations.

## Configuration policy

Numerical settings explicitly stated in the manuscript are externalized in YAML. Missing or ambiguous values are `null`; they must be supplied from the authors' verified code or study records. Do not fill them with guesses. Mathematical constants intrinsic to algorithm definitions remain in the relevant mathematical implementation.
