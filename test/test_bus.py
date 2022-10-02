import bitarray
import bitarray.util

from slothpu import Bus


def test_smoke():
    num_bits = 8
    target = Bus(num_bits)

    target.value = bitarray.util.int2ba(10, length=num_bits, endian="little")
    assert target.value == bitarray.bitarray("00001010"[::-1], endian="little")

def test_to01():
    num_bits = 4

    target = Bus(num_bits)
    target.value = bitarray.util.int2ba(10, length=num_bits, endian="little")
    assert target.to01() == "1010"
