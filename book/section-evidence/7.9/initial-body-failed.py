from pathlib import Path
import contextlib,io,json
codes=[
r'''import math
import torch
import flagquantum as fq
from examples.foundations import entanglement_limits as t
from examples.foundations.tensor_spaces import OPTIONS

for message in (0,1):
    c = fq.Circuit(2,dtype=torch.complex128).h(0).cx(0,1)
    if message:
        c.x(0)
    r = fq.run(c,outputs=[fq.probabilities(qubits=(1,)),
        fq.samples(qubits=(0,1))],shots=17,options=OPTIONS)
    t.RUNS += 1
    t.close(r.probabilities[0],[.5,.5])
    assert all((a ^ b)==message for a,b in r.samples[0].tolist())
print("Two Alice choices:Bob probabilities=[0.5,0.5] in both cases.")
print("Correlated random records do not give Bob Alice's chosen bit.")''',
r'''psi = t.qubit(.93,-.47)
c = fq.Circuit(3,dtype=torch.complex128).unitary(0,unitary=t.prepare(psi))
c.h(1).cx(1,2).cx(0,1).h(0)
r = fq.run(c,outputs=[fq.probabilities(qubits=(2,)),
    fq.expectation(fq.X(2),name="bx"),
    fq.expectation(fq.Y(2),name="by"),
    fq.expectation(fq.Z(2),name="bz")],options=OPTIONS)
t.RUNS += 1
t.close(r.statevector()[0],t.teleport_reference(psi))
branches = t.teleport_branches(r.statevector()[0])
for k,(p,v) in enumerate(branches):
    m,n = divmod(k,2)
    t.close(p,.25)
    t.close(t.correction(m,n)@v,psi)
for name in ("bx","by","bz"):
    t.close(r.expectation(name)[0],0.)
for A in (t.X,t.Y,t.Z):
    t.close(sum(p*t.mean(v,A) for p,v in branches),0.)
print("Four corrected branches equal the input;without the message Bob X=Y=Z=0.")''',
r'''resource = torch.tensor([1,0,0,1],dtype=torch.complex128)/math.sqrt(2)
states = [t.qubit(0.,0.),t.qubit(math.pi,0.),
          t.qubit(math.pi/2,0.),t.qubit(math.pi/2,math.pi/2)]
fidelities = []
for v in states:
    c = fq.Circuit(4,dtype=torch.complex128).unitary(0,unitary=t.prepare(v))
    c.h(2).cx(2,3).cx(0,1)
    r = fq.run(c,outputs=[fq.probabilities()],options=OPTIONS)
    t.RUNS += 1
    expected,target = t.clone_reference(v)
    t.close(r.statevector()[0],expected)
    fidelities.append(float(abs(torch.vdot(target,r.statevector()[0]))**2))
left,right = torch.kron(states[0],resource),torch.kron(states[2],resource)
t.close(torch.vdot(left,right),1/math.sqrt(2))
t.close(fidelities,[1.,1.,.5,.25])
print("CNOT candidate target fidelities for 0,1,+,+i:",
      [round(x,8) for x in fidelities])
print("Fixed entangled resource preserves the obstructing input overlap 1/sqrt(2).")''',
r'''for a in (0,1):
    for b in (0,1):
        for received in (False,True):
            c = fq.Circuit(2,dtype=torch.complex128).h(0).cx(0,1)
            if b:
                c.x(0)
            if a:
                c.z(0)
            if received:
                c.cx(0,1).h(0)  # Bob must hold both qubits for this decoder
            r = fq.run(c,outputs=[fq.probabilities(qubits=(1,),name="bob"),
                fq.probabilities(qubits=(0,1),name="joint")],options=OPTIONS)
            t.RUNS += 1
            if not received:
                t.close(r.measurement("bob").value[0],[.5,.5])
            else:
                target = torch.zeros(4,dtype=torch.complex128)
                target[2*a+b] = 1.
                t.close(r.statevector()[0],target)
print("Four messages:Bob-only marginals identical;after qubit receipt and joint decode,labels are exact.")''',
r'''c = fq.Circuit(4,dtype=torch.complex128)
c.h(0).cx(0,1).h(2).cx(2,3).cx(1,2).h(1)
r = fq.run(c,outputs=[fq.probabilities(qubits=(0,3))],options=OPTIONS)
t.RUNS += 1
family = t.swapping.branches(r.statevector()[0])
correct_f,stale_f = [],[]
for k,(p,v) in enumerate(family):
    m,n = divmod(k,2)
    good = torch.kron(t.I,t.correction(m,n))@v
    stale = torch.kron(t.I,t.correction(m ^ 1,n))@v
    correct_f.append(float(abs(torch.vdot(t.swapping.bell(0,0),good))**2))
    stale_f.append(float(abs(torch.vdot(t.swapping.bell(0,0),stale))**2))
    t.close(abs(torch.linalg.det(stale.reshape(2,2))),.5)
t.close(correct_f,[1.]*4)
t.close(stale_f,[0.]*4)
print("Correct frames:four target fidelities1;stale phase frames:four target fidelities0.")
print("All stale-frame states are still maximally entangled.")''',
r'''zx = ((0.,0.),(0.,math.pi/2),(math.pi/2,0.),(math.pi/2,math.pi/2))
tilted = ((0.,math.pi/4),(0.,-math.pi/4),
          (math.pi/2,math.pi/4),(math.pi/2,-math.pi/4))
values = []
for j,(a,b) in enumerate(zx+tilted):
    c = fq.Circuit(2,dtype=torch.complex128).h(0).cx(0,1)
    c.ry(0,-a).ry(1,-b)
    r = fq.run(c,outputs=[fq.probabilities(),
        fq.expectation(fq.Z(0)@fq.Z(1),name="e")],options=OPTIONS)
    t.RUNS += 1
    e = float(r.expectation("e")[0])
    t.close(e,t.correlation(a,b))
    if j<4:
        t.close(r.probabilities[0],t.local_table(j//2,j % 2))
    values.append(e)
S0 = sum(s*e for s,e in zip((1,1,1,-1),values[:4]))
S1 = sum(s*e for s,e in zip((1,1,1,-1),values[4:]))
t.close(S0,0.)
t.close(S1,2*math.sqrt(2))
print("Same Bell resource:Z/X contexts S="+format(S0,".8f")+
      ";tilted contexts S="+format(S1,".8f"))''',
r'''k,roles = 3,(5,1,3,0,4,2)  # left roles first,then right roles
c = fq.Circuit(2*k,dtype=torch.complex128)
for j in range(k):
    c.h(roles[j]).cx(roles[k+j])
r = fq.run(c,outputs=[fq.probabilities(),fq.samples()],shots=11,options=OPTIONS)
t.RUNS += 1
ref = t.pair_reference(k,roles)
t.close(r.statevector()[0],ref)
t.close(r.probabilities[0],ref.abs().square())
C = torch.zeros((2**k,2**k),dtype=torch.complex128)
for x in range(2**k):
    for y in range(2**k):
        bits = [0]*(2*k)
        for q,b in zip(roles,format(x,"03b")+format(y,"03b")):
            bits[q] = int(b)
        idx = sum(b << (2*k-1-q) for q,b in enumerate(bits))
        C[x,y] = r.statevector()[0,idx]
t.close(C,torch.eye(2**k,dtype=torch.complex128)/math.sqrt(2**k))
for row in r.samples[0].tolist():
    assert all(row[roles[j]]==row[roles[k+j]] for j in range(k))
print("Three Bell pairs:Schmidt rank8;Z distribution is exactly3fair bits duplicated.")
print("All11native records obey the pair constraints;no frequency-equality test.")''',
r'''vplus = t.qubit(math.pi/2,0.)
for phi,calibrated in ((0.,False),(math.pi,False),(math.pi,True)):
    c = fq.Circuit(3,dtype=torch.complex128).h(0).h(1).cx(1,2).p(1,phi)
    if calibrated:
        c.p(1,-phi)  # compensate the known resource phase before using the pair
    c.cx(0,1).h(0)
    r = fq.run(c,outputs=[fq.probabilities(qubits=(2,))],options=OPTIONS)
    t.RUNS += 1
    phase = 0. if calibrated else phi
    t.close(r.statevector()[0],t.teleport_reference(vplus,phase))
    f = []
    for k,(p,v) in enumerate(t.teleport_branches(r.statevector()[0])):
        m,n = divmod(k,2)
        corrected = t.correction(m,n)@v
        f.append(float(abs(torch.vdot(vplus,corrected))**2))
    target = math.cos(phase/2)**2
    t.close(f,[target]*4)
    print("phi="+format(phi,".8f"),"calibrated="+str(calibrated),
          "four-branch F="+format(target,".8f"))
print("Literal body native executions:",t.RUNS)'''
]
ns={}
rows=[]
for j,code in enumerate(codes,1):
    out=io.StringIO()
    with contextlib.redirect_stdout(out):
        exec(compile(code,f'7.9-fragment-{j}','exec'),ns)
    rows.append({'code':code+'\n','output':out.getvalue()})
Path('/private/tmp/limits_fragments.json').write_text(json.dumps(rows,indent=2))
Path('book/section-evidence/7.9/body-execution.txt').write_text(''.join(f'Unit{j}\n'+r['output'] for j,r in enumerate(rows,1)))
print('Executed8units:',ns['t'].RUNS,'native circuits.')
for j,r in enumerate(rows,1):print(j,r['output'])
