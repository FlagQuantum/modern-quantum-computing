"""Execute the cumulative section 7.1 body fragments and compare printed output."""
from pathlib import Path
import contextlib
import io
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
path = ROOT/'docs/chapters/ch-entanglement-and-quantum-information-protocols.md'
body = path.read_text().split('<span id="sec-entanglement-and-quantum-information-protocols-1"></span>', 1)[1]
# Keep this checker scoped to 7.1 when future sections are appended.
body = body.split('<!-- end-section-7.1 -->', 1)[0]
blocks = re.findall(r'```python\n(.*?)```\s*```text\n(.*?)```', body, re.S)
assert len(blocks) == 8, len(blocks)
assert len(re.findall(r'```python\n',body)) == len(blocks)
namespace = {}
for number, (code, expected) in enumerate(blocks, 1):
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exec(compile(code, f'7.1-fragment-{number}', 'exec'), namespace)
    assert stdout.getvalue() == expected, (number, stdout.getvalue(), expected)
print('8 cumulative 7.1 prose fragments: exact outputs and assertions passed.')
expected = re.search(r'Expected output of the complete program:\s*```text\n(.*?)```', body, re.S)[1]
actual = subprocess.check_output([sys.executable, str(ROOT/'examples/foundations/product_entanglement.py')], text=True)
assert actual == expected, (actual, expected)
print('Complete 7.1 example: exact expected-output comparison passed.')
