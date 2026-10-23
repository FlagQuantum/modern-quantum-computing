"""8.3: native expectations/premeasurement outputs and explicit host density updates."""
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
I=e.I;X=e.X;Y=e.Y;Z=e.Z
H=.7*X-.2*Y+1.3*Z
P0=torch.diag(torch.tensor([1,0],dtype=D))
P1=I-P0
Z_GROUPS=((P0,),(P1,))
HAD=torch.tensor([[1,1],[1,-1]],dtype=D)/math.sqrt(2)


def run(c,outputs,mode='statevector'):
    global RUNS
    if mode not in ('statevector','density_matrix'):
        raise ValueError('Declared tested execution mode required')
    result=fq.run(c,outputs=outputs,options=replace(e.OPTIONS,mode=mode))
    RUNS+=1
    return result


def mean(rho,A):
    e.density(rho);e.hermitian(A)
    if rho.shape!=A.shape:raise ValueError('Observable dimension must match density')
    answer=torch.trace(rho@A)
    if abs(answer.imag.item())>ATOL:raise ArithmeticError('Non-real mean residual')
    return answer.real.item()


def native(v,mode='statevector'):
    e.state(v)
    if len(v)!=2:raise ValueError('Single-qubit native input helper required')
    c=fq.Circuit(1,dtype=D).unitary(0,unitary=e.prepare(v))
    result=run(c,[fq.density_matrix(),fq.probabilities(),
        fq.expectation(fq.X(0),name='x'),fq.expectation(fq.Y(0),name='y'),
        fq.expectation(fq.Z(0),name='z'),
        fq.expectation(.7*fq.X(0)-.2*fq.Y(0)+1.3*fq.Z(0),name='h')],mode)
    e.close(result.density_matrix[0],e.outer(v))
    e.close(result.probabilities[0],v.abs().square())
    for label,A in (('x',X),('y',Y),('z',Z),('h',H)):
        e.close(result.expectation(label)[0],mean(result.density_matrix[0],A))
        e.close(result.expectation(label)[0],e.born((1.,),(v,),(A+2*I)/4)*4-2
                if label=='h' else torch.vdot(v,A@v))
    return result


def family(groups,d):
    if (type(groups)is not tuple or not groups
            or any(type(g)is not tuple or not g for g in groups)):
        raise ValueError('Nonempty tuple of nonempty outcome groups required')
    eye=torch.eye(d,dtype=D);effects=[]
    for group in groups:
        effect=torch.zeros_like(eye)
        for K in group:
            e.matrix(K)
            if K.shape!=(d,d):raise ValueError('Operator dimensions must match input')
            effect+=K.mH@K
        effects.append(effect)
    if not torch.allclose(sum(effects,torch.zeros_like(eye)),eye,atol=ATOL,rtol=0):
        raise ValueError('Complete instrument required;no rescaling repair')
    return tuple(effects)


def instrument(rho,groups):
    """Host update. Zero-probability outcome returns None,never a guessed state."""
    e.density(rho);effects=family(groups,len(rho))
    sigmas=[];probabilities=[];states=[]
    for group,E in zip(groups,effects):
        left=[K@rho for K in group]
        sigma=sum((A@K.mH for A,K in zip(left,group)),torch.zeros_like(rho))
        raw=torch.trace(sigma)
        if abs(raw.imag.item())>ATOL or raw.real.item()<0:
            raise ArithmeticError('Non-real/negative branch probability;no clipping')
        p=raw.real.item()
        e.close(raw,torch.trace(rho@E))
        if p==0:
            if bool((sigma!=0).any()) or any(bool((A!=0).any()) for A in left):
                raise FloatingPointError('Nonzero branch factors with zero trace:underflow/cancellation,not an impossible event')
            selected=None
        else:
            selected=sigma/p;e.density(selected)
        sigmas.append(sigma);probabilities.append(p);states.append(selected)
    e.close(sum(probabilities),1)
    ignored=sum(sigmas,torch.zeros_like(rho));e.density(ignored)
    return tuple(probabilities),tuple(states),tuple(sigmas),ignored


def scalar_branches(weights,vectors,groups):
    """Independent finite sums over component amplitudes,not K rho K-dagger."""
    e.ensemble(weights,vectors);family(groups,len(vectors[0]));d=len(vectors[0])
    sigmas=[]
    for group in groups:
        out=torch.zeros((d,d),dtype=D)
        for weight,v in zip(weights,vectors):
            for K in group:
                w=[sum(K[a,b].item()*v[b].item() for b in range(d)) for a in range(d)]
                for a in range(d):
                    for b in range(d):out[a,b]+=weight*w[a]*w[b].conjugate()
        sigmas.append(out)
    return tuple(sigmas)


def weak(strength,flip=False):
    if (type(strength)not in (int,float) or not math.isfinite(strength)
            or not 0<=strength<=1 or type(flip)is not bool):
        raise ValueError('Finite dimensionless strength in[0,1] and Boolean flip required')
    a,b=math.sqrt((1+strength)/2),math.sqrt((1-strength)/2)
    M0=torch.diag(torch.tensor([a,b],dtype=D))
    M1=torch.diag(torch.tensor([b,a],dtype=D))
    return ((M0,),((X@M1)if flip else M1,))


def coupled(v,strength,flip=False,analyzer=False,mode='statevector'):
    """Native unitary premeasurement;host extraction of diagonal meter blocks."""
    e.state(v)
    if len(v)!=2 or type(analyzer)is not bool:raise ValueError('Single input and Boolean analyzer required')
    groups=weak(strength,flip)
    a,b=math.sqrt((1+strength)/2),math.sqrt((1-strength)/2)
    c=fq.Circuit(2,dtype=D).unitary(0,unitary=e.prepare(v))
    c.RY(1,theta=2*math.acos(a))
    c.CRY(0,1,theta=2*math.acos(b)-2*math.acos(a))
    if flip:c.CX(1,0)
    if analyzer:c.H(0)
    result=run(c,[fq.density_matrix(),fq.probabilities(qubits=(1,),name='record'),
        fq.probabilities(qubits=(1,0),name='record-readout'),
        fq.expectation(fq.X(0),name='x'),fq.expectation(fq.Z(0),name='z')],mode)
    joint=result.density_matrix[0];target=torch.zeros(4,dtype=D)
    for r,group in enumerate(groups):
        target[r::2]=(HAD if analyzer else I)@(group[0]@v)
    e.close(joint,e.outer(target))
    probs,states,sigmas,ignored=instrument(e.outer(v),groups)
    readout=result.measurement('record-readout').value[0].reshape(2,2)
    e.close(result.measurement('record').value[0],probs)
    blocks=[]
    for r in range(2):
        idx=torch.tensor([r,2+r]);block=joint[idx][:,idx];blocks.append(block)
        expected=HAD@sigmas[r]@HAD if analyzer else sigmas[r]
        e.close(block,expected);e.close(readout[r],expected.diagonal().real)
    for label,A in (('x',X),('z',Z)):
        output=HAD@ignored@HAD if analyzer else ignored
        e.close(result.expectation(label)[0],mean(output,A))
    return result,tuple(blocks),readout


def bell(theta,phi,mode='statevector'):
    v=e.qubit(theta,phi)
    c=fq.Circuit(2,dtype=D).RY(0,theta=theta).P(0,theta=phi).CX(0,1)
    result=run(c,[fq.density_matrix(),fq.probabilities(),
        fq.expectation(fq.X(0)@fq.X(1),name='xx'),
        fq.expectation(fq.X(0)@fq.Y(1),name='xy')],mode)
    full=torch.stack((v[0],v[0]*0,v[0]*0,v[1]))
    e.close(result.density_matrix[0],e.outer(full))
    e.close(result.expectation('xx')[0],math.sin(theta)*math.cos(phi))
    e.close(result.expectation('xy')[0],math.sin(theta)*math.sin(phi))
    return result,full


def sequential(rho,first,second):
    probs,states,sigmas,ignored=instrument(rho,first)
    family(second,len(rho));table=torch.zeros((len(first),len(second)),dtype=torch.float64)
    for r,sigma in enumerate(sigmas):
        for s,group in enumerate(second):
            table[r,s]=sum(torch.trace(L@sigma@L.mH).real.item() for L in group)
        e.close(table[r].sum(),probs[r])
        if states[r]is not None:
            later=instrument(states[r],second)[0]
            e.close(table[r],torch.tensor(later,dtype=torch.float64)*probs[r])
    e.close(table.sum(0),instrument(ignored,second)[0])
    return table


def invalid_checks():
    rho=I/2
    calls=[lambda:instrument(2*rho,Z_GROUPS),lambda:instrument(torch.tensor([[1,1],[0,0]],dtype=D),Z_GROUPS),
      lambda:instrument(torch.diag(torch.tensor([1.1,-.1],dtype=D)),Z_GROUPS),
      lambda:instrument(rho,()),lambda:instrument(rho,((I,),())),
      lambda:instrument(rho,((I/2,),)),lambda:instrument(rho,((torch.eye(4,dtype=D),),)),
      lambda:instrument(rho,((I.real,),)),lambda:instrument(rho,((torch.full_like(I,complex('nan')),),)),
      lambda:weak(1.1),lambda:weak(float('nan')),lambda:weak(.3,'flip'),
      lambda:mean(rho,torch.tensor([[0,1],[0,0]],dtype=D))]
    for call in calls:
        try:call()
        except ValueError:pass
        else:raise AssertionError('Malformed contract accepted')
    rare=torch.diag(torch.tensor([1-1e-20,1e-20],dtype=D))
    probs,states,_,_=instrument(rare,Z_GROUPS)
    assert probs[1]>0 and states[1]is not None;e.close(states[1],P1)
    zero=instrument(P0,Z_GROUPS);assert zero[0][1]==0 and zero[1][1]is None
    try:instrument(rho,((1e-200*I,),(I,)))
    except FloatingPointError:pass
    else:raise AssertionError('Underflow passed as impossible branch')
    return len(calls)


def main():
    inputs=tuple(e.qubit(t,p) for t,p in ((0.,0.),(math.pi,0.),(math.pi/2,0.),
        (math.pi/2,math.pi/2),(.83,-.49),(1.31,.72)))
    for mode in ('statevector','density_matrix'):
        for v in inputs:native(v,mode)
    print('12 native input circuits:both modes;density,probabilities and X/Y/Z/H means passed.')
    for mode in ('statevector','density_matrix'):
        for strength in (0.,.6,1.):
            for flip in (False,True):
                pair=[]
                for v in (inputs[0],inputs[4],inputs[5]):
                    result,blocks,table=coupled(v,strength,flip,mode=mode)
                    pair.append(blocks)
                rho=e.rho((.34,.66),(inputs[4],inputs[5]))
                probs,states,sigmas,ignored=instrument(rho,weak(strength,flip))
                reference=scalar_branches((.34,.66),(inputs[4],inputs[5]),weak(strength,flip))
                for r in range(2):
                    e.close(sigmas[r],.34*pair[1][r]+.66*pair[2][r]);e.close(sigmas[r],reference[r])
    print('36 native weak couplings:strength0/.6/1,two instruments,two modes;host mixed branches match joint-density blocks.')
    XP=((I+X)/2,);XM=((I-X)/2,);second=(XP,XM)
    for mode in ('statevector','density_matrix'):
        tables=[]
        for v in (inputs[4],inputs[5]):
            _,_,table=coupled(v,1.,analyzer=True,mode=mode);tables.append(table)
        rho=e.rho((.34,.66),(inputs[4],inputs[5]))
        e.close(sequential(rho,Z_GROUPS,second),.34*tables[0]+.66*tables[1])
    print('4 native Z-record/X-readout circuits:chronological joint probabilities,conditionals and ignored marginal passed.')
    even=torch.diag(torch.tensor([1,0,0,1],dtype=D));odd=torch.eye(4,dtype=D)-even
    fine=((torch.diag(torch.tensor([1,0,0,0],dtype=D)),torch.diag(torch.tensor([0,0,0,1],dtype=D))),
          (torch.diag(torch.tensor([0,1,0,0],dtype=D)),torch.diag(torch.tensor([0,0,1,0],dtype=D))))
    for mode in ('statevector','density_matrix'):
        for theta,phi in ((math.pi/2,0.),(math.pi/2,math.pi/2),(.72,-.31)):
            result,v=bell(theta,phi,mode);rho=result.density_matrix[0]
            coarse=instrument(rho,((even,),(odd,)));forgotten=instrument(rho,fine)
            e.close(coarse[0],forgotten[0]);e.close(coarse[1][0],rho)
            assert forgotten[1][1]is None
            for label,A in (('xx',torch.kron(X,X)),('xy',torch.kron(X,Y))):
                e.close(mean(coarse[3],A),result.expectation(label)[0]);e.close(mean(forgotten[3],A),0)
    print('6 native joint preparations:coarse parity preserves coherence,fine Z with forgotten labels removes it.')
    phase=e.outer(inputs[2]);groups=((P0,P1),);mixed=instrument(phase,groups)
    rotated=instrument(phase,((I/math.sqrt(2),Z/math.sqrt(2)),))
    e.close(mixed[3],I/2);e.close(rotated[3],mixed[3])
    print(f'{invalid_checks()} malformed contracts rejected;positive1e-20 retained,zero returns None,underflow raises.')
    assert RUNS==58
    print('58 actual native circuits;all conditional updates and ensemble sums are explicit host calculations.')


if __name__=='__main__':main()
