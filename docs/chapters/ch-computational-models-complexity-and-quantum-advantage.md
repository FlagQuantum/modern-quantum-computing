# 14. Computational Models, Complexity, and Quantum Advantage

**Working drafts: sections 14.1–14.2 · Writing Baseline 1.0 · October 26, 2026.** The B 02 writing queue reaches this chapter after Chapter 8; Chapters 9–13 retain their own later scheduled batches. Author checks are separate from independent mathematical/implementation review and reader trial, which remain pending.

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
