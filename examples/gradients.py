import torch
import flagquantum as fq

options = fq.ExecutionOptions(mode="statevector", backend="pytorch", device="cpu",
    precision="complex128", allow_backend_fallback=False, allow_approximate=False)

def expectation(phi):
    circuit = fq.Circuit(1, dtype=torch.complex128).ry(0, phi)
    return fq.run(circuit, outputs=[fq.expectation(fq.Z(0), name="z")], options=options).expectation("z").squeeze(0)

phi = torch.tensor(0.6, dtype=torch.float64, requires_grad=True)
value = expectation(phi)
gradient, = torch.autograd.grad(value, phi)
with torch.no_grad():
    shifted = (expectation(phi+torch.pi/2)-expectation(phi-torch.pi/2))/2
    finite_difference = (expectation(phi+1e-5)-expectation(phi-1e-5))/(2e-5)
torch.testing.assert_close(gradient, -torch.sin(phi), rtol=1e-10, atol=1e-10)
torch.testing.assert_close(gradient, shifted, rtol=1e-10, atol=1e-10)
torch.testing.assert_close(gradient, finite_difference, rtol=1e-8, atol=1e-8)
print(f"<Z> = {value.item():.9f}")
print(f"d<Z>/dphi = {gradient.item():.9f}")
print("Autograd, analytic, parameter-shift, and finite-difference gradients agree.")
