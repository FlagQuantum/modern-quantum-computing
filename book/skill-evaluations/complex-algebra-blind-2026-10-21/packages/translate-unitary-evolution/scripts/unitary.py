#!/usr/bin/env python3
"""Bounded phase-tracked single-qubit evolution, contract 0.1.0."""
import cmath
from importlib.metadata import version,PackageNotFoundError
import json
import math
import sys

VERSION='0.1.0'
VALIDATION=1e-12
ENDPOINT=1e-12
I=[[1+0j,0j],[0j,1+0j]]
PAULI=[[[0j,1+0j],[1+0j,0j]],[[0j,-1j],[1j,0j]],[[1+0j,0j],[0j,-1+0j]]]

class Invalid(ValueError):pass
class Unsupported(ValueError):pass


def real(x,bound=1e100):
    if type(x) not in (int,float) or not -bound<=x<=bound:raise Invalid('Expected finite real number within declared bound')
    return float(x)
def scalar(x):
    if not isinstance(x,list) or len(x)!=2:raise Invalid('Complex entries must be [real,imaginary]')
    return complex(real(x[0]),real(x[1]))
def matrix(x):
    if not isinstance(x,list) or len(x)!=2 or any(not isinstance(r,list) or len(r)!=2 for r in x):raise Invalid('Only 2x2 matrices; no batch axis')
    return [[scalar(z) for z in row] for row in x]
def state(x):
    if not isinstance(x,list) or len(x)!=2:raise Invalid('Exactly two complex amplitudes required')
    v=[scalar(z) for z in x]
    if any(abs(z)>2 for z in v) or abs(sum(abs(z)**2 for z in v)-1)>VALIDATION:raise Invalid('State must already have unit squared norm within 1e-12')
    return v
def mm(a,b):return [[sum(a[j][k]*b[k][l] for k in range(len(b))) for l in range(len(b[0]))] for j in range(len(a))]
def mv(a,v):return [sum(x*y for x,y in zip(row,v)) for row in a]
def adj(a):return [[a[k][j].conjugate() for k in range(len(a))] for j in range(len(a))]
def scale(z,a):return [[z*x for x in row] for row in a]
def error(a,b):return max(abs(x-y) for ra,rb in zip(a,b) for x,y in zip(ra,rb))
def encode(x):
    if isinstance(x,list):return [encode(z) for z in x]
    z=complex(x);return [z.real,z.imag]
def rotation(axis,theta):
    c,s=math.cos(theta/2),math.sin(theta/2)
    if axis=='z':return [[cmath.exp(-.5j*theta),0j],[0j,cmath.exp(.5j*theta)]]
    if axis=='y':return [[c,-s],[s,c]]
    return [[c,-1j*s],[-1j*s,c]]
def unitary(u):
    if error(mm(adj(u),u),I)>VALIDATION:raise Invalid('Input must already be unitary; no projection or rescaling')
def factor(u):
    determinant=u[0][0]*u[1][1]-u[0][1]*u[1][0]
    alpha=.5*cmath.phase(determinant)
    v=scale(cmath.exp(-1j*alpha),u);a,c=v[0][0],v[1][0]
    if abs(c)<=ENDPOINT:beta,gamma,delta,branch=-2*cmath.phase(a),0.,0.,'north'
    elif abs(a)<=ENDPOINT:beta,gamma,delta,branch=2*cmath.phase(c),math.pi,0.,'south'
    else:beta,gamma,delta,branch=cmath.phase(c)-cmath.phase(a),2*math.atan2(abs(c),abs(a)),-cmath.phase(c)-cmath.phase(a),'generic'
    native=mm(mm(rotation('z',beta),rotation('y',gamma)),rotation('z',delta))
    rebuilt=scale(cmath.exp(1j*alpha),native)
    return dict(alpha=alpha,beta=beta,gamma=gamma,delta=delta,branch=branch),native,rebuilt

def validate(q):
    base={'task','basis','state','context'}
    if not isinstance(q,dict) or not base<=set(q):raise Invalid('Required base keys: task,basis,state,context; optional atol')
    if q['basis']!=['0','1']:raise Unsupported('Canonical computational basis 0,1 required')
    if q['context'] not in ('isolated','coherent-control'):raise Invalid('Explicit context isolated or coherent-control required')
    initial=state(q['state']);atol=q.get('atol',1e-10)
    if type(atol) not in (int,float) or not 5e-12<=atol<=1e-8:raise Invalid('Absolute verification atol must be in [5e-12,1e-8]')
    task=q['task'];info={}
    if task=='factor':
        if set(q)-base-{'atol','unitary'} or 'unitary' not in q:raise Invalid('factor requires exactly base fields plus unitary and optional atol')
        u=matrix(q['unitary']);unitary(u);info['source']='supplied full unitary, not a ray or probability table'
        E=None
    elif task=='rotation':
        if set(q)-base-{'atol','axis','angle'} or not {'axis','angle'}<=set(q):raise Invalid('rotation requires axis and angle')
        axis=q['axis'];angle=q['angle']
        if not isinstance(axis,list) or len(axis)!=3:raise Invalid('Axis requires three real components')
        axis=[real(x,2) for x in axis]
        if abs(sum(x*x for x in axis)-1)>VALIDATION:raise Invalid('Axis must already be unit length; no normalization')
        if not isinstance(angle,dict) or set(angle)!={'value','unit'}:raise Invalid('Angle requires value and explicit unit')
        if angle['unit']!='radian':raise Unsupported('Rotation angles require radians; clarify units before conversion')
        theta=real(angle['value'],64)
        E=[[theta/2*sum(axis[k]*PAULI[k][j][l] for k in range(3)) for l in range(2)] for j in range(2)]
        u=[[math.cos(theta/2)*I[j][l]-1j*math.sin(theta/2)*sum(axis[k]*PAULI[k][j][l] for k in range(3)) for l in range(2)] for j in range(2)]
        info={'axis':axis,'theta_radians':theta,'rotation_convention':'active exp(-i theta n.sigma/2)'}
    elif task=='evolve':
        if set(q)-base-{'atol','generator','time','hbar'} or not {'generator','time'}<=set(q):raise Invalid('evolve requires generator and time; hbar only for energy units')
        gen,time=q['generator'],q['time']
        if not isinstance(gen,dict) or set(gen)!={'matrix','unit'} or not isinstance(time,dict) or set(time)!={'value','unit'}:raise Invalid('Generator/time require their explicit matrix or value and unit')
        g=matrix(gen['matrix']);magnitude=max(abs(x) for row in g for x in row)
        if error(g,adj(g))>VALIDATION*magnitude:raise Invalid('Generator must be Hermitian with scale-relative entrywise tolerance 1e-12, even at t=0')
        t=real(time['value']);gu,tu=gen['unit'],time['unit']
        if gu=='1':
            if tu!='1' or 'hbar' in q:raise Invalid('Dimensionless K uses dimensionless time tau, with no hbar field')
            conversion=t
        elif gu in ('rad/s','J','eV'):
            if tu not in ('s','ns'):raise Unsupported('Physical time units supported: s, ns')
            seconds=t*(1e-9 if tu=='ns' else 1.)
            if gu=='rad/s':
                if 'hbar' in q:raise Invalid('Angular-frequency generator already equals H/hbar; no second hbar division')
                conversion=seconds
            else:
                h=q.get('hbar')
                if not isinstance(h,dict) or set(h)!={'value','unit'}:raise Invalid('Energy Hamiltonian requires explicit positive hbar and matching energy*time unit')
                if h['unit']!=gu+'*s':raise Invalid('hbar unit must match Hamiltonian energy unit times seconds')
                hv=real(h['value'])
                if not 1e-100<=hv<=1e100:raise Invalid('hbar must be positive in [1e-100,1e100]')
                conversion=seconds/hv
        else:raise Unsupported('Generator units: 1, rad/s, J or eV; cyclic Hz is not angular frequency')
        E=scale(conversion,g)
        if any(not math.isfinite(x.real) or not math.isfinite(x.imag) or abs(x)>32 for row in E for x in row):raise Invalid('Dimensionless exponent entries must be finite with magnitude at most 32')
        h0=(E[0][0].real+E[1][1].real)/2
        components=[(E[0][1].real+E[1][0].real)/2,(E[1][0].imag-E[0][1].imag)/2,(E[0][0].real-E[1][1].real)/2]
        radius=math.sqrt(sum(x*x for x in components));sinc=math.sin(radius)/radius if radius else 1.
        u=[[cmath.exp(-1j*h0)*(math.cos(radius)*I[j][l]-1j*sinc*sum(components[k]*PAULI[k][j][l] for k in range(3))) for l in range(2)] for j in range(2)]
        info={'generator_unit':gu,'time_unit':tu,'time_value':t,'exponent_multiplier':conversion,'effective_exponent':encode(E),
              'trace_shift_phase':encode(cmath.exp(-1j*h0)),'trace_shift_exponent':h0,'hbar':q.get('hbar'),
              'note':'Constant generator only; no inference of H or its scalar shift from a single endpoint'}
    else:raise Unsupported('Supported tasks: evolve, rotation, factor; no time-dependent solver or inverse-generator profile')
    return initial,atol,u,E,info


def controlled(u):return [[complex(j==k) if j<2 and k<2 else u[j-2][k-2] if j>=2 and k>=2 else 0j for k in range(4)] for j in range(4)]

def run(q):
    initial,atol,u,E,info=validate(q)
    try:fv,tv=version('flagquantum'),version('torch')
    except PackageNotFoundError as exc:raise Unsupported('Missing pinned runtime: '+str(exc)) from exc
    if fv!='0.3.1' or tv.split('+')[0]!='2.13.0':raise Unsupported('Requires FlagQuantum 0.3.1 and Torch 2.13.0')
    import flagquantum as fq
    import torch
    D=torch.complex128
    options=fq.ExecutionOptions(mode='statevector',backend='pytorch',device='cpu',precision='complex128',allow_backend_fallback=False,allow_approximate=False)
    errors={}
    if E is not None:
        scalar_reference=u
        u=torch.matrix_exp(-1j*torch.tensor(E,dtype=D)).tolist()
        errors['exponential_reference_max_absolute']=error(u,scalar_reference)
    params,native,rebuilt=factor(u);alpha=params['alpha']
    errors.update(unitarity_max_absolute=error(mm(adj(u),u),I),reconstruction_max_absolute=error(u,rebuilt))
    axis_native=None
    if q['task']=='rotation':
        axis=info['axis']
        for j,name in enumerate('xyz'):
            if abs(axis[j])==1 and all(axis[k]==0 for k in range(3) if k!=j):axis_native=(name,axis[j]*info['theta_radians'])
    records=[]
    def execute(v,label,path,full=None,repair=False):
        n=2 if full is not None else 1
        c=fq.Circuit(n,dtype=D);a,b=v
        prep=torch.tensor([[a,-b.conjugate()],[b,a.conjugate()]],dtype=D)
        c.unitary(1 if n==2 else 0,unitary=prep)
        if n==2:
            c.h(0);c.unitary(0,1,unitary=torch.tensor(full,dtype=D))
            if repair:c.phase(0,theta=alpha)
        elif path=='native-axis':getattr(c,'r'+axis_native[0])(0,theta=axis_native[1])
        elif path=='native-zyz':
            c.rz(0,theta=params['delta']);c.ry(0,theta=params['gamma']);c.rz(0,theta=params['beta'])
        else:c.unitary(0,unitary=torch.tensor(u,dtype=D))
        r=fq.run(c,outputs=[fq.probabilities()],options=options);sv,p=r.statevector(),r.probabilities
        dimension=4 if n==2 else 2
        if sv.shape!=(1,dimension) or p.shape!=(1,dimension) or sv.dtype!=D or p.dtype!=torch.float64 or sv.device.type!='cpu' or p.device.type!='cpu':raise RuntimeError('Output shape/dtype/device outside profile')
        if not torch.isfinite(sv).all() or not torch.isfinite(p).all():raise RuntimeError('Nonfinite simulator output')
        statevector=sv[0].tolist();probabilities=p[0].tolist()
        input_full=[x/math.sqrt(2) for x in v+v] if n==2 else v
        expected=mv(controlled(u) if n==2 and path!='controlled-unrepaired' else full if n==2 else native if path=='native-zyz' else u,input_full)
        diagnostic=[cmath.exp(1j*alpha)*x for x in statevector] if path=='native-zyz' else statevector
        target=mv(u,v) if n==1 else expected
        err={'submitted_state_max_absolute':max(abs(x-y) for x,y in zip(statevector,expected)),
             'born_max_absolute':max(abs(x-abs(y)**2) for x,y in zip(probabilities,statevector)),
             'normalization_absolute':abs(sum(probabilities)-1)}
        if path=='native-zyz':err['phase_corrected_diagnostic_max_absolute']=max(abs(x-y) for x,y in zip(diagnostic,target))
        return {'input_label':label,'path':path,'statevector':encode(statevector),'probabilities':probabilities,'expected_submitted_state':encode(expected),
                'diagnostic_phase_corrected_state':encode(diagnostic) if path=='native-zyz' else None,
                'diagnostic_is_submitted_gate':False,'errors':err,'passed':max(err.values())<=atol,'shape':[1,dimension],'state_dtype':str(sv.dtype),'probability_dtype':str(p.dtype),'device':'cpu'}
    for label,v in [('supplied',initial),('zero',[1+0j,0j]),('one',[0j,1+0j])]:
        records.append(execute(v,label,'direct'));records.append(execute(v,label,'native-zyz'))
        if axis_native is not None:records.append(execute(v,label,'native-axis'))
    context=None
    if q['context']=='coherent-control':
        cu,cv=controlled(u),controlled(native)
        repair=[[complex(j==k)*(1 if j<2 else cmath.exp(1j*alpha)) for k in range(4)] for j in range(4)]
        context={'basis':['00','01','10','11'],'control_qubit':0,'target_qubit':1,'alpha_radians':alpha,
                 'repair':'actual phase(0,theta=alpha) on control after controlled(native)',
                 'matrix_repair_max_absolute':error(mm(repair,cv),cu),'omitted_phase_operator_raw_frobenius':math.sqrt(sum(abs(x-y)**2 for ra,rb in zip(cu,cv) for x,y in zip(ra,rb))),
                 'whole_output_global_multiplier_is_not_branch_repair':True}
        errors['controlled_matrix_repair_max_absolute']=context['matrix_repair_max_absolute']
        records += [execute(initial,'coherent-control','controlled-direct',cu),execute(initial,'coherent-control','controlled-repaired',cv,True),execute(initial,'coherent-control','controlled-unrepaired',cv)]
    verified=max(errors.values())<=atol and all(r['passed'] for r in records)
    return {'contract_version':VERSION,'status':'verified' if verified else 'verification_failed','task':q['task'],'context':q['context'],'basis':['0','1'],
            'versions':{'flagquantum':fv,'torch':tv},'absolute_tolerance':atol,'unitarity_validation_atol':VALIDATION,'endpoint_threshold':ENDPOINT,
            'units_and_generator':info,'unitary':encode(u),'native_zyz_matrix':encode(native),'reconstructed_full_matrix':encode(rebuilt),'zyz':params,
            'phase_convention':'U=exp(i alpha) Rz(beta) Ry(gamma) Rz(delta); alpha=half principal arg(det U)',
            'native_chronological_gates':[['rz',params['delta']],['ry',params['gamma']],['rz',params['beta']]],
            'native_circuit_implements':'V only; exp(i alpha) on isolated output is diagnostic arithmetic, not a submitted global-phase gate',
            'controlled_context':context,'matrix_errors':errors,'records':records,'actual_flagquantum_circuits':len(records),
            'execution':{'mode':'statevector','backend':'pytorch','device':'cpu','precision':'complex128','allow_backend_fallback':False,'allow_approximate':False},
            'limitations':['No unique Euler angles or continuous branch claim','No unique generator inferred from endpoint U','Ideal deterministic matrices/states, not shots, noise or hardware','Constant generator and one target qubit only; optional control is a declared two-qubit preview']}


def reject_constant(x):raise Invalid('Nonstandard JSON constant '+x)
def unique_object(pairs):
    q={}
    for k,v in pairs:
        if k in q:raise Invalid('Duplicate key '+k)
        q[k]=v
    return q

def main():
    runtime={'implementation':sys.implementation.name,'python':'.'.join(map(str,sys.version_info[:3]))}
    if sys.implementation.name!='cpython' or sys.version_info[:2]!=(3,12):
        print(json.dumps({'contract_version':VERSION,'status':'unsupported','reason':'unsupported_runtime: CPython 3.12 required','runtime':runtime}));return 3
    try:q=json.load(sys.stdin,parse_constant=reject_constant,object_pairs_hook=unique_object)
    except (ValueError,OverflowError,RecursionError) as exc:
        print(json.dumps({'contract_version':VERSION,'status':'invalid_input','reason':str(exc),'runtime':runtime}));return 2
    try:output=run(q)
    except Unsupported as exc:output={'contract_version':VERSION,'status':'unsupported','reason':str(exc)}
    except Invalid as exc:output={'contract_version':VERSION,'status':'invalid_input','reason':str(exc)}
    except Exception as exc:output={'contract_version':VERSION,'status':'execution_failed','reason':type(exc).__name__+': '+str(exc)}
    output['runtime']=runtime;print(json.dumps(output,allow_nan=False,sort_keys=True))
    return {'verified':0,'verification_failed':1,'invalid_input':2,'unsupported':3,'execution_failed':4}[output['status']]

if __name__=='__main__':sys.exit(main())
