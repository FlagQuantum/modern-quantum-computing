"""14.6: declared logical costs, terminal evidence and independent host references."""
import math,itertools
from fractions import Fraction as F
from dataclasses import dataclass,replace
import torch,flagquantum as fq
try:
 from examples.foundations import statistical_ensembles as e,uniform_reversible as u,accuracy_repetition as a
except ModuleNotFoundError:
 import statistical_ensembles as e,uniform_reversible as u,accuracy_repetition as a
RUNS=0

def integer(x,minimum=0):
 if type(x)is not int or x<minimum:raise ValueError('Literal integer within the declared range required')
 return x
@dataclass(frozen=True)
class Work:
 gates:int=0
 queries:int=0
 prepared:int=0
 measured:int=0
 read_bits:int=0
 write_bits:int=0
 def __post_init__(self):
  for x in self.__dict__.values():integer(x)
 def __add__(self,other):
  if type(other)is not Work:raise ValueError('Matching cost units required')
  return Work(*(x+y for x,y in zip(self.__dict__.values(),other.__dict__.values())))
 def scale(self,n):
  integer(n);return Work(*(n*x for x in self.__dict__.values()))

def layers(supports,width):
 integer(width,1);last=[0]*width;out=[]
 if type(supports)is not tuple:raise ValueError('Tuple gate supports required')
 for qs in supports:
  if type(qs)is not tuple or not qs or len(set(qs))!=len(qs)or any(type(q)is not int or not 0<=q<width for q in qs):raise ValueError('Nonempty distinct in-range ordered support required')
  finish=1+max(last[q]for q in qs);out.append(finish)
  for q in qs:last[q]=finish
 return tuple(out),max(last)

def repeat_plan(n,shots,parallel=1,full=False,bits=16):
 integer(n);integer(shots,1);integer(parallel,1);integer(bits,1)
 if n>100 or shots>10000 or parallel>shots or type(full)is not bool:raise ValueError('Bounded host plan n<=100,shots<=10000,parallel<=shots and literal full flag required')
 w=n+1;k=w if full else 1;d=n+1 if n else 0
 return dict(one=Work(gates=2*n,prepared=w,measured=k,write_bits=k),
   total=Work(gates=2*n,prepared=w,measured=k,write_bits=k).scale(shots),
   input_bits=n*bits,peak_qubits=parallel*w,depth_bound=math.ceil(shots/parallel)*d,
   rounds=math.ceil(shots/parallel),record_payload_bits=shots*k,counter_bits=shots.bit_length(),
   exact_report_bits=2*shots.bit_length(),circuit_builds=1,native_invocations=1)

def substitute(outer_gates,calls,oracle_gates,repeats,setup_bits):
 for x in (outer_gates,calls,oracle_gates,repeats,setup_bits):integer(x)
 return dict(queries=calls*repeats,logical_gates=(outer_gates+calls*oracle_gates)*repeats,setup_bits=setup_bits)

def failure_total(bounds):
 if type(bounds)is not tuple or any(type(x)is not F or not 0<=x<=1 for x in bounds):raise ValueError('Exact event bounds in[0,1]required')
 return min(F(1),sum(bounds,F(0)))

def adaptive_first_failure(ps):
 # Enumerate a bounded two-stage tree: stage2 failure may depend on stage1 history.
 if type(ps)is not tuple or len(ps)!=3 or any(type(x)is not F or not 0<=x<=1 for x in ps):raise ValueError('Three exact branch probabilities required')
 p,p_bad,p_good=ps
 rows={(b1,b2):(p if b1 else 1-p)*( (p_bad if b1 else p_good)if b2 else (1-p_bad if b1 else 1-p_good))for b1,b2 in itertools.product((0,1),repeat=2)}
 assert sum(rows.values())==1
 bad=sum(w for (b1,b2),w in rows.items()if b1 or b2)
 assert bad==p+(1-p)*p_good and bad<=failure_total((p,p_good))
 return bad

def simulate(angles,shots=23,mode='statevector',full=False):
 global RUNS
 if type(angles)is not tuple or len(angles)>4 or any(type(x)not in (int,float)or not math.isfinite(x)for x in angles)or mode not in ('statevector','density_matrix'):raise ValueError('Finite radian tuple n<=4 and tested mode required')
 plan=repeat_plan(len(angles),shots,full=full);n=len(angles);w=n+1
 c=fq.Circuit(w,dtype=torch.complex128)
 for j,theta in enumerate(angles):c.RY(j,theta=theta)
 for j in range(n):c.CX(j,n)
 ir=c.to_ir();supports=tuple(tuple(op.wires)for op in ir.instructions)
 layer,depth=layers(supports,w);analysis=c.analysis()
 assert len(ir.instructions)==2*n and analysis.n_instructions==2*n
 assert analysis.depth==depth==(n+1 if n else 0)
 assert analysis.gate_counts==({'ry':n,'cx':n}if n else {})
 target=torch.zeros(2**w,dtype=torch.complex128)
 for data in itertools.product((0,1),repeat=n):
  z=sum(data)%2;amp=math.prod(math.sin(t/2)if bit else math.cos(t/2)for bit,t in zip(data,angles))
  target[u.index(data+(z,))]=amp
 q=(1-math.prod(math.cos(t)for t in angles))/2
 selected=tuple(range(w))if full else(n,)
 r=fq.run(c,outputs=[fq.density_matrix(name='rho'),fq.probabilities(qubits=(n,),name='out'),fq.samples(qubits=selected,name='raw')],
   shots=shots,options=replace(e.OPTIONS,mode=mode,seed=67));RUNS+=1
 e.close(r.measurement('rho').value[0],torch.outer(target,target.conj()))
 e.close(r.measurement('out').value[0],torch.tensor([1-q,q],dtype=torch.float64))
 if mode=='statevector':e.close(r.statevector()[0],target)
 raw=r.measurement('raw').value;assert raw.shape==(1,shots,len(selected))and bool(((raw==0)|(raw==1)).all())
 if full:assert bool((raw[0,:,-1]==raw[0,:,:-1].sum(dim=1)%2).all())
 count=sum(int(x)for x in raw[0,:,-1]);estimate=F(count,shots)
 assert 0<=estimate<=1 and count.bit_length()<=plan['counter_bits']
 payload=raw.numel();storage=raw.numel()*raw.element_size()
 assert payload==plan['record_payload_bits']and storage>=math.ceil(payload/8)
 return r,plan,dict(q=q,estimate=estimate,record_tensor_bytes=storage,logical_payload_bits=payload,depth=depth)

def simulator_storage(width):
 integer(width,1)
 if width>20:raise ValueError('Storage arithmetic teaching guard width<=20')
 return dict(statevector_bytes=16*2**width,density_bytes=16*4**width)

def invalid_checks():
 calls=[lambda:Work(gates=-1),lambda:Work(gates=True),lambda:repeat_plan(3,0),lambda:repeat_plan(3,9,parallel=10),lambda:repeat_plan(3,9,bits=0),lambda:repeat_plan(3,9,full=1),lambda:layers(((0,0),),1),lambda:layers(((2,),),2),lambda:substitute(1,-1,3,4,8),lambda:failure_total((.1,)),lambda:simulate((math.nan,)),lambda:simulate((0.,)*5),lambda:simulate((0.,),mode='hardware'),lambda:simulator_storage(21)]
 before=RUNS
 for call in calls:
  try:call()
  except ValueError:pass
  else:raise AssertionError('Malformed resource contract accepted')
 assert RUNS==before;return len(calls)

def main():
 cases=[()]+[angles for n in range(1,5)for angles in ((0.,)*n,(math.pi,)+(0.,)*(n-1),tuple(.17+.23*j for j in range(n)))]
 for angles in cases:
  for mode in ('statevector','density_matrix'):
   for full in (False,True):simulate(angles,23,mode,full)
 assert RUNS==52
 # Additive vectors form an associative monoid,with independent coordinate arithmetic.
 x,y,z=Work(2,1,3,1,4,1),Work(5,2,4,2,8,2),Work(0,0,1,1,0,1)
 assert (x+y)+z==x+(y+z)and x+Work()==x and (x+y).scale(3)==x.scale(3)+y.scale(3)
 for n in range(5):
  for r in (1,7,80):
   for p in (1,min(3,r)):
    t=repeat_plan(n,r,p);assert t['total'].gates==sum(2*n for _ in range(r))and t['peak_qubits']==p*(n+1)
    assert t['rounds']*p>=r and (t['rounds']-1)*p<r
 for ps in ((F(1,10),F(1),F(1,5)),(F(0),F(1),F(1,3)),(F(1),F(0),F(0))):adaptive_first_failure(ps)
 assert a.mean_budget(F(1,4),F(1,20))==80
 assert substitute(4,2,3,80,8)==dict(queries=160,logical_gates=800,setup_bits=8)
 assert simulator_storage(4)==dict(statevector_bytes=256,density_bytes=4096)
 print('52 native CPU complex128 circuits: 13 angle cases, two modes and selected/full terminal records passed.')
 print('Native IR gate counts/depth match independent support scheduling; full vectors/densities, scalar parity probabilities and raw-record relations checked.')
 print('At n=3 and 80 preparations: 480 logical gates, serial depth 320, peak 4 qubits, 80 selected record bits; four-way schedule depth 80 and peak 16.')
 print('Three adaptive error-tree cases and exact additive/query/repetition/host-payload ledgers passed; diagnostic tensors are separate from task output.')
 print(f'{invalid_checks()} malformed contracts rejected before execution; no hardware timing, calibrated errors or automatic end-to-end estimator claimed.')
if __name__=='__main__':main()
