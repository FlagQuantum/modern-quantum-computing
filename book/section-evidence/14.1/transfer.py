from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from examples.foundations import input_models as m
rows=[]
for mode in ('statevector','density_matrix'):
 for x in ('1110','1001'):
  for y in (0,1):
   r,cost=m.execute(x,y,mode)
   rows.append(dict(mode=mode,x=x,y=y,answer=int(r.measurement('record').value[0,0,0]),cost=cost,total_gates_including_target=cost['gates_with_loading']+y))
assert m.RUNS==8
assert m.binary('001000')==(8,6)and m.binary('1000')==(8,4)
assert m.binary('1'+'0'*63)==(2**63,64)
assert len(m.family(513))==513
print(json.dumps(dict(status='passed',native_circuits=8,host_gate_list_only_length513=True,cases=rows),indent=2))
