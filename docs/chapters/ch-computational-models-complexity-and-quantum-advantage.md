# 14. Computational Models, Complexity, and Quantum Advantage

**Working drafts: sections 14.1–14.4 · Writing Baseline 1.0 · October 26, 2026.** The B 02 writing queue reaches this chapter after Chapter 8; Chapters 9–13 retain their own later scheduled batches. Author checks are separate from independent mathematical/implementation review and reader trial, which remain pending.

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
