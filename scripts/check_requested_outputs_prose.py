"""Execute only 44.1 literal code/output pairs and the complete companion."""
from pathlib import Path
import contextlib,io,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
s=(ROOT/'docs/chapters/ch-exact-simulation-tensor-execution-and-numerical-reliability.md').read_text()
body=s.split('<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-1"></span>',1)[1].split('<!-- end-section-44.1 -->',1)[0]
f=chr(96)*3;blocks=re.findall(f+r'python\n(.*?)'+f+r'\s*'+f+r'text\n(.*?)'+f,body,re.S)
assert len(blocks)==8 and body.count(f+'python\n')==8
assert all(ord(c)>=32 or c in '\n\t'for c in body)
prose=re.sub(f+r'.*?'+f,'',body,flags=re.S)
prose=re.sub(r'\$\$.*?\$\$|\\\(.*?\\\)|`[^`]*`|\*\*.*?\*\*','',prose,flags=re.S)
assert '*' not in prose,'Unprotected prose star can corrupt conjugate notation;use inlineTeX'
ns={}
for j,(code,expected)in enumerate(blocks,1):
 out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(code,f'44.1-fragment-{j}','exec'),ns)
 assert out.getvalue()==expected,(j,out.getvalue(),expected)
assert ns['o'].RUNS==2
print('Eight literal 44.1 units: 3 native circuits, all assertions and exact outputs passed.')
expected=re.search('Expected output of the complete program:'+r'\s*'+f+r'text\n(.*?)'+f,body,re.S)[1]
actual=subprocess.check_output([sys.executable,str(ROOT/'examples/foundations/requested_outputs.py')],text=True,timeout=120)
assert actual==expected,(actual,expected)
print('Complete 44.1 program: 56 native circuits, payload/output/reference checks and exact output passed.')
print('Actual complete-program stdout follows:')
print(actual,end='')
