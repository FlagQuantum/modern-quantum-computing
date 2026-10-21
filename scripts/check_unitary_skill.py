#!/usr/bin/env python3
"""Author regression of phase-tracked evolution; independent NumPy eigensystem oracle."""
import argparse,copy,hashlib,json,math,platform,subprocess,sys,tempfile,shutil
from pathlib import Path
from collections import Counter
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT/'skills/translate-unitary-evolution'
EVIDENCE=ROOT/'book/skill-evaluations/unitary-evolution-v0.1.0'
def enc(x):
    a=np.asarray(x);return np.stack((a.real,a.imag),axis=-1).tolist()
def dec(x):
    a=np.asarray(x);return a[...,0]+1j*a[...,1]
def oracle(q):
    if q['task']=='factor':return dec(q['unitary'])
    if q['task']=='rotation':
        x,y,z=q['axis'];e=q['angle']['value']/2*np.array([[z,x-1j*y],[x+1j*y,-z]])
    else:
        e=dec(q['generator']['matrix']);u=q['generator']['unit'];t=q['time']['value']
        if q['time']['unit']=='ns':t*=1e-9
        if u in ('J','eV'):t/=q['hbar']['value']
        e=e*t
    vals,vec=np.linalg.eigh(e);return (vec*np.exp(-1j*vals))@vec.conj().T

def verify(q,out):
    u=oracle(q);np.testing.assert_allclose(dec(out['unitary']),u,rtol=0,atol=q.get('atol',1e-10))
    np.testing.assert_allclose(dec(out['reconstructed_full_matrix']),u,rtol=0,atol=q.get('atol',1e-10))
    v=dec(out['native_zyz_matrix']);alpha=out['zyz']['alpha']
    np.testing.assert_allclose(np.exp(1j*alpha)*v,u,rtol=0,atol=q.get('atol',1e-10))
    cu=np.eye(4,dtype=complex);cu[2:,2:]=u
    cv=np.eye(4,dtype=complex);cv[2:,2:]=v
    for r in out['records']:
        initial=dec(q['state']) if r['input_label'] in ('supplied','coherent-control') else np.array([1,0]) if r['input_label']=='zero' else np.array([0,1])
        if r['path'].startswith('controlled'):
            initial=np.kron([1/math.sqrt(2)]*2,initial);mat=cv if r['path']=='controlled-unrepaired' else cu
        else:mat=v if r['path']=='native-zyz' else u
        expected=mat@initial
        np.testing.assert_allclose(dec(r['statevector']),expected,rtol=0,atol=q.get('atol',1e-10))
        np.testing.assert_allclose(r['probabilities'],abs(expected)**2,rtol=0,atol=q.get('atol',1e-10))
        assert r['device']=='cpu' and r['state_dtype']=='torch.complex128' and r['probability_dtype']=='torch.float64'
    assert out['runtime']['python'].startswith('3.12.') and out['versions']['flagquantum']=='0.3.1'
    return len(out['records'])
def main():
    p=argparse.ArgumentParser();p.add_argument('--record',action='store_true');a=p.parse_args()
    assert sys.version_info[:2]==(3,12)
    hashes={str(f.relative_to(PACKAGE)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(PACKAGE.rglob('*')) if f.is_file() and '__pycache__' not in str(f)}
    assert hashes==json.loads((EVIDENCE/'package-freeze.json').read_text())['sha256']
    base=dict(task='rotation',basis=['0','1'],state=enc([.6j,.8]),context='isolated',axis=[0,1,0],angle={'value':.7,'unit':'radian'})
    cases=[]
    def add(name,cat,q,status='verified'):cases.append(dict(name=name,category=cat,request=q,expected_status=status))
    def rot(axis,theta,context='isolated'):
        q=copy.deepcopy(base);q.update(axis=axis,angle={'value':theta,'unit':'radian'},context=context);return q
    def evo(g,t,gu='1',tu='1',h=None,context='isolated'):
        q={k:copy.deepcopy(base[k]) for k in ('basis','state')};q.update(task='evolve',context=context,generator={'matrix':enc(g),'unit':gu},time={'value':t,'unit':tu})
        if h is not None:q['hbar']=h
        return q
    def fac(u,context='isolated'):
        return dict(task='factor',basis=['0','1'],state=enc([.6j,.8]),context=context,unitary=enc(u))
    Y=np.array([[0,-1j],[1j,0]]);K=2*np.eye(2)+Y
    for name,g,t in [('zero',K,0),('negative_time',K,-.37),('trace_only',2*np.eye(2),.61),('generic_hermitian',[[.7,.2-.4j],[.2+.4j,-.3]],.83)]:add(name,'normal',evo(g,t))
    add('angular_seconds','normal',evo(K*1e8,2e-9,'rad/s','s'))
    add('angular_nanoseconds','normal',evo(K*1e8,2,'rad/s','ns'))
    for unit,h in [('J',1.054571817e-34),('eV',6.582119569e-16)]:add('energy_'+unit,'normal',evo(K*h*1e8,2,unit,'ns',{'value':h,'unit':unit+'*s'}))
    for j,axis in enumerate(([1,0,0],[0,1,0],[0,0,1],[-1,0,0])):add('cartesian_'+str(j),'normal',rot(axis,.917))
    for name,t in [('zero_rotation',0),('two_pi',2*math.pi),('four_pi',4*math.pi),('negative',-.73),('max_angle',64)]:add(name,'boundary',rot([1,0,0],t,'coherent-control'))
    for name,u in [('identity',np.eye(2)),('hadamard',np.array([[1,1],[1,-1]])/math.sqrt(2)),('pauli_x',[[0,1],[1,0]]),('pauli_y',Y),('phase_gate',np.diag([1,np.exp(.817j)]))]:add(name,'boundary',fac(u,'coherent-control'))
    for n,t in enumerate([1e-13,math.pi-1e-13,1e-9,math.pi-1e-9]):add('endpoint_'+str(n),'boundary',fac(np.exp(.31j)*oracle(rot([0,1,0],t))))
    for n,phase in enumerate([math.pi/2-1e-10,math.pi/2+1e-10,-math.pi/2]):add('det_branch_'+str(n),'boundary',fac(np.exp(1j*phase)*np.eye(2)))
    add('new_general_axis','author-transfer',rot([2/3,-1/3,2/3],1.137,'coherent-control'))
    add('new_complex_generator','author-transfer',evo([[.613,-.297+.419j],[-.297-.419j,-.183]],-.731,context='coherent-control'))
    add('new_full_unitary','author-transfer',fac(np.exp(-.719j)*oracle(rot([1/math.sqrt(3)]*3,.983)),'coherent-control'))
    errors=[('nonunit_axis',{'axis':[0,0,2]},'invalid_input'),('degree',{'angle':{'value':30,'unit':'degree'}},'unsupported'),('nonunit_state',{'state':enc([1,1])},'invalid_input'),('wrong_basis',{'basis':['1','0']},'unsupported'),('loose_atol',{'atol':.1},'invalid_input'),('bool_angle',{'angle':{'value':True,'unit':'radian'}},'invalid_input'),('oversize_angle',{'angle':{'value':65,'unit':'radian'}},'invalid_input'),('extra_key',{'shots':10},'invalid_input'),('time_dependent',{'task':'time-dependent'},'unsupported')]
    for name,change,status in errors:q=copy.deepcopy(base);q.update(change);add(name,'error',q,status)
    q=copy.deepcopy(base);q.pop('context');add('missing_context','error',q,'invalid_input')
    add('nonunitary','error',fac([[1,1],[0,1]]),'invalid_input')
    add('tiny_nonhermitian_zero_time','error',evo([[0,1e-24j],[0,0]],0,'J','ns',{'value':1e-34,'unit':'J*s'}),'invalid_input')
    add('missing_hbar','error',evo(K,1,'eV','ns'),'invalid_input')
    add('mismatched_hbar','error',evo(K,1,'eV','ns',{'value':1,'unit':'J*s'}),'invalid_input')
    add('double_hbar','error',evo(K,1,'rad/s','s',{'value':1,'unit':'J*s'}),'invalid_input')
    add('Hz_ambiguous','error',evo(K,1,'Hz','ns'),'unsupported')
    add('exponent_bound','error',evo(K,100),'invalid_input')
    add('dimensionless_time_mismatch','error',evo(K,1,'1','s'),'invalid_input')
    logs=[];count=0
    with tempfile.TemporaryDirectory(prefix='mqc-unitary-author-') as tmp:
        package=Path(tmp)/PACKAGE.name;shutil.copytree(PACKAGE,package)
        for case in cases:
            proc=subprocess.run([sys.executable,str(package/'scripts/unitary.py')],input=json.dumps(case['request']),text=True,capture_output=True,timeout=60)
            out=json.loads(proc.stdout);assert out['status']==case['expected_status'],(case['name'],out,proc.stderr)
            assert proc.returncode=={'verified':0,'invalid_input':2,'unsupported':3}[case['expected_status']] and not proc.stderr
            if out['status']=='verified':count+=verify(case['request'],out)
            logs.append({**case,'actual_exit_code':proc.returncode,'actual_stdout':out,'actual_stderr':proc.stderr,'passed':True})
        for name,raw in [('nan','{"x":NaN}'),('duplicate','{"task":"x","task":"y"}'),('syntax','{')]:
            proc=subprocess.run([sys.executable,str(package/'scripts/unitary.py')],input=raw,text=True,capture_output=True);out=json.loads(proc.stdout);assert proc.returncode==2 and out['status']=='invalid_input'
            logs.append(dict(name=name,category='error',raw_request=raw,actual_stdout=out,actual_exit_code=proc.returncode,actual_stderr=proc.stderr,passed=True))
    report=dict(skill=PACKAGE.name,version='0.1.0',evaluator_role='author/conductor',passed=len(logs),counts=dict(Counter(c['category'] for c in logs)),actual_flagquantum_circuits=count,package_sha256=hashes,reference='NumPy Hermitian eigendecomposition (not Torch matrix_exp or helper Pauli expansion); full complex coordinates and controlled branch repair',environment={'python':platform.python_version(),'numpy':np.__version__},scientific_acceptance='pending',reader_trial='not run',cases=logs)
    if a.record:
        path=EVIDENCE/'author-report.json';assert not path.exists();path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('passed','counts','actual_flagquantum_circuits')}))
if __name__=='__main__':main()
