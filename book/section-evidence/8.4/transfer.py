"""Fresh8.4B-D and new retained triples;author tests,not independent review."""
import sys,json,math
from pathlib import Path
import torch,flagquantum as fq
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from examples.foundations import partial_trace as t
from examples.foundations import statistical_ensembles as e
from examples.foundations import density_updates as d
keeps=((3,1),(1,3),(0,),(1,),(2,),(3,))
for mode in ('statevector','density_matrix'):
 pair=[]
 for kind,theta,phi in (('chain',-.67,.39),('product',1.08,-.53)):
  result,v=t.native(4,theta,phi,kind=kind,mode=mode,keeps=keeps);pair.append(result)
  full=result.measurement('full').value[0];R=result.measurement('r_3_1').value[0]
  # Explicit printed bit lift,independent of helper lift.
  lift=lambda i,mu:8*(mu//2)+4*(i%2)+2*(mu%2)+i//2
  explicit=torch.tensor([[sum(full[lift(i,mu),lift(j,mu)].item()for mu in range(4))for j in range(4)]for i in range(4)],dtype=t.D)
  e.close(R,explicit)
 full=sum(w*r.measurement('full').value[0]for w,r in zip((.29,.71),pair))
 for S in keeps:
  mixture=sum(w*r.measurement(t.key(S)).value[0]for w,r in zip((.29,.71),pair))
  e.close(mixture,t.indexed(full,4,S));e.close(mixture,t.axes(full,4,S));e.close(mixture,t.reconstruct(full,4,S));t.density(mixture)
# PrintedC:actual rotation on discarded q1,not helper's rotate_last.
U=e.prepare(e.qubit(-.47,.62));V=t.embed(U,3,(1,))
for mode in ('statevector','density_matrix'):
 before,v=t.native(3,.64,-.82,mode=mode,keeps=((2,0),(1,)))
 c,_=t.preparation(3,.64,-.82);c.unitary(1,unitary=U)
 after=t.run(c,[fq.density_matrix(name='full'),fq.density_matrix(qubits=(2,0),name='retained')],mode)
 full=before.measurement('full').value[0];changed=after.measurement('full').value[0]
 e.close(changed,V@full@V.mH)
 e.close(after.measurement('retained').value[0],before.measurement('r_2_0').value[0])
 e.close(t.indexed(V.mH@full@V,3,(2,0)),t.indexed(full,3,(2,0)))
for mode in ('statevector','density_matrix'):
 for phi in (-.51,math.pi/2):
  result,v=t.native(2,1.07,phi,kind='bell',mode=mode)
  full=result.measurement('full').value[0];prior=result.measurement('r_0').value[0]
  probs,states,sigmas,ignored=d.instrument(full,((torch.kron(e.I,d.P0),),(torch.kron(e.I,d.P1),)))
  e.close(t.indexed(ignored,2,(0,)),prior)
  e.close(t.indexed(states[0],2,(0,)),d.P0);e.close(t.indexed(states[1],2,(0,)),d.P1)
  assert not torch.allclose(full,ignored,atol=t.ATOL,rtol=0)
  e.close(torch.trace(ignored@torch.kron(e.X,e.Y)),0)
# Two fresh retained-triple cases beyond the printed pair selections.
for mode in ('statevector','density_matrix'):
 result,v=t.native(4,.42,-1.03,mode=mode,keeps=((3,0,2),(2,0,3)))
 full=result.measurement('full').value[0]
 e.close(t.indexed(t.indexed(full,4,(3,0,2)),3,(0,2)),t.indexed(full,4,(3,2)))
# PrintedD:complex positive3x2global matrix,host-only.
u=torch.tensor([1,1j,0,0,0,0],dtype=t.D)/math.sqrt(2)
v=torch.tensor([0,0,1,0,0,1j],dtype=t.D)/math.sqrt(2)
M=.4*torch.outer(u,u.conj())+.6*torch.outer(v,v.conj());t.density(M)
R=t.trace_ab(M,3,2);e.close(R,torch.diag(torch.tensor([.4,.3,.3],dtype=t.D)))
e.close(R,torch.einsum('imjm->ij',M.reshape(3,2,3,2)))
for i in range(3):
 E=torch.zeros((3,3),dtype=t.D);E[i,i]=1
 e.close(torch.trace(R@E),torch.trace(M@torch.kron(E,e.I)))
 for j in range(i+1,3):
  for phase in (1.,-1j):
   A=torch.zeros_like(E);A[i,j]=phase;A[j,i]=complex(phase).conjugate()
   e.close(torch.trace(R@A),torch.trace(M@torch.kron(A,e.I)))
e.close(t.trace_ab(.23*M,3,2),.23*R)
e.close(t.trace_ab(M,1,6),torch.ones((1,1),dtype=t.D));e.close(t.trace_ab(M,6,1),M)
assert t.RUNS==14
print(json.dumps(dict(native_circuits=t.RUNS,printed_exercises=['8.4B','8.4C','8.4D'],extra_retained_triples=[[3,0,2],[2,0,3]],classical_3_by_2_diagonal=[.4,.3,.3],status='passed'),indent=2))
