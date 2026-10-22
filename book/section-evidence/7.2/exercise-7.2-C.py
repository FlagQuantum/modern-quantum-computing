import sys,math,cmath
sys.path.insert(0,'.')
import torch,flagquantum as fq
import examples.foundations.schmidt_decomposition as s
import examples.foundations.product_entanglement as e
theta,phi,beta,gamma=-.61,.92,.37,-.83
state,_=s.query(fq.Circuit(4,dtype=s.D).ry(0,theta).cx(0,3).p(0,phi).ry(1,beta).ry(2,gamma))
expected=[]
for k in range(16):
 x=list(map(int,format(k,'04b')))
 pair=(math.cos(theta/2) if x[0]==0 else cmath.exp(1j*phi)*math.sin(theta/2)) if x[0]==x[3] else 0
 expected.append(pair*(math.cos(beta/2) if x[1]==0 else math.sin(beta/2))*(math.cos(gamma/2) if x[2]==0 else math.sin(gamma/2)))
assert torch.allclose(state,torch.tensor(expected,dtype=s.D),atol=s.ATOL,rtol=0)
for A,Bcut,target in (((3,0),(2,1),[1,0,0,0]),((0,2),(3,1),[math.cos(.61/2),math.sin(.61/2),0,0])):
 C=e.coefficients(state,A,Bcut);U,values,B=s.decompose(C)
 assert torch.allclose(values,torch.tensor(target,dtype=torch.float64),atol=s.ATOL,rtol=0)
 assert torch.allclose(C,s.scalar_rebuild(U,values,B),atol=s.ATOL,rtol=0)
assert s.RUNS==1
print('Exercise7.2-C exact printed angles:1 additional native circuit;all16 scalar amplitudes and both4x4 spectra passed.')
print('This supplements the12 fresh transfer circuits;it does not re-execute or replace that evidence.')
