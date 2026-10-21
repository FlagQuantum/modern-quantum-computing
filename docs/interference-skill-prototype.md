# Second agent skill: reproduce single-qubit interference

**Prototype 0.1.0 · October 21, 2026 · independent-agent-tested; scientific acceptance pending.** This is the second executable task package under the [dual-entry design](dual-entry.md), based on existing textbook [3.2 Relative phase and interference](chapters/ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-2). No textbook section is added.

[SKILL.md](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/skills/reproduce-qubit-interference/SKILL.md) · [Exact experiment/input/output contract](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/skills/reproduce-qubit-interference/references/contract.md) · [Author execution report](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/skill-evaluations/qubit-interference-v0.1.0/author-report.json) · [Independent blind-test report](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/skill-evaluations/qubit-interference-blind-2026-10-21/report.json)

## Task and boundary

Given an explicitly prepared pure qubit, a relative-phase scan and a specified readout, construct an ideal FlagQuantum experiment and check its complex amplitudes and probabilities against independent references. The chronological order is **prepare supplied state → D(phi) → optional D(-delta), H → computational readout**. Direct readout and recombining readout are separate experiments; no intermediate measurement is inserted.

The package requires CPython 3.12, FlagQuantum 0.3.1 and Torch base version 2.13.0. It runs statevector/PyTorch on CPU with complex128, fallback and approximation disabled. It records actual versions, shapes, dtypes and device. It does not install dependencies, change the environment or submit hardware jobs. It is a repository package, not a globally installed skill or an accepted release.

The profile supports two complex amplitudes in basis 0,1; a list of 1–129 phase angles; and either computational readout or the analyzer H D(-delta). It does not certify noise, laboratory visibility, mixed states, shot statistics, tomography, intermediate measurements or arbitrary gate chronology. Missing preparation, units or analyzer context must be clarified before dependent execution.

## Formula → implementation → verification

The source section's stable formula IDs are linked in the package contract. Imports are pure states/Born probabilities from 3.1, complex arithmetic/inner products and matrix order from 2.1–2.3, and numerical contracts from 2.8. These remain explained drafts; prototype testing does not promote their scientific acceptance.

<span id="interference-input-v1"></span>

The input is the already prepared state, in the declared fixed basis:

$$
|\psi\rangle=\alpha|0\rangle+\beta|1\rangle,
\qquad n=|\alpha|^2+|\beta|^2\approx1.
$$

The helper checks the squared norm within absolute 1e-12; it does not repair it. For arbitrary complex input it constructs a preparation matrix whose first column is the supplied representative:

$$
U_{\mathrm{prep}}=
\begin{pmatrix}\alpha&-\beta^*\\\beta&\alpha^*\end{pmatrix}.
$$

The columns have equal squared norm n and their inner product cancels. At exact unit norm this is unitary, and its action on the initial basis state gives the supplied amplitudes. `circuit.unitary(0, unitary=preparation)` is a checked API in the pinned release; no initialization API is invented. For the balanced real input it prepares the same state as the first Hadamard in the textbook experiment.

<span id="interference-amplitudes-v1"></span>

After the phase scan and the selected analyzer, the two output amplitudes are

$$
\gamma_0=\frac{\alpha+e^{i(\phi-\delta)}\beta}{\sqrt2},
\qquad
\gamma_1=\frac{\alpha-e^{i(\phi-\delta)}\beta}{\sqrt2}.
$$

The code calls `phase(0, theta=phi)`, then `phase(0, theta=-delta)`, then `h(0)`. The scalar `reference` follows that order; the actual complex statevector must match it. For computational-only readout there is no analyzer: the output coordinates are simply alpha and exp(i phi) beta.

<span id="interference-probabilities-v1"></span>

Expanding the squared moduli, rather than propagating input probabilities, gives

$$
\begin{aligned}
p_0&=n/2+\operatorname{Re}\!\left(\alpha^*e^{i(\phi-\delta)}\beta\right),\\
p_1&=n/2-\operatorname{Re}\!\left(\alpha^*e^{i(\phi-\delta)}\beta\right).
\end{aligned}
$$

`cross` retains the conjugate on alpha. `analytic` computes both probabilities independently of the simulator matrices; using n/2 retains the actual validated floating-point norm. Each point checks the simulator statevector against scalar amplitudes, the simulator probabilities against this formula, and probabilities against squared output moduli. The author test runner adds an independent NumPy matrix product H D(-delta) D(phi) applied to the original input.

<span id="interference-extrema-v1"></span>

For a complete continuous phase scan, fixed input magnitudes give

$$
p_{0,\min}=n/2-|\alpha||\beta|,
\qquad p_{0,\max}=n/2+|\alpha||\beta|,
\qquad \mathcal V=\frac{2|\alpha||\beta|}{n}.
$$

`fringe` reports these analytic continuous extrema separately from the extrema over the supplied sample grid. Sparse samples need not reach either extremum. If one input amplitude vanishes, visibility is zero and its relative phase is unidentifiable. Unequal coherent amplitudes can give visibility below one without a noise model. A fixed analyzer can also give identical probabilities for distinct state rays: the blind tests check that distinction with the [first comparison skill](comparison-skill-prototype.md).

## Run an example

Use a CPython 3.12 environment with the pinned example requirements installed. In the commands below, `python` must resolve to that compatible interpreter; otherwise substitute its explicit path. From the repository root:

```bash
cat > /tmp/mqc-interference-request.json <<'JSON'
{"profile":"ideal-pure-single-qubit","state":[[0.7071067811865475,0],[0.7071067811865475,0]],"basis":["0","1"],"angle_unit":"radian","phase_radians":[0,1.5707963267948966,3.141592653589793],"readout":{"type":"phase-h","delta_radians":0},"atol":1e-10}
JSON
python skills/reproduce-qubit-interference/scripts/interference.py \
  < /tmp/mqc-interference-request.json > /tmp/mqc-interference-result.json
python - <<'PY'
import json
with open('/tmp/mqc-interference-result.json') as stream:
    result = json.load(stream)
print(result['status'])
for point in result['records']:
    print([round(p,9) for p in point['probabilities']])
print('visibility',round(result['fringe']['continuous_visibility'],9))
PY
```

Expected output:

```text
verified
[1.0, 0.0]
[0.5, 0.5]
[0.0, 1.0]
visibility 1.0
```

To test complex conjugation and unequal magnitudes, change the input state to `[[0,0.6],[0,-0.8]]`, scan to `[0]`, and keep delta zero. The predicted probabilities are `(0.02,0.98)` and full-scan visibility 0.96. The helper actually executes these complex inputs; it does not reduce them to input probabilities or silently remove their phase.

## Input/output and failure semantics

All required fields are explicit: profile, two complex amplitudes as `[real,imaginary]` pairs, basis, angle unit, phase list and readout object. Only `atol` is optional. Phases/delta are bounded to [-1024,1024] radians. The absolute verification budget defaults to 1e-10, with allowed [1e-12,1e-8] and zero relative tolerance. Scalar coordinates must be finite; malformed/duplicate JSON, booleans, strings, invalid shapes, nonunit states and undeclared fields are rejected. The [exact contract](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/skills/reproduce-qubit-interference/references/contract.md) gives all limits.

| Status / exit | Meaning |
|---|---|
| `verified` / 0 | This bounded ideal execution agrees with its references within the declared budget |
| `verification_failed` / 1 | Actual numerical records exceeded that budget; preserve them as a failure |
| `invalid_input` / 2 | Schema/state admission failed; no valid experiment result |
| `unsupported` / 3 | Representation, unit, basis, readout or runtime outside profile |
| `execution_failed` / 4 | Dependency/import/backend execution failed; no successful simulation claim |

A successful ideal run does **not** make a supplied formula, cache, noisy interpretation or laboratory claim true. Keep those claims outside the strict helper request, compare them with fresh evidence and return a separate disposition. In the noisy blind task the untouched raw request includes an undeclared noise field, so the CLI actually returns schema error/exit 2. The agent correctly explains that the physical noise/laboratory task is unsupported; it does not relabel the CLI outcome or replace it with an ideal certification.

## Author verification and independent blind evaluation

The [package freeze](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/skill-evaluations/qubit-interference-v0.1.0/package-freeze.json) pins the evaluated working-tree package with SHA-256. Its checkout base is the prior published repository, not a claim that the old commit already contained this skill. [Author criteria](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/skill-evaluations/qubit-interference-v0.1.0/protocol.json) require correct statuses/exit codes and coordinate/probability agreement with the independent matrix reference within absolute 2e-12.

**35/35 author cases passed**, with **167 actual FlagQuantum circuit executions**: 6 normal cases, 6 boundaries, 19 invalid/unsupported cases and 4 post-freeze author transfer fixtures. The boundaries include absent paths, negative/duplicate angles, angle limits, a 129-point maximum grid, and sampled versus continuous extrema. Real admission probes additionally confirm rejection of Python 3.9.6 and a CPython 3.12 environment with site packages disabled. Author fixtures are not independent-agent evidence.

Three **new agents with no inherited conversation history** received a frozen catalog containing two implemented skills, raw new tasks and existing interpreter candidates. No expected answers, suspected defects or prior conclusions were supplied. References and criteria were frozen outside their permitted workspaces before dispatch. They asked questions, ran actual helpers, wrote verification scripts and saved requests, stdout/stderr, exit codes, runtimes, explanations and claim dispositions. The author/conductor graded those artifacts; scientific and reader acceptance remain separate.

| Blind task(s) | Behavior checked | Result |
|---|---|---|
| A1, C1 | Missing readout; missing units despite a misleading field name | Asked before execution; applied caller-specified analyzer or explicit degree-to-radian conversion, preserving original values |
| A2 | Complex conjugation, unequal magnitudes, sparse versus continuous extrema | Correct amplitudes/probabilities and visibility 0.96 |
| A3 | Nonunit input | Rejected unchanged; no normalization repair |
| A4 | A comparison question rather than an experiment | Selected the first skill, not the interference helper |
| B1 | Explicit direct readout | Preserved absence of analyzer; probabilities 0.34,0.66 with no fringe |
| B2 | Equal fixed-setting probabilities for different rays | Used both skills; experiments agree on probabilities while ray comparison gives distance √2 |
| B3 | Noisy profile and unsupported laboratory certification | Preserved actual schema rejection; asked for unavailable physics/evidence and did not certify the claim |
| B4, C4 | Wrong plus-delta formula; false cached success | Fresh executions and independent checks refuted both |
| C2 | Absent path | Zero visibility; relative phase unidentifiable |
| C3 | Phase, H, H instead of H, phase, H | Reported chronology mismatch; separately derived the literal sequence without claiming helper execution |

**12/12 blind tasks passed**: 8 supported interference tasks, 1 invalid input, 2 unsupported tasks and 1 comparison-only task. The agents executed **18 actual FlagQuantum circuits**, making 13 recorded helper invocations across the two skills. There were zero false successes and zero incorrect abstentions under these task contracts. Two required semantic clarifications and one additional unsupported-domain/evidence clarification were recorded. No package defect or numerical discrepancy was found in this set, so no post-blind tuning was performed.

The [frozen evidence bundle](https://github.com/FlagQuantum/modern-quantum-computing/tree/main/book/skill-evaluations/qubit-interference-blind-2026-10-21) includes raw tasks, both loaded package snapshots, reference keys, invocation prompts, question/reply records, independent agent artifacts and conductor grades. Workspace read restrictions were logical, not OS-enforced. The sample is small and conductor-designed; agents inherited one model configuration, and exact backend revisions/token/cost telemetry were unavailable. No statistical, cross-model, arbitrary-paper or L4/L5 capability claim follows from these L1 tasks.

## Replay and lifecycle

```bash
python scripts/check_interference_skill.py
python scripts/check_interference_blind_evidence.py
python scripts/build_agent_skills_plan.py --check
python -m mkdocs build --strict
```

CI runs author examples and replays frozen numerical requests, checking hashes, routing, context, units, original inputs, claims and independent reference values. It does not rerun autonomous agents or count published tasks as new held-out evidence. Future changes need preserved failures and fresh task sets where relevant. The skill is now an **independent-agent-tested prototype**; independent scientific acceptance, reader trials and release remain pending. The first skill is unchanged. No new textbook section, paper run, hardware submission or PDF edition is included.
