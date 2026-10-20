"""Section 1.2: real-amplitude interference, independent arithmetic and FlagQuantum.

Ideal statevector probabilities only: no intermediate measurement, shots or hardware.
Run with the repository's requirements-examples.txt (FlagQuantum 0.3.1).
"""
from importlib.metadata import version
from math import isclose, sqrt

import flagquantum as fq
import torch

S = 1 / sqrt(2)
H = [[S, S], [S, -S]]
Z = [[1.0, 0.0], [0.0, -1.0]]
OPTIONS = fq.ExecutionOptions(
    mode="statevector", backend="pytorch", device="cpu", precision="complex128",
    allow_backend_fallback=False, allow_approximate=False,
)


def apply(matrix, pair):
    # Row 0 produces the new outcome-0 amplitude; row 1 produces outcome 1.
    return [sum(matrix[row][column] * pair[column] for column in range(2))
            for row in range(2)]


def reference(gates):
    pair = [1.0, 0.0]
    for gate in gates:
        pair = apply(H if gate == "h" else Z, pair)
    return pair


def main():
    assert version("flagquantum") == "0.3.1", "Revalidate before changing the pinned release."
    cases = [
        ("H", ["h"], [S, S], [0.5, 0.5]),
        ("H then H", ["h", "h"], [1.0, 0.0], [1.0, 0.0]),
        ("H then Z", ["h", "z"], [S, -S], [0.5, 0.5]),
        ("H then Z then H", ["h", "z", "h"], [0.0, 1.0], [0.0, 1.0]),
    ]
    for label, gates, hand_pair, hand_probabilities in cases:
        pair = reference(gates)
        assert all(isclose(a, b, rel_tol=0, abs_tol=1e-12)
                   for a, b in zip(pair, hand_pair))
        assert isclose(sum(a*a for a in pair), 1, rel_tol=0, abs_tol=1e-12)
        circuit = fq.Circuit(1, dtype=torch.complex128)  # Starts in outcome-0 state.
        for gate in gates:
            if gate == "h":
                circuit.h(0)
            else:
                circuit.z(0)
        result = fq.run(circuit, outputs=[fq.probabilities()], options=OPTIONS)
        state = result.statevector()  # Simulator diagnostic, not physical readout.
        probabilities = result.probabilities
        assert tuple(state.shape) == tuple(probabilities.shape) == (1, 2)
        torch.testing.assert_close(state[0], torch.tensor(pair, dtype=torch.complex128),
                                   rtol=0, atol=1e-12)
        torch.testing.assert_close(probabilities[0], torch.tensor(hand_probabilities, dtype=torch.float64),
                                   rtol=0, atol=1e-12)
        torch.testing.assert_close(probabilities[0], state[0].abs().square(), rtol=0, atol=1e-12)
        print(f"{label}: P(0)={probabilities[0, 0].item():.9f}, P(1)={probabilities[0, 1].item():.9f}")

    # The probability-only mistake: treat the first H as an incoherent coin toss.
    wrong_probabilities = [0.5*0.5 + 0.5*0.5, 0.5*0.5 + 0.5*0.5]
    assert wrong_probabilities != cases[1][3]
    # Check the omitted cross term for a real normalized pair, independently.
    a, b = 3/5, 4/5
    recombined = apply(H, [a, b])
    p0_with_interference = (a*a + b*b)/2 + a*b
    assert isclose(recombined[0]**2, p0_with_interference, abs_tol=1e-12)
    assert not isclose(recombined[0]**2, (a*a + b*b)/2, abs_tol=1e-12)
    # Transfer: H twice returns either supplied basis input to itself.
    for basis in ([1.0, 0.0], [0.0, 1.0]):
        assert all(isclose(a, b, abs_tol=1e-12) for a, b in zip(apply(H, apply(H, basis)), basis))
    print("Probability-only recombination: P(0)=0.500000000, P(1)=0.500000000 (wrong for H then H)")
    print("Hand arithmetic, independent matrices, and FlagQuantum agree (atol=1e-12).")


if __name__ == "__main__":
    main()
