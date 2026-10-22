"""6.6: native terminal samples, explicit index/count conversion, exact finite ensemble checks."""
from dataclasses import replace
from fractions import Fraction as F
from itertools import product, permutations
from math import pi, prod, sin, cos, isfinite
from importlib.metadata import version
import torch
import flagquantum as fq
try:
    from examples.foundations.projective_born import OPTIONS, D, ATOL
except ModuleNotFoundError:
    from projective_born import OPTIONS, D, ATOL
RUNS = 0


def positive_integer(x):
    if type(x) is not int or x <= 0: raise ValueError('Positive literal integer required')
    return x


def histogram(bits):
    if not isinstance(bits,torch.Tensor) or bits.device.type != 'cpu' or bits.dtype != torch.int64 or bits.ndim != 2 or bits.shape[0] == 0 or not 1 <= bits.shape[1] <= 4 or not bool(((bits==0)|(bits==1)).all()):
        raise ValueError('Nonempty CPU int64 binary rows with 1-4 declared columns required')
    k=bits.shape[1]
    weights=2**torch.arange(k-1,-1,-1,dtype=torch.int64)
    indices=bits@weights
    counts=torch.bincount(indices,minlength=2**k)
    assert counts.sum().item()==len(bits)
    return indices,counts,counts.to(torch.float64)/len(bits)


def native(circuit,selected,N,seed):
    global RUNS
    positive_integer(N)
    if type(seed) is not int or seed < 0:raise ValueError('Nonnegative literal seed required')
    n=circuit.n_qubits
    if not 1 <= n <= 4 or not isinstance(selected,tuple) or not selected or any(type(q) is not int or not 0 <= q < n for q in selected) or len(set(selected)) != len(selected):
        raise ValueError('Distinct ordered qubits required; dense teaching guard 1-4 qubits')
    r=fq.run(circuit,outputs=[fq.probabilities(qubits=selected),fq.samples(qubits=selected)],shots=N,options=replace(OPTIONS,seed=seed))
    RUNS+=1
    p,bits=r.probabilities,r.samples
    k=len(selected)
    assert p.shape==(1,2**k) and p.dtype==torch.float64
    assert bits.shape==(1,N,k) and bits.dtype==torch.int64
    assert p.device.type==bits.device.type=='cpu' and torch.isfinite(p).all()
    assert bool((p>=0).all()) and abs(p.sum().item()-1)<ATOL
    # Independent scalar indexing of full actual state amplitudes.
    ref=torch.zeros(2**k,dtype=torch.float64)
    for j,z in enumerate(r.statevector()[0].tolist()):
        key=0
        for q in selected:key=2*key+((j>>(n-1-q))&1)
        ref[key]+=abs(z)**2
    torch.testing.assert_close(p[0],ref,atol=ATOL,rtol=0)
    ids,counts,freq=histogram(bits[0])
    assert bool((p[0,ids]>0).all())
    return p[0],bits[0],counts,freq


def register(theta=pi/3):
    if type(theta) not in (int,float) or not isfinite(theta):raise ValueError('Finite radian angle required')
    return fq.Circuit(3,dtype=D).ry(0,theta).cx(0,2).x(2)


def ensemble(probabilities,N):
    positive_integer(N)
    if not isinstance(probabilities,tuple) or not probabilities or any(type(p) is not F or p<0 for p in probabilities) or sum(probabilities)!=1:
        raise ValueError('Normalized tuple of exact nonnegative Fraction probabilities required')
    k=len(probabilities)
    if k**N>4096:raise ValueError('Exact enumeration teaching guard: at most 4096 sequences')
    rows=[]
    for seq in product(range(k),repeat=N):
        weight=prod((probabilities[j] for j in seq),start=F(1))
        frequencies=tuple(F(seq.count(j),N) for j in range(k))
        rows.append((seq,weight,frequencies))
    assert sum(w for _,w,_ in rows)==1
    for j,p in enumerate(probabilities):assert sum(w*f[j] for _,w,f in rows)==p
    return rows


def invalid_checks():
    z=torch.zeros((2,1),dtype=torch.int64)
    calls=[lambda:histogram(z.float()),lambda:histogram(z[0]),lambda:histogram(z[:0]),
           lambda:histogram(torch.tensor([[2]],dtype=torch.int64)),lambda:histogram(torch.zeros((1,5),dtype=torch.int64)),
           lambda:positive_integer(0),lambda:positive_integer(True),lambda:positive_integer(1.5),
           lambda:native(fq.Circuit(1,dtype=D),(0,),1,True),lambda:native(fq.Circuit(1,dtype=D),(0,0),1,0),
           lambda:ensemble((F(1,3),F(1,3)),2),lambda:ensemble((F(-1),F(2)),2),
           lambda:ensemble((.5,.5),2),lambda:ensemble((F(1,2),F(1,2)),13)]
    for call in calls:
        try:call()
        except ValueError:pass
        else:raise AssertionError('Invalid sample contract admitted')
    return len(calls)


def main():
    assert version('flagquantum')=='0.3.1' and version('torch').split('+')[0]=='2.13.0'
    for n in (1,2,3):
        for word in product((0,1),repeat=n):
            c=fq.Circuit(n,dtype=D)
            for q,a in enumerate(word):
                if a:c.x(q)
            p,s,counts,f=native(c,tuple(reversed(range(n))),17,29)
            assert s.tolist()==[list(reversed(word))]*17
            assert counts[int(''.join(map(str,reversed(word))),2)]==17
    print('14 basis circuits: exact labels, ordered sample columns and deterministic counts passed.')
    for theta in (0.,pi/3,-.83,pi):
        for seed in (0,11,67):
            p,s,c,f=native(fq.Circuit(1,dtype=D).ry(0,theta),(0,),37,seed)
            torch.testing.assert_close(p,torch.tensor([cos(theta/2)**2,sin(theta/2)**2],dtype=torch.float64),atol=ATOL,rtol=0,check_dtype=False)
            assert c.sum()==37 and f.sum()==1
    print('12 Bernoulli circuits: analytic Ry probabilities and finite-shot accounting passed; no frequency-equality threshold.')
    for k in (1,2,3):
        for selected in permutations(range(3),k):
            for seed in (3,17):
                p,s,c,f=native(register(),selected,41,seed)
                # Only full-register indices 1 and 4 have nonzero mass.
                ref=torch.zeros(2**k,dtype=torch.float64)
                for word,weight in [((0,0,1),.75),((1,0,0),.25)]:
                    key=0
                    for q in selected:key=2*key+word[q]
                    ref[key]+=weight
                torch.testing.assert_close(p,ref,atol=ATOL,rtol=0)
                ids,_,_=histogram(s)
                assert c.tolist()==[ids.tolist().count(j) for j in range(2**k)]
    print('30 ordered-register circuits: all 15 nonempty ordered selections at two seeds; scalar probability and independent count references passed.')
    a=native(register(),(2,0),64,101); b=native(register(),(2,0),64,101)
    assert torch.equal(a[1],b[1])
    # Different seeds need not yield different records; do not assert they must.
    for seed in range(8):native(register(-.61),(2,0),1+seed,seed)
    print('10 replay/short-record circuits: pinned-seed replay and 1-8-shot contracts passed; replay is not new statistical evidence.')
    fixtures=[((F(3,4),F(1,4)),4),((F(0),F(1)),3),((F(1),F(0)),3),
              ((F(1,6),F(1,3),F(1,2)),3),((F(0),F(1,4),F(3,4),F(0)),3)]
    for p,N in fixtures:
        rows=ensemble(p,N)
        scores=tuple(F(2*j-1) for j in range(len(p)))
        mean=sum(v*q for v,q in zip(scores,p))
        assert sum(w*sum(v*q for v,q in zip(scores,f)) for _,w,f in rows)==mean
    print('5 exact rational ensembles: normalized IID laws and all categorical/event/score estimator means passed.')
    assert invalid_checks()==14
    assert RUNS==66,RUNS
    print('14 malformed contracts rejected before native execution; empty records are not assigned a zero frequency.')
    print('66 actual CPU complex128 circuit executions; native terminal samples, not hardware shots or mid-circuit collapse.')
    print('Exact-probability atol 1e-12, rtol 0; random frequencies are observations, not exact-probability assertions.')

if __name__=='__main__':main()
