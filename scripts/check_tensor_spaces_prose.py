"""Execute the cumulative section 4.1 fragments and check their displayed outputs."""
from pathlib import Path
import re,io,contextlib,subprocess,sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
p=ROOT / Path('docs/chapters/ch-composite-systems-tensor-products-and-qubit-ordering.md')
s=p.read_text().split('<span id="sec-composite-systems-tensor-products-and-qubit-ordering-2">')[0]; ns={}
blocks=re.findall(r'```python\n(.*?)```\s*```text\n(.*?)```',s,re.S)
assert len(blocks)==7,len(blocks)
for i,(code,want) in enumerate(blocks,1):
    out=io.StringIO()
    with contextlib.redirect_stdout(out):exec(compile(code,f'4.1-fragment-{i}','exec'),ns)
    assert out.getvalue()==want,(i,out.getvalue(),want)
print('7 cumulative prose fragments: exact outputs and assertions passed.')
want=re.search(r'Expected output of the complete program:\s*```text\n(.*?)```',s,re.S)[1]
out=subprocess.check_output([sys.executable,str(ROOT / 'examples/foundations/tensor_spaces.py')],text=True)
assert out==want,(out,want)
print('Complete example: exact expected-output comparison passed.')
