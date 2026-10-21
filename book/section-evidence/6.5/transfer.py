"""Fresh 6.5 transfer: twelve weak dilations and two trine preparations."""
from math import cos,sin
import cmath,torch
import flagquantum as fq
from examples.foundations import generalized_measurements as g
b=g.b;start=b.RUNS
pairs=((- .4,.8),(1.03,-.27),(2.2,1.1))
for kappa in (.17,.73):
 for theta,phi in pairs:
  state=torch.tensor([cos(theta/2),cmath.exp(1j*phi)*sin(theta/2)],dtype=b.D)
  predictions=[]
  for flip in (False,True):
   joint,p=g.native_weak(state,kappa,flip)
   alpha,beta=state.tolist()
   u,v=((1+kappa)/2)**.5,((1-kappa)/2)**.5
   expected=torch.tensor([u*alpha,v*alpha,v*beta,u*beta],dtype=b.D)
   if flip:expected=expected[[0,3,2,1]]
   torch.testing.assert_close(joint,expected,rtol=0,atol=b.ATOL)
   formula=torch.tensor([(1+kappa*(abs(alpha)**2-abs(beta)**2))/2,
                         (1-kappa*(abs(alpha)**2-abs(beta)**2))/2],dtype=torch.float64)
   torch.testing.assert_close(p,formula,rtol=0,atol=b.ATOL)
   predictions.append(p)
  torch.testing.assert_close(*predictions,rtol=0,atol=b.ATOL)
print('12 fresh weak-instrument transfers passed: two strengths, three complex inputs, both updates, explicit scalar joint amplitudes and equal meter probabilities.')
ts,groups,effects=g.trine()
for theta,phi in ((.83,-.41),(-.66,.92)):
 state,p_native=b.run(fq.Circuit(1,dtype=b.D).ry(0,theta).p(0,phi),[(1,0)])
 alpha,beta=cos(theta/2),cmath.exp(1j*phi)*sin(theta/2)
 torch.testing.assert_close(state,torch.tensor([alpha,beta],dtype=b.D),rtol=0,atol=b.ATOL)
 p,rows=g.instrument(state,groups,('t0','t1','t2'))
 scalar=torch.tensor([abs(alpha+cmath.exp(-2j*cmath.pi*j/3)*beta)**2/3 for j in range(3)],dtype=torch.float64)
 torch.testing.assert_close(p,scalar,rtol=0,atol=b.ATOL)
 torch.testing.assert_close(p,g.povm(state,effects,('t0','t1','t2')),rtol=0,atol=b.ATOL)
assert b.RUNS-start==14
print('2 new native trine-input preparations passed against closed amplitudes, scalar probabilities and effect/operator consistency.')
print('14 actual CPU complex128 circuits; author transfer, not independent review, reader trial or general native instrument execution.')
