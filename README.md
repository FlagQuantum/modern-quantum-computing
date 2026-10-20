# Modern Quantum Computing: A Formula-to-Code Approach

*Theory, Algorithms, and Reproducible Experiments with FlagQuantum*

**Wei Liu** · [liuwei01@baai.ac.cn](mailto:liuwei01@baai.ac.cn)

FlagQuantum Team · Beijing Academy of Artificial Intelligence (BAAI)

**Version 0.1.0-draft.4 · 2026-10-20**

An open English textbook that connects quantum computing equations to executable programs and independent numerical checks.

**Status: early draft.** This repository contains a nine-part, 50-chapter plan, shared conventions, and three starter chapters. It is not a complete textbook. The examples target **FlagQuantum 0.3.1** on CPU with complex128 precision; newer releases require revalidation.

## Start reading

- [Book introduction](docs/index.md)
- [Quantum-classical hybrid patterns and implementations](docs/hybrid-computing.md)
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
python scripts/check_prose.py
```

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md), the [chapter template](templates/chapter.md), and [ROADMAP.md](ROADMAP.md). Corrections to derivations, independently checked examples, and reader feedback are especially welcome.

Text and original illustrations: [CC BY 4.0](LICENSE-CONTENT.md). Code: [MIT](LICENSE). Third-party data and sources retain their own rights; see [source notes](docs/sources.md).
