# Part 3. Quantum Algorithms and Computational Resources

**Detailed plan · 2026-10-20 · Planned material; architecture review pending.** [All sections](../section-plan.md) · [Full plan](../book-plan.md) · [Reader continuity](../reader-continuity.md)

Each section specifies its argument and independent evidence. Framework implementation, mathematical review and reader review have separate status. Closing materials follow the [section-plan guide](../section-plan.md#how-to-read-the-specification).

<span id="ch-computational-models-complexity-and-quantum-advantage"></span>

## Chapter 14

**Computational Models, Complexity, and Quantum Advantage**

**Reading level:** Core. **Chapter prerequisites:** 4–6.

<span id="sec-computational-models-complexity-and-quantum-advantage-1"></span>

### 14.1 Problems, input length, and computational models

**Learning and derivation target:** Define families of problems and distinguish finite examples from algorithms.

**Implementation and evidence target:** Specify task size and required output for representative problems.

<span id="sec-computational-models-complexity-and-quantum-advantage-2"></span>

### 14.2 Reversible computation and uniform circuit families

**Learning and derivation target:** Explain uniformity, classical control and efficient circuit generation.

**Implementation and evidence target:** Audit a circuit generator's workspace and construction cost.

<span id="sec-computational-models-complexity-and-quantum-advantage-3"></span>

### 14.3 Complexity classes and bounded error

**Learning and derivation target:** Introduce P, BPP, BQP and promise problems at the declared level.

**Implementation and evidence target:** Classify model assumptions and avoid claiming unproved class separations.

<span id="sec-computational-models-complexity-and-quantum-advantage-4"></span>

### 14.4 Oracle and data-access models

**Learning and derivation target:** Distinguish black-box queries, explicit circuits and classical data loading.

**Implementation and evidence target:** Compare costs when the same oracle is free versus synthesized.

<span id="sec-computational-models-complexity-and-quantum-advantage-5"></span>

### 14.5 Accuracy, repetition, and success probability

**Learning and derivation target:** Derive a representative amplification/repetition argument.

**Implementation and evidence target:** Count runs and requested precision in a small complete task.

<span id="sec-computational-models-complexity-and-quantum-advantage-6"></span>

### 14.6 Complete resource accounting

**Learning and derivation target:** Combine gates, depth, ancillas, measurements and classical processing.

**Implementation and evidence target:** Build an auditable cost table including preparation and readout.

<span id="sec-computational-models-complexity-and-quantum-advantage-7"></span>

### 14.7 Classical baselines and advantage claims

**Learning and derivation target:** State what evidence supports an empirical or asymptotic comparison.

**Implementation and evidence target:** Diagnose omitted costs, unmatched error tolerances and inappropriate baselines.

<span id="sec-computational-models-complexity-and-quantum-advantage-8"></span>

### 14.8 Resource-audit laboratory

**Learning and derivation target:** Turn an informal algorithm claim into an explicit access and cost specification.

**Implementation and evidence target:** Recompute conclusions when input access or target accuracy changes.

<span id="ch-interference-oracles-and-phase-kickback"></span>

## Chapter 15

**Interference, Oracles, and Phase Kickback**

**Reading level:** Core. **Chapter prerequisites:** 5, 14.

<span id="sec-interference-oracles-and-phase-kickback-1"></span>

### 15.1 Boolean functions as reversible oracles

**Learning and derivation target:** Define a reversible oracle and its clean-workspace assumptions.

**Implementation and evidence target:** Compare truth tables with permutation matrices.

<span id="sec-interference-oracles-and-phase-kickback-2"></span>

### 15.2 Phase kickback

**Learning and derivation target:** Derive how an eigenstate target turns function evaluation into a phase.

**Implementation and evidence target:** Check basis and superposition inputs against a dense reference.

<span id="sec-interference-oracles-and-phase-kickback-3"></span>

### 15.3 Deutsch's problem

**Learning and derivation target:** Derive exact outcome probabilities and specify the classical comparison.

**Implementation and evidence target:** Enumerate the promised one-bit functions and count queries.

<span id="sec-interference-oracles-and-phase-kickback-4"></span>

### 15.4 The Deutsch-Jozsa promise

**Learning and derivation target:** Derive constructive/destructive interference for the promised cases.

**Implementation and evidence target:** Verify small oracles and identify behavior outside the promise.

<span id="sec-interference-oracles-and-phase-kickback-5"></span>

### 15.5 Bernstein-Vazirani and hidden parity

**Learning and derivation target:** Derive the phase pattern and recovered bit string.

**Implementation and evidence target:** Generate all tiny parity instances with explicit oracle construction.

<span id="sec-interference-oracles-and-phase-kickback-6"></span>

### 15.6 Oracle synthesis and uncomputation

**Learning and derivation target:** Connect an abstract function query to a reversible circuit.

**Implementation and evidence target:** Account for workspace, gate count and restoration.

<span id="sec-interference-oracles-and-phase-kickback-7"></span>

### 15.7 Interference-algorithm laboratory

**Learning and derivation target:** Identify the promise, amplitude calculation and resource claim in one complete example.

**Implementation and evidence target:** Compare gate-level, matrix and analytic outputs and diagnose a wrong phase convention.

<span id="ch-grover-search-amplitude-amplification-and-estimation"></span>

## Chapter 16

**Grover Search, Amplitude Amplification, and Estimation**

**Reading level:** Core with advanced extensions. **Chapter prerequisites:** 6, 14, 15; revisit after 17.

**Bridge:** read 16.1–16.5, then Chapter 17's phase-estimation sections, before 16.6–16.8.

<span id="sec-grover-search-amplitude-amplification-and-estimation-1"></span>

### 16.1 Search promises and marked subspaces

**Learning and derivation target:** Define a search oracle, marked fraction and requested outcome.

**Implementation and evidence target:** Check explicit small marked sets and access assumptions.

<span id="sec-grover-search-amplitude-amplification-and-estimation-2"></span>

### 16.2 Reflections and the invariant plane

**Learning and derivation target:** Derive the two-dimensional action of the Grover iterate.

**Implementation and evidence target:** Compare its matrix with the full-register construction.

<span id="sec-grover-search-amplitude-amplification-and-estimation-3"></span>

### 16.3 Success probability and stopping

**Learning and derivation target:** Derive the iteration-dependent success curve and overshoot.

**Implementation and evidence target:** Sweep iterations and compare every result with the formula.

<span id="sec-grover-search-amplitude-amplification-and-estimation-4"></span>

### 16.4 General amplitude amplification

**Learning and derivation target:** Extend the construction to a state-preparation unitary and its inverse.

**Implementation and evidence target:** Verify success amplification and include preparation/uncomputation cost.

<span id="sec-grover-search-amplitude-amplification-and-estimation-5"></span>

### 16.5 Unknown success probabilities [Advanced]

**Learning and derivation target:** Explain a scoped strategy when the marked fraction is unknown.

**Implementation and evidence target:** Compare success and expected query use over several declared instances.

<span id="sec-grover-search-amplitude-amplification-and-estimation-6"></span>

### 16.6 Phase-estimation-based amplitude estimation [Advanced; after 17]

**Learning and derivation target:** Derive the eigenphase connection and state an error/query guarantee.

**Implementation and evidence target:** Compare tiny estimation distributions after completing the relevant Chapter 17 sections.

<span id="sec-grover-search-amplitude-amplification-and-estimation-7"></span>

### 16.7 Alternative estimation strategies and Monte Carlo [Advanced]

**Learning and derivation target:** State selected estimator assumptions and cost/accuracy criteria.

**Implementation and evidence target:** Compare like-for-like access models and total queries without assuming every estimator is advantageous.

<span id="sec-grover-search-amplitude-amplification-and-estimation-8"></span>

### 16.8 Search-and-estimation laboratory

**Learning and derivation target:** Integrate oracle construction, iteration/estimation and output uncertainty.

**Implementation and evidence target:** Audit a complete experiment and diagnose incorrect reflection or success definitions.

<span id="ch-fourier-transforms-and-quantum-phase-estimation"></span>

## Chapter 17

**Fourier Transforms and Quantum Phase Estimation**

**Reading level:** Core. **Chapter prerequisites:** 4–6, 14, 15.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-1"></span>

### 17.1 The discrete Fourier transform

**Learning and derivation target:** Define phases, normalization and basis conventions.

**Implementation and evidence target:** Construct the dense transform and check unitarity.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-2"></span>

### 17.2 Factorizing the QFT

**Learning and derivation target:** Derive the tensor-product form and controlled-phase circuit.

**Implementation and evidence target:** Compare every small basis input with the Fourier matrix.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-3"></span>

### 17.3 Inverse transforms and qubit reversal

**Learning and derivation target:** Derive the inverse circuit and distinguish output reversal from numerical indexing.

**Implementation and evidence target:** Test explicit permutations and a round trip.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-4"></span>

### 17.4 Approximate QFT

**Learning and derivation target:** Derive an error estimate for omitting selected rotations.

**Implementation and evidence target:** Compare operator/state errors with the declared approximation criterion.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-5"></span>

### 17.5 Controlled powers and phase kickback

**Learning and derivation target:** Derive the phase register for a unitary eigenstate.

**Implementation and evidence target:** Verify powers of a known small unitary and count their construction cost.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-6"></span>

### 17.6 Exact-grid phase estimation

**Learning and derivation target:** Derive deterministic outcomes and binary phase conventions.

**Implementation and evidence target:** Check representable phases and readout ordering.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-7"></span>

### 17.7 Off-grid phases and superposed eigenstates

**Learning and derivation target:** Derive finite-precision probabilities and mixtures associated with eigenstate weights.

**Implementation and evidence target:** Compare the complete distribution with an independent geometric-series calculation.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-8"></span>

### 17.8 Precision, success, and algorithmic cost

**Learning and derivation target:** Relate register size, repetitions and controlled-evolution cost.

**Implementation and evidence target:** Audit a phase-estimation experiment including synthesis and state preparation.

<span id="ch-period-finding-factoring-and-algorithmic-arithmetic"></span>

## Chapter 18

**Period Finding, Factoring, and Algorithmic Arithmetic**

**Reading level:** Advanced. **Chapter prerequisites:** 5, 14, 17.

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-1"></span>

### 18.1 From factoring to order finding

**Learning and derivation target:** Derive the number-theoretic reduction and its success conditions.

**Implementation and evidence target:** Check both successful and exceptional classical instances.

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-2"></span>

### 18.2 Reversible modular arithmetic

**Learning and derivation target:** Construct a small modular multiplication/addition map with explicit valid-subspace behavior.

**Implementation and evidence target:** Compare truth tables and complete reversible operators.

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-3"></span>

### 18.3 Coherent modular exponentiation

**Learning and derivation target:** Derive controlled powers and workspace uncomputation.

**Implementation and evidence target:** Verify the function on all small inputs, including a superposition.

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-4"></span>

### 18.4 Period information from phase estimation

**Learning and derivation target:** Derive the measured phase distribution for order finding.

**Implementation and evidence target:** Compare circuit outputs with an independent spectral/distribution reference.

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-5"></span>

### 18.5 Continued fractions and candidate verification

**Learning and derivation target:** Derive conditions for recovering a denominator and checking an order.

**Implementation and evidence target:** Test ambiguous fractions and reject incorrect candidates.

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-6"></span>

### 18.6 Factoring end to end

**Learning and derivation target:** Combine quantum samples with randomized classical postprocessing.

**Implementation and evidence target:** Factor tiny integers without choosing circuits that assume the answer.

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-7"></span>

### 18.7 Arithmetic, synthesis, and resource growth

**Learning and derivation target:** Count gates, ancillas, precision and success amplification under a named construction.

**Implementation and evidence target:** Separate measured tiny-circuit costs from asymptotic estimates.

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-8"></span>

### 18.8 A reproducible factoring laboratory

**Learning and derivation target:** Record circuit generation, samples, postprocessing and failures.

**Implementation and evidence target:** Diagnose a precompiled demonstration that hides the difficult computation.

<span id="ch-hamiltonian-simulation-and-error-bounds"></span>

## Chapter 19

**Hamiltonian Simulation and Error Bounds**

**Reading level:** Core with advanced extensions. **Chapter prerequisites:** 2, 5, 14, 17.

<span id="sec-hamiltonian-simulation-and-error-bounds-1"></span>

### 19.1 Hamiltonians, evolution, and access models

**Learning and derivation target:** Specify the simulation task, norm scale, time and accuracy.

**Implementation and evidence target:** Compare a Pauli-list input with an abstract sparse-access model.

<span id="sec-hamiltonian-simulation-and-error-bounds-2"></span>

### 19.2 Commuting terms and exact factorizations

**Learning and derivation target:** Derive conditions under which exponentials factor exactly.

**Implementation and evidence target:** Check commuting and noncommuting counterexamples.

<span id="sec-hamiltonian-simulation-and-error-bounds-3"></span>

### 19.3 First-order product formulas

**Learning and derivation target:** Derive a finite-system commutator-based error estimate.

**Implementation and evidence target:** Compare simulated evolution with a dense exponential as step size changes.

<span id="sec-hamiltonian-simulation-and-error-bounds-4"></span>

### 19.4 Symmetric and higher-order constructions

**Learning and derivation target:** Derive a second-order formula and explain recursive extensions at a stated level.

**Implementation and evidence target:** Check observed error scaling against explicit assumptions.

<span id="sec-hamiltonian-simulation-and-error-bounds-5"></span>

### 19.5 Pauli-term exponentiation

**Learning and derivation target:** Translate a Pauli-string exponential into basis changes, parity accumulation and a rotation.

**Implementation and evidence target:** Compare full small unitaries with generator exponentials.

<span id="sec-hamiltonian-simulation-and-error-bounds-6"></span>

### 19.6 State, observable, and operator error

**Learning and derivation target:** Relate the requested output to the appropriate comparison metric.

**Implementation and evidence target:** Show that an accurate observable can coexist with a larger full-state error.

<span id="sec-hamiltonian-simulation-and-error-bounds-7"></span>

### 19.7 Alternative simulation paradigms [Advanced]

**Learning and derivation target:** Explain the access/precision questions that motivate LCU, qubitization and QSP.

**Implementation and evidence target:** Map an example's requirements to Chapters 20–21 without assuming their results.

<span id="sec-hamiltonian-adiabatic-model"></span>

### 19.8 Adiabatic computation and gap assumptions [Advanced]

**Learning and derivation target:** State an adiabatic theorem with its spectral-gap and smoothness assumptions; distinguish an algorithmic model from a device annealing schedule.

**Implementation and evidence target:** Compare a tiny gapped interpolation with exact time evolution and diagnose a schedule that violates the stated error conditions.

<span id="sec-hamiltonian-simulation-and-error-bounds-8"></span>
<span id="198-dynamics-laboratory-and-resource-budget"></span>

### 19.9 Dynamics laboratory and resource budget

**Learning and derivation target:** Combine decomposition, approximation, execution and error reporting.

**Implementation and evidence target:** Report gate count, step count, synthesis assumptions and a verified finite-system error.

<span id="ch-block-encodings-and-quantum-linear-algebra"></span>

## Chapter 20

**Block Encodings and Quantum Linear Algebra**

**Reading level:** Advanced. **Chapter prerequisites:** 2, 5, 14, 17, 19.

<span id="sec-block-encodings-and-quantum-linear-algebra-1"></span>

### 20.1 Why matrix access must be specified

**Learning and derivation target:** Define the computational input/output task and its normalization.

**Implementation and evidence target:** Audit a matrix problem with explicit data-loading and readout costs.

<span id="sec-block-encodings-and-quantum-linear-algebra-2"></span>

### 20.2 Block-encoding definitions and ancillas

**Learning and derivation target:** State normalization, approximation and subspace conventions.

**Implementation and evidence target:** Construct a tiny block encoding and extract its encoded block independently.

<span id="sec-block-encodings-and-quantum-linear-algebra-3"></span>

### 20.3 Linear combinations of unitaries

**Learning and derivation target:** Derive PREPARE/SELECT and the encoded weighted sum.

**Implementation and evidence target:** Verify normalization and success amplitudes for a two-term example.

<span id="sec-block-encodings-and-quantum-linear-algebra-4"></span>

### 20.4 Composing encoded operations

**Learning and derivation target:** Derive selected sum/product constructions and approximation propagation.

**Implementation and evidence target:** Compare encoded blocks with ordinary matrix arithmetic.

<span id="sec-block-encodings-and-quantum-linear-algebra-5"></span>

### 20.5 Postselection and amplification

**Learning and derivation target:** Derive success probability and explain input-state dependence.

**Implementation and evidence target:** Compare accepted branches with an independent projector calculation.

<span id="sec-block-encodings-and-quantum-linear-algebra-6"></span>

### 20.6 Quantum linear systems and conditioning

**Learning and derivation target:** Specify a state-output task and derive a representative condition-number/success dependence.

**Implementation and evidence target:** Solve a tiny system while reporting normalization, state error and readout requirements.

<span id="sec-block-encodings-and-quantum-linear-algebra-7"></span>

### 20.7 Spectral functions and application contracts

**Learning and derivation target:** State the domain, spectral promise and requested matrix function.

**Implementation and evidence target:** Build an acceptance specification for the QSVT chapter.

<span id="sec-block-encodings-and-quantum-linear-algebra-8"></span>

### 20.8 Linear-algebra laboratory

**Learning and derivation target:** Integrate encoding, preparation, transformation and output comparison.

**Implementation and evidence target:** Compare with an independent classical solve and identify unrealistic access assumptions.

<span id="ch-quantum-signal-processing-and-singular-value-transformation"></span>

## Chapter 21

**Quantum Signal Processing and Singular Value Transformation**

**Reading level:** Advanced. **Chapter prerequisites:** 16, 19, 20.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-1"></span>

### 21.1 A scalar signal encoded in SU(2)

**Learning and derivation target:** Fix a QSP convention and derive the elementary signal unitary.

**Implementation and evidence target:** Verify the matrix identity at interior and boundary signal values.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-2"></span>

### 21.2 Phase-controlled polynomial sequences

**Learning and derivation target:** Derive low-degree sequences and their parity structure.

**Implementation and evidence target:** Compare matrix products with independently expanded polynomials.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-3"></span>

### 21.3 Admissibility and approximation

**Learning and derivation target:** State parity, boundedness and domain constraints for the selected theorem.

**Implementation and evidence target:** Test admissible targets and explain a deliberately impossible target.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-4"></span>

### 21.4 Phase synthesis and numerical stability

**Learning and derivation target:** Explain the phase-finding problem and conditioning of a specified method.

**Implementation and evidence target:** Check residuals and sensitivity rather than assuming a returned phase list is correct.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-5"></span>

### 21.5 From eigenvalues to singular values

**Learning and derivation target:** Derive how a block encoding and projected rotations act on invariant subspaces.

**Implementation and evidence target:** Compare a small non-Hermitian example through its SVD.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-6"></span>

### 21.6 A precise QSVT theorem [Advanced]

**Learning and derivation target:** State the transformation theorem with normalization/error assumptions and a proof roadmap.

**Implementation and evidence target:** Verify selected finite cases while preserving the distinction between theorem and numerical evidence.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-7"></span>

### 21.7 Applications: filtering, inversion, and evolution

**Learning and derivation target:** Derive one complete application and state spectral-gap/conditioning requirements.

**Implementation and evidence target:** Compare transformed values with a classical matrix-function reference.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-8"></span>

### 21.8 Precision and complete complexity

**Learning and derivation target:** Combine polynomial degree, approximation, synthesis error and oracle costs.

**Implementation and evidence target:** Produce an auditable budget for the chosen application.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-9"></span>

### 21.9 Signal-processing laboratory

**Learning and derivation target:** Connect a target function, synthesized phases, block-encoded circuit and validation.

**Implementation and evidence target:** Report scalar-domain and matrix-level errors, including endpoints and failure cases.

<span id="ch-quantum-walks-lower-bounds-and-algorithm-design"></span>

## Chapter 22

**Quantum Walks, Lower Bounds, and Algorithm Design**

**Reading level:** Advanced. **Chapter prerequisites:** 14–21.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-1"></span>

### 22.1 Walk models and computational tasks

**Learning and derivation target:** Define a selected discrete-time quantum walk and its classical comparison.

**Implementation and evidence target:** Construct a small walk from an explicit graph.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-2"></span>

### 22.2 Unitarity, spectra, and dynamics

**Learning and derivation target:** Derive the walk's invariant structure or spectral relation.

**Implementation and evidence target:** Compare a circuit/tensor realization with an independent matrix.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-3"></span>

### 22.3 Search and marked vertices

**Learning and derivation target:** Specify the promised search task and derive a tractable success example.

**Implementation and evidence target:** Compare time-dependent marked probability under matched graph/access assumptions.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-4"></span>

### 22.4 Hitting behavior and algorithmic resources

**Learning and derivation target:** Explain which classical and quantum quantities are actually being compared.

**Implementation and evidence target:** Count initialization, walk steps, oracle use and readout.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-5"></span>

### 22.5 The polynomial method [Advanced]

**Learning and derivation target:** Derive how oracle algorithms induce bounded-degree acceptance expressions in a representative setting.

**Implementation and evidence target:** Check a small acceptance polynomial independently.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-6"></span>

### 22.6 A representative query lower bound

**Learning and derivation target:** State assumptions and work through a selected lower-bound argument.

**Implementation and evidence target:** Identify exactly which algorithm class/access model the result restricts.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-7"></span>

### 22.7 Choosing an algorithmic framework

**Learning and derivation target:** Relate walks, amplification and spectral transformations without claiming every method dominates.

**Implementation and evidence target:** Compare candidate approaches for the same small task.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-8"></span>

### 22.8 Algorithm-design laboratory

**Learning and derivation target:** Require a construction, proof obligation, access model and independent reference.

**Implementation and evidence target:** Diagnose an invalid speedup argument or a lower bound applied outside its model.
