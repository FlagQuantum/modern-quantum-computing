#!/usr/bin/env python3
"""CPU complex128 inner products checked with integer-coordinate arithmetic.

Python 3.12 and PyTorch 2.13.0. No quantum backend or device experiment.
"""
from itertools import product
import torch

DTYPE = torch.complex128


def tensor(values):
    return torch.as_tensor(values, dtype=DTYPE, device="cpu")


def pair_inner(v, w):
    """Independent (real,imaginary) expansion of sum(conjugate(v_k)*w_k)."""
    real = imag = 0
    for (a, b), (c, d) in zip(v, w):
        real += a*c + b*d
        imag += a*d - b*c
    return complex(real, imag)


def check(actual, expected):
    torch.testing.assert_close(tensor(actual), tensor(expected), rtol=0, atol=1e-12)


def projection(axis, vector):
    denominator = torch.vdot(axis, axis)
    if denominator.item() == 0:
        raise ValueError("Projection axis must be nonzero")
    return axis * (torch.vdot(axis, vector) / denominator)


def main():
    pairs = list(product((-1, 0, 1), repeat=2))
    coordinates = list(product(pairs, repeat=2))
    vectors = [tensor([complex(*z) for z in row]) for row in coordinates]
    for v_pair, v in zip(coordinates, vectors):
        for w_pair, w in zip(coordinates, vectors):
            value = torch.vdot(v, w)
            check(value, pair_inner(v_pair, w_pair))
            check(torch.vdot(w, v).conj(), value)
            left = abs(value.item())**2
            right = torch.vdot(v, v).real.item()*torch.vdot(w, w).real.item()
            assert left <= right + 1e-12
    axis, v = tensor([1, 1j]), tensor([2, 1+1j])
    overlap = torch.vdot(axis, v)
    p = projection(axis, v)
    residual = v-p
    check(overlap, 3-1j)
    check(p, [1.5-0.5j, 0.5+1.5j])
    check(residual, [0.5+0.5j, 0.5-0.5j])
    check(torch.vdot(axis, residual), 0)
    check(torch.vdot(v, v), 6)
    check(torch.vdot(p, p), 5)
    check(torch.vdot(residual, residual), 1)
    unit = axis/torch.sqrt(torch.vdot(axis, axis).real)
    check(torch.vdot(unit, unit), 1)
    check(unit*torch.vdot(unit, v), p)
    # Equality and zero cases in Cauchy-Schwarz; zero cannot be a projection axis.
    parallel = (2-1j)*axis
    check(abs(torch.vdot(axis, parallel))**2,
          torch.vdot(axis, axis).real*torch.vdot(parallel, parallel).real)
    zero = torch.zeros_like(axis)
    check(torch.vdot(zero, v), 0)
    try:
        projection(zero, v)
    except ValueError:
        pass
    else:
        raise AssertionError("Zero projection axis accepted")
    # Transposition alone is not an adjoint.
    matrix = tensor([[1, 1j], [2-1j, 3]])
    check(matrix.mH, [[1, 2+1j], [-1j, 3]])
    check(torch.vdot(axis, matrix@v), 2-6j)
    check(torch.vdot(matrix.mH@axis, v), 2-6j)
    assert not torch.isclose(torch.vdot(matrix.T@axis, v), tensor(2-6j))
    check(torch.dot(axis, axis), 0)  # Wrong positive-length rule.
    check(torch.vdot(axis, axis), 2)
    assert axis.conj().shape == axis.shape == (2,)
    assert axis[:, None].mH.shape == (1, 2)
    print("Tensor execution: CPU, complex128; no quantum backend.")
    print("<a,v>=3-1j; squared norms a=2, v=6; Cauchy-Schwarz: 10 <= 12")
    print("Projection=[1.5-0.5j, 0.5+1.5j]; residual=[0.5+0.5j, 0.5-0.5j]")
    print("<a,residual>=0; squared norms: 6 = 5 + 1")
    print("Adjoint check: <a,A v> = <A^H a,v> = 2-6j")
    print("Bilinear dot(a,a)=0 is wrong for length; vdot(a,a)=2")
    print("81 vectors / 6561 ordered inner products match integer-pair references.")
    print("Projection, normalization, equality, zero-axis, and conjugation checks passed.")


if __name__ == "__main__":
    main()
