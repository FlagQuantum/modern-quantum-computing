from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from examples.foundations import measurement_execution as m
cases=[(3,(2,0),(1,0,0)),(3,(2,0),(0,0,1)),(3,(0,2,1),(1,1,0)),(5,(4,2,0),(1,0,0,0,0)),(5,(0,3),(1,0,0,0,0)),(5,(2,1,4,0),(1,0,0,0,0))]
for n,Q,bits in cases:
 for mode in('statevector','density_matrix'):m.calibrate(n,Q,bits,mode)
assert m.RUNS==12
print('12 native X-only basis-label calibration calls passed: six asymmetric declared masks/bit patterns,both modes; exact one-hot probabilities and every raw bit column agree.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(m.RECEIPTS,indent=2)+'\n')
