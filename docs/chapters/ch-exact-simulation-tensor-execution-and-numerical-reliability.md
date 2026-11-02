# 44. Exact Simulation, Tensor Execution, and Numerical Reliability

**Working drafts: sections 44.1–44.3 and 44.6 · Writing Baseline 1.0 · November 2, 2026.** The B03 execution bridge is drafted here before the algorithm laboratories. The global chapter number and Volume VII placement remain unchanged. Author validation is separate from independent mathematical/implementation review and reader trial, which remain pending.

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

**Sources and review status.** The frozen NC §2.1.7 tensor-product locator, beginning at printed page 71, was checked against the [publisher's contents](https://assets.cambridge.org/97811070/02173/toc/9781107002173_toc.pdf); this is not a claim of full textbook access. The [QuEST v1 representation discussion](https://arxiv.org/pdf/1802.08032v1#page=2) was consulted narrowly for dense statevector representation and the distinction between array payload and execution overhead; its PDF hash is recorded without uploading the paper. All indexing, embedding, contraction and chronological proofs needed here are supplied locally. No uninspected historical performance or hardware claim is imported. The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/44.2.json) keeps author validation separate from independent mathematical/implementation review, reader trial and formal acceptance. This remains a working draft. Continue with [44.3 Observables and measurement execution](../section-plans/06-simulation.md#sec-exact-simulation-tensor-execution-and-numerical-reliability-3).

<!-- end-section-44.2 -->

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-3"></span>
## 44.3 Observables and measurement execution

**Question.** Which calculations connect a simulated state to exact expectations, marginal probabilities, conditional branches and a finite record of measurement outcomes?

The prerequisites are [44.2, local tensor execution](#sec-exact-simulation-tensor-execution-and-numerical-reliability-2), [6.2, conditional states](ch-measurement-expectation-values-and-statistical-estimation.md#sec-measurement-expectation-values-and-statistical-estimation-2) and [6.3, observables and expectations](ch-measurement-expectation-values-and-statistical-estimation.md#sec-measurement-expectation-values-and-statistical-estimation-3). This F-depth section derives the corresponding kernels and their requested-output costs. Assume a normalized pure simulated state and declared ideal projective readout semantics. Exact algebra, floating-point deterministic calculations and random records have separate meanings; no physical measurement-update endpoint or hardware IID certificate follows from a simulator result.

### 44.3.1 Freeze a state, observable and record contract

Let v be a normalized complex vector on n qubits, N=2ⁿ, with the q₀-first index convention from 44.2. All scores and angles here are dimensionless, with angles in radians. Our three-qubit preparation applies RY₀(π/2), P₀(π/2), RY₁(π/3), P₁(π/2), followed by CX(0,2) and CX(1,2). The target q₂ begins at zero, so its final bit is x₀ XOR x₁. Multiplying the two prepared qubit coefficients and retaining their phases gives

$$
|\psi\rangle=\sqrt{\tfrac38}|000\rangle
+i\sqrt{\tfrac18}|011\rangle
+i\sqrt{\tfrac38}|101\rangle
-\sqrt{\tfrac18}|110\rangle.
$$

The squared moduli sum to 3/8+1/8+3/8+1/8=1. Choose R=Y₀X₂ and the real Pauli sum \(\mathcal H=0.7R-0.2Z_0+0.4Z_1\). The Y action is Y|0⟩=i|1⟩, Y|1⟩=−i|0⟩. Applying R pairs 000 with 101 and 011 with 110 with precisely the phases already present, so Rψ=ψ and ⟨R⟩=1. The q₀ probabilities are 1/2,1/2, giving ⟨Z₀⟩=0; the q₁ probabilities are 3/4,1/4, giving ⟨Z₁⟩=1/2. Hence ⟨𝓗⟩=9/10.

One native call requests exact simulator expectations and probabilities together with a **single joint** terminal record in ordered columns Q=(q₂,q₀). A finite record is not the exact expectation tensor. For a Pauli sum, use `result.expectation(name)` to retrieve the coefficient-weighted logical aggregate. Its internal term results may share the requested name, so `result.measurement(name)` can be ambiguous for that sum. The initial raw-term selector failure and a rename-only attempt are retained; changing the name alone did not replace the required aggregation accessor. No native numerical defect is inferred from those two API-selection failures.

```python
import math,torch,flagquantum as fq
from dataclasses import replace
from fractions import Fraction as F
from examples.foundations import measurement_execution as m
angles=(math.pi/2,math.pi/2,math.pi/3,math.pi/2);Q=(2,0)
c=fq.Circuit(3,dtype=m.D).RY(0,theta=angles[0]).P(0,theta=angles[1]).RY(1,theta=angles[2]).P(1,theta=angles[3]).CX(0,2).CX(1,2)
R=fq.Y(0)@fq.X(2);observable=.7*R-.2*fq.Z(0)+.4*fq.Z(1)
r=fq.run(c,outputs=[fq.probabilities(qubits=Q,name='p'),fq.expectation(R,name='r_mean'),fq.expectation(observable,name='hamiltonian_mean'),fq.samples(qubits=Q,name='raw')],shots=17,options=replace(m.e.OPTIONS,mode='statevector',seed=101))
v=torch.zeros(8,dtype=m.D);v[0]=math.sqrt(3/8);v[3]=1j*math.sqrt(1/8);v[5]=1j*math.sqrt(3/8);v[6]=-math.sqrt(1/8)
m.e.close(r.statevector()[0],v)
m.e.close(r.expectation('r_mean')[0],torch.tensor(1.,dtype=torch.float64))
m.e.close(r.expectation('hamiltonian_mean')[0],torch.tensor(.9,dtype=torch.float64))
assert r.measurement('raw').value.shape==(1,17,2)
print('Actual native parity preparation: R=Y0X2 has mean1; the weighted Pauli sum has mean9/10; aggregate retrieved with result.expectation(name).')
```

```text
Actual native parity preparation: R=Y0X2 has mean1; the weighted Pauli sum has mean9/10; aggregate retrieved with result.expectation(name).
```


### 44.3.2 Contract an observable without forming a global matrix

Let A be a d×d Hermitian matrix on ordered support Q of k qubits, d=2ᵏ, and h=N/d spectators. Hermitian means \(A_{ca}^*=A_{ac}\). Gather v as the d×h coefficient matrix W from 44.2. Substitute that section's embedded action into the quadratic form from 6.3:

$$
\begin{aligned}
\mu_A&=\langle\psi|E_Q(A)|\psi\rangle
=\sum_{b=0}^{h-1}\sum_{a,c=0}^{d-1}W_{ab}^*A_{ac}W_{cb}\\
&=\sum_b W_{:,b}^\dagger A W_{:,b}.
\end{aligned}
$$

The spectator identity removes cross terms with different spectator labels; it does not require the state to factorize. Conjugating the scalar and exchanging a,c uses Hermiticity to give \(\mu_A^*=\mu_A\), so the exact result is real. The implementation applies A locally and takes one inner product, or contracts each packed column, rather than materializing \(E_Q(A)\). In the example Q=(2,0), the local matrix for Y₀X₂ is X⊗Y because q₂ is the first local axis.

A Pauli word offers another independent kernel. For P=P₀⊗⋯⊗Pₙ₋₁, let f have bit one at X or Y positions, let \(n_Y\) count the Y factors, and define

$$
P|x\rangle=\gamma_P(x)|x\mathbin\oplus f\rangle,\qquad
\gamma_P(x)=i^{n_Y}(-1)^{\sum_{j:P_j\in\{Y,Z\}}x_j}.
$$

This follows by multiplying the single-qubit actions of I,X,Y,Z. Consequently

$$
\mu_P=\sum_x v_{i(x\oplus f)}^*\gamma_P(x)v_{i(x)}.
$$

The scalar reference compiles the flip/sign masks once, then gathers each paired coefficient with its phase. It preserves the Y sign and the conjugate; replacing amplitudes by probabilities would lose this interference information. Separate dense-Kronecker checks cover all 84 Pauli words on one through three qubits, including multiple Y factors. Real linearity gives ⟨ΣⱼcⱼPⱼ⟩=Σⱼcⱼ⟨Pⱼ⟩. This exact state contraction does not assume that noncommuting terms have simultaneous measurement outcomes.

```python
A=torch.kron(m.X,m.Y);W=m.t.pack(v,3,(2,0))
mu=sum(torch.vdot(W[:,j],A@W[:,j])for j in range(W.shape[1]))
m.e.close(mu,m.expectation(v,A,3,(2,0)))
m.e.close(mu,torch.vdot(v,m.t.entry_matrix(A,3,(2,0))@v))
assert abs(m.pauli(v,3,'YIX')-1)<1e-12
assert abs(.7*m.pauli(v,3,'YIX')-.2*m.pauli(v,3,'ZII')+.4*m.pauli(v,3,'IZI')-.9)<1e-12
print('Packed local contraction, dense quadratic form, Pauli flip/phase kernel and native aggregate agree; conjugation and Y signs retained.')
```

```text
Packed local contraction, dense quadratic form, Pauli flip/phase kernel and native aggregate agree; conjugation and Y signs retained.
```


### 44.3.3 Sum probabilities over spectator coordinates

Adopt computational-basis Born probabilities |vᵢ₍ₓ₎|². For ordered selected qubits Q=(a₀,…,aₘ₋₁), let y encode their bits in that order. Outcomes on unselected qubits are mutually exclusive, so

$$
p_Q(y)=\sum_{x:\,x_{a_j}=y_j\ \forall j}|v_{i(x)}|^2
=\sum_{b=0}^{2^{n-m}-1}|W_{yb}|^2.
$$

Every full basis string belongs to exactly one selected label, proving nonnegativity and \(\sum_y p_Q(y)=\sum_x|v_{i(x)}|^2=1\). The output is 2ᵐ real numbers; it is not a smaller statevector. Summing complex amplitudes over spectators and then taking a squared modulus would add interference between distinguishable spectator outcomes and compute a different object.

For Q=(2,0), the four nonzero strings in 44.3.1 produce labels 00,10,11,01, respectively, giving \(p_Q=(3,1,1,3)/8\). Ordered full readout Q=(0,2,1) instead places the weights at indices 0,3,6,5. This checks the output-label map even when a particular two-bit marginal happens to be symmetric under swapping its two columns.

```python
def marginal(v,n,Q):
 m.state(v,n);W=m.t.pack(v,n,Q);sq=W.abs().square()
 if bool(((W!=0)&(sq==0)).any()):raise FloatingPointError('Positive squared contribution underflow')
 return sq.sum(1)
p=marginal(v,3,Q);m.e.close(p,torch.tensor([3/8,1/8,1/8,3/8],dtype=torch.float64))
m.e.close(p,r.measurement('p').value[0])
ordered=marginal(v,3,(0,2,1))
assert abs(ordered[5].item()-1/8)<1e-12 and abs(ordered[6].item()-3/8)<1e-12
print('Ordered (q2,q0) marginal=(3,1,1,3)/8; full permuted mask(q0,q2,q1) places probabilities1/8 and3/8 at indices5 and6.')
```

```text
Ordered (q2,q0) marginal=(3,1,1,3)/8; full permuted mask(q0,q2,q1) places probabilities1/8 and3/8 at indices5 and6.
```


### 44.3.4 Derive prefix conditionals and branch states

For a prefix z=(z₀,…,zₗ₋₁) of the ordered Q record, let \(C_z\) contain full strings matching those first ℓ selected bits, and define the prefix projector \(\Pi_z\) as the diagonal mask of \(C_z\). Its weight is

$$
w(z)=\|\Pi_zv\|^2=\sum_{x\in C_z}|v_{i(x)}|^2.
$$

The empty prefix has weight one. Its two child events partition \(C_z\), so w(z)=w(z0)+w(z1). If w(z)>0, the ideal conditional state from 6.2 is \(v^{(z)}=\Pi_zv/\sqrt{w(z)}\). For the next bit b, the child projector satisfies \(\Pi_{zb}\Pi_z=\Pi_{zb}\). Therefore

$$
\Pr(b\mid z)=\|\Pi_{zb}v^{(z)}\|^2
=\frac{w(zb)}{w(z)}.
$$

The quotient is nonnegative and its two values sum to one. Multiplying these conditional probabilities along a positive path telescopes:

$$
\prod_{\ell=0}^{m-1}
\frac{w(y_0\ldots y_\ell)}{w(y_0\ldots y_{\ell-1})}
=\frac{w(y)}{w(\varnothing)}=p_Q(y).
$$

A zero-weight prefix has no conditional state or conditional next-bit law; a sampler must never enter it. It must not invent equal probabilities there. In the worked example the first selected bit q₂ is fair, but q₀ conditioned on q₂=0 has law (3/4,1/4), while conditioned on q₂=1 it has (1/4,3/4). Multiplying two unconditional fair marginals would incorrectly give the uniform two-bit law. An exact Bell-law fixture (1/2,0,0,1/2) makes this error sharper: independent fair bits would create impossible 01 and 10 records.

The branch helper returns `None` for an exactly absent event and retains the phase of each positive branch. It checks all prefix nodes against separately constructed diagonal projector matrices and scalar masks. These are classical reference calculations on the pre-readout simulated state. Native terminal records do not establish that a collapse was applied to the returned state, nor do these helpers implement a native mid-circuit measurement endpoint. Marginalizing a prefix of this fixed commuting readout gives \(p(y_{\rm rest})=\sum_{z:w(z)>0}w(z)p(y_{\rm rest}\mid z)\). This does not assert that a physical measurement left the original state unchanged. After an actual earlier measurement, a later observable B has ignored-record prediction \(\sum_{z:w(z)>0}w(z)\langle v^{(z)}|B|v^{(z)}\rangle\), which can differ from its original-state expectation; it is not an average of normalized branch vectors. The [zero-native-call check](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-evidence/44.3/ignored-prefix-check.py) includes the 6.2 example of Z readout on a plus state followed by X.

```python
p0,c0=m.branch(v,3,Q,(0,));p1,c1=m.branch(v,3,Q,(1,))
assert abs(p0-.5)<1e-12 and abs(p1-.5)<1e-12
m.e.close(m.probabilities(c0,3,(0,)),torch.tensor([.75,.25],dtype=torch.float64))
m.e.close(m.probabilities(c1,3,(0,)),torch.tensor([.25,.75],dtype=torch.float64))
assert m.check_prefixes(v,3,(0,2,1))==15
zero,absent=m.branch(v,3,(0,2,1),(0,0,1));assert zero==0 and absent is None
weight,phase=m.branch(v,3,(0,2,1),(1,1,0));target=torch.zeros(8,dtype=m.D);target[5]=1j;m.e.close(phase,target)
print('Every full-mask prefix checked: 15 nodes; q0 conditional laws are(3/4,1/4)/(1/4,3/4), not its unconditional(1/2,1/2).')
print('Impossible branch has no conditional vector; the selected positive branch retains its i phase. These are classical reference updates.')
```

```text
Every full-mask prefix checked: 15 nodes; q0 conditional laws are(3/4,1/4)/(1/4,3/4), not its unconditional(1/2,1/2).
Impossible branch has no conditional vector; the selected positive branch retains its i phase. These are classical reference updates.
```


### 44.3.5 Prove CDF and cached-prefix sampling

Let p₀,…,p_K₋₁ be the selected joint law in binary label order, K=2ᵐ. Define \(F_{-1}=0\) and \(F_j=\sum_{i=0}^jp_i\). Given an ideal uniform u in [0,1), return the first j with Fⱼ>u. Outcome j occupies the half-open interval [Fⱼ₋₁,Fⱼ), whose length is pⱼ. These intervals are disjoint and cover [0,1), proving the sampled law. Zero probabilities have empty intervals and must be skipped; using the wrong inequality at an exact endpoint can select such a leaf in a finite implementation.

The executable reference specializes to **declared exact rational laws**. Choose a common denominator D with integer masses aⱼ=Dpⱼ summing to D. A uniform integer rank r∈{0,…,D−1} is assigned to the first cumulative integer mass strictly greater than r. Exactly aⱼ ranks select j, proving the rational law without a statistical frequency test. The reference does not silently convert native floating probabilities into a certified exact rational law.

Cache a binary tree of masses, with the two children extending a prefix by 0 or 1. At a node of mass M, let its left mass be M₀. A uniform residual rank r in {0,…,M−1} goes left if r<M₀; otherwise it goes right after subtracting M₀. The branch probabilities are M₀/M and (M−M₀)/M. Conditioned on either positive branch, translating the chosen interval makes its residual rank uniform on that child's range. Induction gives each leaf mass divided by D, the same joint law as the CDF. Zero-mass children have no ranks and are never chosen. This proof also explains the real-weight tree through the prefix ratios from 44.3.4.

For the worked law the integer masses are (3,1,1,3), cumulative boundaries (3,4,5,8), and the eight ranks select labels (0,0,0,1,2,3,3,3). The tests enumerate every rank, not merely a pseudorandom sample. Python `randrange(D)` supplies reference ranks under its pseudorandom contract; seed replay is reproducibility, not independent statistical evidence or a hardware randomness certificate. No equality between its stream and FlagQuantum's native stream is requested.

```python
ps=(F(3,8),F(1,8),F(1,8),F(3,8));s=m.Sampler(ps)
def prefix_at(s,rank):
 node=1
 while node<s.K:
  left=s.mass[2*node]
  if rank<left:node*=2
  else:rank-=left;node=2*node+1
 return node-s.K
assert s.cdf==[3,4,5,8] and [prefix_at(s,k)for k in range(8)]==[0,0,0,1,2,3,3,3]
assert m.exact_sampler_check(ps)==8
zeros=m.Sampler((F(0),F(1,4),F(0),F(3,4)));assert zeros.at(0)==1 and zeros.at(1)==3
assert s.draw(17,seed=31)==s.draw(17,seed=31,method='cdf')
assert m.Sampler((F(1,2),F(0),F(0),F(1,2))).conditional((0,))==(F(1),F(0))
print('Integer CDF/prefix samplers assign ranks0..7 to labels[0,0,0,1,2,3,3,3]; zero-width intervals skipped at exact boundaries.')
print('Seed replay shares ranks and is not independent evidence; native random streams are not compared with these reference streams.')
```

```text
Integer CDF/prefix samplers assign ranks0..7 to labels[0,0,0,1,2,3,3,3]; zero-width intervals skipped at exact boundaries.
Seed replay shares ranks and is not independent evidence; native random streams are not compared with these reference streams.
```


### 44.3.6 Execute a declared measurement basis

For a fixed unitary analyzer V followed by computational readout, the event probabilities are \(\|\Pi_yVv\|^2=v^\dagger V^\dagger\Pi_yVv\). Thus the original-state effects are V†Π_yV. This is a change of measurement context, not permission to sample an arbitrary observable from the unrotated computational record.

To read R=Y₀X₂, call P₀(−π/2), H₀ and H₂. With S=diag(1,i), the analyzer is V=(HS†)₀H₂. Using HZH=X and SXS†=Y gives

$$
V^\dagger(Z_0Z_2)V
=(SHZHS^\dagger)_0(HZH)_2=Y_0X_2.
$$

For recorded bits (b₂,b₀), the eigenvalue score is (−1)ᵇ⁰⁺ᵇ², computed as 1−2(b₂ XOR b₀). In the worked state, Y₀ alone or X₂ alone flips one parity-constrained bit and maps its support outside the original four strings, so both local expectations vanish; the product expectation is one. The commuting computational projectors (I+(−1)ᵇZ)/2 then give the following law, writing a=b₂ and b=b₀:

$$
p_{ab}=\tfrac14\left[1+(-1)^a\langle Z_2\rangle_{Vv}
+(-1)^b\langle Z_0\rangle_{Vv}
+(-1)^{a+b}\langle Z_2Z_0\rangle_{Vv}\right].
$$

Substituting (0,0,1) for these three means yields (1/2,0,0,1/2). The code checks the native rotated probability and exact ZZ expectation against these formulas, while computing a finite sample score separately. Floating arithmetic can leave tiny positive residues in ideally zero cells; no finite-record accuracy hit is demanded as a deterministic pass condition.

The sum 𝓗 also contains Z₀, which does not commute with R. Its native exact expectation query is a sum of state contractions. Estimating that sum from a physical record would require a declared measurement scheme and appropriate contexts or a measurement of its spectral observable; the Y/X record alone is not an estimator of every term. No such hardware measurement protocol is implied here.

```python
for mode in ('statevector','density_matrix'):
 analyzer,_=m.preparation(3,angles);analyzer.P(0,theta=-math.pi/2).H(0).H(2)
 read=fq.run(analyzer,outputs=[fq.probabilities(qubits=Q,name='p'),fq.expectation(fq.Z(0)@fq.Z(2),name='zz_mean'),fq.samples(qubits=Q,name='raw'),fq.density_matrix(name='rho')],shots=17,options=replace(m.e.OPTIONS,mode=mode,seed=103))
 B0=m.H@torch.diag(torch.tensor([1,-1j],dtype=m.D));w=m.t.apply(m.t.apply(v,B0,3,(0,)),m.H,3,(2,))
 m.e.close(read.measurement('p').value[0],marginal(w,3,Q));m.e.close(read.measurement('p').value[0],torch.tensor([.5,0.,0.,.5],dtype=torch.float64))
 m.e.close(read.expectation('zz_mean')[0],torch.tensor(1.,dtype=torch.float64))
 m.e.close(read.measurement('rho').value[0],w[:,None]*w.conj()[None,:])
 rows=read.measurement('raw').value[0].tolist();scores=[1-2*(row[0]^row[1])for row in rows];assert all(x in(-1,1)for x in scores)
print('Actual P(-pi/2),H on q0 and H on q2 implement Y0/X2 readout; both modes match the rotated probability law and exact ZZ mean.')
print('The finite raw score is computed separately; no required frequency hit and no returned-state collapse inferred.')
```

```text
Actual P(-pi/2),H on q0 and H on q2 implement Y0/X2 readout; both modes match the rotated probability law and exact ZZ mean.
The finite raw score is computed separately; no required frequency hit and no returned-state collapse inferred.
```


### 44.3.7 Charge setup, contraction and record output separately

For a local dense A on k qubits, d=2ᵏ, the 44.2 apply-plus-inner-product scheme uses Nd+N complex products and N(d−1)+(N−1)=Nd−1 additions in the stated unoptimized arithmetic model. It stores the N-coefficient state and d² local matrix, plus working arrays. A generic full dense observable has d=N; its small scalar output does not make its contraction constant-cost.

A Pauli word uses a coefficient permutation and phases in {1,−1,i,−i}. After O(n) mask preparation, the implemented loop visits N coefficients; O(N) fixed-word index operations per term assume the indices fit that word model. Arbitrary-size integer operations carry their own bit cost. L Pauli terms therefore admit O(LN) contractions in that declared fixed-word model, without a full N×N observable. This describes the reference scheme, not measured native operation counts or hardware time.

For selected m-bit probabilities, packing and scanning N coefficients computes 2ᵐ outputs with N magnitude-squared contributions and N−2ᵐ within-row additions. The selected table needs 2ᵐ real slots; packed arrays may be views or copies. Building a CDF or a prefix tree from that table costs O(K), K=2ᵐ, in the unit arithmetic model. A complete binary tree has 2K−1 mass nodes. CDF binary search or cached tree descent uses O(log K)=O(m) comparisons per rank, giving O(K+Sm) reference sampling work after probabilities are available. The exact-rational implementation additionally performs denominator and integer-mass arithmetic; those bit costs and pseudorandom-rank generation are not free.

Recomputing every conditional probability by scanning a full state for each bit and shot instead costs O(SmN) in a direct scheme. The cached terminal table avoids that work because the state, analyzer and record context are fixed. An adaptive basis change or a different later measurement generally needs a new conditional calculation; the cached table is not a universal instrument simulator.

A packed S×m record contains Sm bits; this native int64 tensor occupies 8Sm bytes, before headers/serialization. The exact-mean scalar, probability table and raw record are distinct outputs. One native `run(...,shots=S)` invocation is not evidence that its CPU simulator evolved S separate states. Physical repeated preparations and simulator sampling costs must be specified independently. The validation harness deliberately builds dense prefix projectors and full density outputs for small systems; its memory is not advertised as the efficient kernel's working memory.

```python
N=8;d=4;K=4;shots=17
assert N*d+N==40 and 8*K==32 and shots*2==34 and 8*shots*2==272
assert len(s.mass)-1==2*K-1==7
assert m.invalid_checks()==15 and m.RUNS==0
print('Declared local matvec-plus-inner-product scheme:40 complex products; selected table32 bytes; 17 two-bit records34 logical bits/272 int64 bytes.')
print('Seven cached tree nodes; 15 invalid contracts rejected, rare positive branch preserved, squared-norm underflow reported explicitly.')
```

```text
Declared local matvec-plus-inner-product scheme:40 complex products; selected table32 bytes; 17 two-bit records34 logical bits/272 int64 bytes.
Seven cached tree nodes; 15 invalid contracts rejected, rare positive branch preserved, squared-norm underflow reported explicitly.
```


### 44.3.8 Keep numerical and API boundaries reviewable

This profile actually executes released FlagQuantum 0.3.1 `Circuit.RY/P/CX/H`, `run`, `probabilities`, `expectation`, `samples` and `density_matrix`, plus the statevector accessor in statevector mode and the logical `result.expectation(name)` aggregator. Native Observable `@` is used only for disjoint-qubit Pauli products and real scalars form sums. The exact-rational sampler, local contractions, masks, branch states and prefix checks are book-side Python/PyTorch. The returned simulator state/density is compared with the pre-readout state, rather than described as a selected collapsed branch. A separate X-only basis calibration checks the ordered sample labels exactly, including asymmetric bit patterns in both modes. This is a CPU software convention check, not physical detector calibration; it supplements the generic records' schema checks.

Native tests use Python 3.12.14, Torch 2.13.0, CPU complex128, statevector and density-matrix modes, absolute tolerance 10⁻¹² and relative tolerance zero. “Exact” deterministic outputs refer to full-state formulas without an intentional stochastic/truncation approximation; roundoff remains and the tolerance is not an interval certificate. The code does not clip probabilities, repair input normalization, symmetrize a non-Hermitian observable or fit global phase. A required conditional-state normalization is the stated Lüders formula, not an input repair.

Zero probability is not defined by a tolerance cutoff. A positive 10⁻²⁰ branch is retained with its phase. If a nonzero amplitude's square, or a nonzero projected branch's squared norm, underflows to zero, the reference raises explicitly instead of labeling the event impossible. Conditioning very small branches can amplify numerical error; full-state agreement does not certify uniformly accurate conditional directions on every rare branch. All prefix-reference comparisons here start from the same declared pre-readout simulated vector and test different projection/address calculations.

We do not exercise a native collapse/reset API, general instrument composition, hardware calibration, adaptive measurement backend or an IID diagnostic. These restrictions describe this experiment, not a denial of broader framework capabilities. Guards n≤5 for these reference states, n=3…5 for the native preparation family, K≤32 outcomes, 128-bit common integer mass and D≤4096 for exhaustive rank checks bound the teaching program. They are not FlagQuantum capacity limits.

```python
checked,reference,permuted=m.native(3,(0,2,1),angles,mode='density_matrix',shots=17)
m.e.close(permuted,ordered);assert m.RUNS==1
cal=m.calibrate(3,(2,0),(1,0,0));assert cal.measurement('raw').value[0].tolist()==[[0,1]]*5
assert m.RUNS==2
assert r.measurement('raw').value[0].numel()==34
print('Native full ordered-mask and deterministic X-only label checks agree; body total is five fq.run calls: three explicit calls plus two companion calls.')
print('Exact expectation, conditional reference states and terminal samples remain distinct outputs; hardware,reset and IID certification are outside this profile.')
```

```text
Native full ordered-mask and deterministic X-only label checks agree; body total is five fq.run calls: three explicit calls plus two companion calls.
Exact expectation, conditional reference states and terminal samples remain distinct outputs; hardware,reset and IID certification are outside this profile.
```


The complete [measurement_execution.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/measurement_execution.py) runs 48 native calls: three- and four-qubit preparations, three angle choices including deterministic computational inputs, two ordered masks, both execution modes and two analyzer contexts. Every prefix node, including zero-weight branches, is checked against dense diagonal projectors and scalar masks. Five exact rational laws cover 27 exhaustive integer ranks; fifteen invalid contracts and both squared-norm underflow routes are checked. The [evidence record](https://github.com/FlagQuantum/modern-quantum-computing/tree/main/book/section-evidence/44.3) also retains the two initial one-call selector failures, the corrected run, the 84 independent Pauli-word checks, twelve separate deterministic basis-label calibration calls and fresh five-qubit validation. Their runs are recorded separately, without turning repeated seeds or author checks into independent review.

Run from the repository root:

```bash
python examples/foundations/measurement_execution.py
python scripts/check_measurement_execution_prose.py
```

Expected output of the complete program:

```text
48 native CPU complex128 circuits: three- and four-qubit preparations,two ordered masks,both execution modes and computational/Y-X analyzer profiles.
Exact Pauli/local contractions,marginals and every prefix branch agree with scalar/dense references; native terminal samples checked for schema,not frequency hits.
Five exact rational laws,27 integer ranks: CDF and cached-prefix samplers reproduce every outcome mass,including zero leaves and boundary ranks.
15 malformed contracts rejected; positive1e-20 branch retained and two squared-norm underflow routes explicitly rejected.
Book conditional states and exact-rational samplers are separate from native terminal requests; no collapse/reset,hardware IID certificate or shared random-stream claim.
```

**Check your understanding.** Which outputs are deterministic state calculations, and which are random records? Why does multiplying unconditional qubit probabilities fail on correlated data? What is undefined at a zero-weight prefix? Why does an exact Pauli-sum expectation not specify a single physical measurement context?

**Problems and transfer.**

- **44.3-A — prefix law.** Derive every weight in the two-bit prefix tree for (3,1,1,3)/8 and list the eight integer ranks' labels. For the Bell law (1/2,0,0,1/2), derive the conditional next-bit laws and identify the false outcomes generated by two independent fair bits.
- **44.3-B — rare versus absent.** For v=(1,i·10⁻¹⁰), interpreted under the stated floating normalization contract, compute the positive second-branch weight and normalized phase. Contrast amplitude i·10⁻²⁰⁰. For exact rational law (1−10⁻²⁰,10⁻²⁰), show how its last integer rank selects the rare event without enumerating 10²⁰ ranks. Does zero observed count prove that event impossible?
- **44.3-C — fresh execution.** Use the five-qubit preparation with angles (−0.83,0.41,0.67,−0.49), masks (4,2,0), (0,3), (2,1,4,0), both modes and analyzer profiles, S=23. Compare all prefixes and exact observables against scalar/matrix references. Separately validate new rational laws (1,2,3,4,5,6,7,8)/36 and (0,1,0,2,0,0,1,0)/4 by every integer rank. Retain actual records without requiring an empirical mean hit.
- **44.3-D — repair execution claims.** Diagnose a report that reads a multi-term Pauli aggregate through a raw measurement selector, multiplies unconditional marginals, drops every p<10⁻¹² branch, and says its two same-seed samplers are independent hardware evidence. State the requested-output cost when N=8,d=4,m=2,S=17, and identify what remains outside those arithmetic/payload counts.

<details markdown="1">
<summary>Answers and verification guidance for 44.3-A–D</summary>

**A.** Root mass is 8; its children have masses 4 and 4. The four leaves have masses 3,1,1,3, so conditional second-bit laws are (3/4,1/4) and (1/4,3/4). The rank labels are 0,0,0,1,2,3,3,3. For the Bell law the conditionals are (1,0) and (0,1). Independent fair draws incorrectly assign probability 1/4 to each impossible label 01 and 10.

**B.** The positive branch has squared norm approximately 10⁻²⁰ and its normalized vector is (0,i), including the retained phase. The second amplitude in the contrast is nonzero but its square underflows in the tested dtype; the reference reports the numerical failure. It does not define a zero-probability physical event. The rational law has D=10²⁰; rank D−1 selects its one-rank rare interval and D−2 selects the common outcome. This reference integer fits the declared mass guard, but exhaustive validation deliberately rejects such a huge rank sweep. A finite zero count is not a zero-probability proof.

**C.** Twelve fresh native calls cover three masks, two modes and two analyzers. The two new rational fixtures require 36 and 4 ranks respectively. Their prefix and CDF assignments agree exactly, including empty intervals. The five-qubit native probability/expectation/density references and all prefix projections agree within the stated tolerance. Bit rows and ordering are checked; frequencies are observations, not forced matches. The exact-rational fixture law is separate from a claim that arbitrary floating simulator probabilities are rationally certified.

**D.** `result.expectation(name)` performs the logical coefficient-weighted aggregation; raw lowered term results can be ambiguous. Joint probabilities require conditionals or a joint table; a numerical tolerance is not a pruning threshold for positive events. Replayed pseudorandom ranks are reproducibility, not independent evidence or device calibration. The stated local dense contraction plus inner product uses 40 complex products and 31 additions. The selected float64 table is 32 bytes, and 17 two-bit rows are 34 logical bits or 272 int64 bytes. State preparation/evolution, local matrix and work buffers, exact-integer setup, rank generation, serialization, physical repeated preparations and any hardware timing require their own accounting.

</details>

**Sources and review status.** NC §2.2.3 begins on printed page 84, confirmed against the [publisher's contents](https://assets.cambridge.org/97811070/02173/toc/9781107002173_toc.pdf); no full-textbook access is claimed. The frozen [QuEST v1 representation source](https://arxiv.org/pdf/1802.08032v1#page=2) was consulted only for the dense simulated-state context, not as evidence of this runtime's sampler or hardware performance. All contraction, marginal, prefix and inverse-CDF proofs used here are supplied locally from the declared semantics. Source hashes and review scope are recorded without uploading third-party text. The [section record](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/section-records/44.3.json) separates author validation, independent mathematical/implementation review, reader trial and acceptance. This remains a working draft. The next section in the frozen B03 queue is [44.6 Precision, stability, and normalization drift](#sec-exact-simulation-tensor-execution-and-numerical-reliability-6); 44.4–44.5 retain their later scheduled prerequisites.

<!-- end-section-44.3 -->

<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-6"></span>

## 44.6 Precision, stability, and normalization drift

An ideal unitary preserves norm. A computed vector can gradually gain or lose norm, but a norm close to one does not certify the intended state. A wrong rotation, a lost relative phase, or an incorrect qubit convention can preserve norm perfectly. We need a state-error budget as well as a normalization diagnostic.

The prerequisites are [44.2, indexed local execution](#sec-exact-simulation-tensor-execution-and-numerical-reliability-2), and [2.8, floating-point contracts](ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-8), including the induced Euclidean operator norm imported there from 2.7. Depth **M**: derive a telescoping norm budget and distinguish radial correction from recovering lost phase information. We supply the finite derivations used in the laboratory; we do not assert a rounding theorem for every native kernel.

Run the eight Python blocks in order in a fresh namespace from the repository root. The complete [companion](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/precision_drift.py) and `python scripts/check_precision_drift_prose.py` check the actual snippets and printed outputs. Angles are in **radians**; state norms, probabilities and the Pauli observables in this section are dimensionless. The tested runtime is released FlagQuantum 0.3.1, PyTorch 2.13.0, Python 3.12.14, CPU, with `complex64` and `complex128` explicitly requested. No native result is normalized or phase-aligned before comparison.

### 44.6.1 Precision is a representation contract

A complex64 coordinate has two float32 components; complex128 has two float64 components. In the normalized range, round-to-nearest arithmetic with $p$ significant binary digits has unit roundoff $u=2^{-p}$, while the spacing above one is $\epsilon=2u$. This model excludes overflow and underflow. Neither number by itself bounds an entire circuit's error.

For example, $d=2^{-25}$ is too small to survive addition to one in float32. The exact expression $(1+d)-1=d$ becomes zero. Casting that zero to float64 retains zero; recomputing from the original inputs is different. A small absolute error in the addition becomes a relative error of one in the tiny difference. This is cancellation and sensitivity, not evidence that every subtraction has a large absolute rounding error. A stable method controls error relative to its declared problem; **backward stability** means that the computed answer is an exact answer for suitably small input perturbations. We do not infer that property for FlagQuantum from these tests.

**Formula → code → result: component precision and lost increments.**

```python
import math
import torch
from examples.foundations import precision_drift as n
u32 = torch.finfo(torch.float32).eps/2
u64 = torch.finfo(torch.float64).eps/2
one = torch.tensor(1., dtype=torch.float32)
d = 2**-25
assert float((one+d)-one) == 0
assert float(((one+d)-one).double()) == 0
assert float((torch.tensor(1., dtype=torch.float64)+d)-1) == d
print(u32 == 2**-24, u64 == 2**-53, "casting does not recover the increment")
```

```text
True True casting does not recover the increment
```

### 44.6.2 Derive a state-error budget before inspecting drift

Let $v_0$ be a normalized exact vector and $U_1,\ldots,U_L$ exact unitary operators on the same register. Define $v_j=U_jv_{j-1}$. A finite computed vector $\widehat v_j$ has a local residual

$$
f_j=\widehat v_j-U_j\widehat v_{j-1},\qquad
 d_j=\widehat v_j-v_j,
 \qquad d_j=U_jd_{j-1}+f_j.
$$

Substitute the preceding recurrence repeatedly. With an empty product interpreted as the identity,

$$
d_L=U_L\cdots U_1d_0+
 \sum_{j=1}^{L}U_L\cdots U_{j+1}f_j.
$$

Every intervening product is unitary. It preserves Euclidean norm, so the triangle inequality gives the **telescoping residual budget**

$$
E_L:=\|d_L\|_2\le\|d_0\|_2+\sum_{j=1}^{L}\|f_j\|_2
 \le E_0+\sum_{j=1}^{L}\eta_j=:B_L,
$$

provided the declared nonnegative numbers $\eta_j$ bound the corresponding residuals. If every residual has a justified common bound $\eta$, this becomes $E_0+L\eta$. Assuming such an $\eta$ is different from setting it equal to machine epsilon. Gate arity, reduction order, intermediate magnitudes, matrix construction and backend arithmetic all matter.

For a normalized ideal final vector $v$, write $w=v+d$, $E=\|d\|_2$ and $r=\|w\|_2$. Reverse triangle gives $|r-1|\le E$. Expanding the squared norm gives

$$
\left|r^2-1\right|
 =\left|2\operatorname{Re}\langle v,d\rangle+\|d\|_2^2\right|
 \le 2E+E^2\le 2B_L+B_L^2.
$$

Thus a state-error bound controls drift. The converse does not follow: norm is only one scalar constraint. For an exactly radial positive error $d=av$, $a\ge0$, both the state and drift bounds are attained. The following fixture uses exact dyadic additions and $U_j=I$; its errors are deliberately injected, not observed native rounding.

**Formula → code → result: four radial residuals with an exact reference.**

```python
v0 = torch.tensor([1,0], dtype=torch.complex128)
w = v0.clone()
eta = 2**-12
for _ in range(4):
    w = w + torch.tensor([eta,0], dtype=torch.complex128)
m = n.metrics(w,v0)
assert m['error'] == 4*eta
assert m['drift'] == m['bound']
print(m['error'], m['drift'], "telescoping and drift bounds attained")
```

```text
0.0009765625 0.0019540786743164062 telescoping and drift bounds attained
```

### 44.6.3 Separate represented gates from execution residuals

Suppose a represented local gate is $A_j=U_j+\Delta_j$ and the actual arithmetic satisfies

$$
\widehat v_j=A_j\widehat v_{j-1}+e_j.
$$

Then $f_j=\Delta_j\widehat v_{j-1}+e_j$, and the induced norm inequality from 2.7 yields

$$
\|f_j\|_2\le\|\Delta_j\|\,\|\widehat v_{j-1}\|_2+\|e_j\|_2.
$$

The first term includes representation or parameter error relative to the specified $U_j$; the second includes arithmetic error relative to the represented matrix. An intentional approximate synthesis adds its own gate-model error. Changing precision does not remove a wrong gate or an incorrect input parameter.

For intuition, if $A_j$ alone were applied in exact arithmetic, its unitarity defect would obey

$$
\begin{aligned}
A_j^\dagger A_j-I&=U_j^\dagger\Delta_j+\Delta_j^\dagger U_j+\Delta_j^\dagger\Delta_j,\\
\|A_j^\dagger A_j-I\|&\le2\|\Delta_j\|+\|\Delta_j\|^2.
\end{aligned}
$$

Multiplying the left side between a vector and its adjoint bounds that step's squared-norm change by this defect times the input squared norm. Conversely, a wrong but exactly unitary $A_j$ has zero defect. Unitarity testing cannot identify which unitary was intended.

The book helper `local_trace` applies a two-coordinate RY matrix in the selected dtype, then estimates every residual in complex128. It checks both the direct residual recurrence and the matrix-representation/arithmetic split. The binary64 matrix used by that trace is itself a finite reference; accumulated reference arithmetic and norm calculations are not exact. The small additive guard below is an implementation-check allowance, **not** a rigorous bound on all possible residuals. It does not inspect hidden native intermediates.

**Formula → code → result: residuals at every prefix of a classical execution.**

```python
low, reference, trace = n.local_trace(64, .037, torch.complex64)
budget = sum(row['eta'] for row in trace)
assert n.norm(low.to(torch.complex128)-reference) <= budget+2e-13
assert all(row['error'] <= row['budget']+2e-13 for row in trace)
print(len(trace), "prefix residual inequalities passed; estimates are not certificates")
```

```text
64 prefix residual inequalities passed; estimates are not certificates
```

### 44.6.4 Compare raw native evolution with an independent scalar target

Submit $L$ calls to RY on qubit 0, then $L$ calls to P on qubit 0, then CX with control 0 and target 1. The initial register is $|00\rangle$. Since RY rotations about the same axis add angles and P is diagonal,

$$
|v_L\rangle=c_L|00\rangle+e^{iL\phi}s_L|11\rangle,
\quad c_L=\cos(L\theta/2),\quad s_L=\sin(L\theta/2).
$$

The signed $s_L$ is retained. The computational probabilities are $(c_L^2,0,0,s_L^2)$; applying $X\otimes X$ exchanges the two nonzero coordinates, so

$$
\langle XX\rangle=2\operatorname{Re}(c_L e^{iL\phi}s_L)
 =\sin(L\theta)\cos(L\phi).
$$

The analytic target uses the exact real values represented by the supplied Python float angles. The companion converts those floats with `Decimal.from_float`, accumulates angles in a declared decimal context and evaluates sine/cosine Taylor sums with 180 terms at 60 and 80 digits. Their binary64 exports agree for the tested cases. This is an independent high-precision diagnostic; it is not interval arithmetic, a certified transcendental evaluation, or a claim to recover the intended decimal angle from a previously rounded float.

**Formula → code → result: actual gate calls, requests and raw comparisons.**

```python
from dataclasses import replace
import flagquantum as fq
from examples.foundations.tensor_spaces import OPTIONS
for dtype, precision, tolerance in [(torch.complex64,'complex64',3e-4),
                                     (torch.complex128,'complex128',1e-11)]:
    L, theta, phi = 33, 1/32, -1/64  # angles in radians
    circuit = fq.Circuit(2,dtype=dtype)
    for _ in range(L): circuit.ry(0,theta)
    for _ in range(L): circuit.p(0,phi)
    circuit.cx(0,1)
    result = fq.run(circuit,
        outputs=[fq.probabilities(name='all'),
                 fq.expectation(fq.X(0)@fq.X(1),name='xx')],
        options=replace(OPTIONS,precision=precision))
    raw = result.statevector()[0]
    target = n.reference(L,theta,phi)
    report = n.metrics(raw,target)
    assert raw.dtype == dtype and report['error'] < tolerance
    assert report['drift'] < tolerance
    probabilities = result.measurement('all').value[0].to(torch.float64)
    assert float((probabilities-raw.to(torch.complex128).abs().square()).abs().max()) < tolerance
    expected_xx = 2*(target[0].conj()*target[3]).real.item()
    assert abs(float(result.expectation('xx')[0])-expected_xx) < 2*tolerance
    print(precision, "raw state, drift, probabilities and XX passed")
```

```text
complex64 raw state, drift, probabilities and XX passed
complex128 raw state, drift, probabilities and XX passed
```

There are $2L+1$ submitted gate calls, not a certified count of backend floating operations. No assertion requires error or norm drift to increase monotonically with depth, or complex128 to win in every individual coordinate. Both precisions must satisfy their declared absolute tolerances: $3\times10^{-4}$ and $10^{-11}$ for these bounded cases, with zero relative tolerance. These are validation thresholds, not estimates of every circuit's physical or numerical accuracy. `allow_approximate=False` does not turn finite arithmetic into symbolic arithmetic.

### 44.6.5 Renormalization changes radius, not direction

For $w\ne0$, define $\widetilde w=w/r$. In exact arithmetic,

$$
\|\widetilde w-w\|_2=|1-r|,\qquad
\|\widetilde w-v\|_2\le|1-r|+E\le2E.
$$

The first equality follows by factoring $(1/r-1)w$. The second follows by adding and subtracting $w$ and using the reverse triangle bound. Normalization can completely remove a positive radial error, but cannot change the ray of $w$. It is not guaranteed to reduce the full vector error for every $w$; it provides the displayed bound. Its floating implementation introduces additional error.

For $|+\rangle=(|0\rangle+|1\rangle)/\sqrt2$ and $|-\rangle=(|0\rangle-|1\rangle)/\sqrt2$, both norms equal one, yet their X expectations are $+1$ and $-1$. Normalizing the wrong vector cannot restore the relative phase. A missing global phase is also unrecoverable from norm alone; it is unobservable for an isolated ray but can be relative phase when the preparation becomes one branch of a controlled construction. Full-vector comparisons here fix the declared circuit phase and do not silently align it.

**Formula → code → result: radial repair and a phase-error counterexample.**

```python
plus = torch.tensor([1,1],dtype=torch.complex128)/math.sqrt(2)
minus = plus*torch.tensor([1,-1])
radial = n.normalize(w)
phase_wrong = n.normalize(minus)
assert torch.equal(radial,v0)
assert abs(n.norm(phase_wrong)-1) < 1e-15
assert n.norm(phase_wrong-plus) > 1.4
X = torch.tensor([[0,1],[1,0]],dtype=torch.complex128)
assert abs(float(torch.vdot(plus,X@plus).real)-1) < 1e-15
assert abs(float(torch.vdot(phase_wrong,X@phase_wrong).real)+1) < 1e-15
print("radial error removed; relative-phase error and opposite X predictions remain")
```

```text
radial error removed; relative-phase error and opposite X predictions remain
```

### 44.6.6 Compute diagnostics without manufacturing zeros

Naively squaring very small nonzero components can underflow. For a finite nonzero vector choose $s$ as the maximum absolute real or imaginary component. Algebraically,

$$
\|w\|_2=s\left(\sum_i |w_i/s|^2\right)^{1/2}.
$$

Scaling before squaring avoids the particular underflow in this example. The helper first promotes representable input components to complex128, computes this scale, and explicitly rejects zero normalization. Promotion cannot recover components already lost in an earlier computation. A true norm outside the floating range cannot be returned as an ordinary finite scalar; the normalization helper explicitly reports that range failure. This is not a universal subnormal-arithmetic guarantee. Normalization must be an explicit, recorded transformation, with the original vector and raw norm preserved.

Here `tiny` is an unnormalized mathematical vector used to test a norm kernel; it is not submitted as a quantum state to FlagQuantum. No square-underflow value is interpreted as a physically impossible event.

**Formula → code → result: a scaled norm and the zero-vector boundary.**

```python
tiny = torch.tensor([1e-200,1e-200j],dtype=torch.complex128)
naive_square_sum = float(tiny.abs().square().sum())
scaled_length = n.norm(tiny)
assert naive_square_sum == 0 and scaled_length > 0
assert abs(n.norm(n.normalize(tiny))-1) < 1e-14
try: n.normalize(tiny*0)
except ValueError: print("scaled norm retains nonzero direction; zero normalization rejected")
else: raise AssertionError("zero vector accepted")
```

```text
scaled norm retains nonzero direction; zero normalization rejected
```

### 44.6.7 Propagate error to observables and rare conditional branches

For a Hermitian operator $H$, adding and subtracting $v^\dagger Hw$ gives

$$
\begin{aligned}
w^\dagger Hw-v^\dagger Hv&=d^\dagger Hw+v^\dagger Hd,\\
|w^\dagger Hw-v^\dagger Hv|&\le\|H\|E(r+1)\le\|H\|E(2+E).
\end{aligned}
$$

The same proof for an event projector $P$, whose operator norm is at most one, bounds the difference of **raw quadratic weights** by $E(2+E)$. If $w$ is not normalized these weights need not sum to one and must not be called a normalized probability distribution. After explicit normalization, write $E'=\|\widetilde w-v\|_2$; since both norms are one, the bound is $2\|H\|E'$ or $2E'$ for an event, with $E'\le2E$ as above. Relative error in a tiny probability can be large even when the absolute bound is small. Shot fluctuation is a separate statistical error from Chapters 6 and 14.

For a rare event with $b=Pv$, $a=Pw$ and $p=\|b\|_2^2>0$, a conditional comparison requires $a\ne0$. Adding and subtracting $a/\|b\|_2$ yields

$$
\left\|\frac{a}{\|a\|_2}-\frac{b}{\|b\|_2}\right\|_2
 \le\frac{|\|b\|_2-\|a\|_2|+\|a-b\|_2}{\|b\|_2}
 \le\frac{2\|a-b\|_2}{\sqrt p}\le\frac{2E}{\sqrt p}.
$$

There is no uniform small conditional error as $p$ tends to zero. If the computed projection vanishes, the normalized computed branch is undefined; inventing a branch or clipping it is not validation. The following two normalized vectors differ only by moving a rare amplitude between two selected coordinates. Their global difference is small but their conditional vectors are orthogonal.

**Formula → code → result: absolute output control without a false conditional guarantee.**

```python
p = 1e-12
before = torch.tensor([math.sqrt(1-p),math.sqrt(p),0,0],dtype=torch.complex128)
after = torch.tensor([math.sqrt(1-p),0,math.sqrt(p),0],dtype=torch.complex128)
mask = torch.tensor([0,1,1,0],dtype=torch.complex128)
E = n.norm(after-before)
conditional_error = n.norm(n.normalize(after*mask)-n.normalize(before*mask))
assert E < 2e-6 and conditional_error > 1.4
assert conditional_error <= 2*E/math.sqrt(p)
report = n.metrics(after,before)
assert report['event_error'] <= report['bound']+1e-15
print("small global error, large conditional error; absolute event bound passed")
```

```text
small global error, large conditional error; absolute event bound passed
```

### 44.6.8 Keep implementation support and verification separate

The actual APIs exercised here are `Circuit(...,dtype=...)`, named RY/P/CX gate calls, `ExecutionOptions(precision=...)`, `fq.run`, `result.statevector()`, `result.measurement(name).value` and `result.expectation(name)`. `probabilities` is a tensor-valued result property in this release, not a callable named-result accessor; the initial prototype incorrectly called it and failed after one native run. That source and failure log are retained. The corrected named measurement accessor is used throughout the final snippets. This was a book-side API misuse, not a reported native numerical defect.

The complete program uses a CPU statevector profile and checks the returned dtype, raw vector, norm drift, full probabilities and XX expectation in both precisions. It does not claim to validate GPU arithmetic, density-matrix drift, gradients, every precision/backend combination, automatic error estimation, native per-gate residual tracing or an interval certificate. The optional `normalize` routine and residual trace belong to this book; their existence is not a native normalization-policy API. No post-hoc correction is used to make a failed raw comparison pass.

**Formula → code → result: independently chosen parameters and explicit correction checks.**

```python
for dtype in (torch.complex64,torch.complex128):
    raw, target, report = n.native(91,-.047,.031,dtype)
    corrected = n.normalize(raw)
    assert n.norm(corrected.to(torch.complex128)-target) <= 2*report['error']+1e-12
assert n.errors() == 14
n.examples()
print("2 fresh native checks and 14 rejected contracts; raw reports kept before optional correction")
```

```text
2 fresh native checks and 14 rejected contracts; raw reports kept before optional correction
```

In the initial author execution of the printed $L=91$ check, complex64 gave vector error approximately $1.19\times10^{-7}$ and squared-norm drift $2.52\times10^{-8}$; complex128 gave vector error $2.20\times10^{-15}$ and reported drift zero. These are archived observations on this CPU, not portable exact outputs or proof of exact normalization.

The complete program performs 24 native runs: four depths $L\in\{1,7,64,257\}$, three signed angle pairs, and both precisions. It also checks eight classical residual traces, exact radial fixtures, relative phase, rare conditioning, scaled norms and 14 invalid contracts. The final checker executes four additional native runs in the eight printed units. Fresh transfer evidence changes depths and signed angles in both precisions; it is recorded separately from these calls. Tests support the implementation translation; the algebra above supplies the declared bounds under its assumptions.

Expected output of the complete program:

```text
24 native CPU statevector runs: two precisions, four depths, three signed angle pairs passed.
Decimal 60/80-digit references agree after binary64 export; raw state, norm, probabilities and XX checked.
8 local residual traces; cancellation, radial drift, phase loss, rare conditioning and scaled-norm checks passed.
14 malformed contracts rejected; no native output renormalization or phase alignment applied.
```

**Check your understanding and transfer.**

- **44.6-A — error budget.** With exact $v_0$, $L=100$, and justified residual bounds $\eta_j\le10^{-8}$, find a state-error and squared-norm-drift bound. Does measured zero drift prove zero state error?
- **44.6-B — lost phase.** Replace $|+\rangle$ by $(|0\rangle+i|1\rangle)/\sqrt2$. Compare norm, computational probabilities, X and Y expectations. Can normalization identify which state was intended?
- **44.6-C — fresh execution.** Use $L\in\{19,113,311\}$ and $(\theta,\phi)=(-.029,.017)$ in both precisions, compare raw native outputs with the Decimal reference, and retain all errors before trying explicit normalization. Do not require drift to be monotone or observed errors to attain the theoretical bound.
- **44.6-D — conditioning and failure.** Repeat the rare-amplitude construction with $p=10^{-16}$. Explain why a tolerance justified for an unconditional probability cannot automatically certify the conditional state. Diagnose a report that casts an already rounded result, normalizes it, then declares accuracy from its norm alone.

<details markdown="1">
<summary>Answers and verification guidance for 44.6-A–D</summary>

**A.** $B_L=10^{-6}$ and $|r^2-1|\le2\times10^{-6}+10^{-12}$. Zero drift is consistent with a wrong unitary or a relative-phase error. It cannot invert the implication from state error to drift.

**B.** Both norms are one and both computational laws are $(1/2,1/2)$. The original state has $(\langle X\rangle,\langle Y\rangle)=(1,0)$; the changed state has $(0,1)$, using the Y sign convention of 6.3. Radius and computational probabilities do not determine the phase. Compare a phase-sensitive observable against a declared target.

**C.** The transfer program records six native calls with new depths, signed angles and both precisions. It checks raw vector/probability/XX errors against their declared thresholds and the scalar reference before any correction. Different depths can have cancelling errors; lower drift alone does not select the more accurate vector. Decimal agreement is diagnostic, not a certified error enclosure.

**D.** The global distance is $\sqrt{2p}$ while the two selected, normalized branches remain distance $\sqrt2$ apart. The bound $2E/\sqrt p$ is then larger than one, as it should be. An already lost component is not recreated by casting. Normalization discards a radial diagnostic and leaves wrong direction or phase untouched. Retain raw errors, identify the source and recompute at suitable precision if needed; do not relabel a repaired norm as recovered information.

</details>

**Sources and review status.** The norm conventions and induced-operator inequalities were checked against [Watrous §1.1.3, printed pp. 32–33](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf#page=40). The [QuEST v1 representation passage, PDF p. 2](https://arxiv.org/pdf/1802.08032v1#page=2) supplies context for finite floating complex state storage and declared precision, not a FlagQuantum rounding guarantee. The local residual, normalization and conditioning derivations above are supplied here; third-party source text is not redistributed. The section record separates author execution from pending independent mathematical/implementation review and reader trial. This is a draft, not accepted. The next scheduled B03 target is 44.8, not the deferred 44.4–44.5 or 44.7.

<!-- end-section-44.6 -->
