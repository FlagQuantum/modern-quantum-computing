# 2. Complex Vectors, Operators, and Numerical Reasoning

**Working draft: sections 2.1–2.8 · Writing Baseline 1.0 · October 21, 2026.** All eight sections have working drafts. Author execution checks are recorded separately from independent mathematical, implementation and reader review, which remain pending. This is not an accepted chapter. Section 2.1 uses Python 3.12 and its standard library; 2.2–2.8 add PyTorch 2.13.0 CPU complex128 tensor checks.

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

The next lesson, [2.3 Linear maps, bases, and changes of coordinates](#sec-complex-vectors-operators-and-numerical-reasoning-3), develops how transformations act on coordinates and how their representations change.

### Source, status, and limits

Assigned companion source: [NC:2.1.4](../references/proof-sources.md#source-nc-2-1-4), Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010), §2.1.4, printed pp. 65–68, especially the inner-product conventions, normalization and Box 2.1. Those pages were consulted from the previously supplied local copy. The residual-based proof here supplies its own steps and equality/zero cases; it does not depend on the book's separate Gram–Schmidt argument. The matrix bridge, worked coordinates and exercises are original exposition.

Depth **F**: full derivation of orthogonal projection, nearest-point uniqueness and Cauchy–Schwarz with equality conditions for a positive-definite inner product. [The section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/2.2.json) separates author execution from pending independent mathematical, implementation and reader reviews. Projection is a mathematical construction here; quantum measurement rules are not inferred from it.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-3"></span>

## 2.3 Linear maps, bases, and changes of coordinates

Two programs can store different coordinate arrays for the same vector, and different matrices for the same transformation. To compare them, we must know which basis each array uses. Matching the printed entries is not the right test; reconstructing the same vector and transformed output is.

The prerequisite is [2.2](#sec-complex-vectors-operators-and-numerical-reasoning-2), including inner products, adjoints and its matrix-vector bridge. We now define bases and linear maps, derive their matrix representations, and prove the change-of-basis rule. No determinant or eigenvalue calculation is assumed.

### A basis makes coordinates unique

A finite complex vector space is a collection in which vector addition and multiplication by complex scalars obey the usual arithmetic rules. Our concrete model is $\mathbb C^n$ from 2.1; we also use a label $V$ for the underlying space to distinguish a vector from its chosen coordinates.

An ordered collection $E=(e_1,\ldots,e_n)$ is a **basis** when it spans $V$ and is linearly independent. Spanning means every $v\in V$ can be written as $v=\sum_j x_j e_j$. Independence means the only coefficients satisfying $\sum_j c_j e_j=0$ are all zero. All coefficients are complex scalars, and the order of the vectors matters.

These conditions prove uniqueness: if $\sum_j x_j e_j=\sum_j y_j e_j$, subtraction gives $\sum_j(x_j-y_j)e_j=0$, so independence forces $x_j=y_j$ for every $j$. Spanning supplies existence; independence supplies uniqueness. We write the coordinate column as

$$
[v]_E=\begin{pmatrix}x_1\\\vdots\\x_n\end{pmatrix}.
$$

The symbol $[v]_E$ is a coordinate representation of $v$. A different basis can give a different column without changing $v$. In $\mathbb C^2$, the standard basis columns $(1,0)$ and $(0,1)$ are independent because a zero linear combination forces both coefficients to vanish, and span because $(a,b)=a(1,0)+b(0,1)$. This gives a concrete basis without invoking a general basis-existence theorem.

### A linear map is determined by its basis images

A map $T:V\to W$ assigns a vector of $W$ to each vector of $V$. It is **linear** when, for all complex scalars $\alpha,\beta$ and vectors $v,w$ in its input space,

$$
T(\alpha v+\beta w)=\alpha T(v)+\beta T(w).
$$

For example, swapping the two coordinates of $\mathbb C^2$ is linear: swapping a coordinatewise sum or scalar multiple gives the sum or multiple of the swapped columns. By contrast, entrywise conjugation is not complex linear: conjugating $iv$ gives $-iv^*$ rather than $iv^*$ for a nonzero $v$.

Choose input basis $E=(e_1,\ldots,e_n)$ and output basis $F=(f_1,\ldots,f_m)$. Expand each basis image as $T(e_j)=\sum_i A_{ij}f_i$. These coefficients form column $j$ of an $m$-by-$n$ matrix $A$. For an arbitrary $v=\sum_j x_j e_j$, linearity gives

$$
\begin{aligned}
T(v)&=\sum_j x_j T(e_j)\\
    &=\sum_j x_j\sum_i A_{ij}f_i\\
    &=\sum_i\left(\sum_j A_{ij}x_j\right)f_i.
\end{aligned}
$$

Uniqueness of coordinates therefore proves $[T(v)]_F=A[v]_E$. Conversely, any specified matrix gives a linear rule on coordinate columns, since distributing its finite sums over $\alpha x+\beta y$ gives $\alpha Ax+\beta Ay$. Thus choosing bases relates linear maps to matrices; a matrix representation needs both its input and output basis labels.

If one matrix $A$ maps input coordinates to intermediate coordinates and a second matrix $D$ maps those intermediate coordinates to final coordinates, composition means first $A$, then $D$. The final coordinate $i$ is $\sum_j D_{ij}\sum_k A_{jk}x_k$. Regrouping the finite sums gives $\sum_k(\sum_j D_{ij}A_{jk})x_k$. This defines the matrix product $(DA)_{ik}=\sum_j D_{ij}A_{jk}$ and proves the composition rule. The rightmost matrix acts first. The intermediate coordinate basis and dimensions must match.

**2.3-A — Build the columns.** For the map that swaps standard-coordinate entries in $\mathbb C^2$, what are its two basis images and hence its matrix? Why are the images columns rather than rows?

### Derive the coordinate conversion before transforming a matrix

For a map $T:V\to V$, suppose the old basis is $E$ and the new basis is $B=(b_1,\ldots,b_n)$. Define $S$ to have column $j$ equal to $[b_j]_E$. If $y=[v]_B$, expanding $v=\sum_j y_jb_j$ in old coordinates gives

$$
x=[v]_E=Sy,\qquad y=[v]_B=S^{-1}x.
$$

Here $S^{-1}$ denotes the inverse coordinate conversion. It exists because each old coordinate column represents exactly one vector, which has exactly one new coordinate column. In particular, solving $Sy=x$ has a unique solution for every $x$. This inverse conversion is linear: if $Sy=x$ and $Sz=w$, then $S(\alpha y+\beta z)=\alpha x+\beta w$, and uniqueness identifies $\alpha y+\beta z$ as the inverse image of that combination. The matrix-representation result above therefore also applies to the inverse conversion. Its matrix satisfies $S^{-1}S=SS^{-1}=I$, where $I$ denotes the identity matrix, leaving coordinate columns unchanged. This argument uses the basis assumptions, not merely that $S$ is square.

Let $A$ represent $T$ with basis $E$ for both input and output. Starting with new coordinates $y$, the three stages are

$$
y\ \xrightarrow{\ S\ }\ x\ \xrightarrow{\ A\ }\ x'
\ \xrightarrow{\ S^{-1}\ }\ y'.
$$

The prime labels an output; it is not differentiation. Substituting gives $y'=S^{-1}ASy$ for every input $y$. Therefore the new representation, denoted $A_B$, is

$$
A_B=S^{-1}AS.
$$

This is a **similarity transformation**. It changes the representation of the same map. The final inverse is required because $ASy$ is still in the old output coordinates. Omitting it mixes coordinate types.

For distinct input and output spaces with different basis conversions, the same three-stage argument gives $A_{\mathrm{new}}=S_{\mathrm{out}}^{-1}A S_{\mathrm{in}}$. Here $S_{\mathrm{in}}$ and $S_{\mathrm{out}}$ convert new coordinates to old coordinates in their respective spaces. Only when the same conversion applies on both sides does this become the displayed similarity formula.

### A nonorthogonal basis exposes the missing inverse

For the swap map, use the old standard basis and the new columns $b_1=(1,0)$, $b_2=(1,1)$. They span because $x=(x_1,x_2)$ equals $(x_1-x_2)b_1+x_2b_2$, and this formula is unique. Hence they are a basis. Their inner product is 1, so they are not orthogonal. The matrices are

$$
A=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
S=\begin{pmatrix}1&1\\0&1\end{pmatrix},\quad
S^{-1}=\begin{pmatrix}1&-1\\0&1\end{pmatrix}.
$$

The inverse follows from the explicit coefficients $y_1=x_1-x_2$, $y_2=x_2$; multiplying $S$ and this inverse in either order also gives $I$. Now calculate

$$
AS=\begin{pmatrix}0&1\\1&1\end{pmatrix},\qquad
A_B=S^{-1}(AS)=\begin{pmatrix}-1&0\\1&1\end{pmatrix}.
$$

An independent column check avoids relying on that multiplication alone. The swap sends $b_1$ to $(0,1)=-b_1+b_2$, giving the first column $(-1,1)$. It sends $b_2$ to itself, giving the second column $(0,1)$. These are exactly the columns of $A_B$.

For $x=(2,3)$, the new coordinates are $y=(-1,3)$. Applying $A_B$ gives $y'=(1,2)$, which reconstructs $Sy'=(3,2)$, exactly the direct swap output $Ax$.

Now treat $AS$ as though it were the new matrix. It returns $(3,2)$ from input $y$, but those numbers are old coordinates. Interpreting them as new coordinates reconstructs $S(3,2)=(5,2)$, the wrong vector. A matrix can return plausible-looking numbers while violating its coordinate contract.

### When an adjoint can replace an inverse

Suppose both the old and new bases are orthonormal for the same inner product. In old orthonormal coordinates, entry $(j,k)$ of $S^\dagger S$ is the inner product of new basis vectors $b_j,b_k$. Orthonormality makes this entry 1 when $j=k$ and 0 otherwise, so $S^\dagger S=I$. Since $S$ is invertible, multiplying this equality on the right by $S^{-1}$ gives $S^\dagger=S^{-1}$, and hence also $SS^\dagger=I$.

A square matrix with these two adjoint identities is called **unitary**. In this special case,

$$
A_B=S^\dagger AS.
$$

Broader properties of unitary operators belong to 2.4. Here the criterion follows directly from orthonormal columns. It does not apply to our nonorthogonal $S$, whose adjoint is $\begin{pmatrix}1&0\\1&1\end{pmatrix}$ rather than its inverse.

For a complex orthonormal example, take

$$
Q=\frac1{\sqrt2}\begin{pmatrix}1&1\\i&-i\end{pmatrix}.
$$

Each column has squared length $(1+1)/2=1$, and their overlap is $(1+(-i)(-i))/2=0$. Therefore $Q^{-1}=Q^\dagger$. With the same swap map,

$$
Q^\dagger A Q=\begin{pmatrix}0&-i\\i&0\end{pmatrix}.
$$

For example, the first column comes from overlaps of the two new unit columns with $A(1,i)/\sqrt2=(i,1)/\sqrt2$: they are 0 and $i$. The second gives $-i$ and 0. This supplies a component check independent of a matrix-product routine. A plain transpose still fails because $Q$ has complex entries.

The inner product also needs its coordinate convention. With the old basis orthonormal, for general $x=Sy$ the adjoint identity from 2.2 gives

$$
\langle x,x\rangle=\langle Sy,Sy\rangle
 =y^\dagger(S^\dagger S)y.
$$

The array $G=S^\dagger S$ is called the **Gram matrix** of the new basis. It records the inner products between its columns. With an orthonormal new basis $G=I$; with our nonorthogonal basis,

$$
G=\begin{pmatrix}1&1\\1&2\end{pmatrix}.
$$

For $y=(-1,3)$, the naive coordinate sum of squared moduli is 10, but $Gy=(2,5)$ gives $y^\dagger Gy=-2+15=13$, agreeing with $\|x\|^2=4+9=13$. The vector's length did not change. The Euclidean-coordinate formula cannot be transferred unchanged to a nonorthonormal basis.

### Passive coordinates and active transformations

A **passive** basis change replaces $x$ by $S^{-1}x$ and changes how we interpret its entries. It represents the same underlying vector. An **active** linear transformation instead applies a map to the vector while keeping the coordinate basis fixed.

For example, in the fixed standard basis, $Sx=(5,3)$ differs from $x=(2,3)$: the same array $S$ is now being used as an active map. By contrast, $y=S^{-1}x=(-1,3)$ reconstructs $Sy=x$. The role is determined by the declared input and output meanings, not by the array's entries alone. Neither a change of coordinates nor an arbitrary linear map automatically specifies a physically allowed quantum operation.

### Formula to executable coordinate contracts

The [complete program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/basis_changes.py) targets Python 3.12, PyTorch 2.13.0, CPU `complex128`. It uses a linear-system solver rather than explicitly constructing an inverse in routine calculations. `torch.linalg.solve(S, x)` finds the column $y$ satisfying $Sy=x$; with matrix right-hand side `A @ S`, it solves once for each column to obtain $S^{-1}AS$.

| Mathematical statement | Program operation | Independent reference |
|---|---|---|
| New coordinates $y=S^{-1}x$ | `torch.linalg.solve(basis, x)` | Explicit $(x_1-x_2,x_2)$ |
| New map $A_B=S^{-1}AS$ | `torch.linalg.solve(basis, matrix @ basis)` | Basis-image columns $(-1,1)$ and $(0,1)$ |
| Same transformed vector | `basis @ (changed @ y)` | Direct coordinate swap $(x_2,x_1)$ |
| Omitted output inverse | `wrong = matrix @ basis` | Incorrect reconstruction $(5,2)$ for the worked input |
| Orthonormal special case | `q.mH @ matrix @ q` | Explicit matrix with off-diagonal entries $-i,i$ |
| Preserved inner product | `torch.vdot(y, gram @ y)` | Hand-expanded 13, compared with naive 10 |

Run from the repository root with the existing pinned environment:

```bash
python -m pip install -r requirements-examples.txt
python examples/foundations/basis_changes.py
```

Expected output:

```text
CPU complex128 coordinate checks; no quantum execution.
S=[[1,1],[0,1]]; B=S^(-1) A S=[[-1,0],[1,1]]
x=[2,3] -> new coordinates y=[-1,3] -> B*y=[1,2]
Reconstructed output S*B*y=[3,2], equal to direct swap(x)
Omitting output inverse gives reconstructed [5,2] (wrong)
Squared length: old=13, naive new=10, Gram-weighted new=13
Complex orthonormal basis: Q^H A Q=[[0,-i],[i,0]]
625 complex inputs match independent coordinate formulas.
Active/passive, adjoint/inverse, and dependent-column checks passed.
```

The output's `B` names the new matrix, which the prose calls $A_B$; its `Q^H` means the adjoint $Q^\dagger$. The 625 test inputs use real and imaginary parts in $-2,-1,0,1,2$ for both coordinates. Solver results are compared with the independent formulas using zero relative tolerance and $10^{-12}$ absolute tolerance. Additional cases check the complex orthonormal conversion and reject an exactly dependent column set. Nearly dependent bases need conditioning analysis; a solver returning numbers is not a guarantee of accurate coordinates. That numerical limitation is separate from the exact invertibility assumption.

### Transfer and debugging

**2.3-B — Rescale one basis vector.** Replace the new basis by $b_1=2e_1$, $b_2=e_2$. Derive the new representation of the swap map, and verify its action on $x=(2,3)$ by reconstructing the output.

**2.3-C — Explain the failed adjoint shortcut.** Why does $S^\dagger AS$ fail for the nonorthogonal example? Would real entries alone justify replacing inverse by transpose?

**2.3-D — Check the basis assumption.** Consider columns $(1,0)$ and $(2,0)$. Which basis condition fails, and can every old coordinate column be converted to a unique new column?

**2.3-E — Distinguish a map from its representation.** A colleague changes both coordinates and matrix using the proved rule, then says the vector and physical device have changed. Which conclusion follows from the algebra, and which needs additional evidence?

**Answers and reasoning**

- **A.** The images are $e_2$ and $e_1$, giving $A=\begin{pmatrix}0&1\\1&0\end{pmatrix}$. Multiplying $A$ by coordinate column $e_j$ selects column $j$, so its entries must represent the image of that input basis vector.
- **B.** Here $S=\begin{pmatrix}2&0\\0&1\end{pmatrix}$ and $A_B=\begin{pmatrix}0&1/2\\2&0\end{pmatrix}$. Input $x$ becomes $y=(1,3)$, which maps to $(3/2,2)$; reconstructing gives $(3,2)$.
- **C.** The columns are not orthonormal, so $S^\dagger S\ne I$ and $S^\dagger\ne S^{-1}$. Real entries make adjoint equal transpose, but do not make either equal inverse. Orthogonality and normalization, not reality alone, justify that shortcut.
- **D.** The columns are dependent because $2(1,0)-(2,0)=0$, and they do not span $\mathbb C^2$. For instance $(0,1)$ has no expansion; $(1,0)$ has multiple expansions. Thus a unique conversion for every column is impossible.
- **E.** A consistent passive change preserves the vector and the linear transformation, while changing their coordinate representations. No physical-device modification or execution follows from this algebra. Such a claim needs its own operational meaning and evidence.

Next, [2.4 Hermitian, unitary, and positive operators](#sec-complex-vectors-operators-and-numerical-reasoning-4) develops operator properties whose definitions must be distinguished from a particular displayed matrix.

### Source, status, and limits

Assigned companion source: [NC:2.1.2](../references/proof-sources.md#source-nc-2-1-2), Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010), §2.1.2, printed pp. 63–64. Those pages, including the preceding basis discussion, were consulted from the previously supplied local copy. They support the linear-map and matrix-representation conventions. The coordinate-conversion derivation, nonorthogonal and complex-basis checks, active/passive distinction and exercises here provide original worked exposition, rather than attributing every displayed identity to that subsection.

Depth **F**: derive similarity from coordinate conversion, justify invertibility from the basis assumptions, and prove the orthonormal adjoint shortcut. [The section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/2.3.json) separates author execution from pending independent mathematical, implementation and reader reviews. Numerical checks validate the bounded implementations, not the general theorem or any quantum hardware behavior.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-4"></span>

## 2.4 Hermitian, unitary, and positive operators

A matrix can equal its adjoint, preserve lengths, or give nonnegative quadratic forms. These are different requirements. Confusing them can turn a valid matrix calculation into an invalid interpretation of an observable, a transformation or a probability model. We first establish the algebra, before assigning physical roles in later chapters.

The prerequisite is [2.3](#sec-complex-vectors-operators-and-numerical-reasoning-3), including its distinction between a linear map and its coordinates. All matrix formulas below use a fixed **orthonormal basis** and the standard inner product, conjugate linear in its first argument. Operators act on the same finite-dimensional complex inner product space as their output space. No spectral decomposition is assumed.

### Definitions that do different work

For a square matrix $A$, its adjoint $A^\dagger$ is the conjugate transpose. Conjugating twice and exchanging indices twice returns $A$, so $(A^\dagger)^\dagger=A$. Adjoint also distributes over addition, and conjugates scalar coefficients: these facts follow entry by entry from 2.1.

An operator $H$ is **Hermitian**, or **self-adjoint**, when $H^\dagger=H$. An operator $U$ is **unitary** when $U^\dagger U=UU^\dagger=I$. The identity $I$ leaves each vector unchanged. Section 2.3 introduced this unitary criterion for changes between orthonormal bases; here we study its effect when $U$ acts on vectors.

For any $A$, define its **quadratic form** at $v$ by the scalar

$$
q_A(v)=\langle v,Av\rangle=v^\dagger Av.
$$

We call $A$ **positive semidefinite**, written $A\succeq0$, when $q_A(v)$ is real and nonnegative for every vector $v$. “Positive” without a qualifier means semidefinite in this book. It does not mean that every matrix entry is positive. We call $A$ **positive definite** when the same form is strictly positive for every nonzero $v$. The zero vector always gives zero and must be excluded from the strict condition.

We will prove that these positivity definitions imply Hermiticity. A complex scalar has no ordinary ordering compatible with comparing it to zero in this definition; the word **real** is an essential part of the condition.

### Hermitian operators give real quadratic forms

Conjugate symmetry and the adjoint identity from 2.2 give

$$
\begin{aligned}
q_H(v)^*
 &=\langle Hv,v\rangle\\
 &=\langle v,H^\dagger v\rangle\\
 &=\langle v,Hv\rangle=q_H(v).
\end{aligned}
$$

The middle equality follows by applying the adjoint identity to $H^\dagger$ and using its double adjoint. A scalar equals its conjugate exactly when its imaginary part is zero, so $q_H(v)$ is real. This alone imposes no sign on it.

An **eigenpair** consists of a scalar $\lambda$ and a **nonzero** vector $v$ such that $Av=\lambda v$. The scalar is an eigenvalue and $v$ an eigenvector. The nonzero requirement prevents the meaningless identity $A0=\lambda0$ from making every scalar an eigenvalue.

If $H$ is Hermitian and $Hv=\lambda v$, linearity in the second argument gives

$$
q_H(v)=\langle v,\lambda v\rangle
       =\lambda\|v\|^2.
$$

The left side is real, and $\|v\|^2>0$. Dividing by this positive real number proves that $\lambda$ is real. This argument applies to every eigenpair, but does not yet construct a complete eigenbasis. That existence result belongs to 2.5.

### Why the quadratic-form condition forces Hermiticity

We now prove the converse fact needed for positivity: if $q_A(v)$ is real for every complex vector $v$, then $A$ is Hermitian. Define $D=A-A^\dagger$. By the same adjoint identity,

$$
v^\dagger Dv=q_A(v)-q_A(v)^*=0
$$

for every $v$. Let $e_j$ be the coordinate column with a 1 at position $j$ and zeros elsewhere. Taking $v=e_j$ gives $D_{jj}=0$. For distinct indices $j,k$, use two further probes:

$$
\begin{aligned}
(e_j+e_k)^\dagger D(e_j+e_k)&=D_{jk}+D_{kj}=0,\\
(e_j+i e_k)^\dagger D(e_j+i e_k)&=iD_{jk}-iD_{kj}=0.
\end{aligned}
$$

The diagonal terms vanished by the first probe. The two remaining equations imply $D_{jk}=-D_{kj}$ and $D_{jk}=D_{kj}$, hence both entries are zero. All diagonal and off-diagonal entries of $D$ therefore vanish, so $A=A^\dagger$.

Thus a real, nonnegative quadratic form for all vectors implies Hermiticity as well as the sign condition. Equivalently, one may define positive semidefiniteness as **Hermitian plus nonnegative quadratic form**. The argument is algebraic for arbitrary finite dimension; it is not a claim that a collection of randomly sampled forms establishes the condition for all vectors. Probing only real vectors would also omit the crucial $i e_k$ information.

For a positive semidefinite $A$, any eigenpair satisfies $\lambda\|v\|^2=q_A(v)\ge0$, so $\lambda\ge0$. For a positive definite $A$, the inequality is strict. The reverse implication from nonnegative eigenvalues will be justified for Hermitian operators using the spectral theorem in 2.5; we do not import that theorem here.

A useful sufficient construction avoids it. If $C$ is any finite rectangular matrix, then

$$
q_{C^\dagger C}(v)=\langle v,C^\dagger Cv\rangle
                 =\langle Cv,Cv\rangle=\|Cv\|^2\ge0.
$$

The value is real, so the preceding proof also makes $C^\dagger C$ Hermitian and positive semidefinite. It is positive definite exactly when $Cv=0$ forces $v=0$. Both directions follow because a squared norm vanishes exactly at the zero vector.

### Unitary operators preserve overlaps and norms

For unitary $U$, the adjoint identity yields

$$
\begin{aligned}
\langle Uv,Uw\rangle
 &=\langle v,U^\dagger Uw\rangle\\
 &=\langle v,Iw\rangle=\langle v,w\rangle.
\end{aligned}
$$

Setting $w=v$ proves $\|Uv\|^2=\|v\|^2$, hence $\|Uv\|=\|v\|$ by nonnegative square roots. This is stronger than checking the length of one test vector: it preserves every pair's inner product.

If $Uv=\lambda v$ with $v\ne0$, then norm scaling from 2.2 gives $\|v\|=\|Uv\|=\lvert\lambda\rvert\|v\|$. Dividing by the positive norm proves $\lvert\lambda\rvert=1$. An eigenvalue of a unitary operator need not be real. Hermiticity and unitarity constrain different aspects of an eigenvalue.

**2.4-A — Predict before testing.** Can an eigenvalue 3 belong to a Hermitian operator? A positive definite operator? A unitary operator? State which proved condition supports each answer.

### One positive definite matrix that stretches a vector

Consider the complex matrix

$$
H=\begin{pmatrix}2&i\\-i&2\end{pmatrix}.
$$

Conjugate transpose returns the same matrix. For $v=(a,b)$ as a column, direct expansion gives

$$
\begin{aligned}
q_H(v)
 &=2\lvert a\rvert^2+2\lvert b\rvert^2+i a^*b-i b^*a\\
 &=\lvert a+i b\rvert^2+\lvert a\rvert^2+\lvert b\rvert^2.
\end{aligned}
$$

The second equality follows by multiplying $(a+i b)^*(a+i b)=(a^*-i b^*)(a+i b)$. Every term is nonnegative. If $v\ne0$, at least one of $\lvert a\rvert^2,\lvert b\rvert^2$ is positive, proving positive definiteness for all vectors without sampling or diagonalization.

Two explicit eigenpair checks are

$$
H\begin{pmatrix}1\\i\end{pmatrix}=\begin{pmatrix}1\\i\end{pmatrix},\qquad
H\begin{pmatrix}1\\-i\end{pmatrix}=3\begin{pmatrix}1\\-i\end{pmatrix}.
$$

The eigenvalues 1 and 3 are consistent with Hermiticity and positive definiteness. Yet $He_1=(2,-i)$ has squared norm 5, whereas $e_1=(1,0)$ has squared norm 1. Thus $H$ is not unitary. Real, positive quadratic forms do not require norm preservation.

For an independent coordinate reference, write $a=a_r+i a_i$ and $b=b_r+i b_i$, with real subscripts denoting parts. Since $a+i b=(a_r-b_i)+i(a_i+b_r)$, the form becomes

$$
q_H(v)=(a_r-b_i)^2+(a_i+b_r)^2+a_r^2+a_i^2+b_r^2+b_i^2.
$$

The program checks this real-arithmetic expression against the tensor quadratic form.

### Counterexamples that separate the classes

Here are three further operators in standard orthonormal coordinates:

$$
U=\begin{pmatrix}1&0\\0&i\end{pmatrix},\quad
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\quad
P=\begin{pmatrix}1&0\\0&0\end{pmatrix}.
$$

For $v=(a,b)$, $Uv=(a,ib)$ has the same squared norm as $v$, and direct multiplication gives $U^\dagger U=UU^\dagger=I$. But $U^\dagger=\operatorname{diag}(1,-i)\ne U$, and $q_U(e_2)=i$ is not real. Here $\operatorname{diag}$ names the matrix with the listed diagonal entries and zeros elsewhere.

Both $Z^\dagger=Z$ and $Z^\dagger Z=ZZ^\dagger=I$ hold, so $Z$ is simultaneously Hermitian and unitary. Nevertheless $q_Z(e_2)=-1$, refuting positivity. For $P$, $q_P(v)=\lvert a\rvert^2\ge0$, so $P$ is positive semidefinite. It is not positive definite because the nonzero vector $e_2$ gives zero. It is not unitary because it maps that vector to zero. This $P$ is also the orthogonal projection onto the first coordinate line, connecting to 2.2.

| Operator | Hermitian | Unitary | Positive semidefinite | Positive definite |
|---|---|---|---|---|
| $H$ above | Yes | No | Yes | Yes |
| $U=\operatorname{diag}(1,i)$ | No | Yes | No | No |
| $Z=\operatorname{diag}(1,-1)$ | Yes | Yes | No | No |
| $P=\operatorname{diag}(1,0)$ | Yes | No | Yes | No |

A final warning concerns eigenvalues without Hermiticity. Let

$$
N=\begin{pmatrix}0&1\\0&0\end{pmatrix}.
$$

For an eigenpair $N(x,y)=\lambda(x,y)$, the coordinate equations are $y=\lambda x$ and $0=\lambda y$. If $\lambda\ne0$, they force $y=x=0$, contradicting the nonzero eigenvector requirement. The value 0 does occur, with eigenvector $e_1$, so it is the only eigenvalue. Yet $q_N((1,-1))=-1$, and $q_N((1,i))=i$. Thus nonnegative eigenvalues alone do not establish positivity for an arbitrary non-Hermitian matrix.

### Formula to executable evidence

The [complete program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/operator_classes.py) uses Python 3.12, PyTorch 2.13.0, CPU `complex128`. It supplies eigenvectors and eigenvalues from the hand calculations; an eigensolver is not the source of its expected results.

| Claim or test | Tensor calculation | Independent evidence |
|---|---|---|
| Hermiticity | Compare `h.mH` with `h` | Conjugate the displayed entries and transpose |
| Unitarity | Compare `u.mH @ u` and `u @ u.mH` with identity | The diagonal products are 1 and $(-i)i=1$ |
| Positive definite $H$ | `torch.vdot(v, h @ v)` | Explicit six-square expression in real coordinates |
| Norm preservation for $U$ | `torch.vdot(u @ v, u @ v)` | $\lvert a\rvert^2+\lvert ib\rvert^2=\lvert a\rvert^2+\lvert b\rvert^2$ |
| Supplied eigenpair | Norm of `matrix @ v - value*v` | Nonzero, explicit eigenvectors and scalar products above |
| Invalid implications | Evaluate forms at the stated witnesses | Negative, zero or non-real values diagnose the exact failed condition |

Run from the repository root in the existing pinned example environment:

```bash
python -m pip install -r requirements-examples.txt
python examples/foundations/operator_classes.py
```

Expected output:

```text
CPU complex128 checks; algebraic models only.
H: Hermitian and positive definite; squared norm of H*e1=5, not 1
U=diag(1,i): unitary, not Hermitian; quadratic form at e2=i
Z=diag(1,-1): Hermitian and unitary, not positive; form at e2=-1
P=diag(1,0): positive semidefinite, not positive definite; form at e2=0
N=[[0,1],[0,0]]: N^2=0; forms -1 and i refute positivity
5 supplied nonzero eigenvectors: maximum residual=0.0e+00
625 vectors match independent H/U/P coordinate formulas.
Defining identities and counterexamples passed; sampled forms are not a proof.
```

The 625 vectors use real and imaginary coordinates from $-2$ to $2$. Tensor comparisons use zero relative tolerance and $10^{-12}$ absolute tolerance; the supplied eigenpair residuals must also be at most $10^{-12}$. A small residual checks that particular nonzero vector and candidate eigenvalue. It does not establish a complete eigenbasis or a universal property of a different operator. Likewise, a finite set of nonnegative sampled forms is not a positivity certificate. The proofs above, including the explicit all-vector expression for $H$, supply the general claims.

FlagQuantum is not needed for these linear-algebra reference checks. No circuit, quantum measurement or hardware execution is claimed.

### Coordinate and numerical boundaries

The simple tests $A^\dagger=A$ and $U^\dagger U=I$ assume orthonormal coordinates. An operator may acquire a matrix that is not equal to its ordinary conjugate transpose when expressed in a nonorthonormal basis. For example, the swap map in 2.3 is Hermitian in standard coordinates, but its nonorthogonal-basis matrix $\begin{pmatrix}-1&0\\1&1\end{pmatrix}$ is not equal to its plain conjugate transpose. This is a representation issue, not a changed operator. The Gram-weighted inner product from 2.3 must be retained in that coordinate system.

Numerically, an approximate equality within a chosen tolerance differs from an exact identity. A form slightly below zero near the rounding scale requires an error analysis, not an automatic declaration of either positivity or a physical inconsistency. This section uses small exact entries and explicitly scoped checks; conditioning and robust numerical diagnostics follow later.

### Transfer and diagnosis

**2.4-B — Positive entries?** Consider $M=\begin{pmatrix}1&2\\2&1\end{pmatrix}$. All entries are positive. Evaluate its form at $(1,-1)$ and decide whether that establishes positive semidefiniteness or refutes it.

**2.4-C — Zero versus strict positivity.** Why does $q_P(e_2)=0$ refute positive definiteness but not positive semidefiniteness? Why is it insufficient to test only $e_1$?

**2.4-D — Sampling as a claim.** A program tests 100 vectors, obtains real nonnegative forms and declares an unfamiliar matrix positive. Which quantifier has not been justified? What would a verified factorization $A=C^\dagger C$ establish instead?

**2.4-E — A representation trap.** A colleague uses the nonorthogonal basis from 2.3, finds a nonsymmetric representation of the swap and declares the underlying map non-Hermitian. Identify the missing coordinate assumption.

**Answers and reasoning**

- **A.** Yes for Hermitian and positive definite operators: the displayed $H$ has eigenvalue 3. No for a unitary operator, whose eigenvalues must have modulus 1.
- **B.** $M(1,-1)=(-1,1)$ and the quadratic form is $-2$. This one counterexample refutes the all-vector nonnegativity condition. Entrywise positivity is a different property.
- **C.** Strict positivity requires a positive value at every nonzero vector, and $e_2\ne0$. Semidefiniteness permits zero. Testing $e_1$ alone misses a different direction in which the form vanishes.
- **D.** “For every vector” has not been established by those finite samples. An exact, verified factorization gives $q_A(v)=\|Cv\|^2\ge0$ for all $v$, proving positive semidefiniteness. Strict positivity additionally requires that $Cv=0$ only for $v=0$.
- **E.** Ordinary conjugate-transpose tests represent the adjoint in orthonormal coordinates. That assumption fails for the chosen basis; use its Gram-weighted inner product or convert back consistently before applying those tests.

The next lesson, [2.5 Spectral decomposition and singular values](#sec-complex-vectors-operators-and-numerical-reasoning-5), builds the decomposition results needed to turn suitable eigenvalue information into complete operator statements.

### Source, status, and limits

Assigned companion source: [NC:2.1.6](../references/proof-sources.md#source-nc-2-1-6), Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010), §2.1.6, printed pp. 69–71. Those pages were consulted from the previously supplied local copy. They supply the adjoint, Hermitian, unitary and positivity conventions. The proofs here explicitly supply the quadratic-form implication and all-vector worked forms without assuming the spectral theorem or importing an external exercise as a missing step. Examples, counterexamples and answer explanations are original exposition.

Depth **F**: prove real Hermitian eigenvalues, the real nonnegative quadratic-form condition and unitary norm preservation, with assumptions and boundary cases stated. [The section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/2.4.json) distinguishes author checks from pending independent mathematical, implementation and reader review. Physical meanings are developed in their later owning sections.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-5"></span>

## 2.5 Spectral decomposition and singular values

Knowing that every Hermitian eigenvalue is real does not yet tell us that enough eigenvectors exist to reconstruct the operator. Knowing several numerical eigenpairs does not fill that gap either. This section proves the missing existence and completeness results, then uses them to construct a decomposition for any rectangular complex matrix, including its zero directions.

The prerequisite is [2.4](#sec-complex-vectors-operators-and-numerical-reasoning-4). We use its Hermitian real forms, positive Gram forms and inner-product conventions. Coordinate bases are orthonormal throughout. We supply the needed finite-dimensional compactness and basis-completion arguments locally, without assuming a spectral theorem in its own proof.

### A finite orthonormal-completion bridge

Start with an orthonormal list $q_1,\ldots,q_k$ in $\mathbb C^n$, possibly empty. For any vector $x$, remove its components along the list:

$$
r=x-\sum_{j=1}^k q_j\langle q_j,x\rangle.
$$

Taking the inner product with $q_\ell$ leaves $\langle q_\ell,x\rangle-\langle q_\ell,x\rangle=0$, because all other overlaps vanish. If $r\ne0$, append $r/\|r\|$; it is a unit vector orthogonal to the whole list. If $r=0$, $x$ was already in its span. This proves the step used in the **Gram–Schmidt** construction, including its zero-residual decision.

Apply the step successively to standard coordinate vectors $e_1,\ldots,e_n$, starting with the given list. The resulting finite list spans every $e_j$ and hence the space. It remains orthonormal and is independent: taking an inner product with each list member in a zero linear combination forces its coefficient to vanish.

Here is also an explicit count, so dimension is not hidden in that argument. For any orthonormal list of length $k$, its residuals for the standard vectors satisfy

$$
\sum_{j=1}^n\left\|e_j-\sum_{\ell=1}^k q_\ell\langle q_\ell,e_j\rangle\right\|^2
 =n-\sum_{\ell=1}^k\sum_{j=1}^n\lvert\langle q_\ell,e_j\rangle\rvert^2=n-k.
$$

The first equality follows by the orthogonal squared-length decomposition from 2.2; each $e_j$ has squared length 1. The inner sum is $\|q_\ell\|^2=1$. Nonnegativity gives $k\le n$. For a spanning list all residuals vanish, giving $k=n$. Thus a unit vector can be completed to an orthonormal basis of exactly $n$ members. The remaining $n-1$ members span its orthogonal complement: in the basis expansion, orthogonality forces the first coefficient to be zero.

### Why a Hermitian quadratic form attains a maximum

For Hermitian $H\in\mathbb C^{n\times n}$, consider $q_H(x)=x^\dagger Hx$ on the unit sphere $\|x\|=1$. It is real by 2.4. For nonzero vectors, the ratio $q_H(x)/\|x\|^2$ is called the **Rayleigh quotient**; restricting to unit vectors removes its denominator.

We need an attained maximum, not merely a numerical search. Identify $\mathbb C^n$ with $\mathbb R^{2n}$ using real and imaginary coordinates. A sequence of unit vectors has bounded real coordinates. Every bounded real sequence has a convergent subsequence: repeatedly bisect a bounding interval, keep a closed half containing infinitely many terms, and choose terms with increasing indices in these nested halves. Their lengths tend to zero and real-number completeness gives the common limit. Applying this argument to each of the finitely many coordinates, extracting subsequences successively, gives a subsequence converging in all coordinates. Its norm is still 1, since the finite sum of squared moduli is continuous.

The form $q_H$ is also continuous: it is a finite sum of products of coordinates and fixed entries. It is bounded on the unit sphere, for example

$$
\lvert q_H(x)\rvert\le\sum_{j,k}\lvert H_{jk}\rvert,
$$

because every coordinate has modulus at most 1 and the scalar triangle inequality bounds the finite sum. The sphere is nonempty for $n\ge1$. By the least-upper-bound property of the real numbers, its real form values have a supremum $\lambda$. Choose unit vectors whose values approach this supremum, with the $s$th value greater than $\lambda-1/s$. The convergent subsequence just constructed has a unit limit $u$. Continuity gives $q_H(u)=\lambda$. This is the finite compactness/maximum argument needed below. It uses completeness of the real numbers, not eigenvalue existence, determinants or diagonalization.

### A maximizing vector is an eigenvector

Let $u$ be that maximizing unit vector, and take any $w$ with $\langle u,w\rangle=0$. For a real number $t$, the vector

$$
x(t)=\frac{u+tw}{\sqrt{1+t^2\|w\|^2}}
$$

has unit norm by orthogonality. Expand its quadratic form and use $q_H(x(t))\le\lambda=q_H(u)$:

$$
2t\operatorname{Re}\langle u,Hw\rangle
+t^2\bigl(q_H(w)-\lambda\|w\|^2\bigr)\le0.
$$

This expansion uses $\langle w,Hu\rangle=\langle u,Hw\rangle^*$ from Hermiticity. The coefficient of $t$ must be zero. To see the contradiction explicitly, let $b=\operatorname{Re}\langle u,Hw\rangle$ and $d=q_H(w)-\lambda\|w\|^2$, both real. If $b\ne0$, choose $t$ with the same sign as $b$ and $0<\lvert t\rvert<\lvert b\rvert/(\lvert d\rvert+1)$. Then $2tb+t^2d\ge\lvert t\rvert(2\lvert b\rvert-\lvert t\rvert\lvert d\rvert)>0$, contradicting the inequality. Thus $\operatorname{Re}\langle u,Hw\rangle=0$.

The vector $iw$ is also orthogonal to $u$. Repeating the argument with it makes $\operatorname{Re}(i\langle u,Hw\rangle)=-\operatorname{Im}\langle u,Hw\rangle$ zero. Both parts vanish, so $\langle u,Hw\rangle=\langle w,Hu\rangle=0$ for every $w$ orthogonal to $u$.

Set $r=Hu-\lambda u$. Since $\langle u,r\rangle=q_H(u)-\lambda=0$, the preceding result applies with $w=r$. It gives

$$
0=\langle r,Hu\rangle
 =\langle r,\lambda u+r\rangle=\|r\|^2.
$$

Positive definiteness forces $r=0$. Hence $Hu=\lambda u$ with $u\ne0$: an eigenpair has been constructed rather than assumed.

### Hermitian spectral theorem by induction

We can now state and prove the finite **Hermitian spectral theorem**: every Hermitian $H$ on $\mathbb C^n$ has an orthonormal basis of eigenvectors with real eigenvalues.

For $n=1$, a Hermitian scalar is real and its unit coordinate vector is an eigenvector. For $n>1$, construct $u$ as above. Its orthogonal complement is invariant under $H$: if $w$ is orthogonal to $u$, then

$$
\langle u,Hw\rangle=\langle Hu,w\rangle
 =\langle\lambda u,w\rangle=\lambda\langle u,w\rangle=0,
$$

where $\lambda$ is real by 2.4. The restriction of $H$ to this complement is Hermitian, since its inner-product adjoint identity holds for every pair of vectors in the complement. The completion bridge provides orthonormal coordinates of dimension $n-1$ there. Apply the induction hypothesis to that restriction, and append $u$ to its orthonormal eigenbasis. This yields $n$ eigenvectors spanning the original space, completing the proof.

Let the resulting columns be $q_1,\ldots,q_n$ with eigenvalues $\lambda_1,\ldots,\lambda_n$. Put them into a unitary matrix $Q$, and let $\Lambda$ be the diagonal matrix with those eigenvalues. The column equations $Hq_j=\lambda_jq_j$ give

$$
HQ=Q\Lambda,\qquad H=Q\Lambda Q^\dagger
 =\sum_{j=1}^n\lambda_j q_jq_j^\dagger.
$$

Here $q_jq_j^\dagger$ denotes an outer-product matrix, acting on $x$ as $q_j\langle q_j,x\rangle$. Because the columns are an orthonormal basis, $x=\sum_j q_j\langle q_j,x\rangle$; applying $H$ gives precisely the reconstruction formula.

If eigenvalues coincide, the individual eigenvectors are not uniquely determined. For each distinct value $\lambda$, group its orthonormal eigenvectors into

$$
P_\lambda=\sum_{j:\lambda_j=\lambda}q_jq_j^\dagger,\qquad
H=\sum_\lambda\lambda P_\lambda.
$$

The product of outer products is $q_j(q_j^\dagger q_k)q_k^\dagger$, so orthonormality gives $P_\lambda^2=P_\lambda$, $P_\lambda^\dagger=P_\lambda$, mutually zero products for distinct values, and $\sum_\lambda P_\lambda=I$. The projector is independent of the chosen orthonormal basis within that eigenspace: it is the identity on that subspace and zero on its orthogonal complement. Rotating a degenerate eigenbasis changes columns but not this action.

The spectral theorem now closes the positivity converse left open in 2.4. For $x=\sum_j c_jq_j$,

$$
q_H(x)=\sum_j\lambda_j\lvert c_j\rvert^2.
$$

If all eigenvalues are nonnegative, every term is nonnegative, so $H\succeq0$. Combined with 2.4's necessary direction, a Hermitian matrix is positive semidefinite exactly when all its eigenvalues are nonnegative. Strict positivity is equivalent to all eigenvalues being strictly positive: this expression is positive at any nonzero coefficient column, whereas a zero or negative eigenvalue supplies an eigenvector violating strict positivity.

**2.5-A — Identify the missing premise.** Does a list of real nonnegative eigenvalues make an arbitrary square matrix positive semidefinite? Which premise enabled the displayed all-vector expansion?

### Construct an SVD for a rectangular complex matrix

Let $A\in\mathbb C^{m\times n}$, with positive integers $m,n$. The Gram matrix $G=A^\dagger A$ is $n$-by-$n$ and positive semidefinite by 2.4. Its spectral theorem provides an orthonormal basis $v_1,\ldots,v_n$ and eigenvalues $\mu_i\ge0$. Reorder so the positive ones come first, in decreasing order. Let $r$ be their number and set $\sigma_i=\sqrt{\mu_i}>0$ for $1\le i\le r$. These are the positive **singular values** of $A$.

For positive indices define output vectors

$$
u_i=\frac{Av_i}{\sigma_i}.
$$

They are orthonormal, because

$$
\langle u_i,u_j\rangle
 =\frac{\langle Av_i,Av_j\rangle}{\sigma_i\sigma_j}
 =\frac{\langle v_i,Gv_j\rangle}{\sigma_i\sigma_j}
 =\frac{\mu_j\langle v_i,v_j\rangle}{\sigma_i\sigma_j}.
$$

This is 1 when $i=j$ and 0 otherwise. The completion bridge implies $r\le m$ and extends these vectors to an orthonormal basis $u_1,\ldots,u_m$ of the output space. No division by a zero singular value has occurred.

For $i>r$, $\mu_i=0$ and

$$
\|Av_i\|^2=\langle v_i,Gv_i\rangle=0,
$$

so $Av_i=0$. These right-side directions must be retained as kernel directions, not normalized by an undefined $1/0$.

Form unitary matrices $U$ with the $m$ output columns and $V$ with the $n$ input columns. Define $\Sigma\in\mathbb R^{m\times n}$ to have $\sigma_i$ at diagonal position $(i,i)$ for $i\le r$ and zero everywhere else. Its diagonal has $\min(m,n)$ positions, with any additional singular values set to zero. The action on every input basis column now agrees:

$$
Av_i=U\Sigma e_i\quad(1\le i\le n).
$$

For $i\le r$ both sides equal $\sigma_i u_i$; for $i>r$ both are zero, including indices beyond the rectangular diagonal. Thus

$$
AV=U\Sigma,\qquad A=U\Sigma V^\dagger.
$$

This is the **full singular-value decomposition**, or SVD. It holds whether $A$ is square, rectangular, invertible, rank deficient or zero. For $A=0$, take any orthonormal input and output bases and $\Sigma=0$; the construction needs no positive singular vector.

The **kernel** is the set of inputs mapped to zero; the **image** is the set of attainable outputs. To identify them completely, expand any input as $x=\sum_i c_iv_i$. The orthonormal output vectors give

$$
Ax=\sum_{i=1}^r\sigma_i c_i u_i,\qquad
\|Ax\|^2=\sum_{i=1}^r\sigma_i^2\lvert c_i\rvert^2.
$$

The second expression vanishes exactly when all $c_i$ with $i\le r$ vanish. Hence the kernel is spanned by $v_{r+1},\ldots,v_n$, and has dimension $n-r$. The image is spanned by $u_1,\ldots,u_r$: each is attained using $v_i/\sigma_i$, and the expansion shows there are no other image directions. Its dimension $r$ is the **rank**. Output basis vectors $u_{r+1},\ldots,u_m$ are orthogonal to the image. This accounts for both sides when $m\ne n$. The unused output subspace is also the kernel of $A^\dagger$: if $u$ is orthogonal to every $Ax$, then $\langle x,A^\dagger u\rangle=\langle Ax,u\rangle=0$ for every $x$. Choosing $x=A^\dagger u$ forces $A^\dagger u=0$. Conversely that zero equation makes $u$ orthogonal to every output by the same identity.

A reduced SVD keeps fewer columns, which can be enough for reconstructing $A$. It may omit right-kernel or unused output directions; it must not be mistaken for a full basis of both spaces.

### Eigenvalues and singular values answer different questions

For Hermitian $H=Q\Lambda Q^\dagger$, $H^\dagger H=H^2$ sends $q_j$ to $\lambda_j^2q_j$. Therefore its singular values are the numbers $\lvert\lambda_j\rvert$, reordered and counted with multiplicity. They discard negative signs. For a unitary square matrix, $U^\dagger U=I$, so every singular value is 1.

For a general square matrix, singular values are not the moduli of its eigenvalues. The matrix $N=\begin{pmatrix}0&1\\0&0\end{pmatrix}$ from 2.4 has only eigenvalue 0, but $N^\dagger N=\operatorname{diag}(0,1)$ gives singular values 1 and 0. It maps $e_2$ to $e_1$ rather than annihilating every input. Eigenvectors describe preserved directions up to scalar multiplication; singular vectors describe orthonormal input-output directions and their scaling. Rectangular matrices also have an SVD, even though an eigenvalue equation between different input and output dimensions has no such meaning.

### Work both decompositions before calling a solver

For the previous section's Hermitian example,

$$
H=\begin{pmatrix}2&i\\-i&2\end{pmatrix},\quad
Q=\frac1{\sqrt2}\begin{pmatrix}1&1\\i&-i\end{pmatrix},\quad
\Lambda=\begin{pmatrix}1&0\\0&3\end{pmatrix}.
$$

Section 2.4 checked the two eigenpairs; 2.3 checked these columns are orthonormal. Multiplying $Q\Lambda Q^\dagger$ reconstructs $H$. The numerical check compares each rank-one projector with the hand-derived one, rather than requiring an eigensolver to choose identical phases.

For a rectangular case, take

$$
A=\begin{pmatrix}3&0&0\\0&0&4i\end{pmatrix},\qquad
A^\dagger A=\begin{pmatrix}9&0&0\\0&0&0\\0&0&16\end{pmatrix}.
$$

The right singular basis in decreasing positive order is $v_1=e_3$, $v_2=e_1$, $v_3=e_2$. Applying $A$ and dividing by 4 and 3 gives $u_1=i e_2$ and $u_2=e_1$. Thus explicit full factors are

$$
U=\begin{pmatrix}0&1\\i&0\end{pmatrix},\quad
\Sigma=\begin{pmatrix}4&0&0\\0&3&0\end{pmatrix},\quad
V=\begin{pmatrix}0&1&0\\0&0&1\\1&0&0\end{pmatrix}.
$$

Their product $U\Sigma V^\dagger$ returns $A$. The two listed singular values are 4 and 3, although the right Gram matrix has three eigenvalues. The extra zero appears through the third right basis vector and the zero column of $\Sigma$. Its kernel is exactly $\operatorname{span}(e_2)$, meaning all complex multiples of $e_2$; its image is all of $\mathbb C^2$.

For any input $x=(a,b,c)$, an independent direct reference is

$$
Ax=\begin{pmatrix}3a\\4ic\end{pmatrix},\qquad
\|Ax\|^2=9\lvert a\rvert^2+16\lvert c\rvert^2.
$$

The coordinate $b$ never affects the output, independently confirming the kernel direction.

### Formula to code, with explicit factor dimensions

The [complete program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/spectral_svd.py) targets Python 3.12 and PyTorch 2.13.0, CPU `complex128`.

| Mathematical object or check | Tensor operation | Independent evidence |
|---|---|---|
| Hermitian eigendecomposition | `torch.linalg.eigh(h)` | Hand eigenvalues 1, 3 and rank-one projectors from $Q$ |
| Spectral reconstruction | `vectors @ diag(values) @ vectors.mH` | Explicit $H$ and column eigenpair residuals |
| Full rectangular SVD | `torch.linalg.svd(a, full_matrices=True)` | Explicit full $U,\Sigma,V$ above |
| Right adjoint | Returned `vh` is $V^\dagger$ | Reconstruct with `u @ sigma_numeric @ vh` |
| Right kernel | Third column of `vh.mH` | Projector onto $e_2$ and zero output |
| Direct action | Reconstructed factors applied to each input | Real/imaginary coordinate formula for $(3a,4ic)$ |
| Degeneracy and zero | Compare projectors and reconstructed operators | A rotated eigenbasis of $\operatorname{diag}(2,2,0)$ and the zero 3-by-2 map |

For a 2-by-3 input with full factors, `u` is 2-by-2, `vh` is 3-by-3 and the returned singular-value vector has length 2. The program inserts those entries into a separate 2-by-3 zero array to build $\Sigma$. Multiplying by a 2-by-2 diagonal array alone would lose the third input coordinate in the full-factor expression.

Run in the existing pinned example environment:

```bash
python -m pip install -r requirements-examples.txt
python examples/foundations/spectral_svd.py
```

Expected output:

```text
CPU complex128; reconstruction and subspace checks, no quantum execution.
Hermitian H: eigenvalues [1,3]; analytic eigenprojectors and reconstruction agree
Rectangular A (2x3): singular values [4,3]; full factor shapes U=2x2, Sigma=2x3, V^H=3x3
Right kernel: span(e2); full V retains the direction omitted by a reduced SVD
SVD reconstruction Frobenius residual <= 1e-12: True
729 inputs match direct three-coordinate formulas.
Degenerate eigenspace projector and all-zero rectangular kernel checks passed.
Nilpotent N: only eigenvalue 0 (proved in text), singular values [1,0]
Missing right adjoint detected with a complex right basis; no phase matching required.
```

The 729 inputs have three complex coordinates, each real and imaginary part in $-1,0,1$. Comparisons use zero relative tolerance and $10^{-12}$ absolute tolerance. The **Frobenius residual** is the square root of the sum of squared moduli of all entries of the reconstructed matrix minus $A$. It checks reconstruction on this bounded example, not the existence theorem.

The main example's $V$ is real, so replacing its adjoint by transpose would accidentally pass. The program therefore also constructs a complex right basis, multiplying the first coordinate row of $V$ by $i$. It checks that using transpose instead of adjoint then fails. Further cases check a rotated degenerate eigenspace projector and a zero rectangular map whose entire input space is kernel. Neither arbitrary phases nor a solver's choice of basis within a degenerate subspace should be treated as a correctness failure.

No FlagQuantum API or quantum hardware execution is needed for this mathematical reference. In floating point, a very small singular value is not automatically an exact zero. Choosing a numerical rank threshold needs scale and error information, addressed in later numerical reasoning; no universal threshold is inferred here.

### Transfer, proof diagnosis, and answers

**2.5-B — Zero singular direction.** A proposed SVD proof defines $u_i=Av_i/\sigma_i$ for every right Gram eigenvector. Locate the invalid step when $\sigma_i=0$ and replace it with the correct kernel argument.

**2.5-C — Repeated eigenvalues.** Two eigensolvers return different orthonormal columns for eigenvalue 2 of $\operatorname{diag}(2,2,0)$. What should be compared, and why can both answers be correct?

**2.5-D — Dimensions.** A 3-by-2 matrix has rank 1. State the shapes of its full factors, its right-kernel dimension and the dimension of the output complement orthogonal to its image. What changes if the matrix is zero?

**2.5-E — Preserve a sign.** Compare eigenvalues and singular values of $\operatorname{diag}(1,-2)$. Which decomposition retains the negative sign needed to diagnose lack of positivity?

**Answers and reasoning**

- **A.** No. The orthonormal eigenbasis and all-vector reconstruction were proved under Hermiticity. The non-Hermitian $N$ has only eigenvalue 0 yet has negative and non-real forms, as 2.4 showed.
- **B.** Division by zero is undefined. Instead $\|Av_i\|^2=\mu_i=0$ forces $Av_i=0$. Retain the right vector in the kernel basis; complete the positive left singular vectors to an output basis independently.
- **C.** Compare the summed projector onto the eigenvalue-2 subspace and the reconstructed operator. Rotations within that subspace preserve both, even when individual columns differ.
- **D.** $U$ is 3-by-3, $\Sigma$ is 3-by-2, and $V^\dagger$ is 2-by-2. Right kernel dimension is $2-1=1$; unused output dimension is $3-1=2$. For the zero map the factor shapes stay the same, all singular values vanish, and those dimensions become 2 and 3.
- **E.** Eigenvalues are 1 and $-2$; singular values in decreasing order are 2 and 1. The Hermitian spectral decomposition retains the sign. Singular values alone cannot distinguish this operator from a positive one with the same absolute eigenvalues.

Next, [2.6 Functions of matrices and time evolution](#sec-complex-vectors-operators-and-numerical-reasoning-6) uses decompositions to define and evaluate functions of operators with their assumptions stated.

### Source, status, and limits

Assigned sources: [NC:2.1.5](../references/proof-sources.md#source-nc-2-1-5), Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010), §2.1.5, printed pp. 68–69, and [NC:2.1.10](../references/proof-sources.md#source-nc-2-1-10), printed pp. 78–79. The companion spectral statement in Box 2.2 on printed p. 72 was also consulted. These pages were read from the previously supplied local copy. The source's normal-operator theorem and square SVD do not replace the local proof obligations here: this section supplies a Rayleigh-maximum/compactness proof for finite Hermitian matrices and a rectangular SVD construction with its kernel, without assuming a polar decomposition. Our convention writes $A=U\Sigma V^\dagger$ with right singular vectors as columns of $V$; the source's square formula names the whole right unitary factor $V$, so its symbol already includes that adjoint.

Depth **F**: full Hermitian diagonalization and rectangular singular-value construction, including their local bridges and zero cases. [The section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/2.5.json) separates author execution from pending independent mathematical, implementation and reader review. Infinite-dimensional spectral theory and general normal-operator diagonalization are outside this section's asserted theorem.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-6"></span>

## 2.6 Functions of matrices and time evolution

What should the square root or exponential of a matrix mean? Taking a scalar function of each entry usually gives the wrong operation. A matrix represents a transformation, and its function must respect that transformation's spectral structure and its coordinate conventions.

The prerequisite is [2.5](#sec-complex-vectors-operators-and-numerical-reasoning-5): Hermitian spectral projectors and reconstruction. We first define functions on that spectrum, then justify the exponential series and its convergence without assuming the operator-norm material of 2.7. Our evolution example uses a **constant**, finite Hermitian generator and dimensionless real time. It is a mathematical model, not a derivation of a quantum dynamical postulate or a hardware execution.

### Apply a function to spectral values, not entries

Write the Hermitian spectral decomposition using **distinct** eigenvalues $\lambda$ and their full eigenspace projectors:

$$
H=\sum_\lambda\lambda P_\lambda,\qquad
P_\lambda P_\mu=0\ (\lambda\ne\mu),\quad
P_\lambda^2=P_\lambda,\quad \sum_\lambda P_\lambda=I.
$$

For a scalar function $f$ defined at every eigenvalue, define

$$
f(H)=\sum_\lambda f(\lambda)P_\lambda.
$$

There are only finitely many terms. No continuity of $f$ is needed for this definition on a finite spectrum. It is well defined because 2.5 proved that each full eigenspace projector is independent of the orthonormal basis chosen inside that eigenspace. Assigning different function values to two vectors with the same eigenvalue would not be a scalar function of $H$.

If $H=Q\Lambda Q^\dagger$, this definition becomes $f(H)=Q f(\Lambda)Q^\dagger$, where $f(\Lambda)$ is diagonal with entries $f(\lambda_j)$. It does **not** mean apply $f$ to every entry of $\Lambda$: off-diagonal zero entries remain zero even when $f(0)\ne0$.

For example, a positive semidefinite $H$ has a spectral square root

$$
H^{1/2}=\sum_\lambda\sqrt\lambda\,P_\lambda.
$$

The nonnegative scalar square roots are defined because $\lambda\ge0$. Multiplying the projector sums gives $(H^{1/2})^2=H$, and its real nonnegative coefficients make it positive semidefinite. An inverse uses $f(\lambda)=1/\lambda$ and therefore requires no zero eigenvalue; its product with $H$ is $I$. A real logarithm on a Hermitian spectrum requires strictly positive eigenvalues if we use the ordinary real scalar logarithm. A domain or branch choice is part of specifying $f$, not something a solver can silently supply.

### Prove the algebra and composition rule

For scalar functions $f,h$ defined on the spectrum, finite projector multiplication gives

$$
\begin{aligned}
f(H)h(H)
 &=\sum_{\lambda,\mu}f(\lambda)h(\mu)P_\lambda P_\mu\\
 &=\sum_\lambda f(\lambda)h(\lambda)P_\lambda
 =(fh)(H).
\end{aligned}
$$

Here $(fh)(x)=f(x)h(x)$ is pointwise multiplication of scalar values. Addition and scalar multiplication work term by term in the same finite sums. Also $f(H)^\dagger=\sum_\lambda f(\lambda)^*P_\lambda$, because every projector is Hermitian. Thus real-valued $f$ on the spectrum produces a Hermitian matrix.

Composition needs care about the domain of the inner operator. Let $g$ be **real valued** on the spectrum of $H$, so $g(H)$ is Hermitian and our definition can be applied to it. If different values of $\lambda$ give the same number $\nu=g(\lambda)$, its eigenspace projector in $g(H)$ is the grouped sum $\sum_{g(\lambda)=\nu}P_\lambda$. Consequently, when $f$ is defined at every such $\nu$,

$$
\begin{aligned}
f(g(H))
 &=\sum_\nu f(\nu)\sum_{g(\lambda)=\nu}P_\lambda\\
 &=\sum_\lambda f(g(\lambda))P_\lambda=(f\circ g)(H).
\end{aligned}
$$

The notation $f\circ g$ means first apply $g$, then $f$. This proves composition even when $g$ merges eigenvalues. It does not assume $g$ is invertible. A calculus for non-Hermitian intermediate matrices needs additional definitions and is not asserted by this particular proof.

**2.6-A — A merged spectrum.** The previous $H$ has eigenvalues 1 and 3. For $g(x)=(x-2)^2$, what is $g(H)$? If $f(x)=e^x$, what should $f(g(H))$ be? We define this scalar exponential next.

### Define the scalar exponential and justify its products

For any complex scalar $z$, define

$$
e^z=\sum_{k=0}^{\infty}\frac{z^k}{k!},\qquad 0!=1,
$$

where $k!$ is the product of positive integers through $k$ for $k\ge1$. The term for $k=0$ is 1, including when $z=0$. For the series of absolute values, the ratio of successive nonzero terms is $\lvert z\rvert/(k+1)$. Past a finite index this is at most $1/2$, so the remaining terms are bounded by a convergent geometric tail. Thus the series is absolutely convergent; the case $z=0$ is immediate.

Absolute convergence allows multiplication and regrouping of its double series. Grouping by total power $k$ and applying the finite binomial expansion gives

$$
\begin{aligned}
e^ze^w
 &=\sum_{k=0}^\infty\sum_{p=0}^k
      \frac{z^p w^{k-p}}{p!(k-p)!}\\
 &=\sum_{k=0}^\infty\frac{(z+w)^k}{k!}=e^{z+w}.
\end{aligned}
$$

The binomial coefficient is $k!/(p!(k-p)!)$, so the middle sum is precisely the expansion of $(z+w)^k/k!$. The absolute double sum is finite because it is bounded by the product of the two convergent absolute series. This is the reason the regrouping is legitimate.

Termwise conjugation gives $(e^z)^*=e^{z^*}$; also $e^0=1$. Taking $w=-z$ proves $e^ze^{-z}=1$, so an exponential is never zero. For real $\theta$,

$$
\lvert e^{i\theta}\rvert^2=e^{-i\theta}e^{i\theta}=1.
$$

This scalar phase identity, rather than an assumed matrix property, will establish unitarity.

### The finite-matrix exponential series converges absolutely

For any square $M\in\mathbb C^{n\times n}$, define

$$
\exp(M)=\sum_{k=0}^\infty\frac{M^k}{k!},\qquad M^0=I.
$$

The powers are matrix products; this is not an entrywise scalar series. Let $a=\max_{j,\ell}\lvert M_{j\ell}\rvert$. For $k\ge1$, expanding an entry of $M^k$ gives $n^{k-1}$ products, each with $k$ factors of modulus at most $a$. The scalar triangle inequality therefore gives

$$
\lvert(M^k)_{j\ell}\rvert\le n^{k-1}a^k\le(na)^k.
$$

The entrywise absolute series is bounded by the scalar exponential series with nonnegative argument $na$, plus the finite identity term. Hence every entry converges absolutely. If $a=0$, all positive powers vanish and the result is $I$. No operator norm has been assumed.

For Hermitian $H$, induction using projector multiplication gives $H^k=\sum_\lambda\lambda^kP_\lambda$, including $k=0$. Therefore, for any scalar $z$,

$$
\begin{aligned}
\exp(zH)
 &=\sum_{k=0}^\infty\frac{z^k}{k!}
      \sum_\lambda\lambda^kP_\lambda\\
 &=\sum_\lambda\left(\sum_{k=0}^\infty\frac{(z\lambda)^k}{k!}\right)P_\lambda\\
 &=\sum_\lambda e^{z\lambda}P_\lambda.
\end{aligned}
$$

The spectral sum is finite and each scalar series is absolutely convergent. These facts justify interchanging the sums and prove agreement between the matrix power series and the spectral definition.

### Constant Hermitian evolution is unitary

For real dimensionless $t$, define

$$
U(t)=\exp(-itH)=\sum_\lambda e^{-it\lambda}P_\lambda.
$$

Every $\lambda$ is real. The scalar phase identity and orthogonal projectors give

$$
U(t)^\dagger U(t)
 =\sum_\lambda\lvert e^{-it\lambda}\rvert^2P_\lambda=I.
$$

The reverse product is the same projector sum, so $U(t)$ is unitary. Also

$$
U(0)=I,\qquad U(t)^\dagger=U(-t),\qquad
U(t)U(s)=U(t+s).
$$

The last equality follows from multiplying the same spectral projectors and using $e^{-it\lambda}e^{-is\lambda}=e^{-i(t+s)\lambda}$. Section 2.4 then proves that $U(t)$ preserves all overlaps and norms.

There is also an explicit differential equation. For a fixed complex $c$ and real $h\ne0$, the scalar series gives

$$
\left|\frac{e^{ch}-1}{h}-c\right|
 \le\lvert c\rvert^2\lvert h\rvert e^{\lvert c\rvert\lvert h\rvert}
 \longrightarrow0\quad(h\to0).
$$

To obtain the bound, sum the absolute terms starting at power 2 and use $1/(j+2)!\le1/j!$. Combining this limit with $e^{c(t+h)}=e^{ct}e^{ch}$ proves the derivative $d e^{ct}/dt=c e^{ct}$. Differentiating the **finite** spectral sum now gives

$$
\frac{dU(t)}{dt}=-iHU(t),\qquad
\psi(t)=U(t)\psi(0)\ \Longrightarrow\ i\frac{d\psi(t)}{dt}=H\psi(t).
$$

A derivative is the limit of a difference quotient; only the scalar limit above and finite sums were needed here. This proves an equation satisfied by the function we constructed. It does not derive the physical law connecting a particular system's Hamiltonian to its dynamics. Physical units and that interpretation are introduced later; in this example both $H$ and $t$ are dimensionless. If a generator depends on time, the constant-generator proof no longer applies as written.

Nor does the same-generator product rule apply automatically to unrelated matrices. Expanding $\exp(\epsilon A)\exp(\epsilon B)$ gives second-order mixed term $\epsilon^2 AB$, whereas $\exp(\epsilon(A+B))$ gives $\epsilon^2(AB+BA)/2$. Without $AB=BA$, these coefficients differ. The example checks a concrete failure instead of assuming a universal product identity.

### A two-by-two calculation with independent scalar phases

Use the earlier Hermitian matrix and its already verified spectral columns:

$$
H=\begin{pmatrix}2&i\\-i&2\end{pmatrix},\qquad
Q=\frac1{\sqrt2}\begin{pmatrix}1&1\\i&-i\end{pmatrix},\qquad
\lambda_1=1,\ \lambda_2=3.
$$

Set $a(t)=e^{-it}$ and $b(t)=e^{-3it}$. Multiplying $Q\operatorname{diag}(a(t),b(t))Q^\dagger$ gives

$$
U(t)=\begin{pmatrix}
(a+b)/2&-i(a-b)/2\\
i(a-b)/2&(a+b)/2
\end{pmatrix}.
$$

For example, entry $(1,2)$ is $a(-i)/2+bi/2=-i(a-b)/2$; entry $(2,1)$ follows from the corresponding row-column product. At $t=0$, both phases are 1, giving $I$. At $t=0.4$, the first diagonal entry is approximately $0.641709374-0.660728714i$. This is a matrix entry, not a sampled measurement outcome.

The same spectral columns give $H^{1/2}=Q\operatorname{diag}(1,\sqrt3)Q^\dagger$ and $H^{-1}=Q\operatorname{diag}(1,1/3)Q^\dagger$. The merged-spectrum example gives $(H-2I)^2=I$, hence $\exp((H-2I)^2)=eI$, with $e=e^1$.

### Formula to code and a bounded series remainder

The [complete program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/matrix_functions.py) uses Python 3.12 and PyTorch 2.13.0, CPU `complex128`. Its independent series stores two-by-two matrices as Python lists of complex numbers, implements matrix multiplication with explicit sums, and updates the term as `term = term @ M / k` using that list implementation. It does not call a tensor eigensolver or matrix-exponential routine to build its reference.

| Formula or distinction | Executable operation | Independent check |
|---|---|---|
| $f(H)$ through eigenvalues | `q @ diag(f(eigenvalues)) @ q.mH` | Previously hand-derived eigenbasis and scalar phases |
| Full exponential | `torch.linalg.matrix_exp(-1j*t*h)` | Closed scalar-entry formula and pure-Python power series |
| Matrix powers | List-based `multiply` in `series_exponential` | Explicit entries of $-itH$: $(-2it,t;-t,-2it)$ |
| Square root and reciprocal | Spectral diagonal square root and reciprocal | Square/product recovers $H$/$I$ |
| Merged-spectrum composition | `matrix_exp((h-2I) @ (h-2I))` | Independent identity $(H-2I)^2=I$ |
| Entrywise exponential | `torch.exp(-1j*t*h)` | Deliberately differs from `matrix_exp` |
| Adjoint, group, norm | Tensor products and inner products | Proven all-vector spectral identities |

A finite series needs a truncation bound. Let $B=na$ be the entry bound above, and retain terms $k=0,\ldots,N$. If $\rho=B/(N+2)<1$, the ratio between successive omitted scalar bounds is at most $\rho$, so every matrix entry has mathematical remainder at most

$$
\sum_{k=N+1}^\infty\frac{B^k}{k!}
 \le\frac{B^{N+1}}{(N+1)!}\frac1{1-\rho}.
$$

For $M=-itH$ with $\lvert t\rvert\le1$, $n=2$ and its largest entry modulus is at most 2, so $B=4$ is valid uniformly. With $N=40$, the bound is about $1.598\times10^{-25}$ per entry, below the conservatively reported $2.0\times10^{-25}$. The program verifies this tail inequality with exact rational arithmetic using `Fraction`. This is a bound on truncating the **exact arithmetic** series, not on floating-point roundoff. Numerical agreement is checked separately at absolute tolerance $10^{-12}$ with zero relative tolerance.

Run in the existing pinned example environment:

```bash
python -m pip install -r requirements-examples.txt
python examples/foundations/matrix_functions.py
```

Expected output:

```text
CPU complex128; dimensionless constant Hermitian generator, no physical execution.
Square root squared equals H; reciprocal times H equals identity
Merged-spectrum composition: exp((H-2I)^2)=e*I
5 real times: scalar phases, Python series and tensor matrix exponential agree
At t=0.4: U[0,0]=0.641709374-0.660728714j
Order-40 series: per-entry mathematical tail < 2.0e-25 for |t|<=1
Adjoint, group and unit-norm checks passed; first-order Taylor is not unitary
Entrywise exponential, non-Hermitian norm preservation and unrelated-generator product refuted
```

The five times are $-1,-0.4,0,0.4,1$. A unit-vector norm check, the group identity and the inverse-time adjoint are additional implementation checks. They do not replace the all-time proof.

The first-order polynomial $T_1(t)=I-itH$ exposes an approximation boundary:

$$
T_1(t)^\dagger T_1(t)=(I+itH)(I-itH)=I+t^2H^2.
$$

It is generally not unitary, even though the exact exponential is. The program checks this identity and its failure to equal $I$ for the worked nonzero time. It also uses the non-Hermitian generator $\operatorname{diag}(1,i)$, whose exponential at real $t$ is $\operatorname{diag}(e^{-it},e^t)$; the second direction changes norm. Hermiticity and exact functional evaluation are genuine assumptions, not optional labels.

No FlagQuantum API or quantum hardware execution is needed for these mathematical references. Larger times, large matrix entries and alternative precisions require a fresh error analysis; the small fixed-order series here is not a general-purpose numerical exponentiation algorithm. Pauli-specific exponential identities are derived only after their matrices and algebra are introduced in Chapter 3.

### Transfer, failure analysis, and answers

**2.6-B — A zero eigenvalue.** For $P=\operatorname{diag}(1,0)$, which of the spectral square root, reciprocal and real logarithm are defined under this section's scalar domains? Explain the failed domains rather than silently replacing zero.

**2.6-C — Truncation.** A program uses $I-itH$ and reports exact norm preservation because $H$ is Hermitian. Use the displayed product to identify the missing error term. At what boundary cases can that term vanish?

**2.6-D — Changing generator.** A colleague replaces the constant $H$ by a different Hermitian matrix at each time, but reuses the proof of $U(t+s)=U(t)U(s)$ from this section. Which shared object in that proof is no longer guaranteed?

**2.6-E — The wrong exponential.** An entrywise routine exponentiates every entry of the zero two-by-two matrix. Compare its result with the matrix exponential. Why is this a useful diagnostic even before using complex entries?

**Answers and reasoning**

- **A.** Both eigenvalues map to 1, so $g(H)=I$ and $f(g(H))=eI$. The eigenspaces merge, but grouping their projectors still gives the identity.
- **B.** The spectral square root exists and equals $P$. The reciprocal is undefined at eigenvalue 0, and the ordinary real logarithm is undefined there. A pseudoinverse or another regularization would be a separately specified function, not the inverse just defined.
- **C.** The product contains $t^2H^2$. For all-vector norm preservation it vanishes when $t=0$ or, for Hermitian $H$, $H=0$; the latter follows from its real eigenvalues and spectral theorem. On an individual input $v$, the extra squared norm is $t^2\|Hv\|^2$, so it can also vanish in a kernel direction.
- **D.** The proof multiplied phases on one fixed family of spectral projectors belonging to one fixed $H$. Different generators need not share those projectors or commute. A time-dependent evolution requires a separate construction and analysis.
- **E.** Entrywise exponentiation returns a matrix of ones because each scalar zero maps to 1. The matrix power series returns $I$, since all positive powers vanish. The two transformations already differ on this zero-input test.

Next, [2.7 Norms, conditioning, and perturbations](#sec-complex-vectors-operators-and-numerical-reasoning-7) develops the numerical tools needed to interpret approximation errors and sensitivity beyond these bounded examples.

### Source, status, and limits

Assigned companion source: [NC:2.1.8](../references/proof-sources.md#source-nc-2-1-8), Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010), §2.1.8, printed p. 75. That page was consulted from the previously supplied local copy. It supplies the spectral-function convention; this section provides its own projector composition proof, scalar exponential bridge, absolute convergence bounds and two-by-two calculation. No Pauli exponential or physical dynamical postulate is assumed from that source.

Depth **F**: prove spectral composition under the stated domains, agreement of the convergent exponential series and spectral formula, and unitary constant-Hermitian evolution. [The section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/2.6.json) separates author execution from pending independent mathematical, implementation and reader reviews. Time-dependent generators, non-Hermitian spectral calculus and general numerical stability are outside the asserted results here.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-7"></span>

## 2.7 Norms, conditioning, and perturbations

A program returns a candidate solution and reports a residual near zero. Is the solution accurate? The answer depends on how strongly the problem amplifies changes in its inputs. A residual measures whether the equations are nearly satisfied; it is not automatically the distance to the exact solution.

The prerequisites are [2.3](#sec-complex-vectors-operators-and-numerical-reasoning-3) and [2.5](#sec-complex-vectors-operators-and-numerical-reasoning-5): linear maps, inverses and singular-value decomposition. This section does not require 2.6. We use Euclidean vector norms and their induced matrix norms in fixed orthonormal coordinates. The relative-error results concern square invertible systems with nonzero right-hand sides; zero and singular cases are identified separately.

### From vector size to the largest possible amplification

For $x\in\mathbb C^n$, write its Euclidean norm as $\|x\|_2=\sqrt{\sum_j\lvert x_j\rvert^2}$. For $A\in\mathbb C^{m\times n}$, define the **induced operator norm** by

$$
\|A\|_{\mathrm{op}}=\max_{\|x\|_2=1}\|Ax\|_2.
$$

It measures the largest output length for a unit input, not the size of a particular matrix entry. To see that the maximum exists and compute it, use the SVD from 2.5. If $x=\sum_j c_jv_j$ in its orthonormal right basis, then

$$
\|Ax\|_2^2=\sum_{j=1}^r\sigma_j^2\lvert c_j\rvert^2
 \le\sigma_{\max}^2\sum_j\lvert c_j\rvert^2
 =\sigma_{\max}^2\|x\|_2^2.
$$

For a nonzero matrix the right singular vector for $\sigma_{\max}$ attains equality. For the zero matrix every output is zero. Therefore $\|A\|_{\mathrm{op}}=\sigma_{\max}$, with value 0 for the zero matrix, and

$$
\|Ax\|_2\le\|A\|_{\mathrm{op}}\|x\|_2
$$

for every input, including zero. For nonzero $x$, the same bound also follows directly by applying the definition to $x/\|x\|_2$.

This is a matrix norm: nonnegativity and homogeneity follow from the vector norm, and a nonzero matrix has a nonzero column, so its norm cannot vanish. For addition, apply the vector triangle inequality to $(A+B)x$, bound each term and maximize over unit $x$ to obtain $\|A+B\|_{\mathrm{op}}\le\|A\|_{\mathrm{op}}+\|B\|_{\mathrm{op}}$.

If $B$ maps into the input space of $A$, apply the matrix-vector bound twice:

$$
\|ABx\|_2\le\|A\|_{\mathrm{op}}\|Bx\|_2
 \le\|A\|_{\mathrm{op}}\|B\|_{\mathrm{op}}\|x\|_2.
$$

Maximizing over unit input proves **submultiplicativity**:

$$
\|AB\|_{\mathrm{op}}\le\|A\|_{\mathrm{op}}\|B\|_{\mathrm{op}}.
$$

Both the dimensions and the intermediate vector norm must match. More general induced norms can use other consistent vector norms; all numerical constants and condition numbers in this section use the Euclidean choice.

### Do not confuse operator and Frobenius norms

The **Frobenius norm** is $\|A\|_F=\sqrt{\sum_{i,j}\lvert A_{ij}\rvert^2}$, the Euclidean size of the whole entry array. It differs from the induced norm. For the two-by-two identity, $\|I\|_{\mathrm{op}}=1$ because it preserves every vector, while $\|I\|_F=\sqrt2$.

They do satisfy $\|A\|_{\mathrm{op}}\le\|A\|_F$. For each output row, Cauchy–Schwarz gives $\lvert\sum_j A_{ij}x_j\rvert^2\le(\sum_j\lvert A_{ij}\rvert^2)\|x\|_2^2$. Sum over rows and maximize over unit $x$ to obtain that bound. An upper bound is useful, but changing norms midway through an argument changes what its constants mean.

Notation varies across books. The assigned Watrous source calls the spectral/Euclidean-induced norm a Schatten infinity norm, and its Schatten 2-norm is Frobenius. We use the explicit subscript “op” to avoid interpreting its $\|A\|_2$ as our induced norm. In the code, `torch.linalg.matrix_norm(A, ord=2)` computes the induced spectral norm; `ord="fro"` computes Frobenius. The order argument is part of the verification contract.

### Absolute sensitivity and a relative condition number

Let $A$ be an invertible $n$-by-$n$ matrix. All its singular values are positive. The SVD gives the lower bound $\|Ax\|_2\ge\sigma_{\min}\|x\|_2$, and an inverse gain at most $1/\sigma_{\min}$. This gain is attained: $Av_{\min}=\sigma_{\min}u_{\min}$ implies $A^{-1}u_{\min}=v_{\min}/\sigma_{\min}$. Thus

$$
\|A^{-1}\|_{\mathrm{op}}=\frac1{\sigma_{\min}},\qquad
\kappa(A)=\|A\|_{\mathrm{op}}\|A^{-1}\|_{\mathrm{op}}
 =\frac{\sigma_{\max}}{\sigma_{\min}}\ge1.
$$

This $\kappa(A)$ is the **relative normwise condition number** for the linear system under these norms. “Normwise” means we measure the size of a whole perturbation vector or matrix, rather than prescribing separate relative changes for each entry. If $A$ is singular, this inverse and finite condition number are unavailable; one often records the condition number as infinite by convention.

For $Ax=b$, perturb only the right-hand side by $f$. The solution change is $\Delta x=A^{-1}f$, giving the **absolute** bound

$$
\|\Delta x\|_2\le\|A^{-1}\|_{\mathrm{op}}\|f\|_2.
$$

For a relative statement, assume $b\ne0$. Then $x\ne0$, and $\|b\|_2=\|Ax\|_2\le\|A\|_{\mathrm{op}}\|x\|_2$. Dividing the absolute bound and using this relation gives

$$
\frac{\|\Delta x\|_2}{\|x\|_2}
 \le\kappa(A)\frac{\|f\|_2}{\|b\|_2}.
$$

The condition number is a worst-case amplification bound. A particular perturbation may point in a direction with much smaller amplification.

### Turn a residual into a conditional error bound

Let $\widehat x$ be any candidate for the exact solution $x=A^{-1}b$. Define its **residual** by $r=b-A\widehat x$ and its solution error by $e=\widehat x-x$. Subtracting $Ax=b$ gives $Ae=-r$, so

$$
\|e\|_2\le\|A^{-1}\|_{\mathrm{op}}\|r\|_2,\qquad
\frac{\|e\|_2}{\|x\|_2}
 \le\kappa(A)\frac{\|r\|_2}{\|b\|_2}\quad(b\ne0).
$$

The relative error on the left is called a **forward error**. Holding $A$ fixed, the candidate exactly solves $A\widehat x=b-r$. Thus $-r$ is the required right-hand-side perturbation; $\|r\|_2/\|b\|_2$ is the corresponding **right-hand-side backward error**. Other backward-error models may permit changes in both $A$ and $b$ and use a different normalization. We are stating which model is used.

A small backward error can coexist with a large forward error when $\kappa(A)$ is large. This is a property of the problem's sensitivity, not automatically a failure of the algorithm that produced a candidate. For $b=0$, the exact solution is zero and these relative ratios divide by zero; use the absolute error bound instead.

**2.7-A — Read the bound.** Suppose the relative residual is $10^{-8}$ and $\kappa(A)=10^6$. What upper bound follows for relative forward error? Does it imply that the actual error equals that number?

### A small-residual counterexample with exact arithmetic

Take a positive scalar $\delta<1$ and

$$
A=\begin{pmatrix}1&0\\0&\delta\end{pmatrix},\qquad
b=\begin{pmatrix}1\\0\end{pmatrix},\qquad
x=\begin{pmatrix}1\\0\end{pmatrix},\qquad
\widehat x=\begin{pmatrix}1\\1\end{pmatrix}.
$$

The diagonal action gives singular values 1 and $\delta$, so $\kappa(A)=1/\delta$. Direct subtraction gives

$$
r=b-A\widehat x=\begin{pmatrix}0\\-\delta\end{pmatrix},\qquad
\frac{\|r\|_2}{\|b\|_2}=\delta,\qquad
\frac{\|\widehat x-x\|_2}{\|x\|_2}=1.
$$

The error bound is attained: $(1/\delta)\delta=1$. Making $\delta$ smaller improves the residual without changing this candidate's forward error. The candidate is exactly the solution of the nearby input $b-r=(1,\delta)$. Both statements follow from coordinate arithmetic, independent of any solver.

The code uses $\delta=2^{-4},2^{-12},2^{-20}$, which are exactly representable binary values. For the last case, the relative residual is approximately $9.536743164\times10^{-7}$ and the relative forward error is 1, with $\kappa(A)=1048576$. It also solves both original and perturbed systems and compares them to the explicit solutions. It does **not** claim that a solver returned the constructed inaccurate candidate for the original input.

### Perturb the matrix as well as the input

First consider a general matrix-vector product. If $A$ changes by $E$ and $x$ by $d$, distributing gives the exact identity

$$
(A+E)(x+d)-Ax=Ad+Ex+Ed.
$$

The triangle and induced-norm bounds imply

$$
\|(A+E)(x+d)-Ax\|_2
 \le\|A\|_{\mathrm{op}}\|d\|_2
   +\|E\|_{\mathrm{op}}\|x\|_2
   +\|E\|_{\mathrm{op}}\|d\|_2.
$$

The last term is part of the exact bound; it should not be silently dropped as if it were zero.

For a changed linear system, suppose

$$
(A+E)(x+\Delta x)=b+f,\qquad Ax=b.
$$

Define $\eta=\|A^{-1}\|_{\mathrm{op}}\|E\|_{\mathrm{op}}$ and assume $\eta<1$. This ensures the perturbed square matrix is still invertible. Indeed,

$$
\|(A+E)z\|_2
 \ge\|Az\|_2-\|Ez\|_2
 \ge\left(\frac1{\|A^{-1}\|_{\mathrm{op}}}-\|E\|_{\mathrm{op}}\right)\|z\|_2.
$$

The bracket is positive. A zero singular value would provide a nonzero vector with zero output, contradicting this inequality. The square SVD therefore has only positive singular values and can be inverted, proving existence of the changed solution.

Subtract the original system, apply $A^{-1}$, and bound all terms:

$$
\Delta x=A^{-1}(f-Ex-E\Delta x),
$$

$$
(1-\eta)\|\Delta x\|_2
 \le\|A^{-1}\|_{\mathrm{op}}
       \bigl(\|f\|_2+\|E\|_{\mathrm{op}}\|x\|_2\bigr).
$$

For $b\ne0$, define relative input sizes $\epsilon_A=\|E\|_{\mathrm{op}}/\|A\|_{\mathrm{op}}$ and $\epsilon_b=\|f\|_2/\|b\|_2$. Then $\eta=\kappa(A)\epsilon_A$, and dividing by $\|x\|_2$ and using $\|b\|_2\le\|A\|_{\mathrm{op}}\|x\|_2$ yields

$$
\frac{\|\Delta x\|_2}{\|x\|_2}
 \le\frac{\kappa(A)}{1-\kappa(A)\epsilon_A}
       (\epsilon_b+\epsilon_A),\qquad
\kappa(A)\epsilon_A<1.
$$

This is a sufficient small-perturbation condition. If it fails, this bound is unavailable; it does not say every such perturbed matrix must be singular.

In the diagonal example, choose $E=\operatorname{diag}(0,-\delta/2)$ and $f=(0,\delta)$. The new matrix is $\operatorname{diag}(1,\delta/2)$ and the new exact solution is $(1,2)$, giving relative change 2. Here $\eta=1/2$, $\epsilon_A=\delta/2$ and $\epsilon_b=\delta$; the bound gives $(1/\delta)(3\delta/2)/(1/2)=3$, consistent with 2. By contrast, $E=\operatorname{diag}(0,-\delta)$ gives $\eta=1$ and makes this specific matrix singular. The latter is an example of failure at the boundary, not a theorem about every perturbation with $\eta\ge1$.

### Scale, conditioning and numerical stability

A small singular value by itself does not imply a large **relative** condition number. For $A=\delta I$ with $\delta>0$, every singular value is $\delta$, so $\kappa(A)=1$, while $\|A^{-1}\|_{\mathrm{op}}=1/\delta$ can be large. The absolute and relative sensitivity statements answer different questions. Uniformly rescaling a nonzero matrix changes its absolute gain but leaves the singular-value ratio unchanged.

Conditioning describes sensitivity of the stated mathematical problem under a specified perturbation model. Numerical stability describes how an algorithm's computed result relates to exact solutions of nearby inputs. A small right-hand-side backward error alone does not establish stability under every data model, and a large forward error on an ill-conditioned problem does not by itself locate a faulty implementation. The diagonal example deliberately separates those claims.

Coordinates also matter. These Euclidean formulas refer to orthonormal coordinates and stated input/output scales. A nonorthonormal basis or different physical units can change the appropriate vector norm or require a Gram-weighted one, as in 2.3. Report the representation and perturbation model with a condition number.

### Formula to code and exact reference checks

The [complete example](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/conditioning.py) targets Python 3.12, PyTorch 2.13.0, CPU `complex128`. The diagonal matrices, solutions and bounds are derived above. `Fraction` supplies exact binary-scale values and the rational combined bound; tensor norms and solves are checked against those references.

| Quantity or claim | Code | Independent reference |
|---|---|---|
| Induced operator norm | `matrix_norm(A, ord=2)` | Largest singular value; explicit diagonal values |
| Vector residual | `b - A @ candidate` | $(0,-\delta)$ by direct coordinate subtraction |
| Condition number | `op(A) * op(inverse)` | Exact $1/\delta$, with diagonal inverse specified independently |
| Forward error and nearby input | Norm of `candidate-exact`; `solve(A, b-residual)` | Explicit original $(1,0)$ and nearby $(1,1)$ solutions |
| Combined perturbation | `solve(A+E, b+f)` | Exact solution $(1,2)$ and rational upper bound 3 |
| Norm convention | Operator and Frobenius norms of $I$ | 1 versus $\sqrt2$ |
| Submultiplicativity/product change | Compatible matrix products and norm bounds | Explicit reconstructed product and distributed perturbation terms |

Run in the existing pinned example environment:

```bash
python -m pip install -r requirements-examples.txt
python examples/foundations/conditioning.py
```

Expected output:

```text
CPU complex128; constructed sensitivity cases, not observed solver failures.
delta=2^-4: kappa=16; relative residual=6.250000000e-02; relative error=1.0
delta=2^-12: kappa=4096; relative residual=2.441406250e-04; relative error=1.0
delta=2^-20: kappa=1048576; relative residual=9.536743164e-07; relative error=1.0
Combined perturbation: eta=1/2; relative solution change=2; proven bound=3
Specific eta=1 perturbation is singular; zero direction checked
Uniformly scaled identity: kappa=1 despite small singular values
Identity norms: operator=1, Frobenius=sqrt(2) (different conventions)
Exact references, nearby solves, submultiplicativity and perturbation checks passed.
```

Tensor comparisons use absolute tolerance $10^{-12}$ and zero relative tolerance. The additional product inequalities allow $10^{-12}$ for rounding. Frobenius and operator calculations both explicitly use `complex128`; changing a tensor's default precision can otherwise change an apparently unrelated check. Large problems or different scales need tolerances justified for their own errors, not a universal reuse of this constant.

The proofs establish the norm bounds. Numerical tests establish agreement on the stated cases, not stability of every solver or accuracy of a condition estimate for every near-singular matrix. No FlagQuantum API, quantum circuit or hardware execution is involved.

### Transfer and diagnosis

**2.7-B — A residual-only claim.** A report states “relative residual $10^{-10}$, therefore relative solution error below $10^{-10}$.” What information is missing? How would $\kappa(A)=10^8$ change the guaranteed upper bound?

**2.7-C — Zero right-hand side.** For invertible $A$ and $b=0$, how should one assess a nonzero candidate? Which relative quantities in this section are undefined?

**2.7-D — Change the matrix.** In the diagonal example, a perturbation has $\eta=1.2$. Does the proved bound apply? Does that number alone prove the new matrix singular?

**2.7-E — Absolute versus relative.** For $A=10^{-6}I$, determine $\kappa(A)$ and $\|A^{-1}\|_{\mathrm{op}}$. Explain why the two answers are compatible.

**Answers and reasoning**

- **A.** The bound is $10^{-2}$. It is an upper bound under the stated assumptions, not an assertion that the actual error equals it. Direction matters.
- **B.** The norm/coordinate convention, invertibility and condition number are missing. Under this section's assumptions the bound becomes $10^{-2}$, not $10^{-10}$. A stronger conclusion needs additional information.
- **C.** The exact solution is zero. Compute $r=-A\widehat x$ and use $\|\widehat x\|_2\le\|A^{-1}\|_{\mathrm{op}}\|r\|_2$. Both residual divided by $\|b\|_2$ and error divided by $\|x\|_2$ are undefined; their denominators vanish.
- **D.** The sufficient condition $\eta<1$ fails, so the displayed small-perturbation bound cannot be used. The new matrix may or may not be singular. Inspect it or use another justified argument.
- **E.** The relative condition number is 1 and the absolute inverse gain is $10^6$. All directions scale equally, so relative perturbations are not amplified by an unequal singular-value ratio, while a fixed absolute input change can produce a large absolute solution change.

Next, [2.8 Floating-point arithmetic and verification contracts](#sec-complex-vectors-operators-and-numerical-reasoning-8) separates mathematical error bounds, representation/rounding effects and executable correctness claims.

### Source, status, and limits

Assigned companion source: [TQI:1.1.3](../references/proof-sources.md#source-tqi-1-1-3), John Watrous, *The Theory of Quantum Information*, author prepublication copy (2018), §1.1.3, especially printed pp. 32–33, equations (1.166), (1.175)–(1.176) and the spectral/Frobenius discussion. [The author's public PDF](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf#page=40) and its existing local cache were consulted for the norm conventions. The condition-number and residual/perturbation proofs and diagonal cases above are original exposition, not claims that this source presents those same examples or sensitivity bounds. No source text or PDF is redistributed.

Depth **F**: prove the induced norm bound and submultiplicativity, condition-dependent error amplification and the stated matrix-perturbation estimate, with an ill-conditioned counterexample. [The section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/2.7.json) separates author execution from pending independent mathematical, implementation and reader review. Rectangular least-squares conditioning and componentwise stability are not asserted by these square-system bounds.

<span id="sec-complex-vectors-operators-and-numerical-reasoning-8"></span>

## 2.8 Floating-point arithmetic and verification contracts

Suppose an assertion says that a computed result is close to a reference. Before trusting it, ask: close in which units, at which scale, with which shape and precision, and compared with what independent evidence? An assertion can execute correctly while checking a weaker claim than the experiment needs.

The prerequisite is [2.7](#sec-complex-vectors-operators-and-numerical-reasoning-7): conditioning, residuals and error bounds. Here we introduce a bounded rounding model and turn those mathematical distinctions into executable verification contracts. The examples use dense CPU tensors with explicitly declared dtypes; they do not establish the behavior of every numerical kernel or platform.

### What a floating-point dtype can retain

A binary floating-point format stores a sign, a bounded exponent and a finite number of significant binary digits. In a normalized positive interval $[2^e,2^{e+1})$, a format with $p$ significant bits has spacing $2^{e-(p-1)}$. Negative values have the corresponding spacing by magnitude. Not every real number is representable.

With rounding to nearest, and away from overflow and underflow, rounding a nonzero real value $x$ incurs at most half that spacing. Since $\lvert x\rvert\ge2^e$,

$$
\frac{\lvert\operatorname{fl}(x)-x\rvert}{\lvert x\rvert}
 \le\frac{2^{e-p}}{2^e}=2^{-p}=u.
$$

Here $\operatorname{fl}(x)$ denotes the rounded value and $u$ the **unit roundoff** for this model. This local statement is not a bound on an entire algorithm: later arithmetic can propagate earlier errors. The spacing immediately above 1 is $\epsilon=2^{-(p-1)}=2u$, often reported as machine epsilon. Do not confuse spacing with half-spacing.

For the CPU formats used here, `float32` has $p=24$ and `float64` has $p=53$; their spacings above 1 are $2^{-23}$ and $2^{-52}$. `torch.finfo(dtype).eps` reports these values in the tested runtime. `complex128` stores two `float64` components; it does not give each component 128 significant bits. Underflow, overflow, special values and alternative execution modes fall outside the simple normalized-range inequality.

Take the exactly representable increment $d=2^{-25}$. Around 1 it is smaller than half the `float32` spacing, so evaluating $(1+d)-1$ in that dtype returns zero. The same operations in `float64` return exactly $d$ in this case. Converting the already rounded zero to `float64` cannot restore the lost increment; recomputing from suitable inputs is different from casting a result.

Operation order also matters. The program computes, in `float32`, both

$$
(2^{25}+1)-2^{25}=0\quad\text{in the tested floating arithmetic},
$$

and

$$
(2^{25}-2^{25})+1=1.
$$

The exact real expressions both equal 1. Near $2^{25}$ the `float32` spacing is 4, so the first addition loses the 1 before the subtraction occurs. The example does not require random input or a changing device to produce different answers: changing the arithmetic order is enough. It also shows why one operation's small relative rounding error need not give a small relative error in a later tiny difference.

### Write the comparison as an inequality

For a finite computed scalar $a$ and reference $b$, a common reference-scaled contract is

$$
\lvert a-b\rvert\le\mathrm{atol}+\mathrm{rtol}\lvert b\rvert.
$$

The **absolute tolerance** `atol` has the same units as the output. The **relative tolerance** `rtol` is dimensionless. Both must be finite and nonnegative. For complex scalars we use the modulus of the difference, not independent sign checks. For a tensor, the example requires the inequality at every corresponding entry after validating metadata.

The two terms address different scales. When $b=0$, the relative term vanishes, so a nonzero permissible residual needs an absolute budget. For an order-one nonzero reference, a relative budget can express the desired fractional accuracy. Their numerical values must follow from the intended output accuracy, a justified error analysis or an explicitly labeled validation target. Merely choosing a large enough value to make a failure disappear supplies no new evidence.

For a tiny expected signal $b=10^{-12}$ and computed value $a=0$, the absolute error is $10^{-12}$ but the relative error is 1. The pair passes `atol=1e-8, rtol=0`. If the actual task requires relative error at most $10^{-6}$ with no absolute floor, its budget is $10^{-18}$ and the pair fails. The first assertion is not broken; it answered a less demanding question that permits losing the signal entirely.

Conversely, a target value 0 and actual residual $5\times10^{-13}$ pass an explicitly chosen absolute budget $10^{-12}$. A relative-only comparison to zero would demand exact zero regardless of how large `rtol` is. This absolute budget is a declared check for our bounded example, not a universal claim about acceptable physical or numerical error.

The predicate is also reference dependent. With `atol=0, rtol=0.75`, actual 1 compared with expected 2 passes, whereas actual 2 compared with expected 1 fails. The errors are both 1, but the allowed budgets are 1.5 and 0.75. Such loose values illustrate the asymmetry; they are not recommended tolerances. Choose the expected argument as the reference rather than swapping roles until a test passes.

**2.8-A — Preserve a signal.** A nonzero reference is $10^{-9}$ and the task allows at most 1% relative error. With no absolute floor, what budget applies? Would zero be acceptable?

### Metadata and finite values belong in the contract

Numerical proximity alone does not check whether the objects have the required interpretation. The complete program's `assert_finite_close` first requires identical shape, dtype and device, then finite entries, then the stated error inequality. It performs no implicit casting or shape broadcasting. It also rejects non-finite error or budget arithmetic, so overflow in the comparison itself cannot silently certify a result. This is a small comparator for the bounded examples, not a general library for arbitrary tensor types and scales.

A concrete shape trap uses `[1, 1]` with shape `(2,)` and `[[1], [1]]` with shape `(2, 1)`. In the tested runtime, `torch.allclose` broadcasts them and returns true even with zero tolerances. It effectively compares expanded two-by-two arrays of ones. If the intended contract was two columns of the same declared shape, that result does not satisfy it. Our comparator rejects the mismatch before subtraction.

The example also rejects equal infinities: its task requires finite results, even though a generic comparison may legitimately consider matching infinities equal. `NaN`, meaning “not a number,” needs an explicit finite check. Merely testing whether any error is larger than a tolerance can miss it, because a comparison of `NaN` with that threshold is false. Requiring all entries finite before calculating a closeness predicate avoids that failure here.

Dtype is likewise a semantic choice. A `float32` array does not satisfy a `float64` execution contract simply because its printed numbers match. The earlier lost-increment case explains the distinction. A deliberate precision conversion should be recorded and justified; it should not hide an unexpected precision change in the computation under test.

### A residual budget must respect conditioning

Reuse the exact diagonal case from 2.7 with $\delta=2^{-20}$:

$$
A=\operatorname{diag}(1,\delta),\quad b=x=(1,0),\quad
\widehat x=(1,1),\quad \kappa(A)=2^{20}.
$$

All displayed vectors are columns. Its residual norm is $\delta\approx9.536743164\times10^{-7}$, so comparing that norm with zero at `atol=1e-6` passes. Its relative forward error is still 1.

The proved condition-dependent bound gives a different verification target. To guarantee a target relative error $\tau=10^{-8}$ from that bound, a **sufficient** condition is

$$
\frac{\|r\|_2}{\|b\|_2}\le\frac{\tau}{\kappa(A)}.
$$

Here $\|b\|_2=1$, giving an absolute residual budget about $9.536743164\times10^{-15}$. The constructed candidate fails this test, while the exact solution has zero residual and passes. Failure of a sufficient bound does not prove that every candidate failing it has excessive forward error; it means that this bound no longer certifies the target. For this particular candidate the independently known forward error confirms the failure.

These binary diagonal inputs make the displayed residual calculation exact in the tested arithmetic. On a general problem, the computed residual and condition estimate have their own errors. A comparison cannot turn uncertain diagnostics into exact bounds without accounting for those uncertainties. This example links a proved mathematical bound to a check under explicitly controlled conditions.

### Match each claim to an independent check

The [complete program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/verification_contracts.py) uses Python 3.12 and PyTorch 2.13.0, CPU. It deliberately runs `float32`, `float64` and `complex128` cases. Exact rational `Fraction` references establish the dyadic increment and condition-derived budget. Deliberate rejection cases are caught and verified; a silently accepted wrong result makes the program fail.

| Intended claim | Program operation | Independent evidence or counterexample |
|---|---|---|
| An increment survives arithmetic | Compare low/high precision evaluation | Exact rational $2^{-25}$; casting the low result cannot restore it |
| A tiny nonzero signal is preserved | Explicit `atol`, `rtol` inequality | Zero passes a loose absolute check but fails the task's relative budget |
| A zero residual fits its budget | Absolute comparison with zero | Relative term vanishes at the reference zero |
| Corresponding outputs have the declared type | Shape/dtype/device checks | Broadcasting and precision mismatch are rejected |
| The result is finite | `torch.isfinite` before arithmetic | `NaN` and matching infinities are rejected for this finite-output task |
| Complex proximity uses modulus | `torch.abs(actual-expected)` | $1+i$ is farther than 1.1 from zero although each component is only 1 |
| Residual supports a forward-error target | Divide target by exact $\kappa(A)$ | Known exact solution and constructed candidate from 2.7 |

Run in the pinned example environment:

```bash
python -m pip install -r requirements-examples.txt
python examples/foundations/verification_contracts.py
```

Expected output:

```text
Declared CPU dtypes; exact references and finite verification contracts, no quantum execution.
Increment 2^-25: float32 loses it; float64 retains it; later casting does not restore it
Float32 operation order: (2^25+1)-2^25=0; (2^25-2^25)+1=1
Tiny 1e-12 signal: zero passes atol=1e-8, but fails the declared relative-only budget
Zero and order-one checks use different justified absolute/relative budgets
Expected-scaled comparison can change when actual and expected are swapped
Broadcasting allclose passes the wrong shape; strict metadata contract rejects it
Wrong dtype, NaN, Inf and complex-modulus counterexamples rejected
Residual below 1e-6 can accompany relative forward error=1
For target relative error 1e-8: conditioned absolute residual budget=9.536743164e-15
All declared cases passed; this is not an all-input or cross-platform proof.
```

The program does not invoke FlagQuantum because these are arithmetic and verification references. Comparing two wrappers around the same mistaken formula would not be independent evidence. Keep a hand calculation, exact rational case or separately derived representation alongside implementation comparisons.

### Record reproducibility without promising identical bits

The optional command

```bash
python examples/foundations/verification_contracts.py --environment
```

prints a JSON record instead of the test cases. It reports Python/PyTorch versions, operating-system family, architecture, CPU target, the case dtypes and whether PyTorch's deterministic-algorithm mode is enabled. Values vary by machine; they are environment evidence, not a second fixed expected-output block. The author run used Python 3.12.14 and PyTorch 2.13.0 on macOS ARM64 CPU, with deterministic-algorithm mode disabled; no stronger mode is implied.

A full experiment additionally records the source revision, dependency versions, operation/input specification, precision settings, seeds when randomness is used, reference construction, tolerance rationale and actual checks. A seed controls a random sequence within a specified setup; it does not specify every arithmetic order, backend or software version. Deterministic execution in one setup and bitwise equality across all setups are different claims. Here the reassociated-sum example already shows why changing arithmetic order can change bits.

Reproduce the declared mathematical task and verification contract. If results differ, preserve the differing environment and diagnostic outputs, identify whether metadata, arithmetic, modeling or an input changed, and investigate before changing the error budget. The verification result and the review status remain separate records.

### Transfer and answers

**2.8-B — Upscaling a result.** A calculation loses a small increment in `float32`. A colleague converts only its final result to `float64` and expects the correct digits to return. What does the worked case predict, and what must instead be recomputed?

**2.8-C — A misleading check.** A checker computes `bad = abs(actual-expected) > tol` and accepts when no entry of `bad` is true. What extra checks are needed for the task in this section?

**2.8-D — Correct the conclusion.** A candidate passes a residual threshold of $10^{-6}$ in the diagonal example. An author calls this a proof of $10^{-6}$ relative solution accuracy and deterministic behavior on any hardware. Which two inferences exceed the evidence?

**Answers and reasoning**

- **A.** The budget is $0.01\times10^{-9}=10^{-11}$. Zero has error $10^{-9}$ and fails. A larger absolute floor would change the task's accepted errors.
- **B.** The final low-precision zero remains zero after conversion. Recompute the relevant operations with inputs and intermediates represented at the intended precision; even then establish that the new budget meets the task, rather than assuming a cast fixes prior rounding.
- **C.** Validate shape/dtype/device, finite values and finite comparison arithmetic, and define the absolute/relative budget. A `NaN` can evade the oversized-error mask, while broadcasting can compare unintended entries. The complete comparator supplies these guards for the declared dense floating-point cases.
- **D.** Residual accuracy does not imply equal forward accuracy without conditioning and a justified error bound. One successful run also does not establish hardware-independent bitwise behavior. Record exactly the candidate's checks and environment; neither inference follows from that threshold.

### Chapter 2 synthesis and problems

We now have a connected route from complex coordinates through adjoints, basis changes, operator classes, spectral/SVD reconstructions and numerical error contracts. The mathematical identities and their execution checks answer different questions. Use the following problems to connect the layers rather than treating a passing scalar comparison as the endpoint.

**2-C1 — Derivation and coordinates.** For unitary $Q$, prove that $B=Q^\dagger AQ$ has the same induced Euclidean operator norm as $A$. Explain why the nonorthogonal-basis swap matrix from 2.3 need not preserve that naive coordinate norm.

**Answer.** For every unit $y$, $\|By\|_2=\|AQy\|_2$ because $Q^\dagger$ preserves vector norms. The map $y\mapsto Qy$ bijects the unit sphere, with inverse $Q^\dagger$, so maximizing gives $\|B\|_{\mathrm{op}}=\|A\|_{\mathrm{op}}$. For the nonorthogonal case, $B=\begin{pmatrix}-1&0\\1&1\end{pmatrix}$ sends unit $e_1$ to $(-1,1)$ of length $\sqrt2$, whereas the old swap has operator norm 1. The underlying operator did not change; the appropriate Gram-weighted coordinate norm must be retained.

**2-C2 — Debug two agreeing implementations.** Two implementations use an unconjugated dot product to calculate the squared length of $(1,i)$. Both return zero and agree exactly. Design an independent check and identify which extra metadata checks alone would fail to expose the mathematical defect.

**Answer.** The independent real/imaginary calculation gives $\lvert1\rvert^2+\lvert i\rvert^2=2$. Positive definiteness also forbids zero length for this nonzero vector. Correct shape, dtype, device and finite values would all pass for the wrong scalar zero; those guards are necessary for their own claims but cannot replace the correct conjugation rule and independent reference.

**2-C3 — Implementation contract for an SVD.** Plan verification for the full 2-by-3 example of 2.5. Specify factor shapes, finite/dtype requirements, a reconstruction check and a phase-independent kernel check. Explain what to compare when singular or eigenvalues are degenerate.

**Answer.** Require $U$ shape `(2,2)`, real singular-value vector shape `(2,)`, $V^\dagger$ shape `(3,3)`, complex factors `complex128` and singular values `float64` on CPU, all finite. Build a 2-by-3 $\Sigma$, check unitary factors and compare $U\Sigma V^\dagger$ with the independent explicit matrix under a declared budget. Check the last right column is annihilated and its rank-one projector equals the projector onto $e_2$. Compare projectors onto whole degenerate subspaces and reconstructed actions, rather than insisting on identical phases or individual columns. The complete `spectral_svd.py` program supplies these numerical cases; add metadata guards of the kind introduced here to its result contract.

Continue with the working draft [3.1 The pure-state postulate and physical equivalence](ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-1). The mathematics now supports stating a quantum-state postulate and distinguishing physical equivalence from equality of stored coordinate arrays. Chapter 2 has eight working section drafts; independent mathematical, implementation and reader acceptance remain pending.

### Source, status, and limits

Assigned sources are [NC:2.1.2](../references/proof-sources.md#source-nc-2-1-2), Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010), printed pp. 63–64, and [ED:protocol](../references/proof-sources.md#source-ed-protocol), the project's original [reader-continuity and acceptance standard](../reader-continuity.md). The specified textbook pages and local protocol were consulted. The first supports the matrix/map distinction; it is not being cited as a floating-point specification. The rounding models, executable contracts and chapter problems here are original exposition.

API behavior was checked against installed PyTorch 2.13.0 documentation and actual execution, including the documented reference-scaled comparison in `torch.testing.assert_close`. Its [official reference](https://docs.pytorch.org/docs/stable/testing.html) may track a newer release; the example's pinned runtime and explicit predicate define the tested behavior. The custom contract deliberately rejects all non-finite values for this finite-output task rather than inheriting every generic comparator policy.

Depth **M**: explain the rounding model and tolerance contracts, and derive the controlled residual-versus-error case using 2.7. [The section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/2.8.json) distinguishes author execution from pending independent review and reader trials. No general solver-stability theorem, universal tolerance or cross-platform bitwise guarantee is claimed.
