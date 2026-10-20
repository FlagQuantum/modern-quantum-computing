## Appendices and companion laboratories

- **A. Mathematical and Physical Bridges:** probability, asymptotics, selected algebra, oscillator mathematics, elementary circuit/atomic/optical models and selected proofs. Required local bridges also appear before their first use in the main text.
- **B. Matrix Calculus and Differentiation Conventions:** complex derivatives, adjoints and PyTorch contracts.
- **C. FlagQuantum Runtime Contracts and Interoperability:** versioned APIs, compiler interfaces and serialization. Compilation theory and algorithms belong in Chapters 41–43.
- **D. Experiment Records and Benchmark Protocols:** manifests, uncertainty, comparison workloads and reproducibility.
- **E. Platform Access Laboratories:** installation, accelerators, distributed execution and provider access. Physical encodings, control and device constraints belong in Chapters 34–40.
- **F. Problems, Selected Solutions and Reproduction Worksheets:** stable problem identifiers and reader/teacher support.

The bibliography, symbol index, glossary, errata and acknowledgements are separate back matter. Hardware credentials are optional. Essential explanations, proof steps and answers remain usable offline.

## Dependencies and course routes

The numbered order is one reference-book arrangement. It is not a requirement to read all 50 chapters consecutively. The common core and explicit branch routes give the learner a continuous path without requiring every specialization.

| Route | Sequence and bridges | Intended outcome |
|---|---|---|
| Opening core | 1–8, with local mathematics bridges; selected 9–10 and 14 | State, gate, measurement, information and resource reasoning |
| First algorithms | 14–15, 16.1–16.5, 17, then 16.6–16.8 and selected 18–19 | Complete search, estimation and Fourier-based explanations without a hidden forward prerequisite |
| Information course | 7–13, after the necessary foundations | Channels, inference, entropy, communication and security assumptions |
| Modern algorithms | 14–22, supported by 2–6 and 9–10 | Algorithm derivations, access models, error and complete resource cost |
| Differentiable applications | 23–27, with 10, 14 and selected 19/28 | Gradients, trainability, variational/learning objectives and baselines |
| Error correction | 28–33, after 7–10; graph-state material in 30 links back to teleportation | From noise and correction conditions to logical operations and resource models |
| Hardware-to-compiler course | 34, one of 35–40, then 41–42; 43 after 19, 23, 28 and 32–33 | Model and control a selected physical platform, compile a task and validate the whole contract |
| Platform comparison | 34 and guided comparison sections from 35–40 | Compare encodings, constraints and evidence without taking every advanced branch |
| Classical simulation | 30, 44–47, with 2, 4, 7–10, 14 and 23 | Exact/structured simulation, approximation and tractability |
| Research | 48, then 49 or 50 after its application prerequisites | A scoped, independently checked paper reproduction |

A 14-week course selects sections from a route. The full curriculum is a reference and multi-course project. Page budgets, core/advanced allocation and possible multi-volume publication must be assessed at the architecture-review gate; they are not fixed by chapter count.

Chapter 7 first derives no-signalling from marginal probabilities and revisits the reduced-state proof after Chapter 8. Chapter 19 supplies a scoped adiabatic-model bridge; Chapter 30 introduces graph states and measurement-based gates before photonic computation. Chapter 33 introduces physical resource parameters as explicit abstract assumptions; Chapters 34–40 explain their platform-specific origins and limits.

## Ownership of recurring concepts

| Concept | First development | Later use without duplicate derivation |
|---|---|---|
| Gate identities and simple universality | 5 | Compiler correctness and synthesis in 41–42 |
| Channels and conditional operations | 6, 8–9 | Noise (28), hardware readout and dynamic compilation |
| Entanglement and teleportation | 7–8 | Coding, graph-state computation, photonics and topology |
| Time evolution and approximation | 19 | Hardware effective models and control-level lowering |
| Gradients and optimization | 23–24 | Variational applications and pulse optimization in 43 |
| Stabilizers and logical computation | 29–32 | Photonic/topological branches, logical compilation and simulation |
| Resource/error budgets | 14, 19, 28, 33 | Hardware comparison, compiler objectives and research reports |
| Physical experiment/target contract | 34 and one selected platform | Mapping, scheduling and control in 41–43 |
| Independent execution/reference methods | Small local references throughout; general methods in 44–47 | Full research capstones in 49–50 |

## Planning review before substantial drafting

The [curriculum audit](curriculum-audit.md) records the remaining gates. The expanded architecture is **not frozen** and has not yet received specialist or learner approval.

1. Review coverage and chapter ownership, including compilation, physical platforms, alternative computational models and the interfaces between them.
2. Audit first use of concepts, prerequisite bridges, section transitions and explicit learning outcomes using the [reader-continuity standard](reader-continuity.md).
3. Check depth and workload with algorithm, information, compilation, hardware and error-correction specialists; record the actual scope reviewed.
4. Test the opening core and representative cross-layer routes with target readers. Record where a reader cannot reconstruct a step.
5. Resolve missing bridges, overload and redundant material; assign provisional page/problem budgets and freeze a versioned architecture baseline.
6. Begin sustained chapter drafting against that baseline. Use stable chapter/section IDs and a public change record for later revisions.

Small existing pilots supply evidence for this review. They do not establish that the full architecture, every proof or every experiment has been validated.

## Writing priorities after the review gate

Complete the opening sequence (1–8), then depth pilots in measurement (6), differentiation (23), correction (29), and a hardware-to-compiler thread (34, selected 35–40, 41–42). Expand channels/inference, resources and the first algorithm path. Develop the VQE research route through 48–49. Draft specialized branches with exact sources and explicit proof obligations; complete simulation and the logical-memory capstone (50) as their prerequisites are available.

This is a writing sequence rather than an importance ranking. Missing FlagQuantum capabilities are investigated upstream while mathematical explanations and independent references are developed.

## Research anchors and source work

The earlier [reading guide](references/reading-guide.md) supports the foundations. [Compilation and physical-platform source notes](references/compilation-and-platforms.md) identify primary author references and official specifications used to scope the added routes. These are starting points, not claims of complete source or proof review.

Additional anchors include [QSVT](https://arxiv.org/abs/1806.01838), [surface codes](https://arxiv.org/abs/1208.0928v2), and [classical shadows](https://arxiv.org/abs/2002.08953). Each authored section needs exact theorem/equation locators, assumptions and an independent verification plan. Hardware performance and scientific-maturity comparisons require dated, claim-specific evidence.

## Stable identifiers, compatibility and history

The canonical records are in the repository's book/curriculum.json; display numbers and detailed pages are generated by scripts/build_curriculum.py. Stable chapter/section IDs are independent of display numbering. Check generated views with the script's --check option.

The earlier 40-chapter, 328-section plan omitted substantive hardware and compilation routes. This revision adds those routes and two computational-model bridges. The original simulation/research URLs retain legacy chapter and section anchors; current navigation points to stable chapter IDs. Published PDF samples retain their own numbering, source revision and validated scope.

The historical Nielsen–Chuang and Quantum Country reviews remain design records rather than the current chapter allocation. Current starter homes are **6, 23 and 49**; each requires expansion and review.
