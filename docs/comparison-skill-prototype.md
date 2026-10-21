# First agent skill prototype: state and operator comparison

**Version 0.1.0 · October 21, 2026 · author-verified prototype.** This is the first executable package under the [dual-entry design](dual-entry.md). It is not independently accepted or a released skill. No new textbook section is authored here.

[Skill entry and instructions](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/skills/compare-quantum-states-and-operators/SKILL.md) · [Exact input/output contract](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/skills/compare-quantum-states-and-operators/references/contract.md) · [Actual evaluation evidence](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/skill-evaluations/state-operator-v0.1/author-report.json)

## Invoke the prototype

Ask an agent that supports local `SKILL.md` packages to load `skills/compare-quantum-states-and-operators/SKILL.md` from this repository. For example: “Use this skill to compare these two statevectors; preserve the computational basis and allow one overall state phase. Save the request, residuals and limitations.” No global installation is performed by this update. Runtime-specific discovery/installation is separate from the scientific contract.

The bundled helper is independently callable with Python 3.12 and its standard library. The package can be copied alone to a temporary workspace. Run from the repository root:

```bash
cat > /tmp/mqc-comparison-request.json <<'JSON'
{"kind":"state","mode":"global-phase","basis_a":["0","1"],"basis_b":["0","1"],"a":[[1,0],[0,0]],"b":[[0,1],[0,0]]}
JSON
python skills/compare-quantum-states-and-operators/scripts/compare.py \
  < /tmp/mqc-comparison-request.json > /tmp/mqc-comparison-result.json
python - <<'PY'
import json
with open('/tmp/mqc-comparison-result.json') as stream:
    result = json.load(stream)
print(result['status'])
print(result['alignment_multiplier_on_b'])
print(result['aligned_residual'])
PY
```

Expected output:

```text
within_tolerance
[0.0, -1.0]
0.0
```

The full result also contains the raw residual, decision residual, overlap, dimensions, phase scope and absolute tolerance. Exit codes are 0 for within tolerance, 1 for outside tolerance, 2 for invalid input and 3 for unsupported scope. An outside-tolerance result is a valid answer; handle exit 1 when using a shell that stops on nonzero status. Invalid/unsupported results are not evidence of physical inequality.

## Three explicit comparison questions

The source derivations remain in [3.1](chapters/ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-1) and [3.7](chapters/ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-7). Support mathematics comes from 2.1, 2.2, 2.8 and the phase-tracked decomposition of 3.6. These source sections remain drafts with independent acceptance pending.

| Mode | Mathematical question | Code and verification |
|---|---|---|
| `coordinates` | Are the supplied coordinates close with their phase retained? | Decide using the direct Euclidean/Frobenius residual. A state and its multiple by i differ by distance √2. |
| `global-phase` | Can one unit-modulus scalar align the entire state or isolated operator? | Use one flattened inner product. I and −I align; I and Z have operator distance 2 despite agreeing on basis-input rays. |
| `controlled` | Are the full controlled extensions equivalent up to one phase on that full operation? | Construct diag(I,U) before comparison. Controlled I and controlled −I have residual √8, even though the isolated targets align. |

<span id="comparison-alignment-v1"></span>

For flattened entries of two validated objects, the mathematical-to-code contract is

$$
c=\sum_j a_j^*b_j,\qquad
z=\begin{cases}c^*/|c|,&c\ne0,\\1,&c=0,\end{cases}
\qquad r=\left\|a-zb\right\|.
$$

Expanding the squared norm gives the phase-dependent term $-2\operatorname{Re}(zc)$. Its minimum therefore uses the stated z. `overlap` computes c; `compare` applies z to **b**; `norm` computes the residual directly, avoiding cancellation in the squared-distance identity near equality. For matrices, flattening gives the Frobenius norm and a single phase for the whole operator. Per-column phase alignment would answer a weaker and incorrect equivalence question.

Zero overlap has no identifiable aligning phase: the deterministic convention is z=1, and the result sets `phase_identifiable=false`. Near-zero overlap makes the phase unstable; a stable residual does not make the phase physically identifiable. The flag describes the floating-point overlap, not confidence from measurements.

## Inputs, outputs and stopping boundaries

The JSON contract declares `kind`, `mode`, both basis-label lists and both arrays; `atol` is optional. Every complex entry is an explicit `[real,imaginary]` pair. Only dimension-2/4 pure states and square unitaries are supported; controlled mode takes a dimension-2 target. Both bases must be canonical: 0,1 or 00,01,10,11. In controlled mode the first output qubit is the control. The helper cannot prove that a caller labeled an array correctly.

Inputs must already be normalized/unitary within the declared validation tolerance 1e-12. The helper rejects invalid arrays without renormalization, basis guessing, imaginary-part removal or batch reshaping. The default comparison tolerance is absolute 1e-10; permitted values are [1e-14,1e-6]. State distance is Euclidean; operator distance is Frobenius, without dimension normalization. Equality at the threshold counts as within tolerance. This numerical decision is not a proof of exact physical equality.

Missing phase context requires clarification. Density matrices, channels, shot distributions, unknown bases and larger controlled contexts require another profile. Equal computational probabilities do not establish state equality. A dropped target phase cannot be ignored under coherent control. No comparison result establishes algorithmic equivalence, hardware fidelity or whole-paper reproduction.

The helper itself does not execute FlagQuantum. The evaluation adapter checks actual output shape `(1,4)`, CPU device, complex128/float64 dtypes, finiteness, normalization and amplitude/probability agreement before exporting one sample. It runs released FlagQuantum 0.3.1 with statevector/PyTorch, fallback and approximation disabled.

## Evidence and acceptance

The [predeclared protocol](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/skill-evaluations/state-operator-v0.1/protocol.json) requires correct statuses and exit codes, analytic residual agreement within absolute 2e-12, and zero false successes, incorrect abstentions or unexpected exceptions. The [package freeze](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/skill-evaluations/state-operator-v0.1/package-freeze.json) records SHA-256 for every package file before the transfer fixtures were written. Execution uses a fresh temporary copy of that package, without repository imports.

| Category | Cases passed / total | Representative obligation |
|---|---|---|
| Normal | 11 / 11 | Global versus relative phase; whole operator versus columns; three real FlagQuantum comparisons |
| Boundary | 7 / 7 | Zero/near-zero overlap, dimension 4, exact tolerance and its adjacent floating-point values |
| Error or unsupported scope | 21 / 21 | Zero/nonunit state, nonunitary matrix, missing context, malformed/nonfinite JSON, basis mismatch, density input |
| Post-freeze transfer | 6 / 6 | Nonlandmark complex states, four-coordinate input, generic complex unitary, controlled target phase |

**45/45 helper cases passed; three actual FlagQuantum executions passed.** Analytic residual references include orthogonal-state √2, I/Z distance 2, controlled sign distance √8 and generic phase-dependent distances. Wrong-input cases check rejection rather than counting a stopped task as a numerical success. The saved report includes every request, expected status/metric, actual structured output, exit code, environment and package hash.

The transfer cases are author-designed after package freeze. They exercise inputs not used in helper development, but **are not a blind independent agent evaluation**. This run evaluates the executable helper and the producing-program adapter; it does not establish autonomous skill selection, ambiguity clarification or unseen-paper competence. An independent agent must still receive raw tasks without expected answers and be evaluated on routing, artifact production, context questions and false-success/abstention rates. Independent mathematical/implementation acceptance and reader trials remain pending; released-skill count remains zero.

Rerun the recorded test set (the CLI's isolated package copy needs only the standard library; the evaluation runner needs the existing example environment):

```bash
python -m pip install -r requirements-examples.txt
python scripts/check_comparison_skill.py
python scripts/build_agent_skills_plan.py --check
python -m mkdocs build --strict
```

The default rerun verifies the frozen hashes and cases without overwriting original evidence. `--record` is reserved for an initial report and refuses to overwrite it. Future fixes require preserved failure evidence and a newly versioned package/evaluation set. The package is added to CI; a green rerun does not advance independent acceptance. The next step is independent forward testing of this bounded skill, rather than broader paper-reproduction claims or new textbook prose.
