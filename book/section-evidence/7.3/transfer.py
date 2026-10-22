import math,cmath,sys
sys.path.insert(0,'.')
import torch,flagquantum as fq
import examples.foundations.bell_basis as t
for pair in ((3,0),(0,3),(2,1)):
 for theta,phi in ((.83,-.92),(1.21,.37)):
  left,right=pair
  c=fq.Circuit(4,dtype=t.D).ry(left,theta).cx(left,right).p(left,phi)
  factors={}
  for q,(eta,lam) in zip([q for q in range(4) if q not in pair],((.37,.21),(-.69,.43))):
   c.ry(q,eta).p(q,lam);factors[q]=(math.cos(eta/2),cmath.exp(1j*lam)*math.sin(eta/2))
  def scalar(pair_amplitudes):
   values=[]
   for k in range(16):
    bits=list(map(int,format(k,'04b')))
    amp=pair_amplitudes[2*bits[left]+bits[right]]
    for q,factor in factors.items():amp*=factor[bits[q]]
    values.append(amp)
   return torch.tensor(values,dtype=t.D)
  a,b=math.cos(theta/2),cmath.exp(1j*phi)*math.sin(theta/2)
  prepared=t.query(c,pair)
  assert torch.allclose(prepared['state'],scalar([a,0,0,b]),atol=t.ATOL,rtol=0)
  analyzed=t.query(t.decode(c,pair),pair,shots=53,seed=43)
  coeff=[(a+b)/math.sqrt(2),0,(a-b)/math.sqrt(2),0]
  assert torch.allclose(analyzed['state'],scalar(coeff),atol=t.ATOL,rtol=0)
  probabilities=torch.tensor([abs(z)**2 for z in coeff],dtype=torch.float64)
  assert torch.allclose(analyzed['probabilities'],probabilities,atol=t.ATOL,rtol=0)
  assert analyzed['counts'].tolist()==[analyzed['bits'].tolist().count([j//2,j%2]) for j in range(4)]
  # Reversing only output columns permutes labels01 and10,not physical amplitudes.
  swapped=torch.zeros(4,dtype=torch.float64)
  for k,z in enumerate(analyzed['state'].tolist()):
   bits=list(map(int,format(k,'04b')));swapped[2*bits[right]+bits[left]]+=abs(z)**2
  assert torch.allclose(swapped,probabilities[torch.tensor([0,2,1,3])],atol=t.ATOL,rtol=0)
# An actual wrong chronological analyzer:encoder repeated instead of itsinverse.
wrong=t.query(t.preparation(0,1).h(0).cx(0,1),shots=17)
expected=torch.tensor([0,1,0,0],dtype=torch.float64)
assert not torch.allclose(wrong['probabilities'],expected,atol=t.ATOL,rtol=0)
assert torch.allclose(wrong['probabilities'],torch.full((4,),.25,dtype=torch.float64),atol=t.ATOL,rtol=0)
assert t.RUNS==13,t.RUNS
print('12 fresh four-qubit queries:complex scalar amplitudes,ordered Bell probabilities and53-shot accounting passed.')
print('Printed exercise7.3-C parameters included;reversing only output columns permutes01/10 as predicted.')
print('1 deliberate wrong-order analyzer:uniform probabilities rejected against deterministicPsi+ label01.')
