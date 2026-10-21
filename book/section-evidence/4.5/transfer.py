from examples.foundations.permutations_swap import run, DTYPE, ATOL
import torch
state,p=run((0,3,2,1),[(0,1),(0,1),(1,0),(1,0)])
expected=torch.zeros(16,dtype=DTYPE);expected[9]=1
assert torch.allclose(state,expected,rtol=0,atol=ATOL)
assert torch.allclose(p,expected.abs().square(),rtol=0,atol=ATOL)
print('Separate four-qubit transfer: SWAP(1,3),1100 ->1001,index9; all16amplitudes/probabilities passed.')
