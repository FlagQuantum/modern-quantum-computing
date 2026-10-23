from pathlib import Path
import sys,torch
sys.path.insert(0,str(Path(__file__).resolve().parents[4]))
from examples.foundations import reduced_spectra as g,statistical_ensembles as e
for mode in ('statevector','density_matrix'):
 r,C,data=g.pair(1.39,-.81,.44,-.91,mode)
 assert data[1].pow(4).sum()>=.5-1e-12
 rr,dd=g.rectangular(.91,.68,mode)
 for A,dim in ((rr.measurement('A0').value[0],4),(rr.measurement('B0').value[0],2)):
  for z in (.17+.43j,-.51+.29j):
   e.close(torch.linalg.det(z*torch.eye(dim,dtype=g.D)-A),torch.prod(z-g.full_spectrum(dd[0][1],dim)))
assert g.RUNS==4
print('4fresh native circuits:complex characteristic polynomial checks and reduced purity bound passed in both modes.')
