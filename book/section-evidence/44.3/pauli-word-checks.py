from pathlib import Path
import sys,itertools,torch
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from examples.foundations import measurement_execution as m
matrices={'I':torch.eye(2,dtype=m.D),'X':m.X,'Y':m.Y,'Z':m.Z};count=0
for n in range(1,4):
 N=1<<n;v=torch.tensor([complex(j+1,N-j)/N for j in range(N)],dtype=m.D);v=v/torch.linalg.vector_norm(v)
 for word in itertools.product('IXYZ',repeat=n):
  A=matrices[word[0]]
  for c in word[1:]:A=torch.kron(A.contiguous(),matrices[c])
  m.e.close(torch.tensor(m.pauli(v,n,''.join(word)),dtype=torch.float64),torch.vdot(v,A@v).real);count+=1
assert count==84 and m.RUNS==0
print('84 zero-native scalar checks: every Pauli word through three qubits,including multipleY phases,matches dense Kronecker expectations.')
