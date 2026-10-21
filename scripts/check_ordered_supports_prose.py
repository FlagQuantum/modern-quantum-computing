"""Execute the cumulative section 4.4 body fragments and compare printed output."""
from pathlib import Path
import contextlib
import io
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
path = ROOT/'docs/chapters/ch-composite-systems-tensor-products-and-qubit-ordering.md'
body = path.read_text().split('<span id="sec-composite-systems-tensor-products-and-qubit-ordering-4"></span>', 1)[1]
# Keep this checker scoped to 4.4 when future sections are appended.
body = body.split('<span id="sec-composite-systems-tensor-products-and-qubit-ordering-5">', 1)[0]
blocks = re.findall(r'```python\n(.*?)```\s*```text\n(.*?)```', body, re.S)
assert len(blocks) == 8, len(blocks)
assert len(re.findall(r'```python\n',body)) == len(blocks)
namespace = {}
for number, (code, expected) in enumerate(blocks, 1):
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exec(compile(code, f'4.4-fragment-{number}', 'exec'), namespace)
    assert stdout.getvalue() == expected, (number, stdout.getvalue(), expected)
print('8 cumulative 4.4 prose fragments: exact outputs and assertions passed.')
expected = re.search(r'Expected output of the complete program:\s*```text\n(.*?)```', body, re.S)[1]
actual = subprocess.check_output([sys.executable, str(ROOT/'examples/foundations/ordered_supports.py')], text=True)
assert actual == expected, (actual, expected)
print('Complete 4.4 example: exact expected-output comparison passed.')
