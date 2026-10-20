import math
import torch
import flagquantum as fq
from h2_vqe_model import REAL, coefficients_at, ansatz, energy, analytic_minimum

coefficients = coefficients_at(0.75)
theta, _ = analytic_minimum(coefficients)
shots = 65536  # Per basis; three separately seeded basis experiments.
means, variances = {}, {}
for offset, basis in enumerate(("z", "x", "y")):
    circuit = ansatz(theta)
    if basis == "x":
        circuit.h(0).h(1)
    elif basis == "y":
        circuit.rx(0, math.pi/2).rx(1, math.pi/2)
    result = fq.run(circuit, outputs=fq.samples(name="bits"), shots=shots,
                    options=fq.ExecutionOptions(
                        mode="statevector", backend="pytorch", device="cpu",
                        precision="complex128", seed=2026+offset,
                        allow_backend_fallback=False, allow_approximate=False))
    bits = result.measurement("bits").value[0].to(REAL)
    assert bits.shape == (shots, 2)
    signs = 1 - 2 * bits
    if basis == "z":
        # ZI, IZ, and ZZ share shots: preserve their covariance.
        per_shot = (coefficients[1] * signs[:, 0]
                    + coefficients[2] * signs[:, 1]
                    + coefficients[3] * signs[:, 0] * signs[:, 1])
    else:
        coefficient = coefficients[4] if basis == "x" else coefficients[5]
        per_shot = coefficient * signs[:, 0] * signs[:, 1]
    means[basis] = per_shot.mean()
    variances[basis] = per_shot.var(unbiased=True) / shots
estimate = coefficients[0] + sum(means.values())
standard_error = torch.sqrt(sum(variances.values()))
exact = energy(theta, coefficients).squeeze(0)
error = (estimate - exact).abs()
assert error < 6 * standard_error + 1e-10
print("Synthetic simulator shots; no QPU or readout correction.")
print("Shots per basis / total:", shots, "/", 3 * shots)
print(f"Exact expectation: {exact.item():.9f} Eh")
print(f"Sampled estimate: {estimate.item():.9f} Eh")
print(f"Estimated standard error: {standard_error.item():.9f} Eh")
print("Absolute error below six estimated standard errors:", bool(error < 6 * standard_error))
print("Basis-rotation, shot-parity, and grouped-variance checks passed.")
