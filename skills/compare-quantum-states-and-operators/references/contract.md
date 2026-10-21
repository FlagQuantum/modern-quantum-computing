# Comparison contract 0.1.1

Runtime: CPython 3.12 standard library, binary64 complex arithmetic, CPU. The folder is self-contained; it needs neither repository imports nor an installed FlagQuantum. The optional FlagQuantum evaluation adapter is in the repository test runner.

## Sources and symbol mapping

Canonical prose at source revision `62f7055475ba3ad5b418ea8249e08fa7e8add588`:

- [3.1 pure states](https://flagquantum.github.io/modern-quantum-computing/chapters/ch-single-qubit-states-and-rotations/#sec-single-qubit-states-and-rotations-1); formula IDs `formula-code-3-1-normalization`, `formula-code-3-1-alignment`.
- [3.7 phase contracts](https://flagquantum.github.io/modern-quantum-computing/chapters/ch-single-qubit-states-and-rotations/#sec-single-qubit-states-and-rotations-7); formula IDs `formula-code-3-7-operators`, `formula-code-3-7-controlled`.
- Prerequisite closure: 2.1 complex coordinates, 2.2 inner products, 2.8 numerical validation; 3.6 for phase-tracked decomposition applications. These are explained drafts, not independently accepted sources. The catalog dependency on `translate-complex-linear-algebra` is a mathematical import, not an installed-package dependency.

For flattened entries, set `c = sum(conj(a[j])*b[j])` (`overlap`). Expansion gives squared distance `||a||² + ||b||² - 2 Re(z*c)`. Maximizing the last term yields `z = conj(c)/abs(c)` when `c != 0`. The script multiplies **b** by z; reversing inputs conjugates that phase. It computes `||a-z*b||` directly (`norm`) to avoid cancellation in `2-2*abs(c)`. For unitaries the flattening gives Frobenius distance, with one z across all entries, not per column. Numerical checks retain the actual validated norms rather than assuming exactly normalized floating-point inputs.

When c is zero every unit phase minimizes the distance: return z=1 and `phase_identifiable=false`; no division by zero. For near-zero c the selected phase is ill conditioned. Neither case invalidates the residual. Phase identifiability describes this exact floating-point overlap, not statistical confidence.

`controlled` constructs diag(I,U) in order 00,01,10,11 with the first qubit the control (`controlled`). Align only the **full** four-dimensional operation. An isolated target phase becomes a relative branch phase and is observable on coherent inputs. No control-phase repair is inserted automatically.

## Runtime admission

The CLI checks its actual interpreter before parsing an object request. A different Python minor version or implementation returns `unsupported` (exit 3), with reason `unsupported_runtime` and the actual runtime. Do not count this as a state/operator result or silently widen the supported runtime. Select an available CPython 3.12 interpreter explicitly and rerun, or report the environment boundary. Every CLI result records its actual `runtime` implementation and Python version.

## Input

One JSON object, exactly these keys (plus optional `atol`):

```json
{"kind":"state","mode":"global-phase","basis_a":["0","1"],"basis_b":["0","1"],"a":[[1,0],[0,0]],"b":[[0,1],[0,0]]}
```

- `kind`: `state` or `unitary`. Vector entries or square-matrix entries are `[real,imaginary]` pairs of JSON numbers. No strings, booleans, NaN, infinity, duplicate keys or extra fields. Dimensionless coordinates, each real/imaginary part bounded by 2 before arithmetic to prevent overflow.
- State shape (2,) or (4,); unitary shape (2,2) or (4,4). No batch axis. Each state must already satisfy squared norm within 1e-12 of 1; each entry of U†U-I must have magnitude at most 1e-12. Reject rather than repair. This entrywise validation is distinct from the Frobenius decision metric.
- `basis_a`, `basis_b`: exactly `["0","1"]` or `["00","01","10","11"]`, matched to dimension. Matrix rows and columns use the same order. Different/undeclared bases require a documented transformation first. For controlled mode input basis labels describe the target; output order is control then target.
- `mode`: explicit `coordinates`, `global-phase`, or `controlled`; controlled requires kind unitary and dimension 2. A coherent implementation inside a still larger context is outside this profile.
- `atol`: absolute Euclidean/Frobenius tolerance, default 1e-10, allowed finite [1e-14,1e-6]. No relative tolerance or dimension normalization. Specify it before execution; values below validation tolerance do not imply stricter normalization. This is a bounded numerical profile, not a physical error budget or exact equality proof.

## Output and failure boundary

`within_tolerance` (exit 0) or `outside_tolerance` (exit 1) includes raw and aligned residuals, chosen decision residual, multiplier on b, overlap, phase-identifiability flag, dimensions, metric, phase scope and tolerances. Coordinates mode decides using the raw residual; the aligned residual is diagnostic only. The other modes decide using aligned residual. The boundary is inclusive (`residual <= atol`). No shot uncertainty is applicable to these deterministic arrays.

`invalid_input` (exit 2) returns a reason for a violated input contract: malformed JSON, missing/unknown fields, shape mismatch, nonfinite/zero/nonunit state, nonunitary matrix, invalid tolerance or invalid mode. It is not evidence that the intended physical objects differ.

`unsupported` (exit 3) returns a reason for other representation kinds (density, channel, counts), noncanonical basis, or a dimension-4 target requested in controlled mode. Other dimensions fail this bounded input schema. Report the unavailable profile; do not reshape or substitute another problem. A missing mode/context must be clarified by the agent, not guessed from the arrays.

Equal probabilities, agreement on basis-input rays, or a scalar phase of an isolated target are insufficient for stronger comparisons. A comparison also does not prove that two algorithms or noisy physical implementations are equivalent.
