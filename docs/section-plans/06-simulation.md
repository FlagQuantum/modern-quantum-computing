# Part 8. Classical Simulation and the Boundary of Tractability

**Detailed plan · 2026-10-20 · Planned material; architecture review pending.** [All sections](../section-plan.md) · [Full plan](../book-plan.md) · [Reader continuity](../reader-continuity.md)

Each section specifies its argument and independent evidence. Framework implementation, mathematical review and reader review have separate status. Closing materials follow the [section-plan guide](../section-plan.md#how-to-read-the-specification).

<span id="ch-exact-simulation-tensor-execution-and-numerical-reliability"></span>
<span id="chapter-34"></span>

## Chapter 44

**Exact Simulation, Tensor Execution, and Numerical Reliability**

**Reading level:** Core. **Chapter prerequisites:** 2, 4–6, 8, 14, 23.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-1"></span>
<span id="341-requested-outputs-and-exact-simulation-cost"></span>

### 44.1 Requested outputs and exact-simulation cost

**Learning and derivation target:** Derive statevector/density storage and distinguish state, amplitude, sample and expectation requests.

**Implementation and evidence target:** Predict memory and output size for declared workloads.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-2"></span>
<span id="342-applying-local-gates-by-tensor-indices"></span>

### 44.2 Applying local gates by tensor indices

**Learning and derivation target:** Derive reshape/permute/contraction gate application.

**Implementation and evidence target:** Build an independent minimal executor and compare with dense matrices.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-3"></span>
<span id="343-observables-and-measurement-execution"></span>

### 44.3 Observables and measurement execution

**Learning and derivation target:** Derive exact expectations, probabilities and conditional sampling.

**Implementation and evidence target:** Check all branches against a separate state/matrix reference.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-4"></span>
<span id="344-density-matrix-and-channel-execution"></span>

### 44.4 Density-matrix and channel execution

**Learning and derivation target:** Derive local channel application on doubled tensor indices.

**Implementation and evidence target:** Compare independent Kraus sums and complete small channel matrices.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-5"></span>
<span id="345-batching-and-differentiation"></span>

### 44.5 Batching and differentiation

**Learning and derivation target:** Explain batch semantics and differentiation through a simulated calculation.

**Implementation and evidence target:** Compare batched/scalar results and analytic gradients.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-6"></span>
<span id="346-precision-stability-and-normalization-drift"></span>

### 44.6 Precision, stability, and normalization drift

**Learning and derivation target:** Analyze numerical error sources without silently renormalizing away defects.

**Implementation and evidence target:** Compare precision levels, residuals and physically meaningful error metrics.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-7"></span>
<span id="347-parallel-execution-and-communication"></span>

### 44.7 Parallel execution and communication

**Learning and derivation target:** Derive a simple data distribution and gate-dependent communication model.

**Implementation and evidence target:** Compare predicted data movement with a declared implementation or reference cost model.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-8"></span>
<span id="348-exact-executor-laboratory-and-benchmarks"></span>

### 44.8 Exact-executor laboratory and benchmarks

**Learning and derivation target:** Define workload, timing boundaries, warmup and correctness acceptance.

**Implementation and evidence target:** Verify before timing and record environment, resource use and output semantics.

<span id="ch-stabilizer-simulation-magic-and-classical-simulability"></span>
<span id="chapter-35"></span>

## Chapter 45

**Stabilizer Simulation, Magic, and Classical Simulability**

**Reading level:** Advanced. **Chapter prerequisites:** 14, 30, 44.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-1"></span>
<span id="351-clifford-operations-and-stabilizer-states"></span>

### 45.1 Clifford operations and stabilizer states

**Learning and derivation target:** State the allowed operations and efficient-description setting.

**Implementation and evidence target:** Represent simple states independently as tableaus and dense vectors.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-2"></span>
<span id="352-tableau-representations-and-phase-conventions"></span>

### 45.2 Tableau representations and phase conventions

**Learning and derivation target:** Derive a consistent binary/phase tableau layout.

**Implementation and evidence target:** Check generators, commutation and encoded phases.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-3"></span>
<span id="353-clifford-gate-updates"></span>

### 45.3 Clifford gate updates

**Learning and derivation target:** Derive update rules for a selected generating set.

**Implementation and evidence target:** Compare each update with dense conjugation.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-4"></span>
<span id="354-measurement-and-classical-control"></span>

### 45.4 Measurement and classical control

**Learning and derivation target:** Derive deterministic/random outcome cases and conditional tableau updates.

**Implementation and evidence target:** Verify branch probabilities and feed-forward on small states.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-5"></span>
<span id="355-the-gottesman-knill-theorem"></span>

### 45.5 The Gottesman-Knill theorem

**Learning and derivation target:** State the simulation claim with input, gate, measurement and output assumptions.

**Implementation and evidence target:** Map the implementation's operations and data sizes to the theorem's proof structure.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-6"></span>
<span id="356-beyond-stabilizers-non-clifford-resources"></span>

### 45.6 Beyond stabilizers: non-Clifford resources

**Learning and derivation target:** Explain where the efficient representation ceases to close.

**Implementation and evidence target:** Introduce one controlled extension and compare it with an exact reference.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-7"></span>
<span id="357-magic-as-a-computational-resource-advanced"></span>

### 45.7 Magic as a computational resource [Advanced]

**Learning and derivation target:** State a selected resource notion and its relation to simulation constraints.

**Implementation and evidence target:** Evaluate tractable examples without equating every non-Clifford circuit with advantage.

<span id="sec-stabilizer-simulation-magic-and-classical-simulability-8"></span>
<span id="358-stabilizer-simulation-laboratory"></span>

### 45.8 Stabilizer-simulation laboratory

**Learning and derivation target:** Compare exact dense and tableau executions including adaptive branches.

**Implementation and evidence target:** Audit both correctness and operation growth; preserve failure cases.

<span id="ch-matrix-product-states-entanglement-and-truncation"></span>
<span id="chapter-36"></span>

## Chapter 46

**Matrix Product States, Entanglement, and Truncation**

**Reading level:** Advanced. **Chapter prerequisites:** 2, 4, 7, 8, 10, 44.

<span id="sec-matrix-product-states-entanglement-and-truncation-1"></span>
<span id="361-entanglement-and-compact-state-representations"></span>

### 46.1 Entanglement and compact state representations

**Learning and derivation target:** Relate Schmidt rank across cuts to representational requirements.

**Implementation and evidence target:** Compare product, Bell-pair and more entangled example states.

<span id="sec-matrix-product-states-entanglement-and-truncation-2"></span>
<span id="362-building-an-mps-by-successive-svds"></span>

### 46.2 Building an MPS by successive SVDs

**Learning and derivation target:** Derive tensor shapes and boundary conventions.

**Implementation and evidence target:** Reconstruct a small state and compare with its exact vector.

<span id="sec-matrix-product-states-entanglement-and-truncation-3"></span>
<span id="363-gauge-freedom-and-canonical-forms"></span>

### 46.3 Gauge freedom and canonical forms

**Learning and derivation target:** Derive equivalent tensor descriptions and orthogonality conditions.

**Implementation and evidence target:** Verify gauges and canonical residuals numerically.

<span id="sec-matrix-product-states-entanglement-and-truncation-4"></span>
<span id="364-single-and-two-qubit-updates"></span>

### 46.4 Single- and two-qubit updates

**Learning and derivation target:** Derive local updates, bond growth and qubit-order effects.

**Implementation and evidence target:** Compare each step with an independent statevector calculation.

<span id="sec-matrix-product-states-entanglement-and-truncation-5"></span>
<span id="365-truncation-and-discarded-weight"></span>

### 46.5 Truncation and discarded weight

**Learning and derivation target:** Derive a scoped error relation with normalization assumptions.

**Implementation and evidence target:** Compare predicted and actual state error for controlled truncations.

<span id="sec-matrix-product-states-entanglement-and-truncation-6"></span>
<span id="366-accumulated-error-and-observable-accuracy"></span>

### 46.6 Accumulated error and observable accuracy

**Learning and derivation target:** Explain how repeated truncations and requested observables change validation.

**Implementation and evidence target:** Track fidelity/norm and observable error independently.

<span id="sec-matrix-product-states-entanglement-and-truncation-7"></span>
<span id="367-bond-dimension-entanglement-and-cost"></span>

### 46.7 Bond dimension, entanglement, and cost

**Learning and derivation target:** Derive memory/operation growth for a stated update method.

**Implementation and evidence target:** Vary bond limits and circuit geometry without claiming all shallow circuits are easy.

<span id="sec-matrix-product-states-entanglement-and-truncation-8"></span>
<span id="368-mps-laboratory"></span>

### 46.8 MPS laboratory

**Learning and derivation target:** Connect canonicalization, updates, truncation settings and independent evidence.

**Implementation and evidence target:** Report all approximation settings, error records and cost/accuracy tradeoffs.

<span id="ch-tensor-networks-contraction-and-hybrid-simulation-strategies"></span>
<span id="chapter-37"></span>

## Chapter 47

**Tensor Networks, Contraction, and Hybrid Simulation Strategies**

**Reading level:** Advanced. **Chapter prerequisites:** 14, 44, 46.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-1"></span>
<span id="371-circuits-as-indexed-tensor-networks"></span>

### 47.1 Circuits as indexed tensor networks

**Learning and derivation target:** Derive gate/state/measurement tensors and their connected indices.

**Implementation and evidence target:** Compare a small network with an independently constructed circuit matrix.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-2"></span>
<span id="372-contraction-order-and-intermediate-size"></span>

### 47.2 Contraction order and intermediate size

**Learning and derivation target:** Show why equivalent contractions have different memory and work.

**Implementation and evidence target:** Calculate intermediate shapes for several explicit paths.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-3"></span>
<span id="373-path-selection-and-structural-parameters"></span>

### 47.3 Path selection and structural parameters

**Learning and derivation target:** Explain a selected path heuristic and graph-based complexity intuition.

**Implementation and evidence target:** Compare estimated versus realized costs without implying optimality.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-4"></span>
<span id="374-slicing-and-recomputation"></span>

### 47.4 Slicing and recomputation

**Learning and derivation target:** Derive decomposition over selected indices and its memory/work tradeoff.

**Implementation and evidence target:** Verify slice summation against an unsliced contraction.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-5"></span>
<span id="375-amplitudes-expectations-sampling-and-full-states"></span>

### 47.5 Amplitudes, expectations, sampling, and full states

**Learning and derivation target:** Specify distinct output tasks and their contraction implications.

**Implementation and evidence target:** Compare equivalent requested outputs and avoid misleading benchmark substitutions.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-6"></span>
<span id="376-hybrid-and-distributed-strategies"></span>

### 47.6 Hybrid and distributed strategies

**Learning and derivation target:** Explain partitioning and a selected statevector/network or sliced execution strategy.

**Implementation and evidence target:** Record communication, scheduling and aggregation semantics.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-7"></span>
<span id="377-approximation-and-numerical-reliability"></span>

### 47.7 Approximation and numerical reliability

**Learning and derivation target:** State any approximations and contraction/rounding validation criteria.

**Implementation and evidence target:** Compare with exact small references and expose cancellation-sensitive cases.

<span id="sec-tensor-networks-contraction-and-hybrid-simulation-strategies-8"></span>
<span id="378-tensor-network-laboratory"></span>

### 47.8 Tensor-network laboratory

**Learning and derivation target:** Choose a workload, path, memory limit and precise output contract.

**Implementation and evidence target:** Report verified outputs, path/slicing records and honest tractability limits.
