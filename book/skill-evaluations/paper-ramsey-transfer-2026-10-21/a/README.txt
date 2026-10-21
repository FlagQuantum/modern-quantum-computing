Result: result.json. Full complex outputs, source PDF SHA-256/locators, derivation,
explicit full pulse matrices, source-axis conversion, claim ledger and counters
are contained there. No paper page image/text is part of the delivered artifacts.

Scientific runtime: /private/tmp/mqc-writing-venv/bin/python, CPython 3.12.14,
Torch 2.13.0, FlagQuantum 0.3.1. runtime.json records exact runtime information.
No packages were installed or modified. Supplied skills and runner were not edited.

Reproduction: archive the existing raw directory and result files, then execute:
  /private/tmp/mqc-writing-venv/bin/python /private/tmp/mqc-paper-transfer/a/reproduce.py
The script intentionally refuses to overwrite an existing raw directory.
The unchanged source skill scripts are under ../packet/skills.

raw/<label>/request.json, stdout.json, stderr.txt and execution.json preserve each
of the 12 helper subprocess calls, including exits, commands and SHA-256 hashes.
raw/continuous-circuit-request.json and continuous-circuit-output.json preserve
the six additional in-process continuous circuit calls, their full outputs and
metadata. Their process stdout/stderr/exit is the enclosing workflow evidence.

Source was inspected by rendering original PDF pages 2 and 3 with pdftoppm;
the temporary page images were removed after inspection to avoid redistributing
source content. Source provenance and semantic locators are in result.json.
An attempted pdftotext extraction could not run because that command was absent.

Actual counts: 2 classical algebra calls, 8 comparison calls, 1 evolution call,
1 interference call; 9 evolution + 6 interference + 6 continuous FlagQuantum
circuits = 21 total. No hardware calls or shots.
