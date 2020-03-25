# Iterable Types

Python defines several built-in iterable types:
- str
- bytes and bytearray
- memoryview
- range
- slice
- dict
- list
- tuple
- set and frozenset


# The *bytes()* and *bytearray()* built-ins.

The `bytes()` and `bytearray()` built-ins are not functions but types.
Both types are sequences of integers in the range(0, 256).
The `bytes` type is *immutable*.
The `bytearray` type is *mutable*.

The `bytes()` and `bytearray()` built-ins take up to three arguments:
- `source`: an int, iterable or string
- `encoding`: a string. Must be given if `source` is a string. Otherwise, must not be given.
- `errors`: a string. May be given if `source` is a string. Otherwise, must not be given.

## Passing no arguments to the `bytes` or `bytearray` built-ins.

When no arguments are given,
an empty `bytes` or `bytearray` object is returned.

```python
>>> bytes()
b''
>>> bytearray()
bytearray(b'')
>>>
```

## Passing an `int` to the `bytes` or `bytearray` built-ins.

When the `source` argument is an `int`
(or has an `__index__` method),
no other arguments may be given.
A new `bytes` or `bytearray` object is returned with that number of elements
all initialised with null bytes.

```python
>>> bytes(True)
b'\x00'
>>> bytes(8)
b'\x00\x00\x00\x00\x00\x00\x00\x00'
>>> bytes(b'\n'[0])
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
>>> bytes(type('A', (), dict(__index__=lambda _:4))())
b'\x00\x00\x00\x00'
>>>
```

Passing zero as the `source` argument returns an empty
`bytes` or `bytearray` object.
Passing a negative number raises an exception.

```python
>>> bytearray(0)
bytearray(b'')
>>> bytes(False)
b''
>>> bytearray(-1)
Traceback (most recent call last):
  File "<pyshell#3>", line 1, in <module>
    bytearray(-1)
ValueError: negative count
>>>
```

## Passing a non-string iterable to the `bytes` or `bytearray` built-ins.

When the `source` argument is an iterable that is not a `str`,
no other arguments may be given.
`source` must be an iterable of integers in the range(0, 256)

```python
>>> bytearray([137, 80, 78, 71, 13, 10, 26, 10])
bytearray(b'\x89PNG\r\n\x1a\n')
>>> bytearray((137, 80, 78, 71, 13, 10, 26, 10))
bytearray(b'\x89PNG\r\n\x1a\n')
>>> bytearray({137, 80, 78, 71, 13, 10, 26, 10})
bytearray(b'G\x89\n\rNP\x1a')
>>> bytearray({80: 'eighty', 78: 'days', 71: 'later'})
bytearray(b'PNG')
>>> bytearray(range(48, 58))
bytearray(b'0123456789')
>>> import random
>>> bytearray(random.randint(0, 255) for _ in range(8))
bytearray(b'\x11\xbb`\xeex(z\x8d')
>>>
```

## Passing a buffer to the `bytes` or `bytearray` built-ins.

When the `source` argument is a buffer,
no other arguments may be given.
A new `bytes` or `bytearray` is returned that is a *copy* of the bytes of
the given buffer.

```python
>>> original = bytearray([137, 80, 78, 71, 13, 10, 26, 10])
>>> copy = bytearray(original)
>>> original[2] = 73
>>> original
bytearray(b'\x89PIG\r\n\x1a\n')
>>> copy
bytearray(b'\x89PNG\r\n\x1a\n')
>>>
```

When the buffer is a sequence of unsigned bytes, the behaviour is
indistinguishable from being passed an iterable of integers.
However, it is the underlying bytes of the buffer
that form the sequence.
This can be seen when the buffer is an `array` of some other type.

```python
>>> bytearray(array.array('b', [0, 127, -128, -1]))
bytearray(b'\x00\x7f\x80\xff')
>>> bytearray(array('h', [383, -2]))
bytearray(b'\x7f\x01\xfe\xff')
>>>
```

## Passing a string to the `bytes` or `bytearray` built-ins.

When the `source` argument is a string,
the `encoding` argument must be given
and must be a valid encoding
(unlike for the `str()` built-in which doesn't use the `encoding` parameter
if no decoding is performed.)
The `errors` argument is optional, and like for the `str()` built-in,
is only required to be valid if it is used.

```python
>>> bytes(source='')
Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    bytes(source='')
TypeError: string argument without an encoding
>>> bytes(source='', encoding='nonsuch')
Traceback (most recent call last):
  File "<pyshell#2>", line 1, in <module>
    bytes(source='', encoding='nonsuch')
LookupError: unknown encoding: nonsuch
>>> bytes(source='', encoding='utf8', errors='nonsuch')
b''
>>>
```

As with the `str()` built-in,
the `encoding` argument is pseudo-case-insensitive
and allows enclosing whitespace
and sequences of whitespace, hyphens or underscores where a single hyphen or
underscore appears in the encoding name or one of its aliases.

```python
>>> bytes('bob', 'iso8859-1')
b'bob'
>>> bytes('bob', 'ISO-8859-1')
b'bob'
>>> bytes('bob', ' iso\n8859\t1 ')
b'bob'
>>> bytes('bob', '- -iso- -8859- -1- -')
b'bob'
>>> bytes('bob', '_____iso___8859___1___')
b'bob'
>>>
```

The `errors` argument (when used) must exactly match one of the registered
error handlers (such as `strict`, `ignore`, `replace`, *etc*).
Encoding from string to bytes supports additional error-handling than
decoding from bytes to string.

```python
>>> bytes('pa\u017fs', 'latin1', 'ignore')
b'pas'
>>> bytes('pa\u017fs', 'latin1', 'replace')
b'pa?s'
>>> bytes('pa\u017fs', 'latin1', 'namereplace')
b'pa\\N{LATIN SMALL LETTER LONG S}s'
>>> bytes('pa\u017fs', 'latin1', 'xmlcharrefreplace')
b'pa&#383;s'
>>>
```

## The `fromhex` classmethod.

The `bytes` and `bytearray` classes have a `fromhex` classmethod
that can be used to make a new object from a string of hex digits.
The hex digits must be in pairs and the pairs may be separated by ASCII
whitespace.

```python
>>> bytes.fromhex('89 50 4E 47 0D 0A 1A 0A\f')
b'\x89PNG\r\n\x1a\n'
>>> bytearray.fromhex('8950 4E47\t0D0A 1A0A')
bytearray(b'\x89PNG\r\n\x1a\n')
>>>
```


# The *memoryview()* built-in.

The `memoryview()` built-in is not a function but a type.
It takes one argument which must support the buffer protocol.
The argument may be given as a positional argument or as a keyword argument.

```python
>>> memoryview(b'bob')
<memory at 0x106ab0340>
>>> memoryview(object=b'bob')
<memory at 0x106ab0640>
>>>
```

The `memoryview` is immutable if the underlying object is immutable; and
the `memoryview` is mutable if the underlying object is mutable.

```python
>>> b = bytearray(b'\x89P')
>>> view = memoryview(b)
>>> view[0] = 0x59
>>> b
bytearray(b'YP')
>>>
```

However, the underlying type may not be re-sizeable if it has a `memoryview`
viewing it.

```python
>>> b.extend([0x30, 0x31])
Traceback (most recent call last):
  File "<pyshell#1209>", line 1, in <module>
    b.extend([0x30, 0x31])
BufferError: Existing exports of data: object cannot be re-sized
>>> view.release()
>>> b.extend([0x30, 0x31])
>>> b
bytearray(b'YP01')
>>>
```


# The *range()* built-in.

The `range()` built-in is not a function but a type.
It does not take keyword arguments,
but may take one, two or three positional arguments.
All arguments must be integers.

```python
>>> range(4)
range(0, 4)
>>> range(False, True)
range(False, True)
>>> range(*b'(x\n')
range(40, 120, 10)
>>> range(type('A', (), {'__index__':lambda _:10})())
range(0, 10)
>>>
```

Although keyword arguments are not accepted,
the three parameters are named `start`, `stop` and `step`.
These names correspond to the `range` object's member variables.
The `step` argument must not be zero.

```python
>>> rev = range(10, 0, -1)
>>> rev.start, rev.stop, rev.step
(10, 0, -1)
>>> fwd = range(10)
>>> fwd.start, fwd.stop, fwd.step
(0, 10, 1)
>>>
```

## One argument.

When only one argument is passed
to the `range()` built-in
it is assigned to the `stop` parameter.
The `start` parameter defaults to 0 and the `step` parameter defaults to 1.

```python
>>> fwd = range(10)
>>> fwd.start, fwd.stop, fwd.step
(0, 10, 1)
>>> print(*fwd)
0 1 2 3 4 5 6 7 8 9
>>>
```

## Two arguments.

When two arguments are passed
to the `range()` built-in,
they are assigned to the `start` and `stop` parameters respectively.
The `step` parameter defaults to 1.

```python
>>> r = range(0x30, 0x3a)
>>> r.start, r.stop, r.step
(48, 58, 1)
>>> print(*r)
48 49 50 51 52 53 54 55 56 57
>>> print(*map(chr, r))
0 1 2 3 4 5 6 7 8 9
>>>
```

## Three arguments.

In order to specify a `step` other than 1,
all three arguments must be specified.

```python
>>> range(0,10,2)
range(0, 10, 2)
>>> range(0, -10, -1)
range(0, -10, -1)
>>>
```

## Immutability.

Range objects are immutable and hashable.

```python
>>> d = {range(3): 'ranges can be keys'}
>>> d
{range(0, 3): 'ranges can be keys'}
>>> d[range(0, 3, 1)]
'ranges can be keys'
>>>
```


# The *slice()* built-in.

The `slice()` built-in is not a function but a type.
It does not take keyword arguments,
but may take one, two or three positional arguments.
The arguments to the `slice()` built-in behave similarly to the `range()` built-in:
- a single argument is assigned to the `stop` parameter. The other parameters are set to None.
- two arguments are assigned to the `start` and `stop` parameters respectively. The `step` parameter is set to None.

```python
>>> slice(10)
slice(None, 10, None)
>>> slice(2, 10)
slice(2, 10, None)
>>> slice(0, 10, 2)
slice(0, 10, 2)
>>>
```

Unlike the `range()` built-in, though, its arguments may be of any type.
This means that a slice object is not hashable.

```python
>>> sli = slice('a', 3.14159, bool)
>>> sli.start
'a'
>>> sli.stop
3.14159
>>> sli.step
<class 'bool'>
>>>
```

## Negative arguments.

A negative argument *has no special meaning*.
(In fact, no value has any particular meaning.)
It is entirely up to an object's `__getitem__` method as to the interpretation
of `start`, `stop` and `step`.
For the standard built-in sequence types, the `__getitem__` method
interprets a negative index by adding the length of the sequence to the index.
Other, custom-built, types may have different semantics.
See the source file [slices.py](slices.py) for an example of using strings
as the `start` and `stop` parameters.

## Using a *slice* object.

A `slice` object may be used where a *slice expression* can be used.
The example below uses `a_string_object[slice_object]` to produce slices of
the given string.

```python
>>> row4 = '@ABCDEFGHIJKLMNO'
>>> for sli in slice(3), slice(1,7), slice(1, None, 2), slice(8,5,-1):
        print(sli, '=>', row4[sli])

slice(None, 3, None) => @AB
slice(1, 7, None) => ABCDEF
slice(1, None, 2) => ACEGIKMO
slice(8, 5, -1) => HGF
>>>
```


# The *dict()* built-in.

The `dict()` built-in is not a function but a type.
It may take zero or one positional arguments, plus any number of keyword arguments.
The keyword arguments are added to the dictionary created by the positional argument and the resulting dictionary is returned.

## Passing no positional arguments to the *dict()* built-in.

If no positional arguments are passed to the `dict()` built-in,
an empty dictionary is created, to which are added any keyword arguments.

```python
>>> dict()
{}
>>> dict(king='Arthur', quest='Holy Grail', year=597)
{'king': 'Arthur', 'quest': 'Holy Grail', 'year': 597}
>>>
```

## Passing a mapping to the *dict()* built-in.

If one positional argument is passed to the `dict()` built-in,
and that is a mapping,
a new dictionary is created with the same key-value pairs as the mapping object;
to which are added any keyword arguments.
Keys from the keyword arguments replace keys in the newly created dictionary.

```python
>>> mapping = {'king':'Henry VIII', 'wife':'Catherine of Aragon'}
>>> dict(mapping)
{'king': 'Henry VIII', 'wife': 'Catherine of Aragon'}
>>> dict(mapping, wife='Anne Boleyn', child='Elizabeth')
{'king': 'Henry VIII', 'wife': 'Anne Boleyn', 'child': 'Elizabeth'}
>>>
```

## Passing an iterable to the *dict()* built-in.

If one positional argument is passed to the `dict()` built-in,
and that is an iterable (that is not also a mapping),
the iterable must consist of two-item iterables
(therefore an iterable of iterables;
or, conceptually, an iterable of pairs).
A new dictionary is created using the pairs (the first of the pair is the key
and the second of the pair is the value)
to which are added any keyword arguments.
If a key appears more than once, later values replace earlier values.
Keys from the keyword arguments replace keys in the newly created dictionary.

```python
>>> pair1 = divmod(355, 113)
>>> pair2 = set([True, False])
>>> pair3 = ['Jack', 'Hearts']
>>> pair4 = {'king':'Henry VIII', 'wife':'Catherine of Aragon'}
>>> pair5 = 0.0, 1.0
>>> iterable_of_pairs = [pair1, pair2, pair3, pair4, pair5, 'OK']
>>> dict(iterable_of_pairs)
{3: 16, False: 1.0, 'Jack': 'Hearts', 'king': 'wife', 'O': 'K'}
>>> dict(iterable_of_pairs, Jack='Diamonds', king='clubs')
{3: 16, False: 1.0, 'Jack': 'Diamonds', 'king': 'clubs', 'O': 'K'}
>>>
```

Notice how the pair `False: True` (from `pair2`) was superceded by `0.0: 1.0`
(from `pair5`) to become `False: 1.0`.

## Keyword arguments.

As for any function that takes keyword arguments,
those passed to the `dict()` built-in must be valid Python identifiers.

```python
>>> dict(si×='thirty')
SyntaxError: invalid character in identifier
>>> dict(False=0)
SyntaxError: cannot assign to False
>>> dict(await=2.5)
SyntaxError: invalid syntax
>>>
```

Note that Python performs normalisation on the identifiers before they
are handled by the function.
This means that:
- identifiers that normalise to keywords are successfully handled
- multiple identifiers that are identical after normalisation cause a SyntaxError

```python
>>> dict(paſs='keyword')
{'pass': 'keyword'}
>>> dict(ϖιϹ='fields', πιΣ='pi-iota-sigma')
SyntaxError: keyword argument repeated
>>>
```


# The *list()*, *tuple()*, *set()* and *frozenset()* built-ins.

The *list()*, *tuple()*, *set()* and *frozenset()* built-ins are not functions but types.
Each can take either zero or one positional arguments.
They do not take keyword arguments.

With zero arguments, each returns an empty object of the expected type.

```python
>>> list()
[]
>>> tuple()
()
>>> set()
set()
>>> frozenset()
frozenset()
>>>
```

When given a single argument it must be an *iterable*.
A new object is returned containing the members of the iterable.
For the sequence types (*list* and *tuple*) the members of the new object
are in the same order as the given iterable.

```python
>>> list('cauliflower')
['c', 'a', 'u', 'l', 'i', 'f', 'l', 'o', 'w', 'e', 'r']
>>> tuple('cauliflower')
('c', 'a', 'u', 'l', 'i', 'f', 'l', 'o', 'w', 'e', 'r')
>>> set('cauliflower')
{'f', 'a', 'o', 'r', 'e', 'l', 'u', 'i', 'w', 'c'}
>>> frozenset('cauliflower')
frozenset({'f', 'a', 'o', 'r', 'e', 'l', 'u', 'i', 'w', 'c'})
>>>
```

The *list()*, *tuple()*, *set()* and *frozenset()* built-ins make shallow
copies of the given iterable. So, for example, calling `list(another_list)`
will return a new list object (its `id` is different from `another_list`)
but its members are the same.

```python
>>> another_list = [1, 2, 5, "Three sir", 3, ['throw', 'ye', 'the', 'Holy Handgrenade']]
>>> shallow = list(another_list)
>>> shallow == another_list
True
>>> shallow is another_list
False
>>>
```

Modifying the list does not effect the original list ...

```python
>>> shallow[2:4] = []
>>> shallow
[1, 2, 3, ['throw', 'ye', 'the', 'Holy Handgrenade']]
>>> another_list
[1, 2, 5, 'Three sir', 3, ['throw', 'ye', 'the', 'Holy Handgrenade']]
>>>
```

... but a mutable member of either list will be modified in both lists (since they both contain the *same object* rather than a copy)

```python
>>> another_list[-1][3:] = ['Holy', 'hand', 'grenade']
>>> another_list
[1, 2, 5, 'Three sir', 3, ['throw', 'ye', 'the', 'Holy', 'hand', 'grenade']]
>>> shallow
[1, 2, 3, ['throw', 'ye', 'the', 'Holy', 'hand', 'grenade']]
>>>
```
