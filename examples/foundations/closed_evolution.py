"""Section3.4: specified constant generator, not a calibrated physical Hamiltonian.

Time t is numerical time in a declared reference unit; K=H*t0/hbar is dimensionless.
"""
import cmath
from importlib.metadata import version
from math import cos, isclose, pi, sin, sqrt

import flagquantum as fq
import torch

DTYPE = torch.complex128
ATOL = 1e-12
K = torch.tensor([[2,-1j],[1j,2]],dtype=DTYPE)
I = torch.eye(2,dtype=DTYPE)
OPTIONS = fq.ExecutionOptions(mode="statevector",backend="pytorch",device="cpu",precision="complex128",
                              allow_backend_fallback=False,allow_approximate=False)


def closed_matrix(t):
    e = cmath.exp(-2j*t)
    return torch.tensor([[e*cos(t),-e*sin(t)],[e*sin(t),e*cos(t)]],dtype=DTYPE)


def closed_derivative(t):
    # Independent scalar differentiation of the closed matrix, not matrix_exp AD.
    e,c,s = cmath.exp(-2j*t),cos(t),sin(t)
    return torch.tensor([[e*(-2j*c-s),e*(2j*s-c)],
                         [e*(-2j*s+c),e*(-2j*c-s)]],dtype=DTYPE)


def close(a,b):
    torch.testing.assert_close(a,b,rtol=0,atol=ATOL)


def simulate(u,kind):
    circuit = fq.Circuit(1,dtype=DTYPE)
    if kind == "one":circuit.x(0)
    elif kind == "plus":circuit.h(0)
    circuit.unitary(0,unitary=u)
    result = fq.run(circuit,outputs=[fq.probabilities()],options=OPTIONS)
    batch,p = result.statevector(),result.probabilities
    assert batch.shape == p.shape == (1,2)
    assert batch.dtype == DTYPE and p.dtype == torch.float64
    assert batch.device.type == p.device.type == "cpu"
    assert torch.isfinite(batch).all() and torch.isfinite(p).all()
    return batch[0],p[0]


def main():
    assert version("flagquantum") == "0.3.1"
    close(K.mH,K)
    for t in [0,pi/6,pi/4,pi/2,pi]:
        u = torch.matrix_exp(-1j*t*K)
        reference = closed_matrix(t)
        close(u,reference)
        close(u.mH@u,I)
        close(torch.matrix_exp(1j*t*K),u.mH)
        derivative = closed_derivative(t)
        close(1j*derivative,K@reference)
        close(1j*derivative@reference.mH,K)
        close(torch.matrix_exp(-1j*(t+.13)*K),u@torch.matrix_exp(-.13j*K))
        for kind,initial in [("zero",[1,0]),("one",[0,1]),("plus",[1/sqrt(2),1/sqrt(2)])]:
            state,p = simulate(u,kind)
            expected = reference@torch.tensor(initial,dtype=DTYPE)
            close(state,expected)
            close(p,expected.abs().square())
            assert isclose(torch.vdot(state,state).real.item(),1,rel_tol=0,abs_tol=ATOL)
            if kind == "zero":
                close(p,torch.tensor([cos(t)**2,sin(t)**2],dtype=torch.float64))
                print(f"t/pi={t/pi:.6f}: P(0)={p[0]:.9f}, P(1)={p[1]:.9f}")
        # Scalar energy/frequency shift changes the whole matrix by a common phase.
        shift = .7
        shifted = torch.matrix_exp(-1j*t*(K+shift*I))
        close(shifted,cmath.exp(-1j*t*shift)*u)
        close(shifted[:,0].abs().square(),u[:,0].abs().square())
    print("Closed matrix, analytic derivative, Hermitian generator and FlagQuantum agree (atol=1e-12).")
    # Single endpoint does not identify its constant generator, even up to scalar shifts.
    alternative = torch.diag(torch.tensor([0,2*pi],dtype=DTYPE))
    close(torch.matrix_exp(-1j*alternative),I)
    midpoint = torch.matrix_exp(-.5j*alternative)
    plus = torch.tensor([1/sqrt(2),1/sqrt(2)],dtype=DTYPE)
    assert abs(torch.vdot(plus,midpoint@plus).item()) < ATOL
    print("Different constant generators: same U(1)=I, orthogonal plus-state rays at t=0.5.")
    # A non-Hermitian matrix can preserve one chosen input while amplifying another.
    bad = torch.diag(torch.tensor([0,1j],dtype=DTYPE))
    v = torch.matrix_exp(-1j*bad)
    close(v[:,0],torch.tensor([1,0],dtype=DTYPE))
    assert v[:,1].norm().item() > 2
    assert not torch.allclose(v.mH@v,I,rtol=0,atol=ATOL)
    print("One preserved input does not certify unitarity; non-Hermitian counterexample checked.")
    print("No shots, hardware calibration or time-dependent solver invoked.")


if __name__ == "__main__":main()
