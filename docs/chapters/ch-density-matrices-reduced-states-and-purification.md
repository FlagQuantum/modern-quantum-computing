# 8. Density Matrices, Reduced States, and Purification

**Working drafts: sections 8.1–8.3 · Writing Baseline 1.0 · October 23, 2026.** Author execution is separate from independent mathematical review, implementation review and reader trial; these remain pending. The examples use released FlagQuantum 0.3.1, PyTorch 2.13.0 and CPU complex128.

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
