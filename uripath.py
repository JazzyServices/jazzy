"""
A URI has the following form:
scheme:[//[user:password@]host[:port]][/]path[?query][#fragment]

This module handles the "path" part of a URI
Paths also appear in filesystem (obvs) so this module can handle those as well

UPaths are created by passing a pathname to the constructor:
E.g
    pwd = UPath(os.getcwd())

UPaths can be concatenated together using the '/' operator (__div__ method)
UPaths can also be concatenated with strings
E.g
>>> abso = UPath('/usr/lib')
>>> rel = UPath('python2.7/site-packages')
>>> abso / rel
UPath('/usr/lib/python2.7/site-packages')
>>> abso / "ruby/gems"
UPath('/usr/lib/ruby/gems')
>>> "~/local" / rel
UPath('~/local/python2.7/site-packages')

The dirname and basename can be extracted using slicing/subscription
E.g
>>> u = UPath('/usr/lib/python2.7/site-packages/uripath.py')
>>> dirn = u[:-1]
>>> dirn
UPath('/usr/lib/python2.7/site-packages')
>>> base = u[-1]
>>> base
UPath('uripath.py')
"""
import os.path

# if you need to make this module OS-specific (rather than for URIs)
# set these variables after importing the uripath module:-
#   uripath.sep = os.sep
#   uripath.curdir = os.curdir
sep = '/'
curdir = '.'


class _UPath(object):
    """A Universal Path; for use in URIs and filesystem paths."""
    def __init__(self, norma):
        self.normalised = norma

    def _appendpath(self, other):
        'Generate a new UPath by joining self to other'
        other = _otherpath(other)
        if os.path.isabs(other):
            raise RuntimeError("Can't append absolute path %s" % other)
        return UPath(
            os.path.join(
                self.normalised,
                other
            )
        )

    def _prependpath(self, other):
        'Generate a new UPath by joining other to self'
        if os.path.isabs(self.normalised):
            raise RuntimeError("Can't append %s to absolute path" % other)
        other = _otherpath(other)
        return UPath(
            os.path.join(
                other,
                self.normalised
            )
        )

    def __div__(self, other):
        return self._appendpath(other)

    def __truediv__(self, other):
        return self._appendpath(other)

    def __rdiv__(self, other):
        return self._prependpath(other)

    def __cmp__(self, other):
        other = _otherpath(other)
        return cmp(self.normalised, other)

    def __hash__(self):
        return hash(self.normalised)

    def __len__(self):
        return len(self.normalised)

    def __str__(self):
        return self.normalised

    def __unicode__(self):
        return self.normalised.decode('utf-8')

    def __repr__(self):
        return 'UPath(%s)' % repr(self.normalised)


class RootUPath(_UPath):
    """The root path '/'

    Since dirname('/') is still '/',
    and in most cases a slice [:-1] would give us the dirname of a path
    we need to ensure slicing '/' gives us the same result.
    """
    def __init__(self):
        _UPath.__init__(self, sep)

    def __getitem__(self, key):
        if isinstance(key, slice):
            if key.start in (0, None) and key.stop in (-1, None):
                ans = sep
            else:
                sli = [''].__getitem__(key)
                ans = sep.join(sli)
        elif key == 0:
            ans = sep
        else:
            ans = [''][key]
        return UPath(ans) if ans != '' else ans

    def __len__(self):
        return 1


class _NonRootUPath(_UPath):
    def __init__(self, norm):
        _UPath.__init__(self, norm)
        self.split = self.normalised.split(sep)

    def __getitem__(self, key):
        if isinstance(key, slice):
            sli = self.split.__getitem__(key)
            ans = sep.join(sli) if sli != [''] else sep
        else:
            ans = self.split[key]
            if ans == '':
                ans = sep
        return UPath(ans) if ans else ''

    def __len__(self):
        return len(self.split)


class AbsoluteUPath(_NonRootUPath):
    def __init__(self, norm):
        _NonRootUPath.__init__(self, norm)


class RelativeUPath(_NonRootUPath):
    def __init__(self, norm):
        _NonRootUPath.__init__(self, norm)


_AbsoluteUPath = AbsoluteUPath
_RelativeUPath = RelativeUPath
del AbsoluteUPath, RelativeUPath

def _otherpath(other):
    if isUPath(other):
        other = other.normalised
    elif isinstance(other, unicode):
        other = other.encode('utf-8')
    elif not isinstance(other, str):
        raise RuntimeError('bad arg [%s] type %s' % (other, type(other)))
    return other


def isUPath(obj):
    return isinstance(obj, _UPath)


def UPath(other=None):
    """UPath factory."""
    if other is None:
        other = curdir

    other = _otherpath(other)
    norm = os.path.normpath(other)

    if norm == '/' or norm == '//':
        return RootUPath()
    elif norm[0] == '/':
        return _AbsoluteUPath(norm)
    else:
        return _RelativeUPath(norm)
