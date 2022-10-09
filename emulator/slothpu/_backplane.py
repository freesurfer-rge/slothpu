from ._bus import Bus


class BackPlane:
    def __init__(self, n_bits: int):
        self._n_bits = n_bits
        self._A_bus = Bus(self.n_bits)
        self._B_bus = Bus(self.n_bits)
        self._C_bus = Bus(self.n_bits)
        self._salu_flag = 0
        self._dalu_flag = 0

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
    def C_bus(self) -> Bus:
        return self._C_bus

    @property
    def SALU_flag(self) -> int:
        assert self._salu_flag == 0 or self._salu_flag == 1
        return self._salu_flag

    @SALU_flag.setter
    def SALU_flag(self, value: int):
        assert isinstance(value, int)
        assert value == 0 or value == 1
        self._salu_flag = value

    @property
    def DALU_flag(self) -> int:
        assert self._dalu_flag == 0 or self._dalu_flag == 1
        return self._dalu_flag

    @DALU_flag.setter
    def DALU_flag(self, value: int):
        assert isinstance(value, int)
        assert value == 0 or value == 1
        self._dalu_flag = value
