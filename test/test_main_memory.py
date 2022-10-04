import bitarray.util

from slothpu import BackPlane, MainMemory


def test_smoke():
    n_bits = 8
    bp = BackPlane(n_bits)

    target = MainMemory(2**n_bits, n_bits, bp)

    target_loc = 127
    tl_ba = bitarray.util.int2ba(target_loc, endian="little")
    tl_ba.fill()  # Since n_bits=8
    bp.A_bus.value = tl_ba
    assert bp.W_bus.value == bitarray.util.zeros(8, endian="little")
    target.execute("READ")
    # Memory values are initialised to their location
    assert bitarray.util.ba2int(bp.W_bus.value) == target_loc

    # Now write
    write_value = 21  # Big enough to use 8 bits
    bp.B_bus.value = bitarray.util.int2ba(write_value, length=n_bits, endian="little")
    target.execute("WRITE")
    # Read it back
    assert bitarray.util.ba2int(bp.W_bus.value) == target_loc  # Should be unchanged
    target.execute("READ")
    assert bitarray.util.ba2int(bp.W_bus.value) == write_value
