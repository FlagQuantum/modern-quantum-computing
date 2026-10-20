# Part 1: Foundations and Quantum Information Primitives

**Detailed section plan · October 20, 2026 · Planned material.** [All section plans](../section-plan.md) · [Curriculum and prerequisites](../book-plan.md)

Each numbered section specifies its intended argument and independent evidence. The unnumbered closing material and authoring rules are defined in the [section-plan guide](../section-plan.md#how-to-read-the-specification). Implementation status remains separate from curriculum status.

## Chapter 1

**What Quantum Computing Computes**

**Reading level:** Core. **Chapter prerequisites:** Basic Python.

### 1.1 Problems, inputs, and observable outputs

**Learning and derivation target:** Identify a computational task and what an algorithm must return.

**Implementation and evidence target:** Specify input size, requested output and success criterion for a tiny task.

### 1.2 A first interference experiment

**Learning and derivation target:** Predict how two paths and a relative phase affect a measurement probability.

**Implementation and evidence target:** Compare a hand calculation, a two-by-two matrix reference and a small FlagQuantum circuit.

### 1.3 What a quantum state describes

**Learning and derivation target:** Introduce amplitudes and normalization informally; distinguish a state description from an observed sample.

**Implementation and evidence target:** Contrast full simulated amplitudes with the information available from repeated measurements.

### 1.4 Algorithms, simulators, and physical devices

**Learning and derivation target:** Explain the mathematical model, a classical executor and an experiment as different sources of evidence.

**Implementation and evidence target:** Annotate which parts of the opening calculation are mathematical, simulated or measured.

### 1.5 What computational advantage would require

**Learning and derivation target:** Introduce fair input/output access and total-resource accounting without requiring complexity theory.

**Implementation and evidence target:** Diagnose an invalid speedup claim based on simulator wall time or free data loading.

### 1.6 A map of the learning routes

**Learning and derivation target:** Explain the progression from a concrete question to definitions, proofs, implementation and evidence.

**Implementation and evidence target:** Choose an introductory route and complete a notation/background diagnostic.

## Chapter 2

**Complex Vectors, Operators, and Numerical Reasoning**

**Reading level:** Core. **Chapter prerequisites:** 1; introductory linear algebra.

### 2.1 Complex scalars, vectors, and conjugation

**Learning and derivation target:** Define complex arithmetic, conjugation and vector coordinates.

**Implementation and evidence target:** Check identities against explicit real/imaginary calculations.

### 2.2 Inner products, adjoints, and orthogonality

**Learning and derivation target:** Derive conjugate symmetry, normalization and orthogonal projection.

**Implementation and evidence target:** Compare hand calculations with tensor conjugation and inner products.

### 2.3 Linear maps, bases, and changes of coordinates

**Learning and derivation target:** Derive matrix representations and basis-change rules.

**Implementation and evidence target:** Check the same map in two bases and diagnose an omitted inverse.

### 2.4 Hermitian, unitary, and positive operators

**Learning and derivation target:** State the defining properties and derive elementary consequences for eigenvalues and norms.

**Implementation and evidence target:** Verify residuals and build counterexamples to confusing Hermiticity with unitarity.

### 2.5 Spectral decomposition and singular values

**Learning and derivation target:** Derive spectral reconstruction for Hermitian matrices and introduce SVD.

**Implementation and evidence target:** Reconstruct small operators and compare eigenvalue and singular-value diagnostics.

### 2.6 Functions of matrices and time evolution

**Learning and derivation target:** Define matrix functions through spectra and series; derive a Pauli exponential.

**Implementation and evidence target:** Compare independent series, eigendecomposition and matrix-exponential calculations.

### 2.7 Norms, conditioning, and perturbations

**Learning and derivation target:** Relate vector/operator norms and explain why a small residual may not imply a small solution error.

**Implementation and evidence target:** Perturb a nearly singular example and report condition-dependent sensitivity.

### 2.8 Floating-point arithmetic and verification contracts

**Learning and derivation target:** Explain rounding, absolute/relative tolerances and reproducibility limits.

**Implementation and evidence target:** Design assertions for tiny and order-one values and identify a misleading all-close test.

## Chapter 3

**Single-Qubit States and Rotations**

**Reading level:** Core. **Chapter prerequisites:** 2.

### 3.1 The pure-state postulate and physical equivalence

**Learning and derivation target:** State normalization and equivalence up to global phase.

**Implementation and evidence target:** Compare normalized vectors with and without phase alignment.

### 3.2 Relative phase and interference

**Learning and derivation target:** Derive how relative phase changes a subsequent measurement after a basis rotation.

**Implementation and evidence target:** Construct states with identical computational-basis probabilities and different interference.

### 3.3 The Bloch-sphere representation

**Learning and derivation target:** Derive Bloch coordinates of a pure qubit and their normalization.

**Implementation and evidence target:** Recover coordinates from independent Pauli expectations.

### 3.4 Closed-system evolution and generators

**Learning and derivation target:** State unitary evolution and connect Hermitian generators to continuous transformations.

**Implementation and evidence target:** Compare generator exponentiation with an explicit unitary.

### 3.5 Pauli algebra and rotation matrices

**Learning and derivation target:** Derive Pauli products and the three axis-rotation matrices.

**Implementation and evidence target:** Verify matrix formulas, inverse rotations and angle conventions.

### 3.6 Composing rotations

**Learning and derivation target:** Explain noncommutativity and parameterize a single-qubit unitary up to phase.

**Implementation and evidence target:** Compare two operation orders and verify a small decomposition.

### 3.7 Physical phase versus numerical equality

**Learning and derivation target:** Define an appropriate state-comparison criterion and its limitations.

**Implementation and evidence target:** Diagnose tests that reject a harmless global phase or overlook a changed relative phase.

### 3.8 The no-cloning theorem

**Learning and derivation target:** Prove the elementary inner-product argument and state its assumptions.

**Implementation and evidence target:** Contrast copying orthogonal basis states with the failure on a superposition; label the calculation as an illustration.

## Chapter 4

**Composite Systems, Tensor Products, and Qubit Ordering**

**Reading level:** Core. **Chapter prerequisites:** 2, 3.

### 4.1 Tensor-product spaces and basis states

**Learning and derivation target:** Construct composite spaces and derive product-state amplitudes.

**Implementation and evidence target:** Compare hand-built products with Kronecker-product references.

### 4.2 Registers, labels, and basis indices

**Learning and derivation target:** Derive the bit-string-to-index map for the stated most-significant-qubit convention.

**Implementation and evidence target:** Check every basis input for two and three qubits.

### 4.3 Local operators on a composite register

**Learning and derivation target:** Derive an operator acting on one selected subsystem.

**Implementation and evidence target:** Compare explicit Kronecker matrices with circuit execution.

### 4.4 Multiple-qubit operators and ordered supports

**Learning and derivation target:** Specify how operator arguments correspond to tensor axes and basis order.

**Implementation and evidence target:** Test a nonsymmetric two-qubit gate on nonadjacent qubits.

### 4.5 Permutations, SWAP, and relabeling

**Learning and derivation target:** Distinguish a physical SWAP from changing the description of subsystem labels.

**Implementation and evidence target:** Compare permutation matrices, reshaped arrays and actual SWAP gates.

### 4.6 Tensor reshaping as indexed mathematics

**Learning and derivation target:** Translate index sums into reshape, permute and contraction operations.

**Implementation and evidence target:** Implement a minimal local-operator reference without a full-register matrix.

### 4.7 Cross-framework convention translation

**Learning and derivation target:** Explain how an equivalent circuit can have a differently indexed statevector.

**Implementation and evidence target:** Build and verify an explicit permutation between two declared ordering conventions.

## Chapter 5

**Gates, Reversible Computation, and Circuit Synthesis**

**Reading level:** Core. **Chapter prerequisites:** 3, 4.

### 5.1 Circuit composition, inversion, and call order

**Learning and derivation target:** Derive the relation between chronological gate calls and matrix multiplication.

**Implementation and evidence target:** Check a nonsymmetric gate sequence and its inverse.

### 5.2 Controlled operations and ancillas

**Learning and derivation target:** Derive controlled-unitary blocks and the role of a clean control/ancilla.

**Implementation and evidence target:** Verify all basis inputs and a superposition control.

### 5.3 Classical logic made reversible

**Learning and derivation target:** Construct reversible Boolean maps and identify information discarded by ordinary gates.

**Implementation and evidence target:** Check a small truth table and account for auxiliary outputs.

### 5.4 Uncomputation and reusable workspace

**Learning and derivation target:** Derive compute-use-uncompute while retaining a desired result.

**Implementation and evidence target:** Verify restoration of workspace, including a coherent input.

### 5.5 Universal gate sets

**Learning and derivation target:** State exact versus approximate universality and its computational meaning.

**Implementation and evidence target:** Verify a small exact construction and delimit what a finite demonstration establishes.

### 5.6 Decomposing controlled and multi-qubit gates

**Learning and derivation target:** Derive selected decompositions with explicit ancilla assumptions.

**Implementation and evidence target:** Compare complete unitaries and count elementary operations.

### 5.7 Approximation, synthesis, and precision

**Learning and derivation target:** Define a unitary-error criterion and relate synthesis precision to circuit error.

**Implementation and evidence target:** Study a controlled approximation and compare it against an explicit bound.

### 5.8 Circuit identities and safe transformations

**Learning and derivation target:** State when cancellation, commuting gates and global-phase transformations preserve the requested result.

**Implementation and evidence target:** Test identities on complete small unitaries and give an invalid rewrite counterexample.

## Chapter 6

**Measurement, Expectation Values, and Statistical Estimation**

**Reading level:** Core. **Chapter prerequisites:** 3–5.

### 6.1 Measurement outcomes and the Born rule

**Learning and derivation target:** State projective measurement probabilities and normalization.

**Implementation and evidence target:** Compute rotated-qubit probabilities independently and expand the existing starter.

### 6.2 Conditional states and ignored outcomes

**Learning and derivation target:** Derive normalized post-measurement states and the unconditioned outcome-averaged state.

**Implementation and evidence target:** Verify both branches and show the difference between postselection and discarding a record.

### 6.3 Observables, spectra, and expectations

**Learning and derivation target:** Derive an expectation as a probability-weighted eigenvalue sum.

**Implementation and evidence target:** Compare spectral, matrix and FlagQuantum evaluations.

### 6.4 Measuring in another basis

**Learning and derivation target:** Derive the basis rotation needed for X and Y measurements.

**Implementation and evidence target:** Compare rotated computational-basis statistics with exact observable expectations.

### 6.5 Generalized measurements and instruments [Advanced]

**Learning and derivation target:** Define POVM effects and explain why outcome probabilities do not specify a state update.

**Implementation and evidence target:** Construct two instruments with the same effects and different conditional states.

### 6.6 From exact probabilities to samples

**Learning and derivation target:** Derive categorical/Bernoulli estimators and distinguish exact expectation from shots.

**Implementation and evidence target:** Compare seeded sampling with exact probabilities over repeated trials.

### 6.7 Variance, covariance, and uncertainty

**Learning and derivation target:** Derive estimator variance and explain covariance in combined observables.

**Implementation and evidence target:** Check predicted versus empirical variance using independent repetitions.

### 6.8 Confidence intervals and shot budgets

**Learning and derivation target:** Specify coverage assumptions and derive one usable concentration bound.

**Implementation and evidence target:** Test empirical coverage and shot-count scaling; avoid presenting one favorable run as validation.

### 6.9 Measurement laboratory and failure diagnosis

**Learning and derivation target:** Connect probabilities, conditional states, observables and statistical estimates.

**Implementation and evidence target:** Diagnose ordering, normalization and uncertainty-reporting errors in a small complete experiment.

## Chapter 7

**Entanglement and Quantum Information Protocols**

**Reading level:** Core. **Chapter prerequisites:** 4–6.

**Reading dependency:** Derive no-signalling first through marginal probabilities; revisit the reduced-density-operator argument after Chapter 8.

### 7.1 Product states and entangled states

**Learning and derivation target:** Define pure-state separability and show why local amplitudes are insufficient in general.

**Implementation and evidence target:** Compare explicit coefficient matrices of product and Bell states.

### 7.2 Schmidt decomposition

**Learning and derivation target:** Derive the bipartite decomposition by SVD and identify Schmidt rank.

**Implementation and evidence target:** Reconstruct a state and verify its coefficients; revisit reduced spectra in Chapter 8.

### 7.3 Bell states and basis changes

**Learning and derivation target:** Derive preparation and measurement in the Bell basis.

**Implementation and evidence target:** Check all four basis states and a general superposition.

### 7.4 Correlations and the CHSH experiment

**Learning and derivation target:** Derive a classical bound under explicit assumptions and calculate a quantum example.

**Implementation and evidence target:** Compare the exact correlators and finite-sample estimates without implying a loophole-free hardware test.

### 7.5 Teleportation, branch by branch

**Learning and derivation target:** Derive all four conditional receiver states and their corrections.

**Implementation and evidence target:** Verify each branch for several general complex inputs.

### 7.6 Superdense coding

**Learning and derivation target:** Derive message encoding and decoding and count the required shared resources.

**Implementation and evidence target:** Check every message and report entanglement and communication requirements.

### 7.7 No-signalling and classical communication

**Learning and derivation target:** Derive unchanged remote marginal probabilities when local outcomes are ignored.

**Implementation and evidence target:** Compare conditioned and unconditioned statistics; connect the density-matrix proof to Chapter 8.

### 7.8 What entanglement alone does not guarantee

**Learning and derivation target:** Distinguish correlation, communication and a usable computational protocol.

**Implementation and evidence target:** Analyze a failed protocol proposal and identify its missing assumption or resource.

## Chapter 8

**Density Matrices, Reduced States, and Purification**

**Reading level:** Core. **Chapter prerequisites:** 2, 4, 6, 7.

### 8.1 Statistical ensembles and density operators

**Learning and derivation target:** Derive the density matrix of a mixture and its basic properties.

**Implementation and evidence target:** Compare different ensembles that produce the same operator.

### 8.2 Pure states, mixed states, and purity

**Learning and derivation target:** Derive spectral and purity criteria and their assumptions.

**Implementation and evidence target:** Check pure, mixed and deliberately nonphysical matrices.

### 8.3 Expectation values and measurement updates

**Learning and derivation target:** Derive trace expressions for observables and measurement branches.

**Implementation and evidence target:** Verify equivalence with pure-state formulas and ensemble averaging.

### 8.4 Partial trace from operational consistency

**Learning and derivation target:** Derive the subsystem operator that reproduces every local expectation.

**Implementation and evidence target:** Compare explicit index sums with a tensor implementation.

### 8.5 Reduced states of entangled systems

**Learning and derivation target:** Relate reduced spectra to Schmidt coefficients.

**Implementation and evidence target:** Check Bell and nonmaximally entangled examples without confusing mixedness with classical preparation.

### 8.6 Purification and nonuniqueness

**Learning and derivation target:** Construct a purification from a spectral decomposition and explain freedom in its environment.

**Implementation and evidence target:** Trace out independently constructed purifications and compare the recovered state.

### 8.7 Proper and improper mixtures

**Learning and derivation target:** Explain what local statistics establish and how joint access can distinguish preparations.

**Implementation and evidence target:** Compare globally different preparations with identical local states.

### 8.8 Density-operator verification laboratory

**Learning and derivation target:** State physicality checks, numerical tolerances and comparison criteria.

**Implementation and evidence target:** Diagnose positivity, trace, basis-order and partial-trace implementation errors.
