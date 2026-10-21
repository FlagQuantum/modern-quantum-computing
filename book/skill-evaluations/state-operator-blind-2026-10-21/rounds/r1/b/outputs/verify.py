import json,math,pathlib
O=pathlib.Path(__file__).resolve().parent
checks={}
for tid in ['B1','B2']:
 r=json.loads((O/(tid+'.request.json')).read_text()); actual=json.loads((O/(tid+'.stdout.json')).read_text())
 a=[[complex(*v) for v in row] for row in r['a']]; b=[[complex(*v) for v in row] for row in r['b']]
 n=len(a)
 unitary_errors=[]
 for m in (a,b):
  unitary_errors.append(max(abs(sum(m[k][i].conjugate()*m[k][j] for k in range(n))-(i==j)) for i in range(n) for j in range(n)))
 assert max(unitary_errors)<1e-12
 if tid=='B1':
  # Construct full extensions without first aligning targets.
  a=[[complex(i==j) if i<2 and j<2 else a[i-2][j-2] if i>=2 and j>=2 else 0j for j in range(4)] for i in range(4)]
  b=[[complex(i==j) if i<2 and j<2 else b[i-2][j-2] if i>=2 and j>=2 else 0j for j in range(4)] for i in range(4)]
  witness=[1/math.sqrt(2),0,1/math.sqrt(2),0]
 else: witness=[1/math.sqrt(2),1/math.sqrt(2)]
 overlap=sum(x.conjugate()*y for ar,br in zip(a,b) for x,y in zip(ar,br))
 sqnorm=sum(abs(x)**2+abs(y)**2 for ar,br in zip(a,b) for x,y in zip(ar,br))
 residual=math.sqrt(max(0,sqnorm-2*abs(overlap)))
 assert math.isclose(residual,actual['decision_residual'],abs_tol=1e-14)
 assert residual>r['atol'] and actual['status']=='outside_tolerance'
 u=[sum(x*y for x,y in zip(row,witness)) for row in a]; v=[sum(x*y for x,y in zip(row,witness)) for row in b]
 fidelity=abs(sum(x.conjugate()*y for x,y in zip(u,v)))**2
 assert fidelity<1-1e-10
 checks[tid]={'passed':True,'independent_trace_identity_residual':residual,'unitarity_entrywise_errors':unitary_errors,'coherent_input':[[complex(x).real,complex(x).imag] for x in witness],'output_ray_fidelity':fidelity,'helper_exit_code':json.loads((O/(tid+'.execution.json')).read_text())['exit_code']}
r=json.loads((O/'B3.stdout.json').read_text())
assert r['observed_proportion']==47/125
# Equivalent binomial variance computation using integer counts.
assert math.isclose(r['plug_in_standard_error'], math.sqrt(47*78/125**3),abs_tol=1e-16)
checks['B3']={'passed':True,'observed_proportion':r['observed_proportion'],'plug_in_standard_error':r['plug_in_standard_error']}
print(json.dumps(checks,indent=2))
