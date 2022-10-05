import bitarray.util

from slothpu import BackPlane, ProgramCounter


def test_smoke():
    bp = BackPlane(8)
    target = ProgramCounter(bp)

    assert bitarray.util.ba2int(target.pc) == 0


def test_increment():
    bp = BackPlane(8)
    target = ProgramCounter(bp)

    assert bitarray.util.ba2int(target.pc) == 0
    target.increment()
    assert bitarray.util.ba2int(target.pc) == 2


def test_execute_increment():
    bp = BackPlane(8)
    target = ProgramCounter(bp)

    assert bitarray.util.ba2int(target.pc) == 0
    target.execute("INC")
    target.execute("INC")
    assert bitarray.util.ba2int(target.pc) == 4


def test_execute_fetch0():
    bp = BackPlane(8)
    target = ProgramCounter(bp)

    target.increment()
    target.increment()
    assert bitarray.util.ba2int(target.pc) == 4
    assert bitarray.util.ba2int(bp.A_bus.value) == 0
    target.execute("FETCH0")
    assert bitarray.util.ba2int(bp.A_bus.value) == 4


def test_execute_fetch1():
    bp = BackPlane(8)
    target = ProgramCounter(bp)

    target.increment()
    target.increment()
    assert bitarray.util.ba2int(target.pc) == 4
    assert bitarray.util.ba2int(bp.A_bus.value) == 0
    target.execute("FETCH1")
    assert bitarray.util.ba2int(bp.A_bus.value) == 5
