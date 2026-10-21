import json, subprocess, sys, time, pathlib, platform, importlib.metadata as md
root=pathlib.Path('/private/tmp/mqc-unitary-blind-r1/a'); out=root/'outputs'
python='/private/tmp/mqc-writing-venv/bin/python'
runtime={'selected_interpreter':sys.executable,'python':sys.version,'implementation':platform.python_implementation(),'FlagQuantum':md.version('FlagQuantum'),'torch':md.version('torch')}
(out/'runtime.json').write_text(json.dumps(runtime,indent=2))
for t in json.loads((root/'tasks.json').read_text()):
 d=out/t['id'];d.mkdir(exist_ok=True)
 req=t['data'].copy()
 if t['id']=='A1':
  req['hbar']={'value':6.582119569e-16,'unit':'eV*s'}
  (d/'clarification.json').write_text(json.dumps({'question':'Supply explicit hbar conversion input for energy eV and time ns.','response':'Use hbar = 6.582119569e-16 eV*s as the explicitly declared numerical conversion input for this task. Preserve it in the record; no additional physical-constant provenance is supplied.','source':'parent /root clarification'},indent=2))
 (d/'request.json').write_text(json.dumps(req,indent=2))
 skill='compare-quantum-states-and-operators' if t['id']=='A4' else 'translate-unitary-evolution'
 script='compare.py' if t['id']=='A4' else 'unitary.py'
 command=[python,str(root/'skills'/skill/'scripts'/script)]
 start=time.time(); p=subprocess.run(command,input=json.dumps(req),text=True,capture_output=True);end=time.time()
 (d/'stdout.json').write_text(p.stdout);(d/'stderr.txt').write_text(p.stderr)
 (d/'execution.json').write_text(json.dumps({'command':command,'stdin':'request.json','exit_code':p.returncode,'started_unix':start,'elapsed_seconds':end-start,'runtime':runtime},indent=2))
 print(t['id'],p.returncode,p.stdout[:300])
