import torch
from h2_vqe_model import (
    REAL, COMPLEX, coefficients_at, expectations, energy,
    closed_energy, closed_gradient, dense_hamiltonian, analytic_minimum,
)

coefficients = coefficients_at(0.75)
hamiltonian = dense_hamiltonian(coefficients)
x = torch.tensor([[0, 1], [1, 0]], dtype=COMPLEX)
y = torch.tensor([[0, -1j], [1j, 0]], dtype=COMPLEX)
generator = torch.kron(x, y)
hf = torch.tensor([0, 0, 1, 0], dtype=COMPLEX)
for angle in (0.0, 0.13, -0.4, 0.9):
    theta = torch.tensor(angle, dtype=REAL, requires_grad=True)
    terms, result = expectations(theta)
    state = result.statevector()[0]
    zero = torch.zeros_like(theta)
    derived_state = torch.stack([zero, theta.sin(), theta.cos(), zero]).to(COMPLEX)
    matrix_state = torch.linalg.matrix_exp(-1j * theta * generator) @ hf
    torch.testing.assert_close(state, derived_state, rtol=1e-10, atol=1e-10)
    torch.testing.assert_close(state, matrix_state, rtol=1e-10, atol=1e-10)
    expected_terms = torch.stack([-(2*theta).cos(), (2*theta).cos(),
                                  -torch.ones_like(theta), (2*theta).sin(),
                                  (2*theta).sin()]).unsqueeze(0)
    torch.testing.assert_close(terms, expected_terms, rtol=1e-10, atol=1e-10)
    value = coefficients[0] + (terms * coefficients[1:]).sum()
    gradient, = torch.autograd.grad(value, theta)
    matrix_energy = torch.vdot(matrix_state, hamiltonian @ matrix_state).real
    matrix_gradient, = torch.autograd.grad(matrix_energy, theta)
    torch.testing.assert_close(value, closed_energy(theta, coefficients), rtol=1e-10, atol=1e-10)
    torch.testing.assert_close(value, matrix_energy, rtol=1e-10, atol=1e-10)
    torch.testing.assert_close(gradient, closed_gradient(theta, coefficients), rtol=1e-10, atol=1e-10)
    torch.testing.assert_close(gradient, matrix_gradient, rtol=1e-10, atol=1e-10)
    with torch.no_grad():
        # Generator eigenvalues are +/-1, not +/-1/2.
        shifted = (energy(theta + torch.pi/4, coefficients)
                   - energy(theta - torch.pi/4, coefficients)).squeeze(0)
    torch.testing.assert_close(gradient, shifted, rtol=1e-10, atol=1e-10)

theta_star, minimum = analytic_minimum(coefficients)
eigenvalues = torch.linalg.eigvalsh(hamiltonian)
torch.testing.assert_close(minimum, eigenvalues.min(), rtol=1e-10, atol=1e-10)
print("Checked 4 angles: state, matrix exponential, 5 Pauli terms, energy, gradients.")
print("Autograd, closed-form, dense-matrix, and parameter-shift gradients agree.")
print(f"Hartree-Fock energy at R=0.75: {closed_energy(torch.tensor(0.0, dtype=REAL), coefficients).item():.9f} Eh")
print(f"Analytical theta*: {theta_star.item():.9f} rad")
print(f"Exact ground energy at R=0.75: {minimum.item():.9f} Eh")
print("All identity, sign, ordering, and gradient checks passed.")
