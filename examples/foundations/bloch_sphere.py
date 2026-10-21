"""Section3.3: pure-qubit geometry; quadratic forms are not sampled readouts.

Uses pinned requirements-examples.txt and released FlagQuantum0.3.1.
"""
import cmath
from importlib.metadata import version
from math import cos, isclose, pi, sin, sqrt

import flagquantum as fq
import torch

DTYPE = torch.complex128
ATOL = 1e-12
PAULI = torch.tensor([[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]], dtype=DTYPE)
OPTIONS = fq.ExecutionOptions(mode="statevector", backend="pytorch", device="cpu", precision="complex128",
                              allow_backend_fallback=False, allow_approximate=False)


def unit_state(v):
    if not isinstance(v, torch.Tensor) or v.shape != (2,) or v.dtype != DTYPE:
        raise ValueError("Expected shape(2,) complex128")
    if v.device.type != "cpu" or v.layout != torch.strided or not torch.isfinite(v).all().item():
        raise ValueError("Expected finite dense CPU coordinates")
    if not isclose(torch.vdot(v,v).real.item(),1,rel_tol=0,abs_tol=ATOL):
        raise ValueError("Expected unit state; no automatic normalization")
    return v


def bloch(v):
    unit_state(v)
    forms = torch.stack([torch.vdot(v, matrix @ v) for matrix in PAULI])
    torch.testing.assert_close(forms.imag, torch.zeros(3,dtype=torch.float64), rtol=0, atol=ATOL)
    return forms.real


def scalar_coordinates(alpha, beta):
    # Independent explicit complex arithmetic, no Pauli matrices or torch.vdot.
    c = alpha.conjugate()*beta
    return (2*c.real, 2*c.imag, abs(alpha)**2-abs(beta)**2)


def inverse(point):
    if not isinstance(point,torch.Tensor) or point.shape != (3,) or point.dtype != torch.float64:
        raise ValueError("Expected shape(3,) float64")
    if point.device.type != "cpu" or point.layout != torch.strided or not torch.isfinite(point).all().item():
        raise ValueError("Expected finite dense CPU point")
    x,y,z = point.tolist()
    if not isclose(x*x+y*y+z*z,1,rel_tol=0,abs_tol=ATOL):
        raise ValueError("Expected unit-sphere point, not a general ball point")
    # Use the larger amplitude as the denominator; no division by a vanishing pole coordinate.
    if z >= 0:
        alpha = sqrt((1+z)/2)
        beta = complex(x,y)/(2*alpha)
    else:
        beta = sqrt((1-z)/2)
        alpha = complex(x,-y)/(2*beta)
    return unit_state(torch.tensor([alpha,beta],dtype=DTYPE))


def agrees(a,b):
    torch.testing.assert_close(a,torch.tensor(b,dtype=torch.float64),rtol=0,atol=ATOL)


def rejects(function,value):
    try:
        function(value)
    except ValueError:
        return True
    return False


def main():
    assert version("flagquantum") == "0.3.1"
    s = 1/sqrt(2)
    cases = [("|0>",[1,0],(0,0,1),"zero"), ("|1>",[0,1],(0,0,-1),"one"),
             ("|+>",[s,s],(1,0,0),"plus"), ("|->",[s,-s],(-1,0,0),"minus"),
             ("|+i>",[s,1j*s],(0,1,0),"positive_i"), ("|-i>",[s,-1j*s],(0,-1,0),"negative_i")]
    for label,coords,hand,preparation in cases:
        circuit = fq.Circuit(1,dtype=DTYPE)
        if preparation == "one":
            circuit.x(0)
        elif preparation != "zero":
            circuit.h(0)
            if preparation == "minus":circuit.z(0)
            elif preparation == "positive_i":circuit.phase(0,theta=pi/2)
            elif preparation == "negative_i":circuit.phase(0,theta=-pi/2)
        result = fq.run(circuit,outputs=[fq.probabilities()],options=OPTIONS)
        batch = result.statevector()
        assert batch.shape == result.probabilities.shape == (1,2)
        v = unit_state(batch[0])
        torch.testing.assert_close(v,torch.tensor(coords,dtype=DTYPE),rtol=0,atol=ATOL)
        agrees(bloch(v),hand)
        assert isclose(abs(torch.vdot(v,inverse(bloch(v))).item()),1,rel_tol=0,abs_tol=ATOL)
        agrees(bloch(v),scalar_coordinates(*map(complex,coords)))
        agrees(result.probabilities[0],((1+hand[2])/2,(1-hand[2])/2))
        print(f"{label}: Bloch=({hand[0]:.9f}, {hand[1]:.9f}, {hand[2]:.9f})")
    v = torch.tensor([sqrt(3)/2,.5j],dtype=DTYPE)
    point = bloch(v)
    agrees(point,(0,sqrt(3)/2,.5))
    print(f"worked state: Bloch=({point[0]:.9f}, {point[1]:.9f}, {point[2]:.9f}); P(0)=0.750000000")
    for k in range(13):
        theta = pi*k/12
        for ell in range(13):
            phi = 2*pi*ell/13
            alpha,beta = complex(cos(theta/2)),cmath.exp(1j*phi)*sin(theta/2)
            v = unit_state(torch.tensor([alpha,beta],dtype=DTYPE))
            point = bloch(v)
            agrees(point,scalar_coordinates(alpha,beta))
            agrees(point,(sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta)))
            assert isclose(torch.dot(point,point).item(),1,rel_tol=0,abs_tol=ATOL)
            agrees(bloch(cmath.exp(.37j)*v),point.tolist())
            restored = inverse(point)
            assert isclose(abs(torch.vdot(v,restored).item()),1,rel_tol=0,abs_tol=ATOL)
            agrees(bloch(restored),point.tolist())
            perpendicular = torch.tensor([-beta.conjugate(),alpha.conjugate()],dtype=DTYPE)
            assert abs(torch.vdot(v,perpendicular).item()) < ATOL
            agrees(bloch(perpendicular),(-point).tolist())
    for theta in [1e-7,pi-1e-7]:
        v = torch.tensor([cos(theta/2),cmath.exp(.7j)*sin(theta/2)],dtype=DTYPE)
        agrees(bloch(inverse(bloch(v))),bloch(v).tolist())
    # A transposed Y has the wrong sign. Real-only input tests miss this bug.
    positive_i = torch.tensor([s,1j*s],dtype=DTYPE)
    wrong_y = torch.vdot(positive_i,PAULI[1].T @ positive_i).real.item()
    assert isclose(wrong_y,-1,rel_tol=0,abs_tol=ATOL)
    bad_states = [torch.zeros(2,dtype=DTYPE),torch.tensor([1,1],dtype=DTYPE),positive_i.to(torch.complex64)]
    bad_points = [torch.zeros(3,dtype=torch.float64),torch.tensor([0,0,2.],dtype=torch.float64),
                  torch.tensor([0,0,float("nan")],dtype=torch.float64)]
    assert all(rejects(bloch,x) for x in bad_states)
    assert all(rejects(inverse,x) for x in bad_points)
    print("169 angle pairs: scalar/matrix/spherical coordinates, unit length and inverse-ray checks passed.")
    print("Global phases, orthogonal antipodes, poles, 2 near-pole cases and Y-sign witness checked.")
    print("6 invalid-input cases rejected; atol=1e-12. No shots, hardware or expectation-value API.")


if __name__ == "__main__":main()
