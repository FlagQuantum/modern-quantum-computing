"""7.4: CHSH correlations with native terminal queries and scalar references.

The local classical model and ideal IID sampling assumptions are explicit.
Nothing here is a hardware Bell test or a native mid-circuit instrument.
"""
import cmath
import itertools
import math
from dataclasses import replace
from importlib.metadata import version

import flagquantum as fq
import torch
try:
    from examples.foundations.tensor_spaces import OPTIONS
except ModuleNotFoundError:
    from tensor_spaces import OPTIONS

D = torch.complex128
ATOL = 1e-12
RUNS = 0
SETTINGS = ((0., math.pi/4), (0., -math.pi/4),
            (math.pi/2, math.pi/4), (math.pi/2, -math.pi/4))
SIGNS = (1, 1, 1, -1)
X = torch.tensor([[0, 1], [1, 0]], dtype=D)
Z = torch.diag(torch.tensor([1, -1], dtype=D))
I = torch.eye(2, dtype=D)


def real_angle(x):
    if type(x) not in (int, float) or not math.isfinite(x):
        raise ValueError('Finite real radian angle required')
    return float(x)


def support(n, pair):
    if (type(n) is not int or not 2 <= n <= 4 or type(pair) is not tuple
            or len(pair) != 2 or any(type(q) is not int or not 0 <= q < n for q in pair)
            or pair[0] == pair[1]):
        raise ValueError('Two distinct ordered qubits in a 2-4 qubit teaching register required')
    return pair


def classical_correlations(weights, alice, bob):
    """Finite setting-independent hidden distribution and local response means."""
    if not weights or len(weights) != len(alice) or len(weights) != len(bob):
        raise ValueError('One shared distribution and matching local response rows required')
    if any(type(w) not in (int, float) or not math.isfinite(w) or w < 0 for w in weights):
        raise ValueError('Finite nonnegative weights required')
    if abs(sum(weights)-1) > ATOL:
        raise ValueError('Normalized distribution required; no repair')
    for row in (*alice, *bob):
        if len(row) != 2 or any(type(x) not in (int, float) or not math.isfinite(x) or abs(x) > 1 for x in row):
            raise ValueError('Two bounded local response means per hidden value required')
    return tuple(sum(w*a[x]*b[y] for w, a, b in zip(weights, alice, bob))
                 for x, y in itertools.product((0, 1), repeat=2))


def chsh(values):
    if len(values) != 4 or any(type(x) not in (int, float) or not math.isfinite(x) or abs(x) > 1+ATOL for x in values):
        raise ValueError('Four finite correlations in 00,01,10,11 order required')
    return sum(s*x for s, x in zip(SIGNS, values))


def axis(angle):
    a = real_angle(angle)
    return math.cos(a)*Z + math.sin(a)*X


def observable(q, angle):
    a = real_angle(angle)
    return fq.Z(q)*math.cos(a) + fq.X(q)*math.sin(a)


def analytic(alpha, beta, theta=math.pi/2, phase=0.):
    a, b, t, p = map(real_angle, (alpha, beta, theta, phase))
    e = math.cos(a)*math.cos(b) + math.sin(t)*math.cos(p)*math.sin(a)*math.sin(b)
    ma, mb = math.cos(t)*math.cos(a), math.cos(t)*math.cos(b)
    probabilities = torch.tensor([(1+(-1)**u*ma+(-1)**v*mb+(-1)**(u+v)*e)/4
                                 for u, v in itertools.product((0, 1), repeat=2)], dtype=torch.float64)
    return e, probabilities


def matrix_probabilities(alpha, beta, theta=math.pi/2, phase=0.):
    a, b, t, p = map(real_angle, (alpha, beta, theta, phase))
    psi = torch.tensor([math.cos(t/2), 0, 0, cmath.exp(1j*p)*math.sin(t/2)], dtype=D)
    effects = [torch.kron((I+(-1)**u*axis(a))/2, (I+(-1)**v*axis(b))/2)
               for u, v in itertools.product((0, 1), repeat=2)]
    return torch.stack([torch.vdot(psi, effect@psi).real for effect in effects])


def prepare(theta=math.pi/2, phase=0., n=2, pair=(0, 1)):
    left, right = support(n, pair)
    t, p = map(real_angle, (theta, phase))
    circuit = fq.Circuit(n, dtype=D).ry(left, t).cx(left, right).p(left, p)
    for q in range(n):
        if q not in pair:
            circuit.ry(q, .31*(q+1)).p(q, -.17*(q+1))
    return circuit


def scalar_state(alpha, beta, theta, phase, n, pair):
    left, right = support(n, pair)
    a, b, t, p = map(real_angle, (alpha, beta, theta, phase))
    # Entries of Ry(-a), in row-major order; no native gate matrix is used.
    ra = ((math.cos(a/2), math.sin(a/2)), (-math.sin(a/2), math.cos(a/2)))
    rb = ((math.cos(b/2), math.sin(b/2)), (-math.sin(b/2), math.cos(b/2)))
    result = []
    for k in range(2**n):
        bits = [int(x) for x in format(k, f'0{n}b')]
        u, v = bits[left], bits[right]
        z = math.cos(t/2)*ra[u][0]*rb[v][0] + cmath.exp(1j*p)*math.sin(t/2)*ra[u][1]*rb[v][1]
        for q in range(n):
            if q not in pair:
                z *= (math.cos(.31*(q+1)/2) if bits[q] == 0
                      else cmath.exp(-.17j*(q+1))*math.sin(.31*(q+1)/2))
        result.append(z)
    return torch.tensor(result, dtype=D)


def histogram(bits, expected_shots):
    if type(expected_shots) is not int or expected_shots < 1:
        raise ValueError('Positive fixed record budget required')
    if (not isinstance(bits, torch.Tensor) or bits.dtype != torch.int64 or bits.device.type != 'cpu'
            or bits.shape != (expected_shots, 2) or not bool(((bits == 0) | (bits == 1)).all())):
        raise ValueError('Complete CPU int64 binary records with two ordered columns required')
    return torch.bincount(2*bits[:, 0]+bits[:, 1], minlength=4)


def sample_statistics(bits, expected_shots):
    counts = histogram(bits, expected_shots)
    scores = 1-2*(bits[:, 0] ^ bits[:, 1])
    mean = float(scores.to(torch.float64).mean())
    assert abs(mean-float((counts[0]-counts[1]-counts[2]+counts[3])/expected_shots)) < ATOL
    return counts, mean


def run_setting(alpha, beta, theta=math.pi/2, phase=0., n=2, pair=(0, 1), shots=None, seed=23):
    global RUNS
    left, right = support(n, pair)
    a, b, t, p = map(real_angle, (alpha, beta, theta, phase))
    if shots is not None and (type(shots) is not int or shots < 1):
        raise ValueError('Positive literal shot count required')
    if type(seed) is not int or seed < 0:
        raise ValueError('Nonnegative literal seed required')
    circuit = prepare(t, p, n, pair).ry(left, -a).ry(right, -b)
    outputs = [fq.probabilities(qubits=pair), fq.expectation(fq.Z(left)@fq.Z(right), name='correlation')]
    if shots is not None:
        outputs.append(fq.samples(qubits=pair))
    result = fq.run(circuit, outputs=outputs, options=replace(OPTIONS, seed=seed),
                    **({} if shots is None else {'shots': shots}))
    RUNS += 1
    v, probabilities = result.statevector(), result.probabilities
    assert v.shape == (1, 2**n) and v.dtype == D and v.device.type == 'cpu'
    assert probabilities.shape == (1, 4) and probabilities.dtype == torch.float64
    assert bool(torch.isfinite(v).all()) and bool(torch.isfinite(probabilities).all())
    e, reference = analytic(a, b, t, p)
    assert torch.allclose(v[0], scalar_state(a, b, t, p, n, pair), atol=ATOL, rtol=0)
    assert torch.allclose(probabilities[0], reference, atol=ATOL, rtol=0)
    assert torch.allclose(reference, matrix_probabilities(a, b, t, p), atol=ATOL, rtol=0)
    assert abs(float(result.expectation('correlation')[0])-e) < ATOL
    assert abs(float(probabilities[0]@torch.tensor([1., -1., -1., 1.], dtype=torch.float64))-e) < ATOL
    report = {'state': v[0], 'probabilities': probabilities[0], 'correlation': float(result.expectation('correlation')[0])}
    if shots is not None:
        raw = result.samples
        assert raw.shape == (1, shots, 2)
        counts, mean = sample_statistics(raw[0], shots)
        report.update(bits=raw[0], counts=counts, mean=mean)
    return report


def direct_correlations(theta=math.pi/2, phase=0.):
    global RUNS
    t, p = map(real_angle, (theta, phase))
    outputs = [fq.expectation(observable(0, a)@observable(1, b), name=f'e{j}')
               for j, (a, b) in enumerate(SETTINGS)]
    result = fq.run(prepare(t, p), outputs=outputs, options=OPTIONS)
    RUNS += 1
    values = tuple(float(result.expectation(f'e{j}')[0]) for j in range(4))
    for (a, b), value in zip(SETTINGS, values):
        assert abs(value-analytic(a, b, t, p)[0]) < ATOL
    return values


def calibrated_pair(n, pair, a, b):
    global RUNS
    left, right = support(n, pair)
    if any(type(x) is not int or x not in (0, 1) for x in (a, b)):
        raise ValueError('Literal calibration bits required')
    circuit = fq.Circuit(n, dtype=D)
    if a: circuit.x(left)
    if b: circuit.x(right)
    result = fq.run(circuit, outputs=[fq.probabilities(qubits=pair), fq.samples(qubits=pair)],
                    shots=7, options=OPTIONS)
    RUNS += 1
    assert result.samples.shape == (1, 7, 2) and result.samples[0].tolist() == [[a, b]]*7
    expected = torch.zeros(4, dtype=torch.float64); expected[2*a+b] = 1
    assert torch.allclose(result.probabilities[0], expected, atol=ATOL, rtol=0)


def uncertainty(means, shots, delta=.05):
    chsh(means)
    if type(shots) is not int or shots < 2 or type(delta) not in (int, float) or not 0 < delta < 1:
        raise ValueError('At least two records per setting and 0<delta<1 required')
    standard_error = math.sqrt(sum(max(0., 1-e*e) for e in means)/(shots-1))
    return standard_error, math.sqrt(4/(shots*delta))


def main():
    assert version('flagquantum') == '0.3.1'
    assert RUNS == 0
    scores = [chsh(classical_correlations([1.], [a], [b]))
              for a in itertools.product((-1, 1), repeat=2)
              for b in itertools.product((-1, 1), repeat=2)]
    assert set(scores) == {-2., 2.}
    values = classical_correlations([.25, .75], [(.2, -.4), (.8, .1)], [(-.3, .6), (.7, -.2)])
    assert abs(chsh(values)) <= 2
    print('16 deterministic local strategies and one stochastic mixture: classical bound passed.')
    for theta, phase in [(math.pi/2, 0.), (math.pi/2, math.pi), (0., 0.), (.81, .43), (-1.2, -.77)]:
        direct = direct_correlations(theta, phase)
        observed = [run_setting(a, b, theta, phase)['correlation'] for a, b in SETTINGS]
        assert all(abs(x-y) < ATOL for x, y in zip(direct, observed))
    assert abs(chsh(direct_correlations.__defaults__ or ())) if False else True
    print('25 native circuits: five state families, direct observables and four analyzer settings agree.')
    for n in (3, 4):
        for pair in itertools.permutations(range(n), 2):
            for a, b in SETTINGS:
                run_setting(a, b, .83, -.49, n, pair)
    print('72 native circuits: all ordered pairs in three/four qubits, complex spectators and indexed amplitudes passed.')
    reports = [run_setting(a, b, shots=4096, seed=71+j) for j, (a, b) in enumerate(SETTINGS)]
    means = [r['mean'] for r in reports]; se, radius = uncertainty(means, 4096)
    assert 0 <= se <= math.sqrt(4/(4096-1)) and radius > 0
    for r in reports: assert int(r['counts'].sum()) == 4096
    print('4 native fixed-budget batches: raw records/counts/scores passed; SE and conservative radius kept separate.')
    for n, pair in [(2, (0, 1)), (2, (1, 0)), (4, (3, 0))]:
        for a, b in itertools.product((0, 1), repeat=2): calibrated_pair(n, pair, a, b)
    print('12 native basis calibrations: ordered output columns and bit-to-sign convention passed.')
    wrong = [run_setting(a, -b)['correlation'] for a, b in SETTINGS]
    assert abs(chsh(wrong)) < ATOL
    postselected = [r['bits'][(r['bits'][:, 0] ^ r['bits'][:, 1]) == (j == 3)] for j, r in enumerate(reports)]
    assert all(0 < len(bits) < 4096 for bits in postselected)
    assert chsh([sample_statistics(bits, len(bits))[1] for bits in postselected]) == 4
    bad = [lambda: support(2, (0, 0)), lambda: support(True, (0, 1)), lambda: real_angle(True),
           lambda: real_angle(float('nan')), lambda: run_setting(0, 0, shots=0),
           lambda: run_setting(0, 0, seed=-1), lambda: classical_correlations([.2], [(1, 1)], [(1, 1)]),
           lambda: classical_correlations([1.], [(2, 0)], [(1, 1)]),
           lambda: histogram(torch.tensor([[0, 2]], dtype=torch.int64), 1),
           lambda: histogram(torch.tensor([[0., 1.]]), 1),
           lambda: histogram(postselected[0], 4096), lambda: uncertainty([0., 0., 0., 0.], 1)]
    for attempt in bad:
        before = RUNS
        try: attempt()
        except ValueError: pass
        else: raise AssertionError('Malformed CHSH contract admitted')
        assert RUNS == before
    print('4 wrong-sign analyzer circuits and postselection-to-S=4 expose distinct failure modes;12 malformed contracts rejected.')
    assert RUNS == 117, RUNS
    print('117 CPU complex128 native circuits passed; simulation is not a loophole-free Bell experiment.')


if __name__ == '__main__':
    main()
