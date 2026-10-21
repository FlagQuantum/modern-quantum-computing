# 3. Single-Qubit States and Rotations

**Working draft: sections 3.1–3.2 · Writing Baseline 1.0 · October 21, 2026.** Author execution is recorded separately from independent mathematical, implementation and reader review, all pending. This is not an accepted chapter. Examples use released FlagQuantum 0.3.1 and PyTorch 2.13.0 on CPU with complex128 statevectors.

<span id="sec-single-qubit-states-and-rotations-1"></span>

## 3.1 The pure-state postulate and physical equivalence

A simulator stores an array. A physical state is not identified with every detail of that array: multiplying every amplitude by the same complex number of modulus one changes the array but preserves the pure state it represents. We need a precise rule for this equivalence before deciding whether two simulation outputs agree.

The prerequisite is [2.2 Inner products, adjoints, and orthogonality](ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-2), including its Cauchy–Schwarz equality condition. We introduce the physical assumptions here; they do not follow from linear algebra. By the end, you should be able to distinguish vector equality, pure-state equivalence and agreement of probabilities in one measurement setting.

### The postulates: a unit vector, an equivalence, and an outcome rule

For an ideal qubit described by a **pure state**, the state space is the two-dimensional complex inner-product space $\mathbb C^2$. Pure states are the scope of this section, not a claim that every physical qubit always has such a description. Correlations with an environment and uncertain preparations will require a more general description later.

Fix two orthonormal vectors, called the **computational basis**, with the coordinate convention

$$
|0\rangle=\begin{pmatrix}1\\0\end{pmatrix},\qquad
|1\rangle=\begin{pmatrix}0\\1\end{pmatrix}.
$$

A **ket** $|\psi\rangle$ denotes a column vector. Its **bra** $\langle\psi|$ is the conjugate transpose introduced in 2.2. Here the digits label basis vectors and eventual measurement outcomes; they are not the amplitudes. State our restricted postulates as follows:

1. A pure qubit state has a unit-vector representative $|\psi\rangle=\alpha|0\rangle+\beta|1\rangle$, with complex amplitudes $\alpha,\beta$ and $\langle\psi|\psi\rangle=1$.
2. Unit vectors $|\psi\rangle$ and $u|\psi\rangle$ represent the same pure state whenever $|u|=1$. The common multiplier is a **global phase**. Equivalently, $u=e^{i\theta}$ for a real angle $\theta$.
3. An ideal computational-basis measurement returns a label $b\in\{0,1\}$ with **Born probability** $p(b)=|\langle b|\psi\rangle|^2$.

The equivalence class of representatives is often called a **ray**. We use normalized representatives, so the allowed multiplier between them has modulus one. A ray can also be specified by a nonzero unnormalized vector, but that vector must first be normalized before using the probability formula above.

These are physical modeling rules. The first two specify a state description; the third connects that description to observations. A computational-basis probability pair alone does not establish the second rule for all possible experiments. Chapter 6 will introduce general measurement rules and the state after measurement; neither is assumed in the derivations below.

### Deriving the normalization and probabilities

Expand the unit-norm condition using orthonormality. The cross terms vanish because $\langle0|1\rangle=\langle1|0\rangle=0$, and each basis vector has norm one:

$$
\begin{aligned}
\langle\psi|\psi\rangle
&=(\alpha^*\langle0|+\beta^*\langle1|)
  (\alpha|0\rangle+\beta|1\rangle)\\
&=|\alpha|^2+|\beta|^2=1.
\end{aligned}
$$

Likewise $\langle0|\psi\rangle=\alpha$ and $\langle1|\psi\rangle=\beta$. Substituting into the outcome postulate gives

$$
p(0)=|\alpha|^2,\qquad p(1)=|\beta|^2,\qquad p(0)+p(1)=1.
$$

Nonnegativity follows from squared complex moduli. The sum-one statement is a consequence of normalization and orthonormality, not an additional independent postulate. For example, $\alpha=\sqrt3/2$ and $\beta=i/2$ give probabilities $3/4$ and $1/4$. The imaginary amplitude contributes a positive probability, since $(i/2)^*(i/2)=(-i/2)(i/2)=1/4$.

In the code, this coordinate calculation becomes:

```python
u = torch.tensor([sqrt(3)/2, .5j], dtype=torch.complex128)
probabilities = u.abs().square()  # [0.75, 0.25]; not u.square()
```

For a nonzero raw vector $v=(a,b)^T$, a unit representative is $v/\sqrt{|a|^2+|b|^2}$. Dividing $(1,i)^T$ by $\sqrt2$ is a choice of normalized description, not a laboratory preparation procedure. The zero vector cannot represent a state because no division can make its norm one. Our executable comparison rejects unnormalized inputs instead of silently repairing them.

### Global phase invariance, with its logical limit

Let $|\phi\rangle=u|\psi\rangle$ with $|u|=1$. Both normalization and the computational-basis probabilities are unchanged:

$$
\langle\phi|\phi\rangle=u^*u\langle\psi|\psi\rangle=1,
\qquad
|\langle b|\phi\rangle|^2=|u\langle b|\psi\rangle|^2
=|u|^2p(b)=p(b).
$$

This checks consistency with our restricted measurement rule. It does **not** prove that any two vectors with the same probability pair are equivalent. To see the missing information, compare

$$
|\psi\rangle=\frac1{\sqrt2}\begin{pmatrix}1\\i\end{pmatrix},\qquad
|\phi\rangle=i|\psi\rangle=\frac1{\sqrt2}\begin{pmatrix}i\\-1\end{pmatrix},\qquad
|\chi\rangle=\frac1{\sqrt2}\begin{pmatrix}1\\-i\end{pmatrix}.
$$

All three give $(p(0),p(1))=(1/2,1/2)$. The first two differ by a common multiplier $i$. The first and third cannot: their nonzero first coordinates require a multiplier $1$, while their second coordinates require $-1$. Their **relative phase** differs. Section 3.2 will show how a subsequent interference experiment can reveal the difference. Here we only establish that they are different rays under the stated rule.

“Global” applies to the entire vector being compared. Changing the sign of only one amplitude is not global. Nor should a phase attached to one branch of a larger state be discarded as if it multiplied the entire larger state.

### A phase-aware comparison derived from the inner product

For two unit vectors $a,b$, define their overlap $c=\langle a|b\rangle$. If $b=ua$ with $|u|=1$, then $c=u$. Cauchy–Schwarz from 2.2 gives $|c|\leq1$, with equality exactly when the nonzero vectors are linearly dependent. Unit norms then force the dependence multiplier to have modulus one. Therefore, in exact arithmetic,

$$
a\text{ and }b\text{ represent the same pure state}
\quad\Longleftrightarrow\quad |\langle a|b\rangle|=1.
$$

For a comparison in coordinates, align $b$ to $a$. For any $|z|=1$, expanding the squared distance gives

$$
\|a-zb\|^2=2-zc-z^*c^*=2-2\operatorname{Re}(zc).
$$

Since $\operatorname{Re}(zc)\leq|c|$, the smallest squared distance is $2-2|c|$. For $c\ne0$, choose $z=c^*/|c|$ to attain it. If $c=0$, every phase gives squared distance $2$; no phase can align these orthogonal vectors into equality. The implementation computes a residual directly:

```python
c = torch.vdot(a, b)                    # conjugates a, as the overlap requires
phase = c.conj() / c.abs() if c.abs().item() != 0 else 1.0
distance = torch.linalg.vector_norm(a - phase*b).item()
```

At zero overlap, `phase=1` is only a convention for evaluating the distance. It is not a claim of equivalence. For nearly zero overlap, the selected phase can be sensitive to roundoff, while the distance remains near $\sqrt2$. Near equivalence, directly subtracting $2-2|c|$ can also lose small differences through cancellation; the script uses the aligned residual, with an explicit absolute tolerance. A small residual is numerical evidence under that tolerance, not an exact mathematical identity.

For the three hand vectors, $\langle\psi|\phi\rangle=i$ and $\langle\psi|\chi\rangle=0$. The raw distance between $\psi$ and $\phi$ is $\sqrt2$, but the aligned distance is zero. The aligned distance between $\psi$ and $\chi$ stays $\sqrt2$. Omitting the conjugate in the alignment multiplier sends $i\psi$ to $-\psi$ and produces the wrong distance $2$.

### Runnable verification and expected output

The complete executable is [pure_states.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/pure_states.py). From the repository root in the [pinned example environment](https://github.com/FlagQuantum/modern-quantum-computing#run-the-examples):

```bash
python -m pip install -r requirements-examples.txt
python examples/foundations/pure_states.py
```

The script first checks the complex-coordinate example against explicit scalar arithmetic and the hand overlap values. It then runs the real-amplitude cases $H|0\rangle$ and $ZH|0\rangle$ in released FlagQuantum 0.3.1. These preparation gates are the earlier Chapter 1 preview; their general theory is not a prerequisite for the postulates here. Their independently specified reference coordinates are $(1,1)^T/\sqrt2$ and $(1,-1)^T/\sqrt2$.

The actual API-to-formula correspondence is:

| Formula or obligation | Executed code |
|---|---|
| Ideal one-qubit preparation | `fq.Circuit(1, dtype=torch.complex128)`, then `circuit.h(0)` and optionally `circuit.z(0)` |
| Ideal computational-basis probabilities | `fq.run(circuit, outputs=[fq.probabilities()], options=OPTIONS)` |
| Simulator representative for comparison | `result.statevector()[0]`, validated as a finite CPU complex128 unit vector of shape `(2,)` |
| Squared moduli and probability reference | `v.abs().square()`; direct reference pairs checked with `torch.testing.assert_close` |
| Global phase on a stored representative | `1j*v`; this is array arithmetic, not a submitted gate or physical experiment |
| Equivalence test with declared tolerance | `aligned_distance(v, 1j*v) < 1e-12` |

`OPTIONS` requires the PyTorch CPU complex128 statevector method and disallows backend fallback and approximation. Statevector inspection is a simulator diagnostic, not a physical-device readout. The script checks the raw batch shape `(1,2)` before selecting its single state.

Expected output in the author-tested environment:

```text
complex example: P(0)=0.500000000, P(1)=0.500000000
global i: raw distance=1.414213562, aligned distance=0.000000000
relative sign: same probabilities, aligned distance=1.414213562
FlagQuantum H: P(0)=0.500000000, P(1)=0.500000000
FlagQuantum H then Z: P(0)=0.500000000, P(1)=0.500000000
Unequal probabilities, zero overlap, and 6 invalid-input cases checked.
Scalar references and released FlagQuantum agree (atol=1e-12); no shots or hardware.
```

The absolute tolerance is $10^{-12}$ with zero relative tolerance for unit-scale coordinates/probabilities. The validator rejects zero norm, a scaled non-unit vector, wrong shape, complex64, NaN and infinity. A separate exact zero-overlap basis pair exercises the zero branch. These checks cover small specified inputs; they do not establish the postulates experimentally, verify a physical preparation, sample measurement frequencies or provide state tomography.

### Understanding checks and transfer problems

**3.1-A — Postulate or consequence?** Classify: (i) pure qubit representatives have unit norm; (ii) computational-basis probabilities sum to one; (iii) global-phase multiples represent the same state; (iv) vectors with the same computational-basis probabilities represent the same state.

**3.1-B — Normalize without inventing an operation.** For $v=(2,2i)^T$, find a unit representative and its probability pair. Is dividing the vector by its norm a demonstrated physical preparation? What fails for $v=0$?

**3.1-C — Repair the comparison.** A program computes $c=\langle a|b\rangle$ and compares $a$ with $(c/|c|)b$. Use $b=ia$ to diagnose the error and give the correct multiplier. What should it do when $c=0$?

**3.1-D — Transfer to a boundary state.** Are $(0,1)^T$ and $(0,-i)^T$ equivalent? Explain why their zero first coordinate cannot determine the phase. Contrast them with the two non-equivalent equal-probability vectors above.

### Answers

**A.** (i) and (iii) are our state-description postulates. (ii) follows by orthonormal expansion and the Born rule. (iv) is false: $\psi$ and $\chi$ have equal probability pairs but incompatible coordinate ratios. A computational-basis distribution contains less information than a pure-state ray.

**B.** The norm is $\sqrt8=2\sqrt2$, giving $(1,i)^T/\sqrt2$ and $(1/2,1/2)$. This converts a mathematical description; it gives no laboratory preparation protocol. The zero vector has norm zero and cannot be normalized.

**C.** Here $c=i$, so the wrong multiplier gives $i(ia)=-a$ and distance $2$. Use $c^*/|c|=-i$ instead. For zero overlap, division is undefined; any unit phase gives distance $\sqrt2$. Return that nonzero distance or compute it using a documented phase convention, never report equivalence.

**D.** They are equivalent with common multiplier $-i$. The equation $0=u0$ gives no constraint on $u$; the second coordinate determines it. For $\psi$ and $\chi$, both coordinates are nonzero and demand different multipliers. Looking at only one coordinate or only squared moduli misses that contradiction.

### Sources, limits, and next step

The assigned sources are Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010), **§2.2.1, printed pp.80–81** (unit state vectors and a qubit), and **§2.2.3, printed pp.84–85**, especially Eq.(2.96) and the computational-basis example on p.85. These correspond to [NC:2.2.1 and NC:2.2.3 in the exact-source catalog](../references/proof-sources.md). For the global/relative-phase distinction, supplementary **§2.2.7, printed p.93** supplies the more general observational argument. Our restricted presentation states phase equivalence explicitly and derives only its fixed-basis consistency check here. The phase-alignment proof uses the earlier Cauchy–Schwarz equality condition, not a new physical postulate or an experimental result.

The physical assumptions apply to an ideal pure qubit with a fixed basis; general measurements, post-measurement states and mixed states remain outside this section. See the [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/3.1.json) for execution provenance and pending reviews. Continue with the working draft [3.2 Relative phase and interference](#sec-single-qubit-states-and-rotations-2), where a subsequent operation turns the information missing from one probability pair into an observable difference.

<span id="sec-single-qubit-states-and-rotations-2"></span>

## 3.2 Relative phase and interference

In 3.1 we found different pure states with identical computational-basis probabilities. How can a later experiment tell them apart? A measurement that reads the same squared moduli cannot recover the missing information. We first combine the amplitudes coherently, and then apply the probability rule.

The prerequisites are [3.1](#sec-single-qubit-states-and-rotations-1), for normalized pure states and Born probabilities, and [2.3](ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-3), for linear maps, matrix order and basis coordinates. We will derive the complex interference term in full and identify when a chosen experiment can, or cannot, reveal relative phase. General evolution postulates, measurement updates and noise models remain for later sections.

### Specify the phase and the experiment

For nonzero amplitudes, write

$$
\alpha=r e^{ia},\qquad \beta=s e^{ib},\qquad
r,s>0,\quad r^2+s^2=1.
$$

Here $a,b$ are real phase angles in radians; $r,s$ are magnitudes. We use Euler's identity $e^{ix}=\cos x+i\sin x$. Adding $2\pi$ to an angle gives the same complex phase. Multiplying the whole vector by $e^{-ia}$ selects the representative

$$
|\psi_\phi\rangle=r|0\rangle+s e^{i\phi}|1\rangle,
\qquad \phi=b-a\pmod{2\pi}.
$$

The angle $\phi$ is a **relative phase in this specified basis**. A common phase shifts $a,b$ equally and leaves their difference unchanged. If either amplitude is zero, its phase is undefined; a phase assigned only to that absent component cannot affect the state. A relative phase also depends on the phase conventions for the basis vectors. We hold those conventions, the preparation and the analyzer fixed while varying $\phi$.

Our ideal experiment uses two explicitly defined linear maps:

$$
D(\phi)=\begin{pmatrix}1&0\\0&e^{i\phi}\end{pmatrix},
\qquad H=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}.
$$

$D$ changes only the outcome-1 amplitude. $H$, the Hadamard map, replaces amplitudes $\alpha,\beta$ by $(\alpha+\beta)/\sqrt2$ and $(\alpha-\beta)/\sqrt2$. These transfer rules specify the ideal preparation/analyzer model for this experiment. We are not deriving laboratory controls or assuming the general evolution theory of 3.4.

Both maps preserve normalization. For $D$, multiplying one coordinate by a number of modulus one preserves its squared modulus. For $H$, direct expansion gives

$$
\frac{|\alpha+\beta|^2+|\alpha-\beta|^2}{2}
=|\alpha|^2+|\beta|^2.
$$

The cross terms cancel, so normalized inputs remain valid states to which the Born rule applies. Preparing from $|0\rangle$ with **$H$ first, then $D(\phi)$** produces the balanced state

$$
D(\phi)H|0\rangle
=\frac{|0\rangle+e^{i\phi}|1\rangle}{\sqrt2}.
$$

The rightmost matrix acts first. This is an active preparation, with no intermediate measurement. Separate ideal runs either read the computational basis directly or apply an analyzer and then read it. The code's two runs do not measure one qubit and subsequently reuse its pre-measurement amplitudes.

### Derive the interference term before substituting a phase

Let $|\psi\rangle=\alpha|0\rangle+\beta|1\rangle$ be any normalized pure qubit. After $H$, the outcome-0 amplitude is $(\alpha+\beta)/\sqrt2$. Applying the probability rule from 3.1 and multiplying out every factor,

$$
\begin{aligned}
p_H(0)
&=\frac12(\alpha+\beta)^*(\alpha+\beta)\\
&=\frac12\bigl(|\alpha|^2+|\beta|^2
              +\alpha^*\beta+\beta^*\alpha\bigr)\\
&=\frac12+\operatorname{Re}(\alpha^*\beta).
\end{aligned}
$$

The last step uses normalization and the identity $z+z^*=2\operatorname{Re}z$. Similarly,

$$
\begin{aligned}
p_H(1)
&=\frac12(\alpha-\beta)^*(\alpha-\beta)\\
&=\frac12\bigl(|\alpha|^2+|\beta|^2
              -\alpha^*\beta-\beta^*\alpha\bigr)\\
&=\frac12-\operatorname{Re}(\alpha^*\beta).
\end{aligned}
$$

The **interference contribution** is the cross term, with opposite signs in the two outputs. It redistributes probability while preserving $p_H(0)+p_H(1)=1$. With $\alpha=r$ and $\beta=s e^{i\phi}$, it becomes $rs\cos\phi$, yielding

$$
p_H(0)=\frac12+rs\cos\phi,\qquad
p_H(1)=\frac12-rs\cos\phi.
$$

These are valid probabilities: $(r-s)^2\geq0$ implies $2rs\leq r^2+s^2=1$, hence $rs\leq1/2$. Their range is therefore within $[0,1]$. If one amplitude vanishes, $rs=0$ and this experiment has no phase dependence.

For a common phase multiplier $u$ with $|u|=1$, the cross term is unchanged because $(u\alpha)^*(u\beta)=u^*u\alpha^*\beta=\alpha^*\beta$. For a relative phase on $\beta$ alone it generally changes. This is the algebraic distinction between the two kinds of phase in this experiment.

For another specified linear analyzer, an output amplitude has the form $A\alpha+B\beta$, where $A,B$ are that output row's matrix entries. The same expansion gives

$$
|A\alpha+B\beta|^2
=|A|^2|\alpha|^2+|B|^2|\beta|^2
 +2\operatorname{Re}\bigl(A^*B\alpha^*\beta\bigr).
$$

This identity explains why the analyzer matters: its complex coefficients select which part of the overlap contributes. To interpret all outputs as probabilities, the full analyzer must preserve normalization, as we checked explicitly for our chosen maps.

### Balanced fringes and a probability-only mistake

For $r=s=1/\sqrt2$, direct computational-basis probabilities are always $(1/2,1/2)$. After $H$ they become

$$
p_H(0)=\frac{1+\cos\phi}{2},\qquad
p_H(1)=\frac{1-\cos\phi}{2}.
$$

At $\phi=0$, the two amplitudes add in output 0 and cancel in output 1. At $\phi=\pi$, the addition and cancellation exchange outputs. At $\phi=\pm\pi/2$, the cross term is purely imaginary, so its real part vanishes. Varying the phase produces an **interference fringe**, the oscillation of a probability with the controlled phase.

A tempting incorrect calculation discards the input phases and propagates the two input probabilities separately:

$$
p_{\mathrm{drop}}(0)
=\frac12|\alpha|^2+\frac12|\beta|^2=\frac12.
$$

It omits the cross term and predicts no fringe, even for a known coherent input. This is not the calculation for the stated experiment. Intermediate measurements or uncontrolled variation of relative phase would change the experiment; they cannot be inserted silently into an amplitude calculation. We do not need a general noise or measurement-update model to detect this mismatch.

For an unbalanced example, $r=3/5$ and $s=4/5$ give

$$
p_H(0)=\frac12+\frac{12}{25}\cos\phi.
$$

The minimum is $1/50=0.02$ and the maximum $49/50=0.98$. Defining the fringe visibility for this scan as $\mathcal V=(p_{\max}-p_{\min})/(p_{\max}+p_{\min})$, we obtain $\mathcal V=2rs=24/25$. This definition presumes the specified phase scan and ideal analyzer. Reduced contrast here comes from unequal amplitudes; it is not evidence of decoherence.

### One analyzer can miss a difference

The states $(|0\rangle+i|1\rangle)/\sqrt2$ and $(|0\rangle-i|1\rangle)/\sqrt2$ from 3.1 give the same probabilities both directly and after $H$. Their phases are $\pi/2$ and $-\pi/2$, and cosine is even. Thus **different rays need not produce different probabilities in every chosen setting**.

To reveal this difference, apply a known phase $D(-\delta)$ before the final $H$. Call $H D(-\delta)$ the analyzer; $\delta$ is a controlled real angle, not a fitted value inferred from one observed outcome. The output-0 amplitude and probability are

$$
\frac{\alpha+e^{-i\delta}\beta}{\sqrt2},\qquad
p_\delta(0)=\frac12+
\operatorname{Re}\bigl(\alpha^*e^{-i\delta}\beta\bigr).
$$

For the balanced family, substituting the amplitudes gives

$$
p_\delta(0)=\frac{1+\cos(\phi-\delta)}2,
\qquad p_\delta(1)=1-p_\delta(0).
$$

Choosing $\delta=\pi/2$ produces $p_\delta(0)=1$ for the positive-i state and $0$ for the negative-i state. This is an ideal distinguishing setting for this specified pair, not a claim that arbitrary different pure states are perfectly distinguishable.

We can also describe the plain $H$ analyzer as reading coordinates in the basis $|+\rangle=(|0\rangle+|1\rangle)/\sqrt2$, $|-\rangle=(|0\rangle-|1\rangle)/\sqrt2$. Their overlaps with the input are the sum and difference amplitudes above. By 2.3, this passive coordinate description uses the conjugate-transpose basis matrix. Here it equals $H$ itself. The equivalence of the probability calculations does not mean merely changing coordinate labels physically applies a gate: the code actively applies $H$ before a fixed computational-basis readout.

### Formula-to-code experiment and independent verification

The full runnable program is [relative_phase.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/relative_phase.py). In the [pinned Python 3.12 example environment](https://github.com/FlagQuantum/modern-quantum-computing#run-the-examples), run:

```bash
python -m pip install -r requirements-examples.txt
python examples/foundations/relative_phase.py
```

The central released FlagQuantum 0.3.1 construction is:

```python
circuit = fq.Circuit(1, dtype=torch.complex128)
circuit.h(0)
circuit.phase(0, theta=phi)
if recombine:
    circuit.phase(0, theta=-delta)
    circuit.h(0)
result = fq.run(circuit, outputs=[fq.probabilities()], options=OPTIONS)
```

| Mathematical step | Code and check |
|---|---|
| $D(\phi)H\lvert0\rangle$ prepares two coherent amplitudes | `h(0)` followed by `phase(0, theta=phi)`; direct-state coordinates checked against `(S, S*cmath.exp(1j*phi))` |
| $H D(-\delta)$ combines those amplitudes | Optional negative analysis phase followed by `h(0)`; matrix order follows chronological API calls |
| Apply the computational-basis Born rule | `result.probabilities`; compared both with squared moduli and independent scalar amplitude arithmetic |
| Check the analytic balanced fringe | `.5*(1+cos(phi-delta))` and its complementary probability |
| Inspect the simulated coordinates | `result.statevector()`; expected batch shape `(1,2)`, CPU complex128, finite entries |
| Preserve the declared execution model | `OPTIONS` requires PyTorch CPU complex128 statevector execution, with fallback and approximation disabled |

The installed release's `phase` operator schema takes one qubit and parameter `theta`; its matrix is $D(\theta)$ as defined here. We inspected and executed this API. We use `phase`, rather than assuming a similarly named axis rotation has identical coordinate phases. General rotation conventions belong to 3.5.

Expected output in the author-tested environment:

```text
phi/pi=0.0: direct=(0.500000000, 0.500000000), after H=(1.000000000, 0.000000000)
phi/pi=0.5: direct=(0.500000000, 0.500000000), after H=(0.500000000, 0.500000000)
phi/pi=1.0: direct=(0.500000000, 0.500000000), after H=(0.000000000, 1.000000000)
phi/pi=1.5: direct=(0.500000000, 0.500000000), after H=(0.500000000, 0.500000000)
phi/pi=2.0: direct=(0.500000000, 0.500000000), after H=(1.000000000, 0.000000000)
+i relative phase: P(0) after H=0.500000000, shifted analyzer=1.000000000
-i relative phase: P(0) after H=0.500000000, shifted analyzer=0.000000000
17-point sweep: scalar amplitudes, analytic fringes and FlagQuantum agree (atol=1e-12).
Unbalanced fringe: min P(0)=0.020000000, max P(0)=0.980000000.
Global-phase, absent-path, conjugation, operation-order and probability-only checks passed.
```

The script checks 17 additional phase values with a non-cardinal analysis angle $\pi/7$, compares standard-library complex amplitudes with simulator outputs and analytic probabilities, and checks unbalanced scalar cases independently. It rejects the probability-only and missing-conjugate formulas using concrete counterexamples. For the order test, moving the preparation phase before the first $H$ makes it act trivially on $|0\rangle$; the subsequent two $H$ maps return $|0\rangle$, so the intended phase dependence disappears.

Comparisons use absolute tolerance $10^{-12}$ and zero relative tolerance for unit-scale amplitudes/probabilities. Printed zeros may contain roundoff below that budget; they are not claims of bitwise exactness. This is author execution in the pinned release, not independent implementation review. These are ideal probabilities and simulator diagnostics, with no shots, physical-device data, intermediate measurements or state-tomography claim.

### Understanding checks and transfer problems

**3.2-A — Derive an unbalanced prediction.** For $\alpha=3/5$ and $\beta=(4/5)e^{i\phi}$, derive both output probabilities with analyzer phase $\delta$. Find the range and visibility, and explain why a visibility below one does not by itself diagnose noise.

**3.2-B — Diagnose a missing conjugate.** A program uses $1/2+\operatorname{Re}(\alpha e^{-i\delta}\beta)$ for output 0. Why do tests with real $\alpha$ miss the bug? Evaluate the correct and incorrect predictions at $\alpha=i/\sqrt2$, $\beta=1/\sqrt2$, $\delta=\pi/2$.

**3.2-C — Transfer the analyzer.** Direct readout and a plain $H$ analyzer cannot distinguish the positive-i and negative-i states above. Pick a known $\delta$ that distinguishes them. Would equal probabilities in these two unshifted settings prove their statevectors equal up to phase?

**3.2-D — Change the preparation order.** Starting from $|0\rangle$, a student executes `phase(phi)`, then `h`, then `h`, expecting the fringe from `h`, then `phase(phi)`, then `h`. Compute both output-0 probabilities and identify which amplitude ever acquired the phase in the mistaken preparation.

### Answers

**A.** Substitute into $\alpha^*e^{-i\delta}\beta=(12/25)e^{i(\phi-\delta)}$. The outputs are $1/2\pm(12/25)\cos(\phi-\delta)$. Each ranges from $1/50$ to $49/50$, with $\mathcal V=24/25$. These are normalized coherent amplitudes throughout; their unequal magnitudes limit the cancellation even in the ideal model. A noise diagnosis would need a separate specified model and evidence.

**B.** If $\alpha$ is real, $\alpha^*=\alpha$, so both formulas coincide. For the proposed complex input, $\alpha^*e^{-i\delta}\beta=(-i)(-i)/2=-1/2$, giving correct probability $0$. The incorrect expression gives $i(-i)/2=1/2$ and hence probability $1$. Conjugation is essential even though both wrong and right values lie in $[0,1]$.

**C.** Choose $\delta=\pi/2$; output-0 probabilities become $1$ and $0$. The unshifted settings do not determine the sign of this relative phase. Equal probability pairs in them do not imply equal rays, as the incompatible coordinate ratios already show.

**D.** The intended circuit has output-0 probability $(1+\cos\phi)/2$. In the mistaken circuit $D(\phi)|0\rangle=|0\rangle$: the only amplitude multiplied by $e^{i\phi}$ was zero. The two subsequent Hadamard maps give $H^2|0\rangle=|0\rangle$, so output 0 has probability $1$ for every $\phi$. Matrix order changes the preparation, not just its written notation.

### Sources, limits, and next step

The assigned source is [NC:2.2.7](../references/proof-sources.md#source-nc-2-2-7), Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010), **§2.2.7, printed p.93**, including the global/relative-phase distinction and the pair in Eq.(2.121). The source was consulted; the fringe derivation, shifted-analyzer experiment, independent checks and exercises here are original exposition. The local $H,D$ transfer rules and execution assumptions are stated explicitly, rather than importing the later general evolution theory.

Depth **F**: the probability expansion, phase dependence, normalization, range and analyzer choice are derived, including zero-amplitude and fixed-setting limits. The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/3.2.json) separates author checks from pending independent reviews and reader trials. A controlled ideal phase scan does not validate hardware control, establish coherence of an unknown preparation or reconstruct an arbitrary unknown state from one outcome. Next: [3.3 The Bloch-sphere representation](../section-plans/01-foundations.md#sec-single-qubit-states-and-rotations-3).
