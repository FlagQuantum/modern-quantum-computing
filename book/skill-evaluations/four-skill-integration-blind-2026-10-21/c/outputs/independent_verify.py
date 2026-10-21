"""Independent classical binary64 verification: no workflow/helper/library imports.
Evolution is calculated by characteristic eigenvalues and spectral projectors;
all state operations are explicit complex scalar sums. This is not quantum execution.
"""
import cmath,math,json,pathlib,hashlib,subprocess,sys,time
P=pathlib.Path(__file__).resolve().parent
ROOT=P.parent
SKILLS=['translate-complex-linear-algebra','translate-unitary-evolution','reproduce-qubit-interference','compare-quantum-states-and-operators']
def read(p):return json.loads(p.read_text())
def dec(v):
 if len(v)==2 and all(type(x) in (float,int) for x in v):return complex(*v)
 return [dec(x) for x in v]
def enc(x):
 if isinstance(x,list):return [enc(z) for z in x]
 return [complex(x).real,complex(x).imag]
def mv(a,x):return [sum(aij*xj for aij,xj in zip(row,x)) for row in a]
def flatten(x):
 if isinstance(x,list):return [z for row in x for z in flatten(row)]
 return [x]
def err(a,b):
 assert len(flatten(a))==len(flatten(b))
 return max(abs(x-y) for x,y in zip(flatten(a),flatten(b)))
def spectral(e):
 # For distinct Hermitian eigenvalues, exp(-iE)=f(l1)P1+f(l2)P2.
 trace=(e[0][0]+e[1][1]).real; gap=math.sqrt((e[0][0].real-e[1][1].real)**2+4*abs(e[0][1])**2)
 l1=(trace+gap)/2;l2=(trace-gap)/2
 assert gap>0
 p1=[[(e[i][j]-(l2 if i==j else 0))/gap for j in range(2)] for i in range(2)]
 return [[cmath.exp(-1j*l1)*p1[i][j]+cmath.exp(-1j*l2)*((1 if i==j else 0)-p1[i][j]) for j in range(2)] for i in range(2)]
def final(x,phi,delta):
 z=cmath.exp(1j*(phi-delta))*x[1]
 return [(x[0]+z)/math.sqrt(2),(x[0]-z)/math.sqrt(2)]
def comparison(name,a,b,kind='state'):
 q={'kind':kind,'mode':'coordinates','basis_a':['0','1'],'basis_b':['0','1'],'a':enc(a),'b':enc(b),'atol':1e-10}
 (P/(name+'.request.json')).write_text(json.dumps(q,indent=2));cmd=[sys.executable,str(ROOT/'skills/compare-quantum-states-and-operators/scripts/compare.py')];start=time.time();p=subprocess.run(cmd,input=json.dumps(q),text=True,capture_output=True)
 (P/(name+'.stdout.json')).write_text(p.stdout);(P/(name+'.stderr.txt')).write_text(p.stderr);(P/(name+'.execution.json')).write_text(json.dumps({'command':cmd,'exit_code':p.returncode,'elapsed_seconds':time.time()-start},indent=2))
 return read(P/(name+'.stdout.json'))
reports={};results=[]
for task in read(ROOT/'tasks.json'):
 id=task['id'];q=task['experiment'];wf=P/(id+'-workflow');r=read(wf/'report.json');eps=q['tolerance']['coordinate_atol']
 if id=='C3':
  assert r['status']=='unsupported' and r['actual_flagquantum_circuits']==0
  boundary={'requested':'Actual noisy hardware probabilities and confidence bound','status':'unsupported','reason':'Ideal statevector packages do not execute hardware, noise or shot distributions. No provider, device, calibration/noise model, credentials, actual shot counts, provenance or confidence level supplied. shots=1000 is a requested count, not an observation.','ideal_substitution_performed':False,'hardware_execution_performed':False,'confidence_bound_computed':False,'necessary_next_information':['Hardware provider/device and access or authenticated execution artifacts','Actual per-setting measurement counts and shot totals, circuit/transpilation and timing provenance','Confidence level and statistical assumptions; noise/calibration data for noise-specific claims']}
  (P/'C3-scope-disposition.json').write_text(json.dumps(boundary,indent=2))
  results.append({'id':id,'selected_skills':['reproduce-qubit-interference','translate-unitary-evolution','compare-quantum-states-and-operators'],'clarification_question':None,'status':'unsupported','evidence_paths':['C3-task.json','C3-request.json','C3-workflow/report.json','C3-workflow.execution.json','C3-scope-disposition.json'],'verification':boundary,'limitations':['No actual noisy quantum execution or hardware statistics profile is supplied. No ideal run is offered as certification.']});continue
 assert r['status']=='verified'
 h=dec(q['generator']['matrix']);mult=q['time']['value']*1e-9/q['hbar']['value'];e=[[mult*z for z in row] for row in h];u=spectral(e);state=dec(q['initial_state']);x=mv(u,state)
 ev=read(wf/'02-evolution/stdout.json');env=read(wf/'handoff-envelope.json');native=dec(ev['native_zyz_matrix']);alpha=ev['zyz']['alpha']
 checks=[]
 def check(label,value,budget=eps):
  checks.append({'check':label,'max_absolute_error':value,'budget':budget,'passed':value<=budget});assert value<=budget,(id,label,value,budget)
 check('independent dimensionless exponent vs saved conversion',err(e,dec(r['conversion']['effective_exponent'])))
 check('spectral-projector full U vs evolution actual U',err(u,dec(ev['unitary'])))
 check('spectral-projector full U vs classical helper exponential',err(u,dec(read(wf/'01-classical-exponential/stdout.json')['result']['value'])))
 check('native matrix phase reconstruction',err(u,[[cmath.exp(1j*alpha)*z for z in row] for row in native]))
 check('independent evolved state vs literal handoff',err(x,dec(env['state'])))
 assert env['basis']==['0','1'] and env['shape']==[1,2] and env['dtype']=='torch.complex128' and env['device']=='cpu'
 assert env['source_sha256']==hashlib.sha256((wf/env['source_path']).read_bytes()).hexdigest()
 assert read(wf/'09-interference/request.json')['state']==env['state']
 for record in ev['records']:
  label=record['input_label'];path=record['path']
  if label=='coherent-control':
   y=mv(native if path=='controlled-unrepaired' else u,state);ref=[z/math.sqrt(2) for z in state+y]
  else:ref=mv(native if path=='native-zyz' else u,{'supplied':state,'zero':[1,0],'one':[0,1]}[label])
  check('actual evolution '+label+'/'+path+' coordinates',err(ref,dec(record['statevector'])))
  check('actual evolution '+label+'/'+path+' probabilities',err([abs(z)**2 for z in ref],record['probabilities']))
 continuous=read(wf/'continuous-circuit.json');staged=read(wf/'09-interference/stdout.json');finals=[]
 for phi,a,b in zip(q['phase_scan']['values'],continuous['records'],staged['records']):
  y=final(x,phi,q['analyzer']['delta']);probs=[abs(z)**2 for z in y];cross=(x[0].conjugate()*cmath.exp(1j*(phi-q['analyzer']['delta']))*x[1]).real;n=sum(abs(z)**2 for z in x)
  check('final coordinates phi='+str(phi),err(y,dec(a['statevector'])));check('staged final coordinates phi='+str(phi),err(y,dec(b['statevector'])))
  check('final probabilities phi='+str(phi),err(probs,a['probabilities']));check('independent scalar cross formula phi='+str(phi),err(probs,[n/2+cross,n/2-cross]))
  finals.append({'phase_radians':phi,'independent_coordinates':enc(y),'independent_probabilities':probs})
 for call in r['helper_calls']:
  output=read(wf/call['request_path'].replace('request.json','stdout.json'));assert output['runtime']['python'].startswith('3.12.')
  meta=read(wf/call['request_path'].replace('request.json','execution.json'));assert call==meta
  assert (wf/call['request_path'].replace('request.json','stderr.txt')).read_text()==''
  assert hashlib.sha256(json.dumps(read(wf/call['request_path']),sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()==call['request_sha256']
 verification={'method':'Independent standard-library characteristic eigenvalues/spectral-projector exponential and scalar complex arithmetic; no helper/workflow imports','quantum_execution':False,'checks':checks,'all_passed':all(z['passed'] for z in checks),'final_outputs':finals,'handoff_provenance_and_metadata_passed':True,'runtime_and_helper_receipts_checked':True,'actual_workflow_flagquantum_circuits':r['actual_flagquantum_circuits'],'absolute_coordinate_tolerance':eps,'rtol':0}
 disposition={'fresh_run_status':'verified','scientific_acceptance':'pending; numerical agreement does not confer scientific acceptance','candidate_claim':'No candidate supplied','candidate_disposition':'not_applicable'}
 status='verified';paths=[id+'-task.json',id+'-request.json',id+'-workflow/report.json',id+'-workflow/continuous-circuit.json',id+'-workflow/handoff-envelope.json',id+'-workflow.execution.json','independent_verify.py',id+'-independent-verification.json',id+'-claim-disposition.json']
 if id=='C2':
  candidate=read(P/'C2-candidate-interference.stdout.txt');assert candidate['status']=='verified';audit=[]
  # A(phi) is H D(-delta) D(phi); submitted is H D(+delta) D(phi).
  delta=q['analyzer']['delta'];declared=[[1/math.sqrt(2),cmath.exp(-1j*delta)/math.sqrt(2)],[1/math.sqrt(2),-cmath.exp(-1j*delta)/math.sqrt(2)]];submitted=[[1/math.sqrt(2),cmath.exp(1j*delta)/math.sqrt(2)],[1/math.sqrt(2),-cmath.exp(1j*delta)/math.sqrt(2)]]
  op=comparison('C2-analyzer-operator-audit',declared,submitted,'unitary');assert op['status']=='outside_tolerance'
  for phi,a,b in zip(q['phase_scan']['values'],candidate['records'],continuous['records']):
   yc=final(x,phi,-delta);pd=[abs(z)**2 for z in final(x,phi,delta)];pc=[abs(z)**2 for z in yc];check('synthetic submitted chronology prediction '+str(phi),err(yc,dec(a['statevector'])))
   cmp=comparison('C2-candidate-vs-declared-'+str(phi),dec(b['statevector']),dec(a['statevector']));assert cmp['status']=='outside_tolerance'
   audit.append({'phase_radians':phi,'declared_probabilities':pd,'submitted_probabilities':pc,'max_probability_difference':err(pd,pc),'coordinate_comparison':cmp['status'],'coordinate_l2_residual':cmp['decision_residual']})
  disposition.update(candidate_claim=task['claim'],candidate_disposition='rejected',reason='Declared phase-h analyzer is H D(-delta). Submitted D(+delta) then H implements H D(+delta); operator and final complex coordinates/probabilities differ.',synthetic_fixture=True,candidate_numeric_run_status='verified',candidate_numeric_run_meaning='Valid ideal simulation of the submitted alternative chronology via explicitly changed delta, not acceptance as the declared experiment.',operator_audit=op,per_phase_audit=audit)
  status='rejected';paths+=['C2-candidate-request.json','C2-candidate-interference.stdout.txt','C2-candidate-interference.execution.json','C2-analyzer-operator-audit.stdout.json']
 verification['all_passed']=all(z['passed'] for z in checks)
 (P/(id+'-independent-verification.json')).write_text(json.dumps(verification,indent=2));(P/(id+'-claim-disposition.json')).write_text(json.dumps(disposition,indent=2))
 results.append({'id':id,'selected_skills':SKILLS,'clarification_question':None,'status':status,'evidence_paths':paths,'verification':{'fresh_run_status':'verified','independent_checks_passed':verification['all_passed'],'independent_verification_path':id+'-independent-verification.json','candidate_claim_disposition':disposition['candidate_disposition'],'scientific_acceptance':'pending'},'limitations':['Ideal CPU complex128 statevector simulations only; no hardware or noisy data.','Independent numerical checks use binary64 and are not exact proofs or outward-rounded certificates.','Caller-supplied hbar numerical value retained; physical provenance/accuracy not independently certified.','Continuous-circuit artifact means original preparation and operations in one circuit per supplied phase, not an exhaustive continuous-phase execution.']})
(P/'results.json').write_text(json.dumps(results,indent=2));print(json.dumps({'results':results,'independent_quantum_execution':False},indent=2))
