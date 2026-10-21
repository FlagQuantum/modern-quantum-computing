#!/usr/bin/env python3
"""Author-run bounded composition checks; independent NumPy/analytic final oracle."""
import argparse,copy,hashlib,json,math,shutil,subprocess,sys,tempfile
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];EVIDENCE=ROOT/'book/skill-evaluations/four-skill-integration-v0.1.0';WORKFLOW=ROOT/'examples/integration/four_skill_interference.py'
def enc(x):
 a=np.asarray(x);return np.stack((a.real,a.imag),axis=-1).tolist()
def dec(x):
 a=np.asarray(x);return a[...,0]+1j*a[...,1]
def oracle(q):
 g=dec(q['generator']['matrix']);t=q['time']['value']*(1e-9 if q['time']['unit']=='ns' else 1);e=g*t/(q['hbar']['value'] if q['generator']['unit']=='eV' else 1)
 vals,vec=np.linalg.eigh(e);u=(vec*np.exp(-1j*vals))@vec.conj().T;v=u@dec(q['initial_state']);delta=q['analyzer']['delta'];H=np.array([[1,1],[1,-1]])/math.sqrt(2)
 records=[]
 for phi in q['phase_scan']['values']:
  state=H@np.diag([1,np.exp(1j*(phi-delta))])@v;records.append((state,abs(state)**2))
 return u,v,records

def verify_directory(directory,q):
 directory=Path(directory);report=json.loads((directory/'report.json').read_text());assert report['status']=='verified' and report['workflow_is_agent_skill'] is False
 u,v,records=oracle(q);eps=q['tolerance']['coordinate_atol'];ev=json.loads((directory/'02-evolution/stdout.json').read_text());np.testing.assert_allclose(dec(ev['unitary']),u,rtol=0,atol=eps)
 for expected,actual in zip(records,report['outputs']):
  state,p=expected
  np.testing.assert_allclose(dec(actual['statevector']),state,rtol=0,atol=eps);np.testing.assert_allclose(dec(actual['staged_statevector']),state,rtol=0,atol=eps);np.testing.assert_allclose(actual['probabilities'],p,rtol=0,atol=eps)
  # Separate scalar Born expansion, not a tensor backend.
  phi=actual['phase_radians'];p0=sum(abs(v)**2)/2+(v[0].conjugate()*np.exp(1j*(phi-q['analyzer']['delta']))*v[1]).real
  assert abs(actual['probabilities'][0]-p0)<=eps
  assert actual['shape']==[1,2] and actual['state_dtype']=='torch.complex128' and actual['probability_dtype']=='torch.float64' and actual['device']=='cpu'
 ledger=report['tolerance_ledger'];assert ledger['coordinate_max_absolute']==eps and ledger['state_l2_atol']==math.sqrt(2)*eps and ledger['operator_frobenius_atol']==2*eps and ledger['rtol']==0
 calls=report['helper_calls'];assert {c['skill'] for c in calls}==set(report['skills']) and len(report['skills'])==4
 circuits=0
 for c in calls:
  folder=directory/Path(c['request_path']).parent;raw=json.loads((folder/'stdout.json').read_text());request=json.loads((folder/'request.json').read_text())
  assert raw['runtime']['python'].startswith('3.12.') and not (folder/'stderr.txt').read_text()
  text=json.dumps(request,sort_keys=True,separators=(',',':'),allow_nan=False);assert hashlib.sha256(text.encode()).hexdigest()==c['request_sha256']
  circuits+=raw.get('actual_flagquantum_circuits',len(raw.get('records',[])) if c['skill']=='reproduce-qubit-interference' else 0)
 circuits+=json.loads((directory/'continuous-circuit.json').read_text())['actual_flagquantum_circuits'];assert circuits==report['actual_flagquantum_circuits']==9+2*len(records)
 return report

def main():
 p=argparse.ArgumentParser();p.add_argument('--record',action='store_true');args=p.parse_args();assert sys.version_info[:2]==(3,12)
 freeze=json.loads((EVIDENCE/'freeze.json').read_text())
 if (EVIDENCE/'evidence-manifest.json').exists():
  for n,h in json.loads((EVIDENCE/'evidence-manifest.json').read_text())['sha256'].items():assert hashlib.sha256((EVIDENCE/n).read_bytes()).hexdigest()==h,n
 for n,h in freeze['sha256'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
 base=json.loads((ROOT/'examples/integration/interference-request.json').read_text());cases=[]
 def add(name,cat,q,status='verified',fault=None):cases.append(dict(name=name,category=cat,request=q,expected_status=status,fault=fault))
 add('energy_baseline','normal',base)
 q=copy.deepcopy(base);q['generator']={'matrix':enc(dec(q['generator']['matrix'])/q.pop('hbar')['value']),'unit':'rad/s'};add('same_angular_generator','normal',q)
 q=copy.deepcopy(base);q['time']={'value':.61e-9,'unit':'s'};add('same_time_seconds','normal',q)
 q=copy.deepcopy(base);q['generator']['matrix']=enc(np.array([[.13,.19-.23j],[.19+.23j,-.17]])*base['hbar']['value']*1e9);q['tolerance']['coordinate_atol']=5e-12;add('general_complex_transfer','author-transfer',q)
 q=copy.deepcopy(base);q['time']['value']=0;add('zero_time','boundary',q)
 q=copy.deepcopy(base);q['initial_state']=enc([1,0]);q['phase_scan']['values']=[-.5,.5];add('basis_input','boundary',q)
 for f in ('ns-as-s','drop-phase','basis-swap','shape-broadcast','stale-cache','analyzer-sign','tolerance-loosen'):add(f,'injected-error',base,'rejected_mismatch',f)
 for name,change,status in [('missing_hbar',{'hbar':None},'needs_clarification'),('unresolved_Hz',{'generator':{'matrix':base['generator']['matrix'],'unit':'Hz'}},'needs_clarification'),('bad_norm',{'initial_state':enc([1,1])},'invalid_input'),('hardware_claim',{'profile':'hardware'},'unsupported'),('nonzero_rtol',{'tolerance':{'coordinate_atol':1e-10,'rtol':1e-8}},'invalid_input')]:
  q=copy.deepcopy(base);q.update(change);add(name,'input-boundary',q,status)
 logs=[];total=0
 with tempfile.TemporaryDirectory(prefix='mqc-composition-author-') as tmp:
  for c in cases:
   folder=Path(tmp)/c['name'];request=Path(tmp)/(c['name']+'.json');request.write_text(json.dumps(c['request']));cmd=[sys.executable,str(WORKFLOW),'--request',str(request),'--output',str(folder),'--skills-root',str(ROOT/'skills')]
   if c['fault']:cmd+=['--fault',c['fault']]
   proc=subprocess.run(cmd,capture_output=True,text=True,timeout=180);r=json.loads((folder/'report.json').read_text());assert r['status']==c['expected_status'] and not proc.stderr,(c['name'],proc.stdout,proc.stderr,r.get('reason'))
   assert proc.returncode=={'verified':0,'rejected_mismatch':1,'needs_clarification':2,'invalid_input':2,'unsupported':3}[r['status']]
   if r['status']=='verified':verify_directory(folder,c['request'])
   if c['name']=='drop-phase':assert r['phase_witness']['state_ray']=='within_tolerance' and r['phase_witness']['controlled_operator']=='outside_tolerance' and r['stage']=='08-state-coordinate-handoff'
   total+=r['actual_flagquantum_circuits'];logs.append({**c,'actual_exit_code':proc.returncode,'actual_stdout':json.loads(proc.stdout),'actual_stderr':proc.stderr,'workflow_report':r,'passed':True})
   if args.record:
    target=EVIDENCE/'cases'/c['name'];assert not target.exists();shutil.copytree(folder,target)
 report={'experiment':'four-skill-interference','workflow_version':'0.1.0','author_cases':len(logs),'passed':len(logs),'counts':dict(Counter(c['category'] for c in logs)),'actual_flagquantum_circuits':total,'oracle':'Independent NumPy Hermitian eigensystem, chronological readout products and scalar Born cross term; local budgets and caller data validated separately','evaluator_role':'author/conductor','scientific_acceptance':'pending','reader_trial':'not run','new_agent_skills':0,'cases':logs}
 if args.record:
  target=EVIDENCE/'author-report.json';assert not target.exists();target.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ('passed','counts','actual_flagquantum_circuits','new_agent_skills')}))
if __name__=='__main__':main()
