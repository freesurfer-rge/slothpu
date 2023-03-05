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
)

instructions = instructions_rev1
input_decoder = input_decoder_rev1


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
            assert inputs[v], f"Checking {k}"

        # Now set an instruction
        acb.Instruction(instructions[current_instruction])
        acb.send()

        # However, nothing should have changed yet
        acb.recv()
        inputs = acb.Inputs()
        for k, v in input_decoder.items():
            assert inputs[v], f"Checking {k}"

        # Now set select
        acb.Select(False)
        acb.send()

        # We should be able to detect the instruction
        acb.recv()
        inputs = acb.Inputs()
        for k, v in input_decoder.items():
            assert inputs[v] == (k != current_instruction), f"Checking {k}"

        # And deselect again
        acb.Select(True)
        acb.send()

        acb.recv()
        inputs = acb.Inputs()
        for k, v in input_decoder.items():
            assert inputs[v], f"Checking {k}"
