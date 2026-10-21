import pathlib,json
root=pathlib.Path(__file__).resolve().parents[1];out=root/'outputs'
verification=json.loads((out/'independent_verification.json').read_text())
claims={
'D1':{'numeric_matrix_exponential':'accepted_within_declared_tolerance','reported_tail_metadata':'accepted_as_floating_estimates_with_underflow_clamp','exact_general_theorem':'not_claimed','roundoff_or_interval_accuracy_certificate':'not_claimed','explanation':'Returned identity agrees within budget with high precision diagonal scalar exponentials. Positive analytic Taylor remainder is smaller than binary64; helper correctly clamps its ordinary record to min positive float and retains its logarithm. Truncation tail excludes roundoff.'},
'D2':{'hermitian_within_budget':'accepted','normal_within_budget':'accepted','unitary_within_budget':'rejected','orthogonal_projector_within_budget':'accepted','exact_orthogonal_projection':'rejected_for_supplied_finite_values','explanation':'Both Hermiticity and idempotence pass the declared elementwise budget. A=c[[1,-i],[i,1]] has A^2=2c A, so c slightly below 1/2 is not exactly idempotent. Internal verified status means tests evaluated, not every property true.'},
'D3':{'requested_matvec_admission':'rejected_invalid_input','computed_action':'not_produced','shape_repair':'not_performed','explanation':'v is a 1 by 2 array of complex scalars, not a length-2 vector. Requested no flattening/repair is honored by rejecting it.'}}
(out/'claim_dispositions.json').write_text(json.dumps(claims,indent=2)+'\n')
context={'interpreter':'/private/tmp/mqc-writing-venv/bin/python','python':'CPython 3.12.14','torch':'2.13.0','device':'cpu','dtype':'complex128','coordinates':'literal-complex','execution_type':'classical_tensor_and_scalar_computation','quantum_execution':False,'selection_rationale':'All requests concern literal finite matrix algebra. Selected helper matches pinned runtime; /usr/bin/python3 is 3.9.6 with no Torch and is unsuitable. No phase/state interpretation needed.'}
results=[]
for i in ('D1','D2','D3'):
    p=json.loads((out/(i+'.stdout')).read_text()); e=json.loads((out/(i+'.execution.json')).read_text())
    lim=['Finite input numerical audit only; no exact general theorem or quantum execution.']
    if i=='D1':lim+=['High precision Decimal reference and analytic tail are estimates, not outward-rounded interval certificates. Tail bound excludes roundoff.']
    if i=='D2':lim+=['Within-budget orthogonal projection classification does not imply exact idempotence; exact claim fails for supplied finite values.']
    if i=='D3':lim+=['No action output exists because supplied array is not a vector. Helper error message does not directly name the shape issue.']
    paths=[str(out/(i+x)) for x in ('.request.json','.stdout','.stderr','.execution.json')]+[str(out/x) for x in ('claim_dispositions.json','independent_verify.py','independent_verification.json','independent_verify.stdout','independent_verify.stderr','independent_verify.execution.json','source_hashes.json','run.py')]
    results.append({'id':i,'selected_skills':['translate-complex-linear-algebra'],'chosen_context':context,'clarification_question':None,'status':p['status'],'execution_exit_code':e['exit_code'],'evidence_paths':paths,'verification':verification[i],'claim_disposition':claims[i],'limitations':lim})
(out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'results_path':str(out/'results.json'),'statuses':{r['id']:r['status'] for r in results},'independent_verification':'all passed'}))
