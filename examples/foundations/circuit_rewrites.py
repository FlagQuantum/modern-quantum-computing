"""5.8: exact local rewrite contracts, full-phase checks, conservative book-side cancellation."""
from itertools import product
from importlib.metadata import version
from math import pi, sqrt, isfinite
import cmath
import torch
import flagquantum as fq
try:
    from examples.foundations.pauli_rotations import explicit
    from examples.foundations.circuit_composition import execute, product_input
    from examples.foundations.reversible_logic import basis_factors, complex_factors
except ModuleNotFoundError:
    from pauli_rotations import explicit
    from circuit_composition import execute, product_input
    from reversible_logic import basis_factors, complex_factors
D = torch.complex128
ATOL = 1e-12
RUNS = 0
FIXED = {'h', 'x', 'y', 'z', 's', 'sdg', 't', 'tdg', 'cx'}
ANGULAR = {'rx', 'ry', 'rz', 'p', 'crx', 'rzz'}
INVERSE = {'h':'h', 'x':'x', 'y':'y', 'z':'z', 's':'sdg', 'sdg':'s', 't':'tdg', 'tdg':'t', 'cx':'cx'}


def validate(n, program):
    if type(n) is not int or not 1 <= n <= 4 or not isinstance(program, tuple):
        raise ValueError('Teaching program requires 1-4 qubits and an instruction tuple')
    for inst in program:
        if not isinstance(inst, tuple) or len(inst) != 3:
            raise ValueError('Instruction is (name, ordered support, angle tuple)')
        name, qs, params = inst
        if type(name) is not str or name not in FIXED | ANGULAR:
            raise ValueError('Unsupported gate; measurement/reset/barrier not admitted')
        arity = 2 if name in {'cx', 'crx', 'rzz'} else 1
        if not isinstance(qs, tuple) or len(qs) != arity or any(type(q) is not int or not 0 <= q < n for q in qs) or len(set(qs)) != arity:
            raise ValueError('Declared distinct ordered qubit positions required')
        if not isinstance(params, tuple) or len(params) != (1 if name in ANGULAR else 0):
            raise ValueError('Declared angle arity required')
        if any(type(t) not in (int, float) or not isfinite(t) or abs(t) > 100 for t in params):
            raise ValueError('Fixed finite literal radian angles, absolute value <=100 required')


def compile_program(n, program):
    validate(n, program)
    result = fq.Circuit(n, dtype=D)
    for name, qs, params in program:
        getattr(result, name)(*qs, *params)
    return result


def cancellation(n, program):
    validate(n, program)
    stack = []
    for name, qs, params in program:
        if name in ANGULAR and params == (0,):
            continue
        inst = (name, qs, params)
        if stack:
            old_name, old_qs, old_params = stack[-1]
            fixed_inverse = name in FIXED and old_name in FIXED and INVERSE[name] == old_name
            angle_inverse = name in ANGULAR and name == old_name and params[0] == -old_params[0]
            if qs == old_qs and (fixed_inverse or angle_inverse):
                stack.pop()
                continue
        stack.append(inst)
    return tuple(stack)


def local_matrix(name, params):
    if name in {'rx','ry','rz'}:
        return explicit(name[1], params[0])
    if name == 'h':
        return torch.tensor([[1,1],[1,-1]], dtype=D)/sqrt(2)
    if name == 'x': return torch.tensor([[0,1],[1,0]], dtype=D)
    if name == 'y': return torch.tensor([[0,-1j],[1j,0]], dtype=D)
    if name == 'z': return torch.diag(torch.tensor([1,-1], dtype=D))
    theta = {'s':pi/2, 'sdg':-pi/2, 't':pi/4, 'tdg':-pi/4}.get(name, params[0] if params else 0)
    return torch.diag(torch.tensor([1, cmath.exp(1j*theta)], dtype=D))


def operator(n, inst):
    validate(n, (inst,))
    name, qs, params = inst
    out = torch.zeros((2**n, 2**n), dtype=D)
    for j in range(2**n):
        if name in {'cx','crx'}:
            c, t = qs; control = (j >> (n-1-c)) & 1
            if not control:
                out[j,j] = 1
                continue
            U = local_matrix('x', ()) if name == 'cx' else explicit('x', params[0])
        elif name == 'rzz':
            parity = ((j >> (n-1-qs[0])) ^ (j >> (n-1-qs[1]))) & 1
            out[j,j] = cmath.exp(-.5j*params[0]*(1-2*parity))
            continue
        else:
            t = qs[0]; U = local_matrix(name, params)
        mask = 1 << (n-1-t); bit = int(bool(j & mask))
        for e in (0,1):
            out[(j & ~mask) | (e << (n-1-t)), j] = U[e,bit]
    return out


def matrix(n, program):
    validate(n, program)
    total = torch.eye(2**n, dtype=D)
    for inst in program:
        total = operator(n, inst) @ total
    return total


def run(block, factors):
    global RUNS
    v,p = execute(block,factors); RUNS += 1
    return v,p


def inputs(n):
    return [basis_factors(bits) for bits in product((0,1),repeat=n)] + [complex_factors(n)]


def check(n, left, right):
    U,V = matrix(n,left),matrix(n,right)
    torch.testing.assert_close(U,V,rtol=0,atol=ATOL)
    for f in inputs(n):
        expected = U @ product_input(f)
        for program in (left,right):
            v,_ = run(compile_program(n,program),f)
            torch.testing.assert_close(v,expected,rtol=0,atol=ATOL)


def main():
    assert version('flagquantum') == '0.3.1' and version('torch').split('+')[0] == '2.13.0'
    cases = []
    for name in ('h','x','y','z'):
        cases.append((1,((name,(0,),()),(name,(0,),()))))
    for name,inverse in (('s','sdg'),('t','tdg')):
        cases.append((1,((name,(0,),()),(inverse,(0,),()))))
    cases += [(1,(('ry',(0,),(.37,)),('ry',(0,),(-.37,)))),
              (1,(('p',(0,),(.23,)),('p',(0,),(-.23,)))),
              (1,(('rx',(0,),(0.,)),)),(1,(('rx',(0,),(2*pi,)),)),
              (2,(('cx',(0,1),()),('cx',(0,1),()))),
              (2,(('h',(0,),()),('cx',(0,1),()),('cx',(0,1),()),('h',(0,),()))),
              (2,(('cx',(0,1),()),('cx',(1,0),()))),
              (2,(('h',(0,),()),('t',(0,),()),('h',(0,),()))),
              (2,(('rzz',(1,0),(.4,)),('rzz',(1,0),(-.4,))))]
    for n,program in cases:
        reduced = cancellation(n,program)
        assert len(reduced) <= len(program) and cancellation(n,reduced) == reduced
        check(n,program,reduced)
    assert cancellation(1,(('rx',(0,),(2*pi,)),)) != ()
    assert len(cancellation(2,(('cx',(0,1),()),('cx',(1,0),())))) == 2
    print('15 cancellation programs: exact inverses, nested pairs, zero/full-turn and ordered-support boundaries passed.')
    for name in ('rx','ry','rz','p'):
        for theta,phi in ((.23,.37),(pi,pi),(.43,-.43)):
            check(1,((name,(0,),(theta,)),(name,(0,),(phi,))),((name,(0,),(theta+phi,)),))
    print('12 same-generator/phase merges: basis and complex vectors checked without modulo-2*pi rotation deletion.')
    left=(('rx',(0,),(.41,)),('rz',(2,),(-.37,)))
    check(3,left,tuple(reversed(left)))
    prep=(('h',(0,),()),('cx',(0,2),()))
    for program in (prep+left,prep+tuple(reversed(left))):
        v,_=run(compile_program(3,program),basis_factors((0,0,0)))
        torch.testing.assert_close(v,matrix(3,prep+left) @ product_input(basis_factors((0,0,0))),rtol=0,atol=ATOL)
    print('Disjoint supports: all 3-qubit basis/complex inputs plus 2 correlated-input circuits passed.')
    for name,q in (('rz',0),('rx',1)):
        for theta in (.31,0.,2*pi):
            gate=(name,(q,),(theta,));cx=('cx',(0,1),())
            check(2,(gate,cx),(cx,gate))
    theta=.61;cx=('cx',(0,1),());rz=('rz',(1,),(theta,));rzz=('rzz',(0,1),(theta,))
    check(2,(cx,rz),(rzz,cx))
    assert not torch.allclose(matrix(2,(cx,rz)),matrix(2,(rz,cx)),rtol=0,atol=ATOL)
    for f in inputs(2):
        v,_=run(compile_program(2,(rz,cx)),f)
        torch.testing.assert_close(v,matrix(2,(rz,cx)) @ product_input(f),rtol=0,atol=ATOL)
    print('6 valid shared-support commutations and CX/Rz-to-RZZ propagation passed; unchanged-target-Rz swap rejected by full operators.')
    h=('h',(0,),())
    for name,out,sign in (('rx','rz',1),('rz','rx',1),('ry','ry',-1)):
        for theta in (.47,0.,2*pi):
            check(1,(h,(name,(0,),(theta,)),h),((out,(0,),(sign*theta,)),))
    print('9 Hadamard conjugations: axes and the Ry angle sign passed at generic, zero and full-turn angles.')
    first=(('rx',(0,),(pi/2,)),('rz',(0,),(pi/2,)),h)
    second=(('rz',(0,),(pi/2,)),('rx',(0,),(pi/2,)),h)
    for f in inputs(1):
        for program in (first,second):
            v,_=run(compile_program(1,program),f)
            torch.testing.assert_close(v,matrix(1,program) @ product_input(f),rtol=0,atol=ATOL)
    assert not torch.allclose(matrix(1,first),matrix(1,second),rtol=0,atol=ATOL)
    native=(('crx',(0,1),(pi,)),);wrong=(('cx',(0,1),()),)
    corrected=(('p',(0,),(-pi/2,)),('cx',(0,1),()))
    check(2,native,corrected)
    assert not torch.allclose(matrix(2,native),matrix(2,wrong),rtol=0,atol=ATOL)
    for f in inputs(2):
        v,_=run(compile_program(2,wrong),f)
        torch.testing.assert_close(v,matrix(2,wrong) @ product_input(f),rtol=0,atol=ATOL)
    tail=(('cx',(0,1),()),('h',(0,),()))
    probs=[]
    for program in (native,wrong,corrected):
        v,p=run(compile_program(2,program+tail),[(1/sqrt(2),1/sqrt(2)),(1,0)])
        probs.append(p[0].item())
    assert max(abs(p-e) for p,e in zip(probs,(.5,1.,.5))) < ATOL
    print('Noncommuting rotations and controlled Rx(pi)-to-X phase witness passed; corrected control phase retained.')
    invalid=[lambda: cancellation(0,()),lambda: cancellation(2,(('cx',(0,0),()),)),
             lambda: compile_program(2,(('cx',(0,2),()),)),lambda: compile_program(1,(('rz',(0,),(float('nan'),)),)),
             lambda: compile_program(1,(('rx',(0,),(True,)),)),lambda: compile_program(1,(('reset',(0,),()),)),
             lambda: cancellation(1,[('h',(0,),())]),lambda: compile_program(1,(('h',(0,),(1.,)),)),
             lambda: compile_program(1,(('ry',(0,),()),)),lambda: cancellation(2,(('cx',(True,1),()),))]
    for call in invalid:
        try: call()
        except ValueError: pass
        else: raise AssertionError('Malformed rewrite contract admitted')
    assert RUNS == 355, RUNS
    print(f'{RUNS} actual CPU complex128 circuits; full-phase atol 1e-12, rtol 0; 10 malformed contracts rejected.')
    print('Conservative book-side cancellation only; no native optimizer, approximate rewrite, gradient, measurement, noise or hardware claim.')


if __name__ == '__main__':
    main()
