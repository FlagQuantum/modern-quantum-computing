# Part 8. Classical Simulation and the Boundary of Tractability

**Detailed plan · 2026-10-20 · Scope fixed by Writing Baseline 1.0; prose and independent acceptance pending.** [All sections](../section-plan.md) · [Full plan](../book-plan.md) · [Reader continuity](../reader-continuity.md)

Each section specifies its argument and independent evidence. Framework implementation, mathematical review and reader review have separate status. Closing materials follow the [section-plan guide](../section-plan.md#how-to-read-the-specification).

<span id="ch-exact-simulation-tensor-execution-and-numerical-reliability"></span>
<span id="chapter-34"></span>

## Chapter 44

**Exact Simulation, Tensor Execution, and Numerical Reliability**

**Reading level:** Core. **Entry guidance:** 2, 4–6 for the exact-state executor; 8–9 for channels, 23 for gradients and 14 for parallel-resource analysis.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-1"></span>
<span id="341-requested-outputs-and-exact-simulation-cost"></span>

### 44.1 Requested outputs and exact-simulation cost

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-1).

**Section level:** core. **Required earlier sections:** [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2), [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3).

**Learning and derivation target:** Derive statevector/density storage and distinguish state, amplitude, sample and expectation requests.

**Implementation and evidence target:** Predict memory and output size for declared workloads.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-2"></span>
<span id="342-applying-local-gates-by-tensor-indices"></span>

### 44.2 Applying local gates by tensor indices

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-2).

**Section level:** core. **Required earlier sections:** [4.6](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-6), [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1).

**Learning and derivation target:** Derive reshape/permute/contraction gate application.

**Implementation and evidence target:** Build an independent minimal executor and compare with dense matrices.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-3"></span>
<span id="343-observables-and-measurement-execution"></span>

### 44.3 Observables and measurement execution

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-3).

**Section level:** core. **Required earlier sections:** [44.2](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-2), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3).

**Learning and derivation target:** Derive exact expectations, probabilities and conditional sampling.

**Implementation and evidence target:** Check all branches against a separate state/matrix reference.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-4"></span>
<span id="344-density-matrix-and-channel-execution"></span>

### 44.4 Density-matrix and channel execution

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-4).

**Section level:** core. **Required earlier sections:** [44.2](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-2), [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3).

**Learning and derivation target:** Derive local channel application on doubled tensor indices.

**Implementation and evidence target:** Compare independent Kraus sums and complete small channel matrices.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-5"></span>
<span id="345-batching-and-differentiation"></span>

### 44.5 Batching and differentiation

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-5).

**Section level:** core. **Required earlier sections:** [44.2](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-2), [23.6](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-6).

**Learning and derivation target:** Explain batch semantics and differentiation through a simulated calculation.

**Implementation and evidence target:** Compare batched/scalar results and analytic gradients.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-6"></span>
<span id="346-precision-stability-and-normalization-drift"></span>

### 44.6 Precision, stability, and normalization drift

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-6).

**Section level:** core. **Required earlier sections:** [44.2](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-2), [2.8](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-8).

**Learning and derivation target:** Analyze numerical error sources without silently renormalizing away defects.

**Implementation and evidence target:** Compare precision levels, residuals and physically meaningful error metrics.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-7"></span>
<span id="347-parallel-execution-and-communication"></span>

### 44.7 Parallel execution and communication

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-7).

**Section level:** core. **Required earlier sections:** [44.1](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-1), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Learning and derivation target:** Derive a simple data distribution and gate-dependent communication model.

**Implementation and evidence target:** Compare predicted data movement with a declared implementation or reference cost model.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-8"></span>
<span id="348-exact-executor-laboratory-and-benchmarks"></span>

### 44.8 Exact-executor laboratory and benchmarks

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-8).

**Section level:** core. **Required earlier sections:** [44.2](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-2), [44.3](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-3), [44.6](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-6), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Learning and derivation target:** Define workload, timing boundaries, warmup and correctness acceptance.

**Implementation and evidence target:** Verify before timing and record environment, resource use and output semantics.

<span id="ch-stabilizer-simulation-magic-and-classical-simulability"></span>
<span id="chapter-35"></span>

## Chapter 45

**Stabilizer Simulation, Magic, and Classical Simulability**

**Reading level:** Advanced. **Entry guidance:** 5–6 and Pauli/stabilizer sections of 30; a full error-correction or statevector chapter is not required for tableau entry.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-1"></span>
<span id="351-clifford-operations-and-stabilizer-states"></span>

### 45.1 Clifford operations and stabilizer states

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-1).

**Section level:** advanced. **Required earlier sections:** [30.1](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-1), [30.2](../section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-2), [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1).

**Learning and derivation target:** State the allowed operations and efficient-description setting.

**Implementation and evidence target:** Represent simple states independently as tableaus and dense vectors.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-2"></span>
<span id="352-tableau-representations-and-phase-conventions"></span>

### 45.2 Tableau representations and phase conventions

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-2).

**Section level:** advanced. **Required earlier sections:** [45.1](../section-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-1).

**Learning and derivation target:** Derive a consistent binary/phase tableau layout.

**Implementation and evidence target:** Check generators, commutation and encoded phases.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-3"></span>
<span id="353-clifford-gate-updates"></span>

### 45.3 Clifford gate updates

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-3).

**Section level:** advanced. **Required earlier sections:** [45.2](../section-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-2), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Learning and derivation target:** Derive update rules for a selected generating set.

**Implementation and evidence target:** Compare each update with dense conjugation.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-4"></span>
<span id="354-measurement-and-classical-control"></span>

### 45.4 Measurement and classical control

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-4).

**Section level:** advanced. **Required earlier sections:** [45.3](../section-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-3), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2).

**Learning and derivation target:** Derive deterministic/random outcome cases and conditional tableau updates.

**Implementation and evidence target:** Verify branch probabilities and feed-forward on small states.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-5"></span>
<span id="355-the-gottesman-knill-theorem"></span>

### 45.5 The Gottesman-Knill theorem

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-5).

**Section level:** advanced. **Required earlier sections:** [45.3](../section-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-3), [45.4](../section-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-4), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Learning and derivation target:** State the simulation claim with input, gate, measurement and output assumptions.

**Implementation and evidence target:** Map the implementation's operations and data sizes to the theorem's proof structure.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-6"></span>
<span id="356-beyond-stabilizers-non-clifford-resources"></span>

### 45.6 Beyond stabilizers: non-Clifford resources

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-6).

**Section level:** advanced. **Required earlier sections:** [45.3](../section-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-3), [32.6](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-6).

**Learning and derivation target:** Explain where the efficient representation ceases to close.

**Implementation and evidence target:** Introduce one controlled extension and compare it with an exact reference.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-7"></span>
<span id="357-magic-as-a-computational-resource-advanced"></span>

### 45.7 Magic as a computational resource [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-7).

**Section level:** advanced. **Required earlier sections:** [45.6](../section-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-6), [11.3](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-3), [11.5](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-5).

**Learning and derivation target:** State a selected resource notion and its relation to simulation constraints.

**Implementation and evidence target:** Evaluate tractable examples without equating every non-Clifford circuit with advantage.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-8"></span>
<span id="358-stabilizer-simulation-laboratory"></span>

### 45.8 Stabilizer-simulation laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-8).

**Section level:** advanced. **Required earlier sections:** [45.3](../section-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-3), [45.4](../section-plans/06-simulation.md#sec-stabilizer-simulation-magic-and-classical-simulability-4), [44.2](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-2).

**Learning and derivation target:** Compare exact dense and tableau executions including adaptive branches.

**Implementation and evidence target:** Audit both correctness and operation growth; preserve failure cases.

<span id="ch-matrix-product-states-entanglement-and-truncation"></span>
<span id="chapter-36"></span>

## Chapter 46

**Matrix Product States, Entanglement, and Truncation**

**Reading level:** Advanced. **Entry guidance:** 2, 4, Schmidt structure in 7; selected 10/44 for comparisons, not tomography or autograd.

<span id="sec-matrix-product-states-entanglement-and-truncation-1"></span>
<span id="361-entanglement-and-compact-state-representations"></span>

### 46.1 Entanglement and compact state representations

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-1).

**Section level:** advanced. **Required earlier sections:** [7.2](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-2).

**Learning and derivation target:** Relate Schmidt rank across cuts to representational requirements.

**Implementation and evidence target:** Compare product, Bell-pair and more entangled example states.

<span id="sec-matrix-product-states-entanglement-and-truncation-2"></span>
<span id="362-building-an-mps-by-successive-svds"></span>

### 46.2 Building an MPS by successive SVDs

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-2).

**Section level:** advanced. **Required earlier sections:** [46.1](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-1), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Learning and derivation target:** Derive tensor shapes and boundary conventions.

**Implementation and evidence target:** Reconstruct a small state and compare with its exact vector.

<span id="sec-matrix-product-states-entanglement-and-truncation-3"></span>
<span id="363-gauge-freedom-and-canonical-forms"></span>

### 46.3 Gauge freedom and canonical forms

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-3).

**Section level:** advanced. **Required earlier sections:** [46.2](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-2).

**Learning and derivation target:** Derive equivalent tensor descriptions and orthogonality conditions.

**Implementation and evidence target:** Verify gauges and canonical residuals numerically.

<span id="sec-matrix-product-states-entanglement-and-truncation-4"></span>
<span id="364-single-and-two-qubit-updates"></span>

### 46.4 Single- and two-qubit updates

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-4).

**Section level:** advanced. **Required earlier sections:** [46.3](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-3), [4.4](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-4).

**Learning and derivation target:** Derive local updates, bond growth and qubit-order effects.

**Implementation and evidence target:** Compare each step with an independent statevector calculation.

<span id="sec-matrix-product-states-entanglement-and-truncation-5"></span>
<span id="365-truncation-and-discarded-weight"></span>

### 46.5 Truncation and discarded weight

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-5).

**Section level:** advanced. **Required earlier sections:** [46.2](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-2), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Learning and derivation target:** Derive a scoped error relation with normalization assumptions.

**Implementation and evidence target:** Compare predicted and actual state error for controlled truncations.

<span id="sec-matrix-product-states-entanglement-and-truncation-6"></span>
<span id="366-accumulated-error-and-observable-accuracy"></span>

### 46.6 Accumulated error and observable accuracy

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-6).

**Section level:** advanced. **Required earlier sections:** [46.4](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-4), [46.5](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-5), [10.3](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-3).

**Learning and derivation target:** Explain how repeated truncations and requested observables change validation.

**Implementation and evidence target:** Track fidelity/norm and observable error independently.

<span id="sec-matrix-product-states-entanglement-and-truncation-7"></span>
<span id="367-bond-dimension-entanglement-and-cost"></span>

### 46.7 Bond dimension, entanglement, and cost

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-7).

**Section level:** advanced. **Required earlier sections:** [46.4](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-4), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Learning and derivation target:** Derive memory/operation growth for a stated update method.

**Implementation and evidence target:** Vary bond limits and circuit geometry without claiming all shallow circuits are easy.

<span id="sec-matrix-product-states-entanglement-and-truncation-8"></span>
<span id="368-mps-laboratory"></span>

### 46.8 MPS laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-8).

**Section level:** advanced. **Required earlier sections:** [46.3](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-3), [46.4](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-4), [46.5](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-5), [46.6](../section-plans/06-simulation.md#sec-matrix-product-states-entanglement-and-truncation-6), [44.2](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-2).

**Learning and derivation target:** Connect canonicalization, updates, truncation settings and independent evidence.

**Implementation and evidence target:** Report all approximation settings, error records and cost/accuracy tradeoffs.

<span id="ch-tensor-networks-contraction-and-hybrid-simulation-strategies"></span>
<span id="chapter-37"></span>

## Chapter 47

**Tensor Networks, Contraction, and Hybrid Simulation Strategies**

**Reading level:** Advanced. **Entry guidance:** 4–5, 14 for circuit contractions; 6/9 for cutting and 44/46 only for the chosen hybrid executor.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-1"></span>
<span id="371-circuits-as-indexed-tensor-networks"></span>

### 47.1 Circuits as indexed tensor networks

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-1).

**Section level:** advanced. **Required earlier sections:** [4.6](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-6), [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1).

**Learning and derivation target:** Derive gate/state/measurement tensors and their connected indices.

**Implementation and evidence target:** Compare a small network with an independently constructed circuit matrix.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-2"></span>
<span id="372-contraction-order-and-intermediate-size"></span>

### 47.2 Contraction order and intermediate size

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-2).

**Section level:** advanced. **Required earlier sections:** [47.1](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-1), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Learning and derivation target:** Show why equivalent contractions have different memory and work.

**Implementation and evidence target:** Calculate intermediate shapes for several explicit paths.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-3"></span>
<span id="373-path-selection-and-structural-parameters"></span>

### 47.3 Path selection and structural parameters

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-3).

**Section level:** advanced. **Required earlier sections:** [47.2](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-2).

**Learning and derivation target:** Explain a selected path heuristic and graph-based complexity intuition.

**Implementation and evidence target:** Compare estimated versus realized costs without implying optimality.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-4"></span>
<span id="374-slicing-and-recomputation"></span>

### 47.4 Slicing and recomputation

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-4).

**Section level:** advanced. **Required earlier sections:** [47.2](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-2).

**Learning and derivation target:** Derive decomposition over selected indices and its memory/work tradeoff.

**Implementation and evidence target:** Verify slice summation against an unsliced contraction.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-5"></span>
<span id="375-amplitudes-expectations-sampling-and-full-states"></span>

### 47.5 Amplitudes, expectations, sampling, and full states

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-5).

**Section level:** advanced. **Required earlier sections:** [47.1](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-1), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2).

**Learning and derivation target:** Specify distinct output tasks and their contraction implications.

**Implementation and evidence target:** Compare equivalent requested outputs and avoid misleading benchmark substitutions.

<span id="sec-circuit-cutting-reconstruction"></span>

### 47.6 Circuit cutting and classical reconstruction

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-circuit-cutting-reconstruction).

**Section level:** advanced. **Required earlier sections:** [47.1](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-1), [6.5](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-5), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3).

**Learning and derivation target:** Derive a small cut decomposition with coefficients, fragment preparation/measurement settings and a precisely requested reconstructed observable.

**Implementation and evidence target:** Compare a cut/reconstructed expectation with the complete uncut circuit; account for all fragment settings and distinguish this from distributed coherent execution.

<span id="sec-circuit-cutting-statistics"></span>

### 47.7 Reconstruction variance and sampling overhead

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-circuit-cutting-statistics).

**Section level:** advanced. **Required earlier sections:** [47.6](../section-plans/06-simulation.md#sec-circuit-cutting-reconstruction), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Learning and derivation target:** Derive a scoped variance/shot-allocation relation including signed coefficients and state the noise/independence assumptions.

**Implementation and evidence target:** Compare repeated reconstructed estimates with an exact reference; report coefficient norm, settings, total shots and cases of prohibitive overhead.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-6"></span>
<span id="376-hybrid-and-distributed-strategies"></span>
<span id="476-hybrid-and-distributed-strategies"></span>

### 47.8 Hybrid and distributed strategies

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-6).

**Section level:** advanced. **Required earlier sections:** [47.4](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-4), [44.7](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-7).

**Learning and derivation target:** Explain partitioning and a selected statevector/network or sliced execution strategy.

**Implementation and evidence target:** Record communication, scheduling and aggregation semantics.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-7"></span>
<span id="377-approximation-and-numerical-reliability"></span>
<span id="477-approximation-and-numerical-reliability"></span>

### 47.9 Approximation and numerical reliability

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-7).

**Section level:** advanced. **Required earlier sections:** [47.2](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-2), [2.8](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-8).

**Learning and derivation target:** State any approximations and contraction/rounding validation criteria.

**Implementation and evidence target:** Compare with exact small references and expose cancellation-sensitive cases.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-8"></span>
<span id="378-tensor-network-laboratory"></span>
<span id="478-tensor-network-laboratory"></span>

### 47.10 Tensor-network laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-8).

**Section level:** advanced. **Required earlier sections:** [47.2](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-2), [47.3](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-3), [47.4](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-4), [47.5](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-5), [47.9](../section-plans/06-simulation.md#sec-tensor-networks-contraction-and-hybrid-simulation-strategies-7).

**Learning and derivation target:** Choose a workload, path, memory limit and precise output contract.

**Implementation and evidence target:** Report verified outputs, path/slicing records and honest tractability limits.
