"""7.2 Schmidt decomposition: native circuits plus explicit classical thin SVD.

All computed singular values are retained. A threshold is a resolution diagnostic,
never an exact entanglement certificate for a physical state.
"""
import math
import cmath
from importlib.metadata import version
import torch
import flagquantum as fq
try:
    from examples.foundations import product_entanglement as e
except ModuleNotFoundError:
    import product_entanglement as e
D=e.D
ATOL=e.ATOL
OPTIONS=e.OPTIONS
RUNS=0


def decompose(C):
    e.validate_matrix(C)
    U,s,Vh=torch.linalg.svd(C,full_matrices=False)
    B=Vh.T  # columns are conjugates of V columns, not V itself
    k=s.numel(); I=torch.eye(k,dtype=D)
    assert bool(torch.isfinite(s).all()) and bool((s>=0).all())
    assert torch.allclose(U.mH@U,I,atol=ATOL,rtol=0)
    assert torch.allclose(B.mH@B,I,atol=ATOL,rtol=0)
    assert torch.allclose((U*s)@B.T,C,atol=ATOL,rtol=0)
    assert abs(s.square().sum().item()-1)<ATOL
    return U,s,B


def resolved_rank(s,tau):
    if not isinstance(s,torch.Tensor) or s.ndim!=1 or not s.numel() or s.dtype!=torch.float64 or s.device.type!='cpu' or not bool(torch.isfinite(s).all()) or not bool((s>=0).all()):
        raise ValueError('Finite nonnegative float64 singular-value vector required')
    if type(tau) not in (int,float) or not math.isfinite(tau) or tau<=0:
        raise ValueError('Declare a finite positive diagnostic threshold')
    return int((s>tau).sum().item())


def query(circuit):
    global RUNS
    state,p=e.query(circuit); RUNS+=1
    return state,p


def ry(theta):
    return torch.tensor([[math.cos(theta/2),-math.sin(theta/2)],
                         [math.sin(theta/2),math.cos(theta/2)]],dtype=D)


def phase(phi):
    return torch.diag(torch.tensor([1,cmath.exp(1j*phi)],dtype=D))


def pair(theta,phi,alpha=.4,beta=-.8):
    if any(type(t) not in (float,int) or not math.isfinite(t) for t in (theta,phi,alpha,beta)):
        raise ValueError('Finite literal radian angles required')
    return fq.Circuit(2,dtype=D).ry(0,theta).cx(0,1).p(0,phi).ry(0,alpha).p(1,beta)


def pair_reference(theta,phi,alpha=.4,beta=-.8):
    diagonal=torch.diag(torch.tensor([math.cos(theta/2),cmath.exp(1j*phi)*math.sin(theta/2)],dtype=D))
    return ry(alpha)@diagonal@phase(beta).T


def scalar_rebuild(U,s,B):
    return torch.tensor([[sum(s[k].item()*U[i,k].item()*B[j,k].item() for k in range(s.numel()))
                          for j in range(B.shape[0])] for i in range(U.shape[0])],dtype=D)


def overlap(C,a,b):
    return sum(a[i].conj().item()*b[j].conj().item()*C[i,j].item()
               for i in range(C.shape[0]) for j in range(C.shape[1]))


def main():
    assert version('flagquantum')=='0.3.1' and version('torch').split('+')[0]=='2.13.0'
    for n in (2,3):
        for t in range(6):
            circuit=fq.Circuit(n,dtype=D);factors=[]
            for q in range(n):
                theta=.19+.21*t+.13*q;phi=-.73+.17*t-.31*q
                circuit.ry(q,theta).p(q,phi)
                factors.append((math.cos(theta/2),cmath.exp(1j*phi)*math.sin(theta/2)))
            state,_=query(circuit)
            assert torch.allclose(state,e.scalar_product(factors),atol=ATOL,rtol=0)
            for A,Bcut in e.cuts(n):
                C=e.coefficients(state,A,Bcut);U,s,B=decompose(C)
                assert abs(s[0].item()-1)<ATOL and bool((s[1:]<ATOL).all())
                assert torch.allclose(C,scalar_rebuild(U,s,B),atol=ATOL,rtol=0)
    print('12 native complex products: all ordered cuts reconstruct with one resolved coefficient.')
    for theta in (.31,math.pi/2,2.2):
        for phi in (0.,.71,-1.2):
            for alpha,beta in ((.4,-.8),(-.37,.63)):
                state,_=query(pair(theta,phi,alpha,beta));C=e.coefficients(state,(0,),(1,))
                reference=pair_reference(theta,phi,alpha,beta)
                assert torch.allclose(C,reference,atol=ATOL,rtol=0)
                U,s,B=decompose(C)
                target=torch.tensor(sorted([abs(math.cos(theta/2)),abs(math.sin(theta/2))],reverse=True),dtype=torch.float64)
                assert torch.allclose(s,target,atol=ATOL,rtol=0)
                assert torch.allclose(C,scalar_rebuild(U,s,B),atol=ATOL,rtol=0)
                assert abs(abs(overlap(C,U[:,0],B[:,0]))-s[0].item())<ATOL
                for angle in (.2,.91,1.4):
                    a=torch.tensor([math.cos(angle),1j*math.sin(angle)],dtype=D)
                    b=torch.tensor([math.sin(angle),cmath.exp(.7j)*math.cos(angle)],dtype=D)
                    assert abs(overlap(C,a,b))<=s[0].item()+ATOL
    print('18 complex entangled pairs: closed coefficients, scalar reconstruction and product-overlap checks passed.')
    for phi in (0.,.43,-.91):
        state,_=query(pair(math.pi/2,phi,0.,0.));C=e.coefficients(state,(0,),(1,))
        U,s,B=decompose(C);W=phase(.67)@ry(.83)
        assert abs(s[0].item()-s[1].item())<ATOL
        assert torch.allclose((U@W*s)@(B@W.conj()).T,C,atol=ATOL,rtol=0)
        assert torch.linalg.vector_norm(U@W-U).item()>.1
    print('3 degenerate Bell spectra: conjugate paired basis rotations reconstruct unchanged states.')
    for phi in (0.,.43,-.91):
        state,_=query(fq.Circuit(3,dtype=D).h(0).cx(0,2).p(0,phi).ry(1,.82))
        for A,Bcut,target in (((2,0),(1,),[1,0]),((0,),(1,2),[1/math.sqrt(2)]*2)):
            U,s,B=decompose(e.coefficients(state,A,Bcut))
            assert torch.allclose(s,torch.tensor(target,dtype=torch.float64),atol=ATOL,rtol=0)
    print('3 nonadjacent-register states: spectra depend on the bipartition, not its internal ordering.')
    for epsilon in (0.,1e-10):
        state,_=query(fq.Circuit(2,dtype=D).ry(0,2*math.asin(epsilon)).cx(0,1))
        U,s,B=decompose(e.coefficients(state,(0,),(1,)))
        assert abs(s[1].item()-epsilon)<1e-20
        assert resolved_rank(s,1e-9)==1
        if epsilon: assert resolved_rank(s,1e-12)==2
    print('2 near-product spectra: all singular values retained; threshold-dependent diagnostics declared.')
    for theta,phi in ((.31,.71),(.9,-1.2),(1.7,.43),(2.2,-.83),(.67,1.1),(1.3,-.41)):
        C=pair_reference(theta,phi);U,s,B=decompose(C)
        circuit=pair(theta,phi).unitary(0,unitary=U.mH.contiguous()).unitary(1,unitary=B.mH.contiguous())
        state,p=query(circuit);expected=torch.diag(s.to(D)).reshape(-1)
        assert torch.allclose(state,expected,atol=ATOL,rtol=0)
        assert torch.allclose(p,torch.tensor([s[0].item()**2,0,0,s[1].item()**2],dtype=torch.float64),atol=ATOL,rtol=0)
    print('6 native inverse-basis analyzers: complete amplitudes and matched-label probabilities passed.')
    for circuit,target in ((fq.Circuit(2,dtype=D).h(0).h(1),[1,0]),(fq.Circuit(2,dtype=D).h(0).h(1).cz(0,1),[1/math.sqrt(2)]*2)):
        state,p=query(circuit);U,s,B=decompose(e.coefficients(state,(0,),(1,)))
        assert torch.allclose(p,torch.full((4,),.25,dtype=torch.float64),atol=ATOL,rtol=0)
        assert torch.allclose(s,torch.tensor(target,dtype=torch.float64),atol=ATOL,rtol=0)
    print('2 identical computational distributions: different Schmidt spectra verified.')
    C=pair_reference(.9,.71)
    bad=[lambda:decompose(C*2),lambda:decompose(C.real),lambda:decompose(C.reshape(-1)),
         lambda:decompose(torch.zeros((2,2),dtype=D)),lambda:decompose(torch.tensor([[float('nan')]],dtype=D)),
         lambda:resolved_rank(torch.tensor([1.,0.],dtype=torch.float64),0),
         lambda:resolved_rank(torch.tensor([1.,0.],dtype=torch.float64),True),
         lambda:resolved_rank(torch.tensor([1.,0.],dtype=torch.float32),1e-12),
         lambda:resolved_rank(torch.tensor([1.,-1.],dtype=torch.float64),1e-12),
         lambda:pair(.9,float('inf'))]
    for f in bad:
        try:f()
        except ValueError:pass
        else:raise AssertionError('Invalid input admitted')
    print('10 malformed contracts rejected before simulation.')
    assert RUNS==46,RUNS
    print('46 CPU complex128 circuits passed; no exact numerical-rank or hardware certificate claimed.')


if __name__=='__main__':main()
