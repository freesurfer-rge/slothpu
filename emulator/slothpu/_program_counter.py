import bitarray
import bitarray.util

from ._backplane import BackPlane
from ._utils import bitarray_add, to_01_bigendian


class ProgramCounter:
    def __init__(self, backplane: BackPlane):
        self._backplane = backplane
        self._n_bits = 2 * self._backplane.n_bits
        self._pc = bitarray.util.zeros(self.n_bits, endian="little")

    @property
    def pc(self) -> bitarray.bitarray:
        assert len(self._pc) == self.n_bits
        assert self._pc.endian() == "little"
        assert self._pc[0] == 0, "PC must be even"
        return self._pc

    @property
    def n_bits(self) -> int:
        return self._n_bits

    def get_as_string(self) -> str:
        return to_01_bigendian(self.pc)

    def _set_pc(self, value: bitarray.bitarray):
        assert isinstance(value, bitarray.bitarray)
        assert len(value) == self.n_bits
        assert value.endian() == "little"
        assert value[0] == 0, "Must set PC to be even"
        # Make sure we copy
        self._pc = bitarray.bitarray(value)

    def increment(self):
        step = bitarray.util.int2ba(2, length=self.n_bits, endian="little")
        self._pc, _ = bitarray_add(self.pc, step, carry_in=0)

    def execute(self, command: str):
        if command == "INC":
            self.increment()
        elif command == "BRANCH":
            # Copy....
            target = self._backplane.A_bus.value + self._backplane.B_bus.value
            self._set_pc(target)
        elif command == "BRANCH_IF_ZERO":
            target = self._backplane.A_bus.value + self._backplane.B_bus.value
            if bitarray.util.ba2int(self._backplane.C_bus.value) == 0:
                self._set_pc(target)
            else:
                self.increment()
        elif command == "BRANCH_IF_NONZERO":
            target = self._backplane.A_bus.value + self._backplane.B_bus.value
            if bitarray.util.ba2int(self._backplane.C_bus.value) == 0:
                self.increment()
            else:
                self._set_pc(target)
        elif command == "FETCH0":
            # Put current address onto A_bus and B_bus
            self._backplane.A_bus.value = self._pc[0:8]
            self._backplane.B_bus.value = self._pc[8:16]
        elif command == "FETCH1":
            # Put current address+1 onto A_bus and B_bus
            one = bitarray.util.int2ba(
                1, length=self._backplane.n_bits, endian="little"
            )
            self._backplane.A_bus.value = self._pc[0:8] | one
            self._backplane.B_bus.value = self._pc[8:16]
        else:
            raise ValueError("Unrecognised PC command: " + command)