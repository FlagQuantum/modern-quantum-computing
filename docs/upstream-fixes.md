# Upstream correctness fixes

This is a revision-specific repair ledger, checked on **October 23, 2026 (Beijing time)**. It supplements the original implementation evidence in Sections 5.1, 7.1 and 7.2. It does not replace those records or change their draft/review status. The [machine-readable evidence ledger](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/verification/upstream-fixes-2026-10-22/manifest.json) links the original failures, final runs and baseline controls.

## Source repair, merge and release are separate

| Defect | Source repair | Validation | Merge/release status |
|---|---|---|---|
| [#685: nonunitary custom matrices accepted by `Circuit.adjoint`](https://github.com/flagos-ai/FlagQuantum/issues/685) | Merged [PR #711](https://github.com/flagos-ai/FlagQuantum/pull/711), commit `1f001da4c1f13260b1bba34dda14d958399a5a3f` | 202 focused adjoint/composition tests pass, including 80 adjoint tests | Merged by maintainer on October 22, 2026 at 05:13 UTC as `a1aab92d89dc732dbdc8b7fe020a5acb35c1a0fb`; no fixed release verified |
| [#704: tiny nonzero amplitudes lost in exact execution](https://github.com/flagos-ai/FlagQuantum/issues/704) | Merged [PR #712](https://github.com/flagos-ai/FlagQuantum/pull/712), implementation `046c465c6`; PR head `99f8c90befef7ca3480ef5f88909462b9e137115` | 439 focused compiler/inversion/synthesis tests pass, including 34 end-to-end cases | Merged on 2026-10-22T07:07:19Z as `8a18f55638affab78f3f6efffbaa6b196291da7a`; no fixed release verified |

Both branches start from upstream `main` commit `f187adbbf`. Their changes concern separate Core and Compiler ownership domains. A temporary local combination also passes **575 distinct selected tests**. These overlapping selections are separate checks, not additive test counts.

The source checkouts still report package version `0.3.1`; that string does **not** identify the published wheel or establish that a released package contains these changes. The commit IDs above identify the actual repaired implementations. Tests used Python 3.12.14, PyTorch 2.13.0, CPU, and complex128 unless an explicit complex64/other-dtype case was selected.

## What the repairs validate

### Custom-matrix inversion

Before the repair, all eight invalid-matrix regression cases failed because no rejection occurred: projectors, scaled unitaries, NaN and Inf were accepted in both complex64 and complex128. Two legitimate phase/gradient controls passed on the original implementation.

The proposed guard checks finite entries and both unitary Gram products, using zero relative tolerance and an absolute tolerance of 32 machine epsilons of the real component dtype. It validates the flattened operator rather than confusing tensor storage axes with matrix axes. Integer permutations remain admissible. The emitted conjugate transpose retains the original autograd graph and overall phase.

This is a numerical admission check, not an exact unitarity certificate or an inverse for a general nonunitary map. Channel and conditional-operation refusals remain in place.

### Tiny amplitudes and phases

Before the repair, 18 of the original 24 named/custom Ry-and-CNOT cases failed; six larger-amplitude controls passed. The new tests inspect tiny complex components with **zero absolute tolerance**, so a returned zero cannot pass merely because a general-purpose tolerance exceeds the expected amplitude.

The proposed compiler changes require an actual scalar zero for zero-angle deletion, retain nonzero residues near an identity period, and conservatively decline tolerance-based matrix folds for explicitly supplied components below their resolution. A guard on a small angle/component preserves the original gate; it is not permission to truncate that value. The existing numerical target-basis synthesis thresholds are retained explicitly. This repair concerns submitted-gate optimization; it does not certify tiny-angle accuracy through arbitrary target-basis decomposition.

The 34 end-to-end cases cover optimization levels 0/1/2; named and custom-matrix Ry; amplitudes from `1e-10` to `1e-14`; signed complex amplitudes; tiny relative and overall phases; nearly cancelling rotations; a trainable parameter initialized at zero; and nearly antidiagonal matrices. The implementation may retain extra gates where a tolerance-based rewrite cannot establish the required distinction. It is not a general interval error certificate or a claim about every backend, device or compiler transformation.

## Validation limits and review status

Ruff, Black and the domain ownership checks pass. The repository-wide tiers were also run. Initial integration invocations encountered 16 sandbox-denied localhost TCP failures/errors on each branch; the restriction was reproduced on the unmodified base, and all 16 passed when localhost process groups were permitted. The final frozen Compiler `pr-runtime` invocation passes uninterrupted: **1,838 passes and 122 skips**, with no failures or errors. The original restricted runs and recovery records are retained separately. The final frozen Core integration rerun also passes uninterrupted: **1,804 passes and 122 skips**, with no failures or errors. Both final invocations permit the localhost fixtures that the restricted runs could not initialize.

The frozen Core `pr-default` rerun completed with **14,395 passes, 304 skips and 15 failures**. All 15 failed cases were re-run on the unmodified base commit and also failed there. They concern CPU-kernel/gate-count expectations and evidence-policy checks. This establishes a baseline comparison, not a green full suite. The final Compiler rerun has **14,382 passes, 304 skips and the identical 15 failed node IDs**. All 15 failed node IDs match the base controls and both PR branches. Full-suite green is not claimed.

The initial Compiler patch's remote CPU job found 25 synthesis/factorization regressions. That revision is superseded by `046c465c6`: numerical basis synthesis is restored, the two-qubit guard is limited to the replacement step, and the affected files now pass. The split-block reach test uses exact S factors without relaxing its count/operator assertions; its original floating Rz-factor input is retained as a separate conservative-retention test. Original failures and revised validation are kept separately.

One earlier local Core whole-suite run loaded a transient compiler file while the working copy was being restored. It raised missing-helper import errors and is invalidated as mixed-source verification, not attributed to the product. The frozen-commit rerun above replaces it.

PR #711 was merged by maintainer `FlagQuantum`; its final head has 41 successful and two skipped checks. PR #712 was merged by maintainer `FlagQuantum` as `8a18f5563` after all latest-head CI checks completed: **41 successful, two conditional skips, no failures or pending checks**. The [frozen merge/check record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/verification/upstream-fixes-2026-10-22/pr712-merged-ci.json) records the exact head and outcomes. Their GitHub check panels are the authoritative live CI status. The merge is recorded separately from the CPU validation and does not establish a fixed package release. No GPU, hardware, distributed scalability or package-release validation is claimed here. Independent code review, mathematical review and reader acceptance have not been invented or marked complete.

The first latest-head CI attempt had canceled coverage jobs and stalled source-artifact downloads, not a reported assertion failure. Its [outcomes](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/verification/upstream-fixes-2026-10-22/pr712-ci-attempt1-jobs.json) and [recovery record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/verification/upstream-fixes-2026-10-22/pr712-ci-infrastructure-recovery.json) are retained separately from the successful final checks. No source changes or weaker test thresholds were used for this recovery.

## Benchmark-policy follow-up

The optional Qiskit job found five benchmark contracts still expecting the former near-zero deletion policy. Follow-up `99f8c90be` keeps the production compiler Python byte-for-byte unchanged from `046c465c6`, fixes the historical counterfactual tolerance explicitly, and re-measures the current contracts. **All 241 compiler benchmark-contract tests pass on certified Qiskit 2.5.2.**

The audit also found that the old benchmark erased intermediate measurements before comparing coherent vectors. That changes the experiment. Its bounded classical reference now sums unnormalized measurement branches and independently compares each optimized circuit with its source, keeping the existing probability-error bound. A dedicated H–measurement–H check distinguishes the instruments. The current policy retains more gates than the lossy reference (net signed reduction **-174**, not a speedup); old published result files are not rewritten. See the [upstream benchmark note](https://github.com/flagos-ai/FlagQuantum/blob/99f8c90befef7ca3480ef5f88909462b9e137115/benchmarks/notes/exact_identity_policy.md) and the evidence ledger.

## What readers should do now

Continue to use the released-version safeguards in [Section 5.1](chapters/ch-gates-reversible-computation-and-circuit-synthesis.md#sec-gates-reversible-computation-and-circuit-synthesis-1), [Section 7.1](chapters/ch-entanglement-and-quantum-information-protocols.md#sec-entanglement-and-quantum-information-protocols-1) and [Section 7.2](chapters/ch-entanglement-and-quantum-information-protocols.md#sec-entanglement-and-quantum-information-protocols-2). The book-side `checked_adjoint` guard and the validated larger epsilon remain in their released-0.3.1 examples. The original projector/scaled-H admission failure and tiny-angle failure evidence are retained.

The literal prose programs and complete examples in Sections 5.1, 7.1 and 7.2 were re-run on the installed released package; their expected outputs and assertions pass with the existing safeguards. The status update preserves all existing program/output fences and inline/display mathematics in those chapter pages. No new textbook section, skill, paper reproduction or PDF edition is introduced.

After a repair is merged and a release containing it is available, re-run the affected textbook programs and literal prose examples in a clean environment on that release, record its package provenance and independent references, and only then revise the compatibility notes or remove a workaround. A source regression, a merged PR and a newly published version each require their own evidence.
