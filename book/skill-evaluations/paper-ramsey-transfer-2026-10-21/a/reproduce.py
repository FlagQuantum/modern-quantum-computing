#!/usr/bin/env python3
"""Blind source-transfer experiment. Run with the explicitly pinned interpreter."""
import cmath, hashlib, json, math, platform, subprocess, sys, time
from pathlib import Path
from importlib.metadata import version

ROOT=Path(__file__).resolve().parent
PACKET=ROOT.parent/'packet'
EPS=1e-10
X=[0,0.23,0.5,1,1.37,2]
PHI=[math.pi*x for x in X]
def enc(z):
    if isinstance(z,(list,tuple)):return [enc(x) for x in z]
    z=complex(z);return [z.real,z.imag]
def dec(z):
    if len(z)==2 and all(type(v) in (int,float) for v in z):return complex(*z)
    return [dec(v) for v in z]
def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    started=time.time()
    evidence=ROOT/'raw'
    evidence.mkdir(exist_ok=False)
    calls=[]
    def call(label,skill,script,request):
        folder=evidence/label;folder.mkdir()
        save(folder/'request.json',request)
        source=PACKET/'skills'/skill/'scripts'/script
        cmd=[sys.executable,str(source)]
        tic=time.perf_counter()
        p=subprocess.run(cmd,input=json.dumps(request),text=True,capture_output=True,timeout=90)
        elapsed=time.perf_counter()-tic
        (folder/'stdout.json').write_text(p.stdout)
        (folder/'stderr.txt').write_text(p.stderr)
        meta={'command':cmd,'exit_code':p.returncode,'elapsed_seconds':elapsed,'script_sha256':sha(source),
              'request_sha256':sha(folder/'request.json'),'stdout_sha256':sha(folder/'stdout.json'),
              'stderr_sha256':sha(folder/'stderr.txt')}
        save(folder/'execution.json',meta)
        r=json.loads(p.stdout)
        calls.append(dict(label=label,skill=skill,status=r.get('status'),**meta))
        assert p.returncode==0 and r['status'] in ('verified','within_tolerance'),(label,r)
        assert r['runtime']['python']=='3.12.14',r['runtime']
        return r
    alg='translate-complex-linear-algebra';ev='translate-unitary-evolution'
    inter='reproduce-qubit-interference';comp='compare-quantum-states-and-operators'
    def algebra(label,**fields):
        return call(label,alg,'algebra.py',dict(coordinates='literal-complex',tolerance={'atol':EPS,'rtol':0},**fields))
    def compare(label,a,b,kind='state'):
        # Deliberately stricter norm budget EPS implies each coordinate <= EPS.
        return call(label,comp,'compare.py',dict(kind=kind,mode='coordinates',basis_a=['0','1'],basis_b=['0','1'],a=enc(a),b=enc(b),atol=EPS))
    s=1/math.sqrt(2)
    A=[[s,-s],[s,s]]
    # E=(pi/4)sigma_y, so -iE=[[0,-pi/4],[pi/4,0]]. Dimensionless ideal rotation.
    exp=algebra('01-classical-pulse-exponential',task='function',kind='exp',units='dimensionless',matrix=enc([[0,-math.pi/4],[math.pi/4,0]]))
    pulse=call('02-ideal-pulse-rotation',ev,'unitary.py',dict(task='rotation',basis=['0','1'],state=enc([1,0]),context='isolated',axis=[0,1,0],angle={'value':math.pi/2,'unit':'radian'},atol=EPS))
    compare('03-pulse-full-matrix',dec(exp['result']['value']),dec(pulse['unitary']),kind='unitary')
    preparation=algebra('04-preparation',task='algebra',operation='matvec',matrix=enc(A),v=enc([1,0]))
    # Validate actual producer singleton metadata before extracting its only sample.
    handoff=next(r for r in pulse['records'] if r['input_label']=='supplied' and r['path']=='direct')
    assert handoff['shape']==[1,2] and handoff['state_dtype']=='torch.complex128' and handoff['device']=='cpu'
    compare('05-prepared-state',dec(preparation['result']['value']),dec(handoff['statevector']))
    iq=dict(profile='ideal-pure-single-qubit',basis=['0','1'],state=handoff['statevector'],angle_unit='radian',phase_radians=PHI,readout={'type':'phase-h','delta_radians':math.pi},atol=EPS)
    fringe=call('06-interference',inter,'interference.py',iq)

    # A separate continuous circuit uses the declared ideal pulse matrices directly.
    import flagquantum as fq
    import torch
    assert version('flagquantum')=='0.3.1' and version('torch').split('+')[0]=='2.13.0'
    options=fq.ExecutionOptions(mode='statevector',backend='pytorch',device='cpu',precision='complex128',allow_backend_fallback=False,allow_approximate=False)
    rows=[]
    for j,(x,phi,r) in enumerate(zip(X,PHI,fringe['records'])):
        c=fq.Circuit(1,dtype=torch.complex128)
        c.unitary(0,unitary=torch.tensor(A,dtype=torch.complex128));c.phase(0,theta=phi);c.unitary(0,unitary=torch.tensor(A,dtype=torch.complex128))
        actual=fq.run(c,outputs=[fq.probabilities()],options=options)
        sv,p=actual.statevector(),actual.probabilities
        assert list(sv.shape)==list(p.shape)==[1,2]
        assert sv.dtype==torch.complex128 and p.dtype==torch.float64
        assert sv.device.type==p.device.type=='cpu' and torch.isfinite(sv).all() and torch.isfinite(p).all()
        v=sv[0].tolist();prob=p[0].tolist()
        # Independent scalar reference is derived from the source-compatible matrices;
        # it neither imports helper code nor obtains predictions from their outputs.
        q=cmath.exp(1j*phi)
        ref=[(1-q)/2,(1+q)/2]
        pref=[(1-math.cos(phi))/2,(1+math.cos(phi))/2]
        helper_v=dec(r['statevector'])
        compare(f'07-{j}-independent-reference',helper_v,ref)
        errs={'continuous_coordinate_vs_analytic':max(abs(a-b) for a,b in zip(v,ref)),
              'helper_coordinate_vs_analytic':max(abs(a-b) for a,b in zip(helper_v,ref)),
              'continuous_probability_vs_analytic':max(abs(a-b) for a,b in zip(prob,pref)),
              'helper_probability_vs_analytic':max(abs(a-b) for a,b in zip(r['probabilities'],pref)),
              'continuous_born':max(abs(a-abs(b)**2) for a,b in zip(prob,v)),
              'continuous_normalization':abs(sum(prob)-1)}
        assert max(errs.values())<=EPS
        rows.append({'source_x_in_pi_units':x,'phase_radians':phi,'analytic_statevector':enc(ref),'analytic_probabilities':pref,
                     'helper_statevector':r['statevector'],'helper_probabilities':r['probabilities'],
                     'continuous_statevector':enc(v),'continuous_probabilities':prob,'errors':errs,
                     'shape':[1,2],'state_dtype':str(sv.dtype),'probability_dtype':str(p.dtype),'device':str(sv.device)})
    save(evidence/'continuous-circuit-request.json',{'basis':['0=g','1=e'],'initial_state':enc([1,0]),'chronology':['A','D(phi)','A'],'pulse_matrix':enc(A),'phase_radians':PHI,'execution':fringe['execution']})
    save(evidence/'continuous-circuit-output.json',{'actual_flagquantum_circuits':len(rows),'records':rows,'runtime':{'python':platform.python_version(),'flagquantum':version('flagquantum'),'torch':version('torch')}})
    source={'url':'https://arxiv.org/pdf/1608.04908v1','supplied_file':'../packet/paper.pdf','sha256':sha(PACKET/'paper.pdf'),
            'locators':[{'page':2,'location':'Figure 1d and caption: Ramsey qubit wire, vacuum WPD off; two pulses with intervening phase/cavity interaction'},
                        {'page':2,'location':'left column below Figure 1, discussion surrounding Eq. (2): preparation, phase, vacuum coupling invariance and stated ground probability'},
                        {'page':3,'location':'top left paragraph: phase is incorporated by adjusting the first microwave pulse phase'},
                        {'page':3,'location':'Figure 2b horizontal axis labeled phi (pi), spanning 0 to 2'}]}
    runtime={'executable':sys.executable,'implementation':sys.implementation.name,'python':platform.python_version(),'full_version':sys.version,
             'torch':version('torch'),'flagquantum':version('flagquantum'),'numpy':version('numpy'),'scipy':version('scipy'),
             'execution':fringe['execution']}
    save(ROOT/'runtime.json',runtime)
    counters={'helper_calls':len(calls),'classical_algebra_calls':2,'comparison_calls':8,
              'evolution_calls':1,'interference_calls':1,'evolution_flagquantum_circuits':pulse['actual_flagquantum_circuits'],
              'interference_flagquantum_circuits':len(fringe['records']),'continuous_flagquantum_circuits':len(rows),
              'actual_flagquantum_circuits':pulse['actual_flagquantum_circuits']+len(fringe['records'])+len(rows),
              'quantum_hardware_calls':0,'shots':0}
    result={'status':'verified','scope':'ONLY ideal vacuum-WPD ground-state Ramsey fringe under a labeled compatible ideal pulse convention',
       'source':source,'basis':{'ordered':['0','1'],'mapping':{'0':'g','1':'e'},'cavity':'fixed vacuum; U acts as identity in this sector'},
       'target':{'ground_probability':'(1-cos(phi))/2 = sin(phi/2)^2','ground_probability_in_source_axis':'sin(pi*x/2)^2'},
       'convention':{'status':'chosen compatible ideal convention; not uniquely extracted calibrated pulses','H1':enc(A),'H2':enc(A),
          'D(phi)':'diag(1,exp(i phi))','vacuum_U':enc([[1,0],[0,1]]),'measurement_g_projector':enc([[1,0],[0,0]]),
          'rotation':'A=Ry(pi/2)=exp(-i*pi*sigma_y/4)','helper_analyzer':'H D(-pi)=A; chronological D(-pi), canonical H',
          'physical_phase_implementation':'Paper incorporates phi into first pulse phase; separate D(phi) is the equivalent ideal state-preparation representation used here.'},
       'derivation':['A|g>=(|g>+|e>)/sqrt(2).','D(phi) gives (|g>+exp(i phi)|e>)/sqrt(2).',
          'The cavity vacuum has photon number zero, hence the conditional cavity phase does not label either qubit path.',
          'A D(phi) A |g>=[(1-exp(i phi))/2,(1+exp(i phi))/2]^T.',
          'Born probability of g is |1-exp(i phi)|^2/4=(1-cos(phi))/2.',
          'Choosing canonical H on both ends instead yields (1+cos(phi))/2: literal named-gate interpretation contradicts the stated target. Preparation alone fixes one column, not the entire physical pulse. The selected Ry convention fixes both columns explicitly.'],
       'conversions':{'source_x':X,'source_axis_unit':'pi radians','radians':PHI,'rule':'phi=pi*x','analyzer_delta_radians':math.pi,
                      'rotation_angle_radians':math.pi/2,'dimensionless_exponent':'E=(pi/4)*sigma_y','energy_time_hbar_conversion':'none; ideal rotation, no inferred duration or Hamiltonian'},
       'tolerance':{'maximum_complex_coordinate_absolute':EPS,'maximum_probability_absolute':EPS,'rtol':0,
                    'comparison_helper_norm_atol':EPS,'note':'Norm <= EPS is a stricter sufficient test for max coordinate <= EPS; final max coordinate and probability errors separately checked.'},
       'records':rows,'maximum_errors':{k:max(r['errors'][k] for r in rows) for k in rows[0]['errors']},
       'continuous_fringe':{'minimum':0,'maximum':1,'visibility':1,'minimum_phi':'0 mod 2pi','maximum_phi':'pi mod 2pi','basis':'analytic full scan; source-axis samples are separately listed'},
       'claim_ledger':[{'claim':'Paper-stated ideal vacuum ground-state fringe','disposition':'reproduced at the six requested source-axis coordinates using the explicit compatible convention','evidence':'records and independent scalar derivation'},
           {'claim':'Both named Hadamards can be taken literally as canonical H with the stated intervening phase and ground measurement','disposition':'incompatible: predicts plus cosine; no silent phase-origin shift or ground/excited relabeling'},
           {'claim':'Paper uniquely specifies the full calibrated microwave pulse matrices','disposition':'not established; this result uses a labeled ideal convention'},
           {'claim':'Full complex coordinate agreement under that convention','disposition':'verified against independent analytic amplitudes and separately composed continuous circuits'},
           {'claim':'Hardware agreement, noisy fringe, coherent-cavity/cat-state reproduction, or whole-paper reproduction','disposition':'not claimed and not tested'}],
       'runtime':runtime,'actual_counters':counters,'calls':calls,
       'handoff':{'source':'02-ideal-pulse-rotation supplied/direct','checked_metadata':{'shape':[1,2],'dtype':'torch.complex128','device':'cpu'},'action':'extract sole sample after validation; retain full complex phase','repair_or_normalization':False},
       'limits':['Deterministic floating-point statevector evidence, not an exact proof or interval bound.','No photon-number truncation is needed in the fixed vacuum sector.','No cavity dynamics outside vacuum, decoherence, calibration, shot statistics, or physical pulse duration is modeled.','Unitary phase was preserved; no ray alignment used.'],
       'provenance':{'workflow_sha256':sha(Path(__file__)),'source_skills_unchanged':True,'source_skill_script_hashes':{c['skill']:c['script_sha256'] for c in calls},'runner_used':False},
       'elapsed_seconds':time.time()-started}
    save(ROOT/'result.json',result)
    print(json.dumps({'status':result['status'],'actual_counters':counters,'maximum_errors':result['maximum_errors']}))
if __name__=='__main__':main()
