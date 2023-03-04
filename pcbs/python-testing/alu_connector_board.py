from typing import Dict, List, Union

import bitarray.util

from tester_board import TesterBoard


class ALUConnectorBoard:
    def __init__(self):
        """Initialise with an internal TesterBoard."""
        self._tb = TesterBoard()

        # Enable all outputs
        self._tb.enable_outputs([True for _ in range(5)])

        # Set up the outputs; only have the Select line high
        # (recall select is active-low)
        self._outputs = [False for _ in range(self._tb.n_pins)]
        self._outputs[self.Output_Pins["Select"]] = True
        self.send()

        # Read in the inputs
        self._inputs = self._tb.recv()

    @property
    def Output_Pins(self) -> Dict[str, Union[int, List[int]]]:
        op = dict(
            A_bus=[31, 29, 27, 25, 23, 21, 19, 17],
            B_bus=[15, 13, 11, 9, 7, 5, 3, 1],
            I=[33, 35, 37, 39],
            Commit=32,
            Execute=34,
            Decode=36,
            Select=38,
        )
        return op

    def send(self):
        self._tb.send(self._outputs)

    def _set_output_bus(self, value: int, bus_name: str):
        assert isinstance(value, int)
        assert value >= 0
        assert value < 256

        converted = bitarray.util.int2ba(value, length=8, endian="little")
        for i in range(8):
            self._outputs[self.Output_Pins[bus_name][i]] = converted[i]

    def A(self, value: int):
        self._set_output_bus(value, "A_bus")

    def B(self, value: int):
        self._set_output_bus(value, "B_bus")

    def Select(self, value: bool):
        self._outputs[self.Output_Pins["Select"]] = value

    def Phase(self, phase: str):
        pins = dict(Commit=False, Execute=False, Decode=False)
        if phase == "Other":
            pass
        elif phase == "Decode":
            pins["Decode"] = True
        elif phase == "Execute":
            pins["Execute"] = True
        elif phase == "Commit":
            pins["Commit"] = True
        else:
            raise ValueError(f"Bad phase: {phase}")

        # Set the output pins
        for k, v in pins.items():
            self._outputs[self.Output_Pins[k]] = v

    def Instruction(self, instr: str):
        if instr == "ADD":
            pins = [False, False, False, False]
        elif instr == "SUB":
            pins = [True, False, False, False]
        elif instr == "OR":
            pins = [False, False, True, False]
        elif instr == "XOR":
            pins = [True, False, True, False]
        elif instr == "AND":
            pins = [False, True, True, False]
        elif instr == "NAND":
            pins = [True, True, True, False]
        else:
            raise ValueError(f"Bad instruction: {instr}")
        assert len(pins) == 4

        for i in range(len(pins)):
            self._outputs[self.Output_Pins["I"][i]] = pins[i]
