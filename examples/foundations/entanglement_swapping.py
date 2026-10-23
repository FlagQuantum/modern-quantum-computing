"""7.8: exact entanglement-swapping branches and network execution boundaries.

Native static source/analyzer circuits and terminal queries. Conditional vectors,
corrections on known fixtures and classical message checks do not implement
mid-circuit measurement, distributed feedforward, storage or network transport.
"""
import cmath
import itertools
import math
from dataclasses import replace

import flagquantum as fq
import torch
try:
    from examples.foundations.tensor_spaces import OPTIONS
except ModuleNotFoundError:
    from tensor_spaces import OPTIONS

D = torch.complex128
ATOL = 1e-12
RUNS = 0
I = torch.eye(2, dtype=D)
X = torch.tensor([[0, 1], [1, 0]], dtype=D)
Y = torch.tensor([[0, -1j], [1j, 0]], dtype=D)
Z = torch.diag(torch.tensor([1, -1], dtype=D))


def close(actual, expected):
    actual = torch.as_tensor(actual, dtype=D)
    expected = torch.as_tensor(expected, dtype=D)
    assert actual.shape == expected.shape
    torch.testing.assert_close(actual, expected, atol=ATOL, rtol=0)


def roles_contract(roles):
    if (type(roles) is not tuple or len(roles) != 4
            or any(type(q) is not int or not 0 <= q < 4 for q in roles)
            or len(set(roles)) != 4):
        raise ValueError('Four distinct ordered physical qubits in the four-qubit teaching register required')
    return roles


def bit(m):
    if type(m) is not int or m not in (0, 1):
        raise ValueError('Literal classical bit required')
    return m


def link(theta, phi):
    if any(type(t) not in (int, float) or not math.isfinite(t) for t in (theta, phi)):
        raise ValueError('Finite real angles in radians required')
    return torch.tensor([math.cos(theta/2), cmath.exp(1j*phi)*math.sin(theta/2)], dtype=D)


def coefficients(v):
    if (not isinstance(v, torch.Tensor) or v.shape != (2,) or v.dtype != D
            or v.device.type != 'cpu' or not bool(torch.isfinite(v).all())
            or abs(torch.vdot(v, v).item()-1) > ATOL):
        raise ValueError('Two finite normalized CPUcomplex128 link coefficients required;no repair')
    return v


def index(values, roles):
    roles_contract(roles)
    out = [0]*4
    for q, value in zip(roles, values):
        out[q] = bit(value)
    return sum(x << (3-q) for q, x in enumerate(out))


def bell(m, n):
    bit(m); bit(n)
    v = torch.zeros(4, dtype=D)
    v[n] = 1/math.sqrt(2)
    v[2+(1 ^ n)] = (-1)**m/math.sqrt(2)
    return v


def reference(d, e, roles=(0, 1, 2, 3), decoded=False, coherent=False):
    """Independent scalar bit-index amplitudes;no native matrix expansion."""
    coefficients(d); coefficients(e); roles_contract(roles)
    if coherent and not decoded:
        raise ValueError('Coherent corrections require the decoded source')
    v = torch.zeros(16, dtype=D)
    for i, j in itertools.product((0, 1), repeat=2):
        if not decoded:
            v[index((i, i, j, j), roles)] = d[i]*e[j]
        else:
            for m in (0, 1):
                n = j ^ i
                r = j ^ (n if coherent else 0)
                phase = (-1)**(m*i)
                if coherent:
                    phase *= (-1)**(m*r)
                v[index((i, m, n, r), roles)] += phase*d[i]*e[j]/math.sqrt(2)
    return v


def source(roles=(0, 1, 2, 3), angles=(math.pi/2, 0., math.pi/2, 0.),
           decoded=True, coherent=False):
    left, u, v, right = roles_contract(roles)
    if type(angles) is not tuple or len(angles) != 4:
        raise ValueError('Two declared (theta,phi) link angles required')
    link(*angles[:2]); link(*angles[2:])
    if coherent and not decoded:
        raise ValueError('Decode before coherent correction')
    c = fq.Circuit(4, dtype=D)
    for a, b, theta, phi in ((left, u, *angles[:2]), (v, right, *angles[2:])):
        c.ry(a, theta).p(a, phi).cx(a, b)
    if decoded:
        c.cx(u, v).h(u)
    if coherent:
        c.cx(v, right).cz(u, right)
    return c


def execute(c, outputs, shots=None, seed=781):
    global RUNS
    if shots is not None and (type(shots) is not int or shots <= 0):
        raise ValueError('Positive literal shot count required')
    if type(seed) is not int or seed < 0:
        raise ValueError('Nonnegative literal seed required')
    result = fq.run(c, outputs=outputs, options=replace(OPTIONS, seed=seed),
                    **({} if shots is None else {'shots': shots}))
    RUNS += 1
    return result


def branches(v, roles=(0, 1, 2, 3)):
    roles_contract(roles)
    if (not isinstance(v, torch.Tensor) or v.shape != (16,) or v.dtype != D
            or v.device.type != 'cpu' or not bool(torch.isfinite(v).all())
            or abs(torch.vdot(v, v).item()-1) > ATOL):
        raise ValueError('Normalized finite CPUcomplex128 four-qubit vector required')
    out = []
    for m, n in itertools.product((0, 1), repeat=2):
        eta = torch.stack([v[index((i, m, n, j), roles)]
                           for i, j in itertools.product((0, 1), repeat=2)])
        p = float(torch.vdot(eta, eta).real)
        if p == 0 and bool((eta != 0).any()):
            raise FloatingPointError('Positive branch squared norm underflow;not an impossible event')
        out.append((p, None if p == 0 else eta/math.sqrt(p)))
    return out


def expected_branch(d, e, m, n):
    coefficients(d); coefficients(e); bit(m); bit(n)
    eta = torch.zeros(4, dtype=D)
    for i in (0, 1):
        eta[2*i+(i ^ n)] = (-1)**(m*i)*d[i]*e[i ^ n]/math.sqrt(2)
    p = float(torch.vdot(eta, eta).real)
    if p == 0 and bool((eta != 0).any()):
        raise FloatingPointError('Positive analytic branch squared norm underflow')
    return p, None if p == 0 else eta/math.sqrt(p)


def correction(m, n):
    bit(m); bit(n)
    return (Z if m else I) @ (X if n else I)


def moment(v, a, b):
    return float(torch.vdot(v, torch.kron(a, b)@v).real)


def weighted_moment(family, a, b):
    return sum(p*moment(v, a, b) for p, v in family if p > 0)


def analyze(angles=(math.pi/2, 0., math.pi/2, 0.), roles=(0, 1, 2, 3)):
    d, e = link(*angles[:2]), link(*angles[2:])
    result = execute(source(roles, angles), [fq.probabilities(qubits=(roles[1], roles[2]))])
    state = result.statevector()[0]
    close(state, reference(d, e, roles, decoded=True))
    family = branches(state, roles)
    for k, (p, v) in enumerate(family):
        q, w = expected_branch(d, e, k//2, k % 2)
        close(p, q)
        if p > 0:
            close(v, w)  # no phase alignment
    close(result.probabilities[0], [p for p, _ in family])
    return result, family


def corrected_fixture(m, n, roles=(0, 1, 2, 3), wrong=False):
    left, _, _, right = roles_contract(roles)
    bit(m); bit(n)
    c = fq.Circuit(4, dtype=D).h(left).cx(left, right)
    if m:
        c.z(left)
    if n:
        c.x(right)
    # Known Bell branch prepared afresh as a fixture,not retained-state feedforward.
    if n:
        c.x(right)
    if m and not wrong:
        c.z(right)
    r = execute(c, [fq.probabilities(qubits=(left, right))])
    expected = torch.zeros(16, dtype=D)
    target = bell(m if wrong else 0, 0)
    for i, j in itertools.product((0, 1), repeat=2):
        expected[index((i, 0, 0, j), roles)] = target[2*i+j]
    close(r.statevector()[0], expected)
    return r


def packet(bits, columns, roles, trial):
    roles_contract(roles)
    if type(trial) is not str or not trial:
        raise ValueError('Nonempty matching trial ID required')
    if (not isinstance(bits, torch.Tensor) or bits.dtype != torch.int64
            or bits.ndim != 2 or bits.shape[1] != 2 or len(bits) == 0
            or not bool(((bits == 0) | (bits == 1)).all())):
        raise ValueError('Nonempty literal N-by2 int64 raw bit records required')
    if type(columns) is not tuple or set(columns) != {roles[1], roles[2]} or len(columns) != 2:
        raise ValueError('Named two middle output columns required')
    order = [columns.index(q) for q in (roles[1], roles[2])]
    return bits[:, order].clone(), trial


def frame(sign_x, sign_z, m, n):
    bit(m); bit(n)
    if sign_x not in (-1, 1) or sign_z not in (-1, 1):
        raise ValueError('Pauli product outcomes must be signed unit values')
    return ((-1)**m*sign_x, (-1)**n*sign_z)


def main():
    global RUNS
    for roles in itertools.permutations(range(4)):
        d = link(math.pi/2, 0.)
        for decoded, coherent in ((False, False), (True, False), (True, True)):
            c = source(roles, decoded=decoded, coherent=coherent)
            r = execute(c, [fq.probabilities(qubits=(roles[0], roles[3]))])
            close(r.statevector()[0], reference(d, d, roles, decoded, coherent))
            if decoded and not coherent:
                for k, (p, v) in enumerate(branches(r.statevector()[0], roles)):
                    close(p, .25); close(v, bell(k//2, k % 2))
                close(r.probabilities[0], [.25]*4)
            if coherent:
                close(r.probabilities[0], [.5, 0, 0, .5])
    print('72native circuits:all24role permutations;two sources,middle decoder and coherent non-network correction match scalar amplitudes.')
    for m, n in itertools.product((0, 1), repeat=2):
        corrected_fixture(m, n)
        close(torch.kron(I, correction(m, n))@bell(m, n), bell(0, 0))
    print('4native fresh Bell fixtures:all communicated-bit X-then-Z corrections recover Phi+ with exact branch phase.')
    for axis, operator in (('X', X), ('Y', Y), ('Z', Z)):
        c = source()
        for q in (0, 3):
            if axis == 'X':
                c.h(q)
            elif axis == 'Y':
                c.p(q, -math.pi/2).h(q)
        r = execute(c, [fq.probabilities(), fq.samples(qubits=(2, 1))], shots=13)
        family = branches(reference(link(math.pi/2, 0.), link(math.pi/2, 0.), decoded=True))
        expected_joint = torch.zeros(16, dtype=D)
        # Independent signed Pauli means imply each parity distribution.
        for m, n in itertools.product((0, 1), repeat=2):
            corr = ((-1)**m if axis == 'X' else (-1)**n if axis == 'Z'
                    else -(-1)**(m+n))
            for a, b in itertools.product((0, 1), repeat=2):
                expected_joint[index((a, m, n, b), (0, 1, 2, 3))] = (1+(-1)**(a+b)*corr)/16
        close(r.probabilities[0], expected_joint)
        close(weighted_moment(family, operator, operator), 0.)
        mapped, trial = packet(r.samples[0], (2, 1), (0, 1, 2, 3), 'trial-7.8')
        assert mapped.shape == (13, 2) and trial == 'trial-7.8'
    print('3native joint Pauli analyzers:XX/YY/ZZ branch signs,uniform ignored ensemble and reversed raw middle columns passed.')
    cases = [(1.13, .37, .89, -.51), (.72, -.4, 1.7, .63),
             (0., 0., math.pi/2, 0.), (math.pi/2, 0., 0., 0.),
             (1e-10, .2, 0., 0.), (0., 0., 0., 0.), (math.pi/2, .7, math.pi/2, -.2)]
    for angles in cases:
        _, family = analyze(angles)
        close(sum(p for p, _ in family), 1.)
        d, e = link(*angles[:2]), link(*angles[2:])
        for k, (p, v) in enumerate(family):
            if p:
                corrected = torch.kron(I, correction(k//2, k % 2))@v
                ideal = torch.tensor([d[0]*e[k % 2], 0., 0., d[1]*e[1 ^ (k % 2)]], dtype=D)
                ideal = ideal/torch.linalg.vector_norm(ideal)
                close(corrected, ideal)
    print('7native nonideal-link cases:unequal weights,relative phases,zero branches and tiny positive branches retained;no entanglement repair claimed.')
    wrong = fq.Circuit(4, dtype=D).h(0).cx(0, 1).h(2).cx(2, 3).h(1).cx(1, 2)
    r = execute(wrong, [fq.probabilities(qubits=(1, 2))])
    assert not torch.allclose(r.statevector()[0], reference(link(math.pi/2, 0.), link(math.pi/2, 0.), decoded=True), atol=ATOL, rtol=0)
    # Middle outcome frequencies alone fail to diagnose this wrong analyzer.
    close(r.probabilities[0], [.25]*4)
    r = corrected_fixture(1, 1, wrong=True)
    assert abs(torch.vdot(r.statevector()[0], corrected_fixture(0, 0).statevector()[0])) < ATOL
    print('3native diagnostic fixtures:wrong-order analyzer has plausible uniform outcomes;missing phase correction fails the full-state target.')
    family = [(0.25, bell(m, n)) for m, n in itertools.product((0, 1), repeat=2)]
    wrong_average = sum(v for _, v in family)
    wrong_average /= torch.linalg.vector_norm(wrong_average)
    close(moment(wrong_average, X, X), 0.)
    close(moment(wrong_average, Z, I), 1.)  # ignored ensemble has local Z=0
    close(weighted_moment(family, Z, I), 0.)
    rejects = [
        lambda: roles_contract((0, 1, 1, 3)),
        lambda: roles_contract((0, 1, 2, 4)),
        lambda: roles_contract([0, 1, 2, 3]),
        lambda: roles_contract((False, 1, 2, 3)),
        lambda: coefficients(torch.ones(2, dtype=D)),
        lambda: coefficients(torch.tensor([1., 0.])),
        lambda: link(float('nan'), 0.),
        lambda: correction(2, 0),
        lambda: correction(True, 0),
        lambda: branches(torch.ones(16, dtype=D)),
        lambda: source(coherent=True, decoded=False),
        lambda: packet(torch.zeros((2, 2), dtype=torch.int64), (0, 1), (0, 1, 2, 3), 'x'),
        lambda: packet(torch.zeros((2, 2), dtype=torch.int64), (1, 2), (0, 1, 2, 3), ''),
        lambda: packet(torch.full((2, 2), 2, dtype=torch.int64), (1, 2), (0, 1, 2, 3), 'x'),
        lambda: execute(source(), [fq.probabilities()], shots=0),
        lambda: frame(0, 1, 0, 0),
    ]
    before = RUNS
    for reject in rejects:
        try:
            reject()
        except ValueError:
            pass
        else:
            raise AssertionError('Malformed contract accepted')
    assert RUNS == before == 89
    tiny = torch.zeros(16, dtype=D)
    tiny[0] = 1.
    tiny[index((1, 1, 1, 1), (0, 1, 2, 3))] = 1e-200
    try:
        branches(tiny)
    except FloatingPointError:
        pass
    else:
        raise AssertionError('Squared-norm underflow disguised as zero probability')
    print('16malformed contracts rejected before native execution;squared-norm underflow explicit;normalized-vector averaging gives a false local bias.')
    print('89CPUcomplex128native circuits passed;static/coherent fixtures do not certify distributed messaging,loss,storage or dynamic collapse.')


if __name__ == '__main__':
    main()
