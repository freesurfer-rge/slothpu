from typing import List

import bitarray
import bitarray.util
import pytest

from alu_connector_board import ALUConnectorBoard


instructions_rev1 = dict(
    INC=[False, False, False, False],
    DEC=[True, False, False, False],
    NOT=[False, True, False, False],
    COPY=[True, True, False, False],
    LBARREL=[False, False, False, True],
    RBARREL=[True, False, False, True],
    LSHIFT0=[False, False, True, True],
    LSHIFT1=[True, False, True, True],
    RSHIFT0=[False, True, True, True],
    RSHIFT1=[True, True, True, True],
)

instructions = instructions_rev1


class TestOperations:
    # Used to figure out the expected output
    def compute_expected(self, A: int, operation: str):
        assert A >= 0 and A < 256
        flag = False
        A_bits = bitarray.util.int2ba(A, 8, endian="little")

        flag = 0
        if operation == "INC":
            result = A + 1
            if result >= 256:
                result = result - 256
                flag = 1
        elif operation == "DEC":
            result = A - 1
            if result < 0:
                result = result + 256
                flag = 1
        elif operation == "NOT":
            result = bitarray.util.ba2int(~A_bits)
        elif operation == "COPY":
            result = A
        elif operation == "LBARREL":
            result = A << 1
            top_bit, result = divmod(result, 256)
            assert top_bit == 0 or top_bit == 1
            result = result + top_bit
        elif operation == "RBARREL":
            result, bottom_bit = divmod(A, 2)
            result = result + (bottom_bit * 128)
        elif operation == "LSHIFT0":
            result = A << 1
            dropped_bit, result = divmod(result, 256)
            assert dropped_bit == 0 or dropped_bit == 1
            flag = dropped_bit
        elif operation == "LSHIFT1":
            result = A << 1
            result = result + 1
            dropped_bit, result = divmod(result, 256)
            assert dropped_bit == 0 or dropped_bit == 1
            flag = dropped_bit
        elif operation == "RSHIFT0":
            result, dropped_bit = divmod(A, 2)
            assert dropped_bit == 0 or dropped_bit == 1
            flag = dropped_bit
        elif operation == "RSHIFT1":
            result, dropped_bit = divmod(A, 2)
            result = result + 128
            assert dropped_bit == 0 or dropped_bit == 1
            flag = dropped_bit
        else:
            raise ValueError(f"Unrecognised operation: {operation}")

        return result, flag

    @pytest.mark.parametrize(
        "operation",
        [
            "INC",
            "DEC",
            "NOT",
            "COPY",
            "LBARREL",
            "RBARREL",
            "LSHIFT0",
            "LSHIFT1",
            "RSHIFT0",
            "RSHIFT1",
        ],
    )
    def test_smoke(self, operation):
        acb = ALUConnectorBoard()

        A_val = 6
        C_expected, flag_expected = self.compute_expected(A_val, operation)
        
        acb.A(A_val)
        acb.Instruction(instructions[operation])
        acb.Select(False)
        acb.Phase("Decode")

        acb.send()

        acb.recv()
        inputs = acb.Inputs()

        acb.Phase("Execute")
        acb.send()
        acb.recv()
        inputs = acb.Inputs()
        assert acb.C() == C_expected
        assert acb.ALU_Flag() == flag_expected

        acb.Phase("Commit")
        acb.send()
        acb.recv()
        assert acb.C() == C_expected
        assert acb.ALU_Flag() == flag_expected

        acb.Phase("Other")
        acb.send()
        acb.recv()
        assert acb.C() == 0
        assert acb.ALU_Flag() == flag_expected


    @pytest.mark.parametrize("A_val", range(256))
    @pytest.mark.parametrize(
        "operation",
        [
            "INC",
            "DEC",
            "NOT",
            "COPY",
            "LBARREL",
            "RBARREL",
            "LSHIFT0",
            "LSHIFT1",
            "RSHIFT0",
            "RSHIFT1",
        ],
    )
    def test_full(self, A_val, operation):
        acb = ALUConnectorBoard()

        C_expected, flag_expected = self.compute_expected(A_val, operation)

        acb.A(A_val)
        acb.Instruction(instructions[operation])
        acb.Select(False)
        acb.Phase("Decode")

        acb.send()

        acb.recv()
        inputs = acb.Inputs()

        acb.Phase("Execute")
        acb.send()
        acb.recv()
        inputs = acb.Inputs()
        assert acb.C() == C_expected
        assert acb.ALU_Flag() == flag_expected

        acb.Phase("Commit")
        acb.send()
        acb.recv()
        assert acb.C() == C_expected
        assert acb.ALU_Flag() == flag_expected

        acb.Phase("Other")
        acb.send()
        acb.recv()
        assert acb.C() == 0
        assert acb.ALU_Flag() == flag_expected
