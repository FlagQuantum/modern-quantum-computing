# FlagQuantum capability gaps and implementation workflow

The textbook's theory and learning outcomes determine implementation requirements. A missing API must not remove an important subject from the [curriculum](book-plan.md). Confirmed capability gaps are reported to [flagos-ai/FlagQuantum](https://github.com/flagos-ai/FlagQuantum/issues), using the [issue specification template](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/templates/flagquantum-capability-gap.md).

## Separate three kinds of status

| Record | Example statuses | Meaning |
|---|---|---|
| Chapter | Planned; draft; mathematically reviewed; teaching pilot; edition-ready | Progress of explanation, proofs, problems and learning review |
| Capability | Not assessed; existing; gap confirmed; issue linked; implemented; released | Evidence about the required software behavior |
| Experiment | Reference only; FlagQuantum pending; executed on a named release; independently verified | Actual execution and verification evidence |

A merged implementation does not certify an example, and an API's absence in one stable release does not establish absence on the development branch. Always record which revision was examined.

## Investigate and report a concrete requirement

1. Identify the chapter, formula, mathematical object and smallest educational experiment.
2. Inspect the relevant stable release and current upstream source, tests and documentation. Search open and closed issues before opening another. Record dates, versions, source paths and relevant existing interfaces.
3. Build the smallest independent executable reference that captures the intended semantics. For large problems, provide a mathematically specified acceptance case and a tractable test instance.
4. Classify the finding: supported but undocumented; documentation/example defect; incorrect behavior; missing API; missing algorithm/backend; performance or scalability requirement.
5. Reuse a matching issue or file a focused issue upstream. Include observed behavior, proposed semantics, the mathematical reference, minimal input, expected result and tolerances, and correctness/error/resource acceptance criteria.
6. Link the issue from the chapter's implementation status and a capability record. Preserve the chapter and independent calculation while implementation is pending.
7. After implementation, run the textbook example on a named commit or release, check independent references and limits, and record the evidence. Update compatibility notes and release/migration instructions.

Do not infer missing support from a curriculum heading or invent an API to make a code block appear complete. No upstream issues are claimed as opened by this planning document.

## Requirements to investigate as chapters are drafted

These are **unassessed curriculum requirements**, not confirmed software deficiencies.

| Chapters | Required behavior to investigate | Acceptance-case direction | Capability status |
|---|---|---|---|
| 6–10, 28 | Conditional measurements, channels/instruments, reduced states and density evolution | Compare probability, conditional state and channel action with independent finite matrices | Not assessed |
| 10 | Measurement estimators, basis changes and shadow-style workflows | Seeded estimators with declared measurement ensemble, uncertainty and independent state reference | Not assessed |
| 18–22 | Modular arithmetic, controlled operations, block encodings and signal-processing sequences | Check tiny exact blocks/distributions and polynomial constraints before resource experiments | Not assessed |
| 23–27 | Shared-parameter derivatives, differentiation modes, geometry and hybrid models | Multiple parameter occurrences; dense/analytic gradient checks; execution and memory accounting | Not assessed |
| 29–33, 45, 50 | Stabilizers, adaptive/repeated syndrome measurements, decoder interchange and logical observables | Small-code dense equivalence, enumerated faults and repeated-round detection events | Not assessed |
| 34–40 | Physical levels/modes, effective Hamiltonians, driven controls, readout, leakage/loss and constraint records | Truncation convergence, frame/unit checks and complete model-to-observable references | Not assessed |
| 41–43 | Program/IR semantics, compiler passes, synthesis, mapping/routing, timing, dynamic control and target lowering | Exact/conditional-map equivalence, legality, output mapping and explicit approximate-error contracts | Not assessed |
| 44, 46–47 | Exact/approximate executors, truncation records and contraction/resource reporting | Known exact states, explicit approximation settings and independently checked error/cost metrics | Not assessed |
| 48–50 | Experiment records, deterministic replay and result/uncertainty export | Reproduce a declared claim from pinned inputs with provenance and discrepancy reporting | Not assessed |

Issue granularity follows the actual architecture. A high-level scientific protocol may use existing composable operations and need only a textbook implementation. Do not request a new framework API for every chapter.

## Capability record

For each investigated requirement, store: stable ID; chapter/section/formula; status; audited release and upstream commit; existing source/test links; independent reference; upstream issue/PR; acceptance criteria; validated textbook example and execution environment; last review date. Use TBD explicitly for unknown fields, and update the record when evidence changes.

The author has authorized filing confirmed missing capabilities in the upstream repository. This workflow does not request extra approval for each such issue; it requires a concrete, deduplicated engineering report.
