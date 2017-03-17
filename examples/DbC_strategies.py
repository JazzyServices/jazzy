# coding:ascii
""" Example usage of DbC (design by contract)

Strategies for the order in which to specify the decorators

Note that at level ASSERTION_INVARIANT, an exception raised by the
outgoing-invariant will supercede any raised by wrapped functions.
"""
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import DbC
DbC.ASSERTION_LEVEL = DbC.ASSERTION_ALL

from DbC import pre, post, invariant_safe

class Strategies(object):
    'Strategies for placing the @invariant_safe decorators.'
    def _invariant(I):
        print('INVARIANT')
    def _pre(I):
        print('PRE')
    def _post(I, rval):
        print('POST')

    # strategy 1.
    # put the @invariant_safe decorator last
    @pre(_pre)
    @post(_post)
    @invariant_safe(_invariant)
    def strategy1(my):
        print('++ Invariant is called after PRE then before POST')
        print('++ If PRE asserts, the invariant will not be called')

    # strategy 2.
    # put the @invariant_safe decorator first
    @invariant_safe(_invariant)
    @pre(_pre)
    @post(_post)
    def strategy2(my):
        print(
'''\
++ Invariant is called before PRE and after POST.
++ Guarantees that the invariant will be called on entry and on exit.\
'''     )

    # strategy 3.
    @post(_post)
    @invariant_safe(_invariant)
    @pre(_pre)
    def strategy3(my):
        print(
'''\
++ Invariant is called before PRE and again before POST.
++ Guarantees that the invariant will be called on entry and on exit.
++ POST checks the return value after invariant has verified that class
++ is consistent.\
'''     )

r = Strategies()
print('-- STRATEGY 1  - -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --')
r.strategy1()
print('-- STRATEGY 2  - -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --')
r.strategy2()
print('-- STRATEGY 3  - -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --')
r.strategy3()
print('-- -- -- -- -- - -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --')


class AlternativeStrategy(object):
    'An alternative strategy: call the invariant directly in pre/post.'
    # optionally decorate the invariant with an assertion level
    @DbC.checker_for(DbC.ASSERTION_WEAK_INVARIANT)
    def _invariant(I):
        print('INVARIANT')
    def _pre(I):
        print('PRE')
        I._invariant()
    def _post(I, rval):
        I._invariant()
        print('POST')

    @pre(_pre)
    @post(_post)
    def alternative(my):
        print(
'''\
++ Invariant is called directly by PRE and POST.
++ So depending on the placement of the call within those checkers the
++ invariant can be called after or before PRE and/or POST.
++ Since the invariant is called directly it has the same level as the PRE
++ and POST checkers (ASSERTION_REQUIRE or ASSERTION_ENSURE).
++ We can optionally decorate the invariant using @checker_for\
'''     )

r = AlternativeStrategy()
print('-- ALTERNATIVE STRATEGY - -- -- -- -- -- -- -- -- -- -- -- -- -- --')
r.alternative()
print('-- -- -- -- -- - -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --')
