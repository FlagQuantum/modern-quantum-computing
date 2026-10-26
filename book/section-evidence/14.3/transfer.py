"""Fresh14.3C graph accounting and explicit smaller native implementation."""
import json,itertools,math,torch,flagquantum as fq
from dataclasses import replace
from examples.foundations import bounded_error as b,uniform_reversible as u,statistical_ensembles as e
nodes=(('AND',(0,1)),('AND',(0,2)),('AND',(1,2)),('XOR',(4,5)),('XOR',(7,6)),('XOR',(8,3)))
net,cost=u.translate(4,nodes,(9,));assert cost['qubits']==11 and cost['network_gates']==19
for z in itertools.product((0,1),repeat=4):assert u.evaluate(z,nodes,(9,))[0]==(int(sum(z[:3])>=2)^z[3],)
rows=[];explicit=0
for mode in ('statevector','density_matrix'):
 for x in ('101','010'):
  data=b.word(x);c=fq.Circuit(5,dtype=e.D)
  for j,v in enumerate(data):
   if v:c.X(j)
  c.H(3).CCX(0,1,4).CCX(0,2,4).CCX(1,2,4).CX(3,4)
  r=fq.run(c,outputs=[fq.density_matrix(name='rho'),fq.probabilities(qubits=(4,),name='answer')],options=replace(e.OPTIONS,mode=mode));explicit+=1
  target=torch.zeros(32,dtype=e.D)
  for coin in (0,1):target[u.index(data+(coin,int(sum(data)>=2)^coin))]=1/math.sqrt(2)
  e.close(r.measurement('rho').value[0],torch.outer(target,target.conj()))
  e.close(r.measurement('answer').value[0],torch.tensor([.5,.5],dtype=torch.float64))
  if mode=='statevector':e.close(r.statevector()[0],target)
  rows.append(dict(word=x,mode=mode,probability='1/2',class_contract=False))
 for x in ('110','111'):
  for comp in (False,True):
   _,p,cost2=b.execute(x,complement=comp,mode=mode)
   assert b.contract(p,(sum(b.word(x))%2)^int(comp))
   rows.append(dict(word=x,mode=mode,complement=comp,probability=str(p)))
assert explicit==4 and b.RUNS==8
print(json.dumps(dict(native_runs=12,graph_host_truth_cases=16,graph_qubits=11,graph_network_gates=19,native_equivalent_qubits=5,cases=rows),indent=2))
