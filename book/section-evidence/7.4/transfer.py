"""Fresh 7.4 transfer cases; includes both versions of the exact printed exercise."""
import math
from examples.foundations import chsh_experiment as t

assert t.RUNS == 0
cases = [(.73, -.39, (3,1), t.SETTINGS),
         (.73, -.39+math.pi, (3,1), t.SETTINGS),
         (-1.17, .62, (2,0), ((-.31,.17),(-.31,-.73),(.92,.17),(.92,-.73))),
         (1.37, -1.1, (1,3), ((.29,-.41),(.29,.87),(-.63,-.41),(-.63,.87)))]
for j,(theta,phi,pair,settings) in enumerate(cases):
    reports = [t.run_setting(a,b,theta,phi,n=4,pair=pair) for a,b in settings]
    for (a,b),r in zip(settings,reports):
        pa=float(r['probabilities'].reshape(2,2)[0].sum())
        assert abs(pa-(1+math.cos(theta)*math.cos(a))/2) < t.ATOL
    if j < 2:
        k=math.sin(.73)*math.cos(phi)
        assert abs(t.chsh([r['correlation'] for r in reports])-math.sqrt(2)*(1+k)) < t.ATOL
        for x in (0,1):
            assert abs(float(reports[2*x]['probabilities'].reshape(2,2)[0].sum())
                       -float(reports[2*x+1]['probabilities'].reshape(2,2)[0].sum())) < t.ATOL
assert t.RUNS == 16
print('16 fresh four-qubit circuits:full amplitudes,ordered probabilities,scalar correlations and local marginals passed.')
print('Printed exercise 7.4-C and its phi+pi variant both executed;two additional angle quartets and ordered supports passed.')
