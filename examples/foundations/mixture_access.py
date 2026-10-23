"""8.7: access contracts for equal local densities and unequal extensions."""
import math,torch
try:
 from examples.foundations import purification as g,statistical_ensembles as e,partial_trace as t
except ModuleNotFoundError:
 import purification as g,statistical_ensembles as e,partial_trace as t
D=e.D

def case(p,phi,alpha,mode='statevector'):
 if type(p)not in (int,float)or not math.isfinite(p)or not 0<=p<=1:raise ValueError('Probability in[0,1]required')
 Q=e.prepare(e.qubit(alpha,.43));C,rho=g.spectral((p,1-p),Q,2)
 phase=complex(math.cos(phi),math.sin(phi));C[:,1]*=phase
 result,_=g.execute(C,mode=mode)
 u0,u1=Q[:,0],Q[:,1];z=torch.tensor([1,0],dtype=D);o=torch.tensor([0,1],dtype=D)
 a=torch.kron(u0,z);b=torch.kron(u1,o)
 classical=p*torch.outer(a,a.conj())+(1-p)*torch.outer(b,b.conj())
 pure=result.measurement('full').value[0]
 e.close(t.trace_ab(classical,2,2),rho);e.close(result.measurement('S').value[0],rho)
 # Explicit system effects from several complex directions;the proof covers all effects.
 for th,ph in ((0.,0.),(.71,-.39),(1.28,.62)):
  v=e.qubit(th,ph);E=torch.outer(v,v.conj());P=torch.kron(E,e.I)
  e.close(torch.trace(pure@P),torch.trace(classical@P))
 # Joint coherence witness adapted to declared phase and system basis.
 witness=phase.conjugate()*torch.outer(a,b.conj())+phase*torch.outer(b,a.conj())
 # a,b orthogonal;witness eigenvalues +1,-1,0,0.
 e.close(torch.trace(pure@witness),2*math.sqrt(p*(1-p)))
 e.close(torch.trace(classical@witness),0)
 effect=(torch.eye(4,dtype=D)+witness)/2
 assert torch.linalg.eigvalsh(effect).min()>-1e-12
 e.close(torch.trace(pure@effect),.5+math.sqrt(p*(1-p)))
 e.close(torch.trace(classical@effect),.5)
 return result,rho,pure,classical,witness

def conditional(M,E):
 t.density(M);e.effect(E)
 joint= M.reshape(2,2,2,2)
 S=torch.einsum('imjn,nm->ij',joint,E)
 prob=torch.trace(S).real.item()
 if prob<=0:raise ValueError('Positive branch probability required')
 return prob,S/prob

def main():
 for mode in ('statevector','density_matrix'):
  for p in (.2,.5,.83,1.):
   for phi in (0.,.67,-.91):
    case(p,phi,.78,mode)
 print('24 native pure extensions:equal full local densities/effect probabilities;host classical extensions and joint coherence witness passed.')
 z=torch.diag(torch.tensor([1,0],dtype=D));o=e.I-z
 _,_,P,M,_=case(.5,0.,0.)
 plus=e.qubit(math.pi/2,0.);E=torch.outer(plus,plus.conj())
 for R in (P,M):
  a,A=conditional(R,z);b,B=conditional(R,o);e.close(a*A+b*B,e.I/2)
 a,A=conditional(P,E);b,B=conditional(M,E);e.close(a,.5);e.close(b,.5);e.close(A,E);e.close(B,e.I/2)
 try:case(-.1,0.,0.)
 except ValueError:pass
 else:raise AssertionError('Bad probability accepted')
 assert g.RUNS==25
 print('25 actual native circuits;classical mixtures/conditional states are explicit host calculations,no sampled collapse.')
if __name__=='__main__':main()
