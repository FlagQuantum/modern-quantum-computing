"""6.9: bounded measurement acceptance with independent references and deliberate failures."""
from dataclasses import replace
from fractions import Fraction as F
from itertools import product
from math import sin,cos,pi,sqrt,isfinite
import cmath,hashlib,json
from importlib.metadata import version
import torch
import flagquantum as fq
try:
    from examples.foundations import projective_born as b
    from examples.foundations import conditional_states as cs
    from examples.foundations import confidence_shots as conf
    from examples.foundations import observables as o
    from examples.foundations.circuit_rewrites import matrix
except ModuleNotFoundError:
    import projective_born as b
    import conditional_states as cs
    import confidence_shots as conf
    import observables as o
    from circuit_rewrites import matrix
D,R,ATOL=b.D,torch.float64,b.ATOL
SELECTED=(2,0)
EPS,DELTA=F(1,4),F(1,5)
RUNS=0
REPORTS={}
RAW={}
I=torch.eye(8,dtype=D)
Y0=torch.kron(torch.kron(o.Y,o.I),o.I)
X0X2=torch.kron(torch.kron(o.X,o.I),o.X)
X2=torch.kron(torch.kron(o.I,o.I),o.X)


def angles(theta,phi):
    if any(type(t) not in (int,float) or not isfinite(t) or abs(t)>100 for t in (theta,phi)):
        raise ValueError('Finite literal radian angles of magnitude<=100 required')


def prepare(theta,phi):
    angles(theta,phi)
    return fq.Circuit(3,dtype=D).ry(0,theta).cx(0,2).x(1).p(0,phi)


def reference(theta,phi):
    angles(theta,phi)
    v=torch.zeros(8,dtype=D)
    v[2]=cos(theta/2);v[7]=cmath.exp(1j*phi)*sin(theta/2)
    return v


def effects():
    # Ordered outcomes x(q2),y(q0); ranks2, spectatorq1 not resolved.
    return tuple((I+(-1)**y*Y0)@(I+(-1)**x*X2)/4 for x,y in product((0,1),repeat=2))


def encode(x):
    if isinstance(x,torch.Tensor):
        if x.is_complex():return dict(real=x.real.tolist(),imag=x.imag.tolist())
        return x.tolist()
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [encode(v) for v in x]
    return x


def fingerprint(payload):
    return hashlib.sha256(json.dumps(encode(payload),sort_keys=True,separators=(',',':')).encode()).hexdigest()


def acquire(theta,phi,variant='correct',N=None,seed=31):
    global RUNS
    angles(theta,phi)
    if variant not in ('correct','wrong-y','outcome-phase'):raise ValueError('Declare a supported lab candidate')
    if N is None:N=conf.budget(F(1),EPS,DELTA)
    conf.s.positive_integer(N)
    if N>10000 or type(seed) is not int or seed<0:raise ValueError('Positive shots<=10000 and literal nonnegative seed required')
    initial_result=fq.run(prepare(theta,phi),outputs=[fq.probabilities()],options=b.OPTIONS);RUNS+=1
    sign=1 if variant=='wrong-y' else -1
    c=prepare(theta,phi).p(0,sign*pi/2).h(0).h(2)
    program=(('p',(0,),(sign*pi/2,)),('h',(0,),()),('h',(2,),()))
    if variant=='outcome-phase':
        c.p(0,.37);program+=(('p',(0,),(.37,)),)
    result=fq.run(c,outputs=[fq.probabilities(qubits=SELECTED),fq.samples(qubits=SELECTED)],shots=N,options=replace(b.OPTIONS,seed=seed));RUNS+=1
    assert initial_result.statevector().shape==result.statevector().shape==(1,8)
    assert result.probabilities.shape==(1,4) and result.samples.shape==(1,N,2)
    ids,counts,_=conf.s.histogram(result.samples[0])
    return dict(theta=theta,phi=phi,variant=variant,selected=SELECTED,N=N,seed=seed,
                variance_bound=F(1),epsilon=EPS,delta=DELTA,
                initial=initial_result.statevector()[0],after=result.statevector()[0],
                p=result.probabilities[0],bits=result.samples[0],counts=counts,
                analyzer=matrix(3,program),program=program,
                ir_sha256=hashlib.sha256(repr(c.to_ir()).encode()).hexdigest())


def close(a,b_):return bool(torch.allclose(a,b_,rtol=0,atol=ATOL))


def audit(payload):
    for key,shape,dtype in [('initial',(8,),D),('after',(8,),D),('p',(4,),R),('counts',(4,),torch.int64)]:
        x=payload[key]
        if not isinstance(x,torch.Tensor) or x.shape!=shape or x.dtype!=dtype or x.device.type!='cpu' or not torch.isfinite(x).all():raise ValueError('Malformed '+key)
    if not isinstance(payload['analyzer'],torch.Tensor) or payload['analyzer'].shape!=(8,8) or payload['analyzer'].dtype!=D or payload['analyzer'].device.type!='cpu' or not torch.isfinite(payload['analyzer']).all():raise ValueError('Malformed analyzer reference')
    ids,raw_counts,_=conf.s.histogram(payload['bits'])
    angles(payload['theta'],payload['phi']);conf.design(payload['epsilon'],payload['delta'])
    conf.exact(payload['variance_bound']);conf.s.positive_integer(payload['N'])
    theta,phi=payload['theta'],payload['phi'];v=payload['initial'];A=payload['analyzer']
    Q,labels=b.marginal_family(3,SELECTED)
    expected=effects();actual=tuple(A.mH@P@A for P in Q)
    C=sin(theta)*sin(phi)
    predicted=torch.tensor([(1+C)/4,(1-C)/4,(1-C)/4,(1+C)/4],dtype=R)
    # No input normalization/phase alignment; operational equivalence is checked by effects.
    checks=dict(initial_model=close(v,reference(theta,phi)),
                normalized=abs(torch.vdot(v,v).item()-1)<ATOL and abs(torch.vdot(payload['after'],payload['after']).item()-1)<ATOL,
                reference_evolution=close(payload['after'],A@v),
                analyzer_unitary=close(A.mH@A,I) and close(A@A.mH,I),
                measurement_effects=all(close(P,Q_) for P,Q_ in zip(actual,expected)),
                probability_model=close(payload['p'],predicted),
                probability_from_effects=close(payload['p'],torch.tensor([torch.vdot(v,P@v).real.item() for P in actual],dtype=R)),
                labels_and_counts=payload['selected']==SELECTED and len(payload['bits'])==payload['N'] and torch.equal(payload['counts'],raw_counts),
                fixed_budget=payload['variance_bound']==F(1) and payload['N']>=conf.budget(F(1),payload['epsilon'],payload['delta']))
    observed=F(sum((-1)**int(k.bit_count()) for k in ids.tolist()),len(ids))
    return dict(accepted=all(checks.values()),checks=checks,candidate_sha256=fingerprint(payload),
                exact_correlation=C,observed_correlation=str(observed),interval_half_width=str(payload['epsilon']),
                interval_contains_toy_target=abs(float(observed)-C)<=float(payload['epsilon']),
                note='Interval membership is a statistical diagnostic,not an implementation acceptance gate. Hash is a fingerprint,not authentication.')


def calibrate(order=SELECTED,words=None):
    global RUNS
    if not isinstance(order,tuple) or sorted(order)!=[0,2]:raise ValueError('This fixture compares ordered q0/q2 selections')
    if words is None:words=tuple(product((0,1),repeat=3))
    passed=[]
    for word in words:
        if not isinstance(word,tuple) or len(word)!=3 or any(type(t) is not int or t not in (0,1) for t in word):raise ValueError('Literal three-bit basis word required')
        c=fq.Circuit(3,dtype=D)
        for q,t in enumerate(word):
            if t:c.x(q)
        r=fq.run(c,outputs=[fq.probabilities(qubits=order)],options=b.OPTIONS);RUNS+=1
        desired=2*word[2]+word[0]
        ref=torch.zeros(4,dtype=R);ref[desired]=1
        passed.append(close(r.probabilities[0],ref))
    return dict(accepted=all(passed),fixtures=len(passed),passed=sum(passed),declared_order=SELECTED,executed_order=order)


def branch_report(v):
    P,labels=b.marginal_family(3,(2,));p,w=cs.branches(v,P,labels)
    # Independent coordinate masks preserve full conditional phase.
    for k,branch in enumerate(w):
        z=torch.tensor([a.item() if (j&1)==k else 0 for j,a in enumerate(v)],dtype=D)
        q=sum(abs(a.item())**2 for a in z)
        if q==0:assert branch is None
        else:assert close(branch,z/sqrt(q))
    table=cs.joint(v,P,labels,P,labels)
    assert close(table,torch.diag(p))
    xx=((I+X0X2)/2,(I-X0X2)/2)
    original=b.born(v,xx,('plus','minus'))
    ignored=cs.joint(v,P,labels,xx,('plus','minus')).sum(0)
    assert abs(ignored[0].item()-.5)<ATOL
    parity=torch.diag(torch.tensor([int(((j>>2)&1)==(j&1)) for j in range(8)],dtype=D))
    pc,wc=cs.branches(v,(parity,I-parity),('even','odd'))
    assert abs(pc[0].item()-1)<ATOL and wc[1] is None and close(wc[0],v)
    return dict(probabilities=p,states=w,xx_original=original,xx_after_forgotten_Z=ignored)


def averaged_branch_fault(v):
    report=branch_report(v)
    # Deliberate wrong proposal: normalize the probability-weighted vector sum.
    # It is NOT used by the accepted branch algorithm.
    z=sum((p*w for p,w in zip(report['probabilities'],report['states']) if w is not None),torch.zeros(8,dtype=D))
    z=z/torch.linalg.vector_norm(z)
    wrong=(1+torch.vdot(z,X0X2@z).real.item())/2
    correct=report['xx_after_forgotten_Z'][0].item()
    return dict(accepted=abs(wrong-correct)<=ATOL,wrong_plus=wrong,correct_plus=correct,
                reason='A normalized average vector still retains false coherence;keep an outcome ensemble.')


def invalid_checks(base):
    bad=dict(base);bad['p']=base['p'].float()
    badshape=dict(base);badshape['initial']=base['initial'][None,:]
    calls=[lambda:prepare(True,.1),lambda:prepare(float('nan'),.1),lambda:prepare(101.,.1),
           lambda:acquire(.3,.4,'missing'),lambda:acquire(.3,.4,N=0),lambda:acquire(.3,.4,seed=True),
           lambda:audit(bad),lambda:audit(badshape),lambda:calibrate((0,0)),
           lambda:calibrate(SELECTED,((0,0,2),))]
    for call in calls:
        try:call()
        except ValueError:pass
        else:raise AssertionError('Malformed lab contract admitted')
    return len(calls)


def save_case(name,payload):
    REPORTS[name]=audit(payload);RAW[name]=encode(payload)
    return REPORTS[name]


def main():
    assert version('flagquantum')=='0.3.1' and version('torch').split('+')[0]=='2.13.0'
    calibration=calibrate();reversed_cal=calibrate((0,2))
    assert calibration['accepted'] and not reversed_cal['accepted']
    print('16 native basis-calibration circuits: all8 intended-order fixtures pass; reversed order fails4 asymmetric fixtures.')
    for theta in (0.,.73,pi/3,pi/2):
        for phi in (0.,pi/3,-.71):
            for variant in ('correct','outcome-phase'):
                payload=acquire(theta,phi,variant)
                assert audit(payload)['accepted']
                branch_report(payload['initial'])
                if theta==pi/3 and phi==pi/3 and variant=='correct':base=payload
    save_case('valid',base)
    print('48 native circuits:24 preparations/readouts over complex/zero-branch inputs and two effect-equivalent analyzers pass; branch/repeatability checks are classical.')
    wrong=acquire(pi/3,pi/3,'wrong-y');wrong_report=save_case('wrong-Y',wrong)
    lucky=acquire(pi/3,0.,'wrong-y');lucky_report=save_case('zero-signal-wrong-Y',lucky)
    short=acquire(pi/3,pi/3,N=4);short_report=save_case('insufficient-shots',short)
    assert not wrong_report['accepted'] and not wrong_report['checks']['measurement_effects']
    assert not lucky_report['accepted'] and lucky_report['checks']['probability_model'] and not lucky_report['checks']['measurement_effects']
    assert not short_report['accepted'] and not short_report['checks']['fixed_budget']
    wrongcount=dict(base);wrongcount['counts']=base['counts'].clone();wrongcount['counts'][0]+=1
    stale=dict(base);stale['phi']=-base['phi']
    understated=dict(base);understated['variance_bound']=F(0)
    for name,payload,flag in [('corrupted-counts',wrongcount,'labels_and_counts'),('stale-phase-source',stale,'initial_model'),('unsupported-variance',understated,'fixed_budget')]:
        report=save_case(name,payload);assert not report['accepted'] and not report['checks'][flag]
    branch_fault=averaged_branch_fault(base['initial']);REPORTS['averaged-branch']=branch_fault
    assert not branch_fault['accepted'] and abs(branch_fault['wrong_plus']-.65)<ATOL
    assert REPORTS['valid']['candidate_sha256']!=REPORTS['wrong-Y']['candidate_sha256']
    assert not REPORTS['wrong-Y']['accepted'] # successful valid candidate never replaces the rejected one
    print('6 more native circuits:wrong-Y,zero-signal wrong-Y and insufficient-shot candidates rejected; exact effect tests expose a probability-only blind spot.')
    print('4 additional classical faults rejected:corrupted counts,stale preparation phase,unsupported variance bound and normalized-vector averaging.')
    assert invalid_checks(base)==10
    assert RUNS==70,RUNS
    print('10 malformed contracts rejected before execution; correct and rejected candidate fingerprints/raw records kept separately.')
    print('70 actual CPU complex128 circuit executions; deterministic atol1e-12,rtol0; interval membership is diagnostic and is not forced to pass.')
    print('Acceptance here is this bounded author-run implementation protocol,not independent scholarly review,hardware validation or a new agent skill.')

if __name__=='__main__':main()
