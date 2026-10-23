from pathlib import Path
import itertools,json,math,cmath
import torch,flagquantum as fq
from examples.foundations import statistical_ensembles as e
rpop,phi=.61,-.72
basis=tuple(torch.eye(2,dtype=e.D))
nonorth=tuple(torch.tensor([math.sqrt(rpop),s*cmath.exp(1j*phi)*math.sqrt(1-rpop)],dtype=e.D) for s in (1,-1))
a,b=-.94,.33
U=torch.diag(torch.tensor([1,cmath.exp(1j*b)],dtype=e.D))@torch.tensor([[math.cos(a/2),-math.sin(a/2)],[math.sin(a/2),math.cos(a/2)]],dtype=e.D)
outputs=[]
for weights,vectors in (((rpop,1-rpop),basis),((.5,.5),nonorth)):
 matrices=[]
 for v in vectors:
  out=e.native(v,U=U,mode='density_matrix')
  matrices.append(out.density_matrix[0])
 R=sum(p*M for p,M in zip(weights,matrices))
 e.close(R,U@e.scalar_rho(weights,vectors)@U.mH)
 e.close(torch.trace(R@e.Z),(2*rpop-1)*math.cos(a))
 outputs.append(R)
e.close(outputs[0],outputs[1])
def scalar_W(v):
 # Ry(.47) on q1,then CX(q1,q0),then P(-.31) on q0.
 t=.47;phase=-.31;out=torch.zeros(4,dtype=e.D)
 for q0,q1 in itertools.product((0,1),repeat=2):
  mixed=math.cos(t/2)*v[2*q0+q1]+(-math.sin(t/2) if q1==0 else math.sin(t/2))*v[2*q0+(1-q1)]
  new0=q0 ^ q1
  out[2*new0+q1]=mixed*cmath.exp(1j*phase*new0)
 return out
families=[]
for bell in (False,True):
 matrices=[]
 for a,b in itertools.product((0,1),repeat=2):
  c=fq.Circuit(2,dtype=e.D)
  if a:c.x(0)
  if b:c.x(1)
  if bell:c.h(0).cx(0,1)
  c.ry(1,.47).cx(1,0).p(0,-.31)
  result=e.execute(c,[fq.density_matrix(name='full'),fq.density_matrix(qubits=(1,0),name='reverse')])
  v=torch.zeros(4,dtype=e.D)
  if bell:
   v[b]=1/math.sqrt(2);v[2+(1^b)]=(-1)**a/math.sqrt(2)
  else:v[2*a+b]=1.
  expected=scalar_W(v)
  e.close(result.measurement('full').value[0],e.outer(expected))
  perm=torch.tensor([0,2,1,3])
  e.close(result.measurement('reverse').value[0],e.outer(expected[perm]))
  matrices.append(result.measurement('full').value[0])
 families.append(sum(matrices)/4)
e.close(families[0],families[1])
e.close(families[0],torch.eye(4,dtype=e.D)/4)
assert e.RUNS==12
Path('book/section-evidence/8.1/transfer.json').write_text(json.dumps({'native_runs':12,'printed8.1B':{'r':rpop,'phi':phi,'theta_U':-.94,'phase_U':.33,'expected_Z':(2*rpop-1)*math.cos(-.94)},'printed8.1D':'W=Ry(.47)q1,CXq1q0,P(-.31)q0;all8transformed basis/Bell components;full/reversed outputs','reference':'scalar gate expansion,not native gate matrices','phase_alignment':False},indent=2)+'\n')
print('12fresh CPUcomplex128native circuits:4density-mode transformed nonorthogonal/spectral components;8mapped two-qubit components passed.')
print('Exact printed8.1B-D,scalar W amplitudes and full/reversed density outputs passed.')
