#!/usr/bin/env python3
"""Ideal one-qubit interference, bounded contract 0.1.0."""
import cmath
from importlib.metadata import version, PackageNotFoundError
import json
import math
import sys

VERSION='0.1.0'
VALIDATION_ATOL=1e-12


class Invalid(ValueError):pass
class Unsupported(ValueError):pass


def real(x, bound):
    if type(x) not in (float,int):raise Invalid('Expected real JSON number, not bool/string')
    if not -bound<=x<=bound:raise Invalid('Nonfinite or out-of-profile number')
    return float(x)


def scalar(x):
    if not isinstance(x,list) or len(x)!=2:raise Invalid('Use [real,imaginary] complex entries')
    return complex(real(x[0],2),real(x[1],2))


def validate(q):
    required={'profile','state','basis','angle_unit','phase_radians','readout'}
    if not isinstance(q,dict) or not required<=set(q) or set(q)-required-{'atol'}:
        raise Invalid('Required keys: profile,state,basis,angle_unit,phase_radians,readout; optional atol')
    if q['profile']!='ideal-pure-single-qubit':raise Unsupported('Only ideal pure single-qubit experiments; no noise, density, shots or hardware profile')
    if q['basis']!=['0','1']:raise Unsupported('Canonical computational basis 0,1 required; no inferred reordering')
    if q['angle_unit']!='radian':raise Unsupported('This profile takes radians; clarify/convert explicit units before execution')
    if not isinstance(q['state'],list) or len(q['state'])!=2:raise Invalid('Exactly two amplitudes required; no batch axis')
    a,b=map(scalar,q['state']); n=abs(a)**2+abs(b)**2
    if abs(n-1)>VALIDATION_ATOL:raise Invalid('Input must already have unit squared norm within 1e-12; no normalization repair')
    phases=q['phase_radians']
    if not isinstance(phases,list) or not 1<=len(phases)<=129:raise Invalid('Supply 1..129 explicit phase values')
    phases=[real(x,1024) for x in phases]
    readout=q['readout']
    if not isinstance(readout,dict):raise Invalid('Readout must be an explicit object')
    if readout.get('type')=='computational':
        if set(readout)!={'type'}:raise Invalid('Computational readout takes no analyzer delta')
        delta=None
    elif readout.get('type')=='phase-h':
        if set(readout)!={'type','delta_radians'}:raise Invalid('phase-h requires exactly type and delta_radians')
        delta=real(readout['delta_radians'],1024)
    else:raise Unsupported('Supported readouts: computational or phase-h = H D(-delta)')
    atol=q.get('atol',1e-10)
    if type(atol) not in (int,float) or not 1e-12<=atol<=1e-8:raise Invalid('Absolute atol must lie in [1e-12,1e-8]')
    return a,b,n,phases,delta,atol


def encode(xs):return [[z.real,z.imag] for z in xs]


def run(q):
    a,b,n,phases,delta,atol=validate(q)
    try:
        fq_version=version('flagquantum');torch_version=version('torch')
    except PackageNotFoundError as exc:raise Unsupported('Missing pinned example environment: '+str(exc)) from exc
    if fq_version!='0.3.1' or torch_version.split('+')[0]!='2.13.0':
        raise Unsupported('Validated runtime requires FlagQuantum 0.3.1 and Torch 2.13.0; actual '+fq_version+', '+torch_version)
    import flagquantum as fq
    import torch
    options=fq.ExecutionOptions(mode='statevector',backend='pytorch',device='cpu',precision='complex128',allow_backend_fallback=False,allow_approximate=False)
    # Columns (a,b) and (-b*,a*) prepare the supplied complex state from |0>.
    preparation=torch.tensor([[a,-b.conjugate()],[b,a.conjugate()]],dtype=torch.complex128)
    records=[]
    for phi in phases:
        circuit=fq.Circuit(1,dtype=torch.complex128)
        circuit.unitary(0,unitary=preparation)
        circuit.phase(0,theta=phi)
        if delta is not None:
            circuit.phase(0,theta=-delta)
            circuit.h(0)
        result=fq.run(circuit,outputs=[fq.probabilities()],options=options)
        state,p=result.statevector(),result.probabilities
        if state.shape!=(1,2) or p.shape!=(1,2):raise RuntimeError('Unexpected state/probability shape')
        if state.dtype!=torch.complex128 or p.dtype!=torch.float64 or state.device.type!='cpu' or p.device.type!='cpu':raise RuntimeError('Unexpected dtype/device')
        if not torch.isfinite(state).all() or not torch.isfinite(p).all():raise RuntimeError('Nonfinite simulator output')
        post=(a,cmath.exp(1j*phi)*b)
        if delta is None:
            reference=post;analytic=[abs(a)**2,abs(b)**2];cross=None
        else:
            shifted=cmath.exp(-1j*delta)*post[1]
            reference=((a+shifted)/math.sqrt(2),(a-shifted)/math.sqrt(2))
            cross=(a.conjugate()*cmath.exp(1j*(phi-delta))*b).real
            analytic=[n/2+cross,n/2-cross]
        actual=state[0].tolist(); probs=p[0].tolist()
        errors={
            'state_max_absolute':max(abs(x-y) for x,y in zip(actual,reference)),
            'probability_formula_max_absolute':max(abs(x-y) for x,y in zip(probs,analytic)),
            'probability_born_max_absolute':max(abs(x-abs(y)**2) for x,y in zip(probs,actual)),
            'normalization_absolute':abs(sum(probs)-1),
        }
        records.append({'phase_radians':phi,'post_phase_reference':encode(post),'reference_state':encode(reference),
                        'statevector':encode(actual),'probabilities':probs,'analytic_probabilities':analytic,
                        'interference_contribution':cross,'errors':errors,'passed':max(errors.values())<=atol,
                        'shape':[1,2],'state_dtype':str(state.dtype),'probability_dtype':str(p.dtype),'device':'cpu'})
    if delta is None:
        fringe={'applicable':False,'reason':'No recombining analyzer; probabilities do not scan the relative phase'}
    else:
        # Analytic full continuous-scan extrema; not min/max of a sparse sampled grid.
        contrast=abs(a)*abs(b)
        fringe={'applicable':True,'continuous_p0_min':n/2-contrast,'continuous_p0_max':n/2+contrast,
                'continuous_visibility':2*contrast/n,'sampled_p0_min':min(r['probabilities'][0] for r in records),
                'sampled_p0_max':max(r['probabilities'][0] for r in records),
                'relative_phase_identifiable':abs(a)>0 and abs(b)>0}
    return {'contract_version':VERSION,'status':'verified' if all(r['passed'] for r in records) else 'verification_failed',
            'profile':q['profile'],'basis':['0','1'],'angle_unit':'radian','input_state':q['state'],
            'readout':q['readout'],'operation_order':['prepare supplied state','D(phi)']+([] if delta is None else ['D(-delta)','H'])+['computational readout'],
            'absolute_tolerance':atol,'validation_atol':VALIDATION_ATOL,'execution':{'mode':'statevector','backend':'pytorch','device':'cpu','precision':'complex128','allow_backend_fallback':False,'allow_approximate':False},
            'versions':{'flagquantum':fq_version,'torch':torch_version},'records':records,'fringe':fringe,
            'limitations':['Ideal deterministic probabilities, not sampled counts or hardware data','A fixed readout can miss a relative-phase difference','Reduced visibility alone does not diagnose decoherence','Numerical verification is not a proof or whole-paper reproduction']}


def reject_constant(x):raise Invalid('Nonstandard JSON constant '+x)
def unique_object(pairs):
    q={}
    for k,v in pairs:
        if k in q:raise Invalid('Duplicate JSON key '+k)
        q[k]=v
    return q


def main():
    runtime={'implementation':sys.implementation.name,'python':'.'.join(map(str,sys.version_info[:3]))}
    if sys.implementation.name!='cpython' or sys.version_info[:2]!=(3,12):
        print(json.dumps({'contract_version':VERSION,'status':'unsupported','reason':'unsupported_runtime: requires CPython 3.12','runtime':runtime},sort_keys=True));return 3
    try:
        q=json.load(sys.stdin,parse_constant=reject_constant,object_pairs_hook=unique_object)
        output=run(q)
    except Unsupported as exc:output={'contract_version':VERSION,'status':'unsupported','reason':str(exc)}
    except (Invalid,json.JSONDecodeError,OverflowError,RecursionError) as exc:output={'contract_version':VERSION,'status':'invalid_input','reason':str(exc)}
    except Exception as exc:output={'contract_version':VERSION,'status':'execution_failed','reason':type(exc).__name__+': '+str(exc)}
    output['runtime']=runtime
    print(json.dumps(output,allow_nan=False,sort_keys=True))
    return {'verified':0,'verification_failed':1,'invalid_input':2,'unsupported':3,'execution_failed':4}[output['status']]


if __name__=='__main__':sys.exit(main())
