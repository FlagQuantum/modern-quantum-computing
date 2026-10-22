"""7.3 Phase-fixed Bell basis: native gates/readout plus independent scalar references.

Label a is phase, b is parity; full basis q0q1. Conditional branches below are
classical ideal-projector calculations, not native sampled-collapse requests.
"""
import math
import cmath
from dataclasses import replace
from importlib.metadata import version
import torch
import flagquantum as fq
try:
    from examples.foundations.tensor_spaces import OPTIONS
except ModuleNotFoundError:
    from tensor_spaces import OPTIONS
D=torch.complex128
ATOL=1e-12
RUNS=0


def label(a,b):
    if any(type(x) is not int or x not in (0,1) for x in (a,b)):
        raise ValueError('Literal bits a,b required')
    return 2*a+b


def support(n,pair):
    if type(n) is not int or not 2<=n<=4 or not isinstance(pair,tuple) or len(pair)!=2 or any(type(q) is not int or not 0<=q<n for q in pair) or pair[0]==pair[1]:
        raise ValueError('Two distinct ordered qubits in a2-4qubit teaching register required')
    return pair


def bell_vector(a,b):
    label(a,b)
    v=torch.zeros(4,dtype=D);v[b]=1/math.sqrt(2);v[2+(1^b)]=(-1)**a/math.sqrt(2)
    return v


BELL=torch.stack([bell_vector(a,b) for a in (0,1) for b in (0,1)],dim=1)
XX=torch.tensor([[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]],dtype=D)
ZZ=torch.diag(torch.tensor([1,-1,-1,1],dtype=D))


def encode(circuit,pair=(0,1)):
    left,right=support(circuit.n_qubits,pair)
    return circuit.h(left).cx(left,right)


def decode(circuit,pair=(0,1)):
    left,right=support(circuit.n_qubits,pair)
    return circuit.cx(left,right).h(left)


def preparation(a,b,n=2,pair=(0,1),method='basis'):
    label(a,b);left,right=support(n,pair)
    if method not in ('basis','left','right-zx','right-xz'):raise ValueError('Unknown declared preparation method')
    circuit=fq.Circuit(n,dtype=D)
    if method=='basis':
        if a:circuit.x(left)
        if b:circuit.x(right)
        return encode(circuit,pair)
    encode(circuit,pair)
    if method=='left':
        if a:circuit.z(left)
        if b:circuit.x(right)
    elif method=='right-zx':
        if a:circuit.z(right)
        if b:circuit.x(right)
    else:
        if b:circuit.x(right)
        if a:circuit.z(right)
    return circuit


def vector_contract(v):
    if not isinstance(v,torch.Tensor) or v.shape!=(4,) or v.dtype!=D or v.device.type!='cpu' or not bool(torch.isfinite(v).all()):
        raise ValueError('Finite unbatched CPUcomplex128 two-qubit pure vector required')
    if abs(torch.vdot(v,v).item()-1)>ATOL:raise ValueError('Normalized input required;no repair')


def coordinates(v):
    vector_contract(v)
    x,y,z,w=v
    return torch.stack((x+w,y+z,x-w,y-z))/math.sqrt(2)


def branches(v):
    c=coordinates(v);out=[]
    for j,z in enumerate(c):
        p=float(z.abs().square())
        if p==0:
            if z.item()!=0:raise ArithmeticError('Positive branch probability underflow')
            out.append((p,None))
        else:out.append((p,(z/abs(z))*BELL[:,j]))
    assert abs(sum(p for p,_ in out)-1)<ATOL
    return tuple(out)


def histogram(bits):
    if not isinstance(bits,torch.Tensor) or bits.dtype!=torch.int64 or bits.ndim!=2 or bits.shape[1]!=2 or bits.shape[0]<1 or not bool(((bits==0)|(bits==1)).all()):
        raise ValueError('Nonempty int64 two-column binary records required')
    return torch.bincount(2*bits[:,0]+bits[:,1],minlength=4)


def query(circuit,pair=(0,1),shots=None,seed=17):
    global RUNS
    left,right=support(circuit.n_qubits,pair)
    if shots is not None and (type(shots) is not int or shots<1):raise ValueError('Positive literal shot count required')
    if type(seed) is not int or seed<0:raise ValueError('Nonnegative literal seed required')
    outputs=[fq.probabilities(qubits=pair),fq.expectation(fq.X(left)@fq.X(right),name='xx'),fq.expectation(fq.Z(left)@fq.Z(right),name='zz')]
    kwargs={}
    if shots is not None:outputs.append(fq.samples(qubits=pair));kwargs['shots']=shots
    result=fq.run(circuit,outputs=outputs,options=replace(OPTIONS,seed=seed),**kwargs)
    RUNS+=1
    raw,p=result.statevector(),result.probabilities
    assert raw.shape==(1,2**circuit.n_qubits) and raw.dtype==D
    assert p.shape==(1,4) and p.dtype==torch.float64
    assert raw.device.type==p.device.type=='cpu' and bool(torch.isfinite(raw).all()) and bool(torch.isfinite(p).all())
    ref=torch.zeros(4,dtype=torch.float64)
    for index,z in enumerate(raw[0].tolist()):
        key=2*((index>>(circuit.n_qubits-1-left))&1)+((index>>(circuit.n_qubits-1-right))&1)
        ref[key]+=abs(z)**2
    assert torch.allclose(p[0],ref,atol=ATOL,rtol=0)
    report=dict(state=raw[0],probabilities=p[0],xx=float(result.expectation('xx')[0]),zz=float(result.expectation('zz')[0]))
    if shots is not None:
        bits=result.samples
        assert bits.shape==(1,shots,2) and bits.dtype==torch.int64
        report['bits']=bits[0];report['counts']=histogram(bits[0]);assert int(report['counts'].sum())==shots
    return report


def complex_preparation(theta,phi,eta,lam):
    if any(type(t) not in (float,int) or not math.isfinite(t) for t in (theta,phi,eta,lam)):raise ValueError('Finite literal radian angles required')
    return fq.Circuit(2,dtype=D).ry(0,theta).p(0,phi).ry(1,eta).p(1,lam).cx(0,1)


def scalar_preparation(theta,phi,eta,lam):
    a0,a1=math.cos(theta/2),cmath.exp(1j*phi)*math.sin(theta/2)
    b0,b1=math.cos(eta/2),cmath.exp(1j*lam)*math.sin(eta/2)
    return torch.tensor([a0*b0,a0*b1,a1*b1,a1*b0],dtype=D)


def embedded_bell(n,pair,a,b,factors):
    left,right=support(n,pair);target=bell_vector(a,b);values=[]
    for k in range(2**n):
        bits=list(map(int,format(k,f'0{n}b')))
        z=target[2*bits[left]+bits[right]].item()
        for q,factor in factors.items():z*=factor[bits[q]]
        values.append(z)
    return torch.tensor(values,dtype=D)


def main():
    assert version('flagquantum')=='0.3.1' and version('torch').split('+')[0]=='2.13.0'
    assert torch.allclose(BELL.mH@BELL,torch.eye(4,dtype=D),atol=ATOL,rtol=0)
    for a in (0,1):
        for b in (0,1):
            r=query(preparation(a,b));assert torch.allclose(r['state'],bell_vector(a,b),atol=ATOL,rtol=0)
            assert abs(r['xx']-(-1)**a)<ATOL and abs(r['zz']-(-1)**b)<ATOL
            r=query(decode(preparation(a,b)),shots=32,seed=23)
            expected=torch.zeros(4,dtype=D);expected[label(a,b)]=1
            assert torch.allclose(r['state'],expected,atol=ATOL,rtol=0)
            assert r['bits'].tolist()==[[a,b]]*32
            for method in ('left','right-zx','right-xz'):
                r=query(preparation(a,b,method=method));phase=(-1)**(a*b) if method=='right-xz' else 1
                assert torch.allclose(r['state'],phase*bell_vector(a,b),atol=ATOL,rtol=0)
    print('20 native Bell preparations/readouts: four vectors,Pauli eigenlabels,32-shot labels and Pauli-order phases passed.')
    fixtures=[(.31,.71,.63,-.42),(.9,-1.2,.37,.83),(1.7,.43,-.91,.26),(-.61,-.83,.57,1.1),(.67,1.1,1.31,-.29),(1.3,-.41,.82,.91)]
    for args in fixtures:
        ref=scalar_preparation(*args);r=query(complex_preparation(*args))
        assert torch.allclose(r['state'],ref,atol=ATOL,rtol=0)
        encoded=query(encode(complex_preparation(*args)))
        assert torch.allclose(encoded['state'],BELL@ref,atol=ATOL,rtol=0)
        roundtrip=query(decode(encode(complex_preparation(*args))))
        assert torch.allclose(roundtrip['state'],ref,atol=ATOL,rtol=0)
        analyzed=query(decode(complex_preparation(*args)))
        expected=coordinates(ref)
        assert torch.allclose(analyzed['state'],expected,atol=ATOL,rtol=0)
        assert torch.allclose(analyzed['probabilities'],expected.abs()**2,atol=ATOL,rtol=0)
        for j,(p,branch) in enumerate(branches(ref)):
            projected=BELL[:,j]*torch.vdot(BELL[:,j],ref)
            if p:
                assert torch.allclose(branch,projected/math.sqrt(p),atol=ATOL,rtol=0)
                assert abs(torch.vdot(branch,branch).item()-1)<ATOL
        sampled=query(decode(complex_preparation(*args)),shots=73,seed=31)
        assert torch.equal(sampled['counts'],torch.tensor([sampled['bits'].tolist().count([j//2,j%2]) for j in range(4)]))
    print('30 native complex-basis queries: scalar amplitudes,encoder/inverse,phase-preserving branches and raw-count accounting passed.')
    for theta in (math.pi/3,.91):
        for phi in (0.,.37,math.pi,-.83):
            c=fq.Circuit(2,dtype=D).ry(0,theta).cx(0,1).p(0,phi)
            r=query(decode(c));expected=torch.tensor([(1+math.sin(theta)*math.cos(phi))/2,0,(1-math.sin(theta)*math.cos(phi))/2,0],dtype=torch.float64)
            assert torch.allclose(r['probabilities'],expected,atol=ATOL,rtol=0)
    print('8 phase-sensitive Bell readouts: analytic interference probabilities passed.')
    for a in (0,1):
        for b in (0,1):
            r=query(decode(preparation(a,b),(1,0)),pair=(1,0),shots=17)
            expected=torch.zeros(4,dtype=D);expected[2*b+a]=(-1)**(a*b)
            assert torch.allclose(r['state'],expected,atol=ATOL,rtol=0)
            assert r['bits'].tolist()==[[a,b]]*17
    print('4 reversed ordered analyzers:raw columns(a,b),full basis(b,a) and singlet minus sign passed.')
    for n,pair in ((3,(2,0)),(3,(0,2)),(4,(3,1)),(4,(1,3))):
        for a in (0,1):
            for b in (0,1):
                c=preparation(a,b,n,pair);factors={}
                for q in range(n):
                    if q not in pair:
                        theta=.37+.13*q;phi=-.61+.2*q;c.ry(q,theta).p(q,phi)
                        factors[q]=(math.cos(theta/2),cmath.exp(1j*phi)*math.sin(theta/2))
                r=query(c,pair);expected=embedded_bell(n,pair,a,b,factors)
                assert torch.allclose(r['state'],expected,atol=ATOL,rtol=0)
                r=query(decode(c,pair),pair,shots=19)
                assert r['bits'].tolist()==[[a,b]]*19
    print('32 nonadjacent ordered-register queries:scalar spectator amplitudes and all four decoded labels passed.')
    zero=torch.tensor([1,0,0,0],dtype=D)
    bad=[lambda:bell_vector(True,0),lambda:bell_vector(0,2),lambda:support(2,(0,0)),lambda:support(3,(0,3)),lambda:support(2,(False,1)),
         lambda:coordinates(zero*2),lambda:coordinates(zero.real),lambda:coordinates(zero.reshape(1,4)),
         lambda:query(fq.Circuit(2,dtype=D),shots=0),lambda:histogram(torch.tensor([[0,2]],dtype=torch.int64)),
         lambda:histogram(torch.empty((0,2),dtype=torch.int64)),lambda:preparation(0,0,method='guess')]
    for f in bad:
        try:f()
        except ValueError:pass
        else:raise AssertionError('Invalid Bell contract admitted')
    print('12 malformed contracts rejected before simulation.')
    assert RUNS==94,RUNS
    print('94 CPUcomplex128 native circuits passed;terminal readout distinct from assumed conditional projection.')


if __name__=='__main__':main()
