# coding:ascii
""" Example usage of DbC (design by contract)

In this example we show you how to use post-condition checkers,
and some of the issues we might see.
We also should you how to declare post-condition checkers
when the decorated functions take varargs, keywords arguments, etc

"""
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import DbC
DbC.ASSERTION_LEVEL = DbC.ASSERTION_ALL

# in this example we bring `post` into our namespace
from DbC import post

#   ____________________________
# _| function with no arguments |_____________________________________________
# If the function that we want to decorate with a post-condition checker
# has no arguments, the post-condition checker takes a single argument
# which is the return value from the function.

def check_default_joiner(rval):
    'Post-condition checker for get_default_joiner.'
    DbC.assertPostCondition(
        len(rval) == 1,
        'default joiner should be a single character'
    )

@post(check_default_joiner)
def get_default_joiner():
    'Return the default joining character.'
    return ' '

# Let's run this example
print( 24*'- -' )
dj = get_default_joiner()
print('The default joiner is "{}"'.format(dj))

#   _________________
# _| No return value |________________________________________________________
# Even if the function doesn't return a value, the post-condition checker
# still takes an extra argument

def check_print_version(rval):
    'Post-condition checker for print_version.'
    DbC.assertPostCondition(
        rval is None,
        'print_version should not return a value'
    )

@post(check_print_version)
def print_version():
    'Print the version of this module.'
    print('Jazzy Joiner. Version 3.1.42 (c) Jazzy Services Ltd 2017')

# Let's run this example
print( 24*'- -' )
print_version()

#   __________________________
# _| Functions with arguments |_______________________________________________
# The post-condition checkers for functions-with-arguments always have one
# more argument than the decorated function (the return value from the fn)

def check_join_a_tuple(joiner, tup, rval):
    """Post-condition checker for join_a_tuple.

    It takes one more parameter (rval) than the decorated function.
    """
    # Always check with the reverse operation.
    # Since the function used join, we need to use split.
    sp = rval.split(joiner)
    # The split list should have the same number of items as the tuple
    assert len(sp) == len(tup), 'Split length does not match!'

@post(check_join_a_tuple)
def join_a_tuple(joiner, tup):
    'Join the elements of a tuple using the given joiner.'
    return joiner.join(str(a) for a in tup)

# Let's run this example in a few different ways
print( 24*'- -' )
print( join_a_tuple('-', ('hy', 'phen', 'ated')) )
print( join_a_tuple('/', ('', 'var', 'tmp')) )
print( join_a_tuple('!', ('a single item',)) )
print( join_a_tuple('-', (0, 800, 'GO', 4, 'IT')) ) # converts ints to str

# So far so good.
# But writing post-condition checkers is not always easy.
# Why do the following examples raise exceptions?
# (Turn off post-condition checking on line 15 and see what happens)
try:
    print( join_a_tuple('!', ()) )  # empty tuple
except AssertionError as e:
    print(e)
try:
    print( join_a_tuple("'", ("don't use a cat", "o", "nine tails")) )
except AssertionError as e:
    print(e)
try:
    # The squares of the first few integers
    print( join_a_tuple(',', (i*i for i in range(5))) )
except TypeError as e:
    print('Exception thrown in post-condition checker')

# But this one is OK.
# The squares of the first few integers (take 2)
print( join_a_tuple(',', [i*i for i in range(5)]) )

#   _________
# _| GOTCHAS |________________________________________________________________
# The main purpose of post-condition checkers is to verify that the return
# value is `sane`. So often they don't bother with the arguments.
# But if the arguments are used it is worth remembering that:
# + some arguments might be iterators, in which case they will have been
#   fully read by the time the checker is called
# + some arguments are mutable, in which case they will have been mutated
#   by the time the checker is called (so we don't know what they were like
#   when the function was entered)
#
# If the checker is going to validate the return value against the original
# arguments (assuming they are available) then the right strategy is to use
# "reverse operation".
# E.g given:
#       def add(a, b): return a+b
# the checker should assert that: (rval - a == b) and/or (rval - b == a)
# there is no value in asserting that: (rval == a+b) since you are just
# repeating the action of the function.
# Therefore, when writing a checker you must be certain that you can
# reverse ANY return value that the function could produce.
# In our examples above, we assumed that, for example, the string:
#   "tic-tac-toe"
# was made via:
#   '-'.join(['tic', 'tac', 'toe'])
# but that is not necessarily the case.
# The following expressions also produce the same result:
#   '-'.join(['tic-tac', 'toe'])
#   '-'.join(['tic', 'tac-toe'])
#   '-'.join(['tic-tac-toe'])
#
# We could have tried to examine `tup` but because it contained non-strings
# we would have had to be careful that we could correctly reverse these
# values. The complexity would have introduced other bugs which would have
# reduced the value of having post-condition checker at all.
# ____________________________________________________________________________

#   _____________________________
# _| Functions that take varargs |____________________________________________
# We shall change the way we pass arguments to the joiner function
# the signature of the new function shall be:
#   def join_args(joiner, *args):
# In order to write a post-condition checker for this we can't say:
#   def check_join_args(joiner, *args, rval):
# Instead, the checker will be called with one more vararg than the original
# function.

def check_join_args(joiner, *args):
    'Post-condition checker for join_args.'
    # The return value is the last vararg
    rval = args[-1]
    # All we can say is that the number of joiners in the return value
    # must be at least (N-1) given N args
    N = len(args) - 1   # (subtract the rval from the args)
    njoiners = rval.count(joiner)
    assert njoiners >= N - 1

@post(check_join_args)
def join_args(joiner, *args):
    'Join the args using the given joiner.'
    return joiner.join(str(a) for a in args)

# Let's run this example in a few different ways
print( 24*'- -' )
print( join_args('-', 'hy', 'phen', 'ated') )
print( join_args('/', '', 'var', 'tmp') )
print( join_args('!', 'a single item') )
print( join_args('-', 0, 800, 'GO', 4, 'IT') )
print( join_args('#') )
print( join_args("'", "don't use a cat", "o", "nine tails") )
print( join_args(',', *(i*i for i in range(5))) )

#   __________________________________
# _| Functions that ONLY take varargs |_______________________________________
# This is no different from a function that takes one or more positional
# arguments plus varargs. The last vararg is the return value.

def check_join_args_dflt(*args):
    'Post-condition checker for join_args_dflt.'
    joiner = get_default_joiner()
    # It is perfectly acceptable to call another checker ...
    check_join_args(joiner, *args)

@post(check_join_args_dflt)
def join_args_dflt(*args):
    'Join the args using the default joiner.'
    joiner = get_default_joiner()
    return joiner.join(str(a) for a in args)

# Let's run this example in a few different ways
print( 24*'- -' )
print( join_args_dflt('This call has', 3, 'arguments') )
print( join_args_dflt('Single-argument') )
print( join_args_dflt() )
print( join_args_dflt('pi', '~=', 355.0/113.0) )
print( join_args_dflt(*(i*i for i in range(5))) )

#   __________________________________
# _| Functions with default arguments |_______________________________________
# Post-checkers for functions with default arguments don't take defaults
# because the decorator uses all args explicitly.
#

def check_wrapstring(s, quotes, rval):
    'Post-condition checker; note that `quotes` is not defaulted.'
    assert rval[0] == quotes[0]
    assert rval[1:-1] == s
    assert rval[-1] == quotes[-1]

@post(check_wrapstring)
def wrapstring(s, quotes='[]'):
    return quotes[0] + s + quotes[-1]

# Let's run this example in a few different ways
print( 24*'- -' )
print( wrapstring('hello world', '"') )
print( wrapstring('bracketed') )
print( wrapstring(quotes='{}', s='curly') )
try:
    print( wrapstring('Guillemet', ['<<', '>>']) )
except AssertionError:
    print('GOTCHA!')
    # determine why this failed and re-write check_wrapstring
    # to handle this case

#   __________________________________
# _| Functions with keyword arguments |_______________________________________

def check_wrapargs(*args, **kw):
    'Post-condition checker for wrapargs and wrapargs2.'
    rval = args[-1]
    quotes = kw.get('quotes', '[]')
    joiner = kw.get('joiner', get_default_joiner())
    assert rval[0] == quotes[0]
    # call another checker
    check_join_args(joiner, *args)
    assert rval[-1] == quotes[-1]

@post(check_wrapargs)
def wrapargs(*args, **kw):
    'Join the args together and wrap in quotes.'
    quotes = kw.get('quotes', '[]')
    s = join_args_dflt(*args)
    return wrapstring(s, quotes)

# Let's run this example in a few different ways
print( 24*'- -' )
print( wrapargs('hello', 'world', quotes='"') )
print( wrapargs('bracketed') )


@post(check_wrapargs)
def wrapargs2(*args, **kw):
    'Join the args together and wrap in quotes.'
    quotes = kw.get('quotes', '[]')
    joiner = kw.get('joiner', get_default_joiner())
    s = join_args(joiner, *args)
    return wrapstring(s, quotes)

# Let's run this example in a few different ways
print( 24*'- -' )
print( wrapargs2('hello', 'world', quotes='"') )
print( wrapargs2(0,800,'GO',4,'IT', joiner='-', quotes='()') )
