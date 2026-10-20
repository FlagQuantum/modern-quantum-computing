# Part 4. Variational and Differentiable Quantum Computing

**Detailed plan · 2026-10-20 · Planned material; architecture review pending.** [All sections](../section-plan.md) · [Full plan](../book-plan.md) · [Reader continuity](../reader-continuity.md)

Each section specifies its argument and independent evidence. Framework implementation, mathematical review and reader review have separate status. Closing materials follow the [section-plan guide](../section-plan.md#how-to-read-the-specification).

<span id="ch-parameterized-circuits-quantum-gradients-and-differentiation"></span>

## Chapter 23

**Parameterized Circuits, Quantum Gradients, and Differentiation**

**Reading level:** Core. **Chapter prerequisites:** 2–6; elementary calculus.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-1"></span>

### 23.1 Parameterized quantum models and tensor contracts

**Learning and derivation target:** Define states, observable-valued outputs, parameter occurrences and batch dimensions.

**Implementation and evidence target:** Check a batched model against separate scalar executions.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-2"></span>

### 23.2 Differentiating a unitary expectation

**Learning and derivation target:** Derive the expectation derivative with explicit complex conjugation and real-parameter assumptions.

**Implementation and evidence target:** Compare a generator-based expression with dense derivatives.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-3"></span>

### 23.3 The single-Pauli parameter-shift rule

**Learning and derivation target:** Derive the shift and prefactor from the generator's two eigenvalues.

**Implementation and evidence target:** Expand the existing starter with analytic and shifted-execution checks.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-4"></span>

### 23.4 Generator spectra and generalized shift rules [Advanced]

**Learning and derivation target:** Explain how spectral gaps determine the frequency structure and valid rules.

**Implementation and evidence target:** Test a multi-eigenvalue example against an independent spectral reference.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-5"></span>

### 23.5 Shared parameters and classical reparameterization

**Learning and derivation target:** Derive the sum over occurrences and the classical chain rule.

**Implementation and evidence target:** Check a reused parameter and a scaled angle; diagnose a missing chain-rule factor.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-6"></span>

### 23.6 Backpropagation and automatic differentiation

**Learning and derivation target:** Explain the mathematical derivative and the computational graph that carries it. Separate simulator backpropagation through amplitudes from hardware estimators such as parameter shift; specify what classical data crosses the device boundary.

**Implementation and evidence target:** Check real outputs, complex state tensors and deliberate detach errors.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-7"></span>

### 23.7 Adjoint differentiation and memory tradeoffs

**Learning and derivation target:** Derive reverse propagation for a pure-state circuit and state its assumptions.

**Implementation and evidence target:** Compare gradients and operation/memory counts with a simple independent implementation.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-8"></span>

### 23.8 Finite differences and numerical diagnostics

**Learning and derivation target:** Analyze truncation, rounding and step-size sensitivity.

**Implementation and evidence target:** Sweep finite-difference steps and compare with an exact analytic derivative.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-9"></span>

### 23.9 Finite-shot gradient estimation

**Learning and derivation target:** Derive estimator variance under a declared measurement/allocation model.

**Implementation and evidence target:** Compare exact gradients with repeated stochastic estimates and their uncertainty.

<span id="sec-parameterized-circuits-quantum-gradients-and-differentiation-10"></span>

### 23.10 Differentiation laboratory and cost audit

**Learning and derivation target:** Combine parameter structure, derivative method, accuracy and complete execution cost.

**Implementation and evidence target:** Require analytic, dense, shifted and autograd agreement where each method applies.

<span id="ch-optimization-geometry-and-trainability"></span>

## Chapter 24

**Optimization, Geometry, and Trainability**

**Reading level:** Advanced. **Chapter prerequisites:** 10, 14, 23.

<span id="sec-optimization-geometry-and-trainability-1"></span>

### 24.1 Objectives and optimization problems

**Learning and derivation target:** Distinguish an expectation model, a loss, constraints and the desired optimum.

**Implementation and evidence target:** Specify a small objective with a known analytic or exhaustive reference.

<span id="sec-optimization-geometry-and-trainability-2"></span>

### 24.2 Exact and stochastic gradients

**Learning and derivation target:** Derive how gradient noise enters a selected update rule.

**Implementation and evidence target:** Compare deterministic and finite-shot trajectories under matched initialization.

<span id="sec-optimization-geometry-and-trainability-3"></span>

### 24.3 Optimizers, initialization, and diagnostics

**Learning and derivation target:** Explain optimizer state, post-update loss, stopping and local minima.

**Implementation and evidence target:** Log reproducible trajectories and compare multiple starts without cherry-picking.

<span id="sec-optimization-geometry-and-trainability-4"></span>

### 24.4 Quantum geometric tensor

**Learning and derivation target:** Derive the state-space metric and identify phase/gauge redundancy.

**Implementation and evidence target:** Compare analytic metric entries with independent state derivatives.

<span id="sec-optimization-geometry-and-trainability-5"></span>

### 24.5 Natural-gradient updates and singular metrics

**Learning and derivation target:** Derive a constrained or regularized update and its assumptions.

**Implementation and evidence target:** Study rank deficiency, regularization and step sensitivity in a tiny model.

<span id="sec-optimization-geometry-and-trainability-6"></span>

### 24.6 Expressivity, identifiability, and trainability

**Learning and derivation target:** Separate representable functions from the ability to identify or optimize parameters.

**Implementation and evidence target:** Construct redundant parameterizations and compare behavior.

<span id="sec-optimization-geometry-and-trainability-7"></span>

### 24.7 Barren plateaus and ensemble assumptions [Advanced]

**Learning and derivation target:** State a selected gradient-concentration theorem and explain its proof structure and scaling assumptions.

**Implementation and evidence target:** Use controlled finite examples as illustrations; do not treat a random-circuit plot as a general proof.

<span id="sec-optimization-geometry-and-trainability-8"></span>

### 24.8 Noise, shot budgets, and mitigation overhead

**Learning and derivation target:** Relate estimator variance and bias to optimization effort.

**Implementation and evidence target:** Compare configurations with a fixed total execution budget.

<span id="sec-optimization-geometry-and-trainability-9"></span>

### 24.9 Optimization laboratory and honest conclusions

**Learning and derivation target:** Distinguish convergence evidence from global optimality and model utility.

**Implementation and evidence target:** Compare an optimizer result with exact references and report failed runs.

<span id="ch-variational-simulation-chemistry-and-ground-state-problems"></span>

## Chapter 25

**Variational Simulation, Chemistry, and Ground-State Problems**

**Reading level:** Core application. **Chapter prerequisites:** 8, 14, 19, 23–24.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-1"></span>

### 25.1 The variational principle and its assumptions

**Learning and derivation target:** Prove the ground-energy upper bound and identify normalization/subspace assumptions.

**Implementation and evidence target:** Check the bound and construct a counterexample from an invalid estimator/model.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-2"></span>

### 25.2 Second quantization and occupation states

**Learning and derivation target:** Define fermionic modes, creation/annihilation operators and sign conventions.

**Implementation and evidence target:** Build a tiny occupation-basis Hamiltonian independently.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-3"></span>

### 25.3 Jordan-Wigner and fermion-to-qubit translation

**Learning and derivation target:** Derive the parity strings and verify anticommutation relations.

**Implementation and evidence target:** Compare fermionic and qubit Hamiltonian matrices.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-4"></span>

### 25.4 Symmetries and reduced models

**Learning and derivation target:** Explain conserved sectors and the conditions for valid reductions.

**Implementation and evidence target:** Compare sector spectra and identify an incorrect reference-state sector.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-5"></span>

### 25.5 Ansatz design and reachable states

**Learning and derivation target:** Relate physical structure, circuit expressivity and parameterization.

**Implementation and evidence target:** Compare a chosen ansatz with an exactly solvable tiny subspace.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-6"></span>

### 25.6 Measuring an energy objective

**Learning and derivation target:** Derive Pauli-weighted estimates and shot-allocation uncertainty.

**Implementation and evidence target:** Compare exact energy with grouped finite-shot estimators.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-7"></span>

### 25.7 Variational dynamics and extensions [Advanced]

**Learning and derivation target:** Derive a selected projected time-evolution principle and its linear system.

**Implementation and evidence target:** Compare a tiny variational trajectory with exact dynamics.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-8"></span>

### 25.8 Chemistry model and error budgets

**Learning and derivation target:** Separate basis, mapping, truncation, ansatz, optimization and sampling errors.

**Implementation and evidence target:** Record units, constant offsets and independent reference energies.

<span id="sec-quantum-embedding-model"></span>

### 25.9 Classical environments and quantum embedding [Advanced]

**Learning and derivation target:** Derive a tractable fragment/bath or active-space construction with explicitly stated approximation and double-counting conventions.

**Implementation and evidence target:** Compare the embedded Hamiltonian and observables against a complete small classical reference; identify which properties embedding approximates.

<span id="sec-quantum-embedding-self-consistency"></span>

### 25.10 Self-consistent quantum impurity solvers [Advanced]

**Learning and derivation target:** Specify a classical environment update driven by quantum-estimated reduced observables; distinguish inner solver error from outer self-consistency and embedding error.

**Implementation and evidence target:** Compare exact-fragment and quantum-estimator loops on the same tiny model, including shot uncertainty, convergence and failure cases.

<span id="sec-sample-assisted-subspace-solve"></span>

### 25.11 Quantum sampling and classical subspace diagonalization [Advanced]

**Learning and derivation target:** Define a sampled-configuration subspace, its projected Hamiltonian and a classical eigenvalue solve with the precise assumptions behind any variational statement.

**Implementation and evidence target:** Compare selected configurations and projected solutions with exact tiny-instance results; record quantum sampling, configuration processing and classical solve costs.

<span id="sec-variational-simulation-chemistry-and-ground-state-problems-9"></span>
<span id="259-variational-simulation-laboratory"></span>

### 25.12 Variational-simulation laboratory

**Learning and derivation target:** Connect Hamiltonian construction, circuit model, optimization and evidence.

**Implementation and evidence target:** Verify matrices before training and interpret the final result with all declared limitations.

<span id="ch-qaoa-quantum-optimization-and-classical-comparisons"></span>

## Chapter 26

**QAOA, Quantum Optimization, and Classical Comparisons**

**Reading level:** Advanced application. **Chapter prerequisites:** 14–16, 23, 24.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-1"></span>

### 26.1 From a discrete objective to a Hamiltonian

**Learning and derivation target:** Derive a small MaxCut cost and state bit/spin/sign conventions.

**Implementation and evidence target:** Compare every bit-string energy with its classical objective.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-2"></span>

### 26.2 Cost and mixer evolution

**Learning and derivation target:** Derive the alternating-unitary circuit and identify normalization conventions.

**Implementation and evidence target:** Compare circuit layers with independent matrix exponentials.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-3"></span>

### 26.3 Low-depth analytic behavior

**Learning and derivation target:** Derive one selected graph's expectation at small depth.

**Implementation and evidence target:** Check parameter-dependent predictions with exhaustive references.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-4"></span>

### 26.4 Constraints and feasible mixers [Advanced]

**Learning and derivation target:** Specify a constrained search space and derive a mixer that preserves it.

**Implementation and evidence target:** Verify invariance and diagnose leakage outside the feasible subspace.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-5"></span>

### 26.5 Parameter landscapes and depth

**Learning and derivation target:** Explain parameter periodicity, symmetries and optimization challenges.

**Implementation and evidence target:** Compare grids and optimized results with an exact tiny-instance landscape.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-6"></span>

### 26.6 Sampled solutions and approximation quality

**Learning and derivation target:** Define expectation, best observed sample and approximation metric separately.

**Implementation and evidence target:** Report distributions and finite-sample uncertainty rather than only the best sample.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-7"></span>

### 26.7 Classical comparisons and total cost

**Learning and derivation target:** State matched objectives, time/budget boundaries and baseline assumptions.

**Implementation and evidence target:** Compare exhaustive and heuristic methods on identical inputs.

<span id="sec-qaoa-quantum-optimization-and-classical-comparisons-8"></span>

### 26.8 Optimization laboratory

**Learning and derivation target:** Require an end-to-end objective mapping, optimizer record and solution interpretation.

**Implementation and evidence target:** Diagnose sign errors, infeasible samples and unsupported advantage claims.

<span id="ch-quantum-learning-kernels-and-hybrid-models"></span>

## Chapter 27

**Quantum Learning, Kernels, and Hybrid Models**

**Reading level:** Advanced application. **Chapter prerequisites:** 10, 14, 23, 24; basic machine learning.

<span id="sec-quantum-learning-kernels-and-hybrid-models-1"></span>

### 27.1 Learning tasks and data-access assumptions

**Learning and derivation target:** Specify labels, distributions, encoding access and the desired prediction.

**Implementation and evidence target:** Define a train/validation/test protocol before constructing a quantum model.

<span id="sec-quantum-learning-kernels-and-hybrid-models-2"></span>

### 27.2 Encoding data into quantum states

**Learning and derivation target:** Derive selected angle/amplitude encodings and their resource implications.

**Implementation and evidence target:** Compare input normalization and state preparation with explicit vectors.

<span id="sec-quantum-learning-kernels-and-hybrid-models-3"></span>

### 27.3 Hybrid models and the joint chain rule

**Learning and derivation target:** Derive classical preprocessing, quantum expectation and output-head gradients. Distinguish trainable quantum layers, fixed quantum features and a kernel-estimation pipeline; identify which parameters actually require quantum derivatives.

**Implementation and evidence target:** Check every component and their composition independently.

<span id="sec-quantum-learning-kernels-and-hybrid-models-4"></span>

### 27.4 Quantum feature maps and kernels

**Learning and derivation target:** Derive overlap-based kernels and Gram-matrix properties.

**Implementation and evidence target:** Compare explicit feature vectors, circuit estimates and numerical kernel checks. Audit all pairwise kernel queries, finite-shot non-PSD estimates and any regularization/repair bias.

<span id="sec-quantum-learning-kernels-and-hybrid-models-5"></span>

### 27.5 Training kernels and hybrid models

**Learning and derivation target:** Explain regularization, optimization and estimator noise.

**Implementation and evidence target:** Train tiny models with reproducible splits and inspect failure modes.

<span id="sec-quantum-learning-kernels-and-hybrid-models-6"></span>

### 27.6 Generalization and statistical claims

**Learning and derivation target:** State a selected learning guarantee's assumptions and distinguish empirical evaluation.

**Implementation and evidence target:** Report held-out uncertainty, repeated seeds and data leakage diagnostics.

<span id="sec-quantum-learning-kernels-and-hybrid-models-7"></span>

### 27.7 Classical simulability and meaningful baselines

**Learning and derivation target:** Relate encoding/model structure to possible classical implementations.

**Implementation and evidence target:** Compare like-for-like classical features, kernels and compute/measurement budgets.

<span id="sec-quantum-learning-kernels-and-hybrid-models-8"></span>

### 27.8 Learning laboratory and claim audit

**Learning and derivation target:** Connect mathematical model, data protocol, implementation and evidence.

**Implementation and evidence target:** Require a baseline, gradient verification and a complete cost record before interpreting usefulness.
