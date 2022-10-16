import argparse
import logging

from slothpu import assemble_lines

_logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


def build_argument_parser():
    desc = "Assembler for SlothPU"

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "--assembler-file",
        help="The file containing the assembly code",
        required=True,
    )
    parser.add_argument(
        "--output-file",
        help="The file containing the encoded output",
        required=True,
    )

    return parser


def main():
    parser = build_argument_parser()
    args = parser.parse_args()

    _logger.info(f"Parsing: {args.assembler_file}")

    # Read in the file
    with open(args.assembler_file) as f_assembler:
        raw_lines = f_assembler.readlines()
    lines = [line.strip() for line in raw_lines]
    _logger.info(f"Found {len(lines)} lines")

    # List to hold the result
    machine_code = assemble_lines(lines)

    _logger.info(f"Writing {args.output_file}")
    with open(args.output_file, "w") as of:
        for c in machine_code:
            of.write(f"{c}\n")
    _logger.info("File written")


if __name__ == "__main__":
    main()
