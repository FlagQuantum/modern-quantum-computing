#!/usr/bin/env python3
"""Author cases and separate NumPy/analytic references; no quantum execution."""
import argparse,copy,hashlib,json,math,platform,shutil,subprocess,sys,tempfile
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];PACKAGE=ROOT/'skills/translate-complex-linear-algebra';EVIDENCE=ROOT/'book/skill-evaluations/complex-algebra-v0.1.0'
def enc(x):
 a=np.asarray(x);return np.stack((a.real,a.imag),axis=-1).tolist()
def dec(x):
 a=np.asarray(x);return a[...,0]+1j*a[...,1]
def request(task,**kw):return dict(task=task,coordinates='literal-complex',tolerance={'atol':1e-11,'rtol':1e-12},**kw)
def close(a,b):np.testing.assert_allclose(a,b,rtol=1e-12,atol=1e-11)
def verify(q,o):
 assert o['runtime']['python'].startswith('3.12.') and o['versions']['torch'].split('+')[0]=='2.13.0' and o['quantum_execution'] is False
 r=o['result'];t=q['task']
 if t=='algebra':
  op=q['operation']
  if op=='inner':ref=np.vdot(dec(q['v']),dec(q['w']))
  elif op=='outer':ref=np.outer(dec(q['v']),dec(q['w']).conj())
  elif op=='adjoint':ref=dec(q['matrix']).conj().T
  elif op=='matvec':ref=dec(q['matrix'])@dec(q['v'])
  else:ref=dec(q['left'])@dec(q['right'])
  close(dec(r['value']),ref)
 elif t=='basis':
  a,s,x=dec(q['matrix']),dec(q['basis_columns']),dec(q['v']);y=np.linalg.solve(s,x);b=np.linalg.solve(s,a@s)
  close(dec(r['new_coordinates']),y);close(dec(r['new_operator']),b);close(dec(r['gram']),s.conj().T@s)
  close(r['gram_squared_length'],np.vdot(x,x).real)
 elif t=='classify':
  a=dec(q['matrix']);refs={'hermitian':(a,a.conj().T),'unitary':(a.conj().T@a,np.eye(len(a))),'normal':(a.conj().T@a,a@a.conj().T),'idempotent':(a@a,a)}
  for k,(x,y) in refs.items():assert r['identity_tests'][k]['passed']==bool(np.all(abs(x-y)<=q['tolerance']['atol']+q['tolerance']['rtol']*abs(y)))
  assert r['orthogonal_projector_within_budget']==(r['identity_tests']['hermitian']['passed'] and r['identity_tests']['idempotent']['passed'])
 elif t=='decompose':
  a=dec(q['matrix']);close(dec(r['reconstruction']),a)
  if q['kind']=='hermitian':
   vals,vec=np.linalg.eigh(a);close(r['eigenvalues'],vals);u=dec(r['eigenvectors_columns']);close(a@u,u*np.array(r['eigenvalues']))
   # Compare whole eigenspace projectors, grouping repeated eigenvalues.
   for v in np.unique(np.round(vals,9)):
    mask=abs(vals-v)<1e-8;close(u[:,mask]@u[:,mask].conj().T,vec[:,mask]@vec[:,mask].conj().T)
  else:
   u,vals,vh=np.linalg.svd(a,full_matrices=True);close(r['singular_values'],vals);rank=int(sum(vals>q.get('rank_rtol',1e-12)*vals[0]));assert r['numerical_rank']==rank
   v=vh.conj().T;close(dec(r['right_numerical_kernel_projector']),v[:,rank:]@v[:,rank:].conj().T)
 elif t=='function':
  a=dec(q['matrix']);n=len(a)
  if q['kind']=='polynomial':ref=sum((complex(*c)*np.linalg.matrix_power(a,k) for k,c in enumerate(q['coefficients'])),start=np.zeros_like(a))
  elif np.allclose(a@a,0,atol=0,rtol=0):ref=np.eye(n)+a
  elif np.allclose(a-np.diag(np.diag(a)),0,atol=0,rtol=0):ref=np.diag(np.exp(np.diag(a)))
  elif n==2 and a[0,0]==a[1,1] and a[1,0]==0:ref=np.exp(a[0,0])*(np.eye(n)+a-a[0,0]*np.eye(n))
  else:
   vals,vec=np.linalg.eig(a);ref=vec@np.diag(np.exp(vals))@np.linalg.inv(vec)
  close(dec(r['value']),ref)
 elif t=='solve':
  a,b=dec(q['matrix']),dec(q['rhs']);x=np.linalg.solve(a,b);close(dec(r['solution']),x);close(r['condition_2'],np.linalg.cond(a))
  if 'candidate' in q:
   c=dec(q['candidate']);res=np.linalg.norm(b-a@c);close(r['candidate']['residual_2'],res)
   assert r['candidate']['candidate_forward_accuracy_certified'] is False
   if np.linalg.norm(b):close(r['candidate']['relative_forward_error_bound_2'],np.linalg.cond(a)*res/np.linalg.norm(b))
   else:assert r['candidate']['relative_forward_error_bound_2'] is None
 elif t=='check':
  a,b=dec(q['actual']['values']),dec(q['reference']['values']);passed=bool(np.all(abs(a-b)<=q['tolerance']['atol']+q['tolerance']['rtol']*abs(b)));assert o['status']==('within_tolerance' if passed else 'outside_tolerance')

def main():
 p=argparse.ArgumentParser();p.add_argument('--record',action='store_true');args=p.parse_args();assert sys.version_info[:2]==(3,12)
 hashes={str(f.relative_to(PACKAGE)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(PACKAGE.rglob('*')) if f.is_file() and '__pycache__' not in str(f)};assert hashes==json.loads((EVIDENCE/'package-freeze.json').read_text())['sha256']
 cases=[]
 def add(name,cat,q,status='verified'):cases.append(dict(name=name,category=cat,request=q,expected_status=status))
 for name,op,fields in [('inner_conjugate','inner',{'v':enc([1,1j]),'w':enc([2,1+1j])}),('outer_complex','outer',{'v':enc([1j,2]),'w':enc([1+2j,-1j,3])}),('adjoint_rectangular','adjoint',{'matrix':enc([[1,2j,3],[4j,5,6j]])}),('matvec_rectangular','matvec',{'matrix':enc([[1,2j,3],[4,5,6]]),'v':enc([1j,2,3j])}),('ordered_product','matmul',{'left':enc([[1,1j],[0,1]]),'right':enc([[0,1],[1,0]])})]:add(name,'normal',request('algebra',operation=op,**fields))
 for name,s in [('nonorthogonal',[[1,1],[0,1]]),('complex_orthonormal',np.array([[1,1],[1j,-1j]])/math.sqrt(2)),('uniform_tiny',1e-15*np.eye(2))]:add(name,'normal',request('basis',matrix=enc([[0,1],[1,0]]),basis_columns=enc(s),v=enc([2j,3]),direction='passive-new-in-old',max_condition=1e8))
 for name,a in [('hermitian',[[2,1j],[-1j,2]]),('unitary',np.diag([1,1j])),('oblique',[[1,1],[0,0]]),('nilpotent',[[0,1],[0,0]]),('zero',np.zeros((2,2)))]:add('classify_'+name,'normal',request('classify',matrix=enc(a)))
 for name,a in [('complex',[[2,1j],[-1j,2]]),('degenerate',np.diag([2,2,0])),('zero',np.zeros((3,3)))]:add('spectral_'+name,'boundary' if name!='complex' else 'normal',request('decompose',kind='hermitian',matrix=enc(a)))
 for name,a in [('wide',[[3,0,0],[0,0,4j]]),('tall',[[1,0],[0,2j],[0,0]]),('zero',np.zeros((3,2))),('repeated',np.diag([2,2,0])),('tiny_retained',np.diag([1,1e-13]))]:add('svd_'+name,'boundary',request('decompose',kind='svd',matrix=enc(a)))
 add('nilpotent_polynomial','normal',request('function',kind='polynomial',units='dimensionless',matrix=enc([[0,1],[0,0]]),coefficients=enc([2,3j,-1])))
 for name,a in [('nilpotent',[[0,.5j],[0,0]]),('diagonal',np.diag([.3j,-.7j])),('jordan',[[.13j,.237-.119j],[0,.13j]]),('hermitian',[[.2,.1j],[-.1j,.3]])]:add('exp_'+name,'normal',request('function',kind='exp',units='dimensionless',matrix=enc(a)))
 add('solve_generic','normal',request('solve',matrix=enc([[2,1j],[1,-1]]),rhs=enc([1j,2]),max_condition=1e8))
 add('solve_zero_rhs','boundary',request('solve',matrix=enc(np.eye(2)),rhs=enc([0,0]),candidate=enc([1,0]),max_condition=1e8))
 q=request('solve',matrix=enc(np.diag([1,2**-30])),rhs=enc([1,0]),candidate=enc([1,1]),max_condition=1e10);q['tolerance']={'atol':1e-8,'rtol':0};add('small_residual_large_error','boundary',q)
 def checkq(actual,reference,shape=None):
  if shape is None:shape=[len(actual)]
  item=lambda v:dict(shape=shape,dtype='complex128',device='cpu',values=enc(v))
  return request('check',actual=item(actual),reference=item(reference))
 add('literal_phase_is_different','boundary',checkq([1j],[1]),'outside_tolerance')
 add('check_same','normal',checkq([1j,2],[1j,2]),'within_tolerance')
 q=checkq([0],[1e-12]);q['tolerance']={'atol':0,'rtol':1e-8};add('tiny_signal_relative_only','boundary',q,'outside_tolerance')
 q=checkq([1e-9+1e-9j],[0]);q['tolerance']={'atol':1e-9,'rtol':0};add('complex_modulus_not_components','boundary',q,'outside_tolerance')
 q=checkq([0],[0]);q['actual']['shape']=[1,1];add('broadcast_shape','error',q,'invalid_input')
 q=checkq([1],[1]);q['actual']['dtype']='float32';add('dtype_mismatch','error',q,'invalid_input')
 q=checkq([1],[1]);q['actual']['device']='cuda';add('device_mismatch','error',q,'invalid_input')
 for name,q,status in [('singular_basis',request('basis',matrix=enc(np.eye(2)),basis_columns=enc([[1,0],[0,0]]),v=enc([1,0]),direction='passive-new-in-old',max_condition=1e8),'invalid_input'),('active_ambiguous',request('basis',matrix=enc(np.eye(2)),basis_columns=enc(np.eye(2)),v=enc([1,0]),direction='active',max_condition=1e8),'unsupported'),('condition_limit',request('solve',matrix=enc(np.diag([1,1e-10])),rhs=enc([1,0]),max_condition=1e8),'unsupported'),('tiny_nonhermitian',request('decompose',kind='hermitian',matrix=enc([[0,1e-15j],[0,0]])),'invalid_input'),('non_square_spectral',request('decompose',kind='hermitian',matrix=enc([[1,2,3],[4,5,6]])),'invalid_input'),('physical_function',request('function',kind='exp',matrix=enc(np.eye(2)*.1),units='J'),'unsupported'),('exponential_bound',request('function',kind='exp',matrix=enc(np.eye(2)*1.1),units='dimensionless'),'unsupported'),('log_branch',request('function',kind='log',matrix=enc(-np.eye(2)),units='dimensionless'),'unsupported'),('shape_inner',request('algebra',operation='inner',v=enc([1]),w=enc([1,2])),'invalid_input'),('bool_tolerance',{**request('classify',matrix=enc(np.eye(2))),'tolerance':{'atol':True,'rtol':0}},'invalid_input'),('loose_tolerance',{**request('classify',matrix=enc(np.eye(2))),'tolerance':{'atol':1e-3,'rtol':0}},'invalid_input'),('extra_field',{**request('classify',matrix=enc(np.eye(2))),'shots':100},'invalid_input')]:add(name,'error',q,status)
 q=request('classify',matrix=enc(np.eye(2)));q.pop('tolerance');add('missing_tolerance','error',q,'invalid_input')
 add('new_rectangular_product','author-transfer',request('algebra',operation='matmul',left=enc([[.17+.29j,-.63j,1.19]]),right=enc([[.83j,.13],[-.41,.37j],[.59,-.71]])))
 add('new_nonnormal_polynomial','author-transfer',request('function',kind='polynomial',units='dimensionless',matrix=enc([[.17j,.31-.41j],[.23j,-.19]]),coefficients=enc([.61j,-.37,1.13j,.29])))
 add('new_basis','author-transfer',request('basis',matrix=enc([[.3,.2j],[-.7j,.9]]),basis_columns=enc([[1,.217j],[.137,1]]),v=enc([.613j,-.791]),direction='passive-new-in-old',max_condition=100))
 logs=[];codes={'verified':0,'within_tolerance':0,'outside_tolerance':1,'invalid_input':2,'unsupported':3}
 with tempfile.TemporaryDirectory(prefix='mqc-algebra-author-') as tmp:
  pkg=Path(tmp)/PACKAGE.name;shutil.copytree(PACKAGE,pkg)
  for c in cases:
   p=subprocess.run([sys.executable,str(pkg/'scripts/algebra.py')],input=json.dumps(c['request']),text=True,capture_output=True,timeout=60);o=json.loads(p.stdout)
   assert o['status']==c['expected_status'] and p.returncode==codes[c['expected_status']] and not p.stderr,(c['name'],o,p.stderr)
   if o['status'] in ('verified','within_tolerance','outside_tolerance'):verify(c['request'],o)
   if c['name']=='small_residual_large_error':assert o['result']['candidate']['residual_within_elementwise_budget'] and o['result']['candidate']['observed_distance_to_computed_solution_2']==1
   logs.append({**c,'actual_stdout':o,'actual_stderr':p.stderr,'actual_exit_code':p.returncode,'passed':True})
  for name,raw in [('nan','{"x":NaN}'),('duplicate','{"task":"a","task":"b"}'),('syntax','{')]:
   p=subprocess.run([sys.executable,str(pkg/'scripts/algebra.py')],input=raw,capture_output=True,text=True);o=json.loads(p.stdout);assert p.returncode==2
   logs.append(dict(name=name,category='error',raw_request=raw,actual_stdout=o,actual_stderr=p.stderr,actual_exit_code=p.returncode,passed=True))
 report=dict(skill=PACKAGE.name,version='0.1.0',passed=len(logs),counts=dict(Counter(c['category'] for c in logs)),actual_flagquantum_circuits=0,author_helper_calls=len(logs),package_sha256=hashes,environment={'python':platform.python_version(),'numpy':np.__version__},reference='Separate NumPy indexed algebra/LAPACK, analytic nilpotent/Jordan functions, exact diagonal conditioned examples and subspace-projector checks; NumPy and Torch may share numerical backend families, not independent proofs',evaluator_role='author/conductor',scientific_acceptance='pending',reader_trial='not run',cases=logs)
 if args.record:
  path=EVIDENCE/'author-report.json';assert not path.exists();path.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ('passed','counts','actual_flagquantum_circuits')}))
if __name__=='__main__':main()
