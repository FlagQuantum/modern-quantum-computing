# Contents and chapter status

**Reference-informed planning revision: October 20, 2026.** Six parts, 28 chapters and six appendices. This revises the first outline after reading the preface, contents and selected teaching passages of Nielsen and Chuang; see the [design review](references/nielsen-chuang-design-review.md).

The [learning design](learning-design.md) adds recall, prediction and error diagnosis within this structure, informed by the [Quantum Country review](references/quantum-country-design-review.md).

Only three starter chapters currently exist, with intended homes in Chapters **6, 16 and 28**. They require expansion and editorial review. The versioned three-chapter PDF is a format pilot with its own numbering, not the full manuscript.

See the [full book plan](book-plan.md) for prerequisites, derivations, experiments, learning paths and writing priorities. Planned topics do not certify the availability of a FlagQuantum API or execution backend.

## Part I. Foundations and Quantum Information Primitives

| Chapter | Title | Reading role | Status |
|---|---|---|---|
| 1 | What Quantum Computing Computes: A First Formula-to-Code Experiment | Core; opening motivation | Planned |
| 2 | Complex Vectors, Operators, and Numerical Checks | Core | Planned |
| 3 | Single-Qubit States and Rotations | Core | Planned |
| 4 | Composite Systems, Tensor Products, and Qubit Ordering | Core | Planned |
| 5 | Quantum Gates and Circuit Construction | Core | Planned |
| 6 | Measurement, Expectation Values, and Sampling | Core | [Measurement starter](chapters/measurement.md) |
| 7 | Entanglement and Quantum Information Protocols | Core | Planned |
| 8 | Density Matrices, Reduced States, and Purification | Core | Planned |

## Part II. Computational Models and Quantum Algorithms

| Chapter | Title | Reading role | Status |
|---|---|---|---|
| 9 | Computational Models, Resource Accounting, and Quantum Advantage | Core | Planned |
| 10 | Interference, Oracles, and Phase Kickback | Core | Planned |
| 11 | Grover Search and Amplitude Amplification | Core | Planned |
| 12 | The Quantum Fourier Transform | Core | Planned |
| 13 | Quantum Phase Estimation and Algorithmic Cost | Core | Planned |
| 14 | Hamiltonian Simulation and Product Formulas | Extension | Planned |

## Part III. Variational and Differentiable Quantum Computing

| Chapter | Title | Reading role | Status |
|---|---|---|---|
| 15 | Parameterized Circuits and Observable Design | Core | Planned |
| 16 | Quantum Gradients and Automatic Differentiation | Core | [Gradients starter](chapters/gradients.md) |
| 17 | Loss Functions, Optimization, and Training Diagnostics | Core | Planned |
| 18 | Hybrid Classical-Quantum Models | Core application | Planned |
| 19 | Variational Algorithms and Molecular Energy Problems | Core application | Planned |
| 20 | QAOA and Combinatorial Optimization | Application and independent project | Planned |

## Part IV. Noise, Quantitative Comparisons, and Error Correction

| Chapter | Title | Reading role | Status |
|---|---|---|---|
| 21 | Noise and Open-System Simulation | Core extension | Planned |
| 22 | State Distances, Fidelity, and Introductory Quantum Information | Core measurement and validation language | Planned |
| 23 | Quantum Error Correction and Syndrome Experiments | Extension | Planned |

## Part V. Classical Simulation of Quantum Systems

| Chapter | Title | Reading role | Status |
|---|---|---|---|
| 24 | How a Statevector Simulator Works | Core implementation reading | Planned |
| 25 | Matrix Product States and Truncation Error | Extension | Planned |
| 26 | Tensor Networks and Contraction Strategies | Extension | Planned |

## Part VI. From Papers to Reproducible Research

| Chapter | Title | Reading role | Status |
|---|---|---|---|
| 27 | From a Paper to a Reproducible Computational Experiment | Core research method | Planned |
| 28 | Reproducing Molecular Hydrogen VQE | Research capstone | [Hydrogen VQE starter](chapters/vqe.md) |

## Appendices and companion laboratories

- **A. Mathematical Reference, Probability, and Selected Proofs** — planned.
- **B. Matrix Calculus and PyTorch Autograd Conventions** — planned.
- **C. FlagQuantum Runtime Contracts, Compilation, and Interoperability** — planned.
- **D. Experiment Manifests, Uncertainty Records, and Benchmark Protocols** — planned.
- **E. Platform Laboratories: Accelerators, Distribution, and Hardware Access** — planned.
- **F. Selected Solutions and Paper-Reproduction Worksheets** — planned.

Appendix E and linked platform laboratories contain version-dependent installation, device, distributed-launch and cloud-job details. The textbook retains the theory and resource models needed to understand them. The bibliography, symbol index, glossary and acknowledgements are separate back matter.

The [reference reading guide](references/reading-guide.md) and [source notes](sources.md) are already available.
