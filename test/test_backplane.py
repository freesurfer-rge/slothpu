from slothpu import BackPlane


def test_smoke():
    num_bits = 8
    target = BackPlane(num_bits)

    assert target.A_bus.n_bits == num_bits
    assert target.B_bus.n_bits == num_bits
    assert target.W_bus.n_bits == num_bits
    assert target.SALU_flag == 0
    assert target.DALU_flag == 0

def test_set_salu_flag():
    target = BackPlane(8)
    assert target.SALU_flag == 0
    target.SALU_flag = 1
    assert target.SALU_flag == 1


def test_set_dalu_flag():
    target = BackPlane(8)
    assert target.DALU_flag == 0
    target.DALU_flag = 1
    assert target.DALU_flag == 1