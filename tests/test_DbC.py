import sys
import unittest

import context
import DbC
DbC.ASSERTION_LEVEL = DbC.ASSERTION_ALL

#   ________________________
# _| Pre-Condition checkers |_________________________________________________
def pre_checker_1(x):
    assert x is not None

def pre_checker_2(x, y):
    DbC.assertPreCondition(x<y, x, 'must be less than', y)

def pre_checker_dflt_args(i=0, e=0):
    if i == 0:
        assert e == 0

def pre_checker_varargs(*args):
    assert all(a for a in args)

def pre_checker_kwargs(**kw):
    assert all(a for a in kw.values())

def pre_checker_varargs_kwargs(first=0, second=0, *args, **kw):
    assert first == len(args)
    assert second == len(kw)

#   _________________________
# _| Post-Condition checkers |________________________________________________
def post_checker_1(x, y, rval):
    assert rval > 0

def post_checker_2(x, y, rval):
    DbC.assertPostCondition(rval > 0, x, '-', y, 'must produce value > 0')

def post_checker_varargs(*args):
    # When a POST-checker has varargs, the last arg is the return value
    # from the function
    rval = args[-1]
    assert len(rval) > 0

def post_checker_kwargs(rval, **kw):
    # There is always one more positional argument in a post-checker
    assert rval > 0

def post_checker_varargs_kwargs(first, *args, **kw):
    # When a POST-checker has varargs, the last arg is the return value
    # from the function
    rval = args[-1]
    assert rval > 0

#   __________________________________
# _| Classes used for invariant tests |_______________________________________
class BaseCounter(object):
    def __init__(my, c):
        my.counter = c
        my.calls = 0
        my.checks = 0
    def invariant(my):
        my.checks += 1
        assert my.counter > 0, 'counter too small'

def check_is_even(obj):
    'A function (not a method) used as an invariant.'
    obj.checks += 1
    assert (obj.counter & 1) == 0, 'counter is odd'

class Counter(BaseCounter):
    #[
    @DbC.invariant_safe(BaseCounter.invariant)
    def decrement(my):
        my.calls += 1
        my.counter -= 1
    #
    @DbC.invariant_safe(BaseCounter.invariant)
    def decrement_by(my, by):
        my.calls += 1
        my.counter -= by
    #
    @DbC.invariant_safe(check_is_even)
    def halve(my):
        my.calls += 1
        my.counter //= 2
    #
    @DbC.invariant_safe(BaseCounter.invariant)
    def increment(my):
        raise NotImplementedError('TODO: write increment method')
    #]

#   ___________
# _| The Tests |______________________________________________________________

class Test_Pre(unittest.TestCase):

    def test_pre_called(I):
        'Test that Pre Condition is called.'
        DbC.ASSERTION_LEVEL = DbC.ASSERTION_ALL
        @DbC.pre(pre_checker_1)
        def sut(x):
            return x.__class__.__name__
        with I.assertRaises(AssertionError):
            ans = sut(None)

    def test_pre_level0(I):
        'Test that Pre Condition is not called below REQUIRE.'
        DbC.ASSERTION_LEVEL = DbC.ASSERTION_NONE
        @DbC.pre(pre_checker_1)
        def sut(x):
            return x.__class__.__name__
        ans = sut(None)
        I.assertEqual(ans, 'NoneType')

    def test_pre_pass(I):
        "Test that Pre Condition doesn't assert if expr is true."
        DbC.ASSERTION_LEVEL = DbC.ASSERTION_ALL
        @DbC.pre(pre_checker_1)
        def sut(x):
            return x.__class__.__name__
        ans = sut(0)
        I.assertEqual(ans, 'int')

    def test_pre_exception(I):
        'Test that Pre Condition raises PreConditionError.'
        DbC.ASSERTION_LEVEL = DbC.ASSERTION_REQUIRE
        @DbC.pre(pre_checker_2)
        def sut(x, y):
            return x - y
        with I.assertRaises(AssertionError) as cm:
            ans = sut(0, 0)
        msg = cm.exception.args[0]
        I.assertEqual(msg, 'PreCondition failure: 0 must be less than 0')
        I.assertIsInstance(cm.exception, DbC.PreConditionError)

    def test_pre_dfltargs(I):
        'Test that pre-checker handles default arguments.'
        DbC.ASSERTION_LEVEL = DbC.ASSERTION_ALL
        @DbC.pre(pre_checker_dflt_args)
        def sut(i=0, e=0):
            return i * 10**e
        # check that good data doesn't raise an exception
        ans = sut(4.2, e=1)
        I.assertEqual(ans, 42.0)
        # check that invalid data does raise an exception
        with I.assertRaises(AssertionError):
            ans = sut(0, -1)
        with I.assertRaises(AssertionError):
            ans = sut(e=-2)
        # when pre-cond fails, no value is returned (ans remains unchanged)
        I.assertEqual(ans, 42.0)

    def test_pre_varargs(I):
        'Test that pre-checker takes varargs.'
        DbC.ASSERTION_LEVEL = DbC.ASSERTION_ALL
        @DbC.pre(pre_checker_varargs)
        def sut(*args):
            return sorted(args)
        # check that good data doesn't raise an exception
        ans = sut(1, 4, 2)
        I.assertEqual(ans, [1, 2, 4])
        # check that invalid data does raise an exception
        with I.assertRaises(AssertionError):
            ans = sut(5, 3, 0, 2)
        # when pre-cond fails, no value is returned (ans remains unchanged)
        I.assertEqual(ans, [1, 2, 4])

    def test_pre_kwargs(I):
        'Test that pre-checker takes kwargs.'
        DbC.ASSERTION_LEVEL = DbC.ASSERTION_ALL
        @DbC.pre(pre_checker_kwargs)
        def sut(**kw):
            return len(kw)
        # check that good data doesn't raise an exception
        ans = sut(one=1, four=4, two=2)
        I.assertEqual(ans, 3)
        # check that invalid data does raise an exception
        with I.assertRaises(AssertionError):
            ans = sut(five=5, three=3, zero=0, two=2)
        # when pre-cond fails, no value is returned (ans remains unchanged)
        I.assertEqual(ans, 3)

    def test_pre_varargs_kwargs(I):
        'Test that pre-checker takes varargs and kwargs.'
        DbC.ASSERTION_LEVEL = DbC.ASSERTION_ALL
        @DbC.pre(pre_checker_varargs_kwargs)
        def sut(first=0, second=0, *args, **kw):
            return first - len(args) + second - len(kw)
        # check that good data doesn't raise an exception
        ans = sut(1, 3, 'arg', one=1, four=4, two=2)
        I.assertEqual(ans, 0)
        I.assertEqual(sut(), 0)
        I.assertEqual(sut(1, 0, 'arg'), 0)
        I.assertEqual(sut(0, 1, k='arg'), 0)
        I.assertEqual(sut(second=1, k='arg'), 0)
        # check that invalid data does raise an exception
        with I.assertRaises(AssertionError):
            ans = sut(1, 3, one=1, four=4, two=2)
        with I.assertRaises(AssertionError):
            ans = sut(1, 3, 'arg', four=4, two=2)
        with I.assertRaises(AssertionError):
            ans = sut(1)
        with I.assertRaises(AssertionError):
            ans = sut(second=1)
        with I.assertRaises(AssertionError):
            ans = sut(second=0, first=1)
        # when pre-cond fails, no value is returned (ans remains unchanged)
        I.assertEqual(ans, 0)


class Test_Post(unittest.TestCase):

    def test_post_called(I):
        'Test that Post Condition is called.'
        DbC.ASSERTION_LEVEL = DbC.ASSERTION_ALL
        @DbC.post(post_checker_1)
        def sut(x, y):
            return x - y
        with I.assertRaises(AssertionError):
            ans = sut(2, 5)

    def test_post_level1(I):
        'Test that Post Condition is not called below ENSURE.'
        DbC.ASSERTION_LEVEL = DbC.ASSERTION_REQUIRE
        @DbC.post(post_checker_1)
        def sut(x, y):
            return x - y
        ans = sut(2, 5)
        I.assertEqual(ans, -3)

    def test_post_pass(I):
        "Test that Post Condition doesn't assert if expr is true."
        DbC.ASSERTION_LEVEL = DbC.ASSERTION_ALL
        @DbC.post(post_checker_1)
        def sut(x, y):
            return x - y
        ans = sut(5, 2)
        I.assertEqual(ans, 3)

    def test_post_exception(I):
        'Test that Post Condition raises PostConditionError.'
        DbC.ASSERTION_LEVEL = DbC.ASSERTION_ENSURE
        @DbC.post(post_checker_2)
        def sut(x, y):
            return x - y
        with I.assertRaises(AssertionError) as cm:
            ans = sut(0, 0)
        msg = cm.exception.args[0]
        I.assertEqual(msg,
            'PostCondition failure: 0 - 0 must produce value > 0')
        I.assertIsInstance(cm.exception, DbC.PostConditionError)

    def test_post_varargs(I):
        'Test that post-checker takes varargs.'
        DbC.ASSERTION_LEVEL = DbC.ASSERTION_ALL
        @DbC.post(post_checker_varargs)
        def sut(*args):
            return [a for a in args if not a]
        with I.assertRaises(AssertionError):
            ans = sut(5, 3, 1, 2)

    def test_post_kwargs(I):
        'Test that post-checker takes kwargs.'
        DbC.ASSERTION_LEVEL = DbC.ASSERTION_ALL
        @DbC.post(post_checker_kwargs)
        def sut(**kw):
            return min(a for a in kw.values())
        # check that good data doesn't raise an exception
        ans = sut(one=1, four=4, two=2)
        I.assertEqual(ans, 1)
        # check that invalid data does raise an exception
        with I.assertRaises(AssertionError):
            ans = sut(five=5, three=3, zero=0, two=2)
        # when pre-cond fails, no value is returned (ans remains unchanged)
        I.assertEqual(ans, 1)

    def test_post_varargs_kwargs(I):
        'Test that post-checker takes varargs and kwargs.'
        DbC.ASSERTION_LEVEL = DbC.ASSERTION_ALL
        @DbC.post(post_checker_varargs_kwargs)
        def sut(first=0, *args, **kw):
            return first - len(args) - len(kw)
        # check that good data doesn't raise an exception
        ans = sut(3, 'arg', key='a')
        I.assertEqual(ans, 1)
        # check that invalid data does raise an exception
        with I.assertRaises(AssertionError):
            ans = sut(4, 3, 'arg', four=4, two=2)
        with I.assertRaises(AssertionError):
            ans = sut()
        with I.assertRaises(AssertionError):
            ans = sut(1, x='!')
        # when post-cond fails, no value is returned (ans remains unchanged)
        I.assertEqual(ans, 1)

class Test_Invariant(unittest.TestCase):

    def test_invariant_called_on_entry(I):
        'Test that Invariant is called on entry to the method.'
        sut = Counter(0)
        # since counter is 0, we should get an assertion
        with I.assertRaises(AssertionError) as cm:
            sut.decrement()
        I.assertEqual(cm.exception.args[0], 'counter too small')
        I.assertEqual(sut.checks, 1)
        I.assertEqual(sut.calls, 0)

    def test_invariant_called_on_exit(I):
        'Test that Invariant is called on exit from the method.'
        sut = Counter(1)
        # since counter is 1, we should get an assertion after decrement
        with I.assertRaises(AssertionError) as cm:
            sut.decrement()
        I.assertEqual(cm.exception.args[0], 'counter too small')
        I.assertEqual(sut.checks, 2)
        # verify that decrement was called
        I.assertEqual(sut.calls, 1)

    def test_invariant_args(I):
        'Test that Invariant only takes one arg.'
        sut = Counter(4)
        sut.decrement_by(2)
        I.assertEqual(sut.checks, 2)
        I.assertEqual(sut.calls, 1)
        I.assertEqual(sut.counter, 2)

    def test_invariant_error(I):
        'Test that Invariant can raise InvariantError.'
        DbC.ASSERTION_LEVEL = DbC.ASSERTION_INVARIANT
        class LocalCounter(BaseCounter):
            def local_invariant(my):
                my.checks += 1
                DbC.assertInvariant(my.counter > 0,
                    'counter', my.counter, 'too small')
            @DbC.invariant_safe(local_invariant)
            def decrement(my):
                my.calls += 1
                my.counter -= 1
        sut = LocalCounter(0)
        with I.assertRaises(DbC.InvariantError) as cm:
            sut.decrement()
        I.assertEqual(cm.exception.args[0],
            'Invariant violation: counter 0 too small')
        I.assertEqual(sut.checks, 1)
        I.assertEqual(sut.calls, 0)
        I.assertEqual(sut.counter, 0)

    def test_invariant_function(I):
        'Test that an Invariant can be a plain function.'
        # assertion raised on entry
        sut = Counter(5)
        with I.assertRaises(AssertionError) as cm:
            sut.halve()
        I.assertEqual(cm.exception.args[0], 'counter is odd')
        I.assertEqual(sut.checks, 1)
        I.assertEqual(sut.calls, 0)
        # assertion raised on exit
        sut = Counter(6)
        with I.assertRaises(AssertionError) as cm:
            sut.halve()
        I.assertEqual(cm.exception.args[0], 'counter is odd')
        I.assertEqual(sut.checks, 2)
        I.assertEqual(sut.calls, 1)

    def test_invariant_level(I):
        'Test that Invariant is not called below WEAK_ASSERTION.'
        DbC.ASSERTION_LEVEL = DbC.ASSERTION_ENSURE
        class LocalCounter(BaseCounter):
            @DbC.invariant_safe(BaseCounter.invariant)
            def decrement(my):
                my.calls += 1
                my.counter -= 1
        sut = LocalCounter(0)
        sut.decrement()
        # verify that decrement was called and counter decremented
        I.assertEqual(sut.calls, 1)
        I.assertEqual(sut.counter, -1)
        # verify that invariant wasn't called
        I.assertEqual(sut.checks, 0)

    def test_invariant_exception(I):
        'Test that Invariant is still called across an exception.'
        sut = Counter(1)
        with I.assertRaises(NotImplementedError) as cm:
            sut.increment()
        I.assertEqual(cm.exception.args[0], 'TODO: write increment method')
        I.assertEqual(sut.checks, 2)
        I.assertEqual(sut.calls, 0)
        I.assertEqual(sut.counter, 1)

    def test_weak_invariant_exception(I):
        'Test that Weak Invariant is not called across an exception.'
        DbC.ASSERTION_LEVEL = DbC.ASSERTION_WEAK_INVARIANT
        class LocalCounter(BaseCounter):
            @DbC.invariant_safe(BaseCounter.invariant)
            def increment(my):
                raise NotImplementedError('TODO: write increment method')
        sut = LocalCounter(1)
        with I.assertRaises(NotImplementedError) as cm:
            sut.increment()
        I.assertEqual(cm.exception.args[0], 'TODO: write increment method')
        # invariant is only called once
        I.assertEqual(sut.checks, 1)
        I.assertEqual(sut.calls, 0)
        I.assertEqual(sut.counter, 1)


if __name__ == '__main__':
    unittest.main()
