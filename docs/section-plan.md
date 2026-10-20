# Detailed chapter and section plan

**Planning revision: October 20, 2026.** This expands the [40-chapter curriculum](contents.md) into numbered sections. Each section has a learning/derivation target and a concrete implementation or evidence target. These are authoring specifications; they are not completed textbook sections, reviewed proofs or validated FlagQuantum features.

Reading levels and chapter prerequisites are inherited from the [book plan](book-plan.md). Sections marked Advanced can be deferred on an introductory route. A framework gap follows the [implementation workflow](implementation-roadmap.md) and does not remove the section's mathematical target.

## How to read the specification

- A section number such as **23.5** identifies a planned section within Chapter 23. Titles and allocation remain reviewable before the first complete edition.
- Learning/derivation targets state what the reader should be able to explain or derive. A central result needs its assumptions, proof or explicit advanced-proof roadmap.
- Implementation/evidence targets state what a worked program, counterexample, resource calculation or independent reference must establish. Numerical examples do not prove general theorems.
- Each chapter also has **unnumbered closing material**: a recap, short conceptual checks, substantial derivation/proof and transfer problems, programming/debugging laboratories, selected answer guidance, precise source locators, and a review/implementation-status record. These are not counted as scientific sections.
- No section requires inventing an unsupported API. Some resource, security or theorem sections appropriately use independent classical calculations or proof exercises; their scientific objective determines the implementation.
- Detailed subsections, equation numbers, exact theorem/source mappings and problem sets are developed during chapter drafting and mathematical review.


## Parts and chapters


### Part 1. Foundations and Quantum Information Primitives

| Chapter | Sections | Detailed plan |
|---|---|---|
| 1 | 1.1–1.6 | [What Quantum Computing Computes](section-plans/01-foundations.md#chapter-1) |
| 2 | 2.1–2.8 | [Complex Vectors, Operators, and Numerical Reasoning](section-plans/01-foundations.md#chapter-2) |
| 3 | 3.1–3.8 | [Single-Qubit States and Rotations](section-plans/01-foundations.md#chapter-3) |
| 4 | 4.1–4.7 | [Composite Systems, Tensor Products, and Qubit Ordering](section-plans/01-foundations.md#chapter-4) |
| 5 | 5.1–5.8 | [Gates, Reversible Computation, and Circuit Synthesis](section-plans/01-foundations.md#chapter-5) |
| 6 | 6.1–6.9 | [Measurement, Expectation Values, and Statistical Estimation](section-plans/01-foundations.md#chapter-6) |
| 7 | 7.1–7.8 | [Entanglement and Quantum Information Protocols](section-plans/01-foundations.md#chapter-7) |
| 8 | 8.1–8.8 | [Density Matrices, Reduced States, and Purification](section-plans/01-foundations.md#chapter-8) |

### Part 2. Quantum Information: Channels, Inference, and Communication

| Chapter | Sections | Detailed plan |
|---|---|---|
| 9 | 9.1–9.8 | [Quantum Channels and Their Representations](section-plans/02-information.md#chapter-9) |
| 10 | 10.1–10.8 | [Distinguishability, Fidelity, and Quantum State Inference](section-plans/02-information.md#chapter-10) |
| 11 | 11.1–11.8 | [Entropy, Relative Entropy, and Information Processing](section-plans/02-information.md#chapter-11) |
| 12 | 12.1–12.8 | [Compression, Entanglement, and Communication Limits](section-plans/02-information.md#chapter-12) |
| 13 | 13.1–13.8 | [Quantum Cryptography and Security Reasoning](section-plans/02-information.md#chapter-13) |

### Part 3. Quantum Algorithms and Computational Resources

| Chapter | Sections | Detailed plan |
|---|---|---|
| 14 | 14.1–14.8 | [Computational Models, Complexity, and Quantum Advantage](section-plans/03-algorithms.md#chapter-14) |
| 15 | 15.1–15.7 | [Interference, Oracles, and Phase Kickback](section-plans/03-algorithms.md#chapter-15) |
| 16 | 16.1–16.8 | [Grover Search, Amplitude Amplification, and Estimation](section-plans/03-algorithms.md#chapter-16) |
| 17 | 17.1–17.8 | [Fourier Transforms and Quantum Phase Estimation](section-plans/03-algorithms.md#chapter-17) |
| 18 | 18.1–18.8 | [Period Finding, Factoring, and Algorithmic Arithmetic](section-plans/03-algorithms.md#chapter-18) |
| 19 | 19.1–19.8 | [Hamiltonian Simulation and Error Bounds](section-plans/03-algorithms.md#chapter-19) |
| 20 | 20.1–20.8 | [Block Encodings and Quantum Linear Algebra](section-plans/03-algorithms.md#chapter-20) |
| 21 | 21.1–21.9 | [Quantum Signal Processing and Singular Value Transformation](section-plans/03-algorithms.md#chapter-21) |
| 22 | 22.1–22.8 | [Quantum Walks, Lower Bounds, and Algorithm Design](section-plans/03-algorithms.md#chapter-22) |

### Part 4. Variational and Differentiable Quantum Computing

| Chapter | Sections | Detailed plan |
|---|---|---|
| 23 | 23.1–23.10 | [Parameterized Circuits, Quantum Gradients, and Differentiation](section-plans/04-variational.md#chapter-23) |
| 24 | 24.1–24.9 | [Optimization, Geometry, and Trainability](section-plans/04-variational.md#chapter-24) |
| 25 | 25.1–25.9 | [Variational Simulation, Chemistry, and Ground-State Problems](section-plans/04-variational.md#chapter-25) |
| 26 | 26.1–26.8 | [QAOA, Quantum Optimization, and Classical Comparisons](section-plans/04-variational.md#chapter-26) |
| 27 | 27.1–27.8 | [Quantum Learning, Kernels, and Hybrid Models](section-plans/04-variational.md#chapter-27) |

### Part 5. Noise, Error Correction, and Fault-Tolerant Computation

| Chapter | Sections | Detailed plan |
|---|---|---|
| 28 | 28.1–28.9 | [Noise, Open Systems, and Error Mitigation](section-plans/05-fault-tolerance.md#chapter-28) |
| 29 | 29.1–29.9 | [Quantum Error Correction: Conditions and Recovery](section-plans/05-fault-tolerance.md#chapter-29) |
| 30 | 30.1–30.9 | [Stabilizer Codes, Logical Operators, and Decoding](section-plans/05-fault-tolerance.md#chapter-30) |
| 31 | 31.1–31.8 | [Surface Codes and Repeated Syndrome Measurements](section-plans/05-fault-tolerance.md#chapter-31) |
| 32 | 32.1–32.8 | [Fault-Tolerant Gates and Universal Logical Computation](section-plans/05-fault-tolerance.md#chapter-32) |
| 33 | 33.1–33.8 | [From Logical Algorithms to Physical Resource Estimates](section-plans/05-fault-tolerance.md#chapter-33) |

### Part 6. Classical Simulation and the Boundary of Tractability

| Chapter | Sections | Detailed plan |
|---|---|---|
| 34 | 34.1–34.8 | [Exact Simulation, Tensor Execution, and Numerical Reliability](section-plans/06-simulation.md#chapter-34) |
| 35 | 35.1–35.8 | [Stabilizer Simulation, Magic, and Classical Simulability](section-plans/06-simulation.md#chapter-35) |
| 36 | 36.1–36.8 | [Matrix Product States, Entanglement, and Truncation](section-plans/06-simulation.md#chapter-36) |
| 37 | 37.1–37.8 | [Tensor Networks, Contraction, and Hybrid Simulation Strategies](section-plans/06-simulation.md#chapter-37) |

### Part 7. From Papers to Reproducible Research

| Chapter | Sections | Detailed plan |
|---|---|---|
| 38 | 38.1–38.9 | [Reading Papers, Building Evidence, and Reproducing Results](section-plans/07-research.md#chapter-38) |
| 39 | 39.1–39.9 | [Case Study: Molecular Hydrogen from Hamiltonian to Verified VQE](section-plans/07-research.md#chapter-39) |
| 40 | 40.1–40.9 | [Case Study: Logical Memory and Error-Correction Experiments](section-plans/07-research.md#chapter-40) |

## Coverage and integration

The plan contains **40 chapters and 328 numbered sections**, organized into seven parts. The three existing starter chapters contribute material to **6**, **23** and **39**; they do not complete the corresponding section plans. The published three-chapter PDF keeps its independent sample numbering.

The chapter overview links to these detailed plans, and the chapter template requires authors to record the planned section number, prerequisite bridge, mathematical result and independent verification before drafting. Review overloaded chapters and prerequisite jumps with instructors and target readers; a numbered table of contents alone does not establish an effective course.

## First depth pilots

- **Chapter 6:** connect postulates, conditional states, generalized measurements and statistical estimates.
- **Chapter 23:** connect generator spectra, shared parameters, differentiation methods and estimator/resource cost.
- **Chapter 29:** connect logical information, error spans, correction conditions and a constructed recovery.

These pilots test the teaching method across foundational reasoning, modern computational methods and a substantive theorem. The [roadmap](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/ROADMAP.md) gives the writing priorities.
