"""6.2: enumerate ideal projective branches of pure global simulated states.

Classical branch postprocessing, not a native collapse, reset or shot API.
"""
from itertools import product, permutations
from math import sqrt, pi, cos
import torch
import flagquantum as fq
try:
    from examples.foundations import projective_born as b
    from examples.foundations.circuit_rewrites import matrix
except ModuleNotFoundError:
    import projective_born as b
    from circuit_rewrites import matrix
D, ATOL = b.D, b.ATOL


def branches(state, projectors, labels):
    """Keep all labels; impossible branches are None, not a zero state."""
    probabilities = b.born(state, projectors, labels)
    states = []
    for P, p in zip(projectors, probabilities):
        w = P @ state
        if p.item() == 0:
            if bool((w != 0).any()):
                raise FloatingPointError('Nonzero projected amplitude but squared norm underflowed')
            states.append(None)
        else:
            conditional = w / torch.sqrt(p)
            if not torch.isfinite(conditional).all():
                raise FloatingPointError('Unrepresentable normalized branch')
            torch.testing.assert_close(torch.vdot(conditional,conditional),
                                       torch.ones((),dtype=D),rtol=0,atol=ATOL)
            states.append(conditional)
    return probabilities, tuple(states)


def joint(state, first, first_labels, second, second_labels):
    """Rows: first labels; columns: later labels. No evolution between them."""
    p, states = branches(state, first, first_labels)
    # Validate second family even when a particular first row is impossible.
    b.born(state, second, second_labels)
    table = torch.zeros((len(first),len(second)),dtype=torch.float64)
    for a, conditional in enumerate(states):
        if conditional is not None:
            table[a] = p[a] * b.born(conditional,second,second_labels)
    torch.testing.assert_close(table.sum(1),p,rtol=0,atol=ATOL)
    torch.testing.assert_close(table.sum(),torch.ones((),dtype=torch.float64),rtol=0,atol=ATOL)
    # Independent unnormalized ordered-product formula; no division.
    direct = torch.tensor([[torch.vdot(Q@P@state,Q@P@state).real.item()
                            for Q in second] for P in first],dtype=torch.float64)
    torch.testing.assert_close(table,direct,rtol=0,atol=ATOL)
    return table


def plus_family(n):
    """Rank-one |+...+> test and its orthogonal complement."""
    d = b.dimension(n); u = torch.ones(d,dtype=D)/sqrt(d)
    P = torch.outer(u,u.conj())
    return (P,torch.eye(d,dtype=D)-P),('all-plus','other')


def conditional_at(state, projectors, labels, label):
    if type(label) is not str or label not in labels:
        raise ValueError('Choose a declared outcome label')
    p, states = branches(state,projectors,labels)
    j = labels.index(label)
    if states[j] is None:
        raise ValueError('No conditional state for an exactly impossible outcome')
    return p[j], states[j]


def invalid_checks():
    v=torch.tensor([1,0],dtype=D);P,names=b.basis_family(1);I=torch.eye(2,dtype=D)
    cases=[lambda:branches(2*v,P,names),lambda:branches(v.real,P,names),
           lambda:branches(v[None,:],P,names),
           lambda:branches(torch.tensor([float('nan'),0],dtype=D),P,names),
           lambda:branches(v,P[:1],names[:1]),
           lambda:branches(v,(I/2,I/2),names),
           lambda:branches(v,P,('same','same')),
           lambda:conditional_at(v,P,names,'missing'),
           lambda:conditional_at(v,P,names,'1'),
           lambda:joint(v,P,names,(torch.eye(4,dtype=D),),('all',))]
    for call in cases:
        try:call()
        except ValueError:pass
        else:raise AssertionError('Malformed branch contract admitted')
    # Positive rare events are not dropped merely because p < ATOL.
    rare=torch.tensor([sqrt(1-1e-20),1e-10j],dtype=D)
    p,w=conditional_at(rare,P,names,'1')
    assert 0 < p.item() < ATOL
    torch.testing.assert_close(w,torch.tensor([0,1j],dtype=D),rtol=0,atol=ATOL)
    try:branches(torch.tensor([1,1e-200j],dtype=D),P,names)
    except FloatingPointError:pass
    else:raise AssertionError('Squared-norm underflow silently classified as impossible')
    return len(cases)


def main():
    start=b.RUNS
    for n in (1,2,3):
        factors=[b.basis_factors(bits) for bits in product((0,1),repeat=n)]+[b.complex_factors(n)]
        for fs in factors:
            v,native=b.run(fq.Circuit(n,dtype=D),fs)
            torch.testing.assert_close(v,b.product_input(fs),rtol=0,atol=ATOL)
            for family in (b.basis_family(n),b.parity_family(n)):
                P,names=family;p,ws=branches(v,P,names)
                for a,w in enumerate(ws):
                    diagonal=P[a].diagonal()
                    scalar=torch.tensor([v[j].item()*diagonal[j].item() for j in range(2**n)],dtype=D)
                    expected=sum(abs(z.item())**2 for z in scalar)
                    assert abs(p[a].item()-expected)<ATOL
                    if w is None:assert expected==0
                    else:
                        torch.testing.assert_close(w,scalar/sqrt(expected),rtol=0,atol=ATOL)
                table=joint(v,P,names,P,names)
                torch.testing.assert_close(table,torch.diag(p),rtol=0,atol=ATOL)
    print('17 basis/complex circuits: scalar-mask conditional states, zero branches and repeatability passed.')
    program=(('ry',(0,),(.41,)),('cx',(0,2),()),('p',(1,),(.37,)))
    for selected in permutations(range(3),2):
        P,names=b.marginal_family(3,selected)
        for fs in (b.basis_factors((0,0,0)),b.basis_factors((1,0,1)),b.complex_factors(3)):
            block=fq.Circuit(3,dtype=D).ry(0,.41).cx(0,2).p(1,.37)
            v,native=b.run(block,fs,selected)
            torch.testing.assert_close(v,matrix(3,program)@b.product_input(fs),rtol=0,atol=ATOL)
            p,ws=branches(v,P,names)
            torch.testing.assert_close(p,native,rtol=0,atol=ATOL)
            for a,w in enumerate(ws):
                indices=[j for j in range(8) if ''.join(format(j,'03b')[q] for q in selected)==names[a]]
                predicted=sum(abs(v[j].item())**2 for j in indices)
                assert abs(p[a].item()-predicted)<ATOL
                if w is not None:
                    for j in range(8):
                        z=v[j].item()/sqrt(predicted) if j in indices else 0
                        assert abs(w[j].item()-z)<ATOL
    print('18 ordered-support circuits: all six two-qubit selections on a correlated three-qubit register passed.')
    for phi in (0.,pi/2,pi,-.57):
        v,_=b.run(b.bell(phi),b.basis_factors((0,0)))
        P,names=b.marginal_family(2,(0,));Q,other=b.marginal_family(2,(1,))
        table=joint(v,P,names,Q,other)
        torch.testing.assert_close(table,torch.diag(torch.tensor([.5,.5],dtype=torch.float64)),rtol=0,atol=ATOL)
        torch.testing.assert_close(table.sum(0),b.born(v,Q,other),rtol=0,atol=ATOL)
        Z,zn=b.basis_family(2);XX,xn=b.xx_family()
        lost=joint(v,Z,zn,XX,xn).sum(0)
        torch.testing.assert_close(lost,torch.tensor([.5,.5],dtype=torch.float64),rtol=0,atol=ATOL)
    print('4 Bell circuits: conditional correlations, ignored local outcomes and lost phase-sensitive interference passed.')
    P,names=b.basis_family(1);Q,other=plus_family(1)
    for theta in (0.,.43,pi/2,pi):
        v,_=b.run(fq.Circuit(1,dtype=D).h(0).p(0,theta),b.basis_factors((0,)))
        table=joint(v,P,names,Q,other)
        torch.testing.assert_close(table,torch.full((2,2),.25,dtype=torch.float64),rtol=0,atol=ATOL)
        averaged=sum(p*w for p,w in zip(*branches(v,P,names)))
        assert abs(torch.vdot(averaged,averaged).real.item()-.5)<ATOL
        # Renormalizing the average restores the original coherent vector here, not the measured ensemble.
        normalized=averaged/torch.linalg.vector_norm(averaged)
        assert abs(b.born(normalized,Q,other)[0].item()-(1+cos(theta))/2)<ATOL
        if theta != pi/2:
            assert abs(b.born(normalized,Q,other)[0].item()-.5)>ATOL
    print('4 single-qubit circuits: joint tables normalize, while normalized averaged statevectors give a wrong later probability.')
    Q,qn=plus_family(2)
    for phi in (0.,.63,pi):
        v,_=b.run(b.bell(phi),b.basis_factors((0,0)))
        coarse,cn=b.parity_family(2);fine,fn=b.basis_family(2)
        a=joint(v,coarse,cn,Q,qn).sum(0)
        c=joint(v,fine,fn,Q,qn).sum(0)
        torch.testing.assert_close(a,b.born(v,Q,qn),rtol=0,atol=ATOL)
        torch.testing.assert_close(c,torch.tensor([.25,.75],dtype=torch.float64),rtol=0,atol=ATOL)
        assert abs(a[0].item()-(1+cos(phi))/4)<ATOL
    print('3 coarse/fine circuits: parity-only projection preserves within-event coherence; forgetting a fine record does not.')
    assert invalid_checks()==10
    assert b.RUNS-start==46,b.RUNS-start
    print('10 invalid contracts rejected; positive 1e-20 branch retained; squared-norm underflow explicitly rejected.')
    print('46 actual CPU complex128 preparation circuits; conditional branches and later probabilities are classical postprocessing, not native collapse or shots.')
    print('Implementation atol 1e-12, rtol 0; no vector averaging, phase alignment or input normalization repair; density-operator update deferred to Chapter 8.')


if __name__=='__main__':main()
