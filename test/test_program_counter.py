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


def test_execute_branch():
    bp = BackPlane(8)
    target = ProgramCounter(bp)

    target.increment()
    target.increment()
    assert bitarray.util.ba2int(target.pc) == 4
    loc = 10
    bp.A_bus.value = bitarray.util.int2ba(loc, length=bp.n_bits, endian="little")
    target.execute("BRANCH")
    assert bitarray.util.ba2int(target.pc) == loc


def test_execute_branch_if_zero():
    bp = BackPlane(8)
    target = ProgramCounter(bp)

    target.increment()
    target.increment()
    assert bitarray.util.ba2int(target.pc) == 4
    loc = 130
    bp.A_bus.value = bitarray.util.int2ba(loc, length=bp.n_bits, endian="little")

    # Set up B_bus to be non-zero
    bp.B_bus.value = bitarray.util.int2ba(2, length=bp.n_bits, endian="little")
    target.execute("BRANCH_IF_ZERO")
    assert bitarray.util.ba2int(target.pc) == 6  # We will have incremented instead

    # Now have B_bus be zero
    bp.B_bus.value = bitarray.util.zeros(8, endian="little")
    target.execute("BRANCH_IF_ZERO")
    assert bitarray.util.ba2int(target.pc) == loc


def test_execute_branch_if_zero():
    bp = BackPlane(8)
    target = ProgramCounter(bp)

    target.increment()
    target.increment()
    assert bitarray.util.ba2int(target.pc) == 4
    loc = 130
    bp.A_bus.value = bitarray.util.int2ba(loc, length=bp.n_bits, endian="little")

    # Set up B_bus to be non-zero
    bp.B_bus.value = bitarray.util.int2ba(2, length=bp.n_bits, endian="little")
    target.execute("BRANCH_IF_NONZERO")
    assert bitarray.util.ba2int(target.pc) == loc

    # Now have B_bus be zero
    bp.B_bus.value = bitarray.util.zeros(8, endian="little")
    target.execute("BRANCH_IF_NONZERO")
    assert bitarray.util.ba2int(target.pc) == loc + 2  # Increment instead
