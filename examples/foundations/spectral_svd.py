#!/usr/bin/env python3
"""Spectral/SVD reconstruction with analytic references and kernel checks.

Python 3.12, PyTorch 2.13.0; CPU complex128. No quantum execution.
"""
from itertools import product
import math
import torch


def tensor(values):
    return torch.as_tensor(values, dtype=torch.complex128, device="cpu")


def check(actual, expected):
    torch.testing.assert_close(tensor(actual), tensor(expected), rtol=0, atol=1e-12)


def main():
    h = tensor([[2, 1j], [-1j, 2]])
    values, vectors = torch.linalg.eigh(h)
    q = tensor([[1, 1], [1j, -1j]])/math.sqrt(2)
    check(values, [1, 3])
    check(q.mH@q, torch.eye(2))
    check(q@torch.diag(tensor([1, 3]))@q.mH, h)
    check(vectors@torch.diag(values.to(torch.complex128))@vectors.mH, h)
    for i in range(2):
        check(h@vectors[:, i], values[i]*vectors[:, i])
        # Compare rank-one projectors, not arbitrary eigenvector phases.
        check(torch.outer(vectors[:, i], vectors[:, i].conj()),
              torch.outer(q[:, i], q[:, i].conj()))
    a = tensor([[3, 0, 0], [0, 0, 4j]])
    check(a.mH@a, torch.diag(tensor([9, 0, 16])))
    u_ref = tensor([[0, 1], [1j, 0]])
    v_ref = tensor([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    sigma = tensor([[4, 0, 0], [0, 3, 0]])
    check(u_ref@sigma@v_ref.mH, a)
    u, singular, vh = torch.linalg.svd(a, full_matrices=True)
    check(singular, [4, 3])
    assert u.shape == (2, 2) and vh.shape == (3, 3)
    sigma_numeric = torch.zeros((2, 3), dtype=torch.complex128)
    sigma_numeric[0, 0], sigma_numeric[1, 1] = singular[0], singular[1]
    check(u@sigma_numeric@vh, a)
    check(u.mH@u, torch.eye(2))
    check(vh@vh.mH, torch.eye(3))
    v = vh.mH
    check(a@v[:, 2], [0, 0])
    check(torch.outer(v[:, 2], v[:, 2].conj()), torch.diag(tensor([0, 1, 0])))
    for ar, ai, br, bi, cr, ci in product((-1, 0, 1), repeat=6):
        x = tensor([complex(ar, ai), complex(br, bi), complex(cr, ci)])
        direct = tensor([complex(3*ar, 3*ai), complex(-4*ci, 4*cr)])
        check(a@x, direct)
        check(u@sigma_numeric@(vh@x), direct)
        check(torch.vdot(a@x, a@x), 9*(ar*ar+ai*ai)+16*(cr*cr+ci*ci))
    # Degenerate eigenvectors can rotate without changing their spectral projector.
    d = torch.diag(tensor([2, 2, 0]))
    rotation = tensor([[1, 1, 0], [1j, -1j, 0], [0, 0, math.sqrt(2)]])/math.sqrt(2)
    check(rotation@d@rotation.mH, d)
    projector = rotation[:, :2]@rotation[:, :2].mH
    check(projector, torch.diag(tensor([1, 1, 0])))
    zero = torch.zeros((3, 2), dtype=torch.complex128)
    uz, sz, vhz = torch.linalg.svd(zero, full_matrices=True)
    check(sz, [0, 0])
    check(uz@torch.zeros((3, 2), dtype=torch.complex128)@vhz, zero)
    check(zero@vhz.mH, torch.zeros((3, 2)))  # Every right direction is in kernel.
    n = tensor([[0, 1], [0, 0]])
    check(torch.linalg.svdvals(n), [1, 0])
    check(u_ref@sigma@v_ref.T, a)  # A real right basis hides the conjugation error.
    # Ensure the missing-adjoint trap involves a complex right singular basis.
    complex_v = torch.diag(tensor([1j, 1, 1]))@v_ref
    complex_a = u_ref@sigma@complex_v.mH
    check(complex_a, [[-3j, 0, 0], [0, 0, 4j]])
    assert not torch.allclose(u_ref@sigma@complex_v.T, complex_a)
    residual = torch.linalg.vector_norm(u@sigma_numeric@vh-a).item()
    print("CPU complex128; reconstruction and subspace checks, no quantum execution.")
    print("Hermitian H: eigenvalues [1,3]; analytic eigenprojectors and reconstruction agree")
    print("Rectangular A (2x3): singular values [4,3]; full factor shapes U=2x2, Sigma=2x3, V^H=3x3")
    print("Right kernel: span(e2); full V retains the direction omitted by a reduced SVD")
    print(f"SVD reconstruction Frobenius residual <= 1e-12: {residual <= 1e-12}")
    print("729 inputs match direct three-coordinate formulas.")
    print("Degenerate eigenspace projector and all-zero rectangular kernel checks passed.")
    print("Nilpotent N: only eigenvalue 0 (proved in text), singular values [1,0]")
    print("Missing right adjoint detected with a complex right basis; no phase matching required.")


if __name__ == "__main__":
    main()
