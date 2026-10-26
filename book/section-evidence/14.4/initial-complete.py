"""14.4: explicit bounded lookup/preparation examples and separate cost units."""
import itertools,math,hashlib,json
from dataclasses import replace
import torch,flagquantum as fq
try:
 from examples.foundations import statistical_ensembles as e,uniform_reversible as u
except ModuleNotFoundError:
 import statistical_ensembles as e,uniform_reversible as u
D=e.D;RUNS=0

def validate(table,a,b):
 if type(a)is not int or type(b)is not int or a not in (1,2)or b not in (1,2):raise ValueError('Teaching address/data widths1or2required')
 if type(table)is not tuple or len(table)!=2**a or any(type(v)is not int or not 0<=v<2**b for v in table):raise ValueError('Complete tuple of literal b-bit integers required;pad explicitly')
 return table

def fingerprint(table,a,b):
 validate(table,a,b);return hashlib.sha256(json.dumps([a,b,table]).encode()).hexdigest()

def build(table,a,b):
 validate(table,a,b);ops=[];active=0
 for i,v in enumerate(table):
  if not v:continue
  active+=1;negative=tuple(j for j,x in enumerate(u.bits(i,a))if x==0)
  ops.extend(('X',(j,))for j in negative)
  for k,bit in enumerate(u.bits(v,b)):
   if bit:ops.append(('CX',(0,a+k))if a==1 else('CCX',(0,1,a+k)))
  ops.extend(('X',(j,))for j in reversed(negative))
 cost=dict(table_words=len(table),serialized_bits=len(table)*b,address_qubits=a,data_qubits=b,
           active_words=active,X=sum(op=='X'for op,_ in ops),controlled_writes=sum(op!='X'for op,_ in ops),gates=len(ops))
 return tuple(ops),cost

def initial(a,b,i,y,coherent):
 if coherent:
  q=a+b;factors=[e.qubit(.41+.12*j,-.27+.19*j)for j in range(q)]
  v=torch.tensor([math.prod(factors[j][bit].item()for j,bit in enumerate(u.bits(k,q)))for k in range(2**q)],dtype=D)
  out=torch.zeros_like(v)
  for k,z in enumerate(v):
   bits=list(u.bits(k,q));bits[-1]^=bits[0];out[u.index(bits)]=z
  return out
 v=torch.zeros(2**(a+b),dtype=D);v[(i<<b)|y]=1;return v

def execute(table,a,b,i=0,y=0,coherent=False,repeats=1,mode='statevector'):
 global RUNS
 ops,cost=build(table,a,b)
 if type(i)is not int or not 0<=i<2**a or type(y)is not int or not 0<=y<2**b or type(coherent)is not bool or type(repeats)is not int or repeats not in (1,2)or mode not in ('statevector','density_matrix'):raise ValueError('Declared basis labels,coherence,repeats and tested mode required')
 c=fq.Circuit(a+b,dtype=D)
 if coherent:
  for j in range(a+b):c.RY(j,theta=.41+.12*j).P(j,theta=-.27+.19*j)
  c.CX(0,a+b-1)
 else:
  for j,bit in enumerate(u.bits(i,a)+u.bits(y,b)):
   if bit:c.X(j)
 for _ in range(repeats):
  for op,qs in ops:getattr(c,op)(*qs)
 v=initial(a,b,i,y,coherent)
 # Inverse-index pull is independent of the minterm gate list.
 target=torch.tensor([v[(x<<b)|(z^(table[x]if repeats%2 else 0))].item()for x in range(2**a)for z in range(2**b)],dtype=D)
 result=fq.run(c,outputs=[fq.density_matrix(name='rho'),fq.probabilities(name='full'),
    fq.probabilities(qubits=tuple(range(a,a+b)),name='data'),fq.samples(qubits=tuple(range(a,a+b)),name='record')],
    shots=11,options=replace(e.OPTIONS,mode=mode,seed=59));RUNS+=1
 e.close(result.measurement('rho').value[0],torch.outer(target,target.conj()));e.close(result.measurement('full').value[0],target.abs().square())
 if mode=='statevector':e.close(result.statevector()[0],target)
 marginal=torch.tensor([sum(abs(target[(x<<b)|z].item())**2 for x in range(2**a))for z in range(2**b)],dtype=torch.float64)
 e.close(result.measurement('data').value[0],marginal)
 record=result.measurement('record').value;assert record.shape==(1,11,b)and bool(((record==0)|(record==1)).all())
 if not coherent:assert bool((record==torch.tensor(u.bits(y^(table[i]if repeats%2 else 0),b))).all())
 return result,cost

def phase(table,a,minus=True,mode='statevector'):
 global RUNS
 ops,_=build(table,a,1)
 if type(minus)is not bool or mode not in ('statevector','density_matrix'):raise ValueError('Literal phase-target convention and tested mode required')
 c=fq.Circuit(a+1,dtype=D)
 for j in range(a):c.H(j)
 if minus:c.X(a)
 c.H(a)
 for op,qs in ops:getattr(c,op)(*qs)
 for j in range(a):c.H(j)
 N=2**a
 target=torch.tensor([sum((-1)**(sum(x*z for x,z in zip(u.bits(i,a),u.bits(k,a)))+(v+table[i]if minus else 0))for i in range(N))/(N*math.sqrt(2))for k in range(N)for v in (0,1)],dtype=D)
 result=fq.run(c,outputs=[fq.density_matrix(name='rho'),fq.probabilities(qubits=tuple(range(a)),name='address')],options=replace(e.OPTIONS,mode=mode));RUNS+=1
 e.close(result.measurement('rho').value[0],torch.outer(target,target.conj()))
 if mode=='statevector':e.close(result.statevector()[0],target)
 p=torch.tensor([sum(abs(target[2*k+v].item())**2 for v in (0,1))for k in range(N)],dtype=torch.float64);e.close(result.measurement('address').value[0],p)
 return result

def amplitude(d,twice=False,mode='statevector'):
 global RUNS
 if type(d)is not tuple or len(d)not in (2,4)or any(type(x)is not int or not 0<=x<=16 for x in d)or not any(d):raise ValueError('Nonzero tuple of2or4nonnegative integer entries0..16required')
 if type(twice)is not bool or mode not in ('statevector','density_matrix'):raise ValueError('Literal inverse flag and tested mode required')
 norm=math.sqrt(sum(x*x for x in d));v=torch.tensor([x/norm for x in d],dtype=D);e0=torch.zeros(len(d),dtype=D);e0[0]=1
 if torch.equal(v,e0):A=torch.eye(len(d),dtype=D)
 else:
  w=e0-v;A=torch.eye(len(d),dtype=D)-2*torch.outer(w,w.conj())/torch.vdot(w,w)
 e.close(A.mH@A,torch.eye(len(d),dtype=D));e.close(A@e0,v)
 n=len(d).bit_length()-1;c=fq.Circuit(n,dtype=D).unitary(*range(n),unitary=A)
 if twice:c.unitary(*range(n),unitary=A.mH.contiguous())
 target=e0 if twice else v
 result=fq.run(c,outputs=[fq.density_matrix(name='rho'),fq.probabilities(name='p')],options=replace(e.OPTIONS,mode=mode));RUNS+=1
 e.close(result.measurement('rho').value[0],torch.outer(target,target.conj()));e.close(result.measurement('p').value[0],target.abs().square())
 if mode=='statevector':e.close(result.statevector()[0],target)
 return result,dict(norm=norm,host_input_entries=len(d),dense_matrix_entries=len(d)**2,custom_unitary_calls=2 if twice else 1)

def ledger(table,a,b,calls_per_trial,trials):
 _,cost=build(table,a,b)
 if any(type(x)is not int or x<0 for x in (calls_per_trial,trials)):raise ValueError('Nonnegative literal query/trial counts required')
 return dict(classical_serialized_bits=cost['serialized_bits'],oracle_calls=calls_per_trial*trials,
             oracle_implementation_gates=cost['gates']*calls_per_trial*trials,setup_builds=1)

def invalid_checks():
 calls=[lambda:build((0,1,0),2,1),lambda:build((0,2),1,1),lambda:build((0,True),1,1),lambda:build((0,1),True,1),
        lambda:build((0,1),1,3),lambda:execute((0,1),1,1,i=2),lambda:execute((0,1),1,1,y=-1),lambda:execute((0,1),1,1,repeats=True),
        lambda:phase((0,2),1),lambda:amplitude((0,0)),lambda:amplitude((1,-1)),lambda:amplitude((1.,2.)),
        lambda:amplitude((1,2,3)),lambda:ledger((0,1),1,1,-1,1)]
 before=RUNS
 for call in calls:
  try:call()
  except ValueError:pass
  else:raise AssertionError('Malformed access model accepted')
 assert RUNS==before;return len(calls)

def main():
 tables=[((0,1),1,1),((0,3),1,2),((0,1,1,0),2,1),((0,1,3,2),2,2)]
 for mode in ('statevector','density_matrix'):
  for table,a,b in tables:
   for i in range(2**a):
    for y in range(2**b):execute(table,a,b,i,y,mode=mode)
   execute(table,a,b,coherent=True,mode=mode)
   execute(table,a,b,coherent=True,repeats=2,mode=mode)
  for table in ((0,1,1,0),(0,0,0,1)):
   for minus in (False,True):phase(table,2,minus,mode)
  for d in ((1,2),(1,2,2,1),(1,0,0,0),(2,4,4,2)):amplitude(d,mode=mode)
  for d in ((1,2),(1,2,2,1)):amplitude(d,twice=True,mode=mode)
 assert RUNS==108
 _,cost=build((0,1,3,2),2,2);assert cost['X']==4 and cost['controlled_writes']==4 and cost['gates']==8
 bill=ledger((0,1,3,2),2,2,2,5);assert bill==dict(classical_serialized_bits=8,oracle_calls=10,oracle_implementation_gates=80,setup_builds=1)
 assert fingerprint((0,1,3,2),2,2)!=fingerprint((0,1,2,2),2,2)
 print('108 actual native circuits:72basis,8complex lookup,8two-query cancellation,8phase-interface and12amplitude preparation/inverse cases passed.')
 print('Both CPUcomplex128 modes checked against full scalar amplitude/density references;terminal lookup records validated.')
 print('Gray lookup:one abstract query expands to4X+4CCX;five two-query trials use10calls/80implementation gates;8classical data bits separate.')
 print(f'{invalid_checks()} malformed access contracts rejected;no QRAM,free generic loading or query-to-runtime equivalence claimed.')
if __name__=='__main__':main()
