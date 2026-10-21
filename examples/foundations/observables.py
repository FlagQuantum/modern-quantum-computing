"""6.3: native Pauli expectations versus spectral probabilities and dense quadratic forms."""
from math import isfinite, sqrt, sin, cos, pi
from itertools import product
import torch
import flagquantum as fq
try:
    from examples.foundations import projective_born as b
    from examples.foundations.circuit_rewrites import matrix
except ModuleNotFoundError:
    import projective_born as b
    from circuit_rewrites import matrix
D,ATOL=b.D,b.ATOL
I=torch.eye(2,dtype=D)
X=torch.tensor([[0,1],[1,0]],dtype=D)
Y=torch.tensor([[0,-1j],[1j,0]],dtype=D)
Z=torch.diag(torch.tensor([1,-1],dtype=D))
H=.7*X-.2*Y+1.3*Z
RUNS=0


def hermitian(A):
    if not isinstance(A,torch.Tensor) or A.ndim!=2 or A.shape[0]!=A.shape[1] or A.shape[0] not in (2,4,8,16) or A.dtype!=D or A.device.type!='cpu' or not torch.isfinite(A).all():
        raise ValueError('Finite square CPU complex128 matrix on 1-4 qubits required')
    if not torch.allclose(A,A.mH,atol=ATOL,rtol=0):
        raise ValueError('Hermitian observable required; no symmetrization repair')
    return A


def dense_mean(state,A):
    hermitian(A)
    b.born(state,(torch.eye(A.shape[0],dtype=D),),('all',))
    value=torch.vdot(state,A@state)
    if abs(value.imag.item())>ATOL:
        raise ArithmeticError('Unexpected imaginary expectation residual')
    return value.real


def spectral_mean(state,values,projectors,labels):
    if not isinstance(values,tuple) or len(values)!=len(projectors) or any(type(x) not in (int,float) or not isfinite(x) for x in values):
        raise ValueError('One finite real eigenvalue per projector required')
    probabilities=b.born(state,projectors,labels)
    A=sum((value*P for value,P in zip(values,projectors)),torch.zeros_like(projectors[0]))
    result=sum(value*p for value,p in zip(values,probabilities))
    torch.testing.assert_close(result,dense_mean(state,A),rtol=0,atol=ATOL)
    low,high=min(values),max(values)
    assert low-ATOL <= result.item() <= high+ATOL
    return result,probabilities


def numerical_spectrum(A):
    """Rank-one numerical refinement; no near-degenerate eigenvalue clustering."""
    hermitian(A)
    values,V=torch.linalg.eigh(A)
    projectors=tuple(torch.outer(V[:,j],V[:,j].conj()) for j in range(A.shape[0]))
    labels=tuple('column-'+str(j) for j in range(A.shape[0]))
    reconstructed=sum((value*P for value,P in zip(values,projectors)),torch.zeros_like(A))
    torch.testing.assert_close(reconstructed,A,rtol=0,atol=ATOL)
    return tuple(values.tolist()),projectors,labels


def query(block,factors,observables):
    global RUNS
    n=block.n_qubits;b.dimension(n)
    if not isinstance(observables,dict) or not observables:
        raise ValueError('Declare named native observables')
    circuit=fq.Circuit(n,dtype=D)
    for q,factor in enumerate(factors):
        circuit.unitary(q,unitary=b.prepare_matrix(torch.tensor(factor,dtype=D)))
    circuit.compose(block)
    requests=[fq.probabilities()]+[fq.expectation(op,name=name) for name,op in observables.items()]
    result=fq.run(circuit,outputs=requests,options=b.OPTIONS)
    state,prob=result.statevector(),result.probabilities
    assert state.shape==(1,2**n) and prob.shape==(1,2**n)
    assert state.dtype==D and prob.dtype==torch.float64
    values={}
    for name in observables:
        raw=result.expectation(name)
        assert raw.shape==(1,) and raw.dtype==torch.float64 and torch.isfinite(raw).all()
        values[name]=raw[0]
    RUNS+=1
    return state[0],prob[0],values


def invalid_checks():
    v=torch.tensor([1,0],dtype=D);P,names=b.basis_family(1)
    cases=[lambda:hermitian(torch.tensor([[0,1],[0,0]],dtype=D)),
           lambda:hermitian(X.real),lambda:hermitian(torch.eye(3,dtype=D)),
           lambda:hermitian(torch.tensor([[float('nan'),0],[0,1]],dtype=D)),
           lambda:dense_mean(2*v,Z),lambda:dense_mean(v[None,:],Z),
           lambda:spectral_mean(v,(1,),P,names),
           lambda:spectral_mean(v,(1j,-1),P,names),
           lambda:spectral_mean(v,(True,-1),P,names),
           lambda:spectral_mean(v,(float('inf'),-1),P,names)]
    for call in cases:
        try:call()
        except ValueError:pass
        else:raise AssertionError('Malformed observable contract admitted')
    return len(cases)


def main():
    start=RUNS
    nativeH=.7*fq.X(0)-.2*fq.Y(0)+1.3*fq.Z(0)
    for theta in (0.,pi/2,pi,-.37,.61):
        for phi in (0.,.43,-1.17):
            v,p,means=query(fq.Circuit(1,dtype=D).ry(0,theta).p(0,phi),b.basis_factors((0,)),
                            {'x':fq.X(0),'y':fq.Y(0),'z':fq.Z(0),'h':nativeH})
            expected=torch.tensor([cos(theta/2),complex(cos(phi),sin(phi))*sin(theta/2)],dtype=D)
            torch.testing.assert_close(v,expected,rtol=0,atol=ATOL)
            for name,reference in [('x',sin(theta)*cos(phi)),('y',sin(theta)*sin(phi)),('z',cos(theta))]:
                assert abs(means[name].item()-reference)<ATOL
            r=sqrt(.7**2+.2**2+1.3**2)
            family=((I-H/r)/2,(I+H/r)/2)
            spectral,_=spectral_mean(v,(-r,r),family,('minus','plus'))
            torch.testing.assert_close(means['h'],spectral,rtol=0,atol=ATOL)
            torch.testing.assert_close(means['h'],dense_mean(v,H),rtol=0,atol=ATOL)
            torch.testing.assert_close(means['z'],p[0]-p[1],rtol=0,atol=ATOL)
    print('15 single-qubit circuits: X/Y/Z signs, closed amplitudes and native/analytic-spectral/dense H expectations passed.')
    ZZ=torch.kron(Z,Z);XX=torch.kron(X,X);YY=torch.kron(Y,Y)
    A=.7*ZZ+.2*XX-.3*torch.kron(Y,I)
    spectral=numerical_spectrum(A)
    nativeA=.7*(fq.Z(0)@fq.Z(1))+.2*(fq.X(0)@fq.X(1))-.3*fq.Y(0)
    families=[b.basis_factors(bits) for bits in product((0,1),repeat=2)]+[b.complex_factors(2)]
    # Five inputs at each of three phase values, plus two independent basis cases.
    cases=[(fs,phi) for phi in (0.,.41,-.73) for fs in families]+[(b.basis_factors((0,0)),pi),(b.basis_factors((1,1)),pi/2)]
    for fs,phi in cases:
        v,p,m=query(fq.Circuit(2,dtype=D).h(0).cx(0,1).p(0,phi),fs,
                    {'z0':fq.Z(0),'z1':fq.Z(1),'zz':fq.Z(0)@fq.Z(1),'xx':fq.X(0)@fq.X(1),'yy':fq.Y(0)@fq.Y(1),'a':nativeA})
        program=(('h',(0,),()),('cx',(0,1),()),('p',(0,),(phi,)))
        torch.testing.assert_close(v,matrix(2,program)@b.product_input(fs),rtol=0,atol=ATOL)
        for name,M in [('zz',ZZ),('xx',XX),('yy',YY),('a',A)]:
            torch.testing.assert_close(m[name],dense_mean(v,M),rtol=0,atol=ATOL)
        value,_=spectral_mean(v,*spectral)
        torch.testing.assert_close(value,m['a'],rtol=0,atol=ATOL)
        even,labels=b.parity_family(2)
        z,_=spectral_mean(v,(1,-1),even,labels)
        torch.testing.assert_close(z,m['zz'],rtol=0,atol=ATOL)
        assert abs(m['zz'].item()-sum(((-1)**j.bit_count())*p[j].item() for j in range(4)))<ATOL
    print('17 two-qubit circuits: degenerate ZZ projectors, parity signs, XX/YY correlations and native/numerical-spectral/dense sums passed.')
    A3=.6*torch.kron(torch.kron(X,I),Y)-.4*torch.kron(torch.kron(I,Z),I)
    native3=.6*(fq.Y(2)@fq.X(0))-.4*fq.Z(1)
    for fs in [b.basis_factors(bits) for bits in product((0,1),repeat=3)]+[b.complex_factors(3)]:
        v,p,m=query(fq.Circuit(3,dtype=D).ry(1,.27).cx(2,0).p(2,-.52),fs,{'a3':native3})
        program=(('ry',(1,),(.27,)),('cx',(2,0),()),('p',(2,),(-.52,)))
        torch.testing.assert_close(v,matrix(3,program)@b.product_input(fs),rtol=0,atol=ATOL)
        mean,_=spectral_mean(v,*numerical_spectrum(A3))
        torch.testing.assert_close(m['a3'],mean,rtol=0,atol=ATOL)
    print('9 three-qubit circuits: reversed nonadjacent Pauli supports, independently indexed states and dense spectral means passed.')
    assert invalid_checks()==10
    assert RUNS-start==41,RUNS-start
    print('10 malformed observable/state/eigenvalue contracts rejected; no Hermitian or state normalization repair.')
    print('41 actual CPU complex128 circuits; native exact expectations, not single-shot outcomes, a hardware measurement protocol or an interval certificate.')


if __name__=='__main__':main()
