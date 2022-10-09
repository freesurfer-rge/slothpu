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
    target.C_register =3
    assert target.A_register == 1
    assert target.B_register == 2
    assert target.C_register == 3

    assert target.write_B_register is False
    assert target.write_C_register is False

def test_execute_registerread_all():
    bp = BackPlane(n_bits=8)
    target = RegisterFile(8, bp)

    target.A_register = 4
    target.B_register = 6
    target.C_register = 7

    target.execute("RegisterRead")
    # Registers initialised with their index
    assert bitarray.util.ba2int(bp.A_bus.value) == 4
    assert bitarray.util.ba2int(bp.B_bus.value) == 6
    assert bitarray.util.ba2int(bp.C_bus.value) == 7

def test_execute_registerread_notC():
    bp = BackPlane(n_bits=8)
    target = RegisterFile(8, bp)

    target.A_register = 4
    target.B_register = 6
    target.C_register = 7

    target.write_C_register = True

    target.execute("RegisterRead")
    # Registers initialised with their index
    assert bitarray.util.ba2int(bp.A_bus.value) == 4
    assert bitarray.util.ba2int(bp.B_bus.value) == 6
    assert bitarray.util.ba2int(bp.C_bus.value) == 0


def test_execute_registerread_notB():
    bp = BackPlane(n_bits=8)
    target = RegisterFile(8, bp)

    target.A_register = 4
    target.B_register = 6
    target.C_register = 7

    target.write_B_register = True

    target.execute("RegisterRead")
    # Registers initialised with their index
    # Buses initialised to zero
    assert bitarray.util.ba2int(bp.A_bus.value) == 4
    assert bitarray.util.ba2int(bp.B_bus.value) == 0
    assert bitarray.util.ba2int(bp.C_bus.value) == 7