import json, subprocess, time, pathlib, hashlib
root=pathlib.Path(__file__).resolve().parents[1]
out=root/'outputs'
py='/private/tmp/mqc-writing-venv/bin/python'
helper=root/'skills/translate-complex-linear-algebra/scripts/algebra.py'
def run_record(label,command,stdin=None):
    started=time.time(); p=subprocess.run(command,input=stdin,text=True,capture_output=True,cwd=root); elapsed=time.time()-started
    (out/(label+'.stdout')).write_text(p.stdout); (out/(label+'.stderr')).write_text(p.stderr)
    record={'command':command,'stdin_path':label+'.request.json' if stdin is not None else None,'exit_code':p.returncode,'elapsed_seconds':elapsed,'started_unix_seconds':started,'stdout_path':label+'.stdout','stderr_path':label+'.stderr'}
    (out/(label+'.execution.json')).write_text(json.dumps(record,indent=2))
    return record
for n,candidate in enumerate(json.loads((root/'environment.json').read_text())['python_candidates']):
    run_record('interpreter_probe_'+str(n),[candidate,'-c','import sys,importlib.metadata as m; print(sys.version); print(m.version("torch"))'])
for task in json.loads((root/'tasks.json').read_text()):
    raw=json.dumps(task['data'],indent=2)+'\n'; (out/(task['id']+'.request.json')).write_text(raw)
    run_record(task['id'],[py,str(helper)],raw)
(out/'source_hashes.json').write_text(json.dumps({str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [root/'tasks.json',root/'catalog.json',root/'environment.json',helper]},indent=2))
