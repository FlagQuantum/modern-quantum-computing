"""14.2: uniform gate-list translation with explicit clean workspace."""
import itertools,math
from dataclasses import replace
import torch,flagquantum as fq
try:
 from examples.foundations import statistical_ensembles as e
except ModuleNotFoundError:
 import statistical_ensembles as e
D=e.D;RUNS=0
ARITY={'NOT':1,'COPY':1,'AND':2,'XOR':2,'ZERO':0,'ONE':0}

def validate(n,nodes,outputs):
 if type(n)is not int or not 0<=n<=32 or type(nodes)is not tuple or len(nodes)>64 or type(outputs)is not tuple or not 1<=len(outputs)<=16:raise ValueError('Bounded integer n/tuple gate list/nonempty output tuple required')
 for j,node in enumerate(nodes):
  if type(node)is not tuple or len(node)!=2 or node[0]not in ARITY or type(node[1])is not tuple or len(node[1])!=ARITY[node[0]]:raise ValueError('Supported opcode and matching source tuple required')
  if any(type(k)is not int or not 0<=k<n+j for k in node[1]):raise ValueError('Only earlier nodes/input labels allowed')
 if any(type(k)is not int or not 0<=k<n+len(nodes)for k in outputs):raise ValueError('Valid output taps required')
 return n,len(nodes),len(outputs)

def evaluate(x,nodes,outputs):
 if type(x)is not tuple or any(type(b)is not int or b not in (0,1)for b in x):raise ValueError('Literal input bit tuple required')
 validate(len(x),nodes,outputs);values=list(x)
 for op,args in nodes:
  a=[values[k]for k in args]
  values.append({'NOT':lambda:1-a[0],'COPY':lambda:a[0],'AND':lambda:a[0]*a[1],'XOR':lambda:a[0]^a[1],'ZERO':lambda:0,'ONE':lambda:1}[op]())
 return tuple(values[k]for k in outputs),tuple(values[len(x):])

def translate(n,nodes,outputs):
 n,L,m=validate(n,nodes,outputs);compute=[]
 for j,(op,args)in enumerate(nodes):
  t=n+j
  if op=='NOT':compute.extend((('X',(t,)),('CX',(args[0],t))))
  elif op=='COPY':compute.append(('CX',(args[0],t)))
  elif op=='ONE':compute.append(('X',(t,)))
  elif op=='XOR'and args[0]!=args[1]:compute.extend(('CX',(a,t))for a in args)
  elif op=='AND':compute.append(('CX',(args[0],t))if args[0]==args[1]else('CCX',args+(t,)))
 copy=[('CX',(source,n+L+j))for j,source in enumerate(outputs)]
 net=tuple(compute+copy+list(reversed(compute)))
 assert len(net)==2*len(compute)+m and len(net)<=4*L+m
 assert all(len(set(q))==len(q)for _,q in net)
 return net,dict(inputs=n,workspace=L,outputs=m,qubits=n+L+m,compute_gates=len(compute),network_gates=len(net))

def parity_family(n):
 if type(n)is not int or not 0<=n<=32:raise ValueError('Bounded literal length required')
 if n==0:return (('ZERO',()),),(0,)
 if n==1:return (), (0,)
 nodes=[('XOR',(0,1))]
 for i in range(2,n):nodes.append(('XOR',(n+len(nodes)-1,i)))
 return tuple(nodes),(n+len(nodes)-1,)

def bits(k,n):return tuple((k>>(n-1-j))&1 for j in range(n))
def index(b):return sum(v<<(len(b)-1-j)for j,v in enumerate(b))

def logical(n,m,coherent,x,y):
 if coherent:
  factors=[e.qubit(.37+.11*j,-.41+.17*j)for j in range(n+m)]
  v=torch.tensor([math.prod(factors[j][b].item()for j,b in enumerate(bits(k,n+m)))for k in range(2**(n+m))],dtype=D)
  out=torch.zeros_like(v)
  for k,z in enumerate(v):
   b=list(bits(k,n+m))
   if len(b)>1:b[-1]^=b[0]
   out[index(b)]=z
  return out
 out=torch.zeros(2**(n+m),dtype=D);out[index(x+y)]=1;return out

def execute(n,nodes,outputs,x=None,y=None,coherent=False,cycles=1,mode='statevector'):
 global RUNS
 net,cost=translate(n,nodes,outputs);L,m=cost['workspace'],cost['outputs'];q=cost['qubits']
 if q>8:raise ValueError('Native teaching guard totalqubits<=8')
 if type(coherent)is not bool or cycles not in (1,2)or type(cycles)is not int or mode not in ('statevector','density_matrix'):raise ValueError('Declared mode/cycles required')
 x=tuple(0 for _ in range(n))if x is None else x;y=tuple(0 for _ in range(m))if y is None else y
 if type(x)is not tuple or len(x)!=n or type(y)is not tuple or len(y)!=m or any(type(b)is not int or b not in (0,1)for b in x+y):raise ValueError('Matching input/output literal bit tuples required')
 c=fq.Circuit(q,dtype=D);labels=tuple(range(n))+tuple(range(n+L,q))
 if coherent:
  for j,label in enumerate(labels):c.RY(label,theta=.37+.11*j).P(label,theta=-.41+.17*j)
  if len(labels)>1:c.CX(labels[0],labels[-1])
 else:
  for label,b in zip(labels,x+y):
   if b:c.X(label)
 for _ in range(cycles):
  for op,qs in net:getattr(c,op)(*qs)
 inp=logical(n,m,coherent,x,y);target=torch.zeros(2**q,dtype=D)
 for k,z in enumerate(inp):
  b=bits(k,n+m);f,_=evaluate(b[:n],nodes,outputs);out=tuple(a^(b1 if cycles%2 else 0)for a,b1 in zip(b[n:],f))
  target[index(b[:n]+(0,)*L+out)]=z
 r=fq.run(c,outputs=[fq.density_matrix(name='full'),fq.probabilities(name='p')],options=replace(e.OPTIONS,mode=mode));RUNS+=1
 e.close(r.measurement('full').value[0],torch.outer(target,target.conj()));e.close(r.measurement('p').value[0],target.abs().square())
 if mode=='statevector':e.close(r.statevector()[0],target)
 leak=sum(r.measurement('p').value[0,k].item()for k in range(2**q)if any(bits(k,q)[n:n+L]))
 assert abs(leak)<1e-12
 return r,cost,leak

def invalid_checks():
 calls=[lambda:translate(True,(),(0,)),lambda:translate(1,(('AND',(0,)),),(1,)),lambda:translate(1,(('COPY',(1,)),),(1,)),lambda:translate(1,(('WHAT',(0,)),),(1,)),lambda:translate(1,(),()),lambda:translate(1,(),(True,)),lambda:translate(1,(),(1,)),lambda:execute(1,(),(0,),x=(2,)),lambda:execute(9,(),(0,)),lambda:parity_family(-1)]
 for call in calls:
  try:call()
  except ValueError:pass
  else:raise AssertionError('Invalid circuit contract accepted')
 return len(calls)

def fault(mode='statevector'):
 global RUNS
 # Deliberately omit inverse compute for f=a AND b.
 c=fq.Circuit(4,dtype=D).X(0).X(1).CCX(0,1,2).CX(2,3)
 r=fq.run(c,outputs=[fq.probabilities()],options=replace(e.OPTIONS,mode=mode));RUNS+=1
 assert r.probabilities[0,15].item()==1
 return r

def main():
 cases=[(2,(('AND',(0,1)),('NOT',(2,))),(3,)),(2,(('XOR',(0,1)),('AND',(0,1))),(2,3)),(1,(('XOR',(0,0)),('AND',(0,0)),('COPY',(2,))),(1,3)),(0,(('ZERO',()),('ONE',())),(0,1)),(2,(),(0,1))]
 for mode in ('statevector','density_matrix'):
  for n,nodes,outs in cases:
   for x in itertools.product((0,1),repeat=n):
    for y in itertools.product((0,1),repeat=len(outs)):execute(n,nodes,outs,x,y,mode=mode)
   execute(n,nodes,outs,coherent=True,mode=mode)
  n,nodes,outs=cases[0];execute(n,nodes,outs,coherent=True,cycles=2,mode=mode);fault(mode)
 for n in range(33):
  nodes,outs=parity_family(n);net,cost=translate(n,nodes,outs)
  for x in (tuple(0 for _ in range(n)),tuple(1 for _ in range(n))):assert evaluate(x,nodes,outs)[0]==(sum(x)%2,)
 assert RUNS==118
 print('118actual native circuits:104basis cases,10complex joint-input cases,2workspace reuse cases and2deliberate missing-uncompute cases passed.')
 print('Host parity-family generation/evaluation for lengths0..32passed;no large native execution claimed.')
 print(f'{invalid_checks()} malformed graph/input contracts rejected;gate bound2G+m<=4L+m checked.')
if __name__=='__main__':main()
