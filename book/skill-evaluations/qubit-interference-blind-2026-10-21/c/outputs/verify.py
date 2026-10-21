"""Independent dense 2x2 matrix propagation; no helper or FlagQuantum imports."""
import cmath,json,math,pathlib
root=pathlib.Path(__file__).resolve().parent
H=[[1/math.sqrt(2),1/math.sqrt(2)],[1/math.sqrt(2),-1/math.sqrt(2)]]
def mv(m,v):return [sum(m[i][j]*v[j] for j in range(2)) for i in range(2)]
def D(x):return [[1,0],[0,cmath.exp(1j*x)]]
def enc(v):return [[z.real,z.imag] for z in v]
results={}
for ident in ['C1','C2','C4']:
    q=json.loads((root/(ident+'.request.json')).read_text());r=json.loads((root/(ident+'.helper.stdout')).read_text())
    assert r['status']=='verified'
    a=[complex(*z) for z in q['state']];records=[]
    for phi,actual in zip(q['phase_radians'],r['records']):
        v=mv(H,mv(D(-q['readout']['delta_radians']),mv(D(phi),a)))
        p=[abs(z)**2 for z in v]
        stateerr=max(abs(z-complex(*w)) for z,w in zip(v,actual['statevector']))
        perr=max(abs(z-w) for z,w in zip(p,actual['probabilities']))
        assert max(stateerr,perr)<q.get('atol',1e-10)
        records.append({'phase_radians':phi,'state':enc(v),'probabilities':p,'state_error':stateerr,'probability_error':perr})
    results[ident]={'passed':True,'method':'independent chronological dense-matrix amplitude propagation and Born rule','records':records}
# C2: absent alpha makes exp(i phi) a global phase, and every phase is flat.
q=json.loads((root/'C2.request.json').read_text());assert q['state'][0]==[0.0,0.0]
assert all(max(abs(p-0.5) for p in x['probabilities'])<1e-10 for x in results['C2']['records'])
results['C2'].update(relative_phase_identifiable=False,continuous_visibility=0,proof='With alpha=0, the scan multiplies the entire state by a common phase. H maps the only occupied path to equal outcome probabilities.')
# C3 explicitly preserves chronological D(phi), H, H; do not use the helper.
tasks=json.loads((root.parent/'tasks.json').read_text());t=next(x for x in tasks if x['id']=='C3');records=[]
for phi in t['data']['phase_radians']:
    v=[1+0j,0j];steps=[]
    for name,m in [('D(phi)',D(phi)),('H',H),('H',H)]:
        v=mv(m,v);steps.append({'operation':name,'state':enc(v)})
    p=[abs(z)**2 for z in v];assert abs(p[0]-1)<1e-10 and p[1]<1e-10
    records.append({'phase_radians':phi,'steps':steps,'probabilities':p})
results['C3']={'passed':True,'method':'separate independent matrix derivation, not a supported interference-helper execution','records':records,'symbolic_reason':'D(phi)|0>=|0> and H H=I, so readout is (1,0) for every phi.'}
# C4 compare fresh raw experiment against cache, never accept its status.
cache=next(x for x in tasks if x['id']=='C4')['cache']
p=results['C4']['records'][0]['probabilities'];err=max(abs(a-b) for a,b in zip(p,cache['probabilities'][0]))
assert err>1e-10
results['C4'].update(cache_claim='rejected',cache_max_absolute_error=err,explanation='Input is (|0>+i|1>)/sqrt(2). At phi=delta=0, H yields amplitudes (1+i)/2 and (1-i)/2, hence equal probabilities, contradicting cached (1,0).')
(root/'verification.results.json').write_text(json.dumps(results,indent=2))
print(json.dumps({'passed':True,'tasks':list(results)}))
