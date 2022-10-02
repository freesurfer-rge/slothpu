import bitarray
from bitarray.util import ba2int

from slothpu import RegisterFile


def test_smoke():
    target = RegisterFile(4, 8)
    assert len(target) == 4
    assert target.n_bits == 8

    for i in range(4):
        value = ba2int(target[i])
        assert value == 2**i


def test_set_bitarray_smoke():
    target = RegisterFile(8, 8)

    # It's easier to type the string big-endian, but we
    # want things stored little endian
    nv = bitarray.bitarray("00000011"[::-1], endian="little")

    idx = 4
    assert ba2int(target[idx]) == 16
    target[idx] = nv
    assert ba2int(target[idx]) == 3


def test_set_bitarray_extension_required():
    target = RegisterFile(8, 8)

    # It's easier to type the string big-endian, but we
    # want things stored little endian
    nv = bitarray.bitarray("1011"[::-1], endian="little")

    idx = 4
    assert ba2int(target[idx]) == 16
    target[idx] = nv
    assert ba2int(target[idx]) == 11


def test_set_string_smoke():
    target = RegisterFile(8, 8)

    idx = 5
    assert ba2int(target[idx]) == 32
    target[idx] = "10000010"
    assert ba2int(target[idx]) == 130


def test_set_string_extension_required():
    target = RegisterFile(8, 8)

    idx = 5
    assert ba2int(target[idx]) == 32
    target[idx] = "1101"
    assert ba2int(target[idx]) == 13
