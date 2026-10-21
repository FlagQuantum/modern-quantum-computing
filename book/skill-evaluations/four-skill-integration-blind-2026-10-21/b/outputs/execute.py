import json,sys,subprocess,time,pathlib,hashlib,math
R=pathlib.Path(__file__).resolve().parents[1]; O=R/'outputs'; T=json.loads((R/'tasks.json').read_text()); P='/private/tmp/mqc-writing-venv/bin/python'
def save(p,x):
 p=O/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def run(label,cmd,stdin=None):
 d=O/label;d.mkdir(parents=True,exist_ok=True);start=time.monotonic();r=subprocess.run(cmd,input=stdin,capture_output=True,text=True,cwd=R);(d/'stdout.txt').write_text(r.stdout);(d/'stderr.txt').write_text(r.stderr);save(label+'/execution.json',{'command':cmd,'exit_code':r.returncode,'elapsed_seconds':time.monotonic()-start,'stdin':stdin});return r
for i,p in enumerate(json.loads((R/'environment.json').read_text())['python_candidates']):
 run('runtime-'+str(i),[p,'-c','import sys, json, importlib.metadata as m; print(json.dumps({"implementation":sys.implementation.name,"python":sys.version,"packages":{x:m.version(x) for x in ["torch","flagquantum"]}}))'])
for t in T:save(t['id']+'/source-task.json',t)
q=T[0]['experiment'];q=json.loads(json.dumps(q));q['generator']['matrix']=[[[x*2*math.pi,y*2*math.pi] for x,y in row] for row in q['generator']['matrix']];q['generator']['unit']='rad/s';q['phase_scan']={'values':[v*math.pi/180 for v in q['phase_scan']['values']],'unit':'radian'};q['analyzer']={'delta':q['analyzer']['delta']*math.pi/180,'unit':'radian'}
save('B1/conversion.json',{'clarification_received_from':'root','semantics':'Generator entries are cyclic Hz = H/h; multiply every entry by 2*pi for angular H/hbar in rad/s; no hbar division. Angles degree*pi/180. Time remains 0.29 ns.','original':T[0]['experiment'],'converted':q})
for ident,request in [('B1',q),('B2',T[1]['experiment'])]:
 save(ident+'/request.json',request);run(ident+'/runner',[P,str(R/'workflow/four_skill_interference.py'),'--request',str(O/ident/'request.json'),'--output',str(O/ident/'fresh'),'--skills-root',str(R/'skills')])
t=T[2]; receipt=t['submitted_budget_receipt'];req={'task':'check','coordinates':'literal-complex','tolerance':{'atol':receipt['requested_coordinate_atol'],'rtol':0},'actual':{'shape':[],'dtype':'complex128','device':'cpu','values':[[receipt['observed_probability_max_absolute_error'],0]]},'reference':{'shape':[],'dtype':'complex128','device':'cpu','values':[[0,0]]}}
save('B3/request.json',req);save('B3/check-context.json',{'evidence_type':'Classical scalar check of supplied synthetic absolute-error receipt against requested tolerance. Not a circuit execution or fabricated probability pair.','synthetic_fixture':True,'quantum_execution':False})
run('B3/helper',[P,str(R/'skills/translate-complex-linear-algebra/scripts/algebra.py')],json.dumps(req))
