from slothpu import SlothPU


def test_pipeline_step():
    target = SlothPU()

    assert target.pipeline_stage == "Inactive"
    target.advance_pipeline()
    assert target.advance_pipeline == "Fetch0"

