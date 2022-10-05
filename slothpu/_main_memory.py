from turtle import back
import bitarray.util

from ._backplane import BackPlane
from ._memory import Memory


class MainMemory:
    main_memory_address_bits = 14

    def __init__(self, backplane: BackPlane):
        assert backplane is not None
        assert isinstance(backplane, BackPlane)
        self._backplane = backplane
        self._memory = Memory(n_locations=2**MainMemory.main_memory_address_bits, n_bits=self._backplane.n_bits)

    @property
    def memory(self) -> Memory:
        return self._memory

    def execute(self, command: str):
        # Concatenate A and B buses for the address
        ba_address = self._backplane.A_bus.value + self._backplane.B_bus.value
        address = bitarray.util.ba2int(ba_address)

        if command == "READ":
            self._backplane.C_bus.value = self._memory[address]
        elif command == "WRITE":
            self._memory[address] = self._backplane.C_bus.value
        else:
            raise ValueError("Unrecognised memory command: " + command)
