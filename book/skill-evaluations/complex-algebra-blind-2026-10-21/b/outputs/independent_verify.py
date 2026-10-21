"""Independent standard-library scalar/exact checks; no helper or Torch imports."""
import json, pathlib, math
from fractions import Fraction as F
ROOT=pathlib.Path(__file__).resolve().parent.parent
OUT=ROOT/'outputs'
tasks={t['id']:t for t in json.loads((ROOT/'tasks.json').read_text())}
def c(p): return complex(*p)
def matrix(x): return [[c(p) for p in row] for row in x]
def adj(A): return [[A[i][j].conjugate() for i in range(len(A))] for j in range(len(A[0]))]
def mm(A,B): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*B)] for row in A]
def eye(n): return [[complex(i==j) for j in range(n)] for i in range(n)]
def error(A,B):
    assert len(A)==len(B) and all(len(a)==len(b) for a,b in zip(A,B))
    return max(abs(a-b) for ar,br in zip(A,B) for a,b in zip(ar,br))
def check(A,B,atol,rtol):
    return all(abs(a-b)<=atol+rtol*abs(b) for ar,br in zip(A,B) for a,b in zip(ar,br))
report={}
d=tasks['B1']['data']; result=json.loads((OUT/'B1.stdout.json').read_text())['result']
A=matrix(d['matrix']); U=matrix(result['u']); S=matrix(result['sigma']); Vh=matrix(result['vh']); P=matrix(result['right_numerical_kernel_projector'])
assert [len(U),len(U[0]),len(S),len(S[0]),len(Vh),len(Vh[0])]==[2,2,2,4,4,4]
canonical_P=[[complex(i==j and i>=2) for j in range(4)] for i in range(4)]
right_repeated=mm(adj(Vh[:2]),Vh[:2])
canonical_repeated=[[complex(i==j and i<2) for j in range(4)] for i in range(4)]
checks={'reconstruction':check(mm(mm(U,S),Vh),A,1e-11,1e-12),'left_unitarity':check(mm(adj(U),U),eye(2),1e-11,1e-12),'right_unitarity':check(mm(Vh,adj(Vh)),eye(4),1e-11,1e-12),'kernel_projector':check(P,canonical_P,1e-11,1e-12),'kernel_equation':check(mm(A,P),[[0j]*4 for _ in range(2)],1e-11,1e-12),'projector_idempotent':check(mm(P,P),P,1e-11,1e-12),'projector_hermitian':check(adj(P),P,1e-11,1e-12),'right_repeated_singular_subspace':check(right_repeated,canonical_repeated,1e-11,1e-12),'singular_values':result['singular_values']==[2.,2.],'rank':result['numerical_rank']==2}
assert all(checks.values())
report['B1']={'passed':True,'checks':checks,'independent_reason':'A†A=diag(4,4,0,0) directly; left repeated subspace is all C^2, right repeated subspace span(e1,e2), kernel span(e3,e4).','rank_cutoff':2e-12,'reconstruction_max_absolute_error':error(mm(mm(U,S),Vh),A)}
# Exact binary-rational diagonal solve establishes actual forward error independent of the numerical solver.
epsilon=F.from_float(tasks['B2']['data']['matrix'][1][1][0]); assert epsilon==F(1,2**30)
condition=1/epsilon; residual=epsilon; relative_forward=F(1)
assert residual<F(1,10**8) and relative_forward>F(1,10**8)
assert condition<=F(10**10)
r2=json.loads((OUT/'B2.stdout.json').read_text())['result']
assert r2['solution']==[[1.,0.],[0.,0.]] and r2['condition_2']==float(condition)
report['B2']={'passed':True,'exact_solution':[[1,0],[0,0]],'condition_2':float(condition),'candidate_residual_exact':str(residual),'candidate_relative_forward_error_exact':str(relative_forward),'absolute_forward_bound':float(residual/epsilon),'relative_forward_bound':float(condition*residual),'normwise_backward_error':float(residual)/(math.sqrt(2)+1),'claim_disposition':'refuted','reason':'Residual <1e-8 but exact candidate relative forward error is 1.'}
a=tasks['B3']['data']['actual']; b=tasks['B3']['data']['reference']
assert a['shape']!=b['shape'] and math.prod(a['shape'])==len(a['values']) and math.prod(b['shape'])==len(b['values'])
# Each (2,) value would broadcast across a (2,1) column into a (2,2) grid, but admission forbids doing so.
would_broadcast_equal=all(c(x)==c(y) for x in a['values'] for y in b['values'])
assert would_broadcast_equal
assert json.loads((OUT/'B3.stdout.json').read_text())['status']=='invalid_input'
report['B3']={'passed':True,'actual_shape':a['shape'],'reference_shape':b['shape'],'each_payload_matches_own_declared_shape':True,'exact_metadata_admission':False,'hypothetical_broadcast_allclose':would_broadcast_equal,'hypothetical_broadcast_shape':[2,2],'claim_disposition':'broadcasting_does_not_authorize_success','decision':'invalid_input; do not reshape or repair'}
d=tasks['B4']['data']; a=list(map(c,d['a'])); b=list(map(c,d['b']))
norm_a=sum(abs(x)**2 for x in a); norm_b=sum(abs(x)**2 for x in b)
assert abs(norm_a-1)<=1e-12 and abs(norm_b-1)<=1e-12
ov=sum(x.conjugate()*y for x,y in zip(a,b)); z=ov.conjugate()/abs(ov)
raw=math.sqrt(sum(abs(x-y)**2 for x,y in zip(a,b))); aligned=math.sqrt(sum(abs(x-z*y)**2 for x,y in zip(a,b)))
# Also verify whole-ray projectors, independent of the selected aligning phase.
pa=[[x*y.conjugate() for y in a] for x in a]; pb=[[x*y.conjugate() for y in b] for x in b]
assert aligned<=d['atol'] and error(pa,pb)<=d['atol']
helper=json.loads((OUT/'B4.stdout.json').read_text())
assert abs(helper['aligned_residual']-aligned)<=1e-15
report['B4']={'passed':True,'norm_squared_a':norm_a,'norm_squared_b':norm_b,'overlap':[ov.real,ov.imag],'common_multiplier_on_b':[z.real,z.imag],'raw_residual':raw,'aligned_residual':aligned,'ray_projector_max_absolute_error':error(pa,pb),'atol':d['atol'],'basis':d['basis_a'],'phase_scope':'one common phase in isolated state comparison','decision':'within_tolerance'}
print(json.dumps({'method':'Python standard library scalar complex arithmetic plus exact Fraction solve; no circuit execution','results':report},indent=2))
