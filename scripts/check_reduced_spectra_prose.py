"""Execute only8.5literal code/output pairs and complete companion."""
from pathlib import Path
import contextlib,io,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
s=(ROOT/'docs/chapters/ch-density-matrices-reduced-states-and-purification.md').read_text()
body=s.split('<span id="sec-density-matrices-reduced-states-and-purification-5"></span>',1)[1].split('<!-- end-section-8.5 -->',1)[0]
f=chr(96)*3;blocks=re.findall(f+r'python\n(.*?)'+f+r'\s*'+f+r'text\n(.*?)'+f,body,re.S)
assert len(blocks)==8 and body.count(f+'python\n')==8
assert all(ord(c)>=32 or c in '\n\t'for c in body)
ns={}
for j,(code,expected)in enumerate(blocks,1):
 out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(code,f'8.5-fragment-{j}','exec'),ns)
 assert out.getvalue()==expected,(j,out.getvalue(),expected)
assert ns['g'].RUNS==11
print('Eight literal8.5units:11native circuits,all assertions and exact outputs passed.')
expected=re.search('Expected output of the complete program:'+r'\s*'+f+r'text\n(.*?)'+f,body,re.S)[1]
actual=subprocess.check_output([sys.executable,str(ROOT/'examples/foundations/reduced_spectra.py')],text=True,timeout=120)
assert actual==expected,(actual,expected)
print('Complete8.5program:44native circuits,full spectra/eigenpair/purity checks,12malformed contracts and exact output passed.')
