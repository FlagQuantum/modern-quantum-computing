"""Section5.2: coherent controls, explicit ancilla contracts and uncomputation."""
from itertools import product
from importlib.metadata import version
from math import sqrt
import cmath
import torch
import flagquantum as fq
from flagquantum.errors import CapabilityError,ValidationError
try:
    from examples.foundations.circuit_composition import execute,product_input,H,rx,rz
    from examples.foundations.ordered_supports import complex_gate,scalar_scatter
except ModuleNotFoundError:
    from circuit_composition import execute,product_input,H,rx,rz
    from ordered_supports import complex_gate,scalar_scatter
DTYPE=torch.complex128
ATOL=1e-12
X=torch.tensor([[0,1],[1,0]],dtype=DTYPE)
RUNS=0


def controlled_matrix(U):
    if not isinstance(U,torch.Tensor) or U.ndim!=2 or U.shape[0]!=U.shape[1] or U.shape[0]<2 or U.shape[0]&(U.shape[0]-1) or U.dtype!=DTYPE or U.device.type!='cpu' or U.layout!=torch.strided or not torch.isfinite(U).all():
        raise ValueError('Book guard: finite CPU complex128 qubit-target square matrix required')
    d=U.shape[0]
    if not torch.allclose(U.mH@U,torch.eye(d,dtype=DTYPE),rtol=0,atol=ATOL):raise ValueError('Book guard: target must be unitary')
    C=torch.zeros((2*d,2*d),dtype=DTYPE);C[:d,:d]=torch.eye(d,dtype=DTYPE);C[d:,d:]=U
    return C


def run(block,factors):
    global RUNS
    state,p=execute(block,factors);RUNS+=1
    return state,p


def basis_factors(bits):return [(1,0) if b==0 else (0,1) for b in bits]


def verify_generic(U,n,support,factors):
    C=controlled_matrix(U);initial=product_input(factors)
    c=fq.Circuit(n,dtype=DTYPE).unitary(*support,unitary=C)
    state,p=run(c,factors)
    expected=torch.tensor(scalar_scatter(C,initial.tolist(),n,support),dtype=DTYPE)
    torch.testing.assert_close(state,expected,rtol=0,atol=ATOL)
    if n==2 and support==(0,1):
        v=initial.tolist();d=U.shape[0]
        branch=torch.tensor(v[:d]+[sum(U[i,j].item()*v[d+j] for j in range(d)) for i in range(d)],dtype=DTYPE)
        torch.testing.assert_close(state,branch,rtol=0,atol=ATOL)
    return state,p


def prob_one(p,q):
    n=p.numel().bit_length()-1
    return sum(p[j].item() for j in range(len(p)) if (j>>(n-1-q))&1)


def workspace(stage):
    if stage not in ('compute','use','clean','bad-data'):raise ValueError('Declare a supported coherent workspace stage')
    compute=fq.Circuit(4,dtype=DTYPE).cx(0,2).cx(1,2)
    block=fq.Circuit(4,dtype=DTYPE).compose(compute)
    if stage!='compute':block.cx(2,3)
    if stage=='bad-data':block.x(0)
    if stage in ('clean','bad-data'):block.compose(compute.adjoint())
    return block


def workspace_reference(data,stage,blank=0,target=0):
    if stage not in ('compute','use','clean','bad-data') or type(blank) is not int or blank not in (0,1) or type(target) is not int or target not in (0,1):raise ValueError('Declare stage and literal initial blank/target bits')
    out=torch.zeros(16,dtype=DTYPE)
    for j,(x,y) in enumerate(product((0,1),repeat=2)):
        a=blank^x^y;t=target
        if stage!='compute':t^=a
        if stage=='bad-data':x^=1
        if stage in ('clean','bad-data'):a^=y;a^=x
        out[8*x+4*y+2*a+t]+=data[j]
    return out


def data_factors():return [(.6,.8j),(sqrt(.7),cmath.exp(.2j)*sqrt(.3))]


def coherence(clean):
    c=fq.Circuit(2,dtype=DTYPE).h(0).cx(0,1)
    if clean:c.cx(0,1)
    return c.h(0)


def main():
    assert version('flagquantum')=='0.3.1' and version('torch').split('+')[0]=='2.13.0'
    print('Controlled matrix uses ordered support(control,target...); no measurement of the control.')
    gates=[X,rz(-.4)@rx(.7),cmath.exp(.37j)*(rz(-.4)@rx(.7))]
    for U in gates:
        for bits in product((0,1),repeat=2):verify_generic(U,2,(0,1),basis_factors(bits))
        for bits in product((0,1),repeat=3):verify_generic(U,3,(2,0),basis_factors(bits))
        verify_generic(U,2,(0,1),[(.6,.8j),(sqrt(.7),cmath.exp(.2j)*sqrt(.3))])
    for bits in product((0,1),repeat=3):verify_generic(complex_gate(),3,(0,1,2),basis_factors(bits))
    assert RUNS==47
    print('47generic controlled circuits: basis,complex,nonadjacent and two-target cases; scalar/branch references agree.')
    for n,pairs in ((2,[(0,1),(1,0)]),(3,[(2,0)])):
        for c,t in pairs:
            for bits in product((0,1),repeat=n):
                expected=list(bits);expected[t]^=bits[c]
                state,_=run(fq.Circuit(n,dtype=DTYPE).cx(c,t),basis_factors(bits))
                v=torch.zeros(2**n,dtype=DTYPE);v[int(''.join(map(str,expected)),2)]=1
                torch.testing.assert_close(state,v,rtol=0,atol=ATOL)
    for bits in product((0,1),repeat=3):
        expected=list(bits);expected[2]^=bits[0]&bits[1]
        state,_=run(fq.Circuit(3,dtype=DTYPE).ccx(0,1,2),basis_factors(bits))
        v=torch.zeros(8,dtype=DTYPE);v[int(''.join(map(str,expected)),2)]=1
        torch.testing.assert_close(state,v,rtol=0,atol=ATOL)
    factors=[(1/sqrt(2),1/sqrt(2)),(.6,.8j),(1,0)];state,_=run(fq.Circuit(3,dtype=DTYPE).ccx(0,1,2),factors)
    expected=torch.zeros(8,dtype=DTYPE)
    for j,(a,b) in enumerate(product((0,1),repeat=2)):expected[4*a+2*b+(a&b)]=product_input(factors[:2])[j]
    torch.testing.assert_close(state,expected,rtol=0,atol=ATOL)
    print('16named CX basis circuits and9CCX basis/superposition circuits checked.')
    source=fq.Circuit(1,dtype=DTYPE).rx(0,.7).rz(0,-.4)
    native=source.control(1,ctrl_qubits=(1,));assert native is not source and native.n_qubits==2 and len(source.to_ir().instructions)==2
    U=rz(-.4)@rx(.7);C=controlled_matrix(U)
    inputs=[basis_factors(bits) for bits in product((0,1),repeat=2)]+[[ (.6,.8j),(sqrt(.7),cmath.exp(.2j)*sqrt(.3)) ]]
    for factors in inputs:
        state,_=run(native,factors)
        expected=torch.tensor(scalar_scatter(C,product_input(factors).tolist(),2,(1,0)),dtype=DTYPE)
        torch.testing.assert_close(state,expected,rtol=0,atol=ATOL)
    factors=[(.6,.8j),(1,0)];mapped=fq.Circuit(2,dtype=DTYPE).compose(native,qubits=(1,0))
    state,_=run(mapped,factors)
    expected=torch.tensor(scalar_scatter(C,product_input(factors).tolist(),2,(0,1)),dtype=DTYPE)
    torch.testing.assert_close(state,expected,rtol=0,atol=ATOL)
    print('6native block-control circuits: added controlq1,targetq0,then explicit placement map; source retained.')
    for sign,index in ((1,0),(-1,2)):
        c=fq.Circuit(2,dtype=DTYPE).unitary(0,1,unitary=controlled_matrix(sign*torch.eye(2,dtype=DTYPE))).h(0)
        state,p=run(c,[(1/sqrt(2),1/sqrt(2)),(1,0)])
        v=torch.zeros(4,dtype=DTYPE);v[index]=1
        torch.testing.assert_close(state,v,rtol=0,atol=ATOL)
    print('2controlled-phase analyzer circuits: C(I) ->00; C(-I) ->10; target global phase is observable on control.')
    for factors in [basis_factors(bits) for bits in product((0,1),repeat=2)]+[data_factors()]:
        data=product_input(factors)
        for stage in ('compute','use','clean'):
            state,p=run(workspace(stage),factors+[(1,0),(1,0)])
            torch.testing.assert_close(state,workspace_reference(data,stage),rtol=0,atol=ATOL)
            if stage=='clean':assert prob_one(p,2)<ATOL
    factors=data_factors();data=product_input(factors)
    for stage,blank,target in (('clean',1,0),('bad-data',0,0),('clean',0,1)):
        state,p=run(workspace(stage),factors+basis_factors((blank,target)))
        torch.testing.assert_close(state,workspace_reference(data,stage,blank,target),rtol=0,atol=ATOL)
        assert abs(prob_one(p,2)-(1 if blank or stage=='bad-data' else 0))<ATOL
    print('18parity workspace circuits: coherent stages,clean ancilla,wrong blank,data-change and initial-output boundaries.')
    for clean,expected0 in ((False,.5),(True,1.)):
        state,p=run(coherence(clean),[(1,0),(1,0)])
        if clean:expected=torch.tensor([1,0,0,0],dtype=DTYPE)
        else:expected=torch.tensor([1,1,1,-1],dtype=DTYPE)/2
        torch.testing.assert_close(state,expected,rtol=0,atol=ATOL)
        assert abs(p[:2].sum().item()-expected0)<ATOL
    bad=[(ValueError,lambda:controlled_matrix(2*X)),(ValueError,lambda:controlled_matrix(torch.eye(3,dtype=DTYPE))),(ValueError,lambda:controlled_matrix(torch.eye(2,dtype=torch.complex64))),(ValueError,lambda:controlled_matrix(torch.full((2,2),float('nan'),dtype=DTYPE))),(ValidationError,lambda:source.control(1,ctrl_qubits=(0,))),(CapabilityError,lambda:fq.Circuit(1,dtype=DTYPE).unitary(0,unitary=X).control(1,ctrl_qubits=(1,))),(ValidationError,lambda:source.control(2,ctrl_qubits=(1,1))),(ValidationError,lambda:source.control(1,ctrl_qubits=(1,2))),(ValueError,lambda:workspace('reset')),(ValueError,lambda:workspace_reference(data,'clean',blank=2))]
    for error,action in bad:
        try:action()
        except error:pass
        else:raise AssertionError('Invalid control/ancilla contract admitted')
    assert RUNS==100,RUNS
    print('2coherence circuits: data P0=0.5without cleanup,1.0with uncompute;10invalid contracts rejected.')
    print('100 actual CPU complex128 circuits; atol=1e-12,rtol=0; no control measurement,reset,shots or hardware.')


if __name__=='__main__':main()
