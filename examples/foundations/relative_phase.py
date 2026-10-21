"""Section3.2: coherent relative-phase fringes in ideal one-qubit simulation.

No shots, intermediate measurements, hardware, noise or tomography claims.
Run with requirements-examples.txt, released FlagQuantum0.3.1.
"""
import cmath
from importlib.metadata import version
from math import cos, isclose, pi, sqrt

import flagquantum as fq
import torch

S = 1/sqrt(2)
ATOL = 1e-12
OPTIONS = fq.ExecutionOptions(
    mode="statevector", backend="pytorch", device="cpu", precision="complex128",
    allow_backend_fallback=False, allow_approximate=False,
)


def hadamard(a, b):
    # Standard-library complex arithmetic, separate from simulator matrices.
    return ((a+b)*S, (a-b)*S)


def probabilities(pair):
    return tuple(abs(x)**2 for x in pair)


def reference(phi, delta=0, recombine=True):
    pair = (complex(S), S*cmath.exp(1j*phi))
    if recombine:
        pair = hadamard(pair[0], cmath.exp(-1j*delta)*pair[1])
    return pair


def execute(phi, delta=0, recombine=True):
    circuit = fq.Circuit(1, dtype=torch.complex128)
    circuit.h(0)
    circuit.phase(0, theta=phi)
    if recombine:
        circuit.phase(0, theta=-delta)
        circuit.h(0)
    result = fq.run(circuit, outputs=[fq.probabilities()], options=OPTIONS)
    state, p = result.statevector(), result.probabilities
    assert state.shape == p.shape == (1, 2)
    assert state.dtype == torch.complex128 and p.dtype == torch.float64
    assert state.device.type == p.device.type == "cpu"
    assert torch.isfinite(state).all() and torch.isfinite(p).all()
    expected = reference(phi, delta, recombine)
    torch.testing.assert_close(state[0], torch.tensor(expected, dtype=torch.complex128), rtol=0, atol=ATOL)
    torch.testing.assert_close(p[0], torch.tensor(probabilities(expected), dtype=torch.float64), rtol=0, atol=ATOL)
    torch.testing.assert_close(p[0], state[0].abs().square(), rtol=0, atol=ATOL)
    assert isclose(p.sum().item(), 1, rel_tol=0, abs_tol=ATOL)
    if recombine:
        fringe = (.5*(1+cos(phi-delta)), .5*(1-cos(phi-delta)))
        torch.testing.assert_close(p[0], torch.tensor(fringe, dtype=torch.float64), rtol=0, atol=ATOL)
    return p[0].tolist()


def main():
    assert version("flagquantum") == "0.3.1"
    # Displayed hand-checkable phases; both paths refer to separate circuits.
    for phi in [0, pi/2, pi, 3*pi/2, 2*pi]:
        direct = execute(phi, recombine=False)
        after = execute(phi)
        print(f"phi/pi={phi/pi:.1f}: direct=({direct[0]:.9f}, {direct[1]:.9f}), after H=({after[0]:.9f}, {after[1]:.9f})")
    for label, phi in [("+i", pi/2), ("-i", -pi/2)]:
        plain, shifted = execute(phi), execute(phi, delta=pi/2)
        assert isclose(plain[0], .5, rel_tol=0, abs_tol=ATOL)
        target = 1 if label == "+i" else 0
        assert isclose(shifted[0], target, rel_tol=0, abs_tol=ATOL)
        print(f"{label} relative phase: P(0) after H={plain[0]:.9f}, shifted analyzer={shifted[0]:.9f}")

    # Non-cardinal cases catch angle/dtype/sign mistakes hidden by the table.
    for k in range(17):
        phi, delta = 2*pi*k/17, pi/7
        execute(phi, recombine=False)
        execute(phi, delta)
        alpha, beta = 3/5, (4/5)*cmath.exp(1j*phi)
        for analysis_phase in [0, pi/2, pi/7]:
            term = alpha.conjugate()*cmath.exp(-1j*analysis_phase)*beta
            actual = probabilities(hadamard(alpha, cmath.exp(-1j*analysis_phase)*beta))
            expected = (.5+term.real, .5-term.real)
            assert all(isclose(a,b,rel_tol=0,abs_tol=ATOL) for a,b in zip(actual,expected))
            assert isclose(expected[0], .5+(12/25)*cos(phi-analysis_phase), rel_tol=0, abs_tol=ATOL)
        # A common phase multiplies both amplitudes and leaves outputs unchanged.
        u = cmath.exp(.37j)
        assert all(isclose(a,b,rel_tol=0,abs_tol=ATOL) for a,b in zip(
            probabilities(hadamard(alpha,beta)), probabilities(hadamard(u*alpha,u*beta))))
        # With one path absent, changing its phase has no observable effect here.
        assert all(isclose(x,.5,rel_tol=0,abs_tol=ATOL) for x in probabilities(hadamard(0,cmath.exp(1j*phi))))
    print("17-point sweep: scalar amplitudes, analytic fringes and FlagQuantum agree (atol=1e-12).")
    print("Unbalanced fringe: min P(0)=0.020000000, max P(0)=0.980000000.")
    for phi,target in [(0,.98),(pi,.02)]:
        assert isclose(probabilities(hadamard(.6,.8*cmath.exp(1j*phi)))[0], target, rel_tol=0, abs_tol=ATOL)
    # A conjugation error is invisible for real alpha but fails for this case.
    alpha, beta = 1j*S, S
    correct = probabilities(hadamard(alpha, cmath.exp(-1j*pi/2)*beta))[0]
    wrong = .5+(alpha*cmath.exp(-1j*pi/2)*beta).real
    assert isclose(correct,0,rel_tol=0,abs_tol=ATOL)
    assert isclose(wrong,1,rel_tol=0,abs_tol=ATOL)
    # Reversing H then phase into phase then H on |0> loses the prepared phase.
    wrong_order = probabilities(hadamard(*hadamard(1,0)))
    assert isclose(wrong_order[0],1,rel_tol=0,abs_tol=ATOL)
    assert not isclose(wrong_order[0], probabilities(reference(pi))[0],rel_tol=0,abs_tol=ATOL)
    # Dropping the coherent cross term would predict .5 at every phase.
    assert not isclose(.5, probabilities(reference(0))[0],rel_tol=0,abs_tol=ATOL)
    print("Global-phase, absent-path, conjugation, operation-order and probability-only checks passed.")


if __name__ == "__main__":
    main()
