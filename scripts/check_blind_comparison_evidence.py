#!/usr/bin/env python3
"""Check frozen blind-agent artifacts and replay their numerical requests.

This replays deterministic evidence; it does NOT launch or claim new agent tests.
Run with the profile's CPython 3.12 interpreter.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'book/skill-evaluations/state-operator-blind-2026-10-21'
SKILL='compare-quantum-states-and-operators'
ATOL=2e-12
CODES={'within_tolerance':0,'outside_tolerance':1,'invalid_input':2,'unsupported':3}


def load(path):return json.loads(path.read_text())
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def results(path):
    data=load(path)
    return data if isinstance(data,list) else data['results']


def artifact(directory,ident,kind):
    candidates=[directory/f'{ident}.{kind}',directory/ident/kind]
    if kind=='stdout.json':candidates.append(directory/ident/'stdout.txt')
    for p in candidates:
        if p.exists():return p
    return None


def runtime_version(execution):
    command=execution.get('command',execution.get('argv',[]))
    if isinstance(command,str):return None
    return command[0] if command else None


def validate_round(name,version):
    folder=BASE/'rounds'/name
    key=load(folder/'reference-key.json')
    protocol=load(folder/'conductor-protocol.json')
    assert digest(folder/'reference-key.json')==protocol['reference_key_sha256']
    freeze=load(folder/'input-freeze.json')
    for relative,expected in freeze['files'].items():
        parts=Path(relative).parts
        if len(parts)>3 and parts[1]=='skills':
            p=BASE/'packages'/version/Path(*parts[3:])
        else:p=folder/relative
        assert digest(p)==expected,('Changed input',p)
    grade=[];helper_calls=0;runtime_compliant=0
    for group in sorted(p for p in folder.iterdir() if p.is_dir()):
        tasks={t['id']:t for t in load(group/'tasks.json')}
        output=group/'outputs'
        returned=results(output/'results.json')
        assert {r['id'] for r in returned}==set(tasks)
        for result in returned:
            ident=result['id'];task=tasks[ident];expected=key[ident]
            request_path=artifact(output,ident,'request.json')
            stdout_path=artifact(output,ident,'stdout.json')
            exec_path=artifact(output,ident,'execution.json')
            # Counts are a correct off-profile calculation, not a helper run.
            if ident in ('B3','H3'):
                assert result['selected_skill'] is None
                counts=task['data'];p=counts['successes']/counts['shots']
                se=math.sqrt(p*(1-p)/counts['shots'])
                answer=result.get('outcome',result.get('answer',{}))
                def numeric_values(obj):
                    if isinstance(obj,dict):return [v for x in obj.values() for v in numeric_values(x)]
                    if isinstance(obj,(float,int)):return [obj]
                    return []
                vals=numeric_values(answer)
                if stdout_path:vals+=numeric_values(load(stdout_path))
                assert any(abs(x-p)<ATOL for x in vals) and any(abs(x-se)<ATOL for x in vals),(ident,vals)
                grade.append({'id':ident,'disposition':'off-profile calculation; no pure-state skill selected','task_passed':True,'helper_executed':False})
                continue
            if ident in ('C4','I5') or expected['status']=='unsupported':
                assert result['selected_skill'] in (None,SKILL),(ident,'wrong boundary routing')
            else:assert result['selected_skill']==SKILL,(ident,'wrong skill routing')
            assert result.get('verification'),(ident,'missing verification evidence')
            if ident in ('C4','I5'):
                assert result['status'] in ('unsupported','not_admissible'),(ident,result['status'])
                assert task['data']['dtype']=='complex64'
                assert request_path is None,(ident,'producer contract was bypassed')
                grade.append({'id':ident,'disposition':'unsupported producer; no cast or comparison','task_passed':True,'helper_executed':False})
                continue
            assert result['status']==expected['status'],(ident,result['status'],expected)
            if 'residual' in expected or expected['status']=='invalid_input':
                assert request_path and stdout_path and exec_path,(ident,'missing actual execution artifacts')
            # A scope boundary may be explained without executing a deliberately invalid profile.
            if not (request_path and stdout_path and exec_path):
                assert expected['status']=='unsupported'
                grade.append({'id':ident,'disposition':'unsupported scope; no object decision','task_passed':True,'helper_executed':False})
                continue
            request=load(request_path);observed=load(stdout_path);execution=load(exec_path)
            assert all(request.get(k)==v for k,v in task['data'].items()),(ident,'supplied data changed')
            if 'mode' in expected:assert request['mode']==expected['mode']
            assert observed['status']==expected['status']
            exit_code=execution.get('exit_code',execution.get('returncode'))
            assert exit_code==CODES[expected['status']],(ident,exit_code)
            stderr=artifact(output,ident,'stderr.txt')
            assert stderr is None or stderr.read_text()==''
            helper_calls+=1
            if version=='0.1.1':
                assert observed['runtime']['implementation']=='cpython'
                assert observed['runtime']['python'].startswith('3.12.')
                runtime_compliant+=1
            else:
                # Historical artifact uses the captured default interpreter.
                assert runtime_version(execution)=='/Library/Developer/CommandLineTools/usr/bin/python3'
            if 'residual' in expected:
                assert abs(observed['decision_residual']-expected['residual'])<=ATOL,(ident,'analytic reference mismatch')
                assert request.get('atol',1e-10)==1e-10
                assert observed['proof_of_exact_equality'] is False
            # Replay from an isolated temporary script, preserving the recorded old numerical kernel.
            with tempfile.TemporaryDirectory(prefix='mqc-blind-replay-') as tmp:
                helper=Path(tmp)/'compare.py'
                helper.write_bytes((BASE/'packages'/version/'scripts/compare.py').read_bytes())
                proc=subprocess.run([sys.executable,str(helper)],input=json.dumps(request),capture_output=True,text=True,cwd=tmp,timeout=10)
            replay=json.loads(proc.stdout)
            assert proc.returncode==exit_code and not proc.stderr
            assert replay['status']==observed['status']
            if 'residual' in expected:
                assert abs(replay['decision_residual']-observed['decision_residual'])<=ATOL
            if ident in ('C2','F1','I2','I3'):
                assert task['cached_result']['status']!=observed['status'],(ident,'cache was not challenged')
            grade.append({'id':ident,'disposition':expected['status'],'task_passed':True,'helper_executed':True,'runtime_compliant':version=='0.1.1','residual':observed.get('decision_residual'),'original_interpreter':runtime_version(execution)})
    assert {g['id'] for g in grade}==set(key)
    for chat in load(folder/'clarification-transcript.json'):
        ident=chat['task']
        assert ident in key and 'initial' in key[ident]
        assert chat['reply']==key[ident]['reply'] and chat['numeric_answer_supplied'] is False
        matching=[r for group in folder.iterdir() if group.is_dir() for r in results(group/'outputs/results.json') if r['id']==ident]
        assert matching[0]['clarification_question'],(ident,'no question recorded')
    return {'round':name,'skill_version':version,'tasks':len(grade),'task_decisions_passed':len(grade),'helper_calls':helper_calls,'runtime_compliant_calls':runtime_compliant,'overall_runtime_gate':'passed' if version=='0.1.1' else 'failed post-run runtime audit','tasks_detail':grade}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--record',action='store_true');args=p.parse_args()
    assert sys.implementation.name=='cpython' and sys.version_info[:2]==(3,12),'Use CPython 3.12 for replay'
    manifest=BASE/'evidence-manifest.json'
    if manifest.exists():
        for relative,sha in load(manifest)['sha256'].items():assert digest(BASE/relative)==sha,relative
    rounds=[validate_round('r1','0.1.0'),validate_round('r2','0.1.0'),validate_round('r3','0.1.1')]
    assert [r['tasks'] for r in rounds]==[10,6,11]
    assert sum(r['helper_calls'] for r in rounds[:2])==14
    runtime=load(BASE/'runtime-admission.json')['checks']
    assert runtime[0]['exit_code']==3 and json.loads(runtime[0]['stdout'])['status']=='unsupported'
    assert json.loads(runtime[0]['stdout'])['runtime']['python']=='3.9.6'
    assert runtime[1]['exit_code']==1 and json.loads(runtime[1]['stdout'])['runtime']['python'].startswith('3.12.')
    current=ROOT/'skills'/SKILL
    for f in (BASE/'packages/0.1.1').rglob('*'):
        if f.is_file():assert f.read_bytes()==(current/f.relative_to(BASE/'packages/0.1.1')).read_bytes()
    report={'skill':SKILL,'current_version':'0.1.1','behavior_status':'independent-agent-tested prototype','rounds':rounds,'initial_tasks':16,'initial_decisions_correct':16,'initial_nonconforming_helper_calls':14,'initial_disposition':'not a complete pass: declared Python 3.12 runtime was not enforced or recorded','repair':'0.1.1 checks CPython 3.12 admission before parsing; reports actual runtime; instructions require explicit interpreter selection. Numerical kernel unchanged.','fresh_retest_tasks':11,'fresh_retest_passed':11,'fresh_retest_categories':{'supported_comparison':6,'invalid_input':1,'unsupported_profile':3,'off_profile_counts':1},'fresh_retest_false_successes':0,'fresh_retest_incorrect_abstentions':0,'fresh_retest_clarifications':1,'all_round_clarifications':3,'independent_executors':9,'blind_to_reference_answers':True,'grader_role':'author/conductor; analytic targets frozen before agent dispatch','scientific_acceptance':'pending','reader_trial':'not run','released_skills':0,'limitations':['Small conductor-designed nonrandom sample; not a statistical competence estimate','One implemented skill among 23 catalog entries; no claim of competition among multiple working skills','No-history agents inherit the same model configuration; exact backend revision/token/cost telemetry unavailable','Read restrictions are logical and not OS-enforced; no secret-proof isolation claim','CI replays frozen artifacts and numerical requests; it does not rerun autonomous agents']}
    if args.record:
        assert not (BASE/'report.json').exists(),'Preserve original grading record'
        (BASE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    else:
        assert load(BASE/'report.json')==report,'Recorded grade differs'
    print(json.dumps({'archived_tasks_checked':27,'initial_runtime_audit':'failed: 14 incompatible helper calls','fresh_retest':'11/11 passed','replayed_helper_calls':sum(r['helper_calls'] for r in rounds),'scientific_acceptance':'pending'}))

if __name__=='__main__':main()
