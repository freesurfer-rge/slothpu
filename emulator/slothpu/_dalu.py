import bitarray
import bitarray.util

from ._backplane import BackPlane

from ._utils import bitarray_add


class DALU:
    def __init__(self, backplane: BackPlane):
        self._bp = backplane
        self._n_bits = self._bp.n_bits

    @property
    def n_bits(self) -> int:
        return self._n_bits

    def execute(self, command: str):
        if command == "ADD":
            result, carry = bitarray_add(self._bp.A_bus.value, self._bp.B_bus.value, 0)
            self._bp.C_bus.value = result
            self._bp.DALU_flag = carry
        elif command == "SUB":
            result, borrow = bitarray_add(
                self._bp.A_bus.value, ~self._bp.B_bus.value, 1
            )
            self._bp.C_bus.value = result
            self._bp.DALU_flag = 1 - borrow
        elif command == "OR":
            self._bp.C_bus.value = self._bp.A_bus.value | self._bp.B_bus.value
            self._bp.DALU_flag = 0
        else:
            raise ValueError(f"DALU: Unrecognised {command}")
