# Phase-tracked unitary contract 0.1.0

## Sources and implementation map

Canonical book source commit: `9f65888ea23c76466cbfacd2ab5147bdabcc0ec0`. [Chapter 3](https://flagquantum.github.io/modern-quantum-computing/chapters/ch-single-qubit-states-and-rotations/) supplies 3.4 constant Hermitian generation and dimensionless K=H*t0/hbar, 3.5 Pauli algebra/active rotations, and 3.6 phase-tracked ZYZ with endpoint cases. Stable section IDs end in `-4`, `-5`, `-6`; the optional coherent-control extension imports the explicit local block-matrix bridge in 3.7 (`-7`). Prerequisites: 2.1–2.3 complex arithmetic and matrix order; 2.4–2.6 Hermitian/spectral/function results; 2.8 numerical contracts; 3.1 normalized pure states. These are explained drafts with independent scientific/reader acceptance pending.

`validate` forms a dimensionless Hermitian exponent E from the declared input. Evolution uses U=exp(-iE), computed by `torch.matrix_exp` with the original validated E. An independent scalar Pauli reference writes E=e0 I+v.sigma, rho=|v|, and uses exp(-i e0)[cos(rho) I-i sin(rho)/rho v.sigma], with the rho=0 limit 1. This follows by squaring v.sigma and separating even/odd powers; no time-ordering rule is assumed. The identity coefficient e0 is retained, and its phase exp(-i e0) is reported. A single endpoint cannot identify e0, H or a unique logarithm.

`rotation` forms E=theta n.sigma/2 for a declared real unit axis. The scalar reference uses cos(theta/2)I-i sin(theta/2)n.sigma. Active, right-handed rotations use this **minus-i** convention. A positive z rotation gives diag(exp(-i theta/2),exp(i theta/2)); `phase(theta)` instead equals exp(i theta/2)Rz(theta). In particular Rn(2pi)=-I and Rn(4pi)=I. Native rx/ry/rz is additionally executed for exact signed Cartesian axes.

`factor` validates a supplied full 2x2 unitary U. `factor` chooses alpha=arg(det U)/2 using `cmath.phase`'s principal branch and V=exp(-i alpha)U. Let a=V00, c=V10. In the generic case beta=arg(c)-arg(a), gamma=2 atan2(|c|,|a|), delta=-arg(c)-arg(a). For |c|<=1e-12 select gamma=0, delta=0, beta=-2 arg(a); for |a|<=1e-12 select gamma=pi, delta=0, beta=2 arg(c). Endpoint snapping is checked by full reconstruction; the verification budget is at least 5e-12. No parameter uniqueness, branch continuity or stable angle inference near poles is claimed. Choosing the other square root changes both alpha and V; keeping old V while changing alpha is wrong.

The matrix convention is **U=exp(i alpha)Rz(beta)Ry(gamma)Rz(delta)**. `native_zyz_matrix` is only V. Native circuit calls go right-to-left through the product: rz(delta), ry(gamma), rz(beta). Actual direct and native circuits are checked on the supplied state and both basis states. Complex coordinates retain phase; no ray alignment is used for full reconstruction. The phase-corrected isolated output is labeled **diagnostic array arithmetic**, not an extra submitted gate.

For `coherent-control`, construct C(U)=diag(I,U), with basis 00,01,10,11, control qubit 0 and target qubit 1. C(V) alone generally differs; diag(I,exp(i alpha)I)C(V)=C(U). The helper executes that repair with native `phase(0,theta=alpha)` after the explicit controlled(V) matrix, on a superposed control and supplied target state. It also executes direct and unrepaired variants, with the latter checked against its own intentionally different matrix. It does not claim native controlled-Euler synthesis: the controlled V uses the existing generic `unitary(0,1,unitary=...)` API. A whole-output scalar would also change the control-0 branch and cannot replace the repair. If alpha=0, this particular omission witness may vanish; V can still be -I, as for a 2pi rotation.

## Exact JSON inputs

All tasks require `task`, `basis` exactly `["0","1"]`, `state` as two `[real,imaginary]` pairs, and explicit `context` (`isolated` or `coherent-control`). Optional `atol` defaults to 1e-10, allowed [5e-12,1e-8], absolute maximum-entry/coordinate errors with zero relative tolerance. Input-state squared norm must already be within 1e-12 of 1. No implicit batch stripping, basis permutation, normalization or phase discard.

### Constant generator

```json
{"task":"evolve","basis":["0","1"],"state":[[1,0],[0,0]],"context":"isolated","generator":{"matrix":[[[2,0],[0,-1]],[[0,1],[2,0]]],"unit":"1"},"time":{"value":0.5,"unit":"1"}}
```

Permitted generator/time pairs:

| Generator unit | Time unit | E | hbar field |
|---|---|---|---|
| `1` | `1` | tau K; K=H*t0/hbar and tau=t/t0 are already dimensionless | Forbidden; no physical t0 is inferred |
| `rad/s` | `s` or `ns` | t_seconds G, with G=H/hbar an angular-frequency generator | Forbidden; no second hbar division |
| `J` | `s` or `ns` | t_seconds H/hbar | Required `{"value":positive_number,"unit":"J*s"}` |
| `eV` | `s` or `ns` | t_seconds H/hbar | Required matching `eV*s` |

Nanoseconds convert by the exact factor 1e-9. Cyclic `Hz` is unsupported: clarify angular versus cyclic frequency before any explicit conversion. There is **no built-in physical constant lookup**. The caller supplies hbar's value, unit and external provenance/accuracy when using energies; the helper verifies matching units/positive value, not whether that numerical value is a scientifically justified physical constant. The number used in an experiment remains part of its input record.

Generator Hermiticity is checked **before multiplying by time**, using max-entry discrepancy <=1e-12 times the matrix's maximum entry magnitude, including tiny physical energy scales and t=0. No symmetrization is performed. Raw matrix/time coordinate magnitudes are bounded by 1e100, positive hbar by [1e-100,1e100]. Every dimensionless E entry must be finite with magnitude <=32. Signed time is allowed as mathematical inverse evolution, not a laboratory reversal claim.

### Active axis rotation

```json
{"task":"rotation","basis":["0","1"],"state":[[1,0],[0,0]],"context":"isolated","axis":[0,1,0],"angle":{"value":1.5707963267948966,"unit":"radian"}}
```

Three finite real axis components, each <=2 in magnitude, squared norm within 1e-12 of 1; no axis normalization. Angle is explicit radians with magnitude <=64. No degrees are guessed or silently relabeled.

### Full unitary factorization

```json
{"task":"factor","basis":["0","1"],"state":[[1,0],[0,0]],"context":"coherent-control","unitary":[[[0,0],[1,0]],[[1,0],[0,0]]]}
```

Square dimension-2 complex matrix; each entry of U†U-I must have magnitude <=1e-12. No projection onto a nearby unitary. This is an operator input, not a probability table or independently phase-aligned columns. All scalar parts are finite JSON numbers; strings, booleans, duplicate keys, nonstandard constants, missing/extra task fields and invalid shapes are rejected.

## Runtime, output and boundaries

CPython 3.12, released FlagQuantum 0.3.1, Torch base 2.13.0; actual wheel suffix/version recorded. CPU/PyTorch/statevector complex128, no fallback or approximation. The package does not install dependencies or grant hardware authority.

A verified output includes the original target matrix, phase-retaining reconstructed matrix, native V matrix, alpha/beta/gamma/delta and branch, chronological native calls, all unit-conversion details, and actual direct/native outputs on three declared inputs. Optional controlled records specify basis/qubit order, actual repair and omitted-phase operator residual. Shape/dtype/device/finiteness, Born probabilities, normalization and full complex coordinates are checked. Generator/rotation exponentials have the independent Pauli reference as well; author tests add a Hermitian eigensolver reference.

Statuses/exits: `verified`/0, `verification_failed`/1 (preserve actual failed checks), `invalid_input`/2, `unsupported`/3 (including runtime/profile), `execution_failed`/4. Unsupported larger, time-dependent, noisy/mixed/hardware or inverse-generator tasks must be stopped/routed, not silently replaced. Successful internal verification does not certify an external formula, cache, omitted-phase implementation, exact theorem, unique generator, or whole-paper reproduction. Report those claim dispositions separately from the helper status.
