#!/usr/bin/env python3
"""Complex arithmetic checked against independent integer-pair arithmetic.

Python 3.12, standard library only. No quantum-state or device execution.
"""
import math


def pair_add(z, w):
    return z[0] + w[0], z[1] + w[1]


def pair_mul(z, w):
    a, b = z
    c, d = w
    return a*c - b*d, a*d + b*c


def pair_conj(z):
    return z[0], -z[1]


def pair_mod2(z):
    return z[0]**2 + z[1]**2


def as_complex(z):
    return complex(z[0], z[1])


def conjugate_vector(vector):
    return [z.conjugate() for z in vector]


def scale(scalar, vector):
    return [scalar*z for z in vector]


def add_vectors(v, w):
    if len(v) != len(w):
        raise ValueError("Coordinate lengths must match")
    return [a+b for a, b in zip(v, w)]


def squared_length(vector):
    terms = [z.conjugate()*z for z in vector]
    assert all(math.isclose(term.imag, 0.0, rel_tol=0.0, abs_tol=1e-12)
               for term in terms)
    return sum(term.real for term in terms)


def main():
    # Finite exact integer checks are implementation evidence, not general proofs.
    pairs = [(a, b) for a in range(-2, 3) for b in range(-2, 3)]
    for p in pairs:
        z = as_complex(p)
        assert z.conjugate() == as_complex(pair_conj(p))
        assert z.conjugate().conjugate() == z
        assert z.conjugate()*z == pair_mod2(p)
        for q in pairs:
            w = as_complex(q)
            assert z+w == as_complex(pair_add(p, q))
            assert z*w == as_complex(pair_mul(p, q))
            assert (z+w).conjugate() == z.conjugate()+w.conjugate()
            assert (z*w).conjugate() == z.conjugate()*w.conjugate()
            assert pair_mod2(pair_mul(p, q)) == pair_mod2(p)*pair_mod2(q)
    z, w = 2-3j, -1+4j
    assert z*w == 10+11j
    assert (z.conjugate()*z).real == 13
    assert (w.conjugate()*w).real == 17
    assert ((z+w).conjugate()*(z+w)).real == 2
    v = [1+1j, 2-1j]
    other = [-1+2j, 3+0j]
    assert add_vectors(v, other) == [3j, 5-1j]
    assert conjugate_vector(add_vectors(v, other)) == add_vectors(
        conjugate_vector(v), conjugate_vector(other))
    try:
        add_vectors(v, [0j])
    except ValueError:
        pass
    else:
        raise AssertionError("Unequal coordinate lengths were silently accepted")
    assert squared_length(v) == 7
    assert sum(item**2 for item in v) == 3-2j  # Deliberately wrong length rule.
    assert conjugate_vector(scale(1j, v)) == [-1-1j, 1-2j]
    assert conjugate_vector(scale(1j, v)) != scale(1j, conjugate_vector(v))
    assert conjugate_vector(scale(2-1j, v)) == scale(2+1j, conjugate_vector(v))
    assert squared_length(scale(2-1j, v)) == 5*7
    u = scale(1/math.sqrt(7), v)
    assert math.isclose(squared_length(u), 1.0, rel_tol=0.0, abs_tol=1e-12)
    assert squared_length([0j, 0j]) == 0
    print("z=2-3j, w=-1+4j: z*w=10+11j; squared moduli=13,17")
    print("Squared modulus of z+w: 2; sum of squared moduli: 30 (not additive)")
    print("v=[1+1j, 2-1j]: squared length=7; sum of squares=3-2j (wrong rule)")
    print("conjugate(i*v)=[-1-1j, 1-2j]; keeping i unchanged fails")
    print(f"After dividing v by sqrt(7): squared length={squared_length(u):.12f}")
    print("25 scalars / 625 ordered pairs checked against integer-coordinate arithmetic.")
    print("Conjugation, product modulus, vector scaling, and zero-vector checks passed.")


if __name__ == "__main__":
    main()
