# 1. What Quantum Computing Computes

**Working draft: sections 1.1–1.3 · Writing Baseline 1.0 · October 20, 2026.** Sections 1.4–1.6 remain planned. Independent mathematical and reader review are pending; this is not an accepted chapter. Section 1.1 uses Python 3.12 and the standard library. Sections 1.2–1.3 add pinned FlagQuantum 0.3.1 simulations.

<span id="sec-what-quantum-computing-computes-1"></span>

## 1.1 Problems, inputs, and observable outputs

Imagine that a program prints `01101011`. Has it solved a problem? That depends on what we asked it to return. The string could be an answer, eight records from repeated runs, or a label in a larger calculation. Its appearance alone does not tell us whether the computation succeeded.

Before constructing a quantum circuit, we therefore need a **task contract**: what is given, how it is represented, what must be returned, what counts as success, and which resources we count. A task contract specifies the goal; an algorithm specifies how to pursue it. Several algorithms, classical or quantum, may be candidates for the same contract.

You need arithmetic and basic Python lists to follow this section. By its end, you should be able to write a contract and detect when a program returns the wrong kind of result. We introduce no quantum postulate here.

### One problem, many input instances

Consider the question: does a nonempty list of bits contain an odd number of ones? A **bit** is a value that is either 0 or 1. The rule is a computational problem; the particular list `[1, 0, 1, 1]` is one **instance** of that problem. We will call this list $x$ and its length $n$. Here $n=4$.

The same instance can be stored as a Python list or as the string `"1011"`. Those representations need different parsing code. They do not change which answer is correct, provided their decoding agrees. For this example, our accepted input representation is a nonempty list of integer bits.

Our requested output is the **parity**: 1 for an odd number of ones and 0 for an even number. For $x=[1,0,1,1]$, adding the entries gives

$$
1+0+1+1=3.
$$

Dividing 3 by 2 leaves remainder 1, so the answer is 1. More generally, let $x_j$ denote the $j$th bit, with $j$ running from 1 to $n$. Then

$$
f(x)=(x_1+x_2+\cdots+x_n)\bmod 2.
$$

Here $f$ names the requested function and $\bmod 2$ means “take the remainder after division by 2.” Returning the original four-bit list would preserve information about the instance, but would not return the requested single-bit answer.

A complete contract for this case is:

| Contract item | Parity task |
|---|---|
| Given information | A nonempty list $x$ of $n$ integer bits, accessible in ordinary computer memory |
| Requested output | One integer bit $y$ |
| Success | $y=f(x)$, exactly |
| Resource boundary | Count input reads and classical work; include reading the list rather than assuming its parity is supplied |

A direct procedure begins at 0 and changes 0 to 1, or 1 to 0, whenever it reads a one. An even number of changes returns to 0; an odd number ends at 1. This explains the loop in the program below. It reads all $n$ entries. We make no lower-bound claim about other access models here.

**Checkpoint 1.1-A.** For the input `[1, 1, 0, 0]`, should the result be `1100`, 2, or 0? Explain the role of each candidate before checking the answer below.

### One outcome is different from an estimated average

Now suppose an experiment returns a bit each time it runs. One run might return 0 and the next 1. A **shot** means one preparation, execution and readout. For our next task, assume that repeated shots use the same preparation and readout and are independent: knowing an earlier outcome does not change the probabilities of later outcomes.

Assign a numerical **score** to each outcome. For a bit $b$, define

$$
z(b)=1-2b.
$$

Substituting 0 gives $z(0)=1$; substituting 1 gives $z(1)=-1$. A bit is the recorded outcome; its score is a number assigned by our processing rule. We do not need an operator or a quantum state to define this rule.

Let $p_0$ and $p_1$ be the probabilities of outcomes 0 and 1. They add to 1. Define the **expectation**, or probability-weighted mean score, by

$$
\mu=p_0z(0)+p_1z(1)=p_0-p_1.
$$

The symbol $\mu$ denotes a property of the outcome distribution. It is not generally the score from one shot. In a supplied teaching model with $p_0=1/4$ and $p_1=3/4$, the mean is $\mu=1/4-3/4=-1/2$. A single shot still has score either $+1$ or $-1$, never $-1/2$.

In an estimation problem, the probabilities are usually unknown. What we can collect is a list of outcomes. For $N$ shots, write their bits as $b_1,\ldots,b_N$ and define the **sample mean**

$$
\widehat{\mu}=\frac{z(b_1)+\cdots+z(b_N)}{N}
=\frac{n_0-n_1}{N}.
$$

The hat marks an estimate. The counts $n_0$ and $n_1$ are the numbers of zeros and ones, so $n_0+n_1=N$. The second expression follows because each zero contributes $+1$ and each one contributes $-1$.

For the fixed teaching data `[0, 1, 1, 0, 1, 0, 1, 1]`, we have $N=8$, $n_0=3$ and $n_1=5$. Therefore

$$
\widehat{\mu}=\frac{3-5}{8}=-\frac14.
$$

This differs from the model mean $-1/2$. Finite data need not reproduce the mean exactly. These eight records are a constructed fixture for checking arithmetic, not measurements collected from a quantum device.

### What does success mean when the output varies?

To specify an estimation task, choose an allowed absolute error $\epsilon>0$ and an allowed failure probability $\delta$ between 0 and 1. The contract asks for a numerical estimate satisfying

$$
\Pr\!\left(\lvert\widehat{\mu}-\mu\rvert\leq\epsilon\right)\geq1-\delta.
$$

Read this as: if the sampling procedure were repeated, the probability that its estimate lies within the allowed error must be at least $1-\delta$. The probability includes the randomness in collecting the data. An acceptable output type alone does not establish this guarantee.

For our fixture, choose $\epsilon=1/4$. Its absolute error is

$$
\left\lvert-\frac14-\left(-\frac12\right)\right\rvert=\frac14,
$$

so **this estimate** passes the error check, including the boundary. That does not establish the probability guarantee for the procedure. The accompanying program separately computes that probability for the supplied independent-shot model: it enumerates all 256 eight-bit records, weights each by its probability, and adds the weights of the successful ones. They are not equally likely when $p_0\ne p_1$.

The resulting probability is $12879/16384$, approximately 0.7861. Thus this particular model and $N=8$ meet a requirement $1-\delta=3/4$. This is not a guarantee for all unknown distributions or correlated device data. Chapter 6 develops statistical error guarantees; we have not derived a general shot-count rule here.

| Contract item | Mean-score estimation task |
|---|---|
| Given information | Access to independent repetitions of a fixed experiment; a known bit-to-score rule; chosen $\epsilon$ and $\delta$ |
| Requested output | A numerical estimate $\widehat{\mu}$ |
| Success | The stated error event has probability at least $1-\delta$ under the declared model |
| Resource boundary | Include each preparation, execution and readout, as well as data processing; report $N$ |

The small verifier is given $p_0$ and $p_1$ so that it can check the estimator. An experimental estimator is not being handed the unknown answer. If the probabilities were already available exactly, computing $p_0-p_1$ would be a different input-access contract.

**Checkpoint 1.1-B.** A program returns only the eight raw bits when the requested output is a mean estimate. What processing is missing? Would one successful estimate establish the probability guarantee?

### Formula to code: make the output checkable

The [complete reference program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/task_contracts.py) implements the following correspondences. `Fraction(a, b)` stores the rational number $a/b$ exactly. Python indexes lists from 0; our mathematical subscripts above begin at 1, but the order of entries is the same.

| Definition or check | Python expression | Independent reference |
|---|---|---|
| Parity $f(x)$ | `parity(bits)` toggles on each one | `sum(bits) % 2` on every four-bit input |
| Score $z(b)=1-2b$ | `1 - 2 * bit` | Substitute each of the two allowed bits |
| Sample mean $\widehat{\mu}$ | `mean_score(shots)` sums scores and divides by the number of shots | `Fraction(shots.count(0) - shots.count(1), len(shots))` |
| Error at most $\epsilon$ | `abs(value - target) <= epsilon` | Fixture arithmetic above; a deliberately incorrect estimate must fail |
| Model success probability | Weighted enumeration of all eight-bit records | Group records by their zero count; see laboratory 1.1-E |

From the repository root, with Python 3.12, run:

```bash
python examples/foundations/task_contracts.py
```

No package installation is required. Expected output:

```text
Parity of 1011: 1
Fixture: N=8, zeros=3, ones=5
Estimate: -1/4; reference mean: -1/2; tolerance: 1/4
Model success probability: 12879/16384 = 0.786071777
Required success probability: 3/4
Enumeration, grouped reference, and contract failure checks passed.
```

The program also rejects empty or nonbinary data and rejects a bitstring supplied in place of a numerical estimate. Exact rational arithmetic makes these checks deterministic. It verifies the specified finite examples, not the correctness of an arbitrary device or a general statistical theorem. Exhaustive enumeration grows with the number of possible records and is suitable here only because the model is small.

### What is available at the output boundary?

A quantum experiment can produce recorded outcomes, and classical processing can turn many outcomes into statistics. A simulator may additionally expose its stored **statevector**, a list of numerical coordinates used to represent the simulated quantum state. We will define those coordinates later. Inspecting that list is a software operation; it is not a generic physical readout that returns every coordinate in one shot.

Likewise, an exact expectation computed from simulated probabilities and an estimate computed from finite shots answer different access contracts. Either can be useful, but a result must state which was returned. In a FlagQuantum example, we will identify whether a call returns internal simulation data, an exact ideal-model quantity or sampled outcomes before using it as evidence. No FlagQuantum call is needed to settle that distinction here.

### Practice, answers, and the next question

**1.1-C — Transfer.** An experiment reports either `success` or `failure`. You want its success rate to absolute error 0.05 with success probability at least 0.95. Specify the access assumption, output, score, error criterion and resource boundary. Do not guess a shot count without a statistical argument.

**1.1-D — Debugging.** A report says: “The simulator returned an exact mean of $-1/2$, so eight device shots will return the same mean.” Identify the unsupported step and give a possible eight-shot record that contradicts the asserted certainty.

**1.1-E — Optional enumeration laboratory.** Check the program's probability calculation by grouping records by the number $k$ of zero outcomes. For eight shots, their mean score is $2k/8-1$. Which integer values of $k$ pass the error check? Use the grouping calculation in the program to verify the total. This laboratory introduces counting as an independent check; it is not a prerequisite for the next section.

**Answers and reasoning**

- **A.** The answer is 0 because there are two ones. `1100` represents the input; 2 is the count of ones, an intermediate quantity. Neither is the requested parity bit.
- **B.** Apply the score rule and average: the fixture gives $-1/4$. A single passed error check says nothing by itself about how often the procedure passes over repeated data collections.
- **C.** Assume independent repetitions with a fixed success probability, or state a different model explicitly. Assign score 1 to success and 0 to failure. Return a numerical estimate $\widehat p$ of the unknown rate $p$, requiring $\Pr(\lvert\widehat p-p\rvert\leq0.05)\geq0.95$. Count all repetitions and processing. The scoring rule is different from the $+1/-1$ rule used above.
- **D.** An exact model mean is substituted for a random sample mean. Eight zeros give a sample mean of $+1$ and have nonzero probability $(1/4)^8$ in the supplied independent model. The procedure can satisfy a probability guarantee while some records fail.
- **E.** Substitution gives $\lvert k/4-1/2\rvert\leq1/4$, or $1\leq k\leq3$. There are $\binom{8}{k}$ records with $k$ zeros: this symbol counts ways to choose their positions. Each has probability $(1/4)^k(3/4)^{8-k}$ by independence. Sum these products for $k=1,2,3$ to obtain $12879/16384$. Python's `comb(8, k)` supplies that position count. Neither equal weighting of all records nor counting successful records alone gives the probability here.

You can now separate an instance from its encoding, specify a requested output and state how its correctness is judged. The next section, [1.2 A first interference experiment](#sec-what-quantum-computing-computes-2), asks how a quantum model changes the probabilities from which outcomes are drawn. It will introduce its preview arithmetic locally.

### Source and validation note

For resource-model context, the assigned companion source is Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010), §3.2.1, printed pp. 136–137; [source record NC:3.2.1](../references/proof-sources.md#source-nc-3-2-1). That discussion motivates specifying input size and the computational model before comparing costs. The contracts, examples, synthetic data and finite probability verification above are original teaching material, not quotations or reproduced exercises from that book.

Proof-depth role: **P**, a task definition and its consequences; no new physical postulate or complexity theorem. Local execution details and unresolved review status are recorded in [the section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/1.1.json). Author checks are separate from independent mathematical review and target-reader testing; both remain pending.

<span id="sec-what-quantum-computing-computes-2"></span>

## 1.2 A first interference experiment

A fair coin tossed twice remains random. Can a different kind of two-step operation produce a random-looking intermediate prediction but a certain final outcome? We will calculate a case in which it can. The distinction is that we combine **amplitudes** before converting them to probabilities.

Start from the input/output distinction in [1.1](#sec-what-quantum-computing-computes-1). Our task here is to predict the final probabilities of two possible readouts, labelled 0 and 1. We will compare an explicit arithmetic model with an ideal FlagQuantum simulation. No physical experiment or finite-shot measurement is performed.

### A supplied model, with all arithmetic visible

For this preview, represent one qubit by a column of two **real amplitudes**, $a_0$ and $a_1$. The subscript labels the readout to which an amplitude belongs. Adopt the following rule:

$$
p_0=a_0^2,\qquad p_1=a_1^2,\qquad a_0^2+a_1^2=1.
$$

The last condition is **normalization**: the two readout probabilities add to one. An amplitude can be negative even though its squared probability cannot. This is a restricted model supplied for the example, not a derivation of quantum mechanics. General states use complex amplitudes and squared magnitudes; formal state and measurement postulates belong to 3.1 and 6.1. We need neither complex arithmetic nor those later results for this calculation.

We begin with amplitudes $(a_0,a_1)=(1,0)$, which predict readout 0 with certainty. Define an operation called the **Hadamard gate**, written $H$, by

$$
H=\frac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix},
\qquad
H\begin{pmatrix}a_0\\a_1\end{pmatrix}
=\begin{pmatrix}(a_0+a_1)/\sqrt2\\(a_0-a_1)/\sqrt2\end{pmatrix}.
$$

A matrix is a table of numbers. Its first row produces the new outcome-0 amplitude: multiply the first input by $1/\sqrt2$, the second by $1/\sqrt2$, then add. The second row does the same with coefficients $1/\sqrt2$ and $-1/\sqrt2$. These two row calculations define the displayed multiplication.

This gate preserves normalization in our real model. If the incoming entries are $a_0,a_1$, the sum of squared outgoing entries is

$$
\frac{(a_0+a_1)^2+(a_0-a_1)^2}{2}
=\frac{2a_0^2+2a_1^2}{2}
=a_0^2+a_1^2=1.
$$

The middle equality follows by expanding the two squares: their $+2a_0a_1$ and $-2a_0a_1$ terms cancel. Thus the operation and probability rule give a consistent normalized prediction for every normalized real input pair. This does not establish the general physical gate postulate.

### Two Hadamard gates: cancellation and reinforcement

Apply the first $H$ to the initial column:

$$
\begin{pmatrix}1\\0\end{pmatrix}
\xrightarrow{H}
\begin{pmatrix}(1+0)/\sqrt2\\(1-0)/\sqrt2\end{pmatrix}
=\begin{pmatrix}1/\sqrt2\\1/\sqrt2\end{pmatrix}.
$$

If we read out at this point, the model predicts $p_0=p_1=1/2$. Instead, apply another $H$, **without measuring between the gates**. Write $s=1/\sqrt2$, so $s^2=1/2$. The second gate gives

$$
a'_0=s(s+s)=s^2+s^2=1,\qquad
 a'_1=s(s-s)=s^2-s^2=0.
$$

The prime labels the new amplitudes. For outcome 0, the two contributions reinforce. For outcome 1, they cancel. Squaring only after adding gives

$$
p'_0=1^2=1,\qquad p'_1=0^2=0.
$$

This cancellation or reinforcement of amplitude contributions is **interference**. Here the two contributions refer to terms in the calculation; we are not asserting that the qubit followed two measured trajectories.

**Checkpoint 1.2-A.** Before squaring, which two numbers cancel in the outcome-1 amplitude? Why would replacing each number by its square first lose that cancellation?

### Change a relative sign, then recombine

Now insert a gate $Z$ between the two Hadamard gates. Define it by

$$
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\qquad
Z\begin{pmatrix}a_0\\a_1\end{pmatrix}
=\begin{pmatrix}a_0\\-a_1\end{pmatrix}.
$$

It leaves the first amplitude unchanged and reverses the second one's sign. After the first $H$ and then $Z$, the amplitudes are $(s,-s)$. Their immediate probabilities are still $(1/2,1/2)$: squaring hides the sign change. Apply the final $H$:

$$
a'_0=s(s-s)=0,\qquad
 a'_1=s(s+s)=1.
$$

Now outcome 0 cancels and outcome 1 reinforces. The final probabilities are $(0,1)$, the reverse of the two-$H$ experiment.

| Operations, in time order | Final amplitude pair | Final probabilities $(p_0,p_1)$ |
|---|---|---|
| $H$ | $(s,s)$ | $(1/2,1/2)$ |
| $H$, then $H$ | $(1,0)$ | $(1,0)$ |
| $H$, then $Z$, stopping there | $(s,-s)$ | $(1/2,1/2)$ |
| $H$, then $Z$, then $H$ | $(0,1)$ | $(0,1)$ |

Gate calls in code follow time order. Matrix products act from right to left: “$H$, then $Z$” is the product $ZH$ on the initial column. The final experiment is $HZH$ on that column. No intermediate readout is included in either sequence.

**Checkpoint 1.2-B.** If the final $H$ is omitted, can the immediate probabilities tell apart $(s,s)$ and $(s,-s)$? What changes when recombination is included?

### Locate the term that a probability-only calculation loses

For real amplitudes $a,b$ entering $H$, the outgoing outcome-0 probability is

$$
\left(\frac{a+b}{\sqrt2}\right)^2
=\frac{a^2+2ab+b^2}{2}
=\frac{a^2+b^2}{2}+ab.
$$

The term $ab$ comes from multiplying the two different amplitude contributions when expanding the square. It is positive for equal signs and negative for opposite signs. Adding only the squared contributions would omit it.

For $a=b=s$, the probability-only part is $1/2$ and $ab=1/2$, giving 1. For $a=s,b=-s$, the probability-only part is still $1/2$, but $ab=-1/2$, giving 0. Both cases have the same incoming probabilities and different outgoing predictions.

A wrong calculation treats the first $H$ as an ordinary coin toss and the second as another independent coin toss. For either final outcome it adds $1/4+1/4=1/2$. This is not our unmeasured amplitude model. An intervening measurement changes the experiment; its formal treatment is deferred to Chapter 6. The missing cross term already identifies the error in the unmeasured calculation.

### Formula to FlagQuantum code

The [complete program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/interference.py) contains an independent two-by-two matrix implementation using Python arithmetic. It checks the four hand-calculated cases above, then compares their amplitudes and probabilities with FlagQuantum.

| Mathematical step or contract | Code expression | What is checked |
|---|---|---|
| Initial column $(1,0)$ | `fq.Circuit(1, dtype=torch.complex128)` | One qubit, initially in the outcome-0 state |
| Apply $H$ or $Z$ | `circuit.h(0)` or `circuit.z(0)` | Qubit index 0; gate calls are in time order |
| Multiply a supplied matrix by a pair | `apply(matrix, pair)` | Each row's two contributions are added explicitly |
| Ideal final probabilities | `fq.run(circuit, outputs=[fq.probabilities()], options=OPTIONS)` | CPU, PyTorch, statevector mode, complex128; fallback and approximation disabled |
| Read one circuit's probabilities | `result.probabilities[0]` | Entries are ordered as readouts 0, 1 |
| Inspect simulated amplitudes | `result.statevector()[0]` | A diagnostic comparison with the independent reference, not a physical readout |
| Convert amplitudes to probabilities | `state[0].abs().square()` | This release uses complex tensors; squared magnitudes implement the rule |

The state and probability arrays have shape `(1, 2)`: one circuit result and two ordered coordinates. A real negative amplitude is stored as a complex number with zero imaginary part. No sampled shot record is returned.

From the repository root, install the pinned environment and run:

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell instead: .venv\Scripts\Activate.ps1
python -m pip install -r requirements-examples.txt
python examples/foundations/interference.py
```

Expected output:

```text
H: P(0)=0.500000000, P(1)=0.500000000
H then H: P(0)=1.000000000, P(1)=0.000000000
H then Z: P(0)=0.500000000, P(1)=0.500000000
H then Z then H: P(0)=0.000000000, P(1)=1.000000000
Probability-only recombination: P(0)=0.500000000, P(1)=0.500000000 (wrong for H then H)
Hand arithmetic, independent matrices, and FlagQuantum agree (atol=1e-12).
```

The comparisons use absolute tolerance $10^{-12}$ because a computer approximates $1/\sqrt2$. Nine printed decimal places do not mean that every internal value is exact. The extra checks include normalization, the wrong probability-only model, and a changed real input pair $(3/5,4/5)$, whose outcome-0 probability after $H$ is $49/50$, rather than $1/2$.

These are ideal simulation results for a supplied model. They do not demonstrate a hardware experiment, an arbitrary-precision computation or a computational advantage.

### Practice and accessible answers

**1.2-C — Transfer.** Start with $(0,1)$. Predict the amplitudes after the first $H$ and after the second $H$, showing both row calculations. Does $H$ twice always produce readout 0?

**1.2-D — Debugging.** A program replaces $(s,-s)$ by $(1/2,1/2)$ and then feeds those numbers into the final $H$ as amplitudes. Identify both the meaning error and the normalization error.

**1.2-E — Derivation.** Starting from a real pair $(a,b)$, apply the displayed $H$ rule twice. Show why the result is $(a,b)$, without citing a matrix identity from a later chapter.

**Answers and reasoning**

- **A.** The two terms are $s^2=1/2$ and $-s^2=-1/2$, whose sum is zero. Squaring each first makes both nonnegative and discards the relative sign needed for cancellation.
- **B.** Immediate probabilities cannot distinguish them. A final $H$ maps them to $(1,0)$ and $(0,1)$, which do have different readout probabilities. The next section will examine what this says about state descriptions and observed data.
- **C.** The first result is $((0+1)/\sqrt2,(0-1)/\sqrt2)=(s,-s)$. The second is $(s(s-s),s(s+s))=(0,1)$. Two $H$ gates return this input to itself; they do not reset every input to 0.
- **D.** Squared amplitudes are probabilities, a different kind of object. The replacement also has squared norm $1/4+1/4=1/2$, not 1. Renormalizing it would still lose the sign and give the wrong interference prediction.
- **E.** The first result is $((a+b)/\sqrt2,(a-b)/\sqrt2)$. Applying the rule again gives $((a+b+a-b)/2,(a+b-a+b)/2)=(a,b)$. Both signs and the factor $1/2$ are required. This proves the identity on the declared real model; general gate theory remains in its owning chapters.

### Sources, scope, and continuation

The supplied $Z$ and $H$ matrices are standard: Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010), §1.3.1, especially printed p. 19, Eqs. (1.13)–(1.14); [NC:1.3.1 source record](../references/proof-sources.md#source-nc-1-3-1). The row calculations, wrong-model diagnosis and exercises here are original. This section derives predictions within an adopted real-amplitude model; it does not prove physical postulates.

Local execution and unresolved reviews are recorded in [the section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/1.2.json). Mathematical and reader acceptance remain pending. Continue with [1.3 What a quantum state describes](#sec-what-quantum-computing-computes-3).

<span id="sec-what-quantum-computing-computes-3"></span>

## 1.3 What a quantum state describes

Suppose two preparations both give outcome 0 half the time and outcome 1 half the time. Do they prepare the same quantum state? The interference calculation in [1.2](#sec-what-quantum-computing-computes-2) gives us a way to test that conclusion. Equal predictions for one readout need not imply equal predictions for a different experiment.

We will keep the same real-amplitude preview and introduce no new quantum postulate. The goal is to separate three objects: a **state description**, a **measurement setting**, and the **data recorded from repetitions**. Confusing them can turn a valid simulator calculation into an invalid claim about an experiment.

### A state description predicts more than one histogram

Write $s=1/\sqrt2$. Starting from the amplitude pair $(1,0)$, define two preparations:

$$
A:\ H\quad\longrightarrow\quad(s,s),\qquad
B:\ H\text{, then }Z\quad\longrightarrow\quad(s,-s).
$$

Here $A$ and $B$ are labels for preparation procedures, not new gates. The pairs are their mathematical state descriptions within our supplied model. A state description is used, together with the specified operations and readout rule, to calculate predictions. It is not itself the recorded result of a shot.

We will use two **measurement settings**, meaning two specified procedures for obtaining a final outcome:

- **Direct:** prepare the qubit and read out the label 0 or 1 immediately.
- **Recombined:** prepare the qubit, apply $H$, then use the same 0-or-1 readout.

There is no measurement before the final readout in the recombined setting. Adding $H$ changes the overall measurement procedure even though the final readout labels remain 0 and 1.

For the direct setting, square the two amplitudes:

$$
A:\ (s^2,s^2)=(1/2,1/2),\qquad
B:\ (s^2,(-s)^2)=(1/2,1/2).
$$

For the recombined setting, use the row calculations already derived in 1.2:

$$
H(s,s)=(1,0),\qquad H(s,-s)=(0,1).
$$

Squaring these outgoing amplitudes gives the following predictions.

| Preparation | Direct probabilities $(p_0,p_1)$ | Recombined probabilities $(p_0,p_1)$ |
|---|---|---|
| $A$: amplitude pair $(s,s)$ | $(1/2,1/2)$ | $(1,0)$ |
| $B$: amplitude pair $(s,-s)$ | $(1/2,1/2)$ | $(0,1)$ |

The two descriptions contain a relative-sign distinction that the direct setting does not reveal. It matters because recombination can convert it into different readout probabilities. This is why storing only the direct probabilities would lose information needed to predict a later experiment.

**Checkpoint 1.3-A.** A file contains only the exact direct probabilities `(0.5, 0.5)`. Can a program infer whether to predict `(1, 0)` or `(0, 1)` after recombination? Identify the missing information.

### A shot, a record, and a distribution are different objects

For the direct setting, a single shot produces a label such as 1. It does not return `(s, -s)` or the pair `(0.5, 0.5)`. In the model, those are descriptions used to predict outcomes; 1 is one possible outcome.

To collect repeated data, prepare the qubit again for each shot, use the same setting and store each readout. Re-preparation matters: we are not claiming that repeatedly reading the same undisturbed qubit produces independent copies of the original experiment. Assume independent repetitions with the same probabilities, as in 1.1.

Consider the **constructed teaching record**

```text
0 1 0 1 1 0 0 1
```

Its histogram has four zeros and four ones. The empirical frequency of zero is therefore

$$
\widehat p_0=\frac{\text{number of zeros}}{\text{number of shots}}=\frac48=\frac12.
$$

The hat again marks an estimate computed from data. The value happens to equal the supplied model probability here. Another record need not contain equal counts.

Under either preparation in the direct setting, the probability of this particular **ordered** eight-shot record is

$$
\frac12\times\frac12\times\cdots\times\frac12
=\left(\frac12\right)^8=\frac1{256}.
$$

There are eight factors because independence lets us multiply one probability per shot. This is the probability of that exact sequence, not the probability of every sequence with four zeros. Under both preparations each specified bit has the same probability, so every possible ordered record has the same probability under $A$ as under $B$. Collecting more data using only this direct setting cannot separate these two models. It can improve an estimate of their common direct-readout distribution.

Changing to the recombined setting does separate them: in this ideal example, $A$ predicts only 0 and $B$ predicts only 1. That statement is specific to these two known candidate preparations and our ideal model. It does not establish a method for identifying an arbitrary unknown state from one shot, or a guarantee about noisy hardware.

**Checkpoint 1.3-B.** Eight direct readouts are all 1. Is that impossible under the supplied model? Does it select $B$ over $A$?

### What a simulator exposes

A statevector simulator stores numerical amplitude coordinates. Its software interface may let us inspect them. In contrast, a physical 0-or-1 readout produces the specified outcome label. These are different access contracts, in the sense of 1.1.

Inspecting amplitudes is useful for debugging a simulator program: it lets us check that the preparation applied the intended sign. It does not demonstrate that one device shot revealed that sign. Conversely, returning a sampled label is not a failed attempt to return an amplitude pair; it is the expected output of that readout procedure.

A numerical state description also includes conventions, such as which coordinate refers to outcome 0. We retain the order 0, then 1 throughout this example. We are not yet introducing a general equivalence criterion for state descriptions; Chapter 3 will supply it. The operational distinction needed here is the one we have calculated: these two preparations predict different results in the recombined setting.

### Formula, code, and the evidence boundary

The [complete program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/state_descriptions.py) reuses the supplied [1.2 matrix reference](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/interference.py). Both files are included in the repository. It evaluates each preparation in each setting, checks the state and probability coordinates against independent arithmetic, and calculates the probability of the constructed record.

| Object or calculation | Code | Interpretation |
|---|---|---|
| Preparation $A$ or $B$ | `preparation = ["h"]` or `["h", "z"]` | Gate sequence applied to the initial qubit |
| Measurement setting | `evaluate(preparation, recombine)` | Append `circuit.h(0)` only when recombination is requested |
| Predicted distribution | `result.probabilities[0]` | Ideal model probabilities ordered 0, 1; no shot data |
| Simulator state description | `result.statevector()[0]` | Privileged numerical diagnostic, not device readout |
| Constructed data | `record = [0, 1, 0, 1, 1, 0, 0, 1]` | Explicit teaching fixture, not a simulated or physical measurement run |
| Probability of an ordered record | `record_probability(record, model_a)` | Multiply the specified independent-shot probabilities using exact fractions |

After installing [the pinned example environment](https://github.com/FlagQuantum/modern-quantum-computing#run-the-examples), run from the repository root:

```bash
python examples/foundations/state_descriptions.py
```

Expected output:

```text
Preparation A: direct P(0)=0.500000000; after H P(0)=1.000000000
Preparation B: direct P(0)=0.500000000; after H P(0)=0.000000000
Constructed record: 01011001; zeros=4, ones=4
Probability of this ordered record: A=1/256, B=1/256
Fixture's second readout: 1 (not an amplitude pair)
State, setting, and record checks passed (atol=1e-12).
```

FlagQuantum 0.3.1 executes the ideal circuits on CPU using the PyTorch backend and complex128, with approximation and backend fallback disabled. State and probability comparisons use absolute tolerance $10^{-12}$. The record probabilities use exact rational arithmetic. There is no random sampling, seed, device execution or state-reconstruction procedure in this program.

### Transfer and debugging

**1.3-C — Choose evidence.** You are given either preparation $A$ or preparation $B$, with those as the only candidates. In the ideal preview, which of our two settings would you choose to distinguish them, and what would each outcome indicate? Explain why a direct-readout histogram cannot serve the same purpose.

**1.3-D — Change both signs.** Compare $(s,s)$ with $(-s,-s)$. Calculate their direct and recombined probabilities. Does our two-setting test distinguish them? Keep the conclusion limited to what you calculated.

**1.3-E — Repair a claim.** A report says: “The simulator printed amplitudes $(s,-s)$, so the physical experiment measured the relative sign in one direct readout.” Rewrite it as a statement supported by the program above, and name the additional setting that gives a sign-sensitive prediction for the supplied candidates.

**Answers and reasoning**

- **A.** No. Both preparations yield that file, but the relative amplitude sign needed for recombination is absent. The program needs the preparation/state description or additional experimental information.
- **B.** It is possible, with probability $1/256$ for that ordered record under either preparation. Equal probabilities do not force equal finite counts, and this record gives no distinction between $A$ and $B$ in the assumed model.
- **C.** Choose recombination followed by readout. Outcome 0 identifies $A$ and outcome 1 identifies $B$ within the ideal, two-candidate model. Direct-readout data have the same distribution for both, even with independent repetitions.
- **D.** Direct probabilities are $(1/2,1/2)$ for both. Recombination gives amplitudes $(1,0)$ and $(-1,0)$; both have probabilities $(1,0)$. These two settings do not distinguish them. Formal equivalence of state descriptions is developed later rather than inferred from this finite test alone.
- **E.** The simulator's internal amplitude coordinates match preparation $B$ in the supplied ideal model. No physical experiment was executed. Adding $H$ before readout yields the sign-sensitive prediction established above; the claim must specify that setting and its model assumptions.

A state description supplies predictions once the operations and readout are specified. A distribution describes possible outcomes for that procedure; a finite record is data from repetitions, or an explicitly labelled fixture. The next planned section, [1.4 Algorithms, simulators, and physical devices](../section-plans/01-foundations.md#sec-what-quantum-computing-computes-4), will separate the roles of those implementations more systematically.

### Companion source and review status

For the state/observation distinction, see Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010), §1.2, printed pp. 13–14, especially Eqs. (1.1)–(1.2); [NC:1.2 source record](../references/proof-sources.md#source-nc-1-2). The setting comparison, constructed record and exercises here are original teaching material. This is a conceptual preview with depth **P**; the formal mathematical state space and full measurement theory are taught in their owning chapters.

Execution details and outstanding reviews are in [the section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/1.3.json). Author checks are distinct from independent mathematical, implementation and reader review; acceptance remains pending.
