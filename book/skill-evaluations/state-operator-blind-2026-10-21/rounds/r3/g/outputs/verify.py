import json, math, cmath, pathlib, sys
ROOT=pathlib.Path('/private/tmp/mqc-comparison-blind-r3/g')
OUT=ROOT/'outputs'
checks={}
for task in json.loads((ROOT/'tasks.json').read_text()):
    tid=task['id']; d=OUT/tid
    req=json.loads((d/'request.json').read_text()); got=json.loads((d/'stdout.json').read_text())
    assert req['a']==task['data']['a'] and req['b']==task['data']['b'], 'Arrays altered'
    assert req['basis_a']==req['basis_b']==['0','1']
    a=[complex(*v) for v in req['a']]; b=[complex(*v) for v in req['b']]
    na=sum(v.real*v.real+v.imag*v.imag for v in a)
    nb=sum(v.real*v.real+v.imag*v.imag for v in b)
    v={'squared_norm_a':na,'squared_norm_b':nb,'arrays_preserved':True,'basis_assertion_checked':True}
    exitcode=json.loads((d/'execution.json').read_text())['exit_code']
    if abs(na-1)>1e-12 or abs(nb-1)>1e-12:
        assert got['status']=='invalid_input' and exitcode==2
        v.update(expected_status='invalid_input',reason='Supplied state is nonunit; no normalization or comparison substituted.')
    else:
        # Independent minimization using overlap angle and cancellation-sensitive identity as cross-check.
        overlap=sum(x.conjugate()*y for x,y in zip(a,b))
        angle=-cmath.phase(overlap)
        z=cmath.rect(1,angle)
        direct=math.sqrt(sum((x-z*y).real**2+(x-z*y).imag**2 for x,y in zip(a,b)))
        identity=math.sqrt(max(0,na+nb-2*abs(overlap)))
        raw=math.sqrt(sum(abs(x-y)**2 for x,y in zip(a,b)))
        assert abs(direct-got['decision_residual'])<1e-14
        assert abs(raw-got['raw_residual'])<1e-14
        assert abs(identity-direct)<1e-7
        expected='within_tolerance' if direct<=1e-10 else 'outside_tolerance'
        assert got['status']==expected
        assert exitcode==({'within_tolerance':0,'outside_tolerance':1}[expected])
        # Arbitrary common phases cannot improve the overlap-angle minimizer.
        sampled=min(math.sqrt(sum(abs(x-cmath.rect(1,2*math.pi*j/2048)*y)**2 for x,y in zip(a,b))) for j in range(2048))
        assert sampled>=direct-1e-14
        v.update(expected_status=expected,direct_angle_residual=direct,norm_identity_residual=identity,raw_residual=raw,phase_grid_minimum=sampled)
    assert got['runtime']=={'implementation':'cpython','python':'3.12.14'}
    v['passed']=True
    (d/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
    checks[tid]=v
print(json.dumps({'interpreter':sys.executable,'python':sys.version,'checks':checks,'passed':True},indent=2))
