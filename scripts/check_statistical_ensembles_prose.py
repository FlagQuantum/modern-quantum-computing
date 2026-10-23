"""Execute only8.1literal code/output units and complete companion."""
from pathlib import Path
import re,contextlib,io,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
s=(ROOT/'docs/chapters/ch-density-matrices-reduced-states-and-purification.md').read_text()
body=s.split('<span id="sec-density-matrices-reduced-states-and-purification-1"></span>',1)[1].split('<!-- end-section-8.1 -->',1)[0]
f=chr(96)*3
blocks=re.findall(f+r'python\n(.*?)'+f+r'\s*'+f+r'text\n(.*?)'+f,body,re.S)
assert len(blocks)==8 and body.count(f+'python\n')==8
rows=body.split('| Operation in this section |',1)[1].split('The public density request',1)[0]
rows=[r for r in rows.splitlines() if r.startswith('|')]
assert len(rows)==6 and all(r.count('|')==4 for r in rows)
assert all(ord(c)>=32 or c in '\n\t' for c in body)
ns={}
for j,(code,expected) in enumerate(blocks,1):
 out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(code,f'8.1-fragment-{j}','exec'),ns)
 assert out.getvalue()==expected,(j,out.getvalue(),expected)
assert ns['e'].RUNS==34
print('Eight literal8.1units:34native circuits,all assertions and exact outputs passed.')
expected=re.search('Expected output of the complete program:'+r'\s*'+f+r'text\n(.*?)'+f,body,re.S)[1]
actual=subprocess.check_output([sys.executable,str(ROOT/'examples/foundations/statistical_ensembles.py')],text=True,timeout=120)
assert actual==expected,(actual,expected)
print('Complete8.1program:54native circuits,36classical effects/probes,14malformed contracts and exact output passed.')
