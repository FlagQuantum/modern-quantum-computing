import sys
sys.path.insert(0,'/Users/baai/Documents/liuwei/modern-quantum-computing')
from examples.foundations import variance_estimators as v
from fractions import Fraction as F
import flagquantum as fq,torch
v.RUNS=0
for theta,phi in [(-.37,.83),(1.73,-.92),(.0007,2.31)]:
 for a,b in [(.23,-1.7),(-.61,.41)]:v.quantum(theta,phi,a,b)
for selected in ((3,0),(0,3),(1,3,0),(3,2,0,1)):
 for seed in (53,139):
  c=fq.Circuit(4,dtype=v.D).h(0).ry(1,.67).p(1,-.31).ry(2,-1.23).h(3).cx(0,2).cx(3,1)
  p,bits,_,_=v.native(c,selected,29,seed)
  K=len(p);scores=torch.tensor([[float((j%3)-1),float(j.bit_count()%2)] for j in range(K)],dtype=torch.float64)
  mean,C=v.moments(p,scores);a=torch.tensor([.43,-1.17],dtype=torch.float64)
  direct=sum(p[j].item()*((scores[j]@a).item()-(mean@a).item())**2 for j in range(K))
  assert abs(v.weighted(C,a)-direct)<1e-12
  ids,_,_=v.s.histogram(bits);observed=scores[ids]
  assert abs(v.weighted(v.sample_covariance(observed),a)-v.sample_covariance((observed@a)[:,None]).item())<1e-12
for setting,N,seed in [('X',11,23),('Z',19,67)]:
 c=fq.Circuit(1,dtype=v.D).ry(0,-.91).p(0,.62)
 if setting=='X':c.h(0)
 p,_,_,_=v.native(c,(0,),N,seed)
 _,C=v.moments(p,torch.tensor([[1.],[-1.]],dtype=torch.float64))
 assert C.item()>=0
rows=v.s.ensemble((F(1,10),F(2,10),F(3,10),F(4,10)),3)
scores=(2,-1,0,3);mu=F(6,5);var_mean=F(0);expected_sample=F(0)
for seq,w,f in rows:
 values=[F(scores[j]) for j in seq];mean=sum(values)/3
 var_mean+=w*(mean-mu)**2
 expected_sample+=w*sum((x-mean)**2 for x in values)/2
assert var_mean==F(23,25) and expected_sample==F(69,25)
assert v.RUNS==16
print('16 fresh native circuits: 6 new spectral/centered quantum variances; 8 complex four-qubit ordered score/covariance checks; 2 new separate-basis readouts passed.')
print('New four-category exact ensemble: variance of mean23/25, expected sample variance69/25 over64 records; zero quantum calls.')
