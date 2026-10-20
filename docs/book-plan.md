# Full book plan

**Reference-informed revision: October 20, 2026.** This editorial plan supersedes the initial feature-oriented outline. It follows a review of the preface, complete contents and selected instructional passages in Nielsen and Chuang; it does not claim a cover-to-cover review. See the [design review and source locators](references/nielsen-chuang-design-review.md).

## Audience and learning outcomes

Readers know basic Python and introductory linear algebra; the first chapter provides motivation before the mathematical review. Elementary calculus becomes necessary in Chapter 16 and neural-network knowledge in Chapter 18. No previous quantum mechanics course is assumed for the core route.

The outcome is the ability to understand a quantum calculation, derive its assumptions and formulas, implement a small model, and verify a carefully scoped paper reproduction. A successful program is one piece of evidence; mathematical arguments and resource analysis remain essential.

## Teaching design

1. Begin each chapter with a physical or computational question and a small worked example.
2. State the relevant definitions, postulates and assumptions, then derive the general result with explicit intermediate steps.
3. Pair important formulas with implementation expressions and independently checked small cases.
4. Insert short checkpoints where new notation, a convention or an inference is introduced.
5. End with a recap, derivation problems, programming laboratories and a deeper investigation.
6. Provide precise source locators, a history/further-reading note and explicit scope limits.

Installation and exhaustive API documentation belong in companion material. Code should serve a conceptual argument, while independent references distinguish mathematical correctness from framework behavior. The first starters target FlagQuantum 0.3.1; future examples need an explicit supported release and must not silently depend on development-only APIs.

## Part I. Foundations and Quantum Information Primitives

### Chapter 1: What Quantum Computing Computes: A First Formula-to-Code Experiment

**Role:** Core; opening motivation. **Prerequisites:** Basic Python; no quantum background.

**Learning focus:** Problems, states, transformations and observations; the distinction between a mathematical model, a simulator and physical hardware.

**Derivation:** Walk through one small interference experiment in informal notation, explain the question and interpretation, and identify the mathematical tools to be developed later.

**Experiment and verification:** Run a tiny introductory experiment with a supplied environment, predict its outcomes and show what the result does and does not establish. The chapter is a map of the book, not a prerequisite-heavy survey.

### Chapter 2: Complex Vectors, Operators, and Numerical Checks

**Role:** Core. **Prerequisites:** Python; introductory linear algebra.

**Learning focus:** Complex inner products, adjoints, eigenvalues, matrix exponentials and floating-point tolerances.

**Derivation:** Derive normalization and spectral decomposition for small Hermitian matrices.

**Experiment and verification:** Build independent PyTorch/NumPy reference calculations; check reconstruction and residual norms.

### Chapter 3: Single-Qubit States and Rotations

**Role:** Core. **Prerequisites:** 2.

**Learning focus:** Amplitudes, global and relative phase, Bloch coordinates and Pauli rotations. State the finite-dimensional state and closed-system evolution postulates, and distinguish global from relative phase.

**Derivation:** Derive the rotation matrices and their action on an arbitrary normalized state. Include the elementary no-cloning argument with its assumptions.

**Experiment and verification:** Compare explicit matrices with FlagQuantum rotations, including zero-angle, inverse and phase-equivalence checks.

### Chapter 4: Composite Systems, Tensor Products, and Qubit Ordering

**Role:** Core. **Prerequisites:** 2, 3.

**Learning focus:** Tensor-product spaces, registers, computational basis indices and subsystem labels.

**Derivation:** Derive the bit-string-to-index map and the action of an operator on a selected wire.

**Experiment and verification:** Check two- and three-qubit circuits against Kronecker products and deliberately swapped wire conventions.

### Chapter 5: Quantum Gates and Circuit Construction

**Role:** Core. **Prerequisites:** 3, 4.

**Learning focus:** Single-qubit gates, controlled gates, composition, inversion and basic decompositions. Introduce universality and approximation at a stated, limited level.

**Derivation:** Derive circuit matrices and distinguish call order from matrix multiplication order.

**Experiment and verification:** Build a Bell circuit and a small reversible circuit; compare complete states or unitaries with dense references.

### Chapter 6: Measurement, Expectation Values, and Sampling

**Role:** Core; starter available. **Prerequisites:** 3, 4, 5.

**Learning focus:** Born probabilities, observable expectations, variance and finite-shot estimators. State measurement probabilities and conditional post-measurement states; treat generalized measurements as a deeper section.

**Derivation:** Derive probabilities and expectations for a rotated qubit, then connect variance to estimator uncertainty.

**Experiment and verification:** Extend the existing exact-expectation starter with seeded shot experiments and a comparison of sampling error versus shot count.

### Chapter 7: Entanglement and Quantum Information Protocols

**Role:** Core. **Prerequisites:** 4, 5, 6.

**Learning focus:** Product versus entangled pure states, Bell states, correlations, teleportation and superdense coding.

**Derivation:** Start from a Bell experiment, derive a pure-state Schmidt decomposition and work through the four conditional branches of teleportation.

**Experiment and verification:** Verify each protocol branch and its conditional correction against the input state; distinguish classical communication from signalling by entanglement alone. Use explicit reference calculations where a runtime lacks a needed operation.

### Chapter 8: Density Matrices, Reduced States, and Purification

**Role:** Core. **Prerequisites:** 2, 4, 6, 7.

**Learning focus:** Statistical ensembles, density operators, partial traces, reduced states and purification.

**Derivation:** Use two preparations with the same one-qubit statistics to motivate density matrices; derive expectation values, reduced states and the relation to Schmidt coefficients.

**Experiment and verification:** Compare pure and mixed preparations with identical selected measurement statistics; check positivity, unit trace, reduced states and expectation agreement.

## Part II. Computational Models and Quantum Algorithms

### Chapter 9: Computational Models, Resource Accounting, and Quantum Advantage

**Role:** Core. **Prerequisites:** 1, 4, 5, 6.

**Learning focus:** Reversible classical circuits, input size, circuit families, oracle access, gate count, shots, precision and classical baselines.

**Derivation:** State the distinction between query complexity and complete computational cost; introduce the meaning and limits of asymptotic speedup claims.

**Experiment and verification:** Count resources for small classical and quantum tasks including oracle construction and readout. Identify invalid comparisons caused by excluding data preparation or comparing simulator wall time with a hardware algorithmic bound.

### Chapter 10: Interference, Oracles, and Phase Kickback

**Role:** Core. **Prerequisites:** 4, 5, 6, 9.

**Learning focus:** Interference as a computational resource; reversible functions, phase oracles and query models.

**Derivation:** Derive phase kickback and a small Deutsch-Jozsa example, stating the oracle promise and query cost.

**Experiment and verification:** Enumerate truth tables and compare gate-level oracles with their dense diagonal or permutation matrices.

### Chapter 11: Grover Search and Amplitude Amplification

**Role:** Core. **Prerequisites:** 6, 9, 10.

**Learning focus:** Reflections, marked subspaces, iteration counts and success probabilities.

**Derivation:** Reduce Grover iteration to a two-dimensional rotation and derive the ideal success curve.

**Experiment and verification:** Run small searches with different numbers of marked states; compare every iteration with the analytic formula and count oracle calls.

### Chapter 12: The Quantum Fourier Transform

**Role:** Core. **Prerequisites:** 4, 5, 10.

**Learning focus:** Discrete Fourier phases, controlled rotations, inverse transforms and output reversal.

**Derivation:** Derive the product representation of the QFT and the role of final wire swaps.

**Experiment and verification:** Compare the circuit with the dense Fourier matrix for each basis input and quantify a small approximate-QFT error.

### Chapter 13: Quantum Phase Estimation and Algorithmic Cost

**Role:** Core. **Prerequisites:** 6, 9, 10, 12.

**Learning focus:** Eigenphases, controlled powers, finite precision and the connection to factoring.

**Derivation:** Derive exact-grid outcomes and the off-grid probability distribution; distinguish query cost from gate synthesis cost.

**Experiment and verification:** Estimate phases of a known small unitary, compare the full distribution and explain what changes when the input is not an eigenstate.

### Chapter 14: Hamiltonian Simulation and Product Formulas

**Role:** Extension. **Prerequisites:** 2, 5, 13.

**Learning focus:** Pauli expansions, time evolution, noncommuting terms and product-formula error.

**Derivation:** Derive first-order and symmetric second-order product formulas for a small Hamiltonian.

**Experiment and verification:** Compare decomposed evolution with a dense matrix exponential; measure error as the time step decreases without claiming general scalability.

## Part III. Variational and Differentiable Quantum Computing

### Chapter 15: Parameterized Circuits and Observable Design

**Role:** Core. **Prerequisites:** 5, 6; 8 for mixed-state extensions.

**Learning focus:** Trainable angles, data-dependent angles, Pauli sums, batch dimensions and ansatz structure.

**Derivation:** Express a circuit model as an expectation-valued function and identify all parameter occurrences.

**Experiment and verification:** Build a batched model and verify each batch element and Pauli term against separate scalar and dense calculations.

### Chapter 16: Quantum Gradients and Automatic Differentiation

**Role:** Core; starter available. **Prerequisites:** 2, 3, 6, 15; elementary calculus.

**Learning focus:** Autograd, parameter shift, generator spectra, shared parameters and finite differences.

**Derivation:** Derive the single-Pauli shift rule, its normalization changes and the chain rule for reused parameters.

**Experiment and verification:** Extend the existing gradient starter with independent analytic, dense-matrix and shifted-execution checks; report execution cost.

### Chapter 17: Loss Functions, Optimization, and Training Diagnostics

**Role:** Core. **Prerequisites:** 15, 16.

**Learning focus:** Scalar losses, optimizer state, initialization, local minima, gradient noise and convergence diagnostics. Introduce trainability and gradient concentration as a scoped extension, without treating small random-circuit plots as a general barren-plateau proof.

**Derivation:** Derive a small loss and its gradient, and distinguish exact-expectation from finite-shot optimization.

**Experiment and verification:** Train a small circuit with PyTorch, log post-update losses, and compare final results with an analytic or exhaustive reference.

### Chapter 18: Hybrid Classical-Quantum Models

**Role:** Core application. **Prerequisites:** 15, 16, 17; basic neural networks.

**Learning focus:** Classical preprocessing, quantum layers, output heads and end-to-end differentiation.

**Derivation:** Derive the chain rule across the classical and quantum boundary and state feature and output dimensions.

**Experiment and verification:** Train a small hybrid model with a classical baseline and held-out evaluation; verify gradients through both components.

### Chapter 19: Variational Algorithms and Molecular Energy Problems

**Role:** Core application. **Prerequisites:** 2, 4, 6, 15, 16, 17.

**Learning focus:** The variational principle, Hamiltonian measurement, ansatz choice and small molecular models.

**Derivation:** Prove the energy upper bound under its assumptions and derive a weighted Pauli objective; introduce a small fermion-to-qubit mapping.

**Experiment and verification:** Check energies against exact diagonalization and a tiny occupation-basis Hamiltonian; separate ideal VQE, shot estimates and optimizer behavior.

### Chapter 20: QAOA and Combinatorial Optimization

**Role:** Application and independent project. **Prerequisites:** 5, 6, 9, 10, 15, 16, 17.

**Learning focus:** Graph objectives, cost and mixer Hamiltonians, alternating circuits and sampled solutions.

**Derivation:** Translate a small MaxCut objective into a Hamiltonian and derive the alternating-unitary conventions before selecting a reference paper.

**Experiment and verification:** Compare sampled cut values and optimized expectations with exhaustive classical enumeration. Require a source/version record and independent checks; do not infer quantum advantage from a small example.

## Part IV. Noise, Quantitative Comparisons, and Error Correction

### Chapter 21: Noise and Open-System Simulation

**Role:** Core extension. **Prerequisites:** 6, 8; 14 for continuous-time extensions.

**Learning focus:** Kraus channels, density-matrix evolution, trajectories and Lindblad dynamics.

**Derivation:** Derive a small amplitude-damping example and a simple master-equation evolution.

**Experiment and verification:** Compare against independent density-matrix evolution; check trace, positivity, limiting cases and stochastic uncertainty where applicable.

### Chapter 22: State Distances, Fidelity, and Introductory Quantum Information

**Role:** Core measurement and validation language. **Prerequisites:** 2, 6, 7, 8.

**Learning focus:** Classical distribution distance, quantum trace distance, fidelity conventions, distinguishability and elementary Shannon/von Neumann entropy.

**Derivation:** Motivate each measure with a concrete comparison; derive the pure-state case, the commuting-state reduction and simple entropy examples.

**Experiment and verification:** Compare a phase-shifted state, a mixed state and a noisy state with appropriate metrics. Verify analytic limiting cases and explain why selected measurement probabilities cannot certify arbitrary state equivalence. General channel capacities and advanced entropy inequalities remain further reading.

### Chapter 23: Quantum Error Correction and Syndrome Experiments

**Role:** Extension. **Prerequisites:** 4, 5, 6, 7, 8, 21; 22 for quantitative comparisons.

**Learning focus:** Parity checks, stabilizers, syndrome extraction, decoding and logical errors. Explain the distinction between ideal recovery and fault-tolerant operations.

**Derivation:** Derive a repetition-code syndrome table and introduce the stabilizer conditions for a quantum code. Motivate the quantum difficulties before introducing the code.

**Experiment and verification:** Enumerate injected errors and verify decoding; distinguish classical bit-flip protection from protection against general quantum noise.

## Part V. Classical Simulation of Quantum Systems

### Chapter 24: How a Statevector Simulator Works

**Role:** Core implementation reading. **Prerequisites:** 2, 4, 5; 9 for resource accounting.

**Learning focus:** Reshape/permute gate application, batching, memory cost and differentiation through simulation.

**Derivation:** Derive tensor-axis gate application and the exponential statevector storage cost.

**Experiment and verification:** Implement a minimal independent reference executor and compare it with FlagQuantum on short random circuits.

### Chapter 25: Matrix Product States and Truncation Error

**Role:** Extension. **Prerequisites:** 2, 4, 7, 8, 22, 24.

**Learning focus:** SVD factorizations, bond dimensions, canonical forms, entanglement and truncation.

**Derivation:** Construct an MPS from successive Schmidt decompositions and derive the meaning of discarded singular-value weight.

**Experiment and verification:** Compare small MPS calculations with exact statevectors while varying bond dimension; report approximation settings and error.

### Chapter 26: Tensor Networks and Contraction Strategies

**Role:** Extension. **Prerequisites:** 4, 9, 22, 24, 25.

**Learning focus:** Circuit tensor networks, contraction order, slicing and amplitude versus full-state requests.

**Derivation:** Translate a small circuit into indexed tensor contractions and count intermediate tensor sizes.

**Experiment and verification:** Verify contractions against a dense reference and compare contraction paths without implying that every circuit is tractable.

## Part VI. From Papers to Reproducible Research

### Chapter 27: From a Paper to a Reproducible Computational Experiment

**Role:** Core research method. **Prerequisites:** 4, 6, 9; 16 and 17 for variational cases.

**Learning focus:** Source revisions, symbol tables, assumptions, units, equation dependencies, independent references, uncertainty and experimental records.

**Derivation:** Turn a carefully scoped source equation into an executable specification; separate discretization, truncation, sampling and optimization errors and define comparison criteria.

**Experiment and verification:** Build a paper-reproduction worksheet and environment manifest. Validate limiting cases and one independent equation-level calculation before optimization; report resource and timing boundaries if benchmarking is relevant.

### Chapter 28: Reproducing Molecular Hydrogen VQE

**Role:** Research capstone; starter available. **Prerequisites:** 4, 6, 16, 17, 19, 22, 27.

**Learning focus:** The O'Malley paper, corrected source data, wire labels, ansatz normalization and energy curves.

**Derivation:** Derive the reduced Hamiltonian, ansatz amplitudes, expectations, gradient and exact sector minimum.

**Experiment and verification:** Expand the existing reproduction into a complete case study: all 54 geometries, bounded grid error, optimizer and sampling extensions, provenance and limits.

## Appendices and companion laboratories

- **A. Mathematical Reference, Probability, and Selected Proofs.**
- **B. Matrix Calculus and PyTorch Autograd Conventions.**
- **C. FlagQuantum Runtime Contracts, Compilation, and Interoperability.**
- **D. Experiment Manifests, Uncertainty Records, and Benchmark Protocols.**
- **E. Platform Laboratories: Accelerators, Distribution, and Hardware Access.**
- **F. Selected Solutions and Paper-Reproduction Worksheets.**

The mathematical appendices provide refreshers and lengthy optional arguments. Technical appendices provide explicit versioned contracts and laboratory setup. Accelerator and hardware experiments are optional, and live credentials must never be required for the core course. Dedicated primary references and a supported software path must be selected before drafting specialized simulation or platform examples.

## Dependency and reading paths

- **Entry and foundations:** 1 motivates the subject; 2–6 develop the mathematical and circuit model; 7–8 connect concrete protocols to density matrices.
- **Algorithms:** 9 establishes resource accounting, 10 oracles and phase kickback; 11 develops search, while 12 → 13 develops Fourier-based methods; 14 adds dynamics.
- **Differentiable applications:** 15 → 16 → 17, then choose 18, 19 or 20.
- **Realistic information processing:** 8 → 21 → 22 → 23, with the circuit and measurement prerequisites.
- **Simulation:** 24 gives an independent exact executor; 7–8 and 22 supply the entanglement and error language for 25–26.
- **Research:** 27 can be read once its application prerequisites are met; 28 draws on the energy, gradient and verification chapters.

The numbered order is not a requirement to finish every branch before beginning research practice. Core designates conceptual importance, not a promise that all core-labelled material fits in a single semester.

## Example 14-week introductory course

| Week | Reading and practical objective |
|---|---|
| 1 | Chapter 1 and selected Chapter 2: the first experiment and notation diagnostic |
| 2 | Chapters 3–4: states, rotations, tensor products and basis indices |
| 3 | Chapter 5: gates, circuit order and dense-matrix agreement |
| 4 | Chapter 6: measurement, conditional states, expectations and shots |
| 5 | Chapters 7–8: a teleportation or superdense-coding lab, then reduced states |
| 6 | Chapters 9–10: resource models, reversible oracles and phase kickback |
| 7 | Chapter 11: Grover geometry and iteration counts |
| 8 | Chapters 12–13, selected sections: QFT and phase estimation |
| 9 | Chapters 15–16: parameterized models and verified gradients |
| 10 | Chapter 17 and one application in 18–20 |
| 11 | Chapters 21–22, selected sections: noise and quantitative correctness |
| 12 | Chapter 23 introductory code and syndrome lab |
| 13 | Chapter 27: source specification, independent checks and reproducibility |
| 14 | Chapter 28 for the VQE branch, or another scoped final project |

Assign mathematical refreshers as needed. The simulation chapters, deeper information-theory sections and additional application branches form an advanced second-semester or independent-study route.

## Writing order and acceptance gates

1. **Validate the architecture.** Review this reference-informed outline, learning outcomes, prerequisite paths and exercise design with target readers.
2. **Write a coherent opening block.** Draft Chapter 1, the required parts of 2, and Chapters 3–6. The opening example should motivate the tools that the following chapters establish.
3. **Complete the conceptual bridge.** Write 7–9 so protocols, mixed states and resource accounting are in place.
4. **Build the first research path.** Develop 15–17 and 19, followed by 27–28. Expand the existing starters in their new homes rather than treating their short text as final chapters.
5. **Complete algorithms and quantitative information.** Write 10–14 and 21–23 with explicit proofs, resource assumptions, noise models and comparison metrics.
6. **Add advanced applications and simulation.** Develop 18, 20 and 24–26, plus supported companion laboratories.
7. **Review a full edition.** Resolve mathematical and reader-review findings, exercises, attribution and all web/print checks before freezing a coherent scholarly manuscript.

A chapter is reviewable only when its motivating question, definitions, assumptions, derivation and code mapping are explicit; the full examples run; expected results and tolerances are recorded; and short checkpoints, substantial problems, recap and primary-source locators are present. Publishing a sample PDF does not establish readiness of the full textbook.

## Scope of the first complete edition

The book includes introductory information concepts needed for validation and error correction. Full quantum Shannon theory, channel-capacity theorems, advanced cryptographic security proofs and fault-tolerance threshold proofs remain further reading. The resource chapter introduces complexity and oracle assumptions without reproducing an entire theoretical-computer-science course. Detailed device engineering and provider-specific operations remain companion laboratories.

## Relation to the current samples

| Existing artifact | Intended book home | Required expansion |
|---|---|---|
| Measurement starter | Chapter 6 | Measurement postulates, conditional states, broader observables and sampling |
| Gradient starter | Chapter 16 | Generator spectra, parameter reuse, costs and graded exercises |
| Hydrogen VQE starter | Chapter 28 | A full paper specification and interpretation of the complete experiments |
| Conventions | Front matter and Appendix C | Notation and runtime contracts consistently referenced by every chapter |
| Reference guide | Bibliography and authoring support | Exact source locations actually consulted in completed chapters |

The three-chapter sample PDF keeps its own numbering and source revision. The book outline is a separate living plan. See the [reading guide](references/reading-guide.md) and [mapping](references/chapter-mapping.md) for companion resources.
