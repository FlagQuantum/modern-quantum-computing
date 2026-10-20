# Result and proof plan: Classical Simulation and the Boundary of Tractability

[Depth definitions](../proof-plan.md#proof-depth-contract) · [Source catalogue](../references/proof-sources.md) · [Volume plan](../volume-plan.md)

Authoring specifications only. No result/proof/API is certified by this plan. F/M/R have different scope; imported results are the exact prerequisite sections linked below.

## Chapter 44: Exact Simulation, Tensor Execution, and Numerical Reliability

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-1"></span>

### 44.1 Requested outputs and exact-simulation cost

**Core result / role:** Exact state/density storage and output lower bounds.

**Assumptions and scope:** n qubits, explicit complex dtype and requested output.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Count amplitudes/entries and output size; separate simulation strategy from hardware complexity.

**Imported earlier results:** [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2), [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3).

**Exact source targets:** [QUEST:representation](../references/proof-sources.md#source-quest-representation): Statevector representation and local-gate execution.

**Independent evidence target:** Predict memory and output size for declared workloads.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-2"></span>

### 44.2 Applying local gates by tensor indices

**Core result / role:** Local tensor gate kernel is dense operator action.

**Assumptions and scope:** Fixed index order and support mapping.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Expand all contracted indices and prove equality to the Kronecker-embedded matrix.

**Imported earlier results:** [4.6](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-6), [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1).

**Exact source targets:** [NC:2.1.7](../references/proof-sources.md#source-nc-2-1-7): Section 2.1.7 Tensor products; [QUEST:representation](../references/proof-sources.md#source-quest-representation): Statevector representation and local-gate execution.

**Independent evidence target:** Build an independent minimal executor and compare with dense matrices.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-3"></span>

### 44.3 Observables and measurement execution

**Core result / role:** Exact expectation, marginalization and sampling kernels.

**Assumptions and scope:** Normalized simulated state and declared measurement semantics.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive contraction and prefix/marginal probabilities; count cost for the requested output.

**Imported earlier results:** [44.2](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-2), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3).

**Exact source targets:** [NC:2.2.3](../references/proof-sources.md#source-nc-2-2-3): Section 2.2.3 Quantum measurement; [QUEST:representation](../references/proof-sources.md#source-quest-representation): Statevector representation and local-gate execution.

**Independent evidence target:** Check all branches against a separate state/matrix reference.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-4"></span>

### 44.4 Density-matrix and channel execution

**Core result / role:** Density-channel execution by Kraus/vectorized action.

**Assumptions and scope:** Fixed vectorization convention and finite Kraus set.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive both kernels and their trace/positivity invariants.

**Imported earlier results:** [44.2](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-2), [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3).

**Exact source targets:** [TQI:2.2.2](../references/proof-sources.md#source-tqi-2-2-2): Section 2.2.2 Representations and characterizations of channels.

**Independent evidence target:** Compare independent Kraus sums and complete small channel matrices.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-5"></span>

### 44.5 Batching and differentiation

**Core result / role:** Batch and derivative execution preserve component contracts.

**Assumptions and scope:** Independent batch axes; specified differentiation method.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the batching index map and reuse 23's derivative recurrence; account for memory.

**Imported earlier results:** [44.2](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-2), [23.6](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-6).

**Exact source targets:** [ADJ:2.2](../references/proof-sources.md#source-adj-2-2): Section 2.2 Derivation; [QUEST:parallel](../references/proof-sources.md#source-quest-parallel): Parallelization/distributed execution and benchmark methods.

**Independent evidence target:** Compare batched/scalar results and analytic gradients.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-6"></span>

### 44.6 Precision, stability, and normalization drift

**Core result / role:** Rounding/normalization drift is an execution error budget.

**Assumptions and scope:** Declared precision and gate count; bounded local errors.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive a telescoping norm bound and distinguish renormalization from recovering a lost phase.

**Imported earlier results:** [44.2](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-2), [2.8](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-8).

**Exact source targets:** [TQI:1.1.3](../references/proof-sources.md#source-tqi-1-1-3): Section 1.1.3 Operator decompositions and norms; [QUEST:representation](../references/proof-sources.md#source-quest-representation): Statevector representation and local-gate execution.

**Independent evidence target:** Compare precision levels, residuals and physically meaningful error metrics.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-7"></span>

### 44.7 Parallel execution and communication

**Core result / role:** Distributed statevector execution trades computation for communication.

**Assumptions and scope:** Explicit partition, local memory and network cost model.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive which gate indices require exchange and count transferred data.

**Imported earlier results:** [44.1](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-1), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Exact source targets:** [QUEST:parallel](../references/proof-sources.md#source-quest-parallel): Parallelization/distributed execution and benchmark methods.

**Independent evidence target:** Compare predicted data movement with a declared implementation or reference cost model.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-8"></span>

### 44.8 Exact-executor laboratory and benchmarks

**Core result / role:** Executor benchmark acceptance protocol.

**Assumptions and scope:** Same outputs, precision, warmup and hardware/environment record.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Check correctness before timings; report scaling, communication and uncertainty.

**Imported earlier results:** [44.2](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-2), [44.3](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-3), [44.6](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-6), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Exact source targets:** [QUEST:parallel](../references/proof-sources.md#source-quest-parallel): Parallelization/distributed execution and benchmark methods; [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Verify before timing and record environment, resource use and output semantics.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 45: Stabilizer Simulation, Magic, and Classical Simulability

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-1"></span>

### 45.1 Clifford operations and stabilizer states

**Core result / role:** Clifford conjugation closes the Pauli group.

**Assumptions and scope:** Selected Clifford generators and phase convention.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive generator conjugation tables and show stabilizer-state closure.

**Imported earlier results:** [30.1](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-1), [30.2](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-2), [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1).

**Exact source targets:** [NC:10.5.2](../references/proof-sources.md#source-nc-10-5-2): Section 10.5.2 Unitary gates and the stabilizer formalism.

**Independent evidence target:** Represent simple states independently as tableaus and dense vectors.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-2"></span>

### 45.2 Tableau representations and phase conventions

**Core result / role:** Tableau rows represent signed stabilizers.

**Assumptions and scope:** Declared symplectic/phase representation and independent generators.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove representation and row-product invariants.

**Imported earlier results:** [45.1](../section-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-1).

**Exact source targets:** [NC:10.5.1](../references/proof-sources.md#source-nc-10-5-1): Section 10.5.1 The stabilizer formalism.

**Independent evidence target:** Check generators, commutation and encoded phases.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-3"></span>

### 45.3 Clifford gate updates

**Core result / role:** Tableau Clifford updates are symplectic conjugations.

**Assumptions and scope:** Selected gate set and tableau convention.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive each bit/phase update and compare to Pauli matrix conjugation.

**Imported earlier results:** [45.2](../section-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-2), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Exact source targets:** [NC:10.5.2](../references/proof-sources.md#source-nc-10-5-2): Section 10.5.2 Unitary gates and the stabilizer formalism.

**Independent evidence target:** Compare each update with dense conjugation.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-4"></span>

### 45.4 Measurement and classical control

**Core result / role:** Stabilizer measurement branches and control.

**Assumptions and scope:** Specified Pauli measurement and valid tableau.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove deterministic versus random cases and row updates, retaining conditional records.

**Imported earlier results:** [45.3](../section-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-3), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2).

**Exact source targets:** [NC:10.5.3](../references/proof-sources.md#source-nc-10-5-3): Section 10.5.3 Measurement in the stabilizer formalism.

**Independent evidence target:** Verify branch probabilities and feed-forward on small states.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-5"></span>

### 45.5 The Gottesman-Knill theorem

**Core result / role:** Gottesman-Knill efficient-simulation theorem.

**Assumptions and scope:** Clifford preparation, Pauli measurements and supported classical control.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Combine tableau updates into an explicit polynomial-time algorithm and count its costs.

**Imported earlier results:** [45.3](../section-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-3), [45.4](../section-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-4), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Exact source targets:** [NC:10.5.4](../references/proof-sources.md#source-nc-10-5-4): Section 10.5.4 The Gottesman–Knill theorem.

**Independent evidence target:** Map the implementation's operations and data sizes to the theorem's proof structure.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-6"></span>

### 45.6 Beyond stabilizers: non-Clifford resources

**Core result / role:** Non-Clifford decomposition introduces a resource overhead.

**Assumptions and scope:** Chosen stabilizer expansion and output task.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive a selected small decomposition and count terms/weights; no generic efficient simulation claim.

**Imported earlier results:** [45.3](../section-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-3), [32.6](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-6).

**Exact source targets:** [MAGIC:resource](../references/proof-sources.md#source-magic-resource): Resource/free-operation definitions and discrete-Wigner restrictions; Theorem 5 (relative entropy of magic).

**Independent evidence target:** Introduce one controlled extension and compare it with an exact reference.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-7"></span>

### 45.7 Magic as a computational resource [Advanced]

**Core result / role:** Relative entropy of magic monotonicity (Veitch et al. Theorem 5), with the odd-prime Wigner caveat.

**Assumptions and scope:** Convex stabilizer free-state set; deterministic stabilizer-preserving CPTP maps; finite-copy relative entropy and support conventions.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Minimize relative entropy over free states and use data processing/free-set preservation to prove deterministic monotonicity; prove Clifford invariance. Do not assert monotonicity on every selected measurement branch or an asymptotic conversion-rate theorem.

**Imported earlier results:** [45.6](../section-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-6), [11.3](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-3), [11.5](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-5).

**Exact source targets:** [MAGIC:resource](../references/proof-sources.md#source-magic-resource): Resource/free-operation definitions and discrete-Wigner restrictions; Theorem 5 (relative entropy of magic).

**Independent evidence target:** Evaluate tractable examples without equating every non-Clifford circuit with advantage.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-8"></span>

### 45.8 Stabilizer-simulation laboratory

**Core result / role:** Stabilizer-simulator acceptance protocol.

**Assumptions and scope:** Independent dense reference and random/deterministic branches.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Check signs, distributions, frame updates and unsupported non-Clifford cases.

**Imported earlier results:** [45.3](../section-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-3), [45.4](../section-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-4), [44.2](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-2).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Audit both correctness and operation growth; preserve failure cases.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 46: Matrix Product States, Entanglement, and Truncation

<span id="sec-matrix-product-states-entanglement-and-truncation-1"></span>

### 46.1 Entanglement and compact state representations

**Core result / role:** Schmidt rank bounds exact MPS bond dimension.

**Assumptions and scope:** Finite ordered pure state and all bipartite cuts.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Relate each cut rank to factorization size and show ordering dependence.

**Imported earlier results:** [7.2](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-2).

**Exact source targets:** [SCHOLL:4.1.1](../references/proof-sources.md#source-scholl-4-1-1): Section 4.1.1 SVD and Schmidt decomposition; [MPS:rank](../references/proof-sources.md#source-mps-rank): State decomposition, updates and bounded-Schmidt-rank simulation argument.

**Independent evidence target:** Compare product, Bell-pair and more entangled example states.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-matrix-product-states-entanglement-and-truncation-2"></span>

### 46.2 Building an MPS by successive SVDs

**Core result / role:** Successive SVD constructs an exact MPS.

**Assumptions and scope:** Finite normalized coefficient tensor.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive each reshaping/SVD step and reconstruct every amplitude.

**Imported earlier results:** [46.1](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-1), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Exact source targets:** [SCHOLL:4.1.3](../references/proof-sources.md#source-scholl-4-1-3): Section 4.1.3 Decomposition of arbitrary quantum states into MPS.

**Independent evidence target:** Reconstruct a small state and compare with its exact vector.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-matrix-product-states-entanglement-and-truncation-3"></span>

### 46.3 Gauge freedom and canonical forms

**Core result / role:** MPS gauge freedom and canonical identities.

**Assumptions and scope:** Explicit internal bond spaces and invertible gauge map.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove cancellation and left/right isometry conditions; treat rank-deficient bonds.

**Imported earlier results:** [46.2](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-2).

**Exact source targets:** [SCHOLL:4.4](../references/proof-sources.md#source-scholl-4-4): Section 4.4 Bringing an MPS into canonical form.

**Independent evidence target:** Verify gauges and canonical residuals numerically.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-matrix-product-states-entanglement-and-truncation-4"></span>

### 46.4 Single- and two-qubit updates

**Core result / role:** Local gates update MPS tensors exactly before truncation.

**Assumptions and scope:** Specified adjacent support and MPS gauge.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive one-site contraction and two-site merge/SVD; account for nonadjacent movement.

**Imported earlier results:** [46.3](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-3), [4.4](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-4).

**Exact source targets:** [SCHOLL:7.3.2](../references/proof-sources.md#source-scholl-7-3-2): Section 7.3.2 Time-evolving block decimation.

**Independent evidence target:** Compare each step with an independent statevector calculation.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-matrix-product-states-entanglement-and-truncation-5"></span>

### 46.5 Truncation and discarded weight

**Core result / role:** Eckart-Young truncation and discarded weight.

**Assumptions and scope:** Frobenius norm; fixed retained rank; normalized Schmidt form.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove optimal SVD truncation in the selected norm and derive normalized-state error.

**Imported earlier results:** [46.2](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-2), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Exact source targets:** [SCHOLL:4.5.1](../references/proof-sources.md#source-scholl-4-5-1): Section 4.5.1 Compressing an MPS by SVD; [TQI:1.1.3](../references/proof-sources.md#source-tqi-1-1-3): Section 1.1.3 Operator decompositions and norms.

**Independent evidence target:** Compare predicted and actual state error for controlled truncations.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-matrix-product-states-entanglement-and-truncation-6"></span>

### 46.6 Accumulated error and observable accuracy

**Core result / role:** Sequential truncation bounds observable error.

**Assumptions and scope:** Specified normalization and per-step discarded weights.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Compose state errors and apply the bounded-observable inequality; avoid treating weights as universal infidelity.

**Imported earlier results:** [46.4](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-4), [46.5](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-5), [10.3](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-3).

**Exact source targets:** [SCHOLL:4.5.1](../references/proof-sources.md#source-scholl-4-5-1): Section 4.5.1 Compressing an MPS by SVD; [NC:9.2.1](../references/proof-sources.md#source-nc-9-2-1): Section 9.2.1 Trace distance.

**Independent evidence target:** Track fidelity/norm and observable error independently.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-matrix-product-states-entanglement-and-truncation-7"></span>

### 46.7 Bond dimension, entanglement, and cost

**Core result / role:** Entanglement entropy bounds rank but does not alone ensure efficiency.

**Assumptions and scope:** Finite cut spectrum and declared approximation criterion.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove the entropy/rank inequality and show why an exact-rank statement differs from a useful truncation guarantee.

**Imported earlier results:** [46.4](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-4), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Exact source targets:** [MPS:rank](../references/proof-sources.md#source-mps-rank): State decomposition, updates and bounded-Schmidt-rank simulation argument; [SCHOLL:3](../references/proof-sources.md#source-scholl-3): Section 3 DMRG and entanglement.

**Independent evidence target:** Vary bond limits and circuit geometry without claiming all shallow circuits are easy.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-matrix-product-states-entanglement-and-truncation-8"></span>

### 46.8 MPS laboratory

**Core result / role:** MPS acceptance protocol.

**Assumptions and scope:** Dense small-state reference and bond-dimension sweep.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Check gauges, spectra, discarded weights, observables and order-dependent costs.

**Imported earlier results:** [46.3](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-3), [46.4](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-4), [46.5](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-5), [46.6](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-6), [44.2](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-2).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Report all approximation settings, error records and cost/accuracy tradeoffs.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 47: Tensor Networks, Contraction, and Hybrid Simulation Strategies

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-1"></span>

### 47.1 Circuits as indexed tensor networks

**Core result / role:** Circuit tensor contraction equals the requested amplitude.

**Assumptions and scope:** Fixed index and boundary-state convention.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Expand inserted basis resolutions and identify every tensor index.

**Imported earlier results:** [4.6](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-6), [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1).

**Exact source targets:** [TN:3](../references/proof-sources.md#source-tn-3): Section 3 Tensors and tensor networks.

**Independent evidence target:** Compare a small network with an independently constructed circuit matrix.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-2"></span>

### 47.2 Contraction order and intermediate size

**Core result / role:** Contraction order changes intermediate sizes, not exact value.

**Assumptions and scope:** Finite exact tensor sums.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Use associativity/distributivity and count free indices for two orders.

**Imported earlier results:** [47.1](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-1), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Exact source targets:** [TN:3](../references/proof-sources.md#source-tn-3): Section 3 Tensors and tensor networks; [COTENGRA:II](../references/proof-sources.md#source-cotengra-ii): Section II Problem Statement.

**Independent evidence target:** Calculate intermediate shapes for several explicit paths.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-3"></span>

### 47.3 Path selection and structural parameters

**Core result / role:** Graph structure controls a stated contraction bound.

**Assumptions and scope:** Specified graph parameter and bounded tensor dimensions.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** State the exact selected treewidth/contraction-complexity relation and roadmap its graph-theoretic proof.

**Imported earlier results:** [47.2](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-2).

**Exact source targets:** [TN:4](../references/proof-sources.md#source-tn-4): Section 4 Contraction complexity and treewidth.

**Independent evidence target:** Compare estimated versus realized costs without implying optimality.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local advanced bridge to supply:** Tensor-network graph, line graph, tree decomposition and width.

**Explicitly deferred proof ingredients:** Graph-theoretic contraction-complexity/treewidth equivalence and tree-decomposition algorithm; Markov-Shi Section 4, Theorems 4.3/4.5.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-4"></span>

### 47.4 Slicing and recomputation

**Core result / role:** Slicing is exact summation with recomputation costs.

**Assumptions and scope:** Explicit sliced indices and full slice enumeration.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove reconstruction and count memory/work changes; distinguish partial-slice approximation.

**Imported earlier results:** [47.2](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-2).

**Exact source targets:** [COTENGRA:slicing](../references/proof-sources.md#source-cotengra-slicing): Section on Practical Performance, subsection Slicing.

**Independent evidence target:** Verify slice summation against an unsliced contraction.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-5"></span>

### 47.5 Amplitudes, expectations, sampling, and full states

**Core result / role:** Amplitude, expectation, sampling and full-state tasks have different boundaries.

**Assumptions and scope:** Explicit input/output tensors and output-size contract.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive each boundary contraction and explain where sampling needs conditional contractions.

**Imported earlier results:** [47.1](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-1), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2).

**Exact source targets:** [TN:3](../references/proof-sources.md#source-tn-3): Section 3 Tensors and tensor networks; [COTENGRA:II](../references/proof-sources.md#source-cotengra-ii): Section II Problem Statement.

**Independent evidence target:** Compare equivalent requested outputs and avoid misleading benchmark substitutions.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-circuit-cutting-reconstruction"></span>

### 47.6 Circuit cutting and classical reconstruction

**Core result / role:** Circuit cutting reconstructs a declared scalar output.

**Assumptions and scope:** Chosen complete operator decomposition and fragment interfaces.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive signed coefficients and fragment expectation identity; no claim of a physically larger coherent state.

**Imported earlier results:** [47.1](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-1), [6.5](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-5), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3).

**Exact source targets:** [CUT:identity](../references/proof-sources.md#source-cut-identity): Main-text circuit-decomposition identity and Appendix proof.

**Independent evidence target:** Compare a cut/reconstructed expectation with the complete uncut circuit; account for all fragment settings and distinguish this from distributed coherent execution.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-circuit-cutting-statistics"></span>

### 47.7 Reconstruction variance and sampling overhead

**Core result / role:** Cutting-estimator variance depends on signed weights.

**Assumptions and scope:** Unbiased fragment estimates and stated covariance/allocation model.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove expectation and variance formulas and derive a scoped shot-overhead bound.

**Imported earlier results:** [47.6](../section-plans/06-simulation.md#sec-circuit-cutting-reconstruction), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Exact source targets:** [CUT:variance](../references/proof-sources.md#source-cut-variance): Sampling/overhead analysis and Appendix proofs; [NC:A1](../references/proof-sources.md#source-nc-a1): Appendix 1: Notes on basic probability theory.

**Independent evidence target:** Compare repeated reconstructed estimates with an exact reference; report coefficient norm, settings, total shots and cases of prohibitive overhead.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-6"></span>

### 47.8 Hybrid and distributed strategies

**Core result / role:** Hybrid/distributed contraction needs a complete cost model.

**Assumptions and scope:** Specified slicing, devices, communication and reconstruction.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive one workload decomposition and include path search, transfers and aggregation.

**Imported earlier results:** [47.4](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-4), [44.7](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-7).

**Exact source targets:** [COTENGRA:slicing](../references/proof-sources.md#source-cotengra-slicing): Section on Practical Performance, subsection Slicing; [CUT:variance](../references/proof-sources.md#source-cut-variance): Sampling/overhead analysis and Appendix proofs.

**Independent evidence target:** Record communication, scheduling and aggregation semantics.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-7"></span>

### 47.9 Approximation and numerical reliability

**Core result / role:** Approximate contraction has model-specific error.

**Assumptions and scope:** Explicit discarded terms or low-rank truncations and precision.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Prove one selected bound or mark a heuristic without one; distinguish approximation from floating-point error.

**Imported earlier results:** [47.2](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-2), [2.8](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-8).

**Exact source targets:** [TQI:1.1.3](../references/proof-sources.md#source-tqi-1-1-3): Section 1.1.3 Operator decompositions and norms; [SCHOLL:4.5.1](../references/proof-sources.md#source-scholl-4-5-1): Section 4.5.1 Compressing an MPS by SVD.

**Independent evidence target:** Compare with exact small references and expose cancellation-sensitive cases.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-8"></span>

### 47.10 Tensor-network laboratory

**Core result / role:** Tensor-network acceptance protocol.

**Assumptions and scope:** Independent dense outputs and alternative exact paths.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Verify task boundaries, all slices/weights, uncertainty and full runtime/memory cost.

**Imported earlier results:** [47.2](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-2), [47.3](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-3), [47.4](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-4), [47.5](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-5), [47.9](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-7).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Report verified outputs, path/slicing records and honest tractability limits.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.
