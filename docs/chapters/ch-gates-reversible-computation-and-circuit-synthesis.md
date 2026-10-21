# 5. Gates, Reversible Computation, and Circuit Synthesis

**Working drafts: sections 5.1–5.8 · Writing Baseline 1.0 · October 22, 2026.** Author execution is separate from independent mathematical, implementation and reader review, which remain pending. Examples use installed released FlagQuantum 0.3.1 and PyTorch 2.13.0 on CPU with complex128 statevectors.

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

**Construction.** Suppose U acts on one target and has k≥2 positive controls. Separate the last control b from the other k−1 controls A. Let a denote the Boolean AND of A's basis values; a is notation for a condition, not an allocated qubit. Choose a unitary square root V with $V^2=U$. Only the 2×2 case is needed. Its quadratic characteristic polynomial has a complex root λ, hence a normalized eigenvector v. Since U preserves norms, $|\lambda|=1$ and $U^\dagger v=\overline\lambda v$. For any w orthogonal to v,

$$
\langle v,Uw\rangle=\langle U^\dagger v,w\rangle
=\lambda\langle v,w\rangle=0.
$$

Thus the one-dimensional orthogonal complement is invariant. Choosing a unit w there gives $Uw=\mu w$ with $|\mu|=1$, again by norm preservation. The columns v,w form a unitary Q, so for real eigenvalue phases θ1,θ2,

$$
U=Q\operatorname{diag}(e^{i\theta_1},e^{i\theta_2})Q^\dagger,\qquad
V=Q\operatorname{diag}(e^{i\theta_1/2},e^{i\theta_2/2})Q^\dagger.
$$

Direct multiplication gives $V^\dagger V=I$ and $V^2=U$. This proof includes repeated eigenvalues and retains the target's full phase; no particular root branch or root uniqueness is required.

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

The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/5.5.json) records author execution, actual body/full outputs and the new-target transfer. Independent mathematical review, implementation review and reader trials are pending; this remains a working draft. No ancilla, approximate simulator, hardware routing, efficient general compilation or finite-alphabet universality theorem was used or claimed. Continue with [5.6 Decomposing controlled and multi-qubit gates](#sec-gates-reversible-computation-and-circuit-synthesis-6).

<span id="sec-gates-reversible-computation-and-circuit-synthesis-6"></span>

## 5.6 Decomposing controlled and multi-qubit gates

A native multi-qubit instruction can hide both its elementary cost and its phase convention. Here we derive selected exact replacements and check the complete complex output, rather than accepting a matching truth table. The prerequisites are [5.2](#sec-gates-reversible-computation-and-circuit-synthesis-2), for coherent controls, and [5.4](#sec-gates-reversible-computation-and-circuit-synthesis-4), for workspace contracts. The constructive universality result of 5.5 provides context; this section proves its displayed identities directly rather than repeating general synthesis.

Assume fixed ideal unitary circuits, computational basis ordered as $|q_0q_1\cdots q_{n-1}\rangle$, distinct declared support positions, and unrestricted logical CNOT pairs. Test preparations lie outside the decomposed block. All numerical examples use released FlagQuantum 0.3.1/PyTorch 2.13.0, CPU complex128, absolute tolerance $10^{-12}$ and relative tolerance zero, without phase alignment, normalization repair, approximate simulation or fallback. The algebraic proofs are exact; floating-point tests do not certify an interval error bound.

<span id="formula-code-5-6-rotations"></span>

### 1. Controlled rotations without a phase shortcut

**Formula.** Angles are dimensionless radians. For $j=y,z$, define $R_j(\theta)=\exp(-i\theta\sigma_j/2)$ and let $C R_j$ apply this rotation only when control qubit $c$ is one. Chronological calls are

$$
R_j(\theta/2)_t,\quad CX_{c,t},\quad
R_j(-\theta/2)_t,\quad CX_{c,t}.
$$

**Derivation.** Since $X\sigma_yX=-\sigma_y$ and $X\sigma_zX=-\sigma_z$, conjugating each power in the exponential series gives $XR_j(s)X=R_j(-s)$. On control zero the two rotations multiply to identity. On control one, rightmost-first matrix multiplication gives

$$
X R_j(-\theta/2)X R_j(\theta/2)
=R_j(\theta/2)R_j(\theta/2)=R_j(\theta).
$$

These two control subspaces span the register, proving the full operator identity, including a superposed control and an input entangled with other qubits. This particular identity is not an $R_x$ identity: X commutes with $R_x$, and the same sequence would cancel. At $\theta=2\pi$, $R_z(2\pi)=-I$, so the controlled operation is Z on the control, not identity. Reducing this angle modulo $2\pi$ would discard a measurable branch phase.

**FlagQuantum code → verification result.** The imported functions are original book helpers that emit released named gates, not native decomposition APIs. `run` uses the checked state preparation and execution contract of 5.1. The independent reference contracts scalar target indices; it does not reuse the emitted gate list. All snippets below are cumulative and run from the repository root.

```python
import math
import torch
import flagquantum as fq
import examples.foundations.gate_decompositions as g
f = g.complex_factors(2)
theta = .73
block = fq.Circuit(2, dtype=g.D).ry(1, theta/2).cx(0, 1).ry(1, -theta/2).cx(0, 1)
v, _ = g.run(block, f)
reference = g.controlled_reference(g.product_input(f), g.explicit('y', .73), 2, 0, 1)
torch.testing.assert_close(v, reference, rtol=0, atol=g.ATOL)
v, _ = g.run(g.controlled_rotation('z', 2*math.pi), f)
reference = g.product_input(f).clone(); reference[2:] *= -1
torch.testing.assert_close(v, reference, rtol=0, atol=g.ATOL)
print('Controlled Ry(.73) and CRz(2*pi): full complex references passed.')
```
```text
Controlled Ry(.73) and CRz(2*pi): full complex references passed.
```

<span id="formula-code-5-6-phase"></span>

### 2. Compensate the phase of a controlled phase gate

**Formula.** With $P(\phi)=\operatorname{diag}(1,e^{i\phi})$,

$$
P(\phi)=e^{i\phi/2}R_z(\phi),\qquad
CP(\phi)=P_c(\phi/2)\,CR_z(\phi).
$$

**Derivation.** On control zero both factors act as identity. On control one the additional scalar $e^{i\phi/2}$ turns $\operatorname{diag}(e^{-i\phi/2},e^{i\phi/2})$ into $\operatorname{diag}(1,e^{i\phi})$. The compensation is on the **control**, even though the original phase gate targets t. Thus $CP(2\pi)=I$, while the uncompensated $CR_z(2\pi)$ is Z on the control. At a general angle these two circuits have equal computational-basis probabilities for every input, but unequal relative phases across the control branches.

**FlagQuantum code → verification result.** The correct reference is $\operatorname{diag}(1,1,1,e^{i\phi})$ in order $|q_0q_1\rangle$. The test deliberately checks the wrong candidate too; agreement of probabilities does not accept that candidate.

```python
phi = -.63
phase_block = g.controlled_rotation('z', phi).p(0, phi/2)
correct, probabilities = g.run(phase_block, f)
wrong, wrong_probabilities = g.run(g.controlled_rotation('z', phi), f)
reference = g.product_input(f).clone()
reference[3] *= torch.exp(torch.tensor(1j*phi, dtype=g.D))
torch.testing.assert_close(correct, reference, rtol=0, atol=g.ATOL)
torch.testing.assert_close(probabilities, wrong_probabilities, rtol=0, atol=g.ATOL)
assert not torch.allclose(correct, wrong, rtol=0, atol=g.ATOL)
print('Compensated CP matches all amplitudes; uncompensated CRz only matches probabilities.')
```
```text
Compensated CP matches all amplitudes; uncompensated CRz only matches probabilities.
```

<span id="formula-code-5-6-cz-swap"></span>

### 3. Reduce CZ and SWAP to single-qubit gates and CNOT

**Formula.** With chronological lists in parentheses,

$$
CZ_{a,b}=(H_b,CX_{a,b},H_b),\qquad
\operatorname{SWAP}_{a,b}=(CX_{a,b},CX_{b,a},CX_{a,b}).
$$

**Derivation.** For CZ, control zero gives $HH=I$ and control one gives $HXH=Z$. For SWAP, let initial basis bits be $(a,b)$. The three updates are

$$
(a,b)\longmapsto(a,b\oplus a)
\longmapsto(b,b\oplus a)\longmapsto(b,a).
$$

There is no branch phase in either construction. Therefore equality on all basis vectors extends by linearity to all complex vectors. The SWAP is an active quantum operation; it is not a passive index permutation or a label rename (see [4.5](ch-composite-systems-tensor-products-and-qubit-ordering.md#sec-composite-systems-tensor-products-and-qubit-ordering-5)).

**FlagQuantum code → verification result.** These helpers emit only H/CX or CX. The complete program additionally compares each construction with the released native CZ/SWAP on every basis input.

```python
initial = g.product_input(f)
v, _ = g.run(fq.Circuit(2, dtype=g.D).h(1).cx(0, 1).h(1), f)
reference = initial.clone(); reference[3] *= -1
torch.testing.assert_close(v, reference, rtol=0, atol=g.ATOL)
v, _ = g.run(fq.Circuit(2, dtype=g.D).cx(0, 1).cx(1, 0).cx(0, 1), f)
torch.testing.assert_close(v, initial[[0, 2, 1, 3]], rtol=0, atol=g.ATOL)
print('CZ signs and active SWAP amplitudes passed independent coordinate checks.')
```
```text
CZ signs and active SWAP amplitudes passed independent coordinate checks.
```

<span id="formula-code-5-6-toffoli"></span>

### 4. Prove an exact six-CNOT Toffoli decomposition

**Formula.** Define $T=\operatorname{diag}(1,e^{i\pi/4})$ and $T^\dagger=T^{-1}$. The diagonal CCZ has action $|abc\rangle\mapsto(-1)^{abc}|abc\rangle$. The integer identity behind its circuit is

$$
a+b+c-(a\oplus b)-(a\oplus c)-(b\oplus c)
+(a\oplus b\oplus c)=4abc.
$$

**Derivation.** For Boolean variables, $a\oplus b=a+b-2ab$. Applying this again gives

$$
a\oplus b\oplus c=a+b+c-2(ab+ac+bc)+4abc.
$$

Substitute these expressions into the first identity. Each linear coefficient is $1-2+1=0$; each pair-product coefficient is $2-2=0$. Only $4abc$ remains. Each positive parity term can therefore contribute a T phase, and each negative term a $T^\dagger$ phase, after reversibly computing the required parity.

Here is the actual chronological `ccz` circuit. The letters a,b,c below designate its two control positions and target position; in the Python helper the last position is named `t`.

| Chronological operations | Phase exponent in units of $\pi/4$ | Basis labels afterward |
|---|---|---|
| CX(b,c), T†(c) | $-(b\oplus c)$ | $(a,b,b\oplus c)$ |
| CX(a,c), T(c) | $+(a\oplus b\oplus c)$ | $(a,b,a\oplus b\oplus c)$ |
| CX(b,c), T†(c) | $-(a\oplus c)$ | $(a,b,a\oplus c)$ |
| CX(a,c), T(b), T(c) | $+b+c$ | $(a,b,c)$ |
| CX(a,b), T(a), T†(b), CX(a,b) | $+a-(a\oplus b)$ | $(a,b,c)$ |

Every label is restored. Summing phases gives $e^{i\pi abc}=(-1)^{abc}$, exactly, not merely up to a global phase. Now

$$
CCX_{a,b;t}=H_t\,CCZ_{a,b,t}\,H_t.
$$

When $ab=0$, the target sees $HH=I$; when $ab=1$, it sees $HZH=X$. This proves Toffoli on all eight basis inputs and hence on arbitrary superpositions. The construction contains six CNOTs, two H gates, four T gates and three $T^\dagger$ gates, with no ancilla. Its proof is the label-and-phase derivation above; testing eight rows is an additional implementation check.

**FlagQuantum code → verification result.** Both blocks emit their decompositions directly. The companion program also checks native `ccx` and all six permutations of ordered control/target positions.

```python
f3 = g.complex_factors(3)
initial3 = g.product_input(f3)
ccz = (fq.Circuit(3, dtype=g.D)
       .cx(1, 2).tdg(2).cx(0, 2).t(2)
       .cx(1, 2).tdg(2).cx(0, 2).t(1).t(2)
       .cx(0, 1).t(0).tdg(1).cx(0, 1))
v, _ = g.run(ccz, f3)
reference = initial3.clone(); reference[7] *= -1
torch.testing.assert_close(v, reference, rtol=0, atol=g.ATOL)
exact_toffoli = fq.Circuit(3, dtype=g.D).h(2).compose(ccz).h(2)
v, _ = g.run(exact_toffoli, f3)
torch.testing.assert_close(v, g.flip_reference(initial3, 3, 0, 1, 2), rtol=0, atol=g.ATOL)
assert g.resources(g.toffoli()) == {'h': 2, 't': 4, 'tdg': 3, 'cx': 6}
print('CCZ phase and exact Toffoli amplitudes passed; emitted Toffoli contains six CX.')
```
```text
CCZ phase and exact Toffoli amplitudes passed; emitted Toffoli contains six CX.
```

<span id="formula-code-5-6-relative"></span>

### 5. A truth-table match can still be a different quantum gate

**Formula.** Omit the last row of the CCZ construction. Its phase exponent becomes $4abc-a+(a\oplus b)$. After the same H conjugations the shortened circuit acts as

$$
|a,b,c\rangle\longmapsto
\exp\!\left[\frac{i\pi}{4}\bigl(-a+(a\oplus b)\bigr)\right]
|a,b,c\oplus ab\rangle.
$$

**Derivation.** The missing correction depends only on a,b and commutes with target H. It is not constant across control branches: for $(a,b)=(0,0)$ it is 1, while for $(0,1)$ it is $e^{i\pi/4}$. The truth table and computational-basis output probabilities therefore match exact Toffoli, but the quantum operators differ. Prepare $|0,+,0\rangle$ and apply H on b after the candidate gate. Exact Toffoli leaves $|000\rangle$. The shortened circuit instead gives amplitudes

$$
\alpha_{000}=\frac{1+e^{i\pi/4}}2,\qquad
\alpha_{010}=\frac{1-e^{i\pi/4}}2,\qquad
p_{000}=\frac{1+\cos(\pi/4)}2.
$$

This is a counterexample to substituting a truth-table-equivalent circuit without tracking phase. A particular relative-phase construction may be useful when its extra phases cancel in a separately proved surrounding network. No such cancellation is assumed here. This example is our explicitly defined shortened network, not a transcription of a similarly named circuit from a paper.

**FlagQuantum code → verification result.** The analyzer turns the extra branch phase into a measurable probability difference.

```python
analyzer_input = [(1, 0), (1/math.sqrt(2), 1/math.sqrt(2)), (1, 0)]
readout = []
for relative in (False, True):
    block = fq.Circuit(3, dtype=g.D).compose(g.toffoli(relative=relative)).h(1)
    v, p = g.run(block, analyzer_input)
    readout.append(p[0].item())
assert abs(readout[0]-1) < g.ATOL
assert abs(readout[1]-(1+math.cos(math.pi/4))/2) < g.ATOL
print('Exact / shortened Toffoli analyzer p(000):', *(f'{p:.6f}' for p in readout))
```
```text
Exact / shortened Toffoli analyzer p(000): 1.000000 0.853553
```

<span id="formula-code-5-6-clean"></span>

### 6. A clean ancilla implements a three-control NOT

**Formula.** Use ordered positions $(a,b,c,w,t)=(q_0,q_1,q_2,q_3,q_4)$. A clean workspace requires $w=0$. Let C be Toffoli $(a,b;w)$ and U be Toffoli $(w,c;t)$. The chronological sequence C,U,C implements

$$
|a,b,c,0,t\rangle\longmapsto|a,b,c,0,t\oplus abc\rangle.
$$

**Derivation.** The first C writes $ab$ into w; U toggles t by $(ab)c$; the second C restores $ab\oplus ab=0$. Each constituent is the phase-exact decomposition just proved. All other labels are preserved, so the basis proof extends to arbitrary joint amplitudes of the data and target with w initially zero, including correlated data/target inputs.

If w instead starts at d, the actual action is

$$
|a,b,c,d,t\rangle\longmapsto
|a,b,c,d,t\oplus abc\oplus dc\rangle.
$$

Restoring the workspace alone is insufficient: the retained operation contains an unwanted $dc$ term. For $a=b=c=d=1,t=0$, the network returns w=1 but leaves t=0 instead of flipping it to one.

**FlagQuantum code → verification result.** Test both the valid complex input and this invalid-blank witness. A successful run on the witness does not make its clean-input contract valid.

```python
f5 = g.complex_factors(3) + [(1, 0), g.complex_factors(1)[0]]
C = g.toffoli(0, 1, 3, n=5)  # compute a*b into workspace q3
U = g.toffoli(3, 2, 4, n=5)  # use workspace and q2 to toggle q4
clean_block = fq.Circuit(5, dtype=g.D).compose(C).compose(U).compose(C)
v, p = g.run(clean_block, f5)
torch.testing.assert_close(v, g.ancilla_reference(g.product_input(f5), 'dirty'), rtol=0, atol=g.ATOL)
assert g.probability_one(p, 3) < g.ATOL
bad = g.basis_factors((1, 1, 1, 1, 0))
v, p = g.run(g.ancilla('clean'), bad)
assert abs(p[30].item()-1) < g.ATOL
print('Clean workspace returns zero and retained operation passes; wrong blank gives |11110>.')
```
```text
Clean workspace returns zero and retained operation passes; wrong blank gives |11110>.
```

<span id="formula-code-5-6-dirty"></span>

### 7. Borrow an arbitrary ancilla with an echo sequence

**Formula.** With the same C,U, use chronological U,C,U,C. A dirty (borrowed) ancilla has an arbitrary initial quantum state that must be returned, rather than initialized to zero:

$$
|a,b,c,d,t\rangle\longmapsto|a,b,c,d,t\oplus abc\rangle.
$$

**Derivation.** The first U toggles t by dc. The first C changes w to $d\oplus ab$. The second U toggles t by $(d\oplus ab)c$. The second C returns w to d. Therefore the net target toggle is

$$
dc\oplus(d\oplus ab)c=dc\oplus dc\oplus abc=abc.
$$

No phase is introduced by the exact Toffolis. The action is identity on the borrowed factor and the desired three-control X on the other factors. Linearity proves the result even if d is superposed or correlated with the retained register or an external spectator. Returning the borrowed information does not mean setting it to zero; existing correlations need not disappear. The guarantee concerns the complete joint operator, not just the marginal probability of w.

**FlagQuantum code → verification result.** The second circuit entangles a with the borrowed qubit before the decomposition. Its final vector must be $(|01100\rangle+|11111\rangle)/\sqrt2$, preserving the relative amplitude as well as both branches.

```python
f5 = g.complex_factors(5)
dirty_block = fq.Circuit(5, dtype=g.D).compose(U).compose(C).compose(U).compose(C)
v, _ = g.run(dirty_block, f5)
torch.testing.assert_close(v, g.ancilla_reference(g.product_input(f5), 'dirty'), rtol=0, atol=g.ATOL)
block = fq.Circuit(5, dtype=g.D).h(0).cx(0, 3).compose(g.ancilla('dirty'))
v, _ = g.run(block, g.basis_factors((0, 1, 1, 0, 0)))
reference = torch.zeros(32, dtype=g.D)
reference[12] = reference[31] = 1/math.sqrt(2)
torch.testing.assert_close(v, reference, rtol=0, atol=g.ATOL)
print('Borrowed complex input and correlated ancilla passed full-vector checks at indices 12,31.')
```
```text
Borrowed complex input and correlated ancilla passed full-vector checks at indices 12,31.
```

<span id="formula-code-5-6-cost"></span>

### 8. State the elementary basis, costs and failure boundaries

**Formula and derivation.** Expanding every exact Toffoli gives the following logical instruction counts; concatenating three or four copies multiplies each count by three or four.

| Construction | H | T | T† | CNOT | Total |
|---|---:|---:|---:|---:|---:|
| Exact Toffoli, no ancilla | 2 | 4 | 3 | 6 | 15 |
| Three-control X, one clean ancilla | 6 | 12 | 9 | 18 | 45 |
| Three-control X, one borrowed ancilla | 8 | 16 | 12 | 24 | 60 |

Combining T and $T^\dagger$ as a T-type cost gives 7,21,28. These are costs of these constructions, not lower bounds or optimality claims. They assume unrestricted logical CNOT pairs. Routing, native pulse synthesis, error correction, timing and hardware calibration are not included. Units 1–2 permit continuous rotations/P gates; units 4–7 use the exact finite alphabet H,T,T†,CNOT. Counting a continuous rotation as one logical instruction does not make it one T gate.

**FlagQuantum code → verification result.** Inspect the actual emitted IR rather than estimating from a helper name. The teaching helpers reject malformed supports, nonfinite/nonliteral radian angles and undeclared ancilla modes. Choosing `clean` remains a caller's input-state obligation; the circuit constructor cannot inspect a future input. The negative witness in unit 6 checks this semantic boundary separately.

```python
for mode in ('clean', 'dirty'):
    counts = g.resources(g.ancilla(mode))
    print(mode, counts, 'total', sum(counts.values()))
invalid = [lambda: g.controlled_rotation('x', .3),
           lambda: g.controlled_rotation('z', float('nan')),
           lambda: g.controlled_rotation('y', True),
           lambda: g.controlled_rotation('y', .3, 0, 0),
           lambda: g.toffoli(0, 0, 2), lambda: g.toffoli(0, 1, 3),
           lambda: g.ancilla('reset')]
for candidate in invalid:
    try:
        candidate()
    except ValueError:
        pass
    else:
        raise AssertionError('Invalid contract accepted')
assert g.RUNS == 14
print('Seven malformed contracts rejected; fourteen actual body circuits verified.')
```
```text
clean {'h': 6, 't': 12, 'tdg': 9, 'cx': 18} total 45
dirty {'h': 8, 't': 16, 'tdg': 12, 'cx': 24} total 60
Seven malformed contracts rejected; fourteen actual body circuits verified.
```

### Complete program and independent references

Run `python examples/foundations/gate_decompositions.py` from the repository root. The [companion program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/gate_decompositions.py) checks 307 actual circuits: native/decomposed controlled rotations and boundary angles, compensated phase gates, native/decomposed CZ/SWAP and every Toffoli support permutation, phase-variant witnesses, both ancilla networks on all 32 basis inputs and complex products, and a correlated borrowed input. Independent scalar contractions, bit permutations and explicit phase factors supply the references. The exact integer parity checks supplement the symbolic proof. The body checker executes all eight cumulative snippets and compares their printed output exactly; the body itself uses 14 actual circuits.

Expected output of the complete program:

```text
80 controlled-rotation native/decomposed circuits and 20 phase-compensated circuits: all basis, complex and angle-boundary checks passed.
CZ and SWAP: 20 native/decomposed circuits agree on every basis input and complex product.
Exact Toffoli: 6 support permutations, all 8 basis and complex inputs, native/decomposed paths; 108 circuits.
Integer phase identity checked exactly on 8 Boolean triples; 9 phase-variant circuits match truth probabilities but retain extra branch phases.
Clean/dirty ancilla networks: all 32 basis + complex each, plus clean-contract complex input; 67 circuits, full complex references.
2 phase-sensitive analyzer circuits and 1 entangled borrowed-ancilla circuit passed; 7 malformed contracts rejected.
307 actual CPU complex128 circuits; atol 1e-12, rtol 0; exact Toffoli uses 6 CX, 4 T, 3 T-dagger, 2 H.
Clean three-control construction: 18 CX; borrowed-dirty echo: 24 CX; no optimality, routing, reset, noise or hardware claim.
```

### Understanding checks and transfer exercises

**5.6-A — New support and angle.** Implement controlled Ry and Rz with angle 0.91, control q2 and target q0 in a three-qubit register. Compare all eight basis inputs and a complex product. Where must the phase correction go if you replace Rz by P?

**5.6-B — Borrowed workspace on a new layout.** Map the five logical positions (a,b,c,w,t) to (q4,q2,q0,q3,q1). Write the destination index for each input coefficient. Must the borrowed qubit be initially separable?

**5.6-C — A false optimization.** Can the shortened Toffoli in unit 5 replace every exact Toffoli in the clean network merely because both have the same truth table? What evidence would a valid replacement require?

**5.6-D — Restored versus clean.** On input |11110>, what do the clean and dirty networks return? Why does a restored workspace not prove the retained operation correct?

<details markdown="1">
<summary>Answers and reasoning</summary>

**A.** Call `controlled_rotation(axis, .91, c=2, t=0, n=3)` for each axis. Use the scalar contraction with that same ordered support, not a two-qubit vector padded into the wrong axis order. A controlled P needs P(.91/2) on q2. The separate author transfer executes 18 new-parameter/support circuits, comparing full complex vectors.

**B.** In five-qubit big-endian indexing, the target q1 has integer mask 8. Toggle that mask exactly when bits q4,q2,q0 are all one. The reference is `out[j ^ (8 if condition else 0)] += input[j]`. The mapped circuit is `Circuit(5, dtype=g.D).compose(g.ancilla('dirty'), qubits=(4,2,0,3,1))`. The borrowed qubit may be correlated; the operator proof holds on every basis vector with no branch phase, so extends to joint inputs by linearity. The separate mapped complex-input test adds one circuit, for 19 transfer circuits total. This is author transfer validation, not independent review.

**C.** No. The omitted phase depends on control bits, which may change roles across Toffolis. One must derive the net branch phases and prove equality of the entire surrounding operator under its declared input contract. Computational-basis probabilities alone cannot do this; unit 5 supplies an explicit interference witness.

**D.** The clean network returns |11110>, whereas the dirty network returns |11111>. Both return w=1. The clean-input assumption was violated in the first call, introducing the unwanted dc term. Workspace restoration and retained-operation correctness are distinct obligations.

</details>

### Sources, depth and next step

Depth **F**: every selected identity is proved on all computational-basis inputs, with phase tracking and an explicit extension by linearity. Assigned background is Nielsen and Chuang, 10th Anniversary Edition (2010), §4.3; no fresh local-PDF inspection is claimed. The public primary paper [Barenco et al., Elementary gates for quantum computation (1995), arXiv quant-ph/9503016v1](https://arxiv.org/pdf/quant-ph/9503016v1), §§6.1–6.2 (PDF pages 14–16), provides controlled-gate reduction and the warning that phase-congruent networks need not be interchangeable in quantum computations. These locations were checked against the public PDF. Our six-CNOT T-phase network and its explicitly defined shortened variant are proved above; they are not claimed to be the paper's displayed network or its particular phase variant.

The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/5.6.json) separates author execution from independent mathematical/implementation review and reader trials, which remain pending. This is an author-verified working draft, not accepted content. No optimal synthesis, reset, hardware execution, noise model or approximate compiler is claimed. Continue with [5.7 Approximation, synthesis, and precision](#sec-gates-reversible-computation-and-circuit-synthesis-7).

<span id="sec-gates-reversible-computation-and-circuit-synthesis-7"></span>

## 5.7 Approximation, synthesis, and precision

Exact continuous universality does not say how to approximate a desired gate using a fixed finite instruction alphabet. Nor does a simulator reproducing a gate word accurately say how close that word is to the desired operation. This section connects the approximation theorem to separate, checkable error budgets. Prerequisites are [2.7](ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-7), for induced norms, and [5.5](#sec-gates-reversible-computation-and-circuit-synthesis-5), for the continuous-versus-finite distinction.

The theorem has depth **R**: we state its assumptions, identify its deferred ingredients, prove the local norm and commutator lemmas and derive the recursion exponent. The runnable compiler illustration is a bounded exhaustive search, explicitly separate from the theorem's constructive algorithm. Numerical examples use FlagQuantum 0.3.1/PyTorch 2.13.0, CPU complex128, implementation tolerance $10^{-12}$ with relative tolerance zero, full operator phase and no state repair. Mathematical approximation tolerances are separately stated; a computed floating-point norm is not an interval certificate.

<span id="formula-code-5-7-phase"></span>

### 1. Choose an operator and phase contract before approximating

**Formula.** The special unitary group is

$$
SU(d)=\{V\in\mathbb C^{d\times d}:V^\dagger V=I,\ \det V=1\}.
$$

For a unitary U, choose $\chi=\operatorname{Arg}(\det U)/d$ and set $V=e^{-i\chi}U$. Then $U=e^{i\chi}V$ and $\det V=e^{-id\chi}\det U=1$. Here Arg denotes the principal argument in $(-\pi,\pi]$. Other determinant roots give other valid pairs; the chosen phase must accompany V. This is a coordinate convention, not permission to discard a phase in a controlled context.

**Derivation.** Multiplying a d-dimensional matrix by a scalar multiplies its determinant by the scalar's dth power. Thus the displayed conversion preserves the exact U when reconstructed. The operator metric below distinguishes I and −I: $\|I-(-I)\|_2=2$, even though they give the same isolated pure-state ray. If an application permits quotienting by a global phase, that must be a different, explicit acceptance contract. This section keeps full operator phase. See [3.7](ch-single-qubit-states-and-rotations.md#sec-single-qubit-states-and-rotations-7) for why controlling a block can expose its phase.

**FlagQuantum code → verification result.** These are original book helpers, not a native SK API. The scalar/determinant convention is checked separately from executing the complete U(2) matrix. Preparations remain outside the tested block. The snippets are cumulative.

```python
import math
import torch
import flagquantum as fq
import examples.foundations.approximation_precision as a
f = [(.6, .8j)]
U = torch.exp(torch.tensor(.31j, dtype=a.D))*a.explicit('z', .73)
chi, V = a.strip_phase(U)
torch.testing.assert_close(torch.exp(torch.tensor(1j*chi, dtype=a.D))*V, U, rtol=0, atol=a.ATOL)
v, _ = a.run(fq.Circuit(1, dtype=a.D).unitary(0, unitary=U), f)
torch.testing.assert_close(v, U @ a.product_input(f), rtol=0, atol=a.ATOL)
v, _ = a.run(fq.Circuit(1, dtype=a.D).rz(0, 2*math.pi), f)
torch.testing.assert_close(v, -a.product_input(f), rtol=0, atol=a.ATOL)
print(f'Retained determinant phase: {chi:.6f}; distance(I,-I): {a.distance(a.I, -a.I):.6f}')
```
```text
Retained determinant phase: 0.310000; distance(I,-I): 2.000000
```

<span id="formula-code-5-7-metric"></span>

### 2. Translate an operator error into state and probability errors

**Formula.** Use the induced Euclidean operator norm from [2.7](ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-7):

$$
\delta=\|U-V\|_2=\sup_{\|\psi\|_2=1}\|(U-V)\psi\|_2.
$$

For normalized $|u\rangle=U|\psi\rangle$ and $|v\rangle=V|\psi\rangle$, their vector distance is at most δ. For an orthogonal projector $\Pi=\Pi^\dagger=\Pi^2$,

$$
\bigl|\langle u|\Pi|u\rangle-\langle v|\Pi|v\rangle\bigr|
\le 2\delta.
$$

**Derivation.** Insert and subtract $\langle v|\Pi|u\rangle$ to write the difference as
$\langle u-v|\Pi|u\rangle+\langle v|\Pi|u-v\rangle$. Cauchy–Schwarz, $\|\Pi\|_2\le1$ and unit norms bound each term by $\|u-v\|_2$. A probability difference is also at most one, so $\min(1,2\delta)$ is a valid bound. This bounds each event projector, not the sum of absolute errors over many outcomes. Here a basis event uses $\Pi_j=|j\rangle\langle j|$; broader measurement theory follows in Chapter 6.

**FlagQuantum code → verification result.** The simulator must reproduce the chosen approximate matrix to implementation tolerance; it need not reproduce the ideal target to that same tolerance. Compare these two residuals separately. Numerical singular values give an estimated operator norm, not a rigorous interval certificate.

```python
target = a.explicit('z', .73)
candidate = a.explicit('z', .70)
delta = a.distance(target, candidate)
v, p = a.run(fq.Circuit(1, dtype=a.D).rz(0, .70), f)
ideal = target @ a.product_input(f)
implementation = torch.linalg.vector_norm(v-candidate @ a.product_input(f)).item()
state_error = torch.linalg.vector_norm(v-ideal).item()
assert implementation < a.ATOL and state_error <= delta+a.ATOL
assert torch.max(torch.abs(p-ideal.abs().square())).item() <= 2*delta+a.ATOL
print(f'Operator / state errors: {delta:.6f} / {state_error:.6f}; implementation residual < 1e-12.')
```
```text
Operator / state errors: 0.015000 / 0.015000; implementation residual < 1e-12.
```

<span id="formula-code-5-7-composition"></span>

### 3. Allocate a circuit budget with a telescoping proof

**Formula.** Let chronological target gates be $U_1,\ldots,U_m$, and their unitary replacements $V_1,\ldots,V_m$. Then

$$
\left\|V_m\cdots V_1-U_m\cdots U_1\right\|_2
\le\sum_{j=1}^m\|V_j-U_j\|_2.
$$

**Derivation.** Insert hybrid products, replacing one factor at a time. Their signed differences telescope exactly:

$$
V_m\cdots V_1-U_m\cdots U_1
=\sum_{j=1}^m V_m\cdots V_{j+1}(V_j-U_j)U_{j-1}\cdots U_1.
$$

An absent prefix/suffix is identity. Each surrounding product is unitary and has norm one. Submultiplicativity and the triangle inequality give the claimed sum. No independence or cancellation assumption is used. Thus for $m>0$, a uniform per-gate budget $\varepsilon/m$ suffices for a total budget ε. Unequal allocations may be more useful when gates have different synthesis costs.

Inverse words cost no extra alphabet assumption when the alphabet is inverse-closed: reverse chronological order and invert every instruction. Moreover $\|U^\dagger-V^\dagger\|_2=\|U-V\|_2$, because a matrix and its adjoint have the same singular values. This preserves approximation accuracy, not merely the truth table of an inverse.

**FlagQuantum code → verification result.** Test a three-gate replacement and an exact inverse-word roundtrip. The product order matches [5.1](#sec-gates-reversible-computation-and-circuit-synthesis-1).

```python
exact = [('x', .31), ('z', -.63), ('y', .87)]
Ut = a.I.clone(); Va = a.I.clone(); budget = 0.
block = fq.Circuit(1, dtype=a.D)
for axis, theta in exact:
    u, v = a.explicit(axis, theta), a.explicit(axis, theta+.01)
    Ut = u @ Ut; Va = v @ Va; budget += a.distance(u, v)
    getattr(block, 'r'+axis)(0, theta+.01)
v, _ = a.run(block, f)
torch.testing.assert_close(v, Va @ a.product_input(f), rtol=0, atol=a.ATOL)
assert a.distance(Ut, Va) <= budget+a.ATOL
word = (('x', 1), ('z', -1), ('x', 1))
roundtrip = a.word_circuit(word).compose(a.word_circuit(a.inverse_word(word)))
v, _ = a.run(roundtrip, f)
torch.testing.assert_close(v, a.product_input(f), rtol=0, atol=a.ATOL)
print(f'Circuit operator error <= allocated sum {budget:.6f}; inverse-word roundtrip passed.')
```
```text
Circuit operator error <= allocated sum 0.015000; inverse-word roundtrip passed.
```

<span id="formula-code-5-7-rounding"></span>

### 4. Derive a radian-grid error without losing a full-turn phase

**Formula.** For $R_z(\theta)=\operatorname{diag}(e^{-i\theta/2},e^{i\theta/2})$,

$$
\|R_z(\theta)-R_z(\widetilde\theta)\|_2
=2\left|\sin\frac{\theta-\widetilde\theta}{4}\right|
\le\frac{|\theta-\widetilde\theta|}{2}.
$$

**Derivation.** The difference is diagonal, so its norm is the larger absolute diagonal entry. Both entries have magnitude $|e^{ix}-e^{iy}|=2|\sin((x-y)/2)|$. Substitute the half angles and use $|\sin s|\le|s|$. On a grid of step $h=4\pi/2^b$, nearest-integer rounding gives $|\theta-\widetilde\theta|\le h/2$, hence operator error at most $h/4=\pi/2^b$. A sufficient positive integer b for a desired positive error η is $b\ge\log_2(\pi/\eta)$; use at least one bit in this helper.

The period is $4\pi$ for a phase-exact rotation matrix. The code rounds the **unwrapped** radian angle and never replaces $2\pi$ by zero. This grid-resolution b is not the binary mantissa precision of Python floats. The inequality is an exact real-arithmetic statement; floating angle arithmetic and computed residuals have a separate numerical tolerance. The helper's limits of 1–20 grid bits and absolute angle ≤100 are teaching guards, not FlagQuantum restrictions.

**FlagQuantum code → verification result.** A Z rotation preserves computational-basis probabilities while changing relative phases. Therefore the full complex vector, rather than that probability distribution alone, is the reference.

```python
for bits in (3, 6, 10):
    rounded, h = a.quantized_angle(.73, bits)
    Uq = a.explicit('z', rounded)
    err = a.distance(a.explicit('z', .73), Uq)
    assert abs(err-2*abs(math.sin((.73-rounded)/4))) < a.ATOL
    assert err <= h/4+a.ATOL
    v, _ = a.run(fq.Circuit(1, dtype=a.D).rz(0, rounded), f)
    torch.testing.assert_close(v, Uq @ a.product_input(f), rtol=0, atol=a.ATOL)
    print(f'grid bits {bits}: angle {rounded:.6f}, operator error {err:.6f}, bound {h/4:.6f}')
```
```text
grid bits 3: angle 0.000000, operator error 0.362977, bound 0.392699
grid bits 6: angle 0.785398, operator error 0.027698, bound 0.049087
grid bits 10: angle 0.724039, operator error 0.002981, bound 0.003068
```

<span id="formula-code-5-7-words"></span>

### 5. Use a finite-word search without mistaking it for a theorem

**Formula.** A chronological word $w=(g_1,\ldots,g_\ell)$ represents $M(w)=g_\ell\cdots g_1$. For an alphabet of size four, the number of words of length at most k is

$$
N_k=\sum_{j=0}^k4^j=\frac{4^{k+1}-1}{3}.
$$

**Derivation.** There are four independent choices at each position, hence $4^j$ words of length j, including the empty identity word at j=0. Enumerating all such words supplies a finite set of candidate matrices. Since the catalog at k contains the catalog at k−1, its best estimated error cannot increase. This proves neither that the errors approach zero nor that the set covers all targets at a desired accuracy.

The teaching alphabet is $\{R_x(\pi/4),R_x(-\pi/4),R_z(\pi/4),R_z(-\pi/4)\}$. Its matrices are in SU(2) and each inverse is explicitly present. Those statements follow directly from the rotation eigenvalues and sign reversal. **Density is a separate theorem hypothesis; neither this search nor its passing examples certify it.** A finite alphabet has countably many finite words, so it cannot exactly represent an uncountable group. Countable sets can be dense: approximate coverage and exact representability are different questions.

**FlagQuantum code → verification result.** `search` exhausts every word up to the requested depth without deduplicating or phase-aligning matrices. It returns the chronological word, its matrix, estimated target error and number searched. Depth ≤6 is a teaching memory/time guard. It is not an SK implementation, optimal compiler or guaranteed net construction. The emitted circuit uses only the declared ±π/4 named Rx/Rz calls, never a native custom gate holding the ideal target.

```python
target = a.explicit('y', .71) @ a.explicit('z', -.43)
previous = float('inf')
for depth in (2, 4, 6):
    word, candidate, delta, count = a.search(target, depth)
    assert count == (4**(depth+1)-1)//3 and delta <= previous+a.ATOL
    previous = delta
    print(f'depth {depth}: {count} words, best operator error {delta:.6f}')
v, _ = a.run(a.word_circuit(word), f)
torch.testing.assert_close(v, candidate @ a.product_input(f), rtol=0, atol=a.ATOL)
assert torch.linalg.vector_norm(v-target @ a.product_input(f)).item() <= delta+a.ATOL
print('Selected finite word executed; implementation and target residuals checked separately.')
```
```text
depth 2: 21 words, best operator error 0.377938
depth 4: 341 words, best operator error 0.123685
depth 6: 5461 words, best operator error 0.121237
Selected finite word executed; implementation and target residuals checked separately.
```

<span id="formula-code-5-7-commutator"></span>

### 6. Explain the cancellation that makes recursive improvement possible

**Formula.** A group commutator is $K(V,W)=VWV^\dagger W^\dagger$. It is not the matrix difference $VW-WV$. If V,W are near identity, their group commutator can be closer still. For $V=R_x(\alpha)$ and $W=R_y(\beta)$,

$$
\|K(V,W)-I\|_2=2|\sin(\alpha/2)\sin(\beta/2)|.
$$

**Local derivation.** Write $R_x(\alpha)=c_\alpha I-is_\alpha X$ and $R_y(\beta)=c_\beta I-is_\beta Y$, where $c_\alpha=\cos(\alpha/2)$ and $s_\alpha=\sin(\alpha/2)$. Conjugation gives $R_x(\alpha)Y R_x(-\alpha)=\cos\alpha\,Y+\sin\alpha\,Z$. Multiplying this conjugated W by $W^\dagger=c_\beta I+is_\beta Y$, the coefficient of identity is

$$
c_\beta^2+s_\beta^2\cos\alpha
=1-2s_\alpha^2s_\beta^2.
$$

All Pauli terms have zero trace, so the trace of K is twice this coefficient. Since a two-dimensional special unitary has conjugate eigenvalues $e^{i\omega},e^{-i\omega}$, both eigenvalues of $(I-K)^\dagger(I-K)=2I-K-K^\dagger$ equal $2-\operatorname{tr}K$. Taking square roots yields the displayed norm. Small α and β therefore produce a quadratic rather than linear distance.

We also need a **perturbation lemma**, not just a small commutator. Let V',W' be unitary approximations, with $d_V=\|V'-V\|_2$ and $d_W=\|W'-W\|_2$. Then

$$
\|K(V',W')-K(V,W)\|_2
\le2d_V\|W-I\|_2+2d_W\|V'-I\|_2.
$$

To prove the first term, put $E=V'V^\dagger$, $A=VWV^\dagger$ and write

$$
EAE^\dagger-A=(E-I)(A-I)E^\dagger+(A-I)(E^\dagger-I).
$$

Both sides expand to the same matrix. Norms of unitary factors are one, $\|E-I\|_2=d_V$ and $\|A-I\|_2=\|W-I\|_2$. Right multiplication by $W^\dagger$ does not change the norm. For the second term interchange V,W and use $K(W,V)=K(V,W)^\dagger$, then the triangle inequality to combine the two replacements. If $d_V,d_W\le\varepsilon$ and $\|V-I\|_2,\|W-I\|_2\le B\sqrt\varepsilon$, this implies

$$
\|K(V',W')-K(V,W)\|_2
\le4B\varepsilon^{3/2}+2\varepsilon^2.
$$

Here $\|V'-I\|_2\le B\sqrt\varepsilon+\varepsilon$. For $0<\varepsilon\le1$, the last bound is at most $(4B+2)\varepsilon^{3/2}$. This elementary lemma explains the gain **conditional on** finding balanced V,W. It does not construct them for an arbitrary desired residual; that geometric step is deferred below.

**FlagQuantum code → verification result.** To implement $VWV^\dagger W^\dagger$, chronological calls start with $W^\dagger$, not V. The numerical reference is independent matrix multiplication; the norm additionally has the closed-form check above.

```python
alpha, beta = .2, .3
V, W = a.explicit('x', alpha), a.explicit('y', beta)
K = a.commutator(V, W)
block = (fq.Circuit(1, dtype=a.D).ry(0, -beta).rx(0, -alpha)
         .ry(0, beta).rx(0, alpha))
v, _ = a.run(block, f)
torch.testing.assert_close(v, K @ a.product_input(f), rtol=0, atol=a.ATOL)
closed_form = 2*abs(math.sin(alpha/2)*math.sin(beta/2))
assert abs(a.distance(K, a.I)-closed_form) < a.ATOL
eps = .001
Vp = a.explicit('z', eps) @ V; Wp = a.explicit('x', -eps) @ W
bound = 2*a.distance(Vp, V)*a.distance(W, a.I)+2*a.distance(Wp, W)*a.distance(Vp, a.I)
assert a.distance(a.commutator(Vp, Wp), K) <= bound+a.ATOL
print(f'Group commutator norm {closed_form:.6f}; exact formula and perturbation bound passed.')
```
```text
Group commutator norm 0.029838; exact formula and perturbation bound passed.
```

<span id="formula-code-5-7-theorem"></span>

### 7. State the scoped theorem and derive its recursion exponent

**Theorem (Solovay–Kitaev, scoped).** Fix dimension $d\ge2$ and a finite alphabet $G\subset SU(d)$ that contains every generator's inverse and generates a dense subgroup. For sufficiently small $\varepsilon>0$, every $U\in SU(d)$ has a word S satisfying $\|U-M(S)\|_2\le\varepsilon$ and length $O(\log^c(1/\varepsilon))$. Constants may depend on G and d. A classical commutator construction gives $c=\log5/\log(3/2)\approx3.97$. This is not an optimal exponent, a bound uniform in growing d, or a finite-precision bit-complexity claim. In particular setting $d=2^n$ does not establish efficient general synthesis in n.

The theorem and general construction are imported at depth **R** from the assigned NC Appendix 3, with a publicly inspected companion source: [Dawson and Nielsen, The Solovay-Kitaev algorithm, v2 (2005), Theorem 1 and §§3–5](https://arxiv.org/pdf/quant-ph/0505030v2). The proof here supplies local error lemmas and the following conditional recursion analysis. General balanced-commutator geometry, a certified coarse net and explicit valid constants are deferred to those sources; an unwritten appendix of this book is not treated as an available proof.

**Roadmap → local derivation.** Start with a coarse word $S_{k-1}$ at error $\varepsilon_{k-1}$. The residual $\Delta=U M(S_{k-1})^\dagger$ is that close to I. In the qubit construction, a geometric lemma supplies $\Delta=K(V,W)$ with $\|V-I\|_2,\|W-I\|_2\le B\sqrt{\varepsilon_{k-1}}$. Recursively approximate V,W to error $\varepsilon_{k-1}$, then prepend the resulting commutator to the old **matrix** product. Chronological execution first runs $S_{k-1}$, then $W'^{-1},V'^{-1},W',V'$. Unit 6 bounds the new error by $C\varepsilon_{k-1}^{3/2}$ for a fixed sufficient C. Higher fixed dimensions may use an approximate balanced decomposition with an additional $O(\varepsilon_{k-1}^{3/2})$ residual; this changes C and is also deferred.

Why does this give a polylogarithmic length? Choose the coarse accuracy so $q=C^2\varepsilon_0<1$. Define an upper-bound sequence by $\varepsilon_k=C\varepsilon_{k-1}^{3/2}$. Then

$$
C^2\varepsilon_k=(C^2\varepsilon_{k-1})^{3/2}
=q^{(3/2)^k},\qquad L_k\le5^kL_0.
$$

The five word occurrences are the old word and the two new words with their two inverses. Taking logarithms in $q^{(3/2)^k}/C^2\le\varepsilon$ gives $(3/2)^k=O(\log(1/\varepsilon))$. Raising this to $\log5/\log(3/2)$ gives the theorem's displayed length exponent. A coarse net must cover **all** targets at its claimed accuracy; one target's successful finite search is insufficient. Density and compactness motivate such a fixed finite net, but the catalog here supplies no certified coverage radius.

**Code → verification result.** This scalar recurrence illustrates the derived bounds only. It does not measure the teaching search, determine an SK constant for its alphabet, or certify a gate approximation. We choose illustrative C=6 and ε₀=0.001 and keep the short sequence above the floating-point underflow range.

```python
C, epsilon, length = 6., .001, 1
assert C*C*epsilon < 1
for level in range(4):
    assert epsilon > 0
    print(f'illustrative level {level}: error bound {epsilon:.3e}, word-length bound {length}')
    epsilon = C*epsilon**1.5; length *= 5
print(f'Length exponent log(5)/log(3/2): {math.log(5)/math.log(1.5):.6f}')
```
```text
illustrative level 0: error bound 1.000e-03, word-length bound 1
illustrative level 1: error bound 1.897e-04, word-length bound 5
illustrative level 2: error bound 1.568e-05, word-length bound 25
illustrative level 3: error bound 3.726e-07, word-length bound 125
Length exponent log(5)/log(3/2): 3.969362
```

<span id="formula-code-5-7-budgets"></span>

### 8. Keep the scientific error ledger separate from implementation checks

**Formula and derivation.** If ideal target U, selected exact word S, represented word matrix $\widehat S$ and computed output $|\widehat v\rangle$ refer to the same normalized input, then

$$
\|\widehat v-U\psi\|_2
\le\underbrace{\|\widehat v-\widehat S\psi\|_2}_{\text{execution residual}}
+\underbrace{\|\widehat S-S\|_2}_{\text{representation error}}
+\underbrace{\|S-U\|_2}_{\text{synthesis error}}.
$$

This is the triangle inequality after inserting $\widehat S\psi$ and $S\psi$. An angle-grid error may be a representation error or a deliberate synthesis replacement; assign it to one category once, rather than double-counting it. The exact word S is a mathematical product. Its floating-point product is only a representation. Our singular-value residuals estimate some terms numerically; no bound on every rounding operation or interval enclosure of the exact total is claimed.

A simulator option forbidding approximate simulation does not remove synthesis error: the simulator may accurately execute a deliberately approximate gate word. Conversely, a small target-state residual for one input does not establish a small operator norm for every input. The example checks all basis columns and a complex input for each chosen word and separately computes the small-matrix norm. No hardware, pulse, shot-noise or calibration budget is included.

**Code → verification result.** Reject unsupported dimensions, nonunitary matrices, an unrecorded U(2) phase presented as SU(2), excessive search depth, invalid grid units/types and instructions outside the declared alphabet. These teaching helpers do not repair a bad matrix by normalization or projection. The depth/alphabet/CPU guards are repository contracts, not limitations claimed for FlagQuantum itself.

```python
invalid = [lambda: a.search(torch.eye(3, dtype=a.D), 2), lambda: a.search(2*a.I, 2),
           lambda: a.search(torch.exp(torch.tensor(.2j, dtype=a.D))*a.I, 2),
           lambda: a.catalog(7), lambda: a.catalog(True),
           lambda: a.quantized_angle(float('nan'), 4),
           lambda: a.quantized_angle(.3, True), lambda: a.quantized_angle(.3, 0),
           lambda: a.word_circuit((('y', 1),)), lambda: a.inverse_word((('x', True),))]
for call in invalid:
    try:
        call()
    except ValueError:
        pass
    else:
        raise AssertionError('Invalid approximation contract accepted')
assert a.RUNS == 10
print('Ten invalid contracts rejected; ten actual body circuits; no SK implementation or certified numerical error claim.')
```
```text
Ten invalid contracts rejected; ten actual body circuits; no SK implementation or certified numerical error claim.
```

### Complete program and expected output

Run `python examples/foundations/approximation_precision.py` from the repository root. The [complete example](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/approximation_precision.py) executes 93 actual circuits: 45 angle-grid cases, 9 phase-retaining U(2) cases, 36 finite-word cases and 3 circuit-composition cases. Each selected matrix is checked on both basis inputs and a complex input. Additional classical checks cover exact word inverses, catalog sizes, closed-form angle/commutator norms and perturbation inequalities. The [body checker](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/scripts/check_approximation_precision_prose.py) executes eight cumulative snippets containing ten circuits and compares every printed result exactly.

Expected output of the complete program:

```text
45 quantized-Rz circuits: exact angle-error formula and grid bound passed; angles were not reduced modulo 2*pi.
9 U(2) circuits: determinant phase retained and reconstructed; SU(2) target validated separately.
36 finite-word circuits: depth 0/2/4/6, nested best errors, full vectors and inverse words passed; no SK or density claim.
3 composed-rotation circuits, 3 exact commutator formulas and 3 local perturbation bounds passed.
10 malformed contracts rejected; 93 actual CPU complex128 circuits; implementation atol 1e-12, rtol 0.
Synthesis error, angle rounding and floating-point residuals are separate; no hardware or certified-interval error claim.
```

### Understanding checks and transfer exercises

**5.7-A — New targets, two residuals.** Search to depth five for $R_y(-0.52)R_x(0.19)$, $R_z(0.91)$ and $R_x(1.03)R_z(-0.27)$. Execute the selected words on both basis states and (.6,.8i). Which residual should be compared to 10⁻¹², and which to the returned target error?

**5.7-B — A new grid.** Quantize the unwrapped angle −1.17 with seven grid bits. Predict a valid upper bound on operator error and check the same three inputs. What fails if you first reduce all angles modulo 2π?

**5.7-C — Budget allocation.** A circuit has 200 unitary targets and total operator-error budget 0.01. Give a sufficient uniform synthesis budget, assuming no other error category consumes it. Does passing one input imply the operator bound?

**5.7-D — Missing theorem assumptions.** You tested ten targets at depth six. Which of inverse closure, density, a certified coarse-net radius and the general balanced-residual construction have those runs established? Why is a growing multi-qubit dimension outside a fixed-dimension efficiency claim?

<details markdown="1">
<summary>Answers and reasoning</summary>

**A.** Compare simulator output to the selected word matrix at implementation tolerance 10⁻¹²; compare it to the ideal target using the returned estimated operator error plus the separately stated implementation allowance. Chronological order for the first target is Rx(.19), then Ry(−.52). A return value from a bounded search can be too inaccurate for a desired scientific budget; the caller must reject it in that case, rather than weakening the requirement. The separate author transfer performs nine circuits for these new targets.

**B.** Here h=4π/128, so h/4=π/128 is a valid exact grid bound. The separate author transfer executes three more circuits, for twelve transfer circuits total. Modulo 2π identifies Rz(2π)=−I with Rz(0)=I, changing the full operator phase and potentially a controlled block's relative phase. The 4π grid avoids silently making that identification.

**C.** Each replacement may use at most 0.01/200=0.00005. The telescoping proof does not require independent errors. Other representation/execution errors need their own budget, so this allocation cannot also cover those costs without further bounds. One input probes only one direction; the operator norm is a supremum over every normalized input.

**D.** None of these global conditions follows merely from ten target runs. Inverse closure can instead be proved by inspecting the declared alphabet and its exact inverses. Density and a certified uniform net need mathematical arguments, not a finite success list. The general balanced-residual lemma is an explicit import. Constants and preprocessing may depend on d, which is exponential in qubit count; fixing d therefore does not prove efficient arbitrary n-qubit compilation.

</details>

### Sources, deferred depth and next step

Assigned source: Nielsen and Chuang, 10th Anniversary Edition (2010), Appendix 3, beginning at printed page 617. Its assigned locator is retained; no fresh inspection of the user-local textbook PDF is claimed. Public companion verification used [Dawson and Nielsen (2005), quant-ph/0505030v2](https://arxiv.org/pdf/quant-ph/0505030v2): §2 and Theorem 1 (PDF pages 2–4), the recurrence in §3 (pages 4–7), the balanced-commutator ingredient in §4.1 (pages 8–9) and the fixed-dimension extension in §5 (pages 10–12). The local bounds above are proved explicitly, not outsourced to numerical tests. General residual decomposition, quantitative coarse-net coverage and valid geometric constants remain deferred at the frozen R depth. No numerical search result here is substituted for those obligations.

The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/5.7.json) records actual author execution and separates it from independent mathematical review, implementation review and reader trials, which remain pending. This remains a working draft. Continue with [5.8 Circuit identities and safe transformations](#sec-gates-reversible-computation-and-circuit-synthesis-8).

<span id="sec-gates-reversible-computation-and-circuit-synthesis-8"></span>

## 5.8 Circuit identities and safe transformations

A gate replacement must state the operator it preserves, its ordered support and its parameter/phase conventions. Testing a few output probabilities cannot establish that the replacement is safe in a larger program. This section proves a small rewrite vocabulary and implements a conservative cancellation pass, with explicit counterexamples to broader rules. Prerequisites are [5.1](#sec-gates-reversible-computation-and-circuit-synthesis-1), for call order and inverses, and [5.2](#sec-gates-reversible-computation-and-circuit-synthesis-2), for coherent controls and ancilla contracts.

Every identity below concerns fixed ideal finite-dimensional unitary operators, with basis order $|q_0\cdots q_{n-1}\rangle$ and no discarded global phase. The tests use released FlagQuantum 0.3.1/PyTorch 2.13.0 on CPU complex128, full-vector absolute tolerance $10^{-12}$ and relative tolerance zero, without phase alignment or state repair. Proofs establish the identities; numerical tests check the implementation and its gate conventions. No floating-point interval certificate is claimed.

<span id="formula-code-5-8-cancellation"></span>

### 1. Cancel an inverse only on the same ordered support

**Formula.** Work with fixed ideal unitary gates and the full operator phase. Define

$$
X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix},\quad
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\quad
H=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}.
$$

Their squares are I. A chronological pair $(U,U^\dagger)$ therefore has matrix $U^\dagger U=I$. In particular H,H; X,X; Y,Y; Z,Z; and two identical CNOTs cancel. A CNOT with control c and target t maps $(a,b)$ to $(a,b\oplus a)$; applying it twice returns $(a,b)$ with no phase.

**Derivation.** The support is part of the operator. $CX_{0,1}$ and $CX_{1,0}$ do not form an inverse pair merely because their unordered qubit sets agree: on $|10\rangle$, chronological $CX_{0,1},CX_{1,0}$ gives $|01\rangle$. Nor can two inverse instructions be canceled across an intervening gate without an additional identity. The CNOT proof extends from every basis vector to every complex input by linearity. For the complex entries, $Y^2=\operatorname{diag}((-i)i,i(-i))=I$. For H, multiplying the two displayed integer matrices gives $H^2=\tfrac12\begin{pmatrix}2&0\\0&2\end{pmatrix}=I$. The off-diagonal X exchanges the two coordinates twice, while diagonal Z squares each sign to one.

**FlagQuantum code → verification result.** `cancellation` is an original, deliberately conservative book helper, not a native optimizer. Its instruction is `(name, ordered_qubit_tuple, angle_tuple)`. It removes only adjacent declared inverses and exact zero-angle instructions. It never uses approximate equality to decide a rewrite. The independent matrix reference fills coordinates from scalar gate entries and bit updates. Snippets below are cumulative; run from the repository root.

```python
import math
import torch
import flagquantum as fq
import examples.foundations.circuit_rewrites as w
f2 = w.complex_factors(2)
program = (('h',(0,),()), ('cx',(0,1),()),
           ('rx',(1,),(.37,)), ('rx',(1,),(-.37,)),
           ('cx',(0,1),()), ('h',(0,),()))
reduced = w.cancellation(2, program)
assert reduced == ()
for candidate in (program, reduced):
    v, _ = w.run(w.compile_program(2, candidate), f2)
    torch.testing.assert_close(v, w.product_input(f2), rtol=0, atol=w.ATOL)
print('Nested exact cancellation: six instructions -> zero; full complex vector preserved.')
```
```text
Nested exact cancellation: six instructions -> zero; full complex vector preserved.
```

<span id="formula-code-5-8-generators"></span>

### 2. Merge rotations with the same generator and preserve full-turn phase

**Formula.** For the same Hermitian generator G on the same ordered support,

$$
e^{-i\phi G/2}e^{-i\theta G/2}=e^{-i(\theta+\phi)G/2}.
$$

For a Pauli generator $G\in\{X,Y,Z\}$, $G^2=I$ gives
$R_G(\theta)=\cos(\theta/2)I-i\sin(\theta/2)G$. Also define $P(\theta)=\operatorname{diag}(1,e^{i\theta})$, $S=P(\pi/2)$ and $T=P(\pi/4)$. Their phase angles add as well, with $S^\dagger=P(-\pi/2)$ and $T^\dagger=P(-\pi/4)$.

**Derivation.** In an orthonormal eigenbasis of Hermitian G, each eigenvalue λ contributes scalar factors $e^{-i\phi\lambda/2}e^{-i\theta\lambda/2}=e^{-i(\theta+\phi)\lambda/2}$; conjugating back proves the formula. For the Pauli expression, separate even and odd powers of the exponential series, using $G^{2k}=I$ and $G^{2k+1}=G$. Thus inverse angles cancel, but $R_G(2\pi)=-I$ and $R_G(4\pi)=I$. By contrast $P(2\pi)=I$. A modulo-$2\pi$ rule valid for P cannot be copied to R.

More generally, commuting Hermitian generators yield commuting exponentials: their matrix powers commute term by term in the convergent finite-matrix exponential series. Distinct axes do not satisfy this sufficient condition. Special angles may nevertheless produce commuting gates; noncommuting generators do not forbid every angle-specific identity.

**FlagQuantum code → verification result.** The merge below is constructed explicitly. The cancellation helper does not merge general nonzero angles, so it avoids silently adding a floating-point angle-rounding step. If an implementation does merge, the mathematical identity is exact while the represented sum's rounding belongs in [5.7](#sec-gates-reversible-computation-and-circuit-synthesis-7)'s error ledger. All angles here are radians.

```python
f1 = w.complex_factors(1)
left = fq.Circuit(1, dtype=w.D).ry(0, .23).ry(0, .37)
right = fq.Circuit(1, dtype=w.D).ry(0, .23+.37)
reference = w.explicit('y', .23+.37) @ w.product_input(f1)
for block in (left, right):
    v, _ = w.run(block, f1)
    torch.testing.assert_close(v, reference, rtol=0, atol=w.ATOL)
v, _ = w.run(fq.Circuit(1, dtype=w.D).rz(0, 2*math.pi), f1)
torch.testing.assert_close(v, -w.product_input(f1), rtol=0, atol=w.ATOL)
assert w.cancellation(1, (('rz',(0,),(2*math.pi,)),)) != ()
print('Same-axis merge passed; Rz(2*pi) retains minus identity and is not deleted.')
```
```text
Same-axis merge passed; Rz(2*pi) retains minus identity and is not deleted.
```

<span id="formula-code-5-8-disjoint"></span>

### 3. Commute disjoint supports without assuming a product input

**Formula.** If A and B act on disjoint ordered supports, their full-register embeddings commute. In coordinates placing those supports first,

$$
(A\otimes I)(I\otimes B)=A\otimes B=(I\otimes B)(A\otimes I).
$$

**Derivation.** On a basis vector $|a\rangle\otimes|b\rangle$, either order gives
$\sum_{a',b'}A_{a'a}B_{b'b}|a'\rangle\otimes|b'\rangle$. Scalar entries commute, and the same finite sum results. Those product basis vectors span the joint space, so the identity also holds for entangled inputs. A common permutation back to physical register coordinates conjugates both products by the same permutation and preserves equality. Spectator factors remain identity. This is a statement about operator supports, not about whether a particular state happens to be separable.

**FlagQuantum code → verification result.** q0 and q2 are nonadjacent positions in a three-qubit register. Independent full matrices verify placement, and the complete program additionally checks a correlated q0/q2 input. No qubit is physically moved when call order is exchanged.

```python
f3 = w.complex_factors(3)
left = (('rx',(0,),(.41,)), ('rz',(2,),(-.37,)))
right = tuple(reversed(left))
reference = w.matrix(3, left) @ w.product_input(f3)
for candidate in (left, right):
    v, _ = w.run(w.compile_program(3, candidate), f3)
    torch.testing.assert_close(v, reference, rtol=0, atol=w.ATOL)
print('Nonadjacent disjoint Rx(q0)/Rz(q2) commute with every spectator coordinate preserved.')
```
```text
Nonadjacent disjoint Rx(q0)/Rz(q2) commute with every spectator coordinate preserved.
```

<span id="formula-code-5-8-shared"></span>

### 4. Distinguish control-side commutation from target-side propagation

**Formula.** Let $C=CX_{c,t}$. Its projector form is $|0\rangle\langle0|_c\otimes I_t+|1\rangle\langle1|_c\otimes X_t$. It follows that

$$
[C,Z_c]=0,\qquad[C,X_t]=0,\qquad CZ_tC=Z_cZ_t,
$$

where $[A,B]=AB-BA$. Consequently C commutes with $R_z$ on its control and $R_x$ on its target, but moving target $R_z$ through C changes the operator:

$$
C R_{z,t}(\theta)C=R_{ZZ,c,t}(\theta)
:=e^{-i\theta Z_cZ_t/2},\qquad
R_{z,t}(\theta)C=C R_{ZZ,c,t}(\theta).
$$

**Derivation.** Z on c is diagonal in the two control projectors; X on t commutes with both target blocks I and X. Thus both commute with C, and so do their exponential series. To check the third identity, apply the rightmost C to $|a,b\rangle$, apply Z on the updated target $b\oplus a$, then undo C. The resulting sign is $(-1)^{a\oplus b}=(-1)^a(-1)^b$, the sign from $Z_cZ_t$. Conjugating each exponential power establishes the RZZ identity. Multiplication by C on the left gives the second equation since $C^2=I$.

Read the last equality carefully: chronological C,Rz(target) equals chronological RZZ,C. It does not equal chronological Rz(target),C at a generic angle. Sharing a qubit therefore neither automatically forbids commutation nor automatically permits it. In this convention RZZ has diagonal entries $e^{-i\theta/2},e^{i\theta/2},e^{i\theta/2},e^{-i\theta/2}$ on $|00\rangle,|01\rangle,|10\rangle,|11\rangle$.

**FlagQuantum code → verification result.** Released 0.3.1's named `rzz` was actually executed and checked against those entries. Introducing RZZ changes the required gate alphabet; no decrease in a hardware cost is inferred from this algebraic propagation.

```python
cx = ('cx',(0,1),())
for name, q in (('rz', 0), ('rx', 1)):
    gate = (name,(q,),(.31,))
    reference = w.matrix(2, (cx, gate)) @ w.product_input(f2)
    for candidate in ((cx, gate), (gate, cx)):
        v, _ = w.run(w.compile_program(2, candidate), f2)
        torch.testing.assert_close(v, reference, rtol=0, atol=w.ATOL)
rz = ('rz',(1,),(.61,)); rzz = ('rzz',(0,1),(.61,))
reference = w.matrix(2, (cx, rz)) @ w.product_input(f2)
for candidate in ((cx, rz), (rzz, cx)):
    v, _ = w.run(w.compile_program(2, candidate), f2)
    torch.testing.assert_close(v, reference, rtol=0, atol=w.ATOL)
assert not torch.allclose(w.matrix(2,(cx,rz)), w.matrix(2,(rz,cx)), rtol=0, atol=w.ATOL)
print('Control Rz / target Rx commute; target Rz propagates to RZZ, not unchanged Rz.')
```
```text
Control Rz / target Rx commute; target Rz propagates to RZZ, not unchanged Rz.
```

<span id="formula-code-5-8-basis"></span>

### 5. Carry both the axis and angle sign through a basis change

**Formula.** Direct multiplication of the matrices in unit 1 gives

$$
HXH=Z,\qquad HZH=X,\qquad HYH=-Y.
$$

Therefore

$$
H R_x(\theta)H=R_z(\theta),\quad
H R_z(\theta)H=R_x(\theta),\quad
H R_y(\theta)H=R_y(-\theta).
$$

**Derivation.** For example, explicit multiplication gives $HY=\frac{i}{\sqrt2}\begin{pmatrix}1&-1\\-1&-1\end{pmatrix}$ and $YH=-\frac{i}{\sqrt2}\begin{pmatrix}1&-1\\-1&-1\end{pmatrix}$, so $HY=-YH$. Likewise $HX=ZH$ and $HZ=XH$. Multiply each identity by H on the right and use $H^2=I$. Conjugating a power gives $H G^k H=(HGH)^k$, because each pair of intermediate H factors cancels. The exponential series thus satisfies $H e^A H=e^{HAH}$. The Y case changes its Hermitian generator from Y to −Y, which negates θ. Dropping that sign would give the inverse rotation at a generic angle. The chronological H,rotation,H call list has the same palindromic product; no call-order reversal is hidden here.

**FlagQuantum code → verification result.** Test all three axes directly, including the negative Ry angle. The complete program repeats this on both basis inputs and a complex input, at generic, zero and full-turn angles.

```python
for name, out, sign in (('rx','z',1), ('rz','x',1), ('ry','y',-1)):
    block = fq.Circuit(1, dtype=w.D).h(0)
    getattr(block, name)(0, .47)
    block.h(0)
    v, _ = w.run(block, f1)
    reference = w.explicit(out, sign*.47) @ w.product_input(f1)
    torch.testing.assert_close(v, reference, rtol=0, atol=w.ATOL)
print('H-conjugated Rx, Rz and Ry passed; Ry requires the negative angle.')
```
```text
H-conjugated Rx, Rz and Ry passed; Ry requires the negative angle.
```

<span id="formula-code-5-8-noncommuting"></span>

### 6. Turn an invalid axis swap into a measurable counterexample

**Formula.** Since $XZ=-iY$ and $ZX=iY$, expanding the two Pauli rotation formulas yields

$$
R_x(\theta)R_z(\phi)-R_z(\phi)R_x(\theta)
=2i\sin(\theta/2)\sin(\phi/2)Y.
$$

**Derivation.** The identity and single-Pauli terms agree in both products and cancel on subtraction. Their cross terms are $-\sin(\theta/2)\sin(\phi/2)XZ$ and the same scalar times ZX; insert the two products to obtain the displayed difference. At $\theta=\phi=\pi/2$, its operator norm is one. At a zero angle the difference instead vanishes, illustrating why a special passing fixture is not a general commutation rule.

On input $|0\rangle$, chronological Rx(π/2),Rz(π/2) produces $e^{-i\pi/4}|+\rangle$, whereas reversed calls produce $e^{-i\pi/4}(|0\rangle-i|1\rangle)/\sqrt2$. Their computational-basis probabilities agree. Append H to read their phase difference: the first circuit has p(0)=1 and the second p(0)=1/2. Matching those probabilities before the analyzer would miss the invalid rewrite.

**FlagQuantum code → verification result.** Both actual outputs are checked against their separately ordered matrix products, including full phase. The differing analyzer probabilities are expected evidence against the proposed swap, not an execution failure.

```python
h = ('h',(0,),())
first = (('rx',(0,),(math.pi/2,)), ('rz',(0,),(math.pi/2,)), h)
second = (('rz',(0,),(math.pi/2,)), ('rx',(0,),(math.pi/2,)), h)
p0 = []
for candidate in (first, second):
    v, p = w.run(w.compile_program(1, candidate), [(1,0)])
    reference = w.matrix(1, candidate) @ torch.tensor([1,0], dtype=w.D)
    torch.testing.assert_close(v, reference, rtol=0, atol=w.ATOL)
    p0.append(p[0].item())
assert abs(p0[0]-1) < w.ATOL and abs(p0[1]-.5) < w.ATOL
print('Invalid axis-swap analyzer p(0):', *(f'{p:.6f}' for p in p0))
```
```text
Invalid axis-swap analyzer p(0): 1.000000 0.500000
```

<span id="formula-code-5-8-phase"></span>

### 7. Preserve a replacement phase before controlling a block

**Formula.** $R_x(\pi)=-iX$. These are different phase-exact matrices. Controlling the rotation gives

$$
CR_x(\pi)=P_c(-\pi/2)\,CX_{c,t},
$$

rather than bare CNOT.

**Derivation.** On control zero both sides act as identity. On control one, the phase gate contributes $e^{-i\pi/2}=-i$ and CNOT contributes X, matching $R_x(\pi)$. For input $|+,0\rangle$, the native controlled rotation gives $(|00\rangle-i|11\rangle)/\sqrt2$; bare CNOT gives $(|00\rangle+|11\rangle)/\sqrt2$. A further CNOT disentangles the target in each case; H on the control gives p(00)=1/2 and 1 respectively. The compensated CNOT restores the first result. This extends [5.2](#sec-gates-reversible-computation-and-circuit-synthesis-2)'s coherent-control convention to gate replacement.

A whole isolated state may be compared up to a global phase under an explicitly declared ray contract. A reusable controlled subroutine cannot silently inherit that weaker contract. Here every rewrite preserves the full matrix, so no phase alignment is used to accept the wrong candidate.

**FlagQuantum code → verification result.** All three candidate paths run. The complete program also checks native CRx(π) and its compensated replacement on every two-qubit basis input and a complex product.

```python
native = (('crx',(0,1),(math.pi,)),)
wrong = (cx,)
corrected = (('p',(0,),(-math.pi/2,)), cx)
tail = (cx, ('h',(0,),()))
f = [(1/math.sqrt(2),1/math.sqrt(2)), (1,0)]
p00 = []
for candidate in (native, wrong, corrected):
    v, p = w.run(w.compile_program(2, candidate+tail), f)
    torch.testing.assert_close(v, w.matrix(2,candidate+tail) @ w.product_input(f), rtol=0, atol=w.ATOL)
    p00.append(p[0].item())
assert max(abs(p-e) for p,e in zip(p00,(.5,1.,.5))) < w.ATOL
print('Native / bare CX / compensated CX analyzer p(00):', *(f'{p:.6f}' for p in p00))
```
```text
Native / bare CX / compensated CX analyzer p(00): 0.500000 1.000000 0.500000
```

<span id="formula-code-5-8-pass"></span>

### 8. Prove a small safe pass, and state the limits of the proof

**Formula and derivation.** The cancellation pass scans a finite instruction list once, maintaining a stack. Its invariant is that the stack's chronological matrix equals that of the processed input prefix. Initially both are identity. Pushing a gate left-multiplies both matrices by that gate. If the new gate is the adjacent inverse of the stack top on exactly the same ordered support, popping replaces their product by identity. Skipping an exact zero-angle gate also preserves identity. These are all branches, so induction proves the invariant for the complete list. Each iteration consumes one input instruction, hence termination; stack length never exceeds input length. The helper does not attempt a general search or reordering pass.

Its admitted fixed pairs are H/X/Y/Z/CX with themselves and S/S†,T/T† in either order. Rotation, P, CRx and RZZ pairs cancel only for identical gate/support declarations and exactly opposite fixed angles. A small nonzero angle is retained. No approximate `allclose` predicate licenses a rewrite. Numeric nonzero-angle merges in unit 2 are deliberately outside this pass.

If a replacement has full operator identity $A=B$, then $LAR=LBR$ in any surrounding unitary program; the same holds after tensoring with spectators and after coherent control. If instead A and B agree only on an initialized-ancilla subspace, the preceding prefix must place the actual joint input in that subspace at the replacement site. Merely saying that a qubit was clean at program start is insufficient. This pass uses full operator identities and no hidden clean-ancilla assumptions.

The mathematical identities do not assert equality of two noisy gate implementations, pulses, timings or gradients of a dynamically rebound program. These helpers accept fixed numeric radians and reject unknown gate kinds. Tensor/lazy parameters are not detached or evaluated into constants. A hardware optimizer or differentiable rewrite system needs additional contracts. The released nonunitary-adjoint admission boundary recorded in [5.1](#sec-gates-reversible-computation-and-circuit-synthesis-1) remains guarded there; no native fix is claimed here.

**Code → verification result.** The n≤4 bound is a teaching guard shared with the dense independent reference, not a FlagQuantum limit. Unsupported barriers, measurements and reset operations are not reordered or removed; they are outside this abstract unitary language. Check invalid shape/type/support/angle contracts separately from mathematically invalid proposed equivalences.

```python
invalid = [lambda: w.cancellation(0, ()),
           lambda: w.cancellation(2, (('cx',(0,0),()),)),
           lambda: w.compile_program(2, (('cx',(0,2),()),)),
           lambda: w.compile_program(1, (('rz',(0,),(float('nan'),)),)),
           lambda: w.compile_program(1, (('rx',(0,),(True,)),)),
           lambda: w.compile_program(1, (('reset',(0,),()),)),
           lambda: w.cancellation(1, [('h',(0,),())]),
           lambda: w.compile_program(1, (('h',(0,),(1.,)),)),
           lambda: w.compile_program(1, (('ry',(0,),()),)),
           lambda: w.cancellation(2, (('cx',(True,1),()),))]
for call in invalid:
    try:
        call()
    except ValueError:
        pass
    else:
        raise AssertionError('Malformed rewrite contract admitted')
assert w.cancellation(1, (('rz',(0,),(1e-14,)),)) != ()
assert w.RUNS == 21
print('Ten malformed contracts rejected; tiny nonzero angle retained; 21 actual body circuits verified.')
```
```text
Ten malformed contracts rejected; tiny nonzero angle retained; 21 actual body circuits verified.
```

### Complete example and verification results

Run `python examples/foundations/circuit_rewrites.py` from the repository root. The [complete program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/circuit_rewrites.py) runs 355 actual circuits: 110 cancellation-path circuits, 72 merge circuits, 20 disjoint/correlated-input circuits, 75 shared-support/propagation circuits, 54 basis-conjugation circuits, 6 noncommuting-axis circuits and 18 controlled-phase circuits. Equivalent paths are compared with an independent scalar-index matrix, on every basis input and a complex product. The invalid-order/phase candidates are tested against their own correct references, then rejected as equivalences. Their expected disagreement is not recorded as a simulation failure. The actual body checker separately runs all eight cumulative snippets, containing 21 circuits, and compares their printed results exactly.

Expected output of the complete program:

```text
15 cancellation programs: exact inverses, nested pairs, zero/full-turn and ordered-support boundaries passed.
12 same-generator/phase merges: basis and complex vectors checked without modulo-2*pi rotation deletion.
Disjoint supports: all 3-qubit basis/complex inputs plus 2 correlated-input circuits passed.
6 valid shared-support commutations and CX/Rz-to-RZZ propagation passed; unchanged-target-Rz swap rejected by full operators.
9 Hadamard conjugations: axes and the Ry angle sign passed at generic, zero and full-turn angles.
Noncommuting rotations and controlled Rx(pi)-to-X phase witness passed; corrected control phase retained.
355 actual CPU complex128 circuits; full-phase atol 1e-12, rtol 0; 10 malformed contracts rejected.
Conservative book-side cancellation only; no native optimizer, approximate rewrite, gradient, measurement, noise or hardware claim.
```

### Understanding checks and transfer exercises

**5.8-A — A new nested cancellation on a nonadjacent pair.** In a three-qubit register, use chronological H(q2),Rz(q0,−.27),CX(q2,q0),Rx(q1,.83),Rx(q1,−.83),CX(q2,q0),Rz(q0,.27),H(q2). Reduce it and check all eight basis inputs and a complex product. Which support order must be retained?

**5.8-B — Transfer the controlled phase.** Replace CRx(q2,q0,−π) by a phase-compensated CNOT. Derive the sign of the control phase, then verify both paths on all eight basis inputs and a complex product.

**5.8-C — An unsafe tolerance rule.** Why must `Rz(1e-14)` remain under a phase-exact identity contract even if one float comparison says it is close to identity? Can a deliberately approximate rewrite still be useful?

**5.8-D — A reusable proof obligation.** You found a rewrite that works when a workspace is zero. What must be checked before using it after an arbitrary preceding block? Why is comparing the workspace probability alone insufficient?

<details markdown="1">
<summary>Answers and reasoning</summary>

**A.** The Rx pair cancels first, exposing two CX(q2,q0) instructions. They cancel, exposing the opposite Rz angles, which cancel and expose H(q2),H(q2). The final list is empty. Reversing one CNOT's control/target would invalidate that cancellation. The separate author transfer runs the original and empty program on nine inputs: 18 actual circuits.

**B.** $R_x(-\pi)=iX$, so the correction is P(q2,+π/2), followed by CX(q2,q0). The phase belongs on the control q2 and commutes with this CNOT. The separate author transfer compares the native and compensated paths on nine inputs, adding 18 circuits for 36 transfer circuits total. This is author validation, not independent agent review.

**C.** It is not mathematically the identity; repeated use or phase-sensitive surrounding operations can expose the difference. A bounded approximate rewrite may be useful under a separately declared synthesis-error budget, as in 5.7. The acceptance condition must change explicitly, rather than borrowing an implementation `allclose` tolerance as an exact proof.

**D.** The preceding block must map the actual joint input into the promised input subspace at that exact site, including any correlations with retained registers. One must also verify the intended operation on retained information and its phases, not just whether the workspace returns to a particular marginal probability. Full operator equality avoids such a restricted-input obligation; a subspace identity does not.

</details>

### Chapter synthesis, sources and next step

Chapter 5 has connected call order and inversion, coherent controls, reversible embeddings and workspace reuse, exact universality, selected decompositions, approximation budgets and safe identities. A replacement can now be judged by its full operator contract, permitted alphabet, phase, support, input-subspace assumptions and error budget. Eight working drafts do not constitute independent chapter acceptance.

Depth **F**: the displayed cancellation, generator, support, conjugation and controlled-phase identities are proved explicitly, and the finite cancellation pass has an invariant and termination proof. Assigned background is Nielsen and Chuang, 10th Anniversary Edition (2010), §§4.2–4.3. These assigned locators are retained; no fresh inspection of the user-local textbook PDF is claimed. Released named gate behavior, including CRx and RZZ half-angle conventions, was checked by actual execution and source provenance. The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/5.8.json) separates author checks from independent mathematical/implementation review and reader trials, which remain pending.

Continue with [6.1 Measurement outcomes and the Born rule](ch-measurement-expectation-values-and-statistical-estimation.md#sec-measurement-expectation-values-and-statistical-estimation-1).

<!-- end-section-5.8 -->
