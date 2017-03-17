import re
import sys
import unittest

import context
from jazzy import to_unicode


class Test_toUnicode(unittest.TestCase):

    def test_unicode(I):
        datum = u'unicode'
        converted = to_unicode(datum)
        I.assertEqual(datum, converted)
        I.assertTrue(datum is converted)

    def test_decode_non_method(I):
        # a non-callable decode won't get called
        class X:
            decode = 'not a function'
            if (sys.version_info.major >= 3):
                def __str__(my):
                    return 'I am Unicode\u2026'
            else:
                def __unicode__(my):
                    return u'I am Unicode\u2026'
        datum = X()
        converted = to_unicode(datum)
        I.assertEqual(u'I am Unicode\u2026', converted)

    def test_several(I):
        data = [
            (None, u'None'),
            (123, u'123'),
            (3.14159, u'3.14159'),
            (b'ascii', u'ascii'),
            (b'L\xc1tin1', u'L\xc1tin1'),
            (b'utf\xe2\x80\x928', u'utf\u20128'),
        ]
        for datum, exp in data:
            ans = to_unicode(datum)
            I.assertEqual(ans, exp)

    def test_bare_class(I):
        class Bare(object):
            pass
        # Bare class
        ans = to_unicode(Bare)
        I.assertTrue(ans.startswith('<class '))
        I.assertTrue(ans.endswith(".Bare'>"))
        m = re.match(r"<class.*\.Bare'>$", ans)
        I.assertTrue(bool(m))
        # Bare object
        ans = to_unicode(Bare())
        m = re.match(r"<.*\.Bare object at .*>$", ans)
        I.assertTrue(bool(m))

    if (sys.version_info.major < 3):
        def test_bad_repr(I):
            'Test that an object with a __repr__ that returns Latin1.'
            class BadRepr(object):
                def __repr__(my):
                    return '\xfe\xff'
            ans = to_unicode(BadRepr())
            m = re.match(r"<BadRepr#0x[0-9a-f]+>$", ans)
            I.assertTrue(bool(m))

if __name__ == '__main__':
    unittest.main()
