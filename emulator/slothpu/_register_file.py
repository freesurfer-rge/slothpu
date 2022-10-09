import bitarray
import bitarray.util

from ._backplane import BackPlane
from ._memory import Memory


class RegisterFile:
    def __init__(self, n_registers:int, backplane: BackPlane):
        self._backplane = backplane
        self._n_bits = self._backplane.n_bits
        self._registers = Memory(n_registers, self.n_bits)
        self._write_B_register = False
        self._write_C_register = False

    
    @property
    def n_bits(self) -> int:
        return self._n_bits

    @property
    def registers(self) -> Memory:
        return self._registers

    def set_B_write(self, write_B_register: bool):
        self._write_B_register = write_B_register

    def set_C_write(self, write_C_register: bool):
        self._write_C_register = write_C_register