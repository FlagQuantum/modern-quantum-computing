"""Section5.6: phase-exact controlled gates,Toffoli,and clean/dirty ancilla contracts."""
from itertools import product,permutations
from math import pi,sqrt,cos,isfinite
from importlib.metadata import version
import cmath
import torch
import flagquantum as fq
try:
    from examples.foundations.pauli_rotations import explicit
    from examples.foundations.circuit_composition import execute,product_input
    from examples.foundations.reversible_logic import basis_factors,complex_factors,probability_one
except ModuleNotFoundError:
    from pauli_rotations import explicit
    from circuit_composition import execute,product_input
    from reversible_logic import basis_factors,complex_factors,probability_one
D=torch.complex128
ATOL=1e-12
RUNS=0


def support(n,*qubits):
    if type(n) is not int or n<1 or any(type(q) is not int or q<0 or q>=n for q in qubits) or len(set(qubits))!=len(qubits):
        raise ValueError('Declared distinct register positions required')


def angle(theta):
    if type(theta) not in (int,float) or not isfinite(theta):raise ValueError('Finite literal radian angle required')


def controlled_rotation(axis,theta,c=0,t=1,n=2):
    support(n,c,t);angle(theta)
    if axis not in ('y','z'):raise ValueError('Choose declared Ry orRz identity')
    gate='r'+axis
    result=fq.Circuit(n,dtype=D)
    getattr(result,gate)(t,theta/2);result.cx(c,t)
    getattr(result,gate)(t,-theta/2);result.cx(c,t)
    return result


def controlled_phase(theta,c=0,t=1,n=2):
    return controlled_rotation('z',theta,c,t,n).p(c,theta/2)


def ccz(a=0,b=1,t=2,n=3,relative=False):
    support(n,a,b,t)
    c=fq.Circuit(n,dtype=D).cx(b,t).tdg(t).cx(a,t).t(t).cx(b,t).tdg(t).cx(a,t).t(b).t(t)
    if not relative:c.cx(a,b).t(a).tdg(b).cx(a,b)
    return c


def toffoli(a=0,b=1,t=2,n=3,relative=False):
    support(n,a,b,t)
    return fq.Circuit(n,dtype=D).h(t).compose(ccz(a,b,t,n,relative)).h(t)


def swap(n=2,a=0,b=1):
    support(n,a,b)
    return fq.Circuit(n,dtype=D).cx(a,b).cx(b,a).cx(a,b)


def cz(n=2,a=0,b=1):
    support(n,a,b)
    return fq.Circuit(n,dtype=D).h(b).cx(a,b).h(b)


def ancilla(mode='clean'):
    if mode not in ('clean','dirty'):raise ValueError('Declare clean ordirty ancilla contract')
    a,b,c,w,t=0,1,2,3,4
    C=toffoli(a,b,w,5);use=toffoli(w,c,t,5)
    out=fq.Circuit(5,dtype=D)
    if mode=='dirty':out.compose(use)
    return out.compose(C).compose(use).compose(C)


def run(c,factors):
    global RUNS
    v,p=execute(c,factors);RUNS+=1
    return v,p


def controlled_reference(v,U,n,c,t):
    # Independent scalar target contraction,not a simulator matrix gate.
    out=torch.zeros_like(v);mask=1<<(n-1-t)
    for j,z in enumerate(v):
        if not ((j>>(n-1-c))&1):out[j]+=z
        else:
            b=int(bool(j&mask))
            for e in (0,1):out[(j&~mask)|(e<<(n-1-t))]+=U[e,b]*z
    return out


def flip_reference(v,n,a,b,t,relative=False):
    out=torch.zeros_like(v)
    for j,z in enumerate(v):
        aa=(j>>(n-1-a))&1;bb=(j>>(n-1-b))&1
        phase=cmath.exp(.25j*pi*(-aa+(aa^bb))) if relative else 1
        out[j^(1<<(n-1-t)) if aa&bb else j]+=phase*z
    return out


def ancilla_reference(v,mode):
    if mode not in ('clean','dirty'):raise ValueError('Declared reference contract required')
    out=torch.zeros_like(v)
    for j,z in enumerate(v):
        a,b,c,w,t=((j>>s)&1 for s in (4,3,2,1,0))
        toggle=(a&b&c)^((w&c) if mode=='clean' else 0)
        out[j^toggle]+=z
    return out


def resources(c):
    names=[i.name for i in c.to_ir().instructions]
    assert all(name in ('h','t','tdg','cx') for name in names),set(names)
    return {name:names.count(name) for name in ('h','t','tdg','cx')}


def main():
    assert version('flagquantum')=='0.3.1' and version('torch').split('+')[0]=='2.13.0'
    inputs=lambda n:[basis_factors(bits) for bits in product((0,1),repeat=n)]+[complex_factors(n)]
    for axis in ('y','z'):
        for theta in (-.7,0.,pi/2,2*pi):
            compiled=controlled_rotation(axis,theta)
            native=fq.Circuit(2,dtype=D);getattr(native,'cr'+axis)(0,1,theta)
            for f in inputs(2):
                expected=controlled_reference(product_input(f),explicit(axis,theta),2,0,1)
                for block in (compiled,native):
                    v,p=run(block,f);torch.testing.assert_close(v,expected,rtol=0,atol=ATOL)
    assert RUNS==80
    for theta in (-.63,0.,pi/4,2*pi):
        P=torch.diag(torch.tensor([1,cmath.exp(1j*theta)],dtype=D))
        for f in inputs(2):
            v,p=run(controlled_phase(theta),f)
            torch.testing.assert_close(v,controlled_reference(product_input(f),P,2,0,1),rtol=0,atol=ATOL)
    print('80 controlled-rotation native/decomposed circuits and 20 phase-compensated circuits: all basis, complex and angle-boundary checks passed.')
    for name,compiled,native in [('CZ',cz(),fq.Circuit(2,dtype=D).cz(0,1)),('SWAP',swap(),fq.Circuit(2,dtype=D).swap(0,1))]:
        for f in inputs(2):
            initial=product_input(f);expected=initial.clone()
            if name=='CZ':expected[3]*=-1
            else:expected=initial[[0,2,1,3]]
            for block in (compiled,native):
                v,p=run(block,f);torch.testing.assert_close(v,expected,rtol=0,atol=ATOL)
    print('CZ and SWAP: 20 native/decomposed circuits agree on every basis input and complex product.')
    for a,b,t in permutations(range(3)):
        for f in inputs(3):
            expected=flip_reference(product_input(f),3,a,b,t)
            for block in (toffoli(a,b,t),fq.Circuit(3,dtype=D).ccx(a,b,t)):
                v,p=run(block,f);torch.testing.assert_close(v,expected,rtol=0,atol=ATOL)
    print('Exact Toffoli: 6 support permutations, all 8 basis and complex inputs, native/decomposed paths; 108 circuits.')
    for a,b,c in product((0,1),repeat=3):
        integer_phase=a+b+c-(a^b)-(a^c)-(b^c)+(a^b^c)
        assert integer_phase==4*a*b*c
    for f in inputs(3):
        v,p=run(toffoli(relative=True),f)
        torch.testing.assert_close(v,flip_reference(product_input(f),3,0,1,2,True),rtol=0,atol=ATOL)
        torch.testing.assert_close(p,flip_reference(product_input(f),3,0,1,2).abs().square(),rtol=0,atol=ATOL)
    print('Integer phase identity checked exactly on 8 Boolean triples; 9 phase-variant circuits match truth probabilities but retain extra branch phases.')
    for mode in ('clean','dirty'):
        for f in inputs(5):
            v,p=run(ancilla(mode),f)
            torch.testing.assert_close(v,ancilla_reference(product_input(f),mode),rtol=0,atol=ATOL)
    f=complex_factors(3)+[(1,0),complex_factors(1)[0]]
    v,p=run(ancilla('clean'),f)
    torch.testing.assert_close(v,ancilla_reference(product_input(f),'dirty'),rtol=0,atol=ATOL);assert probability_one(p,3)<ATOL
    print('Clean/dirty ancilla networks: all 32 basis + complex each, plus clean-contract complex input; 67 circuits, full complex references.')
    for relative,expected0 in ((False,1.),(True,(1+cos(pi/4))/2)):
        block=fq.Circuit(3,dtype=D).compose(toffoli(relative=relative)).h(1)
        v,p=run(block,[(1,0),(1/sqrt(2),1/sqrt(2)),(1,0)])
        assert abs(p[0].item()-expected0)<ATOL
    f=basis_factors((0,1,1,0,0))
    block=fq.Circuit(5,dtype=D).h(0).cx(0,3).compose(ancilla('dirty'))
    v,p=run(block,f);expected=torch.zeros(32,dtype=D);expected[12]=expected[31]=1/sqrt(2)
    torch.testing.assert_close(v,expected,rtol=0,atol=ATOL)
    assert resources(toffoli())=={'h':2,'t':4,'tdg':3,'cx':6}
    assert resources(ancilla('clean'))=={'h':6,'t':12,'tdg':9,'cx':18}
    assert resources(ancilla('dirty'))=={'h':8,'t':16,'tdg':12,'cx':24}
    invalid=[lambda:controlled_rotation('x',.3),lambda:controlled_rotation('z',float('nan')),lambda:controlled_rotation('y',True),lambda:controlled_rotation('y',.3,0,0),lambda:toffoli(0,0,2),lambda:toffoli(0,1,3),lambda:ancilla('reset')]
    for f in invalid:
        try:f()
        except ValueError:pass
        else:raise AssertionError('Malformed decomposition/ancilla contract admitted')
    assert RUNS==307,RUNS
    print('2 phase-sensitive analyzer circuits and 1 entangled borrowed-ancilla circuit passed; 7 malformed contracts rejected.')
    print('307 actual CPU complex128 circuits; atol 1e-12, rtol 0; exact Toffoli uses 6 CX, 4 T, 3 T-dagger, 2 H.')
    print('Clean three-control construction: 18 CX; borrowed-dirty echo: 24 CX; no optimality, routing, reset, noise or hardware claim.')


if __name__=='__main__':main()
