from slothpu.interface import SlothPU_Interface


def test_smoke():
    # A very simple smoke test....
    spu = SlothPU_Interface()
    assert spu is not None
