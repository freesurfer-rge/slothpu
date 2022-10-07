# Functional Units

We will now go through the various function units in more detail, and note what each can do and when.

In the following, phrases such as 'reading the value of Register A' should be understood to mean
'during the decode phase, the value of Register A will be placed on A bus.'
Similarly, 'writing the value of Register C' means 'during the commit phase, Register C will be
updated from the C bus.'
We will only specify the process in more detail for

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

This instruction is used to place a constant into Register C




## Single Operand ALU

*Functional Selector:* SALU

