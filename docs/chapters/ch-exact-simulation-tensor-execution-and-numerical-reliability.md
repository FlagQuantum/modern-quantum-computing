# 44. Exact Simulation, Tensor Execution, and Numerical Reliability

**Working drafts: sections 44.1–44.2 · Writing Baseline 1.0 · November 2, 2026.** The B03 execution bridge is drafted here before the algorithm laboratories. The global chapter number and Volume VII placement remain unchanged. Author validation is separate from independent mathematical/implementation review and reader trial, which remain pending.

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

A matrix representing a linear operator on the same space has one entry per ordered pair of basis labels (i,j), hence N²=4ⁿ complex slots. For a pure state, the **density matrix** is ρ=ψψ†, meaning \(\rho_{ij}=\psi_i\psi_j^*\). Here † denotes conjugate transpose and `*` denotes scalar conjugation. More generally an ensemble with probabilities wₗ and unit vectors ψ⁽ˡ⁾ has \(\rho_{ij}=\sum_\ell w_\ell\psi_i^{(\ell)}\psi_j^{(\ell)*}\). This locally defines the matrix notation needed here; general mixed-state/channel execution belongs to 44.4. A pure density matrix can be represented compactly by ψ, but a request to materialize all its entries still has N² slots.

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

Let Q=(qₐ₀,…,qₐₘ₋₁) be an **ordered** tuple of distinct selected qubits. For an output label y=(y₀,…,yₘ₋₁), define its index j(y)=Σₜyₜ2ᵐ⁻¹⁻ᵗ. For computational-basis readout, adopt the Born probabilities Pr(x)=|ψᵢ₍ₓ₎|². Summing mutually exclusive outcomes gives

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

For example \(\rho_{25}=(\sqrt3/2)(i/2)^*=-i\sqrt3/4\), while ρ₅₂ is its conjugate. Diagonal probabilities alone cannot recover those coherences. The full requested array is 8×8, hence 64 complex128 entries or 1024 bytes, even when many entries vanish. It is a matrix output, not a second list of amplitudes.

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

For a Hermitian matrix A, meaning \(A_{ji}^*=A_{ij}\), define its pure-state expectation by the finite quadratic sum. Substituting \(\rho_{ij}=\psi_i\psi_j^*\) into the diagonal sum defining the trace gives

$$
\langle A\rangle=\sum_{i,j}\psi_i^*A_{ij}\psi_j
=\operatorname{Tr}(\rho A),\qquad
\operatorname{Tr}(\rho A)=\sum_{i,j}\rho_{ij}A_{ji}.
$$

To check the equality, replace ρᵢⱼ by \(\psi_i\psi_j^*\), then interchange the dummy indices i,j. Complex conjugating the quadratic sum and using \(A_{ji}^*=A_{ij}\) proves it is real. The same identity holds for an ensemble by distributing the finite weighted sum, without additional execution assumptions.

For Z₀, its action is +1 on strings with x₀=0 and −1 when x₀=1, so ⟨Z₀⟩=3/4−1/4=1/2. The product X₀X₁X₂ interchanges 010 and 101. Its expectation is the sum of their two cross terms, \(2\operatorname{Re}(i\sqrt3/4)=0\). Native Pauli-product requests below are compared with scalar coordinate sums that retain conjugation.

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

The local matrix has d² entries; an out-of-place update needs two length-N vector buffers rather than an N×N global gate matrix. For fixed k this particular arithmetic scheme is O(2ⁿ) per local gate. A density update UρU† can apply the same local action to every column on the left and every row on the right: N copies of each pass, hence 2N²d multiplications in this unoptimized scheme and O(N²) density buffers. The [44.2 kernel proof](#sec-exact-simulation-tensor-execution-and-numerical-reliability-2) supplies the indexed equality to the embedded matrix. These are arithmetic counts for the stated unoptimized algorithm; actual backend operation counts require separate evidence. Gate fusion, diagonal/permutation structure, threading and memory traffic can change a real implementation's cost.

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

**Sources and review status.** The frozen [QuEST v1 source](https://arxiv.org/pdf/1802.08032v1#page=2), PDF pages 1–3, was inspected for the representation discussion, especially §II.A.1 on page 2: its double-precision statevector payload and the separation from process/communication overhead. No historical benchmark or hardware-capacity claim is imported. The source hash and narrow reading scope are recorded without uploading the paper. The density, output-write and local-arithmetic counts are fully derived above. The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/44.1.json) distinguishes author checks from independent mathematical/implementation review, reader trial and acceptance; this remains a working draft. Continue with [44.2 Applying local gates by tensor indices](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-2).

<!-- end-section-44.1 -->

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-2"></span>
## 44.2 Applying local gates by tensor indices

**Question.** Why does gathering selected tensor axes, multiplying a small local matrix and restoring the axes give exactly the same linear map as a full embedded operator?

The prerequisites are [4.6, tensor reshaping as indexed mathematics](ch-composite-systems-tensor-products-and-qubit-ordering.md#sec-composite-systems-tensor-products-and-qubit-ordering-6) and [5.1, chronological composition](ch-gates-reversible-computation-and-circuit-synthesis.md#sec-gates-reversible-computation-and-circuit-synthesis-1). We reuse their conventions to build a minimal independent executor. The F-depth proof below establishes equality for every complex input vector, including unnormalized vectors, with any finite local square matrix. Deterministic quantum gates additionally require unitarity; that is a separate native-execution precondition. Numerical agreement checks the implementation and does not replace this all-input proof.

### 44.2.1 Fix the ordered support and its spectator labels

Let n be the register size, N=2ⁿ and i(x)=Σⱼxⱼ2ⁿ⁻¹⁻ʲ the q₀-first binary index. A flat vector v has entries \(v_{i(x)}\). Let S=(s₀,…,sₖ₋₁) be a tuple of distinct selected qubit labels, in the order used for the local matrix. Let T=(t₀,…,tₙ₋ₖ₋₁) be the complementary labels in increasing order. Write d=2ᵏ and h=2ⁿ⁻ᵏ. For a global bit string x define

$$
a_S(x)=\sum_{j=0}^{k-1}x_{s_j}2^{k-1-j},\qquad
b_T(x)=\sum_{j=0}^{n-k-1}x_{t_j}2^{n-k-1-j}.
$$

Conversely, ι(a,b) is the unique global bit string obtained by placing the k bits of a at S and the n−k bits of b at T. Existence follows by filling each label once; uniqueness follows because S and T partition all labels. Thus x↔(a,b) is a bijection. The packed flat index of (a,b) is ah+b.

For n=3,S=(2,0),T=(1), the axis order is (2,0,1). The original string 001 has a=2,b=0 and packed index 4, while its original flat index is 1. `reshape` alone preserves the logical coefficient sequence; `permute` is what changes which qubit label occupies each axis. Restoring the original logical axes requires the inverse permutation (1,2,0), not a second application of the original permutation.

```python
import torch,flagquantum as fq
from dataclasses import replace
from examples.foundations import tensor_gate_executor as o,statistical_ensembles as e
n=3;S=(2,0);markers=torch.arange(8,dtype=torch.float64).to(torch.complex128)
order,inverse=o.axes(n,S);W=o.pack(markers,n,S)
assert order==(2,0,1) and inverse==(1,2,0)
assert W.real.tolist()==[[0.,2.],[4.,6.],[1.,3.],[5.,7.]]
print('S=(2,0), spectators=(1,): axes(2,0,1), inverse(1,2,0); input001 occupies row2,column0.')
```

```text
S=(2,0), spectators=(1,): axes(2,0,1), inverse(1,2,0); input001 occupies row2,column0.
```


### 44.2.2 Derive the embedded matrix entry by entry

Define a permutation matrix P of dimension N×N by

$$
P_{ah+b,\,i(x)}=
\delta_{a,a_S(x)}\delta_{b,b_T(x)},
$$

where the Kronecker delta δ is one when its two labels agree and zero otherwise. Each column has exactly one nonzero entry, and the bijection in 44.2.1 puts different columns in different rows. Hence its columns are an orthonormal basis and P†P=PP†=I. Its entries are real, so P†=Pᵀ; this is a coordinate permutation, not a physical SWAP operation.

For a d×d local matrix U and the h×h spectator identity Iₕ, define

$$
E_S(U)=P^\dagger(U\otimes I_h)P.
$$

The Kronecker product convention is explicitly

$$
(U\otimes I_h)_{ah+b,\,ch+t}=U_{ac}\delta_{bt}.
$$

Expand both matrix products at original output x and input y. The summation labels a,c range from 0 to d−1 and b,t from 0 to h−1:

$$
\begin{aligned}
\bigl[E_S(U)\bigr]_{i(x),i(y)}
&=\sum_{a,b,c,t}
 P^*_{ah+b,i(x)}\,U_{ac}\delta_{bt}\,P_{ch+t,i(y)}\\
&=U_{a_S(x),a_S(y)}\delta_{b_T(x),b_T(y)}\\
&=U_{a_S(x),a_S(y)}\prod_{q\notin S}\delta_{x_q,y_q}.
\end{aligned}
$$

The first two permutation factors force a=a_S(x),b=b_T(x),c=a_S(y),t=b_T(y); the remaining identity factor forces equal spectator bits. Equality of their binary indices is equivalent to equality of every spectator bit. This proves the entry formula, including nonadjacent or reversed supports. It says exactly which input coefficients may contribute to each output, without assuming a product input state.

The code constructs this matrix twice for validation: once by P†(U⊗I)P and once by direct row/column bit comparisons. Neither dense matrix is used by the local kernel.

```python
U=o.fourier(2);P=o.permutation(n,S);I=torch.eye(2,dtype=torch.complex128)
e.close(P.mH@P,torch.eye(8,dtype=torch.complex128))
assert P.real.argmax(dim=1).tolist()==[0,2,4,6,1,3,5,7]
E=P.mH@torch.kron(U.contiguous(),I)@P
e.close(E,o.entry_matrix(U,n,S))
print('Permutation-Kronecker embedding equals the independently indexed 8x8 matrix; P maps each basis column to one unique packed coordinate.')
```

```text
Permutation-Kronecker embedding equals the independently indexed 8x8 matrix; P maps each basis column to one unique packed coordinate.
```


### 44.2.3 Expand the contraction and prove the packed kernel

The embedded action is the finite sum \(v'_{i(x)}=\sum_y[E_S(U)]_{i(x),i(y)}v_{i(y)}\). By the entry formula, only inputs whose spectator bits match x survive. Those inputs are exactly ι(c,b_T(x)), one for each c. Therefore

$$
v'_{i(x)}=\sum_{c=0}^{d-1}
 U_{a_S(x),c}\,v_{i(\iota(c,b_T(x)))}.
$$

Equivalently, regard U as a 2k-axis tensor: first k axes are output bits on S and last k axes are input bits on S. Expanding c into bits c₀,…,cₖ₋₁ gives the complete local contraction

$$
v'_{x_0\ldots x_{n-1}}
=\sum_{c_0,\ldots,c_{k-1}=0}^1
 U_{x_{s_0}\ldots x_{s_{k-1}},\,c_0\ldots c_{k-1}}
 v_{y_0\ldots y_{n-1}},\qquad
 y_{s_j}=c_j,\quad y_{t_j}=x_{t_j}.
$$

There is no complex conjugation in this forward action. A transpose or adjoint would define a different local map.

Now reshape v to n binary axes and permute them into S+T. Flatten the first k axes as a and the rest as b. By the bijection, the resulting d×h matrix is \(W_{ab}=v_{i(\iota(a,b))}\). Ordinary matrix multiplication produces

$$
W'_{ab}=(UW)_{ab}=\sum_{c=0}^{d-1}U_{ac}W_{cb}
=\sum_cU_{ac}v_{i(\iota(c,b))}.
$$

Reshape W′ back to binary axes in S+T order, apply the inverse permutation and flatten in q₀-first order. Its coordinate at x is \(W'_{a_S(x),b_T(x)}\), which is precisely the preceding embedded-action sum. Every x has therefore been proved equal, so the complete vectors agree. No normalization, unitarity, sparsity or absence of entanglement was used. This establishes the stated theorem for all complex vectors and square local matrices.

Here is the actual minimal kernel, with its book-side shape/finite-value checks. Its only matrix multiplication is the local d×d matrix times a d×h coefficient array.

```python
def tensor_step(v,U,n,S):
 o.vector(v,n);o.support(n,S);o.matrix(U,len(S))
 order,inverse=o.axes(n,S)
 packed=v.reshape((2,)*n).permute(order).reshape(1<<len(S),1<<(n-len(S)))
 changed=U@packed
 return changed.reshape((2,)*n).permute(inverse).reshape(1<<n)
v=torch.tensor([complex(j-2,2*j%5-1)/9 for j in range(8)],dtype=torch.complex128)
y=tensor_step(v,U,n,S)
e.close(y,E@v);e.close(y,o.scalar(v,U,n,S));e.close(y,o.apply(v,U,n,S))
print('Literal reshape/permute/matmul/inverse kernel matches dense and scalar references on an arbitrary complex vector; no normalization assumed.')
```

```text
Literal reshape/permute/matmul/inverse kernel matches dense and scalar references on an arbitrary complex vector; no normalization assumed.
```


### 44.2.4 Work one ordered gate through the indices

Use the local controlled-X matrix in ordered basis 00,01,10,11:

$$
U_{\rm CX}=\begin{pmatrix}
1&0&0&0\\0&1&0&0\\0&0&0&1\\0&0&1&0
\end{pmatrix}.
$$

Its first support qubit controls the second. For S=(2,0), each fixed spectator bit b=x₁ gives

$$
W_{:,b}=\begin{pmatrix}v_{0b0}\\v_{1b0}\\v_{0b1}\\v_{1b1}\end{pmatrix},\qquad
U_{\rm CX}W_{:,b}=\begin{pmatrix}v_{0b0}\\v_{1b0}\\v_{1b1}\\v_{0b1}\end{pmatrix}.
$$

In particular |001⟩ has local input 10 and spectator zero. The local matrix sends 10 to 11, which restores to |101⟩, global index 5. Sorting the support to (0,2) without changing U instead uses q₀ as control; it leaves |001⟩ unchanged. Both circuits are valid, but they are different gates. This deliberate wrong-support candidate is an indexing counterexample, not an API failure.

```python
CX=torch.tensor([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=torch.complex128)
basis=torch.zeros(8,dtype=torch.complex128);basis[1]=1
r=fq.run(fq.Circuit(3,dtype=torch.complex128).X(2).unitary(2,0,unitary=CX),outputs=fq.probabilities(name='p'),options=e.OPTIONS)
wrong=fq.run(fq.Circuit(3,dtype=torch.complex128).X(2).unitary(0,2,unitary=CX),outputs=fq.probabilities(name='p'),options=e.OPTIONS)
expected=torch.zeros_like(basis);expected[5]=1
e.close(r.statevector()[0],expected);e.close(tensor_step(basis,CX,3,(2,0)),expected)
e.close(wrong.statevector()[0],basis)
print('Actual native ordered CX: |001> -> |101> on (2,0); sorting support to (0,2) leaves |001>. Different gate, not a numerical failure.')
```

```text
Actual native ordered CX: |001> -> |101> on (2,0); sorting support to (0,2) leaves |001>. Different gate, not a numerical failure.
```


### 44.2.5 Compare an independent executor with native evolution

The companion's `execute(v,gates,n)` starts from a copy of v and applies the local kernel for each (support,matrix) pair. The dense oracle independently constructs entries from bit comparisons; the scalar oracle directly gathers input coefficients by overwriting selected input bits. It uses no `reshape`, `permute`, `kron` or dense matrix. Comparing these different address calculations helps expose a common ordering or conjugation error.

For native validation we first prepare a full complex input using RYⱼ(θⱼ), Pⱼ(φⱼ), where θⱼ=0.43+0.17j and φⱼ=−0.31+0.23j in radians. Before any entangling gate its coefficient at x is

$$
v_{i(x)}=\prod_{j=0}^{n-1}
 \begin{cases}\cos(\theta_j/2),&x_j=0,\\
e^{i\phi_j}\sin(\theta_j/2),&x_j=1.\end{cases}
$$

For n>1, CX(0,n−1) then permutes the last bit when x₀=1, which the scalar preparation reference implements by explicit bit replacement. This allows correlated inputs; the local-kernel theorem does not require preparation to factorize.

Let U be the phased Fourier matrix \(U_{ac}=\exp[i(2\pi ac/d+0.19a)]/\sqrt d\). Its columns are orthonormal: the finite geometric sum of exp[2πia(c−c′)/d] is d when c=c′ and zero otherwise, and each row phase cancels with its conjugate in the inner product. For distinct columns, writing z=exp[2πi(c−c′)/d] gives z≠1 and (1−z)Σₐzᵃ=1−zᵈ=0, which proves the zero sum. Set V=diag(exp(−0.37i),exp(0.37i)) on qₙ₋₁. The test chain calls U on S, V on its single-qubit support and then U† on S. Each native custom matrix is checked for unitarity before `Circuit.unitary`; each prefix is independently evaluated classically. Separate native calls test selected shorter prefixes as well as complete chains.

Native statevector-mode output is compared as a complete complex vector, without fitting an overall phase. Density-mode output is compared with the outer product of the independently computed final vector, and both modes' probabilities with its squared moduli.

```python
sv,initial,answer=o.native(3,(2,0))
dm,other,answer2=o.native(3,(2,0),mode='density_matrix')
e.close(initial,other);e.close(answer,answer2)
e.close(sv.statevector()[0],answer)
e.close(dm.measurement('rho').value[0],answer[:,None]*answer.conj()[None,:])
print('Native three-gate chain on a complex correlated preparation agrees with the independent executor in statevector and density-matrix modes.')
```

```text
Native three-gate chain on a complex correlated preparation agrees with the independent executor in statevector and density-matrix modes.
```


### 44.2.6 Prove chronological composition and inverse execution

Let the chronological gate list be (S₁,U₁),…,(Sₘ,Uₘ), and write Eⱼ=Eₛⱼ(Uⱼ). The empty list gives v⁽⁰⁾=v. If after r−1 steps the executor has v⁽ʳ⁻¹⁾=Eᵣ₋₁⋯E₁v, the proved single-step identity gives v⁽ʳ⁾=Eᵣv⁽ʳ⁻¹⁾. Induction establishes

$$
v^{(m)}=E_mE_{m-1}\cdots E_1v.
$$

This is a proof for varying, overlapping supports, not an assumption that the gates commute. In the native tests, a dense accumulator starts at I and is updated as `total=E@total` in chronological order; multiplying on the other side generally reverses the computation.

Because P is unitary,

$$
E_S(U)^\dagger=E_S(U^\dagger),\qquad
E_S(U)^\dagger E_S(U)
=P^\dagger[(U^\dagger U)\otimes I_h]P.
$$

Thus a unitary U gives a unitary embedding. The inverse full product is E₁†⋯Eₘ†, so its **chronological** calls are Uₘ†,…,U₁† with each matrix retaining its own original ordered support. Reversing the original matrices without adjointing them is not this inverse. The companion builds this reversed-adjoint list itself; it does not call a native `adjoint()` method or depend on an unstated native inverse-admission policy. Nonunitary matrices still satisfy the forward theorem but are not assigned an inverse by this argument.

```python
gates=o.chain(3,(2,0));total=torch.eye(8,dtype=torch.complex128)
for T,A in gates:total=o.entry_matrix(A,3,T)@total
e.close(answer,total@initial)
back=o.execute(answer,[(T,A.mH)for T,A in reversed(gates)],3);e.close(back,initial)
wrong_order=o.execute(initial,list(reversed(gates)),3)
assert not torch.allclose(wrong_order,answer,atol=1e-12,rtol=0)
print('Chronological E1,E2,E3 gives E3@E2@E1; reversing adjoints restores the input, while reversing the original calls changes this result.')
```

```text
Chronological E1,E2,E3 gives E3@E2@E1; reversing adjoints restores the input, while reversing the original calls changes this result.
```


### 44.2.7 Preserve the contract at layout and support boundaries

A noncontiguous one-dimensional tensor still has a defined logical coefficient sequence. `permute` changes logical axis placement; `reshape` may copy data when a compatible view is unavailable. Copying does not conjugate amplitudes, and none of these coordinate operations is a physical SWAP. The kernel must restore logical axes even if intermediate arrays have the right flat length. Its output may own new storage; it does not mutate the input.

The algebra also covers empty support: k=0,d=1,U is a 1×1 scalar, and the same calculation multiplies every coefficient by that scalar. For n=0 there is one empty global basis label and the vector has length one. These are book-side linear-algebra boundaries; this native profile uses n≥1 and nonempty supports. Identity and zero maps, zero vectors and an empty gate list need no special normalization repair. A nonunitary map may change the norm; that is not a reason to normalize away its mathematical action or submit it as a deterministic native quantum gate.

Reordering a support requires changing the local matrix as well. If R maps the old selected-coordinate order to the new one, while spectators retain the same order, then P_new=(R⊗I)P_old. Substitution gives

$$
E_{S_{\rm new}}(RUR^\dagger)
=P_{\rm old}^\dagger(U\otimes I)P_{\rm old}.
$$

Indeed the two adjacent R†R pairs cancel after substituting the new permutation and matrix. For a two-qubit reversal, R is the 4×4 basis permutation with row-to-column order (0,2,1,3). Using U unchanged after sorting S lacks these cancellations and generally changes the map, as the controlled-X example showed.

```python
buf=torch.zeros(16,dtype=torch.complex128);buf[::2]=v;before=buf.clone()
e.close(tensor_step(buf[::2],U,3,S),E@v);assert torch.equal(buf,before)
M=torch.tensor([[1,2j],[0,0]],dtype=torch.complex128)
e.close(o.apply(v,M,3,(1,)),o.entry_matrix(M,3,(1,))@v)
e.close(o.apply(torch.tensor([2+3j],dtype=torch.complex128),torch.tensor([[1j]],dtype=torch.complex128),0,()),torch.tensor([-3+2j],dtype=torch.complex128))
assert torch.equal(o.execute(v,[],3),v)
R=torch.eye(4,dtype=torch.complex128)[[0,2,1,3],:]
e.close(o.entry_matrix(R@U@R.mH,3,(0,2)),o.entry_matrix(U,3,(2,0)))
print('Strided input is unchanged; general nonunitary maps remain linear; empty support is scalar multiplication and an empty gate list is identity. No native empty-support gate claimed.')
```

```text
Strided input is unchanged; general nonunitary maps remain linear; empty support is scalar multiplication and an empty gate list is identity. No native empty-support gate claimed.
```


### 44.2.8 State the implementation and cost limits

For fixed spectator b, multiplying d rows by d input coefficients requires d² complex products and d(d−1) additions in an unoptimized dot-product scheme. There are h=N/d spectators, giving Nd products and N(d−1) additions. The local matrix has d² entries; packed input, contracted output and restored flat vector each have N coefficients. Some are views and some may be copies. The working-array scaling of this book kernel is O(N+d²), without a full N×N gate matrix; no allocator, BLAS temporary or process peak is certified by that logical count.

The **validation harness** deliberately does construct N×N dense references and request full density outputs for small systems. Its total memory and wall time must not be advertised as the cost of only the local kernel. Likewise numerical equality with the independent kernel does not establish that FlagQuantum internally uses this exact algorithm. No native kernel replacement, optimizer or speedup is claimed.

The actual released FlagQuantum 0.3.1 APIs used are `Circuit.RY`, `P`, `CX`, `X`, `unitary`, structural `analysis`, `run`, simulator `probabilities` and `density_matrix`, plus the result's statevector accessor in statevector mode. Native tests use CPU complex128, both statevector and density-matrix modes, Python 3.12.14 and Torch 2.13.0. The minimal executor, scalar gather, dense embedding and support checks are book-side PyTorch/Python. The independent executor evolves vectors only; density-mode comparisons validate native outputs for these pure preparations. We do not exercise native arbitrary nonunitary gates, zero-qubit or empty-support gate calls, batch axes, gradients, hardware, noise, distributed execution or mid-circuit measurement. Broader framework capabilities are not inferred from this bounded profile.

Full complex vectors, probabilities and densities use absolute tolerance 10⁻¹² and relative tolerance zero. No phase alignment, probability clipping or input normalization repair is applied. Floating-point agreement is implementation evidence, not symbolic exactness or an interval error certificate. The helper guards kernel n≤8, dense reference n≤5 and native 1≤n≤5 bound this teaching program; they are not FlagQuantum capacity limits.

```python
N=32;d=4;assert (N//d)*d*d==128 and (N//d)*d*(d-1)==96
assert 16*N==512 and 16*d*d==256 and 16*N*N==16384
assert o.invalid_checks()==14 and o.RUNS==2
print('Five-qubit/two-qubit-local model: 128 complex products,96 additions; state512 bytes,local matrix256 bytes,full dense reference16384 bytes.')
print('14 invalid contracts rejected; eight body units use four native calls, two explicit fq.run calls plus two companion calls.')
```

```text
Five-qubit/two-qubit-local model: 128 complex products,96 additions; state512 bytes,local matrix256 bytes,full dense reference16384 bytes.
14 invalid contracts rejected; eight body units use four native calls, two explicit fq.run calls plus two companion calls.
```


The complete [tensor_gate_executor.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/tensor_gate_executor.py) executes 58 native circuits: 48 three-gate chains, four shorter prefixes and six basis-input chains. All nonempty ordered supports through three qubits and four additional ordered supports at four qubits are included, in both tested modes. Forty-eight classical linear-map cases cover all ordered supports including empty through n=3, and both unitary and nonunitary matrices. Strided layouts, zero/identity cases, support reversal, chronological products and inverse lists are checked separately, along with fourteen rejected contracts. The proof covers every finite n; the bounded tests validate code rather than establish that theorem by enumeration.

Run from the repository root:

```bash
python examples/foundations/tensor_gate_executor.py
python scripts/check_tensor_gate_executor_prose.py
```

Expected output of the complete program:

```text
58 native CPU complex128 circuits: 48 three-gate chains, four shorter prefixes and six basis-input chains; both statevector and density-matrix modes.
48 classical linear-map cases include empty/full supports, n=0..3 and nonunitary maps; tensor, scalar gather, entry matrix and permutation-Kronecker references agree.
Chronological products and reversed adjoints agree; complex correlated inputs, nonadjacent/reversed supports, zero/identity and strided layouts passed.
14 malformed/native-boundary contracts rejected; no sorting, conjugating, clipping or normalization repair in the local kernel.
Book kernel forms no full-register operator; dense validation and native full-density requests are separate small-system diagnostics, not a memory benchmark.
```

**Check your understanding.** Why does the spectator delta remove a sum rather than set the spectator bits to zero? Which axes of the local tensor are summed? Why is the inverse axis order necessary even when the output already has N entries? Why does the forward theorem allow a nonunitary matrix while a deterministic gate call has an additional contract?

**Problems and transfer.**

- **44.2-A — reconstruct the labels.** For n=4,S=(3,1), find T, the packed row/column for x=1101, and the original output index when the local output bits are 01 with spectators unchanged. Which entry of U multiplies the input basis coefficient into that output?
- **44.2-B — retain complex coherence.** Apply the controlled-X matrix on S=(2,0) to (|001⟩+i|110⟩)/√2, then repeat with the incorrectly sorted support. Write both complete output vectors. Can a global-phase adjustment repair the difference?
- **44.2-C — fresh executor.** On the stated five-qubit complex preparation, test supports (4,1),(1,4),(3,0,4). Replace U by diag(exp(0.11ia))U and use RX(−0.58) on q₂ between it and its adjoint. Compare both modes with all independent references. Also test the original Fourier prefix alone on full reversed support (4,3,2,1,0), both modes. Check a fresh arbitrary nonunitary map classically, not as a native gate.
- **44.2-D — repair an ordering bug.** A kernel sorts S, uses Uᵀ, or skips inverse-axis restoration because the flat output has the expected length. Explain each change mathematically and construct a case that detects it. Give the correct matrix conversion when replacing (2,0) by (0,2) while preserving the same physical map.

<details markdown="1">
<summary>Answers and verification guidance for 44.2-A–D</summary>

**A.** T=(0,2). The selected bits are (1,1), so a=3; the spectators are (1,0), so b=2. The packed flat index is 3·4+2=14, while the original input index is 13. With local output 01, the restored string is 1100, index 12. Its coefficient receives \(U_{1,3}\) times the input basis amplitude; spectators were retained, not reset.

**B.** The correct result is \((|101\rangle+i|110\rangle)/\sqrt2\). The incorrectly sorted gate gives \((|001\rangle+i|111\rangle)/\sqrt2\). Their nonzero coordinates are disjoint, so multiplying by an overall phase cannot turn one into the other. The transfer artifact checks the explicit coefficients classically; finite checks do not replace the preceding linear proof.

**C.** There are eight fresh native calls: three changed chains in both modes and two full reversed-support prefixes. Row multiplication by unit phases preserves column orthonormality, so the changed U is admissible; RX(−0.58) is unitary. Dense bit-entry, permutation-Kronecker, scalar gather and local kernel agree on the complete complex vector; both native modes agree on full probabilities/densities. The arbitrary nonunitary reference is retained without normalization. No global-phase fit is used.

**D.** Sorting changes the selected-coordinate interpretation unless U changes covariantly. Transposition exchanges local input/output roles without implementing the original matrix action. Omitting restoration leaves an S+T-ordered coefficient sequence that is mislabeled as q₀-first. A nonsymmetric complex U and a nontrivial spectator distinguish these errors. For the two-qubit reversal use R with row-to-column order (0,2,1,3), and replace U by \(RUR^\dagger\) on (0,2). For general U, neither merely keeping it unchanged nor merely transposing it supplies that conversion.

</details>

**Sources and review status.** The frozen NC §2.1.7 tensor-product locator, beginning at printed page 71, was checked against the [publisher's contents](https://assets.cambridge.org/97811070/02173/toc/9781107002173_toc.pdf); this is not a claim of full textbook access. The [QuEST v1 representation discussion](https://arxiv.org/pdf/1802.08032v1#page=2) was consulted narrowly for dense statevector representation and the distinction between array payload and execution overhead; its PDF hash is recorded without uploading the paper. All indexing, embedding, contraction and chronological proofs needed here are supplied locally. No uninspected historical performance or hardware claim is imported. The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/44.2.json) keeps author validation separate from independent mathematical/implementation review, reader trial and formal acceptance. This remains a working draft. Continue, when drafted, with [44.3 Observables and measurement execution](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-3).

<!-- end-section-44.2 -->
