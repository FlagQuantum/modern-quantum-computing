---
name: translate-unitary-evolution
description: Translate constant single-qubit generator evolution, active Pauli rotations and phase-tracked ZYZ factorization into verified FlagQuantum circuits. Use when units, gate order or full operator phase matter; not for time-dependent solvers, inverse Hamiltonian identification, noise or hardware.
---

# Translate phase-tracked unitary evolution

**Prototype 0.1.0.** Read [the mathematical and input/output contract](references/contract.md) before preparing a request. Sources are textbook 3.4–3.6, with complex algebra/numerics from Chapter 2, pure-state conventions from 3.1 and the optional controlled-context bridge from 3.7. Source drafts and numerical runs do not confer scientific acceptance.

Identify the requested task (`evolve`, `rotation`, `factor`), basis, initial state, and context (`isolated` or `coherent-control`). Ask for missing semantics before dependent execution. A dimensionless generator, angular frequency H/hbar, energy Hamiltonian, cyclic frequency in Hz and rotation angle are different inputs. Do not guess units, hbar, a factor of 2pi or whether a scalar phase may be dropped. Only a constant 2x2 generator is supported; a single endpoint does not identify a unique generator.

Read the actual interpreter/package versions. Use an existing CPython 3.12 environment with released FlagQuantum 0.3.1 and Torch base 2.13.0. Select that interpreter explicitly; do not assume `python3` is compatible or install/change software silently.

```bash
/path/to/python3.12 /path/to/translate-unitary-evolution/scripts/unitary.py < request.json > result.json
```

Save the request, actual stdout/stderr/exit code, runtime and independent verification. Preserve the full target matrix U and the returned scalar phase. The convention is U = exp(i alpha) Rz(beta) Ry(gamma) Rz(delta), with active rotations Rn(theta)=exp(-i theta n.sigma/2) and angles in radians. Native calls occur in chronological order **rz(delta), ry(gamma), rz(beta)**. Branches and endpoint choices need not give unique or continuous Euler angles; verify reconstructed matrices instead of demanding one angle tuple.

The three native rotations implement V, not generally U. In isolated checks, multiplying the returned array by exp(i alpha) is explicitly diagnostic arithmetic, not a submitted global-phase gate. In `coherent-control`, the helper actually implements the missing branch phase with `phase(0,theta=alpha)` on the control after controlled(V). Multiplying the whole two-qubit output by one scalar is not that repair. Rotation through 2pi can give -I even when a chosen determinant-phase branch has alpha=0; do not infer that V=I from alpha alone.

For `evolve`, preserve the scalar identity contribution in the generator and report the declared conversion to the dimensionless exponent. The trace-shift phase and the canonical determinant phase are different records: one describes the supplied generator, the other a nonunique factorization of its endpoint matrix. No energy zero or generator is inferred from U alone.

A `verified` helper result means this declared ideal computation agrees with references, not that a supplied paper claim, cache, omitted-phase decomposition or hardware claim is correct. Audit such claims separately. For an explicit state/operator-equivalence question choose an available comparison skill; for a prepared phase scan/analyzer experiment choose an interference skill rather than silently changing the task.

Stop or route unsupported time dependence, larger target registers, unknown units/bases, mixed/noisy/hardware models and inverse-generator requests. Reject nonunit axes, non-Hermitian generators, invalid states or nonunitary target matrices without repair. Exit 0 is verified, 1 numerical verification failed, 2 invalid input, 3 unsupported scope/runtime, 4 execution failed. Preserve failures rather than relabeling them successful scientific results.
