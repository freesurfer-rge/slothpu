import bitarray

def to_01_bigendian(ba: bitarray.bitarray):
    assert ba.endian() == 'little'
    return ba.to01()[::-1]