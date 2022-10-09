import bitarray.util

from slothpu import BackPlane, StatusRegister


def test_smoke():
    bp = BackPlane(8)
    target = StatusRegister(bp)

    assert bitarray.util.ba2int(target.value) == 0