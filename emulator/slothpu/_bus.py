import bitarray
import bitarray.util

from ._utils import to_01_bigendian


class Bus:
    def __init__(self, n_bits: int):
        self._n_bits = n_bits
        self._value = bitarray.util.zeros(self.n_bits, endian="little")

    @property
    def n_bits(self) -> int:
        return self._n_bits

    @property
    def value(self) -> bitarray.bitarray:
        assert isinstance(self._value, bitarray.bitarray)
        assert len(self._value) == self.n_bits
        assert self._value.endian() == "little"
        return self._value

    @value.setter
    def value(self, v: bitarray.bitarray):
        assert isinstance(v, bitarray.bitarray)
        assert len(v) == self.n_bits
        assert v.endian() == "little"
        # Make sure we copy....
        self._value = bitarray.bitarray(v)

    def to01(self):
        return to_01_bigendian(self.value)
