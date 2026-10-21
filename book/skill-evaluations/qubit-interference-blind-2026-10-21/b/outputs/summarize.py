import json, pathlib, subprocess, sys, time
OUT=pathlib.Path(__file__).resolve().parent
v=json.loads((OUT/'verification-summary.json').read_text())
question='What exact dephasing channel/Kraus map does probability 0.19 denote, and what laboratory data/uncertainty and acceptance criterion support certifying visibility 0.43?'
reply='No Kraus map, raw laboratory records, uncertainty model, or acceptance criterion is supplied beyond the original task. Do not assume additional data or physical parameters.'
(OUT/'B3'/'clarification.json').write_text(json.dumps({'question':question,'sent_to':'/root','reply':reply,'disposition':'No further semantics or data available. Preserve noisy meaning and leave physical claim unverified.'},indent=2)+'\n')
explanations={
'B1':'Verified direct computational readout at phi=0.35 and 1.73 radians gives (0.34,0.66) both times. There is no final analyzer and no relative-phase probability fringe: multiplying beta by a unit phase leaves its squared modulus unchanged at every phase. The coherent state still carries relative phase; this readout does not reveal it.',
'B2':'Both verified ideal experiments return probabilities (0.5,0.5) under the plain H analyzer. Equal probabilities at this setting do not establish state equivalence. The separate global-phase comparison at absolute Euclidean tolerance 1e-10 returns outside_tolerance (exit 1), with zero overlap and aligned residual sqrt(2)=1.414213562373095. The preparations are orthogonal and are not equal up to global phase. With zero overlap, no unique aligning phase exists; the helper deterministically chooses 1.',
'B3':'The requested dephasing-noisy-single-qubit experiment is outside the available ideal interference and pure-state comparison workflows. The untouched noisy request was saved and submitted to the ideal helper only to record its rejection: actual exit 2 invalid_input due to the extra dephasing_probability field. This failed request is not noisy experiment evidence. The noise field and profile were not removed or relabeled. The caller confirms no Kraus map, raw laboratory records, uncertainty model, or acceptance criterion exists beyond the task. Thus the dephasing simulation and laboratory visibility 0.43 remain unverified; neither confirmation nor refutation follows. A defined channel/density-matrix workflow and laboratory statistical evidence are required.',
'B4':'The ideal run verifies the declared chronological sequence prepare -> D(phi) -> D(-0.387) -> H -> computational measurement, preserving positive analyzer delta. The paper formula (1+cos(phi+delta))/2 is refuted at all three supplied phases. Fresh p0 values are 0.9938503973795471, 0.9404585062842689, and 0.4938983148537082; independent matrix calculations agree within 2.3e-16. At phi=0.23, the claimed value is 0.9078089485395904, differing by about 0.08604144884, above 1e-10. The matching formula is (1+cos(phi-delta))/2 up to the supplied floating-point normalization. Verified simulation and refuted claim are separate dispositions.'}
results=[]
for id in ['B1','B2','B3','B4']:
    (OUT/id/'explanation.txt').write_text(explanations[id]+'\n')
    disposition={'B1':'verified_no_relative_phase_fringe','B2':'verified_experiments_states_not_ray_equivalent','B3':'unsupported_physical_profile_laboratory_claim_unverified','B4':'verified_ideal_run_claim_refuted'}[id]
    evidence=sorted(str(p.relative_to(OUT.parent)) for p in (OUT/id).iterdir() if p.is_file())
    evidence+=['outputs/verify.py','outputs/verify.stdout.json','outputs/verify.stderr.txt','outputs/verify.execution.json','outputs/verification-summary.json','outputs/executions.json','outputs/run.py']
    skills=['reproduce-qubit-interference']
    if id=='B2': skills+=['compare-quantum-states-and-operators']
    if id=='B3': skills=[]
    context={'basis':['0','1'],'angle_unit':'radian','atol':1e-10,'input_preserved':True}
    context['operation_order']=['prepare supplied state','D(phi)']+(['D(-delta)','H'] if id!='B1' else [])+['computational readout']
    if id=='B2':context['separate_comparison']={'kind':'state','mode':'global-phase','metric':'Euclidean','tolerance':1e-10}
    if id=='B3':context={'requested_profile':'dephasing-noisy-single-qubit','dephasing_probability':0.19,'laboratory_visibility':0.43,'channel_semantics':'not supplied','unsupported_helper_probe':'exact untouched raw request; rejected, no experimental evidence'}
    if id=='B4':context['analyzer_delta_radians']=0.387
    limitations=['Deterministic finite precision numerical checks; no exact equality theorem or hardware evidence.'] if id!='B3' else ['No available noisy-channel skill.','Dephasing channel semantics absent.','No raw laboratory data, uncertainty model, or acceptance criterion.','Ideal helper rejection is not evidence about laboratory visibility.']
    record={'id':id,'selected_skills':skills,'chosen_context':context,'clarification_question':question if id=='B3' else None,'status':disposition,'evidence_paths':evidence,'verification':v[id],'limitations':limitations,'explanation':explanations[id]}
    if id=='B3':record['clarification_answer']=reply;record['routing_note']='Available ideal skill inspected for boundary and raw rejection only; not selected as a physical noise simulator.'
    if id=='B4':record['claim_disposition']='refuted for all supplied phases'
    results.append(record)
(OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
# Save a standalone actual environment probe and its process evidence.
cmd=[sys.executable,'-c','import sys,platform,importlib.metadata,json; print(json.dumps({"executable":sys.executable,"implementation":platform.python_implementation(),"python":platform.python_version(),"versions":{k:importlib.metadata.version(k) for k in ["flagquantum","torch"]}}))']
t=time.perf_counter(); proc=subprocess.run(cmd,capture_output=True,text=True)
(OUT/'runtime.stdout.json').write_text(proc.stdout)
(OUT/'runtime.stderr.txt').write_text(proc.stderr)
(OUT/'runtime.execution.json').write_text(json.dumps({'command':cmd,'exit_code':proc.returncode,'elapsed_seconds':time.perf_counter()-t},indent=2)+'\n')
print(json.dumps({'results':str(OUT/'results.json'),'tasks':[{ 'id':r['id'],'status':r['status']} for r in results]},indent=2))
