from typing import Tuple

import bitarray
import bitarray.util

from ._backplane import BackPlane
from ._status_register import StatusRegister


class RegisterUnit:
    def __init__(self, backplane: BackPlane, status_register: StatusRegister):
        self._bp = backplane
        self._sr = status_register
        self._n_bits = self._bp.n_bits

    @property
    def n_bits(self) -> int:
        return self._n_bits

    def decode(self, instruction: bitarray.bitarray) -> Tuple[str, str]:
        assert instruction.endian() == "little"
        assert len(instruction) == 2 * self.n_bits

        # Decode complicated by the SETnnn instruction
        if bitarray.util.ba2int(instruction[3:5]) == 0:
            value_bits = instruction[5:13]
            value = bitarray.util.ba2int(value_bits)
            operation = f"SET{value:03}"
        elif bitarray.util.ba2int(instruction[3:7]) ==1:
            # We have a LOAD STATUS instruction
            operation = "LOADSTATUS"
        else:
            # HAVE NOT YET FILLED OUT ALL VALID INSTRUCTIONS
            raise ValueError(f"RegisterUnit failed to decode {instruction}")

        commit_target = "REGISTERS"
        return operation, commit_target

    def execute(self, command: str):
        if command.startswith("SET"):
            value_str = command[3:7]
            value = int(value_str)
            self._bp.C_bus.value = bitarray.util.int2ba(
                value, self.n_bits, endian="little"
            )
        elif command == "LOADSTATUS":
            self._sr.execute(command)
        else:
            raise ValueError(f"RegisterUnit unrecognised command : {command}")
