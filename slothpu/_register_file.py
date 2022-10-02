from typing import Union

import bitarray
import bitarray.util


class RegisterFile:
    def __init__(self, n_registers: int, n_bits: int):
        # Registers are stored little-endian since it's convenient
        # for bit 0 to be the least significant
        self._n_bits = n_bits
        self._registers = [
            bitarray.util.zeros(self.n_bits, endian="little")
            for _ in range(n_registers)
        ]
        for i in range(n_registers):
            self._registers[i][i] = 1

    @property
    def n_bits(self) -> int:
        return self._n_bits

    def __len__(self):
        return len(self._registers)

    def __getitem__(self, key: int) -> bitarray.bitarray:
        assert isinstance(self._registers[key], bitarray.bitarray)
        assert len(self._registers[key]) == self.n_bits
        assert self._registers[key].endian() == "little"
        return self._registers[key]

    def __setitem__(self, key: int, value: Union[str, bitarray.bitarray]):
        assert isinstance(value, str) or isinstance(value, bitarray.bitarray)
        assert key >= 0
        assert key < len(self)

        if isinstance(value, bitarray.bitarray):
            assert value.endian() == "little"
            assert len(value) <= self.n_bits
            # Make sure we have a copy
            self._registers[key] = bitarray.bitarray(value)
        else:
            # Assume that a string is supplied big-endian
            # This means we must reverse it before supplying to the constructor
            self._registers[key] = bitarray.bitarray(value[::-1], endian="little")

        self._registers[key].extend("0" * (self.n_bits - len(self._registers[key])))
        assert len(self._registers[key]) == self.n_bits

    def get_as_string(self, idx: int) -> str:
        assert isinstance(self._registers[idx], bitarray.bitarray)
        assert len(self._registers[idx]) == self.n_bits
        # Converts to 01 string, as Big Endian (storage is Little Endian)
        return self._registers[idx].to01()[::-1]
