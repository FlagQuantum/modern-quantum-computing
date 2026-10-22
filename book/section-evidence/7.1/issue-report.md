A nonzero tiny Ry is dropped in CPU complex128 statevector execution even with `allow_approximate=False`. This was encountered while validating a textbook pure-state entanglement example; it is distinct from an approximate rank test.

Environment: FlagQuantum 0.3.1, PyTorch 2.13.0, Python 3.12.14, CPU.

```python
import math
import torch
import flagquantum as fq
options = fq.ExecutionOptions(mode='statevector', backend='pytorch', device='cpu',
    precision='complex128', allow_approximate=False, allow_backend_fallback=False)
for epsilon in (1e-10, 1e-12, 1e-13, 1e-14):
    c = fq.Circuit(2, dtype=torch.complex128)
    c.ry(0, 2*math.asin(epsilon)).cx(0, 1)
    result = fq.run(c, outputs=[fq.probabilities()], options=options)
    print(epsilon, result.statevector()[0].tolist())
```

Observed final |11> amplitude: 1e-10 for the first input, exactly zero for all three smaller inputs. Expected amplitude is epsilon for each. The smallest amplitudes are representable in complex128; this is not underflow. The resulting pure coefficient determinant is changed from nonzero to zero. Replacing Ry by its explicit 2x2 unitary also produced zero in a separate one-circuit probe.

Inspection of the installed `compiler/pipeline.py` found `_is_zero(value, atol=1e-12)` and its use to remove parameterized gates. This is a suspected contributing path, not a complete root-cause attribution. Please preserve nonzero rotations for exact execution, or make the numerical simplification policy explicit and controllable. Regression checks should inspect the tiny amplitude directly (ordinary allclose with atol1e-12 can hide this).

The textbook retains the failed candidate/probes and uses epsilon1e-10 for the runnable native near-product illustration. This does not claim a library fix.
