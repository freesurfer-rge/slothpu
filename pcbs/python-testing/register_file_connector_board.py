from typing import Dict, List, Union

import bitarray.util

from tester_board import TesterBoard


class RegisterFileConnectorBoard:
    def __init__(self):
        """Initialise with an internal Testerboard."""
        self._tb = TesterBoard()

        # Start with all outputs disabled
        # This is safer since we read and write from C bus
        self._tb.enable_outputs([False for _ in range(5)])

        # Now set up the outputs
        # Most low, but set the 'C_write_read' pin high
        self._outputs = [False for _ in range(self._tb.n_pins)]
        self._outputs[self.Output_Pins["C_write_read"]] = True
        self.send()
        self._tb.enable_outputs([True for _ in range(5)])

        # Read in the inputs
        self.recv()

    @property
    def Output_Pins(self) -> Dict[str, Union[int, List[int]]]:
        op = dict(
            C_bus=[7, 6, 5, 4, 3, 2, 1, 0],
            C_write_read=9,
            R_A=[11, 13, 15],
            R_B=[17, 19, 21],
            R_C=[23, 25, 27],
            Commit=37,
            Execute=38,
            Decode=36,
            PCUpdate=39,
        )
        return op

    @property
    def Input_Pins(self) -> Dict[str, Union[int, List[int]]]:
        ip = dict(
            A_bus=[1, 3, 5, 7, 9, 11, 13, 15],
            B_bus=[17, 19, 21, 23, 25, 27, 29, 31],
            C_bus=[0, 2, 4, 6, 8, 10, 12, 14],
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


    def C_bus_write(self, value: int):
        self._set_output_bus(value, "C_bus")

    def C_write_read(self, value: bool):
        if value:
            # Going to write to C_bus, need to enable output
            self._tb.enable_output([True, True, True, True, True])
        else:
            # We're reading, so need to disable the output pins for
            # C_bus
            self._tb.enable_output([False, True, True, True, True])
        self._outputs[self.Output_Pins["C_write_read"]] = value


    def Phase(self, phase: str):
        pins = dict(Commit=False, Execute=False, Decode=False, PCUpdate=False)
        if phase == "Other":
            pass
        elif phase == "Decode":
            pins["Decode"] = True
        elif phase == "Execute":
            pins["Execute"] = True
        elif phase == "Commit":
            pins["Commit"] = True
        elif phase == "PCUpdate":
            pins["PCUpdate"] = True
        else:
            raise ValueError(f"Bad phase: {phase}")

        # Set the output pins
        for k, v in pins.items():
            self._outputs[self.Output_Pins[k]] = v


    def _read_input_bus(self, bus_name: str) -> int:
        target_pins = self.Input_Pins[bus_name]
        vals = []
        for p in target_pins:
            vals.append(self._inputs[p])

        value = bitarray.util.ba2int(bitarray.bitarray(vals, endian="little"))
        return value

    def A_bus(self) -> int:
        return self._read_input_bus("A_bus")

    def B_bus(self) -> int:
        return self._read_input_bus("B_bus")

    def C_bus_read(self) -> int:
        return self._read_input_bus("C_bus")

    
    def _select_register(register_name: str, id: int):
        assert isinstance(id, int)
        assert id>=0 and id <8

        converted = bitarray.util.int2ba(id, length=3, endian="little")
        for i in range(3):
            self._outputs[self.Output_pins[id][i]] = converted[i]
            
        

    def R_A(self, id: int):
        self._select_register("R_A", id)

    def R_B(self, id: int):
        self._select_register("R_B", id)

    def R_C(self, id:int):
        self._select_register("R_C", id)
