"""Section4.8: actual FQ/Qiskit state, local gate and count-schema translation."""
from itertools import product,permutations
from importlib.metadata import version
from math import sqrt
import torch
import flagquantum as fq
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector,Operator
from qiskit.primitives import StatevectorSampler
try:
    from examples.foundations.tensor_spaces import prepare_matrix,OPTIONS
    from examples.foundations.ordered_supports import complex_gate,controlled_flip,scalar_scatter,dense_embedding,input_product,support_tuple,checked_matrix
except ModuleNotFoundError:
    from tensor_spaces import prepare_matrix,OPTIONS
    from ordered_supports import complex_gate,controlled_flip,scalar_scatter,dense_embedding,input_product,support_tuple,checked_matrix
DTYPE=torch.complex128
ATOL=1e-12


def labels(order):
    if not isinstance(order,(tuple,list)) or not order or any(type(x) is not str or not x for x in order) or len(set(order))!=len(order):
        raise ValueError('Declare unique nonempty string labels in most-significant-first order')
    return tuple(order)


def basis_map(source,target):
    source=labels(source);target=labels(target)
    if set(source)!=set(target):raise ValueError('Both orders must name the same qubits')
    n=len(source);B=torch.zeros((2**n,2**n),dtype=DTYPE)
    for col,bits in enumerate(product((0,1),repeat=n)):
        by_name=dict(zip(source,bits));row=int(''.join(str(by_name[q]) for q in target),2)
        B[row,col]=1
    return B


def reversal(n):
    if type(n) is not int or n<1:raise ValueError('Declare positive integer n')
    source=tuple(f'q{q}' for q in range(n))
    return basis_map(source,source[::-1])


def q_local(U,k):
    U=checked_matrix(U,k,unitary=True);R=reversal(k)
    return R@U@R.mH


def q_circuit(factors,U=None,S=None,reverse_arguments=False):
    n=len(factors);qc=QuantumCircuit(n)
    for q,v in enumerate(factors):qc.unitary(prepare_matrix(torch.tensor(v,dtype=DTYPE)).numpy(),[q])
    if U is not None:
        S=support_tuple(n,S);U=checked_matrix(U,len(S),unitary=True)
        if reverse_arguments:qc.unitary(U.numpy(),list(S[::-1]))
        else:qc.unitary(q_local(U,len(S)).numpy(),list(S))
    return qc


def pair(factors,U=None,S=None):
    n=len(factors);c=fq.Circuit(n,dtype=DTYPE)
    for q,v in enumerate(factors):c.unitary(q,unitary=prepare_matrix(torch.tensor(v,dtype=DTYPE)))
    initial=input_product(factors)
    if U is not None:
        S=support_tuple(n,S);U=checked_matrix(U,len(S),unitary=True)
        c.unitary(*S,unitary=U)
        reference=torch.tensor(scalar_scatter(U,initial.tolist(),n,S),dtype=DTYPE)
    else:reference=initial
    r=fq.run(c,outputs=[fq.probabilities()],options=OPTIONS)
    raw,p=r.statevector(),r.probabilities
    assert raw.shape==p.shape==(1,2**n) and raw.dtype==DTYPE and p.dtype==torch.float64
    assert raw.device.type==p.device.type=='cpu' and torch.isfinite(raw).all() and torch.isfinite(p).all()
    qc=q_circuit(factors,U,S);z=torch.from_numpy(Statevector.from_instruction(qc).data.copy())
    assert z.shape==(2**n,) and z.dtype==DTYPE and torch.isfinite(z).all()
    torch.testing.assert_close(raw[0],reference,rtol=0,atol=ATOL)
    torch.testing.assert_close(z,reversal(n)@raw[0],rtol=0,atol=ATOL)
    torch.testing.assert_close(p[0],raw[0].abs().square(),rtol=0,atol=ATOL)
    return raw[0],z,qc


def slot_map(mapping):
    if not isinstance(mapping,(tuple,list)) or not mapping or any(type(x) is not int for x in mapping) or sorted(mapping)!=list(range(len(mapping))):
        raise ValueError('This adapter requires one distinct classical slot per declared measured label, all slots used')
    return tuple(mapping)


def decode_key(key,mapping,groups=None):
    mapping=slot_map(mapping);n=len(mapping)
    if type(key) is not str:raise ValueError('Declare binary count string')
    if groups is None:chunks=[key];groups=(n,)
    else:
        if not isinstance(groups,(tuple,list)) or not groups or any(type(x) is not int or x<1 for x in groups) or sum(groups)!=n:raise ValueError('Declare positive displayed group widths summing to slot count')
        chunks=key.split(' ')
    if len(chunks)!=len(groups) or any(len(chunk)!=width or any(c not in '01' for c in chunk) for chunk,width in zip(chunks,groups)):
        raise ValueError('Count string does not match the declared binary display schema')
    # Caller declares displayed groups as descending classical-slot blocks.
    displayed=''.join(chunks);classical=displayed[::-1]
    return ''.join(classical[mapping[q]] for q in range(n))


def canonical_counts(counts,mapping,groups=None):
    if not isinstance(counts,dict) or not counts:raise ValueError('Declare nonempty count dictionary')
    result={}
    for key,count in counts.items():
        if type(count) is not int or count<0:raise ValueError('Counts must be nonnegative literal integers')
        canonical=decode_key(key,mapping,groups);result[canonical]=result.get(canonical,0)+count
    return result


def sample(qc,mapping,shots):
    mapping=slot_map(mapping)
    if len(mapping)!=qc.num_qubits or qc.num_clbits!=0:raise ValueError('Expected unmeasured circuit matching the full readout map')
    if type(shots) is not int or shots<1:raise ValueError('Positive integer shots required')
    measured=QuantumCircuit(qc.num_qubits,qc.num_qubits);measured.compose(qc,inplace=True)
    for q,c in enumerate(mapping):measured.measure(q,c)
    pub=StatevectorSampler(seed=20261021).run([measured],shots=shots).result()[0]
    raw=pub.data.c.get_counts()
    assert sum(raw.values())==shots
    return raw,canonical_counts(raw,mapping)


def sample_partial(qc,S,shots):
    S=support_tuple(qc.num_qubits,S)
    if qc.num_clbits!=0 or type(shots) is not int or shots<1:raise ValueError('Unmeasured circuit and positive integer shots required')
    measured=QuantumCircuit(qc.num_qubits,len(S));measured.compose(qc,inplace=True)
    for c,q in enumerate(S):measured.measure(q,c)
    raw=StatevectorSampler(seed=20261021).run([measured],shots=shots).result()[0].data.c.get_counts()
    assert sum(raw.values())==shots
    return raw,canonical_counts(raw,tuple(range(len(S))))


def marginal(p,n,S):
    S=support_tuple(n,S)
    if p.shape!=(2**n,) or p.dtype!=torch.float64 or not torch.isfinite(p).all() or (p<0).any():raise ValueError('Expected finite nonnegative float64 full probability vector')
    out=torch.zeros(2**len(S),dtype=torch.float64)
    for j,bits in enumerate(product((0,1),repeat=n)):
        row=int(''.join(str(bits[q]) for q in S),2);out[row]+=p[j]
    return out


def factors_complex():return [(.6,.8j),(sqrt(3)/2,.5j),(1/sqrt(2),1j/sqrt(2))]


def main():
    assert version('flagquantum')=='0.3.1' and version('torch').split('+')[0]=='2.13.0' and version('qiskit')=='2.5.2'
    print('FQ0.3.1:q0MSB; Qiskit2.5.2:q0LSB; labels and physical qubits matched explicitly.')
    for n in range(1,5):
        for bits in product((0,1),repeat=n):pair([(1,0) if b==0 else (0,1) for b in bits])
    print('30 basis-preparation pairs through4qubits: every complex coordinate and probability checked.')
    U=complex_gate()
    for S in permutations(range(3),2):
        for bits in product((0,1),repeat=3):pair([(1,0) if b==0 else (0,1) for b in bits],U,S)
    print('48 ordered-support basis pairs: asymmetric complex local gate on all3qubit ordered pairs.')
    for S in ((2,0),(0,2),(2,0,1)):
        if len(S)==2:gate=U
        else:
            try:from examples.foundations.tensor_reshaping import local_gate
            except ModuleNotFoundError:from tensor_reshaping import local_gate
            gate=local_gate(3)
        f,z,qc=pair(factors_complex(),gate,S)
        reverse=torch.from_numpy(Statevector.from_instruction(q_circuit(factors_complex(),gate,S,True)).data.copy())
        torch.testing.assert_close(reverse,z,rtol=0,atol=ATOL)
        op=QuantumCircuit(3);op.unitary(q_local(gate,len(S)).numpy(),list(S))
        O=torch.from_numpy(Operator(op).data.copy());R=reversal(3)
        torch.testing.assert_close(O,R@dense_embedding(gate,3,S)@R.mH,rtol=0,atol=ATOL)
    # Negative translation witness: same numeric local matrix with same qarg list is wrong.
    wrong=q_circuit(factors_complex());wrong.unitary(U.numpy(),[2,0])
    f,z,qc=pair(factors_complex(),U,(2,0))  # Included in the ledger below as a fourth complex pair.
    bad_z=torch.from_numpy(Statevector.from_instruction(wrong).data.copy())
    assert not torch.allclose(z,bad_z,rtol=0,atol=ATOL)
    event=torch.diag(torch.tensor([1 if bits[0] else 0 for bits in product((0,1),repeat=3)],dtype=DTYPE))
    R=reversal(3);converted=R@event@R.mH
    assert abs(torch.vdot(f,event@f).item()-torch.vdot(z,converted@z).item())<ATOL
    print('4complex pairs,3reversed-argument alternatives,3operator matrices; raw-matrix negative witness rejected.')
    for order in permutations(('q0','q1','q2')):
        B=basis_map(('q0','q1','q2'),order);back=basis_map(order,('q0','q1','q2'))
        assert torch.equal(back@B,torch.eye(8,dtype=DTYPE))
    basis=q_circuit([(0,1),(1,0),(1,0)])
    raw1,canonical1=sample(basis,(0,1,2),64);raw2,canonical2=sample(basis,(2,0,1),64)
    assert raw1=={'001':64} and raw2=={'100':64} and canonical1==canonical2=={'100':64}
    print('Actual64shot basis readout: map(0,1,2) raw001; map(2,0,1) raw100; both canonical100.')
    raw,counts=sample(qc,(2,0,1),1024)
    empirical=torch.tensor([counts.get(format(j,'03b'),0)/1024 for j in range(8)],dtype=torch.float64)
    assert (empirical-f.abs().square()).abs().max()<.1
    assert torch.allclose(marginal((R.mH@z).abs().square(),3,(2,0)),marginal(f.abs().square(),3,(2,0)),rtol=0,atol=ATOL)
    _,partial=sample_partial(qc,(2,0),1024)
    partial_empirical=torch.tensor([partial.get(format(j,'02b'),0)/1024 for j in range(4)],dtype=torch.float64)
    assert (partial_empirical-marginal(f.abs().square(),3,(2,0))).abs().max()<.1
    assert canonical_counts({'10 0':7},(0,1,2),(2,1))=={'001':7}
    bad=[lambda:basis_map(('a','a'),('a','b')),lambda:basis_map(('a','b'),('a','c')),lambda:slot_map((0,0,2)),lambda:slot_map((False,1)),lambda:decode_key('1',(0,1,2)),lambda:decode_key('0x1',(0,1,2)),lambda:decode_key('10 0',(0,1,2)),lambda:decode_key('10 0',(0,1,2),(1,2)),lambda:canonical_counts({'001':-1},(0,1,2)),lambda:canonical_counts({'001':True},(0,1,2))]
    for action in bad:
        try:action()
        except ValueError:pass
        else:raise AssertionError('Invalid convention schema admitted')
    print('1024shot complex readout: counts conserved, all frequencies within0.1of exact probabilities; actual1024shot partial readout matches ordered marginal.')
    print('6basis-order roundtrips, explicit grouped fixture and10invalid schemas checked.')
    print('82FQ circuits;86Qiskit statevector circuits;3Operator constructions;4Sampler pubs,2176shots; ideal CPU only.')


if __name__=='__main__':main()
