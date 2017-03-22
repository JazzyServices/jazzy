# coding: ascii ; Copyright: (c) Jazzy Services Limited 2017
'''
The base41 encoding scheme encodes pairs of bytes to three ASCII chars.
A single trailing byte is encoded to either a single ASCII char or to two
ASCII chars depending on its byte value.

The chars are all safe to use in filenames, pathnames, URIs, etc
This gives it an advantage over base64 which uses '/' as one of the letters
of its alphabet. In order to get round this limitation in base64, programmers
would have to remember to pass the correct `altchars` to b64encode and to
pass the same `altchars` to b64decode. This has led to many bugs in systems
that use slightly different base64 alphabets for different things.

Base41 solves this by using an alphabet that consists only of letters and
digits: 0123456789jklmnopABCDEFGHIJKLMNOPQRSTUVWX
Each byte of this alphabet obeys the rule: (byte % 48) == value
giving the choice of alphabet an internal logic rather than it just being a
substitution cipher.

Example Usage:
# encode a UUID to base41
>>> import uuid
>>> u=uuid.UUID('a98bd614-b023-45c2-99b1-057a3edeff92')
>>> b=b41encode(u.bytes)
>>> print(b.decode('ascii')) # for the benefit of python2/3 compatibility
IQILHPPQJGIjJpG8R0FG9OUV
>>> d=b41decode(b)
>>> uuid.UUID(bytes=d)
UUID('a98bd614-b023-45c2-99b1-057a3edeff92')

In the above example we encoded a UUID (usually represented using 36 chars)
to a string of 24 base41 chars. We could then use this string as a filename,
directory name or in a URI. If we would have used base64, the encoded string
would have been 'qYvWFLAjRcKZsQV6Pt7/kg==' which not only has annoying padding
chars, but contains an embedded slash.

Copyright: (c) Jazzy Services Limited 2017
License file: ./LICENSE
'''
#   _________
# _| helpers |________________________________________________________________

def out_tostring(src):
    return ''.join(chr(i) for i in src)

if bytes == str:
    out_tobytes = out_tostring
    def in_tobytes(src):
        return (ord(i) for i in src)
else:
    def out_tobytes(src):
        return bytes(src)
    def in_tobytes(src):
        return src

#   __________
# _| ENCODING |_______________________________________________________________

# The standard base41 alphabet
# These are BYTEs rather than CHARs.
# The bytearray() call is for the benefit of Python 2 to ensure that
# the alphabet is bytes.
ALFA = bytearray(b'0123456789jklmnopABCDEFGHIJKLMNOPQRSTUVWX')

# Convert a BYTE-PAIR to UINT16
# Python3 has from_bytes()
# Python2 does it "long hand"
# The encoding scheme always treats a BYTE-PAIR as a big-endian UINT16
if hasattr(int, 'from_bytes'):
    def pair_to_uint16(pair):
        'Convert a pair of bytes to UINT16.'
        return int.from_bytes(pair, 'big')
else:
    def pair_to_uint16(pair):
        'Convert a pair of bytes to UINT16.'
        return pair[0] << 8 | pair[1]

class B41Encoder(object):
    'Iterator to encode a byte source to the Base41 Alphabet.'
    def __init__(my, src):
        # Source iterator
        my.octets = iter(src)
        # "working storage" ;)
        my.pair = bytearray()
    def u16_iter(my):
        'MANY octet-pair => MANY UINT16'
        while True:
            # read two octets (may raise a StopIteration during either read)
            my.pair = bytearray()
            my.pair.append(next(my.octets))
            my.pair.append(next(my.octets))
            u16 = pair_to_uint16(my.pair)
            yield u16
    def __iter__(my):
        'MANY UINT16 => MANY B41-char'
        for u16 in my.u16_iter():
            # -- B41 TRIPLE --
            # low-order B41-Char
            himid,lo = divmod(u16, 41)
            yield ALFA[lo]
            # middle- and high-order B41-Chars
            hi,mid = divmod(himid, 41)
            yield ALFA[mid]
            yield ALFA[hi]
        # encode the trailing byte
        try:
            hi,lo = divmod(my.pair[0], 41)
            yield ALFA[lo]
            if hi > 0:
                yield ALFA[hi]
        except IndexError:
            pass

def b41encode(src):
    'Encode a byte source using base41 encoding.'
    return out_tobytes(byt for byt in B41Encoder(src))

def b41string(src):
    'Encode a byte source using base41 encoding.'
    return out_tostring(byt for byt in B41Encoder(src))

class B41U16Encoder(object):
    'Iterator to encode a source of UINT16s to the Base41 Alphabet.'
    def __init__(my, src):
        # Source iterator
        my.u16_iter = iter(src)
    def __iter__(my):
        'MANY UINT16 => MANY B41-char'
        for u16 in my.u16_iter:
            # -- B41 TRIPLE --
            # low-order B41-Char
            himid,lo = divmod(u16, 41)
            yield ALFA[lo]
            # middle- and high-order B41-Chars
            hi,mid = divmod(himid, 41)
            yield ALFA[mid]
            yield ALFA[hi]

#   __________
# _| DECODING |_______________________________________________________________

class UnderflowError(ArithmeticError):
    'Underflow error.'
    def __init__(self, *args):
        super(UnderflowError, self).__init__(*args)

def b41d_filter(src):
    'Yield only B41-BYTEs from a byte source.'
    for byte in src:
        if (32 < byte < 127) and ((byte % 48) < 41):
            yield byte % 48

def decode_triplet(triplet):
    'Decode a triplet of base41-encoded bytes.'
    u16 = triplet[0] + 41 * (triplet[1] + 41 * triplet[2])
    if u16 >= 65536:
        msg = 'decoding three bytes gave a value ({0}) greater than 65535'
        overflow = msg.format(u16)
        raise OverflowError(overflow)
    return u16

def decode_double(double):
    'Decode a pair of trailing bytes from base41.'
    u8 = double[0] + 41 * double[1]
    if u8 < 41:
        msg = 'decoding two bytes gave a value ({0}) less than 41'
        underflow = msg.format(u8)
        raise UnderflowError(underflow)
    if u8 >= 256:
        msg = 'decoding two bytes gave a value ({0}) greater than 255'
        overflow = msg.format(u8)
        raise OverflowError(overflow)
    return u8

def decode_single(single):
    'Decode a single trailing byte from base41.'
    u8 = single[0]
    assert u8 < 41, 'Overflow error: u8={}'.format(u8)
    return u8


class B41Decoder(object):
    'Iterator to decode a base41-encoded byte source.'
    def __init__(my, src):
        my.src = b41d_filter(src)
        my.acc = bytearray()
    def u16_iter(my):
        # MANY b41-triplet => MANY UINT16
        while True:
            my.acc = bytearray()
            my.acc.append(next(my.src))
            my.acc.append(next(my.src))
            my.acc.append(next(my.src))
            u16 = decode_triplet(my.acc)
            yield u16
    def __iter__(my):
        for u16 in my.u16_iter():
            yield u16 >> 8
            yield u16 & 0xff
        #
        if len(my.acc) == 2:
            yield decode_double(my.acc)
        elif len(my.acc) == 1:
            yield decode_single(my.acc)

def b41decode(src):
    'Decode a base41-encoded byte source.'
    dsrc = in_tobytes(src)
    return out_tobytes(byt for byt in B41Decoder(dsrc))


class B41U16Decoder(object):
    'Iterator to decode a base41-encoded byte source to UINT16s.'
    def __init__(my, src):
        my.src = b41d_filter(src)
    def __iter__(my):
        # MANY b41-triplet => MANY UINT16
        acc = bytearray()
        while True:
            acc.append(next(my.src))
            acc.append(next(my.src))
            acc.append(next(my.src))
            u16 = decode_triplet(acc)
            acc = bytearray()
            yield u16
        # Trailing bytes not allowed
        assert len(acc) == 0, 'Trailing bytes while decoding to UINT16'

