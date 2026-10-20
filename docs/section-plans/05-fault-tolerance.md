# Part 5. Noise, Error Correction, and Fault-Tolerant Computation

**Detailed plan · 2026-10-20 · Planned material; editorial pass completed, external validation/freeze pending.** [All sections](../section-plan.md) · [Full plan](../book-plan.md) · [Reader continuity](../reader-continuity.md)

Each section specifies its argument and independent evidence. Framework implementation, mathematical review and reader review have separate status. Closing materials follow the [section-plan guide](../section-plan.md#how-to-read-the-specification).

<span id="ch-noise-open-systems-and-error-mitigation"></span>

## Chapter 28

**Noise, Open Systems, and Error Mitigation**

**Reading level:** Core. **Entry guidance:** 8–9 for channels; local time-evolution/differential-equation bridge for the dynamics branch.

<span id="sec-noise-open-systems-and-error-mitigation-1"></span>

### 28.1 Noise models and system-environment assumptions

**Section level:** core. **Required earlier sections:** [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3).

**Learning and derivation target:** State memory, correlation and initial-state assumptions of a noise description.

**Implementation and evidence target:** Compare a named channel model with its explicit environment construction.

<span id="sec-noise-open-systems-and-error-mitigation-2"></span>

### 28.2 Discrete channels: dephasing and depolarization

**Section level:** core. **Required earlier sections:** [28.1](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-1), [3.3](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-3).

**Learning and derivation target:** Derive channel action in state/Bloch representations.

**Implementation and evidence target:** Verify limiting cases, fixed points, trace and positivity.

<span id="sec-noise-open-systems-and-error-mitigation-3"></span>

### 28.3 Amplitude damping and relaxation

**Section level:** core. **Required earlier sections:** [28.1](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-1), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3).

**Learning and derivation target:** Derive Kraus operators and their physical parameter interpretation.

**Implementation and evidence target:** Compare density evolution with an independent matrix calculation.

<span id="sec-noise-open-systems-and-error-mitigation-4"></span>

### 28.4 Lindblad dynamics

**Section level:** core. **Required earlier sections:** [28.1](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-1), [2.6](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-6).

**Learning and derivation target:** Derive a simple generator and state the Markovian approximation assumptions.

**Implementation and evidence target:** Compare analytic evolution and an independent ODE/exponential reference.

<span id="sec-noise-open-systems-and-error-mitigation-5"></span>

### 28.5 Quantum trajectories and unravelings

**Section level:** core. **Required earlier sections:** [28.4](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-4), [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6), [9.7](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-7).

**Learning and derivation target:** Explain conditional stochastic evolution and averaging over records.

**Implementation and evidence target:** Compare trajectory averages with deterministic density evolution and uncertainty.

<span id="sec-noise-open-systems-and-error-mitigation-6"></span>

### 28.6 Correlated and non-Markovian limitations [Advanced]

**Section level:** advanced. **Required earlier sections:** [28.1](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-1), [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4).

**Learning and derivation target:** Give a concrete model that violates an independent-memoryless assumption.

**Implementation and evidence target:** Show which correlations the simple channel model cannot reproduce.

<span id="sec-noise-open-systems-and-error-mitigation-7"></span>

### 28.7 Error mitigation: bias, variance, and cost

**Section level:** core. **Required earlier sections:** [28.2](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-2), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Learning and derivation target:** Derive one scoped mitigation estimator and its noise-model requirements.

**Implementation and evidence target:** Compare bias, variance and execution overhead under controlled model mismatch.

<span id="sec-noise-open-systems-and-error-mitigation-8"></span>

### 28.8 Calibration, drift, and model validation

**Section level:** core. **Required earlier sections:** [28.1](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-1), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Learning and derivation target:** Explain parameter inference and the limits of transferring a calibration across time/tasks.

**Implementation and evidence target:** Compare held-out synthetic/available data with a fitted model and record provenance.

<span id="sec-device-characterization-benchmarking"></span>

### 28.9 SPAM, gate characterization, and randomized benchmarking [Advanced]

**Section level:** advanced. **Required earlier sections:** [9.5](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-5), [10.5](../section-plans/02-information.md#sec-channel-error-metrics), [10.6](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-5), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Learning and derivation target:** Distinguish preparation/measurement error, process tomography and randomized benchmarking. Introduce the needed finite gate-ensemble/twirling bridge locally, derive one decay model, and state stationarity/gate-dependence assumptions.

**Implementation and evidence target:** Fit synthetic records from a known model and a mismatched model; report uncertainty and avoid treating one decay parameter as every circuit’s failure probability.

<span id="sec-noise-open-systems-and-error-mitigation-9"></span>
<span id="289-noise-laboratory-and-evidence-boundaries"></span>

### 28.10 Noise laboratory and evidence boundaries

**Section level:** core. **Required earlier sections:** [28.2](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-2), [28.3](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-3), [28.4](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-4), [28.8](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-8), [28.9](../section-plans/05-fault-tolerance.md#sec-device-characterization-benchmarking).

**Learning and derivation target:** Separate ideal simulation, stochastic noise models and hardware observations.

**Implementation and evidence target:** Report all model assumptions and independent solver/statistical checks.

<span id="ch-quantum-error-correction-conditions-and-recovery"></span>

## Chapter 29

**Quantum Error Correction: Conditions and Recovery**

**Reading level:** Core. **Entry guidance:** 4–6, 8–9; selected 28 for physical noise examples.

<span id="sec-quantum-error-correction-conditions-and-recovery-1"></span>

### 29.1 The quantum error-correction problem

**Section level:** core. **Required earlier sections:** [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2).

**Learning and derivation target:** Explain why copying, direct logical measurement and classical redundancy need care.

**Implementation and evidence target:** Analyze failed correction proposals on an unknown superposition.

<span id="sec-quantum-error-correction-conditions-and-recovery-2"></span>

### 29.2 Encoding and logical information

**Section level:** core. **Required earlier sections:** [29.1](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-1), [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3).

**Learning and derivation target:** Define a code subspace, encoding isometry and logical observables.

**Implementation and evidence target:** Verify preservation of arbitrary encoded amplitudes.

<span id="sec-quantum-error-correction-conditions-and-recovery-3"></span>

### 29.3 Repetition codes and syndrome extraction

**Section level:** core. **Required earlier sections:** [29.2](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-2), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2).

**Learning and derivation target:** Derive bit-flip checks and why syndrome measurement need not reveal the logical state.

**Implementation and evidence target:** Enumerate errors and compare conditional post-measurement states.

<span id="sec-quantum-error-correction-conditions-and-recovery-4"></span>

### 29.4 Error sets and coherent combinations

**Section level:** core. **Required earlier sections:** [29.2](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-2), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3).

**Learning and derivation target:** Explain the operator-span argument and the role of distinguishable error actions.

**Implementation and evidence target:** Test coherent combinations instead of only stochastic Pauli injections.

<span id="sec-quantum-error-correction-conditions-and-recovery-5"></span>

### 29.5 Knill-Laflamme conditions

**Section level:** core. **Required earlier sections:** [29.4](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-4), [2.4](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-4).

**Learning and derivation target:** State and prove the finite-dimensional correction condition at the declared level.

**Implementation and evidence target:** Verify the matrix conditions on an explicit small code.

<span id="sec-quantum-error-correction-conditions-and-recovery-6"></span>

### 29.6 Constructing a recovery operation

**Section level:** core. **Required earlier sections:** [29.5](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-5), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3).

**Learning and derivation target:** Derive a recovery from correctable error subspaces and specify trace-preserving completion.

**Implementation and evidence target:** Compare recovered states with the encoded reference.

<span id="sec-quantum-error-correction-conditions-and-recovery-7"></span>

### 29.7 Degeneracy, distance, and limitations

**Section level:** core. **Required earlier sections:** [29.5](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-5), [29.6](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-6).

**Learning and derivation target:** Explain indistinguishable error actions, uncorrectable errors and the meaning of distance.

**Implementation and evidence target:** Construct correctable and failing error patterns.

<span id="sec-quantum-error-correction-conditions-and-recovery-8"></span>

### 29.8 Beyond bit-flip protection

**Section level:** core. **Required earlier sections:** [29.3](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-3), [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5).

**Learning and derivation target:** Derive a small concatenated bit/phase repetition construction without relying on undeveloped stabilizer or CSS terminology; those generalizations belong to Chapter 30.

**Implementation and evidence target:** Verify nontrivial superpositions under independent error types.

<span id="sec-quantum-error-correction-conditions-and-recovery-9"></span>

### 29.9 Recovery laboratory and logical-state verification

**Section level:** core. **Required earlier sections:** [29.5](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-5), [29.6](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-6), [29.8](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-8).

**Learning and derivation target:** Connect encoding, noise, syndrome record, correction and decoded output.

**Implementation and evidence target:** Check a spanning operator basis or an equivalent complete small-code reference; quantify failures.

<span id="ch-stabilizer-codes-logical-operators-and-decoding"></span>

## Chapter 30

**Stabilizer Codes, Logical Operators, and Decoding**

**Reading level:** Core with advanced extensions. **Entry guidance:** 4–6 for Pauli/stabilizer entry; 29 for code/recovery branches; binary algebra is local.

<span id="sec-stabilizer-codes-logical-operators-and-decoding-1"></span>

### 30.1 Pauli groups and binary symplectic algebra

**Section level:** core. **Required earlier sections:** [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5), [4.3](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-3).

**Learning and derivation target:** Introduce arithmetic over the binary field, elementary row reduction and group terminology locally; derive Pauli binary/phase representation and the symplectic commutation form.

**Implementation and evidence target:** Compare binary operations with dense Pauli products.

<span id="sec-stabilizer-codes-logical-operators-and-decoding-2"></span>

### 30.2 Stabilizer groups and code spaces

**Section level:** core. **Required earlier sections:** [30.1](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-1).

**Learning and derivation target:** Derive projector/dimension formulas under independence assumptions.

**Implementation and evidence target:** Compare stabilizer projectors with explicit code-state bases.

<span id="sec-stabilizer-codes-logical-operators-and-decoding-3"></span>

### 30.3 Syndromes as commutation data

**Section level:** core. **Required earlier sections:** [30.2](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-2), [29.3](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-3).

**Learning and derivation target:** Derive the syndrome map for Pauli errors.

**Implementation and evidence target:** Check every single-qubit error on a small code.

<span id="sec-stabilizer-codes-logical-operators-and-decoding-4"></span>

### 30.4 CSS codes from classical checks

**Section level:** core. **Required earlier sections:** [30.1](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-1), [30.2](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-2).

**Learning and derivation target:** Derive the commutation/orthogonality conditions of CSS constructions.

**Implementation and evidence target:** Build and verify a selected tiny CSS code.

<span id="sec-stabilizer-codes-logical-operators-and-decoding-5"></span>

### 30.5 Logical operators and code distance

**Section level:** core. **Required earlier sections:** [30.2](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-2), [30.3](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-3), [29.7](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-7).

**Learning and derivation target:** Derive the normalizer quotient interpretation and identify logical representatives.

**Implementation and evidence target:** Enumerate low-weight operators and verify distance for the tiny code.

<span id="sec-stabilizer-codes-logical-operators-and-decoding-6"></span>

### 30.6 Degeneracy and decoding choices

**Section level:** core. **Required earlier sections:** [30.3](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-3), [30.5](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-5).

**Learning and derivation target:** Explain why the same syndrome can admit physically different corrections.

**Implementation and evidence target:** Compare decoders using logical equivalence rather than exact error identity.

<span id="sec-stabilizer-codes-logical-operators-and-decoding-7"></span>

### 30.7 Syndrome circuits and fault propagation

**Section level:** core. **Required earlier sections:** [30.3](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-3), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Learning and derivation target:** Derive a check-measurement circuit and track ancilla-induced faults.

**Implementation and evidence target:** Compare ideal syndrome outcomes and enumerated circuit faults.

<span id="sec-stabilizer-codes-logical-operators-and-decoding-8"></span>

### 30.8 Decoder interfaces and evidence records

**Section level:** core. **Required earlier sections:** [30.5](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-5), [30.6](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-6).

**Learning and derivation target:** Specify syndrome layout, boundaries, correction representation and logical success.

**Implementation and evidence target:** Check an interchangeable decoder against exact hand-enumerated cases.

<span id="sec-quantum-ldpc-architecture"></span>

### 30.9 Quantum LDPC families and architectural tradeoffs [Advanced]

**Section level:** advanced. **Required earlier sections:** [30.4](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-4), [30.5](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-5), [30.7](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-7).

**Learning and derivation target:** Define bounded-weight checks and code-rate/distance questions; connect one explicit CSS construction to connectivity, measurement circuits and decoder requirements without universal performance claims.

**Implementation and evidence target:** Verify a tiny check matrix, commutation and logical operators; compare cost assumptions with a small surface-code model under matched declared noise/decoder conditions.

<span id="sec-stabilizer-graph-state-mbqc"></span>
<span id="309-graph-states-and-measurement-based-computation"></span>

### 30.10 Graph states and measurement-based computation

**Section level:** core. **Required earlier sections:** [30.1](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-1), [30.2](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-2), [7.5](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-5).

**Learning and derivation target:** Derive a one-step measurement-based gate from teleportation and graph-state stabilizers, including adaptive corrections.

**Implementation and evidence target:** Check every branch and the corrected logical action; provide the theoretical bridge to photonic resource-state computation.

<span id="sec-stabilizer-codes-logical-operators-and-decoding-9"></span>
<span id="3010-stabilizer-code-laboratory"></span>
<span id="309-stabilizer-code-laboratory"></span>

### 30.11 Stabilizer-code laboratory

**Section level:** core. **Required earlier sections:** [30.3](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-3), [30.4](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-4), [30.5](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-5), [30.7](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-7), [30.8](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-8).

**Learning and derivation target:** Connect algebra, circuits, syndrome decoding and logical observables.

**Implementation and evidence target:** Compare independent binary and dense calculations before large experiments.

<span id="ch-surface-codes-and-repeated-syndrome-measurements"></span>

## Chapter 31

**Surface Codes and Repeated Syndrome Measurements**

**Reading level:** Advanced. **Entry guidance:** Selected noise, correction and stabilizer sections in 28–30.

<span id="sec-surface-codes-and-repeated-syndrome-measurements-1"></span>

### 31.1 From stabilizer checks to a surface-code lattice

**Section level:** advanced. **Required earlier sections:** [30.4](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-4), [30.5](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-5).

**Learning and derivation target:** Define a chosen patch, qubit layout, checks and boundaries precisely.

**Implementation and evidence target:** Compare the lattice description with an independently built commutation matrix.

<span id="sec-surface-codes-and-repeated-syndrome-measurements-2"></span>

### 31.2 Logical operators and distance

**Section level:** advanced. **Required earlier sections:** [31.1](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-1).

**Learning and derivation target:** Derive logical strings and the minimum-weight mechanism for the selected boundaries.

**Implementation and evidence target:** Enumerate small-patch representatives and verify claimed distance.

<span id="sec-surface-codes-and-repeated-syndrome-measurements-3"></span>

### 31.3 Syndrome-extraction circuits

**Section level:** advanced. **Required earlier sections:** [31.1](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-1), [30.7](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-7).

**Learning and derivation target:** Derive a repeated check schedule and explain scheduling/fault-propagation constraints.

**Implementation and evidence target:** Verify ideal checks and selected data/ancilla fault effects.

<span id="sec-surface-codes-and-repeated-syndrome-measurements-4"></span>

### 31.4 Measurement faults and detection events

**Section level:** advanced. **Required earlier sections:** [31.3](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-3), [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Learning and derivation target:** Derive how successive syndrome differences expose space-time faults.

**Implementation and evidence target:** Hand-enumerate detection patterns for a small number of rounds.

<span id="sec-surface-codes-and-repeated-syndrome-measurements-5"></span>

### 31.5 Space-time decoding

**Section level:** advanced. **Required earlier sections:** [31.4](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-4), [30.8](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-8).

**Learning and derivation target:** State the noise model, graph and boundary conventions of a selected decoder.

**Implementation and evidence target:** Compare decoder inputs/outputs with independently enumerated faults.

<span id="sec-surface-codes-and-repeated-syndrome-measurements-6"></span>

### 31.6 Logical memory and failure observables

**Section level:** advanced. **Required earlier sections:** [31.2](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-2), [31.3](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-3), [31.5](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-5).

**Learning and derivation target:** Define preparation, rounds, final readout and the logical failure criterion.

**Implementation and evidence target:** Verify a tiny noiseless memory experiment and injected logical failures.

<span id="sec-surface-codes-and-repeated-syndrome-measurements-7"></span>

### 31.7 Finite-size scaling and threshold claims

**Section level:** advanced. **Required earlier sections:** [31.6](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-6), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Learning and derivation target:** Explain per-round/per-shot metrics, uncertainty and the assumptions behind scaling analysis.

**Implementation and evidence target:** Report confidence intervals and distinguish an illustrative crossing from a threshold proof.

<span id="sec-surface-codes-and-repeated-syndrome-measurements-8"></span>

### 31.8 Surface-code laboratory

**Section level:** advanced. **Required earlier sections:** [31.4](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-4), [31.5](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-5), [31.6](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-6), [31.7](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-7).

**Learning and derivation target:** Integrate layout, circuit schedule, noise, decoder and logical readout.

**Implementation and evidence target:** Preserve seeds and failure examples and cross-check a tractable subset exactly.

<span id="ch-fault-tolerant-gates-and-universal-logical-computation"></span>

## Chapter 32

**Fault-Tolerant Gates and Universal Logical Computation**

**Reading level:** Advanced. **Entry guidance:** 28–30; 31 only for the surface-code/lattice-surgery branch; factoring is not required.

<span id="sec-fault-tolerant-gates-and-universal-logical-computation-1"></span>

### 32.1 Fault tolerance and propagation of errors

**Section level:** advanced. **Required earlier sections:** [28.1](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-1), [30.7](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-7).

**Learning and derivation target:** Define a fault model and the containment property of a selected operation.

**Implementation and evidence target:** Track single faults through circuits and identify dangerous propagation.

<span id="sec-fault-tolerant-gates-and-universal-logical-computation-2"></span>

### 32.2 Fault-tolerant preparation, measurement, and recovery

**Section level:** advanced. **Required earlier sections:** [32.1](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-1), [29.6](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-6).

**Learning and derivation target:** Explain why correction circuitry itself must satisfy fault constraints.

**Implementation and evidence target:** Enumerate a small gadget's faults and compare logical effects.

<span id="sec-fault-tolerant-gates-and-universal-logical-computation-3"></span>

### 32.3 Transversal operations and their limits

**Section level:** advanced. **Required earlier sections:** [32.1](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-1), [30.5](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-5).

**Learning and derivation target:** Derive selected logical actions and state a relevant universality limitation with assumptions.

**Implementation and evidence target:** Compare physical transversal operations with encoded logical matrices.

<span id="sec-fault-tolerant-gates-and-universal-logical-computation-4"></span>

### 32.4 Threshold reasoning [Advanced]

**Section level:** advanced. **Required earlier sections:** [32.1](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-1), [32.2](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-2), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Learning and derivation target:** State a selected threshold theorem, its noise/locality assumptions and proof roadmap.

**Implementation and evidence target:** Analyze a tractable recursion or gadget bound without presenting a finite simulation as a theorem.

<span id="sec-fault-tolerant-gates-and-universal-logical-computation-5"></span>

### 32.5 Code deformation and lattice surgery

**Section level:** advanced. **Required earlier sections:** [31.1](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-1), [31.3](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-3), [32.2](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-2).

**Learning and derivation target:** Derive one logical measurement/operation from changing or merging checks.

**Implementation and evidence target:** Verify ideal logical branches and the required classical interpretation.

<span id="sec-fault-tolerant-gates-and-universal-logical-computation-6"></span>

### 32.6 Magic states and gate injection

**Section level:** advanced. **Required earlier sections:** [7.5](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-5), [30.5](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-5), [32.3](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-3).

**Learning and derivation target:** Derive a selected injection protocol, corrections and consumed resources.

**Implementation and evidence target:** Check every measurement branch on a general logical input.

<span id="sec-fault-tolerant-gates-and-universal-logical-computation-7"></span>

### 32.7 Distillation and rejection costs

**Section level:** advanced. **Required earlier sections:** [32.6](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-6), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Learning and derivation target:** Derive a small protocol's acceptance/error mechanism under a specified input model.

**Implementation and evidence target:** Compare exact small calculations and stochastic estimates, including rejected attempts.

<span id="sec-fault-tolerant-gates-and-universal-logical-computation-8"></span>

### 32.8 Universal logical computation laboratory

**Section level:** advanced. **Required earlier sections:** [32.2](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-2), [32.3](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-3), [32.6](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-6), [32.7](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-7).

**Learning and derivation target:** Assemble a scoped logical operation with preparation, control and verification.

**Implementation and evidence target:** Report fault assumptions, logical error, acceptance and total resource consumption.

<span id="ch-from-logical-algorithms-to-physical-resource-estimates"></span>

## Chapter 33

**From Logical Algorithms to Physical Resource Estimates**

**Reading level:** Advanced synthesis. **Entry guidance:** 14 and selected logical-computation sections of 32; a chosen algorithm workload, not every algorithm chapter.

<span id="sec-from-logical-algorithms-to-physical-resource-estimates-1"></span>

### 33.1 Define an algorithmic workload and success target

**Section level:** advanced. **Required earlier sections:** [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Learning and derivation target:** Specify input/output accuracy, overall failure budget and logical circuit.

**Implementation and evidence target:** Create an auditable workload record rather than a hardware-independent headline.

<span id="sec-from-logical-algorithms-to-physical-resource-estimates-2"></span>

### 33.2 Logical synthesis and non-Clifford resources

**Section level:** advanced. **Required earlier sections:** [5.7](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-7), [32.6](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-6).

**Learning and derivation target:** Derive a representative rotation-synthesis budget and count T/Clifford operations.

**Implementation and evidence target:** Check counts, synthesis precision and assumptions against a tiny explicit decomposition.

<span id="sec-from-logical-algorithms-to-physical-resource-estimates-3"></span>

### 33.3 Distributing an error budget

**Section level:** advanced. **Required earlier sections:** [33.1](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-1), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Learning and derivation target:** Use stated bounds to allocate algorithmic, synthesis and logical errors.

**Implementation and evidence target:** Recompute allocations and identify invalid independence assumptions.

<span id="sec-from-logical-algorithms-to-physical-resource-estimates-4"></span>

### 33.4 Code distance and logical reliability

**Section level:** advanced. **Required earlier sections:** [32.4](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-4), [33.3](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-3).

**Learning and derivation target:** Relate a named logical-error model to required reliability and distance.

**Implementation and evidence target:** Sweep model parameters and label empirical fits versus proven bounds.

<span id="sec-from-logical-algorithms-to-physical-resource-estimates-5"></span>

### 33.5 Magic-state factories and scheduling

**Section level:** advanced. **Required earlier sections:** [32.7](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-7), [33.2](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-2).

**Learning and derivation target:** Model production, acceptance, consumption and bottlenecks.

**Implementation and evidence target:** Check a small factory/data schedule and account for idle resources.

<span id="sec-from-logical-algorithms-to-physical-resource-estimates-6"></span>

### 33.6 Physical qubits, cycles, and runtime

**Section level:** advanced. **Required earlier sections:** [33.4](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-4), [33.5](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-5).

**Learning and derivation target:** Derive a full estimate under declared architecture, timing and connectivity assumptions.

**Implementation and evidence target:** Verify units and compare component sums with a complete ledger.

<span id="sec-from-logical-algorithms-to-physical-resource-estimates-7"></span>

### 33.7 Sensitivity, uncertainty, and comparison

**Section level:** advanced. **Required earlier sections:** [33.6](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-6), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Learning and derivation target:** Explain which input assumptions dominate a resource estimate.

**Implementation and evidence target:** Report ranges and alternative assumptions rather than one unsupported number.

<span id="sec-from-logical-algorithms-to-physical-resource-estimates-8"></span>

### 33.8 Resource-estimation laboratory

**Section level:** advanced. **Required earlier sections:** [33.1](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-1), [33.3](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-3), [33.6](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-6), [33.7](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-7).

**Learning and derivation target:** Connect workload, logical synthesis, correction and physical costs.

**Implementation and evidence target:** Reproduce an estimate from versioned inputs and distinguish projections from device measurements.
