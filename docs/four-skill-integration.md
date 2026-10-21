# Four-skill composition: energy offsets and interference

**Experiment workflow 0.1.0 · October 21, 2026 · independent scientific acceptance pending.** This is one bounded integration experiment through the mathematical and qubit conventions of Chapters 2–3. It is **not a fifth agent skill**, a new textbook section, an accepted release or a whole-paper reproduction.

[Runnable workflow](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/integration/four_skill_interference.py) · [Complete example input](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/integration/interference-request.json) · [Dual entry](dual-entry.md)

## The four responsibilities

| Existing skill | Responsibility in this experiment | Execution evidence |
|---|---|---|
| [Complex linear algebra 0.1.1](complex-algebra-skill-prototype.md) | Dimensionless matrix exponential, ordered matrix action and readout references | Classical CPU complex128; no quantum circuits |
| [Unitary evolution 0.1.0](unitary-evolution-skill-prototype.md) | Physical units to full unitary; direct/native evolution; actual controlled-phase repair | Released FlagQuantum 0.3.1, Torch 2.13.0 |
| [Interference 0.1.0](interference-skill-prototype.md) | Consume the prepared complex state; phase scan and declared analyzer | Actual fresh state preparation and FlagQuantum readout per scan point |
| [Comparison 0.1.1](comparison-skill-prototype.md) | Full-coordinate state/operator checks, isolated ray and controlled-context distinctions | Classical residual computation; not a circuit execution |

The workflow also executes a **continuous single-circuit path** with the original preparation, evolution and readout in one circuit per phase. The interference helper instead prepares the supplied intermediate state anew. Agreement between them checks the classical handoff; it does not make that handoff a persistent backend state, a hardware state-transfer protocol or a mid-circuit measurement.

## Formula → derivation → code → observed result

### 1. Convert energy and time before forming a matrix function

Use a constant energy Hamiltonian $\mathsf H$, an explicitly declared numerical $\hbar$, and elapsed time $t$. Define

$$
E=\frac{t\mathsf H}{\hbar},\qquad U=\exp(-iE).
$$

The example specifies

$$
\mathsf H=\frac{\hbar}{1\,\mathrm{ns}}K,\qquad K=0.37I+0.49Y,\qquad t=0.61\,\mathrm{ns}.
$$

Thus $E=0.61K$. Since $Y^2=I$, even and odd terms in the exponential give

$$
U=e^{-i(0.37)(0.61)}\left[\cos(0.49\cdot0.61)I-i\sin(0.49\cdot0.61)Y\right].
$$

The scalar phase is $e^{-0.2257i}$; it is retained. `01-classical-exponential` calls the algebra skill on the dimensionless matrix $-iE$. `02-evolution` passes the original eV Hamiltonian, ns time and explicit eV*s value of ℏ to the evolution skill. `03-full-matrix` compares the complete matrices without phase alignment.

The value 6.582119569e-16 eV*s is a declared numerical conversion input here. No external provenance or physical-constant accuracy is certified. Angular-frequency input in rad/s instead uses $E=tG$ with no second division by ℏ. Cyclic Hz must be resolved and explicitly multiplied by $2\pi$ before using that profile.

### 2. Preserve the prepared state, including its phase

The example starts with $|\psi_0\rangle=0.6i|0\rangle+0.8|1\rangle$. Let

$$
|\psi_t\rangle=U|\psi_0\rangle=a|0\rangle+b|1\rangle.
$$

`04-classical-action` computes the reference matrix-vector product. The evolution helper's supplied-input/direct record supplies the actual state. Before extraction, the workflow checks the documented singleton shape `(1,2)`, CPU complex128 metadata, canonical basis, source record and content digest. It then extracts exactly that one validated sample to the interference helper's `(2,)` JSON contract. Both real and imaginary components remain intact; there is no normalization or phase repair.

The state ray, complete coordinates and complete controlled operation answer different questions. If the three native Euler gates implement $V=e^{-i\alpha}U$, then

$$
V|\psi_0\rangle=e^{-i\alpha}|\psi_t\rangle,
\qquad C(U)=\operatorname{diag}(I,U).
$$

The isolated rays agree, but full coordinates need not. Generally $C(V)$ also differs from $C(U)$ up to any single phase on the whole controlled operation. `05`–`08` retain these separate decisions. For the baseline, the isolated operator ray passes while the omitted-phase controlled comparison fails, with residual approximately **0.225580256**. This is an intentional counterexample; the evolution helper's actual phase-repaired controlled circuit passes its own checks.

### 3. Apply the declared analyzer in chronological order

Define $D(\theta)=\operatorname{diag}(1,e^{i\theta})$ and let $W$ be the Hadamard matrix. The declared chronological readout is $D(\phi)$, then $D(-\delta)$, then $W$:

$$
|\chi(\phi)\rangle=WD(-\delta)D(\phi)|\psi_t\rangle
=\frac{1}{\sqrt2}\begin{pmatrix}a+e^{i(\phi-\delta)}b\\a-e^{i(\phi-\delta)}b\end{pmatrix}.
$$

Expanding the complex modulus yields

$$
p_0(\phi)=\frac{|a|^2+|b|^2}{2}+\operatorname{Re}\left[\overline a\,e^{i(\phi-\delta)}b\right],\qquad
p_1(\phi)=|a|^2+|b|^2-p_0(\phi).
$$

The actual validated norm is retained in this formula rather than silently rounded to exactly one. The workflow passes the unchanged radian scan and delta to `09-interference`, checks staged and continuous full complex outputs through the comparison skill, and checks final probabilities separately. The author verifier uses an independent NumPy Hermitian eigensystem, chronological matrices and scalar cross term. Both algebra and evolution helpers use Torch internally, so their mutual agreement alone is not the independent scientific reference.

With delta **0.31 rad**, the baseline observations are:

| Phase (rad) | Probability 0 | Probability 1 |
|---|---|---|
| 0.17 | 0.354994689 | 0.645005311 |
| 1.03 | 0.757265695 | 0.242734305 |
| 2.11 | 0.985349377 | 0.014650623 |

These deterministic probabilities are neither shot counts nor hardware confidence intervals.

## Tolerance and handoff ledger

The caller declares one local maximum-coordinate budget $\epsilon$ and zero relative tolerance. The supported experiment range is $5\times10^{-12}\leq\epsilon\leq10^{-9}$. The classical exponential profile additionally requires $\lVert E\rVert_\infty\leq1$; no silent scaling extends this profile.

| Boundary | Contract |
|---|---|
| Classical algebra | Elementwise complex error <= epsilon, rtol=0 |
| Evolution and interference | Maximum coordinate/probability error <= epsilon; existing 1e-12 input validation remains independent |
| Two-component state comparison | Euclidean budget sqrt(2)*epsilon |
| 2×2 operator comparison | Frobenius budget 2*epsilon |
| Basis / shape / dtype / device | Exact metadata admission before arithmetic; no inferred permutation, broadcasting or low-precision promotion |
| Source receipt | Canonical request digest and preserved actual helper stdout; cached status alone is insufficient |
| Final continuous versus staged output | Full complex state comparisons plus independent final per-coordinate/probability checks |

The input profile is `constant-qubit-interference` with exactly two canonical amplitudes and a Hermitian 2×2 generator. Numeric time values in s/ns have absolute value <=1; generator/state scalar parts are finite with magnitude <=1e12, and state norm² must be within1e-12 of1. Energy inputs require a positive caller-declared hbar in[1e-100,1]eV*s. The explicitly listed scan has1..9phase values and analyzer delta, each in[-1024,1024]radians. Signed time is mathematical inverse evolution, not a laboratory reversal claim. Missing context or conversion data blocks dependent execution.

The dimension factors follow $\lVert x\rVert_2\leq\sqrt d\lVert x\rVert_\infty$ and its four-entry matrix version. They are explicit metric conversions, not hidden tolerance loosening. Local budgets do not prove an arbitrary accumulated-error theorem: the final experiment outputs are checked separately. Declared producer metadata and hashes are evidence linkage, not a security attestation of an untrusted producer.

## Run the complete example

Use the pinned CPython 3.12 / FlagQuantum 0.3.1 / Torch 2.13.0 CPU environment from the repository root:

```bash
integration_tmp=$(mktemp -d)
python examples/integration/four_skill_interference.py \
  --request examples/integration/interference-request.json \
  --output "$integration_tmp/run" --skills-root skills
python - "$integration_tmp/run/report.json" <<'PYCODE'
import json,sys
r=json.load(open(sys.argv[1]))
print('helpers:', len(r['helper_calls']))
print('new skill:', r['workflow_is_agent_skill'])
for item in r['outputs']:
    print(f"phi={item['phase_radians']:.2f}: p0={item['probabilities'][0]:.9f}")
PYCODE
```

Expected output:

```text
{"actual_flagquantum_circuits": 15, "stage": "complete", "status": "verified"}
helpers: 18
new skill: False
phi=0.17: p0=0.354994689
phi=1.03: p0=0.757265695
phi=2.11: p0=0.985349377
```

Each new output directory contains the source request, all actual helper requests/stdout/stderr/exits, digests, versions, handoff envelope, continuous-circuit records and final report. Existing output directories are rejected to preserve evidence. The 15 actual circuits are nine evolution/witness circuits, three staged scan circuits and three continuous circuits. The witness count includes the deliberately unrepaired controlled variant; it is not fifteen independent hardware experiments.

## Errors deliberately included

The author's 18 cases comprise six supported experiments, seven injected handoff/unit errors and five input/scope boundaries. All registered case checks pass, with **142 actual simulator circuit executions** across successful paths, intentional witness circuits and rejected partial paths.

- ns relabeled as s exceeds the original dimensionless exponent contract.
- Dropping the intermediate scalar phase passes a state-ray diagnostic but fails the full-coordinate handoff and controlled-context claim.
- Reversed basis labels, a broadcast-looking shape, or a foreign source digest are rejected before the state is consumed.
- Analyzer sign changes or a widened helper tolerance are rejected against the caller's unchanged contract.
- Missing ℏ and unresolved Hz require clarification; invalid norms and nonzero relative tolerance are rejected; hardware/noise/shot certification remains unsupported.

Faults are explicitly marked test injections. Synthetic blind-audit fixtures are labeled synthetic, not fabricated execution records. Failed paths retain their actual partial executions and do not become successful experiments because an earlier helper returned `verified`.

**Independent blind evaluation:** three fresh agents passed all nine registered task dispositions: three new full experiments, five submitted-result audits and one unsupported hardware request. Their actual records contain six successful fresh workflow runs, one unsupported preflight, eight additional audit-helper calls, 110 helper calls in total and **89 actual FlagQuantum circuit executions**. The two required unit/conversion clarifications occurred before dependent execution. No change to the frozen runner or four packages was required. Fresh-run success never overrode candidate rejection.

[Author evidence](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/skill-evaluations/four-skill-integration-v0.1.0/author-report.json) · [Independent blind-agent evidence](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/skill-evaluations/four-skill-integration-blind-2026-10-21/report.json)

```bash
python scripts/check_four_skill_integration.py
python scripts/check_four_skill_blind_evidence.py
```

The first command reruns the author case suite. The second grades/replays archived executor artifacts; it does not rerun autonomous agents. Original requests, explicit conversion replies, frozen code/packages, independent verifier code and actual run records are retained separately. Executor agents have no author conversation history or expected answers; the conductor grades outcomes against registered dispositions. Sampling is small/nonrandom, restrictions are logical rather than OS-enforced, and exact backend/token/cost telemetry is unavailable. Scientific acceptance and reader trials remain pending. Four skill packages remain implemented; zero are accepted releases. No fifth skill or textbook section is created.
