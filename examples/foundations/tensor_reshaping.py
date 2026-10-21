"""Section4.6: prove and check reshape/permute/contraction as indexed mathematics."""
from itertools import product, permutations
from importlib.metadata import version
import cmath
from math import pi, sqrt
import torch
import flagquantum as fq
try:
    from examples.foundations.tensor_spaces import prepare_matrix, OPTIONS
    from examples.foundations.ordered_supports import support_tuple, checked_matrix, scalar_scatter, dense_embedding, input_product, controlled_flip
    from examples.foundations.permutations_swap import complex_factors, entangled_reference
except ModuleNotFoundError:
    from tensor_spaces import prepare_matrix, OPTIONS
    from ordered_supports import support_tuple, checked_matrix, scalar_scatter, dense_embedding, input_product, controlled_flip
    from permutations_swap import complex_factors, entangled_reference
DTYPE=torch.complex128
ATOL=1e-12


def checked_vector(state,n):
    if type(n) is not int or n<1:raise ValueError('Declare positive integer n')
    if not isinstance(state,torch.Tensor) or state.shape!=(2**n,) or state.dtype!=DTYPE or state.device.type!='cpu' or state.layout!=torch.strided or not torch.isfinite(state).all():
        raise ValueError('Expected finite dense CPU complex128 vector of length2**n; no batch axis')
    return state


def axis_order(n,support):
    support=support_tuple(n,support)
    return support+tuple(q for q in range(n) if q not in support)


def undo_order(order):
    return tuple(order.index(q) for q in range(len(order)))


def apply_local(state,matrix,n,support):
    """Logical indexed action: no 2**n by 2**n matrix; general linear maps allowed."""
    state=checked_vector(state,n);support=support_tuple(n,support)
    matrix=checked_matrix(matrix,len(support));order=axis_order(n,support)
    tensor=state.reshape((2,)*n)
    packed=tensor.permute(order).reshape(2**len(support),2**(n-len(support)))
    changed=matrix@packed
    return changed.reshape((2,)*n).permute(undo_order(order)).reshape(2**n)


def local_gate(k):
    m=2**k
    # Fourier columns are orthonormal; multiplying rows by unit phases preserves it.
    return torch.tensor([[cmath.exp(1j*(2*pi*r*c/m+.17*r))/sqrt(m) for c in range(m)] for r in range(m)],dtype=DTYPE)


def execute(matrix,n,support,factors,entangle=False):
    support=support_tuple(n,support);matrix=checked_matrix(matrix,len(support),unitary=True)
    if len(factors)!=n:raise ValueError('Declare one local preparation per qubit')
    if entangle and n<2:raise ValueError('Entangling preparation requires at least two qubits')
    c=fq.Circuit(n,dtype=DTYPE)
    for q,v in enumerate(factors):c.unitary(q,unitary=prepare_matrix(torch.tensor(v,dtype=DTYPE)))
    if entangle:c.unitary(0,1,unitary=controlled_flip())
    c.unitary(*support,unitary=matrix)
    result=fq.run(c,outputs=[fq.probabilities()],options=OPTIONS)
    state,p=result.statevector(),result.probabilities
    assert state.shape==p.shape==(1,2**n) and state.dtype==DTYPE and p.dtype==torch.float64
    assert state.device.type==p.device.type=='cpu' and torch.isfinite(state).all() and torch.isfinite(p).all()
    torch.testing.assert_close(p[0],state[0].abs().square(),rtol=0,atol=ATOL)
    return state[0],p[0]


def compare(initial,matrix,n,support):
    answer=apply_local(initial,matrix,n,support)
    scalar=torch.tensor(scalar_scatter(matrix,initial.tolist(),n,support),dtype=DTYPE)
    torch.testing.assert_close(answer,scalar,rtol=0,atol=ATOL)
    torch.testing.assert_close(answer,dense_embedding(matrix,n,support)@initial,rtol=0,atol=ATOL)
    return answer


def supports(n):return [s for k in range(1,n+1) for s in permutations(range(n),k)]


def main():
    assert version('flagquantum')=='0.3.1' and version('torch').split('+')[0]=='2.13.0'
    print('Logical axes(q0,...,q[n-1]); last bit varies fastest; batch axis excluded.')
    count=0;math_count=0
    for n in range(1,5):
        selected=supports(n) if n<4 else [(3,1),(1,3),(2,0,3,1)]
        for S in selected:
            U=local_gate(len(S))
            arbitrary=torch.tensor([complex((i%5)-2,((3*i)%7)-3)/10 for i in range(2**n)],dtype=DTYPE)
            compare(arbitrary,U,n,S);math_count+=1
            for bits in product((0,1),repeat=n):
                factors=[(1,0) if b==0 else (0,1) for b in bits]
                expected=compare(input_product(factors),U,n,S)
                actual,_=execute(U,n,S,factors)
                torch.testing.assert_close(actual,expected,rtol=0,atol=ATOL);count+=1
    assert count==186 and math_count==23
    print('186 basis circuits; all nonempty ordered supports through3qubits plus3four-qubit supports.')
    psi=entangled_reference()
    for S in supports(3):
        U=local_gate(len(S));expected=compare(psi,U,3,S)
        actual,_=execute(U,3,S,complex_factors(),True)
        torch.testing.assert_close(actual,expected,rtol=0,atol=ATOL)
        assert abs(torch.vdot(actual,actual).real.item()-1)<ATOL
    print('15 complex joint-state circuits;23arbitrary-vector classical cases; scalar/dense/packed references agree.')
    order=axis_order(3,(2,0));markers=torch.arange(8).reshape(2,2,2)
    packed=markers.permute(order).reshape(4,2)
    assert packed[3,0].item()==5 and markers.reshape(4,2)[3,0].item()==6
    assert torch.equal(packed.reshape(2,2,2).permute(undo_order(order)),markers)
    print(f'Support(2,0), axes{order}: input101 -> row3,column0,value{packed[3,0].item()}.')
    view=psi.reshape(2,2,2).permute(order)
    assert not view.is_contiguous()
    torch.testing.assert_close(view.reshape(4,2),view.contiguous().view(4,2),rtol=0,atol=0)
    # Strided 1D input: same logical coefficients, not a promise about storage.
    storage=torch.zeros(16,dtype=DTYPE);storage[::2]=psi
    torch.testing.assert_close(apply_local(storage[::2],local_gate(2),3,(2,0)),apply_local(psi,local_gate(2),3,(2,0)),rtol=0,atol=ATOL)
    M=torch.tensor([[1,2j],[0,0]],dtype=DTYPE)
    answer=compare(psi,M,3,(1,));assert abs(torch.vdot(answer,answer).real.item()-1)>.1
    assert torch.equal(apply_local(psi,torch.eye(4,dtype=DTYPE),3,(2,0)),psi)
    bad=[lambda:checked_vector(psi[None,:],3),lambda:checked_vector(psi,2),lambda:checked_vector(psi.to(torch.complex64),3),lambda:checked_vector(torch.full((8,),float('nan'),dtype=DTYPE),3),lambda:checked_vector(psi,True),lambda:axis_order(3,()),lambda:axis_order(3,(0,0)),lambda:axis_order(3,(0,3)),lambda:axis_order(3,(False,1)),lambda:apply_local(psi,torch.eye(2,dtype=DTYPE),3,(2,0)),lambda:checked_matrix(M,1,unitary=True)]
    for action in bad:
        try:action()
        except ValueError:pass
        else:raise AssertionError('Malformed contract admitted')
    print('Identity, full support, noncontiguous layout, nonunitary linear map and11invalid contracts checked.')
    print('201 actual CPU complex128 circuits; atol=1e-12,rtol=0; no phase alignment, shots or hardware.')


if __name__=='__main__':main()
