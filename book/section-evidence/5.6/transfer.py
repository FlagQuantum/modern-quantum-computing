"""New parameters and support placements; author transfer, not independent review."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from itertools import product
import torch
import flagquantum as fq
import examples.foundations.gate_decompositions as g
for axis in ('y','z'):
    for factors in [g.basis_factors(b) for b in product((0,1),repeat=3)]+[g.complex_factors(3)]:
        actual,_=g.run(g.controlled_rotation(axis,.91,c=2,t=0,n=3),factors)
        expected=g.controlled_reference(g.product_input(factors),g.explicit(axis,.91),3,2,0)
        torch.testing.assert_close(actual,expected,rtol=0,atol=g.ATOL)
factors=g.complex_factors(5)
actual,_=g.run(fq.Circuit(5,dtype=g.D).compose(g.ancilla('dirty'),qubits=(4,2,0,3,1)),factors)
initial=g.product_input(factors);expected=torch.zeros_like(initial)
for j,z in enumerate(initial):
    toggle=((j>>0)&1)&((j>>2)&1)&((j>>4)&1)
    expected[j^(8 if toggle else 0)]+=z
torch.testing.assert_close(actual,expected,rtol=0,atol=g.ATOL)
assert g.RUNS==19
print('19 new-parameter/support transfer circuits passed: 18 reversed nonadjacent controlled rotations and 1 mapped borrowed-ancilla complex input.')
