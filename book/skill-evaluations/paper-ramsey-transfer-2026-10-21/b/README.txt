Independent blind paper-transfer trial B

Result: result.json
Independent non-helper numerical evidence: independent-reference.json
Actual helper evidence: run/<stage>/{request.json,stdout.json,stderr.txt,execution.json}
Actual runner evidence: runner.{execution.json,stdout.txt,stderr.txt}
Continuous circuit evidence: run/continuous-circuit.json

Reproduce with the supplied packet unchanged and the compatible existing runtime:
/private/tmp/mqc-writing-venv/bin/python /private/tmp/mqc-paper-transfer/b/reproduce.py /private/tmp/mqc-paper-transfer/b/fresh-reproduction
Choose a fresh destination each time; the supplied runner preserves existing evidence by rejecting an existing run directory.

Source pages 2 and 3 were visually inspected using pdftoppm renders in this workspace. Those intermediate PNGs are source inspection evidence, not publication artifacts. The result contains only source locators, URL, hash, mathematical claims and explicit chosen/new conventions.

Actual counters for this trial: 1 runner invocation; 24 helper calls (7 algebra, 1 evolution, 1 interference, 15 comparison); 19 FlagQuantum circuits (9 evolution, 5 interference, 5 continuous); 5 independent final points; independent reference itself executes no FlagQuantum circuits. Auxiliary controlled mismatch is intentional and preserved.
