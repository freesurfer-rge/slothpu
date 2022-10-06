import bitarray.util

from slothpu import BackPlane, InstructionRegister

def test_smoke():
    bp = BackPlane(8)
    target = InstructionRegister(bp)

    assert target.n_bits == 16
    assert len(target.ir) == 16