"""Fresh14.9quality/input audits; twelve actual native calls."""
from pathlib import Path
import sys,json,copy,itertools
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from examples.foundations import resource_audit as r
F=r.F
cases=[(F(2,9),F(3,7)),(F(2,9),F(3,7),F(4,11),F(5,13))]
ledgers=[]
for ps in cases:
 plan=r.Plan(ps,epsilon=F(1,6),beta=F(1,32),delta=F(1,8));assert plan.shots==110 and plan.bits=={2:5,4:6}[len(ps)]
 assert r.b.exact_mean(ps)==r.b.enumerate_law(ps)
 assert abs(r.b.exact_mean(ps)-r.b.exact_mean(plan.quantized))<=plan.bound<=plan.beta
 assert r.a.target_coverage(r.b.exact_mean(ps),r.b.exact_mean(plan.quantized),110,plan.epsilon)>=1-plan.delta
 for mode in ('statevector','density_matrix'):
  for reverse in (False,True):
   p=r.execute(plan,mode,reverse,seed=709);assert r.audit(plan,p)['accepted']
   bad=copy.deepcopy(p);bad['identity']='stale';r.rejection(plan,bad,'stale')
   bad=copy.deepcopy(p);bad['gates']=len(ps);r.rejection(plan,bad,'underreported recipe')
 L=r.resources(plan);ledgers.append(L)
 assert tuple(L[k]for k in ('total_preparations','total_gates','total_serial_gate_layers','record_bits'))==({2:(130,500,380,390),4:(190,1360,910,950)}[len(ps)])
plan=r.Plan(cases[0],epsilon=F(1,6),beta=F(1,32),delta=F(1,8))
for bits in itertools.product((0,1),repeat=2):assert r.audit(plan,r.execute(plan,basis=bits,seed=709))['accepted']
assert r.RUNS==12
print('12 fresh native calls passed: two new rational inputs,new quality,both modes/commuting orders and four basis calibrations.')
print('b=5/6,S=110; complete logical ledgers=(130,500,380,390)/(190,1360,910,950) for preparations,gates,layers,record bits; stale/underreported packets rejected.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(dict(packets=r.PACKETS,receipts=r.RECEIPTS,ledgers=ledgers),indent=2)+'\n')
