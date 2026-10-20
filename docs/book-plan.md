# Full book plan

**Long-term curriculum revision: October 20, 2026.** Seven parts, 40 chapters and six appendices. This supersedes the 28-chapter outline. The [editorial charter](editorial-charter.md) records the author's aim: a rigorous, accessible modern classic that helps present and future learners enter the field.

This is a curriculum architecture, not a completed manuscript or a claim that every proposed experiment is supported. Three starter chapters currently exist, with intended homes in Chapters **6, 23 and 39**. The three-chapter PDF retains independent sample numbering and its published version.

## Audience, depth and reading levels

Entry readers need basic Python and introductory linear algebra. Foundations supply the quantum model and mathematical bridges; advanced chapters introduce additional probability, optimization, algebra and complexity prerequisites where needed. Readers should be able to reason, derive, implement, verify and critique a new calculation.

**Core** identifies conceptual foundations; **Advanced** adds demanding theory or specialization; **Research** integrates a scoped paper reproduction. A chapter may have a core narrative and advanced proof sections. These labels do not promise that all core chapters fit in one semester. A complete book supports several courses.

The theory determines the curriculum. A missing FlagQuantum API becomes a tracked implementation requirement through the [capability-gap workflow](implementation-roadmap.md). Authors may develop independent executable references while an upstream implementation is pending. Only actually executed, versioned FlagQuantum examples receive validated status.

## Section architecture and acceptance standard

Each chapter below specifies its section sequence, mathematical outcome and independent check. These are authoring targets, not claims of existing proofs or code.

1. Open with a concrete question, prerequisites and a prediction.
2. State definitions, physical postulates, access models and assumptions.
3. Give named results with their quantifiers and conditions. Prove central results at the declared level; identify deferred proof ingredients and exact sources.
4. Derive important intermediate steps and connect them to code, including indices, units, dimensions and normalization.
5. Analyze resources and error, including precision and success probability where relevant.
6. Verify small cases independently; include a counterexample or failure diagnosis that tests the assumptions.
7. End with conceptual, derivation/proof, implementation and transfer problems, plus sources and a recap.

Short recall prompts follow the [learning design](learning-design.md); substantial problems develop mathematical and research ability. Numerical agreement supplies evidence about implementation, not a proof of a general theorem. Every specialized chapter needs a reviewed primary-source map before drafting.


## Part 1. Foundations and Quantum Information Primitives

### Chapter 1: What Quantum Computing Computes

**Reading level:** Core. **Prerequisites:** Basic Python.

**Planned sections:** Problems and outputs; interference experiment; models, simulators and hardware; guide to the book.

**Mathematical outcome:** Derive one interference probability before introducing the general formalism.

**Experiment and independent verification:** Predict and verify a tiny circuit; explain why its simulation establishes no speedup.

### Chapter 2: Complex Vectors, Operators, and Numerical Reasoning

**Reading level:** Core. **Prerequisites:** 1; introductory linear algebra.

**Planned sections:** Complex inner products; adjoints and spectra; matrix functions; norms, conditioning and tolerances.

**Mathematical outcome:** Derive spectral reconstruction and matrix-exponential identities under stated assumptions.

**Experiment and independent verification:** Check residuals and conditioning with independent NumPy/PyTorch calculations.

### Chapter 3: Single-Qubit States and Rotations

**Reading level:** Core. **Prerequisites:** 2.

**Planned sections:** State and evolution postulates; relative and global phase; Bloch sphere; Pauli rotations; no-cloning.

**Mathematical outcome:** Derive rotations from their generators and prove the elementary no-cloning statement.

**Experiment and independent verification:** Compare matrices and circuit results, including phase-equivalent and distinguishable states.

### Chapter 4: Composite Systems, Tensor Products, and Qubit Ordering

**Reading level:** Core. **Prerequisites:** 2, 3.

**Planned sections:** Tensor products; register labels and basis indices; local operations; subsystem permutations.

**Mathematical outcome:** Derive the basis-index map and local-operator action on an arbitrary register.

**Experiment and independent verification:** Compare two- and three-qubit operations with Kronecker products and deliberately changed qubit ordering.

### Chapter 5: Gates, Reversible Computation, and Circuit Synthesis

**Reading level:** Core. **Prerequisites:** 3, 4.

**Planned sections:** Gate composition; controlled operations; reversible Boolean computation; universality; approximation and synthesis cost.

**Mathematical outcome:** Derive controlled-gate matrices and a small reversible construction; state the approximation model.

**Experiment and independent verification:** Verify complete unitaries and account for ancillas and inverse operations.

### Chapter 6: Measurement, Expectation Values, and Statistical Estimation

**Reading level:** Core. **Prerequisites:** 3–5.

**Planned sections:** Born rule; conditional states and instruments; generalized measurements; observables; variance and confidence intervals.

**Mathematical outcome:** Derive projective and generalized-measurement probabilities and finite-shot estimator uncertainty.

**Experiment and independent verification:** Extend the measurement starter; test conditional states and empirical coverage over repeated seeded trials.

### Chapter 7: Entanglement and Quantum Information Protocols

**Reading level:** Core. **Prerequisites:** 4–6.

**Planned sections:** Schmidt decomposition; Bell correlations; teleportation; superdense coding; no-signalling.

**Mathematical outcome:** Derive Schmidt structure and all conditional branches of teleportation.

**Experiment and independent verification:** Verify corrections for arbitrary input states; inspect the receiver's unconditioned reduced state.

### Chapter 8: Density Matrices, Reduced States, and Purification

**Reading level:** Core. **Prerequisites:** 2, 4, 6, 7.

**Planned sections:** Ensembles; density operators; partial trace; purification; improper and proper mixtures.

**Mathematical outcome:** Derive mixed-state expectations and the relation between Schmidt coefficients and reduced spectra.

**Experiment and independent verification:** Check trace, positivity and subsystem states against explicit index sums.

## Part 2. Quantum Information: Channels, Inference, and Communication

### Chapter 9: Quantum Channels and Their Representations

**Reading level:** Core. **Prerequisites:** 8.

**Planned sections:** Completely positive maps; Kraus representation; Stinespring dilation; Choi representation; channel composition.

**Mathematical outcome:** Establish finite-dimensional representation equivalences and explain why positivity alone is insufficient.

**Experiment and independent verification:** Translate one small channel among representations; test complete positivity, trace preservation and environment dilation.

### Chapter 10: Distinguishability, Fidelity, and Quantum State Inference

**Reading level:** Core. **Prerequisites:** 6, 8, 9.

**Planned sections:** Trace distance; fidelity conventions; operational discrimination; tomography; measurement grouping; classical shadows.

**Mathematical outcome:** Derive binary discrimination and simple estimation bounds; state the assumptions of shadow guarantees.

**Experiment and independent verification:** Compare independently reconstructed states and estimator errors; expose incomplete-measurement counterexamples.

### Chapter 11: Entropy, Relative Entropy, and Information Processing

**Reading level:** Core with advanced proofs. **Prerequisites:** 8–10.

**Planned sections:** Shannon and von Neumann entropy; relative entropy; mutual information; data processing; strong subadditivity.

**Mathematical outcome:** Prove accessible special cases and selected central results; identify the ingredients and source of deferred general proofs.

**Experiment and independent verification:** Compute small exact and commuting examples and counterexamples to invalid entropy intuitions.

### Chapter 12: Compression, Entanglement, and Communication Limits

**Reading level:** Advanced. **Prerequisites:** 7–11.

**Planned sections:** Typicality; Schumacher compression; entanglement concentration; Holevo bound; channel-capacity formulations.

**Mathematical outcome:** Derive a finite-block compression example and state coding theorems with their operational assumptions.

**Experiment and independent verification:** Compare small block encodings and success/error tradeoffs; distinguish finite demonstrations from asymptotic proofs.

### Chapter 13: Quantum Cryptography and Security Reasoning

**Reading level:** Advanced. **Prerequisites:** 6–12.

**Planned sections:** BB84; parameter estimation; adversarial models; privacy amplification; finite-size and composable security.

**Mathematical outcome:** Derive an intercept-resend example and the logic of a scoped security argument; delimit the full security theorem.

**Experiment and independent verification:** Run a toy protocol with confidence bounds; explain why a low observed error rate alone does not establish security.

## Part 3. Quantum Algorithms and Computational Resources

### Chapter 14: Computational Models, Complexity, and Quantum Advantage

**Reading level:** Core. **Prerequisites:** 4–6.

**Planned sections:** Circuit families; reversible models; BQP and promise problems; query versus gate cost; precision; classical baselines.

**Mathematical outcome:** Relate input/output access assumptions to a complete resource expression.

**Experiment and independent verification:** Audit examples including state preparation, oracle synthesis, repetitions and readout; avoid simulator-time speedup claims.

### Chapter 15: Interference, Oracles, and Phase Kickback

**Reading level:** Core. **Prerequisites:** 5, 14.

**Planned sections:** Reversible oracles; phase kickback; Deutsch-Jozsa; Bernstein-Vazirani; oracle promises.

**Mathematical outcome:** Derive the phase-oracle action and complete output distributions.

**Experiment and independent verification:** Check truth tables and gate-level oracles against dense permutation and diagonal references.

### Chapter 16: Grover Search, Amplitude Amplification, and Estimation

**Reading level:** Core with advanced extensions. **Prerequisites:** 6, 14, 15; revisit after 17.

**Planned sections:** Two-dimensional geometry; iteration counts; general amplification; amplitude estimation; query bounds.

**Mathematical outcome:** Derive the success curve and a scoped estimation error/query relation.

**Experiment and independent verification:** Compare complete distributions with analytic predictions and ordinary Monte Carlo under the same access assumptions.

### Chapter 17: Fourier Transforms and Quantum Phase Estimation

**Reading level:** Core. **Prerequisites:** 4–6, 14, 15.

**Planned sections:** Discrete Fourier transform; QFT factorization; inverse and approximate QFT; exact/off-grid phase estimation.

**Mathematical outcome:** Derive QFT structure and finite-precision phase-estimation probabilities.

**Experiment and independent verification:** Compare every small basis input and off-grid output distribution with dense references.

### Chapter 18: Period Finding, Factoring, and Algorithmic Arithmetic

**Reading level:** Advanced. **Prerequisites:** 5, 14, 17.

**Planned sections:** Order finding; modular arithmetic; continued fractions; success probabilities; arithmetic and synthesis costs.

**Mathematical outcome:** Derive the reduction from factoring to order finding and its classical postprocessing conditions.

**Experiment and independent verification:** Factor tiny examples using explicit modular arithmetic; avoid precompiled circuits that assume the answer.

### Chapter 19: Hamiltonian Simulation and Error Bounds

**Reading level:** Core with advanced extensions. **Prerequisites:** 2, 5, 14, 17.

**Planned sections:** Pauli decompositions; first/second-order formulas; commutator error; sparse and oracle models; precision dependence.

**Mathematical outcome:** Derive product formulas and a finite-system error bound; prepare the transition to signal processing.

**Experiment and independent verification:** Compare with matrix exponentials and verify error scaling against an actual bound.

### Chapter 20: Block Encodings and Quantum Linear Algebra

**Reading level:** Advanced. **Prerequisites:** 2, 5, 14, 17, 19.

**Planned sections:** Normalization and access models; exact small block encodings; LCU; postselection; linear-system conditioning.

**Mathematical outcome:** Construct a block encoding and derive normalization, success probability and condition-number dependence.

**Experiment and independent verification:** Check encoded blocks numerically and include state preparation/readout in the resource analysis.

### Chapter 21: Quantum Signal Processing and Singular Value Transformation

**Reading level:** Advanced. **Prerequisites:** 16, 19, 20.

**Planned sections:** SU(2) polynomial sequences; parity and boundedness; phase sequences; QSVT; spectral filtering and simulation.

**Mathematical outcome:** Derive low-degree constructions, state a precise transformation theorem and prove a selected application.

**Experiment and independent verification:** Compare transformed scalar values and small matrix singular values with polynomial targets; report synthesis and approximation errors.

### Chapter 22: Quantum Walks, Lower Bounds, and Algorithm Design

**Reading level:** Advanced. **Prerequisites:** 14–21.

**Planned sections:** Walk constructions; search and hitting problems; polynomial method; query lower bounds; algorithm selection.

**Mathematical outcome:** Analyze a small walk and derive a representative lower bound under an explicit oracle model.

**Experiment and independent verification:** Compare walk evolution with an independent transition/spectral construction and identify inaccessible speedup assumptions.

## Part 4. Variational and Differentiable Quantum Computing

### Chapter 23: Parameterized Circuits, Quantum Gradients, and Differentiation

**Reading level:** Core. **Prerequisites:** 2–6; elementary calculus.

**Planned sections:** Observable-valued models; generator spectra; parameter shift; shared parameters; adjoint differentiation; autograd contracts.

**Mathematical outcome:** Derive spectral shift rules, normalization changes and parameter-reuse chain rules; analyze execution and memory costs.

**Experiment and independent verification:** Expand the gradient starter with analytic, dense, shifted and autograd checks for multiple parameter occurrences.

### Chapter 24: Optimization, Geometry, and Trainability

**Reading level:** Advanced. **Prerequisites:** 10, 14, 23.

**Planned sections:** Exact and stochastic losses; optimizer diagnostics; quantum geometric tensor; natural gradient; barren plateaus; noise.

**Mathematical outcome:** Derive a small metric and gradient-variance example; state the ensemble assumptions of trainability results.

**Experiment and independent verification:** Separate convergence, expressivity and sampling effects; compare initializations and controlled classical baselines.

### Chapter 25: Variational Simulation, Chemistry, and Ground-State Problems

**Reading level:** Core application. **Prerequisites:** 8, 14, 19, 23.

**Planned sections:** Variational principle; fermions and Jordan-Wigner mapping; symmetries; ansatz selection; measurement allocation; dynamics.

**Mathematical outcome:** Prove the energy bound and derive a small occupation-to-qubit Hamiltonian with units and offsets.

**Experiment and independent verification:** Compare independent fermionic/qubit matrices and exact diagonalization; report all model and estimator errors.

### Chapter 26: QAOA, Quantum Optimization, and Classical Comparisons

**Reading level:** Advanced application. **Prerequisites:** 14–16, 23, 24.

**Planned sections:** Objective-to-Hamiltonian mapping; mixers; constrained spaces; depth; approximation quality; sampling and optimization cost.

**Mathematical outcome:** Derive MaxCut and one low-depth result under explicit graph and sign conventions.

**Experiment and independent verification:** Compare against exhaustive solutions and meaningful classical heuristics without inferring advantage from tiny instances.

### Chapter 27: Quantum Learning, Kernels, and Hybrid Models

**Reading level:** Advanced application. **Prerequisites:** 10, 14, 23, 24; basic machine learning.

**Planned sections:** Data access and encoding; hybrid chain rule; quantum kernels; generalization; classical simulability and baselines.

**Mathematical outcome:** Derive kernel/feature-map relations and joint gradients; state learning-task and data-access assumptions.

**Experiment and independent verification:** Use held-out evaluation, classical baselines and end-to-end gradient checks; include encoding and measurement costs.

## Part 5. Noise, Error Correction, and Fault-Tolerant Computation

### Chapter 28: Noise, Open Systems, and Error Mitigation

**Reading level:** Core. **Prerequisites:** 8–10; 19 for dynamics.

**Planned sections:** Kraus noise; Lindblad dynamics; trajectories; correlated noise; calibration; mitigation and its overhead.

**Mathematical outcome:** Derive amplitude damping and one master equation; analyze the bias/variance tradeoff of a mitigation example.

**Experiment and independent verification:** Compare density evolution with an independent solver and trajectory averages; test positivity, trace and estimator uncertainty.

### Chapter 29: Quantum Error Correction: Conditions and Recovery

**Reading level:** Core. **Prerequisites:** 7–10, 28.

**Planned sections:** Quantum obstacles; repetition codes; error discretization; Knill-Laflamme conditions; recovery and logical information.

**Mathematical outcome:** Prove the correction condition in a finite example and explain preservation of logical information by syndrome measurement.

**Experiment and independent verification:** Enumerate errors and verify recovery on arbitrary encoded superpositions, including coherent error combinations.

### Chapter 30: Stabilizer Codes, Logical Operators, and Decoding

**Reading level:** Core with advanced extensions. **Prerequisites:** 5–8, 29; binary linear algebra.

**Planned sections:** Pauli symplectic representation; stabilizer groups; CSS construction; distance; logical operators; decoder interfaces.

**Mathematical outcome:** Derive a code's syndrome map, logical operators and distance; connect binary algebra to quantum operators.

**Experiment and independent verification:** Compare stabilizer calculations with dense small-code references and injected-error enumeration.

### Chapter 31: Surface Codes and Repeated Syndrome Measurements

**Reading level:** Advanced. **Prerequisites:** 28–30.

**Planned sections:** Lattice checks; boundaries; syndrome circuits; measurement faults; detection events; space-time decoding; logical failure.

**Mathematical outcome:** Derive checks and detection-event patterns for a small patch and repeated rounds.

**Experiment and independent verification:** Verify hand-enumerated faults before Monte Carlo; report noise model, decoder, distance, uncertainty and finite-size limits.

### Chapter 32: Fault-Tolerant Gates and Universal Logical Computation

**Reading level:** Advanced. **Prerequisites:** 5, 18, 28–31.

**Planned sections:** Fault propagation; transversal operations; threshold logic; lattice surgery; code deformation; magic states and distillation.

**Mathematical outcome:** Derive a fault-propagation example and a small distillation/rejection calculation; state threshold assumptions and explain proof structure.

**Experiment and independent verification:** Compare ideal logical actions with fault-injected circuits and count accepted outputs, logical errors and consumed resources.

### Chapter 33: From Logical Algorithms to Physical Resource Estimates

**Reading level:** Advanced synthesis. **Prerequisites:** 14, 18–21, 28–32.

**Planned sections:** Logical gate synthesis; T count/depth; factories; error budgets; code distance; physical qubits; runtime and sensitivity.

**Mathematical outcome:** Derive a complete small cost model with a target success probability and explicit architecture/noise assumptions.

**Experiment and independent verification:** Recompute resource estimates under changing assumptions; separate symbolic estimates from measured device performance.

## Part 6. Classical Simulation and the Boundary of Tractability

### Chapter 34: Exact Simulation, Tensor Execution, and Numerical Reliability

**Reading level:** Core. **Prerequisites:** 2, 4–6, 8, 14, 23.

**Planned sections:** Statevector and density evolution; tensor-axis operations; precision; memory; batching; differentiation; parallel execution.

**Mathematical outcome:** Derive local-gate tensor contractions and storage/time costs, including communication assumptions.

**Experiment and independent verification:** Build an independent minimal executor; compare states, channels and gradients before benchmarking.

### Chapter 35: Stabilizer Simulation, Magic, and Classical Simulability

**Reading level:** Advanced. **Prerequisites:** 14, 30, 34.

**Planned sections:** Tableau updates; Clifford circuits; adaptive measurements; Gottesman-Knill; non-Clifford resources.

**Mathematical outcome:** Derive tableau updates and explain the assumptions behind efficient stabilizer simulation.

**Experiment and independent verification:** Compare tableau and dense results, including measurement branches; trace the resource impact of non-Clifford operations.

### Chapter 36: Matrix Product States, Entanglement, and Truncation

**Reading level:** Advanced. **Prerequisites:** 2, 4, 7, 8, 10, 34.

**Planned sections:** Successive SVD; canonical forms; gate updates; bond dimensions; entanglement; truncation bounds.

**Mathematical outcome:** Derive MPS construction and discarded-weight error relations with normalization assumptions.

**Experiment and independent verification:** Compare with exact states while varying bonds and gate geometry; report accumulated error and cost.

### Chapter 37: Tensor Networks, Contraction, and Hybrid Simulation Strategies

**Reading level:** Advanced. **Prerequisites:** 14, 34, 36.

**Planned sections:** Circuit tensors; contraction paths; intermediate sizes; slicing; distributed contraction; amplitudes versus full states.

**Mathematical outcome:** Derive a circuit contraction and predict path-dependent intermediate memory.

**Experiment and independent verification:** Check independent contractions, profile declared workloads and explain when simulation becomes intractable.

## Part 7. From Papers to Reproducible Research

### Chapter 38: Reading Papers, Building Evidence, and Reproducing Results

**Reading level:** Core research method. **Prerequisites:** 4, 6, 10, 14; application-specific prerequisites.

**Planned sections:** Source revisions; symbols and assumptions; equation dependencies; units; independent references; uncertainty; resource records.

**Mathematical outcome:** Turn a source claim into a mathematical specification and distinguish proof, numerical evidence and empirical inference.

**Experiment and independent verification:** Build a versioned reproduction worksheet, environment record and discrepancy analysis before optimizing.

### Chapter 39: Case Study: Molecular Hydrogen from Hamiltonian to Verified VQE

**Reading level:** Research capstone. **Prerequisites:** 23–25, 38.

**Planned sections:** Corrected paper data; reduction and qubit mapping; ansatz; closed-form minimum; full curve; optimization; shot uncertainty.

**Mathematical outcome:** Derive the model and parameter conventions, amplitudes, observables, gradients and sector minimum.

**Experiment and independent verification:** Expand the H2 starter across 54 geometries with independent matrices, grid-error bounds, optimizers, sampling and provenance.

### Chapter 40: Case Study: Logical Memory and Error-Correction Experiments

**Reading level:** Research capstone. **Prerequisites:** 28–33, 35, 38.

**Planned sections:** Paper selection and claim specification; repeated syndrome model; decoder; logical observable; scaling; failure analysis.

**Mathematical outcome:** Derive the selected code/model's detection and logical-failure definitions before reproducing a claim.

**Experiment and independent verification:** Select and document a primary source before implementation; compare tiny exact references and stochastic results with uncertainty. No hardware reproduction is implied.


## Appendices and companion laboratories

- **A. Mathematical Reference and Probability:** linear algebra, asymptotics, concentration, selected algebra and proof tools.
- **B. Matrix Calculus and Differentiation Conventions:** complex derivatives, adjoints and PyTorch contracts.
- **C. FlagQuantum Runtime Contracts and Interoperability:** supported releases, compilation, ordering and result semantics.
- **D. Experiment Records and Benchmark Protocols:** manifests, uncertainty, comparison workloads and reproducibility.
- **E. Platform Laboratories:** installation, accelerators, distributed execution and hardware access.
- **F. Problems, Selected Solutions and Reproduction Worksheets:** stable problem identifiers and reader/teacher support.

The bibliography, symbol index, glossary, errata and acknowledgements are separate back matter. Hardware credentials are optional for the core learning route. Essential explanations, proofs and answers remain usable offline in print.


## Dependencies and course routes

Prerequisite lists are conceptual: for example, Chapter 16's amplitude-amplification material can precede Chapter 17, and its phase-estimation-based extension follows it. Advanced results should introduce missing tools locally or point to an explicit prerequisite section.

| Route | Suggested material | Intended outcome |
|---|---|---|
| First course | 1–8; selected 9–10 and 14–17; introduction to 28–30; a small project | Understand states, circuits, information, algorithmic assumptions and correction |
| Information course | 7–13, with the needed foundations | Understand channels, inference, entropy, communication and security assumptions |
| Modern algorithms | 14–22, supported by 2–6 and 9–10 | Derive algorithms and assess their complete costs and assumptions |
| Variational and learning | 23–27, with 10, 14 and selected 19/28 | Differentiate and evaluate models with statistical and classical baselines |
| Error correction and fault tolerance | 28–33, with 7–10 and selected algorithms | Move from recovery conditions to logical operations and physical resource budgets |
| Simulation | 30, 34–37, supported by 2, 4, 7–10, 14 and 23 | Understand exact and structured simulation, approximation and tractability |
| Research practice | 38 followed by 39 or 40, after its prerequisites | Translate a scoped paper claim into independently checked evidence |

A 14-week introduction should select sections rather than compress every route into one semester. Later courses and independent reading supply the advanced theory. No reading route assumes access to a paid cloud or large accelerator.

## Writing order and review gates

1. Complete a coherent opening block: Chapters 1–8 and its problems.
2. Produce three depth pilots: measurement (6), differentiation (23), and correction conditions (29). Test whether the formula-to-code method handles postulates, spectral reasoning and a substantial theorem.
3. Establish channels/inference and computational resources (9–10, 14), then the first algorithm sequence (15–19).
4. Expand the first research route (23–25, 38–39) and complete the information-theory sequence (11–13).
5. Build the modern algorithm and logical-computing routes (20–22, 28–33) with primary-source and specialist review.
6. Complete learning/optimization applications, simulation and the second capstone (24, 26–27, 34–37, 40), plus exercises and solution review.
7. Pilot full course routes with readers and instructors; resolve mathematical, pedagogical and executable-example findings before freezing an edition.

Priority is a writing sequence, not a declaration that other subjects are less important. References and capability investigations can proceed while earlier chapters are written.

## Depth and scope commitments

Quantum information, modern algorithms and fault-tolerant computation are substantive parts of the book. Channel representations, information inequalities, coding/security theorem statements, QSP/QSVT and fault-tolerance arguments must receive meaningful development. Selected long or highly specialized proofs can be advanced readings with an explicit proof map and sources; they must not be replaced by a successful numerical experiment.

The book is finite. It need not survey every hardware modality, algorithm or code family. Topic inclusion follows durable explanatory value, connection to the core and teaching evidence; an emerging topic can first enter a dated research laboratory. A claim of current advantage or device performance needs dated evidence.

## Research anchors and remaining source work

These primary works are starting points for the added scope, not completed chapter-level source reviews:

- [Gilyén et al., QSVT (STOC 2019)](https://arxiv.org/abs/1806.01838): polynomial transformations of block-encoded matrices, algorithmic applications and limits.
- [Fowler et al., surface codes, v2 (2012)](https://arxiv.org/abs/1208.0928v2): stabilizers, logical operations and a resource-oriented surface-code construction. Treat its architectural estimates as historical model-specific results.
- [Huang, Kueng and Preskill, classical shadows (2020)](https://arxiv.org/abs/2002.08953): property estimation with a measurement-dependent statistical guarantee.

Use the [reading guide](references/reading-guide.md) for foundational texts. Before authoring a specialized section, record the exact result, source version, proof dependencies, applicability conditions and an independent verification plan. Later developments need their own source review.

## Relation to earlier plans and samples

The earlier [Nielsen–Chuang](references/nielsen-chuang-design-review.md) and [Quantum Country](references/quantum-country-design-review.md) reviews remain historical design records. Their 28-chapter allocation is superseded here; their pedagogical findings still apply.

| Existing artifact | Intended home | Required expansion |
|---|---|---|
| Measurement starter | Chapter 6 | Conditional/generalized measurements, estimators and statistical reasoning |
| Gradient starter | Chapter 23 | Spectra, shared parameters, adjoint methods, cost and substantial problems |
| Hydrogen VQE starter | Chapter 39 | Hamiltonian construction, complete experiments and scientific interpretation |

Published sample editions retain their own numbering and pinned source revision. Expanding this plan does not change the validated scope of those editions.
