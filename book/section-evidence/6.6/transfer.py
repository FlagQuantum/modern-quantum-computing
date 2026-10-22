import sys
sys.path.insert(0,'/Users/baai/Documents/liuwei/modern-quantum-computing')
from examples.foundations import exact_samples as s
import torch,flagquantum as fq
from fractions import Fraction as F
s.RUNS=0
for angle in (.19,-1.17,2.83,-3.62,.00003):
 for seed in (31,97):
  p,b,c,f=s.native(fq.Circuit(1,dtype=s.D).ry(0,angle).p(0,.73),(0,),19,seed)
  from math import cos,sin
  torch.testing.assert_close(p,torch.tensor([cos(angle/2)**2,sin(angle/2)**2],dtype=torch.float64),atol=1e-12,rtol=0)
for selected in ((3,0),(1,3,0),(2,0,3,1)):
 for seed in (43,113):
  circuit=fq.Circuit(4,dtype=s.D).ry(0,-.47).h(1).ry(2,1.13).p(2,.9).h(3).cx(3,0).cx(0,2)
  p,b,c,f=s.native(circuit,selected,29,seed)
  ids,_,_=s.histogram(b)
  assert c.tolist()==[ids.tolist().count(j) for j in range(len(p))]
  assert c.sum()==29
rows=s.ensemble((F(1,10),F(2,10),F(3,10),F(4,10)),3)
assert sum(w*sum(v*x for v,x in zip((2,-1,0,3),f)) for _,w,f in rows)==F(6,5)
assert s.RUNS==16
print('16 fresh native circuits: 10 new phase-bearing Bernoulli cases; 6 complex correlated four-qubit ordered nonadjacent readouts passed.')
print('Fresh exact four-category score ensemble: mean 6/5 over 64 records; zero quantum calls.')
