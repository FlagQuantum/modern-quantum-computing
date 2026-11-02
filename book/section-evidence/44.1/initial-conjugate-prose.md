# 44. Exact Simulation, Tensor Execution, and Numerical Reliability

**Working draft: section 44.1 · Writing Baseline 1.0 · November 2, 2026.** The B03 execution bridge is drafted here before the algorithm laboratories. The global chapter number and Volume VII placement remain unchanged. Author validation is separate from independent mathematical/implementation review and reader trial, which remain pending.

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-1"></span>
## 44.1 Requested outputs and exact-simulation cost

**Question.** How much must a classical simulator store or return when the requested answer is a state, a density matrix, a few amplitudes, samples or expectations?

The prerequisites are [4.2, registers and basis indices](ch-composite-systems-tensor-products-and-qubit-ordering.md#sec-composite-systems-tensor-products-and-qubit-ordering-2) and [2.3, linear maps and coordinates](ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-3). We derive finite storage and output bounds completely for a declared **explicit dense representation**. These are not universal lower bounds for every simulation algorithm, nor costs of operating a quantum device. A tensor-network method, a sparse formula or a task-specific classical algorithm may answer a smaller question without constructing this representation.

### 44.1.1 Count coordinates before allocating memory

Let n≥0 be the number of qubits. In our q₀-first basis convention, x=(x₀,…,xₙ₋₁) has index i(x)=Σⱼxⱼ2ⁿ⁻¹⁻ʲ. There is one empty bit string at n=0. Appending either 0 or 1 doubles the number of strings, so induction gives N=2ⁿ. A dense pure-state vector stores one complex amplitude ψᵢ for each string:

$$
|\psi\rangle=\sum_{i=0}^{N-1}\psi_i|i\rangle,\qquad
N=2^n,\qquad\sum_i|\psi_i|^2=1.
$$

A matrix representing a linear operator on the same space has one entry per ordered pair of basis labels (i,j), hence N²=4ⁿ complex slots. For a pure state, the **density matrix** is ρ=ψψ†, meaning ρᵢⱼ=ψᵢψⱼ*. More generally an ensemble with probabilities wₗ and unit vectors ψ⁽ˡ⁾ has ρᵢⱼ=Σₗwₗψᵢ⁽ˡ⁾ψⱼ⁽ˡ⁾*. This locally defines the matrix notation needed here; general mixed-state/channel execution belongs to 44.4. A pure density matrix can be represented compactly by ψ, but a request to materialize all its entries still has N² slots.

Let z be bytes per complex entry and r=z/2 bytes per real component. In the tested Torch dtypes, complex64 has z=8,r=4 and complex128 has z=16,r=8. Thus

$$
B_{\rm vector}=z2^n,\qquad B_{\rm density}=B_{\rm dense\ operator}=z4^n.
$$

These count array payloads, not independent physical degrees of freedom: normalization, overall phase and Hermitian symmetry do not remove slots from a specified full rectangular array. Hermitian packing would be a different representation contract. Headers, strides, allocator bookkeeping, alignment, copies and work buffers are additional.

```python
import math,torch,flagquantum as fq
from dataclasses import replace
from examples.foundations import requested_outputs as o,statistical_ensembles as e
for dtype,expected in ((torch.complex64,(64,512)),(torch.complex128,(128,1024))):
 s=o.actual_arrays(3,dtype);assert (s['state_bytes'],s['density_bytes'])==expected
assert o.dimension(0)==1
print('Three qubits: eight complex vector entries or 64 complex matrix entries; complex64 payloads 64/512 bytes, complex128 128/1024 bytes.')
```

```text
Three qubits: eight complex vector entries or 64 complex matrix entries; complex64 payloads 64/512 bytes, complex128 128/1024 bytes.
```


### 44.1.2 Make a budget prediction without allocating the array

Adding one qubit doubles vector payload and quadruples full density payload, directly from the exponents. Since 1 GiB=2³⁰ bytes, one complex128 30-qubit vector and one 15-qubit density matrix each require 16 GiB. This estimate creates Python integers only; the program never allocates either large array. A decimal GB is 10⁹ bytes, so GiB and GB must not be interchanged.

For a byte budget H, a single vector array fits this payload test exactly when z2ⁿ≤H; a full density fits when z4ⁿ≤H. If H≥z, the largest integers allowed by these tests are

$$
n_{\rm vector}\le\left\lfloor\log_2(H/z)\right\rfloor,\qquad
n_{\rm density}\le\left\lfloor\tfrac12\log_2(H/z)\right\rfloor.
$$

When H<z, not even the n=0 one-entry array fits. The implementation compares integers rather than rounding a floating-point logarithm at a power-of-two boundary. A fit is necessary for that array, not sufficient for a full run. Two simultaneous vector buffers need 2z2ⁿ payload bytes; materializing ψ and ρ together needs z(2ⁿ+4ⁿ), before any other live data. If a returned tensor aliases an existing allocation, do not count it as a second owning buffer. Conversely a copy is not free. This section reports payloads and observed result tensors, without claiming a measured allocator/process/GPU peak.

```python
GiB=2**30
assert o.storage(30)['state_bytes']==o.storage(15)['density_bytes']==16*GiB
assert o.fit(30,'statevector',16*GiB) and not o.fit(31,'statevector',16*GiB)
assert o.payload(30,'amplitudes',count=3)['bytes']==48
assert o.payload(30,'expectations',count=2)['bytes']==16
assert o.payload(30,'probabilities',qubits=(29,0))['bytes']==32
print('Virtual estimates only: 30-qubit vector and 15-qubit full density each16GiB; three amplitudes48 bytes, two expectations16 bytes, two-qubit probabilities32 bytes.')
```

```text
Virtual estimates only: 30-qubit vector and 15-qubit full density each16GiB; three amplitudes48 bytes, two expectations16 bytes, two-qubit probabilities32 bytes.
```


### 44.1.3 Distinguish the full vector from a selected amplitude

Consider three qubits initially zero, RY₀(π/3), then P₀(π/2), then CX(0,1), CX(0,2), then X₁. Angles are in radians. The first rotation gives √3/2|0⟩+1/2|1⟩ on q₀, and P multiplies its |1⟩ coefficient by i. The two CX gates copy the computational-basis label coherently, and X₁ flips the middle bit. Therefore

$$
|\psi\rangle=\frac{\sqrt3}{2}|010\rangle+\frac{i}{2}|101\rangle,
\qquad i(010)=2,\quad i(101)=5.
$$

The statevector contains eight complex entries, although this particular vector has only two nonzero coordinates. A request for its amplitude at index 5 returns the complex number i/2, not the probability 1/4. Phase information is lost by taking the squared modulus.

In the installed FlagQuantum profile we execute `fq.run` in statevector mode, obtain `result.statevector()`, and then index the returned tensor in Python. This is an actual state-producing run followed by **host extraction**. It is not a demonstrated amplitude-only native execution strategy. In particular, indexing one coefficient after producing a full vector does not reduce that run's state storage to 16 bytes.

```python
n=3;theta=math.pi/3;phi=math.pi/2;flips=(0,1,0);mask=(1,0)
c=fq.Circuit(3,dtype=torch.complex128).RY(0,theta=theta).P(0,theta=phi).CX(0,1).CX(0,2).X(1)
r=fq.run(c,options=replace(e.OPTIONS,mode='statevector'))
v=r.statevector()[0]
expected=torch.zeros(8,dtype=torch.complex128);expected[2]=math.sqrt(3)/2;expected[5]=.5j
e.close(v,expected);e.close(v[5],torch.tensor(.5j,dtype=torch.complex128))
assert v.numel()*v.element_size()==128
print('Actual native state-only run: sqrt(3)/2 at index2, i/2 at index5; full state payload128 bytes; amplitude extracted by host indexing.')
```

```text
Actual native state-only run: sqrt(3)/2 at index2, i/2 at index5; full state payload128 bytes; amplitude extracted by host indexing.
```


### 44.1.4 Marginals and records are different requested objects

Let Q=(qₐ₀,…,qₐₘ₋₁) be an **ordered** tuple of distinct selected qubits. For an output label y=(y₀,…,yₘ₋₁), define its index j(y)=Σₜyₜ2ᵐ⁻¹⁻ᵗ. Summing mutually exclusive basis probabilities gives

$$
p_Q(y)=\sum_{x:\,x_{a_t}=y_t\ \text{for all }t}|\psi_{i(x)}|^2.
$$

There are 2ᵐ labels y, so a full selected probability table needs r2ᵐ bytes, not r2ⁿ unless m=n. For Q=(q₁,q₀) in our example, 010 maps to label 10, index 2, and 101 maps to 01, index 1. Thus p_Q=(0,1/4,3/4,0). Reversing the mask to (q₀,q₁) swaps the middle probabilities; ignoring the tuple order changes the answer's meaning.

A record of S terminal samples on these m qubits has S rows and m binary labels per row. An ideally packed record requires Sm bits; a rectangular int64 tensor occupies 8Sm bytes. Here S=11,m=2 gives 22 logical bits but 176 actual tensor bytes. Headers and serialization are extra. Do not assume two separate sampling requests have aligned rows. Native exact probability output is a floating-point simulator calculation; a finite sample frequency is a random statistic and need not equal that probability.

```python
queries,qr=o.execute(n,theta,phi,flips,mask,profile='queries',shots=11)
e.close(queries.measurement('selected').value[0],torch.tensor([0.,.25,.75,0.],dtype=torch.float64))
assert (qr['selected_probability_bytes'],qr['raw_tensor_bytes'],qr['retained_state_bytes'])==(32,176,128)
assert qr['mask']==(1,0)
print('Native query profile: ordered (q1,q0) probabilities (0,1/4,3/4,0), 32 bytes; 11 two-bit rows occupy176 int64 bytes; full state still retained.')
```

```text
Native query profile: ordered (q1,q0) probabilities (0,1/4,3/4,0), 32 bytes; 11 two-bit rows occupy176 int64 bytes; full state still retained.
```


### 44.1.5 Returning a density matrix changes the output obligation

The pure density follows by multiplying coefficients and their conjugates:

$$
\rho=\frac34|010\rangle\langle010|+\frac14|101\rangle\langle101|
-\frac{i\sqrt3}{4}|010\rangle\langle101|
+\frac{i\sqrt3}{4}|101\rangle\langle010|.
$$

For example ρ₂₅=(√3/2)(i/2)*=−i√3/4, while ρ₅₂ is its conjugate. Diagonal probabilities alone cannot recover those coherences. The full requested array is 8×8, hence 64 complex128 entries or 1024 bytes, even when many entries vanish. It is a matrix output, not a second list of amplitudes.

The next call explicitly selects density-matrix execution mode and requests a full density output. Its agreement with ψψ† checks the result on this pure example; it does not turn a general mixed state into a unique statevector. We use the `statevector()` accessor only for tested statevector-mode results. A full density output can also be formed from a pure-state simulation by an outer product; that would still require materializing N² output entries, without proving that the earlier evolution used N² working storage.

```python
full,dr=o.execute(n,theta,phi,flips,mask,mode='density_matrix',profile='full',shots=11)
rho=full.measurement('rho').value[0]
e.close(rho,expected[:,None]*expected.conj()[None,:])
e.close(rho[2,5],torch.tensor(-1j*math.sqrt(3)/4,dtype=torch.complex128))
assert dr['density_output_bytes']==1024
print('Native full density output: shape8x8, 1024 bytes; rho[2,5]=-i*sqrt(3)/4, with the conjugate entry at [5,2].')
```

```text
Native full density output: shape8x8, 1024 bytes; rho[2,5]=-i*sqrt(3)/4, with the conjugate entry at [5,2].
```


### 44.1.6 A scalar expectation can require a large calculation

For a Hermitian matrix A, define its pure-state expectation by the finite quadratic sum. Substituting ρᵢⱼ=ψᵢψⱼ* into the diagonal sum defining the trace gives

$$
\langle A\rangle=\sum_{i,j}\psi_i^*A_{ij}\psi_j
=\operatorname{Tr}(\rho A),\qquad
\operatorname{Tr}(\rho A)=\sum_{i,j}\rho_{ij}A_{ji}.
$$

To check the equality, replace ρᵢⱼ by ψᵢψⱼ*, then interchange the dummy indices i,j. Complex conjugating the quadratic sum and using Aⱼᵢ*=Aᵢⱼ proves it is real. The same identity holds for an ensemble by distributing the finite weighted sum, without additional execution assumptions.

For Z₀, its action is +1 on strings with x₀=0 and −1 when x₀=1, so ⟨Z₀⟩=3/4−1/4=1/2. The product X₀X₁X₂ interchanges 010 and 101. Its expectation is the sum of their two cross terms, 2 Re[(√3/2)*i/2]=0. Native Pauli-product requests below are compared with scalar coordinate sums that retain conjugation.

T real expectations require rT output bytes: two float64 values occupy 16 payload bytes. This output count says nothing by itself about computing an arbitrary expectation. A generic dense A quadratic sum can examine N² matrix entries; diagonal and Pauli-product structure can permit O(N) statevector contractions after evolution. Which strategy is used must be established separately. The request API does not imply that every scalar answer can be found in constant time or constant memory.

```python
z=sum((-1)**o.u.bits(x,3)[0]*abs(v[x].item())**2 for x in range(8))
x=sum(v[j].item().conjugate()*v[7-j].item() for j in range(8))
e.close(queries.measurement('z').value[0],torch.tensor(z,dtype=torch.float64))
e.close(queries.measurement('x').value[0],torch.tensor(x,dtype=torch.complex128))
assert abs(z-.5)<1e-12 and abs(x)<1e-12
assert o.payload(3,'expectations',count=2)['bytes']==16
print('Scalar coordinate sums match native Z0=1/2 and X0X1X2=0 within1e-12; two real outputs require16 payload bytes, not a16-byte execution guarantee.')
```

```text
Scalar coordinate sums match native Z0=1/2 and X0X1X2=0 within1e-12; two real outputs require16 payload bytes, not a16-byte execution guarantee.
```


### 44.1.7 Separate evolution work from output writes

In an explicitly dense matrix-vector algorithm, each of N output coordinates is a length-N dot product. With no zero skipping or special structure, that algorithm uses N² complex multiplications and N(N−1) complex additions for one matrix application. It also stores the N²-entry operator. These are costs of that algorithm, not of every gate implementation.

For a k-qubit local gate, fix the other n−k basis labels. There are 2ⁿ⁻ᵏ=N/d such groups, where d=2ᵏ. Within each group a d×d local matrix produces d length-d dot products. Counting rows and factors gives

$$
C_{\times}=\frac Nd\,d^2=Nd=N2^k,\qquad
C_+=\frac Nd\,d(d-1)=N(2^k-1).
$$

The local matrix has d² entries; an out-of-place update needs two length-N vector buffers rather than an N×N global gate matrix. For fixed k this particular arithmetic scheme is O(2ⁿ) per local gate. A density update UρU† can apply the same local action to every column on the left and every row on the right: N copies of each pass, hence 2N²d multiplications in this unoptimized scheme and O(N²) density buffers. The indexed equality of the local kernel and the global operator is proved in 44.2; the present counting does not import an unproved performance theorem or assert these are actual backend operation counters. Gate fusion, diagonal/permutation structure, threading and memory traffic can change a real implementation's cost.

For requested outputs, use a separate **explicit-output model**: a fresh materialized complex array has one fixed-width complex word per entry. Writing or serializing all L entries requires L word writes/transfers, hence Ω(L) work in that model. This proves Ω(2ⁿ) for an exported full vector and Ω(4ⁿ) for an exported full density. A request for K named amplitudes, T expectations or a 2ᵐ-entry probability table instead has K complex words, T real words or 2ᵐ real words. An unpacked sample tensor has Sm integer entries; a packed record has Sm bits, or at least ⌈Sm/w⌉ words with w bits per machine word.

These lower bounds concern explicit materialization/export. Returning a handle or a view of an already existing array can take constant interface work; its data still occupies storage, and exporting all entries later incurs the corresponding transfer. A bandwidth-only model with rate β bytes per second additionally gives T_transfer≥B_output/β, conditional on that model, not a measured device timing. Output size is a necessary cost, not a sufficient estimate of evolution, sampling, communication or peak memory. In particular a short answer does not supply an efficient general algorithm for obtaining it.

```python
w=o.work(3,1)
assert (w['blocks'],w['local_multiplications'],w['local_additions'],w['dense_multiplications'],w['dense_additions'])==(4,16,8,64,56)
assert w['density_two_pass_multiplications']==256
assert sum(1 for block in range(4)for row in range(2)for col in range(2))==16
print('Declared unoptimized arithmetic: one-qubit state update16 complex products/8 additions; full8x8 matvec64/56; density left/right passes256 products.')
```

```text
Declared unoptimized arithmetic: one-qubit state update16 complex products/8 additions; full8x8 matvec64/56; density left/right passes256 products.
```


### 44.1.8 Freeze a workload and reject ambiguous accounting

A reproducible workload specifies n, input-state construction, gate family/count, precision, execution strategy/backend, selected output kinds and ordered labels, S if sampling, batch size and which simultaneous allocations/transfers count. This laboratory has batch size one, CPU complex128 native evolution, finite parameters and full reference checks. Array-only tests additionally exercise complex64. The native workloads have no noise, hardware routing, gradients or distributed execution. Do not estimate those costs from this result.

The APIs actually exercised on released FlagQuantum 0.3.1 are `Circuit.RY/P/CX/X`, `run`, the statevector-mode result accessor, and `probabilities`, `expectation`, `density_matrix` and terminal `samples`. The companion's amplitude and byte-planning functions are book-side mathematics. In this tested CPU statevector path the result still exposes the full state even when its terminal requests are small. We do not claim an output-sensitive planner, amplitude-only execution, universal state access for every backend or a peak-memory optimization. The density output is a simulator diagnostic, not free tomography of a physical device.

“Exact simulation” here means the full stated state/density strategy without an intentional truncation or stochastic approximation to those deterministic outputs. Floating-point roundoff remains: no symbolic exactness, interval certificate or zero numerical error follows from that name or from `allow_approximate=False`. The numerical profile is Python 3.12.14, Torch 2.13.0, CPU complex128, absolute tolerance 10⁻¹² and relative tolerance zero, with no phase alignment, clipping or normalization repair. Samples are validated for schema and allowed outcomes; no empirical-frequency hit is required.

```python
assert o.payload(3,'samples',qubits=mask,shots=11)==dict(entries=22,packed_bits=22,int64_bytes=176)
assert o.payload(0,'probabilities',qubits=())==dict(entries=1,bytes=8)
assert o.payload(3,'amplitudes',count=0)==dict(entries=0,bytes=0)
assert o.invalid_checks()==13 and o.RUNS==2
print('22 record bits versus176 int64 bytes; empty marginal has one probability; 13 invalid request/storage contracts rejected before execution.')
print('Body: three actual native calls, including explicit state-only fq.run; no single-amplitude native endpoint or output-sensitive memory optimization asserted.')
```

```text
22 record bits versus176 int64 bytes; empty marginal has one probability; 13 invalid request/storage contracts rejected before execution.
Body: three actual native calls, including explicit state-only fq.run; no single-amplitude native endpoint or output-sensitive memory optimization asserted.
```


The complete [requested_outputs.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/requested_outputs.py) executes 56 native circuits: 48 query/full-output calls on n=1,…,4, three angle cases including deterministic endpoints and both statevector/density-matrix modes, plus eight state-only runs including negative rotations. Independent scalar coordinates, outer products, ordered marginals and Pauli expectations are checked. Fourteen small actual allocations verify both complex dtypes for n=0,…,6; large estimates allocate no large quantum array. Local arithmetic counts and thirteen malformed requests/storage contracts are also checked. The helper's n≤5 native, N≤64 allocation-test, S≤1000 and n≤60 estimate guards bound this teaching program, not FlagQuantum's capacity.

Run from the repository root:

```bash
python examples/foundations/requested_outputs.py
python scripts/check_requested_outputs_prose.py
```

Expected output of the complete program:

```text
56 native CPU complex128 circuits: 48 terminal query/full-output runs and eight state-only runs, n=1..4, both tested execution modes.
Scalar complex coordinates, full density, ordered marginals, Pauli expectations and terminal record schemas agree; no frequency-hit test.
14 actual complex64/complex128 array checks for n=0..6 match dense payload formulas; virtual 30-qubit state and 15-qubit density each require16GiB.
Selected requests retain the full statevector in this tested CPU profile; scalar output size does not certify scalar working memory.
Dense/local arithmetic counts, explicit-output payloads, budget endpoints and 13 invalid contracts passed; no hardware or universal simulation lower bound claimed.
```

**Check your understanding.** Why can the same pure state have an eight-entry vector and a 64-entry full density output? Which bytes are counted when an accessor returns a view? Why does a single requested expectation not establish a constant-time algorithm? What changes when a selected mask is reversed?

**Problems and transfer.**

- **44.1-A — fit versus feasibility.** In a 1 GiB payload budget, find the largest complex128 vector and density qubit counts. Repeat for complex64. Then require two simultaneous owning vector buffers. Explain why none of these tests alone establishes total process feasibility.
- **44.1-B — explicit output.** For n=20, complex128/float64, request K=7 amplitudes, T=3 expectations, a full marginal on m=4 ordered qubits and S=1000 unpacked four-bit samples. Compute each payload and the packed sample size. If a statevector implementation first computes the full state, may its working memory be bounded by their sum?
- **44.1-C — fresh execution.** Test the five-qubit flipped family with θ=−0.91, φ=0.73, flips=(1,0,1,0,0), ordered mask (4,0,2), S=23, both modes and query/full profiles, plus a state-only run. Test n=2, θ=1.17, φ=−0.38, flips=(1,0), mask (1,0), both modes. Finally compare single-qubit phase +0.8 and −0.8 at θ=0.69: probabilities agree, but the complex amplitudes differ. Retain the output/storage receipts and reject a stale/duplicate mask contract.
- **44.1-D — scope of a lower bound.** A program returns a scalar, so its author claims O(1) time and memory. Another exports all density entries of a specially structured pure state and calls its Ω(4ⁿ) output work a proof that every scalar simulation task is exponential. Diagnose both mistakes. Can a lazy array handle contradict the explicit-export bound?

<details markdown="1">
<summary>Answers and verification guidance for 44.1-A–D</summary>

**A.** Complex128 has z=16, so \(16\,2^n\le2^{30}\) gives n≤26 for one vector and \(16\,4^n\le2^{30}\) gives n≤13 for one density. Complex64 has z=8: n≤27 and n≤13 respectively. Two vector buffers cost \(2z2^n\), reducing the maxima to 25 and 26. Other live outputs, input data, runtime metadata, temporary buffers and allocator/parallel copies are still uncounted.

**B.** The payloads are 112 bytes, 24 bytes, 128 bytes and 32000 bytes respectively. Packed samples need 4000 bits or 500 bytes. One complex128 20-qubit state alone needs 16777216 bytes=16 MiB, so those small outputs do not bound the statevector executor's working storage. Nor does their sum include any intermediate allocations or preprocessing.

**C.** There are nine fresh native calls: four five-qubit query/full calls, one state-only call, two two-qubit full-output calls and two single-qubit query calls. The selected five-qubit record has 69 bits, stored here in 552 int64 bytes. Its selected probability table has eight real entries=64 bytes; the full vector is 512 bytes and full density 16384. The n=2 reversed mask explicitly orders q₁ before q₀. In the single-qubit pair, multiplying the |1⟩ amplitude by opposite phases leaves squared moduli unchanged but reverses its imaginary part. A probability-only comparison would miss that distinction. The transfer artifact checks scalar references without a required frequency hit.

**D.** Output size alone does not upper-bound the work of computing that output. Conversely an explicit full-array output bound is tied to that requested representation, not to every smaller task or compressed strategy. A lazy handle may avoid materialization at the interface; if the user later requires every explicit entry to be exported, the bound applies to that export. The distinction does not establish or refute any general quantum advantage claim.

</details>

**Sources and review status.** The frozen [QuEST v1 source](https://arxiv.org/pdf/1802.08032v1#page=2), PDF pages 1–3, was inspected for the representation discussion, especially §II.A.1 on page 2: its double-precision statevector payload and the separation from process/communication overhead. No historical benchmark or hardware-capacity claim is imported. The source hash and narrow reading scope are recorded without uploading the paper. The density, output-write and local-arithmetic counts are fully derived above. The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/44.1.json) distinguishes author checks from independent mathematical/implementation review, reader trial and acceptance; this remains a working draft. Continue, when drafted, with [44.2 Applying local gates by tensor indices](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-2).

<!-- end-section-44.1 -->
