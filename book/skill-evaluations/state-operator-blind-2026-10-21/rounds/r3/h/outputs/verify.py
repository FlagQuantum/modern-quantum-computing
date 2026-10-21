import json,math,pathlib,sys,decimal
root=pathlib.Path(__file__).resolve().parent.parent
out=root/'outputs'; checks={}
for task in json.loads((root/'tasks.json').read_text()):
    tid=task['id']; result=json.loads((out/tid/'stdout.json').read_text())
    if tid in ('H1','H2'):
        a=[[complex(*v) for v in row] for row in task['data']['a']]
        b=[[complex(*v) for v in row] for row in task['data']['b']]
        if tid=='H1':
            a=[[complex(int(i==j)) if i<2 and j<2 else (a[i-2][j-2] if i>=2 and j>=2 else 0j) for j in range(4)] for i in range(4)]
            b=[[complex(int(i==j)) if i<2 and j<2 else (b[i-2][j-2] if i>=2 and j>=2 else 0j) for j in range(4)] for i in range(4)]
        gram_error=max(abs(sum(m[k][i].conjugate()*m[k][j] for k in range(4))-int(i==j)) for m in (a,b) for i in range(4) for j in range(4))
        trace=sum(a[i][j].conjugate()*b[i][j] for i in range(4) for j in range(4))
        min_squared=sum(abs(v)**2 for row in a+b for v in row)-2*abs(trace)
        phase=complex(*result['alignment_multiplier_on_b'])
        direct=math.sqrt(sum(abs(a[i][j]-phase*b[i][j])**2 for i in range(4) for j in range(4)))
        assert gram_error<1e-12 and abs(abs(phase)-1)<1e-14
        assert abs(direct-result['decision_residual'])<1e-14
        assert abs(direct**2-min_squared)<1e-14
        if tid=='H1':
            assert min_squared>1e-10**2 and result['status']=='outside_tolerance'
        else:
            ratios=[a[i][j]/b[i][j] for i in range(4) for j in range(4) if abs(b[i][j])>0]
            assert max(abs(z-ratios[0]) for z in ratios)<1e-14
            assert direct<=1e-10 and result['status']=='within_tolerance'
        checks[tid]={'passed':True,'unitarity_max_entry_error':gram_error,'independent_min_squared_residual':min_squared,'direct_residual':direct}
    else:
        decimal.getcontext().prec=60
        D=decimal.Decimal; p=D(62)/D(173); se=(D(62)*D(111)/(D(173)**3)).sqrt()
        assert abs(float(p)-result['observed_proportion'])<1e-16
        assert abs(float(se)-result['plugin_standard_error'])<1e-16
        checks[tid]={'passed':True,'decimal_proportion':str(p),'decimal_standard_error':str(se)}
verification={'runtime':{'executable':sys.executable,'version':sys.version,'implementation':sys.implementation.name},'checks':checks}
(out/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
records=json.loads((out/'results.json').read_text())
for r in records:
    r['verification']={'status':'passed','details':checks[r['id']],'script_path':str(out/'verify.py'),'results_path':str(out/'verification.json')}
    r['evidence_paths'] += [str(out/'verification.json'),str(out/'verify.py'),str(out/'interpreter-system.stdout'),str(out/'interpreter-venv.stdout')]
(out/'results.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(verification,indent=2))
