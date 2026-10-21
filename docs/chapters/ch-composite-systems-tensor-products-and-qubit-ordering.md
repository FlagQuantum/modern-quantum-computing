# 4. Composite Systems, Tensor Products, and Qubit Ordering

**Working drafts: sections 4.1–4.8 · Writing Baseline 1.0 · October 21, 2026.** Author execution is recorded separately from independent mathematical, implementation and reader review, which remain pending. This is not an accepted chapter. Examples use released FlagQuantum 0.3.1 and PyTorch 2.13.0 on CPU with complex128 statevectors.

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

The [4.2 section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/4.2.json) records source-access limits, actual execution and separate pending mathematical, implementation and reader reviews. This is an author-verified working draft, not an accepted section. Continue with [4.3 Local operators on a composite register](#sec-composite-systems-tensor-products-and-qubit-ordering-3).

<span id="sec-composite-systems-tensor-products-and-qubit-ordering-3"></span>

## 4.3 Local operators on a composite register

A command such as `circuit.unitary(0, unitary=U)` supplies a two-by-two matrix even when the statevector has eight coordinates. What linear map does that command mean on the whole register? The answer must identify the factor being changed, preserve the other factors and specify the coordinate order. A two-by-two matrix alone does not contain that information.

The prerequisites are [4.1](#sec-composite-systems-tensor-products-and-qubit-ordering-1), for ordered product bases and independent preparations, and [3.4](ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-4), for unitary dynamics and Hermitian generators. We state the coordinate convention locally below, so the proof does not require a theorem about permutations, multiple-qubit supports or matrix reshaping. [4.2](#sec-composite-systems-tensor-products-and-qubit-ordering-2) supplies the optional integer-index interpretation of these same labels.

### Define the map by its action on a product basis

Let V and W have ordered orthonormal bases $\{f_i\}_{i=0}^{m-1}$ and $\{g_j\}_{j=0}^{d-1}$. A linear operator $A:V\to V$ has entries defined by $Af_k=\sum_i A_{ik}f_i$. On each joint basis vector, define

$$
\mathcal E_V(A)(f_k\otimes g_\ell)=(Af_k)\otimes g_\ell
=\sum_i A_{ik}f_i\otimes g_\ell.
$$

The joint product vectors form a basis by 4.1, so prescribing their images determines one and only one linear operator on the composite space. Existence follows by extending the rule to every finite linear combination; uniqueness follows because two linear operators that agree on every basis vector agree on their span.

For arbitrary $v=\sum_k v_k f_k$ and $w=\sum_\ell w_\ell g_\ell$, bilinearity and linearity give

$$
\mathcal E_V(A)(v\otimes w)
=\sum_{i,k,\ell}A_{ik}v_k w_\ell f_i\otimes g_\ell
=(Av)\otimes w.
$$

This is the meaning of a **local operator on V**: it acts on the specified tensor factor and as the identity on the other factor. A general joint vector need not factor as $v\otimes w$. Nevertheless the basis definition acts on it, by the same linear extension. Locality describes the operator, not a restriction that its input must be a product state.

### Derive the Kronecker matrices and the coefficient update

List joint coordinates as $(0,0),(0,1),\ldots,(m-1,d-1)$, with the W label changing fastest. Reading coefficients in the definition gives

$$
[\mathcal E_V(A)]_{(i,j),(k,\ell)}=A_{ik}\delta_{j\ell}.
$$

Here $\delta_{j\ell}$ is one when the spectator labels agree and zero otherwise. The matrix is conventionally written $A\otimes I_d$: its block in row i, column k is $A_{ik}I_d$. Similarly an operator $B:W\to W$ acting only on W has

$$
[\mathcal E_W(B)]_{(i,j),(k,\ell)}=\delta_{ik}B_{j\ell},\qquad
\mathcal E_W(B)=I_m\otimes B.
$$

These formulas derive the matrix placements; they are not interchangeable notations for the same operation. For two qubits and $A=\left(\begin{smallmatrix}a&b\\c&d\end{smallmatrix}\right)$, they become

$$
A\otimes I_2=\begin{pmatrix}a&0&b&0\\0&a&0&b\\c&0&d&0\\0&c&0&d\end{pmatrix},\qquad
I_2\otimes A=\begin{pmatrix}a&b&0&0\\c&d&0&0\\0&0&a&b\\0&0&c&d\end{pmatrix}.
$$

Use the computational order `00,01,10,11`; qubit 0 is the first factor. An n-qubit version follows by the same basis prescription:

$$
\mathcal E_q(A)=I_2^{\otimes q}\otimes A\otimes I_2^{\otimes(n-1-q)},\qquad
[\mathcal E_q(A)]_{b,c}=A_{b_qc_q}\prod_{r\ne q}\delta_{b_rc_r}.
$$

At the ends there are no identity factors on one side; their omission leaves A in the first or last position. More generally, choose $A|c_q\rangle$ on the selected position of each product-basis vector and leave all other entries in place. Expanding that one factor gives the displayed matrix entries and proves the formula for every finite n. The identity factors each have dimension two, so the resulting matrix is $2^n$ by $2^n$.

<span id="formula-code-4-3-kronecker"></span>

**Formula → block construction → checked reference.** The cumulative code blocks below run from the repository root. `embedding()` implements the ordered identity-factor construction with `torch.kron`; its strict qubit/shape/dtype checks are in the linked complete program. This is a dense mathematical reference, not an instruction to allocate a full dense operator for a large simulator.

```python
from examples.foundations.local_operators import (
    rotation, embedding, scalar_action, execute, initial_product,
)
import torch
U = rotation()
left, right = embedding(U, 2, 0), embedding(U, 2, 1)
assert left.shape == right.shape == (4, 4)
print(tuple(left.shape), torch.allclose(left, right, rtol=0, atol=1e-12))
```

```text
(4, 4) False
```

For arbitrary joint coefficients $z_{k\ell}$, multiplying the first-factor matrix gives

$$
y_{ij}=\sum_{k,\ell}A_{ik}\delta_{j\ell}z_{k\ell}=\sum_k A_{ik}z_{kj}.
$$

Thus an operation on the first factor mixes amplitudes with the same spectator label j. Acting on the second gives $y_{ij}=\sum_\ell B_{j\ell}z_{i\ell}$ instead. There is no conjugation of z in either formula: this is a linear action, not an inner product.

<span id="formula-code-4-3-scalar-action"></span>

**Formula → scalar sums → independent validation.** The reference `scalar_action()` enumerates input and output bit tuples, uses the delta conditions and sums complex scalars. It calls neither `torch.kron` nor a reshaping routine. Test a joint vector that is not assumed to be a product:

```python
from math import sqrt
z = torch.tensor([1, 2j, -3, 4j], dtype=torch.complex128)/sqrt(30)
reference = torch.tensor(scalar_action(U.tolist(), z.tolist(), 2, 0),
                         dtype=torch.complex128)
torch.testing.assert_close(left @ z, reference, rtol=0, atol=1e-12)
print('scalar coefficient rule matches dense action:', True)
```

```text
scalar coefficient rule matches dense action: True
```

This block checks the mathematics on an arbitrary joint vector. It does not claim that a simulator prepared that vector. The actual execution tests below separately use basis inputs and independent product preparations.

### Translate a unitary local operator into FlagQuantum

The embedding construction accepts any linear A, but a deterministic gate in our ideal circuit model must be unitary. For the worked example, choose

$$
U=\begin{pmatrix}\sqrt3/2&-i/2\\-i/2&\sqrt3/2\end{pmatrix}
=\cos(\pi/6)I-i\sin(\pi/6)X,\qquad
X=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
$$

Since $X^\dagger=X$ and $X^2=I$, the even and odd powers of its exponential, as in 3.4, give $U=\exp(-i\pi X/6)$. Multiplying $(\cos t I+i\sin t X)(\cos t I-i\sin t X)$ gives I, proving unitarity. No physical pulse duration or energy unit is inferred from this dimensionless example.

Independently prepare $a=(3/5,4i/5)^T$ and $b=(\sqrt3/2,i/2)^T$. The initial joint vector is $a\otimes b$. The predicted outputs are $(Ua)\otimes b$ when targeting qubit 0 and $a\otimes(Ub)$ when targeting qubit 1. The coefficient formula also computes either result without presuming product structure.

<span id="formula-code-4-3-execution"></span>

**Formula → released API → actual full-state checks.** The first-column preparation matrix from 4.1 prepares each factor. The local operation uses the same two-by-two U regardless of total register size; FlagQuantum receives the selected integer qubit separately.

```python
from examples.foundations.tensor_spaces import prepare_matrix, OPTIONS
import flagquantum as fq
factors = [(.6, .8j), (sqrt(3)/2, .5j)]
initial = torch.tensor(initial_product(factors), dtype=torch.complex128)
outputs = {}
for q in (0, 1):
    circuit = fq.Circuit(2, dtype=torch.complex128)
    for position, factor in enumerate(factors):
        circuit.unitary(position, unitary=prepare_matrix(
            torch.tensor(factor, dtype=torch.complex128)))
    circuit.unitary(q, unitary=U)
    result = fq.run(circuit, outputs=[fq.probabilities()], options=OPTIONS)
    assert result.statevector().shape == result.probabilities.shape == (1, 4)
    state, probability = result.statevector()[0], result.probabilities[0]
    expected = torch.tensor(scalar_action(U.tolist(), initial.tolist(), 2, q),
                            dtype=torch.complex128)
    torch.testing.assert_close(state, expected, rtol=0, atol=1e-12)
    torch.testing.assert_close(probability, expected.abs().square(),
                               rtol=0, atol=1e-12)
    outputs[q] = (state, probability)
    print(q, [round(p, 9) for p in probability.tolist()])
```

```text
0 [0.634269145, 0.211423048, 0.115730855, 0.038576952]
1 [0.36, 0.0, 0.64, 0.0]
```

The target matters: these two output distributions differ, and full complex-state checks also differ. Neither a correctly normalized output nor a correct two-by-two U would rescue a mistaken target position. The shape `(1,4)` has a singleton batch axis, which is checked before selecting its only row.

<span id="formula-code-4-3-basis-checks"></span>

**Basis formula → exhaustive preparation → checked results.** Every computational-basis input is checked on both supports of a two-qubit register. The complete program extends this to every support of three qubits: $2\cdot4+3\cdot8=32$ basis circuits. Since the ideal operations are linear, these basis cases test every column of each tested embedded matrix; floating-point agreement still remains evidence at the stated tolerance, not an exact symbolic proof about a software implementation.

```python
from itertools import product
count = 0
for q in (0, 1):
    for bits in product((0, 1), repeat=2):
        preparations = [(1, 0) if b == 0 else (0, 1) for b in bits]
        state, probability = execute(2, q, preparations)
        reference = torch.tensor(scalar_action(U.tolist(),
            initial_product(preparations), 2, q), dtype=torch.complex128)
        torch.testing.assert_close(state, reference, rtol=0, atol=1e-12)
        count += 1
print('actual two-qubit basis circuits:', count)
```

```text
actual two-qubit basis circuits: 8
```

### Distinguish arbitrary local maps from unitary gates

Taking the conjugate transpose of the entry formula gives $\mathcal E_V(A)^\dagger=\mathcal E_V(A^\dagger)$. To verify the product needed for a norm check, sum over intermediate joint labels:

$$
[\mathcal E_V(A)^\dagger\mathcal E_V(A)]_{(k,\ell),(r,s)}
=\sum_{i,j}\overline{A_{ik}}\delta_{j\ell}A_{ir}\delta_{js}
=(A^\dagger A)_{kr}\delta_{\ell s}.
$$

Thus $\mathcal E_V(A)^\dagger\mathcal E_V(A)=I$ if A is unitary. Conversely, equality with I forces $(A^\dagger A)_{kr}=\delta_{kr}$ by setting $\ell=s$; there is at least one spectator basis label. The same proof applies at any selected factor. This establishes exactly which embedded maps preserve all vector norms.

For example, the local projector $P=\operatorname{diag}(1,0)$ is a valid linear map but not a unitary gate. On our product input, $(P\otimes I)(a\otimes b)=(3/5)|0\rangle\otimes b$, with squared norm $9/25$. Silently normalizing that output would change the task. Describing a physical selective measurement requires probabilities and an instrument, developed later; this section only computes the unnormalized linear image.

<span id="formula-code-4-3-nonunitary"></span>

**Formula → dense mathematical action → explicit failure of unitarity.** This block intentionally makes no `circuit.unitary()` call with P. The reference helper accepts linear maps, while the circuit example uses unitary U only.

```python
P = torch.tensor([[1, 0], [0, 0]], dtype=torch.complex128)
M = embedding(P, 2, 0)
image = M @ initial
print(f'linear-image norm squared: {image.abs().square().sum().item():.9f}')
print('unitary:', torch.allclose(M.mH @ M, torch.eye(4, dtype=torch.complex128),
                               rtol=0, atol=1e-12))
```

```text
linear-image norm squared: 0.360000000
unitary: False
```

### What stays unchanged at an untouched factor?

A local unitary changes joint amplitudes but does not change the other factor's computational-basis probability distribution. For a two-factor vector with coefficients $z_{kj}$, hold the spectator label j fixed. Its probability after acting on V is

$$
\sum_i\left|\sum_k A_{ik}z_{kj}\right|^2
=\sum_{k,r}\left(\sum_i A_{ik}\overline{A_{ir}}\right)z_{kj}\overline{z_{rj}}
=\sum_k|z_{kj}|^2.
$$

The final equality uses the orthonormal columns of A. This argument applies to arbitrary joint coefficients; it does not assume independent initial factors. It says that this particular distribution is unchanged, not that all joint amplitudes or correlations are unchanged. General reduced states and channel versions are developed in their own chapters.

<span id="formula-code-4-3-spectator"></span>

**Formula → explicit spectator sum → checked simulator result.** For qubit 1 in the `00,01,10,11` order, its basis-0 probability sums coordinates 0 and 2. Check the qubit-0 operation already executed above:

```python
before = sum(abs(initial[i].item())**2 for i in (0, 2))
after = sum(outputs[0][1][i].item() for i in (0, 2))
assert abs(before-after) < 1e-12
print(f'untouched qubit 1, probability 0: {before:.9f} -> {after:.9f}')
```

```text
untouched qubit 1, probability 0: 0.750000000 -> 0.750000000
```

### Run the complete verification and respect its limits

[local_operators.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/local_operators.py) targets the existing CPython 3.12, FlagQuantum 0.3.1 and PyTorch 2.13.0 CPU environment. Statevectors use complex128 and probabilities float64. The actual execution options disable backend fallback and approximation. Complex-coordinate comparisons use absolute tolerance $10^{-12}$, relative tolerance zero, without normalization or phase alignment.

The dense reference requires finite CPU complex128 two-by-two matrices and a valid integer support. Its implementation makes an entry-preserving contiguous copy before `torch.kron`, since a conjugate-transposed Torch view can have incompatible strides. This changes array storage, not the tensor-factor order or the mathematical map. A malformed support or precision is rejected before construction.

<span id="formula-code-4-3-boundaries"></span>

**Input contract → rejected metadata → checked result.** Boolean qubit indices are not silently treated as integers.

```python
invalid = [lambda: embedding(U, 2, 2), lambda: embedding(U, 2, True),
           lambda: embedding(U.to(torch.complex64), 2, 0)]
rejected = 0
for action in invalid:
    try:
        action()
    except ValueError:
        rejected += 1
print('invalid support, Boolean support, wrong precision:', rejected, 'rejected')
```

```text
invalid support, Boolean support, wrong precision: 3 rejected
```

Run from the repository root:

```bash
python examples/foundations/local_operators.py
python scripts/check_local_operators_prose.py
```

The complete program executes 34 circuits: 32 basis/support cases and two complex-product cases. Its classical nonunitary and adjoint checks execute no quantum circuit. The cumulative body fragments execute ten circuits, independently of the complete program. The dense references are small-system verification tools; explicitly storing a $2^n$-square matrix is not a scalable simulation requirement. Multiple-qubit ordered supports, SWAP/permutations, general measurement updates, noise, shots and hardware execution are outside this section's checked scope.

Expected output of the complete program:

```text
Local matrix: U=[[sqrt(3)/2,-i/2],[-i/2,sqrt(3)/2]].
32 basis circuits: all supports on two/three qubits match scalar and Kronecker references.
Product input, local qubit 0: 0.634269145, 0.211423048, 0.115730855, 0.038576952.
Product input, local qubit 1: 0.360000000, 0.000000000, 0.640000000, 0.000000000.
Target confusion rejected: U tensor I and I tensor U give different full states.
Nonunitary local map: output norm squared=0.360000000; no unitary-gate execution claimed.
Adjoint/unitarity identities and 6 invalid-input cases checked.
34 actual CPU complex128 circuits; atol=1e-12, rtol=0; no shots or hardware.
```

### Understanding checks, transfer and answers

**4.3-A — Read the support.** In a three-qubit register ordered `q0,q1,q2`, write the dense reference for U acting only on q1. Which entries can connect an input label `101` to an output label? Explain using the delta factors, rather than guessing from matrix dimensions.

**4.3-B — Transfer to a different generator.** Replace U by $D=\operatorname{diag}(1,i)$ and act on the second factor of $a\otimes b$. Derive the new amplitudes and probabilities. Should the computational probabilities distinguish this output from the input? Give a full-coordinate test that would.

**4.3-C — Reject the wrong inference.** A local linear map decreases the squared norm to 0.36, and a programmer divides the output by 0.6 before returning it as a deterministic gate result. What task was changed? Which additional physical description would be needed for a measurement interpretation?

**4.3-D — Finish the argument.** Why is checking an operator only on independent product inputs insufficient unless those inputs include a spanning set? Explain why the computational basis is enough for the linear operator identity, yet finite floating-point software tests do not replace the symbolic proof.

<details markdown="1">
<summary>Answers and reasoning</summary>

**A.** The matrix is $I_2\otimes U\otimes I_2$. Both spectator bits must remain equal to their input values, so only `101` and `111` can have nonzero coefficients from input `101`. Their coefficients are $U_{0,0}$ and $U_{1,0}$, respectively. No input normalization or relabeling is involved.

**B.** The second factor becomes $(\sqrt3/2,-1/2)^T$, because $i(i/2)=-1/2$. The joint vector is $(3\sqrt3/10,-3/10,2i\sqrt3/5,-2i/5)^T$. Squared moduli remain $(0.27,0.09,0.48,0.16)$, the input distribution. Full complex comparison with that vector detects a phase mistake even when all probabilities agree. The separately recorded author transfer check executes the released local gate and compares both coordinates and probabilities; it is not included in the 34-circuit main-program count.

**C.** The normalization replaces a specified linear map by a state-dependent normalized output rule; it is not the declared deterministic unitary gate. A measurement interpretation needs the full measurement/instrument specification, the probability and conditioning event, and the associated state update, not just division by a norm. Those are not inferred by this linear-algebra calculation.

**D.** Agreement on a few product vectors can miss an operator's action on other directions. The full product basis spans the joint space by 4.1; linearity then fixes every vector's image. In the proof, exact basis identities establish exact operators. A simulator run instead checks particular finite arrays with a numerical tolerance, a declared environment and an execution scope. It is evidence about those computations, not an all-environment correctness theorem.

</details>

### Sources, depth and review status

Depth **F**: construction and uniqueness on a product basis, matrix entries, coefficient action, general single-factor embedding and the adjoint/unitarity criterion are derived explicitly. The assigned background remains Nielsen and Chuang, 10th Anniversary Edition, §2.1.7, following the source chain in 4.1. No new inspection of the user-local textbook PDF is claimed here: access was unavailable in the preceding source check. The proofs, examples and translations above are original and self-contained relative to the stated drafts.

The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/4.3.json) separates author execution, its initial reference-layout failure and repair, and pending independent mathematical, implementation and reader review. This is a working draft, not an accepted section. Continue with [4.4 Multiple-qubit operators and ordered supports](#sec-composite-systems-tensor-products-and-qubit-ordering-4).

<span id="sec-composite-systems-tensor-products-and-qubit-ordering-4"></span>

## 4.4 Multiple-qubit operators and ordered supports

A four-by-four matrix describes an operation on two qubits, but it does not specify which two qubits of a larger register are involved, or which one supplies the more significant local bit. The ordered support supplies that missing information. Silently sorting its labels can change an implemented operation while leaving matrix dimensions, normalization and even some test outputs unchanged.

We use the bit-tuple/index bijection from [4.2](#sec-composite-systems-tensor-products-and-qubit-ordering-2) and the basis-defined local embedding from [4.3](#sec-composite-systems-tensor-products-and-qubit-ordering-3). This section generalizes the latter to several selected, possibly nonadjacent qubits. It does not yet implement a permutation, SWAP, routing algorithm or tensor-axis optimization; those belong to later sections.

### Specify an ordered local basis

Fix an n-qubit register with global order `q0,...,q(n-1)`, qubit 0 most significant. Let

$$
S=(s_0,\ldots,s_{k-1}),\qquad 1\leq k\leq n,
$$

be a tuple of **distinct**, in-range integer qubit labels. Its underlying set tells us which qubits participate. Its order tells us how to interpret the matrix's rows and columns. For a global bit tuple b, define

$$
b_S=(b_{s_0},\ldots,b_{s_{k-1}}),\qquad
r_S(b)=J_k(b_S)=\sum_{j=0}^{k-1}b_{s_j}2^{k-1-j}.
$$

The global index is still $J_n(b)$. The first element of S supplies the most significant **local** bit, even when it is the least significant global qubit. Local and global positions answer different indexing questions.

A matrix U on this support has shape $(2^k,2^k)$ and local basis order `00,...,11` for two qubits. Entry $U_{\alpha\beta}$ maps local input basis index $\beta$ to output index $\alpha$. If S contains repeated labels, these k local bits would not describe k distinct factors. We reject that input instead of inventing an interpretation.

<span id="formula-code-4-4-local-indices"></span>

**Formula → local index extraction → checked result.** Run the cumulative blocks below in order, from the repository root. The helpers belong to the complete example; they are not new FlagQuantum APIs.

```python
from examples.foundations.register_indices import basis_index
from examples.foundations.ordered_supports import (
    support_tuple, controlled_flip, complex_gate, dense_embedding,
    scalar_scatter, input_product, execute, checked_matrix,
)
bits = (1, 0, 0)
for support in ((2, 0), (0, 2)):
    local_bits = tuple(bits[q] for q in support)
    print(support, 'local bits', local_bits, 'local index', basis_index(local_bits))
```

```text
(2, 0) local bits (0, 1) local index 1
(0, 2) local bits (1, 0) local index 2
```

The global tuple and index have not changed: `100` is global index 4 in both rows. What changed is the column selected from the local matrix.

### An order-sensitive operator before a general formula

Consider the explicit matrix

$$
C=\begin{pmatrix}1&0&0&0\\0&1&0&0\\0&0&0&1\\0&0&1&0\end{pmatrix}.
$$

Its columns give $00\mapsto00$, $01\mapsto01$, $10\mapsto11$, $11\mapsto10$. Equivalently, it flips the second local bit when the first local bit is 1. This is a controlled flip, defined here by its basis action. Each column is a different unit basis vector, so $C^\dagger C=I$; no assumption about gate synthesis is needed.

On global input `100`, support `(2,0)` selects local input `01`, which C leaves unchanged. Support `(0,2)` selects local input `10`, which C changes to `11`; the global output is then `101`. The unused qubit 1 remains 0 in either case.

<span id="formula-code-4-4-order-witness"></span>

**Formula → actual FlagQuantum call → full-coordinate verification.** The installed FlagQuantum 0.3.1 method accepts positional qubit arguments: `circuit.unitary(*support, unitary=C)`. The star expands the tuple without sorting it. The program prepares `100` and compares the entire returned vector with the corresponding unit basis vector.

```python
import torch
import flagquantum as fq
from examples.foundations.tensor_spaces import OPTIONS
C = controlled_flip()
for support, expected_index in [((2, 0), 4), ((0, 2), 5)]:
    circuit = fq.Circuit(3, dtype=torch.complex128)
    circuit.x(0)
    circuit.unitary(*support, unitary=C)
    result = fq.run(circuit, outputs=[fq.probabilities()], options=OPTIONS)
    assert result.statevector().shape == result.probabilities.shape == (1, 8)
    expected = torch.zeros(8, dtype=torch.complex128)
    expected[expected_index] = 1
    torch.testing.assert_close(result.statevector()[0], expected,
                               rtol=0, atol=1e-12)
    print(support, 'occupied global index', int(result.probabilities[0].argmax()))
```

```text
(2, 0) occupied global index 4
(0, 2) occupied global index 5
```

The two supports have the same underlying set. Changing their order while keeping C fixed changes the operator. No physical SWAP was submitted by these calls. Converting the matrix to another local basis can describe the same operation, but that conversion must be explicit; 4.5 develops the required permutation language. A symmetric matrix or a symmetric input could hide this mistake, which is why this witness uses an asymmetric controlled action and input.

### Derive the general ordered-support action

Write $c[S\leftarrow a]$ for the global tuple obtained by replacing the bits at positions $s_0,\ldots,s_{k-1}$ by the respective bits of the local tuple a, retaining every spectator bit. Distinct support labels make this replacement unambiguous. Let $U_{a,d}$ abbreviate $U_{J_k(a),J_k(d)}$. Define the global linear map by

$$
\mathcal E_S(U)|c\rangle
=\sum_{a\in\{0,1\}^k}U_{a,c_S}|c[S\leftarrow a]\rangle.
$$

The global computational vectors form a basis, so this prescription has a unique linear extension, just as in 4.3. Reading the coefficient of an output tuple b gives

$$
[\mathcal E_S(U)]_{b,c}
=U_{b_S,c_S}\prod_{q\notin S}\delta_{b_qc_q}.
$$

The product is over spectator positions; when there are none, its value is one. A nonzero matrix element requires all spectator bits to agree. The selected bits, however, can change jointly and need not factor into independent one-qubit actions.

For a joint vector $|\psi\rangle=\sum_c\psi_c|c\rangle$, where $\psi_c$ abbreviates $\psi_{J_n(c)}$, linearity gives a sum over all input tuples. The spectator deltas force those tuples to agree with b outside S. Every remaining input is uniquely $b[S\leftarrow d]$ for one local d. Therefore

$$
\boxed{\psi'_b=\sum_{d\in\{0,1\}^k}U_{b_S,d}\,\psi_{b[S\leftarrow d]}.}
$$

This is the requested amplitude update. It uses $2^k$ possible local inputs for each global output, rather than assuming the input vector factors across S and its complement. For $k=1$ it reduces to the single-factor coefficient formula in 4.3. For $k=n$ it acts on the whole register with the explicitly declared local order; ascending order is not silently restored.

<span id="formula-code-4-4-amplitude-sum"></span>

**Formula → two independent constructions → checked result.** `dense_embedding()` implements the matrix-entry equation by output/input enumeration and weighted local indices. `scalar_scatter()` instead visits each input amplitude, enumerates its local outputs, replaces bits and accumulates into global indices using a binary-string parser. It uses no dense embedding, Kronecker routine or reshape. Their agreement is checked on a general complex vector, not just one basis input.

```python
from math import sqrt
z = torch.tensor([1, 1j, 2, -1j, -2, 3j, 1, -1j],
                  dtype=torch.complex128)/sqrt(22)
M = dense_embedding(C, 3, (2, 0))
reference = torch.tensor(scalar_scatter(C, z.tolist(), 3, (2, 0)),
                         dtype=torch.complex128)
torch.testing.assert_close(M @ z, reference, rtol=0, atol=1e-12)
print(tuple(M.shape), 'dense and scalar amplitudes agree')
```

```text
(8, 8) dense and scalar amplitudes agree
```

This is a mathematical reference-vector check. It does not claim that the simulator prepared z. Actual execution on every tested basis input and separate complex product preparations follows below.

### Use a complex matrix that mixes local amplitudes

A permutation-only test does not exercise addition of different local input amplitudes. Build a richer local matrix from

$$
R=\begin{pmatrix}\sqrt3/2&-i/2\\-i/2&\sqrt3/2\end{pmatrix},\qquad
H=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix},\qquad U=C(R\otimes H).
$$

The order within $R\otimes H$ refers to the first and second **local** support positions. Its entries are $(R\otimes H)_{ab,cd}=R_{ac}H_{bd}$, by expanding both factor actions on product-basis vectors. Both R and H are unitary; summing products of these entries makes their two column-inner-product factors each a delta, so $R\otimes H$ is unitary. C permutes orthonormal output rows, hence U is unitary as well. Explicit multiplication gives

$$
U=\frac1{2\sqrt2}\begin{pmatrix}
\sqrt3&\sqrt3&-i&-i\\
\sqrt3&-\sqrt3&-i&i\\
-i&i&\sqrt3&-\sqrt3\\
-i&-i&\sqrt3&\sqrt3
\end{pmatrix}.
$$

<span id="formula-code-4-4-complex-matrix"></span>

**Formula → local matrix → checked unitarity.** This construction is classical matrix arithmetic. The final four-by-four matrix will be passed to FlagQuantum on an ordered pair of qubits, without assuming they are adjacent.

```python
U = complex_gate()
hand = torch.tensor([[sqrt(3), sqrt(3), -1j, -1j],
                     [sqrt(3), -sqrt(3), -1j, 1j],
                     [-1j, 1j, sqrt(3), -sqrt(3)],
                     [-1j, -1j, sqrt(3), sqrt(3)]],
                    dtype=torch.complex128)/(2*sqrt(2))
torch.testing.assert_close(U, hand, rtol=0, atol=1e-12)
torch.testing.assert_close(U.mH @ U, torch.eye(4, dtype=torch.complex128),
                           rtol=0, atol=1e-12)
print('local matrix dimension:', U.shape[0], '; unitary:', True)
```

```text
local matrix dimension: 4 ; unitary: True
```

<span id="formula-code-4-4-nonadjacent"></span>

**Formula → actual nonadjacent execution → checked results.** Independently prepare three specified factors, then use U on `(2,0)` and `(0,2)`. Both scalar and dense references compare the complete complex state, with no phase alignment. Correct probabilities alone would not verify all matrix phases.

```python
factors = [(.6, .8j), (sqrt(3)/2, .5j), (1/sqrt(2), 1j/sqrt(2))]
initial = input_product(factors)
outputs = {}
for support in ((2, 0), (0, 2)):
    state, probability = execute(U, 3, support, factors)
    reference = torch.tensor(scalar_scatter(U, initial.tolist(), 3, support),
                             dtype=torch.complex128)
    torch.testing.assert_close(state, reference, rtol=0, atol=1e-12)
    torch.testing.assert_close(state, dense_embedding(U, 3, support) @ initial,
                               rtol=0, atol=1e-12)
    outputs[support] = (state, probability)
    print(support, [round(p, 9) for p in probability.tolist()])
```

```text
(2, 0) [0.349879763, 0.025120237, 0.116626588, 0.008373412, 0.349879763, 0.025120237, 0.116626588, 0.008373412]
(0, 2) [0.317134573, 0.317134573, 0.105711524, 0.105711524, 0.057865427, 0.057865427, 0.019288476, 0.019288476]
```

The complete program also checks all basis inputs for both two-qubit support orders, all six ordered pairs in a three-qubit register, and the nonadjacent orders `(3,1)` and `(1,3)` in a four-qubit register. This gives $2\cdot4+6\cdot8+2\cdot16=88$ basis/support circuits for U. A support tuple and its sorted version are separate cases.

### Include the full-support boundary and spectator probabilities

For a fixed spectator bit tuple, the supported amplitudes form a length-$2^k$ vector. The global map applies the same U to each such vector without mixing spectator tuples. These groups partition all global basis labels. Summing squared norms over the groups proves that unitary U gives a unitary global map; the adjoint is $\mathcal E_S(U^\dagger)$. Conversely, a nonunitary U is detected on at least one local input vector while fixing any spectator basis word, so its embedding cannot be a deterministic unitary gate. The linear embedding formula still makes mathematical sense for such a matrix.

When $k=n$, there is one group and no spectator label. To test this boundary, use the explicitly defined eight-dimensional Fourier matrix

$$
F_{r,c}=\frac1{\sqrt8}\exp(2\pi i r c/8),\qquad r,c=0,\ldots,7.
$$

The inner product of two columns is a finite geometric sum: it is one for equal columns, while for different columns its ratio is a nontrivial eighth root of unity, giving $(1-1)/(1-\mathrm{ratio})=0$. Thus F is unitary. This finite check supplies the needed fact here; quantum Fourier algorithms are developed later.

For support `(2,0,1)` and global input `001`, the local input is `100`, column 4. That column has entries $(-1)^r/\sqrt8$. Since the least significant local bit is global qubit 1, the global sign is $(-1)^{b_1}$. Uniform probabilities would miss an incorrect sign pattern.

<span id="formula-code-4-4-full-support"></span>

**Formula → full-support execution → phase-sensitive verification.** The block executes one boundary case; the complete program checks all eight basis inputs for this support.

```python
import cmath
from math import pi
F = torch.tensor([[cmath.exp(2j*pi*r*c/8)/sqrt(8) for c in range(8)]
                  for r in range(8)], dtype=torch.complex128)
state, probability = execute(F, 3, (2, 0, 1), [(1, 0), (1, 0), (0, 1)])
expected = torch.tensor([1, 1, -1, -1, 1, 1, -1, -1],
                         dtype=torch.complex128)/sqrt(8)
torch.testing.assert_close(state, expected, rtol=0, atol=1e-12)
print('full-support probabilities:', [round(p, 3) for p in probability.tolist()])
```

```text
full-support probabilities: [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]
```

For any fixed spectator word t, the norm preservation argument also proves

$$
\sum_a|\psi'_{S=a,T=t}|^2=\sum_d|\psi_{S=d,T=t}|^2,
$$

where T is the complement of S in ascending global order and the subscripts denote the unique global tuple with those assignments. This preserves the spectator's computational probability, even for a general joint vector. It does not say that the joint state is unchanged, or introduce a general measurement-update theorem.

<span id="formula-code-4-4-spectator"></span>

**Formula → explicit spectator sum → checked result.** In the three-qubit example, qubit 1 is the spectator, so its outcome-0 positions are `000,001,100,101`.

```python
rows = (0, 1, 4, 5)
before = sum(abs(initial[i].item())**2 for i in rows)
for support in ((2, 0), (0, 2)):
    after = sum(outputs[support][1][i].item() for i in rows)
    assert abs(before-after) < 1e-12
    print(support, f'spectator probability0: {before:.9f} -> {after:.9f}')
```

```text
(2, 0) spectator probability0: 0.750000000 -> 0.750000000
(0, 2) spectator probability0: 0.750000000 -> 0.750000000
```

### Validate contracts and run the complete program

The [complete example](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/ordered_supports.py) uses CPython 3.12, released FlagQuantum 0.3.1 and PyTorch 2.13.0 on CPU. It checks finite complex128 states, float64 probabilities and the exact singleton-batch shapes before extracting rows. Approximation and backend fallback are disabled. Floating comparisons use absolute tolerance $10^{-12}$ and zero relative tolerance, without normalizing or aligning phases.

The dense mathematical reference accepts arbitrary finite local linear maps. The circuit helper separately requires a unitary local matrix. Both reject dimension, support and precision errors before dependent execution. Neither sorts a support, clips an index, silently removes duplicates or changes matrix entries to fit a requested gate.

<span id="formula-code-4-4-invalid-contracts"></span>

**Contract → rejected input → checked result.** A repeated support label is not a smaller gate, and a wrong matrix dimension is not repaired by resizing it.

```python
invalid = [lambda: support_tuple(3, (0, 0)),
           lambda: support_tuple(3, (0, 3)),
           lambda: checked_matrix(U, 1),
           lambda: checked_matrix(2*U, 2, unitary=True)]
rejected = 0
for action in invalid:
    try:
        action()
    except ValueError:
        rejected += 1
assert rejected == 4
print('duplicate support, range, dimension, nonunitarity:', rejected, 'rejected')
```

```text
duplicate support, range, dimension, nonunitarity: 4 rejected
```

Run from the repository root in the existing pinned environment:

```bash
python examples/foundations/ordered_supports.py
python scripts/check_ordered_supports_prose.py
```

The complete program executes 100 circuits: two controlled-order witnesses, 88 basis/support cases for U, two complex products and eight full-support Fourier cases. The eight cumulative body fragments execute five circuits. These counts describe separate invocations. Dense global matrices are small-system references, not scalable implementation requirements. Passing these checks does not certify arbitrary register sizes, compiler routing, remote count strings, noise or hardware execution.

Expected output of the complete program:

```text
Support is an ordered tuple; its first qubit is the most significant local bit.
Input100, support(2, 0): occupied global index 4.
Input100, support(0, 2): occupied global index 5.
88 basis/support circuits: complex asymmetric gate;2/3qubit ordered pairs and4qubit nonadjacent supports.
Complex input, support(2, 0): 0.349879763, 0.025120237, 0.116626588, 0.008373412, 0.349879763, 0.025120237, 0.116626588, 0.008373412.
Complex input, support(0, 2): 0.317134573, 0.317134573, 0.105711524, 0.105711524, 0.057865427, 0.057865427, 0.019288476, 0.019288476.
8 full-support circuits: dimension8 Fourier matrix on ordered support(2,0,1).
Single-factor reduction, global unitarity, nonunitary reference and10invalid-input cases checked.
100 actual CPU complex128 circuits; atol=1e-12,rtol=0; no sorting, shots, routing or hardware.
```

### Understanding checks and transfer exercises

**4.4-A — Translate a new support.** In a four-qubit register, take S=`(3,1)` and input `1011`. Extract the local input bits and index. Apply C and reconstruct the global output, keeping spectators fixed.

**4.4-B — Diagnose sorting.** A collaborator sorts `(2,0)` before submitting C, claiming that the same qubit set means the same operator. Give the counterexample from the section. Why would an identity matrix be a poor test of this claim?

**4.4-C — Trace the sum.** For n=3, S=`(2,0)` and output b=`101`, list all four possible global input tuples in the boxed amplitude update. State which local matrix row is used. Does the input need to factor into independent qubit states?

**4.4-D — Interpret a limited success.** All computational probabilities agree for two implementations of the Fourier boundary case. What additional check is required here, and which sign pattern should the declared input produce? Explain why this still does not certify the whole framework.

<details markdown="1">
<summary>Answers and reasoning</summary>

**A.** The selected bits are `(b3,b1)=(1,0)`, local `10`, index 2. C maps that to `11`, so q3 remains 1 and q1 changes to 1; q0=1 and q2=1 stay fixed. The output is `1111`, global index 15. The separate author transfer check actually executes this four-qubit case and compares every amplitude and probability; its one circuit is outside the complete program's 100-circuit count.

**B.** On input `100`, support `(2,0)` produces `100` while `(0,2)` produces `101`. The identity matrix is invariant under changing local basis order and acts trivially in both cases, so agreement for that special matrix would not establish the general claim. Changing a support's order while holding a general matrix fixed changes its meaning.

**C.** Output `101` has spectator q1=0 and local output `(b2,b0)=(1,1)`, row 3. Local inputs `00,01,10,11` correspond respectively to global inputs `000,100,001,101`. Therefore the output amplitude is $U_{3,0}\psi_{000}+U_{3,1}\psi_{100}+U_{3,2}\psi_{001}+U_{3,3}\psi_{101}$. This expansion applies to an arbitrary joint vector; no product-state assumption appears.

**D.** Compare the full complex vector, including its declared phase convention. The expected signs in global order are `+,+,-,-,+,+,-,-`, divided by sqrt(8). Equal probabilities do not test those signs. The check still concerns particular matrices, inputs, precision and a released backend; it is not an all-size or all-backend correctness theorem.

</details>

### Sources, depth and next step

Depth **F**: unique basis extension, ordered local-index extraction, matrix entries, the full local-input sum and the unitary/spectator arguments are derived explicitly. The assigned background locators remain Nielsen and Chuang, 10th Anniversary Edition, §2.1.7 and §4.3. The derivation here explicitly fixes the local basis and support convention. Its proof and worked translations are original, using the explained prerequisite drafts and the actual released API checked above; source-access provenance is recorded separately in the section record.

The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/4.4.json) separates author execution from pending independent mathematical, implementation and reader review. This remains a working draft. Continue with the working draft [4.5 Permutations, SWAP, and relabeling](#sec-composite-systems-tensor-products-and-qubit-ordering-5).

<span id="sec-composite-systems-tensor-products-and-qubit-ordering-5"></span>

## 4.5 Permutations, SWAP, and relabeling

A program prints `001` where another prints `100`. Has a gate moved the state between qubits, has the same state been expressed in a different ordered basis, or have names merely changed? Those explanations require different corrections. We will specify each operation before translating it into code.

The prerequisites are [4.2](#sec-composite-systems-tensor-products-and-qubit-ordering-2), for the index bijection, and [4.4](#sec-composite-systems-tensor-products-and-qubit-ordering-4), for ordered supports. We retain $J_n(b)=\sum_{q=0}^{n-1}b_q2^{n-1-q}$: qubit 0 is the most significant bit. All spaces here contain finitely many distinguishable qubits with the same two-dimensional local basis. The examples use released FlagQuantum 0.3.1, PyTorch 2.13.0, CPU complex128, absolute tolerance $10^{-12}$ and relative tolerance zero. No state normalization or phase alignment repairs an incorrect permutation.

The eight formula–derivation–code–result units are cumulative. Run their fragments in order from the repository root. The complete companion is [permutations_swap.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/permutations_swap.py); its independent references and broader tests are described below.

<span id="formula-code-4-5-physical-swap"></span>

### 1. Physical SWAP changes the state at fixed qubit positions

**Formula.** On two selected qubits, define

$$
\operatorname{SWAP}|a,b\rangle=|b,a\rangle,\qquad
\operatorname{SWAP}=\begin{pmatrix}
1&0&0&0\\0&0&1&0\\0&1&0&0\\0&0&0&1
\end{pmatrix}.
$$

**Derivation.** The four columns are the images of `00,01,10,11`, respectively. Exchanging twice returns every basis vector, so linearity gives $\operatorname{SWAP}^2=I$. Its columns are an orthonormal permutation of the original basis; hence it is unitary and equals its own adjoint. Embedding this matrix at support `(0,2)` in a three-qubit register leaves the middle qubit fixed. With the original basis and labels held fixed, `100` becomes `001`. This is an active state change. Here “physical SWAP” names an executed gate operation; the example executes it in an ideal simulator, not on a device.

**FlagQuantum code.** The helper prepares each factor with `Circuit.unitary`, applies the swaps through the actual released `circuit.swap(a,b)` method, and checks statevector/probability shapes and dtypes. Here its swap sequence is exactly one call, `circuit.swap(0,2)`.

```python
import torch
from examples.foundations.permutations_swap import (
    DTYPE, ATOL, run, perm_matrix, inverse, moved_bits,
    scalar_permute, swap_sequence, renamed,
    complex_factors, entangled_reference)
from examples.foundations.ordered_supports import dense_embedding, controlled_flip
import flagquantum as fq
from examples.foundations.tensor_spaces import OPTIONS
circuit = fq.Circuit(3, dtype=DTYPE)
circuit.x(0)
circuit.swap(0,2)
result = fq.run(circuit, outputs=[fq.probabilities()], options=OPTIONS)
assert result.statevector().shape == result.probabilities.shape == (1,8)
state, probability = result.statevector()[0], result.probabilities[0]
assert swap_sequence((2,1,0)) == [(0,2)]
expected = torch.zeros(8, dtype=DTYPE); expected[1] = 1
assert torch.allclose(state, expected, rtol=0, atol=ATOL)
print('SWAP(0,2): 100 ->', format(int(probability.argmax()), '03b'))
```

```text
SWAP(0,2): 100 -> 001
```

<span id="formula-code-4-5-cycle-convention"></span>

### 2. Declare the direction of a general permutation

**Formula.** Let $p$ be a bijection of positions $\{0,\ldots,n-1\}$. Our convention is **old position q moves to position p(q)**. Define the moved bit tuple $f_p(b)$ and the linear map $P_p$ by

$$
[f_p(b)]_{p(q)}=b_q,\qquad
P_p|b\rangle=|f_p(b)\rangle.
$$

**Derivation.** Bijection gives exactly one bit for each output position, and distinct input tuples give distinct output tuples. Thus the images of the computational basis form that same orthonormal basis in a different order. Taking inner products of columns proves $P_p^\dagger P_p=I$. Moving each output factor back proves

$$
P_p^{-1}=P_p^\dagger=P_{p^{-1}}.
$$

A transposition cannot distinguish a permutation from its inverse. Instead take $p=(1,2,0)$: old q0 moves to q1, old q1 to q2, old q2 to q0. Then $f_p(a,b,c)=(c,a,b)$, while $f_{p^{-1}}(a,b,c)=(b,c,a)$. In particular, `100` goes to `010` in the forward direction and `001` in the inverse direction. Applying SWAP(0,1), then SWAP(0,2), realizes the forward cycle. Matrix multiplication places the later gate on the left. The helper uses a different valid decomposition: SWAP(0,2), then SWAP(1,2), which sends `(a,b,c)` through `(c,b,a)` to `(c,a,b)`. The code checks the actual helper sequence rather than assuming a unique decomposition.

```python
p = (1,2,0); P = perm_matrix(p)
basis100 = torch.eye(8, dtype=DTYPE)[:,4]
cycle, probability = run(p, [(0,1),(1,0),(1,0)])
assert swap_sequence(p) == [(0,2),(1,2)]
assert torch.allclose(cycle, P @ basis100, rtol=0, atol=ATOL)
assert torch.equal(perm_matrix(inverse(p)), P.mH)
print('forward:', format(int(probability.argmax()), '03b'))
print('inverse:', format(int((P.mH @ basis100).abs().argmax()), '03b'))
```

```text
forward: 010
inverse: 001
```

<span id="formula-code-4-5-coefficients"></span>

### 3. Move complex amplitudes without conjugating them

**Formula.** Expand an arbitrary joint state as $|\psi\rangle=\sum_b\psi_b|b\rangle$. Setting $c=f_p(b)$ in its image gives

$$
(P_p\psi)_c=\psi_{f_{p^{-1}}(c)},\qquad
\Pr_{P_p\psi}(c)=|\psi_{f_{p^{-1}}(c)}|^2.
$$

**Derivation.** Each output receives exactly one input amplitude, with coefficient 1. There is no amplitude sum, complex conjugation or extra phase in this permutation. The formula holds for entangled states as well as products. A coordinate permutation can change a fixed labeled outcome probability even though it preserves the multiset of probabilities and the norm.

For a phase-sensitive example, prepare q0 in $(\sqrt3/2,i/2)$, q1 in $|0\rangle$, and q2 in $(\sqrt{4/5},i\sqrt{1/5})$. Apply the controlled flip on `(0,1)` before permuting. Expanding those preparations gives

$$
|\psi\rangle=\sqrt{3/5}|000\rangle
+i\sqrt{3/20}|001\rangle
+i\sqrt{1/5}|110\rangle
-\sqrt{1/20}|111\rangle.
$$

The minus sign is the product of two imaginary amplitudes. The cycle moves the occupied indices `0,1,6,7` to `0,4,3,7`; their complex coefficients move unchanged. `entangled_reference()` stores this hand expansion. `scalar_permute` instead gathers input coefficients using binary strings, independently of the dense permutation matrix and SWAP synthesis.

```python
psi = entangled_reference()
active, probability = run(p, complex_factors(), entangle=True)
assert torch.allclose(active, P @ psi, rtol=0, atol=ATOL)
assert torch.allclose(active, scalar_permute(psi.tolist(), p), rtol=0, atol=ATOL)
assert abs(active[7].item() + (1/20)**.5) < ATOL
print('active probabilities:', [round(x,6) for x in probability.tolist()])
```

```text
active probabilities: [0.6, 0.0, 0.0, 0.2, 0.15, 0.0, 0.0, 0.05]
```

<span id="formula-code-4-5-passive-basis"></span>

### 4. A passive basis change describes the same physical state

**Formula.** Write the old ordered basis columns as $e_j$. Choose new basis columns $e'_j=P_pe_j$. If $x$ and $x'$ describe the **same abstract vector** in these two bases, then

$$
\sum_j e_jx_j=\sum_j e'_jx'_j
\quad\Longrightarrow\quad
x=P_px',\qquad \boxed{x'=P_p^\dagger x}.
$$

For the same linear operator and a Hermitian observable, respectively,

$$
A'=P_p^\dagger A P_p,\qquad
(x')^\dagger A'x'=x^\dagger Ax.
$$

**Derivation.** The first equality equates two coordinate expansions of one vector; substitute the definition of $e'_j$ and multiply by $P_p^\dagger$. If the old-coordinate equation is $y=Ax$, then $y'=P_p^\dagger y=P_p^\dagger AP_px'$, proving the operator rule. Substituting both transformed expressions in the quadratic form cancels $P_pP_p^\dagger$ twice, proving the expectation identity. It does not assume a product state.

For this convention the reordered qubit-label list is $(L_{p(0)},\ldots,L_{p(n-1)})$. In the cycle example this is `(reference,flag,signal)`. A new tuple assigns its first bit to old q1, its second to old q2 and its third to old q0. Consequently old physical `100` has new coordinates `001`. This also follows directly from $P_p^\dagger|100\rangle$; the forward active result `010` answers a different question.

Let $A=Z_0$, the local Pauli Z on old q0, with eigenvalues +1 and −1. For the displayed $\psi$, the original expectation is $1-2(1/4)=1/2$. After the active cycle, fixed q0 carries the former q2 value, giving $1-2(1/5)=3/5$. After a passive conversion, old q0 is at new position 2: $A'=Z_2$, and its expectation remains 1/2.

```python
Z = torch.diag(torch.tensor([1,-1], dtype=DTYPE))
A = dense_embedding(Z, 3, (0,))
passive = P.mH @ psi
Aprime = P.mH @ A @ P
assert torch.allclose(Aprime, dense_embedding(Z,3,(2,)), rtol=0, atol=ATOL)
def expectation(v, observable):
    return float(torch.vdot(v, observable @ v).real)
print('original Z0:', round(expectation(psi,A),6))
print('active, fixed Z0:', round(expectation(active,A),6))
print('passive, transformed Z0:', round(expectation(passive,Aprime),6))
```

```text
original Z0: 0.5
active, fixed Z0: 0.6
passive, transformed Z0: 0.5
```

The passive calculations are classical coordinate conversions of the state verified in unit 3; they require no new quantum execution. If one holds $A$ fixed while converting only the coordinates, one is generally evaluating a different physical observable. The same rule applies to computational-outcome projectors: transform their labels and matrices together to preserve event probabilities. A permutation basis change only reorders product-basis vectors. A general unitary basis change, such as an X-basis conversion, can mix them and is not merely a qubit permutation.

<span id="formula-code-4-5-support-conjugation"></span>

### 5. Transform ordered supports as well as state coordinates

**Formula.** For the embedding $E_S(U)$ from 4.4 and ordered support $S=(s_0,\ldots,s_{k-1})$,

$$
P_p^\dagger E_S(U)P_p=E_{p^{-1}(S)}(U),\qquad
p^{-1}(S)=(p^{-1}(s_0),\ldots,p^{-1}(s_{k-1})).
$$

**Derivation.** Apply the left-hand side to any basis tuple b. The rightmost $P_p$ puts bit $b_q$ at old position $p(q)$. Thus the ordered input bits read by $E_S(U)$ are $b_{p^{-1}(s_0)},\ldots,b_{p^{-1}(s_{k-1})}$. That operator replaces precisely those bits with its local output tuple, weighted by the corresponding entry of U. The final $P_p^\dagger$ moves them back to positions $p^{-1}(s_j)$, preserving the local tuple order and all spectator bits. This is exactly the 4.4 basis prescription for the right-hand side. Equality on a spanning basis proves the operator identity for any U, including nonunitary linear maps. Admission as a deterministic circuit gate still separately requires U to be unitary.

For $p=(1,2,0)$, old support `(2,0)` becomes `(1,2)`. Sorting the transformed tuple would in general change the meaning of U. Check the identity as matrices and as two actual circuit paths on the complex joint input: apply the old-support gate then the inverse cycle, or apply the inverse cycle then the transformed-support gate.

```python
S = (2,0); T = tuple(inverse(p)[q] for q in S)
C = controlled_flip()
left = P.mH @ dense_embedding(C,3,S) @ P
assert torch.allclose(left, dense_embedding(C,3,T), rtol=0, atol=ATOL)
a, _ = run(inverse(p), complex_factors(), True, before=(S,C))
b, _ = run(inverse(p), complex_factors(), True, after=(T,C))
assert torch.allclose(a,b,rtol=0,atol=ATOL)
print('ordered support:', S, '->', T)
print('two circuit paths: full complex coordinates agree')
```

```text
ordered support: (2, 0) -> (1, 2)
two circuit paths: full complex coordinates agree
```

<span id="formula-code-4-5-labels"></span>

### 6. Renaming a label does not move a state

**Formula.** Let an ordered register list be $L=(L_0,\ldots,L_{n-1})$. An injective replacement of names $r$ gives

$$
L'=(r(L_0),\ldots,r(L_{n-1})),\qquad x'=x,\qquad A'=A.
$$

**Derivation.** Every tuple position and its local basis stays fixed; only the text naming that position changes. Therefore the basis columns, coefficient array and operator entries stay fixed. References to the renamed qubit in application metadata must be updated consistently. This is distinct from *reordering* the register list, which changes which factor each tuple position denotes and requires the passive coordinate rule above. These names are application metadata, not a claim that FlagQuantum exposes this named-register API.

| Action | State/coordinates | Operator/observable | Quantum operation |
|---|---|---|---|
| Active permutation in fixed basis | $x\mapsto P_px$ | A fixed observable stays A | Execute a gate sequence |
| Passive basis $e'_j=P_pe_j$ | $x'=P_p^\dagger x$ | $A'=P_p^\dagger AP_p$ | Coordinate conversion only |
| Rename labels in fixed list positions | Same array | Same matrix; update name references | Metadata only |

An active permutation is not always observable on a chosen input: SWAP leaves $|00\rangle$ invariant. That special case does not identify it with renaming.

```python
labels = ('signal','reference','flag')
new_names = renamed(labels, {'signal':'data'})
before = psi.clone()
assert torch.equal(psi,before)
print('rename in fixed positions:', new_names)
print('passive reordered labels:', tuple(labels[q] for q in p))
```

```text
rename in fixed positions: ('data', 'reference', 'flag')
passive reordered labels: ('reference', 'flag', 'signal')
```

<span id="formula-code-4-5-composition"></span>

### 7. Compose destinations in execution order

**Formula.** If p acts first and r acts second, an old factor q moves first to $p(q)$ and then to $r(p(q))$. Consequently

$$
P_rP_p=P_{r\circ p},\qquad (r\circ p)(q)=r(p(q)).
$$

**Derivation.** Follow a single bit through both basis permutations. All bits end in those destinations, so the composite basis image and hence its linear extension are determined. This also proves the identity rule and the inverse formula used above. Disjoint transpositions commute, but transpositions sharing a qubit need not; a general sequence cannot be reversed without changing the map. `swap_sequence` places the required old factor at each destination in turn. Once a destination is fixed, its required factor cannot be needed elsewhere by bijection; later swaps leave it fixed. At most n−1 swaps suffice because the final position is forced after the first n−1. This is an all-to-all mathematical decomposition, not a hardware connectivity or native-gate cost guarantee.

```python
r = (1,0,2)
composed = tuple(r[p[q]] for q in range(3))
reverse = tuple(p[r[q]] for q in range(3))
assert torch.equal(perm_matrix(r) @ P, perm_matrix(composed))
assert not torch.equal(perm_matrix(composed), perm_matrix(reverse))
assert swap_sequence((0,1,2)) == []
print('first p, then r:', composed)
print('reversed order:', reverse)
```

```text
first p, then r: (0, 2, 1)
reversed order: (2, 1, 0)
```

<span id="formula-code-4-5-boundaries"></span>

### 8. Reject ambiguous or invalid contracts before execution

The permutation requires a nonempty tuple containing every integer from 0 through n−1 exactly once. Booleans and floating-point approximations to integers are rejected. Bits require literal 0 or 1 integers. Renaming requires unique nonempty names before and after replacement, and keys must refer to existing labels. The body examples below make no quantum calls.

```python
invalid = [lambda: perm_matrix((0,0)),
           lambda: perm_matrix((0,2)),
           lambda: perm_matrix((False,1)),
           lambda: moved_bits((1,), (1,0)),
           lambda: renamed(('a','b'), {'a':'b'})]
rejected = 0
for action in invalid:
    try:
        action()
    except ValueError:
        rejected += 1
assert rejected == 5
print('invalid permutation/bit/rename declarations:', rejected, 'rejected')
```

```text
invalid permutation/bit/rename declarations: 5 rejected
```

Do not infer a convention from a statevector alone. Ask whether the intended action is active, passive or a rename; require the old and new ordered labels, destination direction, basis, and phase/precision contract. Qubit permutations introduce no phase, so full complex equality is the appropriate check here. Equal computational probabilities alone would miss a wrong sign or relative phase in a circuit implementation. A tolerance above the discrepancy would also conceal failure; the stated tolerance is for these small double-precision examples, not an all-size error bound.

Run the companion and the body-output checker:

```bash
python examples/foundations/permutations_swap.py
python scripts/check_permutations_swap_prose.py
```

The complete program executes **450 circuits**: every basis input under every permutation for n=1,2,3,4 (442), all six permutations of the complex three-qubit joint state (6), and the two support-conjugation paths (2). Identity permutations and the n=1 boundary execute preparations with no SWAP gates. Dense references and an independent binary-string gather check every complex output. The eight body fragments execute five circuits in a separate invocation. These are author execution checks, not an independent review or a hardware experiment.

Expected output of the complete program:

```text
Convention: p[q] is the destination of old qubit q; qubit0 is most significant.
442 basis circuits: every permutation and every basis input for n=1,2,3,4.
Input100: active cycle index2; passive coordinate index1.
Z0: original 0.500000; active fixed observable 0.600000; passive transformed observable 0.500000.
Passive ordered support (2, 0) -> (1, 2): two actual circuit paths agree in every complex coordinate.
Composition order, identity, inverse, metadata rename and10invalid declarations checked.
450 actual CPU complex128 circuits; atol=1e-12,rtol=0; no phase alignment, shots or hardware.
```

### Understanding checks and transfer exercises

**4.5-A — New nonadjacent swap.** For four qubits, execute SWAP(1,3) on `1100`. Give the output tuple and index. Does this swap commute with SWAP(0,2)? Explain without assuming commutativity of general permutations.

**4.5-B — Direction check.** For p=(2,0,1), find the active output of `100`, the passive coordinates of that same original state in the basis $e'_j=P_pe_j$, and the new ordered labels. Which operation changes the physical state?

**4.5-C — Measurement and support.** For p=(1,2,0), convert old $Z_0$ and support `(0,2)` to passive coordinates. Explain why keeping $Z_0$ numerically unchanged can give the wrong event interpretation. Does the local controlled-flip matrix itself need to change under the ordered-support rule?

**4.5-D — Diagnose a repair.** A collaborator reverses a label list but keeps the statevector and every numeric gate target unchanged, calling it “just a rename.” What must be clarified? Why do tests using only $|000\rangle$ fail to diagnose the problem?

<details markdown="1">
<summary>Answers and reasoning</summary>

**A.** Bits q1=1 and q3=0 exchange, giving `1001`, index 9. SWAP(1,3) and SWAP(0,2) have disjoint supports, so each leaves the other's selected bits unchanged; following any basis tuple proves they commute. A separate author transfer circuit executes the first swap and compares all 16 amplitudes/probabilities. This one circuit is additional to the complete program.

**B.** The active output is `001`, while $P_p^\dagger|100\rangle=|010\rangle$ gives passive coordinates. The ordered labels become `(flag,signal,reference)` for the section's original list. The active gate changes the state at fixed physical positions; the passive conversion describes the same state in the declared new basis.

**C.** Inverse p=(2,0,1), so old $Z_0$ becomes new $Z_2$, and ordered support `(0,2)` becomes `(2,1)`. Keeping the numerical $Z_0$ would ask about new position 0, corresponding to old q1. Keep the same local matrix U and preserve that transformed support order. Sorting it would require an additional local basis conversion; it is not part of this rule.

**D.** Determine whether names are being replaced in fixed positions or the ordered physical-factor list is being rearranged. If it is rearranged, convert coordinates, operator matrices and target positions consistently. If only names change, keep each physical position fixed and update references to those names. Every permutation leaves `000` fixed, so that input cannot distinguish the interpretations. Use an asymmetric basis input, a non-self-inverse cycle and complex joint amplitudes.

</details>

### Sources, depth and next step

Depth **F**: the basis prescription, unitarity, inverse, composition, amplitude rule, passive coordinate/observable transformation, ordered-support conjugation and SWAP decomposition are proved explicitly. Nielsen and Chuang, 10th Anniversary Edition, §4.3 is the assigned background locator; this section supplies its own convention-fixed derivations and does not claim a fresh inspection of the user-local PDF. The released FlagQuantum SWAP method is exercised directly; implementation evidence and source-access limits appear in the [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/4.5.json).

This is an author-verified working draft, with independent mathematical, implementation and reader review pending. Continue with the working draft [4.6 Tensor reshaping as indexed mathematics](#sec-composite-systems-tensor-products-and-qubit-ordering-6).

<span id="sec-composite-systems-tensor-products-and-qubit-ordering-6"></span>

## 4.6 Tensor reshaping as indexed mathematics

A statevector and a rank-n amplitude tensor can hold exactly the same coefficients. The tensor exposes which bit belongs to which qubit; it does not add information. This representation lets us implement a local operator without constructing its full-register matrix. To trust that implementation, we need to identify the index represented by every axis before using `reshape`, `permute` or matrix multiplication.

The prerequisites are [4.2](#sec-composite-systems-tensor-products-and-qubit-ordering-2), for the binary index bijection, and [4.4](#sec-composite-systems-tensor-products-and-qubit-ordering-4), for ordered-support gate action. All claims here concern a finite register of n≥1 qubits with an explicit computational basis. The examples use released FlagQuantum 0.3.1 and PyTorch 2.13.0 on CPU with complex128 statevectors. The tolerance is absolute $10^{-12}$ with relative tolerance zero. We compare full complex coordinates without phase alignment or normalization repair.

The eight formula–derivation–code–result units below are cumulative. Run them in order from the repository root. The complete companion [tensor_reshaping.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/tensor_reshaping.py) includes strict input checks, an independent scalar reference, broader executions and the minimal contraction implementation.

<span id="formula-code-4-6-vector-contract"></span>

### 1. Separate the execution batch axis from the amplitude axes

**Formula.** Our mathematical input is one vector $x\in\mathbb C^{2^n}$. The executed result here stores a batch of one vector:

$$
R\in\mathbb C^{1\times2^n},\qquad x_j=R_{0,j}.
$$

**Derivation.** The first coordinate of R selects an execution batch member; j selects a basis amplitude. It is not an additional qubit. First select that member and check the resulting one-dimensional shape. A library accepting a batch of states would need a separately specified batching contract; the minimal helper in this section rejects it.

Prepare the complex joint state used in 4.5, but reproduce its preparation explicitly here. Local preparation on q0 is $(\sqrt3/2,i/2)$, q1 starts in zero, and q2 is $(\sqrt{4/5},i\sqrt{1/5})$. A controlled flip on ordered support `(0,1)` gives

$$
x=\sqrt{3/5}|000\rangle+i\sqrt{3/20}|001\rangle
+i\sqrt{1/5}|110\rangle-\sqrt{1/20}|111\rangle.
$$

This hand expansion follows by multiplying local coefficients and applying the controlled flip to the q1 bit. It supplies a phase-sensitive reference with nonzero complex joint amplitudes, rather than relying on a product-state shortcut in the contraction proof.

```python
import torch
import flagquantum as fq
from examples.foundations.tensor_spaces import prepare_matrix, OPTIONS
from examples.foundations.ordered_supports import controlled_flip, complex_gate, scalar_scatter
from examples.foundations.tensor_reshaping import (
    DTYPE, ATOL, checked_vector, axis_order, undo_order, apply_local,
    complex_factors, entangled_reference, checked_matrix)
circuit = fq.Circuit(3, dtype=DTYPE)
for q, factor in enumerate(complex_factors()):
    circuit.unitary(q, unitary=prepare_matrix(torch.tensor(factor,dtype=DTYPE)))
circuit.unitary(0,1,unitary=controlled_flip())
result = fq.run(circuit, outputs=[fq.probabilities()], options=OPTIONS)
assert result.statevector().shape == result.probabilities.shape == (1,8)
x = checked_vector(result.statevector()[0], 3)
assert torch.allclose(x,entangled_reference(),rtol=0,atol=ATOL)
print('batch result:', tuple(result.statevector().shape), 'single vector:', tuple(x.shape))
```

```text
batch result: (1, 8) single vector: (8,)
```

<span id="formula-code-4-6-binary-axes"></span>

### 2. Derive the tensor axes from the basis-index formula

**Formula.** Let axis q denote the bit of qubit q, and define

$$
T_{b_0,\ldots,b_{n-1}}=x_{J_n(b)},\qquad
J_n(b)=\sum_{q=0}^{n-1}b_q2^{n-1-q}.
$$

**Derivation.** The last bit changes the index by one, the preceding bit by two, and so on. Therefore a logical row-major reshape to `(2,)*n`, whose last axis varies fastest, realizes this indexing rule. Conversely, flattening these axes in the same logical order returns x, because 4.2 proves that every bit tuple has exactly one index. No conjugation, summation, qubit movement or physical evolution occurs.

For n=3, the logical offsets of axes `(q0,q1,q2)` are `(4,2,1)`. Thus `T[1,1,0]` is the amplitude at index 6, $i\sqrt{1/5}$. The vector dimension is eight, the tensor rank is three, and each axis length is two: those are different quantities.

```python
from itertools import product
T = x.reshape(2,2,2)
for bits in product((0,1),repeat=3):
    j = int(''.join(map(str,bits)),2)
    assert T[bits].item() == x[j].item()
assert torch.equal(T.reshape(8),x)
print('tensor shape:', tuple(T.shape))
print(f'T[1,1,0] = x[6]: {T[1,1,0].imag.item():.9f}j')
```

```text
tensor shape: (2, 2, 2)
T[1,1,0] = x[6]: 0.447213595j
```

<span id="formula-code-4-6-pack-support"></span>

### 3. Move an ordered support to the leading axes

**Formula.** Take a nonempty ordered support $S=(s_0,\ldots,s_{k-1})$ of distinct qubits. List its complement in ascending order as $C=(c_0,\ldots,c_{n-k-1})$. Define the axis order $o=S\mathbin{\Vert}C$, where $\Vert$ means concatenation. For local bits a and spectator bits d, pack

$$
A_{J_k(a),J_{n-k}(d)}=T_b,
\qquad b_{s_r}=a_r,\quad b_{c_t}=d_t.
$$

For k=n, the complement is empty: define its sole index as $J_0(())=0$, so A has one column. This convention introduces no zero-qubit physical register.

**Derivation.** `T.permute(o)` makes new axis r refer to old axis `o[r]`; it does not sort S. Its first k axes are the local tuple and its remaining axes are the spectator tuple. Flattening each group in that logical order gives row $J_k(a)$ and column $J_{n-k}(d)$. Both binary maps are bijections, and S and C partition the register; hence every original coefficient appears exactly once in A.

With S=`(2,0)`, C=`(1,)` and o=`(2,0,1)`, the packing rule is

$$
A_{2b_2+b_0,b_1}=T_{b_0,b_1,b_2}.
$$

Input tuple `101`, global index 5, goes to row 3, column 0. Directly reshaping the original vector to `(4,2)` instead groups `(q0,q1)` into rows and q2 into columns. Use distinct integer markers to expose the difference; they are an indexing fixture, not a normalized quantum state.

```python
S = (2,0); order = axis_order(3,S)
A = T.permute(order).reshape(4,2)
markers = torch.arange(8).reshape(2,2,2)
packed_markers = markers.permute(order).reshape(4,2)
assert packed_markers[3,0].item() == 5
assert markers.reshape(4,2)[3,0].item() == 6
for bits in product((0,1),repeat=3):
    assert A[2*bits[2]+bits[0],bits[1]].item() == T[bits].item()
print('axes:', order, 'packed shape:', tuple(A.shape))
print('row3,column0: permute then reshape =', packed_markers[3,0].item(),
      '; reshape alone =', markers.reshape(4,2)[3,0].item())
```

```text
axes: (2, 0, 1) packed shape: (4, 2)
row3,column0: permute then reshape = 5 ; reshape alone = 6
```

Changing tensor-axis order is a change of coordinate layout. If its flattened array is later interpreted using the old qubit order, it can represent a different vector. Keep the axis labels with the array. A layout conversion alone does not submit a SWAP gate; active operations and passive coordinate descriptions are distinguished in 4.5.

<span id="formula-code-4-6-contract"></span>

### 4. Identify the local gate sum with a matrix contraction

**Formula.** Write the local matrix in the ordered S basis as $U\in\mathbb C^{2^k\times2^k}$. Then

$$
B=UA,\qquad
B_{r,t}=\sum_{v=0}^{2^k-1}U_{r,v}A_{v,t}.
$$

**Derivation.** Fixing column t fixes all spectator bits d. Each column is the group of amplitudes that can mix under the local operator. Matrix multiplication sums over local input index v while holding t fixed. Row r labels the new local output. There is no conjugation: this is linear operator action, not an inner product between two statevectors.

Use the explicitly derived complex asymmetric two-qubit matrix U from 4.4 (`complex_gate()`). To see one entry before trusting `@`, choose output local row 1 and spectator column 0. Its four terms have input tuples `000,100,001,101`, respectively, since the local input order is `(b2,b0)` and b1 is zero. Thus

$$
B_{1,0}=U_{1,0}x_0+U_{1,1}x_4+U_{1,2}x_1+U_{1,3}x_5.
$$

```python
U = complex_gate()
B = U @ A
manual = sum(U[1,v]*x[j] for v,j in enumerate((0,4,1,5)))
assert torch.allclose(B[1,0],manual,rtol=0,atol=ATOL)
wrong = U.conj() @ A
assert not torch.allclose(B,wrong,rtol=0,atol=ATOL)
print('local contraction:', tuple(U.shape), '@', tuple(A.shape), '->', tuple(B.shape))
print('one four-term sum agrees; conjugating U changes this result')
```

```text
local contraction: (4, 4) @ (4, 2) -> (4, 2)
one four-term sum agrees; conjugating U changes this result
```

<span id="formula-code-4-6-unpack"></span>

### 5. Undo the axis permutation and prove the full indexed action

**Formula.** Let $h(q)$ be the position of old axis q in o, so $o_{h(q)}=q$. Unpack B into n binary axes, then restore their old order with h. The resulting vector y satisfies

$$
y_{J_n(b)}
=\sum_{v=0}^{2^k-1}U_{J_k(b_S),v}\,
 x_{J_n(b[S\leftarrow\operatorname{bits}_k(v)])}.
$$

Here $b_S=(b_{s_0},\ldots,b_{s_{k-1}})$, and $b[S\leftarrow a]$ replaces just those selected bits, leaving all others fixed.

**Derivation.** By unit 3, packing the input tuple with local bits $\operatorname{bits}_k(v)$ and spectator bits $b_C$ yields $A_{v,J_{n-k}(b_C)}$. Unit 4 multiplies that coefficient by $U_{J_k(b_S),v}$ and sums over v. Reshaping B exposes the axes in o order; permuting by h sends each one back to its declared q position. Flattening in q0,…,q(n−1) order assigns it index $J_n(b)$. Substitution yields the displayed sum, exactly the 4.4 coefficient formula. This proves the algorithm for arbitrary joint amplitudes and any linear U at finite n, without constructing a global matrix or assuming product states.

For o=`(2,0,1)`, the restoring order is h=`(1,2,0)`. Reusing o would fail because this cycle is not self-inverse. Compare the unpacked result to the minimal helper, an independent scalar input-scatter implementation and the actual FlagQuantum local gate.

```python
restore = undo_order(order)
y = B.reshape(2,2,2).permute(restore).reshape(8)
assert restore == (1,2,0)
assert torch.allclose(y,apply_local(x,U,3,S),rtol=0,atol=ATOL)
scalar = torch.tensor(scalar_scatter(U,x.tolist(),3,S),dtype=DTYPE)
assert torch.allclose(y,scalar,rtol=0,atol=ATOL)
circuit.unitary(*S,unitary=U)
after = fq.run(circuit,outputs=[fq.probabilities()],options=OPTIONS)
assert after.statevector().shape == after.probabilities.shape == (1,8)
assert torch.allclose(after.statevector()[0],y,rtol=0,atol=ATOL)
assert torch.allclose(after.probabilities[0],y.abs().square(),rtol=0,atol=ATOL)
print('restoring axes:', restore)
print('FlagQuantum probabilities:', [round(v,9) for v in after.probabilities[0].tolist()])
```

```text
restoring axes: (1, 2, 0)
FlagQuantum probabilities: [0.373653811, 0.001346189, 0.12455127, 0.00044873, 0.373653811, 0.001346189, 0.12455127, 0.00044873]
```

The minimal helper implements precisely `reshape → permute → reshape → matrix multiply → reshape → inverse permute → flatten`. It stores the state and a $2^k$-square local matrix, rather than a $2^n$-square operator. Its packed amplitude array still has $2^n$ entries: this is a dense-state algorithm, not a tensor-network compression. For a dense local matrix, each of $2^{n-k}$ columns requires $2^{2k}$ scalar multiply/add terms, giving order $2^{n+k}$ arithmetic. Packing may allocate additional state-sized storage. These operation counts are not measured performance claims about the FlagQuantum backend's internal algorithm.

<span id="formula-code-4-6-layout"></span>

### 6. Distinguish logical axes, strides and complex adjoints

**Formula.** Tensor-axis permutation obeys

$$
V_{a_0,\ldots,a_{n-1}}=T_b,\qquad b_{o_r}=a_r.
$$

It copies the logical value into the corresponding coordinate without complex conjugation. Storage strides describe memory access; they are not an additional part of the physical state.

**Derivation.** The same logical tensor can use different layouts. A permutation may expose a noncontiguous view; a subsequent `reshape` may need a copy. We rely on the documented logical order, not on whether storage is shared. A `.view` with a new shape requires compatible strides and can fail where `reshape` succeeds. `.contiguous()` reorganizes storage while preserving entries. In contrast, a matrix adjoint conjugates entries as well as transposing indices; using it in place of an axis rearrangement generally changes amplitudes.

The runtime's actual PyTorch 2.13 docstrings are preserved in the evidence. Public PyTorch API documentation describes [reshape](https://docs.pytorch.org/docs/stable/generated/torch.reshape.html), [permute](https://docs.pytorch.org/docs/stable/generated/torch.permute.html) and [view](https://docs.pytorch.org/docs/stable/generated/torch.Tensor.view.html); those rolling links can describe newer releases. The pinned execution checks below establish the behavior used here.

```python
V = T.permute(order)
assert not V.is_contiguous()
assert torch.equal(V.reshape(4,2),V.contiguous().view(4,2))
failed_view = False
try:
    V.view(4,2)
except RuntimeError:
    failed_view = True
assert failed_view
assert not torch.equal(V,V.conj())
print('permuted layout contiguous:', V.is_contiguous())
print('view rejected incompatible strides:', failed_view)
print('reshape agrees with contiguous copy; conjugation changes complex entries')
```

```text
permuted layout contiguous: False
view rejected incompatible strides: True
reshape agrees with contiguous copy; conjugation changes complex entries
```

The rejected view is an intentional boundary demonstration, not a failed quantum execution. This contract neither promises zero-copy reshaping nor permits dropping axis metadata after a copy.

<span id="formula-code-4-6-boundaries"></span>

### 7. Check single-axis, full-support and nonunitary boundaries

For k=1, packing produces a two-row matrix: each spectator column undergoes the same single-qubit map. For k=n, there is one spectator column, and U acts in the declared full support order, which can differ from `(0,…,n−1)`. Identity U returns every amplitude unchanged because packing and unpacking are inverse bijections.

The proof is linear algebra and does not require unitarity. If U is unitary, each column's squared norm is preserved by $A_t^\dagger U^\dagger UA_t=A_t^\dagger A_t$; summing columns preserves the global norm. A general linear map can change the norm. It must not be silently normalized and submitted as a deterministic gate.

```python
assert torch.equal(apply_local(x,torch.eye(4,dtype=DTYPE),3,S),x)
assert torch.equal(apply_local(x,torch.eye(8,dtype=DTYPE),3,(2,0,1)),x)
M = torch.tensor([[1,2j],[0,0]],dtype=DTYPE)
linear = apply_local(x,M,3,(1,))
linear_scalar = torch.tensor(scalar_scatter(M,x.tolist(),3,(1,)),dtype=DTYPE)
assert torch.allclose(linear,linear_scalar,rtol=0,atol=ATOL)
assert abs(torch.vdot(linear,linear).real.item()-1) > .1
print('identity and full support preserve every coefficient')
print('general linear-map squared norm:', round(torch.vdot(linear,linear).real.item(),6))
```

```text
identity and full support preserve every coefficient
general linear-map squared norm: 1.75
```

These are classical reference calculations on the already verified input, not extra circuit calls. The helper checks finite CPU complex128 vectors and matrices but deliberately allows unnormalized vectors and nonunitary linear maps. The separate circuit path requires a normalized physical preparation and a unitary gate.

<span id="formula-code-4-6-rejections"></span>

### 8. Reject dimension and convention mismatches

The input vector must have shape `(2**n,)`, not `(1,2**n)` or `(2,)*n`. A support contains distinct, in-range integer qubit positions in the intended order. The local matrix must have shape `(2**k,2**k)`. No automatic squeezing, sorting, precision conversion or replacement of nonfinite values is permitted by the helper.

```python
invalid = [lambda: checked_vector(x[None,:],3),
           lambda: checked_vector(x,2),
           lambda: axis_order(3,(0,0)),
           lambda: axis_order(3,(0,3)),
           lambda: apply_local(x,torch.eye(2,dtype=DTYPE),3,S),
           lambda: checked_matrix(M,1,unitary=True)]
rejected = 0
for action in invalid:
    try:
        action()
    except ValueError:
        rejected += 1
assert rejected == 6
print('batch, length, duplicate/range support, matrix shape and gate unitarity:', rejected, 'rejected')
```

```text
batch, length, duplicate/range support, matrix shape and gate unitarity: 6 rejected
```

Run the companion and the actual-body output checker:

```bash
python examples/foundations/tensor_reshaping.py
python scripts/check_tensor_reshaping_prose.py
```

The complete program executes **201 ideal circuits**: 186 basis/support cases and 15 complex joint-state cases. It covers every nonempty ordered support and every basis input through three qubits, plus four-qubit supports `(3,1)`, `(1,3)` and `(2,0,3,1)`. Local Fourier matrices with complex row phases exercise dimensions two, four, eight and sixteen; finite geometric sums establish their orthonormal columns, and row phases preserve the inner products. Twenty-three additional arbitrary-vector classical checks and the nonunitary boundary compare packed contraction, independent scalar scatter and dense embeddings. Dense embeddings are used only as a small-system validation reference, not in `apply_local`.

The eight body fragments execute two circuits in a separate invocation and check exact printed outputs. A separate four-qubit transfer is recorded below. Evidence applies to the stated fixtures, version and precision; it does not certify arbitrary sizes, batched execution, backend internals, GPU memory behavior, noisy simulation or hardware.

Expected output of the complete program:

```text
Logical axes(q0,...,q[n-1]); last bit varies fastest; batch axis excluded.
186 basis circuits; all nonempty ordered supports through3qubits plus3four-qubit supports.
15 complex joint-state circuits;23arbitrary-vector classical cases; scalar/dense/packed references agree.
Support(2,0), axes(2, 0, 1): input101 -> row3,column0,value5.
Identity, full support, noncontiguous layout, nonunitary linear map and11invalid contracts checked.
201 actual CPU complex128 circuits; atol=1e-12,rtol=0; no phase alignment, shots or hardware.
```

### Understanding checks and transfer exercises

**4.6-A — New packing.** For n=4, S=`(3,1)` and ascending complement C, locate input tuple `1011` in the packed matrix: give o, its global index, packed row and column, packed shape and restoring axis order. Apply the controlled flip whose first local bit is control. What output tuple results?

**4.6-B — Restore correctly.** For o=`(2,0,1)`, explain why applying `permute(o)` twice does not generally restore T. Give a coefficient marker that detects the mistake.

**4.6-C — Expand a contraction.** For S=`(2,0)`, write the four input tuples contributing to output tuple `101`, and identify its local row and spectator column. Where would an erroneous conjugation enter?

**4.6-D — Diagnose storage and gate claims.** A collaborator says `reshape` must be free because it only changes shape, that a rank-four tensor is a four-dimensional vector space, and that normalizing the result of M makes M a valid gate. Explain the three errors separately.

<details markdown="1">
<summary>Answers and reasoning</summary>

**A.** C=`(0,2)`, o=`(3,1,0,2)`, and J=11. Selected bits `(b3,b1)=(1,0)` give row 2; spectator bits `(b0,b2)=(1,1)` give column 3. The matrix shape is `(4,4)`, and restoring order h=`(2,1,3,0)`. Controlled flip maps local `10` to `11`, so q1 changes to 1, giving global `1111`, index 15. The separate author transfer actually executes this four-qubit circuit and checks all 16 complex amplitudes/probabilities against packed and scalar references.

**B.** The correct inverse is `(1,2,0)`. With `T=arange(8).reshape(2,2,2)`, the original marker at `(1,0,0)` is 4, whereas `T.permute(o).permute(o)[1,0,0]` is 2. The two cycles compose to the inverse cycle, not to the identity.

**C.** Spectator b1=0, local output `(b2,b0)=(1,1)`, row 3, column 0. Local input `00,01,10,11` gives global `000,100,001,101`. Thus the result is $U_{3,0}x_0+U_{3,1}x_4+U_{3,2}x_1+U_{3,3}x_5$. No term conjugates U or x; replacing U by `U.conj()` or using an adjoint would implement a different linear map in general.

**D.** A reshape can allocate to preserve logical order when strides are incompatible, so “shape only” is a mathematical description, not a zero-cost storage guarantee. Four binary axes have 16 entries; rank counts axes, while the coefficient vector space has dimension 16. Finally, output-dependent normalization is generally nonlinear and does not turn a nonunitary matrix into a deterministic unitary gate. A legitimate measurement/filter interpretation needs additional operations and probabilities, outside this section's circuit contract.

</details>

### Sources, depth and next step

Depth **F**: binary-axis correspondence, packing bijection, contraction, inverse-axis restoration and the full indexed local-action identity are derived at finite n, with unitarity treated separately. Nielsen and Chuang, 10th Anniversary Edition, §2.1.7 is the assigned tensor-product background. No fresh inspection of the user-local PDF is claimed; the proofs above specify the convention independently. Actual released FlagQuantum and installed PyTorch contracts are checked in the [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/4.6.json).

This remains an author-verified working draft. Independent mathematical, implementation and reader review are pending. Continue with the working draft [4.7 The no-cloning theorem](#sec-single-qubit-states-and-rotations-8).

<span id="sec-single-qubit-states-and-rotations-8"></span>

## 4.7 The no-cloning theorem

Copying a classical bit means reproducing one of two distinguishable values. Cloning an unknown qubit would require something stronger: one fixed operation would have to reproduce its entire pure state, including arbitrary relative amplitudes, on a second system. A gate that copies the values zero and one need not clone their superpositions.

The prerequisites are [4.1](#sec-composite-systems-tensor-products-and-qubit-ordering-1), for product states and inner-product factorization, and [3.4](ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-4), for unitary evolution. We will prove the finite pure-state no-cloning theorem for one fixed unitary with one fixed blank. Numerical examples illustrate a particular failed cloning attempt; they do not prove a universal impossibility by testing finitely many states.

The eight formula–derivation–code–result units are cumulative. Run from the repository root using released FlagQuantum 0.3.1 and PyTorch 2.13.0, CPU complex128, absolute tolerance $10^{-12}$ and relative tolerance zero. The complete companion is [no_cloning.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/no_cloning.py). Full complex amplitudes are checked without phase alignment. The theorem itself explicitly allows physically irrelevant whole-output phases.

<span id="formula-code-4-7-contract"></span>

### 1. State the universal copying contract

**Formula.** Let A and B be two copies of a finite state space of dimension at least two. Fix a normalized blank $|b\rangle_B$, independent of the input. A perfect pure-state cloner would be a **single unitary W**, also independent of the input, satisfying

$$
W(|\psi\rangle_A\otimes|b\rangle_B)
=e^{i\alpha_\psi}|\psi\rangle_A\otimes|\psi\rangle_B
$$

for every normalized $|\psi\rangle$. The output phase $\alpha_\psi$ is allowed to depend on the input. We require two separate copies with joint product state $|\psi\rangle\otimes|\psi\rangle$, not merely matching computational-basis frequencies.

**Derivation and assumptions.** “Unknown” means the operation cannot receive a classical amplitude description and be redesigned for that description. The blank is the same in every run. The input system remains as one output copy; the blank becomes the other. We will use only linearity, unitary inner-product preservation and the tensor-product inner product. This proof does not presume a measurement protocol or a state-tomography algorithm.

For a concrete attempt take the blank $|0\rangle$ and the following fixed two-qubit matrix C in basis `00,01,10,11`:

$$
C=\begin{pmatrix}1&0&0&0\\0&1&0&0\\0&0&0&1\\0&0&1&0\end{pmatrix}.
$$

It leaves the first bit unchanged and flips the second when the first is one. Its columns are orthonormal, so C is unitary. Its entries stay fixed across all input cases. Test-state preparation and later analysis gates may depend on a chosen known test vector; they are explicitly outside C.

```python
import torch
import flagquantum as fq
from math import sqrt
from examples.foundations.tensor_spaces import OPTIONS
from examples.foundations.no_cloning import (
    DTYPE, ATOL, COPY, ket, desired, candidate, fidelity, execute)
assert torch.equal(COPY.mH @ COPY,torch.eye(4,dtype=DTYPE))
print('fixed candidate: unitary4x4; blank|0>; qubit0 is the input')
```

```text
fixed candidate: unitary4x4; blank|0>; qubit0 is the input
```

<span id="formula-code-4-7-orthogonal"></span>

### 2. Copying an orthogonal basis is possible

**Formula.** The relevant two columns give

$$
C|00\rangle=|00\rangle,\qquad C|10\rangle=|11\rangle.
$$

**Derivation.** These are exactly the requested outputs for inputs $|0\rangle$ and $|1\rangle$ with blank zero. The other two columns complete a unitary on the entire four-dimensional space. Thus this is a genuine unitary copying operation on the specified orthogonal basis. It is not yet evidence for copying every state in the two-dimensional span as a product of two identical states.

The direct FlagQuantum code prepares each known basis input, keeps q1 in zero, and applies the same matrix on ordered positions `(0,1)`.

```python
basis_outputs = []
for bit in (0,1):
    circuit = fq.Circuit(2,dtype=DTYPE)
    if bit:
        circuit.x(0)
    circuit.unitary(0,1,unitary=COPY)
    result = fq.run(circuit,outputs=[fq.probabilities()],options=OPTIONS)
    assert result.statevector().shape == result.probabilities.shape == (1,4)
    state = result.statevector()[0]
    expected = torch.zeros(4,dtype=DTYPE); expected[3*bit] = 1
    assert torch.allclose(state,expected,rtol=0,atol=ATOL)
    basis_outputs.append(state)
print('basis inputs:', '0 ->00; 1 ->11')
```

```text
basis inputs: 0 ->00; 1 ->11
```

<span id="formula-code-4-7-linearity"></span>

### 3. Derive what the same gate does to a superposition

**Formula.** Let $|\psi\rangle=a|0\rangle+b|1\rangle$, with $|a|^2+|b|^2=1$. By linearity,

$$
C(|\psi\rangle|0\rangle)=a|00\rangle+b|11\rangle.
$$

But the desired product is

$$
|\psi\rangle|\psi\rangle
=a^2|00\rangle+ab|01\rangle+ab|10\rangle+b^2|11\rangle.
$$

**Derivation.** Expand the input as $a|00\rangle+b|10\rangle$ and apply the two known basis images. Expand the desired output by the bilinear tensor-product rule of 4.1. Its coefficients multiply; they do not undergo complex conjugation. Whenever ab is nonzero, the desired product has nonzero `01` and `10` amplitudes, while C's output has zero in both positions. No overall phase can repair that mismatch.

For the plus state, a=b=1/sqrt(2). C produces $(|00\rangle+|11\rangle)/\sqrt2$, whereas two independent plus states have all four amplitudes equal to 1/2. The result is a joint correlated state, not a pair of plus states.

```python
plus = torch.tensor([1,1],dtype=DTYPE)/sqrt(2)
actual_plus, p_plus = execute(plus)
target_plus = desired(plus)
assert torch.allclose(actual_plus,candidate(plus),rtol=0,atol=ATOL)
assert not torch.allclose(actual_plus,target_plus,rtol=0,atol=ATOL)
print('fixed-copy probabilities:', [round(v,6) for v in p_plus.tolist()])
print('desired probabilities:', [round(v,6) for v in target_plus.abs().square().tolist()])
```

```text
fixed-copy probabilities: [0.5, 0.0, 0.0, 0.5]
desired probabilities: [0.25, 0.25, 0.25, 0.25]
```

<span id="formula-code-4-7-complex"></span>

### 4. Keep complex amplitudes in the test

For $a=1/\sqrt2$ and $b=i/\sqrt2$, the two outputs are

$$
C(|\psi\rangle|0\rangle)=\frac{|00\rangle+i|11\rangle}{\sqrt2},\qquad
|\psi\rangle|\psi\rangle=\frac{|00\rangle+i|01\rangle+i|10\rangle-|11\rangle}{2}.
$$

The minus sign in the target is $i^2=-1$. Replacing amplitudes by magnitudes, or conjugating one factor in the tensor product, would lose this information. For normalized joint vectors u and v, use the squared overlap $F=|\langle v|u\rangle|^2$ as a diagnostic: identical rays have F=1, while F<1 certifies that this output is not the desired ray. The inner product uses conjugation in its first argument, even though the tensor-product expansion above does not.

```python
plus_i = torch.tensor([1,1j],dtype=DTYPE)/sqrt(2)
actual_i, _ = execute(plus_i)
target_i = torch.tensor([1,1j,1j,-1],dtype=DTYPE)/2
assert torch.allclose(actual_i,candidate(plus_i),rtol=0,atol=ATOL)
assert torch.allclose(desired(plus_i),target_i,rtol=0,atol=ATOL)
print('plus-i squared overlap:', round(fidelity(actual_i,target_i),6))
```

```text
plus-i squared overlap: 0.25
```

<span id="formula-code-4-7-proof"></span>

### 5. Prove the impossibility for every fixed unitary

**Theorem.** No one unitary W with a fixed normalized blank can perfectly clone all normalized pure states in a space of dimension at least two, even allowing an input-dependent whole-output phase.

**Proof.** Suppose W clones two normalized inputs $|\psi\rangle$ and $|\phi\rangle$. Set $s=\langle\psi|\phi\rangle$. The inner product of their two initial joint states is

$$
\langle\psi|\phi\rangle\langle b|b\rangle=s.
$$

Unitary evolution preserves this inner product. Substituting the two assumed cloned outputs and factorizing the tensor-product inner product yields

$$
s=e^{i(\alpha_\phi-\alpha_\psi)}
\langle\psi|\phi\rangle\langle\psi|\phi\rangle
=e^{i(\alpha_\phi-\alpha_\psi)}s^2.
$$

Taking absolute values removes both arbitrary output phases:

$$
|s|=|s|^2,\qquad |s|(1-|s|)=0.
$$

Therefore $|s|=0$ or $|s|=1$. The first case means the inputs are orthogonal. The second means they are the same physical ray: to verify this directly, when |s|=1 compute

$$
\big\|\,|\phi\rangle-s|\psi\rangle\,\big\|^2=1-|s|^2=0.
$$

Thus $|\phi\rangle=s|\psi\rangle$, with a unit-modulus phase. Distinct nonorthogonal rays have $0<|s|<1$ and cannot both be cloned by W. A space of dimension at least two contains such a pair, for example $|0\rangle$ and $(|0\rangle+|1\rangle)/\sqrt2$. This contradicts the universal contract and proves the theorem.

The argument uses no property of the particular matrix C. Changing its entries cannot avoid inner-product preservation. If output phases had been disallowed, the stronger representative equation would be $s=s^2$; the modulus argument is the appropriate statement about physical pure states.

**Code correspondence.** For zero and plus, the input overlap magnitude is $1/\sqrt2$ while that of their desired copies is 1/2. Their actual outputs under C retain the original overlap. These finite numbers illustrate the contradiction for one pair; the preceding proof quantifies over every candidate W.

```python
zero = torch.tensor([1,0],dtype=DTYPE)
s = abs(torch.vdot(zero,plus).item())
actual_overlap = abs(torch.vdot(basis_outputs[0],actual_plus).item())
perfect_overlap = abs(torch.vdot(desired(zero),desired(plus)).item())
assert abs(actual_overlap-s) < ATOL
assert abs(perfect_overlap-s*s) < ATOL
assert abs(s-perfect_overlap) > .2
print(f'input/actual overlap: {s:.9f}; desired-copy overlap: {perfect_overlap:.9f}')
```

```text
input/actual overlap: 0.707106781; desired-copy overlap: 0.500000000
```

<span id="formula-code-4-7-analyzer"></span>

### 6. Translate the mismatch into a measurement prediction

**Formula.** For a chosen known test vector v, let $R_v$ be the preparation unitary with first column v. Apply $R_v^\dagger$ to each output qubit before computational readout. For a normalized joint state y,

$$
\Pr(00\mid y)=\left|\langle00|
(R_v^\dagger\otimes R_v^\dagger)y\right|^2
=\left|\langle v|\langle v|y\right|^2.
$$

**Derivation.** Since $R_v|0\rangle=|v\rangle$, taking adjoints gives $\langle0|R_v^\dagger=\langle v|$. Apply this identity to both factors. Thus the zero-zero probability equals the squared overlap with the desired product. On two true plus states, the plus-basis analyzer returns `00` with probability one. On C's plus-input output it returns `00` with probability one-half. This is a basis-specific operational distinction, not just a numerical amplitude comparison.

The helper's `known-reference` branch prepares each qubit from the supplied classical vector v. It deliberately uses state-dependent preparation on q1, rather than the fixed C. The two paths then use the same known analyzer. That reference is allowed precisely because the test designer knows v; it is not an implementation of a universal cloner for unknown input.

```python
_, observed = execute(plus,analyze=True)
_, ideal_observed = execute(plus,'known-reference',analyze=True)
assert abs(observed[0].item()-fidelity(actual_plus,target_plus)) < ATOL
assert abs(ideal_observed[0].item()-1) < ATOL
print('chosen plus analyzer P00:', round(observed[0].item(),6))
print('known-reference P00:', round(ideal_observed[0].item(),6))
```

```text
chosen plus analyzer P00: 0.5
known-reference P00: 1.0
```

These are exact ideal simulator probabilities. No finite-shot counts or physical device measurements are reported, and no analyzer for an arbitrary unknown state is assumed to be available.

<span id="formula-code-4-7-known-state"></span>

### 7. Explain what the theorem allows

An input from the declared orthogonal zero/one basis can be copied by C, as actually checked. A known amplitude description can be used to prepare two independent states. Both statements coexist with no-cloning: neither satisfies the universal contract on one arbitrary unknown input.

For example, for known v=(0.6,0.8i), two separately constructed preparation gates produce the product with amplitudes `(0.36,0.48i,0.48i,-0.64)`. That ability does not turn a fixed copying gate into a cloner. Merely matching one measurement distribution also does not establish equality of pure states: different relative phases can agree in the computational basis, as Chapter 3 demonstrated.

```python
known = torch.tensor([.6,.8j],dtype=DTYPE)
reference, _ = execute(known,'known-reference')
explicit = torch.tensor([.36,.48j,.48j,-.64],dtype=DTYPE)
assert torch.allclose(reference,explicit,rtol=0,atol=ATOL)
print('known complex product: all four amplitudes verified')
```

```text
known complex product: all four amplitudes verified
```

The present proof has the fixed-unitary, fixed-blank, pure-state scope stated in unit 1. It does not derive optimal approximate cloning, heralded probabilistic protocols, general quantum-channel impossibility results or mixed-state no-broadcasting. Those require additional definitions and results. No-cloning also does not say that all state information is inaccessible or that all classical data cannot be copied.

<span id="formula-code-4-7-validation"></span>

### 8. Keep numerical contracts and theorem claims separate

The example accepts a finite normalized CPU complex128 two-coordinate state. A batch axis, lower precision, nonfinite values and automatic normalization are outside its contract. The mode must explicitly select the fixed gate attempt or the known-state reference. Unknown modes must not silently trigger a state-dependent “repair.”

```python
invalid = [lambda: ket(torch.ones(2,dtype=DTYPE)),
           lambda: ket(zero[None,:]),
           lambda: ket(zero.to(torch.complex64)),
           lambda: execute(zero,'repair')]
rejected = 0
for action in invalid:
    try:
        action()
    except ValueError:
        rejected += 1
assert rejected == 4
print('unnormalized, batched, wrong precision and ambiguous mode:', rejected, 'rejected')
```

```text
unnormalized, batched, wrong precision and ambiguous mode: 4 rejected
```

Run the full example and actual-body checker:

```bash
python examples/foundations/no_cloning.py
python scripts/check_no_cloning_prose.py
```

The full program executes **24 circuits**: six inputs (`zero,one,plus,minus,plus-i,complex`), each on four paths—fixed C, known-state product reference, analyzed C output, and analyzed known-state reference. Hand four-amplitude expansions check both unanalysed states. Independent scalar sums check the analyzer's complex output. Thirty-five additional classical amplitude fixtures check the bilinear expansion and fixed-C formula, and six invalid contracts are rejected before dependent quantum execution. The eight body fragments execute seven circuits in a separate invocation. A new complex-state transfer is recorded separately.

Expected output of the complete program:

```text
One fixed unitary, blank|0>; known-reference preparation is state-specific, not a cloner.
zero: fixed-copy fidelity=1.000000; analyzer P00=1.000000; known-reference P00=1.000000.
one: fixed-copy fidelity=1.000000; analyzer P00=1.000000; known-reference P00=1.000000.
plus: fixed-copy fidelity=0.500000; analyzer P00=0.500000; known-reference P00=1.000000.
minus: fixed-copy fidelity=0.000000; analyzer P00=0.000000; known-reference P00=1.000000.
plus-i: fixed-copy fidelity=0.250000; analyzer P00=0.250000; known-reference P00=1.000000.
complex: fixed-copy fidelity=0.308800; analyzer P00=0.308800; known-reference P00=1.000000.
Nonorthogonal pair: input overlap=0.707106781; perfect-copy overlap=0.500000000; incompatible.
35 classical amplitude fixtures and6invalid contracts checked; identical rays allowed, universal cloning excluded.
24 actual CPU complex128 circuits; atol=1e-12,rtol=0; no phase alignment, shots or hardware.
```

The zero fidelity for the minus-state attempt is useful: the fixed gate does not even approximate every superposition equally. It is not a bound on the best approximate cloner. Passing these fixtures would never establish universal cloning, and their failure alone would not rule out all possible gates; the inner-product theorem supplies that conclusion.

### Understanding checks and transfer exercises

**4.7-A — New complex input.** Let $a=\sqrt{4/5}$ and $b=e^{i\pi/3}\sqrt{1/5}$. Write the four amplitudes of C's output and of the desired product. Which missing amplitudes already certify failure up to global phase?

**4.7-B — Change the blank.** Could choosing a fixed normalized blank other than zero evade the proof? Identify exactly where the blank enters the inner-product calculation. What changes if a state-dependent blank already contains a copy of the input?

**4.7-C — Identical rays.** Take $|\phi\rangle=i|\psi\rangle$. Explain why the modulus argument permits the pair even though a phase-free representative equation $s=s^2$ would fail. State the difference between vector equality and physical-state cloning.

**4.7-D — Interpret a claim.** A program achieves fidelity one for zero and one, and prepares two plus states using the known plus amplitudes. Does this refute no-cloning? What would the actual universal contract require, and why can finite test success not establish it?

<details markdown="1">
<summary>Answers and reasoning</summary>

**A.** C gives `(a,0,0,b)`. The desired product is $(4/5,(2/5)e^{i\pi/3},(2/5)e^{i\pi/3},(1/5)e^{2i\pi/3})$. The two middle amplitudes are nonzero in the target and zero in the actual output, so a phase cannot reconcile them. The separate author transfer executes this new complex input, checks all four amplitudes/probabilities against the explicit reference, and verifies squared overlap less than one.

**B.** No. For any fixed normalized blank, its contribution is $\langle b|b\rangle=1$ for both inputs. The contradiction therefore remains. If the blank depends on the unknown input, the universal fixed-blank assumption is broken; supplying it as a copy has already supplied the resource the task sought to create.

**C.** Here s=i and |s|=1; the two inputs describe one ray. A linear operation acts on a phased representative once, while the formal tensor square carries the phase twice. The allowed input-dependent output phase reconciles those representative choices. Physical cloning asks for the desired product ray, so the proof must use the modulus condition rather than excluding two representatives of the same state.

**D.** No. The first result concerns a permitted orthogonal basis. The second redesigns the preparation using a classical state description. Universal cloning would require the same operation and same blank for every unknown input, preserving the desired product ray. Finite tests can find counterexamples to a proposed gate; only a general argument establishes impossibility for every gate or proves a property on the whole stated domain.

</details>

### Sources, depth and next step

Depth **F**: the two-input inner-product proof includes output phase freedom, the identical-ray and orthogonal boundaries, and a contradiction from an explicit nonorthogonal pair. The assigned background locator is Nielsen and Chuang, 10th Anniversary Edition, §1.3.5. No fresh inspection of the user-local PDF is claimed. A historical primary reference is W. K. Wootters and W. H. Zurek, [“A single quantum cannot be cloned,” Nature 299, 802–803 (1982)](https://doi.org/10.1038/299802a0); its bibliographic record was checked, without claiming a new full-paper review. The derivation and teaching examples above are original.

The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/4.7.json) keeps author execution separate from pending independent mathematical, implementation and reader review. This remains a working draft. Continue with the working draft [4.8 Cross-framework convention translation](#sec-composite-systems-tensor-products-and-qubit-ordering-7).

<span id="sec-composite-systems-tensor-products-and-qubit-ordering-7"></span>

## 4.8 Cross-framework convention translation

Two simulators can return different arrays for the same labeled physical state. Agreement requires a declared correspondence between qubits, basis indices, local matrix arguments and measured classical bits. Reversing every array or string is not a general translation strategy.

The prerequisites are [4.2](#sec-composite-systems-tensor-products-and-qubit-ordering-2), [4.5](#sec-composite-systems-tensor-products-and-qubit-ordering-5) and [4.6](#sec-composite-systems-tensor-products-and-qubit-ordering-6). We derive a general basis-permutation contract and then execute it between **FlagQuantum 0.3.1** and **Qiskit 2.5.2**, matching qubit q in one circuit with qubit q in the other. Both use ideal CPU simulation here. No physical SWAP or hardware mapping is implied by a coordinate conversion.

Install the additional pinned dependency in a fresh example environment:

```bash
python -m pip install -r requirements-interop.txt
```

That file includes the existing pinned example requirements and `qiskit==2.5.2`. No cloud account, credentials, Aer package or quantum device is required. The eight cumulative formula–derivation–code–result fragments run from the repository root. The complete companion is [convention_translation.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/convention_translation.py). Numerical coordinate comparisons use CPU complex128, absolute tolerance $10^{-12}$ and relative tolerance zero. Sampling checks have a separately declared frequency tolerance.

<span id="formula-code-4-8-index-contract"></span>

### 1. Fix labels before comparing basis indices

**Formula.** Let b=(b0,…,b(n−1)) assign bit bq to the same physical qubit q in both frameworks. The tested conventions are

$$
J_F(b)=\sum_{q=0}^{n-1}b_q2^{n-1-q},\qquad
J_Q(b)=\sum_{q=0}^{n-1}b_q2^q.
$$

**Derivation.** In the FlagQuantum convention established by the preceding executions, q0 is the most significant bit. Qiskit's documented integer convention makes q0 least significant. Its displayed computational ket string runs from q(n−1) to q0. Therefore one physical tuple has two coordinate indices. For n=3, tuple `100` means q0=1, q1=q2=0, so its indices are 4 and 1. Qiskit's string label for that tuple is `001`. A diagram's vertical order does not change this equation. The [official bit-ordering guide](https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering) separates integer, string and diagram conventions; the versions above are actually tested here.

```python
import torch
import flagquantum as fq
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator
from examples.foundations.tensor_spaces import OPTIONS
from examples.foundations.convention_translation import (
    DTYPE, ATOL, basis_map, reversal, q_local, q_circuit, pair,
    complex_gate, factors_complex, dense_embedding,
    sample, sample_partial, canonical_counts, decode_key, slot_map, marginal)
fq_basis = fq.Circuit(3,dtype=DTYPE); fq_basis.x(0)
fq_result = fq.run(fq_basis,outputs=[fq.probabilities()],options=OPTIONS)
assert fq_result.statevector().shape == (1,8)
f = fq_result.statevector()[0]
q_basis = QuantumCircuit(3); q_basis.x(0)
z = torch.from_numpy(Statevector.from_instruction(q_basis).data.copy())
assert int(f.abs().argmax()) == 4 and int(z.abs().argmax()) == 1
print('same physical tuple(q0,q1,q2)=100: FQ index4; Qiskit index1, displayed001')
```

```text
same physical tuple(q0,q1,q2)=100: FQ index4; Qiskit index1, displayed001
```

<span id="formula-code-4-8-permutation"></span>

### 2. Construct the coordinate-conversion matrix

**Formula.** Declare source and target basis orders, each most significant first. For every physical tuple b, define

$$
B_{J_Q(b),J_F(b)}=1,
$$

with all other entries zero. More generally, if $g=J_T\circ J_S^{-1}$ maps a source index to its target index, set $B_{k,j}=\delta_{k,g(j)}$. Then

$$
z=Bx,\qquad x=B^\dagger z,\qquad B^\dagger B=BB^\dagger=I.
$$

**Derivation.** Both index maps are bijections by 4.2, so g is a bijection. Every column and every row of B contains exactly one unit entry; its columns are orthonormal. If source basis vector $e_j$ and target basis vector $f_{g(j)}$ denote the same physical basis state, expanding the same vector in both bases gives $z_{g(j)}=x_j$. That is z=Bx. Here B is defined as a **coordinate converter**; it is not the active gate P from 4.5. The passive rule there is consistent: new basis columns are related by $P=B^\dagger$.

For the particular FQ/Qiskit order pair, B reverses binary digit positions and happens to be its own inverse. It does not reverse the amplitude array: a full array reversal maps index 0 to 7, while a bit-position reversal leaves index 0 fixed. The helper also accepts other declared label orders; do not infer self-inversion for a general converter.

```python
source = ('q0','q1','q2'); target = ('q2','q1','q0')
B = basis_map(source,target)
assert torch.equal(B.mH @ B,torch.eye(8,dtype=DTYPE))
assert torch.allclose(z,B @ f,rtol=0,atol=ATOL)
assert torch.allclose(f,B.mH @ z,rtol=0,atol=ATOL)
cycle = basis_map(source,('q1','q2','q0'))
assert not torch.equal(cycle,cycle.mH)
print('bit-position reversal fixes index0:', int(B[:,0].abs().argmax()))
print('a general declared basis converter need not equal its inverse')
```

```text
bit-position reversal fixes index0: 0
a general declared basis converter need not equal its inverse
```

<span id="formula-code-4-8-local-gate"></span>

### 3. Translate a local matrix independently of the global vector order

**Formula.** In FQ, support $S=(s_0,\ldots,s_{k-1})$ uses s0 as the most significant local bit. For Qiskit's generic `unitary(matrix,qargs)` path tested here, `qargs[0]` supplies the least significant local bit. Let $R_k$ reverse those k binary positions. Keeping the same qarg list requires

$$
U_Q=R_kU_FR_k^\dagger.
$$

**Derivation.** Let a be the local physical bit tuple in S order. The FQ local index is $J_F(a)$ and the Qiskit local index is $J_Q(a)$. The local matrix entry mapping is therefore $(U_Q)_{J_Q(a),J_Q(d)}=(U_F)_{J_F(a),J_F(d)}$, exactly the conjugation above. Alternatively, keep the numerical matrix $U_F$ but supply `list(reversed(S))` to this generic Qiskit operation. That reversal makes the first *physical* bit in S the most significant matrix bit again. These two alternatives are checked against each other. This is not an instruction to reverse arguments of every named gate API; semantic control/target arguments must retain their declared meaning.

Take the asymmetric complex U from 4.4 on nonadjacent support `(2,0)` and the complex product preparation from that section. The same raw U on the same numeric Qiskit qarg list is a deliberate wrong translation. Complex, order-sensitive amplitudes expose the mistake where identity or symmetric gates might not.

```python
S = (2,0); U = complex_gate()
f, z, q_complex = pair(factors_complex(),U,S)
q_alternative = q_circuit(factors_complex(),U,S,reverse_arguments=True)
z_alternative = torch.from_numpy(Statevector.from_instruction(q_alternative).data.copy())
assert torch.allclose(z_alternative,z,rtol=0,atol=ATOL)
q_wrong = q_circuit(factors_complex())
q_wrong.unitary(U.numpy(),list(S))
z_wrong = torch.from_numpy(Statevector.from_instruction(q_wrong).data.copy())
assert not torch.allclose(z_wrong,z,rtol=0,atol=ATOL)
print('converted local matrix == reversed generic qargs: full complex vector checked')
print('same raw local matrix with same qargs: mismatch detected')
```

```text
converted local matrix == reversed generic qargs: full complex vector checked
same raw local matrix with same qargs: mismatch detected
```

The helper's actual FQ call is `circuit.unitary(*S,unitary=U)`. The paired Qiskit call is `qc.unitary(q_local(U,len(S)).numpy(),list(S))`. Independent scalar amplitude sums check the FQ result before the Qiskit comparison. This example concerns these released interfaces; another library's local matrix contract must be inspected rather than assumed.

<span id="formula-code-4-8-observables"></span>

### 4. Convert operators and outcome projectors with the state

**Formula.** If y=Ax in source coordinates and z=Bx, the target operator is

$$
A_Q=BA_FB^\dagger.
$$

For an outcome projector $M_F$, let $M_Q=BM_FB^\dagger$. Then

$$
z^\dagger M_Qz=x^\dagger M_Fx.
$$

For the complete computational distribution, $p_Q=Bp_F$ as well, because B is a zero-one permutation matrix.

**Derivation.** Convert the output: $By=BA_Fx=BA_FB^\dagger z$. This establishes the operator rule. Substitute z=Bx into the quadratic form and cancel $B^\dagger B$ on both sides of $M_F$ to prove event-probability invariance. No numerical phase fitting is involved. For a computational projector selecting one physical tuple, B moves its nonzero diagonal entry to the coordinate of that same tuple in the target basis. Summing such projectors proves the same statement for a set of outcomes.

Check a Qiskit full operator, not only one output state, and then check the event “physical q0 is one.” Both matrices must refer to the same labeled event.

```python
q_operator = QuantumCircuit(3)
q_operator.unitary(q_local(U,2).numpy(),list(S))
OQ = torch.from_numpy(Operator(q_operator).data.copy())
OF = dense_embedding(U,3,S)
assert torch.allclose(OQ,B @ OF @ B.mH,rtol=0,atol=ATOL)
MF = torch.diag(torch.tensor([0,0,0,0,1,1,1,1],dtype=DTYPE))
MQ = B @ MF @ B.mH
pF = f.abs().square(); pQ = z.abs().square()
assert torch.allclose(pQ,B.real @ pF,rtol=0,atol=ATOL)
eventF = torch.vdot(f,MF @ f).real.item()
eventQ = torch.vdot(z,MQ @ z).real.item()
assert abs(eventF-eventQ) < ATOL
print('operator conjugation checked in all64entries')
print(f'physical q0=1 probability: FQ={eventF:.9f}; Qiskit={eventQ:.9f}')
```

```text
operator conjugation checked in all64entries
physical q0=1 probability: FQ=0.500000000; Qiskit=0.500000000
```

Matching only computational probabilities would not verify all phases or the operator on untested vectors. Here the explicit matrix identity and full complex comparisons test those translations. An unexplained global phase is recorded as a discrepancy under this exact-coordinate contract; it is not silently aligned away. Raw ideal circuits here have zero declared circuit-level global phase.

<span id="formula-code-4-8-classical-slots"></span>

### 5. Distinguish quantum labels from measured classical slots

**Formula.** For a full final readout, let $\mu(q)$ be the classical slot receiving physical bit bq. Define classical bits by

$$
c_{\mu(q)}=b_q.
$$

For the single classical register used here, the returned binary key is displayed as $c_{n-1}\cdots c_0$. Thus

$$
b_q=c_{\mu(q)}
$$

is the decoding rule; it depends on the measurement map, not only on qubit order.

**Derivation.** Final computational measurement associates an outcome bit with each selected qubit. The circuit's explicit `measure(q,c)` instruction chooses where that bit is stored. The display then chooses how those classical slots are written. Follow these two maps separately. With identity $\mu=(0,1,2)$, physical tuple `100` displays as `001`. With $\mu=(2,0,1)$, it displays as `100`, although the quantum state is unchanged.

These are actual seeded Qiskit `StatevectorSampler` runs with 64 shots each. The results are deterministic because the input is a computational basis state, not because the seed is being treated as an exact-probability guarantee. The sampler's `data.c` identifies the explicitly named single classical register returned by this circuit construction.

```python
q_readout = QuantumCircuit(3); q_readout.x(0)
raw_identity, canonical_identity = sample(q_readout,(0,1,2),64)
raw_changed, canonical_changed = sample(q_readout,(2,0,1),64)
assert raw_identity == {'001':64} and raw_changed == {'100':64}
print('identity measurement map raw:', raw_identity)
print('changed measurement map raw:', raw_changed)
```

```text
identity measurement map raw: {'001': 64}
changed measurement map raw: {'100': 64}
```

Qiskit result containers can differ between primitive implementations. This example uses the installed local `StatevectorSampler` and validates its returned strings. Do not assume every cloud service, executor, memory dump or framework shares that display contract. The [sampler API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.StatevectorSampler) documents per-classical-register results; the actual pinned runtime is the execution authority here.

<span id="formula-code-4-8-counts"></span>

### 6. Decode counts using declared metadata and conserve totals

**Formula.** Let d(k) decode a returned key k into the chosen canonical physical-bit tuple. The translated counts are

$$
N_F(b)=\sum_{k:\,d(k)=b}N_Q(k),\qquad
\sum_bN_F(b)=\sum_kN_Q(k).
$$

**Derivation.** Assign each returned key to exactly one decoded event and add its nonnegative integer count. The decoded event classes partition the input keys, so regrouping preserves the total. Full bijective readout simply renames keys. Coarse-graining onto fewer measured labels can merge events. Neither operation changes how many shots were recorded.

The helper requires unique measured labels implicitly declared by the caller's ordered list, a bijective slot map for that list, exact binary widths and integer counts. For this full readout the list is `(q0,q1,q2)`. A grouped fixture illustrates an additional metadata requirement: key `10 0` means descending slot blocks `(c2,c1)` and `(c0)` only when those group widths and that slot order have been explicitly declared. It is not an actual sampled key in the preceding runs, and the helper does not discover a multi-register schema from spaces.

```python
assert canonical_identity == canonical_changed == {'100':64}
assert sum(canonical_changed.values()) == sum(raw_changed.values()) == 64
grouped = canonical_counts({'10 0':7},(0,1,2),groups=(2,1))
assert grouped == {'001':7}
print('both full-readout results in(q0,q1,q2) order:', canonical_changed)
print('constructed grouped fixture with explicit slot blocks:', grouped)
```

```text
both full-readout results in(q0,q1,q2) order: {'100': 64}
constructed grouped fixture with explicit slot blocks: {'001': 7}
```

For other result containers, obtain classical register order, slot numbering, encoding and measurement assignments from that result's metadata first. Hexadecimal keys, missing padding and undeclared group layouts are rejected by this minimal adapter. Reset or overwrite histories need an additional explicit circuit/result contract; the generated readout circuits here contain neither, and counts alone cannot diagnose such histories.

<span id="formula-code-4-8-partial"></span>

### 7. Treat partial measurement as a marginal, not an invertible reshape

**Formula.** For an ordered measured subset $S=(s_0,\ldots,s_{k-1})$, define canonical output bits $a=(b_{s_0},\ldots,b_{s_{k-1}})$. Its exact distribution is

$$
p_S(a)=\sum_{b:\,b_S=a}p_F(b).
$$

**Derivation.** All full-register outcomes with the selected bits a correspond to the same measured event. They differ only on unmeasured positions, so their mutually exclusive probabilities add. Grouping by the binary index of a gives a length-$2^k$ vector, with s0 most significant. The grouping loses information when k<n: one partial count string cannot recover the unmeasured bits, the full joint distribution or any relative phases.

Check both full and partial readout on the complex circuit from unit 3. For the partial circuit, measure physical `(q2,q0)` into classical `(c0,c1)`. Its canonical list is explicitly `(q2,q0)`; the raw displayed string is `(c1,c0)`. The returned helper dictionary refers only to these two measured labels, not to a reconstructed three-qubit outcome.

```python
raw_complex, counts_complex = sample(q_complex,(2,0,1),1024)
empirical = torch.tensor([counts_complex.get(format(j,'03b'),0)/1024
                          for j in range(8)],dtype=torch.float64)
assert (empirical-pF).abs().max() < .1
raw_partial, counts_partial = sample_partial(q_complex,(2,0),1024)
exact_partial = marginal(pF,3,(2,0))
partial_empirical = torch.tensor([counts_partial.get(format(j,'02b'),0)/1024
                                 for j in range(4)],dtype=torch.float64)
assert (partial_empirical-exact_partial).abs().max() < .1
assert sum(counts_complex.values()) == sum(counts_partial.values()) == 1024
print('exact ordered(q2,q0) marginal:', [round(v,9) for v in exact_partial.tolist()])
print('full and partial sampled frequencies: max absolute error below0.1;1024shots each')
```

```text
exact ordered(q2,q0) marginal: [0.466506351, 0.466506351, 0.033493649, 0.033493649]
full and partial sampled frequencies: max absolute error below0.1;1024shots each
```

The 0.1 bound is a coarse finite-sampling check on these seeded fixtures, separate from the $10^{-12}$ coordinate tolerance. Repeated execution with the same seed is not fresh independent experimental evidence. Exact probabilities are checked through statevectors; counts are actual finite-shot local-simulator outputs. No hardware noise, measurement calibration or quantum-state reconstruction is claimed.

<span id="formula-code-4-8-rejections"></span>

### 8. Reject missing contracts instead of repairing conventions silently

```python
invalid = [lambda: basis_map(('a','a'),('a','b')),
           lambda: basis_map(('a','b'),('a','c')),
           lambda: slot_map((0,0,2)),
           lambda: decode_key('1',(0,1,2)),
           lambda: decode_key('10 0',(0,1,2)),
           lambda: canonical_counts({'001':-1},(0,1,2))]
rejected = 0
for action in invalid:
    try:
        action()
    except ValueError:
        rejected += 1
assert rejected == 6
print('duplicate/missing labels, duplicate slots, short/undeclared grouped key and negative count:', rejected, 'rejected')
```

```text
duplicate/missing labels, duplicate slots, short/undeclared grouped key and negative count: 6 rejected
```

A complete translation record includes framework versions, logical-qubit correspondence, full and local basis orders, matrix phase conventions, measured-label order, quantum-to-classical assignments, display encoding, register groups and shot count. Transpiled hardware circuits require an additional logical-to-physical layout map; none is used in these ideal raw-circuit examples. This section implements a validated narrow adapter, not an arbitrary circuit importer or universal framework compatibility layer.

Run the complete verification and actual-body checker:

```bash
python examples/foundations/convention_translation.py
python scripts/check_convention_translation_prose.py
```

The complete program executes 82 FQ statevector circuits paired with Qiskit circuits: 30 basis preparations through four qubits, 48 asymmetric-gate basis/support cases on all three-qubit ordered pairs, and four complex-state pairs including full support. Three alternative reversed-qarg executions and one deliberately wrong raw-matrix execution give 86 Qiskit statevector runs in total. Three Qiskit `Operator` constructions check full matrices. Four sampler submissions use 2,176 shots: two deterministic 64-shot readouts plus two 1,024-shot complex full/partial readouts. Six classical basis-order roundtrips, a grouped fixture and ten malformed-schema cases are also checked. FQ probabilities and Qiskit samples are separate evidence types.

Expected output of the complete program:

```text
FQ0.3.1:q0MSB; Qiskit2.5.2:q0LSB; labels and physical qubits matched explicitly.
30 basis-preparation pairs through4qubits: every complex coordinate and probability checked.
48 ordered-support basis pairs: asymmetric complex local gate on all3qubit ordered pairs.
4complex pairs,3reversed-argument alternatives,3operator matrices; raw-matrix negative witness rejected.
Actual64shot basis readout: map(0,1,2) raw001; map(2,0,1) raw100; both canonical100.
1024shot complex readout: counts conserved, all frequencies within0.1of exact probabilities; actual1024shot partial readout matches ordered marginal.
6basis-order roundtrips, explicit grouped fixture and10invalid schemas checked.
82FQ circuits;86Qiskit statevector circuits;3Operator constructions;4Sampler pubs,2176shots; ideal CPU only.
```

The eight body fragments separately execute two FQ circuits, four Qiskit statevector circuits, one Qiskit Operator construction and four sampler submissions using 2,176 shots. The body checker reruns the complete companion as a separate invocation. A new four-qubit nonadjacent transfer is recorded below. These finite tests validate the stated translations and examples; the general preservation identities follow from the proofs, and other frameworks require their own declared and verified maps.

### Understanding checks and transfer exercises

**4.8-A — New nonadjacent support.** In a four-qubit register, apply the asymmetric complex U to ordered support `(3,1)` on physical input `1011`. State the input's FQ and Qiskit global indices, the selected local input indices in the two conventions, and the local matrix Qiskit needs if the qarg list is unchanged.

**4.8-B — Counts are not ket labels.** Decode raw `10 0` with descending slot groups `(2,1)` and map $\mu=(2,0,1)$. Which physical tuple does it denote? Why does the answer differ from the identity map in unit 6?

**4.8-C — Lost bits.** If only `(q2,q0)` is measured and the canonical outcome is `10`, list all consistent three-qubit physical tuples. Can those counts determine the relative phase between them?

**4.8-D — Diagnose a supposed fix.** A collaborator reverses the amplitude array and every gate argument list, then accepts a result because probabilities agree. Identify three distinct contracts that this procedure fails to establish.

<details markdown="1">
<summary>Answers and reasoning</summary>

**A.** Physical tuple `1011` has FQ index 11 and Qiskit index 13 (`1101` in Qiskit's displayed order). Selected local bits `(b3,b1)=(1,0)` have FQ local index 2 and Qiskit local index 1. Use $R_2UR_2^\dagger$ with qargs `[3,1]`, or U with reversed generic qargs `[1,3]`. The separate author transfer actually runs both frameworks for this nonadjacent four-qubit case and compares every complex amplitude and probability after conversion, using scalar gate action as an independent reference.

**B.** Flattened descending slots are `100`, so c2=1,c1=0,c0=0. The map assigns b0=c2=1,b1=c0=0,b2=c1=0: physical tuple `100`. Under the identity map, the same slot contents denote physical `001`. The string alone does not identify the quantum event.

**C.** b2=1 and b0=0, while b1 is unmeasured. The consistent physical tuples `(q0,q1,q2)` are `001` and `011`. Partial counts add their probabilities and reveal neither their separate probabilities nor their relative phase.

**D.** Full array reversal complements all binary bits rather than reversing their significance. Generic local-matrix order and named gate semantics require separate rules; changing every argument list can change control/target meaning. Finally, probability agreement does not establish complex amplitudes, operator phases or correctly labeled measurement events. Require the physical-label map, correct basis permutations and matrix conjugations, and an explicit classical-readout schema, then compare phase-sensitive examples.

</details>

### Sources, depth and next step

Depth **F**: the basis bijection, coordinate converter, operator/projector conjugation, probability preservation, local matrix conversion, count regrouping and ordered marginal are derived explicitly. Assigned background remains Nielsen and Chuang, 10th Anniversary Edition, §2.1.7; the editorial acceptance protocol remains separate from execution evidence. No fresh inspection of the user-local PDF is claimed. The IBM documentation links above support the framework contracts; actual pinned interfaces, runtime versions and source inspection limits are recorded in the [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/4.8.json).

All eight Chapter 4 sections now have author-verified working drafts, not independent acceptance. Mathematical, implementation and reader review remain pending. Continue with the working draft [5.1 Circuit composition, inversion, and call order](ch-gates-reversible-computation-and-circuit-synthesis.md#sec-gates-reversible-computation-and-circuit-synthesis-1).
