import bitarray.util

from slothpu import BackPlane, RegisterFile


def test_smoke():
    bp = BackPlane(n_bits=8)
    target = RegisterFile(8, bp)

    for i in range(8):
        assert bitarray.util.ba2int(target.registers[i]) == i

    assert target.A_register == 0
    assert target.B_register == 0
    assert target.C_register == 0
    target.A_register = 1
    target.B_register = 2
    target.C_register = 3
    assert target.A_register == 1
    assert target.B_register == 2
    assert target.C_register == 3

    assert target.write_C_register is False


def test_decode_all():
    bp = BackPlane(n_bits=8)
    target = RegisterFile(8, bp)

    target.A_register = 4
    target.B_register = 6
    target.C_register = 7

    # Registers are connected to bus during decode step
    target.decode()
    # Registers initialised with their index
    assert bitarray.util.ba2int(bp.A_bus.value) == 4
    assert bitarray.util.ba2int(bp.B_bus.value) == 6
    assert bitarray.util.ba2int(bp.C_bus.value) == 7


def test_decode_notC():
    bp = BackPlane(n_bits=8)
    target = RegisterFile(8, bp)

    target.A_register = 4
    target.B_register = 6
    target.C_register = 7

    target.write_C_register = True

    # Registers are connected to bus during decode step
    target.decode()
    # Registers initialised with their index
    assert bitarray.util.ba2int(bp.A_bus.value) == 4
    assert bitarray.util.ba2int(bp.B_bus.value) == 6
    # We should not update C_bus
    assert bitarray.util.ba2int(bp.C_bus.value) == 0


def test_execute_registerwrite_C():
    bp = BackPlane(n_bits=8)
    write_value = 21
    bp.C_bus.value = bitarray.util.int2ba(write_value, 8, endian="little")
    target = RegisterFile(8, bp)

    target.A_register = 4
    target.B_register = 2
    target.C_register = 1

    target.write_C_register = True

    target.commit("SOME_COMMAND")
    assert bitarray.util.ba2int(target.registers[target.A_register]) == 4
    assert bitarray.util.ba2int(target.registers[target.B_register]) == 2
    assert bitarray.util.ba2int(target.registers[target.C_register]) == write_value
