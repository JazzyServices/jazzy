"""jazzy.py
Utilities you didn't realise you needed but can't live without.

The functions in this module are independent of all imports.
So DON'T add a function to this module that requires an import statement.
Not even `import sys`.
This means that we can't check sys.version
"""

if 'unicode' not in __builtins__:
    unicode = str

def to_unicode(obj):
    'Convert an object to (its) Unicode (representation).'
    # Unicode is already Unicode
    if isinstance(obj, unicode):
        return obj

    # Try to decode it
    try:
        return obj.decode('utf8')
    except UnicodeDecodeError:
        # Since every byte in a Latin-1 sequence is decodable we shouldn't
        # get a decoding error here
        return obj.decode('latin1')
    except (AttributeError, TypeError):
        # The object doesn't have a callable decode method.
        pass

    # try the object's __unicode__ method
    # but if that fails, use its id
    try:
        return unicode(obj)
    except UnicodeDecodeError:
        return u'<{}#{:#x}>'.format(obj.__class__.__name__, id(obj))

def iter_to_unicode(it):
    return iter(to_unicode(a) for a in it)

def tjoin(*args):
    'Join the args into a tuple.'
    return args

