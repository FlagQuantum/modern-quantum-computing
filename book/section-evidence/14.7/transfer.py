from pathlib import Path
import sys,math,json
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from examples.foundations import interaction_patterns as h
packets=[]
for mode in ('statevector','density_matrix'):
 for j,(theta,phi)in enumerate(((-.6,.4),(.37,-.8),(1.3,.9))):
  for basis in ('X','Y','Z'):
   task=h.Task(f'transfer-{mode}-{j}-{basis}',3,theta,phi,basis,shots=43)
   p,d=h.run_task(task,mode);packets.append(p)
   assert abs(d['scalar_mu']-d['native_mu'])<=1e-12
 _,k=h.kernel(-.2,.9,mode);assert abs(k-math.cos(-1.1/2)**2)<1e-12
 branches,ignored,_=h.feedback(.9,-.3,mode)
 assert abs(sum(p for p,_ in branches)-1)<1e-12
 exact,sampled=h.reconstruct(-.5,.9,mode);assert abs(exact-math.cos(.4))<1e-12
 v=-.6
 for row in h.embedding(.3,v,2,'exact-simulator',mode):
  v=.3*v/math.sqrt(1+(.3*v)**2);assert abs(row['new_v']-v)<1e-12
accepted=set()
for p in reversed(packets):h.accept_once(p,p.task,accepted)
assert len(accepted)==18 and h.RUNS==38
# Subnormal branch probability remains positive;phase normalization uses magnitude,not its rounded square.
p,phase=h.branch_phase(1e-160);assert p>0 and phase==1
assert h.invalid_checks()==18
print(json.dumps({'native_runs':38,'basis_cases':18,'kernel_calls':2,'feedback_reference_calls':4,'reconstruction_calls':10,'environment_calls':4,'source':'CPU simulator,complex128,both modes','out_of_order_packets':18,'pure_subnormal_phase_check':'passed;no additional circuit','malformed_contracts':18},indent=2))
