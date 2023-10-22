from typing import List

import bitarray.util
import pytest

from register_file_connector_board import RegisterFileConnectorBoard

# Have discovered a mistake: the board has the regisers update on
# Execute, when it should be happening on Commit


class TestRegisterFile:
    def test_smoke(self):
        rfcb = RegisterFileConnectorBoard()

        expected = []
        for reg in range(8):
            rfcb.Phase("Other")
            rfcb.R_A(reg)
            rfcb.R_B(reg)
            rfcb.R_C(reg)
            rfcb.C_write_read(True)
            nxt_val = 2 ** (1 + reg) - 1
            rfcb.C_bus_write(nxt_val)
            expected.append(nxt_val)
            rfcb.Phase("Decode")
            rfcb.send()
            # Bug on board, we write on Execute :-/
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

        rfcb.Phase("Other")
        rfcb.send()

    @pytest.mark.parametrize("target_register", range(8))
    @pytest.mark.parametrize(
        "target_value", [0, 1, 2, 63, 64, 65, 93, 101, 127, 128, 129, 180, 254, 255]
    )
    def test_target_register(self, target_register: int, target_value: int):
        rfcb = RegisterFileConnectorBoard()

        expected = []
        for reg in range(8):
            rfcb.Phase("Other")
            rfcb.R_C(reg)
            rfcb.C_write_read(True)
            nxt_val = 2 ** (1 + reg) - 1
            rfcb.C_bus_write(nxt_val)
            expected.append(nxt_val)
            # Bug on board, we write on Execute :-/
            rfcb.Phase("Execute")
            rfcb.send()
            rfcb.Phase("Other")
            rfcb.send()

        # Prepare the answer for C_bus
        rfcb.C_bus_write(target_value)
        rfcb.R_C(target_register)

        # Check before
        for r_a in range(8):
            for r_b in range(8):
                rfcb.Phase("Other")
                rfcb.R_A(r_a)
                rfcb.R_B(r_b)
                rfcb.send()
                rfcb.recv()
                assert rfcb.A_bus() == 0
                assert rfcb.B_bus() == 0

        check_phases = ["Decode", "Execute", "Commit", "PCUpdate"]
        for phase in check_phases:
            # Update the expected value of our target register
            # It _should_ be Execute, not Commit, but for board bug
            if phase == "Execute":
                expected[target_register] = target_value
            # Check we can read all expected combinations
            for r_a in range(8):
                for r_b in range(8):
                    rfcb.Phase(phase)
                    rfcb.R_A(r_a)
                    rfcb.R_B(r_b)
                    rfcb.send()
                    rfcb.recv()
                    assert rfcb.A_bus() == expected[r_a]
                    assert rfcb.B_bus() == expected[r_b]

        rfcb.Phase("Other")
        rfcb.send()

    @pytest.mark.parametrize("target_register", range(8))
    @pytest.mark.parametrize(
        "target_value", [0, 1, 2, 63, 64, 65, 93, 101, 127, 128, 129, 180, 254, 255]
    )
    def test_target_register_all_read(self, target_register: int, target_value: int):
        rfcb = RegisterFileConnectorBoard()

        expected = []
        for reg in range(8):
            rfcb.Phase("Other")
            rfcb.R_C(reg)
            rfcb.C_write_read(True)
            if reg == target_register:
                nxt_val = target_value
            else:
                nxt_val = 2 ** (1 + reg) - 1
            rfcb.C_bus_write(nxt_val)
            expected.append(nxt_val)
            # Bug on board, we write on Execute :-/
            rfcb.Phase("Execute")
            rfcb.send()
            rfcb.Phase("Other")
            rfcb.send()

        for r_a in range(8):
            for r_b in range(8):
                for r_c in range(8):
                    rfcb.Phase("Other")
                    rfcb.C_write_read(False)
                    rfcb.R_A(r_a)
                    rfcb.R_B(r_b)
                    rfcb.R_C(r_c)
                    rfcb.send()
                    rfcb.recv()
                    assert rfcb.A_bus() == 0
                    assert rfcb.B_bus() == 0
                    assert rfcb.C_bus_read() == 0

        check_phases = ["Decode", "Execute", "Commit", "PCUpdate"]
        for phase in check_phases:
            for r_a in range(8):
                for r_b in range(8):
                    for r_c in range(8):
                        rfcb.Phase(phase)
                        rfcb.R_A(r_a)
                        rfcb.R_B(r_b)
                        rfcb.R_C(r_c)
                        rfcb.send()
                        rfcb.recv()
                        assert rfcb.A_bus() == expected[r_a]
                        assert rfcb.B_bus() == expected[r_b]
                        assert rfcb.C_bus_read() == expected[r_c]

        rfcb.Phase("Other")
        rfcb.send()
