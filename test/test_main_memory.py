import bitarray.util

from slothpu import BackPlane, MainMemory


def test_smoke():
    n_bits = 8
    bp = BackPlane(n_bits)

    target = MainMemory(bp)

    target_loc = 4000
    assert target_loc < 2**14 # Only have 14 bits of address lines
    tl_ba = bitarray.util.int2ba(target_loc, 16, endian="little")
    bp.A_bus.value = tl_ba[0:8]
    bp.B_bus.value = tl_ba[8:16]
    assert bp.C_bus.value == bitarray.util.zeros(8, endian="little")
    target.execute("READ")
    # Memory values are initialised to their location
    assert bitarray.util.ba2int(bp.C_bus.value) == target_loc %  2**n_bits

    # Now write
    write_value = 21
    bp.C_bus.value = bitarray.util.int2ba(write_value, length=n_bits, endian="little")
    target.execute("WRITE")
    # Read it back
    bp.C_bus.value = bitarray.util.zeros(8, endian='little')
    target.execute("READ")
    assert bitarray.util.ba2int(bp.C_bus.value) == write_value
