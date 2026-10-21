# Paper-to-skills transfer: an ideal Ramsey claim

**Pilot 0.1.0 · October 21, 2026 · scientific acceptance pending.** This experiment asks whether an agent can extract a bounded claim from an original research paper, resolve conventions, choose the four existing skills, execute FlagQuantum and verify the result. It adds neither a fifth skill nor a textbook section. A small, conductor-selected paper pilot does not establish a general paper-reproduction success rate.

[Runnable example](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/integration/paper_ramsey_transfer.py) · [Previous composition experiment](four-skill-integration.md) · [Acceptance standard](paper-reproduction-standard.md) · [Dual entry](dual-entry.md)

## Source and registered scope

K. Liu et al., *A two-fold quantum delayed-choice experiment in a superconducting circuit*, [arXiv:1608.04908v1](https://arxiv.org/abs/1608.04908v1), submitted August 17, 2016; related journal publication [Science Advances 3, e1603159 (2017)](https://doi.org/10.1126/sciadv.1603159). The versioned preprint is the execution target. The journal version is bibliographic context; no assertion of byte-identical versions is needed.

Read PDF page 2, Figure 1d and the vacuum-WPD discussion following Eq. (2); page 3, Figure 2 supplies the phase-axis convention. In vacuum, the cavity interaction leaves the qubit unchanged. The stated ideal ground-state fringe is

$$
p_g(\phi)=\frac{1-\cos\phi}{2}.
$$

Our target is this **ideal vacuum-limit claim**, at six selected phase coordinates, plus independent amplitude checks under an explicit compatible pulse convention. We do not reproduce cavity entanglement, cat-state preparation, postselection, quantum erasure, decoherence, measured points or hardware calibration. The third-party PDF and page images remain outside the public repository; source URL, version, inspected locators and SHA-256 identify it.

The source PDF SHA-256 is `80f85a393022d002156381613121f09b5050bded82d13e3f9684574e88b7e134`. A locally rendered page was inspected to confirm the formula and circuit; the source is not just a search-result snippet.

## 1. Formula → convention → executable preparation

Set the ordered basis to $|g\rangle=|0\rangle$, $|e\rangle=|1\rangle$. Define the canonical Hadamard matrix $H$ and a phase matrix $D$ by

$$
H=\frac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix},\qquad
D(\phi)=\begin{pmatrix}1&0\\0&e^{i\phi}\end{pmatrix}.
$$

The source describes balanced pulses and the prepared state $(|g\rangle+|e\rangle)/\sqrt2$. However, replacing *both named pulses* by the canonical matrix $H$ gives the **opposite** ground-state fringe, $(1+\cos\phi)/2$. A gate's name alone does not settle the pulse-phase/readout convention. This mismatch is retained as a tested candidate failure, not hidden by a probability-label swap.

A compatible ideal completion is

$$
P_1=P_2=R_y(\pi/2)=HZ
=\frac{1}{\sqrt2}\begin{pmatrix}1&-1\\1&1\end{pmatrix},\qquad Z=D(\pi).
$$

This fixes the entire matrices for this reproduction. It is a **chosen ideal completion**, not a unique inference of laboratory microwave pulses from the paper or a correction to the source. Other conventions may produce the same populations while changing full complex coordinates.

`request()` in the runnable example supplies the balanced state. The existing continuous-circuit runner prepares it through a full unitary whose columns are $(a,b)$ and $(-\overline b,\overline a)$; at $a=b=1/\sqrt2$ this is exactly $P_1$. The interference helper consumes the same intermediate amplitudes and prepares a fresh state. This staged path is separately compared with the continuous circuit; it is not persistent quantum-state transfer.

## 2. Formula → derivation → analyzer mapping

Chronological application is $P_1$, then $D(\phi)$, then $P_2$. Multiplying from the right gives

$$
|\chi(\phi)\rangle=P_2D(\phi)P_1|0\rangle
=\frac12\begin{pmatrix}1-e^{i\phi}\\1+e^{i\phi}\end{pmatrix}.
$$

Using $|1-e^{i\phi}|^2=2-2\cos\phi$ gives the target $p_g$. The other outcome is $(1+\cos\phi)/2$, and their sum is one.

The interference skill's declared analyzer is $HD(-\delta)$. Set **delta = pi radians**, because $D(-\pi)=Z$. Thus it executes $HD(-\pi)D(\phi)$, with the same chosen full-coordinate convention to numerical tolerance. The complex phase from floating-point `exp(-i*pi)` remains in the output and is checked; it is not silently rounded or aligned away.

`independent_check()` computes both components with Python scalar complex exponentials and both probabilities with cosine. It compares every continuous and staged state coordinate and every probability with zero relative tolerance. That is independent of the Torch matrix-function implementation used by two of the helpers. Numerical agreement on this finite set does not prove the analytic identity for all phases; the derivation above supplies the general identity.

## 3. Source coordinates → radians → observed results

The Figure 2 horizontal coordinate is $x=\phi/\pi$. Conversion must precede the skill call:

$$
\phi=\pi x,\qquad p_g(x)=\frac{1-\cos(\pi x)}2.
$$

These six positions are selected test coordinates, not digitized experimental measurements:

| Source-axis coordinate x | Computed ground-state probability |
|---|---|
| 0 | 0.000000000 |
| 0.23 | 0.124944465 |
| 0.5 | 0.500000000 |
| 1 | 1.000000000 |
| 1.37 | 0.698573945 |
| 2 | 0.000000000 |

At the endpoints the raw computed probability can be a tiny positive floating-point value rather than exactly zero. Only display formatting rounds it. Passing x directly to an API requiring radians is a different experiment, even if its own helper returns `verified`.

## 4. New instance → units and full phase → checked output

A separate caller extension tests transfer rather than memorizing the source curve. **These are new inputs, not parameters recovered from the paper:** cyclic frequency $f=125\,\mathrm{MHz}$, elapsed time $t=0.83\,\mathrm{ns}$, and scalar offset $c=0.17/t$ in rad/s. To create a positive relative phase on the excited amplitude under $U=\exp(-itG)$, use

$$
\omega=2\pi f,\qquad G=cI-\omega|1\rangle\langle1|,\qquad
U=e^{-ict}\operatorname{diag}(1,e^{i\omega t}).
$$

Thus $\phi=\omega t$, and the full final vector is $e^{-0.17i}|\chi(\phi)\rangle$. In code, the generator is `[[offset,0],[0,offset-omega]]`, in rad/s, and time is converted to seconds. No additional division by ℏ applies. Its dimensionless exponent fits the existing composition profile's norm bound. The target probability is **0.102527823**.

An identity shift leaves isolated probabilities unchanged but changes full coordinates. The comparison skill's coordinate and isolated-ray modes therefore have different expected decisions. The controlled diagnostic is a numerical phase-context witness; it is not an operation performed in the source experiment.

## Existing skill responsibilities and budget

| Skill | Role |
|---|---|
| Complex linear algebra 0.1.1 | Matrix exponential/action and chronological readout references; classical CPU only |
| Phase-tracked unitary evolution 0.1.0 | Declared constant generator, complete unitary, native decomposition and phase witness in actual FlagQuantum circuits |
| State/operator comparison 0.1.1 | Full-coordinate and appropriate ray/controlled comparisons, with explicit metrics |
| Qubit interference 0.1.0 | Reprepare supplied amplitudes and execute the declared phase scan/analyzer |

The caller declares maximum coordinate/probability error **1e-10**, relative tolerance zero. State Euclidean and 2×2 operator Frobenius budgets use the existing explicit factors sqrt(2) and 2. Input norm/unitarity validation stays at its separate 1e-12 contract. No tolerance is increased to force agreement. Final independent checks remain mandatory, because converting metrics does not establish an arbitrary composed-error theorem.

The author example executes **32 actual FlagQuantum simulator circuits and 39 helper calls**: 21 circuits for the six-point vacuum scan and 11 for the one-point new instance. This includes existing evolution/control diagnostics as well as the continuous and staged paths; it is not 32 independent physical experiments. The worst scalar-reference coordinate/probability error observed was **3.3306690738754696e-16**. The classical helpers contribute zero quantum circuits.

## Run and inspect

From the repository root, use the declared CPython 3.12 / FlagQuantum 0.3.1 / Torch 2.13.0 CPU complex128 environment:

```bash
paper_tmp=$(mktemp -d)
python examples/integration/paper_ramsey_transfer.py \
  --output "$paper_tmp/run" --skills-root skills
```

Expected output:

```text
source p_g: 0.000000000 0.124944465 0.500000000 1.000000000 0.698573945 0.000000000
caller extension p_g: 0.102527823
actual FlagQuantum circuits: 32
scientific acceptance: pending
```

The output directory must be new. It preserves each original request, actual helper stdout/stderr, request digests, complete statevectors, staged and continuous execution records, tolerance ledger and summary. The environment is inherited from the existing pinned example requirements; no runtime packages or skill contracts change.

## Error cases and independent agents

Author tests retain three deliberately incorrect interpretations: identical canonical H matrices, source-axis numbers submitted as radians, and cyclic Hz submitted as angular frequency. Each wrong experiment may run successfully; its candidate claim still fails comparison with the registered target. Additional comparisons show that removing the caller identity phase fails full coordinates while passing the isolated ray. A full-paper/hardware claim remains out of scope.

Three fresh agents received the original source, raw tasks, the four frozen skill packages and an optional frozen runner. The private reference key and author results were withheld. They completed **two supported transfer tasks and three claim audits**, with zero false successes or incorrect abstentions in this small sample:

| Independent agent task | Recorded outcome | Helper calls | Actual simulator circuits |
|---|---|---|---|
| A: extract and reproduce the six-point vacuum claim | Compatible convention stated; independent amplitudes/probabilities pass | 12 | 21 |
| B: caller frequency/time/identity-phase transfer, plus five scan points | Units and full phase pass; new inputs distinguished from source parameters | 24 | 19 |
| C: audit three collaborator claims | First-pulse statement supported; compound same-H claim, phase-unit claim and hardware overreach rejected | 10 | 25 |
| Total | Five task/claim dispositions pass conductor grading | 46 | 65 |

The source-translation tasks explicitly allowed a labeled compatible ideal convention, so no live clarification exchange was required or tested. Each agent explained the unresolved physical-pulse identification rather than guessing it. Agent A built its own execution path instead of using the provided composition runner; agent B used the runner and a separate SciPy dense exponential plus scalar reference. SciPy 1.18.1 was available in that recorded evaluation environment; the portable regression checker below uses standard-library scalar references and does not add SciPy as a direct example requirement.

The two author example cases and six negative/scope cases used **44 helper calls and 37 actual circuits** in total. Independent agents used the separately recorded **46 calls and 65 circuits**; regression reruns are not included in those original evaluation counts. No skill package or frozen runner changed after testing.

[Protocol, per-agent evidence and conductor grading](https://github.com/FlagQuantum/modern-quantum-computing/tree/main/book/skill-evaluations/paper-ramsey-transfer-2026-10-21) preserve requests, stdout/stderr, exits, scripts, source hashes and each claim decision. Agent scripts retain their original local packet paths as historical evidence. For a portable rerun, use the repository example and checker:

```bash
python scripts/check_paper_ramsey_transfer.py
```

The checker verifies artifact hashes and source-skill identity, independently checks archived final amplitudes and probabilities, replays all 46 blind helper calls plus five author-negative calls, and executes the complete 32-circuit example in a fresh directory. Its fresh total is 91 simulator circuits. This is a regression replay of published tasks, not another blind test. G5 scientific acceptance remains pending.

## Acceptance ledger and limitations

| Gate | Recorded state |
|---|---|
| G0 scope/feasibility | Protocol, tasks, source identity and private reference key frozen before independent-agent dispatch |
| G1 mathematical translation | Author derivation and agent evidence; compatible completion is explicit, calibrated pulse matrices remain unidentified |
| G2 implementation | Actual pinned simulator execution and independent scalar references, plus retained negative candidates |
| G3 claim comparison | Ideal vacuum probability checked; caller extension separately labeled; hardware/cavity claims excluded |
| G4 reproducible evidence | Versioned raw evidence, hashes and fresh regression execution; no paper PDF redistributed |
| G5 independent scientific acceptance | **Pending**; independent software-agent evaluation is recorded separately and is not human scholarly review |
| Reader trial / accepted release | Not run / not accepted |

All four skill packages and the 435-section curriculum remain unchanged. The pilot was not randomly selected, and source location hints reduce the retrieval burden. Agents use the same inherited model family; exact backend revisions, token counts and costs are unavailable. Logical workspace restrictions are not operating-system isolation. Publication makes these tasks known regression cases; rerunning them is not a fresh blind evaluation. This supports one scoped transfer experiment, not universal paper reproduction or an L5 release.
