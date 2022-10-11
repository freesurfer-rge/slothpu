import bitarray.util

import pytest

from slothpu import BackPlane, RegisterUnit


def test_smoke():
    bp = BackPlane(8)
    target = RegisterUnit(bp)

    assert target.n_bits == bp.n_bits


@pytest.mark.parametrize("value", [0, 1, 8, 16, 127, 128, 254, 255])
def test_setnnn(value):
    command = f"SET{value:03}"
    print(command)

    bp = BackPlane(8)
    target = RegisterUnit(bp)

    assert bitarray.util.ba2int(bp.C_bus.value) == 0
    target.execute(command)
    assert bitarray.util.ba2int(bp.C_bus.value) == value
