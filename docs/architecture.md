# Architecture and stage-wise implementation

## Stage A — Data acquisition and cohort construction
Acquire MIMIC-IV and eICU-CRD under the applicable PhysioNet approvals. Implement database-version-specific SQL using the manuscript's Sepsis-3 operational definition, eligibility criteria, index time, exclusion rules, and follow-up. Keep the patient/admission identifiers needed for grouped splitting locally; never publish row-level records.

## Stage B — Temporal preprocessing
Construct the configured longitudinal time grid. Sort observations by patient and time. Fit medians, means, standard deviations, and any empirical treatment/action cut-points using the training partition only. Apply those frozen statistics to validation, test, and external cohorts. Use biomarker-specific exponential decay and observation-freshness/confidence channels as specified by the manuscript. The supplied preprocessor is a starting implementation and must be checked against the exact time units and imputation equations.

## Stage C — MIRM
Encode vital signs with a causal temporal convolutional stream; encode asynchronous biomarkers using values plus confidence/freshness information; encode intervention events/doses separately. Project streams into compatible representations, learn modality gates, and fuse them using attention and a feed-forward residual block.

## Stage D — PSTE
Initialize the continuous-time state transition using the manuscript's HiPPO-LegS convention. Apply learnable persistence gates, input-dependent modulation, and discretization consistent with the stated sampling interval. The included recurrent implementation is a transparent reference path; verify its matrix convention and ZOH input integral against the manuscript equations before treating it as the final numerical implementation. A production implementation should test stability and compare recurrence and convolution/FFT paths.

## Stage E — SCIG and SIPTW
Define the node dictionary, allowed/forbidden edges, and temporal ordering from the manuscript's causal assumptions. Estimate a graph using the specified conditional-independence procedure and apply structural constraints. Estimate treatment propensities from observed pre-treatment history, calculate stabilized weights, inspect positivity/overlap, truncate using training-derived bounds, and report covariate balance. The graph class in this repository validates and stores a supplied directed graph; it does not claim to implement the full PC discovery algorithm. Connect a validated PC/BIC backend before claiming that stage is reproduced.

## Stage F — CTS
Condition the counterfactual generator on patient history, causal parents, and an explicit intervention sequence. Train with the manuscript's IPTW-weighted objective. The supplied conditional affine flow is a reusable building block, not a complete reproduction of a masked autoregressive flow until masking order, likelihood objective, conditioning variables, and optimization are aligned with the paper.

## Stage G — PTON
Represent each treatment modality using action bins derived from the development cohort according to the manuscript's quantile definition. Train the behavior policy on logged clinician actions. Optimize the target policy using the specified doubly robust off-policy objective and constrain divergence from the behavior policy. The included network provides categorical policy heads, behavior cloning, and KL regularization; connect the full DR estimator, value/Q estimators, and reward construction from the manuscript before claiming full PTON reproduction.

## Stage H — Joint optimization and evaluation
Connect mortality, trajectory forecasting, propensity, CTS, and policy losses with the manuscript's task definitions. Select hyperparameters on validation data only. Keep patient groups disjoint. Evaluate internal held-out data and eICU-CRD externally, using the prespecified metrics and patient-level inference. Do not place reported metrics in source code.
