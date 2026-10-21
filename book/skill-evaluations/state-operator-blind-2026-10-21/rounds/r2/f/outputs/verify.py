"""Independent direct arithmetic verification. Does not import the supplied helper."""
import hashlib,json,math,pathlib,sys
root=pathlib.Path('/private/tmp/mqc-comparison-blind-r2/f')
tasks=json.loads((root/'tasks.json').read_text())
checks={}
for t in tasks:
    tid=t['id']; p=root/'outputs'/tid
    req=json.loads((p/'request.json').read_text()); result=json.loads((p/'result.json').read_text()); execution=json.loads((p/'execution.json').read_text())
    assert req['a']==t['data']['a'] and req['b']==t['data']['b']
    assert req['basis_a']==t['data']['basis_a'] and req['basis_b']==t['data']['basis_b']
    assert req['mode']=='global-phase' and req['atol']==1e-10
    if req['kind']=='state':
        a=[complex(*v) for v in req['a']]; b=[complex(*v) for v in req['b']]
        norms=[sum(v.real*v.real+v.imag*v.imag for v in vs) for vs in (a,b)]
        assert all(abs(v-1)<=1e-12 for v in norms)
        overlap=sum(x.conjugate()*y for x,y in zip(a,b)); z=complex(math.cos(-math.atan2(overlap.imag,overlap.real)), math.sin(-math.atan2(overlap.imag,overlap.real)))
        residual=math.sqrt(sum(abs(x-z*y)**2 for x,y in zip(a,b)))
        raw=math.sqrt(sum(abs(x-y)**2 for x,y in zip(a,b)))
        assert residual<=req['atol'] and result['status']=='within_tolerance'
        assert execution['exit_code']==0
        assert abs(residual-result['aligned_residual'])<=1e-15
        assert abs(raw-result['raw_residual'])<=1e-15
        cached=t['cached_result']
        assert cached['status']!=result['status'] and abs(cached['aligned_residual']-residual)>1e-10
        checks[tid]={'passed':True,'unit_squared_norms':norms,'independent_aligned_residual':residual,'independent_raw_residual':raw,'multiplier_on_b':[z.real,z.imag],'cached_decision_rejected':True}
    else:
        matrices=[[[complex(*v) for v in row] for row in req[k]] for k in ('a','b')]
        grams=[[[sum(m[k][i].conjugate()*m[k][j] for k in range(len(m))) for j in range(len(m))] for i in range(len(m))] for m in matrices]
        errors=[max(abs(g[i][j]-(1 if i==j else 0)) for i in range(len(g)) for j in range(len(g))) for g in grams]
        assert errors[0]<=1e-12 and errors[1]>1e-12
        assert all(abs(g[i][i]-1)<=1e-12 for g in grams for i in range(len(g)))
        assert result['status']=='invalid_input' and execution['exit_code']==2
        assert 'decision_residual' not in result
        checks[tid]={'passed':True,'column_squared_norms':[[g[i][i].real for i in range(len(g))] for g in grams],'gram_matrices':[[[[v.real,v.imag] for v in row] for row in g] for g in grams],'max_entrywise_gram_errors':errors,'unitary_comparison_valid':False,'no_entries_repaired':True}
before=json.loads((root/'outputs/input_hashes.json').read_text())
assert all(hashlib.sha256((root/path).read_bytes()).hexdigest()==digest for path,digest in before.items())
checks['protected_inputs_unchanged']=True
(root/'outputs/verification.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
