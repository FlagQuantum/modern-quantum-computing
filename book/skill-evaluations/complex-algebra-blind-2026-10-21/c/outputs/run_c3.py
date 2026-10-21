import json,pathlib,subprocess,time
root=pathlib.Path('/private/tmp/mqc-algebra-blind-r1/c');out=root/'outputs'/'C3';out.mkdir(exist_ok=True)
task=next(t for t in json.loads((root/'tasks.json').read_text()) if t['id']=='C3')
(out/'original_request.json').write_text(json.dumps(task['data'],indent=2)+'\n')
(out/'clarification.json').write_text(json.dumps({'question':'What explicit atol and rtol budget applies?','answer':'Use explicit atol=1e-9 and rtol=0, comparing modulus of each complex difference against the supplied reference budget; preserve metadata and do not align phase.','source':'Parent /root collaboration message'},indent=2)+'\n')
q=task['data'];q['tolerance']={'atol':1e-9,'rtol':0};req=out/'request.json';req.write_text(json.dumps(q,indent=2)+'\n')
command=['/private/tmp/mqc-writing-venv/bin/python',str(root/'skills/translate-complex-linear-algebra/scripts/algebra.py')]
start=time.perf_counter();cp=subprocess.run(command,input=req.read_text(),capture_output=True,text=True);elapsed=time.perf_counter()-start
(out/'stdout.json').write_text(cp.stdout);(out/'stderr.txt').write_text(cp.stderr)
(out/'execution.json').write_text(json.dumps({'command':command,'stdin':str(req),'exit_code':cp.returncode,'wall_seconds':elapsed},indent=2)+'\n')
