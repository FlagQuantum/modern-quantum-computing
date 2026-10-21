import json,sys,subprocess,time,math,pathlib
root=pathlib.Path(__file__).resolve().parent.parent
out=root/'outputs'
tasks=json.loads((root/'tasks.json').read_text())
clarifications={
 'C1':{'question':'Will the gate be used in isolation or under coherent control?','answer':'The gate is used under coherent control with a superposed control qubit, not just in isolation. Use the declared control-first basis 00,01,10,11 and retain the full controlled operation.','source':'Parent agent clarification received via collaboration.send_message'},
 'C4':{'question':'Are entries cyclic frequencies in Hz or angular frequencies in rad/s?','answer':'The entries are cyclic frequencies in Hz. Convert the entire matrix to an angular-frequency generator in rad/s by multiplying every entry by 2pi; time is 0.7 ns. Preserve both the original values and this explicit conversion.','source':'Parent agent clarification received via collaboration.send_message'}}
(out/'clarifications.json').write_text(json.dumps(clarifications,indent=2))
probes=[]
for exe in json.loads((root/'environment.json').read_text())['python_candidates']:
 start=time.perf_counter()
 p=subprocess.run([exe,'-c','import sys,importlib.metadata as m,json; print(json.dumps({"python":sys.version,"implementation":sys.implementation.name,"packages":{p:m.version(p) for p in ["flagquantum","torch"]}}))'],capture_output=True,text=True)
 probes.append({'command':[exe,'-c','runtime/package version probe'],'stdout':p.stdout,'stderr':p.stderr,'exit_code':p.returncode,'runtime_seconds':time.perf_counter()-start})
(out/'runtime-probes.json').write_text(json.dumps(probes,indent=2))
for t in tasks:
 d=out/t['id'];d.mkdir(exist_ok=True)
 (d/'original-task.json').write_text(json.dumps(t,indent=2))
 q=json.loads(json.dumps(t['data']))
 if t['id']=='C1':q['context']='coherent-control'
 if t['id']=='C4':
  q['generator']['matrix']=[[[2*math.pi*x for x in z] for z in row] for row in q['generator']['matrix']]
  q['generator']['unit']='rad/s'
  (d/'conversion.json').write_text(json.dumps({'original_generator':t['data']['generator'],'declared_conversion':'G_rad_per_s = 2*pi*G_Hz; applies to every complex matrix entry','factor':2*math.pi,'converted_generator':q['generator'],'original_time':q['time'],'seconds':0.7e-9,'exponent':'E = (0.7e-9 s) * (2*pi*G_Hz)'},indent=2))
 (d/'request.json').write_text(json.dumps(q,indent=2))
 command=['/private/tmp/mqc-writing-venv/bin/python',str(root/'skills/translate-unitary-evolution/scripts/unitary.py')]
 start=time.perf_counter();p=subprocess.run(command,input=json.dumps(q),text=True,capture_output=True,cwd=root)
 (d/'stdout.json').write_text(p.stdout);(d/'stderr.txt').write_text(p.stderr)
 (d/'execution.json').write_text(json.dumps({'command':command,'stdin_path':str(d/'request.json'),'exit_code':p.returncode,'runtime_seconds':time.perf_counter()-start},indent=2))
 print(t['id'],p.returncode,p.stdout[:120])
