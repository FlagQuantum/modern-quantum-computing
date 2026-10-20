"""Section 1.4: one task, independent reference, program and execution evidence.

The task is NOT(b) = 1-b for classical b in {0,1}. Runs local ideal simulation only.
No prerequisite interference model, remote provider, shots or physical qubit is used.
"""
from importlib.metadata import version

import flagquantum as fq
import torch

OPTIONS = fq.ExecutionOptions(
    mode="statevector", backend="pytorch", device="cpu", precision="complex128",
    allow_backend_fallback=False, allow_approximate=False,
)


def classical_not(bit):
    if type(bit) is not int or bit not in (0, 1):
        raise ValueError("The task input must be one integer bit.")
    return 1 - bit


def simulate(bit, *, apply_not=True):
    # Circuit starts at label 0. The optional first X encodes the classical input.
    circuit = fq.Circuit(1, dtype=torch.complex128)
    if bit == 1:
        circuit.x(0)  # Input preparation, not the computational NOT below.
    if apply_not:
        circuit.x(0)  # The algorithm's computational step.
    return fq.run(circuit, outputs=[fq.probabilities()], options=OPTIONS)


def main():
    assert version("flagquantum") == "0.3.1", "Revalidate before changing the pinned release."
    for bit in (0, 1):
        answer = classical_not(bit)
        # Independent probability table: input is certain label b; NOT swaps labels.
        before = [1-bit, bit]
        reference = torch.tensor([before[1], before[0]], dtype=torch.float64)
        result = simulate(bit)
        probabilities = result.probabilities
        assert tuple(probabilities.shape) == (1, 2)
        torch.testing.assert_close(probabilities[0], reference, rtol=0, atol=1e-12)
        assert abs(probabilities[0, answer].item() - 1.0) <= 1e-12
        assert result.samples is None  # No sampled data was requested or produced.
        assert result.runtime["mode"] == "statevector"
        assert result.runtime["execution_path"] == "local_statevector"
        assert result.runtime["simulation_engine"] == "pytorch_statevector"
        assert result.runtime["device"] == "cpu"
        assert result.provenance["selected_device"] == "cpu"
        assert result.provenance["cpu_fallback_used"] is False
        assert probabilities.device.type == "cpu"
        # Two falsifiable failure cases: omit the computational X, or relabel outputs.
        missing_gate = simulate(bit, apply_not=False).probabilities[0]
        assert not torch.allclose(missing_gate, reference, rtol=0, atol=1e-12)
        assert not torch.allclose(probabilities[0].flip(0), reference, rtol=0, atol=1e-12)
        print(f"input={bit}: classical answer={answer}; P(0)={probabilities[0, 0].item():.9f}, P(1)={probabilities[0, 1].item():.9f}")
    print(f"Reported execution: {result.runtime['execution_path']} / {result.runtime['simulation_engine']} / {result.runtime['device']}")
    print("Independent truth-table and simulator checks passed (atol=1e-12).")
    print("Missing-gate and swapped-label errors detected.")
    print("Physical-qubit execution: not performed. Sampled records: none.")


if __name__ == "__main__":
    main()
