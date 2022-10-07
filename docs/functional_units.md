# Functional Units

We will now go through the various function units in more detail, and note what
each can do and when.
Instructions can designate any of the 8 physical registers as A, B or C.

In the following, phrases such as 'reading the value of Register A' should be
understood to mean 'during the decode phase, the value of Register A will be
placed on A bus.'
Similarly, 'writing the value of Register C' means 'during the commit phase,
Register C will be updated from the C bus.'
We will only specify the process in more detail when clarity requires.

## Program Counter

*Functional Selector:* PC

This consists of a 16-bit address register and an 'increment enabled' flag.

During the Fetch0 and Fetch1 pipeline stages, it places its value on the A and B buses
(for Fetch1, the LSB is inverted).
Also during the Fetch0 stage, the Program Counter will reset the 'increment enabled' flag
to True.

During the PC Update pipeline stage, the Program Counter will increase its value by 2
(wrapping), unless its 'increment enabled' flag is False.

### Branch (PC BRANCH)

This instruction unconditionally copies the contents of the A and B buses to the Program
Counter, and sets the 'increment enabled' flag to False.

### Branch If Zero (PC BRANCHZERO)

If all lines on C bus are zero, copy the contents of the A and B buses to the Program
Counter and set the 'increment enabled' flag to False. If any of the C bus lines are
non-zero, make no changes to the Program Counter, and leave 'increment enabled' as True



## Register Operations

*Functional Selector:* REG

### Set (REG SETnnn)

This instruction is used to place a constant into Register C.
The value of the constant is embedded in 8-bits of the instruction,
and represented by 'nnn' (base 10) above.

### Load Status Register (REG LOADSTATUS)

Copy the contents of the status register into Register C.
The status register itself is left unchanged.

### Load PC (REG LOADPC)

Copy the contents of the Program Counter into Registers
B (low byte) and C (high byte).
This should be the only instruction which can write to
two registers.



## Single Operand ALU

*Functional Selector:* SALU

The Single Operand ALU takes its input from A bus and can
place its output on C bus.
In the following, we will simply refer to 'the value.'
It also has a 'flag' line which feeds into its own bit
of the status register.

### Increment (SALU INC)

Increment the value by 1.
Set the flag to the carry out (i.e. indicate if overflow
and wrapping occurred).

### Decrement (SALU DEC)

Decrement the value by 1
Do this two's complement, and store the inverse
of the 'carry out' (i.e. borrow/wrap) in the flag.

### Bitwise NOT (SALU NOT)

Perform a bitwise NOT on the value.
Set the flag to zero

### Bitwise Copy (SALU COPY)

Would just copy the value... unsure of the value of this.

### Barrel Shift Left (SALU LBARREL)

Perform a barrel shift left on the value.
That is 87654321 becomes 76543218.
Set the flag to zero

### Barrel Shift Right (SALU RBARREL)

Perform a barrel shift right on the value.
That is 87654321 becomes 187654321.
Set the flag to zero

### Shift Left Inject 0 (SALU LSHIFT0)

Perform a left shift on the value, injecting 0.
That is 87654321 becomes 76543210.
Set the flag to the value of bit 8.

### Shift Right Inject 0 (SALU RSHIFT0)

Perform a right shift on the value, injecting 0.
That is 87654321 becomes 08765432.
Set the flag to the value of bit 0.