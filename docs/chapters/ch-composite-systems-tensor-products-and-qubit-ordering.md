# 4. Composite Systems, Tensor Products, and Qubit Ordering

**Working draft: section 4.1 · Writing Baseline 1.0 · October 21, 2026.** Author execution is recorded separately from independent mathematical, implementation and reader review, which remain pending. This is not an accepted chapter. Examples use released FlagQuantum 0.3.1 and PyTorch 2.13.0 on CPU with complex128 statevectors.

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

Depth **F**: construct the finite product space, prove product-basis orthonormality and dimension, and derive product amplitudes, inner products and normalization. This section does not establish a general bit-string convention, local-operator tensor formulas, permutations or entanglement classification. The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/4.1.json) separates author execution from pending independent reviews. Next: [4.2 Registers, labels, and basis indices](../section-plans/01-foundations.md#sec-composite-systems-tensor-products-and-qubit-ordering-2).
