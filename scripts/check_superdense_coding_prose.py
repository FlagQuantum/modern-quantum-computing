"""Execute section7.6's literal cumulative body and complete output,scoped by stable markers."""
from pathlib import Path
import contextlib
import io
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
source=(ROOT/'docs/chapters/ch-entanglement-and-quantum-information-protocols.md').read_text()
body=source.split('<span id="sec-entanglement-and-quantum-information-protocols-6"></span>',1)[1].split('<!-- end-section-7.6 -->',1)[0]
f=chr(96)*3
blocks=re.findall(f+r'python\n(.*?)'+f+r'\s*'+f+r'text\n(.*?)'+f,body,re.S)
assert len(blocks)==8 and body.count(f+'python\n')==8
table=body.split('| Message | Alice',1)[1].split('The four message choices',1)[0]
rows=[line for line in table.splitlines() if line.startswith('|')]
assert len(rows)==5 and all(line.count('|')==4 for line in rows)
namespace={}
for number,(code,expected) in enumerate(blocks,1):
    captured=io.StringIO()
    with contextlib.redirect_stdout(captured):
        exec(compile(code,f'7.6-fragment-{number}','exec'),namespace)
    assert captured.getvalue()==expected,(number,captured.getvalue(),expected)
assert namespace['s'].RUNS==33
print('8 cumulative7.6body units:33 native circuits,exact outputs and assertions passed.')
expected=re.search('Expected output of the complete program:'+r'\s*'+f+r'text\n(.*?)'+f,body,re.S)[1]
actual=subprocess.check_output([sys.executable,str(ROOT/'examples/foundations/superdense_coding.py')],text=True,timeout=120)
assert actual==expected,(actual,expected)
print('Complete7.6program:229 native circuits,exact output and16 malformed-contract rejections passed.')
