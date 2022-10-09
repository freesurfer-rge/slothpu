import bitarray
import bitarray.util

from ._backplane import BackPlane

from ._utils import to_01_bigendian

class StatusRegister:
    salu_bit = 0
    dalu_bit = 1

    def __init__(self,  backplane: BackPlane):
        self._backplane = backplane
        self._n_bits = self._backplane.n_bits
        self._value = bitarray.util.zeros(self.n_bits, endian='little')

    @property
    def n_bits(self) -> int:
        return self._n_bits

    @property
    def value(self) -> bitarray.bitarray:
        assert len(self._value)==self.n_bits
        assert self._value.endian() == 'little'
        return self._value

    def update(self):
        assert len(self._value)==self.n_bits
        assert self._value.endian() == 'little'
        print(f"salubit: {StatusRegister.salu_bit}")
        self._value[StatusRegister.salu_bit] = self._backplane.SALU_flag
        self._value[StatusRegister.dalu_bit] = self._backplane.DALU_flag

    def get_as_string(self):
        return to_01_bigendian(self._value)

    def execute(self, command: str):
        if command == "LOADSTATUS":
            self._backplane.C_bus.value = self._value
        else:
            raise ValueError(f"Unrecognised StatusRegister Command: {command}")
