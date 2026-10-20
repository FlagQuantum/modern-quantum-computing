"""Section 1.5: a hypothetical cost ledger, not a measured benchmark.

Python 3.12 standard library only. No solver, quantum simulator or device is run.
Accuracy/success targets are requirements; this program does not establish them.
All component costs below are invented microseconds for the same task instance.
"""
from fractions import Fraction

CLASSICAL = {"input": 2000, "compute": 7000, "output": 1000}
QUANTUM = {"input": 4000, "prepare_per_shot": 20,
           "execute_per_shot": 10, "read_per_shot": 20, "postprocess": 2000}


def quantum_total(shots):
    return QUANTUM["input"] + shots * (
        QUANTUM["prepare_per_shot"] + QUANTUM["execute_per_shot"] + QUANTUM["read_per_shot"]
    ) + QUANTUM["postprocess"]


def main():
    shots = 100  # An illustrative cost assumption, not a derived sufficient shot count.
    classical = sum(CLASSICAL.values())
    quantum = quantum_total(shots)
    # Independently expand the ledger rather than trusting a displayed ratio.
    assert classical == 2000 + 7000 + 1000 == 10000
    assert quantum == 4000 + 100*20 + 100*10 + 100*20 + 2000 == 11000
    kernel_ratio = Fraction(CLASSICAL["compute"], shots * QUANTUM["execute_per_shot"])
    full_ratio = Fraction(classical, quantum)
    omitted_input = quantum - QUANTUM["input"]
    wrong_ratio = Fraction(classical, omitted_input)
    assert kernel_ratio == 7 and full_ratio == Fraction(10, 11) < 1
    assert omitted_input == 7000 and wrong_ratio == Fraction(10, 7) > 1
    # Sensitivity at unchanged per-shot prices. This does not infer an accuracy law.
    more_shots = quantum_total(200)
    assert more_shots == 16000 and more_shots - quantum == 100*(20+10+20)
    print("Hypothetical costs only; no performance or accuracy experiment was run.")
    print("Shared target: absolute error <= 1/20, success probability >= 19/20 (not verified here).")
    print(f"Classical total: {classical} us = {classical/1000:.3f} ms")
    print(f"Quantum total, N={shots}: {quantum} us = {quantum/1000:.3f} ms")
    print(f"Compute-only ratio C/Q: {kernel_ratio} = {float(kernel_ratio):.6f}")
    print(f"End-to-end ratio C/Q: {full_ratio} = {float(full_ratio):.6f}")
    print(f"If quantum input cost is omitted: {omitted_input} us; misleading ratio C/Q={wrong_ratio}")
    print(f"At N=200: quantum total={more_shots} us (accuracy implications not inferred).")
    print("Expanded sums, units, and omitted-cost counterexample checks passed.")


if __name__ == "__main__":
    main()
