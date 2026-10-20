# Core results, proof depth, and exact source plan

**50 chapters / 435 sections · 2026-10-20 · planning only.** No new textbook body is written by this specification. Every section has a result or explicit non-theorem role, assumptions, proof obligation and version-specific source locators. A source locator identifies where to read; it does not certify that its proof has been independently checked or that a FlagQuantum API implements it.

[Volume proposal](volume-plan.md) · [Exact source catalogue](references/proof-sources.md) · [Prerequisites](section-review.md) · [Acceptance gates](curriculum-audit.md)

## Proof-depth contract

| Code | Planned depth | Sections | Acceptance requirement |
|---|---|---|---|
| P | Postulate / definition / task contract | 34 | State the adopted model and definitions; derive the listed consequences. A physical postulate is not proved from the circuit model. |
| F | Complete proof at the stated finite scope | 224 | Supply every essential step at the declared scope, using only explicitly imported earlier results. Full means this scoped proposition, not every generalization. |
| M | Complete selected-model derivation | 78 | Derive the specified finite/effective-model result and its approximation domain; no general theorem or optimizer guarantee is implied. |
| R | Precise advanced theorem with proof roadmap | 30 | State the chosen theorem with all hypotheses and quantifiers; prove the listed special case/lemmas, name deferred ingredients and point to their exact source. The general proof is explicitly deferred. |
| V | Validation / methodology specification | 69 | No new theorem is promised. Reuse named prerequisite results and specify acceptance evidence, failure tests and scope. |

**Global convention:** Finite-dimensional complex spaces and exact arithmetic unless the record explicitly uses an oscillator cutoff, asymptotic limit, stochastic model or numerical approximation. Dimensions, normalization, support, access and resource conventions must be restated locally when material.

“Complete proof” is relative to explicitly stated imported earlier results. For example, the Holevo proof can use the previously stated data-processing theorem; it must disclose that dependence. Definitions, physical postulates and experiment protocols are not relabeled as theorems. For R sections, exact quantifiers/constants and the selected theorem revision must be transcribed and reviewed before drafting; the plan is not the theorem statement itself.

## All-section specifications

| Part | Detailed proof/source plan |
|---|---|
| 1 | [Foundations and Quantum Information Primitives](proof-plans/01-foundations.md) |
| 2 | [Quantum Information: Channels, Inference, and Communication](proof-plans/02-information.md) |
| 3 | [Quantum Algorithms and Computational Resources](proof-plans/03-algorithms.md) |
| 4 | [Variational and Differentiable Quantum Computing](proof-plans/04-variational.md) |
| 5 | [Noise, Error Correction, and Fault-Tolerant Computation](proof-plans/05-fault-tolerance.md) |
| 6 | [Physical Realizations and Quantum-System Architecture](proof-plans/physical-platforms.md) |
| 7 | [Quantum Programming, Compilation, and Control](proof-plans/quantum-compilation.md) |
| 8 | [Classical Simulation and the Boundary of Tractability](proof-plans/06-simulation.md) |
| 9 | [From Papers to Reproducible Research](proof-plans/07-research.md) |

## Outstanding source acceptance items

- 49.2: [H2-01–09](references/h2-provenance.md) now pins the integral-to-model chain and independent 324-coefficient audit. Original author integral files were not recovered; mathematical/reader acceptance remains open.
- 40.7: [TOPO-01–09](references/topological-experiments.md) now selects dated primary sources and pairs critique/reply and retraction records. Full subscription comment/reply review and specialist experimental interpretation remain open.
- Chapter 50 now selects Fowler et al. v2, Section VII A/Fig. 5 for syndrome ambiguity. The finite memory experiment is a declared textbook extension; Fig. 4 threshold results are outside the reproduction claim. Exact patch/round/decoder choices still require acceptance.
- All proof plans require mathematical/source review, source-specific counterexamples and calibrated problem/example budgets before baseline freeze. Locator checks and planned full proofs do not satisfy those gates.
