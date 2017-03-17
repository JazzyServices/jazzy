# coding:ascii
""" Example usage of DbC (design by contract)

In this example we show how DbC can catch subtle bugs.

We have a class with two members: `value` and `exponent`
It should always be true that 2**exponent == value (this is the "invariant")

One of the methods (`__ilshift__`) modifies both members.
But if an exception occurs after modifying `exponent` but before the
`value` is changed, then the invariant is violated (it won't be true that
2**exponent == value)

Although the calling code has caught an exception, it won't be obvious
to the caller that the class members are out of sync; and it might not be
till much later that it is noticed (making it difficult to discover where
the original problem lies)

By checking the invariant on entry to, and on exit from, a method we can
find exactly which call caused the problem.
"""
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import DbC
# set the module's assertion level straight after import
# and before declaring any decorated methods
DbC.ASSERTION_LEVEL = DbC.ASSERTION_INVARIANT

class PowerOfTwo(object):
    'A class purely for illustrating the use of DbC.'

    def _invariant(my):
        'Invariant checker. Checks that nothing has gone doolally.'
        # We can use either a straightforward assert or assertInvariant
        # Check that value is a power of 2
        assert ((my.value - 1) & my.value) == 0
        # Check that value is 2**exponent
        DbC.assertInvariant(
            my.value == 1 << my.exponent,
            my.value, 'is not 2 to the power of', my.exponent
        )

    def _post_init(my, exponent, rval):
        'Post-condition checker for __init__ method.'
        # We can call the invariant directly...
        my._invariant()
        # we can use plain old assert instead of assertPostCondition
        assert my.exponent == exponent
        # Post-condition checkers are always called with one more argument
        # than the function they are decorating
        assert rval is None

    # Yes, you can decorate the __init__ method
    @DbC.post(_post_init)
    def __init__(my, exponent=0):
        # you can use asserts directly instead of @DbC.pre(checker)
        assert isinstance(exponent, int), 'exponent must be an integer'
        assert exponent >= 0, 'exponent must be a positive integer'
        my.exponent = exponent
        my.value = 1<<exponent

    # we mark this method as `invariant_safe` to say that the class invariant
    # won't be violated when we call this method.
    # However, there is a bug here that can cause an invariant violation.
    @DbC.invariant_safe(_invariant)
    def __ilshift__(my, other):
        'Augmented left-shift operator <<= .'
        my.exponent += other
        my.value <<= other
        return my

    # We can use the invariant as the pre-condition checker if we like.
    @DbC.pre(_invariant)
    def __int__(my):
        return my.value


def main():
    print( 'calling constructor' )
    s = PowerOfTwo(4)
    print( 'calling augmented shift by 2' )
    s <<= 2
    print( 'calling augmented shift by -1' )
    try:
        s <<= -1
    except ValueError as e:
        print (e)
    # At this point, the invariant has been violated.
    # If ASSERTION_LEVEL is high enough we will see an InvariantError;
    # at a lower ASSERTION_LEVEL we will see the ValueError but won't
    # know whether the object's invariant is OK or not.

    print( 'converting object to int' )
    # at level ASSERTION_REQUIRE or above we will detect the violation
    # when we call the __int__ method
    print( int(s) )

    # now modify DbC.ASSERTION_LEVEL on line 28 to one of the other values
    # and see how this program behaves.
    # The possible values are:
    #   DbC.ASSERTION_NONE
    #   DbC.ASSERTION_REQUIRE
    #   DbC.ASSERTION_ENSURE
    #   DbC.ASSERTION_WEAK_INVARIANT
    #   DbC.ASSERTION_INVARIANT
    #   DbC.ASSERTION_CHECK
    #   DbC.ASSERTION_PARANOID

if __name__ == '__main__':
    main()
