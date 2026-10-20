# Part 6. Physical Realizations and Quantum-System Architecture

**Detailed plan · 2026-10-20 · Planned material; architecture review pending.** [All sections](../section-plan.md) · [Full plan](../book-plan.md) · [Reader continuity](../reader-continuity.md)

Each section specifies its argument and independent evidence. Framework implementation, mathematical review and reader review have separate status. Closing materials follow the [section-plan guide](../section-plan.md#how-to-read-the-specification).

<span id="ch-from-abstract-qubits-to-physical-quantum-systems"></span>

## Chapter 34

**From Abstract Qubits to Physical Quantum Systems**

**Reading level:** Core bridge with optional physics extensions. **Chapter prerequisites:** 2–6, 8–10, 19, 28; selected 29–33 for logical resources.

**Branch design:** use this common bridge, choose one of Chapters 35–40, then proceed to compilation. Other platforms can be compared through their guided summaries.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-1"></span>

### 34.1 Levels, modes, and computational subspaces

**Learning and derivation target:** Define the physical Hilbert space, encoded qubit and leakage states; state the effective-model assumptions.

**Implementation and evidence target:** Compare a two-level approximation with a small multilevel model and quantify leakage.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-2"></span>

### 34.2 Oscillator and light-matter mathematics bridge

**Learning and derivation target:** Introduce ladder operators, Fock states and one interaction model before platform-specific use; explain truncation boundaries.

**Implementation and evidence target:** Check low-energy calculations while showing why finite truncations cannot satisfy the full oscillator commutator exactly.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-3"></span>

### 34.3 Driven systems, rotating frames, and resonance

**Learning and derivation target:** Derive a driven two-level model, a rotating-frame transformation and a scoped rotating-wave approximation.

**Implementation and evidence target:** Compare lab-frame and effective evolutions with consistent state/observable transformations.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-4"></span>

### 34.4 Preparation, control, and readout as an experiment

**Learning and derivation target:** Connect calibrated control parameters and a measurement record to the abstract operations.

**Implementation and evidence target:** Build a complete small prepare-control-readout model with units and probability normalization.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-5"></span>

### 34.5 Digital, analog, and measurement-based models

**Learning and derivation target:** Distinguish gate sequences, Hamiltonian schedules and adaptive resource-state measurements; connect to 19.8 and the graph-state bridge in Chapter 30.

**Implementation and evidence target:** Compare precisely specified tasks and requested outputs rather than treating the models as interchangeable.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-6"></span>

### 34.6 Noise, leakage, loss, and hardware constraints

**Learning and derivation target:** Relate relaxation, dephasing, leakage and heralded erasure to architecture-specific models.

**Implementation and evidence target:** Check explicit channels and explain why equal quoted fidelities need not imply equal workload behavior.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-7"></span>

### 34.7 Connectivity, transport, and modular architectures

**Learning and derivation target:** Define interaction graphs, movable qubits, optical links and simultaneous-operation constraints.

**Implementation and evidence target:** Construct explicit target descriptions and identify which constraints a compiler must preserve.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-8"></span>

### 34.8 A fair platform-comparison framework

**Learning and derivation target:** Specify encoding, native entangler, readout, control, dominant errors and full resource assumptions.

**Implementation and evidence target:** Compare dated primary-source evidence; distinguish proposals, demonstrations and scalable-system projections.

<span id="sec-from-abstract-qubits-to-physical-quantum-systems-9"></span>

### 34.9 Choose a platform learning branch

**Learning and derivation target:** Provide a prerequisite checklist and a common model-control-measurement worksheet for Chapters 35–40.

**Implementation and evidence target:** Complete one branch before Chapters 41–43; do not require sequential mastery of all platform specialties.

<span id="ch-superconducting-qubits-and-circuit-qed-control"></span>

## Chapter 35

**Superconducting Qubits and Circuit-QED Control**

**Reading level:** Advanced platform branch. **Chapter prerequisites:** 2–6, 9, 19, 28, 34.

<span id="sec-superconducting-qubits-and-circuit-qed-control-1"></span>

### 35.1 An electrical circuit becomes a quantum model

**Learning and derivation target:** Introduce circuit coordinates and the effective Josephson model with a local classical-circuit bridge; identify assumptions rather than requiring unexplained BCS theory.

**Implementation and evidence target:** Derive a small effective Hamiltonian with explicit energy/frequency units.

<span id="sec-superconducting-qubits-and-circuit-qed-control-2"></span>

### 35.2 Anharmonicity and the transmon computational subspace

**Learning and derivation target:** Derive a scoped low-energy spectrum and explain why anharmonicity supports selective qubit control.

**Implementation and evidence target:** Compare truncated diagonalization and a justified approximation; quantify convergence.

<span id="sec-superconducting-qubits-and-circuit-qed-control-3"></span>

### 35.3 Microwave control and single-qubit rotations

**Learning and derivation target:** Derive drive phase/amplitude dependence in a declared rotating frame.

**Implementation and evidence target:** Compare controlled evolution with the target qubit rotation including leakage.

<span id="sec-superconducting-qubits-and-circuit-qed-control-4"></span>

### 35.4 Coupling and native two-qubit interactions

**Learning and derivation target:** Derive one representative exchange or conditional-phase gate and compare other native families at an explicit model level.

**Implementation and evidence target:** Check the projected two-qubit action and leakage with a multilevel reference.

<span id="sec-superconducting-qubits-and-circuit-qed-control-5"></span>

### 35.5 Dispersive readout and assignment errors

**Learning and derivation target:** Develop a scoped resonator/readout model and distinguish measurement backaction from classical classification error.

**Implementation and evidence target:** Check outcome statistics and a separate assignment-error model.

<span id="sec-superconducting-qubits-and-circuit-qed-control-6"></span>

### 35.6 Decoherence, crosstalk, and calibration

**Learning and derivation target:** Connect relaxation/dephasing and spectator interactions to a complete experiment.

**Implementation and evidence target:** Compare ideal and imperfect gates with dated calibration inputs and declared model limits.

<span id="sec-superconducting-qubits-and-circuit-qed-control-7"></span>

### 35.7 Target constraints for compilation

**Learning and derivation target:** Specify native gates, coupling, frequency/simultaneity restrictions and frame updates.

**Implementation and evidence target:** Create a small target contract consumed by the compilation laboratories without claiming a provider integration.

<span id="sec-superconducting-qubits-and-circuit-qed-control-8"></span>

### 35.8 Superconducting-model laboratory

**Learning and derivation target:** Integrate spectrum, drive, entangler and readout and state the boundary of the effective model.

**Implementation and evidence target:** Verify one complete experiment independently and report truncation, control and measurement error.

<span id="ch-trapped-ion-qubits-motional-gates-and-transport"></span>

## Chapter 36

**Trapped-Ion Qubits, Motional Gates, and Transport**

**Reading level:** Advanced platform branch. **Chapter prerequisites:** 2–6, 9, 19, 28, 34.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-1"></span>

### 36.1 Internal states, trapping, and preparation

**Learning and derivation target:** Specify a qubit encoding and explain trapping and cooling with a local physics bridge.

**Implementation and evidence target:** Record the effective levels, preparation assumptions and discarded degrees of freedom.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-2"></span>

### 36.2 Collective motion and sidebands

**Learning and derivation target:** Derive a scoped ion-motion coupling and define the Lamb-Dicke/resolved-sideband approximations before use.

**Implementation and evidence target:** Compare low-occupation dynamics with converged oscillator truncations.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-3"></span>

### 36.3 Carrier drives and single-qubit control

**Learning and derivation target:** Derive a representative laser/microwave-driven rotation and frame convention.

**Implementation and evidence target:** Compare control-model and abstract-gate predictions.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-4"></span>

### 36.4 Motional entangling gates

**Learning and derivation target:** Derive one Mølmer-Sørensen or geometric-phase construction including a motion-return condition.

**Implementation and evidence target:** Compare joint spin-motion evolution and the reduced spin gate for several motional inputs.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-5"></span>

### 36.5 Readout, heating, and coherence

**Learning and derivation target:** Distinguish fluorescence assignment, spontaneous processes and motional heating.

**Implementation and evidence target:** Test a complete model and state which omitted effects limit the approximation.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-6"></span>

### 36.6 Chains, QCCD transport, and photonic links

**Learning and derivation target:** Distinguish a chosen interaction model from transport/cooling/zone or modular-network overhead.

**Implementation and evidence target:** Model a tiny transport/operation schedule rather than assuming cost-free all-to-all execution.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-7"></span>

### 36.7 Target constraints for compilation

**Learning and derivation target:** Specify native entanglers, shared modes, zones, simultaneous operations and timing.

**Implementation and evidence target:** Create a target description and compare two schedules for the same declared architecture.

<span id="sec-trapped-ion-qubits-motional-gates-and-transport-8"></span>

### 36.8 Trapped-ion laboratory

**Learning and derivation target:** Integrate internal-state control, motion, entanglement and readout.

**Implementation and evidence target:** Verify a gate and its thermal/truncation sensitivity with an independent reference and resource record.

<span id="ch-neutral-atom-arrays-and-rydberg-quantum-computing"></span>

## Chapter 37

**Neutral-Atom Arrays and Rydberg Quantum Computing**

**Reading level:** Advanced platform branch. **Chapter prerequisites:** 2–6, 9, 19, 28, 34.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-1"></span>

### 37.1 Trapping, internal encodings, and rearrangement

**Learning and derivation target:** Specify the computational states, optical-trap model and classical atom-position controls.

**Implementation and evidence target:** Build an explicit geometry and distinguish moving atoms from a logical SWAP.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-2"></span>

### 37.2 Rydberg interactions and blockade

**Learning and derivation target:** Derive a two-atom effective Hamiltonian and the assumptions of the blockade approximation.

**Implementation and evidence target:** Compare finite-interaction dynamics with the ideal blockade limit.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-3"></span>

### 37.3 Single-qubit and entangling control

**Learning and derivation target:** Derive one gate sequence and identify phases, leakage and interaction constraints.

**Implementation and evidence target:** Compare the gate with an independent two-/multilevel reference.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-4"></span>

### 37.4 Analog Hamiltonian programming

**Learning and derivation target:** Translate geometry, detuning and drive schedules into a declared many-body Hamiltonian.

**Implementation and evidence target:** Compare a small schedule with exact evolution without assuming arbitrary graph programmability.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-5"></span>

### 37.5 Transport, parallelism, and compilation

**Learning and derivation target:** Model motion, blockade neighborhoods and simultaneous gate restrictions.

**Implementation and evidence target:** Compare two explicitly feasible arrangements/schedules and account for transport cost.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-6"></span>

### 37.6 Atom loss, readout, and imperfect interactions

**Learning and derivation target:** Distinguish loss/erasure information, computational error and readout assignment.

**Implementation and evidence target:** Check model-specific outcome records and their treatment in a later correction workflow.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-7"></span>

### 37.7 Digital versus analog experiment contracts

**Learning and derivation target:** Specify inputs, admissible controls, outputs and error metrics for each mode.

**Implementation and evidence target:** Verify one digital and one analog small task with matched mathematical references.

<span id="sec-neutral-atom-arrays-and-rydberg-quantum-computing-8"></span>

### 37.8 Neutral-atom laboratory

**Learning and derivation target:** Connect geometry, Hamiltonian/control, noise and requested observable.

**Implementation and evidence target:** Record all constraints and compare independent dynamics before a hardware-access extension.

<span id="ch-photonic-encodings-optical-circuits-and-measurement-based-computation"></span>

## Chapter 38

**Photonic Encodings, Optical Circuits, and Measurement-Based Computation**

**Reading level:** Advanced platform branch. **Chapter prerequisites:** 2–10, 28, 30, 34.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-1"></span>

### 38.1 Optical modes and qubit encodings

**Learning and derivation target:** Introduce Fock states and polarization/path/time encodings; distinguish physical modes from encoded qubits.

**Implementation and evidence target:** Check the encoding isometry and the dimensions of a small optical model.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-2"></span>

### 38.2 Beam splitters, phases, and interferometers

**Learning and derivation target:** Derive mode transformations and their action on selected photon-number states.

**Implementation and evidence target:** Compare mode-unitary and Fock-space calculations with declared phase conventions.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-3"></span>

### 38.3 Interference, sources, and detection

**Learning and derivation target:** Derive a two-photon interference example and state indistinguishability/detector assumptions.

**Implementation and evidence target:** Compare ideal probabilities with loss or distinguishability perturbations.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-4"></span>

### 38.4 Measurement-induced operations and heralding

**Learning and derivation target:** Derive a scoped conditional optical operation, its success probability and classical feed-forward.

**Implementation and evidence target:** Check all accepted/rejected branches; do not treat passive optics as deterministic universal qubit gates.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-5"></span>

### 38.5 Graph states, fusion, and logical computation

**Learning and derivation target:** Use Chapter 30's measurement-based bridge to analyze one resource-state/fusion operation.

**Implementation and evidence target:** Verify stabilizer updates, logical corrections and failed-fusion outcomes on a tiny instance.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-6"></span>

### 38.6 Continuous-variable and bosonic branches [Advanced]

**Learning and derivation target:** Introduce quadratures, squeezing and Gaussian/non-Gaussian distinctions through a local mathematics bridge.

**Implementation and evidence target:** Compare a tractable Gaussian calculation or converged truncated-state model without equating a mode with a qubit.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-7"></span>

### 38.7 Loss, erasure, and multiplexing resources

**Learning and derivation target:** Separate transmission/detection loss, heralding and resource-state generation cost.

**Implementation and evidence target:** Compute accepted logical-output probability with explicit discarded attempts.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-8"></span>

### 38.8 Photonic compilation and architecture contracts

**Learning and derivation target:** Specify interferometers, resource states, timing, detection and feed-forward targets.

**Implementation and evidence target:** Translate one logical task into a declared optical/measurement pattern and verify its output contract.

<span id="sec-photonic-encodings-optical-circuits-and-measurement-based-computation-9"></span>

### 38.9 Photonic laboratory

**Learning and derivation target:** Connect encoding, optical transformations, conditional detection and resource accounting.

**Implementation and evidence target:** Report model assumptions, truncation if used, success probability and independent checks.

<span id="ch-semiconductor-spin-qubits-and-exchange-based-architectures"></span>

## Chapter 39

**Semiconductor Spin Qubits and Exchange-Based Architectures**

**Reading level:** Advanced platform branch. **Chapter prerequisites:** 2–6, 9, 19, 28, 34.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-1"></span>

### 39.1 Spin encodings and confined-charge models

**Learning and derivation target:** Introduce single-spin, encoded-spin and donor/dot choices with explicit effective assumptions.

**Implementation and evidence target:** Identify the physical and computational subspaces of a tiny model.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-2"></span>

### 39.2 Zeeman control and electrically driven rotations

**Learning and derivation target:** Derive a scoped spin-control Hamiltonian and resonance convention.

**Implementation and evidence target:** Compare time evolution with an independent qubit rotation.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-3"></span>

### 39.3 Exchange and entangling operations

**Learning and derivation target:** Derive a two-spin exchange evolution and its computational action.

**Implementation and evidence target:** Check a selected entangler and account for local phases.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-4"></span>

### 39.4 Charge, valley, and leakage degrees of freedom

**Learning and derivation target:** Explain which extra levels a selected semiconductor model includes and when they matter.

**Implementation and evidence target:** Compare effective-qubit results with a converged small multilevel reference.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-5"></span>

### 39.5 Initialization and spin-to-charge readout

**Learning and derivation target:** Derive a scoped state-preparation/readout process and distinguish its errors.

**Implementation and evidence target:** Compare latent quantum outcomes and reported classical records.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-6"></span>

### 39.6 Noise, variability, and calibration

**Learning and derivation target:** Model a selected charge/hyperfine/control perturbation without universal platform claims.

**Implementation and evidence target:** Study sensitivity and identify which parameters require measured input.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-7"></span>

### 39.7 Coupling, shuttling, and modular constraints

**Learning and derivation target:** Specify a target's couplings, transport/control resources and timing.

**Implementation and evidence target:** Build a small compilation contract with explicitly costed movement and scheduling.

<span id="sec-semiconductor-spin-qubits-and-exchange-based-architectures-8"></span>

### 39.8 Spin-qubit laboratory

**Learning and derivation target:** Integrate encoding, exchange/control, readout and imperfections.

**Implementation and evidence target:** Verify one complete task independently and record the limits of the effective model.

<span id="ch-topological-quantum-computation-and-candidate-physical-realizations"></span>

## Chapter 40

**Topological Quantum Computation and Candidate Physical Realizations**

**Reading level:** Advanced platform branch. **Chapter prerequisites:** 7–9, 25, 28–32, 34.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-1"></span>

### 40.1 Topology, protection, and distinct meanings

**Learning and derivation target:** Distinguish topological order, topological codes and a physical non-Abelian-quasiparticle proposal.

**Implementation and evidence target:** Classify explicit claims and identify the mathematical versus experimental evidence needed.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-2"></span>

### 40.2 Fusion spaces and encoded information

**Learning and derivation target:** Introduce charge sectors and fusion rules before using their notation.

**Implementation and evidence target:** Count a small fusion space and state the encoding assumptions.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-3"></span>

### 40.3 Fusion bases, F/R moves, and braiding

**Learning and derivation target:** Define fusion-basis recoupling and exchange matrices before use; derive one specified braid representation and state its consistency conditions and proof scope.

**Implementation and evidence target:** Check algebraic consistency and compare ordered braid products.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-4"></span>

### 40.4 Measurement, corrections, and computational power

**Learning and derivation target:** Explain a selected model's measurements, available gates and extra resources needed for universality.

**Implementation and evidence target:** Verify a small logical operation without assuming braiding is universally sufficient.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-5"></span>

### 40.5 Majorana models and parity encoding [Advanced]

**Learning and derivation target:** Introduce a scoped fermionic toy Hamiltonian and parity constraints using the Chapter 25 bridge.

**Implementation and evidence target:** Compare an exact finite model with claimed low-energy/parity behavior and finite-size limits.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-6"></span>

### 40.6 Protection assumptions and failure mechanisms

**Learning and derivation target:** Explain gap, locality, poisoning, finite size and readout assumptions of a selected model.

**Implementation and evidence target:** Perturb a tractable model and distinguish conditional robustness from immunity to all errors.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-7"></span>

### 40.7 Experiments, signatures, and unresolved evidence

**Learning and derivation target:** Separate proposed signatures, alternative explanations, demonstrated control and full logical computation.

**Implementation and evidence target:** Build a dated primary-source claim/evidence table without inferring a working universal platform from one signature.

<span id="sec-topological-quantum-computation-and-candidate-physical-realizations-8"></span>

### 40.8 Topological compilation and laboratory

**Learning and derivation target:** Specify allowed braids/measurements, corrections and non-topological supplements.

**Implementation and evidence target:** Verify a toy encoded operation and its resource/error assumptions; state that it is not a hardware reproduction.
