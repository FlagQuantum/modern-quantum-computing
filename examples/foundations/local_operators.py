"""Section4.3: local embeddings, scalar references and actual released execution."""
from importlib.metadata import version
from itertools import product
from math import sqrt
import torch
import flagquantum as fq

DTYPE=torch.complex128
ATOL=1e-12
OPTIONS=fq.ExecutionOptions(mode='statevector',backend='pytorch',device='cpu',precision='complex128',allow_backend_fallback=False,allow_approximate=False)


def rotation():
    return torch.tensor([[sqrt(3)/2,-.5j],[-.5j,sqrt(3)/2]],dtype=DTYPE)


def embedding(matrix,n,q):
    if type(n) is not int or n<1 or type(q) is not int or not 0<=q<n:
        raise ValueError('Declare a positive size and an in-range integer qubit')
    if not isinstance(matrix,torch.Tensor) or matrix.shape!=(2,2) or matrix.dtype!=DTYPE or matrix.device.type!='cpu' or matrix.layout!=torch.strided or not torch.isfinite(matrix).all():
        raise ValueError('Expected finite CPU complex128 2x2 matrix')
    matrix=matrix.contiguous()  # Preserve entries; torch.kron needs a compatible stride.
    out=torch.ones((1,1),dtype=DTYPE)
    for position in range(n):
        out=torch.kron(out,matrix if position==q else torch.eye(2,dtype=DTYPE))
    return out


def scalar_action(matrix,coordinates,n,q):
    # Enumerate tuple labels independently, with no Kronecker routine or reshape.
    labels=list(product((0,1),repeat=n));answer=[]
    for output in labels:
        value=0j
        for input_bits,z in zip(labels,coordinates):
            if all(output[r]==input_bits[r] for r in range(n) if r!=q):
                value+=matrix[output[q]][input_bits[q]]*z
        answer.append(value)
    return answer


def execute(n,q,preparations):
    c=fq.Circuit(n,dtype=DTYPE)
    for position,(a,b) in enumerate(preparations):
        # Same first-column construction proved in4.1.
        c.unitary(position,unitary=torch.tensor([[a,-complex(b).conjugate()],[b,complex(a).conjugate()]],dtype=DTYPE))
    c.unitary(q,unitary=rotation())
    r=fq.run(c,outputs=[fq.probabilities()],options=OPTIONS)
    state,p=r.statevector(),r.probabilities
    assert state.shape==p.shape==(1,2**n)
    assert state.dtype==DTYPE and p.dtype==torch.float64
    assert state.device.type==p.device.type=='cpu'
    assert torch.isfinite(state).all() and torch.isfinite(p).all()
    torch.testing.assert_close(p[0],state[0].abs().square(),rtol=0,atol=ATOL)
    return state[0],p[0]


def initial_product(preparations):
    return [product_coefficient(preparations,bits) for bits in product((0,1),repeat=len(preparations))]


def product_coefficient(preparations,bits):
    z=1+0j
    for vector,bit in zip(preparations,bits):z*=vector[bit]
    return z


def main():
    assert version('flagquantum')=='0.3.1' and version('torch').split('+')[0]=='2.13.0'
    u=rotation();eye=torch.eye(2,dtype=DTYPE)
    torch.testing.assert_close(u.mH@u,eye,rtol=0,atol=ATOL)
    print('Local matrix: U=[[sqrt(3)/2,-i/2],[-i/2,sqrt(3)/2]].')
    count=0
    for n in (2,3):
        for q in range(n):
            m=embedding(u,n,q)
            for bits in product((0,1),repeat=n):
                preparations=[(1,0) if bit==0 else (0,1) for bit in bits]
                reference=scalar_action(u.tolist(),initial_product(preparations),n,q)
                state,p=execute(n,q,preparations)
                torch.testing.assert_close(state,torch.tensor(reference,dtype=DTYPE),rtol=0,atol=ATOL)
                torch.testing.assert_close(m@torch.tensor(initial_product(preparations),dtype=DTYPE),state,rtol=0,atol=ATOL)
                count+=1
    assert count==32
    print('32 basis circuits: all supports on two/three qubits match scalar and Kronecker references.')
    factors=[(.6,.8j),(sqrt(3)/2,.5j)];joint=torch.tensor(initial_product(factors),dtype=DTYPE)
    outputs=[]
    for q in (0,1):
        state,p=execute(2,q,factors);outputs.append(state)
        reference=torch.tensor(scalar_action(u.tolist(),joint.tolist(),2,q),dtype=DTYPE)
        torch.testing.assert_close(state,reference,rtol=0,atol=ATOL)
        # Fixed computational probability for the untouched subsystem.
        untouched=1-q
        for b in (0,1):
            rows=[i for i,bits in enumerate(product((0,1),repeat=2)) if bits[untouched]==b]
            assert abs(sum(p[i].item() for i in rows)-sum(abs(joint[i].item())**2 for i in rows))<ATOL
        print(f'Product input, local qubit {q}: '+', '.join(f'{x:.9f}' for x in p.tolist())+'.')
    assert not torch.allclose(outputs[0],outputs[1],rtol=0,atol=ATOL)
    print('Target confusion rejected: U tensor I and I tensor U give different full states.')
    projector=torch.tensor([[1,0],[0,0]],dtype=DTYPE)
    projected=embedding(projector,2,0)@joint
    assert abs(projected.abs().square().sum().item()-.36)<ATOL
    assert not torch.allclose(embedding(projector,2,0).mH@embedding(projector,2,0),torch.eye(4,dtype=DTYPE),rtol=0,atol=ATOL)
    print('Nonunitary local map: output norm squared=0.360000000; no unitary-gate execution claimed.')
    for n,q in ((2,0),(3,1)):
        m=embedding(u,n,q)
        torch.testing.assert_close(m.mH,embedding(u.mH,n,q),rtol=0,atol=ATOL)
        torch.testing.assert_close(m.mH@m,torch.eye(2**n,dtype=DTYPE),rtol=0,atol=ATOL)
    bad=[lambda:embedding(u,0,0),lambda:embedding(u,2,-1),lambda:embedding(u,2,2),lambda:embedding(u,2,True),lambda:embedding(u.to(torch.complex64),2,0),lambda:embedding(torch.ones(3,3,dtype=DTYPE),2,0)]
    for action in bad:
        try:action()
        except ValueError:pass
        else:raise AssertionError('Invalid local-map metadata accepted')
    print('Adjoint/unitarity identities and 6 invalid-input cases checked.')
    print('34 actual CPU complex128 circuits; atol=1e-12, rtol=0; no shots or hardware.')


if __name__=='__main__':main()
