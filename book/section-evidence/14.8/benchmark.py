from pathlib import Path
import sys,time,json,statistics,platform,hashlib,importlib.metadata as md
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from examples.foundations import classical_baselines as b
root=Path(__file__).resolve().parents[3]
from fractions import Fraction as F
cases=tuple(tuple(F(j+1,2*j+3)for j in range(n))for n in (2,3,4))
rows=[];before=b.RUNS
for ps in cases:
 # One warmup per arm,then three measurements;ordering alternates and all times retained.
 b.check_bits(b.records(ps,43,seed=200),43);b.check_bits(b.native_records(ps,43,seed=200),43)
 times={'classical-product-sampler':[],'FlagQuantum-CPU-terminal':[]}
 for repetition in range(3):
  order=('classical-product-sampler','FlagQuantum-CPU-terminal')if repetition%2==0 else('FlagQuantum-CPU-terminal','classical-product-sampler')
  for name in order:
   start=time.perf_counter_ns()
   result=b.records(ps,43,seed=201+repetition)if name=='classical-product-sampler'else b.native_records(ps,43,seed=201+repetition)
   elapsed=time.perf_counter_ns()-start
   assert elapsed>=0;b.check_bits(result,43);times[name].append(elapsed)
 rows.append({'probabilities':[str(p)for p in ps],'n':len(ps),'shots':43,'times_ns':times,'median_ns':{k:statistics.median(v)for k,v in times.items()}})
assert b.RUNS-before==12
receipt={'date_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'purpose':'Dated CPU software-overhead illustration,not hardware or asymptotic advantage','output':'43 raw parity bits','timed_boundary':'input validation,product setup or circuit construction,execution/sampling,result tuple conversion;reference diagnostics outside timing','excluded':'hardware queue,physical loading/reset,network,QPU execution;none occurred','warmups_per_arm_per_case':1,'measured_repetitions_per_arm_per_case':3,'all_times_retained':True,'seeds':'200warmup;201..203measured,paired deterministic validation not independent statistical evidence','native_calls':12,'classical_calls':12,'environment':{'python':platform.python_version(),'flagquantum':md.version('flagquantum'),'torch':md.version('torch'),'platform':platform.platform(),'machine':platform.machine(),'device':'CPU','clock':str(time.get_clock_info('perf_counter'))},'implementation_sha256':hashlib.sha256((root/'examples/foundations/classical_baselines.py').read_bytes()).hexdigest(),'cases':rows,'interpretation':'No threshold requires a speed ratio above1;three repetitions do not certify a runtime distribution or the best classical baseline. Ideal target marginal checked separately within numerical tolerance,not an interval/hardware-error certificate.'}
print(json.dumps(receipt,indent=2))
