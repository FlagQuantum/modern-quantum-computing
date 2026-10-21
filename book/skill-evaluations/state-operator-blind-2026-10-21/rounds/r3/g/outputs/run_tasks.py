import sys, json, pathlib, subprocess, platform, math
ROOT=pathlib.Path('/private/tmp/mqc-comparison-blind-r3/g')
OUT=ROOT/'outputs'
PYTHON='/private/tmp/mqc-writing-venv/bin/python'
HELPER=ROOT/'skills/compare-quantum-states-and-operators/scripts/compare.py'
tasks=json.loads((ROOT/'tasks.json').read_text())
for idx, candidate in enumerate(json.loads((ROOT/'environment.json').read_text())['python_candidates']):
    cmd=[candidate,'-c','import sys,platform,json; print(json.dumps({"executable":sys.executable,"implementation":platform.python_implementation(),"version":sys.version,"version_info":list(sys.version_info)}))']
    p=subprocess.run(cmd,capture_output=True,text=True)
    (OUT/f'runtime_{idx}.json').write_text(json.dumps({'command':cmd,'stdout':p.stdout,'stderr':p.stderr,'exit_code':p.returncode},indent=2)+'\n')
for t in tasks:
    d=OUT/t['id']; d.mkdir(exist_ok=True)
    req=dict(t['data'],mode='global-phase',atol=1e-10)
    (d/'request.json').write_text(json.dumps(req,indent=2)+'\n')
    cmd=[PYTHON,str(HELPER)]
    p=subprocess.run(cmd,input=json.dumps(req),capture_output=True,text=True)
    (d/'stdout.json').write_text(p.stdout)
    (d/'stderr.txt').write_text(p.stderr)
    (d/'execution.json').write_text(json.dumps({'command':cmd,'stdin_path':str(d/'request.json'),'stdout_path':str(d/'stdout.json'),'stderr_path':str(d/'stderr.txt'),'exit_code':p.returncode},indent=2)+'\n')
