# 2. Complex Vectors, Operators, and Numerical Reasoning

**Working draft: sections 2.1–2.2 · Writing Baseline 1.0 · October 21, 2026.** Sections 2.3–2.8 remain planned. Author execution checks are recorded separately from independent mathematical, implementation and reader review, which remain pending. This is not an accepted chapter. Section 2.1 uses Python 3.12 and its standard library; 2.2 adds PyTorch 2.13.0 CPU complex128 tensor checks.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-1"></span>

## 2.1 Complex scalars, vectors, and conjugation

The interference preview in Chapter 1 used pairs of real numbers. To build the general mathematical language, we now allow each coordinate to have a real part and an imaginary part. Before interpreting any coordinate as a quantum amplitude, we need to know how to add it, multiply it and compute its size without losing a sign.

This section needs real-number arithmetic, square roots and the distributive rule for multiplication over addition. It has no prior numbered-section prerequisite. Python lists will store finite coordinate vectors; their entries need not yet describe a quantum state. By the end, you should be able to derive the conjugation identities and detect a missing conjugate in a numerical calculation.

### A complex number is a pair with a multiplication rule

Write a complex number as $z=a+ib$, where $a$ and $b$ are real numbers and $i$ satisfies $i^2=-1$. Its real part is $a$ and its imaginary part is $b$: the imaginary part of $2-3i$ is $-3$, not $-3i$. Two complex numbers are equal exactly when their respective real and imaginary parts agree. Real numbers are included by setting $b=0$.

For a second complex number $w=c+id$, addition combines the two parts:

$$
z+w=(a+c)+i(b+d).
$$

Multiplication follows by distributing each term and using $i^2=-1$:

$$
\begin{aligned}
zw&=(a+ib)(c+id)\\
  &=ac+iad+ibc+i^2bd\\
  &=(ac-bd)+i(ad+bc).
\end{aligned}
$$

For example, take $z=2-3i$ and $w=-1+4i$. Their sum is $1+i$. Their product has real part $2(-1)-(-3)4=10$ and imaginary part $2(4)+(-3)(-1)=11$, so $zw=10+11i$. The imaginary coordinates contribute to both parts of a product. Multiplying real parts alone loses that information.

Python writes the imaginary unit as `1j`, so these numbers are `2-3j` and `-1+4j`. Bare `j` is a variable name, not the imaginary unit. We will keep $i$ in mathematics and `j` inside Python literals.

### Conjugation: change the imaginary sign, not every sign

The **complex conjugate** of $z=a+ib$ is defined by $z^*=a-ib$. The star denotes this operation, not multiplication. Thus $(2-3i)^*=2+3i$. A second conjugation returns the original number:

$$
(z^*)^*=(a-ib)^*=a+ib=z.
$$

Here are two identities we will use repeatedly. They hold for every pair of complex numbers, not just our numerical example:

$$
(z+w)^*=z^*+w^*,\qquad (zw)^*=z^*w^*.
$$

To prove the sum identity, use the real and imaginary parts of the sum:

$$
(z+w)^*=(a+c)-i(b+d)=(a-ib)+(c-id).
$$

For the product, conjugating the product already derived gives

$$
(zw)^*=(ac-bd)-i(ad+bc).
$$

Multiplying the two conjugates independently gives

$$
\begin{aligned}
z^*w^*&=(a-ib)(c-id)\\
       &=ac-iad-ibc+i^2bd\\
       &=(ac-bd)-i(ad+bc).
\end{aligned}
$$

The real and imaginary parts agree, which proves the identity. A real scalar $r$ obeys $r^*=r$, but a general complex scalar does not. In particular, $i^*=-i$. This distinction will matter when coefficients multiply whole vectors.

**2.1-A — Predict before running.** What is $(i(1+i))^*$? Compare it with $i(1+i)^*$. Which operation causes their difference?

### Modulus: a nonnegative size

Define the **modulus** of $z=a+ib$ by

$$
\lvert z\rvert=\sqrt{a^2+b^2}.
$$

The square root means the nonnegative real square root. On the real line this becomes the ordinary absolute value. Multiplying by the conjugate recovers the squared modulus:

$$
\begin{aligned}
z^*z&=(a-ib)(a+ib)\\
    &=a^2+iab-iab-i^2b^2\\
    &=a^2+b^2=\lvert z\rvert^2.
\end{aligned}
$$

The two imaginary cross terms cancel; the remaining $b^2$ has a plus sign. Consequently $z^*z$ is real and nonnegative, and it is zero exactly when both $a$ and $b$ are zero. Conjugating $z$ changes $b$ to $-b$, whose square is still $b^2$, so $\lvert z^*\rvert=\lvert z\rvert$.

The size of a product also has a useful rule. Using the proved conjugation identity and the fact that complex scalar multiplication commutes,

$$
\begin{aligned}
\lvert zw\rvert^2
  &=(zw)^*(zw)\\
  &=z^*w^*zw\\
  &=(z^*z)(w^*w)\\
  &=\lvert z\rvert^2\lvert w\rvert^2.
\end{aligned}
$$

Both moduli are nonnegative, so taking nonnegative square roots gives $\lvert zw\rvert=\lvert z\rvert\lvert w\rvert$. No division by either number was used; the result includes zero. The rearrangement here concerns scalars. It does not authorize reordering matrix products in later sections.

For a nonzero $z$, the same identity supplies division:

$$
z^{-1}=\frac{z^*}{\lvert z\rvert^2},\qquad
z\frac{z^*}{\lvert z\rvert^2}=1.
$$

The denominator is positive because $z\ne0$. Thus $w/z$ means $wz^{-1}$. There is no corresponding inverse for zero.

The modulus is not additive. For our example, $\lvert z\rvert^2=13$, $\lvert w\rvert^2=17$, but $\lvert z+w\rvert^2=\lvert1+i\rvert^2=2$, not 30. To see the missing terms rather than memorize a warning, expand

$$
\begin{aligned}
\lvert z+w\rvert^2
 &= (z^*+w^*)(z+w)\\
 &= \lvert z\rvert^2+\lvert w\rvert^2+z^*w+w^*z.
\end{aligned}
$$

Here $z^*w=-14+5i$ and $w^*z=-14-5i$. Their sum is $-28$, leaving $13+17-28=2$. The two cross terms are conjugates, so their sum is real. This algebra explains why replacing a sum of complex coordinates by a sum of their squared sizes changes a calculation; assigning measurement probabilities to amplitudes will require the later physical postulates.

### Finite vectors: keep coordinates and operations separate

Let $n$ be a positive integer. The notation $\mathbb C^n$ denotes all ordered lists of $n$ complex numbers, written as columns. For vectors $v,w\in\mathbb C^n$, write their coordinates as $v_k,w_k$, with $k=1,\ldots,n$. A **scalar** is one complex number, such as $\lambda$; a vector has $n$ coordinates. Define addition and scalar multiplication by

$$
(v+w)_k=v_k+w_k,\qquad (\lambda v)_k=\lambda v_k.
$$

Only equal-length coordinate vectors can be added this way. Coordinates in this section are with respect to the fixed standard coordinate system; change of basis is a later topic. In Python a list stores entries in that order: `v[0]` corresponds to mathematical $v_1$. List addition joins lists and does not perform this vector addition, so write `[v[k] + w[k] for k in range(len(v))]` after checking equal lengths.

Define $v^*$ here to mean the **entrywise conjugate column**, so $(v^*)_k=v_k^*$. It is still a column. It is not a transposed row or an adjoint; those operations will be introduced separately. For each coordinate, the scalar identities give

$$
\begin{aligned}
((v+w)^*)_k&=(v_k+w_k)^*=v_k^*+w_k^*,\\
((\lambda v)^*)_k&=(\lambda v_k)^*=\lambda^*v_k^*,\\
((v^*)^*)_k&=(v_k^*)^*=v_k.
\end{aligned}
$$

Since corresponding coordinates agree for every $k$, the vector identities are

$$
(v+w)^*=v^*+w^*,\qquad
(\lambda v)^*=\lambda^*v^*,\qquad
(v^*)^*=v.
$$

The second rule is called **conjugate linearity**: conjugation also acts on the scalar coefficient. For

$$
v=\begin{pmatrix}1+i\\2-i\end{pmatrix},\qquad
iv=\begin{pmatrix}-1+i\\1+2i\end{pmatrix},
$$

we obtain $(iv)^*=(-1-i,\,1-2i)$ as a column. Keeping $i$ unchanged instead gives $iv^*=(1+i,\,-1+2i)$, a different vector. Checking with a real coefficient alone would not expose that error.

Define a coordinate squared length by

$$
L(v)=\sum_{k=1}^n\lvert v_k\rvert^2
    =\sum_{k=1}^n v_k^*v_k.
$$

The summation sign adds the indicated expression for each coordinate. Each term is real and nonnegative. Therefore $L(v)\ge0$, and $L(v)=0$ exactly when every coordinate is zero. Also,

$$
\begin{aligned}
L(\lambda v)
 &=\sum_{k=1}^n\lvert\lambda v_k\rvert^2\\
 &=\sum_{k=1}^n\lvert\lambda\rvert^2\lvert v_k\rvert^2\\
 &=\lvert\lambda\rvert^2 L(v).
\end{aligned}
$$

The last step moves the same real factor outside a finite sum. For the displayed $v$, $L(v)=2+5=7$. Its sum of ordinary squares is instead $(1+i)^2+(2-i)^2=3-2i$, which cannot serve as this real squared length.

For a nonzero vector, let $u=v/\sqrt{L(v)}$, meaning divide each coordinate by the same positive real number. The scaling identity gives $L(u)=(1/L(v))L(v)=1$. A zero vector cannot be normalized this way. This is a coordinate calculation, not yet a derivation of what counts as a physical state. Inner products and their geometry belong to 2.2; Chapter 3 gives state interpretation.

### Match the identities to executable checks

The [complete program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/complex_coordinates.py) uses two representations: Python complex numbers and integer pairs `(a, b)`. The latter compute real and imaginary parts with explicit integer arithmetic rather than calling complex multiplication or conjugation.

| Mathematical operation | Complex implementation | Independent coordinate check |
|---|---|---|
| Addition and multiplication | `z+w`, `z*w` | `pair_add`, `pair_mul` implement the displayed real/imaginary formulas |
| Conjugation | `z.conjugate()` | `pair_conj` negates only the second coordinate |
| Squared modulus | `z.conjugate()*z` | `pair_mod2` returns `a*a+b*b` |
| Vector scaling/conjugation | `scale`, `conjugate_vector` | Explicit displayed result for $iv$ and a non-real coefficient $2-i$ |
| Squared length | `squared_length(v)` | The independently expanded value $2+5=7$ |
| Normalization | `scale(1/math.sqrt(7), v)` | Squared length agrees with 1 within $10^{-12}$ absolute error |

Run from the repository root with Python 3.12; no packages are required:

```bash
python examples/foundations/complex_coordinates.py
```

Expected output:

```text
z=2-3j, w=-1+4j: z*w=10+11j; squared moduli=13,17
Squared modulus of z+w: 2; sum of squared moduli: 30 (not additive)
v=[1+1j, 2-1j]: squared length=7; sum of squares=3-2j (wrong rule)
conjugate(i*v)=[-1-1j, 1-2j]; keeping i unchanged fails
After dividing v by sqrt(7): squared length=1.000000000000
25 scalars / 625 ordered pairs checked against integer-coordinate arithmetic.
Conjugation, product modulus, vector scaling, and zero-vector checks passed.
```

The 25 scalars have integer real and imaginary parts from $-2$ to $2$; the program checks all 625 ordered pairs. These small integer operations are exactly representable in Python's complex floating-point representation. Square-root normalization uses floating point, so its assertion uses an explicit tolerance. A floating-point conjugate product can also carry a tiny imaginary residual: the program checks that its magnitude is at most $10^{-12}$ before summing real parts. This tolerance is scoped to these bounded examples, not a general error bound. The printed twelve decimals do not mean the normalized entries are exact. General large or tiny inputs need numerical care beyond these bounded checks; a future numerical-reasoning section treats that problem.

The finite checks can catch an implementation mistake. The coordinate derivations above, rather than enumeration, establish the identities for arbitrary complex numbers and finite vectors. No FlagQuantum API, quantum experiment or physical probability claim is involved.

### Transfer, debugging, and answers

**2.1-B — A different coordinate.** Take $q=-3+4i$. Compute $q^*$, $\lvert q\rvert^2$, $q^2$ and $q^{-1}$. Explain why $q^2$ and $\lvert q\rvert^2$ differ.

**2.1-C — Repair a program.** A function computes `sum(z*z for z in vector)` and calls it squared length. Show the failure for this section's $v$, repair the expression and explain why testing only real coordinates could miss the defect.

**2.1-D — Transfer the proof.** Without running code, determine $L((2-i)v)$ and show how to normalize that vector. What must be checked before dividing?

**2.1-E — Distinguish operations.** A two-entry vector becomes a two-entry vector after `.conjugate()` is applied to each coordinate. Has it become a row? Has a measurement been performed?

**Answers and reasoning**

- **A.** First $i(1+i)=-1+i$, then conjugate to obtain $-1-i$. Keeping the coefficient unchanged gives $i(1-i)=1+i$. The correct rule conjugates $i$ as well: $(iv)^*=(-i)v^*$.
- **B.** $q^*=-3-4i$, $\lvert q\rvert^2=9+16=25$, $q^2=9-24i-16=-7-24i$, and $q^{-1}=(-3-4i)/25$. Ordinary squaring is not multiplication by the conjugate.
- **C.** The defective expression gives $3-2i$ rather than 7. Use `sum(z.conjugate()*z for z in vector)`; mathematically each term is real. For real entries conjugation changes nothing, so the defective and correct rules agree on that restricted test set.
- **D.** The scalar has squared modulus $2^2+(-1)^2=5$, so $L((2-i)v)=5\cdot7=35$. Divide each coordinate of $(2-i)v$ by $\sqrt{35}$. The divisor is nonzero because the vector is nonzero; for an arbitrary input first check its squared length is positive.
- **E.** Neither. Entrywise conjugation leaves the coordinate shape unchanged. It is a mathematical operation on stored numbers, not a measurement record or a transposition.

The next lesson, [2.2 Inner products, adjoints, and orthogonality](#sec-complex-vectors-operators-and-numerical-reasoning-2), uses these conjugation rules to compare different vectors, rather than just the coordinates of one vector with themselves.

### Source, status, and limits

The assigned locator is [NC:2.1.1](../references/proof-sources.md#source-nc-2-1-1), Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010), §2.1.1 beginning on printed p. 62. The immediately preceding coordinate introduction on printed pp. 61–62 and Figure 2.1 on p. 62 supply the companion vector and conjugation conventions. Those specific pages were consulted from the previously supplied local source copy. The elementary scalar bridge, component proofs, examples and exercises here are original; §2.1.1 is not being cited as a source of every proof written above.

Depth **F**: full component derivations of the stated conjugation and modulus identities, including finite-vector consequences. [The execution and section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/2.1.json) separates author checks from pending independent reviews. No theorem is deferred to an exercise, and no quantum postulate is asserted.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-2"></span>

## 2.2 Inner products, adjoints, and orthogonality

A squared length compares a vector with itself. How can we compare two different vectors, or extract the part of one vector that points along another? We need a rule that preserves complex information while returning a positive squared length when its two inputs coincide.

The entry requirement is [2.1](#sec-complex-vectors-operators-and-numerical-reasoning-1): complex conjugation, scalar multiplication, finite coordinate sums and their squared lengths. This section derives orthogonal projection and the Cauchy–Schwarz inequality, including zero cases and equality conditions. The calculations are mathematical; they are not measurements of a quantum system.

### Fix which argument is conjugated

For equal-length coordinate columns $v,w\in\mathbb C^n$, define the **standard inner product** by

$$
\langle v,w\rangle=\sum_{k=1}^n v_k^*w_k.
$$

We conjugate the **first** argument. The result is one complex scalar, not a vector. Using the scalar identities proved in 2.1 gives three properties:

$$
\begin{aligned}
\langle v,\alpha w+\beta x\rangle
 &=\alpha\langle v,w\rangle+\beta\langle v,x\rangle,\\
\langle\alpha v+\beta w,x\rangle
 &=\alpha^*\langle v,x\rangle+\beta^*\langle w,x\rangle,\\
\langle w,v\rangle&=\langle v,w\rangle^*.
\end{aligned}
$$

Here $x$ is another vector of the same length and $\alpha,\beta$ are complex scalars. To verify the first identity, distribute $v_k^*(\alpha w_k+\beta x_k)$ and take the coefficients outside the finite sum. For the second, $(\alpha v_k+\beta w_k)^*=\alpha^*v_k^*+\beta^*w_k^*$ gives exactly the conjugated coefficients. For the third, conjugating $\sum_k v_k^*w_k$ gives $\sum_k v_kw_k^*=\sum_k w_k^*v_k$. Thus swapping the arguments generally changes the answer.

Also $\langle v,v\rangle=\sum_k\lvert v_k\rvert^2$ is real and nonnegative, and is zero exactly when $v=0$. This is **positive definiteness**. An inner product more generally is a scalar-valued rule with linearity in the second argument, conjugate symmetry and positive definiteness. Conjugate linearity in the first then follows by swapping arguments, using linearity and conjugating back. The projection and inequality proofs below use these properties, so apply to any such positive-definite inner product. Their concrete coordinate formulas here use the standard one.

Define the **norm** by $\|v\|=\sqrt{\langle v,v\rangle}$, taking the nonnegative square root. For the standard coordinates it is the square root of $L(v)$ from 2.1. More generally, the two scaling rules give $\|\alpha v\|^2=\alpha^*\alpha\langle v,v\rangle=\lvert\alpha\rvert^2\|v\|^2$, hence $\|\alpha v\|=\lvert\alpha\rvert\|v\|$. A nonzero vector is normalized by dividing it by its norm. Two vectors are **orthogonal** when their inner product is zero. An **orthonormal** collection consists of unit vectors whose distinct members are orthogonal. These definitions depend on the chosen inner product.

### A worked comparison with complex coordinates

Use the columns

$$
a=\begin{pmatrix}1\\i\end{pmatrix},\qquad
v=\begin{pmatrix}2\\1+i\end{pmatrix}.
$$

Their squared norms are $\|a\|^2=1+1=2$ and $\|v\|^2=4+2=6$. Their inner product is

$$
\langle a,v\rangle=1\cdot2+(-i)(1+i)=2-i+1=3-i.
$$

Reversing the arguments gives $\langle v,a\rangle=3+i$. Omitting conjugation instead gives $1\cdot2+i(1+i)=1+i$. Worse, that unconjugated rule assigns $a$ a “squared length” $1+i^2=0$, although $a\ne0$. Positive definiteness fails.

**2.2-A — Predict the coefficient.** What is $\langle ia,v\rangle$? What is $\langle a,iv\rangle$? Work from $\langle a,v\rangle=3-i$ before calling a tensor routine.

### Derive the component along a direction

Take any nonzero direction vector $a$ and any vector $v$ in the same inner product space. We seek a scalar $c$ for which the residual $r=v-ca$ is orthogonal to $a$. Linearity in the second argument requires

$$
0=\langle a,r\rangle
 =\langle a,v\rangle-c\langle a,a\rangle.
$$

Because $a\ne0$, positive definiteness makes the denominator below positive. Therefore there is exactly one such scalar:

$$
c=\frac{\langle a,v\rangle}{\langle a,a\rangle},\qquad
p=ca,\qquad r=v-p.
$$

The vector $p$ is the **orthogonal projection** onto the line of complex multiples of $a$. The coefficient $c$ is not itself the projection vector. If $a$ is already a unit vector, the denominator is 1; otherwise it must be retained.

For our columns, $c=(3-i)/2$. Multiplying each coordinate of $a$ by this scalar gives

$$
p=\begin{pmatrix}(3-i)/2\\(1+3i)/2\end{pmatrix},\qquad
r=\begin{pmatrix}(1+i)/2\\(1-i)/2\end{pmatrix}.
$$

Check the defining condition directly:

$$
\langle a,r\rangle
 =\frac{1+i}{2}-i\frac{1-i}{2}
 =\frac{1+i-1-i}{2}=0.
$$

In particular $\langle p,r\rangle=c^*\langle a,r\rangle=0$, and conjugate symmetry gives $\langle r,p\rangle=0$. Expanding $v=p+r$ now proves the squared-length decomposition:

$$
\begin{aligned}
\|v\|^2
 &=\langle p+r,p+r\rangle\\
 &=\|p\|^2+\langle p,r\rangle+\langle r,p\rangle+\|r\|^2\\
 &=\|p\|^2+\|r\|^2.
\end{aligned}
$$

Numerically $\|p\|^2=5$ and $\|r\|^2=1$, giving $6=5+1$. Orthogonality, rather than an arbitrary split into two vectors, removes the cross terms.

This also proves a nearest-point statement. For any complex scalar $t$, write $v-ta=r+(c-t)a$. The cross terms vanish for the same reason, so

$$
\|v-ta\|^2=\|r\|^2+\lvert c-t\rvert^2\|a\|^2.
$$

The second term is nonnegative and vanishes exactly when $t=c$. Thus $p$ is the unique nearest point on that line. No differentiation or optimization algorithm was needed. A zero direction cannot be used in the quotient formula; its span contains only zero, whose projection is trivially zero. Our executable routine deliberately requires a nonzero direction and rejects that special input.

### Cauchy–Schwarz and its equality cases

From $p=ca$, the scaling identity gives

$$
\|p\|^2=\lvert c\rvert^2\|a\|^2
 =\frac{\lvert\langle a,v\rangle\rvert^2}{\|a\|^2}.
$$

Substitute this into the squared-length decomposition. The nonnegativity of $\|r\|^2$ gives

$$
0\le\|r\|^2
 =\|v\|^2-\frac{\lvert\langle a,v\rangle\rvert^2}{\|a\|^2}.
$$

Multiply by the positive number $\|a\|^2$ to obtain the **Cauchy–Schwarz inequality**:

$$
\lvert\langle a,v\rangle\rvert^2\le\|a\|^2\|v\|^2.
$$

For $a\ne0$, equality holds exactly when $\|r\|^2=0$, hence exactly when $r=0$ and $v=ca$. If $a=0$, both sides are zero for every $v$, without using a quotient. Combining the cases, equality holds exactly when one vector is zero or the nonzero vectors are scalar multiples of each other. These are precisely the linearly dependent pairs: some complex coefficients, not both zero, make a linear combination of the two vectors zero.

Our example gives $\lvert3-i\rvert^2=10<2\cdot6=12$, consistent with its nonzero residual. Replacing $v$ by $(2-i)a$ gives equality. Checking only one pair with a strict inequality would miss the equality boundary.

For completeness, this inequality supplies the norm's triangle inequality. With $\operatorname{Re}z$ meaning the real part of a scalar, conjugate symmetry gives

$$
\begin{aligned}
\|v+w\|^2
 &=\|v\|^2+2\operatorname{Re}\langle v,w\rangle+\|w\|^2\\
 &\le\|v\|^2+2\|v\|\|w\|+\|w\|^2\\
 &=(\|v\|+\|w\|)^2.
\end{aligned}
$$

The middle step uses $\operatorname{Re}z\le\lvert z\rvert$ from the scalar modulus formula, followed by Cauchy–Schwarz and nonnegative square roots. Taking nonnegative square roots once more yields $\|v+w\|\le\|v\|+\|w\|$.

### An adjoint conjugates and changes shape

The entrywise conjugate column $v^*$ from 2.1 is different from the **adjoint** $v^\dagger$, which is the conjugated **row**:

$$
v^\dagger=\begin{pmatrix}v_1^*&\cdots&v_n^*\end{pmatrix},\qquad
\langle v,w\rangle=v^\dagger w.
$$

The row-column product means sum of corresponding entries. In Dirac notation, $|v\rangle$ denotes the vector column and $\langle v|$ its adjoint row; $\langle v|w\rangle$ is the same scalar as $\langle v,w\rangle$ here. The row and column are different shaped objects even when they contain one coordinate.

A bounded matrix bridge lets us verify the associated rule now. Let $A$ be an $m$-by-$n$ array of complex entries $A_{jk}$, where $j$ labels rows and $k$ columns. Define $(Aw)_j=\sum_k A_{jk}w_k$ for $w\in\mathbb C^n$, and define the adjoint array by $(A^\dagger)_{kj}=A_{jk}^*$. Its shape is $n$-by-$m$. For $v\in\mathbb C^m$,

$$
\begin{aligned}
\langle v,Aw\rangle
 &=\sum_{j,k}v_j^*A_{jk}w_k\\
 &=\sum_k\left(\sum_j A_{jk}^*v_j\right)^*w_k\\
 &=\langle A^\dagger v,w\rangle.
\end{aligned}
$$

The middle equality conjugates each product and uses finite-sum rearrangement; the inner sum is coordinate $k$ of $A^\dagger v$. This identity uses the standard coordinate inner products. We have supplied the array operations locally; the general theory of linear maps and changes of coordinates follows in 2.3.

For an explicit check, use our earlier $a,v$ and

$$
A=\begin{pmatrix}1&i\\2-i&3\end{pmatrix},\qquad
A^\dagger=\begin{pmatrix}1&2+i\\-i&3\end{pmatrix}.
$$

Then $Av=(1+i,\,7+i)$ and $A^\dagger a=(2i,\,2i)$ as columns. Both $\langle a,Av\rangle$ and $\langle A^\dagger a,v\rangle$ evaluate to $2-6i$. Plain transpose exchanges indices but does not conjugate entries, so cannot generally replace the adjoint.

### Formula to tensor operations and independent checks

The [complete example](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/inner_products.py) targets Python 3.12 and PyTorch 2.13.0, CPU `complex128`. It checks tensor results against explicit integer-coordinate arithmetic. For $v_k=a_k+ib_k$ and $w_k=c_k+id_k$, its independent reference sums real parts $a_kc_k+b_kd_k$ and imaginary parts $a_kd_k-b_kc_k$, without calling a complex inner-product routine.

| Formula or distinction | Executable operation | Independent check |
|---|---|---|
| $\sum_k v_k^*w_k$ | `torch.vdot(v, w)` for one-dimensional tensors | `pair_inner` uses the displayed real/imaginary expansion |
| $v^*$ versus $v^\dagger$ | `v.conj()` versus `v[:, None].mH` | Shapes `(2,)` versus `(1, 2)` for the chosen representation |
| $\|v\|^2$ | `torch.vdot(v, v).real` | Hand-expanded 6 for the worked vector |
| Projection onto nonzero $a$ | `projection(a, v)` | Explicit half-integer coordinates of $p,r$ and zero residual overlap |
| $A^\dagger$ and its identity | `A.mH`, `torch.vdot(A.mH @ a, v)` | Explicit adjoint entries and the common value $2-6i$ |
| Missing conjugation | `torch.dot(a, a)` | Returns 0 for a nonzero vector, whereas `vdot` returns 2 |

PyTorch's one-dimensional storage is a coordinate representation, not inherently a row or column; `[:, None]` explicitly makes a column before `.mH` creates its adjoint row. These distinctions avoid relying on a shape convention the tensor does not carry.

From the repository root, install the existing pinned example requirements if needed, then run:

```bash
python -m pip install -r requirements-examples.txt
python examples/foundations/inner_products.py
```

Expected output:

```text
Tensor execution: CPU, complex128; no quantum backend.
<a,v>=3-1j; squared norms a=2, v=6; Cauchy-Schwarz: 10 <= 12
Projection=[1.5-0.5j, 0.5+1.5j]; residual=[0.5+0.5j, 0.5-0.5j]
<a,residual>=0; squared norms: 6 = 5 + 1
Adjoint check: <a,A v> = <A^H a,v> = 2-6j
Bilinear dot(a,a)=0 is wrong for length; vdot(a,a)=2
81 vectors / 6561 ordered inner products match integer-pair references.
Projection, normalization, equality, zero-axis, and conjugation checks passed.
```

The 81 vectors have two complex coordinates, with each real and imaginary part chosen from $-1,0,1$. Tests compare all 6561 ordered inner products, conjugate symmetry and the inequality, then check the worked projection, a unit-direction equivalent, an equality case, a zero vector and rejection of a zero direction. Rounded calculations use absolute tolerance $10^{-12}$, with zero relative tolerance in tensor comparisons. This bounded numerical tolerance is not a general stability guarantee, particularly for nearly zero directions. Numerical conditioning will be treated separately.

The finite tests validate these implementations; they do not prove Cauchy–Schwarz. Its proof is the nonnegative-residual argument above. No FlagQuantum execution is needed for this mathematical reference.

### Transfer, failure analysis, and answers

**2.2-B — Reverse the overlap.** A programmer uses $\langle v,a\rangle/\langle a,a\rangle$ as the coefficient multiplying $a$. For the worked vectors, compute the resulting residual overlap with $a$. Does orthogonality hold?

**2.2-C — Normalize or keep the denominator.** Let $e=a/\sqrt2$. Find $\langle e,v\rangle e$ and explain why it equals the projection computed with the unnormalized direction. What goes wrong if one uses $\langle a,v\rangle a$ directly?

**2.2-D — Transfer the proof boundary.** Suppose an alternative rule assigns zero “squared length” to a nonzero vector. Which step of the projection/inequality proof is no longer justified? Can a finite set of successful tensor comparisons restore the theorem under that rule?

**2.2-E — Change the direction.** Replace $a$ by $b=2ia$. Derive the new coefficient and show that the projection vector stays the same. State the nonzero assumption needed for this argument.

**Answers and reasoning**

- **A.** First-argument scaling conjugates $i$: $\langle ia,v\rangle=-i(3-i)=-1-3i$. Second-argument scaling does not: $\langle a,iv\rangle=i(3-i)=1+3i$.
- **B.** The wrong coefficient is $(3+i)/2$. The residual overlap is $(3-i)-((3+i)/2)2=-2i$, so the defining orthogonality condition fails.
- **C.** $\langle e,v\rangle=(3-i)/\sqrt2$, hence multiplying by $e$ gives $((3-i)/2)a=p$. Omitting the denominator with unnormalized $a$ gives $2p$, not $p$.
- **D.** A nonzero direction no longer guarantees a positive denominator, and zero residual length no longer implies zero residual vector. Positive definiteness supports both steps. Successful samples cannot replace a failed assumption; even the unconjugated dot rule passes some real-coordinate examples.
- **E.** The numerator becomes $-2i\langle a,v\rangle$ and the denominator becomes $4\langle a,a\rangle$, giving coefficient $-ic/2$. Multiplication by $b=2ia$ yields $ca=p$. The original direction must be nonzero; the rescaling factor is also nonzero.

The next planned lesson, [2.3 Linear maps, bases, and changes of coordinates](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-3), develops how transformations act on coordinates and how their representations change.

### Source, status, and limits

Assigned companion source: [NC:2.1.4](../references/proof-sources.md#source-nc-2-1-4), Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010), §2.1.4, printed pp. 65–68, especially the inner-product conventions, normalization and Box 2.1. Those pages were consulted from the previously supplied local copy. The residual-based proof here supplies its own steps and equality/zero cases; it does not depend on the book's separate Gram–Schmidt argument. The matrix bridge, worked coordinates and exercises are original exposition.

Depth **F**: full derivation of orthogonal projection, nearest-point uniqueness and Cauchy–Schwarz with equality conditions for a positive-definite inner product. [The section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/2.2.json) separates author execution from pending independent mathematical, implementation and reader reviews. Projection is a mathematical construction here; quantum measurement rules are not inferred from it.
