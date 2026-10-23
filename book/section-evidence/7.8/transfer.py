import itertools,json,math
from pathlib import Path
import torch
import flagquantum as fq
from examples.foundations import entanglement_swapping as s
rows=[]
cases=[
((3,0,2,1),(.91,-.43,1.27,.29)),
((2,3,1,0),(1.37,.64,.77,-.81)),
((1,3,0,2),(-.88,.31,1.61,-.27)),
((3,2,0,1),(1.91,-.52,-.69,.73)),
((2,0,3,1),(.47,-1.2,2.11,.42)),
((1,2,3,0),(2.23,.19,1.09,-.58)),
]
for roles,angles in cases:
    result,family=s.analyze(angles,roles)
    r=s.execute(s.source(roles,angles),[
        fq.probabilities(qubits=(roles[2],roles[1])),
        fq.samples(qubits=(roles[2],roles[1]))],shots=19,seed=788)
    s.close(r.probabilities[0],[family[0][0],family[2][0],family[1][0],family[3][0]])
    bits,trial=s.packet(r.samples[0],(roles[2],roles[1]),roles,'fresh-078')
    assert len(bits)==19 and trial=='fresh-078'
    d,e=s.link(*angles[:2]),s.link(*angles[2:])
    row={'roles':roles,'angles':angles,'probabilities':[p for p,v in family],'corrected_fidelities':[]}
    for k,(p,v) in enumerate(family):
        target=torch.kron(s.I,s.correction(k//2,k%2))@v
        row['corrected_fidelities'].append(float(abs(torch.vdot(s.bell(0,0),target))**2))
        assert p>0
    rows.append(row)
# Independent classical partial-message effect equality for fresh complex effects.
B=torch.stack([s.bell(0,0),s.bell(1,0)],dim=1)
for theta,phi in ((.63,-.71),(1.34,.39),(2.02,-.48)):
    v=torch.tensor([math.cos(theta/2),complex(math.cos(phi),math.sin(phi))*math.sin(theta/2)],dtype=s.D)
    a=torch.kron(v,s.link(1.17,.44))
    E=torch.outer(a,a.conj())
    lhs=sum(torch.vdot(B[:,m],E@B[:,m]).real/2 for m in (0,1))
    rhs=(E[0,0]+E[3,3])/2
    s.close(lhs,rhs)
assert s.RUNS==12
Path('book/section-evidence/7.8/transfer.json').write_text(json.dumps({'native_runs':s.RUNS,'fresh_cases':rows,'additional_classical_partial_message_effects':3,'exact_printed_exercise':'7.8-C;first case','phase_alignment':False},indent=2))
print('12fresh mapped CPUcomplex128native circuits;all24conditional branches,raw column conversion and exact printed7.8C passed.')
print('3independent complex effects:partial-message product-ensemble equality passed;no native executions for these sums.')
