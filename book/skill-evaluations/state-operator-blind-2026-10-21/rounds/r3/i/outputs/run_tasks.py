import json, pathlib, subprocess, sys, math, hashlib
ROOT=pathlib.Path('/private/tmp/mqc-comparison-blind-r3/i')
OUT=ROOT/'outputs'
def save(p,v):
    (OUT/p).write_text(json.dumps(v,indent=2,allow_nan=False)+'\n')
tasks=json.loads((ROOT/'tasks.json').read_text())
env=json.loads((ROOT/'environment.json').read_text())
skill='compare-quantum-states-and-operators'
helper=ROOT/'skills'/skill/'scripts/compare.py'
probes=[]
for candidate in env['python_candidates']:
    args=[candidate,'-c','import sys,json; print(json.dumps({"executable":sys.executable,"implementation":sys.implementation.name,"version":sys.version,"version_info":list(sys.version_info[:3])}))']
    p=subprocess.run(args,text=True,capture_output=True)
    probes.append({'argv':args,'stdout':p.stdout,'stderr':p.stderr,'exit_code':p.returncode})
save('interpreter_probes.json',probes)
py=next(json.loads(p['stdout'])['executable'] for p in probes if p['exit_code']==0 and json.loads(p['stdout'])['implementation']=='cpython' and json.loads(p['stdout'])['version_info'][:2]==[3,12])
save('actual_interpreter.json',{'driver_executable':sys.executable,'driver_version':sys.version,'helper_executable':py})
save('input_hashes_before.json',{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'catalog.json',ROOT/'tasks.json',ROOT/'environment.json',*sorted((ROOT/'skills').rglob('*'))] if p.is_file()})
results=[]
for t in tasks:
    ident=t['id']; folder=OUT/ident; folder.mkdir(exist_ok=True)
    save(f'{ident}/supplied_task.json',t)
    d=t['data']
    r={'id':ident,'selected_skill':skill,'chosen_context':None,'clarification_question':None,'status':None,'evidence_paths':[f'outputs/{ident}/supplied_task.json'],'verification':None,'limitations':[]}
    if ident in ('I1','I2','I3'):
        r['chosen_context']={'kind':'state','mode':'global-phase','atol':1e-10,'basis_a':d['basis_a'],'basis_b':d['basis_b']}
        req={**d,'mode':'global-phase','atol':1e-10}
        save(f'{ident}/request.json',req)
        argv=[py,str(helper)]
        p=subprocess.run(argv,input=(folder/'request.json').read_text(),capture_output=True,text=True)
        (folder/'stdout.json').write_text(p.stdout); (folder/'stderr.txt').write_text(p.stderr)
        save(f'{ident}/execution.json',{'argv':argv,'stdin_path':str(folder/'request.json'),'stdout_path':str(folder/'stdout.json'),'stderr_path':str(folder/'stderr.txt'),'exit_code':p.returncode})
        actual=json.loads(p.stdout)
        r['status']=actual['status']
        r['evidence_paths'] += [f'outputs/{ident}/{name}' for name in ['request.json','stdout.json','stderr.txt','execution.json']]
        if ident=='I1':
            r['explanation']='The explicit different basis declarations are preserved. The supplied helper rejects the noncanonical second basis with exit 3. This is an unsupported basis contract, not an inequality result. No permutation or relabeling was applied.'
            r['limitations']=['Canonical identical basis declarations are required by this profile. No documented transformation is supplied or authorized.']
        else:
            cached=t['cached_result']['status']; r['explanation']=f'Fresh raw-array comparison returns {actual["status"]}, contradicting cached status {cached}. Cached residual was not used as evidence.'
            r['limitations']=['Finite binary64 numerical comparison at absolute Euclidean tolerance 1e-10, normalization validation tolerance 1e-12; no exact equality theorem or provenance verification.']
    elif ident=='I4':
        r['selected_skill']=None
        r['chosen_context']={'kind':'density','meaning':'mixed-state density matrices','basis_a':d['basis_a'],'basis_b':d['basis_b']}
        r['status']='unsupported'
        r['explanation']='No. The sole available skill covers pure statevectors and unitaries, and cannot certify mixed density matrices. Arrays are retained as matrices; no vectors, pure-state mode, or helper object-comparison claim was substituted.'
        r['limitations']=['A density-matrix comparison profile with its own tolerance, validity and metric contract is required; none is available in the supplied catalog.']
        save(f'{ident}/execution.json',{'executed':False,'reason':'Out-of-scope density representation; no valid helper request prepared.'})
        r['evidence_paths'].append(f'outputs/{ident}/execution.json')
    else:
        r['chosen_context']={'meaning':d['context'],'producer':d['producer'],'dtype':d['dtype'],'shape':d['shape'],'device':d['device'],'basis':d['basis']}
        r['status']='not_admissible'
        r['explanation']='These exports are not admissible as verified FlagQuantum outputs. Producer is explicitly unverified, declared dtype is complex64 and there is a leading batch axis [1,2]. The validated adapter profile uses actual FlagQuantum 0.3.1 CPU complex128, and requires producer-side validation plus export of exactly one validated sample. No axis removal, cast or comparison was performed.'
        r['limitations']=['Actual producing API/version, producer validation, and actual ordering are not evidenced. CPU metadata alone does not establish producer provenance. Need a validated source program/export meeting the profile before comparison.']
        save(f'{ident}/execution.json',{'executed':False,'reason':'Producer contract not established; preserved dtype and batch metadata, so comparison not admitted.'})
        r['evidence_paths'].append(f'outputs/{ident}/execution.json')
    save(f'{ident}/explanation.json',r)
    results.append(r)
save('results.json',results)
print(json.dumps({'tasks_executed':[r['id'] for r in results[:3]],'helper_executable':py,'statuses':{r['id']:r['status'] for r in results}},indent=2))
