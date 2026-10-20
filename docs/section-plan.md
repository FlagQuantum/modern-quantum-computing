# Detailed chapter and section plan

**Revision: 2026-10-20.** 9 parts, 50 chapters and 435 numbered sections. **Writing Baseline 1.0 adopted; section acceptance pending.**

Each section has a learning/derivation target and an implementation/evidence target. These are authoring specifications, not completed sections or validated APIs. See the [curriculum audit](curriculum-audit.md), [reader-continuity standard](reader-continuity.md), and [full book plan](book-plan.md).

## How to read the specification

- Section numbers are display labels; stable chapter/section anchors preserve references when numbering changes.
- A learning target states what the reader can explain or derive; a central result needs assumptions and a proof or an explicit advanced-proof roadmap.
- An evidence target defines an independently checked calculation, experiment, counterexample or resource analysis. Numerical agreement does not prove a general theorem.
- Each chapter has unnumbered closing material: recap, conceptual checks, substantial derivation/proof and transfer problems, programming/debugging laboratories, selected answers, source locators and review records.
- Exact section prerequisites are authoritative; chapter-level entry guidance does not require completing whole chapters. Read local bridges before use. Core/advanced labels apply within specialized chapters too.
- [Framework gaps](implementation-roadmap.md) do not remove a theoretical topic. Unsupported examples stay explicitly pending.
- The [writing baseline](writing-baseline.md) fixes scope, depth, volumes and production order. Future drafts use local start checks; proof/software/reader review remains required for acceptance.

[Full editorial review](architecture-review.md) · [All-section ledger](section-review.md) · [Checked learning paths](learning-paths.md)

## Parts and chapters

### Part 1. Foundations and Quantum Information Primitives

| Chapter | Sections | Detailed plan |
|---|---|---|
| 1 | 1.1–1.6 | [What Quantum Computing Computes](section-plans/01-foundations.md#ch-what-quantum-computing-computes) |
| 2 | 2.1–2.8 | [Complex Vectors, Operators, and Numerical Reasoning](section-plans/01-foundations.md#ch-complex-vectors-operators-and-numerical-reasoning) |
| 3 | 3.1–3.7 | [Single-Qubit States and Rotations](section-plans/01-foundations.md#ch-single-qubit-states-and-rotations) |
| 4 | 4.1–4.8 | [Composite Systems, Tensor Products, and Qubit Ordering](section-plans/01-foundations.md#ch-composite-systems-tensor-products-and-qubit-ordering) |
| 5 | 5.1–5.8 | [Gates, Reversible Computation, and Circuit Synthesis](section-plans/01-foundations.md#ch-gates-reversible-computation-and-circuit-synthesis) |
| 6 | 6.1–6.9 | [Measurement, Expectation Values, and Statistical Estimation](section-plans/01-foundations.md#ch-measurement-expectation-values-and-statistical-estimation) |
| 7 | 7.1–7.9 | [Entanglement and Quantum Information Protocols](section-plans/01-foundations.md#ch-entanglement-and-quantum-information-protocols) |
| 8 | 8.1–8.8 | [Density Matrices, Reduced States, and Purification](section-plans/01-foundations.md#ch-density-matrices-reduced-states-and-purification) |

### Part 2. Quantum Information: Channels, Inference, and Communication

| Chapter | Sections | Detailed plan |
|---|---|---|
| 9 | 9.1–9.8 | [Quantum Channels and Their Representations](section-plans/02-information.md#ch-quantum-channels-and-their-representations) |
| 10 | 10.1–10.9 | [Distinguishability, Fidelity, and Quantum State Inference](section-plans/02-information.md#ch-distinguishability-fidelity-and-quantum-state-inference) |
| 11 | 11.1–11.8 | [Entropy, Relative Entropy, and Information Processing](section-plans/02-information.md#ch-entropy-relative-entropy-and-information-processing) |
| 12 | 12.1–12.9 | [Compression, Entanglement, and Communication Limits](section-plans/02-information.md#ch-compression-entanglement-and-communication-limits) |
| 13 | 13.1–13.9 | [Quantum Cryptography and Security Reasoning](section-plans/02-information.md#ch-quantum-cryptography-and-security-reasoning) |

### Part 3. Quantum Algorithms and Computational Resources

| Chapter | Sections | Detailed plan |
|---|---|---|
| 14 | 14.1–14.9 | [Computational Models, Complexity, and Quantum Advantage](section-plans/03-algorithms.md#ch-computational-models-complexity-and-quantum-advantage) |
| 15 | 15.1–15.8 | [Interference, Oracles, and Phase Kickback](section-plans/03-algorithms.md#ch-interference-oracles-and-phase-kickback) |
| 16 | 16.1–16.8 | [Grover Search, Amplitude Amplification, and Estimation](section-plans/03-algorithms.md#ch-grover-search-amplitude-amplification-and-estimation) |
| 17 | 17.1–17.9 | [Fourier Transforms and Quantum Phase Estimation](section-plans/03-algorithms.md#ch-fourier-transforms-and-quantum-phase-estimation) |
| 18 | 18.1–18.9 | [Period Finding, Factoring, and Algorithmic Arithmetic](section-plans/03-algorithms.md#ch-period-finding-factoring-and-algorithmic-arithmetic) |
| 19 | 19.1–19.9 | [Hamiltonian Simulation and Error Bounds](section-plans/03-algorithms.md#ch-hamiltonian-simulation-and-error-bounds) |
| 20 | 20.1–20.9 | [Block Encodings and Quantum Linear Algebra](section-plans/03-algorithms.md#ch-block-encodings-and-quantum-linear-algebra) |
| 21 | 21.1–21.9 | [Quantum Signal Processing and Singular Value Transformation](section-plans/03-algorithms.md#ch-quantum-signal-processing-and-singular-value-transformation) |
| 22 | 22.1–22.9 | [Quantum Walks, Lower Bounds, and Algorithm Design](section-plans/03-algorithms.md#ch-quantum-walks-lower-bounds-and-algorithm-design) |

### Part 4. Variational and Differentiable Quantum Computing

| Chapter | Sections | Detailed plan |
|---|---|---|
| 23 | 23.1–23.10 | [Parameterized Circuits, Quantum Gradients, and Differentiation](section-plans/04-variational.md#ch-parameterized-circuits-quantum-gradients-and-differentiation) |
| 24 | 24.1–24.9 | [Optimization, Geometry, and Trainability](section-plans/04-variational.md#ch-optimization-geometry-and-trainability) |
| 25 | 25.1–25.12 | [Variational Simulation, Chemistry, and Ground-State Problems](section-plans/04-variational.md#ch-variational-simulation-chemistry-and-ground-state-problems) |
| 26 | 26.1–26.8 | [QAOA, Quantum Optimization, and Classical Comparisons](section-plans/04-variational.md#ch-qaoa-quantum-optimization-and-classical-comparisons) |
| 27 | 27.1–27.8 | [Quantum Learning, Kernels, and Hybrid Models](section-plans/04-variational.md#ch-quantum-learning-kernels-and-hybrid-models) |

### Part 5. Noise, Error Correction, and Fault-Tolerant Computation

| Chapter | Sections | Detailed plan |
|---|---|---|
| 28 | 28.1–28.10 | [Noise, Open Systems, and Error Mitigation](section-plans/05-fault-tolerance.md#ch-noise-open-systems-and-error-mitigation) |
| 29 | 29.1–29.9 | [Quantum Error Correction: Conditions and Recovery](section-plans/05-fault-tolerance.md#ch-quantum-error-correction-conditions-and-recovery) |
| 30 | 30.1–30.11 | [Stabilizer Codes, Logical Operators, and Decoding](section-plans/05-fault-tolerance.md#ch-stabilizer-codes-logical-operators-and-decoding) |
| 31 | 31.1–31.8 | [Surface Codes and Repeated Syndrome Measurements](section-plans/05-fault-tolerance.md#ch-surface-codes-and-repeated-syndrome-measurements) |
| 32 | 32.1–32.8 | [Fault-Tolerant Gates and Universal Logical Computation](section-plans/05-fault-tolerance.md#ch-fault-tolerant-gates-and-universal-logical-computation) |
| 33 | 33.1–33.8 | [From Logical Algorithms to Physical Resource Estimates](section-plans/05-fault-tolerance.md#ch-from-logical-algorithms-to-physical-resource-estimates) |

### Part 6. Physical Realizations and Quantum-System Architecture

| Chapter | Sections | Detailed plan |
|---|---|---|
| 34 | 34.1–34.10 | [From Abstract Qubits to Physical Quantum Systems](section-plans/physical-platforms.md#ch-from-abstract-qubits-to-physical-quantum-systems) |
| 35 | 35.1–35.8 | [Superconducting Qubits and Circuit-QED Control](section-plans/physical-platforms.md#ch-superconducting-qubits-and-circuit-qed-control) |
| 36 | 36.1–36.8 | [Trapped-Ion Qubits, Motional Gates, and Transport](section-plans/physical-platforms.md#ch-trapped-ion-qubits-motional-gates-and-transport) |
| 37 | 37.1–37.8 | [Neutral-Atom Arrays and Rydberg Quantum Computing](section-plans/physical-platforms.md#ch-neutral-atom-arrays-and-rydberg-quantum-computing) |
| 38 | 38.1–38.9 | [Photonic Encodings, Optical Circuits, and Measurement-Based Computation](section-plans/physical-platforms.md#ch-photonic-encodings-optical-circuits-and-measurement-based-computation) |
| 39 | 39.1–39.8 | [Semiconductor Spin Qubits and Exchange-Based Architectures](section-plans/physical-platforms.md#ch-semiconductor-spin-qubits-and-exchange-based-architectures) |
| 40 | 40.1–40.8 | [Topological Quantum Computation and Candidate Physical Realizations](section-plans/physical-platforms.md#ch-topological-quantum-computation-and-candidate-physical-realizations) |

### Part 7. Quantum Programming, Compilation, and Control

| Chapter | Sections | Detailed plan |
|---|---|---|
| 41 | 41.1–41.9 | [Quantum Programs, Intermediate Representations, and Verified Optimization](section-plans/quantum-compilation.md#ch-quantum-programs-intermediate-representations-and-verified-optimization) |
| 42 | 42.1–42.10 | [Gate Synthesis, Qubit Mapping, Routing, and Scheduling](section-plans/quantum-compilation.md#ch-gate-synthesis-qubit-mapping-routing-and-scheduling) |
| 43 | 43.1–43.10 | [Control-Level Lowering, Dynamic Execution, and Logical Compilation](section-plans/quantum-compilation.md#ch-control-level-lowering-dynamic-execution-and-logical-compilation) |

### Part 8. Classical Simulation and the Boundary of Tractability

| Chapter | Sections | Detailed plan |
|---|---|---|
| 44 | 44.1–44.8 | [Exact Simulation, Tensor Execution, and Numerical Reliability](section-plans/06-simulation.md#ch-exact-simulation-tensor-execution-and-numerical-reliability) |
| 45 | 45.1–45.8 | [Stabilizer Simulation, Magic, and Classical Simulability](section-plans/06-simulation.md#ch-stabilizer-simulation-magic-and-classical-simulability) |
| 46 | 46.1–46.8 | [Matrix Product States, Entanglement, and Truncation](section-plans/06-simulation.md#ch-matrix-product-states-entanglement-and-truncation) |
| 47 | 47.1–47.10 | [Tensor Networks, Contraction, and Hybrid Simulation Strategies](section-plans/06-simulation.md#ch-tensor-networks-contraction-and-hybrid-simulation-strategies) |

### Part 9. From Papers to Reproducible Research

| Chapter | Sections | Detailed plan |
|---|---|---|
| 48 | 48.1–48.9 | [Reading Papers, Building Evidence, and Reproducing Results](section-plans/07-research.md#ch-reading-papers-building-evidence-and-reproducing-results) |
| 49 | 49.1–49.9 | [Case Study: Molecular Hydrogen from Hamiltonian to Verified VQE](section-plans/07-research.md#ch-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe) |
| 50 | 50.1–50.9 | [Case Study: Logical Memory and Error-Correction Experiments](section-plans/07-research.md#ch-case-study-logical-memory-and-error-correction-experiments) |

## Integration and review

The complete plan contains **50 chapters and 435 numbered sections**. A higher count does not establish coverage, depth or readability. The [architecture-review gates](curriculum-audit.md) require coverage, dependency, workload and reader review before sustained drafting.

Existing starters supply material to 6, 23 and 49 at their scheduled homes. Writing Baseline 1.0 fixes the production queue; subsequent drafts follow its section-local start checks. Provider access and framework availability are tracked separately from theory.
