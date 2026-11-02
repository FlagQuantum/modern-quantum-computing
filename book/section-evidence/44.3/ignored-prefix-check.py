from pathlib import Path
import sys,math,torch
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from examples.foundations import measurement_execution as m
plus=torch.tensor([1,1],dtype=m.D)/math.sqrt(2)
value=sum(p*m.expectation(w,m.X,1,(0,))for bit in(0,1)for p,w in[m.branch(plus,1,(0,),(bit,))])
m.e.close(value,torch.tensor(0.,dtype=torch.float64));m.e.close(m.expectation(plus,m.X,1,(0,)),torch.tensor(1.,dtype=torch.float64))
_,v=m.preparation(3,(math.pi/2,math.pi/2,math.pi/3,math.pi/2))
weighted=sum(p*m.probabilities(w,3,(0,))for bit in(0,1)for p,w in[m.branch(v,3,(2,0),(bit,))])
m.e.close(weighted,m.probabilities(v,3,(0,)));assert m.RUNS==0
print('Zero native calls: fixed-basis marginal obeys total probability; ignored actual Z measurement on plus changes later X expectation from1 to0 under ideal branch semantics.')
