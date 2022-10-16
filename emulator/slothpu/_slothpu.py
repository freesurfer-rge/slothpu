from typing import List, Optional

from ._backplane import BackPlane
from ._dalu import DALU
from ._instruction_register import InstructionRegister
from ._main_memory import MainMemory
from ._program_counter import ProgramCounter
from ._salu import SALU
from ._status_register import StatusRegister
from ._register_file import RegisterFile
from ._register_unit import RegisterUnit

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
    def __init__(self, initial_memory: Optional[List[int]] = None):
        self._pipeline_stage: int = n_pipeline_stages - 1
        self.n_registers = 8
        self._backplane = BackPlane(n_bits_per_byte)
        self._main_memory = MainMemory(self.backplane, initial_memory)
        self._register_file = RegisterFile(self.n_registers, self.backplane)
        self._program_counter = ProgramCounter(self._backplane)
        self._instruction_register = InstructionRegister(self._backplane)
        self._status_register = StatusRegister(self._backplane)
        self._register_unit = RegisterUnit(self._backplane)
        self._salu = SALU(self.backplane)
        self._dalu = DALU(self.backplane)

        self._dispatcher = {
            "PC": self._program_counter,
            "REG": self._register_unit,
            "MEM": self._main_memory,
            "SALU": self._salu,
            "DALU": self._dalu,
        }

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

        if self._pipeline_stage == 0:
            # Fetch0
            # PARTIALLY COMPLETE
            self.program_counter.fetch0()
            self.main_memory.fetch0()
            self.instruction_register.fetch0()
        elif self._pipeline_stage == 1:
            # Fetch1
            # PARTIALLY COMPLETE
            self.program_counter.fetch1()
            self.main_memory.fetch1()
            self.instruction_register.fetch1()
        elif self._pipeline_stage == 2:
            self.decode_stage()
        elif self._pipeline_stage == 3:
            # Execute
            # PARTIALLY COMPLETE
            self._status_register.update()
        elif self._pipeline_stage == 4:
            # Commit
            # PARTIALLY COMPLETE
            self._status_register.update()
        elif self._pipeline_stage == 5:
            # UpdatePC
            # JUST FOR NOW
            self.program_counter.updatepc()
        else:
            raise ValueError(f"Can't do anything: {self._pipeline_stage}")

    def decode_stage(self):
        self.instruction_register.decode()

        operation, write_C_register = self._dispatcher[self.instruction_register.unit].decode(self.instruction_register.ir)
        self.instruction_register.operation = operation

        # B and C are more complex and TBD...
        self.register_file.A_register = self.instruction_register.R_A
        self.register_file.B_register = self.instruction_register.R_B
        self.register_file.C_register = self.instruction_register.R_C
        self.register_file.write_C_register = write_C_register
        self.register_file.decode()

    @property
    def register_file(self) -> RegisterFile:
        return self._register_file

    @property
    def backplane(self) -> BackPlane:
        return self._backplane

    @property
    def main_memory(self) -> MainMemory:
        return self._main_memory

    @property
    def program_counter(self) -> ProgramCounter:
        return self._program_counter

    @property
    def instruction_register(self) -> InstructionRegister:
        return self._instruction_register

    @property
    def status_register(self) -> StatusRegister:
        return self._status_register

    @property
    def salu(self) -> SALU:
        return self._salu

    @property
    def dalu(self) -> DALU:
        return self._dalu
