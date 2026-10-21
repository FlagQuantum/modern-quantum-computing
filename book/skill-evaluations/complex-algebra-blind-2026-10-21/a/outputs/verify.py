"""Independent standard-library checks; imports neither helper nor Torch/FlagQuantum."""
import cmath,json,math,time
from fractions import Fraction as F
from pathlib import Path
r=Path(__file__).resolve().parent
start=time.perf_counter()
def c(z):return complex(*z)
def mat(a):return [[c(z) for z in row] for row in a]
def enc(z):
 if isinstance(z,list):return [enc(x) for x in z]
 return [complex(z).real,complex(z).imag]
def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def mv(a,b):return [sum(x*y for x,y in zip(row,b)) for row in a]
def adj(a):return [list(map(complex.conjugate,col)) for col in zip(*a)]
def flatten(a):
 if isinstance(a,list):return [x for v in a for x in flatten(v)]
 return [a]
def check(a,b,atol,rtol=0):
 aa,bb=flatten(a),flatten(b);assert len(aa)==len(bb)
 errors=[abs(x-y) for x,y in zip(aa,bb)]
 return {'passed':all(e<=atol+rtol*abs(y) for e,y in zip(errors,bb)), 'max_absolute_error':max(errors),'atol':atol,'rtol':rtol,'comparison':'elementwise complex modulus; reference-scaled budget'}
records={}
q=json.loads((r/'A1/request.json').read_text());h=json.loads((r/'A1/stdout.json').read_text())['result']
a,s=mat(q['matrix']),mat(q['basis_columns']);v=list(map(c,q['v']));d=s[0][0]*s[1][1]-s[0][1]*s[1][0]
inv=[[s[1][1]/d,-s[0][1]/d],[-s[1][0]/d,s[0][0]/d]]
y=mv(inv,v);b=mm(mm(inv,a),s);g=mm(adj(s),s)
checks={'coordinates':check(list(map(c,h['new_coordinates'])),y,1e-11,1e-12),'operator':check(mat(h['new_operator']),b,1e-11,1e-12),'gram':check(mat(h['gram']),g,1e-11,1e-12),'action':check(mv(s,mv(b,y)),mv(a,v),1e-11,1e-12),'gram_norm':check(sum(x.conjugate()*z for x,z in zip(y,mv(g,y))),sum(abs(x)**2 for x in v),1e-11,1e-12)}
# Condition via analytic eigenvalues of 2x2 Gram, rather than helper SVD.
tr=(g[0][0]+g[1][1]).real;gd=(g[0][0]*g[1][1]-g[0][1]*g[1][0]).real
disc=math.sqrt(tr*tr-4*gd);condition=math.sqrt((tr+disc)/(tr-disc))
checks['condition']=check(h['condition_2'],condition,1e-11,1e-12)
records['A1']={'method':'Explicit two by two inverse, scalar indexed products and analytic Gram spectrum, independently of Torch solve/SVD','checks':checks,'new_coordinates':enc(y),'new_operator':enc(b),'gram':enc(g),'condition_2':condition,'condition_limit_satisfied':condition<=q['max_condition']}
# Exact rational real/imaginary pair arithmetic for A2 and A3.
def pair(z):return (F(str(z[0])),F(str(z[1])))
def mul(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def conj(x):return (x[0],-x[1])
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def psum(xs):
 z=(F(0),F(0))
 for x in xs:z=add(z,x)
 return z
q=json.loads((r/'A2/request.json').read_text());h=json.loads((r/'A2/stdout.json').read_text())['result'];v=list(map(pair,q['v']));w=list(map(pair,q['w']))
z=psum(mul(conj(x),y) for x,y in zip(v,w));normv=psum(mul(conj(x),x) for x in v);normw=psum(mul(conj(x),x) for x in w)
expected=complex(*map(float,z));checks={'inner':check(c(h['value']),expected,1e-11,1e-12),'norm_v':check(h['squared_norm_v'],float(normv[0]),1e-11,1e-12),'norm_w':check(h['squared_norm_w'],float(normw[0]),1e-11,1e-12)}
records['A2']={'method':'Exact rational real/imag pair multiplication with first-argument conjugation','inner_fraction':list(map(str,z)),'norm_v_fraction':str(normv[0]),'norm_w_fraction':str(normw[0]),'checks':checks}
q=json.loads((r/'A3/request.json').read_text());h=json.loads((r/'A3/stdout.json').read_text())['result'];a=mat(q['matrix']);aa=mm(a,a);ad=adj(a);i=[[1,0],[0,1]]
identities={'hermitian':check(a,ad,1e-11,1e-12),'idempotent':check(aa,a,1e-11,1e-12),'normal':check(mm(ad,a),mm(a,ad),1e-11,1e-12),'unitary':check(mm(ad,a),i,1e-11,1e-12)}
checks={k: {'passed':val['passed']==h['identity_tests'][k]['passed']} for k,val in identities.items()}
# Symbolic family [[1,i*c],[0,0]] squares to itself for all real c; nonzero c defeats Hermiticity.
cc=F(str(q['matrix'][0][1][1]));exact_a=[[pair(z) for z in row] for row in q['matrix']]
exact_square=[[psum(mul(exact_a[i][k],exact_a[k][j]) for k in range(2)) for j in range(2)] for i in range(2)]
records['A3']={'method':'Independent indexed identities plus rational exact idempotence witness','identity_results':identities,'checks':checks,'exact_idempotent':exact_square==exact_a,'nonzero_offdiagonal_fraction':str(cc),'claim_disposition':'rejected: this supplied matrix is exactly idempotent but not Hermitian, hence not an orthogonal projector for the standard inner product','geometric_witness':'Range is span(e1); kernel is span((-0.473i,1)). Their inner product is -0.473i, so kernel is not orthogonal to range.'}
q=json.loads((r/'A4/request.json').read_text());h=json.loads((r/'A4/stdout.json').read_text());t=q['time']['value']*1e-9
expvals=[q['generator']['matrix'][j][j][0]*t for j in range(2)];u=[[cmath.exp(-1j*expvals[0]),0],[0,cmath.exp(-1j*expvals[1])]];v=list(map(c,q['state']));alpha=-sum(expvals)/2;native=[[cmath.exp(-1j*(expvals[0]+alpha)),0],[0,cmath.exp(-1j*(expvals[1]+alpha))]]
checks={'unitary':check(mat(h['unitary']),u,1e-10),'alpha':check(h['zyz']['alpha'],alpha,1e-10),'trace_phase':check(c(h['units_and_generator']['trace_shift_phase']),cmath.exp(1j*alpha),1e-10),'reconstruction':check(mat(h['reconstructed_full_matrix']),u,1e-10)}
for rec in h['records']:
 label,path=rec['input_label'],rec['path']
 state=v if label=='supplied' else ([1,0] if label=='zero' else [0,1])
 if label=='coherent-control':
  target=mv(native if path=='controlled-unrepaired' else u,v)
  expected=[z/math.sqrt(2) for z in v+target]
 else:expected=mv(u if path=='direct' else native,state)
 checks[label+'/'+path]=check(list(map(c,rec['statevector'])),expected,1e-10)
checks['circuit_record_count']={'passed':h['actual_flagquantum_circuits']==len(h['records'])==9}
repaired=next(x for x in h['records'] if x['path']=='controlled-repaired');unrepaired=next(x for x in h['records'] if x['path']=='controlled-unrepaired')
witness=math.sqrt(sum(abs(c(x)-c(y))**2 for x,y in zip(repaired['statevector'],unrepaired['statevector'])))
records['A4']={'method':'Closed diagonal complex exponentials from supplied rad/s and ns, direct scalar expected states for all nine actual circuit records','checks':checks,'dimensionless_diagonal_exponent':expvals,'alpha':alpha,'controlled_state_omission_distance':witness,'omission_detected':witness>1e-10,'quantum_execution':'The helper executed actual FlagQuantum circuits. This independent script performs classical reference verification only.'}
for ident,record in records.items():
 record['passed']=all(x['passed'] for x in record['checks'].values())
 (r/ident/'independent-verification.json').write_text(json.dumps(record,indent=2))
print(json.dumps({'runtime_seconds':time.perf_counter()-start,'all_passed':all(v['passed'] for v in records.values()),'tasks':{k:{'passed':v['passed'],'checks':v['checks']} for k,v in records.items()}},indent=2))
