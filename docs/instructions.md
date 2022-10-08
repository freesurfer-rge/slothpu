# Instructions

All instructions are 16-bits long and are aligned on 16-bit boundaries.
In this document *little-endian* ordering is used throughout.

## General Format

All instructions are laid out as follows:

```
-0--------8--------
|fff....a|aabbbccc|
-------------------
Byte n    Byte n+1
```

Where

- `fff` identify the functional unit
- `aaa` identify the register to be connected to A bus
- `bbb` identify the register to be connected to B bus
- `ccc` identify the register to be connected to C bus
- The remaining four bits encode the specific operation

If a particular instruction does not use one or more of the
registers, those bits may be used for encoding the operation.
In most cases, register C is being written, and so its input
will be connected to C bus, not its output.
This can happen to register B as well, although that is less
common.
Register A is always read, and hence its output will always
be connected to A bus.

## Program Counter (PC)

*Functional Unit:* `000` (0)

| Instruction | `fff` | Operation | Registers  | Notes |
|-------------|-------|-----------|------------|-------|
| BRANCH      | `000` | `0000`    | `aaabbb000`|       |
| BRANCHZERO  | `100` | `1000`    | `aaabbbccc`|       |



## Memory (MEM)

*Functional Unit:* `100` (1)

| Instruction | `fff` | Operation | Registers  | Notes |
|-------------|-------|-----------|------------|-------|
| LOAD        | `100` | `0000`    | `aaabbbccc`|       |
| STORE       | `100` | `1000`    | `aaabbbccc`|       |

## Registers (REG)

*Functional Unit:* `010` (2)

| Instruction | `fff` | Operation | Registers  | Notes |
|-------------|-------|-----------|------------|-------|
| SETnnn      | `010` | `00vv`    | `vvvvvvccc`| Value is nnn in decimal, and `vvvvvvvv` in little-endian binary      |
