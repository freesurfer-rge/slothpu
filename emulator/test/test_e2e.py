import enum
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

    # Should end about to execute the branch again
    assert bitarray.util.ba2int(target.program_counter.pc) == 8
