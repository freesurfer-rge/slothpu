import bitarray
import bitarray.util

from ._backplane import BackPlane
from ._utils import to_01_bigendian


class InstructionRegister:
    def __init__(self, backplane: BackPlane):
        self._bp = backplane
        self._n_bits = 2 * self._bp.n_bits
        self._ir = bitarray.util.zeros(self.n_bits, endian="little")
        self._unit = "UNSET"
        self._operation = "UNSET"
        self._commit_target = "UNSET"
        self._R_A = 0
        self._R_B = 0
        self._R_C = 0

    @property
    def ir(self):
        assert len(self._ir) == self.n_bits
        assert self._ir.endian() == "little"
        return self._ir

    @property
    def n_bits(self) -> int:
        return self._n_bits

    @property
    def unit(self) -> str:
        return self._unit

    @property
    def operation(self) -> str:
        return self._operation

    @operation.setter
    def operation(self, value: str):
        self._operation = value

    @property
    def commit_target(self) -> str:
        return self._commit_target

    @commit_target.setter
    def commit_target(self, value: str) -> str:
        assert value in ["REGISTERS", "PC", "MEM"]
        self._commit_target = value

    @property
    def R_A(self) -> int:
        return self._R_A

    @property
    def R_B(self) -> int:
        return self._R_B

    @property
    def R_C(self) -> int:
        return self._R_C

    def get_as_string(self) -> str:
        # Given how it is read, little endian might be better
        return to_01_bigendian(self.ir)

    def fetch0(self):
        self._ir[0:8] = self._bp.C_bus.value

    def fetch1(self):
        self._ir[8:16] = self._bp.C_bus.value

    def decode(self):
        function_units = {
            0 : "PC",
            1 : "MEM",
            2 : "REG",
            4 : "SALU",
            5 : "DALU"
        }
        self._unit = function_units[bitarray.util.ba2int(self._ir[0:3])]
        self._R_A = bitarray.util.ba2int(self._ir[7:10])
        self._R_B = bitarray.util.ba2int(self._ir[10:13])
        self._R_C = bitarray.util.ba2int(self._ir[13:16])
