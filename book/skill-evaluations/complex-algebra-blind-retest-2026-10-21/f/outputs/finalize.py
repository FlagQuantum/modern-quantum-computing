import json,pathlib,subprocess,time
b=pathlib.Path('/private/tmp/mqc-algebra-blind-r2/f'); o=b/'outputs'; py='/private/tmp/mqc-writing-venv/bin/python'
def run(argv,stdin,out,err,record):
    t=time.perf_counter(); p=subprocess.run(argv,input=stdin,text=True,capture_output=True)
    out.write_text(p.stdout);err.write_text(p.stderr);record.write_text(json.dumps({'argv':argv,'exit_code':p.returncode,'elapsed_seconds':time.perf_counter()-t,'quantum_execution':False},indent=2))
p=o/'F3';run([py,str(b/'skills/translate-complex-linear-algebra/scripts/algebra.py')],(p/'request.json').read_text(),p/'stdout.json',p/'stderr.txt',p/'execution.json')
run([py,str(o/'verify_independent.py')],None,o/'independent_verification.stdout.json',o/'independent_verification.stderr.txt',o/'independent_verification.execution.json')
clarification={'question':'Which matrix square-root domain and branch convention should be used for sqrt(-I)?','asked_to':'/root','answer':'No square-root branch or domain is supplied. Keep this request unsupported, without selecting a branch or claiming a unique answer. A separate explanation of ambiguity is appropriate.','disposition':'unsupported; no branch selected'}
(p/'clarification.json').write_text(json.dumps(clarification,indent=2))
claims={
'F1':{'status':'accepted_with_scope','output':'exp(0)=I_2; exact identity independently established from the power series.','metadata':'Tail 0 is correct for rho=0, log bound null correctly represents the zero-input special case, underflow flag false. All omitted Taylor terms vanish exactly. The helper explicitly excludes roundoff and disclaims interval certification.','certified':'For this input, exact mathematical identity and numerical agreement at atol=1e-11, rtol=1e-12; displayed metadata is consistent.','not_certified':'No general matrix-exponential forward-error interval, upstream computation, quantum execution, hardware claim, or scientific acceptance.'},
'F2':{'status':'accepted_with_scope','formula':'0.31 I + 0.43 i A - 0.23 A^2','output':[[[0.276822,0],[0,0.108692]],[[0,-0.063716],[0.269326,0]]],'verification':'Exact rational direct powers independently confirm the helper result within atol=1e-11, rtol=1e-12.','not_certified':'No quantum execution, symbolic general theorem, or paper acceptance.'},
'F3':{'status':'unsupported','reason':'The provided helper excludes square-root branch selection, and no domain or branch convention was supplied.','ambiguity':'Both iI and -iI square to -I; more generally this matrix admits distinct square roots. This explains nonuniqueness without selecting any output.','not_certified':'No selected square-root answer, branch implementation, or unsupported-as-inequality inference.'}}
results=[]
for ident in ('F1','F2','F3'):
    p=o/ident; (p/'claim_disposition.json').write_text(json.dumps(claims[ident],indent=2))
    h=json.loads((p/'stdout.json').read_text())
    evidence=[str(x) for x in sorted(p.iterdir()) if x.is_file()]+[str(o/'verify_independent.py'),str(o/'run_tasks.py'),str(o/'finalize.py')]
    results.append({'id':ident,'selected_skills':['translate-complex-linear-algebra'],'chosen_context':{'task':'function','kind':json.loads((p/'request.json').read_text())['kind'],'coordinates':'literal-complex','units':'dimensionless','execution':'classical CPU complex128; no FlagQuantum or quantum circuit','interpreter':py,'runtime':h['runtime'],'torch':h.get('versions',{}).get('torch','2.13.0 per runtime probe')},'clarification_question':clarification if ident=='F3' else None,'status':h['status'],'evidence_paths':evidence,'verification':json.loads((p/'independent_verification.json').read_text()) if ident!='F3' else {'status':'unsupported','actual_helper_exit_code':3,'no_dependent_branch_computation':True,'explanation':'Distinct roots demonstrate need for branch; helper rejects sqrt scope.'},'limitations':claims[ident]['not_certified']})
(o/'results.json').write_text(json.dumps(results,indent=2))
print(json.dumps({'results_path':str(o/'results.json'),'statuses':{x['id']:x['status'] for x in results}}))
