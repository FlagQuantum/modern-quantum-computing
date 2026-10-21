import sys,cmath
from math import cos,sin
sys.path.insert(0,'.')
import torch
import flagquantum as fq
from examples.foundations import controlled_ancillas as ca
D=ca.DTYPE
U=cmath.exp(.31j)*ca.rx(-.52)
expected=torch.tensor([.6,.8j*cmath.exp(.31j)*cos(.26),0,-.8*cmath.exp(.31j)*sin(.26)],dtype=D)
generic=fq.Circuit(2,dtype=D).unitary(1,0,unitary=ca.controlled_matrix(U))
# Rz(-2chi) has relative phase exp(2i*chi), not a global phase gate.
# Use named Phase gate to construct exp(i*chi) I as P(chi) X P(chi) X.
source=fq.Circuit(1,dtype=D).rx(0,-.52).p(0,.31).x(0).p(0,.31).x(0)
native=source.control(1,ctrl_qubits=(1,))
for block in (generic,native):
 v,p=ca.run(block,[(1,0),(.6,.8j)])
 torch.testing.assert_close(v,expected,rtol=0,atol=ca.ATOL)
assert ca.RUNS==2
print('New chi=.31,theta=-.52 reversed-support phase transfer:2actual circuits; explicit trig reference agrees without phase alignment.')
