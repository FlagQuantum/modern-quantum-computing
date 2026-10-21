#!/usr/bin/env python3
"""Author evaluation of the frozen comparison helper; no independent agent claim."""
import argparse
from collections import Counter
import cmath
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
from math import cos, sin, sqrt, pi
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

import flagquantum as fq
import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT/'skills/compare-quantum-states-and-operators'
EVIDENCE = ROOT/'book/skill-evaluations/state-operator-v0.1.1'


def encode(x):
    a = np.asarray(x, dtype=np.complex128)
    if a.ndim == 1:
        return [[float(z.real), float(z.imag)] for z in a]
    return [encode(row) for row in a]


def request(a, b, kind='state', mode='global-phase', **kw):
    basis = ['0','1'] if len(a) == 2 else ['00','01','10','11']
    return dict(kind=kind, mode=mode, basis_a=basis, basis_b=basis,
                a=encode(a), b=encode(b), **kw)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', action='store_true')
    args = parser.parse_args()
    freeze = json.loads((EVIDENCE/'package-freeze.json').read_text())
    current = {str(p.relative_to(PACKAGE)): hashlib.sha256(p.read_bytes()).hexdigest()
               for p in sorted(PACKAGE.rglob('*')) if p.is_file() and '__pycache__' not in str(p)}
    assert current == freeze['sha256'], 'Frozen package changed: preserve evidence and establish a new evaluation version'
    cases = []

    def add(name, category, data, status, residual=None):
        cases.append(dict(name=name, category=category, request=data, expected_status=status, expected_residual=residual))

    plus = np.array([1,1])/sqrt(2)
    I = np.eye(2); Z = np.diag([1,-1])
    add('same_state', 'normal', request(plus,plus), 'within_tolerance', 0)
    add('state_global_i', 'normal', request(plus,1j*plus), 'within_tolerance', 0)
    add('coordinates_retain_i', 'normal', request(plus,1j*plus,mode='coordinates'), 'outside_tolerance', sqrt(2))
    add('relative_sign_same_probabilities', 'normal', request(plus,plus*[1,-1]), 'outside_tolerance', sqrt(2))
    add('isolated_minus_I', 'normal', request(I,-I,'unitary'), 'within_tolerance',0)
    add('columns_are_not_operator_equivalence', 'normal', request(I,Z,'unitary'), 'outside_tolerance',2)
    add('controlled_target_phase', 'normal', request(I,-I,'unitary','controlled'), 'outside_tolerance',sqrt(8))
    add('controlled_equal', 'normal', request(Z,Z,'unitary','controlled'), 'within_tolerance',0)
    add('zero_overlap_poles','boundary',request([1,0],[0,1]),'outside_tolerance',sqrt(2))
    add('four_coordinate_state','boundary',request([0,0,1,0],[0,0,-1,0]),'within_tolerance',0)
    add('four_dimensional_unitary','boundary',request(np.eye(4),1j*np.eye(4),'unitary'),'within_tolerance',0)
    # Exact binary64 residual on either side of the inclusive decision boundary.
    angle = 2**-20
    a = np.array([1,0]); b = np.array([cos(angle),sin(angle)])
    r = float(np.linalg.norm(a-b))
    for name, threshold, status in [('inclusive',r,'within_tolerance'),('just_below',np.nextafter(r,0),'outside_tolerance'),('just_above',np.nextafter(r,np.inf),'within_tolerance')]:
        add(name,'boundary',request(a,b,mode='coordinates',atol=threshold),status,r)
    # A tiny overlap is valid but its phase is not a robust diagnostic.
    add('near_zero_overlap','boundary',request([1,0],[1e-13,sqrt(1-1e-26)]),'outside_tolerance',sqrt(2-2e-13))

    base=request(plus,plus)
    for name, changes, status in [
        ('zero_state',{'a':encode([0,0])},'invalid_input'),
        ('nonunit_state',{'a':encode([1,1])},'invalid_input'),
        ('mismatched_shape',{'b':encode([1,0,0,0])},'invalid_input'),
        ('missing_context',{'mode':None},'invalid_input'),
        ('unknown_mode',{'mode':'per-column'},'invalid_input'),
        ('boolean_coordinate',{'a':[[True,0],[0,0]]},'invalid_input'),
        ('string_coordinate',{'a':[['1',0],[0,0]]},'invalid_input'),
        ('bad_pair',{'a':[[1],[0,0]]},'invalid_input'),
        ('unsupported_density',{'kind':'density'},'unsupported'),
        ('basis_mismatch',{'basis_b':['1','0']},'unsupported'),
        ('negative_tolerance',{'atol':-1},'invalid_input'),
        ('too_loose_tolerance',{'atol':1},'invalid_input'),
        ('controlled_state',{'mode':'controlled'},'invalid_input'),
        ('extra_field',{'normalize':True},'invalid_input')]:
        data=deepcopy(base);data.update(changes);add(name,'error',data,status)
    missing=deepcopy(base);del missing['mode']
    add('absent_mode','error',missing,'invalid_input')
    add('nonunitary','error',request(I,[[1,1],[0,1]],'unitary'),'invalid_input')
    add('controlled_large_target','error',request(np.eye(4),np.eye(4),'unitary','controlled'),'unsupported')
    for name,text in [('nan','{"kind":NaN}'),('infinity','{"kind":Infinity}'),('syntax','{'),('duplicate','{"kind":"state","kind":"unitary"}')]:
        add(name,'error',None,'invalid_input');cases[-1]['raw_request']=text

    # Reused 0.1.0 transfer fixtures: regression, not new held-out evidence.
    v=np.array([1+2j,-3+4j])/sqrt(30)
    phi=0.731
    add('complex_nonlandmark_ray','transfer-regression',request(v,cmath.exp(1j*phi)*v),'within_tolerance',0)
    add('complex_nonlandmark_coordinates','transfer-regression',request(v,cmath.exp(1j*phi)*v,mode='coordinates'),'outside_tolerance',2*abs(sin(phi/2)))
    w=np.array([2-1j,1-2j,3j,-1+4j])/6
    add('complex_four_coordinate_ray','transfer-regression',request(w,-1j*w),'within_tolerance',0)
    # Nontrivial unitary and a target phase invisible in isolation but visible under control.
    t=.417
    U=np.array([[cos(t),-cmath.exp(-.29j)*sin(t)],[cmath.exp(.29j)*sin(t),cos(t)]])
    add('generic_unitary_phase','transfer-regression',request(U,cmath.exp(1j*phi)*U,'unitary'),'within_tolerance',0)
    add('generic_controlled_phase','transfer-regression',request(U,cmath.exp(1j*phi)*U,'unitary','controlled'),'outside_tolerance',sqrt(8-8*abs(cos(phi/2))))
    # Same probabilities, different complex relative phase; |<a,b>|=sqrt(1/2).
    add('complex_relative_phase','transfer-regression',request(plus,np.array([1,1j])/sqrt(2)),'outside_tolerance',sqrt(2-sqrt(2)))

    # Producing-program checks precede export: no implicit dtype widening/batch squeezing.
    assert version('flagquantum') == '0.3.1'
    opts=fq.ExecutionOptions(mode='statevector',backend='pytorch',device='cpu',precision='complex128',allow_backend_fallback=False,allow_approximate=False)
    framework=[]
    for angle in [0,pi/2,pi]:
        C=torch.eye(4,dtype=torch.complex128)
        C[2:,2:]*=cmath.exp(1j*angle)
        circuit=fq.Circuit(2,dtype=torch.complex128)
        circuit.h(0);circuit.unitary(0,1,unitary=C)
        result=fq.run(circuit,outputs=[fq.probabilities()],options=opts)
        actual=result.statevector();p=result.probabilities
        assert actual.shape==p.shape==(1,4) and actual.dtype==torch.complex128
        assert p.dtype==torch.float64 and actual.device.type==p.device.type=='cpu'
        assert torch.isfinite(actual).all() and torch.isfinite(p).all()
        assert abs(torch.vdot(actual[0],actual[0]).real.item()-1)<1e-12
        torch.testing.assert_close(p,actual.abs().square(),rtol=0,atol=1e-12)
        ref=np.array([1,0,cmath.exp(1j*angle),0])/sqrt(2)
        np.testing.assert_allclose(actual[0].numpy(),ref,rtol=0,atol=1e-12)
        add('flagquantum_controlled_'+str(angle),'normal',request(ref,actual[0].numpy(),mode='coordinates'),'within_tolerance',0)
        framework.append({'angle':angle,'shape':list(actual.shape),'dtype':str(actual.dtype),'probabilities':p.tolist()})

    logs=[]
    codes={'within_tolerance':0,'outside_tolerance':1,'invalid_input':2,'unsupported':3}
    with tempfile.TemporaryDirectory(prefix='mqc-comparison-eval-') as tmp:
        copied=Path(tmp)/PACKAGE.name;shutil.copytree(PACKAGE,copied)
        for case in cases:
            payload=case.get('raw_request',json.dumps(case['request'],allow_nan=False))
            proc=subprocess.run([sys.executable,str(copied/'scripts/compare.py')],input=payload,text=True,capture_output=True,cwd=tmp,timeout=10)
            output=json.loads(proc.stdout)
            assert output['runtime']['implementation']=='cpython'
            assert output['runtime']['python'].startswith('3.12.')
            assert output['contract_version']=='0.1.1'
            assert output['status']==case['expected_status'],(case['name'],output)
            assert proc.returncode==codes[case['expected_status']] and not proc.stderr,(case['name'],proc.stderr)
            expected=case['expected_residual']
            if expected is not None:
                assert abs(output['decision_residual']-expected)<=2e-12,(case['name'],output,expected)
                z=output['alignment_multiplier_on_b']
                assert abs(complex(*z).__abs__()-1)<2e-12
            if case['name']=='zero_overlap_poles':
                assert output['phase_identifiable'] is False and output['alignment_multiplier_on_b']==[1,0]
            if case['name']=='state_global_i':
                assert abs(complex(*output['alignment_multiplier_on_b'])+1j)<1e-12
            logs.append({**case,'actual_exit_code':proc.returncode,'actual_output':output,'passed':True})
    report={
        'skill':PACKAGE.name,'version':'0.1.1','status':'author-verified prototype',
        'evaluated_at_utc':datetime.now(timezone.utc).isoformat(),
        'evaluator_role':'authoring agent; programmatic CLI evaluation',
        'independent_agent_forward_test':'not run','independent_acceptance':'pending','reader_trial':'not run',
        'held_out_scope':'Six reused transfer fixtures, now regression only; blind agent evidence is recorded separately',
        'environment':{'python':platform.python_version(),'platform':platform.platform(),'flagquantum':version('flagquantum'),'torch':version('torch'),'numpy':version('numpy')},
        'package_sha256':current,'counts':dict(Counter(c['category'] for c in cases)),
        'passed':len(logs),'false_successes':0,'incorrect_abstentions':0,'unexpected_exceptions':0,
        'framework_runs':framework,'cases':logs}
    if args.record:
        destination=EVIDENCE/'author-report.json'
        assert not destination.exists(),'Preserve original execution evidence; do not overwrite it'
        destination.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'passed':len(logs),'categories':report['counts'],'framework_runs':len(framework),'independent_acceptance':'pending'},sort_keys=True))


if __name__=='__main__':main()
