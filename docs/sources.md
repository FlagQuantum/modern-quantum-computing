# Sources and validation

## Primary paper

P. J. J. O'Malley et al., *Scalable Quantum Simulation of Molecular Energies*, Physical Review X 6, 031007 (2016). [DOI](https://doi.org/10.1103/PhysRevX.6.031007).

The examples use the author-corrected [arXiv:1512.06860v2](https://arxiv.org/abs/1512.06860v2), revised February 4, 2017. This version corrects identity coefficients in Table I. `examples/omalley2016/source-provenance.json` records source hashes; `h2-table.csv` contains the transcribed numerical data. Scientific facts and data are attributed here; no paper figures or full article text are redistributed.

## Origins and scope

The hydrogen scripts were developed for the [FlagQuantum Wiki reproduction tutorial](https://github.com/flagos-ai/FlagQuantum/wiki/Reproducing-Molecular-Hydrogen-VQE), then incorporated into this textbook with a new chapter structure. The Wiki remains an additional detailed reading resource.

Initial local validation: Python 3.12, FlagQuantum 0.3.1, PyTorch 2.13.0, NumPy 2.5.4, Matplotlib 3.11.2, macOS ARM64, CPU, complex128. The repository CI runs deterministic checks on Linux. No GPU, distributed, cloud or physical hardware execution is certified by this draft.

The reference curve is a calculation using the rounded paper table. It is not experimental data. The saved reference manifest records the original generating environment rather than the current reader's environment.

## Attribution and licensing

Original book prose is CC BY 4.0 and repository-authored code is MIT. These licenses do not relicense the cited paper or any third-party material. Cite the original scientific work when using its model or data.

## Bibliography and reading paths

The [reading guide](references/reading-guide.md) identifies reference editions, official access links and editorial uses. The [chapter mapping](references/chapter-mapping.md) connects readings to existing and planned chapters. [Download the BibTeX bibliography](references/references.bib) for six textbook/lecture-note entries and two primary papers. Citation keys identify sources; chapters still need precise locators for any specific result they adapt.
