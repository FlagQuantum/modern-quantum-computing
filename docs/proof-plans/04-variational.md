# Result and proof plan: Variational and Differentiable Quantum Computing

[Depth definitions](../proof-plan.md#proof-depth-contract) · [Source catalogue](../references/proof-sources.md) · [Volume plan](../volume-plan.md)

Authoring specifications only. No result/proof/API is certified by this plan. F/M/R have different scope; imported results are the exact prerequisite sections linked below.

## Chapter 23: Parameterized Circuits, Quantum Gradients, and Differentiation

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-1"></span>

### 23.1 Parameterized quantum models and tensor contracts

**Core result / role:** Parameterized expectation and occurrence map.

**Assumptions and scope:** Real parameters; fixed differentiable gates, batches and observable.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Define a scalar component and distinguish logical parameters from gate occurrences.

**Imported earlier results:** [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1), [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3).

**Exact source targets:** [PS:II](../references/proof-sources.md#source-ps-ii): Section II Computing Quantum Gradients.

**Independent evidence target:** Check a batched model against separate scalar executions.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-2"></span>

### 23.2 Differentiating a unitary expectation

**Core result / role:** Derivative of a unitary expectation.

**Assumptions and scope:** Differentiable finite unitary; fixed input/observable; real parameter.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove product/chain rules locally and retain conjugates in both derivative terms.

**Imported earlier results:** [23.1](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-1), [2.6](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-6).

**Exact source targets:** [PS:III.A](../references/proof-sources.md#source-ps-iii-a): Section III A Parameter-shift rule for gates with generators with two distinct eigenvalues.

**Independent evidence target:** Compare a generator-based expression with dense derivatives.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-3"></span>

### 23.3 The single-Pauli parameter-shift rule

**Core result / role:** Two-eigenvalue parameter-shift rule.

**Assumptions and scope:** One parameter occurrence; generator with two distinct eigenvalues.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive its sine/cosine spectrum, shift distance and prefactor; give a normalization counterexample.

**Imported earlier results:** [23.2](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-2), [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5).

**Exact source targets:** [PS:III.A](../references/proof-sources.md#source-ps-iii-a): Section III A Parameter-shift rule for gates with generators with two distinct eigenvalues.

**Independent evidence target:** Expand the existing starter with analytic and shifted-execution checks.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-4"></span>

### 23.4 Generator spectra and generalized shift rules [Advanced]

**Core result / role:** Generalized shift rules from spectral gaps.

**Assumptions and scope:** Known finite generator gaps and a nonsingular interpolation system.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Prove the frequency expansion and one interpolation construction; delimit repeated/zero-gap cases.

**Imported earlier results:** [23.2](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-2), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Exact source targets:** [GPS:III](../references/proof-sources.md#source-gps-iii): Section III Univariate Cost Functions.

**Independent evidence target:** Test a multi-eigenvalue example against an independent spectral reference.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local mathematical bridge to supply:** Generator-gap Fourier expansion, interpolation matrices and degenerate frequencies.

**Explicitly deferred proof ingredients:** General optimal/minimal shift-rule classification; one nonsingular finite interpolation construction is derived locally from Wierichs et al. Section III.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-5"></span>

### 23.5 Shared parameters and classical reparameterization

**Core result / role:** Shared-parameter chain rule.

**Assumptions and scope:** Differentiable classical reparameterization and multiple gate occurrences.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Differentiate each independent occurrence then sum its Jacobian-weighted contribution.

**Imported earlier results:** [23.2](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-2), [23.3](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-3).

**Exact source targets:** [PS:II](../references/proof-sources.md#source-ps-ii): Section II Computing Quantum Gradients; [GPS:II.A](../references/proof-sources.md#source-gps-ii-a): Section II A Cost functions arising from quantum gates.

**Independent evidence target:** Check a reused parameter and a scaled angle; diagnose a missing chain-rule factor.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-6"></span>

### 23.6 Backpropagation and automatic differentiation

**Core result / role:** Reverse-mode differentiation equals the chain rule on a computation graph.

**Assumptions and scope:** Differentiable deterministic simulator graph; declared complex convention.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove reverse accumulation for the selected graph; separate simulator derivatives from hardware estimators.

**Imported earlier results:** [23.2](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-2), [23.5](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-5).

**Exact source targets:** [ADJ:2.2](../references/proof-sources.md#source-adj-2-2): Section 2.2 Derivation; [PS:II](../references/proof-sources.md#source-ps-ii): Section II Computing Quantum Gradients.

**Independent evidence target:** Check real outputs, complex state tensors and deliberate detach errors.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-7"></span>

### 23.7 Adjoint differentiation and memory tradeoffs

**Core result / role:** Adjoint expectation gradient recurrence.

**Assumptions and scope:** Pure-state unitary circuit; reversible gate application.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive forward/backward state recurrences and parameter contributions; count stored statevectors and operations.

**Imported earlier results:** [23.2](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-2), [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1).

**Exact source targets:** [ADJ:2.2](../references/proof-sources.md#source-adj-2-2): Section 2.2 Derivation; [ADJ:2.3](../references/proof-sources.md#source-adj-2-3): Section 2.3 Algorithm.

**Independent evidence target:** Compare gradients and operation/memory counts with a simple independent implementation.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-8"></span>

### 23.8 Finite differences and numerical diagnostics

**Core result / role:** Finite-difference truncation and rounding tradeoff.

**Assumptions and scope:** Sufficient smoothness; explicit evaluation-error bound.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Use Taylor remainders and derive the selected step-size error balance.

**Imported earlier results:** [23.2](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-2), [2.8](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-8).

**Exact source targets:** [PS:II](../references/proof-sources.md#source-ps-ii): Section II Computing Quantum Gradients.

**Independent evidence target:** Sweep finite-difference steps and compare with an exact analytic derivative.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-9"></span>

### 23.9 Finite-shot gradient estimation

**Core result / role:** Finite-shot parameter-shift estimator variance.

**Assumptions and scope:** Unbiased shifted estimates and stated covariance model.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove unbiasedness and propagate variances/shot allocation through the linear rule.

**Imported earlier results:** [23.3](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-3), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Exact source targets:** [GPS:II.C](../references/proof-sources.md#source-gps-ii-c): Section II C Resource measures for shift rules; [NC:A1](../references/proof-sources.md#source-nc-a1): Appendix 1: Notes on basic probability theory.

**Independent evidence target:** Compare exact gradients with repeated stochastic estimates and their uncertainty.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-10"></span>

### 23.10 Differentiation laboratory and cost audit

**Core result / role:** Derivative acceptance protocol.

**Assumptions and scope:** Analytic, independent matrix and numerical references.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Check generator normalization, parameter reuse, step-size sweeps and total evaluation cost.

**Imported earlier results:** [23.3](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-3), [23.5](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-5), [23.6](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-6), [23.8](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-8), [23.9](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-9), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Require analytic, dense, shifted and autograd agreement where each method applies.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 24: Optimization, Geometry, and Trainability

<span id="sec-optimization-geometry-and-trainability-1"></span>

### 24.1 Objectives and optimization problems

**Core result / role:** Objective, constraints and stationarity.

**Assumptions and scope:** Real scalar objective on a declared feasible domain.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Define local/global optimum and distinguish observable outputs from the loss.

**Imported earlier results:** [23.1](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-1), [23.2](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-2).

**Exact source targets:** [CVX:4.1](../references/proof-sources.md#source-cvx-4-1): Section 4.1 Optimization problems.

**Independent evidence target:** Specify a small objective with a known analytic or exhaustive reference.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-optimization-geometry-and-trainability-2"></span>

### 24.2 Exact and stochastic gradients

**Core result / role:** One-step descent with gradient error.

**Assumptions and scope:** L-smooth objective; explicit gradient bias/variance and stepsize.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the descent lemma and conditional expected update bound; do not infer global nonconvex convergence.

**Imported earlier results:** [24.1](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-1), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Exact source targets:** [CVX:9.3](../references/proof-sources.md#source-cvx-9-3): Section 9.3 Gradient descent method.

**Independent evidence target:** Compare deterministic and finite-shot trajectories under matched initialization.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-optimization-geometry-and-trainability-3"></span>

### 24.3 Optimizers, initialization, and diagnostics

**Core result / role:** Optimizer updates and convergence diagnostics.

**Assumptions and scope:** Selected update rule and explicit optimizer state.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive one deterministic update; distinguish pre/post-update loss and a stopping heuristic from a theorem.

**Imported earlier results:** [24.1](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-1), [24.2](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-2).

**Exact source targets:** [CVX:9.2](../references/proof-sources.md#source-cvx-9-2): Section 9.2 Descent methods; [CVX:9.3](../references/proof-sources.md#source-cvx-9-3): Section 9.3 Gradient descent method.

**Independent evidence target:** Log reproducible trajectories and compare multiple starts without cherry-picking.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-optimization-geometry-and-trainability-4"></span>

### 24.4 Quantum geometric tensor

**Core result / role:** Quantum geometric tensor from neighboring rays.

**Assumptions and scope:** Smooth normalized pure-state family modulo phase.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Expand the overlap to second order and project out the phase direction.

**Imported earlier results:** [23.2](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-2), [10.3](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-3).

**Exact source targets:** [QNG:II.A](../references/proof-sources.md#source-qng-ii-a): Section II A Quantum Information Geometry.

**Independent evidence target:** Compare analytic metric entries with independent state derivatives.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-optimization-geometry-and-trainability-5"></span>

### 24.5 Natural-gradient updates and singular metrics

**Core result / role:** Regularized natural gradient solves a local quadratic problem.

**Assumptions and scope:** Positive semidefinite metric; stated constraint/regularization.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the constrained least-change update, pseudoinverse and null-space limitations.

**Imported earlier results:** [24.3](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-3), [24.4](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-4), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Exact source targets:** [QNG:II.B](../references/proof-sources.md#source-qng-ii-b): Section II B Optimization problem.

**Independent evidence target:** Study rank deficiency, regularization and step sensitivity in a tiny model.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-optimization-geometry-and-trainability-6"></span>

### 24.6 Expressivity, identifiability, and trainability

**Core result / role:** Expressivity does not imply identifiability or trainability.

**Assumptions and scope:** Selected parameterized model and cost.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Give a redundant-parameter example and derive its singular Jacobian/metric.

**Imported earlier results:** [23.1](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-1), [24.1](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-1).

**Exact source targets:** [ENC:II](../references/proof-sources.md#source-enc-ii): Section II The expressivity of quantum models; [QNG:II.A](../references/proof-sources.md#source-qng-ii-a): Section II A Quantum Information Geometry.

**Independent evidence target:** Construct redundant parameterizations and compare behavior.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-optimization-geometry-and-trainability-7"></span>

### 24.7 Barren plateaus and ensemble assumptions [Advanced]

**Core result / role:** McClean et al. gradient-variance concentration for independent random-design blocks.

**Assumptions and scope:** Specified design/Haar ensemble, cost locality and independent blocks.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** State the selected zero-mean/variance result; roadmap Haar moment identities and supply a small exact ensemble case.

**Imported earlier results:** [24.2](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-2), [24.6](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-6).

**Exact source targets:** [BP:theorem](../references/proof-sources.md#source-bp-theorem): Main-text concentration result and gradient-variance discussion; methods proof.

**Independent evidence target:** Use controlled finite examples as illustrations; do not treat a random-circuit plot as a general proof.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local mathematical bridge to supply:** Haar/2-design averages, independent random blocks and observable normalization.

**Explicitly deferred proof ingredients:** Second-moment integral identities and full ensemble variance bound; McClean et al. pp.2–4; no extension to arbitrary shallow circuits.

<span id="sec-optimization-geometry-and-trainability-8"></span>

### 24.8 Noise, shot budgets, and mitigation overhead

**Core result / role:** Noise/shot bias and variance affect optimization cost.

**Assumptions and scope:** Specified estimator, noise channel and mitigation rule.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Propagate bias/variance through the update; distinguish unbiasedness from affordable variance.

**Imported earlier results:** [24.2](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-2), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Exact source targets:** [NOISE:mitigation](../references/proof-sources.md#source-noise-mitigation): Section V A extrapolation and V C quasi-probability methods; [NC:A1](../references/proof-sources.md#source-nc-a1): Appendix 1: Notes on basic probability theory.

**Independent evidence target:** Compare configurations with a fixed total execution budget.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-optimization-geometry-and-trainability-9"></span>

### 24.9 Optimization laboratory and honest conclusions

**Core result / role:** Optimization acceptance protocol.

**Assumptions and scope:** Independent optimum/reference where tractable.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Report repeated seeds, post-update objective, uncertainty and failure cases; no global-optimality inference.

**Imported earlier results:** [24.3](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-3), [24.6](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-6).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Compare an optimizer result with exact references and report failed runs.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 25: Variational Simulation, Chemistry, and Ground-State Problems

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-1"></span>

### 25.1 The variational principle and its assumptions

**Core result / role:** Rayleigh-Ritz variational principle.

**Assumptions and scope:** Finite Hermitian Hamiltonian; normalized trial state.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Expand in an eigenbasis and prove the energy lower bound and equality condition.

**Imported earlier results:** [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5), [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3).

**Exact source targets:** [CHEM:V.B](../references/proof-sources.md#source-chem-v-b): Section V B Variational quantum eigensolver.

**Independent evidence target:** Check the bound and construct a counterexample from an invalid estimator/model.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-2"></span>

### 25.2 Second quantization and occupation states

**Core result / role:** Fermionic anticommutation in occupation space.

**Assumptions and scope:** Finite ordered modes; explicit occupation-sign convention.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Define creation/annihilation action and prove canonical anticommutation on basis states; use the H2 provenance ledger for a concrete convention-sensitive application; retain the general theory in this chapter and avoid duplicating the capstone derivation.

**Imported earlier results:** [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3).

**Exact source targets:** [CHEM:III](../references/proof-sources.md#source-chem-iii): Section III Classical Computational Chemistry; [H2:reduction](../references/proof-sources.md#source-h2-reduction): Appendix A, Eq. (A1)–(A6) and Fig. 5: molecular model, integrals, BK Hamiltonian and reduction; [BK2012:integrals](../references/proof-sources.md#source-bk2012-integrals): Section VII, Eq. (61) and Table III: integral convention and historical RHF fixture.

**Independent evidence target:** Build a tiny occupation-basis Hamiltonian independently.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-3"></span>

### 25.3 Jordan-Wigner and fermion-to-qubit translation

**Core result / role:** Jordan-Wigner representation preserves anticommutation.

**Assumptions and scope:** Fixed fermionic mode and qubit order.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive parity strings and verify their algebra; map a selected one/two-body term; use the H2 provenance ledger for a concrete convention-sensitive application; retain the general theory in this chapter and avoid duplicating the capstone derivation.

**Imported earlier results:** [25.2](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-2), [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5), [4.3](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-3).

**Exact source targets:** [CHEM:IV.A](../references/proof-sources.md#source-chem-iv-a): Section IV A Fermion-to-qubit mappings; [H2:reduction](../references/proof-sources.md#source-h2-reduction): Appendix A, Eq. (A1)–(A6) and Fig. 5: molecular model, integrals, BK Hamiltonian and reduction; [BK2012:integrals](../references/proof-sources.md#source-bk2012-integrals): Section VII, Eq. (61) and Table III: integral convention and historical RHF fixture.

**Independent evidence target:** Compare fermionic and qubit Hamiltonian matrices.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-4"></span>

### 25.4 Symmetries and reduced models

**Core result / role:** Symmetry-sector restriction and energy offsets.

**Assumptions and scope:** Exact commuting symmetry; declared target sector.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove invariant blocks and the selected reduction; distinguish sector minimum from global minimum; use the H2 provenance ledger for a concrete convention-sensitive application; retain the general theory in this chapter and avoid duplicating the capstone derivation.

**Imported earlier results:** [25.3](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-3), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Exact source targets:** [CHEM:IV.C](../references/proof-sources.md#source-chem-iv-c): Section IV C Hamiltonian reduction; [H2:reduction](../references/proof-sources.md#source-h2-reduction): Appendix A, Eq. (A1)–(A6) and Fig. 5: molecular model, integrals, BK Hamiltonian and reduction; [BK2012:integrals](../references/proof-sources.md#source-bk2012-integrals): Section VII, Eq. (61) and Table III: integral convention and historical RHF fixture.

**Independent evidence target:** Compare sector spectra and identify an incorrect reference-state sector.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-5"></span>

### 25.5 Ansatz design and reachable states

**Core result / role:** Ansatz reachable set and symmetry preservation.

**Assumptions and scope:** Chosen generators, reference state and parameter domain.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove selected conserved quantities and characterize one small reachable subspace.

**Imported earlier results:** [25.1](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-1), [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1), [23.1](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-1).

**Exact source targets:** [CHEM:V.B.2](../references/proof-sources.md#source-chem-v-b-2): Section V B 2 Ansatzes.

**Independent evidence target:** Compare a chosen ansatz with an exactly solvable tiny subspace.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-6"></span>

### 25.6 Measuring an energy objective

**Core result / role:** Energy estimator as a weighted Pauli sum.

**Assumptions and scope:** Hamiltonian decomposition; measurement/grouping convention.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive unbiasedness and its total covariance/shot cost by reusing inference results.

**Imported earlier results:** [25.1](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-1), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7), [10.7](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-6).

**Exact source targets:** [CHEM:V.B.1](../references/proof-sources.md#source-chem-v-b-1): Section V B 1 Implementation; [NC:A1](../references/proof-sources.md#source-nc-a1): Appendix 1: Notes on basic probability theory.

**Independent evidence target:** Compare exact energy with grouped finite-shot estimators.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-7"></span>

### 25.7 Variational dynamics and extensions [Advanced]

**Core result / role:** Projected variational dynamics.

**Assumptions and scope:** Differentiable normalized ansatz; chosen real/imaginary-time variational principle.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the metric linear system and residual; state gauge and singular-solver assumptions.

**Imported earlier results:** [25.5](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-5), [24.4](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-4), [19.1](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-1).

**Exact source targets:** [QNG:appendix](../references/proof-sources.md#source-qng-appendix): Appendix: real/imaginary QGT and imaginary-time relationships; [NOISE:variational](../references/proof-sources.md#source-noise-variational): Section II B real/imaginary time and Section IV variational simulation; Appendix A.

**Independent evidence target:** Compare a tiny variational trajectory with exact dynamics.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-8"></span>

### 25.8 Chemistry model and error budgets

**Core result / role:** Chemistry error budget is model dependent.

**Assumptions and scope:** Specified basis, active space, symmetry reduction and target energy.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Separate model, ansatz, optimizer, sampling and hardware errors; no automatic chemical-accuracy claim; use the H2 provenance ledger for a concrete convention-sensitive application; retain the general theory in this chapter and avoid duplicating the capstone derivation.

**Imported earlier results:** [25.3](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-3), [25.4](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-4), [25.6](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-6).

**Exact source targets:** [CHEM:VIII](../references/proof-sources.md#source-chem-viii): Section VIII Discussion and Conclusions; [H2:reduction](../references/proof-sources.md#source-h2-reduction): Appendix A, Eq. (A1)–(A6) and Fig. 5: molecular model, integrals, BK Hamiltonian and reduction; [BK2012:integrals](../references/proof-sources.md#source-bk2012-integrals): Section VII, Eq. (61) and Table III: integral convention and historical RHF fixture.

**Independent evidence target:** Record units, constant offsets and independent reference energies.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-embedding-model"></span>

### 25.9 Classical environments and quantum embedding [Advanced]

**Core result / role:** Schmidt bath and a selected embedding construction.

**Assumptions and scope:** Finite fragment/environment split and declared mean-field reference.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Construct the bath explicitly and distinguish a self-consistency prescription from an exact full-system equivalence.

**Imported earlier results:** [25.2](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-2), [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4).

**Exact source targets:** [DMET:construction](../references/proof-sources.md#source-dmet-construction): Impurity/bath construction, self-consistency and limiting cases.

**Independent evidence target:** Compare the embedded Hamiltonian and observables against a complete small classical reference; identify which properties embedding approximates.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-embedding-self-consistency"></span>

### 25.10 Self-consistent quantum impurity solvers [Advanced]

**Core result / role:** Impurity-solver self-consistency is a fixed-point problem.

**Assumptions and scope:** Specified bath/fragment model and matching condition.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Compose the DMET impurity/matching construction with the VQE variational subroutine as an explicit textbook extension; derive one update/residual and show why fixed-point iteration need not converge. The 2012 source is not claimed to implement a quantum solver.

**Imported earlier results:** [25.9](../section-plans/04-variational.md#sec-quantum-embedding-model), [25.6](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-6), [24.3](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-3).

**Exact source targets:** [DMET:construction](../references/proof-sources.md#source-dmet-construction): Impurity/bath construction, self-consistency and limiting cases; [CHEM:V.B](../references/proof-sources.md#source-chem-v-b): Section V B Variational quantum eigensolver.

**Independent evidence target:** Compare exact-fragment and quantum-estimator loops on the same tiny model, including shot uncertainty, convergence and failure cases.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-sample-assisted-subspace-solve"></span>

### 25.11 Quantum sampling and classical subspace diagonalization [Advanced]

**Core result / role:** Projected sample-selected diagonalization is variational.

**Assumptions and scope:** Fixed finite sampled subspace; exact projected Hermitian matrix.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove the Rayleigh-Ritz upper bound; separate sampling coverage/recovery assumptions from the subspace theorem.

**Imported earlier results:** [25.1](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-1), [25.3](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-3), [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Exact source targets:** [SQD:methods](../references/proof-sources.md#source-sqd-methods): Main Methods I; Supplementary Methods II A 1 Eigenstate solver.

**Independent evidence target:** Compare selected configurations and projected solutions with exact tiny-instance results; record quantum sampling, configuration processing and classical solve costs.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-9"></span>

### 25.12 Variational-simulation laboratory

**Core result / role:** Variational-simulation acceptance protocol.

**Assumptions and scope:** Traceable Hamiltonian and independent spectral reference.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Audit symmetry, energy offsets, estimator/optimizer cost and model limitations.

**Imported earlier results:** [25.1](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-1), [25.3](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-3), [25.5](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-5), [25.6](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-6), [24.3](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-3).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Verify matrices before training and interpret the final result with all declared limitations.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 26: QAOA, Quantum Optimization, and Classical Comparisons

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-1"></span>

### 26.1 From a discrete objective to a Hamiltonian

**Core result / role:** Classical diagonal objective encoding.

**Assumptions and scope:** Binary variables with declared bit-to-Pauli convention.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove basis-state objective equality including constants and signs.

**Imported earlier results:** [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2), [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3).

**Exact source targets:** [QAOA:objective](../references/proof-sources.md#source-qaoa-objective): Objective encoding, alternating ansatz and selected low-depth analysis.

**Independent evidence target:** Compare every bit-string energy with its classical objective.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-2"></span>

### 26.2 Cost and mixer evolution

**Core result / role:** QAOA cost/mixer circuit and depth convention.

**Assumptions and scope:** Selected diagonal objective and unitary mixer.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the alternating state and commuting-term implementation.

**Imported earlier results:** [26.1](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-1), [19.5](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-5).

**Exact source targets:** [QAOA:objective](../references/proof-sources.md#source-qaoa-objective): Objective encoding, alternating ansatz and selected low-depth analysis.

**Independent evidence target:** Compare circuit layers with independent matrix exponentials.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-3"></span>

### 26.3 Low-depth analytic behavior

**Core result / role:** A complete low-depth QAOA example.

**Assumptions and scope:** Single-edge MaxCut objective; one cost layer and transverse-X mixer; fixed angle normalization.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the analytic expectation and compare its exact attainable optimum.

**Imported earlier results:** [26.2](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-2), [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3).

**Exact source targets:** [QAOA:objective](../references/proof-sources.md#source-qaoa-objective): Objective encoding, alternating ansatz and selected low-depth analysis.

**Independent evidence target:** Check parameter-dependent predictions with exhaustive references.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-4"></span>

### 26.4 Constraints and feasible mixers [Advanced]

**Core result / role:** Feasible-subspace mixer invariance.

**Assumptions and scope:** Explicit constraints; mixer commuting with feasibility projector.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove that an XY mixer preserves a fixed-Hamming-weight subspace; separately test connectivity of the selected feasible sector.

**Imported earlier results:** [26.1](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-1), [26.2](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-2).

**Exact source targets:** [MIX:mixers](../references/proof-sources.md#source-mix-mixers): Section II Framework and Section III constrained-mixer constructions.

**Independent evidence target:** Verify invariance and diagnose leakage outside the feasible subspace.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-5"></span>

### 26.5 Parameter landscapes and depth

**Core result / role:** Depth and parameter landscapes.

**Assumptions and scope:** Specified finite objective and ansatz.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive one periodicity/symmetry and show why larger depth need not ease optimization.

**Imported earlier results:** [26.3](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-3), [24.3](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-3).

**Exact source targets:** [QAOA:objective](../references/proof-sources.md#source-qaoa-objective): Objective encoding, alternating ansatz and selected low-depth analysis; [CVX:9.1](../references/proof-sources.md#source-cvx-9-1): Section 9.1 Unconstrained minimization problems.

**Independent evidence target:** Compare grids and optimized results with an exact tiny-instance landscape.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-6"></span>

### 26.6 Sampled solutions and approximation quality

**Core result / role:** Expected objective differs from sampled solution quality.

**Assumptions and scope:** Declared sampling distribution and approximation-ratio convention.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Relate expectations, tails and best-of-shot outcomes without conflating metrics.

**Imported earlier results:** [26.1](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-1), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Exact source targets:** [QAOA:objective](../references/proof-sources.md#source-qaoa-objective): Objective encoding, alternating ansatz and selected low-depth analysis; [NC:A1](../references/proof-sources.md#source-nc-a1): Appendix 1: Notes on basic probability theory.

**Independent evidence target:** Report distributions and finite-sample uncertainty rather than only the best sample.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-7"></span>

### 26.7 Classical comparisons and total cost

**Core result / role:** Matched optimization comparisons.

**Assumptions and scope:** Same instance family and total classical/quantum budget.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Include encoding, training, sampling and baseline work; separate finite evidence from approximation guarantees.

**Imported earlier results:** [26.5](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-5), [26.6](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-6), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Exact source targets:** [MIX:mixers](../references/proof-sources.md#source-mix-mixers): Section II Framework and Section III constrained-mixer constructions; [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Compare exhaustive and heuristic methods on identical inputs.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-8"></span>

### 26.8 Optimization laboratory

**Core result / role:** QAOA acceptance protocol.

**Assumptions and scope:** Independent exhaustive tiny-instance optimum.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Check feasibility, objective signs, distributions and complete optimization cost.

**Imported earlier results:** [26.2](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-2), [26.5](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-5), [26.6](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-6), [26.7](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-7).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Diagnose sign errors, infeasible samples and unsupported advantage claims.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 27: Quantum Learning, Kernels, and Hybrid Models

<span id="sec-quantum-learning-kernels-and-hybrid-models-1"></span>

### 27.1 Learning tasks and data-access assumptions

**Core result / role:** Learning task and generalization target.

**Assumptions and scope:** Explicit data distribution, train/test split and access model.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Define prediction loss and distinguish training fit from held-out performance.

**Imported earlier results:** [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6), [14.4](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4).

**Exact source targets:** [KERNEL:II.A](../references/proof-sources.md#source-kernel-ii-a): Section II A Feature maps and kernels.

**Independent evidence target:** Define a train/validation/test protocol before constructing a quantum model.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-learning-kernels-and-hybrid-models-2"></span>

### 27.2 Encoding data into quantum states

**Core result / role:** Encoding spectrum restricts model frequencies.

**Assumptions and scope:** Specified feature gate and generator spectrum.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive a finite Fourier expansion; include preparation/re-uploading cost.

**Imported earlier results:** [27.1](../section-plans/04-variational.md#sec-quantum-learning-kernels-and-hybrid-models-1), [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5), [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1).

**Exact source targets:** [ENC:I](../references/proof-sources.md#source-enc-i): Section I Quantum models as partial Fourier series; [ENC:II](../references/proof-sources.md#source-enc-ii): Section II The expressivity of quantum models.

**Independent evidence target:** Compare input normalization and state preparation with explicit vectors.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-learning-kernels-and-hybrid-models-3"></span>

### 27.3 Hybrid models and the joint chain rule

**Core result / role:** Joint classical-quantum chain rule.

**Assumptions and scope:** Differentiable preprocessing, quantum estimator and classical head.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive Jacobian/vector-Jacobian shapes and all parameter contributions; specify estimator boundaries.

**Imported earlier results:** [27.2](../section-plans/04-variational.md#sec-quantum-learning-kernels-and-hybrid-models-2), [23.5](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-5), [23.6](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-6).

**Exact source targets:** [PS:II](../references/proof-sources.md#source-ps-ii): Section II Computing Quantum Gradients; [ENC:IV](../references/proof-sources.md#source-enc-iv): Section IV Practical implications for quantum machine learning.

**Independent evidence target:** Check every component and their composition independently.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-learning-kernels-and-hybrid-models-4"></span>

### 27.4 Quantum feature maps and kernels

**Core result / role:** Quantum feature kernels are positive semidefinite.

**Assumptions and scope:** Exact feature states and specified inner-product/fidelity kernel.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Construct an explicit feature representation and prove Gram positivity; distinguish shot-noisy matrices.

**Imported earlier results:** [27.2](../section-plans/04-variational.md#sec-quantum-learning-kernels-and-hybrid-models-2), [2.2](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-2).

**Exact source targets:** [KERNEL:II.A](../references/proof-sources.md#source-kernel-ii-a): Section II A Feature maps and kernels; [KERNEL:II.C](../references/proof-sources.md#source-kernel-ii-c): Section II C Input encoding as a feature map.

**Independent evidence target:** Compare explicit feature vectors, circuit estimates and numerical kernel checks. Audit all pairwise kernel queries, finite-shot non-PSD estimates and any regularization/repair bias.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-learning-kernels-and-hybrid-models-5"></span>

### 27.5 Training kernels and hybrid models

**Core result / role:** Kernel fitting and joint circuit training are distinct optimization problems.

**Assumptions and scope:** Fixed versus trainable feature map; declared regularization.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive a selected classical kernel solve and the separate trainable-parameter chain rule.

**Imported earlier results:** [27.1](../section-plans/04-variational.md#sec-quantum-learning-kernels-and-hybrid-models-1), [27.4](../section-plans/04-variational.md#sec-quantum-learning-kernels-and-hybrid-models-4).

**Exact source targets:** [KERNEL:III.B](../references/proof-sources.md#source-kernel-iii-b): Section III B Building a quantum classifier; [KERNEL:III.D](../references/proof-sources.md#source-kernel-iii-d): Section III D An implicit quantum-assisted classifier.

**Independent evidence target:** Train tiny models with reproducible splits and inspect failure modes.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-learning-kernels-and-hybrid-models-6"></span>

### 27.6 Generalization and statistical claims

**Core result / role:** Held-out risk and finite-sample claims.

**Assumptions and scope:** Declared independent test set and bounded loss.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive one conservative concentration bound; defer full capacity/RKHS learning theory.

**Imported earlier results:** [27.1](../section-plans/04-variational.md#sec-quantum-learning-kernels-and-hybrid-models-1), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Exact source targets:** [CVX:7.4](../references/proof-sources.md#source-cvx-7-4): Section 7.4 Chebyshev and Chernoff bounds; [KERNEL:II.B](../references/proof-sources.md#source-kernel-ii-b): Section II B Reproducing kernel Hilbert spaces.

**Independent evidence target:** Report held-out uncertainty, repeated seeds and data leakage diagnostics.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-learning-kernels-and-hybrid-models-7"></span>

### 27.7 Classical simulability and meaningful baselines

**Core result / role:** Classically simulable features need matched baselines.

**Assumptions and scope:** Specified encoding, observable and data-access cost.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Identify a tractable selected feature model and compare total inference/training costs.

**Imported earlier results:** [27.4](../section-plans/04-variational.md#sec-quantum-learning-kernels-and-hybrid-models-4), [14.8](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-7).

**Exact source targets:** [KERNEL:III.A](../references/proof-sources.md#source-kernel-iii-a): Section III A Feature-encoding circuits; [ENC:IV](../references/proof-sources.md#source-enc-iv): Section IV Practical implications for quantum machine learning.

**Independent evidence target:** Compare like-for-like classical features, kernels and compute/measurement budgets.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-learning-kernels-and-hybrid-models-8"></span>

### 27.8 Learning laboratory and claim audit

**Core result / role:** Learning acceptance protocol.

**Assumptions and scope:** Held-out data, seeded repetitions and independent small features.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Audit leakage, kernel PSD treatment, uncertainty and full task cost.

**Imported earlier results:** [27.5](../section-plans/04-variational.md#sec-quantum-learning-kernels-and-hybrid-models-5), [27.6](../section-plans/04-variational.md#sec-quantum-learning-kernels-and-hybrid-models-6), [27.7](../section-plans/04-variational.md#sec-quantum-learning-kernels-and-hybrid-models-7).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Require a baseline, gradient verification and a complete cost record before interpreting usefulness.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.
