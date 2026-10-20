# Notation and implementation conventions

| Concept | Convention |
|---|---|
| State | Column vector $\lvert\psi\rangle$ |
| Basis | Lexicographic computational basis; for two qubits: $00,01,10,11$ |
| Wire order | Qubit 0 is the most significant bit |
| Basis index | $j=\sum_{k=0}^{n-1}b_k2^{n-1-k}$ |
| Gate order | Circuit calls appear in time order; matrices act right to left |
| Angles | Radians |
| Rotation | $R_P(\phi)=\exp(-i\phi P/2)$ |
| Observable | Hermitian operator; expectation $\langle\psi\rvert O\lvert\psi\rangle$ |
| Precision | torch.float64 angles and torch.complex128 amplitudes |
| Energy | Hartree (Eh) in the VQE chapter |

A batch of one state has shape `(1, 2**n)`. Named expectations have shape `(batch_size,)`; the starter scripts use `.squeeze(0)` to obtain scalar values while preserving autograd.

The VQE paper parameter $\theta$ occurs in $\exp(-i\theta X_0Y_1)$: its generator has eigenvalues $\pm1$. Its shift rule differs from a single `ry(phi)` gate. Never transfer a shift formula without checking the generator normalization.

## Validation policy

Use independent analytic expressions or dense matrices for small reference systems. Set tolerances explicitly. Verify ordering and signs before optimization. Report hardware, dependencies, precision, and stochastic seeds when relevant. A passing check establishes only the tested scope.
