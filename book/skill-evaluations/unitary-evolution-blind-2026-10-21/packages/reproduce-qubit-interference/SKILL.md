---
name: reproduce-qubit-interference
description: Reproduce an ideal single-qubit relative-phase scan with specified preparation and analyzer, using released FlagQuantum and independent amplitude/probability checks. Use for interference predictions; not for noisy data, hardware execution, tomography or generic state equivalence.
---

# Reproduce qubit interference

**Prototype 0.1.0.** Load [the exact experiment contract](references/contract.md) before assembling inputs. The scientific source is textbook 3.2, with pure-state/Born conventions from 3.1 and matrix order/complex arithmetic from 2.1–2.3 and numerical contracts from 2.8. These are explained drafts with scientific acceptance pending.

Establish the prepared complex amplitudes, computational basis, chronological operation order, angle units, phase scan and readout. Ask for missing or ambiguous semantic information before dependent execution. A request for “interference” does not specify whether a final analyzer is present. Do not infer radians from an unlabeled number or infer a coherent state from measured counts.

Check the actual interpreter and installed package versions. The supported profile is CPython 3.12, released FlagQuantum 0.3.1, Torch 2.13.0 (CPU execution, complex128). Select an existing compatible interpreter explicitly. If none is available, report the runtime boundary; do not silently install software, change versions or fall back to another backend.

Run the bundled helper, saving its request, actual stdout/stderr and exit code:

```bash
/path/to/python3.12 /path/to/reproduce-qubit-interference/scripts/interference.py < request.json > result.json
```

The declared experiment is **prepare the supplied state → D(phi) → optional D(-delta), H → computational readout**. Choose explicit `computational` or `phase-h` readout; the latter means the matrix H D(-delta), in that chronological order. The helper actually runs FlagQuantum. It checks full complex state coordinates, Born probabilities and a separate scalar interference formula at every supplied phase. Preserve these checks rather than merely matching a plot or accepting a cached result.

Return the selected experiment/context and units, actual numerical records, tolerances, runtime, independent checks and a claim disposition. `verified` means that this ideal experiment passed the helper's checks; it does not mean a paper's proposed formula, cached result or hardware claim is correct. Compare any supplied claim against the fresh numerical evidence and document agreement or a counterexample. An amplitude calculation, a cosine formula, sparse sampled extrema and full continuous-scan extrema are different evidence; do not substitute one for another.

Never propagate probabilities in place of amplitudes, omit the conjugate on alpha, reverse gate order, treat the analyzer delta as an unknown phase estimated from one measurement, or interpret reduced visibility alone as decoherence. An absent path has no identifiable relative phase. Equal probabilities at a fixed analyzer setting do not imply equal states. For a separate explicit ray/operator-equivalence question, select an available state/operator-comparison skill or explain that distinct amplitudes require a different comparison; this package does not depend on another installed skill to run the experiment.

Exit 0 is a verified ideal execution, 1 an internal verification failure, 2 invalid input, 3 unsupported profile/runtime, 4 execution failure. Invalid/unsupported/failed executions are not experimental evidence. Do not repair normalization, strip a batch axis, reorder bases, replace mixed states by vectors, invent APIs or claim simulation of noise, shots, intermediate measurements, arbitrary gate order or hardware. If the stated experiment lies outside this bounded profile, explain the mismatch and the required model instead of silently changing the experiment.
