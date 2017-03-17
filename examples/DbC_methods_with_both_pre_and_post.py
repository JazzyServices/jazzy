# coding:ascii
""" Example usage of DbC (design by contract)

In this example we show you how to use pre- and post-condition checkers
decorating the same function.

"""
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import DbC
DbC.ASSERTION_LEVEL = DbC.ASSERTION_ALL

# in this example we bring `pre` and `post` into our namespace
from DbC import pre, post

def check_pre(*args):
    'Pre-condition checker.'
    # must have an even number of args
    assert ( len(args) & 1 ) == 0, 'Expected an even number of arguments'
    # all numbers must be non-negative ints
    assert all(i>=0 and isinstance(i,int) for i in args), \
        'Numbers must be positive integers'
    # all second numbers must be < 10
    assert all(i<10 for i in args[1::2]), 'Numbers must be < 10'

def check_post(*args):
    'Post-condition checker.'
    # return value from decorated function is always the last positional
    # parameter
    rval = args[-1]
    # simple check of the number of items in the return
    assert 2 * len(rval) == len(args) - 1
    # check units
    units_out = [i%10 for i in rval]
    units_in  = [i for i in args[1:-1:2]]
    assert units_out == units_in
    # check tens
    tens_out = [i//10 for i in rval]
    tens_in  = [i for i in args[0:-1:2]]
    assert tens_out == tens_in

# It doesn't matter which order you include the decorators
@pre(check_pre)
@post(check_post)
def pairoff(*args):
    'Make tens+units from pairs of numbers.'
    it = iter(args)
    return [10*a+b for a,b in zip(it,it)]

# Test data
print( pairoff(*range(8)) )
print( pairoff(4,2,  10,1) )
try:    # odd number of args
    pairoff(1,2,3,4,5)
except AssertionError as e:
    print(e)
try:    # unit >= 10
    pairoff(4,2, 9,10)
except AssertionError as e:
    print(e)
try:    # negative
    pairoff(4,2, -1,2)
except AssertionError as e:
    print(e)
try:    # non-integer
    pairoff(1.25,0.6)
except AssertionError as e:
    print(e)
