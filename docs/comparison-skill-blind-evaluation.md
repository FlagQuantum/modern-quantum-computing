# State/operator skill: independent agent blind evaluation

**October 21, 2026 · prototype 0.1.1 · independent agent behavior evaluated; scientific acceptance pending.** This follows the [first prototype](comparison-skill-prototype.md), based on textbook 3.1 and 3.7. No new textbook section is written.

[Current skill](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/skills/compare-quantum-states-and-operators/SKILL.md) · [Complete graded report](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/skill-evaluations/state-operator-blind-2026-10-21/report.json) · [Frozen evidence bundle](https://github.com/FlagQuantum/modern-quantum-computing/tree/main/book/skill-evaluations/state-operator-blind-2026-10-21)

## What was blind and independent

Nine distinct agents were started with **no inherited conversation history**, in three groups of three. They were not the authoring/conducting agent. Each received a private working directory containing only its raw tasks, a catalog of 23 skill descriptions with one available implementation, and a frozen copy of the relevant skill package. No reference answers, suspected defect or previous conclusions were supplied. The final round also supplied two available interpreter paths without labeling which one met the contract.

The agents selected a skill or declined it, chose the mathematical context, asked questions when needed, ran the helper, saved actual requests/stdout/stderr/exit codes and wrote their own verification code and explanations. The conductor answered clarification questions with the caller's intended context, not a residual or expected decision. Reference dispositions and analytic targets were stored outside the agents' permitted workspaces before dispatch. [Invocation prompts](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/skill-evaluations/state-operator-blind-2026-10-21/agent-invocations.json), question/reply records, input hashes and raw artifacts are preserved.

These were logically restricted workspaces, not OS-enforced secret isolation. The agents inherited the same model configuration; exact backend revisions and token/cost telemetry were not exposed. This is a small conductor-designed evaluation, not a cross-model study, security test or statistical competence estimate. There was only one implemented skill to choose; rejecting an irrelevant skill was tested, competition among multiple implemented skills was not.

## A real issue found and repaired

In the first two rounds, the agents made the expected mathematical decisions on all 16 tasks. A post-run environment audit nevertheless found that **all 14 helper invocations used system Python 3.9.6**, while the package declared Python 3.12 as its validated profile. Version 0.1.0 did not reject this runtime or report it in the structured result. The first two rounds are therefore **not recorded as complete passes**. Their original evidence and the old package snapshot remain intact.

Version **0.1.1** repairs this contract gap:

- The CLI checks for **CPython 3.12** before parsing a comparison request. An incompatible runtime returns `unsupported`, exit 3, with reason `unsupported_runtime`; it does not certify an object comparison.
- Every CLI result records the actual Python implementation and version.
- The skill instructs an agent to check and explicitly select a compatible interpreter rather than assume that `python` or `python3` meets the profile. If none is available, it reports the environment boundary without silently installing or changing software.

The state/operator comparison mathematics is unchanged. [Actual admission checks](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/skill-evaluations/state-operator-blind-2026-10-21/runtime-admission.json) show Python 3.9.6 being rejected and CPython 3.12.14 producing the requested comparison. No numerical discrepancy was observed in the old runs; that does not justify silently extending the validated runtime.

## Fresh tasks after the repair

Three **new** agents received version 0.1.1 and eleven **new** tasks, without the old answers or defect explanation. They independently selected CPython 3.12.14. The final round passed **11/11 tasks**, including all six supported numerical comparisons; all eight actual helper invocations recorded the required runtime.

| Task(s) | Obligation | Observed result |
|---|---|---|
| G1 | Ambiguous “same state” | Asked about coordinate versus global-phase equivalence and tolerance before the dependent decision; used the caller's reply and verified equivalence |
| G2 | Complex relative phase with equal basis probabilities | Detected distinct rays; residual about 0.5350379316 |
| G3 | Nonunit state supplied without permission to repair | Rejected invalid input; preserved arrays |
| H1 | Scalar phase on a target inside coherent control | Compared the full controlled operation; residual about 0.8074139694 |
| H2 | Four-dimensional isolated unitary with one whole-operator phase | Verified within tolerance without per-column alignment |
| H3 | Bernoulli counts | Declined the pure-state skill; computed the proportion and standard error without inventing amplitudes |
| I1 | Different supplied basis declarations | Reported unsupported scope without guessing a permutation |
| I2, I3 | Incorrect cached success and incorrect cached failure | Reran from raw arrays and corrected both directions of cached error |
| I4 | Mixed-state density matrices | Declined unsupported certification without substituting a statevector |
| I5 | Unverified batched complex64 producer export | Rejected admission without dtype widening, reshaping or claimed producer verification |

Final-round categories are **6 supported comparisons, 1 invalid input, 3 unsupported profiles and 1 off-profile calculation**. The supported comparisons include three within-tolerance and three outside-tolerance results. There were **zero false successes and zero incorrect abstentions** under the registered task contracts. Unsupported inputs are reported separately rather than counted as successful state/operator comparisons.

| Round | Package | Agents / tasks | Task decisions | Runtime conformance | Overall disposition |
|---|---|---|---|---|---|
| r1 | 0.1.0 | 3 / 10 | 10 correct | 0/8 helper calls met declared runtime | Failed post-run runtime audit |
| r2 | 0.1.0 | 3 / 6 | 6 correct; added positive equivalence coverage | 0/6 | Failed post-run runtime audit |
| r3 | 0.1.1 | 3 / 11 | 11 correct on fresh tasks | 8/8 | Passed this bounded behavior evaluation |

Across all rounds, three ambiguous tasks prompted clarification. The initial coordinate-preserving clarification and isolated-operator clarification are preserved alongside the final isolated-state clarification. Independent agent scripts check norms, Gram matrices, scalar/trace distance identities and, for the initial controlled/gate cases, coherent-input witnesses. The conductor additionally checks analytic targets and preserved arrays. These numerical checks do not replace the source proofs or establish general algorithm equivalence.

## Evidence, replay and remaining review

The bundle preserves 27 raw tasks, both package snapshots, reference keys, all agent outputs, actual commands and statuses, verification scripts and the conductor's grades. Immutable file hashes connect these artifacts. The cases are now public: **replaying them is regression checking, not another blind evaluation**. Future claims of held-out agent competence require new tasks and fresh agents.

Run with the example environment's CPython 3.12 interpreter:

```bash
python scripts/check_comparison_skill.py
python scripts/check_blind_comparison_evidence.py
python scripts/build_agent_skills_plan.py --check
python -m mkdocs build --strict
```

The first command reruns **45 author regression cases and three actual released FlagQuantum 0.3.1 executions** for 0.1.1. Its six former transfer cases are now labeled regression, not fresh held-out evidence. The second checks frozen inputs/hashes, recorded routing and clarification, analytic targets, runtime metadata and **22 recorded helper requests** across all rounds. It runs deterministic replays from temporary directories. CI does not launch new agents or fabricate new blind-test results.

The package is now an **independent-agent-tested prototype**, not an accepted or released skill. The author/conductor graded the artifacts; independent human mathematical/implementation acceptance and reader trials remain pending. Textbook source states, all 435 section assignments, prerequisite relationships, proof-depth requirements, seven volumes and the PDF edition are unchanged. This bounded L1 result makes no claim about arbitrary-paper reproduction or broader L4/L5 competence.
