# The *int()* built-in.

The `int()` built-in is not a function but a type.
Its initialiser can take zero, one or two arguments.
Before Python3.7, the first parameter was named "x" and could be specified
using either positional or keyword arguments. From 3.7 onwards it is a
positional-only parameter requiring a positional-only argument.
All of our examples in this section assume a version of Python greater than
or equal to 3.8 (the latest version available when this section was written).
The second parameter is named "base" and can be specified using either positional or keyword arguments.

| arg0   |  base  | returns
|--------|--------|--------
| absent | absent | 0
| int | disallowed | *arg0*
| *rational* | disallowed | *arg0* truncated to zero
| string or *buffer* | absent | decimal interpretation of *arg0*
| string, bytes or bytearray | 2..36 | interpretation of *arg0* in given base
| string, bytes or bytearray | 0 | interpretation of *arg0* as an integer literal

A couple of terms in the table above have the following meaning:

rational
: a rational `float` (not `inf` or `nan`), a Fraction or Decimal.

buffer
: bytes, bytearray, memoryview or array.array


## Passing no arguments to the `int()` built-in.

When no arguments are passed to `int()`,
the return value is zero.

```python
>>> int()
0
>>>
```


## Passing a numeric argument to the `int()` built-in.

When a numeric argument
(int, bool, rational float, Decimal or Fraction)
is passed to the `int()` built-in
the value is truncated towards zero (unless it is already integral of course).

```python
>>> import math, decimal, fractions
>>> int(0b0010)
2
>>> int(2.5)
2
>>> int(-2.5)
-2
>>> int(math.pi)
3
>>> int(decimal.Decimal('3.14'))
3
>>> int(fractions.Fraction(355, 113))
3
>>> int(True)
1
>>>
```

Note, that even though the mathematical constant, π, is irrational,
the floating point value `math.pi` is only an approximation of the constant
and is actually rational.

Because floating-point numbers can't be interpreted exactly,
some conversions to int look incorrect.

```python
>>> int(0.99999999999999995)
1
>>>
```

The non-rational floats are `nan` and `inf` and these can't be converted to integer.

```python
>>> int(math.nan)
Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    int(math.nan)
ValueError: cannot convert float NaN to integer
>>> int(math.inf)
Traceback (most recent call last):
  File "<pyshell#2>", line 1, in <module>
    int(math.inf)
OverflowError: cannot convert float infinity to integer
>>>
```

Complex numbers cannot be converted to integer.

```python
>>> int(0+0j)
Traceback (most recent call last):
  File "<pyshell#34>", line 1, in <module>
    int(0+0j)
TypeError: can't convert complex to int
>>>
```


## Passing a numeric-like argument to the `int()` built-in.

If an object has
an `__int__` method,
an `__index__` method or
a `__trunc__` method
this will be called when that object is passed to the `int()` built-in.
If an object has more than of those methods, they will be accessed in the
order listed
(`__int__` first, then `__index__`, then `__trunc__`).

The following example creates an anonymous class and an object of that class.
It then adds methods to the class to demonstrate the order that the methods
will be looked for when the object is passed to the `int()` built-in.

```python
>>> Anon = type('Anon', (), {'const':42})
>>> anon = Anon()
>>> int(anon)
Traceback (most recent call last):
  File "<pyshell#3>", line 1, in <module>
    int(anon)
TypeError: int() argument must be a string, a bytes-like object or a number, not 'Anon'
>>>
>>> Anon.__trunc__ = lambda my:my.const//10
>>> int(anon)
4
>>> Anon.__index__ = lambda my:my.const % 10
>>> int(anon)
2
>>> Anon.__int__ = lambda my:my.const
>>> int(anon)
42
```


## Passing a string as the only argument to the `int()` built-in.

If a string is passed as the only argument to the `int()` built-in
it is interpreted as a decimal literal. The string consists of:
- one or more decimal digits,
- possibly grouped using underscores,
- preceded by an optional sign (with no intervening space),
- optionally surrounded by whitespace,
- and may contain leading zeroes

```python
>>> int('42')
42
>>> int('+42')
42
>>> int(' -0042 ')
-42
>>> int('355_113')
355113
>>>
```

### Decimal digits

The digits allowed in a string passed to the `int()` built-in not only include
the ASCII digits "0" through "9", but any Unicode character with the "Nd" category.
For those readers unfamiliar with non-ASCII digits, a little education is required.

```python
>>> int('৪') == int('᮴') == int('4')
True
>>>
```

The example above (which may not render properly in all browers or document readers) uses three different characters that have an integer value of 4:
- U+09EA BENGALI DIGIT FOUR
- U+1BB4 SUNDANESE DIGIT FOUR
- U+0034 DIGIT FOUR

and could have been written as:

```python
>>> int('\u09ea') == int('\u1bb4') == int('\x34')
True
>>>
```

Unicode characters without the "Nd" category are not interpreted as digits
even if they have a numeric value in Unicode.

```python
>>> int('\xb2')
Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    int('\xb2')
ValueError: invalid literal for int() with base 10: '²'
>>>
```


### Zeroes

Since zeroes are decimal digits
it is obvious that any character with the "Nd" category and a numeric value of zero can be used as a zero including as a leading zero.
And remember that not all zeroes look like "0".

```python
>>> int('٠5')
5
>>> int('٠٥٥')
55
>>> int('٥٠٥')
505
>>> int('٠٠٠')
0
>>>
```

In Python2 an integer literal with leading zeroes was treated as an octal number.
This syntax was removed in Python3.
Leading zeroes are only allowed now on a literal zero.
When converting a string with leading zeroes using the `int()` built-in
the digit sequence is treated as base 10 (unless an explicit base is provided
-- see below) and not base 8.

```python
>>> 000
0
>>> 033
SyntaxError: invalid token
>>> int('033') == 0x1b
False
>>>
```

### Whitespace in strings passed to the `int()` built-in.

The surrounding whitespace allowed in a string passed to the `int()` built-in not only includes
the ASCII space, tab and newline characters,
but any Unicode character with the "White\_Space" property.

```python
>>> int('\f\v\t 42\r\n')
42
>>> int('\x8585')
85
>>> int('\u20002000')
2000
>>>
```

There is one whitespace character in Unicode that is not "white".
That is, it would consume ink if printed to a printer.
- U+1680 OGHAM SPACE MARK

It is visually similar to a minus sign, but is correctly treated as whitespace
by the `int()` built-in.

```python
>>> int(' 1')
1
>>>
```

### Numerical sign in strings passed to the `int()` built-in.

An optional sign may immediately precede the digits of the string
passed to the `int()` built-in. The only two characters allowed as the sign are:
- U+002B PLUS SIGN
- U+002D HYPHEN-MINUS

any other dashes or plus signs raise an exception

```python
>>> int('⍅2')
Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    int('⍅2')
ValueError: invalid literal for int() with base 10: '⍅2'
>>> int('⎻2')
Traceback (most recent call last):
  File "<pyshell#2>", line 1, in <module>
    int('⎻2')
ValueError: invalid literal for int() with base 10: '⎻2'
>>>
```


### Underscores in strings passed to the `int()` built-in.

Python (since version 3.6) allows integer literals,
and strings passed to the `int()` built-in, to contain underscores
to group digits into a more readable form.

```python
>>> 2_147_483_647
2147483647
>>> int('2_147_483_647')
2147483647
>>>
```

Although there are several conventions
(depending on region or culture)
for separating digits into groups, Python places no restrictions on how many
digits are in a group; with different groups allowed to have differing
numbers of digits. Leading zeroes can also be arbitrarily grouped.
This can make digit strings look like telephone numbers.

```python
>>> int('1_800_273_8255')
18002738255
>>> int('0800_1111')
8001111
>>> int('+44_800_11_11')
448001111
>>>
```

Single underscores may appear *between* digits but not precede nor succeed
the digits.

```python
>>> def valid_int_string(given):
        try:
            int(given)
        except ValueError:
            return False
        else:
            return True

>>> any(map(valid_int_string, ('_', '_1', '1_', '_1_', '-_1', '1__1')))
False
>>>
```

The only character allowed as the group separator is:
- U+005F LOW LINE

any other separator will raise an exception.
To be able to convert strings using a region-specific separator
use the `locale.atoi` function.

```python
>>> int('1,000')
Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    int('1,000')
ValueError: invalid literal for int() with base 10: '1,000'
>>> locale.setlocale(locale.LC_ALL, 'en_US')
'en_US'
>>> locale.atoi('1,000')
1000
>>>
```


## Passing a buffer as the only argument to the `int()` built-in.

A buffer, or binary sequence type, is a
`bytes`,
`bytearray`,
`memoryview`,
or `array.array` object (or any type that implements the
[buffer protocol](https://docs.python.org/3.8/c-api/buffer.html#bufferobjects)).

The same rules regarding whitespace, sign, decimal digits and underscore separator apply to buffers as they do for strings.

```python
>>> import array
>>> int(b' +4_2\r\n')
42
>>> int(bytearray([32, 45, 48, 49]))
-1
>>> int(array.array('I', [0x20323420]))
42
>>> int(memoryview(b'2020_04_01'))
20200401
>>>
```

Since binary sequences are limited to 8-bit bytes, they are limited to the
ASCII digits. Also of note is that the bytes `\xb5` and `\xa0` are *not*
treated as whitespace.

```python
>>> int(b'\f\v\t 42\r\n')
42
>>> int(bytearray([0xb5, 0x34, 0x32, 0xa0]))
Traceback (most recent call last):
  File "<pyshell#2>", line 1, in <module>
    int(bytearray([0xb5, 0x34, 0x32, 0xa0]))
ValueError: invalid literal for int() with base 10: b'\xb542\xa0'
>>>
```


## Passing an explicit base to the `int()` built-in.

The `int()` built-in can take a second argument which is the numerical base
in the range 2 to 36. This may also be specified as a keyword argument.

```python
>>> 6*9 == int('42', 13)
True
>>> print(*(int('10', base) for base in range(2,37)))
2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36
>>> print(*(int('100', base=base) for base in range(2,37)))
4 9 16 25 36 49 64 81 100 121 144 169 196 225 256 289 324 361 400 441 484 529 576 625 676 729 784 841 900 961 1024 1089 1156 1225 1296
>>>
```

For bases above ten, the ASCII letters `a` to `z` (or `A` to `Z`)
take values 10 to 35 as appropriate.
No other Unicode character represents a digit above nine in these higher bases,
not even one of the compatibility characters.

```python
>>> print(*(int('Ni', base) for base in range(24,37)))
570 593 616 639 662 685 708 731 754 777 800 823 846
>>>
```

All of the other rules regarding whitespace, sign, underscores, leading zeroes and Unicode digits still apply when a base has been specified.

```python
>>> int('\u3000 +\u0660_A_\u0666 \n', 13)
136
>>>
```

### Base-2, base-8 and base-16.

If the given base is 2, 8 or 16 then the `int()` built-in allows the string
to have a `0b`, `0B`, `0o`, `0O`, `0x` or `0X` prefix as appropriate.

```python
>>> int(' 0b_00_10 ', 2)
2
>>> int(' 0B1111 ', 2)
15
>>> int('0o033', 8)
27
>>> int('-0O_377', 8)
-255
>>> int('\t0x1c', 16)
28
>>> int('\f0XE5_F00D', 16)
15069197
>>>
```

Note that the zero before the indicator letter *must be*:
- U+0030 DIGIT ZERO

and the indicator letter *must be* one of:
- U+0042 LATIN CAPITAL LETTER B
- U+004F LATIN CAPITAL LETTER O
- U+0058 LATIN CAPITAL LETTER X
- U+0062 LATIN SMALL LETTER B
- U+006F LATIN SMALL LETTER O
- U+0078 LATIN SMALL LETTER X

no other characters are allowed in the numerical prefix.
Unicode digits are allowed after the prefix as normal.

```python
>>> int('0b_\u0660_\u0661_\u0660\u3000', 2)
2
>>> int('0O_\u0660_\u0661_\u0660\u3000', 8)
8
>>> int('0X_\u0666_F', 16)
111
>>>
```


### Bytes and bytearray only.

When the `int()` built-in is given a base argument,
the first argument to the function is only allowed to be a string, bytes
or bytearray object. It cannot be a memoryview or `array.array`.
This is an annoying inconsistency.

```python
>>> int(b'100', 36)
1296
>>> int(bytearray(b'100'), 36)
1296
>>> int(memoryview(b'100'), 36)
Traceback (most recent call last):
  File "<pyshell#2>", line 1, in <module>
    int(memoryview(b'100'), 36)
TypeError: int() can't convert non-string with explicit base
>>> import array
>>> int(array.array('B', b'100'), 36)
Traceback (most recent call last):
  File "<pyshell#6>", line 1, in <module>
    int(array.array('B', b'100'), 36)
TypeError: int() can't convert non-string with explicit base
>>>
```


## Passing base=0 to the `int()` built-in.

When the `int()` built-in is given a base argument equal to zero,
the first argument determines the base (2, 8, 10 or 16).
All of the rules and restrictions given above regarding an explicit base
also apply here.
There is one further restriction, as there is for integer literals.
*Leading zeroes are not allowed in base 10* (except if the value is zero.)

```python
>>> int('0b10', 0)
2
>>> int('0o10', 0)
8
>>> int('0x10', 0)
16
>>> int('00', 0)
0
>>>
```


## The type of the base argument.

The base argument can be an object that is a subclass of `int`
or an object that can be converted to `int` using its `__index__` method.

```python
>>> int('0X_\u0666_F', False)
111
>>> int('0X_\u0666_F', b'\0'[0])
111
>>> int('0X_\u0666_F', type('Anon', (), {'__index__': lambda _:0})())
111
>>>
```
