import bitarray
import bitarray.util

from ._backplane import BackPlane
from ._utils import bitarray_add


class ProgramCounter:
    def __init__(self, backplane: BackPlane):
        self._backplane = backplane
        self._pc = bitarray.util.zeros(self._backplane.n_bits, endian="little")

    @property
    def pc(self) -> bitarray.bitarray:
        assert len(self._pc) == self._backplane.n_bits
        assert self._pc.endian() == "little"
        assert self._pc[0] == 0, "PC must be even"
        return self._pc

    def increment(self):
        step = bitarray.util.int2ba(2, length=self._backplane.n_bits, endian="little")
        self._pc, _ = bitarray_add(self.pc, step, carry_in=0)

    def execute(self, command: str):
        if command == "INC":
            self.increment()
        elif command == "FETCH0":
            # Put current address onto A_bus
            self._backplane.A_bus.value = self._pc
        elif command == "FETCH1":
            # Put current address+1 onto A_bus
            one = bitarray.util.int2ba(
                1, length=self._backplane.n_bits, endian="little"
            )
            self._backplane.A_bus.value = self._pc | one
        else:
            raise ValueError("Unrecognised PC command: " + command)
