# Part 9. From Papers to Reproducible Research

**Detailed plan · 2026-10-20 · Planned material; editorial pass completed, external validation/freeze pending.** [All sections](../section-plan.md) · [Full plan](../book-plan.md) · [Reader continuity](../reader-continuity.md)

Each section specifies its argument and independent evidence. Framework implementation, mathematical review and reader review have separate status. Closing materials follow the [section-plan guide](../section-plan.md#how-to-read-the-specification).

<span id="ch-reading-papers-building-evidence-and-reproducing-results"></span>
<span id="chapter-38"></span>

## Chapter 48

**Reading Papers, Building Evidence, and Reproducing Results**

**Reading level:** Core research method. **Entry guidance:** 4, 6 for scientific specification; application/resource/statistical sections are selected for the claim.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-1"></span>
<span id="381-choose-a-claim-that-can-be-tested"></span>

### 48.1 Choose a claim that can be tested

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-1).

**Section level:** core. **Required earlier sections:** [1.4](../section-plans/01-foundations.md#sec-what-quantum-computing-computes-4), [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Learning and derivation target:** Separate a theorem, a numerical calculation and a hardware observation in a paper.

**Implementation and evidence target:** Produce a scoped claim and an explicit reproduction boundary.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-2"></span>
<span id="382-freeze-sources-data-and-revisions"></span>

### 48.2 Freeze sources, data, and revisions

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-2).

**Section level:** core. **Required earlier sections:** [48.1](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-1).

**Learning and derivation target:** Explain why a version, correction or data transcription changes the specification.

**Implementation and evidence target:** Record exact source versions, locators, data origin and hashes.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-3"></span>
<span id="383-build-a-symbol-and-convention-map"></span>

### 48.3 Build a symbol and convention map

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-3).

**Section level:** core. **Required earlier sections:** [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2), [6.3](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3), [48.1](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-1).

**Learning and derivation target:** Translate units, qubit labels, basis order, normalization and parameter definitions.

**Implementation and evidence target:** Compare one equation with a fully specified array operation.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-4"></span>
<span id="384-trace-equation-and-assumption-dependencies"></span>

### 48.4 Trace equation and assumption dependencies

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-4).

**Section level:** core. **Required earlier sections:** [48.3](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-3).

**Learning and derivation target:** Identify which earlier results and approximations each claim uses.

**Implementation and evidence target:** Build a small dependency record before implementing the final calculation.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-5"></span>
<span id="385-construct-an-independent-reference"></span>

### 48.5 Construct an independent reference

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-5).

**Section level:** core. **Required earlier sections:** [48.4](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-4), [2.8](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-8).

**Learning and derivation target:** Select analytic, dense, enumerated or independently structured checks.

**Implementation and evidence target:** Validate a limiting case and one equation before adding optimization.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-6"></span>
<span id="386-separate-sources-of-error"></span>

### 48.6 Separate sources of error

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-6).

**Section level:** core. **Required earlier sections:** [48.5](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-5), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Learning and derivation target:** Derive a relevant budget for discretization, truncation, sampling and optimization.

**Implementation and evidence target:** Choose tolerances justified by the budget and requested claim.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-7"></span>
<span id="387-design-and-record-the-experiment"></span>

### 48.7 Design and record the experiment

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-7).

**Section level:** core. **Required earlier sections:** [48.2](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-2), [48.6](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-6), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Learning and derivation target:** Specify inputs, seeds, environment, outputs, resources and comparison criteria.

**Implementation and evidence target:** Create a reproducible manifest and rerun from frozen inputs. For hybrid work, preserve task boundaries, queue/transfer/device/classical time, optimizer/solver state and the exact payload returned by each quantum call.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-8"></span>
<span id="388-investigate-discrepancies-and-negative-results"></span>

### 48.8 Investigate discrepancies and negative results

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-8).

**Section level:** core. **Required earlier sections:** [48.5](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-5), [48.7](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-7).

**Learning and derivation target:** Distinguish convention bugs, numerical error, model mismatch and source ambiguity.

**Implementation and evidence target:** Preserve a failing example and explain the evidence for its cause.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-9"></span>
<span id="389-report-review-and-maintain-a-reproduction"></span>

### 48.9 Report, review, and maintain a reproduction

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-9).

**Section level:** core. **Required earlier sections:** [48.6](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-6), [48.7](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-7), [48.8](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-8).

**Learning and derivation target:** State which claim was reproduced, with what uncertainty and unresolved limits.

**Implementation and evidence target:** Prepare an auditable report and track confirmed framework gaps upstream.

<span id="ch-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe"></span>
<span id="chapter-39"></span>

## Chapter 49

**Case Study: Molecular Hydrogen from Hamiltonian to Verified VQE**

**Reading level:** Research capstone. **Entry guidance:** 4, 6, selected derivatives/energy sections of 23/25 and 48; 24 for the optimizer extension, not all embedding/learning topics.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-1"></span>
<span id="391-specify-the-paper-claim-and-corrected-data"></span>

### 49.1 Specify the paper claim and corrected data

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-1).

**Section level:** advanced. **Required earlier sections:** [48.1](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-1), [48.2](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-2).

**Learning and derivation target:** Identify the O'Malley calculation, chosen source revision and ideal-versus-hardware scope.

**Implementation and evidence target:** Validate the transcribed 54-row table and preserve its provenance.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-2"></span>
<span id="392-from-the-molecular-model-to-a-reduced-hamiltonian"></span>

### 49.2 From the molecular model to a reduced Hamiltonian

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-2).

**Section level:** advanced. **Required earlier sections:** [25.1](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-1), [25.3](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-3), [25.4](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-4).

**Learning and derivation target:** Plan the declared STO-6G AO/MO integral conventions, four-mode Fock/BK translation, explicit Z1=Z3=+1 projection and remaining two-electron sector; distinguish original source data from independent reconstruction.

**Implementation and evidence target:** Follow H2-01–09: verify all 324 coefficients at published four-decimal precision, preserve the corrected table/hash, compare the full N=2 spectrum, and disclose unavailable original author integral files.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-3"></span>
<span id="393-units-offsets-symmetries-and-qubit-labels"></span>

### 49.3 Units, offsets, symmetries, and qubit labels

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-3).

**Section level:** advanced. **Required earlier sections:** [49.1](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-1), [49.2](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-2), [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2).

**Learning and derivation target:** Derive the selected sector and reference-state conventions.

**Implementation and evidence target:** Check zero-angle energies and diagnose double-counted constants or swapped labels.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-4"></span>
<span id="394-the-ansatz-from-generator-to-gates"></span>

### 49.4 The ansatz from generator to gates

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-4).

**Section level:** advanced. **Required earlier sections:** [49.3](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-3), [3.5](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-5), [5.4](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-4).

**Learning and derivation target:** Derive amplitudes and a gate decomposition with explicit angle normalization.

**Implementation and evidence target:** Compare analytic states, a matrix exponential and FlagQuantum output.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-5"></span>
<span id="395-observables-energy-and-gradient"></span>

### 49.5 Observables, energy, and gradient

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-5).

**Section level:** advanced. **Required earlier sections:** [49.4](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-4), [23.3](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-3), [23.5](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-5), [23.6](../section-plans/04-variational.md#sec-parameterized-circuits-quantum-gradients-and-differentiation-6).

**Learning and derivation target:** Derive each Pauli expectation, the energy curve and derivative.

**Implementation and evidence target:** Check analytic, dense, shifted and autograd results independently.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-6"></span>
<span id="396-the-exact-sector-minimum-and-global-comparison"></span>

### 49.6 The exact sector minimum and global comparison

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-6).

**Section level:** advanced. **Required earlier sections:** [49.5](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-5), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Learning and derivation target:** Derive the reduced-sector solution and state when it equals the full ground energy.

**Implementation and evidence target:** Compare every tabulated geometry with full-matrix eigenvalues.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-7"></span>
<span id="397-reproduce-the-full-geometry-scan"></span>

### 49.7 Reproduce the full geometry scan

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-7).

**Section level:** advanced. **Required earlier sections:** [49.6](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-6), [2.7](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-7).

**Learning and derivation target:** Derive a grid-error bound for the specified angular scan.

**Implementation and evidence target:** Reproduce the table-wide curve and compare errors with the bound.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-8"></span>
<span id="398-optimization-and-finite-shot-extensions"></span>

### 49.8 Optimization and finite-shot extensions

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-8).

**Section level:** advanced. **Required earlier sections:** [49.5](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-5), [24.3](../section-plans/04-variational.md#sec-optimization-geometry-and-trainability-3), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Learning and derivation target:** Separate tutorial extensions from the source calculation and derive their uncertainty.

**Implementation and evidence target:** Compare optimizer outcomes and seeded energy estimates with exact references.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-9"></span>
<span id="399-interpretation-discrepancy-analysis-and-research-report"></span>

### 49.9 Interpretation, discrepancy analysis, and research report

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-9).

**Section level:** advanced. **Required earlier sections:** [49.1](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-1), [49.3](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-3), [49.5](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-5), [49.6](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-6), [49.7](../section-plans/07-research.md#sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-7), [48.9](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-9).

**Learning and derivation target:** Explain rounded coefficients, geometry coverage and experimental-reproduction limits.

**Implementation and evidence target:** Deliver data, plots, manifest, checks and a claim-by-claim evidence summary.

<span id="ch-case-study-logical-memory-and-error-correction-experiments"></span>
<span id="chapter-40"></span>

## Chapter 50

**Case Study: Logical Memory and Error-Correction Experiments**

**Reading level:** Research capstone. **Entry guidance:** Selected noise, stabilizer/surface-code and research-method sections; exact dense/error enumeration for the small reference. Universal logical gates, factories and a later tableau simulator are not entry requirements.

**Claim/model acceptance gate:** Fowler et al. v2, Section VII A/Fig. 5 anchors syndrome ambiguity. The finite memory benchmark is a declared extension; exact model choices still need acceptance, and no threshold reproduction is promised.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-1"></span>
<span id="401-select-a-source-and-freeze-the-logical-memory-claim"></span>

### 50.1 Select a source and freeze the logical-memory claim

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-1).

**Section level:** advanced. **Required earlier sections:** [48.1](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-1), [48.2](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-2).

**Learning and derivation target:** Freeze Fowler et al., arXiv:1208.0928v2, Section VII A and Fig. 5 as the primary ambiguity claim: complementary error chains can share a syndrome but differ logically. The finite memory benchmark is a declared textbook extension, not reproduction of Fig. 4 thresholds.

**Implementation and evidence target:** Specify the two complementary chains, verify equal syndromes and their logical difference exactly, then separately freeze the patch/noise/decoder/round conventions for the extension.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-2"></span>
<span id="402-specify-the-code-circuit-and-noise-model"></span>

### 50.2 Specify the code, circuit, and noise model

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-2).

**Section level:** advanced. **Required earlier sections:** [28.1](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-1), [31.1](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-1), [31.3](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-3).

**Learning and derivation target:** Define layout, logical preparation, repeated rounds and all noise locations.

**Implementation and evidence target:** Compare the experiment specification with the selected paper and list deviations.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-3"></span>
<span id="403-derive-syndromes-and-detection-events"></span>

### 50.3 Derive syndromes and detection events

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-3).

**Section level:** advanced. **Required earlier sections:** [50.2](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-2), [31.4](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-4).

**Learning and derivation target:** Work through error-to-event patterns with explicit time/boundary conventions.

**Implementation and evidence target:** Hand-enumerate a small set of faults and compare independent event records.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-4"></span>
<span id="404-define-decoding-and-logical-success"></span>

### 50.4 Define decoding and logical success

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-4).

**Section level:** advanced. **Required earlier sections:** [50.3](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-3), [31.5](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-5), [31.6](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-6).

**Learning and derivation target:** Specify decoder input/output, correction equivalence and logical observable.

**Implementation and evidence target:** Verify noiseless cases and deliberately injected logical errors.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-5"></span>
<span id="405-build-an-exact-small-instance-reference"></span>

### 50.5 Build an exact small-instance reference

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-5).

**Section level:** advanced. **Required earlier sections:** [50.4](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-4), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3).

**Learning and derivation target:** Derive an exact dense or enumerated tiny-instance reference from the declared finite channel/error model; a later tableau implementation is optional.

**Implementation and evidence target:** Compare complete tiny-instance logical outcomes before stochastic runs, using explicit matrices or exhaustive finite error branches independent of the primary path.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-6"></span>
<span id="406-design-the-stochastic-experiment"></span>

### 50.6 Design the stochastic experiment

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-6).

**Section level:** advanced. **Required earlier sections:** [50.4](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-4), [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).

**Learning and derivation target:** Specify sampling, stopping, seeds, error bars and failure-event accounting.

**Implementation and evidence target:** Validate estimators and retain representative failures for diagnosis.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-7"></span>
<span id="407-compare-distances-rounds-and-noise-parameters"></span>

### 50.7 Compare distances, rounds, and noise parameters

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-7).

**Section level:** advanced. **Required earlier sections:** [50.6](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-6), [31.7](../section-plans/05-fault-tolerance.md#sec-surface-codes-and-repeated-syndrome-measurements-7).

**Learning and derivation target:** Derive the scope of a scaling comparison and define rates consistently.

**Implementation and evidence target:** Report finite-size uncertainty and avoid claiming a general threshold from a small crossing.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-8"></span>
<span id="408-from-memory-evidence-to-resource-implications"></span>

### 50.8 From memory evidence to resource implications

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-8).

**Section level:** advanced. **Required earlier sections:** [50.7](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-7), [33.6](../section-plans/05-fault-tolerance.md#sec-from-logical-algorithms-to-physical-resource-estimates-6).

**Learning and derivation target:** State which logical-gate or architecture assumptions are missing from a memory experiment.

**Implementation and evidence target:** Perform a scoped sensitivity estimate linked to Chapter 33.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-9"></span>
<span id="409-write-a-reproducible-correction-study-report"></span>

### 50.9 Write a reproducible correction-study report

**Result/proof/source specification:** [Scholarly plan](../proof-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-9).

**Section level:** advanced. **Required earlier sections:** [50.1](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-1), [50.4](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-4), [50.5](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-5), [50.6](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-6), [50.7](../section-plans/07-research.md#sec-case-study-logical-memory-and-error-correction-experiments-7), [48.9](../section-plans/07-research.md#sec-reading-papers-building-evidence-and-reproducing-results-9).

**Learning and derivation target:** Relate each result to the source claim and its limitations.

**Implementation and evidence target:** Deliver source/data records, reference checks, decoder configuration, failures and unresolved gaps.
