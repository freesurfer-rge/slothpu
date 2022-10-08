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
| BRANCHZERO  | `100` | `1000`    | `aaabbbccc`| Register C is read      |



## Memory (MEM)

*Functional Unit:* `100` (1)

| Instruction | `fff` | Operation | Registers  | Notes |
|-------------|-------|-----------|------------|-------|
| LOAD        | `100` | `0000`    | `aaabbbccc`|       |
| STORE       | `100` | `1000`    | `aaabbbccc`| Register C is read      |

## Registers (REG)

*Functional Unit:* `010` (2)

| Instruction | `fff` | Operation | Registers  | Notes |
|-------------|-------|-----------|------------|-------|
| SETnnn      | `010` | `00vv`    | `vvvvvvccc`| Value is 'nnn' in decimal, and `vvvvvvvv` in little-endian binary      |
| LOADSTATUS  | `010` | `1000`    | `000000ccc`|       |
| LOADPC      | `010` | `0100`    | `000bbbccc`| Register B written |

## Single Operand ALU (SALU)

*Functional Unit:* `001` (4)

| Instruction | `fff` | Operation | Registers  | Notes |
|-------------|-------|-----------|------------|-------|
| INC         | `001` | `0000`    | `aaa000ccc`|       |
| DEC         | `001` | `1000`    | `aaa000ccc`| Single bit change aids two's complement      |
| NOT         | `001` | `1100`    | `aaa000ccc`|       |
| COPY        | `001` | `0100`    | `aaa000ccc`| Single bit aids sharing with NOT |
| LBARREL     | `001` | `0001`    | `aaa000ccc`|       |
| RBARREL     | `001` | `0101`    | `aaa000ccc`|       |
| LSHIFT0     | `001` | `0011`    | `aaa000ccc`|       |
| LSHIFT1     | `001` | `1011`    | `aaa000ccc`|       |
| RSHIFT0     | `001` | `0111`    | `aaa000ccc`|       |
| RSHIFT1     | `001` | `1111`    | `aaa000ccc`|       |

Note that the operations for the shifters are all written as
`idm1` were `m` encodes the mode (barrel or regular), `d` encodes
the direction (left or right) and `i` encodes where the
'shift-in' bit is 0 or 1.

## Dual Operand ALU (DALU)

*Functional Unit:* `101` (5)

| Instruction | `fff` | Operation | Registers  | Notes |
|-------------|-------|-----------|------------|-------|
| ADD         | `101` | `0000`    | `aaabbbccc`|       |
| SUB         | `101` | `1000`    | `aaabbbccc`| Single bit aids two's complement      |
