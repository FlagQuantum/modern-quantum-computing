# Source scope for the systematic architecture review

The subsequent [all-section proof/source plan](../proof-plan.md) and [version-specific source catalogue](proof-sources.md) supply exact source targets. The scoping notes below retain their original review scope; locator assignment is not proof approval.

**Reviewed October 20, 2026.** These comparisons informed coverage and sequencing decisions in the [editorial review](../architecture-review.md). The pass inspected official course/notes indexes and the linked papers' abstracts/metadata. It did not verify every source proof, benchmark or implementation. Exact theorem/equation-level reading is required before section acceptance. No source book, exercise set or page image is redistributed.

## Official educational scope comparisons

| Source actually consulted | Design implication |
|---|---|
| [Preskill, Quantum Computation lecture notes: official index](https://www.preskill.caltech.edu/ph219/) | Information theory, computational models, error correction and fault tolerance form substantial connected routes. Local mathematics and proof obligations cannot be replaced by algorithm demonstrations. The index is not evidence that every chapter was read. |
| [Childs, CMSC 657, Fall 2025: official course overview](https://www.cs.umd.edu/class/fall2025/cmsc657/) | Compare algorithms, complexity, mixed operations, information, error correction and security as a connected graduate scope rather than a list of current applications. |
| [IBM, Fundamentals of Quantum Algorithms: course overview](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms) | Check oracle/search/Fourier structure and the entry contract of a first algorithm course. |
| [IBM, Foundations of Quantum Error Correction: course overview](https://quantum.cloud.ibm.com/learning/en/courses/foundations-of-quantum-error-correction) | Check code/stabilizer/fault-tolerance progression and distinguish elementary code experiments from full logical computation. |

Earlier targeted [Nielsen–Chuang](nielsen-chuang-design-review.md) and [Quantum Country](quantum-country-design-review.md) analyses remain separate design records. This review adds dependency closure, workload and whole-curriculum ownership decisions; it does not claim to surpass those works on the basis of topic count.

## Primary-paper anchors for scoped omissions

| Anchor | What it supports in the plan | What remains to be checked |
|---|---|---|
| [Suzuki et al., Amplitude Estimation without Phase Estimation](https://arxiv.org/abs/1904.10246) | A phase-free likelihood example can precede QPE; QPE-based amplitude estimation can follow QPE. | Exact model, estimator/ambiguity handling, schedules and finite-sample guarantees; no blanket speedup claim. |
| [Magesan, Gambetta and Emerson, Scalable and Robust Randomized Benchmarking](https://arxiv.org/abs/1009.3639) | Device characterization needs a distinct experimental-model home beyond tomography and runtime timing. | Gate-ensemble/twirling bridge, noise dependence, fit/identifiability and SPAM scope. |
| [Bravyi et al., High-threshold and low-overhead fault-tolerant quantum memory](https://arxiv.org/abs/2308.07915) | Quantum-LDPC/connectivity tradeoffs deserve a selected modern coding section. | Construction/proof assumptions, decoder/noise models and a fair resource comparison; no universal code ranking. |
| [Watrous, Quantum Computational Complexity](https://arxiv.org/abs/0804.3401) | Make promise, verification and QMA boundaries visible alongside algorithm claims. | Exact selected results and proof prerequisites; a scoped bridge is not a full complexity course. |
| [Kimble, The Quantum Internet](https://arxiv.org/abs/0806.4195) | Shared entanglement/link/network primitives should connect protocol and modular-hardware discussions. | Exact swapping/distillation models and costs; not a commitment to a full network engineering stack. |
| [Albert, Bosonic coding: introduction and use cases](https://arxiv.org/abs/2211.05714) | Oscillator encodings and bosonic protection need an explicit optional bridge. | Truncation, finite-energy/error assumptions, syndrome models and precise code claims. |

## Section-local source record before drafting and acceptance

For each central claim, record the section's stable ID, source edition/revision, exact theorem/equation/page locator, assumptions, proof versus deferred-proof scope, locally supplied bridges, independent small check and source-review date. Hardware maturity comparisons need dated claim-specific evidence. A source title or abstract supports planning, not a completed derivation or an execution claim.
