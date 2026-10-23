"""Execute only8.3literal units and its complete companion."""
from pathlib import Path
import contextlib,io,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
s=(ROOT/'docs/chapters/ch-density-matrices-reduced-states-and-purification.md').read_text()
body=s.split('<span id="sec-density-matrices-reduced-states-and-purification-3"></span>',1)[1].split('<!-- end-section-8.3 -->',1)[0]
f=chr(96)*3
blocks=re.findall(f+r'python\n(.*?)'+f+r'\s*'+f+r'text\n(.*?)'+f,body,re.S)
assert len(blocks)==8 and body.count(f+'python\n')==8
assert all(ord(c)>=32 or c in '\n\t' for c in body)
ns={}
for j,(code,expected)in enumerate(blocks,1):
    out=io.StringIO()
    with contextlib.redirect_stdout(out):exec(compile(code,f'8.3-fragment-{j}','exec'),ns)
    assert out.getvalue()==expected,(j,out.getvalue(),expected)
assert ns['d'].RUNS==13
print('Eight literal8.3units:13native circuits,all assertions and exact outputs passed.')
expected=re.search('Expected output of the complete program:'+r'\s*'+f+r'text\n(.*?)'+f,body,re.S)[1]
actual=subprocess.check_output([sys.executable,str(ROOT/'examples/foundations/density_updates.py')],text=True,timeout=120)
assert actual==expected,(actual,expected)
print('Complete8.3program:58native circuits,13malformed contracts,rare/zero/underflow and exact output passed.')
