import json, math, pathlib
O=pathlib.Path(__file__).resolve().parent
report={}
for ident in ('A1','A2','A3'):
    q=json.loads((O/f'{ident}.request.json').read_text())
    r=json.loads((O/f'{ident}.stdout.json').read_text())
    e=json.loads((O/f'{ident}.execution.json').read_text())
    a=[complex(*v) for v in q['a']]; b=[complex(*v) for v in q['b']]
    na=sum(v.real*v.real+v.imag*v.imag for v in a)
    nb=sum(v.real*v.real+v.imag*v.imag for v in b)
    d={'squared_norm_a':na,'squared_norm_b':nb}
    if ident=='A1':
        raw=math.sqrt(sum(abs(x-y)**2 for x,y in zip(a,b)))
        assert abs(na-1)<=1e-12 and abs(nb-1)<=1e-12
        assert abs(raw-r['decision_residual'])<1e-14
        assert r['mode']=='coordinates' and r['status']=='outside_tolerance' and e['exit_code']==1 and raw>q['atol']
        d['independent_raw_residual']=raw
    elif ident=='A2':
        overlap=sum(x.conjugate()*y for x,y in zip(a,b))
        z=overlap.conjugate()/abs(overlap)
        residual=math.sqrt(sum(abs(x-z*y)**2 for x,y in zip(a,b)))
        d.update(overlap=[overlap.real,overlap.imag],independent_aligned_residual=residual)
        assert abs(residual-r['decision_residual'])<1e-14
        assert abs(na-1)<=1e-12 and abs(nb-1)<=1e-12
        assert r['status']=='outside_tolerance' and e['exit_code']==1 and residual>q['atol']
    else:
        assert abs(nb-1)>1e-12
        assert r['status']=='invalid_input' and e['exit_code']==2
    assert (O/f'{ident}.stderr.txt').read_text()==''
    d['verification']='passed'; report[ident]=d
print(json.dumps(report,indent=2))
