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

    def _set_pc(self, value: bitarray.bitarray):
        assert isinstance(value, bitarray.bitarray)
        assert len(value) == self._backplane.n_bits
        assert value.endian() == "little"
        assert value[0] == 0, "Must set PC to be even"
        # Make sure we copy
        self._pc = bitarray.bitarray(value)

    def increment(self):
        step = bitarray.util.int2ba(2, length=self._backplane.n_bits, endian="little")
        self._pc, _ = bitarray_add(self.pc, step, carry_in=0)

    def execute(self, command: str):
        if command == "INC":
            self.increment()
        elif command == "BRANCH":
            # Copy....
            self._set_pc(bitarray.bitarray(self._backplane.A_bus.value))
        elif command == "BRANCH_IF_ZERO":
            if bitarray.util.ba2int(self._backplane.B_bus.value) == 0:
                self._set_pc(bitarray.bitarray(self._backplane.A_bus.value))
            else:
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
