# Part 6. Physical Realizations and Quantum-System Architecture

**Detailed plan · 2026-10-20 · Scope fixed by Writing Baseline 1.0; prose and independent acceptance pending.** [All sections](../section-plan.md) · [Full plan](../book-plan.md) · [Reader continuity](../reader-continuity.md)

Each section specifies its argument and independent evidence. Framework implementation, mathematical review and reader review have separate status. Closing materials follow the [section-plan guide](../section-plan.md#how-to-read-the-specification).

<span id="ch-from-abstract-qubits-to-physical-quantum-systems"></span>

## Chapter 34

**From Abstract Qubits to Physical Quantum Systems**

**Reading level:** Core bridge with optional physics extensions. **Entry guidance:** 2–3, 5–6, 8 for entry; selected 9/28/29/30 only for corresponding optional branches.

**Branch design:** use selected common bridges and choose a platform. Basic compilation can instead start with a supplied target contract; microscopic platform physics is a separate branch.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-1"></span>

### 34.1 Levels, modes, and computational subspaces

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1).

**Section level:** core. **Required earlier sections:** [3.1](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-1), [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [8.2](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2).

**Learning and derivation target:** Define the physical Hilbert space, encoded qubit and leakage states; state the effective-model assumptions.

**Implementation and evidence target:** Compare a two-level approximation with a small multilevel model and quantify leakage.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-2"></span>

### 34.2 Oscillator and light-matter mathematics bridge

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-2).

**Section level:** core. **Required earlier sections:** [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5), [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1).

**Learning and derivation target:** Introduce ladder operators, Fock states and one interaction model before platform-specific use; explain truncation boundaries.

**Implementation and evidence target:** Check low-energy calculations while showing why finite truncations cannot satisfy the full oscillator commutator exactly.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-3"></span>

### 34.3 Driven systems, rotating frames, and resonance

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-3).

**Section level:** core. **Required earlier sections:** [3.4](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-4), [2.6](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-6), [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1).

**Learning and derivation target:** Derive a driven two-level model, a rotating-frame transformation and a scoped rotating-wave approximation.

**Implementation and evidence target:** Compare lab-frame and effective evolutions with consistent state/observable transformations.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-4"></span>

### 34.4 Preparation, control, and readout as an experiment

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-4).

**Section level:** core. **Required earlier sections:** [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [34.3](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-3).

**Learning and derivation target:** Connect calibrated control parameters and a measurement record to the abstract operations.

**Implementation and evidence target:** Build a complete small prepare-control-readout model with units and probability normalization.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-5"></span>

### 34.5 Digital, analog, and measurement-based models

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-5).

**Section level:** core. **Required earlier sections:** [19.8](../section-plans/03-algorithms.md#sec-hamiltonian-adiabatic-model), [30.10](../section-plans/05-fault-tolerance.md#sec-stabilizer-graph-state-mbqc).

**Learning and derivation target:** Distinguish gate sequences, Hamiltonian schedules and adaptive resource-state measurements; connect to 19.8 and the graph-state bridge in Chapter 30.

**Implementation and evidence target:** Compare precisely specified tasks and requested outputs rather than treating the models as interchangeable.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-6"></span>

### 34.6 Noise, leakage, loss, and hardware constraints

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-6).

**Section level:** core. **Required earlier sections:** [28.2](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-2), [28.3](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-3), [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1).

**Learning and derivation target:** Relate relaxation, dephasing, leakage and heralded erasure to architecture-specific models.

**Implementation and evidence target:** Check explicit channels and explain why equal quoted fidelities need not imply equal workload behavior.

<span id="sec-bosonic-error-correction-bridge"></span>

### 34.7 Oscillator encodings and bosonic correction [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-bosonic-error-correction-bridge).

**Section level:** advanced. **Required earlier sections:** [34.2](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-2), [29.5](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-5), [28.3](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-3).

**Learning and derivation target:** Use oscillator mathematics and the Chapter 29 correction condition to compare a representative cat/binomial/GKP encoding; distinguish ideal infinite-dimensional constructions from finite-energy approximations.

**Implementation and evidence target:** Check one tractable encoding/error example with convergence or analytic bounds; state the scope of protection and link photonic/superconducting applications rather than rederive the theory there.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-7"></span>
<span id="347-connectivity-transport-and-modular-architectures"></span>

### 34.8 Connectivity, transport, and modular architectures

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-7).

**Section level:** core. **Required earlier sections:** [4.5](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-5), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2), [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1).

**Learning and derivation target:** Define interaction graphs, movable qubits, optical links and simultaneous-operation constraints.

**Implementation and evidence target:** Construct explicit target descriptions and identify which constraints a compiler must preserve.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-8"></span>
<span id="348-a-fair-platform-comparison-framework"></span>

### 34.9 A fair platform-comparison framework

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-8).

**Section level:** core. **Required earlier sections:** [34.4](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-4), [34.6](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-6), [34.8](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-7), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Learning and derivation target:** Specify encoding, native entangler, readout, control, dominant errors and full resource assumptions.

**Implementation and evidence target:** Compare dated primary-source evidence; distinguish proposals, demonstrations and scalable-system projections.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-9"></span>
<span id="349-choose-a-platform-learning-branch"></span>

### 34.10 Choose a platform learning branch

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-9).

**Section level:** core. **Required earlier sections:** [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1), [34.3](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-3), [34.4](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-4), [34.8](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-7).

**Learning and derivation target:** Provide a prerequisite checklist and a common model-control-measurement worksheet for Chapters 35–40.

**Implementation and evidence target:** Complete one branch before Chapters 41–43; do not require sequential mastery of all platform specialties.

<span id="ch-superconducting-qubits-and-circuit-qed-control"></span>

## Chapter 35

**Superconducting Qubits and Circuit-QED Control**

**Reading level:** Advanced platform branch. **Entry guidance:** Selected common physics bridge in 34; no whole algorithm or fault-tolerance route is required.

<span id="sec-superconducting-qubits-and-circuit-qed-control-1"></span>

### 35.1 An electrical circuit becomes a quantum model

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-1).

**Section level:** advanced. **Required earlier sections:** [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1), [34.2](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-2).

**Learning and derivation target:** Introduce circuit coordinates and the effective Josephson model with a local classical-circuit bridge; identify assumptions rather than requiring unexplained BCS theory.

**Implementation and evidence target:** Derive a small effective Hamiltonian with explicit energy/frequency units.

<span id="sec-superconducting-qubits-and-circuit-qed-control-2"></span>

### 35.2 Anharmonicity and the transmon computational subspace

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-2).

**Section level:** advanced. **Required earlier sections:** [35.1](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-1), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Learning and derivation target:** Derive a scoped low-energy spectrum and explain why anharmonicity supports selective qubit control.

**Implementation and evidence target:** Compare truncated diagonalization and a justified approximation; quantify convergence.

<span id="sec-superconducting-qubits-and-circuit-qed-control-3"></span>

### 35.3 Microwave control and single-qubit rotations

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-3).

**Section level:** advanced. **Required earlier sections:** [34.3](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-3), [35.2](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-2).

**Learning and derivation target:** Derive drive phase/amplitude dependence in a declared rotating frame.

**Implementation and evidence target:** Compare controlled evolution with the target qubit rotation including leakage.

<span id="sec-superconducting-qubits-and-circuit-qed-control-4"></span>

### 35.4 Coupling and native two-qubit interactions

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-4).

**Section level:** advanced. **Required earlier sections:** [35.2](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-2), [35.3](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-3), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Learning and derivation target:** Derive one representative exchange or conditional-phase gate and compare other native families at an explicit model level.

**Implementation and evidence target:** Check the projected two-qubit action and leakage with a multilevel reference.

<span id="sec-superconducting-qubits-and-circuit-qed-control-5"></span>

### 35.5 Dispersive readout and assignment errors

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-5).

**Section level:** advanced. **Required earlier sections:** [34.4](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-4), [35.1](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-1).

**Learning and derivation target:** Develop a scoped resonator/readout model and distinguish measurement backaction from classical classification error.

**Implementation and evidence target:** Check outcome statistics and a separate assignment-error model.

<span id="sec-superconducting-qubits-and-circuit-qed-control-6"></span>

### 35.6 Decoherence, crosstalk, and calibration

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-6).

**Section level:** advanced. **Required earlier sections:** [28.2](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-2), [28.3](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-3), [35.4](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-4).

**Learning and derivation target:** Connect relaxation/dephasing and spectator interactions to a complete experiment.

**Implementation and evidence target:** Compare ideal and imperfect gates with dated calibration inputs and declared model limits.

<span id="sec-superconducting-qubits-and-circuit-qed-control-7"></span>

### 35.7 Target constraints for compilation

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-7).

**Section level:** advanced. **Required earlier sections:** [35.3](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-3), [35.4](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-4), [34.8](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-7).

**Learning and derivation target:** Specify native gates, coupling, frequency/simultaneity restrictions and frame updates.

**Implementation and evidence target:** Create a small target contract consumed by the compilation laboratories without claiming a provider integration.

<span id="sec-superconducting-qubits-and-circuit-qed-control-8"></span>

### 35.8 Superconducting-model laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-8).

**Section level:** advanced. **Required earlier sections:** [35.2](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-2), [35.3](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-3), [35.4](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-4), [35.5](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-5), [35.6](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-6).

**Learning and derivation target:** Integrate spectrum, drive, entangler and readout and state the boundary of the effective model.

**Implementation and evidence target:** Verify one complete experiment independently and report truncation, control and measurement error.

<span id="ch-trapped-ion-qubits-motional-gates-and-transport"></span>

## Chapter 36

**Trapped-Ion Qubits, Motional Gates, and Transport**

**Reading level:** Advanced platform branch. **Entry guidance:** Selected oscillator/drive/measurement bridge in 34.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-1"></span>

### 36.1 Internal states, trapping, and preparation

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-1).

**Section level:** advanced. **Required earlier sections:** [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1), [34.2](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-2).

**Learning and derivation target:** Specify a qubit encoding and explain trapping and cooling with a local physics bridge.

**Implementation and evidence target:** Record the effective levels, preparation assumptions and discarded degrees of freedom.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-2"></span>

### 36.2 Collective motion and sidebands

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-2).

**Section level:** advanced. **Required earlier sections:** [36.1](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-1), [34.2](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-2), [34.3](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-3).

**Learning and derivation target:** Derive a scoped ion-motion coupling and define the Lamb-Dicke/resolved-sideband approximations before use.

**Implementation and evidence target:** Compare low-occupation dynamics with converged oscillator truncations.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-3"></span>

### 36.3 Carrier drives and single-qubit control

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-3).

**Section level:** advanced. **Required earlier sections:** [36.1](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-1), [34.3](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-3).

**Learning and derivation target:** Derive a representative laser/microwave-driven rotation and frame convention.

**Implementation and evidence target:** Compare control-model and abstract-gate predictions.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-4"></span>

### 36.4 Motional entangling gates

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-4).

**Section level:** advanced. **Required earlier sections:** [36.2](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-2), [36.3](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-3).

**Learning and derivation target:** Derive one Mølmer-Sørensen or geometric-phase construction including a motion-return condition.

**Implementation and evidence target:** Compare joint spin-motion evolution and the reduced spin gate for several motional inputs.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-5"></span>

### 36.5 Readout, heating, and coherence

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-5).

**Section level:** advanced. **Required earlier sections:** [36.2](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-2), [34.4](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-4), [28.3](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-3).

**Learning and derivation target:** Distinguish fluorescence assignment, spontaneous processes and motional heating.

**Implementation and evidence target:** Test a complete model and state which omitted effects limit the approximation.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-6"></span>

### 36.6 Chains, QCCD transport, and photonic links

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-6).

**Section level:** advanced. **Required earlier sections:** [36.1](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-1), [34.8](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-7).

**Learning and derivation target:** Distinguish a chosen interaction model from transport/cooling/zone or modular-network overhead.

**Implementation and evidence target:** Model a tiny transport/operation schedule rather than assuming cost-free all-to-all execution.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-7"></span>

### 36.7 Target constraints for compilation

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-7).

**Section level:** advanced. **Required earlier sections:** [36.4](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-4), [36.6](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-6).

**Learning and derivation target:** Specify native entanglers, shared modes, zones, simultaneous operations and timing.

**Implementation and evidence target:** Create a target description and compare two schedules for the same declared architecture.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-8"></span>

### 36.8 Trapped-ion laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-8).

**Section level:** advanced. **Required earlier sections:** [36.2](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-2), [36.4](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-4), [36.5](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-5).

**Learning and derivation target:** Integrate internal-state control, motion, entanglement and readout.

**Implementation and evidence target:** Verify a gate and its thermal/truncation sensitivity with an independent reference and resource record.

<span id="ch-neutral-atom-arrays-and-rydberg-quantum-computing"></span>

## Chapter 37

**Neutral-Atom Arrays and Rydberg Quantum Computing**

**Reading level:** Advanced platform branch. **Entry guidance:** Selected common bridge in 34; 19 only for advanced dynamics/error analysis.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-1"></span>

### 37.1 Trapping, internal encodings, and rearrangement

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-1).

**Section level:** advanced. **Required earlier sections:** [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1), [34.8](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-7).

**Learning and derivation target:** Specify the computational states, optical-trap model and classical atom-position controls.

**Implementation and evidence target:** Build an explicit geometry and distinguish moving atoms from a logical SWAP.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-2"></span>

### 37.2 Rydberg interactions and blockade

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-2).

**Section level:** advanced. **Required earlier sections:** [37.1](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-1), [2.6](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-6).

**Learning and derivation target:** Derive a two-atom effective Hamiltonian and the assumptions of the blockade approximation.

**Implementation and evidence target:** Compare finite-interaction dynamics with the ideal blockade limit.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-3"></span>

### 37.3 Single-qubit and entangling control

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-3).

**Section level:** advanced. **Required earlier sections:** [37.2](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-2), [34.3](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-3).

**Learning and derivation target:** Derive one gate sequence and identify phases, leakage and interaction constraints.

**Implementation and evidence target:** Compare the gate with an independent two-/multilevel reference.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-4"></span>

### 37.4 Analog Hamiltonian programming

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-4).

**Section level:** advanced. **Required earlier sections:** [37.2](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-2), [19.1](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-1).

**Learning and derivation target:** Translate geometry, detuning and drive schedules into a declared many-body Hamiltonian.

**Implementation and evidence target:** Compare a small schedule with exact evolution without assuming arbitrary graph programmability.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-5"></span>

### 37.5 Transport, parallelism, and compilation

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-5).

**Section level:** advanced. **Required earlier sections:** [37.1](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-1), [37.3](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-3), [34.8](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-7).

**Learning and derivation target:** Model motion, blockade neighborhoods and simultaneous gate restrictions.

**Implementation and evidence target:** Compare two explicitly feasible arrangements/schedules and account for transport cost.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-6"></span>

### 37.6 Atom loss, readout, and imperfect interactions

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-6).

**Section level:** advanced. **Required earlier sections:** [37.2](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-2), [34.4](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-4), [28.3](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-3).

**Learning and derivation target:** Distinguish loss/erasure information, computational error and readout assignment.

**Implementation and evidence target:** Check model-specific outcome records and their treatment in a later correction workflow.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-7"></span>

### 37.7 Digital versus analog experiment contracts

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-7).

**Section level:** advanced. **Required earlier sections:** [37.3](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-3), [37.4](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-4).

**Learning and derivation target:** Specify inputs, admissible controls, outputs and error metrics for each mode.

**Implementation and evidence target:** Verify one digital and one analog small task with matched mathematical references.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-8"></span>

### 37.8 Neutral-atom laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-8).

**Section level:** advanced. **Required earlier sections:** [37.3](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-3), [37.4](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-4), [37.6](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-6).

**Learning and derivation target:** Connect geometry, Hamiltonian/control, noise and requested observable.

**Implementation and evidence target:** Record all constraints and compare independent dynamics before a hardware-access extension.

<span id="ch-photonic-encodings-optical-circuits-and-measurement-based-computation"></span>

## Chapter 38

**Photonic Encodings, Optical Circuits, and Measurement-Based Computation**

**Reading level:** Advanced platform branch. **Entry guidance:** 7 and selected oscillator/measurement bridge in 34; selected 30 for resource-state computation.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-1"></span>

### 38.1 Optical modes and qubit encodings

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-1).

**Section level:** advanced. **Required earlier sections:** [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1), [34.2](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-2).

**Learning and derivation target:** Introduce Fock states and polarization/path/time encodings; distinguish physical modes from encoded qubits.

**Implementation and evidence target:** Check the encoding isometry and the dimensions of a small optical model.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-2"></span>

### 38.2 Beam splitters, phases, and interferometers

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-2).

**Section level:** advanced. **Required earlier sections:** [38.1](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-1), [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3).

**Learning and derivation target:** Derive mode transformations and their action on selected photon-number states.

**Implementation and evidence target:** Compare mode-unitary and Fock-space calculations with declared phase conventions.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-3"></span>

### 38.3 Interference, sources, and detection

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-3).

**Section level:** advanced. **Required earlier sections:** [38.2](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-2), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2).

**Learning and derivation target:** Derive a two-photon interference example and state indistinguishability/detector assumptions.

**Implementation and evidence target:** Compare ideal probabilities with loss or distinguishability perturbations.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-4"></span>

### 38.4 Measurement-induced operations and heralding

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-4).

**Section level:** advanced. **Required earlier sections:** [38.3](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-3), [9.7](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-7).

**Learning and derivation target:** Derive a scoped conditional optical operation, its success probability and classical feed-forward.

**Implementation and evidence target:** Check all accepted/rejected branches; do not treat passive optics as deterministic universal qubit gates.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-5"></span>

### 38.5 Graph states, fusion, and logical computation

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-5).

**Section level:** advanced. **Required earlier sections:** [30.10](../section-plans/05-fault-tolerance.md#sec-stabilizer-graph-state-mbqc), [38.4](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-4).

**Learning and derivation target:** Use Chapter 30's measurement-based bridge to analyze one resource-state/fusion operation.

**Implementation and evidence target:** Verify stabilizer updates, logical corrections and failed-fusion outcomes on a tiny instance.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-6"></span>

### 38.6 Continuous-variable and bosonic branches [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-6).

**Section level:** advanced. **Required earlier sections:** [34.2](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-2), [38.2](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-2).

**Learning and derivation target:** Introduce quadratures, squeezing and Gaussian/non-Gaussian distinctions through a local mathematics bridge.

**Implementation and evidence target:** Compare a tractable Gaussian calculation or converged truncated-state model without equating a mode with a qubit.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-7"></span>

### 38.7 Loss, erasure, and multiplexing resources

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-7).

**Section level:** advanced. **Required earlier sections:** [38.3](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-3), [38.4](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-4), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Learning and derivation target:** Separate transmission/detection loss, heralding and resource-state generation cost.

**Implementation and evidence target:** Compute accepted logical-output probability with explicit discarded attempts.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-8"></span>

### 38.8 Photonic compilation and architecture contracts

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-8).

**Section level:** advanced. **Required earlier sections:** [38.2](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-2), [38.4](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-4), [34.8](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-7).

**Learning and derivation target:** Specify interferometers, resource states, timing, detection and feed-forward targets.

**Implementation and evidence target:** Translate one logical task into a declared optical/measurement pattern and verify its output contract.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-9"></span>

### 38.9 Photonic laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-9).

**Section level:** advanced. **Required earlier sections:** [38.2](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-2), [38.3](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-3), [38.4](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-4), [38.7](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-7).

**Learning and derivation target:** Connect encoding, optical transformations, conditional detection and resource accounting.

**Implementation and evidence target:** Report model assumptions, truncation if used, success probability and independent checks.

<span id="ch-semiconductor-spin-qubits-and-exchange-based-architectures"></span>

## Chapter 39

**Semiconductor Spin Qubits and Exchange-Based Architectures**

**Reading level:** Advanced platform branch. **Entry guidance:** Selected common bridge in 34.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-1"></span>

### 39.1 Spin encodings and confined-charge models

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-1).

**Section level:** advanced. **Required earlier sections:** [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1).

**Learning and derivation target:** Introduce single-spin, encoded-spin and donor/dot choices with explicit effective assumptions.

**Implementation and evidence target:** Identify the physical and computational subspaces of a tiny model.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-2"></span>

### 39.2 Zeeman control and electrically driven rotations

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-2).

**Section level:** advanced. **Required earlier sections:** [39.1](../section-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-1), [34.3](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-3).

**Learning and derivation target:** Derive a scoped spin-control Hamiltonian and resonance convention.

**Implementation and evidence target:** Compare time evolution with an independent qubit rotation.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-3"></span>

### 39.3 Exchange and entangling operations

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-3).

**Section level:** advanced. **Required earlier sections:** [39.2](../section-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-2), [2.6](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-6).

**Learning and derivation target:** Derive a two-spin exchange evolution and its computational action.

**Implementation and evidence target:** Check a selected entangler and account for local phases.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-4"></span>

### 39.4 Charge, valley, and leakage degrees of freedom

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-4).

**Section level:** advanced. **Required earlier sections:** [39.1](../section-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-1), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Learning and derivation target:** Explain which extra levels a selected semiconductor model includes and when they matter.

**Implementation and evidence target:** Compare effective-qubit results with a converged small multilevel reference.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-5"></span>

### 39.5 Initialization and spin-to-charge readout

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-5).

**Section level:** advanced. **Required earlier sections:** [39.1](../section-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-1), [34.4](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-4).

**Learning and derivation target:** Derive a scoped state-preparation/readout process and distinguish its errors.

**Implementation and evidence target:** Compare latent quantum outcomes and reported classical records.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-6"></span>

### 39.6 Noise, variability, and calibration

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-6).

**Section level:** advanced. **Required earlier sections:** [39.3](../section-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-3), [28.2](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-2), [28.3](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-3).

**Learning and derivation target:** Model a selected charge/hyperfine/control perturbation without universal platform claims.

**Implementation and evidence target:** Study sensitivity and identify which parameters require measured input.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-7"></span>

### 39.7 Coupling, shuttling, and modular constraints

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-7).

**Section level:** advanced. **Required earlier sections:** [39.3](../section-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-3), [34.8](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-7).

**Learning and derivation target:** Specify a target's couplings, transport/control resources and timing.

**Implementation and evidence target:** Build a small compilation contract with explicitly costed movement and scheduling.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-8"></span>

### 39.8 Spin-qubit laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-8).

**Section level:** advanced. **Required earlier sections:** [39.2](../section-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-2), [39.3](../section-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-3), [39.5](../section-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-5), [39.6](../section-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-6).

**Learning and derivation target:** Integrate encoding, exchange/control, readout and imperfections.

**Implementation and evidence target:** Verify one complete task independently and record the limits of the effective model.

<span id="ch-topological-quantum-computation-and-candidate-physical-realizations"></span>

## Chapter 40

**Topological Quantum Computation and Candidate Physical Realizations**

**Reading level:** Advanced platform branch. **Entry guidance:** 7–8 and selected 34 for entry; 25 for Majorana models and 29–32 for protection/logical-resource comparisons.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-1"></span>

### 40.1 Topology, protection, and distinct meanings

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-1).

**Section level:** advanced. **Required earlier sections:** [7.1](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-1), [8.2](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2), [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1).

**Learning and derivation target:** Distinguish topological order, topological codes and a physical non-Abelian-quasiparticle proposal.

**Implementation and evidence target:** Classify explicit claims and identify the mathematical versus experimental evidence needed.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-2"></span>

### 40.2 Fusion spaces and encoded information

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-2).

**Section level:** advanced. **Required earlier sections:** [40.1](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-1), [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1).

**Learning and derivation target:** Introduce charge sectors and fusion rules before using their notation.

**Implementation and evidence target:** Count a small fusion space and state the encoding assumptions.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-3"></span>

### 40.3 Fusion bases, F/R moves, and braiding

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-3).

**Section level:** advanced. **Required earlier sections:** [40.2](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-2), [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3).

**Learning and derivation target:** Define fusion-basis recoupling and exchange matrices before use; derive one specified braid representation and state its consistency conditions and proof scope.

**Implementation and evidence target:** Check algebraic consistency and compare ordered braid products.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-4"></span>

### 40.4 Measurement, corrections, and computational power

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-4).

**Section level:** advanced. **Required earlier sections:** [40.3](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-3), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [32.6](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-6).

**Learning and derivation target:** Explain a selected model's measurements, available gates and extra resources needed for universality.

**Implementation and evidence target:** Verify a small logical operation without assuming braiding is universally sufficient.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-5"></span>

### 40.5 Majorana models and parity encoding [Advanced]

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-5).

**Section level:** advanced. **Required earlier sections:** [25.2](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-2), [25.3](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-3), [40.2](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-2).

**Learning and derivation target:** Introduce a scoped fermionic toy Hamiltonian and parity constraints using the Chapter 25 bridge.

**Implementation and evidence target:** Compare an exact finite model with claimed low-energy/parity behavior and finite-size limits.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-6"></span>

### 40.6 Protection assumptions and failure mechanisms

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-6).

**Section level:** advanced. **Required earlier sections:** [40.1](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-1), [28.1](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-1), [29.5](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-5).

**Learning and derivation target:** Explain gap, locality, poisoning, finite size and readout assumptions of a selected model.

**Implementation and evidence target:** Perturb a tractable model and distinguish conditional robustness from immunity to all errors.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-7"></span>

### 40.7 Experiments, signatures, and unresolved evidence

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-7).

**Section level:** advanced. **Required earlier sections:** [40.5](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-5), [40.6](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-6).

**Learning and derivation target:** Separate Abelian statistics, encoded Ising/D4/Fibonacci braiding, material parity readout and protected logical operation; evaluate competing interpretations with dated primary sources.

**Implementation and evidence target:** Follow TOPO-01–09 and dispute cases D1–D9. Full accepted comment, 2025 response, published supplement and joint author/reviewer record are checked. Exact final-reply matching, versioned raw/corrected data reproduction and specialist interpretation remain pending.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-8"></span>

### 40.8 Topological compilation and laboratory

**Result/proof/source specification:** [Scholarly plan](../proof-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-8).

**Section level:** advanced. **Required earlier sections:** [40.3](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-3), [40.4](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-4), [40.6](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-6), [40.7](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-7).

**Learning and derivation target:** Specify allowed braids/measurements, corrections and non-topological supplements.

**Implementation and evidence target:** Verify a toy encoded operation and its resource/error assumptions; state that it is not a hardware reproduction.
