# Full book plan

**Planning revision: October 20, 2026.** This is an editorial plan, not a claim that the book is complete. The current web/PDF sample remains versioned independently. The [contents](contents.md) provide a compact chapter list.

## Audience and outcomes

Target readers know basic Python and introductory linear algebra. Chapter 1 reviews the mathematical tools used later; it does not replace an entire linear algebra course. Elementary calculus is required from Chapter 13 and basic neural-network knowledge from Chapter 15. No prior quantum mechanics course is assumed for the core path.

By the end of the core path, a reader should derive small quantum calculations, build them with FlagQuantum, diagnose ordering and normalization errors, verify results independently, and translate a carefully scoped paper calculation into a reproducible experiment.

## Scope and chapter design

Each chapter follows **question → conventions → derivation → code correspondence → independent verification → experiments → exercises → limits and sources**. Use three depth levels: core calculation, deeper derivation, and research extension. Numerical examples support an argument; they do not replace a proof of a general result.

Theory must not be restricted to the APIs of one release. Small independent PyTorch/NumPy calculations can supply mathematical references. A FlagQuantum execution path must be verified against the chapter's explicitly targeted release. The current starters target 0.3.1; future chapters must not silently assume that all capabilities of a newer development branch are available there.

Before drafting MPS/TN, distributed, compiler or physical-hardware examples, select the appropriate primary references and audit the actual supported software path. Include an exact small CPU reference and label approximation settings and platform-specific evidence. Live cloud execution is optional.

## Part I. Mathematical and Computational Foundations

### Chapter 1: Complex Vectors, Operators, and Numerical Checks

**Role:** Core. **Prerequisites:** Python; introductory linear algebra.

**Learning focus:** Complex inner products, adjoints, eigenvalues, matrix exponentials and floating-point tolerances.

**Derivation:** Derive normalization and spectral decomposition for small Hermitian matrices.

**Experiment and verification:** Build independent PyTorch/NumPy reference calculations; check reconstruction and residual norms.

### Chapter 2: Single-Qubit States and Rotations

**Role:** Core. **Prerequisites:** 1.

**Learning focus:** Amplitudes, global and relative phase, Bloch coordinates and Pauli rotations.

**Derivation:** Derive the rotation matrices and their action on an arbitrary normalized state.

**Experiment and verification:** Compare explicit matrices with FlagQuantum rotations, including zero-angle, inverse and phase-equivalence checks.

### Chapter 3: Composite Systems, Tensor Products, and Qubit Ordering

**Role:** Core. **Prerequisites:** 1, 2.

**Learning focus:** Tensor-product spaces, registers, computational basis indices and subsystem labels.

**Derivation:** Derive the bit-string-to-index map and the action of an operator on a selected wire.

**Experiment and verification:** Check two- and three-qubit circuits against Kronecker products and deliberately swapped wire conventions.

### Chapter 4: Quantum Gates and Circuit Construction

**Role:** Core. **Prerequisites:** 2, 3.

**Learning focus:** Single-qubit gates, controlled gates, composition, inversion and basic decompositions.

**Derivation:** Derive circuit matrices and distinguish call order from matrix multiplication order.

**Experiment and verification:** Build a Bell circuit and a small reversible circuit; compare complete states or unitaries with dense references.

### Chapter 5: Measurement, Expectation Values, and Sampling

**Role:** Core; starter available. **Prerequisites:** 2, 3, 4.

**Learning focus:** Born probabilities, observable expectations, variance and finite-shot estimators.

**Derivation:** Derive probabilities and expectations for a rotated qubit, then connect variance to estimator uncertainty.

**Experiment and verification:** Extend the existing exact-expectation starter with seeded shot experiments and a comparison of sampling error versus shot count.

### Chapter 6: Entanglement, Mixed States, and Quantum Channels

**Role:** Core. **Prerequisites:** 3, 4, 5.

**Learning focus:** Reduced states, Schmidt decomposition, density matrices, purification and channels.

**Derivation:** Derive partial traces, the pure-state entanglement criterion and Kraus completeness.

**Experiment and verification:** Compare Bell and product states; verify density-matrix positivity, trace preservation and a simple channel against dense calculations.

## Part II. Quantum Algorithms and Hamiltonian Dynamics

### Chapter 7: Interference, Oracles, and Phase Kickback

**Role:** Core. **Prerequisites:** 3, 4, 5.

**Learning focus:** Interference as a computational resource; reversible functions, phase oracles and query models.

**Derivation:** Derive phase kickback and a small Deutsch-Jozsa example, stating the oracle promise and query cost.

**Experiment and verification:** Enumerate truth tables and compare gate-level oracles with their dense diagonal or permutation matrices.

### Chapter 8: Grover Search and Amplitude Amplification

**Role:** Core. **Prerequisites:** 5, 7.

**Learning focus:** Reflections, marked subspaces, iteration counts and success probabilities.

**Derivation:** Reduce Grover iteration to a two-dimensional rotation and derive the ideal success curve.

**Experiment and verification:** Run small searches with different numbers of marked states; compare every iteration with the analytic formula and count oracle calls.

### Chapter 9: The Quantum Fourier Transform

**Role:** Core. **Prerequisites:** 3, 4, 7.

**Learning focus:** Discrete Fourier phases, controlled rotations, inverse transforms and output reversal.

**Derivation:** Derive the product representation of the QFT and the role of final wire swaps.

**Experiment and verification:** Compare the circuit with the dense Fourier matrix for each basis input and quantify a small approximate-QFT error.

### Chapter 10: Quantum Phase Estimation and Algorithmic Cost

**Role:** Core. **Prerequisites:** 5, 7, 9.

**Learning focus:** Eigenphases, controlled powers, finite precision and the connection to factoring.

**Derivation:** Derive exact-grid outcomes and the off-grid probability distribution; distinguish query cost from gate synthesis cost.

**Experiment and verification:** Estimate phases of a known small unitary, compare the full distribution and explain what changes when the input is not an eigenstate.

### Chapter 11: Hamiltonian Simulation and Product Formulas

**Role:** Extension. **Prerequisites:** 1, 4, 10.

**Learning focus:** Pauli expansions, time evolution, noncommuting terms and product-formula error.

**Derivation:** Derive first-order and symmetric second-order product formulas for a small Hamiltonian.

**Experiment and verification:** Compare decomposed evolution with a dense matrix exponential; measure error as the time step decreases without claiming general scalability.

## Part III. Differentiable Quantum Computing

### Chapter 12: Parameterized Circuits and Observable Design

**Role:** Core. **Prerequisites:** 4, 5; 6 for mixed-state extensions.

**Learning focus:** Trainable angles, data-dependent angles, Pauli sums, batch dimensions and ansatz structure.

**Derivation:** Express a circuit model as an expectation-valued function and identify all parameter occurrences.

**Experiment and verification:** Build a batched model and verify each batch element and Pauli term against separate scalar and dense calculations.

### Chapter 13: Quantum Gradients and Automatic Differentiation

**Role:** Core; starter available. **Prerequisites:** 1, 2, 5, 12; elementary calculus.

**Learning focus:** Autograd, parameter shift, generator spectra, shared parameters and finite differences.

**Derivation:** Derive the single-Pauli shift rule, its normalization changes and the chain rule for reused parameters.

**Experiment and verification:** Extend the existing gradient starter with independent analytic, dense-matrix and shifted-execution checks; report execution cost.

### Chapter 14: Loss Functions, Optimization, and Training Diagnostics

**Role:** Core. **Prerequisites:** 12, 13.

**Learning focus:** Scalar losses, optimizer state, initialization, local minima, gradient noise and convergence diagnostics.

**Derivation:** Derive a small loss and its gradient, and distinguish exact-expectation from finite-shot optimization.

**Experiment and verification:** Train a small circuit with PyTorch, log post-update losses, and compare final results with an analytic or exhaustive reference.

### Chapter 15: Hybrid Classical-Quantum Models

**Role:** Core application. **Prerequisites:** 12, 13, 14; basic neural networks.

**Learning focus:** Classical preprocessing, quantum layers, output heads and end-to-end differentiation.

**Derivation:** Derive the chain rule across the classical and quantum boundary and state feature and output dimensions.

**Experiment and verification:** Train a small hybrid model with a classical baseline and held-out evaluation; verify gradients through both components.

### Chapter 16: Variational Algorithms and Molecular Energy Problems

**Role:** Core application. **Prerequisites:** 1, 3, 5, 12, 13, 14.

**Learning focus:** The variational principle, Hamiltonian measurement, ansatz choice and small molecular models.

**Derivation:** Prove the energy upper bound under its assumptions and derive a weighted Pauli objective; introduce a small fermion-to-qubit mapping.

**Experiment and verification:** Check energies against exact diagonalization and a tiny occupation-basis Hamiltonian; separate ideal VQE, shot estimates and optimizer behavior.

## Part IV. Simulation Methods and Computational Systems

### Chapter 17: How a Statevector Simulator Works

**Role:** Core implementation reading. **Prerequisites:** 1, 3, 4.

**Learning focus:** Reshape/permute gate application, batching, memory cost and differentiation through simulation.

**Derivation:** Derive tensor-axis gate application and the exponential statevector storage cost.

**Experiment and verification:** Implement a minimal independent reference executor and compare it with FlagQuantum on short random circuits.

### Chapter 18: Matrix Product States and Truncation Error

**Role:** Extension. **Prerequisites:** 1, 3, 6, 17.

**Learning focus:** SVD factorizations, bond dimensions, canonical forms, entanglement and truncation.

**Derivation:** Construct an MPS from successive Schmidt decompositions and derive the meaning of discarded singular-value weight.

**Experiment and verification:** Compare small MPS calculations with exact statevectors while varying bond dimension; report approximation settings and error.

### Chapter 19: Tensor Networks and Contraction Strategies

**Role:** Extension. **Prerequisites:** 3, 17, 18.

**Learning focus:** Circuit tensor networks, contraction order, slicing and amplitude versus full-state requests.

**Derivation:** Translate a small circuit into indexed tensor contractions and count intermediate tensor sizes.

**Experiment and verification:** Verify contractions against a dense reference and compare contraction paths without implying that every circuit is tractable.

### Chapter 20: Accelerators, Distributed Simulation, and Training

**Role:** Platform-dependent extension. **Prerequisites:** 12, 13, 17; basic parallel computing.

**Learning focus:** Device selection, memory bandwidth, state sharding, communication and data-parallel training.

**Derivation:** Distinguish partitioning one quantum state from distributing independent examples; derive a small communication and memory model.

**Experiment and verification:** Provide a CPU baseline and a supported multi-process example; report hardware, topology, backend and synchronization cost for any accelerator evidence.

## Part V. Compilation, Noise, and Physical Execution

### Chapter 21: Circuit Compilation and Interoperability

**Role:** Extension. **Prerequisites:** 3, 4, 7.

**Learning focus:** Gate identities, target gate sets, connectivity, layout and framework conventions.

**Derivation:** Derive simple optimizations and routing identities; distinguish semantic equivalence from identical serialized circuits.

**Experiment and verification:** Check a supported conversion or routing example against dense operators, allowing a documented global phase and wire permutation.

### Chapter 22: Noise and Open-System Simulation

**Role:** Core extension. **Prerequisites:** 5, 6; 11 for time evolution.

**Learning focus:** Kraus channels, density-matrix evolution, trajectories and Lindblad dynamics.

**Derivation:** Derive a small amplitude-damping example and a simple master-equation evolution.

**Experiment and verification:** Compare against independent density-matrix evolution; check trace, positivity, limiting cases and stochastic uncertainty where applicable.

### Chapter 23: Quantum Error Correction and Syndrome Experiments

**Role:** Extension. **Prerequisites:** 3, 4, 5, 6, 22.

**Learning focus:** Parity checks, stabilizers, syndrome extraction, decoding and logical errors.

**Derivation:** Derive a repetition-code syndrome table and introduce the stabilizer conditions for a quantum code.

**Experiment and verification:** Enumerate injected errors and verify decoding; distinguish classical bit-flip protection from protection against general quantum noise.

### Chapter 24: Quantum Hardware, Calibration, and Digital Twins

**Role:** Platform-dependent extension. **Prerequisites:** 5, 21, 22; 25 for comparison protocols.

**Learning focus:** Credentials and jobs, hardware constraints, calibration snapshots and model mismatch.

**Derivation:** Define a small calibrated error model and a comparison statistic with explicit sampling assumptions.

**Experiment and verification:** Offer an offline saved-data path; make live hardware optional and separately validated. Distinguish a calibrated simulator from a predictive physical digital twin.

## Part VI. From Papers to Reproducible Research

### Chapter 25: Reproducibility, Uncertainty, and Benchmarks

**Role:** Core research practice. **Prerequisites:** 1, 5; 17 and 20 for simulator benchmarks.

**Learning focus:** Environment records, seeds, tolerances, timing, warm-up, synchronization and scientific uncertainty.

**Derivation:** Separate discretization, truncation, sampling and optimization errors; define fair timing and comparison boundaries.

**Experiment and verification:** Build an experiment manifest and repeat a small experiment across seeds or settings; use output correctness checks before reporting timings.

### Chapter 26: Translating a Paper into an Executable Specification

**Role:** Core research practice. **Prerequisites:** 3, 5, 13, 25.

**Learning focus:** Source versions, symbol tables, assumptions, units, equation dependencies and verification ladders.

**Derivation:** Work from a source equation to an explicit array expression, resolving omitted conventions and normalization.

**Experiment and verification:** Create a paper-reproduction worksheet, test limiting cases and reproduce one equation with an independent reference before optimization.

### Chapter 27: Reproducing Molecular Hydrogen VQE

**Role:** Research capstone; starter available. **Prerequisites:** 3, 5, 13, 14, 16, 25, 26.

**Learning focus:** The O'Malley paper, corrected source data, wire labels, ansatz normalization and energy curves.

**Derivation:** Derive the reduced Hamiltonian, ansatz amplitudes, expectations, gradient and exact sector minimum.

**Experiment and verification:** Expand the existing reproduction into a complete case study: all 54 geometries, bounded grid error, optimizer and sampling extensions, provenance and limits.

### Chapter 28: From MaxCut to QAOA: An Independent Reproduction Project

**Role:** Research extension. **Prerequisites:** 4, 5, 7, 12, 13, 14, 25, 26.

**Learning focus:** Graph objectives, cost and mixer Hamiltonians, alternating circuits and sampled solutions.

**Derivation:** Translate a small MaxCut objective into a Hamiltonian and derive the alternating-unitary conventions before selecting a reference paper.

**Experiment and verification:** Compare sampled cut values and optimized expectations with exhaustive classical enumeration. Require a source/version record and independent checks; do not infer quantum advantage from a small example.

## Appendices

- **A. Linear Algebra Reference and Useful Identities.**
- **B. Matrix Calculus and PyTorch Autograd Conventions.**
- **C. Mathematical Objects and FlagQuantum Runtime Contracts.**
- **D. Environment Records and Experiment Manifest Templates.**
- **E. Selected Exercise Solutions and Verification Notes.**
- **F. Paper-Reproduction Worksheets and Checklists.**

Appendices C and D should contain stable conventions, contracts and reproducibility templates. Link out to versioned API documentation for exhaustive method signatures and installation details. Keep the bibliography and symbol index separate from the appendices.

## Dependency and reading paths

- **Foundations:** Chapters 1–6 in order. Chapter 3 is required before multi-qubit code.
- **Algorithms:** 7 → 8 and 7 → 9 → 10; Chapter 11 adds Hamiltonian dynamics.
- **Differentiable models:** 12 → 13 → 14, then 15 for hybrid models or 16 for energy problems.
- **Simulation internals:** 17 → 18 → 19; Chapter 20 branches from statevector simulation and gradient concepts.
- **Physical execution:** 21 and 22 lead to 23 or 24. Chapter 25 supplies comparison and uncertainty protocols.
- **Research reproduction:** 25 → 26 → 27 or 28, after the relevant mathematical and variational chapters.

Core does not mean every chapter must fit in one semester. Instructors can assign extensions as readings and choose one application branch.

## Example 14-week course

| Week | Reading and practical goal |
|---|---|
| 1 | Chapters 1–2: normalized states and explicit rotation matrices |
| 2 | Chapter 3: tensor products, indexing and wire conventions |
| 3 | Chapter 4: gates, controlled operations and circuit/matrix agreement |
| 4 | Chapter 5: probabilities, expectations and sampling |
| 5 | Chapter 6: entanglement and reduced density matrices |
| 6 | Chapters 7–8: phase kickback and the Grover success curve |
| 7 | Chapter 9: circuit QFT versus the dense transform |
| 8 | Chapter 10: phase estimation and precision; factorization as context |
| 9 | Chapter 12: parameterized models and Pauli objectives |
| 10 | Chapter 13: analytic, automatic and shifted gradients |
| 11 | Chapter 14: loss design, optimization and diagnostics |
| 12 | Choose Chapter 15 or 16: hybrid learning or variational energies |
| 13 | Chapters 25–26: manifests, uncertainty and paper translation |
| 14 | Chapter 27 for the VQE branch, or an appropriately scoped hybrid project: report derivation, code, independent checks and limits |

This is a pacing proposal. A class with less mathematical preparation needs a longer foundations block. An advanced course can replace the introductory algorithm block with Chapters 11 and 17–24.

## Writing order and acceptance gates

1. **Stabilize the architecture.** Agree on the audience, notation, chapter boundaries and prerequisite graph. Treat the three current starters as format pilots.
2. **Write the missing foundations.** Draft Chapters 1–4, then expand Chapters 5–6. Readers should be able to reach the measurement starter without external prerequisites beyond the stated background.
3. **Complete the first continuous formula-to-code path.** Develop Chapters 12–14 and 16, followed by 25–27; deepen the existing gradient and VQE starters in their final homes.
4. **Complete algorithm coverage.** Write Chapters 7–11 with oracle assumptions, resource accounting and small dense references.
5. **Add applications and technical extensions.** Develop Chapters 15 and 17–24 only with adequate source and software evidence, then use Chapter 28 as an independent capstone.
6. **Review and freeze a scholarly edition.** Resolve cross-references, source rights, exercises, author review and numerical validation before preparing a coherent arXiv manuscript. The existing 17-page sample is not that full edition.

A chapter is ready for editorial review only when its definitions, conventions and derivation are explicit; the equation/code mapping is complete; its full examples run; expected results and tolerances are recorded; exercises include a calculation, modification and debugging task; and limitations and precise primary references are present. Publication readiness additionally requires independent reader review and visual checks in both web and print formats.

## Boundaries for the first complete edition

Fault-tolerant resource estimation, quantum cryptography, full quantum Shannon theory, detailed hardware engineering and many-body tensor-network research are further-reading topics, not additional full parts in the first edition. Factoring is introduced through phase estimation; a complete industrial-scale Shor implementation is not promised. The book should retain enough scope to teach a coherent process rather than collect every feature of a software framework.

## Relation to current material

| Existing artifact | Intended book location | Required expansion |
|---|---|---|
| Measurement starter | Chapter 5 | General observables, uncertainty and finite-shot exercises |
| Gradient starter | Chapter 13 | Generator normalization, shared parameters and gradient-estimation costs |
| Hydrogen VQE starter | Chapter 27 | Explicit paper/specification worksheet and a narrative linking the complete experiments |
| Conventions | Front matter and Appendix C | Consistent notation and contracts referenced by every chapter |
| Reference guide and mapping | Bibliography and authoring support | Exact source locators for each completed chapter |

Use the [reference mapping](references/chapter-mapping.md) to select companion readings. The detailed chapter plan specifies intended outcomes; it does not imply that every listed derivation or example has already been written or tested.
