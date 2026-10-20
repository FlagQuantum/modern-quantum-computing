# 2. Complex Vectors, Operators, and Numerical Reasoning

**Working draft: section 2.1 · Writing Baseline 1.0 · October 21, 2026.** Sections 2.2–2.8 remain planned. Author execution checks are recorded separately from independent mathematical, implementation and reader review, which remain pending. This is not an accepted chapter. The example uses Python 3.12 and its standard library.

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

The next planned lesson, [2.2 Inner products, adjoints, and orthogonality](../section-plans/01-foundations.md#sec-complex-vectors-operators-and-numerical-reasoning-2), uses these conjugation rules to compare different vectors, rather than just the coordinates of one vector with themselves.

### Source, status, and limits

The assigned locator is [NC:2.1.1](../references/proof-sources.md#source-nc-2-1-1), Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010), §2.1.1 beginning on printed p. 62. The immediately preceding coordinate introduction on printed pp. 61–62 and Figure 2.1 on p. 62 supply the companion vector and conjugation conventions. Those specific pages were consulted from the previously supplied local source copy. The elementary scalar bridge, component proofs, examples and exercises here are original; §2.1.1 is not being cited as a source of every proof written above.

Depth **F**: full component derivations of the stated conjugation and modulus identities, including finite-vector consequences. [The execution and section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/2.1.json) separates author checks from pending independent reviews. No theorem is deferred to an exercise, and no quantum postulate is asserted.
