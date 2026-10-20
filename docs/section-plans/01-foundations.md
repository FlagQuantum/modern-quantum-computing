# Part 1. Foundations and Quantum Information Primitives

**Detailed plan · 2026-10-20 · Planned material; editorial pass completed, external validation/freeze pending.** [All sections](../section-plan.md) · [Full plan](../book-plan.md) · [Reader continuity](../reader-continuity.md)

Each section specifies its argument and independent evidence. Framework implementation, mathematical review and reader review have separate status. Closing materials follow the [section-plan guide](../section-plan.md#how-to-read-the-specification).

<span id="ch-what-quantum-computing-computes"></span>

## Chapter 1

**What Quantum Computing Computes**

**Reading level:** Core. **Entry guidance:** Basic Python and arithmetic; the opening calculation is an explicitly supplied preview.

<span id="sec-what-quantum-computing-computes-1"></span>

### 1.1 Problems, inputs, and observable outputs

**Section level:** core. **Required earlier sections:** Entry knowledge / local bridge.

**Learning and derivation target:** Identify a computational task and what an algorithm must return.

**Implementation and evidence target:** Specify input size, requested output and success criterion for a tiny task.

<span id="sec-what-quantum-computing-computes-2"></span>

### 1.2 A first interference experiment

**Section level:** core. **Required earlier sections:** [1.1](../section-plans/01-foundations.md#sec-what-quantum-computing-computes-1).

**Learning and derivation target:** Predict the small experiment using explicitly supplied arithmetic/probability rules; identify it as a preview whose formal state/measurement derivation is developed in Chapters 3–6.

**Implementation and evidence target:** Compare a hand calculation, a two-by-two matrix reference and a small FlagQuantum circuit.

<span id="sec-what-quantum-computing-computes-3"></span>

### 1.3 What a quantum state describes

**Section level:** core. **Required earlier sections:** [1.2](../section-plans/01-foundations.md#sec-what-quantum-computing-computes-2).

**Learning and derivation target:** Introduce amplitudes and normalization informally; distinguish a state description from an observed sample.

**Implementation and evidence target:** Contrast full simulated amplitudes with the information available from repeated measurements.

<span id="sec-what-quantum-computing-computes-4"></span>

### 1.4 Algorithms, simulators, and physical devices

**Section level:** core. **Required earlier sections:** [1.1](../section-plans/01-foundations.md#sec-what-quantum-computing-computes-1).

**Learning and derivation target:** Explain the mathematical model, a classical executor and an experiment as different sources of evidence.

**Implementation and evidence target:** Annotate which parts of the opening calculation are mathematical, simulated or measured.

<span id="sec-what-quantum-computing-computes-5"></span>

### 1.5 What computational advantage would require

**Section level:** core. **Required earlier sections:** [1.4](../section-plans/01-foundations.md#sec-what-quantum-computing-computes-4).

**Learning and derivation target:** Introduce fair input/output access and total-resource accounting without requiring complexity theory.

**Implementation and evidence target:** Diagnose an invalid speedup claim based on simulator wall time or free data loading.

<span id="sec-what-quantum-computing-computes-6"></span>

### 1.6 A map of the learning routes

**Section level:** core. **Required earlier sections:** [1.4](../section-plans/01-foundations.md#sec-what-quantum-computing-computes-4).

**Learning and derivation target:** Explain the progression from a concrete question to definitions, proofs, implementation and evidence.

**Implementation and evidence target:** Choose an introductory route and complete a notation/background diagnostic.

<span id="ch-complex-vectors-operators-and-numerical-reasoning"></span>

## Chapter 2

**Complex Vectors, Operators, and Numerical Reasoning**

**Reading level:** Core. **Entry guidance:** Basic Python; introductory linear algebra is refreshed locally.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-1"></span>

### 2.1 Complex scalars, vectors, and conjugation

**Section level:** core. **Required earlier sections:** Entry knowledge / local bridge.

**Learning and derivation target:** Define complex arithmetic, conjugation and vector coordinates.

**Implementation and evidence target:** Check identities against explicit real/imaginary calculations.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-2"></span>

### 2.2 Inner products, adjoints, and orthogonality

**Section level:** core. **Required earlier sections:** [2.1](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-1).

**Learning and derivation target:** Derive conjugate symmetry, normalization and orthogonal projection.

**Implementation and evidence target:** Compare hand calculations with tensor conjugation and inner products.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-3"></span>

### 2.3 Linear maps, bases, and changes of coordinates

**Section level:** core. **Required earlier sections:** [2.2](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-2).

**Learning and derivation target:** Derive matrix representations and basis-change rules.

**Implementation and evidence target:** Check the same map in two bases and diagnose an omitted inverse.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-4"></span>

### 2.4 Hermitian, unitary, and positive operators

**Section level:** core. **Required earlier sections:** [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3).

**Learning and derivation target:** State the defining properties and derive elementary consequences for eigenvalues and norms.

**Implementation and evidence target:** Verify residuals and build counterexamples to confusing Hermiticity with unitarity.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-5"></span>

### 2.5 Spectral decomposition and singular values

**Section level:** core. **Required earlier sections:** [2.4](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-4).

**Learning and derivation target:** Derive spectral reconstruction for Hermitian matrices and introduce SVD.

**Implementation and evidence target:** Reconstruct small operators and compare eigenvalue and singular-value diagnostics.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-6"></span>

### 2.6 Functions of matrices and time evolution

**Section level:** core. **Required earlier sections:** [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Learning and derivation target:** Define matrix functions through spectra and series and derive a two-by-two Hermitian example. The Pauli-specific exponential is derived after the Pauli matrices/algebra are introduced in Chapter 3.

**Implementation and evidence target:** Compare independent series, eigendecomposition and matrix-exponential calculations.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-7"></span>

### 2.7 Norms, conditioning, and perturbations

**Section level:** core. **Required earlier sections:** [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Learning and derivation target:** Relate vector/operator norms and explain why a small residual may not imply a small solution error.

**Implementation and evidence target:** Perturb a nearly singular example and report condition-dependent sensitivity.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-8"></span>

### 2.8 Floating-point arithmetic and verification contracts

**Section level:** core. **Required earlier sections:** [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Learning and derivation target:** Explain rounding, absolute/relative tolerances and reproducibility limits.

**Implementation and evidence target:** Design assertions for tiny and order-one values and identify a misleading all-close test.

<span id="ch-single-qubit-states-and-rotations"></span>

## Chapter 3

**Single-Qubit States and Rotations**

**Reading level:** Core. **Entry guidance:** 2; the computational-basis probability postulate is introduced locally.

<span id="sec-single-qubit-states-and-rotations-1"></span>

### 3.1 The pure-state postulate and physical equivalence

**Section level:** core. **Required earlier sections:** [2.2](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-2).

**Learning and derivation target:** State normalization, global-phase equivalence and the computational-basis probability postulate for one qubit; defer general measurement and state-update rules to Chapter 6.

**Implementation and evidence target:** Compare normalized vectors with and without phase alignment.

<span id="sec-single-qubit-states-and-rotations-2"></span>

### 3.2 Relative phase and interference

**Section level:** core. **Required earlier sections:** [3.1](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-1), [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3).

**Learning and derivation target:** Derive how relative phase changes a subsequent measurement after a basis rotation.

**Implementation and evidence target:** Construct states with identical computational-basis probabilities and different interference.

<span id="sec-single-qubit-states-and-rotations-3"></span>

### 3.3 The Bloch-sphere representation

**Section level:** core. **Required earlier sections:** [3.1](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-1), [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3).

**Learning and derivation target:** Introduce the Pauli matrices explicitly, then derive the Bloch coordinates of a pure qubit and their normalization; operator algebra is developed in 3.5.

**Implementation and evidence target:** Recover Bloch coordinates from explicitly defined matrix quadratic forms; the operational expectation-value interpretation is developed in 6.3.

<span id="sec-single-qubit-states-and-rotations-4"></span>

### 3.4 Closed-system evolution and generators

**Section level:** core. **Required earlier sections:** [3.1](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-1), [2.6](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-6).

**Learning and derivation target:** State unitary evolution and connect Hermitian generators to continuous transformations.

**Implementation and evidence target:** Compare generator exponentiation with an explicit unitary.

<span id="sec-single-qubit-states-and-rotations-5"></span>

### 3.5 Pauli algebra and rotation matrices

**Section level:** core. **Required earlier sections:** [3.3](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-3), [3.4](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-4).

**Learning and derivation target:** Derive Pauli products and the three axis-rotation matrices.

**Implementation and evidence target:** Verify matrix formulas, inverse rotations and angle conventions.

<span id="sec-single-qubit-states-and-rotations-6"></span>

### 3.6 Composing rotations

**Section level:** core. **Required earlier sections:** [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5).

**Learning and derivation target:** Explain noncommutativity and parameterize a single-qubit unitary up to phase.

**Implementation and evidence target:** Compare two operation orders and verify a small decomposition.

<span id="sec-single-qubit-states-and-rotations-7"></span>

### 3.7 Physical phase versus numerical equality

**Section level:** core. **Required earlier sections:** [3.1](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-1), [3.6](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-6), [2.8](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-8).

**Learning and derivation target:** Define an appropriate state-comparison criterion and its limitations.

**Implementation and evidence target:** Diagnose tests that reject a harmless global phase or overlook a changed relative phase.

<span id="ch-composite-systems-tensor-products-and-qubit-ordering"></span>

## Chapter 4

**Composite Systems, Tensor Products, and Qubit Ordering**

**Reading level:** Core. **Entry guidance:** 2–3.

<span id="sec-composite-systems-tensor-products-and-qubit-ordering-1"></span>

### 4.1 Tensor-product spaces and basis states

**Section level:** core. **Required earlier sections:** [2.2](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-2), [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3), [3.1](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-1).

**Learning and derivation target:** Construct composite spaces and derive product-state amplitudes.

**Implementation and evidence target:** Compare hand-built products with Kronecker-product references.

<span id="sec-composite-systems-tensor-products-and-qubit-ordering-2"></span>

### 4.2 Registers, labels, and basis indices

**Section level:** core. **Required earlier sections:** [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1).

**Learning and derivation target:** Derive the bit-string-to-index map for the stated most-significant-qubit convention.

**Implementation and evidence target:** Check every basis input for two and three qubits.

<span id="sec-composite-systems-tensor-products-and-qubit-ordering-3"></span>

### 4.3 Local operators on a composite register

**Section level:** core. **Required earlier sections:** [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [3.4](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-4).

**Learning and derivation target:** Derive an operator acting on one selected subsystem.

**Implementation and evidence target:** Compare explicit Kronecker matrices with circuit execution.

<span id="sec-composite-systems-tensor-products-and-qubit-ordering-4"></span>

### 4.4 Multiple-qubit operators and ordered supports

**Section level:** core. **Required earlier sections:** [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2), [4.3](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-3).

**Learning and derivation target:** Specify how operator arguments correspond to tensor axes and basis order.

**Implementation and evidence target:** Test a nonsymmetric two-qubit gate on nonadjacent qubits.

<span id="sec-composite-systems-tensor-products-and-qubit-ordering-5"></span>

### 4.5 Permutations, SWAP, and relabeling

**Section level:** core. **Required earlier sections:** [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2), [4.4](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-4).

**Learning and derivation target:** Distinguish a physical SWAP from changing the description of subsystem labels.

**Implementation and evidence target:** Compare permutation matrices, reshaped arrays and actual SWAP gates.

<span id="sec-composite-systems-tensor-products-and-qubit-ordering-6"></span>

### 4.6 Tensor reshaping as indexed mathematics

**Section level:** core. **Required earlier sections:** [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2), [4.4](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-4).

**Learning and derivation target:** Translate index sums into reshape, permute and contraction operations.

**Implementation and evidence target:** Implement a minimal local-operator reference without a full-register matrix.

<span id="sec-single-qubit-states-and-rotations-8"></span>
<span id="38-the-no-cloning-theorem"></span>

### 4.7 The no-cloning theorem

**Section level:** core. **Required earlier sections:** [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [3.4](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-4).

**Learning and derivation target:** Prove the elementary inner-product argument and state its assumptions.

**Implementation and evidence target:** Contrast copying orthogonal basis states with the failure on a superposition; label the calculation as an illustration.

<span id="sec-composite-systems-tensor-products-and-qubit-ordering-7"></span>
<span id="47-cross-framework-convention-translation"></span>

### 4.8 Cross-framework convention translation

**Section level:** core. **Required earlier sections:** [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2), [4.5](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-5), [4.6](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-6).

**Learning and derivation target:** Explain how an equivalent circuit can have a differently indexed statevector.

**Implementation and evidence target:** Build and verify an explicit permutation between two declared ordering conventions.

<span id="ch-gates-reversible-computation-and-circuit-synthesis"></span>

## Chapter 5

**Gates, Reversible Computation, and Circuit Synthesis**

**Reading level:** Core. **Entry guidance:** 3–4.

<span id="sec-gates-reversible-computation-and-circuit-synthesis-1"></span>

### 5.1 Circuit composition, inversion, and call order

**Section level:** core. **Required earlier sections:** [3.4](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-4), [4.3](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-3).

**Learning and derivation target:** Derive the relation between chronological gate calls and matrix multiplication.

**Implementation and evidence target:** Check a nonsymmetric gate sequence and its inverse.

<span id="sec-gates-reversible-computation-and-circuit-synthesis-2"></span>

### 5.2 Controlled operations and ancillas

**Section level:** core. **Required earlier sections:** [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [4.4](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-4), [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1).

**Learning and derivation target:** Derive controlled-unitary blocks and the role of a clean control/ancilla.

**Implementation and evidence target:** Verify all basis inputs and a superposition control.

<span id="sec-gates-reversible-computation-and-circuit-synthesis-3"></span>

### 5.3 Classical logic made reversible

**Section level:** core. **Required earlier sections:** [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Learning and derivation target:** Construct reversible Boolean maps and identify information discarded by ordinary gates.

**Implementation and evidence target:** Check a small truth table and account for auxiliary outputs.

<span id="sec-gates-reversible-computation-and-circuit-synthesis-4"></span>

### 5.4 Uncomputation and reusable workspace

**Section level:** core. **Required earlier sections:** [5.3](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-3).

**Learning and derivation target:** Derive compute-use-uncompute while retaining a desired result.

**Implementation and evidence target:** Verify restoration of workspace, including a coherent input.

<span id="sec-gates-reversible-computation-and-circuit-synthesis-5"></span>

### 5.5 Universal gate sets

**Section level:** core. **Required earlier sections:** [3.6](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-6), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Learning and derivation target:** State exact versus approximate universality and its computational meaning.

**Implementation and evidence target:** Verify a small exact construction and delimit what a finite demonstration establishes.

<span id="sec-gates-reversible-computation-and-circuit-synthesis-6"></span>

### 5.6 Decomposing controlled and multi-qubit gates

**Section level:** core. **Required earlier sections:** [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2), [5.4](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4).

**Learning and derivation target:** Derive selected decompositions with explicit ancilla assumptions.

**Implementation and evidence target:** Compare complete unitaries and count elementary operations.

<span id="sec-gates-reversible-computation-and-circuit-synthesis-7"></span>

### 5.7 Approximation, synthesis, and precision

**Section level:** core. **Required earlier sections:** [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7), [5.5](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-5).

**Learning and derivation target:** Define a unitary-error criterion and relate synthesis precision to circuit error.

**Implementation and evidence target:** Study a controlled approximation and compare it against an explicit bound.

<span id="sec-gates-reversible-computation-and-circuit-synthesis-8"></span>

### 5.8 Circuit identities and safe transformations

**Section level:** core. **Required earlier sections:** [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Learning and derivation target:** State when cancellation, commuting gates and global-phase transformations preserve the requested result.

**Implementation and evidence target:** Test identities on complete small unitaries and give an invalid rewrite counterexample.

<span id="ch-measurement-expectation-values-and-statistical-estimation"></span>

## Chapter 6

**Measurement, Expectation Values, and Statistical Estimation**

**Reading level:** Core. **Entry guidance:** 2–5; elementary probability is introduced locally before sampling.

<span id="sec-measurement-expectation-values-and-statistical-estimation-1"></span>

### 6.1 Measurement outcomes and the Born rule

**Section level:** core. **Required earlier sections:** [3.1](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-1), [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Learning and derivation target:** State projective measurement probabilities and normalization.

**Implementation and evidence target:** Compute rotated-qubit probabilities independently and expand the existing starter.

<span id="sec-measurement-expectation-values-and-statistical-estimation-2"></span>

### 6.2 Conditional states and ignored outcomes

**Section level:** core. **Required earlier sections:** [6.1](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-1).

**Learning and derivation target:** Derive normalized selective updates for pure global states and ignored-outcome marginal probabilities. Do not average statevectors; the unconditioned density-operator update is derived in Chapter 8.

**Implementation and evidence target:** Enumerate pure-state measurement branches and compare the normalized conditional states and marginal probabilities; return to the operator mixture after Chapter 8.

<span id="sec-measurement-expectation-values-and-statistical-estimation-3"></span>

### 6.3 Observables, spectra, and expectations

**Section level:** core. **Required earlier sections:** [6.1](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-1), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Learning and derivation target:** Derive an expectation as a probability-weighted eigenvalue sum.

**Implementation and evidence target:** Compare spectral, matrix and FlagQuantum evaluations.

<span id="sec-measurement-expectation-values-and-statistical-estimation-4"></span>

### 6.4 Measuring in another basis

**Section level:** core. **Required earlier sections:** [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5), [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1), [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3).

**Learning and derivation target:** Derive the basis rotation needed for X and Y measurements.

**Implementation and evidence target:** Compare rotated computational-basis statistics with exact observable expectations.

<span id="sec-measurement-expectation-values-and-statistical-estimation-5"></span>

### 6.5 Generalized measurements and instruments [Advanced]

**Section level:** advanced. **Required earlier sections:** [6.1](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-1), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [2.4](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-4).

**Learning and derivation target:** Define effects and measurement operators for pure-state inputs; derive probabilities and conditional updates. Full mixed-state instruments and composition belong to 9.7.

**Implementation and evidence target:** Construct two instruments with the same effects and different conditional states.

<span id="sec-measurement-expectation-values-and-statistical-estimation-6"></span>

### 6.6 From exact probabilities to samples

**Section level:** core. **Required earlier sections:** [6.1](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-1).

**Learning and derivation target:** Introduce finite probability spaces, conditional probabilities, expectation and independent trials locally, then derive Bernoulli/categorical sample estimators.

**Implementation and evidence target:** Compare seeded sampling with exact probabilities over repeated trials.

<span id="sec-measurement-expectation-values-and-statistical-estimation-7"></span>

### 6.7 Variance, covariance, and uncertainty

**Section level:** core. **Required earlier sections:** [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3), [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Learning and derivation target:** Derive estimator variance and explain covariance in combined observables.

**Implementation and evidence target:** Check predicted versus empirical variance using independent repetitions.

<span id="sec-measurement-expectation-values-and-statistical-estimation-8"></span>

### 6.8 Confidence intervals and shot budgets

**Section level:** core. **Required earlier sections:** [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Learning and derivation target:** Specify coverage assumptions and derive one usable concentration bound.

**Implementation and evidence target:** Test empirical coverage and shot-count scaling; avoid presenting one favorable run as validation.

<span id="sec-measurement-expectation-values-and-statistical-estimation-9"></span>

### 6.9 Measurement laboratory and failure diagnosis

**Section level:** core. **Required earlier sections:** [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [6.4](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-4), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Learning and derivation target:** Connect probabilities, conditional states, observables and statistical estimates.

**Implementation and evidence target:** Diagnose ordering, normalization and uncertainty-reporting errors in a small complete experiment.

<span id="ch-entanglement-and-quantum-information-protocols"></span>

## Chapter 7

**Entanglement and Quantum Information Protocols**

**Reading level:** Core. **Entry guidance:** 2, 4–6; reduced-density arguments are deferred to 8.

**Bridge:** derive no-signalling through marginal probabilities first; revisit the density-operator argument after Chapter 8.

<span id="sec-entanglement-and-quantum-information-protocols-1"></span>

### 7.1 Product states and entangled states

**Section level:** core. **Required earlier sections:** [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1).

**Learning and derivation target:** Define pure-state separability and show why local amplitudes are insufficient in general.

**Implementation and evidence target:** Compare explicit coefficient matrices of product and Bell states.

<span id="sec-entanglement-and-quantum-information-protocols-2"></span>

### 7.2 Schmidt decomposition

**Section level:** core. **Required earlier sections:** [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5), [7.1](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-1).

**Learning and derivation target:** Derive the bipartite decomposition by SVD and identify Schmidt rank.

**Implementation and evidence target:** Reconstruct a state and verify its coefficients; revisit reduced spectra in Chapter 8.

<span id="sec-entanglement-and-quantum-information-protocols-3"></span>

### 7.3 Bell states and basis changes

**Section level:** core. **Required earlier sections:** [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [7.1](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-1).

**Learning and derivation target:** Derive preparation and measurement in the Bell basis.

**Implementation and evidence target:** Check all four basis states and a general superposition.

<span id="sec-entanglement-and-quantum-information-protocols-4"></span>

### 7.4 Correlations and the CHSH experiment

**Section level:** core. **Required earlier sections:** [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7), [7.3](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-3).

**Learning and derivation target:** Derive a classical bound under explicit assumptions and calculate a quantum example.

**Implementation and evidence target:** Compare the exact correlators and finite-sample estimates without implying a loophole-free hardware test.

<span id="sec-entanglement-and-quantum-information-protocols-5"></span>

### 7.5 Teleportation, branch by branch

**Section level:** core. **Required earlier sections:** [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [7.3](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-3).

**Learning and derivation target:** Derive all four conditional receiver states and their corrections.

**Implementation and evidence target:** Verify each branch for several general complex inputs.

<span id="sec-entanglement-and-quantum-information-protocols-6"></span>

### 7.6 Superdense coding

**Section level:** core. **Required earlier sections:** [7.3](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-3), [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1).

**Learning and derivation target:** Derive message encoding and decoding and count the required shared resources.

**Implementation and evidence target:** Check every message and report entanglement and communication requirements.

<span id="sec-entanglement-and-quantum-information-protocols-7"></span>

### 7.7 No-signalling and classical communication

**Section level:** core. **Required earlier sections:** [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [7.3](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-3).

**Learning and derivation target:** Derive unchanged remote marginal probabilities when local outcomes are ignored.

**Implementation and evidence target:** Compare conditioned and unconditioned statistics; connect the density-matrix proof to Chapter 8.

<span id="sec-network-entanglement-primitives"></span>

### 7.8 Entanglement swapping and quantum-network primitives

**Section level:** core. **Required earlier sections:** [7.3](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-3), [7.5](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-5), [7.7](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-7).

**Learning and derivation target:** Derive entanglement swapping from Bell measurement and distinguish classical messages, distributed entanglement and quantum-state transfer. Mixed-state distillation is developed in Chapter 12.

**Implementation and evidence target:** Enumerate all branches of a tiny swapping protocol, track classical corrections and state explicitly which quantum links are assumed.

<span id="sec-entanglement-and-quantum-information-protocols-8"></span>
<span id="78-what-entanglement-alone-does-not-guarantee"></span>

### 7.9 What entanglement alone does not guarantee

**Section level:** core. **Required earlier sections:** [7.5](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-5), [7.6](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-6), [7.7](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-7), [7.8](../section-plans/01-foundations.md#sec-network-entanglement-primitives).

**Learning and derivation target:** Distinguish correlation, communication and a usable computational protocol.

**Implementation and evidence target:** Analyze a failed protocol proposal and identify its missing assumption or resource.

<span id="ch-density-matrices-reduced-states-and-purification"></span>

## Chapter 8

**Density Matrices, Reduced States, and Purification**

**Reading level:** Core. **Entry guidance:** 2, 4, 6; selected 7.2 for reduced Schmidt spectra.

<span id="sec-density-matrices-reduced-states-and-purification-1"></span>

### 8.1 Statistical ensembles and density operators

**Section level:** core. **Required earlier sections:** [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3), [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Learning and derivation target:** Derive the density matrix of a mixture and its basic properties.

**Implementation and evidence target:** Compare different ensembles that produce the same operator.

<span id="sec-density-matrices-reduced-states-and-purification-2"></span>

### 8.2 Pure states, mixed states, and purity

**Section level:** core. **Required earlier sections:** [8.1](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-1), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Learning and derivation target:** Derive spectral and purity criteria and their assumptions.

**Implementation and evidence target:** Check pure, mixed and deliberately nonphysical matrices.

<span id="sec-density-matrices-reduced-states-and-purification-3"></span>

### 8.3 Expectation values and measurement updates

**Section level:** core. **Required earlier sections:** [8.1](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-1), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3).

**Learning and derivation target:** Derive trace expressions for observables and measurement branches.

**Implementation and evidence target:** Verify equivalence with pure-state formulas and ensemble averaging.

<span id="sec-density-matrices-reduced-states-and-purification-4"></span>

### 8.4 Partial trace from operational consistency

**Section level:** core. **Required earlier sections:** [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [8.3](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-3).

**Learning and derivation target:** Derive the subsystem operator that reproduces every local expectation.

**Implementation and evidence target:** Compare explicit index sums with a tensor implementation.

<span id="sec-density-matrices-reduced-states-and-purification-5"></span>

### 8.5 Reduced states of entangled systems

**Section level:** core. **Required earlier sections:** [7.2](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-2), [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4).

**Learning and derivation target:** Relate reduced spectra to Schmidt coefficients.

**Implementation and evidence target:** Check Bell and nonmaximally entangled examples without confusing mixedness with classical preparation.

<span id="sec-density-matrices-reduced-states-and-purification-6"></span>

### 8.6 Purification and nonuniqueness

**Section level:** core. **Required earlier sections:** [8.2](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2), [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4).

**Learning and derivation target:** Construct a purification from a spectral decomposition and explain freedom in its environment.

**Implementation and evidence target:** Trace out independently constructed purifications and compare the recovered state.

<span id="sec-density-matrices-reduced-states-and-purification-7"></span>

### 8.7 Proper and improper mixtures

**Section level:** core. **Required earlier sections:** [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4), [8.6](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-6).

**Learning and derivation target:** Explain what local statistics establish and how joint access can distinguish preparations.

**Implementation and evidence target:** Compare globally different preparations with identical local states.

<span id="sec-density-matrices-reduced-states-and-purification-8"></span>

### 8.8 Density-operator verification laboratory

**Section level:** core. **Required earlier sections:** [8.2](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2), [8.3](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-3), [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4), [8.5](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-5), [2.8](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-8).

**Learning and derivation target:** State physicality checks, numerical tolerances and comparison criteria.

**Implementation and evidence target:** Diagnose positivity, trace, basis-order and partial-trace implementation errors.
