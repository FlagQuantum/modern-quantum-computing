# Editorial charter: a modern classic that remains useful

**Adopted October 20, 2026.** Author's educational direction: serve present and future young people entering quantum computing, with the ambition of a modern classic.

A classic earns that description through sustained scholarly and teaching use. This charter sets working standards; it makes no guarantee of future recognition or permanent completeness. The [curriculum](contents.md) is organized around durable ideas and their relationships, with an accessible entry and substantial advanced routes.

## The subject sets the scope

Select material for explanatory importance, mathematical coherence and educational value. Existing FlagQuantum functionality does not determine the boundaries of the textbook. Required missing capabilities become investigated implementation requirements and, when confirmed, issues in [flagos-ai/FlagQuantum](https://github.com/flagos-ai/FlagQuantum/issues). The [capability-gap workflow](implementation-roadmap.md) defines the evidence and acceptance standard.

FlagQuantum is the primary executable implementation. A chapter must retain a mathematically complete explanation, explicit assumptions, and an independent reference. Unsupported code is never presented as a working API. Pending implementation does not prevent theory, proofs, problems or independent reference programs from being developed.

## Three layers with different rates of change

| Layer | Contents | Maintenance rule |
|---|---|---|
| Foundational argument | Definitions, postulates, theorems, proofs, models, resource/error reasoning | Stable notation and problem IDs; corrections have public errata and edition provenance |
| Executable companion | FlagQuantum examples, independent references, pinned environments, verification records | Validate supported releases; publish migrations and preserve previous edition environments |
| Research laboratories | Recent methods, selected paper reproductions, device results and competing approaches | Date claims, state evidence and limits, review sources and replace obsolete comparisons |

Important modern theory belongs in the foundational argument when it supplies a coherent, durable conceptual framework. The research layer is not an excuse to omit QSVT or fault-tolerant computation from the substantive curriculum.

Stable scientific facts do not expire because an API changes. Assumptions, open problems and empirical claims may change; the text must make those distinctions visible.

## Mathematical and scientific standard

- State the problem, quantifiers, access model and assumptions before a result.
- Provide proofs of central results at the declared reading level, including meaningful intermediate steps.
- For a deferred advanced proof, give the exact theorem, a proof roadmap, prerequisites and precise source locations.
- Connect important equations to indexed, dimensioned and normalized code expressions.
- Analyze accuracy, success probability, sampling, approximation, optimization and resource cost where relevant.
- Include a counterexample, limiting case or failure analysis that exposes why an assumption matters.
- Distinguish mathematical proof, numerical evidence, controlled experiments and physical hardware observations.

A small verified calculation is valuable implementation evidence. It does not establish a general theorem, an asymptotic speedup, hardware performance or a cryptographic security guarantee.

## Educational standard

Readers should progress from intuition to precise statements, from worked cases to transferable reasoning. Provide Core, Advanced and Research routes, mathematical bridges and explicit dependencies. Keep substantial problems and selected solutions alongside short recall/prediction prompts. Evaluate clarity with target readers; use instructor feedback to test whether a course route works.

Use **qubit** consistently for the quantum information carrier and circuit indices, labels and ordering. Essential teaching material remains readable without an account, paid hardware, a network session or an interactive widget. Web and print communicate the same scientific argument.

## Planning and explanatory continuity

The [curriculum audit](curriculum-audit.md) sets coverage, prerequisite, workload, specialist-review and reader-test gates before the architecture is frozen. Physical models and quantum compilation are substantive main-text routes. Stable identifiers and a change record control later reorganizations.

The [reader-continuity standard](reader-continuity.md) requires local bridges, defined symbols, justified intermediate steps and clear section transitions. Phrases such as “obviously” or “well known” cannot discharge an explanation or proof. A central argument is not silently assigned to the reader.

## Longevity, review and editions

1. Before accepting a chapter, obtain mathematical, implementation and reader review. Record the review scope; automated checks alone are insufficient.
2. Before a release, check references, notation, prerequisites, proofs, problems, examples, links and web/print rendering.
3. Preserve published source revisions, data provenance, environments and manifests. Publish corrections rather than silently changing a frozen edition.
4. At least once per year, review the curriculum for significant theoretical developments, revised evidence, obsolete examples and missing learning bridges. This is an editorial policy, not a configured automatic reminder.
5. Review a chapter earlier when a mathematical error, source correction, API change or important contrary result is reported.
6. Keep dated research claims and software compatibility separate from durable mathematical statements. Add topics when they improve understanding; reorganize or retire material when evidence warrants it.

## Evidence of progress toward the ambition

Track completion and independent review of coherent learning routes, success on transfer problems, instructor adoption, reproducibility by readers, and resolution of conceptual errors. Repository popularity and chapter count do not establish educational or theoretical quality.

The immediate milestone is a reviewed, versioned architecture baseline, with exact source/proof maps, workload decisions and specialist/reader evidence. New body and depth-pilot drafting is paused until that gate. After the baseline, develop a coherent opening and three depth pilots: measurement (Chapter 6), quantum differentiation (23), and correction conditions (29). These test whether the approach can teach postulates, spectral arguments and a substantial theorem before the entire book is written.
