"""6.1: projective Born probabilities, native computational marginals and explicit postprocessing.

No samples, collapse update or direct general-projector hardware execution.
"""
from itertools import product, permutations
from importlib.metadata import version
from math import cos, sin, pi, sqrt, isfinite
import cmath
import torch
import flagquantum as fq
try:
    from examples.foundations.tensor_spaces import prepare_matrix, OPTIONS
    from examples.foundations.circuit_composition import product_input
    from examples.foundations.reversible_logic import basis_factors, complex_factors
except ModuleNotFoundError:
    from tensor_spaces import prepare_matrix, OPTIONS
    from circuit_composition import product_input
    from reversible_logic import basis_factors, complex_factors
D = torch.complex128
ATOL = 1e-12
RUNS = 0


def dimension(n):
    if type(n) is not int or not 1 <= n <= 4:
        raise ValueError('Dense teaching reference uses 1-4 qubits')
    return 2**n


def selection(n, qubits):
    dimension(n)
    if not isinstance(qubits, tuple) or not qubits or any(type(q) is not int or not 0 <= q < n for q in qubits) or len(set(qubits)) != len(qubits):
        raise ValueError('Declare distinct ordered qubit positions')
    return qubits


def basis_family(n):
    d = dimension(n)
    eye = torch.eye(d, dtype=D)
    return tuple(torch.outer(v, v.conj()) for v in eye), tuple(format(j, f'0{n}b') for j in range(d))


def marginal_family(n, qubits):
    qubits = selection(n, qubits)
    d = dimension(n); k = len(qubits)
    labels = tuple(format(j, f'0{k}b') for j in range(2**k))
    matrices = []
    for label in labels:
        diagonal = [int(''.join(format(j, f'0{n}b')[q] for q in qubits) == label) for j in range(d)]
        matrices.append(torch.diag(torch.tensor(diagonal, dtype=D)))
    return tuple(matrices), labels


def parity_family(n):
    d = dimension(n)
    even = torch.diag(torch.tensor([int(j.bit_count()%2 == 0) for j in range(d)], dtype=D))
    return (even, torch.eye(d, dtype=D)-even), ('even','odd')


def xx_family():
    # Independent explicit pair-flip matrix in order00,01,10,11.
    pair_flip = torch.tensor([[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]], dtype=D)
    eye = torch.eye(4, dtype=D)
    return ((eye+pair_flip)/2, (eye-pair_flip)/2), ('plus','minus')


def born(state, projectors, labels):
    if not isinstance(state, torch.Tensor) or state.ndim != 1 or state.numel() not in (2,4,8,16) or state.dtype != D or state.device.type != 'cpu' or not torch.isfinite(state).all():
        raise ValueError('Finite unbatched CPU complex128 state required')
    if abs(torch.vdot(state,state).item()-1) > ATOL:
        raise ValueError('Normalized state required; no normalization repair')
    if not isinstance(projectors, tuple) or not projectors or not isinstance(labels, tuple) or len(labels) != len(projectors) or any(type(label) is not str or not label for label in labels) or len(set(labels)) != len(labels):
        raise ValueError('Nonempty projector tuple with distinct declared string labels required')
    d = state.numel(); eye = torch.eye(d, dtype=D)
    for P in projectors:
        if not isinstance(P, torch.Tensor) or P.shape != (d,d) or P.dtype != D or P.device.type != 'cpu' or not torch.isfinite(P).all():
            raise ValueError('Projector shape/dtype/finite contract violated')
        if not torch.allclose(P,P.mH,rtol=0,atol=ATOL) or not torch.allclose(P@P,P,rtol=0,atol=ATOL):
            raise ValueError('Hermitian idempotent projectors required')
    for j, P in enumerate(projectors):
        for Q in projectors[j+1:]:
            if not torch.allclose(P@Q,torch.zeros_like(eye),rtol=0,atol=ATOL):
                raise ValueError('Mutually orthogonal projectors required')
    if not torch.allclose(sum(projectors,torch.zeros_like(eye)),eye,rtol=0,atol=ATOL):
        raise ValueError('Complete projector family required')
    values = []
    for P in projectors:
        projected = P @ state
        probability = torch.vdot(projected,projected).real
        quadratic = torch.vdot(state,P@state)
        assert abs(quadratic.imag.item()) < ATOL
        assert abs(probability.item()-quadratic.real.item()) < ATOL
        values.append(probability)
    result = torch.stack(values)
    assert torch.isfinite(result).all() and bool((result >= 0).all())
    assert abs(result.sum().item()-1) < ATOL
    return result


def run(block, factors, selected=None):
    global RUNS
    n = block.n_qubits; d = dimension(n)
    if len(factors) != n:
        raise ValueError('One normalized preparation per qubit required')
    if selected is not None: selection(n, selected)
    circuit = fq.Circuit(n,dtype=D)
    for q, factor in enumerate(factors):
        circuit.unitary(q,unitary=prepare_matrix(torch.tensor(factor,dtype=D)))
    circuit.compose(block)
    request = fq.probabilities() if selected is None else fq.probabilities(qubits=selected)
    result = fq.run(circuit,outputs=[request],options=OPTIONS)
    v,p = result.statevector(),result.probabilities
    expected_outcomes = d if selected is None else 2**len(selected)
    assert v.shape == (1,d) and p.shape == (1,expected_outcomes)
    assert v.dtype == D and p.dtype == torch.float64 and v.device.type == p.device.type == 'cpu'
    assert torch.isfinite(v).all() and torch.isfinite(p).all()
    RUNS += 1
    return v[0],p[0]


def bell(phi=0., global_phase=0.):
    if any(type(t) not in (int,float) or not isfinite(t) for t in (phi,global_phase)):
        raise ValueError('Finite literal radian phases required')
    scalar = cmath.exp(1j*global_phase)
    return fq.Circuit(2,dtype=D).h(0).cx(0,1).p(0,phi).unitary(0,unitary=scalar*torch.eye(2,dtype=D))


def main():
    assert version('flagquantum') == '0.3.1' and version('torch').split('+')[0] == '2.13.0'
    for n in (1,2,3):
        families = [basis_factors(bits) for bits in product((0,1),repeat=n)] + [complex_factors(n)]
        for factors in families:
            v,p = run(fq.Circuit(n,dtype=D),factors)
            torch.testing.assert_close(v,product_input(factors),rtol=0,atol=ATOL)
            P,labels = basis_family(n)
            torch.testing.assert_close(born(v,P,labels),p,rtol=0,atol=ATOL)
            Q,names = parity_family(n)
            predicted = torch.tensor([sum(p[j].item() for j in range(2**n) if j.bit_count()%2 == a) for a in (0,1)],dtype=torch.float64)
            torch.testing.assert_close(born(v,Q,names),predicted,rtol=0,atol=ATOL)
    print('17 computational-basis circuits: all 1/2/3-qubit basis inputs and complex products; full vectors, Born probabilities and parity sums passed.')
    for k in (1,2,3):
        for selected in permutations(range(3),k):
            P,labels = marginal_family(3,selected)
            for factors in [basis_factors(bits) for bits in product((0,1),repeat=3)] + [complex_factors(3)]:
                v,p = run(fq.Circuit(3,dtype=D),factors,selected)
                torch.testing.assert_close(v,product_input(factors),rtol=0,atol=ATOL)
                torch.testing.assert_close(born(v,P,labels),p,rtol=0,atol=ATOL)
                expected = torch.zeros(2**k,dtype=torch.float64)
                for j,z in enumerate(product_input(factors)):
                    key = int(''.join(format(j,'03b')[q] for q in selected),2)
                    expected[key] += abs(z)**2
                torch.testing.assert_close(p,expected,rtol=0,atol=ATOL)
    print('135 native marginal circuits: all 15 ordered nonempty qubit selections, all 8 basis inputs and a complex product passed.')
    P,labels = xx_family()
    for phi in (0.,pi/2,pi,-.43):
        predictions = []
        for chi in (0.,.71):
            v,p = run(bell(phi,chi),basis_factors((0,0)))
            reference = torch.zeros(4,dtype=D);reference[0]=cmath.exp(1j*chi)/sqrt(2);reference[3]=cmath.exp(1j*(chi+phi))/sqrt(2)
            torch.testing.assert_close(v,reference,rtol=0,atol=ATOL)
            torch.testing.assert_close(p,torch.tensor([.5,0,0,.5],dtype=torch.float64),rtol=0,atol=ATOL)
            q = born(v,P,labels)
            torch.testing.assert_close(q,torch.tensor([(1+cos(phi))/2,(1-cos(phi))/2],dtype=torch.float64),rtol=0,atol=ATOL)
            predictions.append(q)
        torch.testing.assert_close(*predictions,rtol=0,atol=ATOL)
    print('8 phase-sensitive Bell circuits: explicit XX-projector postprocessing matches the cosine law; global phase leaves every probability unchanged.')
    for theta in (0.,.8,pi):
        v,p = run(fq.Circuit(3,dtype=D).ry(0,theta).cx(0,2).x(1),basis_factors((0,0,0)))
        reference = torch.zeros(8,dtype=D);reference[2]=cos(theta/2);reference[7]=sin(theta/2)
        torch.testing.assert_close(v,reference,rtol=0,atol=ATOL)
        torch.testing.assert_close(p,reference.abs().square(),rtol=0,atol=ATOL)
    print('3 sparse-register circuits: 010/111 amplitudes and indices 2/7 checked at zero, generic and pi angles.')
    v=torch.tensor([1,0],dtype=D);P,labels=basis_family(1);I=torch.eye(2,dtype=D)
    zero=torch.zeros_like(I)
    torch.testing.assert_close(born(v,P+(zero,),labels+('never',)),torch.tensor([1.,0.,0.]),rtol=0,atol=ATOL,check_dtype=False)
    oblique=torch.tensor([[1,1],[0,0]],dtype=D)
    invalid=[lambda:born(2*v,P,labels),lambda:born(torch.zeros_like(v),P,labels),
             lambda:born(v.real,P,labels),lambda:born(torch.tensor([float('nan'),0],dtype=D),P,labels),
             lambda:born(v,(oblique,I-oblique),labels),lambda:born(v,(I/2,I/2),labels),
             lambda:born(v,P[:1],labels[:1]),lambda:born(v,(P[0],P[0],P[1]),('a','b','c')),
             lambda:born(v,P,('same','same')),lambda:born(v,(torch.eye(4,dtype=D),),('all',)),
             lambda:marginal_family(3,(0,0)),lambda:marginal_family(3,(True,))]
    for call in invalid:
        try:call()
        except ValueError:pass
        else:raise AssertionError('Malformed projective-probability contract admitted')
    assert RUNS == 163, RUNS
    print('12 malformed contracts rejected; zero-probability labels retained; no renormalization, clipping or state-update inference.')
    print('163 actual CPU complex128 circuits; implementation atol 1e-12, rtol 0; exact probabilities, not finite-shot or hardware observations.')
    print('General projectors are explicit classical postprocessing of a simulated state; not a claimed native general-measurement API.')


if __name__ == '__main__':main()
