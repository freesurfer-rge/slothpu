from bitarray import bitarray

from slothpu import SlothPU


def test_register_initialise():
    target = SlothPU()

    assert target.get_register(0) == bitarray("10000000")
    assert target.get_register(1) == bitarray("01000000")
    assert target.get_register(2) == bitarray("00100000")
    assert target.get_register(3) == bitarray("00010000")
    assert target.get_register(4) == bitarray("00001000")
    assert target.get_register(5) == bitarray("00000100")
    assert target.get_register(6) == bitarray("00000010")
    assert target.get_register(7) == bitarray("00000001")

def test_pipeline_step():
    target = SlothPU()

    assert target.pipeline_stage == "Inactive"
    target.advance_pipeline()
    assert target.pipeline_stage == "Fetch0"
    target.advance_pipeline()
    assert target.pipeline_stage == "Fetch1"
    target.advance_pipeline()
    assert target.pipeline_stage == "Decode"
    target.advance_pipeline()
    assert target.pipeline_stage == "Execute"
    target.advance_pipeline()
    assert target.pipeline_stage == "Commit"
    target.advance_pipeline()
    assert target.pipeline_stage == "UpdatePC"
    target.advance_pipeline()
    assert target.pipeline_stage == "Fetch0"
