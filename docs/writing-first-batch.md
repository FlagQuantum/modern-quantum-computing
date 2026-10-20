# First writing assignment: Chapter 1

**writing-baseline-v1.0 · six prepared authoring briefs; actual work states and body links below.** [Writing baseline](writing-baseline.md) · [Full queue](writing-order.md).

The initial sequence is 1.1–1.6. Use the current queue states to continue from the next undrafted section. Chapter 1 is an entry and preview: it must supply its own minimal arithmetic and notation without importing unproved results from later chapters. The formal mathematics, state postulates, gates and measurement theory will be developed in their named owning chapters. The preview must say what is being adopted and what will be derived later.

## 1.1 Problems, inputs, and observable outputs

**Stable ID:** `sec-what-quantum-computing-computes-1`. **Depth:** P. **State:** draft.

[Read the working draft](chapters/ch-what-quantum-computing-computes.md#sec-what-quantum-computing-computes-1). Independent acceptance remains separate.

**Concrete question:** What can a computation be asked to return?

**Entry knowledge:** Basic Python variables, lists and the distinction between a question and one input instance.

**Exit skill:** Specify input representation, observable output, success criterion and resource boundary for one task.

**Worked-case plan:** A bitstring task versus a repeated-sampling expectation-estimation task; state which quantities are outputs and which are model internals.

**Scope/continuity boundary:** No new quantum law is asserted. Distinguish a sample, an estimated statistic and simulator-only state inspection.

**Formula-to-code plan:** Complete reference: examples/foundations/task_contracts.py; standard library only, no quantum backend required.

**Independent check:** A classical enumerated reference and a deliberately mismatched output contract.

**Transfer task:** Give a new task and ask the reader to identify what must be measured and how success would be checked.

**Assigned exact sources:** [NC:3.2.1](references/proof-sources.md#source-nc-3-2-1). Source assignment is not independent proof review.

## 1.2 A first interference experiment

**Stable ID:** `sec-what-quantum-computing-computes-2`. **Depth:** M. **State:** draft.

[Read the working draft](chapters/ch-what-quantum-computing-computes.md#sec-what-quantum-computing-computes-2). Independent acceptance remains separate.

**Concrete question:** How can two alternatives cancel?

**Entry knowledge:** 1.1 and arithmetic on two real numbers; all preview notation is introduced locally.

**Exit skill:** Predict recombination and distinguish adding amplitudes from adding probabilities.

**Worked-case plan:** A fully displayed two-component, two-step interference calculation with every sum written out; a changed relative sign changes the prediction.

**Scope/continuity boundary:** Use an explicitly labelled preview model. The formal state postulate is owned by 3.1 and the measurement postulate by 6.1; do not cite those future sections as missing prerequisites or claim to derive a physical postulate.

**Formula-to-code plan:** Complete independent real-matrix reference and released FlagQuantum 0.3.1 comparison: examples/foundations/interference.py.

**Independent check:** Hand-computed multiplication and cancellation, followed by a deliberate probability-addition error.

**Transfer task:** Predict a changed sign or missing recombination step and explain which arithmetic step changes.

**Assigned exact sources:** [NC:1.3.1](references/proof-sources.md#source-nc-1-3-1). Source assignment is not independent proof review.

## 1.3 What a quantum state describes

**Stable ID:** `sec-what-quantum-computing-computes-3`. **Depth:** P. **State:** brief_ready.

**Concrete question:** What information does a state description contain?

**Entry knowledge:** 1.2, including the locally introduced two-component preview.

**Exit skill:** Distinguish the mathematical state description, a measurement choice and data collected over repetitions.

**Worked-case plan:** Two preview descriptions with the same immediate outcome frequencies but different later interference.

**Scope/continuity boundary:** Keep this a conceptual preview; complex-space definitions belong to Chapter 2, formal equivalence to 3.1 and measurement statistics to Chapter 6.

**Formula-to-code plan:** Reuse the complete interference reference with changed preparation; avoid a privileged simulator statevector being described as a device readout.

**Independent check:** Predict-first comparison of immediate measurement and subsequent recombination.

**Transfer task:** Explain why an output histogram alone need not determine all future predictions.

**Assigned exact sources:** [NC:1.2](references/proof-sources.md#source-nc-1-2). Source assignment is not independent proof review.

## 1.4 Algorithms, simulators, and physical devices

**Stable ID:** `sec-what-quantum-computing-computes-4`. **Depth:** V. **State:** brief_ready.

**Concrete question:** How do an algorithm, simulator and physical device differ?

**Entry knowledge:** 1.1; recall the task/output contract rather than importing hardware engineering.

**Exit skill:** Identify which object specifies a calculation, emulates it and physically executes a measurement.

**Worked-case plan:** The same task contract expressed as a program, a tiny numerical calculation and an explicitly proposed physical experiment.

**Scope/continuity boundary:** No hardware execution, provider support or speed ranking is claimed. Statevector inspection is a simulator capability with a separate cost.

**Formula-to-code plan:** Plan a complete classical reference and a versioned simulator run when appropriate; hardware access remains optional.

**Independent check:** A claim checklist that detects substitution of simulator output for measured data.

**Transfer task:** Classify a changed result or failure as model, numerical, sampling or device evidence.

**Assigned exact sources:** [ED:protocol](references/proof-sources.md#source-ed-protocol). Source assignment is not independent proof review.

## 1.5 What computational advantage would require

**Stable ID:** `sec-what-quantum-computing-computes-5`. **Depth:** V. **State:** brief_ready.

**Concrete question:** What would establish a computational advantage?

**Entry knowledge:** 1.4 and the explicit task/output contract.

**Exit skill:** Ask for matched problem instances, output accuracy, success probability and full resource accounting.

**Worked-case plan:** A hypothetical cost comparison that includes preparation, repeated measurements and classical processing, without current performance claims.

**Scope/continuity boundary:** This is an entry-level reasoning contract; formal access/complexity and lower-bound arguments belong to Chapter 14 and later algorithms.

**Formula-to-code plan:** A small cost ledger is appropriate; a quantum circuit is not required merely to populate this section.

**Independent check:** Change one omitted cost or precision requirement and reassess the hypothetical comparison.

**Transfer task:** Find the missing assumption in a new claimed speedup without requiring an advanced complexity theorem.

**Assigned exact sources:** [NC:3.2.1](references/proof-sources.md#source-nc-3-2-1). Source assignment is not independent proof review.

## 1.6 A map of the learning routes

**Stable ID:** `sec-what-quantum-computing-computes-6`. **Depth:** V. **State:** brief_ready.

**Concrete question:** Which learning route serves my question?

**Entry knowledge:** 1.4 and the task/model distinction.

**Exit skill:** Choose a route and identify its entry knowledge and first concrete deliverable.

**Worked-case plan:** Three bounded destinations: an algorithm prediction, a trainable circuit objective and a program-to-target transformation.

**Scope/continuity boundary:** Present the existing reader routes and core/advanced distinctions, without pretending every volume is a prerequisite for the next.

**Formula-to-code plan:** Use linked complete examples only as previews, with their actual draft/validation status.

**Independent check:** Resolve the selected route against canonical prerequisites and label unstudied advanced branches.

**Transfer task:** Choose a route for a new task and explain why an unrelated specialization is not required.

**Assigned exact sources:** [ED:routes](references/proof-sources.md#source-ed-routes). Source assignment is not independent proof review.

