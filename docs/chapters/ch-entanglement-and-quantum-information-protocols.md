# 7. Entanglement and Quantum Information Protocols

**Working draft: section 7.1 · Writing Baseline 1.0 · October 22, 2026.** Author execution is recorded separately from independent mathematical review, implementation review and reader trial; all three remain pending. Examples use FlagQuantum 0.3.1, PyTorch 2.13.0 and CPU complex128 statevectors.

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

A product makes each difference zero by substitution. Conversely, if all minors vanish, choose $C_{rs}\ne0$. The minor with rows i,r and columns j,s, with a possible sign from their ordering, gives $C_{ij}C_{rs}=C_{is}C_{rj}$. The same factor construction therefore applies, proving rank one. This proves the equivalence in every finite rectangular dimension, not just for two qubits.

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
