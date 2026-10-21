"""Section4.4: ordered supports; scalar scatter, dense reference and FlagQuantum."""
from importlib.metadata import version
from itertools import product, permutations
from math import sqrt, pi
import cmath
import torch
import flagquantum as fq
try:
    from examples.foundations.tensor_spaces import prepare_matrix, OPTIONS
    from examples.foundations.local_operators import rotation, embedding
except ModuleNotFoundError:
    from tensor_spaces import prepare_matrix, OPTIONS
    from local_operators import rotation, embedding

DTYPE=torch.complex128
ATOL=1e-12


def support_tuple(n,support):
    if type(n) is not int or n<1:
        raise ValueError('Declare a positive integer register size')
    if not isinstance(support,(tuple,list)) or not support or len(support)>n:
        raise ValueError('Declare a nonempty ordered support of size at most n')
    if any(type(q) is not int or not 0<=q<n for q in support) or len(set(support))!=len(support):
        raise ValueError('Support labels must be distinct in-range integers; no sorting or repair')
    return tuple(support)


def checked_matrix(matrix,k,unitary=False):
    if not isinstance(matrix,torch.Tensor) or matrix.shape!=(2**k,2**k) or matrix.dtype!=DTYPE or matrix.device.type!='cpu' or matrix.layout!=torch.strided or not torch.isfinite(matrix).all():
        raise ValueError('Expected finite dense CPU complex128 matrix of the declared local dimension')
    matrix=matrix.contiguous()
    if unitary and not torch.allclose(matrix.mH@matrix,torch.eye(2**k,dtype=DTYPE),rtol=0,atol=ATOL):
        raise ValueError('Deterministic gate matrix must be unitary; no normalization')
    return matrix


def binary(bits):
    return int(''.join(map(str,bits)),2)


def dense_embedding(matrix,n,support):
    support=support_tuple(n,support);matrix=checked_matrix(matrix,len(support))
    labels=list(product((0,1),repeat=n));m=torch.zeros((2**n,2**n),dtype=DTYPE)
    for row,b in enumerate(labels):
        local_row=sum(b[q]*2**(len(support)-1-j) for j,q in enumerate(support))
        for col,c in enumerate(labels):
            if all(b[q]==c[q] for q in range(n) if q not in support):
                local_col=sum(c[q]*2**(len(support)-1-j) for j,q in enumerate(support))
                m[row,col]=matrix[local_row,local_col]
    return m


def scalar_scatter(matrix,coordinates,n,support):
    # Independent input-centric scatter; no dense embedding, kron or reshape.
    support=support_tuple(n,support);a=checked_matrix(matrix,len(support)).tolist()
    if len(coordinates)!=2**n:raise ValueError('Wrong coordinate length')
    out=[0j]*(2**n)
    for input_bits,z in zip(product((0,1),repeat=n),coordinates):
        local_col=binary([input_bits[q] for q in support])
        for local_row,local_output in enumerate(product((0,1),repeat=len(support))):
            output_bits=list(input_bits)
            for q,bit in zip(support,local_output):output_bits[q]=bit
            out[binary(output_bits)]+=a[local_row][local_col]*z
    return out


def controlled_flip():
    return torch.tensor([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=DTYPE)


def complex_gate():
    h=torch.tensor([[1,1],[1,-1]],dtype=DTYPE)/sqrt(2)
    return controlled_flip()@torch.kron(rotation(),h)


def input_product(factors):
    answer=[]
    for bits in product((0,1),repeat=len(factors)):
        z=1+0j
        for v,b in zip(factors,bits):z*=v[b]
        answer.append(z)
    return torch.tensor(answer,dtype=DTYPE)


def execute(matrix,n,support,factors):
    support=support_tuple(n,support);matrix=checked_matrix(matrix,len(support),unitary=True)
    if len(factors)!=n:raise ValueError('Declare one preparation for every qubit')
    c=fq.Circuit(n,dtype=DTYPE)
    for q,v in enumerate(factors):c.unitary(q,unitary=prepare_matrix(torch.tensor(v,dtype=DTYPE)))
    c.unitary(*support,unitary=matrix)
    r=fq.run(c,outputs=[fq.probabilities()],options=OPTIONS)
    state,p=r.statevector(),r.probabilities
    assert state.shape==p.shape==(1,2**n) and state.dtype==DTYPE and p.dtype==torch.float64
    assert state.device.type==p.device.type=='cpu' and torch.isfinite(state).all() and torch.isfinite(p).all()
    torch.testing.assert_close(p[0],state[0].abs().square(),rtol=0,atol=ATOL)
    return state[0],p[0]


def verify(matrix,n,support,factors):
    initial=input_product(factors);state,p=execute(matrix,n,support,factors)
    reference=torch.tensor(scalar_scatter(matrix,initial.tolist(),n,support),dtype=DTYPE)
    torch.testing.assert_close(state,reference,rtol=0,atol=ATOL)
    torch.testing.assert_close(state,dense_embedding(matrix,n,support)@initial,rtol=0,atol=ATOL)
    return state,p


def main():
    assert version('flagquantum')=='0.3.1' and version('torch').split('+')[0]=='2.13.0'
    print('Support is an ordered tuple; its first qubit is the most significant local bit.')
    basis=[(0,1),(1,0),(1,0)]
    for support in ((2,0),(0,2)):
        state,p=verify(controlled_flip(),3,support,basis)
        print(f'Input100, support{support}: occupied global index {int(p.argmax())}.')
    gate=complex_gate();count=0
    for n,supports in ((2,list(permutations(range(2),2))),(3,list(permutations(range(3),2))),(4,[(3,1),(1,3)])):
        for support in supports:
            for bits in product((0,1),repeat=n):
                factors=[(1,0) if b==0 else (0,1) for b in bits]
                verify(gate,n,support,factors);count+=1
    assert count==88
    print('88 basis/support circuits: complex asymmetric gate;2/3qubit ordered pairs and4qubit nonadjacent supports.')
    factors=[(.6,.8j),(sqrt(3)/2,.5j),(1/sqrt(2),1j/sqrt(2))]
    states=[]
    for support in ((2,0),(0,2)):
        state,p=verify(gate,3,support,factors);states.append(state)
        initial=input_product(factors)
        for spectator_bit in (0,1):
            rows=[i for i,b in enumerate(product((0,1),repeat=3)) if b[1]==spectator_bit]
            assert abs(sum(p[i].item() for i in rows)-sum(abs(initial[i].item())**2 for i in rows))<ATOL
        print(f'Complex input, support{support}: '+', '.join(f'{x:.9f}' for x in p.tolist())+'.')
    assert not torch.allclose(states[0],states[1],rtol=0,atol=ATOL)
    # Full3qubit support: discrete Fourier matrix, independent finite scalar sums.
    f=torch.tensor([[cmath.exp(2j*pi*r*c/8)/sqrt(8) for c in range(8)] for r in range(8)],dtype=DTYPE)
    for bits in product((0,1),repeat=3):verify(f,3,(2,0,1),[(1,0) if b==0 else (0,1) for b in bits])
    print('8 full-support circuits: dimension8 Fourier matrix on ordered support(2,0,1).')
    torch.testing.assert_close(dense_embedding(rotation(),3,(1,)),embedding(rotation(),3,1),rtol=0,atol=ATOL)
    m=dense_embedding(gate,3,(2,0))
    torch.testing.assert_close(m.mH@m,torch.eye(8,dtype=DTYPE),rtol=0,atol=ATOL)
    projected=dense_embedding(torch.diag(torch.tensor([1,0,0,0],dtype=DTYPE)),3,(2,0))
    assert not torch.allclose(projected.mH@projected,torch.eye(8,dtype=DTYPE),rtol=0,atol=ATOL)
    bad=[lambda:support_tuple(3,()),lambda:support_tuple(3,(0,0)),lambda:support_tuple(3,(0,3)),lambda:support_tuple(3,(True,1)),lambda:support_tuple(3,(0,1.0)),lambda:support_tuple(0,(0,)),lambda:checked_matrix(gate,1),lambda:checked_matrix(gate.to(torch.complex64),2),lambda:checked_matrix(2*gate,2,True),lambda:checked_matrix(torch.full((4,4),float('nan'),dtype=DTYPE),2)]
    for action in bad:
        try:action()
        except ValueError:pass
        else:raise AssertionError('Malformed local contract admitted')
    print('Single-factor reduction, global unitarity, nonunitary reference and10invalid-input cases checked.')
    print('100 actual CPU complex128 circuits; atol=1e-12,rtol=0; no sorting, shots, routing or hardware.')


if __name__=='__main__':main()
