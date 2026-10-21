#!/private/tmp/mqc-writing-venv/bin/python
"""Blind paper-claim audit. Rerun in a fresh --output directory; no input files changed."""
import argparse, cmath, hashlib, json, math, platform, subprocess, sys
from pathlib import Path
from importlib.metadata import version

P=Path('/private/tmp/mqc-paper-transfer/packet')
p=argparse.ArgumentParser();p.add_argument('--output',default=str(Path(__file__).parent/'evidence'));args=p.parse_args()
O=Path(args.output);O.mkdir(parents=True,exist_ok=True)
eps=1e-10; calls=[]
def save(path,obj):
    Path(path).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')
def enc(v):
    if isinstance(v,list):return [enc(x) for x in v]
    z=complex(v);return [z.real,z.imag]
def call(name,skill,script,q):
    d=O/name;d.mkdir(exist_ok=False);save(d/'request.json',q)
    cmd=[sys.executable,str(P/'skills'/skill/'scripts'/script)]
    r=subprocess.run(cmd,input=json.dumps(q),capture_output=True,text=True,timeout=90)
    (d/'stdout.json').write_text(r.stdout);(d/'stderr.txt').write_text(r.stderr)
    a=json.loads(r.stdout)
    circuits=a.get('actual_flagquantum_circuits',len(a.get('records',[])) if script=='interference.py' else 0)
    meta={'command':cmd,'exit_code':r.returncode,'actual_flagquantum_circuits':circuits,'status':a.get('status'),'request_sha256':hashlib.sha256((d/'request.json').read_bytes()).hexdigest()}
    save(d/'execution.json',meta);calls.append(dict(name=name,**meta))
    assert not r.stderr, r.stderr
    assert r.returncode==({'verified':0,'within_tolerance':0,'outside_tolerance':1}[a['status']])
    return a
def alg(name,**kw):
    return call(name,'translate-complex-linear-algebra','algebra.py',dict(task='algebra',coordinates='literal-complex',tolerance={'atol':eps,'rtol':0},**kw))
def compare(name,a,b,kind='state',mode='coordinates'):
    return call(name,'compare-quantum-states-and-operators','compare.py',dict(kind=kind,mode=mode,basis_a=['0','1'],basis_b=['0','1'],a=enc(a),b=enc(b),atol=eps))
def interference(name,phases,delta):
    return call(name,'reproduce-qubit-interference','interference.py',dict(profile='ideal-pure-single-qubit',state=enc([s,s]),basis=['0','1'],angle_unit='radian',phase_radians=phases,readout={'type':'phase-h','delta_radians':delta},atol=eps))

runtime={'implementation':platform.python_implementation(),'python':platform.python_version(),'packages':{x:version(x) for x in ['numpy','scipy','torch','flagquantum']}}
save(O/'runtime.json',runtime)
s=1/math.sqrt(2);H=[[s,s],[s,-s]];R=[[s,-s],[s,s]];Z=[[1,0],[0,-1]]
first=alg('01-first-H-preparation',operation='matvec',matrix=enc(H),v=enc([1,0]))
rot=call('02-first-Ry-pulse','translate-unitary-evolution','unitary.py',dict(task='rotation',basis=['0','1'],state=enc([1,0]),context='isolated',axis=[0,1,0],angle={'value':math.pi/2,'unit':'radian'},atol=eps))
cp=compare('03-first-pulse-state', [s,s],[complex(*x) for x in rot['records'][0]['statevector']])
op=compare('04-H-vs-Ry-operator',H,R,kind='unitary',mode='global-phase')
hz=alg('05-correct-analyzer-HZ',operation='matmul',left=enc(H),right=enc(Z))
matrix_agreement=compare('06-HZ-vs-Ry',[ [complex(*z) for z in row] for row in hz['result']['value']],R,kind='unitary')
phases=[0,math.pi/2,math.pi,2*math.pi,0.23*math.pi,1.37*math.pi]
candidate=interference('07-C1-candidate-same-H',phases,0)
corrected=interference('08-C1-corrected-analyzer',phases,math.pi)
x=[0.23,1.37];converted=[math.pi*v for v in x]
unconverted=interference('09-C2-candidate-unchanged',x,math.pi)
converted_run=interference('10-C2-converted-radians',converted,math.pi)
paper=lambda phi:(1-math.cos(phi))/2
c1=[{'phase_radians':phi,'candidate_Pg':a['probabilities'][0],'corrected_Pg':b['probabilities'][0],'paper_Pg':paper(phi),'candidate_absolute_error':abs(a['probabilities'][0]-paper(phi)),'corrected_absolute_error':abs(b['probabilities'][0]-paper(phi))} for phi,a,b in zip(phases,candidate['records'],corrected['records'])]
c2=[{'figure_x_pi_units':v,'required_phase_radians':phi,'candidate_input_radians':v,'candidate_Pg':a['probabilities'][0],'converted_Pg':b['probabilities'][0],'paper_Pg':paper(phi),'absolute_discrepancy':abs(a['probabilities'][0]-b['probabilities'][0])} for v,phi,a,b in zip(x,converted,unconverted['records'],converted_run['records'])]
assert max(row['corrected_absolute_error'] for row in c1)<=eps
assert max(row['candidate_absolute_error'] for row in c1)>eps
assert all(row['absolute_discrepancy']>eps for row in c2)
assert cp['status']=='within_tolerance' and op['status']=='outside_tolerance' and matrix_agreement['status']=='within_tolerance'
result={
 'status':'completed','tolerance':{'atol':eps,'rtol':0,'probabilities':'maximum absolute; no relative allowance','comparison_helper':'Euclidean/Frobenius absolute 1e-10, not entrywise substitution'},
 'source':{'url':'https://arxiv.org/pdf/1608.04908v1','local_path':str(P/'paper.pdf'),'sha256':hashlib.sha256((P/'paper.pdf').read_bytes()).hexdigest(),'pages':[2,3],'inspection':'Extracted complete relevant pages and visually inspected both rendered pages. No paper text copied into result artifact.','locators':{'C1':'p.2, left column Ramsey discussion, paragraph before Eq.(2) and vacuum-WPD paragraph after Eq.(2); p.3 opening continuation about pulse phase','C2':'p.3, Fig.2 panels (a),(b), horizontal phase axes labelled phi (pi)','C3':'p.2 Eqs.(2)-(4); p.3 Fig.2 caption and cavity tomography discussion / Fig.3 / conditional post-selection discussion'}},
 'runtime':runtime,
 'derivation':{'basis':'g=0, e=1 is an explicit audit convention, not independently fixed by named pulse labels','D':'diag(1,exp(i phi)); vacuum coupling acts as identity','candidate':'H D(phi) H |0> = ((1+exp(i phi))/2,(1-exp(i phi))/2); Pg=(1+cos phi)/2','paper_consistent_example':'Ry(pi/2) D(phi) Ry(pi/2)|0> = ((1-exp(i phi))/2,(1+exp(i phi))/2); Pg=(1-cos phi)/2','pulse_matrices':{'standard_H':enc(H),'paper_consistent_Ry_pi_over_2':enc(R),'second_analyzer_equivalence':'Ry(pi/2)=H Z. In supplied interference helper use delta=pi, meaning D(-pi) then H. First pulse may be H or Ry(pi/2) on |0>, but these are not equal operators.'},'limits':'This supplies one consistent ideal convention; the quoted text does not uniquely specify the full microwave pulse matrices, axes, rotating frame, or phases.'},
 'claims':{
 'C1':{'disposition':'partially supported; compound claim rejected','supported':'The first-pulse plus superposition is explicitly stated. g=0 is a legitimate declared convention.','rejected':'Using standard H for both named pulses and the stated plus phase with g=0 yields the complementary ground-state fringe.','counterexample':c1[0],'fresh_candidate_helper_status':candidate['status'],'fresh_corrected_helper_status':corrected['status'],'claim_accepted':False,'records':c1,'operator_comparison_status':op['status'],'operator_residual':op['decision_residual']},
 'C2':{'disposition':'rejected','reason':'Figure coordinates are phi/pi (axis phi (pi)), so phi_radians=pi*x. A phase plot does not imply numeric axis values already in radians.','source_x':x,'converted_radians':converted,'records':c2,'claim_accepted':False,'fresh_candidate_helper_status':unconverted['status'],'fresh_corrected_helper_status':converted_run['status']},
 'C3':{'disposition':'rejected as unsupported overreach','claim_accepted':False,'verified_scope':'Ideal pure single-qubit vacuum-WPD Ramsey limit only, under the explicitly chosen pulse/readout convention.','countermodel':'A bare isolated qubit with the same preparation, phase and analyzer yields the identical ideal vacuum fringe without any cavity, eraser, noise model or hardware. The matched scalar curve cannot identify those extra mechanisms.','missing_required_evidence':['Joint qubit-cavity Hilbert-space state and entangling interaction, coherent/cat-state preparation, finite overlaps and phase conventions','Specified erasure/post-selection measurement instrument, outcomes and conditional probabilities; a pure qubit phase scan contains no eraser','Open-system dynamics and independently specified decoherence/Kerr parameters, appropriate mixed-state/channel solver and convergence checks','Actual experimental data, acquisition/measurement-error model and statistical comparison; simulator probabilities are not hardware counts'],'source_specific_scope':'Fig.2 distinguishes symbols as measured data and solid lines as simulations including decoherence and Kerr imperfections. Fig.3 addresses cavity tomography; its evidence cannot be inferred from a vacuum statevector scan.'}},
 'missing_assumptions':['Unique physical pulse matrices are not fixed by the name Hadamard: choose/calibrate axes, phase reference and readout mapping before claiming a physical implementation.','Figure x must be multiplied by pi; retained source coordinates and converted values are recorded.','A mathematically separated phase D(phi) represents the described tunable relative phase; p.3 says the actual experimental phase is incorporated in H1.','No time, generator, hbar, cavity parameters or noise rates were invented for a physical evolution claim.'],
 'acceptance_separation':'All verified helper runs establish their explicitly declared ideal computations. Candidate claims were evaluated separately against the paper and fresh numerical results; verified candidate helper status is not candidate scientific acceptance.',
 'actual_counts':{'helper_calls':len(calls),'flagquantum_circuits':sum(c['actual_flagquantum_circuits'] for c in calls),'classical_algebra_calls':2,'comparison_calls':3,'unitary_helper_calls':1,'interference_helper_calls':4,'hardware_executions':0,'shots':0,'noise_simulations':0,'joint_qubit_cavity_simulations':0,'human_scientific_reviews':0},'calls':calls,
 'scientific_acceptance':'No claim of human scientific review or whole-paper reproduction.'}
save(O.parent/'result.json',result)
save(O/'call-ledger.json',calls)
print(json.dumps({'result':str(O.parent/'result.json'),'counts':result['actual_counts'],'C1_max_error':max(row['candidate_absolute_error'] for row in c1),'C2':c2}))
