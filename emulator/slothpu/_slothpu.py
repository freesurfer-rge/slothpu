from ._backplane import BackPlane
from ._instruction_register import InstructionRegister
from ._main_memory import MainMemory
from ._program_counter import ProgramCounter
from ._status_register import StatusRegister
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
        self._backplane = BackPlane(n_bits_per_byte)
        self._main_memory = MainMemory(self.backplane)
        self._register_file = RegisterFile(self.n_registers, self.backplane)
        self._program_counter = ProgramCounter(self._backplane)
        self._instruction_register = InstructionRegister(self._backplane)
        self._status_register = StatusRegister(self._backplane)

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
            self.program_counter.execute("FETCH0")
            self.main_memory.execute("READ")
            self.instruction_register.execute("FETCH0")
        elif self._pipeline_stage == 1:
            # Fetch1
            # PARTIALLY COMPLETE
            self.program_counter.execute("FETCH1")
            self.main_memory.execute("READ")
            self.instruction_register.execute("FETCH1")
        elif self._pipeline_stage == 2:
            # PARTIALLY COMPLETE
            self.instruction_register.execute("DECODE")

            # B and C are more complex and TBD...
            self.register_file.A_register = self.instruction_register.R_A
            self.register_file.write_B_register = True  # TO BE UPDATED!
            self.register_file.execute("RegisterRead")
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
            self.program_counter.execute("INC")
        else:
            raise ValueError(f"Can't do anything: {self._pipeline_stage}")

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
