"""14.5: exact design contracts and actual native finite repetition examples."""
import itertools,math,cmath
from fractions import Fraction as F
from dataclasses import replace
import torch,flagquantum as fq
try:
 from examples.foundations import statistical_ensembles as e,uniform_reversible as u
except ModuleNotFoundError:
 import statistical_ensembles as e,uniform_reversible as u
D=e.D;RUNS=0

def rational(x):
 if type(x)is not F:raise ValueError('Exact Fraction design input required')
 return x
def prob(x):
 rational(x)
 if not 0<=x<=1:raise ValueError('Probability in[0,1] required')
 return x
def failure(delta):
 rational(delta)
 if not 0<delta<1:raise ValueError('Failure target strictly between0and1 required')
def halfgap(h):
 rational(h)
 if not 0<h<=F(1,2):raise ValueError('Positive certified success half-gap at most1/2 required')
def odd_up(x):
 n=max(1,math.ceil(x));return n if n%2 else n+1
def mean_budget(epsilon,delta,bias=F(0)):
 rational(epsilon);failure(delta);rational(bias)
 if not 0<=bias<epsilon:raise ValueError('Nonnegative bias strictly below accuracy required')
 return max(1,math.ceil(F(1,4)/(delta*(epsilon-bias)**2)))
def effective_gap(gamma,bias):
 halfgap(gamma);rational(bias)
 if not 0<=bias<gamma:raise ValueError('Bias must leave a strictly positive success gap')
 return gamma-bias
def variance_budget(h,delta):
 halfgap(h);failure(delta);return odd_up(F(1,4)/(delta*h*h))
def moment_budget(h,delta):
 halfgap(h);failure(delta);base=1-4*h*h
 for m in range(1,502,2):
  if base**m<=delta**2:return m
 raise ValueError('Exact host moment-budget teaching guard:odd M<=501')
def binomial(p,n):
 prob(p)
 if type(n)is not int or not 1<=n<=501:raise ValueError('Exact binomial teaching count1..501 required')
 rows=tuple((j,F(math.comb(n,j))*p**j*(1-p)**(n-j))for j in range(n+1));assert sum(w for _,w in rows)==1
 return rows
def majority_error(success,m):
 if type(m)is not int or m%2!=1:raise ValueError('Odd majority count required')
 return sum((w for j,w in binomial(success,m)if j<=m//2),F(0))
def minimal_fixed_majority(success,delta):
 prob(success);failure(delta)
 if success<=F(1,2):raise ValueError('Fixed source must have success above1/2')
 for m in range(1,502,2):
  if majority_error(success,m)<=delta:return m
 raise ValueError('Exact search guard exceeded')
def target_coverage(target,actual,n,epsilon):
 prob(target);rational(epsilon)
 if epsilon<=0:raise ValueError('Positive accuracy required')
 return sum((w for j,w in binomial(actual,n)if abs(F(j,n)-target)<=epsilon),F(0))
def grid_bits(length,bias):
 if type(length)is not int or not 1<=length<=10000:raise ValueError('Positive bounded gate count required')
 rational(bias)
 if not 0<bias<=1:raise ValueError('Positive bias budget required')
 b=0
 while F(length,2**(b+1))>bias:b+=1
 return b
def verified_budget(success,delta):
 prob(success);failure(delta)
 if success==0:raise ValueError('Zero success has no finite verified-success budget')
 for n in range(1,10001):
  if (1-success)**n<=delta:return n
 raise ValueError('Verified-success teaching guard exceeded')

def native_mean(p,n,mode='statevector',seed=61):
 global RUNS
 prob(p)
 if type(n)is not int or not 1<=n<=10000 or mode not in ('statevector','density_matrix'):raise ValueError('Tested mode and fixed native shot count1..10000 required')
 theta=2*math.asin(math.sqrt(float(p)));c=fq.Circuit(1,dtype=D).RY(0,theta=theta)
 r=fq.run(c,outputs=[fq.probabilities(name='p'),fq.samples(qubits=(0,),name='raw')],shots=n,options=replace(e.OPTIONS,mode=mode,seed=seed));RUNS+=1
 e.close(r.measurement('p').value[0],torch.tensor([float(1-p),float(p)],dtype=torch.float64))
 raw=r.measurement('raw').value;assert raw.shape==(1,n,1)and bool(((raw==0)|(raw==1)).all())
 count=int(raw.sum());assert 0<=count<=n
 return r,F(count,n)

def native_vote(p,independent=True,mode='statevector'):
 global RUNS
 prob(p)
 if type(independent)is not bool or mode not in ('statevector','density_matrix'):raise ValueError('Literal independence flag and tested mode required')
 theta=2*math.asin(math.sqrt(float(p)));c=fq.Circuit(4,dtype=D).RY(0,theta=theta)
 if independent:c.RY(1,theta=theta).RY(2,theta=theta)
 else:c.CX(0,1).CX(0,2)
 c.CCX(0,1,3).CCX(0,2,3).CCX(1,2,3)
 target=torch.zeros(16,dtype=D)
 for bits in itertools.product((0,1),repeat=3):
  s=sum(bits);amp=(math.sqrt(float(p))**s*math.sqrt(float(1-p))**(3-s))if independent else math.sqrt(float(p if s==3 else 1-p))if s in (0,3)else 0
  target[u.index(bits+(int(s>=2),))]=amp
 r=fq.run(c,outputs=[fq.density_matrix(name='rho'),fq.probabilities(qubits=(3,),name='vote'),fq.samples(qubits=(0,1,2,3),name='raw')],shots=17,options=replace(e.OPTIONS,mode=mode,seed=61));RUNS+=1
 e.close(r.measurement('rho').value[0],torch.outer(target,target.conj()))
 if mode=='statevector':e.close(r.statevector()[0],target)
 correct=1-majority_error(p,3)if independent else p
 e.close(r.measurement('vote').value[0],torch.tensor([float(1-correct),float(correct)],dtype=torch.float64))
 raw=r.measurement('raw').value;assert raw.shape==(1,17,4)and bool(((raw==0)|(raw==1)).all())
 assert bool((raw[0,:,3]==(raw[0,:,:3].sum(dim=1)>=2)).all())
 return r,1-correct

def phase_chain(angles,offsets,mode='statevector'):
 global RUNS
 if type(angles)is not tuple or type(offsets)is not tuple or not 1<=len(angles)==len(offsets)<=8 or any(type(x)not in (int,float)or not math.isfinite(x)for x in angles+offsets)or mode not in ('statevector','density_matrix'):raise ValueError('Finite real radian tuples of equal length1..8and tested mode required')
 c=fq.Circuit(1,dtype=D).H(0)
 for theta,eta in zip(angles,offsets):c.RZ(0,theta=theta+eta)
 c.H(0)
 phi=sum(angles);actual=phi+sum(offsets);target=torch.tensor([math.cos(actual/2),-1j*math.sin(actual/2)],dtype=D)
 r=fq.run(c,outputs=[fq.density_matrix(name='rho'),fq.probabilities(name='p')],options=replace(e.OPTIONS,mode=mode));RUNS+=1
 e.close(r.measurement('rho').value[0],torch.outer(target,target.conj()))
 if mode=='statevector':e.close(r.statevector()[0],target)
 e.close(r.measurement('p').value[0],target.abs().square())
 ideal=math.sin(phi/2)**2;observed=math.sin(actual/2)**2
 local=sum(2*abs(math.sin(eta/4))for eta in offsets);whole=2*abs(math.sin(sum(offsets)/4))
 assert whole<=local+1e-12 and abs(observed-ideal)<=2*local+1e-12
 return r,dict(ideal=ideal,actual=observed,observed_bias=abs(observed-ideal),operator_sum=local,event_bound=2*local)

def median_blocks(p,n0,m,mode='statevector'):
 if type(n0)is not int or n0<1 or type(m)is not int or m<1 or m%2!=1:raise ValueError('Positive fixed block size and odd block count required')
 r,_=native_mean(p,n0*m,mode)
 raw=r.measurement('raw').value[0,:,0].reshape(m,n0)
 means=[F(int(row.sum()),n0)for row in raw];median=sorted(means)[m//2]
 assert 0<=median<=1 and sum(int(row.sum())for row in raw)==int(raw.sum())
 return r,median

def invalid_checks():
 calls=[lambda:mean_budget(F(0),F(1,10)),lambda:mean_budget(F(1,8),F(1,10),F(1,8)),lambda:mean_budget(.1,F(1,10)),
  lambda:mean_budget(F(1,8),F(0)),lambda:variance_budget(F(0),F(1,10)),lambda:effective_gap(F(1,4),F(1,4)),
  lambda:moment_budget(F(1,4),F(1)),lambda:majority_error(F(3,4),2),lambda:native_mean(F(3,4),True),
  lambda:native_mean(F(3,4),10001),lambda:native_vote(F(3,4),1),lambda:phase_chain((0.,),(math.nan,)),
  lambda:median_blocks(F(3,4),4,2),lambda:grid_bits(0,F(1,10)),lambda:verified_budget(F(0),F(1,10)),
  lambda:minimal_fixed_majority(F(1,2),F(1,10))]
 before=RUNS
 for call in calls:
  try:call()
  except ValueError:pass
  else:raise AssertionError('Malformed repetition contract accepted')
 assert RUNS==before;return len(calls)

def main():
 probabilities=(F(0),F(1,4),F(1,2),F(5,8),F(3,4),F(1))
 for mode in ('statevector','density_matrix'):
  for p in probabilities:
   for n in (17,53,250):native_mean(p,n,mode)
   for independent in (False,True):native_vote(p,independent,mode)
   median_blocks(p,16,21,mode)
  for angles in ((.3,.4),(-.8,.17,1.1)):
   for scale in (0.,.03,-.04):phase_chain(angles,tuple(scale*(j+1)for j in range(len(angles))),mode)
 assert RUNS==84
 for h in (F(1,8),F(1,6),F(1,4)):
  for delta in (F(1,5),F(1,20)):
   m=moment_budget(h,delta);assert (1-4*h*h)**m<=delta**2 and majority_error(F(1,2)+h,m)<=delta
   v=variance_budget(h,delta);assert F(1,4)/(v*h*h)<=delta
 assert variance_budget(F(1,4),F(1,20))==81 and moment_budget(F(1,4),F(1,20))==21
 assert minimal_fixed_majority(F(3,4),F(1,20))==9 and grid_bits(32,F(1,32))==9
 assert target_coverage(F(3,4),F(5,8),64,F(1,32))>target_coverage(F(3,4),F(5,8),256,F(1,32))
 assert mean_budget(F(1,4),F(1,10),F(1,8))==160 and verified_budget(F(1,4),F(1,20))==11
 # Small independent median fixture: exact binomial block laws,not a circuit run.
 rows=binomial(F(1,2),4);coverage=sum((w0*w1*w2 for (j0,w0),(j1,w1),(j2,w2)in itertools.product(rows,repeat=3)if abs(F(sorted((j0,j1,j2))[1],4)-F(1,2))<=F(1,4)),F(0))
 bad=F(1)-sum((w for j,w in rows if abs(F(j,4)-F(1,2))<=F(1,4)),F(0));assert 1-coverage<=majority_error(1-bad,3)
 print('84 native CPU complex128 circuits: 36 raw-mean, 24 independent/shared-vote, 12 phase-chain and 12 median-block cases passed.')
 print('Both modes: full deterministic probabilities/densities and raw-record accounting checked; no one-record confidence or majority-success assertion.')
 print('At half-gap 1/4 and failure 1/20: variance budget 81, exact moment-bound budget 21, fixed-p=3/4 exact binomial minimum 9.')
 print('Bias-aware mean budget 160; 32-rotation grid needs 9 fractional bits for event budget 1/32; verified-success budget 11.')
 print(f'{invalid_checks()} malformed contracts rejected; calibration, independence and rigorous bias certificates are assumptions, not inferred from samples.')
if __name__=='__main__':main()
