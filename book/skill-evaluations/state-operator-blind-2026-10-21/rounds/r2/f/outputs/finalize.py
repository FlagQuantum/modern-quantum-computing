import json,pathlib,subprocess,sys
root=pathlib.Path('/private/tmp/mqc-comparison-blind-r2/f'); out=root/'outputs'
(out/'F1/explanation.md').write_text('''# F1 fresh audit

Selected the available compare-quantum-states-and-operators skill because the request supplies two isolated pure state arrays of dimension 4, explicit matching basis labels 00,01,10,11, global-phase scope, and absolute Euclidean tolerance 1e-10. No clarification is required. The cached result is evidence to audit, not input to the helper.

Fresh helper execution exited 0 with within_tolerance. The aligned Euclidean residual is 7.855646793595436e-17, versus raw distance 0.6091648630920243. Multiplying the whole b vector by 0.8144590847870377 - 0.5802209916987329i aligns it with a. Independent arithmetic confirms this decision and squared norms 1.0000000000000002 and 1.0. Thus the cached outside_tolerance decision and residual 0.5 are inconsistent with the raw supplied arrays under the requested comparison.

The basis is the caller's declaration; no producer metadata was supplied to establish physical array ordering. This binary64 comparison establishes agreement within the declared numerical tolerance, not exact equality, circuit equivalence, or physical implementation equivalence. No normalization, permutation, or entry changes were applied.
''')
(out/'F2/explanation.md').write_text('''# F2 input validation

Selected the available compare-quantum-states-and-operators skill for the requested dimension-2 unitary comparison in basis 0,1, with one global phase and Frobenius tolerance 1e-10. No context is missing and no clarification is required.

The helper exited 2 with invalid_input: the matrix must already be unitary within entrywise U†U validation tolerance 1e-12. The identity a is unitary, but b†b = [[1,0.6],[0.6,1]]. Both columns have unit squared norm, as claimed, yet their inner product is 0.6 and they are not orthogonal. Independent direct Gram-matrix computation verifies this failure. Therefore these supplied arrays cannot be compared as two unitaries under this profile. This is invalid input, not an outside-tolerance unitary comparison; there is no valid operator-equivalence decision.

All entries were preserved. Orthogonalization or normalization would change the requested matrices and was not performed. Basis labels remain caller assertions. No physical gate or circuit was executed or inferred from these arrays.
''')
args=[sys.executable,str(out/'verify.py')]
p=subprocess.run(args,text=True,capture_output=True)
(out/'verification.stdout.txt').write_text(p.stdout); (out/'verification.stderr.txt').write_text(p.stderr)
(out/'verification.execution.json').write_text(json.dumps({'argv':args,'exit_code':p.returncode},indent=2)+'\n')
assert p.returncode==0
verification=json.loads((out/'verification.json').read_text())
results=json.loads((out/'results.json').read_text())
for r in results:
    r['verification']['status']='passed'
    r['verification']['details']=verification[r['id']]
    r['evidence_paths'] += ['outputs/verify.py','outputs/verification.json','outputs/verification.stdout.txt','outputs/verification.stderr.txt','outputs/verification.execution.json','outputs/input_hashes.json']
    if r['id']=='F2': r['limitations'].append('Input b is nonunitary; no unitary equivalence conclusion is valid.')
(out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'results_path':str(out/'results.json'),'verification_exit_code':p.returncode,'unresolved_questions':[]},indent=2))
