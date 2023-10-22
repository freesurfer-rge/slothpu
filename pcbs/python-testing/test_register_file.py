from typing import List

import bitarray.util
import pytest

from register_file_connector_board import RegisterFileConnectorBoard

# Have discovered a mistake: the board has the regisers update on
# Execute, when it should be happening on Commit

class TestSmoke:
    def test_smoke(self):
        rfcb = RegisterFileConnectorBoard()

        expected = []
        for reg in range(8):
            rfcb.Phase("Other")
            rfcb.R_A(reg)
            rfcb.R_B(reg)
            rfcb.R_C(reg)
            rfcb.C_write_read(True)
            nxt_val = 2**(1+reg) - 1
            rfcb.C_bus_write(nxt_val)
            expected.append(nxt_val)
            rfcb.Phase("Decode")
            rfcb.send()
            rfcb.Phase("Execute")
            rfcb.send()
            rfcb.Phase("Commit")
            rfcb.send()
            rfcb.Phase("Other")
            rfcb.send()

        # Now do some reading
        for reg in range(8):
            rfcb.Phase("Other")
            rfcb.C_write_read(False)
            rfcb.R_A(reg)
            rfcb.R_B(reg)
            rfcb.R_C(reg)
            rfcb.send()
            rfcb.recv()
            assert rfcb.A_bus() == 0
            assert rfcb.B_bus() == 0
            assert rfcb.C_bus_read() == 0

        output_phases = ["Decode", "Execute", "Commit", "PCUpdate"]
        for phase in output_phases:
            for reg in range(8):
                rfcb.Phase(phase)
                rfcb.C_write_read(False)
                rfcb.R_A(reg)
                rfcb.R_B(reg)
                rfcb.R_C(reg)
                rfcb.send()
                rfcb.recv()
                assert rfcb.A_bus() == expected[reg]
                assert rfcb.B_bus() == expected[reg]
                assert rfcb.C_bus_read() == expected[reg]
