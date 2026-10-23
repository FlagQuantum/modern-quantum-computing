"""Execute only7.7's cumulative literal units and complete companion output."""
from pathlib import Path
import contextlib,io,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
source=(ROOT/'docs/chapters/ch-entanglement-and-quantum-information-protocols.md').read_text()
body=source.split('<span id="sec-entanglement-and-quantum-information-protocols-7"></span>',1)[1].split('<!-- end-section-7.7 -->',1)[0]
f=chr(96)*3
blocks=re.findall(f+r'python\n(.*?)'+f+r'\s*'+f+r'text\n(.*?)'+f,body,re.S)
assert len(blocks)==8 and body.count(f+'python\n')==8
table=body.split('| Alice basis |',1)[1].split('Here ',1)[0]
rows=[x for x in table.splitlines() if x.startswith('|')]
assert len(rows)==4 and all(x.count('|')==4 for x in rows)
namespace={}
for j,(code,expected) in enumerate(blocks,1):
    captured=io.StringIO()
    with contextlib.redirect_stdout(captured):exec(compile(code,f'7.7-fragment-{j}','exec'),namespace)
    assert captured.getvalue()==expected,(j,captured.getvalue(),expected)
assert namespace['s'].RUNS==21
print('Eight literal7.7units:21native circuits,all assertions and exact outputs passed.')
expected=re.search('Expected output of the complete program:'+r'\s*'+f+r'text\n(.*?)'+f,body,re.S)[1]
actual=subprocess.check_output([sys.executable,str(ROOT/'examples/foundations/no_signalling.py')],text=True,timeout=120)
assert actual==expected,(actual,expected)
print('Complete7.7program:100native circuits,302additional classical cases,16guard rejections and exact output passed.')
