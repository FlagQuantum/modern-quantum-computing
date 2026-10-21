# Paper reproduction: verification and acceptance

**Plan 0.1 · October 21, 2026 · proposed execution/acceptance standard.** This is a planning contract for future skills and paper runs. It does not certify an existing whole-paper reproduction. Use the [report worksheet](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/templates/paper-reproduction-report.md) and the [task contract](skill-contract.md).

## Register claims before execution

Assign a local claim ID to each selected theorem, algorithm, equation, numerical value, table/figure, scaling comparison or device result. Record the exact paper version and location, wording/quantifiers, assumptions, supplied artifacts, input access model and the observable/result that would support it. Mark which claims are mandatory, optional or excluded, with a reason and dependencies.

Agree the target model, dataset, system size, basis/order/phase convention, units, parameter grid, precision, seeds or sampling protocol, metrics, acceptance budgets, resources and stopping conditions before inspecting the reproduction's outcome. If a decision was made after seeing results, label it exploratory and rerun a frozen confirmatory protocol when appropriate. Do not choose tolerances, seeds, instances or baselines until a plot matches.

For a long paper, an authorized scoped claim set is a valid project. Its report must name the scope. Calling one reduced example a full-paper reproduction is not valid. A source-only paper or unavailable experimental input may be assessed and documented without being executable in FlagQuantum.

## Evidence depends on the claim

| Claim kind | Appropriate verification | Acceptance boundary |
|---|---|---|
| Mathematical theorem | Exact assumptions/quantifiers, complete proof or the assigned justified proof roadmap, independent scholarly review of the requested result | Finite simulations are sanity checks, not proof; no universal statement is certified by sampled inputs |
| Algorithm or circuit semantics | Tiny exact instances and independent indexed references; coherent/basis/conditional cases where relevant; explicit query/input-access and output semantics | Agreement on one basis distribution does not certify state, channel or controlled-operator equivalence |
| Deterministic numerical result | Traceable model/data, independent analytic/dense/reference implementation, declared metric and error budget, convergence checks when approximate | Distinguish roundoff, discretization, model reduction and truncation; reference provenance matters |
| Sampling, inference or trainable model | Fixed evaluation protocol, estimator and uncertainty, multiple independent seeds/runs when needed, complete outcome reporting and matched objectives/budgets | One favorable seed, overlapping intervals alone or matching a plotted trend does not establish the claimed accuracy |
| Performance, scaling or advantage | Equivalent task/input access, classical comparator, complete loading/compilation/communication/sampling/error-mitigation costs, hardware/software versions, repeated measurements and uncertainty | A small-instance simulation is not asymptotic evidence or quantum advantage; observed and extrapolated costs stay separate |
| Physical-device experiment | Actual device/provider identity, calibration/run dates, controls/readout, data and uncertainty, selection rules and model-to-device comparison | Simulation/model agreement is not repeated hardware execution; unavailable hardware/data must be visible |

If the task concerns state rays, compare one whole-state phase under a validated unit-norm contract. If it concerns a stated matrix convention, retain the specified phase. If it concerns a controlled/dynamic/channel operation, check the full operation and branch/result semantics. Specify the metric appropriate to that object; do not silently replace it with computational-basis probability agreement.

An independent reference must reduce the risk of a shared error: hand/analytic identities, a separately derived scalar/dense implementation, enumerated small cases or independently sourced data are useful. Two wrappers calling the same backend are not independent validation by themselves. Independent rerun/review is a separate requirement from an independent calculation inside one author's script.

## Error and statistical budgets

Choose units and the comparison's scale first. For deterministic arrays, define the object and norm or entrywise criterion, absolute/relative tolerance, metadata checks and finite-value requirements. Justify the total budget from rounding, discretization, truncation and model approximations; test convergence in the controls that affect those errors. Use condition-dependent diagnostics when small residuals do not guarantee small forward errors. There is no book-wide universal tolerance, and the existing unit-scale complex128 fixtures' budgets are not automatically paper acceptance targets.

For stochastic results, state the estimator, sample/shot count, confidence or credible-interval construction and its assumptions, failure/coverage level, effect or equivalence margin, and the number of seeds/instances. Address dependence and multiple comparisons when applicable. Compare against a predeclared scientific accuracy or equivalence criterion with the uncertainty included. Statistical non-rejection is not evidence of equality; an interval too wide to resolve the target leads to an inconclusive result. Raw counts and failed/aborted runs must remain auditable.

A complete reference may itself be uncertain: record exact, measured, digitized or inferred provenance. Matching a figure digitized from a PDF is not exact agreement with unavailable raw data. Never silently fit model parameters to a target and report the fitted comparison as independent reproduction.

## Artifact bundle for an actual run

| Artifact | Minimum contents |
|---|---|
| Paper and claim ledger | DOI/arXiv/URL or supplied source identity, exact version and section/equation/figure locations; mandatory/optional/excluded claims and scope decisions |
| Data/model provenance | Source/license/availability, geometry/integrals/calibration as relevant, retrieval date/hash, transformations and missing items |
| Mathematical/implementation contract | Symbols and units, access model, ordering and phase scope, approximations, formula-to-function/API mapping and source prerequisites |
| Environment and invocation | Repository/package commits, FlagQuantum and dependencies, backend/device/dtype, commands, seed policy, resource limits and genuine runtime settings |
| Actual evidence | Raw logs/status, intermediate outputs and final metrics, independent reference/expected values, uncertainty/error budget, failures and discrepancy analysis |
| Integrity and rerun | Machine-readable artifact inventory and hashes, runnable entry command, deterministic/stochastic comparison criteria and a clean-workspace rerun record |
| Review decisions | Author verification, independent evaluator identity/role and exact scope, scholarly/implementation decisions where needed, unresolved concerns and acceptance disposition |

The proposed bundle is run-local. It must contain actual results, not fields copied from a template as if they had run. Source access and copyright permissions remain relevant: identify third-party papers and lawful artifacts rather than publishing entire third-party books or private data. Credential values are not reproduction artifacts; record the required configuration without secret contents.

## Per-claim outcomes

| Outcome | Meaning |
|---|---|
| Reproduced in declared scope | The registered target met its predeclared criteria with the required evidence |
| Partially reproduced | A stated subset or modified scale/model was checked; differences and their effect are explicit |
| Blocked | A required input, resource or verified capability is missing; the report identifies it and the attempted independent work |
| Inconsistent with target | Checked results conflict with the target under the recorded assumptions; discrepancies are retained and investigated |
| Inconclusive | Evidence or uncertainty cannot resolve the target to the declared accuracy |
| Out of scope | The claim is outside the agreed task/domain, with a reason and no implied verification |

These outcomes are scientific dispositions, not package lifecycle states. A blocked or inconsistent outcome can be a correct, valuable report, but it is not a successful reproduction of that claim. Every mandatory claim must have a disposition; missing rows and cherry-picked successes prevent aggregate acceptance.

## Acceptance gates

| Gate | Required evidence and decision |
|---|---|
| G0: scope and feasibility | Claim ledger, source versions, resource model, required artifacts and frozen acceptance criteria reviewed before confirmatory execution |
| G1: mathematical translation | Assumptions, conventions, derivation/proof imports and formula/code correspondence reviewed; no known blocking scientific error |
| G2: implementation verification | Actual versioned execution, independent references, boundary/failure tests and approximation/statistical checks pass for the scoped implementation |
| G3: claim comparison | Every mandatory target compared using its own declared metrics and uncertainty; changed models/scales or unavailable targets explicitly classified |
| G4: reproducible evidence | Complete artifact/hash manifest and a successful clean-workspace rerun under the declared deterministic/statistical criteria |
| G5: independent acceptance | A distinct evaluator records identity/role, environment, command/results and discrepancies; required scientific/implementation review decisions are explicit and unresolved blocking errors are absent |

At each gate record passed, failed, blocked, not run or a justified not-applicable decision. A template is not evidence. A software agent evaluation must identify itself as such and cannot be represented as a human reviewer or a reader trial. A rerun by the original author is useful G4 evidence, not G5 independent acceptance. Automated CI supports G2/G4 and cannot silently sign G5.

Accept a **scoped claim reproduction** only when its mandatory claims meet the contracted scope and all applicable gates pass. Accept an **integrated paper reproduction** only when its registered mandatory claim set and the aggregate report satisfy the same gates. If the intended full scope was not achieved, label the result partial, blocked, inconsistent or inconclusive as appropriate. A scoped small-system result can be accepted in its scope; it must not inherit the original paper's larger-scale or hardware claim.

If a package is accepted but a new paper run is blocked, report both facts separately. Conversely, successful execution of a known paper does not establish a general L5 skill. L5 needs a pre-registered held-out paper suite with predeclared domain coverage, supported-task success criteria, false-success/incorrect-abstention limits, resource budgets, valid scientific dispositions and case-level evidence. No universal-reproduction rate or new agent benchmark result is claimed here.

## Changes, failures and capability gaps

Changing a target, approximation, seed/instance policy or acceptance budget creates a new protocol revision with a reason and impact record. Preserve the failed evidence; do not retroactively relabel it as a pass. Identify whether a discrepancy originates in source ambiguity, model translation, data, numerical error, compiler/runtime behavior or missing capability before making an upstream claim.

For a confirmed FlagQuantum gap follow the existing [investigation and issue workflow](implementation-roadmap.md). Preserve the independently executable reference and exact expected semantics while support is pending. A merged fix must be re-executed and reviewed on a named release/commit. Filing an issue or obtaining a matching plot does not complete acceptance.
