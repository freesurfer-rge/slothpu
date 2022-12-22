# DALU Design Notes

The DALU has the following inputs and outputs:

- A bus (8 wires)
- B bus (8 wires)
- Instruction OpCode (4 wires)
- DALU selector (active low)
- Pipeline stage indication (3 wires Decode/Execute/Commit)
- C bus (8 wires, output)
- DALU flag (output)

This is a total of 24 input wires and 9 output wires.
All of the input wires should be buffered on the board, since they
are coming from the backplane, and hence being routed to multiple
similar boards.

The DALU selector will come from a 74HC138 3-to-8 decoder on the
backplane, inspecting the three 'functional unit' bits of the
instruction.
This is why this line will be active low.

The pipeline stages relevant to the DALU are Decode, Execute
and Commit.
These are active high lines, but only one will be high at
any one time (or all can be low).


## Decoding the instruction

The instruction opcodes have been chosen to be fairly orthogonal,
with an eye to easy decoding.
However, I believe that it will still be simpler to use a pair
of 74HC138 3-to-8 decoders to produce 16 output lines.
Invalid opcodes can then easily have a red LED attached.
Furthermore, the DALU selector can be included into the decoding
to force all operation lines high.
This means that the individual subunits will not need to
check the DALU selector itself.

## General layout

The DALU contains the following subunits:

- Adder/Subtractor
- AND/NAND
- OR
- XOR

Each of these 'ends' with a tristate buffer, which
is controlled by the appropriate operation line.
If a subunit has more than one function (e.g. add and
subtract), then the buffer (which will be active low)
can be controlled by 'AND'ing the two opertaion
lines together (since these are also active low, and
only one can be active at a time).

The subunit buffers then feed into the output register.
Pulldown resistors will be needed on these lines
since it is possible for all of them to be high impedance
at the same time (if the DALU is not active).

The DALU flag is mainly for the adder/subtractor.
This is set to the carry out of an add operation, and
its inverse for a subtract operation (this is so that
a '1' indicates an over or underflow, and a '0' means
that the answer is complete).
For all other operations, the DALU flag will be reset to
zero.

## Pipeline Stages

The pipeline stage wires are combined with the DALU selector
(which unlike them is active low).

If the DALU selector is low, then it opens the input buffers.

The output register is only connected to C bus if the DALU is
selected and one of the pipeline stage wires is high.

The 'execute' wire is used to clock the output register (and
DALU flag register).