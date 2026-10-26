"""14.3: finite bounded-error examples; no complexity-class inference from tests."""
import itertools, math
from fractions import Fraction as F
from dataclasses import replace
import torch, flagquantum as fq
try:
    from examples.foundations import statistical_ensembles as e, uniform_reversible as u
except ModuleNotFoundError:
    import statistical_ensembles as e, uniform_reversible as u
D=e.D; RUNS=0

def probability(p):
    if type(p) is not F or not 0<=p<=1:
        raise ValueError('Exact Fraction probability in [0,1] required; no clipping')
    return p

def contract(p,label):
    probability(p)
    if label is not None and (type(label) is not int or label not in (0,1)):
        raise ValueError('Literal yes/no bit or None for outside-promise required')
    return None if label is None else p>=F(2,3) if label==1 else p<=F(1,3)

def word(x):
    if type(x) is not str or any(b not in '01' for b in x):
        raise ValueError('Binary string, including empty, required')
    return tuple(map(int,x))

def family(n,coins='fair',complement=False,deterministic=False):
    if type(n) is not int or not 0<=n<=10000:
        raise ValueError('Bounded host length 0..10000 required')
    if coins not in ('fair','reused') or type(complement) is not bool or type(deterministic) is not bool:
        raise ValueError('Declared coin model and literal Boolean flags required')
    # Layout: data, two coins, zero workspace, answer. Logical kernel only.
    ops=[]
    if not deterministic:
        ops.extend([('H',(n,)),('H',(n+1,))])
        ops.append(('CCX',(n,n+1,n+2)) if coins=='fair' else ('CX',(n,n+2)))
    ops.extend(('CX',(j,n+3)) for j in range(n))
    if not deterministic:
        ops.append(('CX',(n+2,n+3)))
        ops.append(('CCX',(n,n+1,n+2)) if coins=='fair' else ('CX',(n,n+2)))
    if complement: ops.append(('X',(n+3,)))
    return tuple(ops)

def execute(x,coins='fair',complement=False,deterministic=False,mode='statevector',shots=19):
    global RUNS
    b=word(x); n=len(b)
    ops=family(n,coins,complement,deterministic)
    if n>3 or mode not in ('statevector','density_matrix') or type(shots) is not int or not 1<=shots<=1000:
        raise ValueError('Native teaching n<=3, tested mode and fixed shots 1..1000 required')
    c=fq.Circuit(n+4,dtype=D)
    for j,v in enumerate(b):
        if v: c.X(j)
    for op,labels in ops: getattr(c,op)(*labels)
    target=torch.zeros(2**(n+4),dtype=D)
    for a,d in ([(0,0)] if deterministic else itertools.product((0,1),repeat=2)):
        err=0 if deterministic else a*d if coins=='fair' else a
        z=sum(b)%2 ^ err ^ int(complement)
        target[u.index(b+(a,d,0,z))]=1 if deterministic else .5
    p_exact=F(0)
    for k in range(len(target)):
        if k&1:p_exact+=F(1 if deterministic else 1,1 if deterministic else 4) if target[k]!=0 else F(0)
    r=fq.run(c,outputs=[fq.density_matrix(name='rho'),fq.probabilities(name='full'),
        fq.probabilities(qubits=(n+3,),name='answer'),fq.samples(qubits=(n+3,),name='record')],
        shots=shots,options=replace(e.OPTIONS,mode=mode,seed=47)); RUNS+=1
    e.close(r.measurement('rho').value[0],torch.outer(target,target.conj()))
    e.close(r.measurement('full').value[0],target.abs().square())
    e.close(r.measurement('answer').value[0],torch.tensor([float(1-p_exact),float(p_exact)],dtype=torch.float64))
    if mode=='statevector':e.close(r.statevector()[0],target)
    record=r.measurement('record').value
    assert record.shape==(1,shots,1) and bool(((record==0)|(record==1)).all())
    count=int(record.sum()); assert count+(shots-count)==shots
    leak=sum(r.measurement('full').value[0,k].item() for k in range(len(target)) if u.bits(k,n+4)[n+2])
    assert abs(leak)<1e-12
    return r,p_exact,dict(qubits=n+4,kernel=len(ops),loading=sum(b),count=count,shots=shots,leak=leak)

def selector(x,mode='statevector'):
    """Promise x0=x1; outside-promise inputs are still explicitly evaluated."""
    global RUNS
    b=word(x)
    if len(b)!=2 or mode not in ('statevector','density_matrix'):raise ValueError('Two bits and tested mode required')
    # Sources x0,x1,r. Nodes d=x0 XOR x1; t=r AND d; out=x0 XOR t.
    nodes=(('XOR',(0,1)),('AND',(2,3)),('XOR',(0,4)))
    ops,cost=u.translate(3,nodes,(5,)); c=fq.Circuit(7,dtype=D)
    for j,v in enumerate(b):
        if v:c.X(j)
    c.H(2)
    for op,qs in ops:getattr(c,op)(*qs)
    target=torch.zeros(128,dtype=D)
    for r in (0,1):
        out=b[r]  # Independent scalar selector, not the Boolean graph evaluator.
        target[u.index(b+(r,0,0,0,out))]=1/math.sqrt(2)
    result=fq.run(c,outputs=[fq.density_matrix(name='rho'),fq.probabilities(qubits=(6,),name='answer')],
        options=replace(e.OPTIONS,mode=mode)); RUNS+=1
    e.close(result.measurement('rho').value[0],torch.outer(target,target.conj()))
    p=F(b[0]+b[1],2);e.close(result.measurement('answer').value[0],torch.tensor([float(1-p),float(p)],dtype=torch.float64))
    return result,p, b[0] if b[0]==b[1] else None

def tail(p,k):
    probability(p)
    if type(k) is not int or not 1<=k<=101 or k%2!=1:raise ValueError('Odd host trial count 1..101 required')
    return sum((F(math.comb(k,j))*p**j*(1-p)**(k-j) for j in range(k//2+1,k+1)),F(0))

def repetition_budget(gamma):
    if type(gamma) is not F or not 0<gamma<=F(1,2):raise ValueError('Exact positive half-gap at most 1/2 required')
    k=math.ceil(F(3,4)/gamma**2)
    return k if k%2 else k+1

def majority(bit,independent=True):
    """Three trials, literal CCX majority; native statevector probabilities only."""
    global RUNS
    if type(bit) is not int or bit not in (0,1) or type(independent) is not bool:
        raise ValueError('Literal answer bit and independence flag required')
    q=10 if independent else 6;out=q-1; c=fq.Circuit(q,dtype=D)
    for j in range(6 if independent else 2):c.H(j)
    flags=(6,7,8) if independent else (2,3,4)
    for j,t in enumerate(flags):
        a,d=(2*j,2*j+1) if independent else (0,1)
        c.CCX(a,d,t)
        if bit:c.X(t)
    for a,d in ((flags[0],flags[1]),(flags[0],flags[2]),(flags[1],flags[2])):c.CCX(a,d,out)
    result=fq.run(c,outputs=[fq.probabilities(qubits=(out,),name='vote')],
        options=replace(e.OPTIONS,mode='statevector'));RUNS+=1
    # Enumerate fair classical coin records independently of native amplitudes.
    rcount=6 if independent else 2;hist=torch.zeros(2**q,dtype=torch.float64)
    for coin in itertools.product((0,1),repeat=rcount):
        z=tuple(bit^(coin[2*j]*coin[2*j+1] if independent else coin[0]*coin[1]) for j in range(3))
        hist[u.index(coin+z+(int(sum(z)>=2),))]+=1/2**rcount
    # The default probability-request guard is 8 qubits. Query one vote qubit;
    # compare the full simulator vector's squared moduli to the classical law.
    e.close(result.statevector()[0].abs().square(),hist)
    error=tail(F(1,4),3) if independent else F(1,4)
    p=1-error if bit else error
    e.close(result.measurement('vote').value[0],torch.tensor([float(1-p),float(p)],dtype=torch.float64))
    return result,error

def invalid_checks():
    calls=[lambda:contract(.75,1),lambda:contract(F(-1),0),lambda:contract(F(2),1),lambda:contract(F(1,2),True),
        lambda:family(True),lambda:family(-1),lambda:family(0,'unknown'),lambda:execute('0x'),lambda:execute('0000'),
        lambda:execute('',shots=0),lambda:tail(F(1,4),2),lambda:repetition_budget(F(0)),lambda:majority(1,1),lambda:selector('0')]
    before=RUNS
    for call in calls:
        try:call()
        except ValueError:pass
        else:raise AssertionError('Malformed bounded-error contract accepted')
    assert RUNS==before;return len(calls)

def main():
    for mode in ('statevector','density_matrix'):
        for n in range(3):
            for bits in itertools.product('01',repeat=n):
                x=''.join(bits);f=sum(word(x))%2
                _,p,_=execute(x,deterministic=True,mode=mode);assert p==f
                for comp in (False,True):
                    _,p,_=execute(x,complement=comp,mode=mode);assert contract(p,f^int(comp))
                    _,p,_=execute(x,coins='reused',complement=comp,mode=mode);assert p==F(1,2) and not contract(p,f^int(comp))
        for bits in itertools.product('01',repeat=2):
            _,p,label=selector(''.join(bits),mode);assert contract(p,label) is (None if label is None else True)
    for bit in (0,1):
        for independent in (False,True):majority(bit,independent)
    assert RUNS==82
    for n in (0,1,17,1000):assert len(family(n))==n+5
    for k in (1,3,5,13):
        for j in range(17):
            p=F(j,16);assert tail(1-p,k)==1-tail(p,k)
        assert tail(F(1,4),k)<=F(1,1)/(4*k*F(1,4)**2)
    assert repetition_budget(F(1,4))==13 and tail(F(1,4),3)==F(5,32)
    assert contract(F(2,3),1) and contract(F(1,3),0)
    assert not contract(F(1,2),0) and not contract(F(1,2),1)
    assert F(7,8)>F(2,3) and not contract(F(0),1)
    print('82 actual native circuits:14 deterministic,28 fair-coin,28 reused-coin,8 promise-selector and4 majority cases passed.')
    print('Full clean states/probabilities checked in both modes for78 circuits;4 majority cases use native statevector probabilities.')
    print('Independent majority error5/32;shared-coin error1/4. Fixed-gap budget13;exact rational boundary/tail checks passed.')
    print(f'{invalid_checks()} malformed contracts rejected before execution;finite checks are not complexity-class certificates.')
if __name__=='__main__':main()
