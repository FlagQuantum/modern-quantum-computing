#!/usr/bin/env python3
"""Grade frozen agent artifacts and replay helpers, not autonomous agent behavior."""
import argparse,copy,hashlib,json,math,subprocess,sys,tempfile
from pathlib import Path
import numpy as np
from check_unitary_skill import verify,dec,enc
from check_interference_skill import oracle as interference_oracle
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'book/skill-evaluations/unitary-evolution-blind-2026-10-21'
UNIT='translate-unitary-evolution';COMPARE='compare-quantum-states-and-operators';INTER='reproduce-qubit-interference'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--record',action='store_true');args=p.parse_args();assert sys.version_info[:2]==(3,12)
    if (BASE/'evidence-manifest.json').exists():
        for name,digest in load(BASE/'evidence-manifest.json')['sha256'].items():assert sha(BASE/name)==digest,name
    protocol=load(BASE/'protocol.json');key=load(BASE/'reference-key.json');assert sha(BASE/'reference-key.json')==protocol['reference_key_sha256']
    for name,digest in load(BASE/'input-freeze.json')['files'].items():
        parts=Path(name).parts;path=BASE/'packages'/Path(*parts[2:]) if parts[1]=='skills' else BASE/name
        assert sha(path)==digest,name
    for f in (BASE/'packages').rglob('*'):
        if f.is_file():assert f.read_bytes()==(ROOT/'skills'/f.relative_to(BASE/'packages')).read_bytes()
    grades=[];calls=[];circuits=0
    for group in 'abc':
        folder=BASE/group;tasks={t['id']:t for t in load(folder/'tasks.json')};results={t['id']:t for t in load(folder/'outputs/results.json')};assert set(tasks)==set(results)
        for ident,result in results.items():
            assert result['status']==key[ident]['status'],(ident,result['status'])
            assert key[ident].get('skill',UNIT) in result['selected_skills']
            assert result['verification'] and result['evidence_paths']
            if ident in ('A1','C1','C4'):assert result['clarification_question']
            if ident=='A4':assert result['selected_skills']==[COMPARE]
            if ident=='B4':assert result['selected_skills']==[INTER]
            if ident=='B2':assert COMPARE in result['selected_skills']
            if ident=='A3':assert result['claim_disposition']['disposition']=='refuted_for_supplied_unitary'
            if ident=='B2':assert result['claim_disposition']['disposition']=='refuted_as_full_operation'
            if ident in ('C2','C3'):assert result['verification']['claim_disposition']['disposition']=='rejected'
            grades.append({'id':ident,'selected_skills':result['selected_skills'],'status':result['status'],'passed':True})
        for path in sorted((folder/'outputs').rglob('*execution.json')):
            execution=load(path);cmd=execution.get('command',[])
            if len(cmd)<2 or not cmd[1].endswith(('/scripts/unitary.py','/scripts/compare.py','/scripts/interference.py')):continue
            package=UNIT if cmd[1].endswith('unitary.py') else INTER if cmd[1].endswith('interference.py') else COMPARE
            prefix='controlled_comparison_' if path.name=='controlled_comparison_execution.json' else ''
            qp=path.parent/(prefix+'request.json');op=path.parent/(prefix+'stdout.json');ep=path.parent/(prefix+'stderr.txt')
            q=load(qp);out=load(op);ident=next(part for part in path.parts if part in tasks);raw=tasks[ident]['data']
            assert ep.read_text()=='' and out['runtime']['python'].startswith('3.12.')
            assert execution['exit_code']=={'verified':0,'within_tolerance':0,'outside_tolerance':1,'invalid_input':2,'unsupported':3}[out['status']]
            if package==UNIT:
                expected=copy.deepcopy(raw)
                if ident=='A1':expected['hbar']={'value':6.582119569e-16,'unit':'eV*s'}
                if ident=='C1':expected['context']='coherent-control'
                if ident=='C4':expected['generator']={'matrix':enc(2*math.pi*dec(raw['generator']['matrix'])),'unit':'rad/s'}
                assert q==expected,(ident,'request drift')
                if ident in ('A2','B3'):assert out['status']=='invalid_input' and 'records' not in out
                elif ident=='C3':assert out['status']=='unsupported' and 'records' not in out
                else:
                    assert out['status']=='verified';circuits+=verify(q,out)
                    if ident=='A3':assert out['controlled_context']['omitted_phase_operator_raw_frobenius']>.6
                    if ident=='B2':np.testing.assert_allclose(dec(out['unitary']),-np.eye(2),rtol=0,atol=5e-12)
                    if ident=='C2':assert out['zyz']['branch']=='north' and out['matrix_errors']['reconstruction_max_absolute']<5e-12
                    if ident=='C1':assert abs(out['zyz']['alpha']-.4085)<5e-12
            elif package==INTER:
                assert ident=='B4' and q==raw and out['status']=='verified'
                for (v,p),record in zip(interference_oracle(q),out['records']):
                    np.testing.assert_allclose(dec(record['statevector']),v,rtol=0,atol=5e-12);np.testing.assert_allclose(record['probabilities'],p,rtol=0,atol=5e-12)
                circuits+=len(out['records'])
            else:
                a,b=dec(q['a']),dec(q['b'])
                if ident=='A4':
                    assert all(q[k]==v for k,v in raw.items());assert q['mode']=='global-phase' and out['status']=='within_tolerance'
                elif ident=='A3':
                    source=load(folder/'outputs/A3/stdout.json');np.testing.assert_allclose(a,dec(source['unitary']),rtol=0,atol=5e-12);np.testing.assert_allclose(b,dec(source['native_zyz_matrix']),rtol=0,atol=5e-12)
                    assert q['mode']=='controlled' and out['status']=='outside_tolerance'
                else:
                    assert ident=='B2';np.testing.assert_allclose(a,-np.eye(2),rtol=0,atol=5e-12);np.testing.assert_allclose(b,np.eye(2),rtol=0,atol=5e-12)
                    assert out['status']==('within_tolerance' if q['mode']=='global-phase' else 'outside_tolerance')
                    if q['mode']=='controlled':assert abs(out['decision_residual']-math.sqrt(8))<5e-12
                if q['mode']=='controlled':
                    aa=np.eye(4,dtype=complex);bb=aa.copy();aa[2:,2:]=a;bb[2:,2:]=b;a,b=aa,bb
                if q['mode']!='coordinates':
                    overlap=np.vdot(a,b)
                    if abs(overlap)>1e-14:b=b*np.exp(-1j*np.angle(overlap))
                residual=np.linalg.norm(a-b);assert abs(residual-out['decision_residual'])<5e-12
            with tempfile.TemporaryDirectory(prefix='mqc-unitary-blind-replay-') as tmp:
                helper=Path(tmp)/Path(cmd[1]).name;helper.write_bytes((BASE/'packages'/package/'scripts'/helper.name).read_bytes())
                proc=subprocess.run([sys.executable,str(helper)],input=json.dumps(q),text=True,capture_output=True,cwd=tmp,timeout=60)
            rerun=json.loads(proc.stdout);assert proc.returncode==execution['exit_code'] and rerun['status']==out['status'] and not proc.stderr
            if package==UNIT and out['status']=='verified':verify(q,rerun)
            calls.append({'task':ident,'skill':package,'exit_code':execution['exit_code'],'status':out['status'],'artifact':str(path.relative_to(BASE))})
    assert len(grades)==12 and len(calls)==16 and circuits==56,(len(grades),len(calls),circuits)
    transcript=load(BASE/'clarification-transcript.json');assert {x['task'] for x in transcript}=={'A1','C1','C3','C4'}
    for x in transcript:
        assert not x['expected_output_supplied']
        if x['task']!='C3':assert x['reply']==key[x['task']]['reply']
    admission=load(BASE/'runtime-admission.json')['checks'];assert len(admission)==2 and all(x['exit_code']==3 and x['stdout']['status']=='unsupported' and not x['stderr'] for x in admission)
    probe=subprocess.run([sys.executable,'-S',str(ROOT/'skills'/UNIT/'scripts/unitary.py')],input=json.dumps(admission[1]['request']),capture_output=True,text=True);assert probe.returncode==3 and json.loads(probe.stdout)['status']=='unsupported'
    report={'skill':UNIT,'version':'0.1.0','status':'independent-agent-tested prototype','agents':3,'new_tasks':12,'passed_tasks':12,'supported_unitary_tasks':7,'invalid_input_tasks':2,'unsupported_tasks':1,'other_skill_only_tasks':2,'actual_flagquantum_circuits':circuits,'recorded_helper_calls':len(calls),'clarification_exchanges':4,'required_semantic_clarifications':3,'false_successes':0,'incorrect_abstentions':0,'task_grades':grades,'calls':calls,'observations':['Three-skill selection passed, including comparison-only and interference-only tasks','No hbar guessed; coherent-control and cyclic-versus-angular frequency clarified before dependent execution','Full complex matrices and states verified independently; omitted control phase and 2pi identity claims rejected','Tiny non-Hermitian energy generator rejected even at zero time; no silent repair','Near-pole matrix passed without unique Euler-angle claim; time-dependent task remained unsupported with separate theoretical counterexample','No package defect found in this set; no package changes or post-blind tuning'],'grading_role':'author/conductor against preregistered dispositions and NumPy eigensystem/matrix references','executor_context':'Three fresh fork_turns=none agents; tasks/catalog/three frozen skills/runtime candidates; no expected answers','scientific_acceptance':'pending','reader_trial':'not run','released_skills':0,'limitations':protocol['limitations']+['Published cases are regression fixtures; CI replay does not rerun autonomous agents or certify arbitrary papers']}
    if args.record:
        assert not (BASE/'report.json').exists();(BASE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    else:assert load(BASE/'report.json')==report
    print(json.dumps({'passed_tasks':12,'replayed_helper_calls':len(calls),'actual_flagquantum_circuits':circuits,'scientific_acceptance':'pending'}))
if __name__=='__main__':main()
