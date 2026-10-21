"""Independent standard-library verification; does not import helper or Torch."""
import cmath,json,math,pathlib
ROOT=pathlib.Path('/private/tmp/mqc-algebra-blind-r1/c'); OUT=ROOT/'outputs'
def read(i):return json.loads((OUT/i/'request.json').read_text())
def decode(a):return [[complex(*z) for z in row] for row in a]
def encode(a):return [[[z.real,z.imag] for z in row] for row in a]
results={}
q=read('C1');a=decode(q['matrix']);z=a[0][0];b=a[0][1]
# A=z I+N, N^2=0, so exp(A)=exp(z)(I+N) exactly.
assert a[1][1]==z and a[1][0]==0
expz=cmath.exp(z);expected=[[expz,expz*b],[0j,expz]]
actual=decode(json.loads((OUT/'C1'/'stdout.json').read_text())['result']['value'])
residuals=[[abs(actual[i][j]-expected[i][j]) for j in range(2)] for i in range(2)]
passed=all(residuals[i][j]<=q['tolerance']['atol']+q['tolerance']['rtol']*abs(expected[i][j]) for i in range(2) for j in range(2))
entrywise=[[cmath.exp(v) for v in row] for row in a]
results['C1']={'method':'Independent closed form A=zI+N with N^2=0; exp(A)=exp(z)(I+N).','expected':encode(expected),'residuals':residuals,'passed':passed,'entrywise_exp':encode(entrywise),'claim_disposition':'rejected','counterexample':'Entrywise exp maps the (1,0) zero to 1; the true matrix exponential has zero there.','quantum_execution':False}
q=read('C2');a=decode(q['matrix']);scale=max(abs(v) for row in a for v in row);defect=max(abs(a[i][j]-a[j][i].conjugate()) for i in range(2) for j in range(2));gate=1e-12*scale
admitted=defect<=gate
assert not admitted
results['C2']={'method':'Direct scalar adjoint calculation and scale-relative admission; no symmetrization.','max_entry_scale':scale,'hermiticity_defect':defect,'admission_budget':gate,'defect_to_scale':defect/scale,'admitted':admitted,'passed':not admitted,'explanation':'A_01=i*1e-15 but conjugate(A_10)=0; defect 1e-15 exceeds 1e-27. The reconstruction atol is not the Hermitian admission rule. No Hermitian spectral decomposition is returned.','quantum_execution':False}
q=read('C3');x=complex(*q['actual']['values'][0]);y=complex(*q['reference']['values'][0]);d=x-y;error=math.hypot(d.real,d.imag);budget=q['tolerance']['atol']+q['tolerance']['rtol']*abs(y);decision=error<=budget
assert not decision
results['C3']={'method':'Independent scalar math.hypot(real difference, imaginary difference) after exact metadata equality.','metadata_match':all(q['actual'][k]==q['reference'][k] for k in ('shape','dtype','device')),'component_errors':[abs(d.real),abs(d.imag)],'complex_modulus_error':error,'budget':budget,'comparison_passed':decision,'passed':not decision,'claim_disposition':'rejected','explanation':'Both component errors equal atol=1e-9, but the complex modulus is sqrt(2)*1e-9, exceeding the budget.','quantum_execution':False}
# No logarithm chosen. Two witnesses refute uniqueness without claiming a branch.
lplus=1j*math.pi;lminus=-1j*math.pi
results['C4']={'method':'Analytic witnesses L_plus=i*pi*I and L_minus=-i*pi*I. Both exponentiate to -I and differ by 2*pi*i*I. More generally (2k+1)*i*pi*I works for each integer k.','numerical_scalar_witness_residuals':[abs(cmath.exp(lplus)+1),abs(cmath.exp(lminus)+1)],'unique':False,'passed':True,'request_disposition':'unsupported','explanation':'The skill excludes logarithm branch selection. No branch/domain was provided; no unique logarithm computed or certified. Witnesses explain nonuniqueness only.','quantum_execution':False}
for ident,result in results.items():(OUT/ident/'independent_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'all_expected_dispositions_verified':all(r['passed'] for r in results.values()),'verification_results':results},indent=2))
assert all(r['passed'] for r in results.values())
