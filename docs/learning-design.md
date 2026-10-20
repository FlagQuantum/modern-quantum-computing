# Learning design: recall, prediction and formula-to-code practice

This is an authoring specification for the proposed textbook. It combines the conceptual structure recorded in the [Nielsen–Chuang review](references/nielsen-chuang-design-review.md) with the reading-method observations in the [Quantum Country review](references/quantum-country-design-review.md). The current site does not implement account-based learning records, an adaptive scheduler or automated reminders.

## A section-level learning loop

1. Pose a concrete question and show the minimum example needed to understand it.
2. Ask the reader to predict a result before giving the derivation or running code.
3. Derive the result with explicit assumptions and intermediate steps.
4. Map important formulas to exact expressions and runtime conventions.
5. Compare the execution with an independent reference and explain disagreement.
6. Ask a short recall or transfer question; revisit relevant ideas in later chapters.

A chapter remains connected prose and argument. Questions support that argument and should not interrupt every sentence. Their number depends on conceptual density and reader testing, rather than a fixed card quota.

## Different activities need different questions

| Activity | Prompt design | Avoid |
|---|---|---|
| Recall | One identifiable concept or convention | A request to reproduce a whole proof from memory |
| Predict | A fully specified state, operation and requested output | An ambiguous answer caused by unstated basis order |
| Translate | A mathematical expression, array meaning and normalization | Memorization of a transient API spelling as the main objective |
| Diagnose | One plausible error and enough evidence to localize it | Several unrelated bugs hidden in a large program |
| Derive | A clear claim and assumptions; intermediate checkpoints if needed | Treating a numerical agreement as a proof |
| Experiment | A hypothesis, runnable program and comparison criterion | A success message without interpretation or a baseline |

## Original example prompts

These examples illustrate this book's learning goals. They are not copied from the reference essays and are not an implemented assessment engine.

### F2C-ORDER-001: predict an index

**Question:** With two qubits, basis order (00,01,10,11), and qubit 0 the most significant bit, what nonzero statevector entry results from applying X to qubit 0 of (lvert00
angle)?

**Answer:** Entry 2, corresponding to (lvert10
angle), using zero-based indexing.

**Diagnosis:** Entry 1 corresponds to flipping qubit 1 under these conventions. A correct answer must state or use the basis convention.

### F2C-MEASURE-001: connect probabilities and expectation

**Question:** A computational-basis measurement of one qubit has probabilities 0.8 and 0.2. Predict the expectation and variance of Z.

**Answer:** The expectation is (0.8-0.2=0.6). Since (Z^2=I), the variance is (1-0.6^2=0.64).

**Transfer:** For independent shots, derive the variance of the sample mean before running a sampling experiment.

### F2C-STATE-001: find a missing comparison

**Question:** Two Bell states have amplitudes ((1,0,0,1)/sqrt2) and ((1,0,0,-1)/sqrt2). Their computational-basis probabilities agree. Does that establish that the quantum states are equivalent up to a global phase?

**Answer:** No. Their relative sign differs. An XX expectation distinguishes them: +1 for the first state and -1 for the second. Equality of one measurement distribution does not establish arbitrary state equivalence.

**Transfer:** Implement the two preparations and compare both probabilities and XX expectations with explicit vectors.

### F2C-GRAD-001: diagnose generator normalization

**Question:** For a single occurrence of (U(	heta)=exp(-i	heta P)), where (P^2=I), can the ordinary RY angle's shift and prefactor be copied without modification?

**Answer:** No. Here the expectation derivative is (f(	heta+pi/4)-f(	heta-pi/4)). The usual single-occurrence RY rule uses shifts of (pi/2) and a factor of one half because its generator is (Y/2). Shared parameters require the additional chain-rule analysis.

**Transfer:** Match both conventions to the gradient and hydrogen VQE starter checks.

## Prompt records and answer quality

Use the [checkpoint template](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/templates/checkpoint.md). Each prompt should have a stable ID, conceptual prerequisite, task type, answer criteria, misconception feedback, and a link to the relevant derivation or executable reference. Keep short answers focused while retaining qualifications that change the result.

A future review system should distinguish a recalled answer from a successful transfer or derivation. Remembering a rule is not sufficient evidence that a reader can decide when it applies.

## Web and PDF parity

| Element | Web design target | Print design target |
|---|---|---|
| Essential explanation | Readable without accounts or hidden UI | Present in full |
| Prediction or recall prompt | Attempt before revealing an answer | Question before a clearly referenced answer |
| Code experiment | Link to a complete versioned script | Include core listings or an exact source reference |
| Revisit | Links to related earlier concepts; possible future local review | Review prompts and a suggested reader-managed revisit |
| Learning record | Optional future design, separate from content access | No dependence on a stored record |

Preserve accessibility, keyboard navigation and copyable math when interactive components are eventually built. Do not collect personal learning records or add notification services as part of merely authoring the textbook.

## Rollout and review

First, pilot this design on the measurement, gradients and teleportation material. Ask readers to explain their predictions and errors. Record unclear wording and prerequisite gaps, then improve the section. Only after the content works should we choose an optional implementation for reveal controls, question export or spaced review. No particular schedule or retention outcome is claimed here.
