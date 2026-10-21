# Modern Quantum Computing: A Formula-to-Code Approach

*Theory, Algorithms, and Reproducible Experiments with FlagQuantum*

**Wei Liu** · [liuwei01@baai.ac.cn](mailto:liuwei01@baai.ac.cn)

FlagQuantum Team · Beijing Academy of Artificial Intelligence (BAAI)

**Version 0.1.0-draft.4 · 2026-10-20**

An open English textbook that connects quantum computing equations to executable programs and independent numerical checks.

**Status: early draft.** This repository contains a nine-part, 50-chapter plan, shared conventions, working drafts of sections 1.1–1.6, 2.1–2.8, 3.1–3.7 and 4.1, and three earlier starter chapters. It is not a complete textbook. The examples target **FlagQuantum 0.3.1** on CPU with complex128 precision; newer releases require revalidation.

## Two entry points: learners and agents

The [dual-entry plan](docs/dual-entry.md) connects the textbook to a proposed [agent capability and chapter map](docs/agent-skills.md). Read the chapters for definitions and derivations; use the planned task contracts to select implementations and evidence for a bounded task. The six-level catalog maps all 50 chapters and 435 sections to 23 proposed task skills. The first [state/operator comparison prototype](docs/comparison-skill-prototype.md) has completed [independent agent blind testing](docs/comparison-skill-blind-evaluation.md): 11 fresh tasks passed after a runtime-contract repair, with 45 author regression cases and three actual FlagQuantum executions. Scientific acceptance remains pending. **No skill package is released yet.**

[Skill contract and evaluation](docs/skill-contract.md) · [Paper reproduction verification and acceptance](docs/paper-reproduction-standard.md). Source understanding, algorithm implementation, numerical reproduction and hardware repetition have distinct evidence requirements. This planning overlay does not change the textbook curriculum or its review states.

## Start reading

- [Executable writing baseline 1.0](docs/writing-baseline.md) · [Full 435-section writing queue](docs/writing-order.md) · [First-chapter briefs](docs/writing-first-batch.md)
- [Read 1.1: Problems, inputs, and observable outputs](docs/chapters/ch-what-quantum-computing-computes.md#sec-what-quantum-computing-computes-1) · working draft; independent review pending
- [Read 1.2: A first interference experiment](docs/chapters/ch-what-quantum-computing-computes.md#sec-what-quantum-computing-computes-2) · real-amplitude derivation and verified FlagQuantum example
- [Read 1.3: What a quantum state describes](docs/chapters/ch-what-quantum-computing-computes.md#sec-what-quantum-computing-computes-3) · state, measurement setting and data
- [Read 1.4: Algorithms, simulators, and physical devices](docs/chapters/ch-what-quantum-computing-computes.md#sec-what-quantum-computing-computes-4) · one task and explicit execution evidence
- [Read 1.5: What computational advantage would require](docs/chapters/ch-what-quantum-computing-computes.md#sec-what-quantum-computing-computes-5) · matched tasks and complete cost accounting
- [Read 1.6: A map of the learning routes](docs/chapters/ch-what-quantum-computing-computes.md#sec-what-quantum-computing-computes-6) · route selection and executable prerequisite checks
- [Read 2.1: Complex scalars, vectors, and conjugation](docs/chapters/ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-1) · component proofs and independent coordinate checks
- [Read 2.2: Inner products, adjoints, and orthogonality](docs/chapters/ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-2) · full projection/Cauchy–Schwarz proofs and tensor checks
- [Read 2.3: Linear maps, bases, and changes of coordinates](docs/chapters/ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-3) · similarity proof, coordinate contracts and counterexamples
- [Read 2.4: Hermitian, unitary, and positive operators](docs/chapters/ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-4) · quadratic-form proofs, norm preservation and counterexamples
- [Read 2.5: Spectral decomposition and singular values](docs/chapters/ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-5) · full Hermitian/SVD proofs, rectangular kernels and reconstruction checks
- [Read 2.6: Functions of matrices and time evolution](docs/chapters/ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-6) · spectral calculus, exponential convergence and unitary evolution
- [Read 2.7: Norms, conditioning, and perturbations](docs/chapters/ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-7) · error amplification, perturbation bounds and small-residual counterexample
- [Read 2.8: Floating-point arithmetic and verification contracts](docs/chapters/ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-8) · scale-aware tolerances, metadata checks and Chapter 2 synthesis
- [Read 3.1: The pure-state postulate and physical equivalence](docs/chapters/ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-1) · normalization, Born probabilities and phase-aware comparisons
- [Read 3.2: Relative phase and interference](docs/chapters/ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-2) · full complex cross-term derivation, shifted analyzers and runnable phase scans
- [Read 3.3: The Bloch-sphere representation](docs/chapters/ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-3) · Pauli coordinates, full sphere/inverse proofs and original geometric illustration
- [Read 3.4: Closed-system evolution and generators](docs/chapters/ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-4) · unitary postulate, Hermitian generator and verified constant evolution
- [Read 3.5: Pauli algebra and rotation matrices](docs/chapters/ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-5) · product table, full rotation derivations and tested angle/phase conventions
- [Read 3.6: Composing rotations](docs/chapters/ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-6) · gate order, complete ZYZ proof, endpoint cases and phase-tracked reconstruction
- [Read 3.7: Physical phase versus numerical equality](docs/chapters/ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-7) · comparison scope, controlled-phase counterexample and Chapter 3 synthesis
- [Read 4.1: Tensor-product spaces and basis states](docs/chapters/ch-composite-systems-tensor-products-and-qubit-ordering.md#sec-composite-systems-tensor-products-and-qubit-ordering-1) · finite construction, product-basis proofs and verified complex amplitudes
- [Book introduction](docs/index.md)
- [Quantum-classical hybrid patterns and implementations](docs/hybrid-computing.md)
- [Core results, proof depth and exact sources](docs/proof-plan.md) · [Adopted seven-volume plan](docs/volume-plan.md)
- [Systematic architecture review](docs/architecture-review.md) · [435-section ledger](docs/section-review.md) · [19 learning paths](docs/learning-paths.md)
- [Curriculum audit and freeze gates](docs/curriculum-audit.md) · [Reader continuity](docs/reader-continuity.md)
- [Editorial charter](docs/editorial-charter.md) · [FlagQuantum capability-gap workflow](docs/implementation-roadmap.md)
- [Full contents: nine parts and 50 chapters](docs/contents.md) · [Detailed chapter plan](docs/book-plan.md) · [Numbered section plans](docs/section-plan.md)
- [Design review: Nielsen and Chuang](docs/references/nielsen-chuang-design-review.md) · [Quantum Country](docs/references/quantum-country-design-review.md)
- [Learning design: recall, prediction and formula-to-code practice](docs/learning-design.md)
- [Notation and conventions](docs/conventions.md)
- [Reference reading guide](docs/references/reading-guide.md) · [Chapter mapping](docs/references/chapter-mapping.md) · [BibTeX bibliography](docs/references/references.bib)
- [Measurement and expectation values](docs/chapters/measurement.md)
- [Parameterized circuits and gradients](docs/chapters/gradients.md)
- [Molecular hydrogen VQE: from a paper to code](docs/chapters/vqe.md)

Every starter chapter connects **equation → derivation → implementation → verification → exercises**. Expected values come from analytical expressions or independent dense linear algebra, rather than from the simulator alone.

The curriculum follows the subject, including modern algorithms, information theory, fault-tolerant computation, quantum compilation and physical-platform branches. Required missing FlagQuantum capabilities are investigated and tracked upstream; they do not restrict the theoretical scope. Existing runnable examples retain their explicit validation status.

## Run the examples

From the repository root, with Python 3.12:

```bash
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements-examples.txt
python examples/foundations/task_contracts.py  # standard library; no package installation needed
python examples/foundations/interference.py
python examples/foundations/state_descriptions.py
python examples/foundations/execution_evidence.py
python examples/foundations/advantage_ledger.py  # standard library; hypothetical cost ledger
python examples/foundations/learning_routes.py  # standard library; checks the planned reading graph
python examples/foundations/complex_coordinates.py  # standard library; complex arithmetic and proofs
python examples/foundations/inner_products.py
python examples/foundations/basis_changes.py
python examples/foundations/operator_classes.py
python examples/foundations/spectral_svd.py
python examples/foundations/matrix_functions.py
python examples/foundations/conditioning.py
python examples/foundations/verification_contracts.py
python examples/foundations/pure_states.py
python examples/foundations/relative_phase.py
python examples/foundations/bloch_sphere.py
python examples/foundations/closed_evolution.py
python examples/foundations/pauli_rotations.py
python examples/foundations/composing_rotations.py
python examples/foundations/phase_contracts.py
python examples/foundations/tensor_spaces.py
python scripts/check_formula_code.py
python examples/measurement.py
python examples/gradients.py
python examples/omalley2016/verify_h2_vqe.py
```

The initial validation environment uses Python 3.12, PyTorch 2.13.0, NumPy 2.5.4 and FlagQuantum 0.3.1 on macOS ARM64 CPU. Linux CI checks the same examples; accelerator support is outside this draft's validation scope.

## Build the book locally

```bash
python -m pip install -r requirements-docs.txt
python -m mkdocs serve
```

Open the local URL printed by MkDocs. Use `python -m mkdocs build --strict` for a release check. GitHub Pages deployment is a separate, manually triggered workflow. No custom domain is configured yet.

## PDF sample edition

[Download PDF](https://github.com/FlagQuantum/modern-quantum-computing/releases/download/v0.1.0-draft.4/modern-quantum-computing.pdf) · [LaTeX source bundle](https://github.com/FlagQuantum/modern-quantum-computing/releases/download/v0.1.0-draft.4/modern-quantum-computing-source.tar.gz) · [Release and build manifest](https://github.com/FlagQuantum/modern-quantum-computing/releases/tag/v0.1.0-draft.4)

The print sample is generated from the same chapters and checked-in Python examples. It includes author information, a versioned cover, contents, numbered display equations, references, paired formulas/code and selected implementation listings. Complete examples accompany the source archive. See [editions and publication](docs/publication.md) for build commands and the manual PDF workflow. The generated LaTeX source bundle supports later scholarly preparation; this sample is not an arXiv submission.

## Check planning and explanatory prose

Run the following checks after changing the plan or drafted chapters. The prose scan requires human review and cannot establish that all derivations are complete.

```bash
python scripts/build_curriculum.py --check
python scripts/review_curriculum.py --check
python scripts/build_scholarly_plan.py --check
python scripts/check_prose.py
```

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md), the [chapter template](templates/chapter.md), and [ROADMAP.md](ROADMAP.md). Corrections to derivations, independently checked examples, and reader feedback are especially welcome.

Text and original illustrations: [CC BY 4.0](LICENSE-CONTENT.md). Code: [MIT](LICENSE). Third-party data and sources retain their own rights; see [source notes](docs/sources.md).
