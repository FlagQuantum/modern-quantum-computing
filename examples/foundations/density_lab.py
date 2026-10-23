"""8.8: bounded density-operator candidate acceptance,without repairs."""
import math,torch
try:
 from examples.foundations import purification as g,statistical_ensembles as e,partial_trace as t
except ModuleNotFoundError:
 import purification as g,statistical_ensembles as e,partial_trace as t
D=e.D;ATOL=1e-12

def reference(p,phi):
 if type(p)not in (int,float)or not math.isfinite(p)or not 0<=p<=1:raise ValueError('Finite probability required')
 Q=e.prepare(e.qubit(.83,phi));C,rho=g.spectral((p,1-p),Q,2)
 return C,rho

def prepare(p,phi,mode='statevector',W=None):
 C,rho=reference(p,phi);result,target=g.execute(C,W,mode)
 return {'full':result.measurement('full').value[0].clone(),'S':result.measurement('S').value[0].clone(),'R':result.measurement('R').value[0].clone()},C

def report(packet,C,scope='joint',atol=ATOL):
 if scope not in ('joint','local'):raise ValueError('Declared joint or local scope required')
 if type(atol)not in (float,int)or not math.isfinite(atol)or not 0<atol<=ATOL:raise ValueError('Positive tolerance no larger than frozen1e-12 required')
 if not isinstance(C,torch.Tensor)or C.dtype!=D or C.shape!=(2,2)or not torch.isfinite(C).all()or abs(C.abs().square().sum().item()-1)>atol:raise ValueError('Normalized complex128reference required')
 failures=[];metrics={}
 if not isinstance(packet,dict)or set(packet)!={'full','S','R'}:return dict(accepted=False,scope=scope,failures=['schema'],metrics={})
 for name,d in (('full',4),('S',2),('R',2)):
  A=packet[name]
  if not isinstance(A,torch.Tensor)or A.dtype!=D or A.device.type!='cpu'or A.shape!=(d,d)or not torch.isfinite(A).all():failures.append(name+':representation');continue
  herm=(A-A.mH).abs().max().item();trace=abs(torch.trace(A).item()-1)
  metrics[name]={'hermitian_residual':herm,'trace_residual':trace}
  if herm>atol:failures.append(name+':Hermitian');continue
  if trace>atol:failures.append(name+':trace')
  low=torch.linalg.eigvalsh(A).min().item();metrics[name]['minimum_eigenvalue']=low
  if low < -atol:failures.append(name+':positive')
 if failures:return dict(accepted=False,scope=scope,failures=failures,metrics=metrics)
 def same(name,A,B):
  err=(A-B).abs().max().item();metrics[name]=err
  if err>atol:failures.append(name)
 full,S,R=(packet[n]for n in ('full','S','R'))
 same('S_from_full',S,t.trace_ab(full,2,2))
 swapped=full.reshape(2,2,2,2).permute(1,0,3,2).reshape(4,4)
 same('R_from_full',R,t.trace_ab(swapped,2,2))
 same('S_reference',S,C@C.mH)
 if scope=='joint':
  v=C.reshape(-1);same('full_reference',full,torch.outer(v,v.conj()))
  same('R_reference',R,C.T@C.conj())
 # Operational quadratics in an informationally complete qubit probe family.
 for j,v in enumerate(e.probes(2)):
  E=torch.outer(v,v.conj());same('effect'+str(j),torch.trace(S@E),torch.trace((C@C.mH)@E))
 return dict(accepted=not failures,scope=scope,failures=failures,metrics=metrics)

def errors(packet,C):
 variants={}
 def copy():return {k:v.clone()for k,v in packet.items()}
 a=copy();a['S'][0,0]=complex(float('nan'));variants['nonfinite']=a
 a=copy();a['S'][0,1]+=.01j;variants['nonHermitian']=a
 a=copy();a['S']*=2;variants['wrongtrace']=a
 a=copy();a['S']=torch.diag(torch.tensor([1.1,-.1],dtype=D));variants['negative']=a
 a=copy();a['S']=a['S'].conj();variants['wrongconjugate']=a
 a=copy();a['R']=a['S'].clone();variants['wrongselection']=a
 a=copy();a['full']=a['full'].real;variants['wrongdtype']=a
 outcomes={name:report(a,C)for name,a in variants.items()}
 assert all(not r['accepted']for r in outcomes.values())
 return outcomes

def main():
 for mode in ('statevector','density_matrix'):
  for p in (.27,.5,.81,1.):
   packet,C=prepare(p,.62,mode);assert report(packet,C)['accepted']
  packet,C=prepare(.27,.62,mode,W=e.Z)
  assert report(packet,C,'local')['accepted']
  assert not report(packet,C,'joint')['accepted']
 # Reuse last original reference via its exact coefficients;no new execution.
 v=C.reshape(-1);full=torch.outer(v,v.conj());original={'full':full,'S':C@C.mH,'R':C.T@C.conj()}
 failures=errors(original,C)
 for tol in (0.,1e-8,float('nan')):
  try:report(original,C,atol=tol)
  except ValueError:pass
  else:raise AssertionError('Invalid tolerance accepted')
 assert g.RUNS==10
 print('10 actual native circuits:8matched preparations and2ancillary-phase candidates passed scoped acceptance checks.')
 print('7 malformed/incorrect density packets rejected without clipping,symmetrization or normalization repair.')
 print('3 invalid tolerance contracts rejected;local acceptance never substitutes for joint acceptance.')
if __name__=='__main__':main()
