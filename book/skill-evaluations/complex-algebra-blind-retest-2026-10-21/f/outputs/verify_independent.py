"""Independent exact rational pair arithmetic; no skill helper or Torch imports."""
import json,pathlib
from fractions import Fraction as Q
root=pathlib.Path('/private/tmp/mqc-algebra-blind-r2/f/outputs')
def scalar(p): return tuple(Q(str(x)) for x in p)
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def mul(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def matmul(a,b):
    return [[sumc(mul(a[i][k],b[k][j]) for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def sumc(items):
    s=(Q(0),Q(0))
    for x in items:s=add(s,x)
    return s
def encode(a):return [[[str(x),str(y)] for x,y in row] for row in a]
results=[]
for ident in ('F1','F2'):
    p=root/ident; q=json.loads((p/'request.json').read_text()); got=json.loads((p/'stdout.json').read_text())
    a=[[scalar(x) for x in row] for row in q['matrix']]; n=len(a); eye=[[(Q(int(i==j)),Q(0)) for j in range(n)] for i in range(n)]
    if ident=='F1':
        assert all(z==(0,0) for row in a for z in row)
        ref=eye
        metadata={'zero_input_exact':True,'exp_zero_identity_exact':True,'rho':0,'all_taylor_terms_above_degree_zero_vanish':True,'expected_truncation_tail':0,'expected_log_tail':None,'expected_underflow_clamped':False,'expected_interval_certificate':False,'expected_excludes_roundoff':True}
        r=got['result']; metadata['metadata_passed']=(r['mathematical_infinity_norm_tail_bound']==0 and r['tail_log_upper_expression'] is None and r['tail_bound_underflow_clamped'] is False and r['tail_numeric_record_is_interval_certificate'] is False and r['tail_bound_excludes_roundoff'] is True)
    else:
        power=eye; ref=[[(Q(0),Q(0)) for j in range(n)] for i in range(n)]; powers=[]
        for c in map(scalar,q['coefficients']):
            powers.append(encode(power))
            ref=[[add(ref[i][j],mul(c,power[i][j])) for j in range(n)] for i in range(n)]; power=matmul(power,a)
        metadata={'method':'exact rational direct matrix powers summed in ascending coefficient order','powers':powers}
    checks=[]
    for i in range(n):
        for j in range(n):
            actual=complex(*got['result']['value'][i][j]); expected=complex(float(ref[i][j][0]),float(ref[i][j][1])); error=abs(actual-expected); budget=q['tolerance']['atol']+q['tolerance']['rtol']*abs(expected)
            checks.append({'index':[i,j],'absolute_error':error,'reference_scaled_budget':budget,'passed':error<=budget})
    result={'id':ident,'reference_exact_rational':encode(ref),'checks':checks,'metadata_audit':metadata,'passed':all(c['passed'] for c in checks) and metadata.get('metadata_passed',True),'limitations':['Exact rational reference treats the supplied decimal coordinates as exact; returned binary64 values are checked against its conversion under the declared asymmetric tolerance.','No interval or hardware/circuit accuracy certificate is inferred.']}
    (p/'independent_verification.json').write_text(json.dumps(result,indent=2)); results.append(result)
print(json.dumps(results,indent=2))
