"""Fresh printed8.6B-D and rank-one larger-reference validation."""
from pathlib import Path
import sys,json,torch
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from examples.foundations import purification as g,statistical_ensembles as e
Q=e.prepare(e.qubit(-.69,.77));W=e.prepare(e.qubit(.83,-.48));weights=(.61,.39)
C,rho=g.spectral(weights,Q,2)
J=torch.zeros((4,2),dtype=g.D);J[1,0]=1j;J[2,1]=1
for mode in ('statevector','density_matrix'):
    small,_=g.execute(C,mode=mode);changed,CW=g.execute(C,W,mode)
    e.close(small.measurement('S').value,changed.measurement('S').value)
    wrong=C@W.mH;assert torch.linalg.vector_norm(wrong-CW).item()>.1
    e.close(changed.measurement('R').value[0],W@torch.diag(torch.tensor(weights,dtype=g.D))@W.mH)
    large,CJ=g.execute(C@J.T,mode=mode);e.close(large.measurement('S').value[0],rho)
    F=g.support_frames(C,Q,weights);G=g.support_frames(CJ,Q,weights)
    T=G@F.mH;e.close(T,J);e.close(T.mH@T,e.I)
    Cd,rd=g.spectral((.5,.5),e.I,2);deg,CdW=g.execute(Cd,W,mode)
    V=e.prepare(e.qubit(.64,-.73));Fd=g.support_frames(Cd,V,(.5,.5));Gd=g.support_frames(CdW,V,(.5,.5));e.close(Gd@Fd.mH,W)
    vs=(e.qubit(.42,-.36),e.qubit(1.27,.63));E=g.ensemble_coeff((.25,.75),vs)
    a,_=g.execute(E,mode=mode);rhoE=e.rho((.25,.75),vs);lam,EV=torch.linalg.eigh(rhoE)
    assert (lam>0).all();Cs,_=g.spectral(tuple(lam.tolist()),EV,2);b,_=g.execute(Cs,mode=mode)
    e.close(a.measurement('S').value,b.measurement('S').value)
    F=g.support_frames(Cs,EV,tuple(lam.tolist()));G=g.support_frames(E,EV,tuple(lam.tolist()));U=G@F.mH;g.unitary(U,2);e.close(Cs@U.T,E)
    h=.5*vs[0]+(.75**.5)*vs[1];bad=torch.outer(h,h.conj());assert abs(torch.trace(bad).item()-1)>.1
    repaired=bad/torch.trace(bad);assert torch.linalg.vector_norm(repaired-rhoE).item()>.1
    Cp,rp=g.spectral((1.,0.),Q,4);rankone,_=g.execute(Cp,mode=mode);e.close(rankone.measurement('S').value[0],rp)
assert g.RUNS==14
print(json.dumps({'status':'passed','native_circuits':g.RUNS,'cases':['printed8.6Bcomplexrotation','printed8.6Ccomplexisometry/degeneratecommonbasis','printed8.6Dnonorthogonalensemble/spectralrelation/wronglabels','rankonefour-dimensionalreference'],'host_wrong_label_trace':torch.trace(bad).real.item(),'host_normalized_wrong_label_density_rejected':True},indent=2))
