import bitarray.util

from ._backplane import BackPlane

from ._utils import bitarray_add


class SALU:
    def __init__(self, backplane: BackPlane):
        self._bp = backplane
        self._n_bits = self._bp.n_bits

    @property
    def n_bits(self) -> int:
        return self._n_bits

    def execute(self, command: str):
        one = bitarray.util.int2ba(1, self.n_bits, endian="little")
        if command == "INC":
            result, carry = bitarray_add(self._bp.A_bus.value, one, 0)
            self._bp.C_bus.value = result
            self._bp.SALU_flag = carry
        elif command == "DEC":
            result, borrow = bitarray_add(
                self._bp.A_bus.value, ~one, 1
            )
            self._bp.C_bus.value = result
            self._bp.SALU_flag = 1 - borrow
        elif command == "NOT":
            self._bp.C_bus.value = ~self._bp.A_bus.value
            self._bp.SALU_flag = 0
        elif command == "COPY":
            self._bp.C_bus.value = self._bp.A_bus.value
            self._bp.SALU_flag = 0
        elif command == "LBARREL":
            # Slight complication: bitarray shift operators
            # are performed relative to the first element
            # in the array. So with a little-endian interpretation
            # a left shift will shift towards a[0], which
            # would be a _right_ shift on the integer
            top_bit = self._bp.A_bus.value[self.n_bits-1]
            tmp = self._bp.A_bus.value >> 1
            assert len(tmp) == 8
            tmp[0] = top_bit
            self._bp.C_bus.value = tmp
            self._bp.SALU_flag = 0
        elif command == "RBARREL":
            # See not about bitarray shift operators above
            bottom_bit = self._bp.A_bus.value[0]
            tmp = self._bp.A_bus.value << 1
            tmp[self.n_bits-1] = bottom_bit
            self._bp.C_bus.value = tmp
            self._bp.SALU_flag = 0
        elif command == "LSHIFT0":
            # See note about bitarray shift operators above
            dropped_bit = self._bp.A_bus.value[self.n_bits-1]
            self._bp.C_bus.value = self._bp.A_bus.value >> 1
            self._bp.SALU_flag = dropped_bit
        elif command == "LSHIFT1":
            # See note about bitarray shift operators above
            dropped_bit = self._bp.A_bus.value[self.n_bits-1]
            tmp = self._bp.A_bus.value >> 1
            tmp[0] = 1
            self._bp.C_bus.value = tmp
            self._bp.SALU_flag = dropped_bit
        elif command == "RSHIFT0":
            # See note about bitarray shift operators above
            dropped_bit = self._bp.A_bus.value[0]
            self._bp.C_bus.value = self._bp.A_bus.value << 1
            self._bp.SALU_flag = dropped_bit
        elif command == "RSHIFT1":
            # See note about bitarray shift operators above
            dropped_bit = self._bp.A_bus.value[0]
            tmp = self._bp.A_bus.value << 1
            tmp[self.n_bits-1] = 1
            self._bp.C_bus.value = tmp
            self._bp.SALU_flag = dropped_bit
        else:
            raise ValueError(f"SALU not recogised {command}")