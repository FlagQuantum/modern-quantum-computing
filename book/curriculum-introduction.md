# Full book plan

**Long-term curriculum revision: October 20, 2026.** Nine parts, 50 chapters and six appendices. The systematic editorial pass covers all 50 chapters and 435 sections, including physical-platform and quantum-compilation routes. The [editorial charter](editorial-charter.md) records the author's aim: a rigorous, accessible modern classic that helps present and future learners enter the field.

This is a curriculum architecture, not a completed manuscript or a claim that every proposed experiment is supported. Three starter chapters currently exist, with intended homes in Chapters **6, 23 and 49**. The three-chapter PDF retains independent sample numbering and its published version.

**Architecture status: [Writing Baseline 1.0](writing-baseline.md) adopted for editorial execution; independent section/route acceptance pending.** The [curriculum audit](curriculum-audit.md) lists coverage, prerequisite bridges, cross-layer laboratories and open review gates. [Reader continuity](reader-continuity.md) defines the no-skipped-steps standard. The [all-section result/proof/source plan](proof-plan.md) and [adopted seven-volume plan](volume-plan.md) extend the architecture review. The [review report](architecture-review.md), [435-section ledger](section-review.md) and [19 learning paths](learning-paths.md) make the review traceable. The [writing queue](writing-order.md) now fixes production order. This baseline change writes no body; subsequent drafts follow local start checks and retain separate acceptance gates. Chapter count is not an acceptance criterion.

## Audience, depth and reading levels

Entry readers need basic Python and introductory linear algebra. Foundations supply the quantum model and mathematical bridges; advanced chapters introduce additional probability, optimization, algebra and complexity prerequisites where needed. Readers should be able to reason, derive, implement, verify and critique a new calculation.

**Core** identifies conceptual foundations; **Advanced** adds demanding theory or specialization; **Research** integrates a scoped paper reproduction. A chapter may have a core narrative and advanced proof sections. These labels do not promise that all core chapters fit in one semester. A complete book supports several courses.

The theory determines the curriculum. A missing FlagQuantum API becomes a tracked implementation requirement through the [capability-gap workflow](implementation-roadmap.md). Authors may develop independent executable references while an upstream implementation is pending. Only actually executed, versioned FlagQuantum examples receive validated status.

## Quantum-classical integration

The [hybrid-computing map](hybrid-computing.md) distinguishes eight composable implementation patterns and their host/controller/device boundaries. The early overview is in 14.7; detailed methods remain in their mathematical and systems homes. Hybrid learning is one branch of this broader subject.

## Section architecture and acceptance standard

Each chapter below specifies its section sequence, mathematical outcome and independent check. The [detailed section plan](section-plan.md) expands all 50 chapters into numbered sections with learning/derivation and implementation/evidence targets. These are authoring targets, not claims of existing proofs or code.

1. Open with a concrete question, prerequisites and a prediction.
2. State definitions, physical postulates, access models and assumptions.
3. Give named results with their quantifiers and conditions. Prove central results at the declared level; identify deferred proof ingredients and exact sources.
4. Derive important intermediate steps and connect them to code, including indices, units, dimensions and normalization.
5. Analyze resources and error, including precision and success probability where relevant.
6. Verify small cases independently; include a counterexample or failure diagnosis that tests the assumptions.
7. End with conceptual, derivation/proof, implementation and transfer problems, plus sources and a recap.

Short recall prompts follow the [learning design](learning-design.md); substantial problems develop mathematical and research ability. Numerical agreement supplies evidence about implementation, not a proof of a general theorem. Before drafting a specialized section, inspect its assigned exact sources and resolve material local uncertainties; before accepting it, obtain independent review. Source work serves the current teaching obligation, without creating a new standalone literature-audit project.
