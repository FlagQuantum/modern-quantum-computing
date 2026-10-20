# Result and proof plan: Quantum Information: Channels, Inference, and Communication

[Depth definitions](../proof-plan.md#proof-depth-contract) · [Source catalogue](../references/proof-sources.md) · [Volume plan](../volume-plan.md)

Authoring specifications only. No result/proof/API is certified by this plan. F/M/R have different scope; imported results are the exact prerequisite sections linked below.

## Chapter 9: Quantum Channels and Their Representations

<span id="sec-quantum-channels-and-their-representations-1"></span>

### 9.1 From closed evolution to quantum channels

**Core result / role:** Reduced unitary dynamics defines a channel.

**Assumptions and scope:** Initially fixed uncorrelated environment; finite system.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Trace the environment; derive linearity, positivity and trace preservation.

**Imported earlier results:** [8.3](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-3), [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4).

**Exact source targets:** [NC:8.2.2](../references/proof-sources.md#source-nc-8-2-2): Section 8.2.2 Environments and quantum operations.

**Independent evidence target:** Compare joint unitary evolution and reduced output.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-channels-and-their-representations-2"></span>

### 9.2 Linearity, positivity, and complete positivity

**Core result / role:** Complete positivity is stronger than positivity.

**Assumptions and scope:** Finite-dimensional linear map; arbitrary finite ancilla.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Use transposition as a counterexample; prove why ancillary positivity is required.

**Imported earlier results:** [8.2](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2), [4.1](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [9.1](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-1).

**Exact source targets:** [TQI:2.2.1](../references/proof-sources.md#source-tqi-2-2-1): Section 2.2.1 Definitions and basic notions concerning channels.

**Independent evidence target:** Use transposition as a counterexample to positivity being sufficient.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-channels-and-their-representations-3"></span>

### 9.3 Kraus operators and trace preservation

**Core result / role:** Kraus characterization of completely positive trace-preserving maps.

**Assumptions and scope:** Finite input/output spaces.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove both directions via Choi spectral decomposition; derive the trace-preserving sum rule.

**Imported earlier results:** [9.1](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-1), [9.2](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-2).

**Exact source targets:** [NC:8.2.3](../references/proof-sources.md#source-nc-8-2-3): Section 8.2.3 Operator-sum representation; [TQI:2.2.2](../references/proof-sources.md#source-tqi-2-2-2): Section 2.2.2 Representations and characterizations of channels.

**Independent evidence target:** Verify a simple channel on a spanning set of inputs.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-channels-and-their-representations-4"></span>

### 9.4 Stinespring dilation

**Core result / role:** Finite Stinespring dilation.

**Assumptions and scope:** Completely positive trace-preserving map.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Build the Kraus isometry; extend it to a unitary with explicit dimension assumptions.

**Imported earlier results:** [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3), [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4).

**Exact source targets:** [TQI:2.2.2](../references/proof-sources.md#source-tqi-2-2-2): Section 2.2.2 Representations and characterizations of channels.

**Independent evidence target:** Recover the channel by explicit partial trace.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-channels-and-their-representations-5"></span>

### 9.5 Choi representation and vectorization

**Core result / role:** Choi positivity and vectorization identities.

**Assumptions and scope:** Fixed input basis and vectorization order.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the Choi/Kraus relation, partial-trace constraint and inverse map.

**Imported earlier results:** [9.2](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-2), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3), [4.2](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2).

**Exact source targets:** [TQI:2.2.2](../references/proof-sources.md#source-tqi-2-2-2): Section 2.2.2 Representations and characterizations of channels.

**Independent evidence target:** Check reshuffling indices against explicit basis operators.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-channels-and-their-representations-6"></span>

### 9.6 Representation equivalence and Kraus nonuniqueness

**Core result / role:** Kraus representations differ by an isometry.

**Assumptions and scope:** Same finite completely positive map; padded Kraus lists.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Use factorizations of the same positive Choi matrix and track redundant operators.

**Imported earlier results:** [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3), [9.4](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-4), [9.5](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-5).

**Exact source targets:** [NC:8.2.3](../references/proof-sources.md#source-nc-8-2-3): Section 8.2.3 Operator-sum representation.

**Independent evidence target:** Convert a small channel between representations and check identical actions.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-channels-and-their-representations-7"></span>

### 9.7 Composition, tensor products, and instruments

**Core result / role:** Channel composition and instruments.

**Assumptions and scope:** Compatible finite input/output spaces; complete outcome family.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Multiply/tensor Kraus operators; retain classical outcome labels when composing instruments.

**Imported earlier results:** [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3), [6.2](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2).

**Exact source targets:** [NC:8.2.3](../references/proof-sources.md#source-nc-8-2-3): Section 8.2.3 Operator-sum representation; [TQI:2.3.2](../references/proof-sources.md#source-tqi-2-3-2): Section 2.3.2 Basic notions concerning measurements.

**Independent evidence target:** Compare sequential, composite and conditional calculations.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-channels-and-their-representations-8"></span>

### 9.8 Channel-validation laboratory

**Core result / role:** Channel-equivalence acceptance protocol.

**Assumptions and scope:** Declared vectorization, positivity and trace tolerances.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Compare Kraus, Choi and dilation outputs including an entangled input.

**Imported earlier results:** [9.5](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-5), [9.6](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-6), [9.7](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-7).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Check Choi positivity and partial traces; diagnose a trace-preserving but non-CP map.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 10: Distinguishability, Fidelity, and Quantum State Inference

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-1"></span>

### 10.1 Classical distinguishability as a starting point

**Core result / role:** Total variation equals optimal binary distinguishing advantage.

**Assumptions and scope:** Finite distributions; specified equal priors.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Optimize the decision set and relate its signed difference to the one-norm.

**Imported earlier results:** [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Exact source targets:** [NC:9.1](../references/proof-sources.md#source-nc-9-1): Section 9.1 Distance measures for classical information.

**Independent evidence target:** Compare two finite distributions and an explicit decision rule.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-2"></span>

### 10.2 Quantum trace distance and binary discrimination

**Core result / role:** Holevo-Helstrom binary discrimination theorem.

**Assumptions and scope:** Two finite density operators; stated priors.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Diagonalize the weighted difference and optimize over two-outcome effects.

**Imported earlier results:** [10.1](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-1), [8.2](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Exact source targets:** [TQI:3.1.1](../references/proof-sources.md#source-tqi-3-1-1): Section 3.1.1 Discriminating between pairs of quantum states.

**Independent evidence target:** Compare a spectral construction with independently enumerated candidate measurements.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-3"></span>

### 10.3 Fidelity and state-comparison conventions

**Core result / role:** Fidelity conventions and Uhlmann characterization.

**Assumptions and scope:** Finite normalized density operators.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive pure/commuting formulas; prove the purification maximization using polar decomposition.

**Imported earlier results:** [8.2](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2), [2.5](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-5).

**Exact source targets:** [TQI:3.2.1](../references/proof-sources.md#source-tqi-3-2-1): Section 3.2.1 Elementary properties of the fidelity function; [TQI:3.2.2](../references/proof-sources.md#source-tqi-3-2-2): Section 3.2.2 Characterizations of the fidelity function.

**Independent evidence target:** Verify analytic limiting cases and contrast fidelity with elementwise equality.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-4"></span>

### 10.4 Monotonicity and operational limits

**Core result / role:** Trace-distance contraction and fidelity monotonicity.

**Assumptions and scope:** Completely positive trace-preserving channel.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Use the measurement variational formula and dilation/purification arguments.

**Imported earlier results:** [10.2](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-2), [10.3](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-3), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3).

**Exact source targets:** [NC:9.2.1](../references/proof-sources.md#source-nc-9-2-1): Section 9.2.1 Trace distance; [TQI:3.2.3](../references/proof-sources.md#source-tqi-3-2-3): Section 3.2.3 Further properties of the fidelity function.

**Independent evidence target:** Construct a strict information-loss example and an incomplete-measurement counterexample.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-channel-error-metrics"></span>

### 10.5 Comparing channels and gate errors [Advanced]

**Core result / role:** Ancilla-assisted channel distance and entanglement fidelity.

**Assumptions and scope:** Finite channel dimensions; exact norm convention.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Prove selected easy bounds; state diamond-norm optimization and defer the full SDP characterization.

**Imported earlier results:** [10.2](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-2), [10.3](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-3), [9.5](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-5).

**Exact source targets:** [TQI:3.3.2](../references/proof-sources.md#source-tqi-3-3-2): Section 3.3.2 The completely bounded trace norm; [TQI:3.3.4](../references/proof-sources.md#source-tqi-3-3-4): Section 3.3.4 Characterizations of the completely bounded trace norm.

**Independent evidence target:** Compare small explicit channels and give a counterexample to inferring worst-case behavior from one state or an average metric.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local advanced bridge to supply:** Ancillary inputs, completely bounded trace norm and semidefinite feasibility vocabulary.

**Explicitly deferred proof ingredients:** Full diamond-norm SDP equivalence/duality and ancilla-size reduction; Watrous 3.3.2–3.3.4.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-5"></span>

### 10.6 State and process tomography

**Core result / role:** Informational completeness and linear inversion.

**Assumptions and scope:** Known spanning preparation/measurement sets.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive qubit Bloch inversion and a Choi linear system; explain physicality constraints.

**Imported earlier results:** [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7), [8.3](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-3), [9.5](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-5).

**Exact source targets:** [NC:8.4.2](../references/proof-sources.md#source-nc-8-4-2): Section 8.4.2 Quantum process tomography; [NC:2.4.2](../references/proof-sources.md#source-nc-2-4-2): Section 2.4.2 General properties of the density operator.

**Independent evidence target:** Reconstruct small states and compare physical versus unconstrained estimates.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-6"></span>

### 10.7 Pauli sums, grouping, and measurement allocation

**Core result / role:** Pauli-sum estimator variance and optimal allocation.

**Assumptions and scope:** Declared grouping and covariance model; fixed total shots.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Expand variance; use a constrained minimization for independent groups.

**Imported earlier results:** [6.4](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-4), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Exact source targets:** [NC:A1](../references/proof-sources.md#source-nc-a1): Appendix 1: Notes on basic probability theory; [CVX:7.5](../references/proof-sources.md#source-cvx-7-5): Section 7.5 Experiment design.

**Independent evidence target:** Compare allocation rules under an identical total-shot budget.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-7"></span>

### 10.8 Classical shadows [Advanced]

**Core result / role:** Unbiased classical-shadow reconstruction and scoped sample bound.

**Assumptions and scope:** Specified measurement ensemble with invertible measurement map.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Prove unbiasedness for the chosen ensemble; state the shadow-norm bound with its concentration assumptions.

**Imported earlier results:** [10.6](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-5), [6.7](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).

**Exact source targets:** [SHADOW:estimator](../references/proof-sources.md#source-shadow-estimator): Section I B-C estimator; Appendix A, Theorem 3 and its linear-prediction proof; Appendix A Theorem 3 (precise sample bound).

**Independent evidence target:** Check a small Pauli-shadow estimator and report ensemble-dependent uncertainty.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local advanced bridge to supply:** Measurement-channel inversion, shadow norm, independent batches and median-of-means.

**Explicitly deferred proof ingredients:** The concentration argument and simultaneous-property union bound in Appendix A Theorem 3; prove only reconstruction unbiasedness locally.

<span id="sec-distinguishability-fidelity-and-quantum-state-inference-8"></span>

### 10.9 Inference laboratory and validation limits

**Core result / role:** Inference-claim acceptance protocol.

**Assumptions and scope:** Distinguish reconstruction, property estimation and certification.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Require identifiable parameters, uncertainty and a counterexample to an overstrong claim.

**Imported earlier results:** [10.2](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-2), [10.3](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-3), [10.6](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-5), [10.7](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-6).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Report estimation error across repeated trials and identify unmeasured degrees of freedom.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 11: Entropy, Relative Entropy, and Information Processing

<span id="sec-entropy-relative-entropy-and-information-processing-1"></span>

### 11.1 Classical entropy and uncertainty

**Core result / role:** Shannon entropy and Gibbs inequality.

**Assumptions and scope:** Finite distributions; explicit zero/support conventions.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove nonnegativity of relative entropy and derive elementary entropy bounds.

**Imported earlier results:** [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Exact source targets:** [TQI:5.1.1](../references/proof-sources.md#source-tqi-5-1-1): Section 5.1.1 Definitions of classical entropic functions; [TQI:5.1.2](../references/proof-sources.md#source-tqi-5-1-2): Section 5.1.2 Properties of classical entropic functions.

**Independent evidence target:** Compare deterministic, uniform and correlated examples.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-entropy-relative-entropy-and-information-processing-2"></span>

### 11.2 Von Neumann entropy and spectra

**Core result / role:** Von Neumann entropy is spectral Shannon entropy.

**Assumptions and scope:** Finite density operator; chosen logarithm base.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive unitary invariance and pure/maximally-mixed cases from eigenvalues.

**Imported earlier results:** [11.1](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-1), [8.2](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2).

**Exact source targets:** [TQI:5.2.1](../references/proof-sources.md#source-tqi-5-2-1): Section 5.2.1 Definitions of quantum entropic functions.

**Independent evidence target:** Compute mixed-state examples and verify pure-state limits.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-entropy-relative-entropy-and-information-processing-3"></span>

### 11.3 Relative entropy and support conditions

**Core result / role:** Quantum relative entropy support condition and positivity.

**Assumptions and scope:** Positive density operators with declared support inclusion.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove the finite-dimensional Klein inequality route; treat infinite values explicitly.

**Imported earlier results:** [11.1](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-1), [11.2](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-2).

**Exact source targets:** [NC:11.3.1](../references/proof-sources.md#source-nc-11-3-1): Section 11.3.1 Quantum relative entropy.

**Independent evidence target:** Test commuting reductions, singular states and numerically unstable cases.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-entropy-relative-entropy-and-information-processing-4"></span>

### 11.4 Mutual and conditional information

**Core result / role:** Mutual information as relative entropy.

**Assumptions and scope:** Finite bipartite state.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Expand logarithms of tensor products and derive conditional-entropy identities.

**Imported earlier results:** [11.2](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-2), [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4).

**Exact source targets:** [NC:11.2.3](../references/proof-sources.md#source-nc-11-2-3): Section 11.2.3 Conditional entropy and mutual information; [TQI:5.2.1](../references/proof-sources.md#source-tqi-5-2-1): Section 5.2.1 Definitions of quantum entropic functions.

**Independent evidence target:** Compare classical correlations with negative quantum conditional entropy.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-entropy-relative-entropy-and-information-processing-5"></span>

### 11.5 Data processing

**Core result / role:** Quantum relative-entropy data processing.

**Assumptions and scope:** Completely positive trace-preserving map; support convention.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Give the dilation/partial-trace roadmap and explicit classical/commuting proof; identify the joint-convexity lemma deferred.

**Imported earlier results:** [11.3](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-3), [11.4](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-4), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3).

**Exact source targets:** [TQI:5.2.3](../references/proof-sources.md#source-tqi-5-2-3): Section 5.2.3 Joint convexity of quantum relative entropy.

**Independent evidence target:** Verify a small channel example and construct a counterexample to an invalid stronger claim.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local advanced bridge to supply:** Convex combinations of states, support limits and isometric dilation.

**Explicitly deferred proof ingredients:** Joint convexity/operator-convexity lemma needed for the full partial-trace proof; Watrous 5.2.3.

<span id="sec-entropy-relative-entropy-and-information-processing-6"></span>

### 11.6 Subadditivity and strong subadditivity [Advanced]

**Core result / role:** Strong subadditivity and subadditivity.

**Assumptions and scope:** Finite tripartite density operator.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Prove the elementary subadditivity consequence; state SSA and its relative-entropy proof route, deferring Lieb's technical theorem.

**Imported earlier results:** [11.4](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-4), [11.5](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-5).

**Exact source targets:** [NC:11.4.1](../references/proof-sources.md#source-nc-11-4-1): Section 11.4.1 Proof of strong subadditivity; [NC:A6](../references/proof-sources.md#source-nc-a6): Appendix 6: Proof of Lieb's theorem.

**Independent evidence target:** Check explicit tripartite examples and explain why a numerical survey is not a proof.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local advanced bridge to supply:** Tripartite reductions and conditional mutual information.

**Explicitly deferred proof ingredients:** Lieb concavity and the general strong-subadditivity proof; NC 11.4.1 and Appendix 6.

<span id="sec-entropy-relative-entropy-and-information-processing-7"></span>

### 11.7 Entropic reasoning in protocols

**Core result / role:** Entropic task bounds under processing.

**Assumptions and scope:** Explicit protocol and accessible subsystems.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Apply an already stated information inequality; distinguish a task bound from an attainable rate.

**Imported earlier results:** [11.4](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-4), [11.5](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-5).

**Exact source targets:** [NC:11.4.2](../references/proof-sources.md#source-nc-11-4-2): Section 11.4.2 Strong subadditivity: elementary applications.

**Independent evidence target:** Track relevant subsystems and diagnose an invalid entropy manipulation.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-entropy-relative-entropy-and-information-processing-8"></span>

### 11.8 Information-inequality laboratory

**Core result / role:** Information-inequality acceptance protocol.

**Assumptions and scope:** Declared dimensions, supports and logarithm base.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Check commuting limits and support failures; numerical tests do not prove inequalities.

**Imported earlier results:** [11.2](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-2), [11.3](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-3), [11.6](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-6).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Compare analytic examples with independently computed spectra and support-aware implementations.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 12: Compression, Entanglement, and Communication Limits

<span id="sec-compression-entanglement-and-communication-limits-1"></span>

### 12.1 Operational tasks and asymptotic statements

**Core result / role:** Operational rate definitions and order of limits.

**Assumptions and scope:** Declared blocklength, error metric and assistance model.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** State what vanishing error and asymptotic rate mean; separate converse and achievability.

**Imported earlier results:** [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8), [11.1](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-1).

**Exact source targets:** [TQI:8.1.1](../references/proof-sources.md#source-tqi-8-1-1): Section 8.1.1 Classical capacities of quantum channels.

**Independent evidence target:** Write a precise compression/communication task before constructing code.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-compression-entanglement-and-communication-limits-2"></span>

### 12.2 Typical sequences and subspaces

**Core result / role:** Typical-set/subspace concentration.

**Assumptions and scope:** Independent identical finite-alphabet or spectral source.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove the selected weak-typicality bound and derive dimension/probability estimates.

**Imported earlier results:** [12.1](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-1), [11.1](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-1), [11.2](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-2).

**Exact source targets:** [NC:12.2.1](../references/proof-sources.md#source-nc-12-2-1): Section 12.2.1 Shannon’s noiseless channel coding theorem; [NC:12.2.2](../references/proof-sources.md#source-nc-12-2-2): Section 12.2.2 Schumacher’s quantum noiseless channel coding theorem.

**Independent evidence target:** Enumerate short blocks and compare retained probability with entropy-based expectations.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-compression-entanglement-and-communication-limits-3"></span>

### 12.3 Schumacher compression

**Core result / role:** Schumacher compression theorem.

**Assumptions and scope:** Independent identical finite-dimensional source; entanglement-fidelity criterion.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Give a full typical-projector achievability argument; outline the converse and exact technical prerequisites.

**Imported earlier results:** [12.2](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-2), [8.2](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2), [10.3](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-3).

**Exact source targets:** [TQI:5.3.2](../references/proof-sources.md#source-tqi-5-3-2): Section 5.3.2 Quantum source coding.

**Independent evidence target:** Build a small typical-subspace encoder and evaluate recovery fidelity.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local advanced bridge to supply:** Typical projector, entanglement fidelity and asymptotic rate/error quantifiers.

**Explicitly deferred proof ingredients:** The full optimal-rate converse and finite-to-asymptotic technical estimates; Watrous 5.3.2.

<span id="sec-compression-entanglement-and-communication-limits-4"></span>

### 12.4 Entanglement concentration and dilution

**Core result / role:** Pure-state entanglement concentration and dilution rates.

**Assumptions and scope:** Asymptotic pure bipartite states; LOCC and vanishing error.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Derive a representative typical-subspace protocol; state which optimal-rate converse is deferred.

**Imported earlier results:** [7.2](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-2), [11.2](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-2), [12.2](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-2).

**Exact source targets:** [NC:12.5.2](../references/proof-sources.md#source-nc-12-5-2): Section 12.5.2 Entanglement distillation and dilution; [TQI:6.2.2](../references/proof-sources.md#source-tqi-6-2-2): Section 6.2.2 Distillable entanglement and entanglement cost.

**Independent evidence target:** Calculate branch probabilities and retained entanglement explicitly.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local advanced bridge to supply:** LOCC, typical Schmidt sequences, error metrics and asymptotic rates.

**Explicitly deferred proof ingredients:** General optimal-rate converse and dilution protocol estimates; NC 12.5.2 and Watrous 6.2.2.

<span id="sec-mixed-entanglement-resources"></span>

### 12.5 Mixed-state entanglement, LOCC, and distillation [Advanced]

**Core result / role:** PPT necessity, entanglement witnesses and distillation boundaries.

**Assumptions and scope:** Finite bipartite states; specified LOCC task.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Prove separability implies PPT and one witness criterion; do not claim PPT sufficiency in arbitrary dimension.

**Imported earlier results:** [8.2](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-2), [8.4](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-4), [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3), [10.2](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-2), [11.4](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-4).

**Exact source targets:** [TQI:6.1.1](../references/proof-sources.md#source-tqi-6-1-1): Section 6.1.1 Separable operators and states; [TQI:6.2.3](../references/proof-sources.md#source-tqi-6-2-3): Section 6.2.3 Bound entanglement and partial transposition.

**Independent evidence target:** Compare known separable/entangled mixed states and a tiny purification/distillation example; do not generalize a sufficient test into a universal criterion.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-compression-entanglement-and-communication-limits-5"></span>

### 12.6 Accessible information and the Holevo bound

**Core result / role:** Holevo bound.

**Assumptions and scope:** Finite classical-quantum ensemble; measurement output.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive the bound from data processing already stated in 11.5; distinguish a conditional proof from re-proving DPI.

**Imported earlier results:** [11.3](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-3), [11.5](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-5), [12.1](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-1).

**Exact source targets:** [NC:12.1.1](../references/proof-sources.md#source-nc-12-1-1): Section 12.1.1 The Holevo bound; [TQI:5.3.3](../references/proof-sources.md#source-tqi-5-3-3): Section 5.3.3 Encoding classical information into quantum states.

**Independent evidence target:** Compare candidate measurements with the ensemble's Holevo quantity.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-compression-entanglement-and-communication-limits-6"></span>

### 12.7 Classical and quantum channel capacities

**Core result / role:** HSW and quantum-capacity theorem statements.

**Assumptions and scope:** Memoryless channels; declared assistance and regularization.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** State exact operational rates and proof roadmaps; defer random coding/decoupling proofs with explicit prerequisites.

**Imported earlier results:** [9.3](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-3), [11.4](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-4), [12.1](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-1), [12.6](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-5).

**Exact source targets:** [TQI:8.1.2](../references/proof-sources.md#source-tqi-8-1-2): Section 8.1.2 The Holevo-Schumacher-Westmoreland theorem; [TQI:8.2.2](../references/proof-sources.md#source-tqi-8-2-2): Section 8.2.2 The quantum capacity theorem.

**Independent evidence target:** Evaluate elementary channels without assuming a universal single-letter capacity formula.

**Planning budget:** 6–10 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local advanced bridge to supply:** Code/decoder families, assistance models, coherent information and regularized limits.

**Explicitly deferred proof ingredients:** HSW random-coding/converse and quantum-capacity decoupling/regularization arguments; Watrous 8.1.2 and 8.2.2.

<span id="sec-compression-entanglement-and-communication-limits-7"></span>

### 12.8 Finite-block limitations and resource accounting

**Core result / role:** Finite blocklength does not establish asymptotic capacity.

**Assumptions and scope:** Finite tested code and error confidence interval.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Derive a finite achieved rate and error budget; show why it is not a capacity proof.

**Imported earlier results:** [12.2](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-2), [12.3](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-3), [12.7](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-6).

**Exact source targets:** [TQI:8.1.1](../references/proof-sources.md#source-tqi-8-1-1): Section 8.1.1 Classical capacities of quantum channels.

**Independent evidence target:** Report block length, fidelity, success probability and communication/entanglement costs.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-compression-entanglement-and-communication-limits-8"></span>

### 12.9 Compression and communication laboratory

**Core result / role:** Communication acceptance protocol.

**Assumptions and scope:** Specified source/channel, blocklength and assistance.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Reuse compression and capacity assumptions; compare finite evidence with the exact claimed rate.

**Imported earlier results:** [12.3](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-3), [12.4](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-4), [12.8](../section-plans/02-information.md#sec-compression-entanglement-and-communication-limits-7).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Compare independent encoders/decoders and document why finite tests cannot prove a coding theorem.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

## Chapter 13: Quantum Cryptography and Security Reasoning

<span id="sec-quantum-cryptography-and-security-reasoning-1"></span>

### 13.1 Security tasks and adversarial models

**Core result / role:** Security as an explicit ideal-versus-real task.

**Assumptions and scope:** Declared adversary, authentication and abort semantics.

**Proof depth:** P — Postulate / definition / task contract. **Proof obligation:** Define correctness/secrecy targets and the accessible adversarial system.

**Imported earlier results:** [6.6](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).

**Exact source targets:** [COMPOSE:definition](../references/proof-sources.md#source-compose-definition): Section 2.2 Security Criteria and 2.3 composition.

**Independent evidence target:** Write a protocol-specific threat model and identify missing assumptions.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-cryptography-and-security-reasoning-2"></span>

### 13.2 BB84 preparation, measurement, and sifting

**Core result / role:** BB84 sifting and intercept-resend disturbance.

**Assumptions and scope:** Ideal single-qubit source/measurement; authenticated classical channel.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive sifted correlations and the selected attack's conditional error probabilities.

**Imported earlier results:** [3.2](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-2), [6.4](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-4), [13.1](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-1).

**Exact source targets:** [NC:12.6.3](../references/proof-sources.md#source-nc-12-6-3): Section 12.6.3 Quantum key distribution.

**Independent evidence target:** Check basis choices, sifted records and expected error statistics.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-cryptography-and-security-reasoning-3"></span>

### 13.3 Parameter estimation and finite samples

**Core result / role:** Parameter-estimation coverage.

**Assumptions and scope:** Declared random sampling model; finite data.

**Proof depth:** F — Complete proof at the stated finite scope. **Proof obligation:** Derive a conservative sampling bound; distinguish sampling with and without replacement.

**Imported earlier results:** [6.8](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8), [13.2](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-2).

**Exact source targets:** [CVX:7.4](../references/proof-sources.md#source-cvx-7-4): Section 7.4 Chebyshev and Chernoff bounds; [QKD:finite](../references/proof-sources.md#source-qkd-finite): Section VIII A 1 Finite-key analysis (scope discussion, not a modern full finite-key theorem).

**Independent evidence target:** Evaluate coverage and abort rates across independent synthetic transcripts.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-cryptography-and-security-reasoning-4"></span>

### 13.4 Error reconciliation and information leakage

**Core result / role:** Reconciliation transcript leaks information.

**Assumptions and scope:** Specified classical code/protocol and public transcript.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Track transcript length and correctness; do not infer optimal leakage from a toy code.

**Imported earlier results:** [11.1](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-1), [13.2](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-2).

**Exact source targets:** [NC:12.6.2](../references/proof-sources.md#source-nc-12-6-2): Section 12.6.2 Privacy ampliﬁcation and information reconciliation.

**Independent evidence target:** Track leakage and residual disagreements in a tiny example.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-quantum-cryptography-and-security-reasoning-5"></span>

### 13.5 Privacy amplification

**Core result / role:** Renner-König quantum-side-information hashing bound (Theorem 4.1; smoothing Corollary 4.2).

**Assumptions and scope:** Two-universal hash independently sampled; classical-quantum side information; the accessed source's S2/S0 and smoothed Renyi conventions.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** State Theorem 4.1 with its exact entropy/trace-distance conventions; prove a classical special case and roadmap the quantum argument plus Corollary 4.2, without substituting a different modern conditional-min-entropy formula.

**Imported earlier results:** [11.3](../section-plans/02-information.md#sec-entropy-relative-entropy-and-information-processing-3), [13.3](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-3), [13.4](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-4).

**Exact source targets:** [PRIVACY:hashing](../references/proof-sources.md#source-privacy-hashing): Section 4.1, Theorem 4.1 and Corollary 4.2; Section 4.2 applications (source Renyi entropy convention).

**Independent evidence target:** Illustrate hashing on toy data without treating it as a secure production implementation.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local advanced bridge to supply:** Classical-quantum state, two-universal hashing, distance security and exact entropy convention.

**Explicitly deferred proof ingredients:** Quantum side-information hashing estimates in Renner-König Section 4.1; no unreviewed substitution of a different smooth-entropy theorem.

<span id="sec-quantum-cryptography-and-security-reasoning-6"></span>

### 13.6 Composable security and proof structure [Advanced]

**Core result / role:** Composable secrecy and correctness composition.

**Assumptions and scope:** Trace-distance criterion; explicit failure parameters.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Derive the selected composition via triangle inequality; roadmap the full QKD reduction and finite-key ingredients.

**Imported earlier results:** [10.2](../section-plans/02-information.md#sec-distinguishability-fidelity-and-quantum-state-inference-2), [13.1](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-1), [13.3](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-3), [13.5](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-5).

**Exact source targets:** [COMPOSE:definition](../references/proof-sources.md#source-compose-definition): Section 2.2 Security Criteria and 2.3 composition; [PRIVACY:hashing](../references/proof-sources.md#source-privacy-hashing): Section 4.1, Theorem 4.1 and Corollary 4.2; Section 4.2 applications (source Renyi entropy convention).

**Independent evidence target:** Identify which protocol steps are covered by the theorem and which implementation assumptions remain.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local advanced bridge to supply:** Ideal/real systems, abort, trace-distance secrecy and explicit failure composition.

**Explicitly deferred proof ingredients:** Complete general-protocol simulation/composition formalism and full finite-key QKD reduction; Müller-Quade/Renner Section 2.3.

<span id="sec-quantum-cryptography-and-security-reasoning-7"></span>

### 13.7 Attacks, side channels, and failure diagnosis

**Core result / role:** A secure ideal protocol need not secure an implementation.

**Assumptions and scope:** Specified source/detector side channel.

**Proof depth:** M — Complete selected-model derivation. **Proof obligation:** Construct an attack violating an explicit model assumption and trace its leakage.

**Imported earlier results:** [13.1](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-1), [13.2](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-2).

**Exact source targets:** [QKD:devices](../references/proof-sources.md#source-qkd-devices): Section III B 3-5 side channels, hacking and uncalibrated devices.

**Independent evidence target:** Analyze a specified attack or missing-authentication counterexample.

**Planning budget:** 3–6 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

<span id="sec-crypto-impossibility-boundaries"></span>

### 13.8 Cryptographic tasks and impossibility boundaries [Advanced]

**Core result / role:** Quantum bit-commitment impossibility (scoped).

**Assumptions and scope:** Unrestricted cheating operations; ideal concealment and purification model.

**Proof depth:** R — Precise advanced theorem with proof roadmap. **Proof obligation:** Prove the perfectly concealing pure-state unitary-cheating argument; defer approximate/general protocol cases.

**Imported earlier results:** [8.6](../section-plans/01-foundations.md#sec-density-matrices-reduced-states-and-purification-6), [13.1](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-1).

**Exact source targets:** [NOGO:cheating](../references/proof-sources.md#source-nogo-cheating): Purification-based cheating construction in the ideal concealing case; [TQI:2.1.3](../references/proof-sources.md#source-tqi-2-1-3): Section 2.1.3 Reductions and purifications of quantum states.

**Independent evidence target:** Analyze a tractable cheating example and document the exact theorem/proof obligations rather than inferring security from simulation.

**Planning budget:** 4–8 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.

**Local advanced bridge to supply:** Purification, concealment, binding and allowed cheating operations.

**Explicitly deferred proof ingredients:** Approximate-concealment/general interactive protocols beyond the proved ideal pure-state case; Lo-Chau pp.2–5.

<span id="sec-quantum-cryptography-and-security-reasoning-8"></span>

### 13.9 A security-claim audit

**Core result / role:** Security-claim acceptance protocol.

**Assumptions and scope:** Explicit theorem scope and actual implementation assumptions.

**Proof depth:** V — Validation / methodology specification. **Proof obligation:** Audit authentication, leakage, abort probability and source/detector models.

**Imported earlier results:** [13.3](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-3), [13.5](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-5), [13.6](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-6), [13.7](../section-plans/02-information.md#sec-quantum-cryptography-and-security-reasoning-7).

**Exact source targets:** [ED:protocol](../references/proof-sources.md#source-ed-protocol): Reader review and acceptance evidence.

**Independent evidence target:** Produce a protocol record with source theorem, finite-size terms and explicit unverified claims.

**Planning budget:** 2–4 pages. **Review status:** planned; source locators assigned; proof review pending; mathematical and implementation review remain separate.
