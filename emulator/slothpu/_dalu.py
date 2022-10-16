from typing import Tuple

import bitarray

from ._backplane import BackPlane

from ._utils import bitarray_add


class DALU:
    def __init__(self, backplane: BackPlane):
        self._bp = backplane
        self._n_bits = self._bp.n_bits

    @property
    def n_bits(self) -> int:
        return self._n_bits

    def decode(self, instruction: bitarray.bitarray) -> Tuple[str, str]:
        assert instruction.endian() == "little"
        assert len(instruction) == 2*self.n_bits

        commit_target = "REGISTERS"

        operations = {
            0: "ADD",
            1: "SUB",
            4: "OR",
            5: "XOR",
            6: "AND",
            7:"NAND"
        }

        op_ba = instruction[3:7]
        op = operations[bitarray.util.ba2int(op_ba)]

        return op, commit_target

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
        elif command == "AND":
            self._bp.C_bus.value = self._bp.A_bus.value & self._bp.B_bus.value
            self._bp.DALU_flag = 0
        elif command == "XOR":
            self._bp.C_bus.value = self._bp.A_bus.value ^ self._bp.B_bus.value
            self._bp.DALU_flag = 0
        elif command == "NAND":
            self._bp.C_bus.value = ~(self._bp.A_bus.value & self._bp.B_bus.value)
            self._bp.DALU_flag = 0
        else:
            raise ValueError(f"DALU: Unrecognised {command}")
