import json, pathlib, subprocess, sys, math
root=pathlib.Path(__file__).resolve().parent.parent
out=root/'outputs'
tasks=json.loads((root/'tasks.json').read_text())
interp='/private/tmp/mqc-writing-venv/bin/python'
helper=root/'skills/compare-quantum-states-and-operators/scripts/compare.py'
records=[]
for task in tasks:
    tid=task['id']; p=out/tid; p.mkdir(exist_ok=True)
    (p/'raw-task.json').write_text(json.dumps(task,indent=2)+'\n')
    if tid in ('H1','H2'):
        request=dict(task['data'],mode='controlled' if tid=='H1' else 'global-phase',atol=1e-10)
        (p/'request.json').write_text(json.dumps(request,indent=2)+'\n')
        command=[interp,str(helper)]
        proc=subprocess.run(command,input=json.dumps(request),capture_output=True,text=True)
        (p/'stdout.json').write_text(proc.stdout); (p/'stderr.txt').write_text(proc.stderr)
        (p/'execution.json').write_text(json.dumps({'argv':command,'stdin_path':str(p/'request.json'),'exit_code':proc.returncode},indent=2)+'\n')
        result=json.loads(proc.stdout)
        explanation=('Construct diag(I,U) and diag(I,V), with control first and basis 00,01,10,11. Align a single scalar phase on those full 4x4 operators. A target-only phase is a relative phase between the control branches.' if tid=='H1' else 'Compare the supplied 4x4 isolated operators in basis 00,01,10,11. Use one scalar phase across all matrix entries; no columnwise alignment.')
        explanation+='\nDecision: '+result['status']+'; Frobenius residual '+str(result['decision_residual'])+' at absolute tolerance 1e-10.\n'
        (p/'explanation.txt').write_text(explanation)
        records.append({'id':tid,'selected_skill':'compare-quantum-states-and-operators','chosen_context':request['mode'],'clarification_question':None,'status':result['status'],'answer':result,'evidence_paths':[str(p/x) for x in ['raw-task.json','request.json','stdout.json','stderr.txt','execution.json','explanation.txt']],'verification':{'status':'pending'},'limitations':['Binary64 numerical comparison, not proof of exact equality.','Basis order is the caller-supplied assertion.']})
    else:
        request={'successes':task['data']['successes'],'shots':task['data']['shots'],'estimator':'p_hat=k/n; plug-in SE=sqrt(p_hat*(1-p_hat)/n)'}
        (p/'request.json').write_text(json.dumps(request,indent=2)+'\n')
        code="import json,math,sys; d=json.load(sys.stdin); k=d['successes']; n=d['shots']; assert isinstance(k,int) and isinstance(n,int) and n>0 and 0<=k<=n; p=k/n; print(json.dumps({'observed_proportion':p,'plugin_standard_error':math.sqrt(p*(1-p)/n),'runtime':{'implementation':sys.implementation.name,'python':'.'.join(map(str,sys.version_info[:3]))}}))"
        (p/'calculate.py').write_text(code+'\n')
        command=[interp,str(p/'calculate.py')]
        proc=subprocess.run(command,input=json.dumps(request),capture_output=True,text=True)
        (p/'stdout.json').write_text(proc.stdout); (p/'stderr.txt').write_text(proc.stderr)
        (p/'execution.json').write_text(json.dumps({'argv':command,'stdin_path':str(p/'request.json'),'exit_code':proc.returncode},indent=2)+'\n')
        result=json.loads(proc.stdout)
        (p/'explanation.txt').write_text('The available comparison skill supports pure statevectors and unitaries and explicitly excludes shot statistics. No skill selected. For independent Bernoulli shots, p_hat=62/173 and plug-in SE=sqrt(p_hat*(1-p_hat)/173).\n'+json.dumps(result)+'\n')
        records.append({'id':tid,'selected_skill':None,'chosen_context':'independent Bernoulli counts; observed proportion and usual plug-in standard error','clarification_question':None,'status':'completed','answer':result,'evidence_paths':[str(p/x) for x in ['raw-task.json','request.json','calculate.py','stdout.json','stderr.txt','execution.json','explanation.txt']],'verification':{'status':'pending'},'limitations':['Plug-in standard error assumes the stated independent Bernoulli trials; it is not a confidence interval.']})
(out/'results.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps({r['id']:r['answer'] for r in records},indent=2))
