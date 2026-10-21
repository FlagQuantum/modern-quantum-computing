# 5. Gates, Reversible Computation, and Circuit Synthesis

**Working draft: section 5.1 · Writing Baseline 1.0 · October 21, 2026.** Author execution is separate from independent mathematical, implementation and reader review, which remain pending. Examples use installed released FlagQuantum 0.3.1 and PyTorch 2.13.0 on CPU with complex128 statevectors.

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

The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/5.1.json) separates author execution, the preserved failure and subsequent passing checks from pending independent mathematical, implementation and reader reviews. This remains a working draft. Continue, when drafted, with [5.2 Controlled operations and ancillas](../section-plans/01-foundations.md#sec-gates-reversible-computation-and-circuit-synthesis-2).
