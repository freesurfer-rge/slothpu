from typing import Union

import bitarray
import bitarray.util

from ._utils import to_01_bigendian


class Memory:
    def __init__(self, n_locations: int, n_bits: int):
        # Memory is stored little-endian since it's convenient
        # for bit 0 to be the least significant
        self._n_bits = n_bits
        self._locations = [
            bitarray.util.zeros(self.n_bits, endian="little")
            for _ in range(n_locations)
        ]
        for i in range(n_locations):
            self[i] = bitarray.util.int2ba(i, endian="little")

    @property
    def n_bits(self) -> int:
        return self._n_bits

    def __len__(self):
        return len(self._locations)

    def __getitem__(self, key: int) -> bitarray.bitarray:
        assert isinstance(self._locations[key], bitarray.bitarray)
        assert len(self._locations[key]) == self.n_bits
        assert self._locations[key].endian() == "little"
        return self._locations[key]

    def __setitem__(self, key: int, value: Union[str, bitarray.bitarray]):
        assert isinstance(value, str) or isinstance(value, bitarray.bitarray)
        assert key >= 0
        assert key < len(self)

        if isinstance(value, bitarray.bitarray):
            assert value.endian() == "little"
            assert len(value) <= self.n_bits
            # Make sure we have a copy
            self._locations[key] = bitarray.bitarray(value)
        else:
            # Assume that a string is supplied big-endian
            # This means we must reverse it before supplying to the constructor
            self._locations[key] = bitarray.bitarray(value[::-1], endian="little")

        self._locations[key].extend("0" * (self.n_bits - len(self._locations[key])))
        assert len(self._locations[key]) == self.n_bits

    def get_as_string(self, idx: int) -> str:
        assert isinstance(self._locations[idx], bitarray.bitarray)
        assert len(self._locations[idx]) == self.n_bits
        # Converts to 01 string, as Big Endian (storage is Little Endian)
        return to_01_bigendian(self._locations[idx])
