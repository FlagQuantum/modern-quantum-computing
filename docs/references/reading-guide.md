# Reference reading guide

These resources support the writing and study of *Modern Quantum Computing: A Formula-to-Code Approach*. The reading recommendations below are editorial choices for this book, not claims that the referenced authors endorse FlagQuantum. Core chapters should be understandable without purchasing another textbook.

Use the [chapter mapping](chapter-mapping.md) to choose a reading, or [download the BibTeX bibliography](references.bib). For exact version/section/page targets, use the [all-section proof/source plan](../proof-plan.md) and its [source catalogue](proof-sources.md); this introductory guide is not the detailed proof map. Citation keys are stable identifiers shared by these files. Official resource pages and bibliographic metadata were checked on **October 20, 2026**; access conditions can change.

## Textbooks and lecture notes

### NC — Nielsen and Chuang

**Michael A. Nielsen and Isaac L. Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition. Cambridge University Press.** Key: `nielsen_chuang_2010`.

[Publisher and access options](https://www.cambridge.org/highereducation/books/quantum-computation-and-quantum-information/01E10196D0A682A6AEFFEA52D53BE9AE) · [Official contents](https://www.cambridge.org/highereducation/books/quantum-computation-and-quantum-information/01E10196D0A682A6AEFFEA52D53BE9AE/contents/729A1063B8E18926B2B83C43A9D3F892).

Use as the theoretical backbone: Chapter 2 for states and measurement; Chapters 4–6 for circuits and algorithms; Chapters 8–10 for noise, distance measures and error correction. Our editorial goal is to make the relevant derivations explicit and add independently checked programs. The bibliography uses the publisher's 2010 edition year; individual print and digital formats have later publication dates. Full-text access is normally through purchase or a participating library.

### RP — Rieffel and Polak

**Eleanor G. Rieffel and Wolfgang H. Polak, *Quantum Computing: A Gentle Introduction*. MIT Press, 2011.** Key: `rieffel_polak_2011`.

[Official book page and supplementary-resource links](https://mitpress.mit.edu/9780262015066/quantum-computing/).

Use as a model for explaining the necessary mathematics to readers who know linear algebra but have not studied quantum physics. For our foundations part, emphasize worked calculations and a gradual transition from vectors to quantum states. The publisher provides links to a preface, index, errata and exercise solutions; these are not unrestricted access to the complete book. The bibliography identifies the 2011 hardcover; the paperback appeared in 2014.

### M — Mermin

**N. David Mermin, *Quantum Computer Science: An Introduction*. Cambridge University Press, 2007.** Key: `mermin_2007`.

[Publisher, contents and access options](https://www.cambridge.org/core/books/quantum-computer-science/66462590D10C8010017CF1D7C45708D7).

Use for a focused computational narrative: Chapter 1 introduces classical and quantum bits; Chapters 3 and 4 develop factoring and searching; Chapter 5 covers error correction and Chapter 6 small-register protocols. For our algorithm chapters, prefer a fully explained small example before the general construction. Full-text access depends on purchase or library access. The 2007 print edition and the later online publication are the same bibliographic work.

### P — Preskill

**John Preskill, *Quantum Computation*, Caltech Ph219/CS219 lecture notes.** Key: `preskill_notes`.

[Official course and lecture-note index](https://www.preskill.caltech.edu/ph229/).

Use for physical interpretation and deeper derivations. The current index lists Chapter 2, States and Ensembles (July 2015); Chapter 3, Measurement and Evolution (July 2015); Chapter 5, Classical and Quantum Circuits (July 2015); Chapter 6, Quantum Algorithms (November 2020); and Chapter 7, Quantum Error Correction (March 2026). Older files on the same page use different numbering: cite the chapter title and revision date, not a chapter number alone. The author's site provides public lecture-note downloads; this repository links to them rather than distributing copies.

### SP — Schuld and Petruccione

**Maria Schuld and Francesco Petruccione, *Machine Learning with Quantum Computers*, second edition. Springer, 2021.** Key: `schuld_petruccione_2021`.

[Official book page, contents and access options](https://link.springer.com/book/10.1007/978-3-030-83098-4).

Use for the differentiable-computing part. Particularly relevant chapter titles are *Representing Data on a Quantum Computer*, *Variational Circuits as Machine Learning Models*, and *Quantum Models as Kernel Methods*. Our chapters should connect those modeling questions to tensor shapes, losses and gradient checks. Treat this as a distinct 2021 edition, not an interchangeable citation to the earlier title. Full-text access depends on purchase or an institutional subscription.

### W — Watrous

**John Watrous, *The Theory of Quantum Information*. Cambridge University Press, 2018.** Key: `watrous_2018`.

[Author's manuscript, chapter links and errata](https://cs.uwaterloo.ca/~watrous/TQI/) · [Publisher](https://www.cambridge.org/core/books/theory-of-quantum-information/AE4AA5638F808D2CFEB070C55431D897).

Use as an advanced mathematical reference: Chapters 1–2 for operators, states and channels; Chapter 3 for distances; Chapter 6 for bipartite entanglement. These are extension readings rather than first prerequisites. The author provides a manuscript for personal use only and expressly prohibits sale or redistribution. Link to that page; do not commit the manuscript to this repository.

## Primary papers used by the starter chapters

- **Schuld et al. (2019), *Evaluating analytic gradients on quantum hardware*.** Key: `schuld_gradients_2019`. [Published article](https://doi.org/10.1103/PhysRevA.99.032331). Read alongside the [gradients starter](../chapters/gradients.md). Our elementary cosine derivation illustrates a restricted case; check generator normalization and parameter reuse before applying a shift rule to other circuits.
- **O'Malley et al. (2016), *Scalable Quantum Simulation of Molecular Energies*.** Key: `omalley_2016`. [Published article](https://doi.org/10.1103/PhysRevX.6.031007) · [Corrected arXiv v2](https://arxiv.org/abs/1512.06860v2). The [VQE starter](../chapters/vqe.md) uses the corrected Table I from v2, revised February 4, 2017. Keep the journal citation and the exact data-source revision together. See [source notes](../sources.md) for hashes and scope.

## Review of textbook design

The [Nielsen–Chuang design review](nielsen-chuang-design-review.md) records the preface, contents and selected passages actually examined, the limitations of that review, and the changes it motivates in our chapter plan.

## Web-based learning design

[Quantum Country](https://quantum.country/), by Andy Matuschak and Michael Nielsen, provides a complementary reading-design reference. See our [design review](quantum-country-design-review.md) and [learning specification](../learning-design.md) for observed features, original adaptations and implementation limits. Citation key: `matuschak_nielsen_quantum_country`.

## How authors should use a reference

Read the relevant source, derive the result independently, and give the exact section, theorem or equation locator when adapting a particular argument. Then write original explanations and executable checks using this book's conventions. The mapping is a reading and editorial plan; it does not imply that every listed source has already been studied in full or that every planned chapter is implemented.

Definitions and proofs need explicit assumptions. Numerical checks establish the behavior of tested examples; they do not replace proofs of general statements. FlagQuantum API behavior must be checked against the targeted software release separately from mathematical references.

## Resource policy

Keep citations, official links, reading notes and original explanations in this repository. Do not add third-party textbook PDFs, scanned chapters, publisher figures or solution manuals without an explicit reuse basis and attribution. Public download access alone does not establish redistribution permission. The repository's content license applies to our original material, not to linked works.
