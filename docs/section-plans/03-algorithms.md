# Part 3. Quantum Algorithms and Computational Resources

**Detailed plan · 2026-10-20 · Scope fixed by Writing Baseline 1.0; prose and independent acceptance pending.** [All sections](../section-plan.md) · [Full plan](../book-plan.md) · [Reader continuity](../reader-continuity.md)

Each section specifies its argument and independent evidence. Framework implementation, mathematical review and reader review have separate status. Closing materials follow the [section-plan guide](../section-plan.md#how-to-read-the-specification).

<span id="ch-computational-models-complexity-and-quantum-advantage"></span>

## Chapter 14

**Computational Models, Complexity, and Quantum Advantage**

**Reading level:** Core. **Entry guidance:** 4–6.

<span id="sec-computational-models-complexity-and-quantum-advantage-1"></span>

### 14.1 Problems, input length, and computational models

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-1).

**Section level:** core. **Required earlier sections:** [5.3](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-3), [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Learning and derivation target:** Define families of problems and distinguish finite examples from algorithms.

**Implementation and evidence target:** Specify task size and required output for representative problems.

<span id="sec-computational-models-complexity-and-quantum-advantage-2"></span>

### 14.2 Reversible computation and uniform circuit families

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-2).

**Section level:** core. **Required earlier sections:** [5.4](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4), [14.1](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-1).

**Learning and derivation target:** Explain uniformity, classical control and efficient circuit generation.

**Implementation and evidence target:** Audit a circuit generator's workspace and construction cost.

<span id="sec-computational-models-complexity-and-quantum-advantage-3"></span>

### 14.3 Complexity classes and bounded error

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-3).

**Section level:** core. **Required earlier sections:** [14.1](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-1), [14.2](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-2), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Learning and derivation target:** Introduce P, BPP, BQP and promise problems at the declared level.

**Implementation and evidence target:** Classify model assumptions and avoid claiming unproved class separations.

<span id="sec-computational-models-complexity-and-quantum-advantage-4"></span>

### 14.4 Oracle and data-access models

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4).

**Section level:** core. **Required earlier sections:** [14.1](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-1), [5.3](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-3).

**Learning and derivation target:** Distinguish black-box queries, explicit circuits and classical data loading.

**Implementation and evidence target:** Compare costs when the same oracle is free versus synthesized.

<span id="sec-computational-models-complexity-and-quantum-advantage-5"></span>

### 14.5 Accuracy, repetition, and success probability

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-5).

**Section level:** core. **Required earlier sections:** [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8), [14.3](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-3).

**Learning and derivation target:** Derive a representative amplification/repetition argument.

**Implementation and evidence target:** Count runs and requested precision in a small complete task.

<span id="sec-computational-models-complexity-and-quantum-advantage-6"></span>

### 14.6 Complete resource accounting

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Section level:** core. **Required earlier sections:** [14.1](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-1), [14.4](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4), [14.5](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-5).

**Learning and derivation target:** Combine gates, depth, ancillas, measurements and classical processing.

**Implementation and evidence target:** Build an auditable cost table including preparation and readout.

<span id="sec-hybrid-interaction-map"></span>

### 14.7 Quantum-classical interaction patterns

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-hybrid-interaction-map).

**Section level:** core. **Required earlier sections:** [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [14.1](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-1).

**Learning and derivation target:** Distinguish subroutine pipelines, outer optimization, hybrid learning, inference/reconstruction, decomposition/embedding and in-execution feedback; separate algorithm structure from runtime architecture.

**Implementation and evidence target:** Draw a typed data/control flow for a small task; identify host, device, measurement records, feedback boundary and complete resource costs.

<span id="sec-computational-models-complexity-and-quantum-advantage-7"></span>
<span id="147-classical-baselines-and-advantage-claims"></span>

### 14.8 Classical baselines and advantage claims

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-7).

**Section level:** core. **Required earlier sections:** [14.4](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Learning and derivation target:** State what evidence supports an empirical or asymptotic comparison.

**Implementation and evidence target:** Diagnose omitted costs, unmatched error tolerances and inappropriate baselines.

<span id="sec-computational-models-complexity-and-quantum-advantage-8"></span>
<span id="148-resource-audit-laboratory"></span>

### 14.9 Resource-audit laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-8).

**Section level:** core. **Required earlier sections:** [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6), [14.7](../section-plans/03-algorithms.md#sec-hybrid-interaction-map), [14.8](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-7).

**Learning and derivation target:** Turn an informal algorithm claim into an explicit access and cost specification.

**Implementation and evidence target:** Recompute conclusions when input access or target accuracy changes.

<span id="ch-interference-oracles-and-phase-kickback"></span>

## Chapter 15

**Interference, Oracles, and Phase Kickback**

**Reading level:** Core. **Entry guidance:** 5, 14; binary linear algebra is introduced locally for Simon’s problem.

<span id="sec-interference-oracles-and-phase-kickback-1"></span>

### 15.1 Boolean functions as reversible oracles

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-1).

**Section level:** core. **Required earlier sections:** [5.3](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-3), [5.4](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4), [14.4](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4).

**Learning and derivation target:** Define a reversible oracle and its clean-workspace assumptions.

**Implementation and evidence target:** Compare truth tables with permutation matrices.

<span id="sec-interference-oracles-and-phase-kickback-2"></span>

### 15.2 Phase kickback

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-2).

**Section level:** core. **Required earlier sections:** [15.1](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-1), [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5).

**Learning and derivation target:** Derive how an eigenstate target turns function evaluation into a phase.

**Implementation and evidence target:** Check basis and superposition inputs against a dense reference.

<span id="sec-interference-oracles-and-phase-kickback-3"></span>

### 15.3 Deutsch's problem

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-3).

**Section level:** core. **Required earlier sections:** [15.2](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-2), [6.1](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-1).

**Learning and derivation target:** Derive exact outcome probabilities and specify the classical comparison.

**Implementation and evidence target:** Enumerate the promised one-bit functions and count queries.

<span id="sec-interference-oracles-and-phase-kickback-4"></span>

### 15.4 The Deutsch-Jozsa promise

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-4).

**Section level:** core. **Required earlier sections:** [15.2](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-2), [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1).

**Learning and derivation target:** Derive constructive/destructive interference for the promised cases.

**Implementation and evidence target:** Verify small oracles and identify behavior outside the promise.

<span id="sec-interference-oracles-and-phase-kickback-5"></span>

### 15.5 Bernstein-Vazirani and hidden parity

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-5).

**Section level:** core. **Required earlier sections:** [15.2](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-2), [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2).

**Learning and derivation target:** Derive the phase pattern and recovered bit string.

**Implementation and evidence target:** Generate all tiny parity instances with explicit oracle construction.

<span id="sec-simon-hidden-structure"></span>

### 15.6 Simon’s problem and hidden structure

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-simon-hidden-structure).

**Section level:** core. **Required earlier sections:** [15.1](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-1), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [15.2](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-2).

**Learning and derivation target:** Introduce the necessary binary linear equations locally; derive the promised two-to-one interference distribution and the classical postprocessing for the hidden string.

**Implementation and evidence target:** Check every tiny valid instance and rank-deficient sample set against an independently enumerated oracle; state the query model and promise.

<span id="sec-interference-oracles-and-phase-kickback-6"></span>
<span id="156-oracle-synthesis-and-uncomputation"></span>

### 15.7 Oracle synthesis and uncomputation

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-6).

**Section level:** core. **Required earlier sections:** [15.1](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-1), [5.4](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4).

**Learning and derivation target:** Connect an abstract function query to a reversible circuit.

**Implementation and evidence target:** Account for workspace, gate count and restoration.

<span id="sec-interference-oracles-and-phase-kickback-7"></span>
<span id="157-interference-algorithm-laboratory"></span>

### 15.8 Interference-algorithm laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-7).

**Section level:** core. **Required earlier sections:** [15.4](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-4), [15.5](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-5), [15.6](../section-plans/03-algorithms.md#sec-simon-hidden-structure), [15.7](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-6).

**Learning and derivation target:** Identify the promise, amplitude calculation and resource claim in one complete example.

**Implementation and evidence target:** Compare gate-level, matrix and analytic outputs and diagnose a wrong phase convention.

<span id="ch-grover-search-amplitude-amplification-and-estimation"></span>

## Chapter 16

**Grover Search, Amplitude Amplification, and Estimation**

**Reading level:** Core with advanced extensions. **Entry guidance:** 5–6, 14–15; phase-free estimation has no Chapter 17 prerequisite.

**Bridge:** Chapter 16 uses phase-free estimation; the QPE-based derivation is 17.8, after phase estimation.

<span id="sec-grover-search-amplitude-amplification-and-estimation-1"></span>

### 16.1 Search promises and marked subspaces

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-1).

**Section level:** core. **Required earlier sections:** [14.4](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4), [15.1](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-1).

**Learning and derivation target:** Define a search oracle, marked fraction and requested outcome.

**Implementation and evidence target:** Check explicit small marked sets and access assumptions.

<span id="sec-grover-search-amplitude-amplification-and-estimation-2"></span>

### 16.2 Reflections and the invariant plane

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-2).

**Section level:** core. **Required earlier sections:** [16.1](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-1), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Learning and derivation target:** Derive the two-dimensional action of the Grover iterate.

**Implementation and evidence target:** Compare its matrix with the full-register construction.

<span id="sec-grover-search-amplitude-amplification-and-estimation-3"></span>

### 16.3 Success probability and stopping

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-3).

**Section level:** core. **Required earlier sections:** [16.2](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-2).

**Learning and derivation target:** Derive the iteration-dependent success curve and overshoot.

**Implementation and evidence target:** Sweep iterations and compare every result with the formula.

<span id="sec-grover-search-amplitude-amplification-and-estimation-4"></span>

### 16.4 General amplitude amplification

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-4).

**Section level:** core. **Required earlier sections:** [16.2](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-2), [5.4](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4).

**Learning and derivation target:** Extend the construction to a state-preparation unitary and its inverse.

**Implementation and evidence target:** Verify success amplification and include preparation/uncomputation cost.

<span id="sec-grover-search-amplitude-amplification-and-estimation-5"></span>

### 16.5 Unknown success probabilities [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-5).

**Section level:** advanced. **Required earlier sections:** [16.3](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-3), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Learning and derivation target:** Explain a scoped strategy when the marked fraction is unknown.

**Implementation and evidence target:** Compare success and expected query use over several declared instances.

<span id="sec-amplitude-estimation-phase-free"></span>

### 16.6 Amplitude estimation without phase estimation [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-amplitude-estimation-phase-free).

**Section level:** advanced. **Required earlier sections:** [16.3](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-3), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Learning and derivation target:** Use the previously derived amplification success curve to construct a small likelihood-based estimator; introduce the required statistical inference locally and state identifiability/aliasing assumptions.

**Implementation and evidence target:** Compare amplified Bernoulli data and an explicit one-dimensional likelihood grid with exact probabilities; account for total oracle calls and uncertainty.

<span id="sec-grover-search-amplitude-amplification-and-estimation-7"></span>
<span id="167-alternative-estimation-strategies-and-monte-carlo-advanced"></span>

### 16.7 Classical estimation, uncertainty, and query comparisons [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-7).

**Section level:** advanced. **Required earlier sections:** [16.4](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-4), [16.6](../section-plans/03-algorithms.md#sec-amplitude-estimation-phase-free), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Learning and derivation target:** Compare ordinary Monte Carlo and the selected phase-free scheme under the same access, accuracy and success criteria; phase-estimation-based derivations are owned by Chapter 17.

**Implementation and evidence target:** Compare like-for-like access models and total queries without assuming every estimator is advantageous.

<span id="sec-grover-search-amplitude-amplification-and-estimation-8"></span>

### 16.8 Search-and-estimation laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-8).

**Section level:** core. **Required earlier sections:** [16.3](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-3), [16.4](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-4), [16.6](../section-plans/03-algorithms.md#sec-amplitude-estimation-phase-free), [16.7](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-7).

**Learning and derivation target:** Integrate oracle construction, iteration/estimation and output uncertainty.

**Implementation and evidence target:** Audit a complete experiment and diagnose incorrect reflection or success definitions.

<span id="ch-fourier-transforms-and-quantum-phase-estimation"></span>

## Chapter 17

**Fourier Transforms and Quantum Phase Estimation**

**Reading level:** Core. **Entry guidance:** 4–6, 14–15; amplitude-estimation extension follows phase estimation here.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-1"></span>

### 17.1 The discrete Fourier transform

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-1).

**Section level:** core. **Required earlier sections:** [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3), [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2).

**Learning and derivation target:** Define phases, normalization and basis conventions.

**Implementation and evidence target:** Construct the dense transform and check unitarity.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-2"></span>

### 17.2 Factorizing the QFT

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-2).

**Section level:** core. **Required earlier sections:** [17.1](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-1), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Learning and derivation target:** Derive the tensor-product form and controlled-phase circuit.

**Implementation and evidence target:** Compare every small basis input with the Fourier matrix.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-3"></span>

### 17.3 Inverse transforms and qubit reversal

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-3).

**Section level:** core. **Required earlier sections:** [17.2](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-2), [4.5](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-5).

**Learning and derivation target:** Derive the inverse circuit and distinguish output reversal from numerical indexing.

**Implementation and evidence target:** Test explicit permutations and a round trip.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-4"></span>

### 17.4 Approximate QFT

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-4).

**Section level:** core. **Required earlier sections:** [17.2](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-2), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Learning and derivation target:** Derive an error estimate for omitting selected rotations.

**Implementation and evidence target:** Compare operator/state errors with the declared approximation criterion.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-5"></span>

### 17.5 Controlled powers and phase kickback

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-5).

**Section level:** core. **Required earlier sections:** [15.2](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-2), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Learning and derivation target:** Derive the phase register for a unitary eigenstate.

**Implementation and evidence target:** Verify powers of a known small unitary and count their construction cost.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-6"></span>

### 17.6 Exact-grid phase estimation

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-6).

**Section level:** core. **Required earlier sections:** [17.3](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-3), [17.5](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-5).

**Learning and derivation target:** Derive deterministic outcomes and binary phase conventions.

**Implementation and evidence target:** Check representable phases and readout ordering.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-7"></span>

### 17.7 Off-grid phases and superposed eigenstates

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-7).

**Section level:** core. **Required earlier sections:** [17.6](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-6), [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Learning and derivation target:** Derive finite-precision probabilities and mixtures associated with eigenstate weights.

**Implementation and evidence target:** Compare the complete distribution with an independent geometric-series calculation.

<span id="sec-grover-search-amplitude-amplification-and-estimation-6"></span>
<span id="166-phase-estimation-based-amplitude-estimation-advanced-after-17"></span>

### 17.8 Phase-estimation-based amplitude estimation [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-6).

**Section level:** advanced. **Required earlier sections:** [16.2](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-2), [16.4](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-4), [17.7](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-7).

**Learning and derivation target:** Derive the eigenphase connection and state an error/query guarantee.

**Implementation and evidence target:** Compare tiny estimation distributions after completing the relevant Chapter 17 sections.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-8"></span>
<span id="178-precision-success-and-algorithmic-cost"></span>

### 17.9 Precision, success, and algorithmic cost

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-8).

**Section level:** core. **Required earlier sections:** [17.4](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-4), [17.7](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-7), [17.8](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-6), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Learning and derivation target:** Relate register size, repetition, input-eigenstate overlap and controlled-evolution cost. Explain why phase estimation alone does not supply a ground-state preparation.

**Implementation and evidence target:** Audit a phase-estimation experiment including synthesis and state preparation.

<span id="ch-period-finding-factoring-and-algorithmic-arithmetic"></span>

## Chapter 18

**Period Finding, Factoring, and Algorithmic Arithmetic**

**Reading level:** Advanced. **Entry guidance:** 5, 14, 17; number-theory/group bridges are local.

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-1"></span>

### 18.1 From factoring to order finding

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-1).

**Section level:** advanced. **Required earlier sections:** [14.4](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4).

**Learning and derivation target:** Provide a local gcd/modular-arithmetic bridge, then derive the factoring-to-order-finding reduction and its success conditions.

**Implementation and evidence target:** Check both successful and exceptional classical instances.

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-2"></span>

### 18.2 Reversible modular arithmetic

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-2).

**Section level:** advanced. **Required earlier sections:** [5.3](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-3), [5.4](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4), [18.1](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-1).

**Learning and derivation target:** Construct a small modular multiplication/addition map with explicit valid-subspace behavior.

**Implementation and evidence target:** Compare truth tables and complete reversible operators.

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-3"></span>

### 18.3 Coherent modular exponentiation

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-3).

**Section level:** advanced. **Required earlier sections:** [18.2](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-2), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Learning and derivation target:** Derive controlled powers and workspace uncomputation.

**Implementation and evidence target:** Verify the function on all small inputs, including a superposition.

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-4"></span>

### 18.4 Period information from phase estimation

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-4).

**Section level:** advanced. **Required earlier sections:** [17.7](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-7), [18.3](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-3).

**Learning and derivation target:** Derive the measured phase distribution for order finding.

**Implementation and evidence target:** Compare circuit outputs with an independent spectral/distribution reference.

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-5"></span>

### 18.5 Continued fractions and candidate verification

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-5).

**Section level:** advanced. **Required earlier sections:** [18.1](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-1), [18.4](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-4).

**Learning and derivation target:** Derive conditions for recovering a denominator and checking an order.

**Implementation and evidence target:** Test ambiguous fractions and reject incorrect candidates.

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-6"></span>

### 18.6 Factoring end to end

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-6).

**Section level:** advanced. **Required earlier sections:** [18.4](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-4), [18.5](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-5).

**Learning and derivation target:** Combine quantum samples with randomized classical postprocessing.

**Implementation and evidence target:** Factor tiny integers without choosing circuits that assume the answer.

<span id="sec-abelian-hidden-subgroups"></span>

### 18.7 Discrete logarithms and Abelian hidden subgroups [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-abelian-hidden-subgroups).

**Section level:** advanced. **Required earlier sections:** [17.1](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-1), [15.6](../section-plans/03-algorithms.md#sec-simon-hidden-structure), [18.4](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-4).

**Learning and derivation target:** Introduce finite-group/character notation locally and derive one small Abelian hidden-subgroup or discrete-log instance as a generalization of period finding; delimit non-Abelian extensions.

**Implementation and evidence target:** Enumerate a tiny group, compare Fourier-sampling distributions and validate classical candidate recovery under the declared access model.

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-7"></span>
<span id="187-arithmetic-synthesis-and-resource-growth"></span>

### 18.8 Arithmetic, synthesis, and resource growth

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-7).

**Section level:** advanced. **Required earlier sections:** [18.2](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-2), [18.3](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-3), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Learning and derivation target:** Count gates, ancillas, precision and success amplification under a named construction.

**Implementation and evidence target:** Separate measured tiny-circuit costs from asymptotic estimates.

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-8"></span>
<span id="188-a-reproducible-factoring-laboratory"></span>

### 18.9 A reproducible factoring laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-8).

**Section level:** advanced. **Required earlier sections:** [18.6](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-6), [18.8](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-7).

**Learning and derivation target:** Record circuit generation, samples, postprocessing and failures.

**Implementation and evidence target:** Diagnose a precompiled demonstration that hides the difficult computation.

<span id="ch-hamiltonian-simulation-and-error-bounds"></span>

## Chapter 19

**Hamiltonian Simulation and Error Bounds**

**Reading level:** Core with advanced extensions. **Entry guidance:** 2, 5 for dynamics; 14 for resource analysis; no QFT/phase-estimation prerequisite for product formulas.

<span id="sec-hamiltonian-simulation-and-error-bounds-1"></span>

### 19.1 Hamiltonians, evolution, and access models

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-1).

**Section level:** core. **Required earlier sections:** [2.6](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-6), [3.4](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-4).

**Learning and derivation target:** Specify the simulation task, norm scale, time and accuracy.

**Implementation and evidence target:** Compare a Pauli-list input with an abstract sparse-access model.

<span id="sec-hamiltonian-simulation-and-error-bounds-2"></span>

### 19.2 Commuting terms and exact factorizations

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-2).

**Section level:** core. **Required earlier sections:** [19.1](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-1).

**Learning and derivation target:** Derive conditions under which exponentials factor exactly.

**Implementation and evidence target:** Check commuting and noncommuting counterexamples.

<span id="sec-hamiltonian-simulation-and-error-bounds-3"></span>

### 19.3 First-order product formulas

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-3).

**Section level:** core. **Required earlier sections:** [19.2](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-2), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Learning and derivation target:** Derive a finite-system commutator-based error estimate.

**Implementation and evidence target:** Compare simulated evolution with a dense exponential as step size changes.

<span id="sec-hamiltonian-simulation-and-error-bounds-4"></span>

### 19.4 Symmetric and higher-order constructions

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-4).

**Section level:** core. **Required earlier sections:** [19.3](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-3).

**Learning and derivation target:** Derive a second-order formula and explain recursive extensions at a stated level.

**Implementation and evidence target:** Check observed error scaling against explicit assumptions.

<span id="sec-hamiltonian-simulation-and-error-bounds-5"></span>

### 19.5 Pauli-term exponentiation

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-5).

**Section level:** core. **Required earlier sections:** [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5), [5.4](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4), [19.1](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-1).

**Learning and derivation target:** Translate a Pauli-string exponential into basis changes, parity accumulation and a rotation.

**Implementation and evidence target:** Compare full small unitaries with generator exponentials.

<span id="sec-hamiltonian-simulation-and-error-bounds-6"></span>

### 19.6 State, observable, and operator error

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-6).

**Section level:** core. **Required earlier sections:** [19.3](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-3), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Learning and derivation target:** Relate the requested output to the appropriate comparison metric.

**Implementation and evidence target:** Show that an accurate observable can coexist with a larger full-state error.

<span id="sec-hamiltonian-simulation-and-error-bounds-7"></span>

### 19.7 Alternative simulation paradigms [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-7).

**Section level:** advanced. **Required earlier sections:** [19.1](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-1), [14.4](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4).

**Learning and derivation target:** Explain the access/precision questions that motivate LCU, qubitization and QSP.

**Implementation and evidence target:** Map an example's requirements to Chapters 20–21 without assuming their results.

<span id="sec-hamiltonian-adiabatic-model"></span>

### 19.8 Adiabatic computation and gap assumptions [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-hamiltonian-adiabatic-model).

**Section level:** advanced. **Required earlier sections:** [19.1](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-1), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Learning and derivation target:** State an adiabatic theorem with its spectral-gap and smoothness assumptions; distinguish an algorithmic model from a device annealing schedule.

**Implementation and evidence target:** Compare a tiny gapped interpolation with exact time evolution and diagnose a schedule that violates the stated error conditions.

<span id="sec-hamiltonian-simulation-and-error-bounds-8"></span>
<span id="198-dynamics-laboratory-and-resource-budget"></span>

### 19.9 Dynamics laboratory and resource budget

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-8).

**Section level:** core. **Required earlier sections:** [19.3](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-3), [19.4](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-4), [19.5](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-5), [19.6](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-6), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Learning and derivation target:** Combine decomposition, approximation, execution and error reporting.

**Implementation and evidence target:** Report gate count, step count, synthesis assumptions and a verified finite-system error.

<span id="ch-block-encodings-and-quantum-linear-algebra"></span>

## Chapter 20

**Block Encodings and Quantum Linear Algebra**

**Reading level:** Advanced. **Entry guidance:** 2, 5, 14; selected 16 for amplification and 19 for dynamics applications.

<span id="sec-block-encodings-and-quantum-linear-algebra-1"></span>

### 20.1 Why matrix access must be specified

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-1).

**Section level:** advanced. **Required earlier sections:** [14.4](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Learning and derivation target:** Define the computational input/output task and its normalization.

**Implementation and evidence target:** Audit a matrix problem with explicit data-loading and readout costs.

<span id="sec-block-encodings-and-quantum-linear-algebra-2"></span>

### 20.2 Block-encoding definitions and ancillas

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-2).

**Section level:** advanced. **Required earlier sections:** [20.1](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-1), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Learning and derivation target:** State normalization, approximation and subspace conventions.

**Implementation and evidence target:** Construct a tiny block encoding and extract its encoded block independently.

<span id="sec-block-encodings-and-quantum-linear-algebra-3"></span>

### 20.3 Linear combinations of unitaries

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-3).

**Section level:** advanced. **Required earlier sections:** [20.2](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-2), [5.4](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4).

**Learning and derivation target:** Derive PREPARE/SELECT and the encoded weighted sum.

**Implementation and evidence target:** Verify normalization and success amplitudes for a two-term example.

<span id="sec-block-encodings-and-quantum-linear-algebra-4"></span>

### 20.4 Composing encoded operations

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-4).

**Section level:** advanced. **Required earlier sections:** [20.2](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-2), [20.3](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-3).

**Learning and derivation target:** Derive selected sum/product constructions and approximation propagation.

**Implementation and evidence target:** Compare encoded blocks with ordinary matrix arithmetic.

<span id="sec-block-encodings-and-quantum-linear-algebra-5"></span>

### 20.5 Postselection and amplification

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-5).

**Section level:** advanced. **Required earlier sections:** [20.3](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-3), [16.4](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-4).

**Learning and derivation target:** Derive success probability and explain input-state dependence.

**Implementation and evidence target:** Compare accepted branches with an independent projector calculation.

<span id="sec-block-encodings-and-quantum-linear-algebra-6"></span>

### 20.6 Quantum linear systems and conditioning

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-6).

**Section level:** advanced. **Required earlier sections:** [20.2](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-2), [20.5](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-5), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Learning and derivation target:** Specify a state-output task and derive a representative condition-number/success dependence. A directly constructed tiny inverse block is an explicitly costly reference; scalable spectral transformation is developed in Chapter 21.

**Implementation and evidence target:** Solve a tiny system while reporting normalization, state error and readout requirements. Report the construction cost rather than treating the desired inverse block as free input.

<span id="sec-qubitization-invariant-subspaces"></span>

### 20.7 Qubitization and invariant subspaces [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-qubitization-invariant-subspaces).

**Section level:** advanced. **Required earlier sections:** [20.2](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-2), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Learning and derivation target:** Derive a selected walk from a normalized Hermitian block encoding and explicit projection/reflection assumptions; connect eigenvalues to the resulting invariant two-dimensional action.

**Implementation and evidence target:** Compare the encoded block, walk spectrum and invariant-subspace calculation with independent small matrices before QSP/QSVT applications.

<span id="sec-block-encodings-and-quantum-linear-algebra-7"></span>
<span id="207-spectral-functions-and-application-contracts"></span>

### 20.8 Spectral functions and application contracts

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-7).

**Section level:** advanced. **Required earlier sections:** [20.6](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-6), [20.7](../section-plans/03-algorithms.md#sec-qubitization-invariant-subspaces).

**Learning and derivation target:** State the domain, spectral promise and requested matrix function.

**Implementation and evidence target:** Build an acceptance specification for the QSVT chapter.

<span id="sec-block-encodings-and-quantum-linear-algebra-8"></span>
<span id="208-linear-algebra-laboratory"></span>

### 20.9 Linear-algebra laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-8).

**Section level:** advanced. **Required earlier sections:** [20.3](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-3), [20.5](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-5), [20.6](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-6), [20.8](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-7).

**Learning and derivation target:** Integrate encoding, preparation, transformation and output comparison.

**Implementation and evidence target:** Compare with an independent classical solve and identify unrealistic access assumptions.

<span id="ch-quantum-signal-processing-and-singular-value-transformation"></span>

## Chapter 21

**Quantum Signal Processing and Singular Value Transformation**

**Reading level:** Advanced. **Entry guidance:** 2, 5, block-encoding sections of 20; application-specific dependencies are listed per section.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-1"></span>

### 21.1 A scalar signal encoded in SU(2)

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-1).

**Section level:** advanced. **Required earlier sections:** [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5), [20.2](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-2).

**Learning and derivation target:** Fix a QSP convention and derive the elementary signal unitary.

**Implementation and evidence target:** Verify the matrix identity at interior and boundary signal values.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-2"></span>

### 21.2 Phase-controlled polynomial sequences

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-2).

**Section level:** advanced. **Required earlier sections:** [21.1](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-1).

**Learning and derivation target:** Derive low-degree sequences and their parity structure.

**Implementation and evidence target:** Compare matrix products with independently expanded polynomials.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-3"></span>

### 21.3 Admissibility and approximation

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-3).

**Section level:** advanced. **Required earlier sections:** [21.2](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-2), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Learning and derivation target:** State parity, boundedness and domain constraints for the selected theorem.

**Implementation and evidence target:** Test admissible targets and explain a deliberately impossible target.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-4"></span>

### 21.4 Phase synthesis and numerical stability

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-4).

**Section level:** advanced. **Required earlier sections:** [21.3](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-3), [2.8](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-8).

**Learning and derivation target:** Explain the phase-finding problem and conditioning of a specified method.

**Implementation and evidence target:** Check residuals and sensitivity rather than assuming a returned phase list is correct.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-5"></span>

### 21.5 From eigenvalues to singular values

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-5).

**Section level:** advanced. **Required earlier sections:** [20.7](../section-plans/03-algorithms.md#sec-qubitization-invariant-subspaces), [21.2](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-2), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Learning and derivation target:** Derive how a block encoding and projected rotations act on invariant subspaces.

**Implementation and evidence target:** Compare a small non-Hermitian example through its SVD.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-6"></span>

### 21.6 A precise QSVT theorem [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-6).

**Section level:** advanced. **Required earlier sections:** [21.3](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-3), [21.5](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-5).

**Learning and derivation target:** State the transformation theorem with normalization/error assumptions and a proof roadmap.

**Implementation and evidence target:** Verify selected finite cases while preserving the distinction between theorem and numerical evidence.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-7"></span>

### 21.7 Applications: filtering, inversion, and evolution

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-7).

**Section level:** advanced. **Required earlier sections:** [21.6](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-6), [20.8](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-7), [19.1](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-1).

**Learning and derivation target:** Derive one complete application and state spectral-gap/conditioning requirements.

**Implementation and evidence target:** Compare transformed values with a classical matrix-function reference.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-8"></span>

### 21.8 Precision and complete complexity

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-8).

**Section level:** advanced. **Required earlier sections:** [21.4](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-4), [21.7](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-7), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Learning and derivation target:** Combine polynomial degree, approximation, synthesis error and oracle costs.

**Implementation and evidence target:** Produce an auditable budget for the chosen application.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-9"></span>

### 21.9 Signal-processing laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-9).

**Section level:** advanced. **Required earlier sections:** [21.4](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-4), [21.5](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-5), [21.7](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-7), [21.8](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-8).

**Learning and derivation target:** Connect a target function, synthesized phases, block-encoded circuit and validation.

**Implementation and evidence target:** Report scalar-domain and matrix-level errors, including endpoints and failure cases.

<span id="ch-quantum-walks-lower-bounds-and-algorithm-design"></span>

## Chapter 22

**Quantum Walks, Lower Bounds, and Algorithm Design**

**Reading level:** Advanced. **Entry guidance:** 5, 14, 16 for entry; selected 20–21 for spectral-framework comparisons.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-1"></span>

### 22.1 Walk models and computational tasks

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-1).

**Section level:** advanced. **Required earlier sections:** [14.4](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Learning and derivation target:** Define a selected discrete-time quantum walk and its classical comparison.

**Implementation and evidence target:** Construct a small walk from an explicit graph.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-2"></span>

### 22.2 Unitarity, spectra, and dynamics

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-2).

**Section level:** advanced. **Required earlier sections:** [22.1](../section-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-1), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Learning and derivation target:** Derive the walk's invariant structure or spectral relation.

**Implementation and evidence target:** Compare a circuit/tensor realization with an independent matrix.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-3"></span>

### 22.3 Search and marked vertices

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-3).

**Section level:** advanced. **Required earlier sections:** [22.2](../section-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-2), [16.2](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-2).

**Learning and derivation target:** Specify the promised search task and derive a tractable success example.

**Implementation and evidence target:** Compare time-dependent marked probability under matched graph/access assumptions.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-4"></span>

### 22.4 Hitting behavior and algorithmic resources

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-4).

**Section level:** advanced. **Required earlier sections:** [22.3](../section-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-3), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Learning and derivation target:** Explain which classical and quantum quantities are actually being compared.

**Implementation and evidence target:** Count initialization, walk steps, oracle use and readout.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-5"></span>

### 22.5 The polynomial method [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-5).

**Section level:** advanced. **Required earlier sections:** [14.4](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4), [15.1](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-1).

**Learning and derivation target:** Derive how oracle algorithms induce bounded-degree acceptance expressions in a representative setting.

**Implementation and evidence target:** Check a small acceptance polynomial independently.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-6"></span>

### 22.6 A representative query lower bound

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-6).

**Section level:** advanced. **Required earlier sections:** [22.5](../section-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-5), [16.1](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-1).

**Learning and derivation target:** State assumptions and work through a selected lower-bound argument.

**Implementation and evidence target:** Identify exactly which algorithm class/access model the result restricts.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-7"></span>

### 22.7 Choosing an algorithmic framework

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-7).

**Section level:** advanced. **Required earlier sections:** [20.7](../section-plans/03-algorithms.md#sec-qubitization-invariant-subspaces), [21.7](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-7), [22.4](../section-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-4), [22.6](../section-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-6).

**Learning and derivation target:** Relate walks, amplification and spectral transformations without claiming every method dominates.

**Implementation and evidence target:** Compare candidate approaches for the same small task.

<span id="sec-hamiltonian-complexity-boundary"></span>

### 22.8 Hamiltonian complexity and limits of optimization [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-hamiltonian-complexity-boundary).

**Section level:** advanced. **Required earlier sections:** [14.3](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-3), [19.1](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-1), [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3).

**Learning and derivation target:** Define a promise-gap ground-energy decision problem and quantum witness verification; state a scoped QMA-completeness result/proof roadmap without confusing query bounds or finite optimization evidence with general complexity claims.

**Implementation and evidence target:** Check a tiny verifier/energy instance and identify which conclusions concern a promise problem versus finding a favorable small variational solution.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-8"></span>
<span id="228-algorithm-design-laboratory"></span>

### 22.9 Algorithm-design laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-8).

**Section level:** advanced. **Required earlier sections:** [22.3](../section-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-3), [22.6](../section-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-6), [22.7](../section-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-7), [22.8](../section-plans/03-algorithms.md#sec-hamiltonian-complexity-boundary).

**Learning and derivation target:** Require a construction, proof obligation, access model and independent reference.

**Implementation and evidence target:** Diagnose an invalid speedup argument or a lower bound applied outside its model.
