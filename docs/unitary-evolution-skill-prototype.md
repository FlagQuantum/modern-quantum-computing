# Phase-tracked unitary evolution: third agent skill

**Prototype 0.1.0 · October 21, 2026 · independent scientific acceptance pending.** This bounded L1 skill implements the contracts of [3.4–3.6](chapters/ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-4), with the coherent-control distinction from [3.7](chapters/ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-7). It adds no textbook section and changes no prerequisite or proof-depth requirement.

[Skill instructions](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/skills/translate-unitary-evolution/SKILL.md) · [Complete input/output contract](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/skills/translate-unitary-evolution/references/contract.md) · [Capability catalog](agent-skills.md)

## Task, input and output

Select this skill for a constant Hermitian generator, an active Pauli-axis rotation, or full-matrix ZYZ factorization. Select the [comparison skill](comparison-skill-prototype.md) for an equivalence decision alone and the [interference skill](interference-skill-prototype.md) for a prepared-state phase scan. A request must declare the computational basis `0,1`, a normalized two-amplitude complex state, and `isolated` or `coherent-control` context. Complex values use `[real, imaginary]`. Missing physical units, conversion constants or phase context require clarification before execution.

| Profile | Required inputs | Boundary |
|---|---|---|
| `evolve` | Constant 2×2 Hermitian generator and signed time | Dimensionless generator/time; angular frequency in rad/s with s/ns; energy in J/eV with explicit matching positive ℏ in `J*s`/`eV*s` |
| `rotation` | Already normalized real axis; signed angle in radians | No silent normalization or degree relabeling |
| `factor` | Full 2×2 unitary, including its phase | No projection onto a unitary or inference from probabilities |

The response records the full matrix, extracted phase and Euler branch, chronological native gates, unit conversions, runtime versions, actual statevectors/probabilities and absolute errors. A corrected isolated state array is explicitly marked diagnostic arithmetic. It is not a submitted global-phase gate. Coherent-control requests additionally execute a two-qubit branch repair and record an intentionally unrepaired witness.

Execution requires **CPython 3.12, FlagQuantum 0.3.1, Torch 2.13.0**, ideal CPU PyTorch statevector simulation, complex128, no fallback or approximation. The helper checks the actual interpreter. This is a tested version contract, not a minimum-version promise.

## Formula → derivation → code → verification

### 1. Convert the generator before exponentiation

For an energy Hamiltonian,

$$
E=\frac{tH}{\hbar},\qquad U(t)=\exp(-iE).
$$

For an angular-frequency generator $G=H/\hbar$, use $E=tG$; for dimensionless $K$ and $\tau$, use $E=\tau K$. Convert ns to s before dividing by ℏ. Cyclic Hz needs an explicit $2\pi$ conversion after the caller resolves the convention. The helper never retrieves or certifies a physical constant.

Decompose $E=e_0I+\boldsymbol{e}\cdot\boldsymbol{\sigma}$. Since $(\boldsymbol{e}\cdot\boldsymbol{\sigma})^2=\rho^2I$, where $\rho=\lVert\boldsymbol{e}\rVert$, even and odd exponential terms give

$$
U=e^{-ie_0}\left[\cos\rho\,I-i\frac{\sin\rho}{\rho}\boldsymbol{e}\cdot\boldsymbol{\sigma}\right],
$$

with the ratio interpreted as 1 at zero. The scalar shift remains in the full matrix. The implementation uses `torch.matrix_exp(-1j * E)` as its primary exponential and checks it against this scalar Pauli expression. Author verification independently uses NumPy Hermitian eigendecomposition, including complex coordinates and unit conversions.

### 2. Keep the half-angle and active-rotation sign

$$
R_{\boldsymbol n}(\theta)=e^{-i\theta\boldsymbol n\cdot\boldsymbol\sigma/2}
=\cos(\theta/2)I-i\sin(\theta/2)\boldsymbol n\cdot\boldsymbol\sigma.
$$

A unit axis makes the squared Pauli combination equal to the identity. This gives $R_{\boldsymbol n}(2\pi)=-I$ and $R_{\boldsymbol n}(4\pi)=I$. Exact signed Cartesian axes are checked against actual native `rx`, `ry` or `rz` gates. Arbitrary axes use the full matrix plus the native ZYZ route.

### 3. Separate matrix factorization from submitted gates

$$
U=e^{i\alpha}V,\qquad V=R_z(\beta)R_y(\gamma)R_z(\delta),\qquad
\alpha=\tfrac12\operatorname{Arg}(\det U).
$$

The chronological circuit is `rz(delta)`, `ry(gamma)`, `rz(beta)`. It implements $V$. Multiplying its output array by $e^{i\alpha}$ checks a reconstruction but does not submit that phase as a gate. The determinant uses its principal argument; the sign of $V$ compensates its branch. Euler angles are neither unique at the poles nor globally continuous. Near-pole branches are judged by matrix error rather than a preferred angle tuple.

For a control-first basis `00,01,10,11`,

$$
C(U)=\operatorname{diag}(I,U),\qquad
[P(\alpha)\otimes I]C(V)=C(U),\qquad
P(\alpha)=\operatorname{diag}(1,e^{i\alpha}).
$$

The repair is an actual `phase(0, theta=alpha)` gate on the control. Multiplying the entire two-qubit output by one phase would change both branches and does not implement this repair. The helper submits a generic controlled matrix; it does not claim a native controlled-Euler compiler.

## Runnable example

From the repository root, in the pinned environment:

```bash
python skills/translate-unitary-evolution/scripts/unitary.py <<'JSON' > /tmp/unitary-result.json
{"task":"rotation","basis":["0","1"],"state":[[0,0.6],[0.8,0]],"context":"coherent-control","axis":[1,0,0],"angle":{"value":6.283185307179586,"unit":"radian"}}
JSON
python - <<'PYCODE'
import json
r=json.load(open('/tmp/unitary-result.json'))
print(r['status'])
print('actual circuits:', r['actual_flagquantum_circuits'])
print('U diagonal:', [round(r['unitary'][j][j][0], 9) for j in range(2)])
print('native rotation checked:', any(x['path']=='native-axis' for x in r['records']))
print('actual control repair:', r['controlled_context']['repair'])
PYCODE
```

Expected output:

```text
verified
actual circuits: 12
U diagonal: [-1.0, -1.0]
native rotation checked: True
actual control repair: actual phase(0,theta=alpha) on control after controlled(native)
```

Here the canonical determinant phase can be zero while $V=-I$. The minus sign has not disappeared: $C(-I)=\operatorname{diag}(1,1,-1,-1)$ differs from $C(I)$. To assess equivalence, invoke the comparison skill under the explicitly declared context. Do not decide from the phase scalar alone.

## Validation and evidence

The frozen package has **53 passing author cases**: 12 normal, 17 boundary, 21 error and 3 author-transfer cases, with **258 actual FlagQuantum circuit executions**. Errors include tiny non-Hermitian energy matrices at zero time, missing/mismatched ℏ, double division by ℏ, ambiguous Hz, invalid axes/states, malformed JSON and unsupported task profiles. Runtime admission probes are recorded separately from the 53 mathematical/schema cases.

**All 12 blind tasks passed:** seven supported evolution/factorization tasks, two invalid inputs, one unsupported task, one comparison-only task and one interference-only task. Their 16 actual helper calls executed 56 FlagQuantum circuits (54 for this skill and two for the interference selection check). Four clarification exchanges included three required semantics and an additional missing-schedule question; no expected results were supplied. No package defect or post-blind tuning occurred.

Three fresh no-history agents received twelve new raw tasks, a catalog with three runnable skills, frozen packages and interpreter candidates; they received no expected answers. The registered gates require correct skill selection, clarification before dependent execution, full complex-state references, phase-sensitive controlled witnesses and honest rejection of unsupported execution. See the [author report](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/skill-evaluations/unitary-evolution-v0.1.0/author-report.json) and [blind report](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/skill-evaluations/unitary-evolution-blind-2026-10-21/report.json) for actual dispositions and counts.

Reproduce the numerical regressions:

```bash
python scripts/check_unitary_skill.py
python scripts/check_unitary_blind_evidence.py
```

The second command replays archived helper requests and grades frozen artifacts; it does not rerun autonomous agents. Published tasks are regression fixtures after this evaluation. The conductor designed and graded a small nonrandom sample; executor agents used the same inherited model configuration and logical workspace restrictions, not OS-enforced isolation. Independent scientific acceptance and reader trials remain pending; zero skills are released.

## Failure boundaries and understanding checks

No time-dependent solver, generator inference from one endpoint, many-qubit synthesis, noisy/shot/hardware execution, gradients, physical calibration certification or arbitrary-paper guarantee is provided. Noncommuting time-dependent terms cannot be replaced silently by their average. Invalid raw generators are rejected before multiplication by time, including at zero time. No state normalization, matrix projection or phase deletion repairs the request silently.

1. Why can the identity part of a Hamiltonian be ignored for isolated probabilities but matter under coherent control? **Answer:** it multiplies the isolated state by one phase; under control it affects only the active branch relative to the idle branch.
2. Does a zero extracted determinant phase prove the gate is the identity? **Answer:** no; $-I$ has determinant 1 and can reside entirely in $V$.
3. Can endpoint Euler angles validate a unique underlying Hamiltonian? **Answer:** no; Euler branch/gauge choices and logarithm branches prevent that inference.
4. Transfer exercise: change the example to an arbitrary unit axis and angle $4\pi$. **Answer:** the full target is $I$ within the numerical budget; use the matrix exponential and reconstruction checks rather than expecting one unique angle tuple. A general axis has no direct Cartesian native-axis record.
