import sys,math,cmath
sys.path.insert(0,'.')
import torch,flagquantum as fq
import examples.foundations.schmidt_decomposition as s
import examples.foundations.product_entanglement as e
for theta in (-.47,.83,1.71):
 for phi in (.37,-.92):
  for beta in (.28,-.56):
   gamma=.69
   circuit=fq.Circuit(4,dtype=s.D).ry(0,theta).cx(0,3).p(0,phi).ry(1,beta).ry(2,gamma)
   state,_=s.query(circuit)
   c,z=math.cos(theta/2),cmath.exp(1j*phi)*math.sin(theta/2)
   expected=[]
   for k in range(16):
    x=list(map(int,format(k,'04b')))
    pair=(c if x[0]==0 else z) if x[0]==x[3] else 0
    expected.append(pair*(math.cos(beta/2) if x[1]==0 else math.sin(beta/2))*(math.cos(gamma/2) if x[2]==0 else math.sin(gamma/2)))
   assert torch.allclose(state,torch.tensor(expected,dtype=s.D),atol=s.ATOL,rtol=0)
   for A,Bcut,target in (((3,0),(2,1),[1.,0,0,0]),((0,2),(3,1),sorted([abs(c),abs(z)],reverse=True)+[0,0])):
    C=e.coefficients(state,A,Bcut);U,values,B=s.decompose(C)
    assert torch.allclose(values,torch.tensor(target,dtype=torch.float64),atol=s.ATOL,rtol=0)
    assert torch.allclose(C,s.scalar_rebuild(U,values,B),atol=s.ATOL,rtol=0)
    assert abs(abs(s.overlap(C,U[:,0],B[:,0]))-values[0].item())<s.ATOL
for angle in (0.,.43,math.pi/4):
 A=s.phase(.79)@s.ry(-.63)
 B=torch.tensor([[cmath.exp(2j*math.pi*j*k/3)/math.sqrt(3) for k in range(2)] for j in range(3)],dtype=s.D)
 values=torch.tensor([math.cos(angle),math.sin(angle)],dtype=torch.float64)
 C=(A*values)@B.T
 U,actual,V=s.decompose(C)
 assert torch.allclose(actual,values,atol=s.ATOL,rtol=0)
 assert torch.allclose(C,s.scalar_rebuild(U,actual,V),atol=s.ATOL,rtol=0)
# Dimension-one boundary and finite complex global phase: zero extra circuits.
C=torch.tensor([[.6,.8j,0]],dtype=s.D)
U,values,B=s.decompose(C)
assert values.numel()==1 and abs(values[0].item()-1)<s.ATOL
_,phase_values,_=s.decompose(cmath.exp(.91j)*C)
assert torch.allclose(values,phase_values,atol=s.ATOL,rtol=0)
assert s.RUNS==12,s.RUNS
print('12 fresh four-qubit circuits: scalar amplitudes, two ordered-cut spectra and product overlap passed.')
print('3 rectangular 2x3 spectra plus singleton/global-phase classical boundaries passed; no extra circuits.')
