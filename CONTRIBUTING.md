# Contributing

Open an issue for a substantial chapter proposal, or submit a pull request for a focused correction. Use English prose, explicit conventions, and the chapter template.

- Follow the [editorial charter](docs/editorial-charter.md): the subject determines scope; investigate required missing functionality through the [capability-gap workflow](docs/implementation-roadmap.md).
- State central results precisely, supply proofs or explicit deferred-proof maps, and provide meaningful transfer problems and counterexamples.
- Cite primary sources with exact versions and data origins. Reuse or add stable keys in `docs/references/references.bib`; give section/equation locators in the chapter and update the reading guide and mapping as needed.
- Link to official third-party resources rather than committing textbook PDFs, scans or solution manuals. Record an explicit reuse basis and attribution for any third-party material included.
- Link runnable Python programs; keep expected output reproducible.
- Check important identities independently of the FlagQuantum execution path.
- Report software versions, devices, precision, tolerances and seeds.
- Label planned, unverified, approximate and hardware-specific material accurately.
- Build the documentation with `python -m mkdocs build --strict` and run affected examples before submitting.
- Preserve source attribution and ensure you have rights to contributed material.

Contributions are provided under the applicable repository license: CC BY 4.0 for prose/original illustrations and MIT for code. Report code problems through an issue with a minimal reproducer and environment details. Never include credentials or private data.
