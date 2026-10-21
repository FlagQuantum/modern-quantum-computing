import json, pathlib, subprocess, sys, time, platform
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs'
tasks=json.loads((ROOT/'tasks.json').read_text())
records={}
def execute(id,name,request,helper):
    folder=OUT/id; folder.mkdir(exist_ok=True)
    (folder/(name+'.request.json')).write_text(json.dumps(request,indent=2)+'\n')
    cmd=[sys.executable,str(ROOT/'skills'/helper/'scripts'/('compare.py' if helper.startswith('compare-') else 'interference.py'))]
    start=time.perf_counter()
    proc=subprocess.run(cmd,input=json.dumps(request),text=True,capture_output=True,cwd=ROOT)
    elapsed=time.perf_counter()-start
    (folder/(name+'.stdout.json')).write_text(proc.stdout)
    (folder/(name+'.stderr.txt')).write_text(proc.stderr)
    meta={'command':cmd,'exit_code':proc.returncode,'elapsed_seconds':elapsed,'runtime':{'implementation':platform.python_implementation(),'python':platform.python_version(),'executable':sys.executable}}
    (folder/(name+'.execution.json')).write_text(json.dumps(meta,indent=2)+'\n')
    return meta
for task in tasks:
    id=task['id']; (OUT/id).mkdir(exist_ok=True)
    (OUT/id/'task.json').write_text(json.dumps(task,indent=2)+'\n')
    runs=[]
    for i,experiment in enumerate(task.get('experiments',[task.get('data')])):
        runs.append(execute(id,'experiment'+str(i+1),experiment,'reproduce-qubit-interference'))
    if id=='B2':
        a,b=task['experiments']
        req={'kind':'state','mode':'global-phase','basis_a':a['basis'],'basis_b':b['basis'],'a':a['state'],'b':b['state'],'atol':1e-10}
        runs.append(execute(id,'comparison',req,'compare-quantum-states-and-operators'))
    records[id]=runs
(OUT/'executions.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records,indent=2))
