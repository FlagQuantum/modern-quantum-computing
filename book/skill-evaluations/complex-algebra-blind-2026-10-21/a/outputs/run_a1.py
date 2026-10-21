import json,subprocess,time,sys
from pathlib import Path
r=Path(__file__).resolve().parent.parent;o=r/'outputs'/'A1';o.mkdir(exist_ok=True)
t=json.loads((r/'tasks.json').read_text())[0]
(o/'original-task.json').write_text(json.dumps(t,indent=2))
clar={'question':'Should basis_columns be interpreted as passive-new-in-old or an active transformation?','answer':'Use passive-new-in-old: columns of S are the new basis in old coordinates; v is the old coordinate vector. Return x_new=S^-1*v, B=S^-1*A*S and the Gram metric. Do not apply S actively to v.','source':'Parent /root clarification response via collaboration.send_message'}
(o/'clarification.json').write_text(json.dumps(clar,indent=2))
q=t['data'].copy();q['direction']='passive-new-in-old';req=json.dumps(q,indent=2)+'\n';(o/'request.json').write_text(req)
cmd=[sys.executable,str(r/'skills/translate-complex-linear-algebra/scripts/algebra.py')]
a=time.perf_counter();p=subprocess.run(cmd,input=req,text=True,capture_output=True);elapsed=time.perf_counter()-a
(o/'stdout.json').write_text(p.stdout);(o/'stderr.txt').write_text(p.stderr);(o/'execution.json').write_text(json.dumps({'command':cmd,'exit_code':p.returncode,'elapsed_seconds':elapsed,'runtime':json.loads((r/'outputs/runtime.json').read_text())},indent=2))
print(p.returncode,p.stdout)
