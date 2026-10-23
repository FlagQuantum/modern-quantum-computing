"""8.5: native reductions versus pure-state Schmidt weights and full spectra."""
import math
from dataclasses import replace
import torch
import flagquantum as fq
try:
    from examples.foundations import partial_trace as t
    from examples.foundations import statistical_ensembles as e
except ModuleNotFoundError:
    import partial_trace as t
    import statistical_ensembles as e
D=e.D;ATOL=1e-12
RUNS=0


def coefficient(v,n,A,B):
    t.selection(n,A);t.selection(n,B)
    if set(A)&set(B)or set(A)|set(B)!=set(range(n)):
        raise ValueError('Ordered disjoint exhaustive bipartition required')
    if (not isinstance(v,torch.Tensor)or v.dtype!=D or v.device.type!='cpu'
        or v.shape!=(2**n,)or not bool(torch.isfinite(v).all())
        or abs(torch.vdot(v,v).item()-1)>ATOL):
        raise ValueError('Finite normalized CPUcomplex128 vector matching register required')
    return torch.tensor([[v[t.lift(i,j,A,B,n)].item()for j in range(2**len(B))]
                        for i in range(2**len(A))],dtype=D)


def schmidt(C):
    if (not isinstance(C,torch.Tensor)or C.dtype!=D or C.device.type!='cpu'
        or C.ndim!=2 or any(not 1<=d<=4 for d in C.shape)
        or not bool(torch.isfinite(C).all())or abs(C.abs().square().sum().item()-1)>ATOL):
        raise ValueError('Finite normalized CPUcomplex128 coefficient matrix with factor dimensions1..4 required')
    U,s,Vh=torch.linalg.svd(C,full_matrices=False)
    B=Vh.T  # conjugate of V,not V
    e.close((U*s)@B.T,C)
    e.close(U.mH@U,torch.eye(len(s),dtype=D));e.close(B.mH@B,torch.eye(len(s),dtype=D))
    return U,s,B


def full_spectrum(s,dimension):
    if (not isinstance(s,torch.Tensor)or s.dtype!=torch.float64 or s.ndim!=1
        or not s.numel()or not bool(torch.isfinite(s).all())or bool((s<0).any())
        or type(dimension)is not int or dimension<len(s)):
        raise ValueError('Finite nonnegative float64 singular values and adequate dimension required')
    return torch.cat((s.square(),torch.zeros(dimension-len(s),dtype=torch.float64))).sort(descending=True).values


def inspect_reductions(C,RA,RB):
    U,s,B=schmidt(C);t.density(RA);t.density(RB)
    if RA.shape!=(C.shape[0],)*2 or RB.shape!=(C.shape[1],)*2:
        raise ValueError('Reduction shapes must match declared coefficient factors')
    e.close(RA,C@C.mH);e.close(RB,C.T@C.conj())
    e.close(RA@U,U*s.square());e.close(RB@B,B*s.square())
    e.close(RA,(U*s.square())@U.mH);e.close(RB,(B*s.square())@B.mH)
    la=torch.linalg.eigvalsh(RA).flip(0);lb=torch.linalg.eigvalsh(RB).flip(0)
    e.close(la,full_spectrum(s,len(RA)));e.close(lb,full_spectrum(s,len(RB)))
    target=s.pow(4).sum();e.close(torch.trace(RA@RA),target);e.close(torch.trace(RB@RB),target)
    return U,s,B,la,lb


def resolved(s,tau):
    full_spectrum(s,len(s))
    if type(tau)not in (int,float)or not math.isfinite(tau)or tau<=0:
        raise ValueError('Finite positive singular-value resolution threshold required')
    return int((s>tau).sum().item())


def run(c,outputs,mode='statevector'):
    global RUNS
    if mode not in ('statevector','density_matrix'):raise ValueError('Declared tested mode required')
    result=fq.run(c,outputs=outputs,options=replace(e.OPTIONS,mode=mode));RUNS+=1
    return result


def query(c,v,cuts,mode='statevector'):
    n=c.n_qubits
    if type(cuts)is not tuple or not cuts:raise ValueError('Nonempty declared cut tuple required')
    requests=[fq.density_matrix(name='full')]
    for j,(A,B)in enumerate(cuts):
        coefficient(v,n,A,B)
        if not A or not B:raise ValueError('Native density requests here require nonempty factors;host handles dimension-one cuts')
        requests += [fq.density_matrix(qubits=A,name='A'+str(j)),fq.density_matrix(qubits=B,name='B'+str(j))]
    requests += [fq.expectation(fq.Y(0),name='y0'),fq.expectation(fq.Y(n-1),name='y_last')]
    if n>1:requests += [fq.expectation(fq.X(0)@fq.X(n-1),name='xx'),fq.expectation(fq.X(0)@fq.Y(n-1),name='xy')]
    result=run(c,requests,mode);full=result.measurement('full').value[0]
    e.close(full,torch.outer(v,v.conj()));t.density(full);e.close(torch.trace(full@full),1)
    data=[]
    for j,(A,Bcut)in enumerate(cuts):
        C=coefficient(v,n,A,Bcut);RA=result.measurement('A'+str(j)).value[0];RB=result.measurement('B'+str(j)).value[0]
        e.close(RA,t.indexed(full,n,A));e.close(RB,t.indexed(full,n,Bcut))
        data.append(inspect_reductions(C,RA,RB))
    e.close(result.expectation('y0')[0],torch.trace(t.indexed(full,n,(0,))@e.Y))
    e.close(result.expectation('y_last')[0],torch.trace(t.indexed(full,n,(n-1,))@e.Y))
    return result,tuple(data)


def pair(theta,phi,alpha=0.,beta=0.,mode='statevector'):
    e.qubit(theta,phi);UA=e.prepare(e.qubit(alpha,.31));UB=e.prepare(e.qubit(beta,-.47))
    c=fq.Circuit(2,dtype=D).RY(0,theta=theta).P(0,theta=phi).CX(0,1)
    c.unitary(0,unitary=UA).unitary(1,unitary=UB)
    diagonal=torch.diag(e.qubit(theta,phi));C=UA@diagonal@UB.T
    result,data=query(c,C.reshape(-1),(((0,),(1,)),),mode)
    target=torch.tensor(sorted((math.cos(theta/2)**2,math.sin(theta/2)**2),reverse=True),dtype=torch.float64)
    e.close(data[0][1].square(),target)
    return result,C,data[0]


def rectangular(theta,phi,mode='statevector'):
    c,v=t.preparation(3,theta,phi)
    return query(c,v,(((2,0),(1,)),((0,),(1,2))),mode)


def spectator(phi,mode='statevector'):
    e.qubit(.73,phi)
    c=fq.Circuit(3,dtype=D).H(0).P(0,theta=phi).CX(0,2).RY(1,theta=.73)
    middle=e.qubit(.73,0.);phase=complex(math.cos(phi),math.sin(phi))
    v=torch.tensor([(middle[t.bits(i,3)[1]].item()*(phase if t.bits(i,3)[0]else 1)/math.sqrt(2)
                    if t.bits(i,3)[0]==t.bits(i,3)[2]else 0)for i in range(8)],dtype=D)
    return query(c,v,(((2,0),(1,)),((0,),(1,2))),mode)


def basis(bits,mode='statevector'):
    c,v=t.preparation(2,0.,0.,kind='basis',basis=bits)
    return query(c,v,(((0,),(1,)),),mode)[0]


def invalid_checks():
    C=torch.diag(torch.tensor([1,0],dtype=D));v=torch.tensor([1,0,0,0],dtype=D)
    calls=[lambda:schmidt(2*C),lambda:schmidt(torch.zeros_like(C)),lambda:schmidt(C.real),
      lambda:schmidt(torch.full_like(C,complex('nan'))),lambda:schmidt(torch.ones((5,1),dtype=D)/math.sqrt(5)),
      lambda:coefficient(v,2,(0,),(0,)),lambda:coefficient(v,2,(0,),()),
      lambda:coefficient(v,2,(True,),(1,)),lambda:coefficient(2*v,2,(0,),(1,)),
      lambda:resolved(torch.tensor([1.],dtype=torch.float64),0.),
      lambda:full_spectrum(torch.tensor([-1.],dtype=torch.float64),1),
      lambda:full_spectrum(torch.tensor([1.,0.],dtype=torch.float64),1)]
    for call in calls:
        try:call()
        except ValueError:pass
        else:raise AssertionError('Malformed Schmidt/reduction contract accepted')
    # Dimension-one factors and rectangular zero padding are host algebra,not empty native requests.
    for C in (torch.tensor([[1,1j,0,0]],dtype=D)/math.sqrt(2),torch.tensor([[1],[1j],[0],[0]],dtype=D)/math.sqrt(2)):
        inspect_reductions(C,C@C.mH,C.T@C.conj())
    return len(calls)


def main():
    for mode in ('statevector','density_matrix'):
        for theta in (.31,math.pi/2,2.2):
            for phi in (0.,.71):
                for alpha,beta in ((0.,0.),(.63,-.82)):
                    pair(theta,phi,alpha,beta,mode)
    print('24 native rotated/unrotated pairs:Schmidt squares,eigenpair residuals,full marginal spectra and purities passed.')
    for mode in ('statevector','density_matrix'):
        for theta,phi in ((.76,-.58),(1.28,.42)):
            result,data=rectangular(theta,phi,mode)
            assert result.measurement('A0').value.shape==(1,4,4)and result.measurement('B0').value.shape==(1,2,2)
    print('4 native complex three-qubit circuits:4x2and2x4coefficient matrices retain unequal zero complements.')
    for mode in ('statevector','density_matrix'):
        for phi in (0.,.43,-.91):
            result,data=spectator(phi,mode)
            e.close(data[0][1].square(),torch.tensor([1.,0.],dtype=torch.float64))
            e.close(data[1][1].square(),torch.tensor([.5,.5],dtype=torch.float64))
    print('6 native spectator-pair circuits:partition changes spectra;internal tuple reordering only changes coordinates.')
    for mode in ('statevector','density_matrix'):
        for eps in (0.,1e-10):
            result,C,data=pair(2*math.asin(eps),.37,mode=mode)
            s=data[1];assert abs(s[1].item()-eps)<1e-20
            if eps:
                tiny=result.measurement('A0').value[0,1,1].real.item()
                assert tiny>0 and abs(tiny-eps**2)<1e-30
                assert resolved(s,1e-9)==1and resolved(s,1e-12)==2
    print('4 native near-product cases:positive1e-20weight retained;singular-value threshold is a resolution diagnostic.')
    for mode in ('statevector','density_matrix'):
        a,b,c=(basis(bits,mode)for bits in ((0,0),(1,1),(1,0)))
        rho=.5*a.measurement('full').value[0]+.5*b.measurement('full').value[0]
        e.close(t.indexed(rho,2,(0,)),e.I/2);e.close(t.indexed(rho,2,(1,)),e.I/2)
        e.close(torch.trace(rho@rho),.5)
        product=.5*a.measurement('full').value[0]+.5*c.measurement('full').value[0]
        e.close(t.indexed(product,2,(0,)),e.I/2);e.close(t.indexed(product,2,(1,)),torch.diag(torch.tensor([1,0],dtype=D)))
    print('6 native product components:host mixed counterexamples show why global purity is an essential hypothesis.')
    print(f'{invalid_checks()} malformed contracts rejected;host dimension-one spectra and all computed singular values retained.')
    assert RUNS==44
    print('44 actual native circuits;SVD,eigenspectra,purities and mixed ensemble sums are explicit host calculations.')


if __name__=='__main__':main()
