# Measurement and expectation values

**Starter draft · FlagQuantum 0.3.1 · CPU · complex128**

## Question and derivation

What does measuring $Z$ tell us about a rotated qubit? Prepare $\lvert0\rangle$ and apply

$$
R_Y(\phi)=\begin{pmatrix}\cos(\phi/2)&-\sin(\phi/2)\\\sin(\phi/2)&\cos(\phi/2)\end{pmatrix}.
$$

Matrix multiplication gives $\lvert\psi\rangle=\cos(\phi/2)\lvert0\rangle+\sin(\phi/2)\lvert1\rangle$. Squaring amplitude magnitudes gives the probabilities. Since $Z=\mathrm{diag}(1,-1)$, the expectation is their difference.

| Formula | Implementation in `examples/measurement.py` |
|---|---|
| $\lvert\psi\rangle=R_Y(\phi)\lvert0\rangle$ | `fq.Circuit(1, dtype=torch.complex128).ry(0, phi)` |
| $P(0)=\cos^2(\phi/2)$ | `torch.cos(phi/2)**2` |
| $P(1)=\sin^2(\phi/2)$ | `torch.sin(phi/2)**2` |
| $\langle Z\rangle=P(0)-P(1)=\cos\phi$ | `result.expectation("z").squeeze(0)`; compare with `torch.cos(phi)` |

## Run and verify

After installing the pinned example requirements, run from the repository root:

```bash
python examples/measurement.py
```

Expected output:

```text
P(0) = 0.912667807
P(1) = 0.087332193
<Z>  = 0.825335615
Analytic and FlagQuantum results agree.
```

[Read the complete program](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/examples/measurement.py). It checks both individual probabilities, the closed-form expectation, and the probability difference with explicit tolerances.

## Exercises and limits

1. Predict the results at $\phi=0,\pi/2,\pi$ before running them.
2. Replace $R_Y$ by $R_Z$ on the initial state. Explain why the probabilities stay unchanged.
3. Derive the variance $\mathrm{Var}(Z)=1-\langle Z\rangle^2$ and the standard error for independent shots.

This program evaluates exact ideal-state probabilities and expectations. It does not generate finite-shot measurements or model noise.

## Further reading

Read NC Chapter 2 or Preskill Chapter 3, *Measurement and Evolution* (July 2015), as listed in the [reading guide](../references/reading-guide.md). These are optional companion readings; the derivation above is self-contained.
