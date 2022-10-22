import os

from typing import List

import bitarray.util
import pytest

from slothpu import SlothPU, assemble_lines


a_b_pairs = [
    (0, 0),
    (1, 0),
    (0, 1),
    (255, 1),
    (1, 255),
    (255, 2),
    (2, 255),
    (255, 255),
    (0, 256),
    (1, 256),
    (2, 256),
    (256, 0),
    (256, 1),
    (256,2),
    (256, 256),
    (16384, 16385),
    (1, 65534),
    (65534, 1),
    (32768, 32767),
    (10542, 6583),
]


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

    # Should end about to execute the jump again
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


def test_count_by_five_branch():
    prog_lines = load_sample_program("count_by_five_branch.txt")
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
    # There's a jump zero about to go past
    assert (a_lo + b_lo) >= 256, "Sanity check for carry"

    while current_instruction < 70:
        target.advance_instruction()
        # 2 bytes per instruction
        current_instruction = current_instruction + 2
    # We should not have taken the jump, and hence
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


@pytest.mark.parametrize(["a", "b"], a_b_pairs)
def test_simple_two_byte_add_vals(a: int, b: int):
    prog_lines = load_sample_program("simple_two_byte_add.txt")

    assert a >= 0 and a < 2**16
    assert b >= 0 and b < 2**16
    assert a + b < 2**16
    # Calculate some bytes
    a_hi, a_lo = divmod(a, 256)
    b_hi, b_lo = divmod(b, 256)
    c_hi, c_lo = divmod(a + b, 256)

    # Doctor the prog_lines for A
    assert prog_lines[21] == "4 REG SET101 R0"
    prog_lines[21] = f"4 REG SET{a_lo:03} R0"
    assert prog_lines[23] == "8 REG SET001 R0"
    prog_lines[23] = f"8 REG SET{a_hi:03} R0"

    # And for B
    assert prog_lines[28] == "14 REG SET237 R0"
    prog_lines[28] = f"14 REG SET{b_lo:03} R0"
    assert prog_lines[31] == "20 REG SET004 R0"
    prog_lines[31] = f"20 REG SET{b_hi:03} R0"

    machine_code = assemble_lines(prog_lines)
    target = SlothPU(machine_code)

    # Run the program
    curr_instruction = 0
    while curr_instruction < 82:
        target.advance_instruction()
        curr_instruction = curr_instruction + 2

    # Check the result
    assert c_lo == bitarray.util.ba2int(target.main_memory.memory[260])
    assert c_hi == bitarray.util.ba2int(target.main_memory.memory[261])


def test_subroutine_two_byte_add():
    prog_lines = load_sample_program("subroutine_two_byte_add.txt")
    machine_code = assemble_lines(prog_lines)
    target = SlothPU(machine_code)

    for idx, ins in enumerate(machine_code):
        assert bitarray.util.ba2int(target.main_memory.memory[idx]) == ins

    a = 29753
    b = 9487
    a_hi, a_lo = divmod(a, 256)
    b_hi, b_lo = divmod(b, 256)
    c_hi, c_lo = divmod(a + b, 256)

    current_instruction = 0
    # Advance until we have stored A and B
    while current_instruction < 28:
        target.advance_instruction()
        # 2 bytes per instruction
        current_instruction = current_instruction + 2

    # Peer into the memory
    assert a_lo == bitarray.util.ba2int(target.main_memory.memory[160])
    assert a_hi == bitarray.util.ba2int(target.main_memory.memory[161])
    assert b_lo == bitarray.util.ba2int(target.main_memory.memory[162])
    assert b_hi == bitarray.util.ba2int(target.main_memory.memory[163])

    # Complete everything
    # Go to what should be a sufficiently high number
    while current_instruction < 200:
        target.advance_instruction()
        # 2 bytes per instruction
        current_instruction = current_instruction + 2

    assert c_lo == bitarray.util.ba2int(target.main_memory.memory[164])
    assert c_hi == bitarray.util.ba2int(target.main_memory.memory[165])


@pytest.mark.parametrize(["a", "b"], a_b_pairs)
def test_subroutine_two_byte_add_vals(a: int, b: int):
    prog_lines = load_sample_program("subroutine_two_byte_add.txt")

    assert a >= 0 and a < 2**16
    assert b >= 0 and b < 2**16
    assert a + b < 2**26
    # Calculate some bytes
    a_hi, a_lo = divmod(a, 256)
    b_hi, b_lo = divmod(b, 256)
    c_hi, c_lo = divmod(a + b, 256)

    # Doctor the prog_lines for A
    assert prog_lines[19] == "4 REG SET057 R2"
    prog_lines[19] = f"4 REG SET{a_lo:03} R2"
    assert prog_lines[22] == "10 REG SET116 R2"
    prog_lines[22] = f"10 REG SET{a_hi:03} R2"

    # And for B
    assert prog_lines[27] == "16 REG SET015 R2"
    prog_lines[27] = f"16 REG SET{b_lo:03} R2"
    assert prog_lines[30] == "22 REG SET037 R2"
    prog_lines[30] = f"22 REG SET{b_hi:03} R2"

    machine_code = assemble_lines(prog_lines)
    target = SlothPU(machine_code)

    # Run the program
    curr_instruction = 0
    while curr_instruction < 200:
        target.advance_instruction()
        curr_instruction = curr_instruction + 2

    # Check the result
    assert c_lo == bitarray.util.ba2int(target.main_memory.memory[164])
    assert c_hi == bitarray.util.ba2int(target.main_memory.memory[165])


@pytest.mark.parametrize(["a", "b"], a_b_pairs)
def test_subroutine_two_byte_add_branch_vals(a: int, b: int):
    prog_lines = load_sample_program("subroutine_two_byte_add_branch.txt")

    assert a >= 0 and a < 2**16
    assert b >= 0 and b < 2**16
    assert a + b < 2**26
    # Calculate some bytes
    a_hi, a_lo = divmod(a, 256)
    b_hi, b_lo = divmod(b, 256)
    c_hi, c_lo = divmod(a + b, 256)

    # Doctor the prog_lines for A
    assert prog_lines[19] == "4 REG SET057 R2"
    prog_lines[19] = f"4 REG SET{a_lo:03} R2"
    assert prog_lines[22] == "10 REG SET116 R2"
    prog_lines[22] = f"10 REG SET{a_hi:03} R2"

    # And for B
    assert prog_lines[27] == "16 REG SET015 R2"
    prog_lines[27] = f"16 REG SET{b_lo:03} R2"
    assert prog_lines[30] == "22 REG SET037 R2"
    prog_lines[30] = f"22 REG SET{b_hi:03} R2"

    machine_code = assemble_lines(prog_lines)
    target = SlothPU(machine_code)

    # Run the program
    curr_instruction = 0
    while curr_instruction < 200:
        target.advance_instruction()
        curr_instruction = curr_instruction + 2

    # Check the result
    assert c_lo == bitarray.util.ba2int(target.main_memory.memory[164])
    assert c_hi == bitarray.util.ba2int(target.main_memory.memory[165])
