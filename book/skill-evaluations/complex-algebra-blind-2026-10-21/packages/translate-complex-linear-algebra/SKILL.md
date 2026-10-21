---
name: translate-complex-linear-algebra
description: Translate finite complex vector and matrix formulas into checked classical computations, including conjugation, basis changes, decompositions, matrix functions and conditioned solves. Use for literal coordinate algebra and numerical contracts, not state-ray equivalence, quantum-circuit execution or symbolic proof.
---

# Translate complex linear algebra

**Prototype 0.1.0.** Read [the task schemas and numerical contract](references/contract.md) for the selected task. Sources are textbook Chapter 2, sections 2.1–2.8. These are explained drafts; numerical verification does not confer scientific acceptance.

Resolve shapes, literal coordinate order, conjugation, multiplication order, units and the requested error budget before executing. Vectors here need not be normalized quantum states. Inner products conjugate the first argument; dyads conjugate the second vector. A transpose is not an adjoint. Missing basis direction, physical conversion, or desired tolerance needs clarification, not a guess.

Use an existing **CPython 3.12 / Torch base 2.13.0** environment explicitly. The helper runs classical CPU complex128 computations and independent scalar references; **it does not import FlagQuantum or execute a quantum circuit**. Do not install packages silently or relabel classical checks as FlagQuantum execution.

```bash
/path/to/python3.12 /path/to/translate-complex-linear-algebra/scripts/algebra.py < request.json > result.json
```

Supported bounded tasks are `algebra`, `basis`, `classify`, `decompose`, `function`, `solve`, and strict metadata-aware `check`. Preserve requests, actual stdout/stderr/exit codes, runtime and separate independent checks. Do not compare raw eigenvector or SVD factor phases as unique answers. Verify reconstruction, defining equations and, when needed, eigenspace/kernel projectors under an explicitly justified spectral cutoff. Numerical rank is not exact rank.

For passive basis conversion, columns of S are the new basis in old coordinates: x_old=S*x_new and B=S^-1*A*S. Use Q† only when orthonormality is established. A nonorthogonal coordinate vector uses S†S as its metric. Ask before choosing passive conversion versus an active map.

Report both absolute and reference-scaled relative tolerances. The elementwise test is |actual-reference| <= atol + rtol*|reference|, with exact shape/dtype/device admission first. Swapping actual and reference can change a decision. The same declared budget applies to internal reconstruction checks; a failed check remains a failure, never an automatic reason to widen tolerance. Classifications are within-budget identity decisions, not exact mathematical theorems.

For solves/basis changes require the caller's maximum condition number. Reject singular inputs or stop when the condition limit is exceeded. A candidate's small residual does not certify its forward accuracy; report the normwise bounds, conditioning assumptions and floating-point limitations separately. No pseudoinverse, rank truncation or symmetrization repairs a request silently.

Successful internal execution does not certify a supplied formula or paper claim. Audit claims separately. Route physical single-qubit evolution to an available unitary-evolution skill, prepared phase scans to the interference skill, and state/operator ray or coherent-control equivalence to the comparison skill. This skill's `check` preserves literal coordinates and never aligns phase.

Stop unsupported symbolic/infinite-dimensional/sparse/batched tasks, general nonnormal eigenproblems, uncontracted function branches, physical-unit exponentials, noise/hardware and circuit synthesis. Status/exit: `verified` or `within_tolerance`/0; `verification_failed` or `outside_tolerance`/1; `invalid_input`/2; `unsupported`/3; `execution_failed`/4. Preserve failed evidence and avoid a blanket arbitrary-paper reproduction claim.
