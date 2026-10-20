# Part 7. Quantum Programming, Compilation, and Control

**Detailed plan · 2026-10-20 · Scope fixed by Writing Baseline 1.0; prose and independent acceptance pending.** [All sections](../section-plan.md) · [Full plan](../book-plan.md) · [Reader continuity](../reader-continuity.md)

Each section specifies its argument and independent evidence. Framework implementation, mathematical review and reader review have separate status. Closing materials follow the [section-plan guide](../section-plan.md#how-to-read-the-specification).

<span id="ch-quantum-programs-intermediate-representations-and-verified-optimization"></span>

## Chapter 41

**Quantum Programs, Intermediate Representations, and Verified Optimization**

**Reading level:** Core systems route with advanced extensions. **Entry guidance:** 4–6 for circuit semantics/IR; 9 for channel/dynamic branches; no microscopic hardware prerequisite.

<span id="sec-quantum-programs-intermediate-representations-and-verified-optimization-1"></span>

### 41.1 What a quantum compiler must preserve

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-1).

**Section level:** core. **Required earlier sections:** [4.3](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-3), [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1).

**Learning and derivation target:** Define program inputs/outputs, unitary/channel semantics and classical records.

**Implementation and evidence target:** Compare equivalent states, channels and distributions and explain which equality a pass must satisfy.

<span id="sec-quantum-programs-intermediate-representations-and-verified-optimization-2"></span>

### 41.2 Programs, types, and quantum-classical control

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-2).

**Section level:** core. **Required earlier sections:** [41.1](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-1), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2).

**Learning and derivation target:** Define qubit allocation, classical values, parameters and legal data dependencies.

**Implementation and evidence target:** Represent a tiny hybrid program and diagnose an invalid use of a measured value or unknown qubit state.

<span id="sec-quantum-programs-intermediate-representations-and-verified-optimization-3"></span>

### 41.3 Circuit DAGs and intermediate representations

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-3).

**Section level:** core. **Required earlier sections:** [41.2](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-2), [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1).

**Learning and derivation target:** Derive a dependency graph and distinguish high-level, gate-level and target-level representations.

**Implementation and evidence target:** Construct a minimal independent IR with explicit ownership/order semantics.

<span id="sec-quantum-programs-intermediate-representations-and-verified-optimization-4"></span>

### 41.4 Lowering and reversible computation

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-4).

**Section level:** core. **Required earlier sections:** [41.3](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-3), [5.4](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4).

**Learning and derivation target:** Connect high-level expressions, ancillas, compute-use-uncompute and controlled operations.

**Implementation and evidence target:** Check a small lowering against an independent function/unitary specification.

<span id="sec-quantum-programs-intermediate-representations-and-verified-optimization-5"></span>

### 41.5 Local rewrites, commutation, and optimization

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-5).

**Section level:** core. **Required earlier sections:** [41.3](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-3), [5.8](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-8).

**Learning and derivation target:** Prove selected cancellation/commutation identities with their side conditions.

**Implementation and evidence target:** Validate passes on full small matrices and preserve invalid-rewrite counterexamples.

<span id="sec-quantum-programs-intermediate-representations-and-verified-optimization-6"></span>

### 41.6 Phase, parameters, and controlled contexts

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-6).

**Section level:** core. **Required earlier sections:** [41.5](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-5), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2), [3.2](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-2).

**Learning and derivation target:** Explain why a phase ignored for an uncontrolled operation can become observable under control; preserve symbolic parameter dependence. Differentiable-program checks are an optional extension using 23.2.

**Implementation and evidence target:** Verify a phase-sensitive controlled rewrite; compare before/after derivatives only on the explicitly prepared differentiation extension.

<span id="sec-quantum-programs-intermediate-representations-and-verified-optimization-7"></span>

### 41.7 Channels, measurements, and dynamic programs

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-7).

**Section level:** core. **Required earlier sections:** [41.2](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-2), [9.7](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-7).

**Learning and derivation target:** Define transformation correctness for conditional branches and ignored records.

**Implementation and evidence target:** Compare branch probabilities and conditional maps rather than only a final statevector.

<span id="sec-quantum-programs-intermediate-representations-and-verified-optimization-8"></span>

### 41.8 Interchange, export, and capability boundaries

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-8).

**Section level:** core. **Required earlier sections:** [41.2](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-2), [41.3](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-3).

**Learning and derivation target:** Explain OpenQASM/QIR-style representation goals without assuming lossless universal interchange.

**Implementation and evidence target:** Round-trip an explicitly supported subset and report rejected or unsupported semantics.

<span id="sec-quantum-programs-intermediate-representations-and-verified-optimization-9"></span>

### 41.9 A minimal verified compiler laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-9).

**Section level:** core. **Required earlier sections:** [41.3](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-3), [41.4](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-4), [41.5](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-5), [41.6](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-6).

**Learning and derivation target:** Build a small pass pipeline with preconditions, provenance and an exact reference.

**Implementation and evidence target:** Check each pass independently and preserve a reproducer for a failing optimization.

<span id="ch-gate-synthesis-qubit-mapping-routing-and-scheduling"></span>

## Chapter 42

**Gate Synthesis, Qubit Mapping, Routing, and Scheduling**

**Reading level:** Core systems route with advanced extensions. **Entry guidance:** 5, 41 and an explicit target contract defined here; physical-platform details and logical synthesis are optional branches.

<span id="sec-gate-synthesis-qubit-mapping-routing-and-scheduling-1"></span>

### 42.1 Target models and native-operation contracts

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-1).

**Section level:** core. **Required earlier sections:** [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Learning and derivation target:** Specify operation families, parameters, connectivity, directionality, durations and simultaneous-use constraints.

**Implementation and evidence target:** Validate a small target description against hand-checked legal/illegal operations.

<span id="sec-gate-synthesis-qubit-mapping-routing-and-scheduling-2"></span>

### 42.2 Single-qubit synthesis

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-2).

**Section level:** core. **Required earlier sections:** [3.6](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-6), [5.5](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-5), [42.1](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-1).

**Learning and derivation target:** Derive a chosen Euler/basis decomposition and an approximation contract where needed.

**Implementation and evidence target:** Compare complete unitaries up to the allowed phase with declared synthesis error.

<span id="sec-gate-synthesis-qubit-mapping-routing-and-scheduling-3"></span>

### 42.3 Two-qubit and multi-qubit synthesis

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-3).

**Section level:** core. **Required earlier sections:** [5.6](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-6), [42.1](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-1).

**Learning and derivation target:** Derive a selected native-entangler decomposition and state ancilla/control assumptions.

**Implementation and evidence target:** Check an asymmetric test gate and report exact elementary costs.

<span id="sec-gate-synthesis-qubit-mapping-routing-and-scheduling-4"></span>

### 42.4 Approximate synthesis and logical gate sets [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-4).

**Section level:** advanced. **Required earlier sections:** [42.2](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-2), [32.6](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-6).

**Learning and derivation target:** Connect rotation precision, Clifford+T representations and error budgets from Chapter 33.

**Implementation and evidence target:** Compare achieved error and T/resource cost without claiming optimal synthesis.

<span id="sec-gate-synthesis-qubit-mapping-routing-and-scheduling-5"></span>

### 42.5 Initial logical-to-physical placement

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-5).

**Section level:** core. **Required earlier sections:** [4.5](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-5), [42.1](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-1).

**Learning and derivation target:** Formulate a placement objective on an explicit interaction/target model.

**Implementation and evidence target:** Compare a heuristic with exhaustive optimal placement on tiny instances.

<span id="sec-gate-synthesis-qubit-mapping-routing-and-scheduling-6"></span>

### 42.6 Routing and changing qubit mappings

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-6).

**Section level:** core. **Required earlier sections:** [42.5](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-5), [4.5](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-5).

**Learning and derivation target:** Derive a SWAP/transport routing step and track the evolving mapping.

**Implementation and evidence target:** Verify the final logical action with explicit input/output permutations.

<span id="sec-gate-synthesis-qubit-mapping-routing-and-scheduling-7"></span>

### 42.7 Routing search and heuristic limits

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-7).

**Section level:** core. **Required earlier sections:** [42.6](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-6).

**Learning and derivation target:** Explain a selected look-ahead/bidirectional heuristic and its cost function.

**Implementation and evidence target:** Compare it against exact small-instance search; do not infer global optimality.

<span id="sec-gate-synthesis-qubit-mapping-routing-and-scheduling-8"></span>

### 42.8 Scheduling with timing and shared resources

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-8).

**Section level:** core. **Required earlier sections:** [41.3](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-3), [42.1](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-1).

**Learning and derivation target:** Derive dependencies, precedence, latency and concurrency constraints.

**Implementation and evidence target:** Check a schedule for feasibility and compare makespan with a tiny exact baseline.

<span id="sec-gate-synthesis-qubit-mapping-routing-and-scheduling-9"></span>

### 42.9 Joint objectives and error-aware compilation

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-9).

**Section level:** core. **Required earlier sections:** [42.3](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-3), [42.6](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-6), [42.8](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-8).

**Learning and derivation target:** Separate gate count, depth, duration, error proxies and measurement/postprocessing costs.

**Implementation and evidence target:** Show a counterexample where fewer gates do not improve the declared workload objective.

<span id="sec-gate-synthesis-qubit-mapping-routing-and-scheduling-10"></span>

### 42.10 Mapping-and-scheduling laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-10).

**Section level:** core. **Required earlier sections:** [42.3](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-3), [42.6](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-6), [42.8](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-8), [42.9](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-9), [41.5](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-5).

**Learning and derivation target:** Compile one logical task to at least two explicitly specified targets.

**Implementation and evidence target:** Report semantic equivalence, output mapping, legality, resource counts and all target assumptions.

<span id="ch-control-level-lowering-dynamic-execution-and-logical-compilation"></span>

## Chapter 43

**Control-Level Lowering, Dynamic Execution, and Logical Compilation**

**Reading level:** Advanced systems route. **Entry guidance:** Branch-specific: control uses selected 19/23/28/34; dynamic execution uses measurement and program semantics; logical lowering uses 32–33.

<span id="sec-control-level-lowering-dynamic-execution-and-logical-compilation-1"></span>

### 43.1 From native gates to control Hamiltonians

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-1).

**Section level:** advanced. **Required earlier sections:** [34.3](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-3), [42.1](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-1).

**Learning and derivation target:** Specify control amplitude, phase, frames, timing and a target transformation.

**Implementation and evidence target:** Compare an effective control model with a native-gate reference.

<span id="sec-control-level-lowering-dynamic-execution-and-logical-compilation-2"></span>

### 43.2 Pulse shaping and constrained optimization

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-2).

**Section level:** advanced. **Required earlier sections:** [43.1](../section-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-1), [23.2](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-2), [24.3](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-3).

**Learning and derivation target:** Derive a scoped control objective/gradient and state amplitude/bandwidth constraints.

**Implementation and evidence target:** Optimize a tiny model with independent evolution/gradient checks and report model sensitivity.

<span id="sec-control-level-lowering-dynamic-execution-and-logical-compilation-3"></span>

### 43.3 Frames, virtual operations, and calibration

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-3).

**Section level:** advanced. **Required earlier sections:** [43.1](../section-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-1), [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5).

**Learning and derivation target:** Derive a frame update and distinguish a mathematical operation from a calibration-dependent implementation.

**Implementation and evidence target:** Check phase-consistent composed controls and record calibration provenance.

<span id="sec-control-level-lowering-dynamic-execution-and-logical-compilation-4"></span>

### 43.4 Crosstalk, leakage, and robust control

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-4).

**Section level:** advanced. **Required earlier sections:** [43.1](../section-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-1), [28.2](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-2), [34.6](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-6).

**Learning and derivation target:** State selected uncertainty/spectator models and robust objective assumptions.

**Implementation and evidence target:** Compare nominal and perturbed models and identify unmodeled limitations.

<span id="sec-control-level-lowering-dynamic-execution-and-logical-compilation-5"></span>
<span id="435-dynamic-circuits-and-feed-forward-latency"></span>

### 43.5 Near-device feedback, decoding, and dynamic execution

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-5).

**Section level:** advanced. **Required earlier sections:** [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [41.2](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-2), [41.7](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-7).

**Learning and derivation target:** Derive measurement-to-classical-decision-to-operation dependencies for dynamic circuits and decoder/Pauli-frame feedback; distinguish a host outer loop from a bounded-latency local controller.

**Implementation and evidence target:** Compare exact branch maps and measured-outcome records; validate a declared latency/resource schedule and report unsupported controller operations.

<span id="sec-control-level-lowering-dynamic-execution-and-logical-compilation-6"></span>

### 43.6 Lowering analog and measurement-based programs

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-6).

**Section level:** advanced. **Required earlier sections:** [34.5](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-5), [42.1](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-1).

**Learning and derivation target:** Specify an analog-control or resource-state target instead of forcing every program into a SWAP-only gate model.

**Implementation and evidence target:** Verify one constrained Hamiltonian schedule or adaptive measurement pattern.

<span id="sec-control-level-lowering-dynamic-execution-and-logical-compilation-7"></span>

### 43.7 Fault-tolerant logical compilation

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-7).

**Section level:** advanced. **Required earlier sections:** [32.5](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-5), [32.7](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-7), [33.2](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-2), [42.4](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-4).

**Learning and derivation target:** Connect T/Clifford synthesis, Pauli frames, distillation and logical-operation scheduling.

**Implementation and evidence target:** Check an explicitly scoped logical lowering with Chapter 33 resource accounting.

<span id="sec-control-level-lowering-dynamic-execution-and-logical-compilation-8"></span>

### 43.8 Cross-layer verification and approximate equivalence

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-8).

**Section level:** advanced. **Required earlier sections:** [41.5](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-5), [42.3](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-3), [43.1](../section-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-1), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Learning and derivation target:** Compose pass, synthesis, control and output-interpretation error contracts.

**Implementation and evidence target:** Check a complete tiny pipeline and distinguish exact semantic equivalence from model-dependent noisy performance.

<span id="sec-hybrid-heterogeneous-runtime"></span>

### 43.9 CPU/GPU/QPU workflows and runtime orchestration

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-hybrid-heterogeneous-runtime).

**Section level:** advanced. **Required earlier sections:** [14.7](../section-plans/03-algorithms.md#sec-hybrid-interaction-map), [41.2](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-2), [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Learning and derivation target:** Specify task graphs, asynchronous execution, parameter binding/batching, checkpointing, result types and failure/retry semantics; distinguish a real QPU from GPU simulation.

**Implementation and evidence target:** Validate a small host/device workflow with an independent local reference and typed records; report queue/communication/device/classical time and keep in-execution feedback separate.

<span id="sec-control-level-lowering-dynamic-execution-and-logical-compilation-9"></span>
<span id="439-hardware-aware-compilation-laboratory"></span>

### 43.10 Hardware-aware compilation laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-9).

**Section level:** advanced. **Required earlier sections:** [42.10](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-10), [43.3](../section-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-3), [43.4](../section-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-4), [43.8](../section-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-8), [43.9](../section-plans/quantum-compilation.md#sec-hybrid-heterogeneous-runtime).

**Learning and derivation target:** Compile a selected task through IR, placement/routing, schedule and one control/logical target.

**Implementation and evidence target:** Publish pass records, calibration/model assumptions, output maps, independent checks and capability gaps.
