## Appendices and companion laboratories

- **A. Mathematical and Physical Bridges:** probability, asymptotics, selected algebra, oscillator mathematics, elementary circuit/atomic/optical models and selected proofs. Required local bridges also appear before their first use in the main text.
- **B. Matrix Calculus and Differentiation Conventions:** complex derivatives, adjoints and PyTorch contracts.
- **C. FlagQuantum Runtime Contracts and Interoperability:** versioned APIs, compiler interfaces and serialization. Compilation theory and algorithms belong in Chapters 41–43.
- **D. Experiment Records and Benchmark Protocols:** manifests, uncertainty, comparison workloads and reproducibility.
- **E. Platform Access Laboratories:** installation, accelerators, distributed execution and provider access. Physical encodings, control and device constraints belong in Chapters 34–40.
- **F. Problems, Selected Solutions and Reproduction Worksheets:** stable problem identifiers and reader/teacher support.

The bibliography, symbol index, glossary, errata and acknowledgements are separate back matter. Hardware credentials are optional. Essential explanations, proof steps and answers remain usable offline.

## Dependencies and course routes

The numbered arrangement is a reference structure. The authoritative [19 learning paths](learning-paths.md) list exact sections, assumed earlier routes and all required preparation. They are generated from the same stable section records as this plan. Do not maintain a second, conflicting course sequence in prose.

The [435-section review ledger](section-review.md) records each section's direct prerequisites, core/advanced level and editorial disposition. Chapter prerequisite prose is entry guidance, not a requirement to complete every section of every listed chapter. Later specialized sections can have additional dependencies without blocking an earlier core task.

The opening route develops mathematics, pure states, tensor products, gates, measurement, entanglement, mixed states and basic computational resources. First algorithms then progress through oracle problems, search/phase-free estimation, Fourier/phase estimation, arithmetic and dynamics. Phase-based amplitude estimation is now 17.8, after its phase-estimation prerequisites; it no longer forces a return to Chapter 16. Pure-state no-cloning is now 4.7, after tensor products.

Fixed quantum kernels, trainable hybrid learning, basic compilation, simulation and hardware branches have separate entry contracts. A selected physical model is useful for a hardware-to-compiler project but is not required before learning basic program semantics or mapping on a supplied target. Logical-memory simulation does not require universal fault tolerance or magic-state factories. H2 VQE does not require every embedding or quantum-learning extension.

## Ownership and scope control

The [curriculum audit](curriculum-audit.md) owns the coverage, duplication and deliberate-exclusion matrices. Develop a recurring concept fully in its owning section; later applications give an exact pointer, recall the necessary statement and explain the new use. New derivations belong in the later section only when its assumptions or mathematical object actually change.

Chapter 7 uses marginal probabilities for no-signalling; Chapter 8 supplies the reduced-state proof. Chapter 19 supplies the adiabatic bridge. Graph-state and adaptive measurement-based gates are in 30.10 before photonic use. Chapter 33 states abstract resource parameters before platform chapters explain their origins. Experimental SPAM/randomized benchmarking belongs to 28, state/process reconstruction to 10, and simulator timing to 44.

The additions from this pass give scoped homes to entanglement swapping, channel metrics/process reconstruction, mixed-state entanglement, cryptographic no-go boundaries, Simon's algorithm, an Abelian hidden-subgroup/discrete-log bridge, qubitization, Hamiltonian promise/verification limits, experimental characterization, quantum LDPC codes and bosonic correction. Their scope is stated in the section targets; mentioning an advanced result does not promise a complete research monograph.

## Workload and publication architecture

The [seven-volume proposal](volume-plan.md) is the recommended packaging overlay. It preserves global chapter numbers, stable IDs and web links while placing Chapter 14 after the foundational sequence, Chapter 48 before the capstones, and 49/50 in their application volumes. Direct prerequisites fit the proposed volume and internal chapter order; no section requires a later volume.

The [proof-depth plan](proof-plan.md) replaces uniform page allowances with result-specific budgets. The reference argument now budgets **1,296–2,546 pages before shared appendices/front matter**; adding 24–40 pages per volume gives **1,464–2,826 pages**, excluding substantial shared appendices/solutions. These are editorial ranges, not measured typeset lengths. They do not authorize scope compression or imply a one-semester course.

The foundation/information split avoids a combined opening volume of up to 738 planned pages. Volumes follow coherent subjects: foundations; information; algorithms; hybrid scientific computing; noise/correction; physical realizations; programming/compilation/simulation. Select one complete learning route rather than reading every specialization in sequence. The detailed proposal specifies all chapter allocations, cross-volume imports and alternatives; final packaging needs reader/typesetting calibration.

## Architecture-first acceptance gates

A complete editorial architecture pass is recorded in the [review report](architecture-review.md): 50 chapter decisions, 435 section dispositions, 1,045 direct prerequisite edges and 19 checked routes. These checks establish record consistency and expose prerequisite burden; they do not prove the explanations teach successfully.

Before new body drafting:

1. Review the assigned central-result/proof obligations and exact source locators; transcribe/check the precise statements and deferred lemmas before acceptance.
2. Obtain specialist review of coverage, ownership and mathematical/physical assumptions; record the actual sections reviewed.
3. Test representative routes and bridge/transition specifications with target readers. Record the precise missing steps and required repairs.
4. Set workable page, example and substantial-problem budgets; resolve volume and course packaging.
5. Resolve findings and tag a versioned architecture baseline with a public change record.

**No new textbook body or depth-pilot drafting while these architecture gates remain open.** Existing three starter chapters remain available as evidence of the format. Source mapping, architectural repairs and validation design can continue; they do not constitute authorization to write new chapters. After the baseline, prioritize a continuous opening and selected complete routes, not isolated topical additions.

## Research anchors and source work

The [reading guide](references/reading-guide.md), [compilation/platform sources](references/compilation-and-platforms.md), [hybrid sources](references/hybrid-computing.md) and [systematic-review source notes](references/architecture-review.md) document consulted scope. Course outlines and paper abstracts support coverage comparisons; they do not certify proofs, API support or experimental results. Every authored result needs exact edition/revision and theorem/equation locators plus its independent verification plan.

The [H2 integral-to-reduced-model provenance plan](references/h2-provenance.md) now records nine checked stages and an independent 54-geometry, 324-coefficient reconstruction at published rounding precision. Original author integral files were not recovered. The [topological experimental evidence ledger](references/topological-experiments.md) selects nine claim-specific cases, including paired critique/reply and retraction records; the [full public argument audit](references/topological-dispute-review.md) now compares nine disputes across preprint, accepted-manuscript and public-rebuttal versions. Exact final-journal-reply matching and independent interpretation remain open. Chapter 50 now selects Fowler et al. v2, Section VII A/Fig. 5 for syndrome ambiguity; its finite memory benchmark is an explicitly labeled extension, not reproduction of the paper's threshold curves. A rounded small-model reproduction cannot stand in for all molecular data or a hardware experiment.

## Stable identifiers and history

Canonical records are book/curriculum.json and book/architecture-review.json. Run scripts/build_curriculum.py, scripts/review_curriculum.py and scripts/build_scholarly_plan.py to generate views; their --check options detect stale outputs and graph/route inconsistencies. IDs remain stable across display renumbering. A split or merge requires an explicit map, prerequisite/route updates and preserved or redirected public anchors.

The former 40-chapter/328-section plan lacked substantial hardware and compilation routes. The expanded 50-chapter/423-section plan received this full editorial pass and now has 435 sections. Historical design reviews remain records, not current allocations. Existing public section anchors are retained, including moved sections. Current starter homes are 6, 23 and 49; the published three-chapter PDF retains its own sample numbering and source/version provenance.
