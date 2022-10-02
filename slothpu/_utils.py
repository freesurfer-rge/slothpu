from typing import Tuple

import bitarray
import bitarray.util


def to_01_bigendian(ba: bitarray.bitarray):
    assert ba.endian() == "little"
    return ba.to01()[::-1]

def half_adder(a: int, b: int) -> Tuple[int, int]:
    assert a==0 or a==1
    assert b==0 or b==1

    sum = a ^ b
    carry = a & b

    return sum, carry


def bitarray_add(a: bitarray.bitarray, b: bitarray.bitarray, carry_in: int) -> Tuple[bitarray.bitarray, int]:
    assert carry_in==0 or carry_in==1
    assert len(a) == len(b)
    assert a.endian()=='little'
    assert b.endian()=='little'

    result = bitarray.util.zeros(len(a), endian='little')
    nxt_carry = carry_in
    for i in range(len(a)):
        a_n = a[i]
        b_n = b[i]

        s_0, c_0 = half_adder(a_n, b_n)
        s_1, c_1 = half_adder(s_0, nxt_carry)

        result[i] = s_1
        nxt_carry = c_0 | c_1
    
    return result, nxt_carry
