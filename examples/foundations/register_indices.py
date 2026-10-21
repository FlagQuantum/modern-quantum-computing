"""Section 4.2: declared register order, exact index maps and released simulation."""
from importlib.metadata import version
from itertools import product
from math import sqrt
import flagquantum as fq
import torch
try:
    from examples.foundations.tensor_spaces import prepare_matrix, OPTIONS
except ModuleNotFoundError:
    from tensor_spaces import prepare_matrix, OPTIONS

ATOL = 1e-12
DTYPE = torch.complex128


def register_labels(labels):
    if not isinstance(labels, (tuple, list)) or not labels:
        raise ValueError("Declare a nonempty ordered list of distinct labels")
    if any(type(x) is not str or not x for x in labels) or len(set(labels)) != len(labels):
        raise ValueError("Labels must be distinct nonempty strings")
    return tuple(labels)


def basis_index(bits):
    if not isinstance(bits, (tuple, list)) or not bits:
        raise ValueError("Declare at least one bit")
    if any(type(b) is not int or b not in (0, 1) for b in bits):
        raise ValueError("Bits must be literal Python integers 0 or 1")
    j = 0
    for b in bits:
        j = 2*j + b
    return j


def basis_bits(j, n):
    if type(n) is not int or n < 1:
        raise ValueError("The register size must be a positive integer")
    if type(j) is not int or not 0 <= j < 2**n:
        raise ValueError("Index must lie in the declared register range")
    return tuple((j // 2**(n-1-k)) % 2 for k in range(n))


def checked_result(circuit, n):
    result = fq.run(circuit, outputs=[fq.probabilities()], options=OPTIONS)
    state, probabilities = result.statevector(), result.probabilities
    assert state.shape == probabilities.shape == (1, 2**n)
    assert state.dtype == DTYPE and probabilities.dtype == torch.float64
    assert state.device.type == probabilities.device.type == 'cpu'
    assert torch.isfinite(state).all() and torch.isfinite(probabilities).all()
    torch.testing.assert_close(probabilities[0], state[0].abs().square(), rtol=0, atol=ATOL)
    return state[0], probabilities[0]


def prepare_basis(bits):
    basis_index(bits)  # Reject malformed input before making a circuit.
    circuit = fq.Circuit(len(bits), dtype=DTYPE)
    for q, b in enumerate(bits):
        if b == 1:
            circuit.x(q)
    return checked_result(circuit, len(bits))


def complex_product():
    # The first-column preparation is already derived in section 4.1.
    factors = ([.6, .8j], [1/sqrt(2), 1j/sqrt(2)], [sqrt(3)/2, .5])
    circuit = fq.Circuit(3, dtype=DTYPE)
    for q, vector in enumerate(factors):
        circuit.unitary(q, unitary=prepare_matrix(torch.tensor(vector, dtype=DTYPE)))
    return checked_result(circuit, 3)


def main():
    assert version('flagquantum') == '0.3.1'
    assert version('torch').split('+')[0] == '2.13.0'
    labels = register_labels(('signal', 'reference', 'flag'))
    print('Register order (most to least significant): ' + ', '.join(labels) + '.')
    assert basis_index((1, 1, 0)) == 6 and basis_index((0, 1, 1)) == 3
    print('110 ->', basis_index((1, 1, 0)), '; 6 ->', basis_bits(6, 3))
    count = 0
    for n in range(1, 9):
        for bits in product((0, 1), repeat=n):
            j = basis_index(bits)
            # Independent binary parser/formatter, not just helper round-trip.
            assert j == int(''.join(map(str, bits)), 2)
            assert basis_bits(j, n) == tuple(map(int, format(j, f'0{n}b'))) == bits
            count += 1
        assert basis_bits(0, n) == (0,)*n and basis_bits(2**n-1, n) == (1,)*n
    assert count == 510
    print('510 mathematical basis labels (n=1..8): index, inverse and independent strings agree.')
    for n in (2, 3):
        rows = []
        for bits in product((0, 1), repeat=n):
            state, probabilities = prepare_basis(bits)
            text = ''.join(map(str, bits))
            expected_j = int(text, 2)
            expected = torch.zeros(2**n, dtype=DTYPE)
            expected[expected_j] = 1
            torch.testing.assert_close(state, expected, rtol=0, atol=ATOL)
            torch.testing.assert_close(probabilities, expected.abs().square(), rtol=0, atol=ATOL)
            rows.append(f'{text}->{int(probabilities.argmax())}')
        print(f'FlagQuantum {n} qubits: ' + ', '.join(rows) + '.')
    print('12 actual basis-preparation circuits: full complex states and probabilities checked.')
    state, probabilities = complex_product()
    hand = [z/(10*sqrt(2)) for z in
            [3*sqrt(3), 3, 3j*sqrt(3), 3j, 4j*sqrt(3), 4j, -4*sqrt(3), -4]]
    torch.testing.assert_close(state, torch.tensor(hand, dtype=DTYPE), rtol=0, atol=ATOL)
    torch.testing.assert_close(probabilities, torch.tensor([.135,.045,.135,.045,.24,.08,.24,.08], dtype=torch.float64), rtol=0, atol=ATOL)
    assert abs(sum(abs(z)**2 for z in hand)-1) <= ATOL
    print('Complex product probabilities: ' + ', '.join(f'{p:.9f}' for p in probabilities.tolist()) + '.')
    print(f'Index 6 is 110: amplitude real={state[6].real.item():.9f}; probability={probabilities[6].item():.9f}.')
    # Deliberate convention mistakes: both must be caught, with no data repair.
    one, _ = prepare_basis((1, 0, 0))
    assert abs(one[4].item()-1) <= ATOL and abs(one[1].item()) <= ATOL
    assert basis_bits(3, 4) == (0, 0, 1, 1)  # Preserve declared width.
    failures = [lambda: basis_index(()), lambda: basis_index((0,2)),
                lambda: basis_index((True,0)), lambda: basis_index((1.,0)),
                lambda: basis_index('10'), lambda: basis_bits(-1,3),
                lambda: basis_bits(8,3), lambda: basis_bits(0,0),
                lambda: basis_bits(True,3), lambda: basis_bits(0,2.5),
                lambda: register_labels(('data','data')), lambda: register_labels(('',))]
    for action in failures:
        try:
            action()
        except ValueError:
            pass
        else:
            raise AssertionError('Malformed register input was accepted')
    print('Reversed-significance witness, leading zeros and 12 malformed-input cases checked.')
    print('14 actual simulator circuits total; CPU complex128, atol=1e-12, rtol=0.')
    print('No sampling, hardware layout, SWAP or marginal-order claim.')


if __name__ == '__main__':
    main()
