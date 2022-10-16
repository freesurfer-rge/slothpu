import argparse

from slothpu import assemble_lines

from slothpu.interface import SlothPU_Interface


def build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--assembler-file",
        help="The file containing the assembly code",
        required=True,
    )

    return parser


def main():
    parser = build_argparser()
    args = parser.parse_args()

    with open(args.assembler_file) as f_assembler:
        raw_lines = f_assembler.readlines()
    initial_memory = assemble_lines(raw_lines)

    spu = SlothPU_Interface(initial_memory)
    spu.main()


if __name__ == "__main__":
    main()
