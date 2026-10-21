"""Separate author transfer: a new three-input majority oracle."""
import sys
from itertools import product
sys.path.insert(0,'.')
import torch
import flagquantum as fq
from examples.foundations import reversible_logic as rl
D=rl.DTYPE
# Derive the table from an independent threshold definition, not the gate formula.
table=[int(a+b+c>=2) for a,b,c in product((0,1),repeat=3)]
assert table==[0,0,0,1,0,1,1,1]
native=fq.Circuit(4,dtype=D).ccx(0,1,3).ccx(0,2,3).ccx(1,2,3)
for factors in [rl.basis_factors(bits) for bits in product((0,1),repeat=4)]+[rl.complex_factors(4)]:
    v,p=rl.run(native,factors)
    expected=rl.oracle_reference(rl.product_input(factors),table,3,1)
    torch.testing.assert_close(v,expected,rtol=0,atol=rl.ATOL)
dense=fq.Circuit(4,dtype=D).unitary(0,1,2,3,unitary=rl.oracle_matrix(table,3,1))
factors=rl.complex_factors(4)
v,p=rl.run(dense,factors)
torch.testing.assert_close(v,rl.oracle_reference(rl.product_input(factors),table,3,1),rtol=0,atol=rl.ATOL)
assert rl.RUNS==18
print('New majority threshold table:16basis and1complex native circuits,1dense complex circuit;18actual runs passed.')
