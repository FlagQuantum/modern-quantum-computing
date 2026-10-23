from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from examples.foundations import density_lab as lab,purification as g,statistical_ensembles as e
rows=[]
for mode in ('statevector','density_matrix'):
 for phase_changed in (False,True):
  packet,C=lab.prepare(.39,-.73,mode,W=e.Z if phase_changed else None)
  local=lab.report(packet,C,'local');joint=lab.report(packet,C,'joint')
  assert local['accepted']and joint['accepted']==(not phase_changed)
  rows.append(dict(mode=mode,reference_Z=phase_changed,local=local,joint=joint,packet={k:[[[z.real,z.imag]for z in row]for row in A.tolist()]for k,A in packet.items()}))
assert g.RUNS==4
print(json.dumps(dict(status='passed',native_circuits=4,original_packets_and_reports=rows),indent=2))
