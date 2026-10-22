# 7. Entanglement and Quantum Information Protocols

**Working drafts: sections 7.1–7.2 · Writing Baseline 1.0 · October 22, 2026.** Author execution is recorded separately from independent mathematical review, implementation review and reader trial; all three remain pending. Examples use FlagQuantum 0.3.1, PyTorch 2.13.0 and CPU complex128 statevectors.

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

**Implementation boundary.** Section 7.1's initial tiny-angle failure is retained in [FlagQuantum issue #704](https://github.com/flagos-ai/FlagQuantum/issues/704). A returned zero amplitude at epsilon $10^{-14}$ did not establish that the intended state was a product. Here epsilon $10^{-10}$ uses the native path already verified to retain that amplitude. We make no claim that the smaller-angle behavior has been fixed.

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
