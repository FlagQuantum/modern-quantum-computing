#!/usr/bin/env python3
"""Grade archived independent-agent evidence and replay helpers, not language agents."""
import argparse,copy,hashlib,json,math,subprocess,sys,tempfile
from pathlib import Path
import numpy as np
from check_algebra_skill import verify,dec
from check_unitary_skill import verify as verify_unitary
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'book/skill-evaluations/complex-algebra-blind-2026-10-21'
ALG='translate-complex-linear-algebra';UNIT='translate-unitary-evolution';COMPARE='compare-quantum-states-and-operators'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--record',action='store_true');args=p.parse_args();assert sys.version_info[:2]==(3,12)
 if (BASE/'evidence-manifest.json').exists():
  for name,digest in load(BASE/'evidence-manifest.json')['sha256'].items():assert sha(BASE/name)==digest,name
 protocol=load(BASE/'protocol.json');key=load(BASE/'reference-key.json');assert sha(BASE/'reference-key.json')==protocol['reference_key_sha256']
 for name,digest in load(BASE/'input-freeze.json')['files'].items():
  parts=Path(name).parts;path=BASE/'packages'/Path(*parts[2:]) if parts[1]=='skills' else BASE/name;assert sha(path)==digest,name
 for f in (BASE/'packages').rglob('*'):
  if f.is_file():assert f.read_bytes()==(ROOT/'skills'/f.relative_to(BASE/'packages')).read_bytes()
 grades=[];calls=[];circuits=0
 for g in 'abc':
  folder=BASE/g;tasks={t['id']:t for t in load(folder/'tasks.json')};results={t['id']:t for t in load(folder/'outputs/results.json')};assert set(tasks)==set(results)
  for ident,result in results.items():
   assert result['status']==key[ident]['status'] and result['selected_skills']==[key[ident]['skill']],ident
   assert result['verification'] and result['evidence_paths']
   if ident in ('A1','C3'):assert result['clarification_question']
   if ident in ('B2','C1','C3'):assert result['claim_disposition'] in ('refuted','rejected')
   if ident=='A3':
    text=(folder/'outputs/A3/explanation.txt').read_text().lower();assert 'not' in text or 'false' in text or 'refut' in text or 'reject' in text
   grades.append({'id':ident,'status':result['status'],'selected_skills':result['selected_skills'],'passed':True})
  for path in sorted((folder/'outputs').rglob('*execution.json')):
   execution=load(path);cmd=execution.get('command',[])
   if len(cmd)<2 or not cmd[1].endswith(('/scripts/algebra.py','/scripts/unitary.py','/scripts/compare.py')):continue
   package=ALG if cmd[1].endswith('algebra.py') else UNIT if cmd[1].endswith('unitary.py') else COMPARE
   ident=path.name.split('.')[0] if path.name!='execution.json' else path.parent.name
   if path.name=='execution.json':qp,op,ep=[path.parent/n for n in ('request.json','stdout.json','stderr.txt')]
   else:qp,op,ep=[path.parent/(ident+n) for n in ('.request.json','.stdout.json','.stderr.txt')]
   if not op.exists():
    # Preserve each executor's original stdout filename rather than renaming it.
    op=path.parent/(ident+'.stdout');ep=path.parent/(ident+'.stderr')
   q,o=load(qp),load(op);raw=tasks[ident]['data'];expected=copy.deepcopy(raw)
   if ident=='A1':expected['direction']='passive-new-in-old'
   if ident=='C3':expected['tolerance']={'atol':1e-9,'rtol':0}
   assert q==expected,(ident,'raw input changed')
   assert ep.read_text()=='' and o['runtime']['python'].startswith('3.12.')
   assert o['status']==key[ident]['status'] and execution['exit_code']=={'verified':0,'within_tolerance':0,'outside_tolerance':1,'invalid_input':2,'unsupported':3}[o['status']]
   if package==ALG:
    if o['status'] in ('verified','within_tolerance','outside_tolerance'):
     verify(q,o)
     if 'checks' in o:assert all(c['passed'] for c in o['checks'].values())
    if ident=='A3':assert o['result']['identity_tests']['idempotent']['passed'] and not o['result']['orthogonal_projector_within_budget']
    if ident=='B2':
     c=o['result']['candidate'];assert c['residual_within_elementwise_budget'] and c['observed_distance_to_computed_solution_2']==1 and c['relative_forward_error_bound_2']==1 and c['candidate_forward_accuracy_certified'] is False
    if ident=='B1':np.testing.assert_allclose(dec(o['result']['right_numerical_kernel_projector']),np.diag([0,0,1,1]),atol=1e-11,rtol=0)
    if ident=='C3':assert o['result']['comparison']['max_absolute_error']>1.4e-9 and o['status']=='outside_tolerance'
    assert o.get('quantum_execution',False) is False
   elif package==UNIT:
    assert ident=='A4';circuits+=verify_unitary(q,o);assert o['actual_flagquantum_circuits']==9 and o['controlled_context']['omitted_phase_operator_raw_frobenius']>.05
   else:
    assert ident=='B4' and q['mode']=='global-phase';a,b=dec(q['a']),dec(q['b']);c=np.vdot(a,b);res=np.linalg.norm(a-b*np.exp(-1j*np.angle(c)));assert res<=1e-10 and abs(o['decision_residual']-res)<=1e-11
   with tempfile.TemporaryDirectory(prefix='mqc-algebra-blind-replay-') as tmp:
    helper=Path(tmp)/Path(cmd[1]).name;helper.write_bytes((BASE/'packages'/package/'scripts'/helper.name).read_bytes());proc=subprocess.run([sys.executable,str(helper)],input=json.dumps(q),capture_output=True,text=True,cwd=tmp,timeout=60)
   out=json.loads(proc.stdout);assert proc.returncode==execution['exit_code'] and out['status']==o['status'] and not proc.stderr
   if package==ALG and out['status'] in ('verified','within_tolerance','outside_tolerance'):verify(q,out)
   elif package==UNIT:verify_unitary(q,out)
   calls.append({'task':ident,'skill':package,'status':o['status'],'exit_code':execution['exit_code'],'artifact':str(path.relative_to(BASE))})
 assert len(grades)==len(calls)==12 and circuits==9,(len(grades),len(calls),circuits)
 trans=load(BASE/'clarification-transcript.json');assert {x['task'] for x in trans}=={'A1','C3','C4'}
 for x in trans:
  assert not x['expected_output_supplied']
  if x['task'] in ('A1','C3'):assert x['reply']==key[x['task']]['reply']
 admission=load(BASE/'runtime-admission.json')['checks'];assert len(admission)==2 and all(c['exit_code']==3 and c['stdout']['status']=='unsupported' and not c['stderr'] for c in admission)
 probe=subprocess.run([sys.executable,'-S',str(ROOT/'skills'/ALG/'scripts/algebra.py')],input=json.dumps(admission[1]['request']),capture_output=True,text=True);assert probe.returncode==3 and json.loads(probe.stdout)['status']=='unsupported'
 report={'skill':ALG,'version':'0.1.0','status':'independent-agent-tested prototype','agents':3,'new_tasks':12,'passed_tasks':12,'supported_algebra_tasks':7,'invalid_input_tasks':2,'unsupported_tasks':1,'other_skill_only_tasks':2,'recorded_helper_calls':12,'algebra_helper_calls':10,'algebra_quantum_circuits':0,'routed_flagquantum_circuits':9,'clarification_exchanges':3,'required_semantic_clarifications':2,'false_successes':0,'incorrect_abstentions':0,'task_grades':grades,'calls':calls,'observations':['Correct selection among four available skill packages, including actual physical circuit routing and isolated ray comparison','Passive basis convention and comparison tolerance clarified before dependent execution','Idempotence-only orthogonal projection, residual-only forward accuracy, entrywise exponential and componentwise complex-error claims rejected','Rectangular repeated-block SVD checked through full reconstruction/kernel projector rather than raw factor uniqueness','Shape-broadcast admission and tiny non-Hermitian spectrum input rejected; logarithm request remained unsupported','Fourth helper made zero quantum executions; nine actual FlagQuantum circuits belong only to routed third skill','No package defect found; no package changes or post-blind tuning'],'grading_role':'author/conductor against preregistered dispositions, separate NumPy/analytic/exact references and raw execution records','executor_context':'Three fresh fork_turns=none agents, no expected answers; raw tasks/catalog/four frozen packages and existing interpreter candidates','scientific_acceptance':'pending','reader_trial':'not run','released_skills':0,'limitations':protocol['limitations']+['NumPy/Torch may share numerical backend families; analytic and exact fixtures supplement their agreement','Published cases become regression fixtures; CI replay does not rerun autonomous agents']}
 if args.record:
  assert not (BASE/'report.json').exists();(BASE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 else:assert load(BASE/'report.json')==report
 print(json.dumps({'passed_tasks':12,'replayed_helper_calls':12,'fourth_skill_quantum_circuits':0,'routed_flagquantum_circuits':9,'scientific_acceptance':'pending'}))
if __name__=='__main__':main()
