from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from examples.foundations import uniform_reversible as u
nodes=(('XOR',(0,1)),('AND',(3,2)));outputs=(4,);rows=[]
for mode in ('statevector','density_matrix'):
 for x in ((1,0,1),(1,1,1)):
  for y in ((0,),(1,)):
   r,cost,leak=u.execute(3,nodes,outputs,x,y,mode=mode);assert cost['network_gates']==7
   rows.append(dict(mode=mode,input=x,old_output=y,function=u.evaluate(x,nodes,outputs)[0],cost=cost,workspace_leak=leak))
 r,cost,leak=u.execute(3,nodes,outputs,coherent=True,mode=mode);rows.append(dict(mode=mode,complex_joint_input=True,cost=cost,workspace_leak=leak))
assert u.RUNS==10
print(json.dumps(dict(status='passed',native_circuits=10,cases=rows),indent=2))
