"""Reproducible runner and independent standard-library verification, workspace B.

Reads only assigned inputs/skills and listed Python environment. Writes outputs only.
The Taylor exponential below does not import the unitary helper or Torch.
"""
import cmath
import hashlib
import json
import math
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs'
PYTHON = '/private/tmp/mqc-writing-venv/bin/python'
TASKS = json.loads((ROOT / 'tasks.json').read_text())

def dump(path, obj):
    path.write_text(json.dumps(obj, indent=2, allow_nan=False) + '\n')

def run(folder, script, request):
    folder.mkdir(exist_ok=True)
    dump(folder / 'request.json', request)
    command = [PYTHON, str(ROOT / 'skills' / script)]
    start = time.perf_counter()
    proc = subprocess.run(command, input=(folder / 'request.json').read_text(),
                          text=True, capture_output=True, cwd=ROOT)
    elapsed = time.perf_counter() - start
    (folder / 'stdout.json').write_text(proc.stdout)
    (folder / 'stderr.txt').write_text(proc.stderr)
    dump(folder / 'execution.json', dict(command=command, cwd=str(ROOT),
         exit_code=proc.returncode, elapsed_seconds=elapsed,
         request_path=str(folder / 'request.json')))
    return json.loads(proc.stdout), proc.returncode

def z(pair):
    return complex(*pair)

def mat(raw):
    return [[z(x) for x in row] for row in raw]

def pairs(v):
    return [[x.real, x.imag] for x in v]

def matrix_pairs(m):
    return [pairs(row) for row in m]

def ident(n):
    return [[complex(i == j) for j in range(n)] for i in range(n)]

def scale(m, c):
    return [[c*x for x in row] for row in m]

def add(a, b):
    return [[x+y for x, y in zip(ar, br)] for ar, br in zip(a, b)]

def mm(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]

def mv(a, b):
    return [sum(x*y for x, y in zip(row, b)) for row in a]

def maxdiff(a, b):
    return max(abs(x-y) for x, y in zip(a, b))

def flat(m):
    return [x for row in m for x in row]

def exp_taylor(a):
    """Direct convergent power series, independent of Pauli/eigensolver references."""
    result = ident(len(a))
    term = ident(len(a))
    for k in range(1, 200):
        term = scale(mm(term, a), 1/k)
        result = add(result, term)
        if max(map(abs, flat(term))) < 1e-19:
            return result, k
    raise AssertionError('Taylor series did not converge')

def controlled(m):
    out = ident(4)
    for i in range(2):
        for j in range(2):
            out[i+2][j+2] = m[i][j]
    return out

def circuit_checks(data, u):
    """Compare every submitted circuit coordinate and probability with own arithmetic."""
    supplied = [z(x) for x in data['state']]
    inputs = {'supplied': supplied, 'zero': [1+0j, 0j], 'one': [0j, 1+0j]}
    checks = []
    for record in outputs[data['task_id']]['records']:
        path = record['path']
        label = record['input_label']
        if label == 'coherent-control':
            inp = [x/math.sqrt(2) for x in supplied]*2
            operator = controlled(u)
            if path == 'controlled-unrepaired':
                operator = controlled(mat(outputs[data['task_id']]['native_zyz_matrix']))
        else:
            inp = inputs[label]
            operator = u
            if path == 'native-zyz':
                operator = mat(outputs[data['task_id']]['native_zyz_matrix'])
        expected = mv(operator, inp)
        actual = [z(x) for x in record['statevector']]
        err = maxdiff(actual, expected)
        probability_err = maxdiff(record['probabilities'], [abs(x)**2 for x in expected])
        check = dict(path=path, input_label=label, coordinate_max_absolute=err,
                     probability_max_absolute=probability_err,
                     passed=max(err, probability_err) <= data['atol'])
        if path == 'native-zyz':
            full = [z(x) for x in record['diagnostic_phase_corrected_state']]
            check['diagnostic_full_coordinate_max_absolute'] = maxdiff(full, mv(u, inp))
            check['passed'] &= check['diagnostic_full_coordinate_max_absolute'] <= data['atol']
        checks.append(check)
    assert all(c['passed'] for c in checks)
    return checks

if sys.version_info[:2] != (3, 12):
    raise RuntimeError('Use explicitly selected CPython 3.12')

manifest = {}
for p in ROOT.rglob('*'):
    if p.is_file() and OUT not in p.parents:
        manifest[str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
dump(OUT / 'input-sha256.json', manifest)

probe_cmd = [PYTHON, '-c', 'import sys,platform,torch,flagquantum,json; print(json.dumps(dict(python=sys.version,implementation=platform.python_implementation(),torch=torch.__version__,flagquantum=flagquantum.__version__)))']
t0 = time.perf_counter()
probe = subprocess.run(probe_cmd, capture_output=True, text=True)
dump(OUT / 'runtime-probe.json', dict(command=probe_cmd, stdout=probe.stdout,
     stderr=probe.stderr, exit_code=probe.returncode, elapsed_seconds=time.perf_counter()-t0))

outputs = {}
codes = {}
for task in TASKS:
    skill_script = ('reproduce-qubit-interference/scripts/interference.py'
                    if task['id'] == 'B4' else 'translate-unitary-evolution/scripts/unitary.py')
    outputs[task['id']], codes[task['id']] = run(OUT / task['id'], skill_script, task['data'])

results = []
for task in TASKS:
    tid = task['id']
    d = task['data']
    result = outputs[tid]
    selected = ['reproduce-qubit-interference' if tid == 'B4' else 'translate-unitary-evolution']
    verification = {}
    claims = {}
    if tid == 'B1':
        exponent = scale(mat(d['generator']['matrix']), d['time']['value'])
        u, count = exp_taylor(scale(exponent, -1j))
        verification = dict(method='independent standard-library power-series matrix exponential',
                            taylor_terms=count,
                            dimensionless_exponent=matrix_pairs(exponent),
                            independent_unitary=matrix_pairs(u),
                            matrix_max_absolute=maxdiff(flat(u), flat(mat(result['unitary']))))
        assert verification['matrix_max_absolute'] <= d['atol']
        e0 = sum(exponent[i][i] for i in range(2))/2
        verification['trace_shift_exponent'] = [e0.real, e0.imag]
        verification['trace_shift_phase'] = pairs([cmath.exp(-1j*e0)])[0]
        verification['circuit_checks'] = circuit_checks(dict(d, task_id=tid), u)
        claims = dict(disposition='reproduced_with_full_complex_coordinates',
                      explanation='E=-0.413 K; trace contribution e0=-0.826 gives scalar phase exp(+0.826i). Native ZYZ alone implements V; retaining the returned phase recovers U as diagnostic arithmetic.')
        explanation = 'Signed time was preserved. The original generator is 2I+sigma_y; no energy-zero shift was applied. Full complex direct and phase-corrected coordinates passed independent checks.'
    elif tid == 'B2':
        selected.append('compare-quantum-states-and-operators')
        theta = d['angle']['value']
        u, count = exp_taylor([[0j, -1j*theta/2], [-1j*theta/2, 0j]])
        verification = dict(method='independent standard-library matrix exponential and full controlled-block witness',
                            taylor_terms=count, independent_unitary=matrix_pairs(u),
                            matrix_max_absolute=maxdiff(flat(u), flat(mat(result['unitary']))),
                            circuit_checks=circuit_checks(dict(d, task_id=tid), u), comparisons={})
        assert verification['matrix_max_absolute'] <= d['atol']
        for mode in ['coordinates', 'global-phase', 'controlled']:
            req = dict(kind='unitary', mode=mode, basis_a=d['basis'], basis_b=d['basis'],
                       a=result['unitary'], b=matrix_pairs(ident(2)), atol=d['atol'])
            comparison, code = run(OUT / tid / ('compare-' + mode),
                                  'compare-quantum-states-and-operators/scripts/compare.py', req)
            expected_code = 0 if mode == 'global-phase' else 1
            assert code == expected_code
            verification['comparisons'][mode] = dict(status=comparison['status'], exit_code=code,
                result_path=str(OUT / tid / ('compare-' + mode) / 'stdout.json'))
        minus_i = scale(ident(2), -1)
        verification['distance_to_minus_identity_max_absolute'] = maxdiff(flat(u), flat(minus_i))
        supplied = [z(x) for x in d['state']]
        plus_input = [x/math.sqrt(2) for x in supplied]*2
        actual = mv(controlled(u), plus_input)
        unchanged = plus_input
        overlap = sum(a.conjugate()*b for a, b in zip(actual, unchanged))
        norm_actual = sum(abs(x)**2 for x in actual)
        norm_identity = sum(abs(x)**2 for x in unchanged)
        verification['coherent_input_witness'] = dict(input=pairs(plus_input), controlled_rotation_output=pairs(actual),
            identity_output=pairs(unchanged), overlap=pairs([overlap])[0],
            ray_distance=math.sqrt(max(0, norm_actual+norm_identity-2*abs(overlap))),
            explanation='For exact 2pi, control |+> changes to |-> while target remains the same ray; identity retains |+>. The two outputs are orthogonal.')
        # One global phase cannot remove the diag(I,-I) branch sign: trace is zero,
        # so Frobenius distance to I4 is sqrt(4+4)=sqrt(8).
        c = sum(controlled(u)[i][i].conjugate() for i in range(4))
        controlled_norm2 = sum(abs(x)**2 for x in flat(controlled(u)))
        verification['independent_controlled_aligned_frobenius'] = math.sqrt(controlled_norm2+4-2*abs(c))
        claims = dict(claim=task['claim'], disposition='refuted_as_full_operation',
            isolated_operator_ray='equivalent to identity up to one global phase -1',
            coherent_control='C(Rx(2pi)) approximately diag(1,1,-1,-1), inequivalent to I4 even up to a whole-operation phase',
            explanation='Active spin-1/2 Rx(2pi)=-I. The canonical factorization alpha=0 does not imply V=I: here V itself is -I.')
        explanation = 'Isolated operator-ray equivalence passes; coordinate equality and coherent controlled-operation equivalence fail. Full controlled Frobenius residual is approximately sqrt(8).'
    elif tid == 'B3':
        h = mat(d['generator']['matrix'])
        norm = max(map(abs, flat(h)))
        discrepancy = max(abs(h[i][j]-h[j][i].conjugate()) for i in range(2) for j in range(2))
        verification = dict(method='independent raw-scale Hermiticity admission before time conversion',
            generator_max_absolute_J=norm, hermiticity_max_absolute_J=discrepancy,
            hermiticity_allowance_J=1e-12*norm, relative_discrepancy=discrepancy/norm,
            admitted=False, time_seconds=d['time']['value']*1e-9,
            zero_time_endpoint_is_identity=True)
        assert discrepancy > 1e-12*norm
        assert codes[tid] == 2 and result['status'] == 'invalid_input'
        claims = dict(disposition='generator_rejected', explanation='The 1e-24 J off-diagonal has no conjugate partner. Relative discrepancy is 1, far above 1e-12. A zero-time identity endpoint does not validate a Hamiltonian.')
        explanation = 'Rejected without symmetrizing or discarding the tiny physical scale. This is invalid Hamiltonian input, not evidence of an unequal endpoint or failed simulator.'
    else:
        alpha, beta = map(z, d['state'])
        n = abs(alpha)**2+abs(beta)**2
        pointchecks = []
        for phi, record in zip(d['phase_radians'], result['records']):
            # Apply three matrices chronologically to preserve complex coordinates.
            state = [alpha, beta]
            phase = [[1+0j, 0j], [0j, cmath.exp(1j*phi)]]
            analyzer = [[1+0j, 0j], [0j, cmath.exp(-1j*d['readout']['delta_radians'])]]
            hadamard = scale([[1+0j, 1+0j], [1+0j, -1+0j]], 1/math.sqrt(2))
            expected = mv(hadamard, mv(analyzer, mv(phase, state)))
            probabilities = [abs(x)**2 for x in expected]
            cross = (alpha.conjugate()*cmath.exp(1j*(phi-d['readout']['delta_radians']))*beta).real
            formula = [n/2+cross, n/2-cross]
            err = maxdiff(expected, [z(x) for x in record['statevector']])
            prob_err = maxdiff(probabilities, record['probabilities'])
            formula_err = maxdiff(formula, record['probabilities'])
            assert max(err, prob_err, formula_err) <= d['atol']
            pointchecks.append(dict(phase_radians=phi, independent_state=pairs(expected),
                independent_probabilities=probabilities, independent_scalar_formula=formula,
                coordinate_max_absolute=err, probability_max_absolute=prob_err,
                formula_max_absolute=formula_err, passed=True))
        verification = dict(method='standard-library chronological D(phi),D(-delta),H matrix action plus scalar Born expansion',
            input_squared_norm=n, point_checks=pointchecks,
            continuous_p0_min=n/2-abs(alpha)*abs(beta), continuous_p0_max=n/2+abs(alpha)*abs(beta),
            sampled_p0_min=min(x['independent_probabilities'][0] for x in pointchecks),
            sampled_p0_max=max(x['independent_probabilities'][0] for x in pointchecks))
        claims = dict(disposition='specified_ideal_scan_reproduced', explanation='Actual simulator probabilities match chronological complex-amplitude calculation and scalar interference formula at both supplied phases. Sparse sampled extrema differ from analytic continuous extrema.')
        explanation = 'Used the prepared-state interference skill for prepare -> D(phi) -> D(-0.19) -> H -> computational readout. No generator or Euler interpretation was introduced.'
    verification['passed'] = True
    dump(OUT / tid / 'independent-verification.json', verification)
    dump(OUT / tid / 'claim-disposition.json', claims)
    (OUT / tid / 'explanation.txt').write_text(explanation+'\n')
    results.append(dict(id=tid, selected_skills=selected,
        chosen_context=('prepared pure qubit phase scan with specified phase-h analyzer' if tid == 'B4'
                        else 'isolated operator ray; full coherently controlled operation; coordinates retain phase' if tid == 'B2'
                        else d['context']), clarification_question=None, status=result['status'],
        evidence_paths=[str(OUT / tid), str(OUT / 'runtime-probe.json'), str(OUT / 'run_all.py')],
        verification=verification, claim_disposition=claims,
        limitations=['Ideal deterministic numerical profile; no noisy/hardware or statistical inference.',
                     'Floating-point checks at declared tolerance do not establish an exact general theorem.'] +
                    (['Invalid raw generator; no admissible Hamiltonian evolution was simulated.'] if tid == 'B3' else [])))

for rel, digest in manifest.items():
    assert hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == digest, rel
dump(OUT / 'input-integrity.json', dict(unchanged=True, file_count=len(manifest), algorithm='SHA-256'))
dump(OUT / 'results.json', results)
print(json.dumps(dict(results=str(OUT / 'results.json'), tasks=[dict(id=r['id'], status=r['status']) for r in results], input_files_unchanged=True)))
