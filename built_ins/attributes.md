# Attributes of objects

This section deals with built-ins that relate to attributes of objects.

- hasattr()
- getattr()
- setattr()
- delattr()
- dir(object)
- vars(object)


# The *hasattr()* built-in.

The `hasattr()` built-in does not accept keyword arguments but takes two
positional arguments (`object`, `name`).
It returns True if the given name
(which must be a string)
is an attribute of the given object or class.

```python
>>> hasattr(0j, 'real')
True
>>> hasattr(complex, 'real')
True
>>>
```

The `hasattr()` built-in is implemented by calling `getattr()` (see below)
and checking whether it raises `AttributeError`.
This means that for certain applications where `__getattr__` performs some
sort of fetch (from a database or a remote device, say) that `hasattr()`
is as slow as `getattr()`.


# The *getattr()* built-in.

The `getattr()` built-in does not accept keyword arguments but takes two
or three
positional arguments (`object`, `name`, `default`).
It returns the value of the attribute with the given name
(which must be a string)
if the given object has such an attribute.
If the object does not have an attribute with that name:
- an `AttributeError` exception is raised, unless
- the `default` is given, in which case that value is returned.

```python
>>> obj = range(10)
>>> getattr(obj, 'stop')
10
>>> getattr(obj, 'ſtop')
Traceback (most recent call last):
  File "<pyshell#2>", line 1, in <module>
    getattr(obj, 'ſtop')
AttributeError: 'range' object has no attribute 'ſtop'
>>> getattr(obj, 'ſtop', -1)
-1
>>> getattr(obj, 'ſtop', obj.ſtop)
10
>>>
```

The above example demonstrates an asymmetry between
- object.attribute
- getattr(object, 'attribute')

in that the former performs normalisation and the latter doesn't.
This means that `getattr` will not find the attribute if Python normalised
the name when setting the attribute but `getattr` is using the un-normalised
name.

In the example below, we assign an attribute `tempºC`
and demonstrate that we can access it via `object.tempºC`
but not via `getattr(object, 'tempºC')`.

```python
>>> Anon = type('Anon', (), {})
>>> anon = Anon()
>>> anon.tempºC = -273.15
>>> print(anon.tempºC)
-273.15
>>> getattr(anon, 'tempºC')
Traceback (most recent call last):
  File "<pyshell#5>", line 1, in <module>
    getattr(anon, 'tempºC')
AttributeError: 'Anon' object has no attribute 'tempºC'
>>>
```

By inspecting the object's `vars` we see that the attribute's name has been
normalised to `tempoC` ...

```python
>>> vars(anon)
{'tempoC': -273.15}
>>> print(anon.tempoC)
-273.15
>>> getattr(anon, 'tempoC')
-273.15
>>> import unicodedata
>>> getattr(anon, unicodedata.normalize('NFKC', 'tempºC'))
-273.15
>>>
```

Python's normalisation of attribute names can cause objects to be given
attributes that it would not normally be allowed (because they are keywords).

```python
>>> Anon = type('Anon', (), {})
>>> anon = Anon()
>>> anon.paſs = 'I am pass'
>>> anon.ﬁnally = 'I am finally'
>>> vars(anon)
{'pass': 'I am pass', 'finally': 'I am finally'}
>>>
```

These attributes can't be accessed via `anon.pass` or `anon.finally`
because Python would raise a `SyntaxError`, but if they were accessed via
`getattr` then only `getattr(anon, 'pass')` and `getattr(anon, 'finally')`
would succeed.

Note that because `hasattr` simply uses `getattr`,
the normalisation asymmetry applies equally to `hasattr` as it does to `getattr`.


# The *setattr()* built-in.

The `setattr()` built-in does not accept keyword arguments but takes three
positional arguments (`object`, `name`, `value`).
It sets the given attribute to the given value providing the object allows it
(objects may have read-only attributes or may not allow arbitrary attributes
to be assigned.)
If the attribute already exists, its value is overwritten;
otherwise a new attribute is assigned to the object.

Like the `getattr()` built-in, the `setattr()` built-in does not perform
normalisation of the attribute name. This can cause an object to be assigned
a new attribute when the intention was to overwrite an existing one.

```python
>>> Anon = type('Anon', (), {})
>>> anon = Anon()
>>> anon.tempºC = 273.15
>>> setattr(anon, 'tempºC', 0.0)
>>> anon.tempºC
273.15
>>> vars(anon)
{'tempoC': 273.15, 'tempºC': 0.0}
>>>
```

The `setattr()` built-in allows attribute names that would otherwise be
illegal.

```python
>>> setattr(anon, 'None', None)
>>> setattr(anon, '1', 1)
>>> setattr(anon, '', 'blank')
>>> vars(anon)
{'tempoC': 273.15, 'tempºC': 0.0, 'None': None, '1': 1, '': 'blank'}
>>>
```

The `setattr()` built-in can be used to add or change an object's methods.
But for the change to take effect, the object's *class* needs the new or updated
method, not the object instance.
This means that all objects of that class will get the new or updated method.

```python
>>> Anon = type('Anon', (), {})
>>> anon, other = Anon(), Anon()
>>> setattr(anon.__class__, 'meth', lambda self:hex(id(self)))
>>> anon.meth()
'0x10e37afd0'
>>> other.meth()
'0x10e363040'
>>>
```

If a function is set as an attribute on an object instance,
it remains a plain function and does not take the object instance as an
implicit first argument.

```python
>>> Anon = type('Anon', (), {})
>>> anon = Anon()
>>> setattr(anon, 'func', lambda *a:f'You gave me {len(a)} args')
>>> anon.func()
'You gave me 0 args'
>>>
```

This allows us to assign bound methods of other objects as function
attributes of an object.
In the following example, an object "spies" on the length of an external
object without holding an explicit reference to the object.
(However, since it holds a reference to that object's bound method, it
keeps the object alive.)

```python
>>> Anon = type('Anon', (), {})
>>> anon = Anon()
>>> mylist = []
>>> setattr(anon, 'spy', mylist.__len__)
>>> anon.spy()
0
>>> mylist.extend(range(3))
>>> anon.spy()
3
>>> del mylist
>>> anon.spy()
3
>>>
```


# The *delattr()* built-in.

The `delattr()` built-in does not accept keyword arguments but takes two
positional arguments (`object`, `name`).
It removes the given attribute from the object if it exists and if the object
allows it.
The same normalisation restrictions apply to `delattr` as they do to `getattr`.

```python
>>> Anon = type('Anon', (), {})
>>> anon = Anon()
>>> anon.paſs = 'I am pass'
>>> delattr(anon, 'paſs')
Traceback (most recent call last):
  File "<pyshell#4>", line 1, in <module>
    delattr(anon, 'paſs')
AttributeError: paſs
>>> delattr(anon, 'pass')
>>>
```


# The *vars()* built-in with one argument.

The `vars()` built-in does not accept keyword arguments;
but when passed one positional argument it returns the `__dict__` attribute
for the given object if it has one;
otherwise it raises a `TypeError`.

```python
>>> Anon = type('Anon', (), {})
>>> anon = Anon()
>>> vars(anon)
{}
>>> vars(Anon)
mappingproxy({'__module__': '__main__', '__dict__': <attribute '__dict__' of 'Anon' objects>, '__weakref__': <attribute '__weakref__' of 'Anon' objects>, '__doc__': None})
>>> import sys
>>> vars(sys)
Squeezed text (375 lines).
>>> vars(object())
Traceback (most recent call last):
  File "<pyshell#7>", line 1, in <module>
    vars(object())
TypeError: vars() argument must have __dict__ attribute
>>>
```


# The *dir()* built-in with one argument.

The `dir()` built-in does not accept keyword arguments;
but when passed one positional argument it returns a sorted list of attributes
of that object.
If the object has a `__dir__` method, it is used to construct the return value.
Otherwise, the `dir()` built-in uses the object's `__dict__` and the
attributes of the object's type.

```python
>>> dir(0j)
['__abs__', '__add__', '__bool__', '__class__', '__delattr__', '__dir__', '__divmod__', '__doc__', '__eq__', '__float__', '__floordiv__', '__format__', '__ge__', '__getattribute__', '__getnewargs__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__int__', '__le__', '__lt__', '__mod__', '__mul__', '__ne__', '__neg__', '__new__', '__pos__', '__pow__', '__radd__', '__rdivmod__', '__reduce__', '__reduce_ex__', '__repr__', '__rfloordiv__', '__rmod__', '__rmul__', '__rpow__', '__rsub__', '__rtruediv__', '__setattr__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', '__truediv__', 'conjugate', 'imag', 'real']
>>> dir(range(1))
['__bool__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'count', 'index', 'start', 'step', 'stop']
>>>
```

Messing with an object's `__dict__` can break the `dir()` built-in.

```python
>>> anon = type('Anon', (), {})()
>>> anon.__dict__[0] = 'Zero'
>>> dir(anon)
Traceback (most recent call last):
  File "<pyshell#3>", line 1, in <module>
    dir(anon)
TypeError: '<' not supported between instances of 'str' and 'int'
>>>
```
