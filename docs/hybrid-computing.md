# Quantum-classical hybrid computing: patterns, contracts, and learning routes

**Curriculum and implementation-design map · October 20, 2026.** Hybrid computation already appears in the variational, learning and dynamic-program chapters, but those topics need a connected account. This map supplies it without adding or renumbering chapters.

The eight patterns below are an **editorial taxonomy**, not an exhaustive or mutually exclusive standard. The first seven describe algorithm/data coupling; the eighth describes execution architecture and can support the others. A workflow can combine several patterns. A classical computer controlling a QPU does not by itself establish useful acceleration.

## Start with the execution boundary

Ask what classical computation does, what the quantum operation returns, where the next decision runs and whether a quantum state must remain available during that decision.

| Boundary | Typical implementation | Essential contract |
|---|---|---|
| Between independently prepared quantum executions | Host process prepares inputs, invokes jobs and processes results | Parameters, observables/shots, result schema, uncertainty, retries and reproducibility |
| During a quantum execution | A supported local controller processes measurement records and changes subsequent operations or frames | Supported expressions, branch semantics, timing, latency and state lifetime |
| Across an application workflow | A task runtime coordinates CPU, GPU, quantum resources and storage | Dependencies, batching, scheduling, payloads, failure recovery and total resource cost |

A simulator may expose an entire statevector and support backpropagation through it. Physical execution supplies measured classical records or estimates; a production algorithm cannot assume that amplitudes or exact simulator gradients are returned. A GPU simulating a circuit is classical computation. Registering a QPU as an accelerator does not make its latency, data model or execution semantics identical to a GPU's.

## Eight composable patterns

| Pattern | Classical responsibility | Quantum responsibility | Main curriculum homes |
|---|---|---|---|
| 1. Subroutine pipeline | Prepare input, call a quantum routine, interpret output | Supply samples, estimated phases or other declared observations | 14–22 |
| 2. Variational outer loop | Build an objective, estimate/update parameters, decide convergence | Evaluate a parameterized experiment and required estimators | 23–26, 49 |
| 3. Hybrid learning and feature methods | Preprocess data, train/read a predictor, evaluate generalization | Supply trainable features or estimated kernels | 23–24, 27 |
| 4. In-execution adaptive feedback | Locally evaluate outcomes, corrections or decoder/frame updates | Measure and continue conditional quantum operations | 6–7, 29–32, 41, 43 |
| 5. Measurement-driven inference | Reconstruct properties, infer models or form estimators | Prepare states and collect chosen measurement records | 6, 10, 28 |
| 6. Circuit decomposition and reconstruction | Choose cuts/settings and combine weighted fragment results | Execute smaller fragment experiments | 47 |
| 7. Embedded/self-consistent solvers | Build an environment/subproblem, update a consistency model | Solve a selected embedded quantum problem and estimate observables | 25 |
| 8. Heterogeneous workflows | Orchestrate tasks, data, classical solves, batching and recovery | Execute the quantum tasks supported by the workflow | 43, 48–50 |

The arrows below specify data/control flow. They are not invented FlagQuantum API calls or claims of current backend support.

### 1. A quantum subroutine in a classical pipeline

**Flow:** classical input/problem reduction → quantum routine → measured record → classical interpretation.

A factoring example uses classical arithmetic and candidate checks around quantum order finding. An estimation application may submit prepared inputs and convert samples into an answer. The host needs an explicit circuit/problem specification, output schema and success/error criterion; it need not optimize parameters.

**Implementation target:** construct and validate the quantum input, invoke the declared executor, retain raw/aggregated records, and run deterministic or statistical classical postprocessing. Separate a single execution from repetitions needed for success.

**Independent check:** exhaustive arithmetic or an exact small distribution, including failed candidate recovery. **Cost:** state/oracle preparation, all executions, communication and readout, plus classical postprocessing. Chapter 14.7 introduces this pattern; Chapters 17–18 develop a concrete algorithmic instance.

### 2. A variational optimization loop

**Flow:** parameters → quantum expectations/gradient experiments → classical objective/update → new parameters.

For a Pauli objective, derive $E(\theta)=\sum_j c_j\langle P_j\rangle_\theta$ and state how each estimate and its uncertainty enter the update. The loop can use gradients, finite differences, parameter shift or a derivative-free strategy; these have different call and shot budgets.

**Implementation target:** keep optimizer state on the host, bind parameter batches, collect named expectation estimates, form the loss, update parameters and checkpoint the complete state. On supported simulators, autograd can provide derivatives; hardware requires an explicit executable derivative/estimator strategy. Backpropagation through simulated amplitudes is not a hardware measurement procedure.

**Independent check:** a small analytic landscape or exact diagonalization, gradient identities and post-update loss records. **Cost:** objective/gradient evaluations, settings and shots per evaluation, queue/transfer time and optimizer steps.

The repository's [training program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/omalley2016/train_h2_vqe.py) and [gradient program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/gradients.py) are existing small examples, within their pinned ideal-simulation scope.

### 3. Hybrid learning: trainable layers, fixed features, and kernels

**Trainable flow:** classical network → data-dependent quantum circuit → estimated features → classical output head/loss → joint parameter updates.

Derive the chain rule, shapes and parameter occurrences across every boundary. The quantum layer must return the derivatives or Jacobian-vector/vector-Jacobian information required by the selected training scheme, using an appropriate simulator or hardware estimator.

**Feature/kernel flow:** data pairs or samples → quantum feature/kernel experiments → classical predictor training. A fixed quantum kernel can be estimated before training a classical kernel model; ordinary classical fitting then does not require quantum-layer backpropagation. A trainable kernel adds its own parameter-update loop.

**Implementation target:** define feature arrays or pairwise kernel queries, batching and measurement budgets. For trainable layers, connect an explicit differentiable contract to the classical framework. For fixed kernels, preserve the estimated Gram matrix and noise/regularization record.

**Independent check:** tiny explicit feature vectors, finite-difference/analytic derivative checks where applicable, and held-out classical baselines. **Cost:** data encoding, pairwise kernel query growth, measurements, training and inference. Finite-shot kernel estimates may lose positive semidefiniteness; document any repair and its effect.

### 4. In-execution adaptive feedback

**Flow:** partial measurement → supported local classical decision → conditional gate/reset/measurement or frame update → continued execution.

Teleportation corrections, active reset and a scoped syndrome-decoding workflow illustrate this boundary. Derive the conditional states/maps and classical records; averaging away records too early can destroy the intended program meaning.

**Implementation target:** represent measurement records, branches and dependencies in a dynamic program; lower supported expressions to a controller with a declared latency budget. A decoder may produce a tracked Pauli-frame update instead of an immediate physical correction. Verify which operation the program actually requests.

**Independent check:** enumerate small branches, conditional probabilities and corrected logical outputs; validate scheduling/feedback constraints. **Cost:** measurement, classical decision/decoding and communication latency relative to the relevant state lifetime.

A host job that finishes and later prepares a new circuit is a different execution contract. Remote Python callbacks cannot be assumed to preserve the required in-execution state or timing.

### 5. Measurement-driven inference and estimation

**Flow:** measurement design → quantum records → classical estimator/reconstruction → property or model.

Tomography, classical-shadow property prediction and selected mitigation/calibration methods place substantial computation after measurement. An adaptive version can feed an inferred model into the next independently prepared experiment.

**Implementation target:** specify measurement ensemble/bases, raw versus aggregated record needs, estimator, confidence criterion and model assumptions. Fit or reconstruct on CPU/GPU, retaining the provenance of any correction or regularization.

**Independent check:** a known small state/channel, repeated-trial uncertainty and a counterexample showing what the chosen measurements cannot identify. **Cost:** samples, settings, inverse/reconstruction complexity and any bias/variance overhead. A reconstructed matrix or error-mitigated estimate is not an unqualified observation of the exact physical state.

### 6. Circuit decomposition and classical reconstruction

**Flow:** original circuit and requested observable → weighted fragment experiments → classical reconstruction.

Derive a chosen decomposition, including signed coefficients, preparations, measurement settings and the output being reconstructed. Schematically, a scalar result can have the form $y=\sum_\alpha w_\alpha g_\alpha$, where each $g_\alpha$ is defined by the selected fragment scheme. The exact form and correlations must be derived, not assumed.

**Implementation target:** build a fragment/settings manifest, execute each required experiment, and combine results with the correct coefficients and covariance/uncertainty treatment. This reconstructs a declared output; it does not mean a larger coherent state has physically existed on the smaller device.

**Independent check:** exact agreement with a small uncut reference before sampling/noise, then repeated stochastic reconstruction tests. **Cost:** fragment count, setting count, signed-weight sampling overhead, shots and classical aggregation. Required resources can grow rapidly with cuts and correlations, so fewer simultaneous qubits is not a free benefit.

### 7. Embedded and self-consistent quantum solvers

**Flow:** classical global/environment model → embedded Hamiltonian → quantum subproblem solver → reduced observables → classical environment update.

A scoped embedding example uses a quantum solver for a fragment/impurity while the classical calculation represents an environment. Derive the effective model and consistency condition before running a nested loop. Density-matrix embedding itself is not inherently a QPU algorithm; the quantum/classical variant must explicitly choose a quantum subproblem solver.

**Implementation target:** build the model and basis transformations classically, specify the quantum solver contract, estimate the required reduced observables, and update declared environment parameters. The inner solver may itself be VQE, creating two distinct convergence/error loops.

**Independent check:** compare the embedded model and outer iteration with exact tiny-instance fragment/global references. Separate embedding approximation, solver optimization, sampling and self-consistency errors. **Cost:** all inner and outer evaluations and classical environment work; a converged residual alone does not certify the global physical answer.

A related, separately derived method uses quantum-generated configurations followed by classical projected-subspace diagonalization. This is neither automatically VQE nor equivalent to self-consistent embedding. Chapter 25 gives it a distinct section and states the precise assumptions of any variational bound.

### 8. CPU/GPU/QPU workflow integration

**Flow:** application task graph → resource-specific tasks → typed results and dependencies → aggregate/update/checkpoint.

CPU tasks may prepare Hamiltonians or coordinate optimizers; GPU tasks may perform classical simulation, inference, training or numerical solves; QPU tasks prepare/measure quantum systems. This execution architecture can host any of the patterns above and does not imply that every workflow needs all three resource types.

**Implementation target:** define task dependencies and result schemas, batch parameter/measurement requests, use asynchronous calls where semantics permit, and checkpoint optimizer/solver/configuration state. Record retries, stale results and data provenance. Keep the low-latency controller loop inside its supported execution boundary rather than hiding it behind a remote task queue.

**Independent check:** replace quantum calls with a tractable exact reference to test the workflow contract, then validate supported device execution separately. Benchmark end-to-end time under matched accuracy, including queueing, transfers, shots, classical solves and failure recovery. Do not call GPU simulation a physical quantum run.

## Related labels describe different axes

- **Digital-analog quantum computing** combines gate-like and Hamiltonian-evolution primitives. Its classical/quantum data flow must still be specified; it is not a synonym for a host optimization loop.
- **Distributed quantum computing** may require entanglement and coherent interconnects. Distributing independent fragment jobs or CPU/GPU tasks does not supply that quantum communication resource.
- **Quantum-inspired classical algorithms** can be important baselines, but a GPU-only numerical computation is not physical QPU execution.
- **Calibration feedback** may run between separately prepared experiments or within a supported local-control loop. State the timing/state-lifetime contract instead of inferring it from the word feedback.

## A common implementation worksheet

For each example record:

1. **Task and mathematical objective:** input, output, access model and required accuracy.
2. **Classical/quantum partition:** each operation's responsibility and the exchanged classical payload.
3. **Quantum-state lifetime:** whether every call starts a new preparation or whether a controller decision occurs during an execution.
4. **Derivatives and statistics:** what is exact, sampled, differentiated, reconstructed or approximated.
5. **Runtime:** host, local controller, CPU/GPU tasks, QPU/simulator calls, concurrency, retries and checkpoints.
6. **Cost and comparison:** all invocations, settings/shots, classical work, memory and end-to-end latency; a matched classical baseline.
7. **Independent evidence:** a small exact reference, limiting case, error budget and a transfer/failure example.
8. **Implementation status:** audited version, complete program, executed environment and confirmed upstream gap when applicable.

For a sequential host-driven workflow, one bookkeeping model is

$$
T_{\mathrm{total}}=T_{\mathrm{init}}+
\sum_{k=1}^{K}
\left(T_{\mathrm{host},k}+T_{\mathrm{queue},k}
+T_{\mathrm{transfer},k}+T_{\mathrm{device},k}\right)
+T_{\mathrm{final}}.
$$

Define disjoint timing boundaries: device time here includes its measurement and local-control execution. Overlapping/asynchronous workflows require critical-path and throughput analysis rather than blindly adding overlapping intervals.

## Integration in the textbook

- **14.7:** early taxonomy and explicit host/controller/device boundary.
- **10:** inference, tomography and property estimation.
- **23–24:** differentiation, exact/stochastic optimization and execution cost.
- **25:** embedding, nested self-consistency, and sampled-configuration classical solving.
- **26–27:** optimization and learning implementations, including the difference between fixed kernels and trainable layers.
- **41–43:** program semantics, local adaptive feedback and heterogeneous workflow contracts.
- **47:** cutting/reconstruction identities, statistical overhead and independent uncut references.
- **48–50:** provenance, complete resource/timing records and research-case validation.

This is a connected planning/implementation guide. Existing linked programs establish only their recorded validation scope. New experiments and FlagQuantum capabilities need explicit audits and checks through the [implementation workflow](implementation-roadmap.md); no new API support or hardware execution is certified by this page.

The [source anchors](references/hybrid-computing.md) give the primary research and official runtime documentation used to scope these patterns. The [architecture audit](curriculum-audit.md) tracks the remaining review work.
