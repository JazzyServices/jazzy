# Built-in numerical functions.

This section will deal with the following built-in functions
that take numerical arguments:

- abs()
- divmod()
- pow()
- round()

The `min`, `max`, `sum`, `any`, and `all` functions take a *sequence of* numbers
and are dealt with in a later section.


## The *abs()* built-in.

Returns the absolute value of the given argument;
which may be an integer, float, complex,
Decimal or Fraction.

```python
>>> import math, decimal, fractions
>>> abs(False)
0
>>> abs(True)
1
>>> abs(-42)
42
>>> abs(-0.0)
0.0
>>> abs(-355/113)
3.1415929203539825
>>> abs(math.nan)
nan
>>> abs(-math.inf)
inf
>>> abs(b'\xff'[0])
255
>>> abs(decimal.Decimal(-6.75))
Decimal('6.75')
>>> abs(fractions.Fraction(-355, 113))
Fraction(355, 113)
>>>
```

For complex numbers, the `abs()` built-in returns the number's *magnitude*.

```python
>>> abs(-3-4j)
5.0
>>> abs(-10+0j)
10.0
>>> abs(-20j)
20.0
>>>
```

## The *divmod()* built-in.

Given two (non complex) numbers as arguments,
divides the first (the *numerator*) by the second (the *divisor*) and
returns a pair of numbers consisting of:
- the *quotient* (a whole number of multiples of the divisor)
- the *remainder*

as in:

> 39 divided by 4 is 9 remainder 3

Arguments to the `divmod()` built-in are *positional only*.

```python
>>> import decimal, fractions
>>> divmod(39, 4)
(9, 3)
>>> divmod(39., 4.)
(9.0, 3.0)
>>> divmod(decimal.Decimal(39), decimal.Decimal(4))
(Decimal('9'), Decimal('3'))
>>> divmod(fractions.Fraction(39, 1), fractions.Fraction(4, 1))
(9, Fraction(3, 1))
>>>
```

### Invariants

The return values from `divmod(numerator, divisor)` (the quotient and remainder)
will *always* obey the follow rules (within floating-point accuracy):
- numerator == quotient * divisor + remainder
- the remainder is *smaller than* the divisor (*i.e.* it lies between zero and the divisor

```python
>>> numerator, divisor = 39, 4
>>> quotient, remainder = divmod(numerator, divisor)
>>> quotient, remainder
(9, 3)
>>> numerator == quotient * divisor + remainder
True
>>>
```

These rules should be self-evident and obvious;
but programmers are sometimes surprised by them
as we shall see in the next few paragraphs.

### Negative numerator.

What is the return value of the expression `divmod(-39, 4)`?

If your answer was `(-9, -3)` then you are wrong;
because `-3` does not lie between zero and the divisor (4).

```python
>>> divmod(-39, 4)
(-10, 1)
>>>
```

Some programmers are surprised by this, and I have even heard them say that
"Python is wrong". But take a real-world example of modular arithmetic --
the 12-hour clock.

> If the time now is 2 o'clock, what was the time 5 hours ago?

It is obvious that the answer is 9 o'clock and not "-3 o'clock".

```python
>>> (2-5) % 12
9
>>>
```

If we perform the same subtraction for the 24-hour clock:

```python
>>> divmod(2-5, 24)
(-1, 21)
>>>
```

... the quotient gives us the number of days (`-1`, *i.e.* one day ago)
and the remainder gives us the hours (`21`, *i.e.* 21:00 or 9pm)

## Negative divisor

If the divisor is negative, the rules still must apply.
Both when the numerator is positive and the numerator is negative.
That is, the remainder must be between zero and the divisor.
And since the divisor is negative, `(divisor < remainder <= 0)` is True.

```python
>>> divmod(39, -4)
(-10, -1)
>>> divmod(-39, -4)
(9, -3)
>>>
```

## Shifted divisor.

There are some applications that require modular arithmetic where the
result (the remainder) lies within the range *-x* to *+x*.
For example, a compass bearing of wind direction might be required to lie within the range
`-180.0 < bearing <= 180.0` with North being 0.0, West -90.0, East +90.0 and South +180.0.

The divisor needs to be 360.0 (not 180.0) but the calculation needs to be
shifted to stay in range. One way of doing this is:

```python
def veer_or_back_v1(direction, change):
    """Derive new wind direction (algorithm 1)."""
    new_direction = (direction + change) % 360.0
    if new_direction > 180.0:
        new_direction -= 360.0
    return new_direction
```

This algorithm gives the correct results
(the reader is encouraged to verify this by writing unit tests)
but requires an extra if-statement.
We could be tempted to re-write this function
so that the direction is normalised to the range `0.0 <= x < 360.0`
prior to addition; then denormalising the answer by subtracting 180.0:

```python
def veer_or_back_v2(direction, change):
    """Derive new wind direction (algorithm 2)."""
    new_direction = (direction + change + 180.0) % 360.0
    return new_direction - 180.0
```

However, this puts the result in the range `-180.0 <= result < 180`
which gives the wrong answer for due South.
To address this problem we need to normalise to the range `-360.0 < x <= 0.0`
then add 180.0

```python
def veer_or_back_v3(direction, change):
    """Derive new wind direction (algorithm 3)."""
    new_direction = (direction + change + 180.0) % -360.0
    return new_direction + 180.0
```

## Non-integral divisor.

If the divisor is non-integral, the rules still must apply.
The quotient is a (floating point) whole number
and the remainder lies between zero and the divisor.

```python
>>> divmod(100, 9.75)
(10.0, 2.5)
>>> divmod(-100, 9.75)
(-11.0, 7.25)
>>> divmod(100, -9.75)
(-11.0, -7.25)
>>> divmod(-100, -9.75)
(10.0, -2.5)
>>>
```

## Non-finite numbers.

If the numerator is infinite, both the quotient and remainder will be NaN.

```python
>>> divmod(math.inf, 2)
(nan, nan)
>>> divmod(math.inf, math.inf)
(nan, nan)
>>>
```

When the numerator is finite but the divisor is infinite,
the quotient and the remainder will be as follows:

```python
>>> divmod(9.75, math.inf)
(0.0, 9.75)
>>> divmod(-9.75, math.inf)
(-1.0, inf)
>>> divmod(9.75, -math.inf)
(-1.0, -inf)
>>> divmod(-9.75, -math.inf)
(0.0, -9.75)
>>>
```

It may seem surprising that the remainder is infinite when one of the operands
is negative; but this follows the pattern for large divisors,
that as the divisor increases, the remainder increases.

```python
>>> divmod(-9.75, 1e1)
(-1.0, 0.25)
>>> divmod(-9.75, 1e2)
(-1.0, 90.25)
>>> divmod(-9.75, 1e4)
(-1.0, 9990.25)
>>> divmod(-9.75, 1e8)
(-1.0, 99999990.25)
>>> divmod(-9.75, 1e16)
(-1.0, 9999999999999990.0)
>>>
```

If either operand is NaN, both the quotient and remainder will be NaN.
The only exception is when the divisor is zero.

```python
>>> divmod(9.75, math.nan)
(nan, nan)
>>> divmod(math.nan, -9.75)
(nan, nan)
>>> divmod(math.nan, 0.0)
Traceback (most recent call last):
  File "<pyshell#3>", line 1, in <module>
    divmod(math.nan, 0.0)
ZeroDivisionError: float divmod()
>>>
```


## The *pow()* built-in.

Prior to Python3.8 the `pow()` built-in only accepted positional arguments,
from that version onwards it accepts keyword arguments for its
parameters (`base`, `exp` and `mod`)

The `pow()` built-in can take two or three arguments.
The difference in behaviour between the two- and three-argument forms
is sufficient enough for us to discuss them in separate sections.


## The *pow()* built-in with two arguments.

The two-argument form of the `pow()` built-in
is equivalent to using the `**` operator.

```python
>>> pow(2, 4)
16
>>> pow(2.0, 4.0)
16.0
>>> pow(decimal.Decimal('2'), decimal.Decimal('4'))
Decimal('16')
>>> pow(1j, 1j)
(0.20787957635076193+0j)
>>>
```

If the `exp` argument is `0`,
the returned value is equal to `1` but in the type of `base`.

```python
>>> pow(42, 0)
1
>>> pow(math.pi, 0)
1.0
>>> pow(1j, 0)
(1+0j)
>>> pow(decimal.Decimal(2.5), 0)
Decimal('1')
>>> pow(fractions.Fraction(355, 113), 0)
Fraction(1, 1)
>>>
```

Raising a number to the power of zero is one of the few operations that
doesn't propogate a NaN.

```python
>>> pow(math.nan, 0)
1.0
>>>
```

If `base` is zero and `exp` is negative,
an exception is raised.

```python
>>> pow(0, -1)
Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    pow(0, -1)
ZeroDivisionError: 0.0 cannot be raised to a negative power
>>>
```

### The *pow()* built-in with boolean arguments

Since a `bool` is an `int`, the `pow()` built-in can take boolean arguments.

```python
>>> pow(False, False)
1
>>> pow(False, True)
0
>>> pow(True, False)
1
>>> pow(True, True)
1
>>>
```

This produces the same
*truth table*
as `exp implies base`

### The *pow()* built-in with integer arguments

If `exp` is positive or zero, the return value is an integer.
If `exp` is negative, the return value is a float.

```python
>>> pow(10, 2)
100
>>> pow(10, 0)
1
>>> pow(10, -2)
0.01
>>>
```

### The *pow()* built-in with float arguments

If both arguments are float (or one is float and the other int)
then the result is usually a float.

```python
>>> pow(1, 1.0)
1.0
>>> pow(1.0, 1)
1.0
>>> pow(2, 0.5)
1.4142135623730951
>>> pow(3.0, -1)
0.3333333333333333
>>>
```

However, if `base` is negative and `exp` is fractional, a complex number is returned.

```python
>>> pow(-1.0, 0.5)
(6.123233995736766e-17+1j)
>>> pow(-1, fractions.Fraction(1, 2))
(6.123233995736766e-17+1j)
>>>
```

Note the rounding error.
The expected answer is `0+1j'

### The *pow()* built-in with one Decimal argument.

Mixing int and `Decimal` arguments returns a `Decimal`.

```python
>>> pow(decimal.Decimal('2.0'), 4)
Decimal('16.0000')
>>> pow(decimal.Decimal('2'), 4)
Decimal('16')
>>> pow(4, decimal.Decimal(2))
Decimal('16')
>>> pow(16, decimal.Decimal('0.5'))
Decimal('4.000000000000000000000000000')
>>>
```

Mixing float and `Decimal` arguments is not supported.

```python
>>> pow(2.0, decimal.Decimal(4))
Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    pow(2.0, decimal.Decimal(4))
TypeError: unsupported operand type(s) for ** or pow(): 'float' and 'decimal.Decimal'
>>> pow(decimal.Decimal('2.0'), 4.0)
Traceback (most recent call last):
  File "<pyshell#2>", line 1, in <module>
    pow(decimal.Decimal('2.0'), 4.0)
TypeError: unsupported operand type(s) for ** or pow(): 'decimal.Decimal' and 'float'
>>>
```

### The *pow()* built-in with one Fraction argument.

If `base` is a `Fraction` and `exp` is int, a `Fraction` is returned.

```python
>>> pow(fractions.Fraction(5,2), -2)
Fraction(4, 25)
>>> pow(fractions.Fraction(5,2), 3)
Fraction(125, 8)
>>>
```

If `base` is an int and `exp` is an integral `Fraction`, an int is returned.

```python
>>> pow(2, fractions.Fraction(2,1))
4
>>>
```

If either argument is a float or `exp` is a proper `Fraction`, a float is returned.

```python
>>> pow(2, fractions.Fraction(1,2))
1.4142135623730951
>>> pow(fractions.Fraction(2,1), fractions.Fraction(1,2))
1.4142135623730951
>>> pow(2.0, fractions.Fraction(4,1))
16.0
>>> pow(fractions.Fraction(2,1), 4.0)
16.0
>>>
```

### The *pow()* built-in with one complex argument.

Calling the `pow()` built-in with at least one complex argument
returns a complex number.

```python
>>> pow(math.e, 1j * math.pi)
(-1+1.2246467991473532e-16j)
>>> pow(1j, 2)
(-1+0j)
>>>
```


## The *pow()* built-in with three arguments.

The three-argument form of the `pow()` built-in
returns `pow(base, exp) % mod`
and is generally used in cryptographic algorithms.
All three arguments must be integers or integral `Decimal`.

```python
>>> pow(2,4,5)
1
>>> pow(decimal.Decimal(2),4,5)
Decimal('1')
>>> pow(decimal.Decimal('2'), decimal.Decimal('4'), 5)
Decimal('1')
>>> pow(decimal.Decimal('2'), decimal.Decimal('4'), decimal.Decimal('5'))
Decimal('1')
>>>
```

If `exp` is negative, the `pow()` built-in returns the *modular inverse*
of `base ** exp % mod`.
Given, `inv = pow(base, -exp, mod)`
then `(inv * pow(base, exp)) % mod == 1`

```python
>>> base, exp, mod = 79, 27, 256
>>> inv = pow(base, -exp, mod)
>>> inv
143
>>> inv * pow(base, exp) % mod
1
>>>
```

A restriction on this equation is that
`base` must be relatively prime to `mod`
(in many cryptographic algorithms `base` will be a prime number).

```python
>>> pow(26, -1, 22)
Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    pow(26, -1, 22)
ValueError: base is not invertible for the given modulus
>>>
```


## The *round()* built-in.

The `round()` built-in can take one or two positional or keyword arguments.
- `round(number, ndigits=None)`.

It rounds a number to the given number of *decimal* places.
If `ndigits` is given, it must be an integer.

```python
>>> round(273.15, 2)
273.15
>>> round(273.15, 1)
273.1
>>> round(273.15, 0)
273.0
>>>
```

If `ndigits` is negative, the return value is the number rounded to
the nearest  `10 ** -ndigits`

```python
>>> round(273.15, -1)
270.0
>>> round(273.15, -2)
300.0
>>> round(273.15, -3)
0.0
>>>
```

If `ndigits` is missing or `None`, the return value is an integer.

```python
>>> round(273.15)
273
>>> round(273.15, None)
273
>>>
```

When `number` is midway between two rounding choices
the number is rounded toward the even choice.

```python
>>> round(decimal.Decimal('273.15'), 1)
Decimal('273.2')
>>> round(decimal.Decimal('273.25'), 1)
Decimal('273.2')
>>> round(decimal.Decimal('273.35'), 1)
Decimal('273.4')
>>> round(decimal.Decimal('273.45'), 1)
Decimal('273.4')
>>>
```


### When *ndigits* is given (and is not None).

If `number` is an int, the return value will be an int.

```python
>>> round(299792458, -4)
299790000
>>> round(299792458, -5)
299800000
>>> round(299792458, -6)
300000000
>>>
```

If `number` is a `Decimal`, the return value will be a `Decimal`,
and the number of decimal places in the `Decimal` will match `ndigits`.

```python
>>> round(decimal.Decimal('273.15'), 1)
Decimal('273.2')
>>> round(decimal.Decimal('273.15'), 3)
Decimal('273.150')
>>> round(decimal.Decimal('273.15'), -1)
Decimal('2.7E+2')
>>>
```

If `number` is a `Fraction`, the return value will be a `Fraction`.

```python
>>> zdeg = fractions.Fraction(5463, 20)
>>> float(zdeg)
273.15
>>> round(zdeg, 1)
Fraction(1366, 5)
>>> float(_)
273.2
>>> round(fractions.Fraction(1, 3), 3)
Fraction(333, 1000)
>>>
```
