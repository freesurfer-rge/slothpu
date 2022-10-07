import bitarray.util
import pytest

import slothpu._utils as spu


class TestAdder:
    def get_bas(self, a, b):
        a_ba = bitarray.util.int2ba(a, length=8, endian="little")
        b_ba = bitarray.util.int2ba(b, length=8, endian="little")

        return a_ba, b_ba

    def test_smoke(self):
        a = 78
        b = 123

        a_ba, b_ba = self.get_bas(a, b)

        sum_ba, carry = spu.bitarray_add(a_ba, b_ba, 0)

        assert (a + b) == bitarray.util.ba2int(sum_ba)
        assert carry == 0

    def test_overflow(self):
        a = 255
        b = 1

        a_ba, b_ba = self.get_bas(a, b)

        sum_ba, carry = spu.bitarray_add(a_ba, b_ba, 0)

        assert 0 == bitarray.util.ba2int(sum_ba)
        assert carry == 1

    def test_carry_in(self):
        a = 0
        b = 0

        a_ba, b_ba = self.get_bas(a, b)

        sum_ba, carry = spu.bitarray_add(a_ba, b_ba, 1)

        assert (a + b + 1) == bitarray.util.ba2int(sum_ba)
        assert carry == 0

    @pytest.mark.parametrize(
        ["a", "b", "carry"],
        [
            (0, 0, 0),
            (0, 0, 1),
            (1, 1, 0),
            (2, 2, 0),
            (3, 5, 0),
            (127, 1, 0),
            (128, 128, 1),
            (128, 255, 0),
            (255, 255, 1),
        ],
    )
    def test_many(self, a, b, carry):
        assert a < 256
        assert b < 256
        a_ba, b_ba = self.get_bas(a, b)

        sum_ba, carry_out = spu.bitarray_add(a_ba, b_ba, carry)
        expected_carry, expected_sum = divmod(a + b + carry, 256)
        assert expected_carry == 0 or expected_carry == 1

        assert expected_sum == bitarray.util.ba2int(sum_ba)
        assert expected_carry == carry_out

    def test_simple_subtract(self):
        a = 128
        b = 7
        a_ba, b_ba = self.get_bas(a, b)

        difference, borrow = spu.bitarray_add(a_ba, ~b_ba, 1)

        assert bitarray.util.ba2int(difference) == a - b
        assert borrow == 1  # We didn't borrow

    def test_simple_subtract_borrow(self):
        a = 9
        b = 128
        a_ba, b_ba = self.get_bas(a, b)

        difference, borrow = spu.bitarray_add(a_ba, ~b_ba, 1)

        assert bitarray.util.ba2int(difference) == (a - b) + 256
        assert borrow == 0  # We borrowed
