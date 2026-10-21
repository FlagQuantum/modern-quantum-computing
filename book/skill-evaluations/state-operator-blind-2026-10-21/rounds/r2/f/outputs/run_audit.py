import hashlib,json,pathlib,subprocess,sys
root=pathlib.Path('/private/tmp/mqc-comparison-blind-r2/f')
out=root/'outputs'
protected=[root/'tasks.json',root/'catalog.json',*(root/'skills').rglob('*')]
protected=[p for p in protected if p.is_file()]
before={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
(out/'input_hashes.json').write_text(json.dumps(before,indent=2)+'\n')
results=[]
for task in json.loads((root/'tasks.json').read_text()):
    tid=task['id']; dest=out/tid; dest.mkdir(exist_ok=True)
    req=dict(task['data']); req.update(mode='global-phase',atol=1e-10)
    (dest/'request.json').write_text(json.dumps(req,indent=2)+'\n')
    command=[sys.executable,str(root/'skills/compare-quantum-states-and-operators/scripts/compare.py')]
    execution=subprocess.run(command,input=json.dumps(req),text=True,capture_output=True)
    (dest/'stdout.txt').write_text(execution.stdout)
    (dest/'stderr.txt').write_text(execution.stderr)
    (dest/'execution.json').write_text(json.dumps({'argv':command,'stdin_path':str(dest/'request.json'),'exit_code':execution.returncode},indent=2)+'\n')
    actual=json.loads(execution.stdout); (dest/'result.json').write_text(json.dumps(actual,indent=2)+'\n')
    results.append({'id':tid,'selected_skill':'compare-quantum-states-and-operators','chosen_context':{'kind':req['kind'],'mode':req['mode'],'basis_a':req['basis_a'],'basis_b':req['basis_b'],'atol':req['atol'],'source':'Explicit user request; supplied labels treated as caller assertions.'},'clarification_question':None,'status':actual['status'],'evidence_paths':[str((dest/name).relative_to(root)) for name in ['request.json','result.json','stdout.txt','stderr.txt','execution.json','explanation.md']],'verification':{'status':'pending','script':'outputs/verify.py','results':'outputs/verification.json'},'limitations':['Binary64 numerical evidence, not proof of exact equality.','Basis labels are supplied assertions; array provenance and physical implementation are not established.']})
after={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
assert before==after
(out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'executed':[{'id':r['id'],'status':r['status']} for r in results],'protected_inputs_unchanged':before==after},indent=2))
