# The *str()* built-in.

The `str` built-in is not a function but a type.
Its initialiser can take up to three arguments (`object`, `encoding`, `errors`),
which, like normal Python functions, can be specified as positional or keyword arguments.

| object | encoding | errors | returns
|--------|----------|--------|--------
| absent |   ANY    |  ANY   | the empty string
| present|  absent  | absent | string representation of the object
| bytes  |  absent  | present| decoded bytes using the default encoding, errors handled using the given scheme
| bytes  | present  | absent | decoded bytes using the given encoding, errors handled using the default scheme (`strict`)
| bytes  | present  | present| decoded bytes using the given encoding, errors handled using the given scheme

When either `encoding` or `errors` is present, `object` must be a bytes-like object (`bytes`, `bytearray`, *etc*). All of the examples below use bytes objects,
but they could equally have used a bytearray, memoryview, *etc*.

The `encoding` and `errors` arguments must be strings,
even if they are unused by `str()`.
The `encoding` argument is unused when the `object` argument is an empty bytestring (which is the default value for the `object` argument in this scenario).
The `errors` argument is only used when the decoder encounters an error.

**This means that an invalid `errors` value might go unnoticed in the code, only to be discovered when an actual error needs to be handled.**


```python
>>> str(encoding='')
''
>>> str(B'', encoding='acsii')  # note mis-spelling
''
>>> str(errors='')
''
>>> str(b'Bush hid the facts', errors='repalce')
'Bush hid the facts'
>>>
```


## `encoding` is case insensitive (sort of).

The `encoding` argument is, according to the Python documentation,
case insensitive. (Also, hyphens and underscores are interchangeable.)

```python
>>> str(b'Bush hid the facts', encoding='ASCII')
'Bush hid the facts'
>>> str(b'Bush hid the facts', encoding='GreeK')
'Bush hid the facts'
>>> str(b'Bush hid the facts', encoding='Utf_16-Le')
'畂桳栠摩琠敨映捡獴'
>>>
```

However, it is not truly case-insensitive.
Characters outside the ASCII range that have a case-insensitive match to
ASCII characters (such as
U+017F LATIN SMALL LETTER LONG S, and
U+212A KELVIN SIGN
) raise an exception when used in the `encoding` argument.
If the caller explicitly case-folds the argument, however, the value is accepted
(as long as the folded string matches a valid encoder).

```python
>>> str(b'Bush hid the facts', encoding='A\u017fcii')
Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    str(b'Bush hid the facts', encoding='A\u017fcii')
LookupError: unknown encoding: Aſcii
>>> str(b'Bush hid the facts', encoding='A\u017fcii'.casefold())
'Bush hid the facts'
>>> str(b'Bush hid the facts', encoding='Gree\u212a')
Traceback (most recent call last):
  File "<pyshell#3>", line 1, in <module>
    str(b'Bush hid the facts', encoding='Gree\u212a')
LookupError: unknown encoding: GreeK
>>> str(b'Bush hid the facts', encoding='Gree\u212a'.casefold())
'Bush hid the facts'
>>>
```

This demonstrates that the claim to be case-insensitive is not correct.
Even after all these years, Python is still not a truly Unicode-aware beast.


## `errors` is always case sensitive.

The `errors` argument (when used) must exactly match one of the registered
error handlers (such as `strict`, `ignore`, `replace`, *etc*).
(Note that in the examples below we use the ill-formed UTF-8 sequence
`"\xc0\xaf"` or the out-of-range UTF-32BE sequence `"\x00\x11\x00\x00"`
to generate a decoding error)

```python
>>> str(B'\xC0\xAF', errors='STRICT')
Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    str(B'\xC0\xAF', errors='STRICT')
LookupError: unknown error handler name 'STRICT'
```

The names of registered error handlers must be strings;
but it is also worth pointing out that it is possible to register an error handler whose name is the empty string.
(The code below registers a lambda rather than a function but it correctly
returns the replacement text (a '?' character)
and the position from which to continue decoding.)

```python
>>> import codecs
>>> codecs.register_error('', lambda e:('?', e.end))

>>> str(b'[\xc0\xfa]', errors='')
'[??]'
>>>
```


## The behaviour of the standard `errors` handlers.

There are several standard error handlers that can be used by the `str()` built-in.

`strict`
: raises a UnicodeDecodeError if an error is encountered

`ignore`
: throws away any bytes that cause an error

```python
>>> str(b'[\xc0\xfa]', errors='ignore')
'[]'
>>>
```

`replace`
: replaces bytes or byte sequences that cause an error with the Unicode replacement character (U+FFFD)

```python
>>> str(b'[\xc0\xfa]', errors='replace')
'[��]'
>>> str(b'\x00\x00\x00[\x00\x11\x00\x00\x00\x00\x00]', encoding='utf-32be', errors='replace')
'[�]'
>>>
```

`backslashreplace`
: replaces bytes that cause an error with backslashed escape sequences

```python
>>> str(b'[\xc0\xfa]', errors='backslashreplace')
'[\\xc0\\xfa]'
>>> str(b'\x00\x00\x00[\x00\x11\x00]\x00\x00\x00]', encoding='utf-32be', errors='backslashreplace')
'[\\x00\\x11\\x00\\x5d]'
>>>
```

`surrogateescape`
: replaces bytes that cause an error with a surrogate in the range U+DC80 to U+DCFF. (Note: this allows for a reversible re-encoding) (Also note: this scheme may only be useful for certain encodings such as UTF-8)

```python
>>> str(b'[\xc0\xfa]', errors='surrogateescape')
'[\udcc0\udcfa]'
>>>
```

`surrogatepass`
: allows the decoding of isolated surrogates, but otherwise behaves like `strict`.


# Calling `str()` with neither `errors` nor `encoding`.

If `str()` is called with a single argument, even a bytes argument,
then no decoding is performed.
Instead, the argument's `__str__` (or `__repr__`) method is called.
For a bytes object this returns a string that looks like a bytes literal.

```python
>>> str(b'\x41')
"b'A'"
>>>
```

For the built-in constants, `str()` returns the expected literal string.

```python
>>> str(None)
'None'
>>> str(1==1)
'True'
>>> str(1!=1)
'False'
>>> str(NotImplemented)
'NotImplemented'
>>> str(...)
'Ellipsis'
>>> str(__debug__)
'True'
>>>
```


## Passing an `int` to the `str()` built-in.

When passing an `int` argument to `str()`, Python returns the decimal representation of that `int`.

```python
>>> str(000)
'0'
>>> str(+42)
'42'
>>> str(- 1)
'-1'
>>> str(0x2a)
'42'
>>> str(-0b00101010)
'-42'
>>> str(0o052)
'42'
>>> str(1<<31)
'2147483648'
>>> str(3**3**3)
'7625597484987'
>>> str(True - False)
'1'
>>>
```


## Passing a `float` to the `str()` built-in.

When passing a `float` argument to `str()`,
Python either returns its normal decimal representation
or, if the number is too large (or too small), its representation in exponent format. Since floating-point numbers have limited precision, a limited number of
digits are returned; as can be seen in the Christmas Tree algorithm below.

```python
>>> for power in range(20):
        x = 10**power
        print(str(x + 1/x))

2.0
10.1
100.01
1000.001
10000.0001
100000.00001
1000000.000001
10000000.0000001
100000000.00000001
1000000000.0
10000000000.0
100000000000.0
1000000000000.0
10000000000000.0
100000000000000.0
1000000000000000.0
1e+16
1e+17
1e+18
1e+19
>>>
```

Python is dependent on the underlying C and hardware implementations;
which means that a negative zero may be possible.
If a negative zero is passed to `str()` the sign will be returned in the string.

```python
>>> str(-0.)
'-0.0'
>>> str(-1.0 * 0.0)
'-0.0'
>>>
```

Infinities and NaN produce the strings `inf`, `-inf` and `nan`.

```python
>>> import math
>>> str(math.inf)
'inf'
>>> str(-math.inf)
'-inf'
>>> str(math.nan)
'nan'
>>> str(-math.nan)
'nan'
>>>
```


## Passing a `complex` to the `str()` built-in.

The formatting of `complex` numbers by the `str()` built-in
is similar to that of `float` except that Python omits the fractional part
of whole numbers and omits the real part if it is zero.

```python
>>> str(1.2 + 3.4j)
'(1.2+3.4j)'
>>> str(1.0 + 3.4j)
'(1+3.4j)'
>>> str(1.2 + 3.0j)
'(1.2+3j)'
>>> str(1.0 + 3.0j)
'(1+3j)'
>>> str(0.0 + 3.0j)
'3j'
>>> str(1.0 + 0.0j)
'(1+0j)'
>>> str(0.0 + 0.0j)
'0j'
>>>
```


## Passing a list to the `str()` built-in.

When a list is passed as the only argument to `str()`
the returned string resembles a
["list display"](https://docs.python.org/3.8/reference/expressions.html#displays-for-lists-sets-and-dictionaries)
with each member of the list represented by its own `str()` value.

```python
>>> str([])
'[]'
>>> str([0])
'[0]'
>>> str([0, 0.0, 0+0j, None, 0>0, "zero", ...])
"[0, 0.0, 0j, None, False, 'zero', Ellipsis]"
>>> str([1., 0b1, "one", 1j, 1==1, NotImplemented])
"[1.0, 1, 'one', 1j, True, NotImplemented]"
>>>
```


## Passing a dictionary to the `str()` built-in.

When a dictionary is passed as the only argument to `str()`
the returned string resembles a
["dictionary display"](https://docs.python.org/3.8/reference/expressions.html#displays-for-lists-sets-and-dictionaries)
with each key and each value of the dictionary represented by its own `str()` value.

```python
>>> str({})
'{}'
>>> str({"zero": [0, 0.0, 0+0j], None: 0>0})
"{'zero': [0, 0.0, 0j], None: False}"
>>>
```


## Passing a tuple to the `str()` built-in.

Tuples behave like lists, with a few differences:

- parentheses instead of square brackets (obviously)
- a 1-member tuple (a 1-tuple) includes a trailing comma

```python
>>> tup = 1., 0b1, "one", 1j, 1==1, NotImplemented
>>> str(tup[:0])
'()'
>>> str(tup[:1])
'(1.0,)'
>>> str(tup)
"(1.0, 1, 'one', 1j, True, NotImplemented)"
>>>
```

Tuples are defined by the comma and not the parentheses,
but since function calls also use commas, when passing a tuple literal
(expression list)
to `str()`, the expressions of the tuple need to be enclosed in parentheses.

```python
>>> str(b'ytes', 'utf-8', 'strict')
'ytes'
>>> str((b'ytes', 'utf-8', 'strict'))
"(b'ytes', 'utf-8', 'strict')"
>>>
```


## Passing a set to the `str()` built-in.

Sets behave like lists, with a few differences:

- curly braces instead of square brackets (obviously)
- the empty set returns the string `set()` to distinguish it from an empty dictionary

```python
>>> set_of_falses = {0, 0.0, 0+0j, False, (), None,}
>>> str(set_of_falses)
'{0, (), None}'
>>> str({0, 0.0, False, 0+0j})
'{0}'
>>> str(set_of_falses - set_of_falses)
'set()'
>>>
```


## Passing a range to the `str()` built-in.

When a range is passed as the only argument to `str()`
the returned string resembles an expression that would produce a range with
the same start, stop, and step. The string always includes the start value,
but only includes the step if it is not equal to one.

```python
>>> str(range(2))
'range(0, 2)'
>>> str(range(0,2))
'range(0, 2)'
>>> str(range(0,2,1))
'range(0, 2)'
>>> str(range(0,2,2))
'range(0, 2, 2)'
>>> str(range(False, True, True))
'range(False, True)'
>>>
```


## Passing a slice to the `str()` built-in.

When a slice is passed as the only argument to `str()`
the returned string resembles an expression that would produce a slice with
the same start, stop, and step. The string includes all three arguments
even if start and step are None.

```python
>>> str(slice(2))
'slice(None, 2, None)'
>>> str(slice(0,2))
'slice(0, 2, None)'
>>> str(slice(0,2,1))
'slice(0, 2, 1)'
>>>
```


## Passing recursive objects to the `str()` built-in.

It is possible in Python to create sequences that contain themselves.
When converting such objects to string, Python prevents recursive output
by replacing already-seen, recursed objects with ellipses.

In the example below, we have a tuple containing a list and a dictionary.
The dictionary also contains the list.

```python
>>> alist = []
>>> adict = { 'list': alist }
>>> atuple = alist, adict
>>> str(atuple)
"([], {'list': []})"
>>>
```

If we now insert the outer tuple into the list and into the dictionary,
and add the dictionary to itself, we can see how Python represents this
recursive structure.

```python
>>> alist.append(atuple)
>>> adict['tuple'] = atuple
>>> adict['dict'] = adict
>>> str(atuple)
"([(...)], {'list': [(...)], 'tuple': (...), 'dict': {...}})"
>>>
```


## Passing other built-in types to the `str()` built-in.

The return value from `str()` when it is passed an object of certain built-in types
resembles the expression that might have been used to construct that object.
We say "might have been", because objects don't remember how they were
constructed; but given their current value an expression can be formed that
would produce an object of that value.

A `frozenset` object is represented as if it were constructed from a `set`.

```python
>>> str(frozenset([7,1,4,5]))
'frozenset({1, 4, 5, 7})'
>>>
```

A `bytearray` object is represented as if it were constructed from `bytes`.

```python
>>> str(bytearray([7,1,4,5]))
"bytearray(b'\\x07\\x01\\x04\\x05')"
>>>
```

Objects of other built-in types produce a string consisting of angle brackets
within which is the name of the type of the object and possibly its address
and other identifying information.

```python
>>> str(__builtins__)
"<module 'builtins' (built-in)>"
>>> str(min)
'<built-in function min>'
>>> str(lambda _:...)
'<function <lambda> at 0x10700a950>'
>>> str(float.hex)
"<method 'hex' of 'float' objects>"
>>> str((1.).hex)
'<built-in method hex of float object at 0x103f16ca8>'
>>> str(object)
"<class 'object'>"
>>> str(memoryview(b'\xc2\xb5'))
'<memory at 0x106fb8408>'
>>> str(map(None, []))
'<map object at 0x1053d2780>'
>>> str(enumerate(''))
'<enumerate object at 0x105036630>'
>>> str(iter(''))
'<str_iterator object at 0x106feaeb8>'
>>> str(iter(range(2)))
'<range_iterator object at 0x106fb4ed0>'
>>> str(open('/dev/null', 'rb'))
"<_io.BufferedReader name='/dev/null'>"
>>>
```


## Passing an exception to the `str()` built-in.

Although we have discussed "other types" above,
we are now mentioning exceptions because exceptions can be constructed with
any type. So the return value from `str()` depends on how the exception was made.

```python
>>> str(Exception('bare exception'))
'bare exception'
>>> str(Exception(...))
'Ellipsis'
>>> str(Exception(b'ytes', 'utf-8', 'strict'))
"(b'ytes', 'utf-8', 'strict')"
>>> str(Exception(int))
"<class 'int'>"
>>>
```

Some exceptions provide more information than just the object with which they
were constructed.

```python
>>> try:
    str(b'\xc0\xaf', 'U8')
except UnicodeError as unicorn:
    s = str(unicorn)

>>> s
"'utf-8' codec can't decode byte 0xc0 in position 0: invalid start byte"
>>>
```
