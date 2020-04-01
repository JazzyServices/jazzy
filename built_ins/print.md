# The *print()* built-in.

The `print()` built-in takes an arbitrary number of positional arguments
and up to four keyword arguments (`file`, `sep`, `end`, `flush`).
Each of the positional arguments is converted to a string and written to
the `file`. After each of the positional arguments is written, the value
of `sep` is written to the file -- except for the last positional argument;
after which the value of `end` is written to the file.
If the truth value of `flush` is True, then the `file` is flushed.

The `sep` keyword argument has a default of `' '` (U+0020 SPACE).
If given, it must be a string or None.
If it is None, then the default is used.
The string can be of any length.

```python
>>> spam = 'Spam'
>>> print(spam, spam, spam)
Spam Spam Spam
>>> print(spam, spam, spam, sep=None)
Spam Spam Spam
>>> print(spam, spam, spam, sep=',')
Spam,Spam,Spam
>>> print(spam, spam, spam, sep='')
SpamSpamSpam
>>> print(spam, spam, spam, sep='!\n')
Spam!
Spam!
Spam
>>>
```

The `end` keyword argument has a default of `'\n'`.
If given, it must be a string or None.
If it is None, then the default is used.
The string can be of any length.

```python
>>> for end in ('\n', None, '!!', '', '--\n--\n'):
        print('[', *range(3), ']', end=end)

[ 0 1 2 ]
[ 0 1 2 ]
[ 0 1 2 ]!![ 0 1 2 ][ 0 1 2 ]--
--
>>>
```

The `file` keyword argument doesn't need to be a subclass of `io.TextIOBase`
(as returned by the  `open()` built-in), all it needs is a `write()` method
that accepts a string argument.
(And a `flush()` method if it is used with the `flush=True` keyword argument.)

The example below "writes" strings to a list.

```python
>>> stream = []
>>> Writer = type('Writer', (), dict(write=stream.append))
>>> print(1, True, file=Writer())
>>> stream
['1', ' ', 'True', '\n']
>>>
```

Note the following:
- `Writer.write` was called four times
- the two positional arguments were converted to strings
- the (default) `sep` was written between each of the converted strings
- the (default) `end` was written at the end

If there are no positional arguments,
the `print()` built-in writes only the `end` argument to the `file`.
Even if the `end` argument is the empty string, `file.write` is still called.

```python
>>> stream = []
>>> Writer = type('Writer', (), dict(write=stream.append))
>>> print(file=Writer())
>>> stream
['\n']
>>> print(file=Writer(), end='')
>>> stream
['\n', '']
>>> print(file=Writer(), end='no newline')
>>> stream
['\n', '', 'no newline']
>>>
```

If the truth value of `flush` is True,
the `print()` built-in calls `file.flush()` after it has written the `end` argument.

```python
>>> write = lambda _,x: print(f'Writing {x!r}')
>>> flush = lambda _: print('FLUSHING')
>>> Trail = type('Trail', (), dict(write=write, flush=flush))
>>> print(1, file=Trail())
Writing '1'
Writing '\n'
>>> print(2.0, 3j, file=Trail(), flush=True)
Writing '2.0'
Writing ' '
Writing '3j'
Writing '\n'
FLUSHING
>>> print(end='end only', file=Trail(), flush=...)
Writing 'end only'
FLUSHING
>>>
```

The success of a call to the `print()` built-in relies on the ability of
the `file` to encode the strings it has been given.
Normally, `sys.stdout` has an encoding of `utf-8`
(and `errors='strict'`)
meaning that printing isolated surrogates raises an exception.

```python
>>> print('OK', '\udc00')
OK Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    print('OK', '\udc00')
UnicodeEncodeError: 'utf-8' codec can't encode character '\udc00' in position 0: surrogates not allowed
>>> print('OK', 'so', 'far', end='\udc00')
OK so farTraceback (most recent call last):
  File "<pyshell#2>", line 1, in <module>
    print('OK', 'so', 'far', end='\udc00')
UnicodeEncodeError: 'utf-8' codec can't encode character '\udc00' in position 0: surrogates not allowed
>>>
```
