# Ideal interference contract 0.1.0

## Scientific imports and formula-to-code mapping

Canonical source: [3.2 Relative phase and interference](https://flagquantum.github.io/modern-quantum-computing/chapters/ch-single-qubit-states-and-rotations/#sec-single-qubit-states-and-rotations-2), book source commit `3442e4e54a9467825af5e42fd45ad6e4aca825d7`. Stable formula IDs: `formula-code-3-2-preparation`, `formula-code-3-2-cross-term`, `formula-code-3-2-visibility`, `formula-code-3-2-analyzer`, `formula-code-3-2-execution`. Imports: 3.1 pure states/Born rule; 2.1–2.2 complex arithmetic/inner products, 2.3 matrix action/order, 2.8 numerical reasoning. Drafts do not confer independent scientific acceptance.

Let the **already prepared** state be alpha|0> + beta|1>, with squared norm n near 1. D(phi) multiplies beta by exp(i phi). `post` in `run` implements this scalar action. For `phase-h`, D(-delta) acts next, then H; the final coordinates are `(alpha ± exp(i*(phi-delta))*beta)/sqrt(2)`. `reference` computes them with standard-library complex arithmetic. Expanding the squared modulus gives `n/2 ± Re(conj(alpha)*exp(i*(phi-delta))*beta)`: `cross` and `analytic` implement this independently of the tensor simulator. Using n/2 retains the actual validated floating-point norm rather than silently normalizing it to 1.

The released simulator is constructed with `Circuit(1,dtype=torch.complex128)`, `unitary(0,unitary=preparation)`, `phase(0,theta=phi)`, optionally `phase(0,theta=-delta)`, `h(0)`, and `fq.run(... outputs=[fq.probabilities()], options=...)`. The preparation matrix has columns `(alpha,beta)` and `(-conj(beta),conj(alpha))`. Their inner product cancels and their squared norms are n, so exact unit normalization makes this a unitary whose first column prepares the supplied representative from |0>. It preserves the input's common phase in the inspected output coordinates. No unverified initialization API is assumed.

For a full continuous phase scan with fixed magnitudes, the outcome-0 extrema are `n/2 ± abs(alpha)*abs(beta)` and visibility is `2*abs(alpha)*abs(beta)/n`. `fringe` returns these **analytic continuous** quantities separately from extrema over the supplied sample grid. Sparse sampling can miss either extremum. If a path amplitude is zero, visibility is zero and its relative phase is unidentifiable. With computational-only readout, interference-fringe quantities are not applicable.

## Exact JSON input

```json
{"profile":"ideal-pure-single-qubit","state":[[0.6,0],[0.8,0]],"basis":["0","1"],"angle_unit":"radian","phase_radians":[0,3.141592653589793],"readout":{"type":"phase-h","delta_radians":0},"atol":1e-10}
```

Required keys are exactly `profile`, `state`, `basis`, `angle_unit`, `phase_radians`, `readout`; optional `atol` only. The helper accepts no extra noise/shot/claim/cache fields. Preserve a caller's claim separately and compare it with the fresh results.

- Profile: `ideal-pure-single-qubit`, no channels, mixtures, noise, shots, hardware or intermediate measurement. Unknown profiles return unsupported.
- State: two `[real,imaginary]` pairs of finite JSON numbers, each coordinate part bounded by 2. No booleans/strings, batch axis or silent casting/normalization. Squared norm must already be within absolute 1e-12 of 1. Basis exactly `["0","1"]`.
- Units: explicit `radian`. Other units require an explicit documented conversion with preserved source values, not relabeling. If units are not supplied, the agent must clarify before constructing a helper request.
- Scan: a list of 1–129 real phase values in [-1024,1024] radians; duplicates and endpoints are allowed. No implicit sweep, angle reduction or inferred fitting.
- Readout: exactly `{"type":"computational"}` (no analyzer) or `{"type":"phase-h","delta_radians":number}` with delta in [-1024,1024]. A missing analyzer is semantically ambiguous; do not default it.
- Absolute comparison tolerance: default 1e-10, permitted [1e-12,1e-8], zero relative tolerance. This is a dimensionless numerical error budget, not a statistical confidence bound. Validation tolerance remains 1e-12 independently of the requested verification tolerance.

Nonstandard JSON constants, malformed JSON, duplicate keys, nonfinite numbers and schema violations are rejected. Experimental order must match the declared profile; raw circuits with a different chronology require another execution contract or an explicitly justified separate derivation, not a silently rewritten circuit.

## Output and evidence

`status=verified` (exit 0) includes:

- actual CPython, FlagQuantum and Torch versions; explicit CPU/statevector/PyTorch/complex128 options with fallback and approximation disabled;
- declared input/readout and operation order; one record per phase;
- scalar post-phase and final reference coordinates, actual statevector and probabilities, separate analytic probabilities and real cross term;
- actual shape `(1,2)`, CPU complex128 state and float64 probability dtypes, and finite checks;
- per-point maximum absolute coordinate error, probability/formula error, probability/Born error and normalization error; all must be at most `atol`;
- continuous-scan fringe predictions and sampled-grid extrema clearly separated, or an explicit not-applicable result for computational-only readout; relative-phase identifiability for the analyzed scan.

A runtime must be **CPython 3.12** before object parsing. Packages must be FlagQuantum 0.3.1 and Torch base version 2.13.0; any wheel suffix is recorded. No dependencies are installed by the helper. The complete existing repository example environment is pinned in `requirements-examples.txt`. Missing/incompatible runtimes/packages return `unsupported` (exit 3). Dependency/import/backend failures return `execution_failed` (exit 4), not simulated results.

`verification_failed` (exit 1) preserves numerical records that exceeded the declared error budget. `invalid_input` (exit 2) identifies schema or invalid-state violations. `unsupported` (exit 3) identifies unsupported representations, units, bases, readouts or runtimes. These are separate from rejecting a **user's scientific claim**, which the agent evaluates from actual successful experiment records. A verified ideal run neither certifies a noisy laboratory result nor establishes a whole-paper reproduction, arbitrary tomography, or general distinguishability of different pure states.
