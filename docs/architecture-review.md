# Systematic editorial architecture review

**Review date: 2026-10-20. Scope: all 50 chapters and 435 sections.** This is a completed editorial architecture pass, not external specialist, mathematical-proof, API or reader validation. **New textbook body drafting is paused until the architecture baseline gate is satisfied.**

[Findings and scope decisions](curriculum-audit.md) · [Exact section ledger](section-review.md) · [Checked learning paths](learning-paths.md)

## Findings and dispositions

| ID | Finding | Repair or explicit disposition |
|---|---|---|
| F01 | Definitions arrived after their first operational use: single-qubit probabilities, Pauli matrices and Pauli-specific matrix functions. | State the computational-basis probability postulate in 3.1, define Pauli matrices in 3.3, and keep 2.6 a generic Hermitian-function bridge. |
| F02 | No-cloning required a two-system tensor-product argument before tensor products were introduced. | Move the existing stable section from 3 to 4, after tensor-product structure; preserve old public anchors. |
| F03 | Selective measurement and ignored records risked an unintroduced or invalid statevector average. | Limit 6.2 to selective pure-state updates and marginal probabilities; own density mixtures in 8 and mixed-state instruments in 9. |
| F04 | Phase-based amplitude estimation required jumping from 16 to 17 and back. | Put a phase-free inference example in 16 and move the phase-estimation-based derivation to 17 after QPE; no Chapter 17 prerequisite remains in 16. |
| F05 | The algorithm route lacked Simon’s canonical hidden-structure example and a clear Abelian/discrete-log bridge. | Add explicit optional/core-scoped sections in 15 and 18 with local binary/group/arithmetic bridges. |
| F06 | Qubitization was named but not assigned its own invariant-subspace derivation. | Add a selected Hermitian block-encoding walk construction in 20 before spectral transformation applications. |
| F07 | Quantum information comparison did not clearly cover channel error contracts, mixed entanglement or cryptographic no-go boundaries. | Assign channel metrics/process tomography to 10, mixed-state LOCC/witness/distillation to 12, and a scoped no-go argument to 13. |
| F08 | Calibration and runtime performance risked being confused with experimental device characterization. | Add SPAM/RB in 28 under explicit model assumptions; keep state/process inversion in 10 and runtime timing in 44. |
| F09 | Modern QEC coverage lacked named quantum-LDPC and bosonic-code homes. | Add an architecture-aware LDPC section in 30 and an optional oscillator-correction bridge in 34; both require explicit model/error assumptions. |
| F10 | Optical links and modular hardware were named without a shared networking primitive. | Own pure-state entanglement swapping and classical-message/quantum-link distinctions in 7; mixed-state distillation belongs to 12. |
| F11 | Several whole-chapter prerequisite lists forced unrelated advanced topics before simple entry tasks. | Replace them with entry guidance and a curated direct-prerequisite graph for every section. Validate compiler, kernel, tensor and memory paths against unnecessary-topic regressions. |
| F12 | Compilers and basic physical models inherited QFT, full hardware surveys or broad fault-tolerance routes. | Let 41 enter from circuit semantics and 42 from an explicit target contract; physical branches use selected common bridges and advanced controller/logical tracks have separate requirements. |
| F13 | Fixed kernels inherited trainable-layer prerequisites; MPS became an unnecessary gatekeeper for general contractions. | Create independently checked fixed-kernel and trainable-layer routes; permit general contractions from tensor/circuit tools without 46. |
| F14 | Repeated concepts risked being fully re-taught across foundations, algorithms, hardware, compilation and simulation. | Record a unique explanatory owner for each recurring concept and mark later uses as applications/reminders, with an explicit duplication matrix. |
| F15 | The full plan’s workload had no quantitative planning bound. | Assign provisional section page ranges and compute chapter/route totals. Recommend modular/volume packaging review rather than advertising 50 chapters as a single introductory course. |
| F16 | Basic mathematical/physical tools were sometimes assumed under a broad audience promise. | Assign local probability, calculus, binary algebra, arithmetic/group, oscillator and rotating-frame bridges before use, with exact section dependencies. |
| F17 | Small algorithm demonstrations could imply stronger preparation, verification or complexity claims. | State eigenstate-overlap cost in QPE, scoped promise/QMA limits in 22 and the expensive tiny-reference boundary in linear-system examples. |
| F18 | Chapter titles had been treated as sufficient evidence of coverage and learning continuity. | Publish the all-section ledger, chapter-specific decisions and prerequisite-closed routes; require independent specialist/source and reader validation before freeze. |
| F19 | The H2 reduction and logical-memory source selection still have unresolved scholarly scope. | Keep exact molecular-source/reduction mapping and the Chapter 50 primary-claim selection as explicit outstanding gates; do not write around them with invented evidence. |
| F20 | The roadmap still allowed new depth/body pilots before the user’s architecture-first requirement was met. | Pause new body drafting. Continue architecture, source mapping and validation design only until the baseline gate is satisfied. |

## Every-chapter review and provisional workload

Ranges are editorial planning estimates for explanatory text, examples and exercises; they are not measured reading time or completed page counts. They use per-section budgets and exclude appendices/front matter. Advanced modules can be omitted from an introductory route.

| Chapter | Sections | Planned pages | Specific architecture decision |
|---|---|---|---|
| 1 | 6 | 12–24 | Retain an informal preview with supplied rules; do not pretend formal measurement/evolution has already been established. Revisit the calculation after 3–6. |
| 2 | 8 | 16–32 | Remove the premature Pauli specialization from matrix-function introduction. Own linear algebra/norm/tolerance foundations; statistical and physical bridges have named later homes. |
| 3 | 7 | 14–28 | State the single-qubit probability postulate before interference/Bloch use. Introduce Pauli matrices before their algebra; move no-cloning to the tensor-product chapter. |
| 4 | 8 | 16–32 | Own subsystem/index conventions and now the no-cloning proof after tensor products. Runtime gate kernels are developed in 44 rather than re-derived here. |
| 5 | 8 | 16–32 | Retain introductory reversible logic, universality and small identities. Advanced synthesis algorithms and pass correctness are owned by 41–42. |
| 6 | 9 | 19–37 | Repair selective versus ignored-outcome language: no averaging statevectors. Introduce probability/independence before estimator claims; full mixed-state instruments belong to 8–9. |
| 7 | 9 | 18–36 | Add entanglement swapping/network-resource primitives. Derive no-signalling from marginal probabilities first; mixed-state entanglement is deferred to 12. |
| 8 | 8 | 16–32 | Own ensembles, reduced states, purification and unconditioned density updates. Entry does not require completing every protocol or Bell-test topic in 7. |
| 9 | 8 | 16–32 | Retain representation equivalence and complete-positivity arguments. This is the channel/instrument owner, not a duplicate physical-noise catalogue. |
| 10 | 9 | 20–38 | Add channel/gate comparison contracts and process tomography. Treat shadows and advanced channel norms as optional inference branches; device characterization protocols are owned by 28. |
| 11 | 8 | 17–33 | Retain entropy/relative entropy/data processing with explicit support and proof scope. Do not require tomography/shadows before basic entropy. |
| 12 | 9 | 27–45 | Add mixed-state entanglement/LOCC/witness/distillation reasoning and distinguish finite experiments from capacity theorems. Keep specialized full capacity proofs as scoped advanced readings. |
| 13 | 9 | 27–45 | Scope a complete QKD path and add an explicit cryptographic no-go boundary. Remove the requirement to complete all channel-capacity theory before the protocol entry. |
| 14 | 9 | 18–36 | Retain input/output, access, complexity and complete costs plus the hybrid map. Separate comparison assumptions from empirical advantage claims. |
| 15 | 8 | 16–32 | Restore Simon’s problem and a local binary-equation bridge. Oracle construction remains explicit; general hidden-subgroup structure is owned by 18. |
| 16 | 8 | 19–35 | Replace the forward phase-estimation dependency with a locally introduced phase-free inference method. Move the phase-estimation-based derivation to 17 and preserve its stable ID. |
| 17 | 9 | 19–37 | Own QFT/QPE and the phase-based amplitude-estimation extension in sequence. Make eigenstate-overlap/preparation cost explicit; no ground-state-preparation claim follows from QPE alone. |
| 18 | 9 | 27–45 | Add an advanced Abelian hidden-subgroup/discrete-log example with a local group/arithmetic bridge. Keep non-Abelian representation theory outside the core route. |
| 19 | 9 | 20–38 | Remove the unnecessary QFT/QPE entry requirement for time evolution/product formulas. Retain adiabatic assumptions and operator/state/observable error distinctions. |
| 20 | 9 | 27–45 | Add the missing qubitization invariant-subspace derivation between block encodings and QSP/QSVT. Keep access, normalization, conditioning and postselection costs visible. |
| 21 | 9 | 27–45 | Retain a complete scalar-to-matrix signal-processing path; one proved application plus explicit advanced theorem scope. Do not duplicate polynomial derivations in the walk chapter. |
| 22 | 9 | 27–45 | Separate algorithm design, query lower bounds and Hamiltonian-complexity limits. Add a scoped promise/QMA boundary without turning small optimizer experiments into complexity evidence. |
| 23 | 10 | 21–41 | Retain spectral/shared-parameter differentiation with a local calculus bridge. Parameterized tensor contracts are owned here; learning/encoding claims belong to 27. |
| 24 | 9 | 27–45 | Remove full state-inference prerequisites from optimizer entry. Geometry, trainability theorems and noisy-gradient arguments are branches with exact section requirements. |
| 25 | 12 | 28–52 | Mark the long chemistry/embedding chapter as a core energy/model path plus independent advanced modules. Do not force embedding, dynamics or sampled-subspace methods before the H2 capstone. |
| 26 | 8 | 24–40 | Retain objective mapping, alternating circuits and honest solution metrics. Reuse optimization tools from 24 rather than re-teach optimizers. |
| 27 | 8 | 17–33 | Make fixed-kernel/feature and trainable-layer paths independent. Fixed kernels must not inherit quantum backpropagation prerequisites; include data-access and evaluation bridges. |
| 28 | 10 | 21–41 | Own physical-noise assumptions, calibration and device characterization. Add SPAM/RB with its own local ensemble/model assumptions; runtime timing benchmarks are owned by 44. |
| 29 | 9 | 18–36 | Retain the full correction-condition/recovery argument and coherent error-span logic. Teach the first bit-and-phase construction without requiring undeveloped CSS terminology. |
| 30 | 11 | 23–45 | Add quantum-LDPC/check/connectivity tradeoffs. Keep three separable branches: stabilizer codes, measurement-based graph states and decoder interfaces; introduce binary/group tools locally. |
| 31 | 8 | 24–40 | Retain repeated syndrome circuits, boundaries, decoder and logical failure definitions. Threshold/scaling evidence remains model-specific; shared syndrome algebra is referenced from 30. |
| 32 | 8 | 24–40 | Remove factoring and full surface-code prerequisites from the generic logical-gate route. Require surface-code material only for surgery, and retain explicit threshold/magic-state assumptions. |
| 33 | 8 | 24–40 | Remove all-algorithm prerequisites. A named logical workload and logical-operation/error models suffice; actual decomposition algorithms remain in 42. |
| 34 | 10 | 21–41 | Retain a common physical bridge, now with an optional bosonic-correction module. Do not require QFT, every noise topic or every code family before basic hardware models. |
| 35 | 8 | 24–40 | Keep a self-contained effective circuit/transmon branch using selected common physics. Detailed BCS/device fabrication remains out of scope; compiler algorithms are referenced rather than repeated. |
| 36 | 8 | 24–40 | Keep the local oscillator/sideband/drive bridge and explicit motion-return/transport costs. Avoid cost-free connectivity assumptions and unrelated algorithm prerequisites. |
| 37 | 8 | 24–40 | Retain distinct digital, analog and motion contracts. The adiabatic theorem is developed in 19; a Rydberg device model does not imply arbitrary graph programmability. |
| 38 | 9 | 27–45 | Separate optical modes, encoded qubits, conditional gates, graph-state computation and optional CV material. Require only the relevant graph-state/oscillator sections for each branch. |
| 39 | 8 | 24–40 | Retain a local effective spin/exchange/readout model with explicit omitted levels. No whole chemistry, Fourier or fault-tolerance route is needed for entry. |
| 40 | 8 | 24–40 | Retain a theory-first, evidence-qualified advanced branch. Majorana/fermionic and protection/logical supplements have separate prerequisites; full tensor-category theory is an explicit exclusion. |
| 41 | 9 | 18–36 | Remove microscopic hardware from program/IR entry. Own program semantics, dynamic maps, rewrites and interchange boundaries; optional derivative checks use the differentiation bridge. |
| 42 | 10 | 21–41 | Remove whole-platform prerequisites from mapping/scheduling entry: an explicit target contract suffices. Own synthesis/mapping algorithms; logical-set approximation is an optional prepared branch. |
| 43 | 10 | 30–50 | Separate control, local dynamic feedback, logical lowering and host workflow tracks. Runtime orchestration must not require pulse optimization, and decoder feedback need not traverse every logical-gate chapter. |
| 44 | 8 | 16–32 | Make the minimal exact-state executor accessible before AD and density evolution. Own execution/parallel-runtime benchmarks, not experimental RB error characterization. |
| 45 | 8 | 24–40 | Make tableau entry depend on Pauli/stabilizer sections, not all error-correction or numerical-executor topics. Defer magic-resource extensions explicitly. |
| 46 | 8 | 24–40 | Retain the SVD/Schmidt-to-MPS argument. Pure-state construction needs neither tomography nor all density/gradient execution; compare truncation with declared metrics. |
| 47 | 10 | 30–50 | Remove MPS as a prerequisite for general circuit contraction. Keep contraction and cutting/reconstruction as distinct branches, with all signed-weight/statistical overhead explicit. |
| 48 | 9 | 18–36 | Allow scientific specification and paper-reading habits early. Statistical/resource and application tools are selected for a claim rather than requiring whole advanced courses. |
| 49 | 9 | 27–45 | Require only the energy/mapping/gradient and research sections needed by the selected H2 calculation. Full molecular reduction/source locators still need review; embedding/learning are not prerequisites. |
| 50 | 9 | 27–45 | Remove logical universality/resource-estimation prerequisites from the memory experiment. Resource extrapolation is optional; selecting a primary claim/source remains an explicit unresolved gate. |

The whole reference architecture budgets **1088–1958 pages before appendices/front matter**. This does not fit a single introductory course. Use the route-specific selections; assess coordinated volume packaging before freezing publication scope.

## What has and has not passed

- Editorial coverage/ownership pass: all 50 chapters and 435 sections recorded.
- Exact prerequisite graph: 1042 direct edges, each earlier than its use; no cycles or unresolved section references.
- Learning paths: 19 explicit routes reconstructed from prerequisites and checked for missing entry knowledge.
- Specialist validation, exact theorem/source acceptance, complete cross-layer programs and target-reader testing remain pending.
- Scope/volume choice and a tagged architecture freeze remain pending; no new body chapters are authorized by this audit alone.
