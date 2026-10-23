"""8.2: native pure outputs,explicit ensemble sums and numerical purity diagnostics."""
import math
from dataclasses import replace
import torch
import flagquantum as fq
try:
    from examples.foundations import statistical_ensembles as e
except ModuleNotFoundError:
    import statistical_ensembles as e
D=e.D
ATOL=1e-12
RUNS=0


def native(theta,phi,mode='statevector',bell=False):
    """One real circuit invocation;density output is native,not reconstructed."""
    global RUNS
    if mode not in ('statevector','density_matrix') or type(bell)is not bool:
        raise ValueError('Declared mode and Boolean bell flag required')
    v=e.qubit(theta,phi)
    c=fq.Circuit(2 if bell else 1,dtype=D)
    c.RY(0,theta=theta).P(0,theta=phi)
    if bell:c.CX(0,1)
    result=fq.run(c,outputs=[fq.density_matrix(),fq.probabilities()],
                  options=replace(e.OPTIONS,mode=mode))
    RUNS+=1
    if bell:v=torch.stack((v[0],v[0]*0,v[0]*0,v[1]))
    a=result.density_matrix[0]
    e.close(a,e.outer(v));e.close(result.probabilities[0],v.abs().square())
    return a,v


def diagnostics(a):
    """Validate numerically;report residuals,never return an exact pure/mixed label."""
    e.density(a)
    values=torch.linalg.eigvalsh(a)
    trace_square=torch.trace(a@a).real.item()
    frobenius=sum(abs(a[i,j].item())**2 for i in range(len(a)) for j in range(len(a)))
    spectral=sum(x*x for x in values.tolist())
    e.close(trace_square,frobenius);e.close(trace_square,spectral)
    return {'purity':trace_square,'eigenvalues':values,
            'idempotence_residual':torch.linalg.matrix_norm(a@a-a).item(),
            'minimum_eigenvalue':values.min().item()}


def overlaps(weights,vectors):
    e.ensemble(weights,vectors)
    # Independent scalar inner products,not matrix multiplication or eigenvalues.
    return sum(p*q*abs(sum(x.item().conjugate()*y.item() for x,y in zip(u,v)))**2
               for p,u in zip(weights,vectors) for q,v in zip(weights,vectors))


def mixture(weights,vectors,matrices):
    e.ensemble(weights,vectors)
    if len(matrices)!=len(vectors):raise ValueError('One matrix per component required')
    for a,v in zip(matrices,vectors):
        e.density(a);e.close(a,e.outer(v))
    a=sum((p*m for p,m in zip(weights,matrices)),torch.zeros_like(matrices[0]))
    e.close(a,e.scalar_rho(weights,vectors))
    out=diagnostics(a);e.close(out['purity'],overlaps(weights,vectors))
    return a,out


def spectral_check(a):
    e.density(a)
    values,Q=torch.linalg.eigh(a)
    rebuilt=sum((values[j]*e.outer(Q[:,j]) for j in range(len(a))),torch.zeros_like(a))
    e.close(rebuilt,a)
    return values,Q


def rejected():
    bad=[torch.tensor([[1,1],[0,0]],dtype=D),
         torch.diag(torch.tensor([1.2,-.2],dtype=D)),
         torch.eye(2,dtype=D),torch.zeros((2,2),dtype=D),
         torch.diag(torch.tensor([2/3,2/3,-1/3,0],dtype=D)),
         torch.full((2,2),complex('nan'),dtype=D),
         torch.eye(3,dtype=D)/3,torch.eye(2,dtype=torch.complex64)/2]
    count=0
    for a in bad:
        try:diagnostics(a)
        except ValueError:count+=1
        else:raise AssertionError('Malformed density accepted')
    for args in (((-.1,1.1),(torch.tensor([1,0],dtype=D),)*2),
                 ((.2,.2),(torch.tensor([1,0],dtype=D),)*2)):
        try:e.ensemble(*args)
        except ValueError:count+=1
        else:raise AssertionError('Malformed weights accepted')
    assert count==10
    return count


def main():
    # 24native outputs across one/two qubits and both modes.
    for mode in ('statevector','density_matrix'):
        for bell in (False,True):
            for theta,phi in ((0.,0.),(math.pi,0.),(math.pi/2,0.),
                              (math.pi/2,math.pi/2),(.83,-.49),(1.31,.72)):
                a,v=native(theta,phi,mode,bell)
                out=diagnostics(a);e.close(out['purity'],1)
                spectral_check(a)
    print('24native pure outputs:both modes,one/two qubits;purity1 and spectral reconstruction passed.')
    # 12native components;all host mixtures checked by four independent formulas.
    case_count=0
    for bell in (False,True):
        parts=[native(t,p,bell=bell) for t,p in ((0.,0.),(math.pi,0.),
                (math.pi/2,0.),(math.pi/2,math.pi),(.91,.37),(1.57,-.62))]
        for i,j,w in ((0,1,.5),(0,1,.73),(2,3,.5),(4,5,.28),(4,4,.41),(0,5,0.)):
            a,out=mixture((w,1-w),(parts[i][1],parts[j][1]),(parts[i][0],parts[j][0]))
            spectral_check(a)
            assert 1/len(a)-ATOL<=out['purity']<=1+ATOL
            case_count+=1
    print('12ensembles:trace-square,entry norm,spectrum and scalar overlap agree;zero weights and duplicate rays retained.')
    # Four native Bell-basis components,cover rank1,2,3,4 uniform states.
    mats=[];vecs=[]
    for a in range(2):
        for b in range(2):
            global RUNS
            c=fq.Circuit(2,dtype=D)
            if a:c.X(0)
            if b:c.X(1)
            c.H(0).CX(0,1)
            r=fq.run(c,outputs=[fq.density_matrix()],options=e.OPTIONS);RUNS+=1
            v=torch.zeros(4,dtype=D);v[b]=1/math.sqrt(2);v[2+(b^1)]=(-1)**a/math.sqrt(2)
            e.close(r.density_matrix[0],e.outer(v));mats.append(r.density_matrix[0]);vecs.append(v)
    for rank in (1,2,3,4):
        a,out=mixture((1/rank,)*rank,tuple(vecs[:rank]),tuple(mats[:rank]))
        e.close(out['purity'],1/rank)
    print('Four native Bell components:uniform rank-r mixtures have purity1/r for r=1,2,3,4.')
    U=e.prepare(e.qubit(.47,-.82))
    a=e.rho((.36,.64),(e.qubit(.71,.29),e.qubit(1.82,-.53)))
    e.close(diagnostics(U@a@U.mH)['purity'],diagnostics(a)['purity'])
    eps=1e-8;near=torch.diag(torch.tensor([1-eps,eps],dtype=D))
    e.close(diagnostics(near)['purity'],1-2*eps+2*eps**2)
    tiny=torch.diag(torch.tensor([1-1e-20,1e-20],dtype=D))
    assert diagnostics(tiny)['purity']==1.0 and tiny[1,1].real>0
    print('Unitary invariance and near-pure diagnostics passed;rounded purity1 is not an exact rank-one certificate.')
    print(f'{rejected()}malformed contracts rejected;no clipping,normalization repair or exact numerical purity labels.')
    assert RUNS==40
    print('40actual native circuits;host mixture algebra is recorded separately.')


if __name__=='__main__':main()
