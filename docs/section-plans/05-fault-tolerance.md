# Part 5: Noise, Error Correction, and Fault-Tolerant Computation

**Detailed section plan · October 20, 2026 · Planned material.** [All section plans](../section-plan.md) · [Curriculum and prerequisites](../book-plan.md)

Each numbered section specifies its intended argument and independent evidence. The unnumbered closing material and authoring rules are defined in the [section-plan guide](../section-plan.md#how-to-read-the-specification). Implementation status remains separate from curriculum status.

## Chapter 28

**Noise, Open Systems, and Error Mitigation**

**Reading level:** Core. **Chapter prerequisites:** 8–10; 19 for dynamics.

### 28.1 Noise models and system-environment assumptions

**Learning and derivation target:** State memory, correlation and initial-state assumptions of a noise description.

**Implementation and evidence target:** Compare a named channel model with its explicit environment construction.

### 28.2 Discrete channels: dephasing and depolarization

**Learning and derivation target:** Derive channel action in state/Bloch representations.

**Implementation and evidence target:** Verify limiting cases, fixed points, trace and positivity.

### 28.3 Amplitude damping and relaxation

**Learning and derivation target:** Derive Kraus operators and their physical parameter interpretation.

**Implementation and evidence target:** Compare density evolution with an independent matrix calculation.

### 28.4 Lindblad dynamics

**Learning and derivation target:** Derive a simple generator and state the Markovian approximation assumptions.

**Implementation and evidence target:** Compare analytic evolution and an independent ODE/exponential reference.

### 28.5 Quantum trajectories and unravelings

**Learning and derivation target:** Explain conditional stochastic evolution and averaging over records.

**Implementation and evidence target:** Compare trajectory averages with deterministic density evolution and uncertainty.

### 28.6 Correlated and non-Markovian limitations [Advanced]

**Learning and derivation target:** Give a concrete model that violates an independent-memoryless assumption.

**Implementation and evidence target:** Show which correlations the simple channel model cannot reproduce.

### 28.7 Error mitigation: bias, variance, and cost

**Learning and derivation target:** Derive one scoped mitigation estimator and its noise-model requirements.

**Implementation and evidence target:** Compare bias, variance and execution overhead under controlled model mismatch.

### 28.8 Calibration, drift, and model validation

**Learning and derivation target:** Explain parameter inference and the limits of transferring a calibration across time/tasks.

**Implementation and evidence target:** Compare held-out synthetic/available data with a fitted model and record provenance.

### 28.9 Noise laboratory and evidence boundaries

**Learning and derivation target:** Separate ideal simulation, stochastic noise models and hardware observations.

**Implementation and evidence target:** Report all model assumptions and independent solver/statistical checks.

## Chapter 29

**Quantum Error Correction: Conditions and Recovery**

**Reading level:** Core. **Chapter prerequisites:** 7–10, 28.

### 29.1 The quantum error-correction problem

**Learning and derivation target:** Explain why copying, direct logical measurement and classical redundancy need care.

**Implementation and evidence target:** Analyze failed correction proposals on an unknown superposition.

### 29.2 Encoding and logical information

**Learning and derivation target:** Define a code subspace, encoding isometry and logical observables.

**Implementation and evidence target:** Verify preservation of arbitrary encoded amplitudes.

### 29.3 Repetition codes and syndrome extraction

**Learning and derivation target:** Derive bit-flip checks and why syndrome measurement need not reveal the logical state.

**Implementation and evidence target:** Enumerate errors and compare conditional post-measurement states.

### 29.4 Error sets and coherent combinations

**Learning and derivation target:** Explain the operator-span argument and the role of distinguishable error actions.

**Implementation and evidence target:** Test coherent combinations instead of only stochastic Pauli injections.

### 29.5 Knill-Laflamme conditions

**Learning and derivation target:** State and prove the finite-dimensional correction condition at the declared level.

**Implementation and evidence target:** Verify the matrix conditions on an explicit small code.

### 29.6 Constructing a recovery operation

**Learning and derivation target:** Derive a recovery from correctable error subspaces and specify trace-preserving completion.

**Implementation and evidence target:** Compare recovered states with the encoded reference.

### 29.7 Degeneracy, distance, and limitations

**Learning and derivation target:** Explain indistinguishable error actions, uncorrectable errors and the meaning of distance.

**Implementation and evidence target:** Construct correctable and failing error patterns.

### 29.8 Beyond bit-flip protection

**Learning and derivation target:** Derive how a selected code protects against both bit and phase errors.

**Implementation and evidence target:** Verify nontrivial superpositions under independent error types.

### 29.9 Recovery laboratory and logical-state verification

**Learning and derivation target:** Connect encoding, noise, syndrome record, correction and decoded output.

**Implementation and evidence target:** Check a spanning operator basis or an equivalent complete small-code reference; quantify failures.

## Chapter 30

**Stabilizer Codes, Logical Operators, and Decoding**

**Reading level:** Core with advanced extensions. **Chapter prerequisites:** 5–8, 29; binary linear algebra.

### 30.1 Pauli groups and binary symplectic algebra

**Learning and derivation target:** Derive the representation, phase bookkeeping and commutation form.

**Implementation and evidence target:** Compare binary operations with dense Pauli products.

### 30.2 Stabilizer groups and code spaces

**Learning and derivation target:** Derive projector/dimension formulas under independence assumptions.

**Implementation and evidence target:** Compare stabilizer projectors with explicit code-state bases.

### 30.3 Syndromes as commutation data

**Learning and derivation target:** Derive the syndrome map for Pauli errors.

**Implementation and evidence target:** Check every single-qubit error on a small code.

### 30.4 CSS codes from classical checks

**Learning and derivation target:** Derive the commutation/orthogonality conditions of CSS constructions.

**Implementation and evidence target:** Build and verify a selected tiny CSS code.

### 30.5 Logical operators and code distance

**Learning and derivation target:** Derive the normalizer quotient interpretation and identify logical representatives.

**Implementation and evidence target:** Enumerate low-weight operators and verify distance for the tiny code.

### 30.6 Degeneracy and decoding choices

**Learning and derivation target:** Explain why the same syndrome can admit physically different corrections.

**Implementation and evidence target:** Compare decoders using logical equivalence rather than exact error identity.

### 30.7 Syndrome circuits and fault propagation

**Learning and derivation target:** Derive a check-measurement circuit and track ancilla-induced faults.

**Implementation and evidence target:** Compare ideal syndrome outcomes and enumerated circuit faults.

### 30.8 Decoder interfaces and evidence records

**Learning and derivation target:** Specify syndrome layout, boundaries, correction representation and logical success.

**Implementation and evidence target:** Check an interchangeable decoder against exact hand-enumerated cases.

### 30.9 Stabilizer-code laboratory

**Learning and derivation target:** Connect algebra, circuits, syndrome decoding and logical observables.

**Implementation and evidence target:** Compare independent binary and dense calculations before large experiments.

## Chapter 31

**Surface Codes and Repeated Syndrome Measurements**

**Reading level:** Advanced. **Chapter prerequisites:** 28–30.

### 31.1 From stabilizer checks to a surface-code lattice

**Learning and derivation target:** Define a chosen patch, qubit layout, checks and boundaries precisely.

**Implementation and evidence target:** Compare the lattice description with an independently built commutation matrix.

### 31.2 Logical operators and distance

**Learning and derivation target:** Derive logical strings and the minimum-weight mechanism for the selected boundaries.

**Implementation and evidence target:** Enumerate small-patch representatives and verify claimed distance.

### 31.3 Syndrome-extraction circuits

**Learning and derivation target:** Derive a repeated check schedule and explain scheduling/fault-propagation constraints.

**Implementation and evidence target:** Verify ideal checks and selected data/ancilla fault effects.

### 31.4 Measurement faults and detection events

**Learning and derivation target:** Derive how successive syndrome differences expose space-time faults.

**Implementation and evidence target:** Hand-enumerate detection patterns for a small number of rounds.

### 31.5 Space-time decoding

**Learning and derivation target:** State the noise model, graph and boundary conventions of a selected decoder.

**Implementation and evidence target:** Compare decoder inputs/outputs with independently enumerated faults.

### 31.6 Logical memory and failure observables

**Learning and derivation target:** Define preparation, rounds, final readout and the logical failure criterion.

**Implementation and evidence target:** Verify a tiny noiseless memory experiment and injected logical failures.

### 31.7 Finite-size scaling and threshold claims

**Learning and derivation target:** Explain per-round/per-shot metrics, uncertainty and the assumptions behind scaling analysis.

**Implementation and evidence target:** Report confidence intervals and distinguish an illustrative crossing from a threshold proof.

### 31.8 Surface-code laboratory

**Learning and derivation target:** Integrate layout, circuit schedule, noise, decoder and logical readout.

**Implementation and evidence target:** Preserve seeds and failure examples and cross-check a tractable subset exactly.

## Chapter 32

**Fault-Tolerant Gates and Universal Logical Computation**

**Reading level:** Advanced. **Chapter prerequisites:** 5, 18, 28–31.

### 32.1 Fault tolerance and propagation of errors

**Learning and derivation target:** Define a fault model and the containment property of a selected operation.

**Implementation and evidence target:** Track single faults through circuits and identify dangerous propagation.

### 32.2 Fault-tolerant preparation, measurement, and recovery

**Learning and derivation target:** Explain why correction circuitry itself must satisfy fault constraints.

**Implementation and evidence target:** Enumerate a small gadget's faults and compare logical effects.

### 32.3 Transversal operations and their limits

**Learning and derivation target:** Derive selected logical actions and state a relevant universality limitation with assumptions.

**Implementation and evidence target:** Compare physical transversal operations with encoded logical matrices.

### 32.4 Threshold reasoning [Advanced]

**Learning and derivation target:** State a selected threshold theorem, its noise/locality assumptions and proof roadmap.

**Implementation and evidence target:** Analyze a tractable recursion or gadget bound without presenting a finite simulation as a theorem.

### 32.5 Code deformation and lattice surgery

**Learning and derivation target:** Derive one logical measurement/operation from changing or merging checks.

**Implementation and evidence target:** Verify ideal logical branches and the required classical interpretation.

### 32.6 Magic states and gate injection

**Learning and derivation target:** Derive a selected injection protocol, corrections and consumed resources.

**Implementation and evidence target:** Check every measurement branch on a general logical input.

### 32.7 Distillation and rejection costs

**Learning and derivation target:** Derive a small protocol's acceptance/error mechanism under a specified input model.

**Implementation and evidence target:** Compare exact small calculations and stochastic estimates, including rejected attempts.

### 32.8 Universal logical computation laboratory

**Learning and derivation target:** Assemble a scoped logical operation with preparation, control and verification.

**Implementation and evidence target:** Report fault assumptions, logical error, acceptance and total resource consumption.

## Chapter 33

**From Logical Algorithms to Physical Resource Estimates**

**Reading level:** Advanced synthesis. **Chapter prerequisites:** 14, 18–21, 28–32.

### 33.1 Define an algorithmic workload and success target

**Learning and derivation target:** Specify input/output accuracy, overall failure budget and logical circuit.

**Implementation and evidence target:** Create an auditable workload record rather than a hardware-independent headline.

### 33.2 Logical synthesis and non-Clifford resources

**Learning and derivation target:** Derive a representative rotation-synthesis budget and count T/Clifford operations.

**Implementation and evidence target:** Check counts, synthesis precision and assumptions against a tiny explicit decomposition.

### 33.3 Distributing an error budget

**Learning and derivation target:** Use stated bounds to allocate algorithmic, synthesis and logical errors.

**Implementation and evidence target:** Recompute allocations and identify invalid independence assumptions.

### 33.4 Code distance and logical reliability

**Learning and derivation target:** Relate a named logical-error model to required reliability and distance.

**Implementation and evidence target:** Sweep model parameters and label empirical fits versus proven bounds.

### 33.5 Magic-state factories and scheduling

**Learning and derivation target:** Model production, acceptance, consumption and bottlenecks.

**Implementation and evidence target:** Check a small factory/data schedule and account for idle resources.

### 33.6 Physical qubits, cycles, and runtime

**Learning and derivation target:** Derive a full estimate under declared architecture, timing and connectivity assumptions.

**Implementation and evidence target:** Verify units and compare component sums with a complete ledger.

### 33.7 Sensitivity, uncertainty, and comparison

**Learning and derivation target:** Explain which input assumptions dominate a resource estimate.

**Implementation and evidence target:** Report ranges and alternative assumptions rather than one unsupported number.

### 33.8 Resource-estimation laboratory

**Learning and derivation target:** Connect workload, logical synthesis, correction and physical costs.

**Implementation and evidence target:** Reproduce an estimate from versioned inputs and distinguish projections from device measurements.
