import json,copy,cmath,math
from pathlib import Path
O=Path('/private/tmp/mqc-composition-blind-r1/a/outputs')
tasks=json.loads((O.parent/'tasks.json').read_text())
q1=json.loads((O/'A1/source-experiment.json').read_text())
def save(p,x):
 (O/p).write_text(json.dumps(x,indent=2)+'\n')
# Independent standard-library matrix-power Taylor reference: no imports from helpers or FlagQuantum.
def dec(a):
 if isinstance(a,list) and len(a)==2 and all(type(x) in (int,float) for x in a):return complex(*a)
 return [dec(x) for x in a]
def enc(a):
 if isinstance(a,list):return [enc(x) for x in a]
 return [a.real,a.imag]
def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def mv(a,v):return [sum(a[i][j]*v[j] for j in range(2)) for i in range(2)]
def err(a,b):return max(abs(x-y) for x,y in zip(a,b))
def expm(a):
 total=[[1+0j,0j],[0j,1+0j]];term=copy.deepcopy(total)
 for n in range(1,65):
  term=[[z/n for z in row] for row in mm(term,a)]
  total=[[total[i][j]+term[i][j] for j in range(2)] for i in range(2)]
 return total
references={}
for tid,q in [('A1',q1),('A2',tasks[1]['experiment'])]:
 factor=q['time']['value']*1e-9/q['hbar']['value'];g=dec(q['generator']['matrix']);u=expm([[-1j*z*factor for z in row] for row in g]);s=mv(u,dec(q['initial_state']));references[tid]=(u,s)
 report=json.loads((O/tid/'fresh-workflow/report.json').read_text());cont=json.loads((O/tid/'fresh-workflow/continuous-circuit.json').read_text());ev=json.loads((O/tid/'fresh-workflow/02-evolution/stdout.json').read_text())
 checks=[]
 for record in cont['records']:
  phase=record['phase_radians'];b=cmath.exp(1j*(phase-q['analyzer']['delta']))*s[1];out=[(s[0]+b)/math.sqrt(2),(s[0]-b)/math.sqrt(2)];actual=dec(record['statevector']);staged=dec(record['staged_statevector']);probs=[abs(z)**2 for z in out]
  checks.append({'phase':phase,'coordinate_error':err(actual,out),'staged_error':err(staged,out),'whole_vs_staged':err(actual,staged),'probability_error':max(abs(x-y) for x,y in zip(probs,record['probabilities']))})
 matrix_error=max(abs(x-y) for a,b in zip(u,dec(ev['unitary'])) for x,y in zip(a,b));epsilon=q['tolerance']['coordinate_atol'];passed=matrix_error<=epsilon and all(max(c[k] for k in ('coordinate_error','staged_error','whole_vs_staged','probability_error'))<=epsilon for c in checks)
 save(tid+'/independent-verification.json',{'method':'64-term matrix Taylor series, scalar list matvec, direct analyzer amplitudes; classical arithmetic, not a circuit','exponent_multiplier':factor,'time_seconds':q['time']['value']*1e-9,'reference_unitary':enc(u),'reference_evolved_state':enc(s),'matrix_error':matrix_error,'checks':checks,'atol':epsilon,'rtol':0,'passed':passed,'fresh_workflow_status':report['status'],'actual_flagquantum_circuits':report['actual_flagquantum_circuits'],'limits':'Finite binary64 numerical checks; no interval certification or experimental/hardware evidence.'})

print(json.dumps({tid:json.loads((O/tid/'independent-verification.json').read_text())['passed'] for tid in ['A1','A2']}))
