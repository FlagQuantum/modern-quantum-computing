"""Standard-library cross-checks without helper imports or FlagQuantum."""
import json,math,pathlib,time,sys,platform
root=pathlib.Path(__file__).resolve().parent
start=time.perf_counter(); results={}
for tid in ['A1','A2','A3','A4']:
 d=root/tid;q=json.loads((d/'request.json').read_text());r=json.loads((d/'stdout.json').read_text())
 if tid=='A3':
  norm=math.fsum(x*x+y*y for x,y in q['state'])
  v={'squared_norm':norm,'normalization_error':abs(norm-1),'admissible':abs(norm-1)<=1e-12,'helper_rejection_agrees':r['status']=='invalid_input'}
  assert not v['admissible'] and v['helper_rejection_agrees']
 elif tid=='A4':
  a=[complex(*x) for x in q['a']];b=[complex(*x) for x in q['b']]
  # Derive the phase from one nonzero component, independently of overlap alignment.
  z=a[0]/b[0];z/=abs(z)
  residual=math.sqrt(math.fsum(abs(x-z*y)**2 for x,y in zip(a,b)))
  reported=complex(*r['alignment_multiplier_on_b'])
  v={'method':'single-component phase ratio, checked on the full state','norms_squared':[sum(abs(x)**2 for x in a),sum(abs(x)**2 for x in b)],'alignment_multiplier_on_b':[z.real,z.imag],'residual':residual,'phase_error':abs(z-reported),'within_tolerance':residual<=q['atol']}
  assert v['within_tolerance'] and v['phase_error']<=q['atol'] and r['status']=='within_tolerance'
 else:
  ar,ai=q['state'][0];br,bi=q['state'][1];n=ar*ar+ai*ai+br*br+bi*bi
  rows=[];maxerr=0
  for phi,record in zip(q['phase_radians'],r['records']):
   t=phi-q['readout']['delta_radians'];c=math.cos(t);s=math.sin(t)
   rr=br*c-bi*s;ii=br*s+bi*c
   coords=[[(ar+rr)/math.sqrt(2),(ai+ii)/math.sqrt(2)],[(ar-rr)/math.sqrt(2),(ai-ii)/math.sqrt(2)]]
   probs=[x*x+y*y for x,y in coords]
   # Separate expanded real cross term, including the complex conjugation signs.
   p0=n/2+(ar*br+ai*bi)*c-(ar*bi-ai*br)*s
   err=max([abs(complex(*x)-complex(*y)) for x,y in zip(coords,record['statevector'])]+[abs(x-y) for x,y in zip(probs,record['probabilities'])]+[abs(p0-probs[0])])
   assert err<=q['atol'];maxerr=max(maxerr,err)
   rows.append({'phase_radians':phi,'amplitudes':coords,'probabilities':probs,'expanded_p0':p0,'max_error':err})
  contrast=math.sqrt((ar*ar+ai*ai)*(br*br+bi*bi));analytic={'continuous_p0_min':n/2-contrast,'continuous_p0_max':n/2+contrast,'continuous_visibility':2*contrast/n,'sampled_p0_min':min(x['probabilities'][0] for x in rows),'sampled_p0_max':max(x['probabilities'][0] for x in rows)}
  for k,x in analytic.items():assert abs(x-r['fringe'][k])<=q['atol']
  v={'method':'real 2D rotations and explicit H, squared magnitudes, expanded real cross term and analytic extrema','records':rows,'fringe':analytic,'max_absolute_error':maxerr,'passed':True}
 v['passed']=True
 (d/'verification.json').write_text(json.dumps(v,indent=2));results[tid]=v
print(json.dumps({'passed':True,'tasks':results,'runtime':{'python':platform.python_version(),'executable':sys.executable},'elapsed_seconds':time.perf_counter()-start},indent=2))
