# Curriculum architecture audit and freeze gates

**Revision: October 20, 2026. Status: editorial self-audit; specialist and reader review pending.** This audit follows the author's identification of missing substantive quantum-compilation and physical-platform content. The current [curriculum](contents.md) has nine parts and 50 chapters. Its size is not evidence that the architecture is complete.

## Coverage decisions

| Area | Home and responsibility | Review status |
|---|---|---|
| Foundations and quantum information | 1–13: postulates, mathematics, protocols, channels, inference, entropy, coding/security | Section targets specified; exact proof/source maps and workload review pending |
| Algorithmic models and resources | 14–22: gate/oracle models, search, estimation, arithmetic, dynamics, block encodings, QSVT, walks/lower bounds | Section targets specified; advanced proof selection pending |
| Other computational models | Adiabatic bridge in 19; graph-state/measurement-based bridge in 30; analog and optical models in 34, 37–38 | Bridges added; specialist review and route testing pending |
| Quantum-classical integration | [Eight-pattern map](hybrid-computing.md), introduced in 14.7; inference, optimization/learning, embedding, adaptive feedback, reconstruction and heterogeneous execution | Cross-cutting map and method-specific sections specified; mathematical/API/workflow review pending |
| Differentiable and variational computation | 23–27: spectral derivatives, optimization/geometry, chemistry, QAOA, learning | Section targets specified; three current starters do not complete this route |
| Noise, correction and logical computation | 28–33: physical error models through correction, decoding, fault tolerance and physical-resource budgets | Section targets specified; proof, noise-model and workload review pending |
| Physical realization | 34 common bridge; 35 superconducting; 36 trapped ions; 37 neutral atoms; 38 photonics; 39 semiconductor spins; 40 topology/candidates | Formal main-text routes added; source scoping only, no comprehensive platform review claimed |
| Quantum compilation | 41 program semantics/IR/optimization; 42 synthesis/mapping/routing/scheduling; 43 control/dynamic/logical lowering | Formal main-text route added; API audit and worked pipeline pending |
| Classical simulation | 44–47: exact, stabilizer, MPS and contraction methods | Targets specified; independent implementations and specialized review pending |
| Research practice | 48 methods; 49 H2 VQE; 50 logical memory | H2 starter exists; correction-study primary source still to be selected |

Platform software installation and provider access remain companion laboratories. Physical models, native interactions, compilation correctness and scheduling algorithms are in the main text.

## Platform worksheet and evidence discipline

Every platform branch answers the same questions: what encodes the information; which physical Hilbert space and effective model are assumed; how preparation, control, entanglement and readout work; what noise/leakage/loss is represented; which constraints the compiler receives; and which result the independent reference checks.

Topological codes, non-Abelian theoretical models and candidate physical realizations require separate explanations. A source's proposal, a model calculation, a measured signature, a controlled operation and demonstrated logical computation are different claims. The chapter must supply dated, claim-specific evidence. No ranking of present platform maturity is asserted by this plan.

Semiconductor spins are included alongside the five requested routes. Further encodings, device families, bosonic protection and network architectures can appear as comparisons or research extensions after a coverage review; no finite list is exhaustive.

## Dependency and first-use ledger

| Potential break in learning | Planned repair | Remaining acceptance evidence |
|---|---|---|
| Probability estimates before the learner has statistical tools | Local estimator/coverage development in 6, with Appendix A references | Reader reconstructs an uncertainty calculation |
| Schmidt decomposition before reduced density matrices | Develop SVD/pure-state structure in 7; reduced spectra in 8 | A worked reconstruction and explicit revisit |
| Amplitude estimation before phase estimation | Read 16.1–16.5, then 17, then 16.6–16.8 | Route review confirms no hidden forward dependency |
| Analog computation without adiabatic assumptions | Dedicated 19.8 bridge and a declared small model | Source theorem, assumptions and counterexample reviewed |
| Photonics before measurement-based theory | Graph states and adaptive gates in 30.9, linked to teleportation | All conditional branches derived before photonic use |
| Hardware chapters assuming unseen physics | Common oscillator/drive/measurement bridge in 34 and local circuit/atomic/optical/spin bridges | First-use physics and notation audit for each chosen branch |
| Resource chapter requiring every hardware specialty | 33 states abstract parameters; 34 explains their origin; comparison uses selected branch summaries | Complete example with assumptions and sensitivity |
| Compilation without a physical target contract | 34 plus one branch before 41–42; 43 adds control/logical prerequisites | One complete target description and semantic-preservation test |
| Hybrid computation reduced to a trainable quantum layer | Eight composable patterns, with host/controller/device boundaries and an early 14.7 map | Each chosen pattern has an independent contract, total-cost record and a transfer task |
| Physical transport treated as a cost-free logical SWAP | Platform models distinguish motion, interaction, mapping and output interpretation | Target-specific schedule/resource comparison |
| Broad hardware tour interrupting the first course | Common core plus a selected branch; no sequential requirement to master 35–40 | Tested introductory and hardware/compiler course routes |

This ledger is a review agenda, not a declaration that the missing bridges have already been written.

## Cross-layer pilot specifications

| Pilot | Scope | Acceptance target |
|---|---|---|
| One entangling-state preparation | Abstract circuit to two contrasting explicitly modeled targets | Exact logical contract, input/output map, legal operations, timing assumptions and independent reference |
| One dynamic measurement/correction | Conditional branches through classical control and readout | Branch probabilities/maps, correction record, latency and no silent postselection |
| One host-driven hybrid loop | Objective/estimator or embedded solve across classical and quantum tasks | Typed records, independent reference, checkpoint/state, latency and all sampling/classical costs |
| One cut/reconstructed result | A declared observable from smaller fragment executions | Exact uncut comparison, signed coefficients, variance/shot costs and no claim of coherent distributed execution |
| One logical rotation | Approximate synthesis to a declared logical gate set and resource model | Error budget, T/factory/scheduling cost and traceable assumptions |
| One physical-control calculation | Effective multilevel or coupled-mode dynamics | Units, frame convention, truncation convergence, leakage/loss interpretation and reference solver |

Pilots may reveal software requirements. Confirmed gaps follow the [upstream issue workflow](implementation-roadmap.md); pending software does not erase the theoretical objective.

## Scope, duplication and workload

Chapter 5 owns introductory gate identities and universality; 41–43 develop compiler semantics, algorithms and target lowering. Chapter 19 owns basic time evolution and approximation; physical chapters derive their model-specific interactions. Chapters 29–32 own stabilizer/logical theory; photonic/topological branches apply or extend it with explicit extra assumptions.

Before freezing the architecture, assign provisional page, worked-example and substantial-problem budgets. Check the complete opening, a full algorithm route and a hardware-to-compiler route for overload. Decide whether the publication should be one reference book or a coordinated volume sequence only after that review; no volume split is declared here.

## Freeze gates and change control

| Gate | Required evidence | Current status |
|---|---|---|
| Coverage and chapter ownership | Specialist-informed matrix with justified exclusions and no unowned core topic | Self-audit drafted; external review pending |
| Dependency and continuity | Section-level first-use ledger and complete bridge/transition checks | Ledger drafted; full audit pending |
| Mathematical depth | Exact statements, proof plans and primary-source locators for depth pilots | Pending |
| Executable cross-layer contracts | Small independent references and confirmed capability reports | Pending |
| Workload and accessibility | Page/problem budgets and target-reader route evidence | Pending |
| Baseline freeze | Resolved findings, recorded review scope, tagged plan and change log | Pending |

Do not treat a successful website build, large section count or authoring template as passing these gates. Small pilots can develop while the architecture is reviewed; sustained full-chapter production follows the baseline gate.

Stable IDs are held in book/curriculum.json. Current display numbers are generated from the record. Reorganizing content must retain IDs or publish an explicit split/merge map, update prerequisites and course routes, preserve or redirect public anchors, and explain why the change is necessary. Published editions keep their frozen sources.
