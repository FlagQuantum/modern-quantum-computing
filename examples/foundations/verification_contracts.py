#!/usr/bin/env python3
"""Declared finite numerical contracts with exact binary references.

Python 3.12, PyTorch 2.13.0; CPU. No quantum execution.
"""
import argparse
from fractions import Fraction
import json
import math
import platform
import torch


def values(data, dtype=torch.float64):
    return torch.tensor(data, dtype=dtype, device="cpu")


def assert_finite_close(actual, expected, *, atol, rtol):
    """Exact metadata, finite entries, then a reference-scaled modulus bound.

    No implicit shape broadcasting, dtype conversion, or non-finite equality.
    """
    if not all(math.isfinite(t) and t >= 0 for t in (atol, rtol)):
        raise ValueError("Tolerances must be finite and nonnegative")
    if (actual.shape != expected.shape or actual.dtype != expected.dtype
            or actual.device != expected.device):
        raise AssertionError("Shape, dtype, and device must match")
    if (actual.layout != torch.strided or expected.layout != torch.strided
            or not (actual.is_floating_point() or actual.is_complex())):
        raise AssertionError("Dense floating or complex tensors are required")
    if not torch.isfinite(actual).all().item() or not torch.isfinite(expected).all().item():
        raise AssertionError("This contract requires finite entries")
    error = torch.abs(actual-expected)
    budget = atol+rtol*torch.abs(expected)
    if not torch.isfinite(error).all().item() or not torch.isfinite(budget).all().item():
        raise AssertionError("Comparison arithmetic exceeded its finite range")
    if not torch.all(error <= budget).item():
        raise AssertionError("Reference-scaled error budget exceeded")


def must_reject(actual, expected, *, atol=0.0, rtol=0.0):
    try:
        assert_finite_close(actual, expected, atol=atol, rtol=rtol)
    except AssertionError:
        return
    raise AssertionError("A deliberately invalid case was accepted")


def environment():
    return dict(python=platform.python_version(), torch=torch.__version__,
                system=platform.system(), architecture=platform.machine(), device="cpu",
                dtypes=["float32", "float64", "complex128"],
                deterministic_algorithms=torch.are_deterministic_algorithms_enabled())


def main():
    increment = Fraction(1, 2**25)
    low = (values(1, torch.float32)+values(float(increment), torch.float32))-values(1, torch.float32)
    high = (values(1)+values(float(increment)))-values(1)
    assert low.item() == 0 and Fraction.from_float(high.item()) == increment
    assert low.to(torch.float64).item() == 0  # Casting cannot restore discarded bits.
    big, one = values(2**25, torch.float32), values(1, torch.float32)
    left, right = (big+one)-big, (big-big)+one
    assert left.item() == 0 and right.item() == 1
    expected_tiny, missing_tiny = values([1e-12]), values([0.0])
    assert_finite_close(missing_tiny, expected_tiny, atol=1e-8, rtol=0)
    must_reject(missing_tiny, expected_tiny, atol=0, rtol=1e-6)
    assert_finite_close(values([5e-13]), values([0.0]), atol=1e-12, rtol=0)
    must_reject(values([5e-13]), values([0.0]), atol=0, rtol=1e-6)
    assert_finite_close(values([1+1e-10]), values([1.0]), atol=0, rtol=1e-9)
    must_reject(values([1+1e-10]), values([1.0]), atol=0, rtol=1e-12)
    # Relative budgets use expected as reference, so swapping roles can change the result.
    must_reject(values([2.0]), values([1.0]), atol=0, rtol=0.75)
    assert_finite_close(values([1.0]), values([2.0]), atol=0, rtol=0.75)
    flat, column = values([1, 1]), values([[1], [1]])
    assert torch.allclose(flat, column, atol=0, rtol=0)  # Broadcasts to an unintended 2x2 test.
    must_reject(flat, column)
    must_reject(values([1], torch.float32), values([1], torch.float64))
    must_reject(values([float("nan")]), values([0.0]), atol=1e-12)
    must_reject(values([float("inf")]), values([float("inf")]))
    # NaN > tolerance is false: merely searching for an oversized error is unsafe.
    assert not torch.any(torch.abs(values([float("nan")])-values([0.0])) > 1e-12).item()
    must_reject(values([1+1j], torch.complex128), values([0j], torch.complex128), atol=1.1)
    assert_finite_close(values([1+1j], torch.complex128), values([1+1j], torch.complex128), atol=0, rtol=0)
    delta = Fraction(1, 2**20)
    a = torch.diag(values([1, float(delta)], torch.complex128))
    b, exact, candidate = (values(v, torch.complex128) for v in ([1, 0], [1, 0], [1, 1]))
    residual = torch.linalg.vector_norm(b-a@candidate)
    assert_finite_close(residual, values(0.0), atol=1e-6, rtol=0)  # Loose residual test passes.
    forward = torch.linalg.vector_norm(candidate-exact).item()/torch.linalg.vector_norm(exact).item()
    assert forward == 1
    target_error = Fraction(1, 10**8)
    required_residual = target_error*delta  # ||b||=1, kappa=1/delta.
    must_reject(residual, values(0.0), atol=float(required_residual), rtol=0)
    assert_finite_close(torch.linalg.vector_norm(b-a@exact), values(0.0),
                        atol=float(required_residual), rtol=0)
    print("Declared CPU dtypes; exact references and finite verification contracts, no quantum execution.")
    print("Increment 2^-25: float32 loses it; float64 retains it; later casting does not restore it")
    print("Float32 operation order: (2^25+1)-2^25=0; (2^25-2^25)+1=1")
    print("Tiny 1e-12 signal: zero passes atol=1e-8, but fails the declared relative-only budget")
    print("Zero and order-one checks use different justified absolute/relative budgets")
    print("Expected-scaled comparison can change when actual and expected are swapped")
    print("Broadcasting allclose passes the wrong shape; strict metadata contract rejects it")
    print("Wrong dtype, NaN, Inf and complex-modulus counterexamples rejected")
    print("Residual below 1e-6 can accompany relative forward error=1")
    print(f"For target relative error 1e-8: conditioned absolute residual budget={float(required_residual):.9e}")
    print("All declared cases passed; this is not an all-input or cross-platform proof.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--environment", action="store_true", help="Print runtime metadata instead of cases")
    args = parser.parse_args()
    if args.environment:
        print(json.dumps(environment(), indent=2, sort_keys=True))
    else:
        main()
