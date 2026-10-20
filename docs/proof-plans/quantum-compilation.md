# Result and proof plan: Quantum Programming, Compilation, and Control

[Depth definitions](../proof-plan.md#proof-depth-contract) · [Source catalogue](../references/proof-sources.md) · [Volume plan](../volume-plan.md)

Authoring specifications only. No result/proof/API is certified by this plan. F/M/R have different scope; imported results are the exact prerequisite sections linked below.

## Chapter 41: Quantum Programs, Intermediate Representations, and Verified Optimization

<span id="sec-quantum-programs-intermediate-representations-and-verified-optimization-1"></span>

### 41.1 What a quantum compiler must preserve

**Core result / role:** Compiler correctness is contextual semantic preservation.

**Assumptions and scope:** Declared unitary/channel/instrument task and output map.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Specify exact versus approximate equivalence including phase-sensitive controlled contexts.

**Imported earlier results:** [4.3](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-3), [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1).

**Exact source targets:** [OQ3:6.1](../references/proof-sources.md#source-oq3-6-1): Section 6.1 Target-independent compilation phase.

**Independent evidence target:** Compare equivalent states, channels and distributions and explain which equality a pass must satisfy.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-programs-intermediate-representations-and-verified-optimization-2"></span>

### 41.2 Programs, types, and quantum-classical control

**Core result / role:** Typed quantum-classical programs and state lifetime.

**Assumptions and scope:** Explicit register types, branches and controller model.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Define allowed data/control dependencies and prevent use of unavailable amplitudes.

**Imported earlier results:** [41.1](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-1), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2).

**Exact source targets:** [OQ3:4.4](../references/proof-sources.md#source-oq3-4-4): Section 4.4 Real-time classical computing.

**Independent evidence target:** Represent a tiny hybrid program and diagnose an invalid use of a measured value or unknown qubit state.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-programs-intermediate-representations-and-verified-optimization-3"></span>

### 41.3 Circuit DAGs and intermediate representations

**Core result / role:** Circuit DAG dependency invariant.

**Assumptions and scope:** Finite program and declared commutation/resource relation.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove that legal topological reorderings preserve the selected semantics.

**Imported earlier results:** [41.2](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-2), [5.1](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1).

**Exact source targets:** [MLIR:IR](../references/proof-sources.md#source-mlir-ir): Multi-level IR and transformation pipeline descriptions.

**Independent evidence target:** Construct a minimal independent IR with explicit ownership/order semantics.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-programs-intermediate-representations-and-verified-optimization-4"></span>

### 41.4 Lowering and reversible computation

**Core result / role:** Correct lowering composes local semantic identities.

**Assumptions and scope:** Each lowered operation satisfies its interface/ancilla contract.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove compositional correctness and track workspace cleanup.

**Imported earlier results:** [41.3](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-3), [5.4](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4).

**Exact source targets:** [NC:3.2.5](../references/proof-sources.md#source-nc-3-2-5): Section 3.2.5 Energy and computation; [OQ3:6.1](../references/proof-sources.md#source-oq3-6-1): Section 6.1 Target-independent compilation phase.

**Independent evidence target:** Check a small lowering against an independent function/unitary specification.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-programs-intermediate-representations-and-verified-optimization-5"></span>

### 41.5 Local rewrites, commutation, and optimization

**Core result / role:** A verified local rewrite set.

**Assumptions and scope:** Matched support, parameter and side-effect preconditions.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove each rewrite and exhibit counterexamples when its preconditions are removed.

**Imported earlier results:** [41.3](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-3), [5.8](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-8).

**Exact source targets:** [NC:4.2](../references/proof-sources.md#source-nc-4-2): Section 4.2 Single qubit operations; [NC:4.3](../references/proof-sources.md#source-nc-4-3): Section 4.3 Controlled operations.

**Independent evidence target:** Validate passes on full small matrices and preserve invalid-rewrite counterexamples.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-programs-intermediate-representations-and-verified-optimization-6"></span>

### 41.6 Phase, parameters, and controlled contexts

**Core result / role:** Global phase and symbolic parameters under control.

**Assumptions and scope:** Exact parameter domains and controlled contexts.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove phase-sensitive identities; make derivative preservation an optional prepared extension.

**Imported earlier results:** [41.5](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-5), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2), [3.2](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-2).

**Exact source targets:** [NC:4.3](../references/proof-sources.md#source-nc-4-3): Section 4.3 Controlled operations; [OQ3:4.2](../references/proof-sources.md#source-oq3-4-2): Section 4.2 Gate modifiers.

**Independent evidence target:** Verify a phase-sensitive controlled rewrite; compare before/after derivatives only on the explicitly prepared differentiation extension.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-programs-intermediate-representations-and-verified-optimization-7"></span>

### 41.7 Channels, measurements, and dynamic programs

**Core result / role:** Dynamic-program equivalence retains classical records.

**Assumptions and scope:** Finite branching instrument with explicit outcome labels.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive branch maps and prove the selected record-preserving equality.

**Imported earlier results:** [41.2](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-2), [9.7](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-7).

**Exact source targets:** [TQI:2.3.2](../references/proof-sources.md#source-tqi-2-3-2): Section 2.3.2 Basic notions concerning measurements; [OQ3:4.3](../references/proof-sources.md#source-oq3-4-3): Section 4.3 Non-unitary operations.

**Independent evidence target:** Compare branch probabilities and conditional maps rather than only a final statevector.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-programs-intermediate-representations-and-verified-optimization-8"></span>

### 41.8 Interchange, export, and capability boundaries

**Core result / role:** Interchange preserves only a declared supported subset.

**Assumptions and scope:** Pinned representation and explicit unsupported features.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Define round-trip success and failures; a paper's language semantics do not prove FlagQuantum support.

**Imported earlier results:** [41.2](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-2), [41.3](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-3).

**Exact source targets:** [OQ3:6.1](../references/proof-sources.md#source-oq3-6-1): Section 6.1 Target-independent compilation phase; [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Round-trip an explicitly supported subset and report rejected or unsupported semantics.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-programs-intermediate-representations-and-verified-optimization-9"></span>

### 41.9 A minimal verified compiler laboratory

**Core result / role:** Compiler acceptance protocol.

**Assumptions and scope:** Independent dense branch semantics and negative cases.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Verify every pass, output map, symbolic domain and unsupported-feature diagnostic.

**Imported earlier results:** [41.3](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-3), [41.4](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-4), [41.5](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-5), [41.6](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-6).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Check each pass independently and preserve a reproducer for a failing optimization.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 42: Gate Synthesis, Qubit Mapping, Routing, and Scheduling

<span id="sec-gate-synthesis-qubit-mapping-routing-and-scheduling-1"></span>

### 42.1 Target models and native-operation contracts

**Core result / role:** Native-operation target contract.

**Assumptions and scope:** Explicit connectivity, direction, duration and resource exclusions.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Define legal programs and output interpretation without requiring microscopic hardware derivations.

**Imported earlier results:** [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Exact source targets:** [OQ3:5.1](../references/proof-sources.md#source-oq3-5-1): Section 5.1 Timing and optimization.

**Independent evidence target:** Validate a small target description against hand-checked legal/illegal operations.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-gate-synthesis-qubit-mapping-routing-and-scheduling-2"></span>

### 42.2 Single-qubit synthesis

**Core result / role:** Single-qubit Euler/native-basis synthesis.

**Assumptions and scope:** Chosen continuous native rotations and phase convention.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive a constructive decomposition and handle degenerate angles.

**Imported earlier results:** [3.6](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-6), [5.5](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-5), [42.1](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-1).

**Exact source targets:** [NC:4.2](../references/proof-sources.md#source-nc-4-2): Section 4.2 Single qubit operations.

**Independent evidence target:** Compare complete unitaries up to the allowed phase with declared synthesis error.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-gate-synthesis-qubit-mapping-routing-and-scheduling-3"></span>

### 42.3 Two-qubit and multi-qubit synthesis

**Core result / role:** Selected entangler-based multi-qubit synthesis.

**Assumptions and scope:** Declared native entangler, ancillas and allowed rotations.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Apply two-level/QR elimination to a specified four-by-four unitary; reuse the universality result from 5.5, synthesize each selected block and count the chosen native/ancilla costs.

**Imported earlier results:** [5.6](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-6), [42.1](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-1).

**Exact source targets:** [NC:4.5.1](../references/proof-sources.md#source-nc-4-5-1): Section 4.5.1 Two-level unitary gates are universal; [SYNTH:general](../references/proof-sources.md#source-synth-general): Section 8 Efficient general gate constructions; two-level elimination synthesis.

**Independent evidence target:** Check an asymmetric test gate and report exact elementary costs.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-gate-synthesis-qubit-mapping-routing-and-scheduling-4"></span>

### 42.4 Approximate synthesis and logical gate sets [Advanced]

**Core result / role:** Clifford+T approximation with a stated algorithm.

**Assumptions and scope:** Specified number-theoretic assumptions, accuracy and gate set.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Derive a small exact example; state the selected synthesis guarantee and defer number-theoretic lemmas.

**Imported earlier results:** [42.2](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-2), [32.6](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-6).

**Exact source targets:** [ROSS:synthesis](../references/proof-sources.md#source-ross-synthesis): Sections 7-8: approximate synthesis algorithm and its analysis.

**Independent evidence target:** Compare achieved error and T/resource cost without claiming optimal synthesis.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local advanced bridge to supply:** Clifford+T ring arithmetic, Diophantine feasibility and epsilon operator error.

**Explicitly deferred proof ingredients:** Ross-Selinger number-theoretic search/runtime lemmas and their conditional assumptions; Sections 7–8; the small exact case is local.

<span id="sec-gate-synthesis-qubit-mapping-routing-and-scheduling-5"></span>

### 42.5 Initial logical-to-physical placement

**Core result / role:** Placement is an explicit graph objective.

**Assumptions and scope:** Logical interaction and target graphs; fixed cost proxy.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Define the optimization problem and give a finite exact comparator.

**Imported earlier results:** [4.5](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-5), [42.1](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-1).

**Exact source targets:** [SABRE:mapping](../references/proof-sources.md#source-sabre-mapping): Section III A-B mapping problem/objectives.

**Independent evidence target:** Compare a heuristic with exhaustive optimal placement on tiny instances.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-gate-synthesis-qubit-mapping-routing-and-scheduling-6"></span>

### 42.6 Routing and changing qubit mappings

**Core result / role:** Routing maintains a logical-to-physical permutation invariant.

**Assumptions and scope:** Explicit SWAP/transport semantics and output map.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove the invariant after each routing step and derive final result relabeling.

**Imported earlier results:** [42.5](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-5), [4.5](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-5).

**Exact source targets:** [SABRE:mapping](../references/proof-sources.md#source-sabre-mapping): Section III A-B mapping problem/objectives; [NC:4.3](../references/proof-sources.md#source-nc-4-3): Section 4.3 Controlled operations.

**Independent evidence target:** Verify the final logical action with explicit input/output permutations.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-gate-synthesis-qubit-mapping-routing-and-scheduling-7"></span>

### 42.7 Routing search and heuristic limits

**Core result / role:** SABRE-style heuristic preserves feasibility, not optimality.

**Assumptions and scope:** Declared search/look-ahead objective and tie breaking.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive a small run and compare with exact search; no global-optimality theorem.

**Imported earlier results:** [42.6](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-6).

**Exact source targets:** [SABRE:heuristic](../references/proof-sources.md#source-sabre-heuristic): Section IV B-D SWAP heuristic and look-ahead cost.

**Independent evidence target:** Compare it against exact small-instance search; do not infer global optimality.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-gate-synthesis-qubit-mapping-routing-and-scheduling-8"></span>

### 42.8 Scheduling with timing and shared resources

**Core result / role:** Scheduling obeys precedence and shared-resource constraints.

**Assumptions and scope:** Nonnegative durations and explicit exclusion model.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove feasibility of the selected schedule and derive lower bounds; do not claim an optimal general scheduler.

**Imported earlier results:** [41.3](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-3), [42.1](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-1).

**Exact source targets:** [OQ3:5.1](../references/proof-sources.md#source-oq3-5-1): Section 5.1 Timing and optimization; [OQ3:5.3](../references/proof-sources.md#source-oq3-5-3): Section 5.3 Solving the stretch problem.

**Independent evidence target:** Check a schedule for feasibility and compare makespan with a tiny exact baseline.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-gate-synthesis-qubit-mapping-routing-and-scheduling-9"></span>

### 42.9 Joint objectives and error-aware compilation

**Core result / role:** Compiler objectives encode different tasks.

**Assumptions and scope:** Specified error proxy and duration/gate-count model.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive one tradeoff/counterexample; distinguish a proxy from measured success probability.

**Imported earlier results:** [42.3](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-3), [42.6](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-6), [42.8](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-8).

**Exact source targets:** [SABRE:heuristic](../references/proof-sources.md#source-sabre-heuristic): Section IV B-D SWAP heuristic and look-ahead cost; [OQ3:5.1](../references/proof-sources.md#source-oq3-5-1): Section 5.1 Timing and optimization.

**Independent evidence target:** Show a counterexample where fewer gates do not improve the declared workload objective.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-gate-synthesis-qubit-mapping-routing-and-scheduling-10"></span>

### 42.10 Mapping-and-scheduling laboratory

**Core result / role:** Mapping/scheduling acceptance protocol.

**Assumptions and scope:** At least two explicit targets and independent semantics.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Check legality, mapping, timing, objective values and output interpretation.

**Imported earlier results:** [42.3](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-3), [42.6](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-6), [42.8](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-8), [42.9](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-9), [41.5](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-5).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Report semantic equivalence, output mapping, legality, resource counts and all target assumptions.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 43: Control-Level Lowering, Dynamic Execution, and Logical Compilation

<span id="sec-control-level-lowering-dynamic-execution-and-logical-compilation-1"></span>

### 43.1 From native gates to control Hamiltonians

**Core result / role:** Control Hamiltonians implement native gates in a stated frame.

**Assumptions and scope:** Selected platform model and approximation regime.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive the gate-control map and separate ideal/projected from multilevel action.

**Imported earlier results:** [34.3](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-3), [42.1](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-1).

**Exact source targets:** [SC:IV.D](../references/proof-sources.md#source-sc-iv-d): Section IV D Single-qubit gates; [OQ3:5.2](../references/proof-sources.md#source-oq3-5-2): Section 5.2 Calibrating quantum instructions.

**Independent evidence target:** Compare an effective control model with a native-gate reference.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-control-level-lowering-dynamic-execution-and-logical-compilation-2"></span>

### 43.2 Pulse shaping and constrained optimization

**Core result / role:** Piecewise-control gradient and constrained update.

**Assumptions and scope:** Finite discretization and differentiable propagators; explicit control bounds.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the exact product derivative or state the exponential-derivative approximation; no general convergence claim.

**Imported earlier results:** [43.1](../section-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-1), [23.2](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-2), [24.3](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-3).

**Exact source targets:** [ADJ:2.2](../references/proof-sources.md#source-adj-2-2): Section 2.2 Derivation; [CVX:9.3](../references/proof-sources.md#source-cvx-9-3): Section 9.3 Gradient descent method.

**Independent evidence target:** Optimize a tiny model with independent evolution/gradient checks and report model sensitivity.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-control-level-lowering-dynamic-execution-and-logical-compilation-3"></span>

### 43.3 Frames, virtual operations, and calibration

**Core result / role:** Frame updates and calibration alter operation interpretation.

**Assumptions and scope:** Declared physical/virtual frame and calibrated phase convention.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive conjugation and tracked phase updates; expose stale-calibration failure.

**Imported earlier results:** [43.1](../section-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-1), [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5).

**Exact source targets:** [SC:IV.D](../references/proof-sources.md#source-sc-iv-d): Section IV D Single-qubit gates; [OQ3:5.2](../references/proof-sources.md#source-oq3-5-2): Section 5.2 Calibrating quantum instructions.

**Independent evidence target:** Check phase-consistent composed controls and record calibration provenance.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-control-level-lowering-dynamic-execution-and-logical-compilation-4"></span>

### 43.4 Crosstalk, leakage, and robust control

**Core result / role:** Robust-control objective is an ensemble/model approximation.

**Assumptions and scope:** Explicit drift/crosstalk/leakage ensemble and truncation.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive the average/worst-case objective and a finite sensitivity calculation.

**Imported earlier results:** [43.1](../section-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-1), [28.2](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-2), [34.6](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-6).

**Exact source targets:** [SC:III.B](../references/proof-sources.md#source-sc-iii-b): Section III B Modeling noise and decoherence; [SC:IV.H](../references/proof-sources.md#source-sc-iv-h): Section IV H Gate implementations with tunable coupling.

**Independent evidence target:** Compare nominal and perturbed models and identify unmodeled limitations.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-control-level-lowering-dynamic-execution-and-logical-compilation-5"></span>

### 43.5 Near-device feedback, decoding, and dynamic execution

**Core result / role:** Conditional controller execution has semantic and latency constraints.

**Assumptions and scope:** Finite branch maps, specified decoder/controller and state lifetime.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the record/frame update and prove ideal branch correctness; treat latency feasibility as an engineering constraint.

**Imported earlier results:** [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [41.2](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-2), [41.7](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-7).

**Exact source targets:** [OQ3:2.4](../references/proof-sources.md#source-oq3-2-4): Section 2.4 Execution model; [OQ3:4.4](../references/proof-sources.md#source-oq3-4-4): Section 4.4 Real-time classical computing.

**Independent evidence target:** Compare exact branch maps and measured-outcome records; validate a declared latency/resource schedule and report unsupported controller operations.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-control-level-lowering-dynamic-execution-and-logical-compilation-6"></span>

### 43.6 Lowering analog and measurement-based programs

**Core result / role:** Analog/measurement-based lowering preserves a selected task.

**Assumptions and scope:** Declared model, adaptive corrections and approximation budget.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive one lowering contract rather than asserting universal cross-model efficiency.

**Imported earlier results:** [34.5](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-5), [42.1](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-1).

**Exact source targets:** [MBQC:pattern](../references/proof-sources.md#source-mbqc-pattern): Computation by adaptive one-qubit measurements and byproduct operators; [ATOM:4.2](../references/proof-sources.md#source-atom-4-2): Section 4.2 Hamiltonian control over the device.

**Independent evidence target:** Verify one constrained Hamiltonian schedule or adaptive measurement pattern.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-control-level-lowering-dynamic-execution-and-logical-compilation-7"></span>

### 43.7 Fault-tolerant logical compilation

**Core result / role:** Logical lowering preserves operation and error contracts.

**Assumptions and scope:** Specified code, gadgets, synthesis and factory assumptions.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Compose correctness/error bounds and resource schedules; delimit hardware estimates.

**Imported earlier results:** [32.5](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-5), [32.7](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-7), [33.2](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-2), [42.4](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-4).

**Exact source targets:** [RESOURCE:surgery](../references/proof-sources.md#source-resource-surgery): Patch operations and Section 1.1 Pauli product measurements; [RESOURCE:cost](../references/proof-sources.md#source-resource-cost): Section 4 tradeoffs, especially 4.3 distance selection, and Section 5.

**Independent evidence target:** Check an explicitly scoped logical lowering with Chapter 33 resource accounting.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-control-level-lowering-dynamic-execution-and-logical-compilation-8"></span>

### 43.8 Cross-layer verification and approximate equivalence

**Core result / role:** Cross-layer error bounds require matched metrics.

**Assumptions and scope:** Specified norms, encodings and observation maps.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove a selected triangle/telescoping bound and identify model versus numerical errors.

**Imported earlier results:** [41.5](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-5), [42.3](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-3), [43.1](../section-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-1), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Exact source targets:** [TQI:1.1.3](../references/proof-sources.md#source-tqi-1-1-3): Section 1.1.3 Operator decompositions and norms; [TQI:3.3.3](../references/proof-sources.md#source-tqi-3-3-3): Section 3.3.3 Distances between channels.

**Independent evidence target:** Check a complete tiny pipeline and distinguish exact semantic equivalence from model-dependent noisy performance.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-hybrid-heterogeneous-runtime"></span>

### 43.9 CPU/GPU/QPU workflows and runtime orchestration

**Core result / role:** Heterogeneous workflow correctness is a dataflow contract.

**Assumptions and scope:** Explicit task dependencies, records, retries and state lifetime.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Specify idempotent job boundaries and total cost; no scheduler-speedup theorem.

**Imported earlier results:** [14.7](../section-plans/03-algorithms.md#sec-hybrid-interaction-map), [41.2](../section-plans/quantum-compilation.md#sec-quantum-programs-intermediate-representations-and-verified-optimization-2), [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Exact source targets:** [OQ3:2.4](../references/proof-sources.md#source-oq3-2-4): Section 2.4 Execution model; [REPRO:software](../references/proof-sources.md#source-repro-software): Section 2 Software.

**Independent evidence target:** Validate a small host/device workflow with an independent local reference and typed records; report queue/communication/device/classical time and keep in-execution feedback separate.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-control-level-lowering-dynamic-execution-and-logical-compilation-9"></span>

### 43.10 Hardware-aware compilation laboratory

**Core result / role:** Cross-layer compiler acceptance protocol.

**Assumptions and scope:** One complete task and independent physical/logical references.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Validate every boundary with units, phases, branches, timing and error budget.

**Imported earlier results:** [42.10](../section-plans/quantum-compilation.md#sec-gate-synthesis-qubit-mapping-routing-and-scheduling-10), [43.3](../section-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-3), [43.4](../section-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-4), [43.8](../section-plans/quantum-compilation.md#sec-control-level-lowering-dynamic-execution-and-logical-compilation-8), [43.9](../section-plans/quantum-compilation.md#sec-hybrid-heterogeneous-runtime).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Publish pass records, calibration/model assumptions, output maps, independent checks and capability gaps.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.
