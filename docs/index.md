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

## Two entries into the same knowledge base

| Goal | Start here |
|---|---|
| Learn the mathematics and translate formulas into code | [Textbook contents](contents.md) and [learning paths](learning-paths.md) |
| Plan a bounded agent task or paper reproduction | [Dual-entry design](dual-entry.md), [skill capability map](agent-skills.md) and [verification/acceptance standard](paper-reproduction-standard.md) |

The agent entry has **four independent-agent-tested prototypes** among 23 proposed task skills, zero released packages: [state/operator comparison](comparison-skill-prototype.md). Its [blind evaluation](comparison-skill-blind-evaluation.md) passed 11 fresh tasks after a runtime repair. The second [single-qubit interference skill](interference-skill-prototype.md) passed 35 author cases and 12 new blind-agent tasks. The third [phase-tracked unitary evolution skill](unitary-evolution-skill-prototype.md) passed 53 author cases and 12 blind tasks with unit clarification and controlled phase repair. The fourth [complex linear algebra skill](complex-algebra-skill-prototype.md) passed 55 author cases and 12 blind tasks, separating classical validation from routed actual FlagQuantum execution. Author execution, agent behavior and scientific acceptance remain separate records. It shares the textbook's scientific sources, conventions, implementations and evidence. A mapped chapter or an executable example does not establish an accepted skill. No new textbook section is written by this planning update.

## Educational aim

Our aim is a rigorous modern classic that helps present and future learners enter quantum computing. The [editorial charter](editorial-charter.md) sets standards for depth, accessibility, review and long-term maintenance. The curriculum includes foundations, quantum information, modern algorithms, differentiable computing, fault tolerance, physical implementations, quantum compilation, simulation and reproducible research.

The subject determines the scope. Required missing capabilities are investigated and reported through the [FlagQuantum capability-gap workflow](implementation-roadmap.md); existing API coverage does not limit the theory. Current sample execution claims remain pinned to their tested release.

A [systematic editorial architecture review](architecture-review.md) covers all 50 chapters and 435 sections, with an [exact prerequisite ledger](section-review.md) and [19 learning paths](learning-paths.md). [Writing Baseline 1.0](writing-baseline.md) now fixes scope, depth, volumes and a [435-section production queue](writing-order.md). Independent section/route acceptance remains pending; [reader continuity](reader-continuity.md) is an explicit acceptance standard.

The [all-section result/proof/source plan](proof-plan.md) and [adopted seven-volume plan](volume-plan.md) specify the scholarly scope and publication structure. These remain planning artifacts; mathematical/source and learner review are pending.

The [quantum-classical hybrid map](hybrid-computing.md) connects eight composable algorithm/runtime patterns, their implementation contracts and their chapter homes.

## Who this book is for

Readers who know basic Python and linear algebra and want to understand quantum computing through calculations they can reproduce. Familiarity with complex numbers, matrix multiplication, eigenvalues and elementary derivatives is helpful. The foundational course is being drafted; consult [contents and status](contents.md) for the actual section progress.

## How to use a chapter

1. State the physical question and mathematical conventions.
2. Derive the formula before calling a simulator.
3. Match each important expression to code.
4. Compare the implementation with an independent reference.
5. Change a parameter or deliberately introduce an error.
6. Record the software version and the limits of the experiment.

Start with [1.1 Problems, inputs, and observable outputs](chapters/ch-what-quantum-computing-computes.md#sec-what-quantum-computing-computes-1). It is an author-checked working draft, with independent review pending. Continue with [1.2 A first interference experiment](chapters/ch-what-quantum-computing-computes.md#sec-what-quantum-computing-computes-2), including a released FlagQuantum comparison. Then read [1.3 What a quantum state describes](chapters/ch-what-quantum-computing-computes.md#sec-what-quantum-computing-computes-3), comparing state descriptions, measurement settings and data. [1.4 Algorithms, simulators, and physical devices](chapters/ch-what-quantum-computing-computes.md#sec-what-quantum-computing-computes-4) traces one task through code, simulation and a proposed experiment. [1.5 What computational advantage would require](chapters/ch-what-quantum-computing-computes.md#sec-what-quantum-computing-computes-5) audits a hypothetical cost comparison. [1.6 A map of the learning routes](chapters/ch-what-quantum-computing-computes.md#sec-what-quantum-computing-computes-6) connects concrete goals to prerequisite-checked paths. These are working drafts. Continue with the working draft [2.1 Complex scalars, vectors, and conjugation](chapters/ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-1). Then read [2.2 Inner products, adjoints, and orthogonality](chapters/ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-2), also a working draft. [2.3 Linear maps, bases, and changes of coordinates](chapters/ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-3) now derives coordinate conversion and similarity. The working draft [2.4 Hermitian, unitary, and positive operators](chapters/ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-4) separates quadratic-form and norm conditions. The working draft [2.5 Spectral decomposition and singular values](chapters/ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-5) proves Hermitian diagonalization and rectangular SVD. The working draft [2.6 Functions of matrices and time evolution](chapters/ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-6) derives spectral functions and constant-Hermitian evolution. The working draft [2.7 Norms, conditioning, and perturbations](chapters/ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-7) relates residuals to condition-dependent error bounds. The working draft [2.8 Floating-point arithmetic and verification contracts](chapters/ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-8) closes Chapter 2 with numerical contracts and synthesis problems. The working draft [3.1 The pure-state postulate and physical equivalence](chapters/ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-1) connects state-description postulates, probabilities and phase-aware comparison. The working draft [3.2 Relative phase and interference](chapters/ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-2) derives complex interference terms and checks shifted-analyzer predictions. The working draft [3.3 The Bloch-sphere representation](chapters/ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-3) derives pure-state sphere coordinates and their inverse, including pole cases. The working draft [3.4 Closed-system evolution and generators](chapters/ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-4) connects unitary dynamics, Hermitian generators and a verified constant-Hamiltonian example. The working draft [3.5 Pauli algebra and rotation matrices](chapters/ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-5) derives Pauli products and half-angle rotations with explicit active Bloch-coordinate checks. The working draft [3.6 Composing rotations](chapters/ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-6) derives ZYZ parameters, endpoint conventions and phase-tracked circuit reconstruction. The working draft [3.7 Physical phase versus numerical equality](chapters/ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-7) distinguishes whole-state and operator phase contracts and proves the controlled-context limitation. Chapter3 now has seven working drafts with independent acceptance pending. The working draft [4.1 Tensor-product spaces and basis states](chapters/ch-composite-systems-tensor-products-and-qubit-ordering.md#sec-composite-systems-tensor-products-and-qubit-ordering-1) constructs the finite product space and verifies ordered complex amplitudes. The next drafting assignment is [4.2 Registers, labels, and basis indices](section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2). The existing [measurement](chapters/measurement.md), [gradients](chapters/gradients.md), and [VQE](chapters/vqe.md) pages are format pilots, with assumed background, rather than the first-course reading order. Shared [conventions](conventions.md) apply throughout. The [contents](contents.md) and [detailed book plan](book-plan.md) explain the proposed learning sequence, prerequisites and experiments. The [numbered section plans](section-plan.md) give derivation and verification targets. The [Nielsen–Chuang design review](references/nielsen-chuang-design-review.md) records how reference reading informed the revision.

## Scope

FlagQuantum is the implementation framework. Mathematical identities are stated separately from its versioned APIs. Ideal simulation, synthetic shot sampling, and physical hardware experiments must be identified separately. A small model reproducing a paper's calculation does not reproduce its hardware experiment.

The initial runtime target is FlagQuantum 0.3.1, CPU, PyTorch backend, and complex128 statevectors. See the repository README for setup commands.

## Further reading

The [reference reading guide](references/reading-guide.md) introduces six textbooks and lecture-note collections, plus primary papers used by the starter chapters. The [chapter mapping](references/chapter-mapping.md) suggests targeted readings and separates drafted material from the proposed curriculum.
