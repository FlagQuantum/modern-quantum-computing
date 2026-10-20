# Writing roadmap

[Writing Baseline 1.0](docs/writing-baseline.md) is adopted for editorial execution: **50 chapters, 435 stable sections, 19 reader routes, seven volumes and 16 ordered writing batches**. The full theory and proof obligations remain in their owning sections. Baseline adoption is not a claim that prose, proofs, API support or reader validation are complete.

## Next writing assignment

Sections [1.1–1.6](docs/chapters/ch-what-quantum-computing-computes.md) now have working drafts and author-executed independent references; 1.2–1.4 also compare with released FlagQuantum 0.3.1. Independent mathematical, implementation and target-reader review remain pending. Section [2.1](docs/chapters/ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-1) now supplies full component proofs and author-executed coordinate checks. Draft **2.2 Inner products, adjoints, and orthogonality** next, following its frozen contract and [writing queue](docs/writing-order.md). Chapter 1 now has six drafts; this is not chapter acceptance. The existing measurement, gradients and H2 pages remain format pilots until expanded at their scheduled chapter homes.

The [full queue](docs/writing-order.md) lists every section exactly once, in prerequisite-safe production order. The [reader routes](docs/learning-paths.md) remain separate: a writing batch is not a requirement that students read all earlier production batches.

## Adopted production order

| Batches | Work |
|---|---|
| B01–B02 | Chapters 1–8 and 14: a continuous foundational course and Volume I |
| B03 | The independent exact-execution/measurement bridge |
| B04–B05 | Oracles/search, Fourier/arithmetic and Hamiltonian dynamics |
| B06 | Gradients, optimization, molecular modelling and a complete H2 route |
| B07 | Core programming and compilation on explicit abstract targets |
| B08–B10 | Complete information/security, hybrid methods and spectral algorithms |
| B11–B12 | Noise, code conditions, decoding and finite memory, then fault tolerance/resources |
| B13–B15 | Shared physical models/superconducting branch, remaining compiler/control and alternative platforms |
| B16 | Remaining exact/stabilizer/MPS/tensor methods and series integration |

Exact section targets, automatically inserted prerequisite bridges and exit targets are in the baseline and queue. Never silently skip an imported section or turn an optional specialization into a prerequisite for a core route.

## Start, draft and accept

- Before drafting a section, complete its brief, establish usable prerequisite explanations, inspect the exact local source target and define an independent check.
- A working draft may support the next draft when its imported results and conventions are explained and no known blocking error remains. This does not make either section accepted.
- Before publication acceptance, record separate mathematical, implementation or justified N/A, and target-reader evidence. Complete examples, formula-to-code correspondence, expected outputs, transfer tasks and accessible answers are part of acceptance.
- Follow the existing P/F/M/R/V depth contracts. Do not compress a central proof to fit a preferred page count or claim a theorem was proved by numerical agreement.
- Missing FlagQuantum APIs use the [confirmed-capability-gap workflow](docs/implementation-roadmap.md). Required theory and independent references continue; unsupported framework execution stays pending.

## Scope and change control

The operational baseline replaces the previous all-series drafting pause. Pending specialist or reader evidence is gathered on actual sections and routes; it does not require the entire unwritten series to pass review before Chapter 1 can begin.

Keep the existing nine-part curriculum and seven-volume chapter allocation. Any material scope, depth, dependency, priority or placement change needs an impact record, a baseline revision and regenerated views. Preserve stable IDs and public anchors. Physical trim and empirical page/problem budgets are calibrated during authoring.

**No further standalone paper audit is scheduled.** Existing source-audit records remain archived references. Inspect only the exact source claims needed by the section being authored; qualify or omit an optional disputed hardware example without blocking unrelated work.

## Release milestones

A batch first produces a coherent working route, then passes its acceptance checks. Volume publication follows accepted content and accepted prerequisite imports, not the completion of every unrelated specialization. Website and PDF must tell the same scientific argument; the current 16-page sample keeps its existing draft version until an explicit publication build.

Use [book/writing-progress.json](book/writing-progress.json) for actual work states and review evidence. Do not advance a state by counting planned headings, source links or synthetic checks as finished prose or independent review.
