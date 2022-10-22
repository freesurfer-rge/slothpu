import pytest

import bitarray.util

from slothpu import BackPlane, ProgramCounter


def test_smoke():
    bp = BackPlane(8)
    target = ProgramCounter(bp)

    assert bitarray.util.ba2int(target.pc) == 0
    assert bitarray.util.ba2int(target.jr) == 0


def test_increment():
    bp = BackPlane(8)
    target = ProgramCounter(bp)
    assert bitarray.util.ba2int(target.jr) == 0

    assert bitarray.util.ba2int(target.pc) == 0
    target.increment()
    assert bitarray.util.ba2int(target.pc) == 2
    assert bitarray.util.ba2int(target.jr) == 0

@pytest.mark.parametrize('delta', [0, 2, 4, 8, 24, 254])
def test_addpc(delta: int):
    bp = BackPlane(8)
    target = ProgramCounter(bp)
    assert bitarray.util.ba2int(target.jr) == 0

    assert bitarray.util.ba2int(target.pc) == 0
    
    delta_ba = bitarray.util.int2ba(delta, target.n_bits, endian="little")
    target.add_pc(delta_ba)
    assert bitarray.util.ba2int(target.pc) == delta
    assert bitarray.util.ba2int(target.jr) == 0
    target.add_pc(delta_ba)
    assert bitarray.util.ba2int(target.pc) == 2 * delta
    assert bitarray.util.ba2int(target.jr) == 0

def test_updatepc():
    bp = BackPlane(8)
    target = ProgramCounter(bp)
    assert bitarray.util.ba2int(target.jr) == 0

    assert bitarray.util.ba2int(target.pc) == 0
    target.updatepc("NOT_BRANCH")
    target.updatepc("NOT_BRANCH")
    assert bitarray.util.ba2int(target.pc) == 4
    target._increment_enable = False
    # Have to use a command which can disable incrementing
    # Since PC has internal sanity check
    target.updatepc("JUMP")
    assert bitarray.util.ba2int(target.pc) == 4
    assert bitarray.util.ba2int(target.jr) == 0


def test_fetch0():
    bp = BackPlane(8)
    target = ProgramCounter(bp)

    # Want to poke a value which will affect the upper and lower byte
    start_loc = 8200
    loc_ba = bitarray.util.int2ba(start_loc, target.n_bits, endian="little")
    bp.A_bus.value = loc_ba[0:8]
    bp.B_bus.value = loc_ba[8:16]
    target.commit("JUMP")
    assert target.increment_enable is False  # Because we pushed a jump

    assert bitarray.util.ba2int(target.pc) == start_loc

    # Clear the buses
    bp.A_bus.value = bitarray.util.zeros(8, endian="little")
    bp.B_bus.value = bitarray.util.zeros(8, endian="little")

    target.fetch0()
    expect_b, expect_a = divmod(start_loc, 2**bp.n_bits)
    assert bitarray.util.ba2int(bp.A_bus.value) == expect_a
    assert bitarray.util.ba2int(bp.B_bus.value) == expect_b
    # FETCH0 should re-enable increment
    assert target.increment_enable is True
    assert bitarray.util.ba2int(target.jr) == 0


def test_fetch1():
    bp = BackPlane(8)
    target = ProgramCounter(bp)

    # Want to poke a value which will affect the upper and lower byte
    start_loc = 9200
    loc_ba = bitarray.util.int2ba(start_loc, target.n_bits, endian="little")
    bp.A_bus.value = loc_ba[0:8]
    bp.B_bus.value = loc_ba[8:16]
    target.commit("JUMP")
    assert target.increment_enable is not True

    assert bitarray.util.ba2int(target.pc) == start_loc

    bp.A_bus.value = bitarray.util.zeros(8, endian="little")
    bp.B_bus.value = bitarray.util.zeros(8, endian="little")
    target.fetch1()
    expect_b, expect_a = divmod(start_loc + 1, 2**bp.n_bits)
    assert bitarray.util.ba2int(bp.A_bus.value) == expect_a
    assert bitarray.util.ba2int(bp.B_bus.value) == expect_b
    assert bitarray.util.ba2int(target.jr) == 0


def test_jump():
    bp = BackPlane(8)
    target = ProgramCounter(bp)

    target.increment()
    target.increment()
    assert target.increment_enable
    assert bitarray.util.ba2int(target.pc) == 4
    loc = 4000
    loc_ba = bitarray.util.int2ba(loc, target.n_bits, endian="little")
    bp.A_bus.value = loc_ba[0:8]
    bp.B_bus.value = loc_ba[8:16]
    target.commit("JUMP")
    assert bitarray.util.ba2int(target.pc) == loc
    assert not target.increment_enable
    assert bitarray.util.ba2int(target.jr) == 0


def test_jump_if_zero():
    bp = BackPlane(8)
    target = ProgramCounter(bp)

    start_loc = 3512
    jump_loc = 5684

    # Push the inital PC value
    loc_ba = bitarray.util.int2ba(start_loc, target.n_bits, endian="little")
    bp.A_bus.value = loc_ba[0:8]
    bp.B_bus.value = loc_ba[8:16]
    target.commit("JUMP")
    assert bitarray.util.ba2int(target.pc) == start_loc

    # Now set up A & B with the jump target
    loc_ba = bitarray.util.int2ba(jump_loc, target.n_bits, endian="little")
    bp.A_bus.value = loc_ba[0:8]
    bp.B_bus.value = loc_ba[8:16]

    # Set up C bus to be non_zero
    bp.C_bus.value = bitarray.util.int2ba(2, length=bp.n_bits, endian="little")

    # Check that we do not jump and we leave incrementing enabled
    target._increment_enable = True
    target.commit("JUMPZERO")
    assert bitarray.util.ba2int(target.pc) == start_loc
    assert target.increment_enable is True

    # Now have C_bus be zero, see that we jump and disable incrementing
    bp.C_bus.value = bitarray.util.zeros(8, endian="little")
    target.commit("JUMPZERO")
    assert bitarray.util.ba2int(target.pc) == jump_loc
    assert target.increment_enable is False
    assert bitarray.util.ba2int(target.jr) == 0


def test_jsr():
    bp = BackPlane(8)
    target = ProgramCounter(bp)

    start_loc = 3512
    subroutine_loc = 7932

    # Push the inital PC value
    loc_ba = bitarray.util.int2ba(start_loc, target.n_bits, endian="little")
    bp.A_bus.value = loc_ba[0:8]
    bp.B_bus.value = loc_ba[8:16]
    target.commit("JUMP")
    assert bitarray.util.ba2int(target.pc) == start_loc
    assert bitarray.util.ba2int(target.jr) == 0

    # Now set up A & B with the jump target
    loc_ba = bitarray.util.int2ba(subroutine_loc, target.n_bits, endian="little")
    bp.A_bus.value = loc_ba[0:8]
    bp.B_bus.value = loc_ba[8:16]

    # Jump to the subroutine
    target.execute("JSR")
    assert bitarray.util.ba2int(target.jr) == start_loc
    target.commit("JSR")
    assert bitarray.util.ba2int(target.pc) == subroutine_loc
    assert target.increment_enable is False


def test_ret():
    bp = BackPlane(8)
    target = ProgramCounter(bp)

    start_loc = 3512

    # Push the inital PC value
    loc_ba = bitarray.util.int2ba(start_loc, target.n_bits, endian="little")
    bp.A_bus.value = loc_ba[0:8]
    bp.B_bus.value = loc_ba[8:16]
    target.commit("JUMP")
    assert bitarray.util.ba2int(target.pc) == start_loc
    assert bitarray.util.ba2int(target.jr) == 0

    # Now set up A & B with some random value
    loc_ba = bitarray.util.int2ba(8848, target.n_bits, endian="little")
    bp.A_bus.value = loc_ba[0:8]
    bp.B_bus.value = loc_ba[8:16]

    # Now do the return
    target.commit("RET")
    assert bitarray.util.ba2int(target.pc) == 0
    assert bitarray.util.ba2int(target.jr) == 0
    assert target.increment_enable is True


def test_store_load_jr():
    bp = BackPlane(8)
    target = ProgramCounter(bp)

    assert bitarray.util.ba2int(target.jr) == 0

    loc = 3512
    loc_ba = bitarray.util.int2ba(loc, target.n_bits, endian="little")
    bp.A_bus.value = loc_ba[0:8]
    bp.B_bus.value = loc_ba[8:16]

    # Store in JR
    target.commit("STOREJUMP")
    assert bitarray.util.ba2int(target.jr) == 3512

    # Clear the buses
    bp.A_bus.value = bitarray.util.zeros(bp.n_bits, endian="little")
    bp.B_bus.value = bitarray.util.zeros(bp.n_bits, endian="little")
    bp.C_bus.value = bitarray.util.zeros(bp.n_bits, endian="little")

    # Load lower bits
    target.execute("LOADJUMP0")
    assert bp.C_bus.value == loc_ba[0:8]
    # Load the upper bits
    target.execute("LOADJUMP1")
    assert bp.C_bus.value == loc_ba[8:16]
