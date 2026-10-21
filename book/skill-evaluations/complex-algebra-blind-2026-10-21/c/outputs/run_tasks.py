import json, pathlib, subprocess, time, sys
ROOT=pathlib.Path('/private/tmp/mqc-algebra-blind-r1/c')
OUT=ROOT/'outputs'
PYTHON='/private/tmp/mqc-writing-venv/bin/python'
HELPER=ROOT/'skills/translate-complex-linear-algebra/scripts/algebra.py'
tasks=json.loads((ROOT/'tasks.json').read_text())
for task in tasks:
    if task['id']=='C3': continue
    ident=task['id']; folder=OUT/ident;folder.mkdir(exist_ok=True)
    request=folder/'request.json';request.write_text(json.dumps(task['data'],indent=2)+'\n')
    start=time.perf_counter()
    cp=subprocess.run([PYTHON,str(HELPER)],input=request.read_text(),capture_output=True,text=True)
    elapsed=time.perf_counter()-start
    (folder/'stdout.json').write_text(cp.stdout);(folder/'stderr.txt').write_text(cp.stderr)
    (folder/'execution.json').write_text(json.dumps({'command':[PYTHON,str(HELPER)],'stdin':str(request),'exit_code':cp.returncode,'wall_seconds':elapsed},indent=2)+'\n')
probe="import sys,importlib.metadata,json;print(json.dumps({'python':sys.version,'executable':sys.executable,'torch':importlib.metadata.version('torch')}))"
cp=subprocess.run([PYTHON,'-c',probe],capture_output=True,text=True)
(OUT/'environment_probe.json').write_text(json.dumps({'command':[PYTHON,'-c',probe],'stdout':cp.stdout,'stderr':cp.stderr,'exit_code':cp.returncode},indent=2)+'\n')
