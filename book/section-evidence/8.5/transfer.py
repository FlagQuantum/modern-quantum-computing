"""Fresh8.5B-D author transfer cases;not independent review."""
import json,math,sys
from pathlib import Path
import torch
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from examples.foundations import reduced_spectra as g
from examples.foundations import statistical_ensembles as e
from examples.foundations import partial_trace as t
# B:two modes,two rotations per mode=4native circuits.
for mode in ('statevector','density_matrix'):
 before,C0,data0=g.pair(1.17,.62,mode=mode)
 result,C,data=g.pair(1.17,.62,-.53,.91,mode)
 for name in ('A0','B0'):
  e.close(torch.linalg.eigvalsh(before.measurement(name).value[0]),torch.linalg.eigvalsh(result.measurement(name).value[0]))
 e.close(torch.trace(result.measurement('A0').value[0]@result.measurement('A0').value[0]),math.cos(1.17/2)**4+math.sin(1.17/2)**4)
 expectedY=math.cos(1.17)*math.sin(.91)*math.sin(-.47)
 e.close(result.expectation('y_last')[0],expectedY)
 e.close(torch.trace(C.mH@C@e.Y),-expectedY)
 assert abs(expectedY)>.1
# C:two four-qubit modes+two three-qubit modes+two biased pairs=6native circuits.
for mode in ('statevector','density_matrix'):
 c,v=t.preparation(4,-.67,.39)
 result,data=g.query(c,v,(((3,1),(0,2)),((1,3),(2,0))),mode)
 e.close(data[0][1],data[1][1])
 result,data=g.rectangular(1.23,-.64,mode)
 assert len(data[1][3])==2 and len(data[1][4])==4
 result,C,data=g.pair(.93,-.72,mode=mode)
 e.close(data[1].pow(4).sum(),math.cos(.93/2)**4+math.sin(.93/2)**4)
# D:one pure pair and two native product components=3native circuits.
p=.68;phi=-.57
pure,C,data=g.pair(2*math.acos(math.sqrt(p)),phi)
a=g.basis((0,0));b=g.basis((1,1))
mixed=p*a.measurement('full').value[0]+(1-p)*b.measurement('full').value[0]
for name,kept in (('A0',(0,)),('B0',(1,))):
 e.close(pure.measurement(name).value[0],t.indexed(mixed,2,kept))
e.close(torch.trace(mixed@mixed),p*p+(1-p)**2)
e.close(pure.expectation('xy')[0],2*math.sqrt(p*(1-p))*math.sin(phi))
e.close(torch.trace(mixed@torch.kron(e.X,e.Y)),0)
for weights in ((.5,.5,0.),(2/3,1/6,1/6)):
 C3=torch.diag(torch.tensor(weights,dtype=g.D).sqrt())
 data3=g.inspect_reductions(C3,C3@C3.mH,C3.T@C3.conj());e.close(data3[1].pow(4).sum(),.5)
# Additional fresh degenerate complex pair checks conjugate mixing=1native circuit.
deg,C,data=g.pair(math.pi/2,-.83,-.41,.67)
U,s,B=data[:3];W=e.prepare(e.qubit(-.92,.56))
e.close((U@W*s)@(B@W.conj()).T,C)
e.close((U@W*s.square())@(U@W).mH,deg.measurement('A0').value[0])
assert g.RUNS==14
print(json.dumps(dict(native_circuits=g.RUNS,printed_exercises=['8.5B','8.5C','8.5D'],mixed_purity=p*p+(1-p)**2,retained_small_weight='native complete/body epsilon1e-10 checks retained1e-20',status='passed'),indent=2))
