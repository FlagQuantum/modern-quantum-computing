"""8.4: partial trace from indexed local expectations and native selected densities."""
import itertools,math
from dataclasses import replace
import torch
import flagquantum as fq
try:
    from examples.foundations import statistical_ensembles as e
except ModuleNotFoundError:
    import statistical_ensembles as e
D=e.D;ATOL=1e-12
RUNS=0


def matrix(M):
    if (not isinstance(M,torch.Tensor)or M.dtype!=D or M.device.type!='cpu'
        or M.layout!=torch.strided or M.ndim!=2 or M.shape[0]!=M.shape[1]
        or not 1<=M.shape[0]<=16 or not bool(torch.isfinite(M).all())):
        raise ValueError('Finite dense square CPUcomplex128 matrix,dimension1..16 required')
    return M


def density(M):
    matrix(M)
    if (not torch.allclose(M,M.mH,atol=ATOL,rtol=0)
        or abs(torch.trace(M).item()-1)>ATOL or torch.linalg.eigvalsh(M).min().item() < -ATOL):
        raise ValueError('Numerically positive Hermitian unit-trace density required;no repair')
    return M


def trace_ab(M,dA,dB):
    matrix(M)
    if any(type(d)is not int or d<1 for d in (dA,dB))or dA*dB!=len(M):
        raise ValueError('Positive integer factor dimensions matching matrix required')
    return torch.tensor([[sum(M[i*dB+mu,j*dB+mu].item()for mu in range(dB))
                          for j in range(dA)]for i in range(dA)],dtype=D)


def selection(n,keep):
    if (type(n)is not int or not 1<=n<=4 or type(keep)is not tuple
        or any(type(q)is not int or not 0<=q<n for q in keep)or len(set(keep))!=len(keep)):
        raise ValueError('Ordered distinct in-range qubit tuple on1..4qubits required')
    return tuple(q for q in range(n)if q not in keep)


def bits(index,width):return tuple((index>>(width-1-q))&1 for q in range(width))


def lift(i,mu,keep,rest,n):
    full=[0]*n
    for q,b in zip(keep,bits(i,len(keep))):full[q]=b
    for q,b in zip(rest,bits(mu,len(rest))):full[q]=b
    return sum(b<<(n-1-q)for q,b in enumerate(full))


def indexed(M,n,keep):
    matrix(M);rest=selection(n,keep)
    if len(M)!=2**n:raise ValueError('Matrix dimension must match declared register')
    da,db=2**len(keep),2**len(rest)
    return torch.tensor([[sum(M[lift(i,mu,keep,rest,n),lift(j,mu,keep,rest,n)].item()
        for mu in range(db))for j in range(da)]for i in range(da)],dtype=D)


def axes(M,n,keep):
    matrix(M);rest=selection(n,keep)
    if len(M)!=2**n:raise ValueError('Matrix dimension must match register')
    order=keep+rest+tuple(n+q for q in keep)+tuple(n+q for q in rest)
    tensor=M.reshape((2,)*(2*n)).permute(order)
    tensor=tensor.reshape(2**len(keep),2**len(rest),2**len(keep),2**len(rest))
    return torch.einsum('imjm->ij',tensor)


def coefficient(v,n,keep):
    rest=selection(n,keep)
    if not isinstance(v,torch.Tensor)or v.dtype!=D or v.shape!=(2**n,):raise ValueError('Matching complex vector required')
    C=torch.tensor([[v[lift(i,mu,keep,rest,n)].item()for mu in range(2**len(rest))]
                    for i in range(2**len(keep))],dtype=D)
    return C@C.mH


def embed(A,n,keep):
    matrix(A);rest=selection(n,keep)
    if len(A)!=2**len(keep):raise ValueError('Observable dimension must match retained tuple')
    out=torch.zeros((2**n,)*2,dtype=D)
    for i in range(len(A)):
        for j in range(len(A)):
            for mu in range(2**len(rest)):
                out[lift(i,mu,keep,rest,n),lift(j,mu,keep,rest,n)]=A[i,j]
    return out


def reconstruct(M,n,keep):
    """dA-squared Hermitian observable means fix all entries,including imaginary sign."""
    rest=selection(n,keep);da=2**len(keep);out=torch.zeros((da,da),dtype=D)
    def local_mean(A):return torch.trace(M@embed(A,n,keep)).real.item()
    for i in range(da):
        E=torch.zeros_like(out);E[i,i]=1;out[i,i]=local_mean(E)
        for j in range(i+1,da):
            X=torch.zeros_like(out);X[i,j]=X[j,i]=1
            Y=torch.zeros_like(out);Y[i,j]=-1j;Y[j,i]=1j
            out[i,j]=(local_mean(X)-1j*local_mean(Y))/2;out[j,i]=out[i,j].conj()
    return out


def preparation(n,theta,phi,kind='chain',basis=None,rotate_last=None):
    selection(n,());e.qubit(theta,phi)
    c=fq.Circuit(n,dtype=D)
    if kind=='basis':
        if type(basis)is not tuple or len(basis)!=n or any(type(b)is not int or b not in (0,1)for b in basis):
            raise ValueError('One integer bit per qubit required')
        v=torch.zeros(2**n,dtype=D);v[sum(b<<(n-1-q)for q,b in enumerate(basis))]=1
        for q,b in enumerate(basis):
            if b:c.X(q)
    elif kind=='bell':
        if n!=2:raise ValueError('Two-qubit Bell-family helper required')
        c.RY(0,theta=theta).P(0,theta=phi).CX(0,1)
        a,b=e.qubit(theta,phi);v=torch.stack((a,a*0,a*0,b))
    elif kind in ('product','chain'):
        factors=[e.qubit(theta+.23*q,phi-.17*q)for q in range(n)]
        v=torch.tensor([math.prod(factors[q][b].item()for q,b in enumerate(bits(i,n)))for i in range(2**n)],dtype=D)
        for q in range(n):c.RY(q,theta=theta+.23*q).P(q,theta=phi-.17*q)
        if kind=='chain':
            for q in range(n-1):
                c.CX(q,q+1);out=torch.empty_like(v)
                for i in range(len(v)):
                    target=i^((1<<(n-2-q))if bits(i,n)[q]else 0);out[target]=v[i]
                v=out
            if n>1:
                c.CZ(0,n-1)
                v=torch.tensor([(-a if bits(i,n)[0]and bits(i,n)[-1]else a)for i,a in enumerate(v)],dtype=D)
    else:raise ValueError('Declared preparation family required')
    if rotate_last is not None:
        e.matrix(rotate_last);e.close(rotate_last.mH@rotate_last,e.I)
        c.unitary(n-1,unitary=rotate_last.contiguous());v=embed(rotate_last,n,(n-1,))@v
    return c,v


def run(c,outputs,mode='statevector'):
    global RUNS
    if mode not in ('statevector','density_matrix'):raise ValueError('Declared tested mode required')
    result=fq.run(c,outputs=outputs,options=replace(e.OPTIONS,mode=mode));RUNS+=1
    return result


def supports(n):return tuple(s for k in range(1,n+1)for s in itertools.permutations(range(n),k))


def key(keep):return 'r_'+'_'.join(map(str,keep))


def native(n,theta,phi,kind='chain',basis=None,rotate_last=None,mode='statevector',keeps=None):
    c,v=preparation(n,theta,phi,kind,basis,rotate_last)
    keeps=supports(n)if keeps is None else keeps
    if type(keeps)is not tuple or not keeps:raise ValueError('Nonempty tuple of native selections required')
    for s in keeps:
        selection(n,s)
        if not s:raise ValueError('Empty native selection is not mathematical trace-all;use host indexed')
    if len(set(keeps))!=len(keeps):raise ValueError('Distinct native output labels required')
    outputs=[fq.density_matrix(name='full')]
    for s in keeps:outputs += [fq.density_matrix(qubits=s,name=key(s)),fq.probabilities(qubits=s,name='p_'+key(s))]
    outputs += [fq.expectation(fq.Z(q),name='z'+str(q))for q in range(n)]
    outputs += [fq.expectation(fq.Y(0),name='y0')]
    if n>1:outputs += [fq.expectation(fq.X(0)@fq.X(n-1),name='xx'),fq.expectation(fq.X(0)@fq.Y(n-1),name='xy')]
    result=run(c,outputs,mode);full=result.measurement('full').value[0]
    e.close(full,torch.outer(v,v.conj()));density(full)
    for s in keeps:
        R=result.measurement(key(s)).value[0]
        e.close(R,indexed(full,n,s));e.close(R,axes(full,n,s));e.close(R,coefficient(v,n,s));e.close(R,reconstruct(full,n,s))
        density(R);e.close(R.diagonal().real,result.measurement('p_'+key(s)).value[0])
    for q in range(n):e.close(result.expectation('z'+str(q))[0],torch.trace(indexed(full,n,(q,))@e.Z))
    e.close(result.expectation('y0')[0],torch.trace(indexed(full,n,(0,))@e.Y))
    if n>1:
        local=indexed(full,n,(0,n-1))
        for label,A in (('xx',torch.kron(e.X,e.X)),('xy',torch.kron(e.X,e.Y))):
            e.close(result.expectation(label)[0],torch.trace(local@A))
    return result,v


def invalid_checks():
    M=torch.eye(4,dtype=D)/4
    calls=[lambda:trace_ab(M,3,2),lambda:trace_ab(M,True,4),lambda:trace_ab(M,2,0),
      lambda:indexed(M,2,(0,0)),lambda:indexed(M,2,(2,)),lambda:indexed(M,2,(True,)),
      lambda:indexed(M,2,[0]),lambda:indexed(M,3,(0,)),lambda:indexed(M.real,2,(0,)),
      lambda:indexed(torch.full_like(M,complex('nan')),2,(0,)),lambda:selection(5,()),
      lambda:embed(torch.eye(4,dtype=D),2,(0,)),lambda:density(2*M),
      lambda:density(torch.diag(torch.tensor([1.2,-.2],dtype=D)))]
    for call in calls:
        try:call()
        except ValueError:pass
        else:raise AssertionError('Malformed partial-trace contract accepted')
    e.close(indexed(M,2,()),torch.ones((1,1),dtype=D));e.close(indexed(M,2,(0,1)),M)
    # The linear partial trace does not normalize unnormalized operators.
    e.close(indexed(3*M,2,()),torch.tensor([[3]],dtype=D))
    return len(calls)


def main():
    selected_outputs=0
    for mode in ('statevector','density_matrix'):
        for n in (2,3):
            for basis in itertools.product((0,1),repeat=n):
                native(n,0.,0.,kind='basis',basis=basis,mode=mode);selected_outputs+=len(supports(n))
    print('24 native basis circuits:all nonempty ordered two/three-qubit selections match scalar sums and paired-axis traces.')
    mixtures=[]
    for mode in ('statevector','density_matrix'):
        for n in (2,3):
            pair=[]
            for kind in ('product','chain'):
                for theta,phi in ((.83,-.49),(1.31,.72)):
                    r,v=native(n,theta,phi,kind=kind,mode=mode);selected_outputs+=len(supports(n));pair.append(r)
            full=.37*pair[1].measurement('full').value[0]+.63*pair[3].measurement('full').value[0]
            for s in supports(n):
                R=.37*pair[1].measurement(key(s)).value[0]+.63*pair[3].measurement(key(s)).value[0]
                e.close(R,indexed(full,n,s));e.close(R,reconstruct(full,n,s))
            mixtures.append(full)
    print('16 native complex product/chain circuits:entry/axis/coefficient/observable-frame references and host mixed reductions passed.')
    for mode in ('statevector','density_matrix'):
        for theta,phi in ((math.pi/2,0.),(math.pi/2,math.pi/2),(.72,-.31)):
            native(2,theta,phi,kind='bell',mode=mode);selected_outputs+=len(supports(2))
    print('6 native Bell-family circuits:reduced states and phase-sensitive global Pauli correlations passed.')
    U=e.prepare(e.qubit(.63,.27))
    for mode in ('statevector','density_matrix'):
        before,_=native(2,.91,-.36,mode=mode);after,_=native(2,.91,-.36,rotate_last=U,mode=mode)
        selected_outputs+=2*len(supports(2))
        e.close(before.measurement('r_0').value,after.measurement('r_0').value)
        full=before.measurement('full').value[0];B=torch.kron(e.I,U)
        e.close(indexed(B.mH@full@B,2,(0,)),indexed(full,2,(0,)))
    print('4 native discarded-subsystem rotations:retained density invariant,including passive basis contraction.')
    general=torch.diag(torch.tensor([.1,.2,.1,.3,.2,.1],dtype=D))
    e.close(trace_ab(general,3,2),torch.diag(torch.tensor([.3,.4,.3],dtype=D)))
    e.close(trace_ab(general,1,6),torch.ones((1,1),dtype=D));e.close(trace_ab(general,6,1),general)
    print(f'{invalid_checks()} malformed contracts rejected;dimension-one/empty/full and unnormalized linear traces passed.')
    assert RUNS==50 and selected_outputs==464
    print('50 actual native circuits;464 selected-density outputs;classical probes and host mixtures are not extra quantum executions.')


if __name__=='__main__':main()
