from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from examples.foundations import measurement_execution as m
F=m.F
for Q in((4,2,0),(0,3),(2,1,4,0)):
 for mode in('statevector','density_matrix'):
  for analyzer in(False,True):m.native(5,Q,(-.83,.41,.67,-.49),mode,analyzer,shots=23,seed=907)
assert m.RUNS==12
assert m.exact_sampler_check(tuple(F(j,36)for j in range(1,9)))==36
assert m.exact_sampler_check(tuple(F(j,4)for j in(0,1,0,2,0,0,1,0)))==4
rare=m.Sampler((F(1)-F(1,10**20),F(1,10**20)))
assert rare.at(rare.D-1)==1 and rare.at(rare.D-2)==0
try:m.exact_sampler_check((F(1)-F(1,10**20),F(1,10**20)))
except ValueError:pass
else:raise AssertionError('Huge exhaustive-rank sweep accepted')
print('12 fresh five-qubit native calls passed: three ordered masks,both modes and computational/Y-X analyzer profiles; all prefix references checked.')
print('Two fresh rational laws passed all40 ranks; rare exact last-rank event retained,huge exhaustive sweep rejected; no frequency-hit requirement.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(m.RECEIPTS,indent=2)+'\n')
