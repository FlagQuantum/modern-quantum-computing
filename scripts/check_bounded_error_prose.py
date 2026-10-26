"""Execute only14.3 literal code/output pairs and complete companion."""
from pathlib import Path
import contextlib,io,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
s=(ROOT/'docs/chapters/ch-computational-models-complexity-and-quantum-advantage.md').read_text()
body=s.split('<span id="sec-computational-models-complexity-and-quantum-advantage-3"></span>',1)[1].split('<!-- end-section-14.3 -->',1)[0]
f=chr(96)*3;blocks=re.findall(f+r'python\n(.*?)'+f+r'\s*'+f+r'text\n(.*?)'+f,body,re.S)
assert len(blocks)==8 and body.count(f+'python\n')==8
assert all(ord(c)>=32 or c in '\n\t'for c in body)
ns={}
for j,(code,expected)in enumerate(blocks,1):
 out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(code,f'14.3-fragment-{j}','exec'),ns)
 assert out.getvalue()==expected,(j,out.getvalue(),expected)
assert ns['b'].RUNS==8
print('Eight literal14.3units:10native circuits,all assertions and exact outputs passed.')
expected=re.search('Expected output of the complete program:'+r'\s*'+f+r'text\n(.*?)'+f,body,re.S)[1]
actual=subprocess.check_output([sys.executable,str(ROOT/'examples/foundations/bounded_error.py')],text=True,timeout=120)
assert actual==expected,(actual,expected)
print('Complete14.3program:82native circuits,bounded-error/promise/majority checks and exact output passed.')
