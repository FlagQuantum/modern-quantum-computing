"""Section 5.3: finite Boolean XOR embeddings and explicit clean-workspace logic."""
from itertools import product
from importlib.metadata import version
from math import sqrt
import cmath
import torch
import flagquantum as fq
try:
    from examples.foundations.circuit_composition import execute, product_input
except ModuleNotFoundError:
    from circuit_composition import execute, product_input
DTYPE = torch.complex128
ATOL = 1e-12
RUNS = 0


def validate_table(table, n, m):
    # This dense teaching constructor is explicitly bounded, not a synthesis API.
    if type(n) is not int or type(m) is not int or n < 1 or m < 1 or n+m > 6:
        raise ValueError('Book helper requires positive integer widths with n+m<=6')
    if not isinstance(table, (list, tuple)) or len(table) != 2**n:
        raise ValueError('One declared integer output per input basis label required')
    if any(type(v) is not int or not 0 <= v < 2**m for v in table):
        raise ValueError('Outputs must be literal integers in the m-bit range')
    return tuple(table)


def oracle_matrix(table, n, m):
    table = validate_table(table, n, m)
    U = torch.zeros((2**(n+m),)*2, dtype=DTYPE)
    for x in range(2**n):
        for y in range(2**m):
            U[(x << m) | (y ^ table[x]), (x << m) | y] = 1
    return U


def oracle_reference(v, table, n, m):
    table = validate_table(table, n, m)
    if v.shape != (2**(n+m),):
        raise ValueError('Reference vector width does not match declared registers')
    # Pull each output coefficient from its unique inverse input, rather than a matrix product.
    return torch.tensor([v[(x << m) | (y ^ table[x])].item()
                         for x in range(2**n) for y in range(2**m)], dtype=DTYPE)


def run(block, factors):
    global RUNS
    v, p = execute(block, factors)
    RUNS += 1
    return v, p


def basis_factors(bits):
    return [(1,0) if b == 0 else (0,1) for b in bits]


def complex_factors(n):
    return [(.6,.8j) if q % 2 == 0 else (sqrt(.7), cmath.exp(.2j)*sqrt(.3)) for q in range(n)]


def logic_block(name):
    if name == 'NOT':
        return fq.Circuit(2,dtype=DTYPE).x(1).cx(0,1)
    c = fq.Circuit(3,dtype=DTYPE)
    if name == 'AND':
        return c.ccx(0,1,2)
    if name == 'XOR':
        return c.cx(0,2).cx(1,2)
    if name == 'OR':
        return c.cx(0,2).cx(1,2).ccx(0,1,2)
    raise ValueError('Supported named Boolean examples: NOT,AND,XOR,OR')


def network(stage='clean'):
    if stage not in ('compute','use','clean','bad-data'):
        raise ValueError('Declare a supported reversible network stage')
    compute = fq.Circuit(5,dtype=DTYPE).ccx(0,1,3)
    c = fq.Circuit(5,dtype=DTYPE).compose(compute)
    if stage != 'compute':
        c.cx(3,4).cx(2,4)
    if stage == 'bad-data':
        c.x(0)
    if stage in ('clean','bad-data'):
        c.compose(compute.adjoint())
    return c


def network_reference(v, stage='clean'):
    if stage not in ('compute','use','clean','bad-data') or v.shape != (32,):
        raise ValueError('Declared stage and five-qubit vector required')
    out = torch.zeros(32,dtype=DTYPE)
    for j,bits in enumerate(product((0,1),repeat=5)):
        a,b,c,w,y = bits
        w ^= a & b
        if stage != 'compute':
            y ^= w ^ c
        if stage == 'bad-data':
            a ^= 1
        if stage in ('clean','bad-data'):
            w ^= a & b
        out[16*a+8*b+4*c+2*w+y] += v[j]
    return out


def probability_one(p, q):
    n = len(p).bit_length()-1
    return sum(p[j].item() for j in range(len(p)) if (j >> (n-1-q)) & 1)


def main():
    assert version('flagquantum') == '0.3.1' and version('torch').split('+')[0] == '2.13.0'
    # Every one of the 16 two-input, one-output Boolean truth tables.
    for table in product((0,1),repeat=4):
        U = oracle_matrix(table,2,1)
        assert torch.equal(U.mH@U,torch.eye(8,dtype=DTYPE))
        assert torch.equal(U@U,torch.eye(8,dtype=DTYPE))
        block = fq.Circuit(3,dtype=DTYPE).unitary(0,1,2,unitary=U)
        inputs = [basis_factors(bits) for bits in product((0,1),repeat=3)]+[complex_factors(3)]
        for factors in inputs:
            v,p = run(block,factors)
            torch.testing.assert_close(v,oracle_reference(product_input(factors),table,2,1),rtol=0,atol=ATOL)
        factors = complex_factors(3)
        v,p = run(fq.Circuit(3,dtype=DTYPE).compose(block).compose(block),factors)
        torch.testing.assert_close(v,product_input(factors),rtol=0,atol=ATOL)
    assert RUNS == 160
    print('16 Boolean functions: all8 basis inputs,complex input and U_f squared checked;160circuits.')
    table = [0,2,2,1]  # output bits: sum=a XOR b, carry=a AND b; MSB sum, LSB carry.
    block = fq.Circuit(4,dtype=DTYPE).unitary(0,1,2,3,unitary=oracle_matrix(table,2,2))
    for factors in [basis_factors(bits) for bits in product((0,1),repeat=4)]+[complex_factors(4)]:
        v,p = run(block,factors)
        torch.testing.assert_close(v,oracle_reference(product_input(factors),table,2,2),rtol=0,atol=ATOL)
    factors = complex_factors(4)
    v,p = run(fq.Circuit(4,dtype=DTYPE).compose(block).compose(block),factors)
    torch.testing.assert_close(v,product_input(factors),rtol=0,atol=ATOL)
    native = fq.Circuit(4,dtype=DTYPE).cx(0,2).cx(1,2).ccx(0,1,3)
    for factors in [basis_factors(bits) for bits in product((0,1),repeat=4)]+[complex_factors(4)]:
        v,p = run(native,factors)
        torch.testing.assert_close(v,oracle_reference(product_input(factors),table,2,2),rtol=0,atol=ATOL)
    print('Two-output half-adder table [0,2,2,1]: dense and named-gate paths,all16 inputs,complex input and roundtrip;35circuits.')
    tables = {'NOT':[1,0],'AND':[0,0,0,1],'XOR':[0,1,1,0],'OR':[0,1,1,1]}
    for name,table in tables.items():
        n = 1 if name == 'NOT' else 2
        block = logic_block(name)
        for factors in [basis_factors(bits) for bits in product((0,1),repeat=n+1)]+[complex_factors(n+1)]:
            v,p = run(block,factors)
            torch.testing.assert_close(v,oracle_reference(product_input(factors),table,n,1),rtol=0,atol=ATOL)
    print('Named X,CX,CCX constructions of NOT,AND,XOR,OR: all target bits and complex inputs;32circuits.')
    for factors in [basis_factors(bits) for bits in product((0,1),repeat=5)]+[complex_factors(5)]:
        v,p = run(network(),factors)
        torch.testing.assert_close(v,network_reference(product_input(factors)),rtol=0,atol=ATOL)
    factors = complex_factors(3)+[(1,0),(.6,.8j)]
    for stage in ('compute','use','clean'):
        v,p = run(network(stage),factors)
        torch.testing.assert_close(v,network_reference(product_input(factors),stage),rtol=0,atol=ATOL)
        if stage == 'clean':
            assert probability_one(p,3)<ATOL
    print('g(a,b,c)=(a AND b) XOR c: all32 network inputs,complex input and3coherent stages;36circuits.')
    # Phase kickback is a full-vector check; the minus target remains a separate factor.
    factors = complex_factors(2)+[(1/sqrt(2),-1/sqrt(2))]
    v,p = run(logic_block('AND'),factors)
    expected = product_input(factors)
    expected[6:] *= -1
    torch.testing.assert_close(v,expected,rtol=0,atol=ATOL)
    # Explicit wrong-blank and changed-data witnesses, with b=1 for certain failed cleanup.
    for stage,bits in (('clean',(1,1,0,1,0)),('bad-data',(1,1,0,0,0))):
        factors = basis_factors(bits)
        v,p = run(network(stage),factors)
        torch.testing.assert_close(v,network_reference(product_input(factors),stage),rtol=0,atol=ATOL)
        assert abs(probability_one(p,3)-1)<ATOL
    print('Minus-target phase kickback and2wrong-contract witnesses:3circuits; workspace failures predicted.')
    # An entangled input, independently prepared and referenced, is not a classical random branch.
    block = fq.Circuit(3,dtype=DTYPE).h(0).cx(0,1).compose(logic_block('AND'))
    v,p = run(block,basis_factors((0,0,0)))
    expected = torch.zeros(8,dtype=DTYPE);expected[0]=expected[7]=1/sqrt(2)
    torch.testing.assert_close(v,expected,rtol=0,atol=ATOL)
    bad = [lambda:oracle_matrix([0]*4,True,1),lambda:oracle_matrix([0]*4,2,0),
           lambda:oracle_matrix([0]*4,2,5),lambda:oracle_matrix([0]*3,2,1),
           lambda:oracle_matrix([0,0,0,2],2,1),lambda:oracle_matrix([0,0,0,-1],2,1),
           lambda:oracle_matrix([0,0,0,True],2,1),lambda:oracle_matrix([0,0,0,1.],2,1),
           lambda:network('reset'),lambda:logic_block('arbitrary-callable'),
           lambda:oracle_reference(torch.zeros(4,dtype=DTYPE),[0,0,0,1],2,1)]
    for action in bad:
        try: action()
        except ValueError: pass
        else: raise AssertionError('Invalid Boolean/register contract admitted')
    assert RUNS == 267, RUNS
    print('Entangled input checked;11invalid contracts rejected;267actual CPUcomplex128 circuits,atol1e-12,rtol0.')
    print('Dense oracle helper limited to n+m<=6; no efficient-synthesis,reset,shots,noise or hardware claim.')


if __name__ == '__main__':
    main()
