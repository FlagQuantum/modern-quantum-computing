import torch
from examples.foundations import basis_measurement as a,conditional_states as c
b=a.b;v=torch.tensor([.6,.8j],dtype=b.D)
cases=0
for theta,phi in ((.71,.43),(-.29,.81),(1.21,-.4)):
 B=a.tilted(theta,phi);P=a.basis_family(B,('zero','one'));p,states=c.branches(v,P,('zero','one'));eta=B.mH@v
 for j in (0,1):
  w=torch.zeros(2,dtype=b.D);w[j]=eta[j]/torch.sqrt(p[j])
  torch.testing.assert_close(B@w,states[j],rtol=0,atol=b.ATOL)
  torch.testing.assert_close(w.norm(),torch.ones((),dtype=torch.float64),rtol=0,atol=b.ATOL)
  cases+=1
print('6 classical selected-branch phase/restoration checks passed; zero additional FlagQuantum circuits.')
