import bitarray.util

import pytest

from slothpu import DALU, BackPlane


@pytest.mark.parametrize(
    ["a", "b"],
    [
        (0, 0),
        (1, 0),
        (0, 1),
        (128, 128),
        (255, 1),
        (1, 255),
        (137, 2),
        (7, 240),
        (255, 255),
    ],
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
