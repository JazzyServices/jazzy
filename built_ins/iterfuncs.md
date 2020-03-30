# Built-in Functions Processing Iterable Types

There are several built-in functions that take an iterable as an argument.

- len()
- all() and any()
- sum()
- sorted()
- min() and max()
- iter()
- next()


# The *len()* built-in.

The `len()` built-in takes one positional argument and does not accept keyword arguments. It returns an integer >= 0 which is the number of items in the given object. The argument object must have a `__len__` method.

```python
>>> len('cauliflower')
11
>>> len(globals())
7
>>> len(range(10,100))
90
>>>
```

In CPython, the length is required to be at most `sys.maxsize`.
If the length is larger than `sys.maxsize`, calling `len()` may raise `OverflowError`.

```python
>>> import sys
>>> len(range(sys.maxsize + 1))
Traceback (most recent call last):
  File "<pyshell#2>", line 1, in <module>
    len(range(sys.maxsize + 1))
OverflowError: Python int too large to convert to C ssize_t
>>>
```

Objects without a `__len__` method raise a `TypeError`.

```python
>>> len(slice(0,10,1))
Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    len(slice(0,10,1))
TypeError: object of type 'slice' has no len()
>>> len(open('/etc/manpaths'))
Traceback (most recent call last):
  File "<pyshell#2>", line 1, in <module>
    len(open('/etc/manpaths'))
TypeError: object of type '_io.TextIOWrapper' has no len()
>>>
```


# The *any()* and *all()* built-ins.

The `any()` and `all()` built-ins take one positional argument (an iterable)
and do not accept keyword arguments.
They determine the *truth value* of each item in the iterable in turn until
one of the items negates the function's predicate, or until the end of the iterable.
That is, the `any()` and `all()` built-ins are *short-circuit* operations.
- the `any()` built-in returns False *unless* it encounters an item that is True.
- the `all()` built-in returns True *unless* it encounters an item that is False.

The implication of this is that,
for an empty iterable argument,
the `any()` built-in returns False, and
the `all()` built-in returns True.

```python
>>> any([])
False
>>> all([])
True
>>>
```

To demonstrate that the `any()` and `all()` built-ins are short-circuit operations we can see how much of an iterator each of them consumes.

```python
>>> it = iter([1,0,1])
>>> any(it)
True
>>> print(*it)
0 1
>>>
```

```python
>>> it = iter([1,0,1])
>>> all(it)
False
>>> print(*it)
1
>>>
```

Note that the `any()` built-in only consumes the first `1`
and the `all()` built-in consumes `[1, 0]`.


# The *sum()* built-in.

The `sum()` built-in takes one mandatory positional argument (an iterable)
and one optional argument (`start`) which may be specified either positionally
or via a keyword.
The `sum()` built-in returns the sum of all the items in the iterable
plus the value of `start` which defaults to zero.
The return type depends on the types of items in the iterable.

```python
>>> sum(range(10))
45
>>> sum(range(10), start=10)
55
>>> sum(b'\x89PNG\r\n\x1a\n')
425
>>> sum((1/7, 2/7, 3/7, 4/7, 5/7, 6/7))
3.0
>>> sum([1.0, 0+1j, 1-1j, -2])
0j
>>>
```

## The *start* argument.

The `start` argument may be any type apart from `str`, `bytes` or `bytearray`.
This is not because adding strings is disallowed but because Python is
nannying you into having to do string concatenation in a different
(but admittedly more efficient) way.
This is generally against Python's philosophy of The Programmer is Always Right.
No other part of the Python eco-system deliberately prevents you performing
inefficient tasks.
*E.g.* `functools.reduce` allows you to do it.

```python
>>> sum(['holy', 'hand', 'grenade'], '')
Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    sum(['holy', 'hand', 'grenade'], '')
TypeError: sum() can't sum strings [use ''.join(seq) instead]
>>> import functools, operator
>>> functools.reduce(operator.add, ['holy', 'hand', 'grenade'], '')
'holyhandgrenade'
>>> sum(['holy', 'hand', 'grenade'], type('Anon', (), {'__add__':lambda _,b:b})())
'holyhandgrenade'
>>>
```

The `sum()` built-in uses an object's `__add__` (or `__radd__`) method to
calculate its return value; therefore unless these methods support
operands of the types of all the iterable's items, an expection will be raised.
For example, `list.__add__` supports an argument that is another list but not
arguments of other types.

```python
>>> sum(([1], [2, 3], [5, 8, 13]), [])
[1, 2, 3, 5, 8, 13]
>>> sum(([1], [2, 3], [5, 8, 13], 21), [])
Traceback (most recent call last):
  File "<pyshell#2>", line 1, in <module>
    sum(([1], [2, 3], [5, 8, 13], 21), [])
TypeError: can only concatenate list (not "int") to list
>>>
```

If a class' `__add__` method supports arbitrary types,
then we can "sum" heterogenous iterables.

```python
>>> import collections
>>> class MyCounter:
        def __init__(my):
            my.counter = collections.Counter()
        def __add__(my, other):
            my.counter += {other:1}
            return my

>>> total = sum(['str', 1, 3.14, None, ..., min, 1.0, True], MyCounter())
>>> total.counter
Counter({1: 3, 'str': 1, 3.14: 1, None: 1, Ellipsis: 1, <built-in function min>: 1})
>>>
```


# The *sorted()* built-in.

The `sorted()` built-in takes one positional argument (an iterable)
and up to two keyword arguments (`key`, `reverse`).
It returns a new list containing the items of the iterable in sorted order.

```python
>>> sorted('cauliflower')
['a', 'c', 'e', 'f', 'i', 'l', 'l', 'o', 'r', 'u', 'w']
>>> sorted(b'\x89PNG\r\n\x1a\n')
[10, 10, 13, 26, 71, 78, 80, 137]
>>> sorted({'king': 'Henry VIII', 'wife': 'Anne Boleyn', 'child': 'Elizabeth'})
['child', 'king', 'wife']
>>> sorted(i%13 for i in range(0,70,10))
[0, 1, 4, 7, 8, 10, 11]
>>>
```

If the iterable contains NaNs,
then the returned list may not be as expected.
This is because NaN is neither greater than nor less than a real number,
so when the sorting algorithm compares NaN to a number it doesn't move the
compared number within the sort-space.

```python
>>> sorted([4, 2, 8, math.nan, 5, 7, 1])
[1, 2, 4, 5, 8, nan, 7]
>>>
```

## The *reverse* keyword.

If the `reverse` keyword argument is passed to the `sorted()` built-in
it must be an integer.
If the value of the integer is non-zero, the returned list is sorted in reverse order.

```python
>>> sorted(range(10), reverse=True)
[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
>>> sorted(range(10), reverse=1)
[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
>>> sorted(range(10), reverse=b'\n'[0])
[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
>>>
```

## The *key* keyword.

If the `key` keyword argument is passed to the `sorted()` built-in
it must be either None
(in which case the items are compared directly as if the `key` argument were not given)
or a callable taking one argument.
The callable is passed each item from the iterable in turn
and returns the *sort key* for that item.
For example, if each item is a 2-tuple and we wished to order by the 2nd member of the tuple, the sort key is `item[1]`; so the callable needs to return that.

In the snippet below, we produce a list of a dictionary's key-value pairs
sorted by value. The callable is a lambda that returns `item[1]`.

```python
>>> d = dict(name='Arthur', rank='King', quest='Holy Grail', sword='Excalibur')
>>> key = lambda item: item[1]
>>> result = sorted(d.items(), key=key)
>>> for pair in result:
        print('%5s %s' % pair)

 name Arthur
sword Excalibur
quest Holy Grail
 rank King
>>>
```

The value returned by the callable does not have to appear in the sorted output.
The example below sorts numbers by their binary representation;
the order being `0b0 0b1 0b10 0b100 0b1000 0b1001 0b101` *etc.*

```python
>>> sorted(range(16), key=bin)
[0, 1, 2, 4, 8, 9, 5, 10, 11, 3, 6, 12, 13, 7, 14, 15]
>>>
```


# The *min()* and *max()* built-ins.

The `min()` and `max()` built-ins differ from other built-in functions in that
they accept either an iterable *or* an arbitrary number of positional arguments
in lieu of the iterable. They also accept two keyword arguments (`key`, `default`).

```python
>>> min(4, 2, 8, 5, 7, 1, 4, 2)
1
>>> min([4, 2, 8, 5, 7, 1, 4, 2])
1
>>> min('hello')
'e'
>>> min('hello', 'world')
'hello'
>>>
```

There needs to be at least two positional arguments otherwise the first (only)
argument is treated as the iterable.

```python
>>> max(5/8, 8/13)
0.625
>>> max(5/8, )
Traceback (most recent call last):
  File "<pyshell#2>", line 1, in <module>
    max(5/8, )
TypeError: 'float' object is not iterable
>>>
```

If multiple items are maximal/minimal, the first one encountered is returned.

```python
>>> max(0, False, 0.0, -0.0)
0
>>> max(False, 0, -0.0, 0.0)
False
>>>
```

## The *key* keyword argument.

The `key` keyword argument has the same semantics as for the `sorted()` built-in above.
It must be either None
(in which case the items are compared directly as if the `key` argument were not given)
or a callable taking one argument.
The callable is passed each item from the iterable in turn
and returns the *comparison key* for that item.

```python
>>> d = dict(name='Arthur', rank='King', quest='Holy Grail', sword='Excalibur')
>>> key = lambda item: item[1]
>>> min(d.items(), key=key)
('name', 'Arthur')
>>> max(d.items(), key=key)
('rank', 'King')
>>>
```

## The *default* keyword argument.

The `default` keyword argument is only allowed if there is exactly one positional argument. Without it, an empty iterable passed to `min()` or `max()` would
raise an exception.
If the `default` keyword argument is given and the iterable is empty,
the value of the `default` is returned.

```python
>>> max(b'')
Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    max(b'')
ValueError: max() arg is an empty sequence
>>> max(b'', default=-1)
-1
>>> max(b'\0', default=-1)
0
>>>
```


# The *iter()* built-in.

The `iter()` built-in takes one or two positional arguments.
It does not accept keyword arguments.
The returned object is always an *iterator*
(it supports the [*iterator protocol*](https://docs.python.org/3.8/library/stdtypes.html#typeiter).)
But the exact type of object it returns depends on the type of the first argument.

```python
>>> iter('Arthur')
<str_iterator object at 0x10b8aac70>
>>> iter([1,2,5,'three sir',3])
<list_iterator object at 0x10b8d52b0>
>>> iter(input, '')
<callable_iterator object at 0x10b8aac70>
>>> iter('Galahad').__class__ == iter('Lancelot').__class__
True
>>> iter('Galahad').__class__ == iter(b'Lancelot').__class__
False
>>>
```

The `iter()` built-in function is two functions in disguise
(usually the sign of an anti-pattern).
The first form of `iter()` takes one positional argument that must be an iterable.
The second form of `iter()` takes two positional arguments the first of which must be a callable.

## The *iter()* built-in with one argument.

If the `iter()` built-in is passed exactly one argument,
that argument must be an iterable (it has a `__iter__` method),
or it must have a `__getitem__` method taking sequential integer arguments starting from zero.
All of the built-in sequence types are also iterables, so the second of the accepted types given above only applies to custom types.

The example below creates a new sequence type `Squares` that has
no `__iter__` method,
only a `__getitem__` method.
An object of type `Squares` is an infinite sequence of the squares of the
natural numbers.
The example creates an iterator over the sequence,
and calls `next()` on the iterator twelve times (once for each letter of the string `"Monty Python"`).

```python
>>> Squares = type('Squares', (), {'__getitem__':lambda _,x:x*x})
>>> sqiter = iter(Squares())
>>> [next(sqiter) for _ in 'Monty Python']
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121]
>>>
```

## The *iter()* built-in with two arguments.

If the `iter()` built-in is passed two arguments,
the first must be a callable taking no arguments,
the second is a value (the "sentinel") that the callable will return to stop the iterator.

In the example below, we create an iterator to read a line at a time from
`sys.stdin` until it gets a blank line.
The callable is `sys.stdin.readline` and the sentinel is `"\n"`.

```python
>>> import sys
>>> reader = iter(sys.stdin.readline, '\n')
>>> list(reader)
first line
second
 indented
last

['first line\n', 'second\n', ' indented\n', 'last\n']
>>>
```


# The *next()* built-in.

The `next()` built-in takes one or two positional arguments.
It does not accept keyword arguments.
The first argument must be an iterator (such as is returned by the
`iter()`, `enumerate()`, `map()`, `filter()` or `zip()` built-ins.)
The `next()` built-in returns the next item in the given iterator unless the
iterator is exhausted.
If the iterator is exhausted, `next()` will:
- return the value of the second argument, or
- raise `StopIteration` if no second argument was given.

```python
>>> next(zip('ABC', '123'))
('A', '1')
>>> next(map(bin, b'\n'))
'0b1010'
>>> next(enumerate('ABC'))
(0, 'A')
>>> next(filter(None, bytes(8)), 'No bytes')
'No bytes'
>>> next(filter(None, bytes(8)))
Traceback (most recent call last):
  File "<pyshell#5>", line 1, in <module>
    next(filter(None, bytes(8)))
StopIteration
>>>
```
