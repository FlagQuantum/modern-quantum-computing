# Result and proof plan: Foundations and Quantum Information Primitives

[Depth definitions](../proof-plan.md#proof-depth-contract) · [Source catalogue](../references/proof-sources.md) · [Volume plan](../volume-plan.md)

Authoring specifications only. No result/proof/API is certified by this plan. F/M/R have different scope; imported results are the exact prerequisite sections linked below.

## Chapter 1: What Quantum Computing Computes

<span id="sec-what-quantum-computing-computes-1"></span>

### 1.1 Problems, inputs, and observable outputs

**Core result / role:** Computational-task specification.

**Assumptions and scope:** Declared input, output and success criterion.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Distinguish a problem instance from its representation and requested observation.

**Imported earlier results:** Entry knowledge / locally supplied bridge.

**Exact source targets:** [NC:3.2.1](../references/proof-sources.md#source-nc-3-2-1): Section 3.2.1 How to quantify computational resources.

**Independent evidence target:** Specify input size, requested output and success criterion for a tiny task.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-what-quantum-computing-computes-2"></span>

### 1.2 A first interference experiment

**Core result / role:** Two-path interference calculation (preview).

**Assumptions and scope:** Supplied normalized amplitudes and measurement rule.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Multiply the two-by-two matrices; expose the cross term; defer formal postulates.

**Imported earlier results:** [1.1](../section-plans/01-foundations.md#sec-what-quantum-computing-computes-1).

**Exact source targets:** [NC:1.3.1](../references/proof-sources.md#source-nc-1-3-1): Section 1.3.1 Single qubit gates.

**Independent evidence target:** Compare a hand calculation, a two-by-two matrix reference and a small FlagQuantum circuit.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-what-quantum-computing-computes-3"></span>

### 1.3 What a quantum state describes

**Core result / role:** State descriptions do not equal observed samples.

**Assumptions and scope:** Finite measurement alphabet.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Separate amplitude coordinates, probabilities and a single random outcome.

**Imported earlier results:** [1.2](../section-plans/01-foundations.md#sec-what-quantum-computing-computes-2).

**Exact source targets:** [NC:1.2](../references/proof-sources.md#source-nc-1-2): Section 1.2 Quantum bits.

**Independent evidence target:** Contrast full simulated amplitudes with the information available from repeated measurements.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-what-quantum-computing-computes-4"></span>

### 1.4 Algorithms, simulators, and physical devices

**Core result / role:** Mathematical, simulated and experimental evidence.

**Assumptions and scope:** Explicit evidence provenance.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Classify claims by their source and specify a falsifiable check.

**Imported earlier results:** [1.1](../section-plans/01-foundations.md#sec-what-quantum-computing-computes-1).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Annotate which parts of the opening calculation are mathematical, simulated or measured.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-what-quantum-computing-computes-5"></span>

### 1.5 What computational advantage would require

**Core result / role:** End-to-end advantage is a comparison contract.

**Assumptions and scope:** Same task, access, accuracy and success target.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Account for preparation, execution and output costs; make no separation theorem.

**Imported earlier results:** [1.4](../section-plans/01-foundations.md#sec-what-quantum-computing-computes-4).

**Exact source targets:** [NC:3.2.1](../references/proof-sources.md#source-nc-3-2-1): Section 3.2.1 How to quantify computational resources.

**Independent evidence target:** Diagnose an invalid speedup claim based on simulator wall time or free data loading.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-what-quantum-computing-computes-6"></span>

### 1.6 A map of the learning routes

**Core result / role:** Prerequisite-closed reading paths.

**Assumptions and scope:** Canonical section dependency graph.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Explain entry, optional branches and exit checks without a quantum theorem.

**Imported earlier results:** [1.4](../section-plans/01-foundations.md#sec-what-quantum-computing-computes-4).

**Exact source targets:** [ED:routes](../references/proof-sources.md#source-ed-routes): Checked prerequisite paths.

**Independent evidence target:** Choose an introductory route and complete a notation/background diagnostic.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 2: Complex Vectors, Operators, and Numerical Reasoning

<span id="sec-complex-vectors-operators-and-numerical-reasoning-1"></span>

### 2.1 Complex scalars, vectors, and conjugation

**Core result / role:** Complex-coordinate and conjugation identities.

**Assumptions and scope:** Finite complex vectors.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive conjugation and modulus identities component by component.

**Imported earlier results:** Entry knowledge / locally supplied bridge.

**Exact source targets:** [NC:2.1.1](../references/proof-sources.md#source-nc-2-1-1): Section 2.1.1 Bases and linear independence.

**Independent evidence target:** Check identities against explicit real/imaginary calculations.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-2"></span>

### 2.2 Inner products, adjoints, and orthogonality

**Core result / role:** Cauchy-Schwarz and orthogonal projection.

**Assumptions and scope:** Positive-definite inner product.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Use a nonnegative squared norm; derive projection and equality conditions.

**Imported earlier results:** [2.1](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-1).

**Exact source targets:** [NC:2.1.4](../references/proof-sources.md#source-nc-2-1-4): Section 2.1.4 Inner products.

**Independent evidence target:** Compare hand calculations with tensor conjugation and inner products.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-3"></span>

### 2.3 Linear maps, bases, and changes of coordinates

**Core result / role:** Similarity under a change of basis.

**Assumptions and scope:** Invertible coordinate map; unitary map for orthonormal bases.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the coordinate transformation and distinguish active from passive maps.

**Imported earlier results:** [2.2](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-2).

**Exact source targets:** [NC:2.1.2](../references/proof-sources.md#source-nc-2-1-2): Section 2.1.2 Linear operators and matrices.

**Independent evidence target:** Check the same map in two bases and diagnose an omitted inverse.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-4"></span>

### 2.4 Hermitian, unitary, and positive operators

**Core result / role:** Hermitian positivity and unitary norm preservation.

**Assumptions and scope:** Finite-dimensional operators.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove real Hermitian eigenvalues, the quadratic-form condition and norm preservation.

**Imported earlier results:** [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3).

**Exact source targets:** [NC:2.1.6](../references/proof-sources.md#source-nc-2-1-6): Section 2.1.6 Adjoints and Hermitian operators.

**Independent evidence target:** Verify residuals and build counterexamples to confusing Hermiticity with unitarity.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-5"></span>

### 2.5 Spectral decomposition and singular values

**Core result / role:** Spectral theorem and singular-value decomposition.

**Assumptions and scope:** Finite Hermitian matrix; arbitrary rectangular complex matrix.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove Hermitian diagonalization; construct SVD from the positive Gram operator, including its kernel.

**Imported earlier results:** [2.4](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-4).

**Exact source targets:** [NC:2.1.5](../references/proof-sources.md#source-nc-2-1-5): Section 2.1.5 Eigenvectors and eigenvalues; [NC:2.1.10](../references/proof-sources.md#source-nc-2-1-10): Section 2.1.10 The polar and singular value decompositions.

**Independent evidence target:** Reconstruct small operators and compare eigenvalue and singular-value diagnostics.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-6"></span>

### 2.6 Functions of matrices and time evolution

**Core result / role:** Spectral functional calculus and exponential unitarity.

**Assumptions and scope:** Hermitian generator; convergent finite-matrix exponential.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Define the function on eigenvalues; prove composition and unitary evolution.

**Imported earlier results:** [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Exact source targets:** [NC:2.1.8](../references/proof-sources.md#source-nc-2-1-8): Section 2.1.8 Operator functions.

**Independent evidence target:** Compare independent series, eigendecomposition and matrix-exponential calculations.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-7"></span>

### 2.7 Norms, conditioning, and perturbations

**Core result / role:** Submultiplicativity and condition-number error amplification.

**Assumptions and scope:** Induced norm; invertible linear system.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Bound matrix-vector perturbations and exhibit an ill-conditioned counterexample.

**Imported earlier results:** [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Exact source targets:** [TQI:1.1.3](../references/proof-sources.md#source-tqi-1-1-3): Section 1.1.3 Operator decompositions and norms.

**Independent evidence target:** Perturb a nearly singular example and report condition-dependent sensitivity.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-8"></span>

### 2.8 Floating-point arithmetic and verification contracts

**Core result / role:** Residual, absolute tolerance and relative tolerance contracts.

**Assumptions and scope:** Declared floating-point dtype and scaling.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Separate conditioning from rounding; derive a small residual-versus-error example.

**Imported earlier results:** [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Exact source targets:** [NC:2.1.2](../references/proof-sources.md#source-nc-2-1-2): Section 2.1.2 Linear operators and matrices; [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Design assertions for tiny and order-one values and identify a misleading all-close test.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 3: Single-Qubit States and Rotations

<span id="sec-single-qubit-states-and-rotations-1"></span>

### 3.1 The pure-state postulate and physical equivalence

**Core result / role:** Pure-state and Born-probability postulates.

**Assumptions and scope:** Normalized vector; fixed computational basis.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** State the postulates; derive normalization and global-phase invariance of probabilities.

**Imported earlier results:** [2.2](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-2).

**Exact source targets:** [NC:2.2.1](../references/proof-sources.md#source-nc-2-2-1): Section 2.2.1 State space; [NC:2.2.3](../references/proof-sources.md#source-nc-2-2-3): Section 2.2.3 Quantum measurement.

**Independent evidence target:** Compare normalized vectors with and without phase alignment.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-single-qubit-states-and-rotations-2"></span>

### 3.2 Relative phase and interference

**Core result / role:** Interference depends on relative phase.

**Assumptions and scope:** Two coherent amplitudes in a specified basis.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Expand the output probability and isolate its phase-dependent cross term.

**Imported earlier results:** [3.1](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-1), [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3).

**Exact source targets:** [NC:2.2.7](../references/proof-sources.md#source-nc-2-2-7): Section 2.2.7 Phase.

**Independent evidence target:** Construct states with identical computational-basis probabilities and different interference.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-single-qubit-states-and-rotations-3"></span>

### 3.3 The Bloch-sphere representation

**Core result / role:** Pure-qubit Bloch-sphere parametrization.

**Assumptions and scope:** Normalized two-component state modulo global phase.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Introduce Pauli matrices; derive the spherical coordinates and expectation components.

**Imported earlier results:** [3.1](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-1), [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3).

**Exact source targets:** [NC:1.2](../references/proof-sources.md#source-nc-1-2): Section 1.2 Quantum bits; [NC:2.1.3](../references/proof-sources.md#source-nc-2-1-3): Section 2.1.3 The Pauli matrices.

**Independent evidence target:** Recover Bloch coordinates from explicitly defined matrix quadratic forms; the operational expectation-value interpretation is developed in 6.3.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-single-qubit-states-and-rotations-4"></span>

### 3.4 Closed-system evolution and generators

**Core result / role:** Closed-system evolution and Hermitian generators.

**Assumptions and scope:** Differentiable finite closed-system dynamics.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Adopt unitary evolution; derive generator Hermiticity and the Schrödinger equation for a fixed generator.

**Imported earlier results:** [3.1](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-1), [2.6](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-6).

**Exact source targets:** [NC:2.2.2](../references/proof-sources.md#source-nc-2-2-2): Section 2.2.2 Evolution.

**Independent evidence target:** Compare generator exponentiation with an explicit unitary.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-single-qubit-states-and-rotations-5"></span>

### 3.5 Pauli algebra and rotation matrices

**Core result / role:** Pauli multiplication and rotation exponential.

**Assumptions and scope:** Pauli generator with square equal to identity.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Split the power series into even and odd terms; derive the half-angle convention.

**Imported earlier results:** [3.3](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-3), [3.4](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-4).

**Exact source targets:** [NC:2.1.3](../references/proof-sources.md#source-nc-2-1-3): Section 2.1.3 The Pauli matrices; [NC:4.2](../references/proof-sources.md#source-nc-4-2): Section 4.2 Single qubit operations.

**Independent evidence target:** Verify matrix formulas, inverse rotations and angle conventions.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-single-qubit-states-and-rotations-6"></span>

### 3.6 Composing rotations

**Core result / role:** Rotation composition and Euler parametrization.

**Assumptions and scope:** Single-qubit unitary; global phase explicitly tracked.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Multiply rotations; derive a selected Euler factorization and singular parameter cases.

**Imported earlier results:** [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5).

**Exact source targets:** [NC:4.2](../references/proof-sources.md#source-nc-4-2): Section 4.2 Single qubit operations.

**Independent evidence target:** Compare two operation orders and verify a small decomposition.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-single-qubit-states-and-rotations-7"></span>

### 3.7 Physical phase versus numerical equality

**Core result / role:** Global phase becomes relative in controlled contexts.

**Assumptions and scope:** Comparison of a unitary and its controlled extension.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove ray equivalence on an isolated register and exhibit a controlled-phase counterexample.

**Imported earlier results:** [3.1](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-1), [3.6](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-6), [2.8](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-8).

**Exact source targets:** [NC:2.2.7](../references/proof-sources.md#source-nc-2-2-7): Section 2.2.7 Phase; [NC:4.3](../references/proof-sources.md#source-nc-4-3): Section 4.3 Controlled operations.

**Independent evidence target:** Diagnose tests that reject a harmless global phase or overlook a changed relative phase.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 4: Composite Systems, Tensor Products, and Qubit Ordering

<span id="sec-composite-systems-tensor-products-and-qubit-ordering-1"></span>

### 4.1 Tensor-product spaces and basis states

**Core result / role:** Tensor-product dimension and product-basis orthonormality.

**Assumptions and scope:** Finite subsystem spaces with ordered bases.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Construct the product basis; prove its inner products and dimension.

**Imported earlier results:** [2.2](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-2), [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3), [3.1](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-1).

**Exact source targets:** [NC:2.1.7](../references/proof-sources.md#source-nc-2-1-7): Section 2.1.7 Tensor products.

**Independent evidence target:** Compare hand-built products with Kronecker-product references.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-composite-systems-tensor-products-and-qubit-ordering-2"></span>

### 4.2 Registers, labels, and basis indices

**Core result / role:** Bijection between bit tuples and statevector indices.

**Assumptions and scope:** Declared significance and qubit-label order.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the index map and inverse; include a non-palindromic bit pattern.

**Imported earlier results:** [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1).

**Exact source targets:** [NC:2.1.7](../references/proof-sources.md#source-nc-2-1-7): Section 2.1.7 Tensor products.

**Independent evidence target:** Check every basis input for two and three qubits.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-composite-systems-tensor-products-and-qubit-ordering-3"></span>

### 4.3 Local operators on a composite register

**Core result / role:** Local operator embedding.

**Assumptions and scope:** Specified tensor factor and basis order.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the Kronecker embedding on each product-basis vector.

**Imported earlier results:** [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [3.4](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-4).

**Exact source targets:** [NC:2.1.7](../references/proof-sources.md#source-nc-2-1-7): Section 2.1.7 Tensor products.

**Independent evidence target:** Compare explicit Kronecker matrices with circuit execution.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-composite-systems-tensor-products-and-qubit-ordering-4"></span>

### 4.4 Multiple-qubit operators and ordered supports

**Core result / role:** Ordered-support multi-qubit action.

**Assumptions and scope:** Distinct support labels and explicit local basis.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the sum over local input indices; separate support order from sorted labels.

**Imported earlier results:** [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2), [4.3](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-3).

**Exact source targets:** [NC:2.1.7](../references/proof-sources.md#source-nc-2-1-7): Section 2.1.7 Tensor products; [NC:4.3](../references/proof-sources.md#source-nc-4-3): Section 4.3 Controlled operations.

**Independent evidence target:** Test a nonsymmetric two-qubit gate on nonadjacent qubits.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-composite-systems-tensor-products-and-qubit-ordering-5"></span>

### 4.5 Permutations, SWAP, and relabeling

**Core result / role:** Permutation conjugation and physical SWAP.

**Assumptions and scope:** Bijective subsystem permutation.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove how states and operators transform; distinguish relabeling from an executed gate.

**Imported earlier results:** [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2), [4.4](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-4).

**Exact source targets:** [NC:4.3](../references/proof-sources.md#source-nc-4-3): Section 4.3 Controlled operations.

**Independent evidence target:** Compare permutation matrices, reshaped arrays and actual SWAP gates.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-composite-systems-tensor-products-and-qubit-ordering-6"></span>

### 4.6 Tensor reshaping as indexed mathematics

**Core result / role:** Reshape-transpose-contraction equals indexed gate action.

**Assumptions and scope:** Fixed tensor-axis convention.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Expand the contraction and identify the same basis-index update.

**Imported earlier results:** [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2), [4.4](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-4).

**Exact source targets:** [NC:2.1.7](../references/proof-sources.md#source-nc-2-1-7): Section 2.1.7 Tensor products.

**Independent evidence target:** Implement a minimal local-operator reference without a full-register matrix.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-single-qubit-states-and-rotations-8"></span>

### 4.7 The no-cloning theorem

**Core result / role:** No-cloning theorem.

**Assumptions and scope:** One fixed linear unitary; arbitrary unknown pure input; fixed blank.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Preserve inner products for two inputs; show only identical or orthogonal states evade contradiction.

**Imported earlier results:** [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [3.4](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-4).

**Exact source targets:** [NC:1.3.5](../references/proof-sources.md#source-nc-1-3-5): Section 1.3.5 Qubit copying circuit?.

**Independent evidence target:** Contrast copying orthogonal basis states with the failure on a superposition; label the calculation as an illustration.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-composite-systems-tensor-products-and-qubit-ordering-7"></span>

### 4.8 Cross-framework convention translation

**Core result / role:** Convention translation preserves physical predictions.

**Assumptions and scope:** Explicit basis permutation in both frameworks.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Conjugate states, operators and measurement labels consistently; test a changed ordering.

**Imported earlier results:** [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2), [4.5](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-5), [4.6](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-6).

**Exact source targets:** [NC:2.1.7](../references/proof-sources.md#source-nc-2-1-7): Section 2.1.7 Tensor products; [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Build and verify an explicit permutation between two declared ordering conventions.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 5: Gates, Reversible Computation, and Circuit Synthesis

<span id="sec-gates-reversible-computation-and-circuit-synthesis-1"></span>

### 5.1 Circuit composition, inversion, and call order

**Core result / role:** Circuit inversion reverses gate order.

**Assumptions and scope:** Finite product of unitary gates.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove the inverse-product identity and connect algebraic order to execution order.

**Imported earlier results:** [3.4](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-4), [4.3](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-3).

**Exact source targets:** [NC:4.1](../references/proof-sources.md#source-nc-4-1): Section 4.1 Quantum algorithms.

**Independent evidence target:** Check a nonsymmetric gate sequence and its inverse.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-gates-reversible-computation-and-circuit-synthesis-2"></span>

### 5.2 Controlled operations and ancillas

**Core result / role:** Controlled-unitary block form and ancilla contracts.

**Assumptions and scope:** Orthogonal control projectors; specified ancillary input.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove unitarity and derive action on a control superposition.

**Imported earlier results:** [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [4.4](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-4), [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1).

**Exact source targets:** [NC:4.3](../references/proof-sources.md#source-nc-4-3): Section 4.3 Controlled operations.

**Independent evidence target:** Verify all basis inputs and a superposition control.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-gates-reversible-computation-and-circuit-synthesis-3"></span>

### 5.3 Classical logic made reversible

**Core result / role:** Reversible embedding of a Boolean function.

**Assumptions and scope:** Finite deterministic function; XOR target register.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove the embedding is bijective and self-inverse for the declared oracle.

**Imported earlier results:** [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Exact source targets:** [NC:3.1.2](../references/proof-sources.md#source-nc-3-1-2): Section 3.1.2 Circuits.

**Independent evidence target:** Check a small truth table and account for auxiliary outputs.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-gates-reversible-computation-and-circuit-synthesis-4"></span>

### 5.4 Uncomputation and reusable workspace

**Core result / role:** Compute-copy-uncompute cleans workspace.

**Assumptions and scope:** Coherent reversible computation; orthogonal output encoding.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Track all registers and show why copying basis information does not clone unknown states.

**Imported earlier results:** [5.3](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-3).

**Exact source targets:** [NC:3.2.5](../references/proof-sources.md#source-nc-3-2-5): Section 3.2.5 Energy and computation.

**Independent evidence target:** Verify restoration of workspace, including a coherent input.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-gates-reversible-computation-and-circuit-synthesis-5"></span>

### 5.5 Universal gate sets

**Core result / role:** Single-qubit gates and CNOT are universal.

**Assumptions and scope:** Arbitrary finite unitary; exact continuous one-qubit gates.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Give the two-level decomposition and reduce each two-level unitary to the allowed gates.

**Imported earlier results:** [3.6](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-6), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Exact source targets:** [NC:4.5.1](../references/proof-sources.md#source-nc-4-5-1): Section 4.5.1 Two-level unitary gates are universal; [NC:4.5.2](../references/proof-sources.md#source-nc-4-5-2): Section 4.5.2 Single qubit and CNOT gates are universal.

**Independent evidence target:** Verify a small exact construction and delimit what a finite demonstration establishes.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-gates-reversible-computation-and-circuit-synthesis-6"></span>

### 5.6 Decomposing controlled and multi-qubit gates

**Core result / role:** Selected controlled-gate and Toffoli decomposition.

**Assumptions and scope:** Chosen elementary basis; declared clean/dirty ancillas.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove each selected identity on all basis inputs and extend by linearity.

**Imported earlier results:** [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2), [5.4](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4).

**Exact source targets:** [NC:4.3](../references/proof-sources.md#source-nc-4-3): Section 4.3 Controlled operations; [SYNTH:gates](../references/proof-sources.md#source-synth-gates): Sections 5-6: two-bit and three-bit networks; selected controlled gates.

**Independent evidence target:** Compare complete unitaries and count elementary operations.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-gates-reversible-computation-and-circuit-synthesis-7"></span>

### 5.7 Approximation, synthesis, and precision

**Core result / role:** Solovay-Kitaev approximation theorem (scoped).

**Assumptions and scope:** Fixed inverse-closed dense gate set; operator norm; fixed dimension.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** State the theorem and commutator-recursion roadmap; defer technical approximation lemmas to Appendix 3.

**Imported earlier results:** [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7), [5.5](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-5).

**Exact source targets:** [NC:A3](../references/proof-sources.md#source-nc-a3): Appendix 3: The Solovay-Kitaev theorem.

**Independent evidence target:** Study a controlled approximation and compare it against an explicit bound.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local advanced bridge to supply:** Inverse-closed dense gates; operator norm; SU(d), commutators and recursive accuracy vocabulary.

**Explicitly deferred proof ingredients:** General balanced-commutator construction, base-net existence and recursion constants; NC Appendix 3.

<span id="sec-gates-reversible-computation-and-circuit-synthesis-8"></span>

### 5.8 Circuit identities and safe transformations

**Core result / role:** Gate cancellation and commutation under explicit conditions.

**Assumptions and scope:** Same support and parameter conventions; commuting generators where invoked.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove a minimal rewrite set and give a noncommuting counterexample.

**Imported earlier results:** [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Exact source targets:** [NC:4.2](../references/proof-sources.md#source-nc-4-2): Section 4.2 Single qubit operations; [NC:4.3](../references/proof-sources.md#source-nc-4-3): Section 4.3 Controlled operations.

**Independent evidence target:** Test identities on complete small unitaries and give an invalid rewrite counterexample.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 6: Measurement, Expectation Values, and Statistical Estimation

<span id="sec-measurement-expectation-values-and-statistical-estimation-1"></span>

### 6.1 Measurement outcomes and the Born rule

**Core result / role:** Projective Born rule and normalization.

**Assumptions and scope:** Orthogonal complete projectors; normalized input.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** State the rule; derive nonnegative probabilities summing to one.

**Imported earlier results:** [3.1](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-1), [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Exact source targets:** [NC:2.2.5](../references/proof-sources.md#source-nc-2-2-5): Section 2.2.5 Projective measurements.

**Independent evidence target:** Compute rotated-qubit probabilities independently and expand the existing starter.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-measurement-expectation-values-and-statistical-estimation-2"></span>

### 6.2 Conditional states and ignored outcomes

**Core result / role:** Selective update and marginal probabilities.

**Assumptions and scope:** Pure global input; nonzero selected outcome probability.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Normalize each projected branch; sum probabilities without averaging statevectors.

**Imported earlier results:** [6.1](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-1).

**Exact source targets:** [NC:2.2.3](../references/proof-sources.md#source-nc-2-2-3): Section 2.2.3 Quantum measurement.

**Independent evidence target:** Enumerate pure-state measurement branches and compare the normalized conditional states and marginal probabilities; return to the operator mixture after Chapter 8.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-measurement-expectation-values-and-statistical-estimation-3"></span>

### 6.3 Observables, spectra, and expectations

**Core result / role:** Spectral expectation identity.

**Assumptions and scope:** Hermitian observable and projective spectral measurement.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the probability-weighted eigenvalue sum and its inner-product form.

**Imported earlier results:** [6.1](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-1), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Exact source targets:** [NC:2.2.5](../references/proof-sources.md#source-nc-2-2-5): Section 2.2.5 Projective measurements.

**Independent evidence target:** Compare spectral, matrix and FlagQuantum evaluations.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-measurement-expectation-values-and-statistical-estimation-4"></span>

### 6.4 Measuring in another basis

**Core result / role:** Measurement after basis rotation.

**Assumptions and scope:** Unitary basis change and specified measurement convention.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Conjugate the measured projector; derive the X and Y basis circuits.

**Imported earlier results:** [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5), [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1), [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3).

**Exact source targets:** [NC:1.3.3](../references/proof-sources.md#source-nc-1-3-3): Section 1.3.3 Measurements in bases other than the computational basis.

**Independent evidence target:** Compare rotated computational-basis statistics with exact observable expectations.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-measurement-expectation-values-and-statistical-estimation-5"></span>

### 6.5 Generalized measurements and instruments [Advanced]

**Core result / role:** POVM normalization and conditional measurement-operator rule.

**Assumptions and scope:** Positive effects summing to identity; declared measurement operators.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Distinguish effects from state updates; derive the pure-input probability/update consistency.

**Imported earlier results:** [6.1](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-1), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [2.4](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-4).

**Exact source targets:** [NC:2.2.3](../references/proof-sources.md#source-nc-2-2-3): Section 2.2.3 Quantum measurement; [NC:2.2.6](../references/proof-sources.md#source-nc-2-2-6): Section 2.2.6 POVM measurements.

**Independent evidence target:** Construct two instruments with the same effects and different conditional states.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-measurement-expectation-values-and-statistical-estimation-6"></span>

### 6.6 From exact probabilities to samples

**Core result / role:** Unbiased Bernoulli and categorical estimators.

**Assumptions and scope:** Independent identically distributed finite trials.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Introduce conditional probability and expectation; prove estimator means explicitly.

**Imported earlier results:** [6.1](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-1).

**Exact source targets:** [NC:A1](../references/proof-sources.md#source-nc-a1): Appendix 1: Notes on basic probability theory.

**Independent evidence target:** Compare seeded sampling with exact probabilities over repeated trials.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-measurement-expectation-values-and-statistical-estimation-7"></span>

### 6.7 Variance, covariance, and uncertainty

**Core result / role:** Variance of a weighted estimator.

**Assumptions and scope:** Finite second moments; stated inter-sample independence.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Expand covariance terms; show when independent-group variances add.

**Imported earlier results:** [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3), [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Exact source targets:** [NC:A1](../references/proof-sources.md#source-nc-a1): Appendix 1: Notes on basic probability theory.

**Independent evidence target:** Check predicted versus empirical variance using independent repetitions.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-measurement-expectation-values-and-statistical-estimation-8"></span>

### 6.8 Confidence intervals and shot budgets

**Core result / role:** Chebyshev coverage and a conservative shot bound.

**Assumptions and scope:** Independent bounded outcomes; finite variance; fixed confidence target.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove Markov then Chebyshev; solve the resulting shot inequality and distinguish it from exact binomial coverage.

**Imported earlier results:** [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Exact source targets:** [CVX:7.4](../references/proof-sources.md#source-cvx-7-4): Section 7.4 Chebyshev and Chernoff bounds.

**Independent evidence target:** Test empirical coverage and shot-count scaling; avoid presenting one favorable run as validation.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-measurement-expectation-values-and-statistical-estimation-9"></span>

### 6.9 Measurement laboratory and failure diagnosis

**Core result / role:** Measurement acceptance protocol.

**Assumptions and scope:** Earlier postulates and statistical assumptions.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Reuse 6.1–6.8; require branch, basis and uncertainty checks plus a deliberate failure.

**Imported earlier results:** [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [6.4](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-4), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Diagnose ordering, normalization and uncertainty-reporting errors in a small complete experiment.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 7: Entanglement and Quantum Information Protocols

<span id="sec-entanglement-and-quantum-information-protocols-1"></span>

### 7.1 Product states and entangled states

**Core result / role:** Pure-state separability is rank one.

**Assumptions and scope:** Bipartite pure state and fixed coefficient matrix.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove product form if and only if coefficient rank is one.

**Imported earlier results:** [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1).

**Exact source targets:** [NC:2.5](../references/proof-sources.md#source-nc-2-5): Section 2.5 The Schmidt decomposition and puriﬁcations.

**Independent evidence target:** Compare explicit coefficient matrices of product and Bell states.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-entanglement-and-quantum-information-protocols-2"></span>

### 7.2 Schmidt decomposition

**Core result / role:** Schmidt decomposition and Schmidt-rank invariance.

**Assumptions and scope:** Finite bipartite pure state.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Apply SVD to the coefficient matrix; prove normalization and local-unitary invariance.

**Imported earlier results:** [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5), [7.1](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-1).

**Exact source targets:** [NC:2.5](../references/proof-sources.md#source-nc-2-5): Section 2.5 The Schmidt decomposition and puriﬁcations.

**Independent evidence target:** Reconstruct a state and verify its coefficients; revisit reduced spectra in Chapter 8.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-entanglement-and-quantum-information-protocols-3"></span>

### 7.3 Bell states and basis changes

**Core result / role:** Bell-basis orthonormality and preparation.

**Assumptions and scope:** Two qubits; fixed Bell phase conventions.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive all four vectors and the preparation/analysis inverse.

**Imported earlier results:** [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [7.1](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-1).

**Exact source targets:** [NC:1.3.6](../references/proof-sources.md#source-nc-1-3-6): Section 1.3.6 Example: Bell states.

**Independent evidence target:** Check all four basis states and a general superposition.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-entanglement-and-quantum-information-protocols-4"></span>

### 7.4 Correlations and the CHSH experiment

**Core result / role:** CHSH classical bound and a quantum violation.

**Assumptions and scope:** Local hidden-variable model for the bound; declared quantum observables.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove the classical bound by conditioning; calculate a quantum value without inferring loophole-free evidence.

**Imported earlier results:** [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7), [7.3](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-3).

**Exact source targets:** [NC:2.6](../references/proof-sources.md#source-nc-2-6): Section 2.6 EPR and the Bell inequality.

**Independent evidence target:** Compare the exact correlators and finite-sample estimates without implying a loophole-free hardware test.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-entanglement-and-quantum-information-protocols-5"></span>

### 7.5 Teleportation, branch by branch

**Core result / role:** Teleportation correctness in every branch.

**Assumptions and scope:** Unknown input; shared Bell pair; two classical bits.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Expand four outcomes and prove each conditional correction recovers the input.

**Imported earlier results:** [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [7.3](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-3).

**Exact source targets:** [NC:1.3.7](../references/proof-sources.md#source-nc-1-3-7): Section 1.3.7 Example: quantum teleportation.

**Independent evidence target:** Verify each branch for several general complex inputs.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-entanglement-and-quantum-information-protocols-6"></span>

### 7.6 Superdense coding

**Core result / role:** Dense-coding decode identity.

**Assumptions and scope:** Shared Bell pair; one transmitted qubit; agreed encoding.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove the four encoded states are distinguishable by one Bell measurement.

**Imported earlier results:** [7.3](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-3), [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1).

**Exact source targets:** [NC:2.3](../references/proof-sources.md#source-nc-2-3): Section 2.3 Application: superdense coding.

**Independent evidence target:** Check every message and report entanglement and communication requirements.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-entanglement-and-quantum-information-protocols-7"></span>

### 7.7 No-signalling and classical communication

**Core result / role:** No-signalling through local nonselective measurement.

**Assumptions and scope:** Local complete measurement; no conditioned remote record.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Sum joint probabilities and prove the remote marginal is unchanged.

**Imported earlier results:** [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [7.3](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-3).

**Exact source targets:** [NC:2.2.8](../references/proof-sources.md#source-nc-2-2-8): Section 2.2.8 Composite systems.

**Independent evidence target:** Compare conditioned and unconditioned statistics; connect the density-matrix proof to Chapter 8.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-network-entanglement-primitives"></span>

### 7.8 Entanglement swapping and quantum-network primitives

**Core result / role:** Entanglement-swapping branch identity.

**Assumptions and scope:** Two Bell pairs; middle Bell measurement; communicated outcome.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Expand the four conditional outer states and required Pauli corrections; distinguish link creation from signalling.

**Imported earlier results:** [7.3](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-3), [7.5](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-5), [7.7](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-7).

**Exact source targets:** [NC:1.3.7](../references/proof-sources.md#source-nc-1-3-7): Section 1.3.7 Example: quantum teleportation; [NET:links](../references/proof-sources.md#source-net-links): Elementary quantum networks, nodes, channels and entanglement distribution.

**Independent evidence target:** Enumerate all branches of a tiny swapping protocol, track classical corrections and state explicitly which quantum links are assumed.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-entanglement-and-quantum-information-protocols-8"></span>

### 7.9 What entanglement alone does not guarantee

**Core result / role:** Entanglement is insufficient for unrestricted tasks.

**Assumptions and scope:** Specified local operations and output task.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Use no-signalling and no-cloning to construct task-specific counterexamples.

**Imported earlier results:** [7.5](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-5), [7.6](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-6), [7.7](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-7), [7.8](../section-plans/01-foundations.md#sec-network-entanglement-primitives).

**Exact source targets:** [NC:2.2.8](../references/proof-sources.md#source-nc-2-2-8): Section 2.2.8 Composite systems.

**Independent evidence target:** Analyze a failed protocol proposal and identify its missing assumption or resource.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 8: Density Matrices, Reduced States, and Purification

<span id="sec-density-matrices-reduced-states-and-purification-1"></span>

### 8.1 Statistical ensembles and density operators

**Core result / role:** Ensemble density operator reproduces all measurement probabilities.

**Assumptions and scope:** Classical mixture of normalized vectors.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive trace expectations and show distinct ensembles can be operationally equivalent.

**Imported earlier results:** [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3), [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Exact source targets:** [NC:2.4.1](../references/proof-sources.md#source-nc-2-4-1): Section 2.4.1 Ensembles of quantum states.

**Independent evidence target:** Compare different ensembles that produce the same operator.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-density-matrices-reduced-states-and-purification-2"></span>

### 8.2 Pure states, mixed states, and purity

**Core result / role:** Purity criterion for finite density operators.

**Assumptions and scope:** Positive unit-trace operator.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Use its eigenvalues to prove purity at most one with equality exactly for rank one.

**Imported earlier results:** [8.1](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-1), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Exact source targets:** [NC:2.4.2](../references/proof-sources.md#source-nc-2-4-2): Section 2.4.2 General properties of the density operator.

**Independent evidence target:** Check pure, mixed and deliberately nonphysical matrices.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-density-matrices-reduced-states-and-purification-3"></span>

### 8.3 Expectation values and measurement updates

**Core result / role:** Selective and nonselective density updates.

**Assumptions and scope:** Complete instrument; normalized density input.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive branch normalization and sum the unnormalized branch operators.

**Imported earlier results:** [8.1](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-1), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3).

**Exact source targets:** [NC:2.4.2](../references/proof-sources.md#source-nc-2-4-2): Section 2.4.2 General properties of the density operator; [NC:8.2.3](../references/proof-sources.md#source-nc-8-2-3): Section 8.2.3 Operator-sum representation.

**Independent evidence target:** Verify equivalence with pure-state formulas and ensemble averaging.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-density-matrices-reduced-states-and-purification-4"></span>

### 8.4 Partial trace from operational consistency

**Core result / role:** Partial trace is fixed by local expectations.

**Assumptions and scope:** Finite tensor product; all local observables.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive components from trace consistency and prove uniqueness.

**Imported earlier results:** [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [8.3](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-3).

**Exact source targets:** [NC:2.4.3](../references/proof-sources.md#source-nc-2-4-3): Section 2.4.3 The reduced density operator.

**Independent evidence target:** Compare explicit index sums with a tensor implementation.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-density-matrices-reduced-states-and-purification-5"></span>

### 8.5 Reduced states of entangled systems

**Core result / role:** Reduced spectra equal squared Schmidt coefficients.

**Assumptions and scope:** Normalized bipartite pure state.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Insert the Schmidt form and trace each subsystem explicitly.

**Imported earlier results:** [7.2](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-2), [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4).

**Exact source targets:** [NC:2.5](../references/proof-sources.md#source-nc-2-5): Section 2.5 The Schmidt decomposition and puriﬁcations.

**Independent evidence target:** Check Bell and nonmaximally entangled examples without confusing mixedness with classical preparation.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-density-matrices-reduced-states-and-purification-6"></span>

### 8.6 Purification and nonuniqueness

**Core result / role:** Purification and ancillary-unitary equivalence.

**Assumptions and scope:** Finite density operator; sufficiently large ancillary space.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Construct a spectral purification and prove equivalence on the supported ancillary subspace.

**Imported earlier results:** [8.2](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2), [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4).

**Exact source targets:** [TQI:2.1.3](../references/proof-sources.md#source-tqi-2-1-3): Section 2.1.3 Reductions and purifications of quantum states.

**Independent evidence target:** Trace out independently constructed purifications and compare the recovered state.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-density-matrices-reduced-states-and-purification-7"></span>

### 8.7 Proper and improper mixtures

**Core result / role:** Local measurements cannot distinguish proper and improper mixtures.

**Assumptions and scope:** Equal reduced density operators; local access only.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Compare every local effect; explain how joint access changes the task.

**Imported earlier results:** [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4), [8.6](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-6).

**Exact source targets:** [NC:2.4.3](../references/proof-sources.md#source-nc-2-4-3): Section 2.4.3 The reduced density operator.

**Independent evidence target:** Compare globally different preparations with identical local states.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-density-matrices-reduced-states-and-purification-8"></span>

### 8.8 Density-operator verification laboratory

**Core result / role:** Density-operator acceptance protocol.

**Assumptions and scope:** Finite tolerance and declared reference representation.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Reuse 8.1–8.6; test trace, positivity, partial traces and operational equivalence.

**Imported earlier results:** [8.2](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2), [8.3](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-3), [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4), [8.5](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-5), [2.8](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-8).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Diagnose positivity, trace, basis-order and partial-trace implementation errors.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.
