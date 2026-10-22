# Executable writing baseline 1.0

**2026-10-20 · writing-baseline-v1.0 · adopted for editorial execution.** Operational writing baseline for the existing 50 chapters, 435 sections, 19 reader routes and seven volumes; not a claim of completed prose, proof review, reader validation or a scholarly edition.

[Full ordered queue](writing-order.md) · [First-chapter briefs](writing-first-batch.md) · [Result/proof obligations](proof-plan.md) · [Reader routes](learning-paths.md) · [Seven-volume allocation](volume-plan.md)

## Decision and immediate next work

This baseline change writes planning only. Subsequent body work follows the queue and section-local start checks; all-series external review is not a condition for starting the first draft. Publication acceptance remains separate.

The previous all-series drafting hold is replaced by this baseline plus the local start and acceptance gates below. External mathematical, software and reader review are still required for acceptance; none is being claimed complete. A versioned working structure lets that evidence be collected while coherent drafts are written, rather than requiring evidence from an unwritten book before drafting can start.

**Next acceptance target:** [1.1](section-plans/01-foundations.md#sec-what-quantum-computing-computes-1) Problems, inputs, and observable outputs. **Next drafting assignment:** [6.9](section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-9) Measurement laboratory and failure diagnosis. The initial sequence is 1.1–1.6; all six briefs are prepared. Current body links are in the queue and chapter briefs. Current queue: **0 brief-ready / 45 drafts / 0 in review / 0 accepted / 390 not started**. The three previous starters are format pilots and are not counted as accepted sections.

No new standalone paper audits. Existing source-audit records are archived reference material. Verify only the exact claims needed for the section being drafted; a disputed optional hardware claim is qualified or omitted without blocking unrelated chapters.

## Frozen scope and authoritative records

| Decision | Baseline |
|---|---|
| Contents and ownership | Nine subject parts, 50 global chapters, 435 stable section IDs; current intentional exclusions and owner/reuse boundaries remain in force. |
| Prerequisites | 1,045 exact direct section dependencies and 19 reader routes; use exact sections rather than entire preceding volumes. |
| Depth | Every section keeps its existing result, assumptions and P/F/M/R/V obligation; no proof downgrade to make the project shorter. |
| Packaging | Seven volumes with the chapter allocation below; global IDs and chapter numbers are preserved. Trim size, typeset pages and release dates remain production decisions. |
| Production | 16 ordered batches and one generated 435-section queue; imported prerequisite bridges are exposed before first use. |
| Changes | The structural scope digest and tagged Git revision preserve the baseline. Citation refinements and body edits can proceed within frozen learning/proof scope; material changes use a new baseline revision. |

Canonical records are `book/curriculum.json` (scope/graph/routes), `book/proof-plan.json` (depth/result/assumptions), `book/volumes.json` (allocation), `book/writing-baseline.json` (batch/acceptance decisions), and `book/writing-progress.json` (actual work/review state). Planning source-locator checks remain distinct from actual manuscript review evidence. The full baseline is recoverable from Git tag `writing-baseline-v1.0`; the book/PDF edition number is separate.

## Adopted seven-volume plan

| Volume | Title | Global chapters, in reading order | Sections | Planned pages |
|---|---|---|---|---|
| I | Foundations of Quantum Computing | [1](section-plans/01-foundations.md#ch-what-quantum-computing-computes), [2](section-plans/01-foundations.md#ch-complex-vectors-operators-and-numerical-reasoning), [3](section-plans/01-foundations.md#ch-single-qubit-states-and-rotations), [4](section-plans/01-foundations.md#ch-composite-systems-tensor-products-and-qubit-ordering), [5](section-plans/01-foundations.md#ch-gates-reversible-computation-and-circuit-synthesis), [6](section-plans/01-foundations.md#ch-measurement-expectation-values-and-statistical-estimation), [7](section-plans/01-foundations.md#ch-entanglement-and-quantum-information-protocols), [8](section-plans/01-foundations.md#ch-density-matrices-reduced-states-and-purification), [14](section-plans/03-algorithms.md#ch-computational-models-complexity-and-quantum-advantage) | 72 | 231–450 |
| II | Quantum Information, Communication, and Security | [9](section-plans/02-information.md#ch-quantum-channels-and-their-representations), [10](section-plans/02-information.md#ch-distinguishability-fidelity-and-quantum-state-inference), [11](section-plans/02-information.md#ch-entropy-relative-entropy-and-information-processing), [12](section-plans/02-information.md#ch-compression-entanglement-and-communication-limits), [13](section-plans/02-information.md#ch-quantum-cryptography-and-security-reasoning) | 43 | 175–328 |
| III | Quantum Algorithms and Their Limits | [15](section-plans/03-algorithms.md#ch-interference-oracles-and-phase-kickback), [16](section-plans/03-algorithms.md#ch-grover-search-amplitude-amplification-and-estimation), [17](section-plans/03-algorithms.md#ch-fourier-transforms-and-quantum-phase-estimation), [18](section-plans/03-algorithms.md#ch-period-finding-factoring-and-algorithmic-arithmetic), [19](section-plans/03-algorithms.md#ch-hamiltonian-simulation-and-error-bounds), [20](section-plans/03-algorithms.md#ch-block-encodings-and-quantum-linear-algebra), [21](section-plans/03-algorithms.md#ch-quantum-signal-processing-and-singular-value-transformation), [22](section-plans/03-algorithms.md#ch-quantum-walks-lower-bounds-and-algorithm-design) | 70 | 243–468 |
| IV | Differentiable and Hybrid Quantum Computing | [23](section-plans/04-variational.md#ch-parameterized-circuits-quantum-gradients-and-differentiation), [24](section-plans/04-variational.md#ch-optimization-geometry-and-trainability), [25](section-plans/04-variational.md#ch-variational-simulation-chemistry-and-ground-state-problems), [26](section-plans/04-variational.md#ch-qaoa-quantum-optimization-and-classical-comparisons), [27](section-plans/04-variational.md#ch-quantum-learning-kernels-and-hybrid-models), [48](section-plans/07-research.md#ch-reading-papers-building-evidence-and-reproducing-results), [49](section-plans/07-research.md#ch-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe) | 65 | 199–390 |
| V | Noise, Error Correction, and Logical Computation | [28](section-plans/05-fault-tolerance.md#ch-noise-open-systems-and-error-mitigation), [29](section-plans/05-fault-tolerance.md#ch-quantum-error-correction-conditions-and-recovery), [30](section-plans/05-fault-tolerance.md#ch-stabilizer-codes-logical-operators-and-decoding), [31](section-plans/05-fault-tolerance.md#ch-surface-codes-and-repeated-syndrome-measurements), [32](section-plans/05-fault-tolerance.md#ch-fault-tolerant-gates-and-universal-logical-computation), [33](section-plans/05-fault-tolerance.md#ch-from-logical-algorithms-to-physical-resource-estimates), [50](section-plans/07-research.md#ch-case-study-logical-memory-and-error-correction-experiments) | 63 | 215–414 |
| VI | Physical Realizations of Quantum Computing | [34](section-plans/physical-platforms.md#ch-from-abstract-qubits-to-physical-quantum-systems), [35](section-plans/physical-platforms.md#ch-superconducting-qubits-and-circuit-qed-control), [36](section-plans/physical-platforms.md#ch-trapped-ion-qubits-motional-gates-and-transport), [37](section-plans/physical-platforms.md#ch-neutral-atom-arrays-and-rydberg-quantum-computing), [38](section-plans/physical-platforms.md#ch-photonic-encodings-optical-circuits-and-measurement-based-computation), [39](section-plans/physical-platforms.md#ch-semiconductor-spin-qubits-and-exchange-based-architectures), [40](section-plans/physical-platforms.md#ch-topological-quantum-computation-and-candidate-physical-realizations) | 59 | 190–368 |
| VII | Quantum Programming, Compilation, and Classical Simulation | [41](section-plans/quantum-compilation.md#ch-quantum-programs-intermediate-representations-and-verified-optimization), [42](section-plans/quantum-compilation.md#ch-gate-synthesis-qubit-mapping-routing-and-scheduling), [43](section-plans/quantum-compilation.md#ch-control-level-lowering-dynamic-execution-and-logical-compilation), [44](section-plans/06-simulation.md#ch-exact-simulation-tensor-execution-and-numerical-reliability), [45](section-plans/06-simulation.md#ch-stabilizer-simulation-magic-and-classical-simulability), [46](section-plans/06-simulation.md#ch-matrix-product-states-entanglement-and-truncation), [47](section-plans/06-simulation.md#ch-tensor-networks-contraction-and-hybrid-simulation-strategies) | 63 | 211–408 |

Page envelopes include the existing 24–40 pages of front/back material per volume and exclude substantial shared appendices/solutions. They are estimates, not rendered lengths. Appendix A–F subjects and a common bibliography, glossary, symbol index and errata remain shared. Volume I closes with global Chapter 14; global Chapter 48 precedes capstones in Volume IV; 49 closes IV and 50 closes V. A partial chapter bridge stays at its owning section and is reused later.

## Writing order and batch exit targets

This is the production order, not a new reader prerequisite chain. Later batch placement of a platform does not make it a prerequisite for earlier abstract compilation. “Exit” below is a target to review, not a claim that the batch is complete.

| Batch | Planned work | New sections | Inserted prerequisites | Exit target |
|---|---|---|---|---|
| [B01](writing-order.md#b01) | The opening: tasks, mathematical language, states and registers | 29 | None | A continuous first four chapters with no undeclared mathematics; predictions and ordering checks are explained before the reader uses them. |
| [B02](writing-order.md#b02) | Complete the foundational course | 43 | None | A coherent Volume I draft: gates, measurement, entanglement, mixtures and resource/access models; expand the existing measurement starter in its proper context. |
| [B03](writing-order.md#b03) | Independent exact-execution bridge | 5 | None | A small independently checked executor and measurement reference, used by later labs. This does not require writing all of Volume VII. |
| [B04](writing-order.md#b04) | Interference, oracles and search | 16 | None | One complete oracle/search route with query assumptions, amplitude geometry and precision/error accounting. |
| [B05](writing-order.md#b05) | Fourier, arithmetic and dynamics | 27 | None | Complete the QFT/QPE/arithmetic/Hamiltonian route and its local algebra/error bridges before advanced spectral methods. |
| [B06](writing-order.md#b06) | Gradients to a verified H2 capstone | 40 | [10.7](section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-6) | An end-to-end derivative/energy/optimization/research route; expand the gradients and H2 starters without counting their current form as accepted chapters. |
| [B07](writing-order.md#b07) | Basic quantum programming and compilation | 24 | [9.1](section-plans/02-information.md#sec-quantum-channels-and-their-representations-1), [9.2](section-plans/02-information.md#sec-quantum-channels-and-their-representations-2), [9.3](section-plans/02-information.md#sec-quantum-channels-and-their-representations-3), [9.7](section-plans/02-information.md#sec-quantum-channels-and-their-representations-7) | A complete program-to-target core compiler route on an explicit abstract target; no requirement to finish all physical-platform chapters. |
| [B08](writing-order.md#b08) | Complete information, communication and security | 38 | None | Complete Volume II, including the later general channels/inference/information proofs; previously written prerequisite bridges remain in their owning chapters. |
| [B09](writing-order.md#b09) | Complete differentiable and hybrid methods | 26 | None | Complete gradient variants, geometry/trainability, embedding, QAOA and quantum learning; all eight hybrid patterns retain their mathematical/system owners. |
| [B10](writing-order.md#b10) | Complete modern spectral algorithms and limits | 27 | None | Block encodings, qubitization/QSVT, walks and scoped lower-bound/complexity results with declared advanced proof roadmaps. |
| [B11](writing-order.md#b11) | Noise, correction and finite logical memory | 46 | None | A finite logical-memory route with code conditions, stabilizers, syndromes and decoding; it precedes universal fault tolerance and factory/resource claims. |
| [B12](writing-order.md#b12) | Universal logical computation and resources | 17 | None | Complete fault-tolerant operations and scoped resource estimation; add the memory-to-resource interpretation only after these imports. |
| [B13](writing-order.md#b13) | Shared physical models and a superconducting route | 18 | None | One complete hardware-to-program/control thread with local oscillator/circuit bridges; benchmark the shared platform comparison contract. |
| [B14](writing-order.md#b14) | Complete control, dynamic and logical lowering | 9 | None | Complete remaining compiler/control branches after physical and logical prerequisites, reusing the already written core compiler material. |
| [B15](writing-order.md#b15) | Alternative physical realizations | 41 | None | Complete ion, atom, photon, spin and topology branches using the shared comparison contract. Topological theory is retained; a contested device claim may be qualified or omitted locally without restarting a paper audit. |
| [B16](writing-order.md#b16) | Complete classical simulation and series integration | 29 | None | Complete stabilizer, MPS and general tensor/cutting routes, batching/parallel execution and volume integration; finish indices, shared appendices and cross-volume links. |

Batch B06 explicitly inserts 10.7 (Pauli sums/grouping/shot allocation); B07 inserts 9.1, 9.2, 9.3 and 9.7 (the exact channel/semantics bridges). These do not require completing the whole information volume first. Basic executor sections are written in B03 and complete Chapter 44 later in B16. Finite logical memory is written in B11; only its resource-interpretation section waits for B12.

## Fixed section-depth contract

| Code | Sections | Required depth |
|---|---|---|
| P | 34 | State the adopted model and definitions; derive the listed consequences. A physical postulate is not proved from the circuit model. |
| F | 224 | Supply every essential step at the declared scope, using only explicitly imported earlier results. Full means this scoped proposition, not every generalization. |
| M | 78 | Derive the specified finite/effective-model result and its approximation domain; no general theorem or optimizer guarantee is implied. |
| R | 30 | State the chosen theorem with all hypotheses and quantifiers; prove the listed special case/lemmas, name deferred ingredients and point to their exact source. The general proof is explicitly deferred. |
| V | 69 | No new theorem is promised. Reuse named prerequisite results and specify acceptance evidence, failure tests and scope. |

Each queue row links to its exact section specification; its result, assumptions, local bridge and deferred ingredients remain in the [detailed proof plans](proof-plan.md). These are minimum obligations, not a request to prove every generalization or to turn a physical postulate into a theorem.

## Start a section

1. Use the next scheduled stable section ID and its existing result/proof/source record; complete the brief before writing prose.
2. Every imported earlier result has a usable draft with definitions and matching conventions, or a bounded local bridge is supplied and scheduled. Known blocking errors in an imported result are resolved first.
3. Inspect the exact source target needed for this section; fix or qualify a material uncertainty locally. A generic whole-book source review is not required.
4. Choose the independent small reference and the worked/transfer cases; investigate an API only when its actual use is imminent. No new validated-execution claim is made without a run.

## Accept a section and a batch

1. A filled brief names the concrete question, entry/exit skills, exact prerequisite IDs, result/scope and P/F/M/R/V obligation, local notation, complete-example or justified non-code role, independent check, source target and problem/answer plan.
2. The draft defines every new symbol before use, supplies local mathematical/physical bridges, explains central intermediate steps, and points to the exact imported result. A central argument cannot be hidden in an exercise or dismissed as obvious.
3. Mathematical review checks the exact result and assumptions at the frozen depth. Numerical tests validate an implementation, not a theorem. An R section must include its local special-case proof/lemmas and name what is deferred.
4. Code-bearing sections have a complete executable program, formula-to-code correspondence, pinned environment, expected output/tolerance and an independent reference. Actual FlagQuantum support and execution are recorded; missing APIs use the upstream gap workflow and never remove required theory. A non-code section records why code is not appropriate.
5. Each section includes at least one worked example or justified conceptual/model case, one local comprehension/prediction checkpoint and one transfer/failure-analysis task with an accessible answer/hint path. A chapter closes with conceptual, derivation/proof, implementation and debugging problems as appropriate; exact counts are calibrated after the opening batch.
6. A target reader attempts the argument and a transfer task. Record the missing step, repair and recheck. Before acceptance record mathematical, implementation or justified N/A, and reader reviews separately with evidence. Accepted prerequisites are required for publication; an explained working draft can support the next draft.

A draft may use an explained, convention-consistent earlier draft while both remain in review. Publication requires the route’s prerequisite sections and each released section to be accepted. A batch exits drafting when its sections form a continuous working route; it exits acceptance only when the required independent reviews, integrated example, problem answers and web/print checks pass. Do not fabricate a reviewer, reader trial or successful run to advance a status.

## Local risks rather than a global research backlog

| Item | Writing decision |
|---|---|
| Unchecked theorem details | Inspect only the exact theorem required for the current section; resolve a central proof uncertainty before claiming the result. Other batches continue. |
| Missing FlagQuantum API | Write the mathematics and independent reference, investigate the actual call and track a confirmed upstream gap. Keep framework execution explicitly pending. |
| H2 original author integral files | Use the checked STO-6G reconstruction at published precision and disclose the provenance limit in 49; no renewed search is a baseline prerequisite. |
| Contested topological-device interpretation | Retain the existing audit as reference. Use a bounded dated claim or omit the optional disputed example in 40.7; do not resume a standalone paper investigation. |
| Specialist/reader workload and print calibration | Collect evidence on the authored section/batch. Do not label an untested draft accepted or require all seven volumes to pass before starting Chapter 1. |

## Change control

- Editorial clarification, typo fixes and improved examples may preserve the baseline when scope, prerequisites, proof obligations and volume placement remain unchanged.
- A dependency, section split/merge, depth change, central-result/scope change, new topic or volume reassignment needs an impact record, stable-ID/anchor migration if relevant, a new baseline version and regenerated queue. Never silently downgrade a proof to meet a page budget.
- Priority changes need a versioned batch amendment and a fresh dependency check. Page ranges are planning envelopes, not typeset promises; significant expansion is assessed against reader workload and proof completeness.
- Correct mathematical or safety-critical claims immediately, record affected sections/examples and revalidation; do not preserve a known error merely to keep the baseline unchanged.

Use [the baseline-change record template](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/templates/baseline-change.md) for an intentional revision. The initial decision record is [in the repository](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/baseline-changes/v1.0.md). Automated checks verify scope/coverage/order; they do not supply scientific or educational sign-off.
