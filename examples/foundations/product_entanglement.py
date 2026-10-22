"""7.1 Pure-state products: native preparation and explicit coefficient analysis.

The theorem is exact. Numeric residuals are diagnostics, not rank certificates.
"""
import math
import cmath
from itertools import permutations, product
from importlib.metadata import version
import torch
import flagquantum as fq
try:
    from examples.foundations.tensor_spaces import OPTIONS
except ModuleNotFoundError:
    from tensor_spaces import OPTIONS
D = torch.complex128
ATOL = 1e-12
RUNS = 0


def coefficients(state, left, right):
    """Gather C[i,j] in explicitly ordered, complementary qubit bases."""
    if not isinstance(state, torch.Tensor) or state.dtype != D or state.device.type != 'cpu' or state.ndim != 1 or state.numel() not in (4,8,16) or not bool(torch.isfinite(state).all()):
        raise ValueError('Finite unbatched CPU complex128 vector of 2-4 qubits required')
    if abs(torch.vdot(state,state).item()-1) > ATOL:
        raise ValueError('Normalized pure vector required; no repair')
    n = state.numel().bit_length()-1
    if any(not isinstance(side,tuple) or not side or any(type(q) is not int for q in side) for side in (left,right)) or sorted(left+right) != list(range(n)):
        raise ValueError('Declare nonempty ordered complementary qubit tuples')
    C = torch.empty((2**len(left),2**len(right)),dtype=D)
    for i in range(C.shape[0]):
        for j in range(C.shape[1]):
            bits = ['0']*n
            for q,bit in zip(left,format(i,f'0{len(left)}b')): bits[q]=bit
            for q,bit in zip(right,format(j,f'0{len(right)}b')): bits[q]=bit
            C[i,j] = state[int(''.join(bits),2)]
    return C


def validate_matrix(C):
    if not isinstance(C,torch.Tensor) or C.ndim != 2 or min(C.shape)<1 or max(C.shape)>16 or C.dtype != D or C.device.type != 'cpu' or not bool(torch.isfinite(C).all()):
        raise ValueError('Finite nonempty CPU complex128 coefficient matrix required')
    if abs(torch.sum(C.abs()**2).item()-1)>ATOL:
        raise ValueError('Unit Frobenius norm required; no repair')


def minors(C):
    validate_matrix(C)
    return [C[i,j]*C[k,l]-C[i,l]*C[k,j]
            for i in range(C.shape[0]) for k in range(i+1,C.shape[0])
            for j in range(C.shape[1]) for l in range(j+1,C.shape[1])]


def pivot_factors(C):
    """Candidate from a largest entry; return measured reconstruction residual.

    The left factor has unit norm; the right factor is retained without repair.
    Their outer product need not equal C.
    They are candidate diagnostics, never an automatic exact-product verdict.
    """
    validate_matrix(C)
    flat = int(torch.argmax(C.abs()).item()); r,s = divmod(flat,C.shape[1])
    a = C[:,s].clone(); b = C[r,:]/C[r,s]
    scale = torch.linalg.vector_norm(a)
    a = a/scale; b = b*scale
    # Exact rank-one normalized C gives ||b||=1. For other inputs preserve b,
    # so the residual tests the actual pivot formula rather than a repaired fit.
    residual = float(torch.linalg.vector_norm(C-torch.outer(a,b)))
    return a,b,residual


def query(circuit):
    global RUNS
    result = fq.run(circuit,outputs=[fq.probabilities()],options=OPTIONS)
    raw,p = result.statevector(),result.probabilities
    assert raw.shape == (1,2**circuit.n_qubits) and p.shape == raw.shape
    assert raw.dtype==D and p.dtype==torch.float64
    RUNS += 1
    assert torch.allclose(p[0],raw[0].abs()**2,atol=ATOL,rtol=0)
    return raw[0],p[0]


def scalar_product(factors):
    return torch.tensor([math.prod(factors[q][int(bits[q])] for q in range(len(factors)))
                         for bits in product('01',repeat=len(factors))],dtype=D)


def cuts(n):
    return [(order[:k],order[k:]) for order in permutations(range(n)) for k in range(1,n)]


def main():
    assert version('flagquantum')=='0.3.1'
    assert version('torch').split('+')[0]=='2.13.0'
    # Each native state is checked across every ordered bipartition.
    for n in (2,3):
        for index in range(2**n):
            circuit=fq.Circuit(n,dtype=D)
            for q,bit in enumerate(format(index,f'0{n}b')):
                if bit=='1': circuit.x(q)
            state,_=query(circuit)
            expected=torch.zeros(2**n,dtype=D); expected[index]=1
            assert torch.equal(state,expected)
            for A,B in cuts(n):
                C=coefficients(state,A,B); a,b,e=pivot_factors(C)
                assert e==0 and all(m==0 for m in minors(C))
    print('12 native basis states: all ordered bipartitions passed.')
    for n in (2,3):
        for t in range(6):
            circuit=fq.Circuit(n,dtype=D); factors=[]
            for q in range(n):
                theta=.19+.21*t+.13*q; phi=-.73+.17*t-.31*q
                circuit.ry(q,theta).p(q,phi)
                factors.append((math.cos(theta/2),cmath.exp(1j*phi)*math.sin(theta/2)))
            state,_=query(circuit)
            assert torch.allclose(state,scalar_product(factors),atol=ATOL,rtol=0)
            for A,B in cuts(n):
                C=coefficients(state,A,B); a,b,e=pivot_factors(C)
                assert e<ATOL and max(abs(m) for m in minors(C))<ATOL
                assert abs(torch.linalg.vector_norm(b).item()-1)<ATOL
    print('12 complex product preparations: scalar factors and pivot reconstructions passed.')
    for theta in (.31,math.pi/2,2.2):
        for phi in (0.,.71,-1.2):
            state,_=query(fq.Circuit(2,dtype=D).ry(0,theta).cx(0,1).p(0,phi))
            c,s=math.cos(theta/2),math.sin(theta/2)*cmath.exp(1j*phi)
            expected=torch.tensor([c,0,0,s],dtype=D)
            assert torch.allclose(state,expected,atol=ATOL,rtol=0)
            C=coefficients(state,(0,),(1,))
            assert abs(minors(C)[0].item()-c*s)<ATOL
            assert abs(minors(C)[0])>.1
    print('9 entangled pair preparations: closed complex determinant passed.')
    for phi in (0.,.43,-.91):
        theta=.82
        state,_=query(fq.Circuit(3,dtype=D).h(0).cx(0,2).p(0,phi).ry(1,theta))
        expected=torch.tensor([math.cos(theta/2)/math.sqrt(2),0,math.sin(theta/2)/math.sqrt(2),0,
            0,cmath.exp(1j*phi)*math.cos(theta/2)/math.sqrt(2),0,cmath.exp(1j*phi)*math.sin(theta/2)/math.sqrt(2)],dtype=D)
        assert torch.allclose(state,expected,atol=ATOL,rtol=0)
        separated=coefficients(state,(2,0),(1,))
        splitpair=coefficients(state,(0,),(1,2))
        assert pivot_factors(separated)[2]<ATOL
        assert max(abs(m) for m in minors(splitpair))>.1
    print('3 nonadjacent-register preparations: product across one cut, entangled across another.')
    for epsilon in (0.,1e-5,1e-10):
        state,_=query(fq.Circuit(2,dtype=D).ry(0,2*math.asin(epsilon)).cx(0,1))
        C=coefficients(state,(0,),(1,)); det=minors(C)[0].item()
        assert abs(det-epsilon*math.sqrt(1-epsilon**2))<ATOL
        if epsilon: assert abs(det)>0
    print('3 near-product states: nonzero small minors retained; no exact numeric rank certificate.')
    for theta,phi in ((.23,.7),(-.6,1.1),(1.3,-.9),(.91,2.1)):
        state,_=query(fq.Circuit(2,dtype=D).h(0).cx(0,1).ry(0,theta).p(1,phi))
        C=coefficients(state,(0,),(1,))
        assert abs(abs(minors(C)[0].item())-.5)<ATOL
    print('4 local-unitary Bell transformations: determinant magnitude preserved.')
    C=torch.tensor([[1,1j],[1j,-1]],dtype=D)/2
    invalid=[lambda:coefficients(torch.zeros(4,dtype=D),(0,),(1,)),
             lambda:coefficients(torch.ones(4,dtype=torch.float32),(0,),(1,)),
             lambda:coefficients(torch.ones(4,dtype=D)/2,(0,),(0,)),
             lambda:coefficients(torch.ones(4,dtype=D)/2,(),(0,1)),
             lambda:coefficients(torch.ones(4,dtype=D)/2,(False,),(1,)),
             lambda:coefficients(torch.ones((1,4),dtype=D)/2,(0,),(1,)),
             lambda:pivot_factors(torch.zeros((2,2),dtype=D)),
             lambda:pivot_factors(C*2),
             lambda:minors(torch.tensor([[float('nan')]],dtype=D)),
             lambda:minors(torch.ones((2,2),dtype=torch.float64)/2)]
    for f in invalid:
        try: f()
        except ValueError: pass
        else: raise AssertionError('Malformed input admitted')
    print('10 malformed contracts rejected before simulation.')
    assert RUNS==43,RUNS
    print('43 CPU complex128 circuits passed; exact theorem and numeric diagnostics remain distinct.')


if __name__=='__main__': main()
