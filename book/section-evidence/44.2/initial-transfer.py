"""Fresh44.2 changed local matrices/supports; eight actual native calls."""
from pathlib import Path
import sys,cmath,math,json
ROOT=Path('/Users/baai/Documents/liuwei/modern-quantum-computing');sys.path.insert(0,str(ROOT));sys.path.insert(0,'/private/tmp')
try:from examples.foundations import tensor_gate_executor as o
except ImportError:import tensor_gate_executor as o
import torch,flagquantum as fq
from dataclasses import replace
rows=[];direct=0
for S in((4,1),(1,4),(3,0,4)):
 d=1<<len(S);U=torch.diag(torch.tensor([cmath.exp(.11j*a)for a in range(d)],dtype=o.D))@o.fourier(len(S))
 theta=-.58;V=torch.tensor([[math.cos(theta/2),-1j*math.sin(theta/2)],[-1j*math.sin(theta/2),math.cos(theta/2)]],dtype=o.D)
 gates=[(S,U),((2,),V),(S,U.mH)]
 for mode in('statevector','density_matrix'):
  c,v=o.preparation(5);target=v.clone()
  for T,A in gates:o.matrix(A,len(T),True);target=o.check(target,A,5,T);c.unitary(*T,unitary=A.contiguous())
  o.e.close(target,o.execute(v,gates,5))
  r=fq.run(c,outputs=[fq.probabilities(name='p'),fq.density_matrix(name='rho')],options=replace(o.e.OPTIONS,mode=mode));direct+=1
  o.e.close(r.measurement('p').value[0],abs(target)**2);o.e.close(r.measurement('rho').value[0],target[:,None]*target.conj()[None,:])
  if mode=='statevector':o.e.close(r.statevector()[0],target)
  rows.append(dict(support=S,mode=mode,theta=theta,row_phase_increment=.11,probability_max_residual=float((r.measurement('p').value[0]-abs(target)**2).abs().max())))
for mode in('statevector','density_matrix'):o.native(5,(4,3,2,1,0),mode,prefix=1)
v=torch.tensor([complex((i%7)-3,(3*i)%11-5)/13 for i in range(16)],dtype=o.D);M=o.fourier(2).clone();M[1]*=1.7;o.check(v,M,4,(3,0))
CX=torch.tensor([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=o.D);v=torch.zeros(8,dtype=o.D);v[1]=1/math.sqrt(2);v[6]=1j/math.sqrt(2)
a=o.apply(v,CX,3,(2,0));bad=o.apply(v,CX,3,(0,2));expected=torch.zeros_like(v);expected[5]=1/math.sqrt(2);expected[6]=1j/math.sqrt(2);o.e.close(a,expected)
expected2=torch.zeros_like(v);expected2[1]=1/math.sqrt(2);expected2[7]=1j/math.sqrt(2);o.e.close(bad,expected2);assert abs(torch.vdot(a,bad))<1e-12
R=torch.eye(4,dtype=o.D)[[0,2,1,3],:];o.e.close(o.entry_matrix(R@M@R.mH,4,(0,3)),o.entry_matrix(M,4,(3,0)))
assert direct+o.RUNS==8
print('Eight fresh native calls passed: three changed five-qubit chains,both modes,and two full reversed-support Fourier prefixes.')
print('Fresh nonunitary/arbitrary-vector,complex controlled-X exercise and support-covariance references passed classically; no phase alignment or normalization repair.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(dict(changed_chains=rows,prefixes=o.RECEIPTS),indent=2)+'\n')
