# 14. Computational Models, Complexity, and Quantum Advantage

**Working drafts: sections 14.1–14.8 · Writing Baseline 1.0 · November 2, 2026.** The B 02 writing queue reaches this chapter after Chapter 8; Chapters 9–13 retain their own later scheduled batches. Author checks are separate from independent mathematical/implementation review and reader trial, which remain pending.

<span id="sec-computational-models-complexity-and-quantum-advantage-1"></span>
## 14.1 Problems, input length, and computational models

**Question.** When an algorithm uses resources that grow with its input, what is the input, and what does its size mean?

The prerequisites are [5.3, reversible classical logic](ch-gates-reversible-computation-and-circuit-synthesis.md#sec-gates-reversible-computation-and-circuit-synthesis-3) and [6.6, exact probabilities and samples](ch-measurement-expectation-values-and-statistical-estimation.md#sec-measurement-expectation-values-and-statistical-estimation-6). This P-depth section establishes definitions and modeling conventions, then derives a small example under them. It does not assert a separation between classical and quantum computational power. Bits, gate counts and amplitudes here are dimensionless; no physical execution time is inferred from a gate count.

### 14.1.1 Specify an encoding before naming an input size

Let Σ={0, 1} be the binary alphabet. A string x=x₀…xₙ₋₁ has length |x|=n; Σ* denotes all finite strings, including the empty string ε of length zero. An **encoding** is the declared rule by which such a string represents an object. For a nonempty unsigned binary numeral, the numerical value is

$$
m(x)=\sum_{j=0}^{n-1}x_j2^{n-1-j}.
$$

A canonical representation has no leading zeros except the single string `0`. For m≥1 its canonical length is floor(log₂m)+1: an n-bit canonical numeral has leading bit one, so 2ⁿ⁻¹≤m≤2ⁿ−1, and conversely that interval determines n. We assign canonical length one to zero. These are integer statements; the code uses exact integer arithmetic rather than floating-point logarithms.

The numeral `10000000000` has value 1024 but length 11. Reading a string of length n and iterating m times are different costs. The equality m=2ⁿ⁻¹ for a power-of-two input shows why a loop polynomial in a numerical value need not be polynomial in its bitlength. Padding changes the representation length even when it preserves the represented value.

```python
import torch,flagquantum as fq
from examples.foundations import input_models as m,statistical_ensembles as e
value,length=m.binary('10000000000')
assert value==1024 and length==11
assert m.binary('0001')==(1,4)
print('10000000000:value1024,length11;0001:value1,length4')
```

```text
10000000000:value1024,length11;0001:value1,length4
```

The parser deliberately accepts leading-zero numerals and reports their **actual** length. It rejects an empty numeral; the empty string will still be a valid input for the parity problem below. A format contract is part of the problem, not a cosmetic choice made after timing an algorithm.

### 14.1.2 Define a computational problem as a family of instances

A decision problem asks a yes/no question for every allowed encoded input. A language L⊆Σ* is the set of yes-inputs; its decision function has value 1 on L and 0 elsewhere. A function problem instead requests a specified output string f(x). A promise problem specifies disjoint yes/no sets and only demands correctness on their union. If a promise is used, it must be stated rather than treating a convenient test set as the whole domain.

Our example has no promise: on every binary string define

$$
f(x)=\left(\sum_{j=0}^{n-1}x_j\right)\bmod2,
\qquad f(\varepsilon)=0.
$$

Its associated language L_odd contains the strings with an odd number of 1 digits. This is parity of the **digits**, not oddness of an integer encoded by those digits. One three-bit experiment is an instance; the problem also includes every other length and every other input at those lengths.

```python
x='11';bits=m.word_bits(x)
assert sum(bits)%2==0 and int(x,2)%2==1
print('Parity of the input digits is0;oddness of the encoded integer is1')
```

```text
Parity of the input digits is0;oddness of the encoded integer is1
```

A complete specification includes the domain/encoding, required output or error criterion, and access model. “Process an integer, ” “produce a quantum state” or “return a useful answer” is incomplete until the representation and the requested observable/output are defined. A quantum state as input would require a different access description from the classical strings used here.

### 14.1.3 Declare a model and a uniform circuit family

A computational model specifies allowed configurations, elementary operations, initialization and input access, output rules, and what resources are counted. For a deterministic classical bit algorithm these might be tape steps or bit operations. For a randomized model there is also a random source. In a quantum circuit model there are qubit registers, an allowed gate alphabet or precision convention, and measurement rules. A machine step, a circuit gate and a simulator instruction are not interchangeable units by definition.

We choose a finite exact gate alphabet {X, CX} for this example, computational-basis classical input, one initialized target qubit, and terminal computational-basis output. This gate subset suffices for parity; we do not call it universal. For each n, the **kernel circuit** C_n consists of CX(j, n) for j=0, …, n−1, with data qubits q 0, …, q(n−1) and target qn. Its topology depends on n, not on the bits of x.

A family {C_n} is **polynomial-time uniform** in the convention used here when one fixed deterministic classical procedure, on unary input 1ⁿ, outputs an explicit description of C_n in time polynomial in n. Unary 1ⁿ is an indexing convention for the generator, not the original problem input x. Without a generation condition, an arbitrary circuit chosen separately at each length could hide unaccounted information in its design.

Our generator loops through n controls and emits two qubit labels per CX. With explicit binary labels, each label uses O(log(n+1))bits for n≥1; separators and gate identifiers have fixed size. The whole description is therefore O(n log(n+1))bits and is constructible within a polynomial bit-operation bound by this loop. The empty-length circuit has one target and no gates. This establishes the uniform construction for the mathematical family; the Python generator imposes a finite teaching guard rather than claiming execution at arbitrary n.

```python
assert m.family(3)==((0,3),(1,3),(2,3))
assert m.family(0)==()
print('One length3kernel:CX(0,3),CX(1,3),CX(2,3);length0kernel has no gates')
```

```text
One length3kernel:CX(0,3),CX(1,3),CX(2,3);length0kernel has no gates
```

If the generator receives binary n instead, its input has only O(log n)bits, and even writing n gate records can take time exponential in that indexing length. There is no contradiction:uniformity was explicitly parameterized by n via 1ⁿ. We do not hide an exponentially long gate list inside a short compressed encoding and then count it as a constant-cost gate.

### 14.1.4 Derive and execute the reversible computation

Let y be the initial target bit. CX(j, n) leaves every data bit unchanged and toggles y by x_j. After the first k calls, the target is y XOR x₀ XOR … XOR xₖ₋₁. Induction on k proves

$$
C_n|x,y\rangle=|x,y\mathbin{\mathrm{XOR}}f(x)\rangle.
$$

The base case k=0 has no toggles; the next CX appends exactly the next XOR. At k=n this is the required map. It is bijective and self-inverse because applying the same parity toggle twice adds zero modulo 2. This is the reversible embedding of 5.3, not an irreversible erasure of x. For target 0, the terminal target probability is exactly concentrated on f(x) in the ideal model.

The next unit explicitly prepares input 101, executes the generated kernel and asks the actual FlagQuantum runtime for probabilities and terminal samples. There is no oracle whose implementation cost has been assumed away.

```python
x='101';n=len(x)
c=fq.Circuit(n+1,dtype=m.D).X(0).X(2)
for control,target in m.family(n):c.CX(control,target)
r=fq.run(c,outputs=[fq.probabilities(qubits=(n,),name='answer'),
 fq.samples(qubits=(n,),name='record')],shots=7,options=e.OPTIONS)
e.close(r.measurement('answer').value[0],torch.tensor([1.,0.],dtype=torch.float64))
assert bool((r.measurement('record').value==0).all())
print('Input101:exact answer probabilities[1,0];seven terminal records all0')
```

```text
Input101:exact answer probabilities[1,0];seven terminal records all0
```

The seven identical records are expected for this deterministic ideal output. They are not a statistical confidence certificate or evidence that every quantum algorithm has deterministic outputs. General sampling conventions remain those of 6.6.

### 14.1.5 Validate the whole family contract, not one lucky instance

A circuit that always returns 0 would succeed on input 101, y=0, but fail on many other inputs. Testing the opposite target bit checks the reversible map rather than only its answer on a zero-initialized target. The full-register probability reference also checks that data bits remain unchanged.

```python
reverse,counts=m.execute('101',1,mode='density_matrix')
e.close(reverse.measurement('answer').value[0],torch.tensor([0.,1.],dtype=torch.float64))
print('Same kernel with target1returns1;data bits are unchanged in the full probability check')
```

```text
Same kernel with target1returns1;data bits are unchanged in the full probability check
```

For n data qubits the full output basis index, in our q 0-most-significant convention, is 2 m(x)+(y XOR f(x)); for the empty input m is taken as 0 only for this indexing formula. The independent reference computes f by a scalar sum modulo 2, then places probability one at that index. No native probability is reused to manufacture the reference. The complete program enumerates all strings of lengths 0–4, both target bits and both tested modes. Such tests validate the implementation over that finite domain; the induction above proves the unrestricted circuit identity.

### 14.1.6 Keep loading and output costs visible

The kernel uses exactly n CX gates and n+1 qubits. Preparing a particular basis input from all zeros adds wt(x)=Σ_jx_j X gates. A target initially equal to 1 adds one further X. Thus

$$
G_{\mathrm{kernel}}(n)=n,\qquad
G_{\mathrm{total}}(x,y)=n+\operatorname{wt}(x)+y.
$$

The helper's resource dictionary reports zero-target loading costs; the y=1 experiment separately includes its initialization gate. All CX gates share one target. If the abstract schedule permits only disjoint gates in a time layer, this serial kernel has n CX layers; no physical gate durations or routing schedule are supplied. A different synthesis or target architecture would require a new resource analysis.

```python
cost=m.resources('101')
assert (cost['CX_kernel'],cost['X_loading'],cost['gates_with_loading'])==(3,2,5)
assert cost['data_qubits']+cost['target_qubits']==4
print('Input101:3kernelCX+2loadingX=5gates;4qubits')
```

```text
Input101:3kernelCX+2loadingX=5gates;4qubits
```

A classical running-XOR algorithm computes the same f by reading bits sequentially, updating one accumulator and returning that bit. The existence of a quantum implementation here is not a quantum advantage claim. It makes the input, output and resource accounting concrete. Reading the string, generating its preparation gates, executing the kernel and recording the answer are separate steps of the full workflow.

### 14.1.7 Distinguish a quantum register from its classical simulation

For n+1 qubits, a dense pure-state simulator stores 2ⁿ⁺¹ complex amplitudes. A dense density representation stores 4ⁿ⁺¹ complex entries. These dimensions follow by counting basis strings and ordered pairs of basis strings, respectively; they are not the number of physical qubits. At n=3 the counts are 16 and 256, while the abstract circuit has 4 qubits and 3 kernel gates.

```python
cost=m.resources('101')
assert cost['statevector_entries']==16 and cost['density_entries']==256
assert len(m.family(257))==257
print('Four-qubit host representations:16complex amplitudes or256density entries')
print('Length257gate list generated on host only;no257qubit experiment claimed')
```

```text
Four-qubit host representations:16complex amplitudes or256density entries
Length257gate list generated on host only;no257qubit experiment claimed
```

The dictionary's array sizes are representation counts, not a measured memory allocation or a promise about a particular backend's internal optimization. Timing `fq.run` would measure host simulation, compilation and other runtime overheads on this setup. It would not directly measure the abstract quantum computation's physical execution time. Conversely, an exponentially large dense reference vector does not imply that the physical circuit has exponentially many qubits.

Formal complexity comparisons require the same encoded task and a declared model/resource convention. A unit-cost arithmetic operation on an unbounded integer, an arbitrary-precision real rotation, or a lookup table containing all answers would each need its own accounting; none is silently assumed here. Definitions of complexity classes and reductions are developed in the following scheduled sections.

### 14.1.8 State limits and test edge cases

```python
empty,_=m.execute('',0)
e.close(empty.measurement('answer').value[0],torch.tensor([1.,0.],dtype=torch.float64))
assert m.invalid_checks()==9
assert m.RUNS==2
print('Empty parity input returns0on one target qubit;9malformed contracts rejected')
print('Body executed2helper-native calls plus1explicit fq.run')
```

```text
Empty parity input returns0on one target qubit;9malformed contracts rejected
Body executed2helper-native calls plus1explicit fq.run
```

The executable [input_models.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/input_models.py) runs 124 actual circuits:31 strings across lengths 0–4, two target values and two execution modes. The eight cumulative body units execute three circuits, including the explicit native call. The complete program also checks exact integer encodings and host gate-list construction up to 1000 controls, without executing those large circuits.

We tested Python 3.12.14, released FlagQuantum 0.3.1 and Torch 2.13.0 on CPU complex128. Real API calls are `Circuit`, `X`, `CX`, `run`, named `probabilities` and terminal `samples`; density-matrix mode is requested by the runtime option. The samples are returned as integer rows with the selected target column. Deterministic probability comparisons use absolute tolerance 10⁻¹², relative tolerance 0; integer and gate-list checks use exact equality. No normalization repair or phase alignment is used.

The Python generator's maximum n=10000 and native example's n≤4 are teaching guards, not FlagQuantum capacity limits. There is no native complexity-class verifier, uniformity prover, resource estimator or hardware timing endpoint in this example:the generator, resource dictionary, scalar reference and mathematical analysis are book code. Terminal sampling does not claim mid-circuit collapse, reset, hardware execution or an oracle that supplies an answer for free. The absence of rotations also avoids importing an arbitrary-precision gate convention into the parity example.

Expected output of the complete program:

```text
124 actual native circuits:all31binary inputs of lengths0..4,two target bits,two execution modes passed.
Exact integer bitlength/padding and bounded uniform gate-list construction passed;no large circuit executed.
9 malformed input/model contracts rejected before native execution.
Parity kernel uses n CX gates and n+1qubits;input loading and simulator arrays are recorded separately.
```

**Problems and transfer.**

- **14.1-A — encoding.** Compare the value and actual length of `001000` and `1000`. For the canonical numeral representing 2⁶³, what are value, length and the number of iterations in a loop that counts to that value?
- **14.1-B — definition.** For strings `1110` and `1001`, compute digit parity and numerical oddness. Which language does the circuit decide? Does changing leading-zero padding change digit parity?
- **14.1-C — execution.** Run both strings with y=0 and 1 in both execution modes. Check full basis probabilities, raw target records and gate counts, including the extra target-loading X when y=1.
- **14.1-D — uniformity and simulation.** Generate the length 513 kernel on the host without running it. Explain why this does not test 513 qubits. What changes when generator length is encoded in binary instead of unary? Why is a dense simulation time not a physical quantum speedup measurement?

<details markdown="1">
<summary>Answers and verification guidance for 14.1-A–D</summary>

**A.** Both numerals represent 8, but actual lengths are 6 and 4. The value 2⁶³ is 9223372036854775808 and its canonical binary length is 64. A loop with one iteration per value unit would use 2⁶³ iterations, despite a 64 bit input; the bitlength/parser checks do not run that loop.

**B.** `1110` has digit parity 1 but represents the even integer 14. `1001` has digit parity 0 but represents the odd integer 9. The circuit decides the language of odd digit parity, not integer oddness. Adding leading zeros preserves digit parity but increases actual encoded length.

**C.** With zero target, the answers are 1 and 0; with target 1 they are 0 and 1. The full output preserves x and changes only y by its parity. Four data qubits plus one target require five qubits. Kernel cost is 4 CX; loading costs are 3 and 2 data X gates, respectively, and y=1 adds one target X. Fresh transfer executes all eight circuits.

**D.** The generated list has 513 CX descriptions, all targeting label 513. It is a classical description of a 514 qubit circuit, not an executed register. Unary indexing has 513 symbols; binary 513 has 10 bits, and writing 513 records still takes 513 output steps at minimum. The claimed polynomial uniformity is in the unary index length. A dense simulator represents the whole joint state with exponentially many entries and runs on a classical host, so its wall time is not a physical circuit runtime or a quantum/classical speedup certificate.

</details>

Frozen source targets are NC §§3.1.1 and 3.2.1 (contents locators printed 122 and 136; no new full-text review claimed). The uniform circuit-description convention was checked against [Watrous, *Quantum Computational Complexity*, §IV.1, Definition 2, printed 12](https://cs.uwaterloo.ca/~watrous/Papers/QuantumComputationalComplexity.pdf#page=12). The parity derivation and resource accounting are supplied here; no theorem asserting a complexity separation is imported. This is an author-verified working draft; independent mathematical/implementation review, reader trial and formal acceptance remain pending.

<!-- end-section-14.1 -->

<span id="sec-computational-models-complexity-and-quantum-advantage-2"></span>
## 14.2 Reversible computation and uniform circuit families

**Question.** Given an explicitly described classical Boolean circuit, can we construct a reversible circuit that computes its outputs, preserves its inputs and returns all temporary qubits to zero? If a single algorithm generates the classical circuit family, does the construction preserve that uniformity?

The prerequisites are [5.4, uncomputation and reusable workspace](ch-gates-reversible-computation-and-circuit-synthesis.md#sec-gates-reversible-computation-and-circuit-synthesis-4), and [14.1, encoded inputs and uniform circuit families](#sec-computational-models-complexity-and-quantum-advantage-1). This section has depth **F**: we give the construction, its input-subspace proof and the gate/space and uniformity bounds. We simulate a declared finite classical circuit, not an arbitrary classical machine without a circuit-generation theorem. All counts below are logical counts, not energy or hardware timing predictions.

### 14.2.1 Specify the classical circuit and its dependency order

There are n classical input bits x=(x₀, …, xₙ₋₁), L internal nodes and m output taps. We take n and L to be nonnegative integers and m to be a positive integer. Each internal node has one output bit and one of the operations NOT, AND, XOR, COPY, ZERO or ONE. The last two generate constant bits. We assume the nodes are listed in a topological order: node j has output label n+j, and may read only input labels or node labels strictly earlier than n+j. An output tap selects any available input or node label; the same label may be selected more than once.

This is a bounded-fan-in Boolean circuit representation, not a truth table of the whole function. Repeated use of a source is allowed. If another fixed finite bounded-fan-in Boolean gate alphabet is supplied, each gate can be expanded into a constant-size AND/NOT network by its fixed truth table and De Morgan's law; the constant may depend on the chosen gate alphabet. No constant overhead is asserted for gates with unbounded fan-in. We henceforth count L after this declared normalization.

Let z_j(x) be node j's value and z(x) their L-bit list. The m selected values define f(x). A scalar evaluator processes the list from left to right. For example, two nodes implement NAND: node 2=x₀ AND x₁ and node 3=NOT node 2. The output tap is label 3.

```python
import torch,flagquantum as fq
from examples.foundations import uniform_reversible as u,statistical_ensembles as e
nodes=(('AND',(0,1)),('NOT',(2,)))
outputs=(3,)
f,work=u.evaluate((1,0),nodes,outputs)
assert f==(1,) and work==(0,1)
print('Classical NAND:input10,gates(AND,NOT),stored intermediates01,output1')
```

```text
Classical NAND:input10,gates(AND,NOT),stored intermediates01,output1
```

A future-reference, wrong arity or nonexistent output tap is a malformed circuit description. Uniform generation cannot be assessed until this representation is fixed. The code's finite size guards are stated below; the theorem itself applies to any finite n, L and m with valid labels.

### 14.2.2 Translate each classical node into a reversible write

Allocate data X with n qubits, workspace W with one initially zero qubit per node, and output Y with m qubits. These register names denote roles, not extra operations. Node j writes to fresh target t=n+j. On basis states, its small reversible block changes t to t XOR g_j while preserving all source bits:

| Classical operation | Actual compute calls on fresh t | Logical cost |
| --- | --- | --- |
| NOT(a) | X(t), then CX(a, t) | 2 |
| AND(a, b), distinct labels | CCX(a, b, t) | 1 |
| XOR(a, b), distinct labels | CX(a, t), then CX(b, t) | 2 |
| COPY(a) | CX(a, t) | 1 |
| ZERO | no call | 0 |
| ONE | X(t) | 1 |

If AND reads the same source twice, a AND a=a, so use CX rather than a CCX with duplicate controls. If XOR reads the same source twice, its value is zero, so emit no call. These simplifications preserve the classical semantics and the distinct-qubit contract of native gates.

For each listed block, substituting t=0 gives the intended classical node bit. The block is nevertheless a permutation for arbitrary t; it is not an irreversible assignment. Let G be the number of emitted compute gates, counted in the declared {X, CX, CCX} alphabet. Every node costs at most two, hence G≤2 L. The gate alphabet is fixed and exact for this construction; counting a CCX as one is part of this logical model, not a hardware CNOT-cost estimate.

```python
net,cost=u.translate(2,nodes,outputs)
assert cost['compute_gates']==3 and cost['network_gates']==7
assert cost['qubits']==5 and cost['workspace']==2
print('Compute3gates+copy1+inverse3=7gates;2data+2workspace+1output=5qubits')
```

```text
Compute3gates+copy1+inverse3=7gates;2data+2workspace+1output=5qubits
```

**Check.** Why is NOT emitted as X(t) followed by CX(a, t), rather than NOT on the original source? The latter would change data used by later nodes. The fresh-target write preserves both the input and the previously stored intermediate values.

### 14.2.3 Prove the compute invariant and the clean result

Let C_j be the reversible compute prefix for the first j classical nodes. We claim

$$
C_j|x,0^L\rangle
=|x,z_0(x),\ldots,z_{j-1}(x),0^{L-j}\rangle.
$$

For j=0 this is initialization. Assume it for j. The next node's sources are among the unchanged input bits and the first j stored workspace values, so the induction hypothesis supplies exactly its classical arguments. Its fresh target is still zero, and the preceding table writes z_j(x) without changing those sources. This establishes the invariant for j+1. At j=L, C=C_L stores the full intermediate list z(x).

Next apply m CX gates, one from each output tap to its distinct output qubit. Call this block B. With arbitrary initial output string y, it maps y to y XOR f(x), while leaving X and W unchanged. Finally apply C† to XW, in reverse primitive-call order. X, CX and CCX are each their own adjoint, so reversing the emitted compute list implements the inverse exactly. For example, the inverse of the NOT-write block has CX before X; reversing node order alone while retaining every node's original internal order would not in general suffice.

The full circuit U=C†BC, in right-to-left matrix order, therefore satisfies

$$
\begin{aligned}
U|x,0^L,y\rangle
&=C^\dagger|x,z(x),y\mathbin{\mathrm{XOR}}f(x)\rangle\\
&=|x,0^L,y\mathbin{\mathrm{XOR}}f(x)\rangle.
\end{aligned}
$$

The inverse works because the copy block does not alter any input to C†. We inverse **only compute**, not the whole used computation: inverting B as well would erase the wanted output. This proves the claimed clean embedding for every basis x and y. Here is the NAND network expanded into actual native calls, including its inverse and named output request.

```python
# Direct actual gate calls for the translated NAND network;target starts0.
c=fq.Circuit(5,dtype=u.D).X(0)
c.CCX(0,1,2).X(3).CX(2,3).CX(3,4)
c.CX(2,3).X(3).CCX(0,1,2)
r=fq.run(c,outputs=[fq.probabilities(name='full')],options=e.OPTIONS)
expected=torch.zeros(32,dtype=torch.float64);expected[17]=1
# Output basis string10001:data10,workspace00,output1.
e.close(r.measurement('full').value[0],expected)
print('Explicit native NAND:all probability on10001;workspace00anddata10retained')
```

```text
Explicit native NAND:all probability on10001;workspace00anddata10retained
```

### 14.2.4 Extend the result to correlated quantum inputs

Because every primitive is a linear unitary and the basis equality has exact coefficient +1, the same U acts on an arbitrary normalized joint input as

$$
\sum_{x,y}\alpha_{xy}|x,0^L,y\rangle
\quad\longmapsto\quad
\sum_{x,y}\alpha_{xy}|x,0^L,y\mathbin{\mathrm{XOR}}f(x)\rangle.
$$

No amplitude is conjugated or given a branch-dependent phase. If a further reference register is present, expand its basis too and apply the same identity to each reference coefficient; U acts as the identity on that register. Since W is exactly zero in every term on the right, it factors as a clean zero state even if the retained data and output remain correlated. This is the zero-input workspace contract of 5.4, now proved for the whole translated family.

```python
coherent,cc,leak=u.execute(2,nodes,outputs,coherent=True)
assert abs(leak)<1e-12
print('Complex correlated data/output input:full amplitudes and joint density match the clean XOR embedding')
```

```text
Complex correlated data/output input:full amplitudes and joint density match the clean XOR embedding
```

The example prepares complex correlated data/output amplitudes using RY, P and CX, then compares the full native density to an independent amplitude permutation. In statevector mode it also compares the complete statevector without phase alignment. In density-matrix mode, the full projector tests all relative coherences but cannot distinguish a global phase. The phase-sensitive claim for the theorem comes from the basis-level permutation proof, not from a density comparison alone.

“Copy output” means XORing computational-basis values into Y. It does not clone an arbitrary unknown quantum vector: for a superposition of distinct classical outputs it can create correlations. It also does not require y=0; preserving a nonzero output string by XOR is essential to a reversible function embedding.

### 14.2.5 Track the exact logical overhead

The compute list has G gates, the copy block m, and the reverse list G again. With n data qubits, L work qubits and m output qubits,

$$
\begin{gathered}
N_{\mathrm{qubits}}=n+L+m,\\
N_{\mathrm{network}}=2G+m\leq4L+m.
\end{gathered}
$$

These counts exclude preparation of x and y, readout and any hardware routing or decomposition. Basis loading from all zeros adds wt(x)+wt(y) X gates. A specified decomposition of CCX into another fixed finite gate alphabet would multiply its logical contribution by a constant, but that cost must be stated for that different model. We make no minimal-gate or minimal-space claim. One qubit per node stores the entire classical computation history, including constants and outputs already tapped from input; it is a simple sufficient construction.

```python
adder=(('XOR',(0,1)),('AND',(0,1)))
hr,hc,hl=u.execute(2,adder,(2,3),x=(1,1),y=(1,0),mode='density_matrix')
assert hc['network_gates']==8 and hr.measurement('p').value[0,51].item()==1
print('Half-adder:input11,oldoutput10,newoutput11,workspace00;8network gates')
```

```text
Half-adder:input11,oldoutput10,newoutput11,workspace00;8network gates
```

This two-output half-adder shows why output width m belongs in both resource formulas. Repeated output taps also work: they control different fresh Y qubits, so each is a separately counted CX. An output copied directly from X needs no new internal node; the complete program includes an L=0 direct-tap case. Such cases are not reasons to drop the initialization contract for the workspace that is actually used.

### 14.2.6 Prove that the compiler preserves uniformity

Suppose a single deterministic classical generator, on unary input 1ⁿ, produces an explicit topologically ordered classical description D_n in time polynomial in n. Because writing the output takes time, L(n) and m(n) are polynomially bounded for an explicit, uncompressed description. Our reversible translator makes a finite scan of the nodes and output taps, chooses one of the fixed table entries, assigns fresh labels n+j, and emits compute, copy and reversed compute lists. It never evaluates a truth table over all 2ⁿinputs and never queries f(x) to decide the topology.

All emitted qubit labels lie below n+L+m. Binary labels therefore require O(log(n+L+m+1)) bits each. There are at most 4 L+m constant-arity gate records. Storing, reversing and printing these records, and checking valid labels, require polynomial bit-operation time in n plus the length of D_n. Composing the classical family generator with this fixed translator is thus polynomial time in n. This supplies one uniform reversible family with polynomial gate and qubit overhead. If the original classical family is merely specified separately at each length with no uniform generator, the translation does **not** create uniformity from nothing.

```python
alias=(('XOR',(0,0)),('AND',(0,0)))
ar,ac,al=u.execute(1,alias,(1,2),x=(1,),y=(1,0))
assert ac['compute_gates']==1 and ac['network_gates']==4
assert all(len(set(q))==len(q)for _,q in u.translate(1,alias,(1,2))[0])
print('Repeated XOR cancels;repeated AND becomes COPY;no duplicate CCXcontrol submitted')
```

```text
Repeated XOR cancels;repeated AND becomes COPY;no duplicate CCXcontrol submitted
```

The repeated-input case above tests the table's alias handling. A separate host generator constructs a running-XOR classical graph for each n; translation then produces its clean reversible network. This is a family-generation example, not an enumeration of every Boolean function. The n=0 family has a ZERO node and the n=1 family taps its input directly, so their finite edge cases remain within the same contract.

### 14.2.7 Verify reusable workspace and identify failed cleanups

The clean map preserves x, so applying the same U a second time toggles its output by the same f(x) again. Since f XOR f=0, the second call returns the original joint XY vector and again leaves W=0. This follows for arbitrary correlated XY input by the linear identity already proved. Returning W to a product zero state also supplies the input condition needed by any subsequent correctly specified computation on the same workspace; there is no need to discard or physically reset W between clean calls.

```python
reuse,rc,rl=u.execute(2,nodes,outputs,coherent=True,cycles=2)
assert abs(rl)<1e-12
for n in (0,1,5,17):
 graph,taps=u.parity_family(n)
 assert u.evaluate((1,)*n,graph,taps)[0]==(n%2,)
print('Two clean calls cancel their output XOR while restoring workspace each time')
print('One host algorithm generates parity graphs including lengths0and1;large graphs not executed')
```

```text
Two clean calls cancel their output XOR while restoring workspace each time
One host algorithm generates parity graphs including lengths0and1;large graphs not executed
```

If the inverse compute is omitted, the answer bits may still be correct while the workspace is not reusable. For x=11 in a one-node AND computation, compute-copy leaves the full basis string 1111: data 11, workspace 1 and output 1. It must fail the zero-workspace contract even though the function output is correct. The helper below runs that deliberate counterexample; it does not count its expected rejection as an unexpected runtime failure.

```python
bad=u.fault()
assert bad.probabilities[0,15].item()==1
assert u.invalid_checks()==10 and u.RUNS==5
print('Missing inverse on input11leaves1111:answer correct but workspace dirty;candidate rejected')
print('10malformed contracts rejected;body uses5helper-native calls plus1explicit fq.run')
```

```text
Missing inverse on input11leaves1111:answer correct but workspace dirty;candidate rejected
10malformed contracts rejected;body uses5helper-native calls plus1explicit fq.run
```

Other invalid transformations include changing X before the inverse, using unknown nonzero workspace as if it were clean, or reversing only a convenient part of compute. The proof's invariant names the exact sources and initial zeros; it makes no promise for such changed preconditions. Checking output probabilities alone is insufficient. We check the full joint density and the probability of the **joint** event that any workspace bit is 1, rather than multiplying separate marginal zero probabilities.

For full-register basis probabilities p(x,w,y), the reported workspace leakage is the single event

$$
\ell=\sum_{x,y}\sum_{w\neq0^L}p(x,w,y).
$$

The helper sums those full-register entries directly; no independence of workspace bits is assumed. An empty workspace has leakage zero by the empty-event convention.

### 14.2.8 Preserve the execution and modeling boundaries

The companion [uniform_reversible.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/uniform_reversible.py) executes 118 actual CPU complex128 circuits:104 basis cases covering arbitrary output bits, 10 complex joint-input cases, 2 clean reuse cases and 2 deliberately omitted inverse cases. Both statevector and density-matrix modes are used. The eight body units execute 6 circuits, including the explicit NAND program. The scalar classical evaluator supplies f and intermediate values independently of native IR or returned probabilities; the coherent reference applies the declared XY permutation to separately calculated complex amplitudes.

Tested versions are Python 3.12.14, released FlagQuantum 0.3.1 and Torch 2.13.0. Actual native APIs used are X, CX, CCX, RY, P, `run`, named full `density_matrix` and `probabilities`, plus statevector retrieval in its supported execution mode. The gate-list translator, graph validator, cost accounting and reference evaluator are book code, not a native Boolean compiler, uniformity prover or hardware estimator. The inverse is built by reversing a list of self-adjoint primitive gates; this example does not rely on or assert a fix to any separate `Circuit.adjoint` admission issue.

Host guards are n≤32, L≤64 and m≤16; native examples additionally require total qubits≤8. They are teaching memory/description bounds, not FlagQuantum capacity limits. Host-generated longer graphs are not large-system execution evidence. Deterministic implementation comparisons use absolute tolerance 10⁻¹² and relative tolerance 0, with no clipping, normalization repair or phase alignment. No hardware execution, reset, energy-dissipation bound, optimal reversible simulation or quantum speedup is claimed. A theoretical reversible map does not by itself specify the thermodynamic cost of a physical implementation.

Expected output of the complete program:

```text
118actual native circuits:104basis cases,10complex joint-input cases,2workspace reuse cases and2deliberate missing-uncompute cases passed.
Host parity-family generation/evaluation for lengths0..32passed;no large native execution claimed.
10 malformed graph/input contracts rejected;gate bound2G+m<=4L+m checked.
```

**Problems and transfer.**

- **14.2-A — invariant.** State the compute invariant for a circuit with three nodes. Why does using a future node label make both classical evaluation and the induction invalid? Derive the clean embedding for an arbitrary old output y rather than only y=0.
- **14.2-B — cost.** Suppose a normalized Boolean circuit has L=100 nodes and m=3 outputs. Give the construction's workspace, total qubits in terms of n, and gate upper bound. Which costs are absent from that bound? Does it establish an optimal-space reversible simulation?
- **14.2-C — fresh implementation.** Use three input bits and the graph node 3=x₀ XOR x₁, node 4=node 3 AND x₂, with output tap 4. Test x=101 and 111, both old output bits and both execution modes. Then test a complex correlated input on the data and output. Verify the full state and joint workspace-zero event.
- **14.2-D — failure and uniformity.** Explain the dirty workspace in the omitted-inverse AND example. Can a translator that receives an arbitrary nonuniform family claim a uniform family merely because its own per-circuit translation is efficient? Identify the required generator assumption.

<details markdown="1">
<summary>Answers and verification guidance for 14.2-A–D</summary>

**A.** After j nodes, the data remain x, the first j work bits equal their classical values, and the remaining work bits are zero. A future label has no defined earlier value and violates the fresh-write/topological premise. Copy XORs f(x) into y; reversing compute leaves the selected output untouched because compute acts only on XW.

**B.** Workspace is 100 qubits; total is n+103. Since G≤200, the network has at most 403 logical gates in the declared X/CX/CCX alphabet. Input/output loading, readout, decomposition, routing and physical timing are excluded. Retaining one bit for every node is a sufficient construction, not a space-optimal one.

**C.** The function is (x₀ XOR x₁) AND x₂. It gives 1 on 101 and 0 on 111; a target initially 1 receives the complementary answers. There are 3 data, 2 work and 1 output qubits. Compute uses 2 CX for XOR and 1 CCX for AND, so G=3 and the clean network uses 7 gates. Every basis result retains the data and returns work 00. The fresh transfer also compares full complex joint amplitudes/densities in both modes, rather than only these classical outputs.

**D.** Without inverse compute, the stored AND bit remains 1 and may carry correlations on a superposition. Correct output alone is insufficient. Uniformity requires one efficient generator for the source classical family on 1ⁿ; composing it with the translator yields the uniform reversible generator. Efficient translation of each already supplied circuit does not supply a missing source generator.

</details>

The frozen locators are NC §§3.1.2 and 3.2.5 (contents starts printed 129 and 153). The latter concerns energy and computation; no thermodynamic theorem is assumed here and no new full-text review is claimed. For circuit-family conventions and classical simulation context, [Watrous, *Quantum Computational Complexity*, §§IV.1 andIV.3](https://cs.uwaterloo.ca/~watrous/Papers/QuantumComputationalComplexity.pdf#page=12) was inspected. The clean finite-circuit construction and its uniformity/overhead proof are supplied above, rather than inferred from a complexity-class containment. This is an author-verified draft; independent mathematical/implementation review, reader trial and formal acceptance remain pending.

<!-- end-section-14.2 -->

<span id="sec-computational-models-complexity-and-quantum-advantage-3"></span>
## 14.3 Complexity classes and bounded error

**Question.** What must a quantum algorithm guarantee on every allowed input before we call its decision problem efficiently solvable with bounded error?

The prerequisites are [14.1, input length and uniform circuit families](#sec-computational-models-complexity-and-quantum-advantage-1), [14.2, clean reversible simulation](#sec-computational-models-complexity-and-quantum-advantage-2), and [6.8, fixed-design probability bounds](ch-measurement-expectation-values-and-statistical-estimation.md#sec-measurement-expectation-values-and-statistical-estimation-8). This **F-depth** section defines its models, proves selected elementary containments and complement closure, and proves a constant-gap normalization statement. Numerical examples check those constructions; they do not decide an unknown complexity-class relationship. All probabilities, bit counts and logical gate counts below are dimensionless.

### 14.3.1 Put the quantifiers and the promise into the definition

Write Σ={0,1}, and let A=(A_yes,A_no) consist of disjoint sets of finite binary strings. Its **promise** is their union. On x∈A_yes the answer is 1; on x∈A_no it is 0. Outside the promise there is no required answer. A language is the special case in which the union is Σ*. We use promise-problem versions of the classes below, as in the frozen source; restricting to languages gives the corresponding language versions.

For this section, use the following uniform circuit formulations. “Polynomial” means bounded by a fixed polynomial in n=|x|, not in the numerical value encoded by x. Every family has one deterministic classical generator that, given 1ⁿ, prints an explicit uncompressed gate list in polynomial time. Its topology is generated from the length, not separately designed after seeing each x.

- **P:** a uniform family of polynomial-size bounded-fan-in Boolean circuits C_n computes the correct bit on every promised x. Constants and explicit copies are allowed. This is the circuit formulation of deterministic polynomial computation used here.
- **BPP:** C_n also receives r(n) independent uniform random bits, where r is polynomially bounded and efficiently generated. Define its acceptance probability by the finite random-bit count below.
- **BQP:** a uniform family Q_n uses polynomially many qubits and gates, classical basis input x, zero ancillary qubits, and one terminal computational-basis answer qubit. Fix a finite efficiently specified universal gate alphabet. One convenient choice is {H,T,T†,X,CX,CCX}; including the reversible gates makes the construction below explicit. Gate entries do not carry arbitrary real advice. The finite-alphabet and approximation issues introduced in 5.5–5.7 are different from counting an arbitrary floating-point rotation as a free elementary operation.

Let a(n) be the number of zero ancillas in Q_n, and let Π₁ project onto answer 1 while acting as identity on every other qubit. **We consistently call 1 acceptance.** Then the two probabilistic models define

$$
p_C(x)=2^{-r(n)}\sum_{s\in\{0,1\}^{r(n)}} C_n(x,s),
\qquad
p_Q(x)=\left\|\Pi_1 Q_n|x,0^{a(n)}\rangle\right\|^2.
$$

For either model, the bounded-error conditions are

$$
\forall x\in A_{\mathrm{yes}}:\ p(x)\geq\frac23,
\qquad
\forall x\in A_{\mathrm{no}}:\ p(x)\leq\frac13.
$$

The yes/no acceptance gap is 1/3. Equivalently, each promised input is answered correctly with probability at least 2/3. This is a statement about a single algorithm family on **all** promised inputs, not average correctness over a chosen input distribution. It is not a confidence interval inferred from a finite record of answers. Exact acceptance probabilities 2/3 and 1/3 satisfy the endpoints; 1/2 satisfies neither label.

```python
from fractions import Fraction as F
import torch,flagquantum as fq
from dataclasses import replace
from examples.foundations import bounded_error as b,statistical_ensembles as e,uniform_reversible as u
assert b.contract(F(2,3),1) and b.contract(F(1,3),0)
assert not b.contract(F(1,2),1) and not b.contract(F(1,2),0)
assert b.contract(F(1,2),None) is None
print('Boundary2/3 and1/3 accepted;1/2 fails both labels;outside-promise has no required label.')
```

```text
Boundary2/3 and1/3 accepted;1/2 fails both labels;outside-promise has no required label.
```

The helper uses exact rational numbers for these logical boundary checks. Floating-point comparison with an analytic probability is a separate implementation check. A `None` label explicitly records an input outside the promise; it is not a third measurement result.

### 14.3.2 Prove the deterministic elementary containment

**Claim: P⊆BPP.** Take the uniform Boolean family defining a problem in P and give it zero random bits. The sum defining p_C then has exactly one term, so p_C(x)=C_n(x)∈{0,1}. Every promised yes-input has probability 1 and every promised no-input probability 0. The same generator and polynomial resource bound still work. This proves the containment; it does not prove that the two classes differ.

For a concrete language, define f(x)=⊕_j x_j, with f(ε)=0. A chain of XOR gates has linear size and a loop over j generates it uniformly. Hence odd digit parity is in P. In a reversible implementation with answer initialized to zero, CX(j,answer) for j=0,…,n−1 gives

$$
|x,0\rangle\longmapsto|x,f(x)\rangle,
\qquad p(x)=f(x).
$$

The data remain unchanged and the answer is deterministic. The companion retains the same declared four ancillary positions as the noisy example below; its deterministic branch leaves the coin/workspace positions zero. They are extra declared space, not a minimal implementation claim.

```python
_,p,cost=b.execute('101',deterministic=True)
assert p==0 and cost['kernel']==3 and cost['qubits']==7
assert len(b.family(1000))==1005
print('101 has even parity:p_accept=0;3 deterministic CX gates,7 declared qubits.')
print('Host generator length1000:1005 noisy-kernel gates;no length1000 native execution.')
```

```text
101 has even parity:p_accept=0;3 deterministic CX gates,7 declared qubits.
Host generator length1000:1005 noisy-kernel gates;no length1000 native execution.
```

The n=1000 assertion checks a host-generated gate list only. Executing a small simulator instance and generating a longer list are different evidence. Membership for every n follows from the loop, the parity argument and its resource bound, not from the largest tested length.

### 14.3.3 Prepare classical random bits coherently

H|0⟩=(|0⟩+|1⟩)/√2. Applying H to r distinct initialized qubits gives

$$
H^{\otimes r}|0^r\rangle
=2^{-r/2}\sum_{s\in\{0,1\}^r}|s\rangle.
$$

This follows by distributing the tensor product of the r two-term sums: each bit string selects exactly one term and has amplitude 2⁻ʳᐟ². Distinct strings are orthogonal, so terminal measurement gives each string probability 2⁻ʳ. For any assignment to any subset of the bits, exactly 2^(r−subset size) strings extend it. Its probability is therefore the product of the corresponding factors 1/2. Thus the measured bits have the independent fair-bit distribution.

The state is initially a coherent superposition, rather than a classical record already sampled inside the program. In the containment proof we will keep the coin labels until the terminal marginal is formed.

```python
coins=fq.Circuit(2,dtype=torch.complex128).H(0).H(1)
coin_result=fq.run(coins,outputs=[fq.probabilities(name='joint'),fq.samples(qubits=(0,1),name='coins')],
    shots=13,options=replace(e.OPTIONS,seed=47))
e.close(coin_result.measurement('joint').value[0],torch.full((4,),.25,dtype=torch.float64))
raw=coin_result.measurement('coins').value
assert raw.shape==(1,13,2) and bool(((raw==0)|(raw==1)).all())
print('Two H-prepared coins:joint probabilities[1/4,1/4,1/4,1/4];13 raw two-bit records checked.')
```

```text
Two H-prepared coins:joint probabilities[1/4,1/4,1/4,1/4];13 raw two-bit records checked.
```

The thirteen raw records check the native two-column output contract and valid bit values. They do not empirically prove independence or require exactly equal observed frequencies. Independence in the ideal model came from the product preparation and the calculation above.

### 14.3.4 Prove BPP⊆BQP without erasing the coin labels

Let C_n(x,s) be the one-bit Boolean result of a BPP circuit. Treat its n+r(n) input bits as data for the construction in 14.2. That result supplies a uniform reversible circuit U_n and zero workspace W of L(n) qubits with the exact clean action

$$
U_n|x,s,0^{L(n)},0\rangle
=|x,s,0^{L(n)},C_n(x,s)\rangle.
$$

Initialize the coin register with r(n) Hadamards, then apply U_n. The resulting pure state is

$$
|\Psi_x\rangle
=2^{-r(n)/2}\sum_s|x,s,0^{L(n)},C_n(x,s)\rangle.
$$

**Probability proof.** Project the last qubit onto 1. Only strings with C_n(x,s)=1 survive. When taking the squared norm, every cross term with s≠t vanishes because ⟨s|t⟩=0. Terms with s=t each contribute 2⁻ʳ. Consequently,

$$
\begin{aligned}
\Pr_Q[1\mid x]
&=2^{-r(n)}\sum_{s,t:C_n(x,s)=C_n(x,t)=1}\langle t|s\rangle\\
&=2^{-r(n)}\sum_s C_n(x,s)=p_C(x).
\end{aligned}
$$

The input x is fixed in this expression; there is no averaging over inputs. We neither add conditional coin-state vectors as if their labels were absent nor measure an undocumented intermediate collapse. The equality preserves the two error bounds on every promised x.

**Resource and uniformity proof.** If the Boolean circuit has L nodes, 14.2 implements its one-bit result with at most 4L+1 reversible gates and L work qubits. Adding r Hadamards costs r gates and r coin qubits. Including input and answer, the sufficient totals are n+r+L+1 qubits and at most r+4L+1 kernel gates. All are polynomial because r and L are polynomial. Compose the given uniform classical generator with the explicit polynomial-time translator, then prefix the r Hadamards. This is one uniform quantum generator. No truth table of size 2ʳ is constructed by the implementation; the sum above is for proof. The chosen alphabet contains all gates used. These facts prove **BPP⊆BQP**, and transitivity gives **P⊆BPP⊆BQP**.

For an executable example valid at every length, set

$$
C_n(x,s_0,s_1)=f(x)\mathbin{\oplus}(s_0\mathbin{\land}s_1).
$$

Exactly one of the four fair coin strings flips f(x). Thus

$$
p_C(x)=\begin{cases}1/4,&f(x)=0,\\3/4,&f(x)=1.\end{cases}
$$

Our specialized clean kernel computes the AND into a zero work qubit, XORs the data parity and work into the answer, and applies the same CCX again to clear work. Its cost is n+5 gates: two H, two CCX, n data-to-answer CX and one work-to-answer CX. It uses n+4 qubits. Basis input loading costs wt(x) additional X gates, where wt counts the 1 digits. These logical costs exclude target decomposition, routing and physical runtime.

```python
# Layout q0,q1=data; q2,q3=coins; q4=workspace; q5=answer.
c=fq.Circuit(6,dtype=torch.complex128).X(1).H(2).H(3)
c.CCX(2,3,4)
c.CX(0,5).CX(1,5).CX(4,5)
c.CCX(2,3,4)
r=fq.run(c,outputs=[fq.density_matrix(name='rho'),fq.probabilities(qubits=(5,),name='answer'),
    fq.samples(qubits=(5,),name='record')],shots=19,options=replace(e.OPTIONS,seed=47))
v=torch.zeros(64,dtype=torch.complex128)
for a,d in ((0,0),(0,1),(1,0),(1,1)):
    v[u.index((0,1,a,d,0,1^(a*d)))]=.5
e.close(r.measurement('rho').value[0],torch.outer(v,v.conj()))
e.close(r.measurement('answer').value[0],torch.tensor([.25,.75],dtype=torch.float64))
assert r.measurement('record').value.shape==(1,19,1)
print('Native clean randomized parity on01:p_accept=3/4;full density and terminal record shape checked.')
```

```text
Native clean randomized parity on01:p_accept=3/4;full density and terminal record shape checked.
```

Here 01 has f(x)=1. The full density check includes the retained coherent coin labels and exactly zero work, so matching the answer probability alone cannot hide incorrect cleanup. The use of H and reversible gates is a classical randomized algorithm embedded in a quantum model; the example makes no quantum speedup claim.

The companion also exercises a genuine **promise** example. Given x₀,x₁ and one fair selector bit s, return x_s. A Boolean implementation is x₀ XOR [s AND (x₀ XOR x₁)]. On promised inputs x₀=x₁, it is exactly correct. On 01 or 10 its acceptance probability is 1/2, which causes no violation because those inputs were excluded from this particular promise. The graph translator of 14.2 is actually called here; the independent reference directly indexes x_s.

```python
_,p_out,label_out=b.selector('01')
_,p_yes,label_yes=b.selector('11',mode='density_matrix')
assert p_out==F(1,2) and b.contract(p_out,label_out) is None
assert p_yes==1 and b.contract(p_yes,label_yes)
print('Selector promise x0=x1:11 accepts with1;01 gives1/2 outside the promise.')
```

```text
Selector promise x0=x1:11 accepts with1;01 gives1/2 outside the promise.
```

**Checkpoint.** Can the selector family solve the total language “the first bit is one” with the same error bound? No: the outside-promise inputs become required inputs of that total problem, and on them this family has probability 1/2. This says the displayed family fails that contract, not that the total language is hard.

### 14.3.5 Prove closure under exchanging yes and no

For a promise problem A, let its complement be coA=(A_no,A_yes), retaining the same promise. In a classical circuit, append NOT to the answer. In a quantum circuit, append X to the answer immediately before terminal readout. X swaps its 0 and 1 subspaces while leaving every other register alone. Since the two terminal answer probabilities sum to one,

$$
p_{\mathrm{new}}(x)=1-p_{\mathrm{old}}(x).
$$

On an old no-input, p_old≤1/3 implies p_new≥2/3. On an old yes-input, p_old≥2/3 implies p_new≤1/3. Appending one fixed gate preserves polynomial size and uniformity. This proves that BPP and BQP are each closed under complementation, often written coBPP=BPP and coBQP=BQP. The same NOT argument also applies to P. It is an explicit construction, not a numerical symmetry inferred from a few test pairs.

```python
_,p_no,_=b.execute('01',complement=True)
_,p_yes,_=b.execute('00',complement=True,mode='density_matrix')
assert p_no==F(1,4) and p_yes==F(3,4)
assert b.contract(p_no,0) and b.contract(p_yes,1)
print('One output X complements acceptance:01->1/4;00->3/4;both new labels satisfy the contract.')
```

```text
One output X complements acceptance:01->1/4;00->3/4;both new labels satisfy the contract.
```

No phase alignment is involved. An X on the designated answer exchanges acceptance probabilities exactly even if that answer is entangled with retained registers.

### 14.3.6 Explain why a fixed gap matters, and prove a normalization

Suppose instead of the constants above a uniform algorithm has, for a fixed 0<γ≤1/2,

$$
x\in A_{\mathrm{yes}}\Rightarrow p(x)\geq\frac12+\gamma,
\qquad
x\in A_{\mathrm{no}}\Rightarrow p(x)\leq\frac12-\gamma.
$$

Run k independent fresh copies on the same classical input x, with k odd, and accept when a strict majority of their answer bits is 1. Let B_i be the ith terminal bit and \(\overline B=k^{-1}\sum_iB_i\). Independent copies have

$$
\mathbb E[\overline B]=p,
\qquad
\operatorname{Var}(\overline B)=\frac{p(1-p)}k\leq\frac1{4k}.
$$

For a yes-input, a wrong majority implies \(\overline B<1/2\), hence \(|\overline B-p|\geq\gamma\). For a no-input a wrong majority implies \(\overline B>1/2\) and the same deviation bound. Applying the Chebyshev result from 6.8 gives

$$
\Pr[\text{wrong majority}\mid x]\leq\frac1{4k\gamma^2}.
$$

Choose any odd integer k≥3/(4γ²); then the error is at most 1/3. Because γ is fixed, k is constant as a function of n. We have proved that **any fixed symmetric gap about 1/2 can be converted to the 2/3 versus 1/3 convention**. Conversely those standard bounds already have γ=1/6. This proves equivalence of these constant-gap conventions, without claiming a tight repetition budget. Inverse-polynomial gaps, very small target failure probabilities and accumulated implementation error will be treated with the accuracy budget in 14.5.

We must still justify that majority is available efficiently inside the circuit model. Here is a construction rather than a free majority oracle. For answer bits b₁,…,b_k, let D_j,t mean “at least t of the first j bits are one.” Set D_j,0=1 and D_0,t=0 for t>0. For j≥1 and t≥1, use

$$
D_{j,t}=(\neg b_j\land D_{j-1,t})
\lor(b_j\land D_{j-1,t-1}).
$$

If b_j=0, reaching t requires t among the previous bits. If b_j=1, it requires t−1 among them. These two cases prove the recurrence by induction on j. Compute it row by row up to t=(k+1)/2 using O(k²) constant-size Boolean gates; D_k,(k+1)/2 is the majority. OR can itself be written NOT(AND(NOT a,NOT b)). The nested loops are a uniform generator. Section 14.2 turns this graph into a clean reversible majority using O(k²) additional gates and work qubits.

In the quantum model prepare k disjoint copies of the original circuit. Before any copy runs, use n(k−1) CX gates to copy the computational-basis input x into k−1 fresh zero input registers. The same fixed fanout pattern works for every x; no generator is allowed to hard-code that x. This does not clone an unknown quantum input. With no coupling between copies before voting, their state is a tensor product; the joint output probabilities multiply. Apply the reversible majority to their answer registers and measure its output. On each computational answer string its projector selects exactly the majority event, so even if the copies' answers are entangled with their own work, the vote probability equals the classical majority probability. For a base circuit with T(n) gates and q(n) qubits, sufficient resources are kT(n)+n(k−1)+O(k²) gates and kq(n)+O(k²) qubits, including this basis-input fanout; any external basis preparation is recorded separately. All generators compose in polynomial time.

For three bits specifically, majority(a,b,c)=ab XOR ac XOR bc: for 0,1,2,3 ones the number of true pairs is respectively 0,0,1,3, giving the right bit. Three CCX gates into a zero answer implement it. Our example's single-trial error is 1/4. Independent three-trial majority has exact error

$$
3(1/4)^2(3/4)+(1/4)^3=\frac5{32}.
$$

If all three answers reuse the same underlying two coin bits, they agree on every trial and the error remains 1/4. Their individual marginals are unchanged; the product-law and variance reduction are lost.

```python
_,independent_error=b.majority(0,independent=True)
_,shared_error=b.majority(0,independent=False)
assert independent_error==F(5,32) and shared_error==F(1,4)
gamma=F(1,4);k=b.repetition_budget(gamma)
assert k==13 and F(1,4)/(k*gamma**2)==F(4,13)<=F(1,3)
assert b.tail(F(1,4),k)<=F(4,13)
def threshold(bits):
    h=len(bits)//2+1
    previous=[1]+[0]*h
    for bit in bits:
        current=[1]+[0]*h
        for t in range(1,h+1):
            current[t]=((1-bit)&previous[t]) | (bit&previous[t-1])
        previous=current
    return previous[h]
for length in (1,3,5):
    for j in range(2**length):
        bits=u.bits(j,length)
        assert threshold(bits)==int(sum(bits)>length//2)
print('Three votes:independent error5/32;shared-coin error1/4.')
print('Chebyshev design:gamma1/4,k13,error bound4/13<=1/3;exact binomial tail checked.')
```

```text
Three votes:independent error5/32;shared-coin error1/4.
Chebyshev design:gamma1/4,k13,error bound4/13<=1/3;exact binomial tail checked.
```

The `threshold` loop is the displayed D recurrence with only its previous row retained; it is exhaustively compared with direct bit counting at lengths 1, 3 and 5. This host calculation validates the recurrence implementation, not the general proof. The thirteen-trial budget is a host exact-rational calculation; no thirteen-copy native circuit is claimed. The two native three-trial cases check the independent and shared-coin constructions, including their entire classical output distributions. The independent case occupies ten qubits and uses only the statevector execution mode in this companion.

### 14.3.7 Diagnose a missing gap and a misleading average

Using the same coin for both arguments of AND replaces s₀ AND s₁ by s₀ AND s₀=s₀. The error bit is now fair: p(x)=1/2 for both parities. This particular circuit no longer meets either promised label's bounded-error contract. It does not imply the parity problem left P; its deterministic algorithm still exists.

A second mistake is replacing “for every x” with a favorable input average. Consider eight length-three strings and a hypothetical deterministic answer table correct on seven strings but wrong on 111. Uniform-input average correctness is 7/8, above 2/3; its success probability on 111 is zero. The table fails the universal requirement. Membership means the existence of some qualifying uniform family, not that every proposed algorithm for the problem is correct.

```python
_,p_bad,_=b.execute('00',coins='reused')
assert p_bad==F(1,2) and not b.contract(p_bad,0)
labels=[sum(u.bits(j,3))%2 for j in range(8)]
probabilities=[F(y) for y in labels];probabilities[7]=F(0)
correct=[p if y else 1-p for p,y in zip(probabilities,labels)]
assert sum(correct)/8==F(7,8) and not all(b.contract(p,y) for p,y in zip(probabilities,labels))
assert b.invalid_checks()==14
print('Reusing a coin inside AND destroys the gap:p_accept=1/2.')
print('Average correctness7/8 can hide a failing input;14 malformed contracts rejected.')
```

```text
Reusing a coin inside AND destroys the gap:p_accept=1/2.
Average correctness7/8 can hide a failing input;14 malformed contracts rejected.
```

No assertion here requires sampled frequency to be numerically close to p. The native exact probability, the analytic rational probability, and the finite random record have separate roles. A small record that happens to be correct on every trial proves neither a universal error bound nor a complexity-class separation. Replaying a fixed seed is useful for debugging and supplies no new independent statistical evidence.

### 14.3.8 Keep the API and the conclusion within their evidence

The complete companion is [bounded_error.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/bounded_error.py). Run from the repository root with its pinned example environment:

```bash
python examples/foundations/bounded_error.py
python scripts/check_bounded_error_prose.py
```

Expected output of the complete program:

```text
82 actual native circuits:14 deterministic,28 fair-coin,28 reused-coin,8 promise-selector and4 majority cases passed.
Full clean states/probabilities checked in both modes for78 circuits;4 majority cases use native statevector probabilities.
Independent majority error5/32;shared-coin error1/4. Fixed-gap budget13;exact rational boundary/tail checks passed.
14 malformed contracts rejected before execution;finite checks are not complexity-class certificates.
```

The tested runtime is released FlagQuantum 0.3.1, PyTorch 2.13.0 and Python 3.12.14 on CPU. The first 78 circuits use complex128 and exercise both statevector and density-matrix modes. They compare complete density operators and probabilities against explicit scalar coin enumeration; statevector mode also compares full complex amplitudes. The last four majority cases use statevector mode, native vote-qubit probabilities and full simulator-vector squared moduli against an independently enumerated classical histogram. Probabilities/densities use absolute tolerance 10⁻¹² and relative tolerance zero. No phase alignment, clipping or normalization repair is performed. Exact boundary decisions and binomial sums use `Fraction`; floating-point tests are not interval certificates.

The literal API calls are `Circuit.H/X/CX/CCX`, `fq.run`, `fq.probabilities`, `fq.samples` and `fq.density_matrix`. The first complete attempt reached 79 actual executions, then its ten-qubit *full* probability request was rejected before that circuit ran: this release's default marginal-probability request limit is eight qubits. The corrected version queries only the one vote qubit and uses the statevector accessor for the independent full-distribution check. The original source and failure log remain in the evidence. This is a request guard, not a claim that the simulator cannot execute ten-qubit circuits.

The parity helper's n≤3 native guard, length≤10000 host-generation guard, exact-tail k≤101 guard and shots≤1000 are bounded teaching contracts, not framework scalability limits. Bit loading uses actual X gates; output requests are ideal terminal simulator queries. No native complexity-class recognizer, proof checker, BPP compiler, runtime advantage test, hardware random-source certification, mid-circuit collapse or dynamic-controller capability is established by this section. Reversible graph translation, rational analysis and resource accounting are book code.

The selected containments and complement statements have full proofs above. There is no proof here that P, BPP or BQP are distinct. We do not infer NP relations from superposition, from a simulator runtime or from the success of one problem. More advanced upper bounds are outside this section's selected elementary claims. A quantum computer's ability to represent the constructed circuit is separate from the classical cost of simulating its full state.

**Understanding and transfer tasks**

- **14.3-A — quantifiers.** A test reports average correctness 99% on its chosen inputs. Which missing statements prevent it from proving a problem is in BQP? What changes outside a promise?
- **14.3-B — derivation.** Replace two coins by r coins in the containment proof. Identify the inner product that removes cross terms, derive the acceptance sum, and explain why deleting the coin labels before squaring is wrong.
- **14.3-C — fresh implementation.** For data x of length three, use one coin r and output majority(x₀,x₁,x₂) XOR r. Construct majority as the XOR of its three pairwise ANDs and translate the graph with 14.2 to inspect its resource count. Then implement the equivalent smaller circuit described in the answer, prepare r with H and validate full state/density in both modes on x=101 and 010. Does this circuit have a bounded-error gap for majority? Also run fresh noisy-parity inputs 110 and 111 with complement both off and on.
- **14.3-D — amplification.** For γ=1/10, find the smallest odd k meeting this section's Chebyshev sufficient bound. Explain why identical marginal answer laws are insufficient to use it, and why the bound need not equal the exact binomial failure probability.

<details markdown="1">
<summary>Answers and verification guidance for 14.3-A–D</summary>

**A.** One needs a declared input encoding and promise, one uniform generator, polynomial resources and a correctness bound on every promised input at every length. A finite test distribution supplies none of the missing universal claims by itself. Outside the promise no answer is required, but it cannot be silently enlarged after testing.

**B.** The projected norm contains ⟨t|s⟩=δ_ts in the retained coin register. Therefore it is 2⁻ʳ times the number of accepting coin strings. Replacing the distinguishable branches by a vector sum on only the answer register changes both normalization and interference; it is not the marginal measurement operation.

**C.** Three AND nodes followed by two XOR nodes form majority, and a final XOR with r forms the output. With three data bits and one coin, six work qubits and one answer, the direct 14.2 construction uses eleven qubits, which is larger than needed for this exercise. A bounded implementation can avoid the intermediate XOR storage: use three CCX gates into a zero answer, then CX from the fair coin into the answer. This three-data-plus-coin-plus-answer construction uses five qubits, retains the coin and needs no additional workspace. For either x the output is fair, so the candidate fails both bounded-error labels. The independent transfer deliberately validates this smaller explicit native construction rather than invoking the helper beyond its bounded graph/native guard. The separate noisy-parity cases have probabilities 1/4 on 110 and 3/4 on 111, exchanged by complement. Exact states/densities and terminal probabilities must agree, not only one sampled record.

**D.** k≥3/[4(1/10)²]=75 and 75 is odd. Independence is used in Var(average)=p(1−p)/k; perfectly correlated copies retain the original variance. Chebyshev bounds a larger deviation event and need not be tight for the discrete majority event. Repetition-resource counts include fresh copies, majority work and input loading.

</details>

The frozen source `COMPLEX:BQP` is Watrous, [*Quantum Computational Complexity*, §§IV.1–IV.3, PDF pages 12–14](https://arxiv.org/pdf/0804.3401v1#page=12). Those pages were inspected for uniform circuit definitions, bounded-error conventions and classical simulation; the author-hosted copy was also checked. Our explicit clean-workspace proof, examples and conservative Chebyshev normalization are supplied locally. Watrous labels acceptance by the opposite terminal bit in his setup; this section fixes acceptance to 1 throughout. The source's more general error-reduction and quantum-subroutine results are not being claimed as proved here.

The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/14.3.json) separates author execution from independent mathematical/implementation review and reader trial. It remains a working draft. Continue, when drafted, with [14.4 Oracle and data-access models](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-4).

<!-- end-section-14.3 -->

<span id="sec-computational-models-complexity-and-quantum-advantage-4"></span>
## 14.4 Oracle and data-access models

**Question.** When an algorithm says “query the data once,” what operation has actually been supplied, and which costs did that sentence leave outside the query count?

The prerequisites are [14.1, input length and computational models](#sec-computational-models-complexity-and-quantum-advantage-1) and [5.3, classical logic embedded reversibly](ch-gates-reversible-computation-and-circuit-synthesis.md#sec-gates-reversible-computation-and-circuit-synthesis-3). This **P-depth** section specifies access contracts and then derives small checks under those contracts. Supplying an oracle is an additional computational assumption, not a consequence of storing data in a Python array or preparing a superposition. We do not prove a search algorithm or a query lower bound here; those arguments belong to Chapters 15–16.

### 14.4.1 State the interface before counting a query

Let D=(D₀,…,D_N₋₁) be a classical table of N words, each an unsigned b-bit integer. For now N=2ᵃ, so an a-qubit address register I represents every table position. The first listed address qubit is the most significant bit; the first listed value qubit is the most significant value bit, as in Chapter 4. Address and value registers have disjoint supports.

Here are four different access contracts. An algorithm must say which one it assumes.

| Contract | Declared action | Information supplied or still missing |
|---|---|---|
| Classical word access | A classical address i returns D_i | Memory organization, word width, read/update costs and input-loading costs remain model choices. |
| Coherent value access | O_D sends address i and value z to i and z XOR D_i | A unitary action on every basis input, including nonzero z, with declared workspace behavior. |
| Binary phase access | P_f multiplies address i by (−1)^f(i) | A one-bit predicate f; inverse/controlled variants are separate interface questions. |
| Normalized-state access | A preparation supplies the state with amplitudes d_i divided by the Euclidean norm of d | This does not by itself supply d's norm, value access, all other columns of a preparation unitary, or its inverse. |

The conventional **XOR value oracle** is

$$
O_D|i,z\rangle=|i,z\mathbin{\oplus}D_i\rangle,
\qquad 0\leq i<N,\quad 0\leq z<2^b.
$$

The XOR is bitwise on exactly b bits; it is not integer addition modulo 2ᵇ. The map applied twice returns (i,z), so it is a permutation of the entire computational basis and hence unitary, as established generally in 5.3. This also fixes O_D†=O_D for this particular convention. The action on z≠0 matters: a black box specified only on zero targets would leave too much of the unitary undefined.

An implementation with workspace W must additionally state whether it returns W to its initial blank state. The clean convention is

$$
|i,z,0_W\rangle\longmapsto|i,z\mathbin{\oplus}D_i,0_W\rangle.
$$

An unknown address-dependent garbage register is not interchangeable with clean access in interference experiments. The bounded examples below use no workspace at all.

```python
import math,torch,flagquantum as fq
from dataclasses import replace
from examples.foundations import oracle_access as q,statistical_ensembles as e,uniform_reversible as u
table=(0,1,3,2);a=b=2
ops,cost=q.build(table,a,b)
assert cost['serialized_bits']==8 and cost['gates']==8
assert table[2]==3
print('Four 2-bit words; 8 serialized classical bits; one toy lookup expands to 4 X + 4 CCX.')
```

```text
Four 2-bit words; 8 serialized classical bits; one toy lookup expands to 4 X + 4 CCX.
```

The helper scans a complete immutable tuple on the host and constructs a short gate list. Its eight-bit payload count uses an ideal fixed-width format; it is not the storage size of a Python tuple or the length of the JSON used for fingerprinting. It is book code, not a native database or QRAM endpoint. Its serialization count is in **classical bits**; its gate count is in the declared logical X/CX/CCX alphabet. Adding those numbers as if they were one physical runtime would mix units.

### 14.4.2 Implement one oracle and expose its gates

Take a=2, b=2 and D=(0,1,3,2). Write the address as (i₀,i₁), most significant bit first. The table is the two-bit Gray map

$$
D_{i_0i_1}=(i_0,\ i_0\mathbin{\oplus}i_1).
$$

The high value bit receives i₀ and the low value bit receives i₀ XOR i₁. Thus three CX gates implement the entire XOR oracle on arbitrary initial value bits:

$$
(i_0,i_1,z_0,z_1)\longmapsto
(i_0,i_1,z_0\mathbin{\oplus}i_0,
 z_1\mathbin{\oplus}i_1\mathbin{\oplus}i_0).
$$

The first two X gates in the following program load address 10 and initial value 01. They are preparation, outside the three-gate oracle block.

```python
# Same table, exploiting its Gray-code structure instead of minterm synthesis.
c=fq.Circuit(4,dtype=torch.complex128).X(0).X(3)
c.CX(0,2).CX(1,3).CX(0,3)
r=fq.run(c,outputs=[fq.probabilities(name='full'),fq.samples(qubits=(2,3),name='data')],
    shots=7,options=replace(e.OPTIONS,seed=59))
expected=torch.zeros(16,dtype=torch.float64);expected[10]=1
e.close(r.measurement('full').value[0],expected)
assert bool((r.measurement('data').value==torch.tensor([1,0])).all())
print('Address 10, target 01 -> address 10, target 10; structured oracle uses 3 CX; 7 native records checked.')
```

```text
Address 10, target 01 -> address 10, target 10; structured oracle uses 3 CX; 7 native records checked.
```

The generic helper implements the same table without exploiting its Gray structure. For each address with a nonzero word, it temporarily flips the zero address bits, writes each 1 digit with a controlled X, then restores those address flips. For a≤2, a write is respectively CX or CCX, with no ancillary qubit. Distinct address minterms are mutually exclusive, so the target receives exactly the selected word. Its logical counts are

$$
G_X=2\sum_{i:D_i\ne0}\bigl(a-\operatorname{wt}(i)\bigr),
\qquad
G_{\mathrm{write}}=\sum_i\operatorname{wt}(D_i),
$$

where wt counts 1 digits in the declared fixed-width bit string. Here G_X=4 and G_write=4, giving eight gates. At larger address width the corresponding multiple-control writes would themselves require synthesis; this small helper does not pretend that every such write is one elementary gate.

Both the eight-gate implementation and the three-gate structured implementation are **one abstract query** when placed behind the same O_D interface. This is exactly why an oracle-call count and a gate count answer different questions. Logical gate counts also do not imply physical speed: X, CX and CCX have different decompositions and target costs.

### 14.4.3 Preserve superpositions without promising all the data as output

For arbitrary complex amplitudes α_i,z, linearity gives

$$
O_D\sum_{i,z}\alpha_{i,z}|i,z\rangle
=\sum_{i,z}\alpha_{i,z}|i,z\mathbin{\oplus}D_i\rangle.
$$

A classical call `table[i]` with a sampled i does not implement this transformation on a coherent address register. The query must preserve the specified relative phases. Address order, value-bit order, phase conventions, blank-workspace assumptions and output correlations are all part of a reproducible interface.

The independent reference pulls each output amplitude from its unique inverse input:

$$
\beta_{i,z}=\alpha_{i,z\oplus D_i}.
$$

This reference uses neither the native gate list nor its intermediate states. Applying O_D twice gives β=α, including correlated address/value input and a nonzero initial value.

```python
q.execute(table,2,2,coherent=True)
q.execute(table,2,2,coherent=True,repeats=2,mode='density_matrix')
print('Complex joint address/value input checked; two XOR-oracle calls restore the full input.')
```

```text
Complex joint address/value input checked; two XOR-oracle calls restore the full input.
```

For a uniform address and a zero value register, the returned state is N⁻¹ᐟ²∑_i|i,D_i⟩. Measuring both registers returns **one** address/value pair. A single terminal record is not a classical listing of all N words. The simulator's full-state accessor and full-density output are diagnostic classical arrays in this laboratory; they are not extra hardware outputs that a query algorithm may read for free.

### 14.4.4 Distinguish a phase query from a value query

For a binary table f:{0,…,N−1}→{0,1}, define

$$
P_f|i\rangle=(-1)^{f(i)}|i\rangle.
$$

With the XOR oracle and a target prepared as |−⟩=(|0⟩−|1⟩)/√2, the target's X eigenvalue is −1, so

$$
O_f(|i\rangle|{-}\rangle)
=|i\rangle X^{f(i)}|{-}\rangle
=(-1)^{f(i)}|i\rangle|{-}\rangle.
$$

This local calculation is sufficient to check this interface conversion. The target preparation has a cost, and the clean action is still required. With |+⟩ instead, X|+⟩=|+⟩ and no f-dependent phase appears. A target initialized to zero instead produces a value bit correlated with the address; it is a different experiment.

For f=(0,1,1,0), the predicate is address parity. After preparing a uniform two-qubit address, querying with |−⟩, and applying H to both address qubits for readout, the amplitude of address k is

$$
\frac14\sum_{i\in\{0,1\}^2}(-1)^{f(i)+i\cdot k},
$$

where i·k means i₀k₀+i₁k₁ modulo 2. This follows by inserting ⟨k|H⊗H|i⟩=(−1)^(i·k)/2 into the phase-weighted input sum. For k=11 every term is +1; for any other k the signs cancel in pairs. The |+⟩ target instead leaves address 00 after the same readout.

```python
# Binary parity table f=(0,1,1,0); the target is |->, not |0>.
c=fq.Circuit(3,dtype=torch.complex128).H(0).H(1).X(2).H(2)
c.CX(0,2).CX(1,2)
c.H(0).H(1)
r_phase=fq.run(c,outputs=[fq.probabilities(qubits=(0,1),name='address')],options=e.OPTIONS)
e.close(r_phase.measurement('address').value[0],torch.tensor([0.,0.,0.,1.],dtype=torch.float64))
v_phase=torch.zeros(8,dtype=torch.complex128);v_phase[6]=1/math.sqrt(2);v_phase[7]=-1/math.sqrt(2)
e.close(r_phase.statevector()[0],v_phase)
r_plus=q.phase((0,1,1,0),2,minus=False)
e.close(r_plus.measurement('address').value[0],torch.tensor([1.,0.,0.,0.],dtype=torch.float64))
print('Minus-target parity query gives address 11 after H readout; plus-target gives 00 and carries no table phase.')
```

```text
Minus-target parity query gives address 11 after H readout; plus-target gives 00 and carries no table phase.
```

This verifies a particular conversion, not free equivalence of all oracle interfaces. In particular, a phase-oracle contract need not include a controlled version. For the constant predicates 0 and 1, their phase oracles are I and −I. In a circuit with a fixed number Q of uncontrolled calls they differ only by the overall phase (−1)^Q, so they yield the same measurement probabilities. A value query on a zero target distinguishes their values immediately. Adding controlled access changes the available operation and must be stated; it cannot be silently inferred from the word “oracle.”

### 14.4.5 Separate amplitude preparation from numerical data lookup

For a nonzero vector d=(d₀,…,d_N₋₁), a normalized-state input contract may supply

$$
|d\rangle=\frac1{\|d\|_2}\sum_i d_i|i\rangle,
\qquad
\|d\|_2=\sqrt{\sum_i|d_i|^2}.
$$

This contract supplies a quantum state, not a coherent XOR read of b-bit values. It has to specify a preparation mechanism, numerical precision, repeated-use cost and whether the norm or other metadata is provided. Measuring the state gives i with probability |d_i|²/∥d∥₂², not a numerical value d_i. For complex d, probabilities alone also omit relative phases.

**Input-model counterexample.** Let d=(1,2,2,1), so ∥d∥₂=√10 and its entry sum is 6. The vector 2d has norm 2√10 and sum 12, yet

$$
|2d\rangle=|d\rangle.
$$

No measurement on this state-only input can reveal which sum was intended: identical density operators give identical probabilities for every measurement effect. Repeated copies are also identical. An algorithm for exact numerical sum therefore cannot assume that this normalized state by itself specifies the original unnormalized data. Supplying the norm or a value oracle changes the input model. If access is instead to an entire preparation unitary, the promise on its zero-input column alone still does not guarantee extra scale information in its other columns; a legal implementation may choose the very same unitary for d and 2d.

For the small nonnegative real vectors in the companion, we explicitly construct one such preparation unitary. Let v=d/∥d∥₂, e₀=(1,0,…,0), and w=e₀−v. If w=0 use A=I. Otherwise set

$$
A=I-2\frac{ww^\dagger}{w^\dagger w}.
$$

The rank-one factor ww†/(w†w) is a projector, so squaring I−2 times that projector gives I. Thus A is unitary and Hermitian. For real normalized v with w≠0, w†e₀=1−v₀ and w†w=2(1−v₀), so Ae₀=e₀−w=v. The helper checks both identities numerically before requesting native execution. This construction is deliberately dense: it first reads the explicit entries and builds N² matrix entries. One simulator call containing that matrix is not a proof of an efficient generic data loader.

```python
data=torch.tensor([1,2,2,1],dtype=torch.complex128)
v=data/math.sqrt(10);e0=torch.zeros(4,dtype=torch.complex128);e0[0]=1
w=e0-v;A=torch.eye(4,dtype=torch.complex128)-2*torch.outer(w,w.conj())/torch.vdot(w,w)
e.close(A.mH@A,torch.eye(4,dtype=torch.complex128))
c=fq.Circuit(2,dtype=torch.complex128).unitary(0,1,unitary=A)
r_amp=fq.run(c,outputs=[fq.density_matrix(name='rho'),fq.probabilities(name='p')],options=e.OPTIONS)
e.close(r_amp.measurement('rho').value[0],torch.outer(v,v.conj()))
e.close(r_amp.measurement('p').value[0],torch.tensor([.1,.4,.4,.1],dtype=torch.float64))
r_scaled,_=q.amplitude((2,4,4,2),mode='density_matrix')
e.close(r_scaled.measurement('rho').value[0],r_amp.measurement('rho').value[0])
assert sum((1,2,2,1))==6 and sum((2,4,4,2))==12
print('One supplied 4x4 unitary prepares probabilities [.1,.4,.4,.1]; host reads 4 entries and constructs 16 matrix entries.')
print('Data sums 6 and 12 yield the same normalized state; state-only access does not specify the scale.')
```

```text
One supplied 4x4 unitary prepares probabilities [.1,.4,.4,.1]; host reads 4 entries and constructs 16 matrix entries.
Data sums 6 and 12 yield the same normalized state; state-only access does not specify the scale.
```

The native custom-unitary request receives the entire 4×4 matrix. Its physical gate synthesis, rotation accuracy, loading latency, device connectivity and hardware calibration have not thereby been priced as one elementary operation. Our two-qubit example is an executed modeling illustration, not a QRAM architecture or a universal state-preparation compiler.

### 14.4.6 Specify inverse, controlled and workspace access separately

In an oracle algorithm, expressions such as A†, controlled-A or a clean query have content only after their interfaces are supplied or constructed. A promise A|0⟩=|d⟩ leaves A's action on all other inputs unspecified. Different unitary extensions may agree on this state but differ elsewhere. A black box that merely delivers copies of |d⟩ is weaker still; it has not supplied an operation A†.

In this laboratory the matrix A is known, so we can explicitly pass its conjugate transpose as a second custom unitary. This does not require or claim anything about a generic inverse-oracle service, `Circuit.adjoint`, or a released upstream fix. It verifies a known matrix and accounts for two calls.

```python
_,preparation=q.amplitude((1,2,2,1),twice=True)
assert preparation['custom_unitary_calls']==2 and preparation['dense_matrix_entries']==16
print('Known A followed by its supplied matrix adjoint returns |00>; 2 custom-unitary calls counted.')
```

```text
Known A followed by its supplied matrix adjoint returns |00>; 2 custom-unitary calls counted.
```

For the XOR oracle specifically, a second identical query is its inverse, as proved in 14.4.1. For a general preparation unitary A, the inverse is not obtained by assuming A=A†; our Hermitian toy construction is a special case. If a larger algorithm needs query, inverse-query and controlled-query access, list each assumed service and its workspace convention explicitly.

### 14.4.7 Build a cost ledger with consistent units

An abstract query algorithm with Q calls may be written

$$
V_Q O_D V_{Q-1} O_D\cdots O_D V_0,
$$

with the V_j representing the allowed non-oracle operations. In a black-box comparison, these operations and the initial state cannot secretly depend on the unknown D. They may use declared public parameters and, where the model allows adaptive execution, earlier measurement records. A provider that reads the full known table to construct or optimize O_D is performing implementation/setup work; this is not uncounted access that the query algorithm may hide inside a V_j. Counting Q deliberately suppresses the implementation of O_D. It does not say that generating D, building the oracle, generating the V_j, loading the input or reporting the output is free in a complete implementation. In particular, D may be an explicitly stored table of N=2ᵃ words, or it may be generated by a short formula; these are different data descriptions even when a few observed outputs coincide.

A sequential time model for R repeated trials could declare

$$
\begin{aligned}
T_{\mathrm{total}}&=T_{\mathrm{read}}+T_{\mathrm{build}}
+K\,T_{\mathrm{update}}+T_{\mathrm{post}}\\
&\quad+R\Bigl(T_{\mathrm{prepare}}+Q\,T_O
+Q_{\mathrm{inv}}\,T_{O^\dagger}\\
&\hspace{5.7em}+T_{\mathrm{other}}+T_{\mathrm{measure}}\Bigr).
\end{aligned}
$$

All T terms must use the same time unit and the same machine/access assumptions. K counts data updates; Q and Q_inv are forward/inverse calls **per trial**, and R is the number of trials. Setup is amortized here only when the same data structure is actually reusable. Parallel or overlapping execution needs a different timing model. A query theorem alone supplies none of these time constants.

The following exact ledger instead keeps classical bit counts and logical gate counts as separate fields. For five trials of two queries each, it records ten oracle calls. With the minterm realization, that is 80 implementation gates; with this table's structured realization, 30 CX gates. Neither includes preparation/readout, and neither turns eight serialized classical bits into eight gates or seconds. This is an analytic bill for a reusable compiled snapshot, not a measured timing or a claim that the validation loop caches its repeated Python construction.

```python
bill=q.ledger(table,2,2,calls_per_trial=2,trials=5)
assert bill['oracle_calls']==10 and bill['oracle_implementation_gates']==80
assert bill['classical_serialized_bits']==8 and bill['setup_builds']==1
assert 3*10==30
print('Five trials, two queries each: 10 abstract calls; 80 minterm gates or 30 structured gates; 8 setup bits remain a separate unit.')
```

```text
Five trials, two queries each: 10 abstract calls; 80 minterm gates or 30 structured gates; 8 setup bits remain a separate unit.
```

Reading this explicit table once and representing each fixed-width entry requires Nb serialized bits under the chosen format. Since N=2ᵃ, a cost linear in the number of entries is exponential in address width. That is a comparison of representation sizes, not a lower bound on every possible oracle architecture. A short formula or a pre-existing reusable memory service may change setup assumptions, which must then be included in the comparison.

For a simple classical illustration, any deterministic procedure computing the exact sum of an arbitrary explicit table through entry reads must inspect every entry in the worst case: if one entry is unread, two tables differing only there produce the same observed reads but different sums. This argument concerns that exact classical input task. It is not a quantum state-preparation lower bound or a search lower-bound theorem.

The simulator has additional classical state/density arrays and contractions. Their memory or runtime is a simulation resource, not the hardware resource of the abstract query algorithm. Retrieving a full simulator density matrix during verification does not grant the algorithm free access to it.

### 14.4.8 Handle padding, data versions and the API boundary

If the actual table has M entries with M not a power of two, choose a=ceil(log₂M), declare which addresses are valid, and define the oracle on the remaining computational basis states. Zero padding is one possible unitary extension. It must not silently turn an invalid problem address into a valid one. Likewise, a compiled table is a snapshot: changing D requires a matching rebuild/update or a versioned cache contract.

```python
padded=(0,1,1,0)
q.execute(padded,2,1,i=3)
assert not 3<3  # Physical address11 is outside the declared three-entry task domain.
assert q.fingerprint(table,2,2)!=q.fingerprint((0,1,2,2),2,2)
assert q.invalid_checks()==14
print('Padding defines a unitary on address 11 but does not make it a valid three-entry problem address.')
print('Changed data invalidate the snapshot fingerprint; 14 malformed access contracts rejected.')
```

```text
Padding defines a unitary on address 11 but does not make it a valid three-entry problem address.
Changed data invalidate the snapshot fingerprint; 14 malformed access contracts rejected.
```

The fingerprint is a host consistency check on an immutable toy snapshot. It is not authentication, hardware provenance, or proof that a remote memory holds the desired data. The padded three-entry example defines a value at physical address 11, while the problem promise still excludes that address.

The complete companion is [oracle_access.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/oracle_access.py). Run from the repository root with its pinned example environment:

```bash
python examples/foundations/oracle_access.py
python scripts/check_oracle_access_prose.py
```

Expected output of the complete program:

```text
108 actual native circuits: 72 basis, 8 complex lookup, 8 two-query cancellation, 8 phase-interface and 12 amplitude preparation/inverse cases passed.
Both CPU complex128 modes checked against full scalar amplitude/density references; terminal lookup records validated.
Gray lookup: one abstract query expands to 4 X + 4 CCX; five two-query trials use 10 calls/80 implementation gates; 8 classical data bits separate.
14 malformed access contracts rejected; no QRAM, free generic loading or query-to-runtime equivalence claimed.
```

The tested runtime is FlagQuantum 0.3.1, PyTorch 2.13.0 and Python 3.12.14, CPU complex128, in both statevector and density-matrix modes. Full complex states in statevector mode and full density matrices in both modes are compared with independent inverse-index/finite-sum references. Native terminal probabilities and raw records are checked separately. Absolute tolerance is 10⁻¹², relative tolerance zero; there is no phase alignment, probability clipping or normalization repair. The division by ∥d∥₂ is the **declared amplitude encoding**, not a repair of a supposedly already normalized state. The zero vector is rejected. Floating-point checks are not interval certificates.

Native execution here uses H/X/CX/CCX, RY/P for complex input tests, `Circuit.unitary` with a supplied dense matrix, `fq.run`, density/probability requests and terminal samples. Inspection of the installed public root/Circuit API did not find a dedicated `oracle`, `qram` or `qrom` service under those names. This does not deny that gates can implement a lookup: the examples execute exactly such implementations. Table validation, minterm synthesis, normalization, dense matrix construction, fingerprints and cost ledgers are book-side classical code. No live coherent database, hardware QRAM, device transport, free generic loading, automatic complexity proof or calibrated physical timing is established.

The helper deliberately restricts a and b to 1 or 2, and amplitude data to nonzero tuples of 2 or 4 nonnegative integers at most 16. These are teaching guards, not claims about maximum FlagQuantum circuit size or all possible encodings. The structured Gray implementation is independently checked on all basis address/value pairs in both modes by the fresh transfer. Larger controlled writes, sparse data access, general state-preparation synthesis and asymptotic query algorithms require their own declared constructions and costs.

**Understanding and transfer tasks**

- **14.4-A — interface.** Why must the XOR oracle work on nonzero z? Why does ordinary classical `table[i]` not specify its coherent action, phases or clean workspace?
- **14.4-B — cost.** For the displayed Gray table, count setup bits and logical gates for seven trials of three queries. State separately which costs are absent. Would replacing the table by a short formula automatically prove a hardware speedup?
- **14.4-C — fresh execution.** Use D=(3,1,2,0), validate addresses 00 and 11 with target values 00 and 10 in both modes, and check a fresh complex joint input. Prepare normalized d=(1,3,2,0) by the supplied dense construction and predict its probability vector before running. Keep state preparation and queries as separate access contracts.
- **14.4-D — failure analysis.** Can a state-only algorithm distinguish d from 2d to report their different exact sums? Can uncontrolled phase queries distinguish the constant predicates 0 and 1? What additional access would change each question?

<details markdown="1">
<summary>Answers and verification guidance for 14.4-A–D</summary>

**A.** The full reversible contract includes z XOR D_i for every b-bit target. Its permutation and self-inverse properties then determine the unitary action on superpositions by linearity. Classical entry reads give values on classical addresses; they do not specify a coherent physical operation or guarantee restored workspace. Phases and residual garbage can change interference even if basis output values look right.

**B.** The explicit data format has 4×2=8 bits. There are 7×3=21 abstract calls: 168 minterm implementation gates or 63 structured CX gates, excluding preparation, readout, host generation, synthesis, routing, updates and postprocessing. Bits, gates and seconds remain separate units. A short formula changes an implementation possibility, not by itself the speed of an actual device or the fairness of a baseline.

**C.** On address 00 the word is 11, so targets 00 and 10 become 11 and 01. On address 11 the word is 00 and targets are unchanged. The amplitude-data squared norm is 14; predicted probabilities are (1/14,9/14,4/14,0). The transfer compares full complex states/densities with the independent scalar map in both modes, as well as the marginal probabilities. The known structured Gray circuit is separately regressed on every basis pair.

**D.** State-only d and 2d are identical after normalization, so the specified input does not determine the original sum. Providing a norm, unnormalized numerical data or a value oracle changes that input model. Uncontrolled I and −I differ only by global phase for a fixed number of queries and give the same probabilities; explicitly supplied controlled access changes that interface. Neither extra resource follows automatically from the original weaker contract.

</details>

The frozen source target is Nielsen and Chuang, [*Quantum Computation and Quantum Information*, §6.1.1 “The oracle,” beginning on printed page 248](https://www.cambridge.org/highereducation/books/quantum-computation-and-quantum-information/01E10196D0A682A6AEFFEA52D53BE9AE). The existing record is a contents locator, not a full-text review. Its publisher edition page was checked; no full chapter inspection is claimed. For the actual basis-action/query convention, the primary accessible source [Watrous, *Quantum Computational Complexity*, §III.4, PDF pages 10–11](https://cs.uwaterloo.ca/~watrous/Papers/QuantumComputationalComplexity.pdf#page=10) was inspected. The input-model distinctions, dense preparation, concrete cost ledger and counterexamples above are stated and derived locally. They do not import an unproved quantum-search theorem.

The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/14.4.json) separates author execution from independent mathematical/implementation review and reader trial. This remains a working draft. Continue, when drafted, with [14.5 Accuracy, repetition, and success probability](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-5).

<!-- end-section-14.4 -->

<span id="sec-computational-models-complexity-and-quantum-advantage-5"></span>
## 14.5 Accuracy, repetition, and success probability

**Question.** How many repetitions are sufficient, and which implementation errors can repetition never remove?

The prerequisites are [6.8, fixed-design confidence bounds](ch-measurement-expectation-values-and-statistical-estimation.md#sec-measurement-expectation-values-and-statistical-estimation-8) and [14.3, bounded-error computation](#sec-computational-models-complexity-and-quantum-advantage-3). This **F-depth** section extends the constant-confidence discussion to explicit accuracy and failure targets. It proves variance and exponential majority bounds, relates implementation precision to probability bias, and constructs an independent-block estimator. The assumptions matter as much as the resulting integer budgets.

### 14.5.1 Name three different parameters

We will use these dimensionless quantities for a Bernoulli output:

- **Accuracy ε>0:** the allowed absolute error in a reported probability or mean.
- **Failure target 0<δ<1:** an upper bound on the probability that the prescribed procedure exceeds its allowed error or returns the wrong decision.
- **Success half-gap γ>0:** a lower bound on the base decision procedure's success probability above 1/2. Thus base success is at least 1/2+γ. The yes/no acceptance gap in a symmetric decision contract is 2γ.

Numerical precision is a fourth, implementation-dependent quantity: for example, an angle grid spacing or an operator-norm approximation error. It is not automatically equal to ε, δ or γ. A change in any of these can change the required work.

First distinguish an ideal target probability p from the actual fixed probability q sampled by the implemented circuit. Let B₁,…,B_N be independent identically distributed bits with mean q. Write

$$
\widehat q=\frac1N\sum_{i=1}^N B_i,
\qquad
\mathbb E[\widehat q]=q,
\qquad
\operatorname{Var}(\widehat q)=\frac{q(1-q)}N\leq\frac1{4N}.
$$

The variance identity follows by expanding the centered square: independence makes every cross covariance zero, and each Bernoulli variance is q−q². The inequality follows from q(1−q)=1/4−(q−1/2)²≤1/4. In the unbiased implementation q=p, Chebyshev from 6.8 gives

$$
\Pr\{ |\widehat q-p|>\epsilon\}
\leq\frac1{4N\epsilon^2}.
$$

Thus N≥ceil[1/(4δε²)] is sufficient. This is a conservative guarantee, not an assertion that every random record lies inside its target interval. The strict failure event is the complement of the closed accuracy interval; bounding the larger non-strict Chebyshev event is still valid.

```python
import math,itertools,torch,flagquantum as fq
from fractions import Fraction as F
from dataclasses import replace
from examples.foundations import accuracy_repetition as a,statistical_ensembles as e,uniform_reversible as u
epsilon,delta,bias=F(1,4),F(1,5),F(0)
n=a.mean_budget(epsilon,delta,bias);assert n==20
c=fq.Circuit(1,dtype=torch.complex128).RY(0,theta=2*math.pi/3)
r=fq.run(c,outputs=[fq.probabilities(name='p'),fq.samples(qubits=(0,),name='raw')],
    shots=n,options=replace(e.OPTIONS,seed=61))
e.close(r.measurement('p').value[0],torch.tensor([.25,.75],dtype=torch.float64))
raw=r.measurement('raw').value;assert raw.shape==(1,20,1) and bool(((raw==0)|(raw==1)).all())
estimate=F(int(raw.sum()),n);assert 0<=estimate<=1
print('Accuracy 1/4, failure 1/5, zero bias: 20 shots; native probabilities and raw counts checked.')
```

```text
Accuracy 1/4, failure 1/5, zero bias: 20 shots; native probabilities and raw counts checked.
```

The program checks the exact simulator probabilities and the raw record's shape/bit accounting. It deliberately does not assert that this particular estimate must be within ε of p. An occasional failure is permitted by a probabilistic guarantee.

### 14.5.2 Reserve part of the accuracy for bias

Assume a separate argument supplies a deterministic bound |q−p|≤β. This bound must come from the implementation/model contract, not be guessed from a favorable random record. The triangle inequality gives

$$
|\widehat q-p|\leq |\widehat q-q|+\beta.
$$

For 0≤β<ε, put t=ε−β>0. Exceeding the total accuracy ε requires a sampling deviation larger than t, so a sufficient shot count is

$$
\Pr\{|\widehat q-p|>\epsilon\}
\leq\frac1{4Nt^2},
\qquad
N\geq\left\lceil\frac1{4\delta(\epsilon-\beta)^2}\right\rceil.
$$

Holding δ fixed, halving the available statistical radius t multiplies this sufficient budget by four before integer rounding. If β≥ε, this argument supplies no positive radius; the budget helper rejects that request. This does not prove that every such implementation must fail, but it does mean the stated bias bound cannot justify the proposed accuracy by this method.

There is also a concrete failure mechanism. Suppose the actual offset is |q−p|=β>ε. Whenever an estimate is within ε of the ideal p, the reverse triangle inequality requires |q̂−q|≥β−ε. Therefore

$$
\Pr\{|\widehat q-p|\leq\epsilon\}
\leq\frac1{4N(\beta-\epsilon)^2}\longrightarrow0.
$$

This proof uses the same variance bound and needs no appeal to an unstated limit theorem. More repetitions concentrate the estimate around the wrong mean. Discrete coverage need not decrease at every successive N; the upper bound describes the eventual obstruction. The code compares two specified sample sizes using exact binomial sums, not an unsupported monotonicity assertion.

```python
n=a.mean_budget(F(1,4),F(1,10),F(1,8));assert n==160
_,estimate_biased=a.native_mean(F(5,8),n,mode='density_matrix')
c64=a.target_coverage(F(3,4),F(5,8),64,F(1,32))
c256=a.target_coverage(F(3,4),F(5,8),256,F(1,32))
assert c256<c64
print('Bias 1/8 leaves statistical radius 1/8: 160-shot conservative design.')
print('At target 3/4 but actual 5/8, exact coverage at radius 1/32 drops from N=64 to N=256.')
```

```text
Bias 1/8 leaves statistical radius 1/8: 160-shot conservative design.
At target 3/4 but actual 5/8, exact coverage at radius 1/32 drops from N=64 to N=256.
```

This is why “increase shots until stable” does not validate calibration, data loading or the model. Stability around q is not a certificate that q equals p.

### 14.5.3 Prove the majority variance bound at arbitrary confidence

Now consider a decision procedure whose **actual** success probability s satisfies s≥1/2+h, for a certified h>0. Execute M independent fresh repetitions on the same allowed classical input, with M odd. Let A_i indicate that repetition i is correct. In the proof those indicators refer to correctness; the algorithm need not know which individual answers are correct.

Majority is wrong only when \(\overline A=M^{-1}\sum_i A_i<1/2\). Since its mean is at least 1/2+h, this event requires a deviation of at least h. The same variance expansion yields

$$
\Pr\{\text{wrong majority}\}
\leq\frac1{4Mh^2}.
$$

Choose the least odd integer at least 1/(4δh²) to obtain error at most δ. Section 14.3's constant-confidence budget is the special case δ=1/3. Here the explicit dependence on both h and δ matters: if h shrinks with input size, it is not a constant hidden in the resource count.

For three bits, the majority bit is ab XOR ac XOR bc. A zero fourth qubit receives this bit through three CCX gates. We prepare three independent output bits of success probability 3/4, then validate the exact vote distribution and the raw vote relation. The comparison circuit prepares one bit and fans it out to the other two, preserving the same marginals while correlating all three records.

```python
# Three fresh answer qubits; fourth qubit receives their majority.
c=fq.Circuit(4,dtype=torch.complex128)
for j in (0,1,2):c.RY(j,theta=2*math.pi/3)
c.CCX(0,1,3).CCX(0,2,3).CCX(1,2,3)
r_vote=fq.run(c,outputs=[fq.probabilities(qubits=(3,),name='vote'),fq.samples(qubits=(0,1,2,3),name='raw')],
    shots=17,options=replace(e.OPTIONS,seed=61))
e.close(r_vote.measurement('vote').value[0],torch.tensor([5/32,27/32],dtype=torch.float64))
v=torch.zeros(16,dtype=torch.complex128)
for bits in itertools.product((0,1),repeat=3):
    s=sum(bits);v[u.index(bits+(int(s>=2),))]=math.sqrt(.75)**s*math.sqrt(.25)**(3-s)
e.close(r_vote.statevector()[0],v)
bits=r_vote.measurement('raw').value;assert bits.shape==(1,17,4)
assert bool((bits[0,:,3]==(bits[0,:,:3].sum(dim=1)>=2)).all())
_,shared_error=a.native_vote(F(3,4),independent=False,mode='density_matrix')
assert shared_error==F(1,4) and a.variance_budget(F(1,4),F(1,20))==81
print('Three independent votes: error 5/32; shared source: error 1/4; variance-bound budget: 81.')
```

```text
Three independent votes: error 5/32; shared source: error 1/4; variance-bound budget: 81.
```

For the shared source, every repetition agrees with the first; the error stays 1/4. More generally,

$$
\operatorname{Var}(\overline A)
=\frac1{M^2}\left(\sum_i\operatorname{Var}(A_i)
+2\sum_{i<j}\operatorname{Cov}(A_i,A_j)\right).
$$

With identical copies A_i=A, this equals Var(A), not Var(A)/M. The ideal product preparation in the first circuit justifies the independent model. A single experimental record, or replaying a seed, does not establish hardware independence. Known classical inputs can be copied before independent circuit execution as explained in 14.3; this is not a license to clone unknown quantum inputs or reuse one random output as independent evidence.

### 14.5.4 Prove an exponential majority bound

The variance bound is sufficient but loose at small δ. We can obtain logarithmic dependence on 1/δ with a separate complete argument. Let E_i=1−A_i be the error bit and q_e=Pr(E_i=1)≤q₀=1/2−h. Assume first 0<h<1/2. A wrong odd majority has at least M/2 error bits. For any λ>0, apply Markov's inequality to the nonnegative variable exp(λ∑E_i):

$$
\begin{aligned}
\Pr\{\text{wrong majority}\}
&\leq e^{-\lambda M/2}\,\mathbb E\exp\!\left(\lambda\sum_iE_i\right)\\
&=\left[e^{-\lambda/2}\bigl(1-q_e+q_e e^\lambda\bigr)\right]^M\\
&\leq\left[e^{-\lambda/2}\bigl(1-q_0+q_0 e^\lambda\bigr)\right]^M.
\end{aligned}
$$

The equality uses independence to factor the expectation into M one-bit expectations. The last inequality holds because e^λ−1>0, so that expectation increases with q_e. Choose λ=ln[(1−q₀)/q₀]>0. Then q₀e^λ=1−q₀, and the bracket is 2√[q₀(1−q₀)]. Consequently,

$$
\Pr\{\text{wrong majority}\}
\leq (1-4h^2)^{M/2}
\leq e^{-2Mh^2}.
$$

For completeness, ln(1−u)≤−u on 0≤u<1: the derivative of ln(1−u)+u is −u/(1−u)≤0 and its value at zero is zero. Apply this with u=4h² to obtain the final inequality. This one-line real-calculus bridge explains the exponential estimate rather than treating it as a numerical fit. At h=1/2 every trial succeeds with certainty, so majority error is zero and one repetition suffices; no infinite logarithm need be evaluated.

For 0<h<1/2 it is sufficient to take odd

$$
M\geq\frac{\ln(1/\delta)}{2h^2}.
$$

For rational designs, the helper avoids a potentially ambiguous floating-point log/ceiling decision by using the stronger first bound: it selects the first odd M satisfying the **exact rational inequality**

$$
(1-4h^2)^M\leq\delta^2.
$$

This is a sufficient moment-bound budget, not the smallest M satisfying the true error target. At h=1/4 and δ=1/20, the variance budget is 81, the exact moment-bound budget is 21, and the simpler e-bound suffices with 25. For the particular IID Bernoulli source s=3/4, direct enumeration of the binomial law gives a smaller exact minimum of 9. Each statement names the guarantee it actually uses.

For that fixed source, the exact error law is

$$
\Pr\{\text{wrong majority}\}
=\sum_{j=0}^{(M-1)/2}\binom Mj s^j(1-s)^{M-j}.
$$

Indeed, each M-bit record with j successes has probability sʲ(1−s)ᴹ⁻ʲ, and exactly binomial(M,j) records have that count. These disjoint events give the sum. The code's exact minimum refers only to this fixed law; it is not an optimality theorem for quantum algorithms.

```python
h,delta=F(1,4),F(1,20)
m=a.moment_budget(h,delta);assert m==21 and (1-4*h*h)**m<=delta**2
assert a.majority_error(F(3,4),m)<=delta
assert a.minimal_fixed_majority(F(3,4),delta)==9
assert a.majority_error(F(3,4),7)>delta
print('Exact moment-bound budget: 21; fixed p=3/4 exact binomial minimum: 9; 7 fails the target.')
```

```text
Exact moment-bound budget: 21; fixed p=3/4 exact binomial minimum: 9; 7 fails the target.
```

The threshold M≤501 is a host exact-arithmetic teaching guard. It does not restrict the theorem or FlagQuantum. The bound improves confidence only under the declared independence and positive-gap assumptions.

### 14.5.5 Translate implementation precision into probability error

Sampling and majority cannot correct an unbudgeted change to the circuit. Here is a sufficient deterministic connection. Let ideal and implemented unitary chains be U=U_L…U₁ and V=V_L…V₁, with phase conventions fixed and

$$
\|V_j-U_j\|_{\mathrm{op}}\leq\eta_j.
$$

Insert and subtract successive hybrid products. The result is the telescoping identity

$$
V-U=\sum_{j=1}^L
V_L\cdots V_{j+1}(V_j-U_j)U_{j-1}\cdots U_1.
$$

One can verify it by expanding each parenthesis: the negative term of one hybrid cancels the positive term of its neighbor, leaving V−U. Empty products at the endpoints mean identity. All other factors are unitary and have operator norm one; the triangle inequality gives ∥V−U∥_op≤∑η_j. If the normalized prepared input itself differs from its ideal input by at most η_prep in vector norm, add and subtract V acting on the ideal input to obtain

$$
\|\phi-\psi\|_2\leq\eta_{\mathrm{prep}}+\sum_j\eta_j,
$$

where ψ is the ideal final vector and φ the implemented final vector. For any measurement effect 0≤E≤I, expand the expectation difference as

$$
\begin{gathered}
\langle\phi|E|\phi\rangle-\langle\psi|E|\psi\rangle\\
=\langle\phi-\psi|E|\phi\rangle
+\langle\psi|E|\phi-\psi\rangle.
\end{gathered}
$$

Cauchy–Schwarz, ∥E∥_op≤1 and normalized φ,ψ bound the magnitude by 2∥φ−ψ∥₂. Therefore a sufficient event-probability bias bound is

$$
\beta\leq2\left(\eta_{\mathrm{prep}}+\sum_j\eta_j\right).
$$

The expression can exceed one and then be uninformative; it is still an upper bound. It is not a numerical renormalization rule. A sampled residual, an unverified SVD norm or a framework tolerance is not automatically a rigorous certificate for the η_j. The statement assumes unitary implementations and a fixed measurement effect. General noise and readout-model errors require their own bounds.

In the native illustration, exact H gates bracket a sequence of RZ rotations. An angle offset d_j radians gives

$$
\|R_Z(\theta_j+d_j)-R_Z(\theta_j)\|_{\mathrm{op}}
=2|\sin(d_j/4)|\leq |d_j|/2.
$$

This follows directly from the two diagonal entries e^(±iθ/2). The sine inequality follows from sin x=∫₀ˣcos t dt and |cos t|≤1. We track the full matrix convention rather than reducing angles modulo 2π or aligning phases after execution. These RZ rotations commute, so their total angle also supplies an independent analytic reference.

With a nearest-point angle grid of step Δ=2⁻ᵇ radians, |d_j|≤Δ/2. For L such rotations and no other errors, the sufficient bound becomes β≤LΔ/2. Thus choosing b with L2⁻ᵇ/2≤β_budget prices the required **fractional angle bits**. Integer/exponent storage, synthesis cost and device accuracy remain separate. For L=32 and β_budget=1/32, the least such b is 9.

```python
c=fq.Circuit(1,dtype=torch.complex128).H(0)
c.RZ(0,theta=.4+.02).RZ(0,theta=.5-.01).H(0)
r_precision=fq.run(c,outputs=[fq.probabilities(name='p')],options=e.OPTIONS)
q_ideal=math.sin(.9/2)**2;q_actual=math.sin(.91/2)**2
local_norms=2*abs(math.sin(.02/4))+2*abs(math.sin(-.01/4))
assert abs(q_actual-q_ideal)<=2*local_norms
e.close(r_precision.measurement('p').value[0],torch.tensor([1-q_actual,q_actual],dtype=torch.float64))
e.close(r_precision.statevector()[0],torch.tensor([math.cos(.91/2),-1j*math.sin(.91/2)],dtype=torch.complex128))
assert a.grid_bits(32,F(1,32))==9
_,bad_precision=a.phase_chain((2*math.pi/3,),(-math.pi/3,),mode='density_matrix')
assert abs(bad_precision['ideal']-.75)<1e-12 and abs(bad_precision['actual']-.25)<1e-12
print('Native RZ chain obeys the analytic operator/event bound; 32-rotation grid budget: 9 fractional bits.')
print('A persistent angle error changes ideal success 3/4 to actual 1/4; more shots do not repair it.')
```

```text
Native RZ chain obeys the analytic operator/event bound; 32-rotation grid budget: 9 fractional bits.
A persistent angle error changes ideal success 3/4 to actual 1/4; more shots do not repair it.
```

The small-offset circuit checks the analytic bound. The deliberately large offset changes ideal success 3/4 to actual success 1/4. This is an implementation-model discrepancy, not a random fluctuation to be removed by increasing shots. Floating-point execution of the chosen angles validates the example; it does not certify all devices or all quantized angle inputs.

### 14.5.6 Budget the surviving gap before choosing repetitions

Suppose the ideal decision procedure has success at least 1/2+γ and a separate argument bounds its success-probability change by β. Then actual success is at least 1/2+γ−β. To use either majority theorem, we need

$$
h=\gamma-\beta>0.
$$

Insert this **surviving** half-gap into the budget. Using γ while ignoring β can underestimate the repetitions. For γ=1/4 and β=1/8, the moment-bound budget at δ=1/20 increases from 21 to 93. If β≥γ, the helper refuses to manufacture a majority guarantee. It is not claiming that no better implementation could work; it is refusing a guarantee from insufficient assumptions.

```python
h=a.effective_gap(F(1,4),F(1,8));assert h==F(1,8)
assert a.moment_budget(h,F(1,20))==93
_,degraded=a.native_vote(F(5,8),mode='density_matrix')
_,wrong=a.native_vote(F(1,4))
assert degraded==F(81,256) and wrong==F(27,32)
print('Bias halves the guaranteed gap: moment budget rises from 21 to 93.')
print('Actual base success 5/8 gives three-vote error 81/256; base success 1/4 gives error 27/32.')
```

```text
Bias halves the guaranteed gap: moment budget rises from 21 to 93.
Actual base success 5/8 gives three-vote error 81/256; base success 1/4 gives error 27/32.
```

If actual base success falls below one half, majority can favor the wrong label: in the shown three-trial example its error grows from 3/4 to 27/32. The measured output bit must be related to correctness by the task's specification; relabeling a wrong circuit's most frequent outcome is not a general repair when the correct answer is unknown.

If an implementation bound can itself fail with probability δ_impl, a combined guarantee needs a uniform statistical bound over every admitted implementation satisfying that bound. With such a contract, the failure events give δ_total≤δ_impl+δ_stat. This is not obtained by conditioning on a favorable observed record. Correlated calibration errors shared across trials are precisely why the implementation premise must be stated separately.

### 14.5.7 Amplify numerical accuracy with independent blocks

The direct mean's variance bound is proportional to 1/δ. That is a property of the selected bound, not a lower bound on estimation. We can combine the two proved tools to obtain logarithmic confidence dependence for numerical estimation as well.

Reserve β<ε and let t=ε−β. Split the experiment into M independent blocks, each of fixed size

$$
n_0=\max\{1,\lceil t^{-2}\rceil\}.
$$

Each block mean has deviation greater than t from the actual q with probability at most 1/(4n₀t²)≤1/4. Call a block **good** when its mean lies in [q−t,q+t]. The good-block indicators are independent because the underlying trial groups are independent, and each has success probability at least 3/4.

Take M odd and report the median of the M block means. If more than half the blocks are good, the median lies inside [q−t,q+t]: a median below the lower endpoint would require at least (M+1)/2 block means below it, and similarly for a median above the upper endpoint. Either case contradicts a good majority. Hence the probability that the median exceeds total accuracy ε around p is at most the bad-majority probability, because the triangle inequality adds only β.

Apply the moment bound with h=1/4:

$$
\Pr\{|\operatorname{median}-p|>\epsilon\}
\leq(3/4)^{M/2}\leq e^{-M/8}.
$$

An exact rational choice satisfying (3/4)^M≤δ² suffices. The total sample count is n₀M, growing as a sufficient order of (ε−β)⁻²[1+ln(1/δ)] in the small-accuracy regime. At ε=1/4, β=0, δ=1/20, our design uses 21 blocks of 16 samples, or 336 samples. The direct Chebyshev mean would use 80 samples at these particular constants. Better asymptotic dependence on δ does not guarantee smaller budgets at every finite parameter choice.

```python
t=F(1,4);n0=math.ceil(1/t**2);m=a.moment_budget(F(1,4),F(1,20))
assert (n0,m,n0*m)==(16,21,336)
r_blocks,median=a.median_blocks(F(3,4),n0,m,mode='density_matrix')
assert r_blocks.measurement('raw').value.shape==(1,336,1) and 0<=median<=1
print('Median of means: 21 independent blocks of 16 samples, 336 total; block accounting checked.')
```

```text
Median of means: 21 independent blocks of 16 samples, 336 total; block accounting checked.
```

The median calculation is explicit host postprocessing of native records. All group sizes and the number of groups are fixed before observing them. The result is not a native confidence-interval endpoint, an adaptive stopping theorem or a certificate of hardware independence. Persistent bias remains after taking medians just as it does after taking means.

### 14.5.8 Separate verified success, total failure and execution evidence

A different repetition task is “obtain at least one **verifiably** successful candidate.” With independent attempts of success probability s>0 and a reliable success flag, R fixed attempts all fail with probability (1−s)^R. This follows by multiplying their failure probabilities; its complement is the probability of at least one success. A sufficient finite cap is the first R satisfying

$$
(1-s)^R\leq\delta.
$$

For s=1/4 and δ=1/20 this is R=11, even though s is below one half. The rule requires a verifier that tells which candidate succeeded. Without it, a collection containing a correct answer need not identify that answer, and an “any success” probability cannot replace a majority correctness guarantee. In the toy record the task defines output 1 itself as the success flag; this does not construct a verifier for an arbitrary computational problem.

For K events, each with justified failure bound δ_j, the union bound gives

$$
\Pr\{\text{any failure}\}\leq\sum_{j=1}^K\delta_j.
$$

This follows from the pointwise inequality that the indicator of a union is at most the sum of its event indicators, then taking expectations. Independence between these K failure events is unnecessary; independence was needed **inside** the earlier repetition arguments. Allocate δ_j before running. In adaptive settings, a bound used for a subroutine needs to hold uniformly for its admitted inputs/history; selective reporting of the successful calls is not such a contract.

```python
r=a.verified_budget(F(1,4),F(1,20));assert r==11 and F(3,4)**r<=F(1,20)
a.native_mean(F(1,4),r)
assert F(3,4)**(r-1)>F(1,20)
assert F(1,50)+F(2,25)==F(1,10)
per_call=F(1,10)/3
assert sum((per_call for _ in range(3)),F(0))==F(1,10)
assert a.invalid_checks()==17
print('Verified success needs 11 fixed attempts at p=1/4; a success flag is required to select a winner.')
print('Three failure budgets of 1/30 sum to 1/10; 17 malformed contracts rejected before execution.')
```

```text
Verified success needs 11 fixed attempts at p=1/4; a success flag is required to select a winner.
Three failure budgets of 1/30 sum to 1/10; 17 malformed contracts rejected before execution.
```

The complete companion is [accuracy_repetition.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/accuracy_repetition.py). Run from the repository root in the pinned example environment:

```bash
python examples/foundations/accuracy_repetition.py
python scripts/check_accuracy_repetition_prose.py
```

Expected output of the complete program:

```text
84 native CPU complex128 circuits: 36 raw-mean, 24 independent/shared-vote, 12 phase-chain and 12 median-block cases passed.
Both modes: full deterministic probabilities/densities and raw-record accounting checked; no one-record confidence or majority-success assertion.
At half-gap 1/4 and failure 1/20: variance budget 81, exact moment-bound budget 21, fixed-p=3/4 exact binomial minimum 9.
Bias-aware mean budget 160; 32-rotation grid needs 9 fractional bits for event budget 1/32; verified-success budget 11.
17 malformed contracts rejected; calibration, independence and rigorous bias certificates are assumptions, not inferred from samples.
```

The restored runtime is Python 3.12.14, FlagQuantum 0.3.1 and PyTorch 2.13.0, CPU complex128. Both statevector and density-matrix modes execute the declared preparations; deterministic probability/density comparisons use absolute tolerance 10⁻¹² and relative tolerance zero. Statevector mode additionally checks phase-fixed complex vectors for the vote and phase-chain cases. References use scalar product amplitudes, the explicit majority permutation and analytic RZ formulas, not native gate-list introspection. Exact budgets and finite binomial references use `Fraction`. No phase alignment, clipping, norm repair or interval certificate is introduced.

Actual API calls are `Circuit.RY/H/RZ/CX/CCX`, `fq.run`, `fq.probabilities`, `fq.density_matrix` and `fq.samples`. A terminal `shots=N` request supplies N ideal sample records from the simulator's output distribution; it is not N separately timed hardware executions, resets or host calls. The execution ledger counts circuit invocations separately from statistical trials. Seed replay is a debugging facility and is not additional independent evidence. The hand-written mean, median, majority budgets, exact binomial analysis and angle-grid design are book-side code. No framework calibration certificate, native confidence theorem, hardware IID guarantee, noise model or physical runtime improvement is established by these tests.

The native shot cap 10000, exact binomial/moment search cap 501, phase-chain length cap 8 and grid gate-count cap 10000 are teaching limits, not FlagQuantum scalability limits. Nonfinite aggregate angles, nonpositive gaps, accuracy exhausted by bias, even majority counts and malformed design inputs are rejected. The exact small median fixture sums finite block distributions; it is not a quantum execution. A random record or vote is never required to succeed as a deterministic test of its probability guarantee.

**Understanding and transfer tasks**

- **14.5-A — parameters and units.** Why is an algorithm's half-gap not the same as an estimator's accuracy? If the available statistical radius is halved, what happens to the direct variance budget? Does changing float precision automatically provide a bound on β?
- **14.5-B — proof and assumptions.** Reproduce the exponential-moment factorization and the choice of λ. Identify exactly where independence is used. What replaces the mean variance if every repetition copies the same random bit?
- **14.5-C — fresh execution.** Use new sources s=7/10 and 9/10, sample sizes 41 and 127, and both modes. Compare independent/shared three-vote circuits at s=7/10. Run a four-RZ chain with ideal angles (−.2,.3,.7,−.4) and offsets (.01,−.02,.005,.004). For a median design with t=1/5 and δ=1/50, compute block size and block count before collecting data. Compare an independent exact seven-bit record enumeration with the binomial reference.
- **14.5-D — full guarantees.** For L=32 rotations and event-bias budget 1/32, derive the grid-bit requirement. If γ=1/4 and β=1/8, which gap belongs in the repetition bound? Why can an eleven-attempt “any success” calculation be inappropriate for unknown yes/no answers?

<details markdown="1">
<summary>Answers and verification guidance for 14.5-A–D</summary>

**A.** γ is a margin above random guessing for a decision task; ε is a numerical deviation tolerance for a reported mean. Neither determines the other without a task-specific reduction. Halving t multiplies the direct sufficient variance budget by four before rounding. Floating-point format alone does not certify preparation, synthesis, calibration or readout errors; β needs its own argument.

**B.** Markov bounds exp(λ∑E_i); independence factors its expectation into one-bit terms. Replacing q_e by q₀=1/2−h bounds each factor, and λ=ln[(1−q₀)/q₀] gives the bracket 2√[q₀(1−q₀)]. Shared copies have all covariances equal to Var(A), so Var(average)=Var(A), not Var(A)/M. Marginals alone are insufficient.

**C.** The four-rotation ideal total is .4 radians and the implemented total is .399 radians. The median design has block size 25, moment-bound count 29 and total 725 samples. No one generated median is required to lie inside the target interval. The fresh exact seven-vote enumeration and three-block median fixture are classical references; the transfer has 16 native executions, including the new circuit parameters in both modes.

**D.** Each rounded angle differs by at most Δ/2; each rotation has operator error at most Δ/4, so event bias is bounded by LΔ/2. The inequality 32×2⁻ᵇ/2≤1/32 gives b≥9. The surviving half-gap is 1/8, whose exact moment-bound count at δ=1/20 is 93. “At least one correct answer exists” does not tell the program which answer is correct without a verifier. The applicable majority bound instead depends on a justified success margin above 1/2.

</details>

The frozen source is Boyd and Vandenberghe, [*Convex Optimization*, §7.4](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf#page=388): §7.4.1 begins on printed page 374, and the exponential Markov formulation in §7.4.2 is on printed page 379. The author-hosted PDF was downloaded and PDF pages 388–389 and 393 were inspected in this pass; its SHA256 matches the frozen seventh-printing source record. Primary indexed page text was also checked. The section supplies its own full Bernoulli majority, bias, precision and block-median arguments. It does not import general convex optimization results as undeclared prerequisites. No third-party textbook text is included in the repository.

The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/14.5.json) distinguishes author execution from independent mathematical/implementation review and reader trial. It remains a working draft. Continue, when drafted, with [14.6 Complete resource accounting](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-6).

<!-- end-section-14.5 -->

<span id="sec-computational-models-complexity-and-quantum-advantage-6"></span>
## 14.6 Complete resource accounting

**Question.** What must be counted before a small quantum kernel becomes a resource claim for a complete task?

The prerequisites are [14.1, input and computational models](#sec-computational-models-complexity-and-quantum-advantage-1), [14.4, access models](#sec-computational-models-complexity-and-quantum-advantage-4) and [14.5, accuracy and repetition](#sec-computational-models-complexity-and-quantum-advantage-5). This F-depth section proves compositional cost and error rules. The rules hold in a **declared model**; they cannot supply missing gate durations, connectivity, a loading mechanism or calibrated error bounds.

Our worked task estimates the odd-parity probability of n independently prepared qubits. The classical input is a list of n finite angles θⱼ in radians, with a specified representation; the answer is a rational frequency from R terminal records. R is fixed before sampling. We count continuous RY and CX as named logical gates, with unit logical duration and all-to-all availability. Initialization and terminal measurement are counted separately. These conventions are adequate for this model calculation, not a finite-alphabet synthesis or physical implementation estimate.

### 14.6.1 Compose costs with matching units

A resource is defined by its unit and its boundary. Let a **work vector** be

$$
\mathbf c=(G,Q,I,M,B_{\rm in},B_{\rm out}),
$$

where G counts logical gates, Q abstract oracle calls, I individual qubit initializations, M measured qubits, and the last two coordinates count classical payload bits read and written. G and Q are separate coordinates: an oracle call is not silently identified with a single elementary gate. A measurement on k qubits contributes k to M under this convention, even if one runtime request returns them together. Here input/output payload bits cross the declared task interface; they are not a count of all internal memory or controller traffic. Payload bits exclude framing and object overhead, which require their own record if relevant.

For serial stages A then B, define c(A;B)=c(A)+c(B), component by component, provided B's input contract is met by A's output. To prove additivity, label every primitive counted event by its stage. The two labeled sets are disjoint, so each coordinate's event count is the sum of the two cardinalities. Applying this argument to the first k stages and then stage k+1 proves the rule for any finite list by induction. The empty list has zero work, and addition is associative because integer addition is associative. A declared setup stage used once and a trial repeated R times therefore give

$$
\mathbf c_{\rm task}=\mathbf c_{\rm setup}+R\mathbf c_{\rm trial}+\mathbf c_{\rm post}.
$$

This equality counts the specified implementation. Recompiling, caching, algebraic cancellation or changing the task boundary can change the implementation and must produce a new ledger. Shared data read only once belongs to setup, not automatically to every trial. Conversely, preparing the quantum input again for each independent trial belongs to every trial.

```python
from fractions import Fraction as F
from dataclasses import replace
import math,torch,flagquantum as fq
from examples.foundations import resource_accounting as r
from examples.foundations import statistical_ensembles as e,oracle_access as q
setup=r.Work(read_bits=192);trial=r.Work(gates=6,prepared=4,measured=1,write_bits=1)
total=setup+trial.scale(80)
assert total==r.Work(gates=480,prepared=320,measured=80,read_bits=192,write_bits=80)
assert (setup+trial)+trial==setup+(trial+trial)
print('Typed serial work: 480 gates, 320 initialized qubits across preparations, 80 measured bits, 192 input bits and 80 record bits.')
```

```text
Typed serial work: 480 gates, 320 initialized qubits across preparations, 80 measured bits, 192 input bits and 80 record bits.
```

Peak space does **not** follow this sum rule. If A and B reuse an allocation after A has released its temporary qubits and B's initialization contract has been restored, peak space is at most max(W_A,W_B), including any persistent registers in both widths. Simultaneous disjoint allocations instead require their sum. An unknown entangled workspace cannot be declared released and replaced by zero for free; the cleanup proof in 5.4 or an explicitly charged physical preparation/reset mechanism is needed.

### 14.6.2 Derive depth from dependencies rather than gate count

For the following gate-list model, gates take one time slot, gates sharing a qubit keep their listed order, and gates on disjoint qubits may overlap. There are no other constraints. Let P(j) contain the immediately preceding gate on each qubit used by gate j. Set the finish layer of an absent predecessor to zero and define

$$
\ell_j=1+\max_{i\in P(j)}\ell_i,\qquad
D=\max_j\ell_j,
$$

using max(empty)=0 and D=0 for an empty circuit. Every legal schedule must finish j at least one layer after every predecessor; induction on the gate list proves its finish time is at least ℓⱼ. Conversely place j in layer ℓⱼ. Two gates sharing a qubit have a predecessor chain between them and hence strictly increasing layers, so this placement has no shared-qubit collision and respects every constraint. It attains the lower bound D. This is a proof of optimal depth **for this fixed dependency graph**, not over all equivalent circuits or hardware schedules.

The helper implements the recurrence by keeping the latest finish layer for each qubit. The independent native structural analysis agrees on this circuit:

```python
supports=((0,),(1,),(2,),(0,3),(1,3),(2,3))
finish,depth=r.layers(supports,4)
c=fq.Circuit(4,dtype=torch.complex128)
for j,t in enumerate((.2,.4,.6)):c.RY(j,theta=t)
for j in range(3):c.CX(j,3)
analysis=c.analysis()
assert finish==(1,1,1,2,3,4) and depth==analysis.depth==4
assert analysis.n_instructions==6 and analysis.gate_counts=={'ry':3,'cx':3}
assert tuple(tuple(op.wires)for op in c.to_ir().instructions)==supports
print('Native IR: three RY plus three CX; independent finish layers (1,1,1,2,3,4), depth 4.')
```

```text
Native IR: three RY plus three CX; independent finish layers (1,1,1,2,3,4), depth 4.
```

For serial stages separated by a barrier, their depths add. Without a barrier the concatenated graph may permit overlap: two one-gate stages on disjoint qubits have depths one and one but combined depth one. Thus the sum of depths is a valid sequential schedule bound, not an unconditional minimum. Gate commutation does not automatically remove a shared-qubit scheduling constraint in this declared model. Physical durations or limited connectivity would change the graph or the recurrence.

### 14.6.3 Include preparation and readout in a complete small task

Start n data qubits and output qubit qₙ at zero. Prepare each data qubit with RY(θⱼ), then call CX(j,n) for j=0,…,n−1. On a computational basis component x=(x₀,…,xₙ₋₁), the CX sequence writes z=⊕ⱼxⱼ. Therefore the full final pure state is

$$
|\Psi\rangle=
\sum_{x\in\{0,1\}^n}
\left[\prod_{j=0}^{n-1}
\bigl(\cos(\theta_j/2)\bigr)^{1-x_j}
\bigl(\sin(\theta_j/2)\bigr)^{x_j}\right]
|x\rangle|\mathop{\oplus}_j x_j\rangle.
$$

A scalar reference for the output is obtained without executing the gate list. For independent bits Xⱼ with Pr(Xⱼ=1)=sin²(θⱼ/2), the sign of parity is the product of the signs of the bits. Factor the finite sum over x to get

$$
\begin{aligned}
\mathbb E[(-1)^z]
 &=\prod_j\mathbb E[(-1)^{X_j}]
 =\prod_j\cos\theta_j,\\
p_{\rm odd}
 &=\frac{1-\prod_j\cos\theta_j}{2}.
\end{aligned}
$$

This task is chosen to expose costs, not to claim quantum advantage: the displayed product also gives a direct classical reference using n cosine factors. A fair performance comparison would charge its numerical evaluation and accuracy too.

The first equality uses the product preparation; it would not hold for an arbitrary correlated input. The second uses E[(-1)ᶻ]=Pr(z=0)−Pr(z=1)=1−2p_odd. The companion checks the complete amplitude vector, density and this scalar probability, not only one sampled frequency. Here are actual native execution and terminal requests on the circuit just built:

```python
native=fq.run(c,outputs=[fq.probabilities(qubits=(3,),name='out'),
    fq.samples(qubits=(3,),name='raw')],shots=80,options=e.OPTIONS)
expected=(1-math.prod(math.cos(t)for t in (.2,.4,.6)))/2
e.close(native.measurement('out').value[0],torch.tensor([1-expected,expected],dtype=torch.float64))
raw=native.measurement('raw').value
assert raw.shape==(1,80,1) and bool(((raw==0)|(raw==1)).all())
print('Explicit native RY/CX preparation: analytic parity probability and 80 terminal one-bit records checked.')
```

```text
Explicit native RY/CX preparation: analytic parity probability and 80 terminal one-bit records checked.
```

One trial uses n RY plus n CX, W=n+1 qubits, I=n+1 initializations and one selected measured qubit. All RY gates can occupy the first layer; the n CX gates form a chain through the output qubit. For n≥1, G=2n and D=n+1. For n=0 the empty parity is zero, G=D=0, but requesting records still uses the one output qubit. The output qubit is measured, not cleaned for coherent reuse. The initialization assumption is explicit; this code does not demonstrate a reset operation on hardware.

### 14.6.4 Charge repetitions and state a concurrency contract

For a zero-bias estimate with ε=1/4 and δ=1/20, the sufficient variance budget from 14.5 is R=80. At n=3 a serial implementation consequently has 480 gate applications, 320 individual qubit initializations, 80 selected measured bits and peak width four. The same four qubits may be reused between properly initialized trials; 320 initializations does not mean 320 simultaneous qubits.

Suppose P disjoint copies are available, with no shared control, loading or readout bottleneck. Assign trials to successive batches of at most P. The number of batches is ⌈R/P⌉: fewer batches have capacity less than R, while filling all but the final batch attains this number. A schedule using P copies thus obeys

$$
G_{\rm total}=RG,\qquad
W_{\rm peak}=PW,\qquad
D_{\rm schedule}\le\lceil R/P\rceil D.
$$

Here P≤R and the width counts allocated copies. The depth bound is achievable in the stipulated unit-duration model; it excludes initialization/readout latency, which have separate counts. If they had known durations, each batch would include those durations too. This construction proves a work/space/schedule tradeoff, not a speedup measured on the present CPU.

```python
serial=r.repeat_plan(3,80,bits=64);parallel=r.repeat_plan(3,80,parallel=4,bits=64)
assert serial['total'].gates==parallel['total'].gates==480
assert (serial['peak_qubits'],serial['depth_bound'])==(4,320)
assert (parallel['peak_qubits'],parallel['depth_bound'])==(16,80)
assert serial['native_invocations']==1 and serial['total'].prepared==320
r.simulate((.2,.4,.6),80);r.simulate((.2,.4,.6),80,mode='density_matrix')
print('80 ideal trials: serial peak 4/depth 320; four-way peak 16/depth 80; both have 480 logical gates.')
print('One simulator run per record batch is distinct from 80 conceptual fresh preparations.')
```

```text
80 ideal trials: serial peak 4/depth 320; four-way peak 16/depth 80; both have 480 logical gates.
One simulator run per record batch is distinct from 80 conceptual fresh preparations.
```

The auditable n=3, R=80 ledger is:

| Quantity and unit | One trial | Serial trials | Four allocated copies |
| --- | ---: | ---: | ---: |
| RY logical gates | 3 | 240 | 240 |
| CX logical gates | 3 | 240 | 240 |
| Individual qubit initializations | 4 | 320 | 320 |
| Selected measured qubits | 1 | 80 | 80 |
| Raw selected payload bits | 1 | 80 | 80 |
| Peak allocated qubits | 4 | 4 | 16 |
| Scheduled gate layers | 4 | 320 | 80 |
| Physical elapsed time | unspecified | unspecified | unspecified |

The angle payload is 192 bits read once and the circuit is built once in this reuse contract. The parallel column is a model schedule, not an executed parallel hardware benchmark.

**A simulator invocation is another unit.** In these ideal terminal-sampling examples one `fq.run(...,shots=R)` prepares a simulated state and produces R records. It need not apply every simulated gate R times. The logical experiment model counts R fresh preparations; the author execution ledger counts actual calls to `fq.run`. Neither number should be substituted for the other. Batch size, shots, logical trials and independent hardware runs are different declarations. Reusing a seed is reproducibility, not additional statistical evidence.

### 14.6.5 Replace a query by its implementation exactly once

Let an outer circuit use G₀ non-oracle gates and Q queries per trial. Suppose a chosen oracle implementation has g gates per call, with setup payload B. Concatenating Q copies of its gate list with the outer list gives

$$
G_{\rm task}=R(G_0+Qg),\qquad
Q_{\rm task}=RQ,\qquad B_{\rm setup}=B.
$$

The gate equality follows by counting outer and substituted gates separately. It assumes the same implementation and no cross-boundary optimization; with such optimization it is an upper bound for the unoptimized construction. Counting Q again as elementary gates would double-count the same implementation. Leaving Q unexpanded is legitimate only as an **oracle-model** report, with the omitted implementation cost visibly named.

For the Gray table from 14.4, a structured oracle uses three CX gates. Its minterm realization uses four X and four CCX calls, hence eight named gates in that different logical alphabet. With G₀=4, Q=2 and R=80, the two gate totals are 800 and 1600 although both reports have 160 queries. This comparison does not assign equal physical duration or synthesis cost to CX and CCX.

```python
cost=r.substitute(4,2,3,80,8)
assert cost=={'queries':160,'logical_gates':800,'setup_bits':8}
_,gray=q.execute((0,1,3,2),2,2,i=2,y=1)
assert gray['gates']==8
# The same Gray oracle has a structured implementation with just three CX gates.
assert 80*(4+2*8)==1600 and cost['logical_gates']==800
print('160 abstract queries: structured implementation gives 800 task gates; minterm implementation gives 1600, with the same query count.')
```

```text
160 abstract queries: structured implementation gives 800 task gates; minterm implementation gives 1600, with the same query count.
```

An inverse or controlled oracle requires its own stated implementation and cost. A data update may invalidate setup and require rebuilding it. If U updates each cost S_update in some declared common unit, that unit's deterministic ledger becomes S_setup+U S_update+R C_trial+C_post. No assumption about free coherent memory access is hidden in that equality.

### 14.6.6 Prove a compositional failure budget, including adaptive calls

Let Fⱼ be a bad event at stage j in a fixed finite list of K calls. For any outcome ω, the indicator of the union is at most the sum of the indicators. Taking expectations proves

$$
\Pr\!\left(\bigcup_{j=1}^K F_j\right)
\le\sum_{j=1}^K\Pr(F_j)
\le\sum_{j=1}^K\delta_j.
$$

No independence between the bad events is used. This composition rule requires a correctness implication: if no named bad event occurs, the complete task satisfies its declared output/accuracy contract. Otherwise an omitted failure mechanism remains outside the guarantee.

Adaptive stages need care because a later call may receive a different input after an earlier failure. Let Hⱼ₋₁ denote the previous classical history and Gⱼ₋₁ the event of no earlier failure. Failures need not be observable, so Gⱼ₋₁ is an additional mathematical condition, not necessarily a field in the history. Assume that for **every history with positive probability together with Gⱼ₋₁**, the conditional chance of failure at call j is at most δⱼ. Define Eⱼ=Gⱼ₋₁∩Fⱼ as the event that j is the first failure. Summing over histories gives

$$
\begin{aligned}
\Pr(E_j)
 &=\sum_h
 \Pr(G_{j-1},H_{j-1}=h)
\Pr(F_j\mid G_{j-1},H_{j-1}=h)\\
 &\le\delta_j\Pr(G_{j-1})\le\delta_j.
\end{aligned}
$$

The Eⱼ are disjoint and their union is the event of any failure, so their probabilities sum and give the same budget. Zero-probability histories contribute zero and require no conditional distribution. For a bounded adaptive algorithm with at most K calls, pad unused positions with zero-cost, zero-failure stages and apply this proof. A guarantee only on one convenient input, or only averaged over a different history distribution, does not meet the premise. A cap is necessary for a deterministic worst-case ledger; an unbounded repeat-until-success process needs a separately stated tail or expected-cost analysis.

```python
bad=r.adaptive_first_failure((F(1,10),F(1),F(1,5)))
assert bad==F(7,25) and r.failure_total((F(1,10),F(1,5)))==F(3,10)
per_call=F(1,20)/160
assert r.failure_total((per_call,)*160)==F(1,20)
assert r.failure_total((F(1,20),F(1,20)))==F(1,10)
print('Adaptive first-failure probability 7/25 is bounded by 3/10; 160 per-call allowances of 1/3200 sum to 1/20.')
```

```text
Adaptive first-failure probability 7/25 is bounded by 3/10; 160 per-call allowances of 1/3200 sum to 1/20.
```

For 160 calls and an implementation-failure allocation 1/20, a uniform allowance 1/3200 per call suffices. Combining that allocation with statistical failure at most 1/20 gives total failure at most 1/10, assuming the statistical bound holds uniformly when implementation has not failed. This is different from summing deterministic probability biases: biases consume an accuracy or success-gap budget as in 14.5, while probabilities δⱼ bound bad events. The helper checks exact arithmetic, not the truth of a device's supplied δⱼ.

### 14.6.7 Count classical input, records and the reported answer

Fix a parameter payload of b bits per angle, excluding common metadata. Reading all n parameters costs nb payload bits. In this Python example b=64 describes the binary64 values handed to the runtime; it is a storage convention, not a claim of 64 accurate physical control bits. A smaller fixed-point encoding needs an explicit quantization and probability-bias analysis from 14.5. Parsing, circuit construction and parameter transfer do not disappear because they run on the host.

For a concrete instruction-payload encoding, use one opcode bit to distinguish RY from CX and a=max(1,⌈log₂(n+1)⌉) bits for each qubit label. The n RY records contain one label and b angle bits each; the n CX records contain two labels each. Counting these fields gives

$$
B_{\rm circuit}=2n+3na+nb.
$$

This excludes common width/count/framing metadata and is a specified compact format, not a claim about the runtime's JSON or Python object layout. For n=3 and b=64 it is 216 bits. The simple builder emits 2n instruction records once, so its append count is linear in n in a unit-cost host model; bit-cost construction must additionally account for writing these descriptor fields. The initial classical angle payload and the stored circuit description are two representations of related data, not two unrelated input requirements. If both are retained, both allocations matter.

If k selected qubits are recorded on each of R trials, the raw logical record payload is Rk bits. Changing the request from the parity output alone to all n+1 qubits multiplies that payload by n+1. These records permit the stronger check z=⊕x on every sampled row, but the additional output is a diagnostic choice, not required by the estimation task.

The count C=∑zᵣ lies in {0,…,R} and fits in ⌈log₂(R+1)⌉ bits. The implementation uses `R.bit_length()`, which equals that ceiling for every positive integer R: if 2ᵃ≤R<2ᵃ⁺¹, then a<log₂(R+1)≤a+1. The rational report C/R can be encoded as two unsigned integers of that width, using at most twice as many payload bits; common framing or printing digits is additional. A streaming counter reads R bits and uses R additions on O(log(R+1))-bit integers. Each binary addition scans at most that many bit positions, giving an O(R log(R+1)) bit-operation upper bound and O(log(R+1)) counter space. Retaining the raw record tensor instead uses its full output storage. These are different postprocessing choices, not incompatible estimates.

```python
_,full,info=r.simulate((.2,.4,.6),80,full=True)
assert full['input_bits']==192 and full['record_payload_bits']==320
assert serial['record_payload_bits']==80 and full['counter_bits']==7
descriptor_bits=2*3+3*3*2+3*64
assert descriptor_bits==216 and 2*3==6
assert full['exact_report_bits']==14 and info['record_tensor_bytes']>=40
print('Input payload 192 bits; selected output 80 bits versus full records 320 bits; count storage 7 bits and numerator/denominator report at most 14 bits.')
print('Native tensor byte storage is measured separately from packed logical payload.')
print('Declared compact circuit payload 216 bits; builder emits six instructions once, while streaming postprocessing uses 80 additions.')
```

```text
Input payload 192 bits; selected output 80 bits versus full records 320 bits; count storage 7 bits and numerator/denominator report at most 14 bits.
Native tensor byte storage is measured separately from packed logical payload.
Declared compact circuit payload 216 bits; builder emits six instructions once, while streaming postprocessing uses 80 additions.
```

The code measures tensor storage with `numel()*element_size()` and reports it separately: a tensor normally does not pack one bit per logical binary outcome. Object headers, allocator overhead and copies are additional. Likewise reading a claimed L-bit input or emitting an L-bit output takes at least L bit transfers in the declared serial bit-I/O model. This elementary boundary can dominate a cheap kernel; it is not a theorem about an unspecified parallel interface. A function returning an entire statevector and a task returning one probability estimate have different output contracts.

### 14.6.8 Keep logical, simulator and physical ledgers separate

A dense statevector on W qubits has 2ᵂ complex entries; a dense density matrix has 4ᵂ. One complex128 entry has 16 bytes. Multiplying dimensions by this element size gives payload storage of one such tensor, not peak process memory. Temporaries, measurement results, autograd state and other tensors may coexist. The companion requests dense reference outputs only for small validation cases; they are not charged as operational answers to the parity-estimation task.

```python
storage=r.simulator_storage(4)
assert storage=={'statevector_bytes':256,'density_bytes':4096}
_,empty,_=r.simulate((),7)
assert empty['total'].gates==0 and empty['peak_qubits']==1 and empty['record_payload_bits']==7
assert r.invalid_checks()==14
print('One four-qubit complex128 vector payload is 256 bytes; one dense density payload is 4096 bytes, excluding temporaries.')
print('Empty parity: zero gates still needs one output qubit and seven requested records; 14 malformed contracts rejected.')
```

```text
One four-qubit complex128 vector payload is 256 bytes; one dense density payload is 4096 bytes, excluding temporaries.
Empty parity: zero gates still needs one output qubit and seven requested records; 14 malformed contracts rejected.
```

A complete report must identify setup/loading and updates, gate alphabet and precision, preparation, workspace lifetime and cleanup, queries and their implementations, measurements/records, repetition and concurrency, classical postprocessing, the final answer representation and the accuracy/failure contract. If durations τⱼ in one common unit are supplied, a fully serial time model may sum them. A weighted total is meaningless until its weights and unit are given; adding “six gates plus four qubits plus eighty bits” does not produce time. With overlapping activities use a schedule and dependencies instead of summing all times or assuming perfect overlap. No physical durations, connectivity, calibration or energy data are supplied here, so the ledger leaves those fields unspecified rather than estimating them from CPU runtime.

**Implementation support and verification.** The released FlagQuantum 0.3.1 API actually used here supplies `Circuit.RY`, `CX`, `to_ir()`, `analysis()`, `run`, exact probabilities/densities and terminal samples in both statevector and density-matrix modes. Its structural analysis provides instruction counts, named-gate counts and a support-based depth; the chapter independently checks those fields against the declared gate graph. Neither this API use nor our host helper establishes a complete hardware cost estimator, routing/synthesis optimum, calibrated failure probability, physical reset protocol or measured parallel speedup. Field names in inspected IR may use a different legacy naming convention; the textbook consistently calls the physical/logical systems qubits.

The complete program is [resource_accounting.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/resource_accounting.py). Its 52 actual CPU complex128 executions cover empty input, basis endpoints and nontrivial angle lists through n=4, both modes and selected/full terminal records. Deterministic references use atol=10⁻¹² and rtol=0. Raw samples are checked for valid shape, bits, count accounting and exact parity relations when available; a random estimate is not required to hit its confidence interval. Host cost guards and exact adaptive error trees are separate from quantum executions. The n≤4 native bound is a dense teaching/reference guard, not a FlagQuantum qubit limit. The host planner limits n to 100 and R to 10,000, requires 1≤P≤R, and the tensor-size arithmetic helper limits W to 20; these are explicit local guards, not asymptotic theorems or framework capacity limits. No phase alignment, probability clipping, input normalization repair or interval error certificate is used.

Expected output of the complete program:

```text
52 native CPU complex128 circuits: 13 angle cases, two modes and selected/full terminal records passed.
Native IR gate counts/depth match independent support scheduling; full vectors/densities, scalar parity probabilities and raw-record relations checked.
At n=3 and 80 preparations: 480 logical gates, serial depth 320, peak 4 qubits, 80 selected record bits; four-way schedule depth 80 and peak 16.
Three adaptive error-tree cases and exact additive/query/repetition/host-payload ledgers passed; diagnostic tensors are separate from task output.
14 malformed contracts rejected before execution; no hardware timing, calibrated errors or automatic end-to-end estimator claimed.
```

**Check your understanding.** Which ledger changes if the identical logical circuit returns all qubit records rather than only the parity bit? Does one batched simulator invocation mean the task requires only one preparation? Why can two depth-one stages have combined depth one?

**Problems and transfer.**

- **14.6-A — compose contracts.** A setup reads 96 bits. A trial uses 10 gates, initializes five qubits and returns two measured bits. For 31 sequential trials, give total work and peak width when reuse is valid. What changes with three allocated copies? Explain why a retained output register must be included in the peak-space argument.
- **14.6-B — propagate failures.** A two-stage process has first-stage failure 1/10. Given a good first stage, the second fails with probability at most 1/5; given a bad first stage it may fail with probability one. Derive the exact “any failure” probability for those values and the union budget. Then give a per-call allocation for 12 calls and total failure at most 3/100. State the conditional premise needed for adaptive inputs.
- **14.6-C — fresh execution.** Use angles (−.3,.9), (.13,−.7,1.2) and (.4,.2,−.8,.6), each with 31 samples, both modes and selected/full records. Check scalar probabilities and full amplitudes/densities, payloads and parity relations. Independently enumerate dependency paths for the six-gate n=3 circuit and compare its longest path with the recurrence/native depth.
- **14.6-D — audit an incomplete claim.** A claim reports Q=3 queries, G₀=2 other gates and 50 trials. The supplied implementation costs 7 gates/query; setup reads 120 bits. Compute the gate/query ledger. If one call emits all amplitudes of a 20-qubit state in complex128, what output tensor payload is requested? Explain why neither number is a hardware duration and why an expected number of trials cannot silently replace a hard cap.

<details markdown="1">
<summary>Answers and verification guidance for 14.6-A–D</summary>

**A.** Work totals are 310 gates, 155 individual initializations, 62 measured bits, 96 input payload bits and 62 record payload bits. Reusing a five-qubit allocation gives peak five, not 155. Three allocated copies give peak 15 and ⌈31/3⌉=11 batches; total work is unchanged. A persistent output remains live across calls, so include it as persistent space plus the active temporary allocation. A reuse or zero-initialization precondition must be justified.

**B.** The first-failure events have probabilities 1/10 and (9/10)(1/5), yielding 7/25, bounded by 1/10+1/5=3/10. Later behavior after an earlier failure is irrelevant to “any failure.” Uniform allowances of (3/100)/12=1/400 sum to 3/100. Each call's bound must hold on every reachable no-earlier-failure history, rather than on a single test input.

**C.** These are 12 new native executions, not twelve confidence certificates. Widths are 3,4,5; per-trial gates are 4,6,8 and depth 3,4,5. Selected payload is 31 bits in each case; full payloads are 93,124,155 bits. The n=3 dependency path RY(0)→CX(0,3)→CX(1,3)→CX(2,3) has four gates; no path is longer. The transfer reference enumerates all increasing intersecting-support paths rather than calling the scheduling helper.

**D.** There are 150 queries and 50(2+3·7)=1150 logical gates, with 120 setup bits. One requested vector payload is 16·2²⁰=16,777,216 bytes, excluding all additional storage. The final output contract must say whether it requests that vector or a small estimate. No gate durations or interface bandwidths are given. A process with finite expected work may still have arbitrarily long executions, whereas a hard resource bound must cover every allowed execution or explicitly budget an abort tail.

</details>

**Source and review status.** The frozen locator is Nielsen and Chuang, [§3.2.1, beginning on printed page 136](https://assets.cambridge.org/97811070/02173/toc/9781107002173_toc.pdf); the publisher's contents was checked, not treated as access to the full chapter. As a directly inspected primary model reference, Watrous, [*Quantum Computational Complexity*, §III.1–III.2, PDF pages 7–8](https://cs.uwaterloo.ca/~watrous/Papers/QuantumComputationalComplexity.pdf#page=7), defines a circuit-size convention and explains why a gate-cost model must constrain its allowed gates. Its combined size convention differs from our separate gate/width ledger; conventions must be declared rather than interchanged. All central additive, scheduling and error-composition proofs needed here are supplied locally. The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/14.6.json) distinguishes author verification from independent mathematical/implementation review and reader trial. This remains a working draft. Continue, when drafted, with [14.7 Quantum-classical interaction patterns](../section-plans/03-algorithms.md#sec-hybrid-interaction-map).

<!-- end-section-14.6 -->

<span id="sec-hybrid-interaction-map"></span>
## 14.7 Quantum-classical interaction patterns

**Question.** What exactly passes between classical computation and a quantum experiment, and which decisions must occur while a quantum state remains available?

The prerequisites are [5.1, composition and call order](ch-gates-reversible-computation-and-circuit-synthesis.md#sec-gates-reversible-computation-and-circuit-synthesis-1), [6.2, conditional states and ignored outcomes](ch-measurement-expectation-values-and-statistical-estimation.md#sec-measurement-expectation-values-and-statistical-estimation-2), and [14.1, input and execution contracts](#sec-computational-models-complexity-and-quantum-advantage-1). This **P-depth** section introduces a typed interaction model and the eight patterns of the [editorial hybrid map](../hybrid-computing.md). They are composable teaching categories, not an exhaustive, mutually exclusive or standardized taxonomy. Patterns 1–7 describe algorithm/data coupling; pattern 8 describes execution architecture that may support any of them. Later chapters supply the full learning, cutting, embedding and controller theories. The small identities below make the boundaries executable without claiming those general algorithms have already been implemented.

A **host** prepares task descriptions, manages application data and processes returned results. A **controller** makes supported execution-time decisions close to the quantum operations. A **quantum executor** performs a specified preparation, evolution and measurement. These are roles, not necessarily three separate physical machines. In this section the host and executor both run on a CPU, and the executor is an ideal FlagQuantum simulator. No GPU or physical QPU is used.

| Boundary | Exchanged object | State-lifetime obligation |
| --- | --- | --- |
| Host to a new experiment | Circuit, numerical parameters, basis, shot count and task/revision identifiers | Declare a fresh preparation |
| Terminal experiment to host | Bits, counts or an explicitly labeled estimate | No retained measured-branch handle is supplied by this example |
| Measurement to a local controller within one execution | Outcome or decoder/frame data, then a control decision | Preserve the remaining state and meet a supported timing contract |
| Between application tasks | Typed results, dependencies and checkpoints | Do not infer coherent state sharing from job dependencies |

The complete task needs a data schema **and** a control/state-lifetime schema. A real array of amplitudes is a classical simulator object; it is not a list of measured amplitudes or permission to clone an unknown state. An exact simulator expectation, a finite-shot statistic and a bit record are distinct data types even if all are stored as ordinary numbers.

### 14.7.1 Pattern 1: a subroutine in a classical pipeline

Here is the typed data flow of our terminal-sampling path. The return arrow contains classical bits, not a quantum-state continuation:

```text
HOST: Task(id, revision, theta, phi, basis, S)
  | control: circuit + radian parameters + S
  v
CPU SIMULATOR: fresh |0>, gates, terminal sampling
  | data: bits[1,S,1], declared basis and task identity
  v
HOST: validate -> statistic -> answer / next Task
  | next call starts a new preparation
```

Let S be the positive integer shot count. Our task prepares the single-qubit state

$$
|\psi(\theta,\phi)\rangle
=\cos(\theta/2)|0\rangle
+e^{i\phi}\sin(\theta/2)|1\rangle
$$

using RY(θ) then P(φ), with all angles in radians. For a Z-basis result b∈{0,1}, assign score s(b)=1−2b. The two Born probabilities give

$$
p_Z(1)=\sin^2(\theta/2),\qquad
\mu_Z=\mathbb E[s(b)]=\cos\theta,\qquad
\widehat\mu_Z=\frac1S\sum_{r=1}^{S}(1-2b_r).
$$

This finite mean is a host calculation on bits. Its expectation equals \(\mu_Z\) when each record has the declared marginal distribution, by distributing the finite sum; an independence assumption is needed for many uncertainty bounds, not for that equality alone. The task contract includes input parameters, the selected basis, S, a task identifier and a revision. The local packet validator rejects a result for another revision or another measurement setting before forming the mean. This validates a schema, not authenticity of a remote device.

```python
from dataclasses import replace
from fractions import Fraction as F
import math,torch,flagquantum as fq
from examples.foundations import interaction_patterns as h,statistical_ensembles as e
task=h.Task('pipeline',0,.7,.2,shots=19)
c=fq.Circuit(1,dtype=torch.complex128).RY(0,theta=task.theta).P(0,theta=task.phi)
out=fq.run(c,outputs=[fq.probabilities(name='p'),fq.samples(qubits=(0,),name='raw')],shots=task.shots,options=e.OPTIONS)
e.close(out.measurement('p').value[0],torch.tensor([(1+math.cos(.7))/2,(1-math.cos(.7))/2],dtype=torch.float64))
raw=out.measurement('raw').value;assert raw.shape==(1,19,1)
packet=h.Packet(task,tuple(int(b)for b in raw[0,:,0]))
mean=h.sample_mean(packet,task);assert -1<=mean<=1
print('Pipeline: 19 terminal bits become a validated rational Z-score mean; exact probabilities remain simulator diagnostics.')
```

```text
Pipeline: 19 terminal bits become a validated rational Z-score mean; exact probabilities remain simulator diagnostics.
```

The exact probabilities in that snippet validate an ideal reference. The returned `Packet` contains terminal bits with a CPU-simulator source label. The numerical expectation or full statevector is not silently inserted into the bit-estimator input. Hardware would require its own execution, measurement and statistical contract; replacing an exact diagnostic by a sampled estimate changes the evidence and often the required budget.

### 14.7.2 Pattern 2: a variational outer loop

An outer loop sends parameters to experiments, combines their observations into a classical objective, and constructs the next parameter task. It need not retain the previous quantum state. For a bounded introductory example, take the objective

$$
L(\theta)=(\mu_Z(\theta)-t)^2=(\cos\theta-t)^2,
$$

where t is a fixed dimensionless target. With t=0 and the finite candidate list {0,π/2,π}, the exact objective values are 1,0,1. A host can instead compute the plug-in values (\(\widehat{\mu}_Z\)−t)² from the actual bit records and select the lowest **observed** candidate. Squaring a noisy mean does not in general produce an unbiased objective estimate: at θ=π/2, t=0 and S=1, the score is ±1, so the plug-in squared loss is always 1 although the true loss is 0. Selecting an observed minimum also does not prove that the true objective decreased.

```python
rows,chosen=h.outer((0.,math.pi/2,math.pi),target=0.)
assert all(rows[chosen]['sampled_loss']<=row['sampled_loss']for row in rows)
assert abs(rows[1]['diagnostic_loss'])<1e-12
assert abs(rows[0]['diagnostic_loss']-1)<1e-12 and abs(rows[2]['diagnostic_loss']-1)<1e-12
print('Finite outer loop: three fresh preparations, sample-based candidate selection, separately checked analytic landscape; no convergence theorem inferred.')
```

```text
Finite outer loop: three fresh preparations, sample-based candidate selection, separately checked analytic landscape; no convergence theorem inferred.
```

This executable performs one finite candidate-selection update, not a general optimizer. The candidate list is classical control data; the three preparations are distinct quantum experiments. Its exact landscape is a separately labeled simulator check. General VQE needs an explicit observable decomposition, estimator/derivative strategy, optimizer state, stopping rule and total experiment budget; those are developed in Chapters 23–26. Differentiating a simulated statevector is not a hardware measurement protocol, and this example does not invoke autograd or certify optimizer convergence.

### 14.7.3 Pattern 3: hybrid learning, fixed features and kernels

A quantum-derived feature can feed a classical prediction rule. In the one-feature example f(x)=\(\mu_Z\)(x), a classical affine head computes y=a f+b. A record-based feature \(\widehat{\mu}_Z\) gives a correspondingly record-based prediction. Shape and source type must be preserved across that boundary; naming a value a “quantum layer” does not provide gradients for a training scheme.

A fixed kernel is a different interface: two data inputs x,x′ request one similarity estimate. Restrict φ=0 and define |φ(x)⟩=RY(x)|0⟩. Expanding the two real coordinates and using the angle-subtraction identity gives

$$
\begin{aligned}
\langle\varphi(x')|\varphi(x)\rangle
 &=\cos\!\left(\frac{x-x'}2\right),\\
K(x,x')
 &=\left|\langle\varphi(x')|\varphi(x)\rangle\right|^2
 =\cos^2\!\left(\frac{x-x'}2\right).
\end{aligned}
$$

The probability of zero after RY(x) followed by RY(−x′) is K: 5.1's call/matrix convention makes the net operation RY(−x′)RY(x). The input pair and resulting scalar can then be consumed by a classical predictor. The quantum experiment need not be rerun for every step of a classical fit when those fixed features/kernel entries have already been collected.

```python
x,y=.2,.8
kblock=fq.Circuit(1,dtype=torch.complex128).RY(0,theta=x).RY(0,theta=-y)
kresult=fq.run(kblock,outputs=[fq.probabilities(name='kernel')],options=e.OPTIONS)
exact=math.cos((x-y)/2)**2
e.close(kresult.measurement('kernel').value[0],torch.tensor([exact,1-exact],dtype=torch.float64))
_,checked_kernel=h.kernel(x,y,mode='density_matrix');assert abs(checked_kernel-exact)<1e-12
feature=torch.tensor([float(mean)],dtype=torch.float64)
head=2*feature-.3;assert feature.shape==head.shape==(1,)
print('Fixed feature shape (1,) and classical affine head checked; RY(x),RY(-y) kernel equals cos^2((x-y)/2) in both modes.')
```

```text
Fixed feature shape (1,) and classical affine head checked; RY(x),RY(-y) kernel equals cos^2((x-y)/2) in both modes.
```

This checks a fixed feature and a fixed kernel, not training quality, held-out generalization or a learning advantage. A trainable circuit or trainable kernel adds an explicit parameter-update and derivative contract. A simulator derivative, a parameter-shift experiment and a finite-difference experiment have different sources, calls and statistical costs; they cannot be substituted merely because their output arrays share a shape. Chapter 27 develops these distinctions beyond this one-dimensional interface.

### 14.7.4 Pattern 4: in-execution adaptive feedback

For an execution-time feedback task, some quantum systems must remain live during a classical decision. A schematic local-control path is

```text
live joint state -> measure one part -> classical bit r
       |                                  |
       | retained unmeasured subsystem    | control V_r
       +----------------------------------v
                              continue same execution
```

The present terminal-only program does **not** execute that arrow. To make its required semantics concrete, prepare a control qubit and a target at zero, then apply CX. Write c=cos(θ/2) and d=\(e^{i\phi}\sin(\theta/2)\). The joint vector is c|00⟩+d|11⟩. If the control is ideally measured in Z, the unnormalized target branches, probabilities and normalized states are

$$
\begin{array}{c|c|c|c}
r&\eta_r&p_r&\eta_r/\sqrt{p_r}\ (p_r>0)\\\hline
0&c|0\rangle&|c|^2&(c/|c|)|0\rangle\\
1&d|1\rangle&|d|^2&(d/|d|)|1\rangle
\end{array}
$$

The correction Xʳ sends each nonzero target branch to the zero-state ray, retaining its branch coefficient's phase. A zero-probability branch has no normalized conditional state. If the record is ignored after that correction, the control/target ensemble contains |00⟩ and |10⟩ with weights |c|² and |d|²; it has no coherence between those alternatives. By contrast applying a second **coherent** CX, without measuring, gives (c|0⟩+d|1⟩)|0⟩. The target is zero in both constructions, but the full joint states differ when cd≠0. Thus a coherent conditional gate is not by itself evidence of a classical feedback execution.

```python
branches,ignored,coherent=h.feedback(math.pi/2,.4)
assert all(abs(p-.5)<1e-12 for p,_ in branches)
e.close(ignored,torch.diag(torch.tensor([.5,0,.5,0],dtype=torch.complex128)))
assert abs(coherent[1].measurement('rho').value[0,0,2].abs().item()-.5)<1e-12
try:h.require_retained_state('tested-terminal-path-with-no-state-handle')
except ValueError:pass
else:raise AssertionError('Terminal result was incorrectly treated as a retained branch handle')
print('Two ideal branches correct the target to zero; their ignored joint ensemble differs from the coherent-CX reference.')
print('Native execution here is terminal-only; conditional branches are explicit mathematical postprocessing, not a dynamic feedback endpoint.')
```

```text
Two ideal branches correct the target to zero; their ignored joint ensemble differs from the coherent-CX reference.
Native execution here is terminal-only; conditional branches are explicit mathematical postprocessing, not a dynamic feedback endpoint.
```

The two actual native calls prepare the pre-measurement and coherent-reference states. The conditional branches/corrected ignored ensemble are explicit mathematical postprocessing of the reference vector, as in 6.2; they are not native collapsed states kept alive for a subsequent Python callback. Our tested `Circuit`/terminal-request path does not supply such a measured-branch continuation contract, so the helper refuses that request. Source inspection and terminal sampling do not establish a framework-wide impossibility: a different dynamic-program/controller backend would need its own API and execution audit. No reset, hardware feedforward latency or retained-state handle is claimed here. Positive probabilities that underflow in the host branch arithmetic are rejected rather than treated as impossible outcomes. For a representable positive branch, the code computes its normalized phase as amp/abs(amp), mathematically equivalent to amp/√p but avoiding extra rounding from squaring and taking a square root. A pure-classical regression retains a positive subnormal squared magnitude at amp=10⁻¹⁶⁰; the older square-root path missed unit norm by more than 10⁻¹² and is preserved in the evidence. This repair is in the book reference, not a native API failure.

### 14.7.5 Pattern 5: measurement-driven inference

Inference uses a measurement design and classical estimator to learn a property or model. The design limits what can be identified. On the same preparation, X readout applies H before the terminal Z measurement; Y readout applies S† then H, where S†=diag(1,−i). Multiplying these matrices into the two coordinates above yields

$$
\mu_X=\sin\theta\cos\phi,\qquad
\mu_Y=\sin\theta\sin\phi,\qquad
\mu_Z=\cos\theta.
$$

For example, subtracting the two squared H-output magnitudes gives 2 Re(c* d)=sinθ cosφ. With S† first the corresponding difference is 2 Im(c* d)=sinθ sinφ, fixing the Y sign. These are setting-specific score means, not three simultaneous outcomes from one qubit preparation. Each setting needs its own preparations in this implementation.

At θ=π/2, φ=0 and φ=π give the plus and minus states. Their Z distributions are both (1/2,1/2), so no amount of Z-only data can distinguish them by this distribution. X readout instead gives means +1 and −1. The unavailable information cannot be recovered merely by applying a more elaborate classical function to the same Z records.

```python
observed={}
for sign,phi in (('plus',0.),('minus',math.pi)):
 for basis in ('Z','X'):
  t=h.Task(sign+basis,0,math.pi/2,phi,basis)
  p,d=h.run_task(t);observed[sign+basis]=d['native_mu']
  assert -1<=h.sample_mean(p,t)<=1
assert abs(observed['plusZ']-observed['minusZ'])<1e-12
assert abs(observed['plusX']-1)<1e-12 and abs(observed['minusX']+1)<1e-12
print('Z-only records cannot identify plus versus minus; the X setting distinguishes their opposite means. Four preparation/settings checked.')
```

```text
Z-only records cannot identify plus versus minus; the X setting distinguishes their opposite means. Four preparation/settings checked.
```

This is a measurement-identifiability example, not a general tomography, mitigation or classical-shadow implementation. The full vectors/native expectations used by the author are separate diagnostics. A physical inference workflow would specify the observation model, settings, shot budget, uncertainty and any fitted constraints or regularization. Exact simulator access must not be added as an undeclared inference measurement.

### 14.7.6 Pattern 6: decomposition with classical reconstruction

A decomposition method executes fragments/settings and classically combines their outputs. A declared identity is essential; “split a circuit” alone is not a reconstruction rule. For a bounded scalar example, compose RY(a) and RY(b) on |0⟩. Define \(z_a\)=cos a, \(x_a\)=sin a and similarly for b. Direct rotation multiplication or the cosine addition identity gives the exact Z mean

$$
y=\cos(a+b)=\(z_a\) z_b-\(x_a\) x_b.
$$

Four separate single-qubit means provide the right-hand side; a fifth, uncut RY(a)-then-RY(b) experiment checks the left-hand side. The reconstruction is a scalar with a signed term, not the preparation of a larger coherent state from classical numbers. All circuits here already use one qubit; no width advantage is claimed. This example supplies one temporal-composition identity, not a general circuit-cutting compiler or the full methods of Chapter 47.

If every estimated component is in [−1,1] and within η of its exact value, a two-factor telescoping expansion gives |â b̂−ab|≤|â||b̂−b|+|b||â−a|≤2η. Applying this to the two products and adding gives |ŷ−y|≤4η. This deterministic error implication needs component error bounds; it does not infer them from a favorable sampled reconstruction.

```python
reconstructed,sampled=h.reconstruct(.4,.7)
assert abs(reconstructed-math.cos(1.1))<1e-12 and -2<=sampled<=2
eta=F(1,100);bound=4*eta;assert bound==F(1,25)
print('Four fragment means reconstruct the fifth, uncut reference: cos(a)cos(b)-sin(a)sin(b)=cos(a+b).')
print('Products/signs are classical; four uniform component errors of at most 1/100 give output error at most 1/25, without clipping.')
```

```text
Four fragment means reconstruct the fifth, uncut reference: cos(a)cos(b)-sin(a)sin(b)=cos(a+b).
Products/signs are classical; four uniform component errors of at most 1/100 give output error at most 1/25, without clipping.
```

The plug-in sampled reconstruction can lie outside [−1,1] even though the true observable mean cannot; it is not silently clipped. Products of random estimates need independence or a covariance analysis for unbiasedness/uncertainty claims. The common-seed diagnostic examples here do not establish such statistical guarantees. The tested claims are the exact reconstruction identity, packet accounting and the conditional 4η error bound. Signed weights, settings, correlations and the total sampling overhead become part of a full decomposition contract.

### 14.7.7 Pattern 7: embedded and self-consistent solvers

In a self-consistent workflow, a classical environment parameter changes a quantum subproblem, whose measured property changes the environment again. The inner solver may itself use pattern 2, so inner optimization and outer consistency are different loops. A small solvable illustration avoids pretending that a full embedding method has already been derived.

Take a dimensionless environment variable v∈[−1,1] and fixed 0≤g<1. Define the two-level subproblem

$$
H(v)=-Z-gvX
=\begin{pmatrix}-1&-gv\\-gv&1\end{pmatrix},
\qquad v_{k+1}=\langle X\rangle_{v_k}.
$$

Its characteristic equation is λ²−[1+(gv)²]=0. Set θ(v)=arctan(gv). The normalized RY(θ(v))|0⟩ vector satisfies \(H(v)|\psi_v\rangle=-\sqrt{1+(gv)^2}|\psi_v\rangle\) by multiplying the two rows, so it is the lower-eigenvalue state. Thus the exact inner solution gives the explicit outer map

$$
v_{k+1}=F(v_k)
=\frac{gv_k}{\sqrt{1+(gv_k)^2}}.
$$

A record-based update instead uses \(\widehat{\mu}_X\) from a fresh preparation. An exact native expectation update is useful for an ideal simulator reference, but must be labeled as such. The code records the old environment, the angle, the chosen source, new environment and observed step residual \(|v_{k+1}-v_k|\) for each iteration.

```python
sampled_trace=h.embedding(.5,.8,steps=2,source='samples')
exact_trace=h.embedding(.5,.8,steps=2,source='exact-simulator',mode='density_matrix')
v=.8
for row in exact_trace:
 expected=.5*v/math.sqrt(1+(.5*v)**2)
 assert abs(row['new_v']-expected)<1e-12;v=expected
assert all(row['source']=='samples'for row in sampled_trace)
assert all(row['source']=='exact-simulator'for row in exact_trace)
print('Two-step toy environment update checked for sampled and exact-simulator paths; analytic inner preparation is explicit, not a general embedded solver.')
```

```text
Two-step toy environment update checked for sampled and exact-simulator paths; analytic inner preparation is explicit, not a general embedded solver.
```

The inner preparation is analytic book code, not a native ground-state solver. This is not DMET, a many-body embedding construction or a global physical accuracy certificate. We verify the stated 2×2 eigenvector and a finite update trace; we do not infer a general convergence theorem from two decreasing residuals. A small observed residual can coexist with model error, solver bias or sampling error. Real embedded applications need a declared effective model, environment update, nested stopping/error budgets and independent global references; Chapter 25 supplies those method-specific ingredients.

### 14.7.8 Pattern 8: heterogeneous workflow architecture

The application can represent the previous experiments and classical calculations as a task graph. An edge specifies which typed result an operation requires; an independent job may finish in another order, but a consumer cannot use a result from the wrong parameter revision. CPU orchestration, GPU numerical computation and QPU experiments are possible resource roles in such an architecture, not mandatory ingredients or interchangeable execution labels.

In this CPU-only executable, the host accepts one packet per task/revision and checks parameters, basis, shot count and source label. Revisions distinguish changed requests; independent replicate tasks need distinct identifiers rather than reusing the same packet as extra observations. A retry policy must charge all attempted executions and decide which result is accepted. A label is not device authentication, and these schema checks cannot establish that a remote producer actually ran the claimed hardware.

```python
accepted=set();h.accept_once(packet,task,accepted)
for bad_task in (replace(task,revision=1),replace(task,basis='X')):
 try:h.checked(packet,bad_task)
 except ValueError:pass
 else:raise AssertionError('Stale/mismatched result accepted')
try:h.accept_once(packet,task,accepted)
except ValueError:pass
else:raise AssertionError('Duplicate result counted twice')
assert h.invalid_checks()==18 and len(h.PATTERNS)==8
assert h.RUNS==19
print('Task/revision/basis/shot schema checked; duplicate and stale results rejected; 18 malformed contracts rejected before further execution.')
print('Body: 19 companion-native calls plus two explicit fq.run calls; only CPU simulation executed, with no GPU/QPU or hardware timing claim.')
```

```text
Task/revision/basis/shot schema checked; duplicate and stale results rejected; 18 malformed contracts rejected before further execution.
Body: 19 companion-native calls plus two explicit fq.run calls; only CPU simulation executed, with no GPU/QPU or hardware timing claim.
```

The complete program validates 36 actual packets in reverse arrival order after their serialized CPU executions. This exercises result matching, not an asynchronous runtime, a GPU job scheduler or coherent quantum networking. A terminal callback on the host does not gain a local-controller state-lifetime guarantee by being placed in a task graph.

For disjoint **sequential** timing intervals, one host-driven task can be modeled as

$$
\begin{aligned}
T_{\rm task}&=T_{\rm setup}+T_{\rm final}\\
&\quad+\sum_{k=1}^{K}
\bigl(T_{\rm host,k}+T_{\rm queue,k}\\
&\hspace{6em}+T_{\rm transfer,k}+T_{\rm exec,k}\bigr).
\end{aligned}
$$

Each term needs a common time unit and a non-overlapping boundary; execution time includes the stipulated local control/readout rather than counting it twice. Overlap requires dependency/schedule analysis, not adding overlapping durations or assuming all work overlaps. The resource distinctions in 14.6 apply: settings, repetitions, compilation, I/O, classical updates, state lifetimes and failure recovery remain visible. No physical timing values or speedup claim are supplied by this CPU run.

**Implementation support and limits.** We inspected and actually used released FlagQuantum 0.3.1 `Circuit.RY/P/H/SDG/CX`, `run`, terminal `samples`, exact `probabilities`, `density_matrix` and `expectation(fq.Z(0))`. Both statevector and density-matrix modes were executed on CPU complex128 with Python 3.12.14 and Torch 2.13.0. Basis rotations turn the native post-analyzer Z expectation into the requested setting's score mean. Packet validation, candidate selection, classical head, kernel interpretation, branch analysis, fragment reconstruction, environment update and result matching are book-side computations. This path does not certify general dynamic feedforward, retained collapsed-state continuation, hardware reset/calibration, gradient training, automatic cutting/embedding, GPU/QPU execution or a complete workflow runtime.

The full program is [interaction_patterns.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/interaction_patterns.py). Its 90 native calls cover both modes, three angles, two complex phases and all X/Y/Z settings; finite candidate scans, pair kernels, zero-probability branch boundaries and coherent references; signed-angle reconstructions and sampled/exact-labeled environment traces. The 21 body calls include two explicit `fq.run` calls. Deterministic scalar/full-state/density/expectation checks use atol=10⁻¹², rtol=0, without phase alignment, clipping or input repair. Samples are checked through their schemas and score ranges, not required to meet a confidence interval or improve a noisy objective. Source/parameter checks reject nonfinite inputs, positive branch underflow, stale/duplicate/diagnostic records, unsupported lifetime requests and malformed settings before additional native execution. Local guards are |angle|≤10 radians, 1≤S≤1000, at most five candidates and at most four outer-environment iterations; they are not framework capacity limits.

From the repository root, run:

```bash
python examples/foundations/interaction_patterns.py
python scripts/check_interaction_patterns_prose.py
```

Expected output of the complete program:

```text
90 native CPU complex128 circuits: 36 basis/feature, 6 outer-candidate, 4 kernel, 12 feedback-reference, 20 reconstruction and 12 embedded-loop executions passed.
Both modes: full vector/density, scalar probability and native expectation references checked; samples used only through validated terminal records.
Eight editorial patterns classified; sampled/exact-simulator data, new preparations/coherent references and task revisions remain distinct.
36 out-of-order packets accepted once; 18 malformed/stale/diagnostic/unsupported-lifetime contracts rejected before further execution.
No retained measured-state handle, dynamic feedback, GPU/QPU run, general cutting/embedding solver or learning-speedup claim is made.
```

**Check your understanding.** Which of the eight patterns can occur in the same workflow? Which object crosses each arrow: a circuit, a bit record, an estimate, a parameter update or a retained quantum system? Why does an ordinary host loop not prove in-execution feedback support?

**Problems and transfer.**

- **14.7-A — typed arrows.** Describe a workflow with a fixed quantum kernel followed by classical training. Which part uses pattern 3, which part may use pattern 8, and when would pattern 2 be added? State what derivatives are required only if the kernel itself becomes trainable.
- **14.7-B — branch lifetime.** For θ=π/2 and φ=.6, write both normalized target branches, their Xʳ corrections, and the ignored joint ensemble. Compare its |00⟩⟨10| entry with the coherent-CX reference. Does serially submitting the corrected target state in a fresh job demonstrate retained-state feedback?
- **14.7-C — new execution.** Use (θ,φ)=(−.6,.4),(.37,−.8),(1.3,.9), all three bases and both modes; then test kernel inputs (−.2,.9), feedback θ=.9,φ=−.3, reconstruction a=−.5,b=.9, and a two-step exact-simulator environment trace at g=.3,v₀=−.6. Verify scalar/full-state references and packet labels. Count actual native calls separately from host packet processing.
- **14.7-D — reject invalid exchanges.** Give concrete examples of an exact diagnostic passed as a bit record, a stale basis/revision, duplicate result and unsupported retained-state request. If each of four fragment means has error at most .02, derive the stated reconstruction bound. Why is this conditional bound not a sampling confidence certificate? What costs are absent from a report containing only inner quantum gate counts?

<details markdown="1">
<summary>Answers and verification guidance for 14.7-A–D</summary>

**A.** Fixed kernel experiments supply scalar pair similarities; the classical fit can reuse them without a new quantum call at every optimizer update. A heterogeneous task graph is pattern 8 and may schedule those independent experiments. Training circuit/kernel parameters adds a parameter-update interaction and a derivative/Jacobian or declared derivative-free contract. Simulator backpropagation and hardware derivative experiments have different operational sources and budgets.

**B.** Branches have weights 1/2 and states |0⟩ and \(e^{i0.6}|1\rangle\). Xʳ gives |0⟩ and \(e^{i0.6}|0\rangle\). The ignored joint ensemble puts weight 1/2 on each of |00⟩ and |10⟩; its |00⟩⟨10| entry is zero. The coherent reference has entry \(e^{-i0.6}/2\). A fresh-job preparation of the known target is a simulation/reference or a different task, not evidence of preserving an unknown live state across a classical decision.

**C.** There are 38 fresh native executions: 18 basis-setting cases, two kernels, four pre/coherent feedback references, ten reconstruction/reference calls and four environment updates. Processing their packets again is not an additional quantum execution or independent statistical evidence. The exact environment reference follows v↦.3v/√[1+(.3v)²]; the two modes must agree with that same finite trace. CPU simulator labels must remain explicit.

**D.** The validator refuses source `statevector-diagnostic`, the wrong revision/basis, a second acceptance of one task/revision, and the tested terminal path's requested retained-branch continuation. The arithmetic implication is 4η=.08 if all four component errors are bounded by .02 and all component estimates lie in [−1,1]. It supplies no probability that those premises hold. Complete costs include preparation, basis/settings and shots, host computation/optimizer or solver iterations, transfer/queueing, compilation, records, retries, and any state-lifetime/controller requirements.

</details>

**Source and review status.** The eight patterns are the book's [original editorial specification](../hybrid-computing.md), preserved here rather than attributed to an external universal taxonomy. The frozen execution-model source is Cross et al., [*OpenQASM 3*, arXiv:2104.14722v1 §2.4, PDF page 6 and Figure 1 on PDF page 7](https://arxiv.org/pdf/2104.14722v1#page=6). Those exact pages were inspected, with the real-time/near-time distinction on PDF page 3 for context. They motivate separating program, compilation and controllers; they do not establish FlagQuantum feature support. Our local algebra and execution receipts support only the examples stated above. The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/14.7.json) keeps author checks separate from independent mathematical/implementation review and reader trial. This remains a working draft. Continue, when drafted, with [14.8 Classical baselines and advantage claims](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-7).

<!-- end-section-14.7 -->

<span id="sec-computational-models-complexity-and-quantum-advantage-7"></span>
## 14.8 Classical baselines and advantage claims

**Question.** Which classical algorithm should a quantum method be compared with, and what conclusion can a finite comparison actually support?

The prerequisites are [14.4, oracle and data-access models](#sec-computational-models-complexity-and-quantum-advantage-4) and [14.6, complete resource accounting](#sec-computational-models-complexity-and-quantum-advantage-6). This **V-depth** section supplies an executable comparison protocol, independent classical references and deliberately invalid comparison cases. It does not turn a small circuit simulation into evidence of an asymptotic separation or a physical quantum speedup. “Advantage” needs a named task, a comparison class/model and an evidence level; the word by itself supplies none of those.

Our recurring task makes a common mistake visible. The input is an explicit finite list of rational probabilities pⱼ∈[0,1]. Independently prepared bits Xⱼ have Pr(Xⱼ=1)=pⱼ, and Z=⊕ⱼXⱼ is their parity. Depending on the declared output contract, we may request its mean q=Pr(Z=1), an estimate with absolute accuracy ε and failure allowance δ, or S raw parity records. These are different tasks. Returning all amplitudes of a simulated register is a further, much larger output request, not the default classical obligation.

### 14.8.1 Match the task before comparing costs

A comparison contract records the allowed instance family or finite fixture, input representation and access, required output, accuracy/failure criterion, and resource metric. An algorithm is **eligible** if its actual guarantees meet that task. This does not require identical internal computations, identical precision or identical numbers of samples. A stronger solution is eligible if its additional work is counted.

For a requested probability mean with tolerance ε and failure at most δ, an exact classical answer has error zero and failure zero, hence meets any nonnegative looser requirement. In contrast, a method returning only unrelated samples or assuming an oracle instead of reading the specified data needs a justified adapter/model change before it can be compared.

| Item to match | What must be stated | A misleading substitution |
| --- | --- | --- |
| Task and instances | Same requested property and allowed inputs | Full classical vector versus one quantum scalar |
| Access and representation | Explicit list, samples, oracle, preparation; bitlength | Free coherent access versus charged classical loading |
| Accuracy and success | Error metric, ε, δ and any implementation bias | Exact classical output versus an unqualified noisy estimate |
| Resource boundary | Common unit; setup, repetitions, output and host work | Classical end-to-end time versus quantum kernel gates |
| Implementations | Dated code/version, configuration, hardware and baseline search scope | An obsolete/naive method labeled “the classical cost” |

```python
from dataclasses import replace
from fractions import Fraction as F
from pathlib import Path
import math,json,hashlib,torch,flagquantum as fq
from examples.foundations import classical_baselines as b,statistical_ensembles as e,accuracy_repetition as a
ps=(F(1,3),F(2,5));task=b.Contract((ps,))
exact_contract=replace(task,epsilon=F(0),delta=F(0))
assert b.fulfills(exact_contract,task)
print('Same explicit inputs and probability-mean output: an exact classical answer is eligible for a looser accuracy/failure task.')
```

```text
Same explicit inputs and probability-mean output: an exact classical answer is eligible for a looser accuracy/failure task.
```

The `fulfills` helper checks declarations and rejects mismatches. Its raw-record contract also fixes the record count and declares the exact ideal target law; approximate-law sampling would need an explicit distance metric and is not certified by this helper. It does not prove that a producer satisfies those declarations. The exact classical guarantee below comes from a finite algebraic identity; the ideal sampling budget comes from a probability argument; numerical native agreement has its separately stated tolerance. A schema check cannot replace any of them.

### 14.8.2 Derive a classical baseline that uses the task structure

Parity satisfies (−1)ᶻ=∏ⱼ(−1)ˣʲ. Independence factors its finite expectation, and E[(−1)ˣʲ]=1−2pⱼ. Since E[(−1)ᶻ]=1−2q, solving gives

$$
q=\frac{1-\prod_{j=0}^{n-1}(1-2p_j)}2.
$$

Thus computing the requested scalar does not require enumerating 2ⁿ basis strings. Enumeration is useful as a small independent reference, but making it the only classical baseline would ignore a better algorithm for this task. For n=0, the empty product is one and q=0.

The rational input also makes precision visible. Write pⱼ=aⱼ/dⱼ with integers 0≤aⱼ≤dⱼ and dⱼ>0. Let

$$
A=\prod_j(d_j-2a_j),\qquad D=\prod_jd_j,
\qquad q=\frac{D-A}{2D}.
$$

The code accumulates two integer products and then forms this rational answer. Because |dⱼ−2aⱼ|≤dⱼ, we have |A|≤D and 0≤D−A≤2D. If B is the sum of the denominators' binary bitlengths, the stored numerator/denominator need at most B+2 bits, including the empty-list boundary. For nonempty input, multiplying the denominator bounds gives D<2ᴮ; doubling and forming D−A establish the stated bit bound. This is an exact finite representation, not a unit-cost arbitrary real.

There are two integer multiplications per input entry in the unreduced-product algorithm. Schoolbook multiplication of numbers with at most B+O(1) bits uses O((B+1)²) bit operations by summing at most that many single-bit partial products. A sufficient bound for that particular algorithm is O(1+n(B+1)²), with O(B+1) accumulator storage in addition to input. Optional fraction reduction has its own arithmetic cost; Python's `Fraction` performs it, and the actual timing below includes the implementation used. This arithmetic upper bound is not a CPU-time measurement or a lower bound on all classical algorithms.

For the quantum encoding, prepare RY(2 arcsin√pⱼ)|0⟩ for each data qubit and accumulate parity into a zero output qubit with CX gates. Each data bit has the requested ideal probability pⱼ, so the same finite parity argument supplies the output law. At p=(1/3,2/5), A=1,D=15 and q=7/15:

```python
num,den=b.integer_pair(ps)
assert (num,den)==(14,30) and b.exact_mean(ps)==b.enumerate_law(ps)==F(7,15)
c=fq.Circuit(3,dtype=torch.complex128)
for j,p in enumerate(ps):c.RY(j,theta=2*math.asin(math.sqrt(float(p))))
c.CX(0,2).CX(1,2)
out=fq.run(c,outputs=[fq.probabilities(qubits=(2,),name='parity')],options=e.OPTIONS)
e.close(out.measurement('parity').value[0],torch.tensor([8/15,7/15],dtype=torch.float64))
print('Integer-product pair 14/30, exhaustive classical law and explicit native RY/CX probability all agree with 7/15.')
```

```text
Integer-product pair 14/30, exhaustive classical law and explicit native RY/CX probability all agree with 7/15.
```

The full companion independently enumerates classical bit strings and compares the complete positive-amplitude quantum vector and density, as well as the output probability. Its tested basis convention is q₀ most significant, with the parity output last. The zero/one probability endpoints and empty list are included. These finite tests validate the chosen implementation; the product identity gives the mathematical result under the independence/input assumptions.

### 14.8.3 Give a sampling task a sampling baseline

If the task requests S raw parity bits rather than q, a classical baseline must return records. One implementation draws each Xⱼ with rational probability pⱼ and XORs them for every record. Another first computes q from the product, then draws one Bernoulli(q) bit for each record. Both produce the same single-record law under the ideal uniform-random-source model. Fresh independent random draws give the corresponding product law for the S records.

The second sampler is a legitimate baseline: its setup cost is charged, not forbidden. It avoids rebuilding every underlying bit when only their parity is requested. The Python implementation draws a uniform integer in {0,…,d−1} and returns one if it is below a for a/d; exactly a of the d integers give one. It uses a seeded pseudorandom generator for reproducible validation, not a hardware randomness or independence certificate. The two sampling implementations are different algorithms, even when their target output laws agree.

```python
more=(F(1,3),F(2,5),F(3,7));q=b.exact_mean(more)
classical_coins=b.records(more,31,method='coins')
classical_product=b.records(more,31,method='product')
quantum_records,checked_q=b.validate_native(more,31)
assert q==checked_q==b.enumerate_law(more)
for bits in (classical_coins,classical_product,quantum_records):assert 0<=b.check_bits(bits,31)<=1
print('Matched 31-bit record task: coin-parity, optimized classical Bernoulli and native terminal records pass schemas; random frequencies need not coincide.')
```

```text
Matched 31-bit record task: coin-parity, optimized classical Bernoulli and native terminal records pass schemas; random frequencies need not coincide.
```

A fair correctness check does not demand identical random bit lists or an empirical frequency exactly equal to q. Here it checks output schemas and exact reference laws; the native probabilities/full state are checked independently at numerical tolerance. An experiment that returns only the parity bits cannot be charged as though it had returned every data bit or an entire simulated wavefunction. If those additional outputs are required, change the task and account for their storage, readout and processing on both sides.

### 14.8.4 Match accuracy without handicapping an exact method

For a mean estimate from ideal IID parity records, the variance bound recalled in 14.5 gives

$$
\Pr\{|\widehat q-q|>\epsilon\}
\le\frac1{4S\epsilon^2},\qquad
S\ge\left\lceil\frac1{4\delta\epsilon^2}\right\rceil.
$$

This is a sufficient budget, not the optimal number of samples for every q. At ε=1/4, δ=1/20 it gives S=80. The companion checks a fixed q=3/4 case against its exact binomial coverage as an independent finite reference. No particular random record is required to succeed as a deterministic test.

If an implemented distribution has a certified bias at most β<ε from the target, the available statistical radius is ε−β and the sufficient denominator uses (ε−β)² instead. As 14.5 explains, implementation precision, model bias and statistical uncertainty are separate. A small observed floating-point residual against the reference is numerical validation; it is not an interval proof of β or a hardware calibration certificate.

```python
shots=a.mean_budget(F(1,4),F(1,20));assert shots==80
raw,q=b.validate_native((F(3,4),),shots,mode='density_matrix')
assert q==F(3,4) and b.exact_mean((F(3,4),))==q
coverage=a.target_coverage(q,q,shots,F(1,4));assert coverage>=F(19,20)
assert 0<=b.check_bits(raw,shots)<=1
print('Ideal-model mean task: 80-shot variance budget and exact binomial coverage checked; classical exact mean needs no imposed sampling budget.')
print('Floating-point native residual checks are numerical validation, not a rigorous hardware/angle-bias certificate.')
```

```text
Ideal-model mean task: 80-shot variance budget and exact binomial coverage checked; classical exact mean needs no imposed sampling budget.
Floating-point native residual checks are numerical validation, not a rigorous hardware/angle-bias certificate.
```

The exact classical mean needs no imposed 80-shot loop to meet the same requested mean accuracy. Forcing that loop would handicap an eligible baseline. Conversely, exact evaluation of q does not by itself emit S random records when that is the output requested; the sampler and its output costs still belong in that separate task. A comparison must say which of these contracts it evaluates.

### 14.8.5 Use the same resource boundary and unit

With a fully specified implementation, a common resource unit and positive candidate cost, a named ratio can be written

$$
R_{\rm named}=\frac{C_{\rm classical,named}}{C_{\rm candidate}}.
$$

A value above one favors the candidate only for those costs, that named baseline and that scope. Gates, arithmetic operations, seconds, energy and memory are different metrics; a ratio between unlike units is not a speedup. Physical gate durations, routing, reset, loading and readout cannot be supplied by CPU simulator gate counts.

For a serial repeated task, charge setup plus repeated trials plus postprocessing, as in 14.6. The following **synthetic arithmetic fixture** uses one explicitly common “declared work” unit: classical kernel cost 2 and candidate kernel cost 1 appear to give ratio 2. Adding classical postprocessing 10 and candidate setup 100 instead yields complete costs 12 and 101, so the ratio is 12/101. These numbers are invented model inputs for diagnosing a faulty comparison, not timing observations.

```python
kernel=b.cost_ratio(2,1)
cold=b.cost_ratio(b.end_cost(0,2,1,10),b.end_cost(100,1,1,0))
assert kernel==2 and cold==F(12,101)
assert b.cost_ratio(12*9,100+9)<1 and b.cost_ratio(12*10,100+10)>1
print('Synthetic common-unit costs: kernel ratio 2, complete cold-task ratio 12/101; shared-setup model crosses at 10 tasks.')
print('These are declared arithmetic fixtures, not measured device timings or quantum-advantage data.')
```

```text
Synthetic common-unit costs: kernel ratio 2, complete cold-task ratio 12/101; shared-setup model crosses at 10 tasks.
These are declared arithmetic fixtures, not measured device timings or quantum-advantage data.
```

If the candidate setup is legally shared across K tasks in a different amortized-work contract, the same fixture has costs 12K and 100+K. The candidate becomes cheaper when 12K>100+K, first at integer K=10. This change in conclusion comes from the declared reuse contract; a cold single-task result and an amortized batch result answer different questions. Data changes that invalidate setup, retries, success repetitions and unsuccessful candidates must be charged under the actual workflow. Do not report only the successful run or omit a failed attempt's work.

### 14.8.6 Record an actual dated software experiment without relabeling it

The repository includes a small CPU timing receipt for three preselected explicit inputs of sizes n=2,3,4, requesting 43 raw parity records each. The two arms are the product-based classical sampler and `native_records`, which builds and runs the FlagQuantum parity circuit with **only the requested sample output**. Full density/probability diagnostics are outside this timed path and were validated separately. Comparing a reference path that requests a dense density matrix with a task path that requests one bit would measure a changed output request.

The protocol uses one warmup per arm and three measured repetitions per case, alternates arm order, retains every measured duration, and records seeds, source hash, software versions, CPU platform and clock. The timed region includes input validation, product setup or circuit construction, sampling/execution and conversion to the returned tuple. The common fixtures are already parsed `Fraction` objects; file I/O and creating those shared inputs are outside both timed arms. Imports/process startup, physical-QPU loading, network and queueing are not measured; this is a warmed single-process software experiment. No physical device execution occurred.

```python
receipt=json.loads((Path(b.__file__).resolve().parents[2]/'book/section-evidence/14.8/cpu-timing.json').read_text())
assert receipt['native_calls']==12 and receipt['classical_calls']==12
assert receipt['implementation_sha256']==hashlib.sha256(Path(b.__file__).read_bytes()).hexdigest()
assert len(receipt['cases'])==3
saved_table=(Path(b.__file__).resolve().parents[2]/'book/section-evidence/14.8/cpu-timing-table.md').read_text()
for row in receipt['cases']:
 c=row['median_ns']['classical-product-sampler'];q=row['median_ns']['FlagQuantum-CPU-terminal']
 ratio=f'{c/q:.6f}'if q else 'undefined'
 expected_line=f"| {row['n']} | 43 | {c/1000:.3f} | {q/1000:.3f} | {ratio} |"
 assert expected_line in saved_table
for row in receipt['cases']:
 for values in row['times_ns'].values():assert len(values)==3 and all(v>=0 for v in values)
assert len(b.native_records(ps,17))==17
print('Dated CPU timing receipt: three cases, one warmup and three retained repetitions per arm; 12 native calls recorded separately.')
print('Timed path returns only requested raw records; no ratio threshold, QPU timing or best-classical claim is inferred.')
```

```text
Dated CPU timing receipt: three cases, one warmup and three retained repetitions per arm; 12 native calls recorded separately.
Timed path returns only requested raw records; no ratio threshold, QPU timing or best-classical claim is inferred.
```

Observed medians from the three measured CPU repetitions, rounded for display (both time columns are in microseconds):

| n | Requested bits | Classical median (µs) | FlagQuantum CPU median (µs) | Median ratio C/FQ |
| --- | ---: | ---: | ---: | ---: |
| 2 | 43 | 17.625 | 1002.750 | 0.017577 |
| 3 | 43 | 17.500 | 1033.459 | 0.016933 |
| 4 | 43 | 19.041 | 1190.208 | 0.015998 |


The last column is only the ratio of those named software medians, not a speedup confidence interval. The [raw CPU timing receipt](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-evidence/14.8/cpu-timing.json) and [benchmark program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-evidence/14.8/benchmark.py) are the numerical results, with all values and exclusions retained. They are descriptive software timings over these named implementations. Three repetitions do not establish a runtime distribution, a statistically reliable speed advantage, the best classical algorithm or a physical quantum advantage. Seed replay is not extra independent evidence. Numerical agreement with the ideal target is scoped to the stated tolerance, not a rigorous implementation-error certificate. The validation never requires a timing ratio to exceed one.

A serious empirical comparison would need an appropriate baseline search, controlled settings, representative instances, a predeclared aggregation/error analysis, complete preprocessing/output costs, robustness to implementations/hardware, and matching validated answer quality. A faster result over one named code version should be reported with that qualification, not silently promoted to a claim against every classical method.

### 14.8.7 Separate finite implementation evidence from an asymptotic claim

Different conclusions require different evidence:

| Claim | Necessary evidence boundary |
| --- | --- |
| This small program implements the specified model | Independent references, complete code, tolerances and failure cases |
| This implementation used fewer declared logical resources | Same task, access, units, alphabet/precision and complete ledgers |
| This implementation ran faster than a named baseline here | Matched validated quality, dated implementations/hardware and sound timing protocol |
| This algorithm has a proved asymptotic advantage in a stated model | A mathematical upper/lower-bound or conditional result with its assumptions |
| This task exceeds the relevant classical comparison class | A justified statement about that class; testing one weak implementation is insufficient |

Finite timing data alone cannot determine an arbitrary algorithm family's asymptotic behavior. For a concrete logical counterexample, fix a largest tested size N and define **synthetic cost functions**

$$
\begin{aligned}
T_Q(n)&=n,\qquad T_{C,A}(n)=n,\\
T_{C,B}(n)&=
\begin{cases}n,&n\le N,\\n^2,&n>N.\end{cases}
\end{aligned}
$$

All three agree at every tested positive size through N. Beyond that range one classical function remains linear while the other is quadratic. Thus the finite values are compatible with different asymptotic relations. These are constructed functions illustrating logical insufficiency, not measured algorithm runtimes or a classical lower-bound proof. Mathematical analysis of known code may establish more; the finite measurements alone do not supply it.

```python
for n in range(1,9):
 f=b.finite_curves(n,8);assert f['quantum_model']==f['classical_A']==f['classical_B']
f=b.finite_curves(9,8);assert f['classical_A']==9 and f['classical_B']==81
assert 'not QPU' in b.claim_scope('CPU-timing-over-named-code','CPU-simulator')
try:b.claim_scope('asymptotic-quantum-advantage','CPU-simulator')
except ValueError:pass
else:raise AssertionError('Finite toy data certified an asymptotic claim')
print('Two synthetic classical families agree at every tested size 1..8 but diverge at 9; finite agreement cannot determine their asymptotic relation.')
```

```text
Two synthetic classical families agree at every tested size 1..8 but diverge at 9; finite agreement cannot determine their asymptotic relation.
```

Likewise a large dense statevector contains 2ᵂ amplitudes, but that representation's size is not a lower bound for the scalar parity task solved above. Neither the number of simulated qubits, entanglement by itself, nor the cost of a naive classical enumeration establishes quantum advantage. A conditional complexity result must name its model/conjecture; an oracle-query comparison must retain its oracle assumptions; an empirical hardware statement must remain tied to its measured task, quality and dated baseline scope.

### 14.8.8 Make acceptance and rejection reviewable

The operational checklist is: state the task/access/instances; specify output and acceptable error/success; explain the selected classical algorithms and their search scope; freeze code/versions and numerical/resource units; validate each output independently; account for all relevant work; retain unsuccessful/mismatched cases; report only the conclusion warranted by that evidence. An implementation receipt is not independent mathematical review or a lower-bound theorem. The helper's claim-scope check is an editorial guard, not an automated scientific certifier.

```python
assert b.invalid_checks()==20 and b.RUNS==3
sizes=[len(x)for x in task.instances];assert sizes==[2]
assert b.claim_scope('software-correctness','CPU-simulator')=='Bounded implementation evidence only'
print('20 malformed task/access/precision/metric/claim/record contracts rejected before further native execution.')
print('Body: three companion-native calls plus one explicit fq.run; scope remains CPU software correctness/comparison protocol, not quantum advantage.')
```

```text
20 malformed task/access/precision/metric/claim/record contracts rejected before further native execution.
Body: three companion-native calls plus one explicit fq.run; scope remains CPU software correctness/comparison protocol, not quantum advantage.
```

The actual APIs used here are released FlagQuantum 0.3.1 `Circuit.RY`, `CX`, structural `analysis()`, `run`, exact `probabilities`/`density_matrix` and terminal `samples` on CPU complex128. Python is 3.12.14 and Torch 2.13.0. The full-vector/density/scalar checks use atol=10⁻¹² and rtol=0, with no phase alignment, clipping or input normalization repair. `Fraction` product and finite-enumeration references are exact; native angle preparation is floating-point and separately validated. The native sample records and classical pseudorandom samples are checked for shape/bits and counted, not forced to have matching frequencies.

The complete program [classical_baselines.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/classical_baselines.py) executes 52 native circuits: 13 input cases including empty, deterministic endpoints and nontrivial rational probabilities, both statevector/density-matrix modes and record lengths 1 and 31. Its local guards limit lists to five probabilities and sampling to 1000 records; they are teaching/reference limits, not framework limits. Exact scalar product, exhaustive finite law, full amplitudes/densities, task eligibility, complete-cost fixtures, finite-claim counterexamples and 20 malformed contracts are checked. The 12 timing-path native calls are recorded separately, as are the four body calls. No native “quantum advantage verifier,” hardware run, optimal-classical search, general complexity classifier or interval calibration theorem is claimed.

From the repository root, run:

```bash
python examples/foundations/classical_baselines.py
python scripts/check_classical_baselines_prose.py
```

Expected output of the complete program:

```text
52 native CPU complex128 circuits: 13 explicit rational-input cases, two modes and two record lengths passed.
Exact integer-product, exhaustive finite-law and scalar amplitude/density references agree; classical coin and product samplers return the requested records.
Exact-mean baseline meets any looser mean accuracy contract; 80-shot ideal estimation budget is separate from implementation-bias certification.
Kernel-only ratio 2 becomes end-to-end ratio 12/101 in declared synthetic work units; finite data do not decide asymptotic behavior.
20 invalid task/access/precision/cost/claim/record contracts rejected before further execution; no quantum advantage claimed.
```

**Check your understanding.** Why may a classical exact formula be an eligible baseline for a noisy estimation task? When would it fail to fulfill a raw-record task? Which boundary changes when a benchmark requests a full density matrix only from one arm? What can a named timing ratio say, and what can it not say?

**Problems and transfer.**

- **14.8-A — independent baseline.** For p=(1/3,2/5), derive the integer pair and q by both the product and explicit enumeration. Show that at least one observed quantum frequency differing from q is compatible with a correct sampler; identical record lists are not the criterion.
- **14.8-B — complete cost.** In the synthetic common-unit fixture, derive the cold-task ratio and the first integer K at which setup sharing changes the ordering. What task/data-reuse assumption would be violated if every new input required paying setup again?
- **14.8-C — fresh execution.** Test p=(2/7,3/8,4/11), (1/5,2/9,3/10,4/13) and (1/6,2/7,3/11,4/15,5/17), S=37, both modes. Add the mixed deterministic inputs (1,0) and (0,1,0). Compare exact product/enumeration and full native references, validate both classical samplers' record schemas and reject a stale instance/output/accuracy contract.
- **14.8-D — audit a claim.** A report times classical full-state enumeration against a quantum scalar kernel, omits loading and repetitions, then fits an exponential separation to n≤8 CPU simulations. Identify four distinct unsupported steps and specify the evidence needed for a narrower defensible claim. Can replacing the named baseline by a better classical method change the observed ratio without changing the task?

<details markdown="1">
<summary>Answers and verification guidance for 14.8-A–D</summary>

**A.** D=15,A=1 gives (D−A)/(2D)=14/30=7/15. The two odd strings 01 and 10 have probabilities (2/3)(2/5)=4/15 and (1/3)(3/5)=3/15, which sum to 7/15. A single record is either 0 or 1, so its frequency differs from 7/15 even when drawn from the correct distribution. Correct output laws do not require identical random realizations.

**B.** The cold complete costs are 12 and 101, giving 12/101 despite kernel ratio 2. Sharing setup over K tasks gives 12K/(100+K); this exceeds one when 11K>100, first at K=10. If setup is invalidated for every input, the candidate instead pays 101K and there is no such crossover in this fixture. These remain hypothetical costs in declared units, not measured quantum speedups.

**C.** There are ten new native calls: three rational lists plus two mixed deterministic lists, each in two modes. Both mixed deterministic inputs have odd parity with probability one. Exact products and exhaustive laws agree, full native vectors/densities and probabilities match within the stated numerical tolerance, and every requested record has valid shape/bits. No record-frequency confidence test or hardware certificate is inferred. Stronger accuracy is eligible; weaker quality or changed access/output/instances is not the same comparison.

**D.** The report changes the output task, changes the resource boundary, conflates CPU simulation with physical quantum execution, and infers asymptotic separation from finite data without a mathematical bound. A narrower report would name both implementations and matched requested outputs/quality, charge their full costs, record versions/hardware and timing uncertainty, and call the result a scoped software comparison. A better classical algorithm can change the named ratio; the task did not change. One code's failure to compete is not a lower bound on every classical method.

</details>

**Source and review status.** The frozen NC §3.2.1 locator, beginning on printed page 136, was checked against the [publisher's contents](https://assets.cambridge.org/97811070/02173/toc/9781107002173_toc.pdf), not treated as access to the full chapter. The book's [reader-review/acceptance protocol](../reader-continuity.md) supplies the original editorial evidence obligations. The product, bitlength, task-eligibility examples and finite-function counterexample are given locally; no unproved separation or new standalone paper reproduction is imported. The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/14.8.json) distinguishes author validation from independent mathematical/implementation review and reader trial. This remains a working draft. Continue, when drafted, with [14.9 Resource-audit laboratory](../section-plans/03-algorithms.md#sec-computational-models-complexity-and-quantum-advantage-8).

<!-- end-section-14.8 -->
