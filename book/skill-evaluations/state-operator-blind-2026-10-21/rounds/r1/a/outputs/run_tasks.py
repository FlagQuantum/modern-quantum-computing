import json, pathlib, subprocess, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs'
tasks=json.loads((ROOT/'tasks.json').read_text())
for task in tasks:
    ident=task['id']
    if ident=='A1':
        (OUT/'A1.pending.json').write_text(json.dumps({'id':ident,'status':'pending_clarification','question':'Should these statevectors be compared with coordinates/phases retained, or as isolated pure states up to one overall global phase?','default_atol_if_unspecified':1e-10},indent=2)+'\n')
        continue
    request=dict(task['data'],mode='global-phase',atol=1e-10)
    (OUT/f'{ident}.request.json').write_text(json.dumps(request,indent=2)+'\n')
    p=subprocess.run([sys.executable,str(ROOT/'skills/compare-quantum-states-and-operators/scripts/compare.py')],input=json.dumps(request),capture_output=True,text=True)
    (OUT/f'{ident}.stdout.json').write_text(p.stdout)
    (OUT/f'{ident}.stderr.txt').write_text(p.stderr)
    (OUT/f'{ident}.execution.json').write_text(json.dumps({'command':[sys.executable,str(ROOT/'skills/compare-quantum-states-and-operators/scripts/compare.py')],'stdin':f'{ident}.request.json','stdout':f'{ident}.stdout.json','stderr':f'{ident}.stderr.txt','exit_code':p.returncode},indent=2)+'\n')
    print(ident,p.returncode,p.stdout.strip())
