from ._bus import Bus


class BackPlane:
    def __init__(self, n_bits: int):
        self._n_bits = n_bits
        self._A_bus = Bus(self.n_bits)
        self._B_bus = Bus(self.n_bits)
        self._W_bus = Bus(self.n_bits)

    @property
    def n_bits(self) -> int:
        return self._n_bits

    @property
    def A_bus(self) -> Bus:
        return self._A_bus

    @property
    def B_bus(self) -> Bus:
        return self._B_bus

    @property
    def W_bus(self) -> Bus:
        return self._W_bus
