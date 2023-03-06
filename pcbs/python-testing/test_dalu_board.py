from time import sleep
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

a_b_pairs = [
    (0, 0),
    (1, 0),
    (0, 1),
    (128, 128),
    (255, 1),
    (1, 255),
    (137, 2),
    (101, 13),
    (7, 240),
    (8, 240),
    (240, 8),
    (255, 255),
]

def result_from_input(input: List[bool]):
    assert len(input) == 30

    result_bits = []
    for p in input_decoder["RESULT"]:
        result_bits.append(input[p])

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


class TestAND:
    def test_smoke(self):
        acb = ALUConnectorBoard()

        A_val = 6
        B_val = 130

        acb.A(A_val)
        acb.B(B_val)
        acb.Instruction(instructions["AND"])
        acb.Select(False)
        acb.Phase("Decode")

        acb.send()

        acb.recv()
        inputs = acb.Inputs()
        assert inputs[input_decoder["FLAG"]] == False
        result = result_from_input(inputs)
        assert result == A_val & B_val


        acb.Phase("Execute")
        acb.send()
        acb.recv()
        inputs = acb.Inputs()
        assert inputs[input_decoder["FLAG"]] == False
        result = result_from_input(inputs)
        assert result == A_val & B_val
        assert acb.C() == A_val & B_val
        assert acb.ALU_Flag() == False

        acb.Phase("Commit")
        acb.send()
        acb.recv()
        assert acb.C() == A_val & B_val
        assert acb.ALU_Flag() == False

    @pytest.mark.parametrize(["A", "B"], a_b_pairs)
    def test_specific_values(self, A, B):
        acb = ALUConnectorBoard()

        expected_C = A & B
        
        # Initally, C should be zero since the select
        # line will be high
        acb.recv()
        assert acb.C() == 0

        # Now send the inputs, select the instruction
        # enable the DALU and set to decode
        acb.A(A)
        acb.B(B)
        acb.Instruction(instructions["AND"])
        acb.Select(False)
        acb.Phase("Decode")
        acb.send()

        # Retrieve the internal state
        acb.recv()
        inputs = acb.Inputs()
        assert inputs[input_decoder["FLAG"]] == False
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
