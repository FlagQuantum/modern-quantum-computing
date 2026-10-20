#!/usr/bin/env python3
"""Matrix functions checked with independent scalar phases and Python series.

Python 3.12, PyTorch 2.13.0; CPU complex128. Dimensionless constant generator.
"""
import cmath
from fractions import Fraction
import math
import torch


def tensor(values):
    return torch.as_tensor(values, dtype=torch.complex128, device="cpu")


def check(actual, expected):
    torch.testing.assert_close(tensor(actual), tensor(expected), rtol=0, atol=1e-12)


def multiply(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)]
            for i in range(2)]


def series_exponential(matrix, order=40):
    """Independent Python lists; no tensor exponential or spectral routine."""
    term = [[1+0j, 0j], [0j, 1+0j]]
    total = [row[:] for row in term]
    for k in range(1, order+1):
        product = multiply(term, matrix)
        term = [[value/k for value in row] for row in product]
        total = [[total[i][j]+term[i][j] for j in range(2)] for i in range(2)]
    return total


def analytic_evolution(t):
    a, b = cmath.exp(-1j*t), cmath.exp(-3j*t)
    return [[(a+b)/2, -1j*(a-b)/2], [1j*(a-b)/2, (a+b)/2]]


def main():
    h = tensor([[2, 1j], [-1j, 2]])
    identity = torch.eye(2, dtype=torch.complex128)
    q = tensor([[1, 1], [1j, -1j]])/math.sqrt(2)
    eigenvalues = tensor([1, 3])
    root = q@torch.diag(torch.sqrt(eigenvalues))@q.mH
    inverse = q@torch.diag(1/eigenvalues)@q.mH
    check(root@root, h)
    check(inverse@h, identity)
    # g(x)=(x-2)^2 merges both eigenvalues to 1; f(x)=exp(x).
    g_h = (h-2*identity)@(h-2*identity)
    check(g_h, identity)
    check(torch.linalg.matrix_exp(g_h), math.e*identity)
    times = (-1.0, -0.4, 0.0, 0.4, 1.0)
    order = 40
    for t in times:
        matrix = [[-2j*t, t], [-t, -2j*t]]  # -i*t*H, explicit coordinates.
        direct = torch.linalg.matrix_exp(-1j*t*h)
        spectral = q@torch.diag(torch.exp(-1j*t*eigenvalues))@q.mH
        check(direct, analytic_evolution(t))
        check(spectral, analytic_evolution(t))
        check(series_exponential(matrix, order), analytic_evolution(t))
        check(direct.mH@direct, identity)
        check(torch.linalg.matrix_exp(1j*t*h), direct.mH)
    # Absolute tail bound for each entry; this excludes floating-point roundoff.
    b = 4  # n * max-entry modulus of -i*t*H, for |t|<=1.
    rho = Fraction(b, order+2)
    tail = Fraction(b**(order+1), math.factorial(order+1))/(1-rho)
    assert tail < Fraction(2, 10**25)
    s, t = 0.25, 0.4
    us = torch.linalg.matrix_exp(-1j*s*h)
    ut = torch.linalg.matrix_exp(-1j*t*h)
    check(torch.linalg.matrix_exp(-1j*(s+t)*h), us@ut)
    v = tensor([1, 1j])/math.sqrt(2)
    check(torch.vdot(ut@v, ut@v), 1)
    first_order = identity-1j*t*h
    check(first_order.mH@first_order, identity+t*t*(h@h))
    assert not torch.allclose(first_order.mH@first_order, identity)
    assert not torch.allclose(torch.exp(-1j*t*h), ut)  # Entrywise is a different operation.
    nonhermitian = torch.diag(tensor([1, 1j]))
    bad = torch.linalg.matrix_exp(-1j*t*nonhermitian)
    check(bad, torch.diag(tensor([cmath.exp(-1j*t), math.exp(t)])))
    assert not torch.allclose(bad.mH@bad, identity)
    other = torch.diag(tensor([1, -1]))
    assert not torch.allclose(torch.linalg.matrix_exp(-1j*t*(h+other)),
                              ut@torch.linalg.matrix_exp(-1j*t*other))
    z = analytic_evolution(0.4)[0][0]
    print("CPU complex128; dimensionless constant Hermitian generator, no physical execution.")
    print("Square root squared equals H; reciprocal times H equals identity")
    print("Merged-spectrum composition: exp((H-2I)^2)=e*I")
    print("5 real times: scalar phases, Python series and tensor matrix exponential agree")
    print(f"At t=0.4: U[0,0]={z.real:.9f}{z.imag:+.9f}j")
    print("Order-40 series: per-entry mathematical tail < 2.0e-25 for |t|<=1")
    print("Adjoint, group and unit-norm checks passed; first-order Taylor is not unitary")
    print("Entrywise exponential, non-Hermitian norm preservation and unrelated-generator product refuted")


if __name__ == "__main__":
    main()
