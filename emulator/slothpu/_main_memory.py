from typing import List, Optional

import bitarray.util

from ._backplane import BackPlane
from ._memory import Memory


class MainMemory:
    main_memory_address_bits = 14

    def __init__(
        self, backplane: BackPlane, initial_memory: Optional[List[int]] = None
    ):
        assert backplane is not None
        assert isinstance(backplane, BackPlane)
        self._backplane = backplane
        self._memory = Memory(
            n_locations=2**MainMemory.main_memory_address_bits,
            n_bits=self._backplane.n_bits,
        )
        if initial_memory is not None:
            for i, v in enumerate(initial_memory):
                assert v < 256
                assert i < len(self._memory)
                self._memory[i] = bitarray.util.int2ba(
                    v, self._backplane.n_bits, endian="little"
                )

    @property
    def memory(self) -> Memory:
        return self._memory

    def fetch0(self):
        self.execute("READ")

    def fetch1(self):
        self.execute("READ")

    def execute(self, command: str):
        # Concatenate A and B buses for the address
        ba_address = self._backplane.A_bus.value + self._backplane.B_bus.value
        address = bitarray.util.ba2int(ba_address)

        if command == "READ":
            self._backplane.C_bus.value = self._memory[address]
        elif command == "WRITE":
            pass
        else:
            raise ValueError("Unrecognised memory command: " + command)

    def commit(self, command: str):
        ba_address = self._backplane.A_bus.value + self._backplane.B_bus.value
        address = bitarray.util.ba2int(ba_address)
        if command == "READ":
            pass
        elif command == "WRITE":
            self._memory[address] = self._backplane.C_bus.value
        else:
            raise ValueError("Unrecognised memory command: " + command)