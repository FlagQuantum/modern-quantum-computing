# Contents and chapter status

The full curriculum below is a proposal. Only the three linked starter chapters are currently drafted and executable. They are sample chapters from different parts of the eventual book, not a complete beginner course.

| Part | Proposed chapters | Status |
|---|---|---|
| I. Mathematical and computational foundations | Complex vectors; tensor products; states; gates; measurement; qubit ordering | [Measurement starter](chapters/measurement.md); other chapters planned |
| II. Quantum algorithms | Interference; entanglement; Grover search; QFT; phase estimation | Planned |
| III. Differentiable quantum computing | Parameterized circuits; gradients; optimization; hybrid models | [Gradients starter](chapters/gradients.md); other chapters planned |
| IV. Simulation and physical systems | Statevectors; MPS; tensor networks; noise; open systems; error correction | Planned |
| V. From papers to reproducible experiments | VQE; source provenance; uncertainty; benchmarks | [Hydrogen VQE starter](chapters/vqe.md); other chapters planned |

## Dependencies

Measurement assumes complex vectors and matrix products. Gradients build on measurement and elementary calculus. VQE builds on both starter chapters, tensor products, and eigenvalue problems. All examples use the shared [conventions](conventions.md).

See [source notes](sources.md) for paper provenance and validation scope.
