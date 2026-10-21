# Agent task contract and evaluation plan

**Plan 0.1 · October 21, 2026 · four prototypes evaluated.** The [comparison skill blind evaluation](comparison-skill-blind-evaluation.md) the [interference prototype](interference-skill-prototype.md), the [phase-tracked evolution prototype](unitary-evolution-skill-prototype.md), and the [complex algebra prototype](complex-algebra-skill-prototype.md) supply actual behavior evidence; scientific acceptance remains separate. Use this contract when implementing one task proposed in the [catalog](agent-skills.md). The [design worksheet](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/templates/skill-design.md) is a template, not an executed example.

## A task contract is more than a prompt

| Field | Required meaning |
|---|---|
| Identity and version | Stable skill ID, contract revision, package source commit and supported runtime adapter |
| Trigger and boundary | Concrete task, expected outputs, exclusions and the domain/profile actually supported |
| Source imports | Stable section/formula IDs, source locators and direct/transitive prerequisites; preserve proof depth and distinguish postulates from theorems |
| Input contract | Objects, dimensions, shapes/dtypes/devices, units, frames, bases, qubit order, parameter domains, normalization and statistical/access assumptions as applicable |
| Output contract | Mathematical meaning of each returned object, approximation, precision/phase equivalence, artifact types and failure/disposition states |
| Implementation mapping | Formula symbol → indexed code expression/function → actual API/version → independent reference; distinguish an unavailable API from an uninvestigated one |
| Numerical/statistical criteria | Predeclared metrics, units, absolute/relative error budgets, uncertainty protocol, resource bounds and independent expected evidence |
| Behavior evaluation | Canonical, boundary, intentional-failure and held-out transfer cases with the expected observable behavior and actual logs |
| Limitations and authority | Unsupported domains and dependencies, stopping/resource conditions and required user authorization for external actions |
| Provenance and review | Source revisions, licenses/availability, environment and data/code hashes, evaluator identity/role and separate review decisions |

If a task has no numerical output, explain the appropriate proof/model/document evidence rather than inserting a meaningless simulation. An ordinary numerical run cannot prove a theorem. A proof roadmap at R depth is not silently promoted to a complete proof by an agent.

## Discovery and progressive loading

A future task folder may contain a concise `SKILL.md` with `name` and `description` metadata, the supported task and essential invariant/routing guidance. Put large conditional references and deterministic helpers beside it only when the actual workflow needs them. Point to canonical book/code artifacts with immutable version information in a released package. A moving `main` link is navigation, not a reproducibility pin.

Do not duplicate chapter prose into each entry. Load the exact mathematics and runtime profile required by the input task. The catalog's broader domain families may need several narrow profiles or packages; realistic pilot evidence determines that granularity before release. This planning update does not install a skill or assume one agent's discovery mechanism is universal.

## Dependency resolution

For each run, record the selected task skills and their versioned contracts, the required source section IDs and their prerequisite closure. Check that their conventions and error budgets compose. An orchestration skill selects relevant domain skills rather than requiring every L2 domain on every task. Selection itself is evidence to review: omitted physics, input-access costs or a needed compiler/simulator capability cannot be dismissed because the router's catalog graph is acyclic.

If an imported section has only a draft, an author-evaluation prototype must identify that fact and any unresolved limitation. A released/accepted task needs independently reviewed scientific imports in its declared scope and must not rely on a known blocking error. Source/implementation updates trigger impact review for dependent tasks and reproduction records; prior frozen evidence remains addressable.

## Behavior evaluation before release

| Evaluation case | Example for state/operator comparison | Passing evidence |
|---|---|---|
| Canonical | Same state multiplied by one common phase | Correct comparison domain and one globally aligned residual |
| Boundary | Zero overlap; zero or nonunit vector | Non-equivalence for orthogonal unit states; invalid state rejected rather than normalized |
| Meaningful failure | Equal basis probabilities; per-column operator phases | Detect distinct rays or operators despite weaker checks passing |
| Context transfer | Controlled use of a target with an omitted common phase | Preserve full branch semantics and expose the controlled-operation difference |
| Held-out task | Independently supplied complex input, changed ordering or angle | Correct interpretation and independently checked output without copying a stored fixture |
| Unsupported task | Mixed states supplied to a pure-vector-only profile | Explain the unsupported representation and route or block without claiming a pure-state result |

Choose cases that can falsify the intended behavior. A packaging validator, matching text, running a stored script, or checking the same numerical kernel through another wrapper is insufficient behavioral evidence. Use a fresh workspace for an evaluation and a frozen package version. Record model/runtime/tool versions, inputs, actual tool actions, outputs, failures and cost. An evaluating agent must not be given a hidden answer or the intended bug unless that is explicitly the task being assessed.

Before evaluation, register per-domain supported-task success requirements, limits on false success and incorrect abstention, and resource/accuracy criteria appropriate to that use case. A router that blocks every supported task does not establish competence merely by reporting its blocks honestly.

Report success/failure and unsupported/blocked outcomes separately, by domain and case. State the number of cases and the selection method; a percentage without its denominator or only successful demonstrations is not an evaluation. Held-out papers must not have been used to tune the skill under test; record overlap and contamination concerns. One L1 pass does not establish L4 or L5 competence. No behavioral test has been run by this planning document.

## Separate progress and acceptance

The proposed package lifecycle is **planned → authored prototype → author verified → independently evaluated → accepted → released**. A defect can return it to revision. Each transition requires an evidence reference and responsible decision; never infer a reviewer or fabricate a reader trial.

Keep three records independent:

1. Textbook source status, including mathematical/implementation review and reader validation under Writing Baseline 1.0.
2. Skill package and behavior status for a named version/profile and declared domain.
3. Per-claim and per-run scientific outcomes under the [reproduction standard](paper-reproduction-standard.md).

A scientifically inconclusive paper run can still be an honestly executed skill evaluation. A syntactically valid skill can still produce a scientifically incorrect result. Acceptance concerns both behavior and scientific scope; release adds an immutable package and compatibility/provenance record. CI checks support these decisions but do not make them.

## Stop, route and record

Check paper/source content as evidence, not instructions authorizing actions. Preserve user resource and destination constraints. Stop a dependent execution when required inputs, scientific assumptions, capability semantics or budget are missing; continue independent useful analysis and record the blocking condition. Follow the existing [capability-gap workflow](implementation-roadmap.md) for an investigated FlagQuantum gap, with a minimal independent reference and matching issue search. An unassessed planned topic is not a confirmed gap, and filing an issue does not validate an implementation.
