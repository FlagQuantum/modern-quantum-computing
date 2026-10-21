#!/usr/bin/env python3
"""Fresh blind-retask archive grader/replayer; does not rerun autonomous agents."""
import argparse,copy,hashlib,json,math,subprocess,sys,tempfile
from decimal import Decimal,localcontext
from pathlib import Path
from check_algebra_skill import verify,dec
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'book/skill-evaluations/complex-algebra-blind-retest-2026-10-21';ALG='translate-complex-linear-algebra'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--record',action='store_true');args=p.parse_args();assert sys.version_info[:2]==(3,12)
 if (BASE/'evidence-manifest.json').exists():
  for n,h in load(BASE/'evidence-manifest.json')['sha256'].items():assert sha(BASE/n)==h,n
 protocol=load(BASE/'protocol.json');key=load(BASE/'reference-key.json');assert sha(BASE/'reference-key.json')==protocol['reference_key_sha256']
 for n,h in load(BASE/'input-freeze.json')['files'].items():
  parts=Path(n).parts;p=BASE/'packages'/Path(*parts[2:]) if parts[1]=='skills' else BASE/n;assert sha(p)==h,n
 for f in (BASE/'packages').rglob('*'):
  if f.is_file():assert f.read_bytes()==(ROOT/'skills'/f.relative_to(BASE/'packages')).read_bytes()
 grades=[];calls=[];tails=[]
 for g in 'def':
  folder=BASE/g;tasks={x['id']:x for x in load(folder/'tasks.json')};results={x['id']:x for x in load(folder/'outputs/results.json')};assert set(results)==set(tasks)
  for ident,result in results.items():
   assert result['status']==key[ident]['status'] and result['selected_skills']==[ALG]
   assert result['verification'] and result['evidence_paths']
   if ident=='E2':assert result['clarification_question']
   grades.append({'id':ident,'status':result['status'],'passed':True})
  for path in sorted((folder/'outputs').rglob('*execution.json')):
   record=load(path);cmd=record.get('command',record.get('argv',[]))
   if len(cmd)<2 or not cmd[1].endswith('/scripts/algebra.py'):continue
   ident=path.parent.name if path.name=='execution.json' else path.name.split('.')[0]
   if path.name=='execution.json':qp,op,ep=[path.parent/n for n in ('request.json','stdout.json','stderr.txt')]
   else:qp,op,ep=[path.parent/(ident+n) for n in ('.request.json','.stdout','.stderr')]
   q,o=load(qp),load(op);expected=copy.deepcopy(tasks[ident]['data'])
   if ident=='E2':expected['direction']='passive-new-in-old'
   assert q==expected and not ep.read_text()
   assert o['contract_version']=='0.1.1' and o['runtime']['python'].startswith('3.12.')
   assert o['status']==key[ident]['status'] and record['exit_code']=={'verified':0,'outside_tolerance':1,'invalid_input':2,'unsupported':3}[o['status']]
   if o['status'] in ('verified','outside_tolerance'):
    verify(q,o);assert o['quantum_execution'] is False
   if ident in ('D1','E1'):
    rho=max(sum(abs(z) for z in row) for row in dec(q['matrix']));result=o['result']
    with localcontext() as ctx:
     ctx.prec=180;rr=Decimal.from_float(rho);tail=rr**41/Decimal(math.factorial(41))/(1-rr/42);logtail=tail.ln()
     assert 0<tail<Decimal.from_float(math.nextafter(0.,1.))
     assert Decimal.from_float(result['mathematical_infinity_norm_tail_bound'])>=tail
     assert abs(float(logtail)-result['tail_log_upper_expression'])<1e-10
    assert result['tail_bound_underflow_clamped'] and result['tail_numeric_record_is_interval_certificate'] is False
    tails.append({'task':ident,'decimal_precision':180,'analytic_tail_log':float(logtail),'recorded_bound_positive':True,'underflow_flag':True})
   if ident=='F1':assert o['result']['mathematical_infinity_norm_tail_bound']==0 and not o['result']['tail_bound_underflow_clamped'] and o['result']['tail_log_upper_expression'] is None
   with tempfile.TemporaryDirectory(prefix='mqc-algebra-retest-') as tmp:
    helper=Path(tmp)/'algebra.py';helper.write_bytes((BASE/'packages'/ALG/'scripts/algebra.py').read_bytes());p=subprocess.run([sys.executable,str(helper)],input=json.dumps(q),capture_output=True,text=True,cwd=tmp,timeout=60)
   out=json.loads(p.stdout);assert p.returncode==record['exit_code'] and out['status']==o['status'] and not p.stderr
   if out['status'] in ('verified','outside_tolerance'):verify(q,out)
   calls.append({'task':ident,'status':o['status'],'exit_code':record['exit_code'],'artifact':str(path.relative_to(BASE))})
 assert len(grades)==len(calls)==9 and len(tails)==2
 trans=load(BASE/'clarification-transcript.json');assert {x['task'] for x in trans}=={'E2','F3'} and all(not x['expected_output_supplied'] for x in trans)
 assert next(x['reply'] for x in trans if x['task']=='E2')==key['E2']['reply']
 report={'skill':ALG,'version':'0.1.1','status':'independent-agent-tested prototype','agents':3,'new_tasks':9,'passed_tasks':9,'supported_tasks':7,'invalid_input_tasks':1,'unsupported_tasks':1,'recorded_helper_calls':9,'algebra_quantum_circuits':0,'routed_flagquantum_circuits':0,'clarification_exchanges':2,'required_semantic_clarifications':1,'false_successes':0,'incorrect_abstentions':0,'task_grades':grades,'calls':calls,'independent_decimal_tail_checks':tails,'initial_evaluation':'Initial0.1.0:12/12 tasks passed; author subsequently found numeric tail-bound underflow outside that set. Initial package, reports and failing record preserved.','repair':'0.1.1 retains finite log of positive analytic expression, flags/clamps ordinary positive underflow; zero norm alone reports zero. Numeric records remain non-interval estimates.','grading_role':'author/conductor against registered dispositions, NumPy/analytic/exact references and180-digit Decimal tail checks','executor_context':'Three additional fresh fork_turns=none agents; no expected answers, suspected defect description or prior conclusions supplied','scientific_acceptance':'pending','reader_trial':'not run','released_skills':0,'limitations':protocol['limitations']+['Published tasks are regression fixtures; CI replay is not new autonomous agent testing']}
 if args.record:
  assert not (BASE/'report.json').exists();(BASE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 else:assert load(BASE/'report.json')==report
 print(json.dumps({'fresh_retest_tasks':9,'replayed_helper_calls':9,'decimal_tail_checks':2,'quantum_circuits':0,'scientific_acceptance':'pending'}))
if __name__=='__main__':main()
