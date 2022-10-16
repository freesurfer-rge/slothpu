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
    machine_code = assemble_lines(program_string.split('\n'))

    target = SlothPU(machine_code)

    # Run first instruction
    target.advance_instruction()
    assert bitarray.util.ba2int(target.register_file.registers[0]) == 0

    # Run second instruction
    target.advance_instruction()
    assert bitarray.util.ba2int(target.register_file.registers[1]) == 6