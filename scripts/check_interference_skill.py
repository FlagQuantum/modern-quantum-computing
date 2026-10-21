#!/usr/bin/env python3
"""Author-run CLI tests for the bounded interference skill; not agent evaluation."""
import argparse
from collections import Counter
from copy import deepcopy
from datetime import datetime,timezone
import hashlib
import json
import math
import cmath
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT/'skills/reproduce-qubit-interference'
EVIDENCE=ROOT/'book/skill-evaluations/qubit-interference-v0.1.0'


def encode(xs):return [[complex(z).real,complex(z).imag] for z in xs]
def request(state,phases,delta=0,direct=False):
    return dict(profile='ideal-pure-single-qubit',state=encode(state),basis=['0','1'],angle_unit='radian',phase_radians=phases,
                readout={'type':'computational'} if direct else {'type':'phase-h','delta_radians':delta},atol=1e-10)


def oracle(q):
    state=np.array([complex(*x) for x in q['state']],dtype=np.complex128)
    H=np.array([[1,1],[1,-1]],dtype=np.complex128)/math.sqrt(2)
    records=[]
    for phi in q['phase_radians']:
        D=np.diag([1,np.exp(1j*phi)])
        out=D@state
        if q['readout']['type']=='phase-h':
            out=H@np.diag([1,np.exp(-1j*q['readout']['delta_radians'])])@out
        records.append((out,abs(out)**2))
    return records


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--record',action='store_true');args=parser.parse_args()
    assert sys.implementation.name=='cpython' and sys.version_info[:2]==(3,12)
    freeze=json.loads((EVIDENCE/'package-freeze.json').read_text())
    hashes={str(p.relative_to(PACKAGE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(PACKAGE.rglob('*')) if p.is_file() and '__pycache__' not in str(p)}
    assert hashes==freeze['sha256']
    cases=[]
    def add(name,category,q,status='verified',raw=None):cases.append(dict(name=name,category=category,request=q,expected_status=status,raw_request=raw))
    S=1/math.sqrt(2)
    add('balanced_cardinal_scan','normal',request([S,S],[0,math.pi/2,math.pi,3*math.pi/2,2*math.pi]))
    add('positive_i_shifted','normal',request([S,1j*S],[0],math.pi/2))
    add('negative_i_shifted','normal',request([S,-1j*S],[0],math.pi/2))
    add('complex_conjugate','normal',request([1j*S,S],[0],math.pi/2))
    add('unbalanced_complex','normal',request([.6j,-.8j],[0,.7,math.pi],.2))
    add('computational_direct','normal',request([.6,.8j],[0,.49,2.31],direct=True))
    add('absent_zero_path','boundary',request([0,cmath.exp(.19j)],[-.5,0,1.7],.31))
    add('absent_one_path','boundary',request([1,0],[.4,1.6],-.21))
    add('duplicate_and_negative_phases','boundary',request([S,S],[-math.pi,-math.pi,0,2*math.pi]))
    add('angle_boundaries','boundary',request([.6,.8],[-1024,1024],1024))
    add('maximum_grid','boundary',request([.6,.8],[2*math.pi*k/128 for k in range(129)]))
    add('sparse_extrema','boundary',request([.6,.8],[.41,.99],.17))
    base=request([S,S],[.2,.8],.3)
    changes=[
        ('zero_state',{'state':encode([0,0])},'invalid_input'),
        ('nonunit_state',{'state':encode([1,1])},'invalid_input'),
        ('batch_state',{'state':[encode([S,S])]},'invalid_input'),
        ('wrong_basis',{'basis':['1','0']},'unsupported'),
        ('degrees_not_relabelled',{'angle_unit':'degree'},'unsupported'),
        ('noisy_profile',{'profile':'noisy'},'unsupported'),
        ('missing_delta',{'readout':{'type':'phase-h'}},'invalid_input'),
        ('extra_computational_delta',{'readout':{'type':'computational','delta_radians':0}},'invalid_input'),
        ('unsupported_analyzer',{'readout':{'type':'rotation-y'}},'unsupported'),
        ('empty_grid',{'phase_radians':[]},'invalid_input'),
        ('oversize_grid',{'phase_radians':[0]*130},'invalid_input'),
        ('angle_outside',{'phase_radians':[1024.01]},'invalid_input'),
        ('boolean_angle',{'phase_radians':[True]},'invalid_input'),
        ('extra_key',{'shots':100},'invalid_input'),
        ('loose_budget',{'atol':.1},'invalid_input'),
        ('string_coordinate',{'state':[['1',0],[0,0]]},'invalid_input')]
    for name,change,status in changes:
        q=deepcopy(base);q.update(change);add(name,'error',q,status)
    for name,text in [('nan','{"atol":NaN}'),('duplicate','{"profile":"x","profile":"y"}'),('syntax','{')]:
        add(name,'error',None,'invalid_input',text)
    # New author transfer fixtures after package freeze; distinct from independent agent tasks.
    v=[(1+2j)/math.sqrt(10),(2-1j)/math.sqrt(10)]
    add('nonlandmark_complex_scan','author-transfer',request(v,[-.713,.283,1.917],.613))
    add('common_phase_transfer','author-transfer',request([cmath.exp(.817j)*z for z in v],[-.713,.283,1.917],.613))
    add('nonlandmark_direct','author-transfer',request(v,[.713,1.183],direct=True))
    add('generic_unbalanced','author-transfer',request([.8j,-.6],[.113,.917,2.317],-.413))
    logs=[];circuits=0
    codes={'verified':0,'verification_failed':1,'invalid_input':2,'unsupported':3,'execution_failed':4}
    with tempfile.TemporaryDirectory(prefix='mqc-interference-author-') as tmp:
        copy=Path(tmp)/PACKAGE.name;shutil.copytree(PACKAGE,copy)
        for case in cases:
            text=case['raw_request'] if case['raw_request'] is not None else json.dumps(case['request'],allow_nan=False)
            proc=subprocess.run([sys.executable,str(copy/'scripts/interference.py')],input=text,text=True,capture_output=True,cwd=tmp,timeout=60)
            out=json.loads(proc.stdout)
            assert proc.returncode==codes[case['expected_status']] and out['status']==case['expected_status'],(case['name'],proc.stdout,proc.stderr)
            assert not proc.stderr and out['runtime']['python'].startswith('3.12.')
            if out['status']=='verified':
                q=case['request'];expected=oracle(q)
                assert out['versions']['flagquantum']=='0.3.1' and out['versions']['torch'].split('+')[0]=='2.13.0'
                assert len(expected)==len(out['records'])
                for (v,p),actual in zip(expected,out['records']):
                    np.testing.assert_allclose([complex(*z) for z in actual['statevector']],v,rtol=0,atol=2e-12)
                    np.testing.assert_allclose(actual['probabilities'],p,rtol=0,atol=2e-12)
                    assert actual['shape']==[1,2] and actual['state_dtype']=='torch.complex128' and actual['probability_dtype']=='torch.float64' and actual['device']=='cpu'
                circuits+=len(expected)
                if case['name']=='sparse_extrema':
                    assert out['fringe']['continuous_p0_max']>out['fringe']['sampled_p0_max']
                    assert out['fringe']['continuous_p0_min']<out['fringe']['sampled_p0_min']
                if case['name']=='complex_conjugate':assert out['records'][0]['probabilities'][0]<1e-12
                if case['name'].startswith('absent_'):assert out['fringe']['relative_phase_identifiable'] is False
            logs.append({**case,'actual_exit_code':proc.returncode,'actual_stdout':out,'actual_stderr':proc.stderr,'passed':True})
    a=next(x['actual_stdout'] for x in logs if x['name']=='nonlandmark_complex_scan')
    b=next(x['actual_stdout'] for x in logs if x['name']=='common_phase_transfer')
    for x,y in zip(a['records'],b['records']):np.testing.assert_allclose(x['probabilities'],y['probabilities'],rtol=0,atol=2e-12)
    report={'skill':PACKAGE.name,'version':'0.1.0','status':'author verified; independent agent evidence separate','evaluator_role':'author/conductor','environment':{'python':platform.python_version(),'platform':platform.platform(),'numpy':np.__version__},'package_sha256':hashes,'passed':len(logs),'counts':dict(Counter(x['category'] for x in logs)),'actual_flagquantum_circuits':circuits,'reference':'Independent NumPy matrix product H D(-delta) D(phi) applied to the declared state, separate from helper scalar references and tensor execution','evaluated_at_utc':datetime.now(timezone.utc).isoformat(),'scientific_acceptance':'pending','reader_trial':'not run','cases':logs}
    if args.record:
        path=EVIDENCE/'author-report.json';assert not path.exists();path.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'passed':len(logs),'categories':report['counts'],'actual_flagquantum_circuits':circuits}))


if __name__=='__main__':main()
