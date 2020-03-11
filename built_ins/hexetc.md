# The *hex()* built-in and friends.

This section covers a family of built-ins that take a single integer argument
and return a string:
- `hex()`
- `oct()`
- `bin()`
- `chr()`

The first three functions convert signed integers to hexadecimal, octal and binary representation respectively.
The `chr()` built-in only accepts non-negative integers in the range (0, 0x110000) and returns a 1-character string for the given Unicode code point.

We will also include in this section:
- `ord()`

because it is the inverse of `chr()`.


## Example

In the following example we will use a range object and observe the output
from all four of the int-to-string built-ins alongside the output of `str()`
as a comparison.

```python
>>> seq = range(65, 91)
>>> print(*map(str, seq))
65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90
>>> print(*map(hex, seq))
0x41 0x42 0x43 0x44 0x45 0x46 0x47 0x48 0x49 0x4a 0x4b 0x4c 0x4d 0x4e 0x4f 0x50 0x51 0x52 0x53 0x54 0x55 0x56 0x57 0x58 0x59 0x5a
>>> print(*map(oct, seq))
0o101 0o102 0o103 0o104 0o105 0o106 0o107 0o110 0o111 0o112 0o113 0o114 0o115 0o116 0o117 0o120 0o121 0o122 0o123 0o124 0o125 0o126 0o127 0o130 0o131 0o132
>>> print(*map(bin, seq))
0b1000001 0b1000010 0b1000011 0b1000100 0b1000101 0b1000110 0b1000111 0b1001000 0b1001001 0b1001010 0b1001011 0b1001100 0b1001101 0b1001110 0b1001111 0b1010000 0b1010001 0b1010010 0b1010011 0b1010100 0b1010101 0b1010110 0b1010111 0b1011000 0b1011001 0b1011010
>>> print(*map(chr, seq))
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
>>>
```

The `hex()`, `oct()` and `bin()` built-in functions produce strings that
resemble
[integer literals](https://docs.python.org/3.8/reference/lexical_analysis.html#integer-literals).
Each starts with a zero which is followed by an "x", "o" or "b" then the digits
in the required base. `hex()` uses lowercase letters "a" through "f".
None of the functions produce zero-padded output.


## Zero

The only case where a zero follows the "0x", "0o" or "0b" is when the value is zero.

```python
>>> print(*(fn(0) for fn in (hex, oct, bin)))
0x0 0o0 0b0
>>>
```


## Negative numbers

When converting negative numbers to hexadecimal, octal and binary
the built-in functions simply prepend the sign to the returned string.
This differs from certain other languages that prefer to give the two's
complement representation of a signed integer type.

```python
>>> print(*(fn(-40) for fn in (hex, oct, bin)))
-0x28 -0o50 -0b101000
>>>
```


## Booleans

Since the boolean constants `False` and `True` are instances of `int`
(because `bool` is a subclass of `int`), they can be passed to the
int-to-string built-ins.

```python
>>> tuple(fn(False) for fn in (hex, oct, bin, chr))
('0x0', '0o0', '0b0', '\x00')
>>> tuple(fn(True) for fn in (hex, oct, bin, chr))
('0x1', '0o1', '0b1', '\x01')
>>>
```


## Bytes

Since individual bytes are also integers they can be passed to the int-to-string built-ins.

```python
>>> seq = bytearray(range(65, 91))
>>> print(*map(str, seq))
65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90
>>> print(*map(hex, seq))
0x41 0x42 0x43 0x44 0x45 0x46 0x47 0x48 0x49 0x4a 0x4b 0x4c 0x4d 0x4e 0x4f 0x50 0x51 0x52 0x53 0x54 0x55 0x56 0x57 0x58 0x59 0x5a
>>> print(*map(oct, seq))
0o101 0o102 0o103 0o104 0o105 0o106 0o107 0o110 0o111 0o112 0o113 0o114 0o115 0o116 0o117 0o120 0o121 0o122 0o123 0o124 0o125 0o126 0o127 0o130 0o131 0o132
>>> print(*map(bin, seq))
0b1000001 0b1000010 0b1000011 0b1000100 0b1000101 0b1000110 0b1000111 0b1001000 0b1001001 0b1001010 0b1001011 0b1001100 0b1001101 0b1001110 0b1001111 0b1010000 0b1010001 0b1010010 0b1010011 0b1010100 0b1010101 0b1010110 0b1010111 0b1011000 0b1011001 0b1011010
>>> print(*map(chr, seq))
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
>>>
```


# The *chr()* and *ord()* built-ins.

The `chr()` built-in returns a one-character string representing a Unicode
code point; including unassigned code points, non-characters, combining characters and surrogates.

The examples below have been copy-and-pasted from the Python interpreter,
so if `chr()` produces a printable character, the interpreter will show it ...

```python
>>> chr(97)
'a'
>>> chr(0x2e92)
'⺒'
>>> chr(0x16b5)
'ᚵ'
>>>
```

... but unprintable characters will be escaped appropriately ...

```python
>>> chr(0)
'\x00'
>>> chr(0xfffe)
'\ufffe'
>>> chr(0xd800)
'\ud800'
>>> chr(0x1ff80)
'\U0001ff80'
>>>
```

... though fun can be had with combining characters ...

```python
>>> chr(0x318)
'̘'
>>> chr(0x319)
'̙'
>>> chr(0x20dd)
'⃝'
>>>
```


## The *ord()* built-in.

The `ord()` built-in is the inverse of `chr()`.
It converts a 1-character string to an integer (the Unicode code point of that character).

```python
>>> print(*map(ord, ('a⺒ᚵ')))
97 11922 5813
>>> print(*map(ord, ('\x00', '\ufffe', '\ud800', '\U0001ff80')))
0 65534 55296 130944
>>>
```

A string of any length other than one will raise an exception
even if that string could be normalised to a 1-character string.

```python
>>> import unicodedata
>>> decomposed = 'A\u0300'
>>> print(decomposed)
À
>>> ord(decomposed)
Traceback (most recent call last):
  File "<pyshell#4>", line 1, in <module>
    ord(decomposed)
TypeError: ord() expected a character, but string of length 2 found
>>> ord(unicodedata.normalize('NFC', decomposed))
192
>>>
```
