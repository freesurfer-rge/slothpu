import bitarray
import bitarray.util

from ._register_file import RegisterFile

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
        self._registers = RegisterFile(self.n_registers, n_bits_per_byte)
        self._input_registers = RegisterFile(8, n_bits_per_byte)
        self._output_registers = RegisterFile(8, n_bits_per_byte)

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

    @property
    def registers(self) -> RegisterFile:
        return self._registers

    @property
    def output_registers(self) -> RegisterFile:
        return self._output_registers
