from typing import Tuple

import bitarray
import bitarray.util

from ._backplane import BackPlane
from ._utils import bitarray_add, to_01_bigendian


class ProgramCounter:
    def __init__(self, backplane: BackPlane):
        self._backplane = backplane
        self._n_bits = 2 * self._backplane.n_bits
        self._increment_enable = True
        self._pc = bitarray.util.zeros(self.n_bits, endian="little")
        self._jr = bitarray.util.zeros(self.n_bits, endian="little")

    @property
    def pc(self) -> bitarray.bitarray:
        assert len(self._pc) == self.n_bits
        assert self._pc.endian() == "little"
        assert self._pc[0] == 0, "PC must be even"
        return self._pc

    @property
    def jr(self) -> bitarray.bitarray:
        assert len(self._jr) == self.n_bits
        assert self._jr.endian() == "little"
        assert self._jr[0] == 0, "JR must be even"
        return self._jr

    @property
    def n_bits(self) -> int:
        return self._n_bits

    @property
    def increment_enable(self) -> bool:
        return self._increment_enable

    def get_pc_as_string(self) -> str:
        bin_str = to_01_bigendian(self.pc)
        dec_str = f"{bitarray.util.ba2int(self.pc):05}"
        return f"{bin_str} ({dec_str})"

    def get_jr_as_string(self) -> str:
        return to_01_bigendian(self.jr)

    def _set_pc(self, value: bitarray.bitarray):
        assert isinstance(value, bitarray.bitarray)
        assert len(value) == self.n_bits
        assert value.endian() == "little"
        assert value[0] == 0, "Must set PC to be even"
        # Make sure we copy
        self._pc = bitarray.bitarray(value)

    def _set_jr(self, value: bitarray.bitarray):
        assert isinstance(value, bitarray.bitarray)
        assert len(value) == self.n_bits
        assert value.endian() == "little"
        assert value[0] == 0, "Must set PC to be even"
        # Make sure we copy
        self._jr = bitarray.bitarray(value)

    def increment(self):
        step = bitarray.util.int2ba(2, length=self.n_bits, endian="little")
        self.add_pc(step)

    def add_pc(self, step: bitarray.bitarray):
        assert isinstance(step, bitarray.bitarray)
        assert len(step) == self.n_bits
        assert step.endian() == "little"
        assert step[0] == 0, "Must set PC to be even"
        self._pc, _ = bitarray_add(self.pc, step, carry_in=0)

    def subtract_pc(self, step: bitarray.bitarray):
        assert isinstance(step, bitarray.bitarray)
        assert len(step) == self.n_bits
        assert step.endian() == "little"
        assert step[0] == 0, "Must set PC to be even"

        self._pc, _ = bitarray_add(self.pc, ~step, carry_in=1)

    def fetch0(self):
        # Put current address onto A_bus and B_bus
        self._backplane.A_bus.value = self._pc[0:8]
        self._backplane.B_bus.value = self._pc[8:16]
        # Also ensure that increment is enabled
        self._increment_enable = True

    def fetch1(self):
        # Put current address+1 onto A_bus and B_bus
        one = bitarray.util.int2ba(1, length=self._backplane.n_bits, endian="little")
        self._backplane.A_bus.value = self._pc[0:8] | one
        self._backplane.B_bus.value = self._pc[8:16]

    def decode(self, instruction: bitarray.bitarray) -> Tuple[str, str]:
        assert instruction.endian() == "little"
        assert len(instruction) == self.n_bits

        commit_target = "PC"

        operations = {
            0: "JUMP",
            1: "JUMPZERO",
            2: "STOREJUMP",
            3: "JSR",
            4: "RET",
            8: "LOADJUMP0",
            9: "LOADJUMP1",
            12: "BRANCH",
            14: "BRANCHBACK",
        }

        op_ba = instruction[3:7]
        op = operations[bitarray.util.ba2int(op_ba)]

        return op, commit_target

    def execute(self, command: str):
        if command == "BRANCH":
            pass
        elif command == "BRANCHZERO":
            pass
        elif command == "BRANCHBACK":
            pass
        elif command == "BRANCHBACKZERO":
            pass
        elif command == "JUMP":
            pass
        elif command == "JUMPZERO":
            pass
        elif command == "STOREJUMP":
            pass
        elif command == "JSR":
            self._set_jr(self.pc)
        elif command == "RET":
            pass
        elif command == "LOADJUMP0":
            self._backplane.C_bus.value = self._jr[0:8]
        elif command == "LOADJUMP1":
            self._backplane.C_bus.value = self._jr[8:16]
        else:
            raise ValueError(f"PC Execute Unrecognised: {command}")

    def commit(self, command: str):
        jump_address = self._backplane.A_bus.value + self._backplane.B_bus.value
        if command == "BRANCH":
            pass
        elif command == "BRANCHZERO":
            pass
        elif command == "BRANCHBACK":
            pass
        elif command == "BRANCHBACKZERO":
            pass
        elif command == "JUMP":
            # Copy....
            self._set_pc(jump_address)
            self._increment_enable = False
        elif command == "JUMPZERO":
            target = jump_address
            if bitarray.util.ba2int(self._backplane.C_bus.value) == 0:
                self._set_pc(target)
                self._increment_enable = False
        elif command == "STOREJUMP":
            self._set_jr(jump_address)
        elif command == "JSR":
            self._set_pc(jump_address)
            self._increment_enable = False
        elif command == "RET":
            self._set_pc(self.jr)
            self._increment_enable = True
        elif command == "LOADJUMP0":
            pass
        elif command == "LOADJUMP1":
            pass
        else:
            raise ValueError(f"PC Commit Unrecognised: {command}")

    def updatepc(self, command: str):
        branch_commands = ["BRANCH", "BRANCHZERO", "BRANCHBACK", "BRANCHBACKZERO"]
        # Pad A bus up to 16 bits
        padded_A = self._backplane.A_bus.value + bitarray.util.zeros(
            self._backplane.n_bits, endian="little"
        )

        if self.increment_enable:
            if command not in branch_commands:
                self.increment()
            elif command == "BRANCH":
                self.add_pc(padded_A)
            elif command == "BRANCHZERO":
                if bitarray.util.ba2int(self._backplane.B_bus.value) == 0:
                    self.add_pc(padded_A)
                else:
                    self.increment()
            elif command == "BRANCHBACK":
                self.subtract_pc(padded_A)
            elif command == "BRANCHBACKZERO":
                if bitarray.util.ba2int(self._backplane.B_bus.value) == 0:
                    self.subtract_pc(padded_A)
                else:
                    self.increment()
        else:
            # Only JUMP, JUMPZERO and JSR can inhibit incrementing
            valid_commands = ["JUMP", "JUMPZERO", "JSR"]
            assert command in valid_commands
