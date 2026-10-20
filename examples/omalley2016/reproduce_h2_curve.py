import csv
import json
from pathlib import Path
import platform
import torch
import flagquantum as fq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from h2_vqe_model import REAL, TABLE, DATA_SHA256, expectations, dense_hamiltonian

output = Path("vqe-results")
output.mkdir(exist_ok=True)
angles = -torch.pi + torch.arange(1000, dtype=REAL) * (2 * torch.pi / 1000)
with torch.no_grad():
    terms, _ = expectations(angles)
    # Reuse the same five expectation curves across all 54 bond lengths.
    energies = terms @ TABLE[:, 2:].T + TABLE[:, 1]
    minimum, indices = energies.min(dim=0)
    exact = torch.stack([torch.linalg.eigvalsh(dense_hamiltonian(row[1:])).min()
                         for row in TABLE])
    gaps = minimum - exact
    A, D = TABLE[:, 3] - TABLE[:, 2], TABLE[:, 5] + TABLE[:, 6]
    amplitude = torch.sqrt(A.square() + D.square())
    grid_bound = amplitude * (1 - torch.cos(torch.tensor(2 * torch.pi / 1000, dtype=REAL)))
    assert bool((gaps >= -1e-10).all())
    assert bool((gaps <= grid_bound + 1e-10).all())
    assert gaps.max().item() < 1.6e-3
    analytical = (TABLE[:, 1] - TABLE[:, 4])[None, :] + (
        (2*angles).cos()[:, None] * A[None, :]
        + (2*angles).sin()[:, None] * D[None, :])
    torch.testing.assert_close(energies, analytical, rtol=1e-10, atol=1e-10)

with (output / "h2-curve.csv").open("w", newline="") as stream:
    writer = csv.writer(stream)
    writer.writerow(["R_angstrom", "exact_Eh", "grid_Eh", "grid_error_Eh", "theta_rad"])
    for row, ref, value, gap, index in zip(TABLE, exact, minimum, gaps, indices):
        writer.writerow([row[0].item(), ref.item(), value.item(), gap.item(), angles[index].item()])
(output / "manifest.json").write_text(json.dumps({
    "paper": "arXiv:1512.06860v2", "table": "Table I", "csv_sha256": DATA_SHA256,
    "flagquantum": fq.__version__, "torch": torch.__version__,
    "python": platform.python_version(), "matplotlib": matplotlib.__version__,
    "platform": platform.platform(), "device": "cpu", "precision": "complex128",
    "angle_points": 1000, "geometry_points": 54, "shots": None,
    "hardware_measurements": False,
}, indent=2) + "\n")
fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True,
                         gridspec_kw={"height_ratios": [2, 1]}, constrained_layout=True)
x = TABLE[:, 0].numpy()
axes[0].plot(x, exact.numpy(), color="#163b65", label="Dense exact reference")
axes[0].plot(x, minimum.numpy(), ".", color="#da6c24", label="FlagQuantum: 1000-angle VQE scan")
axes[0].set_ylabel("Total energy (hartree)")
axes[0].legend(loc="best", fontsize=8)
axes[0].set_title("H2 VQE: O'Malley et al. (2016), corrected arXiv v2 Table I\nNoiseless CPU statevector reproduction")
axes[1].plot(x, gaps.numpy(), color="#da6c24", label="Grid error")
axes[1].plot(x, grid_bound.numpy(), "--", color="#163b65", label="Derived grid error bound")
axes[1].set_ylabel("Energy error (hartree)")
axes[1].set_xlabel("Bond length (angstrom)")
axes[1].ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
axes[1].legend(loc="best", fontsize=8)
for axis in axes:
    axis.grid(alpha=0.2)
fig.savefig(output / "h2-vqe-curve.png", dpi=180)
plt.close(fig)
print("Geometry points:", len(TABLE))
print("Angles per geometry:", len(angles))
for index in (1, 11, 26, 36, 53):
    print(f"R={TABLE[index, 0].item():.2f} A: exact={exact[index].item():.9f}, scan={minimum[index].item():.9f} Eh")
print(f"Maximum grid error: {gaps.max().item():.9f} Eh")
print("All 54 grid errors satisfy the derived bound and are below 0.0016 Eh.")
print("Saved vqe-results/h2-curve.csv, manifest.json, h2-vqe-curve.png")
