import json, subprocess, time, sys, importlib.metadata
from pathlib import Path
root=Path(__file__).resolve().parent.parent
out=root/'outputs'
tasks=json.loads((root/'tasks.json').read_text())
runtime={'interpreter':sys.executable,'python':sys.version,'packages':{p:importlib.metadata.version(p) for p in ['torch','flagquantum']}}
(out/'runtime.json').write_text(json.dumps(runtime,indent=2))
for t in tasks:
 if t['id']=='A1':continue
 ident=t['id'];d=out/ident;d.mkdir(exist_ok=True)
 (d/'original-task.json').write_text(json.dumps(t,indent=2))
 req=json.dumps(t['data'],indent=2)+'\n';(d/'request.json').write_text(req)
 skill='translate-unitary-evolution' if ident=='A4' else 'translate-complex-linear-algebra'
 script='unitary.py' if ident=='A4' else 'algebra.py'
 cmd=[sys.executable,str(root/'skills'/skill/'scripts'/script)]
 start=time.perf_counter();p=subprocess.run(cmd,input=req,text=True,capture_output=True);duration=time.perf_counter()-start
 (d/'stdout.json').write_text(p.stdout);(d/'stderr.txt').write_text(p.stderr)
 (d/'execution.json').write_text(json.dumps({'command':cmd,'exit_code':p.returncode,'elapsed_seconds':duration,'runtime':runtime},indent=2))
 print(ident,p.returncode,duration)
