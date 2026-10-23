"""Execute section 7.4's literal cumulative body and complete program output."""
from pathlib import Path
import contextlib
import io
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
source = (ROOT/'docs/chapters/ch-entanglement-and-quantum-information-protocols.md').read_text()
body = source.split('<span id="sec-entanglement-and-quantum-information-protocols-4"></span>', 1)[1]
body = body.split('<!-- end-section-7.4 -->', 1)[0]
blocks = re.findall(r'```python\n(.*?)```\s*```text\n(.*?)```', body, re.S)
assert len(blocks) == 8 and len(re.findall(r'```python\n', body)) == 8
namespace = {}
for number, (code, expected) in enumerate(blocks, 1):
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        exec(compile(code, f'7.4-fragment-{number}', 'exec'), namespace)
    assert captured.getvalue() == expected, (number, captured.getvalue(), expected)
assert namespace['t'].RUNS == 20, namespace['t'].RUNS
print('8 cumulative 7.4 body fragments:20 native circuits, assertions and exact printed outputs passed.')
expected = re.search(r'Expected output of the complete program:\s*```text\n(.*?)```', body, re.S)[1]
actual = subprocess.check_output([sys.executable, str(ROOT/'examples/foundations/chsh_experiment.py')], text=True, timeout=120)
assert actual == expected, (actual, expected)
print('Complete 7.4 program:117 native circuits and exact output passed;13 malformed contracts rejected.')
