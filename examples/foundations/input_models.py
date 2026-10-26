"""14.1: encoded length,uniform parity family and explicit native resources."""
import itertools,math
from dataclasses import replace
import torch,flagquantum as fq
try:
 from examples.foundations import statistical_ensembles as e
except ModuleNotFoundError:
 import statistical_ensembles as e
D=e.D;RUNS=0

def binary(word):
 if type(word)is not str or not word or any(c not in '01'for c in word):raise ValueError('Nonempty binary numeral required')
 return int(word,2),len(word)

def word_bits(x):
 if type(x)is not str or any(c not in '01'for c in x):raise ValueError('Binary input string required;empty parity input allowed')
 return tuple(int(c)for c in x)

def family(n):
 if type(n)is not int or n<0 or n>10000:raise ValueError('Integer length0..10000required for bounded host generator')
 return tuple((i,n)for i in range(n))

def resources(x):
 bits=word_bits(x);n=len(bits)
 return {'input_bits':n,'data_qubits':n,'target_qubits':1,'CX_kernel':n,'X_loading':sum(bits),'gates_with_loading':n+sum(bits),'statevector_entries':2**(n+1),'density_entries':4**(n+1)}

def circuit(x,y=0):
 bits=word_bits(x);n=len(bits)
 if n>4:raise ValueError('Native enumeration teaching guard n<=4;not a FlagQuantum limit')
 if type(y)is not int or y not in (0,1):raise ValueError('Literal target bit required')
 c=fq.Circuit(n+1,dtype=D)
 for i,b in enumerate(bits):
  if b:c.X(i)
 if y:c.X(n)
 for control,target in family(n):c.CX(control,target)
 return c

def execute(x,y=0,mode='statevector'):
 global RUNS
 bits=word_bits(x);n=len(bits);c=circuit(x,y)
 if mode not in ('statevector','density_matrix'):raise ValueError('Tested mode required')
 r=fq.run(c,outputs=[fq.probabilities(qubits=(n,),name='answer'),fq.probabilities(name='full'),fq.samples(qubits=(n,),name='record')],shots=7,options=replace(e.OPTIONS,mode=mode,seed=31));RUNS+=1
 expected=y^(sum(bits)%2);p=r.measurement('answer').value[0];ref=torch.zeros(2,dtype=torch.float64);ref[expected]=1;e.close(p,ref)
 full=r.measurement('full').value[0];index=2*int(x or '0',2)+expected;fullref=torch.zeros(2**(n+1),dtype=torch.float64);fullref[index]=1;e.close(full,fullref)
 record=r.measurement('record').value;assert record.shape==(1,7,1)and bool((record==expected).all())
 return r,resources(x)

def invalid_checks():
 calls=[lambda:binary(''),lambda:binary('102'),lambda:binary(7),lambda:word_bits('01x'),lambda:word_bits(1),lambda:family(True),lambda:family(-1),lambda:circuit('00000'),lambda:circuit('01',True)]
 for call in calls:
  try:call()
  except ValueError:pass
  else:raise AssertionError('Malformed model contract accepted')
 return len(calls)

def main():
 for mode in ('statevector','density_matrix'):
  for n in range(5):
   for b in itertools.product('01',repeat=n):
    for y in (0,1):execute(''.join(b),y,mode)
 assert RUNS==124
 for k in range(1,65):
  a,n=binary('1'+'0'*k);assert a==2**k and n==k+1
  assert binary('0'*(k+2)+'1')==(1,k+3)
 for n in (0,1,17,1000):assert len(family(n))==n
 print('124 actual native circuits:all31binary inputs of lengths0..4,two target bits,two execution modes passed.')
 print('Exact integer bitlength/padding and bounded uniform gate-list construction passed;no large circuit executed.')
 print(f'{invalid_checks()} malformed input/model contracts rejected before native execution.')
 print('Parity kernel uses n CX gates and n+1qubits;input loading and simulator arrays are recorded separately.')
if __name__=='__main__':main()
