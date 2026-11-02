"""44.2: minimal book-side local executor versus independently indexed dense maps."""
import math,cmath,itertools
from dataclasses import replace
import torch,flagquantum as fq
try:
 from examples.foundations import statistical_ensembles as e,uniform_reversible as b
except ModuleNotFoundError:
 import statistical_ensembles as e,uniform_reversible as b
D=torch.complex128
RUNS=0
RECEIPTS=[]

def support(n,S):
 if type(n)is not int or not 0<=n<=8 or type(S)is not tuple or any(type(q)is not int or not 0<=q<n for q in S)or len(set(S))!=len(S):raise ValueError('Literal n0..8 and ordered unique in-range support tuple required')
 return S

def vector(v,n):
 support(n,())
 if not isinstance(v,torch.Tensor)or v.shape!=(1<<n,)or v.dtype!=D or v.device.type!='cpu'or v.layout!=torch.strided or not bool(torch.isfinite(v).all()):raise ValueError('Finite unbatched CPUcomplex128 vector required;no normalization repair')
 return v

def matrix(U,k,unitary=False):
 if not isinstance(U,torch.Tensor)or U.shape!=(1<<k,1<<k)or U.dtype!=D or U.device.type!='cpu'or U.layout!=torch.strided or not bool(torch.isfinite(U).all()):raise ValueError('Finite local CPUcomplex128 square matrix required')
 if unitary and not torch.allclose(U.mH@U,torch.eye(1<<k,dtype=D),atol=1e-12,rtol=0):raise ValueError('Native gate contract requires a unitary matrix')
 return U

def axes(n,S):
 S=support(n,S);order=S+tuple(q for q in range(n)if q not in S)
 return order,tuple(order.index(q)for q in range(n))

def pack(v,n,S):
 vector(v,n);order,_=axes(n,S)
 return v.reshape((2,)*n).permute(order).reshape(1<<len(S),1<<(n-len(S)))

def apply(v,U,n,S):
 vector(v,n);support(n,S);matrix(U,len(S));order,inverse=axes(n,S)
 W=v.reshape((2,)*n).permute(order).reshape(1<<len(S),1<<(n-len(S)))
 changed=U@W
 return changed.reshape((2,)*n).permute(inverse).reshape(1<<n)

def permutation(n,S):
 support(n,S)
 if n>5:raise ValueError('Dense reference guard:n<=5')
 P=torch.zeros((1<<n,)*2,dtype=D);order,_=axes(n,S)
 for i in range(1<<n):
  bits=b.bits(i,n);j=b.index(tuple(bits[q]for q in order));P[j,i]=1
 return P

def embedded(U,n,S):
 support(n,S);matrix(U,len(S));P=permutation(n,S)
 return P.mH@torch.kron(U.contiguous(),torch.eye(1<<(n-len(S)),dtype=D))@P

def entry_matrix(U,n,S):
 support(n,S);matrix(U,len(S))
 if n>5:raise ValueError('Dense reference guard:n<=5')
 out=torch.zeros((1<<n,)*2,dtype=D);T=tuple(q for q in range(n)if q not in S)
 for i in range(1<<n):
  x=b.bits(i,n);a=b.index(tuple(x[q]for q in S))
  for j in range(1<<n):
   y=b.bits(j,n)
   if all(x[q]==y[q]for q in T):out[i,j]=U[a,b.index(tuple(y[q]for q in S))]
 return out

def scalar(v,U,n,S):
 # Output-centric gather: enumerate local input bits;no permute,reshape,kron or dense matrix.
 vector(v,n);support(n,S);matrix(U,len(S));out=[]
 for i in range(1<<n):
  x=b.bits(i,n);row=b.index(tuple(x[q]for q in S));z=0j
  for c in range(1<<len(S)):
   y=list(x)
   for q,bit in zip(S,b.bits(c,len(S))):y[q]=bit
   z+=U[row,c].item()*v[b.index(tuple(y))].item()
  out.append(z)
 return torch.tensor(out,dtype=D)

def check(v,U,n,S):
 out=apply(v,U,n,S);E=embedded(U,n,S);E2=entry_matrix(U,n,S)
 e.close(E,E2);e.close(out,E@v);e.close(out,scalar(v,U,n,S));return out

def execute(v,gates,n):
 out=vector(v,n).clone()
 for S,U in gates:out=apply(out,U,n,S)
 return out

def fourier(k):
 d=1<<k
 return torch.tensor([[cmath.exp(1j*(2*math.pi*a*c/d+.19*a))/math.sqrt(d)for c in range(d)]for a in range(d)],dtype=D)

def chain(n,S):
 U=fourier(len(S));V=torch.diag(torch.tensor([cmath.exp(-.37j),cmath.exp(.37j)],dtype=D))
 return [(S,U),((n-1,),V),(S,U.mH)]

def preparation(n,basis=None):
 c=fq.Circuit(n,dtype=D)
 if basis is not None:
  v=torch.zeros(1<<n,dtype=D);v[basis]=1
  for q,bit in enumerate(b.bits(basis,n)):
   if bit:c.X(q)
  return c,v
 factors=[]
 for q in range(n):
  t=.43+.17*q;p=-.31+.23*q;c.RY(q,theta=t).P(q,theta=p)
  factors.append((math.cos(t/2),cmath.exp(1j*p)*math.sin(t/2)))
 values=[]
 for i in range(1<<n):values.append(math.prod(factors[q][bit]for q,bit in enumerate(b.bits(i,n))))
 if n>1:
  c.CX(0,n-1);old=values.copy()
  for i in range(1<<n):
   bits=list(b.bits(i,n));bits[-1]^=bits[0];values[b.index(tuple(bits))]=old[i]
 return c,torch.tensor(values,dtype=D)

def native(n,S,mode='statevector',prefix=3,basis=None):
 global RUNS
 support(n,S)
 if not 1<=n<=5 or not S or mode not in('statevector','density_matrix')or type(prefix)is not int or not 1<=prefix<=3 or(basis is not None and(type(basis)is not int or not 0<=basis<1<<n)):raise ValueError('Bounded nonempty native unitary chain required')
 gates=chain(n,S)[:prefix]
 for T,U in gates:matrix(U,len(T),True)
 c,v=preparation(n,basis);expected=v.clone();dense=torch.eye(1<<n,dtype=D)
 for T,U in gates:
  expected=check(expected,U,n,T);dense=entry_matrix(U,n,T)@dense;c.unitary(*T,unitary=U.contiguous())
 e.close(expected,dense@v);e.close(expected,execute(v,gates,n))
 r=fq.run(c,outputs=[fq.probabilities(name='p'),fq.density_matrix(name='rho')],options=replace(e.OPTIONS,mode=mode));RUNS+=1
 e.close(r.measurement('p').value[0],abs(expected)**2);e.close(r.measurement('rho').value[0],expected[:,None]*expected.conj()[None,:])
 if mode=='statevector':e.close(r.statevector()[0],expected)
 inverse=[(T,U.mH)for T,U in reversed(gates)];e.close(execute(expected,inverse,n),v)
 RECEIPTS.append(dict(run=RUNS,n=n,support=S,mode=mode,prefix=prefix,basis=basis,gates=c.analysis().n_instructions,state_norm=float(torch.vdot(expected,expected).real),max_probability_residual=float((r.measurement('p').value[0]-abs(expected)**2).abs().max())))
 return r,v,expected

def invalid_checks():
 v=torch.ones(8,dtype=D);U=fourier(2)
 cases=[lambda:support(3,(0,0)),lambda:support(3,(3,)),lambda:support(3,(False,)),lambda:support(True,()),lambda:support(3,[2,0]),lambda:apply(v,U,3,(0,)),lambda:apply(v[None,:],U,3,(2,0)),lambda:apply(v.to(torch.complex64),U,3,(2,0)),lambda:apply(v,torch.full((4,4),float('nan'),dtype=D),3,(2,0)),lambda:apply(torch.full((8,),float('inf'),dtype=D),U,3,(2,0)),lambda:matrix(torch.zeros((2,2),dtype=D),1,True),lambda:permutation(6,(1,)),lambda:native(3,()),lambda:native(3,(2,0),mode='hardware')]
 before=RUNS
 for f in cases:
  try:f()
  except ValueError:pass
  else:raise AssertionError('Invalid local executor contract accepted')
 assert RUNS==before;return len(cases)

def main():
 classical=0
 for n in range(4):
  v=torch.tensor([complex(i%3-1,(2*i)%5-2)/7 for i in range(1<<n)],dtype=D)
  for k in range(n+1):
   for S in itertools.permutations(range(n),k):
    U=fourier(k);M=U.clone();M[0]*=2
    for A in(U,M):check(v,A,n,S);classical+=1
 assert classical==48
 for n in range(1,4):
  for k in range(1,n+1):
   for S in itertools.permutations(range(n),k):
    for mode in('statevector','density_matrix'):native(n,S,mode)
 for S in((3,1),(1,3),(2,0,3),(3,2,1,0)):
  for mode in('statevector','density_matrix'):native(4,S,mode)
 for prefix in(1,2):
  for mode in('statevector','density_matrix'):native(3,(2,0),mode,prefix)
 for basis in(0,1,5):
  for mode in('statevector','density_matrix'):native(3,(2,0),mode,basis=basis)
 assert RUNS==58
 _,v=preparation(3);storage=torch.zeros(16,dtype=D);storage[::2]=v;U=fourier(2);before=v.clone()
 e.close(apply(storage[::2],U,3,(2,0)),check(v,U,3,(2,0)));e.close(v,before)
 e.close(execute(v,[],3),v);e.close(apply(v,torch.eye(4,dtype=D),3,(2,0)),v)
 zero=torch.zeros_like(v);e.close(apply(zero,U,3,(2,0)),zero)
 assert not torch.allclose(apply(v,U,3,(2,0)),apply(v,U,3,(0,2)),atol=1e-12,rtol=0)
 assert invalid_checks()==14
 print('58 native CPU complex128 circuits: 48 three-gate chains, four shorter prefixes and six basis-input chains; both statevector and density-matrix modes.')
 print('48 classical linear-map cases include empty/full supports, n=0..3 and nonunitary maps; tensor, scalar gather, entry matrix and permutation-Kronecker references agree.')
 print('Chronological products and reversed adjoints agree; complex correlated inputs, nonadjacent/reversed supports, zero/identity and strided layouts passed.')
 print('14 malformed/native-boundary contracts rejected; no sorting, conjugating, clipping or normalization repair in the local kernel.')
 print('Book kernel forms no full-register operator; dense validation and native full-density requests are separate small-system diagnostics, not a memory benchmark.')
if __name__=='__main__':
 main()
 if len(__import__('sys').argv)>1:
  from pathlib import Path
  import json
  Path(__import__('sys').argv[1]).write_text(json.dumps(RECEIPTS,indent=2)+'\n')
