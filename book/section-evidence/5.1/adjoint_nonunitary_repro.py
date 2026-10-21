"""Reproduce the released0.3.1 builder boundary; no simulator executions."""
from importlib.metadata import version
import flagquantum as fq
import torch
print('flagquantum',version('flagquantum'))
for name,M in [('projector',torch.diag(torch.tensor([1,0],dtype=torch.complex128))),('scaled-H',2*torch.tensor([[1,1],[1,-1]],dtype=torch.complex128)/2**.5)]:
    block=fq.Circuit(1,dtype=torch.complex128).unitary(0,unitary=M)
    inverse=block.adjoint()
    returned=inverse.to_ir().instructions[0].matrix
    assert torch.allclose(returned,M.mH,rtol=0,atol=1e-12)
    print(name,'accepted; returned adjoint times original is identity:',torch.allclose(returned@M,torch.eye(2,dtype=torch.complex128),rtol=0,atol=1e-12))
