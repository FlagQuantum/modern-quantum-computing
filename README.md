# Modern Quantum Computing: A Formula-to-Code Approach

*Theory, Algorithms, and Reproducible Experiments with FlagQuantum*

An open English textbook that connects quantum computing equations to executable programs and independent numerical checks.

**Status: early draft.** This repository contains a book plan, shared conventions, and three starter chapters. It is not a complete textbook. The examples target **FlagQuantum 0.3.1** on CPU with complex128 precision; newer releases require revalidation.

## Start reading

- [Book introduction](docs/index.md)
- [Contents and chapter status](docs/contents.md)
- [Notation and conventions](docs/conventions.md)
- [Measurement and expectation values](docs/chapters/measurement.md)
- [Parameterized circuits and gradients](docs/chapters/gradients.md)
- [Molecular hydrogen VQE: from a paper to code](docs/chapters/vqe.md)

Every starter chapter connects **equation → derivation → implementation → verification → exercises**. Expected values come from analytical expressions or independent dense linear algebra, rather than from the simulator alone.

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

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md), the [chapter template](templates/chapter.md), and [ROADMAP.md](ROADMAP.md). Corrections to derivations, independently checked examples, and reader feedback are especially welcome.

Text and original illustrations: [CC BY 4.0](LICENSE-CONTENT.md). Code: [MIT](LICENSE). Third-party data and sources retain their own rights; see [source notes](docs/sources.md).
