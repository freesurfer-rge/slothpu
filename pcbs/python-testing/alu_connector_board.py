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
        self.recv()

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

    @property
    def Input_Pins(self) -> Dict[str, Union[int, List[int]]]:
        ip = dict(
            C_bus=[0, 1, 2, 3, 4, 5, 6, 7],
            DALU_Flag=8,
            In=[
                19,
                18,
                17,
                16,
                15,
                14,
                12,
                13,
                10,
                11,  # End of Set 0
                29,
                28,
                27,
                26,
                25,
                24,
                22,
                23,
                20,
                21,  # End of Set 1
                39,
                38,
                37,
                36,
                35,
                34,
                32,
                33,
                30,
                31,  # End of Set 2
            ],
        )
        return ip

    def recv(self):
        self._inputs = self._tb.recv()

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

    def Instruction(self, instructions: List[bool]):
        assert len(instructions) == 4

        for i in range(len(instructions)):
            self._outputs[self.Output_Pins["I"][i]] = instructions[i]

    def C(self) -> int:
        C_pins = self.Input_Pins["C_bus"]
        C_vals = []
        for p in C_pins:
            C_vals.append(self._inputs[p])

        value = bitarray.util.ba2int(bitarray.bitarray(C_vals, endian="little"))
        return value

    def DALU_Flag(self) -> bool:
        return self._inputs[self.Input_Pins["DALU_Flag"]]

    def Inputs(self) -> List[int]:
        result = []
        for p in self.Input_Pins["In"]:
            result.append(self._inputs[p])
        assert len(result) == 30
        return result
