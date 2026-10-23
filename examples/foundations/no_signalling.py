"""7.7 finite local instruments:unconditioned marginals versus remote records.

Native static gates and terminal samples;general branches/effects are explicit
classical analysis,not native sampled collapse,reset or classical networking.
"""
import cmath
import itertools
import math
from dataclasses import replace
from importlib.metadata import version
import flagquantum as fq
import torch
try:
    from examples.foundations.tensor_spaces import OPTIONS
except ModuleNotFoundError:
    from tensor_spaces import OPTIONS
D=torch.complex128
ATOL=1e-12
RUNS=0
I=torch.eye(2,dtype=D)
X=torch.tensor([[0,1],[1,0]],dtype=D)
Y=torch.tensor([[0,-1j],[1j,0]],dtype=D)
Z=torch.diag(torch.tensor([1,-1],dtype=D))
H=torch.tensor([[1,1],[1,-1]],dtype=D)/math.sqrt(2)
P0=torch.diag(torch.tensor([1,0],dtype=D));P1=I-P0


def vector(v):
    if (not isinstance(v,torch.Tensor) or v.ndim!=1 or v.numel() not in (4,8,16)
        or v.dtype!=D or v.device.type!='cpu' or v.layout!=torch.strided or not bool(torch.isfinite(v).all())):
        raise ValueError('Finite unbatched CPUcomplex1282-4qubit state required')
    if abs(float(torch.vdot(v,v).real)-1)>ATOL:raise ValueError('Normalized input required;no repair')
    return v.numel().bit_length()-1


def support(n,positions):
    if type(positions) is not tuple or not positions or any(type(q) is not int or not 0<=q<n for q in positions) or len(set(positions))!=len(positions):
        raise ValueError('Distinct ordered in-register positions required')


def matrix(M,d):
    if not isinstance(M,torch.Tensor) or M.shape!=(d,d) or M.dtype!=D or M.device.type!='cpu' or not bool(torch.isfinite(M).all()):
        raise ValueError('Finite square CPUcomplex128 local matrix of declared dimension required')


def apply(v,M,positions):
    n=v.numel().bit_length()-1;support(n,positions);d=2**len(positions);matrix(M,d)
    out=torch.zeros_like(v)
    for k in range(2**n):
        row=sum(((k>>(n-1-q))&1)<<(len(positions)-1-j) for j,q in enumerate(positions))
        for col in range(d):
            source=k
            for j,q in enumerate(positions):
                mask=1<<(n-1-q);bit=(col>>(len(positions)-1-j))&1
                source=(source|mask) if bit else (source&~mask)
            out[k]+=M[row,col]*v[source]
    return out


def instrument(groups,d):
    if type(groups) is not tuple or not groups or any(type(g) is not tuple or not g for g in groups):
        raise ValueError('Nonempty tuple of outcome-indexed hidden-operator tuples required')
    total=torch.zeros((d,d),dtype=D)
    for group in groups:
        for M in group:matrix(M,d);total+=M.conj().T@M
    if not torch.allclose(total,torch.eye(d,dtype=D),atol=ATOL,rtol=0):
        raise ValueError('Incomplete local process;postselection is not a deterministic operation')


def effects(effects,d):
    if type(effects) is not tuple or not effects:raise ValueError('Complete finite tuple of Bob effects required')
    total=torch.zeros((d,d),dtype=D)
    for E in effects:
        matrix(E,d)
        if not torch.allclose(E,E.conj().T,atol=ATOL,rtol=0) or float(torch.linalg.eigvalsh(E).min()) < -ATOL:
            raise ValueError('Positive Hermitian effects required;no repair')
        total+=E
    if not torch.allclose(total,torch.eye(d,dtype=D),atol=ATOL,rtol=0):raise ValueError('Bob effects must sum to identity')


def quadratic(v,E,positions):
    z=torch.vdot(v,apply(v,E,positions))
    if abs(float(z.imag))>ATOL:raise ValueError('Nonreal probability')
    return float(z.real)


def analyze(v,A,groups,B,es):
    n=vector(v);support(n,A);support(n,B)
    if set(A)&set(B):raise ValueError('Alice and Bob supports must be disjoint')
    instrument(groups,2**len(A));effects(es,2**len(B))
    weights=[];joint=[];columns=[];conditionals=[]
    for group in groups:
        hidden=tuple(apply(v,M,A) for M in group)
        p=sum(float(torch.vdot(w,w).real) for w in hidden)
        if p==0 and any(bool((w!=0).any()) for w in hidden):
            raise FloatingPointError('Positive branch squared norm underflowed')
        q=[sum(quadratic(w,E,B) for w in hidden) for E in es]
        assert abs(sum(q)-p)<ATOL
        weights.append(p);joint.append(q);columns.append(hidden)
        conditionals.append(None if p==0 else torch.tensor(q,dtype=torch.float64)/p)
    joint=torch.tensor(joint,dtype=torch.float64)
    baseline=torch.tensor([quadratic(v,E,B) for E in es],dtype=torch.float64)
    marginal=joint.sum(0)
    assert torch.allclose(marginal,baseline,atol=ATOL,rtol=0)
    assert abs(sum(weights)-1)<ATOL
    return {'weights':torch.tensor(weights,dtype=torch.float64),'joint':joint,'conditional':conditionals,
        'columns':tuple(columns),'baseline':baseline,'marginal':marginal}


def analyzer(basis):
    if basis=='Z':return I
    if basis=='X':return H
    if basis=='Y':return H@torch.diag(torch.tensor([1,-1j],dtype=D))
    raise ValueError('Declare X,Y or Z basis')


def projectors(basis):
    R=analyzer(basis)
    return tuple(R.conj().T@P@R for P in (P0,P1))


def groups_for(basis):
    return tuple((P,) for P in projectors(basis))


def weak(strength):
    if type(strength) not in (int,float) or not math.isfinite(strength) or not 0<=strength<=1:
        raise ValueError('Finite weak strength in[0,1] required')
    c,s=math.sqrt((1+strength)/2),math.sqrt((1-strength)/2)
    return ((torch.diag(torch.tensor([c,s],dtype=D)),),(torch.diag(torch.tensor([s,c],dtype=D)),))


def reset_groups():
    return ((torch.tensor([[1,0],[0,0]],dtype=D),torch.tensor([[0,1],[0,0]],dtype=D)),)


def basis_calls(c,q,basis):
    analyzer(basis)
    if basis=='Y':c.p(q,-math.pi/2)
    if basis in ('X','Y'):c.h(q)
    return c


def fixture(theta,phase,n=2,pair=(0,1)):
    if any(type(x) not in (int,float) or not math.isfinite(x) for x in (theta,phase)):
        raise ValueError('Finite real preparation angles required')
    if type(n) is not int or not 2<=n<=4:raise ValueError('Teaching register bound2-4required')
    support(n,pair)
    if len(pair)!=2:raise ValueError('Ordered(Alice,Bob) pair required')
    a,b=pair;c=fq.Circuit(n,dtype=D).ry(a,theta).p(a,phase).cx(a,b)
    v=torch.zeros(2**n,dtype=D)
    for k in range(2**n):
        bits=[int(x) for x in format(k,f'0{n}b')]
        if bits[a]!=bits[b]:continue
        z=math.cos(theta/2) if bits[a]==0 else cmath.exp(phase*1j)*math.sin(theta/2)
        for q in range(n):
            if q not in pair:z*=math.cos((.39+.11*q)/2) if bits[q]==0 else cmath.exp(-.17j*(q+1))*math.sin((.39+.11*q)/2)
        v[k]=z
    for q in range(n):
        if q not in pair:c.ry(q,.39+.11*q).p(q,-.17*(q+1))
    return c,v


def query(theta=math.pi/2,phase=0.,alice='Z',bob='Z',n=2,pair=(0,1),shots=31,seed=73):
    global RUNS
    if type(shots) is not int or shots<1 or type(seed) is not int or seed<0:raise ValueError('Positive shot count/nonnegative literal seed required')
    RA,RB=analyzer(alice),analyzer(bob)
    c,v=fixture(theta,phase,n,pair);a,b=pair
    basis_calls(c,a,alice);basis_calls(c,b,bob)
    result=fq.run(c,outputs=[fq.probabilities(qubits=pair),fq.samples(qubits=pair)],shots=shots,options=replace(OPTIONS,seed=seed));RUNS+=1
    expected=apply(apply(v,RA,(a,)),RB,(b,))
    assert result.statevector().shape==(1,2**n)
    assert torch.allclose(result.statevector()[0],expected,atol=ATOL,rtol=0)
    report=analyze(v,(a,),groups_for(alice),(b,),projectors(bob))
    assert torch.allclose(result.probabilities[0].reshape(2,2),report['joint'],atol=ATOL,rtol=0)
    # Analyzer+terminal readout has local operators P_a R;ideal restored
    # projectors R^dag P_a R give identical remote predictions.
    g=tuple((P@RA,) for P in (P0,P1))
    direct=analyze(v,(a,),g,(b,),projectors(bob))
    assert torch.allclose(direct['joint'],report['joint'],atol=ATOL,rtol=0)
    raw=result.samples
    assert raw.shape==(1,shots,2) and raw.dtype==torch.int64 and bool(((raw==0)|(raw==1)).all())
    counts=torch.bincount(2*raw[0,:,0]+raw[0,:,1],minlength=4).reshape(2,2)
    assert int(counts.sum())==shots
    report.update(state=v,analyzed_state=expected,bits=raw[0],counts=counts)
    return report


def dilation(strength=.43,theta=.87,phase=-.39,kind='weak'):
    global RUNS
    if kind not in ('weak','reset'):raise ValueError('Declare weak or reset fixture')
    groups=weak(strength) if kind=='weak' else reset_groups()
    c=fq.Circuit(3,dtype=D).ry(0,theta).p(0,phase).cx(0,1)
    if kind=='weak':
        beta0=math.acos(strength);beta1=math.pi-beta0
        c.ry(2,beta0).cry(0,2,beta1-beta0)
    else:c.cx(0,2).cx(2,0)
    result=fq.run(c,outputs=[fq.probabilities(qubits=(2,1),name='meter-bob'),fq.probabilities(qubits=(0,),name='alice')],options=OPTIONS);RUNS+=1
    # One native execution;two named probability requests are inspected below.
    _,v=fixture(theta,phase)
    flat=tuple(M for group in groups for M in group)
    expected=torch.zeros(8,dtype=D)
    for meter,M in enumerate(flat):
        w=apply(v,M,(0,))
        for j,z in enumerate(w):expected[2*j+meter]=z
    assert torch.allclose(result.statevector()[0],expected,atol=ATOL,rtol=0)
    p=torch.zeros((2,2),dtype=torch.float64)
    for meter,M in enumerate(flat):
        w=apply(v,M,(0,))
        for b in (0,1):p[meter,b]=sum(float(abs(w[2*a+b])**2) for a in (0,1))
    assert torch.allclose(result.measurement('meter-bob').value[0].reshape(2,2),p,atol=ATOL,rtol=0)
    assert torch.allclose(p.sum(0),torch.tensor([math.cos(theta/2)**2,math.sin(theta/2)**2],dtype=torch.float64),atol=ATOL,rtol=0)
    alice_expected=torch.tensor([1.,0.] if kind=='reset' else [math.cos(theta/2)**2,math.sin(theta/2)**2],dtype=torch.float64)
    assert torch.allclose(result.measurement('alice').value[0],alice_expected,atol=ATOL,rtol=0)
    return result.statevector()[0],p


def generic(n):
    global RUNS
    if type(n) is not int or not 2<=n<=4:raise ValueError('Teaching bound2-4required')
    c=fq.Circuit(n,dtype=D)
    for q in range(n):c.ry(q,.43+.19*q).p(q,-.21*(q+1))
    for q in range(n-1):c.cx(q,q+1)
    result=fq.run(c,outputs=[fq.probabilities()],options=OPTIONS);RUNS+=1
    expected=torch.zeros(2**n,dtype=D)
    for k in range(2**n):
        bits=[int(x) for x in format(k,f'0{n}b')];z=1+0j
        for q,bit in enumerate(bits):z*=math.cos((.43+.19*q)/2) if bit==0 else cmath.exp(-.21j*(q+1))*math.sin((.43+.19*q)/2)
        for q in range(n-1):bits[q+1]^=bits[q]
        index=sum(bit<<(n-1-q) for q,bit in enumerate(bits));expected[index]=z
    assert torch.allclose(result.statevector()[0],expected,atol=ATOL,rtol=0)
    return expected


def received(a,basis):
    global RUNS
    if type(a) is not int or a not in (0,1) or basis not in ('Z','X'):raise ValueError('Literal bit and declared Z/X message basis required')
    c=fq.Circuit(1,dtype=D)
    if basis=='Z':
        if a:c.x(0)     # known conditional input fixture
        if a:c.x(0)     # correction chosen after assumed record receipt
    else:
        c.h(0)
        if a:c.z(0)     # prepares conditional +/- fixture
        if a:c.z(0)     # record-dependent correction
        c.h(0)
    result=fq.run(c,outputs=[fq.probabilities()],options=OPTIONS);RUNS+=1
    assert torch.allclose(result.statevector()[0],torch.tensor([1,0],dtype=D),atol=ATOL,rtol=0)
    return result.probabilities[0]


def main():
    assert version('flagquantum')=='0.3.1' and RUNS==0
    for theta,phase in ((math.pi/2,0.),(.83,.47),(0.,0.)):
        for alice,bob in itertools.product(('Z','X','Y'),repeat=2):query(theta,phase,alice,bob)
    print('27 native circuits:Bell,unequal and product inputs;all nine basis pairs,complex Y branches and unchanged Bob marginals passed.')
    for n in (2,3,4):
        for pair in itertools.permutations(range(n),2):
            for alice in ('Z','X','Y'):query(.91,-.63,alice,'Y',n,pair)
    print('60 native circuits:all20ordered supports,complex spectators and independent full amplitudes passed.')
    classical=0
    for n in (2,3,4):
        v=generic(n)
        for a,b in itertools.permutations(range(n),2):
            for gs in (groups_for('X'),groups_for('Y'),weak(.37),reset_groups(),((H,),)):
                for bs in ('X','Y','Z'):
                    analyze(v,(a,),gs,(b,),projectors(bs));classical+=1
        if n==4:
            for A,B in (((0,2),(3,1)),((2,0),(1,3))):
                lifted=tuple((torch.kron(M,I),) for group in weak(.59) for M in group)
                es=tuple(torch.kron(E,F) for E in projectors('Y') for F in projectors('X'))
                analyze(v,A,lifted,B,es);classical+=1
    assert classical==302,classical
    print('3 native generic preparations and302classical complete-instrument/effect cases passed,including ordered composite local supports.')
    for strength in (0.,.43,1.):
        for kind in ('weak','reset'):dilation(strength,kind=kind)
    print('6 native coherent dilation fixtures:weak meter/reset-isometry marginals match classical branches;no collapse/reset endpoint claimed.')
    for a,basis in itertools.product((0,1),('Z','X')):received(a,basis)
    print('4 native fresh Bob branch fixtures:record-dependent corrections give zero only after assumed classical receipt.')
    bell=torch.tensor([1,0,0,1],dtype=D)/math.sqrt(2)
    selected=analyze(bell,(0,),groups_for('Z'),(1,),projectors('Z'))
    assert float(selected['conditional'][0][0])==1 and abs(float(selected['marginal'][0])-.5)<ATOL
    wrong=torch.tensor([1,1],dtype=D)/math.sqrt(2)
    assert abs(float(torch.vdot(wrong,P0@wrong))-.5)<ATOL
    rare=torch.tensor([1,0,0,1e-10],dtype=D)
    r=analyze(rare,(0,),groups_for('Z'),(1,),projectors('Z'))
    assert r['weights'][1]>0 and abs(float(r['conditional'][1][1])-1)<ATOL
    zero=analyze(torch.tensor([1,0,0,0],dtype=D),(0,),groups_for('Z'),(1,),projectors('Z'))
    assert zero['conditional'][1] is None
    under=torch.tensor([1,0,0,1e-200],dtype=D)
    try:analyze(under,(0,),groups_for('Z'),(1,),projectors('Z'))
    except FloatingPointError:pass
    else:raise AssertionError('Underflow hidden')
    bad=[lambda:instrument(((P0,),),2),lambda:instrument((),2),lambda:instrument(((2*I,),),2),
         lambda:effects((P0,),2),lambda:effects((I+Z,-Z),2),lambda:effects((X,),2),
         lambda:analyze(2*bell,(0,),groups_for('Z'),(1,),projectors('Z')),
         lambda:analyze(bell.real,(0,),groups_for('Z'),(1,),projectors('Z')),
         lambda:analyze(bell,(0,),groups_for('Z'),(0,),projectors('Z')),
         lambda:analyze(bell,(2,),groups_for('Z'),(1,),projectors('Z')),
         lambda:weak(-.1),lambda:weak(float('nan')),lambda:query(alice='unknown'),
         lambda:query(shots=0),lambda:query(seed=-1),lambda:received(True,'Z')]
    for attempt in bad:
        before=RUNS
        try:attempt()
        except ValueError:pass
        else:raise AssertionError('Malformed contract admitted')
        assert before==RUNS
    print('16malformed contracts rejected;positive1e-20branch retained,zero branch undefined and nonzero-norm underflow explicit.')
    assert RUNS==100,RUNS
    print('100CPUcomplex128native circuits passed;postselection and classical communication are not Alice-only nonselective operations.')


if __name__=='__main__':main()
