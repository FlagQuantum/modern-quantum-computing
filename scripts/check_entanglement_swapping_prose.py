"""Execute only7.8's cumulative literal code/output units and complete program."""
from pathlib import Path
import contextlib
import io
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
source = (ROOT/'docs/chapters/ch-entanglement-and-quantum-information-protocols.md').read_text()
body = source.split('<span id="sec-network-entanglement-primitives"></span>', 1)[1].split('<!-- end-section-7.8 -->', 1)[0]
f = chr(96)*3
blocks = re.findall(f+r'python\n(.*?)'+f+r'\s*'+f+r'text\n(.*?)'+f, body, re.S)
assert len(blocks) == 8 and body.count(f+'python\n') == 8
table = body.split('| Middle bits (m,n) |', 1)[1].split('The table uses', 1)[0]
rows = [row for row in table.splitlines() if row.startswith('|')]
assert len(rows) == 5 and all(row.count('|') == 5 for row in rows)
assert all(ord(c) >= 32 or c in '\n\t' for c in body)
ns = {}
for j, (code, expected) in enumerate(blocks, 1):
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        exec(compile(code, f'7.8-fragment-{j}', 'exec'), ns)
    assert output.getvalue() == expected, (j, output.getvalue(), expected)
assert ns['s'].RUNS == 12
print('Eight literal7.8units:12native circuits,all assertions and exact outputs passed.')
expected = re.search('Expected output of the complete program:'+r'\s*'+f+r'text\n(.*?)'+f, body, re.S)[1]
actual = subprocess.check_output([sys.executable, str(ROOT/'examples/foundations/entanglement_swapping.py')], text=True, timeout=120)
assert actual == expected, (actual, expected)
print('Complete7.8program:89native circuits,16guard rejections,explicit norm-underflow boundary and exact output passed.')
