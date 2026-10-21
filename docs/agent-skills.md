# Agent skills: capability levels and chapter map

**Plan 0.1 · October 21, 2026 · first prototype pilot.** Generated from `book/agent-skills-plan.json`. This catalog contains 23 proposed task skills; four have independent-agent-tested prototypes: state/operator comparison 0.1.1, single-qubit interference 0.1.0, phase-tracked unitary evolution 0.1.0 and complex linear algebra 0.1.0. Their separate evidence records retain failures, author execution and blind-task outcomes. Scientific acceptance remains pending. Zero skills are released. It does not assert existing FlagQuantum support for planned topics.

[Dual-entry design](dual-entry.md) · [Skill contract](skill-contract.md) · [Paper verification and acceptance](paper-reproduction-standard.md)

## Capability levels

Levels describe increasing task composition and evaluation scope. They do not replace the textbook P/F/M/R/V proof-depth codes, its prerequisite graph, or evidence-based competence in a domain. An L5 router does not certify every L2 workflow.

| Level | Capability | Required evidence |
|---|---|---|
| L0: Scope and claim decomposition | Turn a paper or request into a bounded claim ledger, artifact inventory and feasibility decision. | Correctly separate theorem, algorithm, numerical, performance and hardware claims; identify missing premises without claiming execution. |
| L1: Formula-to-code building blocks | Translate a specified finite mathematical object under explicit conventions. | Independent references, shape/unit/phase/order checks, boundary cases and intentional failure witnesses. |
| L2: Verified domain workflows | Compose blocks into an algorithm, model, compiler, inference or simulation workflow. | Task-level correctness/error/resource contracts, supported-release execution and negative/transfer cases. |
| L3: Scoped paper-claim reproduction | Reproduce an explicitly selected equation, table, figure or experiment claim. | Predeclared target and scope; traceable inputs; claim-appropriate reference and discrepancy analysis. |
| L4: Integrated paper reproduction | Coordinate the registered claim set, dependencies, artifacts and aggregate evidence. | Every mandatory claim has a justified disposition; clean rerun, independent evaluation and signed review decisions. |
| L5: Transfer to previously unseen papers | Route held-out papers across domains and handle unsupported requirements explicitly. | Held-out transfer evaluation with per-domain outcomes, bounded resource use, honest blocking and no unsupported success claims. |

## Complete chapter-to-skill mapping

All **50 chapters and 435 sections** have one primary task-family assignment in the JSON catalog. Current source states: 22 drafts, 413 not started, 0 accepted. A draft with checked examples is useful prototype evidence, not a released skill.

The primary owner is an editorial responsibility, not exclusive use or a claim that every section already implements the task. Support references and selected domain workflows create many-to-many reuse. Source links below lead to stable planning anchors; a planned section must not be presented as completed prose.

| Chapter and canonical section range | Primary task skill(s) | Source drafts / sections |
|---|---|---|
| [1. What Quantum Computing Computes](section-plans/01-foundations.md#ch-what-quantum-computing-computes) (1.1–1.6) | [scope-paper-claims](#scope-paper-claims) | 6 / 6 |
| [2. Complex Vectors, Operators, and Numerical Reasoning](section-plans/01-foundations.md#ch-complex-vectors-operators-and-numerical-reasoning) (2.1–2.8) | [translate-complex-linear-algebra](#translate-complex-linear-algebra) | 8 / 8 |
| [3. Single-Qubit States and Rotations](section-plans/01-foundations.md#ch-single-qubit-states-and-rotations) (3.1–3.7) | [compare-quantum-states-and-operators](#compare-quantum-states-and-operators); [convert-bloch-state-coordinates](#convert-bloch-state-coordinates); [reproduce-qubit-interference](#reproduce-qubit-interference); [translate-unitary-evolution](#translate-unitary-evolution) | 7 / 7 |
| [4. Composite Systems, Tensor Products, and Qubit Ordering](section-plans/01-foundations.md#ch-composite-systems-tensor-products-and-qubit-ordering) (4.1–4.8) | [translate-qubit-ordering](#translate-qubit-ordering) | 1 / 8 |
| [5. Gates, Reversible Computation, and Circuit Synthesis](section-plans/01-foundations.md#ch-gates-reversible-computation-and-circuit-synthesis) (5.1–5.8) | [build-and-check-circuits](#build-and-check-circuits) | 0 / 8 |
| [6. Measurement, Expectation Values, and Statistical Estimation](section-plans/01-foundations.md#ch-measurement-expectation-values-and-statistical-estimation) (6.1–6.9) | [measure-and-estimate-observables](#measure-and-estimate-observables) | 0 / 9 |
| [7. Entanglement and Quantum Information Protocols](section-plans/01-foundations.md#ch-entanglement-and-quantum-information-protocols) (7.1–7.9) | [model-composite-states-and-channels](#model-composite-states-and-channels) | 0 / 9 |
| [8. Density Matrices, Reduced States, and Purification](section-plans/01-foundations.md#ch-density-matrices-reduced-states-and-purification) (8.1–8.8) | [model-composite-states-and-channels](#model-composite-states-and-channels) | 0 / 8 |
| [9. Quantum Channels and Their Representations](section-plans/02-information.md#ch-quantum-channels-and-their-representations) (9.1–9.8) | [model-composite-states-and-channels](#model-composite-states-and-channels) | 0 / 8 |
| [10. Distinguishability, Fidelity, and Quantum State Inference](section-plans/02-information.md#ch-distinguishability-fidelity-and-quantum-state-inference) (10.1–10.9) | [measure-and-estimate-observables](#measure-and-estimate-observables) | 0 / 9 |
| [11. Entropy, Relative Entropy, and Information Processing](section-plans/02-information.md#ch-entropy-relative-entropy-and-information-processing) (11.1–11.8) | [audit-information-and-security-claims](#audit-information-and-security-claims) | 0 / 8 |
| [12. Compression, Entanglement, and Communication Limits](section-plans/02-information.md#ch-compression-entanglement-and-communication-limits) (12.1–12.9) | [audit-information-and-security-claims](#audit-information-and-security-claims) | 0 / 9 |
| [13. Quantum Cryptography and Security Reasoning](section-plans/02-information.md#ch-quantum-cryptography-and-security-reasoning) (13.1–13.9) | [audit-information-and-security-claims](#audit-information-and-security-claims) | 0 / 9 |
| [14. Computational Models, Complexity, and Quantum Advantage](section-plans/03-algorithms.md#ch-computational-models-complexity-and-quantum-advantage) (14.1–14.9) | [audit-algorithmic-resource-claims](#audit-algorithmic-resource-claims) | 0 / 9 |
| [15. Interference, Oracles, and Phase Kickback](section-plans/03-algorithms.md#ch-interference-oracles-and-phase-kickback) (15.1–15.8) | [implement-oracle-and-spectral-algorithms](#implement-oracle-and-spectral-algorithms) | 0 / 8 |
| [16. Grover Search, Amplitude Amplification, and Estimation](section-plans/03-algorithms.md#ch-grover-search-amplitude-amplification-and-estimation) (16.1–16.8) | [implement-oracle-and-spectral-algorithms](#implement-oracle-and-spectral-algorithms) | 0 / 8 |
| [17. Fourier Transforms and Quantum Phase Estimation](section-plans/03-algorithms.md#ch-fourier-transforms-and-quantum-phase-estimation) (17.1–17.9) | [implement-oracle-and-spectral-algorithms](#implement-oracle-and-spectral-algorithms) | 0 / 9 |
| [18. Period Finding, Factoring, and Algorithmic Arithmetic](section-plans/03-algorithms.md#ch-period-finding-factoring-and-algorithmic-arithmetic) (18.1–18.9) | [implement-oracle-and-spectral-algorithms](#implement-oracle-and-spectral-algorithms) | 0 / 9 |
| [19. Hamiltonian Simulation and Error Bounds](section-plans/03-algorithms.md#ch-hamiltonian-simulation-and-error-bounds) (19.1–19.9) | [implement-oracle-and-spectral-algorithms](#implement-oracle-and-spectral-algorithms) | 0 / 9 |
| [20. Block Encodings and Quantum Linear Algebra](section-plans/03-algorithms.md#ch-block-encodings-and-quantum-linear-algebra) (20.1–20.9) | [implement-oracle-and-spectral-algorithms](#implement-oracle-and-spectral-algorithms) | 0 / 9 |
| [21. Quantum Signal Processing and Singular Value Transformation](section-plans/03-algorithms.md#ch-quantum-signal-processing-and-singular-value-transformation) (21.1–21.9) | [implement-oracle-and-spectral-algorithms](#implement-oracle-and-spectral-algorithms) | 0 / 9 |
| [22. Quantum Walks, Lower Bounds, and Algorithm Design](section-plans/03-algorithms.md#ch-quantum-walks-lower-bounds-and-algorithm-design) (22.1–22.9) | [audit-algorithmic-resource-claims](#audit-algorithmic-resource-claims) | 0 / 9 |
| [23. Parameterized Circuits, Quantum Gradients, and Differentiation](section-plans/04-variational.md#ch-parameterized-circuits-quantum-gradients-and-differentiation) (23.1–23.10) | [train-differentiable-hybrid-models](#train-differentiable-hybrid-models) | 0 / 10 |
| [24. Optimization, Geometry, and Trainability](section-plans/04-variational.md#ch-optimization-geometry-and-trainability) (24.1–24.9) | [train-differentiable-hybrid-models](#train-differentiable-hybrid-models) | 0 / 9 |
| [25. Variational Simulation, Chemistry, and Ground-State Problems](section-plans/04-variational.md#ch-variational-simulation-chemistry-and-ground-state-problems) (25.1–25.12) | [train-differentiable-hybrid-models](#train-differentiable-hybrid-models) | 0 / 12 |
| [26. QAOA, Quantum Optimization, and Classical Comparisons](section-plans/04-variational.md#ch-qaoa-quantum-optimization-and-classical-comparisons) (26.1–26.8) | [train-differentiable-hybrid-models](#train-differentiable-hybrid-models) | 0 / 8 |
| [27. Quantum Learning, Kernels, and Hybrid Models](section-plans/04-variational.md#ch-quantum-learning-kernels-and-hybrid-models) (27.1–27.8) | [train-differentiable-hybrid-models](#train-differentiable-hybrid-models) | 0 / 8 |
| [28. Noise, Open Systems, and Error Mitigation](section-plans/05-fault-tolerance.md#ch-noise-open-systems-and-error-mitigation) (28.1–28.10) | [simulate-noise-and-mitigation](#simulate-noise-and-mitigation) | 0 / 10 |
| [29. Quantum Error Correction: Conditions and Recovery](section-plans/05-fault-tolerance.md#ch-quantum-error-correction-conditions-and-recovery) (29.1–29.9) | [reproduce-error-correction-experiments](#reproduce-error-correction-experiments) | 0 / 9 |
| [30. Stabilizer Codes, Logical Operators, and Decoding](section-plans/05-fault-tolerance.md#ch-stabilizer-codes-logical-operators-and-decoding) (30.1–30.11) | [reproduce-error-correction-experiments](#reproduce-error-correction-experiments) | 0 / 11 |
| [31. Surface Codes and Repeated Syndrome Measurements](section-plans/05-fault-tolerance.md#ch-surface-codes-and-repeated-syndrome-measurements) (31.1–31.8) | [reproduce-error-correction-experiments](#reproduce-error-correction-experiments) | 0 / 8 |
| [32. Fault-Tolerant Gates and Universal Logical Computation](section-plans/05-fault-tolerance.md#ch-fault-tolerant-gates-and-universal-logical-computation) (32.1–32.8) | [reproduce-error-correction-experiments](#reproduce-error-correction-experiments) | 0 / 8 |
| [33. From Logical Algorithms to Physical Resource Estimates](section-plans/05-fault-tolerance.md#ch-from-logical-algorithms-to-physical-resource-estimates) (33.1–33.8) | [audit-algorithmic-resource-claims](#audit-algorithmic-resource-claims) | 0 / 8 |
| [34. From Abstract Qubits to Physical Quantum Systems](section-plans/physical-platforms.md#ch-from-abstract-qubits-to-physical-quantum-systems) (34.1–34.10) | [model-physical-qubit-platforms](#model-physical-qubit-platforms) | 0 / 10 |
| [35. Superconducting Qubits and Circuit-QED Control](section-plans/physical-platforms.md#ch-superconducting-qubits-and-circuit-qed-control) (35.1–35.8) | [model-physical-qubit-platforms](#model-physical-qubit-platforms) | 0 / 8 |
| [36. Trapped-Ion Qubits, Motional Gates, and Transport](section-plans/physical-platforms.md#ch-trapped-ion-qubits-motional-gates-and-transport) (36.1–36.8) | [model-physical-qubit-platforms](#model-physical-qubit-platforms) | 0 / 8 |
| [37. Neutral-Atom Arrays and Rydberg Quantum Computing](section-plans/physical-platforms.md#ch-neutral-atom-arrays-and-rydberg-quantum-computing) (37.1–37.8) | [model-physical-qubit-platforms](#model-physical-qubit-platforms) | 0 / 8 |
| [38. Photonic Encodings, Optical Circuits, and Measurement-Based Computation](section-plans/physical-platforms.md#ch-photonic-encodings-optical-circuits-and-measurement-based-computation) (38.1–38.9) | [model-physical-qubit-platforms](#model-physical-qubit-platforms) | 0 / 9 |
| [39. Semiconductor Spin Qubits and Exchange-Based Architectures](section-plans/physical-platforms.md#ch-semiconductor-spin-qubits-and-exchange-based-architectures) (39.1–39.8) | [model-physical-qubit-platforms](#model-physical-qubit-platforms) | 0 / 8 |
| [40. Topological Quantum Computation and Candidate Physical Realizations](section-plans/physical-platforms.md#ch-topological-quantum-computation-and-candidate-physical-realizations) (40.1–40.8) | [model-physical-qubit-platforms](#model-physical-qubit-platforms) | 0 / 8 |
| [41. Quantum Programs, Intermediate Representations, and Verified Optimization](section-plans/quantum-compilation.md#ch-quantum-programs-intermediate-representations-and-verified-optimization) (41.1–41.9) | [compile-and-lower-quantum-programs](#compile-and-lower-quantum-programs) | 0 / 9 |
| [42. Gate Synthesis, Qubit Mapping, Routing, and Scheduling](section-plans/quantum-compilation.md#ch-gate-synthesis-qubit-mapping-routing-and-scheduling) (42.1–42.10) | [compile-and-lower-quantum-programs](#compile-and-lower-quantum-programs) | 0 / 10 |
| [43. Control-Level Lowering, Dynamic Execution, and Logical Compilation](section-plans/quantum-compilation.md#ch-control-level-lowering-dynamic-execution-and-logical-compilation) (43.1–43.10) | [compile-and-lower-quantum-programs](#compile-and-lower-quantum-programs) | 0 / 10 |
| [44. Exact Simulation, Tensor Execution, and Numerical Reliability](section-plans/06-simulation.md#ch-exact-simulation-tensor-execution-and-numerical-reliability) (44.1–44.8) | [select-and-validate-classical-simulators](#select-and-validate-classical-simulators) | 0 / 8 |
| [45. Stabilizer Simulation, Magic, and Classical Simulability](section-plans/06-simulation.md#ch-stabilizer-simulation-magic-and-classical-simulability) (45.1–45.8) | [select-and-validate-classical-simulators](#select-and-validate-classical-simulators) | 0 / 8 |
| [46. Matrix Product States, Entanglement, and Truncation](section-plans/06-simulation.md#ch-matrix-product-states-entanglement-and-truncation) (46.1–46.8) | [select-and-validate-classical-simulators](#select-and-validate-classical-simulators) | 0 / 8 |
| [47. Tensor Networks, Contraction, and Hybrid Simulation Strategies](section-plans/06-simulation.md#ch-tensor-networks-contraction-and-hybrid-simulation-strategies) (47.1–47.10) | [select-and-validate-classical-simulators](#select-and-validate-classical-simulators) | 0 / 10 |
| [48. Reading Papers, Building Evidence, and Reproducing Results](section-plans/07-research.md#ch-reading-papers-building-evidence-and-reproducing-results) (48.1–48.9) | [assemble-paper-reproduction](#assemble-paper-reproduction) | 0 / 9 |
| [49. Case Study: Molecular Hydrogen from Hamiltonian to Verified VQE](section-plans/07-research.md#ch-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe) (49.1–49.9) | [reproduce-molecular-vqe](#reproduce-molecular-vqe) | 0 / 9 |
| [50. Case Study: Logical Memory and Error-Correction Experiments](section-plans/07-research.md#ch-case-study-logical-memory-and-error-correction-experiments) (50.1–50.9) | [reproduce-error-correction-experiments](#reproduce-error-correction-experiments) | 0 / 9 |

## Task catalog and dependency contracts

Each proposed package must expose a bounded task/profile before implementation. Broad domain entries may be split into narrower packages after pilot evidence; this does not alter textbook chapters. Load the specific profile and mathematical references needed for a run rather than all domain material.

The declared skill graph is acyclic. A run must additionally name its selected domain profiles, direct and transitive textbook prerequisites, and concrete versions. L3–L5 orchestration may select relevant L2 skills; it must not treat an unlisted domain requirement as satisfied.

### scope-paper-claims

**L0 · planned · not run · independent acceptance pending.**

Classify claims and record feasibility, source locations, access models and missing artifacts.

**Deliverable:** Claim ledger and scoped execution proposal.

**Required task skills:** None at catalog level; this does not waive source prerequisites.

**Primary sources:** [Chapter 1, all sections](section-plans/01-foundations.md#ch-what-quantum-computing-computes)

**Support sources:** [48.1](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-1), [48.2](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-2)

### translate-complex-linear-algebra

**L1 · independent-agent-tested prototype · blind agent tasks: 12/12; author cases: 55/55 · independent acceptance pending.**

Translate complex scalar/vector/operator formulas with explicit coordinate and numerical contracts.

**Deliverable:** Indexed formulas, small independent references and checked implementation.

[Complex linear algebra prototype, numerical contracts and independent blind evaluation](complex-algebra-skill-prototype.md).

**Required task skills:** None at catalog level; this does not waive source prerequisites.

**Primary sources:** [Chapter 2, all sections](section-plans/01-foundations.md#ch-complex-vectors-operators-and-numerical-reasoning)

**Existing candidate evidence:** [complex_coordinates.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/complex_coordinates.py); [inner_products.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/inner_products.py); [basis_changes.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/basis_changes.py); [operator_classes.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/operator_classes.py); [spectral_svd.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/spectral_svd.py); [matrix_functions.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/matrix_functions.py); [conditioning.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/conditioning.py); [verification_contracts.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/verification_contracts.py); [2.1.json](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/2.1.json); [2.2.json](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/2.2.json); [2.3.json](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/2.3.json); [2.4.json](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/2.4.json); [2.5.json](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/2.5.json); [2.6.json](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/2.6.json); [2.7.json](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/2.7.json); [2.8.json](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/2.8.json). These artifacts are not a skill evaluation, an acceptance decision or a whole-paper reproduction claim.

### compare-quantum-states-and-operators

**L1 · independent-agent-tested prototype · blind agent retest: 11/11; author helper regression: 45/45 · independent acceptance pending.**

Choose state, operator or distribution comparison with the correct phase scope.

**Deliverable:** Validated comparison domain, residuals and phase-sensitive counterexamples.

[Prototype usage](comparison-skill-prototype.md) · [Independent blind evaluation and runtime repair](comparison-skill-blind-evaluation.md).

**Required task skills:** [translate-complex-linear-algebra](#translate-complex-linear-algebra)

**Primary sources:** [3.1](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-1); [3.7](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-7)

**Support sources:** [2.1](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-1), [2.2](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-2), [2.8](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-8), [3.6](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-6)

**Existing candidate evidence:** [pure_states.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/pure_states.py); [phase_contracts.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/phase_contracts.py); [3.1.json](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/3.1.json); [3.7.json](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/3.7.json). These artifacts are not a skill evaluation, an acceptance decision or a whole-paper reproduction claim.

### reproduce-qubit-interference

**L1 · independent-agent-tested prototype · blind agent tasks: 12/12; author cases: 35/35 · independent acceptance pending.**

Translate preparation, phase and analyzer formulas into a checked ideal interference experiment.

**Deliverable:** Independent amplitude/fringe references and released FlagQuantum execution.

[Interference prototype, formula-to-code contract and independent blind evaluation](interference-skill-prototype.md).

**Required task skills:** [translate-complex-linear-algebra](#translate-complex-linear-algebra), [compare-quantum-states-and-operators](#compare-quantum-states-and-operators)

**Primary sources:** [3.2](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-2)

**Support sources:** [1.2](section-plans/01-foundations.md#sec-what-quantum-computing-computes-2), [3.1](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-1)

**Existing candidate evidence:** [relative_phase.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/relative_phase.py); [3.2.json](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/3.2.json). These artifacts are not a skill evaluation, an acceptance decision or a whole-paper reproduction claim.

### convert-bloch-state-coordinates

**L1 · planned · not run · independent acceptance pending.**

Translate pure-qubit coordinates and phase charts, including poles and sign conventions.

**Deliverable:** Forward/inverse coordinate checks and explicit pure-state limits.

**Required task skills:** [translate-complex-linear-algebra](#translate-complex-linear-algebra), [compare-quantum-states-and-operators](#compare-quantum-states-and-operators)

**Primary sources:** [3.3](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-3)

**Support sources:** [3.1](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-1), [2.2](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-2), [2.3](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3)

### translate-unitary-evolution

**L1 · independent-agent-tested prototype · blind agent tasks: 12/12; author cases: 53/53 · independent acceptance pending.**

Translate fixed-generator evolution and single-qubit factorizations with units, order and common phase.

**Deliverable:** Matrix/generator/decomposition references and reconstructed circuit action.

[Unitary evolution prototype, units, phase contract and independent blind evaluation](unitary-evolution-skill-prototype.md).

**Required task skills:** [translate-complex-linear-algebra](#translate-complex-linear-algebra)

**Primary sources:** [3.4](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-4); [3.5](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5); [3.6](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-6)

**Support sources:** [2.4](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-4), [2.5](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5), [2.6](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-6), [3.1](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-1), [3.7](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-7)

**Existing candidate evidence:** [closed_evolution.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/closed_evolution.py); [composing_rotations.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/composing_rotations.py); [3.4.json](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/3.4.json); [3.6.json](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/3.6.json); [pauli_rotations.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/pauli_rotations.py); [3.5.json](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/3.5.json). These artifacts are not a skill evaluation, an acceptance decision or a whole-paper reproduction claim.

### translate-qubit-ordering

**L1 · planned · not run · independent acceptance pending.**

Translate subsystem labels, supports, permutations and basis-index conventions.

**Deliverable:** Convention record and cross-representation amplitude/operator checks.

**Required task skills:** [translate-complex-linear-algebra](#translate-complex-linear-algebra)

**Primary sources:** [Chapter 4, all sections](section-plans/01-foundations.md#ch-composite-systems-tensor-products-and-qubit-ordering)

### build-and-check-circuits

**L1 · planned · not run · independent acceptance pending.**

Build a specified circuit or reversible subroutine without changing its input/output semantics.

**Deliverable:** Checked circuit with basis/coherent tests and declared approximation.

**Required task skills:** [translate-unitary-evolution](#translate-unitary-evolution), [translate-qubit-ordering](#translate-qubit-ordering)

**Primary sources:** [Chapter 5, all sections](section-plans/01-foundations.md#ch-gates-reversible-computation-and-circuit-synthesis)

### measure-and-estimate-observables

**L2 · planned · not run · independent acceptance pending.**

Translate measurement, estimation and state-inference claims into statistical contracts.

**Deliverable:** Estimator, uncertainty protocol, independent references and finite-sample limits.

**Required task skills:** [build-and-check-circuits](#build-and-check-circuits), [compare-quantum-states-and-operators](#compare-quantum-states-and-operators)

**Primary sources:** [Chapter 6, all sections](section-plans/01-foundations.md#ch-measurement-expectation-values-and-statistical-estimation); [Chapter 10, all sections](section-plans/02-information.md#ch-distinguishability-fidelity-and-quantum-state-inference)

**Support sources:** [2.7](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7), [2.8](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-8)

### model-composite-states-and-channels

**L2 · planned · not run · independent acceptance pending.**

Model entangled/mixed states, protocols and conditional/channel maps.

**Deliverable:** Normalized physical-model checks, independent map action and correlation tests.

**Required task skills:** [translate-qubit-ordering](#translate-qubit-ordering), [build-and-check-circuits](#build-and-check-circuits)

**Primary sources:** [Chapter 7, all sections](section-plans/01-foundations.md#ch-entanglement-and-quantum-information-protocols); [Chapter 8, all sections](section-plans/01-foundations.md#ch-density-matrices-reduced-states-and-purification); [Chapter 9, all sections](section-plans/02-information.md#ch-quantum-channels-and-their-representations)

### audit-information-and-security-claims

**L2 · planned · not run · independent acceptance pending.**

Audit information/security hypotheses and scoped finite examples without inferring a theorem from samples.

**Deliverable:** Assumption/theorem ledger, proof obligations and bounded checks.

**Required task skills:** [model-composite-states-and-channels](#model-composite-states-and-channels), [measure-and-estimate-observables](#measure-and-estimate-observables)

**Primary sources:** [Chapter 11, all sections](section-plans/02-information.md#ch-entropy-relative-entropy-and-information-processing); [Chapter 12, all sections](section-plans/02-information.md#ch-compression-entanglement-and-communication-limits); [Chapter 13, all sections](section-plans/02-information.md#ch-quantum-cryptography-and-security-reasoning)

### audit-algorithmic-resource-claims

**L2 · planned · not run · independent acceptance pending.**

Check query/access/precision models, classical baselines and complete logical/physical resource accounting.

**Deliverable:** Matched-task cost ledger and explicitly conditional advantage statement.

**Required task skills:** [build-and-check-circuits](#build-and-check-circuits)

**Primary sources:** [Chapter 14, all sections](section-plans/03-algorithms.md#ch-computational-models-complexity-and-quantum-advantage); [Chapter 22, all sections](section-plans/03-algorithms.md#ch-quantum-walks-lower-bounds-and-algorithm-design); [Chapter 33, all sections](section-plans/05-fault-tolerance.md#ch-from-logical-algorithms-to-physical-resource-estimates)

**Support sources:** [6.7](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7), [48.1](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-1), [48.2](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-2), [48.3](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-3), [48.4](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-4), [48.5](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-5), [48.6](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-6), [48.7](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-7), [48.8](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-8), [48.9](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-9)

### implement-oracle-and-spectral-algorithms

**L2 · planned · not run · independent acceptance pending.**

Implement a selected oracle, arithmetic, Fourier, Hamiltonian or spectral algorithm with its access assumptions.

**Deliverable:** Tiny exact cases, algorithmic error bounds and scoped execution/resource evidence.

**Required task skills:** [build-and-check-circuits](#build-and-check-circuits), [measure-and-estimate-observables](#measure-and-estimate-observables)

**Primary sources:** [Chapter 15, all sections](section-plans/03-algorithms.md#ch-interference-oracles-and-phase-kickback); [Chapter 16, all sections](section-plans/03-algorithms.md#ch-grover-search-amplitude-amplification-and-estimation); [Chapter 17, all sections](section-plans/03-algorithms.md#ch-fourier-transforms-and-quantum-phase-estimation); [Chapter 18, all sections](section-plans/03-algorithms.md#ch-period-finding-factoring-and-algorithmic-arithmetic); [Chapter 19, all sections](section-plans/03-algorithms.md#ch-hamiltonian-simulation-and-error-bounds); [Chapter 20, all sections](section-plans/03-algorithms.md#ch-block-encodings-and-quantum-linear-algebra); [Chapter 21, all sections](section-plans/03-algorithms.md#ch-quantum-signal-processing-and-singular-value-transformation)

### train-differentiable-hybrid-models

**L2 · planned · not run · independent acceptance pending.**

Translate gradients, loss functions, optimizers, QAOA and hybrid/classical comparison protocols.

**Deliverable:** Independent derivatives, multiple-run training evidence and matched objectives/budgets.

**Required task skills:** [build-and-check-circuits](#build-and-check-circuits), [measure-and-estimate-observables](#measure-and-estimate-observables)

**Primary sources:** [Chapter 23, all sections](section-plans/04-variational.md#ch-parameterized-circuits-quantum-gradients-and-differentiation); [Chapter 24, all sections](section-plans/04-variational.md#ch-optimization-geometry-and-trainability); [Chapter 25, all sections](section-plans/04-variational.md#ch-variational-simulation-chemistry-and-ground-state-problems); [Chapter 26, all sections](section-plans/04-variational.md#ch-qaoa-quantum-optimization-and-classical-comparisons); [Chapter 27, all sections](section-plans/04-variational.md#ch-quantum-learning-kernels-and-hybrid-models)

**Support sources:** [2.7](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7), [2.8](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-8), [48.1](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-1), [48.2](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-2), [48.3](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-3), [48.4](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-4), [48.5](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-5), [48.6](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-6), [48.7](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-7), [48.8](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-8), [48.9](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-9)

### simulate-noise-and-mitigation

**L2 · planned · not run · independent acceptance pending.**

Specify channels/dynamics and mitigation assumptions with sampling and approximation costs.

**Deliverable:** Model validation, uncertainty/error budget and ideal/noisy comparisons.

**Required task skills:** [model-composite-states-and-channels](#model-composite-states-and-channels), [measure-and-estimate-observables](#measure-and-estimate-observables)

**Primary sources:** [Chapter 28, all sections](section-plans/05-fault-tolerance.md#ch-noise-open-systems-and-error-mitigation)

### reproduce-error-correction-experiments

**L2 · planned · not run · independent acceptance pending.**

Translate codes, syndrome rounds, decoders and logical operations under declared fault models.

**Deliverable:** Enumerated small faults, decoder interfaces, logical metrics and finite-size limits.

**Required task skills:** [model-composite-states-and-channels](#model-composite-states-and-channels), [simulate-noise-and-mitigation](#simulate-noise-and-mitigation)

**Primary sources:** [Chapter 29, all sections](section-plans/05-fault-tolerance.md#ch-quantum-error-correction-conditions-and-recovery); [Chapter 30, all sections](section-plans/05-fault-tolerance.md#ch-stabilizer-codes-logical-operators-and-decoding); [Chapter 31, all sections](section-plans/05-fault-tolerance.md#ch-surface-codes-and-repeated-syndrome-measurements); [Chapter 32, all sections](section-plans/05-fault-tolerance.md#ch-fault-tolerant-gates-and-universal-logical-computation); [Chapter 50, all sections](section-plans/07-research.md#ch-case-study-logical-memory-and-error-correction-experiments)

### model-physical-qubit-platforms

**L2 · planned · not run · independent acceptance pending.**

Map physical assumptions, levels/modes, controls, readout and effective models across platform routes.

**Deliverable:** Unit/frame/truncation checks and simulation-versus-device evidence distinction.

**Required task skills:** [translate-unitary-evolution](#translate-unitary-evolution), [model-composite-states-and-channels](#model-composite-states-and-channels), [simulate-noise-and-mitigation](#simulate-noise-and-mitigation)

**Primary sources:** [Chapter 34, all sections](section-plans/physical-platforms.md#ch-from-abstract-qubits-to-physical-quantum-systems); [Chapter 35, all sections](section-plans/physical-platforms.md#ch-superconducting-qubits-and-circuit-qed-control); [Chapter 36, all sections](section-plans/physical-platforms.md#ch-trapped-ion-qubits-motional-gates-and-transport); [Chapter 37, all sections](section-plans/physical-platforms.md#ch-neutral-atom-arrays-and-rydberg-quantum-computing); [Chapter 38, all sections](section-plans/physical-platforms.md#ch-photonic-encodings-optical-circuits-and-measurement-based-computation); [Chapter 39, all sections](section-plans/physical-platforms.md#ch-semiconductor-spin-qubits-and-exchange-based-architectures); [Chapter 40, all sections](section-plans/physical-platforms.md#ch-topological-quantum-computation-and-candidate-physical-realizations)

### compile-and-lower-quantum-programs

**L2 · planned · not run · independent acceptance pending.**

Transform programs through representations and target constraints while preserving declared semantics.

**Deliverable:** Equivalence/error, legality, layout, dynamic-branch and scheduling evidence.

**Required task skills:** [build-and-check-circuits](#build-and-check-circuits), [translate-qubit-ordering](#translate-qubit-ordering)

**Primary sources:** [Chapter 41, all sections](section-plans/quantum-compilation.md#ch-quantum-programs-intermediate-representations-and-verified-optimization); [Chapter 42, all sections](section-plans/quantum-compilation.md#ch-gate-synthesis-qubit-mapping-routing-and-scheduling); [Chapter 43, all sections](section-plans/quantum-compilation.md#ch-control-level-lowering-dynamic-execution-and-logical-compilation)

### select-and-validate-classical-simulators

**L2 · planned · not run · independent acceptance pending.**

Choose exact, stabilizer, MPS, contraction or cutting methods for a specified output and error target.

**Deliverable:** Independent small exact cases, convergence/error records and memory/runtime accounting.

**Required task skills:** [translate-complex-linear-algebra](#translate-complex-linear-algebra), [translate-qubit-ordering](#translate-qubit-ordering), [model-composite-states-and-channels](#model-composite-states-and-channels)

**Primary sources:** [Chapter 44, all sections](section-plans/06-simulation.md#ch-exact-simulation-tensor-execution-and-numerical-reliability); [Chapter 45, all sections](section-plans/06-simulation.md#ch-stabilizer-simulation-magic-and-classical-simulability); [Chapter 46, all sections](section-plans/06-simulation.md#ch-matrix-product-states-entanglement-and-truncation); [Chapter 47, all sections](section-plans/06-simulation.md#ch-tensor-networks-contraction-and-hybrid-simulation-strategies)

### reproduce-molecular-vqe

**L3 · planned · not run · independent acceptance pending.**

Trace integrals, operators, mappings, reductions, optimizers and reported energy targets for a scoped chemistry claim.

**Deliverable:** Provenance-complete Hamiltonian and energy/gradient/optimization evidence.

**Required task skills:** [scope-paper-claims](#scope-paper-claims), [train-differentiable-hybrid-models](#train-differentiable-hybrid-models), [select-and-validate-classical-simulators](#select-and-validate-classical-simulators)

**Primary sources:** [Chapter 49, all sections](section-plans/07-research.md#ch-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe)

**Existing candidate evidence:** [verify_h2_vqe.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/omalley2016/verify_h2_vqe.py); [h2-provenance.md](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/docs/references/h2-provenance.md). These artifacts are not a skill evaluation, an acceptance decision or a whole-paper reproduction claim.

### reproduce-declared-paper-claim

**L3 · planned · not run · independent acceptance pending.**

Select relevant domain workflows and reproduce one registered claim with no silent substitutions.

**Deliverable:** Per-claim implementation, metrics, uncertainty and discrepancy report.

**Required task skills:** [scope-paper-claims](#scope-paper-claims)

**Primary sources:** Cross-cutting orchestration; no primary section ownership. See support references and the selected run profile.

**Support sources:** [48.1](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-1), [48.2](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-2), [48.3](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-3), [48.4](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-4), [48.5](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-5), [48.6](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-6), [48.7](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-7), [48.8](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-8), [48.9](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-9)

### assemble-paper-reproduction

**L4 · planned · not run · independent acceptance pending.**

Integrate mandatory paper claims, artifacts, dependencies and reviews into a reproducible report.

**Deliverable:** Complete claim ledger, evidence bundle and explicit aggregate disposition.

**Required task skills:** [scope-paper-claims](#scope-paper-claims), [reproduce-declared-paper-claim](#reproduce-declared-paper-claim)

**Primary sources:** [Chapter 48, all sections](section-plans/07-research.md#ch-reading-papers-building-evidence-and-reproducing-results)

**Support sources:** [14.1](section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-1), [14.2](section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-2), [14.3](section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-3), [14.4](section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4), [14.5](section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-5), [14.6](section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6), [14.7](section-plans/03-algorithms.md#sec-hybrid-interaction-map), [14.8](section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-7), [14.9](section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-8), [49.1](section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-1), [49.2](section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-2), [49.3](section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-3), [49.4](section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-4), [49.5](section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-5), [49.6](section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-6), [49.7](section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-7), [49.8](section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-8), [49.9](section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-9), [50.1](section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-1), [50.2](section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-2), [50.3](section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-3), [50.4](section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-4), [50.5](section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-5), [50.6](section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-6), [50.7](section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-7), [50.8](section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-8), [50.9](section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-9)

### transfer-to-unseen-papers

**L5 · planned · not run · independent acceptance pending.**

Evaluate routing and execution on held-out papers, identifying unsupported requirements rather than inventing success.

**Deliverable:** Per-domain held-out evaluation and a versioned capability/limitation report.

**Required task skills:** [assemble-paper-reproduction](#assemble-paper-reproduction)

**Primary sources:** Cross-cutting orchestration; no primary section ownership. See support references and the selected run profile.

**Support sources:** [48.1](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-1), [48.2](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-2), [48.3](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-3), [48.4](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-4), [48.5](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-5), [48.6](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-6), [48.7](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-7), [48.8](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-8), [48.9](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-9)

## Implementation order after this planning pass

1. Preserve the [state/operator blind evaluation](comparison-skill-blind-evaluation.md): 0.1.1 passed 11 fresh tasks after a runtime-contract repair. Gather separate scientific acceptance and reader evidence; published cases are now regression fixtures.
2. Preserve the [interference prototype evidence](interference-skill-prototype.md): 35 author cases and 12 new blind-agent tasks passed, including units, analyzer signs, chronology, claim rejection and selection between two runnable skills. Scientific acceptance remains separate.
3. Preserve the [phase-tracked unitary evolution evidence](unitary-evolution-skill-prototype.md): 53 author cases and 12 blind tasks passed, covering units, generator validation, Euler endpoints, controlled phase repair and selection among three skills. Scientific acceptance remains pending.
4. Preserve the [complex linear algebra evidence](complex-algebra-skill-prototype.md): 55 author cases and 12 blind tasks passed. Classical calculations and actual routed FlagQuantum execution are recorded separately; scientific acceptance remains pending.
5. Establish per-claim evidence bundling and a fresh-workspace rerun. Extend the existing molecular case only after the integral-to-model provenance and the chosen paper targets are explicitly contracted.
6. Add L2 workflows as their source obligations and genuine APIs are authored and verified. Evaluate L4 on a registered multi-claim case, then L5 on held-out papers with separately reported domain coverage.

This order concerns future skill prototypes. It does not reorder the frozen 16 textbook writing batches, start a new chapter, or label a prototype accepted. The first four bounded prototypes are independent-agent-tested; no paper run or new textbook section is performed by this update.
