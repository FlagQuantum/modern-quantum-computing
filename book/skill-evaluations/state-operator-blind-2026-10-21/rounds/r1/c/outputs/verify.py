import json, pathlib, math
OUT=pathlib.Path(__file__).resolve().parent
ROOT=OUT.parent
tasks={t['id']:t for t in json.loads((ROOT/'tasks.json').read_text())}
reports={}
for ident,task in tasks.items():
    dest=OUT/ident
    assert json.loads((dest/'supplied_task.json').read_text())==task
    if ident in ('C1','C2','C3'):
        req=json.loads((dest/'request.json').read_text())
        assert all(req[k]==v for k,v in task['data'].items())
        assert (dest/'stderr.txt').read_text()==''
        actual=json.loads((dest/'stdout.json').read_text())
        execution=json.loads((dest/'execution.json').read_text())
    if ident=='C1':
        assert req['basis_b']!=['00','01','10','11']
        assert actual['status']=='unsupported' and execution['exit_code']==3
        reports[ident]={'passed':True,'basis_declarations_preserved':True,'helper_exit_code':3,'no_inequality_inferred':True}
    elif ident=='C2':
        a=[complex(*z) for z in req['a']]; b=[complex(*z) for z in req['b']]
        n_a=sum(abs(z)**2 for z in a); n_b=sum(abs(z)**2 for z in b)
        assert abs(n_a-1)<=1e-12 and abs(n_b-1)<=1e-12
        c=sum(x.conjugate()*y for x,y in zip(a,b)); z=c.conjugate()/abs(c)
        residual=math.sqrt(sum(abs(x-z*y)**2 for x,y in zip(a,b)))
        ray_distance_formula=math.sqrt(max(0,n_a+n_b-2*abs(c)))
        assert math.isclose(residual,ray_distance_formula,abs_tol=1e-14)
        assert math.isclose(residual,actual['aligned_residual'],abs_tol=1e-14)
        assert residual>1e-10 and execution['exit_code']==1 and actual['status']=='outside_tolerance'
        assert task['cached_result']['status']=='within_tolerance'
        reports[ident]={'passed':True,'helper_exit_code':1,'independent_aligned_residual':residual,'independent_ray_formula':ray_distance_formula,'squared_norm_a':n_a,'squared_norm_b':n_b,'cached_decision_reliable':False,'absolute_tolerance':1e-10}
    elif ident=='C3':
        assert req['kind']=='density' and req['a']==task['data']['a'] and req['b']==task['data']['b']
        assert actual['status']=='unsupported' and execution['exit_code']==3
        rho=[[complex(*x) for x in row] for row in task['data']['a']]
        # A supplementary entry check is not a density-state certification by the skill.
        reports[ident]={'passed':True,'helper_exit_code':3,'representation_preserved':True,'supplied_entries_equal':task['data']['a']==task['data']['b'],'supplementary_trace':[sum(rho[i][i] for i in range(2)).real,0],'supplementary_purity':sum(abs(x)**2 for row in rho for x in row),'density_certification_by_skill':False}
    else:
        admission=json.loads((dest/'admission.json').read_text()); data=task['data']
        assert data['dtype']=='complex64' and data['shape']==[1,2] and len(data['a'])==1
        assert admission['helper_executed'] is False and not (dest/'request.json').exists()
        assert admission['status']=='unsupported'
        reports[ident]={'passed':True,'helper_executed':False,'raw_dtype_preserved':data['dtype'],'raw_shape_preserved':data['shape'],'raw_metadata_preserved':True,'producer_verified':False,'batch_axis_removed':False,'dtype_widened':False}
(OUT/'verification.json').write_text(json.dumps(reports,indent=2)+'\n')
results=json.loads((OUT/'results.json').read_text())
for result in results:
    result['verification']['result']='passed'
    result['verification']['details']=reports[result['id']]
(OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'verification':'passed','task_count':len(reports),'reports':reports},indent=2))
