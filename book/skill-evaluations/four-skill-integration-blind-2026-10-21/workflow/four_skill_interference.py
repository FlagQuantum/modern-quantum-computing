#!/usr/bin/env python3
"""One bounded four-skill integration experiment; not a fifth agent skill."""
import argparse,cmath,copy,hashlib,json,math,subprocess,sys
from pathlib import Path
ALG='translate-complex-linear-algebra';EV='translate-unitary-evolution';INT='reproduce-qubit-interference';CMP='compare-quantum-states-and-operators'
VERSIONS={ALG:'0.1.1',EV:'0.1.0',INT:'0.1.0',CMP:'0.1.1'}
class Stop(ValueError):
 def __init__(self,status,reason):self.status,self.reason=status,reason

def encode(x):
 if isinstance(x,list):return [encode(z) for z in x]
 z=complex(x);return [z.real,z.imag]
def decode(x):
 if isinstance(x,list) and len(x)==2 and all(type(v) in (int,float) for v in x):return complex(*x)
 return [decode(z) for z in x]
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def real(x,limit):
 if type(x) not in (int,float) or not math.isfinite(x) or abs(x)>limit:raise Stop('invalid_input','Finite numeric value exceeds experiment profile')
 return float(x)
def validate(q):
 required={'profile','generator','time','initial_state','basis','phase_scan','analyzer','tolerance','phase_context'}
 if not isinstance(q,dict) or not required<=q.keys():raise Stop('needs_clarification','Missing declared experiment fields; no defaults for units, phase context, analyzer or tolerance')
 if q['profile']!='constant-qubit-interference':raise Stop('unsupported','Ideal constant-generator pure-qubit experiment only; no hardware/noise/shot claim')
 if set(q)-required-{'hbar'}:raise Stop('invalid_input','Unexpected experiment fields')
 if q['basis']!=['0','1']:raise Stop('unsupported','Explicit canonical basis 0,1 required; no implicit permutation')
 if q['phase_context']!='full-coordinates-with-controlled-witness':raise Stop('needs_clarification','This experiment retains full phase and adds a controlled witness; declare that context explicitly')
 tol=q['tolerance']
 if not isinstance(tol,dict) or set(tol)!={'coordinate_atol','rtol'} or type(tol['coordinate_atol']) not in (int,float) or not 5e-12<=tol['coordinate_atol']<=1e-9 or type(tol['rtol']) not in (int,float) or tol['rtol']!=0:raise Stop('invalid_input','Explicit coordinate_atol in [5e-12,1e-9] and rtol=0 required')
 for field,keys in [('generator',{'matrix','unit'}),('time',{'value','unit'}),('phase_scan',{'values','unit'}),('analyzer',{'delta','unit'})]:
  if not isinstance(q[field],dict) or set(q[field])!=keys:raise Stop('needs_clarification','Incomplete '+field+' values/units')
 if q['time']['unit'] not in ('s','ns') or q['phase_scan']['unit']!='radian' or q['analyzer']['unit']!='radian':raise Stop('needs_clarification','Convert declared time/angle units explicitly first; no relabeling')
 gu=q['generator']['unit']
 if gu not in ('eV','rad/s'):raise Stop('needs_clarification','Declare eV energy or angular rad/s; cyclic Hz must be clarified before conversion')
 seconds=real(q['time']['value'],1)*(1e-9 if q['time']['unit']=='ns' else 1)
 if gu=='eV':
  h=q.get('hbar')
  if not isinstance(h,dict) or set(h)!={'value','unit'} or h['unit']!='eV*s':raise Stop('needs_clarification','Explicit positive hbar value in eV*s required; no constant lookup')
  hv=real(h['value'],1)
  if hv<1e-100:raise Stop('invalid_input','hbar must be positive and at least1e-100')
  multiplier=seconds/hv
 else:
  if 'hbar' in q:raise Stop('invalid_input','Angular generator already equals H/hbar; do not divide twice')
  multiplier=seconds
 def scalar(z):
  if not isinstance(z,list) or len(z)!=2:raise Stop('invalid_input','Complex coordinate requires [real,imaginary]')
  return complex(real(z[0],1e12),real(z[1],1e12))
 g=q['generator']['matrix']
 if not isinstance(g,list) or len(g)!=2 or any(not isinstance(row,list) or len(row)!=2 for row in g):raise Stop('invalid_input','Generator must be2x2, no batches')
 g=[[scalar(z) for z in row] for row in g];scale=max(abs(z) for row in g for z in row)
 if max(abs(g[i][j]-g[j][i].conjugate()) for i in range(2) for j in range(2))>1e-12*scale:raise Stop('invalid_input','Generator not Hermitian; no zero-time or tiny-scale repair')
 state=q['initial_state']
 if not isinstance(state,list) or len(state)!=2:raise Stop('invalid_input','One pure qubit state required')
 state=[scalar(z) for z in state]
 if abs(sum(abs(z)**2 for z in state)-1)>1e-12:raise Stop('invalid_input','State not normalized; no implicit repair')
 phases=q['phase_scan']['values']
 if not isinstance(phases,list) or not 1<=len(phases)<=9:raise Stop('invalid_input','Explicit1..9-point scan required')
 phases=[real(x,1024) for x in phases];delta=real(q['analyzer']['delta'],1024)
 e=[[multiplier*z for z in row] for row in g]
 if not all(math.isfinite(z.real) and math.isfinite(z.imag) for row in e for z in row) or max(sum(abs(z) for z in row) for row in e)>1:raise Stop('unsupported','Dimensionless exponent infinity norm must be<=1 for this composition profile')
 return state,e,phases,delta,tol['coordinate_atol'],multiplier


def run(q,out,skills_root,fault=None):
 out=Path(out)
 if out.exists():raise Stop('invalid_input','Output directory already exists; preserve prior evidence')
 out.mkdir(parents=True);(out/'source-request.json').write_text(json.dumps(q,indent=2)+'\n')
 log=[];handoffs=[];count=0;stage='preflight';result={'source_request_sha256':digest(q),'fault_injection':fault,'scientific_acceptance':'pending','reader_trial':'not run'}
 def save(name,value):(out/name).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
 def helper(label,skill,request,allowed=('verified',)):
  nonlocal stage,count
  stage=label;folder=out/label;folder.mkdir();save(label+'/request.json',request);script={ALG:'algebra.py',EV:'unitary.py',INT:'interference.py',CMP:'compare.py'}[skill]
  cmd=[sys.executable,str(Path(skills_root)/skill/'scripts'/script)];proc=subprocess.run(cmd,input=json.dumps(request,allow_nan=False),capture_output=True,text=True,timeout=90)
  (folder/'stdout.json').write_text(proc.stdout);(folder/'stderr.txt').write_text(proc.stderr)
  meta={'command':cmd,'exit_code':proc.returncode,'request_sha256':digest(request),'source_request_sha256':digest(q),'skill':skill,'request_path':label+'/request.json'};save(label+'/execution.json',meta);log.append(meta)
  try:r=json.loads(proc.stdout)
  except ValueError:raise Stop('execution_failed','Helper did not return JSON')
  count+=r.get('actual_flagquantum_circuits',len(r.get('records',[])) if skill==INT else 0)
  expected_codes={'verified':0,'within_tolerance':0,'outside_tolerance':1,'verification_failed':1,'invalid_input':2,'unsupported':3,'execution_failed':4}
  if proc.stderr or r.get('contract_version')!=VERSIONS[skill] or r.get('runtime',{}).get('python','').split('.')[:2]!=['3','12'] or proc.returncode!=expected_codes.get(r.get('status')):raise Stop('execution_failed','Helper runtime/version/exit admission failed')
  if r['status'] not in allowed:raise Stop('rejected_mismatch',label+': '+r['status'])
  return r
 def algebra(label,**fields):return helper(label,ALG,dict(coordinates='literal-complex',tolerance={'atol':eps,'rtol':0},**fields))['result']
 def comparison(label,a,b,kind='state',mode='coordinates',allowed=('within_tolerance',)):
  return helper(label,CMP,dict(kind=kind,mode=mode,basis_a=['0','1'],basis_b=['0','1'],a=a,b=b,atol=eps*(2 if kind=='unitary' else math.sqrt(2))),allowed)
 try:
  if sys.implementation.name!='cpython' or sys.version_info[:2]!=(3,12):raise Stop('unsupported','CPython3.12 required')
  state,e,phases,delta,eps,multiplier=validate(q)
  result['tolerance_ledger']={'coordinate_max_absolute':eps,'probability_max_absolute':eps,'algebra_elementwise_atol':eps,'rtol':0,'state_l2_atol':math.sqrt(2)*eps,'operator_frobenius_atol':2*eps,'reason':'Entrywise epsilon implies l2<=sqrt(d)*epsilon for d=2; matrix Frobenius<=2*epsilon. Local budgets do not imply an arbitrary accumulated-error theorem; final outputs checked separately.'}
  result['conversion']={'time_seconds':q['time']['value']*(1e-9 if q['time']['unit']=='ns' else 1),'exponent_multiplier':multiplier,'effective_exponent':encode(e),'hbar_provenance':'Caller-declared numerical input, not independently certified' if 'hbar' in q else 'not applicable'}
  uref=algebra('01-classical-exponential',task='function',kind='exp',units='dimensionless',matrix=encode([[-1j*z for z in row] for row in e]))['value']
  evq=dict(task='evolve',basis=q['basis'],state=q['initial_state'],context='coherent-control',generator=q['generator'],time=copy.deepcopy(q['time']),atol=eps)
  if 'hbar' in q:evq['hbar']=q['hbar']
  if fault=='ns-as-s':evq['time']['unit']='s'
  ev=helper('02-evolution',EV,evq);u=ev['unitary'];native=ev['native_zyz_matrix']
  comparison('03-full-matrix',uref,u,kind='unitary')
  predicted=algebra('04-classical-action',task='algebra',operation='matvec',matrix=uref,v=q['initial_state'])['value']
  supplied=next(r for r in ev['records'] if r['input_label']=='supplied' and r['path']=='direct')
  envelope={'basis':q['basis'],'shape':supplied['shape'],'dtype':supplied['state_dtype'],'device':supplied['device'],'source_path':'02-evolution/stdout.json','source_sha256':hashlib.sha256((out/'02-evolution/stdout.json').read_bytes()).hexdigest(),'state':supplied['statevector']}
  if fault=='drop-phase':envelope['state']=next(r for r in ev['records'] if r['input_label']=='supplied' and r['path']=='native-zyz')['statevector']
  if fault=='basis-swap':envelope['basis']=['1','0']
  if fault=='shape-broadcast':envelope['shape']=[2,1]
  if fault=='stale-cache':envelope['source_sha256']='0'*64
  save('handoff-envelope.json',envelope);stage='handoff-admission'
  if envelope['basis']!=['0','1'] or envelope['shape']!=[1,2] or envelope['dtype']!='torch.complex128' or envelope['device']!='cpu' or envelope['source_sha256']!=hashlib.sha256((out/envelope['source_path']).read_bytes()).hexdigest():raise Stop('rejected_mismatch','Basis/shape/dtype/device/source-receipt mismatch; no silent repair')
  handoffs.append({'source':'evolution supplied/direct shape(1,2)','destination':'interference state(2,)','action':'Extract exactly one verified sample from documented singleton batch; preserve both complex amplitudes and phase','normalization_or_phase_repair':False})
  # Record both phase scopes even when the literal-coordinate handoff is wrong.
  ray=comparison('05-state-ray-diagnostic',predicted,envelope['state'],mode='global-phase',allowed=('within_tolerance','outside_tolerance'))
  isolated=comparison('06-isolated-operator-witness',u,native,kind='unitary',mode='global-phase',allowed=('within_tolerance','outside_tolerance'))
  controlled=comparison('07-controlled-operator-witness',u,native,kind='unitary',mode='controlled',allowed=('within_tolerance','outside_tolerance'))
  result['phase_witness']={'state_ray':ray['status'],'isolated_operator_ray':isolated['status'],'controlled_operator':controlled['status'],'controlled_residual':controlled['decision_residual'],'omitted_scalar_phase_radians':ev['zyz']['alpha'],'note':'Outside controlled tolerance is an intentional witness, not failure of the repaired evolution.'}
  comparison('08-state-coordinate-handoff',predicted,envelope['state'])
  iq=dict(profile='ideal-pure-single-qubit',state=envelope['state'],basis=q['basis'],angle_unit='radian',phase_radians=phases,readout={'type':'phase-h','delta_radians':delta},atol=eps)
  if fault=='analyzer-sign':iq['readout']['delta_radians']=-delta
  if fault=='tolerance-loosen':iq['atol']=1e-8
  stage='interference-request-admission';save('interference-proposed-request.json',iq)
  if iq['atol']!=eps or iq['readout']!={'type':'phase-h','delta_radians':delta}:raise Stop('rejected_mismatch','Analyzer chronology/sign or caller budget changed during handoff')
  interference=helper('09-interference',INT,iq)
  import flagquantum as fq
  import torch
  from importlib.metadata import version
  if version('flagquantum')!='0.3.1' or version('torch').split('+')[0]!='2.13.0':raise Stop('unsupported','Pinned FlagQuantum/Torch required')
  options=fq.ExecutionOptions(mode='statevector',backend='pytorch',device='cpu',precision='complex128',allow_backend_fallback=False,allow_approximate=False)
  outputs=[];stage='continuous-circuit'
  for j,(phi,staged) in enumerate(zip(phases,interference['records'])):
   a,b=state;c=fq.Circuit(1,dtype=torch.complex128);c.unitary(0,unitary=torch.tensor([[a,-b.conjugate()],[b,a.conjugate()]],dtype=torch.complex128));c.unitary(0,unitary=torch.tensor(decode(u),dtype=torch.complex128));c.phase(0,theta=phi);c.phase(0,theta=-delta);c.h(0)
   r=fq.run(c,outputs=[fq.probabilities()],options=options);sv,p=r.statevector(),r.probabilities;count+=1
   if list(sv.shape)!=[1,2] or list(p.shape)!=[1,2] or sv.dtype!=torch.complex128 or p.dtype!=torch.float64 or sv.device.type!='cpu' or p.device.type!='cpu' or not torch.isfinite(sv).all() or not torch.isfinite(p).all():raise Stop('execution_failed','Continuous circuit output metadata/finiteness failed')
   actual=encode(sv[0].tolist());probs=p[0].tolist();readout=[[1/math.sqrt(2),cmath.exp(1j*(phi-delta))/math.sqrt(2)],[1/math.sqrt(2),-cmath.exp(1j*(phi-delta))/math.sqrt(2)]]
   reference=algebra(f'10-{j}-classical-readout',task='algebra',operation='matvec',matrix=encode(readout),v=predicted)['value']
   comparison(f'11-{j}-continuous-vs-staged',actual,staged['statevector']);comparison(f'12-{j}-continuous-vs-reference',actual,reference)
   probability_error=max(abs(x-y) for x,y in zip(probs,staged['probabilities']))
   if probability_error>eps:raise Stop('rejected_mismatch','Final probabilities exceed caller budget')
   outputs.append({'phase_radians':phi,'statevector':actual,'probabilities':probs,'classical_reference_state':reference,'staged_statevector':staged['statevector'],'staged_probabilities':staged['probabilities'],'probability_max_absolute_error':probability_error,'shape':[1,2],'state_dtype':str(sv.dtype),'probability_dtype':str(p.dtype),'device':'cpu'})
  save('continuous-circuit.json',{'actual_flagquantum_circuits':len(outputs),'versions':{'flagquantum':version('flagquantum'),'torch':version('torch')},'execution':{'mode':'statevector','backend':'pytorch','device':'cpu','precision':'complex128','fallback':False,'approximation':False},'chronology':['prepare original state','U(t)','D(phi)','D(-delta)','H'],'records':outputs})
  result.update(status='verified',outputs=outputs,stage='complete',claim_acceptance='This declared ideal composition only; no independent scientific acceptance or whole-paper claim')
 except Stop as exc:result.update(status=exc.status,reason=exc.reason,stage=stage)
 except Exception as exc:result.update(status='execution_failed',reason=type(exc).__name__+': '+str(exc),stage=stage)
 result.update(runtime={'implementation':sys.implementation.name,'python':'.'.join(map(str,sys.version_info[:3]))},helper_calls=log,handoffs=handoffs,actual_flagquantum_circuits=count,skills=VERSIONS,workflow_is_agent_skill=False)
 save('report.json',result);return result

def reject_constant(x):raise Stop('invalid_input','Nonstandard JSON constant '+x)
def unique_object(pairs):
 q={}
 for k,v in pairs:
  if k in q:raise Stop('invalid_input','Duplicate JSON key '+k)
  q[k]=v
 return q

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--request',required=True);p.add_argument('--output',required=True);p.add_argument('--skills-root',type=Path,default=Path(__file__).resolve().parents[2]/'skills');p.add_argument('--fault',choices=['ns-as-s','drop-phase','basis-swap','shape-broadcast','stale-cache','analyzer-sign','tolerance-loosen']);args=p.parse_args()
 try:
  q=json.loads(Path(args.request).read_text(),parse_constant=reject_constant,object_pairs_hook=unique_object);json.dumps(q,allow_nan=False)
  r=run(q,args.output,args.skills_root,args.fault)
 except Stop as e:r={'status':e.status,'reason':e.reason}
 except (ValueError,OverflowError,RecursionError) as e:r={'status':'invalid_input','reason':str(e)}
 print(json.dumps({k:r[k] for k in ('status','stage','actual_flagquantum_circuits') if k in r},sort_keys=True));return {'verified':0,'rejected_mismatch':1,'invalid_input':2,'needs_clarification':2,'unsupported':3,'execution_failed':4}[r['status']]
if __name__=='__main__':sys.exit(main())
