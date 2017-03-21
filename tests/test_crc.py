"""Unit tests for crc16_8005.

Copyright (c) Jazzy Services Limited 2017
License: ../LICENSE

"""
import unittest

import context
import crc16_8005


class Test_CRC(unittest.TestCase):

    def test_check(I):
        'Test that the CRC check value is correct.'
        message = bytearray(b'123456789')
        sut = crc16_8005.crc16_8005(message)
        I.assertEqual(sut, 0xbb3d)


if __name__ == '__main__':
    unittest.main()
