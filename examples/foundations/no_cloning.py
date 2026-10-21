"""Section4.7: one fixed copying attempt versus state-specific reference preparation."""
from importlib.metadata import version
from math import sqrt,cos,sin,pi
import cmath
import torch
import flagquantum as fq
try:
    from examples.foundations.tensor_spaces import prepare_matrix, OPTIONS
except ModuleNotFoundError:
    from tensor_spaces import prepare_matrix, OPTIONS
DTYPE=torch.complex128
ATOL=1e-12
COPY=torch.tensor([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=DTYPE)


def ket(values):
    if not isinstance(values,torch.Tensor) or values.shape!=(2,) or values.dtype!=DTYPE or values.device.type!='cpu' or not torch.isfinite(values).all():
        raise ValueError('Declare a finite CPU complex128 two-coordinate state')
    if abs(torch.vdot(values,values).real.item()-1)>ATOL:raise ValueError('State must be normalized; no automatic repair')
    return values


def desired(v):
    v=ket(v)
    return torch.tensor([a*b for a in v.tolist() for b in v.tolist()],dtype=DTYPE)


def candidate(v):
    v=ket(v)
    return torch.tensor([v[0].item(),0,0,v[1].item()],dtype=DTYPE)


def fidelity(actual,target):
    return float(abs(torch.vdot(target,actual).item())**2)


def execute(v,mode='fixed-copy',analyze=False):
    v=ket(v)
    if mode not in ('fixed-copy','known-reference'):raise ValueError('Declare fixed-copy or known-reference; no automatic repair')
    if type(analyze) is not bool:raise ValueError('Declare literal boolean analyzer flag')
    c=fq.Circuit(2,dtype=DTYPE)
    c.unitary(0,unitary=prepare_matrix(v))
    if mode=='fixed-copy':c.unitary(0,1,unitary=COPY)
    else:c.unitary(1,unitary=prepare_matrix(v))
    if analyze:
        # Chosen known analysis basis; identical on the two paths, not part of COPY.
        for q in (0,1):c.unitary(q,unitary=prepare_matrix(v).mH.contiguous())
    r=fq.run(c,outputs=[fq.probabilities()],options=OPTIONS)
    state,p=r.statevector(),r.probabilities
    assert state.shape==p.shape==(1,4) and state.dtype==DTYPE and p.dtype==torch.float64
    assert state.device.type==p.device.type=='cpu' and torch.isfinite(state).all() and torch.isfinite(p).all()
    torch.testing.assert_close(p[0],state[0].abs().square(),rtol=0,atol=ATOL)
    return state[0],p[0]


def main():
    assert version('flagquantum')=='0.3.1' and version('torch').split('+')[0]=='2.13.0'
    I=torch.eye(4,dtype=DTYPE)
    torch.testing.assert_close(COPY.mH@COPY,I,rtol=0,atol=0)
    states=[('zero',[1,0]),('one',[0,1]),('plus',[1/sqrt(2),1/sqrt(2)]),('minus',[1/sqrt(2),-1/sqrt(2)]),('plus-i',[1/sqrt(2),1j/sqrt(2)]),('complex',[.6,.8j])]
    print('One fixed unitary, blank|0>; known-reference preparation is state-specific, not a cloner.')
    for name,values in states:
        v=torch.tensor(values,dtype=DTYPE);target=desired(v)
        actual,_=execute(v);reference,_=execute(v,'known-reference')
        torch.testing.assert_close(actual,candidate(v),rtol=0,atol=ATOL)
        torch.testing.assert_close(reference,target,rtol=0,atol=ATOL)
        analyzed,p=execute(v,analyze=True);ideal,ideal_p=execute(v,'known-reference',True)
        B=prepare_matrix(v).mH.contiguous()
        # Independent scalar analyzer contraction, no kron or gate execution helper.
        scalar=torch.tensor([sum(B[i,a]*B[j,b]*actual[2*a+b] for a in (0,1) for b in (0,1)) for i in (0,1) for j in (0,1)],dtype=DTYPE)
        torch.testing.assert_close(analyzed,scalar,rtol=0,atol=ATOL)
        torch.testing.assert_close(ideal,torch.tensor([1,0,0,0],dtype=DTYPE),rtol=0,atol=ATOL)
        F=fidelity(actual,target)
        assert abs(p[0].item()-F)<ATOL and abs(ideal_p[0].item()-1)<ATOL
        print(f'{name}: fixed-copy fidelity={F:.6f}; analyzer P00={p[0].item():.6f}; known-reference P00={ideal_p[0].item():.6f}.')
    zero=torch.tensor([1,0],dtype=DTYPE);plus=torch.tensor([1,1],dtype=DTYPE)/sqrt(2)
    s=abs(torch.vdot(zero,plus).item());assert abs(s-s*s)>.2
    # Classical normalized fixtures, including zero/one boundaries and relative phases.
    count=0
    for theta in (0,pi/12,pi/6,pi/4,pi/3,5*pi/12,pi/2):
        for phi in (0,pi/5,pi/2,pi,7*pi/5):
            v=torch.tensor([cos(theta),cmath.exp(1j*phi)*sin(theta)],dtype=DTYPE)
            out=COPY@torch.tensor([v[0],0,v[1],0],dtype=DTYPE)
            torch.testing.assert_close(out,candidate(v),rtol=0,atol=ATOL)
            torch.testing.assert_close(desired(v),torch.kron(v,v),rtol=0,atol=ATOL)
            assert abs(torch.vdot(desired(v),desired(v)).real.item()-1)<ATOL;count+=1
    assert count==35
    print(f'Nonorthogonal pair: input overlap={s:.9f}; perfect-copy overlap={s*s:.9f}; incompatible.')
    bad=[lambda:ket(torch.ones(2,dtype=DTYPE)),lambda:ket(zero[None,:]),lambda:ket(zero.to(torch.complex64)),lambda:ket(torch.tensor([float('nan'),0],dtype=DTYPE)),lambda:execute(zero,'repair'),lambda:execute(zero,analyze=1)]
    for action in bad:
        try:action()
        except ValueError:pass
        else:raise AssertionError('Invalid contract admitted')
    print('35 classical amplitude fixtures and6invalid contracts checked; identical rays allowed, universal cloning excluded.')
    print('24 actual CPU complex128 circuits; atol=1e-12,rtol=0; no phase alignment, shots or hardware.')


if __name__=='__main__':main()
