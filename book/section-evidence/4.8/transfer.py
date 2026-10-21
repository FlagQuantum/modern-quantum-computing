import torch
from examples.foundations.convention_translation import pair,complex_gate,reversal,DTYPE,ATOL,decode_key
f,z,_=pair([(0,1),(1,0),(0,1),(0,1)],complex_gate(),(3,1))
assert torch.allclose(z,reversal(4)@f,rtol=0,atol=ATOL)
assert torch.allclose(z.abs().square(),reversal(4).real@f.abs().square(),rtol=0,atol=ATOL)
assert decode_key('10 0',(2,0,1),(2,1))=='100'
assert int('1011',2)==11 and sum(b*2**q for q,b in enumerate((1,0,1,1)))==13
print('New4qubit transfer:physical1011,indicesF11/Q13,support(3,1); all16amplitudes/probabilities match after conversion.')
print('Grouped-count transfer with changed measurement map:10 0 -> physical100.')
