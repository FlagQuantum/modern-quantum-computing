"""Section5.5: constructive continuous one-qubit + CNOT universality, small systems."""
import cmath
from math import atan2,pi
from itertools import product
from importlib.metadata import version
import torch
import flagquantum as fq
try:
    from examples.foundations.pauli_rotations import explicit
    from examples.foundations.circuit_composition import execute,product_input
    from examples.foundations.reversible_logic import basis_factors,complex_factors
except ModuleNotFoundError:
    from pauli_rotations import explicit
    from circuit_composition import execute,product_input
    from reversible_logic import basis_factors,complex_factors
D=torch.complex128
I=torch.eye(2,dtype=D)
X=torch.tensor([[0,1],[1,0]],dtype=D)
ATOL=1e-9
RUNS=0


def check_unitary(U,dimension=None):
    if not isinstance(U,torch.Tensor) or U.ndim!=2 or U.shape[0]!=U.shape[1] or U.dtype!=D or U.device.type!='cpu' or U.layout!=torch.strided or not torch.isfinite(U).all():
        raise ValueError('Finite dense square CPUcomplex128 matrix required')
    if dimension is not None and U.shape!=(dimension,dimension):raise ValueError('Declared matrix dimension mismatch')
    if not torch.allclose(U.mH@U,torch.eye(len(U),dtype=D),rtol=0,atol=1e-11):raise ValueError('Unitary input required,no projection')


def zyz(U):
    check_unitary(U,2)
    a,b=U[0].tolist();c,d=U[1].tolist()
    alpha=.5*cmath.phase(a*d-b*c)
    V=cmath.exp(-1j*alpha)*U;a,c=V[0,0].item(),V[1,0].item()
    if abs(c)<=1e-13:beta,gamma,delta=-2*cmath.phase(a),0.,0.
    elif abs(a)<=1e-13:beta,gamma,delta=2*cmath.phase(c),pi,0.
    else:beta,gamma,delta=cmath.phase(c)-cmath.phase(a),2*atan2(abs(c),abs(a)),-cmath.phase(c)-cmath.phase(a)
    rebuilt=cmath.exp(1j*alpha)*explicit('z',beta)@explicit('y',gamma)@explicit('z',delta)
    torch.testing.assert_close(rebuilt,U,rtol=0,atol=1e-11)
    return alpha,beta,gamma,delta


def one(q,U):return [('one',q,U)]


def controlled_one(U,c,t):
    if type(c) is not int or type(t) is not int or min(c,t)<0 or c==t:raise ValueError('Distinct nonnegative control/target required')
    alpha,beta,gamma,delta=zyz(U)
    A=explicit('z',beta)@explicit('y',gamma/2)
    B=explicit('y',-gamma/2)@explicit('z',-(delta+beta)/2)
    C=explicit('z',(delta-beta)/2)
    P=torch.diag(torch.tensor([1,cmath.exp(1j*alpha)],dtype=D))
    return one(t,C)+[('cx',c,t)]+one(t,B)+[('cx',c,t)]+one(t,A)+one(c,P)


def root(U):
    check_unitary(U,2)
    values,Q=torch.linalg.eig(U)
    # For exact unitary U, an orthonormal eigenbasis exists. QR removes floating-point
    # eigenvector overlap; both root identities below are checked,not assumed.
    Q,_=torch.linalg.qr(Q)
    V=Q@torch.diag(torch.exp(.5j*torch.angle(values)))@Q.mH
    check_unitary(V,2)
    torch.testing.assert_close(V@V,U,rtol=0,atol=1e-11)
    return V


def multi(U,controls,target):
    check_unitary(U,2)
    if not isinstance(controls,tuple) or any(type(q) is not int or q<0 for q in controls) or type(target) is not int or target<0 or target in controls or len(set(controls))!=len(controls):
        raise ValueError('Ordered distinct nonnegative support required')
    if len(controls)==0:return one(target,U)
    if len(controls)==1:return controlled_one(U,controls[0],target)
    A,b=controls[:-1],controls[-1];V=root(U)
    return controlled_one(V,b,target)+multi(X,A,b)+controlled_one(V.mH.contiguous(),b,target)+multi(X,A,b)+multi(V,A,target)


def adjacent(U,a,b,n):
    if type(a) is not int or type(b) is not int or not 0<=a<2**n or not 0<=b<2**n or (a^b).bit_count()!=1:raise ValueError('Adjacent distinct n-bit labels required')
    target=n-1-((a^b).bit_length()-1)
    controls=tuple(q for q in range(n) if q!=target)
    zeros=[q for q in controls if ((a>>(n-1-q))&1)==0]
    prefix=[('one',q,X) for q in zeros]
    oriented=U if ((a>>(n-1-target))&1)==0 else X@U@X
    return prefix+multi(oriented,controls,target)+list(reversed(prefix))


def two_level(U,a,b,n):
    check_unitary(U,2)
    if type(n) is not int or not 1<=n<=3 or type(a) is not int or type(b) is not int or a==b or not 0<=a<2**n or not 0<=b<2**n:raise ValueError('Small-register distinct basis labels required')
    path=[a]
    for q in range(n):
        mask=1<<(n-1-q)
        if (a^b)&mask:path.append(path[-1]^mask)
    swaps=[adjacent(X,path[j],path[j+1],n) for j in range(len(path)-2)]
    prefix=[g for block in swaps for g in block]
    # Each adjacent X is a self-inverse operation,although its compiled gate list need not be.
    suffix=[g for block in reversed(swaps) for g in block]
    return prefix+adjacent(U,path[-2],path[-1],n)+suffix


def embedded_two(U,a,b,n):
    M=torch.eye(2**n,dtype=D)
    for i,r in enumerate((a,b)):
        for j,c in enumerate((a,b)):M[r,c]=U[i,j]
    return M


def elimination(U):
    check_unitary(U)
    N=len(U)
    if N not in (2,4,8):raise ValueError('Teaching compiler restricted to1-3qubits')
    M=U.clone();records=[]
    for col in range(N-1):
        for row in range(N-1,col,-1):
            p,q=row-1,row;a,b=M[p,col].item(),M[q,col].item()
            if abs(b)==0:continue
            norm=(abs(a)**2+abs(b)**2)**.5
            G=torch.tensor([[a.conjugate(),b.conjugate()],[-b,a]],dtype=D)/norm
            M[[p,q],:]=G@M[[p,q],:]
            records.append((p,q,G))
    diagonal=torch.diag(torch.exp(1j*torch.angle(torch.diag(M))))
    torch.testing.assert_close(M,diagonal,rtol=0,atol=1e-11)
    return records,diagonal


def compile_unitary(U):
    records,Dmat=elimination(U);n=len(U).bit_length()-1;ops=[]
    for j in range(len(U)):
        local=torch.diag(torch.tensor([Dmat[0,0],1],dtype=D)) if j==0 else torch.diag(torch.tensor([1,Dmat[j,j]],dtype=D))
        ops+=two_level(local,0,1 if j==0 else j,n)
    for a,b,G in reversed(records):ops+=two_level(G.mH.contiguous(),a,b,n)
    return ops


def circuit(ops,n):
    c=fq.Circuit(n,dtype=D)
    for g in ops:
        if g[0]=='one':c.unitary(g[1],unitary=g[2])
        elif g[0]=='cx':c.cx(g[1],g[2])
        else:raise ValueError('Only1qubit gates andCNOT allowed')
    assert all(len(i.wires)==1 or (len(i.wires)==2 and i.name=='cx') for i in c.to_ir().instructions)
    return c


def run(ops,n,factors):
    global RUNS
    v,p=execute(circuit(ops,n),factors);RUNS+=1
    return v,p


def fixture(N,seed):
    g=torch.Generator().manual_seed(seed)
    raw=torch.randn((N,N),generator=g,dtype=torch.float64)+1j*torch.randn((N,N),generator=g,dtype=torch.float64)
    Q,_=torch.linalg.qr(raw)
    return cmath.exp(.37j)*Q


def verify(ops,n,U):
    inputs=[basis_factors(bits) for bits in product((0,1),repeat=n)]+[complex_factors(n)]
    for factors in inputs:
        v,p=run(ops,n,factors)
        torch.testing.assert_close(v,U@product_input(factors),rtol=0,atol=ATOL)


def main():
    assert version('flagquantum')=='0.3.1' and version('torch').split('+')[0]=='2.13.0'
    tests=[I,-I,X,cmath.exp(.39j)*explicit('z',.7)@explicit('y',-.43),fixture(2,55)]
    for U in tests:
        target=embedded_two(U,2,3,2)
        verify(controlled_one(U,0,1),2,target)
    print('5single-control targets includingI,-I,X,complex phase:allbasis andcomplex inputs passed.')
    for U in (X,fixture(2,57)):
        verify(multi(U,(0,1),2),3,embedded_two(U,6,7,3))
    print('2double-control targets:recursive square-root construction checked on all8basis andcomplex input.')
    U=fixture(2,59)
    for a,b in ((0,7),(7,0),(1,6),(5,4)):
        verify(two_level(U,a,b,3),3,embedded_two(U,a,b,3))
    print('4ordered two-level pairs:Gray paths,negative controls and reversed target orientation checked.')
    for N,seed in ((2,61),(4,63),(8,65)):
        U=fixture(N,seed);records,diagonal=elimination(U)
        restored=diagonal.clone()
        for a,b,G in reversed(records):restored=embedded_two(G.mH,a,b,N.bit_length()-1)@restored
        torch.testing.assert_close(restored,U,rtol=0,atol=1e-11)
        ops=compile_unitary(U);verify(ops,N.bit_length()-1,U)
        print(f'{N}x{N}dense unitary:QR reconstruction andallowed-gate circuit passed;{len(ops)}logical gates.')
    for U in (torch.eye(4,dtype=D),cmath.exp(.43j)*torch.eye(4,dtype=D)):
        verify(compile_unitary(U),2,U)
    invalid=[lambda:compile_unitary(2*torch.eye(4,dtype=D)),lambda:compile_unitary(torch.eye(3,dtype=D)),lambda:compile_unitary(torch.eye(16,dtype=D)),lambda:two_level(I,1,1,2),lambda:multi(I,(0,0),1),lambda:multi(I,(0,),0),lambda:controlled_one(I,0,0)]
    for f in invalid:
        try:f()
        except ValueError:pass
        else:raise AssertionError('Malformed synthesis contract admitted')
    assert RUNS==106,RUNS
    print('Identity/global-phase cases and7invalid contracts checked;106actual CPUcomplex128 circuits.')
    print('Numerical fullvector atol1e-9,rtol0;no phasealignment,no native multi-qubit matrix gate or ancilla.')
    print('Constructive existence only;1-3qubit memory guard,not an efficientcompiler or finite-alphabet synthesis claim.')


if __name__=='__main__':main()
