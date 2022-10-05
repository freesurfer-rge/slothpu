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

    # Want to poke a value which will affect the upper and lower byte
    start_loc = 8200
    loc_ba = bitarray.util.int2ba(start_loc, target.n_bits, endian="little")
    bp.A_bus.value = loc_ba[0:8]
    bp.B_bus.value = loc_ba[8:16]
    target.execute("BRANCH")

    assert bitarray.util.ba2int(target.pc) == start_loc

    # Clear the buses
    bp.A_bus.value = bitarray.util.zeros(8, endian="little")
    bp.B_bus.value = bitarray.util.zeros(8, endian="little")
    target.execute("FETCH0")
    expect_b, expect_a = divmod(start_loc, 2**bp.n_bits)
    assert bitarray.util.ba2int(bp.A_bus.value) == expect_a
    assert bitarray.util.ba2int(bp.B_bus.value) == expect_b


def test_execute_fetch1():
    bp = BackPlane(8)
    target = ProgramCounter(bp)

    # Want to poke a value which will affect the upper and lower byte
    start_loc = 9200
    loc_ba = bitarray.util.int2ba(start_loc, target.n_bits, endian="little")
    bp.A_bus.value = loc_ba[0:8]
    bp.B_bus.value = loc_ba[8:16]
    target.execute("BRANCH")

    assert bitarray.util.ba2int(target.pc) == start_loc

    bp.A_bus.value = bitarray.util.zeros(8, endian="little")
    bp.B_bus.value = bitarray.util.zeros(8, endian="little")
    target.execute("FETCH1")
    expect_b, expect_a = divmod(start_loc + 1, 2**bp.n_bits)
    assert bitarray.util.ba2int(bp.A_bus.value) == expect_a
    assert bitarray.util.ba2int(bp.B_bus.value) == expect_b


def test_execute_branch():
    bp = BackPlane(8)
    target = ProgramCounter(bp)

    target.increment()
    target.increment()
    assert bitarray.util.ba2int(target.pc) == 4
    loc = 4000
    loc_ba = bitarray.util.int2ba(loc, target.n_bits, endian="little")
    bp.A_bus.value = loc_ba[0:8]
    bp.B_bus.value = loc_ba[8:16]
    target.execute("BRANCH")
    assert bitarray.util.ba2int(target.pc) == loc


def test_execute_branch_if_zero():
    bp = BackPlane(8)
    target = ProgramCounter(bp)

    start_loc = 3512
    jump_loc = 5684

    # Push the inital PC value
    loc_ba = bitarray.util.int2ba(start_loc, target.n_bits, endian="little")
    bp.A_bus.value = loc_ba[0:8]
    bp.B_bus.value = loc_ba[8:16]
    target.execute("BRANCH")
    assert bitarray.util.ba2int(target.pc) == start_loc

    # Now set up A & B with the branch target
    loc_ba = bitarray.util.int2ba(jump_loc, target.n_bits, endian="little")
    bp.A_bus.value = loc_ba[0:8]
    bp.B_bus.value = loc_ba[8:16]

    # Set up C bus to be non_zero
    bp.C_bus.value = bitarray.util.int2ba(2, length=bp.n_bits, endian="little")

    # Check that we increment instead of branching
    target.execute("BRANCH_IF_ZERO")
    assert (
        bitarray.util.ba2int(target.pc) == start_loc + 2
    )  # We will have incremented instead

    # Now have C_bus be zero, see that we branch
    bp.C_bus.value = bitarray.util.zeros(8, endian="little")
    target.execute("BRANCH_IF_ZERO")
    assert bitarray.util.ba2int(target.pc) == jump_loc


def test_execute_branch_if_nonzero():
    bp = BackPlane(8)
    target = ProgramCounter(bp)

    start_loc = 3512
    jump_loc = 5684

    # Push the inital PC value
    loc_ba = bitarray.util.int2ba(start_loc, target.n_bits, endian="little")
    bp.A_bus.value = loc_ba[0:8]
    bp.B_bus.value = loc_ba[8:16]
    target.execute("BRANCH")
    assert bitarray.util.ba2int(target.pc) == start_loc

    # Now set up A & B with the branch target
    loc_ba = bitarray.util.int2ba(jump_loc, target.n_bits, endian="little")
    bp.A_bus.value = loc_ba[0:8]
    bp.B_bus.value = loc_ba[8:16]

    # Check that we increment instead of branching
    bp.C_bus.value = bitarray.util.zeros(8, endian="little")
    target.execute("BRANCH_IF_NONZERO")
    assert bitarray.util.ba2int(target.pc) == start_loc + 2

    # Check that we branch
    bp.C_bus.value = bitarray.util.int2ba(2, length=bp.n_bits, endian="little")
    target.execute("BRANCH_IF_NONZERO")
    assert bitarray.util.ba2int(target.pc) == jump_loc
