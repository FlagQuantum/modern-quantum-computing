<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-6"></span>

## 44.6 Precision, stability, and normalization drift

An ideal unitary preserves norm. A computed vector can gradually gain or lose norm, but a norm close to one does not certify the intended state. A wrong rotation, a lost relative phase, or an incorrect qubit convention can preserve norm perfectly. We need a state-error budget as well as a normalization diagnostic.

The prerequisites are [44.2, indexed local execution](#sec-exact-simulation-tensor-execution-and-numerical-reliability-2), and [2.8, floating-point contracts](ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-8), including the induced Euclidean operator norm imported there from 2.7. Depth **M**: derive a telescoping norm budget and distinguish radial correction from recovering lost phase information. We supply the finite derivations used in the laboratory; we do not assert a rounding theorem for every native kernel.

Run the eight Python blocks in order in a fresh namespace from the repository root. The complete [companion](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/precision_drift.py) and `python scripts/check_precision_drift_prose.py` check the actual snippets and printed outputs. Angles are in **radians**; state norms, probabilities and the Pauli observables in this section are dimensionless. The tested runtime is released FlagQuantum 0.3.1, PyTorch 2.13.0, Python 3.12.14, CPU, with `complex64` and `complex128` explicitly requested. No native result is normalized or phase-aligned before comparison.

### 44.6.1 Precision is a representation contract

A complex64 coordinate has two float32 components; complex128 has two float64 components. In the normalized range, round-to-nearest arithmetic with $p$ significant binary digits has unit roundoff $u=2^{-p}$, while the spacing above one is $\epsilon=2u$. This model excludes overflow and underflow. Neither number by itself bounds an entire circuit's error.

For example, $d=2^{-25}$ is too small to survive addition to one in float32. The exact expression $(1+d)-1=d$ becomes zero. Casting that zero to float64 retains zero; recomputing from the original inputs is different. A small absolute error in the addition becomes a relative error of one in the tiny difference. This is cancellation and sensitivity, not evidence that every subtraction has a large absolute rounding error. A stable method controls error relative to its declared problem; **backward stability** means that the computed answer is an exact answer for suitably small input perturbations. We do not infer that property for FlagQuantum from these tests.

**Formula → code → result: component precision and lost increments.**

```python
import math
import torch
from examples.foundations import precision_drift as n
u32 = torch.finfo(torch.float32).eps/2
u64 = torch.finfo(torch.float64).eps/2
one = torch.tensor(1., dtype=torch.float32)
d = 2**-25
assert float((one+d)-one) == 0
assert float(((one+d)-one).double()) == 0
assert float((torch.tensor(1., dtype=torch.float64)+d)-1) == d
print(u32 == 2**-24, u64 == 2**-53, "casting does not recover the increment")
```

```text
True True casting does not recover the increment
```

### 44.6.2 Derive a state-error budget before inspecting drift

Let $v_0$ be a normalized exact vector and $U_1,\ldots,U_L$ exact unitary operators on the same register. Define $v_j=U_jv_{j-1}$. A finite computed vector $\widehat v_j$ has a local residual

$$
f_j=\widehat v_j-U_j\widehat v_{j-1},\qquad
 d_j=\widehat v_j-v_j,
 \qquad d_j=U_jd_{j-1}+f_j.
$$

Substitute the preceding recurrence repeatedly. With an empty product interpreted as the identity,

$$
d_L=U_L\cdots U_1d_0+
 \sum_{j=1}^{L}U_L\cdots U_{j+1}f_j.
$$

Every intervening product is unitary. It preserves Euclidean norm, so the triangle inequality gives the **telescoping residual budget**

$$
E_L:=\|d_L\|_2\le\|d_0\|_2+\sum_{j=1}^{L}\|f_j\|_2
 \le E_0+\sum_{j=1}^{L}\eta_j=:B_L,
$$

provided the declared nonnegative numbers $\eta_j$ bound the corresponding residuals. If every residual has a justified common bound $\eta$, this becomes $E_0+L\eta$. Assuming such an $\eta$ is different from setting it equal to machine epsilon. Gate arity, reduction order, intermediate magnitudes, matrix construction and backend arithmetic all matter.

For a normalized ideal final vector $v$, write $w=v+d$, $E=\|d\|_2$ and $r=\|w\|_2$. Reverse triangle gives $|r-1|\le E$. Expanding the squared norm gives

$$
\left|r^2-1\right|
 =\left|2\operatorname{Re}\langle v,d\rangle+\|d\|_2^2\right|
 \le 2E+E^2\le 2B_L+B_L^2.
$$

Thus a state-error bound controls drift. The converse does not follow: norm is only one scalar constraint. For an exactly radial positive error $d=av$, $a\ge0$, both the state and drift bounds are attained. The following fixture uses exact dyadic additions and $U_j=I$; its errors are deliberately injected, not observed native rounding.

**Formula → code → result: four radial residuals with an exact reference.**

```python
v0 = torch.tensor([1,0], dtype=torch.complex128)
w = v0.clone()
eta = 2**-12
for _ in range(4):
    w = w + torch.tensor([eta,0], dtype=torch.complex128)
m = n.metrics(w,v0)
assert m['error'] == 4*eta
assert m['drift'] == m['bound']
print(m['error'], m['drift'], "telescoping and drift bounds attained")
```

```text
0.0009765625 0.0019540786743164062 telescoping and drift bounds attained
```

### 44.6.3 Separate represented gates from execution residuals

Suppose a represented local gate is $A_j=U_j+\Delta_j$ and the actual arithmetic satisfies

$$
\widehat v_j=A_j\widehat v_{j-1}+e_j.
$$

Then $f_j=\Delta_j\widehat v_{j-1}+e_j$, and the induced norm inequality from 2.7 yields

$$
\|f_j\|_2\le\|\Delta_j\|\,\|\widehat v_{j-1}\|_2+\|e_j\|_2.
$$

The first term includes representation or parameter error relative to the specified $U_j$; the second includes arithmetic error relative to the represented matrix. An intentional approximate synthesis adds its own gate-model error. Changing precision does not remove a wrong gate or an incorrect input parameter.

For intuition, if $A_j$ alone were applied in exact arithmetic, its unitarity defect would obey

$$
A_j^\dagger A_j-I=U_j^\dagger\Delta_j+\Delta_j^\dagger U_j+\Delta_j^\dagger\Delta_j,
\qquad \|A_j^\dagger A_j-I\|\le2\|\Delta_j\|+\|\Delta_j\|^2.
$$

Multiplying the left side between a vector and its adjoint bounds that step's squared-norm change by this defect times the input squared norm. Conversely, a wrong but exactly unitary $A_j$ has zero defect. Unitarity testing cannot identify which unitary was intended.

The book helper `local_trace` applies a two-coordinate RY matrix in the selected dtype, then estimates every residual in complex128. It checks both the direct residual recurrence and the matrix-representation/arithmetic split. The binary64 matrix used by that trace is itself a finite reference; accumulated reference arithmetic and norm calculations are not exact. The small additive guard below is an implementation-check allowance, **not** a rigorous bound on all possible residuals. It does not inspect hidden native intermediates.

**Formula → code → result: residuals at every prefix of a classical execution.**

```python
low, reference, trace = n.local_trace(64, .037, torch.complex64)
budget = sum(row['eta'] for row in trace)
assert n.norm(low.to(torch.complex128)-reference) <= budget+2e-13
assert all(row['error'] <= row['budget']+2e-13 for row in trace)
print(len(trace), "prefix residual inequalities passed; estimates are not certificates")
```

```text
64 prefix residual inequalities passed; estimates are not certificates
```

### 44.6.4 Compare raw native evolution with an independent scalar target

Submit $L$ calls to RY on qubit 0, then $L$ calls to P on qubit 0, then CX with control 0 and target 1. The initial register is $|00\rangle$. Since RY rotations about the same axis add angles and P is diagonal,

$$
|v_L\rangle=c_L|00\rangle+e^{iL\phi}s_L|11\rangle,
\quad c_L=\cos(L\theta/2),\quad s_L=\sin(L\theta/2).
$$

The signed $s_L$ is retained. The computational probabilities are $(c_L^2,0,0,s_L^2)$; applying $X\otimes X$ exchanges the two nonzero coordinates, so

$$
\langle XX\rangle=2\operatorname{Re}(c_L e^{iL\phi}s_L)
 =\sin(L\theta)\cos(L\phi).
$$

The analytic target uses the exact real values represented by the supplied Python float angles. The companion converts those floats with `Decimal.from_float`, accumulates angles in a declared decimal context and evaluates sine/cosine Taylor sums with 180 terms at 60 and 80 digits. Their binary64 exports agree for the tested cases. This is an independent high-precision diagnostic; it is not interval arithmetic, a certified transcendental evaluation, or a claim to recover the intended decimal angle from a previously rounded float.

**Formula → code → result: actual gate calls, requests and raw comparisons.**

```python
from dataclasses import replace
import flagquantum as fq
from examples.foundations.tensor_spaces import OPTIONS
for dtype, precision, tolerance in [(torch.complex64,'complex64',3e-4),
                                     (torch.complex128,'complex128',1e-11)]:
    L, theta, phi = 33, 1/32, -1/64  # angles in radians
    circuit = fq.Circuit(2,dtype=dtype)
    for _ in range(L): circuit.ry(0,theta)
    for _ in range(L): circuit.p(0,phi)
    circuit.cx(0,1)
    result = fq.run(circuit,
        outputs=[fq.probabilities(name='all'),
                 fq.expectation(fq.X(0)@fq.X(1),name='xx')],
        options=replace(OPTIONS,precision=precision))
    raw = result.statevector()[0]
    target = n.reference(L,theta,phi)
    report = n.metrics(raw,target)
    assert raw.dtype == dtype and report['error'] < tolerance
    assert report['drift'] < tolerance
    probabilities = result.measurement('all').value[0].to(torch.float64)
    assert float((probabilities-raw.to(torch.complex128).abs().square()).abs().max()) < tolerance
    expected_xx = 2*(target[0].conj()*target[3]).real.item()
    assert abs(float(result.expectation('xx')[0])-expected_xx) < 2*tolerance
    print(precision, "raw state, drift, probabilities and XX passed")
```

```text
complex64 raw state, drift, probabilities and XX passed
complex128 raw state, drift, probabilities and XX passed
```

There are $2L+1$ submitted gate calls, not a certified count of backend floating operations. No assertion requires error or norm drift to increase monotonically with depth, or complex128 to win in every individual coordinate. Both precisions must satisfy their declared absolute tolerances: $3\times10^{-4}$ and $10^{-11}$ for these bounded cases, with zero relative tolerance. These are validation thresholds, not estimates of every circuit's physical or numerical accuracy. `allow_approximate=False` does not turn finite arithmetic into symbolic arithmetic.

### 44.6.5 Renormalization changes radius, not direction

For $w\ne0$, define $\widetilde w=w/r$. In exact arithmetic,

$$
\|\widetilde w-w\|_2=|1-r|,\qquad
\|\widetilde w-v\|_2\le|1-r|+E\le2E.
$$

The first equality follows by factoring $(1/r-1)w$. The second follows by adding and subtracting $w$ and using the reverse triangle bound. Normalization can completely remove a positive radial error, but cannot change the ray of $w$. It is not guaranteed to reduce the full vector error for every $w$; it provides the displayed bound. Its floating implementation introduces additional error.

For $|+\rangle=(|0\rangle+|1\rangle)/\sqrt2$ and $|-\rangle=(|0\rangle-|1\rangle)/\sqrt2$, both norms equal one, yet their X expectations are $+1$ and $-1$. Normalizing the wrong vector cannot restore the relative phase. A missing global phase is also unrecoverable from norm alone; it is unobservable for an isolated ray but can be relative phase when the preparation becomes one branch of a controlled construction. Full-vector comparisons here fix the declared circuit phase and do not silently align it.

**Formula → code → result: radial repair and a phase-error counterexample.**

```python
plus = torch.tensor([1,1],dtype=torch.complex128)/math.sqrt(2)
minus = plus*torch.tensor([1,-1])
radial = n.normalize(w)
phase_wrong = n.normalize(minus)
assert torch.equal(radial,v0)
assert abs(n.norm(phase_wrong)-1) < 1e-15
assert n.norm(phase_wrong-plus) > 1.4
X = torch.tensor([[0,1],[1,0]],dtype=torch.complex128)
assert abs(float(torch.vdot(plus,X@plus).real)-1) < 1e-15
assert abs(float(torch.vdot(phase_wrong,X@phase_wrong).real)+1) < 1e-15
print("radial error removed; relative-phase error and opposite X predictions remain")
```

```text
radial error removed; relative-phase error and opposite X predictions remain
```

### 44.6.6 Compute diagnostics without manufacturing zeros

Naively squaring very small nonzero components can underflow. For a finite nonzero vector choose $s$ as the maximum absolute real or imaginary component. Algebraically,

$$
\|w\|_2=s\left(\sum_i |w_i/s|^2\right)^{1/2}.
$$

Scaling before squaring avoids the particular underflow in this example. The helper first promotes representable input components to complex128, computes this scale, and explicitly rejects zero normalization. Promotion cannot recover components already lost in an earlier computation. A true norm outside the floating range cannot be returned as an ordinary finite scalar; the normalization helper explicitly reports that range failure. This is not a universal subnormal-arithmetic guarantee. Normalization must be an explicit, recorded transformation, with the original vector and raw norm preserved.

Here `tiny` is an unnormalized mathematical vector used to test a norm kernel; it is not submitted as a quantum state to FlagQuantum. No square-underflow value is interpreted as a physically impossible event.

**Formula → code → result: a scaled norm and the zero-vector boundary.**

```python
tiny = torch.tensor([1e-200,1e-200j],dtype=torch.complex128)
naive_square_sum = float(tiny.abs().square().sum())
scaled_length = n.norm(tiny)
assert naive_square_sum == 0 and scaled_length > 0
assert abs(n.norm(n.normalize(tiny))-1) < 1e-14
try: n.normalize(tiny*0)
except ValueError: print("scaled norm retains nonzero direction; zero normalization rejected")
else: raise AssertionError("zero vector accepted")
```

```text
scaled norm retains nonzero direction; zero normalization rejected
```

### 44.6.7 Propagate error to observables and rare conditional branches

For a Hermitian operator $H$, adding and subtracting $v^\dagger Hw$ gives

$$
w^\dagger Hw-v^\dagger Hv=d^\dagger Hw+v^\dagger Hd,
\qquad |w^\dagger Hw-v^\dagger Hv|\le\|H\|E(r+1)\le\|H\|E(2+E).
$$

The same proof for an event projector $P$, whose operator norm is at most one, bounds the difference of **raw quadratic weights** by $E(2+E)$. If $w$ is not normalized these weights need not sum to one and must not be called a normalized probability distribution. After explicit normalization, write $E'=\|\widetilde w-v\|_2$; since both norms are one, the bound is $2\|H\|E'$ or $2E'$ for an event, with $E'\le2E$ as above. Relative error in a tiny probability can be large even when the absolute bound is small. Shot fluctuation is a separate statistical error from Chapters 6 and 14.

For a rare event with $b=Pv$, $a=Pw$ and $p=\|b\|_2^2>0$, a conditional comparison requires $a\ne0$. Adding and subtracting $a/\|b\|_2$ yields

$$
\left\|\frac{a}{\|a\|_2}-\frac{b}{\|b\|_2}\right\|_2
 \le\frac{|\|b\|_2-\|a\|_2|+\|a-b\|_2}{\|b\|_2}
 \le\frac{2\|a-b\|_2}{\sqrt p}\le\frac{2E}{\sqrt p}.
$$

There is no uniform small conditional error as $p$ tends to zero. If the computed projection vanishes, the normalized computed branch is undefined; inventing a branch or clipping it is not validation. The following two normalized vectors differ only by moving a rare amplitude between two selected coordinates. Their global difference is small but their conditional vectors are orthogonal.

**Formula → code → result: absolute output control without a false conditional guarantee.**

```python
p = 1e-12
before = torch.tensor([math.sqrt(1-p),math.sqrt(p),0,0],dtype=torch.complex128)
after = torch.tensor([math.sqrt(1-p),0,math.sqrt(p),0],dtype=torch.complex128)
mask = torch.tensor([0,1,1,0],dtype=torch.complex128)
E = n.norm(after-before)
conditional_error = n.norm(n.normalize(after*mask)-n.normalize(before*mask))
assert E < 2e-6 and conditional_error > 1.4
assert conditional_error <= 2*E/math.sqrt(p)
report = n.metrics(after,before)
assert report['event_error'] <= report['bound']+1e-15
print("small global error, large conditional error; absolute event bound passed")
```

```text
small global error, large conditional error; absolute event bound passed
```

### 44.6.8 Keep implementation support and verification separate

The actual APIs exercised here are `Circuit(...,dtype=...)`, named RY/P/CX gate calls, `ExecutionOptions(precision=...)`, `fq.run`, `result.statevector()`, `result.measurement(name).value` and `result.expectation(name)`. `probabilities` is a tensor-valued result property in this release, not a callable named-result accessor; the initial prototype incorrectly called it and failed after one native run. That source and failure log are retained. The corrected named measurement accessor is used throughout the final snippets. This was a book-side API misuse, not a reported native numerical defect.

The complete program uses a CPU statevector profile and checks the returned dtype, raw vector, norm drift, full probabilities and XX expectation in both precisions. It does not claim to validate GPU arithmetic, density-matrix drift, gradients, every precision/backend combination, automatic error estimation, native per-gate residual tracing or an interval certificate. The optional `normalize` routine and residual trace belong to this book; their existence is not a native normalization-policy API. No post-hoc correction is used to make a failed raw comparison pass.

**Formula → code → result: independently chosen parameters and explicit correction checks.**

```python
for dtype in (torch.complex64,torch.complex128):
    raw, target, report = n.native(91,-.047,.031,dtype)
    corrected = n.normalize(raw)
    assert n.norm(corrected.to(torch.complex128)-target) <= 2*report['error']+1e-12
assert n.errors() == 14
n.examples()
print("2 fresh native checks and 14 rejected contracts; raw reports kept before optional correction")
```

```text
2 fresh native checks and 14 rejected contracts; raw reports kept before optional correction
```

In the initial author execution of the printed $L=91$ check, complex64 gave vector error approximately $1.19\times10^{-7}$ and squared-norm drift $2.52\times10^{-8}$; complex128 gave vector error $2.20\times10^{-15}$ and reported drift zero. These are archived observations on this CPU, not portable exact outputs or proof of exact normalization.

The complete program performs 24 native runs: four depths $L\in\{1,7,64,257\}$, three signed angle pairs, and both precisions. It also checks eight classical residual traces, exact radial fixtures, relative phase, rare conditioning, scaled norms and 14 invalid contracts. The final checker executes four additional native runs in the eight printed units. Fresh transfer evidence changes depths and signed angles in both precisions; it is recorded separately from these calls. Tests support the implementation translation; the algebra above supplies the declared bounds under its assumptions.

Expected output of the complete program:

```text
24 native CPU statevector runs: two precisions, four depths, three signed angle pairs passed.
Decimal 60/80-digit references agree after binary64 export; raw state, norm, probabilities and XX checked.
8 local residual traces; cancellation, radial drift, phase loss, rare conditioning and scaled-norm checks passed.
14 malformed contracts rejected; no native output renormalization or phase alignment applied.
```

**Check your understanding and transfer.**

- **44.6-A — error budget.** With exact $v_0$, $L=100$, and justified residual bounds $\eta_j\le10^{-8}$, find a state-error and squared-norm-drift bound. Does measured zero drift prove zero state error?
- **44.6-B — lost phase.** Replace $|+\rangle$ by $(|0\rangle+i|1\rangle)/\sqrt2$. Compare norm, computational probabilities, X and Y expectations. Can normalization identify which state was intended?
- **44.6-C — fresh execution.** Use $L\in\{19,113,311\}$ and $(\theta,\phi)=(-.029,.017)$ in both precisions, compare raw native outputs with the Decimal reference, and retain all errors before trying explicit normalization. Do not require drift to be monotone or observed errors to attain the theoretical bound.
- **44.6-D — conditioning and failure.** Repeat the rare-amplitude construction with $p=10^{-16}$. Explain why a tolerance justified for an unconditional probability cannot automatically certify the conditional state. Diagnose a report that casts an already rounded result, normalizes it, then declares accuracy from its norm alone.

<details markdown="1">
<summary>Answers and verification guidance for 44.6-A–D</summary>

**A.** $B_L=10^{-6}$ and $|r^2-1|\le2\times10^{-6}+10^{-12}$. Zero drift is consistent with a wrong unitary or a relative-phase error. It cannot invert the implication from state error to drift.

**B.** Both norms are one and both computational laws are $(1/2,1/2)$. The original state has $(\langle X\rangle,\langle Y\rangle)=(1,0)$; the changed state has $(0,1)$, using the Y sign convention of 6.3. Radius and computational probabilities do not determine the phase. Compare a phase-sensitive observable against a declared target.

**C.** The transfer program records six native calls with new depths, signed angles and both precisions. It checks raw vector/probability/XX errors against their declared thresholds and the scalar reference before any correction. Different depths can have cancelling errors; lower drift alone does not select the more accurate vector. Decimal agreement is diagnostic, not a certified error enclosure.

**D.** The global distance is $\sqrt{2p}$ while the two selected, normalized branches remain distance $\sqrt2$ apart. The bound $2E/\sqrt p$ is then larger than one, as it should be. An already lost component is not recreated by casting. Normalization discards a radial diagnostic and leaves wrong direction or phase untouched. Retain raw errors, identify the source and recompute at suitable precision if needed; do not relabel a repaired norm as recovered information.

</details>

**Sources and review status.** The norm conventions and induced-operator inequalities were checked against [Watrous §1.1.3, printed pp. 32–33](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf#page=40). The [QuEST v1 representation passage, PDF p. 2](https://arxiv.org/pdf/1802.08032v1#page=2) supplies context for finite floating complex state storage and declared precision, not a FlagQuantum rounding guarantee. The local residual, normalization and conditioning derivations above are supplied here; third-party source text is not redistributed. The section record separates author execution from pending independent mathematical/implementation review and reader trial. This is a draft, not accepted. The next scheduled B03 target is 44.8, not the deferred 44.4–44.5 or 44.7.

<!-- end-section-44.6 -->
