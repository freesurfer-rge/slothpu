from slothpu import BackPlane


def test_smoke():
    num_bits = 8
    target = BackPlane(num_bits)

    assert target.A_bus.n_bits == num_bits
    assert target.B_bus.n_bits == num_bits
    assert target.C_bus.n_bits == num_bits


