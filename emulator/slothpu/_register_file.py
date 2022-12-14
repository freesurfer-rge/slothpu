from ._backplane import BackPlane
from ._memory import Memory


class RegisterFile:
    def __init__(self, n_registers: int, backplane: BackPlane):
        self._backplane = backplane
        self._n_bits = self._backplane.n_bits
        self._registers = Memory(n_registers, self.n_bits)
        self._write_C_register = False
        self._A_register = 0
        self._B_register = 0
        self._C_register = 0

    @property
    def n_bits(self) -> int:
        return self._n_bits

    @property
    def registers(self) -> Memory:
        return self._registers

    @property
    def A_register(self) -> int:
        assert self._A_register >= 0 and self._A_register < len(self._registers)
        return self._A_register

    @A_register.setter
    def A_register(self, idx: int):
        assert idx >= 0 and idx < len(self._registers)
        self._A_register = idx

    @property
    def B_register(self) -> int:
        assert self._B_register >= 0 and self._B_register < len(self._registers)
        return self._B_register

    @B_register.setter
    def B_register(self, idx: int):
        assert idx >= 0 and idx < len(self._registers)
        self._B_register = idx

    @property
    def C_register(self) -> int:
        assert self._C_register >= 0 and self._C_register < len(self._registers)
        return self._C_register

    @C_register.setter
    def C_register(self, idx: int):
        assert idx >= 0 and idx < len(self._registers)
        self._C_register = idx

    @property
    def write_C_register(self) -> bool:
        return self._write_C_register

    @write_C_register.setter
    def write_C_register(self, value: bool) -> bool:
        self._write_C_register = value

    def decode(self):
        # Registers are placed on the backplane during the 'decode' step
        self._backplane.A_bus.value = self._registers[self.A_register]
        self._backplane.B_bus.value = self._registers[self.B_register]
        if not self.write_C_register:
            self._backplane.C_bus.value = self._registers[self.C_register]

    def commit(self, command: str):
        assert command is not None
        assert self._write_C_register is True
        self._registers[self.C_register] = self._backplane.C_bus.value
