# Part 7: From Papers to Reproducible Research

**Detailed section plan · October 20, 2026 · Planned material.** [All section plans](../section-plan.md) · [Curriculum and prerequisites](../book-plan.md)

Each numbered section specifies its intended argument and independent evidence. The unnumbered closing material and authoring rules are defined in the [section-plan guide](../section-plan.md#how-to-read-the-specification). Implementation status remains separate from curriculum status.

## Chapter 38

**Reading Papers, Building Evidence, and Reproducing Results**

**Reading level:** Core research method. **Chapter prerequisites:** 4, 6, 10, 14; application-specific prerequisites.

### 38.1 Choose a claim that can be tested

**Learning and derivation target:** Separate a theorem, a numerical calculation and a hardware observation in a paper.

**Implementation and evidence target:** Produce a scoped claim and an explicit reproduction boundary.

### 38.2 Freeze sources, data, and revisions

**Learning and derivation target:** Explain why a version, correction or data transcription changes the specification.

**Implementation and evidence target:** Record exact source versions, locators, data origin and hashes.

### 38.3 Build a symbol and convention map

**Learning and derivation target:** Translate units, qubit labels, basis order, normalization and parameter definitions.

**Implementation and evidence target:** Compare one equation with a fully specified array operation.

### 38.4 Trace equation and assumption dependencies

**Learning and derivation target:** Identify which earlier results and approximations each claim uses.

**Implementation and evidence target:** Build a small dependency record before implementing the final calculation.

### 38.5 Construct an independent reference

**Learning and derivation target:** Select analytic, dense, enumerated or independently structured checks.

**Implementation and evidence target:** Validate a limiting case and one equation before adding optimization.

### 38.6 Separate sources of error

**Learning and derivation target:** Derive a relevant budget for discretization, truncation, sampling and optimization.

**Implementation and evidence target:** Choose tolerances justified by the budget and requested claim.

### 38.7 Design and record the experiment

**Learning and derivation target:** Specify inputs, seeds, environment, outputs, resources and comparison criteria.

**Implementation and evidence target:** Create a reproducible manifest and rerun from frozen inputs.

### 38.8 Investigate discrepancies and negative results

**Learning and derivation target:** Distinguish convention bugs, numerical error, model mismatch and source ambiguity.

**Implementation and evidence target:** Preserve a failing example and explain the evidence for its cause.

### 38.9 Report, review, and maintain a reproduction

**Learning and derivation target:** State which claim was reproduced, with what uncertainty and unresolved limits.

**Implementation and evidence target:** Prepare an auditable report and track confirmed framework gaps upstream.

## Chapter 39

**Case Study: Molecular Hydrogen from Hamiltonian to Verified VQE**

**Reading level:** Research capstone. **Chapter prerequisites:** 23–25, 38.

### 39.1 Specify the paper claim and corrected data

**Learning and derivation target:** Identify the O'Malley calculation, chosen source revision and ideal-versus-hardware scope.

**Implementation and evidence target:** Validate the transcribed 54-row table and preserve its provenance.

### 39.2 From the molecular model to a reduced Hamiltonian

**Learning and derivation target:** Derive the mapping/reduction steps that are actually supported by the chosen sources.

**Implementation and evidence target:** Compare independent occupation/qubit operators and mark rounded inputs or deferred upstream derivations.

### 39.3 Units, offsets, symmetries, and qubit labels

**Learning and derivation target:** Derive the selected sector and reference-state conventions.

**Implementation and evidence target:** Check zero-angle energies and diagnose double-counted constants or swapped labels.

### 39.4 The ansatz from generator to gates

**Learning and derivation target:** Derive amplitudes and a gate decomposition with explicit angle normalization.

**Implementation and evidence target:** Compare analytic states, a matrix exponential and FlagQuantum output.

### 39.5 Observables, energy, and gradient

**Learning and derivation target:** Derive each Pauli expectation, the energy curve and derivative.

**Implementation and evidence target:** Check analytic, dense, shifted and autograd results independently.

### 39.6 The exact sector minimum and global comparison

**Learning and derivation target:** Derive the reduced-sector solution and state when it equals the full ground energy.

**Implementation and evidence target:** Compare every tabulated geometry with full-matrix eigenvalues.

### 39.7 Reproduce the full geometry scan

**Learning and derivation target:** Derive a grid-error bound for the specified angular scan.

**Implementation and evidence target:** Reproduce the table-wide curve and compare errors with the bound.

### 39.8 Optimization and finite-shot extensions

**Learning and derivation target:** Separate tutorial extensions from the source calculation and derive their uncertainty.

**Implementation and evidence target:** Compare optimizer outcomes and seeded energy estimates with exact references.

### 39.9 Interpretation, discrepancy analysis, and research report

**Learning and derivation target:** Explain rounded coefficients, geometry coverage and experimental-reproduction limits.

**Implementation and evidence target:** Deliver data, plots, manifest, checks and a claim-by-claim evidence summary.

## Chapter 40

**Case Study: Logical Memory and Error-Correction Experiments**

**Reading level:** Research capstone. **Chapter prerequisites:** 28–33, 35, 38.

**Source-selection gate:** Choose and review a primary paper before freezing this case study's specific code family, noise model and reproduction claim.

### 40.1 Select a source and freeze the logical-memory claim

**Learning and derivation target:** Choose a reviewed primary source, model and tractable reproduction scope before coding.

**Implementation and evidence target:** Record the paper version and a precise evidence target; source selection remains pending.

### 40.2 Specify the code, circuit, and noise model

**Learning and derivation target:** Define layout, logical preparation, repeated rounds and all noise locations.

**Implementation and evidence target:** Compare the experiment specification with the selected paper and list deviations.

### 40.3 Derive syndromes and detection events

**Learning and derivation target:** Work through error-to-event patterns with explicit time/boundary conventions.

**Implementation and evidence target:** Hand-enumerate a small set of faults and compare independent event records.

### 40.4 Define decoding and logical success

**Learning and derivation target:** Specify decoder input/output, correction equivalence and logical observable.

**Implementation and evidence target:** Verify noiseless cases and deliberately injected logical errors.

### 40.5 Build an exact small-instance reference

**Learning and derivation target:** Choose a tractable state, stabilizer or enumerated reference independent of the main path.

**Implementation and evidence target:** Compare complete tiny-instance behavior before large stochastic runs.

### 40.6 Design the stochastic experiment

**Learning and derivation target:** Specify sampling, stopping, seeds, error bars and failure-event accounting.

**Implementation and evidence target:** Validate estimators and retain representative failures for diagnosis.

### 40.7 Compare distances, rounds, and noise parameters

**Learning and derivation target:** Derive the scope of a scaling comparison and define rates consistently.

**Implementation and evidence target:** Report finite-size uncertainty and avoid claiming a general threshold from a small crossing.

### 40.8 From memory evidence to resource implications

**Learning and derivation target:** State which logical-gate or architecture assumptions are missing from a memory experiment.

**Implementation and evidence target:** Perform a scoped sensitivity estimate linked to Chapter 33.

### 40.9 Write a reproducible correction-study report

**Learning and derivation target:** Relate each result to the source claim and its limitations.

**Implementation and evidence target:** Deliver source/data records, reference checks, decoder configuration, failures and unresolved gaps.
