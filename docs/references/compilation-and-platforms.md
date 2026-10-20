# Source anchors for compilation and physical platforms

**Scoping date: October 20, 2026.** These author-written notes identify research and official specifications for the added curriculum. The scoping pass checked bibliographic abstracts/overview information and official documentation scope; it is not a complete reading or proof review of these works. Exact chapter-level theorem/equation locators and later evidence remain to be selected.

Historical reviews can establish concepts and models. They cannot establish present device performance or the scientific maturity of a candidate platform.

| Route | Author reference or official specification | Intended editorial use |
|---|---|---|
| Superconducting | [Krantz et al., A Quantum Engineer's Guide to Superconducting Qubits](https://arxiv.org/abs/1904.06560) | Effective circuits, qubit design, control, noise and readout |
| Trapped ions | [Bruzewicz et al., Trapped-Ion Quantum Computing: Progress and Challenges](https://arxiv.org/abs/1904.04178) | Physical encodings, motion/control and architectural constraints |
| Neutral atoms | [Henriet et al., Quantum computing with neutral atoms](https://quantum-journal.org/papers/q-2020-09-21-327/) | Explicit digital/analog models and their interfaces; performance claims stay dated |
| Photonic operations | [Knill, Laflamme and Milburn, Efficient Linear Optics Quantum Computation](https://arxiv.org/abs/quant-ph/0006088) | Conditional optical operations, detection and feed-forward |
| Photonic resource states | [Bartolucci et al., Fusion-based quantum computation](https://arxiv.org/abs/2101.09310) | Entangling measurements, resource states and model-specific error/erasure accounting |
| Semiconductor spins | [Burkard et al., Semiconductor Spin Qubits](https://arxiv.org/abs/2112.08863) | Effective spin models, control, readout and coupling/scaling assumptions |
| Topological models | [Nayak et al., Non-Abelian Anyons and Topological Quantum Computation](https://arxiv.org/abs/0707.1889) | Fusion/braiding structure, proposed encodings and protection assumptions; not evidence of a current universal device |
| Mapping/routing | [Li, Ding and Xie, Tackling the Qubit Mapping Problem for NISQ-Era Quantum Devices](https://arxiv.org/abs/1809.02573) | A concrete heuristic to compare with exact tiny-instance references |
| IR and transformations | [Quantum Circuit Transformations with a Multi-Level Intermediate Representation Compiler](https://arxiv.org/abs/2112.10677) | Staged representation and transformation responsibilities |
| Program semantics/interchange | [OpenQASM specification](https://openqasm.com/) | Classical control, types, timing and explicit representable subsets; pin a specification version during drafting |
| Target-routing interface | [Cirq qubit routing documentation](https://quantumai.google/cirq/transform/routing_transformer) | An official example of logical-to-physical mapping contracts and routing output interpretation |

Before drafting, choose exact source revisions and result locators, record assumptions and counterexamples, and review proposed numerical acceptance cases. Platform data sheets or marketing summaries require independent claim-specific evaluation; the book does not adopt performance rankings from this scoping exercise.

The [curriculum audit](../curriculum-audit.md) identifies what still needs review; the [reader-continuity standard](../reader-continuity.md) governs how these sources become original explanations.
