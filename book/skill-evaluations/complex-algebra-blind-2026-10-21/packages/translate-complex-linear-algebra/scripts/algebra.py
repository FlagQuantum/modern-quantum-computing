#!/usr/bin/env python3
"""Small dense complex algebra with explicit shape, coordinate and tolerance contracts."""
import cmath,json,math,sys
from importlib.metadata import version,PackageNotFoundError
VERSION='0.1.0'
class Invalid(ValueError):pass
class Unsupported(ValueError):pass

def real(x,bound=1e6):
    if type(x) not in (int,float) or not -bound<=x<=bound:raise Invalid('Finite real component within declared bound required')
    if x and abs(x)<1e-100:raise Invalid('Nonzero input components below 1e-100 are outside this profile')
    return float(x)
def scalar(x):
    if not isinstance(x,list) or len(x)!=2:raise Invalid('Complex number requires [real,imaginary]')
    return complex(real(x[0]),real(x[1]))
def vector(x):
    if not isinstance(x,list) or not 1<=len(x)<=8:raise Invalid('Vector length 1..8 required; no implicit batch stripping')
    return [scalar(z) for z in x]
def matrix(x):
    if not isinstance(x,list) or not 1<=len(x)<=8 or not isinstance(x[0],list) or not 1<=len(x[0])<=8:raise Invalid('Dense matrix dimensions 1..8 required')
    n=len(x[0])
    if any(not isinstance(row,list) or len(row)!=n for row in x):raise Invalid('Ragged matrix')
    return [[scalar(z) for z in row] for row in x]
def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def mv(a,v):return [sum(x*y for x,y in zip(row,v)) for row in a]
def adj(a):return [[a[i][j].conjugate() for i in range(len(a))] for j in range(len(a[0]))]
def encode(x):
    if isinstance(x,list):return [encode(z) for z in x]
    z=complex(x);return [z.real,z.imag]
def flat(x):
    if isinstance(x,list):return [z for y in x for z in flat(y)]
    return [complex(x)]
def norm(v):return math.sqrt(sum(abs(z)**2 for z in v))
def check(a,b,tol):
    aa,bb=flat(a),flat(b)
    if len(aa)!=len(bb):raise RuntimeError('Internal shape mismatch')
    errors=[abs(x-y) for x,y in zip(aa,bb)];budgets=[tol['atol']+tol['rtol']*abs(y) for y in bb]
    if not all(math.isfinite(z) for z in errors+budgets):raise RuntimeError('Nonfinite comparison arithmetic')
    return {'max_absolute_error':max(errors,default=0.),'max_element_budget':max(budgets,default=0.),'passed':all(e<=b for e,b in zip(errors,budgets))}
def tolvalue(x):
    if type(x) not in (int,float) or not 0<=x<=1e-8:raise Invalid('atol/rtol must be finite nonnegative numbers <=1e-8')
    return float(x)
def keys(q,required,optional=()):
    fields={'task','coordinates','tolerance'}|set(required)
    if not fields<=set(q) or set(q)-fields-set(optional):raise Invalid('Missing/extra task fields; required '+','.join(sorted(fields)))
def validate_common(q):
    if not isinstance(q,dict) or not {'task','coordinates','tolerance'}<=set(q):raise Invalid('Required: task,coordinates,tolerance and task-specific fields')
    if q['coordinates']!='literal-complex':raise Unsupported('Literal complex coordinates required; no phase alignment or state normalization')
    t=q['tolerance']
    if not isinstance(t,dict) or set(t)!={'atol','rtol'}:raise Invalid('Explicit tolerance requires atol and rtol')
    return {k:tolvalue(t[k]) for k in ('atol','rtol')}
def main_run(q):
    tol=validate_common(q)
    try:tv=version('torch')
    except PackageNotFoundError as e:raise Unsupported('PyTorch runtime missing') from e
    if tv.split('+')[0]!='2.13.0':raise Unsupported('Torch base 2.13.0 required')
    import torch
    D=torch.complex128
    def T(a):return torch.tensor(a,dtype=D,device='cpu')
    def arr(t):
        if not torch.isfinite(t).all():raise RuntimeError('Nonfinite tensor output')
        return t.tolist()
    def square(a):
        if len(a)!=len(a[0]):raise Invalid('Square matrix required')
    def hermitian(a):
        square(a);scale=max(abs(z) for row in a for z in row)
        if max(abs(a[i][j]-a[j][i].conjugate()) for i in range(len(a)) for j in range(len(a)))>1e-12*scale:raise Invalid('Hermitian input required, scale-relative max-entry tolerance 1e-12; no symmetrization')
    def condition(a,limit):
        if type(limit) not in (int,float) or not 1<=limit<=1e12:raise Invalid('Explicit max_condition must be in [1,1e12]')
        singular=torch.linalg.svdvals(a);lo,hi=singular[-1].item(),singular[0].item()
        if lo==0:raise Invalid('Singular matrix is not an invertible basis/solve input')
        k=hi/lo
        if not math.isfinite(k) or k>limit:raise Unsupported('Condition number exceeds caller limit; no trustworthy-solve certification')
        return k,lo,hi
    task=q['task'];result={};checks={};mat=None
    if task=='algebra':
        op=q.get('operation')
        if op=='inner':
            keys(q,('operation','v','w'));v,w=vector(q['v']),vector(q['w'])
            if len(v)!=len(w):raise Invalid('Vector dimensions differ')
            value=arr(torch.vdot(T(v),T(w)));ref=sum(x.conjugate()*y for x,y in zip(v,w));result={'value':encode(value),'shape':[],'squared_norm_v':norm(v)**2,'squared_norm_w':norm(w)**2}
        elif op=='outer':
            keys(q,('operation','v','w'));v,w=vector(q['v']),vector(q['w']);value=arr(torch.outer(T(v),T(w).conj()));ref=[[x*y.conjugate() for y in w] for x in v];result={'value':encode(value),'shape':[len(v),len(w)]}
        elif op=='adjoint':
            keys(q,('operation','matrix'));a=matrix(q['matrix']);value=arr(T(a).mH);ref=adj(a);result={'value':encode(value),'shape':[len(a[0]),len(a)]}
        elif op=='matvec':
            keys(q,('operation','matrix','v'));a,v=matrix(q['matrix']),vector(q['v'])
            if len(a[0])!=len(v):raise Invalid('Matrix/vector dimensions differ')
            value=arr(T(a)@T(v));ref=mv(a,v);result={'value':encode(value),'shape':[len(a)]}
        elif op=='matmul':
            keys(q,('operation','left','right'));a,b=matrix(q['left']),matrix(q['right'])
            if len(a[0])!=len(b):raise Invalid('Product dimensions differ')
            value=arr(T(a)@T(b));ref=mm(a,b);result={'value':encode(value),'shape':[len(a),len(b[0])]}
        else:raise Unsupported('algebra operations: inner,outer,adjoint,matvec,matmul')
        checks['independent_scalar_reference']=check(value,ref,tol)
    elif task=='basis':
        keys(q,('matrix','basis_columns','v','direction','max_condition'))
        if q['direction']!='passive-new-in-old':raise Unsupported('Clarify active/passive and column convention; supported direction passive-new-in-old')
        a,s,x=matrix(q['matrix']),matrix(q['basis_columns']),vector(q['v']);square(a);square(s)
        if len(a)!=len(s) or len(x)!=len(s):raise Invalid('Basis/operator/vector dimensions differ')
        A,S,X=T(a),T(s),T(x);k,_,_=condition(S,q['max_condition'])
        y=torch.linalg.solve(S,X);b=torch.linalg.solve(S,A@S);gram=S.mH@S
        result={'new_coordinates':encode(arr(y)),'new_operator':encode(arr(b)),'gram':encode(arr(gram)),'condition_2':k,'old_squared_length':torch.vdot(X,X).real.item(),'new_euclidean_squared_length':torch.vdot(y,y).real.item(),'gram_squared_length':torch.vdot(y,gram@y).real.item(),'direction':'passive: x_old=S*x_new; B=S^-1*A*S'}
        checks={'coordinate_reconstruction':check(arr(S@y),x,tol),'operator_intertwining':check(arr(S@b),arr(A@S),tol),'action_reconstruction':check(arr(S@(b@y)),mv(a,x),tol),'metric':check(result['gram_squared_length'],result['old_squared_length'],tol)}
    elif task=='classify':
        keys(q,('matrix',));a=matrix(q['matrix']);square(a);A=T(a);eye=torch.eye(len(a),dtype=D);zero=torch.zeros_like(A)
        tests={'hermitian':check(a,adj(a),tol),'unitary':check(arr(A.mH@A),arr(eye),tol),'normal':check(arr(A.mH@A),arr(A@A.mH),tol),'idempotent':check(arr(A@A),a,tol)}
        result={'identity_tests':tests,'orthogonal_projector_within_budget':tests['hermitian']['passed'] and tests['idempotent']['passed'],'classification_is_exact_theorem':False}
        checks['adjoint_identity']=check(arr(A.mH.mH),a,tol)
    elif task=='decompose':
        keys(q,('matrix','kind'),('rank_rtol',));a=matrix(q['matrix']);A=T(a);m,n=A.shape
        if q['kind']=='hermitian':
            if 'rank_rtol' in q:raise Invalid('rank_rtol is only an SVD cutoff')
            hermitian(a);values,Q=torch.linalg.eigh(A);rebuilt=(Q*values)@Q.mH
            result={'eigenvalues':arr(values),'eigenvectors_columns':encode(arr(Q)),'reconstruction':encode(arr(rebuilt)),'gauge':'Do not compare eigenvector phases or bases inside degenerate subspaces; use eigenspace projectors'}
            checks={'reconstruction':check(arr(rebuilt),a,tol),'orthonormal_columns':check(arr(Q.mH@Q),arr(torch.eye(n,dtype=D)),tol),'eigenpairs':check(arr(A@Q),arr(Q*values),tol)}
        elif q['kind']=='svd':
            cutoff=q.get('rank_rtol',1e-12)
            if type(cutoff) not in (int,float) or not 0<=cutoff<=1e-6:raise Invalid('rank_rtol in [0,1e-6] required')
            U,values,Vh=torch.linalg.svd(A,full_matrices=True);sigma=torch.zeros((m,n),dtype=D)
            for i,v in enumerate(values):sigma[i,i]=v
            rank=int((values>cutoff*(values[0] if len(values) else 0)).sum());V=Vh.mH;kernel=V[:,rank:]@V[:,rank:].mH
            result={'u':encode(arr(U)),'singular_values':arr(values),'vh':encode(arr(Vh)),'sigma':encode(arr(sigma)),'reconstruction':encode(arr(U@sigma@Vh)),'numerical_rank':rank,'rank_relative_cutoff':cutoff,'right_numerical_kernel_projector':encode(arr(kernel)),'kernel_residual_max_absolute':torch.abs(A@kernel).max().item(),'kernel_is_exact':False,'gauge':'Full factors retain rectangular null directions; paired singular-vector phases/subspace bases are nonunique'}
            checks={'reconstruction':check(arr(U@sigma@Vh),a,tol),'left_unitary':check(arr(U.mH@U),arr(torch.eye(m,dtype=D)),tol),'right_unitary':check(arr(Vh@Vh.mH),arr(torch.eye(n,dtype=D)),tol)}
        else:raise Unsupported('decompose kinds: hermitian, svd; no general nonnormal eigendecomposition')
    elif task=='function':
        kind=q.get('kind')
        if kind=='polynomial':
            keys(q,('matrix','kind','coefficients','units'));a=matrix(q['matrix']);square(a)
            coeff=q['coefficients']
            if not isinstance(coeff,list) or not 1<=len(coeff)<=9:raise Invalid('1..9 coefficients in ascending degree order')
            coeff=[scalar(x) for x in coeff];A=T(a);n=len(a);eye=torch.eye(n,dtype=D);value=torch.zeros_like(A)
            for c in reversed(coeff):value=value@A+c*eye
            power=[[complex(i==j) for j in range(n)] for i in range(n)];ref=[[0j]*n for _ in range(n)]
            for c in coeff:
                ref=[[ref[i][j]+c*power[i][j] for j in range(n)] for i in range(n)];power=mm(power,a)
            checks['power_series_vs_horner']=check(arr(value),ref,tol)
        elif kind=='exp':
            keys(q,('matrix','kind','units'));a=matrix(q['matrix']);square(a);A=T(a);n=len(a)
            rho=max(sum(abs(z) for z in row) for row in a)
            if rho>1:raise Unsupported('Matrix exponential requires infinity norm <=1; explicitly rescale elsewhere, no silent replacement')
            value=torch.matrix_exp(A);term=[[complex(i==j) for j in range(n)] for i in range(n)];ref=[row[:] for row in term]
            for k in range(1,41):
                term=[[z/k for z in row] for row in mm(term,a)];ref=[[ref[i][j]+term[i][j] for j in range(n)] for i in range(n)]
            checks['scalar_taylor_order40']=check(arr(value),ref,tol)
            result['mathematical_infinity_norm_tail_bound']=rho**41/math.factorial(41)/(1-rho/42)
            result['tail_bound_excludes_roundoff']=True
        else:raise Unsupported('function kinds: polynomial, exp; no logarithm or square-root branch selection')
        if q['units']!='dimensionless':raise Unsupported('Function argument/coefficient profile requires dimensionless input; clarify physical conversion before execution')
        result.update(value=encode(arr(value)),shape=list(value.shape))
    elif task=='solve':
        keys(q,('matrix','rhs','max_condition'),('candidate',));a,b=matrix(q['matrix']),vector(q['rhs']);square(a)
        if len(a)!=len(b):raise Invalid('Solve dimensions differ')
        A,B=T(a),T(b);k,lo,hi=condition(A,q['max_condition']);solution=torch.linalg.solve(A,B)
        result={'solution':encode(arr(solution)),'condition_2':k,'smallest_singular_value':lo,'largest_singular_value':hi,'solver_backward_residual_2':torch.linalg.vector_norm(B-A@solution).item()}
        checks['solve_residual']=check(arr(A@solution),b,tol)
        if 'candidate' in q:
            candidate=vector(q['candidate'])
            if len(candidate)!=len(b):raise Invalid('Candidate dimensions differ')
            C=T(candidate);res=torch.linalg.vector_norm(B-A@C).item();bn=norm(b)
            result['candidate']={'residual_2':res,'relative_residual_2':res/bn if bn else None,'normwise_backward_error':res/(hi*norm(candidate)+bn) if hi*norm(candidate)+bn else 0.,'absolute_forward_error_bound_2':res/lo,'relative_forward_error_bound_2':k*res/bn if bn else None,'bound_note':'Exact-arithmetic conditioning inequality for declared A,b; floating residual/SVD are estimates, not interval certificates','observed_distance_to_computed_solution_2':torch.linalg.vector_norm(C-solution).item(),'residual_within_elementwise_budget':check(arr(A@C),b,tol)['passed'],'candidate_forward_accuracy_certified':False}
    elif task=='check':
        keys(q,('actual','reference'))
        a,b=q['actual'],q['reference']
        for item in (a,b):
            if not isinstance(item,dict) or set(item)!={'shape','dtype','device','values'}:raise Invalid('Check arrays require shape,dtype,device,flattened values')
        if any(a[k]!=b[k] for k in ('shape','dtype','device')):raise Invalid('Exact shape/dtype/device equality required before arithmetic; no broadcasting or casts')
        if a['dtype']!='complex128' or a['device']!='cpu':raise Unsupported('Check profile supports declared CPU complex128 values only')
        shape=a['shape']
        if not isinstance(shape,list) or len(shape)>2 or any(type(d) is not int or not 1<=d<=8 for d in shape):raise Invalid('Shape must have 0..2 axes, each 1..8')
        values=[]
        for item in (a,b):
            if not isinstance(item['values'],list) or len(item['values'])!=math.prod(shape):raise Invalid('Flattened value count does not equal explicit shape')
            values.append([scalar(z) for z in item['values']])
        decision=check(*values,tol);result={'comparison':decision,'phase_alignment':False,'reference_side':'reference','shape':shape}
        return {'status':'within_tolerance' if decision['passed'] else 'outside_tolerance','result':result,'checks':{},'tolerance':tol,'versions':{'torch':tv},'quantum_execution':False}
    else:raise Unsupported('Tasks: algebra,basis,classify,decompose,function,solve,check; no symbolic proof or quantum execution')
    status='verified' if all(c['passed'] for c in checks.values()) else 'verification_failed'
    return {'status':status,'task':task,'result':result,'checks':checks,'tolerance':tol,'versions':{'torch':tv},'execution':{'device':'cpu','dtype':'complex128','classical_tensor_only':True},'quantum_execution':False,'claim_acceptance':'Not inferred from internal verification'}
def reject(x):raise Invalid('Nonstandard JSON constant '+x)
def unique(pairs):
    q={}
    for k,v in pairs:
        if k in q:raise Invalid('Duplicate key '+k)
        q[k]=v
    return q
def main():
    runtime={'implementation':sys.implementation.name,'python':'.'.join(map(str,sys.version_info[:3]))}
    if sys.implementation.name!='cpython' or sys.version_info[:2]!=(3,12):out={'status':'unsupported','reason':'CPython 3.12 required'}
    else:
        try:
            q=json.load(sys.stdin,parse_constant=reject,object_pairs_hook=unique);out=main_run(q)
        except Unsupported as e:out={'status':'unsupported','reason':str(e)}
        except (Invalid,ValueError,OverflowError,RecursionError) as e:out={'status':'invalid_input','reason':str(e)}
        except Exception as e:out={'status':'execution_failed','reason':type(e).__name__+': '+str(e)}
    out.update(contract_version=VERSION,runtime=runtime)
    try:print(json.dumps(out,allow_nan=False,sort_keys=True))
    except ValueError:out={'status':'execution_failed','reason':'Nonfinite output serialization','runtime':runtime,'contract_version':VERSION};print(json.dumps(out))
    return {'verified':0,'within_tolerance':0,'verification_failed':1,'outside_tolerance':1,'invalid_input':2,'unsupported':3,'execution_failed':4}[out['status']]
if __name__=='__main__':sys.exit(main())
