import torch
import flagquantum as fq

phi = torch.tensor(0.6, dtype=torch.float64)
circuit = fq.Circuit(1, dtype=torch.complex128).ry(0, phi)
options = fq.ExecutionOptions(mode="statevector", backend="pytorch", device="cpu",
    precision="complex128", allow_backend_fallback=False, allow_approximate=False)
result = fq.run(circuit, outputs=[fq.expectation(fq.Z(0), name="z"), fq.probabilities()], options=options)
actual = result.expectation("z").squeeze(0)
probabilities = result.probabilities[0]
expected_probabilities = torch.stack([torch.cos(phi/2)**2, torch.sin(phi/2)**2])
torch.testing.assert_close(probabilities, expected_probabilities, rtol=1e-10, atol=1e-10)
torch.testing.assert_close(actual, torch.cos(phi), rtol=1e-10, atol=1e-10)
torch.testing.assert_close(actual, probabilities[0]-probabilities[1], rtol=1e-10, atol=1e-10)
print(f"P(0) = {probabilities[0].item():.9f}")
print(f"P(1) = {probabilities[1].item():.9f}")
print(f"<Z>  = {actual.item():.9f}")
print("Analytic and FlagQuantum results agree.")
