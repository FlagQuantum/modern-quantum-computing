# Chapter-to-reference mapping

This is a reading and editorial plan. **Only measurement, gradients and hydrogen VQE are drafted.** Other rows describe proposed chapters from the [contents](../contents.md); they do not add completed material or certify FlagQuantum support for a topic. Abbreviations and access information are defined in the [reading guide](reading-guide.md).

## Book chapter numbers

The [full book plan](../book-plan.md) now assigns the measurement, gradients and hydrogen VQE starters to Chapters **6, 16 and 28** respectively. The mapping below groups related topics for reading; consult the plan for the complete 28-chapter sequence and dependencies. The current sample PDF retains its own three-chapter numbering.

See the [Nielsen–Chuang design review](nielsen-chuang-design-review.md) for the reasons behind the revised chapter allocation.

## Existing starter chapters

| Our chapter | Targeted reading | What to derive and implement | Independent verification |
|---|---|---|---|
| [Measurement and expectation values](../chapters/measurement.md) | NC Chapter 2; P Chapter 3, *Measurement and Evolution* (July 2015) | Rotation amplitudes, Born probabilities and the expectation of Z | Closed-form probabilities and the probability-weighted eigenvalue sum |
| [Parameterized circuits and gradients](../chapters/gradients.md) | SP *Variational Circuits as Machine Learning Models*; Schuld et al. (2019), key `schuld_gradients_2019` | Single-Pauli rotation derivatives and the corresponding shift rule | Analytic derivative, autograd, shifted executions and central differences |
| [Molecular hydrogen VQE](../chapters/vqe.md) | O'Malley et al. (2016), key `omalley_2016`; corrected arXiv v2, Eq. (1), Eq. (3), Appendix A/Table I and Appendix B | Translate Hamiltonian labels, qubit order, ansatz and generator normalization | Dense matrix exponential, full Hamiltonian eigenspectrum and closed-form energy/gradient |

The VQE chapter's Adam optimizer and synthetic-shot sampling are tutorial extensions. They must not be attributed to the paper's 1,000-angle scan or described as reproductions of its hardware experiment.

## Proposed foundations and algorithm chapters

| Proposed topic | Targeted reading | Formula-to-code learning objective |
|---|---|---|
| Complex vectors, inner products and operators | RP for introductory explanation; W Chapter 1 for advanced precision | Connect conjugation, normalization, eigenvectors and matrix products to tensor operations |
| Tensor products, registers and qubit ordering | NC Chapter 2; M Chapter 1, *Cbits and Qbits* | Derive basis-index mappings and compare a Kronecker-product reference with circuit execution |
| States, mixed states and measurement | NC Chapter 2; P Chapters 2–3 (July 2015) | Derive projective measurement, partial trace and density-matrix expectations |
| Entanglement | NC Chapter 2; P Chapter 4, *Quantum Entanglement* (2001, incomplete); W Chapter 6 for extensions | Compare reduced states, Schmidt coefficients and explicit small-state calculations |
| Circuits and universal gates | NC Chapter 4; P Chapter 5, *Classical and Quantum Circuits* (July 2015) | Derive gate matrices and check circuit composition against dense operators |
| QFT and phase estimation | NC Chapter 5; P Chapter 6, *Quantum Algorithms* (November 2020); M Chapter 3 for factoring context | Derive phase conventions, controlled powers and output-bit interpretation |
| Grover search | NC Chapter 6; M Chapter 4, *Searching with a quantum computer* | Derive the two-dimensional rotation and check success probability versus iteration count |

## Proposed differentiable-computing chapters

| Proposed topic | Targeted reading | Formula-to-code learning objective |
|---|---|---|
| Data encoding | SP *Representing Data on a Quantum Computer* | State encoding assumptions and track data dimensions through a circuit |
| Hybrid optimization and models | SP *Variational Circuits as Machine Learning Models*; `schuld_gradients_2019` | Derive a loss, its chain rule and gradient-estimation cost; test a small joint model |
| Quantum kernels | SP *Quantum Models as Kernel Methods* | Derive overlaps and Gram matrices; distinguish model definition from empirical advantage |

## Proposed simulation, noise and research chapters

| Proposed topic | Targeted reading | Formula-to-code learning objective |
|---|---|---|
| Noise and quantum channels | NC Chapter 8; P Chapter 3 (July 2015); W Chapter 2 for mathematical definitions | Derive Kraus completeness and channel action; compare with an independent density-matrix calculation |
| State distances and fidelity | NC Chapter 9; W Chapter 3 | State the fidelity convention explicitly and check pure-state and mixed-state cases |
| Error correction | NC Chapter 10; P Chapter 7, *Quantum Error Correction* (March 2026); M Chapter 5 | Derive parity checks and syndrome meaning before simulating an error-and-correction cycle |
| Statevector, MPS and tensor-network simulation | NC Chapter 2 and W Chapter 6 provide background on tensor products and Schmidt structure only | Select dedicated simulation references before drafting: these six resources are not a complete implementation reference for MPS/TN methods |
| Paper reproduction, uncertainty and benchmarks | `omalley_2016` is the first worked case; additional methodological references remain to be selected | Record source revisions and environment; separate analytic checks, approximation error, sampling error and performance measurements |

## Editorial depth

- **Core:** derive the main identity, run a small program and interpret the result.
- **Deeper derivation:** explain proof assumptions, normalization, error terms and computational cost.
- **Research extension:** read a primary source, change the model and design an independent check.

A reference mapping does not grant reuse rights. Follow the [resource policy](reading-guide.md#resource-policy). When a planned chapter becomes a draft, replace broad topic pointers with the exact source locations actually consulted.
