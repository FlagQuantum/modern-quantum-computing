# Modern Quantum Computing

## A Formula-to-Code Approach

*Theory, Algorithms, and Reproducible Experiments with FlagQuantum*

How does an equation in a quantum computing paper become a working program? This open textbook follows that translation explicitly: define the conventions, derive a small result, implement it, and check the answer independently.

**Early draft:** [section 1.1](chapters/ch-what-quantum-computing-computes.md#sec-what-quantum-computing-computes-1) begins the foundational course. Three earlier starter chapters remain format pilots. The full plan comprises nine parts and 50 chapters; the plan is not completed text.

<!-- book-metadata:start -->
**Wei Liu**

FlagQuantum Team

Beijing Academy of Artificial Intelligence (BAAI)

Beijing, China

Correspondence: [liuwei01@baai.ac.cn](mailto:liuwei01@baai.ac.cn)

**Version 0.1.0-draft.4 · 2026-10-20 · Draft**
<!-- book-metadata:end -->

## Educational aim

Our aim is a rigorous modern classic that helps present and future learners enter quantum computing. The [editorial charter](editorial-charter.md) sets standards for depth, accessibility, review and long-term maintenance. The curriculum includes foundations, quantum information, modern algorithms, differentiable computing, fault tolerance, physical implementations, quantum compilation, simulation and reproducible research.

The subject determines the scope. Required missing capabilities are investigated and reported through the [FlagQuantum capability-gap workflow](implementation-roadmap.md); existing API coverage does not limit the theory. Current sample execution claims remain pinned to their tested release.

A [systematic editorial architecture review](architecture-review.md) covers all 50 chapters and 435 sections, with an [exact prerequisite ledger](section-review.md) and [19 learning paths](learning-paths.md). [Writing Baseline 1.0](writing-baseline.md) now fixes scope, depth, volumes and a [435-section production queue](writing-order.md). Independent section/route acceptance remains pending; [reader continuity](reader-continuity.md) is an explicit acceptance standard.

The [all-section result/proof/source plan](proof-plan.md) and [adopted seven-volume plan](volume-plan.md) specify the scholarly scope and publication structure. These remain planning artifacts; mathematical/source and learner review are pending.

The [quantum-classical hybrid map](hybrid-computing.md) connects eight composable algorithm/runtime patterns, their implementation contracts and their chapter homes.

## Who this book is for

Readers who know basic Python and linear algebra and want to understand quantum computing through calculations they can reproduce. Familiarity with complex numbers, matrix multiplication, eigenvalues and elementary derivatives is helpful. A planned foundations part will review these topics; it is not yet written.

## How to use a chapter

1. State the physical question and mathematical conventions.
2. Derive the formula before calling a simulator.
3. Match each important expression to code.
4. Compare the implementation with an independent reference.
5. Change a parameter or deliberately introduce an error.
6. Record the software version and the limits of the experiment.

Start with [1.1 Problems, inputs, and observable outputs](chapters/ch-what-quantum-computing-computes.md#sec-what-quantum-computing-computes-1). It is an author-checked working draft, with independent review pending. The next drafting assignment is [1.2 A first interference experiment](writing-first-batch.md#12-a-first-interference-experiment). The existing [measurement](chapters/measurement.md), [gradients](chapters/gradients.md), and [VQE](chapters/vqe.md) pages are format pilots, with assumed background, rather than the first-course reading order. Shared [conventions](conventions.md) apply throughout. The [contents](contents.md) and [detailed book plan](book-plan.md) explain the proposed learning sequence, prerequisites and experiments. The [numbered section plans](section-plan.md) give derivation and verification targets. The [Nielsen–Chuang design review](references/nielsen-chuang-design-review.md) records how reference reading informed the revision.

## Scope

FlagQuantum is the implementation framework. Mathematical identities are stated separately from its versioned APIs. Ideal simulation, synthetic shot sampling, and physical hardware experiments must be identified separately. A small model reproducing a paper's calculation does not reproduce its hardware experiment.

The initial runtime target is FlagQuantum 0.3.1, CPU, PyTorch backend, and complex128 statevectors. See the repository README for setup commands.

## Further reading

The [reference reading guide](references/reading-guide.md) introduces six textbooks and lecture-note collections, plus primary papers used by the starter chapters. The [chapter mapping](references/chapter-mapping.md) suggests targeted readings and separates drafted material from the proposed curriculum.
