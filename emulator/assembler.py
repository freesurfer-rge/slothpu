import argparse
import logging

_logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)



def build_argument_parser():
    desc = "Assembler for SlothPU"

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "--assembler-filename",
        help="The file containing the assembly code",
        required=True,
    )

    return parser



def main():
    parser = build_argument_parser()
    args = parser.parse_args()

    _logger.info(f"Parsing: {args.assembler_filename}")

if __name__ == "__main__":
    main()