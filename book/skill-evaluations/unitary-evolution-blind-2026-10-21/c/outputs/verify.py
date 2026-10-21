import json,math,cmath,pathlib,subprocess,time
root=pathlib.Path(__file__).resolve().parent.parent;o=root/'outputs'
def dec(a):return [[complex(*z) for z in r] for r in a]
def enc(a):return [[[z.real,z.imag] for z in r] for r in a]
def eye(n):return [[complex(j==k) for k in range(n)] for j in range(n)]
def mm(a,b):return [[sum(a[j][k]*b[k][l] for k in range(len(b))) for l in range(len(b[0]))] for j in range(len(a))]
def scale(a,z):return [[z*x for x in r] for r in a]
def add(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def err(a,b):return max(abs(x-y) for r,s in zip(a,b) for x,y in zip(r,s))
def mv(a,v):return [sum(x*y for x,y in zip(r,v)) for r in a]
def expm(a):
 s=eye(len(a));t=eye(len(a))
 for k in range(1,101):t=scale(mm(t,a),1/k);s=add(s,t)
 return s
Z=[[1+0j,0j],[0j,-1+0j]];Y=[[0j,-1j],[1j,0j]];X=[[0j,1+0j],[1+0j,0j]]
def zyz(p):return mm(mm(expm(scale(Z,-.5j*p['beta'])),expm(scale(Y,-.5j*p['gamma']))),expm(scale(Z,-.5j*p['delta'])))
def ctrl(a):return [[complex(j==k) if j<2 and k<2 else a[j-2][k-2] if j>=2 and k>=2 else 0j for k in range(4)] for j in range(4)]
allres={}
for tid in ['C1','C2','C4']:
 d=o/tid;q=json.loads((d/'request.json').read_text());r=json.loads((d/'stdout.json').read_text());p=r['zyz'];v=zyz(p);rebuilt=scale(v,cmath.exp(1j*p['alpha']))
 target=dec(q['unitary']) if tid!='C4' else expm(scale(dec(q['generator']['matrix']),-.7e-9j))
 checks={'target_vs_helper_matrix':err(target,dec(r['unitary'])),'independent_zyz_full_reconstruction':err(target,rebuilt),'independent_native_matrix':err(v,dec(r['native_zyz_matrix']))}
 psi=[complex(*z) for z in q['state']]
 for k,rec in enumerate(r['records']):
  path=rec['path'];iv=psi if rec['input_label']=='supplied' else [1+0j,0j] if rec['input_label']=='zero' else [0j,1+0j]
  if path.startswith('controlled'):
   iv=[x/math.sqrt(2) for x in psi+psi];mat=ctrl(v) if path=='controlled-unrepaired' else ctrl(target)
  else:mat=v if path=='native-zyz' else target
  expected=mv(mat,iv);actual=[complex(*z) for z in rec['statevector']]
  checks[f'record_{k}_{path}_coordinate_residual']=max(abs(x-y) for x,y in zip(expected,actual))
  checks[f'record_{k}_born_residual']=max(abs(p-abs(z)**2) for p,z in zip(rec['probabilities'],actual))
 extra={}
 if tid=='C1':
  cu,cv=ctrl(target),ctrl(v);repair=eye(4)
  for j in [2,3]:repair[j][j]=cmath.exp(1j*p['alpha'])
  checks['controlled_branch_repair_matrix_residual']=err(mm(repair,cv),cu)
  extra={'omitted_phase_max_entry_discrepancy':err(cu,cv),'alpha_radians':p['alpha'],'basis':['00','01','10','11'],'repair':'phase(alpha) on control, after controlled V','whole_output_scalar_is_not_branch_repair':True}
 if tid=='C2':
  alt=dict(p,beta=p['beta']+.73,delta=p['delta']-.73)
  checks['distinct_endpoint_tuple_same_matrix']=err(v,zyz(alt))
  extra={'claim_disposition':'rejected','returned_tuple':p,'distinct_equivalent_endpoint_tuple':alt,'endpoint_snapping_target_residual':err(target,rebuilt),'explanation':'At gamma=0 only beta+delta is determined; beta+s,delta-s gives the same matrix for every real s. Away from the pole angle branches still have periodic ambiguity. Near gamma=0 arbitrarily small transverse matrix changes can change their azimuth and hence beta and delta by finite amounts. Matrix reconstruction is the verification target, not a preferred angle tuple.','families':[]}
  for phase in [0.,1.,2.]:
   tiny=dict(p,beta=p['beta']+phase,gamma=1e-13,delta=p['delta']-phase)
   extra['families'].append({'tuple':tiny,'matrix_distance_to_endpoint':err(zyz(tiny),v)})
 if tid=='C4':
  original=json.loads((d/'original-task.json').read_text())['data'];expectedE=scale(dec(original['generator']['matrix']),2*math.pi*.7e-9)
  checks['declared_exponent_preserved']=err(expectedE,dec(r['units_and_generator']['effective_exponent']))
  e0=(expectedE[0][0]+expectedE[1][1])/2
  extra={'trace_shift_exponent':e0.real,'trace_shift_phase':[cmath.exp(-1j*e0).real,cmath.exp(-1j*e0).imag],'declared_conversion':'every matrix entry multiplied by 2*pi, Hz to rad/s; time 0.7 ns = 7e-10 s','matrix_exponential_method':'independent 100-term Taylor matrix series, no skill imports or Torch','series_last_term_bound':'matrix infinity norm <=0.792; remainder after 100 terms < exp(0.792)*0.792^101/101!'}
 res={'passed':max(checks.values())<=q['atol'],'atol':q['atol'],'checks':checks,'details':extra};allres[tid]=res;(d/'independent-verification.json').write_text(json.dumps(res,indent=2))
# Explicitly chosen counterexample; not a substitute execution for unspecified H(t).
a=expm(scale(X,-.5j));b=expm(scale(Z,-.5j));ordered=mm(b,a);ordinary=expm(scale(add(X,Z),-.5j));comm=add(mm(X,Z),scale(mm(Z,X),-1))
c3={'passed':True,'claim_disposition':'rejected','task_execution':'unsupported; input generators provide no schedule, and skill has no time-dependent solver','counterexample_scope':'Independent mathematical counterexample only: H(t)=X for 0<=t<0.5 and H(t)=Z for 0.5<=t<=1, dimensionless. Not attributed to supplied task data.','commutator_XZ':enc(comm),'ordered_solution':enc(ordered),'ordinary_exponential_integral':enc(ordinary),'max_entry_discrepancy':err(ordered,ordinary),'conclusion':'Nonzero discrepancy disproves the universal assertion; correct evolution requires time ordering in general. Ordinary exponential can hold for commuting H(t) or special cases.'};allres['C3']=c3;(o/'C3/independent-verification.json').write_text(json.dumps(c3,indent=2))
print(json.dumps({k:{'passed':v['passed'],'maximum_check':max(v.get('checks',{'counterexample_discrepancy':v.get('max_entry_discrepancy',0)}).values())} for k,v in allres.items()},indent=2))
