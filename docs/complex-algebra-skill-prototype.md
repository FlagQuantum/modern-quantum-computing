# Complex linear algebra: fourth agent skill

**Prototype 0.1.1 · October 21, 2026 · scientific acceptance pending.** This bounded L1 package implements selected contracts across [Chapter 2, sections 2.1–2.8](chapters/ch-complex-vectors-operators-and-numerical-reasoning.md). No new textbook section is written.

[Skill instructions](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/skills/translate-complex-linear-algebra/SKILL.md) · [Complete task schemas and numerical contract](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/skills/translate-complex-linear-algebra/references/contract.md) · [Capability catalog](agent-skills.md)

## What depends on FlagQuantum?

This skill performs **classical CPU complex128 linear algebra using Torch 2.13.0 and scalar references under CPython 3.12**. It does not import FlagQuantum and records `quantum_execution:false`. Its vectors need not be normalized states. The textbook's Chapter 2 uses the same separation between mathematical computation and quantum execution.

The [comparison skill](comparison-skill-prototype.md) also has a framework-independent comparison core. The [interference](interference-skill-prototype.md) and [phase-tracked evolution](unitary-evolution-skill-prototype.md) skills construct and run actual released FlagQuantum circuits. A physical qubit evolution request must route to the latter; computing a matrix here does not fulfill a request to execute that circuit. These mathematical references help detect simulator errors rather than using one simulator as its own only reference.

## Task and input/output contract

All requests explicitly declare `coordinates:"literal-complex"` and `tolerance:{"atol":...,"rtol":...}`. Complex coordinates are `[real,imaginary]`; matrices are row lists. Shapes are bounded to 1..8 in each dimension, with no batches or silent reshaping. Finite scalar parts have magnitude at most 1e6, and nonzero magnitude at least 1e-100. Both tolerances are in [0,1e-8]. Values, basis conventions, physical conversions and desired tolerances are inputs, not things to guess.

| Chapter source | Task | Recorded output and boundary |
|---|---|---|
| 2.1–2.2 | `algebra` | Complex inner/dyadic products, adjoint, ordered products and matrix action; indexed scalar references |
| 2.3 | `basis` | Passive coordinates/operator, Gram matrix, condition number and reconstruction; explicit column convention and condition limit |
| 2.4 | `classify` | Within-budget Hermitian/unitary/normal/idempotent identities; orthogonal projection requires Hermiticity as well as idempotence |
| 2.5 | `decompose` | Hermitian spectral reconstruction or full rectangular SVD, numerical rank and right-kernel projector; no unique factor gauge claim |
| 2.6 | `function` | Matrix polynomial or bounded matrix exponential; no uncontracted logarithm/square-root branches or physical-unit substitution |
| 2.7 | `solve` | Solution, singular extremes, condition number, residual and optional candidate-error bounds; no small-residual accuracy shortcut |
| 2.8 | `check` | Exact metadata admission followed by elementwise complex-modulus comparison; no broadcasting, casts or phase alignment |

Outputs preserve runtime, Torch version, declared budgets, internal checks and classical-execution scope. A successful classifier run can correctly report a property as false. A successful solve can correctly expose a poor candidate. Neither is acceptance of an external claim.

## Formula → derivation → code → verification

### Conjugation and literal coordinates

For complex vectors,

$$
\langle v,w\rangle=\sum_j\overline{v_j}w_j,
\qquad (vw^\dagger)_{jk}=v_j\overline{w_k},
\qquad (A^\dagger)_{jk}=\overline{A_{kj}}.
$$

Writing each scalar as $a+ib$ gives $\overline{(a+ib)}(c+id)=(ac+bd)+i(ad-bc)$. This indexed expansion supplies an independent reference for `torch.vdot`. The helper checks dyads and products against scalar coordinate sums as well. It retains input phase and scale; pure-state ray equivalence belongs to the comparison skill.

### Passive coordinates require both conversions

With new basis vectors as columns of $S$, the represented vector satisfies $x=Sy$. Applying $A$ gives $Ax=ASy=SB y$, hence

$$
y=S^{-1}x,\qquad B=S^{-1}AS,\qquad
\lVert x\rVert^2=y^\dagger(S^\dagger S)y.
$$

The helper uses `torch.linalg.solve(S,x)` and `torch.linalg.solve(S,A@S)`, then checks reconstructed action and the Gram metric. Substituting $S^\dagger$ for $S^{-1}$ requires orthonormality; it is invalid for a general basis.

### Decompositions are checked as operators and subspaces

For Hermitian $H$ and rectangular $A$,

$$
H=Q\Lambda Q^\dagger,\qquad A=U\Sigma V^\dagger.
$$

Orthonormal eigenvectors diagonalize $H$; singular vectors instead diagonalize the positive semidefinite operators $A^\dagger A$ and $AA^\dagger$. The helper checks defining equations and reconstruction. Full SVD factors retain right-null directions that a reduced rectangular factor can omit. Phases and repeated-subspace bases are nonunique, so author checks compare projectors instead of demanding one raw vector tuple.

A relative singular-value cutoff defines a numerical rank. The reported numerical kernel and its actual residual do not prove exact rank or authorize replacing the original matrix by a truncated model.

### A small residual can hide a large solution error

Let $x_*$ solve $Ax_*=b$ and let $c$ be a candidate. Then $x_*-c=A^{-1}(b-Ac)$, so

$$
\lVert x_*-c\rVert_2\leq\frac{\lVert b-Ac\rVert_2}{\sigma_{\min}(A)},
$$

and, for nonzero $b$,

$$
\frac{\lVert x_*-c\rVert_2}{\lVert x_*\rVert_2}
\leq\kappa_2(A)\frac{\lVert b-Ac\rVert_2}{\lVert b\rVert_2},
\qquad \kappa_2(A)=\frac{\sigma_{\max}(A)}{\sigma_{\min}(A)}.
$$

The second inequality also uses $\lVert b\rVert_2\leq\lVert A\rVert_2\lVert x_*\rVert_2$. The helper records the estimated singular extremes and these normwise bounds, with a caller-declared condition limit. The inequalities are exact-arithmetic statements; floating-point SVD/residual estimates are not interval certificates. A zero right-hand side makes the relative bound undefined, so it is returned as null.

### Tolerance is a declared asymmetric contract

The strict comparison follows section 2.8:

$$
|a_j-r_j|\leq\mathrm{atol}+\mathrm{rtol}|r_j|.
$$

It checks exact shape/dtype/device declarations and finiteness before arithmetic. Complex modulus couples the real and imaginary errors. No common phase is removed, and swapping actual/reference can change a relative-budget decision. Metadata supplied in JSON is a declaration; retain actual producer logs to establish upstream provenance.

## Runnable conditioned-solve example

Run from the repository root using the pinned interpreter environment:

```bash
python skills/translate-complex-linear-algebra/scripts/algebra.py <<'JSON' > /tmp/algebra-result.json
{"task":"solve","coordinates":"literal-complex","tolerance":{"atol":1e-8,"rtol":0},"matrix":[[[1,0],[0,0]],[[0,0],[9.313225746154785e-10,0]]],"rhs":[[1,0],[0,0]],"candidate":[[1,0],[1,0]],"max_condition":10000000000}
JSON
python - <<'PYCODE'
import json
r=json.load(open('/tmp/algebra-result.json'))
c=r['result']['candidate']
print(r['status'])
print('quantum execution:', r['quantum_execution'])
print('condition number:', int(r['result']['condition_2']))
print('candidate residual passes:', c['residual_within_elementwise_budget'])
print('distance to computed solution:', c['observed_distance_to_computed_solution_2'])
print('relative forward bound:', c['relative_forward_error_bound_2'])
print('candidate accuracy certified:', c['candidate_forward_accuracy_certified'])
PYCODE
```

Expected output:

```text
verified
quantum execution: False
condition number: 1073741824
candidate residual passes: True
distance to computed solution: 1.0
relative forward bound: 1.0
candidate accuracy certified: False
```

Here $A=\operatorname{diag}(1,2^{-30})$, $b=(1,0)^T$, $x_*=(1,0)^T$ and $c=(1,1)^T$. The candidate has residual $2^{-30}<10^{-8}$ and relative forward error exactly 1. Passing the residual budget therefore does not establish the claimed forward accuracy. The declared condition limit allows this deliberately ill-conditioned diagnostic example; it does not remove the warning.

## Evidence and acceptance

The frozen package passed **57 author cases**: 21 normal, 14 boundary, 19 error and three author-transfer cases. These are 57 actual helper invocations and **zero quantum circuits**. References include separate NumPy computations, analytic diagonal/nilpotent/Jordan examples, projector checks and exact conditioned examples. Torch and NumPy can share numerical algorithm/backend families; their agreement is numerical evidence, not an independent proof.

**All 12 new tasks passed their registered disposition gates across three independent agents:** seven supported algebra tasks (including an intentionally failing comparison), two invalid inputs, one unsupported logarithm request, one actual FlagQuantum evolution task and one comparison-only task. There were 12 recorded helper calls: ten to this algebra helper, one to comparison and one to evolution. The algebra helper executed zero circuits; the routed evolution task executed nine actual FlagQuantum circuits. Two required semantics were clarified before execution; a third exchange confirmed the unsupported logarithm scope. No package defect surfaced in this initial set. A subsequent author boundary audit found the error-metadata issue described below; the initial package, outcomes and failure are retained.

### Recorded repair and fresh blind retest

The initially pushed 0.1.0 version computed the analytic Taylor-tail expression directly in binary64. For a positive matrix scale of 1e-100 it displayed a zero bound through underflow, despite a strictly positive analytic expression. The matrix exponential remained correct. The [original failure record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/skill-evaluations/complex-algebra-tail-repair-2026-10-21/failure.json) is preserved.

Version 0.1.1 keeps the logarithm of the analytic expression and flags/clamps an underflowed positive bound to the smallest positive binary64 number; only the zero input norm reports zero. The ordinary and log values remain floating estimates, not interval certificates. Two added author boundary cases check tiny positive and zero input scales.

Three additional fresh agents received nine new tasks without expected answers or a defect description. **All nine retest tasks passed**, including independent high-precision/analytic audits of tiny and zero exponential metadata, a new convention clarification, literal phase-sensitive comparison and unsupported branch selection. Their nine calls are classical; zero quantum circuits were executed in this retest. See the [fresh retest report](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/skill-evaluations/complex-algebra-blind-retest-2026-10-21/report.json). These are separate from the original twelve tasks; do not combine the two rounds into an unqualified first-pass success.

Independent-agent task evidence is recorded separately in the [blind report](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/skill-evaluations/complex-algebra-blind-2026-10-21/report.json), alongside the [author report](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/skill-evaluations/complex-algebra-v0.1.1/author-report.json). Agents receive raw tasks and four available skill packages, not expected answers. Actual FlagQuantum executions from a routing task are attributed to the selected evolution skill, never this classical helper.

```bash
python scripts/check_algebra_skill.py
python scripts/check_algebra_blind_evidence.py
python scripts/check_algebra_retest_evidence.py
```

The latter two commands grade/replay archived evidence; they do not rerun autonomous agents. The task sample is small and conductor-designed; agents use no prior history but the same inherited model family. Workspace restrictions are logical rather than OS-enforced. Scientific acceptance and reader trials remain pending. No skill is released as accepted, and no arbitrary-paper reproduction ability is certified.

## Failure boundaries and transfer checks

Non-Hermitian spectral input, singular bases, mismatched metadata, missing tolerance or malformed arrays are rejected. A caller condition limit can make an otherwise meaningful solve unsupported. General nonnormal eigenproblems, physical-unit functions, uncontracted function branches, arbitrary dimensions, symbolic proofs and quantum execution are outside the profile. Internal check failure is preserved without increasing tolerance.

1. **Why is an idempotent matrix not necessarily an orthogonal projector?** Orthogonal projection also requires self-adjointness in the chosen metric; an oblique projector can satisfy $P^2=P$ while $P\ne P^\dagger$.
2. **Why compare a degenerate eigenspace projector?** An orthonormal basis can rotate within the eigenspace without changing its projector or the operator.
3. **Transfer:** replace $A$ by $10^{-12}I$ and keep nonzero $b$. Its condition number is 1 despite tiny singular values; the solution scale changes, so inspect absolute as well as relative error budgets.
4. **Transfer:** request physical qubit evolution rather than a matrix function. Select the phase-tracked evolution skill and retain actual FlagQuantum execution evidence; this helper's numerical success alone is insufficient.
