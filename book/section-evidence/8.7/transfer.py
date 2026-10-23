from examples.foundations import mixture_access as m,statistical_ensembles as e,purification as g
import torch,math
for mode in ('statevector','density_matrix'):
 for phi in (-.84,.49):
  _,rho,P,M,W=m.case(.37,phi,-.62,mode)
  plus=e.qubit(math.pi/2,0.);minus=e.qubit(-math.pi/2,0.)
  for R in (P,M):
   p,A=m.conditional(R,torch.outer(plus,plus.conj()));q,B=m.conditional(R,torch.outer(minus,minus.conj()));e.close(p,.5);e.close(q,.5);e.close(p*A+q*B,rho)
assert g.RUNS==4
print('4fresh native transfers;printed biased/complex branch and unread reconstruction checks passed.')
