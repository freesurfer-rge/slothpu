import os

from typing import List

import bitarray.util

from slothpu import SlothPU, assemble_lines


def load_sample_program(prog_name: str) -> List[str]:
    prog_dir = "sample_programs"
    target_file = os.path.join(prog_dir, prog_name)

    with open(target_file, "r") as f_assembler:
        raw_lines = f_assembler.readlines()
    lines = [line.strip() for line in raw_lines]
    return lines


def test_increment_r0():
    prog_lines = load_sample_program("incrementer.txt")
    machine_code = assemble_lines(prog_lines)

    target = SlothPU(machine_code)

    for idx, ins in enumerate(machine_code):
        assert bitarray.util.ba2int(target.main_memory.memory[idx]) == ins

    # Run first instruction
    assert bitarray.util.ba2int(target.program_counter.pc) == 0
    target.advance_instruction()
    assert target.instruction_register.unit == "REG"
    assert target.instruction_register.R_C == 0
    assert target.instruction_register.operation == "SET000"
    assert bitarray.util.ba2int(target.register_file.registers[0]) == 0

    # Run second instruction
    assert bitarray.util.ba2int(target.program_counter.pc) == 2
    target.advance_instruction()
    assert target.instruction_register.unit == "REG"
    assert target.instruction_register.R_C == 1
    assert target.instruction_register.operation == "SET006"
    assert bitarray.util.ba2int(target.register_file.registers[1]) == 6

    # Run the third instruction
    target.advance_instruction()
    assert bitarray.util.ba2int(target.register_file.registers[2]) == 0

    # Run the fourth instruction
    target.advance_instruction()
    # R0 should have incremented
    assert bitarray.util.ba2int(target.register_file.registers[0]) == 1

    # Run two more instructions; should have incremented R0 again
    target.advance_instruction()
    target.advance_instruction()
    assert bitarray.util.ba2int(target.register_file.registers[0]) == 2

    # Run through the loop several more times
    nxt_value = 2
    for _ in range(1000):
        nxt_value = nxt_value + 1
        target.advance_instruction()
        target.advance_instruction()
        assert (
            bitarray.util.ba2int(target.register_file.registers[0]) == nxt_value % 256
        )
        assert target.backplane.SALU_flag == (nxt_value % 256 == 0)

    # Should end about to execute the branch again
    assert bitarray.util.ba2int(target.program_counter.pc) == 8


def test_count_by_five():
    prog_lines = load_sample_program("count_by_five.txt")
    machine_code = assemble_lines(prog_lines)
    target = SlothPU(machine_code)

    for idx, ins in enumerate(machine_code):
        assert bitarray.util.ba2int(target.main_memory.memory[idx]) == ins

    # Run the first three instructions
    target.advance_instruction()
    target.advance_instruction()
    target.advance_instruction()

    # Check memory location 30 is zero
    assert bitarray.util.ba2int(target.main_memory.memory[30]) == 0

    # Advance to the loop start
    target.advance_instruction()
    target.advance_instruction()

    expected = 0
    for _ in range(100):
        expected = expected + 5
        # Advance through loop body (4 instructions)
        target.advance_instruction()
        target.advance_instruction()
        target.advance_instruction()
        target.advance_instruction()
        assert bitarray.util.ba2int(target.main_memory.memory[30]) == expected % 256
        # Check for DALU flag on wrap
        assert target.backplane.DALU_flag == ((expected % 256) < 5)


def test_simple_two_byte_add():
    prog_lines = load_sample_program("simple_two_byte_add.txt")
    machine_code = assemble_lines(prog_lines)
    target = SlothPU(machine_code)

    for idx, ins in enumerate(machine_code):
        assert bitarray.util.ba2int(target.main_memory.memory[idx]) == ins

    a = 357
    b = 1261
    a_hi, a_lo = divmod(a, 256)
    b_hi, b_lo = divmod(b, 256)
    c_hi, c_lo = divmod(a + b, 256)

    current_instruction = 0
    # Advance until we have stored A and B
    while current_instruction < 26:
        target.advance_instruction()
        # 2 bytes per instruction
        current_instruction = current_instruction + 2

    # Peer into the memory
    assert a_lo == bitarray.util.ba2int(target.main_memory.memory[256])
    assert a_hi == bitarray.util.ba2int(target.main_memory.memory[257])
    assert b_lo == bitarray.util.ba2int(target.main_memory.memory[258])
    assert b_hi == bitarray.util.ba2int(target.main_memory.memory[259])

    # Advance until we've loaded the two low bytes into R1 and R2
    while current_instruction < 40:
        target.advance_instruction()
        # 2 bytes per instruction
        current_instruction = current_instruction + 2

    # Check that we've got the right low value
    assert a_lo == bitarray.util.ba2int(target.register_file.registers[1])
    assert b_lo == bitarray.util.ba2int(target.register_file.registers[2])

    # Check the low byte of the sum
    assert c_lo == bitarray.util.ba2int(target.register_file.registers[3])
    # Check the loaded status register
    # DALU bit is the second
    lo_carry = ((a_lo + b_lo) >= 256) * 2
    assert lo_carry == bitarray.util.ba2int(target.register_file.registers[4])

    # Advance until we've stored R3 into the low byte of the result
    while current_instruction < 46:
        target.advance_instruction()
        # 2 bytes per instruction
        current_instruction = current_instruction + 2

    assert c_lo == bitarray.util.ba2int(target.main_memory.memory[260])

    # Advance until we've added the high bytes
    while current_instruction < 62:
        target.advance_instruction()
        # 2 bytes per instruction
        current_instruction = current_instruction + 2

    # We haven't yet added on the carry from the low yet, so...
    assert a_hi == bitarray.util.ba2int(target.register_file.registers[1])
    assert b_hi == bitarray.util.ba2int(target.register_file.registers[2])
    assert (a_hi + b_hi) % 256 == bitarray.util.ba2int(
        target.register_file.registers[3]
    )

    # Now the advancing gets slightly difficult
    # There's a branch zero about to go past
    assert (a_lo + b_lo) >= 256, "Sanity check for carry"

    while current_instruction < 70:
        target.advance_instruction()
        # 2 bytes per instruction
        current_instruction = current_instruction + 2
    # We should not have taken the branch, and hence
    # we should have incremented R3
    assert (a_hi + b_hi + 1) % 256 == bitarray.util.ba2int(
        target.register_file.registers[3]
    )
    assert c_hi == a_hi + b_hi + 1

    # Advance to the end

    while current_instruction < 80:
        target.advance_instruction()
        # 2 bytes per instruction
        current_instruction = current_instruction + 2

    # Check the high byte of the final result (neglecting carry)
    assert c_hi == bitarray.util.ba2int(target.main_memory.memory[261])
