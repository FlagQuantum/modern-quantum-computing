"""Separate new dense target and ordered-pair transfer; no expected circuit supplied."""
import sys
sys.path.insert(0,'.')
import torch
from examples.foundations import universal_gates as ug
U=ug.fixture(4,77)
ops=ug.compile_unitary(U)
ug.verify(ops,2,U)
local=ug.fixture(2,79);factors=ug.complex_factors(3)
v,p=ug.run(ug.two_level(local,2,7,3),3,factors)
expected=ug.embedded_two(local,2,7,3)@ug.product_input(factors)
torch.testing.assert_close(v,expected,rtol=0,atol=ug.ATOL)
assert ug.RUNS==6
print('New4x4target(seed77):4basis+complex;newordered pair(010,111),seed79:complex;6actual allowed-gate circuits passed.')
