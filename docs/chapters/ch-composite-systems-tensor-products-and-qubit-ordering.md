# 4. Composite Systems, Tensor Products, and Qubit Ordering

**Working drafts: sections 4.1–4.2 · Writing Baseline 1.0 · October 21, 2026.** Author execution is recorded separately from independent mathematical, implementation and reader review, which remain pending. This is not an accepted chapter. Examples use released FlagQuantum 0.3.1 and PyTorch 2.13.0 on CPU with complex128 statevectors.

<span id="sec-composite-systems-tensor-products-and-qubit-ordering-1"></span>

## 4.1 Tensor-product spaces and basis states

Two independently prepared qubits need a joint description that retains the amplitude for every pair of basis labels. Concatenating their two-coordinate statevectors would store four numbers, but those would be the original individual amplitudes, not the joint amplitudes. We need a mathematical construction that specifies both the new space and the rule for combining independent preparations.

The prerequisites are [2.2](ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-2), for inner products and orthogonality, [2.3](ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-3), for bases and linear maps, and [3.1](ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-1), for pure-state representatives. We will construct a finite tensor-product space, prove its dimension and product-basis orthonormality, then translate independent complex amplitudes into code.

The code fragments below are cumulative: run them in order from the repository root in the pinned example environment. Each displayed output is checked by executing these fragments, separately from the complete example at the end. Finite examples test the translation; the proofs establish the general statements.

### Construct the space before interpreting its states

Let $V$ and $W$ be complex inner-product spaces of positive finite dimensions $m$ and $n$. Choose ordered orthonormal bases $f_0,\ldots,f_{m-1}$ and $g_0,\ldots,g_{n-1}$. For this construction, make one formal basis label $E_{ij}$ for each pair $(i,j)$ and let

$$
V\otimes W=\left\{\sum_{i=0}^{m-1}\sum_{j=0}^{n-1}z_{ij}E_{ij}:z_{ij}\in\mathbb C\right\}.
$$

Addition and scalar multiplication act on the coefficients. Different coefficient arrays specify different vectors. We write $E_{ij}=f_i\otimes g_j$; the symbol $\otimes$ is read “tensor product.”

For arbitrary $v=\sum_i a_i f_i$ and $w=\sum_j b_j g_j$, **define**

$$
v\otimes w=\sum_{i,j}a_i b_j E_{ij}.
$$

A vector of this form is a **product vector**. The product is bilinear: for example, expanding its coefficients gives

$$
(v+v')\otimes w=v\otimes w+v'\otimes w,\qquad
v\otimes(w+w')=v\otimes w+v\otimes w',
$$

and for every complex scalar $\lambda$,

$$
(\lambda v)\otimes w=\lambda(v\otimes w)=v\otimes(\lambda w).
$$

The coefficient at $(i,j)$ in the first identity is $(a_i+a_i')b_j=a_ib_j+a_i'b_j$; the other identities follow from the corresponding distributive and scalar multiplication rules. No conjugation appears here. Tensoring vectors is bilinear, while an inner product conjugates its first argument.

**Formula → code: the coefficient $a_i b_j$.** The two nested loops implement the two finite sums' ordered coefficients; they do not concatenate the inputs or take an inner product.

```python
def tensor(a, b):
    return [x * y for x in a for y in b]

v, w = [1, 2j], [3, 4, 5]
print(tensor(v, w))
```

```text
[3, 4, 5, 6j, 8j, 10j]
```

The second factor varies fastest. These vectors are intentionally unnormalized: bilinearity is a vector-space rule, not a rule limited to physical states.

This construction does not restrict the space to single products. It includes every coefficient array $z_{ij}$, whether or not that array can be written as $a_i b_j$.

### Why this construction captures bilinear combinations

Suppose $F(v,w)$ is any bilinear rule taking pairs from $V,W$ into another vector space. Define a linear rule on the constructed space by

$$
\widetilde F\!\left(\sum_{i,j}z_{ij}E_{ij}\right)
=\sum_{i,j}z_{ij}F(f_i,g_j).
$$

Its value on a product is $\sum_{i,j}a_i b_j F(f_i,g_j)=F(v,w)$, by bilinearity. It is the unique linear rule with this property, since its value on every $E_{ij}=f_i\otimes g_j$ is fixed. Thus a bilinear operation on two inputs can be represented as a linear operation on their tensor product. This extension property explains the construction beyond its array layout. Any other construction with the same property has mutually inverse linear maps to this one: their compositions agree with the identity on every product, so uniqueness makes both compositions identities. Choosing coordinates does not create a different physical system.

### Prove orthonormality and dimension

Equip the constructed space with the inner product

$$
\left\langle\sum_{i,j}z_{ij}E_{ij},\sum_{i,j}t_{ij}E_{ij}\right\rangle
=\sum_{i,j}z_{ij}^*t_{ij}.
$$

It is conjugate-linear in the first argument, linear in the second, and conjugate symmetric. Its squared norm is $\sum_{i,j}|z_{ij}|^2$, positive unless every coefficient is zero, so it is an inner product in the sense of 2.2.

A basis label has one coefficient equal to one and the others zero. Substitution gives

$$
\langle E_{ij}|E_{k\ell}\rangle
=\delta_{ik}\delta_{j\ell}
=\langle f_i|f_k\rangle\langle g_j|g_\ell\rangle,
$$

where $\delta_{ik}$ is one if $i=k$ and zero otherwise. The product labels are therefore orthonormal. They span by construction. If $\sum_{i,j}z_{ij}E_{ij}=0$, taking the inner product with $E_{k\ell}$ gives $z_{k\ell}=0$ for every pair, proving linear independence. There are $mn$ such pairs, hence

$$
\dim(V\otimes W)=mn.
$$

Dimensions multiply; they do not add. Two qubits give $2\times2=4$ basis vectors, but that example alone hides the difference because $2+2$ also happens to equal four. A two-dimensional and a three-dimensional factor give six product-basis vectors, not five. Repeating the dimension argument for $r$ qubits gives $2^r$ coordinates. This counts coordinates in a state description, not bits obtainable from one measurement.

**Formula → code: $\delta_{ik}\delta_{j\ell}$ and $mn$.** Build the six basis vectors for dimensions two and three, then evaluate every entry of their Gram matrix. `gram[p][q]` represents the inner product between basis vectors numbered `p` and `q`.

```python
def dot(x, y):
    assert len(x) == len(y)
    return sum(complex(a).conjugate() * b for a, b in zip(x, y))

basis = [tensor([int(k == i) for k in range(2)],
                [int(k == j) for k in range(3)])
         for i in range(2) for j in range(3)]
gram = [[dot(x, y) for y in basis] for x in basis]
assert gram == [[int(p == q) for q in range(6)] for p in range(6)]
print(len(basis), len(basis[0]), "Gram matrix is I6")
```

```text
6 6 Gram matrix is I6
```

The first number counts basis vectors; the second counts coordinates in each vector. The assertion checks all 36 overlaps. It illustrates the proved dimension statement for one pair of dimensions; it does not prove it for all $m,n$.

### Derive the product inner product and normalization

For products with coefficients $a_i,b_j$ and $a_i',b_j'$, the defined inner product gives

$$
\begin{aligned}
\langle v\otimes w|v'\otimes w'\rangle
&=\sum_{i,j}(a_i b_j)^*a_i'b_j'\\
&=\sum_{i,j}(a_i^*a_i')(b_j^*b_j')\\
&=\left(\sum_i a_i^*a_i'\right)
  \left(\sum_j b_j^*b_j'\right)\\
&=\langle v|v'\rangle\langle w|w'\rangle.
\end{aligned}
$$

All sums are finite, so the regrouping uses distributivity without a convergence assumption. Taking the two products equal yields

$$
\|v\otimes w\|^2=\|v\|^2\|w\|^2,
\qquad \|v\otimes w\|=\|v\|\|w\|.
$$

Thus two unit representatives produce a unit representative; a zero factor produces the zero vector, which cannot describe a pure state. If one factor is orthogonal to its comparison partner, the product inner product is zero regardless of the other factor. A common phase on either factor becomes a common phase on the whole product, as bilinearity already showed.

**Formula → code: factorized inner products and squared norms.** Use the same scalar `tensor` and `dot` functions, with comparison vectors that are neither identical nor orthogonal:

```python
vp, wp = [1j, 1], [1, -1j, 2]
left = dot(tensor(v, w), tensor(vp, wp))
right = dot(v, vp) * dot(w, wp)
assert left == right
norm2 = dot(tensor(v, w), tensor(v, w)).real
assert norm2 == dot(v, v).real * dot(w, w).real
print(left, right)
print(norm2)
```

```text
(-4-13j) (-4-13j)
250.0
```

Conjugation belongs inside `dot`, where the derivation requires it. It does not belong inside `tensor`. Exact integer-complex arithmetic in this fixture makes equality appropriate; the normalized simulator example below uses a stated floating-point tolerance.

### State the physical composition assumption

For distinguishable qubits in this register model, we adopt the following physical assumption: the joint state space is the tensor product of the subsystem spaces, and independent pure preparations $|\psi\rangle_A$, $|\phi\rangle_B$ give the joint representative $|\psi\rangle_A\otimes|\phi\rangle_B$. This is a composition postulate, not a conclusion forced by the preceding vector-space algebra.

A joint computational-basis measurement assigns each joint label the squared modulus of its normalized coordinate. This is the finite-basis Born rule used for the register model. For an independent product, it gives

$$
p(i,j)=|a_i b_j|^2=|a_i|^2|b_j|^2.
$$

The sum is one because $(\sum_i|a_i|^2)(\sum_j|b_j|^2)=1$. The factorization follows for this specified pure product preparation; it is not an assumption about every possible joint state.

For two qubits write $|ij\rangle=|i\rangle_A\otimes|j\rangle_B$. In this section use the ordered basis

$$
|00\rangle,\ |01\rangle,\ |10\rangle,\ |11\rangle.
$$

For each first-factor index, enumerate the second-factor indices in order. Then

$$
\begin{pmatrix}a_0\\a_1\end{pmatrix}
\otimes\begin{pmatrix}b_0\\b_1\end{pmatrix}
=\begin{pmatrix}a_0b_0\\a_0b_1\\a_1b_0\\a_1b_1\end{pmatrix}.
$$

This is the **Kronecker-product representation** of the vector product. For general dimensions, coordinate $(i,j)$ occupies index $in+j$ in this explicitly chosen enumeration. Section 4.2 develops register bit strings and basis indices systematically; here the ordered pairs suffice.

Changing the factor order is not a harmless replacement under fixed subsystem labels. The arrays for $v\otimes w$ and $w\otimes v$ enumerate different ordered pairs and generally differ. Translating between those conventions requires a specified relabeling; permutations and SWAP are treated in 4.5.

### Work through complex amplitudes before using a library

Take the normalized preparations

$$
a=\begin{pmatrix}3/5\\4i/5\end{pmatrix},\qquad
b=\frac1{\sqrt2}\begin{pmatrix}1\\i\end{pmatrix}.
$$

Multiply each first-factor amplitude by both second-factor amplitudes:

$$
a\otimes b
=\frac1{5\sqrt2}\begin{pmatrix}3\\3i\\4i\\-4\end{pmatrix}.
$$

The last entry is negative because $(4i)i=-4$. Squared moduli give joint probabilities $(9/50,9/50,16/50,16/50)=(0.18,0.18,0.32,0.32)$. Their sum is one.

**Formula → code: the four amplitudes and their probabilities.** Python's `1j` denotes $i$; a squared modulus is `abs(z)**2`.

```python
from math import sqrt

a, b = [3/5, 4j/5], [1/sqrt(2), 1j/sqrt(2)]
hand = tensor(a, b)
expected = [z/(5*sqrt(2)) for z in [3, 3j, 4j, -4]]
assert all(abs(x-y) < 1e-12 for x, y in zip(hand, expected))
print([round(abs(z)**2, 2) for z in hand])
```

```text
[0.18, 0.18, 0.32, 0.32]
```

If a program conjugates $b$ during the construction, it instead produces $(3,-3i,4i,4)^T/(5\sqrt2)$. That wrong vector has the same norm and the same computational-basis probabilities, but different relative phases. This is why the example verifies complex amplitudes, not only probabilities.

**Formula → code: detect the phase error that probabilities miss.** A correct norm and correct basis probabilities are insufficient evidence for the statevector:

```python
wrong = tensor(a, [complex(z).conjugate() for z in b])
same_probabilities = all(abs(abs(x)**2-abs(y)**2) < 1e-12
                         for x, y in zip(hand, wrong))
assert abs(dot(hand, wrong)) < 1e-12
print(same_probabilities, round(abs(dot(hand, wrong)), 12))
```

```text
True 0.0
```

The zero overlap shows that the wrong and intended normalized vectors are orthogonal, despite agreeing on this one measurement's probabilities.

General joint vectors need not be products. For $(|00\rangle+|11\rangle)/\sqrt2$, nonzero coefficients at 00 and 11 would require all four individual factor amplitudes to be nonzero. Their cross products at 01 and 10 would then also be nonzero, contradicting the given zero coefficients. The vector belongs to the tensor-product space but cannot be one product vector. Such pure states are called entangled; their systematic treatment is in Chapter 7.

### Runnable verification and actual FlagQuantum preparation

Run the complete example [tensor_spaces.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/tensor_spaces.py) in the [pinned environment](https://github.com/FlagQuantum/modern-quantum-computing#run-the-examples):

```bash
python -m pip install -r requirements-examples.txt
python examples/foundations/tensor_spaces.py
```

The independent scalar construction and library reference are:

```python
import torch

a = torch.tensor([.6, .8j], dtype=torch.complex128)
b = torch.tensor([1, 1j], dtype=torch.complex128) / sqrt(2)
hand = torch.tensor(tensor(a.tolist(), b.tolist()), dtype=torch.complex128)
reference = torch.kron(a, b)
torch.testing.assert_close(hand, reference, rtol=0, atol=1e-12)
print(tuple(reference.shape))
```

```text
(4,)
```

Here `a` and `b` have shape `(2,)`, not a simulator's batched shape `(1,2)`. No conjugation is inserted. The mathematical helper also tests non-normalized and zero vectors; the physical preparation helper separately requires a finite normalized complex128 vector.

To prepare an arbitrary specified qubit vector $(\alpha,\beta)^T$ in the simulator, the example supplies the matrix

$$
Q(\alpha,\beta)=\begin{pmatrix}\alpha&-\beta^*\\\beta&\alpha^*\end{pmatrix}.
$$

Its first column is the desired vector. Both columns have norm one, and their inner product is $-\alpha^*\beta^*+\beta^*\alpha^*=0$; therefore $Q^\dagger Q=I$. The program checks this property and uses the released generic-unitary API as an ideal preparation, without claiming a physical device calibration.

Here subsystem $A$ is qubit 0 and subsystem $B$ is qubit 1. The actual FlagQuantum 0.3.1 calls apply the two specified preparations separately:

```python
import flagquantum as fq
from examples.foundations.tensor_spaces import prepare_matrix, OPTIONS

circuit = fq.Circuit(2, dtype=torch.complex128)
circuit.unitary(0, unitary=prepare_matrix(a))
circuit.unitary(1, unitary=prepare_matrix(b))
result = fq.run(circuit, outputs=[fq.probabilities()], options=OPTIONS)
joint = result.statevector()[0]
torch.testing.assert_close(joint, reference, rtol=0, atol=1e-12)
print([round(x, 2) for x in result.probabilities[0].tolist()])
```

```text
[0.18, 0.18, 0.32, 0.32]
```

`OPTIONS` requires PyTorch CPU complex128 statevector execution and disables fallback and approximation. The program first verifies each preparation in a separate one-qubit circuit, then compares the two-qubit result with the hand vector and `torch.kron`. General tensor-product rules for local operators are deferred to 4.3; the API's specified one-qubit preparation behavior is tested here directly.

| Derived result | Executed evidence |
|---|---|
| Six product-basis vectors for dimensions 2 and 3 | Construct all labels, compare their six coordinates, and check the Gram matrix against $I_6$ |
| Bilinear coefficient construction | Scalar nested loops versus `torch.kron` on 243 complex vector pairs, including zero factors |
| Inner-product and norm factorization | Scalar conjugated sums and finite products over the same grid |
| Worked independent qubit preparations | Separate and joint released FlagQuantum runs, with exact ordered amplitude reference |
| Fixed two-qubit basis order | Four basis preparations checked against index $2i+j$ |
| Meaningful failure witnesses | Reversed factor order and unwanted conjugation, including a wrong vector with unchanged probabilities |

Expected output of the complete program:

```text
C2 tensor C3: 6 ordered basis vectors; Gram matrix is I6.
243 complex2x3 products: scalar/kron, bilinearity and factorized inner products agree.
Worked amplitudes: (3, 3i, 4i, -4)/(5*sqrt(2)); order 00,01,10,11.
FlagQuantum probabilities: (0.180000000, 0.180000000, 0.320000000, 0.320000000).
4 qubit-basis preparations, wrong factor order and unwanted conjugation witnesses checked.
Non-product coefficient witness and 6 invalid-preparation cases checked; atol=1e-12.
No qutrit execution, entangling preparation, shots or hardware claimed.
```

The 243 mathematical fixtures combine nine two-component vectors and 27 three-component vectors. This tests a dimension product different from four; it is not a claim that FlagQuantum executed a three-level subsystem. Simulator results must be finite CPU complex128 statevectors with float64 probabilities and batch shapes `(1,2)` or `(1,4)`. Comparisons use absolute tolerance $10^{-12}$ and zero relative tolerance. The preparation helper rejects zero/nonunit vectors, incorrect shape or dtype, NaN and infinity rather than repairing them. These are bounded author-run checks; they do not replace the proofs or independent review.

### Understanding checks and transfer problems

**4.1-A — Expand a new product.** Let $v=(1,i)^T/\sqrt2$ and $w=(2,-i)^T/\sqrt5$. Write all four product amplitudes in the stated order, derive their probabilities and check normalization.

**4.1-B — Prove an orthogonality consequence.** If $\langle v|v'\rangle=0$ and $w,w'$ are arbitrary finite vectors, prove the product overlap is zero. Does zero product overlap force both individual overlaps to be zero?

**4.1-C — Diagnose two implementation mistakes.** A program returns `[a0*b0, a1*b1]` for two qubits. Another returns the four coefficients of `kron(a, b.conj())`. Identify the mathematical rule each violates and explain which output checks detect the worked-case error.

**4.1-D — Space or single product?** For a two-dimensional first space and three-dimensional second space, state the dimension and number of product-basis labels. Does every vector in that space have to be a single product? Use the two-qubit counterexample to explain the distinction between spanning by product vectors and factorization into one product.

### Answers

**A.** The ordered amplitudes are $(2,-i,2i,1)^T/\sqrt{10}$; the last entry uses $i(-i)=1$. Probabilities are $(4,1,4,1)/10$, summing to one. Their pairwise factorization also follows from the separately normalized factors.

**B.** The derived inner-product rule gives $\langle v\otimes w|v'\otimes w'\rangle=0\cdot\langle w|w'\rangle=0$. The converse requires at least one factor overlap to vanish, not both: take orthogonal $v,v'$ and equal normalized $w=w'$.

**C.** The first omits the cross-label basis coefficients 01 and 10, producing two entries where four are required. The second inserts an unjustified conjugation into a bilinear product. In the worked case the wrong conjugation changes relative phases but not the norm or computational probabilities; complex-coordinate comparison detects it. Shape, ordering and amplitude checks serve different purposes.

**D.** The dimension is $2\times3=6$, with six ordered product-basis labels. A general vector is a linear combination of them. It need not be one product: the normalized 00-plus-11 vector above is a sum of two product-basis vectors whose coefficient constraints forbid a single factorization. Linear spanning is not the same assertion as factorability.

### Sources, scope, and next step

The assigned source is [NC:2.1.7](../references/proof-sources.md#source-nc-2-1-7), Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010), **printed pp.71–74**, especially bilinearity Eqs.(2.42)–(2.44), the product inner product Eq.(2.49), and the Kronecker representation on p.74. These pages were consulted. The explicit finite construction, linear-extension proof, basis/dimension proof, examples and program are original exposition.

For the separately stated physical composition assumption, supplementary **§2.2.8, printed pp.93–94**, especially Postulate 4 on p.94, was consulted. The finite-basis probability rule uses the measurement postulate of **§2.2.3, printed pp.84–85**, already introduced in its qubit form in 3.1. The mathematical definition does not itself establish either physical postulate.

Depth **F**: construct the finite product space, prove product-basis orthonormality and dimension, and derive product amplitudes, inner products and normalization. This section does not establish a general bit-string convention, local-operator tensor formulas, permutations or entanglement classification. The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/4.1.json) separates author execution from pending independent reviews. Continue with [4.2 Registers, labels, and basis indices](#sec-composite-systems-tensor-products-and-qubit-ordering-2).

<span id="sec-composite-systems-tensor-products-and-qubit-ordering-2"></span>

## 4.2 Registers, labels, and basis indices

A simulator returns an array. To interpret its entry at index 6, we need more than the number of qubits: we need the ordered subsystem labels, the basis of each subsystem, the significance of each bit and the meaning of the array's axes. A consistent convention makes those choices explicit before a state is prepared or a result is read.

The prerequisite is [4.1](#sec-composite-systems-tensor-products-and-qubit-ordering-1). We use its ordered product bases, the physical composition assumption for independently prepared pure qubits, and the finite-basis Born rule. No general local-operator embedding, permutation or measurement-update theorem is assumed here. Those have separate homes in later sections.

### An ordered register, rather than a set of names

An **n-qubit register**, in this section, is an ordered collection of n distinguishable qubits, with $n\geq1$. Each qubit has the specified ordered basis $(|0\rangle,|1\rangle)$. Write its application labels as

$$
L=(\ell_0,\ell_1,\ldots,\ell_{n-1}),\qquad
\mathcal H_L=\mathbb C^2_{\ell_0}\otimes\cdots\otimes\mathbb C^2_{\ell_{n-1}}.
$$

The subscripts identify tensor factors, not numbers to be added. The order determines how a bit tuple is read:

$$
|b_0\cdots b_{n-1}\rangle_L
=|b_0\rangle_{\ell_0}\otimes\cdots\otimes|b_{n-1}\rangle_{\ell_{n-1}},\qquad b_k\in\{0,1\}.
$$

For this book, position 0 is the **most significant** position: it has the largest binary weight. In the released FlagQuantum examples, position k is addressed as integer qubit k. A descriptive name such as `signal` has no intrinsic binary weight. The application associates that name with an integer explicitly; a Python dictionary's appearance does not define a physical layout.

Take $L=(\mathrm{signal},\mathrm{reference},\mathrm{flag})$. Then a label `110` means signal is in basis state 1, reference in basis state 1 and flag in basis state 0. It does not mean integer qubit 110. It also does not assert that an arbitrary register is already in this basis state.

<span id="formula-code-4-2-register-order"></span>

**Formula → FlagQuantum-facing code → checked result.** Run the cumulative Python blocks in this section in order, from the repository root in the pinned environment. The names below are application metadata; no named-register API is being claimed.

```python
from examples.foundations.register_indices import (
    register_labels, basis_index, basis_bits, prepare_basis,
)
labels = register_labels(('signal', 'reference', 'flag'))
print([(q, label, 2**(len(labels)-1-q))
       for q, label in enumerate(labels)])
```

```text
[(0, 'signal', 4), (1, 'reference', 2), (2, 'flag', 1)]
```

The first column is the integer used in `circuit.x(q)` or `circuit.unitary(q, ...)`; the last is the bit weight in a global basis index. Neither is a hardware-qubit assignment. Distinct names are required so that decoding an outcome does not assign two different positions to the same name.

### Derive the forward map from the product basis

Extend the pair enumeration in 4.1 by listing bit tuples lexicographically, with 0 before 1 at each position. The rightmost bit changes fastest. There are $2^n$ product-basis vectors by repeated application of 4.1's dimension result.

Let $J_n(b_0,\ldots,b_{n-1})$ be the zero-based position of one tuple in that list. Appending a final bit places two entries under each old prefix: prefix followed by 0, then prefix followed by 1. Therefore

$$
J_1(b_0)=b_0,\qquad J_{n+1}(b_0,\ldots,b_n)=2J_n(b_0,\ldots,b_{n-1})+b_n.
$$

Starting with $J_1=b_0$, substitute this relation once to get $J_2=2b_0+b_1$, and once more to get $J_3=4b_0+2b_1+b_2$. In general, if the formula holds for n, multiplication by 2 increases every old exponent by one and appending $b_n$ supplies the new exponent-zero term. Induction proves

$$
\boxed{J_n(b)=\sum_{k=0}^{n-1}b_k2^{n-1-k}.}
$$

It follows that $0\leq J_n(b)\leq\sum_{r=0}^{n-1}2^r=2^n-1$. These are exactly the legal positions of a length-$2^n$ statevector. This ordering is a representation choice, not an additional quantum-mechanical law.

<span id="formula-code-4-2-forward-index"></span>

**Formula → recurrence → actual basis preparation.** The loop below implements the recurrence directly. It then compares the predicted position with a released FlagQuantum preparation. The single-qubit X operation has matrix $\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)$, so it sends $|0\rangle$ to $|1\rangle$. The helper starts a three-qubit circuit in its zero basis state and calls `x(q)` at positions whose bits are 1. The general matrix-embedding proof is deferred to 4.3; here we check the actual preparation semantics.

```python
import torch
bits = (1, 1, 0)
j = 0
for b in bits:
    j = 2*j + b
assert j == basis_index(bits)
state, probability = prepare_basis(bits)
expected = torch.zeros(8, dtype=torch.complex128)
expected[j] = 1
# Check the whole vector, including phase, rather than only its largest entry.
torch.testing.assert_close(state, expected, rtol=0, atol=1e-12)
print('110 ->', j, '; occupied index:', int(probability.argmax()))
```

```text
110 -> 6 ; occupied index: 6
```

This is a non-palindromic test. Reversing the same three bits gives `011`, whose index is 3. A test using only `000`, `111` or `101` could miss a complete bit reversal.

### Prove the inverse and the bijection

For an integer $j\in\{0,\ldots,2^n-1\}$, define

$$
B_{n,k}(j)=\left\lfloor\frac{j}{2^{n-1-k}}\right\rfloor\bmod2,\qquad k=0,\ldots,n-1.
$$

Here floor means integer quotient, and modulo 2 returns the remainder 0 or 1. To show this recovers $b_k$ from $j=J_n(b)$, separate the sum into more significant positions, position k and less significant positions:

$$
j=2^{n-k}A+b_k2^{n-1-k}+r,\qquad 0\leq r<2^{n-1-k},
$$

where $A=\sum_{h<k}b_h2^{k-1-h}$ is an integer. Division and floor give $2A+b_k$; modulo 2 removes the even term $2A$. Consequently $B_{n,k}(J_n(b))=b_k$, including the last position where $r=0$.

We must also check the other direction, rather than assume that a left inverse covers every integer. Euclidean division writes $j=2q+r_0$ uniquely with $r_0\in\{0,1\}$. Dividing q again gives its final bit; repeat n times. Because $j<2^n$, the quotient after n divisions is zero. Reversing these equalities reconstructs

$$
j=\sum_{k=0}^{n-1}B_{n,k}(j)2^{n-1-k}=J_n(B_n(j)).
$$

Both compositions are identities. The map is therefore a bijection: no two tuples share an index, and no legal index is omitted. The proof uses exact integers and establishes the result for every finite n in scope; a numerical test alone would not do that.

<span id="formula-code-4-2-inverse-index"></span>

**Formula → integer quotient/remainder → decoded result.** In Python, `//` is integer quotient and `%` is remainder. The register size remains an input because the integer 3 by itself does not tell us how many leading zeros to retain.

```python
recovered = tuple((j // 2**(3-1-k)) % 2 for k in range(3))
assert recovered == basis_bits(j, 3) == (1, 1, 0)
print(dict(zip(labels, recovered)))
print('index 3, width 4:', basis_bits(3, 4))
```

```text
{'signal': 1, 'reference': 1, 'flag': 0}
index 3, width 4: (0, 0, 1, 1)
```

The same integer 3 labels `11` in a two-qubit register, `011` in a three-qubit register and `0011` in a four-qubit register. Dropping the width loses part of the state-coordinate convention.

### Validate the convention independently of the helpers

A forward map and inverse could both contain the same reversal bug and still pass a round-trip test. To avoid that circular check, the complete program also uses Python's independent base-two string parser and fixed-width formatter for all 510 tuples of sizes 1 through 8. These mathematical checks allocate no quantum statevectors.

The required simulator check is smaller and exhaustive: every two-qubit and three-qubit basis input. For each input the reference places amplitude 1 at the index obtained from independent binary-string parsing, amplitude 0 elsewhere, and checks every complex coordinate and probability returned by FlagQuantum.

<span id="formula-code-4-2-basis-preparations"></span>

**Formula → independent reference → all 12 actual preparations.** The following block makes twelve fresh simulator circuits. `argmax()` is used only to display a basis state's unique occupied position; it is not a sampling operation.

```python
from itertools import product
for n in (2, 3):
    observed = []
    for bits in product((0, 1), repeat=n):
        text = ''.join(map(str, bits))
        independent_index = int(text, 2)
        state, probability = prepare_basis(bits)
        expected = torch.zeros(2**n, dtype=torch.complex128)
        expected[independent_index] = 1
        torch.testing.assert_close(state, expected, rtol=0, atol=1e-12)
        torch.testing.assert_close(probability, expected.abs().square(),
                                   rtol=0, atol=1e-12)
        assert basis_bits(independent_index, n) == bits
        observed.append(f'{text}->{int(probability.argmax())}')
    print(f'{n} qubits: ' + ', '.join(observed))
```

```text
2 qubits: 00->0, 01->1, 10->2, 11->3
3 qubits: 000->0, 001->1, 010->2, 011->3, 100->4, 101->5, 110->6, 111->7
```

<span id="formula-code-4-2-reversal-witness"></span>

As a separate failure witness, a least-significant-position-0 calculation would assign `(1,0,0)` the index 1. Under our declared convention, the actual prepared state occupies index 4. The wrong rule addresses a different amplitude. It is not repaired by changing a printed qubit name.

```python
state, probability = prepare_basis((1, 0, 0))
wrong_index = sum(b*2**q for q, b in enumerate((1, 0, 0)))
print('declared 100 index:', int(probability.argmax()))
print('reversed-significance index:', wrong_index)
print('amplitude at wrong index:', abs(state[wrong_index].item()))
```

```text
declared 100 index: 4
reversed-significance index: 1
amplitude at wrong index: 0.0
```

If a different external convention is declared, conversion must be explicit. Deriving permutation matrices and implementing SWAP belong to 4.5, and cross-framework conversion to 4.8. Here we establish the coordinate contract those sections will use.

### A basis index addresses an amplitude, not a whole state

For a general normalized register vector, write

$$
|\psi\rangle=\sum_{j=0}^{2^n-1}\psi_j|B_n(j)\rangle_L,\qquad
\sum_j|\psi_j|^2=1.
$$

The symbol $\psi_j$ is a complex amplitude. It is not the integer j and not the probability of j. Applying the finite-basis Born rule from 4.1 gives

$$
\Pr(\text{computational outcome }b)=|\psi_{J_n(b)}|^2.
$$

No measurement has occurred merely because a simulator exposes `statevector()`. Our example requests exact-model probabilities; no finite-shot record, measurement update or hardware count is generated.

To make this distinction concrete, independently prepare the three factors

$$
a=\begin{pmatrix}3/5\\4i/5\end{pmatrix},\quad
b=\frac1{\sqrt2}\begin{pmatrix}1\\i\end{pmatrix},\quad
c=\begin{pmatrix}\sqrt3/2\\1/2\end{pmatrix}.
$$

Repeated use of 4.1 gives $\psi_{J_3(u,v,w)}=a_u b_v c_w$. Listing the products in the now-proved order yields

$$
\psi=\frac1{10\sqrt2}
\begin{pmatrix}3\sqrt3\\3\\3i\sqrt3\\3i\\4i\sqrt3\\4i\\-4\sqrt3\\-4\end{pmatrix}.
$$

For instance, `110` has index 6 and amplitude $a_1b_1c_0=-\sqrt6/5$; the minus sign comes from $i^2=-1$. Its probability is $6/25=0.24$. A norm-only or probability-only check would not detect every phase error, so we also compare the complete vector with this hand expansion.

<span id="formula-code-4-2-complex-product"></span>

**Formula → scalar products → actual released FlagQuantum calls.** The first-column preparation matrix `prepare_matrix()` was derived in 4.1. Each loop iteration assigns one factor to its declared integer qubit. This is independent preparation, not an entangling circuit.

```python
from math import sqrt
import flagquantum as fq
from examples.foundations.tensor_spaces import prepare_matrix, OPTIONS

factors = ([.6, .8j], [1/sqrt(2), 1j/sqrt(2)], [sqrt(3)/2, .5])
circuit = fq.Circuit(3, dtype=torch.complex128)
for q, factor in enumerate(factors):
    circuit.unitary(q, unitary=prepare_matrix(
        torch.tensor(factor, dtype=torch.complex128)))
result = fq.run(circuit, outputs=[fq.probabilities()], options=OPTIONS)
assert result.statevector().shape == result.probabilities.shape == (1, 8)
state, probability = result.statevector()[0], result.probabilities[0]
hand = [z/(10*sqrt(2)) for z in
        [3*sqrt(3), 3, 3j*sqrt(3), 3j, 4j*sqrt(3), 4j, -4*sqrt(3), -4]]
torch.testing.assert_close(state, torch.tensor(hand, dtype=torch.complex128),
                           rtol=0, atol=1e-12)
print([round(p, 3) for p in probability.tolist()])
```

```text
[0.135, 0.045, 0.135, 0.045, 0.24, 0.08, 0.24, 0.08]
```

The leading axis of shape `(1,8)` is one simulated sample, not an additional qubit. Extracting its only row leaves the eight-coordinate register vector. The code checks that shape before extraction; blindly flattening arbitrary batches could combine different states.

<span id="formula-code-4-2-indexed-born"></span>

**Formula → indexed Born rule → checked result.** Use the bit tuple to obtain the array index, then square the modulus at that position. The displayed amplitude is negative, while its probability is nonnegative.

```python
j = basis_index((1, 1, 0))
assert abs(state[j].item() + sqrt(6)/5) < 1e-12
assert abs(abs(state[j].item())**2 - probability[j].item()) < 1e-12
print('bits:', basis_bits(j, 3), '; index:', j)
print(f'amplitude real={state[j].real.item():.9f}; probability={probability[j].item():.9f}')
```

```text
bits: (1, 1, 0) ; index: 6
amplitude real=-0.489897949; probability=0.240000000
```

The probability 0.24 does not say that a particular next shot must return `110`. Choosing `argmax()` for this superposition would choose one most probable outcome, with a possible tie; it would not simulate a draw from the distribution or reconstruct the state. Sampling and statistical uncertainty are developed in Chapter 6.

### Executable contract, boundaries and complete output

The helpers in [register_indices.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/register_indices.py) accept literal integer bits, a positive integer width and an in-range integer index. Boolean and floating-point inputs are rejected instead of being silently converted, as are duplicate labels. Zero qubits are outside this section's execution profile; this does not deny the mathematical usefulness of an empty tensor product elsewhere. Large-register storage limits are also separate: a length-$2^n$ dense array grows exponentially, even though this index formula uses only n bits.

<span id="formula-code-4-2-input-boundaries"></span>

**Contract → rejected input → checked result.** An invalid request is not evidence for a different physical state. We neither clip an out-of-range index nor reduce it modulo the vector length.

```python
checks = [lambda: basis_bits(8, 3), lambda: basis_index((True, 0)),
          lambda: register_labels(('signal', 'signal'))]
rejected = 0
for check in checks:
    try:
        check()
    except ValueError:
        rejected += 1
assert rejected == 3
print('invalid index, Boolean bit, duplicate label:', rejected, 'rejected')
```

```text
invalid index, Boolean bit, duplicate label: 3 rejected
```

Use the existing [pinned example environment](https://github.com/FlagQuantum/modern-quantum-computing#run-the-examples), CPython 3.12, FlagQuantum 0.3.1 and PyTorch 2.13.0. No framework installation or extra API is introduced by this section.

```bash
python examples/foundations/register_indices.py
python scripts/check_register_indices_prose.py
```

The complete program uses CPU complex128 states, float64 probabilities, absolute tolerance $10^{-12}$ and zero relative tolerance, with approximation and backend fallback disabled. Integer index identities are checked exactly. It executes fourteen circuits: twelve exhaustive basis preparations, one complex product and one additional reversed-significance witness. The cumulative body fragments execute fifteen circuits, because their first `110` example is separate from the exhaustive table. Neither count includes any hardware run.

Expected output of the complete program:

```text
Register order (most to least significant): signal, reference, flag.
110 -> 6 ; 6 -> (1, 1, 0)
510 mathematical basis labels (n=1..8): index, inverse and independent strings agree.
FlagQuantum 2 qubits: 00->0, 01->1, 10->2, 11->3.
FlagQuantum 3 qubits: 000->0, 001->1, 010->2, 011->3, 100->4, 101->5, 110->6, 111->7.
12 actual basis-preparation circuits: full complex states and probabilities checked.
Complex product probabilities: 0.135000000, 0.045000000, 0.135000000, 0.045000000, 0.240000000, 0.080000000, 0.240000000, 0.080000000.
Index 6 is 110: amplitude real=-0.489897949; probability=0.240000000.
Reversed-significance witness, leading zeros and 12 malformed-input cases checked.
14 actual simulator circuits total; CPU complex128, atol=1e-12, rtol=0.
No sampling, hardware layout, SWAP or marginal-order claim.
```

The verification is deliberately bounded. A successful three-qubit check does not certify arbitrary register sizes, reordered subset outputs, compiler remapping, remote-provider count strings or physical-device readout. Each such interface needs its own declared convention and test. We also do not recover a state from a single bit-string outcome.

### Understanding checks and transfer exercises

**4.2-A — Decode before assigning names.** For $L=(\mathrm{control},\mathrm{data0},\mathrm{data1},\mathrm{flag})$, decode index 3 and state which named qubits have bit 1. What changes if only the register width is changed to two? Explain why the index alone is insufficient.

**4.2-B — Transfer the preparation.** In a five-qubit register with order $(\mathrm{flag},\mathrm{a},\mathrm{b},\mathrm{c},\mathrm{d})$, prepare only flag and c in basis state 1. Give the bit string and occupied index. Write the relevant `x(q)` calls, and give a full-vector reference rather than relying on `argmax()` alone.

**4.2-C — Debug a self-consistent mistake.** A programmer weights position k by $2^k$, uses an inverse that returns least-significant bits first, and reports that every round-trip test passed. Explain why this does not verify the declared convention. Supply a three-qubit preparation that distinguishes the two conventions and the two predicted indices.

**4.2-D — A coordinate versus an outcome.** In the worked complex product, what are $\psi_6$ and $p(110)$? If one computational readout returns `110`, does it establish that the input state was $|110\rangle$? Can the eight simulator amplitudes be read from a single hardware shot? Distinguish the mathematical state, the ideal probability array and an observed bit string.

**4.2-E — Complete the bijection argument.** Suppose two n-bit tuples differ first at position k. Show that the weight of this leading difference exceeds the maximum possible cancellation by all less significant positions. Explain how that gives another proof of injectivity, and why the range and cardinality then imply surjectivity.

<details markdown="1">
<summary>Answers and reasoning</summary>

**A.** Fixed width four gives `0011`: control=0, data0=0, data1=1, flag=1. Width two gives `11`; it belongs to a different two-factor register and has no automatic assignment to the four original names. The integer is the same, but the domain and tensor-factor labels differ.

**B.** Flag is position 0 and c is position 3, so the tuple is `10010` and $j=16+2=18$. The calls are `circuit = fq.Circuit(5, dtype=torch.complex128)`, then `circuit.x(0)` and `circuit.x(3)`. A reference is a complex128 vector of length 32 with entry 18 equal to 1 and every other entry zero. Under the declared ideal simulator options, compare all coordinates with absolute tolerance $10^{-12}$ and relative tolerance zero, as in the two/three-qubit tests. The author separately executed this five-qubit transfer check and compared all 32 amplitudes and probabilities. Its one additional circuit is recorded separately from the fourteen-circuit complete example and fifteen-circuit body fragments.

**C.** Matching forward and inverse bugs can cancel. Their round trip tests internal consistency, not the external tensor-factor contract. Prepare qubit 0 alone in state 1 in a three-qubit register. The declared tuple `100` occupies index 4; the reversed-significance rule predicts 1. The complete program actually executes this witness, in addition to its exhaustive tables.

**D.** $\psi_6=-\sqrt6/5$ and $p(110)=6/25$. The nonzero probability permits that outcome even though the initial vector has eight nonzero components, so the single observation does not identify the prior vector as one basis state. A simulator's statevector is a model-access output; a shot is one drawn outcome. Neither a probability array nor a full complex vector is delivered by one computational-basis shot. State inference requires additional preparations and measurement settings, addressed later.

**E.** The leading difference contributes magnitude $2^{n-1-k}$. The total magnitude of all later possible differences is at most $\sum_{r=0}^{n-2-k}2^r=2^{n-1-k}-1$, with an empty sum equal to zero at the last position. It cannot cancel the leading contribution, so the indices differ. There are $2^n$ tuples and $2^n$ integers in the established range; an injection between these two finite sets uses every index. This supplies a second complete bijection argument, independent of the quotient/remainder construction.

</details>

### Source, depth and review status

Depth **F**: the recurrence, closed form, inverse identities and bijection are proved, with an alternative leading-difference argument in the answers. The retained background locator is Nielsen and Chuang, 10th Anniversary Edition, §2.1.7, for ordered tensor products, as used in 4.1. The explicit index proof and examples here are original. [Preskill, Chapter 2, §2.3.1, Eq. (2.46)](https://www.preskill.caltech.edu/ph229/notes/chap2.pdf#page=14) is supplementary context for labeled product factors; it does not prescribe FlagQuantum's array order. The latter is checked against the released implementation by the exhaustive preparations above.

The [4.2 section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/4.2.json) records source-access limits, actual execution and separate pending mathematical, implementation and reader reviews. This is an author-verified working draft, not an accepted section. Continue, when drafted, with [4.3 Local operators on a composite register](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-3).
