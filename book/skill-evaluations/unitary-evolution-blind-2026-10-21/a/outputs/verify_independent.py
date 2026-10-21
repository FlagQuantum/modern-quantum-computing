import pathlib,json,cmath,math,sys,subprocess,time
root=pathlib.Path('/private/tmp/mqc-unitary-blind-r1/a');out=root/'outputs'
def read(p):return json.loads(p.read_text())
def dec(x):
 if isinstance(x[0],(int,float)):return complex(*x)
 return [dec(i) for i in x]
def eye(n):return [[complex(i==j) for j in range(n)] for i in range(n)]
def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def mv(a,b):return [sum(x*y for x,y in zip(row,b)) for row in a]
def scale(a,z):return [[z*x for x in r] for r in a]
def diff(a,b):return [x-y for x,y in zip(a,b)]
def flat(a):return sum(a,[])
def maxerr(a,b):return max(map(abs,diff(flat(a),flat(b))))
def norm(a):return math.sqrt(sum(abs(x)**2 for x in a))
def enc(a):
 if isinstance(a,complex):return [a.real,a.imag]
 if isinstance(a,list):return [enc(x) for x in a]
 return a
def controlled(a):
 b=eye(4)
 for i in range(2):
  for j in range(2):b[i+2][j+2]=a[i][j]
 return b
def gates(z):
 def rz(t):return [[cmath.exp(-.5j*t),0j],[0j,cmath.exp(.5j*t)]]
 t=z['gamma']/2; ry=[[complex(math.cos(t)),complex(-math.sin(t))],[complex(math.sin(t)),complex(math.cos(t))]]
 return mul(rz(z['beta']),mul(ry,rz(z['delta'])))
for tid in ['A1','A2','A3','A4']:
 d=out/tid;req=read(d/'request.json');r=read(d/'stdout.json');checks={};detail={}
 if tid=='A2':
  n2=sum(x*x for x in req['axis']); checks={'axis_norm_squared_is_four':n2==4,'rejected_without_repair':r['status']=='invalid_input' and read(d/'execution.json')['exit_code']==2};detail={'axis_norm_squared':n2,'no_rotation_executed':True}
 elif tid=='A4':
  a,b=dec(req['a']),dec(req['b']);overlap=sum(x.conjugate()*y for x,y in zip(a,b));z=overlap.conjugate()/abs(overlap);res=norm([x-z*y for x,y in zip(a,b)])
  checks={'input_a_normalized':abs(norm(a)-1)<1e-12,'input_b_normalized':abs(norm(b)-1)<1e-12,'phase_aligned_within_tolerance':res<=req['atol'],'helper_residual_agrees':abs(res-r['decision_residual'])<1e-14};detail={'overlap':enc(overlap),'multiplier_on_b':enc(z),'raw_euclidean':norm(diff(a,b)),'aligned_euclidean':res}
 else:
  u=dec(r['unitary']);v=gates(r['zyz']);recon=scale(v,cmath.exp(1j*r['zyz']['alpha']));checks['phase_retaining_reconstruction']=maxerr(u,recon)<=req['atol'];detail['reconstruction_max_absolute']=maxerr(u,recon)
  if tid=='A1':
   # Independent standard-library Taylor exponential, not torch.matrix_exp or helper Pauli formula.
   h=dec(req['generator']['matrix']);factor=req['time']['value']*1e-9/req['hbar']['value'];a=scale(h,-1j*factor);u_ref=eye(2);term=eye(2)
   for k in range(1,81):
    term=scale(mul(term,a),1/k);u_ref=[[x+y for x,y in zip(row,tr)] for row,tr in zip(u_ref,term)]
   err=maxerr(u,u_ref);checks['independent_taylor_exponential']=err<=req['atol'];detail.update({'exponent_multiplier':factor,'taylor_terms':80,'final_term_max_absolute':max(map(abs,flat(term))),'taylor_unitary':enc(u_ref),'taylor_max_absolute_error':err,'hbar_provenance':'Parent-declared input; no additional physical-constant provenance supplied'})
  else:u_ref=dec(req['unitary'])
  s=dec(req['state']);inputs={'supplied':s,'zero':[1+0j,0j],'one':[0j,1+0j]};errs=[]
  for record in r['records']:
   label,path=record['input_label'],record['path']; actual=dec(record['statevector'])
   if label!='coherent-control':expected=mv(u_ref if path=='direct' else v,inputs[label])
   else:
    cs=[x/math.sqrt(2) for x in s]*2
    expected=mv(controlled(v if path=='controlled-unrepaired' else u_ref),cs)
   e=max(map(abs,diff(actual,expected)));errs.append({'input':label,'path':path,'max_absolute_error':e})
  checks['all_actual_circuit_outputs_agree_with_independent_matrices']=all(e['max_absolute_error']<=req['atol'] for e in errs);detail['actual_circuit_checks']=errs
  if tid=='A3':
   cu,cv=controlled(u_ref),controlled(v);overlap=sum(x.conjugate()*y for x,y in zip(flat(cu),flat(cv)));z=overlap.conjugate()/abs(overlap);raw=norm(diff(flat(cu),flat(cv)));aligned=norm([x-z*y for x,y in zip(flat(cu),flat(cv))]);p=eye(4)
   for j in [2,3]:p[j][j]=cmath.exp(1j*r['zyz']['alpha'])
   repair=maxerr(cu,mul(p,cv));checks.update({'omission_changes_full_controlled_operation':raw>req['atol'],'whole_operation_phase_alignment_cannot_fix_omission':aligned>req['atol'],'branch_phase_repair_restores_full_operator':repair<=req['atol']});detail.update({'controlled_raw_frobenius':raw,'controlled_global_phase_aligned_frobenius':aligned,'branch_phase_repair_max_absolute':repair,'claim_disposition':'refuted for supplied unitary','claim':'Dropping the returned scalar phase cannot change the full controlled operation.'})
 result={'method':'Independent standard-library complex arithmetic; no helper imports','checks':checks,'passed':all(checks.values()),'details':detail}
 (d/'verification.json').write_text(json.dumps(result,indent=2));print(tid,json.dumps(result))
 if not result['passed']:sys.exit(1)
# Additional structured coherent-control comparison through applicable comparison skill.
d=out/'A3';req=read(d/'request.json');r=read(d/'stdout.json');cq={'kind':'unitary','mode':'controlled','basis_a':['0','1'],'basis_b':['0','1'],'a':req['unitary'],'b':r['native_zyz_matrix'],'atol':req['atol']}
(d/'controlled_comparison_request.json').write_text(json.dumps(cq,indent=2));cmd=[sys.executable,str(root/'skills/compare-quantum-states-and-operators/scripts/compare.py')];start=time.time();p=subprocess.run(cmd,input=json.dumps(cq),text=True,capture_output=True)
(d/'controlled_comparison_stdout.json').write_text(p.stdout);(d/'controlled_comparison_stderr.txt').write_text(p.stderr);(d/'controlled_comparison_execution.json').write_text(json.dumps({'command':cmd,'exit_code':p.returncode,'elapsed_seconds':time.time()-start},indent=2));print('controlled comparison',p.returncode,p.stdout)
assert p.returncode==1 and json.loads(p.stdout)['status']=='outside_tolerance'
