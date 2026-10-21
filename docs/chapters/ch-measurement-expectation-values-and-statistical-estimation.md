# 6. Measurement, Expectation Values, and Statistical Estimation

**Working drafts: sections 6.1–6.2 · Writing Baseline 1.0 · October 22, 2026.** Author execution is separate from independent mathematical, implementation and reader review, which remain pending. Examples use released FlagQuantum 0.3.1 and PyTorch 2.13.0 on CPU with complex128 statevectors. The earlier measurement page remains a format pilot, rather than a substitute for this chapter.

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

The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/6.1.json) separates author checks from independent mathematical review, implementation review and reader trials, which remain pending. This remains a working draft. The existing [measurement starter](measurement.md) retains its separate format-pilot status. Continue with [6.2 Conditional states and ignored outcomes](#sec-measurement-expectation-values-and-statistical-estimation-2).

<span id="sec-measurement-expectation-values-and-statistical-estimation-2"></span>

## 6.2 Conditional states and ignored outcomes

Section [6.1](#sec-measurement-expectation-values-and-statistical-estimation-1) gives probabilities for a projective measurement. If its outcome is recorded and another experiment follows, what state should that experiment use? What changes when the first outcome is unavailable? A probability vector alone does not answer either question.

Our scope is a normalized **pure global state** $|\psi\rangle$ and a finite complete orthogonal family $\{P_a\}$. We explicitly assume an **ideal projective, or Lüders, update**: the selected component is retained without an additional rotation inside or outside its subspace. This is an additional physical update assumption, not a theorem derived from the Born probabilities. Depth **F** requires complete derivations of normalization and selective/joint/marginal probabilities under this assumption. We give those proofs below. The density-operator update remains in Chapter 8.

Examples use FlagQuantum 0.3.1/PyTorch 2.13.0, CPU complex128, with absolute implementation tolerance $10^{-12}$ and relative tolerance zero. The native calls prepare pure states and query exact computational probabilities. Our branches and joint helpers then perform **explicit classical postprocessing**, rather than invoking a native collapse, reset, hardware or shot API. Enumerating branches predicts an ideal experiment; it does not observe an actual outcome.

<span id="formula-code-6-2-selective"></span>

### 1. Normalize a selected component without changing its phase

**Formula and assumption.** For $p_a=\|P_a\psi\|_2^2>0$, the ideal conditional global state is

$$
|\psi_a\rangle=\frac{P_a|\psi\rangle}{\sqrt{p_a}}.
$$

**Derivation.** The update assumption selects the direction $P_a\psi$. Its length is $\sqrt{\langle P_a\psi|P_a\psi\rangle}=\sqrt{p_a}$. Dividing by this positive real number gives $\langle\psi_a|\psi_a\rangle=p_a/p_a=1$. Our helper uses exactly this phase representative. For $|\psi\rangle=.6|0\rangle+.8i|1\rangle$, outcome 1 has $P_1\psi=.8i|1\rangle$, $p_1=.64$ and $|\psi_1\rangle=i|1\rangle$. Although $i|1\rangle$ has the same isolated-state probabilities as $|1\rangle$, silently changing its vector would break the declared formula-to-code comparison.

**FlagQuantum code → verification result.** Execute these snippets cumulatively from the repository root in the pinned example environment. The leading native-result dimension is an execution batch, removed with [0]. After the query, the ideal conditional rule is evaluated classically.

```python
import math
import torch
import flagquantum as fq
import examples.foundations.conditional_states as c
b = c.b
calls = 0
def query(circuit, selected=None):
    global calls
    request = fq.probabilities() if selected is None else fq.probabilities(qubits=selected)
    result = fq.run(circuit, outputs=[request], options=b.OPTIONS)
    v, probabilities = result.statevector(), result.probabilities
    assert v.shape == (1, 2**circuit.n_qubits)
    assert probabilities.shape == (1, 2**(circuit.n_qubits if selected is None else len(selected)))
    assert v.dtype == b.D and probabilities.dtype == torch.float64
    calls += 1
    return v[0], probabilities[0]
prep = torch.tensor([[.6,.8j],[.8j,.6]], dtype=b.D)
qubit, native = query(fq.Circuit(1,dtype=b.D).unitary(0,unitary=prep))
Z, zn = b.basis_family(1)
p, states = c.branches(qubit,Z,zn)
projected = Z[1] @ qubit
normalized = projected / torch.sqrt(p[1])
torch.testing.assert_close(states[1],normalized,rtol=0,atol=b.ATOL)
torch.testing.assert_close(p,native,rtol=0,atol=b.ATOL)
torch.testing.assert_close(states[1],torch.tensor([0,1j],dtype=b.D),rtol=0,atol=b.ATOL)
print('Probabilities:',*(f'{x:.6f}' for x in p),'; selected 1:',states[1].tolist())
```
```text
Probabilities: 0.360000 0.640000 ; selected 1: [0j, 1j]
```

For $p_a=0$, the normalized expression is undefined. It is not the zero vector, which is not a quantum state. The helper retains this outcome label with a conditional value of None; explicitly requesting an impossible branch raises an error.

<span id="formula-code-6-2-register"></span>

### 2. A partial measurement conditions the entire register

**Formula.** Write $|\psi\rangle=\sum_b\alpha_b|b_0\cdots b_{n-1}\rangle$. For ordered selected qubits $S=(s_0,\ldots,s_{k-1})$ and a k-bit label a, let $b_S=(b_{s_0},\ldots,b_{s_{k-1}})$. Then

$$
P_a=\sum_{b:\,b_S=a}|b\rangle\langle b|,\qquad
p_a=\sum_{b:\,b_S=a}|\alpha_b|^2,
$$

$$
(\psi_a)_b=
\begin{cases}
\alpha_b/\sqrt{p_a},&b_S=a,\\
0,&b_S\ne a.
\end{cases}
$$

**Derivation.** Each diagonal projector term keeps one compatible coordinate. Applying $P_a$ masks incompatible bitstrings while preserving every compatible amplitude, including coherence among unmeasured coordinates. Its squared norm is the compatible sum; dividing gives the displayed branch coordinates. This proves the formula for arbitrary joint amplitudes, including entangled inputs. The output still has $2^n$ entries: measured qubits are not deleted and unmeasured qubits are not independently re-prepared.

Take $|\psi\rangle=\cos(\theta/2)|010\rangle+\sin(\theta/2)|111\rangle$. Measuring $(q_2,q_0)$ selects full-register index 2 for label 00 and index 7 for label 11. Labels 01 and 10 have zero probability for this input.

```python
theta = .8
register, native = query(fq.Circuit(3,dtype=b.D).ry(0,theta).cx(0,2).x(1), (2,0))
P, names = b.marginal_family(3,(2,0))
p, ws = c.branches(register,P,names)
torch.testing.assert_close(p,native,rtol=0,atol=b.ATOL)
for label, index in [('00',2),('11',7)]:
    w = ws[names.index(label)]
    reference = torch.zeros(8,dtype=b.D); reference[index] = 1
    torch.testing.assert_close(w,reference,rtol=0,atol=b.ATOL)
assert ws[1] is None and ws[2] is None
print('Ordered labels:',names,'; probabilities:',*(f'{x:.6f}' for x in p))
print('Selected 00 -> full-register index 2; selected 11 -> index 7; impossible 01/10 -> None.')
```
```text
Ordered labels: ('00', '01', '10', '11') ; probabilities: 0.848353 0.000000 0.000000 0.151647
Selected 00 -> full-register index 2; selected 11 -> index 7; impossible 01/10 -> None.
```

<span id="formula-code-6-2-repeat"></span>

### 3. Prove repeatability under the ideal update

**Formula.** Repeat the same ideal projective measurement immediately, without intervening evolution or additional disturbance. For a possible first a,

$$
P_b|\psi_a\rangle
=\frac{P_bP_a|\psi\rangle}{\sqrt{p_a}}
=\delta_{ba}|\psi_a\rangle,\qquad
p(b\mid a)=\delta_{ba}.
$$

**Derivation.** Orthogonality gives zero for distinct subspaces; idempotence preserves the selected normalized vector. Squared lengths are therefore zero or one. The proof also holds for rank-two and larger projectors: the state need not be one particular computational basis vector inside the selected subspace. It uses the ideal update, rather than just the initial probability distribution.

An impossible first a has no conditional distribution. Its joint-table row is zero, rather than an invented normalized state. Consequently the joint table for two identical ideal measurements is $\operatorname{diag}(p)$.

```python
repeat = c.joint(register,P,names,P,names)
torch.testing.assert_close(repeat,torch.diag(p),rtol=0,atol=b.ATOL)
for label in ('00','11'):
    _, w = c.conditional_at(register,P,names,label)
    expected = torch.zeros(4,dtype=torch.float64); expected[names.index(label)] = 1
    torch.testing.assert_close(b.born(w,P,names),expected,rtol=0,atol=b.ATOL)
print('Same-family joint table is diagonal; every possible selected outcome repeats with probability 1.')
```
```text
Same-family joint table is diagonal; every possible selected outcome repeats with probability 1.
```

<span id="formula-code-6-2-joint"></span>

### 4. Derive the ordered joint distribution

Let $\{Q_c\}$ be a second complete orthogonal family on the **same global space**, measured after $\{P_a\}$ without intervening evolution.

**Formula.** For $p_a>0$, $q(c\mid a)=\|Q_c\psi_a\|^2$, so

$$
p(a,c)=p_aq(c\mid a)=\|Q_cP_a\psi\|^2,\qquad
\sum_c p(a,c)=p_a.
$$

**Derivation.** Substitute the normalized branch into the second Born rule and multiply by $p_a$, cancelling its denominator. This uses the ordinary conditional-probability product rule and the declared quantum update. If $p_a=0$, then $P_a\psi=0$ and the unnormalized expression gives the same zero row without division. Completeness gives
$\sum_c\langle P_a\psi|Q_c|P_a\psi\rangle=\|P_a\psi\|^2=p_a$; hence the whole table sums to one. This completes the proof for all finite families and normalized pure global inputs in scope.

**Order matters.** The rightmost projector acts first: $Q_cP_a$, not $P_aQ_c$. For $|+\rangle=(|0\rangle+|1\rangle)/\sqrt2$, Z followed by the plus-test gives four joint entries 1/4. Here plus-test means the two explicit projectors $Q_+=|+\rangle\langle+|$, $Q_-=I-Q_+$, rather than a native measurement API. Reverse the order: plus is certain first, and Z then has probabilities 1/2,1/2. Rows and columns follow the first and second declared label tuples.

```python
plus, _ = query(fq.Circuit(1,dtype=b.D).h(0))
Q, qn = c.plus_family(1)
forward = c.joint(plus,Z,zn,Q,qn)
direct = torch.tensor([[torch.vdot(q@z@plus,q@z@plus).real.item() for q in Q] for z in Z],dtype=torch.float64)
torch.testing.assert_close(forward,direct,rtol=0,atol=b.ATOL)
reverse = c.joint(plus,Q,qn,Z,zn)
torch.testing.assert_close(forward,torch.full((2,2),.25,dtype=torch.float64),rtol=0,atol=b.ATOL)
torch.testing.assert_close(reverse,torch.tensor([[.5,.5],[0,0]],dtype=torch.float64),rtol=0,atol=b.ATOL)
print('Z then plus-test:',[[round(x,6) for x in row] for row in forward.tolist()])
print('Plus-test then Z:',[[round(x,6) for x in row] for row in reverse.tolist()])
```
```text
Z then plus-test: [[0.25, 0.25], [0.25, 0.25]]
Plus-test then Z: [[0.5, 0.5], [0.0, 0.0]]
```

If a known unitary U occurs between measurements, substituting $U\psi_a$ instead gives $p(a,c)=\|Q_cUP_a\psi\|^2$. The joint helper intentionally covers only the no-intervening-evolution contract. Changing chronology requires changing the expression.

<span id="formula-code-6-2-ignored"></span>

### 5. Ignore a record by summing probabilities

**Formula.** If the first measurement is performed but its outcome is unavailable, the later marginal is

$$
q_{\mathrm{ignored}}(c)
=\sum_a p(a,c)
=\sum_a p_aq(c\mid a)
=\sum_a\|Q_cP_a\psi\|^2.
$$

**Derivation.** Each run belongs to one mutually exclusive recorded alternative a. The classical law of total probability sums their joint probabilities. It does not supply a new unconditioned statevector. Nor is the marginal generally the no-measurement probability $\|Q_c\psi\|^2$. Expanding $\psi=\sum_aP_a\psi$ shows that the latter contains additional interference terms $\langle Q_cP_b\psi|Q_cP_a\psi\rangle$ for $a\ne b$, which need not vanish after applying the later projector.

For the preceding $|+\rangle$ example, forgetting the Z result gives later plus probability 1/2; skipping Z gives 1. The proposed vector average $\frac12|0\rangle+\frac12|1\rangle$ has norm squared 1/2. Renormalizing it creates $|+\rangle$ and incorrectly predicts 1. Neither the unnormalized nor the normalized vector average describes this ignored-record experiment.

```python
ignored = forward.sum(0)
p0, branches0 = c.branches(plus,Z,zn)
weighted = sum(weight*b.born(w,Q,qn) for weight,w in zip(p0,branches0))
torch.testing.assert_close(ignored,weighted,rtol=0,atol=b.ATOL)
bad = sum(weight*w for weight,w in zip(p0,branches0))
norm2 = torch.vdot(bad,bad).real.item()
bad = bad/torch.linalg.vector_norm(bad)
wrong = b.born(bad,Q,qn)[0].item()
assert abs(norm2-.5)<b.ATOL and abs(wrong-1)<b.ATOL
torch.testing.assert_close(ignored,torch.tensor([.5,.5],dtype=torch.float64),rtol=0,atol=b.ATOL)
print(f'Ignored Z record: plus probability {ignored[0]:.6f}; normalized vector-average prediction {wrong:.6f}.')
print(f'Before the extra normalization, the averaged vector had norm squared {norm2:.6f}.')
```
```text
Ignored Z record: plus probability 0.500000; normalized vector-average prediction 1.000000.
Before the extra normalization, the averaged vector had norm squared 0.500000.
```

Probabilities can weight a classical sum of **probabilities**. They are not amplitudes of a coherent superposition of mutually exclusive recorded alternatives. Chapter 8 will derive an operator representation of the ignored-outcome state; a vector average would introduce the wrong physics.

<span id="formula-code-6-2-coarse"></span>

### 6. Distinguish coarse projection from forgetting a fine record

A measurement may detect only parity, or distinguish every computational string and later erase its record. Initial parity probabilities agree, but their disturbances need not.

**Formula.** Group mutually orthogonal fine projectors $P_j$ into event A, with $R_A=\sum_{j\in A}P_j$. A coarse ideal measurement followed by test $Q_c$ gives

$$
p_{\mathrm{coarse}}(A,c)
=\left\|Q_c\sum_{j\in A}P_j\psi\right\|^2.
$$

A fine measurement followed by forgetting j except for A gives

$$
p_{\mathrm{fine}}(A,c)=\sum_{j\in A}\|Q_cP_j\psi\|^2.
$$

**Derivation.** Apply the proved joint formula to $R_A$ in the first procedure. In the second, apply it to each $P_j$ and sum the exclusive fine records. The difference consists of cross terms for distinct j within A. A coarse ideal projection preserves coherence inside its subspace; a fine measurement, even with a subsequently unavailable record, requires the probability sum. A reported coarse label alone therefore does not identify the physical procedure.

For $|\Phi_\phi\rangle=(|00\rangle+e^{i\phi}|11\rangle)/\sqrt2$, the even projector preserves the vector. The XX-plus test from 6.1 then has probability $(1+\cos\phi)/2$. Fine computational measurement with the string forgotten instead gives 1/2. This is compatible with 6.1's addition rule for coarse **initial outcome probabilities**.

```python
phi = .6
bell, _ = query(fq.Circuit(2,dtype=b.D).h(0).cx(0,1).p(0,phi))
coarse, cn = b.parity_family(2)
fine, fn = b.basis_family(2)
XX, xn = b.xx_family()
coarse_later = c.joint(bell,coarse,cn,XX,xn).sum(0)
fine_later = c.joint(bell,fine,fn,XX,xn).sum(0)
torch.testing.assert_close(coarse_later,b.born(bell,XX,xn),rtol=0,atol=b.ATOL)
assert abs(coarse_later[0].item()-(1+math.cos(phi))/2)<b.ATOL
torch.testing.assert_close(fine_later,torch.tensor([.5,.5],dtype=torch.float64),rtol=0,atol=b.ATOL)
print(f'XX-plus: parity-only measurement {coarse_later[0]:.6f}; fine measurement, forgotten record {fine_later[0]:.6f}.')
```
```text
XX-plus: parity-only measurement 0.912668; fine measurement, forgotten record 0.500000.
```

<span id="formula-code-6-2-correlated"></span>

### 7. Condition correlations without assuming independent subsystem states

**Formula.** For an arbitrary bipartite pure vector
$|\psi\rangle=\sum_{i,j}\alpha_{ij}|i\rangle_A|j\rangle_B$, computational measurement of A gives

$$
p(a)=\sum_j|\alpha_{aj}|^2,\qquad
|\psi_a\rangle
=|a\rangle_A\otimes
\frac{\sum_j\alpha_{aj}|j\rangle_B}{\sqrt{p(a)}}.
$$

Keeping precisely the terms with i=a proves the factorization for this rank-one local measurement. It does not assign independent pure states to arbitrary subsystems before measuring.

**Ignored local outcomes.** More generally, let $\{R_a\}$ be a complete projective family on A and $S_c$ a projector on B. The global projectors $P_a=R_a\otimes I$ and $Q_c=I\otimes S_c$ commute, since each acts as identity on the other's factor. Thus

$$
\sum_a\|Q_cP_a\psi\|^2
=\sum_a\langle\psi|P_aQ_cP_a|\psi\rangle
=\langle\psi|Q_c\sum_aP_a|\psi\rangle
=\langle\psi|Q_c|\psi\rangle.
$$

The first equality uses $Q_c^\dagger Q_c=Q_c$; the second uses commutation and $P_a^2=P_a$. An ignored ideal local measurement on A therefore preserves B's local outcome distribution. It need not preserve their joint state, correlations or a later joint interference test. Selecting an outcome can change B's conditional distribution, but learning the selection requires its classical record.

**Update boundary.** The initial probabilities do not force the ideal update: measure Z and deliberately apply X afterward. The first probabilities agree, but an immediate later Z result flips rather than repeats. We calculate this alternative as $X\psi_a$, not as the ideal branch. The Bell check also retains the selected branch's scalar $e^{i\phi}$ without phase alignment.

```python
A, an = b.marginal_family(2,(0,))
B, bn = b.marginal_family(2,(1,))
correlated = c.joint(bell,A,an,B,bn)
torch.testing.assert_close(correlated,torch.diag(torch.tensor([.5,.5],dtype=torch.float64)),rtol=0,atol=b.ATOL)
torch.testing.assert_close(correlated.sum(0),b.born(bell,B,bn),rtol=0,atol=b.ATOL)
p_a, global_branch = c.conditional_at(bell,A,an,'1')
expected = torch.zeros(4,dtype=b.D); expected[3] = complex(math.cos(phi),math.sin(phi))
torch.testing.assert_close(global_branch,expected,rtol=0,atol=b.ATOL)
# A deliberately different operation: ideal Z measurement followed by X.
X = torch.tensor([[0,1],[1,0]],dtype=b.D)
old_p, old_ws = c.branches(qubit,Z,zn)
later_z = sum(weight*b.born(X@w,Z,zn) for weight,w in zip(old_p,old_ws))
torch.testing.assert_close(later_z,old_p.flip(0),rtol=0,atol=b.ATOL)
print('Bell q0/q1 joint outcomes: 00 and 11 each 0.5; ignoring q0 retains q1 probabilities 0.5, 0.5.')
print('Same initial Z probabilities, different update (Z then X): later Z probabilities',*(f'{x:.6f}' for x in later_z))
```
```text
Bell q0/q1 joint outcomes: 00 and 11 each 0.5; ignoring q0 retains q1 probabilities 0.5, 0.5.
Same initial Z probabilities, different update (Z then X): later Z probabilities 0.640000 0.360000
```

<span id="formula-code-6-2-contracts"></span>

### 8. Separate impossible events, rare events and numeric failure

**Mathematical contract.** A conditional state requires $p_a>0$, not $p_a>10^{-12}$. Our comparison tolerance is not a physical probability threshold. For
$|\psi\rangle=\sqrt{1-\epsilon^2}|0\rangle+i\epsilon|1\rangle$ and $\epsilon=10^{-10}$, outcome 1 has probability $10^{-20}$ and conditional state $i|1\rangle$. Dropping it would change the model.

**Numerical boundary.** Division by $\sqrt{p_a}$ can amplify errors in a small projected component. If the computed projection is nonzero but its squared norm underflows to zero in float64, the helper raises FloatingPointError rather than calling it impossible or fabricating a state. The representable amplitude $\epsilon=10^{-200}$ triggers this boundary. No interval certificate or general relative-accuracy guarantee for rare events is claimed. A computed exactly zero projection is instead retained as None.

Inputs must satisfy the complete Hermitian orthogonal projector and normalized CPU complex128 vector contracts of 6.1. Batched vectors, malformed families, duplicate labels and unknown selected labels are rejected. The four-qubit dimension guard belongs to this dense teaching reference, rather than to FlagQuantum.

```python
assert c.invalid_checks() == 10
rare = torch.tensor([math.sqrt(1-1e-20),1e-10j],dtype=b.D)
rare_p, rare_w = c.conditional_at(rare,Z,zn,'1')
assert 0 < rare_p.item() < b.ATOL
torch.testing.assert_close(rare_w,torch.tensor([0,1j],dtype=b.D),rtol=0,atol=b.ATOL)
assert calls == 4
print('10 invalid contracts rejected; positive 1e-20 event retained; squared-norm underflow rejected explicitly.')
print('4 actual native body preparations; subsequent branches are explicit classical predictions, not native sampled collapse.')
```
```text
10 invalid contracts rejected; positive 1e-20 event retained; squared-norm underflow rejected explicitly.
4 actual native body preparations; subsequent branches are explicit classical predictions, not native sampled collapse.
```

### Complete program and expected output

Run the [complete program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/conditional_states.py) with the repository-root command:

    python examples/foundations/conditional_states.py

It executes 46 native preparation circuits: 17 basis/complex inputs, 18 ordered correlated-register cases, four Bell cases, four one-qubit interference cases and three coarse/fine comparisons. Scalar masks, an independently indexed gate reference, closed formulas and unnormalized ordered projector products provide independent implementation checks. Finite tests do not replace the proofs.

Run the scoped body checker with:

    python scripts/check_conditional_states_prose.py

It executes the eight cumulative snippets with four native preparations and compares actual outputs, then checks the complete program. Subsequent branch/joint predictions are classical postprocessing, rather than native sampled collapse.

Expected output of the complete program:

```text
17 basis/complex circuits: scalar-mask conditional states, zero branches and repeatability passed.
18 ordered-support circuits: all six two-qubit selections on a correlated three-qubit register passed.
4 Bell circuits: conditional correlations, ignored local outcomes and lost phase-sensitive interference passed.
4 single-qubit circuits: joint tables normalize, while normalized averaged statevectors give a wrong later probability.
3 coarse/fine circuits: parity-only projection preserves within-event coherence; forgetting a fine record does not.
10 invalid contracts rejected; positive 1e-20 branch retained; squared-norm underflow explicitly rejected.
46 actual CPU complex128 preparation circuits; conditional branches and later probabilities are classical postprocessing, not native collapse or shots.
Implementation atol 1e-12, rtol 0; no vector averaging, phase alignment or input normalization repair; density-operator update deferred to Chapter 8.
```

### Understanding checks and transfer exercises

**6.2-A — New register.** On a four-qubit product input, apply Ry(q0,−.29),CX(q0,q3),P(q1,.47), measure (q3,q1), then measure the reversed selection (q1,q3). Check the conditional coordinate masks and joint-table support on basis and complex inputs.

**6.2-B — Complex subspaces.** For Fourier columns $B_{jk}=e^{2\pi i jk/4}/2$, group columns 0,1 versus 2,3. Form each projected vector from column overlaps, check its normalization and repeatability, then compute later computational probabilities with the first label ignored. Must a selected probability exceed the implementation tolerance?

**6.2-C — Record or amplitude?** Starting with $|+\rangle$, compare a later plus-test after (i) no first measurement, (ii) Z=0 selected and (iii) Z measured with its record unavailable. Why does renormalizing a vector average fail in (iii)?

**6.2-D — Which update?** An apparatus reports a computational outcome, then prepares the opposite computational state. Can its first probabilities agree with Born's rule? Does the repeatability proof apply? Why is a parity label also insufficient to choose the disturbance in unit 6?

<details markdown="1">
<summary>Answers and reasoning for 6.2</summary>

**A.** For first label $(u,v)$, retain coordinates with $b_3=u,b_1=v$ and divide by the square root of their total squared magnitude, only when it is positive. The global vector still has sixteen entries. The second selection maps $(u,v)$ deterministically to $(v,u)$, so each possible row has exactly one nonzero joint entry equal to its initial probability. Impossible rows are zero and have no conditional vectors. The separate author transfer checks all sixteen basis inputs and a complex product.

**B.** Fourier-column orthogonality follows from the finite geometric sum in 6.1. For A={0,1} or {2,3}, let $w_A=\sum_{k\in A}|b_k\rangle\langle b_k|\psi\rangle$ and $p_A=\sum_{k\in A}|\langle b_k|\psi\rangle|^2$. Normalize only for $p_A>0$. Orthogonality makes the selected label repeat; later ignored-record computational probability at index j is $\sum_A|(w_A)_j|^2$, not the squared sum over A. Retain a representable positive rare event below the comparison tolerance; report squared-norm underflow separately. Three new prepared states are checked in the author transfer, which is not a reader trial.

**C.** The plus probabilities are 1, 1/2 and 1/2. Selecting Z=0 gives $|0\rangle$; ignoring Z sums the conditional probability predictions for |0⟩ and |1⟩. Their probability-weighted vector average has norm squared 1/2 and becomes $|+\rangle$ on normalization, incorrectly predicting 1.

**D.** Its first probabilities can agree exactly. The additional X changes the conditional output, violating the ideal update assumption; repeatability no longer follows. Similarly, an ideal parity projection retains within-subspace superpositions, while a finer computational measurement with a forgotten record loses that coherence. The coarse initial distribution alone cannot identify the disturbance.

</details>

### Sources, depth and next step

The frozen target is Nielsen and Chuang, 10th Anniversary Edition (2010), §2.2.3, beginning at printed page 84. Its assigned locator is retained; no fresh inspection of the user-local PDF is claimed. The public author source [Preskill, Caltech Chapter 3, §3.1.1](https://www.preskill.caltech.edu/ph219/chap3_15.pdf), equation (3.16), PDF page 8, was checked for the normalized projective branch. The currently served header is October 2018. We use branch/probability reasoning here and defer the density-operator discussion that follows to Chapter 8.

The proofs are complete within the stated finite pure-global ideal-projective scope, with the physical update assumed. The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/6.2.json) separates author execution from independent mathematical/implementation review and reader trials, which remain pending. Continue, when drafted, with [6.3 Observables, spectra, and expectations](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-3).
