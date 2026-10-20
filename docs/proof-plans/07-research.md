# Result and proof plan: From Papers to Reproducible Research

[Depth definitions](../proof-plan.md#proof-depth-contract) · [Source catalogue](../references/proof-sources.md) · [Volume plan](../volume-plan.md)

Authoring specifications only. No result/proof/API is certified by this plan. F/M/R have different scope; imported results are the exact prerequisite sections linked below.

## Chapter 48: Reading Papers, Building Evidence, and Reproducing Results

<span id="sec-reading-papers-building-evidence-and-reproducing-results-1"></span>

### 48.1 Choose a claim that can be tested

**Core result / role:** A reproducible claim has a testable scope.

**Assumptions and scope:** Explicit task, inputs, output and acceptance criterion.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Separate reproducing a model calculation from reproducing a hardware result.

**Imported earlier results:** [1.4](../section-plans/01-foundations.md#sec-what-quantum-computing-computes-4), [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Exact source targets:** [REPRO:software](../references/proof-sources.md#source-repro-software): Section 2 Software.

**Independent evidence target:** Produce a scoped claim and an explicit reproduction boundary.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-2"></span>

### 48.2 Freeze sources, data, and revisions

**Core result / role:** Source/data/environment provenance is part of the experiment.

**Assumptions and scope:** Pinned versions, hashes and permitted data use.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Specify immutable inputs and transformations without redistributing restricted sources.

**Imported earlier results:** [48.1](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-1).

**Exact source targets:** [REPRO:data](../references/proof-sources.md#source-repro-data): Section 1 Data Management; [REPRO:changes](../references/proof-sources.md#source-repro-changes): Section 5 Keeping Track of Changes.

**Independent evidence target:** Record exact source versions, locators, data origin and hashes.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-3"></span>

### 48.3 Build a symbol and convention map

**Core result / role:** Symbol/convention translation is an explicit map.

**Assumptions and scope:** Declared basis, signs, units and parameter normalization.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Build a bijective convention map and small consistency checks.

**Imported earlier results:** [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2), [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3), [48.1](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-1).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Compare one equation with a fully specified array operation.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-4"></span>

### 48.4 Trace equation and assumption dependencies

**Core result / role:** Equation dependence distinguishes assumptions from derived claims.

**Assumptions and scope:** Exact source version and result locators.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Record an argument graph, imported lemmas and approximation steps; no new theorem.

**Imported earlier results:** [48.3](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-3).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Build a small dependency record before implementing the final calculation.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-5"></span>

### 48.5 Construct an independent reference

**Core result / role:** Independent references should fail differently.

**Assumptions and scope:** Small tractable reference with separately derived conventions.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Specify analytic/dense/enumerative comparator and adversarial changed cases.

**Imported earlier results:** [48.4](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-4), [2.8](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-8).

**Exact source targets:** [REPRO:software](../references/proof-sources.md#source-repro-software): Section 2 Software.

**Independent evidence target:** Validate a limiting case and one equation before adding optimization.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-6"></span>

### 48.6 Separate sources of error

**Core result / role:** Error sources must be identified separately.

**Assumptions and scope:** Model, approximation, statistics and numerical errors declared.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Assign an independent check or bound to each source; do not hide discrepancies in one tolerance.

**Imported earlier results:** [48.5](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-5), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Choose tolerances justified by the budget and requested claim.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-7"></span>

### 48.7 Design and record the experiment

**Core result / role:** Experiment manifests make comparisons auditable.

**Assumptions and scope:** Frozen input/output, budget and randomization protocol.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Record commands, environments, seeds, derived data and all classical/quantum costs.

**Imported earlier results:** [48.2](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-2), [48.6](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-6), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Exact source targets:** [REPRO:data](../references/proof-sources.md#source-repro-data): Section 1 Data Management; [REPRO:organization](../references/proof-sources.md#source-repro-organization): Section 4 Project Organization.

**Independent evidence target:** Create a reproducible manifest and rerun from frozen inputs. For hybrid work, preserve task boundaries, queue/transfer/device/classical time, optimizer/solver state and the exact payload returned by each quantum call.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-8"></span>

### 48.8 Investigate discrepancies and negative results

**Core result / role:** A discrepancy is evidence to investigate.

**Assumptions and scope:** Independent references and declared acceptance threshold.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Design a diagnostic decision record and include negative results without a theorem claim.

**Imported earlier results:** [48.5](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-5), [48.7](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-7).

**Exact source targets:** [REPRO:software](../references/proof-sources.md#source-repro-software): Section 2 Software.

**Independent evidence target:** Preserve a failing example and explain the evidence for its cause.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-9"></span>

### 48.9 Report, review, and maintain a reproduction

**Core result / role:** Research reports preserve claim and evidence provenance.

**Assumptions and scope:** Traceable sources, data/code revisions and limitations.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Specify a reviewable report, archival record and correction process.

**Imported earlier results:** [48.6](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-6), [48.7](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-7), [48.8](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-8).

**Exact source targets:** [REPRO:changes](../references/proof-sources.md#source-repro-changes): Section 5 Keeping Track of Changes; [REPRO:manuscripts](../references/proof-sources.md#source-repro-manuscripts): Section 6 Manuscripts.

**Independent evidence target:** Prepare an auditable report and track confirmed framework gaps upstream.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 49: Case Study: Molecular Hydrogen from Hamiltonian to Verified VQE

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-1"></span>

### 49.1 Specify the paper claim and corrected data

**Core result / role:** H2 reproduction claim is limited to the pinned reduced model.

**Assumptions and scope:** Corrected arXiv v2 data and explicit comparison task.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Freeze the paper/data scope; do not identify synthetic sampling with the hardware experiment.

**Imported earlier results:** [48.1](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-1), [48.2](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-2).

**Exact source targets:** [H2:data](../references/proof-sources.md#source-h2-data): Corrected Supplementary Table I in arXiv v2 and surrounding reduced-model notes.

**Independent evidence target:** Validate the transcribed 54-row table and preserve its provenance.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-2"></span>

### 49.2 From the molecular model to a reduced Hamiltonian

**Core result / role:** Molecular reduction must be traced term by term.

**Assumptions and scope:** Declared orbitals, fermionic mapping, symmetry sector and offsets.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Plan the complete source-to-Hamiltonian map; exact molecular integral provenance remains a flagged acceptance item.

**Imported earlier results:** [25.1](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-1), [25.3](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-3), [25.4](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-4).

**Exact source targets:** [CHEM:VII.A](../references/proof-sources.md#source-chem-vii-a): Section VII A Hydrogen, including STO-3G example; [H2:data](../references/proof-sources.md#source-h2-data): Corrected Supplementary Table I in arXiv v2 and surrounding reduced-model notes.

**Independent evidence target:** Compare independent occupation/qubit operators and mark rounded inputs or deferred upstream derivations.

**Planning budget:** 3–6 pages. **Review status:** source-to-integral-and-reduction-map-pending; mathematical and implementation review remain separate.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-3"></span>

### 49.3 Units, offsets, symmetries, and qubit labels

**Core result / role:** Offsets and basis maps change the reported energy interpretation.

**Assumptions and scope:** Pinned coefficients, units, sectors and qubit labels.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive sector matrices and all constant shifts; verify at a non-special parameter.

**Imported earlier results:** [49.1](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-1), [49.2](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-2), [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2).

**Exact source targets:** [H2:data](../references/proof-sources.md#source-h2-data): Corrected Supplementary Table I in arXiv v2 and surrounding reduced-model notes; [H2:VQE](../references/proof-sources.md#source-h2-vqe): Section I, Eqs. (1)-(3) and Fig. 1; reduced-Hamiltonian/ansatz convention.

**Independent evidence target:** Check zero-angle energies and diagnose double-counted constants or swapped labels.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-4"></span>

### 49.4 The ansatz from generator to gates

**Core result / role:** Selected excitation generator reduces to the implemented ansatz.

**Assumptions and scope:** Fixed reference and reduced two-qubit sector.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Exponentiate the generator and derive its gate/angle mapping.

**Imported earlier results:** [49.3](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-3), [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5), [5.4](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4).

**Exact source targets:** [H2:VQE](../references/proof-sources.md#source-h2-vqe): Section I, Eqs. (1)-(3) and Fig. 1; reduced-Hamiltonian/ansatz convention; [CHEM:VII.A](../references/proof-sources.md#source-chem-vii-a): Section VII A Hydrogen, including STO-3G example.

**Independent evidence target:** Compare analytic states, a matrix exponential and FlagQuantum output.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-5"></span>

### 49.5 Observables, energy, and gradient

**Core result / role:** Energy and shared-parameter derivative correspondence.

**Assumptions and scope:** Pinned Hamiltonian/ansatz and real parameter convention.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive every measured Pauli contribution and gradient; reuse 23's occurrence rule.

**Imported earlier results:** [49.4](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-4), [23.3](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-3), [23.5](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-5), [23.6](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-6).

**Exact source targets:** [H2:VQE](../references/proof-sources.md#source-h2-vqe): Section I, Eqs. (1)-(3) and Fig. 1; reduced-Hamiltonian/ansatz convention; [PS:III.A](../references/proof-sources.md#source-ps-iii-a): Section III A Parameter-shift rule for gates with generators with two distinct eigenvalues.

**Independent evidence target:** Check analytic, dense, shifted and autograd results independently.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-6"></span>

### 49.6 The exact sector minimum and global comparison

**Core result / role:** Reachable-sector minimum differs from the full-space minimum.

**Assumptions and scope:** Explicit two-dimensional ansatz sector and full Hermitian model.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Diagonalize both matrices and prove which bound the ansatz attains.

**Imported earlier results:** [49.5](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-5), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Exact source targets:** [H2:data](../references/proof-sources.md#source-h2-data): Corrected Supplementary Table I in arXiv v2 and surrounding reduced-model notes; [CHEM:V.B](../references/proof-sources.md#source-chem-v-b): Section V B Variational quantum eigensolver.

**Independent evidence target:** Compare every tabulated geometry with full-matrix eigenvalues.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-7"></span>

### 49.7 Reproduce the full geometry scan

**Core result / role:** A geometry scan is a repeated model calculation.

**Assumptions and scope:** Every corrected Table I row and one fixed interpretation.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Specify all-row analytic/dense checks and separate data rounding from program error.

**Imported earlier results:** [49.6](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-6), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Exact source targets:** [H2:data](../references/proof-sources.md#source-h2-data): Corrected Supplementary Table I in arXiv v2 and surrounding reduced-model notes; [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Reproduce the table-wide curve and compare errors with the bound.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-8"></span>

### 49.8 Optimization and finite-shot extensions

**Core result / role:** Training and shot sampling add separate uncertainties.

**Assumptions and scope:** Specified optimizer, distribution and post-update objective.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive selected estimator/gradient statistics and distinguish optimizer convergence from exact minimum.

**Imported earlier results:** [49.5](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-5), [24.3](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-3), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Exact source targets:** [H2:VQE](../references/proof-sources.md#source-h2-vqe): Section I, Eqs. (1)-(3) and Fig. 1; reduced-Hamiltonian/ansatz convention; [NC:A1](../references/proof-sources.md#source-nc-a1): Appendix 1: Notes on basic probability theory.

**Independent evidence target:** Compare optimizer outcomes and seeded energy estimates with exact references.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-9"></span>

### 49.9 Interpretation, discrepancy analysis, and research report

**Core result / role:** H2 report must delimit reproduced and unreproduced claims.

**Assumptions and scope:** Pinned model/source/execution record.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Report all geometries, conventions, discrepancies and excluded hardware/molecular claims.

**Imported earlier results:** [49.1](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-1), [49.3](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-3), [49.5](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-5), [49.6](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-6), [49.7](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-7), [48.9](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-9).

**Exact source targets:** [REPRO:manuscripts](../references/proof-sources.md#source-repro-manuscripts): Section 6 Manuscripts; [H2:data](../references/proof-sources.md#source-h2-data): Corrected Supplementary Table I in arXiv v2 and surrounding reduced-model notes.

**Independent evidence target:** Deliver data, plots, manifest, checks and a claim-by-claim evidence summary.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 50: Case Study: Logical Memory and Error-Correction Experiments

<span id="sec-case-study-logical-memory-and-error-correction-experiments-1"></span>

### 50.1 Select a source and freeze the logical-memory claim

**Core result / role:** Complementary error chains can share a syndrome but differ by a logical operator.

**Assumptions and scope:** Fowler et al. v2 Section VII A/Fig. 5; same check and boundary conventions; benchmark extension declared separately.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Verify the two chains, equal syndrome and logical difference; freeze a finite memory extension without claiming the paper's Fig. 4 threshold.

**Imported earlier results:** [48.1](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-1), [48.2](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-2).

**Exact source targets:** [SURFACE:case](../references/proof-sources.md#source-surface-case): Section VII A, Fig. 5: complementary error chains with the same syndrome; source noise list on p.11.

**Independent evidence target:** Specify the two complementary chains, verify equal syndromes and their logical difference exactly, then separately freeze the patch/noise/decoder/round conventions for the extension.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-2"></span>

### 50.2 Specify the code, circuit, and noise model

**Core result / role:** Memory circuit/noise model is a complete task specification.

**Assumptions and scope:** Fixed code, schedule, rounds and noise placement.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Specify all boundary preparations, measurements and fault probabilities before simulation.

**Imported earlier results:** [28.1](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-1), [31.1](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-1), [31.3](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-3).

**Exact source targets:** [SURFACE:circuits](../references/proof-sources.md#source-surface-circuits): Fig. 1 and Sections III-V; gate-level stabilizer cycle.

**Independent evidence target:** Compare the experiment specification with the selected paper and list deviations.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-3"></span>

### 50.3 Derive syndromes and detection events

**Core result / role:** Syndrome/detection maps follow from the frozen circuit.

**Assumptions and scope:** Same boundary and time-order convention as 50.2.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Enumerate selected faults and derive event records and correlations.

**Imported earlier results:** [50.2](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-2), [31.4](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-4).

**Exact source targets:** [SURFACE:decoding](../references/proof-sources.md#source-surface-decoding): Section VII Error Detection; Section VII A and Fig. 5; noise list.

**Independent evidence target:** Hand-enumerate a small set of faults and compare independent event records.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-4"></span>

### 50.4 Define decoding and logical success

**Core result / role:** Logical success is decoder/frame dependent.

**Assumptions and scope:** Declared decoder and final logical observable.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove the success predicate for each error class and correction frame.

**Imported earlier results:** [50.3](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-3), [31.5](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-5), [31.6](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-6).

**Exact source targets:** [SURFACE:decoding](../references/proof-sources.md#source-surface-decoding): Section VII Error Detection; Section VII A and Fig. 5; noise list.

**Independent evidence target:** Verify noiseless cases and deliberately injected logical errors.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-5"></span>

### 50.5 Build an exact small-instance reference

**Core result / role:** Exact tiny-instance enumeration independently verifies memory behavior.

**Assumptions and scope:** Explicitly small finite channel/error model and bounded Hilbert dimension.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Enumerate branches or dense channel action; derive the logical failure probability without requiring a later tableau simulator.

**Imported earlier results:** [50.4](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-4), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3).

**Exact source targets:** [NC:8.2.3](../references/proof-sources.md#source-nc-8-2-3): Section 8.2.3 Operator-sum representation; [NC:10.3](../references/proof-sources.md#source-nc-10-3): Section 10.3 Theory of quantum error-correction.

**Independent evidence target:** Compare complete tiny-instance logical outcomes before stochastic runs, using explicit matrices or exhaustive finite error branches independent of the primary path.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-6"></span>

### 50.6 Design the stochastic experiment

**Core result / role:** Failure-rate estimator and conservative coverage.

**Assumptions and scope:** Independent trials under a fixed frozen model.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove binomial mean/variance and conservative confidence coverage; treat zero observed failures explicitly.

**Imported earlier results:** [50.4](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-4), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Exact source targets:** [NC:A1](../references/proof-sources.md#source-nc-a1): Appendix 1: Notes on basic probability theory; [CVX:7.4](../references/proof-sources.md#source-cvx-7-4): Section 7.4 Chebyshev and Chernoff bounds.

**Independent evidence target:** Validate estimators and retain representative failures for diagnosis.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-7"></span>

### 50.7 Compare distances, rounds, and noise parameters

**Core result / role:** Distance/round comparisons do not alone prove a threshold.

**Assumptions and scope:** Matched noise/circuit/decoder family and uncertainty.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive the plotted quantity and fit assumptions; distinguish finite crossings from asymptotic claims.

**Imported earlier results:** [50.6](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-6), [31.7](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-7).

**Exact source targets:** [SURFACE:threshold](../references/proof-sources.md#source-surface-threshold): Section VII, Fig. 4 and Eqs. (10)-(13); model-specific empirical scaling.

**Independent evidence target:** Report finite-size uncertainty and avoid claiming a general threshold from a small crossing.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-8"></span>

### 50.8 From memory evidence to resource implications

**Core result / role:** Memory evidence supports only conditional resource extrapolation.

**Assumptions and scope:** Explicit fit domain, workload and logical-error target.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Propagate the measured/fitted model into 33's resource calculation and state extrapolation limits.

**Imported earlier results:** [50.7](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-7), [33.6](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-6).

**Exact source targets:** [RESOURCE:cost](../references/proof-sources.md#source-resource-cost): Section 4 tradeoffs, especially 4.3 distance selection, and Section 5.

**Independent evidence target:** Perform a scoped sensitivity estimate linked to Chapter 33.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-9"></span>

### 50.9 Write a reproducible correction-study report

**Core result / role:** Memory report preserves the frozen claim and exclusions.

**Assumptions and scope:** Pinned Fowler v2 ambiguity claim; independently specified finite benchmark extension.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Report the exact source-to-claim map, all benchmark conventions and excluded threshold/hardware claims.

**Imported earlier results:** [50.1](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-1), [50.4](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-4), [50.5](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-5), [50.6](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-6), [50.7](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-7), [48.9](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-9).

**Exact source targets:** [REPRO:manuscripts](../references/proof-sources.md#source-repro-manuscripts): Section 6 Manuscripts; [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Deliver source/data records, reference checks, decoder configuration, failures and unresolved gaps.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.
