import bitarray.util

from slothpu import SlothPU, assemble_lines


def test_increment_r0():
    program_string = """
# Incrementer
# Sets R0 to 0, and then increments in an infinite loop

# Initialisation
0  REG SET000 R0  # The register we will increment
2  REG SET006  R1  # Low byte of address for infinite loop
4  REG SET000 R2  # High byte of address for infinite loop

# The loop
6 SALU INC R0 R0  # Should be able to store back safely
8 PC BRANCH R1 R2
    """
    machine_code = assemble_lines(program_string.split("\n"))

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
    program_string = """
# Sets memory location 30 to 0 and then
# increments by five in an infinite loop

# Initialise the target memory location
0  REG SET030 R1 # Target memory location
2  REG SET000 R0 # Having R0 always zero for convenience
4  MEM STORE R1 R0 R0 # Store a zero in memory location 20

# Initialise the increment value (in R2)
6 REG SET005 R2

8 REG SET010 R7 # Location of loop top
# The loop
10 MEM LOAD R1 R0 R3 # Load location 30 into R3
12 DALU ADD R2 R3 R4 # R4 <- R2 + R3
14 MEM STORE R1 R0 R4 # Save back to location 30
16 PC BRANCH R7 R0
    """
    machine_code = assemble_lines(program_string.split("\n"))
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
