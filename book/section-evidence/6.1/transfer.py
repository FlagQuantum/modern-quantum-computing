"""Author transfer: four-qubit marginal and a new complex rank-two projector family."""
from pathlib import Path
import sys,math,cmath
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from itertools import product
import torch
import examples.foundations.projective_born as b
import examples.foundations.circuit_rewrites as w
program=(('ry',(0,),(-.37,)),('cx',(0,3),()))
U=w.matrix(4,program)
selected=(3,1)
for factors in [b.basis_factors(bits) for bits in product((0,1),repeat=4)]+[b.complex_factors(4)]:
    v,p=b.run(w.compile_program(4,program),factors,selected)
    expected=U @ b.product_input(factors)
    torch.testing.assert_close(v,expected,rtol=0,atol=b.ATOL)
    marginal=torch.zeros(4,dtype=torch.float64)
    for j,z in enumerate(expected):
        key=int(''.join(format(j,'04b')[q] for q in selected),2)
        marginal[key]+=abs(z)**2
    torch.testing.assert_close(p,marginal,rtol=0,atol=b.ATOL)
B=torch.tensor([[cmath.exp(2j*math.pi*j*k/4)/2 for k in range(4)] for j in range(4)],dtype=b.D)
torch.testing.assert_close(B.mH@B,torch.eye(4,dtype=b.D),rtol=0,atol=b.ATOL)
projectors=tuple(B[:,start:start+2] @ B[:,start:start+2].mH for start in (0,2))
program=(('rx',(0,),(.29,)),('h',(1,),()),('p',(1,),(-.62,)),('cx',(1,0),()))
for factors in [b.basis_factors((0,0)),b.basis_factors((1,1)),b.complex_factors(2)]:
    v,_=b.run(w.compile_program(2,program),factors)
    torch.testing.assert_close(v,w.matrix(2,program) @ b.product_input(factors),rtol=0,atol=b.ATOL)
    p=b.born(v,projectors,('first pair','second pair'))
    overlaps=B.mH @ v
    reference=torch.stack([overlaps[:2].abs().square().sum(),overlaps[2:].abs().square().sum()])
    torch.testing.assert_close(p,reference,rtol=0,atol=b.ATOL)
assert b.RUNS==20
print('20 new transfer circuits passed: 17 four-qubit ordered marginals and 3 complex Fourier-projector predictions; no general-projector hardware execution claimed.')
