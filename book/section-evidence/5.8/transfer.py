"""Author transfer: new angles, mapped ordered supports and negative-pi control phase."""
from pathlib import Path
import sys,math
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
import torch
import examples.foundations.circuit_rewrites as w
program=(('h',(2,),()),('rz',(0,),(-.27,)),('cx',(2,0),()),
         ('rx',(1,),(.83,)),('rx',(1,),(-.83,)),('cx',(2,0),()),
         ('rz',(0,),(.27,)),('h',(2,),()))
reduced=w.cancellation(3,program)
assert reduced==()
for factors in w.inputs(3):
    for candidate in (program,reduced):
        v,_=w.run(w.compile_program(3,candidate),factors)
        torch.testing.assert_close(v,w.product_input(factors),rtol=0,atol=w.ATOL)
original=(('crx',(2,0),(-math.pi,)),)
replacement=(('p',(2,),(math.pi/2,)),('cx',(2,0),()))
reference=w.matrix(3,original)
torch.testing.assert_close(reference,w.matrix(3,replacement),rtol=0,atol=w.ATOL)
for factors in w.inputs(3):
    for candidate in (original,replacement):
        v,_=w.run(w.compile_program(3,candidate),factors)
        torch.testing.assert_close(v,reference @ w.product_input(factors),rtol=0,atol=w.ATOL)
assert w.RUNS==36
print('36 new-angle/support transfer circuits passed: nested cancellation and negative-pi control phase on reversed nonadjacent qubits.')
