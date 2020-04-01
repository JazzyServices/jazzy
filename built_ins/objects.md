# General objects and types

This section deals with built-ins that relate to objects in general.

- object()
- type(object)
- id()
- hash()
- issubclass() and isinstance()
- callable()


# The *object()* built-in.

The `object()` built-in is not a function but a type.
It takes no arguments and returns a new featureless object that has few
useful properties.
Plain objects are hashable, however, so there may be cases where a plain
object can be used as a unique key, say.


# The *type()* built-in with one argument.

When exactly one argument is passed to the `type()` built-in
the return value is the type of the given argument.

```python
>>> type(False)
<class 'bool'>
>>> type(False + True)
<class 'int'>
>>> type(False / True)
<class 'float'>
>>> type(False * ())
<class 'tuple'>
>>>
```

The `type()` built-in should generally not be used to check the type of an
object (use the `isinstance()` built-in for that)
*unless* there is a necessity for checking that an object is actually an
instance of a root class.

```python
>>> def typetree(obj):
        typ = type(obj)
        while typ != object:
            print(typ.__name__, end=', ')
            typ = typ.__bases__[0]
        print(typ.__name__)

>>> typetree(TabError())
TabError, IndentationError, SyntaxError, Exception, BaseException, object
>>> typetree(True)
bool, int, object
>>> typetree(object())
object
>>>
```


# The *id()* built-in.

The `id()` built-in does not accept keyword arguments but takes one
positional argument which is any object.
It returns an integer which is the unique identity of that object.
Note that once an object has been garbage-collected, a different object may
be assigned the same `id`.

```python
>>> id(0.0)
4533298192
>>> id(-0.0)
4533300272
>>> id(0.0 == -0.0)
4527468456
>>> id(True)
4527468456
>>>
```


# The *hash()* built-in.

The `hash()` built-in does not accept keyword arguments but takes one
positional argument which is any object.
If the object has a `__hash__` method it is called to provide the return
value to the `hash()` built-in; otherwise an exception is raised.
The returned value is an integer.
Objects that compare equal should have the same hash value.

```python
>>> hash(False) == hash(0) == hash(0.0) == hash(-0.0) == hash(0j) == hash('')
True
>>>
```


# The *issubclass()* and *isinstance()* built-ins.

The `issubclass()` and `isinstance()` built-ins accept no keywords arguments,
but take exactly two positional arguments.
- for the `issubclass()` built-in, the first argument is a class,
- for the `isinstance()` built-in, the first argument is an object,
- for both built-ins the second argument is
  - a class, or
  - a (nested) tuple of classes

A class is considered a subclass of itself.

```python
>>> issubclass(bool, bool)
True
>>> issubclass(bool, int)
True
>>> issubclass(bool, (str, float, (int, bytes)))
True
>>> isinstance(True, int)
True
>>> isinstance(10, (str, float, (int, bytes)))
True
>>>
```

The `issubclass()` and `isinstance()` built-ins also work for the
abstract base classes defined in `numbers` and `collections.abc`
as well as the definitions in `types`.

```python
>>> import numbers, collections.abc, types
>>> issubclass(bool, numbers.Integral)
True
>>> isinstance(True, numbers.Integral)
True
>>> issubclass(str, collections.abc.Sequence)
True
>>> isinstance('bob', collections.abc.Sequence)
True
>>> isinstance(lambda *a:a, types.FunctionType)
True
>>>
```


# The *callable()* built-in.

The `callable()` built-in does not accept keyword arguments but takes one positional argument which is any object.
The returned value is True if the object is a callable (a function, a method,
a class or an instance with a `__call__` method).

```python
>>> callable(min)
True
>>> callable(int)
True
>>> callable(bytes.fromhex)
True
>>> callable(lambda *a:a)
True
>>>
```
