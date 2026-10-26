"""Fresh14.4data plus all-basis structured-path equivalence and interface boundaries."""
import itertools,json,torch,flagquantum as fq
from dataclasses import replace
from examples.foundations import oracle_access as q,statistical_ensembles as e,uniform_reversible as u
rows=[];explicit=0;gray=(0,1,3,2)
for mode in ('statevector','density_matrix'):
 for i,y in itertools.product(range(4),repeat=2):
  c=fq.Circuit(4,dtype=e.D)
  for j,bit in enumerate(u.bits(i,2)+u.bits(y,2)):
   if bit:c.X(j)
  c.CX(0,2).CX(1,3).CX(0,3)
  r=fq.run(c,outputs=[fq.density_matrix(name='rho'),fq.probabilities(name='p')],options=replace(e.OPTIONS,mode=mode));explicit+=1
  v=torch.zeros(16,dtype=e.D);v[(i<<2)|(y^gray[i])]=1
  e.close(r.measurement('rho').value[0],torch.outer(v,v.conj()));e.close(r.measurement('p').value[0],v.abs().square())
  if mode=='statevector':e.close(r.statevector()[0],v)
 new=(3,1,2,0)
 for i,y in itertools.product((0,3),(0,2)):
  q.execute(new,2,2,i,y,mode=mode);rows.append(dict(table=new,address=i,target=y,mode=mode,expected_value=y^new[i]))
 q.execute(new,2,2,coherent=True,mode=mode)
 q.amplitude((1,3,2,0),mode=mode)
 q.execute((0,0),1,1,mode=mode)
 r0=q.phase((0,0,0,0),2,mode=mode);r1=q.phase((1,1,1,1),2,mode=mode)
 e.close(r0.measurement('rho').value[0],r1.measurement('rho').value[0])
 if mode=='statevector':e.close(r0.statevector()[0],-r1.statevector()[0])
assert explicit==32 and q.RUNS==18
print(json.dumps(dict(native_runs=50,structured_gray_basis_runs=32,fresh_lookup_basis_runs=8,fresh_lookup_complex_runs=2,fresh_amplitude_runs=2,zero_oracle_identity_runs=2,constant_phase_runs=4,cases=rows),indent=2))
