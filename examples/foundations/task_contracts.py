"""Section 1.1: exact task checks, with no quantum backend or random sampling.

Python 3.12 reference; standard library only. The eight-shot fixture is synthetic.
Enumeration is a small-model verifier, not an efficient estimation algorithm.
"""
from fractions import Fraction
from itertools import product
from math import comb


def check_bits(bits):
    if not bits or any(type(bit) is not int or bit not in (0, 1) for bit in bits):
        raise ValueError("Expected a nonempty sequence of integer bits.")


def parity(bits):
    """Toggle the answer for each 1; an even number of toggles returns 0."""
    check_bits(bits)
    answer = 0
    for bit in bits:
        if bit == 1:
            answer = 1 - answer
    return answer


def mean_score(bits):
    check_bits(bits)
    return Fraction(sum(1 - 2 * bit for bit in bits), len(bits))


def within_tolerance(value, target, epsilon):
    # A string of samples is not a numerical estimate.
    if not isinstance(value, (int, float, Fraction)) or isinstance(value, bool):
        return False
    return abs(value - target) <= epsilon


def main():
    bits = [1, 0, 1, 1]
    assert parity(bits) == sum(bits) % 2 == 1
    # A second calculation checks every four-bit input, not just the worked case.
    for candidate in product((0, 1), repeat=4):
        assert parity(candidate) == sum(candidate) % 2

    shots = [0, 1, 1, 0, 1, 0, 1, 1]  # Fixed teaching data, not a random draw.
    n = len(shots)
    estimate = mean_score(shots)
    assert estimate == Fraction(shots.count(0) - shots.count(1), n)
    assert estimate == Fraction(-1, 4)
    p0, p1 = Fraction(1, 4), Fraction(3, 4)
    target = p0 - p1
    epsilon, delta = Fraction(1, 4), Fraction(1, 4)
    assert within_tolerance(estimate, target, epsilon)
    assert not within_tolerance("01101011", target, epsilon)
    assert not within_tolerance(Fraction(1), target, epsilon)
    for invalid in ([], [0, 2]):
        try:
            mean_score(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid samples were accepted.")

    # Assume independent repeats with the supplied probabilities. Give each
    # sequence its probability, rather than treating all sequences as equally likely.
    total_mass = Fraction(0)
    success_mass = Fraction(0)
    for sequence in product((0, 1), repeat=n):
        weight = Fraction(1)
        for bit in sequence:
            weight *= p0 if bit == 0 else p1
        total_mass += weight
        if within_tolerance(mean_score(sequence), target, epsilon):
            success_mass += weight
    assert total_mass == 1
    # Independent grouping check: exactly k zero outcomes gives mean 2*k/n - 1.
    # For n=8, target=-1/2 and epsilon=1/4, success means k is 1, 2 or 3.
    grouped_mass = sum(
        (comb(n, k) * p0**k * p1**(n-k) for k in (1, 2, 3)), Fraction(0)
    )
    assert success_mass == grouped_mass == Fraction(12879, 16384)
    assert success_mass >= 1 - delta
    # A possible, rare sequence still fails: probability guarantees allow failures.
    assert not within_tolerance(mean_score([0] * n), target, epsilon)

    print(f"Parity of 1011: {parity(bits)}")
    print(f"Fixture: N={n}, zeros={shots.count(0)}, ones={shots.count(1)}")
    print(f"Estimate: {estimate}; reference mean: {target}; tolerance: {epsilon}")
    print(f"Model success probability: {success_mass} = {float(success_mass):.9f}")
    print(f"Required success probability: {1-delta}")
    print("Enumeration, grouped reference, and contract failure checks passed.")


if __name__ == "__main__":
    main()
