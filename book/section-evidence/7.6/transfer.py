"""Fresh7.6C/D and relocation cases,not additional proof of the theorem."""
import itertools,math
import torch
from examples.foundations import superdense_coding as s
for bits in itertools.product((0,1),repeat=2):
    out=s.query(bits,n=4,pair=(2,0),columns=(0,2),seed=57)
    assert all(x==bits for x in out['messages'])
print('Exact printed7.6C:all four messages,(A,B)=(q2,q0),reversed native columns and complex spectators passed.')
for bits in itertools.product((0,1),repeat=2):
    for stage in ('encoded','decoded'):
        out=s.query(bits,stage,n=3,pair=(2,0),theta=1.17,phase=-.31,seed=61)
        if stage=='decoded':
            probability=float(out['probabilities'][2*bits[0]+bits[1]])
            assert abs(probability-(1+math.sin(1.17)*math.cos(.31))/2)<s.ATOL
for bits in itertools.product((0,1),repeat=2):s.carrier(bits)
assert s.RUNS==16
print('Printed7.6D resource on a fresh ordered pair plus four relocation fixtures passed;16 total native transfer circuits.')
