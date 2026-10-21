"""New author cases for 6.3; no precomputed expected answer supplied to a separate agent."""
from itertools import product
import torch
import flagquantum as fq
from examples.foundations import observables as o
b=o.b;start=o.RUNS
A=.41*torch.kron(o.Y,o.X)-.23*torch.kron(o.X,o.Z)+.17*torch.kron(o.I,o.Z)
native=.41*(fq.Y(0)@fq.X(1))-.23*(fq.X(0)@fq.Z(1))+.17*fq.Z(1)
for theta in (-.82,.19,1.27):
 fs=b.complex_factors(2);program=(('ry',(0,),(theta,)),('cx',(0,1),()),('p',(1,),(-.39,)))
 v,p,m=o.query(fq.Circuit(2,dtype=b.D).ry(0,theta).cx(0,1).p(1,-.39),fs,{'a':native})
 torch.testing.assert_close(v,o.matrix(2,program)@b.product_input(fs),rtol=0,atol=b.ATOL)
 spectral,_=o.spectral_mean(v,*o.numerical_spectrum(A))
 torch.testing.assert_close(m['a'],spectral,rtol=0,atol=b.ATOL)
 scalar=sum(v[j].conj().item()*A[j,k].item()*v[k].item() for j in range(4) for k in range(4))
 assert abs(m['a'].item()-scalar)<b.ATOL
print('3 fresh two-qubit coefficient/preparation transfers passed against explicit scalar quadratic sums and spectral probabilities.')
def tensor(*factors):
 result=torch.ones((1,1),dtype=b.D)
 for x in factors:result=torch.kron(result,x)
 return result
A4=.31*tensor(o.X,o.I,o.I,o.Y)-.27*tensor(o.I,o.I,o.Z,o.I)+.12*tensor(o.I,o.X,o.I,o.I)
native4=.31*(fq.Y(3)@fq.X(0))-.27*fq.Z(2)+.12*fq.X(1)
spec=o.numerical_spectrum(A4)
program=(('ry',(2,),(.33,)),('cx',(3,0),()),('p',(0,),(-.46,)))
for fs in [b.basis_factors(bits) for bits in product((0,1),repeat=4)]+[b.complex_factors(4)]:
 v,p,m=o.query(fq.Circuit(4,dtype=b.D).ry(2,.33).cx(3,0).p(0,-.46),fs,{'a':native4})
 torch.testing.assert_close(v,o.matrix(4,program)@b.product_input(fs),rtol=0,atol=b.ATOL)
 spectral,_=o.spectral_mean(v,*spec)
 torch.testing.assert_close(m['a'],spectral,rtol=0,atol=b.ATOL)
 scalar=sum(v[j].conj().item()*A4[j,k].item()*v[k].item() for j in range(16) for k in range(16))
 assert abs(m['a'].item()-scalar)<b.ATOL
assert o.RUNS-start==20,o.RUNS-start
print('17 four-qubit reversed-support transfers passed: independent prepared vectors, scalar quadratic sums and spectral means.')
print('20 actual CPU complex128 circuits; author transfer, not independent review, reader trial or physical measurement execution.')
