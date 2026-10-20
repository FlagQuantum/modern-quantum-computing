# Topological parity-readout controversy: version and argument audit

**Checked 2026-10-20 · planning only.** Source and argument planning only. Full accessible manuscripts and the joint review record were read; this is not a new chapter, a referee verdict or an independent reanalysis of the device data.

[Experimental evidence ledger](topological-experiments.md) · [Chapter 40 proof plan](../proof-plans/physical-platforms.md#chapter-40-topological-quantum-computation-and-candidate-physical-realizations) · [Exact sources and hashes](proof-sources.md)

## Accessed versions and identity boundaries

The full public comment, early response and later rebuttals have different roles. The accepted manuscript is identified by the university record, title/author and matching journal DOI; the [institutional record](https://research-portal.st-andrews.ac.uk/en/publications/on-the-robustness-of-topological-gap-detection-via-transport/) contains an unrelated 2025 DOI in its rights boilerplate, which is not used to identify the comment. The standard portal file URL returned an access challenge; the university’s public legacy file endpoint supplied the licensed manuscript without login. No source PDFs or article figures are redistributed here.

### V1: Legg early comment (11 March 2025)

[Public source](https://arxiv.org/pdf/2503.08944v1) · [LEGGPRE:argument](proof-sources.md#source-leggpre-argument).

**Access:** Full six-page v1 read.

**Version relation:** Earlier argument and figure numbering; the later accepted comment is separately pinned.

### V2: Microsoft broad response (17 April 2025)

[Public source](https://arxiv.org/pdf/2504.13240v1) · [MSPRE:statistics](proof-sources.md#source-mspre-statistics), [MSPRE:readout](proof-sources.md#source-mspre-readout).

**Access:** Full eleven-page v1 read.

**Version relation:** Explicit response to two 2025 comments. Its journal identity with the narrower 2026 reply is not established.

### V3: Legg Nature accepted manuscript (2026)

[Public source](https://pure.st-andrews.ac.uk/ws/portalfiles/portal/337134077/Legg_2026_Nature-On-robustness-topological-gap-detection_AAM_CCBY.pdf) · [LEGGAAM:argument](proof-sources.md#source-leggaam-argument), [LEGGAAM:figures](proof-sources.md#source-leggaam-figures).

**Access:** Full seven-page author manuscript read via the university public-file endpoint.

**Version relation:** Institutional title/author/journal/DOI record and manuscript title agree; contains revised main text and captions, including significant-disorder concerns.

### V4: Legg published supplement (2026)

[Public source](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-10567-8/MediaObjects/41586_2026_10567_MOESM1_ESM.pdf) · [LEGNOTES:protocol](proof-sources.md#source-legnotes-protocol), [LEGNOTES:symmetry](proof-sources.md#source-legnotes-symmetry).

**Access:** All five pages read.

**Version relation:** Version-specific Supplemental Notes 1–2 and Fig. S1–S7; sensitivity arguments persist here even when condensed or moved out of the main text.

### V5: Nature joint review and author rebuttals (2 July 2026)

[Public source](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-10568-7/MediaObjects/41586_2026_10568_MOESM1_ESM.pdf) · [TPREVIEW:referees](proof-sources.md#source-tpreview-referees), [TPREVIEW:legg](proof-sources.md#source-tpreview-legg), [TPREVIEW:revised-assessments](proof-sources.md#source-tpreview-revised-assessments), [TPREVIEW:microsoft](proof-sources.md#source-tpreview-microsoft).

**Access:** All 21 pages read; two publisher links have identical SHA-256.

**Version relation:** Includes both submissions, version 0/1 reports, Legg rebuttal and Microsoft rebuttal. Review labels are not arXiv revision labels and the file is not a substitute for the final reply.

### V6: Microsoft final Nature reply (24 June 2026)

[Public source](https://www.nature.com/articles/s41586-026-10568-7) · [MR2026:reply](proof-sources.md#source-mr2026-reply).

**Access:** Publisher preview, references, data statement and update checked; exact complete final text not retrieved.

**Version relation:** No public manuscript was verified as word-for-word identical to Nature 654, E27–E28. Keep this narrow version-comparison gate open.

## Issue-by-issue authoring decisions

The “assessment” entries are bounded editorial reasoning from the accessed sources. They separate acknowledged processing facts, competing physical interpretations and tests still required. They do not certify the correctness of either side’s device model. Numbered reviewer positions below are attributed to the **Anonymous Referees** in the public joint review file and its stated review version.

### D1: Bias-coordinate antisymmetrisation and a single-pixel shift

**Exact targets:** [LEGNOTES:protocol](proof-sources.md#source-legnotes-protocol), [MSPRE:readout](proof-sources.md#source-mspre-readout), [TPREVIEW:microsoft](proof-sources.md#source-tpreview-microsoft).

**Comment / challenge:** Legg identifies array reversal on a bias grid not symmetric about zero; dropping one endpoint changes extracted maps.

**Response / qualification:** Microsoft acknowledges asymmetric cropping. Its 2026 rebuttal describes a single bias-pixel shift, not an analogous magnetic-field shift.

**Editorial assessment:** The coordinate condition is mathematically checkable: reversing indices represents V to -V only on an antisymmetric coordinate grid. The two sides disagree about the physical and cluster-level consequences, not the existence of the cropping problem.

**Required before authoring acceptance:** Show the actual bias coordinates, units and zero calibration; keep cropping, interpolation and plotting changes separate. Report per-pixel and cluster changes. A synthetic counterexample verifies the coordinate issue, not the published device maps.

**Status:** Acknowledged processing issue; device-map effect not independently recomputed.

### D2: Existing clusters, per-cutter subregions and displayed regions

**Exact targets:** [LEGGAAM:argument](proof-sources.md#source-leggaam-argument), [LEGNOTES:protocol](proof-sources.md#source-legnotes-protocol), [MSPRE:readout](proof-sources.md#source-mspre-readout), [TPREVIEW:microsoft](proof-sources.md#source-tpreview-microsoft).

**Comment / challenge:** The displayed single cluster omitted other candidate regions and limited the scope of readout comparisons.

**Response / qualification:** The 2026 Microsoft rebuttal says three ROI2s existed before and after correction; one grew after a per-cutter SOI2 changed, and the plot highlighted the readout ROI only. It also narrows its earlier statement to the fixed-field readout slice.

**Editorial assessment:** A new displayed region, a newly merged per-cutter SOI2 and a newly created multi-cutter ROI2 are different claims. The final rebuttal is more specific than the 2025 response; do not merge their wording into one conclusion.

**Required before authoring acceptance:** Track every ROI/SOI label before/after correction, each cutter and the fixed-field slice. Publish an explicit distinction between changes to classifications and changes to what a plot highlights.

**Status:** Argument compared; empirical resolution pending.

### D3: Window and cutter sensitivity versus a statistical classifier

**Exact targets:** [LEGGPRE:argument](proof-sources.md#source-leggpre-argument), [LEGNOTES:protocol](proof-sources.md#source-legnotes-protocol), [MSPRE:statistics](proof-sources.md#source-mspre-statistics).

**Comment / challenge:** The same neighborhood can be labelled differently when the field window or cutter changes, undermining a unique gap diagnosis.

**Response / qualification:** Microsoft treats TGP as model-calibrated tune-up with possible false negatives; its simulated statistics are intended to bound false discoveries rather than guarantee identical masks.

**Editorial assessment:** A changed threshold mask alone proves neither that a device became physically gapless nor that false discoveries remain small. Changing a cutter can also change the physical contact configuration. The comparison must separate classifier sensitivity from model validity.

**Required before authoring acceptance:** Predefine parameter windows and contact settings; sweep thresholds and label stability on fixed data, then separately test the false-discovery claim on independently validated ensembles.

**Status:** Argument compared; empirical resolution pending.

### D4: False discovery, false positive rate and the operating-point claim

**Exact targets:** [MSPRE:statistics](proof-sources.md#source-mspre-statistics), [TPREVIEW:microsoft](proof-sources.md#source-tpreview-microsoft).

**Comment / challenge:** Legg challenges how protocol sensitivity and definitions of an accepted region affect reliability.

**Response / qualification:** The 2025 response defends a small simulation-conditioned false-discovery bound and allows missed regions; its quoted transfer condition assumes simulated and real data share the relevant distribution.

**Editorial assessment:** FDR = FP/(TP+FP) differs from FPR = FP/(FP+TN). A low simulated FDR is not a model-independent probability for one real device or every pixel in an accepted region. ROI-level existence of a qualifying pixel does not certify a chosen readout point.

**Required before authoring acceptance:** Specify population, label definition, numerator/denominator, confidence method, device/disorder sampling and out-of-distribution limits. Do not silently replace “some qualifying point in a region” with “the measured point is topological”.

**Status:** Argument compared; empirical resolution pending.

### D5: Which gap, and which measurement configuration?

**Exact targets:** [LEGGAAM:argument](proof-sources.md#source-leggaam-argument), [MSPRE:readout](proof-sources.md#source-mspre-readout), [MS2025SI:configuration](proof-sources.md#source-ms2025si-configuration), [TPREVIEW:microsoft](proof-sources.md#source-tpreview-microsoft).

**Comment / challenge:** Legg reads structured low-bias transport as evidence against a robust superconducting gap and questions the use of an Andreev-enhanced regime.

**Response / qualification:** Microsoft invokes coupling-dependent local conductance and finite-wire transmission. The original supplement documents a transition from transport to isolated-dot readout, including changed gates and cross-capacitance/hysteresis shifts.

**Editorial assessment:** A parent-superconductor gap, induced spectral gap, threshold-defined transport gap and isolation of a readout mode are not interchangeable. Finite subgap conductance is not by itself a density-of-states measurement outside its stated tunnelling assumptions.

**Required before authoring acceptance:** Record gate values and mappings between configurations. State the energy quantity inferred at every step, lead coupling, temperature and voltage-divider assumptions; compare device-specific alternatives rather than generic signatures.

**Status:** Argument compared; empirical resolution pending.

### D6: Particle-hole symmetry and negative differential conductance

**Exact targets:** [LEGNOTES:symmetry](proof-sources.md#source-legnotes-symmetry), [TPREVIEW:legg](proof-sources.md#source-tpreview-legg), [MSPRE:readout](proof-sources.md#source-mspre-readout), [DANON:symmetry](proof-sources.md#source-danon-symmetry).

**Comment / challenge:** The revised comment tests a relation between antisymmetric local and nonlocal conductances and presents negative local conductance as a possible quantum-dot signature.

**Response / qualification:** Microsoft notes that a three-terminal device can have odd local and even nonlocal conductance without violating the relevant symmetry.

**Editorial assessment:** Danon Eq. (7)–(8) relates a sum of conductances under explicit subgap, grounded-terminal and bias-independent-scattering assumptions. It does not require every element to be even. Violations require checking those assumptions, signs, voltages and device configuration; negative differential conductance is not a unique microscopic diagnosis.

**Required before authoring acceptance:** Import the exact conductance relation with its current directions and voltage arguments. Distinguish Bogoliubov particle-hole redundancy from observed bias symmetry. Test complete matrix relations and nuisance mechanisms before assigning an alternative device explanation.

**Status:** Argument compared; empirical resolution pending.

### D7: Capacitance contrast and the four-Majorana alternative model

**Exact targets:** [MSPRE:readout](proof-sources.md#source-mspre-readout), [MR2026:reply](proof-sources.md#source-mr2026-reply), [MS2025SI:quasi](proof-sources.md#source-ms2025si-quasi).

**Comment / challenge:** Legg questions whether transport establishes the prerequisites for the interpreted parity signal; the accepted comment does not directly fit or refute the capacitance trace.

**Response / qualification:** Microsoft argues that extra thermally accessible modes reduce contrast. S2.7 supplies a four-Majorana model, perturbative and numerical analysis, and a constraint on equilibration and slow switching.

**Editorial assessment:** The supplement is substantive model evidence: its assumptions include intra-parity equilibration faster than measurement/switching and specified couplings/noise. It is not an unrestricted theorem excluding every trivial interacting or nonequilibrium device model, nor a direct measurement of topological protection.

**Required before authoring acceptance:** List the Hamiltonian, parity sectors, drive, thermal/noise assumptions and quantitative observations being fitted. Reproduce model-specific contrast and switching predictions before judging whether a proposed alternative explains the same data.

**Status:** Argument compared; empirical resolution pending.

### D8: Evidence hierarchy, controls and non-TGP regions

**Exact targets:** [LEGGAAM:argument](proof-sources.md#source-leggaam-argument), [TPREVIEW:legg](proof-sources.md#source-tpreview-legg), [TPREVIEW:revised-assessments](proof-sources.md#source-tpreview-revised-assessments), [TPREVIEW:microsoft](proof-sources.md#source-tpreview-microsoft), [MS2025SI:configuration](proof-sources.md#source-ms2025si-configuration).

**Comment / challenge:** Legg and Anonymous Referee 2 question circular support between tune-up and readout interpretation and ask for broader controls.

**Response / qualification:** Microsoft treats readout as additional evidence and states in the later rebuttal that some non-TGP readouts were performed, without claiming an exhaustive scan.

**Editorial assessment:** Mutual consistency is not automatically independent validation; conversely a model that predicts a new observable can add evidence without a logical circle. The review record does not justify saying that no non-TGP controls were ever taken. No self-consistent alternative quantitative fit is supplied by the accepted comment.

**Required before authoring acceptance:** Draw an assumption/data/inference graph; identify reused data, independent predictions and held-out controls. Pin the actual control configurations and outcomes rather than infer their absence or completeness from a reviewer request.

**Status:** Argument compared; empirical resolution pending.

### D9: Version drift and non-unanimous peer review

**Exact targets:** [LEGGAAM:argument](proof-sources.md#source-leggaam-argument), [LEGNOTES:protocol](proof-sources.md#source-legnotes-protocol), [TPREVIEW:referees](proof-sources.md#source-tpreview-referees), [TPREVIEW:revised-assessments](proof-sources.md#source-tpreview-revised-assessments), [TPREVIEW:microsoft](proof-sources.md#source-tpreview-microsoft).

**Comment / challenge:** The accepted comment narrows its stated task to transport evidence and moves some detail to the supplement while retaining concerns about significant disorder and a poorly defined gap.

**Response / qualification:** Microsoft’s rebuttal characterizes some claims as removed. Anonymous Referee 1 finds the revised reply convincing; Referee 2 retains concerns; Referee 3 remains unconvinced that the critique supplies a quantitative alternative.

**Editorial assessment:** Do not treat an author’s summary of the other text as its exact contents. Check the accepted text and supplement directly. Publication of both pieces and disagreement among referees do not resolve the device physics.

**Required before authoring acceptance:** Preserve version-specific citations and attribute reviewer judgments to the numbered Anonymous Referee and review version. Compare the exact final journal reply when available; do not present the 2025 preprint or 2026 rebuttal as that final text.

**Status:** Argument compared; empirical resolution pending.

## Frozen data and analysis versions

A dataset-family DOI and a specific version are different identifiers. Publisher checksums below come from the versioned file listings; they are not claimed as hashes of archives successfully downloaded in this pass.

- **[Original transport data](https://zenodo.org/records/14804380):** 1.0; published 4 February 2025; `tgp2_tuneup.zip`. Publisher MD5: `52e10ebaa6a76d6d8b60785cca5be91f`. Version page and file listing checked; binary download returned HTTP 403; archive not reanalysed.

- **[Corrected transport data](https://zenodo.org/records/21847809):** v2; published 8 August 2026; record created 10 August 2026; `tgp2_tuneup.zip`. Publisher MD5: `be4a40667fde91284bcec41a2bedabd6`. Version page/file listing checked; binary download returned HTTP 403. Publisher reports 4.6% classification changes; this number was not independently recomputed.

- **[Original comment notebook](https://zenodo.org/records/15008728):** 0; published 13 March 2025; `Comment_figs.ipynb`. Publisher MD5: `1a97d6cb34beb0ae2bb75c998c3efeee`. Version page/file listing checked; not run.

- **[Updated comment notebooks](https://zenodo.org/records/16732479):** v2; published 3 August 2025; `comment_figures.py and three device notebooks`. Publisher MD5: `64c2749f7cd9895451033565223adae2 (comment_figures.py)`. Version page/file listing checked; not run. Do not assume automatic identity with every final 2026 figure.

The older Microsoft response reports changes below 5 microelectronvolts for more than 96% of pixels. The later dataset description reports 4.6% of pixels changing classification. These measure different quantities and use different versions; neither percentage certifies small changes to connectivity or selected clusters.

## Limited independent logic checks

The [verification tool](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/scripts/verify_topology_logic.py) checks five synthetic counterexamples/invariants with the Python standard library: bias-coordinate reflection, range-normalised threshold changes at a fixed point, FDR versus FPR, region-existence versus pointwise certification, and pairwise conductance symmetry versus an even local trace. The conductance example checks the algebraic implication only, under the separately imported physical assumptions from Danon Eq. (1)–(8). It is not a fitted device signal.

Run `python3 scripts/verify_topology_logic.py` from the repository root. [Machine-readable results](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/verification/topology-logic.json) record all five checks. No device data are loaded and no measured percentage, TGP map, RF fit or topological phase is reproduced.

## Remaining acceptance gates

- The accessible argument corpus has been read: two full 2025 preprints, Legg’s full 2026 accepted manuscript and supplement, and the complete 21-page joint review file. Keep final-journal-reply text comparison separate and open.
- Reacquire the exact original and corrected transport archives and match their publisher checksums before re-running the published workflows. Resolve data/code version selection, complete ROI/SOI identity maps and numerical differences; the present pass does not reproduce the 4.6% dataset claim.
- Verify the empirical model-transfer assumptions behind FDR estimates and identify the precise readout operating point within the selected region; source reading and synthetic checks do not establish a device probability.
- Independently review the three-terminal symmetry assumptions and the capacitance/quasi-Majorana model, including configuration changes, temperatures, equilibration and nuisance mechanisms. No side’s interpretation or a reviewer vote is accepted as proof of topology.
- Before chapter drafting, obtain specialist assessment of the bounded evidence claims. Preserve the no-body-writing architecture gate and record reader/proof/API acceptance separately.
