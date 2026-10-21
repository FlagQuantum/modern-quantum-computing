# 5. Gates, Reversible Computation, and Circuit Synthesis

**Working drafts: sections 5.1–5.2 · Writing Baseline 1.0 · October 21, 2026.** Author execution is separate from independent mathematical, implementation and reader review, which remain pending. Examples use installed released FlagQuantum 0.3.1 and PyTorch 2.13.0 on CPU with complex128 statevectors.

<span id="sec-gates-reversible-computation-and-circuit-synthesis-1"></span>

## 5.1 Circuit composition, inversion, and call order

A circuit is constructed in the order its gates are to act. Its matrix is written in the opposite visual order, because the rightmost matrix acts first on a column vector. To undo the circuit, we must reverse its chronological gate list and replace every gate by its inverse. Confusing any two of these orders can produce a different state even when computational-basis probabilities happen to agree.

The prerequisites are [3.4](ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-4), for unitary dynamics, and [4.3](ch-composite-systems-tensor-products-and-qubit-ordering.md#sec-composite-systems-tensor-products-and-qubit-ordering-3), for local operators embedded in a register. Here every mathematical gate is a fixed unitary on one finite register space; local gates are understood as their full-register embeddings. Test-state preparation is outside the block being inverted. Measurements, channels and conditional programs are not covered by this unitary inverse-product theorem.

The eight formula–derivation–code–result units below are cumulative. Run from the repository root in the pinned example environment. The companion [circuit_composition.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/circuit_composition.py) checks full complex vectors at absolute tolerance $10^{-12}$ and relative tolerance zero, with no normalization repair or phase alignment. A verified release boundary and an explicitly labeled book-side guard appear in unit 8.

<span id="formula-code-5-1-two-orders"></span>

### 1. Read chronological calls from left to right

**Formula.** Define two one-qubit unitaries

$$
H=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix},\qquad
S=\begin{pmatrix}1&0\\0&i\end{pmatrix}.
$$

Calling H, then S gives $SH|\psi\rangle$. Calling S, then H gives $HS|\psi\rangle$. On the zero state,

$$
SH|0\rangle=\frac{|0\rangle+i|1\rangle}{\sqrt2},\qquad
HS|0\rangle=\frac{|0\rangle+|1\rangle}{\sqrt2}.
$$

**Derivation.** H maps zero to the equal real superposition, and the following S multiplies its one-coordinate by i. In the reversed circuit, S first leaves zero unchanged and H then makes the real superposition. Both gates are unitary: H is real symmetric with $H^2=I$, while S has unit-modulus diagonal entries. Their products differ. Both resulting computational probabilities are `(1/2,1/2)`, so probability equality alone would miss this order error.

```python
import torch
import flagquantum as fq
from math import pi
from flagquantum.errors import CapabilityError, ValidationError
from examples.foundations.tensor_spaces import OPTIONS
from examples.foundations.circuit_composition import (
    DTYPE, ATOL, H, S, rx, rz, matrix_product, scalar_steps,
    product_input, execute, checked_adjoint, embedding)
forward = fq.Circuit(1,dtype=DTYPE).h(0).s(0)
reversed_calls = fq.Circuit(1,dtype=DTYPE).s(0).h(0)
a = fq.run(forward,outputs=[fq.probabilities()],options=OPTIONS)
b = fq.run(reversed_calls,outputs=[fq.probabilities()],options=OPTIONS)
assert a.statevector().shape == b.statevector().shape == (1,2)
zero = torch.tensor([1,0],dtype=DTYPE)
assert torch.allclose(a.statevector()[0],S @ H @ zero,rtol=0,atol=ATOL)
assert torch.allclose(b.statevector()[0],H @ S @ zero,rtol=0,atol=ATOL)
assert not torch.allclose(a.statevector(),b.statevector(),rtol=0,atol=ATOL)
assert torch.allclose(a.probabilities,b.probabilities,rtol=0,atol=ATOL)
print('H then S != S then H: complex amplitudes differ')
print('computational probabilities agree:', [round(v,6) for v in a.probabilities[0].tolist()])
```

```text
H then S != S then H: complex amplitudes differ
computational probabilities agree: [0.5, 0.5]
```

<span id="formula-code-5-1-product"></span>

### 2. Prove the product corresponding to a gate list

**Formula.** Let $G_1,\ldots,G_m$ be the chronological full-register gate matrices and set $x^{(0)}=x$. Successive states satisfy

$$
x^{(t)}=G_tx^{(t-1)},\qquad
x^{(m)}=G_mG_{m-1}\cdots G_1x.
$$

**Derivation.** For t=1 the statement is the definition of the first gate action. Suppose the state after t−1 gates is $G_{t-1}\cdots G_1x$. The next gate acts on that state, giving $G_t(G_{t-1}\cdots G_1x)$. Associativity removes the brackets without changing order. Induction proves the formula for every finite m. For m=0 define the empty circuit matrix as I, which leaves x unchanged.

In coordinates, one step is $x_j^{(t)}=\sum_k(G_t)_{jk}x_k^{(t-1)}$. Substituting the previous step recursively produces the same product entries. This shows why matrix multiplication expresses chronological gate action; it does not authorize interchanging noncommuting gates. An implementation accumulating a matrix in call order must update `total = gate @ total`.

```python
U = matrix_product([H,S],1)
assert torch.allclose(U,S @ H,rtol=0,atol=ATOL)
v = torch.tensor([.6,.8j],dtype=DTYPE)
scalar = scalar_steps([H,S],v.tolist())
assert torch.allclose(scalar,U @ v,rtol=0,atol=ATOL)
assert torch.equal(matrix_product([],1),torch.eye(2,dtype=DTYPE))
print('chronological[H,S] -> matrix S@H; independent scalar steps agree')
print('empty chronological list -> identity')
```

```text
chronological[H,S] -> matrix S@H; independent scalar steps agree
empty chronological list -> identity
```

<span id="formula-code-5-1-compose"></span>

### 3. Compose reusable blocks without changing their meaning

**Formula.** If block A acts before block B, the composed map is

$$
x\longmapsto U_Ax\longmapsto U_BU_Ax.
$$

**Derivation.** Treat each block as one linear map and apply unit 2. The second block is on the left in the product regardless of how many gates either block contains. In FlagQuantum 0.3.1, `destination.compose(source)` appends the source's instructions to the destination, mutates that destination and returns it. It does not create a separate destination automatically. We therefore start a fresh circuit when we need to preserve reusable blocks.

The actual installed source was inspected, and the behavior below is executed. Here A contains H and B contains S. The returned object is the destination; the original source instruction lists remain one gate each. This does not promise deep-copy isolation of tensors that an application later mutates.

```python
A = fq.Circuit(1,dtype=DTYPE).h(0)
B = fq.Circuit(1,dtype=DTYPE).s(0)
program = fq.Circuit(1,dtype=DTYPE)
assert program.compose(A) is program
assert program.compose(B) is program
composed_state, _ = execute(program,[(1,0)])
assert torch.allclose(composed_state,S @ H @ zero,rtol=0,atol=ATOL)
assert len(A.to_ir().instructions) == len(B.to_ir().instructions) == 1
print('compose(A),compose(B): U_B@U_A; destination returned, source lists unchanged')
```

```text
compose(A),compose(B): U_B@U_A; destination returned, source lists unchanged
```

<span id="formula-code-5-1-inverse-proof"></span>

### 4. Prove why the inverse reverses chronological order

**Formula.** For $U=G_m\cdots G_1$, define

$$
V=G_1^\dagger G_2^\dagger\cdots G_m^\dagger.
$$

Then $VU=UV=I$, so $V=U^{-1}=U^\dagger$. The corresponding chronological inverse calls are

$$
G_m^\dagger,\ G_{m-1}^\dagger,\ldots,\ G_1^\dagger.
$$

**Proof.** Because every gate is unitary, $G_t^\dagger G_t=G_tG_t^\dagger=I$. For m=1 the two identities are exactly those single-gate unitary conditions. For m≥2, multiply VU and cancel the innermost pair first:

$$
VU=G_1^\dagger\cdots G_{m-1}^\dagger
(G_m^\dagger G_m)G_{m-1}\cdots G_1
=\cdots=G_1^\dagger G_1=I.
$$

For UV the innermost pair is instead $G_1G_1^\dagger$; canceling outward similarly gives I. Thus V is a two-sided inverse. Taking the adjoint of a matrix product reverses its factors, so V is also $U^\dagger$; alternatively that identity follows by taking inner products and moving each gate across them one at a time. The empty product gives V=I as well. Crucially, the **rightmost matrix of V acts first**, which yields the chronological list displayed above.

For calls H then S, the matrix is SH. Its inverse matrix is $H^\dagger S^\dagger=HS^\dagger$, so inverse calls are S-dagger then H. In the native API these are `sdg(0)` then `h(0)`. The native `program.adjoint()` returns a new block with those instructions in that order. Only taking adjoints while retaining the original chronological order would give H then S-dagger, which is wrong here.

```python
inverse = program.adjoint()
assert inverse is not program
assert [i.name for i in inverse.to_ir().instructions] == ['sdg','h']
assert [i.name for i in program.to_ir().instructions] == ['h','s']
manual = fq.Circuit(1,dtype=DTYPE).compose(program).sdg(0).h(0)
native = fq.Circuit(1,dtype=DTYPE).compose(program).compose(inverse)
wrong = fq.Circuit(1,dtype=DTYPE).compose(program).h(0).sdg(0)
for correct in (manual,native):
    restored, _ = execute(correct,[(1,0)])
    assert torch.allclose(restored,zero,rtol=0,atol=ATOL)
wrong_state, _ = execute(wrong,[(1,0)])
assert not torch.allclose(wrong_state,zero,rtol=0,atol=ATOL)
print('manual/native inverse calls: S-dagger then H; both restore|0>')
print('H then S-dagger after the forward block: wrong inverse detected')
```

```text
manual/native inverse calls: S-dagger then H; both restore|0>
H then S-dagger after the forward block: wrong inverse detected
```

<span id="formula-code-5-1-two-sided"></span>

### 5. Verify both cancellation directions and a complex input

The two-sided proof guarantees recovery on every state, not only zero. For the complex input v=(0.6,0.8i), check both chronological sequences: forward then inverse, and inverse then forward. The initial preparation is external to `program`; it is not included in the block's adjoint. This distinction matters when a larger experiment contains preparation, a reversible processing block and later measurement.

The same identity holds for a multi-qubit register after every local gate has been embedded in that register space, as in 4.3. It does not assume product input states: the proof acts on an arbitrary vector. The complete program checks every computational basis column of its one-, two- and three-qubit programs as well as complex product preparations. The basis argument proves a matrix identity; numerical fixtures test its implementation at the stated tolerance.

```python
left = fq.Circuit(1,dtype=DTYPE).compose(program).compose(inverse)
right = fq.Circuit(1,dtype=DTYPE).compose(inverse).compose(program)
for circuit in (left,right):
    recovered, _ = execute(circuit,[(.6,.8j)])
    assert torch.allclose(recovered,v,rtol=0,atol=ATOL)
assert torch.allclose(U.mH @ U,torch.eye(2,dtype=DTYPE),rtol=0,atol=ATOL)
assert torch.allclose(U @ U.mH,torch.eye(2,dtype=DTYPE),rtol=0,atol=ATOL)
print('both chronological roundtrips restore the full complex input')
```

```text
both chronological roundtrips restore the full complex input
```

<span id="formula-code-5-1-placement"></span>

### 6. Preserve qubit placement when composing and inverting

**Formula.** Let $E_q$ embed a one-qubit block on qubit q of an n-qubit register, as in 4.3. Its adjoint obeys

$$
E_q(U)^\dagger=E_q(U^\dagger).
$$

**Derivation.** The product-basis matrix of the embedding has U on the selected factor and identities elsewhere. Taking its adjoint replaces U by $U^\dagger$ and leaves the identity factors unchanged. Thus inversion changes gate order and each gate's matrix, while keeping its physical qubit address. Moving the inverse to another qubit would undo a different operation.

Map local q0 of the reusable H-then-S block to register q2 using `qubit_map={0:2}`. `qubits=(2,)` is the tested positional alternative used in the full companion. The block acts on q2 without sorting, swapping or relabeling the prepared register.

```python
mapped = fq.Circuit(3,dtype=DTYPE).compose(program,qubit_map={0:2})
factors = [(.6,.8j),(1,0),(.6,.8j)]
initial = product_input(factors)
mapped_state, _ = execute(mapped,factors)
expected = embedding(S @ H,3,2) @ initial
assert torch.allclose(mapped_state,expected,rtol=0,atol=ATOL)
assert all(tuple(i.wires)==(2,) for i in mapped.adjoint().to_ir().instructions)
print('mapped localq0 -> registerq2: full8coordinates checked; inverse keepsq2')
```

```text
mapped localq0 -> registerq2: full8coordinates checked; inverse keepsq2
```

<span id="formula-code-5-1-phase"></span>

### 7. Negate rotation angles in reverse order and retain phase

For the named rotations tested in the companion, angles are radians. Their matrices are

$$
R_x(\theta)=\begin{pmatrix}
\cos(\theta/2)&-i\sin(\theta/2)\\
-i\sin(\theta/2)&\cos(\theta/2)
\end{pmatrix},\qquad
R_z(\phi)=\begin{pmatrix}e^{-i\phi/2}&0\\0&e^{i\phi/2}\end{pmatrix}.
$$

Conjugate-transposing these entries gives $R_x(\theta)^\dagger=R_x(-\theta)$ and $R_z(\phi)^\dagger=R_z(-\phi)$. Thus calls Rx(theta), Rz(phi) are undone by Rz(-phi), Rx(-theta). Negating both angles without reversing their calls generally fails because the two axes' matrices do not commute. The complete program tests the native adjoint against these full matrices on both basis columns and a complex input.

A useful phase boundary is $R_x(2\pi)=-I$, not I as a coordinate matrix. Its computational probabilities are unchanged, but its exact output vector has a minus sign. Appending its true inverse restores the original vector, including that sign. The two runs below do not silently equate matrices up to phase.

```python
full_turn = fq.Circuit(1,dtype=DTYPE).rx(0,2*pi)
turned, _ = execute(full_turn,[(1,0)])
roundtrip = fq.Circuit(1,dtype=DTYPE).compose(full_turn).compose(full_turn.adjoint())
recovered, _ = execute(roundtrip,[(1,0)])
assert torch.allclose(turned,-zero,rtol=0,atol=ATOL)
assert torch.allclose(recovered,zero,rtol=0,atol=ATOL)
assert torch.allclose(rx(.7).mH,rx(-.7),rtol=0,atol=ATOL)
assert torch.allclose(rz(-.4).mH,rz(.4),rtol=0,atol=ATOL)
print('Rx(2pi)|0> = -|0>; forward plus native adjoint = |0>')
```

```text
Rx(2pi)|0> = -|0>; forward plus native adjoint = |0>
```

<span id="formula-code-5-1-boundaries"></span>

### 8. Check the unitary precondition instead of assuming every adjoint is an inverse

For a general matrix M, the adjoint $M^\dagger$ exists even if M has no inverse. For example, the projector $P=\operatorname{diag}(1,0)$ satisfies $P^\dagger P=P\ne I$. The invertible but nonunitary matrix 2H has adjoint 2H and inverse H/2; those are different. The theorem requires unitarity, not merely that a numerical adjoint can be formed.

**Verified FlagQuantum 0.3.1 boundary.** The installed `Circuit.adjoint` docstring states that a custom nonunitary matrix is rejected, but the actual release accepts both P and 2H and returns their matrix adjoints. Neither returned block undoes its input block. The initial author check caught this discrepancy after its 98 simulator runs; its raw failure and a construction-only reproduction are retained. It is reported as [FlagQuantum #685](https://github.com/flagos-ai/FlagQuantum/issues/685). This does not invalidate the preceding tests on genuinely unitary gates.

The companion therefore defines `checked_adjoint`, an explicitly **book-side precondition guard**, not a new FlagQuantum method. It checks the finite custom matrices' Gram matrices against I before delegating to the real `block.adjoint()`. Native named-gate handling still belongs to FlagQuantum; our fixed test programs contain only the declared unitary gates. This is not an inverse for measurements, noise, resets or arbitrary conditional programs.

```python
projector = torch.diag(torch.tensor([1,0],dtype=DTYPE))
invalid = [
    (CapabilityError,lambda: checked_adjoint(fq.Circuit(1,dtype=DTYPE).unitary(0,unitary=projector))),
    (CapabilityError,lambda: checked_adjoint(fq.Circuit(1,dtype=DTYPE).unitary(0,unitary=2*H))),
    (ValidationError,lambda: fq.Circuit(2).compose(program,qubits=(2,))),
    (TypeError,lambda: fq.Circuit(2).compose(program,qubits=(0,),qubit_map={0:1}))]
rejected = 0
for error,action in invalid:
    try:
        action()
    except error:
        rejected += 1
assert rejected == 4
print('book guard rejects2nonunitaries; native compose rejects2invalid placement contracts')
```

```text
book guard rejects2nonunitaries; native compose rejects2invalid placement contracts
```

Run the complete example and actual-body checker:

```bash
python examples/foundations/circuit_composition.py
python scripts/check_circuit_composition_prose.py
```

The complete program executes **98 circuits**. Five programs cover named H/S gates, two noncommuting rotations, a custom complex unitary with an overall phase, a two-qubit full-space permutation sequence, and a single-qubit block mapped into three qubits. For every program it tests all basis columns and one complex product with the forward block, native adjoint and both cancellation directions: 92 runs. Six more runs cover the empty circuit, the full-turn phase and recovery, native mutating composition, and two deliberately incorrect inverses. The two-qubit permutation swaps basis labels `10` and `11`; its controlled-operation interpretation is developed in 5.2, not assumed by the inverse-product proof.

Independent scalar chronological sums check the dense product and every forward output. Matrix adjoints check native inverse outputs, and full complex coordinates check both recovery directions. Seven invalid contracts include the two book-guard rejections and native composition errors. The eight body fragments execute eleven circuits in a separate invocation. A new complex rotation transfer is recorded below. Finite examples test the implementation; the two-sided proof establishes the general finite unitary statement.

Expected output of the complete program:

```text
Chronological G1,...,Gm gives matrix Gm...G1; inverse calls Gm^dagger,...,G1^dagger.
HS: all2basis columns and1complex product,forward/adjoint/both roundtrips passed.
rotations: all2basis columns and1complex product,forward/adjoint/both roundtrips passed.
custom-phase: all2basis columns and1complex product,forward/adjoint/both roundtrips passed.
two-qubit: all4basis columns and1complex product,forward/adjoint/both roundtrips passed.
mapped: all8basis columns and1complex product,forward/adjoint/both roundtrips passed.
Empty circuit,2pi phase,mutating compose,source order,two wrong inverses and7invalid contracts checked.
98 actual CPU complex128 circuits; atol=1e-12,rtol=0; no phase alignment,measurement inversion or hardware.
```

These checks do not certify arbitrary backend versions, differentiable inverse programs, noisy execution or hardware reversal. Construction of an adjoint block does not reverse a previous measurement record or undo an unknown environment.

### Understanding checks and transfer exercises

**5.1-A — New rotation order.** A one-qubit program calls Rz(0.23), Rx(−0.61), then S. Give its total matrix, its inverse matrix and the chronological inverse calls. Check a complex input rather than only a computational probability vector.

**5.1-B — Placement.** A block acts on register q2 but its proposed inverse is applied to q0. Why does the product-inverse theorem not justify recovery? Which placement information must be preserved?

**5.1-C — Interpret mutation.** Given `C = A.compose(B)`, which object changes in the tested API? If A is to remain a reusable source, how should the destination be built instead?

**5.1-D — Phase and nonunitarity.** Why can identical output probabilities conceal an order error? Why is an adjoint not generally an inverse even when the matrix is invertible? Use the examples from this section.

<details markdown="1">
<summary>Answers and reasoning</summary>

**A.** The matrix is $S R_x(-0.61)R_z(0.23)$. Its inverse is $R_z(-0.23)R_x(0.61)S^\dagger$. Chronological inverse calls are S-dagger, Rx(0.61), Rz(−0.23). The separate author transfer actually executes the native forward-plus-adjoint program on v=(0.6,0.8i), checks every complex coordinate, and independently verifies the manually ordered inverse matrix.

**B.** The full-register matrices are different embeddings. The inverse of $E_2(U)$ is $E_2(U^\dagger)$, not $E_0(U^\dagger)$ in general. Preserve the physical target positions and, for any multi-qubit operation, their declared local order as well; this section's mapped one-qubit example has no local-order ambiguity.

**C.** A is the destination and is mutated to contain A followed by B; C is that same object. Use `C = fq.Circuit(n,dtype=DTYPE).compose(A).compose(B)` when both source blocks should remain separately reusable. This preserves the tested source instruction lists; tensor aliasing after application-side mutation is a different contract.

**D.** H-then-S and S-then-H on zero have equal computational probabilities but different relative phase. A full-turn Rx also changes the exact statevector sign without changing those probabilities. Conversely, invertibility alone does not make the adjoint equal the inverse: for 2H the adjoint is 2H but the inverse is H/2. Unit-modulus phase freedom, numerical equality and the mathematical inverse condition must be tracked separately.

</details>

### Sources, depth and next step

Depth **F**: chronological product induction, finite two-sided inverse-product proof, empty-circuit boundary, source/destination block semantics and preserved local embeddings are explicit. The assigned background locator is Nielsen and Chuang, 10th Anniversary Edition, §4.1. No fresh inspection of the user-local PDF is claimed. The installed released FlagQuantum methods were inspected and actually exercised; the native nonunitary admission discrepancy and workaround are documented without inventing an API or weakening the unitary theorem.

The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/5.1.json) separates author execution, the preserved failure and subsequent passing checks from pending independent mathematical, implementation and reader reviews. This remains a working draft. Continue with [5.2 Controlled operations and ancillas](#sec-gates-reversible-computation-and-circuit-synthesis-2).


<span id="sec-gates-reversible-computation-and-circuit-synthesis-2"></span>

## 5.2 Controlled operations and ancillas

A control qubit selects a unitary coherently: both branches survive when the control is in superposition. An auxiliary qubit is a register with an explicitly assigned role and input state. Allocating it is only the beginning; if it is temporary workspace, its final state and correlations must be checked before reuse.

Prerequisites are [4.1](ch-composite-systems-tensor-products-and-qubit-ordering.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), [4.4](ch-composite-systems-tensor-products-and-qubit-ordering.md#sec-composite-systems-tensor-products-and-qubit-ordering-4) and [5.1](#sec-gates-reversible-computation-and-circuit-synthesis-1). We retain q0 as the most significant statevector bit, column-vector left action, declared ordered supports and fixed ideal unitary circuits. All examples use the released CPU complex128 environment stated above. The book runner explicitly prepares the supplied normalized input factors outside the tested block, calls `fq.run` with statevector/PyTorch/CPU/complex128 options and `fq.probabilities()`, and checks the batch-one statevector and probabilities before returning their unbatched vectors. Backend fallback and approximation are disabled; source code is linked below. The eight cumulative units pair each mathematical claim with a concrete check. Run from the repository root; [controlled_ancillas.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/controlled_ancillas.py) contains the helpers and exhaustive small-register checks.

<span id="formula-code-5-2-blocks"></span>

### 1. Orthogonal controls give unitary blocks

**Formula.** Let the control be the first qubit of an ordered support and let $U$ be a unitary on its target register. With $P_b=|b\rangle\langle b|$,

$$
C(U)=P_0\otimes I+P_1\otimes U
=\begin{pmatrix}I&0\\0&U\end{pmatrix}.
$$

**Derivation.** $P_b^\dagger=P_b$, $P_b^2=P_b$, $P_0P_1=P_1P_0=0$ and $P_0+P_1=I$. Expanding the product therefore gives

$$
C(U)^\dagger C(U)=P_0\otimes I+P_1\otimes U^\dagger U=I.
$$

The reverse product is also identity. Conversely, restricting this equality to $|1\rangle\otimes|\psi\rangle$ forces $U^\dagger U=I$. This is a unitary-controlled operation, not a way to make an arbitrary nonunitary map into a gate. For two controls, replace $P_1$ by $Q=|11\rangle\langle11|$ and $P_0$ by $I-Q$; the same orthogonal-projector proof applies. The companion program checks named CCX on all eight basis states and a complex superposition.

**Code.** Imports below are cumulative. `controlled_matrix` is an explicitly named book helper, not a native constructor. It checks finite CPU complex128 qubit matrices and numerical unitarity, then forms the displayed blocks. All angles below are dimensionless radians. No phase alignment or normalization repair is used.

```python
import sys
sys.path.insert(0, '.')
import torch
import flagquantum as fq
from math import sqrt
from flagquantum.errors import CapabilityError, ValidationError
from examples.foundations import controlled_ancillas as ca
from examples.foundations.circuit_composition import product_input, rx, rz
D=ca.DTYPE
I=torch.eye(2,dtype=D)
C=ca.controlled_matrix(ca.X)
assert torch.equal(C[:2,:2],I) and torch.equal(C[2:,2:],ca.X)
torch.testing.assert_close(C.mH@C,torch.eye(4,dtype=D),rtol=0,atol=ca.ATOL)
print('C(X): identity/target blocks and unitary product verified')
```

```text
C(X): identity/target blocks and unitary product verified
```

<span id="formula-code-5-2-superposition"></span>

### 2. A superposed control evolves coherently

**Formula.** For normalized target $|\psi\rangle$ and $|\alpha|^2+|\beta|^2=1$,

$$
C(U)(\alpha|0\rangle+\beta|1\rangle)|\psi\rangle
=\alpha|0\rangle|\psi\rangle+\beta|1\rangle U|\psi\rangle.
$$

**Derivation.** Apply $P_0$ and $P_1$ to each control component; each projector keeps one component and kills the other. There is no intermediate control measurement. More generally an already correlated input $|0\rangle|\psi_0\rangle+|1\rangle|\psi_1\rangle$ becomes $|0\rangle|\psi_0\rangle+|1\rangle U|\psi_1\rangle$, where the branch vectors need not be normalized. If both control coefficients are nonzero, the product input's output is a product state exactly when $U|\psi\rangle$ is proportional to $|\psi\rangle$: comparing the two control components of a proposed product forces both target vectors to be proportional; the converse follows by factoring the target vector out.

For $U=X$ and target zero, the two target vectors are orthogonal. The example is therefore correlated, with complex coordinates in order 00,01,10,11:

$$
0.6|00\rangle+0.8i|11\rangle.
$$

**Code and verification.** The actual named gate is `cx(control,target)`. A separate reference places the two nonzero amplitudes explicitly.

```python
v,p=ca.run(fq.Circuit(2,dtype=D).cx(0,1),[(.6,.8j),(1,0)])
expected=torch.tensor([.6,0,0,.8j],dtype=D)
torch.testing.assert_close(v,expected,rtol=0,atol=ca.ATOL)
print('CX: amplitudes [0.6,0,0,0.8i]; probabilities [0.36,0,0,0.64]')
```

```text
CX: amplitudes [0.6,0,0,0.8i]; probabilities [0.36,0,0,0.64]
```

<span id="formula-code-5-2-phase"></span>

### 3. A target phase becomes a relative control phase

**Formula.** If $U|\psi\rangle=e^{i\phi}|\psi\rangle$, the previous output factors as

$$
(\alpha|0\rangle+\beta e^{i\phi}|1\rangle)|\psi\rangle.
$$

**Derivation.** The phase multiplies only the control-one branch. In particular $C(e^{i\chi}U)$ is generally different from $e^{i\chi}C(U)$: the latter multiplies the zero branch too. With a plus control, $C(I)$ preserves plus whereas $C(-I)$ produces minus. Applying H to the control then gives zero versus one. An overall phase that is dispensable for an isolated target gate cannot be silently discarded before controlling that gate.

**Code and verification.** The target remains zero in both experiments; every complex output coordinate, not just the control probability, is checked.

```python
for sign,index in ((1,0),(-1,2)):
    block=fq.Circuit(2,dtype=D).unitary(0,1,unitary=ca.controlled_matrix(sign*I)).h(0)
    v,p=ca.run(block,[(1/sqrt(2),1/sqrt(2)),(1,0)])
    expected=torch.zeros(4,dtype=D);expected[index]=1
    torch.testing.assert_close(v,expected,rtol=0,atol=ca.ATOL)
print('C(I) then H(control): 00; C(-I) then H(control): 10')
```

```text
C(I) then H(control): 00; C(-I) then H(control): 10
```

<span id="formula-code-5-2-native"></span>

### 4. Control a whole block with explicit placement

**Formula.** Orthogonality of the projectors also yields

$$
C(V)C(U)=P_0\otimes I+P_1\otimes VU=C(VU).
$$

**Derivation.** Expand the four terms; the two mixed-projector terms vanish. Thus controlling chronological U-then-V preserves that call order and yields the controlled total matrix VU.

**Code.** In the tested released API, `source.control(1,ctrl_qubits=(1,))` returns a new circuit. The original source uses q0 as target and the added control is q1, outside the source register. This native placement differs from the conventional control-first support used above. `compose(native,qubits=(1,0))` explicitly maps old target q0 to new q1 and old control q1 to new q0. A generic controlled matrix on ordered support `(0,1)` provides a separate implementation for comparison. The reference below is a direct branch calculation with $U=R_z(-0.4)R_x(0.7)$, not another controlled simulator call.

```python
source=fq.Circuit(1,dtype=D).rx(0,.7).rz(0,-.4)
native=source.control(1,ctrl_qubits=(1,))
assert native is not source and native.n_qubits==2
assert len(source.to_ir().instructions)==2
mapped=fq.Circuit(2,dtype=D).compose(native,qubits=(1,0))
factors=[(.6,.8j),(1,0)]
U=rz(-.4)@rx(.7)
expected=torch.cat((torch.tensor([.6,0],dtype=D),.8j*U[:,0]))
for block in (mapped,fq.Circuit(2,dtype=D).unitary(0,1,unitary=ca.controlled_matrix(U))):
    v,p=ca.run(block,factors)
    torch.testing.assert_close(v,expected,rtol=0,atol=ca.ATOL)
print('Native controlled block and explicit controlled matrix match the same complex branch reference')
```

```text
Native controlled block and explicit controlled matrix match the same complex branch reference
```

<span id="formula-code-5-2-workspace"></span>

### 5. Initialize, compute, use and uncompute

**Contract and formula.** Reserve q0,q1 as data D, q2 as workspace a, and q3 as output t. Both auxiliary inputs are explicitly zero; their roles differ: a must be returned to zero, whereas t carries the computed answer. Let $f(x,y)=x\mathbin{\oplus}y$ and let $\sum_{x,y}|\gamma_{xy}|^2=1$. The basis kets below are always ordered q0,q1,a,t:

$$
\begin{aligned}
\sum_{x,y}\gamma_{xy}|xy,0,0\rangle
&\xrightarrow{C}\sum_{x,y}\gamma_{xy}|xy,f(x,y),0\rangle\\
&\xrightarrow{\mathrm{CX}_{a,t}}\sum_{x,y}\gamma_{xy}|xy,f(x,y),f(x,y)\rangle\\
&\xrightarrow{C^\dagger}\sum_{x,y}\gamma_{xy}|xy,0,f(x,y)\rangle.
\end{aligned}
$$

**Derivation.** C calls CX(q0,a), then CX(q1,a), so its basis action is $a\mapsto a\oplus x\oplus y$. The use step changes t and preserves both data labels and the computed a label. The inverse calls CX(q1,a), then CX(q0,a), so a returns to $f\oplus y\oplus x=0$ on every branch. Linearity extends this to all complex data amplitudes. The workspace consequently factors out as zero (with the declared register ordering); the data and output can remain correlated. This does not copy arbitrary unknown amplitudes into an independent state. It coherently records a basis function.

**Code and verification.** The helper constructs those actual named gates and calls native `compute.adjoint()` for their reverse. `workspace_reference` independently loops over the four data labels and scatters amplitudes into all sixteen output coordinates. No dense full-register gate is used by that reference.

```python
compute=fq.Circuit(4,dtype=D).cx(0,2).cx(1,2)
used=fq.Circuit(4,dtype=D).compose(compute).cx(2,3)
cleaned=fq.Circuit(4,dtype=D).compose(used).compose(compute.adjoint())
factors=ca.data_factors()
data=product_input(factors)
for stage,block in (('use',used),('clean',cleaned)):
    v,p=ca.run(block,factors+[(1,0),(1,0)])
    torch.testing.assert_close(v,ca.workspace_reference(data,stage),rtol=0,atol=ca.ATOL)
    if stage=='clean':assert ca.prob_one(p,2)<ca.ATOL
print('Complex data: all16 amplitudes match after use and uncompute; clean workspace P(1)<1e-12')
```

```text
Complex data: all16 amplitudes match after use and uncompute; clean workspace P(1)<1e-12
```

<span id="formula-code-5-2-contracts"></span>

### 6. A cleanup guarantee has preconditions

**Formula.** For a pure final state expressed by data/output label r and workspace bit a,

$$
|\Psi\rangle=\sum_r z_{r0}|r,0\rangle+\sum_r z_{r1}|r,1\rangle,
\qquad P(a=1)=\sum_r|z_{r1}|^2.
$$

**Derivation.** Orthogonality removes all cross terms in the marginal probability. Exactly zero leakage forces every $z_{r1}=0$ and hence a factorized zero workspace. Here r groups the other qubits conceptually; the code still uses q0,q1,a,q3 order. A computed leakage below tolerance is numerical evidence, not an exact certificate.

Initializing a to one instead gives $a=1\oplus f$ after compute, and restores a to one after uncompute; the recorded output is complemented. Alternatively, start correctly but flip x after use: the inverse uses the changed value, leaving $a=f(x,y)\oplus y\oplus(x\oplus1)=1$. Applying a block's adjoint is not sufficient if the inputs it expects have changed. Preserving the relevant data and computed workspace labels during use is a sufficient condition for this construction, not a necessary condition for every possible cleanup algorithm.

**Code and verification.** Both deliberately incorrect contracts are executed and their incorrect final states are predicted, rather than treated as successful cleanups.

```python
for stage,blank in (('clean',1),('bad-data',0)):
    v,p=ca.run(ca.workspace(stage),factors+ca.basis_factors((blank,0)))
    expected=ca.workspace_reference(data,stage,blank=blank)
    torch.testing.assert_close(v,expected,rtol=0,atol=ca.ATOL)
    assert abs(ca.prob_one(p,2)-1)<ca.ATOL
print('Wrong blank and data changed before inverse: both leave workspace P(1)=1')
```

```text
Wrong blank and data changed before inverse: both leave workspace P(1)=1
```

<span id="formula-code-5-2-interference"></span>

### 7. Forgetting a workspace is not uncomputing it

**Formula.** Starting from 00, H on data followed by CX creates $(|00\rangle+|11\rangle)/\sqrt2$. Without cleanup, a final H on data gives

$$
\frac{|00\rangle+|01\rangle+|10\rangle-|11\rangle}{2},\qquad P(q0=0)=\tfrac12.
$$

With an additional CX before that final H, the two CX gates cancel and the output is 00, with $P(q0=0)=1$.

**Derivation.** Expand H on the first factor of each of the two branches. Their workspace labels differ, so ignoring that label does not make the amplitudes interfere as if it were absent. Uncomputing removes the correlation and restores the interference. A unitary cannot send both orthogonal inputs $|0\rangle_a,|1\rangle_a$ to the same $|0\rangle_a$, since it preserves their inner product. Physical reset involves a different operation and environment contract. No reset or measurement API is used here.

**Code and verification.** This intentionally small experiment checks both the entire vector and the marginal data probability.

```python
for clean,probability in ((False,.5),(True,1.)):
    block=fq.Circuit(2,dtype=D).h(0).cx(0,1)
    if clean:block.cx(0,1)
    block.h(0)
    v,p=ca.run(block,[(1,0),(1,0)])
    expected=torch.tensor([1,0,0,0] if clean else [.5,.5,.5,-.5],dtype=D)
    torch.testing.assert_close(v,expected,rtol=0,atol=ca.ATOL)
    assert abs(p[:2].sum().item()-probability)<ca.ATOL
print('Data P(0): dirty workspace 0.5; uncomputed workspace 1.0')
```

```text
Data P(0): dirty workspace 0.5; uncomputed workspace 1.0
```

<span id="formula-code-5-2-boundaries"></span>

### 8. Reject unsupported contracts explicitly

**Formula and boundary.** A projector $P=\operatorname{diag}(1,0)$ fails $P^\dagger P=I$, so the controlled-unitary theorem does not apply. Numerical unitarity checks use absolute tolerance $10^{-12}$ and relative tolerance zero; they do not prove exact symbolic unitarity. Wrong shapes, nonfinite entries and the wrong precision are also refused by the book helper.

**Code.** Native block control in FlagQuantum 0.3.1 requires newly added control qubits outside the original source register. Its custom-matrix controlled form is not implemented: it raises `CapabilityError`. The explicitly constructed unitary C(U) route above is executable. We do not silently replace an unsupported native operation with an unreported approximation. The workspace helper also refuses an undeclared `reset` stage; this is our helper contract, not a claim to have called a native reset method.

```python
rejected=0
checks=[(ValueError,lambda:ca.controlled_matrix(2*ca.X)),
        (ValidationError,lambda:source.control(1,ctrl_qubits=(0,))),
        (CapabilityError,lambda:fq.Circuit(1,dtype=D).unitary(0,unitary=ca.X).control(1,ctrl_qubits=(1,))),
        (ValueError,lambda:ca.workspace('reset'))]
for error,action in checks:
    try:action()
    except error:rejected+=1
assert rejected==4 and ca.RUNS==11
print('4 invalid contracts rejected; 11 actual body circuits; no reset or hardware execution')
```

```text
4 invalid contracts rejected; 11 actual body circuits; no reset or hardware execution
```

### Run the complete example

```bash
python examples/foundations/controlled_ancillas.py
python scripts/check_controlled_ancillas_prose.py
```

The complete program runs **100 actual circuits**: 47 generic controlled-unitary cases (all basis inputs, complex products, reversed/nonadjacent supports and a two-target matrix), 16 named CX cases, nine CCX cases, six native block-control cases, two phase analyzers, eighteen workspace-stage/contract cases and two interference cases. Direct branch sums, scalar ordered-support action and bit-index scatter references check full complex coordinates. Ten invalid contracts are rejected. The eight cumulative body fragments run eleven additional circuits; a separate unseen-parameter transfer below is also executed by the author. These finite implementation checks supplement the general projector and linearity proofs; they are not independent review.

Expected output of the complete program:

```text
Controlled matrix uses ordered support(control,target...); no measurement of the control.
47generic controlled circuits: basis,complex,nonadjacent and two-target cases; scalar/branch references agree.
16named CX basis circuits and9CCX basis/superposition circuits checked.
6native block-control circuits: added controlq1,targetq0,then explicit placement map; source retained.
2controlled-phase analyzer circuits: C(I) ->00; C(-I) ->10; target global phase is observable on control.
18parity workspace circuits: coherent stages,clean ancilla,wrong blank,data-change and initial-output boundaries.
2coherence circuits: data P0=0.5without cleanup,1.0with uncompute;10invalid contracts rejected.
100 actual CPU complex128 circuits; atol=1e-12,rtol=0; no control measurement,reset,shots or hardware.
```

### Understanding checks and transfer exercises

**5.2-A — Transfer the control phase.** Use $U=e^{0.31i}R_x(-0.52)$, target zero and control $(0.6,0.8i)$. Give all four amplitudes and implement the gate on ordered support (1,0), with q1 as control. Which entries must be permuted relative to control-first coordinates?

**5.2-B — Output initialization.** In the parity example, keep workspace zero but initialize t to one. Which qubit is cleaned, and what remains in t? Does a nonzero output imply failed cleanup?

**5.2-C — Scope of cleanup.** Why does changing data before the displayed inverse break its guarantee? Does the example prove that no computation can ever change data and clean an ancilla?

**5.2-D — Numerical evidence.** Is $P(a=1)<10^{-12}$ an exact proof of zero workspace? Would checking only computational probabilities detect dropping the target's global phase before control?

<details markdown="1">
<summary>Answers and reasoning</summary>

**A.** Put $c=\cos(0.26)$ and $s=\sin(0.26)$. Since $R_x(-0.52)|0\rangle=c|0\rangle+i s|1\rangle$, control-first coordinates are $(0.6,0,0.8i e^{0.31i}c,-0.8e^{0.31i}s)$. In q0,q1 order with target q0 and control q1 they are $(0.6,0.8i e^{0.31i}c,0,-0.8e^{0.31i}s)$. The author separately executes the generic controlled matrix with support (1,0), checks this explicit trigonometric reference, and compares the native phase-tracked named-gate block controlled on added q1. No phase alignment is applied.

**B.** The final branch is $|xy,0,1\mathbin{\oplus}f(x,y)
angle$. Workspace a is cleaned, while t correctly holds a complemented output under the changed input contract. Cleanup is specified per role, not by requiring every qubit to be zero. The complete program checks this case independently.

**C.** The inverse reads changed computational labels and therefore need not undo the stored old function value. The sufficient unchanged-label contract has been violated. This is a counterexample to an unconditional guarantee, not an impossibility theorem for all algorithms that change data; an alternative cleanup may retain or reconstruct the necessary information.

**D.** No: the inequality is a finite-precision numerical check. The exact factorization statement follows from the zero sum of nonnegative squared amplitudes. Raw computational probabilities can miss a phase discrepancy, but the control H analyzer converts the branch phase into different probabilities. Exact vector checks and explicit phase context remain required.

</details>

### Sources, limits and next step

Depth **F**: the orthogonal-projector proof of controlled unitarity, coherent superposition action, controlled-product identity, basis-wise compute/use/uncompute proof and zero-workspace criterion are supplied explicitly. Assigned background: Nielsen and Chuang, 10th Anniversary Edition (2010), §4.3. No fresh inspection of the local third-party PDF is claimed. Installed released FlagQuantum source/signatures for `cx`, `ccx`, `control`, `compose` and `adjoint` were inspected or exercised; numerical matrices retain their full phase. Named-gate inverse use stays within the unitary scope and preserves the previously documented [5.1 boundary](#formula-code-5-1-boundaries).

The examples cover fixed ideal pure-state circuits, not reset, noisy channels, hardware feedback, gradients or fault-tolerant ancilla preparation. No resource-optimal decomposition is claimed. The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/5.2.json) separates author execution from independent mathematical review, implementation review and reader trials, all still pending. This is a working draft. Next, when drafted: [5.3 Classical logic made reversible](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-3).
