# 7. Entanglement and Quantum Information Protocols

**Working drafts: sections 7.1–7.7 · Writing Baseline 1.0 · October 23, 2026.** Author execution is recorded separately from independent mathematical review, implementation review and reader trial; all three remain pending. Examples use FlagQuantum 0.3.1, PyTorch 2.13.0 and CPU complex128 statevectors.

<span id="sec-entanglement-and-quantum-information-protocols-1"></span>

## 7.1 Product states and entangled states

A tensor-product space contains product vectors, but it also contains vectors that cannot be written as one product. This distinction depends on **which systems are grouped together**. We will prove a test for a finite, normalized **pure** state across a declared bipartition, and translate the coefficient indices into code. The prerequisite is [4.1, tensor-product spaces and basis states](ch-composite-systems-tensor-products-and-qubit-ordering.md#sec-composite-systems-tensor-products-and-qubit-ordering-1). Depth **F** requires both directions of the result, including normalization of the recovered factors. No Schmidt decomposition is assumed here; it follows in 7.2.

All amplitudes and angles below are dimensionless; angles are radians. Qubit q0 is the most significant bit in the full statevector index. Ordered qubit tuples specify each subsystem's internal basis order. We use exact mathematics for the theorem and absolute tolerance $10^{-12}$, relative tolerance zero, for deterministic execution checks. Neither a small reconstruction residual nor a numerical rank estimate proves exact separability of an unknown physical state.

Run the eight cumulative Python blocks from the repository root after installing `requirements-examples.txt`. The complete checked program is [product_entanglement.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/product_entanglement.py). Coefficient gathering, minors and pivot factorization are original classical book helpers; FlagQuantum performs the stated preparations and probability/statevector queries.

<span id="formula-code-7-1-coefficients"></span>

### 1. A product has coefficients that multiply without conjugation

**Formula.** Fix orthonormal bases $\{|i\rangle_A\}_{i=0}^{d_A-1}$ and $\{|j\rangle_B\}_{j=0}^{d_B-1}$. Write

$$
|\psi\rangle=\sum_{i,j} C_{ij}|i\rangle_A\otimes|j\rangle_B,
\qquad \sum_{i,j}|C_{ij}|^2=1.
$$

The array C is the **coefficient matrix**. A product state across $A|B$ means that normalized vectors $|a\rangle_A$ and $|b\rangle_B$ exist with $|\psi\rangle=|a\rangle_A\otimes|b\rangle_B$.

**Derivation.** Expand both factors and distribute the tensor product:

$$
\left(\sum_i a_i|i\rangle_A\right)\otimes
\left(\sum_j b_j|j\rangle_B\right)
=\sum_{i,j} a_i b_j|i\rangle_A\otimes|j\rangle_B.
$$

Uniqueness of coordinates in a basis gives $C_{ij}=a_i b_j$, or $C=ab^{\mathsf T}$. The transpose is not an adjoint: there is no inner product between the two factors. For $a=(1,i)^{\mathsf T}/\sqrt2$ and $b=(1,-i)^{\mathsf T}/\sqrt2$, this gives $C=\frac12\begin{pmatrix}1&-i\\ i&1\end{pmatrix}$.

**FlagQuantum code → verification result.** This is the actual native execution path. The `[0]` removes the execution batch axis. Later uses of `e.query` run the same native request with the same options and count actual circuit executions.

```python
import math
import torch
import flagquantum as fq
import examples.foundations.product_entanglement as e
circuit = fq.Circuit(2, dtype=e.D)
circuit.ry(0, math.pi/2).p(0, math.pi/2)
circuit.ry(1, math.pi/2).p(1, -math.pi/2)
result = fq.run(circuit, outputs=[fq.probabilities()], options=e.OPTIONS)
assert result.statevector().shape == (1, 4)
state = result.statevector()[0]
a = torch.tensor([1, 1j], dtype=e.D)/math.sqrt(2)
b = torch.tensor([1, -1j], dtype=e.D)/math.sqrt(2)
C = e.coefficients(state, (0,), (1,))
assert torch.allclose(C, torch.outer(a, b), atol=e.ATOL, rtol=0)
assert torch.allclose(result.probabilities[0], state.abs()**2, atol=e.ATOL, rtol=0)
print(f'coefficient norm squared = {C.abs().square().sum().item():.6f}')
```
```text
coefficient norm squared = 1.000000
```

<span id="formula-code-7-1-partition"></span>

### 2. Declare the cut before reshaping the vector

**Formula.** If $A=(q_{a_0},\ldots,q_{a_{k-1}})$ and $B=(q_{b_0},\ldots,q_{b_{n-k-1}})$ are ordered complementary lists, then

$$
i=\sum_{u=0}^{k-1}x_{a_u}2^{k-1-u},\quad
j=\sum_{v=0}^{n-k-1}x_{b_v}2^{n-k-1-v},\quad
C_{ij}=\psi_{\sum_{q=0}^{n-1}x_q2^{n-1-q}}.
$$

**Derivation.** Each full bit string supplies exactly one row and one column label. Conversely, unpacking i and j into their declared positions recovers exactly one full bit string. Thus gathering coefficients only changes their arrangement; it preserves $\sum|C_{ij}|^2$. A plain reshape implements this arrangement only when its axis order already matches $A$ followed by B. For other cuts, gather indices explicitly or permute the tensor axes first.

For example, prepare a Bell pair on q0 and q2 and a separate state on q1. With $A=(q_2,q_0)$ and $B=(q_1)$,

$$
|\psi\rangle=\frac{|00\rangle_A+|11\rangle_A}{\sqrt2}
\otimes\left(\cos(\pi/6)|0\rangle_B+\sin(\pi/6)|1\rangle_B\right).
$$

The two qubits inside A are entangled with each other, yet the entire vector is a product across $A|B$. The phrase “product state” must identify its cut.

**FlagQuantum code → verification result.** `coefficients` implements the displayed bit formula, rather than assuming that a reshape changes qubit order.

```python
three, _ = e.query(fq.Circuit(3, dtype=e.D).h(0).cx(0, 2).ry(1, math.pi/3))
C_A = e.coefficients(three, (2, 0), (1,))
a_A = torch.tensor([1, 0, 0, 1], dtype=e.D)/math.sqrt(2)
b_B = torch.tensor([math.cos(math.pi/6), math.sin(math.pi/6)], dtype=e.D)
assert torch.allclose(C_A, torch.outer(a_A, b_B), atol=e.ATOL, rtol=0)
assert not torch.allclose(C_A, three.reshape(4, 2), atol=e.ATOL, rtol=0)
print('ordered cut (q2,q0)|(q1): explicit product verified')
```
```text
ordered cut (q2,q0)|(q1): explicit product verified
```

<span id="formula-code-7-1-proof"></span>

### 3. Prove product if and only if rank one

**Theorem.** A normalized pure vector is a product across $A|B$ exactly when its coefficient matrix C has rank one. Here **rank** means the dimension of the linear span of the columns.

**Forward direction.** If $C=ab^{\mathsf T}$, each column is $b_j a$. At least one $b_j$ is nonzero, since b has unit norm, and a is nonzero. Hence the column span is exactly the one-dimensional span of a.

**Reverse direction, including factors and normalization.** Assume rank one. Since C has squared norm one, choose a nonzero entry $C_{rs}$. Column s is nonzero. Every column j is a scalar multiple $\lambda_j$ of column s; its row r gives $\lambda_j=C_{rj}/C_{rs}$. Consequently,

$$
C_{ij}=\frac{C_{is}C_{rj}}{C_{rs}},\qquad
u_i=C_{is},\quad v_j=\frac{C_{rj}}{C_{rs}},\qquad
C=uv^{\mathsf T}.
$$

Let $t=\|u\|_2>0$, $a=u/t$ and $b=tv$. Then $\|a\|_2=1$ and

$$
1=\sum_{i,j}|a_i b_j|^2
=\left(\sum_i|a_i|^2\right)\left(\sum_j|b_j|^2\right)
=\|b\|_2^2.
$$

Thus both factors are normalized and their product equals the original vector, including its phase. Replacing $(a,b)$ by $(e^{i\chi}a,e^{-i\chi}b)$ gives the same vector, so individual factor phases are not unique.

An equivalent exact condition is that **all two-by-two minors vanish**:

$$
C_{ij}C_{kl}-C_{il}C_{kj}=0
\quad(i<k,\ j<l).
$$

A product makes each difference zero by substitution. Conversely, if all minors vanish, choose $C_{rs}\ne0$. If i=r or j=s, the following identity holds directly by substitution. Otherwise the minor with distinct rows i,r and distinct columns j,s, with a possible sign from their ordering, gives $C_{ij}C_{rs}=C_{is}C_{rj}$. The same factor construction therefore applies, proving rank one. This proves the equivalence in every finite rectangular dimension, not just for two qubits.

**Code → verification result.** This classical translation constructs candidates from a largest-magnitude pivot to avoid choosing an unnecessarily small divisor. For non-product inputs it reports a reconstruction residual; it does not force the right factor to unit norm or declare an exact rank. The normalized product from unit 1 reconstructs correctly, while the mistaken adjoint product fails.

```python
recovered_a, recovered_b, residual = e.pivot_factors(C)
assert residual < e.ATOL
assert abs(torch.linalg.vector_norm(recovered_b).item()-1) < e.ATOL
assert max(abs(m) for m in e.minors(C)) < e.ATOL
wrong = torch.outer(a, b.conj())
assert torch.linalg.vector_norm(C-wrong).item() > 1
print('pivot reconstruction and all minors passed; conjugating b failed')
```
```text
pivot reconstruction and all minors passed; conjugating b failed
```

<span id="formula-code-7-1-entangled"></span>

### 4. One nonzero minor proves entanglement of a pure vector

**Formula and derivation.** A pure state that is not a product across the cut is **entangled** across that cut. For two single-qubit subsystems C is two by two, so its only minor is its determinant:

$$
|\psi_{\theta,\phi}\rangle
=\cos(\theta/2)|00\rangle+e^{i\phi}\sin(\theta/2)|11\rangle,
\qquad
\det C=e^{i\phi}\cos(\theta/2)\sin(\theta/2).
$$

If both amplitudes are nonzero, the determinant is nonzero and rank cannot be one. For $\theta=0$ or $\pi$ one amplitude vanishes, giving a product. At $\theta=\pi/2,\phi=0$ this is the Bell state $(|00\rangle+|11\rangle)/\sqrt2$, whose determinant is $1/2$. No choice of phases in two local factors can remove that obstruction.

**FlagQuantum code → verification result.** The sparse analytic vector checks the native preparation independently of a matrix-rank routine. A nonzero two-by-two minor also proves entanglement across the other cut of the three-qubit example.

```python
phi = .7
theta = math.pi/3
bell, _ = e.query(fq.Circuit(2, dtype=e.D).ry(0, theta).cx(0, 1).p(0, phi))
z = complex(math.cos(phi), math.sin(phi))
expected = torch.tensor([math.cos(theta/2), 0, 0, z*math.sin(theta/2)], dtype=e.D)
assert torch.allclose(bell, expected, atol=e.ATOL, rtol=0)
C_bell = e.coefficients(bell, (0,), (1,))
determinant = e.minors(C_bell)[0]
assert abs(determinant.item()-z*math.cos(theta/2)*math.sin(theta/2)) < e.ATOL
assert max(abs(m) for m in e.minors(e.coefficients(three, (0,), (1, 2)))) > .1
print(f'pair determinant magnitude = {abs(determinant.item()):.6f}')
```
```text
pair determinant magnitude = 0.433013
```

<span id="formula-code-7-1-local"></span>

### 5. Local changes preserve product versus entangled

**Formula.** For local unitaries L on A and R on B, expand the two output indices:

$$
C'_{ij}=\sum_{k,l} L_{ik}C_{kl}R_{jl},\qquad C'=LCR^{\mathsf T}.
$$

**Derivation.** Each ket $|k\rangle_A$ becomes $\sum_i L_{ik}|i\rangle_A$ and each $|l\rangle_B$ becomes $\sum_j R_{jl}|j\rangle_B$. Grouping the coefficient of $|i,j\rangle$ gives the formula; again the transpose is not an adjoint. Left multiplication by invertible L maps a column span bijectively, preserving its dimension. Right multiplication by invertible $R^{\mathsf T}$ preserves the column span: its new columns are combinations of old ones, and the inverse expresses old columns as combinations of new ones. Thus $\operatorname{rank}C'=\operatorname{rank}C$.

Changing local bases also multiplies by invertible matrices, so the property does not depend on the chosen local orthonormal coordinates. Changing the bipartition itself is a different operation, as unit 2 showed. For two qubits, unitary determinants have modulus one, hence $|\det C'|=|\det C|$.

**FlagQuantum code → verification result.** Execute a local rotation on q0 and a phase on q1 after the entangling preparation; compare every complex coefficient with $LCR^{\mathsf T}$.

```python
angle, phase = .4, -.8
moved, _ = e.query(fq.Circuit(2, dtype=e.D).ry(0, theta).cx(0, 1).p(0, phi)
                   .ry(0, angle).p(1, phase))
L = torch.tensor([[math.cos(angle/2), -math.sin(angle/2)],
                  [math.sin(angle/2), math.cos(angle/2)]], dtype=e.D)
R = torch.diag(torch.tensor([1, complex(math.cos(phase), math.sin(phase))], dtype=e.D))
C_moved = e.coefficients(moved, (0,), (1,))
assert torch.allclose(C_moved, L@C_bell@R.T, atol=e.ATOL, rtol=0)
assert abs(abs(e.minors(C_moved)[0])-abs(determinant)) < e.ATOL
print('local transformations preserve the determinant magnitude')
```
```text
local transformations preserve the determinant magnitude
```

<span id="formula-code-7-1-probabilities"></span>

### 6. Computational probabilities alone can hide entanglement

**Formula and derivation.** Compare

$$
|p\rangle=\frac{|00\rangle+|01\rangle+|10\rangle+|11\rangle}{2}
=|+\rangle\otimes|+\rangle,
\qquad
|g\rangle=\frac{|00\rangle+|01\rangle+|10\rangle-|11\rangle}{2}.
$$

Both give $p(ij)=1/4$ in computational measurement. However, their coefficient determinants are respectively zero and $-1/2$. Thus even a full computational distribution that factors into two marginal distributions does not establish a product **pure state**. The relative signs matter. Conversely, classical correlations of outcomes alone do not establish entanglement of a general mixed input; mixtures require Chapter 8's definitions.

**FlagQuantum code → verification result.** Controlled-Z changes one amplitude sign; exact computational probabilities stay the same.

```python
plus, p_plus = e.query(fq.Circuit(2, dtype=e.D).h(0).h(1))
graph, p_graph = e.query(fq.Circuit(2, dtype=e.D).h(0).h(1).cz(0, 1))
assert torch.allclose(p_plus, p_graph, atol=e.ATOL, rtol=0)
assert abs(e.minors(e.coefficients(plus, (0,), (1,)))[0]) < e.ATOL
assert abs(e.minors(e.coefficients(graph, (0,), (1,)))[0].item()+.5) < e.ATOL
print('same four probabilities; product determinant 0, entangled determinant -0.5')
```
```text
same four probabilities; product determinant 0, entangled determinant -0.5
```

<span id="formula-code-7-1-precision"></span>

### 7. A numerical tolerance is not the theorem's zero

**Formula and derivation.** For $0<\epsilon<1$,

$$
|\psi_\epsilon\rangle=\sqrt{1-\epsilon^2}|00\rangle+\epsilon|11\rangle,
\qquad \det C_\epsilon=\epsilon\sqrt{1-\epsilon^2}>0.
$$

Every such exact vector is entangled, however small ε is. Its distance from $|00\rangle$ is

$$
\|\psi_\epsilon-|00\rangle\|_2
=\sqrt{\left(\sqrt{1-\epsilon^2}-1\right)^2+\epsilon^2},
$$

which tends to zero. Finite precision can therefore make entangled and product vectors indistinguishable at a declared tolerance. A tolerance-based routine may report “consistent with a product at this resolution”; it must not claim an exact product theorem for the physical input. A positive computed minor is evidence about the represented vector, with floating-point error still requiring assessment. Underflow or uncertain input amplitudes can invalidate a naive exact-zero interpretation.

**FlagQuantum code → verification result.** The amplitude survives at epsilon $10^{-10}$; elementwise closeness to a product at a separately declared diagnostic tolerance $10^{-9}$ still passes. Implementation comparisons retain their tighter $10^{-12}$ tolerance. No automatic numerical-rank threshold is used.

An initial native example at epsilon $10^{-14}$ failed: the returned entangling amplitude was exactly zero. A four-value probe found this also at $10^{-12}$ and $10^{-13}$; an explicit unitary-matrix probe did not restore it. This behavior is retained as an implementation boundary, reported in [FlagQuantum issue #704](https://github.com/flagos-ai/FlagQuantum/issues/704), and is not a proof of an exact product input or a library fix. The runnable example uses the validated larger amplitude; the exact theorem above includes arbitrarily small nonzero epsilon.

**Upstream repair status (October 22, 2026).** [PR #712](https://github.com/flagos-ai/FlagQuantum/pull/712), source commit `046c465c6`, preserves tiny nonzero angles and supplied matrix components through the affected compiler paths. The source-checkout regressions include the smaller amplitudes and use zero absolute tolerance on those components. This source repair is merged as `8a18f5563`. A package release containing it has not been verified. The released-0.3.1 example and its original tiny-angle failure remain unchanged; see the [validation ledger](../upstream-fixes.md).

```python
zero, _ = e.query(fq.Circuit(2, dtype=e.D))
epsilon = 1e-10
tiny, _ = e.query(fq.Circuit(2, dtype=e.D).ry(0, 2*math.asin(epsilon)).cx(0, 1))
minor = e.minors(e.coefficients(tiny, (0,), (1,)))[0].real.item()
assert minor > 0 and abs(minor/epsilon-1) < 1e-12
assert torch.allclose(tiny, zero, atol=1e-9, rtol=0)
print(f'nonzero minor = {minor:.1e}; allclose to a product at 1e-9 = True')
```
```text
nonzero minor = 1.0e-10; allclose to a product at 1e-9 = True
```

<span id="formula-code-7-1-contract"></span>

### 8. State the input contract and verification boundary

**Formula and derivation.** The theorem assumes a nonzero normalized pure vector in $\mathbb C^{d_A}\otimes\mathbb C^{d_B}$, with $d_A,d_B\ge1$, and fixed orthonormal product coordinates. The zero matrix has rank zero and no normalized factors, which explains the nonzero condition. If one subsystem has dimension one, every normalized vector is a product; the minors condition is empty and the pivot construction still works. For a global phase $e^{i\gamma}$, multiplying C by that phase preserves rank, while a two-by-two minor acquires $e^{2i\gamma}$. Vanishing and nonvanishing are unchanged.

The qubit gather helper deliberately accepts only two to four qubits, nonempty complementary tuples and normalized finite unbatched CPU complex128 vectors. The matrix helpers accept normalized finite rectangular arrays of side lengths at most 16. These are teaching reference guards, not FlagQuantum's capacity limits. A density operator, raw outcome counts or a batched array does not satisfy this pure-vector contract. We do not silently flatten, renormalize, infer a cut, or replace a complex transpose by an adjoint.

**Code → verification result.** These malformed requests are rejected before another simulation. The singleton example independently checks the theorem's dimensional boundary, outside the qubit gather helper's narrower interface.

```python
bad = [lambda: e.coefficients(torch.zeros(4, dtype=e.D), (0,), (1,)),
       lambda: e.coefficients(state, (0,), (0,)),
       lambda: e.coefficients(state.reshape(1, 4), (0,), (1,))]
for attempt in bad:
    try:
        attempt()
    except ValueError:
        pass
    else:
        raise AssertionError('invalid pure-vector contract admitted')
singleton = torch.tensor([[.6, .8j]], dtype=e.D)
sa, sb, error = e.pivot_factors(singleton)
assert error < e.ATOL and not e.minors(singleton)
phase_C = complex(math.cos(.83), math.sin(.83))*C_bell
assert abs(abs(e.minors(phase_C)[0])-abs(determinant)) < e.ATOL
print('3 malformed contracts rejected; singleton and global-phase boundaries passed')
```
```text
3 malformed contracts rejected; singleton and global-phase boundaries passed
```

### Complete example and independent checks

```bash
python examples/foundations/product_entanglement.py
python scripts/check_product_entanglement_prose.py
```

The program executes 43 native circuits: 12 basis, 12 complex product, 9 entangled pair, 3 nonadjacent-register, 3 near-product and 4 locally transformed Bell preparations. Every two/three-qubit basis and complex product fixture is checked over every ordered bipartition. Independent references use scalar coordinate products, analytic sparse amplitudes and explicit two-by-two minors, rather than a numerical rank routine. Ten malformed contracts are rejected before simulation. The separate body checker executes the actual eight cumulative fragments, compares their printed outputs exactly, and then checks the complete program's output. A separately recorded four-qubit transfer run uses fresh angles, phases and ordered nonadjacent cuts.

Expected output of the complete program:

```text
12 native basis states: all ordered bipartitions passed.
12 complex product preparations: scalar factors and pivot reconstructions passed.
9 entangled pair preparations: closed complex determinant passed.
3 nonadjacent-register preparations: product across one cut, entangled across another.
3 near-product states: nonzero small minors retained; no exact numeric rank certificate.
4 local-unitary Bell transformations: determinant magnitude preserved.
10 malformed contracts rejected before simulation.
43 CPU complex128 circuits passed; exact theorem and numeric diagnostics remain distinct.
```

These bounded numerical checks support the implementation; the general proof is unit 3. There is no native entanglement-classification endpoint claimed here, no finite-shot state reconstruction, no noise model or hardware execution, and no interval arithmetic certificate. Independent scholarly acceptance and reader testing remain pending.

### Understanding checks and transfer exercises

**7.1-A — Meaning of the cut.** For the state in unit 2, list the nonzero coefficient rows for $(q_2,q_0)|(q_1)$ and identify a nonzero minor for $(q_0)|(q_1,q_2)$. Can both statements “product” and “entangled” be correct?

**7.1-B — Derive the factors.** Starting from a nonzero pivot $C_{rs}$, derive normalized factors and explain why the right factor must be normalized for an exact rank-one normalized C. Explain which step fails for rank two. Repeat with a one-by-three coefficient array.

**7.1-C — Fresh implementation.** Prepare q0 in $R_y(-.61)|0\rangle$, apply CX(q0,q3), put phase .92 on q0, and independently prepare q1 and q2 with $R_y(.37)$ and $R_y(-.83)$. Use $A=(q_3,q_0)$, $B=(q_2,q_1)$. Write the two factors in that exact order, check every complex coefficient, then change to $A=(q_0,q_2)$ and $B=(q_3,q_1)$. Predict whether each cut is a product before calculating minors.

**7.1-D — Diagnose a false acceptance.** A report says “the computational distribution factorizes and the vector is allclose to a product, so entanglement is absent.” Give two distinct flaws, one using unit 6 and one using unit 7. State what information a defensible report must retain.

<details markdown="1">
<summary>Answers and verification guidance for 7.1-A–D</summary>

**A.** Only rows 00 and 11 are nonzero for the first cut; they are equal and proportional to $(\cos(\pi/6),\sin(\pi/6))$. For the second cut, columns 00 and 01 have minor $\cos^2(\pi/6)/2=3/8$. The first partition groups the entangled pair within A; the second splits it. The claims refer to different cuts.

**B.** Set $u=C_{:,s}$, $v=C_{r,:}/C_{rs}$, $a=u/\|u\|$, $b=\|u\|v$. Rank one gives $C=uv^{\mathsf T}$, and the norm identity in unit 3 gives $\|b\|=1$. For rank two, a column need not be a multiple of column s, so the reconstruction equality fails. A normalized one-by-three row always has rank one; the same formulas apply and no two-by-two minors exist. Opposite local phase changes preserve the product.

**C.** Write $c=\cos(-.61/2)$, $s=\sin(-.61/2)$ and $|r_t\rangle=\cos(t/2)|0\rangle+\sin(t/2)|1\rangle$. For the first cut,

$$
|a\rangle=c|00\rangle+e^{.92i}s|11\rangle,\qquad
|b\rangle=|r_{-.83}\rangle_{q_2}\otimes|r_{.37}\rangle_{q_1}.
$$

Gather the native vector using that cut and compare it with $ab^{\mathsf T}$, not $ab^\dagger$. The second cut splits the pair q0/q3 and has rank two: its coefficient matrix contains a nonzero minor proportional to $cse^{.92i}$ and nonzero spectator amplitudes. The transfer log records actual runs with this and other fresh parameters; a reader's own run is separate evidence.

**D.** Unit 6 has the same factorized probabilities for a product and an entangled pure vector; phase information is missing. Unit 7 shows that arbitrarily small nonzero entangling amplitudes can pass a chosen closeness test. Retain the pure-state assumption, full complex representation and provenance, declared partition/basis order, precision, tolerance, measured residuals and numerical limitations. If only counts are available, the present theorem cannot classify the unknown state without additional inference assumptions.

</details>

**Source and next step.** The frozen reference is Nielsen and Chuang, *Quantum Computation and Quantum Information*, §2.5, beginning on printed page 109, for the bipartite pure-state/Schmidt setting ([source locator](../references/proof-sources.md)). The rank-one and minors arguments above are supplied in full as original exposition, rather than assumed from that reference. Section 7.2 will construct the Schmidt decomposition and explain the general rank beyond one. No later result is required for this section's theorem.

<!-- end-section-7.1 -->


<span id="sec-entanglement-and-quantum-information-protocols-2"></span>

## 7.2 Schmidt decomposition

Section 7.1 distinguished a product vector from an entangled pure vector across a fixed cut. Schmidt decomposition provides an orthonormal product expansion for **every** finite bipartite pure state and exposes exactly how many such terms are needed. Prerequisites are [2.5, spectral decomposition and singular values](ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-5), and [7.1](#sec-entanglement-and-quantum-information-protocols-1). Depth **F** means full proofs of existence, normalization and local-unitary invariance; the rank, degeneracy and overlap consequences are also proved below.

We retain orthonormal product coordinates and the q0-most-significant convention. Amplitudes, singular values and overlaps are dimensionless; rotation angles are radians. The examples use released FlagQuantum 0.3.1 and PyTorch 2.13.0, CPU complex128, absolute tolerance $10^{-12}$ and relative tolerance zero for deterministic implementation checks. Theorems concern exact finite vectors. Numerical singular-value thresholds and uncertain experimental data require separate interpretation.

The eight Python fragments run cumulatively from the repository root with `requirements-examples.txt`. The actual complete program is [schmidt_decomposition.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/schmidt_decomposition.py). The native prepared amplitudes are checked against analytic references; `torch.linalg.svd` supplies the explicitly classical decomposition. It is not presented as an undocumented FlagQuantum request.

<span id="formula-code-7-2-existence"></span>

### 1. Construct the Schmidt vectors and keep the complex conjugate

**Theorem (finite pure-state Schmidt decomposition).** For a normalized vector in $\mathcal H_A\otimes\mathcal H_B$, with finite dimensions $d_A,d_B$, there are positive real numbers $s_1,\ldots,s_r$ and orthonormal families $\{|a_k\rangle_A\}$ and $\{|b_k\rangle_B\}$ such that

$$
|\psi\rangle=\sum_{k=1}^r s_k|a_k\rangle_A\otimes|b_k\rangle_B,
\qquad 1\le r\le\min(d_A,d_B).
$$

The numbers $s_k$ are the **Schmidt coefficients**, listed in nonincreasing order. They are amplitudes; their squares will be probabilities for a particular matched measurement.

**Construction and full existence proof.** Fix orthonormal product coordinates and write $|\psi\rangle=\sum_{i,j}C_{ij}|i\rangle_A|j\rangle_B$ as in 7.1. By [2.5's finite spectral theorem](ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-5), the positive semidefinite matrix $H=CC^\dagger$ has an orthonormal eigenbasis $u_k$, with eigenvalues $\lambda_k\ge0$. Positivity follows directly from $x^\dagger Hx=\|C^\dagger x\|^2$. For each positive eigenvalue define

$$
s_k=\sqrt{\lambda_k}>0,\qquad v_k=\frac{C^\dagger u_k}{s_k}.
$$

These right vectors are orthonormal, because

$$
v_k^\dagger v_l
=\frac{u_k^\dagger CC^\dagger u_l}{s_ks_l}
=\frac{\lambda_l\delta_{kl}}{s_ks_l}
=\delta_{kl}.
$$

In particular there are at most $d_B$ of them. If $\lambda_k=0$, then $\|C^\dagger u_k\|^2=0$, so $u_k^\dagger C=0$. Expanding the identity in the full left eigenbasis therefore gives

$$
C=\sum_k u_ku_k^\dagger C
=\sum_{\lambda_k>0}s_k u_kv_k^\dagger.
$$

This is precisely the positive part of a singular value decomposition. For each component,

$$
C_{ij}=\sum_{k=1}^r s_k(u_k)_i\overline{(v_k)_j}.
$$

Define $|a_k\rangle=\sum_i(u_k)_i|i\rangle_A$ and $|b_k\rangle=\sum_j\overline{(v_k)_j}|j\rangle_B$. The first family is orthonormal by construction. For the second,

$$
\langle b_k|b_l\rangle
=\sum_j(v_k)_j\overline{(v_l)_j}
=\overline{v_k^\dagger v_l}=\delta_{kl}.
$$

Substituting the component identity reconstructs every amplitude of the claimed Schmidt expansion. At least one coefficient is positive because the original vector is nonzero. This proves existence, with both local orthonormality conditions; no assumed Schmidt theorem is hidden in the construction.

**Formula → code.** In matrix notation $C=U\Sigma V^\dagger$, the B-system columns are $\overline V$. PyTorch returns `U, sigma, Vh`, with `Vh = V.mH`; hence **`B = Vh.T`**, a transpose without conjugation. This yields $C=(U\Sigma)B^{\mathsf T}$. `s.decompose` uses a thin SVD and retains *all* computed singular values, including numerical zeros, for reconstruction. It is explicit classical analysis of an actual FlagQuantum state, not a native Schmidt-decomposition API.

The native two-qubit preparation is $R_y(\theta)$ on q0, CX(q0,q1), phase $P(\phi)$ on q0, then $R_y(\alpha)$ on q0 and $P(\beta)$ on q1. The independent coefficient reference is

$$
C=R_y(\alpha)\operatorname{diag}\!\left(\cos(\theta/2),e^{i\phi}\sin(\theta/2)\right)P(\beta)^{\mathsf T}.
$$

**FlagQuantum code → verification result.** Native preparation and execution are visible here. The coefficient helper validates shape and norm; the SVD, conjugate-basis translation, Gram matrices and reconstruction are explicit below, without phase alignment or input repair.

```python
import math
import torch
import flagquantum as fq
import examples.foundations.schmidt_decomposition as s
import examples.foundations.product_entanglement as e
theta, phi, alpha, beta = .9, .71, .4, .23
circuit = fq.Circuit(2, dtype=s.D)
circuit.ry(0, theta).cx(0, 1).p(0, phi)
circuit.ry(0, alpha).p(1, beta)
result = fq.run(circuit, outputs=[fq.probabilities()], options=s.OPTIONS)
assert result.statevector().shape == (1, 4)
state = result.statevector()[0]
C = e.coefficients(state, (0,), (1,))
assert torch.allclose(C, s.pair_reference(theta, phi, alpha, beta), atol=s.ATOL, rtol=0)
U, sigma, Vh = torch.linalg.svd(C, full_matrices=False)
B = Vh.T
assert torch.allclose(U.mH@U, torch.eye(2, dtype=s.D), atol=s.ATOL, rtol=0)
assert torch.allclose(B.mH@B, torch.eye(2, dtype=s.D), atol=s.ATOL, rtol=0)
assert torch.allclose(C, s.scalar_rebuild(U, sigma, B), atol=s.ATOL, rtol=0)
wrong = (U*sigma)@B.conj().T
assert torch.linalg.vector_norm(C-wrong).item() > .1
print('complex Schmidt reconstruction passed; using V directly failed')
```
```text
complex Schmidt reconstruction passed; using V directly failed
```

<span id="formula-code-7-2-normalization"></span>

### 2. Prove the normalization and distinguish amplitudes from weights

**Formula and derivation.** The inner product of two tensor terms factors:

$$
\langle a_k,b_k|a_l,b_l\rangle
=\langle a_k|a_l\rangle\langle b_k|b_l\rangle
=\delta_{kl}.
$$

Taking the squared norm of the expansion, retaining all cross terms before applying orthogonality, gives

$$
1=\langle\psi|\psi\rangle
=\sum_{k,l}s_ks_l\delta_{kl}
=\sum_{k=1}^r s_k^2.
$$

Thus $p_k=s_k^2$ are nonnegative and sum to one. There is no requirement that $\sum_k s_k=1$. The equivalent coefficient identity is $\|C\|_F^2=\sum_{i,j}|C_{ij}|^2=\sum_k s_k^2$, with $\|\cdot\|_F$ the Frobenius norm. This equality also shows why rescaling an unnormalized input would change the stated problem.

**Code → verification result.** Form the product columns explicitly, check their orthonormal Gram matrix, and reconstruct the complete native state. `torch.kron` receives contiguous vectors so its reference construction does not depend on a noncontiguous SVD column view.

```python
terms = torch.stack([torch.kron(U[:, k].contiguous(), B[:, k].contiguous())
                     for k in range(sigma.numel())], dim=1)
assert torch.allclose(terms.mH@terms, torch.eye(2, dtype=s.D), atol=s.ATOL, rtol=0)
assert torch.allclose(terms@sigma.to(s.D), state, atol=s.ATOL, rtol=0)
assert abs(sigma.square().sum().item()-1) < s.ATOL
print(f'sum of squared Schmidt coefficients = {sigma.square().sum().item():.6f}')
```
```text
sum of squared Schmidt coefficients = 1.000000
```

<span id="formula-code-7-2-rank"></span>

### 3. Prove the relation to entanglement and matched outcomes

**Schmidt rank.** The coefficient matrix satisfies $Cv_k=s_ku_k$. Its column space therefore contains r independent left vectors. Conversely, its SVD expansion makes every column a combination of those r vectors. Both inclusions prove

$$
\operatorname{rank}C=r.
$$

This also proves that r is the **minimum number of product terms** in any expansion, even one using nonorthogonal or unnormalized factors. If $C=\sum_{t=1}^m x_ty_t^{\mathsf T}$, each column lies in $\operatorname{span}\{x_1,\ldots,x_m\}$, so $r\le m$. The Schmidt expansion attains $m=r$.

By 7.1, a normalized pure state is a product exactly when $r=1$. Normalization then forces its single Schmidt coefficient to be one. A pure state is entangled across this cut exactly when $r>1$. A statement about r always names a bipartition; it is not a classification of a mixed-state density operator.

**Matched measurement, derived.** Extend each orthonormal Schmidt family to a full local orthonormal basis. Such completion is possible by repeatedly taking a vector outside the current span, subtracting its orthogonal projections and normalizing the remaining nonzero vector, until the finite dimension is reached. For the matched product measurement,

$$
\langle a_j,b_l|\psi\rangle
=\sum_k s_k\langle a_j|a_k\rangle\langle b_l|b_k\rangle
=s_j\delta_{jl},\qquad p(j,l)=s_j^2\delta_{jl},
$$

with coefficients zero for any added basis directions. Only matching Schmidt labels occur. This statement concerns the specified local bases; measuring an entangled state in an arbitrary basis need not give such a diagonal table.

**FlagQuantum code → verification result.** For this two-qubit example the thin local matrices are already two-by-two unitaries, so applying $U^\dagger$ and $B^\dagger$ turns the state into $s_1|00\rangle+s_2|11\rangle$. We execute those gates and query the entire vector and probabilities. For rectangular matrices a thin factor is an isometry, so it cannot be submitted directly as a square unitary gate without basis completion.

```python
analyzer = s.pair(theta, phi, alpha, beta)
analyzer.unitary(0, unitary=U.mH.contiguous())
analyzer.unitary(1, unitary=B.mH.contiguous())
aligned, probabilities = s.query(analyzer)
expected = torch.diag(sigma.to(s.D)).reshape(-1)
assert torch.allclose(aligned, expected, atol=s.ATOL, rtol=0)
assert torch.allclose(probabilities, expected.abs()**2, atol=s.ATOL, rtol=0)
assert abs(sigma[1].item()-abs(math.sin(theta/2))) < s.ATOL
print('Schmidt-basis readout: only labels 00 and 11; weights equal squared coefficients')
```
```text
Schmidt-basis readout: only labels 00 and 11; weights equal squared coefficients
```

<span id="formula-code-7-2-invariance"></span>

### 4. Prove local-unitary invariance of the entire spectrum

**Formula.** Under local unitaries L and R, 7.1's index expansion gives $C'=LCR^{\mathsf T}$. Because $R^\dagger R=I$, complex conjugation gives $R^{\mathsf T}\overline R=I$. Therefore

$$
C'C'^\dagger
=LC R^{\mathsf T}\overline R C^\dagger L^\dagger
=L(CC^\dagger)L^\dagger.
$$

**Proof and consequence.** If $CC^\dagger u=\lambda u$, then $C'C'^\dagger(Lu)=\lambda Lu$. The invertible map L maps each eigenspace bijectively to the corresponding eigenspace of the new matrix, with inverse $L^\dagger$. Eigenvalues and their multiplicities are unchanged. Their nonnegative square roots are the Schmidt coefficients; hence the entire sorted Schmidt spectrum, and in particular its positive count r, are invariant. Extra zero eigenvalues on the larger subsystem do not add Schmidt terms.

Equivalently, apply L and R to each local Schmidt vector; unitarity preserves orthonormality and leaves the same coefficients in the expansion. Local orthonormal basis changes and internal relabelings are also unitary coordinate changes. They preserve the spectrum for a fixed cut. Moving a qubit from one side of the cut to the other is not covered by this statement.

**FlagQuantum code → verification result.** Both local matrices here are complex; comparison checks every coefficient with $LCR^{\mathsf T}$ and every singular value with the original spectrum. It does not require the newly computed singular vectors to match a particular phase convention.

```python
local_left, local_right = s.phase(-.37)@s.ry(.83), s.ry(-.29)@s.phase(.41)
moved_circuit = s.pair(theta, phi, alpha, beta)
moved_circuit.unitary(0, unitary=local_left).unitary(1, unitary=local_right)
moved, _ = s.query(moved_circuit)
C_moved = e.coefficients(moved, (0,), (1,))
assert torch.allclose(C_moved, local_left@C@local_right.T, atol=s.ATOL, rtol=0)
_, moved_sigma, _ = s.decompose(C_moved)
assert torch.allclose(moved_sigma, sigma, atol=s.ATOL, rtol=0)
print('local unitaries preserve the entire Schmidt spectrum')
```
```text
local unitaries preserve the entire Schmidt spectrum
```

<span id="formula-code-7-2-freedom"></span>

### 5. Explain what is unique and what is free

**Formula and proof.** The sorted positive coefficients are unique because their squares are the positive eigenvalues of $CC^\dagger$, with multiplicity. Individual Schmidt vectors need not be unique. Opposite changes of phase,

$$
|a_k\rangle\longmapsto e^{i\chi_k}|a_k\rangle,
\qquad |b_k\rangle\longmapsto e^{-i\chi_k}|b_k\rangle,
$$

leave their product unchanged. A global phase of the complete state can instead be carried by all A factors; singular values remain positive real numbers.

For a block of equal coefficients s, let A and B collect the corresponding local columns. Its coefficient contribution is $sAB^{\mathsf T}$. For **any unitary** W of the block dimension, choose

$$
A'=AW,\qquad B'=B\overline W.
$$

Both column families remain orthonormal, and

$$
sA'B'^{\mathsf T}
=sAW\overline W^{\mathsf T}B^{\mathsf T}
=sAWW^\dagger B^{\mathsf T}=sAB^{\mathsf T}.
$$

Rotating both blocks by W instead of the conjugate paired rotation is generally wrong for complex W. For a nondegenerate positive coefficient, the corresponding eigenspace of $CC^\dagger$ is one-dimensional, so the A vector is fixed up to phase and its B partner follows from $C^\dagger a_k/s_k$ and conjugation. Zero-coefficient directions contribute no state amplitude and may be completed differently. Nearly equal floating-point coefficients do not automatically justify treating them as an exactly degenerate block.

**FlagQuantum code → verification result.** A phase Bell state has two exactly equal theoretical coefficients $1/\sqrt2$. We deliberately change both local bases with the paired conjugate rotation and compare full complex reconstruction; comparing singular-vector arrays for exact equality would wrongly reject this valid freedom.

```python
bell, _ = s.query(fq.Circuit(2, dtype=s.D).h(0).cx(0, 1).p(0, .67))
C_equal = e.coefficients(bell, (0,), (1,))
A_equal, equal_sigma, B_equal = s.decompose(C_equal)
W = s.phase(.53)@s.ry(.91)
rotated_A, rotated_B = A_equal@W, B_equal@W.conj()
assert torch.linalg.vector_norm(rotated_A-A_equal).item() > .1
assert torch.allclose((rotated_A*equal_sigma)@rotated_B.T, C_equal, atol=s.ATOL, rtol=0)
assert torch.allclose(equal_sigma, torch.full((2,), 1/math.sqrt(2), dtype=torch.float64), atol=s.ATOL, rtol=0)
print('degenerate spectrum: different orthonormal Schmidt bases, same complex state')
```
```text
degenerate spectrum: different orthonormal Schmidt bases, same complex state
```

<span id="formula-code-7-2-overlap"></span>

### 6. Relate the largest coefficient to the best product overlap

**Result.** Among normalized product vectors, the largest squared overlap with $|\psi\rangle$ is $s_1^2$.

**Full derivation.** For normalized $|x\rangle_A,|y\rangle_B$, define $\alpha_k=\langle x|a_k\rangle$ and $\beta_k=\langle y|b_k\rangle$. Orthogonality implies $\sum_k|\alpha_k|^2\le1$: subtract the orthogonal projection of x onto the Schmidt span, whose squared norm is the sum of its squared coefficients; the remainder has nonnegative squared norm. The same argument gives $\sum_k|\beta_k|^2\le1$. Thus the triangle and Cauchy–Schwarz inequalities yield

$$
|\langle x,y|\psi\rangle|
=\left|\sum_k s_k\alpha_k\beta_k\right|
\le s_1\sum_k|\alpha_k||\beta_k|
\le s_1\sqrt{\sum_k|\alpha_k|^2}\sqrt{\sum_k|\beta_k|^2}
\le s_1.
$$

Taking $x=a_1,y=b_1$ attains the upper bound, so it is a maximum, not just an estimate. This gives another exact criterion for product pure states: $s_1=1$ exactly when all remaining coefficients vanish. After optimizing the overall phase of a product vector, its best Euclidean distance from the state is

$$
\min_{x,y,\gamma}\|\psi-e^{i\gamma}x\otimes y\|_2
=\sqrt{2-2s_1},
$$

because the squared distance between two normalized vectors is $2-2\operatorname{Re}\langle\psi|e^{i\gamma}x,y\rangle$, and phase choice maximizes that real part to the overlap modulus. This normalized-product distance is different from simply discarding terms without normalizing the retained vector.

**Code → verification result.** The scalar overlap helper expands every conjugated bra component explicitly. The known maximizing product attains the bound and reproduces the distance formula; a few other trial vectors are implementation checks, not the proof of optimality.

```python
best_a, best_b = U[:, 0], B[:, 0]
best_overlap = abs(s.overlap(C, best_a, best_b))
assert abs(best_overlap-sigma[0].item()) < s.ATOL
best_product = torch.outer(best_a, best_b)
distance_squared = torch.sum((C-best_product).abs()**2).item()
assert abs(distance_squared-(2-2*sigma[0].item())) < s.ATOL
for angle in (.19, .73, 1.31):
    trial_a = torch.tensor([math.cos(angle), 1j*math.sin(angle)], dtype=s.D)
    trial_b = torch.tensor([math.sin(angle), complex(math.cos(.47), math.sin(.47))*math.cos(angle)], dtype=s.D)
    assert abs(s.overlap(C, trial_a, trial_b)) <= best_overlap+s.ATOL
print(f'maximum squared product overlap = {best_overlap**2:.6f}')
```
```text
maximum squared product overlap = 0.810805
```

<span id="formula-code-7-2-cuts"></span>

### 7. Separate a different cut from a different ordering

**Formula and derivation.** For a Bell pair on q0/q2 and a separate q1 state, the cut $A=(q_2,q_0)$, $B=(q_1)$ has

$$
C_{A|B}=ab^{\mathsf T},\quad
 a=\frac{(1,0,0,e^{i\phi})^{\mathsf T}}{\sqrt2},\quad
 b=\left(\cos(\eta/2),\sin(\eta/2)\right)^{\mathsf T}.
$$

Both factors are normalized, so the thin spectrum is $(1,0)$. For the cut $A'=(q_0)$, $B'=(q_1,q_2)$, write instead

$$
|\psi\rangle=\frac{|0\rangle_{q_0}\,|r\rangle_{q_1}|0\rangle_{q_2}
+e^{i\phi}|1\rangle_{q_0}\,|r\rangle_{q_1}|1\rangle_{q_2}}{\sqrt2}.
$$

The two B-side vectors are orthogonal because the last qubit labels are orthogonal; both have norm one because $|r\rangle$ does. Moving the phase into either local family gives a Schmidt expansion with two coefficients $1/\sqrt2$. The spectrum changed because the physical pair was split across the cut. Merely reversing q2/q0 *within* A permutes rows by a unitary matrix and leaves its spectrum unchanged.

**FlagQuantum code → verification result.** Explicit indexed gathering from 7.1 determines the rectangular matrices. No bare reshape is used to change the partition.

```python
three, _ = s.query(fq.Circuit(3, dtype=s.D).h(0).cx(0, 2).p(0, .43).ry(1, .82))
C_grouped = e.coefficients(three, (2, 0), (1,))
C_split = e.coefficients(three, (0,), (1, 2))
_, grouped_sigma, _ = s.decompose(C_grouped)
_, split_sigma, _ = s.decompose(C_split)
assert torch.allclose(grouped_sigma, torch.tensor([1., 0.], dtype=torch.float64), atol=s.ATOL, rtol=0)
assert torch.allclose(split_sigma, torch.full((2,), 1/math.sqrt(2), dtype=torch.float64), atol=s.ATOL, rtol=0)
_, reordered_sigma, _ = s.decompose(e.coefficients(three, (0, 2), (1,)))
assert torch.allclose(reordered_sigma, grouped_sigma, atol=s.ATOL, rtol=0)
print('grouped cut: (1,0); split cut: (1/sqrt(2),1/sqrt(2)); internal reorder unchanged')
```
```text
grouped cut: (1,0); split cut: (1/sqrt(2),1/sqrt(2)); internal reorder unchanged
```

<span id="formula-code-7-2-boundaries"></span>

### 8. Keep the exact theorem separate from numerical resolution

**Formula and derivation.** The exactly specified state

$$
|\psi_\epsilon\rangle=\sqrt{1-\epsilon^2}|00\rangle+\epsilon|11\rangle
\quad(0<\epsilon<1/\sqrt2)
$$

has Schmidt coefficients $(\sqrt{1-\epsilon^2},\epsilon)$ and exact rank two. A numerical report at threshold $\tau>0$ may instead count

$$
r_\tau=\#\{k:\widehat s_k>\tau\}.
$$

This definition is a declared resolution diagnostic on computed numbers $\widehat s_k$, not the exact r of the theorem. If $\epsilon<\tau$, the diagnostic can report one even for this exactly entangled input. Conversely, rounding can give a mathematically zero singular value a tiny nonzero representation. The helper always retains all computed singular values for reconstruction; `resolved_rank` only reports a separate thresholded count.

There is no state normalization repair, zero clipping, automatic degeneracy grouping or interval certificate. The matrix contract is finite CPU complex128, two-dimensional, unit Frobenius norm within $10^{-12}$, and side lengths 1–16; these are book reference guards. Empty, nonfinite, real-dtype and unnormalized arrays are rejected. `coefficients` additionally requires an explicitly ordered qubit bipartition and a pure vector; measurement counts or a density operator are different inputs. For dimension-one subsystems the sole nonzero Schmidt coefficient is one, and no entanglement across that cut is possible.

**Implementation boundary.** Section 7.1's initial tiny-angle failure is retained in [FlagQuantum issue #704](https://github.com/flagos-ai/FlagQuantum/issues/704). A returned zero amplitude at epsilon $10^{-14}$ did not establish that the intended state was a product. Here epsilon $10^{-10}$ uses the native path already verified to retain that amplitude. The installed release remains subject to that boundary. A source repair was merged in [PR #712](https://github.com/flagos-ai/FlagQuantum/pull/712); the [repair ledger](../upstream-fixes.md) distinguishes source validation from merge and release status.

**FlagQuantum code → verification result.** Inspect the small coefficient directly, then compare two explicitly chosen diagnostic thresholds. Both counts describe the same computed vector.

```python
epsilon = 1e-10
tiny, _ = s.query(fq.Circuit(2, dtype=s.D).ry(0, 2*math.asin(epsilon)).cx(0, 1))
_, tiny_sigma, _ = s.decompose(e.coefficients(tiny, (0,), (1,)))
assert abs(tiny_sigma[1].item()-epsilon) < 1e-20
assert s.resolved_rank(tiny_sigma, 1e-9) == 1
assert s.resolved_rank(tiny_sigma, 1e-12) == 2
for bad in [lambda: s.decompose(C*2), lambda: s.decompose(C.real),
            lambda: s.resolved_rank(tiny_sigma, 0)]:
    try:
        bad()
    except ValueError:
        pass
    else:
        raise AssertionError('invalid contract admitted')
print('same nonzero coefficient: 1 resolved at 1e-9, 2 at 1e-12; 3 invalid contracts rejected')
```
```text
same nonzero coefficient: 1 resolved at 1e-9, 2 at 1e-12; 3 invalid contracts rejected
```

### Complete example, verification scope and exercises

```bash
python examples/foundations/schmidt_decomposition.py
python scripts/check_schmidt_decomposition_prose.py
```

The complete program executes 46 native circuits: 12 complex products checked over all ordered cuts, 18 pairs with closed-form spectra, 3 degenerate Bell preparations, 3 nonadjacent-register preparations, 2 near-product cases, 6 actual inverse-basis analyzers and 2 states with identical computational distributions but different Schmidt spectra. Scalar component sums independently check reconstruction; closed coefficients, explicit Gram matrices and predicted matched outcomes check the SVD translation. Ten malformed contracts are rejected. A separate fresh four-qubit transfer run and rectangular mathematical fixtures are recorded in the section evidence.

Expected output of the complete program:

```text
12 native complex products: all ordered cuts reconstruct with one resolved coefficient.
18 complex entangled pairs: closed coefficients, scalar reconstruction and product-overlap checks passed.
3 degenerate Bell spectra: conjugate paired basis rotations reconstruct unchanged states.
3 nonadjacent-register states: spectra depend on the bipartition, not its internal ordering.
2 near-product spectra: all singular values retained; threshold-dependent diagnostics declared.
6 native inverse-basis analyzers: complete amplitudes and matched-label probabilities passed.
2 identical computational distributions: different Schmidt spectra verified.
10 malformed contracts rejected before simulation.
46 CPU complex128 circuits passed; no exact numerical-rank or hardware certificate claimed.
```

Native support used here is circuit preparation, explicit square local unitaries, exact statevector and computational-probability queries. Decomposition, thresholds and overlap analysis are classical postprocessing. The theorem is for a known pure vector and a fixed bipartition; it is not a mixed-state separability test or hardware tomography protocol. Finite examples support implementation correctness but do not substitute for the proofs. Author verification is separate from pending independent mathematical/implementation review and reader trial.

**7.2-A — Translate a complex SVD.** Given $C=U\Sigma V^\dagger$, write the B-system columns and show that their inner products are orthonormal. What is wrong with setting B equal to V for a general complex coefficient matrix? Derive the actual inverse local analyzers in the two-qubit example.

**7.2-B — Rank and minimality.** Prove why no expansion with fewer than r nonorthogonal product terms can reproduce a state of Schmidt rank r. Does the count of strictly positive floating-point singular values necessarily equal r?

**7.2-C — Fresh ordered-register implementation.** Prepare q0 with $R_y(-.61)$, apply CX(q0,q3) and phase .92 on q0, and put q1 and q2 in independent $R_y(.37)$ and $R_y(-.83)$ states. Predict the sorted spectra for $(q_3,q_0)|(q_2,q_1)$ and $(q_0,q_2)|(q_3,q_1)$. Check the full complex native vector, gathered coefficient matrices and reconstructions. Compare spectra rather than arbitrary SVD vector phases.

**7.2-D — Degeneracy and distance.** For the phase Bell state, choose a complex two-by-two unitary W and derive the paired transformations that leave the state unchanged. Calculate its maximal squared product overlap and best phase-optimized normalized-product distance. Explain how the conclusions differ for a product state.

<details markdown="1">
<summary>Answers and verification guidance for 7.2-A–D</summary>

**A.** The B columns are $\overline V$, so if PyTorch returns Vh, use `B = Vh.T`. Their Gram matrix is $V^{\mathsf T}\overline V=\overline{V^\dagger V}=I$. Using V directly reconstructs $U\Sigma V^{\mathsf T}$, which generally differs from C. The actual analyzers are $U^\dagger$ and $B^\dagger=V^{\mathsf T}$; their transformed coefficient matrix is

$$
U^\dagger C\,(B^\dagger)^{\mathsf T}
=U^\dagger C\overline B=\Sigma.
$$

This gate submission requires square unitaries, which both factors are for the two-qubit example; thin rectangular factors require completion first.

**B.** In an m-term product expansion, every coefficient column lies in the span of its m left factors. Thus rank is at most m. The r-term Schmidt expansion attains that lower bound. Floating-point SVD can round a zero away from zero or fail to resolve a small positive value; a declared threshold describes numerical resolution, not the exact theorem.

**C.** The first cut groups the whole q0/q3 pair on one side and the two spectator qubits on the other. Its thin spectrum is $(1,0,0,0)$. The second splits the pair; spectators are normalized local factors and do not change its positive coefficients. Its thin spectrum is

$$
\left(\cos(.61/2),\sin(.61/2),0,0\right).
$$

The negative sine in the preparation and the .92 phase belong to local Schmidt vectors; the coefficients themselves are nonnegative. Gather using the declared tuple orders, retaining every singular value in reconstruction. Native execution plus independent bit-index amplitudes and these analytic spectra are recorded in the transfer test.

**D.** With coefficient contribution $sAB^{\mathsf T}$, choose $A'=AW$, $B'=B\overline W$, yielding $sA'B'^{\mathsf T}=sAB^{\mathsf T}$. Both Bell coefficients are $1/\sqrt2$, so its maximum squared product overlap is $1/2$ and its minimum normalized-product distance is $\sqrt{2-\sqrt2}$. A product state has coefficient one, overlap one and distance zero. Degenerate bases may change while these numerical invariants stay fixed.

</details>

**Source and transition.** The frozen reference is Nielsen and Chuang, *Quantum Computation and Quantum Information*, §2.5, beginning on printed page 109 ([NC:2.5 source locator](../references/proof-sources.md#source-nc-2-5)). This section supplies its own complete finite proof from the previously proved spectral theorem; no third-party text or unsolved exercise is used as a missing proof step. Section 7.3 will use Bell states and basis changes for explicit information protocols.

<!-- end-section-7.2 -->


<span id="sec-entanglement-and-quantum-information-protocols-3"></span>

## 7.3 Bell states and basis changes

Two entangled qubits can form an orthonormal basis for their entire four-dimensional state space. The **Bell basis** is useful only if its names, phases, circuit ordering and classical output labels agree. We derive those agreements here, including the difference between transforming a vector, expressing it in another basis and measuring in that basis.

Prerequisites are [5.2, controlled operations](ch-gates-reversible-computation-and-circuit-synthesis.md#sec-gates-reversible-computation-and-circuit-synthesis-2), [6.2, conditional states and ignored outcomes](ch-measurement-expectation-values-and-statistical-estimation.md#sec-measurement-expectation-values-and-statistical-estimation-2), and [7.1, pure-state products](#sec-entanglement-and-quantum-information-protocols-1). The proofs have depth **F**: all four vectors, their orthonormality and the preparation/analysis inverse are derived. Section 7.2 is compatible with these examples but its Schmidt theorem is not needed for the proofs below.

Our full computational order is $|q_0q_1\rangle=(|00\rangle,|01\rangle,|10\rangle,|11\rangle)$, with q0 most significant. Angles are radians; amplitudes and probabilities are dimensionless. Deterministic checks use CPU complex128, absolute tolerance $10^{-12}$ and relative tolerance zero, on FlagQuantum 0.3.1 and PyTorch 2.13.0. The eight Python blocks run cumulatively from the repository root. The [complete program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/bell_basis.py) uses native gates, exact queries and terminal samples; all projector-based conditional-state calculations are explicitly classical ideal-update models.

<span id="formula-code-7-3-vectors"></span>

### 1. Define the four vectors and prove that they form a basis

**Formula.** Let $a,b\in\{0,1\}$, and define addition modulo two by $\oplus$. Our phase-fixed convention is

$$
|\beta_{ab}\rangle=\frac{|0,b\rangle+(-1)^a|1,b\oplus1\rangle}{\sqrt2}.
$$

The first label a is the **phase bit**, specifying the relative sign. The second label b is the **parity bit**, specifying even or odd computational parity. The label ab is a Bell-basis coordinate label, not a claim that the two physical qubits are in the product state $|ab\rangle$.

| Bell label ab | Name | Phase-fixed vector | Nonzero computational outcomes |
| --- | --- | --- | --- |
| 00 | $\Phi^+$ | $(\lvert00\rangle+\lvert11\rangle)/\sqrt2$ | 00, 11, each with probability 1/2 |
| 01 | $\Psi^+$ | $(\lvert01\rangle+\lvert10\rangle)/\sqrt2$ | 01, 10, each with probability 1/2 |
| 10 | $\Phi^-$ | $(\lvert00\rangle-\lvert11\rangle)/\sqrt2$ | 00, 11, each with probability 1/2 |
| 11 | $\Psi^-$ | $(\lvert01\rangle-\lvert10\rangle)/\sqrt2$ | 01, 10, each with probability 1/2 |

**Full orthonormality proof.** Terms with different first computational bits have zero inner product. The remaining terms give

$$
\langle\beta_{ab}|\beta_{a'b'}\rangle
=\frac{\delta_{bb'}}{2}\left(1+(-1)^{a+a'}\right)
=\delta_{aa'}\delta_{bb'}.
$$

The middle factor is one when $a=a'$ and zero otherwise. Thus all four vectors have norm one and are mutually orthogonal. Four orthonormal vectors in dimension four span the whole space: their independent columns form an invertible square matrix. They therefore constitute a basis.

They are also all entangled across q0|q1. For b=0 the coefficient matrix is diagonal with entries $1/\sqrt2$ and $(-1)^a/\sqrt2$, giving determinant $(-1)^a/2$. For b=1 it is off-diagonal with those entries, giving determinant $-(-1)^a/2$. Thus all four determinants are $(-1)^{a+b}/2$, which are nonzero; 7.1's exact product criterion applies. Computational probabilities distinguish the even and odd pairs, but cannot distinguish the plus and minus states within a pair.

**FlagQuantum code → verification result.** The four reference columns are written explicitly, independently of a circuit implementation. The first actual preparation checks the full vector and its computational probabilities, retaining the chosen sign convention.

```python
import math
import torch
import flagquantum as fq
import examples.foundations.bell_basis as t
vectors = [torch.tensor(v, dtype=t.D)/math.sqrt(2) for v in
           ([1,0,0,1], [0,1,1,0], [1,0,0,-1], [0,1,-1,0])]
B = torch.stack(vectors, dim=1)
assert torch.allclose(B.mH@B, torch.eye(4, dtype=t.D), atol=t.ATOL, rtol=0)
phi_plus = fq.Circuit(2, dtype=t.D).h(0).cx(0, 1)
result = fq.run(phi_plus, outputs=[fq.probabilities()], options=t.OPTIONS)
assert torch.allclose(result.statevector()[0], vectors[0], atol=t.ATOL, rtol=0)
assert torch.allclose(result.probabilities[0], torch.tensor([.5,0,0,.5], dtype=torch.float64), atol=t.ATOL, rtol=0)
print('Bell columns 00:Phi+, 01:Psi+, 10:Phi-, 11:Psi-; Gram matrix I4')
```
```text
Bell columns 00:Phi+, 01:Psi+, 10:Phi-, 11:Psi-; Gram matrix I4
```

<span id="formula-code-7-3-preparation"></span>

### 2. Derive every preparation and track Pauli ordering

**Formula and derivation.** The Hadamard action on either computational bit is

$$
H|a\rangle=\frac{|0\rangle+(-1)^a|1\rangle}{\sqrt2}.
$$

Controlled-X maps $|x,y\rangle$ to $|x,y\oplus x\rangle$, so applying H on q0 and then CX(q0,q1) gives

$$
|ab\rangle\ \longmapsto
\frac{|0,b\rangle+(-1)^a|1,b\rangle}{\sqrt2}
\ \longmapsto\ |\beta_{ab}\rangle.
$$

Starting from $|00\rangle$, set the input bits with $X_0^aX_1^b$, then execute H and CX in that order. This one construction derives all four phase-fixed states, rather than memorizing four unrelated circuits.

An alternative starts with $|\Phi^+\rangle$ and uses

$$
|\beta_{ab}\rangle=(Z_0^a X_1^b)|\Phi^+\rangle
=(I\otimes X^bZ^a)|\Phi^+\rangle.
$$

The first equality follows because $Z_0$ changes the $|1,\cdot\rangle$ branch sign and $X_1$ flips its second bit. For the second equality, execute $Z_1^a$ **before** $X_1^b$; this first changes the $|11\rangle$ sign and then flips the second qubit. Reversing these two right-side calls gives

$$
(I\otimes Z^aX^b)|\Phi^+\rangle=(-1)^{ab}|\beta_{ab}\rangle,
$$

because $ZX=-XZ$. In the a=b=1 case this changes the full vector by minus one. That global sign does not change probabilities of this isolated prepared state, but it differs from the phase-fixed vector above and must be tracked in coherent operator compositions. We do not silently align it away.

**FlagQuantum code → verification result.** The loop shows actual X/H/CX calls for every label. The two extra preparations expose the right-side ordering sign while verifying the identical computational probabilities.

```python
for a in (0, 1):
    for b in (0, 1):
        circuit = fq.Circuit(2, dtype=t.D)
        if a: circuit.x(0)
        if b: circuit.x(1)
        circuit.h(0).cx(0, 1)
        prepared = t.query(circuit)
        assert torch.allclose(prepared['state'], vectors[2*a+b], atol=t.ATOL, rtol=0)
right_zx = t.query(fq.Circuit(2, dtype=t.D).h(0).cx(0, 1).z(1).x(1))
right_xz = t.query(fq.Circuit(2, dtype=t.D).h(0).cx(0, 1).x(1).z(1))
assert torch.allclose(right_zx['state'], vectors[3], atol=t.ATOL, rtol=0)
assert torch.allclose(right_xz['state'], -vectors[3], atol=t.ATOL, rtol=0)
assert torch.allclose(right_zx['probabilities'], right_xz['probabilities'], atol=t.ATOL, rtol=0)
print('four phase-fixed preparations passed; swapping right-side X/Z gives minus Psi-')
```
```text
four phase-fixed preparations passed; swapping right-side X/Z gives minus Psi-
```

<span id="formula-code-7-3-transform"></span>

### 3. Derive the encoder matrix and its inverse

**Formula.** Let $U_B$ have the Bell vectors as columns in the declared label order $(00,01,10,11)$:

$$
U_B=\frac1{\sqrt2}
\begin{pmatrix}
1&0&1&0\\
0&1&0&1\\
0&1&0&-1\\
1&0&-1&0
\end{pmatrix}
=\mathrm{CX}_{0\to1}(H\otimes I).
$$

**Derivation.** Unit 2 computed the image of each computational basis column. Placing those images side by side gives this matrix, so it implements the map on every superposition by linearity. Orthonormal columns imply $U_B^\dagger U_B=I$. Because this is square, its inverse is $U_B^\dagger$. Taking the adjoint of the product reverses its factors. Both H and CX are self-inverse Hermitian gates, hence

$$
U_B^\dagger=(H\otimes I)\mathrm{CX}_{0\to1}.
$$

The encoder's **chronological calls** are H then CX. The decoder's calls are CX then H. Matrix products act on column vectors from the right, so the written matrix order is the reverse of those chronological lists. In particular $U_B|ab\rangle=|\beta_{ab}\rangle$ and $U_B^\dagger|\beta_{ab}\rangle=|ab\rangle$ with the exact phase conventions already fixed.

There are two distinct uses of this matrix. Physically applying $U_B$ changes an input state vector z to $U_Bz$. Expressing an unchanged physical state $|\psi\rangle$ in Bell coordinates instead gives $c=U_B^\dagger\psi$. Executing the decoder physically maps that state to a computational-coordinate vector whose entries equal c. This connection is how a basis-coordinate calculation becomes a readout circuit.

**FlagQuantum code → verification result.** A complex input, independently derived from scalar amplitudes, checks both the forward map and its coherent roundtrip. This is not a measurement between the two transformations.

```python
encoder = fq.Circuit(2, dtype=t.D).h(0).cx(0, 1)
decoder = fq.Circuit(2, dtype=t.D).cx(0, 1).h(0)
def make_input(theta=.9, phi=.71, eta=.37, lam=-.42):
    return fq.Circuit(2, dtype=t.D).ry(0, theta).p(0, phi).ry(1, eta).p(1, lam).cx(0, 1)
reference = t.scalar_preparation(.9, .71, .37, -.42)
encoded = t.query(make_input().compose(encoder))
restored = t.query(make_input().compose(encoder).compose(decoder))
assert torch.allclose(encoded['state'], B@reference, atol=t.ATOL, rtol=0)
assert torch.allclose(restored['state'], reference, atol=t.ATOL, rtol=0)
assert torch.allclose(B.mH@B, torch.eye(4, dtype=t.D), atol=t.ATOL, rtol=0)
print('H then CX encodes; CX then H decodes; full complex roundtrip passed')
```
```text
H then CX encodes; CX then H decodes; full complex roundtrip passed
```

<span id="formula-code-7-3-coordinates"></span>

### 4. Translate arbitrary complex amplitudes into Bell probabilities

**Formula and derivation.** For a normalized input

$$
|\psi\rangle=x|00\rangle+y|01\rangle+z|10\rangle+w|11\rangle,
$$

multiply by the four Bell bras to obtain

$$
\begin{pmatrix}c_{00}\\c_{01}\\c_{10}\\c_{11}\end{pmatrix}
=U_B^\dagger\psi
=\frac1{\sqrt2}\begin{pmatrix}x+w\\y+z\\x-w\\y-z\end{pmatrix}.
$$

For example $\langle\Phi^-|\psi\rangle=(x-w)/\sqrt2$. The Bell basis vectors happen to have real entries in this convention; the bra still means a conjugate transpose. The input amplitudes remain complex. The inverse expansion $|\psi\rangle=\sum_{a,b}c_{ab}|\beta_{ab}\rangle$ follows from $U_BU_B^\dagger=I$.

If the decoder is followed by computational readout, the Born probabilities are

$$
p(a,b)=|c_{ab}|^2=\langle\psi|P_{ab}|\psi\rangle,
\qquad P_{ab}=|\beta_{ab}\rangle\langle\beta_{ab}|.
$$

Indeed the effective projector is $U_B|ab\rangle\langle ab|U_B^\dagger=P_{ab}$. The four projectors sum to identity by completeness, so the probabilities sum to one. These equations apply to any normalized pure input, not only to a prepared Bell vector.

A useful phase-sensitive special case is $\cos(\theta/2)|00\rangle+e^{i\phi}\sin(\theta/2)|11\rangle$. Only labels 00 and 10 occur, with

$$
p(00)=\frac{1+\sin\theta\cos\phi}{2},\qquad
p(10)=\frac{1-\sin\theta\cos\phi}{2}.
$$

This follows by expanding the squared moduli of $(\cos(\theta/2)\pm e^{i\phi}\sin(\theta/2))/\sqrt2$. The original computational probabilities do not contain φ; the Bell analyzer makes that relative phase observable.

**FlagQuantum code → verification result.** The scalar preparation reference and four direct sum/difference expressions are independent of the native decoder. Compare the entire complex analyzed vector before comparing its squared moduli.

```python
args = (math.pi/3, .71, .83, -.42)
source = t.query(make_input(*args))
psi = t.scalar_preparation(*args)
assert torch.allclose(source['state'], psi, atol=t.ATOL, rtol=0)
x, y, z, w = psi
bell_coefficients = torch.stack([x+w, y+z, x-w, y-z])/math.sqrt(2)
analyzed = t.query(make_input(*args).cx(0, 1).h(0))
assert torch.allclose(bell_coefficients, B.mH@psi, atol=t.ATOL, rtol=0)
assert torch.allclose(analyzed['state'], bell_coefficients, atol=t.ATOL, rtol=0)
assert torch.allclose(analyzed['probabilities'], bell_coefficients.abs()**2, atol=t.ATOL, rtol=0)
print('Bell probabilities [00,01,10,11] =', [round(p, 6) for p in analyzed['probabilities'].tolist()])
```
```text
Bell probabilities [00,01,10,11] = [0.693717, 0.134663, 0.143721, 0.027899]
```

<span id="formula-code-7-3-samples"></span>

### 5. Read the Bell label and distinguish a probability from a record

**Formula and derivation.** On a Bell input, the decoder gives $|ab\rangle$, so

$$
p(a',b'\mid\beta_{ab})=\delta_{aa'}\delta_{bb'}.
$$

Reading columns `(q0,q1)` therefore reports the phase bit followed by the parity bit. Integer histogram index $j=2a+b$ uses that same order. Without the decoder, the computational measurement distinguishes only b and loses the sign information a; its two possible full bit strings occur with probability one half.

For a general input, an N-shot terminal record consists of pairs $(a_t,b_t)$, and its histogram is

$$
n_{ab}=\sum_{t=1}^N\mathbf1[(a_t,b_t)=(a,b)],\qquad
\widehat p_{ab}=n_{ab}/N.
$$

The observed frequencies need not equal the exact probabilities for a finite random record. Native samples here are terminal computational samples after the actual decoder gates. They are not a returned state after a selected mid-circuit Bell measurement. In the helper's actual request, the calls are `fq.probabilities(qubits=(0,1))` and `fq.samples(qubits=(0,1))`, with an explicit shot count and seed; the API and integer-column checks follow 6.6.

**FlagQuantum code → verification result.** Four decoded Bell inputs produce one deterministic label each in these runs. The general complex input checks raw count reconstruction without asserting that random frequencies equal their theoretical values.

```python
bell_counts = []
for a in (0, 1):
    for b in (0, 1):
        readout = t.query(t.preparation(a, b).cx(0, 1).h(0), shots=32, seed=23)
        assert readout['bits'].tolist() == [[a, b]]*32
        bell_counts.append(readout['counts'].tolist())
from dataclasses import replace
sampled_result = fq.run(make_input(*args).cx(0, 1).h(0), outputs=[
    fq.probabilities(qubits=(0,1)), fq.samples(qubits=(0,1))],
    shots=64, options=replace(t.OPTIONS, seed=31))
sampled_bits = sampled_result.samples[0]
assert sampled_bits.shape == (64,2) and sampled_bits.dtype == torch.int64
manual = [sampled_bits.tolist().count([j//2,j%2]) for j in range(4)]
assert t.histogram(sampled_bits).tolist() == manual and sum(manual) == 64
assert torch.allclose(sampled_result.probabilities[0], bell_coefficients.abs()**2, atol=t.ATOL, rtol=0)
print('32-shot counts for four Bell inputs =', bell_counts)
print('complex-input 64-shot raw-count accounting passed; no exact frequency-equality assertion')
```
```text
32-shot counts for four Bell inputs = [[32, 0, 0, 0], [0, 32, 0, 0], [0, 0, 32, 0], [0, 0, 0, 32]]
complex-input 64-shot raw-count accounting passed; no exact frequency-equality assertion
```

<span id="formula-code-7-3-pauli"></span>

### 6. Identify the same basis through two commuting Pauli products

**Formula.** Here $XX=X\otimes X$ flips both bits, and $ZZ=Z\otimes Z$ assigns their parity sign:

$$
XX=\begin{pmatrix}0&0&0&1\\0&0&1&0\\0&1&0&0\\1&0&0&0\end{pmatrix},
\qquad ZZ=\operatorname{diag}(1,-1,-1,1).
$$

**Derivation.** The two computational terms of $\beta_{ab}$ both have parity b, so $ZZ|\beta_{ab}\rangle=(-1)^b|\beta_{ab}\rangle$. Flipping both bits swaps those two terms:

$$
XX|\beta_{ab}\rangle
=\frac{|1,b\oplus1\rangle+(-1)^a|0,b\rangle}{\sqrt2}
=(-1)^a|\beta_{ab}\rangle.
$$

Also $XX\,ZZ=ZZ\,XX$, because $XZ=-ZX$ on each factor introduces two minus signs. Each product squares to identity. The four pairs of eigenvalues $( (-1)^a,(-1)^b )$ are distinct. They label the same orthonormal basis, so

$$
P_{ab}=\frac14\left(I+(-1)^aXX\right)\left(I+(-1)^bZZ\right).
$$

To prove this identity, apply the right side to each Bell vector $\beta_{a'b'}$: its eigenvalue is $\frac14(1+(-1)^{a+a'})(1+(-1)^{b+b'})$, one for the matching label and zero otherwise. Since the four Bell vectors are a basis, the two operators agree on every vector. This derives the joint projectors without assuming a joint-measurement theorem for noncommuting operators.

**FlagQuantum code → verification result.** Exact native Pauli expectation requests verify the eigenvalue signs. These are expectation values on a declared prepared input, not four sampled Bell labels inferred from an arbitrary state's two means. For a general input, two means alone do not specify the full four-outcome distribution.

```python
I4 = torch.eye(4, dtype=t.D)
assert torch.allclose(t.XX@t.ZZ, t.ZZ@t.XX, atol=t.ATOL, rtol=0)
eigenlabels = []
for a in (0, 1):
    for b in (0, 1):
        project = (I4+(-1)**a*t.XX)@(I4+(-1)**b*t.ZZ)/4
        assert torch.allclose(project, torch.outer(vectors[2*a+b], vectors[2*a+b].conj()), atol=t.ATOL, rtol=0)
        result = fq.run(t.preparation(a, b), outputs=[
            fq.expectation(fq.X(0)@fq.X(1), name='xx'),
            fq.expectation(fq.Z(0)@fq.Z(1), name='zz')], options=t.OPTIONS)
        xx = float(result.expectation('xx')[0])
        zz = float(result.expectation('zz')[0])
        assert abs(xx-(-1)**a) < t.ATOL and abs(zz-(-1)**b) < t.ATOL
        eigenlabels.append((round(xx), round(zz)))
print('Bell (XX,ZZ) eigenvalues =', eigenlabels)
```
```text
Bell (XX,ZZ) eigenvalues = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
```

<span id="formula-code-7-3-branches"></span>

### 7. Separate decoding, selecting an outcome and ignoring its record

**Formula and derivation.** For an ideal projective **Bell measurement**, assume 6.2's Lüders update. A selected label with $p_{ab}=|c_{ab}|^2>0$ has conditional state

$$
|\psi_{ab}\rangle
=\frac{P_{ab}|\psi\rangle}{\sqrt{p_{ab}}}
=\frac{c_{ab}}{|c_{ab}|}|\beta_{ab}\rangle.
$$

Its amplitude phase is retained. There is no normalized conditional vector for a zero-probability label. Applying the decoder alone instead gives the coherent vector $\sum_{ab}c_{ab}|ab\rangle$; applying the encoder immediately after it restores $|\psi\rangle$. If an ideal computational projection selects ab between those unitaries, the selected decoded vector is $(c_{ab}/|c_{ab}|)|ab\rangle$, and re-encoding gives the conditional Bell vector above. In this last case the computational readout qubits must remain available to re-encode; the terminal query used in our examples does not model such an endpoint.

If the Bell outcome is ignored, later event probabilities are sums over the conditional alternatives, not probabilities of an averaged statevector:

$$
p(E\mid\text{ignored Bell outcome})
=\sum_{ab:p_{ab}>0}p_{ab}\langle\psi_{ab}|E|\psi_{ab}\rangle.
$$

For an explicit difference, $|00\rangle=(|\Phi^+\rangle+|\Phi^-\rangle)/\sqrt2$. Coherent decode/encode returns $|00\rangle$, giving computational outcome 00 with probability one. An ideal Bell measurement with its outcome ignored instead gives the two Bell alternatives with probabilities one half each. Each alternative gives computational 00 with probability one half, so the later probability is one half. The lost relative coherence is what changes the result.

**Code → verification result.** Conditional branches and the ignored-record sum are classical postprocessing under the stated ideal-update assumption. The actual native circuit below checks only the coherent unitary roundtrip. We do not submit nonunitary Bell projectors as unitary gates or claim native sampled collapse/reset.

```python
for j, (p, branch) in enumerate(t.branches(psi)):
    if p:
        expected_branch = (bell_coefficients[j]/abs(bell_coefficients[j]))*vectors[j]
        assert torch.allclose(branch, expected_branch, atol=t.ATOL, rtol=0)
        assert abs(torch.vdot(branch, branch).item()-1) < t.ATOL
zero = torch.tensor([1,0,0,0], dtype=t.D)
coherent = t.query(fq.Circuit(2, dtype=t.D).cx(0, 1).h(0).h(0).cx(0, 1))
assert torch.allclose(coherent['state'], zero, atol=t.ATOL, rtol=0)
ignored_probability_00 = sum(p*abs(branch[0].item())**2 for p, branch in t.branches(zero) if p)
assert abs(ignored_probability_00-.5) < t.ATOL
print(f'p(00): coherent decode/encode = {coherent["probabilities"][0].item():.6f}, ignored Bell outcome = {ignored_probability_00:.6f}')
```
```text
p(00): coherent decode/encode = 1.000000, ignored Bell outcome = 0.500000
```

<span id="formula-code-7-3-boundaries"></span>

### 8. Preserve output order, full-vector phase and implementation limits

**Formula and derivation.** Changing the ordered pair changes which output column represents each role. Swapping the two physical qubits in a Bell vector gives

$$
\mathrm{SWAP}|\beta_{ab}\rangle=(-1)^{ab}|\beta_{ab}\rangle.
$$

For b=0 both terms are 00 or 11 and are unchanged. For b=1 the two terms exchange places, producing the sign $(-1)^a$. These two cases prove the formula, including the antisymmetry of $\Psi^-$. Consequently, analyzing an original q0/q1 Bell input with the **reversed** decoder, CX(q1,q0) then H(q1), gives

$$
(-1)^{ab}|b\rangle_{q_0}|a\rangle_{q_1}.
$$

To derive it, regard the input in ordered coordinates `(q1,q0)`: it is $(-1)^{ab}\beta_{ab}$, and the matching decoder maps it to $(-1)^{ab}|ab\rangle$ in that order. A native query with columns `(q1,q0)` therefore still reports `(a,b)`. Querying `(q0,q1)` would report `(b,a)`. Test asymmetric labels 01 and 10; 00 and 11 cannot expose this ordering mistake. The singlet's minus sign affects the full vector but does not alter its decoded bit probabilities.

**Contract and limits.** The book helpers require literal bits, two distinct ordered qubit positions, normalized finite CPU complex128 pure vectors and nonempty int64 two-column sample records. They do not guess a Bell naming convention, infer which bit is phase, renormalize input or discard a full-vector phase. Dense reference helpers use two to four qubits as a teaching guard, not a FlagQuantum capacity limit. Native support demonstrated is ideal H/CX/X/Z and unitary gates, exact expectations/probabilities and terminal samples; a hardware platform's ability to implement a complete Bell measurement requires its own gate/readout support. Classical ideal branches are a separate model.

**FlagQuantum code → verification result.** Reverse the actual control/target and the native sample-column order together. Then verify the full signed vector independently of the output record. Malformed input is rejected before another circuit runs.

```python
for a, b in ((0,1), (1,0), (1,1)):
    reversed_readout = t.query(t.preparation(a, b).cx(1, 0).h(1), pair=(1,0), shots=13)
    expected = torch.zeros(4, dtype=t.D)
    expected[2*b+a] = (-1)**(a*b)
    assert torch.allclose(reversed_readout['state'], expected, atol=t.ATOL, rtol=0)
    assert reversed_readout['bits'].tolist() == [[a,b]]*13
for bad in [lambda: t.bell_vector(True,0), lambda: t.support(2,(0,0)),
            lambda: t.histogram(torch.tensor([[0,2]],dtype=torch.int64))]:
    try:
        bad()
    except ValueError:
        pass
    else:
        raise AssertionError('invalid Bell contract admitted')
print('reversed output columns (q1,q0) still report (a,b); full-vector singlet sign retained')
print('3 malformed contracts rejected before simulation')
```
```text
reversed output columns (q1,q0) still report (a,b); full-vector singlet sign retained
3 malformed contracts rejected before simulation
```

### Complete program and independent verification

```bash
python examples/foundations/bell_basis.py
python scripts/check_bell_basis_prose.py
```

The complete program executes 94 native circuits: 20 phase-fixed/alternative preparations and decoded Bell readouts; 30 complex-basis, branch-reference and raw-sample checks; 8 analytic phase-sensitive readouts; 4 reversed analyzers; and 32 nonadjacent-register preparations/readouts with complex spectator amplitudes. References use explicit Bell columns, scalar amplitude formulas, sum/difference coordinates and Pauli projector matrices. Twelve malformed contracts are rejected before simulation. The body checker executes the actual cumulative fragments and compares exact printed outputs, then checks the complete program output. A separate transfer run uses fresh four-qubit ordered supports and complex Bell coefficients.

Expected output of the complete program:

```text
20 native Bell preparations/readouts: four vectors,Pauli eigenlabels,32-shot labels and Pauli-order phases passed.
30 native complex-basis queries: scalar amplitudes,encoder/inverse,phase-preserving branches and raw-count accounting passed.
8 phase-sensitive Bell readouts: analytic interference probabilities passed.
4 reversed ordered analyzers:raw columns(a,b),full basis(b,a) and singlet minus sign passed.
32 nonadjacent ordered-register queries:scalar spectator amplitudes and all four decoded labels passed.
12 malformed contracts rejected before simulation.
94 CPUcomplex128 native circuits passed;terminal readout distinct from assumed conditional projection.
```

These are bounded author checks, not a substitute for the proofs or for independent scholarly review. No accidental phase alignment, probability clipping, state normalization repair, hardware execution or native mid-circuit conditional-state claim is used.

### Understanding checks and transfer exercises

**7.3-A — Prepare and name the state.** Starting from 00, derive the result of X(q0), X(q1), H(q0), CX(q0,q1) in chronological order. Give its Bell label, its full phase-fixed vector and its raw computational probabilities. Repeat using Z(q1) then X(q1) after preparing $\Phi^+$, and explain the sign change if those two calls are reversed.

**7.3-B — Translate an arbitrary vector.** Derive the Bell coordinates and probabilities of $(|00\rangle+i|11\rangle)/\sqrt2$. Compare its computational and Bell distributions with those of $\Phi^+$ and $\Phi^-$. Is a single deterministic Bell label guaranteed for every entangled state?

**7.3-C — Fresh nonadjacent experiment.** In a four-qubit register, use ordered pair `(q3,q0)`. Prepare $\cos(.83/2)|00\rangle+e^{-.92i}\sin(.83/2)|11\rangle$ on that pair with Ry(q3,.83), CX(q3,q0), P(q3,-.92). Put q1 and q2 into independent complex states using Ry(.37), P(.21) and Ry(-.69), P(.43), respectively. Derive the Bell probabilities in output order `(q3,q0)`, run CX(q3,q0) then H(q3), and verify full amplitudes as well as terminal record accounting. State what happens if the output columns are reversed without changing the decoder.

**7.3-D — Update and information.** Derive both conditional Bell branches for the input 00, then compute the probability of later computational 00 if the Bell outcome is forgotten. Compare with an uninterrupted decode/encode circuit. Why is the vector returned by a terminal statevector query not evidence that native outcome-conditioned collapse occurred?

<details markdown="1">
<summary>Answers and verification guidance for 7.3-A–D</summary>

**A.** The input bits are a=b=1, so the result is $\beta_{11}=\Psi^-=(|01\rangle-|10\rangle)/\sqrt2$, with computational probabilities $(0,1/2,1/2,0)$. Preparing $\Phi^+$ then executing Z(q1), X(q1) gives that exact vector. X(q1), Z(q1) gives its negative because $ZX=-XZ$. Raw probabilities alone cannot expose that sign difference.

**B.** The Bell coefficients, in label order 00,01,10,11, are $((1+i)/2,0,(1-i)/2,0)$. Thus the Bell probabilities are $(1/2,0,1/2,0)$. All three even Bell-family inputs mentioned have computational probabilities $(1/2,0,0,1/2)$; $\Phi^+$ decodes deterministically to 00 and $\Phi^-$ to 10, whereas the phase-i input does not. Entanglement does not imply membership in this particular Bell basis.

**C.** With $\theta=.83,\phi=-.92$, the ordered decoder probabilities are

$$
\left(\frac{1+\sin\theta\cos\phi}{2},\ 0,\
\frac{1-\sin\theta\cos\phi}{2},\ 0\right).
$$

The spectator factors multiply the full amplitudes but do not change this two-qubit marginal. Reversing only the output columns moves the nonzero 10 probability to 01. Full-vector checks use the global q0q1q2q3 order, even when the requested sample columns are q3,q0. The exact printed parameters and fresh variants are run in the separate transfer evidence; finite random frequencies are checked for correct reconstruction, not exact equality to these probabilities.

**D.** For input 00, both 00 and 10 Bell labels have probability one half. Their positive-real coefficients give the conditional vectors $\Phi^+$ and $\Phi^-$ without extra phase. The ignored result gives later computational 00 with probability $\frac12\frac12+\frac12\frac12=\frac12$. The coherent inverse/forward circuit gives probability one. Native terminal samples plus an accompanying simulation statevector do not define or demonstrate a selected mid-circuit state-update interface; the conditional branches here were computed classically under an explicit ideal projective assumption.

</details>

**Source and transition.** The frozen source is Nielsen and Chuang, *Quantum Computation and Quantum Information*, §1.3.6, “Example: Bell states,” beginning on printed page 25 ([NC:1.3.6 locator](../references/proof-sources.md#source-nc-1-3-6)). The phase/label convention and all derivations are stated locally; examples and answer explanations are original. Section 7.4 will use these states to distinguish quantum correlations from classical assumptions in the CHSH experiment.

<!-- end-section-7.3 -->

<span id="sec-entanglement-and-quantum-information-protocols-4"></span>
## 7.4 Correlations and the CHSH experiment

**Question.** Can correlations between two qubits be explained by shared randomness and local responses to independently chosen measurement settings? A large correlation alone does not answer that question. Two classical copies of a random bit are perfectly correlated. CHSH combines four different measurement contexts into one testable restriction.

**Entry and scope.** Import the spectral expectation identity from [6.3](ch-measurement-expectation-values-and-statistical-estimation.md#sec-measurement-expectation-values-and-statistical-estimation-3), independent-group variance addition from [6.7](ch-measurement-expectation-values-and-statistical-estimation.md#sec-measurement-expectation-values-and-statistical-estimation-7), and the phase-fixed Bell state from [7.3](#sec-entanglement-and-quantum-information-protocols-3). The finite-probability reasoning and conservative interval below are also spelled out locally. The depth is **F**: prove the classical bound under explicit assumptions and calculate a quantum violation. This section does not promise a loophole-free experiment, an optimal-measurement search or a proof of the general quantum CHSH maximum.

The complete program is [chsh_experiment.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/chsh_experiment.py). Run the following Python fragments cumulatively from the repository root in the existing examples environment. All angles are in radians. Examples use released FlagQuantum 0.3.1 and PyTorch 2.13.0, CPU complex128, absolute implementation tolerance $10^{-12}$ and zero relative tolerance. The previously recorded 0.3.1 limitations and safeguards remain in place; a source merge is not a package-release validation.

### 7.4.1 — Define the local model before calculating its bound

**Formula.** Alice chooses a setting $x\in\{0,1\}$ and Bob chooses $y\in\{0,1\}$. Their recorded bits are $u,v\in\{0,1\}$. Assign numerical outcomes $a=(-1)^u$ and $b=(-1)^v$, each in $\{-1,+1\}$. The settings are choices of apparatus; they are not extra qubits or measured outcome bits. Define

$$
E_{xy}=\mathbb E[ab\mid x,y],
\qquad S=E_{00}+E_{01}+E_{10}-E_{11}.
$$

Specify a shared hidden variable $\lambda$ with normalized probability measure $\mu$. The local model assumes, for every setting pair,

$$
p(u,v\mid x,y)=
\int p_A(u\mid x,\lambda)\,p_B(v\mid y,\lambda)\,d\mu(\lambda).
$$

This expression includes two separate restrictions. **Local factorization** says Alice's conditional response does not depend on Bob's setting and conversely, once $\lambda$ is given. **Measurement independence** says the same $\mu$ applies to all four choices; it is not a different distribution selected by $(x,y)$. Each response is normalized over the complete pair of possible outcomes. Dropping an outcome or retaining different subsets for different settings can invalidate this model for the retained data. These are assumptions to test or justify in a physical application, not facts proved by a simulator.

**Derivation: stochastic responses.** Introduce conditional means

$$
A_x(\lambda)=\sum_{u=0}^1(-1)^u p_A(u\mid x,\lambda),
\qquad
B_y(\lambda)=\sum_{v=0}^1(-1)^v p_B(v\mid y,\lambda).
$$

Normalization and positivity imply $-1\leq A_x,B_y\leq1$. Summing the factorized joint probabilities gives $E_{xy}=\int A_x B_y\,d\mu$. For a fixed $\lambda$, the integrand of $S$ is

$$
s(\lambda)=A_0(B_0+B_1)+A_1(B_0-B_1).
$$

The triangle inequality and the bounds on $A_0,A_1$ give

$$
\begin{aligned}
\lvert s(\lambda)\rvert
&\leq \lvert B_0+B_1\rvert+\lvert B_0-B_1\rvert\\
&=2\max(\lvert B_0\rvert,\lvert B_1\rvert)\leq2 .
\end{aligned}
$$

To justify the middle equality, first suppose $\lvert B_0\rvert\geq\lvert B_1\rvert$. The two quantities $B_0+B_1$ and $B_0-B_1$ have the sign of $B_0$, allowing zero, so their absolute values add to $2\lvert B_0\rvert$. Exchanging the labels covers the other case. Integration now proves the full scoped result:

$$
\lvert S\rvert
=\left\lvert\int s(\lambda)\,d\mu(\lambda)\right\rvert
\leq\int\lvert s(\lambda)\rvert\,d\mu(\lambda)
\leq2.
$$

No independence between trials is needed for this algebraic ensemble bound. Independence will enter our later, narrower statistical calculation. For deterministic responses $A_0,A_1,B_0,B_1\in\{-1,+1\}$, one of $B_0+B_1,B_0-B_1$ is zero and the other is $\pm2$, so $s$ is exactly $\pm2$. Shared randomness only averages these conditional values.

**Code → verification result.** The finite helper represents one setting-independent distribution and two local response means per party. Exhausting the 16 deterministic assignments checks a finite special case; the conditioning proof above covers arbitrary stochastic responses and continuous $\lambda$.

<!-- formula-code: chsh-7-4-local-model -->
```python
import math
import itertools
import torch
import flagquantum as fq
from dataclasses import replace
from examples.foundations import chsh_experiment as t

scores = [t.chsh(t.classical_correlations([1.], [a], [b]))
          for a in itertools.product((-1, 1), repeat=2)
          for b in itertools.product((-1, 1), repeat=2)]
assert set(scores) == {-2., 2.}
e_local = t.classical_correlations([.25, .75],
                                 [(.2, -.4), (.8, .1)],
                                 [(-.3, .6), (.7, -.2)])
assert abs(t.chsh(e_local)) <= 2
print('16 deterministic strategies: S is -2 or +2; stochastic mixture obeys the same bound')
```
```text
16 deterministic strategies: S is -2 or +2; stochastic mixture obeys the same bound
```

### 7.4.2 — What the Bell pair actually correlates

**Formula.** Prepare the Bell state already defined in 7.3:

$$
\lvert\Phi^+\rangle
=\frac{\lvert00\rangle+\lvert11\rangle}{\sqrt2}.
$$

In the full statevector, q0 is the most significant qubit and q1 is the least significant qubit. A and B below act on Alice's and Bob's distinct qubits, respectively.

**Derivation.** Applying $X\otimes X$ exchanges the two nonzero basis components, leaving this vector unchanged. Applying $Z\otimes Z$ multiplies each component by $+1$. In contrast,

$$
\begin{aligned}
(X\otimes Z)\lvert\Phi^+\rangle
&=(\lvert10\rangle-\lvert01\rangle)/\sqrt2,\\
(Z\otimes X)\lvert\Phi^+\rangle
&=(\lvert01\rangle-\lvert10\rangle)/\sqrt2.
\end{aligned}
$$

Both resulting vectors are orthogonal to $\lvert\Phi^+\rangle$, because they have support only on 01 and 10. Therefore

$$
\langle X\otimes X\rangle=1,\quad
\langle Z\otimes Z\rangle=1,\quad
\langle X\otimes Z\rangle=\langle Z\otimes X\rangle=0.
$$

Computational-basis probabilities alone give $(1/2,0,0,1/2)$. They establish a Z correlation, but do not establish an X correlation or a CHSH violation. For example, a classical source emitting 00 or 11 with equal probabilities has the same Z statistics. Our calculation must include other bases.

**FlagQuantum code → verification result.** H(q0) then CX(q0,q1) is the actual preparation; the native Pauli expectation requests directly test all four correlations. The accompanying full-vector comparison retains the phase convention.

<!-- formula-code: chsh-7-4-bell-correlations -->
```python
bell = fq.Circuit(2, dtype=torch.complex128).h(0).cx(0, 1)
bell_result = fq.run(bell, outputs=[
    fq.expectation(fq.X(0)@fq.X(1), name='xx'),
    fq.expectation(fq.Z(0)@fq.Z(1), name='zz'),
    fq.expectation(fq.X(0)@fq.Z(1), name='xz'),
    fq.expectation(fq.Z(0)@fq.X(1), name='zx')], options=t.OPTIONS)
t.RUNS += 1
phi = torch.tensor([1, 0, 0, 1], dtype=t.D)/math.sqrt(2)
assert torch.allclose(bell_result.statevector()[0], phi, atol=t.ATOL, rtol=0)
correlations = [float(bell_result.expectation(name)[0]) for name in ('xx','zz','xz','zx')]
assert all(abs(a-b) < t.ATOL for a,b in zip(correlations, (1,1,0,0)))
print('Phi+: XX=1, ZZ=1, XZ=0, ZX=0; full phase-fixed vector verified')
```
```text
Phi+: XX=1, ZZ=1, XZ=0, ZX=0; full phase-fixed vector verified
```

### 7.4.3 — Translate a measurement direction into a gate call

**Formula.** In the X–Z plane define a dichotomic observable

$$
A(\alpha)=\cos\alpha\, Z+\sin\alpha\, X
=\begin{pmatrix}
\cos\alpha&\sin\alpha\\
\sin\alpha&-\cos\alpha
\end{pmatrix}.
$$

Because $Z^2=X^2=I$ and $ZX+XZ=0$, squaring gives $A(\alpha)^2=I$. It is Hermitian, so the outcome values are $\pm1$. Bob's $B(\beta)$ has the same form on his qubit. Their projectors are $(I+(-1)^u A)/2$ and $(I+(-1)^v B)/2$.

**Derivation: the sign and the angle.** Let $U_\alpha=R_y(-\alpha)$. Its explicit matrix and the effective measured observable are

$$
U_\alpha=
\begin{pmatrix}
\cos(\alpha/2)&\sin(\alpha/2)\\
-\sin(\alpha/2)&\cos(\alpha/2)
\end{pmatrix},
\qquad
U_\alpha^\dagger ZU_\alpha=A(\alpha).
$$

For example, with $c=\cos(\alpha/2)$ and $s=\sin(\alpha/2)$, multiplication gives diagonal entries $c^2-s^2$ and $s^2-c^2$, and off-diagonal entries $2cs$. The half-angle identities give the matrix above. Thus a Z readout after **Ry of minus the observable angle** implements the requested measurement. The gate's matrix contains half-angles; that does not mean the gate call should use $-\alpha/2$.

Expand the product observable and use 7.4.2:

$$
\begin{aligned}
E(\alpha,\beta)
&=\cos\alpha\cos\beta\,\langle Z\otimes Z\rangle
+\sin\alpha\sin\beta\,\langle X\otimes X\rangle\\
&\quad+\cos\alpha\sin\beta\,\langle Z\otimes X\rangle
+\sin\alpha\cos\beta\,\langle X\otimes Z\rangle\\
&=\cos\alpha\cos\beta+\sin\alpha\sin\beta
=\cos(\alpha-\beta).
\end{aligned}
$$

Each local mean is zero on this Bell pair: $Z\otimes I$ gives opposite signs on 00 and 11, while $X\otimes I$ moves to the orthogonal odd subspace; Bob's calculation has the same two steps. Expanding the joint projectors therefore gives

$$
p(u,v\mid\alpha,\beta)
=\frac{1+(-1)^{u+v}\cos(\alpha-\beta)}4.
$$

**FlagQuantum code → verification result.** Both analyzer gates and the actual native run are visible below. Requested probabilities are in ordered label sequence 00,01,10,11 for columns (q0,q1). The book's independent checks use explicit scalar amplitudes and projector matrices, rather than asking the native gate implementation to verify itself.

<!-- formula-code: chsh-7-4-analyzers -->
```python
alpha, beta = 0., math.pi/4
analyzer = (fq.Circuit(2, dtype=t.D).h(0).cx(0, 1)
            .ry(0, -alpha).ry(1, -beta))
readout = fq.run(analyzer, outputs=[fq.probabilities(qubits=(0, 1)),
    fq.expectation(fq.Z(0)@fq.Z(1), name='zz')], options=t.OPTIONS)
t.RUNS += 1
expected_e, expected_p = t.analytic(alpha, beta)
assert torch.allclose(readout.probabilities[0], expected_p, atol=t.ATOL, rtol=0)
assert torch.allclose(readout.probabilities[0], t.matrix_probabilities(alpha,beta), atol=t.ATOL, rtol=0)
assert torch.allclose(readout.statevector()[0], t.scalar_state(alpha,beta,math.pi/2,0.,2,(0,1)), atol=t.ATOL, rtol=0)
print('p(00,01,10,11) =', ' '.join(f'{p:.9f}' for p in readout.probabilities[0]))
print(f'native ZZ after analyzers = {float(readout.expectation("zz")[0]):.9f}')
```
```text
p(00,01,10,11) = 0.426776695 0.073223305 0.073223305 0.426776695
native ZZ after analyzers = 0.707106781
```

### 7.4.4 — Four contexts, one signed combination

**Formula.** Choose Alice's angles $\alpha_0=0,\alpha_1=\pi/2$ and Bob's angles $\beta_0=\pi/4,\beta_1=-\pi/4$. The labels 00,01,10,11 in $E_{xy}$ now refer to **settings**, not to the outcome labels of the previous joint probability vector.

**Derivation.** Substituting each pair into $\cos(\alpha_x-\beta_y)$ gives, in setting order,

$$
(E_{00},E_{01},E_{10},E_{11})
=\frac1{\sqrt2}(1,1,1,-1).
$$

The last sign in the definition of $S$ is also negative, so all four contributions to $S$ are positive:

$$
S=\frac{1+1+1-(-1)}{\sqrt2}=2\sqrt2>2.
$$

An operator check reaches the same result. The chosen directions give $A_0=Z,A_1=X$, $B_0=(Z+X)/\sqrt2$ and $B_1=(Z-X)/\sqrt2$. Hence

$$
A_0\otimes(B_0+B_1)+A_1\otimes(B_0-B_1)
=\sqrt2(Z\otimes Z+X\otimes X),
$$

whose expectation on $\Phi^+$ is $2\sqrt2$. The incompatible A settings have no simultaneous outcome in this circuit model; different settings use fresh preparations. The local model's bound concerns a common distribution of local responses. It is not a constraint that quantum theory imposes on the four separately measured contexts.

As a related interpretation, suppose the settings are uniform and the winning rule is $u\mathbin{\oplus}v=xy$. The event indicator is $(1+(-1)^{xy}ab)/2$. Averaging over four settings yields

$$
p_{\rm win}=\frac12+\frac S8.
$$

Thus the classical upper bound gives $p_{\rm win}\leq3/4$, while this quantum construction gives $(2+\sqrt2)/4$. This is another expression of this experiment's signed correlations, not an additional simulation claim.

**FlagQuantum code → verification result.** Four fresh analyzer circuits produce the deterministic exact probabilities and expectations. The complete program additionally compares these analyzer results to native pre-analyzer requests for $A_x\otimes B_y$.

<!-- formula-code: chsh-7-4-quantum-value -->
```python
quartet = [t.run_setting(a,b) for a,b in t.SETTINGS]
exact = [r['correlation'] for r in quartet]
s_exact = t.chsh(exact)
assert abs(s_exact-2*math.sqrt(2)) < t.ATOL
print('E00,E01,E10,E11 =', ' '.join(f'{e:.9f}' for e in exact))
print(f'S = {s_exact:.9f}; uniform CHSH-game win probability = {.5+s_exact/8:.9f}')
```
```text
E00,E01,E10,E11 = 0.707106781 0.707106781 0.707106781 -0.707106781
S = 2.828427125; uniform CHSH-game win probability = 0.853553391
```

### 7.4.5 — From two bits to a correlation estimate

**Formula.** For a fixed setting pair collect $N$ complete two-bit records. If $n_{uv}$ denotes the count of outcome label $uv$, then

$$
\widehat E_{xy}
=\frac1N\sum_{k=1}^N(-1)^{u_k+v_k}
=\frac{n_{00}-n_{01}-n_{10}+n_{11}}N,
\qquad \sum_{u,v}n_{uv}=N.
$$

**Derivation.** Equal bits have product sign +1; different bits have product sign −1. Grouping the record sum into these four mutually exclusive outcome labels gives the count formula. Every row contributes exactly once. A bit XOR therefore becomes the numerical product score through $1-2(u\mathbin{\oplus}v)$, not through an unsigned bit sum. With a common target distribution in each setting, linearity of expectation gives $\mathbb E[\widehat E_{xy}]=E_{xy}$ and $\mathbb E[\widehat S]=S$.

The first axis of the native sample tensor is the execution batch; the second enumerates records; the third has the explicitly requested qubit columns. It has shape (1,N,2). Do not confuse execution-batch axes, record positions, setting labels and qubit indices. Each record belongs to one setting pair; pooling the four data sets destroys this correspondence.

**FlagQuantum code → verification result.** The helper appends an actual <code>fq.samples(qubits=pair)</code> request to <code>fq.run</code>, with a positive fixed shot count and a recorded seed. It checks the native shape, exact binary record accounting and agreement of the two empirical formulas. It does not require random frequencies to equal exact probabilities. The printed values below are one executed, seeded example in the pinned environment, not a platform-independent random sequence.

<!-- formula-code: chsh-7-4-samples -->
```python
shots = 4096
records = [t.run_setting(a,b,shots=shots,seed=71+j)
           for j,(a,b) in enumerate(t.SETTINGS)]
means = []
for report in records:
    counts, mean = t.sample_statistics(report['bits'], shots)
    assert int(counts.sum()) == shots
    means.append(mean)
print('four complete batches: 4096 two-column records per setting')
print('sample correlations =', ' '.join(f'{e:.6f}' for e in means))
```
```text
four complete batches: 4096 two-column records per setting
sample correlations = 0.701660 0.710938 0.714844 -0.709473
```

### 7.4.6 — State what the error bars assume

**Formula.** For this calculation assume independent, identically prepared ±1 records within each of the four settings, and independent batches across settings, each of fixed size $N\geq2$. These are sampling-model assumptions. Write $Q_{xy,k}=(-1)^{u_k+v_k}$. Then

$$
\operatorname{Var}(Q_{xy,k})=1-E_{xy}^2,
\qquad
\operatorname{Var}(\widehat S)
=\frac1N\sum_{x,y}(1-E_{xy}^2)\leq\frac4N.
$$

**Derivation.** A ±1 variable has $Q^2=1$, giving the first identity from $\operatorname{Var}(Q)=\mathbb E[Q^2]-\mathbb E[Q]^2$. Expanding the centered sum of N records gives N diagonal variance terms. The off-diagonal terms vanish by independence. Different setting batches have zero covariance under the stated assumption, so the variance of their signed sum is the sum of their variances; the signs square to one. For the ideal Bell quartet each $E_{xy}^2=1/2$, giving the sharper model value $2/N$.

The ordinary sample variance for these scores is

$$
s_{xy}^2=\frac{N}{N-1}(1-\widehat E_{xy}^{\,2}),
\qquad
\widehat{\rm SE}(\widehat S)
=\sqrt{\sum_{x,y}\frac{s_{xy}^2}{N}}
=\sqrt{\sum_{x,y}\frac{1-\widehat E_{xy}^{\,2}}{N-1}}.
$$

To obtain the numerator of $s^2$, expand $\sum_k(Q_k-\widehat E)^2$ and use $\sum_kQ_k=N\widehat E$ and $\sum_kQ_k^2=N$. This gives $N(1-\widehat E^2)$. The estimated SE is useful, but it is not by itself a confidence interval.

For a conservative interval, apply the elementary bound to $W=(\widehat S-S)^2\geq0$: since $W\geq r^2$ on the event $W\geq r^2$, $\mathbb E[W]\geq r^2\Pr(W\geq r^2)$. Unbiasedness and the variance bound therefore give

$$
\Pr(\lvert\widehat S-S\rvert\geq r)\leq\frac4{Nr^2}.
$$

For a chosen error probability $0<\delta<1$, set $r=\sqrt{4/(N\delta)}$. This yields a confidence interval $[\widehat S-r,\widehat S+r]$ with coverage at least $1-\delta$ under the stated model. If its lower endpoint exceeds 2, that is evidence against the local-model upper bound **conditional on all these modeling and sampling assumptions**. It is not a loophole-free physical certification. A covered interval is not guaranteed for every realized random sample, and repeated sampling until a favorable interval appears changes this fixed-budget guarantee.

**Code → verification result.** The code reports the estimated SE and the separate conservative radius. The radius uses a proved population bound, not an observed zero variance or a fitted Gaussian quantile. No probabilistic interval-membership event is used as a deterministic implementation acceptance criterion.

<!-- formula-code: chsh-7-4-uncertainty -->
```python
s_hat = t.chsh(means)
se, radius = t.uncertainty(means, shots, delta=.05)
assert abs(radius-math.sqrt(4/(shots*.05))) < t.ATOL
print(f'S_hat = {s_hat:.6f}; estimated SE = {se:.6f}')
print(f'95% conservative radius = {radius:.6f}; lower endpoint = {s_hat-radius:.6f}')
print('interval coverage is a model guarantee, not a deterministic check on each random sample')
```
```text
S_hat = 2.836914; estimated SE = 0.022033
95% conservative radius = 0.139754; lower endpoint = 2.697160
interval coverage is a model guarantee, not a deterministic check on each random sample
```

### 7.4.7 — Diagnose signs and outcome-dependent selection

**Formula and derivation: wrong analyzer sign.** Calling Ry(+β) on Bob implements $B(-\beta)$, not $B(\beta)$. For the Bell state the four requested correlations become $(1,1,-1,1)/\sqrt2$ and their CHSH combination is zero. The two tests with $\alpha=0$ still agree with the intended probabilities, because cosine is even. Testing only those contexts would miss the error.

**Formula and derivation: discarded records.** Now retain only equal-bit records for settings 00,01,10 and only different-bit records for setting 11. The retained-data correlations are exactly

$$
(\widehat E_{00},\widehat E_{01},\widehat E_{10},\widehat E_{11})_{\rm kept}
=(1,1,1,-1),
\qquad \widehat S_{\rm kept}=4.
$$

Each retained row has been selected precisely because its score has the desired sign. This is conditional selection, not the original complete experiment. The denominators shrink differently; the four distributions have changed. A large number calculated this way does not establish stronger quantum correlations. The example below performs this global, setting-dependent data manipulation deliberately so that the failure is inspectable.

**FlagQuantum code → verification result.** Four actual wrong-sign circuits reproduce the predicted zero. Postselection operates on the already generated native records. The fixed-budget input contract rejects those shortened records. That contract catches this form of discarding; it does not authenticate provenance or detect every possible fabricated record.

<!-- formula-code: chsh-7-4-failure-diagnosis -->
```python
wrong_sign = [t.run_setting(a,-b)['correlation'] for a,b in t.SETTINGS]
assert abs(t.chsh(wrong_sign)) < t.ATOL
kept = [r['bits'][(r['bits'][:,0]^r['bits'][:,1]) == (j == 3)]
        for j,r in enumerate(records)]
fake = t.chsh([t.sample_statistics(bits,len(bits))[1] for bits in kept])
assert fake == 4
try:
    t.histogram(kept[0],shots)
except ValueError:
    pass
else:
    raise AssertionError('outcome-selected records accepted as the complete fixed-budget experiment')
print('wrong Bob analyzer sign: S=0; outcome-selected records: apparent S=4')
print('fixed-budget contract rejects discarded records; postselection changes the experiment')
```
```text
wrong Bob analyzer sign: S=0; outcome-selected records: apparent S=4
fixed-budget contract rejects discarded records; postselection changes the experiment
```

### 7.4.8 — Generalize the state, keep the conventions

**Formula.** Consider a normalized even-parity family, with real $\theta,\phi$:

$$
\lvert\psi_{\theta,\phi}\rangle
=\cos(\theta/2)\lvert00\rangle
+e^{i\phi}\sin(\theta/2)\lvert11\rangle.
$$

**Derivation.** ZZ has eigenvalue +1 on each component. XX exchanges the components, so its expectation is
$2\cos(\theta/2)\sin(\theta/2)\cos\phi=\sin\theta\cos\phi$.
The XZ and ZX expectations still vanish. The local Z mean is
$\cos^2(\theta/2)-\sin^2(\theta/2)=\cos\theta$ and the local X mean is zero. Expanding the same product projectors gives

$$
\begin{aligned}
E(\alpha,\beta)
&=\cos\alpha\cos\beta+\sin\theta\cos\phi\,\sin\alpha\sin\beta,\\
p(u,v\mid\alpha,\beta)
&=\frac14\bigl[
1+(-1)^u\cos\theta\cos\alpha
+(-1)^v\cos\theta\cos\beta\\
&\hspace{23mm}+(-1)^{u+v}E(\alpha,\beta)\bigr].
\end{aligned}
$$

Summing over Bob's two outcomes cancels every term containing $(-1)^v$:

$$
p_A(u\mid\alpha,\beta)
=\frac{1+(-1)^u\cos\theta\cos\alpha}{2}.
$$

The result does not depend on β. This model therefore has setting-independent local marginals even when its joint correlations violate CHSH. No signaling through these local outcome probabilities follows from the calculation; it does not restore the local factorized explanation ruled out by $S>2$.

For this family and our fixed quartet,

$$
S_{\theta,\phi}=\sqrt2(1+\sin\theta\cos\phi).
$$

At $\theta=\pi/2,\phi=\pi$, the state is $\Phi^-$, still entangled by 7.1 or 7.2, but this quartet gives zero. Not observing a violation for a fixed choice of measurement directions does not prove a state is a product. At $\theta=0$, the state is 00 and this quartet gives $\sqrt2$, below the classical bound.

**FlagQuantum code → verification result.** In an ordered pair (q3,q0), probability rows refer to q3 and columns to q0. Spectator qubits are in independently prepared complex states; the scalar full-vector reference includes their factors. Testing an unequal local-marginal example matters: the parity score itself is invariant under exchanging the two recorded columns, so a Bell-pair correlation alone cannot calibrate their ordering.

<!-- formula-code: chsh-7-4-general-state -->
```python
theta, phase, alpha = .83, -.49, .23
marginals = []
for beta in (-.91, .47):
    r = t.run_setting(alpha,beta,theta,phase,n=4,pair=(3,0))
    p = r['probabilities'].reshape(2,2)  # rows q3, columns q0
    marginals.append(float(p[0].sum()))
expected = (1+math.cos(theta)*math.cos(alpha))/2
assert all(abs(x-expected) < t.ATOL for x in marginals)
phase_flipped = [t.run_setting(a,b,phase=math.pi)['correlation'] for a,b in t.SETTINGS]
assert abs(t.chsh(phase_flipped)) < t.ATOL
print(f'ordered pair (q3,q0): Alice p(0)={expected:.9f} for both Bob settings')
print('Phi- is entangled but gives S=0 for this fixed measurement quartet')
```
```text
ordered pair (q3,q0): Alice p(0)=0.828551924 for both Bob settings
Phi- is entangled but gives S=0 for this fixed measurement quartet
```

**Contracts and implementation boundary.** The book helper accepts finite real radian angles, two distinct explicitly ordered qubits in a two-to-four-qubit teaching register, positive literal shot counts, nonnegative seeds, and complete CPU int64 two-column binary records. It rejects nonfinite or Boolean angles, duplicate qubits, malformed records, missing records, unnormalized hidden distributions and local response means outside [−1,1]. The register-size guard bounds the dense independent reference; it is not a FlagQuantum capacity limit.

Native features demonstrated are Ry/P/H/CX preparation and analyzer gates, Pauli-sum/product expectation requests, exact ordered probabilities and terminal samples. The full reference retains complex phases and every probability without phase alignment, input normalization repair, probability clipping or backend fallback. No native Bell-test service, hardware timing, locality enforcement, random setting generator, sampled mid-circuit collapse, detector-loss model or device-independent significance test is implied. A single classical computer simulating four settings does not establish experimental separation, setting independence, detector completeness, absence of drift or an adversary-resistant sampling guarantee.

### Complete program and independent verification

Run:

~~~bash
python examples/foundations/chsh_experiment.py
python scripts/check_chsh_experiment_prose.py
~~~

The complete program executes **117 actual native circuits**: 25 compare five pure-state families using direct native observables and four analyzer settings; 72 cover every ordered pair in three- and four-qubit registers with complex spectators; four produce complete fixed-budget sample batches; 12 calibrate basis-state output columns; and four deliberately use Bob's wrong analyzer sign. Thirteen malformed contracts are rejected before any additional native execution.

Independent references are explicit projector matrices, scalar post-analyzer amplitudes, the derived correlation/probability formulas and exact record-count identities. A separate transfer run uses fresh states, settings and nonadjacent ordered supports. Finite tests validate these implementations; they do not replace the classical conditioning proof.

Expected output of the complete program:

```text
16 deterministic local strategies and one stochastic mixture: classical bound passed.
25 native circuits: five state families, direct observables and four analyzer settings agree.
72 native circuits: all ordered pairs in three/four qubits, complex spectators and indexed amplitudes passed.
4 native fixed-budget batches: raw records/counts/scores passed; SE and conservative radius kept separate.
12 native basis calibrations: ordered output columns and bit-to-sign convention passed.
4 wrong-sign analyzer circuits and postselection-to-S=4 expose distinct failure modes;13 malformed contracts rejected.
117 CPU complex128 native circuits passed; simulation is not a loophole-free Bell experiment.
```

### Understanding checks and transfer exercises

**7.4-A — Where the assumption enters.** Let λ contain two bits, and suppose a source could set λ=(x,y) after learning both settings. Construct deterministic responses producing $u=0,v=xy$. Which displayed local-model assumption fails? Why does the resulting S=4 not contradict the theorem?

**7.4-B — Track the two meanings of 01.** For settings x=0,y=1, list the four possible outcome labels, their product signs and their ideal Bell probabilities. Explain why swapping the two qubit output columns leaves the parity correlation unchanged even though it changes the names of asymmetric outcomes. Propose a calibration that detects the swap.

**7.4-C — Fresh formula-to-code experiment.** In a four-qubit register use ordered pair (q3,q1). Prepare the even-parity family with θ=.73, φ=−.39 using Ry(q3,θ), CX(q3,q1), P(q3,φ). Put q0 into Ry(.31), P(−.17), and q2 into Ry(.93), P(−.51), matching the helper's explicit spectator convention. Use the four angles of 7.4.4. Derive all four correlations, S and Alice's marginal for each setting. Run both the full-vector reference and ordered probability checks. Predict the result if φ is increased by π without changing the analyzers.

**7.4-D — Choose a fixed budget.** Under the sampling assumptions of 7.4.6, find an integer N per setting sufficient for a conservative radius at most .1 at δ=.05. Compare with treating one estimated SE as a 95% radius. Explain why collecting samples until the lower endpoint exceeds 2 is outside the fixed-N proof.

<details markdown="1">
<summary>Answers and verification guidance for 7.4-A–D</summary>

**A.** Alice always outputs 0. Bob uses x stored inside λ and his local y to output xy. The distribution of λ now depends on the actual settings, so there is no setting-independent μ. Conditional local response notation alone does not save measurement independence. This is a constructed violation of a hypothesis, not a counterexample to the bound.

**B.** Bob's angle is −π/4 and Alice's is zero, so $E_{01}=1/\sqrt2$. Outcome labels 00 and 11 have product +1 and probability $(1+1/\sqrt2)/4$ each. Labels 01 and 10 have product −1 and probability $(1-1/\sqrt2)/4$ each. Exchanging the columns exchanges 01 and 10 but not their sign, so this parity statistic cannot expose the swap. Prepare a known asymmetric basis state, such as Alice=0 and Bob=1, and require every ordered record to be 01; the complete program includes this calibration in both pair orders.

**C.** Define $k=\sin(.73)\cos(.39)$. The setting-ordered correlations are $(1,1,k,-k)/\sqrt2$, and $S=\sqrt2(1+k)$. Alice's probability of bit zero is $(1+\cos(.73))/2$ for x=0 and one half for x=1, independently of Bob's setting. Bob's local probability is $(1+\cos(.73)/\sqrt2)/2$ for both of his chosen angles, so the local records distinguish the ordered columns. The complex spectator factors multiply amplitudes and disappear when their normalized probabilities are summed. Increasing φ by π reverses k; the predicted S becomes $\sqrt2(1-k)$. The exact printed parameters are executed in the separate transfer evidence; the proof does not depend on a numerical approximation to k.

**D.** Require $4/(N\delta)\leq .1^2$, giving $N\geq8000$ per setting, or 32000 total records. An estimated SE is a plug-in dispersion summary; multiplying or interpreting it as a confidence radius requires further justification and does not follow from its name. Stopping when an endpoint looks favorable changes the event being bounded. The displayed Chebyshev proof controls a preselected fixed-N estimator; no sequential-test guarantee has been derived.

</details>

**Sources and transition.** The frozen textbook locator is Nielsen and Chuang, *Quantum Computation and Quantum Information*, §2.6, “EPR and the Bell inequality,” beginning on printed page 111 ([NC:2.6 locator](../references/proof-sources.md#source-nc-2-6)). The classical-game and measurement-angle conventions were cross-checked against the publicly accessible [IBM Quantum Learning CHSH lesson](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/chsh-game); its state-vector angle convention must be translated to the observable-angle convention used here. Historical attribution is Clauser, Horne, Shimony and Holt, [*Physical Review Letters* 23, 880 (1969)](https://doi.org/10.1103/PhysRevLett.23.880), whose publisher lists an [erratum](https://doi.org/10.1103/PhysRevLett.24.549). The proofs, examples and answers above are local original derivations, not a claim to reproduce the photon proposal or its detection assumptions. Section 7.5 will use Bell pairs as a resource in a communication protocol.

<!-- end-section-7.4 -->

<span id="sec-entanglement-and-quantum-information-protocols-5"></span>

## 7.5 Teleportation, branch by branch

Teleportation transfers an unknown qubit state using a shared Bell pair, local operations and two classical bits. Correctness concerns **every measurement outcome**, including the phase convention. We will derive all four branches, identify the information Bob needs and prove that the protocol preserves entanglement with an untouched reference.

The prerequisites are [6.2, conditional states and ignored outcomes](ch-measurement-expectation-values-and-statistical-estimation.md#sec-measurement-expectation-values-and-statistical-estimation-2), and [7.3, Bell states and basis changes](#sec-entanglement-and-quantum-information-protocols-3). Depth **F** requires the complete expansion and correction proof. Assume ideal gates, a normalized pure input and the ideal projective update of 6.2. Measurement is a physical assumption; the algebra proves its consequences here.

**Execution contract.** By default S=q0 is the source qubit, A=q1 is Alice's Bell half, and B=q2 is Bob's Bell half. Full statevector order is S,A,B, with q0 the most significant index bit. The semantic message is (m,n): m is S's outcome and n is A's outcome. Angles are radians and amplitudes are dimensionless. Deterministic checks use CPU complex128, absolute tolerance $10^{-12}$ and relative tolerance zero, with no phase alignment, probability clipping or normalization repair.

Run the eight cumulative Python blocks from the repository root after installing requirements-examples.txt. The companion [teleportation.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/teleportation.py) contains the complete references and guards. The demonstrated FlagQuantum 0.3.1 workflow supports the static gates, statevectors, probabilities, Pauli expectations and **terminal samples** below. Its public fq.Circuit object has no measure/reset/if_test/c_if methods for the dynamic protocol used here. We distinguish native preparation/readout, classical ideal-branch analysis with fresh Bob test circuits, and a native coherent substitute. None demonstrates mid-circuit collapse followed by native classical feedforward, a hardware link or a distributed implementation. Lower-level IR names alone do not establish that execution contract.

<span id="formula-code-7-5-resource"></span>

### 7.5.1 — Declare the input and shared resource

**Formula.** Alice is given the unknown state

$$
|\psi\rangle_S=a|0\rangle+b|1\rangle,\qquad |a|^2+|b|^2=1.
$$

Alice and Bob already share $|\Phi^+\rangle_{AB}=(|00\rangle+|11\rangle)/\sqrt2$, so

$$
\begin{aligned}
|\Omega_0\rangle&=|\psi\rangle_S|\Phi^+\rangle_{AB}\\
&=\frac1{\sqrt2}\bigl(a|000\rangle+a|011\rangle\\
&\qquad+b|100\rangle+b|111\rangle\bigr).
\end{aligned}
$$

**Derivation.** Tensor multiplication assigns the input coefficient to S and equal Bell coefficients to equal A/B bits. H(A) followed by CX(A,B) prepares the pair. Its distribution to separated parties is assumed to have happened before this protocol.

For a known simulator fixture, define

$$
U_\psi=\begin{pmatrix}a&-b^*\\b&a^*\end{pmatrix}.
$$

Both columns have norm one and inner product $a^*(-b^*)+b^*a^*=0$, proving $U_\psi^\dagger U_\psi=I$. Its first column is ψ. This is preparation of **test data**; in actual teleportation Alice receives the input and neither party needs to know a,b or synthesize this matrix. Bob's classical message will not contain the coefficients.

**FlagQuantum code and verification result.** All eight native resource coordinates are compared with the explicit four-term expansion.

```python
import itertools, math
import flagquantum as fq
import torch
from examples.foundations import teleportation as t
from examples.foundations.tensor_spaces import OPTIONS
D, ATOL = t.D, t.ATOL
psi = torch.tensor([.6, .8*complex(math.cos(.43), math.sin(.43))], dtype=D)
a, b = psi.tolist()
U = torch.tensor([[a, -b.conjugate()], [b, a.conjugate()]], dtype=D)
assert torch.allclose(U.conj().T@U, torch.eye(2, dtype=D), atol=ATOL, rtol=0)
c = fq.Circuit(3, dtype=D).unitary(0, unitary=U).h(1).cx(1, 2)
resource = fq.run(c, outputs=[fq.probabilities()], options=OPTIONS)
t.RUNS += 1
expected = torch.tensor([a,a*0,a*0,a,b,b*0,b*0,b], dtype=D)/math.sqrt(2)
assert torch.allclose(resource.statevector()[0], expected, atol=ATOL, rtol=0)
print("Resource amplitudes at indices 0,3,4,7 equal a,a,b,b divided by sqrt(2).")
```

```text
Resource amplitudes at indices 0,3,4,7 equal a,a,b,b divided by sqrt(2).
```

Here a=.6 and $b=.8e^{.43i}$. Real inputs or computational probabilities alone would miss important phase errors.

<span id="formula-code-7-5-decoder"></span>

### 7.5.2 — Expand Alice's gates before measuring anything

**Formula.** Alice applies CX(S,A), then H(S), using only her systems. After CX,

$$
\begin{aligned}
|\Omega_1\rangle=\frac1{\sqrt2}\bigl(&a|000\rangle+a|011\rangle\\
&+b|110\rangle+b|101\rangle\bigr).
\end{aligned}
$$

Substitute $H|0\rangle=(|0\rangle+|1\rangle)/\sqrt2$ and $H|1\rangle=(|0\rangle-|1\rangle)/\sqrt2$:

$$
\begin{gathered}
|\Omega_2\rangle=\frac12\bigl[\\
a(|000\rangle+|100\rangle)\\
+a(|011\rangle+|111\rangle)\\
+b(|010\rangle-|110\rangle)\\
+b(|001\rangle-|101\rangle)\bigr].
\end{gathered}
$$

Grouping by S/A gives

$$
\begin{gathered}
|\Omega_2\rangle=\frac12\bigl[\\
|00\rangle_{SA}(a|0\rangle+b|1\rangle)_B\\
+|01\rangle_{SA}(b|0\rangle+a|1\rangle)_B\\
+|10\rangle_{SA}(a|0\rangle-b|1\rangle)_B\\
+|11\rangle_{SA}(-b|0\rangle+a|1\rangle)_B\bigr].
\end{gathered}
$$

Define $C_{mn}=X^nZ^m$. The compact identity is

$$
|\Omega_2\rangle=\frac12\sum_{m,n=0}^1|mn\rangle_{SA}C_{mn}|\psi\rangle_B.
$$

**Derivation and index check.** The rightmost Z first multiplies input bit i by $(-1)^{mi}$; X then sends i to $i\oplus n$. Thus at full index $4m+2n+z$,

$$
\langle mnz|\Omega_2\rangle
=\frac12(-1)^{m(z\oplus n)}
\begin{cases}a,&z\oplus n=0,\\b,&z\oplus n=1.\end{cases}
$$

This independently checks the gates and register indices. In particular, the 11 column is **[-b,a]**, not [b,−a] in this exact phase convention.

**FlagQuantum code and verification result.** Request probabilities in (S,A) order and raw sample columns in the deliberately reversed (A,S) order. Column metadata maps each record back to (m,n). Terminal samples do not turn the returned joint vector into a selected branch.

```python
c.cx(0, 1).h(0)
decoded = fq.run(c, outputs=[fq.probabilities(qubits=(0,1)),
    fq.samples(qubits=(1,0)), fq.expectation(fq.X(2), name="bx"),
    fq.expectation(fq.Y(2), name="by"), fq.expectation(fq.Z(2), name="bz")],
    shots=32, options=OPTIONS)
t.RUNS += 1
full = decoded.statevector()[0]
assert torch.allclose(full, t.scalar_state(psi), atol=ATOL, rtol=0)
assert torch.allclose(decoded.probabilities[0], torch.full((4,), .25, dtype=torch.float64), atol=ATOL, rtol=0)
records = decoded.samples[0]
messages = [t.decode_record(row, (1,0)) for row in records]
counts = torch.bincount(torch.tensor([2*m+n for m,n in messages]), minlength=4)
assert records.shape == (32,2) and int(counts.sum()) == 32
assert all(abs(float(decoded.expectation(name)[0])) < ATOL for name in ("bx","by","bz"))
print("Decoded probabilities(m,n):", [round(x,6) for x in decoded.probabilities[0].tolist()])
print("32 reversed-column records mapped; native Bob X,Y,Z means all zero.")
```

```text
Decoded probabilities(m,n): [0.25, 0.25, 0.25, 0.25]
32 reversed-column records mapped; native Bob X,Y,Z means all zero.
```

A finite shot histogram need not be uniform. We check binary records, shape, semantic mapping and total count; the exact native probabilities are compared to one quarter. A favorable histogram or seed replay would not prove correctness.

<span id="formula-code-7-5-branches"></span>

### 7.5.3 — Normalize each measurement branch

**Formula.** The ideal projector is $P_{mn}=|mn\rangle\langle mn|_{SA}\otimes I_B$. Therefore

$$
\begin{gathered}
P_{mn}|\Omega_2\rangle=\frac12|mn\rangle_{SA}C_{mn}|\psi\rangle_B,\\
p_{mn}=\|P_{mn}\Omega_2\|^2=\frac14.
\end{gathered}
$$

**Derivation.** X and Z are unitary, so $\|C_{mn}\psi\|=1$. Dividing by the positive square root $\sqrt{p_{mn}}=1/2$ gives

$$
|\Omega_{mn}\rangle=|mn\rangle_{SA}C_{mn}|\psi\rangle_B.
$$

The four probabilities sum to one for every normalized input. No branch is discarded, and no input makes a branch impossible.

| Message (m,n) | Conditional Bob coordinates | Chronological correction calls | Correction matrix |
|---|---|---|---|
| 00 | $(a,b)^{\mathsf T}$ | none | $I$ |
| 01 | $(b,a)^{\mathsf T}$ | X | $X$ |
| 10 | $(a,-b)^{\mathsf T}$ | Z | $Z$ |
| 11 | $(-b,a)^{\mathsf T}$ | X, then Z | $ZX$ |

**Code and verification result.** The classical helper extract fixes the measured coordinates, computes their squared norm and divides by its positive square root. It implements the assumed ideal update mathematically; it is not a native collapse call. It retains the input's overall phase.

```python
branches = {}
for bits in itertools.product((0,1), repeat=2):
    p, w = t.extract(full, (0,1), bits, (2,))
    branches[bits] = w
    assert abs(p-.25) < ATOL
    assert torch.allclose(w, t.byproduct(psi,bits), atol=ATOL, rtol=0)
assert torch.allclose(branches[(1,1)], torch.tensor([-b,a], dtype=D), atol=ATOL, rtol=0)
print("Four probabilities=1/4; phase-fixed columns: [a,b], [b,a], [a,-b], [-b,a].")
```

```text
Four probabilities=1/4; phase-fixed columns: [a,b], [b,a], [a,-b], [-b,a].
```

For general use, extract rejects zero-probability branches and explicitly reports squared-norm underflow of a nonzero projected column. It does not silently reinterpret underflow as an impossible event. Teleportation's ideal one-quarter branches reach neither boundary.

<span id="formula-code-7-5-messages"></span>

### 7.5.4 — Send the message and undo its byproduct

**Formula.** Alice measures S,A in the computational basis and sends (m,n) through a classical channel. Bob applies X if n=1, **then** Z if m=1. The corresponding matrix and product are

$$
\begin{gathered}
D_{mn}=Z^mX^n,\\
D_{mn}C_{mn}=Z^mX^nX^nZ^m=I.
\end{gathered}
$$

**Every-branch proof.** Since $X^2=Z^2=I$, the adjacent X powers cancel and then the Z powers cancel. No commutation of X past Z is needed. For all complex a,b and all four messages,

$$
(I_{SA}\otimes D_{mn})|\Omega_{mn}\rangle
=|mn\rangle_{SA}|\psi\rangle_B.
$$

The message identifies a known reversible disturbance, not a classical description of the amplitudes. Its distribution is input-independent. This constructs a two-bit protocol; it does not prove a general communication lower bound.

**FlagQuantum code and verification result.** The host chooses gates using only (m,n). To test all branches with the static API, it prepares each **simulator-known conditional vector in a fresh circuit**. Bob could not perform that preparation on an unknown state; it is a test fixture, not the physical mechanism of teleportation or a resumed native measurement trajectory.

```python
corrected = {}
for (m,n), w in branches.items():
    # Known simulator branch is freshly prepared; this is not a native collapse.
    bob = fq.Circuit(1, dtype=D).unitary(0, unitary=t.prepare_matrix(w))
    if n: bob.x(0)
    if m: bob.z(0)
    out = fq.run(bob, outputs=[fq.probabilities(),
        fq.expectation(fq.X(0),name="x"), fq.expectation(fq.Y(0),name="y"),
        fq.expectation(fq.Z(0),name="z")], options=OPTIONS)
    t.RUNS += 1
    corrected[(m,n)] = out.statevector()[0]
    assert torch.allclose(corrected[(m,n)], psi, atol=ATOL, rtol=0)
    for op,name in ((t.X,"x"),(t.Y,"y"),(t.Z,"z")):
        assert abs(float(out.expectation(name)[0])-float(torch.vdot(psi,op@psi).real)) < ATOL
print("Four fresh native Bob circuits: chronological X^n then Z^m recovers the full input vector.")
```

```text
Four fresh native Bob circuits: chronological X^n then Z^m recovers the full input vector.
```

These four real native circuits verify the correction sequence and exact vector phase. Physical teleportation would apply these selected gates to the same surviving B after the classical message arrived. No networking, latency model or native dynamic feedback endpoint is exercised.

<span id="formula-code-7-5-ignored"></span>

### 7.5.5 — Predict what Bob sees without all the bits

**Formula.** Let $O=\begin{pmatrix}u&v\\v^*&w\end{pmatrix}$ be any Hermitian qubit observable, with u,w real. Ignoring Alice's outcome gives

$$
\overline{\langle O\rangle}
=\frac14\sum_{m,n}
\langle\psi|C_{mn}^\dagger O C_{mn}|\psi\rangle
=\frac{u+w}{2}.
$$

**Derivation.** For n=0 the two vectors (a,b), (a,−b) have opposite off-diagonal cross terms. Averaging over m leaves $u|a|^2+w|b|^2$. For n=1 the average is $u|b|^2+w|a|^2$. Average these and use normalization to obtain $(u+w)/2$. This averages predictions with probability one quarter; averaging normalized statevectors would be incorrect.

Every qubit measurement effect is Hermitian. Thus all Bob's local outcome probabilities before using the message are independent of the input. In particular, all three Pauli means vanish, as checked natively in 7.5.2. Choosing an input cannot signal to Bob faster than the classical channel.

If Bob receives only n and applies $X^n$, his state is $Z^m\psi$. Averaging over unknown m erases X,Y and retains Z. If only m arrives and he applies $Z^m$, then

$$
Z^mX^nZ^m|\psi\rangle=(-1)^{mn}X^n|\psi\rangle.
$$

The global branch phase cancels from expectations. Averaging over n retains X but erases Y,Z. A special eigenstate can survive a missing correction; a generic unknown state cannot.

**FlagQuantum code and verification result.** Eight fresh static circuits check both incomplete-message policies. The helper uses the same explicit gate selection as 7.5.4 with the missing correction omitted, and returns native Pauli expectations.

```python
means = {}
for policy in ("only-n","only-m"):
    values = [t.bob_reprepare(w,bits,policy)[1] for bits,w in branches.items()]
    means[policy] = torch.tensor(values,dtype=torch.float64).mean(0)
xyz = torch.tensor([float(torch.vdot(psi,op@psi).real) for op in (t.X,t.Y,t.Z)],dtype=torch.float64)
assert torch.allclose(means["only-n"], torch.tensor([0.,0.,float(xyz[2])],dtype=torch.float64),atol=ATOL,rtol=0)
assert torch.allclose(means["only-m"], torch.tensor([float(xyz[0]),0.,0.],dtype=torch.float64),atol=ATOL,rtol=0)
print("Equal-weight branches: only n preserves Z; only m preserves X; no-message means are all zero.")
```

```text
Equal-weight branches: only n preserves Z; only m preserves X; no-message means are all zero.
```

These are exact simulator means, not estimated sampling errors. Neither zero mean nor a one-bit success on a special input certifies that Bob has the original arbitrary state.

<span id="formula-code-7-5-phase"></span>

### 7.5.6 — Separate message mistakes from branch phases

**Formula.** Swapping semantic m,n generally selects the wrong physical correction. Reversing Bob's two chronological calls has a different effect:

$$
(X^nZ^m)(X^nZ^m)=(-1)^{mn}I.
$$

**Derivation.** If either bit is zero, the repeated Pauli squares to I. If both are one, anticommutation gives $XZXZ=X(-XZ)Z=-I$. Thus reversed call order produces $(-1)^{mn}\psi$. On a selected measured branch this is global phase. It fails the exact-vector convention for 11 but **does not make ordinary measured teleportation physically incorrect**. Every subsequent Bob measurement still has the right probabilities.

By contrast, swapping the message bits assigns Z instead of X in branch 01, and X instead of Z in branch 10. The generic complex fixture has wrong corrected rays in both. Uniform message probabilities cannot diagnose this: one must check column metadata and conditional outputs.

**FlagQuantum code and verification result.** The helper's swap policy exchanges m,n before X-then-Z. Its reverse policy calls Z first. Eight native circuits verify the distinctions, including unit fidelity for all reversed-order outputs.

```python
bad = []
for bits,w in branches.items():
    wrong,_ = t.bob_reprepare(w,bits,"swap")
    if not torch.allclose(wrong,psi,atol=ATOL,rtol=0): bad.append(bits)
    reverse,_ = t.bob_reprepare(w,bits,"reverse")
    assert torch.allclose(reverse,((-1)**(bits[0]*bits[1]))*psi,atol=ATOL,rtol=0)
    assert abs(abs(torch.vdot(psi,reverse).item())**2-1) < ATOL
assert bad == [(0,1),(1,0)]
print("Swapped messages fail branches 01 and10; reverse gate order preserves every ray but gives -psi in11.")
```

```text
Swapped messages fail branches 01 and10; reverse gate order preserves every ray but gives -psi in11.
```

For example, raw record (0,1) with declared columns (A,S) means semantic message (m,n)=(1,0). It does not mean (0,1). The complete program includes native deterministic basis calibrations for this reversed column order.

<span id="formula-code-7-5-coherent"></span>

### 7.5.7 — Execute a coherent substitute with quantum controls

**Formula.** Keep S,A unmeasured and append CX(A,B), then CZ(S,B). Each branch receives $Z^mX^n$, so linearity gives

$$
\begin{aligned}
|\Omega_2\rangle&\longmapsto
\frac12\sum_{m,n}|mn\rangle_{SA}|\psi\rangle_B\\
&=|+\rangle_S|+\rangle_A|\psi\rangle_B.
\end{aligned}
$$

**Derivation and boundary.** Apply the identity $D_{mn}C_{mn}=I$ before adding the branches. Their amplitudes remain equal with the same phase. This is a native static unitary identity. It uses quantum controls between Alice's systems and Bob's system; there is no classical message. It is not a distributed implementation by local operations and classical communication.

Reversing the controlled corrections instead gives

$$
|\Omega_{\mathrm{rev}}\rangle
=\frac{|00\rangle+|01\rangle+|10\rangle-|11\rangle}{2}_{SA}
\otimes|\psi\rangle_B.
$$

Bob is still correct, but Alice's joint coherence changes. XX exchanges 00 with 11 and 01 with 10. Its expectation is $2(-1/4)+2(1/4)=0$ for this state and one for $|++\rangle$. A branch-dependent sign that was unobservable after measurement is now observable when the branches remain coherent.

**FlagQuantum code and verification result.** The first circuit visibly appends CX(A,B), CZ(S,B). The reversed helper appends CZ(S,B), CX(A,B), requesting Alice's XX and Bob's three Pauli means.

```python
# These are unmeasured quantum controls, not classical feedforward.
coherent_c = fq.Circuit(3,dtype=D).unitary(0,unitary=U).h(1).cx(1,2).cx(0,1).h(0).cx(1,2).cz(0,2)
coherent = fq.run(coherent_c,outputs=[fq.expectation(fq.X(0)@fq.X(1),name="axx")],options=OPTIONS)
t.RUNS += 1
assert torch.allclose(coherent.statevector()[0],psi.repeat(4)/2,atol=ATOL,rtol=0)
assert abs(float(coherent.expectation("axx")[0])-1) < ATOL
rev = t.query(psi,"reverse-coherent")
assert abs(rev["alice_xx"]) < ATOL
assert all(abs(x-y)<ATOL for x,y in zip(rev["bloch"],xyz.tolist()))
print("Native coherent correction: Alice XX=1; reversed coherent order: Alice XX=0; Bob unchanged.")
```

```text
Native coherent correction: Alice XX=1; reversed coherent order: Alice XX=0; Bob unchanged.
```

Testing Bob alone would miss this full-joint-state difference. The required comparison contract must say whether it concerns a selected branch ray, an exact vector or a coherent circuit identity.

<span id="formula-code-7-5-reference"></span>

### 7.5.8 — Transfer entanglement with an untouched reference

**Formula.** An unknown input can be correlated with a finite reference R. For a qubit reference write

$$
\begin{gathered}
|\chi\rangle_{RS}=\sum_{r,i=0}^1c_{ri}|r\rangle_R|i\rangle_S,\\
\sum_{r,i}|c_{ri}|^2=1.
\end{gathered}
$$

For a larger finite reference only the r range changes. Since the decoder acts trivially on R, linearity gives

$$
\begin{gathered}
|\chi\rangle_{RS}|\Phi^+\rangle_{AB}\longmapsto\\
\frac12\sum_{m,n}|mn\rangle_{SA}
\sum_{r,i}c_{ri}|r\rangle_R C_{mn}|i\rangle_B.
\end{gathered}
$$

The right side displays factors in grouped order SA,R,B. The four-qubit code uses index order R,S,A,B.

**Complete proof.** For each message, the squared norm of the inner vector is

$$
\begin{gathered}
\sum_{r,i,r',j}c_{ri}^*c_{r'j}
\langle r|r'\rangle
\langle i|C_{mn}^\dagger C_{mn}|j\rangle\\
=\sum_{r,i}|c_{ri}|^2=1.
\end{gathered}
$$

Hence every message still has probability one quarter, and the normalized R/B branch is $(I_R\otimes C_{mn})|\chi\rangle_{RB}$. Bob's correction gives

$$
(I_R\otimes D_{mn})(I_R\otimes C_{mn})|\chi\rangle_{RB}
=|\chi\rangle_{RB}.
$$

This equality for arbitrary coefficients preserves the full joint vector and therefore every external correlation, rather than merely three local means. Coherent correction similarly gives $|++\rangle_{SA}\otimes|\chi\rangle_{RB}$ in grouped order. The algebra is the general proof; finite tests check its implementation.

**FlagQuantum code and verification result.** The native reference fixture uses Ry(R,θ), P(R,φ), CX(R,S), Ry(S,.41), then H(A), CX(A,B), CX(S,A), H(S). Independent input coefficients in R/S order are

$$
\begin{aligned}
c_{00}&=\cos(\theta/2)\cos(.41/2),\\
c_{01}&=\cos(\theta/2)\sin(.41/2),\\
c_{10}&=-e^{i\phi}\sin(\theta/2)\sin(.41/2),\\
c_{11}&=e^{i\phi}\sin(\theta/2)\cos(.41/2).
\end{aligned}
$$

The helper verifies every full amplitude and all four extracted R/B columns. Its coherent run also compares native R/B XX and ZZ with independent quadratic forms. Matrix correction of an extracted column is classical analysis; coherent correction is the native continuation.

```python
for stage in ("decoded","coherent"):
    joint, chi = t.reference_pair(.72,.37,stage)
    for bits in itertools.product((0,1),repeat=2):
        p,w = t.extract(joint,(1,2),bits,(0,3))
        if stage == "decoded": w = torch.kron(t.I,t.correction_matrix(bits))@w
        assert abs(p-.25)<ATOL and torch.allclose(w,chi,atol=ATOL,rtol=0)
assert t.RUNS == 26
print("Reference entanglement: all four corrected R/B columns and coherent joint amplitudes recover chi.")
print("26 native circuits in eight body units; no native dynamic teleportation claimed.")
```

```text
Reference entanglement: all four corrected R/B columns and coherent joint amplitudes recover chi.
26 native circuits in eight body units; no native dynamic teleportation claimed.
```

After an ordinary measured run, Alice has S,A in the recorded basis state |mn⟩. She retains no unknown input copy, and the Bell resource has been consumed. This is consistent with no-cloning. The coherent substitute instead leaves her in |++⟩ and spends nonlocal quantum gates; it has a different physical history.

### Complete execution and failure boundaries

Run the complete program and literal-body checker:

~~~bash
python examples/foundations/teleportation.py
python scripts/check_teleportation_prose.py
~~~

The complete program uses eight inputs: computational poles, real/imaginary equatorial states and complex states retaining overall phase. It checks four corrections per input, every ordered role triple in three and four qubits, complex spectator factors, entangled reference inputs and reversed-column calibration. Its three/four-qubit bounds limit the explicit teaching reference, not FlagQuantum capacity.

Sixteen malformed contracts are rejected before an additional native run, including nonnormalized/wrong-dtype input, noninteger/repeated roles, malformed message, missing columns, invalid raw record, unsupported correction policy and impossible branch extraction. Projectors are never submitted as unitary gates. Exact comparisons use absolute tolerance $10^{-12}$, relative tolerance zero. Random frequencies are not required to equal exact probabilities.

Expected output of the complete program:

```text
56 native circuits:eight inputs,resource/decoder/coherent states and all32 phase-preserving Bob branch corrections passed.
20 native Bob re-preparations:no-message/one-bit/two-bit ordering and branch-global-phase distinctions passed.
60 native circuits:all ordered role triples in three/four qubits,complex spectator factors and full amplitudes passed.
6 native reference-input circuits:all conditional joint R/B states and coherent transferred correlations passed.
12 native basis calibrations:reversed raw columns decode into semantic messages(m,n).
1 native reversed coherent correction:Bob is correct but Alice joint coherence differs from the phase-fixed identity.
16 malformed contracts rejected before another native execution.
155 CPU complex128 native circuits passed;host branch re-preparation is not native dynamic teleportation.
```

This evidence does not establish native sampled collapse, reset, general instruments, hardware networking, noisy fidelity or a dynamic compiler. A future public feedback interface needs tests of outcome-conditioned gates on the **retained** Bob system. Fresh known-state preparations would not establish that capability.

### Understanding checks and transfer exercises

**7.5-A — Resolve branch 11.** Derive its amplitudes without the compact Pauli expression. Compare X-then-Z with Z-then-X. What does an exact-vector checker distinguish, and what can a physical Bob measurement distinguish?

**7.5-B — Decode the record.** Raw record (0,1) arrives in columns (A,S). Find (m,n) and the correction. If only n arrives, which Pauli mean survives averaging? Why can Bob's uncorrected local probabilities not transmit input information?

**7.5-C — Fresh indexed experiment.** Use $|\psi\rangle=\sqrt{.3}|0\rangle+e^{-.61i}\sqrt{.7}|1\rangle$ in four qubits with roles (S,A,B)=(q3,q0,q2), and spectator q1 prepared by Ry(.61), P(−.37). Derive the decoded full-index amplitude, message probabilities and coherent corrected state. Execute both circuits. Also extract the four default three-qubit branches for this input and verify fresh native Bob corrections.

**7.5-D — Preserve a stronger property.** Start with $(|00\rangle+|11\rangle)_{RS}/\sqrt2$. Derive and correct R/B branch 01. Why do Bob's local Pauli means alone fail to certify transferred entanglement? What remains at Alice, and what resource must be supplied again?

<details markdown="1">
<summary>Answers and verification guidance for 7.5-A–D</summary>

**A.** The $a|011\rangle$ term acquires a positive S=1 amplitude from H on its S=0 input. The $b|101\rangle$ term acquires a negative S=1 amplitude from H on S=1. Their S/A=11 components are $a|111\rangle-b|110\rangle$, giving Bob $-b|0\rangle+a|1\rangle$. X then Z gives ψ; Z then X gives −ψ. Exact vectors differ, but selected-branch Bob probabilities agree. Coherent recombination makes the branch-dependent sign observable, as Alice's XX test shows.

**B.** m=1,n=0: apply Z only. Learning n alone preserves Z and erases X/Y after averaging. With no bits, every Hermitian effect has mean $\operatorname{tr}(O)/2$, independent of ψ. The classical message must arrive before Bob can exploit the conditional state.

**C.** At full-index bits $(x_0,x_1,x_2,x_3)$ set m=$x_3$, n=$x_0$, z=$x_2$, and $d_0=\sqrt{.3},d_1=e^{-.61i}\sqrt{.7}$. Spectator coefficients are $s_0=\cos(.61/2)$, $s_1=e^{-.37i}\sin(.61/2)$. The decoded amplitude is $s_{x_1}(-1)^{m(z\oplus n)}d_{z\oplus n}/2$. The coherent amplitude is $s_{x_1}d_z/2$. Summing normalized Bob/spectator probabilities gives $p_{mn}=1/4$. All conditional corrections recover d with the spectator unchanged. The exact printed parameters and separate four branch corrections are executed in transfer evidence.

**D.** Branch 01 is $(|01\rangle+|10\rangle)_{RB}/\sqrt2$; Bob's X returns $(|00\rangle+|11\rangle)/\sqrt2$. Both have zero local Pauli means, as do many outcome-ignored ensembles, so those means alone do not identify their joint correlations. Full R/B amplitudes and correlation checks are needed. Alice retains S/A in |mn⟩ plus the classical bits, not an unknown input copy. Another input requires another shared Bell pair.

</details>

**Sources and transition.** The frozen locator is Nielsen and Chuang, *Quantum Computation and Quantum Information*, §1.3.7, “Quantum teleportation,” beginning on printed page 26 ([NC:1.3.7 locator](../references/proof-sources.md#source-nc-1-3-7)). The public [IBM Quantum Learning teleportation lesson](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/quantum-teleportation) was inspected for protocol/reference scope; translate its register and message letters to the S,A,B and (m,n) conventions here. Historical attribution is Bennett, Brassard, Crépeau, Jozsa, Peres and Wootters, [*Physical Review Letters* 70, 1895 (1993)](https://doi.org/10.1103/PhysRevLett.70.1895), whose publisher metadata and abstract were inspected. These are original local derivations and ideal simulator tests, not an experimental-paper reproduction. Independent review remains pending.

<!-- end-section-7.5 -->

<span id="sec-entanglement-and-quantum-information-protocols-6"></span>

## 7.6 Superdense coding

Alice wants to send one of four classical messages, written as two bits (a,b). If she and Bob already share a Bell pair, she can encode the message by operating on her half, send **that one qubit** to Bob, and let him decode both bits by a joint measurement. We will prove the four encoded states are orthogonal and that a specific inverse Bell circuit distinguishes them with certainty.

The prerequisites are [7.3, Bell states and basis changes](#sec-entanglement-and-quantum-information-protocols-3), and [5.1, circuit composition and call order](ch-gates-reversible-computation-and-circuit-synthesis.md#sec-gates-reversible-computation-and-circuit-synthesis-1). Depth **F** requires the encoded-state and measurement proof for every message. Bits a,b are known classical inputs, not unknown quantum amplitudes. We use the 7.3 convention: a is the phase bit and b the parity bit.

**Execution and resource contract.** Initially A=q0 belongs to Alice and B=q1 to Bob. The full statevector uses A,B order, q0 most significant. Alice applies gates only to A while the parties are separated. Bob's two-qubit decoder is permitted **after A has arrived at Bob**. Quantum transmission changes ownership, not the abstract statevector ordering. It is assumed ideal here. The released FlagQuantum 0.3.1 examples execute static gates and terminal probability/sample queries in one centralized simulator; they do not execute a network-send operation, a quantum link or a hardware Bell detector.

Run the eight cumulative Python blocks from the repository root after installing requirements-examples.txt. The complete companion [superdense_coding.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/superdense_coding.py) supplies indexed references, ordered records and error guards. Angles are radians; amplitudes and probabilities are dimensionless. Deterministic checks use CPU complex128, absolute tolerance $10^{-12}$, relative tolerance zero. No phase alignment, probability clipping or input repair is performed.

<span id="formula-code-7-6-resource"></span>

### 7.6.1 — Supply entanglement before choosing the message

**Formula.** The shared resource is

$$
|\Phi^+\rangle_{AB}=\frac{|00\rangle+|11\rangle}{\sqrt2}.
$$

It is prepared mathematically by the Bell encoder

$$
V=\operatorname{CX}_{A\to B}(H_A\otimes I_B),
\qquad V|00\rangle=|\Phi^+\rangle.
$$

**Derivation and resource accounting.** H creates $(|0\rangle+|1\rangle)/\sqrt2$ on A; CX copies its computational-basis label into initially zero B, producing the two correlated terms. At this point the pair must be shared: preparing both qubits at Alice is not by itself distribution to Bob.

The resource statement is: **one previously shared ideal Bell pair plus one subsequent ideal qubit transmission enables two classical message bits**. The prior pair is often called one ebit of entanglement; here that term means this specified Bell-pair resource, without assuming a general entropy theory. If Alice prepares the pair and sends B to establish it, that earlier transmission must also be counted in an end-to-end ledger. Counting it gives two one-qubit transmissions: the earlier B distribution and the later encoded A transmission. We do not claim two bits per total transmitted qubit with entanglement supplied for free.

**FlagQuantum code and verification result.** Native H/CX prepare the resource, and its four amplitudes are checked independently. Ownership is a protocol declaration; no native transport operation is hidden in this code.

```python
import itertools, math, cmath
import flagquantum as fq
import torch
from examples.foundations import superdense_coding as s
from examples.foundations.tensor_spaces import OPTIONS
D, ATOL = s.D, s.ATOL
shared = fq.Circuit(2,dtype=D).h(0).cx(0,1)
initial = fq.run(shared,outputs=[fq.probabilities()],options=OPTIONS)
s.RUNS += 1
phi = torch.tensor([1,0,0,1],dtype=D)/math.sqrt(2)
assert torch.allclose(initial.statevector()[0],phi,atol=ATOL,rtol=0)
print("Shared Phi+ verified;A=q0 belongs to Alice,B=q1 to Bob before transmission.")
```

```text
Shared Phi+ verified;A=q0 belongs to Alice,B=q1 to Bob before transmission.
```

<span id="formula-code-7-6-encoding"></span>

### 7.6.2 — Encode both bits using Alice's qubit alone

**Formula.** For message (a,b), Alice first applies $X_A^b$, then $Z_A^a$. With matrices acting on the left, the encoder is

$$
E_{ab}=Z^aX^b.
$$

Acting on the Bell resource gives

$$
\begin{gathered}
(E_{ab}\otimes I)|\Phi^+\rangle\\
=\frac1{\sqrt2}\sum_{r=0}^1
(-1)^{a(r\oplus b)}|r\oplus b,r\rangle\\
=\frac1{\sqrt2}\sum_{i=0}^1
(-1)^{ai}|i,i\oplus b\rangle\\
=|\beta_{ab}\rangle.
\end{gathered}
$$

**Derivation.** X changes Alice's basis bit r into $r\oplus b$. Z contributes the sign associated with that changed bit. Replacing the summation variable by $i=r\oplus b$ gives exactly the phase-fixed Bell vector of 7.3. Bob's qubit is untouched throughout this encoding.

| Message | Alice's chronological calls | Encoded Bell state |
|---|---|---|
| 00 | none | $(\lvert00\rangle+\lvert11\rangle)/\sqrt2$ |
| 01 | X | $(\lvert01\rangle+\lvert10\rangle)/\sqrt2$ |
| 10 | Z | $(\lvert00\rangle-\lvert11\rangle)/\sqrt2$ |
| 11 | X, then Z | $(\lvert01\rangle-\lvert10\rangle)/\sqrt2$ |

The four message choices therefore select four **joint** states. They do not select four distinguishable states of A alone.

**FlagQuantum code and verification result.** The code visibly performs only Alice's message-dependent gates. Independent coordinate vectors and native XX/ZZ expectations verify the label: XX has eigenvalue $(-1)^a$, and ZZ has eigenvalue $(-1)^b$. Bob's three local Pauli means remain zero.

```python
encoded = {}
for a,b in itertools.product((0,1),repeat=2):
    c = fq.Circuit(2,dtype=D).h(0).cx(0,1)
    if b: c.x(0)   # chronological X^b,then Z^a on Alice only
    if a: c.z(0)
    out = fq.run(c,outputs=[fq.probabilities(),
        fq.expectation(fq.X(0)@fq.X(1),name="xx"),
        fq.expectation(fq.Z(0)@fq.Z(1),name="zz"),
        fq.expectation(fq.X(1),name="bx"),fq.expectation(fq.Y(1),name="by"),
        fq.expectation(fq.Z(1),name="bz")],options=OPTIONS)
    s.RUNS += 1
    encoded[(a,b)] = out.statevector()[0]
    target = torch.zeros(4,dtype=D)
    target[b]=1/math.sqrt(2);target[2+(1^b)]=(-1)**a/math.sqrt(2)
    assert torch.allclose(encoded[(a,b)],target,atol=ATOL,rtol=0)
    assert abs(float(out.expectation("xx")[0])-(-1)**a)<ATOL
    assert abs(float(out.expectation("zz")[0])-(-1)**b)<ATOL
    assert all(abs(float(out.expectation(k)[0]))<ATOL for k in ("bx","by","bz"))
print("Alice-only X^b then Z^a produces beta_ab exactly;XX=(-1)^a,ZZ=(-1)^b.")
```

```text
Alice-only X^b then Z^a produces beta_ab exactly;XX=(-1)^a,ZZ=(-1)^b.
```

<span id="formula-code-7-6-decoding"></span>

### 7.6.3 — Receive A, then measure in the Bell basis

**Formula.** After Alice physically sends A, Bob possesses both A and B. His decoder is

$$
\begin{gathered}
D=V^\dagger,\\
D=(H_A\otimes I_B)\operatorname{CX}_{A\to B}.
\end{gathered}
$$

The chronological calls are therefore **CX(A,B), then H(A)**. To prove decoding directly, apply CX to the encoded expansion:

$$
|\beta_{ab}\rangle
\longmapsto
\frac{|0\rangle+(-1)^a|1\rangle}{\sqrt2}_A
\otimes|b\rangle_B.
$$

H transforms the first factor into |a⟩. Hence

$$
D|\beta_{ab}\rangle=|a,b\rangle.
$$

**Distinguishability proof.** In the inner product between two Bell expansions, matching first bits forces the same i; matching second bits then forces $b=b'$. The remaining sign sum is

$$
\begin{aligned}
\langle\beta_{a'b'}|\beta_{ab}\rangle
&=\delta_{bb'}\frac12\sum_{i=0}^1(-1)^{(a+a')i}\\
&=\delta_{bb'}\delta_{aa'}.
\end{aligned}
$$

The last equality follows because the sum is two when a=a′ and zero otherwise. There are four orthonormal vectors in the four-dimensional A/B space, so they form a complete basis.

Computational-basis measurement after D has effects

$$
\begin{aligned}
F_{ab}&=D^\dagger|ab\rangle\langle ab|D\\
&=|\beta_{ab}\rangle\langle\beta_{ab}|.
\end{aligned}
$$

These projectors are nonnegative and sum to I by completeness. For input message (c,d),

$$
p(a,b\mid c,d)
=|\langle\beta_{ab}|\beta_{cd}\rangle|^2
=\delta_{ac}\delta_{bd}.
$$

Thus one four-outcome Bell measurement recovers **every** message without postselection. H, CX and terminal computational readout are a circuit realization of that ideal measurement; a platform's physical Bell-measurement capability must be checked separately.

**FlagQuantum code and verification result.** Four native executions compare the full decoded vector with |a,b⟩ and the probabilities with its one-hot distribution. Raw columns are deliberately requested as (B,A), then decoded using their declared order.

```python
BELL = torch.stack(list(encoded.values()),dim=1)
assert torch.allclose(BELL.conj().T@BELL,torch.eye(4,dtype=D),atol=ATOL,rtol=0)
for a,b in encoded:
    c = fq.Circuit(2,dtype=D).h(0).cx(0,1)
    if b: c.x(0)
    if a: c.z(0)
    c.cx(0,1).h(0)  # Bob acts on both qubits after receiving A.
    out = fq.run(c,outputs=[fq.probabilities(qubits=(0,1)),
        fq.samples(qubits=(1,0))],shots=17,options=OPTIONS)
    s.RUNS += 1
    basis = torch.zeros(4,dtype=D);basis[2*a+b]=1
    assert torch.allclose(out.statevector()[0],basis,atol=ATOL,rtol=0)
    expected = torch.zeros(4,dtype=torch.float64);expected[2*a+b]=1
    assert torch.allclose(out.probabilities[0],expected,atol=ATOL,rtol=0)
    assert out.samples.shape==(1,17,2)
    assert all(s.decode_record(row,(1,0),(0,1))==(a,b) for row in out.samples[0])
print("Four decoded full vectors are |a,b>;all17 native records per message recover(a,b).")
```

```text
Four decoded full vectors are |a,b>;all17 native records per message recover(a,b).
```

All seventeen records must match here because the ideal distribution is deterministic. This is not a demand that a random finite histogram match a nontrivial probability vector. A returned statevector is still the simulated state before terminal sampling; these calls do not demonstrate a sampled-collapse interface.

<span id="formula-code-7-6-indices"></span>

### 7.6.4 — Keep message order, qubit order and ownership distinct

**Formula.** A record requested in columns (A,B) is (a,b), whereas columns (B,A) give (b,a). The probability-vector index is $2a+b$ in the former order and $2b+a$ in the latter. These are coordinate conventions, not different protocols.

In a register of n qubits, suppose A and B occupy distinct positions p and q. For full-index bits $x_0,\ldots,x_{n-1}$, the encoded amplitude with factored spectators is

$$
\begin{gathered}
\Psi(x_0,\ldots,x_{n-1})\\
=\frac{(-1)^{a x_p}}{\sqrt2}
\,\mathbf1_{x_q=x_p\oplus b}
\prod_{j\notin\{p,q\}}s_{j,x_j}.
\end{gathered}
$$

Here the indicator is one when its subscripted condition holds and zero otherwise. Each spectator has normalized coefficients $s_{j,0},s_{j,1}$. After the decoder the amplitude is

$$
\Psi_{\mathrm{out}}(x)
=\mathbf1_{x_p=a}\mathbf1_{x_q=b}
\prod_{j\notin\{p,q\}}s_{j,x_j}.
$$

**Derivation.** The gates act as the two-qubit decoder on the ordered pair and as identity on every spectator. Linearity therefore leaves their factors unchanged. This is the full-index version of $D|\beta_{ab}\rangle=|ab\rangle$. It also explains why sending A does not require reversing tensor axes or calling SWAP: the same labeled system simply changes which party can operate on it.

**FlagQuantum code and verification result.** Use (A,B)=(q3,q1), with complex spectators at q0,q2. The helper prepares spectator j by Ry(.29+.17j), P(−.23(j+1)), so

$$
\begin{aligned}
s_{j,0}&=\cos((.29+.17j)/2),\\
s_{j,1}&=e^{-.23i(j+1)}\sin((.29+.17j)/2).
\end{aligned}
$$

It compares every native amplitude with the indexed formula and reconstructs semantic messages from reversed native columns.

```python
for bits in encoded:
    mapped = s.query(bits,n=4,pair=(3,1),columns=(1,3))
    assert all(x==bits for x in mapped["messages"])
    assert int(mapped["counts"][2*bits[0]+bits[1]])==17
print("Mapped roles(A,B)=(q3,q1):raw columns(q1,q3) are(b,a);semantic messages remain(a,b).")
```

```text
Mapped roles(A,B)=(q3,q1):raw columns(q1,q3) are(b,a);semantic messages remain(a,b).
```

A symmetric Bell histogram can hide swapped columns. The four asymmetric decoded labels and exact full-state indices provide a calibration that distinguishes those conventions. No classical label renaming is counted as a quantum transmission.

<span id="formula-code-7-6-local"></span>

### 7.6.5 — Identify why Bob needs a joint decoder

**Formula.** Before A arrives, Bob can measure B alone. For any Hermitian one-qubit observable $O=\begin{pmatrix}u&v\\v^*&w\end{pmatrix}$, the encoded state predicts

$$
\langle\beta_{ab}|I_A\otimes O|\beta_{ab}\rangle
=\frac{u+w}{2}.
$$

**Derivation.** The two terms of the Bell state have orthogonal A factors, so their off-diagonal contributions vanish when O acts only on B. Their B factors are b and $1\oplus b$, and their squared coefficients are both one half. Thus the result is the average of the two diagonal entries, independent of a,b. Every local measurement effect is Hermitian, so Bob has no local measurement whose probabilities reveal the message before transmission. The analogous calculation holds for A alone.

After receiving A, a computational-basis measurement of both qubits still only reveals the parity b: the possibilities are $(0,b)$ and $(1,1\oplus b)$, each with probability one half. Their relative sign contains a, and ordinary computational probabilities do not retain that sign.

If Bob performs CX but forgets H, the state is

$$
H|a\rangle_A\otimes|b\rangle_B,
$$

and his outputs are (0,b), (1,b), each with probability one half. He again recovers only b. The H in the correct decoder converts the relative sign into a deterministic first-bit outcome.

**FlagQuantum code and verification result.** Native local Pauli means were checked in 7.6.2. Here four native circuits omit the final H and verify the exact distribution. The helper's parity stage ends immediately after CX(A,B).

```python
for a,b in encoded:
    parity = s.query((a,b),"parity")
    expected = torch.zeros(4,dtype=torch.float64)
    expected[b]=.5;expected[2+b]=.5
    assert torch.allclose(parity["probabilities"],expected,atol=ATOL,rtol=0)
print("Omitting final H loses a:outputs(0,b),(1,b) each have probability1/2.")
```

```text
Omitting final H loses a:outputs(0,b),(1,b) each have probability1/2.
```

The protocol exploits the four-dimensional **joint** space available after transmission. It does not place four orthogonal messages into an isolated two-dimensional qubit. General capacity statements for arbitrary coding schemes need the later information-theory results; no general capacity theorem is asserted by this four-message example.

<span id="formula-code-7-6-errors"></span>

### 7.6.6 — Diagnose phases separately from decoder errors

**Formula.** An alternative convention applies Zᵃ first and Xᵇ second. Its matrix is $X^bZ^a=(-1)^{ab}Z^aX^b$. Consequently,

$$
\begin{gathered}
D(X^bZ^a\otimes I)|\Phi^+\rangle\\
=(-1)^{ab}|a,b\rangle.
\end{gathered}
$$

**Derivation.** The Pauli anticommutation $XZ=-ZX$ contributes a minus sign only for a=b=1. In this protocol the message is classical: each run chooses one pair of bits. That run's overall sign does not change any measurement probability. The alternate convention still sends both bits correctly, though an exact-vector comparison must include its phase. A coherent superposition of message controls would have a relative phase and would require another contract; it is not the classical communication task here.

Using H followed by CX as Bob's supposed inverse is a different error. It uses V instead of $V^\dagger$. On a Bell vector H already produces four amplitudes, all of modulus one half; CX merely permutes them. Thus this wrong decoder gives probability one quarter to each output for **every** message.

**FlagQuantum code and verification result.** Four explicit native alternate-encoding circuits check the exact $(-1)^{ab}$ phase. Four further native circuits use the wrong decoder order and verify its uniform distribution.

```python
for a,b in encoded:
    c = fq.Circuit(2,dtype=D).h(0).cx(0,1)
    if a: c.z(0)  # alternate chronological Z^a,then X^b
    if b: c.x(0)
    c.cx(0,1).h(0)
    out = fq.run(c,outputs=[fq.probabilities()],options=OPTIONS)
    s.RUNS += 1
    target = torch.zeros(4,dtype=D);target[2*a+b]=(-1)**(a*b)
    assert torch.allclose(out.statevector()[0],target,atol=ATOL,rtol=0)
    wrong = s.query((a,b),"wrong")
    assert torch.allclose(wrong["probabilities"],torch.full((4,),.25,dtype=torch.float64),atol=ATOL,rtol=0)
print("Alternate encoding adds(-1)^(ab),without a message error;wrong decoder H-then-CX gives uniform outputs.")
```

```text
Alternate encoding adds(-1)^(ab),without a message error;wrong decoder H-then-CX gives uniform outputs.
```

A test that checks only normalized vectors can miss decoder mistakes, while a test that rejects every overall sign would falsely reject a working classical protocol. The checks must state whether they test exact circuit identity or classical message probabilities.

<span id="formula-code-7-6-resource-errors"></span>

### 7.6.7 — Calculate failure when the shared resource is not Phi+

**Formula.** Replace the shared pair by the normalized pure state

$$
\begin{gathered}
|\eta_{\theta,\phi}\rangle=c|00\rangle+e^{i\phi}s|11\rangle,\\
c=\cos(\theta/2),\qquad s=\sin(\theta/2).
\end{gathered}
$$

This is a specified pure-resource mismatch, not a noise model. Use the same encoding and decoder. After encoding and CX, the state is

$$
\begin{gathered}
\sum_{r=0}^1d_r(-1)^{a(r\oplus b)}
|r\oplus b,b\rangle,\\
d_0=c,\qquad d_1=e^{i\phi}s.
\end{gathered}
$$

H contributes $(-1)^{t(r\oplus b)}/\sqrt2$ to output first bit t. Set $u=t\oplus a$ and sum the two r values:

$$
\begin{gathered}
\text{amplitude of }|t,b\rangle\\
=\frac{(-1)^{ub}}{\sqrt2}
\left(c+(-1)^u e^{i\phi}s\right).
\end{gathered}
$$

Define $g_\pm=(c\pm e^{i\phi}s)/\sqrt2$. The complete decoded vector is

$$
g_+|a,b\rangle+(-1)^b g_-|a\oplus1,b\rangle.
$$

**Derivation of the error probabilities.** Since c,s are real and $c^2+s^2=1$,

$$
\begin{aligned}
p(\text{both bits correct})&=|g_+|^2\\
&=\frac{1+\sin\theta\cos\phi}{2},\\
p(\text{only a flipped})&=|g_-|^2\\
&=\frac{1-\sin\theta\cos\phi}{2}.
\end{aligned}
$$

The parity bit b remains exact. At θ=π/2,φ=0 the resource is Phi+ and the first probability is one. At θ=0 the resource is a product and the phase bit is completely ambiguous. At θ=π/2,φ=π the resource is Phi− and the assumed decoder flips a with certainty. That pair is still maximally entangled: the failure is a resource-convention mismatch, not proof that entanglement has disappeared.

A common overall phase on both resource coefficients cancels from probabilities. The φ here is their **relative** phase and changes interference. This distinction prevents a phase-alignment routine from concealing a real error.

**FlagQuantum code and verification result.** Native Ry/P/CX prepare the declared imperfect resource, and explicit message gates and decoder follow. All four decoded vectors and exact success probabilities are checked.

```python
theta, phase = .83, -.47
gp = (math.cos(theta/2)+cmath.exp(phase*1j)*math.sin(theta/2))/math.sqrt(2)
gm = (math.cos(theta/2)-cmath.exp(phase*1j)*math.sin(theta/2))/math.sqrt(2)
for a,b in encoded:
    c = fq.Circuit(2,dtype=D).ry(0,theta).p(0,phase).cx(0,1)
    if b: c.x(0)
    if a: c.z(0)
    c.cx(0,1).h(0)
    out = fq.run(c,outputs=[fq.probabilities()],options=OPTIONS)
    s.RUNS += 1
    target = torch.zeros(4,dtype=D)
    target[2*a+b]=gp;target[2*(a^1)+b]=(-1)**b*gm
    assert torch.allclose(out.statevector()[0],target,atol=ATOL,rtol=0)
    assert abs(float(out.probabilities[0,2*a+b])-(1+math.sin(theta)*math.cos(phase))/2)<ATOL
print("Imperfect resource:correct-bit probability=(1+sin(theta)cos(phase))/2;parity bit b is exact.")
```

```text
Imperfect resource:correct-bit probability=(1+sin(theta)cos(phase))/2;parity bit b is exact.
```

The complete program also tests the three boundary resources just discussed, a negative preparation angle and other complex phases. Random frequencies are not required to equal these nontrivial exact probabilities.

<span id="formula-code-7-6-relocation"></span>

### 7.6.8 — Model register relocation without inventing a network API

**Formula.** A simulator may keep A's label fixed during transmission. If an implementation instead assigns the received state to a new slot C initialized to zero, a SWAP(A,C) is an explicit register-relocation fixture. Its three-CX identity follows on every basis input:

$$
\begin{aligned}
(x,y)&\longmapsto(x,y\oplus x)\\
&\longmapsto(y,y\oplus x)\\
&\longmapsto(y,x).
\end{aligned}
$$

The chronological controls are A→C, C→A, A→C. Linearity extends the basis identity to arbitrary, even entangled, amplitudes. For the encoded state with C=0,

$$
\begin{gathered}
|\beta_{ab}\rangle_{AB}|0\rangle_C\longmapsto\\
\frac1{\sqrt2}\sum_{i=0}^1(-1)^{ai}
|0,i\oplus b,i\rangle_{A,B,C}.
\end{gathered}
$$

Bob now decodes the ordered pair (C,B), using CX(C,B), H(C). The full result in **old-A,B,C** index order is

$$
|0,b,a\rangle.
$$

**Derivation and API boundary.** The old slot becomes zero and the correlations move into C,B, exactly as the SWAP identity states. In this fixture C is Alice's spare local slot before departure. After the SWAP, C is the carrier assumed delivered to Bob, while old A stays with Alice; a cross-party SWAP is not being offered as a substitute for the transmission channel. Terminal columns (C,B) therefore return (a,b). This test catches a receiver using the old slot or the wrong ordered pair. It does not establish a physical transport channel: a centralized SWAP is a unitary on simulator registers, not evidence of remote connectivity, loss, latency or hardware transmission.

The physical protocol requires only sending the already encoded A. No SWAP gate is inherently required to move a physical carrier between parties. The fixture is useful for implementations that explicitly change register allocation; it is not an extra hidden quantum-communication resource.

**FlagQuantum code and verification result.** Four native three-qubit runs implement this fixture with explicit CX calls and verify both the old slot and received message.

```python
for a,b in encoded:
    c = fq.Circuit(3,dtype=D).h(0).cx(0,1)
    if b: c.x(0)
    if a: c.z(0)
    c.cx(0,2).cx(2,0).cx(0,2)  # local-register relocation fixture
    c.cx(2,1).h(2)              # now decode ordered pair(carrier,B)
    out = fq.run(c,outputs=[fq.probabilities(qubits=(2,1)),
        fq.samples(qubits=(2,1))],shots=11,options=OPTIONS)
    s.RUNS += 1
    target = torch.zeros(8,dtype=D);target[2*b+a]=1
    assert torch.allclose(out.statevector()[0],target,atol=ATOL,rtol=0)
    assert all(tuple(map(int,row))==(a,b) for row in out.samples[0])
assert s.RUNS==33
print("Relocation returns |0,b,a> in old-A,B,carrier order;all ordered records return(a,b).")
print("33 native circuits in eight body units;physical single-qubit transport is an explicit model assumption.")
```

```text
Relocation returns |0,b,a> in old-A,B,carrier order;all ordered records return(a,b).
33 native circuits in eight body units;physical single-qubit transport is an explicit model assumption.
```

After ideal decoding and measurement, Bob holds a product basis state encoding the two bits. The original shared Bell pair is no longer available as a resource. Alice cannot send a second two-bit message by assuming the consumed pair was silently restored; another shared pair must be supplied. The terminal-query examples do not demonstrate a reset operation or resource recycling.

### Complete execution and support limits

Run the complete program and literal-body checker:

~~~bash
python examples/foundations/superdense_coding.py
python scripts/check_superdense_coding_prose.py
~~~

The complete program checks all four messages on all twenty ordered two-qubit supports in registers of two, three and four qubits, including complex spectators and reversed readout columns. Scalar indexed amplitudes, exact marginal sums, Pauli expectations and integer record counts independently check the native outputs. The small register bound belongs to this explicit reference, not to FlagQuantum's capacity.

Sixteen malformed contracts are rejected before an additional native run: invalid message length/type/value; undersized register, repeated/out-of-range supports; nonfinite/nonreal angles; unknown stage/order; invalid shot count/seed; invalid column declaration; and wrong-dtype, nonbinary or mismatched-column records. No unsupported network method, physical Bell detector or noisy channel is fabricated. All demonstrated preparations, encoders, decoders and relocation fixtures use actual released static gates and native terminal queries.

Expected output of the complete program:

```text
160 native circuits:four messages on all20 ordered2/3/4qubit pairs;exact encoded/decoded vectors,reversed-column records and spectator phases passed.
17 native circuits:resource,omitted-H/wrong-order decoders and alternate encoding phase passed.
48 native circuits:six imperfect pure resources;exact phase-bit error formula and parity-bit preservation passed.
4 native relocation fixtures:old Alice slot=0,carrier/B decoder returns(a,b);not a network transport test.
16 malformed contracts rejected before another native execution.
229 CPU complex128 native circuits passed;one transmitted qubit assumes a previously shared Bell pair.
```

The finite executions verify implementation; they do not replace the four-state proof. This is an author-verified working draft, with independent mathematical review, implementation review and reader trial still pending.

### Understanding checks and transfer exercises

**7.6-A — Fix the convention.** Derive the 11 encoded vector using only Alice's X then Z actions. What changes if she uses Z then X? Which result changes under exact-vector comparison, and which under classical message readout?

**7.6-B — Count the resources.** Explain why Bob cannot run the two-qubit decoder before A arrives. List the shared resource, transmitted system and terminal outputs. If Alice originally prepared both resource halves, identify the extra transmission needed to establish sharing. Is the pair available again after decoding?

**7.6-C — Fresh ordered-register experiment.** Use four qubits with (A,B)=(q2,q0). For spectator j in {1,3}, use Ry(.29+.17j), P(−.23(j+1)). Run all four messages with terminal columns (q0,q2). Predict the full decoded indices and semantic messages. Explain why replacing transport by a relabeling of classical records would not implement the protocol.

**7.6-D — Diagnose a wrong resource.** For θ=1.17,φ=−.31 derive both decoded amplitudes and probabilities for every message. Repeat with θ=π/2,φ=π. Is a measured zero error frequency in a finite batch a certificate of the ideal resource? Propose an exact-probability or interference check suited to the simulator.

<details markdown="1">
<summary>Answers and verification guidance for 7.6-A–D</summary>

**A.** X(A) sends $(|00\rangle+|11\rangle)/\sqrt2$ to $(|10\rangle+|01\rangle)/\sqrt2$. Z(A) changes the sign of the first term, giving $(|01\rangle-|10\rangle)/\sqrt2=\beta_{11}$. Reversing the calls gives its negative. The exact vectors differ, but Bob's decoded message is 11 in both conventions. The four message-selected signs must not be mistaken for a coherent controlled-encoding identity.

**B.** Before transmission Bob controls only B; the joint CX is unavailable under the separated-party contract. A prior shared Phi+ pair and one subsequent A transmission give Bob the two systems needed for Bell readout. The terminal outputs on ordered (A,B) are (a,b). If Alice initially prepared both halves she must first send B to distribute the resource; that earlier use is separate from the encoded-A transmission. The decoded state is a product and the Bell resource is consumed. There is no automatic recycling.

**C.** At full bits $(x_0,x_1,x_2,x_3)$, decoding fixes $x_2=a,x_0=b$. Full indices are $8b+4x_1+2a+x_3$, weighted by the two spectator coefficients. Native raw columns (q0,q2) contain (b,a), while the semantic message remains (a,b). The full state still contains every coherent spectator factor. The printed parameters and all four messages are executed in transfer evidence. Merely permuting a classical record cannot deliver Alice's physical qubit or grant Bob a joint operation on it.

**D.** Set $g_\pm=(\cos(.585)\pm e^{-.31i}\sin(.585))/\sqrt2$. The vector is $g_+|a,b\rangle+(-1)^b g_-|a\oplus1,b\rangle$, with probabilities $(1\pm\sin(1.17)\cos(.31))/2$. For Phi−, $g_+=0,g_-=1$, so a flips certainly and b remains exact; the sign on that erroneous branch is $(-1)^b$. A finite zero-error sample is not a certificate that the true error probability is zero. In this simulator compare the full encoded coefficients, native exact decoder probabilities and XX sign against their declared resource convention.

</details>

**Sources.** The frozen locator is Nielsen and Chuang, *Quantum Computation and Quantum Information*, §2.3, “Application: superdense coding,” beginning on printed page 97 ([NC:2.3 locator](../references/proof-sources.md#source-nc-2-3)); the existing record is a contents-locator check, not a new full-text proof review. The public [IBM Quantum Learning superdense-coding lesson](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/superdense-coding) was inspected for the protocol and message conventions. Its register order and chronological Z/X choice differ from our phase-fixed convention and must be translated. Historical attribution is Bennett and Wiesner, [*Physical Review Letters* 69, 2881 (1992)](https://doi.org/10.1103/PhysRevLett.69.2881); publisher metadata and abstract were inspected, not a full experimental-paper reproduction. All derivations and execution references above are local original work. Section 7.7 develops no-signalling and classical-communication distinctions further.

<!-- end-section-7.6 -->

<span id="sec-entanglement-and-quantum-information-protocols-7"></span>

## 7.7 No-signalling and classical communication

A measurement outcome can change the conditional predictions for a distant entangled system. That fact does not give the measuring party a way to choose the distant observer's unlabelled statistics. The difference is between a selected branch, the sum over all branches and a record that has actually been communicated. We will prove the no-signalling statement, including its completeness assumption, and then identify exactly what changes when classical information is available.

The prerequisites are [6.2, conditional states and ignored outcomes](ch-measurement-expectation-values-and-statistical-estimation.md#sec-measurement-expectation-values-and-statistical-estimation-2), and [7.3, Bell states and basis changes](#sec-entanglement-and-quantum-information-protocols-3). Depth **F** requires the complete marginal-probability proof. We first prove it for arbitrary finite complete projective measurements, then give a local finite-operator bridge that covers local unitaries, weak measurements, ancillary systems and discarded records. Density-operator notation is not needed; its systematic development remains in Chapter 8.

**Scope and execution contract.** Alice and Bob act on separate tensor factors A,B of a fixed shared state, with no interaction or message channel during the comparison. Alice chooses a controllable setting x; Bob's device setting y is held fixed when comparing x choices. The initial joint preparation must be the same, or the same stated ensemble, for every x. Alice's process is complete, and Bob keeps all records. The theorem concerns the finite quantum model under these assumptions. It does not derive the relativistic speed limit from matrix algebra, nor audit spacelike separation in a real experiment.

Default qubits are A=q0 and B=q1, with q0 most significant in full indices. Angles are radians and probabilities are dimensionless. The eight Python units are cumulative from the repository root with requirements-examples.txt installed. [no_signalling.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/no_signalling.py) contains the complete program. Native FlagQuantum 0.3.1 performs the declared static preparations, basis rotations, coherent local-meter gates, exact probabilities and terminal samples. Conditional branches and general operator/effect calculations are explicit classical analysis, not invented native collapse, reset, general-instrument or classical-network endpoints. Deterministic checks use CPU complex128, absolute tolerance $10^{-12}$ and relative tolerance zero, without phase alignment, probability clipping or input normalization repair.

<span id="formula-code-7-7-signal"></span>

### 7.7.1 — Define the operational test for a signal

**Formula.** Let x be a bit or other finite setting Alice can deliberately choose, a her random outcome, and b a result Bob can read locally. A usable change in Bob's probability law would require an event C for which

$$
p_B(C\mid x,y)\ne p_B(C\mid x',y).
$$

The no-signalling conclusion is equality for every C, every fixed y and every pair of allowed local choices x,x′. The conditional law $p(b\mid a,x,y)$ is a different object: it presumes that the branch label a is available.

**Derivation of the distinction.** Alice can choose a measurement basis; she cannot, under the measurement postulate, force whichever random outcome is convenient. Bob cannot sort his records by an unreceived label. His probability is the law of total probability,

$$
p_B(b\mid x,y)
=\sum_a p(a\mid x)\,p(b\mid a,x,y).
$$

Terms of zero weight contribute zero without assigning a normalized state to an impossible branch. No signalling means that this weighted sum, not every term separately, is independent of x.

For the concrete Bell resource,

$$
|\Phi^+\rangle_{AB}=(|00\rangle+|11\rangle)/\sqrt2,
$$

Bob's computational probabilities start at one half each.

**FlagQuantum code and verification result.** A real native preparation/run establishes the fixture and its unconditioned Bob marginal.

```python
import math, itertools
import torch
import flagquantum as fq
from examples.foundations import no_signalling as s
from examples.foundations.tensor_spaces import OPTIONS
D, ATOL = s.D, s.ATOL
c = fq.Circuit(2,dtype=D).h(0).cx(0,1)
out = fq.run(c,outputs=[fq.probabilities(qubits=(1,))],options=OPTIONS)
s.RUNS += 1
phi = torch.tensor([1,0,0,1],dtype=D)/math.sqrt(2)
assert torch.allclose(out.statevector()[0],phi,atol=ATOL,rtol=0)
assert torch.allclose(out.probabilities[0],torch.tensor([.5,.5],dtype=torch.float64),atol=ATOL,rtol=0)
print("Shared Phi+:Bob's unconditioned computational probabilities are(1/2,1/2).")
```

```text
Shared Phi+:Bob's unconditioned computational probabilities are(1/2,1/2).
```

This verifies a simulator prediction, not a distance, clock synchronization or communication speed. The general result follows from the proof below.

<span id="formula-code-7-7-projectors"></span>

### 7.7.2 — Sum a complete local measurement, not a selected outcome

**Formula.** Let $|\Psi\rangle\in\mathcal H_A\otimes\mathcal H_B$ be any normalized finite joint pure state. For each x, Alice's projectors obey

$$
\begin{gathered}
P_{a|x}=P_{a|x}^\dagger,\\
P_{a|x}P_{a'|x}=\delta_{aa'}P_{a|x},\\
\sum_aP_{a|x}=I_A.
\end{gathered}
$$

Bob uses any complete projective family $\{Q_{b|y}\}_b$. Local tensor-factor operations commute:

$$
\begin{gathered}
(P_{a|x}\otimes I_B)(I_A\otimes Q_{b|y})\\
=P_{a|x}\otimes Q_{b|y}.
\end{gathered}
$$

The joint probability is

$$
q(a,b\mid x,y)
=\|(P_{a|x}\otimes Q_{b|y})|\Psi\rangle\|^2.
$$

**Full marginal proof.** Expand the squared norm as an inner product and use both projectors' idempotence:

$$
q(a,b\mid x,y)
=\langle\Psi|P_{a|x}\otimes Q_{b|y}|\Psi\rangle.
$$

Now sum over **every** Alice outcome:

$$
\begin{gathered}
\sum_a q(a,b\mid x,y)\\
=\left\langle\Psi\left|
\left(\sum_aP_{a|x}\right)\otimes Q_{b|y}
\right|\Psi\right\rangle\\
=\langle\Psi|I_A\otimes Q_{b|y}|\Psi\rangle.
\end{gathered}
$$

The last expression is Bob's probability if Alice does nothing. It contains no x. Summing it over any set C of Bob outcomes proves the event version of no-signalling. Summing over all b gives one, so no omitted probability is hiding in this calculation. Exchanging the two parties proves the corresponding statement in the other direction.

For a branch with $p(a\mid x)>0$, the assumed ideal update gives

$$
|\Psi_{a|x}\rangle
=\frac{(P_{a|x}\otimes I)|\Psi\rangle}{\sqrt{p(a\mid x)}}.
$$

Multiplying its Bob prediction by $p(a\mid x)$ cancels the normalization denominator and returns q. If p=0, the projected vector has zero norm and is zero, so all its joint probabilities are zero. There is no division by zero in the marginal proof.

**FlagQuantum code and verification result.** The helper runs all nine Alice/Bob Z,X,Y analyzer pairs. Its native terminal joint probabilities are compared with independent local-projector calculations, and their Alice sum is compared with the probability before Alice's measurement.

```python
reports = {}
for alice,bob in itertools.product(("Z","X","Y"),repeat=2):
    reports[(alice,bob)] = s.query(alice=alice,bob=bob)
    report = reports[(alice,bob)]
    assert torch.allclose(report["joint"].sum(0),torch.tensor([.5,.5],dtype=torch.float64),atol=ATOL,rtol=0)
    assert torch.allclose(report["marginal"],report["baseline"],atol=ATOL,rtol=0)
print("Nine native analyzer pairs:sum over Alice's complete outcomes leaves every Bob basis marginal unchanged.")
```

```text
Nine native analyzer pairs:sum over Alice's complete outcomes leaves every Bob basis marginal unchanged.
```

For a Z measurement there is no analyzer gate; for X use H; for Y use P(−π/2), then H. Without a restoring rotation, the analyzer/readout operators are $|a\rangle\langle a|R_x$, whereas ideal projectors in the original basis are $R_x^\dagger|a\rangle\langle a|R_x$. Their local output vectors differ, but their remote branch probabilities agree. The program checks this agreement explicitly. Terminal sampling does not collapse the returned statevector.

<span id="formula-code-7-7-conditional"></span>

### 7.7.3 — Conditional predictions can change without a signal

**Formula.** For Phi+, suppose Alice measures in the orthonormal basis $\{|u_a\rangle\}$. Write $|u_a\rangle=u_{a0}|0\rangle+u_{a1}|1\rangle$. Direct contraction gives

$$
(\langle u_a|_A\otimes I_B)|\Phi^+\rangle
=\frac{u_{a0}^*|0\rangle+u_{a1}^*|1\rangle}{\sqrt2}.
$$

Its squared norm is one half, so Bob's normalized conditional vector is $|u_a^*\rangle$. The complex conjugate matters for Y.

| Alice basis | Bob conditional vector for a=0 | Bob conditional vector for a=1 |
|---|---|---|
| Z | $\lvert0\rangle$ | $\lvert1\rangle$ |
| X | $\lvert+\rangle$ | $\lvert-\rangle$ |
| Y | $\lvert-i\rangle$ | $\lvert+i\rangle$ |

Here $|\pm i\rangle=(|0\rangle\pm i|1\rangle)/\sqrt2$ and $|\pm\rangle=(|0\rangle\pm|1\rangle)/\sqrt2$. Every row has branch weights one half.

**Derivation.** Z-conditioned Bob results are deterministic in Z, X-conditioned results deterministic in X, and Y-conditioned results have the opposite Y sign. Averaging the two outcomes in the corresponding row makes every Bob Pauli mean zero. More generally, for any Hermitian effect $E=\begin{pmatrix}u&v\\v^*&w\end{pmatrix}$, averaging each of these orthogonal conditional pairs gives $(u+w)/2$. Thus changing the ensemble description does not change any unlabelled Bob measurement probability.

**Code and verification result.** Reuse the actual native analyzed states from the preceding unit. Slicing an Alice row and normalizing it is classical ideal-branch analysis; it is not a new native measurement or remotely accessible statevector.

```python
expected = {"Z":(torch.tensor([1,0],dtype=D),torch.tensor([0,1],dtype=D)),
    "X":(torch.tensor([1,1],dtype=D)/math.sqrt(2),torch.tensor([1,-1],dtype=D)/math.sqrt(2)),
    "Y":(torch.tensor([1,-1j],dtype=D)/math.sqrt(2),torch.tensor([1,1j],dtype=D)/math.sqrt(2))}
for basis in ("Z","X","Y"):
    report = reports[(basis,"Z")]
    for a in (0,1):
        p = float(report["weights"][a])
        bob_column = report["analyzed_state"].reshape(2,2)[a]/math.sqrt(p)
        assert abs(p-.5)<ATOL
        assert torch.allclose(bob_column,expected[basis][a],atol=ATOL,rtol=0)
for a in (0,1):
    assert abs(float(reports[("Y","Y")]["conditional"][a][1-a])-1)<ATOL
print("Reused native states:Alice Z/X/Y branches steer Bob to Z/X/conjugate-Y vectors;no new native run.")
```

```text
Reused native states:Alice Z/X/Y branches steer Bob to Z/X/conjugate-Y vectors;no new native run.
```

An observer who later receives Alice's labels can verify these conditional correlations. Before receiving them, Bob has no local event telling him which row's member occurred. Bell correlations can violate a local hidden-variable factorization while still obeying the marginal equality proved here.

<span id="formula-code-7-7-complete"></span>

### 7.7.4 — Extend the proof to a complete local process

**Formula and local bridge.** Projectors are not the only allowed local operations. Describe a finite local process by operators $M_{ak|x}:\mathcal H_A\to\mathcal H_{A'}$, with visible outcome a and optional unobserved label k. Require

$$
\begin{gathered}
\sum_{a,k}M_{ak|x}^\dagger M_{ak|x}=I_A\\
\text{for every }x.
\end{gathered}
$$

Denote the local sum by $S_x=\sum_{a,k}M_{ak|x}^\dagger M_{ak|x}$, so $S_x=I_A$. For pure global input, define the unnormalized branches

$$
\begin{gathered}
|\eta_{ak|x}\rangle=(M_{ak|x}\otimes I_B)|\Psi\rangle,\\
p(a\mid x)=\sum_k\|\eta_{ak|x}\|^2.
\end{gathered}
$$

Completeness implies $\sum_a p(a\mid x)=\langle\Psi|I|\Psi\rangle=1$. Let Bob's outcome effects $E_{b|y}$ be positive Hermitian matrices summing to $I_B$. Positivity means every quadratic form is nonnegative; the identity sum normalizes their probabilities. Projectors are a special case, but $E^2=E$ is not assumed here.

For this extension, the operator/effect probability rule is a physical assumption, just as the projective update was in 6.2; the no-signalling identity is its mathematical consequence. The joint probability and conditional prediction are

$$
\begin{gathered}
q(a,b\mid x,y)\\
=\sum_k\langle\eta_{ak|x}|I_{A'}\otimes E_{b|y}|\eta_{ak|x}\rangle.
\end{gathered}
$$

$$
\begin{gathered}
p(b\mid a,x,y)=\frac{q(a,b\mid x,y)}{p(a\mid x)}\\
\text{only when }p(a\mid x)>0.
\end{gathered}
$$

**Full complete-process proof.** Insert each unnormalized branch into q, multiply tensor factors and then sum. Linearity collects the local operator sum into Sₓ:

$$
\begin{gathered}
\sum_a q(a,b\mid x,y)\\
=\sum_{a,k}\langle\Psi|
M_{ak|x}^\dagger M_{ak|x}\otimes E_{b|y}
|\Psi\rangle\\
=\langle\Psi|S_x\otimes E_{b|y}|\Psi\rangle\\
=\langle\Psi|I_A\otimes E_{b|y}|\Psi\rangle.
\end{gathered}
$$

No Bob measurement choice and no input entanglement was restricted. Rectangular M are allowed in this mathematical statement; $I_{A'}$ in the intermediate prediction contracts to the input-space identity through completeness. When hidden k values remain, a single normalized vector need not describe the visible outcome a; keep their conditional ensemble rather than adding the vectors.

This finite-operator update is the stated quantum-process model, not a claim that arbitrary nonlinear transformations are physically allowed. The reference program uses square qubit matrices for its bounded examples; its numerical completeness and positivity checks are tolerance checks, not interval certificates. General channel representations receive their full treatment in Chapter 9.

**FlagQuantum code and verification result.** For weak Z measurement with $0\leq\kappa\leq1$, take

$$
M_0=\operatorname{diag}\left(\sqrt{(1+\kappa)/2},\sqrt{(1-\kappa)/2}\right),
$$
$$
M_1=\operatorname{diag}\left(\sqrt{(1-\kappa)/2},\sqrt{(1+\kappa)/2}\right).
$$

Their squared diagonal entries sum to one, proving completeness. A local zero meter C=q2 can realize these branches coherently: use Ry(C,β₀), CRy(A,C,β₁−β₀), where $\beta_0=\arccos\kappa$ and $\beta_1=\pi-\beta_0$. For A=i, the meter angle is βᵢ; its 0/1 amplitudes are precisely the two M entries. This constructs only this specified dilation, not a general native-instrument compiler.

The program requests two named probability outputs. Read each with measurement(name).value; the shortcut .probabilities is ambiguous when more than one probability output is present.

```python
theta, phase, strength = .87, -.39, .43
groups = s.weak(strength)
beta0 = math.acos(strength);beta1 = math.pi-beta0
c = fq.Circuit(3,dtype=D).ry(0,theta).p(0,phase).cx(0,1)
c.ry(2,beta0).cry(0,2,beta1-beta0)  # local meter q2 initially zero
out = fq.run(c,outputs=[fq.probabilities(qubits=(2,1),name="joint"),
    fq.probabilities(qubits=(0,),name="alice")],options=OPTIONS)
s.RUNS += 1
_, v = s.fixture(theta,phase)
report = s.analyze(v,(0,),groups,(1,),s.projectors("Z"))
assert torch.allclose(out.measurement("joint").value[0].reshape(2,2),report["joint"],atol=ATOL,rtol=0)
assert torch.allclose(report["marginal"],torch.tensor([math.cos(theta/2)**2,math.sin(theta/2)**2],dtype=torch.float64),atol=ATOL,rtol=0)
for meter,group in enumerate(groups):
    assert torch.allclose(out.statevector()[0][meter::2],s.apply(v,group[0],(0,)),atol=ATOL,rtol=0)
assert torch.allclose(out.measurement("alice").value[0],report["baseline"],atol=ATOL,rtol=0)
for kappa in (0.,1.):s.dilation(kappa,theta,phase)
print("Three native weak-meter fixtures:complete M0/M1 branches preserve Bob;named probability outputs read explicitly.")
```

```text
Three native weak-meter fixtures:complete M0/M1 branches preserve Bob;named probability outputs read explicitly.
```

All three native fixtures leave Bob's marginal unchanged, including strength endpoints zero and one. Selecting a meter branch remains classical analysis of the unmeasured joint vector. No native sampled collapse or remote conditional execution is claimed.

<span id="formula-code-7-7-discard"></span>

### 7.7.5 — Include discarded records, local resets and local control

**Formula.** A local reset model has one visible outcome and two hidden operators,

$$
\begin{gathered}
R_0=|0\rangle\langle0|,\qquad R_1=|0\rangle\langle1|,\\
R_0^\dagger R_0+R_1^\dagger R_1=I.
\end{gathered}
$$

For $|\Psi\rangle=c|00\rangle+e^{i\phi}s|11\rangle$, the two hidden branches are $c|00\rangle$ and $e^{i\phi}s|01\rangle$. Predictions must add their quadratic forms; adding the vectors would invent a coherent Bob superposition that the discarded record does not supply.

**Derivation and finite-operation scope.** The complete-process proof immediately preserves Bob's probabilities for this reset. It also includes a single local unitary U as the one-operator family, since $U^\dagger U=I$. If Alice applies an outcome-dependent local unitary $V_a$ after $M_a$, the operators are $V_aM_a$ and

$$
\sum_a M_a^\dagger V_a^\dagger V_aM_a
=\sum_a M_a^\dagger M_a=I.
$$

More general finite local adaptive procedures remain complete. At a history h, let the next local operations be $N_{j|h}$ with $\sum_jN_{j|h}^\dagger N_{j|h}=I$. For the accumulated branch Kₕ,

$$
\sum_j(N_{j|h}K_h)^\dagger(N_{j|h}K_h)=K_h^\dagger K_h.
$$

Summing from the leaves of a finite decision tree back to its root gives identity. Keeping or forgetting labels merely groups these leaf operators. Thus local feedback does not evade the theorem.

A local ancillary unitary followed by forgetting an ancilla also fits. With ancilla initialized in |0⟩, its operators are $K_j=(I_{A'}\otimes\langle j|)U(I_A\otimes|0\rangle)$. Inserting $\sum_j|j\rangle\langle j|=I$ between $U^\dagger,U$ proves $\sum_jK_j^\dagger K_j=I$. These identities cover finite standard local preparations, gates, measurements, local controls and discards. For any specified finite ensemble of initial pure states with fixed weights independent of x, applying the result to each component and averaging preserves the same equality. No density-operator update is silently assumed as a prerequisite.

**FlagQuantum code and verification result.** A native coherent fixture implements $|i\rangle_A|0\rangle_C\mapsto|0\rangle_A|i\rangle_C$ by CX(A,C), CX(C,A). Its full output is

$$
|0\rangle_A\left(c|00\rangle+e^{i\phi}s|11\rangle\right)_{BC}.
$$

Alice's original qubit is zero, while its correlations have moved to her local meter. Forgetting that meter gives the reset predictions. This is an explicitly executed isometry on the zero-meter input subspace, not a native reset call or a hardware dissipation model.

```python
hidden = s.reset_groups()
reset_report = s.analyze(v,(0,),hidden,(1,),s.projectors("X"))
assert len(reset_report["columns"])==1 and len(reset_report["columns"][0])==2
assert abs(float(reset_report["weights"][0])-1)<ATOL
assert torch.allclose(reset_report["marginal"],reset_report["baseline"],atol=ATOL,rtol=0)
native, meter_joint = s.dilation(theta=theta,phase=phase,kind="reset")
target = torch.zeros(8,dtype=D)
target[0]=math.cos(theta/2);target[3]=complex(math.cos(phase),math.sin(phase))*math.sin(theta/2)
assert torch.allclose(native,target,atol=ATOL,rtol=0)
print("Native two-CX isometry:Alice=0,Bob-meter correlations retained;hidden branches are not added as vectors.")
```

```text
Native two-CX isometry:Alice=0,Bob-meter correlations retained;hidden branches are not added as vectors.
```

The environment that stores the discarded information matters to the joint state, even though Bob's unconditioned probabilities remain unchanged.

<span id="formula-code-7-7-selection"></span>

### 7.7.6 — Expose three incorrect routes to an apparent signal

**Formula.** First consider the unequal resource $c|00\rangle+e^{i\phi}s|11\rangle$, with $c=\cos(\theta/2)$ and $s=\sin(\theta/2)$. Alice's Z outcomes have probabilities $c^2,s^2$. The correctly weighted Bob Z probability is

$$
p_B(0)=c^2\cdot1+s^2\cdot0=c^2.
$$

An equal-weight average of the normalized branches instead gives one half. Ignoring an outcome does not mean forgetting its probability weight.

Second, Phi+ with Alice Z measurement gives $p_B(0\mid a=0)=1$ but $p_B(0)=1/2$. Keeping only a=0 is postselection. Its unnormalized success joint probability is one half; it becomes one only after dividing by success probability one half. The single filter $F=|0\rangle\langle0|$ has $F^\dagger F\ne I$. It is not a deterministic complete process.

Third, the vectors |0⟩ and |1⟩, each with weight one half, cannot be replaced by the normalized vector sum |+⟩. The ensemble predicts Bob X=+ with probability one half; |+⟩ predicts one. Changing the unobservable phase of one measured branch would even change that false vector-average prediction.

**Why this does not enable communication.** Alice's local decision to retain a record does not delete Bob's other records. Bob needs an acceptance label, an agreed record match or another physical indication to identify the selected subset. If detection or transmission timing carries that indication, it is itself a communication channel, outside the no-channel assumption. Alice also cannot convert a probabilistic filter into deterministic nonlinear renormalization by simply declaring its failed outcomes absent.

**Code and verification result.** One new native unequal-resource run checks the weights; the earlier native Bell runs supply the other two comparisons. The incomplete-filter contract is rejected before another native execution. A separate explicit floating-point reference retains a positive probability near $10^{-20}$; it is not a native tiny-amplitude preparation claim.

```python
unequal = s.query(.83,.47,"Z","Z")
weighted = sum(float(p)*q for p,q in zip(unequal["weights"],unequal["conditional"]))
unweighted = sum(unequal["conditional"])/2
assert torch.allclose(weighted,unequal["baseline"],atol=ATOL,rtol=0)
assert abs(float(unweighted[0]-weighted[0]))>.1
assert abs(float(reports[("Z","Z")]["conditional"][0][0])-1)<ATOL
assert abs(float(reports[("Z","Z")]["marginal"][0])-.5)<ATOL
wrong_vector = torch.tensor([1,1],dtype=D)/math.sqrt(2)
wrong_p = float(torch.vdot(wrong_vector,s.projectors("X")[0]@wrong_vector).real)
assert abs(wrong_p-1)<ATOL
assert abs(float(reports[("Z","X")]["marginal"][0])-.5)<ATOL
before = s.RUNS
try:s.instrument(((s.P0,),),2)
except ValueError:pass
else:raise AssertionError("Incomplete deterministic filter admitted")
assert before==s.RUNS
rare = s.analyze(torch.tensor([1,0,0,1e-10],dtype=D),(0,),s.groups_for("Z"),(1,),s.projectors("Z"))
assert float(rare["weights"][1])>0
print("Unequal weights,success-only postselection and normalized-vector averaging expose three different mistakes.")
print("Incomplete filter rejected before another native run;positive1e-20branch retained.")
```

```text
Unequal weights,success-only postselection and normalized-vector averaging expose three different mistakes.
Incomplete filter rejected before another native run;positive1e-20branch retained.
```

The complete program also checks that zero-probability branches have no normalized conditional distribution, and that a nonzero projected column whose squared norm underflows raises an explicit error. A numerical threshold is not permission to delete rare physical outcomes.

<span id="formula-code-7-7-message"></span>

### 7.7.7 — State what a classical message permits Bob to do

**Formula.** In the Phi+ Z example, Bob's branch is |a⟩. If a classical record a arrives, Bob may apply $X^a$ to obtain |0⟩ on every branch. Before receipt his Z=0 probability is one half; after the record-dependent correction it is one.

This does not contradict the theorem. The total protocol now contains Bob operations chosen using information from Alice. Its branch operators act on both systems, not just A:

$$
L_a=P_a\otimes X^a.
$$

Although the total process is normalized, it is not of the form $M_a\otimes I_B$ required by the Alice-only statement.

For Alice X measurement, Bob's branch is $Z^a|+\rangle$. If both the basis setting and a are known, he applies Zᵃ, then H:

$$
H Z^a Z^a|+\rangle=|0\rangle.
$$

**Derivation of the distinction.** Merely learning a changes which subset of existing records is being predicted. Actually applying a correction changes Bob's subsequent local experiment. Both actions use available classical information; neither is an Alice-only mechanism for altering an unlabelled remote distribution. A pre-agreed basis does not reveal Alice's unpredictable outcome.

**FlagQuantum code and verification result.** Four fresh static one-qubit runs prepare the simulator-known conditional fixtures and execute the selected correction gates. The host is given the presumed received record. These are checks of the correction logic, not a native classical-network or mid-circuit feedback implementation on the retained physical Bob system.

```python
for basis,a in itertools.product(("Z","X"),(0,1)):
    # Fresh known conditional-state fixtures,not native mid-circuit feedback.
    c = fq.Circuit(1,dtype=D)
    if basis=="Z":
        if a:c.x(0)  # prepare |a>
        if a:c.x(0)  # message-dependent X^a
    else:
        c.h(0)
        if a:c.z(0)  # prepare +/- branch
        if a:c.z(0)  # message-dependent Z^a
        c.h(0)
    out = fq.run(c,outputs=[fq.probabilities(),fq.samples()],shots=17,options=OPTIONS)
    s.RUNS += 1
    assert torch.allclose(out.statevector()[0],torch.tensor([1,0],dtype=D),atol=ATOL,rtol=0)
    assert bool((out.samples==0).all())
print("Four fresh native Bob fixtures:received basis/outcome allow correction to |0>;this is not Alice-only signalling.")
```

```text
Four fresh native Bob fixtures:received basis/outcome allow correction to |0>;this is not Alice-only signalling.
```

Teleportation needs its two classical outcome bits for this reason. Superdense coding instead changes Bob's accessible system when a qubit is physically delivered. Neither protocol is a counterexample to the fixed-system, no-communication theorem. If the parties are spacelike separated and no classical or quantum carrier can arrive, these resources are unavailable. The physical causal propagation restriction is a separate assumption; the matrix proof shows that entanglement alone adds no signalling channel.

<span id="formula-code-7-7-records"></span>

### 7.7.8 — Compare whole records without mistaking fluctuation for a signal

**Formula.** The theorem applies to every Bob effect, not just Pauli means. A finite Bob protocol that adapts its measurement to its own past record has leaf operators Tₕ. The same decision-tree calculation as in 7.7.5 gives $\sum_hT_h^\dagger T_h=I$. Its complete-record effects are $E_h=T_h^\dagger T_h$. Applying the complete-process proof to each Eₕ shows that every local record probability is independent of Alice's setting. Any decision rule on those records just sums such probabilities and is likewise independent.

Independence between repetitions is **not** needed for this fundamental statement: one can group the entire fixed shared preparation into a larger finite A/B system. It is needed for the following simple sampling bound. Assume two independent batches, each of N independent, identically prepared Bernoulli records for the same Bob event probability p. For the empirical difference $\widehat d=\widehat p_x-\widehat p_{x'}$,

$$
\mathbb E\widehat d=0,\qquad
\operatorname{Var}(\widehat d)=\frac{2p(1-p)}N\leq\frac1{2N}.
$$

**Derivation.** Each indicator has variance p(1−p); independent averaging divides by N, and independent batch differences add the two variances. The inequality follows from $p(1-p)=1/4-(p-1/2)^2\leq1/4$. On $|\widehat d|\geq\epsilon$, the nonnegative variable $\widehat d^2$ is at least ε², so

$$
\epsilon^2\Pr(|\widehat d|\geq\epsilon)
\leq\mathbb E\widehat d^2
\leq\frac1{2N}.
$$

Thus $N\geq1/(2\delta\epsilon^2)$ suffices for probability at most δ. This is a fixed-budget model bound, not a certificate of hardware independence or a stopping rule.

**FlagQuantum code and verification result.** Two actual terminal-sample batches use different Alice bases on a complex, nonmaximal resource in ordered four-qubit support (q3,q0). Their exact Bob probabilities agree, while finite counts need not. N=160, ε=1/4, δ=1/20 satisfy the bound. The code checks structure and exact probabilities; it does not require equal counts or require a random interval to contain its target.

```python
N, epsilon, delta = 160, .25, .05
rZ = s.query(.91,-.63,"Z","Z",n=4,pair=(3,0),shots=N,seed=73)
rX = s.query(.91,-.63,"X","Z",n=4,pair=(3,0),shots=N,seed=79)
assert torch.allclose(rZ["marginal"],rX["marginal"],atol=ATOL,rtol=0)
for report in (rZ,rX):
    assert int(report["counts"].sum())==N
    assert 0<=int(report["bits"][:,1].sum())<=N
assert 1/(2*N*epsilon**2)<=delta
assert s.RUNS==21
print("Two fixed160record batches:exact Bob probabilities agree;random count equality is not required.")
print("IID model bound on a frequency difference>=1/4:at most1/20;21native body circuits total.")
```

```text
Two fixed160record batches:exact Bob probabilities agree;random count equality is not required.
IID model bound on a frequency difference>=1/4:at most1/20;21native body circuits total.
```

A repeatable difference between exact simulator marginals would indicate a reference, indexing or locality-contract error to investigate. A finite empirical difference alone does not establish signalling. Source changes correlated with x, selective record loss or a physical cross-party gate violate the assumptions and must be diagnosed separately.

### Complete execution and implementation boundaries

Run the complete program and the literal-body checker:

~~~bash
python examples/foundations/no_signalling.py
python scripts/check_no_signalling_prose.py
~~~

The program checks Bell, unequal and product inputs, all nine local basis pairs and all twenty ordered two-qubit supports across two-, three- and four-qubit registers. Three generic native preparations support 302 additional classical local-instrument/effect checks, including nonadjacent composite local supports. Weak/reset coherent fixtures and the four fresh Bob correction fixtures are counted as actual native executions; classical branch/effect calculations are not quantum executions.

Sixteen malformed contracts are rejected before another native run: incomplete/empty/non-normalized local operator families; incomplete/nonpositive Bob effects; nonnormalized/wrong-dtype global input; overlapping/out-of-range supports; invalid weak strength; unknown basis; invalid shots/seed; and a nonliteral classical bit. Positive rare outcomes are retained, impossible branches remain undefined, and positive squared-norm underflow is explicit. The reference's two-to-four-qubit limit is a teaching bound, not a FlagQuantum capacity limit.

Expected output of the complete program:

```text
27 native circuits:Bell,unequal and product inputs;all nine basis pairs,complex Y branches and unchanged Bob marginals passed.
60 native circuits:all20ordered supports,complex spectators and independent full amplitudes passed.
3 native generic preparations and302classical complete-instrument/effect cases passed,including ordered composite local supports.
6 native coherent dilation fixtures:weak meter/reset-isometry marginals match classical branches;no collapse/reset endpoint claimed.
4 native fresh Bob branch fixtures:record-dependent corrections give zero only after assumed classical receipt.
16malformed contracts rejected;positive1e-20branch retained,zero branch undefined and nonzero-norm underflow explicit.
100CPUcomplex128native circuits passed;postselection and classical communication are not Alice-only nonselective operations.
```

The first author run completed 90 native preparations/analyzers and then one weak-meter execution before an ambiguous multiple-probability accessor raised an error. That initial source and captured output remain archived. The correction uses named measurement results; it does not change the physical reference or relax tolerances, and is not a claimed native framework bug. The corrected full program and all literal body units were executed. Independent mathematical/implementation review and reader trial remain pending.

### Understanding checks and transfer exercises

**7.7-A — Locate the exact cancellation.** Reproduce the complete-projector proof with an entangled input of arbitrary finite dimensions. Identify the line that fails if Alice keeps only one outcome. Explain why a zero-probability branch does not require defining a conditional state.

**7.7-B — Keep the hidden label hidden.** For $c|00\rangle+e^{i\phi}s|11\rangle$, compute Bob's X probabilities after the one-visible-outcome reset family R₀,R₁. Compare with adding and normalizing its two hidden branch vectors. What local environment holds the missing coherence in the native two-CX fixture?

**7.7-C — Fresh complex, ordered-support experiment.** Use θ=1.03, φ=−.52 with (A,B)=(q2,q0) in four qubits. Use the helper's spectator preparation Ry(.39+.11j), P(−.17(j+1)) at j=1,3. Derive Bob's conditional Pauli means for Alice X and Y outcomes, then verify all nine local basis pairs. Predict Bob's unconditioned Z=0 probability. Extend the classical check to three trine effects $E_j=(2/3)|t_j\rangle\langle t_j|$, where $|t_j\rangle=(|0\rangle+e^{2\pi i j/3}|1\rangle)/\sqrt2$ and j=0,1,2.

**7.7-D — Explain the purported faster-than-light protocol.** Alice chooses Z or X, retains only a=0, and claims Bob can tell the choice because his retained states are |0⟩ or |+⟩. State what record Bob actually has before any message and what extra data identifies Alice's subset. If she sends the labels and Bob corrects every branch, identify the changed premise. Under the IID batch assumptions, find N per batch for ε=.1,δ=.05.

<details markdown="1">
<summary>Answers and verification guidance for 7.7-A–D</summary>

**A.** Expand each squared joint norm to $\langle\Psi|P_{a|x}\otimes Q_{b|y}|\Psi\rangle$ and sum all a. The replacement $\sum_aP_{a|x}=I_A$ yields Bob's original probability. A proper selected sum is generally a nonidentity projector, so that replacement is unavailable. A zero branch is the zero vector and contributes zero joint probabilities; only division by its zero weight is forbidden.

**B.** Bob's correct X distribution is (1/2,1/2), because summing the two hidden quadratic forms removes cross terms. Adding the vectors would give $c|0\rangle+e^{i\phi}s|1\rangle$, falsely predicting $p_X(0)=(1+\sin\theta\cos\phi)/2$. In the coherent native fixture, the meter carries the orthogonal labels 0,1 and remains correlated with B. Ignoring it requires summing probabilities, not erasing its label coherently.

**C.** Write c=cos(θ/2), s=sin(θ/2). Alice X outcome a gives Bob $c|0\rangle+(-1)^ae^{i\phi}s|1\rangle$, with probability one half. Its Pauli means are

$$
\begin{aligned}
\langle X\rangle_a&=(-1)^a\sin\theta\cos\phi,\\
\langle Y\rangle_a&=(-1)^a\sin\theta\sin\phi,\\
\langle Z\rangle_a&=\cos\theta.
\end{aligned}
$$

For Alice Y the relative phase is φ−π/2, so

$$
\begin{aligned}
\langle X\rangle_a&=(-1)^a\sin\theta\sin\phi,\\
\langle Y\rangle_a&=-(-1)^a\sin\theta\cos\phi,\\
\langle Z\rangle_a&=\cos\theta.
\end{aligned}
$$

The weights are again one half. All unconditioned results have Z=0 probability $\cos^2(.515)$ and X/Y=0 probability one half. The spectators stay normalized and cannot change these marginals. Trine off-diagonal entries sum to zero because $1+e^{2\pi i/3}+e^{4\pi i/3}=0$; diagonal entries sum to one, proving completeness. Each Bob trine probability is one third for this diagonal unconditioned qubit prediction. The printed parameters, all nine native basis pairs and classical trine cases are executed in transfer evidence; no native trine endpoint is claimed.

**D.** Bob holds all his records, with the same unlabelled probability distribution for either Alice basis. He needs her acceptance/outcome labels and a matching record convention to identify the selected subset. Sending those labels is classical communication. Applying a correction chosen from them adds Bob's record-dependent operation, so the protocol is no longer Alice-only. The batch bound gives $N\geq1/(2\cdot.05\cdot.1^2)=1000$ per batch. Neither a claimed postselected state nor an occasional frequency fluctuation supplies a signalling channel without that extra information.

</details>

**Sources.** The frozen locator is Nielsen and Chuang, *Quantum Computation and Quantum Information*, §2.2.8, “Composite systems,” beginning on printed page 93 ([NC:2.2.8 locator](../references/proof-sources.md#source-nc-2-2-8)); its stored status is a contents-locator check, not a new full-text review. For the complete-operator boundary, the author-hosted [Watrous, *The Theory of Quantum Information*, Chapter 2.2.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf), Theorem 2.26 and Corollary 2.27, printed pages 87–89 (PDF pages 95–97), were inspected for normalization/representation scope. Its full density-operator formalism is not assumed here: the necessary finite branch identities are proved locally above. These are original derivations and simulator checks, not a reproduction or redistribution of either textbook. Section 7.8 uses these distinctions when introducing entanglement swapping.

<!-- end-section-7.7 -->
