# Part 9. From Papers to Reproducible Research

**Detailed plan · 2026-10-20 · Planned material; architecture review pending.** [All sections](../section-plan.md) · [Full plan](../book-plan.md) · [Reader continuity](../reader-continuity.md)

Each section specifies its argument and independent evidence. Framework implementation, mathematical review and reader review have separate status. Closing materials follow the [section-plan guide](../section-plan.md#how-to-read-the-specification).

<span id="ch-reading-papers-building-evidence-and-reproducing-results"></span>
<span id="chapter-38"></span>

## Chapter 48

**Reading Papers, Building Evidence, and Reproducing Results**

**Reading level:** Core research method. **Chapter prerequisites:** 4, 6, 10, 14; application-specific prerequisites.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-1"></span>
<span id="381-choose-a-claim-that-can-be-tested"></span>

### 48.1 Choose a claim that can be tested

**Learning and derivation target:** Separate a theorem, a numerical calculation and a hardware observation in a paper.

**Implementation and evidence target:** Produce a scoped claim and an explicit reproduction boundary.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-2"></span>
<span id="382-freeze-sources-data-and-revisions"></span>

### 48.2 Freeze sources, data, and revisions

**Learning and derivation target:** Explain why a version, correction or data transcription changes the specification.

**Implementation and evidence target:** Record exact source versions, locators, data origin and hashes.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-3"></span>
<span id="383-build-a-symbol-and-convention-map"></span>

### 48.3 Build a symbol and convention map

**Learning and derivation target:** Translate units, qubit labels, basis order, normalization and parameter definitions.

**Implementation and evidence target:** Compare one equation with a fully specified array operation.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-4"></span>
<span id="384-trace-equation-and-assumption-dependencies"></span>

### 48.4 Trace equation and assumption dependencies

**Learning and derivation target:** Identify which earlier results and approximations each claim uses.

**Implementation and evidence target:** Build a small dependency record before implementing the final calculation.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-5"></span>
<span id="385-construct-an-independent-reference"></span>

### 48.5 Construct an independent reference

**Learning and derivation target:** Select analytic, dense, enumerated or independently structured checks.

**Implementation and evidence target:** Validate a limiting case and one equation before adding optimization.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-6"></span>
<span id="386-separate-sources-of-error"></span>

### 48.6 Separate sources of error

**Learning and derivation target:** Derive a relevant budget for discretization, truncation, sampling and optimization.

**Implementation and evidence target:** Choose tolerances justified by the budget and requested claim.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-7"></span>
<span id="387-design-and-record-the-experiment"></span>

### 48.7 Design and record the experiment

**Learning and derivation target:** Specify inputs, seeds, environment, outputs, resources and comparison criteria.

**Implementation and evidence target:** Create a reproducible manifest and rerun from frozen inputs.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-8"></span>
<span id="388-investigate-discrepancies-and-negative-results"></span>

### 48.8 Investigate discrepancies and negative results

**Learning and derivation target:** Distinguish convention bugs, numerical error, model mismatch and source ambiguity.

**Implementation and evidence target:** Preserve a failing example and explain the evidence for its cause.

<span id="sec-reading-papers-building-evidence-and-reproducing-results-9"></span>
<span id="389-report-review-and-maintain-a-reproduction"></span>

### 48.9 Report, review, and maintain a reproduction

**Learning and derivation target:** State which claim was reproduced, with what uncertainty and unresolved limits.

**Implementation and evidence target:** Prepare an auditable report and track confirmed framework gaps upstream.

<span id="ch-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe"></span>
<span id="chapter-39"></span>

## Chapter 49

**Case Study: Molecular Hydrogen from Hamiltonian to Verified VQE**

**Reading level:** Research capstone. **Chapter prerequisites:** 23–25, 48.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-1"></span>
<span id="391-specify-the-paper-claim-and-corrected-data"></span>

### 49.1 Specify the paper claim and corrected data

**Learning and derivation target:** Identify the O'Malley calculation, chosen source revision and ideal-versus-hardware scope.

**Implementation and evidence target:** Validate the transcribed 54-row table and preserve its provenance.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-2"></span>
<span id="392-from-the-molecular-model-to-a-reduced-hamiltonian"></span>

### 49.2 From the molecular model to a reduced Hamiltonian

**Learning and derivation target:** Derive the mapping/reduction steps that are actually supported by the chosen sources.

**Implementation and evidence target:** Compare independent occupation/qubit operators and mark rounded inputs or deferred upstream derivations.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-3"></span>
<span id="393-units-offsets-symmetries-and-qubit-labels"></span>

### 49.3 Units, offsets, symmetries, and qubit labels

**Learning and derivation target:** Derive the selected sector and reference-state conventions.

**Implementation and evidence target:** Check zero-angle energies and diagnose double-counted constants or swapped labels.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-4"></span>
<span id="394-the-ansatz-from-generator-to-gates"></span>

### 49.4 The ansatz from generator to gates

**Learning and derivation target:** Derive amplitudes and a gate decomposition with explicit angle normalization.

**Implementation and evidence target:** Compare analytic states, a matrix exponential and FlagQuantum output.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-5"></span>
<span id="395-observables-energy-and-gradient"></span>

### 49.5 Observables, energy, and gradient

**Learning and derivation target:** Derive each Pauli expectation, the energy curve and derivative.

**Implementation and evidence target:** Check analytic, dense, shifted and autograd results independently.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-6"></span>
<span id="396-the-exact-sector-minimum-and-global-comparison"></span>

### 49.6 The exact sector minimum and global comparison

**Learning and derivation target:** Derive the reduced-sector solution and state when it equals the full ground energy.

**Implementation and evidence target:** Compare every tabulated geometry with full-matrix eigenvalues.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-7"></span>
<span id="397-reproduce-the-full-geometry-scan"></span>

### 49.7 Reproduce the full geometry scan

**Learning and derivation target:** Derive a grid-error bound for the specified angular scan.

**Implementation and evidence target:** Reproduce the table-wide curve and compare errors with the bound.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-8"></span>
<span id="398-optimization-and-finite-shot-extensions"></span>

### 49.8 Optimization and finite-shot extensions

**Learning and derivation target:** Separate tutorial extensions from the source calculation and derive their uncertainty.

**Implementation and evidence target:** Compare optimizer outcomes and seeded energy estimates with exact references.

<span id="sec-case-study-molecular-hydrogen-from-hamiltonian-to-verified-vqe-9"></span>
<span id="399-interpretation-discrepancy-analysis-and-research-report"></span>

### 49.9 Interpretation, discrepancy analysis, and research report

**Learning and derivation target:** Explain rounded coefficients, geometry coverage and experimental-reproduction limits.

**Implementation and evidence target:** Deliver data, plots, manifest, checks and a claim-by-claim evidence summary.

<span id="ch-case-study-logical-memory-and-error-correction-experiments"></span>
<span id="chapter-40"></span>

## Chapter 50

**Case Study: Logical Memory and Error-Correction Experiments**

**Reading level:** Research capstone. **Chapter prerequisites:** 28–33, 45, 48.

**Source-selection gate:** select and review a primary paper before fixing the code family, noise model and reproduction claim.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-1"></span>
<span id="401-select-a-source-and-freeze-the-logical-memory-claim"></span>

### 50.1 Select a source and freeze the logical-memory claim

**Learning and derivation target:** Choose a reviewed primary source, model and tractable reproduction scope before coding.

**Implementation and evidence target:** Record the paper version and a precise evidence target; source selection remains pending.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-2"></span>
<span id="402-specify-the-code-circuit-and-noise-model"></span>

### 50.2 Specify the code, circuit, and noise model

**Learning and derivation target:** Define layout, logical preparation, repeated rounds and all noise locations.

**Implementation and evidence target:** Compare the experiment specification with the selected paper and list deviations.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-3"></span>
<span id="403-derive-syndromes-and-detection-events"></span>

### 50.3 Derive syndromes and detection events

**Learning and derivation target:** Work through error-to-event patterns with explicit time/boundary conventions.

**Implementation and evidence target:** Hand-enumerate a small set of faults and compare independent event records.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-4"></span>
<span id="404-define-decoding-and-logical-success"></span>

### 50.4 Define decoding and logical success

**Learning and derivation target:** Specify decoder input/output, correction equivalence and logical observable.

**Implementation and evidence target:** Verify noiseless cases and deliberately injected logical errors.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-5"></span>
<span id="405-build-an-exact-small-instance-reference"></span>

### 50.5 Build an exact small-instance reference

**Learning and derivation target:** Choose a tractable state, stabilizer or enumerated reference independent of the main path.

**Implementation and evidence target:** Compare complete tiny-instance behavior before large stochastic runs.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-6"></span>
<span id="406-design-the-stochastic-experiment"></span>

### 50.6 Design the stochastic experiment

**Learning and derivation target:** Specify sampling, stopping, seeds, error bars and failure-event accounting.

**Implementation and evidence target:** Validate estimators and retain representative failures for diagnosis.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-7"></span>
<span id="407-compare-distances-rounds-and-noise-parameters"></span>

### 50.7 Compare distances, rounds, and noise parameters

**Learning and derivation target:** Derive the scope of a scaling comparison and define rates consistently.

**Implementation and evidence target:** Report finite-size uncertainty and avoid claiming a general threshold from a small crossing.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-8"></span>
<span id="408-from-memory-evidence-to-resource-implications"></span>

### 50.8 From memory evidence to resource implications

**Learning and derivation target:** State which logical-gate or architecture assumptions are missing from a memory experiment.

**Implementation and evidence target:** Perform a scoped sensitivity estimate linked to Chapter 33.

<span id="sec-case-study-logical-memory-and-error-correction-experiments-9"></span>
<span id="409-write-a-reproducible-correction-study-report"></span>

### 50.9 Write a reproducible correction-study report

**Learning and derivation target:** Relate each result to the source claim and its limitations.

**Implementation and evidence target:** Deliver source/data records, reference checks, decoder configuration, failures and unresolved gaps.
