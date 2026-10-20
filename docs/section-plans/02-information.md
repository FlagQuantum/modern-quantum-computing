# Part 2. Quantum Information: Channels, Inference, and Communication

**Detailed plan · 2026-10-20 · Scope fixed by Writing Baseline 1.0; prose and independent acceptance pending.** [All sections](../section-plan.md) · [Full plan](../book-plan.md) · [Reader continuity](../reader-continuity.md)

Each section specifies its argument and independent evidence. Framework implementation, mathematical review and reader review have separate status. Closing materials follow the [section-plan guide](../section-plan.md#how-to-read-the-specification).

<span id="ch-quantum-channels-and-their-representations"></span>

## Chapter 9

**Quantum Channels and Their Representations**

**Reading level:** Core. **Entry guidance:** 8; selected 4–6 for operational examples.

<span id="sec-quantum-channels-and-their-representations-1"></span>

### 9.1 From closed evolution to quantum channels

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-quantum-channels-and-their-representations-1).

**Section level:** core. **Required earlier sections:** [8.3](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-3), [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4).

**Learning and derivation target:** Derive a reduced-system map from an initially specified environment state.

**Implementation and evidence target:** Compare joint unitary evolution and reduced output.

<span id="sec-quantum-channels-and-their-representations-2"></span>

### 9.2 Linearity, positivity, and complete positivity

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-quantum-channels-and-their-representations-2).

**Section level:** core. **Required earlier sections:** [8.2](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2), [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [9.1](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-1).

**Learning and derivation target:** Define each condition and explain the extension by an untouched ancilla.

**Implementation and evidence target:** Use transposition as a counterexample to positivity being sufficient.

<span id="sec-quantum-channels-and-their-representations-3"></span>

### 9.3 Kraus operators and trace preservation

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-quantum-channels-and-their-representations-3).

**Section level:** core. **Required earlier sections:** [9.1](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-1), [9.2](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-2).

**Learning and derivation target:** Derive the operator-sum form and completeness condition.

**Implementation and evidence target:** Verify a simple channel on a spanning set of inputs.

<span id="sec-quantum-channels-and-their-representations-4"></span>

### 9.4 Stinespring dilation

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-quantum-channels-and-their-representations-4).

**Section level:** core. **Required earlier sections:** [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3), [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4).

**Learning and derivation target:** Construct a finite-dimensional dilation and explain environmental freedom.

**Implementation and evidence target:** Recover the channel by explicit partial trace.

<span id="sec-quantum-channels-and-their-representations-5"></span>

### 9.5 Choi representation and vectorization

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-quantum-channels-and-their-representations-5).

**Section level:** core. **Required earlier sections:** [9.2](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-2), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3), [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2).

**Learning and derivation target:** Fix a vectorization convention and derive the channel-to-Choi correspondence.

**Implementation and evidence target:** Check reshuffling indices against explicit basis operators.

<span id="sec-quantum-channels-and-their-representations-6"></span>

### 9.6 Representation equivalence and Kraus nonuniqueness

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-quantum-channels-and-their-representations-6).

**Section level:** core. **Required earlier sections:** [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3), [9.4](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-4), [9.5](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-5).

**Learning and derivation target:** Connect Choi spectral factors, Kraus operators and an environmental isometry.

**Implementation and evidence target:** Convert a small channel between representations and check identical actions.

<span id="sec-quantum-channels-and-their-representations-7"></span>

### 9.7 Composition, tensor products, and instruments

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-quantum-channels-and-their-representations-7).

**Section level:** core. **Required earlier sections:** [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2).

**Learning and derivation target:** Derive channel composition and trace-nonincreasing branches.

**Implementation and evidence target:** Compare sequential, composite and conditional calculations.

<span id="sec-quantum-channels-and-their-representations-8"></span>

### 9.8 Channel-validation laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-quantum-channels-and-their-representations-8).

**Section level:** core. **Required earlier sections:** [9.5](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-5), [9.6](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-6), [9.7](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-7).

**Learning and derivation target:** State physicality and equivalence tests and their finite numerical limits.

**Implementation and evidence target:** Check Choi positivity and partial traces; diagnose a trace-preserving but non-CP map.

<span id="ch-distinguishability-fidelity-and-quantum-state-inference"></span>

## Chapter 10

**Distinguishability, Fidelity, and Quantum State Inference**

**Reading level:** Core. **Entry guidance:** 6, 8–9; advanced channel metrics and shadows are separable branches.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-1"></span>

### 10.1 Classical distinguishability as a starting point

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-1).

**Section level:** core. **Required earlier sections:** [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Learning and derivation target:** Define total-variation distance and its discrimination interpretation.

**Implementation and evidence target:** Compare two finite distributions and an explicit decision rule.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-2"></span>

### 10.2 Quantum trace distance and binary discrimination

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-2).

**Section level:** core. **Required earlier sections:** [10.1](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-1), [8.2](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Learning and derivation target:** Derive the optimal two-state measurement for stated priors.

**Implementation and evidence target:** Compare a spectral construction with independently enumerated candidate measurements.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-3"></span>

### 10.3 Fidelity and state-comparison conventions

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-3).

**Section level:** core. **Required earlier sections:** [8.2](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Learning and derivation target:** Declare squared versus unsquared fidelity and derive pure/commuting cases.

**Implementation and evidence target:** Verify analytic limiting cases and contrast fidelity with elementwise equality.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-4"></span>

### 10.4 Monotonicity and operational limits

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-4).

**Section level:** core. **Required earlier sections:** [10.2](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-2), [10.3](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-3), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3).

**Learning and derivation target:** Explain how channels and restricted measurements affect distinguishability.

**Implementation and evidence target:** Construct a strict information-loss example and an incomplete-measurement counterexample.

<span id="sec-channel-error-metrics"></span>

### 10.5 Comparing channels and gate errors [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-channel-error-metrics).

**Section level:** advanced. **Required earlier sections:** [10.2](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-2), [10.3](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-3), [9.5](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-5).

**Learning and derivation target:** Define channel comparison through inputs/ancillas, entanglement fidelity and a scoped diamond-norm formulation; state any average-fidelity relation with its dimensional and trace-preserving assumptions.

**Implementation and evidence target:** Compare small explicit channels and give a counterexample to inferring worst-case behavior from one state or an average metric.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-5"></span>
<span id="105-quantum-state-tomography"></span>

### 10.6 State and process tomography

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-5).

**Section level:** core. **Required earlier sections:** [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7), [8.3](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-3), [9.5](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-5).

**Learning and derivation target:** Derive qubit-state linear inversion, then a small process reconstruction using the Choi convention from Chapter 9; explain identifiability, positivity and finite-sample limitations.

**Implementation and evidence target:** Reconstruct small states and compare physical versus unconstrained estimates.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-6"></span>
<span id="106-pauli-sums-grouping-and-measurement-allocation"></span>

### 10.7 Pauli sums, grouping, and measurement allocation

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-6).

**Section level:** core. **Required earlier sections:** [6.4](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-4), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Learning and derivation target:** Derive variance/covariance expressions for an estimated weighted observable.

**Implementation and evidence target:** Compare allocation rules under an identical total-shot budget.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-7"></span>
<span id="107-classical-shadows-advanced"></span>

### 10.8 Classical shadows [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-7).

**Section level:** advanced. **Required earlier sections:** [10.6](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-5), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Learning and derivation target:** Define the measurement ensemble, inverse measurement map and property-estimation task.

**Implementation and evidence target:** Check a small Pauli-shadow estimator and report ensemble-dependent uncertainty.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-8"></span>
<span id="108-inference-laboratory-and-validation-limits"></span>

### 10.9 Inference laboratory and validation limits

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-8).

**Section level:** core. **Required earlier sections:** [10.2](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-2), [10.3](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-3), [10.6](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-5), [10.7](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-6).

**Learning and derivation target:** Separate state reconstruction, property prediction and certification claims.

**Implementation and evidence target:** Report estimation error across repeated trials and identify unmeasured degrees of freedom.

<span id="ch-entropy-relative-entropy-and-information-processing"></span>

## Chapter 11

**Entropy, Relative Entropy, and Information Processing**

**Reading level:** Core with advanced proofs. **Entry guidance:** 8 and the state-comparison sections of 10; logarithm identities are introduced locally.

<span id="sec-entropy-relative-entropy-and-information-processing-1"></span>

### 11.1 Classical entropy and uncertainty

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-1).

**Section level:** core. **Required earlier sections:** [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Learning and derivation target:** Introduce the required logarithm and expectation identities locally, then define Shannon entropy and derive basic finite-distribution properties.

**Implementation and evidence target:** Compare deterministic, uniform and correlated examples.

<span id="sec-entropy-relative-entropy-and-information-processing-2"></span>

### 11.2 Von Neumann entropy and spectra

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-2).

**Section level:** core. **Required earlier sections:** [11.1](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-1), [8.2](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2).

**Learning and derivation target:** Derive the spectral formula and unitary invariance.

**Implementation and evidence target:** Compute mixed-state examples and verify pure-state limits.

<span id="sec-entropy-relative-entropy-and-information-processing-3"></span>

### 11.3 Relative entropy and support conditions

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-3).

**Section level:** core. **Required earlier sections:** [11.1](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-1), [11.2](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-2).

**Learning and derivation target:** State classical and quantum definitions with support and infinity conventions.

**Implementation and evidence target:** Test commuting reductions, singular states and numerically unstable cases.

<span id="sec-entropy-relative-entropy-and-information-processing-4"></span>

### 11.4 Mutual and conditional information

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-4).

**Section level:** core. **Required earlier sections:** [11.2](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-2), [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4).

**Learning and derivation target:** Derive the entropy identities and interpret classical and entangled examples.

**Implementation and evidence target:** Compare classical correlations with negative quantum conditional entropy.

<span id="sec-entropy-relative-entropy-and-information-processing-5"></span>

### 11.5 Data processing

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-5).

**Section level:** core. **Required earlier sections:** [11.3](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-3), [11.4](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-4), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3).

**Learning and derivation target:** State operational assumptions, prove a tractable case and map the general proof requirements.

**Implementation and evidence target:** Verify a small channel example and construct a counterexample to an invalid stronger claim.

<span id="sec-entropy-relative-entropy-and-information-processing-6"></span>

### 11.6 Subadditivity and strong subadditivity [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-6).

**Section level:** advanced. **Required earlier sections:** [11.4](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-4), [11.5](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-5).

**Learning and derivation target:** State the inequalities precisely and connect their proof dependencies to relative-entropy monotonicity.

**Implementation and evidence target:** Check explicit tripartite examples and explain why a numerical survey is not a proof.

<span id="sec-entropy-relative-entropy-and-information-processing-7"></span>

### 11.7 Entropic reasoning in protocols

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-7).

**Section level:** core. **Required earlier sections:** [11.4](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-4), [11.5](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-5).

**Learning and derivation target:** Use the established inequalities to analyze information flow in a small protocol.

**Implementation and evidence target:** Track relevant subsystems and diagnose an invalid entropy manipulation.

<span id="sec-entropy-relative-entropy-and-information-processing-8"></span>

### 11.8 Information-inequality laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-8).

**Section level:** core. **Required earlier sections:** [11.2](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-2), [11.3](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-3), [11.6](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-6).

**Learning and derivation target:** Specify stable spectral calculations, boundary cases and proof versus evidence.

**Implementation and evidence target:** Compare analytic examples with independently computed spectra and support-aware implementations.

<span id="ch-compression-entanglement-and-communication-limits"></span>

## Chapter 12

**Compression, Entanglement, and Communication Limits**

**Reading level:** Advanced. **Entry guidance:** 7–8, 11; individual communication/entanglement branches use selected sections.

<span id="sec-compression-entanglement-and-communication-limits-1"></span>

### 12.1 Operational tasks and asymptotic statements

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-compression-entanglement-and-communication-limits-1).

**Section level:** advanced. **Required earlier sections:** [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8), [11.1](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-1).

**Learning and derivation target:** Distinguish block length, error tolerance and achievable rate.

**Implementation and evidence target:** Write a precise compression/communication task before constructing code.

<span id="sec-compression-entanglement-and-communication-limits-2"></span>

### 12.2 Typical sequences and subspaces

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-compression-entanglement-and-communication-limits-2).

**Section level:** advanced. **Required earlier sections:** [12.1](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-1), [11.1](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-1), [11.2](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-2).

**Learning and derivation target:** Derive a finite-alphabet typicality argument and its quantum spectral analogue.

**Implementation and evidence target:** Enumerate short blocks and compare retained probability with entropy-based expectations.

<span id="sec-compression-entanglement-and-communication-limits-3"></span>

### 12.3 Schumacher compression

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-compression-entanglement-and-communication-limits-3).

**Section level:** advanced. **Required earlier sections:** [12.2](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-2), [8.2](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2), [10.3](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-3).

**Learning and derivation target:** State the coding theorem, derive an illustrative construction and map the converse argument.

**Implementation and evidence target:** Build a small typical-subspace encoder and evaluate recovery fidelity.

<span id="sec-compression-entanglement-and-communication-limits-4"></span>

### 12.4 Entanglement concentration and dilution

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-compression-entanglement-and-communication-limits-4).

**Section level:** advanced. **Required earlier sections:** [7.2](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-2), [11.2](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-2), [12.2](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-2).

**Learning and derivation target:** Explain asymptotic resource conversion and derive a small concentration example.

**Implementation and evidence target:** Calculate branch probabilities and retained entanglement explicitly.

<span id="sec-mixed-entanglement-resources"></span>

### 12.5 Mixed-state entanglement, LOCC, and distillation [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-mixed-entanglement-resources).

**Section level:** advanced. **Required earlier sections:** [8.2](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2), [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3), [10.2](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-2), [11.4](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-4).

**Learning and derivation target:** Define separability and LOCC; derive a tractable witness/PPT example, state its dimensional limits and connect entanglement conversion to operational resources.

**Implementation and evidence target:** Compare known separable/entangled mixed states and a tiny purification/distillation example; do not generalize a sufficient test into a universal criterion.

<span id="sec-compression-entanglement-and-communication-limits-5"></span>
<span id="125-accessible-information-and-the-holevo-bound"></span>

### 12.6 Accessible information and the Holevo bound

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-compression-entanglement-and-communication-limits-5).

**Section level:** advanced. **Required earlier sections:** [11.3](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-3), [11.5](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-5), [12.1](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-1).

**Learning and derivation target:** Define an ensemble communication task and derive the scope of the bound.

**Implementation and evidence target:** Compare candidate measurements with the ensemble's Holevo quantity.

<span id="sec-compression-entanglement-and-communication-limits-6"></span>
<span id="126-classical-and-quantum-channel-capacities"></span>

### 12.7 Classical and quantum channel capacities

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-compression-entanglement-and-communication-limits-6).

**Section level:** advanced. **Required earlier sections:** [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3), [11.4](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-4), [12.1](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-1), [12.6](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-5).

**Learning and derivation target:** Specify operational definitions, coding/assistance assumptions and the role of regularization.

**Implementation and evidence target:** Evaluate elementary channels without assuming a universal single-letter capacity formula.

<span id="sec-compression-entanglement-and-communication-limits-7"></span>
<span id="127-finite-block-limitations-and-resource-accounting"></span>

### 12.8 Finite-block limitations and resource accounting

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-compression-entanglement-and-communication-limits-7).

**Section level:** advanced. **Required earlier sections:** [12.2](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-2), [12.3](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-3), [12.7](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-6).

**Learning and derivation target:** Explain the gap between theorem limits and short experiments.

**Implementation and evidence target:** Report block length, fidelity, success probability and communication/entanglement costs.

<span id="sec-compression-entanglement-and-communication-limits-8"></span>
<span id="128-compression-and-communication-laboratory"></span>

### 12.9 Compression and communication laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-compression-entanglement-and-communication-limits-8).

**Section level:** advanced. **Required earlier sections:** [12.3](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-3), [12.4](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-4), [12.8](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-7).

**Learning and derivation target:** Connect one explicit code to its mathematical claim and asymptotic context.

**Implementation and evidence target:** Compare independent encoders/decoders and document why finite tests cannot prove a coding theorem.

<span id="ch-quantum-cryptography-and-security-reasoning"></span>

## Chapter 13

**Quantum Cryptography and Security Reasoning**

**Reading level:** Advanced. **Entry guidance:** 6, 8 for the entry; 10–11 for advanced proof branches, not all of 12.

<span id="sec-quantum-cryptography-and-security-reasoning-1"></span>

### 13.1 Security tasks and adversarial models

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-1).

**Section level:** advanced. **Required earlier sections:** [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Learning and derivation target:** Define correctness, secrecy, authentication and the adversary's capabilities.

**Implementation and evidence target:** Write a protocol-specific threat model and identify missing assumptions.

<span id="sec-quantum-cryptography-and-security-reasoning-2"></span>

### 13.2 BB84 preparation, measurement, and sifting

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-2).

**Section level:** advanced. **Required earlier sections:** [3.2](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-2), [6.4](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-4), [13.1](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-1).

**Learning and derivation target:** Derive ideal correlations and an intercept-resend disturbance example.

**Implementation and evidence target:** Check basis choices, sifted records and expected error statistics.

<span id="sec-quantum-cryptography-and-security-reasoning-3"></span>

### 13.3 Parameter estimation and finite samples

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-3).

**Section level:** advanced. **Required earlier sections:** [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8), [13.2](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-2).

**Learning and derivation target:** Derive a stated bound relating observed data to a security-relevant quantity.

**Implementation and evidence target:** Evaluate coverage and abort rates across independent synthetic transcripts.

<span id="sec-quantum-cryptography-and-security-reasoning-4"></span>

### 13.4 Error reconciliation and information leakage

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-4).

**Section level:** advanced. **Required earlier sections:** [11.1](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-1), [13.2](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-2).

**Learning and derivation target:** Explain reconciliation correctness and the public information it reveals.

**Implementation and evidence target:** Track leakage and residual disagreements in a tiny example.

<span id="sec-quantum-cryptography-and-security-reasoning-5"></span>

### 13.5 Privacy amplification

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-5).

**Section level:** advanced. **Required earlier sections:** [11.3](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-3), [13.3](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-3), [13.4](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-4).

**Learning and derivation target:** State a scoped extraction guarantee, its entropy assumptions and the hash-family requirements.

**Implementation and evidence target:** Illustrate hashing on toy data without treating it as a secure production implementation.

<span id="sec-quantum-cryptography-and-security-reasoning-6"></span>

### 13.6 Composable security and proof structure [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-6).

**Section level:** advanced. **Required earlier sections:** [10.2](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-2), [13.1](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-1), [13.3](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-3), [13.5](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-5).

**Learning and derivation target:** Define a distinguishing-based security target and map a selected proof's assumptions.

**Implementation and evidence target:** Identify which protocol steps are covered by the theorem and which implementation assumptions remain.

<span id="sec-quantum-cryptography-and-security-reasoning-7"></span>

### 13.7 Attacks, side channels, and failure diagnosis

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-7).

**Section level:** advanced. **Required earlier sections:** [13.1](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-1), [13.2](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-2).

**Learning and derivation target:** Explain how an ideal model can fail to cover an implementation.

**Implementation and evidence target:** Analyze a specified attack or missing-authentication counterexample.

<span id="sec-crypto-impossibility-boundaries"></span>

### 13.8 Cryptographic tasks and impossibility boundaries [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-crypto-impossibility-boundaries).

**Section level:** advanced. **Required earlier sections:** [8.6](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-6), [13.1](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-1).

**Learning and derivation target:** Define a bit-commitment task and map a selected no-go argument using purification, with explicit assumptions; distinguish unconditional impossibility from additional-assumption protocols.

**Implementation and evidence target:** Analyze a tractable cheating example and document the exact theorem/proof obligations rather than inferring security from simulation.

<span id="sec-quantum-cryptography-and-security-reasoning-8"></span>
<span id="138-a-security-claim-audit"></span>

### 13.9 A security-claim audit

**Result/proof/source specification:** [Scholarly plan](../proof-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-8).

**Section level:** advanced. **Required earlier sections:** [13.3](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-3), [13.5](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-5), [13.6](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-6), [13.7](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-7).

**Learning and derivation target:** Separate a pedagogical protocol simulation from a complete security proof.

**Implementation and evidence target:** Produce a protocol record with source theorem, finite-size terms and explicit unverified claims.
