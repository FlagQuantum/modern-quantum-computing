"""7.6: two classical bits,one transmitted qubit and a declared shared Bell pair.

Static native gates/terminal queries in one centralized simulator;ownership and
transport are protocol assumptions,not native network operations.
"""
import cmath
import itertools
import math
from dataclasses import replace
from importlib.metadata import version

import flagquantum as fq
import torch
try:
    from examples.foundations.tensor_spaces import OPTIONS
except ModuleNotFoundError:
    from tensor_spaces import OPTIONS

D=torch.complex128
ATOL=1e-12
RUNS=0


def message(bits):
    if type(bits) is not tuple or len(bits)!=2 or any(type(x) is not int or x not in (0,1) for x in bits):
        raise ValueError('Literal semantic (phase bit a,parity bit b) required')
    return bits


def support(n,pair):
    if (type(n) is not int or not 2<=n<=4 or type(pair) is not tuple or len(pair)!=2
        or any(type(q) is not int or not 0<=q<n for q in pair) or len(set(pair))!=2):
        raise ValueError('Distinct ordered(Alice A,Bob B) qubits in a2-4qubit teaching register required')
    return pair


def parameters(theta,phase):
    if any(type(x) not in (int,float) or not math.isfinite(x) for x in (theta,phase)):
        raise ValueError('Finite literal real angles in radians required')


def columns_contract(columns,pair):
    if type(columns) is not tuple or len(columns)!=2 or set(columns)!=set(pair):
        raise ValueError('Both readout columns must be declared exactly once')


def decode_record(row,columns,pair):
    support(max(pair)+1,pair);columns_contract(columns,pair)
    if (not isinstance(row,torch.Tensor) or row.shape!=(2,) or row.dtype!=torch.int64
        or row.device.type!='cpu' or not bool(((row==0)|(row==1)).all())):
        raise ValueError('Complete CPU int64 binary record required')
    return message(tuple(int(row[columns.index(q)]) for q in pair))


def local(bits,stage,theta=math.pi/2,phase=0.,order='xz'):
    a,b=message(bits);parameters(theta,phase)
    if stage not in ('resource','encoded','decoded','parity','wrong'):
        raise ValueError('Unknown declared circuit stage')
    if order not in ('xz','zx'):raise ValueError('Declare chronological xz or zx encoding')
    c=math.cos(theta/2);s=cmath.exp(phase*1j)*math.sin(theta/2)
    def encoded(x,y):
        return ((c if y==0 else s)*(-1)**(a*x)) if y==(x^b) else 0j
    values=[]
    for x,y in itertools.product((0,1),repeat=2):
        if stage=='resource':value=(c if x==0 else s) if x==y else 0j
        elif stage=='encoded':value=encoded(x,y)
        elif stage=='parity':value=encoded(x,y^x)
        elif stage=='decoded':
            u=x^a
            value=((-1)**(u*b))*(c+(-1)**u*s)/math.sqrt(2) if y==b else 0j
        else:
            value=(encoded(0,y^x)+(-1)**x*encoded(1,y^x))/math.sqrt(2)
        if order=='zx' and stage!='resource':value*=(-1)**(a*b)
        values.append(value)
    return torch.tensor(values,dtype=D)


def scalar_state(bits,stage='decoded',n=2,pair=(0,1),theta=math.pi/2,phase=0.,order='xz'):
    left,right=support(n,pair)
    v=local(bits,stage,theta,phase,order);values=[]
    for k in range(2**n):
        binary=[int(x) for x in format(k,f'0{n}b')]
        value=complex(v[2*binary[left]+binary[right]])
        for q in range(n):
            if q not in pair:
                angle=.29+.17*q
                value*=math.cos(angle/2) if binary[q]==0 else cmath.exp(-.23j*(q+1))*math.sin(angle/2)
        values.append(value)
    return torch.tensor(values,dtype=D)


def circuit(bits,stage='decoded',n=2,pair=(0,1),theta=math.pi/2,phase=0.,order='xz'):
    a,b=message(bits);left,right=support(n,pair);parameters(theta,phase)
    if stage not in ('resource','encoded','decoded','parity','wrong'):raise ValueError('Unknown stage')
    if order not in ('xz','zx'):raise ValueError('Unknown encoding order')
    c=fq.Circuit(n,dtype=D)
    if theta==math.pi/2 and phase==0.:c.h(left)
    else:c.ry(left,theta).p(left,phase)
    c.cx(left,right)
    for q in range(n):
        if q not in pair:c.ry(q,.29+.17*q).p(q,-.23*(q+1))
    if stage!='resource':
        if order=='xz':
            if b:c.x(left)
            if a:c.z(left)
        else:
            if a:c.z(left)
            if b:c.x(left)
    if stage in ('decoded','parity'):c.cx(left,right)
    if stage=='decoded':c.h(left)
    if stage=='wrong':c.h(left).cx(left,right)
    return c


def scalar_expectation(v,n,pair,kind):
    left,right=pair;value=0j
    for k,z in enumerate(v.tolist()):
        x=(k>>(n-1-left))&1;y=(k>>(n-1-right))&1
        if kind=='xx':contribution=v[k^(1<<(n-1-left))^(1<<(n-1-right))]
        elif kind=='zz':contribution=(-1)**(x+y)*v[k]
        elif kind=='bx':contribution=v[k^(1<<(n-1-right))]
        elif kind=='by':contribution=(-1j if y==0 else 1j)*v[k^(1<<(n-1-right))]
        elif kind=='bz':contribution=(-1)**y*v[k]
        else:raise ValueError('Unknown Pauli reference')
        value+=z.conjugate()*complex(contribution)
    assert abs(value.imag)<ATOL
    return value.real


def query(bits,stage='decoded',n=2,pair=(0,1),theta=math.pi/2,phase=0.,order='xz',columns=None,shots=17,seed=29):
    global RUNS
    message(bits);support(n,pair);parameters(theta,phase)
    columns=pair if columns is None else columns;columns_contract(columns,pair)
    if type(shots) is not int or shots<1 or type(seed) is not int or seed<0:
        raise ValueError('Positive shot count and nonnegative literal seed required')
    c=circuit(bits,stage,n,pair,theta,phase,order);left,right=pair
    outputs=[fq.probabilities(qubits=columns),fq.samples(qubits=columns),
             fq.expectation(fq.X(left)@fq.X(right),name='xx'),
             fq.expectation(fq.Z(left)@fq.Z(right),name='zz')]
    outputs += [fq.expectation(op(right),name=name) for op,name in ((fq.X,'bx'),(fq.Y,'by'),(fq.Z,'bz'))]
    result=fq.run(c,outputs=outputs,shots=shots,options=replace(OPTIONS,seed=seed));RUNS+=1
    v=result.statevector()
    reference=scalar_state(bits,stage,n,pair,theta,phase,order)
    assert v.shape==(1,2**n) and v.dtype==D
    assert torch.allclose(v[0],reference,atol=ATOL,rtol=0)
    p=torch.zeros(4,dtype=torch.float64)
    for k,z in enumerate(reference.tolist()):
        key=2*((k>>(n-1-columns[0]))&1)+((k>>(n-1-columns[1]))&1)
        p[key]+=abs(z)**2
    assert torch.allclose(result.probabilities[0],p,atol=ATOL,rtol=0)
    for name in ('xx','zz','bx','by','bz'):
        assert abs(float(result.expectation(name)[0])-scalar_expectation(reference,n,pair,name))<ATOL
    raw=result.samples
    assert raw.shape==(1,shots,2) and raw.dtype==torch.int64
    semantic=[decode_record(row,columns,pair) for row in raw[0]]
    counts=torch.bincount(torch.tensor([2*a+b for a,b in semantic]),minlength=4)
    assert int(counts.sum())==shots
    if stage=='decoded' and theta==math.pi/2 and phase==0.:
        assert all(x==bits for x in semantic)
    return {'state':v[0],'probabilities':result.probabilities[0],'bits':raw[0],
        'messages':semantic,'counts':counts,'expectations':{x:float(result.expectation(x)[0]) for x in ('xx','zz','bx','by','bz')}}


def carrier(bits):
    """Static three-CX relocation fixture;not a physical network send."""
    global RUNS
    a,b=message(bits)
    c=fq.Circuit(3,dtype=D).h(0).cx(0,1)
    if b:c.x(0)
    if a:c.z(0)
    c.cx(0,2).cx(2,0).cx(0,2)  # SWAP(old A,empty carrier)
    c.cx(2,1).h(2)             # Bob decodes(carrier,B)
    result=fq.run(c,outputs=[fq.probabilities(qubits=(2,1)),fq.samples(qubits=(2,1))],shots=11,options=OPTIONS)
    RUNS+=1
    expected=torch.zeros(8,dtype=D);expected[2*b+a]=1
    assert torch.allclose(result.statevector()[0],expected,atol=ATOL,rtol=0)
    one=torch.zeros(4,dtype=torch.float64);one[2*a+b]=1
    assert torch.allclose(result.probabilities[0],one,atol=ATOL,rtol=0)
    assert all(tuple(map(int,row))==bits for row in result.samples[0])
    return result.statevector()[0]


def main():
    assert version('flagquantum')=='0.3.1' and RUNS==0
    for n in (2,3,4):
        for pair in itertools.permutations(range(n),2):
            for bits in itertools.product((0,1),repeat=2):
                enc=query(bits,'encoded',n,pair,columns=pair[::-1])
                dec=query(bits,'decoded',n,pair,columns=pair[::-1])
                a,b=bits
                assert abs(enc['expectations']['xx']-(-1)**a)<ATOL
                assert abs(enc['expectations']['zz']-(-1)**b)<ATOL
                assert all(abs(enc['expectations'][x])<ATOL for x in ('bx','by','bz'))
    print('160 native circuits:four messages on all20 ordered2/3/4qubit pairs;exact encoded/decoded vectors,reversed-column records and spectator phases passed.')
    query((0,0),'resource')
    for bits in itertools.product((0,1),repeat=2):
        parity=query(bits,'parity');wrong=query(bits,'wrong')
        expected=torch.zeros(4,dtype=torch.float64);expected[bits[1]]=.5;expected[2+bits[1]]=.5
        assert torch.allclose(parity['probabilities'],expected,atol=ATOL,rtol=0)
        assert torch.allclose(wrong['probabilities'],torch.full((4,),.25,dtype=torch.float64),atol=ATOL,rtol=0)
        for stage in ('encoded','decoded'):
            alt=query(bits,stage,order='zx')
            assert torch.allclose(alt['state'],(-1)**(bits[0]*bits[1])*scalar_state(bits,stage),atol=ATOL,rtol=0)
    print('17 native circuits:resource,omitted-H/wrong-order decoders and alternate encoding phase passed.')
    for theta,phase in ((0.,0.),(.83,-.47),(math.pi/2,math.pi),(.93,.52),(-.71,-.38),(math.pi,0.)):
        for bits in itertools.product((0,1),repeat=2):
            query(bits,'encoded',theta=theta,phase=phase)
            decoded=query(bits,'decoded',theta=theta,phase=phase)
            good=(1+math.sin(theta)*math.cos(phase))/2
            a,b=bits;p=decoded['probabilities']
            assert abs(float(p[2*a+b])-good)<ATOL
            assert abs(float(p[2*(a^1)+b])-(1-good))<ATOL
    print('48 native circuits:six imperfect pure resources;exact phase-bit error formula and parity-bit preservation passed.')
    for bits in itertools.product((0,1),repeat=2):carrier(bits)
    print('4 native relocation fixtures:old Alice slot=0,carrier/B decoder returns(a,b);not a network transport test.')
    bad=[lambda:message((True,0)),lambda:message((0,)),lambda:message((0,2)),
         lambda:support(1,(0,1)),lambda:support(3,(0,0)),lambda:support(3,(0,3)),
         lambda:parameters(float('nan'),0),lambda:parameters(0,1j),
         lambda:query((0,0),stage='unknown'),lambda:query((0,0),order='unknown'),
         lambda:query((0,0),shots=0),lambda:query((0,0),seed=-1),
         lambda:query((0,0),columns=(0,0)),
         lambda:decode_record(torch.tensor([0.,1.]),(0,1),(0,1)),
         lambda:decode_record(torch.tensor([0,2]),(0,1),(0,1)),
         lambda:decode_record(torch.tensor([0,1]),(0,2),(0,1))]
    for attempt in bad:
        before=RUNS
        try:attempt()
        except ValueError:pass
        else:raise AssertionError('Malformed contract admitted')
        assert before==RUNS
    assert RUNS==229,RUNS
    print('16 malformed contracts rejected before another native execution.')
    print('229 CPU complex128 native circuits passed;one transmitted qubit assumes a previously shared Bell pair.')


if __name__=='__main__':main()
