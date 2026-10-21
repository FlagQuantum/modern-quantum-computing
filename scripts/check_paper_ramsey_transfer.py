#!/usr/bin/env python3
"""Replay published transfer evidence; this is not a new blind evaluation."""
import cmath
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT/'book/skill-evaluations/paper-ramsey-transfer-2026-10-21'
SKILLS = ROOT/'skills'
sys.path.insert(0, str(ROOT/'examples/integration'))
from paper_ramsey_transfer import execute


def load(path):
    return json.loads(path.read_text())


def decode(v):
    return [complex(*z) for z in v]


def scalar_reference(state, phi, delta):
    a, b = state
    z = cmath.exp(1j*(phi-delta))*b
    return [(a+z)/math.sqrt(2), (a-z)/math.sqrt(2)]


def check_vector(actual, reference):
    assert len(actual) == len(reference) == 2
    assert max(abs(a-b) for a,b in zip(decode(actual),reference)) <= 1e-10


def identify(q):
    if 'coordinates' in q:
        return 'translate-complex-linear-algebra', 'algebra.py'
    if q.get('kind') in ('state','unitary') and 'mode' in q:
        return 'compare-quantum-states-and-operators', 'compare.py'
    if q.get('profile') == 'ideal-pure-single-qubit':
        return 'reproduce-qubit-interference', 'interference.py'
    if q.get('task') in ('evolve','rotation','factor'):
        return 'translate-unitary-evolution', 'unitary.py'
    raise AssertionError(q)


def verify_evidence():
    for name, sha in load(EVIDENCE/'evidence-manifest.json')['sha256'].items():
        assert hashlib.sha256((EVIDENCE/name).read_bytes()).hexdigest() == sha, name
    reg = load(EVIDENCE/'registration.json')
    assert hashlib.sha256((EVIDENCE/'reference-key.json').read_bytes()).hexdigest() == reg['frozen_reference_sha256']
    for name, sha in reg['packet_sha256'].items():
        if name == 'paper.pdf':
            assert sha == reg['source']['sha256']
            continue
        path = ROOT/'examples/integration/four_skill_interference.py' if name == 'four_skill_interference.py' else ROOT/name
        assert hashlib.sha256(path.read_bytes()).hexdigest() == sha, name
    for agent in 'abc':
        assert hashlib.sha256((EVIDENCE/agent/'task.txt').read_bytes()).hexdigest() == reg['task_sha256'][agent]
    # Grade the actual final coordinates, not just a claimed passed flag.
    a = load(EVIDENCE/'a/result.json')
    assert a['status'] == 'verified' and len(a['records']) == 6
    for row in a['records']:
        x = row['source_x_in_pi_units']
        p = cmath.exp(1j*math.pi*x)
        reference = [(1-p)/2, (1+p)/2]
        check_vector(row['helper_statevector'], reference)
        check_vector(row['continuous_statevector'], reference)
        assert abs(row['helper_probabilities'][0]-(1-math.cos(math.pi*x))/2) <= 1e-10
    b = load(EVIDENCE/'b/run/report.json')
    theta = 2*math.pi*125e6*.83e-9
    for row in b['outputs']:
        p = cmath.exp(1j*(theta+row['phase_radians']))
        reference = [cmath.exp(-.17j)*(1-p)/2, cmath.exp(-.17j)*(1+p)/2]
        check_vector(row['statevector'], reference)
        check_vector(row['staged_statevector'], reference)
        assert abs(row['probabilities'][0]-(1-math.cos(theta+row['phase_radians']))/2) <= 1e-10
    c = load(EVIDENCE/'c/result.json')
    assert 'reject' in c['claims']['C1']['disposition'].lower()
    assert all(c['claims'][name]['disposition'].startswith('rejected') for name in ('C2','C3'))
    evaluation = load(EVIDENCE/'evaluation.json')
    assert evaluation['blind_actual_flagquantum_circuits'] == 65
    assert evaluation['blind_helper_calls'] == 46
    # Replay all independent-agent and author-negative helper calls. Keep archived
    # logs immutable; a fresh mismatch cannot rewrite their original status.
    total, replayed, circuits = 0, 0, 0
    for request in sorted(EVIDENCE.rglob('request.json')):
        old_stdout = request.parent/'stdout.json'
        if not old_stdout.exists():
            continue
        q, old = load(request), load(old_stdout)
        skill, script = identify(q)
        total += 1
        if 'author' == request.relative_to(EVIDENCE).parts[0]:
            continue  # The complete example is independently rerun below.
        proc = subprocess.run([sys.executable,str(SKILLS/skill/'scripts'/script)],
                              input=json.dumps(q),capture_output=True,text=True,timeout=120)
        fresh = json.loads(proc.stdout)
        expected_exit = 1 if old['status'] in ('outside_tolerance','verification_failed') else 0
        assert proc.returncode == expected_exit and not proc.stderr, (str(request),proc.stdout,proc.stderr)
        assert fresh['status'] == old['status']
        assert fresh['runtime']['python'].startswith('3.12.')
        replayed += 1
        circuits += fresh.get('actual_flagquantum_circuits',len(fresh.get('records',[])) if script == 'interference.py' else 0)
        if script == 'interference.py':
            state = decode(q['state'])
            for row, phi in zip(fresh['records'], q['phase_radians']):
                reference = scalar_reference(state,phi,q['readout'].get('delta_radians',0))
                check_vector(row['statevector'],reference)
                assert max(abs(p-abs(z)**2) for p,z in zip(row['probabilities'],reference)) <= 1e-10
    assert (total,replayed,circuits) == (90,51,59), (total,replayed,circuits)
    return circuits


def main():
    assert sys.version_info[:2] == (3,12)
    circuits = verify_evidence()
    with tempfile.TemporaryDirectory(prefix='mqc-paper-transfer-replay-') as temporary:
        result = execute(Path(temporary)/'fresh', SKILLS)
    assert result['actual_flagquantum_circuits'] == 32
    assert result['helper_calls'] == 39
    print(json.dumps({'archived_blind_task_dispositions':5,'fresh_example_circuits':32,
                      'fresh_archived_helper_circuits':circuits,'new_blind_tests':0,
                      'scientific_acceptance':'pending'}))

if __name__ == '__main__':
    main()
