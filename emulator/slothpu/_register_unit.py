from typing import Tuple

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

    def decode(self, instruction: bitarray.bitarray) -> Tuple[str, bool]:
        assert instruction.endian() == "little"
        assert len(instruction) == 2 * self.n_bits

        # Decode complicated by the SETnnn instruction
        if bitarray.util.ba2int(instruction[3:5]) == 0:
            value_bits = instruction[5:13]
            value = bitarray.util.ba2int(value_bits)
            operation = f"SET{value:03}"
        else:
            # HAVE NOT YET FILLED OUT ALL VALID INSTRUCTIONS
            raise ValueError(f"RegisterUnit failed to decode {instruction}")

        write_reg_C = True
        return operation, write_reg_C

    def execute(self, command: str):
        if command.startswith("SET"):
            value_str = command[3:7]
            value = int(value_str)
            self._bp.C_bus.value = bitarray.util.int2ba(
                value, self.n_bits, endian="little"
            )
        else:
            raise ValueError(f"RegisterUnit unrecognised command : {command}")
