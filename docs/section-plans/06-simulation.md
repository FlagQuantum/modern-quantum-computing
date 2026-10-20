# Part 6: Classical Simulation and the Boundary of Tractability

**Detailed section plan · October 20, 2026 · Planned material.** [All section plans](../section-plan.md) · [Curriculum and prerequisites](../book-plan.md)

Each numbered section specifies its intended argument and independent evidence. The unnumbered closing material and authoring rules are defined in the [section-plan guide](../section-plan.md#how-to-read-the-specification). Implementation status remains separate from curriculum status.

## Chapter 34

**Exact Simulation, Tensor Execution, and Numerical Reliability**

**Reading level:** Core. **Chapter prerequisites:** 2, 4–6, 8, 14, 23.

### 34.1 Requested outputs and exact-simulation cost

**Learning and derivation target:** Derive statevector/density storage and distinguish state, amplitude, sample and expectation requests.

**Implementation and evidence target:** Predict memory and output size for declared workloads.

### 34.2 Applying local gates by tensor indices

**Learning and derivation target:** Derive reshape/permute/contraction gate application.

**Implementation and evidence target:** Build an independent minimal executor and compare with dense matrices.

### 34.3 Observables and measurement execution

**Learning and derivation target:** Derive exact expectations, probabilities and conditional sampling.

**Implementation and evidence target:** Check all branches against a separate state/matrix reference.

### 34.4 Density-matrix and channel execution

**Learning and derivation target:** Derive local channel application on doubled tensor indices.

**Implementation and evidence target:** Compare independent Kraus sums and complete small channel matrices.

### 34.5 Batching and differentiation

**Learning and derivation target:** Explain batch semantics and differentiation through a simulated calculation.

**Implementation and evidence target:** Compare batched/scalar results and analytic gradients.

### 34.6 Precision, stability, and normalization drift

**Learning and derivation target:** Analyze numerical error sources without silently renormalizing away defects.

**Implementation and evidence target:** Compare precision levels, residuals and physically meaningful error metrics.

### 34.7 Parallel execution and communication

**Learning and derivation target:** Derive a simple data distribution and gate-dependent communication model.

**Implementation and evidence target:** Compare predicted data movement with a declared implementation or reference cost model.

### 34.8 Exact-executor laboratory and benchmarks

**Learning and derivation target:** Define workload, timing boundaries, warmup and correctness acceptance.

**Implementation and evidence target:** Verify before timing and record environment, resource use and output semantics.

## Chapter 35

**Stabilizer Simulation, Magic, and Classical Simulability**

**Reading level:** Advanced. **Chapter prerequisites:** 14, 30, 34.

### 35.1 Clifford operations and stabilizer states

**Learning and derivation target:** State the allowed operations and efficient-description setting.

**Implementation and evidence target:** Represent simple states independently as tableaus and dense vectors.

### 35.2 Tableau representations and phase conventions

**Learning and derivation target:** Derive a consistent binary/phase tableau layout.

**Implementation and evidence target:** Check generators, commutation and encoded phases.

### 35.3 Clifford gate updates

**Learning and derivation target:** Derive update rules for a selected generating set.

**Implementation and evidence target:** Compare each update with dense conjugation.

### 35.4 Measurement and classical control

**Learning and derivation target:** Derive deterministic/random outcome cases and conditional tableau updates.

**Implementation and evidence target:** Verify branch probabilities and feed-forward on small states.

### 35.5 The Gottesman-Knill theorem

**Learning and derivation target:** State the simulation claim with input, gate, measurement and output assumptions.

**Implementation and evidence target:** Map the implementation's operations and data sizes to the theorem's proof structure.

### 35.6 Beyond stabilizers: non-Clifford resources

**Learning and derivation target:** Explain where the efficient representation ceases to close.

**Implementation and evidence target:** Introduce one controlled extension and compare it with an exact reference.

### 35.7 Magic as a computational resource [Advanced]

**Learning and derivation target:** State a selected resource notion and its relation to simulation constraints.

**Implementation and evidence target:** Evaluate tractable examples without equating every non-Clifford circuit with advantage.

### 35.8 Stabilizer-simulation laboratory

**Learning and derivation target:** Compare exact dense and tableau executions including adaptive branches.

**Implementation and evidence target:** Audit both correctness and operation growth; preserve failure cases.

## Chapter 36

**Matrix Product States, Entanglement, and Truncation**

**Reading level:** Advanced. **Chapter prerequisites:** 2, 4, 7, 8, 10, 34.

### 36.1 Entanglement and compact state representations

**Learning and derivation target:** Relate Schmidt rank across cuts to representational requirements.

**Implementation and evidence target:** Compare product, Bell-pair and more entangled example states.

### 36.2 Building an MPS by successive SVDs

**Learning and derivation target:** Derive tensor shapes and boundary conventions.

**Implementation and evidence target:** Reconstruct a small state and compare with its exact vector.

### 36.3 Gauge freedom and canonical forms

**Learning and derivation target:** Derive equivalent tensor descriptions and orthogonality conditions.

**Implementation and evidence target:** Verify gauges and canonical residuals numerically.

### 36.4 Single- and two-qubit updates

**Learning and derivation target:** Derive local updates, bond growth and qubit-order effects.

**Implementation and evidence target:** Compare each step with an independent statevector calculation.

### 36.5 Truncation and discarded weight

**Learning and derivation target:** Derive a scoped error relation with normalization assumptions.

**Implementation and evidence target:** Compare predicted and actual state error for controlled truncations.

### 36.6 Accumulated error and observable accuracy

**Learning and derivation target:** Explain how repeated truncations and requested observables change validation.

**Implementation and evidence target:** Track fidelity/norm and observable error independently.

### 36.7 Bond dimension, entanglement, and cost

**Learning and derivation target:** Derive memory/operation growth for a stated update method.

**Implementation and evidence target:** Vary bond limits and circuit geometry without claiming all shallow circuits are easy.

### 36.8 MPS laboratory

**Learning and derivation target:** Connect canonicalization, updates, truncation settings and independent evidence.

**Implementation and evidence target:** Report all approximation settings, error records and cost/accuracy tradeoffs.

## Chapter 37

**Tensor Networks, Contraction, and Hybrid Simulation Strategies**

**Reading level:** Advanced. **Chapter prerequisites:** 14, 34, 36.

### 37.1 Circuits as indexed tensor networks

**Learning and derivation target:** Derive gate/state/measurement tensors and their connected indices.

**Implementation and evidence target:** Compare a small network with an independently constructed circuit matrix.

### 37.2 Contraction order and intermediate size

**Learning and derivation target:** Show why equivalent contractions have different memory and work.

**Implementation and evidence target:** Calculate intermediate shapes for several explicit paths.

### 37.3 Path selection and structural parameters

**Learning and derivation target:** Explain a selected path heuristic and graph-based complexity intuition.

**Implementation and evidence target:** Compare estimated versus realized costs without implying optimality.

### 37.4 Slicing and recomputation

**Learning and derivation target:** Derive decomposition over selected indices and its memory/work tradeoff.

**Implementation and evidence target:** Verify slice summation against an unsliced contraction.

### 37.5 Amplitudes, expectations, sampling, and full states

**Learning and derivation target:** Specify distinct output tasks and their contraction implications.

**Implementation and evidence target:** Compare equivalent requested outputs and avoid misleading benchmark substitutions.

### 37.6 Hybrid and distributed strategies

**Learning and derivation target:** Explain partitioning and a selected statevector/network or sliced execution strategy.

**Implementation and evidence target:** Record communication, scheduling and aggregation semantics.

### 37.7 Approximation and numerical reliability

**Learning and derivation target:** State any approximations and contraction/rounding validation criteria.

**Implementation and evidence target:** Compare with exact small references and expose cancellation-sensitive cases.

### 37.8 Tensor-network laboratory

**Learning and derivation target:** Choose a workload, path, memory limit and precise output contract.

**Implementation and evidence target:** Report verified outputs, path/slicing records and honest tractability limits.
