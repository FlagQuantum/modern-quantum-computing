"""8.1: native density outputs and explicit classical ensemble construction."""
import cmath
import itertools
import math
from dataclasses import replace
import torch
import flagquantum as fq
try:
    from examples.foundations.tensor_spaces import OPTIONS
except ModuleNotFoundError:
    from tensor_spaces import OPTIONS
D = torch.complex128
ATOL = 1e-12
RUNS = 0
I = torch.eye(2, dtype=D)
X = torch.tensor([[0,1],[1,0]], dtype=D)
Y = torch.tensor([[0,-1j],[1j,0]], dtype=D)
Z = torch.diag(torch.tensor([1,-1], dtype=D))


def close(a,b):
    a,b = torch.as_tensor(a,dtype=D),torch.as_tensor(b,dtype=D)
    assert a.shape == b.shape
    torch.testing.assert_close(a,b,atol=ATOL,rtol=0)


def state(v):
    if (not isinstance(v,torch.Tensor) or v.dtype!=D or v.device.type!='cpu'
            or v.layout!=torch.strided or v.ndim!=1 or len(v) not in (2,4)
            or not bool(torch.isfinite(v).all())
            or abs(torch.vdot(v,v).item()-1)>ATOL):
        raise ValueError('Finite normalized dense CPUcomplex128 vector of dimension2or4 required')
    return v


def ensemble(weights,vectors):
    if (type(weights) is not tuple or type(vectors) is not tuple or not weights
            or len(weights)!=len(vectors)
            or any(type(p) not in (int,float) or not math.isfinite(p) or p<0 for p in weights)
            or abs(sum(weights)-1)>ATOL):
        raise ValueError('Finite nonnegative normalized tuple of classical weights required;no repair')
    for v in vectors: state(v)
    if len({len(v) for v in vectors})!=1:
        raise ValueError('One common Hilbert-space dimension required')
    return weights,vectors


def outer(v):
    state(v)
    return torch.outer(v,v.conj())


def rho(weights,vectors):
    ensemble(weights,vectors)
    return sum((p*outer(v) for p,v in zip(weights,vectors)),
               torch.zeros((len(vectors[0]),)*2,dtype=D))


def scalar_rho(weights,vectors):
    ensemble(weights,vectors)
    n=len(vectors[0])
    return torch.tensor([[sum(p*v[a].item()*v[b].item().conjugate()
                              for p,v in zip(weights,vectors))
                          for b in range(n)] for a in range(n)],dtype=D)


def matrix(a):
    if (not isinstance(a,torch.Tensor) or a.dtype!=D or a.device.type!='cpu'
            or a.layout!=torch.strided or a.ndim!=2 or a.shape[0]!=a.shape[1]
            or a.shape[0] not in (2,4) or not bool(torch.isfinite(a).all())):
        raise ValueError('Finite square CPUcomplex128 matrix of dimension2or4 required')
    return a


def density(a):
    matrix(a)
    if (not torch.allclose(a,a.mH,atol=ATOL,rtol=0)
            or abs(torch.trace(a).item()-1)>ATOL
            or float(torch.linalg.eigvalsh(a).min()) < -ATOL):
        raise ValueError('Numerically Hermitian,unit-trace,positive density required;no clipping')
    return a


def hermitian(a):
    matrix(a)
    if not torch.allclose(a,a.mH,atol=ATOL,rtol=0):
        raise ValueError('Hermitian operator required')
    return a


def effect(e):
    hermitian(e)
    ev=torch.linalg.eigvalsh(e)
    if float(ev.min()) < -ATOL or float(ev.max()) > 1+ATOL:
        raise ValueError('Effect must lie numerically between0andI')
    return e


def born(weights,vectors,e):
    ensemble(weights,vectors);effect(e)
    if e.shape[0]!=len(vectors[0]):
        raise ValueError('Effect dimension must match ensemble')
    # Independent scalar quadratic forms,not trace(rho E).
    return sum(p*sum(v[a].item().conjugate()*e[a,b].item()*v[b].item()
                     for a in range(len(v)) for b in range(len(v))).real
               for p,v in zip(weights,vectors))


def qubit(theta,phi):
    if any(type(x) not in (int,float) or not math.isfinite(x) for x in (theta,phi)):
        raise ValueError('Finite real radian angles required')
    return torch.tensor([math.cos(theta/2),cmath.exp(1j*phi)*math.sin(theta/2)],dtype=D)


def prepare(v):
    state(v)
    if len(v)!=2: raise ValueError('This preparation matrix is one-qubit only')
    a,b=v.tolist()
    return torch.tensor([[a,-b.conjugate()],[b,a.conjugate()]],dtype=D)


def execute(c,outputs,mode='statevector'):
    global RUNS
    if mode not in ('statevector','density_matrix'):
        raise ValueError('Declared execution mode required')
    r=fq.run(c,outputs=outputs,options=replace(OPTIONS,mode=mode))
    RUNS+=1
    return r


def native(v,mode='statevector',U=None):
    c=fq.Circuit(1,dtype=D).unitary(0,unitary=prepare(v))
    if U is not None:
        matrix(U);close(U.mH@U,I)
        c.unitary(0,unitary=U.contiguous())
    r=execute(c,[fq.density_matrix(),fq.probabilities(),
        fq.expectation(fq.X(0),name='x'),fq.expectation(fq.Y(0),name='y'),
        fq.expectation(fq.Z(0),name='z')],mode)
    target=v if U is None else U@v
    close(r.density_matrix[0],outer(target))
    close(r.probabilities[0],target.abs().square())
    for name,A in (('x',X),('y',Y),('z',Z)):
        close(r.expectation(name)[0],torch.vdot(target,A@target))
    return r


def probes(n):
    if type(n) is not int or n not in (2,4):
        raise ValueError('Dimension2or4 teaching probe family required')
    basis=torch.eye(n,dtype=D)
    out=[v for v in basis]
    for a in range(n):
        for b in range(a+1,n):
            out += [(basis[a]+basis[b])/math.sqrt(2),(basis[a]+1j*basis[b])/math.sqrt(2)]
    return out


def cq(weights,vectors):
    ensemble(weights,vectors)
    if len(weights)!=2 or len(vectors[0])!=2:
        raise ValueError('Two labels and one system qubit in this teaching helper required')
    out=torch.zeros((4,4),dtype=D)
    for j,(p,v) in enumerate(zip(weights,vectors)):
        out[2*j:2*j+2,2*j:2*j+2]=p*outer(v)
    return out


def main():
    basis=tuple(torch.eye(2,dtype=D))
    for mode in ('statevector','density_matrix'):
        for theta,phi in ((0.,0.),(math.pi,0.),(math.pi/2,0.),(math.pi/2,math.pi/2),
                          (.73,-.41),(1.27,.59)):
            native(qubit(theta,phi),mode)
    print('12native pure preparations:both modes return correct density matrices,probabilities and X/Y/Z expectations.')
    cases=[
        ((.5,.5),basis),
        ((.5,.5),(qubit(math.pi/2,0.),qubit(math.pi/2,math.pi))),
        ((.5,.5),(qubit(math.pi/2,math.pi/2),qubit(math.pi/2,-math.pi/2))),
        ((.31,.69),(qubit(.87,-.52),qubit(1.61,.43))),
        ((1.,0.),(qubit(.69,-.8),basis[1])),
    ]
    classical=0
    for weights,vectors in cases:
        R=rho(weights,vectors);density(R);close(R,scalar_rho(weights,vectors))
        for v in probes(2):
            E=outer(v)
            close(torch.trace(R@E),born(weights,vectors,E));classical+=1
        for v in vectors:
            for theta,phi in ((.49,-.27),(1.14,.63)):
                w=qubit(theta,phi);U=prepare(w).mH.contiguous()
                r=native(v,U=U)
                close(r.probabilities[0,0],abs(torch.vdot(w,v))**2)
    print('20native complex analyzers and20classical effect checks match scalar Born sums and trace probabilities.')
    rpop,phi=.73,.41
    pm=tuple(torch.tensor([math.sqrt(rpop),s*cmath.exp(1j*phi)*math.sqrt(1-rpop)],dtype=D) for s in (1,-1))
    native_pm=tuple(native(v).density_matrix[0] for v in pm)
    R=(native_pm[0]+native_pm[1])/2
    close(R,torch.diag(torch.tensor([rpop,1-rpop],dtype=D)))
    close(R,rho((rpop,1-rpop),basis))
    print('2native nonorthogonal components reproduce the unequal-population spectral ensemble;offdiagonal phases cancel.')
    for a,b in itertools.product((0,1),repeat=2):
        for bell in (False,True):
            c=fq.Circuit(2,dtype=D)
            if a:c.x(0)
            if b:c.x(1)
            if bell:c.h(0).cx(0,1)
            r=execute(c,[fq.density_matrix(name='full'),fq.density_matrix(qubits=(1,0),name='reverse')])
            v=torch.zeros(4,dtype=D)
            if bell:
                v[b]=1/math.sqrt(2);v[2+(1^b)]=(-1)**a/math.sqrt(2)
            else:v[2*a+b]=1.
            close(r.measurement('full').value[0],outer(v))
            permutation=torch.tensor([0,2,1,3])
            close(r.measurement('reverse').value[0],outer(v[permutation]))
    for v in probes(4):
        close(torch.vdot(v,(torch.eye(4,dtype=D)/4)@v),.25);classical+=1
    assert classical==36
    print('8native two-qubit preparations:computational/Bell ensembles and reversed density-axis order verified;16classical separating probes passed.')
    for family in (basis,(qubit(math.pi/2,0.),qubit(math.pi/2,math.pi))):
        for j,v in enumerate(family):
            c=fq.Circuit(2,dtype=D)
            if j:c.x(0)
            c.unitary(1,unitary=prepare(v))
            r=execute(c,[fq.density_matrix(),fq.probabilities()])
            joint=torch.kron(torch.eye(2,dtype=D)[j],v)
            close(r.density_matrix[0],outer(joint))
    print('4native classical-label product preparations:equal unlabelled system states can have different labelled joint predictions.')
    a,phi=.83,-.57
    U=torch.diag(torch.tensor([1,cmath.exp(1j*phi)],dtype=D))@torch.tensor([[math.cos(a/2),-math.sin(a/2)],[math.sin(a/2),math.cos(a/2)]],dtype=D)
    for family in (basis,(qubit(math.pi/2,0.),qubit(math.pi/2,math.pi))):
        for j,v in enumerate(family):
            native(v,U=U)
            native(v,U=X if j else I)
    print('8native fixed/label-dependent operations:fixed U preserves equivalence;accessible labels change the operational input.')
    malformed=[
        lambda:rho((-.1,1.1),basis),lambda:rho((.4,.4),basis),
        lambda:rho((float('nan'),0.),basis),lambda:rho((),()),
        lambda:rho((1.,),(torch.ones(2,dtype=D),)),
        lambda:rho((1.,),(torch.tensor([1.,0.]),)),
        lambda:rho((.5,.5),(basis[0],torch.tensor([1.,0.,0.,0.],dtype=D))),
        lambda:density(torch.diag(torch.tensor([1.1,-.1],dtype=D))),
        lambda:density(torch.eye(2,dtype=D)),
        lambda:density(torch.tensor([[1.,1.],[0.,0.]],dtype=D)),
        lambda:effect(2*I),lambda:effect(-I),
        lambda:born((1.,),(basis[0],),torch.eye(4,dtype=D)),
        lambda:cq((1.,),(basis[0],)),
    ]
    before=RUNS
    for f in malformed:
        try:f()
        except ValueError:pass
        else:raise AssertionError('Malformed contract accepted')
    assert RUNS==before==54
    print('14malformed contracts rejected before execution;zero weight retained;54CPUcomplex128native circuits passed.')
    print('Classical ensemble sums are not an arbitrary mixed-state initializer or a finite-data certificate of exact equality.')

if __name__=='__main__':main()
