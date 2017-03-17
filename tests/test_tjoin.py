"""Unit tests for tjoin.

Copyright (c) Jazzy Services Limited 2017
License: ../LICENSE

The main use case for such a simple function is to prefix an existing tuple.
So instead of saying:
    ans = (prefix,) + atuple
we say:
    ans = tjoin(prefix, *atuple)

"""
import unittest

import context
from jazzy import tjoin


class Test_TJoin(unittest.TestCase):

    def test_main_use_case(I):
        'Test the main use case.'
        args = ('myfile.txt', 'rw', 1048576, 'utf-8')
        sut = tjoin('prefix', *args)
        expected = ('prefix',) + args
        I.assertEqual(sut, expected)

    def test_main_it(I):
        'Test iterator to tuple.'
        sut = tjoin(0, *(i*i for i in range(1,5)))
        exp = (0,) + tuple(i*i for i in range(1,5))
        I.assertEqual(sut, exp)


if __name__ == '__main__':
    unittest.main()
