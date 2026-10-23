"""Execute only7.9literal units and complete companion,with exact output checks."""
from pathlib import Path
import contextlib
import io
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
source = (ROOT/'docs/chapters/ch-entanglement-and-quantum-information-protocols.md').read_text()
body = source.split('<span id="sec-entanglement-and-quantum-information-protocols-8"></span>', 1)[1].split('<!-- end-section-7.9 -->', 1)[0]
f = chr(96)*3
blocks = re.findall(f+r'python\n(.*?)'+f+r'\s*'+f+r'text\n(.*?)'+f, body, re.S)
assert len(blocks) == 8 and body.count(f+'python\n') == 8
rows = body.split('| Task | Prior shared resource |', 1)[1].split('These are accounts', 1)[0]
rows = [row for row in rows.splitlines() if row.startswith('|')]
assert len(rows) == 5 and all(row.count('|') == 5 for row in rows)
assert all(ord(c) >= 32 or c in '\n\t' for c in body)
ns = {}
for j, (code, expected) in enumerate(blocks, 1):
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        exec(compile(code, f'7.9-fragment-{j}', 'exec'), ns)
    assert output.getvalue() == expected, (j, output.getvalue(), expected)
assert ns['t'].RUNS == 28
print('Eight literal7.9units:28native circuits,all assertions and exact outputs passed.')
expected = re.search('Expected output of the complete program:'+r'\s*'+f+r'text\n(.*?)'+f, body, re.S)[1]
actual = subprocess.check_output([sys.executable, str(ROOT/'examples/foundations/entanglement_limits.py')], text=True, timeout=120)
assert actual == expected, (actual, expected)
print('Complete7.9program:51native circuits,12malformed-contract rejections and exact output passed.')
