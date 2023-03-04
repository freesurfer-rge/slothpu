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

    def A(self, value: int):
        assert isinstance(value, int)
        assert value > 0
        assert value < 256

        converted = bitarray.util.int2ba(value, length=8, endian="little")
        for i in range(8):
            self._outputs[self.Output_Pins["A_bus"][i]] = converted[i]
