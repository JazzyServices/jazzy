# coding:ascii
""" Example usage of DbC (design by contract)

In this example we show you how to use the DbC.checker_for() decorator
to enable checker functions depending on the ASSERTION_LEVEL

The functions in this module manipulate floating point strings
without converting them to float or Decimal.

A floating point string has seven parts (not counting the decimal point):

    00120300.04005600e+08
 7  | |   |  ||    |   |__ 08: E  (optional exponent)
 6  | |   |  ||    |______ 00: trailing zeroes (ignored)
 5  | |   |  ||________ 40056: FD (fractional digits)
 4  | |   |  |_____________ 0: FZ (fractional leading zeroes)
 3  | |   |_______________ 00: IZ (integral trailing zeroes)
 2  | |_________________ 1203: ID (integral digits)
 1  |_____________________ 00: leading zeroes (ignored)

The function try to extract the significant digits (as a string) and
the power-of-ten from a string using checker functions as they go along.
"""
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import re

import DbC
DbC.ASSERTION_LEVEL = DbC.ASSERTION_ALL

# checker function only enabled if assertion level is REQUIRE or above
@DbC.checker_for(DbC.ASSERTION_REQUIRE)
def check_true(b):
    assert b

# checker function only enabled if assertion level is ENSURE or above
@DbC.checker_for(DbC.ASSERTION_ENSURE)
def check_no_outside_digits(s):
    'Check that either s is zero OR it has no leading/trailing zeroes.'
    assert s == '0' or (s[0] != '0' and s[-1] != '0')

# checker function only enabled if assertion level is ENSURE or above
@DbC.checker_for(DbC.ASSERTION_ENSURE)
def check_v_decimal(s, digits, power):
    'Check that s == digits * 10**power.'
    from decimal import Decimal
    s10 = Decimal(s)
    d10 = Decimal(digits or 0) * Decimal(10) ** Decimal(power)
    assert s10 == d10, 's={} => {} v {}'.format(s, s10, d10)

# checker function only enabled if assertion level is CHECK or above
@DbC.checker_for(DbC.ASSERTION_CHECK)
def check_implies(p, q):
    p or not q


def _get_sig_digs_parts(ID, IZ, FZ, FD, E):
    'Extract the significant digits from the parts of a floating string.'
    # validate that if IZ is set, ID must be set
    check_implies(IZ != '', ID != '')
    # digits before and after the decimal point?
    if ID and FD:
        return ID + IZ + FZ + FD
    # digits before but not after the decimal point?
    elif ID:
        return ID
    # digits after but not before the decimal point?
    elif FD:
        return FD
    else:
        return '0'

def _get_power_of_ten(ID, IZ, FZ, FD, E):
    'Extract the power-of-ten from the parts of a floating string.'
    # validate that if IZ is set, ID must be set
    check_implies(IZ != '', ID != '')
    # 2500 250 25 2.5 .25 .025 <-- number
    #    2   1  0  -1  -2   -3 <-- power of ten
    # Integer part only
    if not FD:
        rval = len(IZ)
    # Has fractional part
    else:
        rval = 0 - len(FZ) - len(FD)
        check_true(rval != 0)
    # Add the exponent
    if E:
        rval += int(E)
    return rval

def _noparts(ID, IZ, FZ, FD, E):
    'Return True if there are no I or F parts.'
    return (ID, IZ, FZ, FD) == ('', '', '', '')

def get_fp_info(s):
    'Extract information from a floating point string with exponent.'
    reg = r'(?:0*)([0-9]*?)(0*)\.(0*)([0-9]*?)(?:0*)(?:[Ee]([+-]?\d+))?$'
    m = re.match(reg, s)
    if not m:
        raise ValueError('Not a floating point number `{}`'.format(s))
    else:
        if s[0] == '.' and _noparts(*m.groups()):
            raise ValueError('Not a floating point number `{}`'.format(s))
        # significant digits
        digits = _get_sig_digs_parts(*m.groups())
        # digits must not have any leading/trailing zeroes
        # (unless the number is actually zero)
        check_no_outside_digits(digits)
        # no need to calculate power if digits is zero
        if digits == '0':
            return 'n', digits, 0
        # power of ten
        power = _get_power_of_ten(*m.groups())
        # check that s == digits * 10**power
        check_v_decimal(s, digits, power)
        return 'p', digits, power

def key_for_float_string(s):
    sign, digits, power = get_fp_info(s)
    if digits == '0':
        return 'o', 0, '0'
    #  2500   250    25   2.5    .25   .025 <-- number
    # 2.5e3 2.5e2 2.5e1 2.5e0 2.5e-1 2.5e-2 <-- scientific
    #     4     3     2     1      0     -1 <-- normalised (e+1)

    # normalise to 0.digits * 10**power
    # (a simpler calculation than to Scientific Notation)
    return 'p', power + len(digits), digits


data = [
    '0.0',
    '3.14159',
    '2.99792458e8', # speed of light m/s
    '6.67408e-11',  # gravitational constant Nm2/kg2
    '6.626070040e-34',    # planck constant Js
    '8.854187817e-12',  # electric constant C2/Nm2
    '1.6021766208e-19', # elementary charge
    '9.80665', # standard gravity m/s2
]
def main():
    # use `key_for_float_string` to sort the strings
    data.sort(key=key_for_float_string)
    for f in data:
        print(f)

if __name__ == '__main__':
    main()
