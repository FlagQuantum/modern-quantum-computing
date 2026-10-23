"""7.5: phase-preserving teleportation branches and explicit execution boundaries.

Native static gates/terminal queries; ideal projections are classical analysis.
Bob branch tests re-prepare simulator-known states and are not dynamic feedforward.
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
X = torch.tensor([[0, 1], [1, 0]], dtype=D)
Z = torch.diag(torch.tensor([1, -1], dtype=D))
Y = torch.tensor([[0, -1j], [1j, 0]], dtype=D)
I = torch.eye(2, dtype=D)


def vector(v, size):
    if (not isinstance(v, torch.Tensor) or v.shape != (size,) or v.dtype != D
            or v.device.type != 'cpu' or v.layout != torch.strided or not bool(torch.isfinite(v).all())):
        raise ValueError('Finite unbatched dense CPU complex128 vector of the declared size required')
    if abs(torch.vdot(v, v).item()-1) > ATOL:
        raise ValueError('Normalized state required; no input repair')
    return v


def prepare_matrix(v):
    vector(v, 2)
    a, b = v.tolist()
    return torch.tensor([[a, -b.conjugate()], [b, a.conjugate()]], dtype=D)


def roles_contract(n, roles):
    if (type(n) is not int or not 3 <= n <= 4 or type(roles) is not tuple or len(roles) != 3
            or any(type(q) is not int or not 0 <= q < n for q in roles) or len(set(roles)) != 3):
        raise ValueError('Distinct ordered (source,Alice-half,Bob) roles in a3-4qubit teaching register required')
    return roles


def message(bits):
    if type(bits) is not tuple or len(bits) != 2 or any(type(b) is not int or b not in (0, 1) for b in bits):
        raise ValueError('Two literal bits in semantic (m,n) order required')
    return bits


def decode_record(row, columns, roles=(0, 1, 2)):
    source, alice, _ = roles_contract(max(roles)+1, roles)
    if type(columns) is not tuple or len(columns) != 2 or set(columns) != {source, alice}:
        raise ValueError('Declare both measured qubit columns exactly once')
    if (not isinstance(row, torch.Tensor) or row.shape != (2,) or row.dtype != torch.int64
            or row.device.type != 'cpu' or not bool(((row == 0) | (row == 1)).all())):
        raise ValueError('One complete CPU int64 binary record required')
    return message((int(row[columns.index(source)]), int(row[columns.index(alice)])))


def byproduct(v, bits):
    a, b = vector(v, 2).tolist(); m, n = message(bits)
    return torch.tensor([a, (-1)**m*b] if n == 0 else [(-1)**m*b, a], dtype=D)


def correction_matrix(bits):
    m, n = message(bits)
    return (Z if m else I)@(X if n else I)


def circuit(v, stage='decoded', n=3, roles=(0, 1, 2)):
    vector(v, 2); source, alice, bob = roles_contract(n, roles)
    if stage not in ('resource', 'decoded', 'coherent', 'reverse-coherent'):
        raise ValueError('Declare resource,decoded,coherent or reverse-coherent stage')
    c = fq.Circuit(n, dtype=D).unitary(source, unitary=prepare_matrix(v)).h(alice).cx(alice, bob)
    for q in range(n):
        if q not in roles: c.ry(q, .61).p(q, -.37)
    if stage != 'resource': c.cx(source, alice).h(source)
    if stage == 'coherent': c.cx(alice, bob).cz(source, bob)
    if stage == 'reverse-coherent': c.cz(source, bob).cx(alice, bob)
    return c


def scalar_state(v, stage='decoded', n=3, roles=(0, 1, 2)):
    a, b = vector(v, 2).tolist(); source, alice, bob = roles_contract(n, roles)
    if stage not in ('resource', 'decoded', 'coherent', 'reverse-coherent'):
        raise ValueError('Unknown stage')
    out = []
    for k in range(2**n):
        bits = [int(x) for x in format(k, f'0{n}b')]
        m, s, z = bits[source], bits[alice], bits[bob]
        if stage == 'resource': value = (a if m == 0 else b)/math.sqrt(2) if s == z else 0j
        elif stage == 'decoded':
            value = ([a, (-1)**m*b] if s == 0 else [(-1)**m*b, a])[z]/2
        else: value = (a if z == 0 else b)*((-1)**(m*s) if stage == 'reverse-coherent' else 1)/2
        for q in range(n):
            if q not in roles:
                value *= math.cos(.61/2) if bits[q] == 0 else cmath.exp(-.37j)*math.sin(.61/2)
        out.append(value)
    return torch.tensor(out, dtype=D)


def query(v, stage='decoded', n=3, roles=(0, 1, 2), shots=None, seed=37, columns=None):
    global RUNS
    source, alice, bob = roles_contract(n, roles); vector(v, 2)
    if type(seed) is not int or seed < 0 or (shots is not None and (type(shots) is not int or shots < 1)):
        raise ValueError('Nonnegative seed and positive literal shot count required')
    columns = (source, alice) if columns is None else columns
    if type(columns) is not tuple or len(columns) != 2 or set(columns) != {source, alice}:
        raise ValueError('Declare both measured qubit columns exactly once')
    c = circuit(v, stage, n, roles)
    outputs = [fq.probabilities(qubits=columns)]
    outputs += [fq.expectation(op(bob), name=name) for op, name in [(fq.X, 'x'), (fq.Y, 'y'), (fq.Z, 'z')]]
    outputs.append(fq.expectation(fq.X(source)@fq.X(alice), name='alice_xx'))
    if shots is not None: outputs.append(fq.samples(qubits=columns))
    result = fq.run(c, outputs=outputs, options=replace(OPTIONS, seed=seed), **({} if shots is None else {'shots': shots}))
    RUNS += 1
    state = result.statevector()
    assert state.shape == (1, 2**n) and state.dtype == D
    assert torch.allclose(state[0], scalar_state(v, stage, n, roles), atol=ATOL, rtol=0)
    assert result.probabilities.shape == (1, 4)
    if stage != 'resource': assert torch.allclose(result.probabilities[0], torch.full((4,), .25, dtype=torch.float64), atol=ATOL, rtol=0)
    expected = torch.zeros(4, dtype=torch.float64)
    for k, amplitude in enumerate(state[0].tolist()):
        key = 2*((k>>(n-1-columns[0]))&1)+((k>>(n-1-columns[1]))&1)
        expected[key] += abs(amplitude)**2
    assert torch.allclose(result.probabilities[0], expected, atol=ATOL, rtol=0)
    bloch = tuple(float(result.expectation(name)[0]) for name in ('x', 'y', 'z'))
    target = tuple(float(torch.vdot(v, op@v).real) for op in (X, Y, Z)) if stage in ('coherent', 'reverse-coherent') else (0., 0., 0.)
    assert all(abs(x-y) < ATOL for x, y in zip(bloch, target))
    report = {'state': state[0], 'probabilities': result.probabilities[0], 'bloch': bloch,
              'alice_xx': float(result.expectation('alice_xx')[0])}
    if shots is not None:
        raw = result.samples
        assert raw.shape == (1, shots, 2) and raw.dtype == torch.int64
        labels = [decode_record(row, columns, roles) for row in raw[0]]
        counts = torch.bincount(torch.tensor([2*m+s for m,s in labels]), minlength=4)
        assert int(counts.sum()) == shots
        report.update(bits=raw[0], messages=labels, counts=counts)
    return report


def extract(state, measured, bits, kept):
    if not isinstance(state, torch.Tensor): raise ValueError('Dense state tensor required')
    n = state.numel().bit_length()-1
    if state.numel() != 2**n or not 2 <= n <= 4: raise ValueError('Qubit dimension required')
    vector(state, 2**n); message(bits)
    if (type(measured) is not tuple or len(measured) != 2 or type(kept) is not tuple
            or any(type(q) is not int for q in (*measured, *kept))
            or len((*measured, *kept)) != n or sorted((*measured, *kept)) != list(range(n))):
        raise ValueError('Measured and kept ordered positions must partition the register')
    values = []
    for j in range(2**len(kept)):
        assignment = dict(zip(measured, bits)); assignment.update(zip(kept, map(int, format(j, f'0{len(kept)}b'))))
        index = sum(assignment[q]<<(n-1-q) for q in range(n))
        values.append(state[index])
    column = torch.stack(values); p = float(torch.vdot(column, column).real)
    if p == 0:
        if bool((column != 0).any()): raise FloatingPointError('Projected squared norm underflowed')
        raise ValueError('No normalized branch for an impossible outcome')
    return p, column/math.sqrt(p)


def bob_reprepare(v, bits, policy='full'):
    """A new static one-qubit run,not a continuation of a collapsed native run."""
    global RUNS
    vector(v, 2); m, n = message(bits)
    if policy not in ('full', 'none', 'only-n', 'only-m', 'swap', 'reverse'):
        raise ValueError('Unknown declared correction policy')
    c = fq.Circuit(1, dtype=D).unitary(0, unitary=prepare_matrix(v))
    if policy == 'swap': m, n = n, m
    if policy == 'reverse':
        if m: c.z(0)
        if n: c.x(0)
    else:
        if n and policy in ('full', 'only-n', 'swap'): c.x(0)
        if m and policy in ('full', 'only-m', 'swap'): c.z(0)
    result = fq.run(c, outputs=[fq.probabilities(), fq.expectation(fq.X(0), name='x'),
        fq.expectation(fq.Y(0), name='y'), fq.expectation(fq.Z(0), name='z')], options=OPTIONS)
    RUNS += 1
    state = result.statevector()[0]
    expected = v
    if policy == 'reverse': expected = (X if n else I)@(Z if m else I)@v
    else:
        if n and policy in ('full', 'only-n', 'swap'): expected = X@expected
        if m and policy in ('full', 'only-m', 'swap'): expected = Z@expected
    assert torch.allclose(state, expected, atol=ATOL, rtol=0)
    assert torch.allclose(result.probabilities[0], state.abs().square(), atol=ATOL, rtol=0)
    return state, tuple(float(result.expectation(name)[0]) for name in ('x', 'y', 'z'))


def reference_pair(theta, phase, stage):
    global RUNS
    if type(theta) not in (int,float) or type(phase) not in (int,float) or not math.isfinite(theta) or not math.isfinite(phase) or stage not in ('decoded','coherent'):
        raise ValueError('Finite reference-pair angles and declared stage required')
    c = fq.Circuit(4, dtype=D).ry(0, theta).p(0, phase).cx(0, 1).ry(1, .41).h(2).cx(2, 3).cx(1, 2).h(1)
    if stage == 'coherent': c.cx(2, 3).cz(1, 3)
    result = fq.run(c, outputs=[fq.probabilities(qubits=(1,2)),
        fq.expectation(fq.X(0)@fq.X(3),name='rb_xx'),fq.expectation(fq.Z(0)@fq.Z(3),name='rb_zz')], options=OPTIONS)
    RUNS += 1
    a,b=math.cos(theta/2),cmath.exp(1j*phase)*math.sin(theta/2)
    co,si=math.cos(.41/2),math.sin(.41/2)
    chi=torch.tensor([a*co,a*si,-b*si,b*co],dtype=D)
    expected=torch.zeros(16,dtype=D)
    for r,m,n,z in itertools.product((0,1),repeat=4):
        if stage=='coherent': amplitude=chi[2*r+z]/2
        else: amplitude=chi[2*r+(z^n)]*((-1)**(m*(z^n)))/2
        expected[8*r+4*m+2*n+z]=amplitude
    state=result.statevector()[0]
    assert torch.allclose(state,expected,atol=ATOL,rtol=0)
    assert torch.allclose(result.probabilities[0],torch.full((4,),.25,dtype=torch.float64),atol=ATOL,rtol=0)
    for bits in itertools.product((0,1),repeat=2):
        p,w=extract(state,(1,2),bits,(0,3));assert abs(p-.25)<ATOL
        if stage=='decoded': w=torch.kron(I,correction_matrix(bits))@w
        assert torch.allclose(w,chi,atol=ATOL,rtol=0)
    if stage=='coherent':
        for op,name in [(X,'rb_xx'),(Z,'rb_zz')]:
            assert abs(float(result.expectation(name)[0])-float(torch.vdot(chi,torch.kron(op,op)@chi).real))<ATOL
    return state,chi


def calibrate(n, roles, bits):
    global RUNS
    source,alice,_=roles_contract(n,roles);m,s=message(bits)
    c=fq.Circuit(n,dtype=D)
    if m:c.x(source)
    if s:c.x(alice)
    result=fq.run(c,outputs=[fq.samples(qubits=(alice,source))],shots=7,options=OPTIONS)
    RUNS+=1
    assert result.samples.shape==(1,7,2)
    assert all(decode_record(row,(alice,source),roles)==bits for row in result.samples[0])


def input_states():
    root=math.sqrt(2)
    return [torch.tensor(v,dtype=D) for v in [(1,0),(0,1),(1/root,1/root),(1/root,-1/root),
            (1/root,1j/root),(1/root,-1j/root),(.6,.8*cmath.exp(.43j)),
            (.6*cmath.exp(.37j),.8*cmath.exp(.08j))]]


def main():
    assert version('flagquantum')=='0.3.1' and RUNS==0
    for v in input_states():
        query(v,'resource');decoded=query(v,shots=32);query(v,'coherent')
        for bits in itertools.product((0,1),repeat=2):
            p,w=extract(decoded['state'],(0,1),bits,(2,))
            assert abs(p-.25)<ATOL and torch.allclose(w,byproduct(v,bits),atol=ATOL,rtol=0)
            corrected,_=bob_reprepare(w,bits)
            assert torch.allclose(corrected,v,atol=ATOL,rtol=0)
    print('56 native circuits:eight inputs,resource/decoder/coherent states and all32 phase-preserving Bob branch corrections passed.')
    v=input_states()[6];policy_states={}
    for policy in ('none','only-n','only-m','swap','reverse'):
        policy_states[policy]=[bob_reprepare(byproduct(v,bits),bits,policy)[0] for bits in itertools.product((0,1),repeat=2)]
    for op in (X,Y,Z):
        mean=sum(float(torch.vdot(w,op@w).real) for w in policy_states['none'])/4
        assert abs(mean)<ATOL
    for j,bits in enumerate(itertools.product((0,1),repeat=2)):
        sign=(-1)**(bits[0]*bits[1]);assert torch.allclose(policy_states['reverse'][j],sign*v,atol=ATOL,rtol=0)
        if bits in ((0,1),(1,0)): assert abs(torch.vdot(v,policy_states['swap'][j]))**2 < 1-.01
    for policy,preserved in [('only-n',Z),('only-m',X)]:
        for op in (X,Y,Z):
            mean=sum(float(torch.vdot(w,op@w).real) for w in policy_states[policy])/4
            target=float(torch.vdot(v,op@v).real) if op is preserved else 0.
            assert abs(mean-target)<ATOL
    print('20 native Bob re-preparations:no-message/one-bit/two-bit ordering and branch-global-phase distinctions passed.')
    for n in (3,4):
        for roles in itertools.permutations(range(n),3):
            v=input_states()[7]
            query(v,'decoded',n,roles);query(v,'coherent',n,roles)
    print('60 native circuits:all ordered role triples in three/four qubits,complex spectator factors and full amplitudes passed.')
    for theta,phase in [(.72,.37),(math.pi/2,0.),(1.2,-.56)]:
        reference_pair(theta,phase,'decoded');reference_pair(theta,phase,'coherent')
    print('6 native reference-input circuits:all conditional joint R/B states and coherent transferred correlations passed.')
    for n,roles in [(3,(0,1,2)),(3,(2,0,1)),(4,(3,1,0))]:
        for bits in itertools.product((0,1),repeat=2):calibrate(n,roles,bits)
    print('12 native basis calibrations:reversed raw columns decode into semantic messages(m,n).')
    reverse=query(input_states()[6],'reverse-coherent')
    assert abs(reverse['alice_xx'])<ATOL
    print('1 native reversed coherent correction:Bob is correct but Alice joint coherence differs from the phase-fixed identity.')
    v=input_states()[6];basis=torch.zeros(8,dtype=D);basis[0]=1
    bad=[lambda:prepare_matrix(torch.ones(3,dtype=D)),lambda:prepare_matrix(2*v),
         lambda:prepare_matrix(v.real),lambda:prepare_matrix(torch.tensor([float('nan'),0],dtype=D)),
         lambda:roles_contract(True,(0,1,2)),lambda:roles_contract(3,(0,0,2)),
         lambda:message((True,0)),lambda:message((0,)),lambda:message((0,2)),
         lambda:bob_reprepare(v,(0,0),'unknown'),lambda:extract(basis[None,:],(0,1),(0,0),(2,)),
         lambda:extract(basis,(0,1),(0,0),(1,)),lambda:extract(basis,(0,1),(1,1),(2,)),
         lambda:decode_record(torch.tensor([0,2]),(0,1)),
         lambda:decode_record(torch.tensor([0.,1.]),(0,1)),lambda:decode_record(torch.tensor([0,1]),(0,2))]
    for attempt in bad:
        before=RUNS
        try:attempt()
        except ValueError:pass
        else:raise AssertionError('Malformed teleportation contract admitted')
        assert RUNS==before
    print('16 malformed contracts rejected before another native execution.')
    assert RUNS==155,RUNS
    print('155 CPU complex128 native circuits passed;host branch re-preparation is not native dynamic teleportation.')


if __name__=='__main__':main()
