#!/usr/bin/env python3
"""Condition-dependent errors with exact diagonal/Fraction references.

Python 3.12, PyTorch 2.13.0; CPU complex128. No quantum execution.
"""
from fractions import Fraction
import torch


def tensor(values):
    return torch.as_tensor(values, dtype=torch.complex128, device="cpu")


def check(actual, expected):
    torch.testing.assert_close(tensor(actual), tensor(expected), rtol=0, atol=1e-12)


def op(matrix):
    return torch.linalg.matrix_norm(matrix, ord=2).item()


def length(vector):
    return torch.linalg.vector_norm(vector).item()


def main():
    b, exact, candidate = tensor([1, 0]), tensor([1, 0]), tensor([1, 1])
    print("CPU complex128; constructed sensitivity cases, not observed solver failures.")
    for exponent in (4, 12, 20):
        delta = Fraction(1, 2**exponent)
        a = torch.diag(tensor([1, float(delta)]))
        inverse = torch.diag(tensor([1, float(1/delta)]))
        check(torch.linalg.solve(a, b), exact)
        residual = b-a@candidate
        check(residual, [0, -float(delta)])
        relative_residual = length(residual)/length(b)
        relative_error = length(candidate-exact)/length(exact)
        condition = op(a)*op(inverse)
        check(condition, float(1/delta))
        check(relative_residual, float(delta))
        check(relative_error, 1)
        check(condition*relative_residual, relative_error)  # Tight bound here.
        # Candidate is the exact solution of a nearby right-hand side.
        check(torch.linalg.solve(a, b-residual), candidate)
        print(f"delta=2^-{exponent}: kappa={int(condition)}; "
              f"relative residual={relative_residual:.9e}; relative error={relative_error:.1f}")
    delta = Fraction(1, 2**20)
    a = torch.diag(tensor([1, float(delta)]))
    e = torch.diag(tensor([0, -float(delta/2)]))
    f = tensor([0, float(delta)])
    changed_solution = torch.linalg.solve(a+e, b+f)
    check(changed_solution, [1, 2])
    eta = Fraction(1, 2)
    eps_a, eps_b, kappa = delta/2, delta, 1/delta
    bound = kappa*(eps_a+eps_b)/(1-kappa*eps_a)
    assert bound == 3 and kappa*eps_a == eta
    assert length(changed_solution-exact)/length(exact) == 2
    check(op(torch.diag(tensor([1, float(1/delta)])))*op(e), float(eta))
    # At eta=1 this specific matrix becomes singular: the smallness test is sufficient.
    critical = a+torch.diag(tensor([0, -float(delta)]))
    check(critical@tensor([0, 1]), [0, 0])
    # Small absolute singular values alone need not give a large relative condition.
    scaled_identity = float(delta)*torch.eye(2, dtype=torch.complex128)
    check(torch.linalg.cond(scaled_identity, p=2), 1)
    check(op(torch.eye(2, dtype=torch.complex128)), 1)
    check(torch.linalg.matrix_norm(torch.eye(2, dtype=torch.complex128), ord="fro"), 2**0.5)
    # Nontrivial matrix-vector/product bounds, independently reconstructed components.
    m = tensor([[1, 1j], [0, 1]])
    n = tensor([[2, 0], [1, 1j]])
    check(m@n, [[2+1j, -1], [1, 1j]])
    assert op(m@n) <= op(m)*op(n)+1e-12
    x, dx = tensor([1, 1j]), tensor([0, 0.25])
    dm = tensor([[0.125, 0], [0, 0]])
    difference = (m+dm)@(x+dx)-m@x
    check(difference, m@dx+dm@x+dm@dx)
    assert length(difference) <= op(m)*length(dx)+op(dm)*(length(x)+length(dx))+1e-12
    print("Combined perturbation: eta=1/2; relative solution change=2; proven bound=3")
    print("Specific eta=1 perturbation is singular; zero direction checked")
    print("Uniformly scaled identity: kappa=1 despite small singular values")
    print("Identity norms: operator=1, Frobenius=sqrt(2) (different conventions)")
    print("Exact references, nearby solves, submultiplicativity and perturbation checks passed.")


if __name__ == "__main__":
    main()
