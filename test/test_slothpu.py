from bitarray import bitarray

from slothpu import SlothPU


def test_register_initialise():
    target = SlothPU()

    assert len(target.registers) == 8
    for i in range(8):
        assert len(target.registers[i]) == 8


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
