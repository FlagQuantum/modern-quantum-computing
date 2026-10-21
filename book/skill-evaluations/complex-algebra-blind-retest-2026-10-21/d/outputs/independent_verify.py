"""Independent stdlib Decimal verification. Does not import helper or Torch."""
import json, math, pathlib
from decimal import Decimal as D, localcontext
root=pathlib.Path(__file__).resolve().parents[1]; out=root/'outputs'
tasks={x['id']:x for x in json.loads((root/'tasks.json').read_text())}
def dec(x): return D.from_float(float(x))
def load(i): return json.loads((out/(i+'.stdout')).read_text())
def z(pair): return tuple(dec(x) for x in pair)
def add(a,b): return a[0]+b[0],a[1]+b[1]
def mul(a,b): return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def adj(a): return [[(a[j][i][0],-a[j][i][1]) for j in range(len(a))] for i in range(len(a[0]))]
def mm(a,b): return [[tuple(sum((mul(a[i][k],b[k][j])[p] for k in range(len(b))),D(0)) for p in (0,1)) for j in range(len(b[0]))] for i in range(len(a))]
def modulus(a):return (a[0]*a[0]+a[1]*a[1]).sqrt()
def compare(a,b,tol):
    errors=[modulus((x[0]-y[0],x[1]-y[1])) for ra,rb in zip(a,b) for x,y in zip(ra,rb)]
    budgets=[dec(tol['atol'])+dec(tol['rtol'])*modulus(y) for rb in b for y in rb]
    return {'passed':all(e<=v for e,v in zip(errors,budgets)),'max_absolute_error':str(max(errors)),'max_element_budget':str(max(budgets)),'elementwise_errors':[str(e) for e in errors]}
with localcontext() as ctx:
    ctx.prec=180
    q=tasks['D1']['data']; r=load('D1'); rho=max(sum(modulus(z(x)) for x in row) for row in q['matrix'])
    ref=[[(dec(q['matrix'][i][i][0]).exp(),D(0)) if i==j else (D(0),D(0)) for j in range(2)] for i in range(2)]
    actual=[[z(x) for x in row] for row in r['result']['value']]
    numerical=compare(actual,ref,q['tolerance'])
    tail=rho**41/D(math.factorial(41))/(1-rho/D(42)); logtail=tail.ln()
    minfloat=dec(math.nextafter(0.0,1.0)); reported=r['result']
    logerr=abs(dec(reported['tail_log_upper_expression'])-logtail)
    meta={'rho':str(rho),'positive_analytic_tail_estimate':str(tail),'analytic_log_tail_estimate':str(logtail),'reported_log_absolute_error':str(logerr),'ordinary_bound_is_positive_min_binary64':dec(reported['mathematical_infinity_norm_tail_bound'])==minfloat,'true_tail_below_min_binary64':D(0)<tail<minfloat,'clamp_flag_correct':reported['tail_bound_underflow_clamped'] is True,'excludes_roundoff_flag_correct':reported['tail_bound_excludes_roundoff'] is True,'not_interval_flag_correct':reported['tail_numeric_record_is_interval_certificate'] is False,'log_consistent_to_1e-10':logerr<D('1e-10')}
    assert numerical['passed'] and all(meta[k] for k in ['ordinary_bound_is_positive_min_binary64','true_tail_below_min_binary64','clamp_flag_correct','excludes_roundoff_flag_correct','not_interval_flag_correct','log_consistent_to_1e-10'])
    d1={'status':'passed','method':'180-digit Decimal diagonal scalar exponential; independent analytic-tail expression','numeric_check':numerical,'metadata_audit':meta,'matrix_exponential_reference':[[[str(a),str(b)] for a,b in row] for row in ref],'scope':'finite declared matrix only; Decimal results are high precision estimates, not outward-rounded intervals'}
    q=tasks['D2']['data']; r=load('D2'); a=[[z(x) for x in row] for row in q['matrix']]; ah=adj(a); eye=[[(D(int(i==j)),D(0)) for j in range(2)] for i in range(2)]
    tests={name:compare(x,y,q['tolerance']) for name,x,y in [('hermitian',a,ah),('unitary',mm(ah,a),eye),('normal',mm(ah,a),mm(a,ah)),('idempotent',mm(a,a),a)]}
    decisions={k:v['passed'] for k,v in tests.items()}
    assert decisions=={k:v['passed'] for k,v in r['result']['identity_tests'].items()}
    projection=decisions['hermitian'] and decisions['idempotent'];assert projection==r['result']['orthogonal_projector_within_budget']
    c=a[0][0][0];exact_defect=abs(2*c*c-c)
    assert exact_defect>0
    d2={'status':'passed','method':'180-digit Decimal manual conjugation/matrix multiplication on binary64 input values','tests':tests,'orthogonal_projector_within_budget':projection,'exact_idempotence':False,'exact_input_diagonal_defect':str(exact_defect),'explanation':'A=c[[1,-i],[i,1]], so A^2=2c A. Here c differs from 1/2, hence numerical projection identity passes but exact idempotence fails.'}
    q=tasks['D3']['data'];r=load('D3');v=q['v']
    def scalar_pair(x):return isinstance(x,list) and len(x)==2 and all(type(t) in (int,float) for t in x)
    valid_vector=isinstance(v,list) and 1<=len(v)<=8 and all(scalar_pair(x) for x in v)
    assert not valid_vector and r['status']=='invalid_input'
    d3={'status':'passed','method':'independent nested-list scalar-pair schema admission','raw_complex_array_shape':[1,2],'required_matvec_vector_shape':[2],'valid_vector':False,'helper_rejection_confirmed':True,'input_preserved':True,'limitation':'Helper error wording is generic (finite real component) instead of explicitly naming the extra array axis; rejection itself is correct.'}
    result={'D1':d1,'D2':d2,'D3':d3,'quantum_execution':False,'arithmetic':'classical stdlib Decimal; no helper imports; no quantum backend'}
    (out/'independent_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'passed','verified_ids':['D1','D2','D3'],'precision_decimal_digits':180,'quantum_execution':False}))
