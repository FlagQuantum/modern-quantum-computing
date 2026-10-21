# One knowledge base, two entry points

The [scoped Ramsey paper-to-skills pilot](paper-ramsey-transfer.md) tests original-source translation, explicit pulse conventions, units and claim boundaries with the four existing prototypes. Scientific acceptance remains pending.

**Plan 0.1 · October 21, 2026 · first prototype pilot.** This document proposes a human textbook entry and an agent task entry for *Modern Quantum Computing: A Formula-to-Code Approach*. It changes neither Writing Baseline 1.0 nor its 50 chapters, 435 sections, seven volumes, 16 batches or proof-depth requirements. The [first comparison prototype](comparison-skill-prototype.md) has [independent blind-test evidence](comparison-skill-blind-evaluation.md); scientific acceptance remains pending. The second [interference prototype](interference-skill-prototype.md) is also independently agent-tested. The third [phase-tracked unitary evolution prototype](unitary-evolution-skill-prototype.md), based on 3.4–3.6, passed 53 author cases and 12 independent blind tasks, including unit clarification and actual coherent-control phase repair. The fourth [complex linear algebra prototype](complex-algebra-skill-prototype.md), based on Chapter 2, passed 57 author cases and nine fresh blind retest tasks after a numeric tail-metadata repair; its initial 12-task evidence and original failure are preserved. Its classical computations are separated from actual FlagQuantum execution routed to the evolution skill. No skill package is released.

The [four-skill composition experiment](four-skill-integration.md) now connects energy/time conversion, phase-tracked FlagQuantum evolution, interference readout and independent comparison. It passed 18 author cases and nine independent-agent blind tasks; staged state preparation and a continuous single-circuit path are recorded separately. This is an experiment workflow, not a fifth skill or independent scientific acceptance.

## Choose an entry

| Reader | Entry | Intended outcome |
|---|---|---|
| Human learner, instructor or researcher | [Textbook contents](contents.md), [learning routes](learning-paths.md) and [notation](conventions.md) | Understand assumptions and derivations, practice implementation and transfer the reasoning to new problems |
| Agent with a concrete task | [Capability and chapter map](agent-skills.md), [task contract](skill-contract.md) and relevant mathematical sources | Select a bounded workflow, implement it with declared conventions and return checkable artifacts |
| Reviewer of a paper reproduction | [Verification and acceptance standard](paper-reproduction-standard.md) and the run's claim ledger | Assess exactly which claims were reproduced, under which conditions and with which evidence |

The common goal is **paper claims → explicit models → FlagQuantum implementations → independently checked evidence**. Every supplied paper can be assessed for scope and feasibility. Successful execution of every quantum-related paper is not an unconditional promise. Theory proofs, numerical studies, complexity claims and device experiments require different evidence; some need unavailable artifacts or resources, or a model outside the current implementation scope.

## Share the scientific core

| Shared object | Human presentation | Agent use | Canonical location today |
|---|---|---|---|
| Definitions, assumptions, results and proof obligations | Explanatory prose with intermediate reasoning | Exact preconditions, invariant and source locator | `book/curriculum.json`, scholarly plan and stable section IDs |
| Conventions and mathematical semantics | Notation, worked examples and failure cases | Units, bases, qubit ordering, phase scope, shapes and output meaning | [Conventions](conventions.md) and the owning section |
| Implementation | Adjacent formula/code/output units and complete companion | Reusable implementation/reference, pinned versions and executable checks | `examples/`, requirements files and `book/formula-code-examples.json` |
| Evidence | Expected outputs, independent references and limitations | Actual logs, metrics, uncertainty, environment and artifact hashes | `book/section-records/` for current examples; future run-local evidence bundles |
| Learning/task dependencies | Readable prerequisite routes | Task-skill graph plus the selected source prerequisite closure | Existing textbook graph and proposed `book/agent-skills-plan.json` |
| Review decisions | Draft, scholarly review, reader trial and acceptance | Separate package, behavior and per-claim/run dispositions | Existing review records; proposed contracts linked below |

Keep one authoritative implementation for a given versioned mathematical contract. A skill should reference the owning theorem/formula and reusable code rather than copy a whole chapter or maintain a divergent formula implementation. The textbook remains understandable without an agent. An agent must be able to load the particular contract and relevant source reasoning without loading the entire book.

An internal equation that is reused by a task will receive a stable formula ID and code-symbol mapping when that task is implemented. This plan does not claim that every existing equation already has such an ID. Existing section IDs remain the stable navigation boundary; any later equation-ID additions must preserve public links.

## Organize skills around tasks

A chapter can support several tasks, and a task can import several chapters. For example:

- Comparing two statevectors uses complex inner products, finite-output validation, pure-state equivalence and phase scope from 2.1–2.2, 2.8, 3.1 and 3.7. Comparing whole operators also needs the factorization/common-phase distinctions of 3.6.
- Reproducing an interference probability uses 3.1–3.2, matrix order from 2.3 and explicit numerical contracts from 2.8. It must state the preparation and analyzer, not merely match a cosine curve.
- Reproducing molecular VQE eventually composes operator provenance, chemical model reduction, measurement, differentiation, optimization and independent reference energies across Chapters 23–25, 48–49 and their actual prerequisites.
- A physical-platform paper can require controls, leakage/loss, calibration and experimental data from Chapters 34–40. A qubit-only simulation is a scoped model study unless the stronger experimental conditions are actually met.

The [six capability levels and complete chapter map](agent-skills.md) assign primary responsibility for every planned section. These assignments are an editorial overlay, not changes to the textbook dependency graph. L0–L5 levels describe task composition; P/F/M/R/V still describes mathematical depth. The agent entry must preserve that depth rather than replace derivations with procedural instructions.

## Proposed repository presentation

| Artifact | Purpose | Status in this update |
|---|---|---|
| `docs/dual-entry.md` | Human/agent navigation and shared-source policy | Planning document |
| `book/agent-skills-plan.json` | Six levels, 23 proposed task skills, dependencies and full section assignments | Validated planning catalog |
| `docs/agent-skills.md` | Generated capability map, chapter mapping and candidate evidence | Planning view; zero released skills |
| `docs/skill-contract.md` | Task/package contract and behavior evaluation requirements | Planning specification |
| `docs/paper-reproduction-standard.md` | Per-claim verification, scientific outcomes and acceptance gates | Planning specification |
| `templates/skill-design.md` and `templates/paper-reproduction-report.md` | Reviewable design and evidence-report worksheets | Unfilled templates; no claimed run |
| `skills/compare-quantum-states-and-operators/SKILL.md` and its contract/helper | First discoverable execution entry | Independent-agent-tested prototype 0.1.1; not installed globally or scientifically accepted |
| `skills/reproduce-qubit-interference/SKILL.md` and its reference/helper | Ideal one-qubit scan with explicit preparation, units and analyzer | Independent-agent-tested prototype 0.1.0; no accepted release |
| `skills/translate-unitary-evolution/SKILL.md` and its reference/helper | Constant generator, Pauli rotation and phase-tracked ZYZ factorization with declared units/context | Independent-agent-tested prototype 0.1.0; no accepted release |
| `skills/translate-complex-linear-algebra/SKILL.md` and its reference/helper | Chapter 2 classical complex algebra, strict metadata/tolerance contracts and conditioned diagnostics | Independent-agent-tested prototype 0.1.1; no accepted release |
| Future `reproductions/<paper-id>/<run-id>/` bundles | Inputs, implementation, environment, actual evidence and review decisions | Not created or fabricated in this pass |

A future `SKILL.md` contains concise discovery metadata, scope, essential invariants, routing and links. Detailed math stays in the source sections; conditional procedures and schemas are loaded as needed. Runtime adapters may differ, but the scientific task/output contract is shared. Instructions do not grant permission to submit hardware jobs, spend resources, upload sources or post external messages.

## Pilot sequence and release conditions

First design and evaluate state/operator comparison, then the bounded interference experiment, then phase-tracked unitary evolution. Existing author-executed examples provide candidate fixtures; they are not evidence that a skill can solve an unseen task. Use independent expected results, negative cases and held-out variants that expose phase, sign, operation-order and endpoint mistakes.

After those pilots, evaluate one explicitly scoped paper claim. Only then assemble a registered multi-claim reproduction. The existing hydrogen starter remains a candidate laboratory; a checked reduced Hamiltonian is not by itself a full molecular or whole-paper reproduction. Broader domain skills are developed as their exact source obligations, implementations and genuine release capabilities become available.

A future skill is released only with a versioned task contract, verified imports, actual behavior evidence and an explicit independent acceptance decision. Author-verified prototypes may cite explained source drafts if their limitations are visible and no blocking error is known. They remain prototypes. Skills do not inherit acceptance from a green CI run or from a chapter heading. Textbook acceptance continues to require its own mathematical, implementation and reader review.

## Maintenance and checks

Run the catalog generator whenever its plan or source progress changes:

```bash
python scripts/build_agent_skills_plan.py
python scripts/build_agent_skills_plan.py --check
python scripts/build_writing_baseline.py --check
python scripts/review_curriculum.py --check
python -m mkdocs build --strict
```

The catalog check verifies all 435 assignments, canonical source IDs, chapter ownership, dependency acyclicity, candidate-evidence paths and truthful planning status. It does not test agent competence or scientific claims. Example execution continues through `python scripts/check_formula_code.py` and the existing CI. The comparison and interference helpers are implemented and independently agent-tested. No new textbook section, paper run, upstream issue, arXiv submission or PDF edition is part of this prototype update.
