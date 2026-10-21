import json, pathlib, subprocess, sys, time
root=pathlib.Path(__file__).resolve().parent.parent
out=root/'outputs'
py='/private/tmp/mqc-writing-venv/bin/python'
tasks=json.loads((root/'tasks.json').read_text())
def run(tag,args,stdin=None):
    start=time.perf_counter()
    r=subprocess.run(args,input=stdin,text=True,capture_output=True,cwd=root)
    (out/(tag+'.stdout')).write_text(r.stdout)
    (out/(tag+'.stderr')).write_text(r.stderr)
    meta={'argv':args,'exit_code':r.returncode,'runtime_seconds':time.perf_counter()-start}
    (out/(tag+'.execution.json')).write_text(json.dumps(meta,indent=2))
    return r
run('environment',[py,'-c',"import sys,importlib.metadata,json; print(json.dumps({'python':sys.version,'implementation':sys.implementation.name,'executable':sys.executable,'flagquantum':importlib.metadata.version('flagquantum'),'torch':importlib.metadata.version('torch')}))"])
for t in tasks:
    ident=t['id']
    (out/(ident+'.original.json')).write_text(json.dumps(t,indent=2))
    if ident in ['C2','C4']:
        req=json.dumps(t['data'],indent=2)
        (out/(ident+'.request.json')).write_text(req)
        run(ident+'.helper',[py,str(root/'skills/reproduce-qubit-interference/scripts/interference.py')],req)
