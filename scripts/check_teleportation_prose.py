"""Execute section7.5's literal body and complete output within its stable scope."""
from pathlib import Path
import contextlib
import io
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
source=(ROOT/'docs/chapters/ch-entanglement-and-quantum-information-protocols.md').read_text()
body=source.split('<span id="sec-entanglement-and-quantum-information-protocols-5"></span>',1)[1].split('<!-- end-section-7.5 -->',1)[0]
fence=chr(96)*3
blocks=re.findall(fence+r'python\n(.*?)'+fence+r'\s*'+fence+r'text\n(.*?)'+fence,body,re.S)
assert len(blocks)==8 and body.count(fence+'python\n')==8
# No literal ket pipes may create unintended table columns.
table=body.split('| Message (m,n)',1)[1].split('**Code and verification result.**',1)[0]
assert len([line for line in table.splitlines() if line.startswith('|')])==5
assert all(line.count('|')==5 for line in table.splitlines() if line.startswith('|'))
namespace={}
for number,(code,expected) in enumerate(blocks,1):
    captured=io.StringIO()
    with contextlib.redirect_stdout(captured):
        exec(compile(code,f'7.5-fragment-{number}','exec'),namespace)
    assert captured.getvalue()==expected,(number,captured.getvalue(),expected)
assert namespace['t'].RUNS==26
print('8 cumulative 7.5 body fragments:26 native circuits,assertions and exact outputs passed.')
expected=re.search('Expected output of the complete program:'+r'\s*'+fence+r'text\n(.*?)'+fence,body,re.S)[1]
actual=subprocess.check_output([sys.executable,str(ROOT/'examples/foundations/teleportation.py')],text=True,timeout=120)
assert actual==expected,(actual,expected)
print('Complete 7.5 program:155 native circuits and exact output passed;16 malformed contracts rejected.')
