import cmath
from math import sqrt,pi
import torch
from examples.foundations.no_cloning import DTYPE,ATOL,execute,fidelity
v=torch.tensor([sqrt(.8),cmath.exp(1j*pi/3)*sqrt(.2)],dtype=DTYPE)
a,p=execute(v)
expected=torch.tensor([sqrt(.8),0,0,cmath.exp(1j*pi/3)*sqrt(.2)],dtype=DTYPE)
target=torch.tensor([.8,.4*cmath.exp(1j*pi/3),.4*cmath.exp(1j*pi/3),.2*cmath.exp(2j*pi/3)],dtype=DTYPE)
assert torch.allclose(a,expected,rtol=0,atol=ATOL)
assert torch.allclose(p,expected.abs().square(),rtol=0,atol=ATOL)
assert fidelity(a,target)<1-ATOL
print(f'New complex-state transfer: all4amplitudes/probabilities passed; squared overlap={fidelity(a,target):.9f}, below1.')
