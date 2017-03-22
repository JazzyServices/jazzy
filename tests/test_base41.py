"""Unit tests for base41.

Copyright: (c) Jazzy Services Limited 2017
License file: ../LICENSE

"""
import sys
import unittest

import context
import base41


class Test_B41Encoder(unittest.TestCase):

    def test_sanity(I):
        'Test the encoder with a standard byte string.'
        datum = b'John'
        sut = [byt for byt in base41.B41Encoder(datum)]
        expected = [0x4f, 0x6d, 0x6b, 0x32, 0x55, 0x6f]
        I.assertEqual(sut, expected)

    def test_sanity_lo_trailing(I):
        'Test the encoder with a low trailing byte.'
        datum = b'John!'
        sut = [byt for byt in base41.B41Encoder(datum)]
        expected = [0x4f, 0x6d, 0x6b, 0x32, 0x55, 0x6f, 0x51]
        I.assertEqual(sut, expected)

    def test_sanity_hi_trailing(I):
        'Test the encoder with a high trailing byte.'
        datum = b'John)'
        sut = [byt for byt in base41.B41Encoder(datum)]
        expected = [0x4f, 0x6d, 0x6b, 0x32, 0x55, 0x6f, 0x30, 0x31]
        I.assertEqual(sut, expected)

    def test_minimum(I):
        'Test the encoder with nulls.'
        N = 100
        datum = N * [0, 0]
        sut = [byt for byt in base41.B41Encoder(datum)]
        expected = N * [0x30, 0x30, 0x30]
        I.assertEqual(sut, expected)

    def test_minimum_trailing(I):
        'Test the encoder with an odd number of nulls.'
        datum = [0,0,0]
        sut = [byt for byt in base41.B41Encoder(datum)]
        expected = [0x30, 0x30, 0x30, 0x30]
        I.assertEqual(sut, expected)

    def test_maximum(I):
        'Test the encoder with 0xff.'
        N = 100
        datum = N * [0xff,0xff]
        sut = [byt for byt in base41.B41Encoder(datum)]
        expected = N * [0x41, 0x58, 0x56]   # AXV
        I.assertEqual(sut, expected)

    def test_maximum_trailing(I):
        'Test the encoder with an odd number of 0xff.'
        datum = [0xff,0xff,0xff]
        sut = [byt for byt in base41.B41Encoder(datum)]
        expected = [0x41, 0x58, 0x56, 0x39, 0x36]   # AXV-96
        I.assertEqual(sut, expected)

    def test_pair_boundaries(I):
        'Test the encoder on base41 boundaries.'
        data = [
            ([  0,   0], [0x30, 0x30, 0x30]), # 000
            ([  0,  40], [0x58, 0x30, 0x30]), # X00
            ([  0,  41], [0x30, 0x31, 0x30]), # 010
            ([  6, 104], [0x30, 0x58, 0x30]), # 0X0
            ([  6, 144], [0x58, 0x58, 0x30]), # XX0
            ([  6, 145], [0x30, 0x30, 0x31]), # 001
            ([249, 134], [0x30, 0x30, 0x56]), # 00V
            ([255, 238], [0x30, 0x58, 0x56]), # 0XV
            ([255, 255], [0x41, 0x58, 0x56]), # AXV
        ]
        for datum, expected in data:
            sut = [byt for byt in base41.B41Encoder(datum)]
            I.assertEqual(sut, expected)

    def test_singles(I):
        'Test the encoder using single bytes.'
        for datum, expected in zip(range(41), base41.ALFA):
            sut = [byt for byt in base41.B41Encoder([datum])]
            I.assertEqual(sut, [expected])


class Test_b41encode(unittest.TestCase):

    def test_sanity(I):
        'Test the encoder with a standard byte string.'
        datum = b'John'
        sut = base41.b41encode(datum)
        I.assertEqual(sut, b'Omk2Uo')

    def test_sanity_lo_trailing(I):
        'Test the encoder with a low trailing byte.'
        datum = b'John!'
        sut = base41.b41encode(datum)
        I.assertEqual(sut, b'Omk2UoQ')

    def test_sanity_hi_trailing(I):
        'Test the encoder with a high trailing byte.'
        datum = b'John)'
        sut = base41.b41encode(datum)
        I.assertEqual(sut, b'Omk2Uo01')

    def test_minimum(I):
        'Test the encoder with nulls.'
        N = 100
        datum = N * [0, 0]
        sut = base41.b41encode(datum)
        expected = N * b'000'
        I.assertEqual(sut, expected)

    def test_minimum_trailing(I):
        'Test the encoder with an odd number of nulls.'
        datum = [0,0,0]
        sut = base41.b41encode(datum)
        I.assertEqual(sut, b'0000')

    def test_maximum(I):
        'Test the encoder with 0xff.'
        N = 100
        datum = N * [0xff,0xff]
        sut = base41.b41encode(datum)
        expected = N * b'AXV'
        I.assertEqual(sut, expected)

    def test_maximum_trailing(I):
        'Test the encoder with an odd number of 0xff.'
        datum = [0xff,0xff,0xff]
        sut = base41.b41encode(datum)
        expected = b'AXV96'
        I.assertEqual(sut, expected)

    def test_pair_boundaries(I):
        'Test the encoder on base41 boundaries.'
        data = [
            ([  0,   0], b'000'),
            ([  0,  40], b'X00'),
            ([  0,  41], b'010'),
            ([  6, 104], b'0X0'),
            ([  6, 144], b'XX0'),
            ([  6, 145], b'001'),
            ([249, 134], b'00V'),
            ([255, 238], b'0XV'),
            ([255, 255], b'AXV'),
        ]
        for datum, expected in data:
            sut = base41.b41encode(datum)
            I.assertEqual(sut, expected)


class Test_b41string(unittest.TestCase):

    def test_sanity(I):
        'Test the encoder with a standard byte string.'
        datum = b'John'
        sut = base41.b41string(datum)
        I.assertEqual(sut, 'Omk2Uo')

    def test_sanity_lo_trailing(I):
        'Test the encoder with a low trailing byte.'
        datum = b'John!'
        sut = base41.b41string(datum)
        I.assertEqual(sut, 'Omk2UoQ')

    def test_sanity_hi_trailing(I):
        'Test the encoder with a high trailing byte.'
        datum = b'John)'
        sut = base41.b41string(datum)
        I.assertEqual(sut, 'Omk2Uo01')

    def test_minimum(I):
        'Test the encoder with nulls.'
        N = 100
        datum = N * [0, 0]
        sut = base41.b41string(datum)
        expected = N * '000'
        I.assertEqual(sut, expected)

    def test_minimum_trailing(I):
        'Test the encoder with an odd number of nulls.'
        datum = [0,0,0]
        sut = base41.b41string(datum)
        I.assertEqual(sut, '0000')

    def test_maximum(I):
        'Test the encoder with 0xff.'
        N = 100
        datum = N * [0xff,0xff]
        sut = base41.b41string(datum)
        expected = N * 'AXV'
        I.assertEqual(sut, expected)

    def test_maximum_trailing(I):
        'Test the encoder with an odd number of 0xff.'
        datum = [0xff,0xff,0xff]
        sut = base41.b41string(datum)
        expected = 'AXV96'
        I.assertEqual(sut, expected)

    def test_pair_boundaries(I):
        'Test the encoder on base41 boundaries.'
        data = [
            ([  0,   0], '000'),
            ([  0,  40], 'X00'),
            ([  0,  41], '010'),
            ([  6, 104], '0X0'),
            ([  6, 144], 'XX0'),
            ([  6, 145], '001'),
            ([249, 134], '00V'),
            ([255, 238], '0XV'),
            ([255, 255], 'AXV'),
        ]
        for datum, expected in data:
            sut = base41.b41string(datum)
            I.assertEqual(sut, expected)


#   _
# _| |________________________________________________________________________

class Test_B41Decoder(unittest.TestCase):

    def test_sanity(I):
        'Test the decoder with a standard byte string.'
        datum = [0x4f, 0x6d, 0x6b, 0x32, 0x55, 0x6f]
        sut = [byt for byt in base41.B41Decoder(datum)]
        expected = [0x4a, 0x6f, 0x68, 0x6e]
        I.assertEqual(sut, expected)

    def test_sanity_lo_trailing(I):
        'Test the decoder with a low trailing byte.'
        datum = [0x4f, 0x6d, 0x6b, 0x32, 0x55, 0x6f, 0x51]
        sut = [byt for byt in base41.B41Decoder(datum)]
        expected = [0x4a, 0x6f, 0x68, 0x6e, 0x21]
        I.assertEqual(sut, expected)

    def test_sanity_hi_trailing(I):
        'Test the decoder with a high trailing byte.'
        datum = [0x4f, 0x6d, 0x6b, 0x32, 0x55, 0x6f, 0x30, 0x31]
        sut = [byt for byt in base41.B41Decoder(datum)]
        expected = [0x4a, 0x6f, 0x68, 0x6e, 0x29]
        I.assertEqual(sut, expected)

    def test_minimum(I):
        'Test the decoder with nulls.'
        N = 100
        datum = N * [0x30, 0x30, 0x30]
        sut = [byt for byt in base41.B41Decoder(datum)]
        expected = N * [0, 0]
        I.assertEqual(sut, expected)

    def test_minimum_trailing(I):
        'Test the decoder with an odd number of nulls.'
        datum = [0x30, 0x30, 0x30, 0x30]
        sut = [byt for byt in base41.B41Decoder(datum)]
        expected = [0,0,0]
        I.assertEqual(sut, expected)

    def test_maximum(I):
        'Test the decoder with 0xff.'
        N = 100
        datum = N * [0x41, 0x58, 0x56]   # AXV
        sut = [byt for byt in base41.B41Decoder(datum)]
        expected = N * [0xff,0xff]
        I.assertEqual(sut, expected)

    def test_maximum_trailing(I):
        'Test the decoder with an odd number of 0xff.'
        datum = [0x41, 0x58, 0x56, 0x39, 0x36]   # AXV-96
        sut = [byt for byt in base41.B41Decoder(datum)]
        expected = [0xff,0xff,0xff]
        I.assertEqual(sut, expected)

    def test_pair_boundaries(I):
        'Test the decoder on base41 boundaries.'
        data = [
            ([  0,   0], [0x30, 0x30, 0x30]), # 000
            ([  0,  40], [0x58, 0x30, 0x30]), # X00
            ([  0,  41], [0x30, 0x31, 0x30]), # 010
            ([  6, 104], [0x30, 0x58, 0x30]), # 0X0
            ([  6, 144], [0x58, 0x58, 0x30]), # XX0
            ([  6, 145], [0x30, 0x30, 0x31]), # 001
            ([249, 134], [0x30, 0x30, 0x56]), # 00V
            ([255, 238], [0x30, 0x58, 0x56]), # 0XV
            ([255, 255], [0x41, 0x58, 0x56]), # AXV
        ]
        for expected, datum in data:
            sut = [byt for byt in base41.B41Decoder(datum)]
            I.assertEqual(sut, expected)

    def test_singles(I):
        'Test the decoder using single bytes.'
        for datum, expected in zip(base41.ALFA, range(41)):
            sut = [byt for byt in base41.B41Decoder([datum])]
            I.assertEqual(sut, [expected])

    def test_triplet_overflow(I):
        'Test the decoder detects overflow > 65536.'
        datum = [0x42, 0x58, 0x56]   # BXV
        with I.assertRaises(OverflowError) as cm:
            sut = [byt for byt in base41.B41Decoder(datum)]
        I.assertEqual(cm.exception.args[0],
            'decoding three bytes gave a value (65536) greater than 65535' )

    def test_triplet_overflow_alt(I):
        'Test the decoder detects overflow > 65536 (alternative chars).'
        datum = [0x72, 0x28, 0x26]   # r(&
        with I.assertRaises(OverflowError) as cm:
            sut = [byt for byt in base41.B41Decoder(datum)]
        I.assertEqual(cm.exception.args[0],
            'decoding three bytes gave a value (65536) greater than 65535' )

    def test_triplet_overflow_max(I):
        'Test the decoder detects overflow > 65536.'
        datum = [0x58, 0x58, 0x58]   # X,X,X
        with I.assertRaises(OverflowError) as cm:
            sut = [byt for byt in base41.B41Decoder(datum)]
        I.assertEqual(cm.exception.args[0],
            'decoding three bytes gave a value (68920) greater than 65535' )

    def test_double_overflow(I):
        'Test the decoder detects double byte overflow > 255.'
        datum = [0x6a, 0x36]   # j6
        with I.assertRaises(OverflowError) as cm:
            sut = [byt for byt in base41.B41Decoder(datum)]
        I.assertEqual(cm.exception.args[0],
            'decoding two bytes gave a value (256) greater than 255' )

    def test_double_overflow_alt(I):
        'Test the decoder detects double byte overflow > 255 (alt chars).'
        datum = [0x3a, 0x66]   # :f
        with I.assertRaises(OverflowError) as cm:
            sut = [byt for byt in base41.B41Decoder(datum)]
        I.assertEqual(cm.exception.args[0],
            'decoding two bytes gave a value (256) greater than 255' )

    def test_double_overflow_max(I):
        'Test the decoder detects double byte overflow > 255 (max).'
        datum = [0x28, 0x56]   # (X
        with I.assertRaises(OverflowError) as cm:
            sut = [byt for byt in base41.B41Decoder(datum)]
        I.assertEqual(cm.exception.args[0],
            'decoding two bytes gave a value (1598) greater than 255' )

    def test_double_underflow(I):
        'Test the decoder detects double byte underflow < 41.'
        datum = [0x58, 0x30]   # X0
        with I.assertRaises(base41.UnderflowError) as cm:
            sut = [byt for byt in base41.B41Decoder(datum)]
        I.assertEqual(cm.exception.args[0],
            'decoding two bytes gave a value (40) less than 41' )


class Test_b41decode(unittest.TestCase):

    def test_sanity(I):
        'Test the decoder with a standard byte string.'
        datum = b'Omk2Uo'
        sut = base41.b41decode(datum)
        I.assertEqual(sut, b'John')

    def test_sanity_lo_trailing(I):
        'Test the decoder with a low trailing byte.'
        datum = b'Omk2UoQ'
        sut = base41.b41decode(datum)
        I.assertEqual(sut, b'John!')

    def test_sanity_hi_trailing(I):
        'Test the decoder with a high trailing byte.'
        datum = b'Omk2Uo01'
        sut = base41.b41decode(datum)
        I.assertEqual(sut, b'John)')

    def test_minimum(I):
        'Test the decoder with nulls.'
        N = 100
        datum = N * b'000'
        sut = base41.b41decode(datum)
        expected = N * b'\x00\x00'
        I.assertEqual(sut, expected)

    def test_minimum_trailing(I):
        'Test the decoder with an odd number of nulls.'
        datum = b'0000'
        sut = base41.b41decode(datum)
        I.assertEqual(sut, b'\x00\x00\x00')

    def test_maximum(I):
        'Test the decoder with 0xff.'
        N = 100
        datum = N * b'AXV'
        sut = base41.b41decode(datum)
        expected = N * b'\xff\xff'
        I.assertEqual(sut, expected)

    def test_maximum_trailing(I):
        'Test the decoder with an odd number of 0xff.'
        datum = b'AXV96'
        sut = base41.b41decode(datum)
        expected = b'\xff\xff\xff'
        I.assertEqual(sut, expected)

    def test_pair_boundaries(I):
        'Test the decoder on base41 boundaries.'
        data = [
            (b'\x00\x00', b'000'),
            (b'\x00(', b'X00'),
            (b'\x00)', b'010'),
            (b'\x06h', b'0X0'),
            (b'\x06\x90', b'XX0'),
            (b'\x06\x91', b'001'),
            (b'\xf9\x86', b'00V'),
            (b'\xff\xee', b'0XV'),
            (b'\xff\xff', b'AXV'),
        ]
        for expected, datum in data:
            sut = base41.b41decode(datum)
            I.assertEqual(sut, expected)


class Test_b41decode_punct(unittest.TestCase):

    def test_sanity(I):
        'Test the decoder with a standard byte string and punctuation.'
        datum = b'[O**m_k+,-./2U^^^^o]'
        sut = base41.b41decode(datum)
        I.assertEqual(sut, b'John')

    def test_just_punct(I):
        'Test the decoder with only punctuation.'
        datum = b'[-+/*___*/]'
        sut = base41.b41decode(datum)
        I.assertEqual(sut, b'')

    def test_sanity_lo_trailing(I):
        'Test the decoder with a low trailing byte and punctuation.'
        datum = b'Omk2Uo-Q/'
        sut = base41.b41decode(datum)
        I.assertEqual(sut, b'John!')

    def test_sanity_hi_trailing(I):
        'Test the decoder with a high trailing byte and punctuation.'
        datum = b'Omk2Uo,0-.-1,'
        sut = base41.b41decode(datum)
        I.assertEqual(sut, b'John)')

    def test_pair_boundaries(I):
        'Test the decoder on base41 boundaries with punctuation.'
        data = [
            (b'\x00\x00', b'0-00'),
            (b'\x00(',    b'X*00'),
            (b'\x00)',    b'01+0'),
            (b'\x06h',    b'0//X0'),
            (b'\x06\x90', b'XX0__'),
            (b'\x06\x91', b'0^0^1'),
            (b'\xf9\x86', b'0-0-V'),
            (b'\xff\xee', b'0[XV]'),
            (b'\xff\xff', b'[AX[[[V'),
        ]
        for expected, datum in data:
            sut = base41.b41decode(datum)
            I.assertEqual(sut, expected)

    def test_singles(I):
        'Test the decoder using single byte and punctuation.'
        datum = b'_-+#+-_'
        sut = base41.b41decode(datum)
        I.assertEqual(sut, b'#')


class Test_b41_encode_decode(unittest.TestCase):

    def test_sanity(I):
        'Test round-trip encode/decode.'
        datum = b'John'
        enc = base41.b41encode(datum)
        sut = base41.b41decode(enc)
        I.assertEqual(sut, datum)

    def test_longer(I):
        'Test round-trip encode/decode.'
        datum = b'Now is the winter of our discontent'
        enc = base41.b41encode(datum)
        sut = base41.b41decode(enc)
        I.assertEqual(sut, datum)

    def test_binary(I):
        'Test round-trip encode/decode with binary data.'
        from base64 import b64decode
        b64 = b'R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs='
        datum = b64decode(b64)
        enc = base41.b41encode(datum)
        sut = base41.b41decode(enc)
        I.assertEqual(sut, datum)
        from base64 import b64encode
        recon = b64encode(sut)
        I.assertEqual(recon, b64)

    def test_binary_reverse(I):
        'Test round-trip decode/encode with binary data.'
        datum = b'4SjBLjkN8j60j609DC5003I0000310000000j60j602006n0j60B1'
        dec = base41.b41decode(datum)
        sut = base41.b41encode(dec)
        I.assertEqual(sut, datum)

    def test_sha1(I):
        'Test round-trip encode/decode with SHA1 data.'
        from hashlib import sha1
        datum = sha1(b'Now is the winter of our discontent').digest()
        enc = base41.b41encode(datum)
        sut = base41.b41decode(enc)
        I.assertEqual(sut, datum)

    def test_uuid(I):
        'Test round-trip encode/decode with a UUID.'
        from uuid import uuid4
        datum = uuid4().bytes
        enc = base41.b41encode(datum)
        sut = base41.b41decode(enc)
        I.assertEqual(sut, datum)


class Test_B41U16Encoder(unittest.TestCase):

    def test_sanity(I):
        'Test encoding of unsigned shorts.'
        datum = [0x4a6f, 0x686e]
        sut = [byt for byt in base41.B41U16Encoder(datum)]
        expected = [0x4f, 0x6d, 0x6b, 0x32, 0x55, 0x6f]
        I.assertEqual(sut, expected)

    def test_utf16(I):
        'Test encoding of UTF-16.'
        china = u'\u4e2d\u534e\u4eba\u6c11\u5171\u548c\u56fd'
        datum = map(ord, china)
        sut = [byt for byt in base41.B41U16Encoder(datum)]
        expected = [
            0x35, 0x55, 0x6b,   # 5Uk
            0x36, 0x4c, 0x6c,   # 6Ll
            0x47, 0x58, 0x6b,   # GXk
            0x4f, 0x42, 0x70,   # OBp
            0x45, 0x70, 0x6c,   # Epl
            0x55, 0x53, 0x6c,   # USl
            0x36, 0x6a, 0x6d    # 6jm
        ]
        I.assertEqual(sut, expected)


class Test_B41U16Decoder(unittest.TestCase):

    def test_sanity(I):
        'Test decoding of unsigned shorts.'
        datum =[0x4f, 0x6d, 0x6b, 0x32, 0x55, 0x6f]
        sut = [byt for byt in base41.B41U16Decoder(datum)]
        expected = [0x4a6f, 0x686e]
        I.assertEqual(sut, expected)

    def test_utf16(I):
        'Test decoding of UTF-16.'
        datum = [
            0x35, 0x55, 0x6b,   # 5Uk
            0x36, 0x4c, 0x6c,   # 6Ll
            0x47, 0x58, 0x6b,   # GXk
            0x4f, 0x42, 0x70,   # OBp
            0x45, 0x70, 0x6c,   # Epl
            0x55, 0x53, 0x6c,   # USl
            0x36, 0x6a, 0x6d    # 6jm
        ]
        sut = [byt for byt in base41.B41U16Decoder(datum)]
        china = u'\u4e2d\u534e\u4eba\u6c11\u5171\u548c\u56fd'
        expected = list(map(ord, china))
        I.assertEqual(sut, expected)


if __name__ == '__main__':
    print('\n+ Running Tests for Python{0.major}.{0.minor}'.format(sys.version_info))
    unittest.main()
