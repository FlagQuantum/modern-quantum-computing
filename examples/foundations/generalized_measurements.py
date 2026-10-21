"""6.5: pure-input POVMs/instruments; native weak-measurement premeasurement circuit.

No nonunitary measurement operator is submitted as a unitary gate.
"""
from math import sqrt,acos,pi,isfinite
import cmath,torch
import flagquantum as fq
try:
    from examples.foundations import projective_born as b
    from examples.foundations.basis_measurement import inputs
except ModuleNotFoundError:
    import projective_born as b
    from basis_measurement import inputs
D,ATOL=b.D,b.ATOL
I=torch.eye(2,dtype=D)
X=torch.tensor([[0,1],[1,0]],dtype=D)
Z=torch.diag(torch.tensor([1,-1],dtype=D))


def labels_check(labels,count):
    if not isinstance(labels,tuple) or len(labels)!=count or any(type(s) is not str or not s for s in labels) or len(set(labels))!=count:
        raise ValueError('Declare a distinct string label per outcome')


def matrix_check(A,d):
    if not isinstance(A,torch.Tensor) or A.shape!=(d,d) or A.dtype!=D or A.device.type!='cpu' or not torch.isfinite(A).all():
        raise ValueError('Finite square CPU complex128 operator matching the state required')


def povm(state,effects,labels):
    # Reuse the normalized pure-input contract, not the projective-family contract.
    if not isinstance(state,torch.Tensor) or state.ndim!=1:
        raise ValueError('Unbatched normalized pure global state required')
    d=state.numel()
    b.born(state,(torch.eye(d,dtype=D),),('all',))
    if not isinstance(effects,tuple) or not effects:
        raise ValueError('Nonempty effect tuple required')
    labels_check(labels,len(effects));eye=torch.eye(d,dtype=D)
    for E in effects:
        matrix_check(E,d)
        if not torch.allclose(E,E.mH,rtol=0,atol=ATOL) or torch.linalg.eigvalsh(E).min().item() < -ATOL:
            raise ValueError('Hermitian positive effects required')
    if not torch.allclose(sum(effects,torch.zeros_like(eye)),eye,rtol=0,atol=ATOL):
        raise ValueError('Effects must sum to identity')
    probabilities=[]
    for E in effects:
        value=torch.vdot(state,E@state)
        if abs(value.imag.item())>ATOL or value.real.item()<0:
            raise ArithmeticError('Non-real/negative probability; no clipping repair')
        probabilities.append(value.real)
    result=torch.stack(probabilities)
    assert abs(result.sum().item()-1)<ATOL
    return result


def instrument(state,groups,labels):
    """Return coarse probabilities and ALL fine probabilities/pure states.

    groups[a][k] is K_{a,k}; no single coarse statevector is invented.
    """
    if not isinstance(groups,tuple) or not groups or any(not isinstance(g,tuple) or not g for g in groups):
        raise ValueError('Nonempty outcome groups of measurement operators required')
    if not isinstance(state,torch.Tensor) or state.ndim!=1:
        raise ValueError('Unbatched pure input required')
    d=state.numel();labels_check(labels,len(groups))
    for group in groups:
        for K in group:matrix_check(K,d)
    effects=tuple(sum((K.mH@K for K in group),torch.zeros((d,d),dtype=D)) for group in groups)
    probabilities=povm(state,effects,labels)
    records=[]
    for group in groups:
        fine=[]
        for K in group:
            w=K@state;p=torch.vdot(w,w).real
            if p.item()==0:
                if bool((w!=0).any()):raise FloatingPointError('Nonzero branch with squared-norm underflow')
                normalized=None
            else:
                normalized=w/torch.sqrt(p)
                torch.testing.assert_close(torch.vdot(normalized,normalized),torch.ones((),dtype=D),rtol=0,atol=ATOL)
            fine.append((p,normalized))
        records.append(tuple(fine))
    sums=torch.stack([sum(p for p,w in row) for row in records])
    torch.testing.assert_close(sums,probabilities,rtol=0,atol=ATOL)
    return probabilities,tuple(records)


def later(state,groups,labels,projectors,names):
    """Joint coarse label and later projective event; no intervening evolution."""
    probabilities,records=instrument(state,groups,labels)
    b.born(state,projectors,names)
    table=torch.zeros((len(groups),len(projectors)),dtype=torch.float64)
    for a,row in enumerate(records):
        for p,w in row:
            if w is not None:table[a]+=p*b.born(w,projectors,names)
    torch.testing.assert_close(table.sum(1),probabilities,rtol=0,atol=ATOL)
    direct=torch.tensor([[sum(torch.vdot(Q@K@state,Q@K@state).real.item() for K in group)
                          for Q in projectors] for group in groups],dtype=torch.float64)
    torch.testing.assert_close(table,direct,rtol=0,atol=ATOL)
    return table


def weak(kappa,flip=False):
    if type(kappa) not in (int,float) or not isfinite(kappa) or not 0<=kappa<=1 or type(flip) is not bool:
        raise ValueError('Finite dimensionless strength 0<=kappa<=1 and Boolean flip required')
    a,beta=sqrt((1+kappa)/2),sqrt((1-kappa)/2)
    M0=torch.diag(torch.tensor([a,beta],dtype=D))
    M1=torch.diag(torch.tensor([beta,a],dtype=D))
    return ((M0,),((X@M1) if flip else M1,))


def weak_circuit(kappa,flip=False):
    weak(kappa,flip)
    a,beta=sqrt((1+kappa)/2),sqrt((1-kappa)/2)
    gamma0,gamma1=2*acos(a),2*acos(beta)
    circuit=fq.Circuit(2,dtype=D).ry(1,gamma0).cry(0,1,gamma1-gamma0)
    if flip:circuit.cx(1,0)
    return circuit


def native_weak(state,kappa,flip=False):
    """System q0, meter q1 initially zero; joint vector is NOT collapsed."""
    groups=weak(kappa,flip);names=('meter-0','meter-1')
    p,records=instrument(state,groups,names)
    v,native=b.run(weak_circuit(kappa,flip),[tuple(state.tolist()),(1,0)],(1,))
    expected=torch.zeros(4,dtype=D)
    for a,group in enumerate(groups):
        w=group[0]@state
        expected[a::2]=w
        torch.testing.assert_close(v[a::2],w,rtol=0,atol=ATOL)
        if p[a].item()>0:
            torch.testing.assert_close(v[a::2]/torch.sqrt(p[a]),records[a][0][1],rtol=0,atol=ATOL)
    torch.testing.assert_close(v,expected,rtol=0,atol=ATOL)
    torch.testing.assert_close(native,p,rtol=0,atol=ATOL)
    return v,native


def trine():
    states=tuple(torch.tensor([1,cmath.exp(2j*pi*j/3)],dtype=D)/sqrt(2) for j in range(3))
    groups=tuple((sqrt(2/3)*torch.outer(t,t.conj()),) for t in states)
    effects=tuple(group[0].mH@group[0] for group in groups)
    return states,groups,effects


def invalid_checks():
    v=torch.tensor([1,0],dtype=D);P0=torch.diag(torch.tensor([1,0],dtype=D))
    cases=[lambda:povm(2*v,(I,),('all',)),lambda:povm(v,(P0,),('only',)),
           lambda:povm(v,(torch.diag(torch.tensor([-.2,.5],dtype=D)),torch.diag(torch.tensor([1.2,.5],dtype=D))),('a','b')),
           lambda:povm(v,(torch.tensor([[1,1],[0,1]],dtype=D),),('all',)),
           lambda:povm(v,(I,),('a','b')),lambda:instrument(v,((I/2,),),('all',)),
           lambda:instrument(v,((torch.eye(4,dtype=D),),),('all',)),
           lambda:instrument(v,((I,),()),('a','b')),
           lambda:weak(1.1),lambda:weak(.3,'conditional')]
    for call in cases:
        try:call()
        except ValueError:pass
        else:raise AssertionError('Malformed POVM/instrument contract admitted')
    return len(cases)


def main():
    start=b.RUNS
    for kappa in (0.,.35,1.):
        for factor in inputs():
            state=torch.tensor(factor,dtype=D)
            prior=None
            for flip in (False,True):
                v,p=native_weak(state,kappa,flip)
                formula=torch.tensor([(1+kappa*(abs(factor[0])**2-abs(factor[1])**2))/2,
                                      (1-kappa*(abs(factor[0])**2-abs(factor[1])**2))/2],dtype=torch.float64)
                torch.testing.assert_close(p,formula,rtol=0,atol=ATOL)
                if prior is not None:torch.testing.assert_close(p,prior,rtol=0,atol=ATOL)
                prior=p
    print('42 two-qubit weak-instrument circuits: three strengths including 0/1, seven inputs and two updates with identical meter probabilities passed.')
    ts,groups,effects=trine();names=('t0','t1','t2')
    for factor in inputs():
        v,native=b.run(fq.Circuit(1,dtype=D),[factor])
        torch.testing.assert_close(v,torch.tensor(factor,dtype=D),rtol=0,atol=ATOL)
        p,records=instrument(v,groups,names)
        formula=torch.tensor([abs(factor[0]+cmath.exp(-2j*pi*j/3)*factor[1])**2/3 for j in range(3)],dtype=torch.float64)
        torch.testing.assert_close(p,formula,rtol=0,atol=ATOL)
        torch.testing.assert_close(p,povm(v,effects,names),rtol=0,atol=ATOL)
    print('7 native single-qubit preparations: genuine three-outcome trine effects and pure measurement-operator branches checked classically against scalar formulas.')
    plus=torch.tensor([1,1],dtype=D)/sqrt(2)
    ZP,zn=b.basis_family(1);Pplus=torch.outer(plus,plus.conj());Q=(Pplus,I-Pplus);qn=('plus','minus')
    identity=((I,),);dephase=((ZP[0],ZP[1]),);mixed_rep=((I/sqrt(2),Z/sqrt(2)),)
    for state in (plus,torch.tensor([.6,.8j],dtype=D)):
        torch.testing.assert_close(later(state,dephase,('kept',),Q,qn),
                                   later(state,mixed_rep,('kept',),Q,qn),rtol=0,atol=ATOL)
    for entangle in (False,True):
        block=fq.Circuit(2,dtype=D).h(0)
        if entangle:block.cx(0,1)
        block.h(0)
        v,p=b.run(block,b.basis_factors((0,0)),(0,))
        reference=later(plus,dephase if entangle else identity,('kept',),Q,qn).sum(0)
        torch.testing.assert_close(p,reference,rtol=0,atol=ATOL)
    print('2 native joint-system readouts: one coarse effect I can preserve or destroy later interference; hidden-operator unitary mixing preserves the instrument predictions.')
    # Edge branch rules: impossible != rare positive != squared-norm underflow.
    state=torch.tensor([1,0],dtype=D);p,rows=instrument(state,weak(1.),('0','1'))
    assert rows[1][0][1] is None and p[1].item()==0
    rare=torch.tensor([1,1e-10j],dtype=D)
    p,rows=instrument(rare,weak(1.),('0','1'))
    assert 0<p[1].item()<ATOL
    torch.testing.assert_close(rows[1][0][1],torch.tensor([0,1j],dtype=D),rtol=0,atol=ATOL)
    try:instrument(torch.tensor([1,1e-200j],dtype=D),weak(1.),('0','1'))
    except FloatingPointError:pass
    else:raise AssertionError('Squared-norm underflow silently accepted')
    assert invalid_checks()==10
    assert b.RUNS-start==51,b.RUNS-start
    print('10 malformed contracts rejected; impossible/positive rare/underflow branches distinguished without clipping or vector averaging.')
    print('51 actual CPU complex128 circuits; native unitary dilation/readout plus explicitly labelled classical branch analysis, not a dedicated POVM/instrument or sampled-collapse API.')


if __name__=='__main__':main()
