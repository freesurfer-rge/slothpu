import bitarray.util

import pytest

from slothpu import DALU, BackPlane


a_b_pairs = [
    (0, 0),
    (1, 0),
    (0, 1),
    (128, 128),
    (255, 1),
    (1, 255),
    (137, 2),
    (101, 13),
    (7, 240),
    (8, 240),
    (240, 8),
    (255, 255),
]


@pytest.mark.parametrize(
    ["a", "b"],
    a_b_pairs,
)
def test_add(a, b):
    bp = BackPlane(8)
    target = DALU(bp)

    bp.A_bus.value = bitarray.util.int2ba(a, 8, endian="little")
    bp.B_bus.value = bitarray.util.int2ba(b, 8, endian="little")
    assert bitarray.util.ba2int(bp.C_bus.value) == 0
    assert bp.DALU_flag == 0

    target.execute("ADD")

    c = a + b
    assert c < 512, "Check inputs!"
    expected_carry, expected_c = divmod(c, 256)

    assert bitarray.util.ba2int(bp.C_bus.value) == expected_c
    assert bp.DALU_flag == expected_carry


@pytest.mark.parametrize(
    ["a", "b"],
    a_b_pairs,
)
def test_sub(a, b):
    bp = BackPlane(8)
    target = DALU(bp)

    bp.A_bus.value = bitarray.util.int2ba(a, 8, endian="little")
    bp.B_bus.value = bitarray.util.int2ba(b, 8, endian="little")
    assert bitarray.util.ba2int(bp.C_bus.value) == 0
    assert bp.DALU_flag == 0

    target.execute("SUB")

    c = a - b
    if c >= 0:
        assert bitarray.util.ba2int(bp.C_bus.value) == c
        assert bp.DALU_flag == 0
    else:
        assert bitarray.util.ba2int(bp.C_bus.value) == c + 256
        assert bp.DALU_flag == 1


@pytest.mark.parametrize(
    ["a", "b"],
    a_b_pairs,
)
def test_or(a, b):
    bp = BackPlane(8)
    target = DALU(bp)

    bp.A_bus.value = bitarray.util.int2ba(a, 8, endian="little")
    bp.B_bus.value = bitarray.util.int2ba(b, 8, endian="little")
    assert bitarray.util.ba2int(bp.C_bus.value) == 0
    assert bp.DALU_flag == 0

    target.execute("OR")

    c = a | b
    assert bitarray.util.ba2int(bp.C_bus.value) == c
    assert bp.DALU_flag == 0


@pytest.mark.parametrize(["a", "b"], a_b_pairs)
def test_and(a, b):
    bp = BackPlane(8)
    target = DALU(bp)

    bp.A_bus.value = bitarray.util.int2ba(a, 8, endian="little")
    bp.B_bus.value = bitarray.util.int2ba(b, 8, endian="little")
    assert bitarray.util.ba2int(bp.C_bus.value) == 0
    assert bp.DALU_flag == 0

    target.execute("AND")

    c = a & b
    assert bitarray.util.ba2int(bp.C_bus.value) == c
    assert bp.DALU_flag == 0


@pytest.mark.parametrize(["a", "b"], a_b_pairs)
def test_xor(a, b):
    bp = BackPlane(8)
    target = DALU(bp)

    bp.A_bus.value = bitarray.util.int2ba(a, 8, endian="little")
    bp.B_bus.value = bitarray.util.int2ba(b, 8, endian="little")
    assert bitarray.util.ba2int(bp.C_bus.value) == 0
    assert bp.DALU_flag == 0

    target.execute("XOR")

    c = a ^ b
    assert bitarray.util.ba2int(bp.C_bus.value) == c
    assert bp.DALU_flag == 0


@pytest.mark.parametrize(["a", "b"], a_b_pairs)
def test_nand(a, b):
    bp = BackPlane(8)
    target = DALU(bp)

    bp.A_bus.value = bitarray.util.int2ba(a, 8, endian="little")
    bp.B_bus.value = bitarray.util.int2ba(b, 8, endian="little")
    assert bitarray.util.ba2int(bp.C_bus.value) == 0
    assert bp.DALU_flag == 0

    target.execute("NAND")

    c = ~(a & b)
    if c < 0:
        c = c + 256
    assert bitarray.util.ba2int(bp.C_bus.value) == c
    assert bp.DALU_flag == 0
