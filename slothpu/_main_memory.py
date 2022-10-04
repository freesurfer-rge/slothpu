from turtle import back
import bitarray.util

from ._backplane import BackPlane
from ._memory import Memory


class MainMemory:
    def __init__(self, n_locations: int, n_bits: int, backplane: BackPlane):
        assert backplane is not None
        assert isinstance(backplane, BackPlane)
        self._backplane = backplane
        self._memory = Memory(n_locations=n_locations, n_bits=n_bits)

    @property
    def memory(self) -> Memory:
        return self._memory

    def execute(self, command: str):
        address = bitarray.util.ba2int(self._backplane.A_bus.value)

        if command == "READ":
            self._backplane.W_bus.value = self._memory[address]
        elif command == "WRITE":
            self._memory[address] = self._backplane.B_bus.value
        else:
            raise ValueError("Unrecognised memory command: " + command)
