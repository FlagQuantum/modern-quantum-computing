#!/usr/bin/env python3
"""Execute the marked cumulative body examples and their complete references.

Each section receives a fresh namespace. Displayed stdout is checked exactly;
assertions inside each fragment check numerical values and failure witnesses.
This is an author execution check, not mathematical or independent review.
"""
import argparse
import contextlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--section', action='append', help='Check only this section; repeatable')
    args = parser.parse_args()
    manifest = json.loads((ROOT/'book/formula-code-examples.json').read_text())
    selected = args.section or list(manifest['sections'])
    if set(selected)-set(manifest['sections']):
        parser.error('Unknown section requested')
    total = 0
    for ref in selected:
        spec = manifest['sections'][ref]
        source = (ROOT/spec['body']).read_text()
        match = re.search(rf'^## {re.escape(ref)} .*?(?=^## \d+\.\d+ |\Z)', source, re.M|re.S)
        if match is None:
            raise AssertionError(f'Missing section {ref}')
        body = match[0]
        fragments = re.findall(r'<!-- formula-code: ([\w.\-]+) -->\s*```python\n(.*?)```\s*```text\n(.*?)```',body,re.S)
        assert [item[0] for item in fragments] == spec['fragments'], f'{ref}: missing/reordered fragments'
        assert len(re.findall(r'^```python$',body,re.M)) == len(fragments), f'{ref}: untracked Python block'
        namespace = {'__name__':f'formula_code_section_{ref}'}
        for name,code,expected in fragments:
            captured = io.StringIO()
            with contextlib.redirect_stdout(captured):
                exec(compile(code,f'{spec["body"]}:{name}','exec'),namespace)
            actual = captured.getvalue()
            assert actual == expected, f'{name}: stdout differs\nactual={actual!r}\nexpected={expected!r}'
        expected_full = re.search(r'Expected output:\s*```text\n(.*?)```',body,re.S)
        assert expected_full, f'{ref}: missing complete program output'
        result = subprocess.run([sys.executable,str(ROOT/spec['script'])],cwd=ROOT,text=True,
                                capture_output=True,check=True,timeout=120)
        assert result.stdout == expected_full[1], f'{ref}: full program stdout differs\n{result.stdout}'
        total += len(fragments)
        print(f'{ref}: {len(fragments)} body fragments and complete program output passed.',flush=True)
    print(f'{len(selected)} existing sections / {total} body fragments: all assertions and exact outputs passed.')


if __name__ == '__main__':
    main()
