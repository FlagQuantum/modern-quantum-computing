import sys,inspect
sys.path.insert(0,'.')
import examples.foundations.product_entanglement as e
import flagquantum as fq
import math
for eps in (1e-10,1e-12,1e-13,1e-14):
 c=fq.Circuit(2,dtype=e.D).ry(0,2*math.asin(eps)).cx(0,1)
 v,_=e.query(c)
 print(eps,repr(v.tolist()),repr(e.minors(e.coefficients(v,(0,),(1,)))[0].item()))
print('native calls',e.RUNS)
print(inspect.getfile(fq.Circuit))
