# Adopted seven-volume writing plan

**Writing Baseline 1.0 · 2026-10-20 · chapter allocation adopted; final trim/pages pending.** Volume allocation is a dependency-compatible presentation overlay. Global chapter numbers and stable IDs remain unchanged. A volume is a reference/teaching resource, not a requirement to finish all previous volumes.

The proof-depth pass changes the earlier uniform budgets. Foundations and information together would reach an estimated 738 pages with closing/front material; splitting them keeps distinct entry and advanced-information courses usable. Seven subject volumes avoid compressing proofs to fit an arbitrary chapter/page count. These are planned ranges, not rendered pages or promised release dates.

| Volume | Title | Global chapters | Sections | Planned pages including 24–40 pages of volume front/back matter |
|---|---|---|---|---|
| [I](#volume-i) | Foundations of Quantum Computing | 1, 2, 3, 4, 5, 6, 7, 8, 14 | 72 | 231–450 |
| [II](#volume-ii) | Quantum Information, Communication, and Security | 9, 10, 11, 12, 13 | 43 | 175–328 |
| [III](#volume-iii) | Quantum Algorithms and Their Limits | 15, 16, 17, 18, 19, 20, 21, 22 | 70 | 243–468 |
| [IV](#volume-iv) | Differentiable and Hybrid Quantum Computing | 23, 24, 25, 26, 27, 48, 49 | 65 | 199–390 |
| [V](#volume-v) | Noise, Error Correction, and Logical Computation | 28, 29, 30, 31, 32, 33, 50 | 63 | 215–414 |
| [VI](#volume-vi) | Physical Realizations of Quantum Computing | 34, 35, 36, 37, 38, 39, 40 | 59 | 190–368 |
| [VII](#volume-vii) | Quantum Programming, Compilation, and Classical Simulation | 41, 42, 43, 44, 45, 46, 47 | 63 | 211–408 |

Series total: **1464–2826 planned pages**, including the stated per-volume front/back allocation, but excluding substantial shared appendices/solutions. Central full proofs have extra space; ordinary F/M sections receive 3–6 pages, advanced theorem roadmaps 4–8, and 23 substantial arguments 6–10. These ranges require reader and typesetting calibration.

## Reading continuity and shared material

Global Chapter 14 closes Volume I so basic computational models are available without first completing advanced information theory. Global Chapter 48 is placed in Volume IV before the two capstones need its methods. The H2 capstone (49) closes Volume IV; memory (50) closes Volume V. Its exact tiny reference uses dense/error enumeration, so it does not require the later tableau implementation (45). Existing global numbers/URLs/IDs remain stable. Print running heads and the series contents identify both the volume and global chapter. Avoid an additional independent numbering scheme for concepts.

No section requires a later volume under the current graph and this internal chapter ordering. This is structural consistency, not completed learner validation. Readers need the **specified sections**, not all preceding volumes. Use the [19 checked routes](learning-paths.md) for courses; fixed kernels, basic compilation and physical branches retain their lighter entry contracts.


<span id="volume-i"></span>

## Volume I: Foundations of Quantum Computing

Mathematical bridges, states, circuits, measurement and protocols, followed by computational/access/resource models. Chapter 14 is placed here to complete a first-course foundation without requiring advanced information theory.

**Cross-volume imports:** 0 distinct direct prerequisite sections across the full volume, including optional advanced branches. This is not one course's mandatory reading list.

No earlier-volume section imports.

<span id="volume-ii"></span>

## Volume II: Quantum Information, Communication, and Security

Channels, distinguishability, inference, entropy, compression, entanglement manipulation and security. This advanced information route is optional before the first algorithm or compiler course.

**Cross-volume imports:** 14 distinct direct prerequisite sections across the full volume, including optional advanced branches. This is not one course's mandatory reading list.

- **Chapter 2:** [2.5](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).
- **Chapter 3:** [3.2](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-2).
- **Chapter 4:** [4.1](section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [4.2](section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2).
- **Chapter 6:** [6.2](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [6.4](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-4), [6.6](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6), [6.7](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7), [6.8](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).
- **Chapter 7:** [7.2](section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-2).
- **Chapter 8:** [8.2](section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2), [8.3](section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-3), [8.4](section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4), [8.6](section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-6).

<span id="volume-iii"></span>

## Volume III: Quantum Algorithms and Their Limits

Oracle algorithms through arithmetic, dynamics, block encodings, QSVT and complexity. Core algorithms precede optional spectral/complexity proofs.

**Cross-volume imports:** 22 distinct direct prerequisite sections across the full volume, including optional advanced branches. This is not one course's mandatory reading list.

- **Chapter 2:** [2.3](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3), [2.5](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5), [2.6](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-6), [2.7](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7), [2.8](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-8).
- **Chapter 3:** [3.4](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-4), [3.5](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5).
- **Chapter 4:** [4.1](section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [4.2](section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2), [4.5](section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-5).
- **Chapter 5:** [5.2](section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2), [5.3](section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-3), [5.4](section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4).
- **Chapter 6:** [6.1](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-1), [6.2](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [6.3](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3), [6.6](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6), [6.7](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7), [6.8](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).
- **Chapter 14:** [14.3](section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-3), [14.4](section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4), [14.6](section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

<span id="volume-iv"></span>

## Volume IV: Differentiable and Hybrid Quantum Computing

Gradients, optimization, chemistry, QAOA and learning, followed by research-method training and the H2 capstone. Chapter 48 is physically placed here before both capstones need it.

**Cross-volume imports:** 25 distinct direct prerequisite sections across the full volume, including optional advanced branches. This is not one course's mandatory reading list.

- **Chapter 1:** [1.4](section-plans/01-foundations.md#sec-what-quantum-computing-computes-4).
- **Chapter 2:** [2.2](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-2), [2.3](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3), [2.5](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5), [2.6](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-6), [2.7](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7), [2.8](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-8).
- **Chapter 3:** [3.5](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5).
- **Chapter 4:** [4.1](section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [4.2](section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2), [4.3](section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-3).
- **Chapter 5:** [5.1](section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1), [5.4](section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4).
- **Chapter 6:** [6.3](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3), [6.6](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6), [6.7](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7), [6.8](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).
- **Chapter 8:** [8.4](section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4).
- **Chapter 10:** [10.3](section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-3), [10.7](section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-6).
- **Chapter 14:** [14.4](section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4), [14.6](section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6), [14.8](section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-7).
- **Chapter 19:** [19.1](section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-1), [19.5](section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-5).

<span id="volume-v"></span>

## Volume V: Noise, Error Correction, and Logical Computation

Noise and device characterization through code conditions, decoding, fault tolerance and resources; the finite memory case study closes the route.

**Cross-volume imports:** 26 distinct direct prerequisite sections across the full volume, including optional advanced branches. This is not one course's mandatory reading list.

- **Chapter 2:** [2.3](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3), [2.4](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-4), [2.5](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5), [2.6](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-6), [2.7](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).
- **Chapter 3:** [3.3](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-3), [3.5](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5).
- **Chapter 4:** [4.1](section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [4.3](section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-3).
- **Chapter 5:** [5.2](section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2), [5.7](section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-7).
- **Chapter 6:** [6.2](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [6.6](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6), [6.7](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7), [6.8](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).
- **Chapter 7:** [7.5](section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-5).
- **Chapter 8:** [8.4](section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4).
- **Chapter 9:** [9.3](section-plans/02-information.md#sec-quantum-channels-and-their-representations-3), [9.5](section-plans/02-information.md#sec-quantum-channels-and-their-representations-5), [9.7](section-plans/02-information.md#sec-quantum-channels-and-their-representations-7).
- **Chapter 10:** [10.5](section-plans/02-information.md#sec-channel-error-metrics), [10.6](section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-5).
- **Chapter 14:** [14.6](section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).
- **Chapter 48:** [48.1](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-1), [48.2](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-2), [48.9](section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-9).

<span id="volume-vi"></span>

## Volume VI: Physical Realizations of Quantum Computing

Shared physical bridges and six alternative platform branches. Teach one branch in depth; compare the rest through common contracts.

**Cross-volume imports:** 24 distinct direct prerequisite sections across the full volume, including optional advanced branches. This is not one course's mandatory reading list.

- **Chapter 2:** [2.3](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3), [2.5](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5), [2.6](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-6).
- **Chapter 3:** [3.1](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-1), [3.4](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-4).
- **Chapter 4:** [4.1](section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [4.5](section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-5).
- **Chapter 5:** [5.2](section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).
- **Chapter 6:** [6.2](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [6.7](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).
- **Chapter 7:** [7.1](section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-1).
- **Chapter 8:** [8.2](section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2).
- **Chapter 9:** [9.7](section-plans/02-information.md#sec-quantum-channels-and-their-representations-7).
- **Chapter 14:** [14.6](section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).
- **Chapter 19:** [19.1](section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-1), [19.8](section-plans/03-algorithms.md#sec-hamiltonian-adiabatic-model).
- **Chapter 25:** [25.2](section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-2), [25.3](section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-3).
- **Chapter 28:** [28.1](section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-1), [28.2](section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-2), [28.3](section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-3).
- **Chapter 29:** [29.5](section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-5).
- **Chapter 30:** [30.10](section-plans/05-fault-tolerance.md#sec-stabilizer-graph-state-mbqc).
- **Chapter 32:** [32.6](section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-6).

<span id="volume-vii"></span>

## Volume VII: Quantum Programming, Compilation, and Classical Simulation

Semantics, synthesis, routing, scheduling and control, followed by exact/stabilizer/MPS/tensor-network execution. Core compilation can enter from supplied targets; advanced control/logical branches import selected earlier-volume sections.

**Cross-volume imports:** 45 distinct direct prerequisite sections across the full volume, including optional advanced branches. This is not one course's mandatory reading list.

- **Chapter 2:** [2.3](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3), [2.5](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5), [2.7](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7), [2.8](section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-8).
- **Chapter 3:** [3.2](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-2), [3.5](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5), [3.6](section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-6).
- **Chapter 4:** [4.2](section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2), [4.3](section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-3), [4.4](section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-4), [4.5](section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-5), [4.6](section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-6).
- **Chapter 5:** [5.1](section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-1), [5.2](section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2), [5.4](section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4), [5.5](section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-5), [5.6](section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-6), [5.8](section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-8).
- **Chapter 6:** [6.2](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [6.3](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3), [6.5](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-5), [6.6](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6), [6.7](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).
- **Chapter 7:** [7.2](section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-2).
- **Chapter 8:** [8.4](section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4).
- **Chapter 9:** [9.3](section-plans/02-information.md#sec-quantum-channels-and-their-representations-3), [9.7](section-plans/02-information.md#sec-quantum-channels-and-their-representations-7).
- **Chapter 10:** [10.3](section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-3).
- **Chapter 11:** [11.3](section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-3), [11.5](section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-5).
- **Chapter 14:** [14.6](section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6), [14.7](section-plans/03-algorithms.md#sec-hybrid-interaction-map).
- **Chapter 23:** [23.2](section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-2), [23.6](section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-6).
- **Chapter 24:** [24.3](section-plans/04-variational.md#sec-optimization-geometry-and-trainability-3).
- **Chapter 28:** [28.2](section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-2).
- **Chapter 30:** [30.1](section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-1), [30.2](section-plans/05-fault-tolerance.md#sec-stabilizer-codes-logical-operators-and-decoding-2).
- **Chapter 32:** [32.5](section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-5), [32.6](section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-6), [32.7](section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-7).
- **Chapter 33:** [33.2](section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-2).
- **Chapter 34:** [34.3](section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-3), [34.5](section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-5), [34.6](section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-6).

## Alternatives and publishing sequence

One/three large books would create long mixed courses and oversized manuscripts. Five/six books reduce bindings but either merge distinct specialization routes or leave the opening volume especially long. Seven volumes are adopted by the [writing baseline](writing-baseline.md), with related volumes also distributable as a series bundle and one searchable website. Calibrate typesetting and reader workload while writing; a later volume reassignment needs an explicit baseline amendment. Do not trade away central proof obligations.

Follow the [16 writing batches](writing-baseline.md#writing-order-and-batch-exit-targets): first the opening chapters and Volume I, then the executor bridge, algorithm and gradient-to-H2 routes. Advanced information, fault tolerance, platforms and systems have explicit later batches. Mathematical and specialist review is required for their acceptance; it is not a reason to defer unrelated first drafts.

Shared appendices A–F, glossary, symbol index and bibliography use one canonical source and stable links; print includes locally required bridges and sufficient notation. Core exercises/selected solutions and independent references remain accessible offline. Runtime/provider instructions stay versioned companions. Exact theorem/source acceptance, reader testing and final page/problem budgets precede chapter/route publication acceptance; the operational allocation is already fixed.
