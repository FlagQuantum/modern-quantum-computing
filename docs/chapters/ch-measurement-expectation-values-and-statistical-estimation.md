# 6. Measurement, Expectation Values, and Statistical Estimation

**Working draft: section 6.1 · Writing Baseline 1.0 · October 22, 2026.** Author execution is separate from independent mathematical, implementation and reader review, which remain pending. Examples use released FlagQuantum 0.3.1 and PyTorch 2.13.0 on CPU with complex128 statevectors. The earlier measurement page remains a format pilot, rather than a substitute for this chapter.

<span id="sec-measurement-expectation-values-and-statistical-estimation-1"></span>

## 6.1 Measurement outcomes and the Born rule

A circuit prepares a quantum state; an experiment reports a classical outcome. To connect them, specify the measurement as well as the state. We begin with finite projective measurements and distinguish their probabilities from sampled outcomes and from the state after a measurement. Prerequisites are [3.1](ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-1), for normalized pure states and the one-qubit Born postulate; [4.1](ch-composite-systems-tensor-products-and-qubit-ordering.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), for tensor bases; and [2.5](ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-5), for orthogonal spectral subspaces.

Depth **P** means that the physical Born rule is stated as a postulate, with its mathematical consequences derived locally. Here a pure state is a normalized complex column vector on a finite register, and a reported event is a classical alternative. The ideal-state examples use full-vector/probability absolute tolerance $10^{-12}$ and relative tolerance zero, without backend fallback or approximate simulation. This numeric allowance is separate from the exact mathematical assumptions. No finite-shot or hardware observations are claimed.

<span id="formula-code-6-1-postulate"></span>

### 1. Declare the outcome labels and projectors before calculating

**Postulate.** Let $|\psi\rangle\in\mathbb C^d$ be normalized, with $\langle\psi|\psi\rangle=1$. A finite projective measurement is specified by a family $\mathcal P=\{P_a:a\in\mathcal A\}$ of matrices and distinct classical outcome labels a. Its conditions are

$$
P_a^\dagger=P_a,\qquad P_aP_b=\delta_{ab}P_a,\qquad
\sum_{a\in\mathcal A}P_a=I.
$$

Here $\delta_{ab}$ is one when the labels agree and zero otherwise; I is the identity on the entire state space. These conditions mean Hermitian projectors onto mutually orthogonal subspaces that together span the space. The **Born rule** assigns

$$
p(a\mid\psi,\mathcal P)=\langle\psi|P_a|\psi\rangle.
$$

The connection between this expression and a physical measurement outcome is a quantum postulate. We do not derive that physical law from matrix algebra or from unitary circuit simulation. We will derive its nonnegativity and normalization from the stated assumptions.

**First translation.** For one qubit in $\alpha|0\rangle+\beta|1\rangle$, computational measurement uses $P_0=\operatorname{diag}(1,0)$ and $P_1=\operatorname{diag}(0,1)$. Thus $p(0)=|\alpha|^2$ and $p(1)=|\beta|^2$. A label is the reported alternative, not its amplitude or probability. For $\beta=0.8i$, $\overline\beta\beta=0.64$; squaring β without complex conjugation would give −0.64 and is the wrong translation.

**FlagQuantum code → verification result.** This native query function is used cumulatively below. It requests exact ideal probabilities, not a sampled outcome. The leading execution dimension is removed with `[0]`; that index does not select qubit q0. The preparation matrix has first column (.6,.8i) and is unitary. `b.born` is an original classical projector checker/postprocessor, not a native general-measurement request.

```python
import math
import torch
import flagquantum as fq
import examples.foundations.projective_born as b
calls = 0
def query(circuit, selected=None):
    global calls
    request = fq.probabilities() if selected is None else fq.probabilities(qubits=selected)
    result = fq.run(circuit, outputs=[request], options=b.OPTIONS)
    raw, probabilities = result.statevector(), result.probabilities
    outcomes = 2**circuit.n_qubits if selected is None else 2**len(selected)
    assert raw.shape == (1, 2**circuit.n_qubits)
    assert probabilities.shape == (1, outcomes)
    assert raw.dtype == b.D and probabilities.dtype == torch.float64
    calls += 1
    return raw[0], probabilities[0]
prep = torch.tensor([[.6, .8j], [.8j, .6]], dtype=b.D)
v, native = query(fq.Circuit(1, dtype=b.D).unitary(0, unitary=prep))
projectors, labels = b.basis_family(1)
p = b.born(v, projectors, labels)
torch.testing.assert_close(v, torch.tensor([.6,.8j], dtype=b.D), rtol=0, atol=b.ATOL)
torch.testing.assert_close(p, native, rtol=0, atol=b.ATOL)
print('Computational labels:', labels, '; probabilities:', *(f'{x:.6f}' for x in p))
```
```text
Computational labels: ('0', '1') ; probabilities: 0.360000 0.640000
```

<span id="formula-code-6-1-normalization"></span>

### 2. Derive a normalized probability distribution without repairing it

**Formula.** Hermiticity and idempotence give

$$
p(a)=\langle\psi|P_a^\dagger P_a|\psi\rangle
=\|P_a\psi\|_2^2\ge0,\qquad
\sum_a p(a)=\left\langle\psi\middle|\sum_aP_a\middle|\psi\right\rangle=1.
$$

**Derivation.** Replace $P_a$ by $P_a^2=P_a^\dagger P_a$ inside the quadratic form. The resulting expression is the inner product of $P_a\psi$ with itself, a real nonnegative sum of squared magnitudes. Linearity moves the finite outcome sum inside the quadratic form; completeness replaces it by I, and the input norm supplies the final one. Since every term is nonnegative and their total is one, each is at most one. No extra division by a computed total is needed. For an unnormalized vector, the same calculation instead gives total $\|\psi\|_2^2$; it does not supply a normalized probability distribution.

An allowed outcome may have probability zero for a particular input. That is not a failed measurement specification, and its label is retained. Computing the vector component $P_a\psi$ here is a way to calculate a probability. This section does not normalize it into, or otherwise specify, a conditional output state; that requires the additional update discussion in 6.2.

**FlagQuantum code → verification result.** The helper checks the state norm and the whole projector family before returning probabilities in `labels` order. It uses projected squared norms and verifies agreement with the quadratic forms. It does not renormalize, clip negative values or discard zero-probability labels. Its tolerance validates finite floating-point data, rather than certifying exact projector identities for arbitrary inputs.

```python
v, native = query(fq.Circuit(1, dtype=b.D))
p = b.born(v, projectors, labels)
torch.testing.assert_close(p, torch.tensor([1.,0.], dtype=torch.float64), rtol=0, atol=b.ATOL)
torch.testing.assert_close(p, native, rtol=0, atol=b.ATOL)
assert p.min().item() >= 0 and abs(p.sum().item()-1) < b.ATOL
print('Normalized probabilities:', *(f'{x:.6f}' for x in p), '; zero-probability outcome retained.')
```
```text
Normalized probabilities: 1.000000 0.000000 ; zero-probability outcome retained.
```

<span id="formula-code-6-1-register"></span>

### 3. Match a register outcome to its statevector coordinate

**Formula.** For n qubits use the ordered tensor basis $|b_0\cdots b_{n-1}\rangle$, with q0 leftmost. For the outcome string b, its projector is $P_b=|b\rangle\langle b|$. If $|\psi\rangle=\sum_b\psi_b|b\rangle$, then

$$
P_b|\psi\rangle=\psi_b|b\rangle,\qquad p(b)=|\psi_b|^2.
$$

**Derivation.** Orthonormality gives $\langle b|c\rangle=\delta_{bc}$, so every term except c=b vanishes when the projector acts. The index convention is the one established in Chapter 4: $j=\sum_{q=0}^{n-1}b_q2^{n-1-q}$. Thus $|010\rangle$ is coordinate 2 and $|111\rangle$ coordinate 7, not qubit numbers 2 and 7. The raw statevector's leading execution dimension remains separate from all these qubit indices.

Prepare $\cos(\theta/2)|010\rangle+\sin(\theta/2)|111\rangle$ by Ry on q0, CNOT from q0 to q2 and X on q1. All other computational outcomes have probability zero. This is a joint distribution: its correlations need not equal a product of separate one-qubit probabilities.

**FlagQuantum code → verification result.** Check the full vector against the closed-form preparation, then its two nonzero probabilities against the corresponding outcome labels.

```python
theta = .8
v, native = query(fq.Circuit(3, dtype=b.D).ry(0, theta).cx(0,2).x(1))
reference = torch.zeros(8, dtype=b.D)
reference[2] = math.cos(theta/2); reference[7] = math.sin(theta/2)
torch.testing.assert_close(v, reference, rtol=0, atol=b.ATOL)
P3, labels3 = b.basis_family(3)
p = b.born(v, P3, labels3)
torch.testing.assert_close(p, native, rtol=0, atol=b.ATOL)
assert labels3[2] == '010' and labels3[7] == '111'
print('p(010), p(111):', *(f'{p[j]:.6f}' for j in (2,7)))
```
```text
p(010), p(111): 0.848353 0.151647
```

<span id="formula-code-6-1-partial"></span>

### 4. Predict a partial outcome by summing compatible joint events

**Formula.** Let $S=(s_0,\ldots,s_{k-1})$ be an ordered selection of distinct qubits. For the reported k-bit string a, define

$$
P_a^{(S)}=\sum_{b:\,(b_{s_0},\ldots,b_{s_{k-1}})=a}|b\rangle\langle b|,
\qquad
p_S(a)=\sum_{b:\,b_S=a}|\psi_b|^2.
$$

**Derivation.** Different complete basis strings are orthogonal, so summing their diagonal rank-one projectors produces a projector onto the compatible subspace. The compatible groups are disjoint and cover the full basis; therefore these partial-outcome projectors are mutually orthogonal and complete. Applying the Born rule gives the displayed marginal sum. This calculates the probability of a partial record, not the state of an ignored qubit after a physical measurement.

For $S=(2,0)$, a='01' means q2=0,q0=1, with q1 unrestricted. It does not mean the two leftmost qubits. For the product preparation below, q0 probabilities are (.36,.64) and q2 probabilities (.7,.3). Hence the ordered q2,q0 probabilities are (.252,.448,.108,.192). Reversing the selected order transposes the middle two entries.

**FlagQuantum code → verification result.** `fq.probabilities(qubits=...)` is a native exact computational marginal request. `marginal_family` independently builds its projectors in that same declared label order. The complete program verifies every nonempty ordered selection of three qubits, including all basis inputs.

```python
factors = [(.6,.8j), (1,0), (math.sqrt(.7), math.sqrt(.3)*complex(math.cos(.2),math.sin(.2)))]
for selected in ((2,0), (0,2)):
    circuit = fq.Circuit(3, dtype=b.D)
    for q, factor in enumerate(factors):
        circuit.unitary(q, unitary=b.prepare_matrix(torch.tensor(factor,dtype=b.D)))
    v, native = query(circuit, selected)
    Ps, names = b.marginal_family(3, selected)
    p = b.born(v, Ps, names)
    torch.testing.assert_close(p, native, rtol=0, atol=b.ATOL)
    print('selected', selected, ':', *(f'{x:.6f}' for x in p))
```
```text
selected (2, 0) : 0.252000 0.448000 0.108000 0.192000
selected (0, 2) : 0.252000 0.108000 0.448000 0.192000
```

<span id="formula-code-6-1-coarse"></span>

### 5. Coarse outcome probabilities add; scalar amplitudes do not

**Formula.** Group fine outcomes into disjoint sets $G_r$ covering all fine labels. The coarse projector is $Q_r=\sum_{a\in G_r}P_a$, giving

$$
Q_r^2=\sum_{a,b\in G_r}P_aP_b=\sum_{a\in G_r}P_a=Q_r,
\qquad p(r)=\sum_{a\in G_r}p(a).
$$

**Derivation.** Mutual orthogonality removes every cross product with a≠b. Hermiticity, orthogonality between different groups and completeness follow from the same conditions on the fine family. The Born quadratic form is linear in its projector, so its probabilities add. Equivalently the vector components $P_a\psi$ remain orthogonal when their norms are squared. This is not the squared magnitude of a sum of scalar coefficients placed into one coordinate.

For two-qubit computational parity,
$Q_{\rm even}=|00\rangle\langle00|+|11\rangle\langle11|$ and
$Q_{\rm odd}=|01\rangle\langle01|+|10\rangle\langle10|$ are rank-two projectors. The state $(|00\rangle+|11\rangle)/\sqrt2$ has even probability one, whereas $|\psi_{00}+\psi_{11}|^2=2$ is not that probability. Predicting this coarse record does not assert which physical instrument was used or how much coherence remains afterward; probability grouping alone does not specify a state update.

**FlagQuantum code → verification result.** The parity values are classical projector postprocessing of the simulated state. Native computational probabilities provide an independent sum for the same reported parity event.

```python
v, native = query(fq.Circuit(2, dtype=b.D).h(0).cx(0,1))
parity, parity_labels = b.parity_family(2)
p = b.born(v, parity, parity_labels)
reference = torch.stack([native[0]+native[3], native[1]+native[2]])
torch.testing.assert_close(p, reference, rtol=0, atol=b.ATOL)
wrong_scalar_sum = abs(v[0]+v[3])**2
assert abs(p[0].item()-1) < b.ATOL and abs(wrong_scalar_sum.item()-2) < b.ATOL
print('Even probability / wrong scalar-amplitude sum:', f'{p[0]:.6f}', f'{wrong_scalar_sum:.6f}')
```
```text
Even probability / wrong scalar-amplitude sum: 1.000000 2.000000
```

<span id="formula-code-6-1-family"></span>

### 6. The measurement family matters even when computational probabilities agree

**Formula.** Define $X=\begin{pmatrix}0&1\\1&0\end{pmatrix}$ and $M=X\otimes X$, which flips both bits. Since $M^\dagger=M$ and $M^2=I$, the matrices

$$
P_+=\frac{I+M}{2},\qquad P_-=\frac{I-M}{2}
$$

form another complete orthogonal rank-two family. Indeed $P_\pm^2=(I\pm2M+M^2)/4=P_\pm$, $P_+P_-=(I-M^2)/4=0$ and $P_++P_-=I$; Hermiticity follows from that of M. These projectors have off-diagonal entries in the computational basis.

**Derivation for a phase-sensitive example.** Let
$|\psi_\phi\rangle=(|00\rangle+e^{i\phi}|11\rangle)/\sqrt2$.
Computational probabilities remain (.5,0,0,.5), and computational parity remains even with certainty. But

$$
P_+|\psi_\phi\rangle=\frac{1+e^{i\phi}}{2\sqrt2}(|00\rangle+|11\rangle),\qquad
p(+)=\frac{1+\cos\phi}{2},\quad p(-)=\frac{1-\cos\phi}{2}.
$$

For P− the two coefficients are $(1-e^{i\phi})/(2\sqrt2)$ and its negative. Squaring these two orthogonal coordinate magnitudes gives $(1-\cos\phi)/2$. Thus a state and a measurement family are both needed to predict an outcome. There is no single distribution of bitstring probabilities that replaces every projective question about the state.

**FlagQuantum code → verification result.** The circuit prepares the state, and the native query supplies computational probabilities. The off-diagonal projector values are explicitly evaluated on its statevector by the book helper. This is an ideal small-system prediction, not a claim that the probability-query API directly performs arbitrary projective measurements on hardware. A basis-change measurement protocol is reserved for 6.4.

```python
XX, xx_labels = b.xx_family()
for phi in (0., math.pi/2, math.pi):
    v, native = query(fq.Circuit(2, dtype=b.D).h(0).cx(0,1).p(0,phi))
    p = b.born(v, XX, xx_labels)
    closed = torch.tensor([(1+math.cos(phi))/2,(1-math.cos(phi))/2], dtype=torch.float64)
    torch.testing.assert_close(p, closed, rtol=0, atol=b.ATOL)
    torch.testing.assert_close(native, torch.tensor([.5,0,0,.5],dtype=torch.float64), rtol=0, atol=b.ATOL)
    print(f'phi/pi = {phi/math.pi:.1f}: p(plus), p(minus) =', *(f'{x:.6f}' for x in p))
```
```text
phi/pi = 0.0: p(plus), p(minus) = 1.000000 0.000000
phi/pi = 0.5: p(plus), p(minus) = 0.500000 0.500000
phi/pi = 1.0: p(plus), p(minus) = 0.000000 1.000000
```

<span id="formula-code-6-1-phase"></span>

### 7. Keep global state phase separate from the relative phase being measured

**Formula and derivation.** For any real χ and any fixed projector,

$$
\langle e^{i\chi}\psi|P_a|e^{i\chi}\psi\rangle
=e^{-i\chi}e^{i\chi}\langle\psi|P_a|\psi\rangle=p(a).
$$

The same scalar multiplies the entire ket, and conjugation supplies its inverse on the bra. Unit 6 changes a relative phase between two coordinates instead; that phase cannot be factored out of the entire state. This is the state-ray invariance from 3.1, now for every projective family. It is not permission to erase the phase of a unitary block before coherently controlling that block; that distinct operator-context question was addressed in 3.7 and 5.2.

**FlagQuantum code → verification result.** Multiply the prepared two-qubit state by a global phase using the one-qubit scalar matrix $e^{i\chi}I$ on q0. The full vectors differ by that scalar, while both computational and XX-family probabilities agree. No numerical phase alignment or renormalization is needed.

```python
phase_results = []
for chi in (0., .71):
    scalar = complex(math.cos(chi), math.sin(chi))
    circuit = (fq.Circuit(2, dtype=b.D).h(0).cx(0,1).p(0,.43)
               .unitary(0, unitary=scalar*torch.eye(2,dtype=b.D)))
    v, native = query(circuit)
    phase_results.append((v, native, b.born(v, XX, xx_labels)))
torch.testing.assert_close(phase_results[1][0], complex(math.cos(.71),math.sin(.71))*phase_results[0][0], rtol=0, atol=b.ATOL)
for index in (1,2):
    torch.testing.assert_close(phase_results[0][index], phase_results[1][index], rtol=0, atol=b.ATOL)
print('Global phase changes the vector by its scalar; computational and XX-family probabilities stay equal.')
```
```text
Global phase changes the vector by its scalar; computational and XX-family probabilities stay equal.
```

<span id="formula-code-6-1-contracts"></span>

### 8. Reject a broken projective contract instead of returning repaired numbers

**Conditions → failure boundaries.** Completeness is a property of the whole measurement family, not of one test state. Keeping only $P_0$ can give total probability one on $|0\rangle$ but misses $|1\rangle$; it is not a complete family on the qubit space. Repeating overlapping projectors is not an exclusive-outcome partition. Hermitian idempotence also matters: the positive complete pair $(I/2,I/2)$ is a possible generalized-measurement effect family, but is not a family of projectors. It is outside this helper's contract, not declared impossible physics; generalized measurements enter in 6.5.

The helper accepts normalized, unbatched CPU complex128 vectors and equally shaped projector matrices, with distinct declared string labels. Its d≤16 teaching guard supports at most four qubits and is not a FlagQuantum limit. It tests Hermiticity, idempotence, pairwise orthogonality and completeness with absolute tolerance 10⁻¹² and relative tolerance zero. Such floating-point admission checks do not constitute a proof or an interval certificate for approximate data.

**Code → verification result.** Reject the missing conditions explicitly, including malformed qubit selections before native execution. The result is a probability vector in the supplied label order. No sampled record, post-measurement state, mixed-state channel, noise model, expectation estimator or hardware result is returned. The statevector used above describes the simulated unitary preparation; requesting probabilities has not established that a physical projective state update occurred.

```python
state = torch.tensor([1,0], dtype=b.D)
P, names = b.basis_family(1); I = torch.eye(2,dtype=b.D)
oblique = torch.tensor([[1,1],[0,0]], dtype=b.D)
invalid = [lambda: b.born(2*state,P,names), lambda: b.born(torch.zeros_like(state),P,names),
           lambda: b.born(state.real,P,names),
           lambda: b.born(torch.tensor([float('nan'),0],dtype=b.D),P,names),
           lambda: b.born(state,(oblique,I-oblique),names), lambda: b.born(state,(I/2,I/2),names),
           lambda: b.born(state,P[:1],names[:1]),
           lambda: b.born(state,(P[0],P[0],P[1]),('a','b','c')),
           lambda: b.born(state,P,('same','same')),
           lambda: b.born(state,(torch.eye(4,dtype=b.D),),('all',)),
           lambda: b.marginal_family(3,(0,0)), lambda: b.marginal_family(3,(True,))]
for call in invalid:
    try:
        call()
    except ValueError:
        pass
    else:
        raise AssertionError('Broken projective contract admitted')
assert calls == 11
print('Twelve malformed contracts rejected; eleven actual body circuits; no probability or state repair.')
```
```text
Twelve malformed contracts rejected; eleven actual body circuits; no probability or state repair.
```

### Complete program and expected output

Run `python examples/foundations/projective_born.py` from the repository root. The [complete program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/projective_born.py) executes 163 actual circuits: 17 full computational cases, 135 native ordered marginal cases, 8 phase-sensitive/global-phase cases and 3 sparse-register preparations. All native probabilities are independently checked against explicit projector norms, scalar sums or closed-form states. The complete computational tests cover every basis input and a complex product for one, two and three qubits. General projectors are evaluated by explicit classical postprocessing of the simulated state, with no claimed native general-measurement request. The body checker executes the eight cumulative snippets above, with eleven actual native queries and exact expected-output comparison.

Expected output of the complete program:

```text
17 computational-basis circuits: all 1/2/3-qubit basis inputs and complex products; full vectors, Born probabilities and parity sums passed.
135 native marginal circuits: all 15 ordered nonempty qubit selections, all 8 basis inputs and a complex product passed.
8 phase-sensitive Bell circuits: explicit XX-projector postprocessing matches the cosine law; global phase leaves every probability unchanged.
3 sparse-register circuits: 010/111 amplitudes and indices 2/7 checked at zero, generic and pi angles.
12 malformed contracts rejected; zero-probability labels retained; no renormalization, clipping or state-update inference.
163 actual CPU complex128 circuits; implementation atol 1e-12, rtol 0; exact probabilities, not finite-shot or hardware observations.
General projectors are explicit classical postprocessing of a simulated state; not a claimed native general-measurement API.
```

### Understanding checks and transfer exercises

**6.1-A — A larger marginal.** Prepare a four-qubit input and apply Ry(q0,−.37),CX(q0,q3). Request outcomes ordered as (q3,q1). Check every basis input and a complex product against the complete-state compatible-event sum. Does the leading result dimension name q3?

**6.1-B — A new projective family.** Let $B_{jk}=e^{2\pi i jk/4}/2$ for j,k=0,1,2,3, with orthonormal columns $|b_k\rangle$. Form Q0 from columns 0,1 and Q1 from columns 2,3. For a new prepared two-qubit state, compare the two projector probabilities with sums of squared overlaps. Is this a native hardware measurement?

**6.1-C — An apparently successful incomplete family.** Why does evaluating only P0 on $|0\rangle$ fail to establish a valid qubit measurement family? Does a zero-probability outcome require removing its label?

**6.1-D — Which claim is a postulate?** Separate the physical probability rule, its normalization proof and the prediction of a conditional output state. Why is an exact probability query not one experimental shot?

<details markdown="1">
<summary>Answers and reasoning</summary>

**A.** For label a, sum full probabilities over strings b whose q3,q1 bits equal a in that order. The corresponding projector is diagonal on precisely those strings; it includes q0,q2 as unrestricted coordinates. `[0]` removes one execution dimension, not a qubit dimension. The separate author transfer executes 17 four-qubit cases, checking the prepared vectors with an independent indexed-gate reference and then the native marginal with compatible-index sums.

**B.** Orthogonality follows from the finite geometric sum $\sum_{j=0}^3e^{2\pi i j(k-\ell)/4}=4\delta_{k\ell}$. Thus $Q_0=\sum_{k=0}^1|b_k\rangle\langle b_k|$, $Q_1=\sum_{k=2}^3|b_k\rangle\langle b_k|$ are orthogonal complete rank-two projectors. Their probabilities are respectively $\sum_{k=0}^1|\langle b_k|\psi\rangle|^2$ and $\sum_{k=2}^3|\langle b_k|\psi\rangle|^2$. The separate author transfer uses three new prepared states, adding three circuits for twenty transfer circuits total. It computes classical predictions on simulated vectors and does not execute a general-projector hardware measurement. It is author validation, not independent review.

**C.** The missing P1 subspace makes the family incomplete; on input $|1\rangle$ its total would be zero. Completeness must hold on the full state space. A zero-probability event for a particular input is compatible with a complete family and retains its label.

**D.** Interpreting $\langle\psi|P_a|\psi\rangle$ as an outcome probability is the physical postulate. Nonnegativity and unit total follow from Hermitian orthogonal complete projectors and normalization. A conditional state additionally needs an update rule, treated in 6.2. A probability query returns deterministic ideal model predictions; a shot would return one label according to an outcome distribution, with finite-sample reasoning developed in 6.6.

</details>

### Sources, depth and next step

Assigned background is Nielsen and Chuang, 10th Anniversary Edition (2010), §2.2.5, beginning at printed page 87. Its assigned locator is retained; no fresh inspection of the user-local textbook PDF is claimed. For a publicly accessible author source, [John Preskill, Caltech Ph219/CS219 Chapter 3, §3.1.1](https://www.preskill.caltech.edu/ph219/chap3_15.pdf), equation (3.11) and the probability statement (3.15) on PDF page 7, were checked. The currently served PDF labels its update **October 2018**, despite the `_15` filename. We use only the finite projective-probability statement here; pointer dynamics, conditional-state formulas and generalized measurements are outside this section's scope.

The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/6.1.json) separates author checks from independent mathematical review, implementation review and reader trials, which remain pending. This remains a working draft. The existing [measurement starter](measurement.md) retains its separate format-pilot status. Continue, when drafted, with [6.2 Conditional states and ignored outcomes](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-2).
