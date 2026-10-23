"""Fresh transfer including the exact printed7.5C exercise."""
import cmath,itertools,math
import torch
from examples.foundations import teleportation as t
D=t.D
v=torch.tensor([math.sqrt(.3),cmath.exp(-.61j)*math.sqrt(.7)],dtype=D)
for stage in ('decoded','coherent'): t.query(v,stage,n=4,roles=(3,0,2))
q=t.query(v)
for bits in itertools.product((0,1),repeat=2):
    p,w=t.extract(q['state'],(0,1),bits,(2,))
    final,_=t.bob_reprepare(w,bits)
    assert abs(p-.25)<t.ATOL and torch.allclose(final,v,atol=t.ATOL,rtol=0)
print('Exact printed7.5C:mapped decoder/coherent,spectator factors and four branch corrections passed;7 native runs.')
for phase,roles in ((-.92,(2,3,0)),(.27,(1,3,2)),(1.13,(0,2,3))):
    v=torch.tensor([math.sqrt(.41),cmath.exp(phase*1j)*math.sqrt(.59)],dtype=D)
    for stage in ('decoded','coherent'):t.query(v,stage,n=4,roles=roles,columns=(roles[1],roles[0]))
for stage in ('decoded','coherent'):t.reference_pair(1.03,-.81,stage)
t.calibrate(4,(2,0,3),(1,0))
assert t.RUNS==16
print('Fresh phase/role/reversed-column and reference-pair cases passed;16 total native transfer runs.')
