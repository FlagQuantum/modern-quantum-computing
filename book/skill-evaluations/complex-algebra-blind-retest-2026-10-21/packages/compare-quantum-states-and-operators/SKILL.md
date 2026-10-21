---
name: compare-quantum-states-and-operators
description: Compare one- or two-qubit pure states and unitary matrices with explicit basis and phase scope, including a one-control gate context. Use for numerical equivalence checks; density matrices, channels and hardware statistics require another profile.
---

# Compare quantum states and operators

**Prototype 0.1.1.** Author verification is separate from independent agent evaluation and scientific acceptance. This repository package is not installed globally or released as an accepted skill.

Ask what is being compared and which phase scope matters if the request is ambiguous. Do not silently choose global-phase equivalence. Obtain both arrays and their basis labels; a supplied convention is an assertion by the caller, not evidence of the array's actual order.

Read [the input/output and mathematical contract](references/contract.md) before preparing a request. The sources are textbook 3.1 (pure states and ray distance) and 3.7 (whole-operator and controlled-context comparisons), with the complex arithmetic and numerical contracts of 2.1, 2.2, 2.8 and the phase-tracked decomposition of 3.6. Their drafts explain the prerequisite mathematics; no other installed skill is required for this prototype.

Check the actual interpreter version before executing the helper. This validated profile requires **CPython 3.12**. Resolve a compatible interpreter explicitly rather than assuming `python` or `python3` names it. If none is available, report the runtime boundary; do not install or change the environment silently. Save the actual runtime returned by the helper with the result. An unsupported-runtime response is not an object-comparison result.

Use the bundled standard-library helper with the selected interpreter:

```bash
/path/to/python3.12 /path/to/compare-quantum-states-and-operators/scripts/compare.py < request.json > result.json
```

The helper supports dimension 2 or 4 only. Choose `coordinates` to retain phase, `global-phase` to permit one phase for the entire state or isolated unitary, or `controlled` to compare the full controlled extensions of two dimension-2 target gates. Never align columns separately. Never remove a target phase before constructing its controlled extension. Equal computational-basis probabilities alone do not establish state equality.

Return the declared object/context, basis, actual structured result, numerical tolerance and limitations with the saved request/result. Exit 1 is a valid outside-tolerance result; exits 2 and 3 require explaining invalid input or unsupported scope, not claiming inequality. Missing context requires clarification. Do not normalize, cast away imaginary parts, infer basis permutations, invent execution, or infer a theorem from floating-point agreement. Exactly zero overlap has no identifiable aligning phase; the helper selects 1 as a deterministic minimizer. Near-zero overlap makes that phase unstable even when the residual is stable.

For FlagQuantum outputs, first check the real API/version, shape, dtype, device, finiteness, normalization and declared ordering in the producing program. Export exactly one validated sample to the JSON profile; do not hide batch axes or silently widen low-precision results. This helper itself does not execute a circuit. The repository evaluation adapter uses released FlagQuantum 0.3.1 on CPU complex128 and records actual circuit comparisons.

For mixed states, channels, shot distributions, larger registers, unknown basis or a coherent control context beyond this profile, report the boundary and the needed representation/context. Do not substitute a pure-state comparison or a simulator run for the missing claim.
