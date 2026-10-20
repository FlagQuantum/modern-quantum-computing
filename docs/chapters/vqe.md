# Molecular hydrogen VQE: from a paper to code

**Starter draft · FlagQuantum 0.3.1 · CPU · complex128**

This chapter reproduces a small ideal-state calculation from O'Malley et al., *Scalable Quantum Simulation of Molecular Energies* (2016), using the corrected [arXiv v2](https://arxiv.org/abs/1512.06860v2). It does not reproduce the superconducting hardware experiment. See [source notes](../sources.md) for provenance and scope.

## 1. Paper Hamiltonian and data

The reduced STO-6G hydrogen Hamiltonian has six Pauli terms:

$$
H=c_I I+c_{ZI}Z_0+c_{IZ}Z_1+c_{ZZ}Z_0Z_1+c_{XX}X_0X_1+c_{YY}Y_0Y_1.
$$

At $R=0.75$ angstrom, corrected Table I gives $(c_I,c_{ZI},c_{IZ},c_{ZZ},c_{XX},c_{YY})=(0.2252,0.3435,-0.4347,0.5716,0.0910,0.0910)$ hartree. The constant already includes the geometry-dependent offset; do not add another nuclear-repulsion term.

**Formula → code:** `coefficients_at(0.75)` loads this labeled row; `dense_hamiltonian(coefficients)` constructs an independent 4 by 4 matrix. Both functions are in `examples/omalley2016/h2_vqe_model.py`.

## 2. Ansatz, ordering, and amplitudes

With this book's wire convention the reference state is $\lvert10\rangle$, prepared using `.x(0)`. Translate the paper's wire order before translating its ket labels.

$$
\lvert\psi(\theta)\rangle=e^{-i\theta X_0Y_1}\lvert10\rangle
=\cos\theta\lvert10\rangle+\sin\theta\lvert01\rangle.
$$

The identity follows from $(X_0Y_1)^2=I$ and $X_0Y_1\lvert10\rangle=i\lvert01\rangle$.

**Formula → code:** `expectations(theta)` constructs the gate decomposition. `verify_h2_vqe.py` compares its statevector with both `[0, sin(theta), cos(theta), 0]` and `torch.linalg.matrix_exp(-1j * theta * generator) @ hf`.

## 3. Derive the energy and gradient

| Derived expectation | Reference expression in the verification script |
|---|---|
| $\langle Z_0\rangle=-\cos(2\theta)$ | `-(2*theta).cos()` |
| $\langle Z_1\rangle=\cos(2\theta)$ | `(2*theta).cos()` |
| $\langle Z_0Z_1\rangle=-1$ | `-torch.ones_like(theta)` |
| $\langle X_0X_1\rangle=\langle Y_0Y_1\rangle=\sin(2\theta)$ | `(2*theta).sin()` |

The diagonal terms follow by weighting the two basis-state eigenvalues. Both XX and YY exchange the two occupied basis states, giving twice the product of their real amplitudes.

Let $a=c_I-c_{ZZ}$, $A=c_{IZ}-c_{ZI}$, and $D=c_{XX}+c_{YY}$. Then

$$
E(\theta)=a+A\cos(2\theta)+D\sin(2\theta),\qquad
E'(\theta)=-2A\sin(2\theta)+2D\cos(2\theta).
$$

**Formula → code:** `closed_energy(theta, coefficients)` and `closed_gradient(theta, coefficients)` implement these identities. The runtime energy is computed separately from the five measured expectations and their coefficients.

The generator has eigenvalues $\pm1$, so

$$
E'(\theta)=E(\theta+\pi/4)-E(\theta-\pi/4).
$$

**Formula → code:** `energy(theta + torch.pi/4, coefficients) - energy(theta - torch.pi/4, coefficients)` checks autograd. There is no factor of one half here.

## 4. Independent minimum and verified output

In the ordered subspace $(\lvert10\rangle,\lvert01\rangle)$,

$$
H_{\mathrm{odd}}=\begin{pmatrix}a+A&D\\D&a-A\end{pmatrix},\quad
E_{\min}=a-\sqrt{A^2+D^2},\quad
\theta_* = \frac12\mathrm{atan2}(-D,-A).
$$

**Formula → code:** `analytic_minimum(coefficients)` returns the closed-form result; `torch.linalg.eigvalsh(hamiltonian).min()` checks it against the full Hamiltonian. An odd-sector minimum need not be the global ground energy for arbitrary coefficients, so this comparison is necessary.

```bash
python examples/omalley2016/verify_h2_vqe.py
```

Expected output:

```text
Checked 4 angles: state, matrix exponential, 5 Pauli terms, energy, gradients.
Autograd, closed-form, dense-matrix, and parameter-shift gradients agree.
Hartree-Fock energy at R=0.75: -1.124600000 Eh
Analytical theta*: -0.114871856 rad
Exact ground energy at R=0.75: -1.145599124 Eh
All identity, sign, ordering, and gradient checks passed.
```

## 5. Extend the experiment

The complete scripts are in [examples/omalley2016](https://github.com/FlagQuantum/modern-quantum-computing/tree/main/examples/omalley2016).

```bash
python examples/omalley2016/reproduce_h2_curve.py
python examples/omalley2016/train_h2_vqe.py
python examples/omalley2016/sample_h2_energy.py
```

The curve script scans 1,000 angles for each of 54 tabulated geometries, writes a CSV, a manifest and a plot under `vqe-results/`, and checks the analytic grid-error bound. The maximum scan-to-exact gap is approximately 0.000029795 Eh. Adam training is an additional teaching experiment: its final energy is approximately -1.145599124 Eh.

The shot script is a synthetic sampling extension with fixed seeds, 65,536 shots per measurement basis and three bases. It is not a hardware run. Sampling uncertainty and rounded Hamiltonian coefficients limit comparison with published physical energies.

## Exercises

1. Prepare `.x(1)` instead of `.x(0)`. Explain the incorrect reference energy at zero angle.
2. Derive the grid-error bound from the sinusoidal energy curve.
3. Change the identity coefficient. Which quantities change: state, gradient, optimal angle, absolute energy?
4. Compare the odd-sector minimum with all four eigenvalues at every geometry.

The table uses rounded coefficients and does not include the paper's finer equilibrium geometry of 0.72 angstrom. Do not infer an experimental reproduction, an exact molecular potential, or a hardware accuracy claim from this ideal calculation.

## Further reading

Use citation key `omalley_2016` in the [BibTeX bibliography](../references/references.bib), and cite corrected arXiv v2 for the numerical table. The [chapter mapping](../references/chapter-mapping.md) identifies the paper locations used by this starter.
