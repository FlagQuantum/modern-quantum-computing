#!/usr/bin/env python3
"""Grade/replay frozen independent-agent composition evidence; no agent rerun."""
import argparse,copy,hashlib,json,math,subprocess,sys,tempfile
from pathlib import Path
import numpy as np
from check_four_skill_integration import verify_directory,dec,enc,oracle
from check_algebra_skill import verify as verify_algebra
from check_interference_skill import oracle as interference_oracle
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'book/skill-evaluations/four-skill-integration-blind-2026-10-21'
ALG='translate-complex-linear-algebra';EV='translate-unitary-evolution';INT='reproduce-qubit-interference';CMP='compare-quantum-states-and-operators'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--record',action='store_true');args=p.parse_args();assert sys.version_info[:2]==(3,12)
 if (BASE/'evidence-manifest.json').exists():
  for n,h in load(BASE/'evidence-manifest.json')['sha256'].items():assert sha(BASE/n)==h,n
 protocol=load(BASE/'protocol.json');key=load(BASE/'reference-key.json');assert sha(BASE/'reference-key.json')==protocol['reference_key_sha256']
 for n,h in load(BASE/'input-freeze.json')['files'].items():
  parts=Path(n).parts
  if parts[1]=='skills':p=BASE/'packages'/Path(*parts[2:])
  elif parts[1]=='workflow':p=BASE/'workflow'/Path(*parts[2:])
  else:p=BASE/n
  assert sha(p)==h,n
 for f in (BASE/'packages').rglob('*'):
  if f.is_file():assert f.read_bytes()==(ROOT/'skills'/f.relative_to(BASE/'packages')).read_bytes()
 assert (BASE/'workflow/four_skill_interference.py').read_bytes()==(ROOT/'examples/integration/four_skill_interference.py').read_bytes()
 grades=[];workflows=[];extra=[];circuits=0;helper_calls=0
 for g in 'abc':
  folder=BASE/g;tasks={x['id']:x for x in load(folder/'tasks.json')};results={x['id']:x for x in load(folder/'outputs/results.json')};assert set(results)==set(tasks)
  roots=[]
  for ident,r in results.items():
   assert r['status']==key[ident]['expected_disposition'] and r['verification'] and r['evidence_paths'],ident
   if ident in ('A1','B1','C1'):assert set(r['selected_skills'])=={ALG,EV,INT,CMP}
   if ident in ('A1','B1'):assert r['clarification_question']
   grades.append({'id':ident,'status':r['status'],'selected_skills':r['selected_skills'],'passed':True})
  for report_path in sorted((folder/'outputs').rglob('report.json')):
   report=load(report_path)
   if report.get('workflow_is_agent_skill') is not False:continue
   directory=report_path.parent;roots.append(directory);q=load(directory/'source-request.json')
   ident=next((x for x in tasks if any(part.startswith(x) for part in directory.relative_to(folder).parts)),None);assert ident is not None
   expected=copy.deepcopy(tasks[ident]['experiment'])
   if ident=='A1':expected['hbar']={'value':6.582119569e-16,'unit':'eV*s'}
   if ident=='B1':
    expected['generator']={'matrix':enc(dec(expected['generator']['matrix'])*(2*math.pi)),'unit':'rad/s'};expected['phase_scan']={'values':[x*math.pi/180 for x in expected['phase_scan']['values']],'unit':'radian'};expected['analyzer']={'delta':expected['analyzer']['delta']*math.pi/180,'unit':'radian'}
   # Explicit degree conversions can differ by one rounding due to product association.
   if ident=='B1':
    assert q['generator']['unit']=='rad/s';np.testing.assert_allclose(dec(q['generator']['matrix']),dec(expected['generator']['matrix']),rtol=2e-16,atol=0)
    np.testing.assert_allclose(q['phase_scan']['values'],expected['phase_scan']['values'],rtol=2e-16,atol=0);assert abs(q['analyzer']['delta']-expected['analyzer']['delta'])<1e-15
    assert all(q[k]==v for k,v in expected.items() if k not in ('generator','phase_scan','analyzer'))
   else:assert q==expected,(ident,'source values changed')
   if report['status']=='verified':verify_directory(directory,q)
   else:assert ident=='C3' and report['status']=='unsupported' and report['actual_flagquantum_circuits']==0 and not report['helper_calls']
   circuits+=report['actual_flagquantum_circuits'];helper_calls+=len(report['helper_calls']);workflows.append({'task':ident,'path':str(directory.relative_to(BASE)),'status':report['status'],'helper_calls':len(report['helper_calls']),'actual_flagquantum_circuits':report['actual_flagquantum_circuits']})
   with tempfile.TemporaryDirectory(prefix='mqc-composition-blind-replay-') as tmp:
    request=Path(tmp)/'request.json';request.write_text(json.dumps(q));output=Path(tmp)/'run';cmd=[sys.executable,str(BASE/'workflow/four_skill_interference.py'),'--request',str(request),'--output',str(output),'--skills-root',str(BASE/'packages')]
    proc=subprocess.run(cmd,capture_output=True,text=True,timeout=180);assert not proc.stderr
    rerun=load(output/'report.json');assert rerun['status']==report['status'] and proc.returncode==(0 if report['status']=='verified' else 3)
    if rerun['status']=='verified':verify_directory(output,q)
  for path in sorted((folder/'outputs').rglob('*execution.json')):
   if any(path.is_relative_to(d) for d in roots):continue
   rec=load(path);cmd=rec.get('command',rec.get('argv',[]))
   if len(cmd)<2 or not cmd[1].endswith(('/scripts/compare.py','/scripts/interference.py','/scripts/algebra.py')):continue
   package=CMP if cmd[1].endswith('compare.py') else INT if cmd[1].endswith('interference.py') else ALG
   if path.name=='execution.json':qp,op,ep=[path.parent/x for x in ('request.json','stdout.json','stderr.txt')]
   else:
    prefix=path.name.removesuffix('.execution.json');qp,op,ep=[path.parent/(prefix+x) for x in ('.request.json','.stdout.json','.stderr.txt')]
   if not op.exists():op=op.with_suffix('.txt')
   if not qp.exists() and path.name=='C2-candidate-interference.execution.json':qp=path.parent/'C2-candidate-request.json'
   if not qp.exists() and (path.parent.parent/'request.json').exists():qp=path.parent.parent/'request.json'
   q=load(qp) if qp.exists() else json.loads(rec['stdin']);o=load(op)
   assert not ep.read_text() and o['runtime']['python'].startswith('3.12.')
   if package==INT:
    assert q['readout']['delta_radians']==-tasks['C2']['experiment']['analyzer']['delta'];assert o['status']=='verified'
    for (v,p),r in zip(interference_oracle(q),o['records']):np.testing.assert_allclose(dec(r['statevector']),v,atol=1e-11,rtol=0);np.testing.assert_allclose(r['probabilities'],p,atol=1e-11,rtol=0)
    circuits+=len(o['records'])
   elif package==ALG:assert o['status']=='outside_tolerance';verify_algebra(q,o)
   else:
    a,b=dec(q['a']),dec(q['b'])
    if q['mode']=='controlled':
     ca,cb=np.eye(4,dtype=complex),np.eye(4,dtype=complex);ca[2:,2:]=a;cb[2:,2:]=b;a,b=ca,cb
    if q['mode']!='coordinates':
     overlap=np.vdot(a,b)
     if abs(overlap)>0:b=b*np.exp(-1j*np.angle(overlap))
    residual=np.linalg.norm(a-b);assert abs(residual-o['decision_residual'])<=1e-11
    assert o['status']==('within_tolerance' if residual<=q['atol'] else 'outside_tolerance')
   with tempfile.TemporaryDirectory(prefix='mqc-composition-extra-replay-') as tmp:
    helper=Path(tmp)/Path(cmd[1]).name;helper.write_bytes((BASE/'packages'/package/'scripts'/helper.name).read_bytes());p=subprocess.run([sys.executable,str(helper)],input=json.dumps(q),capture_output=True,text=True,cwd=tmp,timeout=60)
   assert p.returncode==rec['exit_code'] and json.loads(p.stdout)['status']==o['status'] and not p.stderr
   extra.append({'path':str(path.relative_to(BASE)),'skill':package,'status':o['status'],'exit_code':rec['exit_code']});helper_calls+=1
 # Inspect candidate claims against raw mathematical data, separately from valid fresh runs.
 a2=load(BASE/'a/tasks.json')[1];u,v,_=oracle(a2['experiment']);candidate=dec(a2['submitted_handoff']['state']);overlap=np.vdot(v,candidate)
 assert np.linalg.norm(v-candidate)>.1 and np.linalg.norm(v-candidate*np.exp(-1j*np.angle(overlap)))<1e-11
 b3=load(BASE/'b/tasks.json')[2];assert b3['submitted_budget_receipt']['observed_probability_max_absolute_error']>b3['experiment']['tolerance']['coordinate_atol']
 c2=load(BASE/'c/tasks.json')[1];q=c2['experiment'];_,v,declared=oracle(q);errors=[]
 for phi,(state,p) in zip(q['phase_scan']['values'],declared):
  z=np.exp(1j*(phi+q['analyzer']['delta']));wrong=np.array([v[0]+z*v[1],v[0]-z*v[1]])/math.sqrt(2);errors.append(np.max(abs(abs(wrong)**2-p)))
 assert max(errors)>.1
 trans=load(BASE/'clarification-transcript.json');assert {x['task'] for x in trans}=={'A1','B1'}
 for x in trans:assert x['reply']==key[x['task']]['reply'] and not x['expected_result_supplied']
 assert len(grades)==9 and len(workflows)==7 and len(extra)==8 and helper_calls==110 and circuits==89,(len(grades),len(workflows),len(extra),helper_calls,circuits)
 report={'experiment':'four-skill-interference','workflow_version':'0.1.0','status':'independent-agent-tested composition prototype','agents':3,'new_tasks':9,'passed_tasks':9,'full_experiment_tasks':3,'candidate_audit_tasks':5,'unsupported_tasks':1,'verified_workflow_runs':6,'unsupported_workflow_runs':1,'recorded_helper_calls':helper_calls,'actual_flagquantum_circuits':circuits,'clarification_exchanges':2,'false_successes':0,'incorrect_abstentions':0,'task_grades':grades,'workflow_runs':workflows,'extra_helper_calls':extra,'observations':['Four-skill orchestration and independent whole-circuit/staged/analytic agreement passed','hbar and cyclic/angular/degree conversions clarified before dependent execution; original inputs retained','Lost phase, reversed basis, stale receipt, weakened budget and wrong analyzer sign candidates rejected separately from successful fresh execution','Hardware/noise/confidence-bound request remained unsupported, zero circuits; no synthetic fixture counted as execution','Actual counts include86circuits in six full workflows plus3candidate-interference circuits; classical helpers and unsupported paths add no quantum executions','No defect in frozen skills or bounded runner was found in this task set; no post-blind changes'],'grading_role':'author/conductor against registered dispositions and NumPy/scalar/matrix references','executor_context':'Three fresh no-history agents, raw tasks/four unchanged packages/bounded runner/runtime candidates only; no expected answers supplied','scientific_acceptance':'pending','reader_trial':'not run','new_agent_skills':0,'released_skills':0,'limitations':protocol['limitations']+['Published tasks become regression fixtures; CI replays numeric evidence, not autonomous agents','This is one ideal small experiment, not generic paper reproduction or arbitrary workflow acceptance']}
 if args.record:
  assert not (BASE/'report.json').exists();(BASE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 else:assert load(BASE/'report.json')==report
 print(json.dumps({'passed_tasks':9,'workflow_runs':7,'helper_calls':helper_calls,'actual_flagquantum_circuits':circuits,'new_agent_skills':0}))
if __name__=='__main__':main()
