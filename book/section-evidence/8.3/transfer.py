"""Fresh8.3B-D author cases;not independent review."""
import json,math,sys
from pathlib import Path
import torch
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from examples.foundations import density_updates as d
from examples.foundations import statistical_ensembles as e
u=e.qubit(.57,-.68);v=e.qubit(1.92,.44);weights=(.41,.59)
inputs=[d.native(c)for c in (u,v)]
rho=sum(w*r.density_matrix[0]for w,r in zip(weights,inputs))
a=rho[0,0].real.item();z=rho[0,1].item();k=.43;h=math.sqrt(1-k*k)
analytic=(torch.tensor([[(1+k)*a,h*z],[h*z.conjugate(),(1-k)*(1-a)]],dtype=d.D)/2,
          torch.tensor([[(1-k)*a,h*z],[h*z.conjugate(),(1+k)*(1-a)]],dtype=d.D)/2)
updates=[]
for flip in (False,True):
    groups=d.weak(k,flip);out=d.instrument(rho,groups);updates.append(out)
    native=[d.coupled(c,k,flip)for c in (u,v)]
    for r in range(2):
        sigma=analytic[r]if not(flip and r==1)else d.X@analytic[r]@d.X
        e.close(out[2][r],sigma)
        e.close(sigma,sum(w*result[1][r]for w,result in zip(weights,native)))
        # Bayesian component weights reproduce the same normalized branch.
        K=groups[r][0];posterior=torch.zeros_like(rho);total=0.
        for w,c in zip(weights,(u,v)):
            branch=K@c;q=torch.vdot(branch,branch).real.item()
            posterior+=w*q/out[0][r]*e.outer(branch/math.sqrt(q));total+=w*q/out[0][r]
        e.close(total,1);e.close(posterior,out[1][r])
    e.close(out[3],sum(out[2],torch.zeros_like(rho)))
e.close(updates[0][0],updates[1][0])
e.close(updates[0][0][0],(1+k*(2*a-1))/2)
e.close(d.mean(updates[0][3],d.Z),2*a-1)
assert not torch.allclose(updates[0][3],updates[1][3],atol=d.ATOL,rtol=0)
# PrintedC:four native Bell preparations,including zero-XX trap and both modes.
even=torch.diag(torch.tensor([1,0,0,1],dtype=d.D));odd=torch.eye(4,dtype=d.D)-even
basis=tuple(torch.diag(torch.eye(4,dtype=d.D)[i])for i in range(4))
for mode in ('statevector','density_matrix'):
    for phi in (-.38,math.pi/2):
        result,c=d.bell(math.pi/2,phi,mode);state=result.density_matrix[0]
        coarse=d.instrument(state,((even,),(odd,)));fine=d.instrument(state,((basis[0],basis[3]),(basis[1],basis[2])))
        e.close(coarse[0],fine[0]);e.close(coarse[3],state)
        e.close(fine[3],torch.diag(torch.tensor([.5,0,0,.5],dtype=d.D)))
        for name,A,value in (('xx',torch.kron(d.X,d.X),math.cos(phi)),('xy',torch.kron(d.X,d.Y),math.sin(phi))):
            e.close(d.mean(coarse[3],A),value);e.close(d.mean(fine[3],A),0)
# Hidden-label representations tested on several fresh full input matrices.
for state in (rho,e.outer(u),e.outer(v)):
    e.close(d.instrument(state,((d.P0,d.P1),))[3],d.instrument(state,((d.I/math.sqrt(2),d.Z/math.sqrt(2)),))[3])
# PrintedD:new weak first measurement,thenX;four actual native circuits.
second=(((d.I+d.X)/2,),((d.I-d.X)/2,))
table=d.sequential(rho,d.weak(k),second);p=updates[0][0];t=h*z.real
formula=torch.tensor([[(pr+t)/2,(pr-t)/2]for pr in p],dtype=torch.float64)
e.close(table,formula)
for mode in ('statevector','density_matrix'):
    native=[d.coupled(c,k,analyzer=True,mode=mode)for c in (u,v)]
    e.close(table,sum(w*result[2]for w,result in zip(weights,native)))
    for r,pr in enumerate(p):e.close(table[r]/pr,torch.tensor(d.instrument(updates[0][1][r],second)[0],dtype=torch.float64))
assert not torch.allclose(table,d.sequential(rho,d.Z_GROUPS,second),atol=d.ATOL,rtol=0)
rare=d.instrument(torch.diag(torch.tensor([1-1e-20,1e-20],dtype=d.D)),d.Z_GROUPS)
assert rare[0][1]>0 and rare[1][1]is not None
assert d.RUNS==14
print(json.dumps(dict(native_circuits=d.RUNS,printed_exercises=['8.3B','8.3C','8.3D'],B_probabilities=list(p),B_ignored_Z=[d.mean(o[3],d.Z)for o in updates],D_joint=table.tolist(),rare_positive=rare[0][1],status='passed'),indent=2))
