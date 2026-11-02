from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from examples.foundations import resource_audit as r
F=r.F
end=r.Plan((F(0),F(1),F(1,2)));assert end.quantized==end.ps and r.b.exact_mean(end.ps)==F(1,2)
tie=r.Plan((F(1,128),F(3,128)));assert tie.bits==6 and tie.quantized==(F(0),F(1,32))
assert abs(r.b.exact_mean(tie.ps)-r.b.exact_mean(tie.quantized))<=sum(abs(x-y)for x,y in zip(tie.ps,tie.quantized))==F(1,64)
assert r.a.mean_budget(F(1,16),F(1,10),F(1,128))==836
try:r.Plan((F(1,4),F(1,3),F(2,5)),epsilon=F(1,16),beta=F(1,128))
except ValueError as error:assert '501'in str(error)
else:raise AssertionError('Finite reference guard not enforced')
assert r.RUNS==0
print('Zero native calls: deterministic endpoints, exact ties-to-even (1/128,3/128)->(0,1/32), sharp grid bias sum and836shot reference guard passed.')
