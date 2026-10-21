"""New 6.2 author transfer: 17 four-qubit and 3 complex-subspace preparations."""
from itertools import product
import cmath,math
import torch
import flagquantum as fq
from examples.foundations import conditional_states as c
b=c.b;start=b.RUNS
program=(('ry',(0,),(-.29,)),('cx',(0,3),()),('p',(1,),(.47,)))
P,names=b.marginal_family(4,(3,1));Q,qn=b.marginal_family(4,(1,3))
for fs in [b.basis_factors(bits) for bits in product((0,1),repeat=4)]+[b.complex_factors(4)]:
 v,native=b.run(fq.Circuit(4,dtype=b.D).ry(0,-.29).cx(0,3).p(1,.47),fs,(3,1))
 torch.testing.assert_close(v,c.matrix(4,program)@b.product_input(fs),rtol=0,atol=b.ATOL)
 p,ws=c.branches(v,P,names);table=c.joint(v,P,names,Q,qn)
 torch.testing.assert_close(p,native,rtol=0,atol=b.ATOL)
 expected=torch.zeros_like(table)
 for a,w in enumerate(ws):
  expected[a,qn.index(names[a][::-1])]=p[a]
  indices=[j for j in range(16) if format(j,'04b')[3]+format(j,'04b')[1]==names[a]]
  prob=sum(abs(v[j].item())**2 for j in indices)
  assert abs(p[a].item()-prob)<b.ATOL
  if w is not None:
   ref=torch.tensor([v[j].item()/math.sqrt(prob) if j in indices else 0 for j in range(16)],dtype=b.D)
   torch.testing.assert_close(w,ref,rtol=0,atol=b.ATOL)
 torch.testing.assert_close(table,expected,rtol=0,atol=b.ATOL)
print('17 four-qubit transfers passed: full prepared vectors, ordered scalar masks and reversed-label joint tables.')
F=torch.tensor([[cmath.exp(2j*math.pi*j*k/4)/2 for k in range(4)] for j in range(4)],dtype=b.D)
P=tuple(sum((torch.outer(F[:,k],F[:,k].conj()) for k in group),torch.zeros((4,4),dtype=b.D)) for group in ((0,1),(2,3)))
names=('01-columns','23-columns');Z,zn=b.basis_family(2)
for angle in (-.71,.24,1.19):
 program=(('rx',(0,),(angle,)),('h',(1,),()),('p',(1,),(-.38,)),('cx',(1,0),()))
 v,_=b.run(fq.Circuit(2,dtype=b.D).rx(0,angle).h(1).p(1,-.38).cx(1,0),b.complex_factors(2))
 torch.testing.assert_close(v,c.matrix(2,program)@b.product_input(b.complex_factors(2)),rtol=0,atol=b.ATOL)
 p,ws=c.branches(v,P,names)
 projected=[]
 for a,group in enumerate(((0,1),(2,3))):
  w=sum((F[:,k]*torch.vdot(F[:,k],v) for k in group),torch.zeros(4,dtype=b.D))
  prob=sum(abs(torch.vdot(F[:,k],v).item())**2 for k in group)
  assert abs(p[a].item()-prob)<b.ATOL
  torch.testing.assert_close(ws[a],w/math.sqrt(prob),rtol=0,atol=b.ATOL)
  projected.append(w)
 torch.testing.assert_close(c.joint(v,P,names,P,names),torch.diag(p),rtol=0,atol=b.ATOL)
 scalar=torch.tensor([sum(abs(w[j].item())**2 for w in projected) for j in range(4)],dtype=torch.float64)
 torch.testing.assert_close(c.joint(v,P,names,Z,zn).sum(0),scalar,rtol=0,atol=b.ATOL)
assert b.RUNS-start==20
print('3 complex Fourier-subspace transfers passed: overlap-based branches, repeatability and ignored-record computational marginals.')
print('20 actual CPU complex128 preparation circuits; classical branch enumeration; author transfer, not independent review or reader trial.')
