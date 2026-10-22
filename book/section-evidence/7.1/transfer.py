import sys,math,cmath
sys.path.insert(0,'.')
import torch,flagquantum as fq
import examples.foundations.product_entanglement as e
for theta in (-.61,.9,1.3):
 for phi in (.92,-.41):
  for beta in (.37,-.28):
   gamma=-.83
   circuit=fq.Circuit(4,dtype=e.D).ry(0,theta).cx(0,3).p(0,phi).ry(1,beta).ry(2,gamma)
   state,_=e.query(circuit)
   c,s=math.cos(theta/2),cmath.exp(1j*phi)*math.sin(theta/2)
   a=torch.tensor([c,0,0,s],dtype=e.D)
   b=torch.tensor([math.cos(gamma/2)*math.cos(beta/2),math.cos(gamma/2)*math.sin(beta/2),math.sin(gamma/2)*math.cos(beta/2),math.sin(gamma/2)*math.sin(beta/2)],dtype=e.D)
   C=e.coefficients(state,(3,0),(2,1))
   assert torch.allclose(C,torch.outer(a,b),atol=e.ATOL,rtol=0)
   assert e.pivot_factors(C)[2]<e.ATOL
   split=e.coefficients(state,(0,2),(3,1))
   assert max(abs(m) for m in e.minors(split))>.01
   # Independent bit-index amplitudes, including reversed internal labels.
   expected=[]
   for k in range(16):
    x=list(map(int,format(k,'04b')))
    pair=(c if x[0]==0 else s) if x[0]==x[3] else 0
    expected.append(pair*(math.cos(beta/2) if x[1]==0 else math.sin(beta/2))*(math.cos(gamma/2) if x[2]==0 else math.sin(gamma/2)))
   assert torch.allclose(state,torch.tensor(expected,dtype=e.D),atol=e.ATOL,rtol=0)
for a,b in (([0,1],[.6,.8j,0]),([1j,0],[0,1,0]),([.6,.8j],[1/math.sqrt(2),0,1j/math.sqrt(2)])):
 C=torch.outer(torch.tensor(a,dtype=e.D),torch.tensor(b,dtype=e.D))
 assert max(abs(m) for m in e.minors(C))<e.ATOL
 assert e.pivot_factors(C)[2]<e.ATOL
print('12 fresh four-qubit native circuits: scalar amplitudes, ordered products and entangled recuts passed.')
print('3 rectangular 2x3 classical products: zero columns and complex pivot boundaries passed; no extra quantum calls.')
assert e.RUNS==12
