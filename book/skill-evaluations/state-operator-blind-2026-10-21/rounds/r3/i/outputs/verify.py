import json, math, pathlib, hashlib, sys
ROOT=pathlib.Path('/private/tmp/mqc-comparison-blind-r3/i'); OUT=ROOT/'outputs'
tasks={t['id']:t for t in json.loads((ROOT/'tasks.json').read_text())}
results=json.loads((OUT/'results.json').read_text()); checks=[]
for r in results:
    ident=r['id']; t=tasks[ident]; d=t['data']; evidence={}
    if ident in ('I1','I2','I3'):
        req=json.loads((OUT/ident/'request.json').read_text()); actual=json.loads((OUT/ident/'stdout.json').read_text()); execution=json.loads((OUT/ident/'execution.json').read_text())
        assert all(req[k]==v for k,v in d.items())
        assert req['mode']=='global-phase' and req['atol']==1e-10
        assert actual['runtime']=={'implementation':'cpython','python':'3.12.14'}
        assert (OUT/ident/'stderr.txt').read_text()==''
        if ident=='I1':
            assert req['basis_a']!=req['basis_b']
            assert actual['status']=='unsupported' and execution['exit_code']==3
            assert 'residual' not in actual and 'decision_residual' not in actual
            evidence={'basis_labels_preserved':True,'unsupported_is_not_inequality':True,'helper_reason':actual['reason']}
        else:
            a=[complex(*z) for z in d['a']]; b=[complex(*z) for z in d['b']]
            # Independent calculation: phase from the argument of summed overlaps;
            # Euclidean norm via hypot, without importing helper code.
            c=sum(x.conjugate()*y for x,y in zip(a,b))
            theta=-math.atan2(c.imag,c.real)
            z=complex(math.cos(theta),math.sin(theta))
            norms=[math.hypot(*(v for x in arr for v in (x.real,x.imag))) for arr in (a,b)]
            diffs=[x-z*y for x,y in zip(a,b)]
            residual=math.hypot(*(v for x in diffs for v in (x.real,x.imag)))
            raw=math.hypot(*(v for x,y in zip(a,b) for v in ((x-y).real,(x-y).imag)))
            assert all(abs(n*n-1)<=1e-12 for n in norms)
            assert abs(residual-actual['aligned_residual'])<=1e-14
            assert abs(raw-actual['raw_residual'])<=1e-14
            decision='within_tolerance' if residual<=1e-10 else 'outside_tolerance'
            assert actual['status']==decision and execution['exit_code']==(0 if decision=='within_tolerance' else 1)
            assert actual['status']!=t['cached_result']['status']
            evidence={'independent_method':'atan2 phase and hypot distance, no helper imports','squared_norms':[n*n for n in norms],'overlap':[c.real,c.imag],'alignment_multiplier_on_b':[z.real,z.imag],'aligned_residual':residual,'raw_residual':raw,'fresh_status':decision,'cached_status':t['cached_result']['status'],'cache_agrees':False}
    elif ident=='I4':
        catalog=json.loads((ROOT/'catalog.json').read_text()); available=[s['id'] for s in catalog if s['available']]
        assert available==['compare-quantum-states-and-operators']
        contract=(ROOT/'skills/compare-quantum-states-and-operators/references/contract.md').read_text()
        assert 'other representation kinds (density, channel, counts)' in contract
        assert r['status']=='unsupported' and d['kind']=='density'
        evidence={'available_skills':available,'density_boundary_verified_in_contract':True,'input_matrices_preserved':True,'entrywise_identical_as_supplied':d['a']==d['b'],'scope_note':'Entrywise identity is a direct inspection, not certification by the unavailable density profile.'}
    else:
        assert d['producer']=='unverified export' and d['dtype']=='complex64' and d['shape']==[1,2]
        assert len(d['a'])==1 and len(d['a'][0])==2
        assert r['status']=='not_admissible'
        skill=(ROOT/'skills/compare-quantum-states-and-operators/SKILL.md').read_text()
        assert 'released FlagQuantum 0.3.1 on CPU complex128' in skill
        evidence={'metadata_preserved':True,'verified_producer':False,'declared_dtype':'complex64','declared_shape':[1,2],'batch_axis_present':True,'comparison_executed':False}
    verification={'passed':True,'evidence':evidence,'runtime':{'executable':sys.executable,'version':sys.version}}
    (OUT/ident/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
    r['verification']={'status':'passed','script':'outputs/verify.py','result':f'outputs/{ident}/verification.json'}
    r['evidence_paths'] += [f'outputs/{ident}/explanation.json',f'outputs/{ident}/verification.json']
    r['evidence_paths']=list(dict.fromkeys(r['evidence_paths']))
    checks.append({'id':ident,'passed':True})
before=json.loads((OUT/'input_hashes_before.json').read_text())
after={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in before}
assert before==after
(OUT/'input_preservation.json').write_text(json.dumps({'unchanged':True,'sha256':after},indent=2)+'\n')
(OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'passed':True,'checks':checks,'inputs_unchanged':True},indent=2))
