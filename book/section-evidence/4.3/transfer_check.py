from math import sqrt
import torch
import flagquantum as fq
from examples.foundations.tensor_spaces import prepare_matrix,OPTIONS
from examples.foundations.local_operators import embedding,rotation
c=fq.Circuit(2,dtype=torch.complex128)
for q,v in enumerate([(.6,.8j),(sqrt(3)/2,.5j)]):
 c.unitary(q,unitary=prepare_matrix(torch.tensor(v,dtype=torch.complex128)))
c.unitary(1,unitary=torch.tensor([[1,0],[0,1j]],dtype=torch.complex128))
r=fq.run(c,outputs=[fq.probabilities()],options=OPTIONS)
hand=torch.tensor([3*sqrt(3)/10,-.3,2j*sqrt(3)/5,-.4j],dtype=torch.complex128)
torch.testing.assert_close(r.statevector()[0],hand,rtol=0,atol=1e-12)
torch.testing.assert_close(r.probabilities[0],torch.tensor([.27,.09,.48,.16],dtype=torch.float64),rtol=0,atol=1e-12)
torch.testing.assert_close(embedding(rotation(),1,0),rotation(),rtol=0,atol=1e-12)
print('4.3-B: phase-only local gate matches all4amplitudes and probabilities;1actual circuit.')
print('Single-factor embedding boundary: E0(U)=U.')
