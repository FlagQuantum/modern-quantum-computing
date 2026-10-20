# Result and proof plan: Physical Realizations and Quantum-System Architecture

[Depth definitions](../proof-plan.md#proof-depth-contract) · [Source catalogue](../references/proof-sources.md) · [Volume plan](../volume-plan.md)

Authoring specifications only. No result/proof/API is certified by this plan. F/M/R have different scope; imported results are the exact prerequisite sections linked below.

## Chapter 34: From Abstract Qubits to Physical Quantum Systems

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-1"></span>

### 34.1 Levels, modes, and computational subspaces

**Core result / role:** Encoded subspace and leakage projector.

**Assumptions and scope:** Finite truncation of a specified physical Hilbert space.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive projected logical action and distinguish leakage from an in-subspace Pauli error.

**Imported earlier results:** [3.1](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-1), [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [8.2](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2).

**Exact source targets:** [NC:7.2.1](../references/proof-sources.md#source-nc-7-2-1): Section 7.2.1 Representation of quantum information.

**Independent evidence target:** Compare a two-level approximation with a small multilevel model and quantify leakage.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-2"></span>

### 34.2 Oscillator and light-matter mathematics bridge

**Core result / role:** Oscillator ladder algebra and truncation boundary.

**Assumptions and scope:** Harmonic-oscillator/Fock model; finite numerical cutoff.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive number-state matrix elements and explicitly show the cutoff commutator defect.

**Imported earlier results:** [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5), [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1).

**Exact source targets:** [NC:7.3.2](../references/proof-sources.md#source-nc-7-3-2): Section 7.3.2 The Hamiltonian.

**Independent evidence target:** Check low-energy calculations while showing why finite truncations cannot satisfy the full oscillator commutator exactly.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-3"></span>

### 34.3 Driven systems, rotating frames, and resonance

**Core result / role:** Rotating-frame transformation and a scoped RWA.

**Assumptions and scope:** Declared drive frequency, amplitude and detuning regime.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive the frame Hamiltonian and omitted terms; state the approximation domain.

**Imported earlier results:** [3.4](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-4), [2.6](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-6), [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1).

**Exact source targets:** [SC:IV.D](../references/proof-sources.md#source-sc-iv-d): Section IV D Single-qubit gates.

**Independent evidence target:** Compare lab-frame and effective evolutions with consistent state/observable transformations.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-4"></span>

### 34.4 Preparation, control, and readout as an experiment

**Core result / role:** Preparation-control-readout defines an experiment map.

**Assumptions and scope:** Explicit physical preparation and measurement model.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Translate calibrated controls into operations and measured records; distinguish model inputs from observed values.

**Imported earlier results:** [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [34.3](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-3).

**Exact source targets:** [NC:7.2](../references/proof-sources.md#source-nc-7-2): Section 7.2 Conditions for quantum computation.

**Independent evidence target:** Build a complete small prepare-control-readout model with units and probability normalization.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-5"></span>

### 34.5 Digital, analog, and measurement-based models

**Core result / role:** Digital, analog and measurement-based computational contracts.

**Assumptions and scope:** Declared allowed controls, outputs and adaptive resources.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Compare the three models through explicit tasks; do not assert an unproved efficient equivalence.

**Imported earlier results:** [19.8](../section-plans/03-algorithms.md#sec-hamiltonian-adiabatic-model), [30.10](../section-plans/05-fault-tolerance.md#sec-stabilizer-graph-state-mbqc).

**Exact source targets:** [ADI:adiabatic](../references/proof-sources.md#source-adi-adiabatic): Proposed adiabatic algorithm and spectral-gap discussion; [MBQC:pattern](../references/proof-sources.md#source-mbqc-pattern): Computation by adaptive one-qubit measurements and byproduct operators.

**Independent evidence target:** Compare precisely specified tasks and requested outputs rather than treating the models as interchangeable.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-6"></span>

### 34.6 Noise, leakage, loss, and hardware constraints

**Core result / role:** Leakage, loss and erasure require distinct result models.

**Assumptions and scope:** Specified encoded subspace and detection flag.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive selected channel/flag maps and show when an erasure is heralded.

**Imported earlier results:** [28.2](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-2), [28.3](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-3), [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1).

**Exact source targets:** [SC:III.B](../references/proof-sources.md#source-sc-iii-b): Section III B Modeling noise and decoherence; [FUSION:errors](../references/proof-sources.md#source-fusion-errors): Section VII D Errors in FBQC and Appendix on loss/erasure.

**Independent evidence target:** Check explicit channels and explain why equal quoted fidelities need not imply equal workload behavior.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-bosonic-error-correction-bridge"></span>

### 34.7 Oscillator encodings and bosonic correction [Advanced]

**Core result / role:** Selected bosonic code satisfies a scoped correction condition.

**Assumptions and scope:** Finite-energy/truncated code and explicit error span.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Verify Knill-Laflamme for logical states (Fock-0 plus Fock-4)/sqrt(2) and Fock-2 under error span {identity, annihilation}; distinguish this selected single-loss condition from finite-time damping and ideal GKP limits.

**Imported earlier results:** [34.2](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-2), [29.5](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-5), [28.3](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-3).

**Exact source targets:** [BOSON:codes](../references/proof-sources.md#source-boson-codes): Sections 4.2 GKP, 5.2 Cat, 5.3 Binomial; Section 6 noise.

**Independent evidence target:** Check one tractable encoding/error example with convergence or analytic bounds; state the scope of protection and link photonic/superconducting applications rather than rederive the theory there.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-7"></span>

### 34.8 Connectivity, transport, and modular architectures

**Core result / role:** Interaction, transport and photonic links are different resources.

**Assumptions and scope:** Specified physical architecture and timing model.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** State legal interactions, movement, state transfer and classical-message requirements.

**Imported earlier results:** [4.5](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-5), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2), [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1).

**Exact source targets:** [ION:IV.A](../references/proof-sources.md#source-ion-iv-a): Section IV A Architectures and Techniques for Scaling; [NET:links](../references/proof-sources.md#source-net-links): Elementary quantum networks, nodes, channels and entanglement distribution.

**Independent evidence target:** Construct explicit target descriptions and identify which constraints a compiler must preserve.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-8"></span>

### 34.9 A fair platform-comparison framework

**Core result / role:** Platform comparisons require matched physical contracts.

**Assumptions and scope:** Dated evidence and same task/error/resource target.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Complete the common worksheet; separate model estimates from demonstrated operations.

**Imported earlier results:** [34.4](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-4), [34.6](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-6), [34.8](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-7), [14.6](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Compare dated primary-source evidence; distinguish proposals, demonstrations and scalable-system projections.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-9"></span>

### 34.10 Choose a platform learning branch

**Core result / role:** Platform branch entry and exit checklist.

**Assumptions and scope:** Selected common bridges and one target model.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Choose a path and record prerequisite closure, target contract and comparison limits.

**Imported earlier results:** [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1), [34.3](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-3), [34.4](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-4), [34.8](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-7).

**Exact source targets:** [ED:routes](../references/proof-sources.md#source-ed-routes): Checked prerequisite paths.

**Independent evidence target:** Complete one branch before Chapters 41–43; do not require sequential mastery of all platform specialties.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 35: Superconducting Qubits and Circuit-QED Control

<span id="sec-superconducting-qubits-and-circuit-qed-control-1"></span>

### 35.1 An electrical circuit becomes a quantum model

**Core result / role:** Circuit quantization for a selected LC/Josephson model.

**Assumptions and scope:** Lumped-element approximation; declared canonical variables.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive the Hamiltonian, commutator and oscillator limit with units.

**Imported earlier results:** [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1), [34.2](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-2).

**Exact source targets:** [SC:II.A](../references/proof-sources.md#source-sc-ii-a): Section II A From quantum harmonic oscillator to the transmon.

**Independent evidence target:** Derive a small effective Hamiltonian with explicit energy/frequency units.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-superconducting-qubits-and-circuit-qed-control-2"></span>

### 35.2 Anharmonicity and the transmon computational subspace

**Core result / role:** Transmon anharmonicity and encoded-subspace approximation.

**Assumptions and scope:** Large Josephson/charging-energy ratio; specified retained levels.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive the selected perturbative spectrum and state its truncation/parameter limits.

**Imported earlier results:** [35.1](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-1), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Exact source targets:** [SC:II.A](../references/proof-sources.md#source-sc-ii-a): Section II A From quantum harmonic oscillator to the transmon; [SC:II.B](../references/proof-sources.md#source-sc-ii-b): Section II B Qubit Hamiltonian engineering.

**Independent evidence target:** Compare truncated diagonalization and a justified approximation; quantify convergence.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-superconducting-qubits-and-circuit-qed-control-3"></span>

### 35.3 Microwave control and single-qubit rotations

**Core result / role:** Driven superconducting-qubit rotation.

**Assumptions and scope:** Projected dipole coupling and scoped RWA.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive drive phase, detuning and rotation angle; check leakage outside the approximation.

**Imported earlier results:** [34.3](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-3), [35.2](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-2).

**Exact source targets:** [SC:IV.D](../references/proof-sources.md#source-sc-iv-d): Section IV D Single-qubit gates.

**Independent evidence target:** Compare controlled evolution with the target qubit rotation including leakage.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-superconducting-qubits-and-circuit-qed-control-4"></span>

### 35.4 Coupling and native two-qubit interactions

**Core result / role:** Effective exchange interaction and the iSWAP gate.

**Assumptions and scope:** Chosen coupling, detuning and multilevel model.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive the effective interaction and ideal gate; expose neglected spectator/leakage terms.

**Imported earlier results:** [35.2](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-2), [35.3](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-3), [5.2](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).

**Exact source targets:** [SC:II.C](../references/proof-sources.md#source-sc-ii-c): Section II C Interaction Hamiltonian engineering; [SC:IV.E](../references/proof-sources.md#source-sc-iv-e): Section IV E The iSWAP two-qubit gate in tunable qubits.

**Independent evidence target:** Check the projected two-qubit action and leakage with a multilevel reference.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-superconducting-qubits-and-circuit-qed-control-5"></span>

### 35.5 Dispersive readout and assignment errors

**Core result / role:** Dispersive readout response and assignment matrix.

**Assumptions and scope:** Dispersive regime; declared resonator/readout model.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive the qubit-dependent response and the classical confusion-matrix probabilities.

**Imported earlier results:** [34.4](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-4), [35.1](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-1).

**Exact source targets:** [SC:V.A](../references/proof-sources.md#source-sc-v-a): Section V A Dispersive readout; [SC:V.B](../references/proof-sources.md#source-sc-v-b): Section V B Measuring the resonator amplitude and phase.

**Independent evidence target:** Check outcome statistics and a separate assignment-error model.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-superconducting-qubits-and-circuit-qed-control-6"></span>

### 35.6 Decoherence, crosstalk, and calibration

**Core result / role:** Relaxation/dephasing and calibration limits.

**Assumptions and scope:** Specified noise spectra and operating point.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive one decay law; separate fitted parameters, drift and crosstalk assumptions.

**Imported earlier results:** [28.2](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-2), [28.3](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-3), [35.4](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-4).

**Exact source targets:** [SC:III.B](../references/proof-sources.md#source-sc-iii-b): Section III B Modeling noise and decoherence; [SC:III.C](../references/proof-sources.md#source-sc-iii-c): Section III C Common examples of noise.

**Independent evidence target:** Compare ideal and imperfect gates with dated calibration inputs and declared model limits.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-superconducting-qubits-and-circuit-qed-control-7"></span>

### 35.7 Target constraints for compilation

**Core result / role:** Superconducting target contract.

**Assumptions and scope:** Explicit gate families, couplings, durations and exclusions.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Translate the model into compiler constraints; no hardware-performance theorem.

**Imported earlier results:** [35.3](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-3), [35.4](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-4), [34.8](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-7).

**Exact source targets:** [SC:IV.H](../references/proof-sources.md#source-sc-iv-h): Section IV H Gate implementations with tunable coupling; [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Create a small target contract consumed by the compilation laboratories without claiming a provider integration.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-superconducting-qubits-and-circuit-qed-control-8"></span>

### 35.8 Superconducting-model laboratory

**Core result / role:** Superconducting-model acceptance protocol.

**Assumptions and scope:** Independent multilevel solver and cutoff/drive convergence.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Check units, frames, leakage, readout and the declared native gate.

**Imported earlier results:** [35.2](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-2), [35.3](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-3), [35.4](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-4), [35.5](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-5), [35.6](../section-plans/physical-platforms.md#sec-superconducting-qubits-and-circuit-qed-control-6).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Verify one complete experiment independently and report truncation, control and measurement error.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 36: Trapped-Ion Qubits, Motional Gates, and Transport

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-1"></span>

### 36.1 Internal states, trapping, and preparation

**Core result / role:** Internal-state encoding and trapped-particle approximation.

**Assumptions and scope:** Selected trapped 171Yb+ hyperfine encoding; harmonic confinement and declared preparation model; other species are comparisons.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive a scoped harmonic confinement and encoded-state picture; state omitted atomic structure.

**Imported earlier results:** [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1), [34.2](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-2).

**Exact source targets:** [ION:II.A](../references/proof-sources.md#source-ion-ii-a): Section II A Trapping Individual Ions; [ION:II.B](../references/proof-sources.md#source-ion-ii-b): Section II B Internal States: Qubit Levels.

**Independent evidence target:** Record the effective levels, preparation assumptions and discarded degrees of freedom.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-2"></span>

### 36.2 Collective motion and sidebands

**Core result / role:** Motional normal modes and sideband coupling.

**Assumptions and scope:** Harmonic motion; stated Lamb-Dicke expansion.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive normal-mode coordinates and carrier/red/blue terms with validity conditions.

**Imported earlier results:** [36.1](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-1), [34.2](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-2), [34.3](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-3).

**Exact source targets:** [ION:II.C](../references/proof-sources.md#source-ion-ii-c): Section II C Motional States; [ION:III.B](../references/proof-sources.md#source-ion-iii-b): Section III B Qubit Logic.

**Independent evidence target:** Compare low-occupation dynamics with converged oscillator truncations.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-3"></span>

### 36.3 Carrier drives and single-qubit control

**Core result / role:** Carrier rotation in the chosen frame.

**Assumptions and scope:** Resolved control model and specified motional state.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive the selected rotation and state off-resonant coupling assumptions.

**Imported earlier results:** [36.1](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-1), [34.3](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-3).

**Exact source targets:** [ION:III.B](../references/proof-sources.md#source-ion-iii-b): Section III B Qubit Logic.

**Independent evidence target:** Compare control-model and abstract-gate predictions.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-4"></span>

### 36.4 Motional entangling gates

**Core result / role:** Two-ion Mølmer-Sørensen gate and phase-space closure.

**Assumptions and scope:** Selected interaction and detuning; harmonic modes.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive spin-dependent displacement and the closed-loop geometric phase; quantify residual motion.

**Imported earlier results:** [36.2](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-2), [36.3](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-3).

**Exact source targets:** [ION:III.B](../references/proof-sources.md#source-ion-iii-b): Section III B Qubit Logic.

**Independent evidence target:** Compare joint spin-motion evolution and the reduced spin gate for several motional inputs.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-5"></span>

### 36.5 Readout, heating, and coherence

**Core result / role:** Readout and heating affect different subsystems.

**Assumptions and scope:** Specified fluorescence and motional-noise models.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive selected assignment/heating observables and distinguish their error channels.

**Imported earlier results:** [36.2](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-2), [34.4](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-4), [28.3](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-3).

**Exact source targets:** [ION:III.C](../references/proof-sources.md#source-ion-iii-c): Section III C State Detection; [ION:IV.B](../references/proof-sources.md#source-ion-iv-b): Section IV B Error Reduction and Mitigation.

**Independent evidence target:** Test a complete model and state which omitted effects limit the approximation.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-6"></span>

### 36.6 Chains, QCCD transport, and photonic links

**Core result / role:** Transport/modular operations have time and excitation costs.

**Assumptions and scope:** Explicit chain/QCCD/link model.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive one finite schedule/cost example; do not equate physical transport with free relabeling.

**Imported earlier results:** [36.1](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-1), [34.8](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-7).

**Exact source targets:** [ION:IV.A](../references/proof-sources.md#source-ion-iv-a): Section IV A Architectures and Techniques for Scaling; [NET:links](../references/proof-sources.md#source-net-links): Elementary quantum networks, nodes, channels and entanglement distribution.

**Independent evidence target:** Model a tiny transport/operation schedule rather than assuming cost-free all-to-all execution.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-7"></span>

### 36.7 Target constraints for compilation

**Core result / role:** Ion target contract.

**Assumptions and scope:** Explicit native interactions, modes and concurrency.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Translate mode participation and transport/readout constraints into a target specification.

**Imported earlier results:** [36.4](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-4), [36.6](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-6).

**Exact source targets:** [ION:IV.A](../references/proof-sources.md#source-ion-iv-a): Section IV A Architectures and Techniques for Scaling; [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Create a target description and compare two schedules for the same declared architecture.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-8"></span>

### 36.8 Trapped-ion laboratory

**Core result / role:** Trapped-ion acceptance protocol.

**Assumptions and scope:** Independent oscillator/spin reference and convergence tests.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Check motional return, frames, gate angle and transport assumptions.

**Imported earlier results:** [36.2](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-2), [36.4](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-4), [36.5](../section-plans/physical-platforms.md#sec-trapped-ion-qubits-motional-gates-and-transport-5).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Verify a gate and its thermal/truncation sensitivity with an independent reference and resource record.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 37: Neutral-Atom Arrays and Rydberg Quantum Computing

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-1"></span>

### 37.1 Trapping, internal encodings, and rearrangement

**Core result / role:** Neutral-atom register and loading/readout contract.

**Assumptions and scope:** Selected rubidium ground/Rydberg model, optical traps and explicit occupancy assumptions; digital gates add a second stable ground state locally.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive a selected trap/register approximation and identify loading/rearrangement assumptions.

**Imported earlier results:** [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1), [34.8](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-7).

**Exact source targets:** [ATOM:2.1](../references/proof-sources.md#source-atom-2-1): Section 2.1 Operating an atomic qubit register.

**Independent evidence target:** Build an explicit geometry and distinguish moving atoms from a logical SWAP.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-2"></span>

### 37.2 Rydberg interactions and blockade

**Core result / role:** Rydberg blockade from a finite interacting model.

**Assumptions and scope:** Specified detuning, Rabi coupling and interaction energy.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Diagonalize a two-atom model and derive a controlled blockade limit.

**Imported earlier results:** [37.1](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-1), [2.6](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-6).

**Exact source targets:** [ATOM:2.2.1](../references/proof-sources.md#source-atom-2-2-1): Section 2.2.1 Digital quantum processing.

**Independent evidence target:** Compare finite-interaction dynamics with the ideal blockade limit.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-3"></span>

### 37.3 Single-qubit and entangling control

**Core result / role:** Three-pulse blockade controlled-phase sequence in a declared three-level atom model.

**Assumptions and scope:** Declared pulse model and blockade regime.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive ideal branch phases and quantify finite-blockade/leakage effects.

**Imported earlier results:** [37.2](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-2), [34.3](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-3).

**Exact source targets:** [ATOM:2.2.1](../references/proof-sources.md#source-atom-2-2-1): Section 2.2.1 Digital quantum processing.

**Independent evidence target:** Compare the gate with an independent two-/multilevel reference.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-4"></span>

### 37.4 Analog Hamiltonian programming

**Core result / role:** Geometry determines an analog Hamiltonian.

**Assumptions and scope:** Specified interaction law and available local/global controls.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive coupling coefficients and reachable model; do not assume arbitrary graph programming.

**Imported earlier results:** [37.2](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-2), [19.1](../section-plans/03-algorithms.md#sec-hamiltonian-simulation-and-error-bounds-1).

**Exact source targets:** [ATOM:2.2.2](../references/proof-sources.md#source-atom-2-2-2): Section 2.2.2 Analog quantum processing.

**Independent evidence target:** Compare a small schedule with exact evolution without assuming arbitrary graph programmability.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-5"></span>

### 37.5 Transport, parallelism, and compilation

**Core result / role:** Movement and parallelism constrain the schedule.

**Assumptions and scope:** Explicit geometry, movement and blockade exclusions.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Construct a legal finite schedule and identify incompatible concurrent operations.

**Imported earlier results:** [37.1](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-1), [37.3](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-3), [34.8](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-7).

**Exact source targets:** [ATOM:4.2](../references/proof-sources.md#source-atom-4-2): Section 4.2 Hamiltonian control over the device.

**Independent evidence target:** Compare two explicitly feasible arrangements/schedules and account for transport cost.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-6"></span>

### 37.6 Atom loss, readout, and imperfect interactions

**Core result / role:** Loss/readout/interactions produce different error records.

**Assumptions and scope:** Declared detection and loss model.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive a selected flagged channel and distinguish missing atoms from measurement bit flips.

**Imported earlier results:** [37.2](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-2), [34.4](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-4), [28.3](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-3).

**Exact source targets:** [ATOM:2.1](../references/proof-sources.md#source-atom-2-1): Section 2.1 Operating an atomic qubit register; [ATOM:2.2.3](../references/proof-sources.md#source-atom-2-2-3): Section 2.2.3 Prospects for improving QPU performance.

**Independent evidence target:** Check model-specific outcome records and their treatment in a later correction workflow.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-7"></span>

### 37.7 Digital versus analog experiment contracts

**Core result / role:** Digital and analog correctness use different equivalence tasks.

**Assumptions and scope:** Declared requested output and allowed controls.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** State the gate-unitary versus Hamiltonian-schedule contract and relevant error metric.

**Imported earlier results:** [37.3](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-3), [37.4](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-4).

**Exact source targets:** [ATOM:2.2.1](../references/proof-sources.md#source-atom-2-2-1): Section 2.2.1 Digital quantum processing; [ATOM:2.2.2](../references/proof-sources.md#source-atom-2-2-2): Section 2.2.2 Analog quantum processing.

**Independent evidence target:** Verify one digital and one analog small task with matched mathematical references.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-8"></span>

### 37.8 Neutral-atom laboratory

**Core result / role:** Neutral-atom acceptance protocol.

**Assumptions and scope:** Independent few-atom solver and parameter convergence.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Check blockade, geometric couplings, loss flags and pulse/schedule assumptions.

**Imported earlier results:** [37.3](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-3), [37.4](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-4), [37.6](../section-plans/physical-platforms.md#sec-neutral-atom-arrays-and-rydberg-quantum-computing-6).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Record all constraints and compare independent dynamics before a hardware-access extension.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 38: Photonic Encodings, Optical Circuits, and Measurement-Based Computation

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-1"></span>

### 38.1 Optical modes and qubit encodings

**Core result / role:** Optical modes and dual-rail qubit subspace.

**Assumptions and scope:** Bosonic modes; fixed photon-number encoding.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the encoded basis and separate physical modes from encoded qubits.

**Imported earlier results:** [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1), [34.2](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-2).

**Exact source targets:** [OPTICS:II](../references/proof-sources.md#source-optics-ii): Section II Bosonic Modes.

**Independent evidence target:** Check the encoding isometry and the dimensions of a small optical model.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-2"></span>

### 38.2 Beam splitters, phases, and interferometers

**Core result / role:** Passive linear optics preserves bosonic commutation.

**Assumptions and scope:** Unitary mode transformation and fixed phase convention.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive beam-splitter/phase action on creation operators and encoded states.

**Imported earlier results:** [38.1](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-1), [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3).

**Exact source targets:** [OPTICS:III](../references/proof-sources.md#source-optics-iii): Section III Optical Elements.

**Independent evidence target:** Compare mode-unitary and Fock-space calculations with declared phase conventions.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-3"></span>

### 38.3 Interference, sources, and detection

**Core result / role:** Two-photon interference depends on indistinguishability.

**Assumptions and scope:** Specified source overlap, loss and detection model.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive the ideal Hong-Ou-Mandel amplitudes and delimit partial distinguishability.

**Imported earlier results:** [38.2](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-2), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2).

**Exact source targets:** [OPTICS:III](../references/proof-sources.md#source-optics-iii): Section III Optical Elements.

**Independent evidence target:** Compare ideal probabilities with loss or distinguishability perturbations.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-4"></span>

### 38.4 Measurement-induced operations and heralding

**Core result / role:** KLM nonlinear-sign operation as a heralded Kraus map.

**Assumptions and scope:** Explicit ancilla photons, detection pattern and optical circuit.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the selected Kraus operator, success probability and failed branches.

**Imported earlier results:** [38.3](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-3), [9.7](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-7).

**Exact source targets:** [OPTICS:conditional](../references/proof-sources.md#source-optics-conditional): Sections IV-V conditional operations and selected gate construction.

**Independent evidence target:** Check all accepted/rejected branches; do not treat passive optics as deterministic universal qubit gates.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-5"></span>

### 38.5 Graph states, fusion, and logical computation

**Core result / role:** Fusion/graph-state computation and byproduct tracking.

**Assumptions and scope:** Specified small resource state and fusion measurement.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the successful and failed graph operations; defer architecture-scale threshold claims.

**Imported earlier results:** [30.10](../section-plans/05-fault-tolerance.md#sec-stabilizer-graph-state-mbqc), [38.4](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-4).

**Exact source targets:** [FUSION:II](../references/proof-sources.md#source-fusion-ii): Section II Fusion, especially linear-optical fusion; [MBQC:pattern](../references/proof-sources.md#source-mbqc-pattern): Computation by adaptive one-qubit measurements and byproduct operators.

**Independent evidence target:** Verify stabilizer updates, logical corrections and failed-fusion outcomes on a tiny instance.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-6"></span>

### 38.6 Continuous-variable and bosonic branches [Advanced]

**Core result / role:** CV Gaussian operations and non-Gaussian resource boundary.

**Assumptions and scope:** Declared quadratures, covariance convention and finite-energy approximation.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive selected Gaussian transformations; distinguish idealized bosonic codes and encoded qubit operations.

**Imported earlier results:** [34.2](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-2), [38.2](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-2).

**Exact source targets:** [BOSON:modes](../references/proof-sources.md#source-boson-modes): Section 3 Bosonic modes and Section 4 finite-energy/precision discussion; [OPTICS:II](../references/proof-sources.md#source-optics-ii): Section II Bosonic Modes.

**Independent evidence target:** Compare a tractable Gaussian calculation or converged truncated-state model without equating a mode with a qubit.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-7"></span>

### 38.7 Loss, erasure, and multiplexing resources

**Core result / role:** Loss/erasure and multiplexing resource arithmetic.

**Assumptions and scope:** Specified independent/correlated success assumptions.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive one success/overhead calculation and state where correlations break it.

**Imported earlier results:** [38.3](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-3), [38.4](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-4), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Exact source targets:** [FUSION:errors](../references/proof-sources.md#source-fusion-errors): Section VII D Errors in FBQC and Appendix on loss/erasure.

**Independent evidence target:** Compute accepted logical-output probability with explicit discarded attempts.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-8"></span>

### 38.8 Photonic compilation and architecture contracts

**Core result / role:** Photonic target includes sources, detection and feed-forward.

**Assumptions and scope:** Explicit mode/encoding/conditional-operation contract.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Specify timing, routing, heralding and retained classical records.

**Imported earlier results:** [38.2](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-2), [38.4](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-4), [34.8](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-7).

**Exact source targets:** [FUSION:architecture](../references/proof-sources.md#source-fusion-architecture): Section VII C Physical architecture; [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Translate one logical task into a declared optical/measurement pattern and verify its output contract.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-9"></span>

### 38.9 Photonic laboratory

**Core result / role:** Photonic acceptance protocol.

**Assumptions and scope:** Independent Fock-space reference and all detection branches.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Check photon-number truncation, probabilities, loss flags and conditional normalization.

**Imported earlier results:** [38.2](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-2), [38.3](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-3), [38.4](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-4), [38.7](../section-plans/physical-platforms.md#sec-photonic-encodings-optical-circuits-and-measurement-based-computation-7).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Report model assumptions, truncation if used, success probability and independent checks.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 39: Semiconductor Spin Qubits and Exchange-Based Architectures

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-1"></span>

### 39.1 Spin encodings and confined-charge models

**Core result / role:** Spin encoding in an effective charge/confinement model.

**Assumptions and scope:** Selected single-electron dot and two-site effective Hubbard model; retained orbital/valley states explicitly declared.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive the selected low-energy spin subspace and delimit ignored levels.

**Imported earlier results:** [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1).

**Exact source targets:** [SPIN:II](../references/proof-sources.md#source-spin-ii): Section II Basics of spin qubits; [SPIN:III.A](../references/proof-sources.md#source-spin-iii-a): Section III A Quantum confinement.

**Independent evidence target:** Identify the physical and computational subspaces of a tiny model.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-2"></span>

### 39.2 Zeeman control and electrically driven rotations

**Core result / role:** Zeeman and electrically driven spin rotations.

**Assumptions and scope:** Specified g tensor, field, spin-orbit approximation and frame.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive one effective drive Hamiltonian and its validity domain.

**Imported earlier results:** [39.1](../section-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-1), [34.3](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-3).

**Exact source targets:** [SPIN:III.D](../references/proof-sources.md#source-spin-iii-d): Section III D Zeeman interactions and spin-orbit coupling; [SPIN:V.A](../references/proof-sources.md#source-spin-v-a): Section V A Loss-DiVincenzo single spin qubits.

**Independent evidence target:** Compare time evolution with an independent qubit rotation.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-3"></span>

### 39.3 Exchange and entangling operations

**Core result / role:** Exchange from a two-site model.

**Assumptions and scope:** Declared Hubbard parameters and perturbative regime.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive superexchange and the resulting selected entangling operation.

**Imported earlier results:** [39.2](../section-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-2), [2.6](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-6).

**Exact source targets:** [SPIN:IV.A](../references/proof-sources.md#source-spin-iv-a): Section IV A Kinetic exchange in the Fermi-Hubbard hopping model.

**Independent evidence target:** Check a selected entangler and account for local phases.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-4"></span>

### 39.4 Charge, valley, and leakage degrees of freedom

**Core result / role:** Charge/valley levels create leakage channels.

**Assumptions and scope:** Explicit enlarged local Hilbert space.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Diagonalize a selected avoided crossing and derive projection/leakage effects.

**Imported earlier results:** [39.1](../section-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-1), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Exact source targets:** [SPIN:III.E](../references/proof-sources.md#source-spin-iii-e): Section III E Valleys.

**Independent evidence target:** Compare effective-qubit results with a converged small multilevel reference.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-5"></span>

### 39.5 Initialization and spin-to-charge readout

**Core result / role:** Spin-to-charge preparation/readout map.

**Assumptions and scope:** Specified blockade/tunneling and detection model.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive branch probabilities and the classical assignment matrix.

**Imported earlier results:** [39.1](../section-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-1), [34.4](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-4).

**Exact source targets:** [SPIN:IV.E](../references/proof-sources.md#source-spin-iv-e): Section IV E Pauli spin blockade; [SPIN:V.A](../references/proof-sources.md#source-spin-v-a): Section V A Loss-DiVincenzo single spin qubits.

**Independent evidence target:** Compare latent quantum outcomes and reported classical records.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-6"></span>

### 39.6 Noise, variability, and calibration

**Core result / role:** Selected spin-noise/filter-function model.

**Assumptions and scope:** Declared classical/stochastic noise and stationarity assumptions.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive one dephasing/filter response; delimit non-Markovian and operating-point dependence.

**Imported earlier results:** [39.3](../section-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-3), [28.2](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-2), [28.3](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-3).

**Exact source targets:** [SPIN:VI.A](../references/proof-sources.md#source-spin-vi-a): Section VI A Filter function formalism.

**Independent evidence target:** Study sensitivity and identify which parameters require measured input.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-7"></span>

### 39.7 Coupling, shuttling, and modular constraints

**Core result / role:** Exchange/shuttling/cavity links impose distinct constraints.

**Assumptions and scope:** Specified local/coupler architecture.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** State native operations, connectivity, transport and readout concurrency contracts.

**Imported earlier results:** [39.3](../section-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-3), [34.8](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-7).

**Exact source targets:** [SPIN:IV.F](../references/proof-sources.md#source-spin-iv-f): Section IV F Long-range couplers; [SPIN:VII](../references/proof-sources.md#source-spin-vii): Section VII Hybrid systems.

**Independent evidence target:** Build a small compilation contract with explicitly costed movement and scheduling.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-8"></span>

### 39.8 Spin-qubit laboratory

**Core result / role:** Spin-model acceptance protocol.

**Assumptions and scope:** Independent enlarged-space reference and perturbation sweep.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Check units, exchange sign, leakage, readout and omitted-level convergence.

**Imported earlier results:** [39.2](../section-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-2), [39.3](../section-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-3), [39.5](../section-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-5), [39.6](../section-plans/physical-platforms.md#sec-semiconductor-spin-qubits-and-exchange-based-architectures-6).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Verify one complete task independently and record the limits of the effective model.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 40: Topological Quantum Computation and Candidate Physical Realizations

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-1"></span>

### 40.1 Topology, protection, and distinct meanings

**Core result / role:** Topological protection is a model-dependent statement.

**Assumptions and scope:** Distinguish code, phase of matter and candidate device.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Define each meaning and explicitly separate theoretical protection from empirical realization; distinguish intrinsic phases, engineered defects, digitally prepared states and a protected computational architecture.

**Imported earlier results:** [7.1](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-1), [8.2](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2), [34.1](../section-plans/physical-platforms.md#sec-from-abstract-qubits-to-physical-quantum-systems-1).

**Exact source targets:** [ANYON:II.A](../references/proof-sources.md#source-anyon-ii-a): Section II A Non-Abelian Anyons; [N2020:braiding](../references/proof-sources.md#source-n2020-braiding): Abstract; Fig. 1–3; Extended Data Fig. 2; source data for Fig. 2–3; [G2023:braiding](../references/proof-sources.md#source-g2023-braiding): Braiding non-Abelian anyons; Fig. 3–4; Data availability.

**Independent evidence target:** Classify explicit claims and identify the mathematical versus experimental evidence needed.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-2"></span>

### 40.2 Fusion spaces and encoded information

**Core result / role:** Fusion rules determine encoded state-space dimension.

**Assumptions and scope:** Fibonacci fusion rule; four tau anyons in the total-vacuum sector.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Construct fusion trees and count compatible paths.

**Imported earlier results:** [40.1](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-1), [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1).

**Exact source targets:** [P9:9.12.2](../references/proof-sources.md#source-p9-9-12-2): Section 9.12.2 Fusion spaces.

**Independent evidence target:** Count a small fusion space and state the encoding assumptions.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-3"></span>

### 40.3 Fusion bases, F/R moves, and braiding

**Core result / role:** F/R basis transformations implement braiding.

**Assumptions and scope:** Fibonacci four-anyon encoding with explicitly consistent F/R data and gauge.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive a small braid matrix via basis changes and verify braid/unitarity relations.

**Imported earlier results:** [40.2](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-2), [2.3](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3).

**Exact source targets:** [P9:9.12.3](../references/proof-sources.md#source-p9-9-12-3): Section 9.12.3 Braiding: the R-matrix; [P9:9.12.4](../references/proof-sources.md#source-p9-9-12-4): Section 9.12.4 Associativity of fusion: the F-matrix; [P9:9.12.6](../references/proof-sources.md#source-p9-9-12-6): Section 9.12.6 Braiding in the standard basis: the B-matrix; [P9:9.14](../references/proof-sources.md#source-p9-9-14): Section 9.14 Fibonacci anyons.

**Independent evidence target:** Check algebraic consistency and compare ordered braid products.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local mathematical bridge to supply:** State the chosen Fibonacci F/R data and gauge as model input; verify the finite braid action without claiming to derive the anyon model from a microscopic material..

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-4"></span>

### 40.4 Measurement, corrections, and computational power

**Core result / role:** Fibonacci braiding universality with a deferred density proof; conditional fusion correctness.

**Assumptions and scope:** Specified anyon model, allowed measurements and ancillas.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Derive conditional fusion outcomes; state the selected universality/nonuniversality result and its deferred density argument; separate ideal Ising/Fibonacci computational power from what each processor experiment establishes.

**Imported earlier results:** [40.3](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-3), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2), [32.6](../section-plans/05-fault-tolerance.md#sec-fault-tolerant-gates-and-universal-logical-computation-6).

**Exact source targets:** [P9:9.14](../references/proof-sources.md#source-p9-9-14): Section 9.14 Fibonacci anyons; [P9:9.17](../references/proof-sources.md#source-p9-9-17): Section 9.17 Simulating a quantum circuit with Fibonacci anyons; [G2023:braiding](../references/proof-sources.md#source-g2023-braiding): Braiding non-Abelian anyons; Fig. 3–4; Data availability; [F2024:braiding](../references/proof-sources.md#source-f2024-braiding): Fig. 4; Methods: creation/fusion and braiding; Supplementary Section I.B referenced by the journal; Data and Code availability.

**Independent evidence target:** Verify a small logical operation without assuming braiding is universally sufficient.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local mathematical bridge to supply:** Fibonacci fusion basis, group closure/density and approximation accuracy.

**Explicitly deferred proof ingredients:** General density/universality proof and braid-approximation complexity; Preskill 9.17; finite fusion branches remain explicit.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-5"></span>

### 40.5 Majorana models and parity encoding [Advanced]

**Core result / role:** Majorana parity encoding and exchange representation.

**Assumptions and scope:** Four ideal Majorana modes with fixed total parity; effective algebra only.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive anticommutation, code dimension and braid action; no device-realization claim; distinguish ideal-chain parity algebra from finite-device readout and limited two-site protection.

**Imported earlier results:** [25.2](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-2), [25.3](../section-plans/04-variational.md#sec-variational-simulation-chemistry-and-ground-state-problems-3), [40.2](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-2).

**Exact source targets:** [ANYON:III.B](../references/proof-sources.md#source-anyon-iii-b): Section III B Superconductors with p+ip pairing symmetry; [MS2025:readout](../references/proof-sources.md#source-ms2025-readout): Main text qualification of MZM/Andreev interpretation; Fig. 3 experiment versus Fig. 4 simulation; Data availability; [KITREAD:readout](../references/proof-sources.md#source-kitread-readout): Abstract, main text and Fig. 3–4: capacitance parity readout and charge-sensing comparison.

**Independent evidence target:** Compare an exact finite model with claimed low-energy/parity behavior and finite-size limits.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-6"></span>

### 40.6 Protection assumptions and failure mechanisms

**Core result / role:** Protection requires locality, gaps and control assumptions.

**Assumptions and scope:** Declared perturbations, separation and noise model.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Give a scoped splitting/error argument and a failure example; avoid a universal immunity theorem; make the competing topological/trivial interpretations explicit and require scaling evidence for protection claims; Use D3–D8 to distinguish model-conditioned FDR, transport versus spectral/readout gaps, bias-symmetry assumptions and configuration changes; require quantitative model/measurement comparison before accepting a protection claim.

**Imported earlier results:** [40.1](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-1), [28.1](../section-plans/05-fault-tolerance.md#sec-noise-open-systems-and-error-mitigation-1), [29.5](../section-plans/05-fault-tolerance.md#sec-quantum-error-correction-conditions-and-recovery-5).

**Exact source targets:** [ANYON:IV.D](../references/proof-sources.md#source-anyon-iv-d): Section IV D Errors; [MS2025:readout](../references/proof-sources.md#source-ms2025-readout): Main text qualification of MZM/Andreev interpretation; Fig. 3 experiment versus Fig. 4 simulation; Data availability; [L2026:comment](../references/proof-sources.md#source-l2026-comment): Publisher opening argument; Fig. 1–2 titles; Data/Code availability; Change history; [MR2026:reply](../references/proof-sources.md#source-mr2026-reply): Publisher opening reply; Data availability; Change history; [DANON:symmetry](../references/proof-sources.md#source-danon-symmetry): Eq. (1)–(8), especially Eq. (7)–(8), and subgap/bias-independent-scattering assumptions; [MS2025SI:quasi](../references/proof-sources.md#source-ms2025si-quasi): Section S2.7, Eq. (S21)–(S24), Fig. S4: four-Majorana model and equilibration assumptions; [MS2025SI:configuration](../references/proof-sources.md#source-ms2025si-configuration): Sections S4.1–S4.4: tunnelling transport, lead isolation, tuning and cross-capacitance/hysteresis.

**Independent evidence target:** Perturb a tractable model and distinguish conditional robustness from immunity to all errors.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-7"></span>

### 40.7 Experiments, signatures, and unresolved evidence

**Core result / role:** Experimental signatures do not establish all topological operations.

**Assumptions and scope:** Dated claim-specific primary evidence.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Audit TOPO-01 through TOPO-09: Abelian FQH interference; encoded Ising defects, D4 and Fibonacci experiments; semiconductor parity readout; minimal Kitaev-chain readout; paired comment/reply and retraction. Separate measured observables, model attribution and missing protection/computational tests. Record dated source status and full-text access limits; no claim of independently reproducing experimental data; Compare version-specific public arguments using D1–D9. Separate acknowledged cropping from disputed ROI/SOI consequences, statistics from a single operating-point claim, and measured signals from topological inference. Attribute conflicting referee assessments rather than infer consensus.

**Imported earlier results:** [40.5](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-5), [40.6](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-6).

**Exact source targets:** [N2020:braiding](../references/proof-sources.md#source-n2020-braiding): Abstract; Fig. 1–3; Extended Data Fig. 2; source data for Fig. 2–3; [G2023:braiding](../references/proof-sources.md#source-g2023-braiding): Braiding non-Abelian anyons; Fig. 3–4; Data availability; [I2024:braiding](../references/proof-sources.md#source-i2024-braiding): Abstract; Fig. 3–6; Extended Data Fig. 5; Data and Code availability; [IONEXP:braiding](../references/proof-sources.md#source-ionexp-braiding): Main text and Fig. 4–6: fusion, Borromean braiding and torus sectors; [F2024:braiding](../references/proof-sources.md#source-f2024-braiding): Fig. 4; Methods: creation/fusion and braiding; Supplementary Section I.B referenced by the journal; Data and Code availability; [MS2025:readout](../references/proof-sources.md#source-ms2025-readout): Main text qualification of MZM/Andreev interpretation; Fig. 3 experiment versus Fig. 4 simulation; Data availability; [L2026:comment](../references/proof-sources.md#source-l2026-comment): Publisher opening argument; Fig. 1–2 titles; Data/Code availability; Change history; [MR2026:reply](../references/proof-sources.md#source-mr2026-reply): Publisher opening reply; Data availability; Change history; [K2026:readout](../references/proof-sources.md#source-k2026-readout): Abstract; Fig. 1–4 titles; Data and Code availability; [KITREAD:readout](../references/proof-sources.md#source-kitread-readout): Abstract, main text and Fig. 3–4: capacitance parity readout and charge-sensing comparison; [Z2018:status](../references/proof-sources.md#source-z2018-status): Publisher retraction banner and link to the 2021 Retraction Note; [ZR2021:notice](../references/proof-sources.md#source-zr2021-notice): Retraction notice; reanalysis and data repository; [LEGGPRE:argument](../references/proof-sources.md#source-leggpre-argument): Sections I–III, Fig. 1–6 and conclusions; early comment; [MSPRE:statistics](../references/proof-sources.md#source-mspre-statistics): Introduction and Technical response to Ref. 3; Tables I–II, Fig. 1–4; FDR conditioning and ensemble assumptions; [MSPRE:readout](../references/proof-sources.md#source-mspre-readout): Technical response to Ref. 4; bias-cropping admission, conductance interpretation, Fig. 5, Discussion; [LEGGAAM:argument](../references/proof-sources.md#source-leggaam-argument): Main text lines 14–126; coding artefacts, transport interpretation and scope limitation; [LEGGAAM:figures](../references/proof-sources.md#source-leggaam-figures): Fig. 1–2 and extended-data captions; figure files and parameter labels; [LEGNOTES:protocol](../references/proof-sources.md#source-legnotes-protocol): Supplemental Note 1, Fig. S1–S3 and code excerpt: parameter dependence, displayed clusters, bias coordinates; [LEGNOTES:symmetry](../references/proof-sources.md#source-legnotes-symmetry): Supplemental Note 2, Eq. (S1), Fig. S4–S7: claimed symmetry deviations and negative conductance; [TPREVIEW:referees](../references/proof-sources.md#source-tpreview-referees): Anonymous Referees 1–3, versions 0/1 for both submissions; distinct and changing assessments; [TPREVIEW:legg](../references/proof-sources.md#source-tpreview-legg): Legg response to referees, clarifications and claimed modifications; appendix; [TPREVIEW:revised-assessments](../references/proof-sources.md#source-tpreview-revised-assessments): Anonymous Referees 1–3, reply version 1; no unanimous verdict; [TPREVIEW:microsoft](../references/proof-sources.md#source-tpreview-microsoft): Microsoft response to referees: existing ROI2s, one-pixel shift, controls and configuration change; [DANON:symmetry](../references/proof-sources.md#source-danon-symmetry): Eq. (1)–(8), especially Eq. (7)–(8), and subgap/bias-independent-scattering assumptions.

**Independent evidence target:** Follow TOPO-01–09 and dispute cases D1–D9. Full accepted comment, 2025 response, published supplement and joint author/reviewer record are checked. Exact final-reply matching, versioned raw/corrected data reproduction and specialist interpretation remain pending.

**Planning budget:** 2–4 pages. **Review status:** full-public-argument-corpus-reviewed; exact-final-journal-reply-comparison-and-device-reanalysis-open; mathematical and implementation review remain separate.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-8"></span>

### 40.8 Topological compilation and laboratory

**Core result / role:** Topological compilation acceptance protocol.

**Assumptions and scope:** Specified anyon model and target accuracy.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Compare braid matrices to dense logical targets and record approximation/measurement costs; label ideal braid-matrix calculations as a synthetic model laboratory; obtain data/code versions before planning an experimental reanalysis.

**Imported earlier results:** [40.3](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-3), [40.4](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-4), [40.6](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-6), [40.7](../section-plans/physical-platforms.md#sec-topological-quantum-computation-and-candidate-physical-realizations-7).

**Exact source targets:** [P9:9.17](../references/proof-sources.md#source-p9-9-17): Section 9.17 Simulating a quantum circuit with Fibonacci anyons; [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence; [F2024:braiding](../references/proof-sources.md#source-f2024-braiding): Fig. 4; Methods: creation/fusion and braiding; Supplementary Section I.B referenced by the journal; Data and Code availability; [I2024:braiding](../references/proof-sources.md#source-i2024-braiding): Abstract; Fig. 3–6; Extended Data Fig. 5; Data and Code availability.

**Independent evidence target:** Verify a toy encoded operation and its resource/error assumptions; state that it is not a hardware reproduction.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.
