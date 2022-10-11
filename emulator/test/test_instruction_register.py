import bitarray.util

from slothpu import BackPlane, InstructionRegister


def test_smoke():
    bp = BackPlane(8)
    target = InstructionRegister(bp)

    assert target.n_bits == 16
    assert len(target.ir) == 16


def test_fetch0():
    bp = BackPlane(8)
    target = InstructionRegister(bp)

    assert bitarray.util.ba2int(target.ir) == 0

    value = 127
    bp.C_bus.value = bitarray.util.int2ba(value, bp.n_bits, endian="little")
    target.fetch0()
    assert bitarray.util.ba2int(target.ir) == value


def test_fetch1():
    bp = BackPlane(8)
    target = InstructionRegister(bp)

    assert bitarray.util.ba2int(target.ir) == 0

    value = 119
    bp.C_bus.value = bitarray.util.int2ba(value, bp.n_bits, endian="little")
    target.fetch1()
    assert bitarray.util.ba2int(target.ir) == value * 2**bp.n_bits


def test_decode():
    bp = BackPlane(8)
    target = InstructionRegister(bp)

    target._ir = bitarray.bitarray("0100000101110001", endian="little")
    assert (
        bitarray.util.ba2int(target.ir) == 36482
    )  # Mainly checks that the length is right

    assert target.unit == 0
    assert target.R_A == 0
    assert target.R_B == 0
    assert target.R_C == 0
    target.decode()
    assert target.unit == 2
    assert target.R_A == 5
    assert target.R_B == 3
    assert target.R_C == 4
