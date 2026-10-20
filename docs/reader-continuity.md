# Reader continuity: no unexplained steps

This is a binding authoring and review standard for the textbook. It implements the author's requirement that a young learner can follow a continuous argument without dismissive shortcuts. It complements the [learning design](learning-design.md) and the [architecture audit](curriculum-audit.md).

## A section makes a learning contract

Before drafting, record the question, knowledge assumed, knowledge introduced, result established, worked example, independent check and skill carried into the next section. Link exact earlier sections for prerequisites. A citation to an entire advanced textbook does not supply a missing step on a core learning path.

If a prerequisite has not been taught, provide a local bridge or explicitly move the section to an advanced branch with a usable entry route. Do not introduce notation in a derivation before defining it. Give dimensions, subsystem labels, units and conventions where they first matter.

## Explain the transition, not just the destination

Each significant equation change needs the operation that justifies it: substitution, linearity, orthogonality, spectral decomposition, approximation, conditioning or a named result already established. State when an equality becomes an approximation and why its error is acceptable.

For example, after introducing the rotated state, the Z expectation needs the observable's action and the vanishing cross terms:

$$
\lvert\psi\rangle=c\lvert0\rangle+s\lvert1\rangle,
\qquad c=\cos(\phi/2),\quad s=\sin(\phi/2).
$$

Since $Z\lvert0\rangle=\lvert0\rangle$, $Z\lvert1\rangle=-\lvert1\rangle$ and the basis vectors are orthonormal, expanding the inner product gives

$$
\langle\psi|Z|\psi\rangle
=c^2\langle0|0\rangle-cs\langle0|1\rangle
+sc\langle1|0\rangle-s^2\langle1|1\rangle
=c^2-s^2=\cos\phi.
$$

The final identity is the double-angle formula. The code correspondence then explains why probabilities are squared amplitude magnitudes and why their difference is the expectation. It should not skip directly from a simulator call to a claimed identity.

This example uses real coefficients specified above; a general complex-state derivation must retain conjugates. Explaining such a qualification prevents an example-specific simplification from becoming a false general rule.

## Language that cannot discharge an explanation

Phrases such as “obviously,” “clearly,” “it is easy to see,” “well known,” “straightforward,” and “trivial,” or “众所周知,” “显然,” “容易理解,” and “不难证明,” cannot replace a derivation or prerequisite bridge.

When such wording hides work, replace it with the actual steps, an established proposition with a precise link, or a clearly marked advanced proof roadmap. An exercise may invite a reader to complete a step only after giving the necessary tools and an accessible answer/hint path. Central proof obligations cannot be silently transferred into exercises.

A terminology scan flags possible shortcuts for review. It does not determine whether prose is explanatory; a chapter can omit every flagged phrase and still skip essential reasoning.

## Worked examples and abstraction

Begin a new abstraction with a small question and a fully specified case. Develop the definition and general argument, return to the example, then offer a changed case or counterexample. Introduce generality when the reader can see what problem it solves.

Keep important formula/code mappings nearby. Explain what each axis, variable and coefficient represents. Distinguish a complete runnable program from an excerpt. Preserve code provenance and the independent mathematical reference. Do not make the learner infer the physical meaning from an API name.

## Cross-layer and cross-platform continuity

Use one recurring task to link an abstract circuit, a physical encoding, native operations, placement/routing, scheduling, control and readout. At each boundary state the contract and what changes. Choose representative exact or controlled small models; do not imply identical noisy physics across platforms.

Chapter 34 supplies common physics bridges. Readers then choose a platform branch, complete the worksheet, and enter compilation with a specified target. Other platform specialties are optional comparative branches. Distinguish qubits, physical levels, optical modes, motional modes, ancillary systems and logical code spaces.

## Reader review and acceptance evidence

Reviewers should be able to reconstruct intermediate steps, explain assumptions, trace a code expression to its formula, and transfer the reasoning to a changed example. Record the exact point where a reader becomes stuck, their assumed background, the missing bridge and the correction made. Do not treat a satisfaction score as a replacement for these observations.

Before accepting a section:

- Check each new symbol and prerequisite has an introduction or an exact usable pointer.
- Check each substantive transformation has a reason and each approximation has assumptions.
- Check at least one complete worked example, a transfer task and appropriate independent evidence.
- Check the section's exit skill is sufficient for the next step in its declared learning route.
- Check advanced diversions can be deferred without breaking the core argument.
- Review the prose scan, but also perform a line-by-line mathematical and reader audit.

No completed learner study or specialist approval is claimed by this standard.
