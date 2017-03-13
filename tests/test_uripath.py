import os
import unittest

from context import uripath


class Test_Module(unittest.TestCase):
    'Tests for the uripath module itself.'

    def test_globals(I):
        'Test uripath globals.'
        I.assertTrue(uripath.sep == '/')
        I.assertTrue(uripath.curdir == '.')

    def test_attributes(I):
        'Test uripath attributes.'
        I.assertTrue(hasattr(uripath, 'UPath'))


class UPathTestCase(unittest.TestCase):
    'Wrapper class for UPathTests.'

    def assertIsRoot(I, sut):
        'Assert that SUT is the root path "/" .'
        I.assertTrue(isinstance(sut, uripath.RootUPath))
        I.assertTrue(uripath.isUPath(sut))
        I.assertTrue(str(sut) == '/')
        I.assertTrue(sut == '/')

    def assertIsDot(I, sut):
        'Assert that SUT is the current path "." .'
        I.assertTrue(isinstance(sut, uripath._RelativeUPath))
        I.assertTrue(sut == '.')

    def assertEmptyString(I, sut):
        'Assert that SUT is the empty string.'
        I.assertTrue(isinstance(sut, str))
        I.assertTrue(sut == '')

    def assertUPath(I, sut, value, length=None):
        'Assert that SUT is a UPath with the given value and length.'
        I.assertTrue(uripath.isUPath(sut))
        I.assertTrue(sut == value, '[{}] v [{}]'.format(sut, value))
        if length is not None:
            I.assertTrue(len(sut) == length)


class Test_RootUPath(UPathTestCase):
    'Tests for the Root Path "/" .'

    def test_ctor(I):
        'Test RootUPath()'
        p = uripath.RootUPath()
        I.assertTrue(uripath.isUPath(p))
        I.assertTrue(str(p) == '/')

    def test_slash(I):
        'Test UPath("/").'
        p = uripath.UPath('/')
        I.assertIsRoot(p)

    def test_slashslash(I):
        'Test UPath("//").'
        p = uripath.UPath('//')
        I.assertIsRoot(p)

    def test_eq(I):
        'Test that we __cmp__ against strings'
        p = uripath.UPath('/')
        I.assertTrue(p == '/')

    def test_dirname(I):
        'Test that the dirname of "/" is "/" .'
        p = uripath.UPath('/')[:-1]
        I.assertIsRoot(p)

    def test_dirname0(I):
        'Test that the dirname of "/" is "/" using explicit slice[0:-1].'
        p = uripath.UPath('/')[0:-1]
        I.assertIsRoot(p)

    def test_whole(I):
        'Test that a full slice [:] of "/" is "/" .'
        p = uripath.UPath('/')[:]
        I.assertIsRoot(p)

    def test_whole0(I):
        'Test that a full slice [0:] of "/" is "/" .'
        p = uripath.UPath('/')[0:]
        I.assertIsRoot(p)

    def test_item0(I):
        'Test that the 0th item of "/" is "/" .'
        p = uripath.UPath('/')[0]
        I.assertIsRoot(p)

    def test_filename(I):
        'Test that the basename of "/" is the empty string.'
        f = uripath.UPath('/')[-1]
        I.assertEmptyString(f)

    def test_length(I):
        'Length is the number of components, so is 1.'
        slash= uripath.UPath('/')
        I.assertTrue(len(slash) == 1)
        slashslash= uripath.UPath('//')
        I.assertTrue(len(slashslash) == 1)

    def test_rejoin(I):
        'Test that dirname(x) + filename(x) is always x.'
        d = uripath.UPath('/')[:-1]
        f = uripath.UPath('/')[-1]
        j = d / f
        I.assertIsRoot(j)

    def test_parent(I):
        'Test that the parent of / is /'
        p = uripath.UPath('/') / '..'
        I.assertIsRoot(p)

    def test_join_dot(I):
        'Test that /. is /'
        p = uripath.UPath('/') / '.'
        I.assertIsRoot(p)

    def test_join_root(I):
        "Test that we can't join root on rhs."
        p = uripath.UPath('/')
        with I.assertRaises(RuntimeError):
            bad = p / p


class Test_DotUPath(UPathTestCase):
    'Tests for "." (current directory).'

    def test_dflt(I):
        'Test that an arg-less UPath is "." (dot).'
        p = uripath.UPath()
        I.assertIsDot(p)

    def test_dot(I):
        'Test constructing using "." (dot).'
        p = uripath.UPath('.')
        I.assertIsDot(p)

    def test_None(I):
        'Test constructing using None.'
        p = uripath.UPath(None)
        I.assertIsDot(p)

    def test_eq(I):
        'Test that we __cmp__ against strings'
        p = uripath.UPath('.')
        I.assertTrue(p == '.')

    def test_dirname(I):
        'Test that the dirname of "." is the empty string.'
        p = uripath.UPath('.')
        I.assertEmptyString(p[:-1])
        I.assertEmptyString(p[0:-1])

    def test_whole(I):
        'Test that a full slice [:] of "." is "." .'
        p = uripath.UPath('.')
        I.assertIsDot(p[:])
        I.assertIsDot(p[0:])

    def test_item0(I):
        'Test that the 0th item of "." is "." .'
        p = uripath.UPath('.')
        I.assertIsDot(p[0])

    def test_filename(I):
        'Test that the filename part of "." is "." .'
        p = uripath.UPath('.')[-1]
        I.assertIsDot(p)

    def test_length(I):
        'Length is the number of components, so is 1.'
        p = uripath.UPath('.')
        I.assertTrue(len(p) == 1)

    def test_rejoin(I):
        'Test that dirname(x) + filename(x) is always x.'
        d = uripath.UPath('.')[:-1]
        f = uripath.UPath('.')[-1]
        j = d / f
        I.assertEmptyString(d)
        I.assertIsDot(j)

    def test_parent(I):
        'Test that the parent of . is ..'
        p = uripath.UPath('.') / '..'
        I.assertTrue(isinstance(p, uripath._RelativeUPath))
        I.assertTrue(p == '..')

    def test_join_dot(I):
        'Test that "./." is still "." .'
        p = uripath.UPath('.') / '.'
        I.assertIsDot(p)
        p = '.' / uripath.UPath('.')
        I.assertIsDot(p)

    def test_join_dotslash(I):
        'Test that /. is /'
        p = uripath.UPath('/') / uripath.UPath('.')
        I.assertIsRoot(p)
        p = '/' / uripath.UPath('.')
        I.assertIsRoot(p)


class Test_AbsoluteUPath(UPathTestCase):
    'Tests for absolute paths.'

    def test_abs_toplevel(I):
        'Test a top-level absolute path.'
        p = uripath.UPath('/tmp')
        I.assertUPath(p, '/tmp', 2)
        # checks for subscription
        I.assertUPath(p[0], '/')
        I.assertUPath(p[1], 'tmp')
        I.assertUPath(p[-1], 'tmp')
        with I.assertRaises(IndexError):
            p[2]
        # checks for slicing
        I.assertUPath(p[:], '/tmp')
        I.assertUPath(p[0:], '/tmp')
        I.assertIsRoot(p[:-1])
        I.assertIsRoot(p[0:-1])
        I.assertUPath(p[1:], 'tmp')
        I.assertEmptyString(p[2:])

    def test_abs_multi(I):
        'Test a multi-part absolute path.'
        p = uripath.UPath('/var/tmp')
        I.assertUPath(p, '/var/tmp', 3)
        # checks for subscription
        I.assertUPath(p[0], '/')
        I.assertUPath(p[1], 'var')
        I.assertUPath(p[2], 'tmp')
        I.assertUPath(p[-1], 'tmp')
        I.assertUPath(p[-2], 'var')
        I.assertUPath(p[-3], '/')
        with I.assertRaises(IndexError):
            p[3]
        # checks for slicing
        I.assertUPath(p[:], '/var/tmp')
        I.assertUPath(p[0:], '/var/tmp')
        I.assertUPath(p[:-1], '/var')
        I.assertUPath(p[0:-1], '/var')
        I.assertUPath(p[1:], 'var/tmp')
        I.assertUPath(p[2:], 'tmp')

    def test_abs_join1(I):
        'Test joining absolute path with string.'
        p = uripath.UPath('/var/tmp') / 'daff0d1'
        I.assertUPath(p, '/var/tmp/daff0d1', 4)
        I.assertUPath(p[0], '/')
        I.assertUPath(p[-1], 'daff0d1')

    def test_abs_join2(I):
        'Test joining a path to change one component.'
        p = uripath.UPath('/var/tmp')
        # we can't assign via subscription
        with I.assertRaises(TypeError):
            p[1] = 'local'
        # but we can do it using path joining
        q = p[:1] / 'local' / p[2:]
        I.assertUPath(q, '/local/tmp')

    def test_join_abs_abs(I):
        "Test that we can't join absolute path on the rhs."
        p = uripath.UPath('/usr/local')
        q = uripath.UPath('/bin/python')
        with I.assertRaises(RuntimeError):
            bad = p / q
        with I.assertRaises(RuntimeError):
            bad = p / '/lib/std'
        with I.assertRaises(RuntimeError):
            bad = '/usr' / q
        j = p / q[1:]
        I.assertUPath(j, '/usr/local/bin/python')


class Test_RelativeUPath(UPathTestCase):
    'Tests for relative paths.'

    def test_rel_one(I):
        'Test a single-part relative path.'
        p = uripath.UPath('.ssh')
        I.assertUPath(p, '.ssh', 1)
        # checks for subscription
        I.assertUPath(p[0], '.ssh')
        I.assertUPath(p[-1], '.ssh')
        with I.assertRaises(IndexError):
            p[1]
        # checks for slicing
        I.assertUPath(p[:], '.ssh')
        I.assertUPath(p[0:], '.ssh')
        I.assertEmptyString(p[:-1])
        I.assertEmptyString(p[0:-1])
        I.assertEmptyString(p[1:])

    def test_rel_long(I):
        'Test a multi-part relative path.'
        p = uripath.UPath('lib/python2.7/site-packages')
        I.assertUPath(p, 'lib/python2.7/site-packages', 3)
        # checks for subscription
        I.assertUPath(p[0], 'lib')
        I.assertUPath(p[1], 'python2.7')
        I.assertUPath(p[2], 'site-packages')
        I.assertUPath(p[-1], 'site-packages')
        I.assertUPath(p[-2], 'python2.7')
        I.assertUPath(p[-3], 'lib')
        with I.assertRaises(IndexError):
            p[3]
        # checks for slicing
        I.assertUPath(p[:], 'lib/python2.7/site-packages')
        I.assertUPath(p[0:], 'lib/python2.7/site-packages')
        I.assertUPath(p[:-1], 'lib/python2.7')
        I.assertUPath(p[0:-1], 'lib/python2.7')
        I.assertUPath(p[1:], 'python2.7/site-packages')
        I.assertUPath(p[2:], 'site-packages')

    def test_rel_join(I):
        'Test joining relative paths.'
        pyt = uripath.UPath('python2.7')
        lib = uripath.UPath('lib')
        # => python2.7/lib
        pytlib = pyt / lib
        I.assertUPath(pytlib, 'python2.7/lib', 2)
        # => lib/python2.7
        libpyt = lib / pyt
        I.assertUPath(libpyt, 'lib/python2.7', 2)
        # check we can prepend a string
        ulp = 'usr' / libpyt
        I.assertUPath(ulp, 'usr/lib/python2.7', 3)
        # check we can append strings
        pkg = 'jazzy'
        ulpsj = ulp / 'site-packages' / pkg
        I.assertUPath(ulpsj, 'usr/lib/python2.7/site-packages/jazzy', 5)
        # check we can append string paths
        u = uripath.UPath('usr')
        pth = u / 'local/lib' / pyt / 'site-packages/jazzy/jazzy.py'
        I.assertUPath(pth, 'usr/local/lib/python2.7/site-packages/jazzy/jazzy.py', 7)

    def test_abs_rel_join(I):
        'Join absolute and relative paths.'
        abso = uripath.UPath('/usr/local/lib')
        rel = uripath.UPath('python2.7/site-packages')
        # check joining Absolute, Relative and string
        pth = abso / rel / 'jazzy'
        I.assertUPath(pth, '/usr/local/lib/python2.7/site-packages/jazzy', 7)
        # string + relative
        pth = '/tmp' / rel
        I.assertUPath(pth, '/tmp/python2.7/site-packages', 4)


class Test_UPath_Iter(unittest.TestCase):
    'Test that a UPath is an iterator.'

    def test_iter_append(I):
        'Test UPath as an iter using list append.'
        p = uripath.UPath('/usr/local/lib/python2.7/site-packages/jazzy')
        # old-fashioned append
        a = []
        for part in p:
            a.append(part)
        I.assertTrue(len(a) == len(p))
        I.assertTrue(isinstance(a[0], uripath.RootUPath))
        I.assertTrue( all(uripath.isUPath(i) for i in a) )
        I.assertTrue( all(a[i] == p[i] for i in range(7)))
        I.assertTrue( all(i==j for i,j in zip(a,p)))

    def test_iter_to_list(I):
        'Test UPath as an iter by converting to list.'
        p = uripath.UPath('/usr/local/lib/python2.7/site-packages/jazzy')
        # convert UPath to list
        a = list(p)
        I.assertTrue(len(a) == len(p))
        I.assertTrue(isinstance(a[0], uripath.RootUPath))
        I.assertTrue( all(uripath.isUPath(i) for i in a) )
        I.assertTrue( all(a[i] == p[i] for i in range(7)) )
        I.assertTrue( all(i==j for i,j in zip(a,p)) )


class Test_UPath_Unicode(UPathTestCase):
    'Test UPaths made from unicode strings.'

    def test_unicode_1(I):
        'Test a unicode path.'
        u = u'utf\u20128'
        p = uripath.UPath(u)
        I.assertUPath(p, 'utf\xe2\x80\x928', 1)
        I.assertTrue(p == u'utf\u20128')

    def test_unicode_2(I):
        'Test a path with unicode separators.'
        u = u'/top/\u002e\u002e\u002fevil'
        p = uripath.UPath(u)
        I.assertUPath(p, '/evil', 2)

    def test_unicode_3(I):
        'Test joining a unicode path.'
        top = uripath.UPath('/tmp/xxa55')
        u = u'utf\u20128'
        p = top / u
        I.assertUPath(p, '/tmp/xxa55/utf\xe2\x80\x928', 4)
        I.assertTrue(p[-1] == u'utf\u20128')


if __name__ == '__main__':
    unittest.main()
