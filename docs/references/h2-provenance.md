# H₂: integral-to-reduced-model provenance plan

**Checked 2026-10-20 · authoring specification, not chapter body.** Planning and source verification only; no new chapter body. Numerical regeneration is distinct from recovery of original author files, and citation selection is distinct from independent experimental validation.

[All-section proof plan](../proof-plan.md) · [Topological experiment ledger](topological-experiments.md) · [Exact source catalogue](proof-sources.md)

## Source chain and acceptance obligations

### H2-01: Fix the molecular and energy model

**Owning sections:** [25.2](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-2), [49.2](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-2). **Sources:** [H2:reduction](proof-sources.md#source-h2-reduction).

**Checked:** Born–Oppenheimer, nonrelativistic clamped nuclei, atomic units; R in angstrom for Table I. Neutral singlet H2, two electrons, no frozen core. Keep nuclear repulsion 1/R_bohr as an explicit scalar.

**Authoring acceptance:** Require separate electronic and total energies and an explicit angstrom-to-bohr constant; a minimal basis is a model approximation, not a complete-basis claim.

### H2-02: Pin the STO-6G basis instead of importing a familiar STO-3G model

**Owning sections:** [25.2](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-2), [49.2](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-2). **Sources:** [H2:reduction](proof-sources.md#source-h2-reduction), [BSE6:H](proof-sources.md#source-bse6-h).

**Checked:** O’Malley Appendix A names STO-6G. BSE hydrogen version 1 identifies six primitives and the Hehre–Stewart–Pople origin; PySCF 2.10.0 primitives agree within 2e-10 absolute.

**Authoring acceptance:** Store basis/version, primitive normalization, geometry, RHF convergence, AO ordering and MO phases in the future experiment manifest. The 1969 basis paper is linked through the database, not claimed to have been inspected table by table.

### H2-03: Generate and declare AO-to-MO integral conventions

**Owning sections:** [25.2](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-2), [49.2](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-2). **Sources:** [BK2012:integrals](proof-sources.md#source-bk2012-integrals), [H2:reduction](proof-sources.md#source-h2-reduction).

**Checked:** Use real RHF bonding g and antibonding u MOs; order spin orbitals g_alpha, g_beta, u_alpha, u_beta. PySCF eri[i,j,k,l] is chemist (ij|kl); spin h_pqrs in the paper uses creation p,q and annihilation r,s with spatial (p s|q r) and the corresponding spin deltas.

**Authoring acceptance:** Write the index permutation and the factor 1/2 explicitly; verify Hermiticity, integral symmetries and the negative kinetic-energy operator before drafting. No nuclear scalar may be silently absorbed or added twice.

### H2-04: Distinguish a historical mapping reference from the numeric dataset

**Owning sections:** [25.3](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-3), [49.2](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-2). **Sources:** [BK2012:integrals](proof-sources.md#source-bk2012-integrals), [BK2012:paulis](proof-sources.md#source-bk2012-paulis), [H2:data](proof-sources.md#source-h2-data).

**Checked:** Seeley Table III gives one RHF geometry, 1.401 bohr, and cites PyQuante. Independent STO-3G regeneration matches its six reported integrals within 1e-6; STO-6G does not give that fixture. It therefore supports mapping algebra, not a claim of numerical inheritance of the 2016 STO-6G scan.

**Authoring acceptance:** Cite Table III only as a separate fixture. Do not present its numbers as the unpublished 2016 integral files or reuse them across geometries.

### H2-05: Make the four-mode occupation-to-BK map explicit

**Owning sections:** [25.3](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-3), [49.2](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-2). **Sources:** [BK2012:mapping](proof-sources.md#source-bk2012-mapping), [BK2012:paulis](proof-sources.md#source-bk2012-paulis), [H2:reduction](proof-sources.md#source-h2-reduction).

**Checked:** Use left-to-right f0,f1,f2,f3 and BK bits b=(f0, f0 xor f1, f2, f0 xor f1 xor f2 xor f3). Construct the full 16-dimensional Fock Hamiltonian with fermionic signs, then a basis permutation B. All 15 four-qubit terms of O’Malley Eq. (A5) / Seeley Eq. (79) are checked against the basis-permuted Fock matrix before projection, with the nuclear scalar added once.

**Authoring acceptance:** Require a term-by-term Pauli/matrix comparison in the eventual derivation; do not identify visually similar Pauli expressions without an explicit basis/gauge transformation.

### H2-06: Identify the exact reduction sector and remaining particle-number condition

**Owning sections:** [25.4](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-4), [49.2](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-2), [49.3](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-3). **Sources:** [H2:reduction](proof-sources.md#source-h2-reduction), [H2:gauge](proof-sources.md#source-h2-gauge).

**Checked:** HF occupations 1100 map to BK 1000. Fix Z on old qubits 1 and 3 to +1 and retain old 0,2 as new 0,1. Their basis is vacuum, u-pair, g-pair, fully occupied. The two-electron sector is the odd subspace Z0 Z1=-1, spanned by |01> and |10> in q0-left order.

**Authoring acceptance:** Require commutation checks for the removed Z operators, a projector/isometry, and comparison with the full N=2 block. The two-qubit matrix alone is not a fixed-N=2 Hamiltonian. Paper register printing and library bit order must be translated explicitly.

### H2-07: Bridge the six unique MO integrals to all reduced coefficients

**Owning sections:** [49.2](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-2), [49.3](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-3). **Sources:** [H2:reduction](proof-sources.md#source-h2-reduction), [H2:data](proof-sources.md#source-h2-data).

**Checked:** Verification tooling uses a=h_gg, b=h_uu, u=(gg|gg), v=(uu|uu), w=(gg|uu), k=(gu|gu). Planned algebra must recover g0=E_NN+a+b+(u+v)/2+w-k/2; g1=-a-u/2-w+k/2; g2=-b-v/2-w+k/2; g3=w-k/2; g4=g5=k/2.

**Authoring acceptance:** Require agreement between this analytic bridge and the independently constructed Fock/BK projection; these are conventions of the chosen ordering and sector, not a basis-independent coefficient recipe.

### H2-08: Validate the corrected 54-row table without fitting

**Owning sections:** [49.1](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-1), [49.6](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-6), [49.7](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-7). **Sources:** [H2:data](proof-sources.md#source-h2-data).

**Checked:** Independent STO-6G regeneration checks 54 geometries, 0.20–2.85 angstrom in 0.05 increments, and 324 coefficients against the corrected v2 Table I. Every residual is below 5e-5 Hartree. N=2 block minima equal the odd two-qubit block minima throughout the scan.

**Authoring acceptance:** Preserve the original transcribed table and its hash. Store regenerated coefficients separately; report rounding error bounds and distinguish rounded-model energy from the unrounded integral calculation.

### H2-09: State exactly what provenance has and has not been recovered

**Owning sections:** [49.7](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-7), [49.9](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-9). **Sources:** [H2:reduction](proof-sources.md#source-h2-reduction), [H2:data](proof-sources.md#source-h2-data).

**Checked:** The declared basis, analytic reduction, corrected numerical table and independent regeneration now form a checked source chain. The accessed paper does not supply the original per-geometry AO/MO integral files or a complete author software manifest.

**Authoring acceptance:** Acceptance is reconstruction at published precision, not bitwise recovery of the authors’ workflow or a repetition of their superconducting hardware experiment. Full mathematical and reader review remain open.

## Independent numerical audit

The repository verification tool constructs creation/annihilation matrices and the BK basis permutation independently of the coefficient table. It checks all 15 terms of the four-qubit Pauli expansion before projection, the analytic six-integral bridge, absent reduced Pauli coefficients, removed-Z commutators, fixed-N=2 spectrum and coefficient-rounding energy bound. It does not execute a new FlagQuantum implementation or claim recovery of original author integral files.

- Coverage: 324 coefficients at 54 geometries.
- Maximum absolute coefficient residual: 4.96219941135e-05 Hartree; tolerance 0.00005 Hartree, half the last printed decimal.
- STO-3G counterexample at 0.75 angstrom differs from Table I by more than 0.007 Hartree in an individual coefficient.
- Historical Seeley Table III fixture is checked separately at 1.401 bohr, within its six-decimal reporting precision.

| R (angstrom) | Regenerated total N=2 energy (Hartree) | Rounded-table energy (Hartree) | Maximum coefficient residual (Hartree) |
|---|---|---|---|
| 0.75 | -1.1457416711 | -1.1455991241 | 4.48443e-05 |
| 1.00 | -1.1088730602 | -1.1089167280 | 4.52678e-05 |
| 2.85 | -0.9429134318 | -0.9429725038 | 4.38864e-05 |

Recorded environment: python 3.9.6, pyscf 2.10.0, numpy 1.26.4, scipy 1.13.1, h5py 3.14.0. CPU, macOS ARM64. Linux CI repeats the invariant/tolerance checks; exact floating-point bits are not prescribed.

Verification tooling and machine-readable records: [script](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/scripts/verify_h2_provenance.py), [pinned audit dependencies](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/requirements-provenance.txt), [54-row audit report](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/verification/h2-provenance.json). These optional chemistry dependencies are separate from the FlagQuantum examples environment.

```bash
python3 -m venv .venv-provenance
.venv-provenance/bin/python -m pip install -r requirements-provenance.txt
OMP_NUM_THREADS=1 .venv-provenance/bin/python scripts/verify_h2_provenance.py
```

The command asserts the physical/numerical contracts and prints the coefficient count, maximum residual and tolerance. It leaves the checked-in report unchanged; an intentional new audit can use `--write`.

## Software-method sources

Integral notation is checked against the official [PySCF ao2mo documentation](https://pyscf.org/pyscf_api_docs/pyscf.ao2mo.html) and [AO-to-MO guide](https://pyscf.org/contributor/ao2mo_developer.html). The [PySCF 2.10.0 source](https://github.com/pyscf/pyscf/tree/v2.10.0) pins the implementation; [BSE STO-family notes](https://www.basissetexchange.org/family_notes/sto/) identify the basis origin. The mathematical proof, first-use explanation and reader acceptance gates remain pending.
