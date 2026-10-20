# Full book plan

**Long-term curriculum revision: October 20, 2026.** Nine parts, 50 chapters and six appendices. This revision adds substantive physical-platform and quantum-compilation routes to the previous 40-chapter plan. The [editorial charter](editorial-charter.md) records the author's aim: a rigorous, accessible modern classic that helps present and future learners enter the field.

This is a curriculum architecture, not a completed manuscript or a claim that every proposed experiment is supported. Three starter chapters currently exist, with intended homes in Chapters **6, 23 and 49**. The three-chapter PDF retains independent sample numbering and its published version.

**Architecture status: review pending, not frozen.** The [curriculum audit](curriculum-audit.md) lists coverage, prerequisite bridges, cross-layer laboratories and open review gates. [Reader continuity](reader-continuity.md) defines the no-skipped-steps standard. Chapter count is not an acceptance criterion.

## Audience, depth and reading levels

Entry readers need basic Python and introductory linear algebra. Foundations supply the quantum model and mathematical bridges; advanced chapters introduce additional probability, optimization, algebra and complexity prerequisites where needed. Readers should be able to reason, derive, implement, verify and critique a new calculation.

**Core** identifies conceptual foundations; **Advanced** adds demanding theory or specialization; **Research** integrates a scoped paper reproduction. A chapter may have a core narrative and advanced proof sections. These labels do not promise that all core chapters fit in one semester. A complete book supports several courses.

The theory determines the curriculum. A missing FlagQuantum API becomes a tracked implementation requirement through the [capability-gap workflow](implementation-roadmap.md). Authors may develop independent executable references while an upstream implementation is pending. Only actually executed, versioned FlagQuantum examples receive validated status.

## Quantum-classical integration

The [hybrid-computing map](hybrid-computing.md) distinguishes eight composable implementation patterns and their host/controller/device boundaries. The early overview is in 14.7; detailed methods remain in their mathematical and systems homes. Hybrid learning is one branch of this broader subject.

## Section architecture and acceptance standard

Each chapter below specifies its section sequence, mathematical outcome and independent check. The [detailed section plan](section-plan.md) expands all 50 chapters into numbered sections with learning/derivation and implementation/evidence targets. These are authoring targets, not claims of existing proofs or code.

1. Open with a concrete question, prerequisites and a prediction.
2. State definitions, physical postulates, access models and assumptions.
3. Give named results with their quantifiers and conditions. Prove central results at the declared level; identify deferred proof ingredients and exact sources.
4. Derive important intermediate steps and connect them to code, including indices, units, dimensions and normalization.
5. Analyze resources and error, including precision and success probability where relevant.
6. Verify small cases independently; include a counterexample or failure diagnosis that tests the assumptions.
7. End with conceptual, derivation/proof, implementation and transfer problems, plus sources and a recap.

Short recall prompts follow the [learning design](learning-design.md); substantial problems develop mathematical and research ability. Numerical agreement supplies evidence about implementation, not a proof of a general theorem. Every specialized chapter needs a reviewed primary-source map before drafting.

## Part 1. Foundations and Quantum Information Primitives

<span id="ch-what-quantum-computing-computes"></span>

### Chapter 1: What Quantum Computing Computes

**Reading level:** Core. **Prerequisites:** Basic Python.

**Numbered section specification:** [Sections 1.1–1.6](section-plans/01-foundations.md#ch-what-quantum-computing-computes).

**Planned sections:** Problems and outputs; interference experiment; models, simulators and hardware; guide to the book.

**Mathematical outcome:** Derive one interference probability before introducing the general formalism.

**Experiment and independent verification:** Predict and verify a tiny circuit; explain why its simulation establishes no speedup.

<span id="ch-complex-vectors-operators-and-numerical-reasoning"></span>

### Chapter 2: Complex Vectors, Operators, and Numerical Reasoning

**Reading level:** Core. **Prerequisites:** 1; introductory linear algebra.

**Numbered section specification:** [Sections 2.1–2.8](section-plans/01-foundations.md#ch-complex-vectors-operators-and-numerical-reasoning).

**Planned sections:** Complex inner products; adjoints and spectra; matrix functions; norms, conditioning and tolerances.

**Mathematical outcome:** Derive spectral reconstruction and matrix-exponential identities under stated assumptions.

**Experiment and independent verification:** Check residuals and conditioning with independent NumPy/PyTorch calculations.

<span id="ch-single-qubit-states-and-rotations"></span>

### Chapter 3: Single-Qubit States and Rotations

**Reading level:** Core. **Prerequisites:** 2.

**Numbered section specification:** [Sections 3.1–3.8](section-plans/01-foundations.md#ch-single-qubit-states-and-rotations).

**Planned sections:** State and evolution postulates; relative and global phase; Bloch sphere; Pauli rotations; no-cloning.

**Mathematical outcome:** Derive rotations from their generators and prove the elementary no-cloning statement.

**Experiment and independent verification:** Compare matrices and circuit results, including phase-equivalent and distinguishable states.

<span id="ch-composite-systems-tensor-products-and-qubit-ordering"></span>

### Chapter 4: Composite Systems, Tensor Products, and Qubit Ordering

**Reading level:** Core. **Prerequisites:** 2, 3.

**Numbered section specification:** [Sections 4.1–4.7](section-plans/01-foundations.md#ch-composite-systems-tensor-products-and-qubit-ordering).

**Planned sections:** Tensor products; register labels and basis indices; local operations; subsystem permutations.

**Mathematical outcome:** Derive the basis-index map and local-operator action on an arbitrary register.

**Experiment and independent verification:** Compare two- and three-qubit operations with Kronecker products and deliberately changed qubit ordering.

<span id="ch-gates-reversible-computation-and-circuit-synthesis"></span>

### Chapter 5: Gates, Reversible Computation, and Circuit Synthesis

**Reading level:** Core. **Prerequisites:** 3, 4.

**Numbered section specification:** [Sections 5.1–5.8](section-plans/01-foundations.md#ch-gates-reversible-computation-and-circuit-synthesis).

**Planned sections:** Gate composition; controlled operations; reversible Boolean computation; universality; approximation and synthesis cost.

**Mathematical outcome:** Derive controlled-gate matrices and a small reversible construction; state the approximation model.

**Experiment and independent verification:** Verify complete unitaries and account for ancillas and inverse operations.

<span id="ch-measurement-expectation-values-and-statistical-estimation"></span>

### Chapter 6: Measurement, Expectation Values, and Statistical Estimation

**Reading level:** Core. **Prerequisites:** 3–5.

**Numbered section specification:** [Sections 6.1–6.9](section-plans/01-foundations.md#ch-measurement-expectation-values-and-statistical-estimation).

**Planned sections:** Born rule; conditional states and instruments; generalized measurements; observables; variance and confidence intervals.

**Mathematical outcome:** Derive projective and generalized-measurement probabilities and finite-shot estimator uncertainty.

**Experiment and independent verification:** Extend the measurement starter; test conditional states and empirical coverage over repeated seeded trials.

<span id="ch-entanglement-and-quantum-information-protocols"></span>

### Chapter 7: Entanglement and Quantum Information Protocols

**Reading level:** Core. **Prerequisites:** 4–6.

**Numbered section specification:** [Sections 7.1–7.8](section-plans/01-foundations.md#ch-entanglement-and-quantum-information-protocols).

**Planned sections:** Schmidt decomposition; Bell correlations; teleportation; superdense coding; no-signalling.

**Mathematical outcome:** Derive Schmidt structure and all conditional branches of teleportation.

**Experiment and independent verification:** Verify corrections for arbitrary input states; inspect the receiver's unconditioned reduced state.

<span id="ch-density-matrices-reduced-states-and-purification"></span>

### Chapter 8: Density Matrices, Reduced States, and Purification

**Reading level:** Core. **Prerequisites:** 2, 4, 6, 7.

**Numbered section specification:** [Sections 8.1–8.8](section-plans/01-foundations.md#ch-density-matrices-reduced-states-and-purification).

**Planned sections:** Ensembles; density operators; partial trace; purification; improper and proper mixtures.

**Mathematical outcome:** Derive mixed-state expectations and the relation between Schmidt coefficients and reduced spectra.

**Experiment and independent verification:** Check trace, positivity and subsystem states against explicit index sums.

## Part 2. Quantum Information: Channels, Inference, and Communication

<span id="ch-quantum-channels-and-their-representations"></span>

### Chapter 9: Quantum Channels and Their Representations

**Reading level:** Core. **Prerequisites:** 8.

**Numbered section specification:** [Sections 9.1–9.8](section-plans/02-information.md#ch-quantum-channels-and-their-representations).

**Planned sections:** Completely positive maps; Kraus representation; Stinespring dilation; Choi representation; channel composition.

**Mathematical outcome:** Establish finite-dimensional representation equivalences and explain why positivity alone is insufficient.

**Experiment and independent verification:** Translate one small channel among representations; test complete positivity, trace preservation and environment dilation.

<span id="ch-distinguishability-fidelity-and-quantum-state-inference"></span>

### Chapter 10: Distinguishability, Fidelity, and Quantum State Inference

**Reading level:** Core. **Prerequisites:** 6, 8, 9.

**Numbered section specification:** [Sections 10.1–10.8](section-plans/02-information.md#ch-distinguishability-fidelity-and-quantum-state-inference).

**Planned sections:** Trace distance; fidelity conventions; operational discrimination; tomography; measurement grouping; classical shadows.

**Mathematical outcome:** Derive binary discrimination and simple estimation bounds; state the assumptions of shadow guarantees.

**Experiment and independent verification:** Compare independently reconstructed states and estimator errors; expose incomplete-measurement counterexamples.

<span id="ch-entropy-relative-entropy-and-information-processing"></span>

### Chapter 11: Entropy, Relative Entropy, and Information Processing

**Reading level:** Core with advanced proofs. **Prerequisites:** 8–10.

**Numbered section specification:** [Sections 11.1–11.8](section-plans/02-information.md#ch-entropy-relative-entropy-and-information-processing).

**Planned sections:** Shannon and von Neumann entropy; relative entropy; mutual information; data processing; strong subadditivity.

**Mathematical outcome:** Prove accessible special cases and selected central results; identify the ingredients and source of deferred general proofs.

**Experiment and independent verification:** Compute small exact and commuting examples and counterexamples to invalid entropy intuitions.

<span id="ch-compression-entanglement-and-communication-limits"></span>

### Chapter 12: Compression, Entanglement, and Communication Limits

**Reading level:** Advanced. **Prerequisites:** 7–11.

**Numbered section specification:** [Sections 12.1–12.8](section-plans/02-information.md#ch-compression-entanglement-and-communication-limits).

**Planned sections:** Typicality; Schumacher compression; entanglement concentration; Holevo bound; channel-capacity formulations.

**Mathematical outcome:** Derive a finite-block compression example and state coding theorems with their operational assumptions.

**Experiment and independent verification:** Compare small block encodings and success/error tradeoffs; distinguish finite demonstrations from asymptotic proofs.

<span id="ch-quantum-cryptography-and-security-reasoning"></span>

### Chapter 13: Quantum Cryptography and Security Reasoning

**Reading level:** Advanced. **Prerequisites:** 6–12.

**Numbered section specification:** [Sections 13.1–13.8](section-plans/02-information.md#ch-quantum-cryptography-and-security-reasoning).

**Planned sections:** BB84; parameter estimation; adversarial models; privacy amplification; finite-size and composable security.

**Mathematical outcome:** Derive an intercept-resend example and the logic of a scoped security argument; delimit the full security theorem.

**Experiment and independent verification:** Run a toy protocol with confidence bounds; explain why a low observed error rate alone does not establish security.

## Part 3. Quantum Algorithms and Computational Resources

<span id="ch-computational-models-complexity-and-quantum-advantage"></span>

### Chapter 14: Computational Models, Complexity, and Quantum Advantage

**Reading level:** Core. **Prerequisites:** 4–6.

**Numbered section specification:** [Sections 14.1–14.9](section-plans/03-algorithms.md#ch-computational-models-complexity-and-quantum-advantage).

**Planned sections:** Circuit families; reversible models; BQP and promise problems; query versus gate cost; precision; classical baselines. Includes an early map of quantum-classical interaction patterns.

**Mathematical outcome:** Relate input/output access assumptions to a complete resource expression.

**Experiment and independent verification:** Audit examples including state preparation, oracle synthesis, repetitions and readout; avoid simulator-time speedup claims.

<span id="ch-interference-oracles-and-phase-kickback"></span>

### Chapter 15: Interference, Oracles, and Phase Kickback

**Reading level:** Core. **Prerequisites:** 5, 14.

**Numbered section specification:** [Sections 15.1–15.7](section-plans/03-algorithms.md#ch-interference-oracles-and-phase-kickback).

**Planned sections:** Reversible oracles; phase kickback; Deutsch-Jozsa; Bernstein-Vazirani; oracle promises.

**Mathematical outcome:** Derive the phase-oracle action and complete output distributions.

**Experiment and independent verification:** Check truth tables and gate-level oracles against dense permutation and diagonal references.

<span id="ch-grover-search-amplitude-amplification-and-estimation"></span>

### Chapter 16: Grover Search, Amplitude Amplification, and Estimation

**Reading level:** Core with advanced extensions. **Prerequisites:** 6, 14, 15; revisit after 17.

**Numbered section specification:** [Sections 16.1–16.8](section-plans/03-algorithms.md#ch-grover-search-amplitude-amplification-and-estimation).

**Planned sections:** Two-dimensional geometry; iteration counts; general amplification; amplitude estimation; query bounds.

**Mathematical outcome:** Derive the success curve and a scoped estimation error/query relation.

**Experiment and independent verification:** Compare complete distributions with analytic predictions and ordinary Monte Carlo under the same access assumptions.

<span id="ch-fourier-transforms-and-quantum-phase-estimation"></span>

### Chapter 17: Fourier Transforms and Quantum Phase Estimation

**Reading level:** Core. **Prerequisites:** 4–6, 14, 15.

**Numbered section specification:** [Sections 17.1–17.8](section-plans/03-algorithms.md#ch-fourier-transforms-and-quantum-phase-estimation).

**Planned sections:** Discrete Fourier transform; QFT factorization; inverse and approximate QFT; exact/off-grid phase estimation.

**Mathematical outcome:** Derive QFT structure and finite-precision phase-estimation probabilities.

**Experiment and independent verification:** Compare every small basis input and off-grid output distribution with dense references.

<span id="ch-period-finding-factoring-and-algorithmic-arithmetic"></span>

### Chapter 18: Period Finding, Factoring, and Algorithmic Arithmetic

**Reading level:** Advanced. **Prerequisites:** 5, 14, 17.

**Numbered section specification:** [Sections 18.1–18.8](section-plans/03-algorithms.md#ch-period-finding-factoring-and-algorithmic-arithmetic).

**Planned sections:** Order finding; modular arithmetic; continued fractions; success probabilities; arithmetic and synthesis costs.

**Mathematical outcome:** Derive the reduction from factoring to order finding and its classical postprocessing conditions.

**Experiment and independent verification:** Factor tiny examples using explicit modular arithmetic; avoid precompiled circuits that assume the answer.

<span id="ch-hamiltonian-simulation-and-error-bounds"></span>

### Chapter 19: Hamiltonian Simulation and Error Bounds

**Reading level:** Core with advanced extensions. **Prerequisites:** 2, 5, 14, 17.

**Numbered section specification:** [Sections 19.1–19.9](section-plans/03-algorithms.md#ch-hamiltonian-simulation-and-error-bounds).

**Planned sections:** Pauli decompositions; first/second-order formulas; commutator error; sparse and oracle models; precision dependence. Includes an explicit adiabatic-computation and spectral-gap bridge.

**Mathematical outcome:** Derive product formulas and a finite-system error bound; prepare the transition to signal processing.

**Experiment and independent verification:** Compare with matrix exponentials and verify error scaling against an actual bound.

<span id="ch-block-encodings-and-quantum-linear-algebra"></span>

### Chapter 20: Block Encodings and Quantum Linear Algebra

**Reading level:** Advanced. **Prerequisites:** 2, 5, 14, 17, 19.

**Numbered section specification:** [Sections 20.1–20.8](section-plans/03-algorithms.md#ch-block-encodings-and-quantum-linear-algebra).

**Planned sections:** Normalization and access models; exact small block encodings; LCU; postselection; linear-system conditioning.

**Mathematical outcome:** Construct a block encoding and derive normalization, success probability and condition-number dependence.

**Experiment and independent verification:** Check encoded blocks numerically and include state preparation/readout in the resource analysis.

<span id="ch-quantum-signal-processing-and-singular-value-transformation"></span>

### Chapter 21: Quantum Signal Processing and Singular Value Transformation

**Reading level:** Advanced. **Prerequisites:** 16, 19, 20.

**Numbered section specification:** [Sections 21.1–21.9](section-plans/03-algorithms.md#ch-quantum-signal-processing-and-singular-value-transformation).

**Planned sections:** SU(2) polynomial sequences; parity and boundedness; phase sequences; QSVT; spectral filtering and simulation.

**Mathematical outcome:** Derive low-degree constructions, state a precise transformation theorem and prove a selected application.

**Experiment and independent verification:** Compare transformed scalar values and small matrix singular values with polynomial targets; report synthesis and approximation errors.

<span id="ch-quantum-walks-lower-bounds-and-algorithm-design"></span>

### Chapter 22: Quantum Walks, Lower Bounds, and Algorithm Design

**Reading level:** Advanced. **Prerequisites:** 14–21.

**Numbered section specification:** [Sections 22.1–22.8](section-plans/03-algorithms.md#ch-quantum-walks-lower-bounds-and-algorithm-design).

**Planned sections:** Walk constructions; search and hitting problems; polynomial method; query lower bounds; algorithm selection.

**Mathematical outcome:** Analyze a small walk and derive a representative lower bound under an explicit oracle model.

**Experiment and independent verification:** Compare walk evolution with an independent transition/spectral construction and identify inaccessible speedup assumptions.

## Part 4. Variational and Differentiable Quantum Computing

<span id="ch-parameterized-circuits-quantum-gradients-and-differentiation"></span>

### Chapter 23: Parameterized Circuits, Quantum Gradients, and Differentiation

**Reading level:** Core. **Prerequisites:** 2–6; elementary calculus.

**Numbered section specification:** [Sections 23.1–23.10](section-plans/04-variational.md#ch-parameterized-circuits-quantum-gradients-and-differentiation).

**Planned sections:** Observable-valued models; generator spectra; parameter shift; shared parameters; adjoint differentiation; autograd contracts.

**Mathematical outcome:** Derive spectral shift rules, normalization changes and parameter-reuse chain rules; analyze execution and memory costs.

**Experiment and independent verification:** Expand the gradient starter with analytic, dense, shifted and autograd checks for multiple parameter occurrences.

<span id="ch-optimization-geometry-and-trainability"></span>

### Chapter 24: Optimization, Geometry, and Trainability

**Reading level:** Advanced. **Prerequisites:** 10, 14, 23.

**Numbered section specification:** [Sections 24.1–24.9](section-plans/04-variational.md#ch-optimization-geometry-and-trainability).

**Planned sections:** Exact and stochastic losses; optimizer diagnostics; quantum geometric tensor; natural gradient; barren plateaus; noise.

**Mathematical outcome:** Derive a small metric and gradient-variance example; state the ensemble assumptions of trainability results.

**Experiment and independent verification:** Separate convergence, expressivity and sampling effects; compare initializations and controlled classical baselines.

<span id="ch-variational-simulation-chemistry-and-ground-state-problems"></span>

### Chapter 25: Variational Simulation, Chemistry, and Ground-State Problems

**Reading level:** Core application. **Prerequisites:** 8, 14, 19, 23–24.

**Numbered section specification:** [Sections 25.1–25.12](section-plans/04-variational.md#ch-variational-simulation-chemistry-and-ground-state-problems).

**Planned sections:** Variational principle; fermions and Jordan-Wigner mapping; symmetries; ansatz selection; measurement allocation; dynamics. Adds quantum embedding/self-consistency and quantum-sampled classical subspace solving.

**Mathematical outcome:** Prove the energy bound and derive a small occupation-to-qubit Hamiltonian with units and offsets.

**Experiment and independent verification:** Compare independent fermionic/qubit matrices and exact diagonalization; report all model and estimator errors.

<span id="ch-qaoa-quantum-optimization-and-classical-comparisons"></span>

### Chapter 26: QAOA, Quantum Optimization, and Classical Comparisons

**Reading level:** Advanced application. **Prerequisites:** 14–16, 23, 24.

**Numbered section specification:** [Sections 26.1–26.8](section-plans/04-variational.md#ch-qaoa-quantum-optimization-and-classical-comparisons).

**Planned sections:** Objective-to-Hamiltonian mapping; mixers; constrained spaces; depth; approximation quality; sampling and optimization cost.

**Mathematical outcome:** Derive MaxCut and one low-depth result under explicit graph and sign conventions.

**Experiment and independent verification:** Compare against exhaustive solutions and meaningful classical heuristics without inferring advantage from tiny instances.

<span id="ch-quantum-learning-kernels-and-hybrid-models"></span>

### Chapter 27: Quantum Learning, Kernels, and Hybrid Models

**Reading level:** Advanced application. **Prerequisites:** 10, 14, 23, 24; basic machine learning.

**Numbered section specification:** [Sections 27.1–27.8](section-plans/04-variational.md#ch-quantum-learning-kernels-and-hybrid-models).

**Planned sections:** Data access and encoding; hybrid chain rule; quantum kernels; generalization; classical simulability and baselines.

**Mathematical outcome:** Derive kernel/feature-map relations and joint gradients; state learning-task and data-access assumptions.

**Experiment and independent verification:** Use held-out evaluation, classical baselines and end-to-end gradient checks; include encoding and measurement costs.

## Part 5. Noise, Error Correction, and Fault-Tolerant Computation

<span id="ch-noise-open-systems-and-error-mitigation"></span>

### Chapter 28: Noise, Open Systems, and Error Mitigation

**Reading level:** Core. **Prerequisites:** 8–10; 19 for dynamics.

**Numbered section specification:** [Sections 28.1–28.9](section-plans/05-fault-tolerance.md#ch-noise-open-systems-and-error-mitigation).

**Planned sections:** Kraus noise; Lindblad dynamics; trajectories; correlated noise; calibration; mitigation and its overhead.

**Mathematical outcome:** Derive amplitude damping and one master equation; analyze the bias/variance tradeoff of a mitigation example.

**Experiment and independent verification:** Compare density evolution with an independent solver and trajectory averages; test positivity, trace and estimator uncertainty.

<span id="ch-quantum-error-correction-conditions-and-recovery"></span>

### Chapter 29: Quantum Error Correction: Conditions and Recovery

**Reading level:** Core. **Prerequisites:** 7–10, 28.

**Numbered section specification:** [Sections 29.1–29.9](section-plans/05-fault-tolerance.md#ch-quantum-error-correction-conditions-and-recovery).

**Planned sections:** Quantum obstacles; repetition codes; error discretization; Knill-Laflamme conditions; recovery and logical information.

**Mathematical outcome:** Prove the correction condition in a finite example and explain preservation of logical information by syndrome measurement.

**Experiment and independent verification:** Enumerate errors and verify recovery on arbitrary encoded superpositions, including coherent error combinations.

<span id="ch-stabilizer-codes-logical-operators-and-decoding"></span>

### Chapter 30: Stabilizer Codes, Logical Operators, and Decoding

**Reading level:** Core with advanced extensions. **Prerequisites:** 5–8, 29; binary linear algebra.

**Numbered section specification:** [Sections 30.1–30.10](section-plans/05-fault-tolerance.md#ch-stabilizer-codes-logical-operators-and-decoding).

**Planned sections:** Pauli symplectic representation; stabilizer groups; CSS construction; distance; logical operators; decoder interfaces. Includes graph states, adaptive measurement-based gates and their teleportation bridge.

**Mathematical outcome:** Derive a code's syndrome map, logical operators and distance; connect binary algebra to quantum operators.

**Experiment and independent verification:** Compare stabilizer calculations with dense small-code references and injected-error enumeration.

<span id="ch-surface-codes-and-repeated-syndrome-measurements"></span>

### Chapter 31: Surface Codes and Repeated Syndrome Measurements

**Reading level:** Advanced. **Prerequisites:** 28–30.

**Numbered section specification:** [Sections 31.1–31.8](section-plans/05-fault-tolerance.md#ch-surface-codes-and-repeated-syndrome-measurements).

**Planned sections:** Lattice checks; boundaries; syndrome circuits; measurement faults; detection events; space-time decoding; logical failure.

**Mathematical outcome:** Derive checks and detection-event patterns for a small patch and repeated rounds.

**Experiment and independent verification:** Verify hand-enumerated faults before Monte Carlo; report noise model, decoder, distance, uncertainty and finite-size limits.

<span id="ch-fault-tolerant-gates-and-universal-logical-computation"></span>

### Chapter 32: Fault-Tolerant Gates and Universal Logical Computation

**Reading level:** Advanced. **Prerequisites:** 5, 18, 28–31.

**Numbered section specification:** [Sections 32.1–32.8](section-plans/05-fault-tolerance.md#ch-fault-tolerant-gates-and-universal-logical-computation).

**Planned sections:** Fault propagation; transversal operations; threshold logic; lattice surgery; code deformation; magic states and distillation.

**Mathematical outcome:** Derive a fault-propagation example and a small distillation/rejection calculation; state threshold assumptions and explain proof structure.

**Experiment and independent verification:** Compare ideal logical actions with fault-injected circuits and count accepted outputs, logical errors and consumed resources.

<span id="ch-from-logical-algorithms-to-physical-resource-estimates"></span>

### Chapter 33: From Logical Algorithms to Physical Resource Estimates

**Reading level:** Advanced synthesis. **Prerequisites:** 14, 18–21, 28–32.

**Numbered section specification:** [Sections 33.1–33.8](section-plans/05-fault-tolerance.md#ch-from-logical-algorithms-to-physical-resource-estimates).

**Planned sections:** Logical gate synthesis; T count/depth; factories; error budgets; code distance; physical qubits; runtime and sensitivity.

**Mathematical outcome:** Derive a complete small cost model with a target success probability and explicit architecture/noise assumptions.

**Experiment and independent verification:** Recompute resource estimates under changing assumptions; separate symbolic estimates from measured device performance.

## Part 6. Physical Realizations and Quantum-System Architecture

<span id="ch-from-abstract-qubits-to-physical-quantum-systems"></span>

### Chapter 34: From Abstract Qubits to Physical Quantum Systems

**Reading level:** Core bridge with optional physics extensions. **Prerequisites:** 2–6, 8–10, 19, 28; selected 29–33 for logical resources.

**Numbered section specification:** [Sections 34.1–34.9](section-plans/physical-platforms.md#ch-from-abstract-qubits-to-physical-quantum-systems).

**Planned sections:** Levels, modes, and computational subspaces; Oscillator and light-matter mathematics bridge; Driven systems, rotating frames, and resonance; Preparation, control, and readout as an experiment; Digital, analog, and measurement-based models; Noise, leakage, loss, and hardware constraints; Connectivity, transport, and modular architectures; A fair platform-comparison framework; Choose a platform learning branch.

**Mathematical outcome:** Develop the explicit physical/program model and its stated approximations through the section-level derivations.

**Experiment and independent verification:** Produce a complete small independent reference, an implementation contract and an assumption/error/resource record before claiming framework support.

<span id="ch-superconducting-qubits-and-circuit-qed-control"></span>

### Chapter 35: Superconducting Qubits and Circuit-QED Control

**Reading level:** Advanced platform branch. **Prerequisites:** 2–6, 9, 19, 28, 34.

**Numbered section specification:** [Sections 35.1–35.8](section-plans/physical-platforms.md#ch-superconducting-qubits-and-circuit-qed-control).

**Planned sections:** An electrical circuit becomes a quantum model; Anharmonicity and the transmon computational subspace; Microwave control and single-qubit rotations; Coupling and native two-qubit interactions; Dispersive readout and assignment errors; Decoherence, crosstalk, and calibration; Target constraints for compilation; Superconducting-model laboratory.

**Mathematical outcome:** Develop the explicit physical/program model and its stated approximations through the section-level derivations.

**Experiment and independent verification:** Produce a complete small independent reference, an implementation contract and an assumption/error/resource record before claiming framework support.

<span id="ch-trapped-ion-qubits-motional-gates-and-transport"></span>

### Chapter 36: Trapped-Ion Qubits, Motional Gates, and Transport

**Reading level:** Advanced platform branch. **Prerequisites:** 2–6, 9, 19, 28, 34.

**Numbered section specification:** [Sections 36.1–36.8](section-plans/physical-platforms.md#ch-trapped-ion-qubits-motional-gates-and-transport).

**Planned sections:** Internal states, trapping, and preparation; Collective motion and sidebands; Carrier drives and single-qubit control; Motional entangling gates; Readout, heating, and coherence; Chains, QCCD transport, and photonic links; Target constraints for compilation; Trapped-ion laboratory.

**Mathematical outcome:** Develop the explicit physical/program model and its stated approximations through the section-level derivations.

**Experiment and independent verification:** Produce a complete small independent reference, an implementation contract and an assumption/error/resource record before claiming framework support.

<span id="ch-neutral-atom-arrays-and-rydberg-quantum-computing"></span>

### Chapter 37: Neutral-Atom Arrays and Rydberg Quantum Computing

**Reading level:** Advanced platform branch. **Prerequisites:** 2–6, 9, 19, 28, 34.

**Numbered section specification:** [Sections 37.1–37.8](section-plans/physical-platforms.md#ch-neutral-atom-arrays-and-rydberg-quantum-computing).

**Planned sections:** Trapping, internal encodings, and rearrangement; Rydberg interactions and blockade; Single-qubit and entangling control; Analog Hamiltonian programming; Transport, parallelism, and compilation; Atom loss, readout, and imperfect interactions; Digital versus analog experiment contracts; Neutral-atom laboratory.

**Mathematical outcome:** Develop the explicit physical/program model and its stated approximations through the section-level derivations.

**Experiment and independent verification:** Produce a complete small independent reference, an implementation contract and an assumption/error/resource record before claiming framework support.

<span id="ch-photonic-encodings-optical-circuits-and-measurement-based-computation"></span>

### Chapter 38: Photonic Encodings, Optical Circuits, and Measurement-Based Computation

**Reading level:** Advanced platform branch. **Prerequisites:** 2–10, 28, 30, 34.

**Numbered section specification:** [Sections 38.1–38.9](section-plans/physical-platforms.md#ch-photonic-encodings-optical-circuits-and-measurement-based-computation).

**Planned sections:** Optical modes and qubit encodings; Beam splitters, phases, and interferometers; Interference, sources, and detection; Measurement-induced operations and heralding; Graph states, fusion, and logical computation; Continuous-variable and bosonic branches [Advanced]; Loss, erasure, and multiplexing resources; Photonic compilation and architecture contracts; Photonic laboratory.

**Mathematical outcome:** Develop the explicit physical/program model and its stated approximations through the section-level derivations.

**Experiment and independent verification:** Produce a complete small independent reference, an implementation contract and an assumption/error/resource record before claiming framework support.

<span id="ch-semiconductor-spin-qubits-and-exchange-based-architectures"></span>

### Chapter 39: Semiconductor Spin Qubits and Exchange-Based Architectures

**Reading level:** Advanced platform branch. **Prerequisites:** 2–6, 9, 19, 28, 34.

**Numbered section specification:** [Sections 39.1–39.8](section-plans/physical-platforms.md#ch-semiconductor-spin-qubits-and-exchange-based-architectures).

**Planned sections:** Spin encodings and confined-charge models; Zeeman control and electrically driven rotations; Exchange and entangling operations; Charge, valley, and leakage degrees of freedom; Initialization and spin-to-charge readout; Noise, variability, and calibration; Coupling, shuttling, and modular constraints; Spin-qubit laboratory.

**Mathematical outcome:** Develop the explicit physical/program model and its stated approximations through the section-level derivations.

**Experiment and independent verification:** Produce a complete small independent reference, an implementation contract and an assumption/error/resource record before claiming framework support.

<span id="ch-topological-quantum-computation-and-candidate-physical-realizations"></span>

### Chapter 40: Topological Quantum Computation and Candidate Physical Realizations

**Reading level:** Advanced platform branch. **Prerequisites:** 7–9, 25, 28–32, 34.

**Numbered section specification:** [Sections 40.1–40.8](section-plans/physical-platforms.md#ch-topological-quantum-computation-and-candidate-physical-realizations).

**Planned sections:** Topology, protection, and distinct meanings; Fusion spaces and encoded information; Braiding as a logical transformation; Measurement, corrections, and computational power; Majorana models and parity encoding [Advanced]; Protection assumptions and failure mechanisms; Experiments, signatures, and unresolved evidence; Topological compilation and laboratory.

**Mathematical outcome:** Develop the explicit physical/program model and its stated approximations through the section-level derivations.

**Experiment and independent verification:** Produce a complete small independent reference, an implementation contract and an assumption/error/resource record before claiming framework support.

## Part 7. Quantum Programming, Compilation, and Control

<span id="ch-quantum-programs-intermediate-representations-and-verified-optimization"></span>

### Chapter 41: Quantum Programs, Intermediate Representations, and Verified Optimization

**Reading level:** Core systems route with advanced extensions. **Prerequisites:** 4–6, 9, 14, 34; one chosen platform branch as needed.

**Numbered section specification:** [Sections 41.1–41.9](section-plans/quantum-compilation.md#ch-quantum-programs-intermediate-representations-and-verified-optimization).

**Planned sections:** What a quantum compiler must preserve; Programs, types, and quantum-classical control; Circuit DAGs and intermediate representations; Lowering and reversible computation; Local rewrites, commutation, and optimization; Phase, parameters, and controlled contexts; Channels, measurements, and dynamic programs; Interchange, export, and capability boundaries; A minimal verified compiler laboratory.

**Mathematical outcome:** Develop the explicit physical/program model and its stated approximations through the section-level derivations.

**Experiment and independent verification:** Produce a complete small independent reference, an implementation contract and an assumption/error/resource record before claiming framework support.

<span id="ch-gate-synthesis-qubit-mapping-routing-and-scheduling"></span>

### Chapter 42: Gate Synthesis, Qubit Mapping, Routing, and Scheduling

**Reading level:** Core systems route with advanced extensions. **Prerequisites:** 5, 14, 34, 41; selected 35–40 for the chosen target.

**Numbered section specification:** [Sections 42.1–42.10](section-plans/quantum-compilation.md#ch-gate-synthesis-qubit-mapping-routing-and-scheduling).

**Planned sections:** Target models and native-operation contracts; Single-qubit synthesis; Two-qubit and multi-qubit synthesis; Approximate synthesis and logical gate sets [Advanced]; Initial logical-to-physical placement; Routing and changing qubit mappings; Routing search and heuristic limits; Scheduling with timing and shared resources; Joint objectives and error-aware compilation; Mapping-and-scheduling laboratory.

**Mathematical outcome:** Develop the explicit physical/program model and its stated approximations through the section-level derivations.

**Experiment and independent verification:** Produce a complete small independent reference, an implementation contract and an assumption/error/resource record before claiming framework support.

<span id="ch-control-level-lowering-dynamic-execution-and-logical-compilation"></span>

### Chapter 43: Control-Level Lowering, Dynamic Execution, and Logical Compilation

**Reading level:** Advanced systems route. **Prerequisites:** 19, 23, 28, 32–34, 41–42; one relevant platform branch.

**Numbered section specification:** [Sections 43.1–43.10](section-plans/quantum-compilation.md#ch-control-level-lowering-dynamic-execution-and-logical-compilation).

**Planned sections:** From native gates to control Hamiltonians; Pulse shaping and constrained optimization; Frames, virtual operations, and calibration; Crosstalk, leakage, and robust control; Dynamic circuits and feed-forward latency; Lowering analog and measurement-based programs; Fault-tolerant logical compilation; Cross-layer verification and approximate equivalence; Hardware-aware compilation laboratory. Includes local feedback and heterogeneous host/device runtime orchestration.

**Mathematical outcome:** Develop the explicit physical/program model and its stated approximations through the section-level derivations.

**Experiment and independent verification:** Produce a complete small independent reference, an implementation contract and an assumption/error/resource record before claiming framework support.

## Part 8. Classical Simulation and the Boundary of Tractability

<span id="ch-exact-simulation-tensor-execution-and-numerical-reliability"></span>
<span id="chapter-34-exact-simulation-tensor-execution-and-numerical-reliability"></span>

### Chapter 44: Exact Simulation, Tensor Execution, and Numerical Reliability

**Reading level:** Core. **Prerequisites:** 2, 4–6, 8, 14, 23.

**Numbered section specification:** [Sections 44.1–44.8](section-plans/06-simulation.md#ch-exact-simulation-tensor-execution-and-numerical-reliability).

**Planned sections:** Statevector and density evolution; tensor-axis operations; precision; memory; batching; differentiation; parallel execution.

**Mathematical outcome:** Derive local-gate tensor contractions and storage/time costs, including communication assumptions.

**Experiment and independent verification:** Build an independent minimal executor; compare states, channels and gradients before benchmarking.

<span id="ch-stabilizer-simulation-magic-and-classical-simulability"></span>
<span id="chapter-35-stabilizer-simulation-magic-and-classical-simulability"></span>

### Chapter 45: Stabilizer Simulation, Magic, and Classical Simulability

**Reading level:** Advanced. **Prerequisites:** 14, 30, 44.

**Numbered section specification:** [Sections 45.1–45.8](section-plans/06-simulation.md#ch-stabilizer-simulation-magic-and-classical-simulability).

**Planned sections:** Tableau updates; Clifford circuits; adaptive measurements; Gottesman-Knill; non-Clifford resources.

**Mathematical outcome:** Derive tableau updates and explain the assumptions behind efficient stabilizer simulation.

**Experiment and independent verification:** Compare tableau and dense results, including measurement branches; trace the resource impact of non-Clifford operations.

<span id="ch-matrix-product-states-entanglement-and-truncation"></span>
<span id="chapter-36-matrix-product-states-entanglement-and-truncation"></span>

### Chapter 46: Matrix Product States, Entanglement, and Truncation

**Reading level:** Advanced. **Prerequisites:** 2, 4, 7, 8, 10, 44.

**Numbered section specification:** [Sections 46.1–46.8](section-plans/06-simulation.md#ch-matrix-product-states-entanglement-and-truncation).

**Planned sections:** Successive SVD; canonical forms; gate updates; bond dimensions; entanglement; truncation bounds.

**Mathematical outcome:** Derive MPS construction and discarded-weight error relations with normalization assumptions.

**Experiment and independent verification:** Compare with exact states while varying bonds and gate geometry; report accumulated error and cost.

<span id="ch-tensor-networks-contraction-and-hybrid-simulation-strategies"></span>
<span id="chapter-37-tensor-networks-contraction-and-hybrid-simulation-strategies"></span>

### Chapter 47: Tensor Networks, Contraction, and Hybrid Simulation Strategies

**Reading level:** Advanced. **Prerequisites:** 6, 9, 14, 44, 46.

**Numbered section specification:** [Sections 47.1–47.10](section-plans/06-simulation.md#ch-tensor-networks-contraction-and-hybrid-simulation-strategies).

**Planned sections:** Circuit tensors; contraction paths; intermediate sizes; slicing; distributed contraction; amplitudes versus full states. Includes quantum-executed fragments, classical circuit-cut reconstruction and sampling overhead.

**Mathematical outcome:** Derive a circuit contraction and predict path-dependent intermediate memory.

**Experiment and independent verification:** Check independent contractions, profile declared workloads and explain when simulation becomes intractable.

## Part 9. From Papers to Reproducible Research

<span id="ch-reading-papers-building-evidence-and-reproducing-results"></span>
<span id="chapter-38-reading-papers-building-evidence-and-reproducing-results"></span>

### Chapter 48: Reading Papers, Building Evidence, and Reproducing Results

**Reading level:** Core research method. **Prerequisites:** 4, 6, 10, 14; application-specific prerequisites.

**Numbered section specification:** [Sections 48.1–48.9](section-plans/07-research.md#ch-reading-papers-building-evidence-and-reproducing-results).

**Planned sections:** Source revisions; symbols and assumptions; equation dependencies; units; independent references; uncertainty; resource records.

**Mathematical outcome:** Turn a source claim into a mathematical specification and distinguish proof, numerical evidence and empirical inference.

**Experiment and independent verification:** Build a versioned reproduction worksheet, environment record and discrepancy analysis before optimizing.

<span id="ch-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe"></span>
<span id="chapter-39-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe"></span>

### Chapter 49: Case Study: Molecular Hydrogen from Hamiltonian to Verified VQE

**Reading level:** Research capstone. **Prerequisites:** 23–25, 48.

**Numbered section specification:** [Sections 49.1–49.9](section-plans/07-research.md#ch-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe).

**Planned sections:** Corrected paper data; reduction and qubit mapping; ansatz; closed-form minimum; full curve; optimization; shot uncertainty.

**Mathematical outcome:** Derive the model and parameter conventions, amplitudes, observables, gradients and sector minimum.

**Experiment and independent verification:** Expand the H2 starter across 54 geometries with independent matrices, grid-error bounds, optimizers, sampling and provenance.

<span id="ch-case-study-logical-memory-and-error-correction-experiments"></span>
<span id="chapter-40-case-study-logical-memory-and-error-correction-experiments"></span>

### Chapter 50: Case Study: Logical Memory and Error-Correction Experiments

**Reading level:** Research capstone. **Prerequisites:** 28–33, 45, 48.

**Numbered section specification:** [Sections 50.1–50.9](section-plans/07-research.md#ch-case-study-logical-memory-and-error-correction-experiments).

**Planned sections:** Paper selection and claim specification; repeated syndrome model; decoder; logical observable; scaling; failure analysis.

**Mathematical outcome:** Derive the selected code/model's detection and logical-failure definitions before reproducing a claim.

**Experiment and independent verification:** Select and document a primary source before implementation; compare tiny exact references and stochastic results with uncertainty. No hardware reproduction is implied.

## Appendices and companion laboratories

- **A. Mathematical and Physical Bridges:** probability, asymptotics, selected algebra, oscillator mathematics, elementary circuit/atomic/optical models and selected proofs. Required local bridges also appear before their first use in the main text.
- **B. Matrix Calculus and Differentiation Conventions:** complex derivatives, adjoints and PyTorch contracts.
- **C. FlagQuantum Runtime Contracts and Interoperability:** versioned APIs, compiler interfaces and serialization. Compilation theory and algorithms belong in Chapters 41–43.
- **D. Experiment Records and Benchmark Protocols:** manifests, uncertainty, comparison workloads and reproducibility.
- **E. Platform Access Laboratories:** installation, accelerators, distributed execution and provider access. Physical encodings, control and device constraints belong in Chapters 34–40.
- **F. Problems, Selected Solutions and Reproduction Worksheets:** stable problem identifiers and reader/teacher support.

The bibliography, symbol index, glossary, errata and acknowledgements are separate back matter. Hardware credentials are optional. Essential explanations, proof steps and answers remain usable offline.

## Dependencies and course routes

The numbered order is one reference-book arrangement. It is not a requirement to read all 50 chapters consecutively. The common core and explicit branch routes give the learner a continuous path without requiring every specialization.

| Route | Sequence and bridges | Intended outcome |
|---|---|---|
| Opening core | 1–8, with local mathematics bridges; selected 9–10 and 14 | State, gate, measurement, information and resource reasoning |
| First algorithms | 14–15, 16.1–16.5, 17, then 16.6–16.8 and selected 18–19 | Complete search, estimation and Fourier-based explanations without a hidden forward prerequisite |
| Information course | 7–13, after the necessary foundations | Channels, inference, entropy, communication and security assumptions |
| Modern algorithms | 14–22, supported by 2–6 and 9–10 | Algorithm derivations, access models, error and complete resource cost |
| Quantum-classical integration | 14.7 overview, then the selected patterns in 10, 23–27, 43 and 47; use the [hybrid map](hybrid-computing.md) | Recognize typed data/control flows, algorithmic versus runtime coupling, and end-to-end costs |
| Differentiable applications | 23–27, with 10, 14 and selected 19/28 | Gradients, trainability, variational/learning objectives and baselines |
| Error correction | 28–33, after 7–10; graph-state material in 30 links back to teleportation | From noise and correction conditions to logical operations and resource models |
| Hardware-to-compiler course | 34, one of 35–40, then 41–42; 43 after 19, 23, 28 and 32–33 | Model and control a selected physical platform, compile a task and validate the whole contract |
| Platform comparison | 34 and guided comparison sections from 35–40 | Compare encodings, constraints and evidence without taking every advanced branch |
| Classical simulation | 30, 44–47, with 2, 4, 7–10, 14 and 23 | Exact/structured simulation, approximation and tractability |
| Research | 48, then 49 or 50 after its application prerequisites | A scoped, independently checked paper reproduction |

A 14-week course selects sections from a route. The full curriculum is a reference and multi-course project. Page budgets, core/advanced allocation and possible multi-volume publication must be assessed at the architecture-review gate; they are not fixed by chapter count.

Chapter 7 first derives no-signalling from marginal probabilities and revisits the reduced-state proof after Chapter 8. Chapter 19 supplies a scoped adiabatic-model bridge; Chapter 30 introduces graph states and measurement-based gates before photonic computation. Chapter 33 introduces physical resource parameters as explicit abstract assumptions; Chapters 34–40 explain their platform-specific origins and limits.

## Ownership of recurring concepts

| Concept | First development | Later use without duplicate derivation |
|---|---|---|
| Gate identities and simple universality | 5 | Compiler correctness and synthesis in 41–42 |
| Channels and conditional operations | 6, 8–9 | Noise (28), hardware readout and dynamic compilation |
| Entanglement and teleportation | 7–8 | Coding, graph-state computation, photonics and topology |
| Time evolution and approximation | 19 | Hardware effective models and control-level lowering |
| Gradients and optimization | 23–24 | Variational applications and pulse optimization in 43 |
| Stabilizers and logical computation | 29–32 | Photonic/topological branches, logical compilation and simulation |
| Resource/error budgets | 14, 19, 28, 33 | Hardware comparison, compiler objectives and research reports |
| Hybrid interaction and execution boundary | 14.7; task-specific mathematics in 10, 23–27 | Controller/runtime contracts in 41–43 and fragment reconstruction in 47 |
| Physical experiment/target contract | 34 and one selected platform | Mapping, scheduling and control in 41–43 |
| Independent execution/reference methods | Small local references throughout; general methods in 44–47 | Full research capstones in 49–50 |

## Planning review before substantial drafting

The [curriculum audit](curriculum-audit.md) records the remaining gates. The expanded architecture is **not frozen** and has not yet received specialist or learner approval.

1. Review coverage and chapter ownership, including compilation, physical platforms, alternative computational models and the interfaces between them.
2. Audit first use of concepts, prerequisite bridges, section transitions and explicit learning outcomes using the [reader-continuity standard](reader-continuity.md).
3. Check depth and workload with algorithm, information, compilation, hardware and error-correction specialists; record the actual scope reviewed.
4. Test the opening core and representative cross-layer routes with target readers. Record where a reader cannot reconstruct a step.
5. Resolve missing bridges, overload and redundant material; assign provisional page/problem budgets and freeze a versioned architecture baseline.
6. Begin sustained chapter drafting against that baseline. Use stable chapter/section IDs and a public change record for later revisions.

Small existing pilots supply evidence for this review. They do not establish that the full architecture, every proof or every experiment has been validated.

## Writing priorities after the review gate

Complete the opening sequence (1–8), then depth pilots in measurement (6), differentiation (23), correction (29), and a hardware-to-compiler thread (34, selected 35–40, 41–42). Expand channels/inference, resources and the first algorithm path. Develop the VQE research route through 48–49. Draft specialized branches with exact sources and explicit proof obligations; complete simulation and the logical-memory capstone (50) as their prerequisites are available.

This is a writing sequence rather than an importance ranking. Missing FlagQuantum capabilities are investigated upstream while mathematical explanations and independent references are developed.

## Research anchors and source work

The earlier [reading guide](references/reading-guide.md) supports the foundations. [Compilation and physical-platform source notes](references/compilation-and-platforms.md) identify primary author references and official specifications used to scope the added routes. These are starting points, not claims of complete source or proof review.

The [hybrid-computing source anchors](references/hybrid-computing.md) support the new cross-cutting map, embedding, reconstruction and heterogeneous-workflow planning. Exact method-specific source/proof review remains pending.

Additional anchors include [QSVT](https://arxiv.org/abs/1806.01838), [surface codes](https://arxiv.org/abs/1208.0928v2), and [classical shadows](https://arxiv.org/abs/2002.08953). Each authored section needs exact theorem/equation locators, assumptions and an independent verification plan. Hardware performance and scientific-maturity comparisons require dated, claim-specific evidence.

## Stable identifiers, compatibility and history

The canonical records are in the repository's book/curriculum.json; display numbers and detailed pages are generated by scripts/build_curriculum.py. Stable chapter/section IDs are independent of display numbering. Check generated views with the script's --check option.

The earlier 40-chapter, 328-section plan omitted substantive hardware and compilation routes. This revision adds those routes and two computational-model bridges. The original simulation/research URLs retain legacy chapter and section anchors; current navigation points to stable chapter IDs. Published PDF samples retain their own numbering, source revision and validated scope.

The historical Nielsen–Chuang and Quantum Country reviews remain design records rather than the current chapter allocation. Current starter homes are **6, 23 and 49**; each requires expansion and review.
