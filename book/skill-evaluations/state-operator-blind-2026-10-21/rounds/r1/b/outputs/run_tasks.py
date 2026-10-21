import json, math, pathlib, subprocess, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs'
tasks=json.loads((ROOT/'tasks.json').read_text())
results=[]
def save(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2)+'\n')
for t in tasks:
    tid=t['id']
    if tid in ('B1','B2'):
        req=dict(t['data'],mode='controlled' if tid=='B1' else 'global-phase',atol=1e-10)
        save(tid+'.request.json',req)
        p=subprocess.run([sys.executable,str(ROOT/'skills/compare-quantum-states-and-operators/scripts/compare.py')],input=json.dumps(req),text=True,capture_output=True)
        (OUT/(tid+'.stdout.json')).write_text(p.stdout)
        (OUT/(tid+'.stderr.txt')).write_text(p.stderr)
        save(tid+'.execution.json',{'command':[sys.executable,str(ROOT/'skills/compare-quantum-states-and-operators/scripts/compare.py')],'stdin_path':tid+'.request.json','exit_code':p.returncode})
        actual=json.loads(p.stdout)
        results.append({'id':tid,'selected_skill':'compare-quantum-states-and-operators','chosen_context':req['mode'],'clarification_question':None,'status':actual.get('status',actual.get('result','executed')),'evidence_paths':[tid+'.request.json',tid+'.stdout.json',tid+'.stderr.txt',tid+'.execution.json',tid+'.explanation.txt','verify.py','verification.stdout.json','verification.stderr.txt','verification.execution.json'],'verification':None,'limitations':['Binary64 numerical comparison; declared basis is assumed and not independently established.','Does not establish noisy implementation or algorithm equivalence.']})
    else:
        n=t['data']['shots']; k=t['data']['successes']; phat=k/n; se=math.sqrt(phat*(1-phat)/n)
        save(tid+'.request.json',t)
        save(tid+'.stdout.json',{'observed_proportion':phat,'plug_in_standard_error':se,'shots':n,'successes':k,'formula':'sqrt(p_hat*(1-p_hat)/n)'})
        (OUT/(tid+'.stderr.txt')).write_text('')
        save(tid+'.execution.json',{'executor':'outputs/run_tasks.py using Python standard library math.sqrt','exit_code':0})
        (OUT/(tid+'.explanation.txt')).write_text('No available skill fits shot counts: the available comparison skill excludes hardware statistics and accepts only statevectors/unitaries. Independently compute p_hat=47/125=0.376, and usual Bernoulli plug-in SE=sqrt(p_hat*(1-p_hat)/125). No amplitudes inferred. This is a plug-in SE, not a confidence interval or exact population uncertainty.\n')
        results.append({'id':tid,'selected_skill':None,'chosen_context':'independent Bernoulli shot counts; descriptive proportion and usual plug-in standard error','clarification_question':None,'status':'completed','evidence_paths':[tid+'.request.json',tid+'.stdout.json',tid+'.stderr.txt',tid+'.execution.json',tid+'.explanation.txt','run_tasks.py','verify.py','verification.stdout.json','verification.stderr.txt','verification.execution.json'],'verification':None,'limitations':['Plug-in standard error under the stated independent Bernoulli assumption; no confidence interval requested.']})
save('results.json',results)
print(json.dumps({'executed':[r['id'] for r in results]},indent=2))
