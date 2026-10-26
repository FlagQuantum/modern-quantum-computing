# 14. Computational Models, Complexity, and Quantum Advantage

**Working draft: section 14.1 · Writing Baseline 1.0 · October 26, 2026.** The B 02 writing queue reaches this chapter after Chapter 8; Chapters 9–13 retain their own later scheduled batches. Author checks are separate from independent mathematical/implementation review and reader trial, which remain pending.

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
