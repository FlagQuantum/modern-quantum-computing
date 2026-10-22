import sys
sys.path.insert(0,'/Users/baai/Documents/liuwei/modern-quantum-computing')
from examples.foundations import confidence_shots as c
from fractions import Fraction as F
from math import sin,cos
import torch,flagquantum as fq
c.RUNS=0
for selected in ((3,0),(0,3),(1,3,0),(3,2,0,1)):
 for seed in (47,131):
  circuit=fq.Circuit(4,dtype=c.D).h(0).ry(1,-.63).p(1,.91).ry(2,1.29).h(3).cx(0,2).cx(3,1)
  scores=tuple(F((j%5)-2,2) for j in range(2**len(selected)))
  var=c.range_variance(min(scores),max(scores));eps,delta=F(1,4),F(1,5)
  N=c.budget(var,eps,delta)
  p,bits,counts,freq=c.native(circuit,selected,N,seed)
  ids,_,_=c.s.histogram(bits)
  mean=sum(score*F(count.item(),N) for score,count in zip(scores,counts))
  assert mean==sum((scores[j] for j in ids.tolist()),start=F(0))/N
  assert var/N/eps**2<=delta
  assert all(min(scores)<=s<=max(scores) for s in scores)
for theta in (.19,-.63,1.74,-2.31):
 for seed in (13,71):
  N=c.budget(F(1),F(1,3),F(1,4))
  p,bits,_,_=c.native(fq.Circuit(1,dtype=c.D).ry(0,theta).p(0,.47).h(0),(0,),N,seed)
  assert N==36 and abs(p[0].item()-p[1].item()-sin(theta)*cos(.47))<1e-12
N=c.budget(F(1,4),F(1,5),F(1,4))
assert N==25 and c.coverage(F(2,7),N,F(1,5))>=F(3,4)
for var,eps,delta in [(F(5,9),F(3,11),F(7,31)),(F(0),F(1,17),F(1,101))]:
 N=c.budget(var,eps,delta)
 assert var/N/eps**2<=delta
 if N>1:assert var/(N-1)/eps**2>delta
assert c.RUNS==16
print('16 fresh native circuits:8 complex four-qubit ordered bounded-score records;8 new X-readout preparations with fixed36-shot budgets passed.')
print('Fresh exact p2/7 binomial coverage, rational ceiling cases and zero-variance design passed; no single-interval coverage assertion.')
