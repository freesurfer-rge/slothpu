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
    target.execute("FETCH0")
    assert bitarray.util.ba2int(target.ir) == value

def test_fetch1():
    bp = BackPlane(8)
    target = InstructionRegister(bp)

    assert bitarray.util.ba2int(target.ir) == 0

    value = 119
    bp.C_bus.value = bitarray.util.int2ba(value, bp.n_bits, endian="little")
    target.execute("FETCH1")
    assert bitarray.util.ba2int(target.ir) == value * 2**bp.n_bits