# Full book plan

**Long-term curriculum revision: October 20, 2026.** Nine parts, 50 chapters and six appendices. This revision adds substantive physical-platform and quantum-compilation routes to the previous 40-chapter plan. The [editorial charter](editorial-charter.md) records the author's aim: a rigorous, accessible modern classic that helps present and future learners enter the field.

This is a curriculum architecture, not a completed manuscript or a claim that every proposed experiment is supported. Three starter chapters currently exist, with intended homes in Chapters **6, 23 and 49**. The three-chapter PDF retains independent sample numbering and its published version.

**Architecture status: review pending, not frozen.** The [curriculum audit](curriculum-audit.md) lists coverage, prerequisite bridges, cross-layer laboratories and open review gates. [Reader continuity](reader-continuity.md) defines the no-skipped-steps standard. Chapter count is not an acceptance criterion.

## Audience, depth and reading levels

Entry readers need basic Python and introductory linear algebra. Foundations supply the quantum model and mathematical bridges; advanced chapters introduce additional probability, optimization, algebra and complexity prerequisites where needed. Readers should be able to reason, derive, implement, verify and critique a new calculation.

**Core** identifies conceptual foundations; **Advanced** adds demanding theory or specialization; **Research** integrates a scoped paper reproduction. A chapter may have a core narrative and advanced proof sections. These labels do not promise that all core chapters fit in one semester. A complete book supports several courses.

The theory determines the curriculum. A missing FlagQuantum API becomes a tracked implementation requirement through the [capability-gap workflow](implementation-roadmap.md). Authors may develop independent executable references while an upstream implementation is pending. Only actually executed, versioned FlagQuantum examples receive validated status.

## Section architecture and acceptance standard

Each chapter below specifies its section sequence, mathematical outcome and independent check. The [detailed section plan](section-plan.md) expands all 50 chapters into numbered sections with learning/derivation and implementation/evidence targets. These are authoring targets, not claims of existing proofs or code.

1. Open with a concrete question, prerequisites and a prediction.
2. State definitions, physical postulates, access models and assumptions.
3. Give named results with their quantifiers and conditions. Prove central results at the declared level; identify deferred proof ingredients and exact sources.
4. Derive important intermediate steps and connect them to code, including indices, units, dimensions and normalization.
5. Analyze resources and error, including precision and success probability where relevant.
6. Verify small cases independently; include a counterexample or failure diagnosis that tests the assumptions.
7. End with conceptual, derivation/proof, implementation and transfer problems, plus sources and a recap.

Short recall prompts follow the [learning design](learning-design.md); substantial problems develop mathematical and research ability. Numerical agreement supplies evidence about implementation, not a proof of a general theorem. Every specialized chapter needs a reviewed primary-source map before drafting.
