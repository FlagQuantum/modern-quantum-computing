"""Archive actual seeded readout dictionaries; replay is not an independent trial."""
import json
from pathlib import Path
import torch
from examples.foundations.convention_translation import q_circuit,factors_complex,complex_gate,sample,sample_partial,marginal,DTYPE
from examples.foundations.ordered_supports import input_product,scalar_scatter
initial=input_product(factors_complex());U=complex_gate();S=(2,0)
f=torch.tensor(scalar_scatter(U,initial.tolist(),3,S),dtype=DTYPE)
qc=q_circuit(factors_complex(),U,S)
raw,canonical=sample(qc,(2,0,1),1024)
raw_partial,canonical_partial=sample_partial(qc,S,1024)
empirical=torch.tensor([canonical.get(format(j,'03b'),0)/1024 for j in range(8)],dtype=torch.float64)
partial=torch.tensor([canonical_partial.get(format(j,'02b'),0)/1024 for j in range(4)],dtype=torch.float64)
err=float((empirical-f.abs().square()).abs().max());err_partial=float((partial-marginal(f.abs().square(),3,S)).abs().max())
assert err<.1 and err_partial<.1
result={'seed':20261021,'shots_each':1024,'full_mapping':[2,0,1],'full_canonical_labels':['q0','q1','q2'],'full_raw':raw,'full_canonical':canonical,'partial_measured_labels':['q2','q0'],'partial_slots':[0,1],'partial_raw':raw_partial,'partial_canonical':canonical_partial,'full_max_frequency_error':err,'partial_max_frequency_error':err_partial,'note':'Actual local sampler replay of existing seeded fixtures, not fresh independent scientific evidence.'}
Path(__file__).with_name('readout-counts.json').write_text(json.dumps(result,indent=2)+'\n')
print(f'Archived full/partial counts,2048shots; frequency errors {err:.9f},{err_partial:.9f}.')
