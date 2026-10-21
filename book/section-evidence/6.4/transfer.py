"""Fresh 6.4 author transfers: nine tilted inputs and five four-qubit cases."""
from math import cos,sin,pi
import torch
import flagquantum as fq
from examples.foundations import basis_measurement as a
b=a.b;start=b.RUNS
for theta,phi in ((-.52,.38),(1.13,-.69),(.27,1.21)):
 c,s=cos(theta/2),sin(theta/2);e0=complex(cos(phi/2),-sin(phi/2));e1=e0.conjugate()
 B=torch.tensor([[c*e0,-s*e0],[s*e1,c*e1]],dtype=b.D)
 for initial in (torch.tensor([.6,.8j],dtype=b.D),B[:,0],B[:,1]):
  after,p=b.run(fq.Circuit(1,dtype=b.D).rz(0,-phi).ry(0,-theta),[tuple(initial.tolist())])
  a.full_check(initial,B,('plus','minus'),after,p)
print('9 tilted-basis transfers: three new angle pairs, complex input and both explicit basis columns passed.')
pre=(('ry',(1,),(.32,)),('cx',(3,0),()),('p',(0,),(-.28,)))
read=(('p',(3,),(-pi/2,)),('h',(3,),()),('h',(1,),()))
R=a.matrix(4,read);Q,labels=b.marginal_family(4,(3,1));P=tuple(R.mH@q@R for q in Q)
cases=[b.basis_factors(bits) for bits in ((0,0,0,0),(1,0,1,1),(0,1,1,0),(1,1,0,1))]+[b.complex_factors(4)]
for factors in cases:
 initial=a.matrix(4,pre)@b.product_input(factors)
 block=fq.Circuit(4,dtype=b.D).ry(1,.32).cx(3,0).p(0,-.28).p(3,-pi/2).h(3).h(1)
 after,p=b.run(block,factors,(3,1))
 torch.testing.assert_close(after,R@initial,rtol=0,atol=b.ATOL)
 torch.testing.assert_close(p,b.born(initial,P,labels),rtol=0,atol=b.ATOL)
 sums=torch.zeros(4,dtype=torch.float64)
 for j,z in enumerate(R@initial):
  bits=format(j,'04b');sums[int(bits[3]+bits[1],2)]+=abs(z)**2
 torch.testing.assert_close(p,sums,rtol=0,atol=b.ATOL)
assert b.RUNS-start==14
print('5 four-qubit transfers: four declared basis inputs and one complex product, indexed preparation and (q3,q1) Y/X readout passed.')
print('14 actual CPU complex128 circuits; author transfer, not independent review, hardware measurement or reader trial.')
