import json,subprocess,math,cmath
from pathlib import Path
root=Path('/Users/baai/Documents/liuwei/modern-quantum-computing');out=Path('/private/tmp/mqc-paper-transfer/author-errors');out.mkdir(exist_ok=False)
py='/private/tmp/mqc-writing-venv/bin/python';records=[]
def enc(v):return [[z.real,z.imag] for z in map(complex,v)]
def call(name,skill,script,q,exitcode=0):
 d=out/name;d.mkdir();(d/'request.json').write_text(json.dumps(q,indent=2)+'\n');p=subprocess.run([py,str(root/'skills'/skill/'scripts'/script)],input=json.dumps(q),text=True,capture_output=True);(d/'stdout.json').write_text(p.stdout);(d/'stderr.txt').write_text(p.stderr);(d/'exit.json').write_text(json.dumps({'exit_code':p.returncode})+'\n');assert p.returncode==exitcode and not p.stderr,(name,p.stdout,p.stderr);return json.loads(p.stdout)
s=1/math.sqrt(2);axis=[.23,1.37];ph=[math.pi*x for x in axis]
def interference(name,phases,delta):
 return call(name,'reproduce-qubit-interference','interference.py',dict(profile='ideal-pure-single-qubit',state=enc([s,s]),basis=['0','1'],angle_unit='radian',phase_radians=phases,readout={'type':'phase-h','delta_radians':delta},atol=1e-10))
for name,phases,delta,target in [('literal-H2',ph,0,[(1-math.cos(x))/2 for x in ph]),('axis-as-radians',axis,math.pi,[(1-math.cos(x))/2 for x in ph]),('Hz-as-angular',[125e6*.83e-9],math.pi,[(1-math.cos(2*math.pi*125e6*.83e-9))/2])]:
 r=interference(name,phases,delta);actual=[v['probabilities'][0] for v in r['records']];error=max(abs(a-b) for a,b in zip(actual,target));assert error>1e-3;records.append(dict(case=name,candidate_origin='deliberately constructed incorrect interpretation, not paper data',helper_status=r['status'],candidate_disposition='inconsistent_with_declared_target',max_probability_error=error,actual_flagquantum_circuits=len(r['records'])))
r=json.load(open('/private/tmp/mqc-paper-transfer/author/caller-extension/report.json'));actual=r['outputs'][0]['statevector'];candidate=enc([complex(*z)*cmath.exp(.17j) for z in actual]);q=dict(kind='state',basis_a=['0','1'],basis_b=['0','1'],a=actual,b=candidate,atol=math.sqrt(2)*1e-10)
for mode,exitcode in [('coordinates',1),('global-phase',0)]:
 x=call('identity-phase-'+mode,'compare-quantum-states-and-operators','compare.py',dict(q,mode=mode),exitcode);records.append(dict(case='identity-phase-'+mode,candidate_origin='synthetic phase-stripped vector derived from actual fresh evolution output',helper_status=x['status'],decision_residual=x['decision_residual'],candidate_disposition='rejected_for_full_coordinates' if mode=='coordinates' else 'same_isolated_ray_only',actual_flagquantum_circuits=0))
records.append(dict(case='whole-paper-hardware-claim',candidate_origin='deliberately constructed scope overclaim',candidate_disposition='out_of_scope',reason='No cavity Hilbert space, noise, calibration, shot data or experimental uncertainty in this ideal claim run',actual_flagquantum_circuits=0))
report=dict(cases=records,passed=len(records),actual_flagquantum_circuits=sum(r['actual_flagquantum_circuits'] for r in records),helper_calls=5,scientific_acceptance='pending')
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
