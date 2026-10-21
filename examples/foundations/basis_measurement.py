"""6.4: actual basis-rotation circuits and native computational readout."""
from itertools import product,permutations
from math import sqrt,pi,isfinite
import cmath,torch
import flagquantum as fq
try:
    from examples.foundations import projective_born as b
    from examples.foundations.circuit_rewrites import matrix
    from examples.foundations.observables import X,Y,Z
except ModuleNotFoundError:
    import projective_born as b
    from circuit_rewrites import matrix
    from observables import X,Y,Z
D,ATOL=b.D,b.ATOL
H=torch.tensor([[1,1],[1,-1]],dtype=D)/sqrt(2)
S=torch.diag(torch.tensor([1,1j],dtype=D))
I=torch.eye(2,dtype=D)


def basis_family(B,labels):
    if not isinstance(B,torch.Tensor) or B.ndim!=2 or B.shape[0]!=B.shape[1] or B.shape[0] not in (2,4,8,16) or B.dtype!=D or B.device.type!='cpu' or not torch.isfinite(B).all():
        raise ValueError('Finite square CPU complex128 basis on 1-4 qubits required')
    eye=torch.eye(B.shape[0],dtype=D)
    if not torch.allclose(B.mH@B,eye,rtol=0,atol=ATOL) or not torch.allclose(B@B.mH,eye,rtol=0,atol=ATOL):
        raise ValueError('Unitary basis required; no QR repair')
    if not isinstance(labels,tuple) or len(labels)!=B.shape[0] or any(type(s) is not str or not s for s in labels) or len(set(labels))!=len(labels):
        raise ValueError('One distinct declared label per basis column required')
    return tuple(torch.outer(B[:,j],B[:,j].conj()) for j in range(B.shape[0]))


def tilted(theta,phi):
    if any(type(t) not in (int,float) or not isfinite(t) or abs(t)>100 for t in (theta,phi)):
        raise ValueError('Finite literal radian angles with magnitude <=100 required')
    # Indexed gate reference: chronological Ry(theta), Rz(phi), matrix Rz(phi) Ry(theta).
    return matrix(1,(('ry',(0,),(theta,)),('rz',(0,),(phi,))))


def full_check(initial,B,labels,after,p):
    P=basis_family(B,labels)
    torch.testing.assert_close(after,B.mH@initial,rtol=0,atol=ATOL)
    predicted=b.born(initial,P,labels)
    torch.testing.assert_close(p,predicted,rtol=0,atol=ATOL)
    scalar=torch.tensor([abs(sum(B[k,j].conj().item()*initial[k].item() for k in range(B.shape[0])))**2
                         for j in range(B.shape[0])],dtype=torch.float64)
    torch.testing.assert_close(p,scalar,rtol=0,atol=ATOL)
    return predicted


def inputs():
    return [(1,0),(0,1),(1/sqrt(2),1/sqrt(2)),(1/sqrt(2),-1/sqrt(2)),
            (1/sqrt(2),1j/sqrt(2)),(1/sqrt(2),-1j/sqrt(2)),(.6,.8j)]


def invalid_checks():
    labels=('plus','minus');bad=torch.tensor([[1,1],[0,1]],dtype=D)
    cases=[lambda:basis_family(bad,labels),lambda:basis_family(H.real,labels),
           lambda:basis_family(H[0],labels),lambda:basis_family(torch.eye(3,dtype=D),('a','b','c')),
           lambda:basis_family(torch.tensor([[float('nan'),0],[0,1]],dtype=D),labels),
           lambda:basis_family(H,('same','same')),lambda:basis_family(H,('one',)),
           lambda:tilted('degrees',.2),lambda:tilted(True,.2),lambda:tilted(float('inf'),0)]
    for call in cases:
        try:call()
        except ValueError:pass
        else:raise AssertionError('Malformed basis contract admitted')
    return len(cases)


def main():
    start=b.RUNS;labels=('plus','minus')
    specs=[(H,fq.Circuit(1,dtype=D).h(0),X),
           (S@H,fq.Circuit(1,dtype=D).p(0,-pi/2).h(0),Y),
           (tilted(.71,.43),fq.Circuit(1,dtype=D).rz(0,-.43).ry(0,-.71),None)]
    for B,readout,A in specs:
        for factor in inputs():
            initial=torch.tensor(factor,dtype=D)
            after,p=b.run(readout,[factor])
            full_check(initial,B,labels,after,p)
            if A is not None:
                assert abs((p[0]-p[1]).item()-torch.vdot(initial,A@initial).real.item())<ATOL
    print('21 single-qubit circuits: X, Y and complex tilted bases; full rotated vectors, overlap probabilities and Pauli signs passed.')
    prep=(('ry',(0,),(.29,)),('cx',(0,2),()),('p',(1,),(-.31,)))
    for selected in permutations(range(3),2):
        q,r=selected
        read=(('p',(q,),(-pi/2,)),('h',(q,),()),('h',(r,),()))
        R=matrix(3,read);P0,names=b.marginal_family(3,selected)
        P=tuple(R.mH@Q@R for Q in P0)
        for fs in (b.basis_factors((0,0,0)),b.basis_factors((1,0,1)),b.complex_factors(3)):
            initial=matrix(3,prep)@b.product_input(fs)
            block=fq.Circuit(3,dtype=D).ry(0,.29).cx(0,2).p(1,-.31).p(q,-pi/2).h(q).h(r)
            after,p=b.run(block,fs,selected)
            torch.testing.assert_close(after,R@initial,rtol=0,atol=ATOL)
            torch.testing.assert_close(p,b.born(initial,P,names),rtol=0,atol=ATOL)
            scalar=torch.zeros(4,dtype=torch.float64)
            for j,z in enumerate(R@initial):
                key=int(''.join(format(j,'03b')[k] for k in selected),2);scalar[key]+=abs(z)**2
            torch.testing.assert_close(p,scalar,rtol=0,atol=ATOL)
    print('18 correlated-register circuits: all six ordered two-qubit selections with local Y/X rotations and native partial readout passed.')
    B=matrix(2,(('h',(0,),()),('cx',(0,1),())))
    bell_labels=('Phi+','Psi+','Phi-','Psi-')
    for fs in [b.basis_factors(bits) for bits in product((0,1),repeat=2)]+[b.complex_factors(2)]:
        initial=B@b.product_input(fs)
        after,p=b.run(fq.Circuit(2,dtype=D).h(0).cx(0,1).cx(0,1).h(0),fs)
        full_check(initial,B,bell_labels,after,p)
        torch.testing.assert_close(p,b.product_input(fs).abs().square(),rtol=0,atol=ATOL)
    print('5 Bell-basis circuits: entangling preparation, inverse analyzer and 00/01/10/11 labels Phi+/Psi+/Phi-/Psi- passed.')
    B=tilted(.71,.43)
    for Bnew in (B@torch.diag(torch.tensor([cmath.exp(.2j),cmath.exp(-.8j)],dtype=D)),
                 B[:,[1,0]]):
        for factor in (inputs()[0],inputs()[4],inputs()[6]):
            after,p=b.run(fq.Circuit(1,dtype=D).unitary(0,unitary=Bnew.mH.contiguous()),[factor])
            full_check(torch.tensor(factor,dtype=D),Bnew,labels,after,p)
    print('6 phase/relabel circuits: independent column phases preserve probabilities; column permutation follows declared labels.')
    # Deliberately wrong analyzers, checked against their actual submitted matrices.
    initial=B[:,0]
    factor=tuple(initial.tolist())
    after,p=b.run(fq.Circuit(1,dtype=D).unitary(0,unitary=B),[factor])
    torch.testing.assert_close(after,B@initial,rtol=0,atol=ATOL)
    assert p[1].item()>.1
    after,p=b.run(fq.Circuit(1,dtype=D).rz(0,-.43).ry(0,-.71),[factor])
    full_check(initial,B,labels,after,p);assert abs(p[0].item()-1)<ATOL
    for factor in (inputs()[4],inputs()[5]):
        after,p=b.run(fq.Circuit(1,dtype=D).p(0,pi/2).h(0),[factor])
        expected=torch.tensor([0.,1.] if factor==inputs()[4] else [1.,0.],dtype=torch.float64)
        torch.testing.assert_close(p,expected,rtol=0,atol=ATOL)
    print('4 diagnostic circuits: forward B is not its inverse analyzer; wrong Y phase swaps plus/minus labels, without correcting submitted results.')
    assert invalid_checks()==10
    assert b.RUNS-start==54,b.RUNS-start
    print('10 malformed basis/angle/label contracts rejected; radian inputs, exact labels and full-vector phases retained.')
    print('54 actual CPU complex128 circuits; native post-rotation exact probabilities, not shots, hardware calibration or a post-measurement statevector.')


if __name__=='__main__':main()
