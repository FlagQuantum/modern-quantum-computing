"""Section5.4: phase-tracked compute/copy/uncompute and reusable workspace."""
from itertools import product
from math import sqrt,isfinite
from importlib.metadata import version
import torch
import flagquantum as fq
try:
    from examples.foundations.circuit_composition import execute,product_input
    from examples.foundations.reversible_logic import basis_factors,complex_factors,probability_one
except ModuleNotFoundError:
    from circuit_composition import execute,product_input
    from reversible_logic import basis_factors,complex_factors,probability_one
D=torch.complex128
ATOL=1e-12
RUNS=0


def compute_ops(phi=.43,eta=-.71,delta=.37):
    if any(type(a) not in (int,float) or not isfinite(a) for a in (phi,eta,delta)):
        raise ValueError('Finite literal radian angles required')
    return [('cx',0,2),('h',1),('rz',1,phi),('cx',0,1),('rz',2,eta),('rz',0,delta)]


def inverse(ops):
    return [(g[0],g[1],-g[2]) if g[0]=='rz' else g for g in reversed(ops)]


def circuit(ops,n=4):
    c=fq.Circuit(n,dtype=D)
    for g in ops:
        getattr(c,g[0])(*g[1:])
    return c


def compute(phi=.43,eta=-.71,delta=.37):
    return circuit(compute_ops(phi,eta,delta))


def block(stage='clean',phi=.43,eta=-.71,delta=.37):
    if stage not in ('compute','use','clean','bad-data','phase'):
        raise ValueError('Declared coherent stage required')
    C=compute(phi,eta,delta)
    c=fq.Circuit(4,dtype=D).compose(C)
    if stage=='phase':c.z(2)
    elif stage!='compute':c.cx(2,3)
    if stage=='bad-data':c.x(0)
    if stage in ('clean','bad-data','phase'):c.compose(C.adjoint())
    return c


def ops_for(stage='clean',phi=.43,eta=-.71,delta=.37):
    C=compute_ops(phi,eta,delta)
    if stage=='compute':return C
    if stage=='phase':return C+[('z',2)]+inverse(C)
    if stage=='use':return C+[('cx',2,3)]
    if stage=='clean':return C+[('cx',2,3)]+inverse(C)
    if stage=='bad-data':return C+[('cx',2,3),('x',0)]+inverse(C)
    raise ValueError('Declared reference stage required')


def reference(v,ops,n=4):
    # Independent scalar bit updates; no circuit IR or simulator output used.
    import cmath
    if v.shape!=(2**n,) or v.dtype!=D or v.device.type!='cpu' or not torch.isfinite(v).all():
        raise ValueError('Finite CPUcomplex128 vector matching register width required')
    a=v.tolist()
    for g in ops:
        out=[0j]*len(a);name,q=g[:2];mask=1<<(n-1-q)
        for j,z in enumerate(a):
            b=int(bool(j&mask))
            if name=='cx':
                target=1<<(n-1-g[2]);out[j^target if b else j]+=z
            elif name=='x':out[j^mask]+=z
            elif name=='z':out[j]+=(-1 if b else 1)*z
            elif name=='rz':out[j]+=cmath.exp((.5j if b else -.5j)*g[2])*z
            elif name=='h':
                out[j&~mask]+=z/sqrt(2);out[j|mask]+=(-1 if b else 1)*z/sqrt(2)
            else:raise ValueError('Unsupported reference gate')
        a=out
    return torch.tensor(a,dtype=D)


def run(c,factors):
    global RUNS
    v,p=execute(c,factors);RUNS+=1
    return v,p


def leakage(p,n=4):
    # Joint event (W,F)!=(0,0), not a product of separate marginal probabilities.
    return sum(p[j].item() for j in range(len(p)) if j&(1<<(n-2)|1<<(n-3)))


def clean_reference(factors,n=4):
    initial=product_input(factors)
    return reference(initial,[('cx',0,3)],n)


def reuse():
    C=compute()
    c=fq.Circuit(5,dtype=D).compose(C,qubits=(0,1,2,3)).cx(2,3).compose(C.adjoint(),qubits=(0,1,2,3)).h(0)
    return c.compose(C,qubits=(0,1,2,3)).cx(2,4).compose(C.adjoint(),qubits=(0,1,2,3))


def main():
    assert version('flagquantum')=='0.3.1' and version('torch').split('+')[0]=='2.13.0'
    inputs=[basis_factors(bits) for bits in product((0,1),repeat=4)]+[complex_factors(4)]
    for stage in ('compute','use','clean'):
        for factors in inputs:
            v,p=run(block(stage),factors)
            torch.testing.assert_close(v,reference(product_input(factors),ops_for(stage)),rtol=0,atol=ATOL)
    assert RUNS==51
    valid=[basis_factors((x,0,0,y)) for x,y in product((0,1),repeat=2)]+[[complex_factors(1)[0],(1,0),(1,0),complex_factors(2)[1]]]
    for factors in valid:
        for stage in ('use','clean'):
            v,p=run(block(stage),factors)
            torch.testing.assert_close(v,reference(product_input(factors),ops_for(stage)),rtol=0,atol=ATOL)
            if stage=='clean':
                torch.testing.assert_close(v,clean_reference(factors),rtol=0,atol=ATOL);assert leakage(p)<ATOL
    for angles in ((0.,0.,0.),(6.283185307179586,-1.17,.83)):
        for factors in valid:
            v,p=run(block('clean',*angles),factors)
            torch.testing.assert_close(v,clean_reference(factors),rtol=0,atol=ATOL);assert leakage(p)<ATOL
    assert RUNS==71
    print('Compute/use/clean:51full-register basis/complex runs;20valid-workspace and angle-boundary runs passed.')
    C=compute_ops();reuse_ops=C+[('cx',2,3)]+inverse(C)+[('h',0)]+C+[('cx',2,4)]+inverse(C)
    for factors in [basis_factors(bits) for bits in product((0,1),repeat=5)]+[complex_factors(5)]:
        v,p=run(reuse(),factors)
        torch.testing.assert_close(v,reference(product_input(factors),reuse_ops,5),rtol=0,atol=ATOL)
    factors=[(.6,.8j),(1,0),(1,0),(1,0),(1,0)]
    v,p=run(reuse(),factors);expected=torch.zeros(32,dtype=D)
    for d,alpha in enumerate((.6,.8j)):
        for e in (0,1):expected[17*e+2*d]=alpha*(-1 if d==e==1 else 1)/sqrt(2)
    torch.testing.assert_close(v,expected,rtol=0,atol=ATOL);assert leakage(p,5)<ATOL
    print('Reuse:33full-register tests plus1zero-workspace complex analytic check;retained first output and second computation coherent.')
    for factors in inputs:
        v,p=run(block('phase'),factors)
        torch.testing.assert_close(v,reference(product_input(factors),ops_for('phase')),rtol=0,atol=ATOL)
    factors=valid[-1];v,p=run(block('phase'),factors)
    torch.testing.assert_close(v,reference(product_input(factors),[('z',0)]),rtol=0,atol=ATOL);assert leakage(p)<ATOL
    print('Phase use:18circuits;C-dagger Z(F) C equals Z(data) on clean-input subspace,with workspace restored.')
    factors=basis_factors((0,1,0,0));v,p=run(block(),factors);assert abs(leakage(p)-1)<ATOL
    factors=basis_factors((0,0,0,0));v,p=run(block('bad-data'),factors)
    torch.testing.assert_close(v,reference(product_input(factors),ops_for('bad-data')),rtol=0,atol=ATOL);assert probability_one(p,2)>1-ATOL
    C=compute();used=fq.Circuit(4,dtype=D).compose(C).cx(2,3)
    factors=[(.6,.8j),(1,0),(1,0),(1,0)]
    v,p=run(fq.Circuit(4,dtype=D).compose(used).compose(used.adjoint()),factors)
    torch.testing.assert_close(v,product_input(factors),rtol=0,atol=ATOL)
    c=fq.Circuit(2,dtype=D).h(0).cx(0,1).h(0)
    v,p=run(c,basis_factors((0,0)))
    torch.testing.assert_close(v,torch.tensor([.5,.5,.5,-.5],dtype=D),rtol=0,atol=ATOL)
    assert abs(probability_one(p,0)-.5)<ATOL
    print('4boundary circuits:wrong blank,changed data,whole-used inverse andnonorthogonal-copy failure checked.')
    invalid=[lambda:compute(float('nan')),lambda:compute(True),lambda:block('reset'),
             lambda:reference(torch.zeros(8,dtype=D),[]),lambda:reference(torch.zeros(16),[]),
             lambda:reference(torch.full((16,),float('inf'),dtype=D),[]),
             lambda:reference(torch.zeros(16,dtype=D),[('reset',0)])]
    for action in invalid:
        try:action()
        except ValueError:pass
        else:raise AssertionError('Invalid workspace/reference contract admitted')
    assert RUNS==127,RUNS
    print('127actual CPUcomplex128 circuits;7invalid contracts rejected;atol1e-12,rtol0,no phase alignment.')
    print('Clean subspace and numerical leakage distinguished;no reset,noise,hardware or resource-optimality claim.')


if __name__=='__main__':main()
