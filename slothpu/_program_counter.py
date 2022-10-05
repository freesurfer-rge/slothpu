import bitarray
import bitarray.util

from ._backplane import BackPlane

class ProgramCounter:
    def __init__(self, backplane: BackPlane):
        self._backplane = backplane
        self._pc = bitarray.util.zeros(length=self._backplane.n_bits, endian="little")

    @property
    def pc(self) -> bitarray.bitarray:
        assert len(self._pc)== self._backplane.n_bits
        assert self._pc.endian() == 'little'
        return self._pc