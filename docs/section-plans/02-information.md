# Part 2. Quantum Information: Channels, Inference, and Communication

**Detailed plan · 2026-10-20 · Planned material; architecture review pending.** [All sections](../section-plan.md) · [Full plan](../book-plan.md) · [Reader continuity](../reader-continuity.md)

Each section specifies its argument and independent evidence. Framework implementation, mathematical review and reader review have separate status. Closing materials follow the [section-plan guide](../section-plan.md#how-to-read-the-specification).

<span id="ch-quantum-channels-and-their-representations"></span>

## Chapter 9

**Quantum Channels and Their Representations**

**Reading level:** Core. **Chapter prerequisites:** 8.

<span id="sec-quantum-channels-and-their-representations-1"></span>

### 9.1 From closed evolution to quantum channels

**Learning and derivation target:** Derive a reduced-system map from an initially specified environment state.

**Implementation and evidence target:** Compare joint unitary evolution and reduced output.

<span id="sec-quantum-channels-and-their-representations-2"></span>

### 9.2 Linearity, positivity, and complete positivity

**Learning and derivation target:** Define each condition and explain the extension by an untouched ancilla.

**Implementation and evidence target:** Use transposition as a counterexample to positivity being sufficient.

<span id="sec-quantum-channels-and-their-representations-3"></span>

### 9.3 Kraus operators and trace preservation

**Learning and derivation target:** Derive the operator-sum form and completeness condition.

**Implementation and evidence target:** Verify a simple channel on a spanning set of inputs.

<span id="sec-quantum-channels-and-their-representations-4"></span>

### 9.4 Stinespring dilation

**Learning and derivation target:** Construct a finite-dimensional dilation and explain environmental freedom.

**Implementation and evidence target:** Recover the channel by explicit partial trace.

<span id="sec-quantum-channels-and-their-representations-5"></span>

### 9.5 Choi representation and vectorization

**Learning and derivation target:** Fix a vectorization convention and derive the channel-to-Choi correspondence.

**Implementation and evidence target:** Check reshuffling indices against explicit basis operators.

<span id="sec-quantum-channels-and-their-representations-6"></span>

### 9.6 Representation equivalence and Kraus nonuniqueness

**Learning and derivation target:** Connect Choi spectral factors, Kraus operators and an environmental isometry.

**Implementation and evidence target:** Convert a small channel between representations and check identical actions.

<span id="sec-quantum-channels-and-their-representations-7"></span>

### 9.7 Composition, tensor products, and instruments

**Learning and derivation target:** Derive channel composition and trace-nonincreasing branches.

**Implementation and evidence target:** Compare sequential, composite and conditional calculations.

<span id="sec-quantum-channels-and-their-representations-8"></span>

### 9.8 Channel-validation laboratory

**Learning and derivation target:** State physicality and equivalence tests and their finite numerical limits.

**Implementation and evidence target:** Check Choi positivity and partial traces; diagnose a trace-preserving but non-CP map.

<span id="ch-distinguishability-fidelity-and-quantum-state-inference"></span>

## Chapter 10

**Distinguishability, Fidelity, and Quantum State Inference**

**Reading level:** Core. **Chapter prerequisites:** 6, 8, 9.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-1"></span>

### 10.1 Classical distinguishability as a starting point

**Learning and derivation target:** Define total-variation distance and its discrimination interpretation.

**Implementation and evidence target:** Compare two finite distributions and an explicit decision rule.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-2"></span>

### 10.2 Quantum trace distance and binary discrimination

**Learning and derivation target:** Derive the optimal two-state measurement for stated priors.

**Implementation and evidence target:** Compare a spectral construction with independently enumerated candidate measurements.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-3"></span>

### 10.3 Fidelity and state-comparison conventions

**Learning and derivation target:** Declare squared versus unsquared fidelity and derive pure/commuting cases.

**Implementation and evidence target:** Verify analytic limiting cases and contrast fidelity with elementwise equality.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-4"></span>

### 10.4 Monotonicity and operational limits

**Learning and derivation target:** Explain how channels and restricted measurements affect distinguishability.

**Implementation and evidence target:** Construct a strict information-loss example and an incomplete-measurement counterexample.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-5"></span>

### 10.5 Quantum state tomography

**Learning and derivation target:** Derive linear inversion for a qubit and explain positivity and finite-sample difficulties.

**Implementation and evidence target:** Reconstruct small states and compare physical versus unconstrained estimates.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-6"></span>

### 10.6 Pauli sums, grouping, and measurement allocation

**Learning and derivation target:** Derive variance/covariance expressions for an estimated weighted observable.

**Implementation and evidence target:** Compare allocation rules under an identical total-shot budget.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-7"></span>

### 10.7 Classical shadows [Advanced]

**Learning and derivation target:** Define the measurement ensemble, inverse measurement map and property-estimation task.

**Implementation and evidence target:** Check a small Pauli-shadow estimator and report ensemble-dependent uncertainty.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-8"></span>

### 10.8 Inference laboratory and validation limits

**Learning and derivation target:** Separate state reconstruction, property prediction and certification claims.

**Implementation and evidence target:** Report estimation error across repeated trials and identify unmeasured degrees of freedom.

<span id="ch-entropy-relative-entropy-and-information-processing"></span>

## Chapter 11

**Entropy, Relative Entropy, and Information Processing**

**Reading level:** Core with advanced proofs. **Chapter prerequisites:** 8–10.

<span id="sec-entropy-relative-entropy-and-information-processing-1"></span>

### 11.1 Classical entropy and uncertainty

**Learning and derivation target:** Define Shannon entropy and derive basic finite-distribution properties.

**Implementation and evidence target:** Compare deterministic, uniform and correlated examples.

<span id="sec-entropy-relative-entropy-and-information-processing-2"></span>

### 11.2 Von Neumann entropy and spectra

**Learning and derivation target:** Derive the spectral formula and unitary invariance.

**Implementation and evidence target:** Compute mixed-state examples and verify pure-state limits.

<span id="sec-entropy-relative-entropy-and-information-processing-3"></span>

### 11.3 Relative entropy and support conditions

**Learning and derivation target:** State classical and quantum definitions with support and infinity conventions.

**Implementation and evidence target:** Test commuting reductions, singular states and numerically unstable cases.

<span id="sec-entropy-relative-entropy-and-information-processing-4"></span>

### 11.4 Mutual and conditional information

**Learning and derivation target:** Derive the entropy identities and interpret classical and entangled examples.

**Implementation and evidence target:** Compare classical correlations with negative quantum conditional entropy.

<span id="sec-entropy-relative-entropy-and-information-processing-5"></span>

### 11.5 Data processing

**Learning and derivation target:** State operational assumptions, prove a tractable case and map the general proof requirements.

**Implementation and evidence target:** Verify a small channel example and construct a counterexample to an invalid stronger claim.

<span id="sec-entropy-relative-entropy-and-information-processing-6"></span>

### 11.6 Subadditivity and strong subadditivity [Advanced]

**Learning and derivation target:** State the inequalities precisely and connect their proof dependencies to relative-entropy monotonicity.

**Implementation and evidence target:** Check explicit tripartite examples and explain why a numerical survey is not a proof.

<span id="sec-entropy-relative-entropy-and-information-processing-7"></span>

### 11.7 Entropic reasoning in protocols

**Learning and derivation target:** Use the established inequalities to analyze information flow in a small protocol.

**Implementation and evidence target:** Track relevant subsystems and diagnose an invalid entropy manipulation.

<span id="sec-entropy-relative-entropy-and-information-processing-8"></span>

### 11.8 Information-inequality laboratory

**Learning and derivation target:** Specify stable spectral calculations, boundary cases and proof versus evidence.

**Implementation and evidence target:** Compare analytic examples with independently computed spectra and support-aware implementations.

<span id="ch-compression-entanglement-and-communication-limits"></span>

## Chapter 12

**Compression, Entanglement, and Communication Limits**

**Reading level:** Advanced. **Chapter prerequisites:** 7–11.

<span id="sec-compression-entanglement-and-communication-limits-1"></span>

### 12.1 Operational tasks and asymptotic statements

**Learning and derivation target:** Distinguish block length, error tolerance and achievable rate.

**Implementation and evidence target:** Write a precise compression/communication task before constructing code.

<span id="sec-compression-entanglement-and-communication-limits-2"></span>

### 12.2 Typical sequences and subspaces

**Learning and derivation target:** Derive a finite-alphabet typicality argument and its quantum spectral analogue.

**Implementation and evidence target:** Enumerate short blocks and compare retained probability with entropy-based expectations.

<span id="sec-compression-entanglement-and-communication-limits-3"></span>

### 12.3 Schumacher compression

**Learning and derivation target:** State the coding theorem, derive an illustrative construction and map the converse argument.

**Implementation and evidence target:** Build a small typical-subspace encoder and evaluate recovery fidelity.

<span id="sec-compression-entanglement-and-communication-limits-4"></span>

### 12.4 Entanglement concentration and dilution

**Learning and derivation target:** Explain asymptotic resource conversion and derive a small concentration example.

**Implementation and evidence target:** Calculate branch probabilities and retained entanglement explicitly.

<span id="sec-compression-entanglement-and-communication-limits-5"></span>

### 12.5 Accessible information and the Holevo bound

**Learning and derivation target:** Define an ensemble communication task and derive the scope of the bound.

**Implementation and evidence target:** Compare candidate measurements with the ensemble's Holevo quantity.

<span id="sec-compression-entanglement-and-communication-limits-6"></span>

### 12.6 Classical and quantum channel capacities

**Learning and derivation target:** Specify operational definitions, coding/assistance assumptions and the role of regularization.

**Implementation and evidence target:** Evaluate elementary channels without assuming a universal single-letter capacity formula.

<span id="sec-compression-entanglement-and-communication-limits-7"></span>

### 12.7 Finite-block limitations and resource accounting

**Learning and derivation target:** Explain the gap between theorem limits and short experiments.

**Implementation and evidence target:** Report block length, fidelity, success probability and communication/entanglement costs.

<span id="sec-compression-entanglement-and-communication-limits-8"></span>

### 12.8 Compression and communication laboratory

**Learning and derivation target:** Connect one explicit code to its mathematical claim and asymptotic context.

**Implementation and evidence target:** Compare independent encoders/decoders and document why finite tests cannot prove a coding theorem.

<span id="ch-quantum-cryptography-and-security-reasoning"></span>

## Chapter 13

**Quantum Cryptography and Security Reasoning**

**Reading level:** Advanced. **Chapter prerequisites:** 6–12.

<span id="sec-quantum-cryptography-and-security-reasoning-1"></span>

### 13.1 Security tasks and adversarial models

**Learning and derivation target:** Define correctness, secrecy, authentication and the adversary's capabilities.

**Implementation and evidence target:** Write a protocol-specific threat model and identify missing assumptions.

<span id="sec-quantum-cryptography-and-security-reasoning-2"></span>

### 13.2 BB84 preparation, measurement, and sifting

**Learning and derivation target:** Derive ideal correlations and an intercept-resend disturbance example.

**Implementation and evidence target:** Check basis choices, sifted records and expected error statistics.

<span id="sec-quantum-cryptography-and-security-reasoning-3"></span>

### 13.3 Parameter estimation and finite samples

**Learning and derivation target:** Derive a stated bound relating observed data to a security-relevant quantity.

**Implementation and evidence target:** Evaluate coverage and abort rates across independent synthetic transcripts.

<span id="sec-quantum-cryptography-and-security-reasoning-4"></span>

### 13.4 Error reconciliation and information leakage

**Learning and derivation target:** Explain reconciliation correctness and the public information it reveals.

**Implementation and evidence target:** Track leakage and residual disagreements in a tiny example.

<span id="sec-quantum-cryptography-and-security-reasoning-5"></span>

### 13.5 Privacy amplification

**Learning and derivation target:** State a scoped extraction guarantee, its entropy assumptions and the hash-family requirements.

**Implementation and evidence target:** Illustrate hashing on toy data without treating it as a secure production implementation.

<span id="sec-quantum-cryptography-and-security-reasoning-6"></span>

### 13.6 Composable security and proof structure [Advanced]

**Learning and derivation target:** Define a distinguishing-based security target and map a selected proof's assumptions.

**Implementation and evidence target:** Identify which protocol steps are covered by the theorem and which implementation assumptions remain.

<span id="sec-quantum-cryptography-and-security-reasoning-7"></span>

### 13.7 Attacks, side channels, and failure diagnosis

**Learning and derivation target:** Explain how an ideal model can fail to cover an implementation.

**Implementation and evidence target:** Analyze a specified attack or missing-authentication counterexample.

<span id="sec-quantum-cryptography-and-security-reasoning-8"></span>

### 13.8 A security-claim audit

**Learning and derivation target:** Separate a pedagogical protocol simulation from a complete security proof.

**Implementation and evidence target:** Produce a protocol record with source theorem, finite-size terms and explicit unverified claims.
