import json, subprocess, time, pathlib, sys, platform, importlib.metadata
root=pathlib.Path(__file__).resolve().parent.parent
out=root/'outputs'
tasks=json.loads((root/'tasks.json').read_text())
runtime={'executable':sys.executable,'implementation':platform.python_implementation(),'python':platform.python_version(),'packages':{p:importlib.metadata.version(p) for p in ['flagquantum','torch']}}
(out/'runtime.json').write_text(json.dumps(runtime,indent=2))
for t in tasks:
 d=out/t['id'];d.mkdir(exist_ok=True)
 (d/'original-task.json').write_text(json.dumps(t,indent=2))
 request=t['data'].copy()
 if t['id']=='A1':
  request['readout']={'type':'phase-h','delta_radians':0.419}
  (d/'clarification.json').write_text(json.dumps({'question':'Choose computational readout or phase-h analyzer and supply delta in radians.','answer':'Use a final phase-h analyzer H D(-delta), with delta = 0.419 radians. Keep all supplied phase values in radians.','source':'parent relayed caller clarification'},indent=2))
 if t['id']=='A4': request.update(mode='global-phase',atol=1e-10)
 skill='compare-quantum-states-and-operators' if t['id']=='A4' else 'reproduce-qubit-interference'
 script='compare.py' if t['id']=='A4' else 'interference.py'
 (d/'request.json').write_text(json.dumps(request,indent=2))
 cmd=[sys.executable,str(root/'skills'/skill/'scripts'/script)]
 start=time.perf_counter();p=subprocess.run(cmd,input=json.dumps(request),text=True,capture_output=True,cwd=root);elapsed=time.perf_counter()-start
 (d/'stdout.json').write_text(p.stdout);(d/'stderr.txt').write_text(p.stderr)
 (d/'execution.json').write_text(json.dumps({'command':cmd,'exit_code':p.returncode,'elapsed_seconds':elapsed,'runtime':runtime},indent=2))
 print(t['id'],p.returncode,p.stdout)
