"""Section5.1: chronological calls, products, native composition and adjoints."""
from itertools import product
from importlib.metadata import version
from math import sqrt,cos,sin,pi
import cmath
import torch
import flagquantum as fq
from flagquantum.errors import CapabilityError,ValidationError
try:
    from examples.foundations.tensor_spaces import prepare_matrix,OPTIONS
    from examples.foundations.local_operators import embedding
except ModuleNotFoundError:
    from tensor_spaces import prepare_matrix,OPTIONS
    from local_operators import embedding
DTYPE=torch.complex128
ATOL=1e-12
H=torch.tensor([[1,1],[1,-1]],dtype=DTYPE)/sqrt(2)
S=torch.diag(torch.tensor([1,1j],dtype=DTYPE))
G=torch.tensor([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=DTYPE)


def rx(theta):
    return torch.tensor([[cos(theta/2),-1j*sin(theta/2)],[-1j*sin(theta/2),cos(theta/2)]],dtype=DTYPE)


def rz(phi):return torch.diag(torch.tensor([cmath.exp(-.5j*phi),cmath.exp(.5j*phi)],dtype=DTYPE))


def matrix_product(gates,n):
    total=torch.eye(2**n,dtype=DTYPE)
    for gate in gates:total=gate@total
    return total


def scalar_steps(gates,coordinates):
    # Independent scalar evaluation of each chronological full-register map.
    values=list(coordinates)
    for gate in gates:
        a=gate.tolist();values=[sum(row[j]*values[j] for j in range(len(values))) for row in a]
    return torch.tensor(values,dtype=DTYPE)


def product_input(factors):
    values=[]
    for bits in product((0,1),repeat=len(factors)):
        coefficient=1+0j
        for q,v in enumerate(factors):coefficient*=v[bits[q]]
        values.append(coefficient)
    return torch.tensor(values,dtype=DTYPE)


def checked_adjoint(block):
    # Book-side precondition guard: released0.3.1 does not reject every custom nonunitary.
    for instruction in block.to_ir().instructions:
        if instruction.matrix is not None:
            M=instruction.matrix
            if not isinstance(M,torch.Tensor) or M.ndim!=2 or M.shape[0]!=M.shape[1] or M.dtype!=DTYPE or M.device.type!='cpu' or not torch.isfinite(M).all():
                raise CapabilityError('Book guard requires a finite square CPU complex128 custom matrix')
            if not torch.allclose(M.mH@M,torch.eye(M.shape[0],dtype=DTYPE),rtol=0,atol=ATOL):
                raise CapabilityError('Book guard: adjoint is an inverse only for a unitary custom gate')
    return block.adjoint()


def execute(block,factors):
    if len(factors)!=block.n_qubits:raise ValueError('One preparation per qubit required')
    c=fq.Circuit(block.n_qubits,dtype=DTYPE)
    for q,v in enumerate(factors):c.unitary(q,unitary=prepare_matrix(torch.tensor(v,dtype=DTYPE)))
    c.compose(block)
    r=fq.run(c,outputs=[fq.probabilities()],options=OPTIONS);state,p=r.statevector(),r.probabilities
    assert state.shape==p.shape==(1,2**block.n_qubits) and state.dtype==DTYPE and p.dtype==torch.float64
    assert state.device.type==p.device.type=='cpu' and torch.isfinite(state).all() and torch.isfinite(p).all()
    torch.testing.assert_close(p[0],state[0].abs().square(),rtol=0,atol=ATOL)
    return state[0],p[0]


def hs():return fq.Circuit(1,dtype=DTYPE).h(0).s(0)


def two_case():
    c=fq.Circuit(2,dtype=DTYPE).h(0).s(1).unitary(0,1,unitary=G).rz(0,.17)
    return c,[embedding(H,2,0),embedding(S,2,1),G,embedding(rz(.17),2,0)]


def cases():
    custom=cmath.exp(.31j)*(H@rz(.43))
    mapped=fq.Circuit(3,dtype=DTYPE).compose(hs(),qubits=(2,)).rx(0,.27)
    two,gates=two_case()
    return [('HS',hs(),[H,S]),('rotations',fq.Circuit(1,dtype=DTYPE).rx(0,.7).rz(0,-.4),[rx(.7),rz(-.4)]),('custom-phase',fq.Circuit(1,dtype=DTYPE).h(0).unitary(0,unitary=custom),[H,custom]),('two-qubit',two,gates),('mapped',mapped,[embedding(H,3,2),embedding(S,3,2),embedding(rx(.27),3,0)])]


def main():
    assert version('flagquantum')=='0.3.1' and version('torch').split('+')[0]=='2.13.0'
    print('Chronological G1,...,Gm gives matrix Gm...G1; inverse calls Gm^dagger,...,G1^dagger.')
    runs=0
    for name,block,gates in cases():
        n=block.n_qubits;U=matrix_product(gates,n);names=tuple(i.name for i in block.to_ir().instructions)
        inverse=checked_adjoint(block);assert inverse is not block
        assert tuple(i.name for i in block.to_ir().instructions)==names
        roundtrip=fq.Circuit(n,dtype=DTYPE).compose(block).compose(inverse)
        other=fq.Circuit(n,dtype=DTYPE).compose(inverse).compose(block)
        inputs=[[(1,0) if b==0 else (0,1) for b in bits] for bits in product((0,1),repeat=n)]
        inputs.append([(.6,.8j) if q%2==0 else (sqrt(.7),cmath.exp(.2j)*sqrt(.3)) for q in range(n)])
        for factors in inputs:
            initial=product_input(factors)
            expected=scalar_steps(gates,initial.tolist())
            torch.testing.assert_close(expected,U@initial,rtol=0,atol=ATOL)
            actual,_=execute(block,factors);back,_=execute(inverse,factors)
            recovered,_=execute(roundtrip,factors);recovered_other,_=execute(other,factors);runs+=4
            torch.testing.assert_close(actual,expected,rtol=0,atol=ATOL)
            torch.testing.assert_close(back,U.mH@initial,rtol=0,atol=ATOL)
            torch.testing.assert_close(recovered,initial,rtol=0,atol=ATOL)
            torch.testing.assert_close(recovered_other,initial,rtol=0,atol=ATOL)
        print(f'{name}: all{2**n}basis columns and1complex product,forward/adjoint/both roundtrips passed.')
    assert runs==92
    empty=fq.Circuit(1,dtype=DTYPE);assert len(empty.adjoint().to_ir().instructions)==0
    state,_=execute(empty,[(1,0)]);torch.testing.assert_close(state,torch.tensor([1,0],dtype=DTYPE),rtol=0,atol=ATOL)
    twopi=fq.Circuit(1,dtype=DTYPE).rx(0,2*pi)
    phase,_=execute(twopi,[(1,0)]);undo,_=execute(fq.Circuit(1,dtype=DTYPE).compose(twopi).compose(twopi.adjoint()),[(1,0)])
    torch.testing.assert_close(phase,torch.tensor([-1,0],dtype=DTYPE),rtol=0,atol=ATOL)
    torch.testing.assert_close(undo,torch.tensor([1,0],dtype=DTYPE),rtol=0,atol=ATOL)
    A=fq.Circuit(1,dtype=DTYPE).h(0);B=fq.Circuit(1,dtype=DTYPE).s(0);dest=fq.Circuit(1,dtype=DTYPE)
    assert dest.compose(A) is dest and dest.compose(B) is dest
    value,_=execute(dest,[(.6,.8j)])
    torch.testing.assert_close(value,S@H@torch.tensor([.6,.8j],dtype=DTYPE),rtol=0,atol=ATOL)
    assert len(A.to_ir().instructions)==len(B.to_ir().instructions)==1
    wrong1=fq.Circuit(1,dtype=DTYPE).compose(hs()).h(0).sdg(0)
    wrong2=fq.Circuit(1,dtype=DTYPE).compose(hs()).s(0).h(0)
    for wrong in (wrong1,wrong2):
        bad_state,_=execute(wrong,[(1,0)])
        assert not torch.allclose(bad_state,torch.tensor([1,0],dtype=DTYPE),rtol=0,atol=ATOL)
    bad=[(CapabilityError,lambda:checked_adjoint(fq.Circuit(1,dtype=DTYPE).unitary(0,unitary=torch.diag(torch.tensor([1,0],dtype=DTYPE))))),(CapabilityError,lambda:checked_adjoint(fq.Circuit(1,dtype=DTYPE).unitary(0,unitary=2*H))),(ValidationError,lambda:fq.Circuit(2).compose(hs(),qubits=(2,))),(TypeError,lambda:fq.Circuit(2).compose(hs(),qubits=(0,),qubit_map={0:1})),(ValidationError,lambda:fq.Circuit(2).compose(two_case()[0],qubits=(0,0))),(ValidationError,lambda:fq.Circuit(1).compose(fq.Circuit(1,bsz=2))),(TypeError,lambda:fq.Circuit(1).compose('not-a-program'))]
    for error,action in bad:
        try:action()
        except error:pass
        else:raise AssertionError('Invalid inverse/compose contract admitted')
    print('Empty circuit,2pi phase,mutating compose,source order,two wrong inverses and7invalid contracts checked.')
    print('98 actual CPU complex128 circuits; atol=1e-12,rtol=0; no phase alignment,measurement inversion or hardware.')


if __name__=='__main__':main()
