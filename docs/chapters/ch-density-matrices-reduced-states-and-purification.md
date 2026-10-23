# 8. Density Matrices, Reduced States, and Purification

**Working drafts: sections 8.1–8.8 · Writing Baseline 1.0 · October 23, 2026.** Author execution is separate from independent mathematical review, implementation review and reader trial; these remain pending. The examples use released FlagQuantum 0.3.1, PyTorch 2.13.0 and CPU complex128.

<span id="sec-density-matrices-reduced-states-and-purification-1"></span>

## 8.1 Statistical ensembles and density operators

A source may choose a preparation using a classical random label and then supply only the prepared quantum system. Keeping a list of all possible vectors is sufficient to predict measurements, but it is often redundant. We will construct one operator that reproduces every measurement probability available on that system, prove exactly when two finite ensembles are indistinguishable in this sense, and identify what information this operator does not retain about a source.

The frozen prerequisites are [2.3, Linear maps, bases, and changes of coordinates](ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-3), and [6.6, finite probability and sampling](ch-measurement-expectation-values-and-statistical-estimation.md#sec-measurement-expectation-values-and-statistical-estimation-6). We recall the needed Born rule locally. This section has depth **F**: the probability/expectation identities and the operational equivalence in both directions are proved, rather than inferred from a few tests.

Work in a finite complex space of dimension d with a declared orthonormal basis. For n qubits, d=2ⁿ and q0 is the most significant full-vector bit. All state amplitudes and probabilities are dimensionless; angles in code are radians. Hermitian means equal to the conjugate transpose. We use exact algebra for the proofs and absolute tolerance $10^{-12}$, relative tolerance zero, for deterministic execution checks. A floating-point agreement or numerical positive-semidefinite check is not an exact certificate for an unknown physical preparation.

Run the eight cumulative Python units from the repository root with the pinned example requirements. The complete companion is [statistical_ensembles.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/statistical_ensembles.py). Native density outputs are used explicitly. Classical sums over ensemble weights are labelled as such; they are not presented as an arbitrary mixed-state input API.

### 8.1.1 Replace an ensemble list with an operator

A finite statistical ensemble is a list

$$
\mathcal E=\{(p_j,|\psi_j\rangle):j=1,\ldots,m\},
$$

where $p_j\geq0$, $\sum_jp_j=1$, and each vector has norm one in the same space. The operational prescription is: choose classical label j with probability pⱼ and prepare ψⱼ. Unless stated otherwise, the receiver does **not** receive j. Zero-weight entries can be omitted; duplicate vectors or different global phases need not be distinct states.

Define the **density operator** associated with this ensemble by

$$
\rho_{\mathcal E}
 =\sum_jp_j|\psi_j\rangle\langle\psi_j|.
$$

The outer product denotes the linear map $x\mapsto\psi_j(\psi_j^\dagger x)$. If ψⱼ has coordinates ψⱼ,ₐ, the individual entries are

$$
(\rho_{\mathcal E})_{ab}
 =\sum_jp_j\psi_{j,a}\psi_{j,b}^*.
$$

The complex conjugate belongs on the second factor. Replacing the outer product by a coordinatewise product or omitting that conjugate gives a different object. Although we write a matrix in code, the definition is an operator: a basis change changes all coordinates together, not the underlying preparation.

Some immediate consequences will be needed for probabilities. Each outer product is Hermitian, so ρ is Hermitian. For every vector x,

$$
\langle x|\rho|x\rangle
 =\sum_jp_j|\langle\psi_j|x\rangle|^2\geq0.
$$

This property is called **positive semidefinite**, abbreviated here as positive. Define the trace by $\operatorname{Tr}A=\sum_aA_{aa}$. Then

$$
\operatorname{Tr}\rho
 =\sum_jp_j\sum_a|\psi_{j,a}|^2
 =\sum_jp_j=1.
$$

A density operator is a positive, Hermitian, unit-trace operator. We have proved that every ensemble here produces one. The converse spectral representation and detailed purity criteria belong to 8.2.

For the half/half computational ensemble, the outer matrices are diag(1,0) and diag(0,1), so ρ=I/2. The native request returns a batch axis: one one-qubit matrix has shape (1,2,2). We remove that execution batch axis before combining components.

```python
import math,cmath
import torch
import flagquantum as fq
from dataclasses import replace
from examples.foundations import statistical_ensembles as e
from examples.foundations.tensor_spaces import OPTIONS

basis = tuple(torch.eye(2,dtype=torch.complex128))
native_z = []
for j in (0,1):
    c = fq.Circuit(1,dtype=torch.complex128)
    if j:
        c.x(0)
    r = fq.run(c,outputs=[fq.density_matrix(),fq.probabilities()],options=OPTIONS)
    e.RUNS += 1
    e.close(r.density_matrix[0],e.outer(basis[j]))
    native_z.append(r.density_matrix[0])
rho_z = (native_z[0]+native_z[1])/2  # explicit classical mixture
e.close(rho_z,e.I/2)
e.close(rho_z,e.scalar_rho((.5,.5),basis))
print("Two native pure density outputs;their classical half/half sum is I/2.")
```

```text
Two native pure density outputs;their classical half/half sum is I/2.
```

The factor one half is a classical probability. No random choice was sampled in this calculation: both components were executed, and their exact prescribed weights were applied on the host. The matrix I/2 describes the receiver's system after the label is ignored.

### 8.1.2 Derive the trace probability and expectation rules

For a projective measurement with mutually orthogonal projectors Pᵦ summing to I, the pure-state Born rule is $\langle\psi_j|P_b|\psi_j\rangle$. The law of total probability therefore gives

$$
p(b)=\sum_jp_j\langle\psi_j|P_b|\psi_j\rangle.
$$

The same argument applies to a measurement specified by positive effects Eᵦ summing to I, provided its pure-input probability is $\langle\psi_j|E_b|\psi_j\rangle$, as in 6.5. An effect satisfies $0\leq E_b\leq I$; neither a general update rule nor a native POVM endpoint is assumed here.

To rewrite this probability, expand one outer product in the declared basis:

$$
\begin{aligned}
\operatorname{Tr}(|\psi\rangle\langle\psi|E)
 &=\sum_{a,b}\psi_a\psi_b^*E_{ba}\\
 &=\langle\psi|E|\psi\rangle.
\end{aligned}
$$

Finite sums can be interchanged, so

$$
\boxed{p(b)=\operatorname{Tr}(\rho E_b).}
$$

Every term in the original mixture sum is nonnegative. Summing outcomes gives $\operatorname{Tr}(\rho\sum_bE_b)=\operatorname{Tr}\rho=1$. Thus this is a normalized probability law, not a new independent postulate added to the ensemble model.

For a Hermitian observable A, the pure-state mean is ⟨ψ|A|ψ⟩, as derived from its spectral measurement in 6.3. Averaging over the label and applying the same identity gives

$$
\langle A\rangle_{\mathcal E}
 =\sum_jp_j\langle\psi_j|A|\psi_j\rangle
 =\operatorname{Tr}(\rho A).
$$

This number is real because every Hermitian quadratic form in the mixture is real. It is not generally $\operatorname{Tr}\rho\operatorname{Tr}A$.

For completeness, the trace does not depend on the chosen orthonormal basis. If a new basis has coordinate columns given by a unitary V, then

$$
\begin{aligned}
\operatorname{Tr}(V^\dagger AV)
 &=\sum_{a,b,c}V_{ba}^*A_{bc}V_{ca}\\
 &=\sum_{b,c}A_{bc}\delta_{bc}
 =\operatorname{Tr}A.
\end{aligned}
$$

The middle equality uses $\sum_aV_{ca}V_{ba}^*=\delta_{cb}$. Also $\operatorname{Tr}(AB)=\sum_{a,b}A_{ab}B_{ba}=\operatorname{Tr}(BA)$ by renaming the finite indices. These identities explain why compatible coordinate changes leave the probability invariant.

The next code tests a complex ensemble, a Hermitian Pauli sum, and a non-coordinate rank-one effect E=|w⟩⟨w|. The native analyzer applies the conjugate transpose of a unitary whose first column is w, making that effect the computational zero outcome. The scalar reference independently sums component quadratic forms.

```python
weights = (.35,.65)
vectors = (e.qubit(.87,-.52),e.qubit(1.61,.43))
A = .7*e.X-.2*e.Y+1.3*e.Z
w = e.qubit(1.14,.63)
E = e.outer(w)
native_rhos,means,probabilities = [],[],[]
for v in vectors:
    c = fq.Circuit(1,dtype=torch.complex128).unitary(0,unitary=e.prepare(v))
    r = fq.run(c,outputs=[fq.density_matrix(),
        fq.expectation(fq.X(0),name="x"),fq.expectation(fq.Y(0),name="y"),
        fq.expectation(fq.Z(0),name="z")],options=OPTIONS)
    e.RUNS += 1
    native_rhos.append(r.density_matrix[0])
    means.append(.7*r.expectation("x")[0]-.2*r.expectation("y")[0]+1.3*r.expectation("z")[0])
    # U_w sends |0> to w;U_w^dagger makes the w effect a Z=0 event.
    c.unitary(0,unitary=e.prepare(w).mH.contiguous())
    measured = fq.run(c,outputs=[fq.probabilities()],options=OPTIONS)
    e.RUNS += 1
    probabilities.append(measured.probabilities[0,0])
R = sum(p*q for p,q in zip(weights,native_rhos))
e.close(R,e.scalar_rho(weights,vectors))
e.close(torch.trace(R@E),e.born(weights,vectors,E))
e.close(torch.trace(R@E),sum(p*q for p,q in zip(weights,probabilities)))
e.close(torch.trace(R@A),sum(p*q for p,q in zip(weights,means)))
print("Complex ensemble:trace probabilities match scalar Born sums and native analyzer outcomes.")
print("Trace expectation matches the weighted native X/Y/Z observable mean.")
```

```text
Complex ensemble:trace probabilities match scalar Born sums and native analyzer outcomes.
Trace expectation matches the weighted native X/Y/Z observable mean.
```

Here the Pauli sum uses the native X/Y/Z expectations and combines them with real coefficients. The general effect trace is classical analysis checked against the actual native basis analyzer. No general matrix-observable or POVM execution capability is inferred from a host matrix multiplication.

### 8.1.3 Different ensembles can give exactly the same density

The equal mixtures of |0⟩,|1⟩ and of |+⟩,|−⟩ are different preparation instructions. Nevertheless,

$$
\begin{aligned}
\rho&=\tfrac12|+\rangle\langle+|
     +\tfrac12|-\rangle\langle-|\\
 &=\frac12\begin{pmatrix}1&0\\0&1\end{pmatrix}
 =\frac I2.
\end{aligned}
$$

The off-diagonal terms cancel. The same is true for the equal mixture of $|+i\rangle=(|0\rangle+i|1\rangle)/\sqrt2$ and $|-i\rangle=(|0\rangle-i|1\rangle)/\sqrt2$. By the trace rule, every system-only measurement has the same unlabelled probabilities for all three preparations.

Nonuniqueness is not confined to the equal-identity example. Choose $0<r<1$ and real φ, and define

$$
|u_\pm\rangle
 =\sqrt r\,|0\rangle
 \pm e^{i\phi}\sqrt{1-r}\,|1\rangle.
$$

Their equal mixture has density

$$
\begin{aligned}
\rho&=\tfrac12|u_+\rangle\langle u_+|
     +\tfrac12|u_-\rangle\langle u_-|\\
 &=\begin{pmatrix}r&0\\0&1-r\end{pmatrix}\\
 &=r|0\rangle\langle0|+(1-r)|1\rangle\langle1|.
\end{aligned}
$$

The left description uses two equally weighted vectors with overlap $\langle u_+|u_-\rangle=2r-1$. The right uses orthogonal computational vectors with unequal weights. At r=.73 the first vectors are not orthogonal, yet both ensembles define precisely the same operator. The computational vectors are eigenvectors of this diagonal matrix, with eigenvalues r and 1−r. This eigenvector-and-eigenvalue description is its spectral ensemble; 8.2 develops the general construction.

```python
xy = {}
for name,phases in (("X",(0.,math.pi)),("Y",(math.pi/2,-math.pi/2))):
    components = tuple(e.qubit(math.pi/2,p) for p in phases)
    matrices = []
    for v in components:
        c = fq.Circuit(1,dtype=torch.complex128).unitary(0,unitary=e.prepare(v))
        r = fq.run(c,outputs=[fq.density_matrix()],options=OPTIONS)
        e.RUNS += 1
        matrices.append(r.density_matrix[0])
    xy[name] = components
    e.close((matrices[0]+matrices[1])/2,rho_z)
rpop,phi = .73,.41
nonorth = tuple(torch.tensor([math.sqrt(rpop),s*cmath.exp(1j*phi)*math.sqrt(1-rpop)],
                            dtype=torch.complex128) for s in (1,-1))
matrices = []
for v in nonorth:
    c = fq.Circuit(1,dtype=torch.complex128).unitary(0,unitary=e.prepare(v))
    r = fq.run(c,outputs=[fq.density_matrix()],options=OPTIONS)
    e.RUNS += 1
    matrices.append(r.density_matrix[0])
rho_nonorth = (matrices[0]+matrices[1])/2
e.close(rho_nonorth,e.rho((rpop,1-rpop),basis))
e.close(torch.vdot(nonorth[0],nonorth[1]),2*rpop-1)
print("Z,X,Y equal mixtures all give I/2.")
print("Nonorthogonal half/half mixture gives diag(0.73,0.27);component overlap=0.46.")
```

```text
Z,X,Y equal mixtures all give I/2.
Nonorthogonal half/half mixture gives diag(0.73,0.27);component overlap=0.46.
```

This equality does not identify a unique “actual vector hidden in ρ,” nor does it erase a source's preparation history. It says the history cannot be inferred from measurements of this system alone when the classical labels are inaccessible. A density operator is the operational state description for that specified system. Later reduced-state examples will also show why a mixed density need not be interpreted as ignorance about one uniquely chosen pure component.

### 8.1.4 A statistical mixture is not an averaged amplitude

The coherent vector $|+\rangle=(|0\rangle+|1\rangle)/\sqrt2$ has density

$$
|+\rangle\langle+|
 =\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix}.
$$

It has the same computational diagonal as I/2 but different off-diagonal entries. For X,

$$
\operatorname{Tr}((I/2)X)=0,\qquad
\langle+|X|+\rangle=1.
$$

Normalizing the sum of the computational ensemble's vectors would therefore turn a mixture into a different coherent preparation.

There is a second diagnostic. Multiplying any component ψⱼ by a global phase leaves its outer product fixed, because $e^{i\gamma_j}e^{-i\gamma_j}=1$. But the normalized sum of the component vectors generally changes when their individual phases change. Such a sum cannot be a representation-independent rule for classical mixing.

```python
c = fq.Circuit(1,dtype=torch.complex128).h(0)
r = fq.run(c,outputs=[fq.density_matrix(),
    fq.expectation(fq.X(0),name="x")],options=OPTIONS)
e.RUNS += 1
rho_plus = r.density_matrix[0]
e.close(rho_plus,e.outer((basis[0]+basis[1])/math.sqrt(2)))
e.close(torch.trace(rho_z@e.X),0.)
e.close(r.expectation("x")[0],1.)
phase_changed = (basis[0]+1j*basis[1])/math.sqrt(2)
e.close(e.rho((.5,.5),(basis[0],1j*basis[1])),rho_z)
e.close(torch.vdot(phase_changed,e.Y@phase_changed),1.)
print("Classical Z mixture:X mean0;coherent plus superposition:X mean1.")
print("Changing a component's global phase leaves the mixture fixed but changes a vector-average prediction.")
```

```text
Classical Z mixture:X mean0;coherent plus superposition:X mean1.
Changing a component's global phase leaves the mixture fixed but changes a vector-average prediction.
```

The distinction is addition of probabilities versus addition of amplitudes. A coherent preparation with a specified relative phase is meaningful; it simply is not the result of forgetting a classical preparation label. Renormalizing an arbitrary average vector does not repair this conceptual error.

### 8.1.5 State exactly which record is being ignored

If the label is accessible, the receiver has more than the system described by ρ. For two labels encoded in an orthogonal record basis |0⟩,|1⟩, a joint preparation can be represented by

$$
\Omega_{JQ}
 =\sum_{j=0}^1p_j|j\rangle\langle j|_J
       \otimes|\psi_j\rangle\langle\psi_j|_Q.
$$

This is itself an ensemble density, now of a larger system: each component is the product |j⟩⊗|ψⱼ⟩. A joint event that reads label j and then tests effect E on Q has probability

$$
p(j,E)=p_j\langle\psi_j|E|\psi_j\rangle.
$$

Summing j gives $\operatorname{Tr}(\rho E)$, while retaining j permits different conditional predictions. No partial-trace theorem is needed for this direct mixture calculation; the general reduced-state construction is developed in 8.4.

For the half/half Z and X preparations, write ΩZ and ΩX for these larger joint densities. The event “label=0 and Q measured in Z gives 0” has probability 1/2 for ΩZ and 1/4 for ΩX. Ignoring the label gives Q's zero probability 1/2 in both cases. Thus the two preparations have the same Q state and different JQ states, with no contradiction.

```python
labelled = {}
for name,components in (("Z",basis),("X",xy["X"])):
    parts = []
    for j,v in enumerate(components):
        c = fq.Circuit(2,dtype=torch.complex128)
        if j:
            c.x(0)
        c.unitary(1,unitary=e.prepare(v))
        r = fq.run(c,outputs=[fq.density_matrix()],options=OPTIONS)
        e.RUNS += 1
        parts.append(r.density_matrix[0])
    Omega = (parts[0]+parts[1])/2
    e.close(Omega,e.cq((.5,.5),components))
    labelled[name] = Omega
e.close(labelled["Z"][0,0],.5)
e.close(labelled["X"][0,0],.25)
for Omega in labelled.values():
    e.close(Omega[0,0]+Omega[2,2],.5)
print("Joint label0/systemZ0:Z preparation0.5,X preparation0.25.")
print("Ignoring the label gives system Z0 probability0.5 in both cases.")
```

```text
Joint label0/systemZ0:Z preparation0.5,X preparation0.25.
Ignoring the label gives system Z0 probability0.5 in both cases.
```

The native circuits prepare the four product components in a two-qubit register. Their classical half/half matrix sums form the joint ensemble densities. This does not claim a native classical-memory service or an injected mixed input. Operational equivalence must always name the accessible system and side information.

### 8.1.6 Prove the converse: all probabilities determine the operator

We have proved that equal densities give equal probabilities. Conversely, suppose two finite ensembles have Hermitian densities ρ and σ, and their probabilities agree for every rank-one projector |v⟩⟨v| with normalized v. Each such projector is a valid event in the two-outcome measurement $\{|v\rangle\langle v|,I-|v\rangle\langle v|\}$. Let Δ=ρ−σ. Then

$$
\langle v|\Delta|v\rangle=0
$$

for every normalized v. We now recover all entries in a fixed orthonormal basis.

Taking v=|a⟩ gives Δₐₐ=0. For each a<b, take the two normalized vectors

$$
\begin{aligned}
|v^+_{ab}\rangle&=\frac{|a\rangle+|b\rangle}{\sqrt2},\\
|v^i_{ab}\rangle&=\frac{|a\rangle+i|b\rangle}{\sqrt2}.
\end{aligned}
$$

Hermiticity gives $\Delta_{ba}=\Delta_{ab}^*$. With the diagonals already zero,

$$
\begin{aligned}
\langle v^+_{ab}|\Delta|v^+_{ab}\rangle
 &=\operatorname{Re}\Delta_{ab},\\
\langle v^i_{ab}|\Delta|v^i_{ab}\rangle
 &=-\operatorname{Im}\Delta_{ab}.
\end{aligned}
$$

Both vanish, so every off-diagonal entry vanishes as well. Hence Δ=0 and ρ=σ. Exactly d coordinate vectors plus two vectors per unordered coordinate pair suffice for this argument: $d+2\binom d2=d^2$ rank-one event tests.

We have established the finite-ensemble equivalence:

$$
\begin{gathered}
\rho_{\mathcal E}=\rho_{\mathcal F}\\
\Longleftrightarrow\\
\text{all unlabelled system-only measurement probabilities agree}.
\end{gathered}
$$

These event tests need not belong to one common measurement basis. Equality of the diagonal in one basis only fixes that basis's probabilities, not the whole density. As a two-qubit counterexample, Φ⁺ and the half/half mixture of 00 and 11 have the same Z diagonal. The |++⟩ event has probabilities 1/2 and 1/4 respectively.

The code also compares equal mixtures of the four computational states and the four Bell states. Both give I₄/4. Named native outputs verify a reversed kept-qubit ordering explicitly; the matrix indices must follow the selected order.

```python
twoqubit = {"computational":[],"Bell":[]}
for a in (0,1):
    for b in (0,1):
        for name in ("computational","Bell"):
            c = fq.Circuit(2,dtype=torch.complex128)
            if a:
                c.x(0)
            if b:
                c.x(1)
            if name=="Bell":
                c.h(0).cx(0,1)
            r = fq.run(c,outputs=[fq.density_matrix(name="full"),
                fq.density_matrix(qubits=(1,0),name="reversed")],options=OPTIONS)
            e.RUNS += 1
            M = r.measurement("full").value[0]
            perm = torch.tensor([0,2,1,3])
            e.close(r.measurement("reversed").value[0],M[perm][:,perm])
            twoqubit[name].append(M)
Rcomp = sum(twoqubit["computational"])/4
Rbell = sum(twoqubit["Bell"])/4
e.close(Rcomp,Rbell)
e.close(Rcomp,torch.eye(4,dtype=torch.complex128)/4)
for v in e.probes(4):
    e.close(torch.vdot(v,(Rcomp-Rbell)@v),0.)
# A single basis cannot establish equality.
Rcorr = (twoqubit["computational"][0]+twoqubit["computational"][3])/2
RB = twoqubit["Bell"][0]
e.close(Rcorr.diag(),RB.diag())
plus2 = torch.kron(xy["X"][0],xy["X"][0])
e.close(torch.vdot(plus2,Rcorr@plus2),.25)
e.close(torch.vdot(plus2,RB@plus2),.5)
print("Computational and Bell equal mixtures:I4/4;all16separating probes agree.")
print("Same Z diagonal is insufficient:the plus-plus event distinguishes0.25from0.5.")
```

```text
Computational and Bell equal mixtures:I4/4;all16separating probes agree.
Same Z diagonal is insufficient:the plus-plus event distinguishes0.25from0.5.
```

The sixteen probes in the four-dimensional check implement the algebraic separating family. This is a deterministic implementation check on known matrices, not a finite-data tomography certificate of exact equality. Estimating those probabilities experimentally introduces uncertainty, which the exact converse does not remove.

### 8.1.7 Preserve equivalence under the same operation, not different labelled operations

If every component experiences the same unitary U, then

$$
\rho'
 =\sum_jp_jU|\psi_j\rangle\langle\psi_j|U^\dagger
 =U\rho U^\dagger.
$$

This is just distributivity over the finite sum; U†U=I preserves norms and probabilities. Therefore equal initial densities remain equal after the same U. Any fixed later effect E has probability $\operatorname{Tr}(U\rho U^\dagger E)=\operatorname{Tr}(\rho U^\dagger EU)$. The last identity follows from the cyclic trace identity proved above.

If the operator depends on an available preparation label, it cannot in general be factored out. For example, apply I at j=0 and X at j=1 to both equal-weight preparations:

- From the Z preparation, both corrected vectors are |0⟩.
- From the X preparation, |+⟩ remains |+⟩ and X|−⟩=−|−⟩, so the ignored density remains I/2.

The initial Q densities agree, but the initial JQ states and the label-controlled protocol inputs differ. A rule that accesses J is not a system-only operation on Q.

```python
theta,phi = .83,-.57
U = torch.diag(torch.tensor([1,cmath.exp(1j*phi)],dtype=torch.complex128)) @ torch.tensor(
    [[math.cos(theta/2),-math.sin(theta/2)],[math.sin(theta/2),math.cos(theta/2)]],
    dtype=torch.complex128)
transformed = []
for weights,components in (((rpop,1-rpop),basis),((.5,.5),nonorth)):
    matrices = []
    for v in components:
        c = fq.Circuit(1,dtype=torch.complex128).unitary(0,unitary=e.prepare(v))
        c.ry(0,theta).p(0,phi)
        r = fq.run(c,outputs=[fq.density_matrix()],options=OPTIONS)
        e.RUNS += 1
        matrices.append(r.density_matrix[0])
    transformed.append(sum(p*M for p,M in zip(weights,matrices)))
e.close(transformed[0],transformed[1])
e.close(transformed[0],U@rho_nonorth@U.mH)
controlled = []
for components in (basis,xy["X"]):
    matrices = []
    for j,v in enumerate(components):
        c = fq.Circuit(1,dtype=torch.complex128).unitary(0,unitary=e.prepare(v))
        if j:
            c.x(0)  # host knows the preparation label
        r = fq.run(c,outputs=[fq.density_matrix()],options=OPTIONS)
        e.RUNS += 1
        matrices.append(r.density_matrix[0])
    controlled.append((matrices[0]+matrices[1])/2)
e.close(controlled[0],e.outer(basis[0]))
e.close(controlled[1],e.I/2)
print("Fixed Ry/P operation preserves the nonorthogonal/spectral equivalence.")
print("Label-dependent X changes the inputs:Z ensemble becomes pure0;X ensemble stays I/2.")
```

```text
Fixed Ry/P operation preserves the nonorthogonal/spectral equivalence.
Label-dependent X changes the inputs:Z ensemble becomes pure0;X ensemble stays I/2.
```

The label-dependent X is selected on the host for a known component fixture. It is not a native measurement-conditioned feedback request. The general theory of mixed-state channels and instruments is developed later; this calculation needs only the stated unitary and classical-label operations.

### 8.1.8 Do not infer independence or unsupported execution capabilities

A single-system density does not specify the joint preparation of several systems or trials. Compare two Z sources: one independently draws a fair label for each trial; the other draws a fair label once and reuses it for two trials. Each individual trial has density I/2. Their two-trial densities, in order 00,01,10,11, are

$$
\begin{aligned}
\rho_{\mathrm{ind}}&=I_4/4,\\
\rho_{\mathrm{shared}}&=\tfrac12|00\rangle\langle00|
                    +\tfrac12|11\rangle\langle11|.
\end{aligned}
$$

For the event that the two Z results agree, the effect is $E_{\mathrm{same}}=\operatorname{diag}(1,0,0,1)$. Therefore

$$
\operatorname{Tr}(\rho_{\mathrm{ind}}E_{\mathrm{same}})=\tfrac12,
\qquad
\operatorname{Tr}(\rho_{\mathrm{shared}}E_{\mathrm{same}})=1.
$$

The joint densities differ. The equivalence theorem is about equal states on the **same complete accessible system**, so it does not assert equality of different multi-trial models with only equal individual marginals. IID sampling needs its own preparation assumption, as in 6.6.

The last code reuses actual two-qubit component outputs for these classical joint sums. It then directly exercises the native density-matrix execution mode on a declared pure preparation.

```python
rho_independent = Rcomp
rho_shared_label = Rcorr
same_event = torch.diag(torch.tensor([1,0,0,1],dtype=torch.complex128))
e.close(torch.trace(rho_independent@same_event),.5)
e.close(torch.trace(rho_shared_label@same_event),1.)
for M in (rho_independent,rho_shared_label):
    e.close(M[0,0]+M[1,1],.5)  # first trial Z0
    e.close(M[0,0]+M[2,2],.5)  # second trial Z0
c = fq.Circuit(1,dtype=torch.complex128).h(0).p(0,.37)
r = fq.run(c,outputs=[fq.density_matrix(),fq.probabilities()],
           options=replace(OPTIONS,mode="density_matrix"))
e.RUNS += 1
v = e.qubit(math.pi/2,.37)
e.close(r.density_matrix[0],e.outer(v))
e.close(r.probabilities[0],[.5,.5])
print("Same one-trial density,distinct joint models:P(equal)=0.5or1.")
print("Native density_matrix mode returned the correct pure density and probabilities.")
print("Literal body native executions:",e.RUNS)
```

```text
Same one-trial density,distinct joint models:P(equal)=0.5or1.
Native density_matrix mode returned the correct pure density and probabilities.
Literal body native executions: 34
```

The support boundary is concrete:

| Operation in this section | Actual execution | Scope of the check |
|---|---|---|
| Full density output | fq.density_matrix request | Native pure-state matrices and ordered full-register selections |
| Statevector and density-matrix modes | ExecutionOptions mode | Both modes actually run on pure preparations |
| Ensemble matrix | Classical weighted sum of native component matrices | Deterministic finite classical mixture reference |
| General effect trace | Host matrix multiplication, plus selected native basis analyzers | No native general-POVM endpoint inferred |
| Arbitrary mixed initialization, noise, collapse or feedback | Not used here | No support or performance claim from these examples |

The public density request also accepts selected subsets according to its documented contract; this section exercises full and reversed full-register selections. The formal reduction operation and its independent validation belong to 8.4. The existence of density-matrix mode is not evidence that any guessed mixed-initializer signature, noisy instrument or hardware route works. This section neither passes ρ as a Circuit input nor invents an ensemble initializer.

### Complete-program verification

Run from the repository root:

```sh
python examples/foundations/statistical_ensembles.py
python scripts/check_statistical_ensembles_prose.py
```

The complete program executes 54 CPU complex128 circuits: twelve pure-state checks in the two modes; twenty complex analyzers; two nonorthogonal components; eight computational/Bell preparations; four joint classical-label components; and eight fixed or label-dependent transformations. It separately checks thirty-six classical effect/probe identities. Fourteen malformed contracts are rejected before another native run: invalid weights, empty or mismatched ensembles, unnormalized or wrong-dtype vectors, invalid density matrices/effects, and incompatible dimensions. Zero-weight entries are retained without division.

The book helpers enforce a finite two- or four-dimensional reference contract. That is a teaching bound, not a FlagQuantum limit. Numerical positivity accepts residuals within the stated tolerance and never clips eigenvalues, symmetrizes an input or normalizes invalid weights. Mathematical positivity and exact operational equality are established by the derivations, not by this numerical guard.

Expected output of the complete program:

```text
12native pure preparations:both modes return correct density matrices,probabilities and X/Y/Z expectations.
20native complex analyzers and20classical effect checks match scalar Born sums and trace probabilities.
2native nonorthogonal components reproduce the unequal-population spectral ensemble;offdiagonal phases cancel.
8native two-qubit preparations:computational/Bell ensembles and reversed density-axis order verified;16classical separating probes passed.
4native classical-label product preparations:equal unlabelled system states can have different labelled joint predictions.
8native fixed/label-dependent operations:fixed U preserves equivalence;accessible labels change the operational input.
14malformed contracts rejected before execution;zero weight retained;54CPUcomplex128native circuits passed.
Classical ensemble sums are not an arbitrary mixed-state initializer or a finite-data certificate of exact equality.
```

The preliminary native capability probe executed two circuits, one in each mode. The complete program, every literal body unit, the previous section's scoped regression and fresh transfer cases were then executed. No unexpected scientific example failure occurred. Native density matrices, probabilities and expectations were compared with independently indexed outer products and scalar Born sums; any tiny floating-point imaginary trace residual is retained and checked within tolerance, not silently repaired. Independent mathematical review, implementation review and reader trial remain pending.

### Understanding checks and transfer exercises

**8.1-A — Keep the conjugate.** Derive the four entries of ρ for ψ=(|0⟩+i|1⟩)/√2. Compute its X,Y,Z means from traces. Explain why replacing ψψ† with ψψᵀ fails the density conditions. Which global phases can be changed without altering an ensemble density?

**8.1-B — Fresh nonorthogonal preparation.** Use r=.61 and φ=−.72 in u±. Derive the common density of their half/half ensemble and the spectral ensemble with weights (.61,.39). Apply U=P(.33)Ry(−.94). Predict the transformed Z mean and the probabilities of computational outcomes. Verify both ensembles with native component matrices and compare the complete matrices, not only their diagonals.

**8.1-C — Match the accessible system.** For the equal Z and X preparations, compute p(label0,systemZ0), p(systemZ0), and the conditional zero probability given label0. Apply the host rule I for label0 and X for label1. Why does the resulting difference not contradict equality of their initial Q states? Then contrast two independently chosen Z labels with a shared label across two trials.

**8.1-D — Fresh two-qubit ensemble and a separating effect.** Let W=Ry(.47) on q1, then CX(q1,q0), then P(−.31) on q0. Compare the equal mixtures of W applied to the four computational states and W applied to the four Bell states. Derive their full density and the result in selected order (q1,q0). How many separating rank-one events does the proof use at d=4? Explain what measured agreement within sampling error can and cannot establish.

<details markdown="1">
<summary>Answers and verification guidance for 8.1-A–D</summary>

**A.** The density and means are

$$
\begin{gathered}
\rho=\frac12\begin{pmatrix}1&-i\\i&1\end{pmatrix},\\
(\langle X\rangle,\langle Y\rangle,\langle Z\rangle)=(0,1,0).
\end{gathered}
$$

Using the transpose without conjugation gives $\tfrac12\begin{pmatrix}1&i\\i&-1\end{pmatrix}$, which is not Hermitian and has trace zero. Each component may acquire its own global phase because it cancels inside that component's outer product; changing its relative coordinate phase is generally a different state.

**B.** Both densities equal diag(.61,.39). Their initial Z mean is .22 and their X,Y means vanish. Ry(−.94) rotates that initial diagonal state; the final P(.33) does not change a Z probability. Thus

$$
\begin{aligned}
\langle Z\rangle'&=.22\cos(.94),\\
p(0)&=\frac{1+.22\cos(.94)}2,\\
p(1)&=1-p(0).
\end{aligned}
$$

The complete output matrix is U diag(.61,.39)U†, whose off-diagonal entries need not vanish. Four fresh native component executions, two per representation, are included in transfer evidence. Using only the computational diagonal would miss a possible phase/conjugation error.

**C.** The joint label0/zero probabilities are 1/2 for Z and 1/4 for X. The system zero marginal is 1/2 for either, while the conditional zero probabilities given label0 are 1 and 1/2. The controlled rule accesses an additional record whose joint density differs; it produces |0⟩ for the Z preparation and I/2 for the X preparation. For two trials, both sources have single-trial I/2, but their equal-outcome probabilities are 1/2 and 1. These statements concern different accessible systems or different joint models.

**D.** The untransformed equal mixtures both give I₄/4. The same W acts on every component, so $W(I_4/4)W^\dagger=I_4/4$. Reversing the full-register order permutes both matrix indices and leaves this identity matrix unchanged. The transfer program executes all eight transformed components and checks both named density orderings against independent scalar gate action. The proof needs sixteen rank-one events: four basis vectors and two for each of the six coordinate pairs. These are mathematical event probabilities, not sixteen noiseless experimental facts. Finite estimated agreement supports a tolerance/statistical statement under its model; it cannot prove exact equality of unknown preparations.

</details>

**Sources.** The frozen [NC:2.4.1 locator](../references/proof-sources.md#source-nc-2-4-1) points to “Ensembles of quantum states,” beginning on printed page 99; it remains a contents-locator check, not a new full-text review. The author-hosted [Watrous, *The Theory of Quantum Information*, §2.1.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf#page=70), printed pages 62–64, was inspected for density-state and convex-mixture conventions. The finite trace and operational-equivalence derivations here are self-contained original prose; no source pages are redistributed. Section 8.2 takes up spectral representations and purity without treating an ensemble list as uniquely determined by its density.

<!-- end-section-8.1 -->

<span id="sec-density-matrices-reduced-states-and-purification-2"></span>

## 8.2 Pure states, mixed states, and purity

Does a preparation with two classical labels necessarily produce a mixed state? Does a diagonal density matrix necessarily describe classical uncertainty? Can a purity printed as 1.000000 establish that a state is pure? These questions concern different properties. We will distinguish the mathematical state from a particular ensemble representation and from a finite-precision report.

The frozen prerequisites are [8.1, statistical ensembles and density operators](#sec-density-matrices-reduced-states-and-purification-1), and [2.5, Hermitian spectra and singular values](ch-complex-vectors-operators-and-numerical-reasoning.md#sec-complex-vectors-operators-and-numerical-reasoning-5). This section has depth **F**. We prove the purity criterion from the finite Hermitian spectral theorem, including both directions and its assumptions; the code checks implementations of those formulas rather than replacing the proof.

Fix a nonzero finite-dimensional complex Hilbert space of dimension d, an orthonormal coordinate basis, and a density operator ρ: it is Hermitian, positive semidefinite and has trace one. All quantities here are dimensionless; native gate angles are radians. A **pure state** is an operator of the form ρ=|ψ⟩⟨ψ| for a normalized vector ψ. A **mixed state** is a density operator with no such single-vector representation. “Mixed” refers to the specified system's state, not a uniquely reconstructible story about how it was prepared. In particular, an ensemble list is a representation, not an additional intrinsic property of ρ.

The eight cumulative units below run from the repository root. The companion [state_purity.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/state_purity.py) contains the numerical contracts and complete checks. Native density matrices are obtained from actual preparations. Weighted mixtures, spectral decompositions and purity diagnostics are explicitly classical calculations on those outputs. Absolute tolerance is $10^{-12}$ with relative tolerance zero for deterministic comparisons; it is neither a physical calibration guarantee nor an exact rank certificate.

### 8.2.1 Complete the spectral description of a density operator

The spectral theorem supplies an orthonormal eigenbasis {|uᵢ⟩} and real eigenvalues λᵢ. Positivity, evaluated on uᵢ itself, gives λᵢ≥0. Trace invariance gives Σᵢλᵢ=1. Consequently

$$
\begin{aligned}
\rho&=\sum_{i=1}^{d}\lambda_i|u_i\rangle\langle u_i|,\\
\lambda_i&\geq0,\qquad\sum_i\lambda_i=1.
\end{aligned}
$$

This is a statistical ensemble of normalized vectors with classical weights λᵢ. Zero eigenvalues can be omitted. Conversely, 8.1 proved that every normalized nonnegative weighted sum of normalized outer products is a density operator. Thus the positive, unit-trace operator conditions characterize exactly the finite ensemble states. The eigenvectors are not uniquely determined inside a degenerate eigenspace, and this spectral ensemble is not the only possible ensemble.

For later use, orthonormality eliminates all cross factors in the operator product:

$$
\begin{aligned}
\rho^2&=\sum_{i,j}\lambda_i\lambda_j
 |u_i\rangle\langle u_i|u_j\rangle\langle u_j|\\
&=\sum_i\lambda_i^2|u_i\rangle\langle u_i|.
\end{aligned}
$$

Define the **purity** $\gamma(\rho)=\operatorname{Tr}(\rho^2)$. Taking the trace of this expansion gives $\gamma(\rho)=\sum_i\lambda_i^2$. This is the trace of the squared operator, not the square of its trace, which would always be one.

The following code visibly prepares one complex qubit and requests the released native density output in both supported execution modes. `spectral_check` uses `torch.linalg.eigh` and reconstructs the matrix from all computed eigenpairs without dropping small values. The mode name does not determine whether a physical state is mixed: both modes can describe this same pure preparation.

```python
import math
from dataclasses import replace
import torch
import flagquantum as fq
from examples.foundations import state_purity as p
from examples.foundations import statistical_ensembles as e
for mode in ('statevector','density_matrix'):
    c=fq.Circuit(1,dtype=p.D).RY(0,theta=1.13).P(0,theta=-.42)
    result=fq.run(c,outputs=[fq.density_matrix(),fq.probabilities()],
                  options=replace(e.OPTIONS,mode=mode))
    p.RUNS+=1
    a=result.density_matrix[0]
    v=e.qubit(1.13,-.42)
    e.close(a,e.outer(v))
    e.close(result.probabilities[0],v.abs().square())
    d=p.diagnostics(a)
    e.close(d['purity'],1)
    values,Q=p.spectral_check(a)
    print(mode+':purity=%.12f'%d['purity'])
```

```text
statevector:purity=1.000000000000
density_matrix:purity=1.000000000000
```

### 8.2.2 Prove the purity bounds and the pure-state criterion

Because 0≤λᵢ≤1, each λᵢ²≤λᵢ; summing gives γ≤1. More explicitly,

$$
1-\gamma(\rho)=\sum_i\lambda_i(1-\lambda_i)\geq0.
$$

Every summand is nonnegative, so equality holds exactly when every eigenvalue is either zero or one. Their sum is one, so exactly one is one. Therefore equality means rank one, and the spectral expansion is precisely |u⟩⟨u| for its unique occupied eigenvector ray. Conversely, if ρ=|ψ⟩⟨ψ| with ⟨ψ|ψ⟩=1, then ρ²=ρ and γ=Trρ=1. Finally, ρ²=ρ implies λᵢ²=λᵢ, and the same argument gives rank one. We have proved the complete equivalence

$$
\boxed{\begin{gathered}
\rho\text{ pure}\ \Longleftrightarrow\ \operatorname{rank}\rho=1\\
\Longleftrightarrow\ \rho^2=\rho
\ \Longleftrightarrow\ \gamma(\rho)=1.
\end{gathered}}
$$

The lower bound follows by completing a sum of squares rather than guessing the most mixed spectrum:

$$
\begin{aligned}
\sum_i\left(\lambda_i-\frac1d\right)^2
&=\gamma(\rho)-\frac1d\geq0,\\
\frac1d&\leq\gamma(\rho)\leq1.
\end{aligned}
$$

Equality on the left requires every λᵢ=1/d, hence ρ=I/d. At d=1 the two bounds coincide; the unique density operator is pure. For d>1, every mixed density has γ<1, although it may be arbitrarily close to one. Purity is not a probability of “being pure” on one trial.

A source choosing |0⟩ and |1⟩ with weights .73 and .27 gives diagonal entries equal to the eigenvalues. Native pure-component matrices supply the two terms; the weighted addition is performed on the host.

```python
a0,v0=p.native(0.,0.)
a1,v1=p.native(math.pi,0.)
rho,d=p.mixture((.73,.27),(v0,v1),(a0,a1))
e.close(rho,torch.diag(torch.tensor([.73,.27],dtype=p.D)))
e.close(torch.trace(rho@rho),d['purity'])
e.close(d['purity'],.73**2+.27**2)
print('eigenvalues:',[round(x,6) for x in d['eigenvalues'].tolist()])
print('purity=%.6f'%d['purity'])
```

```text
eigenvalues: [0.27, 0.73]
purity=0.605800
```

### 8.2.3 Several labels can still describe one pure ray

A normalized vector and its global-phase multiple define the same outer product. Therefore two positive ensemble weights do not by themselves imply mixedness. This is a mathematical property of a ray, not a cancellation between amplitudes from mutually exclusive classical labels.

There is also a useful coordinate formula. In any orthonormal basis, Hermiticity gives ρⱼᵢ=ρᵢⱼ* and therefore

$$
\begin{aligned}
\gamma(\rho)
&=\sum_i(\rho^2)_{ii}
 =\sum_{i,j}\rho_{ij}\rho_{ji}\\
&=\sum_{i,j}|\rho_{ij}|^2.
\end{aligned}
$$

Thus the squared Frobenius norm equals purity for a density operator. Keeping only diagonal terms loses coherence and is generally wrong. For ψ=(|0⟩+i|1⟩)/√2, the density has all four entry magnitudes 1/2, so the correct sum is one; its diagonal-only sum is 1/2. The diagonal matrix I/2 is a different state. “Diagonal” itself is basis dependent: every pure density is diagonal in an eigenbasis, with one occupied entry. It is not a mixed-state criterion.

```python
ap,vp=p.native(math.pi/2,math.pi/2)
phase=complex(math.cos(.61),math.sin(.61))
pure,dp=p.mixture((.2,.8),(vp,phase*vp),(ap,ap))
e.close(pure,ap)
diagonal_only=sum(abs(pure[i,i].item())**2 for i in range(2))
print('two positive labels,one ray:purity=%.6f'%dp['purity'])
print('diagonal-only sum=%.6f;offdiagonal coherence must be retained'%diagonal_only)
```

```text
two positive labels,one ray:purity=1.000000
diagonal-only sum=0.500000;offdiagonal coherence must be retained
```

### 8.2.4 Derive purity directly from an arbitrary ensemble

Let ρ=Σⱼpⱼ|ψⱼ⟩⟨ψⱼ|. Multiply this expression without assuming the components are orthogonal. For each pair, the trace of the outer product closes its two scalar overlaps:

$$
\begin{aligned}
\operatorname{Tr}\bigl(
 |\psi_j\rangle\langle\psi_j|
 |\psi_k\rangle\langle\psi_k|\bigr)
&=|\langle\psi_j|\psi_k\rangle|^2,\\
\gamma(\rho)
&=\sum_{j,k}p_jp_k
 |\langle\psi_j|\psi_k\rangle|^2.
\end{aligned}
$$

Normalized vectors have squared overlap at most one. To see its equality condition explicitly, put c=⟨ψⱼ|ψₖ⟩ and w=ψₖ−cψⱼ. Then ⟨ψⱼ|w⟩=0 and ||w||²=1−|c|². Equality |c|²=1 means w=0, so the vectors differ only by a global phase. Since Σⱼₖpⱼpₖ=1,

$$
1-\gamma(\rho)=\sum_{j,k}p_jp_k
 \left(1-|\langle\psi_j|\psi_k\rangle|^2\right).
$$

Every term is nonnegative. Consequently an ensemble represents a pure density exactly when **all positive-weight components belong to one ray**. If γ=1, each positive-weight pair must saturate the overlap bound; picking any positive-weight component identifies the common ray. Conversely, a common ray makes every such overlap one, so the sum is one. Zero-weight vectors impose no condition on that ray. This proves why counting labels or merely noticing nonorthogonal components is insufficient.

For two components u,v with weights p,1−p, the general formula reduces to

$$
\gamma=p^2+(1-p)^2+2p(1-p)|\langle u|v\rangle|^2.
$$

For 0<p<1 it equals one only for the same ray. The example below compares this scalar-overlap reference with three matrix-based calculations. The scalar expression never diagonalizes or multiplies the density matrix.

```python
au,u=p.native(.91,.37)
av,v=p.native(1.57,-.62)
rho,d=p.mixture((.28,.72),(u,v),(au,av))
overlap=abs(sum(x.item().conjugate()*y.item() for x,y in zip(u,v)))**2
expected=.28**2+.72**2+2*.28*.72*overlap
e.close(torch.trace(rho@rho),expected)
e.close(d['purity'],expected)
print('squared overlap=%.9f'%overlap)
print('trace/entries/spectrum/ensemble purity=%.9f'%d['purity'])
```

```text
squared overlap=0.716840651
trace/entries/spectrum/ensemble purity=0.885830150
```

### 8.2.5 Distinguish a projector from a normalized mixed state

Let Π be an orthogonal projector of rank r≥1. Choose an orthonormal basis of its range; then Π is the sum of those r rank-one projectors and TrΠ=r. Its normalized density is ρ=Π/r. Hence

$$
\rho^2=\frac{\Pi}{r^2},\qquad
\gamma(\rho)=\frac1r.
$$

For r>1 this is mixed, even though Π itself is idempotent. A rank-r projector is not a unit-trace density unless r=1. The earlier equivalences were explicitly about density operators; dropping their assumptions changes the result.

More generally, if a density has exactly r positive eigenvalues, the same sum-of-squares proof on just those eigenvalues gives γ≥1/r, with equality exactly for ρ=Π/r on its occupied subspace. This statement does not make numerical threshold rank into an exact physical rank. The d-dimensional maximally mixed state corresponds to r=d; a uniform mixture on a smaller subspace is not I/d.

Here the two-qubit basis index is 2q0+q1. We request four native full-register density matrices and build rank-1,2,3,4 uniform ensembles from their initial subsets. No partial trace or guessed mixed-state initializer is used.

```python
basis=tuple(torch.eye(4,dtype=p.D));matrices=[]
for index in range(4):
    c=fq.Circuit(2,dtype=p.D)
    if index&2:c.X(0)
    if index&1:c.X(1)
    result=fq.run(c,outputs=[fq.density_matrix()],options=e.OPTIONS)
    p.RUNS+=1
    matrices.append(result.density_matrix[0])
for rank in (1,2,3,4):
    flat,fd=p.mixture((1/rank,)*rank,basis[:rank],tuple(matrices[:rank]))
    e.close(fd['purity'],1/rank)
    print('rank%d:purity=%.9f'%(rank,fd['purity']))
```

```text
rank1:purity=1.000000000
rank2:purity=0.500000000
rank3:purity=0.333333333
rank4:purity=0.250000000
```

### 8.2.6 A fixed unitary preserves purity

For a fixed unitary U acting on every component, 8.1 gives ρ′=UρU†. Multiplication and U†U=I imply (ρ′)²=Uρ²U†. Trace cyclicity then gives

$$
\gamma(\rho')
=\operatorname{Tr}(U\rho^2U^\dagger)
=\operatorname{Tr}(\rho^2)=\gamma(\rho).
$$

The eigenvectors change to Uuᵢ while eigenvalues are unchanged. This proof applies equally to an active fixed unitary and to the corresponding unitary coordinate similarity, although those have different physical interpretations. It does not assert invariance under outcome-dependent processing or discarding systems; partial trace and local/global purity are developed in 8.4 and later sections.

Below, two native circuits apply the same U to the actual component preparations. The resulting host mixture is compared with UρU† in its entirety, including off-diagonal phases. `unitary` takes integer qubit arguments and the matrix as the `unitary=` keyword; this is the actual released call signature.

```python
U=e.prepare(e.qubit(.47,-.82));after=[]
for component in (u,v):
    c=fq.Circuit(1,dtype=p.D).unitary(0,unitary=e.prepare(component))
    c.unitary(0,unitary=U)
    result=fq.run(c,outputs=[fq.density_matrix()],options=e.OPTIONS)
    p.RUNS+=1
    after.append(result.density_matrix[0])
rotated,rd=p.mixture((.28,.72),(U@u,U@v),tuple(after))
e.close(rotated,U@rho@U.mH)
e.close(rd['purity'],d['purity'])
print('before=%.9f,after=%.9f'%(d['purity'],rd['purity']))
```

```text
before=0.885830150,after=0.885830150
```

### 8.2.7 Read the single-qubit criterion without losing complex phase

Write a Hermitian, unit-trace qubit matrix as

$$
\rho=\begin{pmatrix}a&z\\z^*&1-a\end{pmatrix},
\qquad a\in\mathbb R,\ z\in\mathbb C.
$$

Positivity requires 0≤a≤1. The eigenvalue product is the determinant a(1−a)−|z|², so positivity also requires |z|²≤a(1−a). Conversely these conditions imply positivity: the two real eigenvalues sum to one and have nonnegative product, so neither can be negative. Thus these conditions are necessary and sufficient. Directly summing the four entry magnitudes gives

$$
\begin{aligned}
\gamma&=a^2+(1-a)^2+2|z|^2,\\
1-\gamma&=2\bigl(a(1-a)-|z|^2\bigr).
\end{aligned}
$$

Within the valid density domain, the equality |z|²=a(1−a) is exactly the pure-state boundary, including the poles a=0,1 with z=0.

To connect with qubit coordinates, use the explicit Pauli matrices of 6.3. Expanding (I+xX+yY+z_B Z)/2 entry by entry gives a=(1+z_B)/2 and ρ₀₁=(x−iy)/2. Therefore x=2Re z, y=−2Im z and z_B=2a−1. Substitution, including the factor of two for the conjugate off-diagonal pair, yields

$$
\begin{aligned}
\gamma&=\frac{1+x^2+y^2+z_B^2}{2},\\
\rho\geq0&\ \Longleftrightarrow\ x^2+y^2+z_B^2\leq1.
\end{aligned}
$$

Unit length means pure; an interior point means mixed. The previously derived pure-qubit sphere is the boundary, not the full mixed-qubit state space. The minus sign in y matters for representing the matrix even though its square hides that sign in this one scalar diagnostic. Purity agreement alone does not verify a whole density matrix.

```python
population=rho[0,0].real.item();z=rho[0,1].item()
x=2*z.real;y=-2*z.imag;zz=2*population-1
entry_formula=population**2+(1-population)**2+2*abs(z)**2
bloch_formula=(1+x*x+y*y+zz*zz)/2
e.close(entry_formula,d['purity']);e.close(bloch_formula,d['purity'])
assert abs(z)**2<=population*(1-population)+p.ATOL
print('entry formula=%.9f,Bloch formula=%.9f'%(entry_formula,bloch_formula))
```

```text
entry formula=0.885830150,Bloch formula=0.885830150
```

### 8.2.8 Separate exact criteria from finite-precision diagnosis

For the exact family ρₑ=diag(1−ε,ε), with 0<ε<1,

$$
\gamma(\rho_\varepsilon)
=1-2\varepsilon+2\varepsilon^2<1.
$$

Every member is mixed, however small ε is. A tolerance-based comparison with one cannot decide exact rank. At ε=10⁻²⁰, double precision rounds 1−ε to one and the computed trace square to one while still representing a positive second diagonal entry. The numerical report describes a rounded matrix within the stated tolerance; it cannot certify the exact rank of the intended state. We retain all computed eigenvalues, report the idempotence residual and minimum eigenvalue, and never return an exact `pure` label from an `allclose` result.

The matrix domain must also be checked first. For example, diag(2/3,2/3,−1/3,0) is Hermitian with trace one and trace square one, but it is not positive. The non-Hermitian matrix [[1,1],[0,0]] is idempotent and has trace one, but is not a density operator either. These do not contradict the theorem because they violate its assumptions. Our helpers reject these cases before interpreting a purity. They also reject bad dimensions, dtype, nonfinite data and malformed weights. The dimension-2-or-4 guard bounds this teaching example; it is not a FlagQuantum dimension limit.

```python
eps=1e-8
near=torch.diag(torch.tensor([1-eps,eps],dtype=p.D))
nd=p.diagnostics(near)
e.close(nd['purity'],1-2*eps+2*eps**2)
tiny=torch.diag(torch.tensor([1-1e-20,1e-20],dtype=p.D))
td=p.diagnostics(tiny)
assert td['purity']==1.0 and td['minimum_eigenvalue']>0
print('epsilon1e-8:purity=%.12f'%nd['purity'])
print('epsilon1e-20:rounded purity1 with positive second eigenvalue;no exact label inferred')
print('%dmalformed contracts rejected'%p.rejected())
print('%dnative body circuits;mixtures and diagnostics are host calculations'%p.RUNS)
```

```text
epsilon1e-8:purity=0.999999980000
epsilon1e-20:rounded purity1 with positive second eigenvalue;no exact label inferred
10malformed contracts rejected
13native body circuits;mixtures and diagnostics are host calculations
```

**Implementation support and limits.** Released FlagQuantum 0.3.1 actually returns full native density matrices through `fq.density_matrix()` and executes the tested preparations in both `statevector` and `density_matrix` modes. `fq.probabilities()` supplies the accompanying computational probabilities. The eight units show direct circuit gates, `fq.run`, and result access; the complete program additionally uses native Bell preparations. The purity trace, entry sums, spectra and ensemble additions here are host PyTorch/Python operations, not a claimed native purity measurement request. We neither initialize an arbitrary mixed matrix through an unverified signature nor invoke noise or a measurement-based purity experiment. This is exact simulator output with floating-point arithmetic, not tomography from finite shots, hardware certification, a collapse interface or an interval error certificate. No clipping, symmetrization, input normalization repair or global-phase alignment is used to obtain agreement.

Expected output of the complete program:

```text
24native pure outputs:both modes,one/two qubits;purity1 and spectral reconstruction passed.
12ensembles:trace-square,entry norm,spectrum and scalar overlap agree;zero weights and duplicate rays retained.
Four native Bell components:uniform rank-r mixtures have purity1/r for r=1,2,3,4.
Unitary invariance and near-pure diagnostics passed;rounded purity1 is not an exact rank-one certificate.
10malformed contracts rejected;no clipping,normalization repair or exact numerical purity labels.
40actual native circuits;host mixture algebra is recorded separately.
```

The complete program makes 40 actual native circuit executions. Its 12 two-component mixture cases and four rank-r mixtures are classical computations from component outputs; they are not additional quantum executions. The literal body makes 13 separate executions. The execution ledger records those runs, the body/complete regression and fresh transfer cases separately. The finite tests cannot establish a theorem for all dimensions; the spectral and nonnegative-sum arguments above do that work.

### Understanding checks and transfer exercises

**8.2-A — Check assumptions before using a scalar.** Explain why the two invalid matrices in 8.2.8 evade an unqualified “trace square one” test. For an orthogonal projector Π of rank 3, compare TrΠ² with the purity of Π/3. Which operator is a density?

**8.2-B — Fresh complex ensemble.** Prepare u=qubit(.63,−.81) and v=qubit(1.84,.27), with weights (.37,.63), using the same qubit(θ,φ) convention as the code. Derive purity from scalar overlaps; verify the trace, entry and eigenvalue formulas against actual native component matrices. Apply the fixed U=prepare(qubit(−.52,.46)) to both components and verify invariance. Is comparing just the two diagonal probabilities sufficient to verify equality of two densities?

**8.2-C — More labels, or more occupied rays?** Use weights (.2,.3,.5) and vectors (u,e^{i.4}u,e^{−i.7}u). Show the state is pure. Replace the last component by a normalized vector w orthogonal to u; find its purity and eigenvalues. Add a zero-weight unrelated vector and explain why the answer is unchanged.

**8.2-D — Resolve a near-pure report.** For ε=10⁻⁷, calculate the purity and the Frobenius distance from ρₑ to |0⟩⟨0|. If a report rounds the purity to six decimal places, may it call the state pure? Compare with a two-qubit uniform density supported on three orthonormal native Bell preparations. State what remains unproved by a floating-point PSD check.

<details markdown="1">
<summary>Answers and verification guidance for 8.2-A–D</summary>

**A.** The first invalid matrix has a negative eigenvalue; the second violates Hermiticity. The theorem requires both, as well as trace one. Π has TrΠ²=3 and trace 3, whereas Π/3 has trace one and purity 1/3. Only Π/3 is a density operator. For rank one both coincide.

**B.** Put c=cos(.63/2)cos(1.84/2)+e^{i( .27+.81 )}sin(.63/2)sin(1.84/2). Then

$$
\gamma=.37^2+.63^2+2(.37)(.63)|c|^2.
$$

The complete matrix transforms as UρU† and the proof gives the same purity. The fresh transfer program evaluates the displayed scalar expression and the full matrix against native outputs. Diagonals alone omit complex off-diagonal information; for example I/2 and |+⟩⟨+| have the same computational probabilities but different purity.

**C.** All original positive-weight components are the same ray, so ρ=|u⟩⟨u| and γ=1. After replacement, the total weight on u is .5 and the weight on w is .5. Thus its occupied eigenvalues are (.5,.5) and γ=.5. A zero-weight vector contributes nothing; its ray need not match either occupied component.

**D.** The exact values are

$$
\begin{aligned}
\gamma&=1-2(10^{-7})+2(10^{-14}),\\
\|\rho_\varepsilon-|0\rangle\langle0|\|_F
&=\sqrt2\,10^{-7}.
\end{aligned}
$$

This state is mixed despite the rounded display. The three-state uniform two-qubit ensemble has spectrum (1/3,1/3,1/3,0), purity 1/3, and a different ambient dimension. A numerical PSD check and residuals give finite-precision diagnostics, not a rigorous enclosure of unknown physical eigenvalues or exact rank. An experimental assertion would also need a declared measurement model, statistical uncertainty and systematic-error budget.

</details>

**Sources and proof scope.** The frozen source locator is NC §2.4.2, printed page 101 (contents locator checked; no new claim of full-text NC review). For pure-ray and spectral-ensemble conventions we consulted [Watrous, author-hosted manuscript §2.1.2, printed page 64](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf#page=72). The bounds, ensemble overlap criterion, rank-r extension and coordinate derivations above are supplied explicitly in this section. Independent mathematical review, implementation review and reader trial remain pending; this is an author-verified draft, not formal acceptance.

<!-- end-section-8.2 -->

<span id="sec-density-matrices-reduced-states-and-purification-3"></span>

## 8.3 Expectation values and measurement updates

The density operator predicts both probabilities and means, but a probability distribution alone does not specify what happens to the system after a measurement. Moreover, “the result was r” and “a measurement occurred but its result is unavailable” describe different information. We will construct the corresponding density operators, prove their normalization, and compare their predictions for a later measurement.

The frozen prerequisites are [8.1, density operators](#sec-density-matrices-reduced-states-and-purification-1), [6.2, conditional states and ignored outcomes](ch-measurement-expectation-values-and-statistical-estimation.md#sec-measurement-expectation-values-and-statistical-estimation-2), and [6.3, spectra and expectations](ch-measurement-expectation-values-and-statistical-estimation.md#sec-measurement-expectation-values-and-statistical-estimation-3). This section has depth **F**. The finite-sum proofs below establish the density update for a specified complete instrument; numerical examples check the implementation rather than establish the theorem.

All spaces are finite and nonzero. The input ρ is Hermitian, positive semidefinite and has trace one. An observable A is Hermitian. A measurement process must specify its update operators as well as its reported labels. The physical update model is an assumption, additional to the Born probability rule. We do not derive disturbance from outcome probabilities alone. The examples use dimensionless observables and probabilities; gate angles are radians. If A has physical units, its expectation has the same units.

Run the eight cumulative units from the repository root with the pinned example requirements. The companion [density_updates.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/density_updates.py) supplies contracts and complete checks. Actual released FlagQuantum 0.3.1 density/probability/Pauli outputs are used explicitly. Mixture formation and conditional density updates are labelled as host calculations. Deterministic comparisons use absolute tolerance $10^{-12}$ and relative tolerance zero, without phase alignment, input repair or probability clipping.

### 8.3.1 Derive the density expectation, not just the outcome probability

A positive, unit-trace operator need not arrive with a preparation list. The finite Hermitian spectral theorem used in 6.3 supplies an orthonormal eigenbasis. Each eigenvalue equals the quadratic form of ρ on its normalized eigenvector and is therefore nonnegative; their sum is the trace, one. These eigenvectors and eigenvalues provide a finite normalized ensemble for any input allowed here.

Write an input ensemble as ρ=Σⱼwⱼ|ψⱼ⟩⟨ψⱼ| with normalized ψⱼ, wⱼ≥0 and Σⱼwⱼ=1. For one component, the spectral expectation rule of 6.3 gives ⟨ψⱼ|A|ψⱼ⟩. Averaging the classical alternatives and using the trace identity from 8.1 gives

$$
\begin{aligned}
\langle A\rangle_\rho
&=\sum_j w_j\langle\psi_j|A|\psi_j\rangle\\
&=\operatorname{Tr}\!\left(
 A\sum_jw_j|\psi_j\rangle\langle\psi_j|\right)\\
&=\operatorname{Tr}(\rho A).
\end{aligned}
$$

This is independent of the chosen ensemble because it depends only on ρ. To connect it with an actual observable distribution, let A=ΣₐaPₐ be its spectral decomposition with distinct real eigenvalues a and orthogonal projectors Pₐ summing to I. The projective Born probabilities are p(a)=Tr(ρPₐ), so

$$
\langle A\rangle_\rho
=\sum_a a\,p(a).
$$

Each p(a) is real and nonnegative: the ensemble expression is a sum of wⱼ||Pₐψⱼ||². Their sum is one because the projectors are complete. Thus the expectation is real and lies between the smallest and largest eigenvalues. Real linearity in A follows directly from the trace; it does not assert that noncommuting observables have jointly available outcomes on one trial. The mean alone also does not determine the complete distribution or its measurement update.

Use the convention qubit(θ,φ)=cos(θ/2)|0⟩+e^{iφ}sin(θ/2)|1⟩ from 8.1. For a concrete complex mixed qubit, we use weights (.34,.66) and A=.7X−.2Y+1.3Z. The native observable sum, direct vector quadratics, density trace and numerical spectral probabilities are checked separately. Native matrices come from the two component preparations; the weighted density is assembled classically.

```python
import math
import torch
import flagquantum as fq
from examples.foundations import density_updates as d
from examples.foundations import statistical_ensembles as e
weights=(.34,.66)
u=e.qubit(.83,-.49);v=e.qubit(1.31,.72)
components=(u,v);matrices=[];native_means=[]
for component in components:
    c=fq.Circuit(1,dtype=d.D).unitary(0,unitary=e.prepare(component))
    result=fq.run(c,outputs=[fq.density_matrix(),fq.probabilities(),
        fq.expectation(.7*fq.X(0)-.2*fq.Y(0)+1.3*fq.Z(0),name='h')],options=e.OPTIONS)
    d.RUNS+=1
    matrices.append(result.density_matrix[0]);native_means.append(result.expectation('h')[0])
    e.close(result.probabilities[0],component.abs().square())
rho=sum(w*a for w,a in zip(weights,matrices))
trace_mean=torch.trace(rho@d.H).real.item()
scalar_mean=sum(w*torch.vdot(c,d.H@c).real.item() for w,c in zip(weights,components))
values,Q=torch.linalg.eigh(d.H)
spectral_mean=sum(values[j].item()*torch.trace(rho@e.outer(Q[:,j])).real.item() for j in range(2))
e.close(trace_mean,scalar_mean);e.close(trace_mean,spectral_mean)
e.close(trace_mean,sum(w*a for w,a in zip(weights,native_means)))
print('H expectation:trace/spectrum/ensemble/native=%.9f'%trace_mean)
```

```text
H expectation:trace/spectrum/ensemble/native=0.949601734
```

### 8.3.2 Select one ideal projective result and normalize only that branch

For an ideal projective measurement with a complete orthogonal family {Pᵣ}, the physical update assumption is the Lüders rule. For a pure input, its unnormalized branch vector is Pᵣψ. For a density input, define

$$
\begin{aligned}
\sigma_r&=P_r\rho P_r,\\
p_r&=\operatorname{Tr}(\sigma_r)
 =\operatorname{Tr}(\rho P_r),\\
\rho_r&=\frac{\sigma_r}{p_r}\quad(p_r>0).
\end{aligned}
$$

Here σᵣ includes the probability weight; ρᵣ is the conditional density given that r was observed. These are different objects. Since σᵣ=Σⱼwⱼ|Pᵣψⱼ⟩⟨Pᵣψⱼ|, it is Hermitian and positive. Its trace is Σⱼwⱼ||Pᵣψⱼ||²=pᵣ. For pᵣ>0, division by this one scalar preserves positivity and gives trace one. If pᵣ=0, all positive-weight projected vectors vanish, hence σᵣ=0 and there is no conditional state to normalize. The implementation returns `None` for an exactly impossible branch; it never chooses an arbitrary replacement vector.

For projectors the conditional state remains in the recorded subspace: PᵣρᵣPᵣ=ρᵣ. A repeated identical ideal projective measurement therefore returns r with probability one. This repeatability statement is specific to that update model, not a consequence of the POVM probabilities alone.

For a one-qubit Z measurement, P₀=|0⟩⟨0| and P₁=|1⟩⟨1|. Both positive-probability conditional states are the corresponding basis densities. The code below also prepares those states in **new** native circuits as an independent output check. Preparing a branch in a fresh circuit does not mean the original native circuit sampled or collapsed into it.

```python
probs,states,sigmas,ignored=d.instrument(rho,d.Z_GROUPS)
branch_native=[]
for r,P in enumerate((d.P0,d.P1)):
    sigma=P@rho@P
    e.close(sigmas[r],sigma);e.close(states[r],sigma/torch.trace(sigma))
    c=fq.Circuit(1,dtype=d.D)
    if r:c.X(0)
    result=fq.run(c,outputs=[fq.density_matrix(),fq.expectation(fq.X(0),name='x')],options=e.OPTIONS)
    d.RUNS+=1;branch_native.append(result)
    e.close(result.density_matrix[0],states[r])
e.close(sum(p*a for p,a in zip(probs,states)),ignored)
assert not torch.allclose((states[0]+states[1])/2,ignored,atol=d.ATOL,rtol=0)
print('Z outcome probabilities:',[round(p,9) for p in probs])
print('Fresh branch preparations agree;unweighted averaging gives a different state')
```

```text
Z outcome probabilities: [0.69981939, 0.30018061]
Fresh branch preparations agree;unweighted averaging gives a different state
```

### 8.3.3 Ignore the result by summing unnormalized branches

If the measurement occurred but its record is unavailable, the state must average the alternatives with their actual probabilities:

$$
\begin{aligned}
\rho_{\mathrm{out}}
&=\sum_{r:p_r>0}p_r\rho_r\\
&=\sum_r\sigma_r
 =\sum_rP_r\rho P_r.
\end{aligned}
$$

The first equality is a classical mixture of conditional states. The second follows by cancellation of each branch's normalization; zero branches contribute zero. Hermiticity and positivity are preserved by the sum. Its trace is Σᵣpᵣ=Tr(ρΣᵣPᵣ)=1, so it is again a density operator. Generally it differs from the input. In particular, completeness does not permit replacing ΣᵣPᵣρPᵣ by (ΣᵣPᵣ)ρ(ΣₛPₛ): the latter includes cross terms r≠s that the unread record has removed.

For any later observable B, linearity gives

$$
\langle B\rangle_{\mathrm{out}}
=\sum_{r:p_r>0}p_r\langle B\rangle_{\rho_r}.
$$

This is a weighted average of density predictions, not an unweighted average of branches and not a coherent sum of their statevectors. For |+⟩, a Z measurement has probabilities (.5,.5). Ignoring its result gives I/2: its X mean is zero. Leaving the system unmeasured preserves |+⟩ and X mean one. Normalizing the vector sum of |0⟩ and |1⟩ would incorrectly restore |+⟩. The computational Z probabilities happen to agree before and after, so checking only that distribution would miss the disturbance.

```python
plus=torch.tensor([1,1],dtype=d.D)/math.sqrt(2)
plus_result=d.native(plus)
plus_rho=plus_result.density_matrix[0]
pp,ss,uu,forgotten=d.instrument(plus_rho,d.Z_GROUPS)
before=plus_result.expectation('x')[0].item();after=d.mean(forgotten,d.X)
e.close(after,sum(p*r.expectation('x')[0] for p,r in zip(pp,branch_native)))
wrong_vector=torch.tensor([1,1],dtype=d.D)/math.sqrt(2)
print('X mean:unperformed=%.6f,performed/result ignored=%.6f'%(before,after))
print('Normalized branch-vector average predicts X=%.6f and is wrong'%d.mean(e.outer(wrong_vector),d.X))
```

```text
X mean:unperformed=1.000000,performed/result ignored=0.000000
Normalized branch-vector average predicts X=1.000000 and is wrong
```

### 8.3.4 Give the complete instrument, then derive its mixed-input update

Projective Lüders measurements are one model. More generally, assume a **specified finite instrument** is given by operators Kᵣα, where r is the reported outcome and α indexes alternatives not distinguished within that outcome. All operators have one common input space and one common output space. They obey the completeness condition

$$
\sum_{r,\alpha}K_{r\alpha}^\dagger K_{r\alpha}=I.
$$

For a pure input, the model assigns an unnormalized vector Kᵣαψ to each fine alternative, with squared norm as its probability. This is the physical process assumption; it must be supplied or justified for the apparatus. We are not proving that every conceivable operation has this representation. The general representation and composition theory is developed in Chapter 9.

For a mixed input ensemble, the unnormalized contribution of fine alternative (j,r,α) is wⱼ|Kᵣαψⱼ⟩⟨Kᵣαψⱼ|. Sum over the inaccessible initial label j and internal label α while holding the reported label r fixed. Finite distributivity gives

$$
\begin{aligned}
\sigma_r
&=\sum_{j,\alpha}w_j
 |K_{r\alpha}\psi_j\rangle\langle K_{r\alpha}\psi_j|\\
&=\sum_\alpha K_{r\alpha}\rho K_{r\alpha}^\dagger,\\
E_r&=\sum_\alpha K_{r\alpha}^\dagger K_{r\alpha},\\
p_r&=\operatorname{Tr}(\sigma_r)
 =\operatorname{Tr}(\rho E_r).
\end{aligned}
$$

Each effect Eᵣ is positive, since x†Eᵣx=Σα||Kᵣαx||²≥0, and completeness gives ΣᵣEᵣ=I. These effects form the POVM, which determines outcome probabilities. They need not be orthogonal projectors. Cyclicity of the trace establishes the displayed probability identity, including rectangular input/output operators.

For any output vector y,

$$
y^\dagger\sigma_r y
=\sum_\alpha(K_{r\alpha}^\dagger y)^\dagger
 \rho(K_{r\alpha}^\dagger y)\geq0.
$$

The expression also shows Hermiticity. Its trace is nonnegative and Σᵣpᵣ=Trρ=1. If pᵣ=0, the earlier ensemble formula is a sum of nonnegative weighted squared norms, so every positive-weight branch vector vanishes and σᵣ=0. If pᵣ>0, ρᵣ=σᵣ/pᵣ is a normalized density. Finally,

$$
\boxed{\begin{aligned}
\rho_r&=\sigma_r/p_r\quad(p_r>0),\\
\rho_{\mathrm{out}}&=\sum_r\sigma_r.
\end{aligned}}
$$

These equations prove both selective and nonselective normalization. They also prove ensemble independence of the entire update, not merely of its probabilities. The unnormalized σᵣ is linear in ρ; normalization usually makes the conditional map nonlinear. In ensemble language, conditioning changes the weights: for a single operator per outcome, an initial component j with q(r|j)>0 receives weight wⱼq(r|j)/pᵣ, not its original wⱼ. This follows directly by dividing its contribution by pᵣ. With several α, the corresponding fine weights are wⱼ||Kᵣαψⱼ||²/pᵣ.

For an explicit counterexample to determining updates from the POVM, let 0≤κ≤1 and set a=√((1+κ)/2), b=√((1−κ)/2). Use

$$
\begin{aligned}
M_0&=\operatorname{diag}(a,b),\\
M_1&=\operatorname{diag}(b,a),\\
N_0&=M_0,\qquad N_1=XM_1.
\end{aligned}
$$

Both models have E₀=(I+κZ)/2 and E₁=(I−κZ)/2 because X†X=I, but their record-1 conditional states obey ρ₁ᴺ=Xρ₁ᴹX. In particular their conditional Z means have opposite signs. At κ=0 the ordinary model leaves the state unchanged within either branch, whereas the second applies X in one branch. At κ=1 the ordinary model is ideal Z measurement. Thus equal effects determine equal record statistics for every input but do not guarantee equal later states.

The native verification uses system q0 and a meter q1 initially |0⟩. Here RY(g) has matrix [[cos(g/2),−sin(g/2)],[sin(g/2),cos(g/2)]], and controlled-RY applies that rotation to q1 only when q0 is one. For g₀=2 arccos a and g₁=2 arccos b, RY(g₀) on the meter followed by controlled-RY(g₁−g₀) gives, respectively, a|0⟩+b|1⟩ when the system is zero and b|0⟩+a|1⟩ when it is one. Therefore the full joint vector is

$$
|\Psi\rangle
 =M_0|\psi\rangle|0\rangle
  +M_1|\psi\rangle|1\rangle.
$$

A subsequent CX controlled by the meter implements the N model coherently. It is not a native classical feedback call. In full basis order (q0,q1), the entries with a fixed meter r have indices (r,2+r). The corresponding 2×2 diagonal block of the native joint density equals Mᵣ|ψ⟩⟨ψ|Mᵣ†, or its N counterpart. Summing the actual component outputs with weights gives the mixed-input σᵣ. This direct coordinate verification uses no unintroduced general partial-trace theorem; 8.4 supplies that construction.

```python
strength=.6
a=math.sqrt((1+strength)/2);b=math.sqrt((1-strength)/2)
outputs=[]
for flip in (False,True):
    joint_matrices=[];record_probs=[];native_z=[]
    for component in components:
        c=fq.Circuit(2,dtype=d.D).unitary(0,unitary=e.prepare(component))
        c.RY(1,theta=2*math.acos(a)).CRY(0,1,theta=2*math.acos(b)-2*math.acos(a))
        if flip:c.CX(1,0)
        result=fq.run(c,outputs=[fq.density_matrix(),fq.probabilities(qubits=(1,),name='record'),
            fq.expectation(fq.Z(0),name='z')],options=e.OPTIONS)
        d.RUNS+=1
        joint_matrices.append(result.density_matrix[0])
        record_probs.append(result.measurement('record').value[0])
        native_z.append(result.expectation('z')[0])
    groups=d.weak(strength,flip)
    p,s,unnormalized,total=d.instrument(rho,groups)
    joint=sum(w*m for w,m in zip(weights,joint_matrices))
    for r in range(2):
        idx=torch.tensor([r,2+r]);block=joint[idx][:,idx]
        explicit=groups[r][0]@rho@groups[r][0].mH
        e.close(block,explicit);e.close(unnormalized[r],explicit)
    e.close(torch.tensor(p,dtype=torch.float64),sum(w*p0 for w,p0 in zip(weights,record_probs)))
    e.close(d.mean(total,d.Z),sum(w*z0 for w,z0 in zip(weights,native_z)))
    outputs.append((p,s,total))
e.close(outputs[0][0],outputs[1][0])
z0=d.mean(outputs[0][1][1],d.Z);z1=d.mean(outputs[1][1][1],d.Z)
e.close(z0,-z1)
print('Identical POVM probabilities:',[round(x,9) for x in outputs[0][0]])
print('Conditional Z at record1:ordinary=%.9f,flipped=%.9f'%(z0,z1))
```

```text
Identical POVM probabilities: [0.619891634, 0.380108366]
Conditional Z at record1:ordinary=-0.263558025,flipped=0.263558025
```

### 8.3.5 An observed label need not specify a pure branch

Suppose a single reported outcome r has two internal operators Kᵣ₀=P₀ and Kᵣ₁=P₁. Its effect is I, so its reported probability is one. For |+⟩ input, however,

$$
\begin{aligned}
\rho_r&=P_0|+\rangle\langle+|P_0
       +P_1|+\rangle\langle+|P_1\\
&=\frac12|0\rangle\langle0|
 +\frac12|1\rangle\langle1|.
\end{aligned}
$$

Thus even knowing the only visible outcome does not make the system pure. Compare this with the single operator K=I: its effect is also I, but its output remains |+⟩⟨+|. The internal alternatives are summed as operators, not as vectors. Replacing the two internal operators by their coherent sum P₀+P₁=I would create a different physical process.

Conversely, different internal operator lists can describe the **same** instrument. For each fixed r, let V be a unitary mixing matrix on its finite internal labels and set Lᵣβ=ΣαVβαKᵣα. Expand the update:

$$
\begin{aligned}
\sum_\beta L_{r\beta}\rho L_{r\beta}^\dagger
&=\sum_{\alpha,\eta}
 \left(\sum_\beta V_{\beta\alpha}V_{\beta\eta}^*\right)
 K_{r\alpha}\rho K_{r\eta}^\dagger\\
&=\sum_\alpha K_{r\alpha}\rho K_{r\alpha}^\dagger.
\end{aligned}
$$

Unitarity makes the parenthesized sum δαη. Hence the unnormalized state, outcome probability and all later conditional predictions are unchanged. This argument mixes internal labels within a reported outcome; it does not license changing which reported outcomes are grouped together. For (P₀,P₁), the two-label Hadamard mixing produces (I/√2,Z/√2), the same dephasing update. Code checks the full output for both a pure input and the earlier mixed input, and checks the pure-input result against native joint-density blocks.

```python
hidden=((d.P0,d.P1),)
hp,hs,hu,ht=d.instrument(plus_rho,hidden)
_,blocks,_=d.coupled(plus,1.)
e.close(ht,blocks[0]+blocks[1]);e.close(hs[0],d.I/2)
rotated=((d.I/math.sqrt(2),d.Z/math.sqrt(2)),)
for input_rho in (plus_rho,rho):
    e.close(d.instrument(input_rho,hidden)[3],d.instrument(input_rho,rotated)[3])
print('One visible outcome:p=%.6f,conditional X=%.6f'%(hp[0],d.mean(hs[0],d.X)))
print('Hidden-label unitary mixing preserves the full update;coherently summing its operators does not')
```

```text
One visible outcome:p=1.000000,conditional X=0.000000
Hidden-label unitary mixing preserves the full update;coherently summing its operators does not
```

### 8.3.6 A coarse Lüders measurement differs from forgetting fine results

Let Pᵣ=ΣαQᵣα sum mutually orthogonal fine projectors belonging to a coarse label r. An **ideal coarse Lüders** measurement has one operator Pᵣ per outcome:

$$
\sigma_r^{\mathrm{coarse}}=P_r\rho P_r.
$$

A fine measurement followed by forgetting α instead gives

$$
\sigma_r^{\mathrm{fine}}
 =\sum_\alpha Q_{r\alpha}\rho Q_{r\alpha}.
$$

Both have effect Pᵣ and probability Tr(ρPᵣ), since Qᵣα²=Qᵣα. Expanding PᵣρPᵣ shows exactly the difference: the coarse ideal update retains terms QᵣαρQᵣη for α≠η within the same subspace; forgetting fine outcomes removes them. The word “coarse” applied only to a readout label does not uniquely specify an apparatus's disturbance.

For two qubits, take even parity Pₑ=|00⟩⟨00|+|11⟩⟨11| and odd parity Pₒ=I−Pₑ. Prepare ψφ=(|00⟩+e^{iφ}|11⟩)/√2. Both processes always report even. Coarse ideal parity preserves the full input density, while fine computational measurement followed by forgetting which even string occurred gives diag(.5,0,0,.5). Their correlations are

$$
\begin{aligned}
\langle X\!\otimes\!X\rangle_{\mathrm{coarse}}&=\cos\phi,\\
\langle X\!\otimes\!Y\rangle_{\mathrm{coarse}}&=\sin\phi,
\end{aligned}
$$

and both vanish in the fine-forgotten state. These formulas follow by applying the two Pauli products to |00⟩ and |11⟩ and keeping the two conjugate cross terms. For φ=π/2, XX is accidentally zero in both states, but XY distinguishes them. A single matching expectation is not equality of states or instruments. The following native preparation and exact Pauli queries check this phase-sensitive case; the two alternative updates are computed explicitly on its native density.

```python
c=fq.Circuit(2,dtype=d.D).H(0).P(0,theta=math.pi/2).CX(0,1)
result=fq.run(c,outputs=[fq.density_matrix(),
    fq.expectation(fq.X(0)@fq.X(1),name='xx'),
    fq.expectation(fq.X(0)@fq.Y(1),name='xy')],options=e.OPTIONS)
d.RUNS+=1
joint_rho=result.density_matrix[0]
even=torch.diag(torch.tensor([1,0,0,1],dtype=d.D));odd=torch.eye(4,dtype=d.D)-even
basis=tuple(torch.diag(torch.eye(4,dtype=d.D)[i]) for i in range(4))
coarse=d.instrument(joint_rho,((even,),(odd,)))
fine=d.instrument(joint_rho,((basis[0],basis[3]),(basis[1],basis[2])))
e.close(coarse[0],fine[0]);e.close(coarse[3],joint_rho)
assert coarse[1][1]is None and fine[1][1]is None
for name,A in (('xx',torch.kron(d.X,d.X)),('xy',torch.kron(d.X,d.Y))):
    e.close(d.mean(coarse[3],A),result.expectation(name)[0])
    print(name+':coarse=%.6f,fine/result forgotten=%.6f'%(d.mean(coarse[3],A),d.mean(fine[3],A)))
```

```text
xx:coarse=0.000000,fine/result forgotten=0.000000
xy:coarse=1.000000,fine/result forgotten=0.000000
```

### 8.3.7 Keep chronological joint probabilities before conditioning again

Let a second complete instrument have operators Lₛβ. Its outcome s follows the first outcome r. Starting with the **unnormalized** first branch σᵣ, define

$$
\begin{aligned}
q(r,s)
&=\sum_\beta\operatorname{Tr}
 (L_{s\beta}\sigma_rL_{s\beta}^\dagger)\\
&=\sum_{\alpha,\beta}\operatorname{Tr}
 (L_{s\beta}K_{r\alpha}\rho
 K_{r\alpha}^\dagger L_{s\beta}^\dagger).
\end{aligned}
$$

The product LₛβKᵣα acts in chronological order, first K then L. Each term is nonnegative by the same branch argument. Summing over s and using second-stage completeness yields Σₛq(r,s)=Trσᵣ=pᵣ. Summing over r and s therefore gives one. When pᵣ>0,

$$
\begin{aligned}
p(s\mid r)&=q(r,s)/p_r,\\
p_{\mathrm{ignored}}(s)
 &=\sum_rq(r,s)\\
 &=\sum_\beta\operatorname{Tr}
 (L_{s\beta}\rho_{\mathrm{out}}L_{s\beta}^\dagger).
\end{aligned}
$$

A zero-probability first outcome has a zero joint row and no conditional distribution; do not divide it by zero. A conditional mean for B is Tr(Bρᵣ), and its probability-weighted mean is Tr(Bρout). If the second process changes according to r, that is a different protocol: the system uses an available classical record, and a single fixed ignored-result instrument cannot generally replace it.

For first Z and then X, any positive Z branch has X probabilities (.5,.5). Thus q(r,s)=pᵣ/2 and the ignored-record X marginal is (.5,.5), even when the original input's X probabilities were unequal. The native circuit below performs the unitary Z-record coupling and applies H to the system before terminal computational readout. Requested columns are (meter q1, system q0); reshaping the four returned probabilities into 2×2 gives rows r and columns s. This checks the joint probability law without claiming an intermediate native collapse.

```python
second=(((d.I+d.X)/2,),((d.I-d.X)/2,))
table=d.sequential(rho,d.Z_GROUPS,second)
explicit=torch.tensor([[sum(torch.trace(L@sigma@L.mH).real.item() for L in group)
    for group in second] for sigma in sigmas],dtype=torch.float64)
e.close(table,explicit)
native_tables=[d.coupled(c,1.,analyzer=True)[2] for c in components]
e.close(table,sum(w*t for w,t in zip(weights,native_tables)))
print('Joint rows(Z record),columns(X outcome):',[[round(x,9) for x in row] for row in table.tolist()])
print('Ignored-record X probabilities:',[round(x,9) for x in table.sum(0).tolist()])
```

```text
Joint rows(Z record),columns(X outcome): [[0.349909695, 0.349909695], [0.150090305, 0.150090305]]
Ignored-record X probabilities: [0.5, 0.5]
```

### 8.3.8 Retain zero, rare and numerically unresolved branches distinctly

An impossible branch has σᵣ=0 and pᵣ=0 in the exact model. A rare branch with pᵣ>0 remains a legitimate conditional state however small its weight. For ρ=diag(1−ε,ε) and projective Z, the record-1 conditional density is |1⟩⟨1| for **every** ε>0, although its probability is only ε. Dropping this branch merely because pᵣ is below an implementation tolerance would change the model.

There is a third possibility: arithmetic cannot resolve the branch weight. The helper detects a zero trace with nonzero Kρ factors or a nonzero branch matrix and raises a numerical error instead of calling the event impossible. For example, a group K₀=10⁻²⁰⁰I has nonzero K₀ρ while K₀ρK₀† underflows to zero in complex128. This diagnostic is conservative: in other problems a cancellation residual can also trigger it. It is not a complete floating-point underflow detector or an interval certificate. Normalization by a very small probability can be ill-conditioned even if the guard passes.

The instrument contract requires completeness. A deliberately incomplete collection models a different, trace-decreasing selected operation; to treat it as an entire measurement one must supply its failure outcomes. The helper rejects incompleteness rather than dividing by the sum of whatever probabilities remain. It also rejects malformed densities, matrices, strengths, dtypes and observables. Its square dimension-2-or-4 operators are a bounded teaching scope, not a native FlagQuantum limit or a restriction of the mathematical formulas above.

```python
zero=d.instrument(d.P0,d.Z_GROUPS)
assert zero[0][1]==0 and zero[1][1]is None
rare=torch.diag(torch.tensor([1-1e-20,1e-20],dtype=d.D))
rare_result=d.instrument(rare,d.Z_GROUPS)
assert rare_result[0][1]>0 and rare_result[1][1]is not None
print('Zero event:None;positive1e-20 event:normalized state retained')
print('%d malformed contracts rejected;nonzero-factor underflow raises'%d.invalid_checks())
print('%d actual native body circuits;no native sampled collapse asserted'%d.RUNS)
```

```text
Zero event:None;positive1e-20 event:normalized state retained
13 malformed contracts rejected;nonzero-factor underflow raises
13 actual native body circuits;no native sampled collapse asserted
```

**Actual API support and limits.** In the installed released version we inspected, `fq.density_matrix`, `fq.probabilities` and Pauli-based `fq.expectation` outputs are available and are actually executed here. Both tested simulator modes produce the full density of the prepared system or coupled system–meter register. The unitary coupling uses the actual RY/CRY/CX gates; the arbitrary matrix calls are unitary preparation matrices, never nonunitary measurement operators submitted to `Circuit.unitary`.

Every σᵣ, ρᵣ, ignored-result sum and sequential table in this section is explicit classical postprocessing or a comparison with the native unitary circuit's outputs. The inspected root API and Circuit surface do not expose an outcome-indexed `instrument` call or a Circuit measurement/reset/conditional method used by these examples. This is a scoped statement about the checked version and interface, not a denial that generalized measurement can be built using gates, or that other noise/runtime interfaces may exist. We do not call a guessed mixed-state initializer, noise function, native sampled collapse, reset or classical-feedback endpoint. Fresh branch preparation is a separate run. Coherent meter-controlled X is unitary control. No hardware or dynamic-circuit implementation claim follows from these simulator checks.

Expected output of the complete program:

```text
12 native input circuits:both modes;density,probabilities and X/Y/Z/H means passed.
36 native weak couplings:strength0/.6/1,two instruments,two modes;host mixed branches match joint-density blocks.
4 native Z-record/X-readout circuits:chronological joint probabilities,conditionals and ignored marginal passed.
6 native joint preparations:coarse parity preserves coherence,fine Z with forgotten labels removes it.
13 malformed contracts rejected;positive1e-20 retained,zero returns None,underflow raises.
58 actual native circuits;all conditional updates and ensemble sums are explicit host calculations.
```

The complete program executes 58 native circuits: 12 input expectation checks, 36 weak couplings, four chronological readout checks and six joint preparations. Host ensembles and updates are not extra quantum executions. The literal body executes 13 additional circuits. Fresh transfer cases and the body/complete checker are recorded separately, as are prior-section regressions. The full finite-instrument proofs apply beyond these examples; independent mathematical review, implementation review and reader trial remain pending.

### Understanding checks and transfer exercises

**8.3-A — Which object is normalized?** Given σᵣ and pᵣ, derive the trace of σᵣ, the trace of ρᵣ when it exists, and the trace of Σᵣσᵣ. Explain what fails if one averages conditional densities with equal weights. What should be returned when a complete measurement has pᵣ=0? Why should an incomplete operator list not be silently renormalized?

**8.3-B — Fresh mixed input and equal effects.** Prepare u=qubit(.57,−.68) and v=qubit(1.92,.44) with weights (.41,.59). For κ=.43, compute the two record probabilities, both conditional densities, the ignored-result state and its Z mean for the M and N models of 8.3.4. Use native component densities and actual couplings to compare complete branch matrices. Predict which quantities must agree for all inputs and which need not.

**8.3-C — A phase-sensitive coarse test.** Prepare ψφ for φ=−.38 and for φ=π/2 in both native modes. Derive the coarse-even and fine-forgotten densities. Check XX and XY; explain why XX alone is inadequate in the second case. Separately prove that (P₀,P₁) and (I/√2,Z/√2) within one outcome give the same update for every input density, not just |+⟩.

**8.3-D — New chronological table and rare branch.** For the fresh mixed input of B, use ordinary weak measurement κ=.43 followed by X. Derive q(r,s), the conditional rows and ignored-record marginal. Verify against native system–meter coupling followed by H, in both modes, with output order (q1,q0). Does replacing the first weak measurement by projective Z give the same table? Retain a projective Z branch with probability 10⁻²⁰ and explain how it differs from both a zero branch and an arithmetic-underflow report.

<details markdown="1">
<summary>Answers and verification guidance for 8.3-A–D</summary>

**A.** The respective traces are pᵣ, one for pᵣ>0, and one by completeness. Equal branch weights generally describe another mixture. A zero branch has no conditional state; `None` conveys this without inventing one. An incomplete list omits physical alternatives, so normalizing its retained sum changes an unconditional question into conditioning on their union. That must be a declared protocol, not a numerical repair.

**B.** Write the native mixed matrix as ρ=[[a,z],[z*,1−a]]. With h=√(1−κ²), the two unnormalized ordinary branches are

$$
\begin{aligned}
\sigma_0^M&=\frac12\begin{pmatrix}
 (1+\kappa)a&hz\\hz^*&(1-\kappa)(1-a)
\end{pmatrix},\\
\sigma_1^M&=\frac12\begin{pmatrix}
 (1-\kappa)a&hz\\hz^*&(1+\kappa)(1-a)
\end{pmatrix}.
\end{aligned}
$$

Their traces are p₀=[1+κ(2a−1)]/2 and p₁=1−p₀. Divide each by its own positive trace. For N, σ₀ is unchanged and σ₁ is Xσ₁ᴹX. Probabilities agree; the record-1 conditional Z mean changes sign, and the ignored-result densities can differ. The ordinary ignored result has diagonal (a,1−a) and off-diagonal hz, so its Z mean remains 2a−1. The N model instead sums σ₀ᴹ+Xσ₁ᴹX. Its diagonal entries are ((1+κ)/2,(1−κ)/2), so its Z mean is κ for every input, which need not equal 2a−1. The transfer program checks these formulas against native joint blocks.

**C.** Coarse-even output is |ψφ⟩⟨ψφ| with off-diagonal entries e^{∓iφ}/2 between indices 0 and 3. Fine-forgotten output has only diagonal entries .5 at those indices. Their (XX,XY) means are respectively (cosφ,sinφ) and (0,0). At φ=π/2 the first coordinate is zero in both cases. For the hidden-label equivalence, expand [(IρI)+(ZρZ)]/2 and substitute I=P₀+P₁, Z=P₀−P₁: the cross terms cancel, leaving P₀ρP₀+P₁ρP₁.

**D.** Let σᵣ be the ordinary weak branches of B. For X outcomes s=0,1, corresponding to eigenvalues +1,−1,

$$
\begin{aligned}
q(r,s)&=\frac{p_r+(-1)^s t_r}{2},\\
t_r&=\operatorname{Tr}(X\sigma_r)
 =\sqrt{1-\kappa^2}\,\operatorname{Re}z.
\end{aligned}
$$

Both branches have the same real off-diagonal sum here. Divide each row by pᵣ to condition; sum rows to ignore r. The ignored X probabilities are [1+(-1)ˢ2√(1−κ²)Re z]/2. For projective Z, κ=1 and every row has equal columns pᵣ/2; the probabilities pᵣ also change with κ, so the full tables generally differ. A 10⁻²⁰ Z branch remains a positive event with a valid normalized basis density. A zero event has no conditional density. An underflow report says arithmetic could not safely establish that distinction; it does not provide evidence for probability zero.

</details>

**Sources and proof scope.** The frozen locators are NC §2.4.2, printed page 101, and §8.2.3, printed page 360 (contents locators checked; no new full-text NC review claimed). We also consulted [Watrous, author-hosted manuscript §2.3.2, printed pages 111–112](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf#page=119) for selective-state and instrument conventions. The finite ensemble, normalization, hidden-label and chronological derivations are provided explicitly above. The general operator-sum representation theorem and full channel/instrument theory are not substituted for these proofs. This is an author-verified draft, not formal acceptance.

<!-- end-section-8.3 -->

<span id="sec-density-matrices-reduced-states-and-purification-4"></span>

## 8.4 Partial trace from operational consistency

Suppose a laboratory has access only to subsystem A of a joint system AB. What density operator should it use? Deleting entries of a statevector, keeping a diagonal block, and averaging blocks are different operations. We will derive the correct operation by requiring agreement with **every local expectation**, then prove that no other local density can satisfy that requirement.

The frozen prerequisites are [4.1, finite tensor-product spaces](ch-composite-systems-tensor-products-and-qubit-ordering.md#sec-composite-systems-tensor-products-and-qubit-ordering-1), and [8.3, density expectations and measurement updates](#sec-density-matrices-reduced-states-and-purification-3). This section has depth **F**. The component derivation, positivity, existence and uniqueness are proved for arbitrary finite factor dimensions. The implementation is bounded to small systems for independent dense references; it does not replace these proofs with numerical examples.

Let the joint space be H_A⊗H_B with dimensions d_A,d_B≥1 and orthonormal product basis |i⟩_A|μ⟩_B. Latin indices refer to A; Greek indices refer to B. The full density ρ_AB is positive, Hermitian and unit trace. A Hermitian operator A on H_A represents an observable accessible to the local laboratory. Its action on the joint space is A⊗I_B: the identity leaves B unobserved. Expectation values and probabilities in the examples are dimensionless; gate angles are radians. If an observable carries units, the two expectations compared below carry those same units.

Run the eight cumulative units from the repository root. The companion [partial_trace.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/partial_trace.py) uses actual released FlagQuantum 0.3.1 selected-density outputs in both tested modes. Scalar index sums, tensor contractions and observable-frame reconstruction are explicit independent host calculations. Deterministic comparisons use absolute tolerance $10^{-12}$ and relative tolerance zero, without clipping, symmetrization, normalization repair or phase alignment.

### 8.4.1 Derive the retained matrix from local expectations

A local state ρ_A must satisfy the operational consistency requirement

$$
\boxed{\operatorname{Tr}_A(\rho_A A)
 =\operatorname{Tr}_{AB}\bigl(\rho_{AB}(A\otimes I_B)\bigr)}
$$

for **every Hermitian A**. This requirement says that predictions for experiments restricted to A do not depend on whether we use the local description or the full one. It does not assert that all these experiments can be performed simultaneously on one copy.

Use the product-basis coordinates

$$
\begin{aligned}
\rho_{i\mu,j\nu}
 &=\langle i,\mu|\rho_{AB}|j,\nu\rangle,\\
(A\otimes I_B)_{j\nu,i\mu}
 &=A_{ji}\delta_{\nu\mu}.
\end{aligned}
$$

Expanding the full trace and applying the Kronecker delta gives

$$
\begin{aligned}
\operatorname{Tr}_{AB}\bigl(\rho_{AB}(A\otimes I_B)\bigr)
 &=\sum_{i,j,\mu,\nu}\rho_{i\mu,j\nu}A_{ji}\delta_{\nu\mu}\\
 &=\sum_{i,j}\left(\sum_\mu\rho_{i\mu,j\mu}\right)A_{ji}.
\end{aligned}
$$

The local trace has the form Σᵢⱼ(ρ_A)ᵢⱼAⱼᵢ. The candidate that makes the two traces equal is therefore

$$
\boxed{(\rho_A)_{ij}=\sum_{\mu=0}^{d_B-1}\rho_{i\mu,j\mu}.}
$$

We call this operator the **partial trace over B**, written ρ_A=Tr_Bρ_AB. “Over B” names the subsystem removed, not the subsystem returned. The same discarded index μ appears in the ket and bra positions. We sum it; we do not sum arbitrary independent μ,ν, and do not divide by d_B.

For two qubits in basis order |q0,q1⟩, q0 is the most significant bit and the full index is 2i+μ. For the Bell state (|00⟩+|11⟩)/√2, the rule gives I/2 on either qubit. The code visibly requests full and selected native density matrices, retrieves them by name, and checks the derived formula and a local Pauli-sum expectation. With several density requests, named access avoids confusing a full output with a reduction.

```python
import math
import torch
import flagquantum as fq
from examples.foundations import partial_trace as t
from examples.foundations import statistical_ensembles as e
c=fq.Circuit(2,dtype=t.D).H(0).CX(0,1)
result=fq.run(c,outputs=[fq.density_matrix(name='full'),
    fq.density_matrix(qubits=(0,),name='A'),fq.density_matrix(qubits=(1,),name='B'),
    fq.expectation(fq.X(0)@fq.X(1),name='xx')],options=e.OPTIONS)
t.RUNS+=1
bell_full=result.measurement('full').value[0]
RA=result.measurement('A').value[0];RB=result.measurement('B').value[0]
explicit=torch.tensor([[sum(bell_full[2*i+mu,2*j+mu].item()for mu in range(2))
    for j in range(2)]for i in range(2)],dtype=t.D)
e.close(RA,explicit);e.close(RA,e.I/2);e.close(RB,e.I/2)
A=.7*e.X-.2*e.Y+1.3*e.Z
e.close(torch.trace(RA@A),torch.trace(bell_full@torch.kron(A,e.I)))
print('Native A/B reductions:',[round(x.real.item(),6)for x in RA.diagonal()])
print('Local trace consistency passed;global XX=%.6f'%result.expectation('xx')[0].item())
```

```text
Native A/B reductions: [0.5, 0.5]
Local trace consistency passed;global XX=1.000000
```

### 8.4.2 Prove that the candidate is a density and that it exists

The component formula must still produce a legitimate local state. Hermiticity follows entry by entry:

$$
(\rho_A)_{ji}^*
 =\sum_\mu\rho_{j\mu,i\mu}^*
 =\sum_\mu\rho_{i\mu,j\mu}
 =(\rho_A)_{ij}.
$$

For any local vector x, use the corresponding joint vectors x⊗|μ⟩. Positivity of the full density gives

$$
\begin{aligned}
x^\dagger\rho_Ax
 &=\sum_\mu
 (x\otimes|\mu\rangle)^\dagger
 \rho_{AB}(x\otimes|\mu\rangle)\\
 &\geq0.
\end{aligned}
$$

Finally, its trace is the sum of every joint diagonal entry exactly once:

$$
\operatorname{Tr}\rho_A
 =\sum_{i,\mu}\rho_{i\mu,i\mu}
 =\operatorname{Tr}\rho_{AB}=1.
$$

Thus the candidate is Hermitian, positive and normalized. Substituting its entries in the local trace reproduces the expansion of 8.4.1, so it satisfies the consistency requirement for every Hermitian A. This proves existence.

The contraction also defines a linear map on any joint operator M, including unnormalized measurement branches: Tr_B(αM+βN)=αTr_BM+βTr_BN, because the entry sums distribute. It preserves the total trace rather than repairing it. A branch operator of trace p reduces to an operator of trace p, not automatically to a density of trace one.

For a product operator C⊗D, the same entries give

$$
\operatorname{Tr}_B(C\otimes D)
 =C\sum_\mu D_{\mu\mu}
 =C\operatorname{Tr}D.
$$

Consequently a product density ρ_A⊗ρ_B reduces to ρ_A. Its local coherences are preserved; a partial trace is not an instruction to diagonalize the retained matrix. The following native complex product preparation verifies this identity and the density conditions.

```python
product_result,product_vector=t.native(2,.81,-.26,kind='product')
product_full=product_result.measurement('full').value[0]
product_A=product_result.measurement('r_0').value[0]
product_B=product_result.measurement('r_1').value[0]
e.close(product_A,e.outer(e.qubit(.81,-.26)))
e.close(product_full,torch.kron(product_A,product_B))
t.density(product_A);t.density(product_B)
print('Product reduction:Hermitian,positive,trace=%.6f'%torch.trace(product_A).real.item())
```

```text
Product reduction:Hermitian,positive,trace=1.000000
```

### 8.4.3 Prove uniqueness using only Hermitian local observables

Suppose σ_A is another density satisfying the same local-expectation requirement. The difference Δ=σ_A−ρ_A is Hermitian, and Tr(ΔA)=0 for every Hermitian A. In particular, choose A=Δ. Then

$$
\begin{aligned}
0=\operatorname{Tr}(\Delta^2)
 &=\sum_{i,j}\Delta_{ij}\Delta_{ji}\\
 &=\sum_{i,j}|\Delta_{ij}|^2.
\end{aligned}
$$

Each term is nonnegative, so every entry is zero and σ_A=ρ_A. This proves uniqueness among local density operators without assuming that a non-Hermitian matrix unit is itself a measurable observable.

There is also an explicit finite reconstruction. Use the d_A diagonal projectors Eᵢᵢ=|i⟩⟨i| and, for each i<j, the Hermitian operators

$$
\begin{aligned}
X_{ij}&=|i\rangle\langle j|+|j\rangle\langle i|,\\
Y_{ij}&=-i|i\rangle\langle j|+i|j\rangle\langle i|.
\end{aligned}
$$

They give Tr(ρ_AEᵢᵢ)=(ρ_A)ᵢᵢ, Tr(ρ_AXᵢⱼ)=2Re(ρ_A)ᵢⱼ and Tr(ρ_AYᵢⱼ)=−2Im(ρ_A)ᵢⱼ. Thus

$$
(\rho_A)_{ij}
 =\frac{\langle X_{ij}\rangle-i\langle Y_{ij}\rangle}{2}
 \quad(i<j).
$$

There are d_A+2·d_A(d_A−1)/2=d_A² such Hermitian probes. Their expectations determine every coordinate, with the conjugates fixing the lower triangle. These are mathematical reconstruction queries, not a simultaneous-measurement claim or a finite-shot tomography certificate.

Our independent reference constructs each A⊗I in full coordinates and evaluates its trace against the actual native full density. The resulting local matrix must agree with the native selected density. A direct native Y query calibrates the imaginary sign: a local (|0⟩+i|1⟩)/√2 has ρ₀₁=−i/2 and Y mean +1. Conjugating that density leaves its diagonal probabilities unchanged but predicts the wrong Y sign. The general d_A² dense probes here are host calculations, not an unverified native arbitrary-matrix expectation API.

```python
c=fq.Circuit(2,dtype=t.D).H(0).P(0,theta=math.pi/2)
result=fq.run(c,outputs=[fq.density_matrix(name='full'),fq.density_matrix(qubits=(0,),name='A'),
    fq.expectation(fq.Y(0),name='y')],options=e.OPTIONS)
t.RUNS+=1
full=result.measurement('full').value[0];actual=result.measurement('A').value[0]
reconstructed=t.reconstruct(full,2,(0,));e.close(reconstructed,actual)
y=result.expectation('y')[0].item()
e.close(y,torch.trace(reconstructed@e.Y));e.close(reconstructed[0,1],-.5j)
wrong=reconstructed.conj();e.close(torch.trace(wrong@e.Y),-1)
print('Hermitian probes:Im(rho01)=%.9f;Re(rho01) checked against0'%reconstructed[0,1].imag.item())
print('Native Y=%.6f;wrong conjugated density predicts Y=%.6f'%(y,torch.trace(wrong@e.Y).real.item()))
```

```text
Hermitian probes:Im(rho01)=-0.500000000;Re(rho01) checked against0
Native Y=1.000000;wrong conjugated density predicts Y=-1.000000
```

### 8.4.4 A local density does not identify the global correlations

Consider the Bell density and the classical mixture

$$
\begin{aligned}
\rho^{\mathrm{Bell}}&=|\Phi^+\rangle\langle\Phi^+|,\\
\rho^{\mathrm{classical}}
 &=\tfrac12|00\rangle\langle00|
  +\tfrac12|11\rangle\langle11|.
\end{aligned}
$$

Both reduce to I/2 on A and on B. However, the Bell matrix contains joint off-diagonal terms |00⟩⟨11|/2 and its adjoint. Those terms disappear under a trace over either factor because their discarded ket and bra indices differ. They remain observable jointly: ⟨X⊗X⟩ is one for the Bell state and zero for the classical mixture. The latter equality follows because each product component has zero X mean on either qubit.

This is consistent with uniqueness. The local state is uniquely determined by all local experiments, but the global state is not uniquely determined by its local states. Partial trace deliberately retains only the predictions available on the specified subsystem. It does not reveal a unique hidden ensemble or certify that a physical measurement was performed on B. In particular, deleting one tensor index from the Bell statevector and normalizing the result would invent a pure local vector with coherences absent from I/2.

The native Bell result from unit 1 is compared with a host mixture of two additional native product preparations. The global correlation distinguishes them even though their complete local density matrices coincide.

```python
components=[t.native(2,0.,0.,kind='basis',basis=b)for b in ((0,0),(1,1))]
mixture=sum(.5*r.measurement('full').value[0]for r,v in components)
mixture_A=t.indexed(mixture,2,(0,))
e.close(mixture_A,RA);e.close(t.indexed(mixture,2,(1,)),RB)
assert not torch.allclose(mixture,bell_full,atol=t.ATOL,rtol=0)
mixture_xx=sum(.5*r.expectation('xx')[0]for r,v in components)
print('Same A and B densities;global XX:Bell=1.000000,classical mixture=%.6f'%mixture_xx.item())
```

```text
Same A and B densities;global XX:Bell=1.000000,classical mixture=0.000000
```

### 8.4.5 Remove dependence on the discarded basis

The definition used a basis {|μ⟩} of B. It must not depend on which orthonormal basis a calculation happens to use. Let |fν⟩=ΣμUμν|μ⟩, with U unitary. Contracting in the new basis gives

$$
\begin{aligned}
R'_{ij}
 &=\sum_{\nu,\mu,\lambda}
 U_{\mu\nu}^*U_{\lambda\nu}
 \rho_{i\mu,j\lambda}\\
 &=\sum_\mu\rho_{i\mu,j\mu}
 =R_{ij},
\end{aligned}
$$

because ΣνU*μνUλν=δμλ. This is a passive change of coordinates in the discarded factor, not a physical SWAP or a new retained subsystem.

A physical unitary V applied only on B also leaves the retained state invariant. For every local A, finite trace cyclicity gives

$$
\begin{aligned}
\operatorname{Tr}\bigl[
 (I\otimes V)\rho(I\otimes V^\dagger)(A\otimes I)\bigr]
 &=\operatorname{Tr}\bigl[\rho(A\otimes V^\dagger V)\bigr]\\
 &=\operatorname{Tr}\bigl[\rho(A\otimes I)\bigr].
\end{aligned}
$$

Uniqueness then fixes the same ρ_A. The two statements have different interpretations even though both follow from unitarity on the factor not accessed. A change of coordinates on the retained factor instead changes its matrix representation covariantly; it is not an invariance of every displayed matrix entry.

For a nontrivial complex two-qubit input, we check both passive contraction of (I⊗U†)ρ(I⊗U) and an actual native U gate on the discarded qubit. The actual full states may change; the retained matrices must agree in the same A basis.

```python
U=e.prepare(e.qubit(.63,.27))
before,_=t.native(2,.91,-.36)
after,_=t.native(2,.91,-.36,rotate_last=U)
full=before.measurement('full').value[0]
B=torch.kron(e.I,U)
changed_coordinates=B.mH@full@B
passive=t.trace_ab(changed_coordinates,2,2)
e.close(passive,before.measurement('r_0').value[0])
e.close(before.measurement('r_0').value,after.measurement('r_0').value)
print('Discarded-basis contraction and actual local B rotation give the same retained density')
```

```text
Discarded-basis contraction and actual local B rotation give the same retained density
```

### 8.4.6 Match tensor axes to the ordered retained qubits

A nonadjacent subsystem is still a tensor factor after a declared regrouping of the basis. For n qubits, the full basis index is Σq b_q2^{n−1−q}. Let S=(s₀,…,sₖ₋₁) be the ordered tuple of retained qubits, and let T list the others in increasing physical-label order. Define the local and discarded indices by their bit strings in those respective orders. The function ℓ(i,μ) places those bits back into their full positions. Then

$$
(\rho_S)_{ij}
 =\sum_\mu\rho_{\ell(i,\mu),\ell(j,\mu)}.
$$

For S=(q2,q0) in a three-qubit register, i=2b₂+b₀ and μ=b₁, so

$$
\begin{aligned}
\ell(i,\mu)
 &=4(i\bmod2)+2\mu+\lfloor i/2\rfloor,\\
(\rho_{(q2,q0)})_{2,1}
 &=\rho_{1,4}+\rho_{3,6}.
\end{aligned}
$$

This explicit index sum is the first reference implementation. The second reshapes the full matrix into n ket axes followed by n bra axes. It permutes them into the order (S,T,S′,T′), then reshapes to (d_S,d_T,d_S,d_T). Here a prime means a bra-coordinate axis, not a second physical register. Contracting with `einsum('imjm->ij', tensor)` uses the same discarded index m in the two discarded positions. A reshape alone does not regroup nonadjacent qubits; the permutation is essential. These axis operations are classical coordinate manipulations, not physical SWAP gates.

For a pure full vector, one further independent check places its coefficients into Cᵢμ=ψ_{ℓ(i,μ)}. Expanding the outer product gives ρ_S=CC† entry by entry. No Schmidt-spectrum identity is assumed here; that result belongs to 8.5.

The native density request uses the tuple as the returned basis order. Thus (q2,q0) and (q0,q2) retain the same physical subsystem but display different matrix coordinates. The two-qubit reordering is π=(0,2,1,3), so R₂₀[i,j]=R₀₂[π(i),π(j)]. Both matrix axes must be permuted; this is not a transpose or a conjugation. The diagonal must also agree with the native computational probabilities requested in that same tuple order.

```python
c,expected=t.preparation(3,.76,-.58)
result=fq.run(c,outputs=[fq.density_matrix(name='full'),
    fq.density_matrix(qubits=(2,0),name='A20'),fq.density_matrix(qubits=(0,2),name='A02'),
    fq.probabilities(qubits=(2,0),name='p20')],options=e.OPTIONS)
t.RUNS+=1
full3=result.measurement('full').value[0]
A20=result.measurement('A20').value[0];A02=result.measurement('A02').value[0]
scalar=t.indexed(full3,3,(2,0));tensor=t.axes(full3,3,(2,0))
e.close(A20,scalar);e.close(A20,tensor)
permutation=torch.tensor([0,2,1,3]);e.close(A20,A02[permutation][:,permutation])
e.close(A20.diagonal().real,result.measurement('p20').value[0])
print('Ordered retained tuple(2,0):scalar indices,tensor axes,native density/probability agree')
print('Reversing retained tuple permutes both matrix axes;it does not transpose/conjugate the matrix')
```

```text
Ordered retained tuple(2,0):scalar indices,tensor axes,native density/probability agree
Reversing retained tuple permutes both matrix axes;it does not transpose/conjugate the matrix
```

### 8.4.7 Distinguish reduction, conditioning and unread local processing

Partial trace alone does not condition on any outcome. If a measurement on B has operators Kᵣα, then the full unnormalized branch from 8.3 is

$$
\sigma_r=\sum_\alpha
 (I_A\otimes K_{r\alpha})\rho
 (I_A\otimes K_{r\alpha}^\dagger).
$$

For pᵣ=Trσᵣ>0, the retained conditional density is Tr_Bσᵣ/pᵣ. Linearity makes its unnormalized reduction have trace pᵣ. If the local process on B is complete and its outcome is ignored, then for every A

$$
\begin{aligned}
\sum_r\operatorname{Tr}\bigl[\sigma_r(A\otimes I)\bigr]
 &=\operatorname{Tr}\!\left[
 \rho\left(A\otimes\sum_{r,\alpha}K_{r\alpha}^\dagger K_{r\alpha}\right)\right]\\
 &=\operatorname{Tr}\bigl[\rho(A\otimes I)\bigr].
\end{aligned}
$$

Uniqueness implies

$$
\sum_{r:p_r>0}p_r\rho_{A\mid r}=\rho_A.
$$

Thus local complete processing of the discarded subsystem does not change the unread local predictions on A, while conditional predictions can change when a record is supplied. An incomplete selected process must not be treated as this complete average. For a zero-probability outcome no conditional density is defined; its unnormalized contribution is zero. This argument is an algebraic local-consistency consequence, not an assertion that a classical outcome has been sent to A.

For ψ=cos(θ/2)|00⟩+e^{iφ}sin(θ/2)|11⟩, a Z result on B conditions A into |0⟩ or |1⟩. Their weights are cos²(θ/2) and sin²(θ/2). The unread A density equals the original native reduction, diag(cos²(θ/2),sin²(θ/2)); an unweighted average is generally wrong. The full ignored-result state loses joint coherence, even though A's local state is unchanged. The following uses θ=.72, φ=.43 and explicit host projective branches on a native full density. It is not a native sampled collapse request.

```python
from examples.foundations import density_updates as d
biased,_=t.native(2,.72,.43,kind='bell')
full=biased.measurement('full').value[0];prior=biased.measurement('r_0').value[0]
groups=((torch.kron(e.I,d.P0),),(torch.kron(e.I,d.P1),))
probs,states,sigmas,ignored=d.instrument(full,groups)
selected_A=[t.indexed(state,2,(0,))for state in states]
e.close(selected_A[0],d.P0);e.close(selected_A[1],d.P1)
e.close(t.indexed(ignored,2,(0,)),prior)
e.close(sum(p*a for p,a in zip(probs,selected_A)),prior)
assert not torch.allclose((selected_A[0]+selected_A[1])/2,prior,atol=t.ATOL,rtol=0)
print('Recorded B outcomes:',[round(p,9)for p in probs])
print('Conditional A states differ;ignored-result A equals its prior native reduction')
```

```text
Recorded B outcomes: [0.875902865, 0.124097135]
Conditional A states differ;ignored-result A equals its prior native reduction
```

### 8.4.8 Keep mathematical edge cases separate from native request conventions

When d_B=1, the partial trace is the identity on the matrix of A. When d_A=1, the output is the 1×1 matrix [Trρ]=[1]. Keeping all qubits in their original order likewise returns the full matrix, while keeping them in a different order permutes its coordinates. Keeping no qubits mathematically leaves a one-dimensional retained space, so the host reference returns [TrM] even for an unnormalized operator M. It never divides by the trace.

A **native API convention differs at this boundary**. In two actual 0.3.1 probes, one in each tested mode, `fq.density_matrix(qubits=())` returned the full two-qubit density with shape (1,4,4), not (1,1,1). The request constructor accepts the empty tuple, but its executed behavior must not be interpreted as the mathematical trace-all operation. All selected native outputs used for the proofs and examples therefore name a nonempty tuple. The companion explicitly rejects an empty native selection and uses the host reference for trace-all. Omitting the selection also requests the full register; the source and the measured probe evidence are retained separately.

Factor dimensions need not be powers of two in the mathematics. A 3×2 bipartite space has a 6×6 joint matrix and a 3×3 retained matrix; the host factor-index implementation covers this case. This does not claim a native qutrit interface. Invalid dimensions, duplicated or out-of-range qubit labels, nonfinite matrices, wrong dtypes and malformed densities are rejected by the corresponding teaching contracts. The dense dimension≤16 and n≤4 limits bound these independent examples; they are not FlagQuantum's general system limits. Numerical positivity checks and equality tolerances are diagnostics, not interval certificates for an unknown preparation.

```python
one=t.indexed(full3,3,());e.close(one,torch.ones((1,1),dtype=t.D))
e.close(t.indexed(full3,3,(0,1,2)),full3)
e.close(t.indexed(3*full3,3,()),torch.tensor([[3]],dtype=t.D))
general=torch.diag(torch.tensor([.1,.2,.1,.3,.2,.1],dtype=t.D))
e.close(t.trace_ab(general,3,2),torch.diag(torch.tensor([.3,.4,.3],dtype=t.D)))
e.close(t.trace_ab(general,1,6),torch.ones((1,1),dtype=t.D))
e.close(t.trace_ab(general,6,1),general)
print('Host empty/full/dimension-one and3x2factor traces passed;no normalization performed')
print('%d malformed contracts rejected'%t.invalid_checks())
print('%d actual native body circuits;native empty tuple is not host trace-all'%t.RUNS)
```

```text
Host empty/full/dimension-one and3x2factor traces passed;no normalization performed
14 malformed contracts rejected
9 actual native body circuits;native empty tuple is not host trace-all
```

**Actual support and costs.** Released FlagQuantum's real `fq.density_matrix(qubits=..., name=...)` output computes selected subsystem matrices, and these examples actually verify nonempty ordered selections in both `statevector` and `density_matrix` modes. Values carry a leading execution batch axis; the code explicitly selects batch element zero. Native selected probabilities and Pauli expectations provide additional local and joint checks. A selected density is a query result, not a physical instruction to erase, measure or reset the other qubits.

The inspected 0.3.1 runtime source constructs a full density matrix on its statevector route and guards that route at 10 qubits before reduction. This limit is source-inspected, not tested by allocating a large matrix here. The density-matrix route already holds a full joint matrix. Therefore a small returned subsystem does not imply that simulation or intermediate memory is small; a full n-qubit dense matrix has 4ⁿ entries. No performance or scalability claim follows from these small examples.

The tested global preparations are pure, but their native reductions can be mixed. Additional mixed global matrices are explicit host weighted sums of actual component outputs, checked using linearity. We do not infer an arbitrary mixed-state initializer, invoke noise, implement native collapse, or claim hardware access. General dense local probes and conditional branch calculations are host references. We do not silently diagonalize, clip, normalize or average statevectors to obtain agreement.

Expected output of the complete program:

```text
24 native basis circuits:all nonempty ordered two/three-qubit selections match scalar sums and paired-axis traces.
16 native complex product/chain circuits:entry/axis/coefficient/observable-frame references and host mixed reductions passed.
6 native Bell-family circuits:reduced states and phase-sensitive global Pauli correlations passed.
4 native discarded-subsystem rotations:retained density invariant,including passive basis contraction.
14 malformed contracts rejected;dimension-one/empty/full and unnormalized linear traces passed.
50 actual native circuits;464 selected-density outputs;classical probes and host mixtures are not extra quantum executions.
```

The complete program executes 50 native circuits and checks 464 selected-density outputs across all nonempty ordered two-/three-qubit selections for its declared preparations. These outputs, classical trace probes and mixture calculations are not additional quantum executions. The literal body executes nine circuits; transfer cases, the body/complete checker and two API probes are recorded separately. Existence and uniqueness for arbitrary finite dimensions follow from the proofs above, not from the number of numerical cases.

### Understanding checks and transfer exercises

**8.4-A — Fix the contraction.** Derive (ρ_A)₀₁ explicitly for a 2×3 factorization. Explain why the discarded ket and bra indices must match and why dividing the sum by three is wrong. Derive Tr_B(C⊗D) for a general, possibly unnormalized, product operator. Prove uniqueness using either Δ or the d_A² Hermitian frame; do not treat a non-Hermitian matrix unit as a physical observable without explanation.

**8.4-B — Fresh ordered four-qubit subsystem.** Use the companion's chain preparation with θ=−.67, φ=.39 on four qubits. Request S=(q3,q1), its reversed order, and the single-qubit reductions. Derive the bit-lift rule for S and the discarded order (q0,q2). Verify native matrices with scalar sums, tensor contraction, coefficient contraction and the Hermitian frame. Repeat for a host mixture with a fresh product preparation θ=1.08, φ=−.53 and weights (.29,.71), in both modes.

**8.4-C — Fresh discarded basis and retained correlations.** On a three-qubit chain preparation with θ=.64, φ=−.82, retain (q2,q0) and apply U=prepare(qubit(−.47,.62)) only to q1. Check invariance of the retained matrix in both modes. Then use biased Bell preparations with θ=1.07 and φ=−.51 or π/2. Compare local reductions, conditional Z branches on B, and the full coherence before and after ignoring B's result. Does a zero XX correlation establish absence of the joint off-diagonal terms?

**8.4-D — Empty selection and a non-qubit factorization.** Contrast the mathematical result for no retained qubits with the measured native empty-tuple behavior. Construct a positive normalized 6×6 matrix with complex off-diagonal entries on a 3×2 space, reduce it by scalar sums and a paired-axis contraction, and verify all nine retained Hermitian probes. Include the d_A=1 and d_B=1 cases and an unnormalized branch. State which parts are classical rather than native qutrit or collapse operations.

<details markdown="1">
<summary>Answers and verification guidance for 8.4-A–D</summary>

**A.** With the full index 3i+μ,

$$
(\rho_A)_{01}=\rho_{0,3}+\rho_{1,4}+\rho_{2,5}.
$$

The identity on the discarded factor supplies δνμ. Dividing by three would give total trace 1/3, not a density, for a normalized joint input. Product entries CᵢⱼDμν give CᵢⱼTrD. The Δ argument gives a sum of squared entry magnitudes, all forced to zero. The finite frame alternatively fixes every diagonal entry and both real components of every upper-triangle entry, with the minus sign for the Y expectation as in 8.4.3.

**B.** Let i=2b₃+b₁ and μ=2b₀+b₂. Reinsert the bits into the declared full order:

$$
\begin{aligned}
\ell(i,\mu)
 &=8\lfloor\mu/2\rfloor
   +4(i\bmod2)\\
 &\quad+2(\mu\bmod2)+\lfloor i/2\rfloor.
\end{aligned}
$$

Use Σμρℓ(i,μ),ℓ(j,μ). Reversing the retained tuple permutes both matrix axes with (0,2,1,3). For the mixture, each retained entry is .29 times the chain reduction plus .71 times the product reduction. The transfer checks complete complex matrices and native probabilities; agreement only on the diagonals would not test all local expectations.

**C.** For the discarded q1 unitary, trace consistency and unitarity force the same density on (q2,q0), regardless of the entanglement of the input. The biased Bell local densities are diag(cos²(1.07/2),sin²(1.07/2)), independent of φ. A Z record on B selects the corresponding A basis density with those unequal probabilities; ignoring the record recovers the prior local density. The full ignored state loses its 00–11 coherence. At φ=π/2, XX vanishes but XY=sin(1.07), so zero XX alone does not imply that the joint coherence is absent.

**D.** The mathematical empty retained space gives [TrM], whereas the measured native empty request returned the full register matrix in this version. One explicit positive complex 3×2 example is the mixture with weights (.4,.6) of

$$
\begin{aligned}
|u\rangle&=(1,i,0,0,0,0)^\mathsf{T}/\sqrt2,\\
|v\rangle&=(0,0,1,0,0,i)^\mathsf{T}/\sqrt2.
\end{aligned}
$$

Its retained density is diag(.4,.3,.3); the full off-diagonal entries include −.2i at (0,1) and −.3i at (2,5), with their conjugates. Its trace is one and it is positive by construction. Scalar contraction equals `einsum('imjm->ij', M.reshape(3,2,3,2))`. The nine Hermitian probes of the retained dimension reconstruct the same matrix. Multiplying M by a positive branch weight p multiplies the reduced operator and its trace by p; it does not normalize it. Dimension-one cases reduce to the trace or to the identity map as appropriate. These are classical finite-matrix checks, not native non-qubit preparation or a sampled measurement.

</details>

**Sources and proof scope.** The frozen source locator is NC §2.4.3, printed page 105 (contents locator checked; no new full-text NC review claimed). We also inspected [Watrous, author-hosted manuscript §2.1.3, printed pages 67–68](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf#page=75) for coordinate and retained-register conventions. The local-expectation derivation, positivity and uniqueness arguments are supplied explicitly here. Independent mathematical review, implementation review and reader trial remain pending; this is an author-verified draft rather than formal acceptance.

<!-- end-section-8.4 -->

<span id="sec-density-matrices-reduced-states-and-purification-5"></span>

## 8.5 Reduced states of entangled systems

A joint system can have a completely specified pure state while neither subsystem has a pure state of its own. This does not contradict normalization or the uniqueness of partial trace. The missing local information is tied to correlations with the other subsystem. We will make that statement precise by proving that the nonzero eigenvalues of either reduced density are the squared Schmidt coefficients of the joint vector, including their multiplicities.

The frozen prerequisites are [7.2, Schmidt decomposition](ch-entanglement-and-quantum-information-protocols.md#sec-entanglement-and-quantum-information-protocols-2), and [8.4, the unique operational partial trace](#sec-density-matrices-reduced-states-and-purification-4). This section has depth **F**. We insert the Schmidt form into the joint density, trace each side explicitly, identify all eigenvectors and zero complements, and then derive the pure/mixed consequences. The result assumes a **normalized bipartite pure global state**. A matrix representing a mixed global state does not have a single statevector to which this argument can be applied.

All spaces are finite and nonzero. Choose ordered orthonormal bases on A and B. State coefficients, probabilities and purities are dimensionless; native gate angles are radians. The code uses actual released FlagQuantum 0.3.1 full and selected density outputs on CPU complex128, together with native Pauli expectations. SVD, eigenvalues and purities are explicit host calculations. Deterministic comparisons use absolute tolerance $10^{-12}$ and relative tolerance zero. These numerical diagnostics do not certify exact physical rank or establish a theorem from finitely many tests.

The eight Python units are cumulative and run from the repository root. The complete companion is [reduced_spectra.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/reduced_spectra.py). All computed singular values and native density eigenvalues are retained. Native qubit selections are explicit nonempty tuples; one-dimensional mathematical factors are checked separately on the host, rather than inferred from an empty native request.

### 8.5.1 Insert the Schmidt form and trace both sides

From 7.2, a normalized joint vector admits a Schmidt form

$$
\begin{aligned}
|\psi\rangle&=\sum_{k=1}^{r}s_k|a_k\rangle|b_k\rangle,\\
s_k&>0,\qquad\sum_ks_k^2=1,
\end{aligned}
$$

where the a vectors are orthonormal in A, the b vectors are orthonormal in B, and r≤min(d_A,d_B). Here r counts the strictly positive coefficients in exact mathematics. Zero terms may be added for bookkeeping but do not increase Schmidt rank. Normalization follows because the tensor-product inner products give δkl on both sides, leaving Σks_k².

Form the full density before removing anything:

$$
\rho_{AB}
 =\sum_{k,l}s_ks_l
 |a_k\rangle\langle a_l|\otimes|b_k\rangle\langle b_l|.
$$

The partial-trace rule of 8.4 gives, for any local vectors,

$$
\begin{aligned}
\operatorname{Tr}_B
 (|x\rangle\langle y|\otimes|u\rangle\langle v|)
 &=|x\rangle\langle y|\sum_\mu
 \langle\mu|u\rangle\langle v|\mu\rangle\\
 &=\langle v|u\rangle\,|x\rangle\langle y|.
\end{aligned}
$$

The second equality uses the resolution of identity on the discarded factor. Applying it to every joint term, orthonormality supplies ⟨b_l|b_k⟩=δlk:

$$
\begin{aligned}
\rho_A&=\sum_{k,l}s_ks_l
 \langle b_l|b_k\rangle\,|a_k\rangle\langle a_l|\\
&=\sum_ks_k^2|a_k\rangle\langle a_k|.
\end{aligned}
$$

Tracing A independently instead supplies ⟨a_l|a_k⟩=δlk:

$$
\begin{aligned}
\rho_B&=\sum_{k,l}s_ks_l
 \langle a_l|a_k\rangle\,|b_k\rangle\langle b_l|\\
&=\sum_ks_k^2|b_k\rangle\langle b_k|.
\end{aligned}
$$

Both reductions are therefore normalized positive operators. Their diagonal mixtures refer to their respective Schmidt bases; they are not generally diagonal in the computational bases used by a program.

To match this proof to complex coordinates, write ψᵢμ=Cᵢμ. Direct partial-trace entries give

$$
\begin{aligned}
\rho_A&=CC^\dagger,\\
(\rho_B)_{\mu\nu}
 &=\sum_iC_{i\mu}C_{i\nu}^*,\\
\rho_B&=C^\mathsf{T}C^*.
\end{aligned}
$$

The star here means entrywise conjugation. It is essential: C†C is the transpose of the physical B matrix in this coefficient convention. It has the same eigenvalues but can predict the wrong local Y expectation. For a thin SVD C=U diag(s)V†, the B Schmidt columns are V*, which in PyTorch is `Vh.T`. Reconstruction is `(U*s) @ B.T`, with no conjugate on that final transpose.

The code below visibly prepares a rotated complex pair, requests both native reductions, and compares complete matrices and eigenpair residuals. It also exposes the conjugation error: checking only the spectrum would miss the wrong B state.

```python
import math
import torch
import flagquantum as fq
from examples.foundations import reduced_spectra as g
from examples.foundations import statistical_ensembles as e
from examples.foundations import partial_trace as t
theta=.83;phi=-.49
L=e.prepare(e.qubit(.63,.31));R=e.prepare(e.qubit(-.82,-.47))
C=L@torch.diag(e.qubit(theta,phi))@R.T
c=fq.Circuit(2,dtype=g.D).RY(0,theta=theta).P(0,theta=phi).CX(0,1)
c.unitary(0,unitary=L).unitary(1,unitary=R)
result=fq.run(c,outputs=[fq.density_matrix(name='full'),
    fq.density_matrix(qubits=(0,),name='A'),fq.density_matrix(qubits=(1,),name='B'),
    fq.expectation(fq.Y(1),name='yB')],options=e.OPTIONS)
g.RUNS+=1
full=result.measurement('full').value[0]
RA=result.measurement('A').value[0];RB=result.measurement('B').value[0]
e.close(full,torch.outer(C.reshape(-1),C.reshape(-1).conj()))
U,s,B,la,lb=g.inspect_reductions(C,RA,RB)
e.close(RA,C@C.mH);e.close(RB,C.T@C.conj())
wrong=C.mH@C
e.close(torch.linalg.eigvalsh(wrong),torch.linalg.eigvalsh(RB))
correct_y=result.expectation('yB')[0].item();wrong_y=torch.trace(wrong@e.Y).real.item()
assert abs(correct_y-wrong_y)>.1
print('Schmidt squares:',[round(x,9) for x in s.square().tolist()])
print('Native B Y=%.9f;wrong C-dagger-C predicts Y=%.9f'%(correct_y,wrong_y))
```

```text
Schmidt squares: [0.83743788, 0.16256212]
Native B Y=0.223468856;wrong C-dagger-C predicts Y=-0.223468856
```

### 8.5.2 Identify every eigenvalue, including the zero complements

Act on a Schmidt vector a_j with the derived A operator. Orthogonality gives

$$
\rho_A|a_j\rangle
 =\sum_ks_k^2|a_k\rangle\langle a_k|a_j\rangle
 =s_j^2|a_j\rangle.
$$

For any vector x perpendicular to the span of {a_k}, every inner product ⟨a_k|x⟩ vanishes, so ρ_Ax=0. Complete the r Schmidt vectors to an orthonormal basis of H_A. In that complete basis the operator is diagonal with entries s₁²,…,sᵣ² and d_A−r zeros, so there are no additional nonzero eigenvalues. The identical calculation for B gives ρ_Bb_j=s_j²b_j and zero on its orthogonal complement. Therefore

$$
\boxed{\begin{gathered}
\operatorname{spec}_{>0}(\rho_A)
 =\operatorname{spec}_{>0}(\rho_B)\\
 =\{s_1^2,\ldots,s_r^2\}
 \quad\text{with multiplicities}.
\end{gathered}}
$$

Repeated coefficients give repeated eigenvalues. In particular, rankρ_A=rankρ_B=r, even though rankρ_AB=1. If d_A≠d_B, the full spectral lists have different lengths and different numbers of zero eigenvalues. The theorem concerns the nonzero multiset, not equality of differently sized matrices or eigenvectors.

A three-qubit example retains A=(q2,q0) and B=(q1). Its coefficient matrix is 4×2. The thin SVD returns two columns on A, not a complete four-dimensional basis. The full A density still has four eigenvalues, including its zero complement. A thin rectangular matrix must not be submitted as a square native gate.

For portable displayed output, we print the padded Schmidt-square targets. The actual native eigenvalues, including tiny signed floating-point residuals near zero, remain unmodified and are compared against those targets in full. No computed value is clipped or discarded to make the result look exact.

The multiplicity claim can also be written as a pair of characteristic polynomials. For a complex variable z define χ_A(z)=det(zI_A−ρ_A), and likewise χ_B. In the completed orthonormal Schmidt basis the matrices are diagonal. A unitary change back to the computational basis leaves the determinant unchanged, because det(U)det(U†)=det(UU†)=1. Therefore

$$
\begin{aligned}
\chi_A(z)&=z^{d_A-r}\prod_{k=1}^{r}(z-s_k^2),\\
\chi_B(z)&=z^{d_B-r}\prod_{k=1}^{r}(z-s_k^2).
\end{aligned}
$$

A repeated positive weight appears as a repeated factor, not as one eigenvalue after deduplication. The only possible difference between the two full characteristic polynomials is the zero-root multiplicity. This is another consequence of the completed-basis proof, not an inference from matching finitely many polynomial samples. The next code independently compares native-matrix determinants with products of the padded computed Schmidt weights at two complex test points; full matrix/eigenpair comparisons remain in place.

```python
rect_result,rect_data=g.rectangular(.76,-.58)
rect=rect_data[0]
print('A dimension4,B dimension2;thin coefficient shape4x2')
print('A target spectrum:',[round(x,9) for x in g.full_spectrum(rect[1],4).tolist()])
print('B target spectrum:',[round(x,9) for x in g.full_spectrum(rect[1],2).tolist()])
e.close(rect[3],g.full_spectrum(rect[1],4));e.close(rect[4],g.full_spectrum(rect[1],2))
for local,dimension in ((rect_result.measurement('A0').value[0],4),(rect_result.measurement('B0').value[0],2)):
    for z in (.23+.31j,-.41+.19j):
        target=g.full_spectrum(rect[1],dimension).to(g.D)
        e.close(torch.linalg.det(z*torch.eye(dimension,dtype=g.D)-local),torch.prod(z-target))
print('Complete spectra match Schmidt squares with their own zero complements')
```

```text
A dimension4,B dimension2;thin coefficient shape4x2
A target spectrum: [0.789186398, 0.210813602, 0.0, 0.0]
B target spectrum: [0.789186398, 0.210813602]
Complete spectra match Schmidt squares with their own zero complements
```

### 8.5.3 Prove when global purity implies local mixedness

A pure joint vector is a product exactly when r=1, as proved in 7.2. The reduced-state expressions now give an equivalent local criterion. If r=1, normalization forces s₁=1, so ρ_A=|a₁⟩⟨a₁| and ρ_B=|b₁⟩⟨b₁| are pure. Conversely, if either reduction is pure, it has rank one, so the spectral result forces r=1 and the joint vector is a product. Thus, under the pure-global hypothesis,

$$
\begin{gathered}
|\psi\rangle\text{ is a product}
 \ \Longleftrightarrow\ \rho_A\text{ is pure}\\
\Longleftrightarrow\ \rho_B\text{ is pure}.
\end{gathered}
$$

Equivalently, a bipartite pure state is entangled exactly when both its reductions are mixed. A local mixed density is not a failure to specify the global pure vector. It is the unique state reproducing experiments on that local subsystem while the other subsystem is inaccessible.

For completeness, the purity criterion needed here follows directly from the reduced spectrum, without adding an unstated prerequisite. For any positive, unit-trace spectrum λ_i,

$$
1-\operatorname{Tr}(\rho^2)
 =\sum_i\lambda_i(1-\lambda_i)\geq0.
$$

Equality requires each λ_i to be zero or one; their sum is one, so exactly one is one. This is precisely a normalized rank-one projector. For the two reductions,

$$
\boxed{\operatorname{Tr}(\rho_A^2)
 =\operatorname{Tr}(\rho_B^2)
 =\sum_ks_k^4.}
$$

For r≥2, at least two positive λ_i lie strictly below one, so the common local purity is strictly less than one. The full projector always obeys ρ_AB²=ρ_AB and purity one. There is no requirement that a subsystem share that global purity.

One can also quantify the distinction at fixed exact Schmidt rank. Put λ_k=s_k² for the r positive weights. Expanding a sum of real squares gives

$$
\sum_{k=1}^{r}(\lambda_k-1/r)^2
=\sum_k\lambda_k^2-1/r\geq0.
$$

Thus the common reduced purity is at least 1/r, with equality exactly when all positive Schmidt weights equal 1/r. This is uniformity on the occupied Schmidt subspace; when r is smaller than d_A, it is not the full ambient density I_A/d_A. In conjunction with the upper bound just proved, r=1 gives purity one, while r>1 permits globally pure states with strictly mixed local descriptions. These are exact statements about the declared pure bipartition, not numerical rank estimates.

A product preparation and a Bell preparation exhibit the difference in actual native density outputs. The trace squares are explicit host calculations on those matrices.

```python
cp,vp=t.preparation(2,.61,-.34,kind='product')
product,product_data=g.query(cp,vp,(((0,),(1,)),))
bell,bell_C,bell_data=g.pair(math.pi/2,0.)
for label,r,data in (('product',product,product_data[0]),('Bell',bell,bell_data)):
    global_density=r.measurement('full').value[0]
    local_density=r.measurement('A0').value[0]
    global_purity=torch.trace(global_density@global_density).real.item()
    local_purity=torch.trace(local_density@local_density).real.item()
    e.close(global_purity,1);e.close(local_purity,data[1].pow(4).sum())
    print(label+':global purity=%.6f,local purity=%.6f'%(global_purity,local_purity))
```

```text
product:global purity=1.000000,local purity=1.000000
Bell:global purity=1.000000,local purity=0.500000
```

### 8.5.4 Keep small Schmidt weights and numerical resolution distinct

For the exact family

$$
|\psi_\varepsilon\rangle
 =\sqrt{1-\varepsilon^2}|00\rangle
  +e^{i\phi}\varepsilon|11\rangle,
 \qquad0<\varepsilon<1,
$$

the joint state is entangled and both local spectra are (1−ε²,ε²). Their purity is

$$
(1-\varepsilon^2)^2+\varepsilon^4
 =1-2\varepsilon^2+2\varepsilon^4<1.
$$

The phase does not enter either local spectrum. At ε=10⁻¹⁰ the small singular value is 10⁻¹⁰, while its local weight is 10⁻²⁰. A threshold on singular values and a threshold on density eigenvalues have different scales: an exact comparison s>τ corresponds to s²>τ², not s²>τ. Generic floating-point perturbations can further obscure a small eigenvalue in a rotated matrix.

The example retains the small value and reports how a declared singular-value resolution changes the count. It does not equate that count with exact Schmidt rank. A purity rounded to one cannot establish that the state is a product. Nor does a numerical PSD check provide an interval enclosure of all physical eigenvalues. The particular near-product native gate is verified at ε=10⁻¹⁰ in both tested modes; no inference about arbitrarily smaller rotation angles follows from it.

```python
epsilon=1e-10
near,near_C,near_data=g.pair(2*math.asin(epsilon),.37,mode='density_matrix')
near_s=near_data[1]
tiny=near.measurement('A0').value[0,1,1].real.item()
assert tiny>0 and abs(tiny-epsilon**2)<1e-30
print('Small Schmidt coefficient=%.3e;native local weight=%.3e'%(near_s[1].item(),tiny))
print('Resolved singular values:tau1e-9=%d,tau1e-12=%d'%(g.resolved(near_s,1e-9),g.resolved(near_s,1e-12)))
print('Rounded local purity=%.12f;no exact product claim follows'%torch.trace(near.measurement('A0').value[0]@near.measurement('A0').value[0]).real.item())
```

```text
Small Schmidt coefficient=1.000e-10;native local weight=1.000e-20
Resolved singular values:tau1e-9=1,tau1e-12=2
Rounded local purity=1.000000000000;no exact product claim follows
```

### 8.5.5 Equal eigenvalues do not select unique Schmidt vectors

A reduced density determines its eigenspaces, but eigenvectors can acquire arbitrary phases. For a nondegenerate Schmidt pair, replacing a_k by e^{iχ_k}a_k and b_k by e^{−iχ_k}b_k preserves the joint term and both outer products. Independent arbitrary phases on the two vectors would generally change their joint product.

Within a block of m equal positive coefficients s, let W be an m×m unitary. Define a′_j=Σka_kW_kj and b′_j=Σlb_lW*_lj. Then

$$
\begin{aligned}
\sum_j s\,|a'_j\rangle|b'_j\rangle
 &=s\sum_{k,l}\left(\sum_jW_{kj}W_{lj}^*\right)
 |a_k\rangle|b_l\rangle\\
 &=s\sum_k|a_k\rangle|b_k\rangle.
\end{aligned}
$$

The conjugate paired rotation is what cancels the mixing. Both reduced operators remain s² times the corresponding occupied-space projector on that block. Hence two correct SVD implementations need not return the same individual vectors or column phases. Compare the reconstructed full vector, the reduced operators, eigenpair residuals and occupied subspaces as appropriate, rather than rejecting a solution because arbitrary basis columns differ.

The Bell-weight example deliberately changes its Schmidt columns while preserving the joint vector and both native marginal matrices. This is a check of basis freedom, not an assertion that every spectrum is degenerate.

```python
degenerate,deg_C,deg_data=g.pair(math.pi/2,.47,.63,-.82)
DU,ds,DB=deg_data[:3];W=e.prepare(e.qubit(.71,.33))
changed_U=DU@W;changed_B=DB@W.conj()
e.close((changed_U*ds)@changed_B.T,deg_C)
e.close((changed_U*ds.square())@changed_U.mH,degenerate.measurement('A0').value[0])
e.close((changed_B*ds.square())@changed_B.mH,degenerate.measurement('B0').value[0])
assert torch.linalg.matrix_norm(changed_U-DU).item()>.1
print('Degenerate weights:',[round(x,6) for x in ds.square().tolist()])
print('Paired conjugate basis rotation preserves global vector and both reduced operators')
```

```text
Degenerate weights: [0.5, 0.5]
Paired conjugate basis rotation preserves global vector and both reduced operators
```

### 8.5.6 Declare the partition before comparing spectra

Local unitaries L on A and R on B transform a coefficient matrix as C′=LCRᵀ. The transpose, rather than the adjoint, follows by expanding the two ket factors. Consequently

$$
\begin{aligned}
\rho'_A&=L\rho_AL^\dagger,\\
\rho'_B&=R\rho_BR^\dagger.
\end{aligned}
$$

A unitary conjugation preserves each full spectrum: an eigenvector x with eigenvalue λ maps to Lx or Rx with the same eigenvalue, including its multiplicity. Internal reordering of the qubits within a factor also acts by a unitary permutation of its coordinates, as established in 8.4, and preserves these spectra.

Changing **which qubits belong to the factor** is a different bipartition. For a Bell pair on q0,q2 and an independent pure q1, the cut (q2,q0)|(q1) has Schmidt rank one: it separates two pure factors. The cut (q0)|(q1,q2) cuts the Bell pair and has weights (.5,.5). Both statements describe the same global vector. There is no partition-free local-mixedness number for an arbitrary composite register.

The companion also checks rotated pairs against their analytic weights. The code below uses one three-qubit native preparation to verify the two different cuts and confirms invariance under reversing the internal order of the Bell-pair factor.

```python
spectator,spectator_data=g.spectator(.43)
for label,data in zip(('A=(q2,q0),B=(q1)','A=(q0),B=(q1,q2)'),spectator_data):
    print(label+':Schmidt squares='+str([round(x,6) for x in data[1].square().tolist()]))
full3=spectator.measurement('full').value[0]
e.close(torch.linalg.eigvalsh(t.indexed(full3,3,(2,0))),torch.linalg.eigvalsh(t.indexed(full3,3,(0,2))))
print('Internal tuple reversal leaves eigenvalues unchanged;changing the partition need not')
```

```text
A=(q2,q0),B=(q1):Schmidt squares=[1.0, 0.0]
A=(q0),B=(q1,q2):Schmidt squares=[0.5, 0.5]
Internal tuple reversal leaves eigenvalues unchanged;changing the partition need not
```

### 8.5.7 State what the pure-global theorem does not establish

The local spectra do not reconstruct the global phase correlations, even when global purity is known. The orthogonal pure states Φ⁺=(|00⟩+|11⟩)/√2 and Φ⁻=(|00⟩−|11⟩)/√2 both have local densities I/2. Their global XX expectations are +1 and −1, respectively. Thus even both complete marginals can leave distinct pure joint states unresolved.

More importantly, the pure-global assumption cannot be dropped. The classical product ensemble

$$
\rho_{\mathrm{classical}}
 =\tfrac12|00\rangle\langle00|
  +\tfrac12|11\rangle\langle11|
$$

also has both marginals I/2, but global purity .5. It is an explicit mixture of product preparations; mixed local states alone do not certify entanglement of an arbitrary joint density. There is no single Schmidt vector decomposition of this global mixture to insert into the pure-state proof.

Conversely, the mixed product density

$$
\rho_{\mathrm{product}}
 =\frac{I_A}{2}\otimes|0\rangle\langle0|_B
$$

has A spectrum (.5,.5) and B spectrum (1,0). The nonzero spectra need not agree for a mixed joint input. One pure marginal in this example does not make the global state pure. These examples delimit the theorem rather than contradict it.

Three actual native product preparations supply the two host mixtures. A further native Φ⁻ preparation is compared with the earlier Φ⁺ result. The code compares full local matrices and global correlations, not merely one local measurement distribution.

```python
basis_results=[g.basis(bits) for bits in ((0,0),(1,1),(1,0))]
r00,r11,r10=[r.measurement('full').value[0] for r in basis_results]
classical=(r00+r11)/2
independent=(r00+r10)/2
for q in (0,1):e.close(t.indexed(classical,2,(q,)),e.I/2)
e.close(torch.trace(classical@classical),.5)
minus,minus_C,minus_data=g.pair(math.pi/2,math.pi)
for name in ('A0','B0'):e.close(minus.measurement(name).value,bell.measurement(name).value)
print('Bell plus/minus:same local states,global XX=%.6f/%.6f'%(bell.expectation('xx')[0].item(),minus.expectation('xx')[0].item()))
print('Classical product mixture:global purity=%.6f,local purities=.5/.5'%torch.trace(classical@classical).real.item())
print('Mixed product example A spectrum:',[round(x,6) for x in torch.linalg.eigvalsh(t.indexed(independent,2,(0,))).flip(0).tolist()])
print('Mixed product example B spectrum:',[round(x,6) for x in torch.linalg.eigvalsh(t.indexed(independent,2,(1,))).flip(0).tolist()])
```

```text
Bell plus/minus:same local states,global XX=1.000000/-1.000000
Classical product mixture:global purity=0.500000,local purities=.5/.5
Mixed product example A spectrum: [0.5, 0.5]
Mixed product example B spectrum: [1.0, 0.0]
```

### 8.5.8 Preserve complete spectra and the scope of the implementation

The mathematical proof handles different factor dimensions and their zero complements. A one-dimensional factor has the single density eigenvalue one for a normalized pure joint input, and the other factor is pure. The host SVD and matrix references check 1×4 and 4×1 coefficient matrices; they do not issue an empty native qubit selection. In the tested 0.3.1 interface an empty density tuple requests the full register, as documented in 8.4, so it must not stand for a one-dimensional factor in these experiments.

A uniform Schmidt distribution on r terms has local density Π/r on each occupied support, where Π projects onto its Schmidt span. Its purity is 1/r. It is maximally mixed on the whole factor only if r equals that factor's full dimension. For a 4×2 coefficient matrix with two equal coefficients, B can be I₂/2 while A has spectrum (.5,.5,0,0), not I₄/4.

Purity is also only one scalar function of the spectrum. For example, the nonnegative normalized weight lists (.5,.5,0) and (2/3,1/6,1/6) have the same sum of squares .5 but different spectra and ranks. Both can occur as the local spectra of pure joint vectors by taking a diagonal coefficient matrix with entries √λ_i. The host checks below verify this finite-matrix example; they do not claim a native qutrit experiment or a complete ordering of entanglement resources by purity.

Malformed coefficient arrays, overlapping or incomplete partitions, nonfinite values, invalid factor dimensions and undeclared thresholds are rejected by the teaching contracts. Their factor-dimension≤4 bound limits dense independent references, not FlagQuantum itself. All computed singular values are kept, and numerical local eigenvalues are not clipped. Padding the predicted spectrum with exact mathematical zero complements is a comparison target, not a repair to the actual output.

```python
flat=torch.zeros((4,2),dtype=g.D);flat[0,0]=flat[1,1]=1/math.sqrt(2)
g.inspect_reductions(flat,flat@flat.mH,flat.T@flat.conj())
for weights in ((.5,.5,0.),(2/3,1/6,1/6)):
    coeff=torch.diag(torch.tensor(weights,dtype=g.D).sqrt())
    data=g.inspect_reductions(coeff,coeff@coeff.mH,coeff.T@coeff.conj())
    e.close(data[1].pow(4).sum(),.5)
print('%d malformed contracts rejected;dimension-one host factors checked'%g.invalid_checks())
print('All computed singular values and native eigenvalues retained;zero padding is not clipping')
print('%d actual native body circuits;SVD and spectra are host calculations'%g.RUNS)
```

```text
12 malformed contracts rejected;dimension-one host factors checked
All computed singular values and native eigenvalues retained;zero padding is not clipping
11 actual native body circuits;SVD and spectra are host calculations
```

**Actual API support and limits.** The real native requests here are `fq.density_matrix(qubits=..., name=...)` and Pauli-based `fq.expectation`; they run in both `statevector` and `density_matrix` modes. Full and selected matrices have a leading batch axis, explicitly indexed by zero. These native reductions are compared with a separately derived normalized vector for the known preparation circuit, and the native full matrix is first checked against that vector's outer product. Using an analytic vector in the density-matrix mode is an independent preparation reference, not a claimed statevector output for a generic mixed state.

Schmidt decomposition, `torch.linalg.svd`, `torch.linalg.eigvalsh`, rank-resolution counts and trace-square purities are host calculations. They are not presented as native Schmidt measurements or hardware tomography. Local unitaries are square preparation/gate matrices; thin rectangular SVD factors are never submitted as unitary gates. No noise, arbitrary mixed-state initializer, sampled collapse or reset interface is inferred or invoked. Host mixtures of native pure components remain explicitly labelled.

As in 8.4, a small selected density does not imply a cheap simulation: the inspected statevector density-output route builds a full density first and has its documented source guard, while density-matrix mode already stores the joint matrix. This section is a correctness laboratory, not a scaling or performance benchmark. Conditional-state protocols, purification nonuniqueness and entropic measures have their own later sections; the proof here concerns the specified pure input and bipartition.

Expected output of the complete program:

```text
24 native rotated/unrotated pairs:Schmidt squares,eigenpair residuals,full marginal spectra and purities passed.
4 native complex three-qubit circuits:4x2and2x4coefficient matrices retain unequal zero complements.
6 native spectator-pair circuits:partition changes spectra;internal tuple reordering only changes coordinates.
4 native near-product cases:positive1e-20weight retained;singular-value threshold is a resolution diagnostic.
6 native product components:host mixed counterexamples show why global purity is an essential hypothesis.
12 malformed contracts rejected;host dimension-one spectra and all computed singular values retained.
44 actual native circuits;SVD,eigenspectra,purities and mixed ensemble sums are explicit host calculations.
```

The complete program executes 44 native circuits: 24 rotated/unrotated pairs, four rectangular-cut preparations, six spectator-pair preparations, four near-product cases and six product components for mixed counterexamples. The body executes 11 additional circuits. SVDs, eigenvalue comparisons and host mixtures are not additional quantum executions. The execution ledger separately records the body/complete checker, fresh transfer cases and previous-section regressions. Independent mathematical review, implementation review and reader trial remain pending.

### Understanding checks and transfer exercises

**8.5-A — Prove the spectral statement with multiplicities.** Insert a normalized Schmidt form into ρ_AB and perform both partial traces. Explain why orthonormality removes k≠l terms and why completing the Schmidt vectors with orthogonal vectors supplies only zero eigenvalues. For d_A=4,d_B=2 and r=2, how many zero eigenvalues occur on each side? Why can the full density have rank one when both reduced ranks are two?

**8.5-B — Fresh complex rotations and conjugation.** Use θ=1.17, φ=.62 and local gates L=prepare(qubit(−.53,.31)), R=prepare(qubit(.91,−.47)) in the pair construction. Derive both reduced matrices, their full spectra and common purity. Compare native reductions, scalar partial traces, eigenpair residuals and SVD reconstruction. Deliberately use C†C for B and find a native observable that rejects it despite matching eigenvalues.

**8.5-C — Fresh four-qubit cuts.** Use the chain preparation of 8.4 with θ=−.67, φ=.39. Compare A=(q3,q1), B=(q0,q2) with the reversed internal orders. Then compare A=(q0), B=(q1,q2) for a fresh three-qubit chain preparation with θ=1.23, φ=−.64. Verify full reduced spectra with correct zero complements in both modes. Why must a numerical zero or unresolved coefficient not be treated as an exact physical rank statement? Add a biased Bell pair with θ=.93 and φ=−.72 to check the analytic local purity.

**8.5-D — Equal marginals, equal purity, different conclusions.** Compare the biased pure pair √p|00⟩+e^{iφ}√(1−p)|11⟩ with the classical mixture p|00⟩⟨00|+(1−p)|11⟩⟨11| for p=.68, φ=−.57. Which complete local matrices agree, and which full-state purity or correlation separates them? Then construct the two diagonal 3×3 coefficient examples in 8.5.8 with identical local purity .5 but different spectra. State the global-purity assumption needed before inferring entanglement from a mixed marginal.

<details markdown="1">
<summary>Answers and verification guidance for 8.5-A–D</summary>

**A.** Each discarded outer product has trace equal to the inner product of its bra and ket vectors, hence δlk. The surviving terms have weights s_k². The Schmidt span contains every nonzero action of the reduction; the perpendicular space is its kernel. A has two zero eigenvalues and B none. The full operator is a single projector |ψ⟩⟨ψ| irrespective of how many product terms its vector needs.

**B.** With D=diag(cos(θ/2),e^{iφ}sin(θ/2)), C=LDRᵀ. Therefore

$$
\begin{aligned}
\rho_A&=L\operatorname{diag}(c^2,s^2)L^\dagger,\\
\rho_B&=R\operatorname{diag}(c^2,s^2)R^\dagger,\\
c&=\cos(1.17/2),\qquad s=\sin(1.17/2).
\end{aligned}
$$

The spectra are {c²,s²} and purity c⁴+s⁴. The phase φ enters the joint vector but cancels from these local matrices. Here the correct B Y mean is cos(1.17)sin(.91)sin(−.47), which is nonzero; the wrong transposed B matrix has its opposite sign. The fresh transfer checks this against the native Y query, as well as the complete matrices.

**C.** The 4×4 cut compares four Schmidt squares on each factor. Internal reversals are unitary coordinate permutations and keep those lists unchanged. The fresh 2×4 cut has at most two nonzero weights, with a two-dimensional zero complement on B if its rank is two. The transfer program compares this larger local matrix without submitting thin factors as gates. It compares full native spectra and analytic coefficient contractions without deleting tiny values. The two-qubit analytic check gives local purity cos⁴(.93/2)+sin⁴(.93/2). Resolution thresholds describe what the computation distinguishes at a declared scale; finite precision does not prove exact rank of a physical preparation.

**D.** Both local matrices equal diag(.68,.32). The pure global density has purity one, whereas the classical mixture has purity .68²+.32²=.5648. Their global XY means are 2√(.68·.32)sin(−.57) and zero, so an appropriate joint experiment distinguishes them. For the host 3×3 examples, diagonal C with entries √(.5),√(.5),0 gives local spectrum (.5,.5,0); diagonal entries √(2/3),√(1/6),√(1/6) give (2/3,1/6,1/6). Both yield purity .5. A mixed marginal witnesses pure-state bipartite entanglement only when the specified joint state is known to be pure; it is not a general test for an arbitrary mixed joint state.

</details>

**Sources and proof scope.** The frozen source locator is NC §2.5, printed page 109 (contents locator checked; no new full-text NC review claimed). We also inspected [Watrous, author-hosted manuscript, Eq. (5.112), printed page 271](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf#page=279) for the two reduced Schmidt-form expressions, without importing the surrounding entropy results as prerequisites. The full partial-trace, eigenvalue, zero-complement and pure/mixed derivations are supplied here. This is an author-verified draft, not formal acceptance.

<!-- end-section-8.5 -->

<span id="sec-density-matrices-reduced-states-and-purification-6"></span>
## 8.6 Purification and nonuniqueness

**Question.** Can a density with more than one positive eigenvalue be the local description of a pure joint state? If so, how much freedom remains in that joint description?

The prerequisites are [8.2](#sec-density-matrices-reduced-states-and-purification-2), which supplies the finite spectral and purity criteria, and [8.4](#sec-density-matrices-reduced-states-and-purification-4), which fixes partial trace by local expectations. We use those results directly; no entropy or channel representation theorem is needed. Every space here is finite-dimensional. S denotes the system being described, R a reference register, d its system dimension, m its reference dimension, and I the identity on the indicated factor. Densities, amplitudes and probabilities are dimensionless; all circuit angles are radians.

A **purification** of a density ρ on S is a normalized vector |Ψ⟩ in S⊗R such that Tr_R(|Ψ⟩⟨Ψ|)=ρ. The global density |Ψ⟩⟨Ψ| is pure. Calling ρ mixed says something about the local density; it does not contradict this pure joint description. A reference is a mathematical extension unless a concrete preparation and access model are also specified. Constructing a purification of a *known density matrix* does not purify an unknown physical input by a universal operation.

### 8.6.1 Construct a purification from the spectral data

Write the density in an orthonormal eigenbasis as

$$
\begin{gathered}
\rho=\sum_{k=1}^{r}\lambda_k|u_k\rangle\langle u_k|,\\
\lambda_k>0,\qquad \sum_k\lambda_k=1.
\end{gathered}
$$

Here r is its rank in exact mathematics. Choose r orthonormal reference vectors |f_k⟩ in a space of dimension m≥r and define

$$
|\Psi\rangle=\sum_{k=1}^{r}\sqrt{\lambda_k}
 |u_k\rangle|f_k\rangle.
$$

The square roots are the positive real square roots; phases can instead be included in the reference vectors. The norm squared is Σ_kl√(λ_kλ_l)⟨u_l|u_k⟩⟨f_l|f_k⟩=Σ_kλ_k=1. To verify the local state, expand the *whole* outer product, including its off-diagonal joint terms, before tracing:

$$
\begin{aligned}
&\operatorname{Tr}_R(|\Psi\rangle\langle\Psi|)\\
&\quad=\sum_{k,l}\sqrt{\lambda_k\lambda_l}
 \langle f_l|f_k\rangle|u_k\rangle\langle u_l|\\
&\quad=\sum_k\lambda_k|u_k\rangle\langle u_k|=\rho.
\end{aligned}
$$

Orthogonality of the reference labels removes the local cross terms; they remain present in the joint pure density. This proves existence for any sufficiently large reference. It also tells us exactly what to implement. With Q's columns equal to the u_k, the coefficient matrix in system-row/reference-column coordinates has columns √λ_k u_k. The joint basis index is i·m+μ, and the local density is CC†. `g.spectral` is a book helper that builds these coefficients from supplied nonnegative spectral weights; it is not a FlagQuantum method.

For a qubit with weights (.73,.27), `RY` and `CX` create the correlated reference labels, and a one-qubit Q puts the system in the chosen complex eigenbasis. This first unit shows the actual gates and execution requests explicitly.

```python
import math,torch,flagquantum as fq
from dataclasses import replace
from examples.foundations import purification as g
from examples.foundations import statistical_ensembles as e
p=.73;weights=(p,1-p);Q=e.prepare(e.qubit(.87,-.52))
C,rho=g.spectral(weights,Q,2)
# System q0,reference q1;basis index=2*i+mu.
c=fq.Circuit(2,dtype=g.D).RY(0,theta=2*math.acos(math.sqrt(p))).CX(0,1)
c.unitary(0,unitary=Q)
r=fq.run(c,outputs=[fq.density_matrix(name='full'),
    fq.density_matrix(qubits=(0,),name='S'),
    fq.density_matrix(qubits=(1,),name='R'),
    fq.probabilities(name='p')],options=e.OPTIONS)
full=r.measurement('full').value[0]
e.close(full,torch.outer(C.reshape(-1),C.reshape(-1).conj()))
e.close(r.measurement('S').value[0],rho)
e.close(r.measurement('R').value[0],torch.diag(torch.tensor(weights,dtype=g.D)))
e.close(r.measurement('p').value[0],C.reshape(-1).abs().square())
e.close(torch.trace(full@full),1)
print('Spectral purification:full purity=1,system spectrum=[0.73, 0.27]')
print('System matrix and every computational-basis probability match explicit coefficients')
```

```text
Spectral purification:full purity=1,system spectrum=[0.73, 0.27]
System matrix and every computational-basis probability match explicit coefficients
```

**Check.** Why does replacing the joint vector by the mixture Σ_kλ_k|u_k,f_k⟩⟨u_k,f_k| retain ρ but generally lose global purity? The mixture deletes the off-diagonal *joint* terms that were essential to the rank-one global projector.

### 8.6.2 Prove the ancillary dimension bound is necessary

Let |Ψ⟩ be any purification, and let C be its d×m coefficient matrix. The coordinate partial-trace formula is ρ=CC†. The column range of CC† lies in that of C. In fact the two matrices have the same rank: for any system vector x,

$$
x^\dagger CC^\dagger x=\|C^\dagger x\|^2,
\qquad
\ker(CC^\dagger)=\ker(C^\dagger).
$$

The two kernel inclusions follow in each direction from this displayed norm and multiplication by C. Taking dimensions, rank(CC†)=rank(C†)=rank(C), where the last equality follows from finite matrix row/column rank, or the SVD proved in 2.5. Since C has m columns, r≤m. Together with the construction above this proves

$$
\boxed{\begin{gathered}
\rho\text{ has a purification in }S\otimes R\\
\Longleftrightarrow\\
\dim R\geq\operatorname{rank}\rho.
\end{gathered}}
$$

Zero spectral weights require no reference directions. A pure density needs only a one-dimensional reference; a rank-four density needs at least four dimensions, hence at least two qubits if the reference must be a qubit register. More generally the minimum number of reference qubits is ceil(log₂r), with zero qubits when r=1. This is a dimension lower bound, not a gate-count or efficient-preparation result.

The next unit realizes a four-dimensional system and reference as four qubits. `g.first_column` completes a known normalized vector to a square unitary on the host, and `g.execute` submits that square matrix on integer qubit labels. Its memory and completion costs are discussed below.

```python
Q4=torch.kron(Q,e.prepare(e.qubit(-.63,.41)))
C4,rho4=g.spectral((.1,.2,.3,.4),Q4,4)
r4,_=g.execute(C4,mode='density_matrix')
e.close(r4.measurement('S').value[0],rho4)
try:g.spectral((.1,.2,.3,.4),Q4,2)
except ValueError:print('Rank4density rejects a two-dimensional ancillary space')
else:raise AssertionError('Insufficient ancillary dimension accepted')
print('Four-qubit preparation:system/reference dimensions4x4,full purity=1')
```

```text
Rank4density rejects a two-dimensional ancillary space
Four-qubit preparation:system/reference dimensions4x4,full purity=1
```

**Predict.** A rank-two density on a four-dimensional system needs a two-dimensional reference, not necessarily a four-dimensional one. The 4×2 cases in the complete program check this distinction.

### 8.6.3 Show that ancillary unitaries preserve the local density

Let U be any unitary on R and |Φ⟩=(I_S⊗U)|Ψ⟩. If C contains Ψ's coefficients, then

$$
C'_{i\nu}=\sum_{\mu}U_{\nu\mu}C_{i\mu},
\qquad C'=CU^T.
$$

This is a transpose, not an adjoint: a ket's coefficients transform without complex conjugating U. Consequently

$$
C'C'^\dagger
=C U^T U^* C^\dagger
=C C^\dagger=\rho,
$$

because UᵀU*=I is the complex conjugate of U†U=I. The reference density σ=CᵀC* instead becomes UσU†. Thus system statistics remain fixed while the joint vector and reference statistics can change. The equality holds for every local system effect E, since its probability is Tr(ρE); no local measurement can identify the chosen ancillary rotation.

```python
W=e.prepare(e.qubit(-.76,.68))
rotated,CW=g.execute(C,W)
e.close(rotated.measurement('S').value[0],rho)
e.close(rotated.measurement('R').value[0],W@torch.diag(torch.tensor(weights,dtype=g.D))@W.mH)
assert torch.linalg.vector_norm(CW-C).item()>.1
wrong=C@W.mH
assert torch.linalg.vector_norm(wrong-CW).item()>.1
print('Ancillary unitary preserves the complete system density but changes the joint vector')
print('Coefficient update is C@W.T;C@W.mH is rejected as the same target vector')
```

```text
Ancillary unitary preserves the complete system density but changes the joint vector
Coefficient update is C@W.T;C@W.mH is rejected as the same target vector
```

For example, the two Bell vectors with a plus or minus sign between |00⟩ and |11⟩ are different purifications of I/2, related by Z on the reference. A wrong transpose can still produce *some* purification, since another unitary also preserves ρ. Therefore comparing only the system density cannot verify the intended global circuit. We check the full joint density, explicit transformed coefficients and reference density as well. No phase alignment is used to repair a wrong candidate.

### 8.6.4 Prove every pair is related on the supported ancillary subspace

The converse must include repeated eigenvalues and unused ancillary dimensions. Fix **one** complete orthonormal system eigenbasis {u_k} of ρ, including its kernel, and consider two arbitrary purifications Ψ and Φ of the same ρ. Expand them in this same basis:

$$
\begin{gathered}
|\Psi\rangle=\sum_{k=1}^{d}|u_k\rangle|w_k\rangle,\\
|w_k\rangle=(\langle u_k|\otimes I_R)|\Psi\rangle.
\end{gathered}
$$

Computing the reduced matrix in that basis gives

$$
\langle w_l|w_k\rangle
=\langle u_k|\rho|u_l\rangle
=\lambda_k\delta_{kl}.
$$

For λ_k=0, the equation k=l gives ∥w_k∥²=0, hence w_k=0; there is no hidden component in a zero-eigenvalue system direction. For λ_k>0 define f_k=w_k/√λ_k. The last display shows that the f_k are orthonormal. Performing exactly the same contraction on Φ produces orthonormal g_k with

$$
\begin{gathered}
|\Psi\rangle=\sum_{k=1}^{r}\sqrt{\lambda_k}|u_k\rangle|f_k\rangle,\\
|\Phi\rangle=\sum_{k=1}^{r}\sqrt{\lambda_k}|u_k\rangle|g_k\rangle.
\end{gathered}
$$

Let F and G be the matrices whose columns are f_k and g_k, and define T=GF†. Then TF=G, T†T=FF† and TT†=GG†. In words, T preserves norms and inner products *on the occupied reference span*, and maps it onto the second occupied span. It need not be unitary on the whole reference space: it is zero on the perpendicular complement of the first span. This is called a **partial isometry** here, with its precise two projector identities just given. Since T f_k=g_k term by term, (I⊗T)|Ψ⟩=|Φ⟩.

If both purifications use the same m-dimensional reference space, complete each r-vector orthonormal frame to an m-vector orthonormal basis. Such completion exists: choose a vector outside the current span, subtract its orthogonal projections, normalize the nonzero remainder, and repeat until the finite dimension is exhausted. Map the first completed basis to the second one. The resulting square operator U preserves all basis inner products and is onto, so U†U=UU†=I. It agrees with T on the occupied span, and therefore

$$
\boxed{|\Phi\rangle=(I_S\otimes U_R)|\Psi\rangle.}
$$

This proves the full same-space equivalence theorem, not merely invariance under a proposed rotation. Different choices of the unused basis vectors give different valid extensions. The following unit reconstructs U when the occupied span is already the whole two-dimensional reference; it also checks why a rank-one support map alone is not a full-space unitary.

```python
F=g.support_frames(C,Q,weights);G=g.support_frames(CW,Q,weights)
recovered=G@F.mH
e.close(recovered,W);g.unitary(recovered,2);e.close(C@recovered.T,CW)
Cp,rhop=g.spectral((1.,0.),Q,2)
pure_rotated,CpW=g.execute(Cp,W)
Fp=g.support_frames(Cp,Q,(1.,0.));Gp=g.support_frames(CpW,Q,(1.,0.))
T=Gp@Fp.mH
e.close(T.mH@T,Fp@Fp.mH);e.close(T@Fp,Gp)
assert not torch.allclose(T.mH@T,e.I,atol=g.ATOL,rtol=0)
e.close(W@Fp,Gp)
print('Full ancillary frame recovers W;rank1support map is not a full-space unitary')
print('Known W supplies a valid orthonormal-complement extension')
```

```text
Full ancillary frame recovers W;rank1support map is not a full-space unitary
Known W supplies a valid orthonormal-complement extension
```

**Check.** Multiplying the entire vector Φ by e^{iχ} causes no difficulty: multiply its g_k by the same phase, and extend that supported map. The equality can therefore be stated for actual vectors, not only rays. The extension's action outside the occupied span is not determined by ρ or by the pair of purifications.

### 8.6.5 Handle degeneracy without matching numerical eigenvectors

If λ_1=λ_2, a diagonalization routine may return any orthonormal basis in their shared eigenspace. The proof did not compare two independently computed eigenbases. It fixed one system basis and contracted *both* joint vectors against that basis. This supplies a common frame even in the degenerate case. It also prevents an arbitrary numerical basis choice from being mistaken for a physically different system density.

For ρ=I/2 every system basis is an eigenbasis. The code repeats the supported-frame construction in two complex system bases. Both recover the same chosen U because the reference support is full. For a rank-deficient reference only the supported action would be fixed.

```python
Cd,rhod=g.spectral((.5,.5),e.I,2)
Ud=e.prepare(e.qubit(.91,-.36))
degenerate,CdU=g.execute(Cd,Ud)
Fd=g.support_frames(Cd,e.I,(.5,.5));Gd=g.support_frames(CdU,e.I,(.5,.5))
e.close(Gd@Fd.mH,Ud);e.close(degenerate.measurement('S').value[0],e.I/2)
V=e.prepare(e.qubit(-.57,.44))
# Both columns' eigenvalues are equal;choose any fixed system eigenbasis V.
Fv=g.support_frames(Cd,V,(.5,.5));Gv=g.support_frames(CdU,V,(.5,.5))
e.close(Gv@Fv.mH,Ud)
print('Degenerate spectrum:the common-eigenbasis proof recovers the same ancillary unitary')
```

```text
Degenerate spectrum:the common-eigenbasis proof recovers the same ancillary unitary
```

The familiar freedom to rotate paired Schmidt vectors inside a degenerate block is consistent with this result. Nothing here asserts that the separately returned columns of two numerical eigensolvers agree, or that a small eigenvalue has been mathematically proved zero.

### 8.6.6 Distinguish unequal reference dimensions from a square unitary

Suppose Ψ uses R of dimension m and Φ uses R′ of dimension n. The same common-system-basis proof still produces the support map T=GF†, now an n×m matrix with T†T=FF† and TT†=GG†. If n≥m, complete the f frame to a basis of R and extend the g frame to m orthonormal vectors in R′. This defines an **isometry** J:R→R′ with J†J=I_R and J f_k=g_k. Hence Φ=(I⊗J)Ψ. Usually JJ† is only a projector, not I_R′.

If n<m, an isometry on all of R cannot exist: m orthonormal vectors cannot fit into n dimensions. The supported partial isometry still works, or one can reverse the isometry direction. Another equivalent statement embeds both references in a common larger space; their padded vectors are then related by a unitary there. These dimension qualifications are part of the theorem.

```python
J=torch.zeros((4,2),dtype=g.D);J[0,0]=1;J[3,1]=1j
e.close(J.mH@J,e.I)
enlarged,CJ=g.execute(C@J.T)
e.close(enlarged.measurement('S').value[0],rho)
e.close(enlarged.measurement('R').value[0],J@torch.diag(torch.tensor(weights,dtype=g.D))@J.mH)
try:g.unitary(J,2)
except ValueError:print('Rectangular isometry is not submitted as a square unitary gate')
else:raise AssertionError('Rectangular gate accepted')
print('Three-qubit pure preparation realizes the larger coefficient matrix;system density unchanged')
```

```text
Rectangular isometry is not submitted as a square unitary gate
Three-qubit pure preparation realizes the larger coefficient matrix;system density unchanged
```

In this example J embeds |0⟩ as |00⟩ and |1⟩ as i|11⟩. Mathematically it maps C to CJᵀ. The implementation prepares the resulting larger pure vector with a square unitary on three qubits. It does **not** pass the rectangular J to `Circuit.unitary`, and does not claim a native isometry compiler or physical register-allocation endpoint. A known extension to a square gate on a larger initialized register would be another implementation, with its initialization contract made explicit.

### 8.6.7 Build a purification from a nonorthogonal ensemble

Spectral data give a convenient existence proof, but they are not required for a construction. For any finite ensemble ρ=Σ_j p_j|v_j⟩⟨v_j| of normalized system kets, choose orthonormal reference labels |j⟩ and set

$$
|\Omega\rangle=\sum_j\sqrt{p_j}|v_j\rangle|j\rangle.
$$

The system vectors v_j need not be mutually orthogonal. The norm is Σ_jp_j=1 because the labels are orthogonal, and tracing the labels gives the stated ensemble density. The reference matrix has entries

$$
(\sigma_R)_{jk}=\sqrt{p_jp_k}\langle v_k|v_j\rangle.
$$

It need not be diagonal, and its diagonal probabilities need not be the eigenvalues of ρ. Ensemble length may exceed rank; the previous support theorem still applies. This is how two apparently different ensemble descriptions can yield different purifications with the same system density. It does not turn the purifying label into a uniquely determined record of how an actual sample was prepared.

```python
vectors=(e.qubit(0.,0.),e.qubit(math.pi/2,.59))
E=g.ensemble_coeff((.4,.6),vectors)
ensemble_run,_=g.execute(E)
rhoE=e.rho((.4,.6),vectors)
e.close(ensemble_run.measurement('S').value[0],rhoE)
lam,EV=torch.linalg.eigh(rhoE)
Cs,_=g.spectral(tuple(lam.tolist()),EV,2)
spectral_run,_=g.execute(Cs)
Fs=g.support_frames(Cs,EV,tuple(lam.tolist()))
Gs=g.support_frames(E,EV,tuple(lam.tolist()))
UE=Gs@Fs.mH;g.unitary(UE,2);e.close(Cs@UE.T,E)
e.close(spectral_run.measurement('S').value,ensemble_run.measurement('S').value)
assert abs(torch.vdot(vectors[0],vectors[1]).item())>.1
assert abs((E.T@E.conj())[0,1].item())>.1
print('Nonorthogonal ensemble kets with orthogonal reference labels purify the same density')
print('Reference density has nonzero off-diagonal entries;it is not merely the probability list')
```

```text
Nonorthogonal ensemble kets with orthogonal reference labels purify the same density
Reference density has nonzero off-diagonal entries;it is not merely the probability list
```

Here a host eigendecomposition of the known two-dimensional ρ supplies a second spectral purification. The native outputs verify both system densities. Host contraction against the same eigenbasis constructs a square ancillary unitary relating the two coefficient matrices. This finite check validates the example; the general proof was the common-frame argument above.

### 8.6.8 Preserve normalization, phase and implementation boundaries

The mathematical construction needs orthogonal *reference* labels. Substituting overlapping reference kets can retain extra cross terms and even destroy normalization. Normalizing that incorrect vector afterward changes the candidate and does not validate the original construction. A nonunitary reference matrix also requires a separate physical operation/update contract; it cannot simply be submitted as a unitary gate.

```python
print(f'{g.invalid_checks()} malformed contracts rejected')
C1,rho1=g.spectral((1.,0.),Q,1)
e.close(C1@C1.mH,rho1)
assert C1.shape==(2,1)
# Nonorthogonal reference labels fail even normalization for this example.
f=e.qubit(math.pi/2,0.)
bad=(math.sqrt(.4)*torch.kron(vectors[0],torch.tensor([1,0],dtype=g.D))
     +math.sqrt(.6)*torch.kron(vectors[1],f))
assert abs(torch.vdot(bad,bad).item()-1)>.1
print('Pure density admits a one-dimensional host reference;native examples use nonempty qubit factors')
print('Nonorthogonal reference labels fail the displayed ensemble-purification contract')
```

```text
12 malformed contracts rejected
Pure density admits a one-dimensional host reference;native examples use nonempty qubit factors
Nonorthogonal reference labels fail the displayed ensemble-purification contract
```

The complete executable [purification.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/purification.py) supplies the helpers used above. `first_column` starts with the normalized target vector and uses two-pass orthogonal projection of computational-basis vectors to complete it to a square unitary. It checks the final matrix and its first column before submission. Its 1e-10 completion-pivot threshold concerns numerical basis construction, not a spectral-rank cutoff. `spectral` takes declared weights, preserves every positive one and rejects an insufficient reference dimension; it does not infer exact rank from noisy eigenvalues. In the nonorthogonal two-vector example, all computed eigenvalues are positive and used without clipping.

The tested runtime is Python 3.12.14, released FlagQuantum 0.3.1 and PyTorch 2.13.0 on CPU, complex128. Native calls prepare *pure* circuits, apply square dense unitaries and query full/selected density matrices, probabilities and Pauli expectations in both tested statevector and density-matrix modes. `unitary` takes variadic integer qubit labels; multi-qubit calls use `unitary(*labels, unitary=U)`. Its source was checked after an initial tuple-as-one-label call failed before execution; that record is retained. The density-matrix execution mode does not itself make this an arbitrary mixed-input initialization experiment.

SVD/eigendecomposition, ensemble sums, spectral construction, partial isometries and first-column completion are explicit host mathematics. There is no claim of a native `purify` endpoint, efficient synthesis, recovery of a lost reference, reset, measurement collapse, noise model, hardware calibration or access to an inaccessible environment. The helper accepts system/reference qubit dimensions 2 or 4 for native runs, and host reference dimension 1 for the pure-state boundary. Four-qubit full dense preparation matrices have dimension 16; these teaching memory guards are not FlagQuantum capacity limits. Preparing a known pure joint vector is distinct from using a rectangular matrix as a gate.

Implementation comparisons use absolute tolerance 1e-12 and relative tolerance zero, with no probability clipping, input normalization repair or phase alignment. A positive reference weight 1e-20 is retained in a host boundary check; a floating-point eigenspectrum is not an exact-rank or interval certificate. The initial API failure executed zero circuits. The complete program runs 36 actual circuits; the eight literal body units run eight, including the explicit first unit. Random trials cannot replace the existence or equivalence proofs.

Expected output of the complete program:

```text
24 native qubit purifications:complex spectral construction,ancillary rotation and supported equivalence passed.
6 native larger-system purifications:rank2with2or4ancillary coordinates and full rank4 passed.
6 native executions:rectangular ancillary isometry via separately prepared larger vector and nonorthogonal ensemble labels passed.
12 malformed contracts rejected;dimension-one and tiny positive weights checked on host.
36 actual native circuits;factorization/completion/support maps are explicit host computations,not a native purification compiler.
```

**Problems and transfer.**

- **8.6-A — dimension and proof.** A four-dimensional density has eigenvalues (.6,.4,0,0). What is the smallest reference dimension? Prove that no one-dimensional reference can work without assuming a circuit implementation. If R has dimension four, how many dimensions of an ancillary unitary are fixed by a pair of its purifications?
- **8.6-B — fresh complex preparation.** Repeat the spectral/ancillary example with weights (.61,.39), system Q=`prepare(qubit(-.69,.77))` and reference W=`prepare(qubit(.83,-.48))`. Check every system/reference matrix entry and the joint target C Wᵀ. Explain why using W† can escape a system-only check.
- **8.6-C — enlargement and degeneracy.** Embed the same two-dimensional reference into four dimensions using J|0⟩=i|01⟩ and J|1⟩=|10⟩. Compare its native system reduction to the small-reference case. Then use weights (.5,.5) and a different complex common system eigenbasis in the support-frame proof. Which map is square, and which is rectangular?
- **8.6-D — ensemble boundary.** Use weights (.25,.75) with |v_0⟩=`qubit(.42,-.36)` and |v_1⟩=`qubit(1.27,.63)`. Compare the label purification with a spectral one and recover the ancillary relation. Replace the two orthonormal reference labels by the same ket. Determine both the unnormalized reduction and why any subsequent normalization is a different construction.

<details markdown="1">
<summary>Answers and verification guidance for 8.6-A–D</summary>

**A.** Rank is two, so two reference dimensions are necessary and sufficient by the column-rank bound and spectral construction. A one-dimensional reference gives a single column C and rank(CC†)≤1. For two purifications in a four-dimensional reference, their relation fixes the image of the occupied two-dimensional span. It leaves a unitary choice between the two unused two-dimensional complements; it need not be identity there.

**B.** With D=diag(√.61,√.39), the coefficient matrices and reductions are

$$
\begin{gathered}
C=QD,\quad C'=QD W^T,\\
\rho_S=QD^2Q^\dagger,\\
\rho_R'=WD^2W^\dagger.
\end{gathered}
$$

W† also supplies a unitary coordinate transformation and preserves CC†, but generally gives the wrong intended global vector and reference matrix. Compare the complete joint projector and the physical transformed coefficients rather than only the system density.

**C.** The rectangular J has J†J=I₂, while JJ† is a rank-two projector in four dimensions. The enlarged vector is flattened C Jᵀ and has the same system density; the reference is J diag(.61,.39) J†. A change of common system eigenbasis inside the degenerate eigenspace changes both contraction frames consistently, so GF† gives the same full two-dimensional unitary. The square ancillary U and rectangular embedding J have different domains.

**D.** The orthogonal-label coefficient columns are √.25 v_0 and √.75 v_1. Contracting against a common eigenbasis yields orthonormal frames and U=GF†, since this example has full reference support. If both labels become |f⟩, the unnormalized system vector is h=√.25 v_0+√.75 v_1, and its reduction is |h⟩⟨h|, including cross terms. Its trace is ⟨h|h⟩ rather than necessarily one; after division by that trace the density is a pure projector, generally unequal to the intended two-component mixture. Fresh transfer assertions check this distinction.

</details>

The frozen source target is [Watrous, *The Theory of Quantum Information*, §2.1.3, Theorems 2.10 and 2.12](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf#page=79), printed pages 71–72 in the author manuscript. The section's full constructive and common-frame proofs are supplied here in our coefficient convention; no external text is redistributed. This is an author-verified draft. Independent mathematical/implementation review, reader trial and formal acceptance remain pending.

<!-- end-section-8.6 -->

<span id="sec-density-matrices-reduced-states-and-purification-7"></span>
## 8.7 Proper and improper mixtures

**Question.** If a system density comes either from a randomized preparation or from discarding part of an entangled pure state, can a measurement on that system tell which happened?

We import the local expectation identity from [8.4](#sec-density-matrices-reduced-states-and-purification-4) and the purification construction from [8.6](#sec-density-matrices-reduced-states-and-purification-6). All spaces are finite. S is the accessible system and R a reference that is initially inaccessible. An effect E on S is a Hermitian operator with 0≤E≤I; its event probability is Tr(ρE). Amplitudes, probabilities and densities are dimensionless; circuit angles are radians. The conclusion below concerns access and predictions, not an interpretation of unobserved individual outcomes.

### 8.7.1 Specify the preparation and the accessible register

A **proper mixture**, in the preparation sense used here, describes an explicitly randomized preparation: choose j with probability p_j and prepare the normalized ket v_j. If the preparation record is unavailable, the density is ρ=Σ_j p_j|v_j⟩⟨v_j|. A **reduced or improper mixture** describes a density obtained by tracing out a reference from an entangled pure state. These terms label descriptions of a preparation or extension; they are not two mathematical species of density operator.

For an orthogonal pair u_0,u_1 and 0<p<1, compare the joint pure state and the recorded classical extension

$$
\begin{gathered}
|\Psi\rangle=\sqrt p\,|u_0,0\rangle
 +e^{i\phi}\sqrt{1-p}\,|u_1,1\rangle,\\
M=p|u_0,0\rangle\langle u_0,0|
 +(1-p)|u_1,1\rangle\langle u_1,1|.
\end{gathered}
$$

Tracing R in either expression leaves ρ=p|u_0⟩⟨u_0|+(1−p)|u_1⟩⟨u_1|. The cross terms of the pure projector vanish locally because ⟨0|1⟩=0. They are absent altogether in M. In the code, S=q0 and R=q1, and Q supplies the complex system basis. `m.case` uses actual FlagQuantum pure preparation and full/selected density requests through the 8.6 helper; M is an explicit classical weighted sum on the host.

```python
import math,torch,flagquantum as fq
from examples.foundations import mixture_access as m
from examples.foundations import purification as g,statistical_ensembles as e,partial_trace as t
p=.68;phi=.57;alpha=.81
result,rho,P,M,W=m.case(p,phi,alpha)
e.close(result.measurement('S').value[0],t.trace_ab(M,2,2))
# Explicit native route for the same known pure extension.
Q=e.prepare(e.qubit(alpha,.43));C,_=g.spectral((p,1-p),Q,2)
C[:,1]*=complex(math.cos(phi),math.sin(phi))
c=fq.Circuit(2,dtype=g.D).unitary(0,1,unitary=g.first_column(C.reshape(-1)))
native=fq.run(c,outputs=[fq.density_matrix(name='full'),
    fq.density_matrix(qubits=(0,),name='S')],options=e.OPTIONS)
e.close(native.measurement('S').value[0],rho)
e.close(native.measurement('full').value[0],P)
print('Native pure extension and host recorded mixture have identical system densities')
```

```text
Native pure extension and host recorded mixture have identical system densities
```

The implementation prepares the known pure vector with a checked square unitary. It does not initialize M through a mixed-input API. The two routes are compared as mathematical extensions with a declared local access contract.

### 8.7.2 Prove equality for every local measurement

Let P and M be any joint densities, pure or mixed, with the same reduction ρ on S. For every local effect E the defining identity of partial trace gives

$$
\begin{aligned}
\Pr_P(E)&=\operatorname{Tr}[P(E\otimes I_R)]\\
 &=\operatorname{Tr}(\rho E)\\
 &=\operatorname{Tr}[M(E\otimes I_R)]
 =\Pr_M(E).
\end{aligned}
$$

This proves equality of the entire outcome distribution of every local POVM, since each of its outcomes is an effect. It does not rely on choosing a particular basis or a finite test set. A local unitary V before measuring changes the effect to V†EV, still a local effect, so it cannot help. The ordinary quantum measurement model represents the event for any fixed local apparatus by an effect on its input; including a fixed independent local ancilla in that apparatus does not give access to R.

For a decision rule based on these identical distributions, the distribution of the decision is also identical: sum the same event probabilities over outcomes assigned to each decision. There is therefore no statistical test with a distinguishing advantage from S-only data under these assumptions. Tests of several explicit effects below validate the translation into code, not this universal quantifier.

```python
v=e.qubit(.93,-.74);E=torch.outer(v,v.conj())
local=torch.kron(E,e.I)
e.close(torch.trace(P@local),torch.trace(M@local))
print('Complex local effect agrees with both full-state contractions')
```

```text
Complex local effect agrees with both full-state contractions
```

**Converse check.** Equal probabilities for all effects imply equal local densities. Let Δ=ρ−σ be nonzero and Hermitian. Its spectral decomposition has a nonzero eigenvalue δ and a normalized eigenvector x. The rank-one effect |x⟩⟨x| has probability difference ⟨x|Δ|x⟩=δ≠0. Thus equality for all effects is exactly equality of densities; equality for one basis alone is weaker.

### 8.7.3 Avoid assigning a unique hidden ensemble

The density does not specify a unique preparation decomposition. For example, I/2 is both the equal mixture of |0⟩,|1⟩ and the equal mixture of |+⟩,|−⟩. Expanding the two plus/minus projectors cancels their off-diagonal entries and leaves I/2. Without a preparation record, neither decomposition can be selected by a local experiment.

```python
Q=e.prepare(e.qubit(alpha,.43));u0,u1=Q[:,0],Q[:,1]
ensemble=e.rho((p,1-p),(u0,u1));e.close(ensemble,rho)
plus=e.qubit(math.pi/2,0.);minus=e.qubit(-math.pi/2,0.)
e.close(e.rho((.5,.5),(plus,minus)),e.I/2)
print('Preparation weights need context;different ensemble decompositions need not be distinct densities')
```

```text
Preparation weights need context;different ensemble decompositions need not be distinct densities
```

Knowing that a source actually used a particular randomized procedure adds preparation information. It does not change the unread local density or allow its ensemble labels to be inferred perfectly from nonorthogonal states. Conversely, the existence of a purification does not show that the physical source used that purification. The operational theorem compares predictions under specified access, without deciding which extension physically exists.

### 8.7.4 Exhibit a joint measurement that changes the task

Write a=|u_0,0⟩ and b=|u_1,1⟩, which are orthonormal, and define

$$
W=e^{-i\phi}|a\rangle\langle b|
  +e^{i\phi}|b\rangle\langle a|.
$$

On span{a,b}, W exchanges the two basis vectors with conjugate phases and W²=I on that span; it is zero on the complement. Its eigenvalues are +1,−1 and zeros. Therefore J=(I+W)/2 is a valid joint effect. Direct expansion yields

$$
\begin{gathered}
\langle\Psi|W|\Psi\rangle=2\sqrt{p(1-p)},
\qquad \operatorname{Tr}(MW)=0,\\
\Pr_P(J)=\tfrac12+\sqrt{p(1-p)},
\qquad \Pr_M(J)=\tfrac12.
\end{gathered}
$$

This witness distinguishes extensions when joint access is permitted. It does not contradict the local theorem because J is not an effect acting on S alone. At p=.5 its probabilities are 1 and .5, so this example does not claim perfect single-shot discrimination of the two hypotheses.

```python
J=(torch.eye(4,dtype=g.D)+W)/2
pure_prob=torch.trace(P@J).real.item();mixed_prob=torch.trace(M@J).real.item()
assert pure_prob>.9;e.close(mixed_prob,.5)
print('Joint effect separates the pure and classical extensions;it is outside system-only access')
```

```text
Joint effect separates the pure and classical extensions;it is outside system-only access
```

At the endpoints p=0 or 1 the two displayed extensions coincide and the gap vanishes. The complete program includes p=1. For 0<p<1 the joint pure state is entangled, whereas M is an explicit mixture of product preparations. Their system spectra alone cannot certify which extension was used.

### 8.7.5 Distinguish an unread reference from a supplied outcome

For a reference effect F, the unnormalized system branch has coordinates

$$
(\tau_F)_{ij}=\sum_{\mu,\nu}
 P_{i\mu,j\nu} F_{\nu\mu},
\qquad p_F=\operatorname{Tr}\tau_F.
$$

For p_F>0 the normalized conditional state is τ_F/p_F. This expression gives the system's conditional state when the reference measurement has effect F and no further action touches S; it is computed by the joint Born rule. Summing a complete reference POVM replaces F by I and gives the same unread ρ. Zero-probability branches cannot be normalized.

For the plus Bell state and its classical Z-recorded mixture, a reference Z result selects the same corresponding Z system ket. A reference X-plus result instead selects |+⟩ for the Bell state and I/2 for the classical mixture, each with probability .5. The code evaluates these conditional matrices explicitly.

```python
bell,rb,PB,MB,WB=m.case(.5,0.,0.,mode='density_matrix')
z=torch.diag(torch.tensor([1,0],dtype=g.D));o=e.I-z
for full in (PB,MB):
 pa,A=m.conditional(full,z);pb,B=m.conditional(full,o)
 e.close(pa*A+pb*B,e.I/2)
pp,AP=m.conditional(PB,torch.outer(plus,plus.conj()))
pm,AM=m.conditional(MB,torch.outer(plus,plus.conj()))
e.close(pp,.5);e.close(pm,.5);e.close(AP,torch.outer(plus,plus.conj()));e.close(AM,e.I/2)
print('Unread local state agrees;reference-X-selected states differ once a record is supplied')
```

```text
Unread local state agrees;reference-X-selected states differ once a record is supplied
```

Selecting that subensemble requires knowing the reference result. With no record supplied, both local states remain I/2. Comparing selected events with an unread population would change the data-access assumptions. This example uses host conditional contractions, not a native sampled-collapse or remote feedback endpoint.

### 8.7.6 Do not infer an extension from its marginal

Even if global purity is promised, a local density can have several pure extensions. The plus and minus Bell states are orthogonal but both reduce to I/2. They differ in accessible joint phase correlations, not in local density.

```python
opposite,rr,Pminus,Mminus,_=m.case(.5,math.pi,0.)
e.close(rr,e.I/2);e.close(Mminus,MB)
assert torch.linalg.vector_norm(Pminus-PB).item()>1
print('Two pure extensions also share the same local density;global phase correlations differ')
```

```text
Two pure extensions also share the same local density;global phase correlations differ
```

The 8.6 ancillary-unitary theorem explains this freedom. Knowing the system density and knowing a complete joint preparation are different specifications. A local tomography experiment reconstructs the former. It cannot reconstruct inaccessible system-reference correlations.

### 8.7.7 State the repeated-copy assumption

If independent copies have density ρ under both hypotheses, their joint accessible density is ρ raised to a tensor power under both hypotheses. The same all-effect argument then applies to collective measurements on any finite number of those copies. This is an exact equality claim, not merely a limitation from a finite shot budget.

Equal one-copy marginals alone do not justify an independence assumption. The two accessible two-qubit densities I/4 and .5|00⟩⟨00|+.5|11⟩⟨11| each have I/2 marginals, but their ZZ means are 0 and 1. Correlated records can therefore reveal information that was not encoded in the one-copy density specification.

```python
iid=torch.kron(e.I/2,e.I/2)
correlated=torch.diag(torch.tensor([.5,0,0,.5],dtype=g.D))
e.close(t.trace_ab(iid,2,2),t.trace_ab(correlated,2,2))
e.close(torch.trace(iid@torch.kron(e.Z,e.Z)),0)
e.close(torch.trace(correlated@torch.kron(e.Z,e.Z)),1)
print('Equal one-copy marginals do not imply equal correlated multi-copy records')
```

```text
Equal one-copy marginals do not imply equal correlated multi-copy records
```

**Check.** Why does this example not distinguish two IID sources of I/2? One candidate is not the product of its one-copy marginals. A source with time correlations requires a joint model before the local-equality theorem can be applied to its full accessible record.

### 8.7.8 Validate the access contract and failures

```python
try:m.case(-.1,0.,0.)
except ValueError:print('Invalid probability rejected before native execution')
else:raise AssertionError('Bad probability accepted')
try:m.conditional(PB,torch.zeros((2,2),dtype=g.D))
except ValueError:print('Zero-probability conditioning rejected')
else:raise AssertionError('Impossible branch normalized')
assert g.RUNS==3
print('3 helper-native calls plus1explicit fq.run;mixture construction and conditional analysis run on host')
```

```text
Invalid probability rejected before native execution
Zero-probability conditioning rejected
3 helper-native calls plus1explicit fq.run;mixture construction and conditional analysis run on host
```

The companion [mixture_access.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/mixture_access.py) checks 25 actual CPU complex128 circuits in released FlagQuantum 0.3.1, using Python 3.12.14 and Torch 2.13.0. The body uses four native executions,including an explicit gate/run/request route. Actual square-unitary preparation, full/selected density outputs and probabilities are supplied by the checked 8.6 helper. Classical mixture matrices, dense joint effects and conditional contractions are host calculations. No native general joint-effect, mixed-input initializer, hardware readout, collapse, reset or interpretation-selection API is claimed.

Implementation equality uses absolute tolerance 1e-12 and relative tolerance zero. No input normalization repair, clipping or phase alignment is used. `m.case` rejects invalid probabilities; `conditional` validates a density and effect and refuses zero-probability branches. It is a two-qubit teaching helper, not an arbitrary-dimension measurement library. The all-effect proof is independent of numerical tolerances.

Expected output of the complete program:

```text
24 native pure extensions:equal full local densities/effect probabilities;host classical extensions and joint coherence witness passed.
25 actual native circuits;classical mixtures/conditional states are explicit host calculations,no sampled collapse.
```

**Problems and transfer.**

- **8.7-A.** Derive the local reduction and both witness probabilities for p=.37, φ=−.84 and Q=`prepare(qubit(-.62,.43))`. Which steps require access to R?
- **8.7-B.** Repeat the conditional reference-X example at p=.37. Find the plus-outcome probability and normalized system ket for the pure extension; compare its classical counterpart. Verify that plus and minus branches sum to the same unread density.
- **8.7-C.** Construct a pair of different densities with equal computational-basis probabilities but different Y means. Explain why this cannot refute the all-effect theorem.
- **8.7-D.** For the correlated-copy example, evaluate the effect (I+Z⊗Z)/2. Then explain which extra source assumption would be needed before using the tensor-power argument.

<details markdown="1">
<summary>Answers and verification guidance for 8.7-A–D</summary>

**A.** The unread state is Q diag(.37,.63) Q†. The joint witness gap in probabilities is √(.37·.63), while a local effect has exactly zero gap. Preparing the system basis does not require R, but the joint witness does.

**B.** In the declared u basis, the pure plus branch has probability .5 and ket √p u_0+e^{iφ}√(1−p)u_1. The minus branch changes the sign of the second term. Each is normalized by orthonormality. The classical plus and minus branches each have probability .5 and conditional density ρ; off-diagonal terms cancel in the weighted pure-branch sum. A basis rotation Q changes the coordinate matrices consistently.

**C.** The kets (|0⟩+i|1⟩)/√2 and (|0⟩−i|1⟩)/√2 have the same Z probabilities but Y means +1 and −1. Their complete densities differ, so the equal-density premise fails.

**D.** The effect probabilities are .5 for the independent I/4 state and 1 for the correlated state. Independent identical preparation across copies, or an explicit equality of the whole accessible joint densities, is needed. Equality of individual marginals is insufficient.

</details>

The frozen locator is NC §2.4.3 (contents locator printed105; no new full-text review claimed). The operational reduction convention was checked against [Watrous §2.1.3, printed68](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf#page=76); the all-effect proof and access-qualified counterexamples are supplied here. This author-verified draft still awaits independent mathematical/implementation review, reader trial and formal acceptance.

<!-- end-section-8.7 -->

<span id="sec-density-matrices-reduced-states-and-purification-8"></span>
## 8.8 Density-operator verification laboratory

**Laboratory question.** A simulator returns a full density and two reductions. Which independent checks justify accepting these as outputs for a *declared task*, and which incorrect candidates can pass a weaker check?

This V-depth laboratory reuses the density criteria of 8.2, the operational probabilities/updates of 8.3, the partial-trace convention of 8.4, the reduced spectra of 8.5 and the tolerance discipline of 2.8. It does not replace their proofs by tests. The system is S=q0, reference R=q1, with joint index 2i+μ. Angles are radians; densities, probabilities and amplitudes are dimensionless. CPU complex128 matrices and a fixed absolute tolerance ε=10⁻¹², relative tolerance zero, define the implementation comparison. These finite comparisons are not exact positivity or interval certificates.

### 8.8.1 Freeze the target before inspecting the candidate

Let p=.27, Q=`prepare(qubit(.83,.62))`, and let Q's orthonormal columns be u_0,u_1. The intended coefficient matrix and joint state are

$$
\begin{gathered}
C=Q\operatorname{diag}(\sqrt p,\sqrt{1-p}),\\
|\Psi\rangle=\sum_{i,\mu}C_{i\mu}|i,\mu\rangle,\qquad
P=|\Psi\rangle\langle\Psi|.
\end{gathered}
$$

Freeze the ordered supports, target parameters, execution mode, dtype, reference representation, tolerance and **acceptance scope** before running. Joint scope requires the full target and both reductions; local scope requires the specified system density, while still checking internal consistency of the supplied extension. A scope change is a new task. It is never a repair that makes an originally wrong joint candidate acceptable.

Here the explicit native route uses a host-completed square preparation unitary from 8.6, then requests all three matrices by name. The analytic C and its outer product are independent references to the returned matrices, rather than a second reading of the same density output.

```python
import math,torch,flagquantum as fq
from examples.foundations import density_lab as lab
from examples.foundations import purification as g,statistical_ensembles as e,partial_trace as t
C,rho=lab.reference(.27,.62)
c=fq.Circuit(2,dtype=g.D).unitary(0,1,unitary=g.first_column(C.reshape(-1)))
r=fq.run(c,outputs=[fq.density_matrix(name='full'),
 fq.density_matrix(qubits=(0,),name='S'),fq.density_matrix(qubits=(1,),name='R')],options=e.OPTIONS)
packet={name:r.measurement(name).value[0].clone()for name in ('full','S','R')}
accepted=lab.report(packet,C)
assert accepted['accepted']
print('Explicit native full/system/reference packet accepted against the declared joint target')
```

```text
Explicit native full/system/reference packet accepted against the declared joint target
```

**Predict.** The global state is pure, but the two reduced eigenvalues are .27 and .73. A test that insists that every returned density have purity one would reject a correct result.

### 8.8.2 Separate physical admissibility from target correctness

For each d×d candidate A, first require a finite dense square matrix of the declared dtype and shape. Compute

$$
\begin{gathered}
h=\max_{ij}|A_{ij}-A_{ji}^*|,\qquad
z=|\operatorname{Tr}A-1|,\\
\lambda_{\min}=\min\operatorname{eigvalsh}(A).
\end{gathered}
$$

Only evaluate the Hermitian eigenvalue routine after the Hermitian residual passes. Otherwise a routine that reads one triangle could conceal an invalid other triangle. Require h≤ε, z≤ε and λ_min≥−ε, reporting the actual residuals. The last allowance is a numerical feasibility guard, not permission to silently replace negative eigenvalues by zero. Nor does it prove the exact matrix positive: a tiny negative eigenvalue may be unresolved at the declared tolerance. Do not symmetrize, clip eigenvalues or renormalize the candidate during verification.

Trace one alone permits negative eigenvalues; positivity and trace one permit many *wrong* target states. Target comparison remains a separate obligation. For our pure preparation, 8.5 predicts

$$
\operatorname{Tr}P^2=1,\qquad
\operatorname{Tr}\rho_S^2=p^2+(1-p)^2=.6058.
$$

```python
e.close(packet['S'],rho)
e.close(torch.trace(packet['full']@packet['full']),1)
e.close(torch.trace(packet['S']@packet['S']),.27**2+.73**2)
e.close(torch.linalg.eigvalsh(packet['S']),torch.tensor([.27,.73],dtype=torch.float64))
print('Global purity1;local eigenvalues[0.27,0.73]and purity0.6058 match analytic weights')
```

```text
Global purity1;local eigenvalues[0.27,0.73]and purity0.6058 match analytic weights
```

Purity is a useful cross-check, not an informationally complete specification. Distinct states can share trace, spectrum and purity. In particular, complex conjugating a density in the computational basis preserves these quantities but can reverse its Y mean.

### 8.8.3 Check both coordinate contractions explicitly

The independent coefficient predictions are ρ_S=CC† and ρ_R=CᵀC*. The matrix-entry partial trace is

$$
(\rho_S)_{ij}=\sum_\mu P_{i\mu,j\mu},
\qquad
(\rho_R)_{\mu\nu}=\sum_i P_{i\mu,i\nu}.
$$

The companion uses scalar indexed sums for these contractions, and checks each returned reduction against the supplied full matrix. It also compares against the *intended* coefficient matrix: internal consistency alone would accept a self-consistent but stale preparation. A generic transpose or a reversal of the selected qubit tuple must not be inferred from the eigenvalues alone.

```python
e.close(packet['S'],t.trace_ab(packet['full'],2,2))
e.close(packet['R'],C.T@C.conj())
assert torch.linalg.vector_norm(packet['S'].conj()-packet['S']).item()>.1
print('Partial traces and complex conjugation checked as full matrices,not only spectra')
```

```text
Partial traces and complex conjugation checked as full matrices,not only spectra
```

The right expression is CᵀC*, not C†C in this ket-coordinate convention. In a diagonal example the wrong expression may accidentally agree; complex system rotations and independent effect checks prevent that special case from concealing an error.

### 8.8.4 Verify probabilities as well as matrices

For a normalized system vector v, the rank-one effect E=|v⟩⟨v| has probability Tr(ρ_SE)=v†ρ_Sv. Use both a matrix trace on the candidate and a scalar quadratic form on the reference. The qubit probes |0⟩, |1⟩, |+⟩ and |+i⟩ determine the diagonal and the real and imaginary parts of the off-diagonal entry. Indeed

$$
\begin{aligned}
p_+&=\tfrac12(\rho_{00}+\rho_{11})+\operatorname{Re}\rho_{01},\\
p_{+i}&=\tfrac12(\rho_{00}+\rho_{11})-\operatorname{Im}\rho_{01}.
\end{aligned}
$$

The sign in the second line follows by inserting v=(1,i)/√2 into v†ρv. This is an operational sign check in addition to the array comparison. A finite probe family is complete here because the displayed coordinate equations reconstruct every Hermitian qubit entry; an arbitrary finite selection of probes in larger dimensions would need its own completeness argument.

```python
for v in e.probes(2):
 E=torch.outer(v,v.conj())
 e.close(torch.trace(packet['S']@E),torch.vdot(v,rho@v))
print('Informationally complete local effects agree with independent quadratic forms')
```

```text
Informationally complete local effects agree with independent quadratic forms
```

**Check.** Why are computational-basis probabilities insufficient? They determine only the diagonal. Both a stale phase and an incorrect conjugation can survive that check.

### 8.8.5 Retain wrong candidates and diagnose the failed layer

The laboratory keeps original packets unchanged and constructs separate deliberately corrupted candidates. They include nonfinite data, an unequal pair of conjugate entries, a doubled trace, a trace-one matrix with eigenvalue −.1, the wrong complex conjugation of S, substituting S for R, and a real-valued full matrix that violates the declared representation. The reports include failed check names and residuals, not a normalized replacement result.

```python
bad=lab.errors(packet,C)
assert all(not x['accepted']for x in bad.values())
print('7 incorrect packets rejected;failure reports retain the original candidate residuals')
```

```text
7 incorrect packets rejected;failure reports retain the original candidate residuals
```

A representation failure stops downstream numerical checks that have no valid input. A Hermitian failure prevents an eigenvalue-based positivity claim for that candidate. Once the matrices pass numerical admissibility, failed contractions or reference comparisons explain a different class of error. A later successful rerun is a new packet; it does not retroactively accept the original one.

### 8.8.6 Test equivalence under the declared access scope

Apply Z to the reference of the intended purification. The system density remains CC†, while the full state and reference coherences must be judged according to their actual target. For this particular diagonal reference density, its matrix remains unchanged too; the full joint phase correlation changes. Thus the candidate passes a local-S task but fails the original joint task.

```python
phase_packet,_=lab.prepare(.27,.62,W=e.Z)
local=lab.report(phase_packet,C,'local');joint=lab.report(phase_packet,C,'joint')
assert local['accepted']and not joint['accepted']
print('Ancillary phase candidate:local accepted,joint rejected;scope is explicit')
```

```text
Ancillary phase candidate:local accepted,joint rejected;scope is explicit
```

The local report checks that the supplied full and reduced matrices form a consistent extension and that S matches the local target. It deliberately does not compare the extension to a specified global target. The joint report additionally compares the full projector and R against their declared reference matrices. The report's `scope` field is therefore part of its meaning, not decorative metadata.

### 8.8.7 Detect a stale reference and budget numerical error honestly

A new target with different p and system phase is a valid preparation in its own right, but it must fail comparison to the old reference. The test below executes it in density-matrix mode and compares both contracts.

```python
matched,_=lab.prepare(.81,-.47,mode='density_matrix')
otherC,_=lab.reference(.81,-.47)
assert lab.report(matched,otherC)['accepted']
assert not lab.report(matched,C)['accepted']
print('Fresh declared target accepted;stale reference rejected')
```

```text
Fresh declared target accepted;stale reference rejected
```

With an entrywise bound max|Δ_ij|≤ε on a d-dimensional matrix, its Frobenius norm is at most dε. Cauchy–Schwarz on matrix entries therefore gives |Tr(ΔE)|≤dε∥E∥_F. This explains why a chosen entrywise tolerance does not automatically equal the error bound for every possible observable; the dimension and the observable norm matter. Numerical residuals from several operations need their own error budget if combined in a later computation. This laboratory reports them separately and does not promote floating-point equality into a certified error interval.

The protocol refuses tolerance zero, nonfinite tolerances and tolerances larger than the frozen ceiling. A caller may request a stricter positive tolerance, accepting that correct floating-point results may then be unresolved. Increasing tolerance until a bad candidate passes would change the acceptance contract after observing the answer.

### 8.8.8 Run the complete protocol and preserve its limits

```python
for tol in (0.,1e-8,float('nan')):
 try:lab.report(packet,C,atol=tol)
 except ValueError:pass
 else:raise AssertionError('Invalid tolerance accepted')
assert g.RUNS==2
print('3invalid tolerances rejected;body executed2helper calls plus1explicit native run')
```

```text
3invalid tolerances rejected;body executed2helper calls plus1explicit native run
```

The executable [density_lab.py](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/foundations/density_lab.py) runs 10 actual FlagQuantum circuits: eight matched preparations and two deliberately changed reference-phase preparations, in statevector and density-matrix modes. The body runs three actual circuits, including the explicit native call in 8.8.1. Tested versions are Python 3.12.14, released FlagQuantum 0.3.1 and Torch 2.13.0. The prior 8.6 helper validates the square preparation matrices and actual native full/selected density outputs; the laboratory's acceptance logic, scalar partial traces, spectral checks and effect contractions are host computations.

This is not a claim of a native density-verification service, arbitrary mixed-input initialization, sampled measurement updates, reset or hardware validation. Shape, numerical admissibility, target agreement, operational agreement, execution provenance and independent scientific review are different questions. A packet's arrays alone do not authenticate its claimed source or runtime. The tests cover a small two-qubit protocol with a known pure joint target; applying it to arbitrary dimensions or other mixed global targets requires a new explicit reference and scope. Mathematical/implementation review, reader trial and scientific acceptance remain separate from author checks.

Expected output of the complete program:

```text
10 actual native circuits:8matched preparations and2ancillary-phase candidates passed scoped acceptance checks.
7 malformed/incorrect density packets rejected without clipping,symmetrization or normalization repair.
3 invalid tolerance contracts rejected;local acceptance never substitutes for joint acceptance.
```

**Chapter synthesis and transfer.**

- **8.8-A — derive.** Starting with C=Q diag(√p,√(1−p)), derive both reduced matrices and both purities. Explain why every pure global input does not produce a pure local density.
- **8.8-B — implement.** Repeat the laboratory for p=.39 and φ=−.73 in both execution modes. Preserve the original candidate and all residuals, and compare full matrices, scalar reductions and probe probabilities.
- **8.8-C — debug.** Apply a reference Z with this fresh target. Submit the packet to both scopes. Which full-state comparison fails? Does a local success authorize accepting the original joint candidate?
- **8.8-D — challenge a certificate.** A matrix has trace one and min eigenvalue −5×10⁻¹³, within the numerical threshold. Can the report certify mathematical positivity? What if its spectrum matches the target but its imaginary off-diagonal signs differ?

<details markdown="1">
<summary>Answers and verification guidance for 8.8-A–D</summary>

**A.** The system is Q diag(p,1−p) Q†, and the reference is diag(p,1−p). Their purities are p²+(1−p)², while the full outer-product purity is one by normalized-vector algebra. Except at p=0 or 1, a positive local rank-two spectrum is mixed despite global purity.

**B.** The native preparation, full/selected queries and candidate acceptance run unchanged with the fresh parameters. The complete system/reference matrices and every rank-one probe must be compared; copying only eigenvalues omits basis and phase information. Fresh transfer evidence records both modes and the changed-phase candidates.

**C.** The full projector comparison fails because its cross terms between the reference labels change sign. S remains unchanged. A local report answers a different task; retain the rejected joint report and do not silently lower its scope.

**D.** The result is only numerical feasibility at the stated tolerance, not exact positivity. No clipping is allowed in the original report. Matching a spectrum cannot fix the eigenvectors or imaginary signs; the full entrywise target and the |+i⟩ probability expose that error.

</details>

This editorial acceptance protocol (`ED:protocol`) reuses the preceding chapter's established results; it introduces no new external theorem. Chapter 8 now has eight working drafts, not formal chapter acceptance. Independent mathematical/implementation review and reader trials remain pending.

<!-- end-section-8.8 -->
