"""Section4.1: finite products, independent references and actual two-qubit preparation.

The2x3 checks are mathematical fixtures, not a non-qubit FlagQuantum API.
"""
from importlib.metadata import version
from itertools import product
from math import isclose, sqrt
import flagquantum as fq
import torch

DTYPE = torch.complex128
ATOL = 1e-12
OPTIONS = fq.ExecutionOptions(mode="statevector",backend="pytorch",device="cpu",precision="complex128",
                              allow_backend_fallback=False,allow_approximate=False)


def tensor(a,b):
    # Mathematical vectors need not be normalized; zero factors are allowed here.
    if not a or not b:raise ValueError("Expected nonempty coordinate lists")
    return [x*y for x in a for y in b]


def dot(a,b):return sum(x.conjugate()*y for x,y in zip(a,b))


def close(a,b):torch.testing.assert_close(a,b,rtol=0,atol=ATOL)


def prepare_matrix(v):
    if not isinstance(v,torch.Tensor) or v.shape != (2,) or v.dtype != DTYPE:
        raise ValueError("Expected shape2 complex128 state")
    if v.device.type != "cpu" or v.layout != torch.strided or not torch.isfinite(v).all().item():
        raise ValueError("Expected finite dense CPU state")
    if not isclose(torch.vdot(v,v).real.item(),1,rel_tol=0,abs_tol=ATOL):raise ValueError("Expected unit norm")
    a,b = v.tolist()
    u = torch.tensor([[a,-b.conjugate()],[b,a.conjugate()]],dtype=DTYPE)
    close(u.mH@u,torch.eye(2,dtype=DTYPE))
    return u


def execute(a,b=None):
    circuit = fq.Circuit(1 if b is None else 2,dtype=DTYPE)
    circuit.unitary(0,unitary=prepare_matrix(a))
    if b is not None:circuit.unitary(1,unitary=prepare_matrix(b))
    result = fq.run(circuit,outputs=[fq.probabilities()],options=OPTIONS)
    state,p = result.statevector(),result.probabilities
    assert state.shape == p.shape == (1,2 if b is None else 4)
    assert state.dtype == DTYPE and p.dtype == torch.float64
    assert state.device.type == p.device.type == "cpu"
    assert torch.isfinite(state).all() and torch.isfinite(p).all()
    close(p[0],state[0].abs().square())
    return state[0],p[0]


def rejected(v):
    try:prepare_matrix(v)
    except ValueError:return True
    return False


def main():
    assert version("flagquantum") == "0.3.1"
    # All6ordered product-basis vectors for C2 tensor C3.
    basis = []
    for i in range(2):
        for j in range(3):
            a = [complex(k==i) for k in range(2)]
            b = [complex(k==j) for k in range(3)]
            expected = [complex(k==3*i+j) for k in range(6)]
            assert tensor(a,b) == expected
            basis.append(tensor(a,b))
    columns = torch.tensor(basis,dtype=DTYPE).T
    close(columns.mH@columns,torch.eye(6,dtype=DTYPE))
    print("C2 tensor C3: 6 ordered basis vectors; Gram matrix is I6.")
    ap,bp = [1+1j,-1j],[1,-1,2j]
    lam = 1-2j
    count = 0
    for a in product([0j,1+0j,1j],repeat=2):
        for b in product([0j,1+0j,-1j],repeat=3):
            hand = tensor(a,b)
            ta,tb = torch.tensor(a,dtype=DTYPE),torch.tensor(b,dtype=DTYPE)
            close(torch.tensor(hand,dtype=DTYPE),torch.kron(ta,tb))
            assert abs(dot(hand,tensor(ap,bp))-dot(a,ap)*dot(b,bp)) < ATOL
            left = tensor([x+y for x,y in zip(a,ap)],b)
            right = [x+y for x,y in zip(hand,tensor(ap,b))]
            assert left == right
            assert tensor(a,[x+y for x,y in zip(b,bp)]) == [x+y for x,y in zip(hand,tensor(a,bp))]
            assert tensor([lam*x for x in a],b) == [lam*x for x in hand]
            assert tensor(a,[lam*x for x in b]) == [lam*x for x in hand]
            assert abs(dot(hand,hand)-dot(a,a)*dot(b,b)) < ATOL
            count += 1
    assert count == 243
    print("243 complex2x3 products: scalar/kron, bilinearity and factorized inner products agree.")
    a = torch.tensor([.6,.8j],dtype=DTYPE)
    b = torch.tensor([1,1j],dtype=DTYPE)/sqrt(2)
    av,_ = execute(a);bv,_ = execute(b)
    close(av,a);close(bv,b)
    joint,p = execute(a,b)
    expected = torch.tensor([3,3j,4j,-4],dtype=DTYPE)/(5*sqrt(2))
    close(joint,expected)
    close(joint,torch.tensor(tensor(a.tolist(),b.tolist()),dtype=DTYPE))
    close(joint,torch.kron(a,b))
    close(p,torch.tensor([.18,.18,.32,.32],dtype=torch.float64))
    assert isclose(torch.vdot(joint,joint).real.item(),1,rel_tol=0,abs_tol=ATOL)
    print("Worked amplitudes: (3, 3i, 4i, -4)/(5*sqrt(2)); order 00,01,10,11.")
    print("FlagQuantum probabilities: (0.180000000, 0.180000000, 0.320000000, 0.320000000).")
    for i in range(2):
        for j in range(2):
            aa,bb = torch.eye(2,dtype=DTYPE)[:,i],torch.eye(2,dtype=DTYPE)[:,j]
            state,_ = execute(aa,bb)
            close(state,torch.eye(4,dtype=DTYPE)[:,2*i+j])
    wrong_conjugate = torch.kron(a,b.conj())
    close(wrong_conjugate.abs().square(),p)
    assert abs(torch.vdot(joint,wrong_conjugate).item()) < ATOL
    assert not torch.allclose(torch.kron(b,a),joint,rtol=0,atol=ATOL)
    print("4 qubit-basis preparations, wrong factor order and unwanted conjugation witnesses checked.")
    # A general joint vector need not factor: diagonal products nonzero would force both cross entries nonzero.
    coefficients = [1/sqrt(2),0,0,1/sqrt(2)]
    assert coefficients[0]*coefficients[3] != coefficients[1]*coefficients[2]
    bad = [torch.zeros(2,dtype=DTYPE),2*a,a.reshape(1,2),a.to(torch.complex64),
           torch.tensor([float("nan"),0],dtype=DTYPE),torch.tensor([float("inf"),0],dtype=DTYPE)]
    assert all(rejected(v) for v in bad)
    print("Non-product coefficient witness and 6 invalid-preparation cases checked; atol=1e-12.")
    print("No qutrit execution, entangling preparation, shots or hardware claimed.")


if __name__ == "__main__":main()
