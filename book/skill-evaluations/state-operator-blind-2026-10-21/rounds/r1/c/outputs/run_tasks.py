import json, pathlib, subprocess, sys, math
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs'
tasks = json.loads((ROOT/'tasks.json').read_text())
helper = ROOT/'skills/compare-quantum-states-and-operators/scripts/compare.py'
results=[]
for task in tasks:
    ident=task['id']; dest=OUT/ident; dest.mkdir(exist_ok=True)
    (dest/'supplied_task.json').write_text(json.dumps(task,indent=2)+'\n')
    if ident in ['C1','C2','C3']:
        req=dict(task['data']); req['mode']='coordinates' if ident=='C3' else 'global-phase'; req['atol']=1e-10
        (dest/'request.json').write_text(json.dumps(req,indent=2)+'\n')
        run=subprocess.run([sys.executable,str(helper)],input=json.dumps(req),capture_output=True,text=True)
        (dest/'stdout.json').write_text(run.stdout); (dest/'stderr.txt').write_text(run.stderr)
        (dest/'execution.json').write_text(json.dumps({'argv':[sys.executable,str(helper)],'stdin':'request.json','exit_code':run.returncode},indent=2)+'\n')
        actual=json.loads(run.stdout)
    if ident=='C1':
        context={'kind':'state','dimension':4,'mode':'global-phase','atol':1e-10,'basis_a':task['data']['basis_a'],'basis_b':task['data']['basis_b']}
        explanation='The helper returns unsupported (exit 3): basis_b is noncanonical and differs from basis_a. Coordinates and basis labels were passed unchanged. Identical numeric arrays do not establish equality under different declared orders. No physical inequality is certified. The user forbids the explicit reorder/transformation needed to enter this profile.'
        status='unsupported'; limits=['No comparison decision is available under the supplied basis declarations.','No permutation was inferred or applied.']
    elif ident=='C2':
        context={'kind':'state','dimension':2,'mode':'global-phase','basis':['0','1'],'atol':1e-10}
        explanation=f"The fresh helper execution returns {actual['status']} (exit {run.returncode}); aligned Euclidean residual is {actual['aligned_residual']:.17g}, exceeding 1e-10. The cached within_tolerance result and zero residual are unreliable. The two basis probabilities coincide, but relative phase differs. The multiplier on b is recorded in stdout.json; inputs were not normalized or repaired."
        status=actual['status']; limits=['Binary64 numerical comparison of the supplied arrays, not exact equality proof or producer validation.']
    elif ident=='C3':
        context={'kind':'density','meaning':'mixed-state density operators','basis':['0','1'],'requested_relation':'matrix equality including mixed-state interpretation','helper_probe':'coordinates, solely to record representation rejection'}
        explanation='The available skill cannot certify density matrices or their mixed-state meaning. A representation-boundary probe returns unsupported (exit 3) before inspecting entries; coordinates in that diagnostic request does not substitute a pure-state comparison. The raw nested matrices are preserved. Their supplied entries agree, but a density-operator profile with Hermiticity, trace, positivity and the declared state metric is needed for the requested certification.'
        status='unsupported'; limits=['No density-matrix certification profile is available in the supplied catalog.','No statevector substitution was made.']
    else:
        context={'kind':'producer statevector export','requested_admission':'verified FlagQuantum','claimed_context':task['data']['context'],'dtype':task['data']['dtype'],'device':task['data']['device'],'shape':task['data']['shape'],'producer':task['data']['producer'],'basis':task['data']['basis']}
        explanation='These exports cannot be admitted as verified FlagQuantum statevectors. The producer is explicitly unverified, and no actual API/version or producing-program validation evidence is supplied. Shape [1,2] contains a batch axis outside the JSON state profile, and complex64 cannot be silently widened into its binary64 profile. The profile requires an exactly one-sample export after producer checks of API/version, shape, dtype, device, finiteness, normalization and declared order. The raw export is saved unchanged; no squeeze, widening, repair or comparison was executed.'
        status='unsupported'; limits=['No real producer validation can be performed from metadata assertions alone.','CPU device and basis declarations do not verify actual producing behavior.','A validated compatible producer export is required for future comparison.']
        (dest/'admission.json').write_text(json.dumps({'status':'unsupported','helper_executed':False,'reasons':['unverified producer and no API/version evidence','batch axis outside state profile','complex64 must not be silently widened'],'preserved_metadata':context},indent=2)+'\n')
    (dest/'explanation.txt').write_text(explanation+'\n')
    evidence=[str(p.relative_to(OUT)) for p in sorted(dest.iterdir())]
    results.append({'id':ident,'selected_skill':'compare-quantum-states-and-operators','chosen_context':context,'clarification_question':None,'status':status,'evidence_paths':evidence,'verification':{'script':'verify.py','report':'verification.json','result':'pending'},'limitations':limits})
(OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'tasks_processed':len(results),'helper_executions':3,'results':'outputs/results.json'}))
