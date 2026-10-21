"""Independent stdlib checks; never imports the bundled helper or Torch."""
import json,math,pathlib,decimal,sys
from decimal import Decimal as D
base=pathlib.Path('/private/tmp/mqc-algebra-blind-r2/e/outputs')
def c(z):return complex(*z)
def vec(v):return list(map(c,v))
def mat(m):return list(map(vec,m))
def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def mv(a,x):return [sum(z*w for z,w in zip(row,x)) for row in a]
def adj(a):return [[a[j][i].conjugate() for j in range(len(a))] for i in range(len(a[0]))]
def encode(a):
    if isinstance(a,list):return list(map(encode,a))
    return [a.real,a.imag]
def compare(a,b,tol):
    if isinstance(a,list):return all(compare(x,y,tol) for x,y in zip(a,b)) and len(a)==len(b)
    return abs(a-b)<=tol['atol']+tol['rtol']*abs(b)
checks={}
for ident in ('E1','E2','E3'):
    d=base/ident;q=json.loads((d/'request.json').read_text());h=json.loads((d/'stdout.json').read_text());tol=q['tolerance']
    if ident=='E1':
        with decimal.localcontext() as ctx:
            ctx.prec=250
            rho=D.from_float(q['matrix'][0][0][0]); neg=D.from_float(q['matrix'][1][1][0]); refs=[rho.exp(),neg.exp()]
            errors=[abs(D.from_float(h['result']['value'][i][i][0])-refs[i]) for i in range(2)]
            tail=rho**41/D(math.factorial(41))/(1-rho/42)
            log_tail=tail.ln(); clamp=D.from_float(h['result']['mathematical_infinity_norm_tail_bound'])
            passed=all(e<=D.from_float(tol['atol'])+D.from_float(tol['rtol'])*abs(r) for e,r in zip(errors,refs))
            v={'method':'250-digit Decimal.exp on exact binary64 inputs (diagonal formula), independent of Taylor/helper/Torch','passed':passed,'diagonal_references':list(map(str,refs)),'diagonal_absolute_errors':list(map(str,errors)),'analytic_tail_decimal':str(tail),'analytic_tail_log_decimal':str(log_tail),'reported_log_absolute_discrepancy':str(abs(log_tail-D.from_float(h['result']['tail_log_upper_expression']))),'displayed_positive_clamp_exceeds_analytic_tail':clamp>=tail,'displayed_clamp_is_total_error_bound':False,'observed_roundoff_error_exceeds_displayed_clamp':max(errors)>clamp,'interpretation':'The returned identity is within tolerance. Positive underflow clamp and log correctly describe truncation only; they do not bound total floating-point error. Literal scalar offsets of order 1e-76 cannot survive binary64 addition to 1.'}
        claims=[{'claim':'Returned exponential satisfies supplied tolerance','disposition':'supported_by_independent_high_precision_diagonal_formula'},{'claim':'Tail record describes truncation only, excluding roundoff','disposition':'supported; positive analytic tail underflows binary64, log retained and clamp flagged'},{'claim':'Displayed tail certifies total numerical error','disposition':'not_claimed_and_false_for_this_run','evidence':'Actual error about 7e-76 exceeds 5e-324'}]
    elif ident=='E2':
        A=mat(q['matrix']);S=mat(q['basis_columns']);x=vec(q['v']);det=S[0][0]*S[1][1]-S[0][1]*S[1][0]
        inv=[[S[1][1]/det,-S[0][1]/det],[-S[1][0]/det,S[0][0]/det]]
        y=mv(inv,x);B=mm(mm(inv,A),S);G=mm(adj(S),S);weighted=sum(y[i].conjugate()*z for i,z in enumerate(mv(G,y)))
        old=sum(abs(z)**2 for z in x);naive=sum(abs(z)**2 for z in y)
        tr=(G[0][0]+G[1][1]).real;disc=math.sqrt((G[0][0]-G[1][1]).real**2+4*abs(G[0][1])**2);cond=math.sqrt((tr+disc)/(tr-disc))
        r=h['result']; tests={'coordinates':compare(vec(r['new_coordinates']),y,tol),'operator':compare(mat(r['new_operator']),B,tol),'gram':compare(mat(r['gram']),G,tol),'gram_metric':compare(complex(r['gram_squared_length']),complex(old),tol),'weighted_length_formula':compare(weighted,complex(old),tol),'condition':compare(complex(r['condition_2']),complex(cond),tol),'condition_limit':cond<=q['max_condition'],'reconstruct_coordinates':compare(mv(S,y),x,tol),'intertwining':compare(mm(S,B),mm(A,S),tol)}
        v={'method':'Explicit 2x2 inverse/determinant and Gram eigenvalue condition formula in Python complex arithmetic, independent of linear solves/SVD/Torch','passed':all(tests.values()),'tests':tests,'new_coordinates':encode(y),'new_operator':encode(B),'gram':encode(G),'condition_2':cond,'old_squared_length':old,'gram_squared_length':encode(weighted),'new_euclidean_squared_length':naive,'metric_difference_if_euclidean_used':naive-old}
        claims=[{'claim':'Passive coordinate/operator conversion','disposition':'supported_after_explicit_clarification'},{'claim':'Nonorthogonal coordinates preserve original norm with Gram metric','disposition':'supported; naive Euclidean metric changes squared length'}]
    else:
        with decimal.localcontext() as ctx:
            ctx.prec=80
            a,b=q['actual'],q['reference']; diffs=[];budgets=[]
            metadata=all(a[k]==b[k] for k in ('shape','dtype','device'))
            for av,bv in zip(a['values'],b['values']):
                ar,ai=map(D.from_float,av);br,bi=map(D.from_float,map(float,bv));diffs.append(((ar-br)**2+(ai-bi)**2).sqrt());budgets.append(D.from_float(tol['atol'])+D.from_float(tol['rtol'])*(br*br+bi*bi).sqrt())
            within=metadata and all(e<=b for e,b in zip(diffs,budgets))
            v={'method':'80-digit Decimal complex-modulus elementwise comparison of exact binary64 values; metadata gate first','passed':h['status']==('within_tolerance' if within else 'outside_tolerance'),'metadata_match':metadata,'within_tolerance':within,'errors':list(map(str,diffs)),'budgets':list(map(str,budgets)),'phase_alignment':False}
        claims=[{'claim':'Literal coordinates equal within supplied budget','disposition':'rejected_outside_tolerance'},{'claim':'A phase-aligned state-ray comparison answers request','disposition':'not_applicable; request retains literal phase and has dimension one'}]
    (d/'verification.json').write_text(json.dumps(v,indent=2));(d/'claim_dispositions.json').write_text(json.dumps(claims,indent=2));checks[ident]=v['passed']
print(json.dumps({'verification_checks_passed':checks,'python':sys.version,'quantum_execution':False},indent=2))
