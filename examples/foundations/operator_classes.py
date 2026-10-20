#!/usr/bin/env python3
"""Operator identities and counterexamples; no finite sampling certification.

Python 3.12, PyTorch 2.13.0; CPU complex128. No quantum execution.
"""
from itertools import product
import torch


def tensor(values):
    return torch.as_tensor(values, dtype=torch.complex128, device="cpu")


def check(actual, expected):
    torch.testing.assert_close(tensor(actual), tensor(expected), rtol=0, atol=1e-12)


def main():
    identity = torch.eye(2, dtype=torch.complex128)
    h = tensor([[2, 1j], [-1j, 2]])
    u = tensor([[1, 0], [0, 1j]])
    z = tensor([[1, 0], [0, -1]])
    p = tensor([[1, 0], [0, 0]])
    n = tensor([[0, 1], [0, 0]])
    check(h.mH, h)
    assert not torch.allclose(h.mH@h, identity)
    check(u.mH@u, identity)
    check(u@u.mH, identity)
    assert not torch.allclose(u.mH, u)
    check(z.mH, z)
    check(z.mH@z, identity)
    check(p.mH, p)
    check(p@p, p)
    check(torch.vdot(tensor([0, 1]), z@tensor([0, 1])), -1)
    check(torch.vdot(tensor([0, 1]), p@tensor([0, 1])), 0)
    check(torch.vdot(tensor([0, 1]), u@tensor([0, 1])), 1j)
    for ar, ai, br, bi in product(range(-2, 3), repeat=4):
        a, b = complex(ar, ai), complex(br, bi)
        v = tensor([a, b])
        # Independent scalar form: |a+i*b|^2 + |a|^2 + |b|^2.
        form = (ar-bi)**2+(ai+br)**2+ar**2+ai**2+br**2+bi**2
        check(torch.vdot(v, h@v), form)
        assert form >= ar**2+ai**2+br**2+bi**2
        check(torch.vdot(u@v, u@v), ar**2+ai**2+br**2+bi**2)
        check(torch.vdot(v, p@v), ar**2+ai**2)
    # Analytically supplied eigenpairs: no eigensolver is the reference.
    eigenpairs = [(h, 1, [1, 1j]), (h, 3, [1, -1j]),
                  (u, 1j, [0, 1]), (z, -1, [0, 1]), (p, 0, [0, 1])]
    residuals = []
    for matrix, value, vector in eigenpairs:
        v = tensor(vector)
        assert torch.linalg.vector_norm(v).item() > 0
        residual = torch.linalg.vector_norm(matrix@v-value*v).item()
        assert residual <= 1e-12
        residuals.append(residual)
    e1 = tensor([1, 0])
    check(torch.vdot(h@e1, h@e1), 5)
    check(n@n, [[0, 0], [0, 0]])
    assert not torch.allclose(n.mH, n)
    check(torch.vdot(tensor([1, -1]), n@tensor([1, -1])), -1)
    check(torch.vdot(tensor([1, 1j]), n@tensor([1, 1j])), 1j)
    print("CPU complex128 checks; algebraic models only.")
    print("H: Hermitian and positive definite; squared norm of H*e1=5, not 1")
    print("U=diag(1,i): unitary, not Hermitian; quadratic form at e2=i")
    print("Z=diag(1,-1): Hermitian and unitary, not positive; form at e2=-1")
    print("P=diag(1,0): positive semidefinite, not positive definite; form at e2=0")
    print("N=[[0,1],[0,0]]: N^2=0; forms -1 and i refute positivity")
    print(f"5 supplied nonzero eigenvectors: maximum residual={max(residuals):.1e}")
    print("625 vectors match independent H/U/P coordinate formulas.")
    print("Defining identities and counterexamples passed; sampled forms are not a proof.")


if __name__ == "__main__":
    main()
