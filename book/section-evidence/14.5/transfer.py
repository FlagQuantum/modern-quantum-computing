"""Fresh14.5 parameters and exact finite reference checks."""
import json,itertools,math
from fractions import Fraction as F
from examples.foundations import accuracy_repetition as a
rows=[]
for mode in ('statevector','density_matrix'):
 for p in (F(7,10),F(9,10)):
  for n in (41,127):
   a.native_mean(p,n,mode);rows.append(dict(kind='mean',p=str(p),n=n,mode=mode))
 for independent in (False,True):
  _,error=a.native_vote(F(7,10),independent,mode);rows.append(dict(kind='vote',independent=independent,error=str(error),mode=mode))
 a.phase_chain((-.2,.3,.7,-.4),(.01,-.02,.005,.004),mode)
 m=a.moment_budget(F(1,4),F(1,50));assert m==29
 a.median_blocks(F(9,10),25,m,mode);rows.append(dict(kind='median',block_size=25,blocks=m,total=25*m,mode=mode))
assert a.RUNS==16
p=F(7,10)
failure=sum((math.prod(p if bit else 1-p for bit in bits)for bits in itertools.product((0,1),repeat=7)if sum(bits)<=3),F(0))
assert failure==a.majority_error(p,7)
block=[(F(j,4),F(math.comb(4,j))*p**j*(1-p)**(4-j))for j in range(5)]
coverage=sum((w0*w1*w2 for (x0,w0),(x1,w1),(x2,w2)in itertools.product(block,repeat=3)if abs(sorted((x0,x1,x2))[1]-p)<=F(1,4)),F(0))
bad=sum((w for x,w in block if abs(x-p)>F(1,4)),F(0));assert 1-coverage<=a.majority_error(1-bad,3)
h=F(1,5);m=a.moment_budget(h,F(1,50));assert (1-4*h*h)**m<=F(1,50)**2 and a.majority_error(F(7,10),m)<=F(1,50)
print(json.dumps(dict(native_runs=16,cases=rows,exact_seven_vote_failure=str(failure),exact_median_coverage=str(coverage),fresh_moment_budget=m),indent=2))
