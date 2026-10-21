#!/private/tmp/mqc-writing-venv/bin/python
"""Reproduce this bounded independent transfer trial; never modifies supplied packet."""
from pathlib import Path
import cmath, hashlib, json, math, subprocess, sys
import numpy as np
from scipy.linalg import expm
from importlib.metadata import version
ROOT=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/private/tmp/mqc-paper-transfer/b')
ROOT.mkdir(parents=True,exist_ok=True)
PACKET=Path('/private/tmp/mqc-paper-transfer/packet')
PYTHON='/private/tmp/mqc-writing-venv/bin/python'
def save(name,x):
 (ROOT/name).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def enc(a):
 if isinstance(a,(list,tuple,np.ndarray)):return [enc(z) for z in a]
 z=complex(a);return [z.real,z.imag]
def dec(a):
 if len(a)==2 and all(type(z) in (float,int) for z in a):return complex(*a)
 return [dec(z) for z in a]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
t=0.83e-9; f=125e6; omega=2*math.pi*f; kappa=0.17/t; theta=omega*t; eps=1e-10
G=np.diag([kappa,kappa-omega]); initial=np.array([1,1],dtype=complex)/math.sqrt(2)
scan=[0,math.pi/2,math.pi,3*math.pi/2,2*math.pi]
request={'profile':'constant-qubit-interference','generator':{'matrix':enc(G),'unit':'rad/s'},'time':{'value':0.83,'unit':'ns'},'initial_state':enc(initial),'basis':['0','1'],'phase_scan':{'values':scan,'unit':'radian'},'analyzer':{'delta':math.pi,'unit':'radian'},'tolerance':{'coordinate_atol':eps,'rtol':0},'phase_context':'full-coordinates-with-controlled-witness'}
save('request.json',request)
cmd=[PYTHON,str(PACKET/'four_skill_interference.py'),'--request',str(ROOT/'request.json'),'--output',str(ROOT/'run'),'--skills-root',str(PACKET/'skills')]
p=subprocess.run(cmd,capture_output=True,text=True)
(ROOT/'runner.stdout.txt').write_text(p.stdout);(ROOT/'runner.stderr.txt').write_text(p.stderr)
save('runner.execution.json',{'command':cmd,'exit_code':p.returncode,'request_sha256':sha(ROOT/'request.json')})
report=json.loads((ROOT/'run/report.json').read_text())
# Independent reference: SciPy dense matrix exponential and full pulse matrices,
# plus a separate scalar cmath formula. No skill/runner imports or helper outputs
# enter the construction of these references.
H1=np.array([[1,-1],[1,1]],dtype=complex)/math.sqrt(2); H2=H1.copy()
U=expm(-1j*G*t)
Uscalar=np.diag([cmath.exp(-0.17j),cmath.exp(-0.17j+1j*theta)])
prepared=H1@np.array([1,0],dtype=complex); evolved=U@prepared
ind=[]; max_coord=max_prob=0.
for phi,actual in zip(scan,report.get('outputs',[])):
 D=np.diag([1,cmath.exp(1j*phi)])
 state=H2@D@U@prepared
 scalar=np.array([cmath.exp(-0.17j)*(1-cmath.exp(1j*(theta+phi)))/2,cmath.exp(-0.17j)*(1+cmath.exp(1j*(theta+phi)))/2])
 prob=np.abs(state)**2; scalar_prob=np.array([(1-math.cos(theta+phi))/2,(1+math.cos(theta+phi))/2])
 measured=np.array(dec(actual['statevector'])); measured_p=np.array(actual['probabilities'])
 errors={'coordinate_max_absolute':float(max(abs(measured-state))),'probability_max_absolute':float(max(abs(measured_p-prob))),'matrix_vs_scalar_coordinate':float(max(abs(state-scalar))),'born_vs_cosine_probability':float(max(abs(prob-scalar_prob)))}
 max_coord=max(max_coord,errors['coordinate_max_absolute']); max_prob=max(max_prob,errors['probability_max_absolute'])
 ind.append({'additional_scan_phase_radians':phi,'total_relative_phase_radians':theta+phi,'actual_state':actual['statevector'],'actual_probabilities':actual['probabilities'],'reference_state':enc(state),'scalar_reference_state':enc(scalar),'reference_probabilities':prob.tolist(),'errors':errors})
unit_error=float(np.max(abs(U-Uscalar)))
save('independent-reference.json',{'method':'SciPy expm and explicit full pulse matrices; independent scalar cmath/cosine formula; no helper/runner imports','runtime':{'python':sys.version,'numpy':version('numpy'),'scipy':version('scipy')},'generator_rad_per_s':enc(G),'dimensionless_exponent':enc(G*t),'U':enc(U),'U_scalar':enc(Uscalar),'U_max_absolute_error':unit_error,'state_after_first_pulse':enc(prepared),'state_after_evolution':enc(evolved),'records':ind})
calls=report.get('helper_calls',[]); skills={}
for c in calls:
 name=c['skill']; skills[name]=skills.get(name,0)+1
counts={'composition_runner_calls':1,'skill_helper_calls':len(calls),'calls_by_skill':skills,'actual_flagquantum_circuits':report.get('actual_flagquantum_circuits',0),'independently_checked_final_scan_points':len(ind),'independent_reference_quantum_circuits':0,'circuit_breakdown':{'unitary_evolution':9,'interference':len(scan),'continuous_composition':len(scan)}}
passed=p.returncode==0 and report['status']=='verified' and len(ind)==len(scan) and max_coord<=eps and max_prob<=eps and unit_error<=eps
result={'status':'verified' if passed else 'failed','claim_scope':'Compatible ideal convention for vacuum-WPD Ramsey fringe only, and a caller-specified new constant-generator instance. Not a whole-paper reproduction.','source':{'url':'https://arxiv.org/pdf/1608.04908v1','supplied_pdf_sha256':sha(PACKET/'paper.pdf'),'locators':['PDF page 2, Figure 1d and caption','PDF page 2, left column vacuum-WPD Ramsey discussion following Eq. (2)','PDF page 3, opening left-column paragraph'],'reading_method':'Visually inspected rendered PDF pages 2–3; source prose/images are not embedded in result.'},'source_vs_new_instance_ledger':{'source_supported':['Ramsey sequence with two balanced qubit operations, relative phase, cavity as WPD, final computational readout.','Vacuum WPD does not collect path information in this ideal case.','Ground-state fringe is (1-cos(phi))/2.','Experimental phase is incorporated into the first microwave pulse by adjusting its phase (page 3).'],'explicit_chosen_convention':['Basis |0>=|g>, |1>=|e>; column state vectors and left matrix action.','H1=H2=Ry(pi/2)= [[1,-1],[1,1]]/sqrt(2), both full matrices including chosen phases.','H1 prepares (|g>+|e>)/sqrt(2); final H2 gives the source minus-cosine ground readout.','Skill analyzer H D(-delta), delta=pi, equals chosen H2; chronological analyzer calls D(-pi), H.','Physical pulse phases, axes and common phase are not uniquely identified by the population curve; these matrices are an explicit compatible completion.','Caller evolution is placed between preparation and analysis; that mathematical new instance is distinct from the source implementation of phase in H1.'],'caller_new_instance':{'cyclic_frequency_hz':f,'duration_ns':0.83,'imposed_identity_phase_radians':0.17,'source_reported_parameter':False},'additional_chosen_checks':{'extra_phase_scan_radians':scan,'interpretation':'Each scan phase is added after the new fixed evolution; first point phi_extra=0 is the requested new endpoint.','coherent_control_witness':'Auxiliary mathematical phase-scope check supplied by runner; not claimed as the paper apparatus.'}},'derivation':{'sign_convention':'Positive excited-amplitude relative phase means c_e/c_g gains exp(+i*omega*t); with U=exp(-iGt), G= kappa I - omega |e><e|.','cyclic_to_angular':'omega=2*pi*f; rad/s generator already equals H/hbar, so no hbar division is applied.','omega_rad_per_s':omega,'kappa_rad_per_s':kappa,'t_seconds':t,'relative_phase_radians':theta,'identity_phase_factor':enc(cmath.exp(-0.17j)),'generator_rad_per_s':enc(G),'dimensionless_exponent':enc(G*t),'full_U':enc(Uscalar),'full_preanalyzer_state':enc([cmath.exp(-0.17j)/math.sqrt(2),cmath.exp(-0.17j+1j*theta)/math.sqrt(2)]),'full_final_state_formula':'exp(-i*0.17)/2 * [1-exp(i*(theta+phi_extra)), 1+exp(i*(theta+phi_extra))]','probabilities_formula':'[(1-cos(theta+phi_extra))/2, (1+cos(theta+phi_extra))/2]','decomposition_phase_caution':'Imposed kappa*t=0.17 is distinct from canonical ZYZ alpha and from total trace phase; retain the full generator and U.'},'new_instance_endpoint':ind[0] if ind else None,'numerical_acceptance':{'coordinate_and_probability_atol':eps,'rtol':0,'max_final_coordinate_error':max_coord,'max_final_probability_error':max_prob,'max_U_error':unit_error,'all_pass':passed,'comparison_metric_conversion':report.get('tolerance_ledger'),'phase_witness':report.get('phase_witness'),'note':'Final coordinate max errors checked independently; Euclidean/Frobenius helper budgets are separately declared.'},'actual_counters':counts,'runtime':{'python':sys.version,'flagquantum':version('flagquantum'),'torch':version('torch'),'numpy':version('numpy'),'scipy':version('scipy')},'unsupported_broader_claims':['Unique calibrated physical pulse matrices or a uniquely inferred generator from population data.','Reproduction of cavity coherent-state/cat-state entanglement, tomography, delayed-choice postselection, decoherence, hardware fidelities, or experimental counts.','Experimental use of the caller frequency, duration, identity offset, extra scan, or auxiliary controlled witness.','Global phase observability in isolated computational populations; full coordinates retained by contract and controlled diagnostic gives a separate context.','Exact symbolic theorem or full continuous-scan experimental validation from finite samples.'],'evidence_files':['request.json','runner.execution.json','runner.stdout.txt','runner.stderr.txt','run/report.json','run/continuous-circuit.json','run/handoff-envelope.json','independent-reference.json','reproduce.py'],'runner_sha256':sha(PACKET/'four_skill_interference.py')}
save('result.json',result)
print(json.dumps({'status':result['status'],'counters':counts,'errors':result['numerical_acceptance'],'endpoint':result['new_instance_endpoint']},indent=2))
raise SystemExit(0 if passed else 1)
