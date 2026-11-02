"""44.6 bounded CPU precision diagnostics; no normalization is applied to native output."""
import math, json
from decimal import Decimal, localcontext
from dataclasses import replace
import torch
import flagquantum as fq
try:
 from examples.foundations.tensor_spaces import OPTIONS
except ModuleNotFoundError:
 from tensor_spaces import OPTIONS
RUNS=0
RECEIPTS=[]

def vector(v):
 if not isinstance(v,torch.Tensor) or v.device.type!='cpu' or v.layout!=torch.strided or v.dtype not in(torch.complex64,torch.complex128) or v.ndim!=1 or len(v) not in(2,4,8,16,32) or not bool(torch.isfinite(v).all()):
  raise ValueError('Finite dense CPU complex64/128 vector of 1..5 qubits required')
 return v

def norm(v):
 vector(v)
 # Scale before squaring, including when the original components are subnormal.
 w=v.to(torch.complex128);scale=max(float(w.real.abs().max()),float(w.imag.abs().max()))
 if scale==0:return 0.
 return scale*float(torch.linalg.vector_norm(w/scale))

def normalize(v):
 vector(v);r=norm(v)
 if r==0:raise ValueError('Zero vector has no normalized direction')
 # Divide in the original dtype; fail if it cannot represent this diagnostic.
 out=v/r
 if not bool(torch.isfinite(out).all()):raise FloatingPointError('Normalization is not representable in the declared dtype')
 return out

def metrics(w,v):
 vector(w);vector(v)
 if w.shape!=v.shape or abs(norm(v)-1)>1e-12:raise ValueError('Same shape and normalized complex reference required')
 a=w.to(torch.complex128);b=v.to(torch.complex128);r=norm(a);E=norm(a-b)
 return dict(norm=r,drift=abs(r*r-1),error=E,event_error=float((a.abs().square()-b.abs().square()).abs().max()),bound=E*(2+E))

def trig(x,precision=80):
 if type(x)is not Decimal or not x.is_finite() or abs(x)>20 or type(precision)is not int or not 50<=precision<=100:raise ValueError('Finite Decimal angle <=20 radians and 50..100 digits required')
 with localcontext() as ctx:
  ctx.prec=precision;ss=st=x;cc=ct=Decimal(1)
  for k in range(1,180):
   st=-st*x*x/Decimal((2*k)*(2*k+1));ct=-ct*x*x/Decimal((2*k-1)*(2*k));ss+=st;cc+=ct
  return +ss,+cc

def reference(L,theta,phi,precision=80):
 contract(L,theta,phi,torch.complex128)
 with localcontext() as ctx:
  ctx.prec=precision
  s,c=trig(Decimal(L)*Decimal.from_float(theta)/2,precision)
  sp,cp=trig(Decimal(L)*Decimal.from_float(phi),precision)
  return torch.tensor([complex(float(c),0),0,0,complex(float(s*cp),float(s*sp))],dtype=torch.complex128)

def contract(L,theta,phi,dtype):
 if type(L)is not int or not 1<=L<=512 or type(theta)not in(int,float) or type(phi)not in(int,float) or not math.isfinite(theta) or not math.isfinite(phi) or abs(L*theta)>20 or abs(L*phi)>20 or dtype not in(torch.complex64,torch.complex128):raise ValueError('L1..512,finite radian angles with accumulated magnitude<=20,and complex64/128 required')

def native(L,theta,phi,dtype):
 global RUNS
 contract(L,theta,phi,dtype)
 c=fq.Circuit(2,dtype=dtype)
 for _ in range(L):c.ry(0,theta)
 for _ in range(L):c.p(0,phi)
 c.cx(0,1)
 precision='complex64' if dtype==torch.complex64 else 'complex128'
 r=fq.run(c,outputs=[fq.probabilities(name='p'),fq.expectation(fq.X(0)@fq.X(1),name='xx')],options=replace(OPTIONS,precision=precision))
 RUNS+=1;w=r.statevector()[0]
 assert w.dtype==dtype
 v=reference(L,theta,phi);assert torch.equal(v,reference(L,theta,phi,60))
 m=metrics(w,v);p=r.probabilities('p')[0].to(torch.float64);xx=float(r.expectation('xx')[0])
 tol=3e-4 if dtype==torch.complex64 else 1e-11
 assert m['error']<tol and m['drift']<tol and m['event_error']<tol,(L,dtype,m)
 assert float((p-w.to(torch.complex128).abs().square()).abs().max())<tol
 target=2*(v[0].conj()*v[3]).real.item()
 assert abs(xx-target)<2*tol and abs(xx-float(torch.vdot(w.to(torch.complex128),w.to(torch.complex128)[torch.tensor([3,2,1,0])]).real))<tol
 assert m['event_error']<=m['bound']+1e-14
 RECEIPTS.append(dict(L=L,theta=theta,phi=phi,precision=precision,submitted_gates=2*L+1,xx_error=abs(xx-target),**m))
 return w,v,m

def local_trace(L=64,theta=.037,dtype=torch.complex64):
 contract(L,theta,0.,dtype)
 U=torch.tensor([[math.cos(theta/2),-math.sin(theta/2)],[math.sin(theta/2),math.cos(theta/2)]],dtype=torch.complex128)
 A=U.to(dtype);w=torch.tensor([1,0],dtype=dtype);v=w.to(torch.complex128);budget=0.;rows=[]
 for _ in range(L):
  prev=w.to(torch.complex128);w=A@w;f=w.to(torch.complex128)-U@prev
  eta=norm(f);budget+=eta;v=U@v;E=norm(w.to(torch.complex128)-v)
  assert E<=budget+2e-13
  delta=float(torch.linalg.matrix_norm(A.to(torch.complex128)-U,ord=2));rounding=norm(w.to(torch.complex128)-A.to(torch.complex128)@prev)
  assert eta<=delta*norm(prev)+rounding+1e-14
  rows.append(dict(eta=eta,budget=budget,error=E))
 return w,v,rows

def examples():
 d=2**-25;one=torch.tensor(1.,dtype=torch.float32)
 assert float((one+d)-one)==0 and float(((one+d)-one).double())==0
 assert float((torch.tensor(1.,dtype=torch.float64)+d)-1)==d
 a=torch.tensor(2**25,dtype=torch.float32);assert float((a+1)-a)==0 and float((a-a)+1)==1
 # Exact dyadic synthetic residuals: U_j=I and f_j=2^-12 |0>.
 v=torch.tensor([1,0],dtype=torch.complex128);w=v.clone();eta=2**-12
 for _ in range(4):w+=torch.tensor([eta,0],dtype=torch.complex128)
 m=metrics(w,v);assert m['error']==4*eta and m['drift']==m['bound']
 corrected=normalize(w);assert torch.equal(corrected,v)
 plus=torch.tensor([1,1],dtype=torch.complex128)/math.sqrt(2);minus=plus*torch.tensor([1,-1])
 assert abs(norm(minus)-1)<1e-15 and norm(normalize(minus)-plus)>1.4
 # Rare selected branches can change direction although total vector error is small.
 p=1e-12;v=torch.tensor([math.sqrt(1-p),math.sqrt(p),0,0],dtype=torch.complex128);w=torch.tensor([math.sqrt(1-p),0,math.sqrt(p),0],dtype=torch.complex128)
 E=norm(w-v);assert E<2e-6
 mask=torch.tensor([0,1,1,0],dtype=torch.complex128)
 b=normalize(v*mask);a=normalize(w*mask);assert norm(a-b)>1.4 and norm(a-b)<=2*E/math.sqrt(p)
 tiny=torch.tensor([1e-200,1e-200j],dtype=torch.complex128)
 assert norm(tiny)>0 and abs(norm(normalize(tiny))-1)<1e-14
 assert float(tiny.abs().square().sum())==0
 return m

def errors():
 v=torch.tensor([1,0],dtype=torch.complex128)
 calls=[lambda:normalize(v*0),lambda:vector(v.real),lambda:vector(v.reshape(1,2)),lambda:vector(torch.tensor([complex('nan'),0],dtype=torch.complex128)),lambda:metrics(v,torch.ones(4,dtype=torch.complex128)/2),lambda:metrics(v,v*2),lambda:contract(True,.1,.1,torch.complex128),lambda:contract(0,.1,.1,torch.complex128),lambda:contract(513,.1,.1,torch.complex128),lambda:contract(1,float('nan'),.1,torch.complex128),lambda:contract(512,1.,.1,torch.complex128),lambda:contract(1,.1,.1,torch.float64),lambda:trig(Decimal('Infinity')),lambda:trig(Decimal(1),20)]
 for f in calls:
  try:f()
  except(ValueError,FloatingPointError):pass
  else:raise AssertionError('Malformed contract accepted')
 return len(calls)

def main():
 examples();assert errors()==14
 for dtype in(torch.complex64,torch.complex128):
  for L in(1,7,64,257):
   for theta,phi in((.017,.023),(-.031,.019),(.041,-.013)):native(L,theta,phi,dtype)
 for dtype in(torch.complex64,torch.complex128):
  for L in(1,7,64,257):local_trace(L,.037,dtype)
 assert RUNS==24
 print('24 native CPU statevector runs: two precisions, four depths, three signed angle pairs passed.')
 print('Decimal 60/80-digit references agree after binary64 export; raw state, norm, probabilities and XX checked.')
 print('8 local residual traces; cancellation, radial drift, phase loss, rare conditioning and scaled-norm checks passed.')
 print('14 malformed contracts rejected; no native output renormalization or phase alignment applied.')
 if __name__=='__main__':
  pass
if __name__=='__main__':main()
