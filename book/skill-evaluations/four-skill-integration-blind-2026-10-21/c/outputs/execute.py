import json,subprocess,time,pathlib,sys
root=pathlib.Path(__file__).resolve().parents[1]; out=root/'outputs'; py='/private/tmp/mqc-writing-venv/bin/python'
def run(name,cmd,request=None):
 start=time.time();p=subprocess.run(cmd,input=None if request is None else json.dumps(request),capture_output=True,text=True,cwd=root)
 (out/(name+'.stdout.txt')).write_text(p.stdout);(out/(name+'.stderr.txt')).write_text(p.stderr)
 (out/(name+'.execution.json')).write_text(json.dumps({'command':cmd,'exit_code':p.returncode,'elapsed_seconds':time.time()-start},indent=2));return p
run('runtime',[py,'-c','import sys,importlib.metadata as m; import torch, flagquantum; print(sys.version);print({x:m.version(x) for x in ["torch","flagquantum"]});print(torch.__file__);print(flagquantum.__file__)'])
tasks=json.loads((root/'tasks.json').read_text())
for task in tasks:
 name=task['id'];(out/(name+'-task.json')).write_text(json.dumps(task,indent=2)); req=out/(name+'-request.json');req.write_text(json.dumps(task['experiment'],indent=2))
 p=run(name+'-workflow',[py,str(root/'workflow/four_skill_interference.py'),'--request',str(req),'--output',str(out/(name+'-workflow')),'--skills-root',str(root/'skills')]);print(name,p.returncode,p.stdout,flush=True)
 if name=='C2' and p.returncode==0:
  iq=json.loads((out/'C2-workflow/09-interference/request.json').read_text());iq['readout']['delta_radians']=-task['experiment']['analyzer']['delta'];(out/'C2-candidate-request.json').write_text(json.dumps(iq,indent=2))
  p=run('C2-candidate-interference',[py,str(root/'skills/reproduce-qubit-interference/scripts/interference.py')],iq);print('C2 candidate numeric experiment',p.returncode,p.stdout[:120],flush=True)
