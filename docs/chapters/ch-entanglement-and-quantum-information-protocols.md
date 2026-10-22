# 7. Entanglement and Quantum Information Protocols

**Working drafts: sections 7.1–7.3 · Writing Baseline 1.0 · October 22, 2026.** Author execution is recorded separately from independent mathematical review, implementation review and reader trial; all three remain pending. Examples use FlagQuantum 0.3.1, PyTorch 2.13.0 and CPU complex128 statevectors.

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
