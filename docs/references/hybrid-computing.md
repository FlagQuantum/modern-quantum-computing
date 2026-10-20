# Source anchors for quantum-classical hybrid computing

The subsequent [all-section proof/source plan](../proof-plan.md) and [version-specific source catalogue](proof-sources.md) supply exact source targets. The scoping notes below retain their original review scope; locator assignment is not proof approval.

**Scoping date: October 20, 2026.** These notes support the author's [eight-pattern teaching map](../hybrid-computing.md). The grouping is editorial and composable; the papers do not establish a unique eight-way taxonomy.

This scoping pass checked bibliographic/abstract information and official runtime documentation. Exact method-specific results, assumptions, code contracts and proof locators remain to be reviewed before chapter drafting.

| Pattern or distinction | Primary research or official documentation | Intended use |
|---|---|---|
| Variational outer loop | [Peruzzo et al., A variational eigenvalue solver on a quantum processor](https://arxiv.org/abs/1304.3061) | Quantum measurement combined with a classical parameter optimizer |
| Fixed kernels versus variational learning | [Schuld and Killoran, Quantum machine learning in feature Hilbert spaces](https://arxiv.org/abs/1803.07128) | State-encoded features, quantum kernel estimation and variational model distinctions |
| In-execution feedback | [IBM: classical feedforward and control flow](https://quantum.cloud.ibm.com/docs/en/guides/classical-feedforward-and-control-flow) | Mid-circuit measurement, supported classical control and explicit hardware limitations |
| Host-driven hybrid jobs | [Amazon Braket Hybrid Jobs](https://docs.aws.amazon.com/braket/latest/developerguide/braket-jobs.html) | A concrete official example of classical/quantum job orchestration; not a universal controller interface |
| Fragment reconstruction | [Peng et al., Simulating Large Quantum Circuits on a Small Quantum Computer](https://arxiv.org/abs/1904.00102) | Cluster/fragment execution with classical recombination and explicit overhead |
| An alternative cutting method | [Perlin et al., Quantum Circuit Cutting with Maximum Likelihood Tomography](https://arxiv.org/abs/2005.12702) | A distinct reconstruction approach to evaluate under its own assumptions |
| Embedding foundations | [Knizia and Chan, Density matrix embedding](https://arxiv.org/abs/1204.5783) | The classical embedding construction; this reference alone does not make it a QPU algorithm |
| A quantum embedding solver | [Mineh and Montanaro, Solving the Hubbard model using DMET and VQE](https://arxiv.org/abs/2108.08611) | A specified quantum-solver/embedding combination and nested approximation/convergence questions |
| Quantum sampling with classical diagonalization | [Robledo-Moreno et al., Chemistry Beyond the Scale of Exact Diagonalization on a Quantum-Centric Supercomputer](https://arxiv.org/abs/2405.05068) | A concrete sampled-configuration/classical-solve workflow; performance conclusions need claim-specific review |

The textbook's existing H2 code remains tied to [O'Malley et al. corrected v2](https://arxiv.org/abs/1512.06860v2); no new primary work is claimed reproduced by adding these source anchors. Official documentation features and restrictions can change, so an implementation chapter must record versions and validate the selected backend rather than infer FlagQuantum support from another framework.
