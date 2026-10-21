"""5.7: exact references, finite-word teaching search and separate error budgets.

The bounded exhaustive search is not a Solovay-Kitaev compiler or a density proof.
"""
import math
from functools import lru_cache
from itertools import product
from importlib.metadata import version
import torch
import flagquantum as fq
try:
    from examples.foundations.pauli_rotations import explicit
    from examples.foundations.circuit_composition import execute, product_input
except ModuleNotFoundError:
    from pauli_rotations import explicit
    from circuit_composition import execute, product_input
D = torch.complex128
I = torch.eye(2, dtype=D)
ATOL = 1e-12
ALPHABET = (('x', 1), ('x', -1), ('z', 1), ('z', -1))
RUNS = 0


def unitary(U, special=False):
    if not isinstance(U, torch.Tensor) or U.shape != (2, 2) or U.dtype != D or U.device.type != 'cpu' or not torch.isfinite(U).all():
        raise ValueError('Finite 2x2 CPU complex128 matrix required')
    if not torch.allclose(U.mH @ U, I, rtol=0, atol=ATOL):
        raise ValueError('Unitary input required; no projection or repair')
    if special and abs(torch.linalg.det(U).item()-1) > ATOL:
        raise ValueError('Declared SU(2) input required; retain U(2) phase separately')


def distance(U, V):
    unitary(U); unitary(V)
    return torch.linalg.svdvals(U-V).max().item()


def strip_phase(U):
    unitary(U)
    chi = torch.angle(torch.linalg.det(U)).item()/2
    V = torch.exp(torch.tensor(-1j*chi, dtype=D))*U
    unitary(V, special=True)
    return chi, V


def quantized_angle(theta, bits):
    if type(theta) not in (int, float) or not math.isfinite(theta) or abs(theta) > 100:
        raise ValueError('Finite literal radian angle with absolute value <=100 required')
    if type(bits) is not int or not 1 <= bits <= 20:
        raise ValueError('Teaching angle grid uses 1 through 20 bits')
    h = 4*math.pi/(2**bits)
    return round(theta/h)*h, h


def check_word(word):
    if not isinstance(word, tuple) or any(not isinstance(g, tuple) or len(g) != 2 or type(g[1]) is not int or g not in ALPHABET for g in word):
        raise ValueError('Chronological tuple of declared (axis, +/-1) instructions required')


def word_matrix(word):
    check_word(word)
    U = I.clone()
    for axis, sign in word:
        U = explicit(axis, sign*math.pi/4) @ U
    return U


def inverse_word(word):
    check_word(word)
    return tuple((axis, -sign) for axis, sign in reversed(word))


def word_circuit(word):
    check_word(word)
    circuit = fq.Circuit(1, dtype=D)
    for axis, sign in word:
        getattr(circuit, 'r'+axis)(0, sign*math.pi/4)
    return circuit


@lru_cache(maxsize=7)
def catalog(depth):
    if type(depth) is not int or not 0 <= depth <= 6:
        raise ValueError('Teaching exhaustive search depth is 0 through 6')
    words = [()]
    for length in range(1, depth+1):
        words.extend(product(ALPHABET, repeat=length))
    matrices = torch.stack([word_matrix(w) for w in words])
    return tuple(words), matrices


def search(U, depth):
    unitary(U, special=True)
    words, matrices = catalog(depth)
    errors = torch.linalg.svdvals(matrices-U).amax(dim=-1)
    index = int(errors.argmin())
    return words[index], matrices[index].clone(), errors[index].item(), len(words)


def commutator(V, W):
    unitary(V, special=True); unitary(W, special=True)
    return V @ W @ V.mH @ W.mH


def run(circuit, factors):
    global RUNS
    v, p = execute(circuit, factors); RUNS += 1
    return v, p


def main():
    assert version('flagquantum') == '0.3.1' and version('torch').split('+')[0] == '2.13.0'
    inputs = [[(1, 0)], [(0, 1)], [(.6, .8j)]]
    for theta in (-2*math.pi, -.91, 0., .73, 2*math.pi):
        for bits in (3, 6, 10):
            rounded, h = quantized_angle(theta, bits)
            U, V = explicit('z', theta), explicit('z', rounded)
            delta = distance(U, V)
            assert abs(delta-2*abs(math.sin((theta-rounded)/4))) < ATOL
            assert delta <= h/4+ATOL
            for f in inputs:
                v, _ = run(fq.Circuit(1, dtype=D).rz(0, rounded), f)
                torch.testing.assert_close(v, V @ product_input(f), rtol=0, atol=ATOL)
                assert torch.linalg.vector_norm(v-U @ product_input(f)).item() <= delta+ATOL
    print('45 quantized-Rz circuits: exact angle-error formula and grid bound passed; angles were not reduced modulo 2*pi.')
    for theta in (-.9, .0, .7):
        U = torch.exp(torch.tensor(.31j, dtype=D))*explicit('z', theta)
        chi, V = strip_phase(U)
        torch.testing.assert_close(torch.exp(torch.tensor(1j*chi, dtype=D))*V, U, rtol=0, atol=ATOL)
        for f in inputs:
            v, _ = run(fq.Circuit(1, dtype=D).unitary(0, unitary=U), f)
            torch.testing.assert_close(v, U @ product_input(f), rtol=0, atol=ATOL)
    print('9 U(2) circuits: determinant phase retained and reconstructed; SU(2) target validated separately.')
    for target in (explicit('y', .71) @ explicit('z', -.43), explicit('x', -.37), -I):
        previous = float('inf')
        for depth in (0, 2, 4, 6):
            word, V, delta, size = search(target, depth)
            assert size == (4**(depth+1)-1)//3
            assert delta <= previous+ATOL; previous = delta
            for f in inputs:
                v, p = run(word_circuit(word), f)
                torch.testing.assert_close(v, V @ product_input(f), rtol=0, atol=ATOL)
                expected = target @ product_input(f)
                assert torch.linalg.vector_norm(v-expected).item() <= delta+ATOL
                assert torch.max(torch.abs(p-expected.abs().square())).item() <= 2*delta+ATOL
            restored = word_matrix(inverse_word(word)) @ V
            torch.testing.assert_close(restored, I, rtol=0, atol=ATOL)
    print('36 finite-word circuits: depth 0/2/4/6, nested best errors, full vectors and inverse words passed; no SK or density claim.')
    exact = [explicit('x', .31), explicit('z', -.63), explicit('y', .87)]
    approx = [explicit(a, t+.01) for a, t in [('x', .31), ('z', -.63), ('y', .87)]]
    U = I.clone(); V = I.clone(); budget = 0.
    for u, v in zip(exact, approx):
        U = u @ U; V = v @ V; budget += distance(u, v)
    assert distance(U, V) <= budget+ATOL
    block = fq.Circuit(1, dtype=D).rx(0, .32).rz(0, -.62).ry(0, .88)
    for f in inputs:
        v, _ = run(block, f)
        torch.testing.assert_close(v, V @ product_input(f), rtol=0, atol=ATOL)
    for a, b in ((.2, .3), (.1, -.17), (.01, .02)):
        C = commutator(explicit('x', a), explicit('y', b))
        assert abs(distance(C, I)-2*abs(math.sin(a/2)*math.sin(b/2))) < ATOL
    for eps in (.01, .001, .0001):
        V, W = explicit('x', math.sqrt(eps)), explicit('y', -math.sqrt(eps))
        Vp, Wp = explicit('z', eps) @ V, explicit('x', -eps) @ W
        dv, dw = distance(V, Vp), distance(W, Wp)
        bound = 2*dv*distance(W, I)+2*dw*distance(Vp, I)
        assert distance(commutator(V, W), commutator(Vp, Wp)) <= bound+ATOL
    print('3 composed-rotation circuits, 3 exact commutator formulas and 3 local perturbation bounds passed.')
    invalid = [lambda: search(torch.eye(3, dtype=D), 2), lambda: search(2*I, 2),
               lambda: search(torch.exp(torch.tensor(.2j, dtype=D))*I, 2),
               lambda: catalog(7), lambda: catalog(True), lambda: quantized_angle(float('nan'), 4),
               lambda: quantized_angle(.3, True), lambda: quantized_angle(.3, 0),
               lambda: word_circuit((('y', 1),)), lambda: inverse_word((('x', True),))]
    for call in invalid:
        try: call()
        except ValueError: pass
        else: raise AssertionError('Invalid approximation contract accepted')
    assert RUNS == 93, RUNS
    print('10 malformed contracts rejected; 93 actual CPU complex128 circuits; implementation atol 1e-12, rtol 0.')
    print('Synthesis error, angle rounding and floating-point residuals are separate; no hardware or certified-interval error claim.')


if __name__ == '__main__':
    main()
