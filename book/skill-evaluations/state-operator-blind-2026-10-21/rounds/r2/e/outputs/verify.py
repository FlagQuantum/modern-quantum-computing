import json, math
from pathlib import Path
root=Path(__file__).resolve().parent
report={}
for d in sorted(root.iterdir()):
    if not d.is_dir() or not (d/'request.json').exists(): continue
    req=json.loads((d/'request.json').read_text())
    result=json.loads((d/'stdout.json').read_text())
    a=[[complex(*x) for x in row] for row in req['a']]
    b=[[complex(*x) for x in row] for row in req['b']]
    n=len(a)
    grams=[]
    for u in (a,b):
        grams.append(max(abs(sum(u[k][i].conjugate()*u[k][j] for k in range(n))-(i==j)) for i in range(n) for j in range(n)))
    if req['mode']=='controlled':
        def extend(u):
            return [[complex(i==j) if i<2 and j<2 else (u[i-2][j-2] if i>=2 and j>=2 else 0j) for j in range(4)] for i in range(4)]
        a,b=extend(a),extend(b);n=4
    pivot=max(((i,j) for i in range(n) for j in range(n)),key=lambda x:abs(b[x[0]][x[1]]))
    phase=a[pivot[0]][pivot[1]]/b[pivot[0]][pivot[1]]
    phase/=abs(phase)
    pivot_residual=math.sqrt(sum(abs(a[i][j]-phase*b[i][j])**2 for i in range(n) for j in range(n)))
    z=complex(*result['alignment_multiplier_on_b'])
    aligned=math.sqrt(sum(abs(a[i][j]-z*b[i][j])**2 for i in range(n) for j in range(n)))
    raw=math.sqrt(sum(abs(a[i][j]-b[i][j])**2 for i in range(n) for j in range(n)))
    decision=raw if req['mode']=='coordinates' else aligned
    assert all(v<=1e-12 for v in grams)
    assert abs(aligned-result['aligned_residual'])<=1e-14
    assert abs(raw-result['raw_residual'])<=1e-14
    assert (decision<=req['atol'])==(result['status']=='within_tolerance')
    report[d.name]={'passed':True,'max_gram_errors':grams,'pivot_phase':[phase.real,phase.imag],'pivot_phase_residual':pivot_residual,'recomputed_raw':raw,'recomputed_aligned':aligned,'decision':decision}
print(json.dumps(report,indent=2))
