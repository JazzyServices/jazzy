# The *bool()* built-in.

The `bool()` built-in is not a function but a type.
Its initialiser can take zero or one arguments.
Before Python3.7, the first parameter was named "x" and could be specified
using either positional or keyword arguments. From 3.7 onwards it is a
positional-only parameter requiring a positional-only argument.
All of our examples in this section assume a version of Python greater than
or equal to 3.8 (the latest version available when this section was written).

## Passing no arguments to the `bool()` built-in.

When no arguments are passed to `bool()`,
the return value is False.

```python
>>> bool()
False
>>>
```

## Passing an argument to the `bool()` built-in.

Expressions that evaluate to zero, or to None, and all empty sequences
are considered False
(so return False when passed to the `bool()` built-in).

```python
>>> falses = None, 0, 0.0, -0.0, 0j, [], (), set(), {}, range(0), '', b''
>>> any(map(bool, falses))
False
>>> bool(b'\0'[0])
False
>>>
```

Range objects that would yield no values
(because the range end has already been reached)
are considered False.

```python
>>> bool(range(-1))
False
>>> bool(range(2,2))
False
>>> bool(range(2,4,-1))
False
>>>
```

All other built-in values are considered True.

```python
>>> some_trues = True, 1, 42, -40, NotImplemented, ...
>>> all(map(bool, some_trues))
True
>>> import math
>>> float_trues = 1.0, 1e-34, math.nan, math.inf
>>> all(map(bool, float_trues))
True
>>> complex_trues = 1+0j, 0+1j, 1+1j
>>> all(map(bool, complex_trues))
True
>>>
```

Non-empty built-in sequences, even if they only contain False values,
are considered True.
Iterators and generator functions, even if they would yield no values,
are considered True. (Compare this to empty ranges above).

```python
>>> all(map(bool, ([False], (0,), {False}, {0:0}, range(1), '\0', b'\0')))
True
>>> bool(iter(''))
True
>>> bool(i for i in '')
True
>>>
```

All modules, classes, functions, built-in exceptions, *etc* are considered True.

```python
>>> bool(__builtins__)
True
>>> bool(bool)
True
>>> bool(bool.bit_length)
True
>>> bool(False.bit_length)
True
>>> bool(lambda _:0)
True
>>> bool(KeyError(0))
True
>>>
```

## Objects with a `__bool__` method.

If an object's class has a `__bool__` method
it will be used by the `bool()` built-in
and by the `if` and `while` statements.

The example below defines an exception with a `__bool__` method.
Unlike built-in exceptions, its truth-value may be False.

```python
>>> class Boo(Exception):
        def __bool__(my):
            return bool(my.args and my.args[0])

>>> bool(Boo())
False
>>> bool(Boo(0))
False
>>> bool(Boo(1))
True
>>> bool(Boo([]))
False
>>> if not Boo(): print("Exception is Falsey.")

Exception is Falsey.
>>>
```

In the next example, we define a class whose objects are only True
some of the time. (This is done by modifying the object's `value`
on each call to `__bool__`.)

```python
>>> class BitTrue:
        def __init__(my, value):
            my.value = abs(int(value))
        def __bool__(my):
            result = bool(my.value & 1)
            my.value >>= 1
            return result

>>> bit_true = BitTrue(0b00010111)
>>> while bit_true:
        print('TRUE', 2 * bit_true.value + 1)

TRUE 23
TRUE 11
TRUE 5
>>>
```


## Objects with a `__len__` method.

If an object's class has a `__len__` method but no `__bool__` method
it will be used by the `bool()` built-in
and by the `if` and `while` statements.

The example below defines a subclass of `itertools.repeat`
that implements the `__len__` method
so that the object will be False if its iterator is exhausted.

```python
>>> import itertools
>>> class Stars(itertools.repeat):
        def __new__(cls, times):
            return super().__new__(cls, '*', times)
        def __len__(my):
            return my.__length_hint__()

>>> stars = Stars(3)
>>> bool(stars)
True
>>> while stars:
        print(next(stars), 'bullet', 3 - len(stars))

* bullet 1
* bullet 2
* bullet 3
>>> bool(stars)
False
>>>
```

