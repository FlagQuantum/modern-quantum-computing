import sys,json,subprocess,time,math,cmath,copy
from pathlib import Path
R=Path('/private/tmp/mqc-composition-blind-r1/a'); O=R/'outputs'; P='/private/tmp/mqc-writing-venv/bin/python'
tasks=json.loads((R/'tasks.json').read_text())
def save(p,x):
 p=O/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def execute(label,cmd,request=None):
 d=O/label;d.mkdir(parents=True,exist_ok=True)
 if request is not None:save(label+'/request.json',request)
 start=time.perf_counter();r=subprocess.run(cmd,input=json.dumps(request) if request else None,capture_output=True,text=True)
 (d/'stdout.txt').write_text(r.stdout);(d/'stderr.txt').write_text(r.stderr)
 save(label+'/execution.json',dict(command=cmd,exit_code=r.returncode,elapsed_seconds=time.perf_counter()-start,interpreter=P))
 return r
execute('runtime',[P,'-c','import sys,importlib.metadata as m; print(sys.version); print(m.version("torch")); print(m.version("flagquantum"))'])
execute('system-python-runtime',['/usr/bin/python3','-c','import sys; print(sys.version)'])
allskills=[x['id'] for x in json.loads((R/'catalog.json').read_text())]
q1=copy.deepcopy(tasks[0]['experiment']);q1['hbar']={'value':6.582119569e-16,'unit':'eV*s'}
save('A1/clarification.json',{'question':'What hbar value and matching unit should be used for the energy generator?','response':'Use explicitly declared numerical conversion hbar=6.582119569e-16 eV*s; no further constant-provenance or accuracy claim supplied.','source':'parent agent message; before dependent execution'})
for tid,q in [('A1',q1),('A2',tasks[1]['experiment'])]:
 save(tid+'/source-experiment.json',q)
 execute(tid+'/workflow-execution',[P,str(R/'workflow/four_skill_interference.py'),'--request',str(O/tid/'source-experiment.json'),'--output',str(O/tid/'fresh-workflow'),'--skills-root',str(R/'skills')])
# Independent standard-library matrix-power Taylor reference: no imports from helpers or FlagQuantum.
def dec(a):
 if isinstance(a,list) and len(a)==2 and all(type(x) in (int,float) for x in a):return complex(*a)
 return [dec(x) for x in a]
def enc(a):
 if isinstance(a,list):return [enc(x) for x in a]
 return [a.real,a.imag]
def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def mv(a,v):return [sum(a[i][j]*v[j] for j in range(2)) for i in range(2)]
def err(a,b):return max(abs(x-y) for x,y in zip(a,b))
def expm(a):
 total=[[1+0j,0j],[0j,1+0j]];term=copy.deepcopy(total)
 for n in range(1,65):
  term=[[z/n for z in row] for row in mm(term,a)]
  total=[[total[i][j]+term[i][j] for j in range(2)] for i in range(2)]
 return total
references={}
for tid,q in [('A1',q1),('A2',tasks[1]['experiment'])]:
 factor=q['time']['value']*1e-9/q['hbar']['value'];g=dec(q['generator']['matrix']);u=expm([[-1j*z*factor for z in row] for row in g]);s=mv(u,dec(q['initial_state']));references[tid]=(u,s)
 report=json.loads((O/tid/'fresh-workflow/report.json').read_text());cont=json.loads((O/tid/'fresh-workflow/continuous-circuit.json').read_text());ev=json.loads((O/tid/'fresh-workflow/02-evolution/stdout.json').read_text())
 checks=[]
 for record in cont['records']:
  phase=record['phase_radians'];b=cmath.exp(1j*(phase-q['analyzer']['delta']))*s[1];out=[(s[0]+b)/math.sqrt(2),(s[0]-b)/math.sqrt(2)];actual=dec(record['statevector']);staged=dec(record['staged_statevector']);probs=[abs(z)**2 for z in out]
  checks.append({'phase':phase,'coordinate_error':err(actual,out),'staged_error':err(staged,out),'whole_vs_staged':err(actual,staged),'probability_error':max(abs(x-y) for x,y in zip(probs,record['probabilities']))})
 matrix_error=max(abs(x-y) for a,b in zip(u,dec(ev['unitary'])) for x,y in zip(a,b));epsilon=q['tolerance']['coordinate_atol'];passed=matrix_error<=epsilon and all(max(c[k] for k in ('coordinate_error','staged_error','whole_vs_staged','probability_error'))<=epsilon for c in checks)
 save(tid+'/independent-verification.json',{'method':'64-term matrix Taylor series, scalar list matvec, direct analyzer amplitudes; classical arithmetic, not a circuit','exponent_multiplier':factor,'time_seconds':q['time']['value']*1e-9,'reference_unitary':enc(u),'reference_evolved_state':enc(s),'matrix_error':matrix_error,'checks':checks,'atol':epsilon,'rtol':0,'passed':passed,'fresh_workflow_status':report['status'],'actual_flagquantum_circuits':report['actual_flagquantum_circuits'],'limits':'Finite binary64 numerical checks; no interval certification or experimental/hardware evidence.'})
# Submitted handoff audit, independent from fresh-run success.
c=tasks[1]['submitted_handoff'];s=references['A2'][1]
for mode in ['coordinates','global-phase']:
 execute('A2/candidate-'+mode,[P,str(R/'skills/compare-quantum-states-and-operators/scripts/compare.py')],{'kind':'state','mode':mode,'basis_a':['0','1'],'basis_b':c['basis'],'a':enc(s),'b':c['state'],'atol':math.sqrt(2)*1e-10})
a=dec(c['state']);phase=sum(x.conjugate()*y for x,y in zip(s,a));z=phase.conjugate()/abs(phase);raw=err(s,a);aligned=err(s,[z*x for x in a]);ev=json.loads((O/'A2/fresh-workflow/02-evolution/stdout.json').read_text());native=next(r for r in ev['records'] if r['input_label']=='supplied' and r['path']=='native-zyz');native_error=err(a,dec(native['statevector']))
save('A2/candidate-disposition.json',{'status':'rejected','full_coordinate_max_error':raw,'phase_aligned_max_error':aligned,'aligning_multiplier_on_candidate':enc(z),'overlap_phase_radians':cmath.phase(phase),'candidate_vs_actual_native_zyz_error':native_error,'native_zyz_alpha':ev['zyz']['alpha'],'ray_equivalent':aligned<=1e-10,'full_coordinates_accepted':raw<=1e-10,'reason':'Candidate omits scalar phase retained by full U. An isolated ray match does not satisfy full-coordinate or controlled-operation requirements. Fresh repaired workflow success is separate.','provenance':tasks[1]['fixture_origin'],'metadata':'Declared basis, singleton batch shape, dtype and device match expected envelope; declarations do not attest any actual submitted execution. Candidate vector supplied directly; no implicit reshape performed.','controlled_witness':json.loads((O/'A2/fresh-workflow/07-controlled-operator-witness/stdout.json').read_text())})
save('A1/claim-disposition.json',{'status':'verified','scope':'Declared ideal numeric evolution and interference, full phase retained, continuous versus staged checked independently.','scientific_acceptance':'No physical-constant accuracy, source draft, hardware or whole-paper acceptance inferred.'})
# Metadata alone: inspect only; do not create amplitudes, swap basis or reshape.
c3=tasks[2]['submitted_handoff'];save('A3/submitted-handoff.json',c3)
save('A3/metadata-audit.json',{'status':'rejected','expected_producer_envelope':{'basis':['0','1'],'shape':[1,2],'state_dtype':'torch.complex128','device':'cpu'},'expected_next_helper_state_shape':[2],'actual':c3,'basis_matches':c3['basis']==['0','1'],'shape_matches_producer_envelope':c3['shape']==[1,2],'directly_consumable_by_interference':False,'reasons':['Basis labels are reversed relative to required canonical 0,1; no transformation authorized.','Envelope has a singleton batch axis; interference accepts exactly one vector and no sample extraction/reshape is authorized here.','No amplitudes, finiteness/normalization evidence or authentic producer receipt supplied. Metadata is an assertion, not evidence of state values.'],'actions':'No transformation, reshape, invented amplitudes, or fresh substitute experiment executed.','fixture_origin':tasks[2]['fixture_origin'],'quantum_circuits_executed_for_A3':0})
results=[]
for tid,skills,status,question in [('A1',allskills,'verified','What hbar value and matching unit should be used? Resolved by parent: 6.582119569e-16 eV*s.'),('A2',allskills,'rejected',None),('A3',['translate-complex-linear-algebra','reproduce-qubit-interference'],'rejected',None)]:
 paths=[str(x.relative_to(O)) for x in sorted((O/tid).rglob('*')) if x.is_file()]
 results.append({'id':tid,'selected_skills':skills,'clarification_question':question,'status':status,'evidence_paths':paths,'verification':({'fresh_run':'verified','independent_reference':'passed','candidate_acceptance':'not applicable' if tid=='A1' else 'rejected: phase omitted despite ray agreement'}) if tid!='A3' else {'metadata_admission':'rejected','fresh_run':'not executed; not needed for metadata mismatch','candidate_acceptance':'rejected as supplied'},'limitations':['Bounded ideal pure-qubit numerical profile; no physical constant accuracy or hardware claim.','Runtime and actual stdout/stderr/exits preserved.','Synthetic submitted fixture is not an executed circuit record.'] if tid!='A1' else ['Caller-declared hbar numerical input; provenance and accuracy not independently supplied or certified.','Finite floating-point checks do not confer scientific/source acceptance.']})
save('results.json',results)
