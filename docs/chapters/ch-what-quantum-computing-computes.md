# 1. What Quantum Computing Computes

**Working draft: sections 1.1–1.6 · Writing Baseline 1.0 · October 20, 2026.** Independent mathematical and reader review are pending; this is not an accepted chapter. Section 1.1 uses Python 3.12 and the standard library. Sections 1.2–1.4 add pinned FlagQuantum 0.3.1 simulations; 1.5–1.6 use standard-library cost and reading-route checks.

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

A state description supplies predictions once the operations and readout are specified. A distribution describes possible outcomes for that procedure; a finite record is data from repetitions, or an explicitly labelled fixture. The next section, [1.4 Algorithms, simulators, and physical devices](#sec-what-quantum-computing-computes-4), will separate the roles of those implementations more systematically.

### Companion source and review status

For the state/observation distinction, see Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010), §1.2, printed pp. 13–14, especially Eqs. (1.1)–(1.2); [NC:1.2 source record](../references/proof-sources.md#source-nc-1-2). The setting comparison, constructed record and exercises here are original teaching material. This is a conceptual preview with depth **P**; the formal mathematical state space and full measurement theory are taught in their owning chapters.

Execution details and outstanding reviews are in [the section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/1.3.json). Author checks are distinct from independent mathematical, implementation and reader review; acceptance remains pending.

<span id="sec-what-quantum-computing-computes-4"></span>

## 1.4 Algorithms, simulators, and physical devices

A circuit diagram, a simulator result and a device readout can all refer to the same computational task. They are different kinds of objects, and they support different claims. A program can implement the wrong algorithm correctly; a simulator can reproduce a model that omits important device effects; an experiment can disagree with a prediction without immediately revealing why.

Our prerequisite is the task contract in [1.1](#sec-what-quantum-computing-computes-1). We will supply a new one-bit example locally, so this section does not require the interference calculations in 1.2–1.3. The goal is to identify what specifies a computation, what calculates a model's predictions, and what constitutes experimental evidence.

### Keep one task fixed

Take an integer bit $b$, either 0 or 1. The requested output is the opposite bit, $y=1-b$. Thus

$$
f(0)=1,\qquad f(1)=0.
$$

Here $f$ names the bit-flip function, also called **NOT**. This is a classical input/output task; a quantum circuit can implement it without changing the requested answer. We choose a small example to make every boundary checkable, not to demonstrate a useful quantum speedup.

| Contract item | Our one-bit task |
|---|---|
| Input | One known classical bit $b$, supplied to the host program |
| Output | One classical bit $y$ |
| Mathematical correctness | $y=1-b$ |
| Ideal prediction | The correct output has probability one in the declared model |
| Resources to record | Input preparation, computational operations, readout and classical processing; also the simulator's work when simulation is used |

The mathematical task does not say which machine to use. A classical Python program can return `1 - bit`. Our alternative operational recipe is: prepare a qubit with the input label $b$, apply a gate that swaps labels 0 and 1, then read the output label. Call that gate $X$.

For this example, adopt the ideal rule that $X$ turns a certain label 0 into a certain label 1, and conversely. We are specifying a small model, not deriving a physical gate law. General gate theory is developed later. A **program** expresses the recipe in a language and API; it is distinct from both the task and the execution of that program.

**Checkpoint 1.4-A.** A program leaves the qubit at the input label and returns it. Has it satisfied the task merely because the returned value is a bit? Which input would reveal the mistake?

### Calculate the ideal reference before running a backend

Let $p_0,p_1$ denote the probabilities of the two labels. A certain input bit has probability pair $(1-b,b)$: input 0 gives $(1,0)$, while input 1 gives $(0,1)$. The supplied $X$ rule swaps those entries, giving the predicted output pair

$$
(q_0,q_1)=(b,1-b).
$$

The letters $q_0,q_1$ refer to output probabilities, not additional qubits. For $b=0$, the output probabilities are $(0,1)$, so the answer 1 is certain. For $b=1$, they are $(1,0)$, so the answer 0 is certain. This checks both allowed inputs and does not depend on FlagQuantum.

An **ideal simulator** is a classical program that computes predictions for a specified mathematical model. A statevector simulator stores numerical state coordinates and updates them according to the circuit. It can return ideal probabilities without generating a single sampled outcome. Floating-point arithmetic can introduce numerical error even when the simulated model contains no physical noise.

Agreement with the independent reference above checks our program on this task and the simulator's handling of these cases. It does not verify all simulator operations or establish the accuracy of a physical qubit.

### Express the recipe and inspect its execution

The [complete example](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/execution_evidence.py) uses the released FlagQuantum 0.3.1 package. A new `fq.Circuit(1, ...)` starts in the label-0 state. To encode a classical input of 1, the program first applies $X$. It then applies a separate computational $X$ for the NOT algorithm.

This distinction matters: for input 1, two $X$ calls appear in the source, but the first is preparation and the second is the computation. Input 0 needs no preparation flip. Preparation remains part of the execution contract even if a compiler later simplifies a gate sequence.

| Task, formula or evidence | Code expression | Meaning |
|---|---|---|
| Classical answer $1-b$ | `classical_not(bit)` | Independent truth-table reference |
| Input probability pair $(1-b,b)$ | `before = [1-bit, bit]` | Supplied certain-input model |
| Output pair $(b,1-b)$ | `[before[1], before[0]]` | Independent label-swap calculation |
| Initialize one qubit | `fq.Circuit(1, dtype=torch.complex128)` | Initial label 0 |
| Encode input 1 | First, conditional `circuit.x(0)` | Preparation of qubit index 0 |
| Perform NOT | Second `circuit.x(0)` | Computational step |
| Request ideal probabilities | `fq.run(..., outputs=[fq.probabilities()], options=OPTIONS)` | Statevector mode, PyTorch backend and CPU; approximation and backend fallback disabled |
| Read execution information | `result.runtime` and `result.provenance` | The installed release reports the local simulation path and selected device |

The probability tensor has shape `(1, 2)`: one circuit result, with entries ordered as labels 0 and 1. These numbers are predictions, not a physical bit record. The program also verifies that no samples were produced. It never chooses the largest probability and describes that choice as a measured shot. The simulator run is a validation calculation whose requested output is a probability distribution. It does not claim to return an experimental answer bit; in this deterministic model, its prediction identifies what a correct readout would return.

After installing [the pinned example environment](https://github.com/FlagQuantum/modern-quantum-computing#run-the-examples), run from the repository root:

```bash
python examples/foundations/execution_evidence.py
```

Expected output:

```text
input=0: classical answer=1; P(0)=0.000000000, P(1)=1.000000000
input=1: classical answer=0; P(0)=1.000000000, P(1)=0.000000000
Reported execution: local_statevector / pytorch_statevector / cpu
Independent truth-table and simulator checks passed (atol=1e-12).
Missing-gate and swapped-label errors detected.
Physical-qubit execution: not performed. Sampled records: none.
```

Comparisons use zero relative tolerance and absolute tolerance $10^{-12}$ with complex128 simulation. The independent reference is just the exact two-case probability table. To make the checks falsifiable, the program runs a deliberately broken circuit with the computational $X$ missing and separately reverses the output labels; both errors must be detected for both inputs. Passing an API call alone is not the acceptance criterion.

### What would make this a device experiment?

All computers are physical. Here **physical-qubit execution** means applying the circuit operations to an experimental qubit and collecting readout records, rather than using a CPU or GPU to simulate a model. Running software on a remote server, or seeing a cloud job identifier, does not by itself establish physical-qubit execution: the selected target may be a simulator.

A possible hardware experiment would prepare each input, execute the NOT step and collect a chosen number of readouts from repeated preparations. It would preserve the actual target and execution record, software/circuit versions, readout-label mapping, relevant calibration information, timestamps, failed attempts and raw results. The fraction of mismatches could then be compared with a declared error model and statistical acceptance rule.

**That experiment is proposed, not performed here.** We provide no hardware result, provider integration or device-specific accuracy claim. The ideal model predicts no wrong answers for this task. A wrong bit is therefore not ordinary finite-shot fluctuation under that exact model; preparation, control, readout, mapping or model assumptions would need investigation. For tasks with genuinely probabilistic ideal outputs, finite-count variation is a separate issue, as in 1.1.

| Evidence in this section | Supported conclusion | Conclusion it does not establish |
|---|---|---|
| Two-case mathematical calculation | The supplied ideal label-swap rule solves the task | A device obeys that rule perfectly |
| Executed classical reference and simulator comparisons | This program reproduces those ideal predictions on the recorded software path | Hardware fidelity or general simulator correctness |
| Runtime information reporting a local CPU statevector run | This execution used the specified simulation path | Physical-qubit execution |
| Proposed hardware procedure | A plan for collecting testable evidence | A measured result, accuracy value or speed comparison |

A simulator may expose internal amplitude coordinates that a physical readout does not return. That access has a classical computation and storage cost. In a full statevector method, each additional qubit doubles the number of amplitude coordinates; this is a property of that representation, not an inference that every simulation method has the same cost. Later chapters derive these resource models. A simulator's elapsed time is not the execution time of the physical circuit it represents.

### Classify a discrepancy before explaining it

**1.4-B — Numerical or logical?** A probability differs from the ideal reference by $2\times10^{-16}$ and passes the declared tolerance. Another run returns the input bit for both inputs because the computational gate was omitted. Classify the two discrepancies and name a check for each.

**1.4-C — Device evidence?** A report labels a cloud job “quantum execution” but supplies only an exact simulator probability array. What information is missing before it can support a physical-qubit claim?

**1.4-D — Sampling or model mismatch?** Someone attributes one wrong output from the ideal NOT model to “normal shot noise.” Is that explanation consistent with the supplied ideal probabilities? Contrast it with a task whose correct model assigns probability $1/2$ to each label.

**1.4-E — Transfer the contract.** Replace NOT by “return the input unchanged.” Give its two-case ideal output probabilities, identify the computational step to remove, and explain why input preparation still matters.

**Answers and reasoning**

- **A.** No. An output type is not a correctness condition. Either allowed input exposes the missing NOT: the unchanged bit is the wrong answer in both cases.
- **B.** The small difference is consistent with floating-point error at the declared tolerance; compare against the independent probability table and check whether it exceeds that tolerance. The missing gate is a program/algorithm mismatch, detected by the truth table for both inputs. Neither observation is device evidence.
- **C.** Identify the actual execution target and preserve the execution provenance and raw readout records, including their mapping to output labels. A job label or probability array alone does not show that physical qubit operations occurred. It may be a valid simulation result.
- **D.** No. In this ideal model the wrong label has probability zero, so sampling the exact distribution cannot produce it. A real wrong readout can motivate investigation of the idealization and execution chain. By contrast, a finite record from a half/half distribution need not have equal counts even when the model is correct.
- **E.** Input 0 predicts $(1,0)$ and input 1 predicts $(0,1)$. Remove the computational $X$, retaining the conditional preparation $X$ for input 1. Otherwise, both circuits would start at label 0 and would not encode the same task inputs.

We now have a common task spanning a mathematical recipe, a program, an executed simulator and an explicitly unexecuted device plan. The next section, [1.5 What computational advantage would require](#sec-what-quantum-computing-computes-5), uses these distinctions to examine resource comparisons.

### Validation standard and scope

The assigned methodological source is [ED:protocol](../references/proof-sources.md#source-ed-protocol), the book's original [reader-review and acceptance-evidence standard](../reader-continuity.md#reader-review-and-acceptance-evidence). It requires explicit assumptions, reconstructable steps and independent checks; it is not an external device experiment. The task, program, evidence classification and exercises here are original.

This section has depth **V**: it specifies falsifiable checks and the scope of their evidence, rather than proving a new quantum theorem. Author execution, environment details and outstanding reviews are recorded in [the section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/1.4.json). Independent mathematical/methodological review, implementation review and reader testing remain pending.

<span id="sec-what-quantum-computing-computes-5"></span>

## 1.5 What computational advantage would require

A computation has a fast central step. Does that make it a faster way to solve the problem? To answer, we need the whole task contract and the costs of completing it. Input preparation, repetitions and reading the answer can reverse a conclusion drawn from the central step alone.

Start from [1.4](#sec-what-quantum-computing-computes-4): an algorithm, an executed simulator and a physical device supply different kinds of evidence. Here we choose **elapsed time** as the resource to compare. Other studies may compare memory or function calls, but the resource and its units must be named. This section establishes a comparison method, not a quantum speedup theorem or a hardware performance result.

### Match the question before comparing the answers

Consider one concrete task. Both candidate methods receive the same nonempty classical array $x$ of $n$ bits, with entries $x_1,\ldots,x_n$. They must return a numerical estimate of its mean,

$$
\mu(x)=\frac{x_1+\cdots+x_n}{n}.
$$

The symbol $n$ is the array length; $\mu(x)$ is the fraction of entries equal to 1. Choose an allowed absolute error $\epsilon$ and failure probability $\delta$. With $\widehat\mu$ denoting the returned estimate, the required success condition is

$$
\Pr\!\left(\lvert\widehat\mu-\mu(x)\rvert\leq\epsilon\right)\geq1-\delta.
$$

The probability is over a method's randomness, if it uses any. A method that computes the exact mean deterministically also meets this requirement. For the example below, set $\epsilon=1/20$ and $1-\delta=19/20$. Those are shared requirements, not guarantees established by the cost calculation.

Call the candidates $C$ and $Q$: a classical workflow and a proposed workflow containing a quantum component. The letters label methods, not gates. We do not implement either solver here. Instead, we will see how a proposed cost comparison must be audited **even if both methods are eventually shown to meet the task contract**.

| Item to match | Why it matters |
|---|---|
| The same instance and input size | An easy small array cannot stand in for a different difficult one |
| Input representation and access | A classical array and a free callable that provides encoded data are different starting resources; constructing special access must be included |
| Output | A mean estimate, a sample and a full probability distribution are different requested answers |
| Error and success probability | A faster answer that misses the required accuracy or reliability does not solve the same task |
| Resource boundary | A central operation and a full time-to-answer measurement are different costs |

If a callable is used to return a data value, its invocation and construction costs must be specified. Giving one method such a callable for free while charging the other for loading the array changes the comparison. Formal access models are developed in Chapter 14; the immediate requirement is to state what each method is given and what it must build.

**Checkpoint 1.5-A.** Method $C$ computes an exact mean, while $Q$ returns one sampled bit. Can their running times establish a speedup for the stated mean-estimation task without further processing and analysis?

### A hypothetical ledger with explicit units

All numbers in this worked example are **invented costs**, expressed in microseconds for bookkeeping. No benchmark, simulator, quantum device or accuracy experiment produced them. They do not represent typical hardware speeds. Assume the stages run serially, with no overlap or amortization. We compare one task instance at a fixed agreed input size.

For $Q$, assume a one-time input/setup cost, $N$ repetitions, and final classical processing. In each repetition, charge separately for preparing the qubits, executing the computational operations and reading out:

$$
T_Q=T_{\mathrm{in}}+
N\bigl(t_{\mathrm{prep}}+t_{\mathrm{exec}}+t_{\mathrm{read}}\bigr)
+T_{\mathrm{post}}.
$$

Capital $T$ labels a whole-instance cost; lowercase $t$ labels a cost per repetition. Multiplication by $N$ converts each per-repetition cost into a total. Every term is therefore in microseconds. The input/setup term is charged once; preparation is charged anew for every repetition. Any actual input-dependent work repeated during preparation belongs in that repeated cost, not in a conveniently shared setup term.

Take $N=100$, input/setup 4000, preparation 20 per repetition, execution 10 per repetition, readout 20 per repetition and post-processing 2000. Then

$$
T_Q=4000+100(20+10+20)+2000=11000.
$$

For $C$, suppose input handling costs 2000, computation costs 7000 and output processing costs 1000:

$$
T_C=2000+7000+1000=10000.
$$

The choice $N=100$ is a cost assumption. We have not shown that it suffices for the chosen accuracy and success probability. An accuracy argument would have to determine an adequate repetition count before these numbers could support an actual performance claim.

| Stage | $C$ total, microseconds | $Q$ total, microseconds |
|---|---|---|
| Input/setup | 2000 | 4000 |
| Qubit preparation | Not applicable | $100\times20=2000$ |
| Computation | 7000 | $100\times10=1000$ |
| Qubit readout | Not applicable | $100\times20=2000$ |
| Output/post-processing | 1000 | 2000 |
| Whole task | 10000 | 11000 |

Ordinary classical input and output costs are included in their named rows. The ledger excludes queues and network delays; an experiment must disclose such exclusions. User time-to-answer may require including them. Shared setup can be amortized only when it is actually reusable, with comparable reuse and caching allowed for the classical baseline too.

### A fast component can belong to a slower workflow

Define the whole-task time ratio

$$
S=\frac{T_C}{T_Q}.
$$

If $S>1$, $Q$ takes less time under this boundary; if $S<1$, it takes more. The compute-only ratio is $7000/1000=7$, but the whole-task ratio is

$$
S=\frac{10000}{11000}=\frac{10}{11}\approx0.909091.
$$

Thus the faster computational component does not give a faster whole workflow in this ledger. Neither ratio establishes whether the methods meet the accuracy requirement.

Now omit just $Q$'s input/setup cost. Its apparent total becomes $11000-4000=7000$, giving a misleading whole-task ratio $10000/7000=10/7>1$. One omitted cost flips the conclusion. The arithmetic is consistent; the accounting boundary is wrong.

If $N$ changes from 100 to 200 with the same component prices, $Q$'s cost rises by $100(20+10+20)=5000$, to 16000. This is a sensitivity calculation, not a claim that doubling repetitions produces a particular error reduction. A stricter accuracy requirement calls for a fresh accuracy analysis and a fresh cost comparison for both candidates.

### Formula to executable bookkeeping

The [complete program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/advantage_ledger.py) calculates only the hypothetical ledger. It runs no candidate solver or quantum circuit. Python 3.12 and its standard library suffice.

| Expression or check | Code | Independent check |
|---|---|---|
| Classical whole-task cost | `sum(CLASSICAL.values())` | Expanded sum $2000+7000+1000$ |
| Quantum whole-task cost | `quantum_total(shots)` | Add all three repeated costs separately, plus setup and post-processing |
| Ratio $T_C/T_Q$ | `Fraction(classical, quantum)` | Exact rational value $10/11$ |
| Missing-input error | `quantum - QUANTUM["input"]` | Recompute the total as 7000 and observe the reversed conclusion |
| Additional repetitions | `quantum_total(200)` | Independently add 100 more complete repetitions, not just execution time |

Run from the repository root:

```bash
python examples/foundations/advantage_ledger.py
```

Expected output:

```text
Hypothetical costs only; no performance or accuracy experiment was run.
Shared target: absolute error <= 1/20, success probability >= 19/20 (not verified here).
Classical total: 10000 us = 10.000 ms
Quantum total, N=100: 11000 us = 11.000 ms
Compute-only ratio C/Q: 7 = 7.000000
End-to-end ratio C/Q: 10/11 = 0.909091
If quantum input cost is omitted: 7000 us; misleading ratio C/Q=10/7
At N=200: quantum total=16000 us (accuracy implications not inferred).
Expanded sums, units, and omitted-cost counterexample checks passed.
```

`Fraction` preserves exact ratios; decimals are for display. One millisecond is 1000 microseconds. Passing these checks verifies bookkeeping and the omitted-cost counterexample. It does not validate any invented duration, repetition requirement or device capability. No FlagQuantum API is needed merely to add a proposed cost ledger.

### What evidence would support an advantage claim?

For an empirical comparison, first establish that both implementations meet the same task and accuracy requirements on the stated inputs. Then record their complete costs under the declared boundary, environments, methods, input selection and uncertainty. A credible classical comparison must consider suitable algorithms and implementation quality; an unnecessarily slow baseline can manufacture an apparent advantage.

A fixed-size experiment compares the tested methods on the tested instances. It does not prove that every classical method must be slower. A statement about how resources grow with input size also requires explicit access, precision and success assumptions; one timing ratio cannot establish it. Chapter 14 and the algorithms chapters develop those formal arguments.

Simulator evidence has a further boundary. A fast classical statevector simulation can support a claim about that simulation program or validate a small quantum model. Its elapsed time is not the time a physical quantum device would take. Measured device costs, predicted device costs and simulator costs must remain separately identified.

### Transfer and diagnosis

**1.5-B — Restore a missing cost.** A report uses the ledger's whole-task classical cost but reports $Q$ as 7000 microseconds. Which stage was omitted, and what is the corrected ratio?

**1.5-C — Change precision.** A report halves the permitted error while retaining $N=100$ and its old timing. What must be established before carrying the original comparison over to the new task contract?

**1.5-D — Change the output.** One program returns all ideal probabilities; another returns one sampled bit. Why does the smaller output time not by itself establish an advantage for either original output task?

**1.5-E — Classify the evidence.** An author times a FlagQuantum CPU simulation and calls the result “measured quantum hardware speedup.” What conclusion could the timing support, and what additional evidence is missing?

**Answers and reasoning**

- **A.** No. A bit is not generally a mean estimate with the required error and reliability. The sampling method needs its estimator, repetition count, post-processing and accuracy analysis; those costs belong in the comparison.
- **B.** The missing stage is the 4000-microsecond input/setup cost. Restore $T_Q=11000$ and obtain $T_C/T_Q=10/11<1$.
- **C.** Check the estimator's error and success guarantee at the new tolerance, determine a sufficient repetition count and recompute relevant costs for both methods. The ledger alone provides no accuracy law. A genuinely exact classical solver may already meet both tolerances, but its performance still needs evidence.
- **D.** The requested outputs differ. Construct the same required output, include the cost of doing so and match accuracy and reliability before comparing times. Smaller output volume is not evidence that the original task has been solved faster.
- **E.** The timing can describe the classical simulator execution under its recorded conditions. It supplies no physical-device timing. A hardware claim needs an actual target/execution record, matched task-quality evidence and the complete comparison boundary.

The next section, [1.6 A map of the learning routes](#sec-what-quantum-computing-computes-6), connects such questions to the book's different study paths.

### Source, status, and limits

The assigned companion source is Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010), §3.2.1, printed pp. 136–137; [NC:3.2.1 source record](../references/proof-sources.md#source-nc-3-2-1). Its computational-resource discussion motivates declaring problem size and model. The mean-estimation contract, fictional costs and exercises here are original; no textbook data or measured benchmark is reproduced.

Depth **V**: specify a testable comparison and diagnose invalid evidence; no complexity separation or performance guarantee is proved. [The section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/1.5.json) separates author execution from pending independent methodological, implementation and reader review.

<span id="sec-what-quantum-computing-computes-6"></span>

## 1.6 A map of the learning routes

Suppose three readers open this book. One wants to predict an algorithm's answer, another wants to train a circuit, and a third wants to translate a program for a constrained processor. They share some foundations, but their next questions differ. Requiring all three to finish every physical platform and every advanced algorithm before doing useful work would hide that structure.

This section starts from [1.4](#sec-what-quantum-computing-computes-4): a task, a program, a simulator and a physical execution are different objects. We use that distinction to choose a destination, identify its entry knowledge and specify a first deliverable. No new quantum theorem is needed. The routes below are **plans with checked dependencies**, not a claim that their lessons are already written or tested with students.

### Start with an output, then choose a route

Write one sentence describing what you want to produce. “Learn quantum computing” is too broad to tell you which calculation to attempt next. “Predict the output distribution of a specified search circuit and state its input-access assumptions” supplies a calculation and an evidence boundary.

| Destination | Planned route after foundations | First bounded deliverable on that route | Boundary |
|---|---|---|---|
| Predict an algorithm's output | [Algorithms](../learning-paths.md#algorithms), Chapters 15–19 selections | A small oracle experiment: specify how the input is accessed, predict probabilities and check them against an independent calculation | A simulation checks the small model; it does not establish a speedup |
| Train a classical-quantum model | [Hybrid learning](../learning-paths.md#hybrid-learning), selections from Chapters 23, 24 and 27 | A scalar objective for a parameterized circuit, its derivative checked independently, and a recorded optimization update | An update alone establishes neither useful learning nor an advantage over classical models |
| Translate a program for a target | [Compiler core](../learning-paths.md#compiler-core), selections from Chapters 41–43 | A small program transformation, a declared target gate/connectivity contract and a check that the requested output behavior is preserved | A shorter gate list does not by itself prove lower device error or runtime |

These are destinations, not three new prerequisites for this section. Their technical terms receive definitions in their owning lessons. An **oracle** is an explicitly specified way an algorithm accesses problem information. A **parameter** is an adjustable number in a model; an **objective** is a numerical quantity used to judge its settings. A **target contract** states what operations and constraints a translation must respect. The table lets you recognize a future question without requiring its full solution now.

For a narrower training goal, the [VQE and optimization route](../learning-paths.md#variational) leads to energy minimization. A fixed circuit used to construct features or a similarity measure instead has a [fixed-kernel route](../learning-paths.md#fixed-kernels); it does not automatically require differentiating a trainable quantum layer. Select the route that matches the requested output, rather than treating every use of a classical computer alongside a quantum circuit as the same learning problem.

### What “assumes foundations” means

Each of these three routes assumes the **planned 64-section foundations route**, not merely this six-section opening chapter. That route supplies complex-vector arithmetic, states, registers, gates, measurement, entanglement, mixtures and computational resource models. Its [exact selection](../learning-paths.md#foundations) includes Chapter 14 alongside Chapters 1–8 selections. Chapter number alone is therefore not a prerequisite rule.

A beginner should next enter Chapter 2, beginning with [2.1 Complex scalars, vectors, and conjugation](ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-1). This is now a working draft. You do not need to know complex-vector notation to select a route here; the next lessons build it. An experienced reader can use a route's entry list to identify material to review, but should demonstrate the required calculations before treating that knowledge as acquired.

The [seven volumes](../volume-plan.md) organize presentation and reference use. They are not a command to finish Volumes I through VII in sequence. The compiler core can use an abstract target without first deriving superconducting or ion-trap control physics. Platform-specific lowering later imports its own physical assumptions. Similarly, general tensor contraction is not automatically downstream of every matrix-product-state technique. Follow the exact dependency list when entering a specialization.

### From a destination to a prerequisite-closed path

Here is a rule we can translate directly into code. A **direct prerequisite** is a section listed in another section's `requires` field. An **indirect prerequisite** is reached by following that field through one or more earlier sections. A path is **closed under prerequisites** when it includes both kinds, either as assumed prior knowledge or as new reading.

Let $T$ be the set of target section identifiers and $K$ the sections in the route's assumed earlier routes. Both are sets: an identifier occurs at most once. Let $P(s)$ denote the direct prerequisites of section $s$. Start with $R_0=T\cup K$, where $\cup$ means set union, and repeat

$$
R_{j+1}=R_j\cup\bigcup_{s\in R_j}P(s).
$$

The index $j$ counts passes through the rule. Each pass adds every prerequisite of the sections already included. Stop when a pass adds nothing; call that final set $R$. Because there are only 435 section identifiers and the sets only grow, the process terminates. The new reading is $R$ with the assumed set $K$ removed, ordered so that each prerequisite comes before the section that uses it. Canonical prerequisites already point to earlier entries in the curriculum; that order supplies such a sequence.

For a hand-sized check, suppose C requires B and B requires A. Start with C: the first pass adds B, the second adds A, and the third adds nothing. The answer is A, B, C. If A was already studied, the new reading is B, C. Merely printing B, C without that assumption leaves B's entry unmet.

| Planning rule | Complete example code | Check |
|---|---|---|
| Targets and assumed knowledge | `targets`, `known` in `resolve_routes` | Expand only the canonical target ranges and assumed routes |
| Add all prerequisites until stable | `closure(targets | known, sections)` | Compare the independent A–B–C example with the expected set |
| Remove assumed knowledge | `complete - known` | Count only the new reading |
| Check the ordered path | `check_order(study, known, sections)` | At each step require all direct prerequisites in `seen` |
| Diagnose a missing entry | Attempt 1.4 with no assumed knowledge | Report the missing 1.1 prerequisite |

The rule checks consistency with the recorded graph. If a necessary mathematical bridge was omitted from that graph, this program could still pass. Mathematical review and reader trials must check that separate question.

### Run the map check

The [complete program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/learning_routes.py) reads `book/curriculum.json` from a complete repository checkout. It checks all 19 routes and displays three. Python 3.12 and the standard library suffice; no FlagQuantum execution is needed to inspect a reading graph.

```bash
python examples/foundations/learning_routes.py
```

Expected output for Writing Baseline 1.0:

```text
Planning graph only; neither learner completion nor prose acceptance is certified.
algorithms: 64 assumed sections; 40 new sections; prerequisite order checked.
hybrid-learning: 64 assumed sections; 17 new sections; prerequisite order checked.
compiler-core: 64 assumed sections; 24 new sections; prerequisite order checked.
Broken entry detected: 1.4 requires 1.1.
Compiler core does not import QFT or microscopic platform chapters.
Tiny-chain reference, all 19 routes, and missing-entry checks passed.
```

“Assumed” is an editorial input, not a record of your learning. The program never tests your understanding. Its counts also do not measure pages, study time or available prose. Availability and review status are recorded separately in the [writing queue](../writing-order.md). At this section's initial publication, 1.1–1.6 are working drafts, with independent review pending; the other full sections remain unwritten. The earlier measurement, gradients and VQE pages are format pilots, rather than completed versions of their planned chapters.

There are runnable previews you can inspect now. [The interference program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/interference.py) and [its explained calculation](#sec-what-quantum-computing-computes-2) compare a hand-sized reference with released FlagQuantum 0.3.1. The [gradient pilot](gradients.md) has a [complete derivative-check program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/gradients.py), but assumes background not taught in this opening chapter. The compiler core currently has a checked plan, not a finished compiler tutorial or a claimed SDK implementation. These different statuses matter when choosing what you can study today.

### Other branches and entry diagnostics

The map also offers [information and security](../learning-paths.md#information), [error correction](../learning-paths.md#error-correction), [classical simulation](../learning-paths.md#simulation) and advanced [spectral algorithms](../learning-paths.md#spectral-algorithms). Hardware routes share entry models and then branch into superconducting, trapped-ion, neutral-atom, photonic, spin or topological systems. A research capstone, such as H₂ reproduction or logical memory, includes its own prerequisite closure. Choosing one branch does not make the others incorrect or unnecessary for every later purpose; it means their knowledge is not imported into this particular core task.

**1.6-A — Check entry knowledge.** Before entering Chapter 2, can you (i) compute the mean of `[0, 1, 1, 0]`, (ii) distinguish one sampled bit from that mean, and (iii) distinguish a simulator's predicted distribution from measured device data? State your answers in words as well as numbers. A difficulty here suggests reviewing 1.1 and 1.4, not skipping directly to a specialized route.

**1.6-B — Trace a dependency.** In the A–B–C example, A is already studied and the target is C. Which new sections are needed? What fails if the proposed new reading is only C?

**1.6-C — Transfer the choice.** You want to rewrite a small program to use an abstract target's allowed gates and compare its output behavior before and after. Which of the three routes fits? Must you first study microscopic models of every hardware platform? What extra knowledge becomes necessary if you later claim that the rewrite reduces a real device's error?

**Answers and reasoning**

- **A.** The mean is $2/4=1/2$. One sampled bit is 0 or 1; it is one record, not that mean. A simulator distribution follows from an implemented mathematical model. Device data require an actual execution and measurement record. Agreement on a small model alone is no speedup or hardware-performance claim.
- **B.** Read B, then C. With only C, its direct prerequisite B is missing even though the indirect prerequisite A is known.
- **C.** Choose compiler core after its foundations entry. Its abstract target does not require every microscopic platform. A physical error claim additionally needs the relevant platform/noise/control model, the target's actual execution conditions and appropriate evidence; a graph check or semantic equivalence alone supplies none of those.

### Chapter synthesis and next step

The opening chapter has separated a requested answer from the method used to obtain it, introduced a bounded interference preview, distinguished state descriptions from data, and explained why simulation and cost bookkeeping support limited claims. Keep those distinctions when the mathematics becomes more detailed.

**1.6-D — Chapter problem.** A report says: “We returned an ideal distribution from a simulator, removed half the gates and therefore trained a better model that will run twice as fast on hardware.” Identify four missing links in that reasoning. Write a narrower claim that the reported work could support.

**Answer D.** The requested task/output and success criterion are unspecified; gate removal needs a behavior-preservation check; better training needs a defined objective and evaluation evidence; hardware time needs a target and complete measured or explicitly modeled costs. An appropriately narrow claim is that a specified simulator program returned the reported distribution for the tested input. If the rewrite was independently checked, one may additionally report preserved behavior for those checked cases, with the method and scope stated.

Next, build the mathematical language rather than accumulating APIs. Chapter 2 begins with complex scalars and conjugation, then develops vectors and operators with explicit numerical checks. The [writing queue](../writing-order.md) tracks when that planned lesson becomes available.

### Source, status, and limits

The assigned source [ED:routes](../references/proof-sources.md#source-ed-routes) is this project's original editorial specification, [checked prerequisite paths](../learning-paths.md), derived from the canonical curriculum. The formula, miniature reference and diagnostic exercises explain that specification; they assert no quantum theorem or experimentally validated learning schedule.

Depth **V**: construct and check a prerequisite-closed reading path, then diagnose entry knowledge. [The section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/1.6.json) separates executed graph checks from pending independent methodological, implementation and reader reviews. Neither this section nor Chapter 1 is marked accepted.
