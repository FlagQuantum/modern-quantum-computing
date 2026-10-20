# Modern Quantum Computing

## A Formula-to-Code Approach

*Theory, Algorithms, and Reproducible Experiments with FlagQuantum*

How does an equation in a quantum computing paper become a working program? This open textbook follows that translation explicitly: define the conventions, derive a small result, implement it, and check the answer independently.

**Early draft:** three starter chapters are available. The full plan comprises six parts and 28 chapters; the remaining chapters are proposed material, not completed text.

<!-- book-metadata:start -->
**Wei Liu**

FlagQuantum Team

Beijing Academy of Artificial Intelligence (BAAI)

Beijing, China

Correspondence: [liuwei01@baai.ac.cn](mailto:liuwei01@baai.ac.cn)

**Version 0.1.0-draft.2 · 2026-10-20 · Draft**
<!-- book-metadata:end -->

## Who this book is for

Readers who know basic Python and linear algebra and want to understand quantum computing through calculations they can reproduce. Familiarity with complex numbers, matrix multiplication, eigenvalues and elementary derivatives is helpful. A planned foundations part will review these topics; it is not yet written.

## How to use a chapter

1. State the physical question and mathematical conventions.
2. Derive the formula before calling a simulator.
3. Match each important expression to code.
4. Compare the implementation with an independent reference.
5. Change a parameter or deliberately introduce an error.
6. Record the software version and the limits of the experiment.

Start with [conventions](conventions.md), then [measurement](chapters/measurement.md), [gradients](chapters/gradients.md), and [VQE](chapters/vqe.md). The [contents](contents.md) and [detailed book plan](book-plan.md) explain the proposed learning sequence, prerequisites and experiments. The [Nielsen–Chuang design review](references/nielsen-chuang-design-review.md) records how reference reading informed the revision.

## Scope

FlagQuantum is the implementation framework. Mathematical identities are stated separately from its versioned APIs. Ideal simulation, synthetic shot sampling, and physical hardware experiments must be identified separately. A small model reproducing a paper's calculation does not reproduce its hardware experiment.

The initial runtime target is FlagQuantum 0.3.1, CPU, PyTorch backend, and complex128 statevectors. See the repository README for setup commands.

## Further reading

The [reference reading guide](references/reading-guide.md) introduces six textbooks and lecture-note collections, plus primary papers used by the starter chapters. The [chapter mapping](references/chapter-mapping.md) suggests targeted readings and separates drafted material from the proposed curriculum.
