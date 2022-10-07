# Execution Pipeline

This design will have the following pipeline stages:

- Fetch0
- Fetch1
- Decode
- Execute
- Commit
- PC Update

Each clock pulse advances the pipeline to the next stage,
so each instruction will take six clock pulses to complete.
Only one instruction will be 'in flight' at a time.
Both of these choices are to maintain simplicity for
learning purposes.

## Fetch0

During this stage, the *low* byte of the next instruction
will be fetched from memory (address provided by the Program
Counter) and placed in the low byte of the Instruction Register.
This stage will also reset the 'increment enabled' flag of
the Program Counter.

## Fetch1

This fetchs the *high* byte of the next instruction, whose location
will be obtained by flipping the LSB of the Program Counter address.

## Decode

During this stage, the appropriate execution unit will
be activated, and their inputs and outputs connected to the
appropriate bus.

## Execute

The appropriate execution unit will perform its task, placing
its result on the appropriate bus.
In the case of a branch instruction, the Program Counter's
'increment enabled' flag will be marked as false.

## Commit

The result is saved from the bus, either to a register or to
main memory.
The SALU and DALU bits of the status register will also be
updated at this time.

## PC Update

If the 'increment enabled' flag of the Program Counter is true
(which it will be unless a branch has occurred), increment
the Program Counter by two.