import bitarray.util

from ._backplane import BackPlane

from ._utils import bitarray_add


class SALU:
    def __init__(self, backplane: BackPlane):
        self._bp = backplane
        self._n_bits = self._bp.n_bits

    @property
    def n_bits(self) -> int:
        return self._n_bits

    def execute(self, command: str):
        one = bitarray.util.int2ba(1, self.n_bits, endian="little")
        if command == "INC":
            result, carry = bitarray_add(self._bp.A_bus.value, one, 0)
            self._bp.C_bus.value = result
            self._bp.SALU_flag = carry
        elif command == "DEC":
            result, borrow = bitarray_add(
                self._bp.A_bus.value, ~one, 1
            )
            self._bp.C_bus.value = result
            self._bp.SALU_flag = 1 - borrow
        else:
            raise ValueError(f"SALU not recogised {command}")