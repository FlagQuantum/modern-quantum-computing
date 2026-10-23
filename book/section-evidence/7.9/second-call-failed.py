"""7.9: task-specific counterexamples to claims from entanglement alone.

Released native static circuits plus independent indexed/effect references.
No complexity separation,capacity theorem,dynamic network or hardware certificate.
"""
import cmath
import itertools
import math
from dataclasses import replace
import torch
import flagquantum as fq
try:
    from examples.foundations.tensor_spaces import OPTIONS
    from examples.foundations import entanglement_swapping as swapping
except ModuleNotFoundError:
    from tensor_spaces import OPTIONS
    import entanglement_swapping as swapping

D = torch.complex128
ATOL = 1e-12
RUNS = 0
I = torch.eye(2, dtype=D)
X = torch.tensor([[0, 1], [1, 0]], dtype=D)
Y = torch.tensor([[0, -1j], [1j, 0]], dtype=D)
Z = torch.diag(torch.tensor([1, -1], dtype=D))


def close(a, b):
    a, b = torch.as_tensor(a, dtype=D), torch.as_tensor(b, dtype=D)
    assert a.shape == b.shape
    torch.testing.assert_close(a, b, atol=ATOL, rtol=0)


def angle(t):
    if type(t) not in (float, int) or not math.isfinite(t):
        raise ValueError('Finite real radian angle required')
    return t


def bit(m):
    if type(m) is not int or m not in (0, 1):
        raise ValueError('Literal bit required')
    return m


def qubit(theta, phi):
    angle(theta); angle(phi)
    return torch.tensor([math.cos(theta/2), cmath.exp(1j*phi)*math.sin(theta/2)], dtype=D)


def vector(v):
    if (not isinstance(v, torch.Tensor) or v.shape != (2,) or v.dtype != D
            or v.device.type != 'cpu' or not bool(torch.isfinite(v).all())
            or abs(torch.vdot(v, v).item()-1) > ATOL):
        raise ValueError('Normalized finite CPUcomplex128 qubit vector required;no repair')
    return v


def prepare(v):
    a, b = vector(v).tolist()
    return torch.tensor([[a, -b.conjugate()], [b, a.conjugate()]], dtype=D)


def run(circuit, outputs, shots=None, seed=79):
    global RUNS
    if shots is not None and (type(shots) is not int or shots < 1):
        raise ValueError('Positive literal shot count required')
    if type(seed) is not int or seed < 0:
        raise ValueError('Nonnegative literal seed required')
    result = fq.run(circuit, outputs=outputs, options=replace(OPTIONS, seed=seed),
                    **({} if shots is None else {'shots': shots}))
    RUNS += 1
    return result


def teleport_reference(psi, resource_phase=0.):
    vector(psi); angle(resource_phase)
    out = torch.zeros(8, dtype=D)
    for i, m, n in itertools.product((0, 1), repeat=3):
        j = i ^ n
        out[4*m+2*n+j] += psi[i]*(-1)**(m*i)*cmath.exp(1j*resource_phase*j)/2
    return out


def teleport_circuit(psi, resource_phase=0.):
    angle(resource_phase)
    c = fq.Circuit(3, dtype=D).unitary((0,), unitary=prepare(psi))
    return c.h(1).cx(1, 2).p(1, resource_phase).cx(0, 1).h(0)


def teleport_branches(full):
    if (not isinstance(full, torch.Tensor) or full.shape != (8,) or full.dtype != D
            or not bool(torch.isfinite(full).all())
            or abs(torch.vdot(full, full).item()-1) > ATOL):
        raise ValueError('Normalized finite CPUcomplex128 three-qubit vector required')
    rows = []
    for m, n in itertools.product((0, 1), repeat=2):
        eta = full[4*m+2*n:4*m+2*n+2]
        p = float(torch.vdot(eta, eta).real)
        if p == 0 and bool((eta != 0).any()):
            raise FloatingPointError('Nonzero branch squared-norm underflow')
        rows.append((p, None if p == 0 else eta/math.sqrt(p)))
    return rows


def correction(m, n):
    bit(m); bit(n)
    return (Z if m else I) @ (X if n else I)


def mean(v, operator):
    return float(torch.vdot(v, operator@v).real)


def clone_reference(psi):
    vector(psi)
    out = torch.zeros(16, dtype=D)
    for i, j in itertools.product((0, 1), repeat=2):
        out[8*i+4*i+2*j+j] = psi[i]/math.sqrt(2)
    resource = torch.tensor([1, 0, 0, 1], dtype=D)/math.sqrt(2)
    target = torch.kron(torch.kron(psi, psi), resource)
    return out, target


def correlation(alpha, beta, theta=math.pi/2):
    angle(alpha); angle(beta); angle(theta)
    return math.cos(alpha)*math.cos(beta)+math.sin(theta)*math.sin(alpha)*math.sin(beta)


def local_table(alpha, beta):
    """Explicit shared (z,x) model for Alice/Bob's declared Z/X settings only."""
    if alpha not in (0, 1) or beta not in (0, 1):
        raise ValueError('Declared Z/X setting indices required')
    p = torch.zeros(4, dtype=torch.float64)
    for z, x in itertools.product((0, 1), repeat=2):
        a = (z, x)[alpha]
        b = (z, x)[beta]
        p[2*a+b] += .25
    return p


def pair_contract(k, roles=None):
    if type(k) is not int or not 1 <= k <= 4:
        raise ValueError('One to four Bell pairs for this teaching reference required')
    roles = tuple(range(2*k)) if roles is None else roles
    if (type(roles) is not tuple or len(roles) != 2*k
            or any(type(q) is not int for q in roles) or sorted(roles) != list(range(2*k))):
        raise ValueError('Declared permutation:all left roles then all right roles required')
    return roles


def pair_index(bits, roles):
    k = len(bits)
    pair_contract(k, roles)
    if any(type(b) is not int or b not in (0, 1) for b in bits):
        raise ValueError('Literal bit tuple required')
    full = [0]*(2*k)
    for j, b in enumerate(bits):
        full[roles[j]] = full[roles[k+j]] = b
    return sum(b << (2*k-1-q) for q, b in enumerate(full))


def pair_reference(k, roles=None):
    roles = pair_contract(k, roles)
    out = torch.zeros(2**(2*k), dtype=D)
    for bits in itertools.product((0, 1), repeat=k):
        out[pair_index(bits, roles)] = 1/math.sqrt(2**k)
    return out


def main():
    for choice in (0, 1):
        for phi in (0., .63, -1.17):
            c = fq.Circuit(2, dtype=D).h(0).cx(0, 1).p(0, phi)
            if choice:
                c.x(0)
            r = run(c, [fq.probabilities(qubits=(1,)),
                        fq.expectation(fq.X(1), name='bx'),
                        fq.expectation(fq.Y(1), name='by')])
            expected = torch.zeros(4, dtype=D)
            for i in (0, 1):
                expected[2*(i ^ choice)+i] = cmath.exp(1j*phi*i)/math.sqrt(2)
            close(r.statevector()[0], expected)
            close(r.probabilities[0], [.5, .5])
            close(r.expectation('bx')[0], 0.)
            close(r.expectation('by')[0], 0.)
    print('6native circuits:Alice bit/phase choices leave Bob Z probabilities uniform and X/Y means zero.')
    inputs = [(0., 0.), (math.pi, 0.), (math.pi/2, 0.), (.83, -.67), (1.41, .39)]
    for theta, phi in inputs:
        psi = qubit(theta, phi)
        for resource_phase in (0., .71, math.pi):
            r = run(teleport_circuit(psi, resource_phase), [fq.probabilities(qubits=(2,))])
            close(r.statevector()[0], teleport_reference(psi, resource_phase))
            family = teleport_branches(r.statevector()[0])
            for k, (p, v) in enumerate(family):
                m, n = divmod(k, 2)
                close(p, .25)
                expected = torch.tensor([psi[i ^ n]*(-1)**(m*(i ^ n))*cmath.exp(1j*resource_phase*i)
                                         for i in (0, 1)], dtype=D)
                close(v, expected)
                output = correction(m, n)@v
                phase_output = torch.tensor([psi[i]*cmath.exp(1j*resource_phase*(i ^ n)) for i in (0, 1)], dtype=D)
                close(output, phase_output)
                predicted = 1-4*abs(psi[0])**2*abs(psi[1])**2*math.sin(resource_phase/2)**2
                close(abs(torch.vdot(psi, output))**2, predicted)
            for A in (X, Y, Z):
                close(sum(p*mean(v, A) for p, v in family), 0.)
    print('15native teleportation circuits:all60phase-exact branches;missing-message Pauli means vanish;resource-phase fidelity formula passed.')
    for theta, phi in inputs:
        psi = qubit(theta, phi)
        c = fq.Circuit(4, dtype=D).unitary((0,), unitary=prepare(psi)).h(2).cx(2, 3).cx(0, 1)
        r = run(c, [fq.probabilities()])
        actual, target = clone_reference(psi)
        close(r.statevector()[0], actual)
        a, b = psi.tolist()
        overlap = a.conjugate()**2*a+b.conjugate()**2*b
        close(abs(torch.vdot(target, actual))**2, abs(overlap)**2)
        if theta == math.pi/2 and phi == 0:
            close(abs(torch.vdot(target, actual))**2, .5)
    print('5native resource-assisted CNOT candidates:known basis copies work;unknown superpositions fail the full independent-copy target.')
    for a, b in itertools.product((0, 1), repeat=2):
        for decoded in (False, True):
            c = fq.Circuit(2, dtype=D).h(0).cx(0, 1)
            if b:
                c.x(0)
            if a:
                c.z(0)
            if decoded:
                c.cx(0, 1).h(0)
            r = run(c, [fq.probabilities(qubits=(1,), name='bob'), fq.probabilities(qubits=(0, 1), name='joint')])
            # Two probability requests require names rather than an ambiguous shortcut.
            marginal = r.measurement('bob').value[0]
            if decoded:
                expected = torch.zeros(4, dtype=D); expected[2*a+b] = 1.
                close(r.statevector()[0], expected)
                close(marginal, [1-b, b])
            else:
                close(marginal, [.5, .5])
                close(r.statevector()[0], swapping.bell(a, b))
    print('8native dense-coding stages:Bob alone cannot decode;the joint decoder recovers four messages only with both qubits.')
    r = run(swapping.source(), [fq.probabilities(qubits=(0, 3))])
    family = swapping.branches(r.statevector()[0])
    for k, (p, v) in enumerate(family):
        m, n = divmod(k, 2)
        correct = torch.kron(I, correction(m, n))@v
        stale = torch.kron(I, correction(m ^ 1, n))@v
        close(abs(torch.vdot(swapping.bell(0, 0), correct))**2, 1.)
        close(abs(torch.vdot(swapping.bell(0, 0), stale))**2, 0.)
        close(abs(torch.linalg.det(stale.reshape(2, 2))), .5)
    print('1native swap:all four stale-phase frames preserve entanglement but give zero Phi+ target fidelity.')
    settings = ((0., 0.), (0., math.pi/2), (math.pi/2, 0.), (math.pi/2, math.pi/2),
                (0., math.pi/4), (0., -math.pi/4), (math.pi/2, math.pi/4), (math.pi/2, -math.pi/4))
    values = []
    for alpha, beta in settings:
        c = fq.Circuit(2, dtype=D).h(0).cx(0, 1).ry(0, -alpha).ry(1, -beta)
        r = run(c, [fq.probabilities(), fq.expectation(fq.Z(0)@fq.Z(1), name='e')])
        e = correlation(alpha, beta); values.append(e)
        close(r.expectation('e')[0], e)
        predicted = [(1+(-1)**(a+b)*e)/4 for a, b in itertools.product((0, 1), repeat=2)]
        close(r.probabilities[0], predicted)
        if (alpha, beta) in settings[:4]:
            close(r.probabilities[0], local_table(int(alpha != 0), int(beta != 0)))
    close(sum(s*v for s, v in zip((1, 1, 1, -1), values[:4])), 0.)
    close(sum(s*v for s, v in zip((1, 1, 1, -1), values[4:])), 2*math.sqrt(2))
    print('8native Bell contexts:same maximally entangled state gives S=0 or2sqrt(2);explicit local Z/X table matches the former.')
    for k in range(1, 5):
        for roles in (tuple(range(2*k)), tuple(reversed(range(2*k)))):
            roles = pair_contract(k, roles)
            c = fq.Circuit(2*k, dtype=D)
            for j in range(k):
                c.h(roles[j]).cx(roles[j], roles[k+j])
            r = run(c, [fq.probabilities(), fq.samples()], shots=11)
            ref = pair_reference(k, roles)
            close(r.statevector()[0], ref)
            close(r.probabilities[0], ref.abs().square())
            assert r.samples.shape == (1, 11, 2*k)
            for row in r.samples[0].tolist():
                assert all(row[roles[j]] == row[roles[k+j]] for j in range(k))
    print('8native pair-family circuits:one to four pairs,two role orders;exact fair-bit classical sampler and record constraints passed.')
    guards = [
        lambda: vector(torch.ones(2, dtype=D)),
        lambda: vector(torch.tensor([1., 0.])),
        lambda: angle(float('nan')),
        lambda: correction(2, 0),
        lambda: correction(True, 0),
        lambda: teleport_branches(torch.ones(8, dtype=D)),
        lambda: pair_contract(0),
        lambda: pair_contract(5),
        lambda: pair_contract(2, (0, 0, 2, 3)),
        lambda: pair_contract(2, [0, 1, 2, 3]),
        lambda: pair_index((0, 2), (0, 1, 2, 3)),
        lambda: run(fq.Circuit(2), [fq.probabilities()], shots=0),
    ]
    before = RUNS
    for guard in guards:
        try:
            guard()
        except ValueError:
            pass
        else:
            raise AssertionError('Malformed contract accepted')
    assert RUNS == before == 51
    print('12malformed contracts rejected before execution;51CPUcomplex128native circuits passed.')
    print('Task counterexamples do not prove a general classical simulation theorem,capacity bound or hardware/network advantage.')


if __name__ == '__main__':
    main()
