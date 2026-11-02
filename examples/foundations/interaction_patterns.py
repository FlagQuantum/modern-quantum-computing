"""14.7: eight editorial interaction patterns with explicit terminal-only contracts."""
import math,cmath,itertools
from dataclasses import dataclass,replace
from fractions import Fraction as F
import torch,flagquantum as fq
try:
 from examples.foundations import statistical_ensembles as e
except ModuleNotFoundError:
 import statistical_ensembles as e
D=torch.complex128;RUNS=0
H=torch.tensor([[1,1],[1,-1]],dtype=D)/math.sqrt(2)
SD=torch.diag(torch.tensor([1,-1j],dtype=D));X=torch.tensor([[0,1],[1,0]],dtype=D)
PATTERNS=('subroutine pipeline','variational outer loop','hybrid learning/features','in-execution adaptive feedback','measurement-driven inference','decomposition/reconstruction','embedded/self-consistent solver','heterogeneous workflow')

def real(x):
 if type(x)not in (int,float)or not math.isfinite(x)or abs(x)>10:raise ValueError('Finite real radians/scalars within teaching range[-10,10]required')
 return x
@dataclass(frozen=True)
class Task:
 name:str
 revision:int
 theta:float
 phi:float=0.
 basis:str='Z'
 shots:int=31
 def __post_init__(self):
  if type(self.name)is not str or not self.name or type(self.revision)is not int or self.revision<0 or self.basis not in ('X','Y','Z')or type(self.shots)is not int or not 1<=self.shots<=1000:raise ValueError('Task identity,revision,basis and literal shot count1..1000required')
  real(self.theta);real(self.phi)
@dataclass(frozen=True)
class Packet:
 task:Task
 bits:tuple
 source:str='cpu-simulator-terminal-bits'

def checked(packet,task):
 if type(task)is not Task or type(packet)is not Packet or packet.task!=task or packet.source!='cpu-simulator-terminal-bits' or type(packet.bits)is not tuple or len(packet.bits)!=task.shots or any(type(b)is not int or b not in (0,1)for b in packet.bits):raise ValueError('Matching revision/parameters/basis/shots and raw terminal bit provenance required')
 return packet

def sample_mean(packet,task):
 checked(packet,task);return F(sum(1-2*b for b in packet.bits),task.shots)

def execute(task,c,mode='statevector'):
 global RUNS
 if type(task)is not Task or mode not in ('statevector','density_matrix'):raise ValueError('Validated task and tested CPU mode required')
 if task.basis=='X':c.H(0)
 if task.basis=='Y':c.SDG(0).H(0)
 v=torch.tensor([math.cos(task.theta/2),cmath.exp(1j*task.phi)*math.sin(task.theta/2)],dtype=D)
 mu={'X':math.sin(task.theta)*math.cos(task.phi),'Y':math.sin(task.theta)*math.sin(task.phi),'Z':math.cos(task.theta)}[task.basis]
 target=(H@v if task.basis=='X'else H@SD@v if task.basis=='Y'else v)
 result=fq.run(c,outputs=[fq.density_matrix(name='rho'),fq.probabilities(name='p'),fq.expectation(fq.Z(0),name='mu'),fq.samples(qubits=(0,),name='raw')],shots=task.shots,options=replace(e.OPTIONS,mode=mode,seed=71+task.revision));RUNS+=1
 e.close(result.measurement('rho').value[0],torch.outer(target,target.conj()))
 e.close(result.measurement('p').value[0],torch.tensor([(1+mu)/2,(1-mu)/2],dtype=torch.float64))
 native=float(result.expectation('mu')[0]);assert abs(native-mu)<=1e-12
 if mode=='statevector':e.close(result.statevector()[0],target)
 raw=result.measurement('raw').value;assert raw.shape==(1,task.shots,1)
 packet=Packet(task,tuple(int(b)for b in raw[0,:,0]));checked(packet,task)
 return packet,dict(native_mu=native,scalar_mu=mu,statevector_diagnostic_available=mode=='statevector')

def run_task(task,mode='statevector'):
 if type(task)is not Task:raise ValueError('Task record required')
 c=fq.Circuit(1,dtype=D).RY(0,theta=task.theta).P(0,theta=task.phi)
 return execute(task,c,mode)

def outer(candidates,target=0.,mode='statevector'):
 real(target)
 if type(candidates)is not tuple or not 1<=len(candidates)<=5:raise ValueError('Finite candidate tuple of length1..5required')
 for t in candidates:real(t)
 rows=[]
 for j,t in enumerate(candidates):
  task=Task('outer',j,t);packet,diag=run_task(task,mode)
  measured=float(sample_mean(packet,task));rows.append(dict(theta=t,sampled_mean=measured,sampled_loss=(measured-target)**2,diagnostic_loss=(diag['native_mu']-target)**2))
 chosen=min(range(len(rows)),key=lambda i:rows[i]['sampled_loss'])
 assert all(rows[chosen]['sampled_loss']<=x['sampled_loss']for x in rows)
 return rows,chosen

def kernel(x,y,mode='statevector'):
 real(x);real(y);task=Task('kernel',0,x-y)
 c=fq.Circuit(1,dtype=D).RY(0,theta=x).RY(0,theta=-y)
 p,d=execute(task,c,mode);exact=(1+d['native_mu'])/2
 assert abs(exact-math.cos((x-y)/2)**2)<=1e-12
 return p,exact

def branch_phase(amp):
 mag=abs(amp);p=mag*mag
 if mag and p==0:raise ValueError('Positive branch probability underflow rejected before execution')
 return p,(amp/mag if mag else None)

def feedback(theta,phi=0.,mode='statevector'):
 global RUNS
 real(theta);real(phi)
 if mode not in ('statevector','density_matrix'):raise ValueError('Tested CPU mode required')
 c0=math.cos(theta/2);c1=cmath.exp(1j*phi)*math.sin(theta/2)
 weights=tuple(branch_phase(amp)for amp in (c0,c1))
 joint=torch.tensor([c0,0,0,c1],dtype=D);product=torch.tensor([c0,0,c1,0],dtype=D)
 results=[]
 for coherent,target in ((False,joint),(True,product)):
  c=fq.Circuit(2,dtype=D).RY(0,theta=theta).P(0,theta=phi).CX(0,1)
  if coherent:c.CX(0,1)
  out=fq.run(c,outputs=[fq.density_matrix(name='rho'),fq.probabilities(qubits=(0,),name='control'),fq.samples(qubits=(0,),name='raw')],shots=19,options=replace(e.OPTIONS,mode=mode,seed=79));RUNS+=1
  e.close(out.measurement('rho').value[0],torch.outer(target,target.conj()))
  if mode=='statevector':e.close(out.statevector()[0],target)
  e.close(out.measurement('control').value[0],torch.tensor([abs(c0)**2,abs(c1)**2],dtype=torch.float64));results.append(out)
 # Explicit mathematical branches of the pre-measurement vector;not native retained-state handles.
 branches=[];corrected=torch.zeros((4,4),dtype=D)
 for bit,amp in enumerate((c0,c1)):
  p,phase=weights[bit]
  if p==0:branches.append((p,None));continue
  v=torch.zeros(2,dtype=D);v[bit]=phase
  fixed=X@v if bit else v
  e.close(torch.outer(fixed,fixed.conj()),torch.diag(torch.tensor([1.,0.],dtype=D)))
  globalv=torch.zeros(4,dtype=D);globalv[2*bit]=amp
  corrected+=torch.outer(globalv,globalv.conj());branches.append((p,fixed))
 e.close(corrected,torch.diag(torch.tensor([abs(c0)**2,0,abs(c1)**2,0],dtype=D)))
 return branches,corrected,results

def require_retained_state(backend):
 # Capability contract of this chapter's terminal-only executable,not a framework-wide claim.
 if backend!='tested-terminal-path-with-no-state-handle':raise ValueError('Declare the tested capability profile')
 raise ValueError('This terminal-only path has no same-execution measured-branch continuation contract')

def reconstruct(a,b,mode='statevector'):
 real(a);real(b);real(a+b)
 rows={};estimates={}
 for tag,theta in (('a',a),('b',b)):
  for basis in ('X','Z'):
   task=Task(tag+basis,0,theta,basis=basis);p,d=run_task(task,mode);rows[tag+basis]=d['native_mu'];estimates[tag+basis]=float(sample_mean(p,task))
 task=Task('uncut',0,a+b);_,uncut=run_task(task,mode)
 exact=rows['aZ']*rows['bZ']-rows['aX']*rows['bX']
 sampled=estimates['aZ']*estimates['bZ']-estimates['aX']*estimates['bX']
 assert abs(exact-uncut['native_mu'])<=1e-12
 assert abs(exact-math.cos(a+b))<=1e-12 and -2<=sampled<=2
 return exact,sampled

def embedding(g,v,steps=3,source='samples',mode='statevector'):
 real(g);real(v)
 if not 0<=g<1 or abs(v)>1 or type(steps)is not int or not 1<=steps<=4 or source not in ('samples','exact-simulator'):raise ValueError('Toy solver g in[0,1),|v|<=1,1..4steps and explicit data source required')
 trace=[]
 for k in range(steps):
  theta=math.atan(g*v);task=Task('embedded-X',k,theta,basis='X');packet,diag=run_task(task,mode)
  expected=g*v/math.sqrt(1+(g*v)**2);assert abs(expected-diag['native_mu'])<=1e-12
  vector=torch.tensor([math.cos(theta/2),math.sin(theta/2)],dtype=D)
  ham=torch.tensor([[-1.,-g*v],[-g*v,1.]],dtype=D)
  e.close(ham@vector,-math.sqrt(1+(g*v)**2)*vector)
  new=float(sample_mean(packet,task))if source=='samples'else diag['native_mu']
  trace.append(dict(v=v,theta=theta,new_v=new,residual=abs(new-v),source=source));v=new
 return trace

def accept_once(packet,expected,accepted):
 checked(packet,expected);key=(expected.name,expected.revision)
 if key in accepted:raise ValueError('Duplicate result is not a new observation')
 accepted.add(key);return sample_mean(packet,expected)

def invalid_checks():
 task=Task('t',0,.2,shots=3);p=Packet(task,(0,1,0));before=RUNS
 calls=[lambda:Task('',0,.2),lambda:Task('t',-1,.2),lambda:Task('t',0,math.nan),lambda:Task('t',0,.2,basis='I'),lambda:Task('t',0,.2,shots=True),lambda:Task('t',0,.2,shots=0),lambda:checked(replace(p,source='statevector-diagnostic'),task),lambda:checked(replace(p,bits=(0,1)),task),lambda:checked(replace(p,bits=(0,1,2)),task),lambda:checked(p,replace(task,revision=1)),lambda:checked(p,replace(task,basis='X')),lambda:run_task(task,'hardware'),lambda:outer(()),lambda:embedding(.5,.2,source='unlabelled'),lambda:require_retained_state('tested-terminal-path-with-no-state-handle'),lambda:accept_once(p,task,{('t',0)}),lambda:feedback(1e-200),lambda:reconstruct(6.,6.)]
 for call in calls:
  try:call()
  except ValueError:pass
  else:raise AssertionError('Malformed interaction contract accepted')
 assert RUNS==before;return len(calls)

def main():
 packets=[]
 for mode in ('statevector','density_matrix'):
  for theta in (0.,math.pi/2,.83):
   for phi in (0.,.61):
    for basis in ('X','Y','Z'):
     t=Task(f'{mode}-{theta}-{phi}-{basis}',0,theta,phi,basis);p,_=run_task(t,mode);packets.append(p)
  outer((0.,math.pi/2,math.pi),mode=mode)
  for x,y in ((.2,.7),(-.4,.9)):kernel(x,y,mode)
  for theta in (0.,math.pi/2,1.1):feedback(theta,.4,mode)
  for a,b in ((.2,.7),(-.3,.8)):reconstruct(a,b,mode)
  for source in ('samples','exact-simulator'):embedding(.5,.8,3,source,mode)
 assert RUNS==90
 accepted=set()
 for packet in reversed(packets):accept_once(packet,packet.task,accepted)
 assert len(accepted)==36 and len(PATTERNS)==8
 probability,phase=branch_phase(1e-160)
 assert probability>0 and phase==1
 assert invalid_checks()==18
 print('90 native CPU complex128 circuits: 36 basis/feature, 6 outer-candidate, 4 kernel, 12 feedback-reference, 20 reconstruction and 12 embedded-loop executions passed.')
 print('Both modes: full vector/density, scalar probability and native expectation references checked; samples used only through validated terminal records.')
 print('Eight editorial patterns classified; sampled/exact-simulator data, new preparations/coherent references and task revisions remain distinct.')
 print('36 out-of-order packets accepted once; 18 malformed/stale/diagnostic/unsupported-lifetime contracts rejected before further execution.')
 print('No retained measured-state handle, dynamic feedback, GPU/QPU run, general cutting/embedding solver or learning-speedup claim is made.')
if __name__=='__main__':main()
