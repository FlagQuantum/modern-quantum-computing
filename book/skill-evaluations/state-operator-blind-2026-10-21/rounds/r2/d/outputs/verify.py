"""Independent checks of saved comparison artifacts using only Python stdlib."""
import cmath
import json
import math
from pathlib import Path

root = Path(__file__).resolve().parent
checks = []
for task_id in ('D1', 'D2'):
    folder = root / task_id
    req = json.loads((folder / 'request.json').read_text())
    got = json.loads((folder / 'stdout.json').read_text())
    a = [complex(*v) for v in req['a']]
    b = [complex(*v) for v in req['b']]
    norm_a_sq = math.fsum(abs(x)**2 for x in a)
    norm_b_sq = math.fsum(abs(x)**2 for x in b)
    c = sum(x.conjugate()*y for x, y in zip(a, b))
    z = complex(*got['alignment_multiplier_on_b'])
    residual = math.sqrt(math.fsum(abs(x-z*y)**2 for x, y in zip(a,b)))
    raw = math.sqrt(math.fsum(abs(x-y)**2 for x,y in zip(a,b)))
    minimum_sq = norm_a_sq + norm_b_sq - 2*abs(c)
    phase_grid = [math.sqrt(math.fsum(abs(x-cmath.exp(1j*t)*y)**2 for x,y in zip(a,b))) for t in [0, .1, .7, 1.2, 2.5, 4.8]]
    assert abs(norm_a_sq-1) <= 1e-12 and abs(norm_b_sq-1) <= 1e-12
    assert abs(abs(z)-1) <= 1e-14
    assert abs(residual-got['decision_residual']) <= 1e-14
    assert abs(raw-got['raw_residual']) <= 1e-14
    assert abs(residual**2-minimum_sq) <= 1e-14
    assert (residual<=req['atol']) == (got['status']=='within_tolerance')
    if task_id == 'D1':
        assert got['phase_identifiable'] and residual <= 1e-10
        ratios = [x/y for x,y in zip(a,b) if y]
        assert all(abs(r-z) <= 1e-14 for r in ratios)
    else:
        assert c == 0j and not got['phase_identifiable']
        assert z == 1 and residual > 1e-10
        assert all(abs(r-math.sqrt(2)) <= 1e-14 for r in phase_grid)
    checks.append(dict(id=task_id,passed=True,norm_a_squared=norm_a_sq,norm_b_squared=norm_b_sq,overlap=[c.real,c.imag],recomputed_residual=residual,minimum_squared_distance_formula=minimum_sq,sampled_phase_residuals=phase_grid))
print(json.dumps({'passed':True,'checks':checks},indent=2))
