import json, subprocess, time, pathlib, sys
base=pathlib.Path('/private/tmp/mqc-algebra-blind-r2/e'); out=base/'outputs'
py='/private/tmp/mqc-writing-venv/bin/python'
env={}
for candidate in json.loads((base/'environment.json').read_text())['python_candidates']:
    t=time.perf_counter(); p=subprocess.run([candidate,'-c','import sys; print(sys.version); import torch; print(torch.__version__)'],text=True,capture_output=True)
    env[candidate]={'stdout':p.stdout,'stderr':p.stderr,'exit_code':p.returncode,'elapsed_seconds':time.perf_counter()-t}
(out/'runtime_discovery.json').write_text(json.dumps(env,indent=2))
for task in json.loads((base/'tasks.json').read_text()):
    d=out/task['id'];d.mkdir(exist_ok=True)
    (d/'original_task.json').write_text(json.dumps(task,indent=2))
    q=task['data'].copy()
    if task['id']=='E2':
        q['direction']='passive-new-in-old'
        (d/'clarification.json').write_text(json.dumps({'question':'Do columns of S represent new basis in old coordinates (passive), or an active map?','answer':'Use passive-new-in-old: the columns of S are the new basis in old coordinates, and v is in old coordinates. Return S^-1*v and S^-1*A*S, preserving the Gram metric.','source':'/root collaboration message'},indent=2))
    (d/'request.json').write_text(json.dumps(q,indent=2))
    cmd=[py,str(base/'skills/translate-complex-linear-algebra/scripts/algebra.py')]
    t=time.perf_counter(); p=subprocess.run(cmd,input=json.dumps(q),text=True,capture_output=True)
    (d/'stdout.json').write_text(p.stdout);(d/'stderr.txt').write_text(p.stderr)
    (d/'execution.json').write_text(json.dumps({'command':cmd,'stdin':'request.json','exit_code':p.returncode,'elapsed_seconds':time.perf_counter()-t,'quantum_execution':False},indent=2))
