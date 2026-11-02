"""Execute only the 44.6 literal units and the complete precision companion."""
from pathlib import Path
import sys,re,io,contextlib,runpy,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
s=(ROOT/'docs/chapters/ch-exact-simulation-tensor-execution-and-numerical-reliability.md').read_text()
body=s.split('<span id="sec-exact-simulation-tensor-execution-and-numerical-reliability-6"></span>',1)[1].split('<!-- end-section-44.6 -->',1)[0]
f='`'*3;blocks=re.findall(f+r'python\n(.*?)'+f+r'\s*'+f+r'text\n(.*?)'+f,body,re.S)
assert len(blocks)==8 and body.count(f+'python\n')==8
assert all(ord(c)>=32 or c in '\n\t' for c in body)
import flagquantum as fq
real=fq.run;calls=0

def counted(*args,**kwargs):
 global calls
 result=real(*args,**kwargs);calls+=1;return result
fq.run=counted;ns={}
try:
 for i,(code,expected) in enumerate(blocks,1):
  out=io.StringIO()
  with contextlib.redirect_stdout(out):exec(compile(code,f'44.6-fragment-{i}','exec'),ns)
  assert out.getvalue()==expected,(i,out.getvalue(),expected)
 assert calls==4 and ns['n'].RUNS==2
finally:fq.run=real
print('Eight literal 44.6 units: 4 native CPU runs, all assertions and exact outputs passed.')
expected=re.search('Expected output of the complete program:'+r'\s*'+f+r'text\n(.*?)'+f,body,re.S)[1]
out=io.StringIO()
with contextlib.redirect_stdout(out):data=runpy.run_path(str(ROOT/'examples/foundations/precision_drift.py'),run_name='__main__')
assert out.getvalue()==expected,(out.getvalue(),expected)
assert data['RUNS']==24
print('Complete 44.6 program: 24 native runs and all classical/error checks passed.')
print(out.getvalue(),end='')
# Runtime receipts are optional author artifacts, never a prerequisite for read-only CI.
if len(sys.argv)==2:Path(sys.argv[1]).write_text(json.dumps(data['RECEIPTS'],indent=2)+'\n')
