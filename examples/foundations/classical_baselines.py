"""14.8: matched task contracts and explicit classical baselines,not an advantage certifier."""
import math,itertools,random
from fractions import Fraction as F
from dataclasses import dataclass,replace
import torch,flagquantum as fq
try:
 from examples.foundations import statistical_ensembles as e,uniform_reversible as u,accuracy_repetition as a
except ModuleNotFoundError:
 import statistical_ensembles as e,uniform_reversible as u,accuracy_repetition as a
RUNS=0

def inputs(ps):
 if type(ps)is not tuple or len(ps)>5 or any(type(p)is not F or not 0<=p<=1 for p in ps):raise ValueError('Explicit tuple of0..5exact rational bit probabilities required')
 return ps

def integer_pair(ps):
 inputs(ps);den=1;sign=1
 for p in ps:den*=p.denominator;sign*=p.denominator-2*p.numerator
 num=den-sign;den*=2
 assert 0<=num<=den
 return num,den

def exact_mean(ps):return F(*integer_pair(ps))

def enumerate_law(ps):
 inputs(ps);q=F(0);mass=F(0)
 for bits in itertools.product((0,1),repeat=len(ps)):
  weight=math.prod(p if bit else 1-p for bit,p in zip(bits,ps));mass+=weight
  if sum(bits)%2:q+=weight
 assert mass==1;return q

def records(ps,shots,seed=101,method='product'):
 inputs(ps)
 if type(shots)is not int or not 1<=shots<=1000 or type(seed)is not int or method not in ('product','coins'):raise ValueError('Literal shots1..1000,integer seed and named classical sampler required')
 rng=random.Random(seed)
 if method=='product':
  q=exact_mean(ps);return tuple(int(rng.randrange(q.denominator)<q.numerator)for _ in range(shots))
 return tuple(sum(int(rng.randrange(p.denominator)<p.numerator)for p in ps)%2 for _ in range(shots))

@dataclass(frozen=True)
class Contract:
 instances:tuple
 output:str='mean'
 access:str='explicit-rational-list'
 epsilon:F=F(1,4)
 delta:F=F(1,20)
 record_count:int=0
 def __post_init__(self):
  if type(self.instances)is not tuple or not self.instances or self.output not in ('mean','records')or self.access not in ('explicit-rational-list','oracle-only')or type(self.epsilon)is not F or not 0<=self.epsilon<=1 or type(self.delta)is not F or not 0<=self.delta<1:raise ValueError('Declared instance set,output/access and exact accuracy/failure contract required')
  if type(self.record_count)is not int or(self.output=='mean'and self.record_count!=0)or(self.output=='records'and(not 1<=self.record_count<=1000 or self.epsilon!=0 or self.delta!=0)):raise ValueError('Mean output has no fixed record count;ideal exact-law records require length1..1000 and zero declared law error')
  for ps in self.instances:inputs(ps)

def fulfills(candidate,required):
 if type(candidate)is not Contract or type(required)is not Contract or candidate.instances!=required.instances or candidate.output!=required.output or candidate.record_count!=required.record_count or candidate.access!=required.access or candidate.epsilon>required.epsilon or candidate.delta>required.delta:raise ValueError('Same task/access/instances and no weaker accuracy/failure guarantee required')
 return True

def cost_ratio(classical,quantum,unit_c='declared-work',unit_q='declared-work'):
 if type(classical)is not int or classical<0 or type(quantum)is not int or quantum<=0 or unit_c!=unit_q:raise ValueError('Nonnegative/positive costs in matching declared units required')
 return F(classical,quantum)

def end_cost(setup,trial,repeats,post):
 if any(type(x)is not int or x<0 for x in (setup,trial,repeats,post)):raise ValueError('Nonnegative literal cost and repetition counts required')
 return setup+trial*repeats+post

def finite_curves(n,cutoff):
 if type(n)is not int or type(cutoff)is not int or n<1 or cutoff<1:raise ValueError('Positive literal sizes/cutoff required')
 return dict(quantum_model=n,classical_A=n,classical_B=n if n<=cutoff else n*n)

def claim_scope(kind,source):
 if kind=='software-correctness'and source=='CPU-simulator':return 'Bounded implementation evidence only'
 if kind=='CPU-timing-over-named-code'and source=='CPU-simulator':return 'Dated software timing,not QPU speedup or optimal-classical lower bound'
 raise ValueError('These toy CPU receipts cannot certify hardware or asymptotic quantum advantage')

def _circuit(ps):
 inputs(ps);c=fq.Circuit(len(ps)+1,dtype=torch.complex128)
 for j,p in enumerate(ps):c.RY(j,theta=2*math.asin(math.sqrt(float(p))))
 for j in range(len(ps)):c.CX(j,len(ps))
 return c

def _shots(shots,seed,mode):
 if type(shots)is not int or not 1<=shots<=1000 or type(seed)is not int or mode not in ('statevector','density_matrix'):raise ValueError('Fixed shots1..1000,integer seed and tested CPU mode required')

def native_records(ps,shots=31,seed=101,mode='statevector'):
 global RUNS
 inputs(ps);_shots(shots,seed,mode);c=_circuit(ps)
 result=fq.run(c,outputs=[fq.samples(qubits=(len(ps),),name='raw')],shots=shots,options=replace(e.OPTIONS,mode=mode,seed=seed));RUNS+=1
 raw=result.measurement('raw').value;assert raw.shape==(1,shots,1)and bool(((raw==0)|(raw==1)).all())
 return tuple(int(b)for b in raw[0,:,0])

def validate_native(ps,shots=31,seed=101,mode='statevector'):
 global RUNS
 inputs(ps);_shots(shots,seed,mode);c=_circuit(ps);n=len(ps);q=exact_mean(ps)
 assert q==enumerate_law(ps)
 target=torch.zeros(2**(n+1),dtype=torch.complex128)
 for bits in itertools.product((0,1),repeat=n):
  amp=math.prod(math.sqrt(float(p if bit else 1-p))for bit,p in zip(bits,ps))
  target[u.index(bits+(sum(bits)%2,))]=amp
 result=fq.run(c,outputs=[fq.density_matrix(name='rho'),fq.probabilities(qubits=(n,),name='p'),fq.samples(qubits=(n,),name='raw')],shots=shots,options=replace(e.OPTIONS,mode=mode,seed=seed));RUNS+=1
 e.close(result.measurement('rho').value[0],torch.outer(target,target.conj()))
 e.close(result.measurement('p').value[0],torch.tensor([float(1-q),float(q)],dtype=torch.float64))
 if mode=='statevector':e.close(result.statevector()[0],target)
 raw=result.measurement('raw').value;assert raw.shape==(1,shots,1)and bool(((raw==0)|(raw==1)).all())
 assert c.analysis().n_instructions==2*n
 return tuple(int(b)for b in raw[0,:,0]),q

def check_bits(bits,shots):
 if type(bits)is not tuple or len(bits)!=shots or any(type(b)is not int or b not in (0,1)for b in bits):raise ValueError('Exactly the requested literal raw bits required')
 return F(sum(bits),shots)

def invalid_checks():
 cases=(((F(1,3),F(2,5))),);task=Contract(cases)
 calls=[lambda:inputs((.5,)),lambda:inputs((F(-1,2),)),lambda:inputs((F(1,2),)*6),lambda:records((),0),lambda:native_records((),True),lambda:native_records((),mode='hardware'),lambda:Contract(cases,epsilon=.1),lambda:fulfills(replace(task,output='records',record_count=3,epsilon=F(0),delta=F(0)),task),lambda:fulfills(replace(task,access='oracle-only'),task),lambda:fulfills(replace(task,epsilon=F(1,2)),task),lambda:fulfills(replace(task,delta=F(1,10)),task),lambda:fulfills(Contract(((F(0),),)),task),lambda:cost_ratio(3,0),lambda:cost_ratio(2,1,'gates','seconds'),lambda:end_cost(0,-1,1,0),lambda:claim_scope('asymptotic-quantum-advantage','CPU-simulator'),lambda:check_bits((0,2),2),lambda:check_bits((0,),2),lambda:Contract(cases,output='records',epsilon=F(0),delta=F(0)),lambda:fulfills(Contract(cases,output='records',epsilon=F(0),delta=F(0),record_count=7),Contract(cases,output='records',epsilon=F(0),delta=F(0),record_count=8))]
 before=RUNS
 for call in calls:
  try:call()
  except ValueError:pass
  else:raise AssertionError('Invalid baseline/comparison contract accepted')
 assert RUNS==before;return len(calls)

def main():
 cases=[()]+[ps for n in range(1,5)for ps in ((F(0),)*n,(F(1),)*n,tuple(F(j+1,2*j+3)for j in range(n))) ]
 for ps in cases:
  assert exact_mean(ps)==enumerate_law(ps)
  for mode in ('statevector','density_matrix'):
   for shots in (1,31):
    bits,q=validate_native(ps,shots,mode=mode);check_bits(bits,shots)
  for method in ('coins','product'):check_bits(records(ps,31,method=method),31)
 assert RUNS==52
 for ps in cases:
  B=sum(p.denominator.bit_length()for p in ps);num,den=integer_pair(ps)
  assert num.bit_length()<=B+2 and den.bit_length()<=B+2
 task=Contract(tuple(cases));assert fulfills(replace(task,epsilon=F(0),delta=F(0)),task)
 assert a.mean_budget(F(1,4),F(1,20))==80
 assert cost_ratio(2,1)==2 and cost_ratio(end_cost(0,2,1,10),end_cost(100,1,1,0))==F(12,101)
 for n in range(1,17):assert finite_curves(n,16)['classical_A']==finite_curves(n,16)['classical_B']
 assert finite_curves(17,16)['classical_A']!=finite_curves(17,16)['classical_B']
 print('52 native CPU complex128 circuits: 13 explicit rational-input cases, two modes and two record lengths passed.')
 print('Exact integer-product, exhaustive finite-law and scalar amplitude/density references agree; classical coin and product samplers return the requested records.')
 print('Exact-mean baseline meets any looser mean accuracy contract; 80-shot ideal estimation budget is separate from implementation-bias certification.')
 print('Kernel-only ratio 2 becomes end-to-end ratio 12/101 in declared synthetic work units; finite data do not decide asymptotic behavior.')
 print(f'{invalid_checks()} invalid task/access/precision/cost/claim/record contracts rejected before further execution; no quantum advantage claimed.')
if __name__=='__main__':main()
