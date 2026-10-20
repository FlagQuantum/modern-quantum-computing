# Full book plan

**Long-term curriculum revision: October 20, 2026.** Nine parts, 50 chapters and six appendices. The systematic editorial pass covers all 50 chapters and 435 sections, including physical-platform and quantum-compilation routes. The [editorial charter](editorial-charter.md) records the author's aim: a rigorous, accessible modern classic that helps present and future learners enter the field.

This is a curriculum architecture, not a completed manuscript or a claim that every proposed experiment is supported. Three starter chapters currently exist, with intended homes in Chapters **6, 23 and 49**. The three-chapter PDF retains independent sample numbering and its published version.

**Architecture status: full editorial pass completed; specialist/reader review and baseline freeze pending.** The [curriculum audit](curriculum-audit.md) lists coverage, prerequisite bridges, cross-layer laboratories and open review gates. [Reader continuity](reader-continuity.md) defines the no-skipped-steps standard. The [all-section result/proof/source plan](proof-plan.md) and [seven-volume proposal](volume-plan.md) extend the architecture review. The [review report](architecture-review.md), [435-section ledger](section-review.md) and [19 learning paths](learning-paths.md) make the review traceable. New textbook body drafting is paused until the architecture baseline gate. Chapter count is not an acceptance criterion.

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

**Reading level:** Core. **Entry guidance:** Basic Python and arithmetic; the opening calculation is an explicitly supplied preview.

**Numbered section specification:** [Sections 1.1–1.6](section-plans/01-foundations.md#ch-what-quantum-computing-computes).

**Planned sections:** Problems, inputs, and observable outputs; A first interference experiment; What a quantum state describes; Algorithms, simulators, and physical devices; What computational advantage would require; A map of the learning routes.

**Mathematical outcome:** Derive one interference probability before introducing the general formalism.

**Experiment and independent verification:** Predict and verify a tiny circuit; explain why its simulation establishes no speedup.

<span id="ch-complex-vectors-operators-and-numerical-reasoning"></span>

### Chapter 2: Complex Vectors, Operators, and Numerical Reasoning

**Reading level:** Core. **Entry guidance:** Basic Python; introductory linear algebra is refreshed locally.

**Numbered section specification:** [Sections 2.1–2.8](section-plans/01-foundations.md#ch-complex-vectors-operators-and-numerical-reasoning).

**Planned sections:** Complex scalars, vectors, and conjugation; Inner products, adjoints, and orthogonality; Linear maps, bases, and changes of coordinates; Hermitian, unitary, and positive operators; Spectral decomposition and singular values; Functions of matrices and time evolution; Norms, conditioning, and perturbations; Floating-point arithmetic and verification contracts.

**Mathematical outcome:** Derive spectral reconstruction and matrix-exponential identities under stated assumptions.

**Experiment and independent verification:** Check residuals and conditioning with independent NumPy/PyTorch calculations.

<span id="ch-single-qubit-states-and-rotations"></span>

### Chapter 3: Single-Qubit States and Rotations

**Reading level:** Core. **Entry guidance:** 2; the computational-basis probability postulate is introduced locally.

**Numbered section specification:** [Sections 3.1–3.7](section-plans/01-foundations.md#ch-single-qubit-states-and-rotations).

**Planned sections:** The pure-state postulate and physical equivalence; Relative phase and interference; The Bloch-sphere representation; Closed-system evolution and generators; Pauli algebra and rotation matrices; Composing rotations; Physical phase versus numerical equality.

**Mathematical outcome:** Derive rotations from their generators and prove the elementary no-cloning statement.

**Experiment and independent verification:** Compare matrices and circuit results, including phase-equivalent and distinguishable states.

<span id="ch-composite-systems-tensor-products-and-qubit-ordering"></span>

### Chapter 4: Composite Systems, Tensor Products, and Qubit Ordering

**Reading level:** Core. **Entry guidance:** 2–3.

**Numbered section specification:** [Sections 4.1–4.8](section-plans/01-foundations.md#ch-composite-systems-tensor-products-and-qubit-ordering).

**Planned sections:** Tensor-product spaces and basis states; Registers, labels, and basis indices; Local operators on a composite register; Multiple-qubit operators and ordered supports; Permutations, SWAP, and relabeling; Tensor reshaping as indexed mathematics; The no-cloning theorem; Cross-framework convention translation.

**Mathematical outcome:** Derive the basis-index map and local-operator action on an arbitrary register.

**Experiment and independent verification:** Compare two- and three-qubit operations with Kronecker products and deliberately changed qubit ordering.

<span id="ch-gates-reversible-computation-and-circuit-synthesis"></span>

### Chapter 5: Gates, Reversible Computation, and Circuit Synthesis

**Reading level:** Core. **Entry guidance:** 3–4.

**Numbered section specification:** [Sections 5.1–5.8](section-plans/01-foundations.md#ch-gates-reversible-computation-and-circuit-synthesis).

**Planned sections:** Circuit composition, inversion, and call order; Controlled operations and ancillas; Classical logic made reversible; Uncomputation and reusable workspace; Universal gate sets; Decomposing controlled and multi-qubit gates; Approximation, synthesis, and precision; Circuit identities and safe transformations.

**Mathematical outcome:** Derive controlled-gate matrices and a small reversible construction; state the approximation model.

**Experiment and independent verification:** Verify complete unitaries and account for ancillas and inverse operations.

<span id="ch-measurement-expectation-values-and-statistical-estimation"></span>

### Chapter 6: Measurement, Expectation Values, and Statistical Estimation

**Reading level:** Core. **Entry guidance:** 2–5; elementary probability is introduced locally before sampling.

**Numbered section specification:** [Sections 6.1–6.9](section-plans/01-foundations.md#ch-measurement-expectation-values-and-statistical-estimation).

**Planned sections:** Measurement outcomes and the Born rule; Conditional states and ignored outcomes; Observables, spectra, and expectations; Measuring in another basis; Generalized measurements and instruments [Advanced]; From exact probabilities to samples; Variance, covariance, and uncertainty; Confidence intervals and shot budgets; Measurement laboratory and failure diagnosis.

**Mathematical outcome:** Derive projective and generalized-measurement probabilities and finite-shot estimator uncertainty.

**Experiment and independent verification:** Extend the measurement starter; test conditional states and empirical coverage over repeated seeded trials.

<span id="ch-entanglement-and-quantum-information-protocols"></span>

### Chapter 7: Entanglement and Quantum Information Protocols

**Reading level:** Core. **Entry guidance:** 2, 4–6; reduced-density arguments are deferred to 8.

**Numbered section specification:** [Sections 7.1–7.9](section-plans/01-foundations.md#ch-entanglement-and-quantum-information-protocols).

**Planned sections:** Product states and entangled states; Schmidt decomposition; Bell states and basis changes; Correlations and the CHSH experiment; Teleportation, branch by branch; Superdense coding; No-signalling and classical communication; Entanglement swapping and quantum-network primitives; What entanglement alone does not guarantee.

**Mathematical outcome:** Derive Schmidt structure and all conditional branches of teleportation.

**Experiment and independent verification:** Verify corrections for arbitrary input states; inspect the receiver's unconditioned reduced state.

<span id="ch-density-matrices-reduced-states-and-purification"></span>

### Chapter 8: Density Matrices, Reduced States, and Purification

**Reading level:** Core. **Entry guidance:** 2, 4, 6; selected 7.2 for reduced Schmidt spectra.

**Numbered section specification:** [Sections 8.1–8.8](section-plans/01-foundations.md#ch-density-matrices-reduced-states-and-purification).

**Planned sections:** Statistical ensembles and density operators; Pure states, mixed states, and purity; Expectation values and measurement updates; Partial trace from operational consistency; Reduced states of entangled systems; Purification and nonuniqueness; Proper and improper mixtures; Density-operator verification laboratory.

**Mathematical outcome:** Derive mixed-state expectations and the relation between Schmidt coefficients and reduced spectra.

**Experiment and independent verification:** Check trace, positivity and subsystem states against explicit index sums.

## Part 2. Quantum Information: Channels, Inference, and Communication

<span id="ch-quantum-channels-and-their-representations"></span>

### Chapter 9: Quantum Channels and Their Representations

**Reading level:** Core. **Entry guidance:** 8; selected 4–6 for operational examples.

**Numbered section specification:** [Sections 9.1–9.8](section-plans/02-information.md#ch-quantum-channels-and-their-representations).

**Planned sections:** From closed evolution to quantum channels; Linearity, positivity, and complete positivity; Kraus operators and trace preservation; Stinespring dilation; Choi representation and vectorization; Representation equivalence and Kraus nonuniqueness; Composition, tensor products, and instruments; Channel-validation laboratory.

**Mathematical outcome:** Establish finite-dimensional representation equivalences and explain why positivity alone is insufficient.

**Experiment and independent verification:** Translate one small channel among representations; test complete positivity, trace preservation and environment dilation.

<span id="ch-distinguishability-fidelity-and-quantum-state-inference"></span>

### Chapter 10: Distinguishability, Fidelity, and Quantum State Inference

**Reading level:** Core. **Entry guidance:** 6, 8–9; advanced channel metrics and shadows are separable branches.

**Numbered section specification:** [Sections 10.1–10.9](section-plans/02-information.md#ch-distinguishability-fidelity-and-quantum-state-inference).

**Planned sections:** Classical distinguishability as a starting point; Quantum trace distance and binary discrimination; Fidelity and state-comparison conventions; Monotonicity and operational limits; Comparing channels and gate errors [Advanced]; State and process tomography; Pauli sums, grouping, and measurement allocation; Classical shadows [Advanced]; Inference laboratory and validation limits.

**Mathematical outcome:** Derive binary discrimination and simple estimation bounds; state the assumptions of shadow guarantees.

**Experiment and independent verification:** Compare independently reconstructed states and estimator errors; expose incomplete-measurement counterexamples.

<span id="ch-entropy-relative-entropy-and-information-processing"></span>

### Chapter 11: Entropy, Relative Entropy, and Information Processing

**Reading level:** Core with advanced proofs. **Entry guidance:** 8 and the state-comparison sections of 10; logarithm identities are introduced locally.

**Numbered section specification:** [Sections 11.1–11.8](section-plans/02-information.md#ch-entropy-relative-entropy-and-information-processing).

**Planned sections:** Classical entropy and uncertainty; Von Neumann entropy and spectra; Relative entropy and support conditions; Mutual and conditional information; Data processing; Subadditivity and strong subadditivity [Advanced]; Entropic reasoning in protocols; Information-inequality laboratory.

**Mathematical outcome:** Prove accessible special cases and selected central results; identify the ingredients and source of deferred general proofs.

**Experiment and independent verification:** Compute small exact and commuting examples and counterexamples to invalid entropy intuitions.

<span id="ch-compression-entanglement-and-communication-limits"></span>

### Chapter 12: Compression, Entanglement, and Communication Limits

**Reading level:** Advanced. **Entry guidance:** 7–8, 11; individual communication/entanglement branches use selected sections.

**Numbered section specification:** [Sections 12.1–12.9](section-plans/02-information.md#ch-compression-entanglement-and-communication-limits).

**Planned sections:** Operational tasks and asymptotic statements; Typical sequences and subspaces; Schumacher compression; Entanglement concentration and dilution; Mixed-state entanglement, LOCC, and distillation [Advanced]; Accessible information and the Holevo bound; Classical and quantum channel capacities; Finite-block limitations and resource accounting; Compression and communication laboratory.

**Mathematical outcome:** Derive a finite-block compression example and state coding theorems with their operational assumptions.

**Experiment and independent verification:** Compare small block encodings and success/error tradeoffs; distinguish finite demonstrations from asymptotic proofs.

<span id="ch-quantum-cryptography-and-security-reasoning"></span>

### Chapter 13: Quantum Cryptography and Security Reasoning

**Reading level:** Advanced. **Entry guidance:** 6, 8 for the entry; 10–11 for advanced proof branches, not all of 12.

**Numbered section specification:** [Sections 13.1–13.9](section-plans/02-information.md#ch-quantum-cryptography-and-security-reasoning).

**Planned sections:** Security tasks and adversarial models; BB84 preparation, measurement, and sifting; Parameter estimation and finite samples; Error reconciliation and information leakage; Privacy amplification; Composable security and proof structure [Advanced]; Attacks, side channels, and failure diagnosis; Cryptographic tasks and impossibility boundaries [Advanced]; A security-claim audit.

**Mathematical outcome:** Derive an intercept-resend example and the logic of a scoped security argument; delimit the full security theorem.

**Experiment and independent verification:** Run a toy protocol with confidence bounds; explain why a low observed error rate alone does not establish security.

## Part 3. Quantum Algorithms and Computational Resources

<span id="ch-computational-models-complexity-and-quantum-advantage"></span>

### Chapter 14: Computational Models, Complexity, and Quantum Advantage

**Reading level:** Core. **Entry guidance:** 4–6.

**Numbered section specification:** [Sections 14.1–14.9](section-plans/03-algorithms.md#ch-computational-models-complexity-and-quantum-advantage).

**Planned sections:** Problems, input length, and computational models; Reversible computation and uniform circuit families; Complexity classes and bounded error; Oracle and data-access models; Accuracy, repetition, and success probability; Complete resource accounting; Quantum-classical interaction patterns; Classical baselines and advantage claims; Resource-audit laboratory.

**Mathematical outcome:** Relate input/output access assumptions to a complete resource expression.

**Experiment and independent verification:** Audit examples including state preparation, oracle synthesis, repetitions and readout; avoid simulator-time speedup claims.

<span id="ch-interference-oracles-and-phase-kickback"></span>

### Chapter 15: Interference, Oracles, and Phase Kickback

**Reading level:** Core. **Entry guidance:** 5, 14; binary linear algebra is introduced locally for Simon’s problem.

**Numbered section specification:** [Sections 15.1–15.8](section-plans/03-algorithms.md#ch-interference-oracles-and-phase-kickback).

**Planned sections:** Boolean functions as reversible oracles; Phase kickback; Deutsch's problem; The Deutsch-Jozsa promise; Bernstein-Vazirani and hidden parity; Simon’s problem and hidden structure; Oracle synthesis and uncomputation; Interference-algorithm laboratory.

**Mathematical outcome:** Derive the phase-oracle action and complete output distributions.

**Experiment and independent verification:** Check truth tables and gate-level oracles against dense permutation and diagonal references.

<span id="ch-grover-search-amplitude-amplification-and-estimation"></span>

### Chapter 16: Grover Search, Amplitude Amplification, and Estimation

**Reading level:** Core with advanced extensions. **Entry guidance:** 5–6, 14–15; phase-free estimation has no Chapter 17 prerequisite.

**Numbered section specification:** [Sections 16.1–16.8](section-plans/03-algorithms.md#ch-grover-search-amplitude-amplification-and-estimation).

**Planned sections:** Search promises and marked subspaces; Reflections and the invariant plane; Success probability and stopping; General amplitude amplification; Unknown success probabilities [Advanced]; Amplitude estimation without phase estimation [Advanced]; Classical estimation, uncertainty, and query comparisons [Advanced]; Search-and-estimation laboratory.

**Mathematical outcome:** Derive the success curve and a scoped estimation error/query relation.

**Experiment and independent verification:** Compare complete distributions with analytic predictions and ordinary Monte Carlo under the same access assumptions.

<span id="ch-fourier-transforms-and-quantum-phase-estimation"></span>

### Chapter 17: Fourier Transforms and Quantum Phase Estimation

**Reading level:** Core. **Entry guidance:** 4–6, 14–15; amplitude-estimation extension follows phase estimation here.

**Numbered section specification:** [Sections 17.1–17.9](section-plans/03-algorithms.md#ch-fourier-transforms-and-quantum-phase-estimation).

**Planned sections:** The discrete Fourier transform; Factorizing the QFT; Inverse transforms and qubit reversal; Approximate QFT; Controlled powers and phase kickback; Exact-grid phase estimation; Off-grid phases and superposed eigenstates; Phase-estimation-based amplitude estimation [Advanced]; Precision, success, and algorithmic cost.

**Mathematical outcome:** Derive QFT structure and finite-precision phase-estimation probabilities.

**Experiment and independent verification:** Compare every small basis input and off-grid output distribution with dense references.

<span id="ch-period-finding-factoring-and-algorithmic-arithmetic"></span>

### Chapter 18: Period Finding, Factoring, and Algorithmic Arithmetic

**Reading level:** Advanced. **Entry guidance:** 5, 14, 17; number-theory/group bridges are local.

**Numbered section specification:** [Sections 18.1–18.9](section-plans/03-algorithms.md#ch-period-finding-factoring-and-algorithmic-arithmetic).

**Planned sections:** From factoring to order finding; Reversible modular arithmetic; Coherent modular exponentiation; Period information from phase estimation; Continued fractions and candidate verification; Factoring end to end; Discrete logarithms and Abelian hidden subgroups [Advanced]; Arithmetic, synthesis, and resource growth; A reproducible factoring laboratory.

**Mathematical outcome:** Derive the reduction from factoring to order finding and its classical postprocessing conditions.

**Experiment and independent verification:** Factor tiny examples using explicit modular arithmetic; avoid precompiled circuits that assume the answer.

<span id="ch-hamiltonian-simulation-and-error-bounds"></span>

### Chapter 19: Hamiltonian Simulation and Error Bounds

**Reading level:** Core with advanced extensions. **Entry guidance:** 2, 5 for dynamics; 14 for resource analysis; no QFT/phase-estimation prerequisite for product formulas.

**Numbered section specification:** [Sections 19.1–19.9](section-plans/03-algorithms.md#ch-hamiltonian-simulation-and-error-bounds).

**Planned sections:** Hamiltonians, evolution, and access models; Commuting terms and exact factorizations; First-order product formulas; Symmetric and higher-order constructions; Pauli-term exponentiation; State, observable, and operator error; Alternative simulation paradigms [Advanced]; Adiabatic computation and gap assumptions [Advanced]; Dynamics laboratory and resource budget.

**Mathematical outcome:** Derive product formulas and a finite-system error bound; prepare the transition to signal processing.

**Experiment and independent verification:** Compare with matrix exponentials and verify error scaling against an actual bound.

<span id="ch-block-encodings-and-quantum-linear-algebra"></span>

### Chapter 20: Block Encodings and Quantum Linear Algebra

**Reading level:** Advanced. **Entry guidance:** 2, 5, 14; selected 16 for amplification and 19 for dynamics applications.

**Numbered section specification:** [Sections 20.1–20.9](section-plans/03-algorithms.md#ch-block-encodings-and-quantum-linear-algebra).

**Planned sections:** Why matrix access must be specified; Block-encoding definitions and ancillas; Linear combinations of unitaries; Composing encoded operations; Postselection and amplification; Quantum linear systems and conditioning; Qubitization and invariant subspaces [Advanced]; Spectral functions and application contracts; Linear-algebra laboratory.

**Mathematical outcome:** Construct a block encoding and derive normalization, success probability and condition-number dependence.

**Experiment and independent verification:** Check encoded blocks numerically and include state preparation/readout in the resource analysis.

<span id="ch-quantum-signal-processing-and-singular-value-transformation"></span>

### Chapter 21: Quantum Signal Processing and Singular Value Transformation

**Reading level:** Advanced. **Entry guidance:** 2, 5, block-encoding sections of 20; application-specific dependencies are listed per section.

**Numbered section specification:** [Sections 21.1–21.9](section-plans/03-algorithms.md#ch-quantum-signal-processing-and-singular-value-transformation).

**Planned sections:** A scalar signal encoded in SU(2); Phase-controlled polynomial sequences; Admissibility and approximation; Phase synthesis and numerical stability; From eigenvalues to singular values; A precise QSVT theorem [Advanced]; Applications: filtering, inversion, and evolution; Precision and complete complexity; Signal-processing laboratory.

**Mathematical outcome:** Derive low-degree constructions, state a precise transformation theorem and prove a selected application.

**Experiment and independent verification:** Compare transformed scalar values and small matrix singular values with polynomial targets; report synthesis and approximation errors.

<span id="ch-quantum-walks-lower-bounds-and-algorithm-design"></span>

### Chapter 22: Quantum Walks, Lower Bounds, and Algorithm Design

**Reading level:** Advanced. **Entry guidance:** 5, 14, 16 for entry; selected 20–21 for spectral-framework comparisons.

**Numbered section specification:** [Sections 22.1–22.9](section-plans/03-algorithms.md#ch-quantum-walks-lower-bounds-and-algorithm-design).

**Planned sections:** Walk models and computational tasks; Unitarity, spectra, and dynamics; Search and marked vertices; Hitting behavior and algorithmic resources; The polynomial method [Advanced]; A representative query lower bound; Choosing an algorithmic framework; Hamiltonian complexity and limits of optimization [Advanced]; Algorithm-design laboratory.

**Mathematical outcome:** Analyze a small walk and derive a representative lower bound under an explicit oracle model.

**Experiment and independent verification:** Compare walk evolution with an independent transition/spectral construction and identify inaccessible speedup assumptions.

## Part 4. Variational and Differentiable Quantum Computing

<span id="ch-parameterized-circuits-quantum-gradients-and-differentiation"></span>

### Chapter 23: Parameterized Circuits, Quantum Gradients, and Differentiation

**Reading level:** Core. **Entry guidance:** 2–3, 5–6; a local calculus bridge precedes differentiation.

**Numbered section specification:** [Sections 23.1–23.10](section-plans/04-variational.md#ch-parameterized-circuits-quantum-gradients-and-differentiation).

**Planned sections:** Parameterized quantum models and tensor contracts; Differentiating a unitary expectation; The single-Pauli parameter-shift rule; Generator spectra and generalized shift rules [Advanced]; Shared parameters and classical reparameterization; Backpropagation and automatic differentiation; Adjoint differentiation and memory tradeoffs; Finite differences and numerical diagnostics; Finite-shot gradient estimation; Differentiation laboratory and cost audit.

**Mathematical outcome:** Derive spectral shift rules, normalization changes and parameter-reuse chain rules; analyze execution and memory costs.

**Experiment and independent verification:** Expand the gradient starter with analytic, dense, shifted and autograd checks for multiple parameter occurrences.

<span id="ch-optimization-geometry-and-trainability"></span>

### Chapter 24: Optimization, Geometry, and Trainability

**Reading level:** Advanced. **Entry guidance:** 23 for entry; 6 for stochastic estimates and 10.3 for geometry, without all state-inference material.

**Numbered section specification:** [Sections 24.1–24.9](section-plans/04-variational.md#ch-optimization-geometry-and-trainability).

**Planned sections:** Objectives and optimization problems; Exact and stochastic gradients; Optimizers, initialization, and diagnostics; Quantum geometric tensor; Natural-gradient updates and singular metrics; Expressivity, identifiability, and trainability; Barren plateaus and ensemble assumptions [Advanced]; Noise, shot budgets, and mitigation overhead; Optimization laboratory and honest conclusions.

**Mathematical outcome:** Derive a small metric and gradient-variance example; state the ensemble assumptions of trainability results.

**Experiment and independent verification:** Separate convergence, expressivity and sampling effects; compare initializations and controlled classical baselines.

<span id="ch-variational-simulation-chemistry-and-ground-state-problems"></span>

### Chapter 25: Variational Simulation, Chemistry, and Ground-State Problems

**Reading level:** Core application. **Entry guidance:** 2, 4, 6 for the energy/model entry; selected 23–24 for optimization and embedding extensions.

**Numbered section specification:** [Sections 25.1–25.12](section-plans/04-variational.md#ch-variational-simulation-chemistry-and-ground-state-problems).

**Planned sections:** The variational principle and its assumptions; Second quantization and occupation states; Jordan-Wigner and fermion-to-qubit translation; Symmetries and reduced models; Ansatz design and reachable states; Measuring an energy objective; Variational dynamics and extensions [Advanced]; Chemistry model and error budgets; Classical environments and quantum embedding [Advanced]; Self-consistent quantum impurity solvers [Advanced]; Quantum sampling and classical subspace diagonalization [Advanced]; Variational-simulation laboratory.

**Mathematical outcome:** Prove the energy bound and derive a small occupation-to-qubit Hamiltonian with units and offsets.

**Experiment and independent verification:** Compare independent fermionic/qubit matrices and exact diagonalization; report all model and estimator errors.

<span id="ch-qaoa-quantum-optimization-and-classical-comparisons"></span>

### Chapter 26: QAOA, Quantum Optimization, and Classical Comparisons

**Reading level:** Advanced application. **Entry guidance:** 5–6, 14; selected 23–24 for the optimization branch.

**Numbered section specification:** [Sections 26.1–26.8](section-plans/04-variational.md#ch-qaoa-quantum-optimization-and-classical-comparisons).

**Planned sections:** From a discrete objective to a Hamiltonian; Cost and mixer evolution; Low-depth analytic behavior; Constraints and feasible mixers [Advanced]; Parameter landscapes and depth; Sampled solutions and approximation quality; Classical comparisons and total cost; Optimization laboratory.

**Mathematical outcome:** Derive MaxCut and one low-depth result under explicit graph and sign conventions.

**Experiment and independent verification:** Compare against exhaustive solutions and meaningful classical heuristics without inferring advantage from tiny instances.

<span id="ch-quantum-learning-kernels-and-hybrid-models"></span>

### Chapter 27: Quantum Learning, Kernels, and Hybrid Models

**Reading level:** Advanced application. **Entry guidance:** 6, 14 and a local learning/statistics bridge; 23–24 for trainable layers, not fixed-kernel entry.

**Numbered section specification:** [Sections 27.1–27.8](section-plans/04-variational.md#ch-quantum-learning-kernels-and-hybrid-models).

**Planned sections:** Learning tasks and data-access assumptions; Encoding data into quantum states; Hybrid models and the joint chain rule; Quantum feature maps and kernels; Training kernels and hybrid models; Generalization and statistical claims; Classical simulability and meaningful baselines; Learning laboratory and claim audit.

**Mathematical outcome:** Derive kernel/feature-map relations and joint gradients; state learning-task and data-access assumptions.

**Experiment and independent verification:** Use held-out evaluation, classical baselines and end-to-end gradient checks; include encoding and measurement costs.

## Part 5. Noise, Error Correction, and Fault-Tolerant Computation

<span id="ch-noise-open-systems-and-error-mitigation"></span>

### Chapter 28: Noise, Open Systems, and Error Mitigation

**Reading level:** Core. **Entry guidance:** 8–9 for channels; local time-evolution/differential-equation bridge for the dynamics branch.

**Numbered section specification:** [Sections 28.1–28.10](section-plans/05-fault-tolerance.md#ch-noise-open-systems-and-error-mitigation).

**Planned sections:** Noise models and system-environment assumptions; Discrete channels: dephasing and depolarization; Amplitude damping and relaxation; Lindblad dynamics; Quantum trajectories and unravelings; Correlated and non-Markovian limitations [Advanced]; Error mitigation: bias, variance, and cost; Calibration, drift, and model validation; SPAM, gate characterization, and randomized benchmarking [Advanced]; Noise laboratory and evidence boundaries.

**Mathematical outcome:** Derive amplitude damping and one master equation; analyze the bias/variance tradeoff of a mitigation example.

**Experiment and independent verification:** Compare density evolution with an independent solver and trajectory averages; test positivity, trace and estimator uncertainty.

<span id="ch-quantum-error-correction-conditions-and-recovery"></span>

### Chapter 29: Quantum Error Correction: Conditions and Recovery

**Reading level:** Core. **Entry guidance:** 4–6, 8–9; selected 28 for physical noise examples.

**Numbered section specification:** [Sections 29.1–29.9](section-plans/05-fault-tolerance.md#ch-quantum-error-correction-conditions-and-recovery).

**Planned sections:** The quantum error-correction problem; Encoding and logical information; Repetition codes and syndrome extraction; Error sets and coherent combinations; Knill-Laflamme conditions; Constructing a recovery operation; Degeneracy, distance, and limitations; Beyond bit-flip protection; Recovery laboratory and logical-state verification.

**Mathematical outcome:** Prove the correction condition in a finite example and explain preservation of logical information by syndrome measurement.

**Experiment and independent verification:** Enumerate errors and verify recovery on arbitrary encoded superpositions, including coherent error combinations.

<span id="ch-stabilizer-codes-logical-operators-and-decoding"></span>

### Chapter 30: Stabilizer Codes, Logical Operators, and Decoding

**Reading level:** Core with advanced extensions. **Entry guidance:** 4–6 for Pauli/stabilizer entry; 29 for code/recovery branches; binary algebra is local.

**Numbered section specification:** [Sections 30.1–30.11](section-plans/05-fault-tolerance.md#ch-stabilizer-codes-logical-operators-and-decoding).

**Planned sections:** Pauli groups and binary symplectic algebra; Stabilizer groups and code spaces; Syndromes as commutation data; CSS codes from classical checks; Logical operators and code distance; Degeneracy and decoding choices; Syndrome circuits and fault propagation; Decoder interfaces and evidence records; Quantum LDPC families and architectural tradeoffs [Advanced]; Graph states and measurement-based computation; Stabilizer-code laboratory.

**Mathematical outcome:** Derive a code's syndrome map, logical operators and distance; connect binary algebra to quantum operators.

**Experiment and independent verification:** Compare stabilizer calculations with dense small-code references and injected-error enumeration.

<span id="ch-surface-codes-and-repeated-syndrome-measurements"></span>

### Chapter 31: Surface Codes and Repeated Syndrome Measurements

**Reading level:** Advanced. **Entry guidance:** Selected noise, correction and stabilizer sections in 28–30.

**Numbered section specification:** [Sections 31.1–31.8](section-plans/05-fault-tolerance.md#ch-surface-codes-and-repeated-syndrome-measurements).

**Planned sections:** From stabilizer checks to a surface-code lattice; Logical operators and distance; Syndrome-extraction circuits; Measurement faults and detection events; Space-time decoding; Logical memory and failure observables; Finite-size scaling and threshold claims; Surface-code laboratory.

**Mathematical outcome:** Derive checks and detection-event patterns for a small patch and repeated rounds.

**Experiment and independent verification:** Verify hand-enumerated faults before Monte Carlo; report noise model, decoder, distance, uncertainty and finite-size limits.

<span id="ch-fault-tolerant-gates-and-universal-logical-computation"></span>

### Chapter 32: Fault-Tolerant Gates and Universal Logical Computation

**Reading level:** Advanced. **Entry guidance:** 28–30; 31 only for the surface-code/lattice-surgery branch; factoring is not required.

**Numbered section specification:** [Sections 32.1–32.8](section-plans/05-fault-tolerance.md#ch-fault-tolerant-gates-and-universal-logical-computation).

**Planned sections:** Fault tolerance and propagation of errors; Fault-tolerant preparation, measurement, and recovery; Transversal operations and their limits; Threshold reasoning [Advanced]; Code deformation and lattice surgery; Magic states and gate injection; Distillation and rejection costs; Universal logical computation laboratory.

**Mathematical outcome:** Derive a fault-propagation example and a small distillation/rejection calculation; state threshold assumptions and explain proof structure.

**Experiment and independent verification:** Compare ideal logical actions with fault-injected circuits and count accepted outputs, logical errors and consumed resources.

<span id="ch-from-logical-algorithms-to-physical-resource-estimates"></span>

### Chapter 33: From Logical Algorithms to Physical Resource Estimates

**Reading level:** Advanced synthesis. **Entry guidance:** 14 and selected logical-computation sections of 32; a chosen algorithm workload, not every algorithm chapter.

**Numbered section specification:** [Sections 33.1–33.8](section-plans/05-fault-tolerance.md#ch-from-logical-algorithms-to-physical-resource-estimates).

**Planned sections:** Define an algorithmic workload and success target; Logical synthesis and non-Clifford resources; Distributing an error budget; Code distance and logical reliability; Magic-state factories and scheduling; Physical qubits, cycles, and runtime; Sensitivity, uncertainty, and comparison; Resource-estimation laboratory.

**Mathematical outcome:** Derive a complete small cost model with a target success probability and explicit architecture/noise assumptions.

**Experiment and independent verification:** Recompute resource estimates under changing assumptions; separate symbolic estimates from measured device performance.

## Part 6. Physical Realizations and Quantum-System Architecture

<span id="ch-from-abstract-qubits-to-physical-quantum-systems"></span>

### Chapter 34: From Abstract Qubits to Physical Quantum Systems

**Reading level:** Core bridge with optional physics extensions. **Entry guidance:** 2–3, 5–6, 8 for entry; selected 9/28/29/30 only for corresponding optional branches.

**Numbered section specification:** [Sections 34.1–34.10](section-plans/physical-platforms.md#ch-from-abstract-qubits-to-physical-quantum-systems).

**Planned sections:** Levels, modes, and computational subspaces; Oscillator and light-matter mathematics bridge; Driven systems, rotating frames, and resonance; Preparation, control, and readout as an experiment; Digital, analog, and measurement-based models; Noise, leakage, loss, and hardware constraints; Oscillator encodings and bosonic correction [Advanced]; Connectivity, transport, and modular architectures; A fair platform-comparison framework; Choose a platform learning branch.

**Mathematical outcome:** Develop the explicit physical/program model and its stated approximations through the section-level derivations.

**Experiment and independent verification:** Produce a complete small independent reference, an implementation contract and an assumption/error/resource record before claiming framework support.

<span id="ch-superconducting-qubits-and-circuit-qed-control"></span>

### Chapter 35: Superconducting Qubits and Circuit-QED Control

**Reading level:** Advanced platform branch. **Entry guidance:** Selected common physics bridge in 34; no whole algorithm or fault-tolerance route is required.

**Numbered section specification:** [Sections 35.1–35.8](section-plans/physical-platforms.md#ch-superconducting-qubits-and-circuit-qed-control).

**Planned sections:** An electrical circuit becomes a quantum model; Anharmonicity and the transmon computational subspace; Microwave control and single-qubit rotations; Coupling and native two-qubit interactions; Dispersive readout and assignment errors; Decoherence, crosstalk, and calibration; Target constraints for compilation; Superconducting-model laboratory.

**Mathematical outcome:** Develop the explicit physical/program model and its stated approximations through the section-level derivations.

**Experiment and independent verification:** Produce a complete small independent reference, an implementation contract and an assumption/error/resource record before claiming framework support.

<span id="ch-trapped-ion-qubits-motional-gates-and-transport"></span>

### Chapter 36: Trapped-Ion Qubits, Motional Gates, and Transport

**Reading level:** Advanced platform branch. **Entry guidance:** Selected oscillator/drive/measurement bridge in 34.

**Numbered section specification:** [Sections 36.1–36.8](section-plans/physical-platforms.md#ch-trapped-ion-qubits-motional-gates-and-transport).

**Planned sections:** Internal states, trapping, and preparation; Collective motion and sidebands; Carrier drives and single-qubit control; Motional entangling gates; Readout, heating, and coherence; Chains, QCCD transport, and photonic links; Target constraints for compilation; Trapped-ion laboratory.

**Mathematical outcome:** Develop the explicit physical/program model and its stated approximations through the section-level derivations.

**Experiment and independent verification:** Produce a complete small independent reference, an implementation contract and an assumption/error/resource record before claiming framework support.

<span id="ch-neutral-atom-arrays-and-rydberg-quantum-computing"></span>

### Chapter 37: Neutral-Atom Arrays and Rydberg Quantum Computing

**Reading level:** Advanced platform branch. **Entry guidance:** Selected common bridge in 34; 19 only for advanced dynamics/error analysis.

**Numbered section specification:** [Sections 37.1–37.8](section-plans/physical-platforms.md#ch-neutral-atom-arrays-and-rydberg-quantum-computing).

**Planned sections:** Trapping, internal encodings, and rearrangement; Rydberg interactions and blockade; Single-qubit and entangling control; Analog Hamiltonian programming; Transport, parallelism, and compilation; Atom loss, readout, and imperfect interactions; Digital versus analog experiment contracts; Neutral-atom laboratory.

**Mathematical outcome:** Develop the explicit physical/program model and its stated approximations through the section-level derivations.

**Experiment and independent verification:** Produce a complete small independent reference, an implementation contract and an assumption/error/resource record before claiming framework support.

<span id="ch-photonic-encodings-optical-circuits-and-measurement-based-computation"></span>

### Chapter 38: Photonic Encodings, Optical Circuits, and Measurement-Based Computation

**Reading level:** Advanced platform branch. **Entry guidance:** 7 and selected oscillator/measurement bridge in 34; selected 30 for resource-state computation.

**Numbered section specification:** [Sections 38.1–38.9](section-plans/physical-platforms.md#ch-photonic-encodings-optical-circuits-and-measurement-based-computation).

**Planned sections:** Optical modes and qubit encodings; Beam splitters, phases, and interferometers; Interference, sources, and detection; Measurement-induced operations and heralding; Graph states, fusion, and logical computation; Continuous-variable and bosonic branches [Advanced]; Loss, erasure, and multiplexing resources; Photonic compilation and architecture contracts; Photonic laboratory.

**Mathematical outcome:** Develop the explicit physical/program model and its stated approximations through the section-level derivations.

**Experiment and independent verification:** Produce a complete small independent reference, an implementation contract and an assumption/error/resource record before claiming framework support.

<span id="ch-semiconductor-spin-qubits-and-exchange-based-architectures"></span>

### Chapter 39: Semiconductor Spin Qubits and Exchange-Based Architectures

**Reading level:** Advanced platform branch. **Entry guidance:** Selected common bridge in 34.

**Numbered section specification:** [Sections 39.1–39.8](section-plans/physical-platforms.md#ch-semiconductor-spin-qubits-and-exchange-based-architectures).

**Planned sections:** Spin encodings and confined-charge models; Zeeman control and electrically driven rotations; Exchange and entangling operations; Charge, valley, and leakage degrees of freedom; Initialization and spin-to-charge readout; Noise, variability, and calibration; Coupling, shuttling, and modular constraints; Spin-qubit laboratory.

**Mathematical outcome:** Develop the explicit physical/program model and its stated approximations through the section-level derivations.

**Experiment and independent verification:** Produce a complete small independent reference, an implementation contract and an assumption/error/resource record before claiming framework support.

<span id="ch-topological-quantum-computation-and-candidate-physical-realizations"></span>

### Chapter 40: Topological Quantum Computation and Candidate Physical Realizations

**Reading level:** Advanced platform branch. **Entry guidance:** 7–8 and selected 34 for entry; 25 for Majorana models and 29–32 for protection/logical-resource comparisons.

**Numbered section specification:** [Sections 40.1–40.8](section-plans/physical-platforms.md#ch-topological-quantum-computation-and-candidate-physical-realizations).

**Planned sections:** Topology, protection, and distinct meanings; Fusion spaces and encoded information; Fusion bases, F/R moves, and braiding; Measurement, corrections, and computational power; Majorana models and parity encoding [Advanced]; Protection assumptions and failure mechanisms; Experiments, signatures, and unresolved evidence; Topological compilation and laboratory.

**Mathematical outcome:** Develop the explicit physical/program model and its stated approximations through the section-level derivations.

**Experiment and independent verification:** Produce a complete small independent reference, an implementation contract and an assumption/error/resource record before claiming framework support.

## Part 7. Quantum Programming, Compilation, and Control

<span id="ch-quantum-programs-intermediate-representations-and-verified-optimization"></span>

### Chapter 41: Quantum Programs, Intermediate Representations, and Verified Optimization

**Reading level:** Core systems route with advanced extensions. **Entry guidance:** 4–6 for circuit semantics/IR; 9 for channel/dynamic branches; no microscopic hardware prerequisite.

**Numbered section specification:** [Sections 41.1–41.9](section-plans/quantum-compilation.md#ch-quantum-programs-intermediate-representations-and-verified-optimization).

**Planned sections:** What a quantum compiler must preserve; Programs, types, and quantum-classical control; Circuit DAGs and intermediate representations; Lowering and reversible computation; Local rewrites, commutation, and optimization; Phase, parameters, and controlled contexts; Channels, measurements, and dynamic programs; Interchange, export, and capability boundaries; A minimal verified compiler laboratory.

**Mathematical outcome:** Develop the explicit physical/program model and its stated approximations through the section-level derivations.

**Experiment and independent verification:** Produce a complete small independent reference, an implementation contract and an assumption/error/resource record before claiming framework support.

<span id="ch-gate-synthesis-qubit-mapping-routing-and-scheduling"></span>

### Chapter 42: Gate Synthesis, Qubit Mapping, Routing, and Scheduling

**Reading level:** Core systems route with advanced extensions. **Entry guidance:** 5, 41 and an explicit target contract defined here; physical-platform details and logical synthesis are optional branches.

**Numbered section specification:** [Sections 42.1–42.10](section-plans/quantum-compilation.md#ch-gate-synthesis-qubit-mapping-routing-and-scheduling).

**Planned sections:** Target models and native-operation contracts; Single-qubit synthesis; Two-qubit and multi-qubit synthesis; Approximate synthesis and logical gate sets [Advanced]; Initial logical-to-physical placement; Routing and changing qubit mappings; Routing search and heuristic limits; Scheduling with timing and shared resources; Joint objectives and error-aware compilation; Mapping-and-scheduling laboratory.

**Mathematical outcome:** Develop the explicit physical/program model and its stated approximations through the section-level derivations.

**Experiment and independent verification:** Produce a complete small independent reference, an implementation contract and an assumption/error/resource record before claiming framework support.

<span id="ch-control-level-lowering-dynamic-execution-and-logical-compilation"></span>

### Chapter 43: Control-Level Lowering, Dynamic Execution, and Logical Compilation

**Reading level:** Advanced systems route. **Entry guidance:** Branch-specific: control uses selected 19/23/28/34; dynamic execution uses measurement and program semantics; logical lowering uses 32–33.

**Numbered section specification:** [Sections 43.1–43.10](section-plans/quantum-compilation.md#ch-control-level-lowering-dynamic-execution-and-logical-compilation).

**Planned sections:** From native gates to control Hamiltonians; Pulse shaping and constrained optimization; Frames, virtual operations, and calibration; Crosstalk, leakage, and robust control; Near-device feedback, decoding, and dynamic execution; Lowering analog and measurement-based programs; Fault-tolerant logical compilation; Cross-layer verification and approximate equivalence; CPU/GPU/QPU workflows and runtime orchestration; Hardware-aware compilation laboratory.

**Mathematical outcome:** Develop the explicit physical/program model and its stated approximations through the section-level derivations.

**Experiment and independent verification:** Produce a complete small independent reference, an implementation contract and an assumption/error/resource record before claiming framework support.

## Part 8. Classical Simulation and the Boundary of Tractability

<span id="ch-exact-simulation-tensor-execution-and-numerical-reliability"></span>
<span id="chapter-34-exact-simulation-tensor-execution-and-numerical-reliability"></span>

### Chapter 44: Exact Simulation, Tensor Execution, and Numerical Reliability

**Reading level:** Core. **Entry guidance:** 2, 4–6 for the exact-state executor; 8–9 for channels, 23 for gradients and 14 for parallel-resource analysis.

**Numbered section specification:** [Sections 44.1–44.8](section-plans/06-simulation.md#ch-exact-simulation-tensor-execution-and-numerical-reliability).

**Planned sections:** Requested outputs and exact-simulation cost; Applying local gates by tensor indices; Observables and measurement execution; Density-matrix and channel execution; Batching and differentiation; Precision, stability, and normalization drift; Parallel execution and communication; Exact-executor laboratory and benchmarks.

**Mathematical outcome:** Derive local-gate tensor contractions and storage/time costs, including communication assumptions.

**Experiment and independent verification:** Build an independent minimal executor; compare states, channels and gradients before benchmarking.

<span id="ch-stabilizer-simulation-magic-and-classical-simulability"></span>
<span id="chapter-35-stabilizer-simulation-magic-and-classical-simulability"></span>

### Chapter 45: Stabilizer Simulation, Magic, and Classical Simulability

**Reading level:** Advanced. **Entry guidance:** 5–6 and Pauli/stabilizer sections of 30; a full error-correction or statevector chapter is not required for tableau entry.

**Numbered section specification:** [Sections 45.1–45.8](section-plans/06-simulation.md#ch-stabilizer-simulation-magic-and-classical-simulability).

**Planned sections:** Clifford operations and stabilizer states; Tableau representations and phase conventions; Clifford gate updates; Measurement and classical control; The Gottesman-Knill theorem; Beyond stabilizers: non-Clifford resources; Magic as a computational resource [Advanced]; Stabilizer-simulation laboratory.

**Mathematical outcome:** Derive tableau updates and explain the assumptions behind efficient stabilizer simulation.

**Experiment and independent verification:** Compare tableau and dense results, including measurement branches; trace the resource impact of non-Clifford operations.

<span id="ch-matrix-product-states-entanglement-and-truncation"></span>
<span id="chapter-36-matrix-product-states-entanglement-and-truncation"></span>

### Chapter 46: Matrix Product States, Entanglement, and Truncation

**Reading level:** Advanced. **Entry guidance:** 2, 4, Schmidt structure in 7; selected 10/44 for comparisons, not tomography or autograd.

**Numbered section specification:** [Sections 46.1–46.8](section-plans/06-simulation.md#ch-matrix-product-states-entanglement-and-truncation).

**Planned sections:** Entanglement and compact state representations; Building an MPS by successive SVDs; Gauge freedom and canonical forms; Single- and two-qubit updates; Truncation and discarded weight; Accumulated error and observable accuracy; Bond dimension, entanglement, and cost; MPS laboratory.

**Mathematical outcome:** Derive MPS construction and discarded-weight error relations with normalization assumptions.

**Experiment and independent verification:** Compare with exact states while varying bonds and gate geometry; report accumulated error and cost.

<span id="ch-tensor-networks-contraction-and-hybrid-simulation-strategies"></span>
<span id="chapter-37-tensor-networks-contraction-and-hybrid-simulation-strategies"></span>

### Chapter 47: Tensor Networks, Contraction, and Hybrid Simulation Strategies

**Reading level:** Advanced. **Entry guidance:** 4–5, 14 for circuit contractions; 6/9 for cutting and 44/46 only for the chosen hybrid executor.

**Numbered section specification:** [Sections 47.1–47.10](section-plans/06-simulation.md#ch-tensor-networks-contraction-and-hybrid-simulation-strategies).

**Planned sections:** Circuits as indexed tensor networks; Contraction order and intermediate size; Path selection and structural parameters; Slicing and recomputation; Amplitudes, expectations, sampling, and full states; Circuit cutting and classical reconstruction; Reconstruction variance and sampling overhead; Hybrid and distributed strategies; Approximation and numerical reliability; Tensor-network laboratory.

**Mathematical outcome:** Derive a circuit contraction and predict path-dependent intermediate memory.

**Experiment and independent verification:** Check independent contractions, profile declared workloads and explain when simulation becomes intractable.

## Part 9. From Papers to Reproducible Research

<span id="ch-reading-papers-building-evidence-and-reproducing-results"></span>
<span id="chapter-38-reading-papers-building-evidence-and-reproducing-results"></span>

### Chapter 48: Reading Papers, Building Evidence, and Reproducing Results

**Reading level:** Core research method. **Entry guidance:** 4, 6 for scientific specification; application/resource/statistical sections are selected for the claim.

**Numbered section specification:** [Sections 48.1–48.9](section-plans/07-research.md#ch-reading-papers-building-evidence-and-reproducing-results).

**Planned sections:** Choose a claim that can be tested; Freeze sources, data, and revisions; Build a symbol and convention map; Trace equation and assumption dependencies; Construct an independent reference; Separate sources of error; Design and record the experiment; Investigate discrepancies and negative results; Report, review, and maintain a reproduction.

**Mathematical outcome:** Turn a source claim into a mathematical specification and distinguish proof, numerical evidence and empirical inference.

**Experiment and independent verification:** Build a versioned reproduction worksheet, environment record and discrepancy analysis before optimizing.

<span id="ch-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe"></span>
<span id="chapter-39-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe"></span>

### Chapter 49: Case Study: Molecular Hydrogen from Hamiltonian to Verified VQE

**Reading level:** Research capstone. **Entry guidance:** 4, 6, selected derivatives/energy sections of 23/25 and 48; 24 for the optimizer extension, not all embedding/learning topics.

**Numbered section specification:** [Sections 49.1–49.9](section-plans/07-research.md#ch-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe).

**Planned sections:** Specify the paper claim and corrected data; From the molecular model to a reduced Hamiltonian; Units, offsets, symmetries, and qubit labels; The ansatz from generator to gates; Observables, energy, and gradient; The exact sector minimum and global comparison; Reproduce the full geometry scan; Optimization and finite-shot extensions; Interpretation, discrepancy analysis, and research report.

**Mathematical outcome:** Derive the model and parameter conventions, amplitudes, observables, gradients and sector minimum.

**Experiment and independent verification:** Expand the H2 starter across 54 geometries with independent matrices, grid-error bounds, optimizers, sampling and provenance.

<span id="ch-case-study-logical-memory-and-error-correction-experiments"></span>
<span id="chapter-40-case-study-logical-memory-and-error-correction-experiments"></span>

### Chapter 50: Case Study: Logical Memory and Error-Correction Experiments

**Reading level:** Research capstone. **Entry guidance:** Selected noise, stabilizer/surface-code and research-method sections; exact dense/error enumeration for the small reference. Universal logical gates, factories and a later tableau simulator are not entry requirements.

**Numbered section specification:** [Sections 50.1–50.9](section-plans/07-research.md#ch-case-study-logical-memory-and-error-correction-experiments).

**Planned sections:** Select a source and freeze the logical-memory claim; Specify the code, circuit, and noise model; Derive syndromes and detection events; Define decoding and logical success; Build an exact small-instance reference; Design the stochastic experiment; Compare distances, rounds, and noise parameters; From memory evidence to resource implications; Write a reproducible correction-study report.

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

The numbered arrangement is a reference structure. The authoritative [19 learning paths](learning-paths.md) list exact sections, assumed earlier routes and all required preparation. They are generated from the same stable section records as this plan. Do not maintain a second, conflicting course sequence in prose.

The [435-section review ledger](section-review.md) records each section's direct prerequisites, core/advanced level and editorial disposition. Chapter prerequisite prose is entry guidance, not a requirement to complete every section of every listed chapter. Later specialized sections can have additional dependencies without blocking an earlier core task.

The opening route develops mathematics, pure states, tensor products, gates, measurement, entanglement, mixed states and basic computational resources. First algorithms then progress through oracle problems, search/phase-free estimation, Fourier/phase estimation, arithmetic and dynamics. Phase-based amplitude estimation is now 17.8, after its phase-estimation prerequisites; it no longer forces a return to Chapter 16. Pure-state no-cloning is now 4.7, after tensor products.

Fixed quantum kernels, trainable hybrid learning, basic compilation, simulation and hardware branches have separate entry contracts. A selected physical model is useful for a hardware-to-compiler project but is not required before learning basic program semantics or mapping on a supplied target. Logical-memory simulation does not require universal fault tolerance or magic-state factories. H2 VQE does not require every embedding or quantum-learning extension.

## Ownership and scope control

The [curriculum audit](curriculum-audit.md) owns the coverage, duplication and deliberate-exclusion matrices. Develop a recurring concept fully in its owning section; later applications give an exact pointer, recall the necessary statement and explain the new use. New derivations belong in the later section only when its assumptions or mathematical object actually change.

Chapter 7 uses marginal probabilities for no-signalling; Chapter 8 supplies the reduced-state proof. Chapter 19 supplies the adiabatic bridge. Graph-state and adaptive measurement-based gates are in 30.10 before photonic use. Chapter 33 states abstract resource parameters before platform chapters explain their origins. Experimental SPAM/randomized benchmarking belongs to 28, state/process reconstruction to 10, and simulator timing to 44.

The additions from this pass give scoped homes to entanglement swapping, channel metrics/process reconstruction, mixed-state entanglement, cryptographic no-go boundaries, Simon's algorithm, an Abelian hidden-subgroup/discrete-log bridge, qubitization, Hamiltonian promise/verification limits, experimental characterization, quantum LDPC codes and bosonic correction. Their scope is stated in the section targets; mentioning an advanced result does not promise a complete research monograph.

## Workload and publication architecture

The [seven-volume proposal](volume-plan.md) is the recommended packaging overlay. It preserves global chapter numbers, stable IDs and web links while placing Chapter 14 after the foundational sequence, Chapter 48 before the capstones, and 49/50 in their application volumes. Direct prerequisites fit the proposed volume and internal chapter order; no section requires a later volume.

The [proof-depth plan](proof-plan.md) replaces uniform page allowances with result-specific budgets. The reference argument now budgets **1,296–2,546 pages before shared appendices/front matter**; adding 24–40 pages per volume gives **1,464–2,826 pages**, excluding substantial shared appendices/solutions. These are editorial ranges, not measured typeset lengths. They do not authorize scope compression or imply a one-semester course.

The foundation/information split avoids a combined opening volume of up to 738 planned pages. Volumes follow coherent subjects: foundations; information; algorithms; hybrid scientific computing; noise/correction; physical realizations; programming/compilation/simulation. Select one complete learning route rather than reading every specialization in sequence. The detailed proposal specifies all chapter allocations, cross-volume imports and alternatives; final packaging needs reader/typesetting calibration.

## Architecture-first acceptance gates

A complete editorial architecture pass is recorded in the [review report](architecture-review.md): 50 chapter decisions, 435 section dispositions, 1,045 direct prerequisite edges and 19 checked routes. These checks establish record consistency and expose prerequisite burden; they do not prove the explanations teach successfully.

Before new body drafting:

1. Review the assigned central-result/proof obligations and exact source locators; transcribe/check the precise statements and deferred lemmas before acceptance.
2. Obtain specialist review of coverage, ownership and mathematical/physical assumptions; record the actual sections reviewed.
3. Test representative routes and bridge/transition specifications with target readers. Record the precise missing steps and required repairs.
4. Set workable page, example and substantial-problem budgets; resolve volume and course packaging.
5. Resolve findings and tag a versioned architecture baseline with a public change record.

**No new textbook body or depth-pilot drafting while these architecture gates remain open.** Existing three starter chapters remain available as evidence of the format. Source mapping, architectural repairs and validation design can continue; they do not constitute authorization to write new chapters. After the baseline, prioritize a continuous opening and selected complete routes, not isolated topical additions.

## Research anchors and source work

The [reading guide](references/reading-guide.md), [compilation/platform sources](references/compilation-and-platforms.md), [hybrid sources](references/hybrid-computing.md) and [systematic-review source notes](references/architecture-review.md) document consulted scope. Course outlines and paper abstracts support coverage comparisons; they do not certify proofs, API support or experimental results. Every authored result needs exact edition/revision and theorem/equation locators plus its independent verification plan.

The [H2 integral-to-reduced-model provenance plan](references/h2-provenance.md) now records nine checked stages and an independent 54-geometry, 324-coefficient reconstruction at published rounding precision. Original author integral files were not recovered. The [topological experimental evidence ledger](references/topological-experiments.md) selects nine claim-specific cases, including paired critique/reply and retraction records; the [full public argument audit](references/topological-dispute-review.md) now compares nine disputes across preprint, accepted-manuscript and public-rebuttal versions. Exact final-journal-reply matching and independent interpretation remain open. Chapter 50 now selects Fowler et al. v2, Section VII A/Fig. 5 for syndrome ambiguity; its finite memory benchmark is an explicitly labeled extension, not reproduction of the paper's threshold curves. A rounded small-model reproduction cannot stand in for all molecular data or a hardware experiment.

## Stable identifiers and history

Canonical records are book/curriculum.json and book/architecture-review.json. Run scripts/build_curriculum.py, scripts/review_curriculum.py and scripts/build_scholarly_plan.py to generate views; their --check options detect stale outputs and graph/route inconsistencies. IDs remain stable across display renumbering. A split or merge requires an explicit map, prerequisite/route updates and preserved or redirected public anchors.

The former 40-chapter/328-section plan lacked substantial hardware and compilation routes. The expanded 50-chapter/423-section plan received this full editorial pass and now has 435 sections. Historical design reviews remain records, not current allocations. Existing public section anchors are retained, including moved sections. Current starter homes are 6, 23 and 49; the published three-chapter PDF retains its own sample numbering and source/version provenance.
