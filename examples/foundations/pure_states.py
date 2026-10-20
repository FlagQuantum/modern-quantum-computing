"""Section3.1: pure-state conventions, not a hardware measurement experiment.

Global phase below multiplies diagnostic arrays; no global-phase gate is claimed.
"""
from importlib.metadata import version
from math import isclose, sqrt

import flagquantum as fq
import torch

DTYPE = torch.complex128
ATOL = 1e-12
OPTIONS = fq.ExecutionOptions(
    mode="statevector", backend="pytorch", device="cpu", precision="complex128",
    allow_backend_fallback=False, allow_approximate=False,
)


def unit_qubit(v):
    """Validate a finite CPU complex128 unit vector; do not silently normalize."""
    if not isinstance(v, torch.Tensor) or v.shape != (2,):
        raise ValueError("Expected a two-coordinate tensor")
    if v.dtype != DTYPE or v.device.type != "cpu" or v.layout != torch.strided:
        raise ValueError("Expected dense CPU complex128")
    if not torch.isfinite(v).all().item():
        raise ValueError("Nonfinite coordinates")
    if not isclose(torch.vdot(v, v).real.item(), 1, rel_tol=0, abs_tol=ATOL):
        raise ValueError("Expected unit norm")
    return v


def aligned_distance(a, b):
    """Return minimum phase-aligned Euclidean distance, including zero overlap."""
    unit_qubit(a)
    unit_qubit(b)
    c = torch.vdot(a, b)
    # At exactly zero overlap every phase gives distance sqrt(2).
    # Picking phase1 is only a convention; it is not evidence of equivalence.
    phase = c.conj() / c.abs() if c.abs().item() != 0 else 1.0
    return torch.linalg.vector_norm(a - phase * b).item()


def reference_overlap(a, b):
    # Independent scalar arithmetic: no torch.vdot or phase helper.
    return sum(x.conjugate() * y for x, y in zip(a, b))


def rejected(v):
    try:
        unit_qubit(v)
    except ValueError:
        return True
    return False


def main():
    assert version("flagquantum") == "0.3.1"
    s = 1 / sqrt(2)
    a = torch.tensor([s, 1j*s], dtype=DTYPE)
    b = 1j * a
    d = torch.tensor([s, -1j*s], dtype=DTYPE)
    for v in (a, b, d):
        unit_qubit(v)
        torch.testing.assert_close(v.abs().square(), torch.tensor([.5, .5], dtype=torch.float64), rtol=0, atol=ATOL)
    torch.testing.assert_close(torch.vdot(a, b), torch.tensor(1j, dtype=DTYPE), rtol=0, atol=ATOL)
    assert abs(reference_overlap([s, 1j*s], [1j*s, -s]) - 1j) < ATOL
    assert abs(reference_overlap([s, 1j*s], [s, -1j*s])) < ATOL
    assert isclose(torch.linalg.vector_norm(a-b).item(), sqrt(2), rel_tol=0, abs_tol=ATOL)
    assert aligned_distance(a, b) < ATOL
    assert isclose(aligned_distance(a, d), sqrt(2), rel_tol=0, abs_tol=ATOL)
    # Wrong conjugation aligns i*a to -a, giving distance2.
    c = torch.vdot(a, b)
    assert isclose(torch.linalg.vector_norm(a-c/c.abs()*b).item(), 2, rel_tol=0, abs_tol=ATOL)
    print("complex example: P(0)=0.500000000, P(1)=0.500000000")
    print(f"global i: raw distance={torch.linalg.vector_norm(a-b).item():.9f}, aligned distance={aligned_distance(a,b):.9f}")
    print(f"relative sign: same probabilities, aligned distance={aligned_distance(a,d):.9f}")

    for label, change_sign, expected in [("H", False, [s, s]), ("H then Z", True, [s, -s])]:
        circuit = fq.Circuit(1, dtype=DTYPE)
        circuit.h(0)
        if change_sign:
            circuit.z(0)
        result = fq.run(circuit, outputs=[fq.probabilities()], options=OPTIONS)
        state = result.statevector()
        assert state.shape == result.probabilities.shape == (1, 2)
        v = unit_qubit(state[0])
        torch.testing.assert_close(v, torch.tensor(expected, dtype=DTYPE), rtol=0, atol=ATOL)
        torch.testing.assert_close(result.probabilities[0], torch.tensor([.5, .5], dtype=torch.float64), rtol=0, atol=ATOL)
        torch.testing.assert_close(result.probabilities[0], v.abs().square(), rtol=0, atol=ATOL)
        assert aligned_distance(v, 1j*v) < ATOL
        print(f"FlagQuantum {label}: P(0)={result.probabilities[0,0].item():.9f}, P(1)={result.probabilities[0,1].item():.9f}")

    # Unequal-probability reference and an explicit zero-overlap branch.
    u = unit_qubit(torch.tensor([sqrt(3)/2, .5j], dtype=DTYPE))
    torch.testing.assert_close(u.abs().square(), torch.tensor([.75, .25], dtype=torch.float64), rtol=0, atol=ATOL)
    e0, e1 = torch.tensor([1, 0], dtype=DTYPE), torch.tensor([0, 1], dtype=DTYPE)
    assert isclose(aligned_distance(e0, e1), sqrt(2), rel_tol=0, abs_tol=ATOL)
    bad = [torch.zeros(2, dtype=DTYPE), 2*a, a.reshape(1, 2), a.to(torch.complex64),
           torch.tensor([float("nan"), 0], dtype=DTYPE), torch.tensor([float("inf"), 0], dtype=DTYPE)]
    assert all(rejected(v) for v in bad)
    print("Unequal probabilities, zero overlap, and 6 invalid-input cases checked.")
    print("Scalar references and released FlagQuantum agree (atol=1e-12); no shots or hardware.")


if __name__ == "__main__":
    main()
