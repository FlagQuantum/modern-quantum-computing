# Result and proof plan: Quantum Algorithms and Computational Resources

[Depth definitions](../proof-plan.md#proof-depth-contract) · [Source catalogue](../references/proof-sources.md) · [Volume plan](../volume-plan.md)

Authoring specifications only. No result/proof/API is certified by this plan. F/M/R have different scope; imported results are the exact prerequisite sections linked below.

## Chapter 14: Computational Models, Complexity, and Quantum Advantage

<span id="sec-computational-models-complexity-and-quantum-advantage-1"></span>

### 14.1 Problems, input length, and computational models

**Core result / role:** Uniform computation and input-size definitions.

**Assumptions and scope:** Finite encoded input; declared model.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Distinguish numerical value from bitlength and define the computational problem family.

**Imported earlier results:** [5.3](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-3), [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Exact source targets:** [NC:3.1.1](../references/proof-sources.md#source-nc-3-1-1): Section 3.1.1 Turing machines; [NC:3.2.1](../references/proof-sources.md#source-nc-3-2-1): Section 3.2.1 How to quantify computational resources.

**Independent evidence target:** Specify task size and required output for representative problems.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-computational-models-complexity-and-quantum-advantage-2"></span>

### 14.2 Reversible computation and uniform circuit families

**Core result / role:** Uniform reversible circuit simulation.

**Assumptions and scope:** Finite classical circuit with declared workspace.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Construct reversible embedding and uncomputation; track gate and ancillary overhead.

**Imported earlier results:** [5.4](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4), [14.1](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-1).

**Exact source targets:** [NC:3.1.2](../references/proof-sources.md#source-nc-3-1-2): Section 3.1.2 Circuits; [NC:3.2.5](../references/proof-sources.md#source-nc-3-2-5): Section 3.2.5 Energy and computation.

**Independent evidence target:** Audit a circuit generator's workspace and construction cost.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-computational-models-complexity-and-quantum-advantage-3"></span>

### 14.3 Complexity classes and bounded error

**Core result / role:** BQP definitions, bounded error and elementary containments.

**Assumptions and scope:** Uniform polynomial circuits; fixed promise gap.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Define the classes and prove only selected elementary containments; do not assert unproved separations.

**Imported earlier results:** [14.1](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-1), [14.2](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-2), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Exact source targets:** [COMPLEX:BQP](../references/proof-sources.md#source-complex-bqp): Polynomial-time quantum computations and BQP definitions.

**Independent evidence target:** Classify model assumptions and avoid claiming unproved class separations.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-computational-models-complexity-and-quantum-advantage-4"></span>

### 14.4 Oracle and data-access models

**Core result / role:** Oracle access is an additional assumption.

**Assumptions and scope:** Declared query unitary, data structure and preparation mechanism.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** State separate query and implementation costs; show an input-model counterexample.

**Imported earlier results:** [14.1](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-1), [5.3](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-3).

**Exact source targets:** [NC:6.1.1](../references/proof-sources.md#source-nc-6-1-1): Section 6.1.1 The oracle.

**Independent evidence target:** Compare costs when the same oracle is free versus synthesized.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-computational-models-complexity-and-quantum-advantage-5"></span>

### 14.5 Accuracy, repetition, and success probability

**Core result / role:** Independent repetition amplifies a bounded success probability.

**Assumptions and scope:** Independent runs with success strictly above one half.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive a selected majority/variance tail bound and its dependence on the gap.

**Imported earlier results:** [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8), [14.3](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-3).

**Exact source targets:** [CVX:7.4](../references/proof-sources.md#source-cvx-7-4): Section 7.4 Chebyshev and Chernoff bounds.

**Independent evidence target:** Count runs and requested precision in a small complete task.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-computational-models-complexity-and-quantum-advantage-6"></span>

### 14.6 Complete resource accounting

**Core result / role:** Compositional resource and error accounting.

**Assumptions and scope:** Specified cost units and subroutine failure bounds.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove additive deterministic cost and the union-bound error budget; include classical I/O.

**Imported earlier results:** [14.1](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-1), [14.4](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4), [14.5](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-5).

**Exact source targets:** [NC:3.2.1](../references/proof-sources.md#source-nc-3-2-1): Section 3.2.1 How to quantify computational resources.

**Independent evidence target:** Build an auditable cost table including preparation and readout.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-hybrid-interaction-map"></span>

### 14.7 Quantum-classical interaction patterns

**Core result / role:** Typed quantum-classical interaction contracts.

**Assumptions and scope:** Host/controller/device boundary and state lifetime.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Classify the eight editorial patterns; distinguish simulator amplitudes from measured records.

**Imported earlier results:** [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [14.1](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-1).

**Exact source targets:** [OQ3:2.4](../references/proof-sources.md#source-oq3-2-4): Section 2.4 Execution model; [ED:hybrid](../references/proof-sources.md#source-ed-hybrid): Eight composable patterns.

**Independent evidence target:** Draw a typed data/control flow for a small task; identify host, device, measurement records, feedback boundary and complete resource costs.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-computational-models-complexity-and-quantum-advantage-7"></span>

### 14.8 Classical baselines and advantage claims

**Core result / role:** Advantage claims require matched classical baselines.

**Assumptions and scope:** Same task and precision; dated implementations.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Specify the comparison and exclude toy simulation as asymptotic evidence.

**Imported earlier results:** [14.4](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Exact source targets:** [NC:3.2.1](../references/proof-sources.md#source-nc-3-2-1): Section 3.2.1 How to quantify computational resources; [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Diagnose omitted costs, unmatched error tolerances and inappropriate baselines.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-computational-models-complexity-and-quantum-advantage-8"></span>

### 14.9 Resource-audit laboratory

**Core result / role:** Resource-audit acceptance protocol.

**Assumptions and scope:** Complete input/output, runtime and uncertainty contract.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Account for preparation, arithmetic, shots, verification and all classical work.

**Imported earlier results:** [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6), [14.7](../section-plans/03-algorithms.md#sec-hybrid-interaction-map), [14.8](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-7).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Recompute conclusions when input access or target accuracy changes.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 15: Interference, Oracles, and Phase Kickback

<span id="sec-interference-oracles-and-phase-kickback-1"></span>

### 15.1 Boolean functions as reversible oracles

**Core result / role:** Coherent reversible Boolean-oracle action.

**Assumptions and scope:** Exact Boolean function and XOR output.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove unitarity by permutation and derive its action on superpositions.

**Imported earlier results:** [5.3](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-3), [5.4](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4), [14.4](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4).

**Exact source targets:** [NC:1.4.1](../references/proof-sources.md#source-nc-1-4-1): Section 1.4.1 Classical computations on a quantum computer.

**Independent evidence target:** Compare truth tables with permutation matrices.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-interference-oracles-and-phase-kickback-2"></span>

### 15.2 Phase kickback

**Core result / role:** Phase kickback identity.

**Assumptions and scope:** Target register in a known oracle eigenstate.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Calculate the eigenvalue phase on each control component.

**Imported earlier results:** [15.1](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-1), [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5).

**Exact source targets:** [NC:1.4.3](../references/proof-sources.md#source-nc-1-4-3): Section 1.4.3 Deutsch’s algorithm.

**Independent evidence target:** Check basis and superposition inputs against a dense reference.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-interference-oracles-and-phase-kickback-3"></span>

### 15.3 Deutsch's problem

**Core result / role:** Deutsch algorithm exact one-query discrimination.

**Assumptions and scope:** Promise of a one-bit constant or balanced function.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the final state for all four functions.

**Imported earlier results:** [15.2](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-2), [6.1](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-1).

**Exact source targets:** [NC:1.4.3](../references/proof-sources.md#source-nc-1-4-3): Section 1.4.3 Deutsch’s algorithm.

**Independent evidence target:** Enumerate the promised one-bit functions and count queries.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-interference-oracles-and-phase-kickback-4"></span>

### 15.4 The Deutsch-Jozsa promise

**Core result / role:** Deutsch-Jozsa promise algorithm.

**Assumptions and scope:** Exact constant/balanced promise; ideal oracle.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the zero-string amplitude and explain behavior outside the promise.

**Imported earlier results:** [15.2](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-2), [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1).

**Exact source targets:** [NC:1.4.4](../references/proof-sources.md#source-nc-1-4-4): Section 1.4.4 The Deutsch–Jozsa algorithm.

**Independent evidence target:** Verify small oracles and identify behavior outside the promise.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-interference-oracles-and-phase-kickback-5"></span>

### 15.5 Bernstein-Vazirani and hidden parity

**Core result / role:** Bernstein-Vazirani hidden-parity identity.

**Assumptions and scope:** Linear Boolean function with hidden binary vector.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Use character orthogonality to recover the vector in one quantum query.

**Imported earlier results:** [15.2](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-2), [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2).

**Exact source targets:** [P6:6.1](../references/proof-sources.md#source-p6-6-1): Section 6.1 Some Quantum Algorithms; Bernstein-Vazirani and Simon passages.

**Independent evidence target:** Generate all tiny parity instances with explicit oracle construction.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-simon-hidden-structure"></span>

### 15.6 Simon’s problem and hidden structure

**Core result / role:** Simon's sampling equations and recovery probability.

**Assumptions and scope:** Exact two-to-one XOR-mask promise; uniform oracle action.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive orthogonality equations over binary arithmetic; bound the chance of collecting enough independent equations.

**Imported earlier results:** [15.1](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-1), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [15.2](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-2).

**Exact source targets:** [P6:6.1](../references/proof-sources.md#source-p6-6-1): Section 6.1 Some Quantum Algorithms; Bernstein-Vazirani and Simon passages.

**Independent evidence target:** Check every tiny valid instance and rank-deficient sample set against an independently enumerated oracle; state the query model and promise.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-interference-oracles-and-phase-kickback-6"></span>

### 15.7 Oracle synthesis and uncomputation

**Core result / role:** Oracle synthesis preserves the promised phase action.

**Assumptions and scope:** Explicit reversible implementation and cleaned ancillas.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Track compute, kickback and uncompute; separate oracle query count from synthesis cost.

**Imported earlier results:** [15.1](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-1), [5.4](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4).

**Exact source targets:** [NC:3.2.5](../references/proof-sources.md#source-nc-3-2-5): Section 3.2.5 Energy and computation.

**Independent evidence target:** Account for workspace, gate count and restoration.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-interference-oracles-and-phase-kickback-7"></span>

### 15.8 Interference-algorithm laboratory

**Core result / role:** Oracle-algorithm acceptance protocol.

**Assumptions and scope:** All small promised instances and changed non-promised cases.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Check all output probabilities and the actual synthesized resource cost.

**Imported earlier results:** [15.4](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-4), [15.5](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-5), [15.6](../section-plans/03-algorithms.md#sec-simon-hidden-structure), [15.7](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-6).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Compare gate-level, matrix and analytic outputs and diagnose a wrong phase convention.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 16: Grover Search, Amplitude Amplification, and Estimation

<span id="sec-grover-search-amplitude-amplification-and-estimation-1"></span>

### 16.1 Search promises and marked subspaces

**Core result / role:** Search reflection on marked subspaces.

**Assumptions and scope:** Explicit Boolean predicate and marked fraction.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Define the two invariant components and the oracle reflection.

**Imported earlier results:** [14.4](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4), [15.1](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-1).

**Exact source targets:** [NC:6.1.1](../references/proof-sources.md#source-nc-6-1-1): Section 6.1.1 The oracle.

**Independent evidence target:** Check explicit small marked sets and access assumptions.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-grover-search-amplitude-amplification-and-estimation-2"></span>

### 16.2 Reflections and the invariant plane

**Core result / role:** Grover iteration is a plane rotation.

**Assumptions and scope:** Nontrivial marked and unmarked subspaces.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Multiply the two reflection matrices and derive the signed rotation angle.

**Imported earlier results:** [16.1](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-1), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Exact source targets:** [NC:6.1.3](../references/proof-sources.md#source-nc-6-1-3): Section 6.1.3 Geometric visualization.

**Independent evidence target:** Compare its matrix with the full-register construction.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-grover-search-amplitude-amplification-and-estimation-3"></span>

### 16.3 Success probability and stopping

**Core result / role:** Grover success curve and overshoot.

**Assumptions and scope:** Known marked fraction and integer iteration count.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove the sinusoidal probability and bound a nearest optimal stopping choice.

**Imported earlier results:** [16.2](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-2).

**Exact source targets:** [NC:6.1.4](../references/proof-sources.md#source-nc-6-1-4): Section 6.1.4 Performance.

**Independent evidence target:** Sweep iterations and compare every result with the formula.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-grover-search-amplitude-amplification-and-estimation-4"></span>

### 16.4 General amplitude amplification

**Core result / role:** General amplitude amplification.

**Assumptions and scope:** Known preparation unitary and its inverse; projective good subspace.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the invariant plane for the prepared state and count both preparation/inverse calls.

**Imported earlier results:** [16.2](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-2), [5.4](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4).

**Exact source targets:** [AMP:2](../references/proof-sources.md#source-amp-2): Section 2 Quantum amplitude amplification.

**Independent evidence target:** Verify success amplification and include preparation/uncomputation cost.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-grover-search-amplitude-amplification-and-estimation-5"></span>

### 16.5 Unknown success probabilities [Advanced]

**Core result / role:** Unknown-success amplification schedule.

**Assumptions and scope:** One declared randomized schedule and oracle cost model.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Derive its success conditional on a range; state the expected-query theorem and outline the geometric schedule proof.

**Imported earlier results:** [16.3](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-3), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Exact source targets:** [AMP:2](../references/proof-sources.md#source-amp-2): Section 2 Quantum amplitude amplification.

**Independent evidence target:** Compare success and expected query use over several declared instances.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local mathematical bridge to supply:** Randomized schedules, expected query cost and geometric-series bounds.

**Explicitly deferred proof ingredients:** Full schedule-specific expected-query proof for unknown amplitude; Brassard et al. Section 2.

<span id="sec-amplitude-estimation-phase-free"></span>

### 16.6 Amplitude estimation without phase estimation [Advanced]

**Core result / role:** Phase-free amplitude likelihood.

**Assumptions and scope:** Independent Bernoulli batches; chosen amplification depths; identifiable amplitude interval.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive likelihood from the Grover curve; expose aliases and boundaries; make no universal finite-sample optimality claim.

**Imported earlier results:** [16.3](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-3), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Exact source targets:** [AE:3.1](../references/proof-sources.md#source-ae-3-1): Section 3.1 The algorithm; [AE:3.2](../references/proof-sources.md#source-ae-3-2): Section 3.2 Statistics; Cramer-Rao bound and Fisher information.

**Independent evidence target:** Compare amplified Bernoulli data and an explicit one-dimensional likelihood grid with exact probabilities; account for total oracle calls and uncertainty.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-grover-search-amplitude-amplification-and-estimation-7"></span>

### 16.7 Classical estimation, uncertainty, and query comparisons [Advanced]

**Core result / role:** Matched estimation query comparison.

**Assumptions and scope:** Same additive error/confidence and access model.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Compare a proved classical bound with the selected phase-free model's stated guarantee; separate asymptotic variance from coverage.

**Imported earlier results:** [16.4](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-4), [16.6](../section-plans/03-algorithms.md#sec-amplitude-estimation-phase-free), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Exact source targets:** [AE:3.2](../references/proof-sources.md#source-ae-3-2): Section 3.2 Statistics; Cramer-Rao bound and Fisher information; [CVX:7.4](../references/proof-sources.md#source-cvx-7-4): Section 7.4 Chebyshev and Chernoff bounds.

**Independent evidence target:** Compare like-for-like access models and total queries without assuming every estimator is advantageous.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-grover-search-amplitude-amplification-and-estimation-8"></span>

### 16.8 Search-and-estimation laboratory

**Core result / role:** Search-and-estimation acceptance protocol.

**Assumptions and scope:** Full oracle construction and independent probabilities.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Verify the curve, ambiguity cases, uncertainty and total oracle work.

**Imported earlier results:** [16.3](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-3), [16.4](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-4), [16.6](../section-plans/03-algorithms.md#sec-amplitude-estimation-phase-free), [16.7](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-7).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Audit a complete experiment and diagnose incorrect reflection or success definitions.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 17: Fourier Transforms and Quantum Phase Estimation

<span id="sec-fourier-transforms-and-quantum-phase-estimation-1"></span>

### 17.1 The discrete Fourier transform

**Core result / role:** Discrete Fourier transform orthogonality.

**Assumptions and scope:** Finite cyclic index set; declared sign convention.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Sum the geometric series and prove unitarity.

**Imported earlier results:** [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3), [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2).

**Exact source targets:** [NC:5.1](../references/proof-sources.md#source-nc-5-1): Section 5.1 The quantum Fourier transform.

**Independent evidence target:** Construct the dense transform and check unitarity.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-2"></span>

### 17.2 Factorizing the QFT

**Core result / role:** QFT product factorization and circuit.

**Assumptions and scope:** Binary input and fixed output significance.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Factor the phase by input bits and derive each controlled rotation.

**Imported earlier results:** [17.1](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-1), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Exact source targets:** [NC:5.1](../references/proof-sources.md#source-nc-5-1): Section 5.1 The quantum Fourier transform.

**Independent evidence target:** Compare every small basis input with the Fourier matrix.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-3"></span>

### 17.3 Inverse transforms and qubit reversal

**Core result / role:** Inverse QFT and output reversal.

**Assumptions and scope:** Same Fourier sign and basis order.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Reverse/invert all gates and derive the final permutation.

**Imported earlier results:** [17.2](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-2), [4.5](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-5).

**Exact source targets:** [NC:5.1](../references/proof-sources.md#source-nc-5-1): Section 5.1 The quantum Fourier transform.

**Independent evidence target:** Test explicit permutations and a round trip.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-4"></span>

### 17.4 Approximate QFT

**Core result / role:** Approximate QFT telescoping error bound.

**Assumptions and scope:** Omitted rotations bounded in operator norm.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Bound each omission and telescope the product; count retained gates.

**Imported earlier results:** [17.2](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-2), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Exact source targets:** [NC:5.2.1](../references/proof-sources.md#source-nc-5-2-1): Section 5.2.1 Performance and requirements.

**Independent evidence target:** Compare operator/state errors with the declared approximation criterion.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-5"></span>

### 17.5 Controlled powers and phase kickback

**Core result / role:** Controlled powers imprint eigenphases.

**Assumptions and scope:** Input eigenvector; controlled unitary powers available at stated cost.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the phase register and distinguish a query power from its compiled gate cost.

**Imported earlier results:** [15.2](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-2), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Exact source targets:** [NC:5.2](../references/proof-sources.md#source-nc-5-2): Section 5.2 Phase estimation.

**Independent evidence target:** Verify powers of a known small unitary and count their construction cost.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-6"></span>

### 17.6 Exact-grid phase estimation

**Core result / role:** Exact-grid QPE correctness.

**Assumptions and scope:** Eigenphase exactly representable in the chosen register.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Apply Fourier orthogonality and prove the deterministic readout.

**Imported earlier results:** [17.3](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-3), [17.5](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-5).

**Exact source targets:** [NC:5.2](../references/proof-sources.md#source-nc-5-2): Section 5.2 Phase estimation.

**Independent evidence target:** Check representable phases and readout ordering.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-7"></span>

### 17.7 Off-grid phases and superposed eigenstates

**Core result / role:** Off-grid QPE distribution and eigenstate overlap.

**Assumptions and scope:** Arbitrary eigenphase; normalized superposition of eigenvectors.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the geometric-series distribution and conditional eigenstate weights; bound selected tail probability.

**Imported earlier results:** [17.6](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-6), [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Exact source targets:** [NC:5.2.1](../references/proof-sources.md#source-nc-5-2-1): Section 5.2.1 Performance and requirements.

**Independent evidence target:** Compare the complete distribution with an independent geometric-series calculation.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-grover-search-amplitude-amplification-and-estimation-6"></span>

### 17.8 Phase-estimation-based amplitude estimation [Advanced]

**Core result / role:** QPE-based amplitude estimation.

**Assumptions and scope:** Amplification unitary; controlled powers; chosen precision/confidence.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive Grover eigenphases, phase-to-amplitude conversion and a scoped finite-register error bound.

**Imported earlier results:** [16.2](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-2), [16.4](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-4), [17.7](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-7).

**Exact source targets:** [AMP:4](../references/proof-sources.md#source-amp-4): Section 4 Quantum amplitude estimation.

**Independent evidence target:** Compare tiny estimation distributions after completing the relevant Chapter 17 sections.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-fourier-transforms-and-quantum-phase-estimation-8"></span>

### 17.9 Precision, success, and algorithmic cost

**Core result / role:** QPE accuracy and state-preparation cost.

**Assumptions and scope:** Explicit overlap lower bound and unitary-power implementation.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Combine spectral overlap, repetitions, precision and evolution cost; QPE alone does not prepare a ground state.

**Imported earlier results:** [17.4](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-4), [17.7](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-7), [17.8](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-6), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Exact source targets:** [NC:5.2.1](../references/proof-sources.md#source-nc-5-2-1): Section 5.2.1 Performance and requirements; [P6:6.8.2](../references/proof-sources.md#source-p6-6-8-2): Section 6.8.2 Estimating energy eigenvalues and preparing energy eigenstates.

**Independent evidence target:** Audit a phase-estimation experiment including synthesis and state preparation.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 18: Period Finding, Factoring, and Algorithmic Arithmetic

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-1"></span>

### 18.1 From factoring to order finding

**Core result / role:** Randomized reduction of factoring to order finding.

**Assumptions and scope:** Odd composite outside declared easy cases; modular coprime samples.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove the useful gcd step and state the number-theoretic success conditions.

**Imported earlier results:** [14.4](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4).

**Exact source targets:** [NC:5.3.2](../references/proof-sources.md#source-nc-5-3-2): Section 5.3.2 Application: factoring; [NC:A4.3](../references/proof-sources.md#source-nc-a4-3): Appendix 4, A4.3 Reduction of factoring to order-finding.

**Independent evidence target:** Check both successful and exceptional classical instances.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-2"></span>

### 18.2 Reversible modular arithmetic

**Core result / role:** Reversible modular arithmetic correctness.

**Assumptions and scope:** Fixed modulus, valid registers and ancillary conventions.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive selected adder/multiplier basis actions and clean workspace.

**Imported earlier results:** [5.3](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-3), [5.4](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4), [18.1](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-1).

**Exact source targets:** [NC:5.3.1](../references/proof-sources.md#source-nc-5-3-1): Section 5.3.1 Application: order-ﬁnding.

**Independent evidence target:** Compare truth tables and complete reversible operators.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local mathematical bridge to supply:** Define modular arithmetic on the valid subspace and a reversible extension on unused computational-basis states; prove the full map is a permutation..

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-3"></span>

### 18.3 Coherent modular exponentiation

**Core result / role:** Repeated-squaring modular exponentiation.

**Assumptions and scope:** Known classical base/modulus and controlled multiplication.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove the binary exponentiation identity and count circuit calls.

**Imported earlier results:** [18.2](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-2), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Exact source targets:** [NC:5.3.1](../references/proof-sources.md#source-nc-5-3-1): Section 5.3.1 Application: order-ﬁnding.

**Independent evidence target:** Verify the function on all small inputs, including a superposition.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-4"></span>

### 18.4 Period information from phase estimation

**Core result / role:** Order information from eigenphases.

**Assumptions and scope:** Cyclic modular-multiplication orbit and stated input overlap.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Construct eigenvectors and show the sampled phase denominator divides the order.

**Imported earlier results:** [17.7](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-7), [18.3](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-3).

**Exact source targets:** [NC:5.3.1](../references/proof-sources.md#source-nc-5-3-1): Section 5.3.1 Application: order-ﬁnding.

**Independent evidence target:** Compare circuit outputs with an independent spectral/distribution reference.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-5"></span>

### 18.5 Continued fractions and candidate verification

**Core result / role:** Continued-fraction rational recovery.

**Assumptions and scope:** Explicit phase-approximation inequality and denominator bound.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove the Legendre continued-fraction recovery criterion using the locally taught recurrence/determinant bridge; verify every candidate order classically.

**Imported earlier results:** [18.1](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-1), [18.4](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-4).

**Exact source targets:** [NC:A4.4](../references/proof-sources.md#source-nc-a4-4): Appendix 4, A4.4 Continued fractions.

**Independent evidence target:** Test ambiguous fractions and reject incorrect candidates.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local mathematical bridge to supply:** Teach Euclidean division, convergent numerator/denominator recurrences and the determinant identity; prove the declared Legendre recovery criterion under its exact error/denominator condition..

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-6"></span>

### 18.6 Factoring end to end

**Core result / role:** Factoring 15 with base-2 order finding and verified classical reduction.

**Assumptions and scope:** Declared sampling model and verified candidate order.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Combine the arithmetic reduction, phase accuracy and candidate verification probabilities.

**Imported earlier results:** [18.4](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-4), [18.5](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-5).

**Exact source targets:** [NC:5.3.2](../references/proof-sources.md#source-nc-5-3-2): Section 5.3.2 Application: factoring.

**Independent evidence target:** Factor tiny integers without choosing circuits that assume the answer.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-abelian-hidden-subgroups"></span>

### 18.7 Discrete logarithms and Abelian hidden subgroups [Advanced]

**Core result / role:** Abelian hidden-subgroup sampling and discrete logarithms.

**Assumptions and scope:** Specified finite Abelian group; efficient group operations/QFT.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Derive the character constraint and discrete logarithm of 5 to base 3 in the multiplicative group modulo 17; roadmap the general Abelian theorem.

**Imported earlier results:** [17.1](../section-plans/03-algorithms.md#sec-fourier-transforms-and-quantum-phase-estimation-1), [15.6](../section-plans/03-algorithms.md#sec-simon-hidden-structure), [18.4](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-4).

**Exact source targets:** [NC:5.4.2](../references/proof-sources.md#source-nc-5-4-2): Section 5.4.2 Discrete logarithms; [NC:5.4.3](../references/proof-sources.md#source-nc-5-4-3): Section 5.4.3 The hidden subgroup problem.

**Independent evidence target:** Enumerate a tiny group, compare Fourier-sampling distributions and validate classical candidate recovery under the declared access model.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local mathematical bridge to supply:** Finite cyclic groups, characters and the implemented group oracle.

**Explicitly deferred proof ingredients:** General finite-Abelian decomposition and character-sampling theorem beyond the worked modulo-17 instance; NC 5.4.3.

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-7"></span>

### 18.8 Arithmetic, synthesis, and resource growth

**Core result / role:** Arithmetic precision and synthesis cost compose.

**Assumptions and scope:** Chosen reversible arithmetic and approximation basis.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Count the selected construction including ancillas, controlled powers and error budget.

**Imported earlier results:** [18.2](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-2), [18.3](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-3), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Exact source targets:** [NC:5.3.1](../references/proof-sources.md#source-nc-5-3-1): Section 5.3.1 Application: order-ﬁnding; [NC:A3](../references/proof-sources.md#source-nc-a3): Appendix 3: The Solovay-Kitaev theorem.

**Independent evidence target:** Separate measured tiny-circuit costs from asymptotic estimates.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-period-finding-factoring-and-algorithmic-arithmetic-8"></span>

### 18.9 A reproducible factoring laboratory

**Core result / role:** Factoring acceptance protocol.

**Assumptions and scope:** Nontrivial compiled instance plus honest scaling record.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Verify factors and all oracle/arithmetic costs without a practical speedup claim.

**Imported earlier results:** [18.6](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-6), [18.8](../section-plans/03-algorithms.md#sec-period-finding-factoring-and-algorithmic-arithmetic-7).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Diagnose a precompiled demonstration that hides the difficult computation.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 19: Hamiltonian Simulation and Error Bounds

<span id="sec-hamiltonian-simulation-and-error-bounds-1"></span>

### 19.1 Hamiltonians, evolution, and access models

**Core result / role:** Hamiltonian evolution is unitary.

**Assumptions and scope:** Finite Hermitian Hamiltonian; specified access and units.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive spectral evolution and state what an evolution oracle supplies.

**Imported earlier results:** [2.6](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-6), [3.4](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-4).

**Exact source targets:** [NC:4.7](../references/proof-sources.md#source-nc-4-7): Section 4.7 Simulation of quantum systems.

**Independent evidence target:** Compare a Pauli-list input with an abstract sparse-access model.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-hamiltonian-simulation-and-error-bounds-2"></span>

### 19.2 Commuting terms and exact factorizations

**Core result / role:** Exponential factorization for commuting operators.

**Assumptions and scope:** Bounded finite matrices that commute.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Multiply convergent power series and show a noncommuting counterexample.

**Imported earlier results:** [19.1](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-1).

**Exact source targets:** [NC:4.7.1](../references/proof-sources.md#source-nc-4-7-1): Section 4.7.1 Simulation in action.

**Independent evidence target:** Check commuting and noncommuting counterexamples.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-hamiltonian-simulation-and-error-bounds-3"></span>

### 19.3 First-order product formulas

**Core result / role:** First-order product-formula error.

**Assumptions and scope:** Finite bounded Hermitian terms and fixed evolution time.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive a local commutator bound and telescope over steps.

**Imported earlier results:** [19.2](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-2), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Exact source targets:** [NC:4.7.2](../references/proof-sources.md#source-nc-4-7-2): Section 4.7.2 The quantum simulation algorithm.

**Independent evidence target:** Compare simulated evolution with a dense exponential as step size changes.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-hamiltonian-simulation-and-error-bounds-4"></span>

### 19.4 Symmetric and higher-order constructions

**Core result / role:** Symmetric splitting cancellation and global error.

**Assumptions and scope:** Bounded time-independent terms; symmetric construction.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Show cancellation of the selected leading terms; prove the stated finite-order bound, defer arbitrary-order recursion.

**Imported earlier results:** [19.3](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-3).

**Exact source targets:** [NC:4.7.2](../references/proof-sources.md#source-nc-4-7-2): Section 4.7.2 The quantum simulation algorithm; [CHEB:comparison](../references/proof-sources.md#source-cheb-comparison): Introduction and query-complexity comparison.

**Independent evidence target:** Check observed error scaling against explicit assumptions.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-hamiltonian-simulation-and-error-bounds-5"></span>

### 19.5 Pauli-term exponentiation

**Core result / role:** Pauli-string exponential by basis change and parity.

**Assumptions and scope:** Hermitian Pauli product with square identity.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Conjugate to Z parity, derive the rotation and uncompute all parity work.

**Imported earlier results:** [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5), [5.4](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4), [19.1](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-1).

**Exact source targets:** [NC:4.7.3](../references/proof-sources.md#source-nc-4-7-3): Section 4.7.3 An illustrative example.

**Independent evidence target:** Compare full small unitaries with generator exponentials.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-hamiltonian-simulation-and-error-bounds-6"></span>

### 19.6 State, observable, and operator error

**Core result / role:** Operator error bounds state and observable error.

**Assumptions and scope:** Normalized input; bounded observable; chosen norm.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove the norm inequalities and distinguish global-phase-insensitive metrics.

**Imported earlier results:** [19.3](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-3), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Exact source targets:** [TQI:1.1.3](../references/proof-sources.md#source-tqi-1-1-3): Section 1.1.3 Operator decompositions and norms; [NC:9.2.1](../references/proof-sources.md#source-nc-9-2-1): Section 9.2.1 Trace distance.

**Independent evidence target:** Show that an accurate observable can coexist with a larger full-state error.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-hamiltonian-simulation-and-error-bounds-7"></span>

### 19.7 Alternative simulation paradigms [Advanced]

**Core result / role:** Selected LCU/qubitization complexity contracts.

**Assumptions and scope:** Explicit block-access, normalization and error promise.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Compare theorem statements with product formulas; defer detailed construction to 20–21.

**Imported earlier results:** [19.1](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-1), [14.4](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4).

**Exact source targets:** [CHEB:theorem](../references/proof-sources.md#source-cheb-theorem): Theorem 1 and Hamiltonian-access assumptions; [QUB:5](../references/proof-sources.md#source-qub-5): Section 5 Application to Hamiltonian Simulation.

**Independent evidence target:** Map an example's requirements to Chapters 20–21 without assuming their results.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local mathematical bridge to supply:** Sparse/LCU/block oracle models and gate-versus-query complexity.

**Explicitly deferred proof ingredients:** Full simulation construction and optimality/lower-bound details; Berry et al. Theorem 1 and Low-Chuang Section 5.

<span id="sec-hamiltonian-adiabatic-model"></span>

### 19.8 Adiabatic computation and gap assumptions [Advanced]

**Core result / role:** Adiabatic approximation with a spectral gap.

**Assumptions and scope:** Smooth path; nonzero gap; explicit schedule/error theorem.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Derive one two-level example; state the selected theorem's conditions and defer its analytic proof.

**Imported earlier results:** [19.1](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-1), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Exact source targets:** [ADI:adiabatic](../references/proof-sources.md#source-adi-adiabatic): Proposed adiabatic algorithm and spectral-gap discussion; [ADBOUND:theorem](../references/proof-sources.md#source-adbound-theorem): Section II: Theorems 1-3 and explicit regularity/gap assumptions; [ADBOUND:theorem](../references/proof-sources.md#source-adbound-theorem): Section II: Theorems 1-3 and explicit regularity/gap assumptions; [ADBOUND:theorem](../references/proof-sources.md#source-adbound-theorem): Section II: Theorems 1-3 and explicit regularity/gap assumptions.

**Independent evidence target:** Compare a tiny gapped interpolation with exact time evolution and diagnose a schedule that violates the stated error conditions.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local mathematical bridge to supply:** Smooth operator path, derivatives, spectral projector and gap.

**Explicitly deferred proof ingredients:** Resolvent/adiabatic integration estimates for Jansen-Ruskai-Seiler Theorem 3; the elementary two-level example is proved locally.

<span id="sec-hamiltonian-simulation-and-error-bounds-8"></span>

### 19.9 Dynamics laboratory and resource budget

**Core result / role:** Dynamics acceptance protocol.

**Assumptions and scope:** Independent matrix exponential and timestep refinement.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Check state/operator/observable error separately and report total gates.

**Imported earlier results:** [19.3](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-3), [19.4](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-4), [19.5](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-5), [19.6](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-6), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Report gate count, step count, synthesis assumptions and a verified finite-system error.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 20: Block Encodings and Quantum Linear Algebra

<span id="sec-block-encodings-and-quantum-linear-algebra-1"></span>

### 20.1 Why matrix access must be specified

**Core result / role:** Matrix access and output define the linear-algebra problem.

**Assumptions and scope:** Specified encoding, normalization and requested observation.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Distinguish reading all solution entries from preparing a normalized solution state.

**Imported earlier results:** [14.4](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Exact source targets:** [QSVT:4.1](../references/proof-sources.md#source-qsvt-4-1): Section 4.1 Block-encoding.

**Independent evidence target:** Audit a matrix problem with explicit data-loading and readout costs.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-block-encodings-and-quantum-linear-algebra-2"></span>

### 20.2 Block-encoding definitions and ancillas

**Core result / role:** Approximate block-encoding definition.

**Assumptions and scope:** Explicit signal projector, scale, ancillas and operator error.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Derive the encoded matrix element and distinguish the block from the full unitary.

**Imported earlier results:** [20.1](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-1), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Exact source targets:** [QSVT:4.1](../references/proof-sources.md#source-qsvt-4-1): Section 4.1 Block-encoding.

**Independent evidence target:** Construct a tiny block encoding and extract its encoded block independently.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-block-encodings-and-quantum-linear-algebra-3"></span>

### 20.3 Linear combinations of unitaries

**Core result / role:** PREPARE/SELECT realizes a linear combination.

**Assumptions and scope:** Known coefficient normalization and controlled unitary terms.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Expand the ancillary sandwich and derive the encoded weighted sum.

**Imported earlier results:** [20.2](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-2), [5.4](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4).

**Exact source targets:** [QSVT:4.2](../references/proof-sources.md#source-qsvt-4-2): Section 4.2 Constructing block-encodings.

**Independent evidence target:** Verify normalization and success amplitudes for a two-term example.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-block-encodings-and-quantum-linear-algebra-4"></span>

### 20.4 Composing encoded operations

**Core result / role:** Block-encoding sum/product and error propagation.

**Assumptions and scope:** Compatible signal spaces and normalization factors.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the selected circuits and bound cross/error terms explicitly.

**Imported earlier results:** [20.2](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-2), [20.3](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-3).

**Exact source targets:** [QSVT:4.3](../references/proof-sources.md#source-qsvt-4-3): Section 4.3 Addition and subtraction; [QSVT:4.4](../references/proof-sources.md#source-qsvt-4-4): Section 4.4 Multiplication.

**Independent evidence target:** Compare encoded blocks with ordinary matrix arithmetic.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-block-encodings-and-quantum-linear-algebra-5"></span>

### 20.5 Postselection and amplification

**Core result / role:** Postselection probability and amplification cost.

**Assumptions and scope:** Specified encoded action on a normalized input.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Normalize the successful branch and derive its input-dependent success probability.

**Imported earlier results:** [20.3](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-3), [16.4](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-4).

**Exact source targets:** [AMP:2](../references/proof-sources.md#source-amp-2): Section 2 Quantum amplitude amplification; [QSVT:4.1](../references/proof-sources.md#source-qsvt-4-1): Section 4.1 Block-encoding.

**Independent evidence target:** Compare accepted branches with an independent projector calculation.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-block-encodings-and-quantum-linear-algebra-6"></span>

### 20.6 Quantum linear systems and conditioning

**Core result / role:** Conditioning controls inverse-state preparation.

**Assumptions and scope:** Known spectral promise; normalized input; explicitly costly tiny inverse reference.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive success and condition-number dependence; do not call an explicitly constructed inverse efficient.

**Imported earlier results:** [20.2](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-2), [20.5](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-5), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Exact source targets:** [QSVT:3.7](../references/proof-sources.md#source-qsvt-3-7): Section 3.7 Direct implementation of the Moore-Penrose pseudoinverse.

**Independent evidence target:** Solve a tiny system while reporting normalization, state error and readout requirements. Report the construction cost rather than treating the desired inverse block as free input.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-qubitization-invariant-subspaces"></span>

### 20.7 Qubitization and invariant subspaces [Advanced]

**Core result / role:** Hermitian qubitization conditions and invariant-subspace construction (Low-Chuang Theorems 2-3).

**Assumptions and scope:** Normalized Hermitian signal block and valid reflection/oracle construction.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove the invariant two-dimensional action and eigenvalue-angle relation; state the exact construction's extra assumptions.

**Imported earlier results:** [20.2](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-2), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Exact source targets:** [QUB:3](../references/proof-sources.md#source-qub-3): Section 3 Qubitization in a Quantum Signal Processor; Theorems 2-3; [QSVT:3.2](../references/proof-sources.md#source-qsvt-3-2): Section 3.2 Singular value transformation by qubitization; Lemma 14, Theorem 17 and Corollary 18.

**Independent evidence target:** Compare the encoded block, walk spectrum and invariant-subspace calculation with independent small matrices before QSP/QSVT applications.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local mathematical bridge to supply:** Treat eigenvalues at plus/minus one separately when the nominal two-dimensional orthogonal component has zero norm..

<span id="sec-block-encodings-and-quantum-linear-algebra-7"></span>

### 20.8 Spectral functions and application contracts

**Core result / role:** Spectral-function application contract.

**Assumptions and scope:** Specified interval, parity, accuracy and success norm.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Translate a requested matrix function into admissible scalar targets; defer efficient implementation to 21.

**Imported earlier results:** [20.6](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-6), [20.7](../section-plans/03-algorithms.md#sec-qubitization-invariant-subspaces).

**Exact source targets:** [QSVT:5.2](../references/proof-sources.md#source-qsvt-5-2): Section 5.2 Bounded polynomial approximations of piecewise smooth functions.

**Independent evidence target:** Build an acceptance specification for the QSVT chapter.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-block-encodings-and-quantum-linear-algebra-8"></span>

### 20.9 Linear-algebra laboratory

**Core result / role:** Block-encoding acceptance protocol.

**Assumptions and scope:** Small independent encoded matrix and postselection record.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Check scale, ancillas, error, preparation and complete output cost.

**Imported earlier results:** [20.3](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-3), [20.5](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-5), [20.6](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-6), [20.8](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-7).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Compare with an independent classical solve and identify unrealistic access assumptions.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 21: Quantum Signal Processing and Singular Value Transformation

<span id="sec-quantum-signal-processing-and-singular-value-transformation-1"></span>

### 21.1 A scalar signal encoded in SU(2)

**Core result / role:** SU(2) signal matrix and scalar parameter.

**Assumptions and scope:** Real signal in the declared interval; fixed phase convention.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the signal rotation and identify its polynomial entries.

**Imported earlier results:** [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5), [20.2](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-2).

**Exact source targets:** [QSVT:3.1](../references/proof-sources.md#source-qsvt-3-1): Section 3.1 Parametrized SU(2) unitaries induced by Pauli rotations; Theorems 3-5 (admissibility/completion).

**Independent evidence target:** Verify the matrix identity at interior and boundary signal values.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-2"></span>

### 21.2 Phase-controlled polynomial sequences

**Core result / role:** QSP sequence parity and degree.

**Assumptions and scope:** Specified signal and phase sequence.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Use induction on sequence length to derive polynomial degree, parity and normalization identities.

**Imported earlier results:** [21.1](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-1).

**Exact source targets:** [QSVT:3.1](../references/proof-sources.md#source-qsvt-3-1): Section 3.1 Parametrized SU(2) unitaries induced by Pauli rotations; Theorems 3-5 (admissibility/completion).

**Independent evidence target:** Compare matrix products with independently expanded polynomials.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-3"></span>

### 21.3 Admissibility and approximation

**Core result / role:** QSP admissibility/completion conditions (Gilyén et al. Theorems 3-5).

**Assumptions and scope:** Bounded polynomial pair satisfying the exact parity/completion conditions.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Prove necessity and a low-degree constructive case; roadmap the general completion/factorization proof.

**Imported earlier results:** [21.2](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-2), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Exact source targets:** [QSVT:3.1](../references/proof-sources.md#source-qsvt-3-1): Section 3.1 Parametrized SU(2) unitaries induced by Pauli rotations; Theorems 3-5 (admissibility/completion).

**Independent evidence target:** Test admissible targets and explain a deliberately impossible target.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local mathematical bridge to supply:** Polynomial degree, parity, boundedness and complex completion.

**Explicitly deferred proof ingredients:** General completion/factorization sufficiency of Gilyén et al. Theorems 3–5; prove necessity and the selected low-degree case locally.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-4"></span>

### 21.4 Phase synthesis and numerical stability

**Core result / role:** Phase-synthesis correctness versus numerical conditioning.

**Assumptions and scope:** Chosen finite polynomial and synthesis routine.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Reconstruct the polynomial from phases; analyze residual sensitivity without promising globally stable synthesis.

**Imported earlier results:** [21.3](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-3), [2.8](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-8).

**Exact source targets:** [QSVT:3.1](../references/proof-sources.md#source-qsvt-3-1): Section 3.1 Parametrized SU(2) unitaries induced by Pauli rotations; Theorems 3-5 (admissibility/completion).

**Independent evidence target:** Check residuals and sensitivity rather than assuming a returned phase list is correct.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-5"></span>

### 21.5 From eigenvalues to singular values

**Core result / role:** Alternating projected unitaries transform singular values.

**Assumptions and scope:** Rectangular block encoding; matched projectors and parity.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Apply SVD, identify invariant subspaces and lift the scalar action.

**Imported earlier results:** [20.7](../section-plans/03-algorithms.md#sec-qubitization-invariant-subspaces), [21.2](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-2), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Exact source targets:** [QSVT:3.2](../references/proof-sources.md#source-qsvt-3-2): Section 3.2 Singular value transformation by qubitization; Lemma 14, Theorem 17 and Corollary 18.

**Independent evidence target:** Compare a small non-Hermitian example through its SVD.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-6"></span>

### 21.6 A precise QSVT theorem [Advanced]

**Core result / role:** QSVT by alternating phase modulation (Gilyén et al. Theorem 17 and Corollary 18).

**Assumptions and scope:** Admissible bounded polynomial; exact parity/projector/error hypotheses.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** State the selected theorem and all oracle counts; connect proved invariant blocks to deferred polynomial existence/robustness lemmas.

**Imported earlier results:** [21.3](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-3), [21.5](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-5).

**Exact source targets:** [QSVT:3.2](../references/proof-sources.md#source-qsvt-3-2): Section 3.2 Singular value transformation by qubitization; Lemma 14, Theorem 17 and Corollary 18; [QSVT:3.3](../references/proof-sources.md#source-qsvt-3-3): Section 3.3 Robustness of singular value transformation.

**Independent evidence target:** Verify selected finite cases while preserving the distinction between theorem and numerical evidence.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local mathematical bridge to supply:** Projector pairs, singular subspaces and admissible phase sequences.

**Explicitly deferred proof ingredients:** General scalar polynomial-existence and robustness lemmas used by Theorem 17/Corollary 18; invariant-subspace lifting is derived locally.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-7"></span>

### 21.7 Applications: filtering, inversion, and evolution

**Core result / role:** Filtering, inversion and evolution applications.

**Assumptions and scope:** Declared spectral gap/condition bound and scalar approximation.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Derive the gapped inverse/pseudoinverse application conditional on Theorem 17 and its polynomial-approximation lemma; give spectral/access/error contracts for filtering and evolution.

**Imported earlier results:** [21.6](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-6), [20.8](../section-plans/03-algorithms.md#sec-block-encodings-and-quantum-linear-algebra-7), [19.1](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-1).

**Exact source targets:** [QSVT:3.7](../references/proof-sources.md#source-qsvt-3-7): Section 3.7 Direct implementation of the Moore-Penrose pseudoinverse; [QSVT:5.1](../references/proof-sources.md#source-qsvt-5-1): Section 5.1 Optimal Hamiltonian simulation; [QSVT:5.2](../references/proof-sources.md#source-qsvt-5-2): Section 5.2 Bounded polynomial approximations of piecewise smooth functions.

**Independent evidence target:** Compare transformed values with a classical matrix-function reference.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local mathematical bridge to supply:** Spectral promises, normalization, polynomial error and postselection probability.

**Explicitly deferred proof ingredients:** The inverse-function polynomial approximation in Lemma 40/Theorem 41 and advanced approximation constructions; the conditional application calculation is local.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-8"></span>

### 21.8 Precision and complete complexity

**Core result / role:** Polynomial approximation and implementation errors compose.

**Assumptions and scope:** Specified approximation interval and noisy block oracle.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Use operator bounds and sequence telescoping; include amplification and input/output work.

**Imported earlier results:** [21.4](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-4), [21.7](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-7), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Exact source targets:** [QSVT:3.3](../references/proof-sources.md#source-qsvt-3-3): Section 3.3 Robustness of singular value transformation.

**Independent evidence target:** Produce an auditable budget for the chosen application.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-signal-processing-and-singular-value-transformation-9"></span>

### 21.9 Signal-processing laboratory

**Core result / role:** QSP/QSVT acceptance protocol.

**Assumptions and scope:** Independent scalar polynomial and dense singular-value reference.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Check parity, bounds, reconstruction, endpoints and full oracle budget.

**Imported earlier results:** [21.4](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-4), [21.5](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-5), [21.7](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-7), [21.8](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-8).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Report scalar-domain and matrix-level errors, including endpoints and failure cases.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 22: Quantum Walks, Lower Bounds, and Algorithm Design

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-1"></span>

### 22.1 Walk models and computational tasks

**Core result / role:** Discrete and continuous quantum-walk models.

**Assumptions and scope:** Specified graph, state space and update model.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Define the operator rather than treating graph adjacency as automatically unitary.

**Imported earlier results:** [14.4](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Exact source targets:** [WALK:construction](../references/proof-sources.md#source-walk-construction): Section III A-D Quantum walk, implementation, propagation and hitting-time bound.

**Independent evidence target:** Construct a small walk from an explicit graph.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-2"></span>

### 22.2 Unitarity, spectra, and dynamics

**Core result / role:** Walk spectral decomposition and conservation.

**Assumptions and scope:** Declared unitary step or Hermitian generator.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove norm conservation and derive selected graph eigenmodes.

**Imported earlier results:** [22.1](../section-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-1), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Exact source targets:** [WALK:construction](../references/proof-sources.md#source-walk-construction): Section III A-D Quantum walk, implementation, propagation and hitting-time bound.

**Independent evidence target:** Compare a circuit/tensor realization with an independent matrix.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-3"></span>

### 22.3 Search and marked vertices

**Core result / role:** Marked-vertex search in a selected graph.

**Assumptions and scope:** Explicit graph family, oracle and initial state.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive the invariant reduction or exact finite dynamics; delimit the graph-specific success claim.

**Imported earlier results:** [22.2](../section-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-2), [16.2](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-2).

**Exact source targets:** [QSVT:3.5.1](../references/proof-sources.md#source-qsvt-3-5-1): Section 3.5.1 Relationship to quantum walks.

**Independent evidence target:** Compare time-dependent marked probability under matched graph/access assumptions.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-4"></span>

### 22.4 Hitting behavior and algorithmic resources

**Core result / role:** Hitting/transport claims require an output protocol.

**Assumptions and scope:** Specified detection, repetition and graph-access cost.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive the selected success/runtime relation; distinguish classical hitting from quantum measurements.

**Imported earlier results:** [22.3](../section-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-3), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Exact source targets:** [WALK:construction](../references/proof-sources.md#source-walk-construction): Section III A-D Quantum walk, implementation, propagation and hitting-time bound.

**Independent evidence target:** Count initialization, walk steps, oracle use and readout.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-5"></span>

### 22.5 The polynomial method [Advanced]

**Core result / role:** Polynomial degree bound for query algorithms.

**Assumptions and scope:** T queries to a Boolean oracle; fixed non-oracle gates.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Induct on amplitude degree and show acceptance probability degree at most twice query count.

**Imported earlier results:** [14.4](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4), [15.1](../section-plans/03-algorithms.md#sec-interference-oracles-and-phase-kickback-1).

**Exact source targets:** [LB:polynomial](../references/proof-sources.md#source-lb-polynomial): Section 3 General lower bounds on the number of queries; polynomial lemma.

**Independent evidence target:** Check a small acceptance polynomial independently.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-6"></span>

### 22.6 A representative query lower bound

**Core result / role:** Unstructured-search query lower bound.

**Assumptions and scope:** Bounded error and standard black-box search model.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Give the selected polynomial/symmetrization proof roadmap and derive its final asymptotic consequence.

**Imported earlier results:** [22.5](../section-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-5), [16.1](../section-plans/03-algorithms.md#sec-grover-search-amplitude-amplification-and-estimation-1).

**Exact source targets:** [LB:search](../references/proof-sources.md#source-lb-search): Section 5.1 OR, database search, and connectives; [NC:6.6](../references/proof-sources.md#source-nc-6-6): Section 6.6 Optimality of the search algorithm.

**Independent evidence target:** Identify exactly which algorithm class/access model the result restricts.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local mathematical bridge to supply:** Acceptance-polynomial symmetrization and approximation degree.

**Explicitly deferred proof ingredients:** The general polynomial derivative/approximation inequality closing the OR/search bound; Beals et al. Section 5.1.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-7"></span>

### 22.7 Choosing an algorithmic framework

**Core result / role:** Algorithm-framework selection as a cost argument.

**Assumptions and scope:** Same access/output/error contract across candidates.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Select by proved assumptions and full cost; supply a counterexample to an unsuitable choice.

**Imported earlier results:** [20.7](../section-plans/03-algorithms.md#sec-qubitization-invariant-subspaces), [21.7](../section-plans/03-algorithms.md#sec-quantum-signal-processing-and-singular-value-transformation-7), [22.4](../section-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-4), [22.6](../section-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-6).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Compare candidate approaches for the same small task.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-hamiltonian-complexity-boundary"></span>

### 22.8 Hamiltonian complexity and limits of optimization [Advanced]

**Core result / role:** Local Hamiltonian promise and QMA boundary.

**Assumptions and scope:** Declared locality, norm bounds and inverse-polynomial promise gap.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Define QMA verification; derive a tiny energy-witness example; defer the history-state completeness reduction.

**Imported earlier results:** [14.3](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-3), [19.1](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-1), [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3).

**Exact source targets:** [COMPLEX:QMA](../references/proof-sources.md#source-complex-qma): Verification of quantum proofs; QMA and local-Hamiltonian examples; [P6:6.10](../references/proof-sources.md#source-p6-6-10): Section 6.10 QMA-completeness of the local Hamiltonian problem.

**Independent evidence target:** Check a tiny verifier/energy instance and identify which conclusions concern a promise problem versus finding a favorable small variational solution.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local mathematical bridge to supply:** Promise gaps, witness registers, verification circuits and local terms.

**Explicitly deferred proof ingredients:** History-state clock construction, propagation-gap and completeness/soundness reduction; Preskill 6.10 and Watrous complexity survey.

<span id="sec-quantum-walks-lower-bounds-and-algorithm-design-8"></span>

### 22.9 Algorithm-design laboratory

**Core result / role:** Algorithm-design acceptance protocol.

**Assumptions and scope:** Explicit promise, access and baseline.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Reuse proved bounds and identify unsupported extrapolations.

**Imported earlier results:** [22.3](../section-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-3), [22.6](../section-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-6), [22.7](../section-plans/03-algorithms.md#sec-quantum-walks-lower-bounds-and-algorithm-design-7), [22.8](../section-plans/03-algorithms.md#sec-hamiltonian-complexity-boundary).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Diagnose an invalid speedup argument or a lower bound applied outside its model.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.
