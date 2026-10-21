#!/usr/bin/env python3
"""Grade/replay frozen independent-agent evidence; does not rerun language agents."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import numpy as np
from check_interference_skill import oracle

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'book/skill-evaluations/qubit-interference-blind-2026-10-21'
INTERFERENCE='reproduce-qubit-interference';COMPARE='compare-quantum-states-and-operators'
ATOL=2e-12


def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def artifacts(path):
    stem=path.name
    if stem=='execution.json':return path.parent/'request.json',path.parent/'stdout.json',path.parent/'stderr.txt'
    if '.helper.execution.json' in stem:
        ident=stem.split('.')[0]
        return path.parent/(ident+'.request.json'),path.parent/(ident+'.helper.stdout'),path.parent/(ident+'.helper.stderr')
    prefix=stem.removesuffix('.execution.json')
    return path.parent/(prefix+'.request.json'),path.parent/(prefix+'.stdout.json'),path.parent/(prefix+'.stderr.txt')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--record',action='store_true');args=p.parse_args()
    assert sys.implementation.name=='cpython' and sys.version_info[:2]==(3,12)
    manifest=BASE/'evidence-manifest.json'
    if manifest.exists():
        for relative,digest in load(manifest)['sha256'].items():assert sha(BASE/relative)==digest,relative
    protocol=load(BASE/'protocol.json');key=load(BASE/'reference-key.json')
    assert sha(BASE/'reference-key.json')==protocol['reference_key_sha256']
    for relative,digest in load(BASE/'input-freeze.json')['files'].items():
        parts=Path(relative).parts
        actual=BASE/'packages'/Path(*parts[2:]) if parts[1]=='skills' else BASE/relative
        assert sha(actual)==digest,relative
    # Both loaded packages must still match their frozen, actually evaluated contents.
    for package in (INTERFERENCE,COMPARE):
        for path in (BASE/'packages'/package).rglob('*'):
            if path.is_file():assert path.read_bytes()==(ROOT/'skills'/package/path.relative_to(BASE/'packages'/package)).read_bytes()
    grades=[];calls=[];circuits=0
    for group in 'abc':
        folder=BASE/group;tasks={x['id']:x for x in load(folder/'tasks.json')};out=folder/'outputs'
        returned={x['id']:x for x in load(out/'results.json')}
        assert set(returned)==set(tasks)
        for ident,result in returned.items():
            assert result.get('verification') and result.get('evidence_paths')
            expected=key[ident]
            if 'skill' in expected:assert expected['skill'] in result['selected_skills'],ident
            if ident=='A4':assert result['selected_skills']==[COMPARE]
            if ident=='B2':
                assert set(result['selected_skills'])=={INTERFERENCE,COMPARE}
                assert result['verification']['global_phase_equivalent'] is False
                assert abs(result['verification']['ray_distance']-math.sqrt(2))<=ATOL
            if ident=='B3':
                assert result['selected_skills']==[]
                assert result['status']=='unsupported_physical_profile_laboratory_claim_unverified'
            elif ident=='C3':
                assert result['status']=='unsupported_profile_with_separate_derivation'
                assert not list(out.glob('C3*execution.json'))
                for record in result['verification']['records']:np.testing.assert_allclose(record['probabilities'],[1,0],rtol=0,atol=ATOL)
            elif ident=='A3':assert result['status']=='invalid_input'
            elif ident=='A4':assert result['status']=='within_tolerance'
            else:assert result['status'].startswith('verified'),ident
            if ident in ('A1','C1'):assert result['clarification_question']
            if ident=='B4':
                comparisons=result['verification']['claim_comparison']
                assert len(comparisons)==3 and all(x['claim_within_tolerance'] is False for x in comparisons)
                for item in comparisons:
                    assert abs(item['claimed_p0']-(1+math.cos(item['phi']+item['delta']))/2)<=ATOL
                    assert abs(item['actual_p0']-item['claimed_p0'])>1e-3
            if ident=='C4':assert result['verification']['cache_claim']=='rejected' and result['verification']['cache_max_absolute_error']>.49
            grades.append({'id':ident,'recorded_status':result['status'],'selected_skills':result['selected_skills'],'disposition_passed':True})
        for path in sorted(out.rglob('*execution.json')):
            execution=load(path);cmd=execution.get('command',execution.get('argv',[]))
            if not isinstance(cmd,list) or len(cmd)<2:continue
            if not (cmd[1].endswith('/scripts/interference.py') or cmd[1].endswith('/scripts/compare.py')):continue
            package=INTERFERENCE if cmd[1].endswith('interference.py') else COMPARE
            request_path,stdout_path,stderr_path=artifacts(path)
            q=load(request_path);actual=load(stdout_path)
            ident=path.parent.name if path.parent.name in tasks else path.name.split('.')[0]
            task=tasks[ident];exit_code=execution['exit_code']
            assert stderr_path.read_text()==''
            assert actual['runtime']['implementation']=='cpython' and actual['runtime']['python'].startswith('3.12.')
            if package==INTERFERENCE:
                if ident=='B2':
                    index=int(path.name.split('.')[0].removeprefix('experiment'))-1
                    source=task['experiments'][index]
                else:source=task['data']
                if ident=='C1':
                    assert q['angle_unit']=='radian'
                    np.testing.assert_allclose(q['phase_radians'],[math.pi/6,5*math.pi/12],rtol=0,atol=ATOL)
                    assert all(q[k]==v for k,v in source.items() if k!='phase_radians')
                else:assert all(q[k]==v for k,v in source.items()),(ident,'changed input')
                if ident=='A1':assert q['readout']=={'type':'phase-h','delta_radians':.419}
                if ident in ('A3','B3'):
                    assert actual['status']=='invalid_input' and exit_code==2 and 'records' not in actual
                else:
                    assert actual['status']=='verified' and exit_code==0
                    assert actual['versions']['flagquantum']=='0.3.1' and actual['versions']['torch'].split('+')[0]=='2.13.0'
                    refs=oracle(q);assert len(refs)==len(actual['records'])
                    for (state,probability),record in zip(refs,actual['records']):
                        np.testing.assert_allclose([complex(*x) for x in record['statevector']],state,rtol=0,atol=ATOL)
                        np.testing.assert_allclose(record['probabilities'],probability,rtol=0,atol=ATOL)
                        assert record['passed'] and record['shape']==[1,2]
                    circuits+=len(refs)
                    if ident=='A2':
                        fringe=actual['fringe'];assert abs(fringe['continuous_visibility']-.96)<=ATOL
                        assert fringe['continuous_p0_min']<fringe['sampled_p0_min'] and fringe['continuous_p0_max']>fringe['sampled_p0_max']
                    if ident=='B1':assert actual['fringe']['applicable'] is False
                    if ident=='C2':assert actual['fringe']['relative_phase_identifiable'] is False and actual['fringe']['continuous_visibility']==0
            else:
                assert q['mode']=='global-phase'
                if ident=='A4':
                    assert all(q[k]==v for k,v in task['data'].items())
                    assert actual['status']=='within_tolerance' and actual['decision_residual']<=ATOL and exit_code==0
                else:
                    assert ident=='B2' and q['a']==task['experiments'][0]['state'] and q['b']==task['experiments'][1]['state']
                    assert actual['status']=='outside_tolerance' and abs(actual['decision_residual']-math.sqrt(2))<=ATOL and exit_code==1
            # Replays actual frozen helper requests, not new autonomous behavior.
            with tempfile.TemporaryDirectory(prefix='mqc-interference-blind-replay-') as temp:
                helper=Path(temp)/Path(cmd[1]).name
                helper.write_bytes((BASE/'packages'/package/'scripts'/helper.name).read_bytes())
                proc=subprocess.run([sys.executable,str(helper)],input=json.dumps(q),text=True,capture_output=True,cwd=temp,timeout=60)
            replay=json.loads(proc.stdout)
            assert proc.returncode==exit_code and replay['status']==actual['status'] and not proc.stderr
            if package==INTERFERENCE and actual['status']=='verified':
                for a,b in zip(replay['records'],actual['records']):np.testing.assert_allclose(a['probabilities'],b['probabilities'],rtol=0,atol=ATOL)
            calls.append({'task':ident,'skill':package,'exit_code':exit_code,'status':actual['status'],'runtime':actual['runtime'],'artifact':str(path.relative_to(BASE))})
    admission=load(BASE/'runtime-admission.json')['checks']
    assert {x['name'] for x in admission}=={'wrong_python','missing_packages'}
    assert all(x['exit_code']==3 and x['stdout']['status']=='unsupported' for x in admission)
    probe=subprocess.run([sys.executable,'-S',str(ROOT/'skills'/INTERFERENCE/'scripts/interference.py')],input=json.dumps(admission[1]['request']),capture_output=True,text=True,timeout=20)
    assert probe.returncode==3 and json.loads(probe.stdout)['status']=='unsupported' and not probe.stderr
    assert len(grades)==12 and len(calls)==13 and circuits==18,(len(grades),len(calls),circuits)
    transcript=load(BASE/'clarification-transcript.json');assert {x['task'] for x in transcript}=={'A1','C1','B3'}
    for entry in transcript:
        assert entry['numeric_answer_supplied'] is False
        if entry['task'] in ('A1','C1'):assert entry['reply']==key[entry['task']]['reply']
    report={'skill':INTERFERENCE,'version':'0.1.0','status':'independent-agent-tested prototype','agents':3,'new_tasks':12,'passed_tasks':12,'supported_interference_tasks':8,'invalid_input_tasks':1,'unsupported_profile_tasks':2,'comparison_only_tasks':1,'actual_flagquantum_circuits':18,'recorded_helper_calls':13,'clarification_exchanges':3,'required_semantic_clarifications':2,'false_successes':0,'incorrect_abstentions':0,'task_grades':grades,'calls':calls,'observations':['Explicit choice between two available packaged skills passed','B2 uses both skills: identical fixed-setting probabilities do not imply equal state rays','B3 untouched raw noisy request fails pure-profile schema with actual exit 2; scientific noisy/laboratory scope remains unsupported, not certified','C3 reports unsupported chronology and separately derives the exact requested order without claiming helper execution','B4 rejects the wrong plus-delta formula; C4 rejects cached success','No package defect or numerical discrepancy was found in this blind set; no post-blind tuning performed'],'grading_role':'author/conductor against frozen reference dispositions and independent matrix oracle','evaluator_context':'Three no-history agents; raw tasks, catalog, frozen packages and existing interpreter candidates only; no expected answers supplied','scientific_acceptance':'pending','reader_trial':'not run','released_skills':0,'limitations':['Small conductor-designed nonrandom task set','Logical workspace restrictions, not OS-enforced isolation','Same inherited model configuration; exact backend revision/token/cost telemetry unavailable','Published cases are regression fixtures after this evaluation','CI replays frozen numeric evidence; it does not rerun agents or certify arbitrary-paper reproduction']}
    if args.record:
        assert not (BASE/'report.json').exists();(BASE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    else:assert load(BASE/'report.json')==report
    print(json.dumps({'passed_tasks':12,'actual_flagquantum_circuits':18,'replayed_helper_calls':13,'scientific_acceptance':'pending'}))


if __name__=='__main__':main()
