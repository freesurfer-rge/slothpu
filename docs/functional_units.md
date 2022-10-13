# Functional Units

We will now go through the various function units in more detail, and note what
each can do and when.
Instructions can designate any of the 8 physical registers as A, B or C.

In the following, phrases such as 'reading the value of Register A' should be
understood to mean 'during the decode phase, the value of Register A will be
placed on A bus, and used during the execute phase.'
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



## Memory Operations

*Functional Selector:* MEM

Memory always uses A (low) and B (high) buses for the address, and C bus for data.
This means that C bus will be bidirectional.
Recall also that main memory will likely only be 14-bit addressable, leaving
the top two bits to select memory mapped peripherals.
All 'memory' units should take care that their connection to C bus is in a high
impedence state unless they are selected by the two top bits.

During the Fetch0 and Fetch1 pipeline stages, the next instruction will be
read.

### Load (MEM LOAD)

During the 'Execute' pipeline stage, combine A bus and B bus into an address.
Put the corresponding byte onto C bus

### Store (MEM STORE)

During the 'Commit' pipeline stage, combine A bus and B bus into an address.
Write the corresponding byte from C bus



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
That is 87654321 becomes 76543218; we are interpreting this as
a left shift on the implied integer, not a left shift on an
array of bits.
Set the flag to zero

### Barrel Shift Right (SALU RBARREL)

Perform a barrel shift right on the value.
That is 87654321 becomes 18765432; we are interpreting this as
a left shift on the implied integer, not a left shift on an
array of bits.
Set the flag to zero

### Shift Left Inject 0 (SALU LSHIFT0)

Perform a left shift on the value, injecting 0.
That is 87654321 becomes 76543210.
We are interpreting the left shift as a multiply by two (mod 256).
Set the flag to the value of bit 8.

### Shift Right Inject 0 (SALU RSHIFT0)

Perform a right shift on the value, injecting 0.
That is 87654321 becomes 08765432.
We are interpreting the left shift as a divide by two on the integer.
Set the flag to the value of bit 0.

### Shift Left Inject 1 (SALU LSHIFT1)

Perform a left shift on the value, injecting 1.
We are interpreting the left shift as a multiply by two (mod 256).
Set the flag to the value of bit 8.

### Shift Right Inject 1 (SALU RSHIFT1)

Perform a right shift on the value, injecting 1.
We are interpreting the left shift as a divide by two on the integer.
Set the flag to the value of bit 0.



## Dual Operand ALU

*Functional Selector:* DALU

The Dual Operand ALU takes its input from A & B buses and can
place its output on C bus.
In the following, we will simply refer to 'the values.'
It also has a 'flag' line which feeds into its own bit
of the status register.

### Sum (DALU ADD)

Add the values.
Place carry out bit (i.e. wrap/overflow) on the flag.

### Difference (DALU SUB)

Subtract B from A.
Place inverse of the carry out bit (i.e. borrow/underflow)
on the flag.

### Bitwise OR (DALU OR)

Perform bitwise OR on the values.
Set flag to 0.

### Bitwise AND (DALU AND)

Perform bitwise AND on the values.
Set flag to 0.
Note that this can share logic
with the NAND below, but just
use an inverting buffer (74HC540 vs 74HC541).

### Bitwise XOR (DALU XOR)

Perform bitwise XOR on the values.
Set flag to 0.

### Bitwise NAND (DALU NAND)

Perform bitwise NAND on the values.
Set flag to 0.