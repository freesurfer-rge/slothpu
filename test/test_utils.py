import bitarray.util

import slothpu._utils as spu

class TestAdder:
    def test_smoke(self):
        a = 78
        b = 123

        a_ba = bitarray.util.int2ba(a, length=8, endian='little')
        b_ba = bitarray.util.int2ba(b, length=8, endian='little')

        sum, carry = spu.bitarray_add(a_ba, b_ba, 0)

        assert (a+b) == bitarray.util.ba2int(sum)
        assert carry == 0