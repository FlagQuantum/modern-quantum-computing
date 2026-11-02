"""44.1: dense payloads and requested outputs,not a universal simulation lower bound."""
import math,itertools
from dataclasses import replace
import torch,flagquantum as fq
try:
 from examples.foundations import statistical_ensembles as e,uniform_reversible as u
except ModuleNotFoundError:
 import statistical_ensembles as e,uniform_reversible as u
RUNS=0
RECEIPTS=[]

def dimension(n):
 if type(n)is not int or not 0<=n<=60:raise ValueError('Literal qubit count0..60required for bounded estimates')
 return 1<<n

def sizes(dtype):
 if dtype not in (torch.complex64,torch.complex128):raise ValueError('Explicit complex64orcomplex128required')
 return (8,4)if dtype==torch.complex64 else(16,8)

def storage(n,dtype=torch.complex128):
 N=dimension(n);z,r=sizes(dtype)
 return dict(dimension=N,state_bytes=z*N,density_bytes=z*N*N,dense_operator_bytes=z*N*N)

def payload(n,kind,*,count=1,qubits=None,shots=1,dtype=torch.complex128):
 N=dimension(n);z,r=sizes(dtype)
 if kind not in ('state','density','amplitudes','probabilities','expectations','samples'):raise ValueError('Named output kind required')
 if type(count)is not int or count<0 or type(shots)is not int or shots<1:raise ValueError('Nonnegative literal count and positive shots required')
 if qubits is None:qubits=tuple(range(n))
 if type(qubits)is not tuple or len(set(qubits))!=len(qubits)or any(type(j)is not int or not 0<=j<n for j in qubits):raise ValueError('Ordered unique qubit tuple required')
 m=len(qubits)
 if kind=='state':return dict(entries=N,bytes=z*N)
 if kind=='density':return dict(entries=N*N,bytes=z*N*N)
 if kind=='amplitudes':return dict(entries=count,bytes=z*count)
 if kind=='expectations':return dict(entries=count,bytes=r*count)
 if kind=='probabilities':return dict(entries=1<<m,bytes=r*(1<<m))
 return dict(entries=shots*m,packed_bits=shots*m,int64_bytes=8*shots*m)

def fit(n,mode,budget,dtype=torch.complex128):
 if mode not in ('statevector','density_matrix')or type(budget)is not int or budget<0:raise ValueError('Named mode and nonnegative byte budget required')
 return storage(n,dtype)['state_bytes'if mode=='statevector'else'density_bytes']<=budget

def work(n,k=1):
 N=dimension(n)
 if type(k)is not int or not 0<=k<=n:raise ValueError('Local support size0..nrequired')
 d=1<<k
 return dict(blocks=N//d,local_multiplications=N*d,local_additions=N*(d-1),dense_multiplications=N*N,dense_additions=N*(N-1),density_two_pass_multiplications=2*N*N*d)

def actual_arrays(n,dtype):
 if dimension(n)>64:raise ValueError('Array verification guard:N<=64;estimates need no allocation')
 v=torch.zeros(dimension(n),dtype=dtype);rho=torch.zeros((dimension(n),)*2,dtype=dtype);s=storage(n,dtype)
 assert(v.numel()*v.element_size(),rho.numel()*rho.element_size())==(s['state_bytes'],s['density_bytes'])
 return s

def configuration(n,theta,phi,flips,mask):
 if type(n)is not int or not 1<=n<=5 or any(type(t)not in(int,float)or not math.isfinite(t)for t in(theta,phi)):raise ValueError('Bounded finite CPU preparation required')
 if type(flips)is not tuple or len(flips)!=n or any(type(x)is not int or x not in(0,1)for x in flips):raise ValueError('Literal flip-bit tuple required')
 payload(n,'probabilities',qubits=mask)
 if not mask:raise ValueError('This native profile uses nonempty terminal masks')

def reference(n,theta,phi,flips):
 v=torch.zeros(1<<n,dtype=torch.complex128)
 v[u.index(flips)]=math.cos(theta/2)
 v[u.index(tuple(1-x for x in flips))]=complex(math.cos(phi),math.sin(phi))*math.sin(theta/2)
 return v

def marginal(v,n,mask):
 out=torch.zeros(1<<len(mask),dtype=torch.float64)
 for x in range(1<<n):
  bits=u.bits(x,n);out[u.index(tuple(bits[j]for j in mask))]+=abs(v[x].item())**2
 return out

def circuit(n,theta,phi,flips):
 c=fq.Circuit(n,dtype=torch.complex128).RY(0,theta=theta).P(0,theta=phi)
 for j in range(1,n):c.CX(0,j)
 for j,bit in enumerate(flips):
  if bit:c.X(j)
 return c

def xproduct(n):
 out=fq.X(0)
 for j in range(1,n):out=out@fq.X(j)
 return out

def execute(n,theta,phi,flips,mask,mode='statevector',profile='full',shots=19,seed=101):
 global RUNS
 configuration(n,theta,phi,flips,mask)
 if mode not in('statevector','density_matrix')or profile not in('state','queries','full')or(profile=='state'and mode!='statevector')or type(shots)is not int or not 1<=shots<=1000:raise ValueError('Supported bounded CPU request profile required')
 c=circuit(n,theta,phi,flips);outputs=None
 if profile!='state':
  outputs=[fq.probabilities(qubits=mask,name='selected'),fq.expectation(fq.Z(0),name='z'),fq.expectation(xproduct(n),name='x'),fq.samples(qubits=mask,name='raw')]
  if profile=='full':outputs +=[fq.probabilities(name='all'),fq.density_matrix(name='rho')]
 result=fq.run(c,outputs=outputs,shots=shots if outputs else None,options=replace(e.OPTIONS,mode=mode,seed=seed));RUNS+=1
 v=reference(n,theta,phi,flips);N=1<<n;record=dict(run=RUNS,n=n,theta=theta,phi=phi,flips=flips,mask=mask,mode=mode,profile=profile,seed=seed,shots=shots if outputs else None,native_gates=c.analysis().n_instructions)
 if mode=='statevector':
  vector=result.statevector()[0];e.close(vector,v);record['retained_state_bytes']=vector.numel()*vector.element_size();assert record['retained_state_bytes']==16*N
 if outputs:
  p=result.measurement('selected').value[0];raw=result.measurement('raw').value[0];e.close(p,marginal(v,n,mask))
  e.close(result.measurement('z').value[0],torch.tensor((-1)**flips[0]*math.cos(theta),dtype=torch.float64))
  e.close(result.measurement('x').value[0],torch.tensor(math.sin(theta)*math.cos(phi),dtype=torch.float64))
  assert raw.shape==(shots,len(mask))and bool(((raw==0)|(raw==1)).all())
  allowed={tuple(flips[j]for j in mask),tuple(1-flips[j]for j in mask)};assert all(tuple(row)in allowed for row in raw.tolist())
  record.update(selected_probability_bytes=p.numel()*p.element_size(),raw_tensor_bytes=raw.numel()*raw.element_size(),raw_rows=raw.tolist())
  assert record['selected_probability_bytes']==payload(n,'probabilities',qubits=mask)['bytes']
  assert record['raw_tensor_bytes']==payload(n,'samples',qubits=mask,shots=shots)['int64_bytes']
  if profile=='full':
   rho=result.measurement('rho').value[0];e.close(rho,v[:,None]*v.conj()[None,:]);e.close(result.measurement('all').value[0],abs(v)**2)
   record['density_output_bytes']=rho.numel()*rho.element_size();assert record['density_output_bytes']==16*N*N
 RECEIPTS.append(record);return result,record

def invalid_checks():
 calls=[lambda:dimension(True),lambda:dimension(-1),lambda:storage(3,torch.float64),lambda:payload(3,'vector-oracle'),lambda:payload(3,'probabilities',qubits=(1,1)),lambda:payload(3,'samples',qubits=(3,)),lambda:payload(3,'samples',shots=0),lambda:payload(3,'amplitudes',count=-1),lambda:fit(3,'hardware',10),lambda:fit(3,'statevector',-1),lambda:work(2,3),lambda:actual_arrays(7,torch.complex128),lambda:execute(2,.4,.2,(0,1),(0,1),profile='state',mode='density_matrix')]
 before=RUNS
 for call in calls:
  try:call()
  except ValueError:pass
  else:raise AssertionError('Invalid output/storage contract accepted')
 assert RUNS==before;return len(calls)

def main():
 for n in range(7):
  for dtype in(torch.complex64,torch.complex128):actual_arrays(n,dtype)
 assert storage(30)['state_bytes']==16*2**30 and storage(15)['density_bytes']==16*2**30
 assert fit(30,'statevector',16*2**30)and not fit(31,'statevector',16*2**30)
 assert payload(0,'probabilities',qubits=())==dict(entries=1,bytes=8)
 for n in range(1,5):
  flips=tuple(j%2 for j in range(n));mask=(0,)if n==1 else(n-1,0)
  for theta,phi in((0.,.3),(math.pi,-.6),(.83,-.47)):
   for mode in('statevector','density_matrix'):
    for profile in('queries','full'):execute(n,theta,phi,flips,mask,mode,profile)
  for theta in(.53,-.79):execute(n,theta,.61,flips,mask,profile='state')
 assert RUNS==56 and invalid_checks()==13
 for n in range(1,7):
  for k in range(n+1):
   d=2**k;N=2**n;w=work(n,k)
   assert w['blocks']*d*d==w['local_multiplications']==N*d
 print('56 native CPU complex128 circuits: 48 terminal query/full-output runs and eight state-only runs, n=1..4, both tested execution modes.')
 print('Scalar complex coordinates, full density, ordered marginals, Pauli expectations and terminal record schemas agree; no frequency-hit test.')
 print('14 actual complex64/complex128 array checks for n=0..6 match dense payload formulas; virtual 30-qubit state and 15-qubit density each require16GiB.')
 print('Selected requests retain the full statevector in this tested CPU profile; scalar output size does not certify scalar working memory.')
 print('Dense/local arithmetic counts, explicit-output payloads, budget endpoints and 13 invalid contracts passed; no hardware or universal simulation lower bound claimed.')
if __name__=='__main__':
 main()
 if len(__import__('sys').argv)>1:
  from pathlib import Path
  import json
  Path(__import__('sys').argv[1]).write_text(json.dumps(RECEIPTS,indent=2)+'\n')
