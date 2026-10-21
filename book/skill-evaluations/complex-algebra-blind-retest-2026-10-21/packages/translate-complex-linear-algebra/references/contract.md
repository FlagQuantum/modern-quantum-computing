# Complex linear algebra contract 0.1.1

## Sources, scope and shared representation

Book source checkout: `5eaf5718de35e5b87152fa6f176f05e7587bd948`. Chapter 2's stable section anchors `sec-complex-vectors-operators-and-numerical-reasoning-1` through `-8` cover scalar coordinates, sesquilinear products, basis changes, operator identities, spectral/SVD reconstruction, matrix functions, conditioning and finite numerical contracts. This package is a bounded task implementation of those drafts, not a claim that every possible linear-algebra formula is implemented.

Every request requires `task`, `coordinates: "literal-complex"`, and `tolerance: {"atol": number, "rtol": number}`. Both tolerances are finite in [0,1e-8], including exact-zero budgets when justified. There is no guessed tolerance. Scalar coordinates are `[real,imaginary]`; vectors are lists of those pairs and matrices lists of rows. Dimensions are 1..8, no batches/ragged arrays/implicit flattening. Scalar parts are finite real JSON numbers with magnitude <=1e6; nonzero parts must have magnitude >=1e-100. No booleans, strings, NaN/Inf, duplicate keys, missing/extra task fields or repair by casting are accepted. Computational inputs use CPU complex128. Literal coordinates retain global phase and scale; vectors need not have norm 1.

For equally shaped finite quantities the comparison is **elementwise complex modulus**:

`abs(actual_j-reference_j) <= atol + rtol*abs(reference_j)`.

No norm substitution, broadcasting or phase alignment. `max_absolute_error` and `max_element_budget` are summaries only: the pass decision checks each corresponding entry. Relative budgets are asymmetric. Runtime: CPython 3.12, Torch base 2.13.0 (wheel suffix recorded). The helper guards the actual interpreter. This package is classical tensor/scalar computation, has no FlagQuantum dependency and records `quantum_execution:false`; that does not verify any upstream simulator.

## Task fields and formula-to-code map

### algebra — sections 2.1–2.2

Require `operation` plus the following exact fields:

| Operation | Additional fields | Output and reference |
|---|---|---|
| `inner` | `v`, `w`, same length | scalar sum conjugate(v_j)*w_j; `torch.vdot`; independent scalar sum; squared norms |
| `outer` | `v`, `w`, lengths m,n | m×n matrix v_j*conjugate(w_k); outer(v,conj(w)) |
| `adjoint` | `matrix` | conjugate transpose, shape n×m; independent row/column indexing |
| `matvec` | `matrix`, `v` | sum_k A_jk*v_k, preserve output dimension |
| `matmul` | `left`, `right` | ordered matrix product; independent indexed scalar sum |

Example:

```json
{"task":"algebra","coordinates":"literal-complex","tolerance":{"atol":1e-12,"rtol":0},"operation":"inner","v":[[1,0],[0,1]],"w":[[2,0],[1,1]]}
```

Expected value is `[3,-1]`, not a bilinear dot product. Outer products use conjugation on w, not v. A scalar can be represented as a length-one vector for supported inner/product operations; arbitrary symbolic scalar parsing is excluded.

### basis — section 2.3

Require square `matrix` A, square `basis_columns` S of the same size, `v` x in old coordinates, `direction:"passive-new-in-old"`, and explicit `max_condition` in [1,1e12]. Columns of S contain the new basis in old coordinates. Solve S*y=x and S*B=A*S. Report y, B, Gram S†S, old length², naive new Euclidean length² and Gram-weighted length². Check S*y=x, S*B=A*S and S*B*y=A*x. S† is the inverse only for an orthonormal S; this profile does not assume it. Active transforms are a different request and must be clarified/routed explicitly.

### classify — section 2.4

Require square `matrix`. Record within-budget residuals for A=A†, A†A=I, A†A=AA† and A²=A. An orthogonal-projector decision requires both Hermiticity and idempotence. `verified` certifies these tests were evaluated consistently, not that every property is true or that a near identity is an exact theorem. Positivity certification from finite sample vectors is not offered.

### decompose — section 2.5

Require `matrix` and `kind`. `hermitian` requires a square Hermitian input before `torch.linalg.eigh`: max-entry discrepancy <=1e-12 times max-entry magnitude, including tiny input scales. No symmetrization. Return eigenvalues, column eigenvectors and reconstruction; check eigenpair equations, orthonormality and Q*diag(values)*Q†. Eigenvectors have phase freedom; repeated eigenspaces have basis freedom. Independently compare eigenvalues, reconstruction and eigenspace projectors, never one raw vector tuple as uniquely required.

`svd` supports rectangular matrices and uses full U, rectangular Sigma and full V†. Return reconstruction and the **numerical** right-kernel projector using optional `rank_rtol` (default1e-12, range[0,1e-6]): retain singular values strictly greater than rank_rtol*s_max. A zero matrix has numerical rank 0. Report cutoff and actual kernel residual; do not present discarded small values as mathematically exact zeros. Kernel residual is diagnostic, not forced to zero by the reconstruction budget. No pseudoinverse or truncated replacement is submitted. Singular-vector signs/phases and bases in repeated blocks are not unique.

### function — section 2.6

Require square `matrix`, `kind`, `units:"dimensionless"`. `polynomial` also requires 1..9 complex `coefficients` in ascending degree order. Evaluate with Horner's matrix rule and check against independently summed matrix powers. Constant coefficients multiply the identity, not an all-ones matrix.

`exp` computes the matrix exponential, not entrywise exponential. It is bounded to infinity norm (maximum absolute row sum) <=1, and checks Torch matrix_exp against an independent scalar-list order-40 Taylor sum. Report mathematical truncation tail bound `rho^41/41!/(1-rho/42)`; it excludes roundoff, so it is not an interval accuracy certificate. For positive rho, a binary64 underflow in the displayed bound is clamped to the smallest positive binary64 number and flagged; the log of the analytic expression is retained. Only rho=0 reports a zero bound. The recorded ordinary/log values are floating estimates, not outward-rounded interval certificates. Non-Hermitian inputs are permitted and no norm-preservation claim follows. No silent input rescaling. Physical energy/time conversion and qubit circuit realization belong to the phase-tracked evolution skill. Logarithm/square-root branch selection, arbitrary functions and time-dependent evolution are excluded.

### solve — section 2.7

Require square `matrix`, matching `rhs`, explicit `max_condition` [1,1e12]; optional matching `candidate`. Solve A*x=b without explicit inversion. Estimate kappa_2=s_max/s_min with SVD; a computed s_min=0 is rejected as singular, and a condition number exceeding the caller limit is unsupported. A nonzero smallest singular value is not a proof of exact nonsingularity: the gate is numerical admission, not symbolic rank certification. Uniform scaling does not itself change kappa.

Report computed solution, singular extremes, kappa and residual. For a candidate c report residual norm r=||b-Ac||_2, relative residual r/||b||_2 when b!=0, normwise backward error r/(||A||_2||c||_2+||b||_2), and bounds r/s_min (absolute forward) and kappa*r/||b||_2 (relative forward). The inequalities are exact-arithmetic statements for declared A,b; reported SVD/residual values are floating estimates, not outward-rounded certificates. With b=0 the relative bound is undefined and returned null; the absolute bound remains meaningful. Distance to the computed solution is an observation, not a certified exact-solution oracle. Candidate accuracy is explicitly not certified by a loose residual pass.

### check — section 2.8

Require `actual` and `reference`, each exactly `{ "shape": [...], "dtype":"complex128", "device":"cpu", "values":[[re,im],...] }`. Shape has 0..2 axes with dimensions1..8; scalar shape[] has one value. Values are explicitly flattened in row-major order with exactly product(shape) entries. Shape/dtype/device declarations must match exactly before arithmetic; current profile supports CPU complex128 only. Declarations are supplied metadata, not attestation of an upstream run; preserve its actual producer records separately. No casting, broadcasting, missing-value repair, phase matching or finite-NaN equality. Return `within_tolerance`/0 or `outside_tolerance`/1 according to the declared elementwise reference-scaled budget. This decision is separate from an internal numerical failure.

## Output and failure boundaries

Outputs carry contract/runtime version, task result, declared tolerance, internal residual checks and actual Torch version. `verified`/0 means supported internal checks pass; false classifications or a candidate with poor forward accuracy can still be honestly reported. `verification_failed`/1 preserves failed internal checks. `invalid_input`/2 covers schema/dimension/nonfinite/admission violations; `unsupported`/3 covers scope/runtime/condition limits; `execution_failed`/4 preserves unexpected backend/finite-output failures. No automatic widening of tolerance.

Small dense classical complex128 only. No sparse/infinite/symbolic proof engine, general nonnormal eigendecomposition, implicit least-squares solution, upstream dtype recovery, arbitrary-paper reproduction, circuit synthesis, noise, shots, hardware or FlagQuantum execution. If a request is an isolated ray/controlled equivalence question select the comparison skill; if it is a prepared phase scan select interference; if it needs a physical generator converted to an actual qubit circuit select unitary evolution. Keep external claim rejection separate from successful execution.
