import bitarray
import bitarray.util

from ._main_memory import MainMemory
from ._memory import Memory
from ._backplane import BackPlane

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
        self._registers = Memory(self.n_registers, n_bits_per_byte)
        self._input_registers = Memory(8, n_bits_per_byte)
        self._output_registers = Memory(8, n_bits_per_byte)
        self._backplane = BackPlane(n_bits_per_byte)
        self._main_memory = MainMemory(
            2**n_bits_per_byte, self.backplane
        )

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
    def registers(self) -> Memory:
        return self._registers

    @property
    def output_registers(self) -> Memory:
        return self._output_registers

    @property
    def backplane(self) -> BackPlane:
        return self._backplane

    @property
    def main_memory(self) -> MainMemory:
        return self._main_memory
