from typing import List

import bitarray.util
import pytest

from alu_connector_board import ALUConnectorBoard

# Rev1 board has decoder outputs backwards
instructions_rev1 = dict(
    ADD=[True, True, True, False],
    SUB=[False, True, True, False],
    OR=[True, True, False, False],
    XOR=[False, True, False, False],
    AND=[
        True,
        False,
        False,
        False,
    ],
    NAND=[False, False, False, False],
)

input_decoder_rev1 = dict(
    ADD=29,
    SUB=28,
    OR=27,
    XOR=26,
    AND=25,
    NAND=24,
    FLAG=9,
    RESULT=[1, 2, 3, 4, 5, 6, 7, 8],
)

instructions = instructions_rev1
input_decoder = input_decoder_rev1

# =======================================


test_values = [
    0,
    1,
    2,
    3,
    4,
    8,
    16,
    31,
    32,
    33,
    64,
    127,
    128,
    129,
    250,
    251,
    252,
    253,
    254,
    255,
]


def result_from_input(input_pins: List[bool]):
    assert len(input_pins) == 30

    result_bits = []
    for p in input_decoder["RESULT"]:
        result_bits.append(input_pins[p])

    value = bitarray.util.ba2int(bitarray.bitarray(result_bits, endian="little"))
    return value


class TestDecoder:
    @pytest.mark.parametrize(
        "current_instruction", ["ADD", "SUB", "OR", "XOR", "AND", "NAND"]
    )
    def test_instruction_decode(self, current_instruction):
        acb = ALUConnectorBoard()

        # On initialisation, all selectors should be high
        acb.recv()
        inputs = acb.Inputs()
        for k, v in input_decoder.items():
            if k in instructions.keys():
                assert inputs[v], f"Checking {k}"

        # Now set an instruction
        acb.Instruction(instructions[current_instruction])
        acb.send()

        # However, nothing should have changed yet
        acb.recv()
        inputs = acb.Inputs()
        for k, v in input_decoder.items():
            if k in instructions.keys():
                assert inputs[v], f"Checking {k}"

        # Now set select
        acb.Select(False)
        acb.send()

        # We should be able to detect the instruction
        acb.recv()
        inputs = acb.Inputs()
        for k, v in input_decoder.items():
            if k in instructions.keys():
                assert inputs[v] == (k != current_instruction), f"Checking {k}"

        # And deselect again
        acb.Select(True)
        acb.send()

        acb.recv()
        inputs = acb.Inputs()
        for k, v in input_decoder.items():
            if k in instructions.keys():
                assert inputs[v], f"Checking {k}"


class TestBitwiseOperations:
    def compute_expected(self, A: int, B: int, operation: str):
        assert A >= 0 and A < 256
        assert B >= 0 and B < 256
        if operation == "AND":
            result = A & B
        elif operation == "NAND":
            result = ~(A & B)
        else:
            raise ValueError(f"Unrecognised operation: {operation}")
        if result < 0:
            result = result + 256
        return result

    @pytest.mark.parametrize("operation", ["AND", "NAND"])
    def test_smoke(self, operation):
        acb = ALUConnectorBoard()

        A_val = 6
        B_val = 130
        C_expected = self.compute_expected(A_val, B_val, operation)

        acb.A(A_val)
        acb.B(B_val)
        acb.Instruction(instructions[operation])
        acb.Select(False)
        acb.Phase("Decode")

        acb.send()

        acb.recv()
        inputs = acb.Inputs()
        assert not inputs[input_decoder["FLAG"]]
        result = result_from_input(inputs)
        assert result == C_expected

        acb.Phase("Execute")
        acb.send()
        acb.recv()
        inputs = acb.Inputs()
        assert not inputs[input_decoder["FLAG"]]
        result = result_from_input(inputs)
        assert result == C_expected
        assert acb.C() == C_expected
        assert not acb.ALU_Flag()

        acb.Phase("Commit")
        acb.send()
        acb.recv()
        assert acb.C() == C_expected
        assert not acb.ALU_Flag()

    @pytest.mark.parametrize("A", test_values)
    @pytest.mark.parametrize("B", test_values)
    @pytest.mark.parametrize("operation", ["AND", "NAND"])
    def test_specific_values(self, A, B, operation):
        acb = ALUConnectorBoard()

        expected_C = self.compute_expected(A, B, operation)

        # Initally, C should be zero since the select
        # line will be high
        acb.recv()
        assert acb.C() == 0

        # Now send the inputs, select the instruction
        # enable the DALU and set to decode
        acb.A(A)
        acb.B(B)
        acb.Instruction(instructions[operation])
        acb.Select(False)
        acb.Phase("Decode")
        acb.send()

        # Retrieve the internal state
        acb.recv()
        inputs = acb.Inputs()
        assert not inputs[input_decoder["FLAG"]]
        result = result_from_input(inputs)
        assert result == expected_C

        # Go to the execute phase
        acb.Phase("Execute")
        acb.send()

        # Check that answer is now externally visible
        acb.recv()
        assert acb.C() == expected_C
        assert not acb.ALU_Flag(), "Check ALU_flag cleared"

        # Go to the commit phase
        acb.Phase("Commit")
        acb.send()

        # Check that the answer is still available
        acb.recv()
        assert acb.C() == expected_C
        assert not acb.ALU_Flag(), "Check ALU_flag cleared"
