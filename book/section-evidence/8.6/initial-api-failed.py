"""8.6: explicit small pure-state preparation and ancillary equivalence."""
import math
from dataclasses import replace
import torch
import flagquantum as fq
try:
    from examples.foundations import statistical_ensembles as e,partial_trace as t
except ModuleNotFoundError:
    import statistical_ensembles as e,partial_trace as t
D=e.D;ATOL=1e-12;RUNS=0


def unitary(U,d):
    if (not isinstance(U,torch.Tensor)or U.dtype!=D or U.device.type!='cpu'
        or U.layout!=torch.strided or U.shape!=(d,d)or not bool(torch.isfinite(U).all())
        or not torch.allclose(U.mH@U,torch.eye(d,dtype=D),atol=ATOL,rtol=0)):
        raise ValueError('Finite square CPUcomplex128 unitary of declared dimension required')
    return U


def spectral(weights,Q,dR):
    if (type(weights)is not tuple or len(weights)not in (2,4)
        or any(type(x)not in (int,float)or not math.isfinite(x)or x<0 for x in weights)
        or abs(sum(weights)-1)>ATOL or type(dR)is not int or not 1<=dR<=4):
        raise ValueError('Nonnegative normalized weights and ancillary dimension1..4 required')
    d=len(weights);unitary(Q,d);active=[k for k,p in enumerate(weights)if p>0]
    if dR<len(active):raise ValueError('Ancillary dimension smaller than declared positive rank')
    C=torch.zeros((d,dR),dtype=D)
    for j,k in enumerate(active):C[:,j]=math.sqrt(weights[k])*Q[:,k]
    rho=(Q*torch.tensor(weights,dtype=torch.float64))@Q.mH
    e.close(C@C.mH,rho);e.close(C.abs().square().sum(),1)
    return C,rho


def first_column(v):
    if (not isinstance(v,torch.Tensor)or v.dtype!=D or v.device.type!='cpu'
        or v.ndim!=1 or len(v)not in (4,8,16)or not bool(torch.isfinite(v).all())
        or abs(torch.vdot(v,v).item()-1)>ATOL):
        raise ValueError('Normalized finite CPUcomplex128 vector of dimension4,8or16 required')
    cols=[v]
    for basis in torch.eye(len(v),dtype=D).T:
        w=basis.clone()
        for _ in range(2):
            for q in cols:w-=q*torch.vdot(q,w)
        norm=torch.linalg.vector_norm(w).item()
        if norm>1e-10:cols.append(w/norm)
        if len(cols)==len(v):break
    U=torch.stack(cols,dim=1);unitary(U,len(v));e.close(U[:,0],v)
    return U


def execute(C,W=None,mode='statevector'):
    global RUNS
    if (not isinstance(C,torch.Tensor)or C.dtype!=D or C.device.type!='cpu'
        or C.ndim!=2 or any(d not in (2,4)for d in C.shape)
        or not bool(torch.isfinite(C).all())or abs(C.abs().square().sum().item()-1)>ATOL):
        raise ValueError('Normalized CPUcomplex128 coefficient matrix with qubit factors2or4 required')
    if mode not in ('statevector','density_matrix'):raise ValueError('Tested execution mode required')
    dS,dR=C.shape;ns,nr=int(math.log2(dS)),int(math.log2(dR));n=ns+nr
    c=fq.Circuit(n,dtype=D).unitary(tuple(range(n)),unitary=first_column(C.reshape(-1)).contiguous())
    target=C
    if W is not None:
        unitary(W,dR);c.unitary(tuple(range(ns,n)),unitary=W.contiguous());target=C@W.T
    r=fq.run(c,outputs=[fq.density_matrix(name='full'),fq.density_matrix(qubits=tuple(range(ns)),name='S'),
        fq.density_matrix(qubits=tuple(range(ns,n)),name='R'),fq.probabilities(name='p'),
        fq.expectation(fq.Y(0),name='ys')],options=replace(e.OPTIONS,mode=mode));RUNS+=1
    full=r.measurement('full').value[0];S=r.measurement('S').value[0];R=r.measurement('R').value[0]
    v=target.reshape(-1);e.close(full,torch.outer(v,v.conj()));e.close(S,target@target.mH);e.close(R,target.T@target.conj())
    e.close(S,t.trace_ab(full,dS,dR));e.close(R,t.trace_ab(full.reshape(dS,dR,dS,dR).permute(1,0,3,2).reshape(dR*dS,dR*dS),dR,dS))
    e.close(r.measurement('p').value[0],v.abs().square());e.close(torch.trace(full@full),1)
    e.close(r.expectation('ys')[0],torch.trace(t.indexed(full,n,(0,))@e.Y))
    return r,target


def support_frames(C,Q,weights):
    if C.shape[0]!=len(weights):raise ValueError('System dimension mismatch')
    unitary(Q,len(weights));rho=(Q*torch.tensor(weights,dtype=torch.float64))@Q.mH
    e.close(C@C.mH,rho)
    active=[k for k,p in enumerate(weights)if p>0]
    # w_k=(<u_k| tensor I)|Psi>;columns contain physical ancillary ket coordinates.
    F=torch.stack([(Q[:,k].conj()@C)/math.sqrt(weights[k])for k in active],dim=1)
    e.close(F.mH@F,torch.eye(len(active),dtype=D))
    e.close((Q[:,active]*torch.tensor([math.sqrt(weights[k])for k in active]))@F.T,C)
    return F


def ensemble_coeff(weights,vectors):
    e.ensemble(weights,vectors)
    return torch.stack([math.sqrt(p)*v for p,v in zip(weights,vectors)],dim=1)


def invalid_checks():
    I=torch.eye(2,dtype=D);v=torch.tensor([1,0,0,0],dtype=D)
    calls=[lambda:spectral((.6,.5),I,2),lambda:spectral((1.1,-.1),I,2),
      lambda:spectral((float('nan'),0.),I,2),lambda:spectral((.5,.5),I,1),
      lambda:spectral((.5,.5),I.real,2),lambda:spectral((.5,.5),2*I,2),
      lambda:spectral((.5,.5),I,True),lambda:first_column(2*v),
      lambda:first_column(v.real),lambda:execute(torch.ones((2,2),dtype=D)),
      lambda:unitary(torch.ones((4,2),dtype=D),2),lambda:ensemble_coeff((.5,.5),(e.qubit(0.,0.),))]
    for call in calls:
        try:call()
        except ValueError:pass
        else:raise AssertionError('Malformed purification contract accepted')
    C,rho=spectral((1.,0.),I,1);e.close(C@C.mH,rho)
    C,rho=spectral((1.,1e-20),I,2);assert C[1,1].real.item()>0
    return len(calls)


def main():
    I=torch.eye(2,dtype=D)
    for mode in ('statevector','density_matrix'):
        for p in (.2,.5,1.):
            for angle in (0.,.81):
                Q=e.prepare(e.qubit(angle,.43));C,rho=spectral((p,1-p),Q,2)
                for beta in (0.,-.73):
                    W=e.prepare(e.qubit(beta,-.57));r,target=execute(C,W,mode)
                    e.close(r.measurement('S').value[0],rho)
                    F=support_frames(C,Q,(p,1-p));G=support_frames(target,Q,(p,1-p));T=G@F.mH
                    e.close(T@F,G);e.close(T.mH@T,F@F.mH)
    print('24 native qubit purifications:complex spectral construction,ancillary rotation and supported equivalence passed.')
    for mode in ('statevector','density_matrix'):
        Q=torch.kron(e.prepare(e.qubit(.61,-.39)),e.prepare(e.qubit(-.47,.52)))
        for weights,dR in (((.6,.4,0.,0.),2),((.1,.2,.3,.4),4),((.5,.5,0.,0.),4)):
            C,rho=spectral(weights,Q,dR);W=first_column(torch.ones(4,dtype=D)/2)if dR==4 else e.prepare(e.qubit(.49,.36))
            r,target=execute(C,W,mode);e.close(r.measurement('S').value[0],rho);support_frames(target,Q,weights)
    print('6 native larger-system purifications:rank2with2or4ancillary coordinates and full rank4 passed.')
    for mode in ('statevector','density_matrix'):
        C,rho=spectral((.67,.33),e.prepare(e.qubit(.91,.46)),2)
        J=torch.zeros((4,2),dtype=D);J[0,0]=1;J[3,1]=1j
        small,_=execute(C,mode=mode);large,_=execute(C@J.T,mode=mode)
        e.close(J.mH@J,I);e.close(small.measurement('S').value,large.measurement('S').value)
        a,b=e.qubit(0.,0.),e.qubit(math.pi/2,.32)
        E=ensemble_coeff((.3,.7),(a,b));rr,_=execute(E,mode=mode);e.close(rr.measurement('S').value[0],e.rho((.3,.7),(a,b)))
    print('6 native executions:rectangular ancillary isometry via separately prepared larger vector and nonorthogonal ensemble labels passed.')
    print(f'{invalid_checks()} malformed contracts rejected;dimension-one and tiny positive weights checked on host.')
    assert RUNS==36
    print('36 actual native circuits;factorization/completion/support maps are explicit host computations,not a native purification compiler.')


if __name__=='__main__':main()
