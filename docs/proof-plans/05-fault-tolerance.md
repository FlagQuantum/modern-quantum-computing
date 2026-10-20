# Result and proof plan: Noise, Error Correction, and Fault-Tolerant Computation

[Depth definitions](../proof-plan.md#proof-depth-contract) · [Source catalogue](../references/proof-sources.md) · [Volume plan](../volume-plan.md)

Authoring specifications only. No result/proof/API is certified by this plan. F/M/R have different scope; imported results are the exact prerequisite sections linked below.

## Chapter 28: Noise, Open Systems, and Error Mitigation

<span id="sec-noise-open-systems-and-error-mitigation-1"></span>

### 28.1 Noise models and system-environment assumptions

**Core result / role:** Channel model requires a system-environment assumption.

**Assumptions and scope:** Initial correlation, memory and stationarity explicitly declared.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** State model scope; use a correlated preparation counterexample to delimit reduced maps.

**Imported earlier results:** [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3).

**Exact source targets:** [NC:8.5](../references/proof-sources.md#source-nc-8-5): Section 8.5 Limitations of the quantum operations formalism.

**Independent evidence target:** Compare a named channel model with its explicit environment construction.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-noise-open-systems-and-error-mitigation-2"></span>

### 28.2 Discrete channels: dephasing and depolarization

**Core result / role:** Dephasing/depolarizing channel action.

**Assumptions and scope:** Declared parameter normalization and complete-positivity range.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive Kraus/Bloch action and verify trace preservation.

**Imported earlier results:** [28.1](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-1), [3.3](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-3).

**Exact source targets:** [NC:8.3.3](../references/proof-sources.md#source-nc-8-3-3): Section 8.3.3 Bit ﬂip and phase ﬂip channels; [NC:8.3.4](../references/proof-sources.md#source-nc-8-3-4): Section 8.3.4 Depolarizing channel.

**Independent evidence target:** Verify limiting cases, fixed points, trace and positivity.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-noise-open-systems-and-error-mitigation-3"></span>

### 28.3 Amplitude damping and relaxation

**Core result / role:** Amplitude-damping channel and relaxation parameter.

**Assumptions and scope:** Two-level relaxation model and stated time-rate relation.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive Kraus action and population/coherence evolution.

**Imported earlier results:** [28.1](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-1), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3).

**Exact source targets:** [NC:8.3.5](../references/proof-sources.md#source-nc-8-3-5): Section 8.3.5 Amplitude damping.

**Independent evidence target:** Compare density evolution with an independent matrix calculation.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-noise-open-systems-and-error-mitigation-4"></span>

### 28.4 Lindblad dynamics

**Core result / role:** Lindblad evolution for a selected finite model.

**Assumptions and scope:** Born/Markov/secular assumptions stated; fixed nonnegative rates.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive a selected generator and solve a simple model; defer general generator characterization.

**Imported earlier results:** [28.1](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-1), [2.6](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-6).

**Exact source targets:** [NC:8.4.1](../references/proof-sources.md#source-nc-8-4-1): Section 8.4.1 Master equations.

**Independent evidence target:** Compare analytic evolution and an independent ODE/exponential reference.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-noise-open-systems-and-error-mitigation-5"></span>

### 28.5 Quantum trajectories and unravelings

**Core result / role:** Trajectory averaging reproduces the master equation.

**Assumptions and scope:** Selected jump unraveling and timestep limit.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Expand no-jump/jump branches and average unnormalized density updates to first order.

**Imported earlier results:** [28.4](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-4), [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6), [9.7](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-7).

**Exact source targets:** [TRAJ:unraveling](../references/proof-sources.md#source-traj-unraveling): Sections 0.3.3 and 0.4.1-0.4.4: master equation, conditional dynamics and quantum jumps.

**Independent evidence target:** Compare trajectory averages with deterministic density evolution and uncertainty.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-noise-open-systems-and-error-mitigation-6"></span>

### 28.6 Correlated and non-Markovian limitations [Advanced]

**Core result / role:** Memory and correlations invalidate independent error models.

**Assumptions and scope:** Explicit finite environment or correlated channel.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive a counterexample to a memoryless/completely divisible description.

**Imported earlier results:** [28.1](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-1), [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4).

**Exact source targets:** [NC:8.5](../references/proof-sources.md#source-nc-8-5): Section 8.5 Limitations of the quantum operations formalism; [TRAJ:unraveling](../references/proof-sources.md#source-traj-unraveling): Sections 0.3.3 and 0.4.1-0.4.4: master equation, conditional dynamics and quantum jumps.

**Independent evidence target:** Show which correlations the simple channel model cannot reproduce.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-noise-open-systems-and-error-mitigation-7"></span>

### 28.7 Error mitigation: bias, variance, and cost

**Core result / role:** Selected mitigation estimator: bias-variance-cost tradeoff.

**Assumptions and scope:** Specified scalable noise parameter or known quasiprobability model.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive two-point Richardson zero-noise extrapolation, leading bias and independent-shot variance; delimit the scalable-noise assumption and model mismatch.

**Imported earlier results:** [28.2](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-2), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Exact source targets:** [NOISE:mitigation](../references/proof-sources.md#source-noise-mitigation): Section V A extrapolation and V C quasi-probability methods.

**Independent evidence target:** Compare bias, variance and execution overhead under controlled model mismatch.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-noise-open-systems-and-error-mitigation-8"></span>

### 28.8 Calibration, drift, and model validation

**Core result / role:** Calibration transfer is an identifiability/drift claim.

**Assumptions and scope:** Specified fitted noise parameters, data and time dependence.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive a small parameter fit and show non-identifiability or drift failure.

**Imported earlier results:** [28.1](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-1), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Exact source targets:** [SC:III.B](../references/proof-sources.md#source-sc-iii-b): Section III B Modeling noise and decoherence; [NC:8.4.2](../references/proof-sources.md#source-nc-8-4-2): Section 8.4.2 Quantum process tomography.

**Independent evidence target:** Compare held-out synthetic/available data with a fitted model and record provenance.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-device-characterization-benchmarking"></span>

### 28.9 SPAM, gate characterization, and randomized benchmarking [Advanced]

**Core result / role:** Randomized-benchmarking decay under a stated model.

**Assumptions and scope:** Specified gate ensemble, twirl, stationary/gate-dependence assumptions.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Derive the idealized twirled decay; state which robust/generalized results are not proved.

**Imported earlier results:** [9.5](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-5), [10.5](../section-plans/02-information.md#sec-channel-error-metrics), [10.6](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-5), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Exact source targets:** [RB:decay](../references/proof-sources.md#source-rb-decay): Twirled decay models and zeroth/first-order fit equations.

**Independent evidence target:** Fit synthetic records from a known model and a mismatched model; report uncertainty and avoid treating one decay parameter as every circuit’s failure probability.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local advanced bridge to supply:** Finite gate ensemble, twirling, design assumptions and noise stationarity.

**Explicitly deferred proof ingredients:** General gate-dependent perturbation corrections and robust fit guarantees; Magesan et al. pp.1–4, beyond the idealized decay derived locally.

<span id="sec-noise-open-systems-and-error-mitigation-9"></span>

### 28.10 Noise laboratory and evidence boundaries

**Core result / role:** Noise-model acceptance protocol.

**Assumptions and scope:** Declared ideal, stochastic and hardware evidence.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Verify channels, trajectories and calibration/characterization fit with assumption failures.

**Imported earlier results:** [28.2](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-2), [28.3](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-3), [28.4](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-4), [28.8](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-8), [28.9](../section-plans/05-fault-tolerance.md#sec-device-characterization-benchmarking).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Report all model assumptions and independent solver/statistical checks.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 29: Quantum Error Correction: Conditions and Recovery

<span id="sec-quantum-error-correction-conditions-and-recovery-1"></span>

### 29.1 The quantum error-correction problem

**Core result / role:** Quantum recovery must preserve unknown information.

**Assumptions and scope:** Specified code, noise and recovery task.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Define correctness on the full code space and distinguish it from restoring one basis state.

**Imported earlier results:** [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2).

**Exact source targets:** [NC:10.1](../references/proof-sources.md#source-nc-10-1): Section 10.1 Introduction.

**Independent evidence target:** Analyze failed correction proposals on an unknown superposition.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-error-correction-conditions-and-recovery-2"></span>

### 29.2 Encoding and logical information

**Core result / role:** Encoding isometry preserves logical inner products.

**Assumptions and scope:** Finite logical space and orthonormal code basis.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove isometry and derive the logical-state map.

**Imported earlier results:** [29.1](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-1), [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3).

**Exact source targets:** [NC:10.1.1](../references/proof-sources.md#source-nc-10-1-1): Section 10.1.1 The three qubit bit ﬂip code.

**Independent evidence target:** Verify preservation of arbitrary encoded amplitudes.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-error-correction-conditions-and-recovery-3"></span>

### 29.3 Repetition codes and syndrome extraction

**Core result / role:** Repetition-code syndrome and recovery correctness.

**Assumptions and scope:** At most one X error; ideal specified extraction circuit.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive all syndrome branches and show logical amplitudes survive.

**Imported earlier results:** [29.2](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-2), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2).

**Exact source targets:** [NC:10.1.1](../references/proof-sources.md#source-nc-10-1-1): Section 10.1.1 The three qubit bit ﬂip code.

**Independent evidence target:** Enumerate errors and compare conditional post-measurement states.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-error-correction-conditions-and-recovery-4"></span>

### 29.4 Error sets and coherent combinations

**Core result / role:** Correctable error span includes coherent combinations.

**Assumptions and scope:** A common recovery for a specified finite error span.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Expand channel/error amplitudes and derive the required cross-error condition.

**Imported earlier results:** [29.2](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-2), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3).

**Exact source targets:** [NC:10.3.1](../references/proof-sources.md#source-nc-10-3-1): Section 10.3.1 Discretization of the errors.

**Independent evidence target:** Test coherent combinations instead of only stochastic Pauli injections.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-error-correction-conditions-and-recovery-5"></span>

### 29.5 Knill-Laflamme conditions

**Core result / role:** Knill-Laflamme conditions.

**Assumptions and scope:** Finite code projector; completely positive noise with specified Kraus span.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove necessity and sufficiency, including diagonalizing the error Gram matrix and constructing recovery.

**Imported earlier results:** [29.4](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-4), [2.4](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-4).

**Exact source targets:** [NC:10.3](../references/proof-sources.md#source-nc-10-3): Section 10.3 Theory of quantum error-correction.

**Independent evidence target:** Verify the matrix conditions on an explicit small code.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-error-correction-conditions-and-recovery-6"></span>

### 29.6 Constructing a recovery operation

**Core result / role:** Recovery from orthogonal error subspaces.

**Assumptions and scope:** Knill-Laflamme condition and nonzero Gram eigenvalues.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Construct syndrome projectors/isometries and complete the recovery on unused space.

**Imported earlier results:** [29.5](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-5), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3).

**Exact source targets:** [NC:10.3](../references/proof-sources.md#source-nc-10-3): Section 10.3 Theory of quantum error-correction.

**Independent evidence target:** Compare recovered states with the encoded reference.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-error-correction-conditions-and-recovery-7"></span>

### 29.7 Degeneracy, distance, and limitations

**Core result / role:** Distance, degeneracy and selected code bounds.

**Assumptions and scope:** Pauli-error model and declared degeneracy assumptions.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive distance correction/detection conditions; prove only a selected bound with its nondegeneracy conditions.

**Imported earlier results:** [29.5](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-5), [29.6](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-6).

**Exact source targets:** [NC:10.3.3](../references/proof-sources.md#source-nc-10-3-3): Section 10.3.3 Degenerate codes; [NC:10.3.4](../references/proof-sources.md#source-nc-10-3-4): Section 10.3.4 The quantum Hamming bound.

**Independent evidence target:** Construct correctable and failing error patterns.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-error-correction-conditions-and-recovery-8"></span>

### 29.8 Beyond bit-flip protection

**Core result / role:** Concatenated repetition protects bit and phase errors.

**Assumptions and scope:** Nine-qubit Shor construction and single-qubit error span.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive inner/outer corrections and prove the required error-span condition without assuming CSS theory.

**Imported earlier results:** [29.3](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-3), [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5).

**Exact source targets:** [NC:10.2](../references/proof-sources.md#source-nc-10-2): Section 10.2 The Shor code.

**Independent evidence target:** Verify nontrivial superpositions under independent error types.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-error-correction-conditions-and-recovery-9"></span>

### 29.9 Recovery laboratory and logical-state verification

**Core result / role:** Recovery acceptance protocol.

**Assumptions and scope:** Unknown logical superpositions and entangled reference checks.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Test the channel on the code space rather than only logical basis states.

**Imported earlier results:** [29.5](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-5), [29.6](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-6), [29.8](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-8).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Check a spanning operator basis or an equivalent complete small-code reference; quantify failures.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 30: Stabilizer Codes, Logical Operators, and Decoding

<span id="sec-stabilizer-codes-logical-operators-and-decoding-1"></span>

### 30.1 Pauli groups and binary symplectic algebra

**Core result / role:** Pauli commutation equals a binary symplectic product.

**Assumptions and scope:** Declared phase convention and binary label ordering.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive multiplication/commutation and introduce the needed binary linear algebra locally.

**Imported earlier results:** [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5), [4.3](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-3).

**Exact source targets:** [NC:10.5.1](../references/proof-sources.md#source-nc-10-5-1): Section 10.5.1 The stabilizer formalism; [P7:7.10.2](../references/proof-sources.md#source-p7-7-10-2): Section 7.10.2 Symplectic Notation.

**Independent evidence target:** Compare binary operations with dense Pauli products.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-stabilizer-codes-logical-operators-and-decoding-2"></span>

### 30.2 Stabilizer groups and code spaces

**Core result / role:** Stabilizer projector and code dimension.

**Assumptions and scope:** Independent commuting Pauli generators; no negative identity.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Construct the group-average projector and prove rank equal to the encoded dimension.

**Imported earlier results:** [30.1](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-1).

**Exact source targets:** [NC:10.5.1](../references/proof-sources.md#source-nc-10-5-1): Section 10.5.1 The stabilizer formalism.

**Independent evidence target:** Compare stabilizer projectors with explicit code-state bases.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-stabilizer-codes-logical-operators-and-decoding-3"></span>

### 30.3 Syndromes as commutation data

**Core result / role:** Syndromes encode error commutation classes.

**Assumptions and scope:** Specified stabilizer generators and Pauli errors.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive each syndrome bit; show why equal syndromes can represent distinct logical classes.

**Imported earlier results:** [30.2](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-2), [29.3](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-3).

**Exact source targets:** [NC:10.5.1](../references/proof-sources.md#source-nc-10-5-1): Section 10.5.1 The stabilizer formalism.

**Independent evidence target:** Check every single-qubit error on a small code.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-stabilizer-codes-logical-operators-and-decoding-4"></span>

### 30.4 CSS codes from classical checks

**Core result / role:** CSS orthogonality yields commuting quantum checks.

**Assumptions and scope:** Binary classical check matrices satisfying the stated orthogonality condition.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove X/Z check commutation and count independent checks.

**Imported earlier results:** [30.1](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-1), [30.2](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-2).

**Exact source targets:** [NC:10.4.1](../references/proof-sources.md#source-nc-10-4-1): Section 10.4.1 Classical linear codes; [NC:10.4.2](../references/proof-sources.md#source-nc-10-4-2): Section 10.4.2 Calderbank–Shor–Steane codes.

**Independent evidence target:** Build and verify a selected tiny CSS code.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-stabilizer-codes-logical-operators-and-decoding-5"></span>

### 30.5 Logical operators and code distance

**Core result / role:** Logical Paulis form a normalizer quotient.

**Assumptions and scope:** Fixed stabilizer group; phases treated consistently.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Construct quotient representatives and derive minimum logical Pauli weight as distance.

**Imported earlier results:** [30.2](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-2), [30.3](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-3), [29.7](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-7).

**Exact source targets:** [NC:10.5.5](../references/proof-sources.md#source-nc-10-5-5): Section 10.5.5 Stabilizer code constructions.

**Independent evidence target:** Enumerate low-weight operators and verify distance for the tiny code.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-stabilizer-codes-logical-operators-and-decoding-6"></span>

### 30.6 Degeneracy and decoding choices

**Core result / role:** Degenerate maximum-likelihood decoding.

**Assumptions and scope:** Specified error distribution and equivalence classes.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Sum class probabilities; exhibit a most-likely-error versus most-likely-class difference.

**Imported earlier results:** [30.3](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-3), [30.5](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-5).

**Exact source targets:** [NC:10.3.3](../references/proof-sources.md#source-nc-10-3-3): Section 10.3.3 Degenerate codes.

**Independent evidence target:** Compare decoders using logical equivalence rather than exact error identity.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-stabilizer-codes-logical-operators-and-decoding-7"></span>

### 30.7 Syndrome circuits and fault propagation

**Core result / role:** Syndrome-extraction fault propagation.

**Assumptions and scope:** Explicit check circuit and insertion locations.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Conjugate Pauli faults gate by gate and identify correlated data/record errors.

**Imported earlier results:** [30.3](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-3), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Exact source targets:** [NC:10.5.8](../references/proof-sources.md#source-nc-10-5-8): Section 10.5.8 Quantum circuits for encoding, decoding, and correction.

**Independent evidence target:** Compare ideal syndrome outcomes and enumerated circuit faults.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-stabilizer-codes-logical-operators-and-decoding-8"></span>

### 30.8 Decoder interfaces and evidence records

**Core result / role:** Decoder contract and independent validation.

**Assumptions and scope:** Detection record, boundary convention and logical frame.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Specify inputs/outputs and test class correctness using exact tiny errors.

**Imported earlier results:** [30.5](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-5), [30.6](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-6).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Check an interchangeable decoder against exact hand-enumerated cases.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-ldpc-architecture"></span>

### 30.9 Quantum LDPC families and architectural tradeoffs [Advanced]

**Core result / role:** Quantum-LDPC check structure and connectivity tradeoffs.

**Assumptions and scope:** Selected finite construction and declared locality/rate/noise model.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Verify sparse commuting checks for one instance; roadmap distance/scaling claims and avoid universal hardware superiority.

**Imported earlier results:** [30.4](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-4), [30.5](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-5), [30.7](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-7).

**Exact source targets:** [LDPC:construction](../references/proof-sources.md#source-ldpc-construction): Section 4 Quasi-cyclic quantum LDPC codes; construction and check matrices.

**Independent evidence target:** Verify a tiny check matrix, commutation and logical operators; compare cost assumptions with a small surface-code model under matched declared noise/decoder conditions.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local advanced bridge to supply:** Sparse check matrices, Tanner graph, rate, distance and physical connectivity.

**Explicitly deferred proof ingredients:** General/asymptotic distance claims and architecture-scale decoding/performance arguments; Bravyi et al. Section 4 and Lemmas 1–4.

<span id="sec-stabilizer-graph-state-mbqc"></span>

### 30.10 Graph states and measurement-based computation

**Core result / role:** Graph-state stabilizers and measurement-induced gates.

**Assumptions and scope:** Declared graph state, measurement bases and classical corrections.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive stabilizers and one adaptive teleportation gate; track byproduct corrections in every branch.

**Imported earlier results:** [30.1](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-1), [30.2](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-2), [7.5](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-5).

**Exact source targets:** [MBQC:pattern](../references/proof-sources.md#source-mbqc-pattern): Computation by adaptive one-qubit measurements and byproduct operators.

**Independent evidence target:** Check every branch and the corrected logical action; provide the theoretical bridge to photonic resource-state computation.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-stabilizer-codes-logical-operators-and-decoding-9"></span>

### 30.11 Stabilizer-code laboratory

**Core result / role:** Stabilizer-code acceptance protocol.

**Assumptions and scope:** Independent Pauli algebra and logical-state checks.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Verify generator independence, syndrome classes, decoder conventions and fault propagation.

**Imported earlier results:** [30.3](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-3), [30.4](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-4), [30.5](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-5), [30.7](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-7), [30.8](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-8).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Compare independent binary and dense calculations before large experiments.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 31: Surface Codes and Repeated Syndrome Measurements

<span id="sec-surface-codes-and-repeated-syndrome-measurements-1"></span>

### 31.1 From stabilizer checks to a surface-code lattice

**Core result / role:** Surface-code checks commute on the lattice.

**Assumptions and scope:** Specified boundaries, data/check locations and cell incidence.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove overlap parity and identify independent checks.

**Imported earlier results:** [30.4](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-4), [30.5](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-5).

**Exact source targets:** [P7:7.18.1](../references/proof-sources.md#source-p7-7-18-1): Section 7.18.1 Code stabilizer and logical operators; [SURFACE:lattice](../references/proof-sources.md#source-surface-lattice): Sections III-IV, Fig. 1 and stabilizer description.

**Independent evidence target:** Compare the lattice description with an independently built commutation matrix.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-surface-codes-and-repeated-syndrome-measurements-2"></span>

### 31.2 Logical operators and distance

**Core result / role:** Homological logical strings and distance.

**Assumptions and scope:** Explicit planar patch and boundary types.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove commuting non-stabilizer string action and derive the selected minimum distance.

**Imported earlier results:** [31.1](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-1).

**Exact source targets:** [P7:7.18.4](../references/proof-sources.md#source-p7-7-18-4): Section 7.18.4 Planar surface codes.

**Independent evidence target:** Enumerate small-patch representatives and verify claimed distance.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-surface-codes-and-repeated-syndrome-measurements-3"></span>

### 31.3 Syndrome-extraction circuits

**Core result / role:** Check schedules determine propagated hook errors.

**Assumptions and scope:** Explicit CNOT order and ancilla reset/measurement.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive each check and propagate a selected ancilla fault through the schedule.

**Imported earlier results:** [31.1](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-1), [30.7](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-7).

**Exact source targets:** [SURFACE:circuits](../references/proof-sources.md#source-surface-circuits): Fig. 1 and Sections III-V; gate-level stabilizer cycle.

**Independent evidence target:** Verify ideal checks and selected data/ancilla fault effects.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-surface-codes-and-repeated-syndrome-measurements-4"></span>

### 31.4 Measurement faults and detection events

**Core result / role:** Repeated measurements produce detection events.

**Assumptions and scope:** Explicit initial/final boundary conventions and measurement faults.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive time-difference records and enumerate single-fault event patterns.

**Imported earlier results:** [31.3](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-3), [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Exact source targets:** [SURFACE:decoding](../references/proof-sources.md#source-surface-decoding): Section VII Error Detection; Section VII A and Fig. 5; noise list.

**Independent evidence target:** Hand-enumerate detection patterns for a small number of rounds.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-surface-codes-and-repeated-syndrome-measurements-5"></span>

### 31.5 Space-time decoding

**Core result / role:** Space-time matching solves a selected decoding surrogate.

**Assumptions and scope:** Declared independent edge model and graph weights.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive graph construction and weight likelihoods; distinguish matching surrogate from exact correlated maximum likelihood.

**Imported earlier results:** [31.4](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-4), [30.8](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-8).

**Exact source targets:** [SURFACE:decoding](../references/proof-sources.md#source-surface-decoding): Section VII Error Detection; Section VII A and Fig. 5; noise list.

**Independent evidence target:** Compare decoder inputs/outputs with independently enumerated faults.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-surface-codes-and-repeated-syndrome-measurements-6"></span>

### 31.6 Logical memory and failure observables

**Core result / role:** Logical-memory failure is a logical-observable event.

**Assumptions and scope:** Specified preparation, rounds, decoding and final logical readout.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove frame-adjusted success criterion and distinguish physical faults from logical failure.

**Imported earlier results:** [31.2](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-2), [31.3](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-3), [31.5](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-5).

**Exact source targets:** [SURFACE:decoding](../references/proof-sources.md#source-surface-decoding): Section VII Error Detection; Section VII A and Fig. 5; noise list.

**Independent evidence target:** Verify a tiny noiseless memory experiment and injected logical failures.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-surface-codes-and-repeated-syndrome-measurements-7"></span>

### 31.7 Finite-size scaling and threshold claims

**Core result / role:** Threshold and finite-size scaling have model-specific meanings.

**Assumptions and scope:** Fixed noise/circuit/decoder family and scaling ansatz.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Define threshold precisely; separate theorem, finite crossing fit and extrapolation; defer broad threshold proof to 32.4.

**Imported earlier results:** [31.6](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-6), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Exact source targets:** [P7:7.18.5](../references/proof-sources.md#source-p7-7-18-5): Section 7.18.5 Surface code accuracy threshold; [SURFACE:threshold](../references/proof-sources.md#source-surface-threshold): Section VII, Fig. 4 and Eqs. (10)-(13); model-specific empirical scaling.

**Independent evidence target:** Report confidence intervals and distinguish an illustrative crossing from a threshold proof.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local advanced bridge to supply:** Threshold definition, thermodynamic/scaling limits and confidence in fitted crossings.

**Explicitly deferred proof ingredients:** General threshold theorem is assigned to 32.4; finite source simulations do not prove asymptotic threshold or universal scaling.

<span id="sec-surface-codes-and-repeated-syndrome-measurements-8"></span>

### 31.8 Surface-code laboratory

**Core result / role:** Surface-code acceptance protocol.

**Assumptions and scope:** Independent patch/check construction and tiny fault enumeration.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Verify boundaries, round conventions, failure observable and uncertainty.

**Imported earlier results:** [31.4](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-4), [31.5](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-5), [31.6](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-6), [31.7](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-7).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Preserve seeds and failure examples and cross-check a tractable subset exactly.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 32: Fault-Tolerant Gates and Universal Logical Computation

<span id="sec-fault-tolerant-gates-and-universal-logical-computation-1"></span>

### 32.1 Fault tolerance and propagation of errors

**Core result / role:** Fault tolerance is a bounded fault-propagation contract.

**Assumptions and scope:** Declared gadget, code distance and noise/fault model.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** State the selected fault-count correctness conditions and test a violating circuit.

**Imported earlier results:** [28.1](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-1), [30.7](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-7).

**Exact source targets:** [NC:10.6.1](../references/proof-sources.md#source-nc-10-6-1): Section 10.6.1 Fault-tolerance: the big picture.

**Independent evidence target:** Track single faults through circuits and identify dangerous propagation.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-fault-tolerant-gates-and-universal-logical-computation-2"></span>

### 32.2 Fault-tolerant preparation, measurement, and recovery

**Core result / role:** Selected fault-tolerant preparation/measurement/recovery gadget.

**Assumptions and scope:** Explicit code and bounded fault count.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Track every relevant single fault and prove the selected gadget's acceptance/correctness claim.

**Imported earlier results:** [32.1](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-1), [29.6](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-6).

**Exact source targets:** [NC:10.6.3](../references/proof-sources.md#source-nc-10-6-3): Section 10.6.3 Fault-tolerant measurement; [FT:gadgets](../references/proof-sources.md#source-ft-gadgets): Section 2 Fault-tolerant simulation at level 1 and Section 3 correctness.

**Independent evidence target:** Enumerate a small gadget's faults and compare logical effects.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-fault-tolerant-gates-and-universal-logical-computation-3"></span>

### 32.3 Transversal operations and their limits

**Core result / role:** Selected transversal actions and the Eastin-Knill obstruction (Theorem 1).

**Assumptions and scope:** Finite code; stated continuous/transversal gate assumptions.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Prove selected transversal actions; state the precise no-go theorem and defer its general proof.

**Imported earlier results:** [32.1](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-1), [30.5](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-5).

**Exact source targets:** [NC:10.6.2](../references/proof-sources.md#source-nc-10-6-2): Section 10.6.2 Fault-tolerant quantum logic; [EK:theorem](../references/proof-sources.md#source-ek-theorem): Theorem 1, product-gate no-go theorem and proof.

**Independent evidence target:** Compare physical transversal operations with encoded logical matrices.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local advanced bridge to supply:** Product representations, local error detection and compact Lie-group/tangent-space vocabulary.

**Explicitly deferred proof ingredients:** General connected-component/Lie-algebra argument of Eastin-Knill Theorem 1; selected transversal conjugations are proved locally.

<span id="sec-fault-tolerant-gates-and-universal-logical-computation-4"></span>

### 32.4 Threshold reasoning [Advanced]

**Core result / role:** AGP independent-stochastic-noise accuracy threshold (Theorem 1).

**Assumptions and scope:** Independent stochastic fault model, gadget conditions and recursive construction.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Derive a toy level-reduction recurrence; state the full selected theorem and roadmap malignant-set/level-reduction lemmas.

**Imported earlier results:** [32.1](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-1), [32.2](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-2), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Exact source targets:** [FT:threshold](../references/proof-sources.md#source-ft-threshold): Section 4, Theorem 1: independent stochastic noise threshold.

**Independent evidence target:** Analyze a tractable recursion or gadget bound without presenting a finite simulation as a theorem.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local advanced bridge to supply:** Rectangles/exRecs, correctness, malignant fault sets and independent stochastic noise.

**Explicitly deferred proof ingredients:** Full AGP good-implies-correct and level-reduction lemmas supporting Section 4 Theorem 1; only the declared toy recurrence is proved locally.

<span id="sec-fault-tolerant-gates-and-universal-logical-computation-5"></span>

### 32.5 Code deformation and lattice surgery

**Core result / role:** Lattice-surgery parity measurement.

**Assumptions and scope:** Specified patch boundaries, merges/splits and logical basis.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the logical parity projector and correction records; separate the ideal operation from noisy gadget evidence.

**Imported earlier results:** [31.1](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-1), [31.3](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-3), [32.2](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-2).

**Exact source targets:** [RESOURCE:surgery](../references/proof-sources.md#source-resource-surgery): Patch operations and Section 1.1 Pauli product measurements.

**Independent evidence target:** Verify ideal logical branches and the required classical interpretation.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-fault-tolerant-gates-and-universal-logical-computation-6"></span>

### 32.6 Magic states and gate injection

**Core result / role:** Magic-state injection correctness.

**Assumptions and scope:** Specified non-Clifford resource state; ideal Clifford operations and measurement.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Expand conditional branches and prove the required logical correction.

**Imported earlier results:** [7.5](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-5), [30.5](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-5), [32.3](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-3).

**Exact source targets:** [DISTILL:protocol](../references/proof-sources.md#source-distill-protocol): Magic-state injection and selected distillation constructions/proofs.

**Independent evidence target:** Check every measurement branch on a general logical input.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-fault-tolerant-gates-and-universal-logical-computation-7"></span>

### 32.7 Distillation and rejection costs

**Core result / role:** Selected distillation map and acceptance overhead.

**Assumptions and scope:** 15-qubit Reed-Muller protocol for a modern T-gate resource, Clifford-equivalent to the H-type state in Bravyi-Kitaev terminology; ideal Clifford checks and transformed independent phase-error model.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Declare the state/basis conversion; derive the selected protocol's finite input/output-error and rejection polynomial, retaining independent-input assumptions.

**Imported earlier results:** [32.6](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-6), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Exact source targets:** [DISTILL:protocol](../references/proof-sources.md#source-distill-protocol): Magic-state injection and selected distillation constructions/proofs.

**Independent evidence target:** Compare exact small calculations and stochastic estimates, including rejected attempts.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-fault-tolerant-gates-and-universal-logical-computation-8"></span>

### 32.8 Universal logical computation laboratory

**Core result / role:** Logical-computation acceptance protocol.

**Assumptions and scope:** Declared gadget/noise model and complete resource record.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Verify accepted branches, correction frames, failure probabilities and rejection costs.

**Imported earlier results:** [32.2](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-2), [32.3](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-3), [32.6](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-6), [32.7](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-7).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Report fault assumptions, logical error, acceptance and total resource consumption.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 33: From Logical Algorithms to Physical Resource Estimates

<span id="sec-from-logical-algorithms-to-physical-resource-estimates-1"></span>

### 33.1 Define an algorithmic workload and success target

**Core result / role:** Resource estimate begins with a specified workload.

**Assumptions and scope:** Exact logical task, accuracy and success target.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Define counted operations, workspace, output and oracle assumptions.

**Imported earlier results:** [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Exact source targets:** [RESOURCE:overview](../references/proof-sources.md#source-resource-overview): Introduction and Section 1 Clifford+T quantum circuits.

**Independent evidence target:** Create an auditable workload record rather than a hardware-independent headline.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-from-logical-algorithms-to-physical-resource-estimates-2"></span>

### 33.2 Logical synthesis and non-Clifford resources

**Core result / role:** Non-Clifford count depends on a synthesis contract.

**Assumptions and scope:** Chosen logical basis and rotation tolerances.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Combine selected decomposition counts; distinguish T count, T depth and arbitrary rotations.

**Imported earlier results:** [5.7](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-7), [32.6](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-6).

**Exact source targets:** [ROSS:synthesis](../references/proof-sources.md#source-ross-synthesis): Sections 7-8: approximate synthesis algorithm and its analysis; [RESOURCE:overview](../references/proof-sources.md#source-resource-overview): Introduction and Section 1 Clifford+T quantum circuits.

**Independent evidence target:** Check counts, synthesis precision and assumptions against a tiny explicit decomposition.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-from-logical-algorithms-to-physical-resource-estimates-3"></span>

### 33.3 Distributing an error budget

**Core result / role:** Union-bound and norm error budgets.

**Assumptions and scope:** Declared coherent/incoherent error measures and event models.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove the selected additive budget and explain when independence is unnecessary or insufficient.

**Imported earlier results:** [33.1](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-1), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Exact source targets:** [NC:A1](../references/proof-sources.md#source-nc-a1): Appendix 1: Notes on basic probability theory; [TQI:1.1.3](../references/proof-sources.md#source-tqi-1-1-3): Section 1.1.3 Operator decompositions and norms.

**Independent evidence target:** Recompute allocations and identify invalid independence assumptions.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-from-logical-algorithms-to-physical-resource-estimates-4"></span>

### 33.4 Code distance and logical reliability

**Core result / role:** Distance selection from an assumed logical-error law.

**Assumptions and scope:** Explicit phenomenological fit and valid parameter domain.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Solve the reliability inequality; expose sensitivity and extrapolation limits.

**Imported earlier results:** [32.4](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-4), [33.3](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-3).

**Exact source targets:** [RESOURCE:cost](../references/proof-sources.md#source-resource-cost): Section 4 tradeoffs, especially 4.3 distance selection, and Section 5; [SURFACE:threshold](../references/proof-sources.md#source-surface-threshold): Section VII, Fig. 4 and Eqs. (10)-(13); model-specific empirical scaling.

**Independent evidence target:** Sweep model parameters and label empirical fits versus proven bounds.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-from-logical-algorithms-to-physical-resource-estimates-5"></span>

### 33.5 Magic-state factories and scheduling

**Core result / role:** Factories impose throughput and scheduling constraints.

**Assumptions and scope:** Specified factory error/yield/latency and consumption schedule.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive rate and buffer requirements; count rejected attempts and idle time.

**Imported earlier results:** [32.7](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-7), [33.2](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-2).

**Exact source targets:** [RESOURCE:factories](../references/proof-sources.md#source-resource-factories): Section 3 Distillation blocks.

**Independent evidence target:** Check a small factory/data schedule and account for idle resources.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-from-logical-algorithms-to-physical-resource-estimates-6"></span>

### 33.6 Physical qubits, cycles, and runtime

**Core result / role:** Physical qubit-time is an architecture-dependent calculation.

**Assumptions and scope:** Declared patch/gadget/factory/timing model.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive qubit, cycle and runtime totals for one named workload.

**Imported earlier results:** [33.4](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-4), [33.5](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-5).

**Exact source targets:** [RESOURCE:cost](../references/proof-sources.md#source-resource-cost): Section 4 tradeoffs, especially 4.3 distance selection, and Section 5.

**Independent evidence target:** Verify units and compare component sums with a complete ledger.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-from-logical-algorithms-to-physical-resource-estimates-7"></span>

### 33.7 Sensitivity, uncertainty, and comparison

**Core result / role:** Resource sensitivity and uncertainty.

**Assumptions and scope:** Uncertain physical parameters and fixed workload/model.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Differentiate or sweep the estimate; distinguish sensitivity analysis from measured performance.

**Imported earlier results:** [33.6](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-6), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Exact source targets:** [RESOURCE:cost](../references/proof-sources.md#source-resource-cost): Section 4 tradeoffs, especially 4.3 distance selection, and Section 5; [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Report ranges and alternative assumptions rather than one unsupported number.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-from-logical-algorithms-to-physical-resource-estimates-8"></span>

### 33.8 Resource-estimation laboratory

**Core result / role:** Resource-estimation acceptance protocol.

**Assumptions and scope:** Traceable source assumptions and an independently recomputed budget.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Publish all parameters, error allocations, rejected work and comparison scope.

**Imported earlier results:** [33.1](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-1), [33.3](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-3), [33.6](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-6), [33.7](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-7).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Reproduce an estimate from versioned inputs and distinguish projections from device measurements.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.
