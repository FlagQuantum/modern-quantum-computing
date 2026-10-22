"""6.7: centered finite covariances, native readout groups and estimator uncertainty."""
from fractions import Fraction as F
from math import sin,cos,sqrt,pi,isfinite
from importlib.metadata import version
from itertools import product
import torch
import flagquantum as fq
try:
    from examples.foundations import exact_samples as s
    from examples.foundations import observables as o
except ModuleNotFoundError:
    import exact_samples as s
    import observables as o
D,ATOL=s.D,s.ATOL
R=torch.float64
RUNS=0


def real_table(x):
    if not isinstance(x,torch.Tensor) or x.device.type!='cpu' or x.dtype!=R or x.ndim!=2 or x.shape[0]<1 or x.shape[1]<1 or not torch.isfinite(x).all():
        raise ValueError('Nonempty finite CPU float64 table required')
    return x


def moments(p,values):
    real_table(values)
    if not isinstance(p,torch.Tensor) or p.device.type!='cpu' or p.dtype!=R or p.ndim!=1 or len(p)!=len(values) or not torch.isfinite(p).all() or not bool((p>=0).all()) or abs(p.sum().item()-1)>ATOL:
        raise ValueError('Matching normalized nonnegative CPU float64 probabilities required')
    mean=p@values
    centered=values-mean
    covariance=centered.T@(p[:,None]*centered)
    if not torch.isfinite(mean).all() or not torch.isfinite(covariance).all():raise FloatingPointError('Moment arithmetic overflowed')
    return mean,covariance


def sample_covariance(data):
    real_table(data)
    N=len(data)
    if N<2:raise ValueError('At least two trials required for unbiased sample covariance')
    centered=data-data.mean(dim=0)
    C=centered.T@centered/(N-1)
    if not torch.isfinite(C).all():raise FloatingPointError('Covariance arithmetic overflowed')
    return C


def weighted(C,a):
    real_table(C)
    if C.shape[0]!=C.shape[1] or not torch.allclose(C,C.T,atol=ATOL,rtol=0) or torch.linalg.eigvalsh(C).min().item() < -ATOL:
        raise ValueError('Symmetric positive-semidefinite covariance required')
    if not isinstance(a,torch.Tensor) or a.shape!=(len(C),) or a.dtype!=R or a.device.type!='cpu' or not torch.isfinite(a).all():
        raise ValueError('Matching finite CPU float64 real coefficient vector required')
    value=(a@C@a).item()
    if not isfinite(value):raise FloatingPointError('Weighted covariance overflowed')
    if value<0:raise FloatingPointError('Negative variance residual; no clipping repair')
    return value


def independent_groups(variances,coefficients,shots):
    if not isinstance(variances,tuple) or not isinstance(coefficients,tuple) or not isinstance(shots,tuple) or not len(variances)==len(coefficients)==len(shots) or not variances:
        raise ValueError('Matching nonempty tuples required')
    for v,a,N in zip(variances,coefficients,shots):
        if type(v) not in (int,float) or not isfinite(v) or v<0 or type(a) not in (int,float) or not isfinite(a):raise ValueError('Finite real coefficients and nonnegative variances required')
        s.positive_integer(N)
    value=sum(a*a*v/N for v,a,N in zip(variances,coefficients,shots))
    if not isfinite(value):raise FloatingPointError('Group arithmetic overflowed')
    return value


def native(*args):
    global RUNS
    answer=s.native(*args);RUNS+=1
    return answer


def quantum(theta,phi,a,b):
    global RUNS
    if any(type(x) not in (int,float) or not isfinite(x) for x in (theta,phi,a,b)):raise ValueError('Finite radian angles and real coefficients required')
    block=fq.Circuit(1,dtype=D).ry(0,theta).p(0,phi)
    H=a*fq.X(0)+b*fq.Z(0)
    result=fq.run(block,outputs=[fq.probabilities(),fq.expectation(H,name='H')],options=s.OPTIONS)
    RUNS+=1
    psi=result.statevector()[0]; mu=result.expectation('H')[0].item()
    A=a*o.X+b*o.Z
    centered=(A-mu*o.I)@psi
    variance=torch.vdot(centered,centered).real.item()
    assert abs(mu-(a*sin(theta)*cos(phi)+b*cos(theta)))<ATOL
    assert abs(variance-(a*a+b*b-mu*mu))<ATOL
    eig,V=torch.linalg.eigh(A)
    p=torch.stack([abs(torch.vdot(V[:,j],psi))**2 for j in range(2)])
    mean,C=moments(p,eig[:,None])
    assert abs(mean.item()-mu)<ATOL and abs(C.item()-variance)<ATOL
    return mu,variance


def joint(theta,opposite,N,seed):
    if type(opposite) is not bool:raise ValueError('Declare Boolean parity branch')
    block=fq.Circuit(2,dtype=D).ry(0,theta).cx(0,1)
    if opposite:block.x(1)
    return native(block,(0,1),N,seed)


def invalid_checks():
    p=torch.tensor([.5,.5],dtype=R);v=torch.tensor([[0.],[1.]],dtype=R);eye=torch.eye(2,dtype=R);a=torch.ones(2,dtype=R)
    calls=[lambda:moments(2*p,v),lambda:moments(torch.tensor([-.1,1.1],dtype=R),v),
           lambda:moments(p.float(),v),lambda:moments(p,v.float()),lambda:moments(p,v[None,:]),
           lambda:moments(p,torch.tensor([[0.],[float('nan')]],dtype=R)),
           lambda:sample_covariance(v[:1]),lambda:sample_covariance(v[:0]),
           lambda:weighted(torch.tensor([[1.,2.],[0.,1.]],dtype=R),a),lambda:weighted(-eye,a),
           lambda:weighted(eye,a[:1]),lambda:independent_groups((1.,),(1.,),(0,)),
           lambda:independent_groups((-1.,),(1.,),(2,)),lambda:independent_groups((1.,),(True,),(2,))]
    for call in calls:
        try:call()
        except ValueError:pass
        else:raise AssertionError('Malformed variance contract admitted')
    return len(calls)


def exact_checks():
    # Independent exact rational references; no quantum calls.
    for probabilities,N in [((F(3,4),F(1,4)),4),((F(0),F(1,4),F(3,4),F(0)),3),((F(1,6),F(1,3),F(1,2)),3)]:
        rows=s.ensemble(probabilities,N)
        for j,p in enumerate(probabilities):
            for k,q in enumerate(probabilities):
                centered=sum(w*(f[j]-p)*(f[k]-q) for _,w,f in rows)
                assert centered==((p if j==k else 0)-p*q)/N
        values=tuple(F(2*j-1) for j in range(len(probabilities)))
        mean=sum(p*v for p,v in zip(probabilities,values));var=sum(p*(v-mean)**2 for p,v in zip(probabilities,values))
        expected_sample=F(0)
        expected_var_mean=F(0)
        for seq,w,f in rows:
            obs=[values[j] for j in seq];avg=sum(obs)/N
            sample=sum((x-avg)**2 for x in obs)/(N-1)
            expected_sample+=w*sample
            expected_var_mean+=w*(avg-mean)**2
        assert expected_sample==var and expected_var_mean==var/N
    left=s.ensemble((F(3,4),F(1,4)),2);right=s.ensemble((F(1,3),F(2,3)),3)
    var_joint=F(0)
    mu=2*F(1,4)-3*F(2,3)
    for _,w,f in left:
        for _,z,g in right:var_joint+=w*z*(2*f[1]-3*g[1]-mu)**2
    assert var_joint==4*F(3,16)/2+9*F(2,9)/3
    return 4


def main():
    assert version('flagquantum')=='0.3.1' and version('torch').split('+')[0]=='2.13.0'
    for theta in (0.,pi/2,pi,-.73):
        for phi in (0.,.42,-1.1):quantum(theta,phi,.7,-.4)
    print('12 native expectation circuits: spectral, centered-vector and analytic quantum variances agree.')
    a=torch.tensor([.7,-1.2],dtype=R)
    values=torch.tensor([[1,1],[1,-1],[-1,1],[-1,-1]],dtype=R)
    for theta in (0.,pi/3,pi/2,-.71,pi):
        for opposite in (False,True):
            for seed in (0,13):
                p,bits,_,_=joint(theta,opposite,31,seed)
                mean,C=moments(p,values)
                sign=-1 if opposite else 1
                ref=sin(theta)**2*torch.tensor([[1.,sign],[sign,1.]],dtype=R)
                torch.testing.assert_close(C,ref,atol=ATOL,rtol=0)
                assert abs(weighted(C,a)-(a[0].item()+sign*a[1].item())**2*sin(theta)**2)<ATOL
                data=1.-2.*bits.to(R)
                assert abs(weighted(sample_covariance(data),a)-sample_covariance((data@a)[:,None]).item())<ATOL
    print('20 joint Z-readout circuits: positive/negative within-shot covariance and weighted sample-variance identities passed.')
    for theta in (pi/3,-.47,1.21):
        for selected in ((2,0),(1,2,0)):
            for seed in (5,37):
                p,bits,_,_=native(s.register(theta),selected,23,seed)
                mean,C=moments(p,torch.eye(len(p),dtype=R))
                torch.testing.assert_close(C,torch.diag(p)-torch.outer(p,p),atol=ATOL,rtol=0)
                ids,_,_=s.histogram(bits);data=torch.nn.functional.one_hot(ids,len(p)).to(R)
                coeff=torch.arange(len(p),dtype=R)-.5
                assert abs(weighted(sample_covariance(data),coeff)-sample_covariance((data@coeff)[:,None]).item())<ATOL
    print('12 categorical circuits: exact one-hot covariance and observed weighted-score identities passed with ordered labels.')
    for theta in (.4,1.1,-.8):
        for phi in (.3,.7):
            for setting,N,seed in [('X',17,17),('Z',23,29)]:
                circuit=fq.Circuit(1,dtype=D).ry(0,theta).p(0,phi)
                if setting=='X':circuit.h(0)
                p,bits,_,_=native(circuit,(0,),N,seed)
                mean,C=moments(p,torch.tensor([[1.],[-1.]],dtype=R))
                ref=sin(theta)*cos(phi) if setting=='X' else cos(theta)
                assert abs(mean.item()-ref)<ATOL and abs(C.item()-(1-ref*ref))<ATOL
    print('12 separate X/Z readout circuits: analytic group means and single-shot variances passed; cross-group independence is a declared model.')
    assert exact_checks()==4 and invalid_checks()==14
    mean,C=moments(torch.tensor([.5,.5],dtype=R),torch.tensor([[1e8],[1e8+1]],dtype=R))
    assert C.item()==.25
    assert sample_covariance(torch.zeros((5,1),dtype=R)).item()==0
    assert RUNS==56,RUNS
    print('4 exact rational ensemble families: categorical covariance, unbiased sample variance, variance/N and independent-group addition passed.')
    print('14 malformed contracts rejected; centered large-offset variance .25 retained; a zero observed variance is not a zero-population certificate.')
    print('56 actual CPU complex128 circuit executions; probability/reference atol 1e-12, rtol 0; no confidence-interval or hardware-independence claim.')

if __name__=='__main__':main()
