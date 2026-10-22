"""6.8: exact design arithmetic, conservative coverage, and native terminal samples."""
from fractions import Fraction as F
from math import comb,pi,sin,cos,sqrt
from importlib.metadata import version
import torch
import flagquantum as fq
try:
    from examples.foundations import exact_samples as s
except ModuleNotFoundError:
    import exact_samples as s
D,ATOL=s.D,s.ATOL
RUNS=0


def exact(x):
    if type(x) is not F:raise ValueError('Declare exact Fraction design inputs; floats and Booleans rejected')
    return x


def design(epsilon,delta):
    exact(epsilon);exact(delta)
    if epsilon<=0 or not 0<delta<1:raise ValueError('Positive epsilon and failure probability0<delta<1 required')


def budget(variance_bound,epsilon,delta):
    exact(variance_bound);design(epsilon,delta)
    if variance_bound<0:raise ValueError('Nonnegative certified single-trial variance upper bound required')
    q=variance_bound/(delta*epsilon**2)
    return max(1,(q.numerator+q.denominator-1)//q.denominator)


def range_variance(lower,upper):
    exact(lower);exact(upper)
    if lower>upper:raise ValueError('Ordered score range required')
    return (upper-lower)**2/4


def binomial_rows(p,N):
    exact(p);s.positive_integer(N)
    if not 0<=p<=1:raise ValueError('Bernoulli probability in[0,1] required')
    if N>1000:raise ValueError('Exact binomial teaching guard:N<=1000')
    rows=tuple((k,F(comb(N,k))*p**k*(1-p)**(N-k)) for k in range(N+1))
    assert sum(w for _,w in rows)==1
    return rows


def coverage(p,N,epsilon):
    exact(epsilon)
    if epsilon<=0:raise ValueError('Positive fixed half-width required')
    return sum((w for k,w in binomial_rows(p,N) if abs(F(k,N)-p)<=epsilon),start=F(0))


def plugin_coverage(p,N,delta):
    """Deliberately unsupported plug-in method: exact counterexample, not a valid CI constructor."""
    exact(delta)
    if not 0<delta<1 or type(N) is not int or N<2:raise ValueError('N>=2 and0<delta<1 required')
    return sum((w for k,w in binomial_rows(p,N)
                if (F(k,N)-p)**2<=F(k,N)*(1-F(k,N))/((N-1)*delta)),start=F(0))


def native(circuit,selected,N,seed):
    global RUNS
    s.positive_integer(N)
    if N>10000:raise ValueError('Teaching execution guard:N<=10000')
    answer=s.native(circuit,selected,N,seed);RUNS+=1
    return answer


def invalid_checks():
    calls=[lambda:budget(F(-1),F(1,10),F(1,20)),lambda:budget(F(1),F(0),F(1,20)),
           lambda:budget(F(1),F(1,10),F(0)),lambda:budget(F(1),F(1,10),F(1)),
           lambda:budget(.25,F(1,10),F(1,20)),lambda:budget(F(1),F(1,10),.05),
           lambda:range_variance(F(2),F(1)),lambda:range_variance(False,F(1)),
           lambda:coverage(F(-1,10),5,F(1,10)),lambda:coverage(F(1,2),True,F(1,10)),
           lambda:coverage(F(1,2),1001,F(1,10)),lambda:coverage(F(1,2),5,F(0)),
           lambda:plugin_coverage(F(1,2),1,F(1,20)),
           lambda:native(fq.Circuit(1,dtype=D),(0,),10001,0)]
    for call in calls:
        try:call()
        except ValueError:pass
        else:raise AssertionError('Malformed coverage contract admitted')
    return len(calls)


def exact_checks():
    for var,e,delta in [(F(1,4),F(1,10),F(1,20)),(F(1),F(1,5),F(1,10)),(F(0),F(1,7),F(1,100)),(F(2,3),F(2,7),F(3,20))]:
        N=budget(var,e,delta)
        assert var/N/e**2<=delta
        if N>1:assert var/(N-1)/e**2>delta
    for p in (F(0),F(1,10),F(1,4),F(1,2),F(9,10),F(1)):
        assert coverage(p,500,F(1,10))>=F(19,20)
    assert coverage(F(1,10),5,F(1,10))==F(45927,50000)
    assert coverage(F(1,10),6,F(1,10))==F(177147,200000)
    assert plugin_coverage(F(1,10),5,F(1,20))==F(819,2000)
    # Exact simultaneous categorical coverage at a small test design.
    probabilities=(F(1,4),F(1,2),F(1,4));eps=F(2,5)
    rows=s.ensemble(probabilities,5)
    simultaneous=sum((w for _,w,f in rows if all(abs(x-p)<=eps for x,p in zip(f,probabilities))),start=F(0))
    assert 0<=simultaneous<=1
    # A first-success-or-two-trial stop changes the sample mean target.
    assert F(1,2)*1+F(1,4)*F(1,2)+F(1,4)*0==F(5,8)
    return simultaneous


def main():
    assert version('flagquantum')=='0.3.1' and version('torch').split('+')[0]=='2.13.0'
    designs=[(F(1,4),F(1,5)),(F(1,5),F(1,10)),(F(1,10),F(1,20))]
    for theta in (0.,pi/3,pi/2,pi):
        for e,delta in designs:
            N=budget(F(1,4),e,delta)
            for seed in (3,41):
                p,bits,c,f=native(fq.Circuit(1,dtype=D).ry(0,theta),(0,),N,seed)
                assert abs(p[1].item()-sin(theta/2)**2)<ATOL
                assert F(c[1].item(),N)==F(int(bits[:,0].sum().item()),N)
                # No assertion that a single random confidence interval must cover.
    print('24 native Bernoulli circuits: three conservative fixed designs, four preparations and two seeds; exact accounting, not single-record coverage assertions.')
    for theta in (0.,pi/3,pi/2,-.71):
        for phi in (0.,.71):
            N=budget(range_variance(F(-1),F(1)),F(1,5),F(1,10))
            circuit=fq.Circuit(1,dtype=D).ry(0,theta).p(0,phi).h(0)
            p,bits,_,_=native(circuit,(0,),N,13)
            assert abs(p[0].item()-p[1].item()-sin(theta)*cos(phi))<ATOL
            assert len(bits)==250
    print('8 native X-readout circuits: score-range bound1 and250-shot design checked against analytic means.')
    for theta in (pi/3,-.73,pi/2):
        for selected in ((2,0),(1,2,0)):
            K=2**len(selected);e,delta=F(1,4),F(1,5)
            N=budget(F(1,4),e,delta/K)
            assert K*F(1,4)/N/e**2<=delta
            for seed in (7,29):
                p,bits,c,f=native(s.register(theta),selected,N,seed)
                assert c.sum()==N and len(f)==K
    print('12 ordered categorical circuits: shared records and union-bound failure allocation checked without assuming independent label counts.')
    N=budget(F(13,20),F(1,5),F(1,10))
    for setting,seed in [('X',17),('Z',53)]:
        c=fq.Circuit(1,dtype=D).ry(0,.83).p(0,-.61)
        if setting=='X':c.h(0)
        p,bits,_,_=native(c,(0,),N,seed)
        assert len(bits)==163
    simultaneous=exact_checks()
    assert invalid_checks()==14 and RUNS==46,RUNS
    print('2 separate X/Z circuits: fixed163shots per independent group; coefficient-square variance bound13/20 is a declared model bound.')
    print('Exact binomial coverage at p=.1,half-width=.1: N5=.91854,N6=.885735; conservative N500 meets>=.95 at six exact test probabilities.')
    print('Unsupported sample-variance plug-in at p=.1,N5,nominal95% has exact coverage .4095; early-stop mean target5/8 differs from1/2.')
    print('Exact simultaneous three-category fixture:',str(simultaneous),'; 14 malformed contracts rejected.')
    print('46 actual CPU complex128 circuit executions; atol1e-12,rtol0 for deterministic probability references; no hardware, posterior or optional-stopping guarantee.')

if __name__=='__main__':main()
