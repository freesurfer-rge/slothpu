import bitarray.util

import pytest

from slothpu import SALU, BackPlane

a_vals = [0,1,2,4,7,15,87,126,127,128,129, 253, 254, 255]

@pytest.mark.parametrize('a', a_vals)
def test_inc(a: int):
    bp = BackPlane(8)
    target = SALU(bp)
    assert a < 256

    bp.A_bus.value = bitarray.util.int2ba(a, 8, endian="little")
    assert bitarray.util.ba2int(bp.C_bus.value) == 0
    assert bp.SALU_flag == 0

    c = a + 1
    carry=0
    if c == 256:
        c = 0
        carry=1

    target.execute("INC")
    assert bitarray.util.ba2int(bp.C_bus.value) == c
    assert bp.SALU_flag == carry


@pytest.mark.parametrize('a', a_vals)
def test_dec(a: int):
    bp = BackPlane(8)
    target = SALU(bp)
    assert a < 256

    bp.A_bus.value = bitarray.util.int2ba(a, 8, endian="little")
    assert bitarray.util.ba2int(bp.C_bus.value) == 0
    assert bp.SALU_flag == 0

    c = a - 1
    borrow=0
    if c < 0:
        c = 255
        borrow=1

    target.execute("DEC")
    assert bitarray.util.ba2int(bp.C_bus.value) == c
    assert bp.SALU_flag == borrow

@pytest.mark.parametrize('a', a_vals)
def test_not(a: int):
    bp = BackPlane(8)
    target = SALU(bp)
    assert a < 256

    bp.A_bus.value = bitarray.util.int2ba(a, 8, endian="little")
    assert bitarray.util.ba2int(bp.C_bus.value) == 0
    assert bp.SALU_flag == 0

    c = 255 - a

    target.execute("NOT")
    assert bitarray.util.ba2int(bp.C_bus.value) == c
    assert bp.SALU_flag == 0

@pytest.mark.parametrize('a', a_vals)
def test_copy(a: int):
    bp = BackPlane(8)
    target = SALU(bp)
    assert a < 256

    bp.A_bus.value = bitarray.util.int2ba(a, 8, endian="little")
    assert bitarray.util.ba2int(bp.C_bus.value) == 0
    assert bp.SALU_flag == 0

    c = a

    target.execute("COPY")
    assert bitarray.util.ba2int(bp.C_bus.value) == c
    assert bp.SALU_flag == 0

@pytest.mark.parametrize('a', a_vals)
def test_lbarrel(a: int):
    bp = BackPlane(8)
    target = SALU(bp)
    assert a < 256

    bp.A_bus.value = bitarray.util.int2ba(a, 8, endian="little")
    assert bitarray.util.ba2int(bp.C_bus.value) == 0
    assert bp.SALU_flag == 0

    c = a << 1
    top_bit, c = divmod(c, 256)
    assert top_bit == 0 or top_bit == 1
    c = c + top_bit

    target.execute("LBARREL")
    assert bitarray.util.ba2int(bp.C_bus.value) == c
    assert bp.SALU_flag == 0

@pytest.mark.parametrize('a', a_vals)
def test_lshift0(a: int):
    bp = BackPlane(8)
    target = SALU(bp)
    assert a < 256

    bp.A_bus.value = bitarray.util.int2ba(a, 8, endian="little")
    assert bitarray.util.ba2int(bp.C_bus.value) == 0
    assert bp.SALU_flag == 0

    c = a << 1
    dropped_bit, c = divmod(c, 256)

    target.execute("LSHIFT0")
    assert bitarray.util.ba2int(bp.C_bus.value) == c
    assert bp.SALU_flag == dropped_bit

@pytest.mark.parametrize('a', a_vals)
def test_lshift1(a: int):
    bp = BackPlane(8)
    target = SALU(bp)
    assert a < 256

    bp.A_bus.value = bitarray.util.int2ba(a, 8, endian="little")
    assert bitarray.util.ba2int(bp.C_bus.value) == 0
    assert bp.SALU_flag == 0

    c = a << 1
    dropped_bit, c = divmod(c, 256)
    c = c+1 # Inject the 1

    target.execute("LSHIFT1")
    assert bitarray.util.ba2int(bp.C_bus.value) == c
    assert bp.SALU_flag == dropped_bit