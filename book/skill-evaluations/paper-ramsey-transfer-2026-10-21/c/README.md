Blind audit completed using only the assigned task and packet for scientific inputs.

- `result.json`: dispositions, explicit basis and phase conventions, source URL/SHA256/page/figure locators, numerical counterexamples, missing assumptions and actual counters.
- `audit.py`: reproducible four-skill executions. Existing evidence directories are never overwritten. To rerun, use `/private/tmp/mqc-writing-venv/bin/python audit.py --output /absolute/fresh-directory/evidence`; the result is saved beside that evidence directory.
- `evidence/`: exact helper requests, actual stdout/stderr and process exits for each of the 10 calls, plus runtime and call ledger. The operator-comparison exit 1 is an expected valid outside-tolerance decision.
- `audit.stdout.txt`, `audit.stderr.txt`, `audit.execution.json`: top-level actual execution records.
- `inspect_source.py`, `source-inspection/`: reproducible source hash/page metadata and visual-inspection records; rendered pages are private audit evidence, not publication artifacts. No source paper text is embedded in `result.json`.

The numerical environment was CPython 3.12.14, FlagQuantum 0.3.1, Torch 2.13.0; all simulator runs used CPU/PyTorch/statevector/complex128 with fallback and approximation disabled. Tolerance: absolute 1e-10, relative zero. Comparisons use their documented Euclidean/Frobenius metric at 1e-10.

Actual totals: 10 skill calls; 25 FlagQuantum circuits (9 unitary, 16 interference); 2 classical algebra calls and 3 standard-library comparison calls. No hardware, shots, noise/channel simulations, joint qubit-cavity simulations or human scientific reviews.

The first-pulse plus state agrees with the paper. The same-standard-H compound claim fails; Figure 2 coordinates require multiplication by pi; matching the ideal vacuum fringe does not establish the remaining experimental mechanisms or data.
