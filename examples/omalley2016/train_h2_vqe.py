import torch
from h2_vqe_model import REAL, coefficients_at, energy, dense_hamiltonian

theta = torch.nn.Parameter(torch.tensor(0.2, dtype=REAL))
coefficients = coefficients_at(0.75)
optimizer = torch.optim.Adam([theta], lr=0.05)
initial = energy(theta, coefficients).item()
for _ in range(300):
    optimizer.zero_grad(set_to_none=True)
    loss = energy(theta, coefficients).mean()
    loss.backward()
    optimizer.step()

with torch.no_grad():
    final = energy(theta, coefficients).squeeze(0)
    exact = torch.linalg.eigvalsh(dense_hamiltonian(coefficients)).min()
    gap = (final - exact).item()
    assert -1e-10 <= gap < 1e-9
    print("Optimizer: Adam (tutorial extension; not the paper's 1000-angle scan)")
    print(f"Initial energy: {initial:.9f} Eh")
    print(f"Trained theta: {theta.item():.9f} rad")
    print(f"Post-update energy: {final.item():.9f} Eh")
    print(f"Exact reference: {exact.item():.9f} Eh")
    print("Energy gap below 1e-9 Eh:", abs(gap) < 1e-9)
    print("Differentiable VQE training checks passed.")
