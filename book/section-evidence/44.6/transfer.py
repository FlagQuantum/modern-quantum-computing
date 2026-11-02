import sys,json,math,torch
sys.path.insert(0,'/Users/baai/Documents/liuwei/modern-quantum-computing')
try:from examples.foundations import precision_drift as n
except ImportError:
 sys.path.insert(0,'/private/tmp');import precision_drift as n
for L in (19,113,311):
 for dtype in(torch.complex64,torch.complex128):
  w,v,m=n.native(L,-.029,.017,dtype)
  assert n.norm(n.normalize(w).to(torch.complex128)-v)<=2*m['error']+1e-12
p=1e-16
v=torch.tensor([math.sqrt(1-p),math.sqrt(p),0,0],dtype=torch.complex128)
w=torch.tensor([math.sqrt(1-p),0,math.sqrt(p),0],dtype=torch.complex128)
mask=torch.tensor([0,1,1,0],dtype=torch.complex128)
assert n.norm(w-v)<2e-8 and n.norm(n.normalize(w*mask)-n.normalize(v*mask))>1.4
plus=torch.tensor([1,1],dtype=torch.complex128)/math.sqrt(2);phase=torch.tensor([1,1j],dtype=torch.complex128)/math.sqrt(2)
X=torch.tensor([[0,1],[1,0]],dtype=torch.complex128);Y=torch.tensor([[0,-1j],[1j,0]],dtype=torch.complex128)
assert torch.equal(plus.abs().square(),phase.abs().square())
assert abs(torch.vdot(phase,X@phase))<1e-15 and abs(torch.vdot(phase,Y@phase)-1)<1e-15
assert n.RUNS==6
json.dump(n.RECEIPTS,open('/private/tmp/446-transfer-receipts.json','w'),indent=2)
print('6 fresh native calls passed: new depths and signed parameters, both CPU precisions.')
print('New p=1e-16 conditional and quarter-turn relative-phase checks passed; no native calls for these fixtures.')
