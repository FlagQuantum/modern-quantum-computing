# Editions, authorship and publication

## Author and affiliation

**Wei Liu**

FlagQuantum Team

Beijing Academy of Artificial Intelligence (BAAI)

Beijing, China

The canonical author, affiliation, version and date are in `book/metadata.json`. Run `python scripts/build_book.py --web-metadata` after changing them, and commit the resulting introduction update. Contributor acknowledgements and any future changes to authorship should reflect actual contributions.

## Two reading formats

The website follows the living Markdown chapters. The PDF is a fixed sample edition built from the same chapter text and the executable Python files, with a cover, contents, numbered sections and display equations, references, and complete core code listings. Wide web tables are rendered as consecutive labeled formula/code blocks for print.

The first edition is **0.1.0-draft.1**, dated **2026-10-20**. It contains three starter chapters plus conventions, reproduction notes and the hydrogen model/verification listing. It is not a complete course or an arXiv submission.

## Build locally

Validated print tools: **Pandoc 3.12.1** and **Tectonic 0.17.0**. Install them from their official distributions; Tectonic may download TeX resources on its first run. The script itself uses only Python's standard library.

```bash
python scripts/build_book.py --web-metadata
python -m pip install -r requirements-docs.txt
python -m mkdocs build --strict
python scripts/build_book.py
```

Set `TECTONIC` to the compiler path when it is not on PATH. Use `python scripts/build_book.py --tex-only` to generate sources without compiling. Generated files are ignored by Git:

- `output/pdf/modern-quantum-computing.pdf`: the sample book.
- `output/pdf/book.tex`: standalone LaTeX with embedded references and listings.
- `output/pdf/modern-quantum-computing-source.tar.gz`: the source archive.
- `output/pdf/manifest.json`: version, source commit, modification status and output hashes.

Build formal release artifacts from a clean commit. Rebuilding may change PDF bytes with the compiler's timestamps; numerical reproducibility is established separately by the example checks.

## Publication workflow

The manual **Build PDF sample** workflow compiles the book and uploads the PDF, standalone sources, log and manifest as a downloadable workflow artifact. Review every page before attaching a PDF/source bundle to a numbered GitHub release. The separate **Publish book (manual)** workflow deploys the website after GitHub Pages is configured for Actions. No custom domain is required to build either format.

## Preparing a later arXiv edition

A scholarly edition needs a coherent scope, reviewed derivations, accurate references, tested code, rights for included material and a reviewed author list. Retain the LaTeX sources for submissions generated from TeX, and check the then-current [arXiv submission instructions](https://info.arxiv.org/help/submit/index.html) and [TeX instructions](https://info.arxiv.org/help/submit_tex.html). The generated archive is a source starting point, not a claim that a submission has been accepted or all platform checks have passed.

This project uses generative-AI assistance in drafting and tooling. The sample PDF discloses that assistance. Before scholarly submission, the named author should review the full manuscript, its attribution and validation evidence, and check the applicable [arXiv moderation guidance](https://info.arxiv.org/help/moderation/index.html). arXiv moderation is not peer review.
