"""Section3.6: phase-tracked ZYZ factorization, with parameter endpoint cases.

Run from this repository; scalar rotation helpers are from Section3.5.
"""
import cmath
from importlib.metadata import version
from math import atan2, isclose, pi, sqrt
import flagquantum as fq
import torch
from pauli_rotations import explicit, coordinates

DTYPE = torch.complex128
UNIT_ATOL = 1e-12
ENDPOINT = 1e-12
RECON_ATOL = 5e-12
I = torch.eye(2,dtype=DTYPE)
OPTIONS = fq.ExecutionOptions(mode="statevector",backend="pytorch",device="cpu",precision="complex128",
                              allow_backend_fallback=False,allow_approximate=False)


def close(a,b,atol=RECON_ATOL):torch.testing.assert_close(a,b,rtol=0,atol=atol)


def factor(u):
    if not isinstance(u,torch.Tensor) or u.shape != (2,2) or u.dtype != DTYPE:
        raise ValueError("Expected2x2 complex128")
    if u.device.type != "cpu" or u.layout != torch.strided or not torch.isfinite(u).all().item():
        raise ValueError("Expected finite dense CPU matrix")
    if not torch.allclose(u.mH@u,I,rtol=0,atol=UNIT_ATOL):
        raise ValueError("Expected unitary input; no projection or renormalization")
    # Scalar2x2 determinant, independent of torch.linalg.det.
    rows = u.tolist();eta = rows[0][0]*rows[1][1]-rows[0][1]*rows[1][0]
    alpha = .5*cmath.phase(eta)
    v = cmath.exp(-1j*alpha)*u
    a,c = v[0,0].item(),v[1,0].item()
    if abs(c) <= ENDPOINT:
        beta,gamma,delta,branch = -2*cmath.phase(a),0.,0.,"north"
    elif abs(a) <= ENDPOINT:
        beta,gamma,delta,branch = 2*cmath.phase(c),pi,0.,"south"
    else:
        beta = cmath.phase(c)-cmath.phase(a)
        gamma = 2*atan2(abs(c),abs(a))
        delta = -cmath.phase(c)-cmath.phase(a)
        branch = "generic"
    reconstructed = cmath.exp(1j*alpha)*(explicit("z",beta)@explicit("y",gamma)@explicit("z",delta))
    close(reconstructed,u)
    return alpha,beta,gamma,delta,branch


def run(gates,initial="zero",matrix=None):
    circuit = fq.Circuit(1,dtype=DTYPE)
    if initial == "one":circuit.x(0)
    elif initial in ["plus","positive_i"]:
        circuit.h(0)
        if initial == "positive_i":circuit.phase(0,theta=pi/2)
    if matrix is not None:circuit.unitary(0,unitary=matrix)
    for axis,theta in gates:getattr(circuit,"r"+axis)(0,theta=theta)
    result = fq.run(circuit,outputs=[fq.probabilities()],options=OPTIONS)
    batch,p = result.statevector(),result.probabilities
    assert batch.shape == p.shape == (1,2)
    assert batch.dtype == DTYPE and p.dtype == torch.float64
    assert batch.device.type == p.device.type == "cpu"
    assert torch.isfinite(batch).all() and torch.isfinite(p).all()
    close(p[0],batch[0].abs().square())
    assert isclose(p.sum().item(),1,rel_tol=0,abs_tol=RECON_ATOL)
    return batch[0]


def rejects(value):
    try:factor(value)
    except ValueError:return True
    return False


def main():
    assert version("flagquantum") == "0.3.1"
    xy = run([("x",pi/2),("z",pi/2)])
    yx = run([("z",pi/2),("x",pi/2)])
    close(xy,(explicit("z",pi/2)@explicit("x",pi/2))[:,0])
    close(yx,(explicit("x",pi/2)@explicit("z",pi/2))[:,0])
    close(torch.tensor(coordinates(xy),dtype=torch.float64),torch.tensor([1,0,0],dtype=torch.float64))
    close(torch.tensor(coordinates(yx),dtype=torch.float64),torch.tensor([0,-1,0],dtype=torch.float64))
    assert isclose(abs(torch.vdot(xy,yx).item())**2,.5,rel_tol=0,abs_tol=RECON_ATOL)
    print("Rx then Rz: Bloch=(1, 0, 0); Rz then Rx: Bloch=(0, -1, 0).")
    #36target fixtures include gamma=0 and gamma=pi for each phase/outer-angle case.
    targets = []
    for alpha in [0,.43,-1.2]:
        for beta,delta in [(.7,-.4),(-1.1,.9),(2.2,-.8)]:
            for gamma in [0,.4,1.3,pi]:
                targets.append(cmath.exp(1j*alpha)*(explicit("z",beta)@explicit("y",gamma)@explicit("z",delta)))
    # Literal matrices check extraction without generated Euler parameters.
    targets += [I,torch.tensor([[0,1],[1,0]],dtype=DTYPE),
                torch.tensor([[0,-1j],[1j,0]],dtype=DTYPE),
                torch.tensor([[1,1],[1,-1]],dtype=DTYPE)/sqrt(2)]
    branches = set()
    inputs = {"zero":[1,0],"one":[0,1],"plus":[1/sqrt(2)]*2,"positive_i":[1/sqrt(2),1j/sqrt(2)]}
    for u in targets:
        alpha,beta,gamma,delta,branch = factor(u);branches.add(branch)
        gates = [("z",delta),("y",gamma),("z",beta)]
        for label,pair in inputs.items():
            expected = u@torch.tensor(pair,dtype=DTYPE)
            direct = run([],label,matrix=u)
            decomposed = run(gates,label)
            close(direct,expected)
            close(cmath.exp(1j*alpha)*decomposed,expected)
    assert branches == {"north","south","generic"}
    print("40 targets: phase-tracked ZYZ reconstruction and both FlagQuantum paths agree on 4 inputs each.")
    print("Generic, gamma=0 and gamma=pi branches checked; parameter uniqueness is not claimed.")
    for gamma in [1e-13,1e-9,pi-1e-13,pi-1e-9]:
        u = cmath.exp(.37j)*(explicit("z",.8)@explicit("y",gamma)@explicit("z",-.3))
        factor(u)
    # Equal isolated rays do not excuse a missing phase in a full matrix check.
    target = cmath.exp(.43j)*explicit("y",.6)
    alpha,beta,gamma,delta,_ = factor(target)
    v = explicit("z",beta)@explicit("y",gamma)@explicit("z",delta)
    assert not torch.allclose(v,target,rtol=0,atol=RECON_ATOL)
    close(v[:,0].abs().square(),target[:,0].abs().square())
    bad = [torch.zeros((2,2),dtype=DTYPE),torch.diag(torch.tensor([1,2],dtype=DTYPE)),
           torch.eye(3,dtype=DTYPE),I.to(torch.complex64),torch.full((2,2),float("nan"),dtype=DTYPE)]
    assert all(rejects(u) for u in bad)
    print("4 near-endpoint cases, omitted-phase witness and 5 invalid-input rejections passed.")
    print("Unitary-input atol=1e-12; endpoint threshold=1e-12; reconstruction atol=5e-12.")
    print("The three-gate circuit implements V; exp(i*alpha) is diagnostic array arithmetic. No hardware.")


if __name__ == "__main__":main()
