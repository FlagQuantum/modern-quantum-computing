from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from examples.foundations import classical_baselines as b
from fractions import Fraction as F
cases=((F(2,7),F(3,8),F(4,11)),(F(1,5),F(2,9),F(3,10),F(4,13)),(F(1,6),F(2,7),F(3,11),F(4,15),F(5,17)),(F(1),F(0)),(F(0),F(1),F(0)))
for ps in cases:
 q=b.exact_mean(ps);assert q==b.enumerate_law(ps)
 for mode in ('statevector','density_matrix'):
  raw,ref=b.validate_native(ps,37,seed=109,mode=mode);assert ref==q;b.check_bits(raw,37)
 for method in ('coins','product'):b.check_bits(b.records(ps,37,seed=109,method=method),37)
task=b.Contract(cases);assert b.fulfills(__import__('dataclasses').replace(task,epsilon=F(0),delta=F(0)),task)
assert b.RUNS==10 and b.invalid_checks()==20
print(json.dumps({'native_runs':10,'rational_lists':[[str(p)for p in ps]for ps in cases],'modes':['statevector','density_matrix'],'shots':37,'exact_product_and_enumeration':'passed','classical_sampler_records':'passed','malformed_comparison_cases':20},indent=2))
