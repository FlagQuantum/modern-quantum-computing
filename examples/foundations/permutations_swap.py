"""Section4.5: active permutations, passive coordinates and metadata renaming."""
from itertools import permutations, product
from importlib.metadata import version
from math import sqrt
import torch
import flagquantum as fq
try:
    from examples.foundations.tensor_spaces import prepare_matrix, OPTIONS
    from examples.foundations.ordered_supports import dense_embedding, controlled_flip, input_product
except ModuleNotFoundError:
    from tensor_spaces import prepare_matrix, OPTIONS
    from ordered_supports import dense_embedding, controlled_flip, input_product
DTYPE=torch.complex128
ATOL=1e-12


def permutation(p):
    if not isinstance(p,(tuple,list)) or not p or any(type(q) is not int for q in p) or sorted(p)!=list(range(len(p))):
        raise ValueError('Declare a nonempty bijective old-position to new-position tuple')
    return tuple(p)


def inverse(p):
    p=permutation(p)
    return tuple(p.index(q) for q in range(len(p)))


def moved_bits(bits,p):
    p=permutation(p)
    if len(bits)!=len(p) or any(type(b) is not int or b not in (0,1) for b in bits):
        raise ValueError('Expected one literal integer bit per declared qubit')
    out=[0]*len(p)
    for q,destination in enumerate(p):out[destination]=bits[q]
    return tuple(out)


def perm_matrix(p):
    p=permutation(p);n=len(p);a=torch.zeros((2**n,2**n),dtype=DTYPE)
    for col,bits in enumerate(product((0,1),repeat=n)):
        row=int(''.join(map(str,moved_bits(bits,p))),2);a[row,col]=1
    return a


def scalar_permute(state,p):
    # Independent output-centric binary-string gather, no matrix or moved_bits.
    p=permutation(p);n=len(p)
    if len(state)!=2**n:raise ValueError('Wrong state length')
    out=[]
    for row in range(2**n):
        output=format(row,f'0{n}b')
        original=''.join(output[p[q]] for q in range(n))
        out.append(state[int(original,2)])
    return torch.tensor(out,dtype=DTYPE)


def swap_sequence(p):
    # Place each old factor at its declared destination using at most n-1 swaps.
    p=permutation(p);at=list(range(len(p)));steps=[]
    for destination in range(len(p)):
        wanted=p.index(destination);source=at.index(wanted)
        if source!=destination:
            steps.append((destination,source))
            at[destination],at[source]=at[source],at[destination]
    assert all(at[p[q]]==q for q in range(len(p)))
    return steps


def renamed(labels,replacements):
    if not isinstance(labels,(tuple,list)) or not labels or any(type(x) is not str or not x for x in labels) or len(set(labels))!=len(labels):
        raise ValueError('Declare unique nonempty string labels')
    if not isinstance(replacements,dict) or any(x not in labels for x in replacements):
        raise ValueError('Rename keys must name existing labels')
    out=tuple(replacements.get(x,x) for x in labels)
    if any(type(x) is not str or not x for x in out) or len(set(out))!=len(out):
        raise ValueError('Renaming must preserve distinct labels')
    return out


def run(p,factors,entangle=False,before=None,after=None):
    p=permutation(p);n=len(p)
    if len(factors)!=n:raise ValueError('One preparation per qubit required')
    if entangle and n<2:raise ValueError('Entangling preparation needs two qubits')
    c=fq.Circuit(n,dtype=DTYPE)
    for q,v in enumerate(factors):c.unitary(q,unitary=prepare_matrix(torch.tensor(v,dtype=DTYPE)))
    if entangle:c.unitary(0,1,unitary=controlled_flip())
    if before is not None:c.unitary(*before[0],unitary=before[1])
    for a,b in swap_sequence(p):c.swap(a,b)
    if after is not None:c.unitary(*after[0],unitary=after[1])
    r=fq.run(c,outputs=[fq.probabilities()],options=OPTIONS);state,prob=r.statevector(),r.probabilities
    assert state.shape==prob.shape==(1,2**n) and state.dtype==DTYPE and prob.dtype==torch.float64
    assert state.device.type==prob.device.type=='cpu' and torch.isfinite(state).all() and torch.isfinite(prob).all()
    torch.testing.assert_close(prob[0],state[0].abs().square(),rtol=0,atol=ATOL)
    return state[0],prob[0]


def complex_factors():return [(sqrt(3)/2,.5j),(1,0),(sqrt(.8),1j*sqrt(.2))]


def entangled_reference():
    # Hand expansion, independently of the preparation circuit and embedding.
    return torch.tensor([sqrt(.6),1j*sqrt(.15),0,0,0,0,1j*sqrt(.2),-sqrt(.05)],dtype=DTYPE)


def main():
    assert version('flagquantum')=='0.3.1' and version('torch').split('+')[0]=='2.13.0'
    print('Convention: p[q] is the destination of old qubit q; qubit0 is most significant.')
    count=0
    for n in range(1,5):
        for p in permutations(range(n)):
            P=perm_matrix(p);I=torch.eye(2**n,dtype=DTYPE)
            torch.testing.assert_close(P.mH@P,I,rtol=0,atol=0)
            torch.testing.assert_close(perm_matrix(inverse(p)),P.mH,rtol=0,atol=0)
            for bits in product((0,1),repeat=n):
                factors=[(1,0) if b==0 else (0,1) for b in bits]
                initial=input_product(factors);state,prob=run(p,factors)
                torch.testing.assert_close(state,P@initial,rtol=0,atol=ATOL)
                torch.testing.assert_close(state,scalar_permute(initial.tolist(),p),rtol=0,atol=ATOL);count+=1
    assert count==442
    print('442 basis circuits: every permutation and every basis input for n=1,2,3,4.')
    psi=entangled_reference();factors=complex_factors()
    for p in permutations(range(3)):
        state,prob=run(p,factors,entangle=True)
        torch.testing.assert_close(state,perm_matrix(p)@psi,rtol=0,atol=ATOL)
        torch.testing.assert_close(state,scalar_permute(psi.tolist(),p),rtol=0,atol=ATOL)
    p=(1,2,0);P=perm_matrix(p)
    basis=torch.eye(8,dtype=DTYPE)[:,4]
    print(f'Input100: active cycle index{int((P@basis).abs().argmax())}; passive coordinate index{int((P.mH@basis).abs().argmax())}.')
    Z=torch.diag(torch.tensor([1,-1],dtype=DTYPE));A=dense_embedding(Z,3,(0,))
    active=P@psi;passive=P.mH@psi;Aprime=P.mH@A@P
    expectation=lambda v,a:float(torch.vdot(v,a@v).real)
    assert abs(expectation(psi,A)-expectation(passive,Aprime))<ATOL
    print(f'Z0: original {expectation(psi,A):.6f}; active fixed observable {expectation(active,A):.6f}; passive transformed observable {expectation(passive,Aprime):.6f}.')
    S=(2,0);T=tuple(inverse(p)[q] for q in S);C=controlled_flip()
    torch.testing.assert_close(P.mH@dense_embedding(C,3,S)@P,dense_embedding(C,3,T),rtol=0,atol=ATOL)
    a,_=run(inverse(p),factors,True,before=(S,C));b,_=run(inverse(p),factors,True,after=(T,C))
    torch.testing.assert_close(a,b,rtol=0,atol=ATOL)
    print(f'Passive ordered support {S} -> {T}: two actual circuit paths agree in every complex coordinate.')
    # Noncommuting cycles: P_r P_p = P_(r o p), not the reverse.
    r=(1,0,2);composed=tuple(r[p[q]] for q in range(3))
    torch.testing.assert_close(perm_matrix(r)@P,perm_matrix(composed),rtol=0,atol=0)
    assert not torch.equal(perm_matrix(tuple(p[r[q]] for q in range(3))),perm_matrix(composed))
    assert renamed(('signal','reference','flag'),{'signal':'data'})==('data','reference','flag')
    bad=[lambda:permutation(()),lambda:permutation((0,0)),lambda:permutation((0,2)),lambda:permutation((False,1)),lambda:permutation((0,1.0)),lambda:moved_bits((1,),(1,0)),lambda:moved_bits((True,0),(1,0)),lambda:renamed(('a','b'),{'a':'b'}),lambda:renamed(('a','b'),{'c':'d'}),lambda:renamed(('a','a'),{})]
    for action in bad:
        try:action()
        except ValueError:pass
        else:raise AssertionError('Invalid declaration admitted')
    print('Composition order, identity, inverse, metadata rename and10invalid declarations checked.')
    print('450 actual CPU complex128 circuits; atol=1e-12,rtol=0; no phase alignment, shots or hardware.')


if __name__=='__main__':main()
