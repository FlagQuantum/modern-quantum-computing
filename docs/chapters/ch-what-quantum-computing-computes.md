# 1. What Quantum Computing Computes

**Working draft: section 1.1 only · Writing Baseline 1.0 · October 20, 2026.** Sections 1.2–1.6 remain planned. Independent mathematical and reader review are pending; this is not an accepted chapter. The accompanying reference program uses Python 3.12 and the standard library. No quantum backend is needed for this opening task specification.

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

You can now separate an instance from its encoding, specify a requested output and state how its correctness is judged. The next planned section, [1.2 A first interference experiment](../section-plans/01-foundations.md#sec-what-quantum-computing-computes-2), asks how a quantum model changes the probabilities from which outcomes are drawn. It will introduce its preview arithmetic locally.

### Source and validation note

For resource-model context, the assigned companion source is Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010), §3.2.1, printed pp. 136–137; [source record NC:3.2.1](../references/proof-sources.md#source-nc-3-2-1). That discussion motivates specifying input size and the computational model before comparing costs. The contracts, examples, synthetic data and finite probability verification above are original teaching material, not quotations or reproduced exercises from that book.

Proof-depth role: **P**, a task definition and its consequences; no new physical postulate or complexity theorem. Local execution details and unresolved review status are recorded in [the section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/1.1.json). Author checks are separate from independent mathematical review and target-reader testing; both remain pending.
