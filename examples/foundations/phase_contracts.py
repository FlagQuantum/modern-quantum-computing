"""Section3.7: phase comparison scope and an explicit four-coordinate preview.

Coordinate order: |00>,|01>,|10>,|11>; index=2*control+target.
"""
import cmath
from importlib.metadata import version
from math import cos, isclose, pi, sqrt
import flagquantum as fq
import torch

DTYPE = torch.complex128
ATOL = 1e-12
I = torch.eye(2,dtype=DTYPE)
OPTIONS = fq.ExecutionOptions(mode="statevector",backend="pytorch",device="cpu",precision="complex128",
                              allow_backend_fallback=False,allow_approximate=False)


def close(a,b):torch.testing.assert_close(a,b,rtol=0,atol=ATOL)


def finite(v):
    if not isinstance(v,torch.Tensor) or v.dtype != DTYPE or v.device.type != "cpu" or v.layout != torch.strided:
        raise ValueError("Expected dense CPU complex128")
    if not torch.isfinite(v).all().item():raise ValueError("Nonfinite coordinates")


def state(v):
    finite(v)
    if v.shape not in [(2,),(4,)]:raise ValueError("Expected2or4 coordinates")
    if not isclose(torch.vdot(v,v).real.item(),1,rel_tol=0,abs_tol=ATOL):raise ValueError("Expected unit norm")


def operator(u):
    finite(u)
    if u.shape not in [(2,2),(4,4)]:raise ValueError("Expected2or4 dimensional square matrix")
    if not torch.allclose(u.mH@u,torch.eye(u.shape[0],dtype=DTYPE),rtol=0,atol=ATOL):raise ValueError("Expected unitary")


def aligned(a,b):
    # Internal helper: public wrappers validate the domain and identical shape.
    c = torch.vdot(a.reshape(-1),b.reshape(-1))
    z = c.conj()/c.abs() if c.abs().item() != 0 else 1.
    return torch.linalg.vector_norm((a-z*b).reshape(-1)).item()


def state_residual(a,b):
    state(a);state(b)
    if a.shape != b.shape:raise ValueError("Shape mismatch")
    return aligned(a,b)


def operator_residual(a,b):
    operator(a);operator(b)
    if a.shape != b.shape:raise ValueError("Shape mismatch")
    return aligned(a,b)


def controlled(u):
    operator(u)
    if u.shape != (2,2):raise ValueError("One target qubit only")
    c = torch.eye(4,dtype=DTYPE);c[2:,2:]=u
    return c


def execute(matrix,basis=None,analyze=False,correction=None):
    c = fq.Circuit(2,dtype=DTYPE)
    if basis is None:c.h(0)
    else:
        if basis//2:c.x(0)
        if basis%2:c.x(1)
    c.unitary(0,1,unitary=matrix)
    if correction is not None:c.phase(0,theta=correction)
    if analyze:c.h(0)
    r = fq.run(c,outputs=[fq.probabilities()],options=OPTIONS)
    v,p = r.statevector(),r.probabilities
    assert v.shape == p.shape == (1,4)
    assert v.dtype == DTYPE and p.dtype == torch.float64
    assert v.device.type == p.device.type == "cpu"
    state(v[0]);assert torch.isfinite(p).all()
    close(p[0],v[0].abs().square())
    return v[0],p[0]


def rejects(function,value):
    try:function(value)
    except ValueError:return True
    return False


def main():
    assert version("flagquantum") == "0.3.1"
    plus = torch.tensor([1,1],dtype=DTYPE)/sqrt(2)
    minus = torch.tensor([1,-1],dtype=DTYPE)/sqrt(2)
    assert isclose(torch.linalg.vector_norm(plus-1j*plus).item(),sqrt(2),rel_tol=0,abs_tol=ATOL)
    assert state_residual(plus,1j*plus) < ATOL
    assert isclose(state_residual(plus,minus),sqrt(2),rel_tol=0,abs_tol=ATOL)
    close(plus.abs().square(),minus.abs().square())
    print("State comparison: raw global-i distance=1.414213562, aligned=0; relative-sign distance=1.414213562.")
    z = torch.diag(torch.tensor([1,-1],dtype=DTYPE))
    for k in [0,1]:assert state_residual(I[:,k],z[:,k]) < ATOL
    assert isclose(operator_residual(I,z),2,rel_tol=0,abs_tol=ATOL)
    print("I versus Z: each basis-column ray matches, but common-phase operator residual=2.000000000.")
    assert operator_residual(I,-I) < ATOL
    assert isclose(operator_residual(controlled(I),controlled(-I)),2*sqrt(2),rel_tol=0,abs_tol=ATOL)
    for phi in [0,pi/2,pi]:
        c = controlled(cmath.exp(1j*phi)*I)
        before,_ = execute(c)
        reference = torch.tensor([1,0,cmath.exp(1j*phi),0],dtype=DTYPE)/sqrt(2)
        close(before,reference)
        # Independent scalar overlap, separate from flatten-and-vdot comparator.
        assert abs(sum(a.conjugate()*b for a,b in zip(reference.tolist(),before.tolist()))-1) < ATOL
        _,p = execute(c,analyze=True)
        p0,p1 = p[:2].sum().item(),p[2:].sum().item()
        assert isclose(p0,(1+cos(phi))/2,rel_tol=0,abs_tol=ATOL)
        print(f"controlled phase phi/pi={phi/pi:.1f}: P(control=0)={p0:.9f}, P(control=1)={p1:.9f}")
    # Generic target from a previous Euler case: V=-iH, alpha=pi/2.
    h = torch.tensor([[1,1],[1,-1]],dtype=DTYPE)/sqrt(2)
    alpha = pi/2;v = cmath.exp(-1j*alpha)*h
    assert operator_residual(h,v) < ATOL
    ry = torch.tensor([[1,-1],[1,1]],dtype=DTYPE)/sqrt(2)
    rz = torch.diag(torch.tensor([-1j,1j],dtype=DTYPE))
    close(ry@rz,v)  # Chapter synthesis: chronological Rz(pi), then Ry(pi/2).
    cu,cv = controlled(h),controlled(v)
    for k in range(4):
        direct,_ = execute(cu,basis=k)
        fixed,_ = execute(cv,basis=k,correction=alpha)
        close(direct,cu[:,k]);close(fixed,direct)
    direct,_ = execute(cu)
    uncorrected,_ = execute(cv)
    fixed,_ = execute(cv,correction=alpha)
    close(fixed,direct)
    assert state_residual(direct,uncorrected) > .5
    print("Basis order verified on 4 columns; native control-phase correction recovers the generic controlled target.")
    # Exact zero overlap is a valid non-equivalence boundary, not division by zero.
    assert isclose(state_residual(torch.tensor([1,0],dtype=DTYPE),torch.tensor([0,1],dtype=DTYPE)),sqrt(2),rel_tol=0,abs_tol=ATOL)
    bad_states = [torch.zeros(2,dtype=DTYPE),2*plus,plus.reshape(1,2),plus.to(torch.complex64),
                  torch.tensor([float("nan"),0],dtype=DTYPE)]
    bad_ops = [torch.zeros((2,2),dtype=DTYPE),torch.eye(3,dtype=DTYPE),
               torch.tensor([[1,0],[0,float("inf")]],dtype=DTYPE)]
    assert all(rejects(state,x) for x in bad_states)
    assert all(rejects(operator,x) for x in bad_ops)
    print("Zero-overlap boundary and 8 invalid-input cases checked; atol=1e-12, no automatic normalization.")
    print("Controlled matrices use declared4-coordinate ordering; no shots or hardware.")


if __name__ == "__main__":main()
