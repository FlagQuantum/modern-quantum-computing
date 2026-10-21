#!/usr/bin/env python3
"""Bounded state/unitary comparison, contract 0.1.0; Python standard library only."""
import json
import math
import sys

VERSION = '0.1.0'
VALIDATION_ATOL = 1e-12


class Invalid(ValueError):
    pass


class Unsupported(ValueError):
    pass


def number(x):
    if type(x) not in (int, float):
        raise Invalid('Expected real JSON numbers, not strings or booleans')
    try:
        x = float(x)
    except OverflowError as exc:
        raise Invalid('Number exceeds binary64 range') from exc
    if not math.isfinite(x) or abs(x) > 2:
        raise Invalid('Coordinates must be finite with real/imaginary parts at most 2')
    return x


def scalar(x):
    if not isinstance(x, list) or len(x) != 2:
        raise Invalid('Complex entries must be [real, imaginary] pairs')
    return complex(number(x[0]), number(x[1]))


def norm(xs):
    return math.sqrt(math.fsum(abs(x)**2 for x in xs))


def overlap(a, b):
    terms = [x.conjugate()*y for x, y in zip(a, b)]
    return complex(math.fsum(x.real for x in terms), math.fsum(x.imag for x in terms))


def array(data, kind):
    if not isinstance(data, list) or len(data) not in (2, 4):
        raise Invalid('Only dimension 2 or 4 is supported')
    d = len(data)
    if kind == 'state':
        out = [scalar(x) for x in data]
        if abs(norm(out)**2-1) > VALIDATION_ATOL:
            raise Invalid('State must already have unit squared norm within 1e-12')
        return out, d
    if any(not isinstance(row, list) or len(row) != d for row in data):
        raise Invalid('Unitary must be square with dimension 2 or 4')
    out = [scalar(x) for row in data for x in row]
    for j in range(d):
        for k in range(d):
            gram = overlap(out[j::d], out[k::d])
            if abs(gram-(1 if j == k else 0)) > VALIDATION_ATOL:
                raise Invalid('Matrix must already be unitary: entrywise U†U tolerance 1e-12')
    return out, d


def controlled(u):
    # Target dimension 2; basis 00,01,10,11 with control first.
    return [complex((j == k) if j < 2 and k < 2 else 0) if j < 2 or k < 2
            else u[2*(j-2)+(k-2)] for j in range(4) for k in range(4)]


def compare(request):
    """No normalization, basis guessing, per-column phases or implicit context."""
    try:
        if not isinstance(request, dict):
            raise Invalid('Request must be an object')
        required = {'kind', 'mode', 'basis_a', 'basis_b', 'a', 'b'}
        if set(request)-required-{'atol'} or not required <= set(request):
            raise Invalid('Required keys: kind, mode, basis_a, basis_b, a, b; optional atol only')
        kind, mode = request['kind'], request['mode']
        if kind not in ('state', 'unitary'):
            raise Unsupported('Only pure statevectors and square unitaries; no density/channel/shot profile')
        if mode not in ('coordinates', 'global-phase', 'controlled'):
            raise Invalid('Choose coordinates, global-phase or controlled explicitly')
        if mode == 'controlled' and kind != 'unitary':
            raise Invalid('Controlled mode requires a target unitary')
        atol = request.get('atol', 1e-10)
        if type(atol) not in (int, float) or not 1e-14 <= atol <= 1e-6:
            raise Invalid('Comparison atol must be a finite absolute number in [1e-14,1e-6]')
        a, d = array(request['a'], kind)
        b, e = array(request['b'], kind)
        if d != e:
            raise Invalid('Input dimensions differ')
        basis = ['0', '1'] if d == 2 else ['00', '01', '10', '11']
        if request['basis_a'] != basis or request['basis_b'] != basis:
            raise Unsupported('Canonical computational basis required for both inputs; transform explicitly first')
        if mode == 'controlled':
            if d != 2:
                raise Unsupported('Controlled profile supports one control and a dimension-2 target only')
            a, b = controlled(a), controlled(b)
        c = overlap(a, b)
        phase_defined = abs(c) != 0
        z = c.conjugate()/abs(c) if phase_defined else 1+0j
        raw = norm([x-y for x, y in zip(a, b)])
        aligned = norm([x-z*y for x, y in zip(a, b)])
        residual = raw if mode == 'coordinates' else aligned
        return {
            'contract_version': VERSION,
            'status': 'within_tolerance' if residual <= atol else 'outside_tolerance',
            'kind': kind, 'mode': mode, 'input_dimension': d,
            'comparison_dimension': 4 if mode == 'controlled' else d,
            'metric': 'euclidean' if kind == 'state' else 'frobenius',
            'raw_residual': raw, 'aligned_residual': aligned,
            'decision_residual': residual, 'absolute_tolerance': atol,
            'alignment_multiplier_on_b': [z.real, z.imag],
            'overlap': [c.real, c.imag],
            'phase_identifiable': phase_defined,
            'validation_atol': VALIDATION_ATOL,
            'phase_scope': 'retained' if mode == 'coordinates' else
                ('one phase on the full controlled operation' if mode == 'controlled' else 'one phase on the whole object'),
            'proof_of_exact_equality': False,
        }
    except (Invalid, Unsupported) as exc:
        return {'contract_version': VERSION,
                'status': 'unsupported' if isinstance(exc, Unsupported) else 'invalid_input',
                'reason': str(exc)}


def reject_constant(value):
    raise Invalid('Nonstandard JSON constant: '+value)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Invalid('Duplicate JSON key: '+key)
        result[key] = value
    return result


def main():
    try:
        result = compare(json.load(sys.stdin, parse_constant=reject_constant, object_pairs_hook=unique_object))
    except (Invalid, ValueError, OverflowError, RecursionError) as exc:
        result = {'contract_version': VERSION, 'status': 'invalid_input', 'reason': str(exc)}
    print(json.dumps(result, allow_nan=False, sort_keys=True))
    return {'within_tolerance': 0, 'outside_tolerance': 1, 'invalid_input': 2, 'unsupported': 3}[result['status']]


if __name__ == '__main__':
    sys.exit(main())
