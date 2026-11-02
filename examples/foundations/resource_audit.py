"""14.9: bounded CPU resource-audit laboratory; not hardware certification."""
import math,itertools,json,hashlib,copy
from fractions import Fraction as F
from dataclasses import dataclass,replace
import torch,flagquantum as fq
try:
 from examples.foundations import classical_baselines as b,statistical_ensembles as e,uniform_reversible as u,accuracy_repetition as a
except ModuleNotFoundError:
 import classical_baselines as b,statistical_ensembles as e,uniform_reversible as u,accuracy_repetition as a
RUNS=0
RECEIPTS=[]
PACKETS=[]
@dataclass(frozen=True)
class Plan:
 ps:tuple
 epsilon:F=F(1,8)
 beta:F=F(1,64)
 delta:F=F(1,10)
 units:str='rad'
 def __post_init__(self):
  b.inputs(self.ps)
  if not 1<=len(self.ps)<=4 or self.units!='rad' or any(type(x)is not F for x in (self.epsilon,self.beta,self.delta))or not 0<self.beta<self.epsilon<1 or not 0<self.delta<1:raise ValueError('Exact bounded rational plan,positive bias budget and radians required')
  if self.shots>501:raise ValueError('Exact binomial reference guard: at most501shots')
 @property
 def bits(self):
  z=0
  while F(len(self.ps),2**(z+1))>self.beta:z+=1
  return z
 @property
 def quantized(self):return tuple(F(round(p*2**self.bits),2**self.bits)for p in self.ps)
 @property
 def bound(self):return F(len(self.ps),2**(self.bits+1))
 @property
 def shots(self):return a.mean_budget(self.epsilon,self.delta,self.beta)
 @property
 def identity(self):
  payload=['resource-audit-v1',[str(p)for p in self.ps],str(self.epsilon),str(self.beta),str(self.delta),self.units]
  return hashlib.sha256(json.dumps(payload,separators=(',',':')).encode()).hexdigest()

def reference(ps):
 n=len(ps);v=torch.zeros(2**(n+1),dtype=torch.complex128)
 for bits in itertools.product((0,1),repeat=n):
  v[u.index(bits+(sum(bits)%2,))]=math.sqrt(float(math.prod(p if bit else 1-p for p,bit in zip(ps,bits))))
 return v

def circuit(plan,reverse=False,fault=None,basis=None):
 n=len(plan.ps);c=fq.Circuit(n+1,dtype=torch.complex128);order=tuple(range(n))[::(-1 if reverse else 1)]
 if basis is None:
  for j in order:c.RY(j,theta=2*math.asin(math.sqrt(float(plan.quantized[j]))))
 else:
  for j,bit in enumerate(basis):
   if bit:c.X(j)
 for j in order:
  if fault!='drop-CX' or j!=n-1:c.CX(j,n)
 if fault=='flip-output':c.X(n)
 return c

def execute(plan,mode='statevector',reverse=False,fault=None,basis=None,seed=101):
 global RUNS
 if mode not in ('statevector','density_matrix')or fault not in (None,'drop-CX','flip-output','wrong-query','reverse-mask'):raise ValueError('Named bounded CPU execution required')
 n=len(plan.ps);c=circuit(plan,reverse,fault,basis);mask=tuple(range(n+1));query=n
 if fault=='reverse-mask':mask=mask[::-1]
 if fault=='wrong-query':query=0
 shots=plan.shots if basis is None else 5
 r=fq.run(c,outputs=[fq.density_matrix(name='rho'),fq.probabilities(qubits=(query,),name='p'),fq.samples(qubits=mask,name='raw')],shots=shots,options=replace(e.OPTIONS,mode=mode,seed=seed));RUNS+=1
 raw=r.measurement('raw').value[0];ir=c.to_ir();analysis=c.analysis()
 packet=dict(identity=plan.identity,source='CPU-simulator',units='rad',mask=list(mask),query=query,shots=shots,basis=None if basis is None else list(basis),rows=raw.tolist(),ones=int(raw[:,-1].sum()),gates=analysis.n_instructions,depth=analysis.depth,raw_bytes=raw.numel()*raw.element_size(),baseline=str(b.exact_mean(plan.ps)),claim='software-correctness',rho=r.measurement('rho').value[0],prob=r.measurement('p').value[0])
 assert sum(analysis.gate_counts.values())==len(ir.instructions)==packet['gates']
 if mode=='statevector':packet['vector']=r.statevector()[0]
 RECEIPTS.append(dict(run=RUNS,mode=mode,fault=fault,basis=packet['basis'],reverse=reverse,identity=plan.identity,shots=shots,gates=packet['gates'],depth=packet['depth']))
 PACKETS.append(dict(plan=dict(ps=[str(x)for x in plan.ps],epsilon=str(plan.epsilon),beta=str(plan.beta),delta=str(plan.delta),seed=seed),packet={k:dict(real=v.real.tolist(),imag=v.imag.tolist())if isinstance(v,torch.Tensor)and v.is_complex()else v.tolist()if isinstance(v,torch.Tensor)else v for k,v in packet.items()}))
 return packet

def record_check(rows,shots,n):
 if len(rows)!=shots or any(type(row)is not list or len(row)!=n+1 or any(type(x)is not int or x not in (0,1)for x in row)for row in rows):raise ValueError('Exact full-register bit record schema required')
 if any(row[-1]!=sum(row[:-1])%2 for row in rows):raise ValueError('Joint parity invariant violated')
 return sum(row[-1]for row in rows)

def audit(plan,p):
 n=len(plan.ps);basis=p['basis'];shots=plan.shots if basis is None else 5
 if p['identity']!=plan.identity or p['source']!='CPU-simulator'or p['units']!='rad'or p['query']!=n or p['mask']!=list(range(n+1))or p['shots']!=shots:raise ValueError('Stale/source/unit/output/budget mismatch')
 if p['baseline']!=str(b.exact_mean(plan.ps))or p['claim']!='software-correctness':raise ValueError('Baseline or claim scope mismatch')
 if basis is not None and(type(basis)is not list or len(basis)!=n or any(type(x)is not int or x not in (0,1)for x in basis)):raise ValueError('Malformed calibration input')
 count=record_check(p['rows'],shots,n)
 if count!=p['ones']:raise ValueError('Counts do not reproduce raw records')
 gates=2*n if basis is None else n+sum(basis);depth=n+1 if basis is None else n+basis[0]
 if(p['gates'],p['depth'])!=(gates,depth):raise ValueError('Underreported or changed logical resource recipe')
 if basis is None:ps=plan.quantized
 else:
  ps=tuple(F(x)for x in basis)
  if any(row!=basis+[sum(basis)%2]for row in p['rows']):raise ValueError('Calibration label mismatch')
 v=reference(ps);rho=v[:,None]*v.conj()[None,:];q=b.exact_mean(ps)
 e.close(p['rho'],rho);e.close(p['prob'],torch.tensor([1-float(q),float(q)],dtype=torch.float64))
 if 'vector'in p:e.close(p['vector'],v)
 target=b.exact_mean(plan.ps)
 return dict(accepted=True,observed_mean=str(F(count,shots)),observed_miss=abs(F(count,shots)-target)>plan.epsilon,scope='CPU software evidence; ideal-model probability guarantee is conditional')

def resources(plan):
 n=len(plan.ps);S=plan.shots;K=2**n;T=5*K;gcal=5*(n*K+n*2**(n-1));dcal=5*(n*K+K//2)
 return dict(main_preparations=S,calibration_preparations=T,total_preparations=S+T,peak_qubits=n+1,main_gates=2*n*S,calibration_gates=gcal,total_gates=2*n*S+gcal,total_serial_gate_layers=(n+1)*S+dcal,initializations=(n+1)*(S+T),record_bits=(n+1)*(S+T),native_calls=K+1,row_parity_checks=S+T,bit_checks=(n+1)*(S+T),counter_bits=S.bit_length(),angle_payload_bits=64*n,quantized_numerator_payload_bits=n*(plan.bits+1),statevector_array_bytes=16*2**(n+1),density_array_bytes=16*4**(n+1))

def rejection(plan,p,reason):
 try:audit(plan,p)
 except(ValueError,AssertionError):return reason
 raise AssertionError('Bad audit packet accepted: '+reason)

def mutations(plan,p):
 changes=[('identity','stale'),('source','hardware'),('units','deg'),('shots',p['shots']-1),('ones',p['ones']+1),('gates',p['gates']-1),('depth',p['depth']-1),('baseline','0'),('claim','quantum-advantage')]
 for key,value in changes:
  bad=copy.deepcopy(p);bad[key]=value;rejection(plan,bad,key)
 bad=copy.deepcopy(p);bad['rows']=bad['rows'][:-1];rejection(plan,bad,'short raw record')
 bad=copy.deepcopy(p);bad['rows'][0][0]=2;rejection(plan,bad,'nonbinary')
 return len(changes)+2

def invalid_checks():
 calls=[lambda:Plan((.5,)),lambda:Plan(()),lambda:Plan((F(1,2),)*5),lambda:Plan((F(-1),)),lambda:Plan((F(1,2),),units='deg'),lambda:Plan((F(1,2),),beta=F(0)),lambda:Plan((F(1,2),),epsilon=F(1,64)),lambda:Plan((F(1,2),),delta=F(-1)),lambda:Plan((F(1,2),),epsilon=F(1,100))]
 before=RUNS
 for call in calls:
  try:call()
  except ValueError:pass
  else:raise AssertionError('Invalid preflight plan accepted')
 assert RUNS==before;return len(calls)

def main():
 base=Plan((F(1,4),F(1,3),F(2,5)));saved=None;rawbytes=0
 cases=[(F(1,3),),(F(1,3),F(2,5)),base.ps,(F(1,5),F(2,7),F(3,11),F(4,13))]
 for ps in cases:
  plan=Plan(ps);assert b.exact_mean(ps)==b.enumerate_law(ps)
  assert abs(b.exact_mean(plan.quantized)-b.exact_mean(ps))<=sum(abs(x-y)for x,y in zip(ps,plan.quantized))<=plan.bound<=plan.beta
  assert a.target_coverage(b.exact_mean(ps),b.exact_mean(plan.quantized),plan.shots,plan.epsilon)>=1-plan.delta
  for mode in ('statevector','density_matrix'):
   for reverse in (False,True):
    packet=execute(plan,mode,reverse);audit(plan,packet)
    if ps==base.ps and mode=='statevector'and not reverse:saved=packet;rawbytes=packet['raw_bytes']
 for mode in ('statevector','density_matrix'):
  for bits in itertools.product((0,1),repeat=3):
   p=execute(base,mode,basis=bits);audit(base,p)
   if mode=='statevector':rawbytes+=p['raw_bytes']
 faults=[(base,'statevector','drop-CX'),(base,'density_matrix','wrong-query'),(Plan((F(1,2),F(1,4))),'statevector','flip-output'),(base,'statevector','reverse-mask')]
 reports=[]
 for plan,mode,fault in faults:reports.append(rejection(plan,execute(plan,mode,fault=fault),fault))
 assert RUNS==36 and mutations(base,saved)==11 and invalid_checks()==9
 assert base.bits==7 and base.shots==209 and b.exact_mean(base.quantized)==F(7919,16384)
 assert b.exact_mean(base.quantized)-b.exact_mean(base.ps)==F(1,245760)
 ledger=resources(base);assert(ledger['total_preparations'],ledger['total_gates'],ledger['total_serial_gate_layers'],ledger['record_bits'])==(249,1434,976,996)
 # A possible record is not a claimed native receipt,even if its estimate misses.
 extreme=[[1,0,0,1]for _ in range(base.shots)];assert record_check(extreme,base.shots,3)==209
 assert abs(F(1)-b.exact_mean(base.ps))>base.epsilon
 print('36 native CPU complex128 calls: 16 main experiments, 16 basis calibrations and four deliberately faulty executions audited.')
 print('Exact input/grid/bias/binomial references passed; b=7, S=209, q=29/60, grid q=7919/16384, actual grid bias=1/245760.')
 print('One base audit: 249 conceptual preparations, 1434 logical gates, 976 serial gate layers, 996 record bits, peak four qubits, nine native calls.')
 print(f'Actual raw tensor storage for that audit: {rawbytes} bytes; payload bits and simulator arrays are separate units.')
 print('Four faulty executions, 11 mutated packets and nine preflight contracts rejected; a constructed possible confidence miss is diagnostic only.')
 print('Exact classical scalar baseline remains eligible; no hardware confidence certificate, physical latency or quantum advantage claimed.')
 return dict(receipts=RECEIPTS,packets=PACKETS,ledger=ledger,fault_reports=reports,raw_tensor_bytes=rawbytes)
if __name__=='__main__':
 report=main()
 if len(__import__('sys').argv)>1:
  with open(__import__('sys').argv[1],'w')as f:json.dump(report,f,indent=2);f.write('\n')
