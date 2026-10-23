import io,contextlib,json
from pathlib import Path
r=Path('/Users/baai/Documents/liuwei/modern-quantum-computing')
codes=[
'''import math
import torch
import flagquantum as fq
from examples.foundations import partial_trace as t
from examples.foundations import statistical_ensembles as e
c=fq.Circuit(2,dtype=t.D).H(0).CX(0,1)
result=fq.run(c,outputs=[fq.density_matrix(name='full'),
    fq.density_matrix(qubits=(0,),name='A'),fq.density_matrix(qubits=(1,),name='B'),
    fq.expectation(fq.X(0)@fq.X(1),name='xx')],options=e.OPTIONS)
t.RUNS+=1
bell_full=result.measurement('full').value[0]
RA=result.measurement('A').value[0];RB=result.measurement('B').value[0]
explicit=torch.tensor([[sum(bell_full[2*i+mu,2*j+mu].item()for mu in range(2))
    for j in range(2)]for i in range(2)],dtype=t.D)
e.close(RA,explicit);e.close(RA,e.I/2);e.close(RB,e.I/2)
A=.7*e.X-.2*e.Y+1.3*e.Z
e.close(torch.trace(RA@A),torch.trace(bell_full@torch.kron(A,e.I)))
print('Native A/B reductions:',[round(x.real.item(),6)for x in RA.diagonal()])
print('Local trace consistency passed;global XX=%.6f'%result.expectation('xx')[0].item())
''',
'''product_result,product_vector=t.native(2,.81,-.26,kind='product')
product_full=product_result.measurement('full').value[0]
product_A=product_result.measurement('r_0').value[0]
product_B=product_result.measurement('r_1').value[0]
e.close(product_A,e.outer(e.qubit(.81,-.26)))
e.close(product_full,torch.kron(product_A,product_B))
t.density(product_A);t.density(product_B)
print('Product reduction:Hermitian,positive,trace=%.6f'%torch.trace(product_A).real.item())
''',
'''c=fq.Circuit(2,dtype=t.D).H(0).P(0,theta=math.pi/2)
result=fq.run(c,outputs=[fq.density_matrix(name='full'),fq.density_matrix(qubits=(0,),name='A'),
    fq.expectation(fq.Y(0),name='y')],options=e.OPTIONS)
t.RUNS+=1
full=result.measurement('full').value[0];actual=result.measurement('A').value[0]
reconstructed=t.reconstruct(full,2,(0,));e.close(reconstructed,actual)
y=result.expectation('y')[0].item()
e.close(y,torch.trace(reconstructed@e.Y));e.close(reconstructed[0,1],-.5j)
wrong=reconstructed.conj();e.close(torch.trace(wrong@e.Y),-1)
print('Hermitian probes reconstruct rho01=%s'%reconstructed[0,1].item())
print('Native Y=%.6f;wrong conjugated density predicts Y=%.6f'%(y,torch.trace(wrong@e.Y).real.item()))
''',
'''components=[t.native(2,0.,0.,kind='basis',basis=b)for b in ((0,0),(1,1))]
mixture=sum(.5*r.measurement('full').value[0]for r,v in components)
mixture_A=t.indexed(mixture,2,(0,))
e.close(mixture_A,RA);e.close(t.indexed(mixture,2,(1,)),RB)
assert not torch.allclose(mixture,bell_full,atol=t.ATOL,rtol=0)
mixture_xx=sum(.5*r.expectation('xx')[0]for r,v in components)
print('Same A and B densities;global XX:Bell=1.000000,classical mixture=%.6f'%mixture_xx.item())
''',
'''U=e.prepare(e.qubit(.63,.27))
before,_=t.native(2,.91,-.36)
after,_=t.native(2,.91,-.36,rotate_last=U)
full=before.measurement('full').value[0]
B=torch.kron(e.I,U)
changed_coordinates=B.mH@full@B
passive=t.trace_ab(changed_coordinates,2,2)
e.close(passive,before.measurement('r_0').value[0])
e.close(before.measurement('r_0').value,after.measurement('r_0').value)
print('Discarded-basis contraction and actual local B rotation give the same retained density')
''',
'''c,expected=t.preparation(3,.76,-.58)
result=fq.run(c,outputs=[fq.density_matrix(name='full'),
    fq.density_matrix(qubits=(2,0),name='A20'),fq.density_matrix(qubits=(0,2),name='A02'),
    fq.probabilities(qubits=(2,0),name='p20')],options=e.OPTIONS)
t.RUNS+=1
full3=result.measurement('full').value[0]
A20=result.measurement('A20').value[0];A02=result.measurement('A02').value[0]
scalar=t.indexed(full3,3,(2,0));tensor=t.axes(full3,3,(2,0))
e.close(A20,scalar);e.close(A20,tensor)
permutation=torch.tensor([0,2,1,3]);e.close(A20,A02[permutation][:,permutation])
e.close(A20.diagonal().real,result.measurement('p20').value[0])
print('Ordered retained tuple(2,0):scalar indices,tensor axes,native density/probability agree')
print('Reversing retained tuple permutes both matrix axes;it does not transpose/conjugate the matrix')
''',
'''from examples.foundations import density_updates as d
biased,_=t.native(2,.72,.43,kind='bell')
full=biased.measurement('full').value[0];prior=biased.measurement('r_0').value[0]
groups=((torch.kron(e.I,d.P0),),(torch.kron(e.I,d.P1),))
probs,states,sigmas,ignored=d.instrument(full,groups)
selected_A=[t.indexed(state,2,(0,))for state in states]
e.close(selected_A[0],d.P0);e.close(selected_A[1],d.P1)
e.close(t.indexed(ignored,2,(0,)),prior)
e.close(sum(p*a for p,a in zip(probs,selected_A)),prior)
assert not torch.allclose((selected_A[0]+selected_A[1])/2,prior,atol=t.ATOL,rtol=0)
print('Recorded B outcomes:',[round(p,9)for p in probs])
print('Conditional A states differ;ignored-result A equals its prior native reduction')
''',
'''one=t.indexed(full3,3,());e.close(one,torch.ones((1,1),dtype=t.D))
e.close(t.indexed(full3,3,(0,1,2)),full3)
e.close(t.indexed(3*full3,3,()),torch.tensor([[3]],dtype=t.D))
general=torch.diag(torch.tensor([.1,.2,.1,.3,.2,.1],dtype=t.D))
e.close(t.trace_ab(general,3,2),torch.diag(torch.tensor([.3,.4,.3],dtype=t.D)))
e.close(t.trace_ab(general,1,6),torch.ones((1,1),dtype=t.D))
e.close(t.trace_ab(general,6,1),general)
print('Host empty/full/dimension-one and3x2factor traces passed;no normalization performed')
print('%d malformed contracts rejected'%t.invalid_checks())
print('%d actual native body circuits;native empty tuple is not host trace-all'%t.RUNS)
''']
ns={};results=[]
for j,code in enumerate(codes,1):
 out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(code,'8.4-unit%d'%j,'exec'),ns)
 results.append(dict(code=code,output=out.getvalue()))
assert ns['t'].RUNS==10
(r/'book/section-evidence/8.4/body-units.json').write_text(json.dumps(results,indent=2)+'\n')
print('\n'.join(x['output']for x in results))
