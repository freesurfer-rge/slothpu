import argparse
import logging

from typing import List

import bitarray
import bitarray.util

_logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)

comment_char = "#"
instruction_size = 16
max_register = 8


def build_argument_parser():
    desc = "Assembler for SlothPU"

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "--assembler-filename",
        help="The file containing the assembly code",
        required=True,
    )
    parser.add_argument(
        "--output-filename",
        help="The file containing the encoded output",
        required=True,
    )

    return parser


def empty_or_comment(line: str) -> bool:
    return len(line) == 0 or line.startswith(comment_char)


def parse_register_part(part: str) -> int:
    assert len(part) == 2
    assert part[0] == "R"
    reg_id = int(part[1])
    assert reg_id >= 0 and reg_id < max_register
    return reg_id


def generate_reg_ba(R_A: int, R_B: int, R_C: int) -> bitarray.bitarray:
    assert R_A >= 0 and R_A < max_register
    assert R_B >= 0 and R_B < max_register
    assert R_C >= 0 and R_C < max_register

    ba_A = bitarray.util.int2ba(R_A, 3, endian="little")
    ba_B = bitarray.util.int2ba(R_B, 3, endian="little")
    ba_C = bitarray.util.int2ba(R_C, 3, endian="little")

    return ba_A + ba_B + ba_C


def assemble_pc_instruction(parts: List[str]) -> bitarray.bitarray:
    assert parts[1] == "PC"
    operation = parts[2]

    instruction_ba = bitarray.util.zeros(instruction_size, endian="little")
    instruction_ba[0:3] = bitarray.bitarray("000", endian="little")

    R_A = 0
    R_B = 0
    R_C = 0
    if operation == "BRANCH":
        assert len(parts) == 5
        R_A = parse_register_part(parts[3])
        R_B = parse_register_part(parts[4])
        op_ba = bitarray.bitarray("0000", endian="little")
    else:
        raise ValueError(f"PC unrecognised operation: {operation}")

    assert len(op_ba) == 4
    assert op_ba.endian() == "little"

    instruction_ba[3:7] = op_ba
    instruction_ba[7:16] = generate_reg_ba(R_A, R_B, R_C)

    return instruction_ba


def assemble_reg_instruction(parts: List[str]) -> bitarray.bitarray:
    assert parts[1] == "REG"
    operation = parts[2]

    instruction_ba = bitarray.util.zeros(instruction_size, endian="little")
    instruction_ba[0:3] = bitarray.bitarray("010", endian="little")

    if operation.startswith("SET"):
        assert len(parts) == 4
        # We have a SET instruction
        instruction_ba[3:5] = bitarray.bitarray("00", endian="little")

        # Parse out the value to be set
        set_value = int(operation[3:6])
        assert set_value >= 0 and set_value < 256
        set_bits = bitarray.util.int2ba(set_value, 8, endian="little")
        instruction_ba[5:13] = set_bits

        R_C = parse_register_part(parts[3])
        instruction_ba[13:16] = bitarray.util.int2ba(R_C, 3, endian="little")
    else:
        raise ValueError(f"REG unrecognised operation: {operation}")

    return instruction_ba


def assemble_salu_instruction(parts: List[str]) -> bitarray.bitarray:
    assert parts[1] == "SALU"
    assert len(parts) == 5
    operation = parts[2]

    instruction_ba = bitarray.util.zeros(instruction_size, endian="little")
    instruction_ba[0:3] = bitarray.bitarray("001", endian="little")

    R_A = parse_register_part(parts[3])
    R_C = parse_register_part(parts[4])
    instruction_ba[7:16] = generate_reg_ba(R_A, 0, R_C)

    salu_instructions = {"INC": "0000", "DEC": "1000"}
    operation_ba = bitarray.bitarray(salu_instructions[operation], endian="little")
    assert len(operation_ba) == 4
    instruction_ba[3:7] = operation_ba

    return instruction_ba


def process_line(line: str, current_location: int) -> bitarray.bitarray:
    # Remove any trailing comments
    instruction_line = line.split(comment_char)[0]

    # Split into individual parts
    instruction_parts = instruction_line.split()

    current_loc = int(instruction_parts[0])
    if current_loc != current_location:
        raise ValueError(f"Out of order instruction: {instruction_parts}")
    # Determine the functional unit
    f_unit = instruction_parts[1]
    if f_unit == "PC":
        result = assemble_pc_instruction(instruction_parts)
    elif f_unit == "MEM":
        raise NotImplementedError("MEM instructions")
    elif f_unit == "REG":
        result = assemble_reg_instruction(instruction_parts)
    elif f_unit == "SALU":
        result = assemble_salu_instruction(instruction_parts)
    elif f_unit == "DALU":
        raise NotImplementedError("DALU instructions")
    else:
        raise ValueError(f"Bad instruction: {instruction_parts}")

    _logger.info(f"{result} : {instruction_parts}")
    return result


def main():
    parser = build_argument_parser()
    args = parser.parse_args()

    _logger.info(f"Parsing: {args.assembler_filename}")

    # Read in the file
    with open(args.assembler_filename) as assembler_file:
        raw_lines = assembler_file.readlines()
    lines = [line.strip() for line in raw_lines]
    _logger.info(f"Found {len(lines)} lines")

    # List to hold the result
    machine_code = []
    for line in lines:
        if empty_or_comment(line):
            continue

        nxt_instruction = process_line(line, len(machine_code))

        machine_code.append(bitarray.util.ba2int(nxt_instruction[0:8]))
        machine_code.append(bitarray.util.ba2int(nxt_instruction[8:16]))
    _logger.info("Assembly complete")

    _logger.info(f"Writing {args.output_filename}")
    with open(args.output_filename, "w") as of:
        for c in machine_code:
            of.write(f"{c}\n")
    _logger.info("File written")


if __name__ == "__main__":
    main()
