# Curriculum architecture audit and freeze gates

**October 20, 2026: full editorial architecture pass completed; external validation and freeze pending.** All 50 chapters and the earlier 423 sections were reviewed; 12 scoped additions give 435 sections. New textbook body drafting is paused until the baseline gate. This is an editorial review, not an assertion of exhaustive coverage or specialist approval.

- [Review report: findings, 50 chapter decisions and workload](architecture-review.md)
- [All 435 sections: direct prerequisites and editorial dispositions](section-review.md)
- [19 learning paths with prerequisite closure](learning-paths.md)
- [Detailed learning/derivation and evidence targets](section-plan.md)

## Coverage and responsibility

| Area | Main responsibility | Scope and boundary |
|---|---|---|
| Foundations | 1–8: mathematical bridges, states, tensor products, gates, measurement, entanglement and mixtures | Probability postulate and Pauli definitions precede use; no-cloning follows tensor products; ignored records are density mixtures rather than averaged statevectors |
| Information | 9–13: channels, inference, entropy, communication, mixed entanglement and security | Channel/process metrics, LOCC/witnesses/PPT and cryptographic no-go scope are explicit; limited examples do not prove general security/capacity |
| Algorithms and models | 14–22: cost/access models, oracles, search, estimation, Fourier/arithmetic, dynamics, block encodings, qubitization/QSVT and complexity | Simon and Abelian/discrete-log examples have local algebra bridges; selected QMA/Hamiltonian promises delimit claims; analog/adiabatic bridge is 19.8 |
| Quantum-classical computing | Early map in 14.7; method homes in 10, 23–27, 43 and 47 | [Eight composable patterns](hybrid-computing.md): subroutine pipelines, outer-loop optimization, trainable/fixed learning, dynamic feedback, inference, fragment reconstruction, embedded solvers and heterogeneous execution |
| Differentiation and applications | 23–27: gradients, optimization/geometry, chemistry, QAOA and learning | Fixed kernels have an independent entry; embedding, dynamics and sample-based diagonalization are optional branches rather than H2 prerequisites |
| Noise and correction | 28–33: physical errors, characterization, code conditions, stabilizers, decoding, fault tolerance and resources | SPAM/RB includes its ensemble/noise assumptions; LDPC/code-connectivity tradeoffs are explicit; memory experiments precede optional universal-FT machinery |
| Physical realization | 34 shared physics/target models; 35 superconducting; 36 trapped ions; 37 neutral atoms; 38 photonics; 39 spins; 40 topological theory/candidates | Shared oscillator/control bridges and optional bosonic correction; choose one platform; theoretical protection, physical candidates and demonstrated operations have separate evidence |
| Quantum compilation | 41 semantics/IR/optimization; 42 synthesis/mapping/routing/scheduling; 43 control/dynamic/logical/runtime lowering | Basic compilation uses an explicit abstract target, without requiring all hardware physics or QFT; advanced lowering has separate prerequisites |
| Simulation | 44 exact execution; 45 stabilizer; 46 MPS; 47 general contractions/cutting | Basic executor before differentiation; tableau from stabilizer tools; MPS is not required before generic contractions; cutting is not coherent networking |
| Research | 48 source/claim/verification methods; 49 H2 VQE; 50 logical memory | H2 source chain and 324-coefficient regeneration are checked at printed precision, with original author integral files unavailable; the memory case selects Fowler v2 Section VII A/Fig. 5, with a declared finite-benchmark extension; no invented execution or experimental evidence |

Platform installation, provider credentials and evolving API details remain versioned companion laboratories. Essential theory and independent checks remain available offline.

## Duplicate derivations and intentional revisits

| Recurring subject | Owner of the main derivation | Later responsibility |
|---|---|---|
| Gate identities/universality | 5 | 41–42 add semantics, algorithms and error-bounded synthesis; 33 accounts for logical costs |
| Measurement/channels | 6 selective pure-state updates; 8 mixtures; 9 full instruments/channels | 28 assigns physical error models; 43 lowers classical feedback and readout contracts |
| Statistical estimation | 6 estimator bridge; 10 state/process reconstruction | 28 develops device-characterization assumptions; 44 measures runtime; applications reuse uncertainty tools |
| Entanglement/SVD | 7 pure-state structure and swapping; 8 reductions; 12 mixed-state resources | 46 derives MPS truncation bounds; 47 develops contraction costs; networking applications reuse the resource statements |
| Differentiation/optimization | 23 derivative rules; 24 optimization and geometry | 25–27 and 43 explain changed objectives/constraints without four repeated optimizer tutorials |
| Stabilizer/logical algebra | 29 code conditions; 30 stabilizers and graph states | 31 specializes geometry/decoding; 32 gives fault-tolerance scope; 38 applies measurement-based gates; 45 builds tableau algorithms |
| Hardware-to-program contract | 34 common model and 35–40 local physical origins | 42 consumes constraints for compilation; 43 derives control and timing consequences |
| Reproducible evidence | 48 full method, with small local records throughout | 49–50 execute source-specific capstones rather than repeat generic manifest tutorials |

An intentional revisit must name what changes: the mathematical object, assumptions, proof strength or implementation contract. A brief recall and exact pointer are preferable to an unmarked duplicate proof.

## Deliberate boundaries

These decisions prevent scope from growing through disconnected topical additions. They may be revisited with a learning objective, prerequisite/workload assessment and an owner.

| Nearby field | Included bridge | Outside the present full-treatment commitment |
|---|---|---|
| Quantum sensing/metrology | Estimation, Fisher/geometry tools and cost reasoning | A complete sensing/instrumentation course and platform metrology survey |
| Quantum networks | Swapping, mixed-state distillation and modular/link contracts | A complete repeater/network protocol stack, routing/security engineering and deployment survey |
| Complexity | Access/promise models, lower bounds, selected BQP/QMA/Hamiltonian problems | Full representation theory/non-Abelian HSP, QIP/MIP* and a complexity-theory monograph |
| Physical engineering | Local circuit/atomic/optical/spin/oscillator models, loss/leakage and control assumptions | Full fabrication, microscopic materials/BCS theory and spectroscopy courses |
| Cryptography | Precisely scoped information-theoretic arguments and no-go boundaries | Production cryptographic implementations or security certification |
| Chemistry | Hamiltonian/mapping/ansatz/reduction reasoning and traceable selected molecular data | A complete integral-generation, electronic-structure or chemical-accuracy pipeline |
| Advanced codes | Selected LDPC and bosonic constructions, assumptions, checks and tradeoffs | An exhaustive coding research survey or a claim that one code family wins universally |

## Learning order and overload findings

The [review report](architecture-review.md) records 20 findings and their dispositions. Major order repairs include moving no-cloning after tensor products and phase-based amplitude estimation after QPE. Device characterization, network primitives and selected modern algorithm/code topics now have scoped homes. Every section has curated direct prerequisites; transitive closure adds only needed preparation to each selected route.

The graph has **1,045 direct edges**, no forward dependencies or cycles, and **19 checked routes**. Regression checks protect basic compiler, fixed-kernel, general-contraction, H2 and logical-memory entry paths from unrelated advanced prerequisites. These are structural checks; a reader can still encounter an unexplained argument in prose that has not yet been written.

The proof-depth revision now plans **1,296–2,546 pages before shared appendices/front matter** make the whole reference unsuitable as one introductory course. Common foundations plus selected branches are the teaching architecture. The [seven-volume proposal](volume-plan.md) gives a dependency-compatible allocation and proof-specific budgets; final packaging, examples/problems and learner workload remain acceptance decisions. The range is an editorial estimate, not a rendered page count.

## Cross-layer validation designs

After the baseline, recurring tasks will test circuit-to-target compilation, dynamic correction, a host-driven hybrid loop, cut/reconstructed expectation, logical rotation and physical control. Their specifications must state inputs/outputs, branch probabilities, units, semantics, error/sampling costs and independent references. Confirmed implementation gaps follow the [upstream workflow](implementation-roadmap.md); missing APIs do not remove required theory.

The current phase may refine these specifications and source maps. It does not start new body chapters or depth-pilot prose.

## Freeze gates and change control

| Gate | Evidence and present status |
|---|---|
| Editorial coverage/ownership | Completed for all 50 chapters/435 sections; exclusions and duplication decisions recorded; specialist assessment pending |
| Section dependency architecture | Curated direct graph, complete ledger and 19 structurally checked routes completed; prose first-use and actual reader testing pending |
| Selected source exceptions | [H2 provenance](references/h2-provenance.md) and [topological evidence](references/topological-experiments.md) now have checked claim-level ledgers; [full public arguments](references/topological-dispute-review.md) reviewed; exact final-reply matching, device-data/model reanalysis and independent scientific acceptance remain open |
| Mathematical depth | [435 result/proof/source records](proof-plan.md) assigned; exact statements, deferred lemmas and independent mathematical/source acceptance remain pending |
| Cross-layer contracts | Planning targets recorded; independent complete programs and actual API verification remain pending |
| Workload and accessibility | Proof-specific budgets and [seven-volume allocation](volume-plan.md) proposed; examples/problems, reader evidence and final packaging pending |
| Baseline freeze | Resolve review findings, record specialist/reader scope and tag an architecture baseline; pending |

**No new textbook body or depth-pilot drafting until the architecture baseline gate is satisfied.** The three existing starters remain format evidence. A successful build or a larger table of contents does not pass the outstanding gates.

Stable IDs are held in book/curriculum.json and review dispositions in book/architecture-review.json. Regenerate both sets of views after structural edits, validate routes and preserve public anchors. A split/merge needs an explicit mapping and rationale; published editions keep their frozen sources. Reassess scope at least annually and on significant corrections, without pretending any curriculum is permanently complete.
