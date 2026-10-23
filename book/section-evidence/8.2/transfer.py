"""Fresh author transfer cases,including printed8.2B-D;not independent review."""
import json,math,sys
from pathlib import Path
import torch
import flagquantum as fq
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from examples.foundations import state_purity as p
from examples.foundations import statistical_ensembles as e
# Printed B,including explicit transformed native component outputs.
au,u=p.native(.63,-.81);av,v=p.native(1.84,.27)
a,out=p.mixture((.37,.63),(u,v),(au,av))
c=math.cos(.63/2)*math.cos(1.84/2)+complex(math.cos(1.08),math.sin(1.08))*math.sin(.63/2)*math.sin(1.84/2)
e.close(out['purity'],.37**2+.63**2+2*.37*.63*abs(c)**2)
U=e.prepare(e.qubit(-.52,.46));rot=[]
for v0 in (u,v):
    circuit=fq.Circuit(1,dtype=p.D).unitary(0,unitary=e.prepare(v0))
    circuit.unitary(0,unitary=U)
    r=fq.run(circuit,outputs=[fq.density_matrix()],options=e.OPTIONS);p.RUNS+=1
    rot.append(r.density_matrix[0])
after,od=p.mixture((.37,.63),(U@u,U@v),tuple(rot))
e.close(after,U@a@U.mH);e.close(od['purity'],out['purity'])
# Printed C:three native global-phase preparations plus a native orthogonal ray.
components=(u,complex(math.cos(.4),math.sin(.4))*u,complex(math.cos(-.7),math.sin(-.7))*u)
mats=[]
for v0 in components:
    circuit=fq.Circuit(1,dtype=p.D).unitary(0,unitary=e.prepare(v0))
    r=fq.run(circuit,outputs=[fq.density_matrix()],options=e.OPTIONS);p.RUNS+=1
    mats.append(r.density_matrix[0]);e.close(mats[-1],e.outer(v0))
aw,w=p.native(math.pi-.63,math.pi-.81)
e.close(torch.vdot(u,w),0)
same,sd=p.mixture((.2,.3,.5),components,tuple(mats));e.close(sd['purity'],1)
changed,cd=p.mixture((.2,.3,.5),(components[0],components[1],w),(mats[0],mats[1],aw));e.close(cd['purity'],.5)
extra,ed=p.mixture((.2,.3,.5,0.),(components[0],components[1],w,v),(mats[0],mats[1],aw,av));e.close(extra,changed)
# Printed D and fresh nonuniform four-Bell spectral ensemble.
mats=[];vecs=[]
for abit in range(2):
    for bbit in range(2):
        circuit=fq.Circuit(2,dtype=p.D)
        if abit:circuit.X(0)
        if bbit:circuit.X(1)
        circuit.H(0).CX(0,1)
        r=fq.run(circuit,outputs=[fq.density_matrix()],options=e.OPTIONS);p.RUNS+=1
        v0=torch.zeros(4,dtype=p.D);v0[bbit]=1/math.sqrt(2);v0[2+(bbit^1)]=(-1)**abit/math.sqrt(2)
        mats.append(r.density_matrix[0]);vecs.append(v0)
for weights in ((1/3,1/3,1/3,0.),(.13,.29,.41,.17)):
    a4,d4=p.mixture(weights,tuple(vecs),tuple(mats));values,Q=p.spectral_check(a4)
    e.close(d4['purity'],sum(x*x for x in weights))
eps=1e-7;near=torch.diag(torch.tensor([1-eps,eps],dtype=p.D))
e.close(p.diagnostics(near)['purity'],1-2*eps+2*eps**2)
e.close(torch.linalg.matrix_norm(near-torch.diag(torch.tensor([1,0],dtype=p.D))),math.sqrt(2)*eps)
assert p.RUNS==12
print(json.dumps({'native_circuits':p.RUNS,'printed_exercises':['8.2B','8.2C','8.2D'],'B_purity':out['purity'],'B_rotated':od['purity'],'C_pure':sd['purity'],'C_orthogonal':cd['purity'],'fresh_Bell_spectrum':[.13,.29,.41,.17],'status':'passed'},indent=2))
