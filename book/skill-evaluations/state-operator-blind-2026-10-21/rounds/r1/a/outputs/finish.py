import json,pathlib,subprocess,sys,math
R=pathlib.Path(__file__).resolve().parents[1]; O=R/'outputs'
tasks=json.loads((R/'tasks.json').read_text())
clarification={'question':'Should A1 compare the supplied statevectors with their coordinates/phases retained, or as isolated pure states up to one overall global phase?','answer':'I mean equality of the exported complex coordinates with phase retained, rather than ray equivalence. Use absolute Euclidean tolerance 1e-10.','source':'Requester clarification relayed by /root via collaboration.send_message'}
(O/'A1.clarification.json').write_text(json.dumps(clarification,indent=2)+'\n')
q=dict(tasks[0]['data'],mode='coordinates',atol=1e-10)
(O/'A1.request.json').write_text(json.dumps(q,indent=2)+'\n')
p=subprocess.run([sys.executable,str(R/'skills/compare-quantum-states-and-operators/scripts/compare.py')],input=json.dumps(q),capture_output=True,text=True)
(O/'A1.stdout.json').write_text(p.stdout);(O/'A1.stderr.txt').write_text(p.stderr)
(O/'A1.execution.json').write_text(json.dumps({'command':[sys.executable,str(R/'skills/compare-quantum-states-and-operators/scripts/compare.py')],'stdin':'A1.request.json','stdout':'A1.stdout.json','stderr':'A1.stderr.txt','exit_code':p.returncode},indent=2)+'\n')
(O/'A1.pending.json').unlink()
results=[]
explanations={
'A1':'The requester clarified coordinate equality with phase retained. Both arrays use declared basis [0,1]. The raw Euclidean residual exceeds 1e-10, so coordinates are outside tolerance. A small aligned residual is diagnostic only and cannot override retained-phase semantics.',
'A2':'These isolated pure states are valid normalized exports in declared basis [0,1]. Applying one optimal phase to the whole b vector leaves Euclidean residual 0.37403457393355366, greater than 1e-10. They are outside tolerance even up to overall phase. Equal component magnitudes do not remove the relative phase difference.',
'A3':'The b export has squared norm 1.0161000000000002, differing from unity by about 0.0161, far above validation tolerance 1e-12. The helper rejects the supplied comparison as invalid_input, exit 2. No normalization was performed, and this rejection is not a claim that valid intended physical states differ.'}
for t in tasks:
    i=t['id']; r=json.loads((O/f'{i}.stdout.json').read_text())
    (O/f'{i}.explanation.txt').write_text(explanations[i]+'\n')
    results.append({'id':i,'selected_skill':'compare-quantum-states-and-operators','chosen_context':{'kind':'state','mode':'coordinates' if i=='A1' else 'global-phase','basis_a':t['data']['basis_a'],'basis_b':t['data']['basis_b'],'atol':1e-10,'source':'requester clarification' if i=='A1' else 'explicit task request'},'clarification_question':clarification['question'] if i=='A1' else None,'clarification_answer':clarification['answer'] if i=='A1' else None,'status':r['status'],'evidence_paths':[f'outputs/{i}.{s}' for s in ('request.json','stdout.json','stderr.txt','execution.json','explanation.txt')]+(['outputs/A1.clarification.json'] if i=='A1' else []),'verification':{'script':'outputs/verify.py','report':'outputs/verification.stdout.json'},'limitations':['Declared basis ordering is an assertion by the caller; source program ordering was not inspected.','Deterministic binary64 numerical comparison, not exact equality proof or experimental evidence.']+(['As-supplied export is not normalized; no physical-state inequality conclusion is valid.'] if i=='A3' else [])})
(O/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(p.stdout.strip())
