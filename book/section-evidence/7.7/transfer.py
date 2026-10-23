"""Printed7.7C with fresh parameters,positive effects and fixed ensembles."""
import itertools,cmath,math
import torch
from examples.foundations import no_signalling as s
for alice,bob in itertools.product(('Z','X','Y'),repeat=2):
    r=s.query(1.03,-.52,alice,bob,n=4,pair=(2,0),seed=97)
    if bob=='Z':assert abs(float(r['marginal'][0])-math.cos(.515)**2)<s.ATOL
    else:assert abs(float(r['marginal'][0])-.5)<s.ATOL
    if alice in ('X','Y'):
        for a in (0,1):
            if alice=='X':x,y=(-1)**a*math.sin(1.03)*math.cos(-.52),(-1)**a*math.sin(1.03)*math.sin(-.52)
            else:x,y=(-1)**a*math.sin(1.03)*math.sin(-.52),-(-1)**a*math.sin(1.03)*math.cos(-.52)
            mean={'X':x,'Y':y,'Z':math.cos(1.03)}[bob]
            assert abs(float(r['conditional'][a][0])-(1+mean)/2)<s.ATOL
v=r['state'];es=[]
for j in range(3):
    w=torch.tensor([1,cmath.exp(2j*math.pi*j/3)],dtype=s.D)/math.sqrt(2)
    es.append((2/3)*torch.outer(w,w.conj()))
es=tuple(es);coin=((math.sqrt(.23)*s.I,),(math.sqrt(.77)*s.H,))
families=(s.groups_for('Z'),s.groups_for('Y'),s.weak(.27),s.reset_groups(),coin,(tuple(g[0] for g in coin),))
for gs in families:
    q=s.analyze(v,(2,),gs,(0,),es)
    assert torch.allclose(q['marginal'],torch.full((3,),1/3,dtype=torch.float64),atol=s.ATOL,rtol=0)
other=s.apply(v,s.X,(0,))
for gs in (s.groups_for('X'),s.weak(.27),s.reset_groups()):
    a=s.analyze(v,(2,),gs,(0,),es);b=s.analyze(other,(2,),gs,(0,),es)
    assert torch.allclose(.23*a['marginal']+.77*b['marginal'],.23*a['baseline']+.77*b['baseline'],atol=s.ATOL,rtol=0)
for kappa in (.21,.79):s.dilation(kappa,theta=.94,phase=.61)
s.dilation(theta=.94,phase=.61,kind='reset')
assert s.RUNS==12
print('Printed7.7C:nine native basis pairs and conditional Pauli formulas passed;three fresh coherent dilation fixtures passed.')
print('12native transfer circuits;12classical trine/instrument reports and3fixed-ensemble averages passed,no native trine endpoint claimed.')
