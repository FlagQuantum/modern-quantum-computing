# 6. Measurement, Expectation Values, and Statistical Estimation

**Working drafts: sections 6.1–6.9 · Writing Baseline 1.0 · October 22, 2026.** Author execution is separate from independent mathematical, implementation and reader review, which remain pending. Examples use released FlagQuantum 0.3.1 and PyTorch 2.13.0 on CPU with complex128 statevectors. The earlier measurement page remains a format pilot, rather than a substitute for this chapter.

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

The proofs are complete within the stated finite pure-global ideal-projective scope, with the physical update assumed. The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/6.2.json) separates author execution from independent mathematical/implementation review and reader trials, which remain pending. Continue with [6.3 Observables, spectra, and expectations](#sec-measurement-expectation-values-and-statistical-estimation-3).

<span id="sec-measurement-expectation-values-and-statistical-estimation-3"></span>

## 6.3 Observables, spectra, and expectations

A measurement can return a label such as “even.” A physical quantity also assigns a numerical value to that alternative. The **expectation** is the probability-weighted mean of those values; it need not itself be a possible individual outcome. This section connects that definition to a Hermitian matrix and then to FlagQuantum's native expectation requests.

Prerequisites are [6.1](#sec-measurement-expectation-values-and-statistical-estimation-1), for projective Born probabilities, and [2.5](ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-5), for the finite-dimensional Hermitian spectral theorem. Conditional-state updates from 6.2 are not needed for the identity proved here. Depth **F** means a complete proof under the stated assumptions: a normalized pure state, a finite Hermitian observable and its projective spectral measurement.

Examples use released FlagQuantum 0.3.1/PyTorch 2.13.0, CPU complex128, absolute implementation tolerance $10^{-12}$ and relative tolerance zero. Native results are exact model expectations, rather than individual shots or hardware data. Numerical eigendecomposition is a classical reference; it is not an implemented physical measurement protocol or an interval certificate.

<span id="formula-code-6-3-outcomes"></span>

### 1. Associate outcome labels with real values

**Formula.** Let $\{P_a\}$ be a complete orthogonal projector family, with real outcome values $\lambda_a$. The observable and its expected value are

$$
A=\sum_a\lambda_aP_a,\qquad
\mathbb E_\psi[A]=\sum_a\lambda_a p_a,\qquad
p_a=\langle\psi|P_a|\psi\rangle.
$$

When the $\lambda_a$ are distinct, the $P_a$ are the spectral projectors for those distinct eigenvalues. A rank-one refinement may have repeated values; equal-value probabilities can instead be grouped.

**First derivation.** Computational measurement of a qubit with values +1 for label 0 and −1 for label 1 measures $Z=P_0-P_1$. Hence $\langle Z\rangle=p_0-p_1$, not $p_1$, not $p_0+p_1$, and not an amplitude difference. For Ry(θ)|0⟩ this gives $\cos^2(\theta/2)-\sin^2(\theta/2)=\cos\theta$. Individual Z outcomes remain ±1 even when this mean lies between them.

**Native FlagQuantum code → result.** Run the snippets cumulatively from the repository root. Named requests are read with result.expectation(name); each raw expectation has shape (1,), whose leading axis is the execution batch, rather than a qubit or outcome axis.

```python
import math
import torch
import flagquantum as fq
import examples.foundations.observables as o
b = o.b
calls = 0
def query(circuit, observables):
    global calls
    requests = [fq.probabilities()]+[fq.expectation(A,name=name) for name,A in observables.items()]
    result = fq.run(circuit,outputs=requests,options=b.OPTIONS)
    v, p = result.statevector(), result.probabilities
    assert v.shape == (1,2**circuit.n_qubits) and p.shape == v.shape
    assert v.dtype == b.D and p.dtype == torch.float64
    values = {}
    for name in observables:
        raw = result.expectation(name)
        assert raw.shape == (1,) and raw.dtype == torch.float64
        values[name] = raw[0]
    calls += 1
    return v[0], p[0], values
theta = .8
v, p, native = query(fq.Circuit(1,dtype=b.D).ry(0,theta),{'z':fq.Z(0)})
mean = p[0]-p[1]
torch.testing.assert_close(mean,native['z'],rtol=0,atol=b.ATOL)
assert abs(mean.item()-math.cos(theta)) < b.ATOL
print(f'Z outcome weights: +1, -1; probabilities {p[0]:.6f}, {p[1]:.6f}; expectation {mean:.6f}.')
```
```text
Z outcome weights: +1, -1; probabilities 0.848353, 0.151647; expectation 0.696707.
```

<span id="formula-code-6-3-quadratic"></span>

### 2. Prove the spectral expectation identity and reality

**Formula.** Substituting the Born probabilities gives

$$
\mathbb E_\psi[A]
=\sum_a\lambda_a\langle\psi|P_a|\psi\rangle
=\left\langle\psi\middle|\sum_a\lambda_aP_a\middle|\psi\right\rangle
=\langle\psi|A|\psi\rangle.
$$

**Complete proof.** The first equality is the definition of a mean for a finite outcome distribution. The second uses distributivity and linearity in the middle operator; the third is the assumed spectral expansion from 2.5. Conversely every finite Hermitian A has that expansion, with real eigenvalues and complete orthogonal spectral projectors, so the identity applies to its projective measurement. Its value is real because the weighted probabilities and weights are real. Equivalently,
$\overline{\langle\psi|A|\psi\rangle}=\langle\psi|A^\dagger|\psi\rangle=\langle\psi|A|\psi\rangle$.
No conditional update or ensemble density matrix was used.

**Complex coordinates.** For $\psi=(\alpha,\beta)^T$,

$$
\langle X\rangle=2\operatorname{Re}(\overline\alpha\beta),\quad
\langle Y\rangle=2\operatorname{Im}(\overline\alpha\beta),\quad
\langle Z\rangle=|\alpha|^2-|\beta|^2,
$$

The matrices used here are

$$
X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix},\quad
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix}.
$$

Multiplying Y by the vector gives $-i\overline\alpha\beta+i\overline\beta\alpha=2\operatorname{Im}(\overline\alpha\beta)$, proving the displayed positive sign. For Ry(θ) followed by P(φ), $\alpha=\cos(\theta/2)$ and $\beta=e^{i\phi}\sin(\theta/2)$. Thus X, Y and Z means are respectively $\sin\theta\cos\phi,\sin\theta\sin\phi,\cos\theta$. Swapping complex-conjugation order would reverse the Y sign.

```python
theta, phi = .9, .63
nativeH = .7*fq.X(0)-.2*fq.Y(0)+1.3*fq.Z(0)
qubit, _, m = query(fq.Circuit(1,dtype=b.D).ry(0,theta).p(0,phi),
                    {'x':fq.X(0),'y':fq.Y(0),'z':fq.Z(0),'h':nativeH})
for name,A,formula in [('x',o.X,math.sin(theta)*math.cos(phi)),
                       ('y',o.Y,math.sin(theta)*math.sin(phi)),
                       ('z',o.Z,math.cos(theta))]:
    quadratic = torch.vdot(qubit,A@qubit)
    assert abs(quadratic.imag.item()) < b.ATOL
    assert abs(quadratic.real.item()-formula) < b.ATOL
    torch.testing.assert_close(m[name],quadratic.real,rtol=0,atol=b.ATOL)
print('X/Y/Z means:',*(f'{m[name]:.6f}' for name in ('x','y','z')))
```
```text
X/Y/Z means: 0.632950 0.461493 0.621610
```

<span id="formula-code-6-3-spectrum"></span>

### 3. Translate a non-diagonal observable without treating its mean as an outcome

Take the dimensionless example $H=.7X-.2Y+1.3Z$. The symbol H here names this illustrative observable, rather than a physical device calibration.

**Formula and derivation.** Direct multiplication of the displayed matrices gives $X^2=Y^2=Z^2=I$, $XY=-YX=iZ$, $YZ=-ZY=iX$ and $ZX=-XZ=iY$. Expanding H squared produces the three squared terms and cross terms proportional to $XY+YX$, $XZ+ZX$ and $YZ+ZY$; each cross term is zero by those identities. Consequently
$H^2=(.7^2+.2^2+1.3^2)I=r^2I$, where $r=\sqrt{2.22}>0$. Its two spectral projectors are

$$
P_-=\frac{I-H/r}{2},\qquad P_+=\frac{I+H/r}{2},\qquad
\lambda_-=-r,\quad\lambda_+=r.
$$

They are Hermitian because H is. Squaring $(I\pm H/r)/2$ and using $H^2/r^2=I$ proves idempotence. Their product is zero and their sum is I. Also $HP_\pm=\pm rP_\pm$, and $rP_+-rP_-=H$. This explicitly proves the claimed spectral family, rather than trusting a numerical eigensolver.

The prediction is $\langle H\rangle=-rp_-+rp_+$. The code compares these probabilities and weights with both a dense quadratic form and the actual native Pauli-sum request. An arbitrary dense Hermitian matrix is evaluated classically here; no native general-matrix expectation API is claimed.

```python
r = math.sqrt(.7**2+.2**2+1.3**2)
P = ((o.I-o.H/r)/2,(o.I+o.H/r)/2)
eigenvalues = (-r,r)
spectral, probabilities = o.spectral_mean(qubit,eigenvalues,P,('minus','plus'))
explicit = sum(value*prob for value,prob in zip(eigenvalues,probabilities))
quadratic = torch.vdot(qubit,o.H@qubit).real
torch.testing.assert_close(spectral,explicit,rtol=0,atol=b.ATOL)
torch.testing.assert_close(spectral,quadratic,rtol=0,atol=b.ATOL)
torch.testing.assert_close(spectral,m['h'],rtol=0,atol=b.ATOL)
print('H eigenvalues:',*(f'{x:.6f}' for x in eigenvalues))
print('Spectral probabilities:',*(f'{x:.6f}' for x in probabilities),'; expectation:',f'{spectral:.6f}')
```
```text
H eigenvalues: -1.489966 1.489966
Spectral probabilities: 0.111112 0.888888 ; expectation: 1.158859
```

<span id="formula-code-6-3-degenerate"></span>

### 4. Group degenerate eigenvalues and retain correlations

For two qubits, $Z_0Z_1=Z\otimes Z$ has eigenvalue +1 on |00⟩,|11⟩ and −1 on |01⟩,|10⟩.

**Formula.**

$$
P_{\mathrm{even}}=|00\rangle\langle00|+|11\rangle\langle11|,\qquad
P_{\mathrm{odd}}=I-P_{\mathrm{even}},\qquad
\langle Z_0Z_1\rangle=p_{\mathrm{even}}-p_{\mathrm{odd}}.
$$

**Derivation.** Apply Z to each computational factor: each 1 contributes a minus sign, so the product is $(-1)^{b_0+b_1}$. Grouping equal signs gives the rank-two projectors and the expectation formula. It also yields the scalar check $\sum_j(-1)^{\operatorname{popcount}(j)}p_j$ using the full register index convention.

A basis inside either eigenspace is not unique. If its orthonormal basis columns are B and another basis is BR for a unitary R, then $(BR)(BR)^\dagger=BRR^\dagger B^\dagger=BB^\dagger$. The spectral projector, probability and mean are therefore invariant under that internal basis choice. Different rank-one refinements might imply different disturbances; that separate point from 6.2 does not change their equal-value mean.

For $|\Phi_\phi\rangle=(|00\rangle+e^{i\phi}|11\rangle)/\sqrt2$, local Z means vanish but $\langle Z_0Z_1\rangle=1$. A product's expectation is not generally a product of expectations. The XX and YY means are $\cos\phi$ and $-\cos\phi$, preserving relative-phase information.

```python
bell, pbell, bm = query(fq.Circuit(2,dtype=b.D).h(0).cx(0,1).p(0,.6),
                         {'z0':fq.Z(0),'z1':fq.Z(1),'zz':fq.Z(0)@fq.Z(1),
                          'xx':fq.X(0)@fq.X(1),'yy':fq.Y(0)@fq.Y(1)})
parity, labels = b.parity_family(2)
zz, probabilities = o.spectral_mean(bell,(1,-1),parity,labels)
scalar = sum((-1)**j.bit_count()*pbell[j] for j in range(4))
torch.testing.assert_close(zz,scalar,rtol=0,atol=b.ATOL)
torch.testing.assert_close(zz,bm['zz'],rtol=0,atol=b.ATOL)
# Rotate an orthonormal basis within the even eigenspace; its projector is unchanged.
u = torch.tensor([1,0,0,1j],dtype=b.D)/math.sqrt(2)
w = torch.tensor([1,0,0,-1j],dtype=b.D)/math.sqrt(2)
rotated = torch.outer(u,u.conj())+torch.outer(w,w.conj())
torch.testing.assert_close(rotated,parity[0],rtol=0,atol=b.ATOL)
assert abs(bm['zz'].item()-bm['z0'].item()*bm['z1'].item()-1)<b.ATOL
print(f'ZZ mean {zz:.6f}; product of local Z means {bm["z0"]*bm["z1"]:.6f}; even probability {probabilities[0]:.6f}.')
print(f'XX {bm["xx"]:.6f}; YY {bm["yy"]:.6f}; internal eigenbasis rotation preserves the even projector.')
```
```text
ZZ mean 1.000000; product of local Z means 0.000000; even probability 1.000000.
XX 0.825336; YY -0.825336; internal eigenbasis rotation preserves the even projector.
```

<span id="formula-code-6-3-support"></span>

### 5. Translate qubit support separately from matrix tensor order

**Formula.** In the established q0-leftmost three-qubit basis, the observable

$$
A_3=.6X_0Y_2-.4Z_1
=.6(X\otimes I\otimes Y)-.4(I\otimes Z\otimes I)
$$

has expectation $\psi^\dagger A_3\psi$. The omitted qubit in each term contributes an identity, rather than being deleted from the register.

**Derivation.** Acting on each tensor-basis state applies the named local matrix to its declared factor. Extending by linearity gives the displayed full-register matrix and its quadratic form. Operators on disjoint qubits commute as tensor factors, so naming Y(q2) first does not make it the leftmost dense tensor factor. Dense order is determined by the register convention.

**API contract.** For native Observable objects, @ constructs products on **disjoint** qubits, + and − form real sums, and * multiplies by a real scalar. Observable @ Observable is not unrestricted same-qubit matrix multiplication; observable * observable is unsupported. These conventions were checked in the released API before execution. The code uses reversed, nonadjacent native support and compares with an independently indexed preparation and the explicit dense spectral reference.

```python
factors = b.complex_factors(3)
circuit = fq.Circuit(3,dtype=b.D)
for q,factor in enumerate(factors):
    circuit.unitary(q,unitary=b.prepare_matrix(torch.tensor(factor,dtype=b.D)))
circuit.ry(1,.27).cx(2,0).p(2,-.52)
nativeA = .6*(fq.Y(2)@fq.X(0))-.4*fq.Z(1)
register, _, values = query(circuit,{'a':nativeA})
A = .6*torch.kron(torch.kron(o.X,o.I),o.Y)-.4*torch.kron(torch.kron(o.I,o.Z),o.I)
weights, projectors, names = o.numerical_spectrum(A)
spectral3, _ = o.spectral_mean(register,weights,projectors,names)
torch.testing.assert_close(spectral3,values['a'],rtol=0,atol=b.ATOL)
torch.testing.assert_close(spectral3,o.dense_mean(register,A),rtol=0,atol=b.ATOL)
print(f'Nonadjacent Y(q2) @ X(q0), with local Z(q1) term: expectation {spectral3:.6f}.')
```
```text
Nonadjacent Y(q2) @ X(q0), with local Z(q1) term: expectation 0.441497.
```

<span id="formula-code-6-3-linearity"></span>

### 6. Prove linearity without inventing simultaneous outcomes

**Formula.** For Hermitian A,B and real scalars s,t,

$$
\langle sA+tB\rangle
=\psi^\dagger(sA+tB)\psi
=s\langle A\rangle+t\langle B\rangle.
$$

**Derivation and boundary.** Distribute the middle matrix and scalar multiplication in the inner product. Real coefficients keep the sum Hermitian. This proof requires no commutation between A and B. It therefore establishes equality of expectations, not the existence of a joint measurement assigning both values simultaneously to each system.

For X+Z, $(X+Z)^2=2I$ and trace zero gives eigenvalues ±√2. These are not the candidate sums −2,0,+2 of two hypothetical simultaneous Pauli outcomes. Separately estimating term means is a possible experimental strategy, but its shot allocation, covariance and uncertainty need additional analysis in later sections. A native exact simulator request does not supply that experimental analysis.

```python
state, _, lm = query(fq.Circuit(1,dtype=b.D).ry(0,.31),
                       {'x':fq.X(0),'z':fq.Z(0),'sum':fq.X(0)+fq.Z(0)})
torch.testing.assert_close(lm['sum'],lm['x']+lm['z'],rtol=0,atol=b.ATOL)
torch.testing.assert_close(lm['sum'],o.dense_mean(state,o.X+o.Z),rtol=0,atol=b.ATOL)
spectrum = torch.linalg.eigvalsh(o.X+o.Z)
torch.testing.assert_close(spectrum,torch.tensor([-math.sqrt(2),math.sqrt(2)],dtype=torch.float64),rtol=0,atol=b.ATOL)
print(f'Linearity: mean(X+Z) = mean(X)+mean(Z) = {lm["sum"]:.6f}.')
print('Spectrum of X+Z: -sqrt(2), +sqrt(2); not the set -2, 0, +2 from adding hypothetical simultaneous Pauli outcomes.')
```
```text
Linearity: mean(X+Z) = mean(X)+mean(Z) = 1.257392.
Spectrum of X+Z: -sqrt(2), +sqrt(2); not the set -2, 0, +2 from adding hypothetical simultaneous Pauli outcomes.
```

<span id="formula-code-6-3-range"></span>

### 7. Preserve units and bound the mean using the spectrum

**Formula.** Since $p_a\ge0$ and $\sum_ap_a=1$,

$$
\lambda_{\min}\le\sum_a\lambda_ap_a\le\lambda_{\max}.
$$

**Derivation.** Multiply each inequality $\lambda_{\min}\le\lambda_a\le\lambda_{\max}$ by nonnegative $p_a$ and sum. This proves a convex spectral bound for a normalized input. It does not make every mean a spectral outcome. For an affine recalibration $A'=sA+tI$, the same projectors give weights $\lambda'_a=s\lambda_a+t$ and $\langle A'\rangle=s\langle A\rangle+t$. Negative s reverses spectral order but does not invalidate the identity.

A physical unit belongs consistently to both the matrix and its eigenvalue weights; probabilities are dimensionless. For illustration only, interpret the preceding H entries in meV, shift all energies by +0.25 meV and convert to eV with $1\,\mathrm{meV}=10^{-3}\,\mathrm{eV}$. The code verifies the identical probability weights and converted spectral mean. This is an explicitly declared example unit, not an inferred device Hamiltonian.

```python
# Treat H and its eigenvalues as an illustrative energy in meV; no physical calibration is implied.
shift_meV = .25
energy_eV = (spectral+shift_meV)*1e-3
weights_eV = tuple((value+shift_meV)*1e-3 for value in eigenvalues)
converted, same_prob = o.spectral_mean(qubit,weights_eV,P,('minus','plus'))
torch.testing.assert_close(converted,energy_eV,rtol=0,atol=b.ATOL)
torch.testing.assert_close(same_prob,b.born(qubit,P,('minus','plus')),rtol=0,atol=b.ATOL)
assert -r-b.ATOL <= spectral.item() <= r+b.ATOL
print(f'Original illustrative H mean {spectral:.6f} meV; after +0.25 meV and conversion: {energy_eV:.9f} eV.')
print('The eigenprojectors and their probabilities are unchanged; every outcome value uses the same declared energy conversion.')
```
```text
Original illustrative H mean 1.158859 meV; after +0.25 meV and conversion: 0.001408859 eV.
The eigenprojectors and their probabilities are unchanged; every outcome value uses the same declared energy conversion.
```

<span id="formula-code-6-3-contracts"></span>

### 8. Validate observables and numerical spectra before interpreting a result

**Contract.** The observable must be a finite Hermitian matrix on the same Hilbert space as the normalized state. The eigenvalue list must contain finite real values, one for each declared projector. The helper rejects complex weights, Boolean values masquerading as eigenvalues, malformed shapes and non-Hermitian matrices; it does not repair them by replacing A with $(A+A^\dagger)/2$ or normalizing an input.

The classical numerical reference uses torch.linalg.eigh after Hermiticity validation. It reconstructs A and verifies the resulting complete projector family. It uses rank-one column labels, **without** merging nearby eigenvalues by a tolerance or claiming a canonical eigenbasis at degeneracy. The spectral-mean identity is invariant under phase choices for the eigenvectors and unitary rotations inside an exactly degenerate eigenspace, as proved above. Floating residual tests do not certify exact degeneracy or an interval error bound. A tiny imaginary quadratic-form residual is checked explicitly before the real part is returned.

```python
assert o.invalid_checks() == 10
weights, projectors, labels = o.numerical_spectrum(o.H)
numerical, _ = o.spectral_mean(qubit,weights,projectors,labels)
torch.testing.assert_close(numerical,spectral,rtol=0,atol=b.ATOL)
assert calls == 5
print('10 invalid contracts rejected; analytic and numerical spectra agree; five actual native body circuits.')
print('Exact expectations are deterministic model values, not individual outcomes, finite-shot estimates or a hardware measurement recipe.')
```
```text
10 invalid contracts rejected; analytic and numerical spectra agree; five actual native body circuits.
Exact expectations are deterministic model values, not individual outcomes, finite-shot estimates or a hardware measurement recipe.
```

### Complete program and expected output

Run the [complete example](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/observables.py):

    python examples/foundations/observables.py

It executes 41 actual native statevector circuits: 15 single-qubit angle pairs, 17 two-qubit inputs/phases and nine three-qubit inputs. Checks compare native exact means, closed amplitudes, analytic projectors, scalar parity sums, dense quadratic forms and numerical spectral reconstruction. This is implementation evidence; the full proof does not depend on the tested sample size.

Run the body/output checker:

    python scripts/check_observables_prose.py

It executes all eight cumulative snippets, with five native circuit calls, then the complete program, checking their exact expected outputs.

Expected output of the complete program:

```text
15 single-qubit circuits: X/Y/Z signs, closed amplitudes and native/analytic-spectral/dense H expectations passed.
17 two-qubit circuits: degenerate ZZ projectors, parity signs, XX/YY correlations and native/numerical-spectral/dense sums passed.
9 three-qubit circuits: reversed nonadjacent Pauli supports, independently indexed states and dense spectral means passed.
10 malformed observable/state/eigenvalue contracts rejected; no Hermitian or state normalization repair.
41 actual CPU complex128 circuits; native exact expectations, not single-shot outcomes, a hardware measurement protocol or an interval certificate.
```

### Understanding checks and transfer exercises

**6.3-A — New complex coefficients.** Prepare a two-qubit complex product and apply Ry(q0,θ),CX(q0,q1),P(q1,−.39). For $A=.41Y_0X_1-.23X_0Z_1+.17Z_1$, compare the native Pauli-sum expectation with a numerical spectral sum and a dense quadratic form. Explain why no eigensolver phase alignment is required.

**6.3-B — Larger reversed support.** On four qubits, test $.31Y_3X_0-.27Z_2+.12X_1$ after Ry(q2,.33),CX(q3,q0),P(q0,−.46). Write the full tensor matrix in q0-leftmost order. Check all basis inputs and a complex product against an independently indexed preparation.

**6.3-C — Outcome or expectation?** Can Z measurement have an individual outcome 0 on a qubit in |+⟩? What is its mean? Why does $\langle X+Z\rangle=\langle X\rangle+\langle Z\rangle$ not imply a joint per-shot assignment of X and Z values?

**6.3-D — Units and an offset.** Change the illustrative H calibration to $H'=-2H+.5I$, all in meV. Give its eigenvalues and mean in eV. Do the probabilities change? What if a numerical solver returns different eigenvectors inside a degenerate subspace?

<details markdown="1">
<summary>Answers and reasoning for 6.3</summary>

**A.** Use $Y\otimes X$, $X\otimes Z$ and $I\otimes Z$ in the dense matrix. Its Hermitian eigensolver yields columns $v_j$, probabilities $|\langle v_j|\psi\rangle|^2$ and weights $\lambda_j$. Replacing a column by $e^{i\chi_j}v_j$ leaves $v_jv_j^\dagger$ and the squared overlap unchanged. Three fresh angles are checked in the separate author transfer; that execution is not independent review.

**B.** The matrix is $.31(X\otimes I\otimes I\otimes Y)-.27(I\otimes I\otimes Z\otimes I)+.12(I\otimes X\otimes I\otimes I)$. Native Y(q3) @ X(q0) still names this q0-leftmost matrix. The transfer checks sixteen basis inputs and one complex product, for twenty transfer circuits together with A.

**C.** Z has only outcomes +1 and −1, each with probability 1/2 for |+⟩, giving mean zero. Linearity follows from inner-product distributivity without any joint probability assumption. In particular X+Z has eigenvalues ±√2, not −2,0,+2.

**D.** With the original eigenvalues ±r, the new eigenvalues are $.5\mp2r$ meV, or $10^{-3}(.5\mp2r)$ eV; their order reverses under the negative multiplier. The mean is $10^{-3}(.5-2\langle H\rangle)$ eV. Projectors and their probabilities remain unchanged, up to relabeling. Degenerate eigenspace rotations preserve the grouped projector; individual refined probabilities may change but their equal-weight sum does not.

</details>

### Sources, depth and next step

The frozen source target is Nielsen and Chuang, 10th Anniversary Edition (2010), §2.2.5, beginning at printed page 87; its assigned locator is retained without claiming fresh inspection of the user-local PDF. A publicly accessible author source checked for this section is [John Preskill, Caltech Chapter 2, §2.1](https://www.preskill.caltech.edu/ph219/chap2_15.pdf), equations (2.4)–(2.9), PDF pages 5–6; its served header says July 2015. These give the finite spectral/projective setup and weighted expectation identity. Our proof and worked translations are supplied above; mixed-state formulas and statistical estimators are deferred.

The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/6.3.json) keeps author checks distinct from independent mathematics/implementation review and reader trials, which remain pending. Continue with [6.4 Measuring in another basis](#sec-measurement-expectation-values-and-statistical-estimation-4).

<span id="sec-measurement-expectation-values-and-statistical-estimation-4"></span>

## 6.4 Measuring in another basis

The simulator's computational probability query does not require every experiment to be interpreted in the computational basis. We can apply a unitary analyzer first. The essential questions are which unitary to apply, which basis its output labels describe, and which state the returned statevector represents.

Prerequisites are [3.5](ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-5), for conjugation and basis changes; [5.1](ch-gates-reversible-computation-and-circuit-synthesis.md#sec-gates-reversible-computation-and-circuit-synthesis-1), for chronological calls and inverse circuits; and [6.3](#sec-measurement-expectation-values-and-statistical-estimation-3), for spectral outcome values and expectations. Depth **F** requires the complete effective-projector proof and explicit X/Y analyzer derivations given below.

All examples execute actual pre-readout gates in released FlagQuantum 0.3.1/PyTorch 2.13.0, using CPU complex128 with absolute implementation tolerance $10^{-12}$ and relative tolerance zero. Native probabilities are exact predictions after those gates, rather than sampled labels or hardware observations. We compare full complex vectors without phase alignment and probabilities without clipping or normalization repair.

<span id="formula-code-6-4-effective"></span>

### 1. Conjugate the measured projector in the correct direction

Let $|\psi\rangle$ be the normalized original register state, R a unitary applied before readout, and $Q_a$ a projector for a computational readout event.

**Formula and complete proof.** The rotated state is $|\eta\rangle=R|\psi\rangle$. Its event probability is

$$
p_a=\langle\eta|Q_a|\eta\rangle
=\langle\psi|R^\dagger Q_aR|\psi\rangle,\qquad
P_a^{\mathrm{effective}}=R^\dagger Q_aR.
$$

Hermiticity follows from $(R^\dagger Q_aR)^\dagger=R^\dagger Q_aR$. For a complete orthogonal readout family, unitarity gives

$$
P_a^{\mathrm{effective}}P_c^{\mathrm{effective}}
=R^\dagger Q_aRR^\dagger Q_cR
=\delta_{ac}R^\dagger Q_aR,\qquad
\sum_aP_a^{\mathrm{effective}}=R^\dagger IR=I.
$$

Thus the rotated readout implements exactly this projective probability family on the original input. The proof holds for an arbitrary pure global register, including entangled inputs and higher-rank computational events.

If columns of a unitary B are the desired orthonormal vectors $|b_j\rangle=B|j\rangle$, choose **R=B†**. Then

$$
P_j=B|j\rangle\langle j|B^\dagger
=|b_j\rangle\langle b_j|,\qquad
p_j=|\langle b_j|\psi\rangle|^2
=|(B^\dagger\psi)_j|^2.
$$

B prepares basis vectors from computational labels; B† analyzes an unknown input in that basis. These directions agree only for special self-adjoint B, such as H.

**FlagQuantum code → result.** Run the snippets cumulatively from the repository root. The query returns the actual rotated vector and native computational probabilities. The leading dimension is an execution batch. Our explicit conjugated projectors are an independent classical prediction, rather than a claimed native general-projector request.

```python
import math
import torch
import flagquantum as fq
import examples.foundations.basis_measurement as a
b = a.b
calls = 0
def query(circuit, selected=None):
    global calls
    request = fq.probabilities() if selected is None else fq.probabilities(qubits=selected)
    result = fq.run(circuit,outputs=[request],options=b.OPTIONS)
    v,p = result.statevector(),result.probabilities
    assert v.shape == (1,2**circuit.n_qubits)
    assert p.shape == (1,2**(circuit.n_qubits if selected is None else len(selected)))
    assert v.dtype == b.D and p.dtype == torch.float64
    calls += 1
    return v[0],p[0]
initial = torch.tensor([.6,.8j],dtype=b.D)
prep = b.prepare_matrix(initial)
B = a.tilted(.4,.2)
R = B.mH
after,p = query(fq.Circuit(1,dtype=b.D).unitary(0,unitary=prep).rz(0,-.2).ry(0,-.4))
E,names = b.basis_family(1)
effective = tuple(R.mH@Q@R for Q in E)
torch.testing.assert_close(p,b.born(initial,effective,names),rtol=0,atol=b.ATOL)
a.full_check(initial,B,('b0','b1'),after,p)
print('Effective projectors R-dagger |j><j| R match native probabilities:',*(f'{x:.6f}' for x in p))
```
```text
Effective projectors R-dagger |j><j| R match native probabilities: 0.408187 0.591813
```

<span id="formula-code-6-4-x"></span>

### 2. Derive X readout: apply H before computational readout

**Formula.** The X eigenbasis is

$$
|x_+\rangle=\frac{|0\rangle+|1\rangle}{\sqrt2},\qquad
|x_-\rangle=\frac{|0\rangle-|1\rangle}{\sqrt2},\qquad
B_X=H=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}.
$$

**Derivation.** Multiplying X by these vectors gives ± the same vector. Their columns form H, and direct multiplication gives $H^\dagger=H$ and $H^2=I$. The analyzer is therefore H itself. Its effective projectors are
$P_{x_\pm}=(I\pm X)/2$, obtained by taking the outer products of the displayed vectors. Hence $HZH=X$ and $\langle X\rangle=p_0-p_1$ after H. Computational label 0 means X+, while label 1 means X−; the measured numerical values are +1 and −1, rather than the bit values 0 and 1.

```python
after,p = query(fq.Circuit(1,dtype=b.D).unitary(0,unitary=prep).h(0))
a.full_check(initial,a.H,('X+','X-'),after,p)
xmean = (p[0]-p[1]).item()
assert abs(xmean-torch.vdot(initial,a.X@initial).real.item())<b.ATOL
torch.testing.assert_close(a.H@a.Z@a.H,a.X,rtol=0,atol=b.ATOL)
print('H then computational readout: X+ and X- probabilities',*(f'{x:.6f}' for x in p))
```
```text
H then computational readout: X+ and X- probabilities 0.500000 0.500000
```

<span id="formula-code-6-4-y"></span>

### 3. Derive Y readout and fix its phase sign

**Formula.** With $S=\operatorname{diag}(1,i)=P(\pi/2)$,

$$
|y_\pm\rangle=\frac{|0\rangle\pm i|1\rangle}{\sqrt2},\qquad
B_Y=SH,\qquad
R_Y=B_Y^\dagger=HS^\dagger.
$$

**Derivation.** Using $Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix}$, multiplication gives $Y(1,\pm i)^T=\pm(1,\pm i)^T$. Multiplying the H columns by S produces precisely these normalized vectors. Therefore the inverse analyzer applies **S† first, H second**, since the rightmost matrix acts first. As a matrix check,

$$
R_Y^\dagger ZR_Y=SHZH S^\dagger
=SXS^\dagger
=\begin{pmatrix}0&-i\\i&0\end{pmatrix}=Y.
$$

The actual calls are P(−π/2), then H. Replacing P(−π/2) by P(+π/2) gives $S^\dagger XS=-Y$ in the effective observable and swaps the meanings of labels 0 and 1. A generic probability check alone can miss that mistake; both Y eigenstates make the sign test decisive.

```python
BY = a.S@a.H
RY = a.H@a.S.mH
torch.testing.assert_close(RY.mH@a.Z@RY,a.Y,rtol=0,atol=b.ATOL)
for sign in (1,-1):
    ystate = torch.tensor([1,sign*1j],dtype=b.D)/math.sqrt(2)
    yprep = b.prepare_matrix(ystate)
    after,p = query(fq.Circuit(1,dtype=b.D).unitary(0,unitary=yprep).p(0,-math.pi/2).h(0))
    a.full_check(ystate,BY,('Y+','Y-'),after,p)
    expected = torch.tensor([1.,0.] if sign==1 else [0.,1.],dtype=torch.float64)
    torch.testing.assert_close(p,expected,rtol=0,atol=b.ATOL)
    print(f'Y eigenstate sign {sign:+d}: P(-pi/2), H -> probabilities',*(f'{x:.6f}' for x in p))
```
```text
Y eigenstate sign +1: P(-pi/2), H -> probabilities 1.000000 0.000000
Y eigenstate sign -1: P(-pi/2), H -> probabilities 0.000000 1.000000
```

<span id="formula-code-6-4-tilted"></span>

### 4. Build a complex tilted basis with the inverse call order

Let $B=R_z(\phi)R_y(\theta)$, with θ and φ declared in **radians**. Write $c=\cos(\theta/2)$ and $s=\sin(\theta/2)$.

**Formula.** Its columns and analyzer are

$$
B=
\begin{pmatrix}
ce^{-i\phi/2}&-se^{-i\phi/2}\\
se^{i\phi/2}&ce^{i\phi/2}
\end{pmatrix},\qquad
R=B^\dagger=R_y(-\theta)R_z(-\phi).
$$

**Derivation.** Multiply the diagonal Rz matrix by Ry to obtain the columns. Inverting a product reverses its factors and changes the rotation angles' signs, as proved in 5.1. Preparing B uses chronological Ry(θ),Rz(φ); analyzing uses chronological **Rz(−φ),Ry(−θ)**. The matrix expression and call list must not be read in the same direction.

The conjugations from 3.5 give
$R_y(\theta)ZR_y(-\theta)=\cos\theta Z+\sin\theta X$ and
$R_z(\phi)XR_z(-\phi)=\cos\phi X+\sin\phi Y$.
Substitution yields

$$
BZB^\dagger
=\sin\theta\cos\phi\,X+\sin\theta\sin\phi\,Y+\cos\theta\,Z,
$$

$$
p_0=\frac{1+\langle BZB^\dagger\rangle_\psi}{2},\qquad p_1=1-p_0.
$$

This proves both the axis convention and the plus/minus interpretation. The native rotated probabilities are checked against this formula and independent column overlaps.

```python
theta,phi = .71,.43
Bt = a.tilted(theta,phi)
after,p_tilt = query(fq.Circuit(1,dtype=b.D).unitary(0,unitary=prep).rz(0,-phi).ry(0,-theta))
a.full_check(initial,Bt,('tilted+','tilted-'),after,p_tilt)
axis = math.sin(theta)*math.cos(phi)*a.X+math.sin(theta)*math.sin(phi)*a.Y+math.cos(theta)*a.Z
torch.testing.assert_close(Bt@a.Z@Bt.mH,axis,rtol=0,atol=b.ATOL)
formula = (1+torch.vdot(initial,axis@initial).real)/2
torch.testing.assert_close(p_tilt[0],formula,rtol=0,atol=b.ATOL)
print('Tilted basis: call Rz(-phi), then Ry(-theta); plus probability',f'{p_tilt[0]:.6f}')
```
```text
Tilted basis: call Rz(-phi), then Ry(-theta); plus probability 0.524260
```

A bare number does not reveal an intended unit: passing 90 means 90 radians here, not 90 degrees. Convert degrees explicitly before calling. The helper's magnitude limit of 100 radians is a teaching-input guard, not a FlagQuantum limitation or an automatic unit detector.

<span id="formula-code-6-4-local"></span>

### 5. Keep ordered partial labels on a correlated register

For selected qubits $S=(s_0,\ldots,s_{k-1})$, let $Q_a$ be the computational projector that keeps all bitstrings whose selected bits equal a in this order.

**Formula.**

$$
p_S(a)=\sum_{j:\,j_S=a}|(R\psi)_j|^2
=\langle\psi|R^\dagger Q_aR|\psi\rangle.
$$

**Derivation.** In rotated coordinates, mutually exclusive compatible bitstrings have probabilities given by squared coordinate magnitudes. Summing them is the diagonal projector $Q_a$. Applying unit 1's conjugation proves the second expression. This derivation makes no product-state assumption: the unmeasured coordinates remain part of the original global vector.

Apply the Y analyzer to q2 and X analyzer to q0. Native labels requested as (q2,q0) name those measured axes in that order; they do not rename the dense q0-leftmost statevector axes. Their probability parity is

$$
p_{00}-p_{01}-p_{10}+p_{11}
=\langle X_0Y_2\rangle
=\langle X\otimes I\otimes Y\rangle.
$$

To prove this, weight each rotated label by its product of ±1 eigenvalues and use the two local conjugations. Identity on spectator q1 stays in the dense matrix.

```python
factors = b.complex_factors(3)
circuit = fq.Circuit(3,dtype=b.D)
for q,factor in enumerate(factors):
    circuit.unitary(q,unitary=b.prepare_matrix(torch.tensor(factor,dtype=b.D)))
circuit.ry(0,.29).cx(0,2).p(1,-.31)
pre = (('ry',(0,),(.29,)),('cx',(0,2),()),('p',(1,),(-.31,)))
original = a.matrix(3,pre)@b.product_input(factors)
read = (('p',(2,),(-math.pi/2,)),('h',(2,),()),('h',(0,),()))
R = a.matrix(3,read)
circuit.p(2,-math.pi/2).h(2).h(0)
after,p = query(circuit,(2,0))
Q,names = b.marginal_family(3,(2,0))
P = tuple(R.mH@q@R for q in Q)
torch.testing.assert_close(after,R@original,rtol=0,atol=b.ATOL)
torch.testing.assert_close(p,b.born(original,P,names),rtol=0,atol=b.ATOL)
parity = p[0]-p[1]-p[2]+p[3]
observable = torch.kron(torch.kron(a.X,a.I),a.Y)
torch.testing.assert_close(parity,torch.vdot(original,observable@original).real,rtol=0,atol=b.ATOL)
print('Native labels ordered (q2,q0):',names,'; local Y(q2)/X(q0) parity mean',f'{parity:.6f}')
```
```text
Native labels ordered (q2,q0): ('00', '01', '10', '11') ; local Y(q2)/X(q0) parity mean -0.268800
```

<span id="formula-code-6-4-bell"></span>

### 6. Analyze an entangled basis with an entangling inverse

A general register basis need not be a product of one-qubit bases. Define the two-qubit Bell preparation B by chronological H(q0),CX(q0,q1), so $B=CX_{0,1}(H\otimes I)$.

**Formula and derivation.** Apply these two gates to each computational input:

$$
B|00\rangle=|\Phi_+\rangle,\quad B|01\rangle=|\Psi_+\rangle,\quad
B|10\rangle=|\Phi_-\rangle,\quad B|11\rangle=|\Psi_-\rangle,
$$

where $|\Phi_\pm\rangle=(|00\rangle\pm|11\rangle)/\sqrt2$ and
$|\Psi_\pm\rangle=(|01\rangle\pm|10\rangle)/\sqrt2$.
The first input bit selects the H relative sign; the controlled flip selects correlated or anticorrelated computational pairs. Since CX and H are individually self-inverse, $B^\dagger=(H\otimes I)CX_{0,1}$: call **CX first, H second**.

Unit 1's proof then identifies readout labels 00,01,10,11 with Φ+,Ψ+,Φ−,Ψ−. The example verifies both Φ+ and Ψ−; the complete program checks all four and a complex superposition in the Bell basis. A coherent gate network is being executed before exact computational probability readout. This is not a claim about which hardware can perform these gates or resolve Bell states under additional platform restrictions.

```python
BB = a.matrix(2,(('h',(0,),()),('cx',(0,1),())))
bell_names = ('Phi+','Psi+','Phi-','Psi-')
for bits,index in [((0,0),0),((1,1),3)]:
    circuit = fq.Circuit(2,dtype=b.D)
    for q,bit in enumerate(bits):
        if bit: circuit.x(q)
    circuit.h(0).cx(0,1)
    before = BB@b.product_input(b.basis_factors(bits))
    circuit.cx(0,1).h(0)
    after,p = query(circuit)
    a.full_check(before,BB,bell_names,after,p)
    expected = torch.zeros(4,dtype=torch.float64); expected[index] = 1
    torch.testing.assert_close(p,expected,rtol=0,atol=b.ATOL)
    print(f'Bell input {bell_names[index]} -> computational label {index:02b}, probability {p[index]:.6f}.')
```
```text
Bell input Phi+ -> computational label 00, probability 1.000000.
Bell input Psi- -> computational label 11, probability 1.000000.
```

<span id="formula-code-6-4-labels"></span>

### 7. Separate basis-column phases from label permutations

**Formula.** Let D be diagonal with entries $e^{i\chi_j}$, and let the permutation matrix Π satisfy $\Pi|j\rangle=|\sigma(j)\rangle$. For $B'=BD\Pi$,

$$
|b'_j\rangle=e^{i\chi_{\sigma(j)}}|b_{\sigma(j)}\rangle,\qquad
p'_j=p_{\sigma(j)},\qquad
B'^\dagger=\Pi^\dagger D^\dagger B^\dagger.
$$

**Derivation.** Multiplication by Π selects column σ(j), and D supplies its phase. The phase cancels in the column's outer product and in the squared overlap, proving the probability relation. The inverse product proves the new analyzer. Thus column phases alone preserve label probabilities, while a column permutation requires the corresponding classical label mapping.

This is an equivalence of projective probability families. It does not authorize removing those phases if B is being reused as a coherent gate in another circuit. The full rotated vectors can differ by component phases; our full-vector comparisons retain them. The following actual analyzer combines new column phases with a column swap and declares the resulting labels explicitly.

```python
phase = torch.diag(torch.tensor([complex(math.cos(.2),math.sin(.2)),
                                  complex(math.cos(-.8),math.sin(-.8))],dtype=b.D))
Bnew = (Bt@phase)[:,[1,0]]
labels = ('old-minus','old-plus')
a.basis_family(Bnew,labels)
after,p = query(fq.Circuit(1,dtype=b.D).unitary(0,unitary=prep).unitary(0,unitary=Bnew.mH.contiguous()))
a.full_check(initial,Bnew,labels,after,p)
torch.testing.assert_close(p,p_tilt.flip(0),rtol=0,atol=b.ATOL)
print('Phased and swapped columns follow labels',labels,'; probabilities',*(f'{x:.6f}' for x in p))
```
```text
Phased and swapped columns follow labels ('old-minus', 'old-plus') ; probabilities 0.475740 0.524260
```

<span id="formula-code-6-4-boundary"></span>

### 8. Diagnose a wrong analyzer and identify the returned state

**Direction check.** On input $|b_0\rangle$, the correct analyzer B† must give label 0 with probability one. Applying B instead measures a different effective family, except in special cases. The diagnostic below submits that wrong forward B, checks its actual full vector $B|b_0\rangle$, and reports its incorrect-for-the-target probabilities. Successful verification of the submitted wrong circuit does not make it a correct implementation of the desired measurement.

**Input contract.** The helper requires a square, finite, unitary CPU complex128 basis matrix and a distinct label for every column. It rejects a nonorthogonal basis rather than repairing it with QR, since QR would change the requested vectors. It also rejects invalid shapes, duplicate labels, nonfinite angles and ambiguous nonnumeric angle declarations.

**State boundary.** An exact native probability query returns the rotated **pre-measurement** vector $B^\dagger\psi$, alongside predicted probabilities; it does not return a sampled collapsed state. If an actual ideal computational measurement subsequently produced a possible j, write $\eta_j=(B^\dagger\psi)_j$ and $p_j=|\eta_j|^2>0$. Its normalized branch in that physical frame would be $\eta_j|j\rangle/\sqrt{p_j}$. Returning it to the original frame requires B and gives $\eta_j|b_j\rangle/\sqrt{p_j}=P_j\psi/\sqrt{p_j}$, consistent with the ideal update in 6.2. These are the isolated rays |j⟩ and |b_j⟩, respectively, but the explicit phase representative is retained in a full-vector comparison. We do not execute that measurement/update process here. Basis probabilities, logical analyzer gates and hardware measurement calibration remain separate claims.

```python
b0 = Bt[:,0]
after,wrong = query(fq.Circuit(1,dtype=b.D).unitary(0,unitary=b.prepare_matrix(b0)).unitary(0,unitary=Bt))
torch.testing.assert_close(after,Bt@b0,rtol=0,atol=b.ATOL)
assert wrong[1].item()>.1
desired = b.born(b0,a.basis_family(Bt,('plus','minus')),('plus','minus'))
torch.testing.assert_close(desired,torch.tensor([1.,0.],dtype=torch.float64),rtol=0,atol=b.ATOL)
assert a.invalid_checks()==10 and calls==10
print(f'Wrong forward-B analyzer on b0: undesired label-1 probability {wrong[1]:.6f}; desired probability {desired[1]:.6f}.')
print('10 malformed contracts rejected; 10 actual native body circuits; returned states are pre-measurement rotated vectors, not collapsed branches.')
```
```text
Wrong forward-B analyzer on b0: undesired label-1 probability 0.405548; desired probability 0.000000.
10 malformed contracts rejected; 10 actual native body circuits; returned states are pre-measurement rotated vectors, not collapsed branches.
```

### Complete program and expected output

Run the [complete program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/basis_measurement.py):

    python examples/foundations/basis_measurement.py

It executes 54 native circuits: 21 single-qubit, 18 correlated-register, five Bell-basis, six phase/relabel and four diagnostic cases. Explicit scalar overlaps, conjugated projectors, indexed preparations and full rotated vectors check the actual submitted circuits. The two kinds of deliberately wrong analyzer are predicted correctly as wrong for the target basis, rather than silently repaired.

Run the eight cumulative body fragments and compare actual stdout with:

    python scripts/check_basis_measurement_prose.py

The body executes ten native circuits. Numerical validation supports the implementation; it does not replace the complete conjugated-projector and X/Y derivations above.

Expected output of the complete program:

```text
21 single-qubit circuits: X, Y and complex tilted bases; full rotated vectors, overlap probabilities and Pauli signs passed.
18 correlated-register circuits: all six ordered two-qubit selections with local Y/X rotations and native partial readout passed.
5 Bell-basis circuits: entangling preparation, inverse analyzer and 00/01/10/11 labels Phi+/Psi+/Phi-/Psi- passed.
6 phase/relabel circuits: independent column phases preserve probabilities; column permutation follows declared labels.
4 diagnostic circuits: forward B is not its inverse analyzer; wrong Y phase swaps plus/minus labels, without correcting submitted results.
10 malformed basis/angle/label contracts rejected; radian inputs, exact labels and full-vector phases retained.
54 actual CPU complex128 circuits; native post-rotation exact probabilities, not shots, hardware calibration or a post-measurement statevector.
```

### Understanding checks and transfer exercises

**6.4-A — Fresh tilted axes.** Use three new pairs of θ,φ and a complex qubit input. Compute B's columns explicitly, execute Rz(−φ),Ry(−θ), and compare native probabilities with scalar overlaps. Test the two new basis eigenstates as inputs.

**6.4-B — Larger partial readout.** On four qubits prepare a complex product, apply Ry(q1,.32),CX(q3,q0),P(q0,−.28), then analyze Y on q3 and X on q1. Request labels ordered (q3,q1). Verify the full rotated vector, each conjugated partial projector and the compatible-index sum, for basis inputs as well as the complex product.

**6.4-C — A sign hidden by a symmetric state.** Why might using P(+π/2),H accidentally pass a probability test on |0⟩? Which two inputs establish the Y sign and label convention?

**6.4-D — Readout versus state.** If B's columns are rephased, which probabilities stay invariant and which returned vector coordinates change? Does a computational-probability request imply that a physical measurement was sampled? What extra gate would restore an ideal selected branch to the original basis?

<details markdown="1">
<summary>Answers and reasoning for 6.4</summary>

**A.** The columns are $(ce^{-i\phi/2},se^{i\phi/2})^T$ and $(-se^{-i\phi/2},ce^{i\phi/2})^T$. For each original input ψ, native p(j) must equal $|\sum_k\overline{B_{kj}}\psi_k|^2$. The corresponding basis-vector inputs give deterministic labels 0 and 1. The separate author transfer checks three new angle pairs on the complex input and both eigenstates.

**B.** Let R be the complete analyzer, including identity on q0,q2. For each label a, let $Q_a=\sum_{j:j_3j_1=a}|j\rangle\langle j|$. Check $\psi^\dagger R^\dagger Q_aR\psi=\sum_{j:j_3j_1=a}|(R\psi)_j|^2$. The first label bit names Y(q3), not the most significant dense register coordinate. The transfer tests four selected basis inputs and a complex product; it records author execution rather than reader trials.

**C.** Both Y signs give probabilities 1/2,1/2 on |0⟩. Use $(|0\rangle+i|1\rangle)/\sqrt2$ and $(|0\rangle-i|1\rangle)/\sqrt2$: the correct analyzer maps them to labels 0 and 1 respectively. Replacing S† by S swaps those labels.

**D.** Independent column phases cancel in projectors and squared overlaps. The corresponding B† output coordinates acquire inverse phases and are retained in full-vector comparisons. The exact probability request predicts a distribution without producing a sampled outcome or collapsed state. Under a separately assumed ideal measurement, applying B maps the normalized rotated branch $\eta_j|j\rangle/\sqrt{p_j}$ to $\eta_j|b_j\rangle/\sqrt{p_j}$ in the original frame. The isolated ray is |b_j⟩; this convention retains its scalar phase.

</details>

### Sources, depth and next step

The frozen source target is Nielsen and Chuang, 10th Anniversary Edition (2010), §1.3.3, “Measurements in bases other than the computational basis,” beginning at printed page 22. Its assigned locator is retained without claiming fresh inspection of the user-local textbook PDF. For the imported finite spectral/Born setup, [Preskill's Caltech Chapter 2, §2.1](https://www.preskill.caltech.edu/ph219/chap2_15.pdf), equations (2.4)–(2.7), PDF page 5, was checked; its served header says July 2015. The analyzer-direction, X/Y, label and register derivations are given explicitly here.

The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/6.4.json) keeps author execution distinct from independent mathematical/implementation review and reader trials, which remain pending. Continue with [6.5 Generalized measurements and instruments](#sec-measurement-expectation-values-and-statistical-estimation-5).

<span id="sec-measurement-expectation-values-and-statistical-estimation-5"></span>

## 6.5 Generalized measurements and instruments [Advanced]

Projectors describe an important measurement model, but not every measurement probability is a projection onto an orthogonal subspace. Moreover, probabilities do not determine the disturbance caused by an apparatus. We now distinguish three objects that are sometimes all informally called “the measurement.”

| Object | What is specified? | What is not determined by that object alone? |
|---|---|---|
| POVM effects $E_a$ | Probabilities for the reported labels a on each input | The conditional output state |
| Measurement operators $K_{a,k}$ | One representation of an outcome's finer update branches | A unique physical implementation or unique operator representation |
| Instrument | The outcome-indexed operational rule for probabilities and subsequent state-dependent predictions | A unique choice of operators representing that rule |

Our prerequisites are [6.1](#sec-measurement-expectation-values-and-statistical-estimation-1), [6.2](#sec-measurement-expectation-values-and-statistical-estimation-2) and [2.4](ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-4). Depth **P** means that the generalized probability/update rules are stated as physical postulates, with their mathematical consistency derived. Inputs here are normalized **pure global states** on a finite space; the code uses square measurement operators on that same input/output space. We describe hidden branches as probability-weighted ensembles. General mixed-input instrument maps and their composition remain in [9.7](../section-plans/02-information.md#sec-quantum-channels-and-their-representations-7), after the density-operator foundations.

The examples use FlagQuantum 0.3.1/PyTorch 2.13.0, CPU complex128, absolute implementation tolerance $10^{-12}$ and relative tolerance zero. Supported unitary gates actually prepare states and couple an auxiliary meter qubit. Explicit classical code computes effects and conditional branches; it does not invent a native POVM/instrument request or claim a sampled collapse.

<span id="formula-code-6-5-effects"></span>

### 1. A POVM specifies probabilities, without specifying an update

**Postulate.** A finite positive operator-valued measure, or POVM, is a family of effects with declared classical labels a satisfying

$$
E_a^\dagger=E_a,\qquad E_a\ge0,\qquad \sum_aE_a=I.
$$

Positivity means $\langle v|E_a|v\rangle\ge0$ for every vector v. On a normalized pure input ψ, its probability rule is

$$
p(a\mid\psi)=\langle\psi|E_a|\psi\rangle.
$$

**Consistency derivation.** Positivity gives nonnegative probabilities; summing them gives $\langle\psi|I|\psi\rangle=1$. Also $I-E_a=\sum_{b\ne a}E_b\ge0$, so every effect lies between zero and I. None of these conditions requires $E_a^2=E_a$ or orthogonality of different effects. Projective measurement is the special case where the effects are orthogonal projectors.

For a dimensionless strength $0\le\kappa\le1$, consider

$$
E_0=\frac{I+\kappa Z}{2},\qquad E_1=\frac{I-\kappa Z}{2}.
$$

Their diagonal eigenvalues are $(1\pm\kappa)/2$, proving positivity and completeness directly. At κ=0 they describe a fair label independent of the input; at κ=1 they are the Z projectors. At intermediate strengths they are not projectors: $E_0E_1=(1-\kappa^2)I/4$. The labels' assigned values +1,−1 would have mean $\kappa\langle Z\rangle$, rather than the unscaled Z mean.

**FlagQuantum preparation → classical formula → result.** Run the eight snippets cumulatively from the repository root. The native call prepares an actual simulated input; the two effect probabilities are then computed by our original classical helper. They are not a dedicated native POVM query.

```python
import math
import torch
import flagquantum as fq
import examples.foundations.generalized_measurements as g
b = g.b
calls = 0
helper_start = b.RUNS
def query(circuit,selected=None):
    global calls
    request = fq.probabilities() if selected is None else fq.probabilities(qubits=selected)
    result = fq.run(circuit,outputs=[request],options=b.OPTIONS)
    v,p = result.statevector(),result.probabilities
    assert v.shape == (1,2**circuit.n_qubits)
    assert p.shape == (1,2**(circuit.n_qubits if selected is None else len(selected)))
    assert v.dtype == b.D and p.dtype == torch.float64
    calls += 1
    return v[0],p[0]
psi = torch.tensor([.6,.8j],dtype=b.D)
prepared,_ = query(fq.Circuit(1,dtype=b.D).unitary(0,unitary=b.prepare_matrix(psi)))
torch.testing.assert_close(prepared,psi,rtol=0,atol=b.ATOL)
kappa = .6
effects = ((g.I+kappa*g.Z)/2,(g.I-kappa*g.Z)/2)
names = ('meter-0','meter-1')
p = g.povm(prepared,effects,names)
assert not torch.allclose(effects[0]@effects[0],effects[0],rtol=0,atol=b.ATOL)
torch.testing.assert_close(p,torch.tensor([.416,.584],dtype=torch.float64),rtol=0,atol=b.ATOL)
print('POVM probabilities:',*(f'{x:.6f}' for x in p),'; effects are not projectors.')
```
```text
POVM probabilities: 0.416000 0.584000 ; effects are not projectors.
```

<span id="formula-code-6-5-operators"></span>

### 2. Measurement operators add the conditional-update information

First consider **one** measurement operator $M_a$ per reported outcome, with

$$
E_a=M_a^\dagger M_a,\qquad \sum_aM_a^\dagger M_a=I.
$$

**Postulated update and consistency.** The branch has probability
$p_a=\|M_a\psi\|^2=\langle\psi|E_a|\psi\rangle$. For $p_a>0$, the conditional pure state is

$$
|\psi_a\rangle=\frac{M_a|\psi\rangle}{\sqrt{p_a}},\qquad
\langle\psi_a|\psi_a\rangle=1.
$$

The equal probability formulas follow by the definition of the adjoint; dividing the branch norm squared by $p_a$ proves normalization. Interpreting this vector as the apparatus's conditional output is the extra physical update rule. The operator $M_a$ need not be Hermitian, positive, projective or unitary. In particular, a nonunitary $M_a$ must not be submitted as a unitary circuit gate.

For the weak effects above, set $u=\sqrt{(1+\kappa)/2}$ and $v=\sqrt{(1-\kappa)/2}$:

$$
M_0=\begin{pmatrix}u&0\\0&v\end{pmatrix},\qquad
M_1=\begin{pmatrix}v&0\\0&u\end{pmatrix}.
$$

Squaring these diagonal matrices gives the specified effects; their squared sum is I. Conditional normalization divides by the input-dependent branch probability, not by the matrix's norm. We retain the complex scalar phase in the declared vector representative, as in 6.2.

More generally, a positive effect admits a square root: diagonalize it with nonnegative eigenvalues and take their nonnegative square roots. Then $M_a=U_a\sqrt{E_a}$, for any unitary $U_a$, obeys $M_a^\dagger M_a=E_a$. This supplies candidate updates but does not select the update implemented by a real apparatus.

```python
groups = g.weak(kappa)
p_operator,records = g.instrument(prepared,groups,names)
for j,group in enumerate(groups):
    M = group[0]
    torch.testing.assert_close(M.mH@M,effects[j],rtol=0,atol=b.ATOL)
    w = M@prepared
    norm_probability = torch.vdot(w,w).real
    normalized = w/torch.sqrt(norm_probability)
    torch.testing.assert_close(p_operator[j],norm_probability,rtol=0,atol=b.ATOL)
    torch.testing.assert_close(records[j][0][1],normalized,rtol=0,atol=b.ATOL)
torch.testing.assert_close(p_operator,p,rtol=0,atol=b.ATOL)
print('Measurement-operator probabilities equal POVM probabilities; both conditional vectors have unit norm and retain their complex phase.')
```
```text
Measurement-operator probabilities equal POVM probabilities; both conditional vectors have unit norm and retain their complex phase.
```

<span id="formula-code-6-5-same-effects"></span>

### 3. Construct different instruments with exactly the same POVM

Compare the preceding update with

$$
N_0=M_0,\qquad N_1=XM_1.
$$

**Derivation.** Since $X^\dagger X=I$, $N_1^\dagger N_1=M_1^\dagger M_1$ and the effects agree for **every** input, not just a tested example. Yet the outcome-1 conditional vector changes from $M_1\psi/\sqrt{p_1}$ to $XM_1\psi/\sqrt{p_1}$. On input |0⟩ and κ=.6, both give probability .2 for outcome 1; the first leaves |0⟩ and the second gives |1⟩. Their next Z predictions are +1 and −1, so they are operationally different instruments.

The POVM alone cannot decide between them. Conversely, changing $M_a$ by an outcome-dependent scalar phase would not change the isolated conditional ray or any subsequent probabilities. Thus “different operator lists” is not by itself sufficient to establish different instruments; a difference in operational predictions is needed.

**Actual native realization check.** The helper below executes the meter-coupling circuit derived in unit 4. In the second implementation it adds a coherent meter-controlled X. The reported conditional vectors are extracted classically from the actual joint simulation; no mid-circuit classical feedback or sampled measurement API is claimed.

```python
zero = torch.tensor([1,0],dtype=b.D)
for flip in (False,True):
    joint,native = g.native_weak(zero,kappa,flip)
    operators = g.weak(kappa,flip)
    probabilities,branches = g.instrument(zero,operators,names)
    torch.testing.assert_close(native,probabilities,rtol=0,atol=b.ATOL)
    selected = branches[1][0][1]
    zmean = torch.vdot(selected,g.Z@selected).real.item()
    assert abs(zmean-(-1 if flip else 1))<b.ATOL
    print(f'Outcome-1 update flip={flip}: probability {native[1]:.6f}; conditional Z mean {zmean:+.6f}.')
```
```text
Outcome-1 update flip=False: probability 0.200000; conditional Z mean +1.000000.
Outcome-1 update flip=True: probability 0.200000; conditional Z mean -1.000000.
```

<span id="formula-code-6-5-dilation"></span>

### 4. Realize the weak operators through a unitary meter coupling

Let the system be q0 and an auxiliary meter be q1, initially |0⟩. We want the joint premeasurement state

$$
|\Omega\rangle=M_0|\psi\rangle\otimes|0\rangle
+M_1|\psi\rangle\otimes|1\rangle.
$$

**Derivation of the gates.** For $\psi=\alpha|0\rangle+\beta|1\rangle$, the desired amplitudes in order 00,01,10,11 are
$(u\alpha,v\alpha,v\beta,u\beta)$. Set
$\gamma_0=2\arccos u$ and $\gamma_1=2\arccos v$, in radians. An Ry(γ0) on the meter makes its amplitudes u,v. A controlled Ry(γ1−γ0), with q0 controlling q1, changes the meter rotation to Ry(γ1) only when the system bit is 1. That branch has meter amplitudes v,u. This proves the displayed joint vector for arbitrary complex α,β by linearity.

Native computational probabilities on q1 therefore give
$p_a=\sum_s|\Omega_{2s+a}|^2=\|M_a\psi\|^2$.
The joint slices at indices [0,2] and [1,3] are precisely the unnormalized system branches. Dividing a nonzero slice by $\sqrt{p_a}$ predicts its conditional pure state under an ideal later meter readout. At a mathematically zero branch, small native floating residuals are checked by the implementation tolerance rather than normalized or clipped.

For $N_1=XM_1$, an additional CX(q1,q0) flips the system only within the meter-1 component. Its norm and hence the meter probability stay unchanged. This is a coherent controlled gate before readout, not an invoked classical feed-forward endpoint.

```python
alpha = math.sqrt((1+kappa)/2)
beta = math.sqrt((1-kappa)/2)
gamma0,gamma1 = 2*math.acos(alpha),2*math.acos(beta)
circuit = fq.Circuit(2,dtype=b.D).unitary(0,unitary=b.prepare_matrix(psi))
circuit.ry(1,gamma0).cry(0,1,gamma1-gamma0)
joint,meter = query(circuit,(1,))
expected = torch.zeros(4,dtype=b.D)
for j in (0,1):
    expected[j::2] = groups[j][0]@psi
torch.testing.assert_close(joint,expected,rtol=0,atol=b.ATOL)
torch.testing.assert_close(meter,p_operator,rtol=0,atol=b.ATOL)
for j in (0,1):
    torch.testing.assert_close(joint[j::2]/torch.sqrt(meter[j]),records[j][0][1],rtol=0,atol=b.ATOL)
print('Native system q0 / zero meter q1: full joint amplitudes match M0|psi>|0> + M1|psi>|1>.')
print('Meter probabilities:',*(f'{x:.6f}' for x in meter),'; conditional branches extracted classically.')
```
```text
Native system q0 / zero meter q1: full joint amplitudes match M0|psi>|0> + M1|psi>|1>.
Meter probabilities: 0.416000 0.584000 ; conditional branches extracted classically.
```

For a general complete operator family, the map
$W\psi=\sum_aM_a\psi\otimes|a\rangle$ preserves inner products because
$W^\dagger W=\sum_aM_a^\dagger M_a=I$. This explains the isometric structure behind a meter model. Here we construct and execute the specific weak family; we do not claim a native general dilation compiler, an efficient implementation for every POVM or a calibrated hardware realization.

<span id="formula-code-6-5-trine"></span>

### 5. A genuinely three-outcome qubit POVM

A projective measurement on a two-dimensional system has at most two nonzero mutually orthogonal projectors. General effects can instead have three nonzero alternatives.

**Formula.** Let $\phi_j=2\pi j/3$ and

$$
|t_j\rangle=\frac{|0\rangle+e^{i\phi_j}|1\rangle}{\sqrt2},\qquad
E_j=\frac23|t_j\rangle\langle t_j|,\qquad j=0,1,2.
$$

**Derivation.** Each effect is positive with eigenvalues 2/3 and zero, so it is not a projector. Summing its 2×2 matrix gives diagonal entries one and off-diagonal entries zero, using $1+e^{2\pi i/3}+e^{4\pi i/3}=0$. Thus the family is complete. Choose $M_j=\sqrt{2/3}|t_j\rangle\langle t_j|$; idempotence of the rank-one projector gives $M_j^\dagger M_j=E_j$.

For $\psi=\alpha|0\rangle+\beta|1\rangle$,

$$
p_j=\frac13|\alpha+e^{-i\phi_j}\beta|^2.
$$

On |+⟩ the three probabilities are 2/3,1/6,1/6. These are three classical labels of one qubit POVM, not a claim that an unextended one-qubit computational readout returns three distinct bitstrings.

```python
trine_input,_ = query(fq.Circuit(1,dtype=b.D).h(0))
trine_states,trine_groups,trine_effects = g.trine()
tp = g.povm(trine_input,trine_effects,('t0','t1','t2'))
ip,_ = g.instrument(trine_input,trine_groups,('t0','t1','t2'))
torch.testing.assert_close(tp,ip,rtol=0,atol=b.ATOL)
torch.testing.assert_close(tp,torch.tensor([2/3,1/6,1/6],dtype=torch.float64),rtol=0,atol=b.ATOL)
print('Trine outcomes on native |+> preparation:',*(f'{x:.6f}' for x in tp))
print('Three-outcome probabilities are classical predictions here; no native three-outcome measurement was submitted.')
```
```text
Trine outcomes on native |+> preparation: 0.666667 0.166667 0.166667
Three-outcome probabilities are classical predictions here; no native three-outcome measurement was submitted.
```

Only the input preparation above is executed natively. The trine effects, probabilities and operator branches are classical predictions in this example; a three-label dilation and its physical readout are not implemented here.

<span id="formula-code-6-5-instrument"></span>

### 6. An instrument can have hidden branches within one reported outcome

A reported outcome a can collect several unobserved fine alternatives k. Specify operators $K_{a,k}$, with

$$
E_a=\sum_kK_{a,k}^\dagger K_{a,k},\qquad
p_a=\sum_k\|K_{a,k}\psi\|^2.
$$

**Pure-input operational description.** If k is also known, its normalized state is
$K_{a,k}\psi/\sqrt{p_{a,k}}$, where $p_{a,k}=\|K_{a,k}\psi\|^2>0$.
If only a is reported and $p_a>0$, keep a classical ensemble with conditional weights $p_{a,k}/p_a$. It need not be a pure state. Do not sum and renormalize the branch vectors.

For a later projective event $Q_c$ with no intervening evolution, the instrument predicts the joint probabilities

$$
p(a,c)=\sum_k\|Q_cK_{a,k}\psi\|^2.
$$

**Consistency derivation.** Multiply each fine branch's later Born probability by $p_{a,k}$, cancel its normalization denominator, then sum the exclusive hidden alternatives. Summing over c returns $p_a$. These outcome-indexed subsequent predictions distinguish instruments in the pure-input sector. The full mixed-input map formalism and composition are deferred to 9.7.

**Same POVM, different coarse disturbance.** A single reported label “kept” can have effect I and either operator group {I} or {P0,P1}, where P0,P1 are the computational projectors. On |+⟩ the first preserves a later plus probability of 1; the second gives 1/2. Both report “kept” with probability one.

**Same instrument, different representation.** The hidden group {P0,P1} can be replaced by
$\{(P_0+P_1)/\sqrt2,(P_0-P_1)/\sqrt2\}=\{I/\sqrt2,Z/\sqrt2\}$.
More generally, if $L_j=\sum_kU_{jk}K_k$ with unitary U mixing hidden indices within one outcome, then

$$
\sum_j\|Q_cL_j\psi\|^2
=\sum_{k,\ell}\left(\sum_j\overline{U_{j\ell}}U_{jk}\right)
\langle Q_cK_\ell\psi|Q_cK_k\psi\rangle
=\sum_k\|Q_cK_k\psi\|^2.
$$

This proves unchanged later-event predictions and, with Q=I, unchanged coarse probability. It demonstrates why measurement operators are a representation of an instrument rather than its unique identity.

The following native circuits compare an uncoupled meter with a CNOT-coupled meter and read the system after H. Their local exact probabilities agree with the two coarse instrument predictions. We do not claim that either run sampled the hidden record. The unmeasured joint system and meter remain a coherent pure state; agreement of these local readout statistics does not establish that an actual classical record was created or discarded.

```python
plus = torch.tensor([1,1],dtype=b.D)/math.sqrt(2)
projectors,zn = b.basis_family(1)
Qplus = torch.outer(plus,plus.conj())
Q,qn = (Qplus,g.I-Qplus),('plus','minus')
do_nothing = ((g.I,),)
hidden_Z = ((projectors[0],projectors[1]),)
mixed_representation = ((g.I/math.sqrt(2),g.Z/math.sqrt(2)),)
same_effect = g.povm(plus,(g.I,),('kept',))
assert abs(same_effect[0].item()-1)<b.ATOL
torch.testing.assert_close(g.later(plus,hidden_Z,('kept',),Q,qn),
                           g.later(plus,mixed_representation,('kept',),Q,qn),rtol=0,atol=b.ATOL)
for entangle in (False,True):
    circuit = fq.Circuit(2,dtype=b.D).h(0)
    if entangle: circuit.cx(0,1)
    circuit.h(0)
    joint,readout = query(circuit,(0,))
    later = g.later(plus,hidden_Z if entangle else do_nothing,('kept',),Q,qn).sum(0)
    torch.testing.assert_close(readout,later,rtol=0,atol=b.ATOL)
    print(f'Effect I, hidden_Z={entangle}: later plus probability {readout[0]:.6f}.')
print('Hidden-operator mixing changes the representation, while the coarse instrument predictions remain identical.')
```
```text
Effect I, hidden_Z=False: later plus probability 1.000000.
Effect I, hidden_Z=True: later plus probability 0.500000.
Hidden-operator mixing changes the representation, while the coarse instrument predictions remain identical.
```

<span id="formula-code-6-5-boundaries"></span>

### 7. Keep impossible, hidden and numerically unresolved branches separate

For a coarse outcome with $p_a=0$, no normalized conditional ensemble is defined. A fine zero-probability branch has no normalized vector; its label remains present with None. For $p_a>0$, hidden fine branches remain explicitly separate, even if their vectors happen to be collinear on a particular input. Our helper reports the ensemble rather than claiming to classify its purity.

A positive probability below $10^{-12}$ is not impossible: that number is a comparison tolerance, not a probability cutoff. At κ=1, input $|0\rangle+10^{-10}i|1\rangle$ is normalized to floating precision and retains the positive $10^{-20}$ outcome-1 probability and its normalized phase representative $i|1\rangle$.

A nonzero projected component whose squared norm underflows to zero is instead rejected explicitly. The code checks this at amplitude $10^{-200}$. Dividing by a tiny probability can amplify input and rounding errors; these tests do not supply a relative-error or interval certificate for arbitrary rare events.

```python
p_edge,edge_rows = g.instrument(zero,g.weak(1.),names)
assert p_edge[1].item()==0 and edge_rows[1][0][1] is None
rare = torch.tensor([1,1e-10j],dtype=b.D)
p_rare,rare_rows = g.instrument(rare,g.weak(1.),names)
assert 0<p_rare[1].item()<b.ATOL
torch.testing.assert_close(rare_rows[1][0][1],torch.tensor([0,1j],dtype=b.D),rtol=0,atol=b.ATOL)
try:
    g.instrument(torch.tensor([1,1e-200j],dtype=b.D),g.weak(1.),names)
except FloatingPointError:
    pass
else:
    raise AssertionError('Underflow silently treated as impossible')
print('Exactly impossible branch -> None; positive 1e-20 branch retained; squared-norm underflow -> explicit error.')
```
```text
Exactly impossible branch -> None; positive 1e-20 branch retained; squared-norm underflow -> explicit error.
```

<span id="formula-code-6-5-support"></span>

### 8. State the implementation boundary precisely

| Operation in this section | Executed support | Limit |
|---|---|---|
| Prepare a pure input | Native unitary circuit gates | Ideal CPU statevector model |
| Weak family and outcome-controlled X | Native Ry, CRy and CX with a zero meter | One constructed two-qubit dilation; coherent control before readout |
| Read the meter or system probabilities | Native computational probability request with declared qubit selection | Exact distribution; no shot or sampled collapse in these examples |
| Arbitrary effect/operator groups and trine probabilities | Original PyTorch postprocessors of a simulated state | Not a native general POVM/instrument request |
| General mixed-state instruments and composition | Deferred to 9.7 | Not established by these examples |

The inspected public FlagQuantum 0.3.1 namespace does not expose requests named povm or instrument, and its Circuit public methods expose no such measurement/update method. This is a report of the checked version and interfaces, not a claim that generalized measurements cannot be realized with supported gates. The package also contains Kraus-channel/noise simulation code; such a channel representation does not by itself specify a reported outcome or establish an outcome-indexed instrument API. We do not invoke those noise functions here.

The book helpers validate positive complete effects, complete operator groups, normalized CPU complex128 inputs and declared labels. No Hermitian symmetrization, QR adjustment, clipping, input normalization repair or statevector averaging is performed. The dense dimension limit of four qubits is a teaching-reference guard, rather than a FlagQuantum limit.

```python
assert g.invalid_checks()==10
assert calls==5 and b.RUNS-helper_start==2
public_requests = [name for name in ('povm','instrument') if hasattr(fq,name)]
assert public_requests == []
print('10 malformed contracts rejected; seven actual native body circuits.')
print('Use supported unitary rotations and computational probability requests; book helpers provide effect/branch calculations, not a native instrument endpoint.')
```
```text
10 malformed contracts rejected; seven actual native body circuits.
Use supported unitary rotations and computational probability requests; book helpers provide effect/branch calculations, not a native instrument endpoint.
```

### Complete program and expected output

Run the [complete example](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/generalized_measurements.py):

    python examples/foundations/generalized_measurements.py

It executes 51 native circuits: 42 two-qubit weak-instrument premeasurement/readout cases, seven one-qubit trine input preparations and two joint-system interference readouts. The weak cases cover strengths 0,.35,1, seven basis/complex inputs and both updates. Trine branches are checked classically against an independent scalar formula. Ten invalid contracts and zero/rare/underflow branch boundaries are also checked.

Run the exact body/output checker:

    python scripts/check_generalized_measurements_prose.py

It executes eight cumulative snippets with seven native circuits, then compares the complete program's actual stdout. Numerical tests validate these implementations; the declared generalized measurement postulates and the distinction between their objects are not proved by sampling simulator outputs.

Expected output of the complete program:

```text
42 two-qubit weak-instrument circuits: three strengths including 0/1, seven inputs and two updates with identical meter probabilities passed.
7 native single-qubit preparations: genuine three-outcome trine effects and pure measurement-operator branches checked classically against scalar formulas.
2 native joint-system readouts: one coarse effect I can preserve or destroy later interference; hidden-operator unitary mixing preserves the instrument predictions.
10 malformed contracts rejected; impossible/positive rare/underflow branches distinguished without clipping or vector averaging.
51 actual CPU complex128 circuits; native unitary dilation/readout plus explicitly labelled classical branch analysis, not a dedicated POVM/instrument or sampled-collapse API.
```

### Understanding checks and transfer exercises

**6.5-A — A new weak instrument.** Choose κ=.17 or .73 and a fresh complex input. Run both meter realizations, compare every joint amplitude with $M_a\psi$ or $N_a\psi$, and check that outcome probabilities agree while subsequent predictions can differ. Which operation is coherent control, rather than a classical feedback API?

**6.5-B — New trine inputs.** Prepare Ry(θ) then P(φ) on a fresh qubit. Compare the three scalar probabilities with effect quadratic forms and measurement-operator norms. Can these three labels be a nonzero orthogonal projective family on that qubit alone?

**6.5-C — What does an outcome specify?** If the report says only “kept” for the group {P0,P1}, why is $(P_0+P_1)\psi$ the wrong conditional statevector in general? Are {P0,P1} and {I/√2,Z/√2} different coarse instruments just because their operators differ?

**6.5-D — Which support was demonstrated?** Does native execution of the weak meter circuit prove a general instrument endpoint, a trine dilation, a noise-calibrated measurement or a sampled collapsed state? What does a zero effect mean, and how does it differ from a nonzero component lost to squared-norm underflow?

<details markdown="1">
<summary>Answers and reasoning for 6.5</summary>

**A.** Before readout, the first realization has joint slices $M_a\psi$; the second has $M_0\psi$ and $XM_1\psi$. Unitarity of X preserves their norms. A coherent CX(q1,q0) executes the outcome-controlled system transformation before the meter is measured; no classical feedback endpoint was invoked. The separate author transfer uses two new strengths, three new complex inputs each and both updates, for twelve native circuits.

**B.** With $\alpha=\cos(\theta/2)$ and $\beta=e^{i\phi}\sin(\theta/2)$, use $p_j=|\alpha+e^{-2\pi i j/3}\beta|^2/3$. The effect matrices are complete but not orthogonal projectors. Three nonzero orthogonal projectors cannot fit into a two-dimensional space. Two new native preparations are checked in the transfer, making fourteen transfer circuits total; their trine readout remains a classical prediction.

**C.** The report hides an exclusive fine alternative. Its later probabilities are sums of squared branch amplitudes, rather than the squared amplitude of a vector sum. For input |+⟩, summing P0ψ and P1ψ restores |+⟩ and incorrectly predicts a certain later plus event. The two operator groups are related by a unitary transformation of the hidden index, so they give identical coarse-instrument subsequent predictions.

**D.** Only the declared unitary dilation and exact computational readout were executed. None of the further claims follows. A zero effect gives an impossible outcome for every input; a nonzero effect can also have zero probability on one particular input. Neither case supplies a normalized conditional state there. Numerical underflow instead means the computed nonzero branch cannot be normalized through its represented squared norm; it is reported as a computational failure, not a physical impossibility.

</details>

### Sources, depth and next step

The assigned targets are Nielsen and Chuang, 10th Anniversary Edition (2010), §2.2.3, beginning at printed page 84, and §2.2.6, beginning at printed page 90. These locators are retained without claiming fresh inspection of the user-local textbook PDF. The public author source [Preskill, Caltech Chapter 3, §3.1.2](https://www.preskill.caltech.edu/ph219/chap3_15.pdf), equations (3.23)–(3.31), PDF pages 9–11, was checked for the operator/effect probability and pure-state update setup; its served header says October 2018. Our hidden-branch examples and representation comparison are supplied locally within the declared pure-input scope.

The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/6.5.json) separates author execution from independent mathematical/implementation review and reader trials, which remain pending. Continue, when drafted, with [6.6 From exact probabilities to samples](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-6).


<span id="sec-measurement-expectation-values-and-statistical-estimation-6"></span>

## 6.6 From exact probabilities to samples

**Working draft — author-verified implementation; independent review and reader trial pending.**

Section 6.1 assigns a probability to each outcome. A run with 64 recorded outcomes produces integers, not another exact probability distribution. This section builds the mathematical bridge between those objects and implements it with native FlagQuantum terminal samples. The central result is finite-sample **unbiasedness**: the mean of an estimator over all possible records equals its target. This statement does not say that one record equals the target, or give a confidence interval.

**Entry:** normalized preparations and Born probabilities from 6.1. No density operators, variance formulas or prior statistics course are required. **Assumptions:** a fixed finite set of labels, a fixed preparation/readout protocol, and independently repeated, identically distributed trials (IID). All counts below include every requested trial; no postselection. In a physical experiment, preparation drift, memory and readout errors must be investigated separately. Independent re-preparation is a model assumption, not a conclusion from observing a plausible histogram.

**Notation:** \(\Omega=\{0,\ldots,K-1\}\) is the outcome index set; \(p_j\) its dimensionless probability; \(Y_t\) the index on trial \(t\); \(N\geq1\) the number of trials. A random variable is a numerical function of possible outcomes. Once a record is observed, its entries and computed estimates are ordinary numbers. Probabilities and frequencies have no physical unit; a numerical outcome score can carry a declared unit.
<span id="formula-code-6-6-native"></span>

### 1. Keep the distribution and the record separate


For a binary computational readout of \(R_y(\theta)|0\rangle\), with \(\theta\) in radians,

\[
p_0=\cos^2(\theta/2),\qquad p_1=\sin^2(\theta/2).
\]

A finite probability model assigns \(p_j\geq0\) with \(\sum_jp_j=1\). An event \(A\subseteq\Omega\) has probability \(P(A)=\sum_{j\in A}p_j\). A sample is one label chosen according to this law. The simulator first computes a floating-point representation of the Born distribution and then generates a pseudorandom record. Its ideal probabilities are “exact” in the sense of no shot noise; floating-point error still exists.

**Formula → implementation.** The following actual native call requests both objects from the same circuit. The leading dimension is an execution batch of size one. The sample tensor has shape `(1, N, number_of_selected_qubits)`. We remove the batch axis explicitly. A terminal sampling request is not a mid-circuit measurement/update instruction.

```python
from dataclasses import replace
from math import pi
from fractions import Fraction as F
import torch
import flagquantum as fq
from examples.foundations import exact_samples as s
circuit = fq.Circuit(1, dtype=torch.complex128).ry(0, pi/3)
result = fq.run(circuit,
    outputs=[fq.probabilities(qubits=(0,)), fq.samples(qubits=(0,))],
    shots=64, options=replace(s.OPTIONS, seed=17))
p = result.probabilities[0]
bits = result.samples[0]
assert result.samples.shape == (1,64,1)
torch.testing.assert_close(p, torch.tensor([.75,.25],dtype=torch.float64), atol=1e-12,rtol=0)
print('Native shapes:', tuple(result.probabilities.shape), tuple(result.samples.shape))
print('Born probabilities:', [round(x,12) for x in p.tolist()])
```

```text
Native shapes: (1, 2) (1, 64, 1)
Born probabilities: [0.75, 0.25]
```

<span id="formula-code-6-6-iid"></span>

### 2. Define conditional probability and the IID record law


For events \(A,B\) with \(P(B)>0\), define \(P(A\mid B)=P(A\cap B)/P(B)\). This is classical conditioning on records, independent of any conditional quantum-state rule. In particular,

\[
P(A\cap B)=P(A\mid B)P(B).
\]

Two events are independent when their joint probability is their product. For a sequence of trials the relevant assumption is stronger than pairwise independence: every next-trial conditional law, given any positive-probability prior history, is the same fixed \(p\). Iterating the displayed identity gives

\[
P(Y_1=j_1,\ldots,Y_N=j_N)=\prod_{t=1}^{N}p_{j_t}.
\]

**Proof.** For \(N=1\) this is the declared distribution. If the formula holds for a prefix, multiply its probability by the conditional probability \(p_{j_N}\) of the next outcome. A prefix with zero probability makes every extension zero; no conditional probability on that prefix is needed. This proves the formula by induction. Summing over every record gives \((\sum_jp_j)^N=1\), so it is a normalized law. Qubits *within* one trial can be correlated; independence here concerns separate repeated trials.

The book helper `ensemble` enumerates this law using exact rational arithmetic, not more circuit executions. For two binary trials the probability of the ordered record `(1,0)` is \((1/4)(3/4)=3/16\), and conditioning on the first label being 1 leaves probability \(1/4\) for the second being 1.

```python
rows2 = s.ensemble((F(3,4),F(1,4)), 2)
weights = {seq:w for seq,w,_ in rows2}
first_one = sum(w for seq,w,_ in rows2 if seq[0] == 1)
both_one = weights[(1,1)]
assert weights[(1,0)] == F(3,16)
assert both_one / first_one == F(1,4)
print('Ordered record P(1,0):', weights[(1,0)])
print('P(second=1 | first=1):', both_one/first_one)
```

```text
Ordered record P(1,0): 3/16
P(second=1 | first=1): 1/4
```

<span id="formula-code-6-6-bernoulli"></span>

### 3. Turn one event into an unbiased Bernoulli estimator


For an event \(A\), define an indicator \(I_t=1\) when \(Y_t\in A\), and \(I_t=0\) otherwise. It is a Bernoulli random variable: its probabilities are \(p_A=P(A)\) for 1 and \(1-p_A\) for 0. Define the count and frequency

\[
C_A=\sum_{t=1}^N I_t,\qquad \widehat p_A=C_A/N.
\]

For any finite random variable \(X\), its expectation is the probability-weighted sum \(\mathbb E[X]=\sum_x xP(X=x)\). Equivalently sum the value of its defining function over all elementary outcomes with their probabilities. Thus \(\mathbb E[I_t]=1p_A+0(1-p_A)=p_A\).

**Proof of unbiasedness.** In a finite model, exchange the two finite sums over trials and possible records:

\[
\mathbb E[\widehat p_A]
=\frac1N\sum_{\boldsymbol j}P(\boldsymbol j)
  \sum_{t=1}^N 1_{\{j_t\in A\}}
=\frac1N\sum_{t=1}^N\mathbb E[I_t]
=p_A.
\]

This also proves the linearity of expectation used here, without assuming independent summands. Identical event marginals are enough for unbiasedness; independence is needed for the product record law, and later for the usual variance reduction. The observed frequency below is a realized estimate, not an identity to assert against `p[1]` with a numerical tolerance.

```python
ones = int(bits[:,0].sum().item())
frequency = ones/len(bits)
assert 0 <= ones <= 64 and 0 <= frequency <= 1
print('Observed one count:', ones, 'of', len(bits))
print('Observed frequency:', frequency, '; target:', round(p[1].item(),12))
```

```text
Observed one count: 9 of 64
Observed frequency: 0.140625 ; target: 0.25
```

<span id="formula-code-6-6-categorical"></span>

### 4. Preserve label order when estimating a categorical law


For every label define \(C_j=\sum_t1_{\{Y_t=j\}}\) and \(\widehat p_j=C_j/N\). Exactly one label occurs per trial, so

\[
\sum_j C_j=N,\qquad \sum_j\widehat p_j=1,
\qquad \mathbb E[\widehat p_j]=p_j.
\]

The last equality follows by the indicator proof separately for each label. These frequency components are constrained by their sum; IID trials do not make the label counts independent.

For selected qubits \((q_{a_0},\ldots,q_{a_{k-1}})\), sample columns follow that declared order. The corresponding integer is

\[
j_t=\sum_{\ell=0}^{k-1} b_{t,\ell}2^{k-1-\ell}.
\]

Here \(q_0\) is first in the full computational basis. The actual circuit prepares \(\sqrt3|001\rangle/2+|100\rangle/2\). Requesting `(2,0)` therefore reports `10` with probability \(3/4\), and `01` with probability \(1/4\). This is a selection/reordering of classical output coordinates, not a physical SWAP. `histogram` includes zero-count labels and checks binary integer rows; it does not infer the column order from data.

```python
register = fq.Circuit(3,dtype=torch.complex128).ry(0,pi/3).cx(0,2).x(2)
preg, record, counts, frequencies = s.native(register,(2,0),64,23)
ids, _, _ = s.histogram(record)
assert counts.tolist() == [ids.tolist().count(j) for j in range(4)]
torch.testing.assert_close(preg,torch.tensor([0.,.25,.75,0.],dtype=torch.float64),atol=1e-12,rtol=0)
assert counts[0] == counts[3] == 0 and counts.sum() == 64
print('Labels in column order (q2,q0):', ['00','01','10','11'])
print('Exact probabilities:', [round(x,12) for x in preg.tolist()])
print('Observed counts:', counts.tolist())
```

```text
Labels in column order (q2,q0): ['00', '01', '10', '11']
Exact probabilities: [0.0, 0.25, 0.75, 0.0]
Observed counts: [0, 15, 49, 0]
```

<span id="formula-code-6-6-scores"></span>

### 5. Estimate a declared numerical score without changing labels


Assign each label a fixed real score \(v_j\), known before inspecting the record. Its target mean and estimator are

\[
\mu=\sum_jv_jp_j,\qquad
\widehat\mu=\frac1N\sum_tv_{Y_t}
=\sum_jv_j\widehat p_j.
\]

**Derivation.** In the sum over trials, group together terms with the same observed label: there are \(C_j\) terms with value \(v_j\). Then take the expectation of the final finite sum and insert \(\mathbb E[\widehat p_j]=p_j\), giving \(\mathbb E[\widehat\mu]=\mu\). The proof allows negative scores and scores with a physical unit. A score table is not a quantum observable implementation by itself: it must be attached to the actual declared readout protocol. Here the scores are dimensionless classical diagnostics.

For the preceding four labels choose \((-1,2,-3,4)\); only labels `01` and `10` occur, so \(\mu=2/4-9/4=-7/4\). The code compares two computations of the *same observed* score, while keeping its ideal target separate.

```python
scores = torch.tensor([-1.,2.,-3.,4.],dtype=torch.float64)
observed = (scores @ frequencies).item()
direct = scores[ids].mean().item()
assert abs(observed-direct) < 1e-12
assert abs((scores @ preg).item()+1.75) < 1e-12
print('Observed score by two routes:', observed, direct)
print('Ideal mean score:', round((scores @ preg).item(),12))
```

```text
Observed score by two routes: -1.828125 -1.828125
Ideal mean score: -1.75
```

<span id="formula-code-6-6-ensemble"></span>

### 6. Verify the estimator over the entire finite ensemble


Under the IID law, all ordered records with a specified count vector \((c_0,\ldots,c_{K-1})\) have the same product probability. There are

\[
\frac{N!}{\prod_jc_j!}
\]

such records: choose the positions of label 0, then those of label 1 among the remaining positions, and continue; the factorial denominators cancel to the displayed expression. Therefore

\[
P(C_0=c_0,\ldots,C_{K-1}=c_{K-1})
=\frac{N!}{\prod_jc_j!}\prod_jp_j^{c_j},
\qquad \sum_jc_j=N.
\]

This is the multinomial law. A factor with exponent zero is 1, including when its probability is zero. For \(K=2\), it becomes the binomial count law. It is a law for counts, not for individual ordered records.

Our independent check uses exact fractions and all \(2^4=16\) binary records, avoiding Monte Carlo noise. It verifies the normalization, the weighted frequency mean \(1/4\), the weighted score mean \(-7/4\) for scores \((-3,2)\), and the binomial probability of exactly one `1`. Passing finitely many checks validates this enumerator, not the general proof above. Enumeration is exponential, and the helper rejects more than 4096 records; this is a teaching guard, not a FlagQuantum restriction.

```python
from math import comb
rows4 = s.ensemble((F(3,4),F(1,4)),4)
mean_frequency = sum(w*f[1] for _,w,f in rows4)
mean_score = sum(w*(-3*f[0]+2*f[1]) for _,w,f in rows4)
prob_one = sum(w for seq,w,_ in rows4 if seq.count(1)==1)
assert prob_one == comb(4,1)*F(1,4)*F(3,4)**3
assert mean_frequency == F(1,4) and mean_score == F(-7,4)
print('All',len(rows4),'records: E[frequency] =',mean_frequency,'; E[score] =',mean_score)
print('P(count of ones = 1):', prob_one)
```

```text
All 16 records: E[frequency] = 1/4 ; E[score] = -7/4
P(count of ones = 1): 27/64
```

<span id="formula-code-6-6-failures"></span>

### 7. Separate zero observations, dependence and drift


With \(p_A>0\), an IID record can still contain no occurrences of \(A\): every trial misses it, so

\[
P(C_A=0)=(1-p_A)^N.
\]

Consequently a zero count does not establish zero probability. By contrast, a mathematically zero-probability label never occurs under the ideal model. Numerical probabilities near zero can be unresolved in floating-point simulation; these examples are not rare-event error certificates.

Two different assumption failures deserve separate treatment. First, draw one Bernoulli value \(B\) with parameter \(p\) and duplicate it \(N\) times. Every marginal still has probability \(p\), and \(\widehat p=B\) is unbiased, but it remains either 0 or 1 for any \(N\); the IID count law is false. Second, with trial-dependent event probabilities \(p_t\), linearity gives

\[
\mathbb E[\widehat p]=\frac1N\sum_tp_t.
\]

The estimate targets this average, not a chosen nominal probability. Neither case is repaired by a larger record or a more permissive numerical tolerance. The code uses exact finite counterexamples; no additional circuit or hardware observation is claimed.

```python
rare = F(1,10000)
miss_all = (1-rare)**10
assert miss_all > F(999,1000)
correlated = [((0,)*8,F(3,4)),((1,)*8,F(1,4))]
assert sum(w*F(sum(seq),len(seq)) for seq,w in correlated) == F(1,4)
assert all(sum(seq) in (0,8) for seq,_ in correlated)
drift_mean = (F(1,4)+F(3,4))/2
assert drift_mean == F(1,2) and drift_mean != F(1,4)
print('Rare positive event can be absent in all 10 trials:', miss_all > F(999,1000))
print('Duplicated trials: unbiased but only all-zero/all-one records.')
print('Two-trial drift targets:', drift_mean, '; not nominal 1/4.')
```

```text
Rare positive event can be absent in all 10 trials: True
Duplicated trials: unbiased but only all-zero/all-one records.
Two-trial drift targets: 1/2 ; not nominal 1/4.
```

<span id="formula-code-6-6-contracts"></span>

### 8. Use replay and validation for the right purposes


A seed fixes a pseudorandom stream within a specified implementation. Repeating the same seeded query is useful for debugging and does not add independent statistical evidence. Distinct seeds are not a proof of physical independence, nor must they produce different finite records. Reordering or adding sampling requests may change stream use. Store the protocol, ordered selection, seed, shot count, software versions and complete raw record, not only a rounded frequency.

**Formula → contract.** The denominator \(N\) must be positive; binary records must contain declared integer bits with a known column order. A batch axis cannot silently become a trial or qubit axis. Reject an empty record rather than assign it frequency zero. The book validators also reject Boolean seeds/shot counts, duplicated selections and invalid exact distributions. They do not diagnose hardware IID violations from data. The raw native result retains the pre-readout simulated state; no collapse or conditional update is inferred from the sample record.

```python
first = s.native(register,(2,0),8,101)
replay = s.native(register,(2,0),8,101)
assert torch.equal(first[1],replay[1])
assert s.invalid_checks() == 14
print('Pinned replay identical:', torch.equal(first[1],replay[1]))
print('14 malformed contracts rejected; replay is not a new independent record.')
```

```text
Pinned replay identical: True
14 malformed contracts rejected; replay is not a new independent record.
```

### Complete program, support and verification

Run from the repository root with the pinned example environment:

```sh
python -m pip install -r requirements-examples.txt
python examples/foundations/exact_samples.py
python scripts/check_exact_samples_prose.py
```

The [complete program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/exact_samples.py) checks deterministic basis inputs, analytic single-qubit probabilities, all ordered nonempty three-qubit selections, short records, seed replay and exact rational ensembles. The checker executes the eight cumulative body fragments and compares their outputs, then runs the complete program. Copy the snippets in order; `s` names the original book helper, not a native FlagQuantum module.

Expected output of the complete program:

```text
14 basis circuits: exact labels, ordered sample columns and deterministic counts passed.
12 Bernoulli circuits: analytic Ry probabilities and finite-shot accounting passed; no frequency-equality threshold.
30 ordered-register circuits: all 15 nonempty ordered selections at two seeds; scalar probability and independent count references passed.
10 replay/short-record circuits: pinned-seed replay and 1-8-shot contracts passed; replay is not new statistical evidence.
5 exact rational ensembles: normalized IID laws and all categorical/event/score estimator means passed.
14 malformed contracts rejected before native execution; empty records are not assigned a zero frequency.
66 actual CPU complex128 circuit executions; native terminal samples, not hardware shots or mid-circuit collapse.
Exact-probability atol 1e-12, rtol 0; random frequencies are observations, not exact-probability assertions.
```

| Object | What was actually executed | What is not established |
|---|---|---|
| Born probabilities | Native statevector probability requests, checked against analytic or independently indexed amplitudes | Floating-point values are not interval certificates |
| Terminal bit records | Native `fq.samples`, positive `shots`, seeded CPU execution | Not hardware shots, mid-circuit collapse or feedback |
| Counts and frequencies | Original explicit binary-index/histogram helper | No inference of undeclared qubit or label order |
| Ensemble means | Exhaustive classical exact-fraction enumeration | No additional quantum executions or proof by Monte Carlo |
| Statistical assumptions | IID finite-trial model stated explicitly | Drift/memory absence is not inferred from a seed or histogram |

Tested on FlagQuantum 0.3.1, PyTorch 2.13.0, Python 3.12.14, CPU complex128. Probability/reference comparisons use absolute tolerance \(10^{-12}\), relative tolerance zero. No observed frequency is required to match its target within that tolerance. Seeded example records are regression fixtures of this pinned CPU implementation; across changed versions/backends a different valid record requires revalidation, not a claim of broken quantum physics. We inspect the released terminal sampling path; it samples with replacement from state probabilities and selects output columns in the requested order. This is a mathematical sampling model implemented by a pseudorandom generator, not a proof about physical repeated preparations.

### Understanding checks and transfer tasks

**A. Event versus label.** In a fresh register output with ordered labels `00,01,10,11` and probabilities \((1/10,2/10,3/10,4/10)\), take event “the first selected qubit is 1.” Find its target, a count-based estimator, and its expectation. Does exchanging the two selected columns preserve that target?

**B. New score.** For the same distribution use scores \((2,-1,0,3)\). Find the ideal mean; explain why zero observations of `00` do not justify deleting its score/probability contribution from the ideal target. Verify the estimator mean using exact enumeration of three trials.

**C. Dependence diagnosis.** Someone concatenates a single seeded 64-shot record with itself ten times and reports a 640-shot experiment. Which algebraic frequency identity remains true, and which independence claim fails? Can unbiasedness alone distinguish it from ten new records?

**D. Empty and rare records.** Why is frequency undefined for zero shots, but well-defined and equal to zero when an event is absent from a nonempty record? For \(p_A=1/100\), derive the probability of no occurrences in 3 IID trials.

<details markdown="1">
<summary>Answers and verification routes</summary>

**A.** The event indices are 2 and 3, so its target is \(7/10\), estimate \((C_2+C_3)/N\), and expectation \(7/10\) by summing the two indicator means. Exchanging columns makes the *new first column* refer to the old second qubit; that target is \(p_1+p_3=6/10\). A physical event stays unchanged only if its label predicate is translated too.

**B.** The mean is \(2/10-2/10+12/10=6/5\). An absent label contributes zero to this record's empirical score, but its ideal contribution remains \(2/10\). Call `s.ensemble((F(1,10),F(2,10),F(3,10),F(4,10)),3)` and sum each record's probability times `sum(v*f for v,f in zip((2,-1,0,3),frequencies))`. Exact arithmetic returns \(6/5\), without simulating extra circuits.

**C.** Every count and the denominator are multiplied by ten, so all frequencies and mean scores remain unchanged. The copies are deterministically dependent; the 640-trial product law is unsupported. Across an ensemble of original records the repeated estimator may still be unbiased. Unbiasedness alone cannot establish independence or an uncertainty reduction.

**D.** Division by zero has no defined empirical proportion. With positive \(N\), a zero count divided by \(N\) is a valid observed zero; it does not imply zero target probability. Independence gives \((99/100)^3=970299/1000000\) for missing the event in all three trials.

</details>

### Sources, limitations and next step

The assigned reference is Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010), Appendix 1, “Notes on basic probability theory,” beginning on printed page 608 (`NC:A1`). This section supplies its own finite-sum proofs. For an openly accessible author-written treatment of indicators and their expectation, see Marco Taboga, [Indicator function, definition and Expected value](https://www.statlect.com/fundamentals-of-probability/indicator-functions). The implementation contract was checked against the installed released FlagQuantum sampling source; its backend's [PyTorch multinomial documentation](https://docs.pytorch.org/docs/stable/generated/torch.multinomial.html) describes sampling with replacement and generator control. A seeded record is not evidence of IID hardware outcomes. Variance, covariance, confidence intervals and shot-budget guarantees are deliberately left to 6.7–6.8.

The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/6.6.json) distinguishes author checks from pending independent mathematical/implementation review and reader trials. Continue, when drafted, with [6.7 Variance, covariance, and uncertainty](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-7).


<span id="sec-measurement-expectation-values-and-statistical-estimation-7"></span>

## 6.7 Variance, covariance, and uncertainty

**Working draft — author execution completed; independent mathematical/implementation review and reader trial pending.**

An unbiased estimate can still fluctuate substantially between experiments. A second question is therefore essential: how widely do the possible estimates spread around their target? We now quantify that spread, retaining correlations between quantities measured from the same record. Dropping those correlations can either overstate or understate the uncertainty.

**Entry:** the spectral mean from 6.3 and finite expectations, indicators and IID records from 6.6. All random variables below are real, have finite second moments, and are defined on a declared joint classical probability model. Coefficients and shot counts are fixed before seeing the data. If coefficients carry units, every term in the weighted sum must have the same resulting unit. We explicitly distinguish independence between repeated trials, independence between measurement groups, and correlations within one trial. A finite outcome set with finite scores automatically has finite second moments.

Here **uncertainty** means standard deviation of an outcome or an estimator under that model. A standard deviation is not a confidence interval, a worst-case error bound or a bound on preparation bias. Noncommuting quantum observables do not automatically supply a joint classical record. This section proves the frozen result, variance of a weighted estimator; general uncertainty-relation theorems and optimal measurement allocation are outside this section. Confidence statements begin in 6.8.
<span id="formula-code-6-7-spread"></span>

### 1. Distinguish single-measurement spread from a mean


For a real random variable \(X\) with mean \(\mu=\mathbb E[X]\), define

\[
\operatorname{Var}(X)=\mathbb E[(X-\mu)^2]
=\mathbb E[X^2]-\mu^2,\qquad
\sigma_X=\sqrt{\operatorname{Var}(X)}.
\]

**Derivation.** Expand \((X-\mu)^2=X^2-2\mu X+\mu^2\), take expectations, and use \(\mathbb E[X]=\mu\) and \(\mathbb E[1]=1\). The centered-square definition is nonnegative; \(\sigma_X\) is its nonnegative square root. If \(X\) has unit \(u\), variance has unit \(u^2\) and standard deviation has unit \(u\). Zero variance means that every positive-probability value equals the mean; it does not say that the state or measurement protocol is known without error.

For a Hermitian observable \(A=\sum_j\lambda_jP_j\), its spectral outcome has mean \(\mu_A=\langle\psi|A|\psi\rangle\). Orthogonal projectors imply \(A^2=\sum_j\lambda_j^2P_j\), hence

\[
\sigma_A^2=\langle\psi|A^2|\psi\rangle-\mu_A^2
=\|(A-\mu_AI)|\psi\rangle\|^2.
\]

The second equality follows by expanding the squared norm and using \(A^\dagger=A\). These are two ways to compute the *single spectral measurement* spread. They do not specify how a decomposition of \(A\) will be sampled on hardware.

**Formula → actual native expectation → independent centered-vector calculation.** Prepare \(R_y(\pi/3)\) then \(P(\pi/2)\), with angles in radians, and choose dimensionless \(A=.7X-.4Z\). Since \(X^2=Z^2=I\) and \(XZ+ZX=0\), \(A^2=.65I\). This state has \(\langle X\rangle=0\), \(\langle Z\rangle=1/2\), so \(\mu_A=-.2\) and \(\sigma_A^2=.61\). The variance calculation below is explicit classical postprocessing; no native variance request is invented.

```python
from math import pi,sqrt
from fractions import Fraction as F
import torch
import flagquantum as fq
from examples.foundations import variance_estimators as v
from examples.foundations import observables as o
circuit = fq.Circuit(1,dtype=torch.complex128).ry(0,pi/3).p(0,pi/2)
result = fq.run(circuit,outputs=[fq.expectation(.7*fq.X(0)-.4*fq.Z(0),name='A')],options=v.s.OPTIONS)
psi = result.statevector()[0]
mu = result.expectation('A')[0].item()
centered = (.7*o.X-.4*o.Z-mu*o.I) @ psi
variance_A = torch.vdot(centered,centered).real.item()
assert abs(mu+.2)<1e-12 and abs(variance_A-.61)<1e-12
print('Native mean:',round(mu,12),'; centered single-measurement variance:',round(variance_A,12))
```

```text
Native mean: -0.2 ; centered single-measurement variance: 0.61
```

<span id="formula-code-6-7-weighted"></span>

### 2. Expand every covariance term before deleting any


For jointly defined real variables \(X_i,X_j\), let \(\mu_i=\mathbb E[X_i]\) and define

\[
\Sigma_{ij}=\operatorname{Cov}(X_i,X_j)
=\mathbb E[(X_i-\mu_i)(X_j-\mu_j)]
=\mathbb E[X_iX_j]-\mu_i\mu_j.
\]

Expanding the product gives the last equality. Multiplication of real numbers gives symmetry, \(\Sigma_{ij}=\Sigma_{ji}\), and \(\Sigma_{ii}=\operatorname{Var}(X_i)\). For fixed real weights \(a_i\), center the weighted sum, multiply it out, and exchange finite expectation and sums:

\[
\begin{aligned}
\operatorname{Var}\!\left(\sum_i a_iX_i\right)
&=\mathbb E\!\left[\left(\sum_i a_i(X_i-\mu_i)\right)^2\right]\\
&=\sum_{i,j}a_ia_j\Sigma_{ij}\\
&=\sum_i a_i^2\Sigma_{ii}
+2\sum_{i<j}a_ia_j\Sigma_{ij}
=\boldsymbol a^T\Sigma\boldsymbol a.
\end{aligned}
\]

This proves the central identity. It also proves that a true covariance matrix is positive semidefinite: the quadratic form is a nonnegative variance for every \(\boldsymbol a\). If \(X_i,X_j\) are independent, their finite joint probability factors; summing \(x_ix_jP(x_i)P(x_j)\) separates into \(\mu_i\mu_j\), giving zero covariance. The converse fails: for uniform \(T\in\{-1,0,1\}\), \(T\) and \(T^2\) have zero covariance by symmetry, yet the latter is determined by the former.

The code first makes two identical signs. Their difference is exactly zero, although deleting covariance would predict variance 2. Then it checks the dependent, zero-covariance example. These are classical fixtures to exercise the formula, not simulated hardware data.

```python
prob = torch.tensor([.5,.5],dtype=torch.float64)
signs = torch.tensor([[1.,1.],[-1.,-1.]],dtype=torch.float64)
means, C = v.moments(prob,signs)
a = torch.tensor([1.,-1.],dtype=torch.float64)
assert v.weighted(C,a) == 0.
_, uncorrelated = v.moments(torch.full((3,),1/3,dtype=torch.float64),
    torch.tensor([[-1.,1.],[0.,0.],[1.,1.]],dtype=torch.float64))
assert abs(uncorrelated[0,1].item())<1e-12
print('Identical-sign difference variance:',v.weighted(C,a),'; deleting covariance would give 2.')
print('Covariance(T,T squared):',round(uncorrelated[0,1].item(),12),'; dependence remains.')
```

```text
Identical-sign difference variance: 0.0 ; deleting covariance would give 2.
Covariance(T,T squared): 0.0 ; dependence remains.
```

<span id="formula-code-6-7-means"></span>

### 3. Derive the uncertainty of an IID mean


For \(N\) measurements of the same score, let \(\overline X=N^{-1}\sum_{t=1}^NX_t\). With common variance \(\sigma^2\), the full formula is

\[
\operatorname{Var}(\overline X)
=\frac1{N^2}\sum_{t,u}\operatorname{Cov}(X_t,X_u).
\]

If trials are independent, every off-diagonal covariance is zero. There are \(N\) diagonal terms, each \(\sigma^2\), giving

\[
\operatorname{Var}(\overline X)=\frac{\sigma^2}{N},\qquad
\operatorname{sd}(\overline X)=\frac{\sigma}{\sqrt N}.
\]

The latter quantity is the **standard error** of this estimator under the model. The single-outcome standard deviation \(\sigma\) has not shrunk. Independence without identical distributions instead gives \(N^{-2}\sum_t\sigma_t^2\); the mean target also changes as described in 6.6. Zero cross-covariances suffice for this variance addition, although they do not imply the full IID record law.

If all trials are copies of one random value, every covariance is \(\sigma^2\). There are now \(N^2\) such terms, so averaging leaves variance \(\sigma^2\). A common random offset shared by independent trials similarly leaves an uncertainty floor: if \(X_t=\mu+\epsilon_t+B\), where all zero-mean \(\epsilon_t\) have common variance \(\sigma_\epsilon^2\), are mutually independent, and are independent of the zero-mean \(B\) with variance \(\sigma_B^2\), then direct covariance expansion gives \(\operatorname{Var}(\overline X)=\sigma_\epsilon^2/N+\sigma_B^2\). A deterministic preparation offset is bias, not this variance.

Here exact enumeration of all four-trial Bernoulli records with \(p=1/4\) checks \(\sigma^2=p(1-p)=3/16\) and mean variance \(3/64\). The copied-record comparison has variance \(3/16\).

```python
rows = v.s.ensemble((F(3,4),F(1,4)),4)
iid_variance = sum(w*(f[1]-F(1,4))**2 for _,w,f in rows)
copied_variance = F(3,4)*(0-F(1,4))**2 + F(1,4)*(1-F(1,4))**2
assert iid_variance == F(3,64) and copied_variance == F(3,16)
print('Exact IID mean variance:',iid_variance,'; copied-record mean variance:',copied_variance)
print('Standard error of IID mean:',round(sqrt(float(iid_variance)),12))
```

```text
Exact IID mean variance: 3/64 ; copied-record mean variance: 3/16
Standard error of IID mean: 0.216506350946
```

<span id="formula-code-6-7-categorical"></span>

### 4. Include the negative covariance between frequency components


Let \(I_{t,j}=1_{\{Y_t=j\}}\) for a categorical record. Within one trial,

\[
I_{t,j}I_{t,k}=\delta_{jk}I_{t,j},\qquad
\operatorname{Cov}(I_{t,j},I_{t,k})
=\delta_{jk}p_j-p_jp_k.
\]

Here \(\delta_{jk}\) is 1 when \(j=k\) and zero otherwise. The product identity holds because one trial cannot have two distinct labels. For IID trials, distinct-trial covariance vanishes. Dividing the sum of \(N\) within-trial covariance matrices by \(N^2\) yields

\[
\operatorname{Cov}(\widehat p_j,\widehat p_k)
=\frac{\delta_{jk}p_j-p_jp_k}{N}.
\]

Off-diagonal entries are negative when both labels have positive probability. Row sums are zero because the frequencies sum to exactly one. For a fixed score table \(w_j\), substitute this matrix in the weighted identity:

\[
\operatorname{Var}\!\left(\sum_jw_j\widehat p_j\right)
=\frac{\sum_jp_jw_j^2-(\sum_jp_jw_j)^2}{N}.
\]

Thus covariance between frequency components is necessary even for independent trials. The actual three-qubit circuit below reports `(q2,q0)` in order `00,01,10,11`, with probabilities \((0,1/4,3/4,0)\). A one-hot row is the vector of indicators for a single categorical outcome. Our helper computes its covariance by centered sums, then compares it with the derived formula. The native random record is retained separately; no frequency-to-target tolerance assertion is used.

```python
p, bits, counts, frequencies = v.native(v.s.register(),(2,0),16,31)
_, single_covariance = v.moments(p,torch.eye(4,dtype=torch.float64))
frequency_covariance = single_covariance/16
torch.testing.assert_close(frequency_covariance,(torch.diag(p)-torch.outer(p,p))/16,atol=1e-12,rtol=0)
assert abs(frequency_covariance[1,2].item()+3/256)<1e-12
assert torch.max(torch.abs(frequency_covariance.sum(dim=1))).item()<1e-12
print('Exact Cov(frequency 01,frequency 10):',round(frequency_covariance[1,2].item(),12))
print('Observed counts in declared order:',counts.tolist())
```

```text
Exact Cov(frequency 01,frequency 10): -0.01171875
Observed counts in declared order: [0, 3, 13, 0]
```

<span id="formula-code-6-7-joint"></span>

### 5. Retain correlations inside one compatible readout group


A single computational readout of two qubits supplies jointly defined scores \(Z_0=(-1)^{b_0}\) and \(Z_1=(-1)^{b_1}\). Preparing

\[
|\psi_\theta\rangle=
\cos(\theta/2)|00\rangle+\sin(\theta/2)|11\rangle
\]

gives \(\mathbb E[Z_0]=\mathbb E[Z_1]=\cos\theta\) and \(\mathbb E[Z_0Z_1]=1\). Therefore their variances and covariance all equal \(\sin^2\theta\). Flipping qubit 1 changes the latter score's sign; its variance remains \(\sin^2\theta\), and covariance becomes \(-\sin^2\theta\).

For the within-shot score \(W=aZ_0+bZ_1\), substitution gives

\[
\operatorname{Var}(W)=(a\pm b)^2\sin^2\theta,
\qquad \operatorname{Var}(\overline W)=\frac{\operatorname{Var}(W)}N,
\]

where the plus sign is the unflipped circuit and the minus sign is the flipped circuit. At \(\theta=\pi/2\), \(a=.7,b=-1.2\), the single-shot variances are .25 and 3.61. Discarding covariance would give 1.93 for both. This is not a rule that grouping always helps: the sign of the covariance and of the weights matters.

Below both circuits actually run. Exact moments come from native probabilities and the explicit joint score table; the observed records are used later for a separate estimate of their covariance.

```python
values = torch.tensor([[1.,1.],[1.,-1.],[-1.,1.],[-1.,-1.]],dtype=torch.float64)
coeff = torch.tensor([.7,-1.2],dtype=torch.float64)
exact_variances = []
for flipped in (False,True):
    pj, pair_bits, _, _ = v.joint(pi/2,flipped,31,7)
    mean_pair, cov_pair = v.moments(pj,values)
    exact_variances.append(v.weighted(cov_pair,coeff))
assert abs(exact_variances[0]-.25)<1e-12 and abs(exact_variances[1]-3.61)<1e-12
print('Single-shot weighted variances, same/opposite signs:',[round(x,12) for x in exact_variances])
print('Ignoring covariance would give:',round(.7**2+1.2**2,12))
```

```text
Single-shot weighted variances, same/opposite signs: [0.25, 3.61]
Ignoring covariance would give: 1.93
```

<span id="formula-code-6-7-groups"></span>

### 6. Add variances only after declaring independent groups


Let group \(g\) produce IID score samples \(W_{g,t}\) with single-shot variance \(\sigma_g^2\) and mean \(\mu_g\). Group \(g\) has \(N_g\geq1\) trials. For fixed weights \(a_g\), the estimator is \(\widehat E=\sum_ga_g\overline W_g\), with target \(\sum_ga_g\mu_g\). The full covariance identity gives

\[
\operatorname{Var}(\widehat E)
=\sum_g\frac{a_g^2\sigma_g^2}{N_g}
+2\sum_{g<h}a_ga_h\operatorname{Cov}(\overline W_g,\overline W_h).
\]

**Proof of the independent-group simplification.** Every group mean is a function of that group's complete record. If the joint probability of all group records factors, a finite sum of a product of their two mean functions factors into their separate expectations. Hence all cross-group covariances are zero, and only the first sum remains. Independence within groups is used for \(\sigma_g^2/N_g\); independence between groups is a separate assumption. Different seeds or separate API calls do not prove either assumption on hardware. If settings share data or a random calibration offset, retain the cross terms.

For \(A=aX+bZ\), use separate X and Z readouts of \(R_y(\theta)\) followed by \(P(\phi)\). The X group appends H before computational readout. Define

\[
x=\sin\theta\cos\phi,\quad z=\cos\theta,\qquad
V_{\mathrm{groups}}=\frac{a^2(1-x^2)}{N_X}
+\frac{b^2(1-z^2)}{N_Z}.
\]

Both scores take values \(\pm1\), so their variances are \(1-x^2\) and \(1-z^2\). These quantities are measured in separate experimental groups; no joint classical product of X and Z is assigned. By contrast, the variance of a *single spectral measurement of A* is \(a^2+b^2-(ax+bz)^2\), since \(XZ+ZX=0\). Dividing that variance by a shot count describes repeated spectral measurements of A, not this two-setting procedure. The following code executes the two native readouts and calculates the variance of their declared independent-group estimator. All coefficients and scores here are dimensionless.

```python
theta,phi = pi/3,pi/4
variances, means, observed_means = [], [], []
for setting,N,seed in [('X',32,19),('Z',64,41)]:
    c = fq.Circuit(1,dtype=torch.complex128).ry(0,theta).p(0,phi)
    if setting == 'X': c.h(0)
    pg, bg, _, _ = v.native(c,(0,),N,seed)
    mg,Cg = v.moments(pg,torch.tensor([[1.],[-1.]],dtype=torch.float64))
    means.append(mg.item()); variances.append(Cg.item())
    observed_means.append((1.-2.*bg.to(torch.float64)).mean().item())
variance_estimator = v.independent_groups(tuple(variances),(.7,-.4),(32,64))
assert abs(variance_estimator-.0114453125)<1e-12
print('Independent-group estimator variance:',round(variance_estimator,12))
print('Its standard error:',round(sqrt(variance_estimator),12))
print('Observed weighted mean:',round(.7*observed_means[0]-.4*observed_means[1],12))
```

```text
Independent-group estimator variance: 0.0114453125
Its standard error: 0.106982767304
Observed weighted mean: 0.0875
```

<span id="formula-code-6-7-estimated"></span>

### 7. Estimate covariance from a finite record without claiming certainty


Usually the exact \(\sigma_g^2\) or within-group covariance is unknown. For \(N\geq2\) IID joint observations \(\boldsymbol X_t\), define

\[
\widehat\Sigma=\frac1{N-1}\sum_{t=1}^N
(\boldsymbol X_t-\overline{\boldsymbol X})
(\boldsymbol X_t-\overline{\boldsymbol X})^T.
\]

**Proof of unbiasedness.** Set \(\boldsymbol U_t=\boldsymbol X_t-\boldsymbol\mu\) and \(\overline{\boldsymbol U}=\overline{\boldsymbol X}-\boldsymbol\mu\). Expanding the centered outer products and using \(\sum_t\boldsymbol U_t=N\overline{\boldsymbol U}\) gives the exact record identity

\[
\sum_t(\boldsymbol X_t-\overline{\boldsymbol X})
(\boldsymbol X_t-\overline{\boldsymbol X})^T
=\sum_t\boldsymbol U_t\boldsymbol U_t^T
-N\overline{\boldsymbol U}\,\overline{\boldsymbol U}^{T}.
\]

The first sum has expectation \(N\Sigma\). For the second, expand \(\overline{\boldsymbol U}\overline{\boldsymbol U}^T=N^{-2}\sum_{t,u}\boldsymbol U_t\boldsymbol U_u^T\): independence and zero means remove the \(t\ne u\) terms, leaving expectation \(\Sigma/N\). Thus the entire right-hand side has expectation \((N-1)\Sigma\), proving \(\mathbb E[\widehat\Sigma]=\Sigma\).

Consequently \(\boldsymbol a^T\widehat\Sigma\boldsymbol a/N\) is an unbiased estimate of the variance of the IID weighted mean. It is still random. Its square root is a reported **estimated standard error**; the nonlinear square root does not preserve unbiasedness. The finite record identity below compares two computations of the same observed quantity, not a comparison of random estimates to their exact population targets. We use centered products to reduce cancellation from large common offsets.

```python
joint_scores = 1.-2.*pair_bits.to(torch.float64)
estimated_cov = v.sample_covariance(joint_scores)
observed_var = v.weighted(estimated_cov,coeff)
score_column = (joint_scores @ coeff)[:,None]
assert abs(observed_var-v.sample_covariance(score_column).item())<1e-12
estimated_variance_of_mean = observed_var/len(pair_bits)
print('Observed score sample variance:',round(observed_var,12))
print('Estimated variance of its mean:',round(estimated_variance_of_mean,12))
print('Estimated standard error:',round(sqrt(estimated_variance_of_mean),12))
```

```text
Observed score sample variance: 3.540129032258
Estimated variance of its mean: 0.114197710718
Estimated standard error: 0.337931517793
```

<span id="formula-code-6-7-boundaries"></span>

### 8. Keep numerical checks and uncertainty claims separate


The helpers reject nonfinite tables, invalid probabilities, wrong dimensions, asymmetric or materially indefinite covariance matrices, and invalid shot counts. The sample covariance requires at least two trials. `independent_groups` implements a formula under an explicit independence model; it cannot inspect numeric variances and determine whether the original groups shared data. Inputs with integer/float32 tensors are rejected rather than silently weakening the declared float64 reference calculation.

A finite record can have zero sample variance when the true variance is positive. For a Bernoulli outcome with \(p=1/100\), the true variance is \(99/10000\), but an all-zero record gives sample variance zero and an estimated standard error of zero. Under IID sampling this record has positive probability \((99/100)^N\). A zero estimate is not a confidence certificate.

The subtraction \(\mathbb E[X^2]-\mu^2\) is useful algebraically but can lose all significant digits for a large mean and small spread. The centered calculation below retains variance \(1/4\) for equiprobable values \(10^8\) and \(10^8+1\). This is not an arbitrary-precision or interval guarantee. The weighted covariance helper refuses a negative computed variance instead of clipping it to zero; near-null numerical cases may require a more accurate reference. Values lost to floating-point representation cannot be restored by centering.

```python
_, shifted_cov = v.moments(torch.tensor([.5,.5],dtype=torch.float64),
    torch.tensor([[1e8],[1e8+1]],dtype=torch.float64))
assert shifted_cov.item() == .25
zero_record = torch.zeros((5,1),dtype=torch.float64)
assert v.sample_covariance(zero_record).item() == 0.
assert F(1,100)*(1-F(1,100)) == F(99,10000)
assert v.invalid_checks() == 14
print('Centered large-offset variance:',shifted_cov.item())
print('All-zero fixture sample variance: 0; true Bernoulli variance may be 99/10000.')
print('14 malformed contracts rejected; no clipping or confidence-interval inference.')
```

```text
Centered large-offset variance: 0.25
All-zero fixture sample variance: 0; true Bernoulli variance may be 99/10000.
14 malformed contracts rejected; no clipping or confidence-interval inference.
```

### Complete program and independent verification

Run from the repository root in the pinned example environment:

```sh
python examples/foundations/variance_estimators.py
python scripts/check_variance_estimators_prose.py
```

The [complete program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/variance_estimators.py) executes 56 CPU complex128 circuits: 12 native expectation queries with independent spectral/centered-vector/analytic references; 20 correlated or anticorrelated pair readouts; 12 ordered categorical readouts; and 12 separate X/Z readouts. Four exact rational ensemble families independently check categorical covariance, the expectation of sample variance, the variance of a mean and independent-group addition. Exact enumeration is classical verification and is counted separately from circuit execution. No independent external reviewer or reader trial is claimed.

Expected output of the complete program:

```text
12 native expectation circuits: spectral, centered-vector and analytic quantum variances agree.
20 joint Z-readout circuits: positive/negative within-shot covariance and weighted sample-variance identities passed.
12 categorical circuits: exact one-hot covariance and observed weighted-score identities passed with ordered labels.
12 separate X/Z readout circuits: analytic group means and single-shot variances passed; cross-group independence is a declared model.
4 exact rational ensemble families: categorical covariance, unbiased sample variance, variance/N and independent-group addition passed.
14 malformed contracts rejected; centered large-offset variance .25 retained; a zero observed variance is not a zero-population certificate.
56 actual CPU complex128 circuit executions; probability/reference atol 1e-12, rtol 0; no confidence-interval or hardware-independence claim.
```

The eight body snippets are cumulative; `v` names original book helpers, not a native FlagQuantum variance module. The body checker executes those snippets and compares their stdout, then runs the complete program. Tested versions: FlagQuantum 0.3.1, PyTorch 2.13.0, Python 3.12.14; CPU complex128 state evolution and float64 classical statistics. Probability and deterministic formula comparisons use absolute tolerance \(10^{-12}\), relative tolerance zero. Observed variances, frequencies and estimated errors are not required to equal their population targets within that tolerance. Sample-output fixtures depend on the pinned CPU sampling implementation.

Native operations used here are unitary preparation/analyzers, exact Pauli expectation and computational probabilities, and terminal bit samples. All covariance matrices, sample variances and error calculations are explicit classical postprocessors. Joint Z scores are defined on the same observed record; separate X/Z group independence is an assumption of the stated experiment. No native uncertainty endpoint, sampled collapse, noise calibration or hardware-independence guarantee is asserted. The inherited small-system and exact-enumeration guards belong to the teaching references. Optimal shot allocation, data-adaptive coefficients, postselection and general uncertainty-relation theorems are not derived here.

### Understanding checks and transfer tasks

**A. Signs and covariance.** An ideal Bell pair has \(Z_0=Z_1\), each with variance 1. Find the single-shot variance of \(W=2Z_0-Z_1\), then the variance of its mean over 25 IID joint readouts. Repeat when \(Z_1=-Z_0\). What would deleting covariance predict?

**B. Independent groups.** Two independent groups have single-shot variances \(3/4\) and \(1/2\), use 12 and 8 shots, and enter the estimator with coefficients 2 and −1. Find the estimator variance and standard error. Which additional term is necessary if the group means have covariance \(1/100\)?

**C. New exact categorical model.** Use probabilities \((1/10,2/10,3/10,4/10)\), scores \((2,-1,0,3)\) and three IID trials. Compute the population score variance and the variance of its mean. Check both by exact enumeration, including the expectation of the unbiased sample variance. Then repeat with the new probabilities of a native four-qubit ordered partial readout and an explicit score table; do not claim exact rational arithmetic for floating-point circuit probabilities.

**D. What does an error bar establish?** A five-shot all-zero Bernoulli record gives sample variance zero. Does that establish an exact probability, a confidence interval, a systematic-error bound or zero quantum spread? Why does increasing the number of copied records fail to help?

<details markdown="1">
<summary>Answers and variance checks for 6.7</summary>

**A.** With equal signs, covariance is 1 and the weighted variance is \(4+1-4=1\); mean variance is \(1/25\). With opposite signs covariance is −1, giving \(4+1+4=9\) and \(9/25\). Deleting covariance gives single-shot variance 5 and mean variance \(1/5\) in both cases, missing the actual effect of the sign.

**B.** The variance is \(4(3/4)/12+(1/2)/8=5/16\), and standard error is \(\sqrt5/4\). A group-mean covariance \(1/100\) adds \(2(2)(-1)/100=-1/25\), so the corrected variance is \(109/400\). This covariance is between means, so it is not divided by the group shot counts again.

**C.** The mean is \(6/5\), second moment \(21/5\), and variance \(21/5-36/25=69/25\); mean variance is \(23/25\). Call `v.s.ensemble((F(1,10),F(2,10),F(3,10),F(4,10)),3)`, then compute each record's score mean and sample variance with denominator 2. Probability-weighted sums give variance of the mean \(23/25\) and expected sample variance \(69/25\). For a new native circuit, compare `v.moments(p,score_table)` with explicit label sums, and compare the observed score sample variance with the weighted sample covariance computed from the same rows. These are distinct comparisons.

**D.** None follows. The record gives one random variance estimate. A positive event probability can produce that record with positive probability; no model bias or physical calibration has been bounded. Copying a record preserves the observed mean and creates deterministically dependent copies. The IID covariance cancellation is unavailable. A confidence method must specify its model and coverage, rather than treat the estimated standard error as a certificate.

</details>

### Sources and next step

The assigned reference is Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010), Appendix 1, “Notes on basic probability theory,” beginning on printed page 608 (`NC:A1`). The local proofs above supply the full finite covariance and weighted-estimator argument. An openly accessible author-written companion is Marco Taboga, [Covariance: definition, bilinearity, and variance of a sum](https://www.statlect.com/fundamentals-of-probability/covariance). Section 6.3 supplies the finite Hermitian spectral expectation identity used for quantum outcome variance. No fresh inspection of the user-local textbook PDF is claimed.

See the [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/6.7.json) for separate author, independent-review and reader statuses. Continue, when drafted, with [6.8 Confidence intervals and shot budgets](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-8).


<span id="sec-measurement-expectation-values-and-statistical-estimation-8"></span>

## 6.8 Confidence intervals and shot budgets

**Working draft — author execution completed; independent mathematical/implementation review and reader trial pending.**

A small estimated standard error does not, by itself, promise that an interval contains the target. This section turns a *proved population variance bound* into a finite-shot coverage guarantee. We prove Markov's inequality, derive Chebyshev's inequality, solve the resulting integer shot-budget inequality, and compare that conservative guarantee with exact binomial coverage. Each guarantee names its probability model and fixed design.

**Entry:** 6.7, including unbiased means, covariance and independent-group variance. Let \(\mu\) be the fixed unknown mean, \(\widehat\mu\) its random unbiased estimate, \(\epsilon>0\) the requested absolute error, and \(0<\delta<1\) the allowed failure probability. The mean and \(\epsilon\) have the same unit; variance has that unit squared; \(\delta\) and shot counts are dimensionless. Choose the measurement, coefficients, trial count and error/failure targets before seeing outcomes. IID means identically prepared independent trials under the declared ideal model; a simulator seed does not establish those conditions on hardware.

The examples compute ideal computational probabilities and native pseudorandom terminal samples. Mathematical coverage refers to the ideal repeated-trial model. Floating-point agreement of a simulator with that model is separately checked, and does not bound physical preparation or readout bias.
<span id="formula-code-6-8-coverage"></span>

### 1. Define a random interval and its coverage


For a fixed half-width \(\epsilon\), define the random closed interval

\[
I(\text{record})=[\widehat\mu-\epsilon,\widehat\mu+\epsilon].
\]

Its coverage at a fixed true parameter is

\[
P_\mu\{\mu\in I(\text{record})\}
=P_\mu\{|\widehat\mu-\mu|\leq\epsilon\}.
\]

The probability averages over possible records generated at that same fixed \(\mu\). After observing one record, its interval endpoints are fixed: the coverage statement does not assign a posterior probability to the fixed unknown parameter. A guaranteed level \(1-\delta\) means the coverage is at least that level for every model/parameter included in the guarantee. One realized interval can miss without contradicting the guarantee.

Here native \(R_y(\pi/3)\) prepares an event with ideal probability \(p=1/4\). We record 20 trials and form an interval of half-width \(1/4\). Unit 4 will justify at least 80% coverage uniformly in an unknown Bernoulli probability for this fixed design. The exact rational count ratio below describes this observed record; its correctness is distinct from a confidence guarantee. Angles are in radians.

```python
from fractions import Fraction as F
from math import pi
import torch
import flagquantum as fq
from examples.foundations import confidence_shots as c
from dataclasses import replace
result = fq.run(fq.Circuit(1,dtype=torch.complex128).ry(0,pi/3),
    outputs=[fq.probabilities(qubits=(0,)),fq.samples(qubits=(0,))],
    shots=20,options=replace(c.s.OPTIONS,seed=41))
record = result.samples[0]
assert record.shape == (20,1)
assert abs(result.probabilities[0,1].item()-.25)<1e-12
estimate = F(int(record[:,0].sum().item()),20)
interval = (estimate-F(1,4),estimate+F(1,4))
print('Observed probability estimate:',estimate)
print('Observed closed interval:',*[str(x) for x in interval])
```

```text
Observed probability estimate: 3/20
Observed closed interval: -1/10 2/5
```

<span id="formula-code-6-8-markov"></span>

### 2. Prove Markov by comparing each outcome with an indicator


Let \(Z\geq0\) have finite mean and let \(t>0\). For every elementary outcome,

\[
Z\geq t\,1_{\{Z\geq t\}}.
\]

**Proof.** On the event \(Z\geq t\), the right side is \(t\), which is no larger than \(Z\). Off that event the right side is zero, which is no larger than nonnegative \(Z\). Taking expectations preserves this pointwise inequality: in a finite model it is just a sum with nonnegative probability weights. Since the indicator's mean is its event probability,

\[
\mathbb E[Z]\geq tP(Z\geq t),\qquad
P(Z\geq t)\leq\frac{\mathbb E[Z]}t.
\]

This is Markov's inequality. Independence is not needed. A bound exceeding 1 is valid but uninformative; probability is also at most 1. Nonnegativity and a positive threshold are essential to this proof.

The code independently sums a finite law with probabilities \((1/2,1/4,1/4)\), values \((0,1,3)\), and threshold 2. It is a classical reference, with no extra circuit execution.

```python
probabilities = (F(1,2),F(1,4),F(1,4))
values = (F(0),F(1),F(3))
threshold = F(2)
expectation = sum(p*z for p,z in zip(probabilities,values))
tail = sum(p for p,z in zip(probabilities,values) if z>=threshold)
assert tail <= expectation/threshold
print('Exact P(Z >= 2):',tail,'; Markov upper bound:',expectation/threshold)
```

```text
Exact P(Z >= 2): 1/4 ; Markov upper bound: 1/2
```

<span id="formula-code-6-8-chebyshev"></span>

### 3. Apply Markov to the squared estimation error


For a real random variable \(T\) of mean \(m\) and finite variance, set \(Z=(T-m)^2\) and \(t=\epsilon^2\). Squaring a real deviation is nonnegative, and \(\epsilon>0\) gives

\[
\{|T-m|\geq\epsilon\}
=\{(T-m)^2\geq\epsilon^2\}.
\]

Markov therefore yields **Chebyshev's inequality**:

\[
P(|T-m|\geq\epsilon)
\leq\frac{\operatorname{Var}(T)}{\epsilon^2}.
\]

This inequality itself does not require independent trials. Independence enters when we use 6.7 to calculate an estimator's variance. For an unbiased IID score mean with single-trial variance at most a known \(v\geq0\),

\[
P(|\widehat\mu-\mu|\geq\epsilon)
\leq\frac{v}{N\epsilon^2}.
\]

It follows that \(P(|\widehat\mu-\mu|<\epsilon)\geq1-v/(N\epsilon^2)\). Our closed interval also includes equality, so it has at least this coverage. For an exact discrete comparison we must retain the chosen endpoint convention: the complement of the closed interval is the **strict** event \(|\widehat\mu-\mu|>\epsilon\), whereas the displayed Chebyshev tail includes equality. The bound is still conservative for the closed interval.

The finite check below enumerates four Bernoulli trials with \(p=1/4\). Their sample mean has variance \(3/64\); at \(\epsilon=1/2\) the non-strict tail is \(13/256\), below the bound \(3/16\).

```python
rows = c.s.ensemble((F(3,4),F(1,4)),4)
variance_mean = sum(w*(f[1]-F(1,4))**2 for _,w,f in rows)
tail = sum(w for _,w,f in rows if abs(f[1]-F(1,4))>=F(1,2))
assert variance_mean == F(3,64) and tail == F(13,256)
assert tail <= variance_mean/F(1,2)**2
print('Exact non-strict tail:',tail,'; Chebyshev upper bound:',variance_mean/F(1,2)**2)
```

```text
Exact non-strict tail: 13/256 ; Chebyshev upper bound: 3/16
```

<span id="formula-code-6-8-budget"></span>

### 4. Derive a usable variance bound and round the shot count upward


To make the preceding failure bound no larger than \(\delta\), solve

\[
\frac{v}{N\epsilon^2}\leq\delta
\quad\Longleftrightarrow\quad
N\geq\frac{v}{\delta\epsilon^2}.
\]

For a positive integer trial count the sufficient design is

\[
N_{\mathrm{safe}}=
\max\!\left\{1,\left\lceil\frac{v}{\delta\epsilon^2}\right\rceil\right\}.
\]

The ceiling is necessary: for \(v=1/4,\epsilon=1/5,\delta=1/10\), the ratio is 62.5, so use 63 trials. A zero certified population variance still requires one observation in this implementation. “Safe” means sufficient under the stated model, not minimal among all possible methods. A smaller N may also have adequate actual coverage.

How can \(v\) be known without knowing \(\mu\)? Suppose the score always lies in a **declared** interval \([L,U]\). Then \((X-L)(U-X)\geq0\). Expand and take expectations to obtain

\[
\begin{aligned}
\mathbb E[X^2]&\leq(L+U)\mu-LU,\\
\operatorname{Var}(X)&\leq(U-\mu)(\mu-L)\\
&=\frac{(U-L)^2}{4}
-\left(\mu-\frac{L+U}{2}\right)^2\\
&\leq\frac{(U-L)^2}{4}.
\end{aligned}
\]

Here \(\mu\in[L,U]\) because it is a weighted average of scores in that range. This proves a distribution-free variance bound within the bounded-score model. An event indicator in \([0,1]\) has \(v=1/4\); a Pauli score in \([-1,1]\) has \(v=1\). With \(\epsilon=.1,\delta=.05\), their conservative budgets are 500 and 2000. Their different units/scales matter. The range must include every possible outcome, not merely the minimum and maximum observed so far.

`budget` uses exact Fraction design inputs and integer ceiling arithmetic. It cannot determine from a number alone whether the caller has proved it is a population variance bound.

```python
epsilon,delta = F(1,10),F(1,20)
bernoulli_v = c.range_variance(F(0),F(1))
pauli_v = c.range_variance(F(-1),F(1))
assert c.budget(bernoulli_v,epsilon,delta)==500
assert c.budget(pauli_v,epsilon,delta)==2000
assert c.budget(F(1,4),F(1,5),F(1,10))==63
print('95% fixed-design budgets at absolute error .1: event',c.budget(bernoulli_v,epsilon,delta),'; Pauli',c.budget(pauli_v,epsilon,delta))
print('Noninteger ratio62.5 rounds upward to:',c.budget(F(1,4),F(1,5),F(1,10)))
```

```text
95% fixed-design budgets at absolute error .1: event 500 ; Pauli 2000
Noninteger ratio62.5 rounds upward to: 63
```

<span id="formula-code-6-8-binomial"></span>

### 5. Compare the bound with exact binomial coverage at a fixed parameter


For IID Bernoulli trials, 6.6 gives the binomial count law. The exact coverage of the closed fixed-half-width interval at a specified true \(p\) is

\[
C_N(p;\epsilon)=
\sum_{\substack{0\leq k\leq N\\|k/N-p|\leq\epsilon}}
\binom Nk p^k(1-p)^{N-k}.
\]

**Derivation.** The sample mean is \(k/N\) precisely when the count is \(k\). Distinct counts are disjoint events. Add their binomial probabilities exactly when their intervals contain the fixed \(p\). Factors with exponent zero are 1, including at \(p=0\) or 1. This finite sum is an actual coverage calculation for that model and parameter, not an upper bound from moments and not a posterior over \(p\).

The included integer endpoints change as N changes. Coverage for this fixed-width rule need not increase at every increment of N. At \(p=.1,\epsilon=.1\), the closed rule includes counts 0 and 1 for both N=5 and N=6, but their binomial masses differ: coverage drops from .91854 to .885735. The exact Fraction comparison avoids silently changing equality through floating-point rounding.

The conservative N=500 guarantee applies to **every** Bernoulli probability under the IID model, by the proof in unit 4. Checking its exact coverage at six rational parameters is a useful implementation test, not a substitute for that uniform proof. Evaluating coverage at an observed frequency used as if it were the unknown true p does not certify the procedure's coverage. Exact inversion methods for a count-dependent interval are a different construction and are not derived here.

```python
p_fixed = F(1,10)
c5 = c.coverage(p_fixed,5,F(1,10))
c6 = c.coverage(p_fixed,6,F(1,10))
c500 = c.coverage(p_fixed,500,F(1,10))
assert c5==F(45927,50000) and c6==F(177147,200000) and c6<c5
assert c500>=F(19,20)
print('Exact closed-rule coverage, N5 and N6:',float(c5),float(c6))
print('Exact N500 coverage is at least95%:',c500>=F(19,20))
```

```text
Exact closed-rule coverage, N5 and N6: 0.91854 0.885735
Exact N500 coverage is at least95%: True
```

<span id="formula-code-6-8-plugin"></span>

### 6. Reject the unsupported sample-variance substitution


The proof in unit 3 needs a nonrandom upper bound on the population variance (or a separately justified valid bound). It does not permit replacing that bound by the observed unbiased sample variance just because its expectation is correct. The resulting random threshold changes the event being bounded.

For Bernoulli observations with count k and N≥2, the observed unbiased sample variance is \(S^2=N\widehat p(1-\widehat p)/(N-1)\). A tempting but unsupported interval uses half-width

\[
h_{\mathrm{plug}}=
\sqrt{\frac{S^2}{N\delta}}
=\sqrt{\frac{\widehat p(1-\widehat p)}{(N-1)\delta}}.
\]

At \(p=.1,N=5,\delta=.05\), an all-zero record produces \(S^2=0\), interval \([0,0]\), and a miss. That event alone has probability \(.9^5=.59049\), already much larger than .05. The all-one record also misses; the intermediate counts cover. Exact enumeration therefore gives coverage \(1-.9^5-.1^5=.4095\), not 95%.

The diagnostic `plugin_coverage` deliberately evaluates this **invalid proposed method**; it is not an exported valid confidence-interval constructor. It compares squared distances with the squared random radius using rational arithmetic, so the counterexample is not a square-root rounding artifact. Other data-dependent intervals can be valid when supplied with their own coverage proof; this counterexample rejects this substitution, not all uses of data-dependent widths.

```python
bad_coverage = c.plugin_coverage(F(1,10),5,F(1,20))
miss_all_zero = F(9,10)**5
assert miss_all_zero>F(1,20)
assert bad_coverage==F(819,2000)
print('All-zero miss probability:',float(miss_all_zero))
print('Unsupported nominal95% plug-in rule actual coverage:',float(bad_coverage))
```

```text
All-zero miss probability: 0.59049
Unsupported nominal95% plug-in rule actual coverage: 0.4095
```

<span id="formula-code-6-8-simultaneous"></span>

### 7. Budget a simultaneous histogram statement without assuming independent labels


If K frequency intervals are each individually valid with failure probabilities \(\delta_j\), let \(F_j\) denote their miss events. Pointwise,

\[
1_{\bigcup_jF_j}\leq\sum_j1_{F_j}.
\]

Taking expectations proves the union bound \(P(\bigcup_jF_j)\leq\sum_jP(F_j)\leq\sum_j\delta_j\). No independence between these events is needed. Choose \(\delta_j=\delta/K\); applying the Bernoulli-indicator variance bound to every label gives the sufficient common record length

\[
N\geq\frac{K}{4\delta\epsilon^2}.
\]

Then all K closed frequency intervals simultaneously cover with probability at least \(1-\delta\). This is more demanding than a per-label guarantee, and is often conservative. The negative covariance of categorical frequencies from 6.7 does not invalidate the union bound. Trials still obey the required repeated-preparation model. The declared K and predicates are fixed before seeing the record, including labels with zero observed counts.

The native three-qubit preparation below requests the ordered selection `(2,0)`, making K=4 labels. With \(\epsilon=1/4,\delta=1/5\), the simultaneous budget is 80 shared trials, not four independent 80-trial experiments. The code verifies counting and the deterministic design inequality; it does not demand that this one observed histogram prove a coverage statement.

```python
K = 4
N = c.budget(F(1,4),F(1,4),F(1,5)/K)
assert N==80 and K*F(1,4)/(N*F(1,4)**2)<=F(1,5)
pg,bg,cg,fg = c.native(c.s.register(),(2,0),N,29)
assert cg.sum()==80 and len(pg)==K
print('Simultaneous four-label budget:',N,'shared trials')
print('Observed counts in q2,q0 order:',cg.tolist())
```

```text
Simultaneous four-label budget: 80 shared trials
Observed counts in q2,q0 order: [0, 18, 62, 0]
```

<span id="formula-code-6-8-weighted"></span>

### 8. Preserve the declared estimator and fixed stopping rule


Chebyshev applies to any unbiased estimator once its variance is bounded; it does not require that the estimator itself be a single raw measurement outcome. For independent X and Z readout groups estimating \(E=.7\langle X\rangle-.4\langle Z\rangle\), use 6.7. If each group has N independent trials and the groups are independent, both ±1 score variances are at most 1, so

\[
\operatorname{Var}(\widehat E)
\leq\frac{.7^2+.4^2}{N}=\frac{13}{20N}.
\]

Choose \(\epsilon=1/5,\delta=1/10\). The sufficient N is 163 **per group**, hence 326 total circuit shots. Native sampling executes the two distinct basis-readout circuits below. It does not perform a single spectral measurement of \(.7X-.4Z\), nor do different seeds prove physical group independence. Shared random calibration or reuse of samples requires the covariance terms retained in 6.7; systematic bias requires a separate error analysis.

The trial count in this proof is fixed. For a concrete stopping counterexample, toss a fair Bernoulli coin, stop immediately on a first 1, otherwise take a second trial and stop. The records `1`, `01`, `00` have probabilities \(1/2,1/4,1/4\), sample means \(1,1/2,0\), and average mean \(5/8\), rather than the target \(1/2\). Repeating a fixed-N argument at a data-chosen stopping time is therefore unsupported. Sequential confidence methods need their own proof.

The helper rejects invalid design inputs, zero budgets for execution, nonpositive error, failure probabilities outside (0,1), and exact binomial evaluations beyond a teaching guard of N=1000. Native teaching executions are capped at 10000 shots. These limits are not FlagQuantum limits. Exact arithmetic in the classical design and binomial reference does not make a floating-point simulator or physical device exact.

```python
Ngroup = c.budget(F(13,20),F(1,5),F(1,10))
observed = []
for setting,seed in [('X',17),('Z',53)]:
    circuit = fq.Circuit(1,dtype=torch.complex128).ry(0,.83).p(0,-.61)
    if setting=='X': circuit.h(0)
    _,sample,_,_ = c.native(circuit,(0,),Ngroup,seed)
    observed.append(1-2*F(int(sample[:,0].sum().item()),Ngroup))
Ehat = F(7,10)*observed[0]-F(2,5)*observed[1]
stopped_mean = F(1,2)*1+F(1,4)*F(1,2)+F(1,4)*0
assert Ngroup==163 and stopped_mean==F(5,8)
assert c.invalid_checks()==14
print('Two-setting design:',Ngroup,'shots per group;',2*Ngroup,'total shots')
print('Observed weighted estimate:',Ehat)
print('Early-stopped fair-coin mean expectation:',stopped_mean,'; target1/2.')
print('14 malformed contracts rejected; no optional-stopping or hardware guarantee.')
```

```text
Two-setting design: 163 shots per group; 326 total shots
Observed weighted estimate: 299/1630
Early-stopped fair-coin mean expectation: 5/8 ; target1/2.
14 malformed contracts rejected; no optional-stopping or hardware guarantee.
```

### Complete program and implementation boundary

Run from the repository root in the pinned example environment:

```sh
python examples/foundations/confidence_shots.py
python scripts/check_confidence_shots_prose.py
```

The [complete program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/confidence_shots.py) executes 46 native CPU complex128 circuits: 24 Bernoulli, eight X-readout, twelve ordered categorical and two independent-setting-model queries. Exact rational checks verify integer-budget rounding, fixed-p binomial probabilities including endpoint parameters, the invalid plug-in rule, a small simultaneous categorical fixture and the stopping counterexample. Native observed intervals are not required to contain their target in every test; that would confuse one record with repeated-experiment coverage. Deterministic analytic probabilities and counts are checked independently.

Expected output of the complete program:

```text
24 native Bernoulli circuits: three conservative fixed designs, four preparations and two seeds; exact accounting, not single-record coverage assertions.
8 native X-readout circuits: score-range bound1 and250-shot design checked against analytic means.
12 ordered categorical circuits: shared records and union-bound failure allocation checked without assuming independent label counts.
2 separate X/Z circuits: fixed163shots per independent group; coefficient-square variance bound13/20 is a declared model bound.
Exact binomial coverage at p=.1,half-width=.1: N5=.91854,N6=.885735; conservative N500 meets>=.95 at six exact test probabilities.
Unsupported sample-variance plug-in at p=.1,N5,nominal95% has exact coverage .4095; early-stop mean target5/8 differs from1/2.
Exact simultaneous three-category fixture: 235/256 ; 14 malformed contracts rejected.
46 actual CPU complex128 circuit executions; atol1e-12,rtol0 for deterministic probability references; no hardware, posterior or optional-stopping guarantee.
```

The eight Python snippets are cumulative. `c` is an original book helper module; native operations are the actual `fq.run`, computational probabilities, selected terminal samples and explicit X-basis analyzer H. Coverage, budgets and diagnostic counterexamples are classical calculations. There is no invented native confidence endpoint, sampled collapse, hardware calibration or Bayesian inference API.

Tested versions: FlagQuantum 0.3.1, PyTorch 2.13.0 and Python 3.12.14. Evolution uses CPU complex128; deterministic probability checks use absolute tolerance \(10^{-12}\), relative tolerance zero. Exact Fraction design inputs deliberately avoid ceiling and lattice-endpoint errors from binary floating-point design values. Printed decimal coverages are presentations of exact finite sums. A correct implementation and seeded regression do not establish physical IID assumptions or interval coverage under model mismatch.

### Understanding checks and transfer tasks

**A. Unit conversion and budget.** A score lies in \([-2,3]\) energy units. Derive a known variance bound, then a sufficient integer budget for absolute energy error \(1/5\) and failure probability \(1/10\). Would scaling both score and requested error by 1000 change that budget?

**B. Closed versus strict events.** At \(p=1/10,N=5,\epsilon=1/10\), which counts make the closed interval cover? What changes if coverage requires \(|\widehat p-p|<\epsilon\)? Compute both probabilities exactly.

**C. Simultaneous statements.** You want eight frequency intervals to cover simultaneously with failure probability at most \(1/20\), each with half-width \(1/5\). Find the conservative shared shot budget. Explain why no independence between the eight frequency components was assumed.

**D. Fresh implementation transfer.** Use a new complex four-qubit preparation and an ordered nonadjacent selection. Assign every outcome an explicit bounded real score, derive the range variance bound, fix \(\epsilon,\delta,N\), and run native sampling. What can one record verify, and what still needs a coverage proof? Repeat with a new exact rational Bernoulli parameter and exact binomial reference.

<details markdown="1">
<summary>Answers and confidence checks for 6.8</summary>

**A.** The range width is 5, hence \(v=25/4\). The ratio is \((25/4)/[(1/10)(1/5)^2]=3125/2\); round upward to 1563. Scaling the score by 1000 scales v by \(1000^2\), and scaling the error by 1000 scales its square by the same factor, leaving the ratio unchanged. Failure probability is dimensionless.

**B.** Closed coverage includes counts 0 and 1: their errors are exactly \(1/10\). Its probability is \((9/10)^5+5(1/10)(9/10)^4=45927/50000\). Strict error smaller than \(1/10\) includes no count at all for this design, giving zero coverage. This sharp lattice effect is why the endpoint convention must be explicit. The Chebyshev bound is uninformative at this small N and does not contradict either result.

**C.** Allocate \(\delta_j=1/160\), so \(N\geq8/[4(1/20)(1/5)^2]=1000\). All labels use the same 1000 trial records. The union-bound proof used an indicator inequality and linearity of expectation, not independence between label events. The individual mean-variance bounds still use the stated independent-trial model.

**D.** Validate selected-column order, label indexing, record length, every score's declared range and the arithmetic of the interval. Compare exact computational probabilities with an independent indexed-amplitude reference within the floating-point tolerance. None of these checks proves that one observed interval must cover or that a physical device is IID. For a fixed rational p, use `c.coverage(p,N,epsilon)` as the exact model reference; retain closed endpoints. If N exceeds its teaching guard, use another explicitly validated reference rather than calling a floating approximation an exact certificate.

</details>

### Sources and next step

The frozen source is Boyd and Vandenberghe, *Convex Optimization* (2004), [§7.4.1 Chebyshev bounds, printed pages 374–375](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf#page=388), PDF pages 388–389 (`CVX:7.4`). The author-hosted PDF was downloaded and these pages inspected for the Markov/Chebyshev setup; only a locator and source hash are retained, not the PDF or extracted source text. This section supplies its own complete finite-model proofs, range-bound derivation, shot conversion and exact discrete examples. Public author-written companions are Marco Taboga's [Markov inequality](https://www.statlect.com/fundamentals-of-probability/Markov-inequality) and [Chebyshev inequality](https://www.statlect.com/fundamentals-of-probability/Chebyshev-inequality). Chernoff/Hoeffding bounds, exact interval inversion, sequential confidence procedures and optimal allocation are not proved or claimed here.

The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/6.8.json) keeps author execution, independent review and reader trials separate. Continue, when drafted, with [6.9 Measurement laboratory and failure diagnosis](../section-plans/01-foundations.md#sec-measurement-expectation-values-and-statistical-estimation-9).


<span id="sec-measurement-expectation-values-and-statistical-estimation-9"></span>

## 6.9 Measurement laboratory and failure diagnosis

**Working draft — bounded author-run verification; independent mathematical/implementation review and reader trial pending.**

This laboratory closes Chapter 6 by making a measurement claim inspectable. We use the earlier results to distinguish four questions: Was the intended state prepared? Does the readout implement the declared measurement? Are conditional and ignored-outcome predictions consistent? Is the uncertainty statement justified by its design? Passing one question cannot substitute for the others.

**Entry:** ideal conditional branches from 6.2, effective readout projectors from 6.4, covariance and mean uncertainty from 6.7, and fixed-design confidence guarantees from 6.8. Depth **V** requires executing an acceptance protocol and diagnosing deliberate failures; it does not introduce a new measurement postulate or replace the earlier proofs by finite tests. “Accepted” in the program means *passes this specific implementation protocol*. It does not mark this section, the chapter, a physical device or a paper reproduction as independently accepted.

The recurring preparation uses three qubits in full basis order \(q_0q_1q_2\), with \(q_0\) the most significant bit. All angles are radians. CPU statevectors are complex128; classical probabilities are float64. We use full-vector and deterministic probability absolute tolerance \(10^{-12}\), relative tolerance zero, without phase alignment or input normalization repair. Branch alternatives are explicit classical calculations on the actual simulated input; native terminal samples do not supply a collapsed state.
<span id="formula-code-6-9-contract"></span>

### 1. Declare the experiment and the acceptance gates


Prepare, in chronological call order, \(R_y(\theta)\) on qubit 0, CX from 0 to 2, X on spectator qubit 1, and \(P(\phi)\) on qubit 0. With \(c=\cos(\theta/2)\), \(s=\sin(\theta/2)\), the independent scalar reference is

\[
|\psi\rangle=c|010\rangle+e^{i\phi}s|111\rangle.
\]

Our main terminal readout measures \(Y_0\) and \(X_2\): apply P(−π/2) then H on qubit 0, H on qubit 2, and request ordered qubits `(2,0)`. Write its two output bits as x for qubit 2 and y for qubit 0. Labels are `00,01,10,11`; their score is \(w_{xy}=(-1)^{x+y}\). The main unknown mean is the expectation of that declared joint score, not a conditional-state amplitude.

| Protocol on the same preparation | Purpose | Executed boundary |
|---|---|---|
| Y0/X2 terminal readout | Joint score and finite record | Actual native rotations, selected probabilities and samples |
| Ideal Z measurement on qubit 2 | Conditional branches and repeatability | Classical projector/branch enumeration of the actual prepared state |
| Coarse even parity versus fine Z outcomes with forgotten record | Preserve or remove within-event coherence | Alternative ideal update models, not inferred native collapse |

For the terminal score the range is [−1,1]. Fix \(\epsilon=1/4\), \(\delta=1/5\) and the uniform single-shot variance bound 1 *before* observing data. Section 6.8 gives

\[
N=\left\lceil\frac{1}{\delta\epsilon^2}\right\rceil=80.
\]

The protocol checks preparation, basis/effects, raw counting and this fixed budget. Exact probability checks are deterministic; whether one reported interval contains the toy target is a separate diagnostic. The book helper is a bounded laboratory, not a new FlagQuantum endpoint or agent skill.

```python
from math import pi,sin,cos
from fractions import Fraction as F
import torch
from examples.foundations import measurement_lab as lab
N = lab.conf.budget(F(1),lab.EPS,lab.DELTA)
assert N==80
print('Declared readout columns: q2 then q0; labels00,01,10,11.')
print('Fixed design:',N,'trials; half-width',lab.EPS,'; failure budget',lab.DELTA)
```

```text
Declared readout columns: q2 then q0; labels00,01,10,11.
Fixed design: 80 trials; half-width 1/4 ; failure budget 1/5
```

<span id="formula-code-6-9-labels"></span>

### 2. Calibrate labels with a state that can expose an order reversal


The main state's qubits 0 and 2 always have equal computational bits. Its ordinary computational marginal on `(2,0)` is therefore identical to the one on `(0,2)`. Such a symmetric fixture cannot establish column order.

Use separate computational-basis calibration inputs. On \(|001\rangle\), the declared order `(2,0)` means bits `(1,0)`, label `10`, integer index

\[
j=2b_2+b_0=2.
\]

Reversing the requested order reports `01`, index 1. The complete program tests all eight basis words and rejects four asymmetric words under reversal. These queries test the native output convention with the analyzer absent; they are not eight copies of the main experiment. The subsequent experiment checks its analyzer separately.

```python
one_fixture = ((0,0,1),)
calibration = lab.calibrate((2,0),one_fixture)
reversed_calibration = lab.calibrate((0,2),one_fixture)
assert calibration['accepted'] and not reversed_calibration['accepted']
print('Asymmetric001 calibration, intended/reversed order:',calibration['accepted'],reversed_calibration['accepted'])
```

```text
Asymmetric001 calibration, intended/reversed order: True False
```

<span id="formula-code-6-9-readout"></span>

### 3. Match the actual circuit to independent scalar and projector references


For \(\theta=\phi=\pi/3\), the main state has amplitudes \(c=\sqrt3/2\) and \(e^{i\pi/3}s=e^{i\pi/3}/2\). In the preparation, indices 2 and 7 are the only nonzero coordinates.

Let R be the analyzer matrix. For the bit outcome `(x,y)` its effective projector is \(E_{xy}=R^\dagger Q_{xy}R\), where \(Q_{xy}\) selects computational bit \(b_2=x,b_0=y\) and leaves spectator qubit 1 unresolved. Using the Y and X analyzer identities from 6.4,

\[
E_{xy}=\frac14
\bigl(I+(-1)^yY_0\bigr)
\bigl(I+(-1)^xX_2\bigr).
\]

The operators act on different qubits and commute; the product is a rank-two projector. The one-qubit Y0 and X2 means vanish because each alone maps the two occupied coordinates outside their span. Their product acts as

\[
Y_0X_2|010\rangle=i|111\rangle,\qquad
Y_0X_2|111\rangle=-i|010\rangle.
\]

Substitution in the inner product gives

\[
C=\langle Y_0X_2\rangle
=-ics e^{i\phi}+ics e^{-i\phi}
=2cs\sin\phi=\sin\theta\sin\phi.
\]

Expanding the projector expectation consequently yields

\[
p_{xy}=\frac{1+(-1)^{x+y}C}{4}.
\]

The target here is \(C=3/4\) and the ordered probabilities are \((7,1,1,7)/16\). `acquire` actually calls native `fq.run` once for the preparation, and once for the prepared circuit with P/H/H analyzer, selected `fq.probabilities` and `fq.samples`. The complete program exposes these calls. Its independent matrix reference verifies the post-analyzer vector; explicit Pauli projectors and the scalar law independently check the measurement probabilities. A discrepancy is not repaired by renormalizing or aligning phases. The body also executes the native gate sequence and terminal request directly, comparing its probabilities and pinned-seed raw record with the wrapper. This adds one explicit native query; it is not counted as independent statistical evidence.

```python
import flagquantum as fq
from dataclasses import replace
native_circuit = fq.Circuit(3,dtype=torch.complex128)
native_circuit.ry(0,pi/3).cx(0,2).x(1).p(0,pi/3)
native_circuit.p(0,-pi/2).h(0).h(2)
native_result = fq.run(native_circuit,
    outputs=[fq.probabilities(qubits=(2,0)),fq.samples(qubits=(2,0))],
    shots=N,options=replace(lab.b.OPTIONS,seed=31))
packet = lab.acquire(pi/3,pi/3,N=N,seed=31)
torch.testing.assert_close(native_result.probabilities[0],packet['p'],atol=1e-12,rtol=0)
assert torch.equal(native_result.samples[0],packet['bits'])
report = lab.audit(packet)
expected = torch.tensor([7/16,1/16,1/16,7/16],dtype=torch.float64)
torch.testing.assert_close(packet['p'],expected,atol=1e-12,rtol=0)
assert report['accepted'] and all(report['checks'].values())
print('Native ordered probabilities:',[round(p,12) for p in packet['p'].tolist()])
print('Closed scalar correlation:',round(report['exact_correlation'],12))
print('Bounded implementation protocol:',report['accepted'])
```

```text
Native ordered probabilities: [0.4375, 0.0625, 0.0625, 0.4375]
Closed scalar correlation: 0.75
Bounded implementation protocol: True
```

<span id="formula-code-6-9-branches"></span>

### 4. Keep a branch ensemble when an outcome is ignored


Analyze an *alternative* ideal Zq2 measurement on the actual prepared input. For the worked positive angles its probabilities and normalized conditional vectors are

\[
p_0=c^2,\quad |\psi_0\rangle=|010\rangle,
\qquad
p_1=s^2,\quad |\psi_1\rangle=e^{i\phi}|111\rangle.
\]

The implementation uses full coordinate masks and preserves the branch phase; for general signed angles it retains the signs of c and s too. Exactly impossible branches are `None`. Positive tiny branches are not dropped merely because their probability is below the numerical comparison tolerance. Section 6.2 supplies the projector normalization and zero/underflow contract.

Repeatability requires \(P(a,\text{repeat }b)=\delta_{ab}p_a\). If the first outcome is ignored, a later projector Q has probability \(\sum_ap_a\langle\psi_a|Q|\psi_a\rangle\), not a probability evaluated on an average vector. For an XX+ test on qubits 0 and 2,

\[
p_+^{\mathrm{original}}=
\frac{1+\sin\theta\cos\phi}{2},\qquad
p_+^{\mathrm{forgotten\ Z_2}}=\frac12.
\]

Each Z branch is a basis state with zero XX mean, giving the latter value. An ideal **coarse** even-parity projection on q0 and q2 leaves the original state unchanged because both occupied basis states have even parity; its later XX+ probability remains the original value. It is a different update from fine measurement followed by forgetting the record.

The deliberate wrong proposal normalizes \(\sum_ap_a|\psi_a\rangle\). For this example it gives amplitudes proportional to \((3/4,e^{i\pi/3}/4)\), hence XX mean \(3/10\) and plus probability .65. Even after normalization it retains false coherence. The accepted algorithm never uses that proposal; it keeps the ensemble and obtains .5.

```python
branch = lab.branch_report(packet['initial'])
wrong_average = lab.averaged_branch_fault(packet['initial'])
assert not wrong_average['accepted']
assert abs(wrong_average['wrong_plus']-.65)<1e-12
print('Zq2 branch probabilities:',[round(p,12) for p in branch['probabilities'].tolist()])
print('XX+ after forgotten Zq2:',round(branch['xx_after_forgotten_Z'][0].item(),12))
print('Deliberate normalized-vector-average proposal:',round(wrong_average['wrong_plus'],12),'-> rejected.')
```

```text
Zq2 branch probabilities: [0.75, 0.25]
XX+ after forgotten Zq2: 0.5
Deliberate normalized-vector-average proposal: 0.65 -> rejected.
```

<span id="formula-code-6-9-basis"></span>

### 5. Accept effect-equivalent output phases and reject the wrong Y sign


A terminal measurement is specified by its effects, not by a unique analyzer matrix. Append an output phase D=P0(.37) after the correct analyzer. It commutes with every computational \(Q_{xy}\), because it is diagonal in those selected output bits. Therefore

\[
(DR)^\dagger Q_{xy}(DR)
=R^\dagger D^\dagger Q_{xy}DR
=R^\dagger Q_{xy}R.
\]

The after-analyzer statevector can change by outcome-dependent phases; this is not necessarily one global phase. The protocol compares native evolution with the *declared* candidate analyzer, then compares its effects with the intended measurement. It accepts this operational equivalence. It does not claim the circuits interchangeable for later coherent operations before terminal readout.

By contrast, changing P(−π/2) to P(+π/2) changes the measured Y to −Y. The joint correlation becomes −C and the probabilities swap the two parity classes. The program records a rejected candidate instead of hiding the failure or changing the target formula. A later passing candidate is a new result; it does not retroactively accept the failed one.

```python
gauge_packet = lab.acquire(pi/3,pi/3,'outcome-phase',N=N,seed=31)
wrong_packet = lab.acquire(pi/3,pi/3,'wrong-y',N=N,seed=31)
gauge_report, wrong_report = lab.audit(gauge_packet),lab.audit(wrong_packet)
assert gauge_report['accepted'] and not wrong_report['accepted']
assert gauge_report['checks']['measurement_effects']
assert not wrong_report['checks']['measurement_effects']
assert wrong_report['candidate_sha256'] != report['candidate_sha256']
print('Output-phase equivalent analyzer accepted:',gauge_report['accepted'])
print('Wrong-Y candidate accepted:',wrong_report['accepted'])
```

```text
Output-phase equivalent analyzer accepted: True
Wrong-Y candidate accepted: False
```

<span id="formula-code-6-9-records"></span>

### 6. Reconstruct counts and check the declared preparation source


For the requested column order, each raw bit row has index \(j_t=2b_{t,0}+b_{t,1}\), count \(C_j=\sum_t1_{\{j_t=j\}}\), and joint score \((-1)^{b_{t,0}+b_{t,1}}\). Rebuild counts from the raw integer bits and verify \(\sum_jC_j=N\). If a saved histogram disagrees, its attractive mean or error bar cannot rescue it.

Source consistency also matters. Reusing the old preparation state while declaring a different φ can leave its computational probabilities unchanged: those depend only on \(c^2,s^2\). The full preparation reference retains the phase and exposes the stale-source mismatch; the declared joint correlation also changes. A digest of the packet is useful for identifying which candidate a report describes. It is not authentication of metadata, a guarantee of hardware provenance, or a substitute for a trusted acquisition path. The lab's analyzer program and its matrix reference are checked for internal agreement; it is not an external attestation system.

The following edits are deliberate fault injections into copies. The original raw record remains unchanged, and both failures retain their own fingerprints.

```python
bad_counts = dict(packet)
bad_counts['counts'] = packet['counts'].clone()
bad_counts['counts'][0] += 1
stale_phase = dict(packet)
stale_phase['phi'] = -packet['phi']
count_report, source_report = lab.audit(bad_counts),lab.audit(stale_phase)
assert not count_report['accepted'] and not count_report['checks']['labels_and_counts']
assert not source_report['accepted'] and not source_report['checks']['initial_model']
assert lab.audit(packet)['candidate_sha256'] == report['candidate_sha256']
print('Count corruption and stale phase-source candidates accepted:',count_report['accepted'],source_report['accepted'])
print('Original candidate remains separately identifiable:',lab.audit(packet)['accepted'])
```

```text
Count corruption and stale phase-source candidates accepted: False False
Original candidate remains separately identifiable: True
```

<span id="formula-code-6-9-uncertainty"></span>

### 7. Check the uncertainty design separately from whether one interval covers


The joint score W takes values ±1. Its variance is \(1-C^2\leq1\), and IID averaging gives a conservative mean-variance bound \(1/N\). The frozen laboratory design uses that uniform bound 1, not an observed variance or a newly inferred tighter bound. With 80 trials its declared interval is \([\widehat C-1/4,\widehat C+1/4]\), with at least 80% coverage under the model from 6.8.

The protocol rejects a packet with four trials for this design, even if its state, effects and exact probabilities are all correct. It also rejects an unexplained replacement of the certified variance bound by zero. A legitimate tighter analytic or separately validated bound would require a documented design change; this lab does not infer it from a favorable record.

Interval membership and implementation validity have different roles. The actual toy-model membership diagnostic may be true or false for a valid packet. A miss is a statistical alert to interpret under the fixed procedure and its model, not an automatic deterministic code defect. Conversely, a deliberately corrupted packet cannot be accepted because its interval happened to include the target. Repeatedly selecting seeds or increasing shots until an interval looks favorable would change the experiment; this protocol does not authorize that stopping/selection rule.

```python
short_packet = lab.acquire(pi/3,pi/3,N=4,seed=31)
short_report = lab.audit(short_packet)
unsupported_bound = dict(packet)
unsupported_bound['variance_bound'] = F(0)
bound_report = lab.audit(unsupported_bound)
assert short_report['checks']['probability_model'] and not short_report['checks']['fixed_budget']
assert not bound_report['checks']['fixed_budget']
assert not short_report['accepted'] and not bound_report['accepted']
print('Four-shot and unexplained-zero-bound candidates accepted:',short_report['accepted'],bound_report['accepted'])
print('Observed correlation estimate:',report['observed_correlation'])
print('This toy interval contains its target:',report['interval_contains_toy_target'],'; diagnostic only.')
```

```text
Four-shot and unexplained-zero-bound candidates accepted: False False
Observed correlation estimate: 33/40
This toy interval contains its target: True ; diagnostic only.
```

<span id="formula-code-6-9-evidence"></span>

### 8. Diagnose a blind spot and retain the original failed evidence


At φ=0 the intended joint correlation C is zero. Both the correct and wrong-sign Y analyzers then produce the same four probabilities for this particular preparation. A probability-only check would pass the faulty candidate. Its *effects* still differ as operators, so the protocol rejects it. This is why the independent operator check and asymmetric calibration are part of the acceptance contract rather than optional decorations.

The evidence bundle retains declared angles, program and IR fingerprint, selected columns, shot count/seed, actual prepared and after-analyzer vectors, exact probabilities, raw bits, counts and separate diagnostic reports. The complete program exports no file by default; the author-run wrapper archives these objects under the section evidence directory. Negative/malformed probabilities, invalid shapes/dtypes/seeds, unknown variants and invalid labels are rejected without repair. Twelve malformed-contract tests run before any new native execution.

A reproducible packet and a passing deterministic protocol are author evidence. Independent mathematical/implementation review and reader trials remain separate. No synthetic raw record is presented as a native observation, and no physical experiment or independent agent review is claimed.

```python
zero_signal_wrong = lab.acquire(pi/3,0.,'wrong-y',N=N,seed=31)
blind_report = lab.audit(zero_signal_wrong)
assert blind_report['checks']['probability_model']
assert not blind_report['checks']['measurement_effects'] and not blind_report['accepted']
assert lab.invalid_checks(packet)==12
assert not wrong_report['accepted'] and lab.audit(packet)['accepted']
print('Zero-signal wrong-Y: probability test passes, effect test fails -> rejected.')
print('12 malformed contracts rejected; original wrong candidate remains rejected after a valid candidate passes.')
```

```text
Zero-signal wrong-Y: probability test passes, effect test fails -> rejected.
12 malformed contracts rejected; original wrong candidate remains rejected after a valid candidate passes.
```

### Complete program and verification record

Run from the repository root with the pinned example environment:

```sh
python examples/foundations/measurement_lab.py
python scripts/check_measurement_lab_prose.py
```

The [complete program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/measurement_lab.py) executes 70 native circuits: 16 basis-calibration queries, 48 queries for 24 normal/effect-equivalent preparation-readout cases, and six queries for three deliberate-failure cases. Conditional branches, repeated-projector tables, coarse/fine predictions and classical corruptions use the actual prepared vectors without additional quantum executions. Deterministic code checks never demand that every random confidence interval cover.

Expected output of the complete program:

```text
16 native basis-calibration circuits: all8 intended-order fixtures pass; reversed order fails4 asymmetric fixtures.
48 native circuits:24 preparations/readouts over complex/zero-branch inputs and two effect-equivalent analyzers pass; branch/repeatability checks are classical.
6 more native circuits:wrong-Y,zero-signal wrong-Y and insufficient-shot candidates rejected; exact effect tests expose a probability-only blind spot.
4 additional classical faults rejected:corrupted counts,stale preparation phase,unsupported variance bound and normalized-vector averaging.
12 malformed contracts rejected before execution; correct and rejected candidate fingerprints/raw records kept separately.
70 actual CPU complex128 circuit executions; deterministic atol1e-12,rtol0; interval membership is diagnostic and is not forced to pass.
Acceptance here is this bounded author-run implementation protocol,not independent scholarly review,hardware validation or a new agent skill.
```

The complete evidence records the deliberately wrong Y sign, its zero-signal probability blind spot, short budget, corrupted count, stale preparation phase, unsupported variance bound, and normalized-vector-average proposal. Their rejection is an intended test result, not an unexpected native API failure. After the first passing version, the author strengthened malformed probability/seed and program-reference guards; the initial passing program/output and subsequent guarded version are retained separately. No original failure is erased by a later passing candidate.

The eight body snippets are cumulative. `lab` is a book helper, not a FlagQuantum acceptance endpoint. Native support here is CPU complex128 unitary preparation and analyzer execution, exact selected computational probabilities and terminal samples, checked on FlagQuantum 0.3.1/PyTorch 2.13.0/Python 3.12.14. General projectors, conditional updates, covariance/design arithmetic and acceptance reports are explicit classical references. The three-qubit setup is a bounded teaching experiment, not a package limit or a general hardware certification tool. Native statevector returns remain pre-readout simulated vectors; no collapse, reset, generalized instrument endpoint or noise-calibrated device result is asserted.

### Chapter 6 synthesis and problems

Chapter 6 now has nine working drafts. Its path separates a probability law, a conditional update, an observable's spectral mean, a basis analyzer, a generalized measurement/instrument, a finite record, its covariance and a confidence procedure. This laboratory checks their interfaces without conflating them. Chapter completion as working drafts is not formal acceptance.

**A. Concept and identifiability.** Why does the main state's computational marginal fail to diagnose qubit-order reversal? Why can wrong-sign Y pass a probability test at φ=0? Give an independent test that resolves each blind spot.

**B. Derivation and update.** In the worked state, derive the forgotten-Zq2 XX+ probability .5 and the normalized-average proposal's .65. Explain why normalization cannot turn that average into the correct ignored-outcome state. What changes for an exactly impossible branch?

**C. Implementation transfer.** Choose θ=−.43 and φ=1.19, then a second fresh pair of angles. Predict the preparation amplitudes and Y0/X2 probabilities. Run both the intended and output-phase analyzers, retain the full conditional phase, and check all report gates. Include one deliberately wrong-sign candidate; predict which gate should reject it before executing it.

**D. Diagnosis and reporting.** Classify each observation: raw-count sum is wrong; prepared probabilities match but phase is stale; a valid fixed-design interval misses; an unexplained zero variance bound is used; a new output phase leaves all effects unchanged. State which evidence to keep and whether implementation acceptance, statistical interpretation or a design change is required.

<details markdown="1">
<summary>Answers and chapter-laboratory checks</summary>

**A.** The occupied basis states have equal q0/q2 bits, so their marginal is invariant under that swap. An asymmetric basis word such as `001` distinguishes labels `10` and `01`. At φ=0, \(C=\sin\theta\sin\phi=0\), making the two wrong/correct analyzers agree on that preparation's probabilities. Compare full effective projectors with the intended Pauli family, or use an independent input with nonzero Y0/X2 correlation. Do not relabel the wrong analyzer as correct solely because the chosen input hides it.

**B.** Each retained Zq2 branch is a computational basis state and has XX mean zero, hence the weighted later plus probability is .5. The wrong normalized average has coefficients \((3/4,e^{i\pi/3}/4)/\sqrt{10/16}\). Its XX mean is \(2(3/4)(1/4)\cos(\pi/3)/(10/16)=3/10\), giving .65. The error is the retained coherence between alternatives, not merely the vector norm. An exactly zero-probability branch is `None` and contributes zero to the ensemble sum; it is not a zero vector to normalize. Tiny positive branches retain their own normalized phase, subject to the explicit underflow contract.

**C.** Use \(v_2=\cos(\theta/2)\), \(v_7=e^{i\phi}\sin(\theta/2)\), and zero elsewhere. For negative θ, the sign of the second amplitude is part of the vector; do not remove it by replacing it with its magnitude. With \(C=\sin\theta\sin\phi\), probabilities are \((1+C,1-C,1-C,1+C)/4\). Both intended and output-phase variants should satisfy the effect and reference-evolution gates. Wrong-sign Y fails the operator-family gate and, for nonzero C, also the probability-model gate. Use the pinned helper and a separately indexed or scalar reference, not only two calls to the same circuit routine.

**D.** Count corruption rejects the record layer; stale phase rejects source/preparation consistency even when computational probabilities agree. A valid interval miss is a statistical diagnostic, requiring the fixed procedure and assumptions to be reported rather than secretly selecting another seed. The unexplained zero bound rejects this design's uncertainty gate; any legitimate tighter bound needs documented justification. Output phases commuting with all final computational projectors are accepted for this terminal measurement, while coherent future uses require their own contract. Preserve each original packet and report separately; a corrected implementation is a new candidate.

</details>

### Sources, status and transition

The frozen source `ED:protocol` is the repository's original [reader continuity and acceptance evidence standard](../reader-continuity.md#reader-review-and-acceptance-evidence). It requires reconstructible reasoning, usable prerequisites, independent references and separate reviewer/reader evidence. The physical and mathematical ingredients are the working drafts of 6.1–6.8, particularly 6.2, 6.4, 6.7 and 6.8; this V section reuses those results rather than importing a new postulate or starting a paper audit. See the [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/6.9.json) for author checks and the [retained diagnostic reports](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-evidence/6.9/reports.json) for deliberate rejection outcomes. Independent mathematical/implementation review and reader trials remain pending.

Continue, when drafted, with [7.1 Product states and entangled states](../section-plans/01-foundations.md#sec-entanglement-and-quantum-information-protocols-1).

<!-- end-section-6.9 -->
