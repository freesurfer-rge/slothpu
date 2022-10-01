pipeline_stages = ["Fetch0", "Fetch1", "Decode", "Execute", "Commit", "UpdatePC", "Inactive"]
n_pipeline_stages = len(pipeline_stages)

class SlothPU:
    def __init__(self):
        self._pipeline_stage: int = n_pipeline_stages - 1

    @property
    def pipeline_stage(self) -> str:
        assert self._pipeline_stage < n_pipeline_stages
        return pipeline_stages

    def advance_pipeline(self):
        assert self._pipeline_stage < n_pipeline_stages
        if self._pipeline_stage == n_pipeline_stages-1:
            self._pipeline_stage = 0
        else:
            self._pipeline_stage = (self._pipeline_stage+1) % (n_pipeline_stages-1)