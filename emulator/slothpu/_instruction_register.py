import bitarray
import bitarray.util

from ._backplane import BackPlane
from ._utils import to_01_bigendian

class InstructionRegister:
    def __init__(self, backplane: BackPlane):
        self._bp = backplane
        self._n_bits = 2 * self._bp.n_bits
        self._ir = bitarray.util.zeros(self.n_bits, endian="little")

    @property
    def ir(self):
        assert len(self._ir) == self.n_bits
        assert self._ir.endian() == "little"
        return self._ir

    @property
    def n_bits(self) -> int:
        return self._n_bits

    
    def get_as_string(self) -> str:
        return to_01_bigendian(self.ir)

    def execute(self, command: str):
        if command == "Fetch0":
            self._ir[0:8] = self._bp.C_bus.value
        elif command == "Fetch1":
            self._ir[8:16] = self._bp.C_bus.value
        else:
            raise ValueError(f"Unrecognised IR command: {command}")