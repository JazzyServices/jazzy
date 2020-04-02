# The *open()* built-in.

The `open()` built-in accepts between one and eight arguments
which may be specified as either positional or keyword arguments.
The interaction between the arguments is quite convoluted and the
`mode` argument is quite arcane;
indicating that the `open()` built-in is trying to do too much.


## The *file* argument.

The `file` argument is the only mandatory argument to the `open()` built-in.
It specifies the file path to open.
It may be an object of the following types:
- str
- bytes
- `os.PathLike` : an abstract base class for objects representing a file system path, *e.g.* `pathlib.PurePath`.
- int : a file descriptor to be wrapped.

```python
>>> import os, pathlib
>>> open('/dev/null')
<_io.TextIOWrapper name='/dev/null' mode='r' encoding='UTF-8'>
>>> open(b'/dev/null')
<_io.TextIOWrapper name=b'/dev/null' mode='r' encoding='UTF-8'>
>>> pth = pathlib.Path('/') / 'dev' / 'null'
>>> open(pth)
<_io.TextIOWrapper name='/dev/null' mode='r' encoding='UTF-8'>
>>> fd = os.open('/dev/null', flags=os.O_RDONLY)
>>> open(fd)
<_io.TextIOWrapper name=8 mode='r' encoding='UTF-8'>
>>> _.close()
>>>
```


## The *mode* argument.

When a file is opened, several actions may be performed by the operating
system before the file is ready for use:
- a new, empty file is created
- the contents of the file are expunged (the file is truncated)
- the read/write position is set

The existence of the file and the value of the `mode` argument determine
which of these are performed.
The `mode` argument must be a string up to three characters in length
and must contains exactly one character from the set `rwax`.
The characters are known as *flags*.

| mode | file doesn't exist | file exists
|------|--------------------|----------------------------------------------
|  r   | ERROR              | read position set to start of file
|  w   | file is created    | file is truncated
|  a   | file is created    | write position set to end of file
|  x   | file is created    | ERROR

Clearly, if the file is created or truncated the write position is set to
the start of the (empty) file which is also the end of the file.

If the `mode` argument also contains a `'+'` flag, the above actions are
still performed but the file is opened for both reading and writing.
(So, `'w+'` will truncate the file, but `'r+'` and `'a+'` will not.)

The `mode` argument *also* determines whether the file is bytes-oriented
or string-oriented. (Demonstrating that the `mode` argument is overloaded.)
The orientation of the file is determined by the presence of one of the
`'b'` ot `'t'` flag.
If the `mode` argument contains a `'b'` flag, then the file is bytes-oriented; otherwise it is string-oriented even in the absence of the `'t'` flag.

If the `file` argument is a file descriptor (an integer),
the `mode` argument should agree with the file status flags of the file,
otherwise operations on the file will fail.
Note that Python doesn't check this during the call to `open()`.

In the following example, we open a file for reading using the low-level
`os.open()` function.
Then call the `open()` built-in with `mode='w'`.
We see that `read()` fails and `write()` succeeds -- but only because the
`write()` has populated the buffer. When we attempt to flush the buffer,
an exception is raised. We also get an exception when we attempt to
close the file (always a good test case).

```python
>>> import os
>>> fd = os.open('/dev/null', flags=os.O_RDONLY)
>>> fp = open(fd, 'w')
>>> fp.read()
Traceback (most recent call last):
  File "<pyshell#4>", line 1, in <module>
    fp.read()
io.UnsupportedOperation: not readable
>>> fp.write('something')
9
>>> fp.flush()
Traceback (most recent call last):
  File "<pyshell#6>", line 1, in <module>
    fp.flush()
OSError: [Errno 9] Bad file descriptor
>>> fp.close()
OSError: [Errno 9] Bad file descriptor

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<pyshell#7>", line 1, in <module>
    fp.close()
OSError: [Errno 9] Bad file descriptor
>>>
```


## The *buffering* argument.

The `buffering` argument must be an integer.
It can take one of three magic values, or the value of the size of the buffer to use. The three magic values are:
* 0 or False = no buffering. Only allowed for `'b'` mode.
* 1 or True = line buffering. Only allowed for `'t'` mode.
* -1 (actually any negative value) = default buffering.
  * if the file is a terminal, use line buffering, otherwise ...
  * use the underlying block size of the device or `os.DEFAULT_BUFFER_SIZE` as a fallback

The combination of the `mode` and `buffering` arguments determine what class
of object is returned by the `open()` built-in.

| class          | mode       | buffering  | comments
|----------------|------------|------------|----------
| FileIO         | `[rw][+]b` | 0          | unbuffered (raw)
| BufferedReader | `rb`       | -1, +ve    |
| BufferedWriter | `wb`       | -1, +ve    |
| BufferedRandom | `[rw]+b`   | -1, +ve    |
| TextIOWrapper  | `[rw][+]t` | 1, -1, +ve | buffered text


## The *encoding* and *errors* arguments.

The `encoding` and `errors` arguments are as for the `str()` and `bytes()` built-ins.
They must be strings or None.
If None is specified, the default values are used.
The `encoding` argument must be a valid encoding.
The `errors` argument is not checked for validity until an error needs to be handled.

If the `mode` contains a `'b'` flag and any of the `encoding` or `errors`
arguments are not None, then an exception is raised.
This is further evidence that the `'b'` and `'t'` flags are misplaced
and the arguments to the `open()` built-in are over-loaded.


## The *newline* argument.

The `newline` argument must be a string or None.
If it is a string, only four values are accepted: `'' '\n' '\r' '\r\n'`.
It is only valid if the `mode` argument does not contain the `'b'` flag.

The `newline` argument determines how the universal newline `'\n'` is
translated when reading/writing a file.

| `newline` | when reading | when writing |
|-----------|--------------|--------------|
|    None   | line endings translated to `'\n'` | `'\n'` translated to `os.linesep`
|    `''`   | no translation | no translation
|   `'\n'`  | line endings passed through | no translation
|   `'\r'`  | `'\r'` translated to `'\n'` | `'\n'` translated to `'\r'`
|   `'\r\n'`  | `'\r\n'` translated to `'\n'` | `'\n'` translated to `'\r\n'`

In the example below, we write a binary file with mixed line endings
then see how each of the valid `newline`  values handle each "line".

```python
>>> testdata = b'carriage return\rnewline\nboth\r\nboth again\r\n'
>>> with open('tempfile', 'wb') as wbstream:
        wbstream.write(testdata)

>>> for newline in None, '', '\n', '\r', '\r\n':
        with open('tempfile', newline=newline) as rstream:
            lines = rstream.readlines()
            print(f'{newline!r:6s} {lines}')

None   ['carriage return\n', 'newline\n', 'both\n', 'both again\n']
''     ['carriage return\r', 'newline\n', 'both\r\n', 'both again\r\n']
'\n'   ['carriage return\rnewline\n', 'both\r\n', 'both again\r\n']
'\r'   ['carriage return\r', 'newline\nboth\r', '\nboth again\r', '\n']
'\r\n' ['carriage return\rnewline\nboth\r\n', 'both again\r\n']
>>>
```


## The *closefd* argument.

The `closefd` argument must be an integer (it is treated as a boolean.)
It is only allowed to be False or zero if the `file` argument is a file
descriptor (an integer).
If the `file` argument is a `str`, `bytes` or path-like object then `closefd`
must be a non-zero integer. The default value is True.


## The *opener* argument.

The `opener` argument must be either None or a callable taking two arguments
(`pathname`, `flags`). It can be used as a mechanism to provide an underlying
open file descriptor. So, therefore, must return that open file descriptor.

The example below simply wraps a call to `os.open()` to provide an open
file descriptor.

```python
>>> import os
>>> def opener(filename, flags):
        print(f'Opening {filename} with {flags=:#o}')
        return os.open(filename, flags)

>>> with open('anyfile', 'wb', buffering=0, opener=opener): pass

Opening anyfile with flags=0o100003001
>>> with open('anyfile', opener=opener): pass

Opening anyfile with flags=0o100000000
>>> with open('anyfile', 'r+', opener=opener): pass

Opening anyfile with flags=0o100000002
>>> with open('nonsuch', 'x', opener=opener): pass

Opening nonsuch with flags=0o100005001
>>>
```

If the `file` argument is a file descriptor (an integer),
then the `opener` argument is ignored.


## Summary of arguments.

The `open()` built-in can be used to provide a file object for various scenarios:
- text
- bytes (possibly unbuffered)
- wrapping an open text file
- wrapping an open binary file

The following table summarises which arguments can be used with which scenarios
and also provides the default values for each argument.

| scenario | file | mode | buffering | encoding | errors | newline | closefd | opener |
|----------|------|------|-----------|----------|--------|---------|---------|--------|
| default | | 'r' | -1 | None | None | None | True | None |
| text | path | must not include 'b' | non-zero | any | any | any | True | any |
| wrapped text | integer | must not include 'b' | non-zero | any | any | any | any | ignored |
| bytes | path | must include 'b' | non-one | None | None | None | True | any |
| wrapped bytes | integer | must include 'b' | non-one | None | None | None | any | ignored |

The different scenarios could be realised by replacing `open()` with some
specialised functions:
* `opentext(file, mode='r', buffering=None, encoding=None, errors=None, newline=None, opener=None)`
* `textio(fd, buffering=None, encoding=None, errors=None, newline=None, closefd=True)`
* `openbinary(file, mode='r', buffering=None, opener=None)`
* `binaryio(fd, buffering=None, closefd=True)`

Note that:
* the `mode` argument to `opentext()` and `openbinary()` would not require/accept a `'b'` or `'t'` flag.
* the `textio()` and `binaryio()` functions do not accept a `mode` argument.
* the `buffering` argument:
    * uses None in place of `-1`
    * only accepts non-negative integers
    * the values `0` and `1` are still special but should be replaced by named constants
