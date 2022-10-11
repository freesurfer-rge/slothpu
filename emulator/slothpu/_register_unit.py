import bitarray
import bitarray.util

from ._backplane import BackPlane


class RegisterUnit:
    def __init__(self, backplane: BackPlane):
        self._bp = backplane
        self._n_bits = self._bp.n_bits

    @property
    def n_bits(self) -> int:
        return self._n_bits

    def execute(self, command:str):
        if command.startswith("SET"):
            value_str = command[3:7]
            value = int(value_str)
            self._bp.C_bus.value = bitarray.util.int2ba(value, self.n_bits, endian="little")
        else:
            raise ValueError(f"RegisterUnit unrecognised command : {command}")