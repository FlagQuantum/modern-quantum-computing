from pathlib import Path
import json,math,itertools
import flagquantum as fq
import torch
from examples.foundations import entanglement_limits as t
rows=[]
for theta,phase,resource_phase in ((1.14,-.38,.83),(1.71,.59,-.64),(.67,-.91,1.23)):
    psi=t.qubit(theta,phase)
    r=t.run(t.teleport_circuit(psi,resource_phase),[
        fq.probabilities(qubits=(2,)),fq.expectation(fq.X(2),name='x'),
        fq.expectation(fq.Y(2),name='y'),fq.expectation(fq.Z(2),name='z')])
    t.close(r.statevector()[0],t.teleport_reference(psi,resource_phase))
    family=t.teleport_branches(r.statevector()[0])
    f=[]
    for k,(p,v) in enumerate(family):
        m,n=divmod(k,2)
        expected=torch.tensor([psi[i ^ n]*(-1)**(m*(i ^ n))*complex(math.cos(resource_phase*i),math.sin(resource_phase*i)) for i in (0,1)],dtype=t.D)
        t.close(v,expected)
        output=t.correction(m,n)@v
        predicted=1-4*abs(psi[0])**2*abs(psi[1])**2*math.sin(resource_phase/2)**2
        t.close(abs(torch.vdot(psi,output))**2,predicted)
        f.append(float(predicted))
    for name in ('x','y','z'):t.close(r.expectation(name)[0],0.)
    c=fq.Circuit(3,dtype=t.D).unitary(0,unitary=t.prepare(psi))
    c.h(1).cx(1,2).p(1,resource_phase).p(1,-resource_phase).cx(0,1).h(0)
    calibrated=t.run(c,[fq.probabilities(qubits=(2,))])
    t.close(calibrated.statevector()[0],t.teleport_reference(psi))
    for k,(p,v) in enumerate(t.teleport_branches(calibrated.statevector()[0])):
        t.close(t.correction(k//2,k % 2)@v,psi)
    rows.append({'theta':theta,'input_phase':phase,'resource_phase':resource_phase,'branch_fidelities':f,'calibrated_fidelity':1.})
k=4;roles=(7,1,5,3,0,6,2,4)
for x_basis in (False,True):
    c=fq.Circuit(8,dtype=t.D)
    # Actual declared source,with left controls and right targets.
    for j in range(k):c.h(roles[j]).cx(roles[j],roles[k+j])
    if x_basis:
        for q in roles[:k]:c.h(q)
    r=t.run(c,[fq.probabilities(),fq.samples()],shots=23,seed=791)
    if not x_basis:
        ref=t.pair_reference(k,roles)
        t.close(r.statevector()[0],ref);t.close(r.probabilities[0],ref.abs().square())
    else:
        # Explicit scalar H expansion:for each output x,y,amplitude=(-1)^(x.y)/16.
        expected=torch.zeros(256,dtype=t.D)
        for physical in range(256):
            bits=[(physical>>(7-q))&1 for q in range(8)]
            phase=sum(bits[roles[j]]*bits[roles[k+j]] for j in range(k))
            expected[physical]=(-1)**phase/16
        t.close(r.statevector()[0],expected)
        t.close(r.probabilities[0],torch.full((256,),1/256,dtype=torch.float64))
for theta,alpha,beta in ((.87,-.63,.49),(1.31,.28,-1.07),(2.04,-.91,1.19),(.59,1.03,.34)):
    c=fq.Circuit(2,dtype=t.D).ry(0,theta).cx(0,1).ry(0,-alpha).ry(1,-beta)
    r=t.run(c,[fq.expectation(fq.Z(0)@fq.Z(1),name='e')])
    t.close(r.expectation('e')[0],t.correlation(alpha,beta,theta))
assert t.RUNS==12
Path('book/section-evidence/7.9/transfer.json').write_text(json.dumps({'native_runs':12,'fresh_resource_cases':rows,'printed_exercises':['7.9-B first resource case','7.9-C mapped four-pair Z/Z and X/Z'],'fresh_correlation_cases':4,'no_phase_alignment':True},indent=2)+'\n')
print('12fresh CPUcomplex128native circuits:6resource-phase/calibration,2mapped four-pair distributions,4signed-angle correlations passed.')
print('Exact printed7.9B-C and all12fresh teleportation branches checked;no phase alignment or sample-frequency equality.')
