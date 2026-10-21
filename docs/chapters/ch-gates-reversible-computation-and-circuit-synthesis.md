# 5. Gates, Reversible Computation, and Circuit Synthesis

**Working drafts: sections 5.1–5.5 · Writing Baseline 1.0 · October 21, 2026.** Author execution is separate from independent mathematical, implementation and reader review, which remain pending. Examples use installed released FlagQuantum 0.3.1 and PyTorch 2.13.0 on CPU with complex128 statevectors.

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

The examples cover fixed ideal pure-state circuits, not reset, noisy channels, hardware feedback, gradients or fault-tolerant ancilla preparation. No resource-optimal decomposition is claimed. The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/5.2.json) separates author execution from independent mathematical review, implementation review and reader trials, all still pending. This is a working draft. Continue with [5.3 Classical logic made reversible](#sec-gates-reversible-computation-and-circuit-synthesis-3).


<span id="sec-gates-reversible-computation-and-circuit-synthesis-3"></span>

## 5.3 Classical logic made reversible

Classical AND forgets which of several inputs produced zero. A closed unitary circuit cannot forget that distinction: its full input/output map must be invertible. The remedy is to retain enough information, write a function value into a separate output register, and clean any temporary workspace without erasing the retained answer.

Prerequisites: [4.2](ch-composite-systems-tensor-products-and-qubit-ordering.md#sec-composite-systems-tensor-products-and-qubit-ordering-2) for basis indices and [5.2](#sec-gates-reversible-computation-and-circuit-synthesis-2) for coherent controls and explicit ancilla contracts. All gates here act ideally on finite qubit registers, q0 is the most significant bit, and XOR means bitwise addition modulo two. The eight cumulative formula–derivation–code–result units below use released FlagQuantum 0.3.1 and PyTorch 2.13.0 on CPU with complex128 precision. Run from the repository root in the pinned example environment. The companion [reversible_logic.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/reversible_logic.py) contains all helpers and complete tests.

<span id="formula-code-5-3-collision"></span>

### 1. Why an irreversible truth table is not a unitary gate

**Formula.** AND is a deterministic function $f:\{0,1\}^2\to\{0,1\}$ with table $(0,0,0,1)$ in input order 00,01,10,11. Trying to overwrite a fixed two-qubit input by $|0,f(x)\rangle$ gives, among others,

$$
|00\rangle\longmapsto|00\rangle,\qquad
|01\rangle\longmapsto|00\rangle.
$$

**Derivation.** The inputs have inner product zero, while the proposed outputs have inner product one. A unitary preserves inner products, so this cannot be its action. The difficulty is information loss, not the particular gate notation. If extra output labels distinguish the colliding inputs, the full map may be reversible; those labels then hold information that cannot simply be discarded inside a unitary circuit. For an in-place map between equally sized computational bases, bijectivity is necessary and sufficient for its basis permutation to be unitary.

**Code and verification.** This first check is classical matrix algebra: there is deliberately no attempt to submit a nonunitary AND-overwrite matrix as a FlagQuantum gate. The following units construct the valid unitary embedding.

```python
import sys
sys.path.insert(0,'.')
import torch
import flagquantum as fq
from math import sqrt
from examples.foundations import reversible_logic as rl
D=rl.DTYPE
and_table=[0,0,0,1]
overwrite=torch.zeros((4,4),dtype=D)
for x,fx in enumerate(and_table):overwrite[fx,x]=1
assert torch.vdot(overwrite[:,0],overwrite[:,1]).item()==1
assert not torch.equal(overwrite.mH@overwrite,torch.eye(4,dtype=D))
print('AND overwrite merges orthogonal columns: not a unitary operation')
```

```text
AND overwrite merges orthogonal columns: not a unitary operation
```

<span id="formula-code-5-3-oracle"></span>

### 2. Preserve the input and XOR into an output register

**Theorem and formula.** Let $f:\{0,1\}^n\to\{0,1\}^m$ be any fixed finite deterministic function, with positive integers n,m. Bitwise XOR acts on the m output bits. Define

$$
U_f|x\rangle|y\rangle=|x\rangle|y\mathbin{\oplus}f(x)\rangle.
$$

Then $U_f$ extends uniquely by linearity to a unitary and $U_f^2=I$, even when f is many-to-one. A zero output gives the familiar $|x,0\rangle\mapsto|x,f(x)\rangle$; the definition must also specify nonzero y.

**Derivation.** For any output pair $(x',y')$, its unique preimage is $(x',y'\oplus f(x'))$. Applying the map twice restores y because each bit satisfies $b\oplus b=0$. Thus the basis map is bijective and self-inverse. For basis pairs, orthogonality follows explicitly:

$$
\langle x',y'|U_f^\dagger U_f|x,y\rangle
=\delta_{x'x}\,\delta_{y'\oplus f(x'),\,y\oplus f(x)}
=\delta_{x'x}\delta_{y'y}.
$$

When $x'\ne x$ the first delta is zero; when $x'=x$, XOR by the same bit string is invertible. This proves $U_f^\dagger U_f=I$; bijectivity also proves the reverse product and the self-inverse claim. Consequently $U_f^\dagger=U_f$. In coordinates, using q0 as the most significant bit and input register first,

$$
j=2^m x+y,\qquad (U_f v)_{2^m x+y}=v_{2^m x+(y\oplus f(x))}.
$$

**Code and verification.** `oracle_matrix` is a bounded book helper that builds this permutation, not a native oracle compiler. `oracle_reference` independently pulls each output coordinate from its inverse input. `rl.run` prepares normalized input factors outside the block and actually calls FlagQuantum with the pinned statevector/PyTorch/CPU/complex128 options, probabilities enabled, and fallback/approximation disabled. It checks batch-one shapes, precision and probabilities before returning unbatched vectors. No phase alignment or normalization repair is used.

```python
U=rl.oracle_matrix(and_table,2,1)
assert torch.equal(U@U,torch.eye(8,dtype=D))
block=fq.Circuit(3,dtype=D).unitary(0,1,2,unitary=U)
factors=rl.complex_factors(3)
initial=rl.product_input(factors)
v,p=rl.run(block,factors)
torch.testing.assert_close(v,rl.oracle_reference(initial,and_table,2,1),rtol=0,atol=rl.ATOL)
roundtrip=fq.Circuit(3,dtype=D).compose(block).compose(block)
v,p=rl.run(roundtrip,factors)
torch.testing.assert_close(v,initial,rtol=0,atol=rl.ATOL)
print('AND XOR-embedding: complex input matches inverse-index reference; U_f twice restores all coordinates')
```

```text
AND XOR-embedding: complex input matches inverse-index reference; U_f twice restores all coordinates
```

<span id="formula-code-5-3-primitives"></span>

### 3. Translate Boolean gates into X, CX and CCX

**Formulas.** With fresh target t initially zero, retain a,b and write a Boolean gate into t:

$$
\begin{aligned}
\mathrm{NOT}:&\quad t\mapsto t\oplus1\oplus a,\\
\mathrm{XOR}:&\quad t\mapsto t\oplus a\oplus b,\\
\mathrm{AND}:&\quad t\mapsto t\oplus ab,\\
\mathrm{OR}:&\quad t\mapsto t\oplus a\oplus b\oplus ab.
\end{aligned}
$$

**Derivation.** NOT a equals $1\oplus a$. AND is the bit product ab, so its XOR embedding is CCX(a,b,t). XOR requires two CX gates to the same target. The four pairs 00,01,10,11 give $a\oplus b\oplus ab=0,1,1,1$, proving the OR identity. Every displayed operation is defined for both t values; each is a permutation rather than a destructive overwrite. A direct NOT on a single retained computational bit is already the reversible X gate; the two-qubit NOT embedding additionally preserves the original a.

**Code.** These are actual released named gates. The loop tests complex input vectors, including a superposed target. The complete example additionally checks every computational basis input, including target one. The input controls of a CCX must refer to distinct qubits; repeated Boolean inputs should be simplified first (for example $a\land a=a$, $a\oplus a=0$).

```python
named={
 'NOT':(fq.Circuit(2,dtype=D).x(1).cx(0,1),[1,0],1),
 'AND':(fq.Circuit(3,dtype=D).ccx(0,1,2),[0,0,0,1],2),
 'XOR':(fq.Circuit(3,dtype=D).cx(0,2).cx(1,2),[0,1,1,0],2),
 'OR':(fq.Circuit(3,dtype=D).cx(0,2).cx(1,2).ccx(0,1,2),[0,1,1,1],2)
}
for name,(c,table,n) in named.items():
    factors=rl.complex_factors(n+1)
    v,p=rl.run(c,factors)
    expected=rl.oracle_reference(rl.product_input(factors),table,n,1)
    torch.testing.assert_close(v,expected,rtol=0,atol=rl.ATOL)
print('NOT,AND,XOR,OR: named gates match four independently indexed complex-output references')
```

```text
NOT,AND,XOR,OR: named gates match four independently indexed complex-output references
```

<span id="formula-code-5-3-outputs"></span>

### 4. Keep multiple output bits in their declared order

**Formula.** A half-adder has sum $s=a\oplus b$ and carry $c=ab$. Declare output order (s,c), so its encoded integer is $f(a,b)=2s+c$. This gives table $(0,2,2,1)$ and embedding

$$
|a,b,u,v\rangle\longmapsto
|a,b,u\oplus(a\oplus b),v\oplus ab\rangle.
$$

**Derivation.** The first output bit is the most significant bit of the two-bit output register. Thus input 01 produces output 10, encoded as two, whereas input 11 produces 01, encoded as one. This is a four-qubit embedding that preserves both inputs, not an in-place two-qubit addition. Each output is XORed with its own declared initial bit, so arbitrary u,v are valid. There is no carry-workspace to clean in this direct construction.

**Code and verification.** The two implementations below share only the declared truth table: one uses a dense permutation matrix and the other three named gates. Every complex coordinate is compared with the scalar inverse-index reference.

```python
half_table=[0,2,2,1]
dense=fq.Circuit(4,dtype=D).unitary(0,1,2,3,unitary=rl.oracle_matrix(half_table,2,2))
half=fq.Circuit(4,dtype=D).cx(0,2).cx(1,2).ccx(0,1,3)
factors=rl.complex_factors(4)
expected=rl.oracle_reference(rl.product_input(factors),half_table,2,2)
for c in (dense,half):
    v,p=rl.run(c,factors)
    torch.testing.assert_close(v,expected,rtol=0,atol=rl.ATOL)
print('Half-adder (sum,carry): encoded table [0,2,2,1]; dense and named-gate complex vectors agree')
```

```text
Half-adder (sum,carry): encoded table [0,2,2,1]; dense and named-gate complex vectors agree
```

<span id="formula-code-5-3-recipe"></span>

### 5. Turn a finite classical circuit into a reversible computation

**Construction.** A finite deterministic truth table has a finite Boolean expression: OR the input minterms for which each output bit is one, using NOT for zero-valued input literals; a constant-zero output has no true minterms. AND, OR and NOT can be realized using the identities above. This establishes existence, not an efficient implementation of an arbitrary table.

Process the resulting acyclic classical gate list in topological order. Retain the input bits; assign a distinct fresh zero workspace qubit to each computed intermediate gate output. Implement each gate with its XOR embedding, leaving all prior inputs and stored gate results intact. If a Boolean gate repeats the same input, simplify it as noted above. For a NOT gate, use X on its fresh target followed by CX from its input. A constant one uses X on its fresh target; constant zero needs no gate.

**Formula and proof.** Induct over the gate list. Initially the input x is retained and every fresh target is zero. If earlier stored values agree with the classical evaluation, the next XOR embedding writes exactly the next classical gate value into its zero target, changing none of those stored values. Hence a finite unitary computation C satisfies, on the specified input subspace,

$$
C|x\rangle|0^r\rangle=|x\rangle|h(x)\rangle,
$$

where h includes all stored intermediate values and output values. The action on other workspace inputs is still unitary, but is not generally this classical computation. This induction does not claim that its chosen workspace is minimal.

**Concrete code.** For $g(a,b,c)=(a\land b)\oplus c$, reserve q0,q1,q2 for data, q3 for temporary AND value w and q4 for output y. The intermediate is $w=ab$, computed by one CCX. This small network needs only the AND intermediate; its final XOR will be written directly to y in the next unit.

```python
compute=fq.Circuit(5,dtype=D).ccx(0,1,3)
factors=rl.complex_factors(3)+[(1,0),(1,0)]
initial=rl.product_input(factors)
v,p=rl.run(compute,factors)
torch.testing.assert_close(v,rl.network_reference(initial,'compute'),rtol=0,atol=rl.ATOL)
expected_leak=.64*.3
assert abs(rl.probability_one(p,3)-expected_leak)<rl.ATOL
print('AND workspace computed coherently; P(w=1)=0.192 before cleanup')
```

```text
AND workspace computed coherently; P(w=1)=0.192 before cleanup
```

<span id="formula-code-5-3-cleanup"></span>

### 6. Retain the answer and reverse temporary computation

**Formula.** For the concrete network, with arbitrary output bit y and zero initial w,

$$
\begin{aligned}
|a,b,c,0,y\rangle
&\longmapsto |a,b,c,ab,y\rangle\\
&\longmapsto |a,b,c,ab,y\oplus ab\oplus c\rangle\\
&\longmapsto |a,b,c,0,y\oplus g(a,b,c)\rangle.
\end{aligned}
$$

**Derivation.** The use step calls CX(w,y) and CX(c,y), leaving the data and w unchanged. The inverse of the AND computation toggles w by ab again, restoring zero. The final state retains the answer in y; reversing the *entire* used circuit would also erase that answer.

For the general stored classical computation C of unit 5, append an m-qubit output register Y and CX each stored output bit into its corresponding Y bit. These CX gates preserve x and the entire stored h(x). Now apply $C^\dagger$ on X and workspace only. On each basis component the overall map is

$$
|x,0^r,y\rangle\longmapsto|x,h(x),y\rangle
\longmapsto|x,h(x),y\oplus f(x)\rangle
\longmapsto|x,0^r,y\oplus f(x)\rangle.
$$

The inverse step is valid because its input X/workspace is exactly the previously computed pair; the retained output register is not a target of that inverse. Linearity proves the same statement for any superposition $\sum_{x,y}\alpha_{xy}|x,0^r,y\rangle$, including correlated X,Y inputs. All nonzero final amplitudes have zero workspace, so it factors out and can be reused. The data/output need not factorize. Copying stored computational-basis labels by CX does not make independent copies of an unknown quantum state, as established in 4.7. Section 5.4 develops broader workspace reuse contracts and tradeoffs; this is the finite Boolean construction needed here.

**Code and verification.** The actual inverse is built from the named compute block, whose unitary gates satisfy the precondition of native `adjoint`. We inspect the full vectors both before and after cleanup.

```python
used=fq.Circuit(5,dtype=D).compose(compute).cx(3,4).cx(2,4)
cleaned=fq.Circuit(5,dtype=D).compose(used).compose(compute.adjoint())
for stage,c in (('use',used),('clean',cleaned)):
    v,p=rl.run(c,factors)
    torch.testing.assert_close(v,rl.network_reference(initial,stage),rtol=0,atol=rl.ATOL)
    if stage=='clean':assert rl.probability_one(p,3)<rl.ATOL
print('Use retains answer; inverse of compute restores workspace zero; all32 complex coordinates checked')
```

```text
Use retains answer; inverse of compute restores workspace zero; all32 complex coordinates checked
```

<span id="formula-code-5-3-coherence"></span>

### 7. Test wrong blanks, changed data and coherent outputs

**Boundary formulas.** If the initial workspace bit is w rather than zero, the displayed network instead produces

$$
|a,b,c,w,y\rangle\longmapsto
|a,b,c,w,y\oplus w\oplus ab\oplus c\rangle.
$$

Thus a wrong blank is returned unchanged but contaminates the answer. If a is flipped before the inverse, starting with w=0, the workspace ends at $ab\oplus(a\oplus1)b=b$. For b=1 it is certainly dirty. These are contract failures, not numerical noise.

**Coherent action.** An oracle is a linear quantum operation, not an instruction to sample x and evaluate f classically. For example

$$
U_f\sum_x\alpha_x|x\rangle|0\rangle
=\sum_x\alpha_x|x,f(x)\rangle.
$$

For a one-bit output prepared in $|-\rangle=(|0\rangle-|1\rangle)/\sqrt2$, the identity $X|-\rangle=-|-\rangle$ gives

$$
U_f\sum_x\alpha_x|x\rangle|-\rangle
=\sum_x(-1)^{f(x)}\alpha_x|x\rangle|-\rangle.
$$

**Derivation and verification.** On each basis branch, XOR by zero is identity and XOR by one applies X. Factoring its minus-target eigenvalue out gives the branch sign. Computational probabilities alone miss that sign; the code checks exact complex coordinates with no phase alignment. The complete program also checks an entangled input made by H and CX before the oracle.

```python
for stage,bits in (('clean',(1,1,0,1,0)),('bad-data',(1,1,0,0,0))):
    f=rl.basis_factors(bits)
    v,p=rl.run(rl.network(stage),f)
    torch.testing.assert_close(v,rl.network_reference(rl.product_input(f),stage),rtol=0,atol=rl.ATOL)
    assert abs(rl.probability_one(p,3)-1)<rl.ATOL
f=rl.complex_factors(2)+[(1/sqrt(2),-1/sqrt(2))]
v,p=rl.run(fq.Circuit(3,dtype=D).ccx(0,1,2),f)
expected=rl.product_input(f);expected[6:]*=-1
# Indices6,7 are input11 followed by either output bit.
torch.testing.assert_close(v,expected,rtol=0,atol=rl.ATOL)
print('Wrong blank and changed data fail as predicted; minus-target AND branch phase verified')
```

```text
Wrong blank and changed data fail as predicted; minus-target AND branch phase verified
```

<span id="formula-code-5-3-limits"></span>

### 8. Distinguish existence, implementation and efficiency

**Resource statement.** A dense $U_f$ for n+m qubits has $2^{n+m}$ basis columns and $2^{2(n+m)}$ stored matrix entries. Building that matrix proves no efficient synthesis theorem. A truth-table minterm construction can also be exponential in n. For a *given* classical Boolean circuit with L intermediate gate results, the construction above uses at most L stored result qubits plus the separate output register. Its named-gate compute and reverse use a constant number of X/CX/CCX gates per Boolean gate, with additional CX gates for the m output bits. These are logical counts; hardware connectivity and decomposition costs are outside this statement.

**Input/output contract.** The dense helper accepts positive literal integer n,m with n+m at most six and exactly $2^n$ literal integer table entries in $[0,2^m)$. It preserves declared input-first/output-second bit order. Its six-qubit bound is an educational memory guard, not a FlagQuantum limit. The helper does not parse arbitrary Python callables, validate a supplied implementation against an unstated paper, or synthesize an efficient hardware oracle. Approximate, probabilistic and externally stateful functions require different specifications.

**Code and verification.** Wrong widths, Boolean-as-integer entries, out-of-range outputs and undeclared workspace operations are rejected before running a circuit. A simulated leakage below $10^{-12}$ is numerical evidence of cleanup; the mathematical factorization follows from the exact basis proof above, not from treating a floating-point tolerance as a theorem.

```python
rejected=0
for action in (lambda:rl.oracle_matrix([0,0,0,True],2,1),
               lambda:rl.oracle_matrix([0,0,0,2],2,1),
               lambda:rl.oracle_matrix([0,0,0,1],2,5),
               lambda:rl.network('reset')):
    try:action()
    except ValueError:rejected+=1
assert rejected==4 and rl.RUNS==14
print('4 malformed contracts rejected;14 actual body circuits; no reset or synthesis API invented')
```

```text
4 malformed contracts rejected;14 actual body circuits; no reset or synthesis API invented
```

### Run the complete example

```bash
python examples/foundations/reversible_logic.py
python scripts/check_reversible_logic_prose.py
```

The complete program executes **267 actual circuits**: 160 runs cover all sixteen two-input/one-output truth tables on every basis input, a complex product and a self-inverse roundtrip; 35 runs compare dense and named-gate half-adders on every basis input and a complex product, plus a dense roundtrip; 32 runs check the four named Boolean gate constructions; 36 runs check all basis inputs of the five-qubit network, a complex full-register product and three coherent stages with initially zero workspace; three runs cover minus-target phase and two wrong-contract witnesses; one more checks an entangled input. The latter prepares $(|00\rangle+|11\rangle)/\sqrt2$ on the AND inputs before its XOR embedding, and verifies $(|000\rangle+|111\rangle)/\sqrt2$ on all coordinates. Eleven malformed contracts are rejected.

The eight actual body fragments run fourteen circuits in a separate invocation, and their complete printed output is checked exactly. An additional majority-function transfer is recorded below. Initial 250-run evidence is retained from before adding the seventeen named-gate half-adder basis/complex checks; it was a passing coverage stage, not a failed run. Small exhaustive examples validate these implementations; they do not replace the general bijection and construction proofs.

Expected output of the complete program:

```text
16 Boolean functions: all8 basis inputs,complex input and U_f squared checked;160circuits.
Two-output half-adder table [0,2,2,1]: dense and named-gate paths,all16 inputs,complex input and roundtrip;35circuits.
Named X,CX,CCX constructions of NOT,AND,XOR,OR: all target bits and complex inputs;32circuits.
g(a,b,c)=(a AND b) XOR c: all32 network inputs,complex input and3coherent stages;36circuits.
Minus-target phase kickback and2wrong-contract witnesses:3circuits; workspace failures predicted.
Entangled input checked;11invalid contracts rejected;267actual CPUcomplex128 circuits,atol1e-12,rtol0.
Dense oracle helper limited to n+m<=6; no efficient-synthesis,reset,shots,noise or hardware claim.
```

### Understanding checks and transfer exercises

**5.3-A — A new Boolean function.** The three-input majority function equals one when at least two inputs are one. Derive a circuit with three CCX gates and no workspace beyond its XOR output. Test arbitrary output bits and a complex superposition.

**5.3-B — Nonzero output.** For the half-adder, take input 11 and initial output 10. What are the final output bits? Why is this not a malfunction of the function embedding?

**5.3-C — Retain versus erase.** Why does reversing the entire computation after copying into a separate output preserve the copied answer, while reversing the entire used block in the concrete network would erase it? Specify which registers each inverse targets.

**5.3-D — Classical and quantum scope.** Does this construction imply an efficient oracle for every truth table? Can it evaluate both branches by first measuring a superposed input and then preparing the classical answer? Explain both limits.

<details markdown="1">
<summary>Answers and reasoning</summary>

**A.** Majority is $ab\oplus ac\oplus bc$. With zero, one, two or three ones in the input, the number of true pair products is respectively zero, zero, one or three; its parity is therefore zero, zero, one or one. Apply `ccx(0,1,3)`, `ccx(0,2,3)`, then `ccx(1,2,3)`. The target becomes its initial bit XOR majority. The separate author transfer tests all sixteen input/output basis states and one complex product on this named-gate circuit, then a dense permutation on the same complex input: eighteen actual executions. The reference table is independently generated from the threshold test $a+b+c\ge2$, not from the pair-product expression. This special simplification does not establish a minimal circuit theorem or eliminate workspace from every Boolean computation.

**B.** On 11, the function output (sum,carry) is 01, so $10\oplus01=11$. Only a zero initial output returns the function value without an XOR offset; the unitary is specified on all initial outputs.

**C.** In the general construction, the copied output Y is separate and untouched by the inverse of C, which targets only X and its computed workspace. In the concrete network, `compute.adjoint()` acts on the AND computation only; the retained y is not a target. Inverting the whole `used` block would first undo the XOR writes to y and then undo the AND computation, returning y to its initial state. Reversibility alone does not choose which answer is to be retained; register roles do.

**D.** No efficient implementation follows from a dense permutation or minterm existence proof: either may have exponential size. If an algorithm assumes oracle access, the oracle's actual construction and cost still need accounting. Measuring the input destroys coherent branch phases and correlations, so measure/evaluate/reprepare is not the unitary $U_f$ on an arbitrary superposition. The minus-target example distinguishes the required phase-sensitive action from a mere list of classical output probabilities.

</details>

### Sources, depth and next step

Depth **F**: the collision/inner-product obstruction, inverse-pair bijection, both-sided unitarity, self-inverse XOR embedding, finite Boolean-circuit construction and its zero-workspace cleanup proof are explicit. Assigned background: Nielsen and Chuang, 10th Anniversary Edition (2010), §3.1.2. No fresh inspection of the user-local PDF is claimed. The source/signatures of the installed released FlagQuantum named gates, custom unitary placement and native compose/adjoint were inspected or exercised; the book helpers are separately labeled. This section does not introduce a new native compiler API. The prior [nonunitary adjoint boundary](#formula-code-5-1-boundaries) is preserved; all inverse blocks here contain named unitary gates.

The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/5.3.json) records execution, exact expected outputs, a separate new-function transfer and the finite resource guard. Independent mathematical review, implementation review and reader trials remain pending. No reset, physical erasure, noise, hardware or efficient general synthesis was executed or claimed. Continue with [5.4 Uncomputation and reusable workspace](#sec-gates-reversible-computation-and-circuit-synthesis-4).


<span id="sec-gates-reversible-computation-and-circuit-synthesis-4"></span>

## 5.4 Uncomputation and reusable workspace

A temporary qubit is reusable when the circuit restores its specified state and removes its correlations with everything retained. Applying an inverse somewhere in a program does not establish that contract. We must identify exactly which registers the inverse sees, what the intervening use changed, and where the answer is kept.

[5.3](#sec-gates-reversible-computation-and-circuit-synthesis-3) constructed finite Boolean computations from retained basis labels. Here the workspace may itself contain complex superpositions. We prove the cleanup statement under an explicit orthogonal output-encoding assumption, then reuse the same auxiliaries in a continuous computation whose retained registers are correlated. All register positions and phases are retained; q0 remains the most significant basis bit. The eight cumulative units use the pinned released FlagQuantum 0.3.1/PyTorch 2.13.0 CPU complex128 environment. Helpers and complete executable checks are in [reusable_workspace.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/reusable_workspace.py).

<span id="formula-code-5-4-roles"></span>

### 1. Declare which registers must be reusable

**Contract.** Let D hold n input qubits, W hold r temporary qubits, F hold m computed output qubits and Y hold m retained output qubits. Only W and F must be restored to zero; Y records the answer. Suppose a fixed unitary C satisfies

$$
C|x,0^r,0^m\rangle=|x\rangle|g_x\rangle|f(x)\rangle.
$$

Here $f(x)\in\{0,1\}^m$, while $|g_x\rangle$ is any normalized workspace vector, including a coherent superposition and branch-dependent phase. The formula is an assumption about C on a specified subspace, not on arbitrary workspace inputs. F is in a definite computational basis code for each basis x. That encoding enables a copy operation which leaves C's full output unchanged apart from the separate Y register.

**Concrete derivation.** Use D=q0, W=q1, F=q2, Y=q3. Our C retains D, computes $f(d)=d$ in F, but deliberately makes W a complex superposition. Its chronological gates are CX(D,F), H(W), Rz(W,φ), CX(D,W), Rz(F,η), Rz(D,δ). With radians φ=0.43, η=−0.71, δ=0.37,

$$
C|d,0,0\rangle=\gamma_d|d\rangle
\frac{e^{-i\phi/2}|d\rangle+e^{i\phi/2}|1\oplus d\rangle}{\sqrt2}|d\rangle,
\qquad \gamma_d=e^{-i(\eta+\delta)(-1)^d/2}.
$$

H creates the two W amplitudes, Rz supplies their opposite half-angle phases, and CX flips the W label when d=1. The last two rotations supply γ. Thus neither W's zero state nor its phase can be inferred by reading F alone.

**Code and verification.** Imports and fragments are cumulative; run from the repository root. The explicit coefficient loop checks every complex output coordinate, including γ. The book runner prepares input factors outside the block, invokes actual `fq.run` with the pinned CPU/PyTorch/statevector complex128 options and probabilities enabled, and checks batch-one shapes and precision. Approximation and backend fallback are disabled. The four-qubit C leaves Y untouched throughout.

```python
import sys
sys.path.insert(0,'.')
import cmath,torch
from math import sqrt
import flagquantum as fq
from examples.foundations import reusable_workspace as rw
D=rw.D
C=fq.Circuit(4,dtype=D).cx(0,2).h(1).rz(1,.43).cx(0,1).rz(2,-.71).rz(0,.37)
factors=[(.6,.8j),(1,0),(1,0),(1,0)]
v,p=rw.run(C,factors)
expected=torch.zeros(16,dtype=D)
for d,alpha in enumerate((.6,.8j)):
    gamma=cmath.exp(-.5j*(-.71+.37)*(-1)**d)
    for t in (0,1):
        expected[8*d+4*(t^d)+2*d]=alpha*gamma*cmath.exp((.5j if t else -.5j)*.43)/sqrt(2)
torch.testing.assert_close(v,expected,rtol=0,atol=rw.ATOL)
print('C computes F=d with complex coherent W and branch phases; all16 coordinates match the analytic formula')
```

```text
C computes F=d with complex coherent W and branch phases; all16 coordinates match the analytic formula
```

<span id="formula-code-5-4-theorem"></span>

### 2. Prove compute-copy-uncompute on the full input subspace

**Theorem.** Let $K=\prod_{j=0}^{m-1}\mathrm{CX}_{F_j,Y_j}$, with the declared bit correspondence. It maps $|z\rangle_F|y\rangle_Y$ to $|z\rangle_F|y\oplus z\rangle_Y$. Define $T=(C^\dagger\otimes I_Y)K(C\otimes I_Y)$. Then

$$
T|x,0^r,0^m,y\rangle
=|x,0^r,0^m,y\oplus f(x)\rangle.
$$

**Proof, tracking every register.** By the assumption on C and by linearity in the workspace vector,

$$
\begin{aligned}
|x,0^r,0^m,y\rangle
&\longmapsto |x\rangle|g_x\rangle|f(x)\rangle|y\rangle\\
&\longmapsto |x\rangle|g_x\rangle|f(x)\rangle|y\oplus f(x)\rangle\\
&\longmapsto |x,0^r,0^m,y\oplus f(x)\rangle.
\end{aligned}
$$

The middle step does not change D,W,F: every component of $|g_x\rangle$ has the same F code f(x), so K makes the same Y change on each component. The last step therefore receives exactly $C|x,0^r,0^m\rangle$ on its own registers, and C-dagger restores them. All phases contained in $|g_x\rangle$ are removed by this exact inverse; we do not delete or align those phases numerically. Applying linearity once more proves

$$
T\sum_{x,y}\alpha_{xy}|x,0^r,0^m,y\rangle
=\sum_{x,y}\alpha_{xy}|x,0^r,0^m,y\oplus f(x)\rangle.
$$

This includes correlated D,Y inputs. It does not require D and Y to remain separate states after evaluation. W and F do factor out as their zero vector; this is the reusable-workspace guarantee.

**Code and verification.** Copy F into the separate Y, then invert only C. The independent reference uses scalar bit updates and complex rotation phases, without reading circuit IR or simulator output. Its clean-subspace result is also checked against the much simpler ideal CX(D,Y).

```python
used=fq.Circuit(4,dtype=D).compose(C).cx(2,3)
cleaned=fq.Circuit(4,dtype=D).compose(used).compose(C.adjoint())
for stage,c in (('use',used),('clean',cleaned)):
    v,p=rw.run(c,factors)
    expected=rw.reference(rw.product_input(factors),rw.ops_for(stage))
    torch.testing.assert_close(v,expected,rtol=0,atol=rw.ATOL)
    if stage=='clean':
        torch.testing.assert_close(v,rw.clean_reference(factors),rtol=0,atol=rw.ATOL)
        assert rw.leakage(p)<rw.ATOL
print('Copy retains Y; C-dagger restores both W and F; clean action equals CX(D,Y) without phase alignment')
```

```text
Copy retains Y; C-dagger restores both W and F; clean action equals CX(D,Y) without phase alignment
```

<span id="formula-code-5-4-target"></span>

### 3. The retained target need not start in zero

**Formula.** The theorem defines an XOR operation on Y, not an overwrite:

$$
\sum_{x,y}\alpha_{xy}|x,y\rangle_{D,Y}
\longmapsto\sum_{x,y}\alpha_{xy}|x,y\oplus f(x)\rangle_{D,Y},
$$

with the zero W,F factors understood in their original register positions. Zero Y exposes f(x) directly. For nonzero or superposed Y, the operation still has the same valid unitary contract.

**Derivation.** In the proof, y was arbitrary. The separate output is never a target of C-dagger, so no condition on Y is needed for restoration of W,F. The special case of a prior Y correlated with D follows from the joint coefficients α, not from preparing D and Y independently. In code, a complex product target is a simple test of this broader contract; the reuse experiment below exercises an already correlated retained register.

**Code and verification.** Compare the whole complex state with the ideal XOR action, including both Y amplitudes and the restored auxiliary zeros.

```python
factors=[(.6,.8j),(1,0),(1,0),rw.complex_factors(2)[1]]
v,p=rw.run(cleaned,factors)
torch.testing.assert_close(v,rw.clean_reference(factors),rtol=0,atol=rw.ATOL)
assert rw.leakage(p)<rw.ATOL
print('A complex initial Y is XORed correctly; zero W,F restored independently of its amplitudes')
```

```text
A complex initial Y is XORed correctly; zero W,F restored independently of its amplitudes
```

<span id="formula-code-5-4-inverse"></span>

### 4. Invert the computation, not the retained use

**Formula.** If the chronological used block is C then K, its total matrix is KC. Reversing that entire block yields

$$
(KC)^\dagger(KC)=I,
$$

and therefore restores Y to its original value too. The desired result instead uses $C^\dagger K C$.

**Derivation.** K is self-inverse, so the full inverse first undoes K's output write, then undoes C. In the clean construction, the inverse excludes K. Both are valid unitary inverses; they implement different tasks. In our tested API, `compose` appends to its destination and `adjoint` returns a new inverse program, so build separate destination circuits to keep reusable source C intact. The inverse uses named unitary gates and stays within the precondition established in 5.1.

**Code and verification.** Execute both tasks on the same input. For zero Y and a control with a nonzero one amplitude, the final vectors differ even though both have clean workspace.

```python
factors=[(.6,.8j),(1,0),(1,0),(1,0)]
undo_everything=fq.Circuit(4,dtype=D).compose(used).compose(used.adjoint())
a,pa=rw.run(undo_everything,factors)
b,pb=rw.run(cleaned,factors)
torch.testing.assert_close(a,rw.product_input(factors),rtol=0,atol=rw.ATOL)
torch.testing.assert_close(b,rw.clean_reference(factors),rtol=0,atol=rw.ATOL)
assert not torch.allclose(a,b,rtol=0,atol=rw.ATOL)
print('Full used-block inverse erases the answer; compute-only inverse preserves the XOR answer')
```

```text
Full used-block inverse erases the answer; compute-only inverse preserves the XOR answer
```

<span id="formula-code-5-4-reuse"></span>

### 5. Reuse the same auxiliary pair in a continuous circuit

**Formula.** After copying input d into Y, apply H to D and compute again into a new retained qubit Z, reusing W,F. With initial D amplitudes $\alpha_d$ and both retained outputs zero,

$$
\sum_d\alpha_d|d,0,0,0,0\rangle
\longmapsto\sum_{d,e}\alpha_d H_{ed}|e,0,0,d,e\rangle.
$$

**Derivation.** The first cleaned call maps $|d,0,0,0,0\rangle$ to $|d,0,0,d,0\rangle$. H then changes D but leaves its earlier record d in Y. Thus D and Y are generally correlated. The second cleaned call writes the new D label e into Z and restores W,F again. It acts linearly on this correlated input, exactly the scope proved in unit 2. No intermediate measurement, partial statevector extraction or repreparation is needed.

**Code and verification.** The book helper builds one five-qubit circuit: the two six-gate compute blocks and their native adjoints surround the two output CX gates, with H(D) between calls. Each four-qubit source is placed explicitly on `(0,1,2,3)` and leaves its fourth qubit untouched. Z is q4. The four nonzero output coefficients below are derived directly from H, independently of the detailed C implementation.

```python
factors=[(.6,.8j),(1,0),(1,0),(1,0),(1,0)]
v,p=rw.run(rw.reuse(),factors)
expected=torch.zeros(32,dtype=D)
for d,alpha in enumerate((.6,.8j)):
    for e in (0,1):expected[17*e+2*d]=alpha*(-1 if d==e==1 else 1)/sqrt(2)
torch.testing.assert_close(v,expected,rtol=0,atol=rw.ATOL)
assert rw.leakage(p,5)<rw.ATOL
print('Continuous two-call reuse: W,F zero; old Y record retained while new Z records the H-transformed data')
```

```text
Continuous two-call reuse: W,F zero; old Y record retained while new Z records the H-transformed data
```

<span id="formula-code-5-4-phase"></span>

### 6. A diagonal phase use can also preserve the computed encoding

**Formula.** Instead of copying F, apply a known diagonal operation $V|z\rangle=e^{i\theta(z)}|z\rangle$. Then

$$
C^\dagger V_F C|x,0^r,0^m\rangle
=e^{i\theta(f(x))}|x,0^r,0^m\rangle.
$$

**Derivation.** V multiplies the whole computed image by a scalar determined by f(x); C-dagger can therefore undo that same image while the scalar remains. This is a coherent phase use, not evidence that every possible operation on F permits cleanup. For our single-bit F and V=Z, the effective operation is Z on D because f(d)=d. The computed branch phases γ cancel, while the intended sign $(-1)^d$ survives.

**Code and verification.** All complex coordinates are compared with the explicit data-Z reference. Computational probabilities alone would not detect dropping this intended phase.

```python
factors=[(.6,.8j),(1,0),(1,0),(1,0)]
phase_use=fq.Circuit(4,dtype=D).compose(C).z(2).compose(C.adjoint())
v,p=rw.run(phase_use,factors)
expected=rw.reference(rw.product_input(factors),[('z',0)])
torch.testing.assert_close(v,expected,rtol=0,atol=rw.ATOL)
assert rw.leakage(p)<rw.ATOL
print('C-dagger Z(F) C retains the intended data sign and restores W,F; phase-sensitive check passed')
```

```text
C-dagger Z(F) C retains the intended data sign and restores W,F; phase-sensitive check passed
```

<span id="formula-code-5-4-boundaries"></span>

### 7. Identify when copying disturbs what the inverse needs

**Wrong-input boundary.** The theorem assumes zero W,F. On another subspace, the overall circuit is still unitary, but the stated cleaned-input function need not hold. Our wrong-W witness is returned to W=1, so it is not a reusable zero ancilla. Flipping D between use and inverse changes the F code expected by the inverse; F is then left dirty.

**Why a basis copy is not cloning.** CX on $|\psi\rangle|0\rangle$, with $|\psi\rangle=a|0\rangle+b|1\rangle$, gives $a|00\rangle+b|11\rangle$, not generally $|\psi\rangle|\psi\rangle$. If a unitary copied two states ψ,φ exactly into independent copies, inner-product preservation would require $s=s^2$, where $s=\langle\psi|\phi\rangle$. Taking moduli gives $|s|=0$ or 1. Thus distinct nonorthogonal rays cannot both be copied; orthogonal computational labels can. This is the 4.7 obstruction applied to the copy step of this proof.

**Concrete failed cleanup.** Prepare a computed output plus by H(q0), copy its computational label with CX(q0,q1), and try to undo its preparation by H(q0). The result is

$$
\tfrac12(|00\rangle+|01\rangle+|10\rangle-|11\rangle).
$$

The first qubit has probability one-half of being one, not zero. Copying its basis label changed the coherent output which H-dagger needed. This circuit violates the deterministic orthogonal F-code assumption; it is not a counterexample to the theorem.

**Code and verification.** Execute the two wrong workspace contracts and the non-basis-copy witness, checking predicted failures rather than accepting them as successful cleanups.

```python
v,p=rw.run(rw.block(),rw.basis_factors((0,1,0,0)))
assert abs(rw.leakage(p)-1)<rw.ATOL
factors=rw.basis_factors((0,0,0,0))
v,p=rw.run(rw.block('bad-data'),factors)
torch.testing.assert_close(v,rw.reference(rw.product_input(factors),rw.ops_for('bad-data')),rtol=0,atol=rw.ATOL)
assert rw.probability_one(p,2)>1-rw.ATOL
v,p=rw.run(fq.Circuit(2,dtype=D).h(0).cx(0,1).h(0),rw.basis_factors((0,0)))
torch.testing.assert_close(v,torch.tensor([.5,.5,.5,-.5],dtype=D),rtol=0,atol=rw.ATOL)
assert abs(rw.probability_one(p,0)-.5)<rw.ATOL
print('Wrong blank,changed data and non-basis copying: all predicted cleanup failures observed')
```

```text
Wrong blank,changed data and non-basis copying: all predicted cleanup failures observed
```

<span id="formula-code-5-4-verification"></span>

### 8. Verify the joint auxiliary state and state the cost

**Formula.** If R denotes all retained registers, expand a pure final state as $\sum_{r,a}z_{ra}|r,a\rangle$, with a the combined W,F bit string. Joint leakage is

$$
\ell=\sum_r\sum_{a\ne0}|z_{ra}|^2.
$$

Exactly zero leakage makes every nonzero-a coefficient vanish, proving factorization of the auxiliary zero state as in 5.2. The code sums this joint event directly; multiplying separate marginal probabilities would require an independence assumption and is not the same test. Finite leakage below tolerance is evidence, not an exact factorization certificate. Full-vector comparison additionally checks the retained operation and phase; clean ancillas alone do not prove that the intended answer was preserved.

**Cost and limits.** A compute block of L named logical gates followed by m output CX gates and its reverse uses 2L+m logical gates in this construction and restores r+m temporary qubits. Our L=6,m=1 example uses thirteen gates. This is not a minimum gate count, a depth estimate or a hardware compilation cost. Reuse saves the need to allocate a fresh temporary block for the second evaluation; the earlier retained output must still be kept. Scheduling, other uncomputation strategies and hardware reset have separate contracts.

**Code and verification.** The book guards reject nonfinite or Boolean-valued radian parameters, an undeclared reset stage and malformed scalar-reference vectors. No native reset capability is invented.

```python
rejected=0
for action in (lambda:rw.compute(float('nan')),lambda:rw.compute(True),
               lambda:rw.block('reset'),lambda:rw.reference(torch.zeros(8,dtype=D),[])):
    try:action()
    except ValueError:rejected+=1
assert rejected==4 and rw.RUNS==11
print('4 malformed contracts rejected;11actual body circuits; clean-subspace proof and finite tolerance kept distinct')
```

```text
4 malformed contracts rejected;11actual body circuits; clean-subspace proof and finite tolerance kept distinct
```

### Run the complete example

```bash
python examples/foundations/reusable_workspace.py
python scripts/check_reusable_workspace_prose.py
```

The complete program runs **127 actual circuits**. Fifty-one runs check compute/use/clean on every four-qubit basis input and one complex product, including the action outside the clean subspace. Twenty more check the clean-input contract with arbitrary Y and additional zero/full-turn angle cases. Thirty-four check continuous reuse on every five-qubit basis state, a complex full-register product and a separately derived clean-input coherent result. Eighteen check the phase use, and four check wrong inputs, changed data, undoing the entire use and copying a non-basis output. Seven malformed helper contracts are rejected. These full-vector checks use independently specified scalar bit/rotation references and simple ideal-operation or analytic coefficient checks. No state is phase-aligned to force agreement.

The eight cumulative body fragments run eleven circuits, with exact expected stdout comparison. The separate transfer described in the exercises uses three new compute angles and a different between-call rotation. The general theorem establishes the clean-subspace guarantee; finite examples test the released implementation rather than proving that guarantee for every possible program.

Expected output of the complete program:

```text
Compute/use/clean:51full-register basis/complex runs;20valid-workspace and angle-boundary runs passed.
Reuse:33full-register tests plus1zero-workspace complex analytic check;retained first output and second computation coherent.
Phase use:18circuits;C-dagger Z(F) C equals Z(data) on clean-input subspace,with workspace restored.
4boundary circuits:wrong blank,changed data,whole-used inverse andnonorthogonal-copy failure checked.
127actual CPUcomplex128 circuits;7invalid contracts rejected;atol1e-12,rtol0,no phase alignment.
Clean subspace and numerical leakage distinguished;no reset,noise,hardware or resource-optimality claim.
```

### Understanding checks and transfer exercises

**5.4-A — New reuse experiment.** Change the compute angles to (−0.29,0.61,−1.03) radians and replace the between-call H by Ry(0.31). Allow arbitrary initial Y,Z. Derive the final state with W,F initially zero, and verify it independently of the detailed C sequence.

**5.4-B — What must remain unchanged?** Why can CX from F into Y preserve the inverse's input even when W is a complex superposition? Why does a generic unitary on F not have the same guarantee? Explain the diagonal phase exception.

**5.4-C — Exact versus numerical reuse.** Does small joint leakage prove that the retained operation is correct? Can the joint zero-state probability be obtained by multiplying separate zero-state marginal probabilities without further assumptions?

**5.4-D — Source and destination.** Which source block should be inverted to keep the answer? What does restoring a wrong initial workspace value demonstrate, and what does it fail to demonstrate?

<details markdown="1">
<summary>Answers and reasoning</summary>

**A.** For initial coefficients $\alpha_{dyz}$ on D,Y,Z, the final state is

$$
\sum_{d,y,z,e}\alpha_{dyz}[R_y(0.31)]_{ed}
|e,0,0,y\oplus d,z\oplus e\rangle.
$$

The first call XORs d into Y; the intervening rotation contributes its matrix entry; the second call XORs e into Z. Both calls restore W,F, irrespective of the changed compute angles, provided the orthogonal output contract still holds. The separate author transfer runs eight D,Y,Z basis inputs and one complex product in a continuous five-qubit circuit, then one additional phase-use circuit: ten actual executions. Its scalar reference uses explicit sine/cosine Ry entries and bitwise output indices, not the helper's compute gate list. It compares full complex coordinates without phase alignment.

**B.** For fixed x, every W component accompanies the same basis code f(x), so the output write is the same on all those components and changes none of D,W,F. A generic F rotation can mix different code values or correlate Y with newly changed F components; C-dagger then need not see its original computed image. A diagonal F operation only multiplies that image by a scalar, which passes through the linear inverse and remains as the intended data phase.

**C.** No. A full used-block inverse is a counterexample: it cleans auxiliaries but erases the answer. Check the retained statevector and phase against the intended operation as well. Joint probability requires a joint event; multiplying marginals assumes independence. An exactly zero leakage gives the pure-state factorization theorem; a computed inequality at finite tolerance is a numerical check rather than an exact proof.

**D.** Invert C on D,W,F, leaving K's retained Y write intact. Inverting KC restores all registers to their input, including Y. Returning a wrong workspace input to its original value can demonstrate reversibility on that input; it does not establish the specified zero-workspace function or availability of a clean reusable ancilla.

</details>

### Sources, depth and next step

Depth **F**: the compute-copy-uncompute statement tracks every register, extends to arbitrary joint D,Y coefficients, permits complex workspace and branch phases, and explains why orthogonal basis encoding permits a nondisturbing copy while generic unknown-state cloning fails. The clean-workspace and retained-output obligations are checked separately. Assigned background: Nielsen and Chuang, 10th Anniversary Edition (2010), §3.2.5. No fresh inspection of the user-local PDF is claimed. Released FlagQuantum source/signatures and actual executions support the named gates, placement, composition and native unitary adjoints; no new compiler, reset or state-preparation API is invented.

The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/5.4.json) records author execution, exact body/full outputs and the new-angle transfer. This remains a working draft: independent mathematical and implementation reviews and reader trials are pending. No physical reset, noise, shots, hardware execution, numerical error certificate or resource-optimal scheduling is claimed. Continue with [5.5 Universal gate sets](#sec-gates-reversible-computation-and-circuit-synthesis-5).


<span id="sec-gates-reversible-computation-and-circuit-synthesis-5"></span>

## 5.5 Universal gate sets

A gate set is useful because compositions can express operations beyond the gates originally listed. To prove universality, we need a route from an arbitrary target unitary to a finite allowed circuit. Recognizing a few familiar circuits is not enough. This section gives a constructive route, retaining ordered basis labels and full phases at every step.

Prerequisites are [3.6](ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-6), for phase-tracked single-qubit factorization, and [5.2](#sec-gates-reversible-computation-and-circuit-synthesis-2), for coherent controlled operations. We use column vectors, left matrix action and q0 as the most significant basis bit. Eight cumulative units pair the proof steps with executable calculations. The full program is [universal_gates.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/universal_gates.py), running released FlagQuantum 0.3.1 and PyTorch 2.13.0 on CPU with complex128 statevectors. Mathematical exactness and floating-point verification are stated separately.

<span id="formula-code-5-5-statement"></span>

### 1. State exactly which universal set is being proved

**Theorem.** On any finite register of n≥1 qubits, every unitary $U\in U(2^n)$ is a finite product of arbitrary continuous one-qubit $U(2)$ gates and CNOT gates between any distinct ordered pair of logical qubits. No auxiliary qubit is required by the construction below. The theorem permits exact real parameters and full one-qubit phases. It is an exact continuous-set existence statement, not a claim about a fixed finite gate alphabet or an efficient hardware compiler.

**Proof plan.** Reduce U to diagonal form by two-level row operations; realize each two-level unitary on two arbitrary basis labels using a Gray path; realize the required multiply controlled one-qubit gate recursively; terminate the recursion with a one-control construction from one-qubit gates and CNOT. Each reduction is established below. This fills the logical gap between saying that two-level matrices suffice and actually constructing them from the allowed gates.

**One-qubit starting point.** Section 3.6 supplies phase-tracked ZYZ factorization:

$$
U=e^{i\alpha}R_z(\beta)R_y(\gamma)R_z(\delta).
$$

The chronological calls are δ rotation, γ rotation, β rotation, followed by the scalar phase. This section's elementary gate list may store a one-qubit matrix directly: arbitrary one-qubit unitaries are precisely the continuous set in the theorem. The retained α becomes essential when a gate is controlled.

**Code.** Imports are cumulative; run from the repository root in the pinned CPU complex128 environment. The numerical teaching compiler is a book helper with a one-to-three-qubit resource guard, not a FlagQuantum compiler API. Every emitted instruction is checked: a one-qubit gate or a named two-qubit CX, with no multi-qubit matrix instruction. The runner uses actual FlagQuantum statevector execution and checks returned probabilities and precision.

```python
import sys,cmath,torch
sys.path.insert(0,'.')
import flagquantum as fq
from math import sqrt
from examples.foundations import universal_gates as ug
D=ug.D
U1=ug.fixture(2,71)
alpha,beta,gamma,delta=ug.zyz(U1)
rebuilt=cmath.exp(1j*alpha)*ug.explicit('z',beta)@ug.explicit('y',gamma)@ug.explicit('z',delta)
factors=ug.complex_factors(1)
v,p=ug.run(ug.one(0,rebuilt),1,factors)
torch.testing.assert_close(v,U1@ug.product_input(factors),rtol=0,atol=ug.ATOL)
print('Continuous one-qubit base case: phase-tracked ZYZ reconstructs the full complex action')
```

```text
Continuous one-qubit base case: phase-tracked ZYZ reconstructs the full complex action
```

<span id="formula-code-5-5-elimination"></span>

### 2. Reduce an arbitrary unitary to two-level matrices

**Formula.** A two-level matrix acts as a chosen 2×2 unitary G on the ordered basis pair (p,q), and as identity on every other basis vector. For complex entries a,b in rows p,q of one column, let $r=(|a|^2+|b|^2)^{1/2}$. If r>0, choose

$$
G=\frac1r\begin{pmatrix}\overline a&\overline b\\-b&a\end{pmatrix},
\qquad G\begin{pmatrix}a\\b\end{pmatrix}=\begin{pmatrix}r\\0\end{pmatrix}.
$$

**Proof.** The displayed product is $(|a|^2+|b|^2,-ba+ab)^T/r$. Its two rows have norm one and inner product zero, giving $GG^\dagger=I$; the reverse product follows directly as well. If b=0 no elimination is needed, including r=0. Start at column zero and eliminate its entries from bottom to top using adjacent rows (row−1,row). Continue with the next column. For an earlier column, both rows now being mixed lie below its diagonal and have zero entries, so their mixing preserves that earlier elimination. The finite procedure uses at most $N(N-1)/2$ two-level operations for N=2^n.

Let their chronological row-operation matrices be $E_1,\ldots,E_L$. The result $D=E_L\cdots E_1U$ is upper triangular and unitary. Its first column has only its diagonal entry, whose modulus is one. Orthogonality with that column forces every other entry in the first row to vanish. Removing that row and column leaves an upper-triangular unitary; induction proves D is diagonal with unit-modulus entries. Therefore

$$
U=E_1^\dagger E_2^\dagger\cdots E_L^\dagger D.
$$

**Code and verification.** This reduction is classical matrix algebra, before constructing a quantum circuit. Rebuild a four-dimensional target from the recorded local factors and diagonal, checking every complex matrix entry. The code chooses unit phases from the computed diagonal and checks its residual; that finite-precision step is not a proof of exact arithmetic.

```python
U4=ug.fixture(4,73)
records,diagonal=ug.elimination(U4)
restored=diagonal.clone()
for a,b,G in reversed(records):
    torch.testing.assert_close(G.mH@G,torch.eye(2,dtype=D),rtol=0,atol=1e-11)
    restored=ug.embedded_two(G.mH,a,b,2)@restored
torch.testing.assert_close(restored,U4,rtol=0,atol=1e-11)
assert len(records)<=6
print('4x4 row elimination: unitary two-level factors and diagonal reconstruct the complete target matrix')
```

```text
4x4 row elimination: unitary two-level factors and diagonal reconstruct the complete target matrix
```

<span id="formula-code-5-5-controlled"></span>

### 3. Build a one-control unitary from two CNOT gates

**Formulas.** For the full ZYZ representation above, define

$$
\begin{aligned}
A&=R_z(\beta)R_y(\gamma/2),\\
B&=R_y(-\gamma/2)R_z[-(\delta+\beta)/2],\\
C&=R_z[(\delta-\beta)/2],\qquad P_\alpha=\operatorname{diag}(1,e^{i\alpha}).
\end{aligned}
$$

Then $ABC=I$ and $AXBXC=R_z(\beta)R_y(\gamma)R_z(\delta)$. Chronologically apply C on target, CX, B on target, CX, A on target, and $P_\alpha$ on control.

**Proof.** In ABC the opposite Ry half-angles cancel, while the Rz angles sum to zero. For the second identity use $XR_y(\theta)X=R_y(-\theta)$ and $XR_z(\theta)X=R_z(-\theta)$, established from the Pauli matrices in 3.5. Moving the two X factors through the middle rotations gives

$$
AXBXC=R_z(\beta)R_y(\gamma/2)R_y(\gamma/2)
R_z[(\delta+\beta)/2]R_z[(\delta-\beta)/2].
$$

The adjacent rotations combine to the claimed product. With control zero, both CX act as I and the target sees ABC=I. With control one, it sees AXBXC and gains the missing scalar $e^{i\alpha}$ from the control phase. Thus the circuit implements the full $C(U)$, not merely a phase-equivalent target. Control superpositions follow by linearity, with no measurement.

**Code and verification.** The helper emits the six allowed instructions just derived. The reference embeds U into the control-one basis pair (10,11).

```python
target=ug.fixture(2,75)
ops=ug.controlled_one(target,0,1)
factors=ug.complex_factors(2)
v,p=ug.run(ops,2,factors)
expected=ug.embedded_two(target,2,3,2)@ug.product_input(factors)
torch.testing.assert_close(v,expected,rtol=0,atol=ug.ATOL)
assert sum(g[0]=='cx' for g in ops)==2
print('Controlled U: two CNOTs and one-qubit gates reproduce both complex branches including target global phase')
```

```text
Controlled U: two CNOTs and one-qubit gates reproduce both complex branches including target global phase
```

<span id="formula-code-5-5-multiple"></span>

### 4. Remove extra controls by a terminating recursion

**Construction.** Suppose U acts on one target and has k≥2 positive controls. Separate the last control b from the other k−1 controls A. Let a denote the Boolean AND of A's basis values; a is notation for a condition, not an allocated qubit. Choose a unitary square root V with $V^2=U$. Such a root exists: unitary U has an orthonormal eigenbasis, and taking half of each eigenvalue phase gives a unitary V.

Apply, chronologically: controlled-V from b to target; X on b controlled by all of A; controlled-V-dagger from b to target; the same controlled X on b; then V on target controlled by all of A.

**Proof.** Controls A never change and b is toggled twice, hence restored. On a fixed control branch the target receives powers of the same V, so they commute. Its total exponent is

$$
b-(b\oplus a)+a=2ab.
$$

For a=0 it is zero; for a=1 it is 2b. Thus the target receives U precisely when all k controls are one, and identity otherwise. Linearity proves the coherent action. The two controlled-X operations and final controlled-V operation have k−1 controls, while the two other controlled operations have one. Recursion therefore terminates at unit 3, or at an uncontrolled one-qubit gate. It requires no ancilla and preserves every control, without assuming that a Boolean AND can be overwritten for free.

**Code and verification.** The numerical root helper orthonormalizes computed eigenvectors and explicitly checks both unitarity and V²≈U. Those checks validate the floating-point fixture; the spectral argument proves root existence. Compare a two-control implementation against the full ordered pair (110,111).

```python
ops=ug.multi(target,(0,1),2)
factors=ug.complex_factors(3)
v,p=ug.run(ops,3,factors)
expected=ug.embedded_two(target,6,7,3)@ug.product_input(factors)
torch.testing.assert_close(v,expected,rtol=0,atol=ug.ATOL)
print('Two controls reduced recursively to one-qubit gates and CNOT; all complex branch amplitudes match')
```

```text
Two controls reduced recursively to one-qubit gates and CNOT; all complex branch amplitudes match
```

<span id="formula-code-5-5-gray"></span>

### 5. Realize a two-level unitary on arbitrary basis labels

**Construction.** For distinct n-bit labels a,b, form a simple Gray path $g_0=a,g_1,\ldots,g_h=b$ by flipping each differing bit once. Adjacent path states differ in one target bit. Swapping exactly such a pair is a multi-controlled X on that bit, conditioned on all other bits matching their common pattern. A zero-valued control is handled by X before and after the positive-control construction.

Use adjacent swaps from $g_0$ through $g_{h-1}$, leaving b unchanged. Their product P maps a to $g_{h-1}$ and b to b. On that now-adjacent ordered pair apply the desired local U, using the common control pattern. Undo the swaps in reverse order. The full matrix is

$$
P^\dagger K P,
$$

and acts as U on the original ordered pair (a,b), leaving every other basis vector fixed.

**Proof.** P is a basis permutation; conjugation transports the support of K back to (a,b). No intermediate swap touches b because the path has no repeated vertices and stops one edge before b. The adjacent pair's target bit may be one in its *first* label. The physical target matrix has local order zero,one, so in this case use XUX; otherwise use U. This preserves the declared ordered pair rather than silently reversing its rows and columns. All control patterns are realized by the positive-control recursion and one-qubit X conjugations, so every operation ultimately uses only the allowed gates.

**Code and verification.** Use the deliberately reversed pair (111,000). The helper's path is 111→011→001→000, so two swaps precede the adjacent operation and two follow it. The full complex reference also verifies that untouched amplitudes remain unchanged.

```python
ops=ug.two_level(target,7,0,3)
factors=ug.complex_factors(3)
v,p=ug.run(ops,3,factors)
expected=ug.embedded_two(target,7,0,3)@ug.product_input(factors)
torch.testing.assert_close(v,expected,rtol=0,atol=ug.ATOL)
assert all(g[0] in ('one','cx') for g in ops)
print('Ordered pair(111,000): Gray swaps,negative controls and local XUX orientation reproduce the full two-level action')
```

```text
Ordered pair(111,000): Gray swaps,negative controls and local XUX orientation reproduce the full two-level action
```

<span id="formula-code-5-5-assembly"></span>

### 6. Assemble the diagonal and inverse factors in chronological order

**Formula.** Write $D=\operatorname{diag}(d_0,\ldots,d_{N-1})$ with unit-modulus entries. For each j>0 apply the two-level diagonal diag(1,d_j) on ordered pair (0,j); also apply diag(d_0,1) on (0,1). Their product is D: the first basis amplitude gets d0, and each other amplitude gets its own d_j. These diagonal factors commute; none of the phases is discarded.

From unit 2, $U=E_1^\dagger\cdots E_L^\dagger D$. Therefore the chronological gate calls are the diagonal factors, then $E_L^\dagger,\ldots,E_1^\dagger$. Each two-level factor now has an allowed-gate implementation by units 3–5. This proves the theorem in unit 1 for every finite n: the elimination, finite Gray paths and decreasing-control recursion all terminate.

**Code and verification.** Compile the four-dimensional fixture from unit 2 and run every basis state plus a complex product. Compare actual statevectors directly with U times the input, without phase alignment. `compile_unitary` is this explicit book construction; it does not call a native FlagQuantum compilation service.

```python
compiled=ug.compile_unitary(U4)
for factors in [ug.basis_factors(bits) for bits in ((0,0),(0,1),(1,0),(1,1))]+[ug.complex_factors(2)]:
    v,p=ug.run(compiled,2,factors)
    torch.testing.assert_close(v,U4@ug.product_input(factors),rtol=0,atol=ug.ATOL)
assert all(len(i.wires)==1 or (len(i.wires)==2 and i.name=='cx') for i in ug.circuit(compiled,2).to_ir().instructions)
print('General4x4 unitary: all4basis columns and a complex input agree; emitted gates are one-qubit or CX only')
```

```text
General4x4 unitary: all4basis columns and a complex input agree; emitted gates are one-qubit or CX only
```

<span id="formula-code-5-5-validation"></span>

### 7. Test the whole reduction beyond a single two-level example

**Validation target.** A generic three-qubit unitary has eight input basis columns. The full example checks every column and a complex product of a deterministically generated dense fixture. This exercises multiple eliminated columns, diagonal phases, nonadjacent ordered pairs, negative controls and recursive controls together. The numerical target matrix is a classical reference; it is never submitted as a multi-qubit matrix gate in the compiled circuit.

**Code and verification.** The body executes a complex input as a compact visible example. The full program additionally tests its eight basis inputs. The circuit contains 2,438 elementary logical instructions for this construction, illustrating why an existence proof is not an efficiency claim. The preparation helper also uses only one-qubit matrices; it introduces no hidden multi-qubit target gate.

```python
U8=ug.fixture(8,65)
compiled8=ug.compile_unitary(U8)
factors=ug.complex_factors(3)
v,p=ug.run(compiled8,3,factors)
torch.testing.assert_close(v,U8@ug.product_input(factors),rtol=0,atol=ug.ATOL)
assert len(compiled8)==2438
print('General8x8 unitary:2438one-qubit/CX instructions reproduce the complex target action')
```

```text
General8x8 unitary:2438one-qubit/CX instructions reproduce the complex target action
```

<span id="formula-code-5-5-scope"></span>

### 8. Separate phase, finite precision and finite gate alphabets

**Phase check.** Although I and −I have the same isolated target probabilities, their controlled versions differ: on plus control and zero target, a final H on control yields 00 for C(I) and 10 for C(−I). The decomposition must preserve this distinction. This test also probes ZYZ endpoint branches and exact target phase conventions.

**Exact theorem versus numerical checks.** The proof uses exact continuous gates and exact row operations. The code performs complex128 arithmetic, tests unitarity/root/reconstruction residuals, and uses phase-based diagonal entries after checking the row-elimination residual. Near ZYZ endpoints it uses a stated small numerical branch threshold. It does not provide an interval error certificate or exact symbolic output. Full-vector comparisons use absolute tolerance $10^{-9}$, relative tolerance zero, across the tested circuits; no phase alignment, backend fallback or approximate simulator mode is enabled. The looser comparison than the short-gate examples accounts for long gate products and multiple floating-point matrix factorizations; it is a declared finite test threshold, not a general error bound.

**Finite alphabet boundary.** A fixed finite gate alphabet has only countably many finite words, whereas even single-qubit unitaries modulo global phase form an uncountable family. Hence no such alphabet exactly realizes every unitary with a finite word. Approximate universality concerns whether its closure is dense under a specified metric and precision target; it requires a separate theorem and synthesis analysis. This section proves neither that a particular finite alphabet is approximately universal nor a gate-count bound for approximating arbitrary gates.

**Resource boundaries.** The proof permits any finite n but offers no efficient compilation guarantee. The numerical helper explicitly restricts general targets to one–three qubits, rejects nonunitaries rather than projecting the input onto a unitary, and requires valid ordered supports. The guard is a teaching resource choice, not a FlagQuantum qubit limit. CNOT connectivity is unrestricted at the logical level; physical routing and native-gate costs need additional compilation.

**Code and verification.** Both analyzers below use the constructed one-control gate, not a native controlled-unitary API.

```python
for sign,index in ((1,0),(-1,2)):
    ops=ug.controlled_one(sign*ug.I,0,1)+ug.one(0,torch.tensor([[1,1],[1,-1]],dtype=D)/sqrt(2))
    v,p=ug.run(ops,2,[(1/sqrt(2),1/sqrt(2)),(1,0)])
    expected=torch.zeros(4,dtype=D);expected[index]=1
    torch.testing.assert_close(v,expected,rtol=0,atol=ug.ATOL)
assert ug.RUNS==12
print('Constructed C(I) andC(-I) remain distinguishable: analyzer outputs00 and10;12actual body circuits')
```

```text
Constructed C(I) andC(-I) remain distinguishable: analyzer outputs00 and10;12actual body circuits
```

### Run the complete example

```bash
python examples/foundations/universal_gates.py
python scripts/check_universal_gates_prose.py
```

The complete program runs **106 actual circuits**. Twenty-five runs check five one-control targets on all basis inputs and a complex product, including I, −I, X and full complex phase. Eighteen check two double-control targets. Thirty-six check four ordered three-qubit two-level pairs, including reverse orientation and nonadjacent basis labels. Seventeen check generic targets of dimensions two, four and eight on all basis columns and a complex product; the classical row-elimination factors are independently reconstructed before synthesis. Ten further runs check identity and a nontrivial global-phase identity. Seven invalid helper contracts are rejected. Every emitted circuit is inspected to contain only one-qubit gates and named CX gates.

The eight cumulative body fragments run twelve additional circuits and compare their printed output exactly. A separate new-target transfer runs six circuits as described below. These tests cover full complex coordinates and preserve global phase; finite fixtures are implementation evidence, not a replacement for the exact finite constructive proof.

Expected output of the complete program:

```text
5single-control targets includingI,-I,X,complex phase:allbasis andcomplex inputs passed.
2double-control targets:recursive square-root construction checked on all8basis andcomplex input.
4ordered two-level pairs:Gray paths,negative controls and reversed target orientation checked.
2x2dense unitary:QR reconstruction andallowed-gate circuit passed;3logical gates.
4x4dense unitary:QR reconstruction andallowed-gate circuit passed;108logical gates.
8x8dense unitary:QR reconstruction andallowed-gate circuit passed;2438logical gates.
Identity/global-phase cases and7invalid contracts checked;106actual CPUcomplex128 circuits.
Numerical fullvector atol1e-9,rtol0;no phasealignment,no native multi-qubit matrix gate or ancilla.
Constructive existence only;1-3qubit memory guard,not an efficientcompiler or finite-alphabet synthesis claim.
```

### Understanding checks and transfer exercises

**5.5-A — New target transfer.** Generate a new four-dimensional unitary with the pinned fixture seed 77, compile it, and compare all basis columns plus a complex product. Separately use a new 2×2 target from seed 79 on ordered pair (010,111). Which gates can be emitted, and which complete matrix is the reference?

**5.5-B — Recursion without a hidden ancilla.** In unit 4, a is the AND of k−1 basis values. Where is a stored physically? Evaluate $b-(b\oplus a)+a$ on all four Boolean pairs and explain why b is restored.

**5.5-C — Ordered support and matrix order.** Why is XUX needed when the first adjacent label has target bit one? Why are the inverse row factors emitted in reverse chronological order after D?

**5.5-D — Exact and approximate universality.** Why does the theorem not imply exact finite-word synthesis from a finite alphabet? Does checking a finite list of matrices establish that a gate set is dense, or certify an error bound for all targets?

<details markdown="1">
<summary>Answers and reasoning</summary>

**A.** Only arbitrary one-qubit matrices and named CNOT gates may appear; a single native multi-qubit target matrix would bypass the reduction being tested. Compare the compiled statevector with the original dense U times the same input. For the ordered-pair transfer compare with the identity matrix whose (2,7) rows/columns are replaced by the local 2×2 target in that order. The separate author transfer performs four basis and one complex execution for the new dense target, then one complex ordered-pair execution: six actual circuits. The reference matrices are the inputs to synthesis, not reconstructed from the emitted instruction list. This is an author transfer, not independent-agent review.

**B.** It is not stored in an auxiliary register; it is a condition used to analyze a computational-basis branch. For (a,b)=(0,0),(0,1),(1,0),(1,1), the exponent is respectively 0,0,0,2. The two controlled X operations both toggle b by a, giving $b\oplus a\oplus a=b$. Lower-control implementations replace these conditional operations recursively; the argument does not assume an unavailable multi-control primitive.

**C.** The local matrix API orders its target bit as zero,one. Reversing that local coordinate order uses the permutation X, so $M_{\mathrm{local}}=XUX$ realizes U in ordered coordinates one,zero. Likewise, $D=E_L\cdots E_1U$ implies $U=E_1^\dagger\cdots E_L^\dagger D$; rightmost factors act first, so chronological calls begin with D and then $E_L^\dagger$ through $E_1^\dagger$. These are coordinate/order requirements, not optional phase conventions.

**D.** The available one-qubit gates here form an uncountable continuous family. A finite alphabet has only countably many finite words, so exact representation of every member of an uncountable unitary family is impossible. A countable set can nevertheless have dense closure; density and quantitative approximation require their own proofs. Neither finitely many passing fixtures nor this continuous-set theorem proves a discrete-alphabet density theorem or a certified numerical error bound.

</details>

### Sources, depth and next step

Depth **F**: the two-level row-elimination proof, upper-triangular unitary diagonalization, full diagonal phase assembly, one-control ABC construction, unitary-root control recursion, Gray-path reduction and ordered-target orientation together establish continuous one-qubit/CNOT universality. Numerical endpoint decisions, root and diagonal residuals are explicitly separated from that exact proof. Assigned background: Nielsen and Chuang, 10th Anniversary Edition (2010), §§4.5.1–4.5.2, with 3.6's phase-tracked factorization as the local prerequisite. No fresh inspection of the user-local PDF is claimed. Installed released FlagQuantum unitary/CX instruction semantics and actual execution were checked; the teaching compiler is original repository code, not a claimed native API.

The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/5.5.json) records author execution, actual body/full outputs and the new-target transfer. Independent mathematical review, implementation review and reader trials are pending; this remains a working draft. No ancilla, approximate simulator, hardware routing, efficient general compilation or finite-alphabet universality theorem was used or claimed. Continue, when drafted, with [5.6 Decomposing controlled and multi-qubit gates](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-6).
