import bitarray
import bitarray.util

pipeline_stages = [
    "Fetch0",
    "Fetch1",
    "Decode",
    "Execute",
    "Commit",
    "UpdatePC",
    "Inactive",
]
n_pipeline_stages = len(pipeline_stages)

n_bits_per_byte = 8


class SlothPU:
    def __init__(self):
        self._pipeline_stage: int = n_pipeline_stages - 1
        self.n_registers = 8
        self._registers = [
            bitarray.util.zeros(n_bits_per_byte) for _ in range(self.n_registers)
        ]
        for i in range(self.n_registers):
            self._registers[i][i] = 1

    @property
    def pipeline_stage(self) -> str:
        assert self._pipeline_stage < n_pipeline_stages
        return pipeline_stages[self._pipeline_stage]

    def advance_pipeline(self):
        assert self._pipeline_stage < n_pipeline_stages
        if self._pipeline_stage == n_pipeline_stages - 1:
            self._pipeline_stage = 0
        else:
            self._pipeline_stage = (self._pipeline_stage + 1) % (n_pipeline_stages - 1)

    def get_register(self, i: int) -> bitarray.bitarray:
        assert len(self._registers[i]) == n_bits_per_byte
        return self._registers[i]
