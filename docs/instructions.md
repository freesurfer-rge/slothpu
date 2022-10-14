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
Nothing but the register file can *write* to A and B buses.

## Program Counter (PC)

*Functional Unit:* `000` (0)

| Instruction | `fff` | Operation | Registers  | Notes |
|-------------|-------|-----------|------------|-------|
| BRANCH      | `000` | `0000`    | `aaabbb000`|       |
| BRANCHZERO  | `000` | `1000`    | `aaabbbccc`| Register C is read      |
| STOREJUMP   | `000` | `0100`    | `aaabbb000`|       |
| JMP         | `000` | `1100`    | `aaabbb000`|       |
| RET         | `000` | `0010`    | `000000000`| Does not use main registers      |
| LOAD0       | `000` | `0001`    | `000000ccc`|       |
| LOAD1       | `000` | `1001`    | `000000ccc`|       |

Note that LOAD0 and LOAD1 are only a single bit different
their operation code.
They also have the most significant bit of that operation
code be a one, and all the others have a zero.
Also note that the operation code for BRANCHZERO is the same
as that for MEM STORE below; both operations *read* from 
register C.


## Memory (MEM)

*Functional Unit:* `100` (1)

| Instruction | `fff` | Operation | Registers  | Notes |
|-------------|-------|-----------|------------|-------|
| LOAD        | `100` | `0000`    | `aaabbbccc`|       |
| STORE       | `100` | `1000`    | `aaabbbccc`| Register C is read      |

Note that the operation code for STORE is the same as for
PC BRANCHZERO.
These are the two operations which *read* from register C.

## Registers (REG)

*Functional Unit:* `010` (2)

| Instruction | `fff` | Operation | Registers  | Notes |
|-------------|-------|-----------|------------|-------|
| SETnnn      | `010` | `00vv`    | `vvvvvvccc`| Value is 'nnn' in decimal, and `vvvvvvvv` in little-endian binary      |
| LOADSTATUS  | `010` | `1000`    | `000000ccc`|       |

The SETnnn instructions borrow bits from the register selectors.

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

Having a single bit of difference between INC and
DEC makes a two's complement implementation relatively
straightforward. Similar considerations apply to NOT and COPY.


## Dual Operand ALU (DALU)

*Functional Unit:* `101` (5)

| Instruction | `fff` | Operation | Registers  | Notes |
|-------------|-------|-----------|------------|-------|
| ADD         | `101` | `0000`    | `aaabbbccc`|       |
| SUB         | `101` | `1000`    | `aaabbbccc`| Single bit aids two's complement      |
| OR          | `101` | `0010`    | `aaabbbccc`|       |
| XOR         | `101` | `1010`    | `aaabbbccc`|       |
| AND         | `101` | `0110`    | `aaabbbccc`| Use NAND with inverting 74HC540 buffer      |
| NAND        | `101` | `1110`    | `aaabbbccc`|       |

The single bit difference in operation code for ADD and
SUB makes a two's complement implementaiton relatively
straightforward.