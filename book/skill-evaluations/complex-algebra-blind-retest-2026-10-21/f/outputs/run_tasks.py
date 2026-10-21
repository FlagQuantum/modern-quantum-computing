import json, pathlib, subprocess, time
base=pathlib.Path('/private/tmp/mqc-algebra-blind-r2/f'); out=base/'outputs'
tasks=json.loads((base/'tasks.json').read_text())
for n, interp in enumerate(json.loads((base/'environment.json').read_text())['python_candidates']):
    code='import sys, json; from importlib.metadata import version, PackageNotFoundError; print(json.dumps({"implementation":sys.implementation.name,"python":sys.version,"torch":version("torch")}))'
    start=time.perf_counter(); run=subprocess.run([interp,'-c',code],capture_output=True,text=True)
    (out/f'runtime_probe_{n}.stdout').write_text(run.stdout); (out/f'runtime_probe_{n}.stderr').write_text(run.stderr)
    (out/f'runtime_probe_{n}.json').write_text(json.dumps({'argv':[interp,'-c',code],'exit_code':run.returncode,'elapsed_seconds':time.perf_counter()-start},indent=2))
interp='/private/tmp/mqc-writing-venv/bin/python'
for task in tasks:
    p=out/task['id']; p.mkdir(exist_ok=True)
    (p/'original_task.json').write_text(json.dumps(task,indent=2)); (p/'request.json').write_text(json.dumps(task['data'],indent=2))
    if task['id']=='F3': continue
    argv=[interp,str(base/'skills/translate-complex-linear-algebra/scripts/algebra.py')]
    start=time.perf_counter(); run=subprocess.run(argv,input=(p/'request.json').read_text(),capture_output=True,text=True)
    (p/'stdout.json').write_text(run.stdout); (p/'stderr.txt').write_text(run.stderr)
    (p/'execution.json').write_text(json.dumps({'argv':argv,'stdin_path':str(p/'request.json'),'exit_code':run.returncode,'elapsed_seconds':time.perf_counter()-start,'quantum_execution':False},indent=2))
