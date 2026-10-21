import json, subprocess, time, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parent.parent
OUT=ROOT/'outputs'
python='/private/tmp/mqc-writing-venv/bin/python'
tasks=json.loads((ROOT/'tasks.json').read_text())
runtime=subprocess.run([python,'-c','import sys, platform, torch; import json; print(json.dumps({"implementation":platform.python_implementation(),"python":sys.version,"torch":torch.__version__}))'],capture_output=True,text=True)
(OUT/'runtime.stdout').write_text(runtime.stdout); (OUT/'runtime.stderr').write_text(runtime.stderr)
(OUT/'runtime.json').write_text(json.dumps({'exit_code':runtime.returncode,'interpreter':python,'runtime':json.loads(runtime.stdout)},indent=2))
for task in tasks:
    ident=task['id']; request=OUT/(ident+'.request.json')
    request.write_text(json.dumps(task['data'],indent=2)+'\n')
    skill='compare-quantum-states-and-operators' if ident=='B4' else 'translate-complex-linear-algebra'
    helper='compare.py' if ident=='B4' else 'algebra.py'
    command=[python,str(ROOT/'skills'/skill/'scripts'/helper)]
    start=time.perf_counter()
    result=subprocess.run(command,input=request.read_text(),capture_output=True,text=True,cwd=ROOT)
    elapsed=time.perf_counter()-start
    (OUT/(ident+'.stdout.json')).write_text(result.stdout)
    (OUT/(ident+'.stderr.txt')).write_text(result.stderr)
    (OUT/(ident+'.execution.json')).write_text(json.dumps({'command':command,'stdin':str(request),'exit_code':result.returncode,'elapsed_seconds':elapsed,'quantum_execution':False},indent=2))
    print(ident,result.returncode,result.stdout)
