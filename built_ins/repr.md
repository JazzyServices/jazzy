# The *repr()* and *ascii()* built-ins.

For most built-in types, the string returned by both `repr(obj)` and `ascii(obj)`
is identical to the string returned by `str(obj)`.
The two built-in types that don't obey this rule are strings and exceptions.


## Passing an exception to the `repr()` or `ascii()` built-ins.

The value returned by `repr()` (and by `ascii()`) when passed an exception
resembles an expression used to create that exception.

```python
>>> try:
    {}[0]
except KeyError as key_error:
    print('str  :', str(key_error))
    print('repr :', repr(key_error))
    print('ascii:', ascii(key_error))

str  : 0
repr : KeyError(0)
ascii: KeyError(0)
>>>
```

```python
>>> try:
    str(b'\xc0\xaf', 'U8')
except UnicodeError as error:
    print('str  :', str(error))
    print('repr :', repr(error))
    print('ascii:', ascii(error))

str  : 'utf-8' codec can't decode byte 0xc0 in position 0: invalid start byte
repr : UnicodeDecodeError('utf-8', b'\xc0\xaf', 0, 1, 'invalid start byte')
ascii: UnicodeDecodeError('utf-8', b'\xc0\xaf', 0, 1, 'invalid start byte')
>>>
```


## Passing a string to the `repr()` or `ascii()` built-ins.

The `repr()` of a string contains enclosing quotes.
Non-printable characters are converted to `\x`, `\u` or `\U` format.
Printable characters are generally not converted;
however, embedded quotes are escaped.
(Note that,
in the examples below,
we use `print()` to make it clear which characters are returned by
 the `repr()` function.)

```python
>>> print(repr('Python'))
'Python'
>>> print(repr('42 J/\xb5g/\u212a'))
'42 J/µg/K'
>>> print(repr('\x1b[0m'))
'\x1b[0m'
>>> print(repr('\udcba'))
'\udcba'
>>> print(repr("""Don't say "Ni"."""))
'Don\'t say "Ni".'
>>>
```

Strings that start with a combining character will cause the open quote to be
combined with the character.
(Note, your browser or document viewer may not render the following example in
the same manner as the Python interpreter.)

```python
>>> print(repr('\u0318'))
'̘'
>>> print(repr('\u20dd'))
'⃝'
>>>
```

The return value from `ascii()` will have printable characters outside of
the ASCII range formatted like non-printable characters
(with `\x`, `\u`, and `\U` sequences).

```python
>>> print(ascii('Python'))
'Python'
>>> print(ascii('42 J/\xb5g/\u212a'))
'42 J/\xb5g/\u212a'
>>> print(ascii('\udcba'))
'\udcba'
>>> print(ascii('\x1b[0m'))
'\x1b[0m'
>>> print(ascii("""Don't say "Ni"."""))
'Don\'t say "Ni".'
>>> print(ascii('\N{OX}'))
'\U0001f402'
>>>
```


## Exceptions constructed with strings.

For exceptions that were constructed using strings,
the `repr()` and `ascii()` values will differ if
the `repr()` and `ascii()` values of the strings differ.

```python
>>> print(repr(KeyError('\xb5g')))
KeyError('µg')
>>> print(ascii(KeyError('\xb5g')))
KeyError('\xb5g')
>>>
```


## User-defined classes.

If a user-defined class lacks `__repr__` and `__str__` methods,
the return value from `str()`, `repr()`, and `ascii()`
when given an instance of that class
is in the generic "angle-bracket" notation.

```python
>>> class microgram:
        pass

>>> obj = microgram()
>>> str(obj)
'<__main__.microgram object at 0x106feaeb8>'
>>> repr(obj)
'<__main__.microgram object at 0x106feaeb8>'
>>> ascii(obj)
'<__main__.microgram object at 0x106feaeb8>'
>>>
```

If a class has a `__repr__` method
this is used by the `repr()` built-in.
It is also used by the `ascii()` built-in which further converts out-of-range
characters to one of the escape formats.
Furthermore, if the class lacks a `__str__` method,
the `__repr__` method
is also used by the `str()` built-in.

```python
>>> class HeatCapacity:
        value = 42.0
        def __repr__(my):
            return repr(my.value) + ' J/\xb5g/\u212a'

>>> print(repr(HeatCapacity()))
42.0 J/µg/K
>>> print(ascii(HeatCapacity()))
42.0 J/\xb5g/\u212a
>>> print(str(HeatCapacity()))
42.0 J/µg/K
>>>
```


### `__str__` but no `__repr__`.

If a class has a `__str__` method but no `__repr__` method,
the value returned by `str()` is that returned by the `__str__` method, but
the return value from `repr()` and `ascii()` is in the "angle bracket" notation.
That is, `repr()` won't use `__str__` even though `str()` would use `__repr__`.

```python
>>> class Ego:
        def __str__(my):
            return my.__class__.__name__

>>> repr(Ego())
'<__main__.Ego object at 0x106fc8fd0>'
>>> ascii(Ego())
'<__main__.Ego object at 0x106fc8fd0>'
>>> str(Ego())
'Ego'
>>>
```


### Non-ascii class names.

Python3 allows the names of things (classes, functions, variables, *etc.*)
to use non-ASCII letters.
When a class has a name containing non-ASCII letters and that class does not
have a `__repr__` method, the `ascii()` built-in still escapes non-ASCII
characters.

```python
>>> class µg:
        pass

>>> obj = µg()
>>> print(repr(obj))
<__main__.μg object at 0x106fc8dd8>
>>> print(ascii(obj))
<__main__.\u03bcg object at 0x106fc8dd8>
>>>
```

(Note that the class's name is represented as `\u03bcg` rather than `\xb5g`.
This is due to the way names are normalised by Python3
-- this is explored in a later section.)

The `ascii()` built-in is useful for spotting visually-similar strings.
The following example uses Cyrillic А and Greek alpha both of which appear
like a Latin A.

```python
>>> class А:
        def Α(my):
                pass

>>> repr(А.Α)
'<function А.Α at 0x10700ae18>'
>>> ascii(А.Α)
'<function \\u0410.\\u0391 at 0x10700ae18>'
>>>
```

