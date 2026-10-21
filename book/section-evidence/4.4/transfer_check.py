import torch
from examples.foundations.ordered_supports import controlled_flip,execute
state,p=execute(controlled_flip(),4,(3,1),[(0,1),(1,0),(0,1),(0,1)])
expected=torch.zeros(16,dtype=torch.complex128);expected[15]=1
torch.testing.assert_close(state,expected,rtol=0,atol=1e-12)
torch.testing.assert_close(p,expected.abs().square(),rtol=0,atol=1e-12)
print('4.4-A: input1011, support(3,1), output1111; all16coordinates/probabilities checked;1actual circuit.')
