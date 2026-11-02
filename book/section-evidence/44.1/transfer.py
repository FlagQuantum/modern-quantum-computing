"""44.1fresh native outputs and phase-preserving references."""
from pathlib import Path
import sys,json,torch
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from examples.foundations import requested_outputs as o
for mode in('statevector','density_matrix'):
 for profile in('queries','full'):o.execute(5,-.91,.73,(1,0,1,0,0),(4,0,2),mode,profile,shots=23,seed=803)
o.execute(5,-.91,.73,(1,0,1,0,0),(4,0,2),profile='state',seed=803)
for mode in('statevector','density_matrix'):o.execute(2,1.17,-.38,(1,0),(1,0),mode,shots=23,seed=803)
a,ra=o.execute(1,.69,.8,(0,),(0,),profile='queries',shots=23,seed=803)
b,rb=o.execute(1,.69,-.8,(0,),(0,),profile='queries',shots=23,seed=803)
o.e.close(a.measurement('selected').value,b.measurement('selected').value)
assert not torch.allclose(a.statevector(),b.statevector(),atol=1e-12,rtol=0)
assert o.RUNS==9
for mask in ((4,4),(5,)):
 try:o.payload(5,'probabilities',qubits=mask)
 except ValueError:pass
 else:raise AssertionError('Invalid fresh mask accepted')
assert o.payload(5,'samples',qubits=(4,0,2),shots=23)['int64_bytes']==552
assert (o.storage(5)['state_bytes'],o.storage(5)['density_bytes'])==(512,16384)
print('Nine fresh native calls passed: five-qubit query/full/state paths,two-qubit ordered masks and opposite single-qubit phases.')
print('Five-qubit selected table64 bytes; 69 record bits occupy552 int64 bytes; full vector512 and density16384 bytes; malformed masks rejected.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(o.RECEIPTS,indent=2)+'\n')
