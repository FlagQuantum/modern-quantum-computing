# 8. Density Matrices, Reduced States, and Purification

**Working draft: section 8.1 · Writing Baseline 1.0 · October 23, 2026.** Author execution is separate from independent mathematical review, implementation review and reader trial; these remain pending. The examples use released FlagQuantum 0.3.1, PyTorch 2.13.0 and CPU complex128.

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

Summing j gives $\operatorname{Tr}(\rho E)$, while retaining j permits different conditional predictions. No partial-trace theorem is needed for this direct mixture calculation; the general reduced-state construction is developed in 8.3.

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

The public density request also accepts selected subsets according to its documented contract; this section exercises full and reversed full-register selections. The formal reduction operation and its independent validation belong to 8.3. The existence of density-matrix mode is not evidence that any guessed mixed-initializer signature, noisy instrument or hardware route works. This section neither passes ρ as a Circuit input nor invents an ensemble initializer.

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
