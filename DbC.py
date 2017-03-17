"""
Design-by-Contract (DbC)

Use @pre(pre_checker_function) and @post(post_checker_function)
to check pre- and post- conditions of a function using checker functions

Use @invariant_safe(invariant_function) to check that methods don't break the
 class invariant

Use @checker_for(assertion_level) to mark a function/method as a checker
function that you intend to call stand-alone (rather than via the decorator).

Checker functions (whether for pre-conditions, post-conditions, invariants or
checks) should use good-old-fashioned assert statements, or should raise
PostConditionError, PreConditionError or InvariantError as appropriate.
Since PostConditionError, PreConditionError and InvariantError are subclasses
of AssertionError, your test code can use "except AssertionError" to catch all
pre-, post-, invariant and check failures.
  _____________________
_| Enabling Assertions |______________________________________________________

In order for the contracts to be checked, you will need to turn on
ASSERTION_ALL (or one of the other levels) -- this can be done using an
environment variable:
    export ASSERTION_LEVEL=ALL
or explicitly via assignment:
    import DbC
    DbC.ASSERTION_LEVEL = DbC.ASSERTION_ALL
______________________________________________________________________________
"""

import os
import sys
import jazzy

# From the Eiffel documentation ...
# no : assertions have no run-time effect.
# require : monitor preconditions only, on routine entry.
# ensure : preconditions on entry, postconditions on exit.
# invariant : same as ensure, plus class invariant on both entry and exit.
# all : same as invariant, plus check instructions.

(
    ASSERTION_NONE,
    ASSERTION_REQUIRE,
    ASSERTION_ENSURE,
    ASSERTION_WEAK_INVARIANT,
    ASSERTION_INVARIANT,
    ASSERTION_CHECK,
    ASSERTION_PARANOID
) = range(7)
ASSERTION_ALL = ASSERTION_CHECK

# The difference between ASSERTION_INVARIANT and ASSERTION_WEAK_INVARIANT is
# that "weak" level won't call the checker function on exit if an exception
# has been raised by the decorated function. This allows you to detect any
# exceptions in the usual way BUT won't guarantee that the invariant has not
# been violated. The "non-weak" level gives priority to the detection of
# invariant violations. If an exception is raised by the decorated function,
# the checker function is still called on exit (via a `finally` clause). If
# the checker function subsequently raises an exception this will cause the
# original exception to be discarded in Python2.x.

_ASSERTION_NAME_MAP = {
    'ASSERTION_NONE': ASSERTION_NONE,
    'ASSERTION_REQUIRE': ASSERTION_REQUIRE,
    'ASSERTION_ENSURE': ASSERTION_ENSURE,
    'ASSERTION_WEAK_INVARIANT': ASSERTION_WEAK_INVARIANT,
    'ASSERTION_INVARIANT': ASSERTION_INVARIANT,
    'ASSERTION_CHECK': ASSERTION_CHECK,
    'ASSERTION_PARANOID': ASSERTION_PARANOID,
    'ASSERTION_ALL': ASSERTION_ALL,
    'NONE': ASSERTION_NONE,
    'REQUIRE': ASSERTION_REQUIRE,
    'ENSURE': ASSERTION_ENSURE,
    'INVARIANT': ASSERTION_INVARIANT,
    'CHECK': ASSERTION_CHECK,
    'PARANOID': ASSERTION_PARANOID,
    'ALL': ASSERTION_ALL,
    '0': ASSERTION_NONE,
    '1': ASSERTION_REQUIRE,
    '2': ASSERTION_ENSURE,
    '3': ASSERTION_WEAK_INVARIANT,
    '4': ASSERTION_INVARIANT,
    '5': ASSERTION_CHECK,
    '6': ASSERTION_PARANOID,
    None: ASSERTION_NONE,
}

# Turn off Design-by-Contract by default
ASSERTION_LEVEL = _ASSERTION_NAME_MAP.get(os.getenv('ASSERTION_LEVEL'), 0)

_DO_NOTHING = lambda *args: None


def _paranoid(value):
    assert value is None, u'checker functions should not return a value'


def _poparg(name, arglis, kwargs, dflts):
    'Pop a named argument from the keyword dictionary or the lists.'
    if name in kwargs:
        rval = kwargs.pop(name)
    elif arglis:
        rval = arglis.pop(0)
    else:
        rval = dflts.pop(0)
    return rval


def _unvarargs(names, args, kwargs, dflts):
    'Convert varargs/keyword/default args to a flat tuple.'
    arglis = list(args)
    rval = tuple(_poparg(name, arglis, kwargs, dflts) for name in names)
    return rval + tuple(arglis)


#   ________________________
# _| PRE-CONDITION CHECKING |_________________________________________________
# aka REQUIRE
#
# You can decorate your functions and methods with:
#  @pre(checker)
# to call the given checker with the same arguments as the original function
# if ASSERTION_LEVEL >= ASSERTION_REQUIRE then the checker will be called
# prior to calling the original function
# if ASSERTION_LEVEL < ASSERTION_REQUIRE then the checker will not be called
#
# The checker should assert that all the required pre-conditions have been met
#
# The checker MUST NOT alter the arguments to the original method;
# it should just check that they are correct.
# The checker SHOULD NOT return a value (because it will be ignored)
#
def pre(checker):

    def pre_decorator(func):

        paranoid = _paranoid \
            if ASSERTION_LEVEL >= ASSERTION_PARANOID \
            else _DO_NOTHING

        def check_pre_condition(*args, **kwargs):
            # Call the checker
            paranoid(checker(*args, **kwargs))
            # Call the function
            return func(*args, **kwargs)

        if ASSERTION_LEVEL >= ASSERTION_REQUIRE:
            return check_pre_condition
        else:
            return func

    return pre_decorator


class PreConditionError(AssertionError):
    pass


def assertPreCondition(expr, *args):
    if not expr:
        prefix = u'PreCondition failure:'
        tup = jazzy.tjoin(prefix, *args)
        message = u' '.join(jazzy.iter_to_unicode(tup))
        raise PreConditionError(message)


#   _________________________
# _| POST-CONDITION CHECKING |________________________________________________
# aka ENSURE
#
# You can decorate your functions and methods with:
#  @post(checker)
# to call the given checker with one additional argument than the original
# function. This additional argument is the return value of the original
# function. For example, if your function is:
#   def fraction(number, denom): ...
# your post checker should be defined thus:
#   def post_fraction(number, denom, result): ...
#
# If your function returns multiple values, result will be a tuple.
# If your function doesn't return anything, result will be None.
# So your post checker function MUST always take one more named parameter
# than the original function.
#
# It is highly recommended that the parameter names are the same between the
# post checker and the original function.
#
# if ASSERTION_LEVEL >= ASSERTION_ENSURE then the checker will be called
# after calling the original function passing the checker the return value
# from the original function.
# if ASSERTION_LEVEL < ASSERTION_ENSURE then the checker will not be called
#
# The checker should assert that all the required post-conditions have been met
#
# The checker MUST NOT alter the arguments to the original method;
# it should just check that they are correct.
# The checker SHOULD NOT return a value (because it will be ignored)
#
def post(checker):

    def post_decorator(func):

        paranoid = _paranoid \
            if ASSERTION_LEVEL >= ASSERTION_PARANOID \
            else _DO_NOTHING

        def check_post_condition(*args, **kwargs):
            # Call the function
            rval = func(*args, **kwargs)
            # Convert varargs to a flat tuple
            # - this is necessary because we need to add the result to the
            #   argument list to pass to the checker
            kcopy = dict(**kwargs)
            try:
                code = func.func_code
            except AttributeError:
                code = func.__code__
            argnames = code.co_varnames[:code.co_argcount]
            try:
                dflts = func.func_defaults
            except AttributeError:
                dflts = func.__defaults__
            postargs = _unvarargs(
                argnames, args, kcopy, list(dflts or []))
            # Append the result to the flat argument list
            postargs = postargs + (rval,)
            # Call the checker
            paranoid(checker(*postargs, **kcopy))
            return rval

        if ASSERTION_LEVEL >= ASSERTION_ENSURE:
            return check_post_condition
        else:
            return func

    return post_decorator


class PostConditionError(AssertionError):
    pass


def assertPostCondition(expr, *args):
    if not expr:
        prefix = u'PostCondition failure:'
        tup = jazzy.tjoin(prefix, *args)
        message = u' '.join(jazzy.iter_to_unicode(tup))
        raise PostConditionError(message)


#   ____________________
# _| INVARIANT CHECKING |_____________________________________________________
#
# You can decorate your methods with
#  @invariant_safe(checker)
# to call the given checker on entry to AND on exit from the decorated method
# The checker method should take only one parameter (self)
# if ASSERTION_LEVEL >= ASSERTION_INVARIANT then the checker will be called
# if ASSERTION_LEVEL < ASSERTION_INVARIANT then the checker will not be called
#
def invariant_safe(checker):

    def invariant_decorator(func):

        paranoid = _paranoid \
            if ASSERTION_LEVEL >= ASSERTION_PARANOID \
            else _DO_NOTHING

        def check_weak_invariant(*args, **kwargs):
            # Call the checker with the first argument only
            paranoid(checker(*args[:1]))
            # Call the function
            rval = func(*args, **kwargs)
            # Call the checker again
            paranoid(checker(*args[:1]))
            return rval

        def check_invariant(*args, **kwargs):
            # Call the checker with the first argument only
            paranoid(checker(*args[:1]))
            rval = None
            try:
                # Call the function
                rval = func(*args, **kwargs)
            finally:
                # Call the checker again
                paranoid(checker(*args[:1]))
            return rval

        if ASSERTION_LEVEL >= ASSERTION_INVARIANT:
            return check_invariant
        elif ASSERTION_LEVEL >= ASSERTION_WEAK_INVARIANT:
            return check_weak_invariant
        else:
            return func

    return invariant_decorator


class InvariantError(AssertionError):
    pass


def assertInvariant(expr, *args):
    if not expr:
        prefix = u'Invariant violation:'
        tup = jazzy.tjoin(prefix, *args)
        message = u' '.join(jazzy.iter_to_unicode(tup))
        raise InvariantError(message)


#   __________
# _| CHECKERS |_______________________________________________________________
# Enable functions depending on ASSERTION_LEVEL
#
# @checker_for(ASSERTION_INVARIANT)
# def my_checker(self):
#   assert self.something is not None

def checker_for(assertion_level):
    'Enable a function when ASSERTION_LEVEL is at or above a threshold.'
    def inner(func):
        if ASSERTION_LEVEL >= assertion_level:
            return func
        else:
            return lambda *args: None
    return inner

