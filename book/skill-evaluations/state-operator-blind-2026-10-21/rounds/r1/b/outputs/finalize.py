import json,pathlib
O=pathlib.Path(__file__).resolve().parent
results=json.loads((O/'results.json').read_text()); verification=json.loads((O/'verification.stdout.json').read_text())
explanations={
'B1':'Compare diag(I,U) and diag(I,V) in declared basis 00,01,10,11, with the first qubit as control. Use one phase on the entire 4x4 operation. The helper returned outside_tolerance with Frobenius residual 0.640234328796479 at tolerance 1e-10 (exit 1, a valid negative comparison). Thus the full operations are not numerically equivalent up to one overall phase. Independent trace-identity calculation confirms the residual; coherent input (|00>+|10>)/sqrt(2) produces output-ray fidelity 0.9001502824096898, so a relative branch phase matters. The basis labels are caller assertions. This is bounded numerical evidence, not an exact equality theorem or physical hardware test.',
'B2':'Compare the whole isolated 2x2 unitary in basis 0,1 with a single phase across every entry. The helper returned outside_tolerance with Frobenius residual 0.6496362243361173 at tolerance 1e-10 (exit 1, a valid negative comparison). Thus these gates are not numerically equivalent for arbitrary coherent inputs up to a single overall phase. Individual computational-basis output rays can agree while their relative phases differ. Independent trace-identity calculation confirms the residual, and input (|0>+|1>)/sqrt(2) gives output-ray fidelity 0.8001180741258791. No independent column alignment was performed. The basis labels are caller assertions; the result is numerical evidence rather than an exact theorem.'}
for r in results:
 tid=r['id']; r['verification']=verification[tid]
 if tid in explanations:
  (O/(tid+'.explanation.txt')).write_text(explanations[tid]+'\n')
  r['outcome']={'equivalent_up_to_single_overall_phase':False,'basis':['00','01','10','11'] if tid=='B1' else ['0','1'],'atol':1e-10,'residual':json.loads((O/(tid+'.stdout.json')).read_text())['decision_residual']}
 else: r['outcome']=json.loads((O/'B3.stdout.json').read_text())
(O/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'results_path':str(O/'results.json'),'all_verification_passed':all(v['passed'] for v in verification.values()),'unresolved_questions':[]}))
