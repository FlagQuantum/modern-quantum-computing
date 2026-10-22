import sys,json
sys.path.insert(0,'/Users/baai/Documents/liuwei/modern-quantum-computing')
from examples.foundations import measurement_lab as lab
from math import sin
lab.RUNS=0
reports=[]
for theta,phi in [(-.43,1.19),(1.27,-2.33),(2.48,.37)]:
 for variant in ('correct','outcome-phase','wrong-y'):
  packet=lab.acquire(theta,phi,variant,seed=73)
  report=lab.audit(packet)
  assert report['accepted']==(variant!='wrong-y')
  if variant=='wrong-y':assert not report['checks']['measurement_effects'] and not report['checks']['probability_model']
  else:
   branch=lab.branch_report(packet['initial'])
   assert abs(report['exact_correlation']-sin(theta)*sin(phi))<1e-12
  reports.append(dict(theta=theta,phi=phi,variant=variant,report=report))
assert lab.RUNS==18
print('18 fresh native circuits:three new signed-angle/complex-phase cases x three analyzer variants; correct/effect-equivalent pass,wrong-Y rejects.')
print('Signed conditional phases and ignored-outcome ensemble predictions checked classically; no new skill,hardware or independent-review claim.')
open('/private/tmp/mqc69/transfer-reports.json','w').write(json.dumps(reports,indent=2)+'\n')
