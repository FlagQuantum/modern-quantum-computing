"""New-angle RY-between-calls transfer, independently expanded on basis labels."""
import sys
from math import cos,sin
from itertools import product
sys.path.insert(0,'.')
import torch
import flagquantum as fq
from examples.foundations import reusable_workspace as rw
D=rw.D
C=rw.compute(-.29,.61,-1.03)
first=fq.Circuit(5,dtype=D).compose(C,qubits=(0,1,2,3)).cx(2,3).compose(C.adjoint(),qubits=(0,1,2,3))
block=fq.Circuit(5,dtype=D).compose(first).ry(0,.31).compose(C,qubits=(0,1,2,3)).cx(2,4).compose(C.adjoint(),qubits=(0,1,2,3))
inputs=[rw.basis_factors((d,0,0,y,z)) for d,y,z in product((0,1),repeat=3)]
inputs.append([(.6,.8j),(1,0),(1,0),rw.complex_factors(2)[1],rw.complex_factors(1)[0]])
for factors in inputs:
    v,p=rw.run(block,factors);expected=torch.zeros(32,dtype=D)
    for d,y,z,e in product((0,1),repeat=4):
        rotation=cos(.31/2) if d==e else (sin(.31/2) if e==1 else -sin(.31/2))
        expected[16*e+2*(y^d)+(z^e)]+=factors[0][d]*factors[3][y]*factors[4][z]*rotation
    torch.testing.assert_close(v,expected,rtol=0,atol=rw.ATOL)
    assert rw.leakage(p,5)<rw.ATOL
factors=inputs[-1][:4]
v,p=rw.run(fq.Circuit(4,dtype=D).compose(C).z(2).compose(C.adjoint()),factors)
expected=rw.product_input(factors);expected[8:]*=-1
torch.testing.assert_close(v,expected,rtol=0,atol=rw.ATOL)
assert rw.leakage(p)<rw.ATOL and rw.RUNS==10
print('New angles(-.29,.61,-1.03),RY(.31) and arbitrary retained inputs:9reuse plus1phase circuits passed independent analytic references.')
