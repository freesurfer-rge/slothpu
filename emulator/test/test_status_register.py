import bitarray.util

from slothpu import BackPlane, StatusRegister


def test_smoke():
    bp = BackPlane(8)
    target = StatusRegister(bp)

    assert bitarray.util.ba2int(target.value) == 0


def test_set_flags():
    bp = BackPlane(8)
    target = StatusRegister(bp)

    assert bitarray.util.ba2int(target.value) == 0
    bp.SALU_flag = 1
    target.update()
    assert bitarray.util.ba2int(target.value) == 1
    bp.SALU_flag = 0
    bp.DALU_flag = 1
    target.update()
    assert bitarray.util.ba2int(target.value) == 2
    bp.SALU_flag = 1
    target.update()
    assert bitarray.util.ba2int(target.value) == 3


def test_execute_loadstatus():
    bp = BackPlane(8)
    target = StatusRegister(bp)

    assert bitarray.util.ba2int(bp.C_bus.value) == 0
    bp.SALU_flag = 1
    bp.DALU_flag = 1
    target.update()
    target.execute("LOADSTATUS")
    assert bitarray.util.ba2int(bp.C_bus.value) == 3
