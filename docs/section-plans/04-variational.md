# Part 4. Variational and Differentiable Quantum Computing

**Detailed plan · 2026-10-20 · Planned material; editorial pass completed, external validation/freeze pending.** [All sections](../section-plan.md) · [Full plan](../book-plan.md) · [Reader continuity](../reader-continuity.md)

Each section specifies its argument and independent evidence. Framework implementation, mathematical review and reader review have separate status. Closing materials follow the [section-plan guide](../section-plan.md#how-to-read-the-specification).

<span id="ch-parameterized-circuits-quantum-gradients-and-differentiation"></span>

## Chapter 23

**Parameterized Circuits, Quantum Gradients, and Differentiation**

**Reading level:** Core. **Entry guidance:** 2–3, 5–6; a local calculus bridge precedes differentiation.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-1"></span>

### 23.1 Parameterized quantum models and tensor contracts

**Section level:** core. **Required earlier sections:** [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1), [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3).

**Learning and derivation target:** Define states, observable-valued outputs, parameter occurrences and batch dimensions.

**Implementation and evidence target:** Check a batched model against separate scalar executions.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-2"></span>

### 23.2 Differentiating a unitary expectation

**Section level:** core. **Required earlier sections:** [23.1](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-1), [2.6](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-6).

**Learning and derivation target:** Provide the needed scalar/multivariable product and chain rules locally; derive an expectation derivative with explicit conjugation, real parameters and generator assumptions.

**Implementation and evidence target:** Compare a generator-based expression with dense derivatives.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-3"></span>

### 23.3 The single-Pauli parameter-shift rule

**Section level:** core. **Required earlier sections:** [23.2](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-2), [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5).

**Learning and derivation target:** Derive the shift and prefactor from the generator's two eigenvalues.

**Implementation and evidence target:** Expand the existing starter with analytic and shifted-execution checks.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-4"></span>

### 23.4 Generator spectra and generalized shift rules [Advanced]

**Section level:** advanced. **Required earlier sections:** [23.2](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-2), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Learning and derivation target:** Explain how spectral gaps determine the frequency structure and valid rules.

**Implementation and evidence target:** Test a multi-eigenvalue example against an independent spectral reference.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-5"></span>

### 23.5 Shared parameters and classical reparameterization

**Section level:** core. **Required earlier sections:** [23.2](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-2), [23.3](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-3).

**Learning and derivation target:** Derive the sum over occurrences and the classical chain rule.

**Implementation and evidence target:** Check a reused parameter and a scaled angle; diagnose a missing chain-rule factor.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-6"></span>

### 23.6 Backpropagation and automatic differentiation

**Section level:** core. **Required earlier sections:** [23.2](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-2), [23.5](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-5).

**Learning and derivation target:** Explain the mathematical derivative and the computational graph that carries it. Separate simulator backpropagation through amplitudes from hardware estimators such as parameter shift; specify what classical data crosses the device boundary.

**Implementation and evidence target:** Check real outputs, complex state tensors and deliberate detach errors.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-7"></span>

### 23.7 Adjoint differentiation and memory tradeoffs

**Section level:** core. **Required earlier sections:** [23.2](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-2), [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1).

**Learning and derivation target:** Derive reverse propagation for a pure-state circuit and state its assumptions.

**Implementation and evidence target:** Compare gradients and operation/memory counts with a simple independent implementation.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-8"></span>

### 23.8 Finite differences and numerical diagnostics

**Section level:** core. **Required earlier sections:** [23.2](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-2), [2.8](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-8).

**Learning and derivation target:** Analyze truncation, rounding and step-size sensitivity.

**Implementation and evidence target:** Sweep finite-difference steps and compare with an exact analytic derivative.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-9"></span>

### 23.9 Finite-shot gradient estimation

**Section level:** core. **Required earlier sections:** [23.3](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-3), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Learning and derivation target:** Derive estimator variance under a declared measurement/allocation model.

**Implementation and evidence target:** Compare exact gradients with repeated stochastic estimates and their uncertainty.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-10"></span>

### 23.10 Differentiation laboratory and cost audit

**Section level:** core. **Required earlier sections:** [23.3](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-3), [23.5](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-5), [23.6](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-6), [23.8](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-8), [23.9](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-9), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Learning and derivation target:** Combine parameter structure, derivative method, accuracy and complete execution cost.

**Implementation and evidence target:** Require analytic, dense, shifted and autograd agreement where each method applies.

<span id="ch-optimization-geometry-and-trainability"></span>

## Chapter 24

**Optimization, Geometry, and Trainability**

**Reading level:** Advanced. **Entry guidance:** 23 for entry; 6 for stochastic estimates and 10.3 for geometry, without all state-inference material.

<span id="sec-optimization-geometry-and-trainability-1"></span>

### 24.1 Objectives and optimization problems

**Section level:** advanced. **Required earlier sections:** [23.1](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-1), [23.2](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-2).

**Learning and derivation target:** Distinguish an expectation model, a loss, constraints and the desired optimum.

**Implementation and evidence target:** Specify a small objective with a known analytic or exhaustive reference.

<span id="sec-optimization-geometry-and-trainability-2"></span>

### 24.2 Exact and stochastic gradients

**Section level:** advanced. **Required earlier sections:** [24.1](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-1), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Learning and derivation target:** Derive how gradient noise enters a selected update rule.

**Implementation and evidence target:** Compare deterministic and finite-shot trajectories under matched initialization.

<span id="sec-optimization-geometry-and-trainability-3"></span>

### 24.3 Optimizers, initialization, and diagnostics

**Section level:** advanced. **Required earlier sections:** [24.1](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-1), [24.2](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-2).

**Learning and derivation target:** Explain optimizer state, post-update loss, stopping and local minima.

**Implementation and evidence target:** Log reproducible trajectories and compare multiple starts without cherry-picking.

<span id="sec-optimization-geometry-and-trainability-4"></span>

### 24.4 Quantum geometric tensor

**Section level:** advanced. **Required earlier sections:** [23.2](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-2), [10.3](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-3).

**Learning and derivation target:** Derive the state-space metric and identify phase/gauge redundancy.

**Implementation and evidence target:** Compare analytic metric entries with independent state derivatives.

<span id="sec-optimization-geometry-and-trainability-5"></span>

### 24.5 Natural-gradient updates and singular metrics

**Section level:** advanced. **Required earlier sections:** [24.3](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-3), [24.4](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-4), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Learning and derivation target:** Derive a constrained or regularized update and its assumptions.

**Implementation and evidence target:** Study rank deficiency, regularization and step sensitivity in a tiny model.

<span id="sec-optimization-geometry-and-trainability-6"></span>

### 24.6 Expressivity, identifiability, and trainability

**Section level:** advanced. **Required earlier sections:** [23.1](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-1), [24.1](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-1).

**Learning and derivation target:** Separate representable functions from the ability to identify or optimize parameters.

**Implementation and evidence target:** Construct redundant parameterizations and compare behavior.

<span id="sec-optimization-geometry-and-trainability-7"></span>

### 24.7 Barren plateaus and ensemble assumptions [Advanced]

**Section level:** advanced. **Required earlier sections:** [24.2](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-2), [24.6](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-6).

**Learning and derivation target:** State a selected gradient-concentration theorem and explain its proof structure and scaling assumptions.

**Implementation and evidence target:** Use controlled finite examples as illustrations; do not treat a random-circuit plot as a general proof.

<span id="sec-optimization-geometry-and-trainability-8"></span>

### 24.8 Noise, shot budgets, and mitigation overhead

**Section level:** advanced. **Required earlier sections:** [24.2](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-2), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Learning and derivation target:** Relate estimator variance and bias to optimization effort.

**Implementation and evidence target:** Compare configurations with a fixed total execution budget.

<span id="sec-optimization-geometry-and-trainability-9"></span>

### 24.9 Optimization laboratory and honest conclusions

**Section level:** advanced. **Required earlier sections:** [24.3](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-3), [24.6](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-6).

**Learning and derivation target:** Distinguish convergence evidence from global optimality and model utility.

**Implementation and evidence target:** Compare an optimizer result with exact references and report failed runs.

<span id="ch-variational-simulation-chemistry-and-ground-state-problems"></span>

## Chapter 25

**Variational Simulation, Chemistry, and Ground-State Problems**

**Reading level:** Core application. **Entry guidance:** 2, 4, 6 for the energy/model entry; selected 23–24 for optimization and embedding extensions.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-1"></span>

### 25.1 The variational principle and its assumptions

**Section level:** core. **Required earlier sections:** [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5), [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3).

**Learning and derivation target:** Prove the ground-energy upper bound and identify normalization/subspace assumptions.

**Implementation and evidence target:** Check the bound and construct a counterexample from an invalid estimator/model.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-2"></span>

### 25.2 Second quantization and occupation states

**Section level:** core. **Required earlier sections:** [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3).

**Learning and derivation target:** Define fermionic modes, creation/annihilation operators and sign conventions.

**Implementation and evidence target:** Build a tiny occupation-basis Hamiltonian independently.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-3"></span>

### 25.3 Jordan-Wigner and fermion-to-qubit translation

**Section level:** core. **Required earlier sections:** [25.2](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-2), [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5), [4.3](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-3).

**Learning and derivation target:** Derive the parity strings and verify anticommutation relations.

**Implementation and evidence target:** Compare fermionic and qubit Hamiltonian matrices.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-4"></span>

### 25.4 Symmetries and reduced models

**Section level:** core. **Required earlier sections:** [25.3](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-3), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Learning and derivation target:** Explain conserved sectors and the conditions for valid reductions.

**Implementation and evidence target:** Compare sector spectra and identify an incorrect reference-state sector.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-5"></span>

### 25.5 Ansatz design and reachable states

**Section level:** core. **Required earlier sections:** [25.1](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-1), [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1), [23.1](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-1).

**Learning and derivation target:** Relate physical structure, circuit expressivity and parameterization.

**Implementation and evidence target:** Compare a chosen ansatz with an exactly solvable tiny subspace.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-6"></span>

### 25.6 Measuring an energy objective

**Section level:** core. **Required earlier sections:** [25.1](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-1), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7), [10.7](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-6).

**Learning and derivation target:** Derive Pauli-weighted estimates and shot-allocation uncertainty.

**Implementation and evidence target:** Compare exact energy with grouped finite-shot estimators.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-7"></span>

### 25.7 Variational dynamics and extensions [Advanced]

**Section level:** advanced. **Required earlier sections:** [25.5](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-5), [24.4](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-4), [19.1](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-1).

**Learning and derivation target:** Derive a selected projected time-evolution principle and its linear system.

**Implementation and evidence target:** Compare a tiny variational trajectory with exact dynamics.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-8"></span>

### 25.8 Chemistry model and error budgets

**Section level:** core. **Required earlier sections:** [25.3](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-3), [25.4](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-4), [25.6](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-6).

**Learning and derivation target:** Separate basis, mapping, truncation, ansatz, optimization and sampling errors.

**Implementation and evidence target:** Record units, constant offsets and independent reference energies.

<span id="sec-quantum-embedding-model"></span>

### 25.9 Classical environments and quantum embedding [Advanced]

**Section level:** advanced. **Required earlier sections:** [25.2](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-2), [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4).

**Learning and derivation target:** Derive a tractable fragment/bath or active-space construction with explicitly stated approximation and double-counting conventions.

**Implementation and evidence target:** Compare the embedded Hamiltonian and observables against a complete small classical reference; identify which properties embedding approximates.

<span id="sec-quantum-embedding-self-consistency"></span>

### 25.10 Self-consistent quantum impurity solvers [Advanced]

**Section level:** advanced. **Required earlier sections:** [25.9](../section-plans/04-variational.md#sec-quantum-embedding-model), [25.6](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-6), [24.3](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-3).

**Learning and derivation target:** Specify a classical environment update driven by quantum-estimated reduced observables; distinguish inner solver error from outer self-consistency and embedding error.

**Implementation and evidence target:** Compare exact-fragment and quantum-estimator loops on the same tiny model, including shot uncertainty, convergence and failure cases.

<span id="sec-sample-assisted-subspace-solve"></span>

### 25.11 Quantum sampling and classical subspace diagonalization [Advanced]

**Section level:** advanced. **Required earlier sections:** [25.1](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-1), [25.3](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-3), [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Learning and derivation target:** Define a sampled-configuration subspace, its projected Hamiltonian and a classical eigenvalue solve with the precise assumptions behind any variational statement.

**Implementation and evidence target:** Compare selected configurations and projected solutions with exact tiny-instance results; record quantum sampling, configuration processing and classical solve costs.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-9"></span>
<span id="259-variational-simulation-laboratory"></span>

### 25.12 Variational-simulation laboratory

**Section level:** core. **Required earlier sections:** [25.1](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-1), [25.3](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-3), [25.5](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-5), [25.6](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-6), [24.3](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-3).

**Learning and derivation target:** Connect Hamiltonian construction, circuit model, optimization and evidence.

**Implementation and evidence target:** Verify matrices before training and interpret the final result with all declared limitations.

<span id="ch-qaoa-quantum-optimization-and-classical-comparisons"></span>

## Chapter 26

**QAOA, Quantum Optimization, and Classical Comparisons**

**Reading level:** Advanced application. **Entry guidance:** 5–6, 14; selected 23–24 for the optimization branch.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-1"></span>

### 26.1 From a discrete objective to a Hamiltonian

**Section level:** advanced. **Required earlier sections:** [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2), [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3).

**Learning and derivation target:** Derive a small MaxCut cost and state bit/spin/sign conventions.

**Implementation and evidence target:** Compare every bit-string energy with its classical objective.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-2"></span>

### 26.2 Cost and mixer evolution

**Section level:** advanced. **Required earlier sections:** [26.1](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-1), [19.5](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-5).

**Learning and derivation target:** Derive the alternating-unitary circuit and identify normalization conventions.

**Implementation and evidence target:** Compare circuit layers with independent matrix exponentials.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-3"></span>

### 26.3 Low-depth analytic behavior

**Section level:** advanced. **Required earlier sections:** [26.2](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-2), [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3).

**Learning and derivation target:** Derive one selected graph's expectation at small depth.

**Implementation and evidence target:** Check parameter-dependent predictions with exhaustive references.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-4"></span>

### 26.4 Constraints and feasible mixers [Advanced]

**Section level:** advanced. **Required earlier sections:** [26.1](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-1), [26.2](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-2).

**Learning and derivation target:** Specify a constrained search space and derive a mixer that preserves it.

**Implementation and evidence target:** Verify invariance and diagnose leakage outside the feasible subspace.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-5"></span>

### 26.5 Parameter landscapes and depth

**Section level:** advanced. **Required earlier sections:** [26.3](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-3), [24.3](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-3).

**Learning and derivation target:** Explain parameter periodicity, symmetries and optimization challenges.

**Implementation and evidence target:** Compare grids and optimized results with an exact tiny-instance landscape.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-6"></span>

### 26.6 Sampled solutions and approximation quality

**Section level:** advanced. **Required earlier sections:** [26.1](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-1), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Learning and derivation target:** Define expectation, best observed sample and approximation metric separately.

**Implementation and evidence target:** Report distributions and finite-sample uncertainty rather than only the best sample.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-7"></span>

### 26.7 Classical comparisons and total cost

**Section level:** advanced. **Required earlier sections:** [26.5](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-5), [26.6](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-6), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Learning and derivation target:** State matched objectives, time/budget boundaries and baseline assumptions.

**Implementation and evidence target:** Compare exhaustive and heuristic methods on identical inputs.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-8"></span>

### 26.8 Optimization laboratory

**Section level:** advanced. **Required earlier sections:** [26.2](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-2), [26.5](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-5), [26.6](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-6), [26.7](../section-plans/04-variational.md#sec-qaoa-quantum-optimization-and-classical-comparisons-7).

**Learning and derivation target:** Require an end-to-end objective mapping, optimizer record and solution interpretation.

**Implementation and evidence target:** Diagnose sign errors, infeasible samples and unsupported advantage claims.

<span id="ch-quantum-learning-kernels-and-hybrid-models"></span>

## Chapter 27

**Quantum Learning, Kernels, and Hybrid Models**

**Reading level:** Advanced application. **Entry guidance:** 6, 14 and a local learning/statistics bridge; 23–24 for trainable layers, not fixed-kernel entry.

<span id="sec-quantum-learning-kernels-and-hybrid-models-1"></span>

### 27.1 Learning tasks and data-access assumptions

**Section level:** core. **Required earlier sections:** [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6), [14.4](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4).

**Learning and derivation target:** Specify labels, distributions, encoding access and the desired prediction.

**Implementation and evidence target:** Define a train/validation/test protocol before constructing a quantum model.

<span id="sec-quantum-learning-kernels-and-hybrid-models-2"></span>

### 27.2 Encoding data into quantum states

**Section level:** core. **Required earlier sections:** [27.1](../section-plans/04-variational.md#sec-quantum-learning-kernels-and-hybrid-models-1), [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5), [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1).

**Learning and derivation target:** Derive selected angle/amplitude encodings and their resource implications.

**Implementation and evidence target:** Compare input normalization and state preparation with explicit vectors.

<span id="sec-quantum-learning-kernels-and-hybrid-models-3"></span>

### 27.3 Hybrid models and the joint chain rule

**Section level:** advanced. **Required earlier sections:** [27.2](../section-plans/04-variational.md#sec-quantum-learning-kernels-and-hybrid-models-2), [23.5](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-5), [23.6](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-6).

**Learning and derivation target:** Derive classical preprocessing, quantum expectation and output-head gradients. Distinguish trainable quantum layers, fixed quantum features and a kernel-estimation pipeline; identify which parameters actually require quantum derivatives.

**Implementation and evidence target:** Check every component and their composition independently.

<span id="sec-quantum-learning-kernels-and-hybrid-models-4"></span>

### 27.4 Quantum feature maps and kernels

**Section level:** core. **Required earlier sections:** [27.2](../section-plans/04-variational.md#sec-quantum-learning-kernels-and-hybrid-models-2), [2.2](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-2).

**Learning and derivation target:** Derive overlap-based kernels and Gram-matrix properties.

**Implementation and evidence target:** Compare explicit feature vectors, circuit estimates and numerical kernel checks. Audit all pairwise kernel queries, finite-shot non-PSD estimates and any regularization/repair bias.

<span id="sec-quantum-learning-kernels-and-hybrid-models-5"></span>

### 27.5 Training kernels and hybrid models

**Section level:** core. **Required earlier sections:** [27.1](../section-plans/04-variational.md#sec-quantum-learning-kernels-and-hybrid-models-1), [27.4](../section-plans/04-variational.md#sec-quantum-learning-kernels-and-hybrid-models-4).

**Learning and derivation target:** Explain regularization, optimization and estimator noise.

**Implementation and evidence target:** Train tiny models with reproducible splits and inspect failure modes.

<span id="sec-quantum-learning-kernels-and-hybrid-models-6"></span>

### 27.6 Generalization and statistical claims

**Section level:** core. **Required earlier sections:** [27.1](../section-plans/04-variational.md#sec-quantum-learning-kernels-and-hybrid-models-1), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Learning and derivation target:** State a selected learning guarantee's assumptions and distinguish empirical evaluation.

**Implementation and evidence target:** Report held-out uncertainty, repeated seeds and data leakage diagnostics.

<span id="sec-quantum-learning-kernels-and-hybrid-models-7"></span>

### 27.7 Classical simulability and meaningful baselines

**Section level:** core. **Required earlier sections:** [27.4](../section-plans/04-variational.md#sec-quantum-learning-kernels-and-hybrid-models-4), [14.8](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-7).

**Learning and derivation target:** Relate encoding/model structure to possible classical implementations.

**Implementation and evidence target:** Compare like-for-like classical features, kernels and compute/measurement budgets.

<span id="sec-quantum-learning-kernels-and-hybrid-models-8"></span>

### 27.8 Learning laboratory and claim audit

**Section level:** core. **Required earlier sections:** [27.5](../section-plans/04-variational.md#sec-quantum-learning-kernels-and-hybrid-models-5), [27.6](../section-plans/04-variational.md#sec-quantum-learning-kernels-and-hybrid-models-6), [27.7](../section-plans/04-variational.md#sec-quantum-learning-kernels-and-hybrid-models-7).

**Learning and derivation target:** Connect mathematical model, data protocol, implementation and evidence.

**Implementation and evidence target:** Require a baseline, gradient verification and a complete cost record before interpreting usefulness.
