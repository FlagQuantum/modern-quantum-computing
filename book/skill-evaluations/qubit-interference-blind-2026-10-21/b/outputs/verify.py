import cmath, json, math, pathlib, sys, platform, time
start=time.perf_counter()
OUT=pathlib.Path(__file__).resolve().parent
ROOT=OUT.parent
tasks=json.loads((ROOT/'tasks.json').read_text())
def matvec(m,v):
    return [sum(m[i][j]*v[j] for j in range(len(v))) for i in range(len(m))]
def convert(pairs): return [complex(*p) for p in pairs]
summary={}
for task in tasks:
    id=task['id']; checks=[]; extra={}
    if id=='B3':
        raw=json.loads((OUT/id/'experiment1.stdout.json').read_text())
        meta=json.loads((OUT/id/'experiment1.execution.json').read_text())
        assert raw['status']=='invalid_input' and meta['exit_code']==2
        result={'status':'boundary_confirmed','checks':['Original noisy request rejected with exit 2; no physical simulation or visibility certified.'],'physical_verification':'pending channel semantics and unavailable noise workflow'}
    else:
        exps=task.get('experiments',[task.get('data')])
        for i,exp in enumerate(exps):
            actual=json.loads((OUT/id/f'experiment{i+1}.stdout.json').read_text())
            assert actual['status']=='verified'
            a=convert(exp['state']); norm=sum(abs(z)**2 for z in a)
            assert abs(norm-1)<1e-12
            for record,phi in zip(actual['records'],exp['phase_radians'],strict=True):
                v=matvec([[1,0],[0,cmath.exp(1j*phi)]],a)
                if exp['readout']['type']=='phase-h':
                    delta=exp['readout']['delta_radians']
                    v=matvec([[1,0],[0,cmath.exp(-1j*delta)]],v)
                    v=matvec([[1/math.sqrt(2),1/math.sqrt(2)],[1/math.sqrt(2),-1/math.sqrt(2)]],v)
                p=[abs(z)**2 for z in v]
                state_error=max(abs(x-y) for x,y in zip(v,convert(record['statevector']),strict=True))
                prob_error=max(abs(x-y) for x,y in zip(p,record['probabilities'],strict=True))
                assert state_error<=exp['atol'] and prob_error<=exp['atol']
                checks.append({'experiment':i+1,'phi':phi,'independent_probabilities':p,'state_error':state_error,'probability_error':prob_error})
        if id=='B1':
            expected=[abs(z)**2 for z in convert(exps[0]['state'])]
            assert all(max(abs(x-y) for x,y in zip(c['independent_probabilities'],expected))<1e-10 for c in checks)
            extra={'fringe':False,'reason':'D(phi) changes only phases of computational amplitudes, so each probability is constant for every phase.'}
        if id=='B2':
            x,y=[convert(e['state']) for e in exps]
            # Independent invariant: equal rays must have the same component ratio.
            determinant=x[0]*y[1]-x[1]*y[0]
            overlap=sum(a.conjugate()*b for a,b in zip(x,y))
            distance=math.sqrt(sum(abs(a)**2 for a in x)+sum(abs(b)**2 for b in y)-2*abs(overlap))
            comparison=json.loads((OUT/id/'comparison.stdout.json').read_text())
            assert abs(determinant)>1e-10 and abs(overlap)<1e-10 and abs(comparison['decision_residual']-distance)<1e-10
            assert comparison['status']=='outside_tolerance'
            assert max(abs(a-b) for a,b in zip(checks[0]['independent_probabilities'],checks[1]['independent_probabilities']))<1e-10
            extra={'same_probabilities':True,'global_phase_equivalent':False,'determinant':[determinant.real,determinant.imag],'overlap':[overlap.real,overlap.imag],'ray_distance':distance}
        if id=='B4':
            rows=[]
            for c in checks:
                phi=c['phi']; delta=exps[0]['readout']['delta_radians']
                claimed=(1+math.cos(phi+delta))/2
                correct=(1+math.cos(phi-delta))/2
                measured=c['independent_probabilities'][0]
                assert abs(measured-correct)<=1e-10
                rows.append({'phi':phi,'delta':delta,'actual_p0':measured,'claimed_p0':claimed,'absolute_claim_error':abs(claimed-measured),'claim_within_tolerance':abs(claimed-measured)<=1e-10})
            assert any(not r['claim_within_tolerance'] for r in rows)
            extra={'claim_disposition':'refuted at supplied positive delta','correct_formula':'(1+cos(phi-delta))/2, up to supplied floating-point normalization','claim_comparison':rows}
        result={'status':'passed','checks':checks,**extra}
    (OUT/id/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    summary[id]=result
summary['runtime']={'python':platform.python_version(),'implementation':platform.python_implementation(),'executable':sys.executable,'elapsed_seconds':time.perf_counter()-start}
(OUT/'verification-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
