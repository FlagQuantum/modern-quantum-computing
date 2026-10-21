import torch
import flagquantum as fq
from examples.foundations.circuit_composition import DTYPE,ATOL,execute,rz,rx,S
v=torch.tensor([.6,.8j],dtype=DTYPE)
block=fq.Circuit(1,dtype=DTYPE).rz(0,.23).rx(0,-.61).s(0)
roundtrip=fq.Circuit(1,dtype=DTYPE).compose(block).compose(block.adjoint())
a,p=execute(roundtrip,[(.6,.8j)])
U=S@rx(-.61)@rz(.23);V=rz(-.23)@rx(.61)@S.mH
assert torch.allclose(V@U,torch.eye(2,dtype=DTYPE),rtol=0,atol=ATOL)
assert torch.allclose(a,v,rtol=0,atol=ATOL)
assert torch.allclose(p,v.abs().square(),rtol=0,atol=ATOL)
print('New rotation transfer: Rz(.23),Rx(-.61),S; inverse calls S-dagger,Rx(.61),Rz(-.23).')
print('One actual roundtrip circuit: both complex amplitudes/probabilities and independent inverse matrix checked.')
