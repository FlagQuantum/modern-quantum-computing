"""44.3: independent expectation,marginal,prefix and exact-rational sampling references."""
import math,cmath,itertools,random,bisect
from fractions import Fraction as F
from dataclasses import replace
import torch,flagquantum as fq
try:
 from examples.foundations import tensor_gate_executor as t,statistical_ensembles as e,uniform_reversible as b
except ModuleNotFoundError:
 import tensor_gate_executor as t,statistical_ensembles as e,uniform_reversible as b
D=torch.complex128
RUNS=0
RECEIPTS=[]
X=torch.tensor([[0,1],[1,0]],dtype=D);Y=torch.tensor([[0,-1j],[1j,0]],dtype=D);Z=torch.diag(torch.tensor([1,-1],dtype=D));H=torch.tensor([[1,1],[1,-1]],dtype=D)/math.sqrt(2)

def state(v,n):
 t.vector(v,n)
 if n>5 or abs(torch.vdot(v,v).item()-1)>1e-12:raise ValueError('Normalized finite CPUcomplex128 pure state on0..5qubits required')
 return v

def probabilities(v,n,Q):
 state(v,n);W=t.pack(v,n,Q);sq=W.abs().square()
 if bool(((W!=0)&(sq==0)).any()):raise FloatingPointError('Positive amplitude contribution squared to zero')
 return sq.sum(1)

def expectation(v,A,n,Q):
 state(v,n);t.support(n,Q);t.matrix(A,len(Q))
 if not torch.allclose(A,A.mH,atol=1e-12,rtol=0):raise ValueError('Hermitian local observable required;no symmetrization')
 z=torch.vdot(v,t.apply(v,A,n,Q))
 if abs(z.imag.item())>1e-12:raise ArithmeticError('Unexpected imaginary expectation residual')
 return z.real

def pauli(v,n,word):
 state(v,n)
 if type(word)is not str or len(word)!=n or any(c not in'IXYZ'for c in word):raise ValueError('One Pauli letter per logical qubit required')
 flip=sign=ny=0
 for q,c in enumerate(word):
  bit=1<<(n-1-q)
  if c in'XY':flip|=bit
  if c in'YZ':sign|=bit
  if c=='Y':ny+=1
 phase=1j**ny;z=0j
 for i in range(1<<n):
  gamma=phase*(-1)**((i&sign).bit_count())
  z+=v[i^flip].item().conjugate()*gamma*v[i].item()
 assert abs(z.imag)<1e-12;return z.real

def branch(v,n,Q,prefix):
 state(v,n);t.support(n,Q)
 if type(prefix)is not tuple or len(prefix)>len(Q)or any(type(x)is not int or x not in(0,1)for x in prefix):raise ValueError('Literal bit prefix of the ordered mask required')
 w=v.clone()
 for i in range(1<<n):
  x=b.bits(i,n)
  if any(x[q]!=bit for q,bit in zip(Q,prefix)):w[i]=0
 p=float(torch.vdot(w,w).real)
 if p==0:
  if bool((w!=0).any()):raise FloatingPointError('Nonzero projected branch squared to zero')
  return 0.,None
 out=w/math.sqrt(p)
 if not bool(torch.isfinite(out).all()):raise FloatingPointError('Unrepresentable conditional state')
 e.close(torch.vdot(out,out),torch.tensor(1,dtype=D));return p,out

def check_prefixes(v,n,Q):
 p=probabilities(v,n,Q);count=0
 for length in range(len(Q)+1):
  for prefix in itertools.product((0,1),repeat=length):
   w,c=branch(v,n,Q,prefix);diagonal=torch.tensor([int(all(b.bits(i,n)[q]==bit for q,bit in zip(Q,prefix)))for i in range(1<<n)],dtype=D);projector=torch.diag(diagonal);projected=projector@v
   e.close(torch.tensor(w,dtype=torch.float64),torch.vdot(projected,projected).real)
   if c is None:assert bool((projected==0).all())
   else:e.close(c,projected/math.sqrt(w))
   if length<len(Q):
    children=[branch(v,n,Q,prefix+(bit,))[0]for bit in(0,1)];assert abs(sum(children)-w)<1e-12
    if c is not None:
     for bit in(0,1):
      cp=probabilities(c,n,(Q[length],))[bit];e.close(cp,torch.tensor(children[bit]/w,dtype=torch.float64))
   else:e.close(torch.tensor(w,dtype=torch.float64),p[b.index(prefix)])
   count+=1
 return count

class Sampler:
 def __init__(self,ps):
  if type(ps)is not tuple or not ps or len(ps)>32 or len(ps)&(len(ps)-1)or any(type(p)is not F or p<0 for p in ps)or sum(ps)!=1:raise ValueError('Power-of-two exact nonnegative rational law,normalized without repair required')
  self.K=len(ps);self.width=self.K.bit_length()-1;self.D=math.lcm(*(p.denominator for p in ps))
  if self.D.bit_length()>128:raise ValueError('Reference integer mass guard:128bits')
  self.mass=[0]*(2*self.K);self.cdf=[];total=0
  for j,p in enumerate(ps):self.mass[self.K+j]=int(p*self.D);total+=int(p*self.D);self.cdf.append(total)
  for j in range(self.K-1,0,-1):self.mass[j]=self.mass[2*j]+self.mass[2*j+1]
  assert self.mass[1]==self.D
 def at(self,rank,method='prefix'):
  if type(rank)is not int or not 0<=rank<self.D or method not in('prefix','cdf'):raise ValueError('Integer rank in half-open0..D and named sampler required')
  if method=='cdf':return bisect.bisect_right(self.cdf,rank)
  node=1
  while node<self.K:
   left=self.mass[2*node]
   if rank<left:node*=2
   else:rank-=left;node=2*node+1
  return node-self.K
 def conditional(self,prefix):
  if type(prefix)is not tuple or len(prefix)>=self.width or any(type(x)is not int or x not in(0,1)for x in prefix):raise ValueError('Proper literal bit prefix required')
  node=(1<<len(prefix))+b.index(prefix);M=self.mass[node]
  return None if M==0 else(F(self.mass[2*node],M),F(self.mass[2*node+1],M))
 def draw(self,shots,seed=101,method='prefix'):
  if type(shots)is not int or not 1<=shots<=10000 or type(seed)is not int:raise ValueError('Literal1..10000record count and integer seed required')
  rng=random.Random(seed);return tuple(self.at(rng.randrange(self.D),method)for _ in range(shots))

def exact_sampler_check(ps):
 s=Sampler(ps)
 if s.D>4096:raise ValueError('Exhaustive-rank validation guard:D<=4096')
 counts=[0]*s.K
 for r in range(s.D):
  a=s.at(r);assert a==s.at(r,'cdf');counts[a]+=1
 assert tuple(F(c,s.D)for c in counts)==ps
 for k in range(s.width):
  for prefix in itertools.product((0,1),repeat=k):
   c=s.conditional(prefix)
   if c is not None:assert sum(c)==1
 return s.D

def preparation(n,angles):
 c=fq.Circuit(n,dtype=D);factors=[]
 for q in range(n):
  theta,phi=(angles[:2]if q==0 else angles[2:]if q==1 else(0.,0.)if q==2 else(.37+.13*q,-.22*q))
  c.RY(q,theta=theta).P(q,theta=phi);factors.append((math.cos(theta/2),cmath.exp(1j*phi)*math.sin(theta/2)))
 v=torch.tensor([math.prod(factors[q][bit]for q,bit in enumerate(b.bits(i,n)))for i in range(1<<n)],dtype=D)
 c.CX(0,2).CX(1,2);out=torch.zeros_like(v)
 for i in range(1<<n):
  bits=list(b.bits(i,n));bits[2]^=bits[0]^bits[1];out[b.index(tuple(bits))]=v[i]
 return c,out

def native(n,Q,angles,mode='statevector',analyzer=False,shots=31,seed=101):
 global RUNS
 t.support(n,Q)
 if not 3<=n<=5 or not Q or mode not in('statevector','density_matrix')or type(analyzer)is not bool or type(shots)is not int or not 1<=shots<=1000 or type(angles)is not tuple or len(angles)!=4 or any(type(x)not in(int,float)or not math.isfinite(x)for x in angles):raise ValueError('Bounded CPU terminal measurement profile required')
 c,v=preparation(n,angles);prepared=v.clone();word='YIX'+'I'*(n-3);R=fq.Y(0)@fq.X(2);nativeH=.7*R-.2*fq.Z(0)+.4*fq.Z(1)
 mu=pauli(v,n,word);muH=.7*mu-.2*pauli(v,n,'Z'+'I'*(n-1))+.4*pauli(v,n,'IZ'+'I'*(n-2))
 assert abs(mu-math.sin(angles[0])*math.sin(angles[1]))<1e-12
 if analyzer:
  c.P(0,theta=-math.pi/2).H(0).H(2);A0=H@torch.diag(torch.tensor([1,-1j],dtype=D));v=t.apply(t.apply(v,A0,n,(0,)),H,n,(2,));R=fq.Z(0)@fq.Z(2)
 outputs=[fq.probabilities(qubits=Q,name='p'),fq.expectation(R,name='r'),fq.samples(qubits=Q,name='raw'),fq.density_matrix(name='rho')]
 if not analyzer:outputs.append(fq.expectation(nativeH,name='hamiltonian_mean'))
 r=fq.run(c,outputs=outputs,shots=shots,options=replace(e.OPTIONS,mode=mode,seed=seed));RUNS+=1
 p=probabilities(v,n,Q);e.close(r.measurement('p').value[0],p);e.close(r.measurement('r').value[0],torch.tensor(mu,dtype=torch.float64));e.close(r.measurement('rho').value[0],v[:,None]*v.conj()[None,:])
 if not analyzer:e.close(r.expectation('hamiltonian_mean')[0],torch.tensor(muH,dtype=torch.float64))
 if mode=='statevector':e.close(r.statevector()[0],v)
 if not analyzer:
  local=torch.kron(X,Y);e.close(expectation(v,local,n,(2,0)),torch.tensor(mu,dtype=torch.float64));e.close(expectation(v,local,n,(2,0)),torch.vdot(v,t.entry_matrix(local,n,(2,0))@v).real)
 # Independent full probability marginalization by scalar global coordinates.
 direct=[0.]*(1<<len(Q))
 for i,z in enumerate(v.tolist()):direct[b.index(tuple(b.bits(i,n)[q]for q in Q))]+=abs(z)**2
 e.close(p,torch.tensor(direct,dtype=torch.float64));branches=check_prefixes(v,n,Q)
 raw=r.measurement('raw').value[0];assert raw.shape==(shots,len(Q))and bool(((raw==0)|(raw==1)).all())
 RECEIPTS.append(dict(n=n,qubits=Q,angles=angles,mode=mode,analyzer=analyzer,shots=shots,seed=seed,probabilities=p.tolist(),expectation_R=mu,expectation_H=muH if not analyzer else None,prefix_nodes_checked=branches,raw_rows=raw.tolist(),raw_tensor_bytes=raw.numel()*raw.element_size()))
 return r,v,p

def calibrate(n,Q,bits,mode='statevector',shots=5):
 global RUNS
 t.support(n,Q)
 if not 3<=n<=5 or not Q or type(bits)is not tuple or len(bits)!=n or any(type(x)is not int or x not in(0,1)for x in bits)or mode not in('statevector','density_matrix')or type(shots)is not int or not 1<=shots<=1000:raise ValueError('Bounded exact-basis label calibration required')
 c=fq.Circuit(n,dtype=D)
 for q,bit in enumerate(bits):
  if bit:c.X(q)
 r=fq.run(c,outputs=[fq.probabilities(qubits=Q,name='p'),fq.samples(qubits=Q,name='raw')],shots=shots,options=replace(e.OPTIONS,mode=mode,seed=809));RUNS+=1
 label=tuple(bits[q]for q in Q);expected=torch.zeros(1<<len(Q),dtype=torch.float64);expected[b.index(label)]=1
 assert torch.equal(r.measurement('p').value[0],expected)
 raw=r.measurement('raw').value[0];assert raw.tolist()==[list(label)for _ in range(shots)]
 RECEIPTS.append(dict(kind='basis-label-calibration',n=n,qubits=Q,basis_bits=bits,mode=mode,shots=shots,expected_label=label,raw_rows=raw.tolist()))
 return r


def invalid_checks():
 v=torch.tensor([1.,0.],dtype=D);s=Sampler((F(1,2),F(1,2)));cases=[lambda:state(2*v,1),lambda:probabilities(v,1,(0,0)),lambda:probabilities(v.real,1,(0,)),lambda:expectation(v,torch.tensor([[0,1],[0,0]],dtype=D),1,(0,)),lambda:pauli(v,1,'A'),lambda:branch(v,1,(0,),(2,)),lambda:Sampler((.5,.5)),lambda:Sampler((F(1,3),F(1,3))),lambda:Sampler((F(1),F(-1))),lambda:s.at(s.D),lambda:s.at(-1),lambda:s.at(True),lambda:s.draw(0),lambda:s.conditional((0,)),lambda:native(3,(),(0.,0.,0.,0.))]
 before=RUNS
 for call in cases:
  try:call()
  except ValueError:pass
  else:raise AssertionError('Invalid measurement execution contract accepted')
 rare=torch.tensor([1.,1e-10j],dtype=D);p,c=branch(rare,1,(0,),(1,));assert 0<p<1e-12;e.close(c,torch.tensor([0,1j],dtype=D))
 for f in(lambda:branch(torch.tensor([1.,1e-200j],dtype=D),1,(0,),(1,)),lambda:probabilities(torch.tensor([1.,1e-200j],dtype=D),1,(0,))):
  try:f()
  except FloatingPointError:pass
  else:raise AssertionError('Positive squared-norm underflow silently discarded')
 assert RUNS==before;return len(cases)

def main():
 specs=((math.pi/2,math.pi/2,math.pi/3,math.pi/2),(.47,-.61,1.13,.37),(0.,.4,0.,-.2))
 for n in(3,4):
  for angles in specs:
   for Q in((2,0),(0,2,1)if n==3 else(3,2,0)):
    for mode in('statevector','density_matrix'):
     for analyzer in(False,True):native(n,Q,angles,mode,analyzer)
 assert RUNS==48
 laws=((F(3,8),F(1,8),F(1,8),F(3,8)),(F(1,2),F(0),F(0),F(1,2)),(F(0),F(1,4),F(0),F(3,4)),(F(1),),(F(1,12),F(2,12),F(3,12),F(6,12)))
 ranks=sum(exact_sampler_check(ps)for ps in laws);assert ranks==27
 assert Sampler(laws[1]).conditional((0,))==(F(1),F(0))
 assert Sampler(laws[2]).at(0)==1 and Sampler(laws[2]).at(1)==3
 assert Sampler(laws[1]).draw(31)==Sampler(laws[1]).draw(31,method='cdf')
 assert invalid_checks()==15
 print('48 native CPU complex128 circuits: three- and four-qubit preparations,two ordered masks,both execution modes and computational/Y-X analyzer profiles.')
 print('Exact Pauli/local contractions,marginals and every prefix branch agree with scalar/dense references; native terminal samples checked for schema,not frequency hits.')
 print('Five exact rational laws,27 integer ranks: CDF and cached-prefix samplers reproduce every outcome mass,including zero leaves and boundary ranks.')
 print('15 malformed contracts rejected; positive1e-20 branch retained and two squared-norm underflow routes explicitly rejected.')
 print('Book conditional states and exact-rational samplers are separate from native terminal requests; no collapse/reset,hardware IID certificate or shared random-stream claim.')
if __name__=='__main__':
 main()
 if len(__import__('sys').argv)>1:
  from pathlib import Path
  import json
  Path(__import__('sys').argv[1]).write_text(json.dumps(RECEIPTS,indent=2)+'\n')
