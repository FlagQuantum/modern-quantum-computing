#!/usr/bin/env python3
"""One linear map in two bases, checked against direct coordinate arithmetic.

Python 3.12, PyTorch 2.13.0, CPU complex128. No quantum backend required.
"""
import math
import torch


def tensor(values):
    return torch.as_tensor(values, dtype=torch.complex128, device="cpu")


def check(actual, expected):
    torch.testing.assert_close(tensor(actual), tensor(expected), rtol=0, atol=1e-12)


def main():
    matrix = tensor([[0, 1], [1, 0]])
    basis = tensor([[1, 1], [0, 1]])  # Columns are the new basis in old coordinates.
    changed = torch.linalg.solve(basis, matrix@basis)
    check(changed, [[-1, 0], [1, 1]])
    for ar in range(-2, 3):
        for ai in range(-2, 3):
            for br in range(-2, 3):
                for bi in range(-2, 3):
                    a, b = complex(ar, ai), complex(br, bi)
                    x = tensor([a, b])
                    y = torch.linalg.solve(basis, x)
                    check(y, [a-b, b])  # Independent inverse-coordinate formula.
                    check(changed@y, [b-a, a])  # Independently re-express swap(x).
                    check(basis@(changed@y), [b, a])
                    check(matrix@x, [b, a])
    x = tensor([2, 3])
    y = torch.linalg.solve(basis, x)
    check(y, [-1, 3])
    check(changed@y, [1, 2])
    check(basis@(changed@y), [3, 2])
    # Omit the output-coordinate conversion: interpret old output as new.
    wrong = matrix@basis
    check(basis@(wrong@y), [5, 2])
    assert not torch.allclose(basis@(wrong@y), matrix@x)
    assert not torch.allclose(basis.mH, torch.linalg.solve(basis, torch.eye(2, dtype=torch.complex128)))
    gram = basis.mH@basis
    check(gram, [[1, 1], [1, 2]])
    check(torch.vdot(x, x), 13)
    check(torch.vdot(y, y), 10)
    check(torch.vdot(y, gram@y), 13)
    # Complex orthonormal basis; plain transpose is still not the inverse.
    q = tensor([[1, 1], [1j, -1j]])/math.sqrt(2)
    check(q.mH@q, [[1, 0], [0, 1]])
    changed_q = q.mH@matrix@q
    check(changed_q, [[0, -1j], [1j, 0]])
    check(changed_q, torch.linalg.solve(q, matrix@q))
    check(q@(changed_q@(q.mH@x)), matrix@x)
    check(torch.vdot(q.mH@x, q.mH@x), torch.vdot(x, x))
    assert not torch.allclose(q.T@matrix@q, changed_q)
    # Active multiplication changes the vector; passive conversion does not.
    check(basis@x, [5, 3])
    check(basis@y, x)
    singular = tensor([[1, 2], [0, 0]])
    try:
        torch.linalg.solve(singular, x)
    except torch.linalg.LinAlgError:
        pass
    else:
        raise AssertionError("A dependent column set was accepted as a basis")
    print("CPU complex128 coordinate checks; no quantum execution.")
    print("S=[[1,1],[0,1]]; B=S^(-1) A S=[[-1,0],[1,1]]")
    print("x=[2,3] -> new coordinates y=[-1,3] -> B*y=[1,2]")
    print("Reconstructed output S*B*y=[3,2], equal to direct swap(x)")
    print("Omitting output inverse gives reconstructed [5,2] (wrong)")
    print("Squared length: old=13, naive new=10, Gram-weighted new=13")
    print("Complex orthonormal basis: Q^H A Q=[[0,-i],[i,0]]")
    print("625 complex inputs match independent coordinate formulas.")
    print("Active/passive, adjoint/inverse, and dependent-column checks passed.")


if __name__ == "__main__":
    main()
