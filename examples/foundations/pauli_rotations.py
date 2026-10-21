"""Section3.5: Pauli algebra and active rotations in radians.

Ideal released FlagQuantum0.3.1 CPU statevector checks, not hardware data.
"""
import cmath
from importlib.metadata import version
from math import cos, isclose, pi, sin, sqrt
import flagquantum as fq
import torch

DTYPE = torch.complex128
ATOL = 1e-12
I = torch.eye(2,dtype=DTYPE)
X = torch.tensor([[0,1],[1,0]],dtype=DTYPE)
Y = torch.tensor([[0,-1j],[1j,0]],dtype=DTYPE)
Z = torch.tensor([[1,0],[0,-1]],dtype=DTYPE)
PAULI = {"x":X,"y":Y,"z":Z}
OPTIONS = fq.ExecutionOptions(mode="statevector",backend="pytorch",device="cpu",precision="complex128",
                              allow_backend_fallback=False,allow_approximate=False)


def close(a,b):torch.testing.assert_close(a,b,rtol=0,atol=ATOL)


def explicit(axis,theta):
    c,s = cos(theta/2),sin(theta/2)
    if axis == "x":return torch.tensor([[c,-1j*s],[-1j*s,c]],dtype=DTYPE)
    if axis == "y":return torch.tensor([[c,-s],[s,c]],dtype=DTYPE)
    if axis == "z":return torch.tensor([[cmath.exp(-.5j*theta),0],[0,cmath.exp(.5j*theta)]],dtype=DTYPE)
    raise ValueError("Unknown rotation axis")


def coordinates(v):
    # Explicit scalar amplitudes, independent of Pauli quadratic-form matrices.
    a,b = v.tolist();q = a.conjugate()*b
    return (2*q.real,2*q.imag,abs(a)**2-abs(b)**2)


def rotate_point(axis,theta,point):
    x,y,z = point;c,s = cos(theta),sin(theta)
    if axis == "x":return (x,c*y-s*z,s*y+c*z)
    if axis == "y":return (c*x+s*z,y,-s*x+c*z)
    if axis == "z":return (c*x-s*y,s*x+c*y,z)
    raise ValueError("Unknown rotation axis")


def execute(gate,theta,preparation):
    c = fq.Circuit(1,dtype=DTYPE)
    if preparation == "one":c.x(0)
    elif preparation in ["plus","positive_i"]:
        c.h(0)
        if preparation == "positive_i":c.phase(0,theta=pi/2)
    getattr(c,gate)(0,theta=theta)
    result = fq.run(c,outputs=[fq.probabilities()],options=OPTIONS)
    v,p = result.statevector(),result.probabilities
    assert v.shape == p.shape == (1,2)
    assert v.dtype == DTYPE and p.dtype == torch.float64
    assert v.device.type == p.device.type == "cpu"
    assert torch.isfinite(v).all() and torch.isfinite(p).all()
    close(p[0],v[0].abs().square())
    return v[0]


def main():
    assert version("flagquantum") == "0.3.1"
    expected = [[I,1j*Z,-1j*Y],[-1j*Z,I,1j*X],[1j*Y,-1j*X,I]]
    for j,a in enumerate(PAULI.values()):
        for k,b in enumerate(PAULI.values()):close(a@b,expected[j][k])
    print("All 9 Pauli products checked, including reversed-order signs.")
    s = 1/sqrt(2)
    inputs = {"zero":[1,0],"one":[0,1],"plus":[s,s],"positive_i":[s,1j*s]}
    for axis,matrix in PAULI.items():
        for k in range(-8,9):
            theta = pi*k/7
            u = explicit(axis,theta)
            close(u,torch.matrix_exp(-.5j*theta*matrix))
            close(u.mH@u,I);close(explicit(axis,-theta),u.mH)
            for label,pair in inputs.items():
                initial = torch.tensor(pair,dtype=DTYPE)
                expected_state = u@initial
                actual = execute("r"+axis,theta,label)
                close(actual,expected_state)
                assert isclose(torch.vdot(actual,actual).real.item(),1,rel_tol=0,abs_tol=ATOL)
                point = rotate_point(axis,theta,coordinates(initial))
                close(torch.tensor(coordinates(actual),dtype=torch.float64),torch.tensor(point,dtype=torch.float64))
        close(explicit(axis,2*pi),-I);close(explicit(axis,4*pi),I)
    for axis,label,target in [("x","zero",(0,-1,0)),("y","zero",(1,0,0)),("z","plus",(0,1,0))]:
        actual = execute("r"+axis,pi/2,label)
        close(torch.tensor(coordinates(actual),dtype=torch.float64),torch.tensor(target,dtype=torch.float64))
        print(f"R{axis}(pi/2), input {label}: Bloch=({target[0]}, {target[1]}, {target[2]})")
    print("51 angle/axis cases: explicit matrices, exponentials and FlagQuantum agree on 4 inputs each.")
    for n in [(1/sqrt(3),)*3,(.6,.8,0),(0,-.6,.8)]:
        generator = sum(nj*m for nj,m in zip(n,PAULI.values()))
        close(generator@generator,I)
        for theta in [-.7,0,1.1]:
            u = cos(theta/2)*I-1j*sin(theta/2)*generator
            close(u,torch.matrix_exp(-.5j*theta*generator))
            close(u.mH@u,I)
    # Nonunit n invalidates the involution shortcut.
    bad = 2*X
    wrong = cos(.5)*I-1j*sin(.5)*bad
    assert not torch.allclose(wrong,torch.matrix_exp(-.5j*bad),rtol=0,atol=ATOL)
    for theta in [-.7,pi/2,2*pi]:
        p = torch.diag(torch.tensor([1,cmath.exp(1j*theta)],dtype=DTYPE))
        close(p,cmath.exp(.5j*theta)*explicit("z",theta))
        for label,pair in inputs.items():
            close(execute("phase",theta,label),p@torch.tensor(pair,dtype=DTYPE))
    print("2pi gives -I; 4pi gives I; phase(theta)=exp(i*theta/2)*Rz(theta).")
    print("Inverse/norm checks, 3 general unit axes and a nonunit-axis failure witness passed (atol=1e-12).")
    print("Angles are radians; no shots, hardware or mixed-axis decomposition invoked.")


if __name__ == "__main__":main()
