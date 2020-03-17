# The *float()* built-in.

The `float()` built-in is not a function but a type.
Its initialiser can take zero or one arguments.
Before Python3.7, the first parameter was named "x" and could be specified
using either positional or keyword arguments. From 3.7 onwards it is a
positional-only parameter requiring a positional-only argument.
All of our examples in this section assume a version of Python greater than
or equal to 3.8 (the latest version available when this section was written).

## Passing no arguments to the `float()` built-in.

When no arguments are passed to `float()`,
the return value is 0.0.

```python
>>> float()
0.0
>>>
```


## Passing a numeric argument to the `float()` built-in.

When a numeric argument
(int, bool, float, Decimal or Fraction)
is passed to the `float()` built-in
it is converted to floating point
if it is within range of the underlying implementation.

```python
>>> import math, decimal, fractions
>>> float(True)
1.0
>>> float(1<<31)
2147483648.0
>>> float(math.nan)
nan
>>> float(-math.inf)
-inf
>>> float(decimal.Decimal(3.14))
3.14
>>> float(fractions.Fraction(355, 113))
3.1415929203539825
>>> float(b'\xff'[0])
255.0
>>>
```

If the argument passed to the `float()` built-in is out of range
an exception is raised.

```python
>>> float(1<<1024)
Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    float(1<<1024)
OverflowError: int too large to convert to float
>>>
```

## Passing a string argument to the `float()` built-in.

The string passed to the `float()` built-in can consist of several parts:
- surrounding whitespace
- sign
- digits before the decimal point
- decimal point
- digits after the decimal point
- exponent indicator
- exponent sign
- exponent digits

As with the `int()` built-in, the only two characters allowed as the sign are:
- U+002B PLUS SIGN
- U+002D HYPHEN-MINUS

this also applies to the sign of the exponent.

The only character allowed as the decimal point is:
- U+002E FULL STOP

The only two characters allowed as the exponent indicator are:
- U+0045 LATIN CAPITAL LETTER E
- U+0065 LATIN SMALL LETTER E

As with the `int()` built-in, the digits can consist of any character with
the "Nd" category and may be separated into groups using:
- U+005F LOW LINE

this also applies to the digits of the exponent.

```python
>>> float(' +0_1_1.1_1_0e0_1 ')
111.1
>>> float('᮴.᮴e᮴')
44000.0
>>> float('\u0666.\u0666E\u0660\u0661\u2000')
66.0
>>> float('٠٥٠.٥٠٥e٠٥')
5050500.0
>>> float('୧e୧')
10.0
>>>
```

### Infinities and NaN.

Alternatively, the string passed to the `float()` built-in can consist of:
- surrounding whitespace
- optional sign
- one of the ASCII strings: "inf", "infinity", "nan".

The string is case-insensitive.

```python
>>> float('INF')
inf
>>> float('-INFinitY')
-inf
>>> float('NaN')
nan
>>> float('\nnAn\n')
nan
>>>
```

## Passing a buffer as the only argument to the `float()` built-in.

A buffer, or binary sequence type, is a
`bytes`,
`bytearray`,
`memoryview`,
or `array.array` object (or any type that implements the
[buffer protocol](https://docs.python.org/3.8/c-api/buffer.html#bufferobjects)).

The same rules regarding whitespace, sign, digits, decimal point, exponent indicator and underscore separator apply to buffers as they do for strings.

```python
>>> import array
>>> float(b' +2.997_924_58e+08\t')
299792458.0
>>> float(bytearray([32, 45, 48, 49, 46, 50]))
-1.2
>>> float(array.array('I', [0x2e323420, 0x302d4533]))
42.3
>>> float(memoryview(b'2020.04_01'))
2020.0401
>>> float(b'-Infinity\r\n')
-inf
>>>
```

Since binary sequences are limited to 8-bit bytes, they are limited to the
ASCII digits. Also of note is that the bytes `\xb5` and `\xa0` are *not*
treated as whitespace.

## Objects with a `__float__` or `__index__` method.

If an object's class has a `__float__` method
it will be used by the `float()` built-in
otherwise the `__index__` method will be used.
If neither is defined, an exception is raised.

```python
>>> Anon = type('Anon', (), {})
>>> anon = Anon()
>>> float(anon)
Traceback (most recent call last):
  File "<pyshell#472>", line 1, in <module>
    float(anon)
TypeError: float() argument must be a string or a number, not 'Anon'
>>> Anon.__index__ = lambda _:42
>>> float(anon)
42.0
>>> Anon.__float__ = lambda _:355/113
>>> float(anon)
3.1415929203539825
>>>
```

