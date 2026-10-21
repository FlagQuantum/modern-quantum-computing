#!/usr/bin/env python3
"""Read-only PDF inspection: retain locators/hash, not extracted paper text."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).parent
SRC=Path('/private/tmp/mqc-paper-transfer/packet/paper.pdf')
OUT=ROOT/'source-inspection';OUT.mkdir(exist_ok=True)
def run(name,cmd):
    r=subprocess.run(cmd,capture_output=True,text=True)
    (OUT/(name+'.stdout.txt')).write_text(r.stdout)
    (OUT/(name+'.stderr.txt')).write_text(r.stderr)
    (OUT/(name+'.execution.json')).write_text(json.dumps({'command':cmd,'exit_code':r.returncode},indent=2)+'\n')
    if r.returncode:raise RuntimeError(name)
    return r
PY='/Users/baai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
run('source-metadata',[PY,'-c',"from pypdf import PdfReader; import json,hashlib; from pathlib import Path; p=Path('/private/tmp/mqc-paper-transfer/packet/paper.pdf'); d=PdfReader(p); print(json.dumps({'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'pages':len(d.pages),'inspected_pages':[{'page':i+1,'extracted_character_count':len(d.pages[i].extract_text())} for i in [1,2]]}))"])
run('render',['/Users/baai/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm','-f','2','-l','3','-scale-to','1500','-png',str(SRC),str(OUT/'page')])
print(json.dumps({'status':'complete','metadata':str(OUT/'source-metadata.stdout.txt'),'rendered_pages':[str(OUT/'page-02.png'),str(OUT/'page-03.png')]}))
