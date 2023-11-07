# Future Plans

Writing approximately a year after I started this project, I have come to the conclusion that this design is not a good one.
There are things I would change around the instruction set (e.g. including a 'compare' instruction), and there are some issues on the manufactured boards (e.g. connecting up the DALU instruction decoder backwards).
Such things could be fixed in a 'rev 2' design.
However, there is a fundamental issue: trying to use 8-bit registers.

## The Problem of Mixed Sizes

I thought that 8-bit registers would simplify the design, and I ignored the warning signs that this wasn't really the case:

1. In order to have a useful program size, you really need at least 16-bit addressing
1. I was going for a load/store design, so ALU operations need to identify three separate registers (two input, one output). This rapidly pushes you to 16-bit instructions

Generating an address then requires two of the registers be read, meaning that the third sometimes has to be read as well (e.g. for 'branch-if-zero' instructions).
This prodded me towards including the 'relative branch' instructions (to avoid burning through too many registers just to perform small loops), requiring addition/subtraction capabilities within the Program Counter unit.
These were easy to add in the emulator, but will require substantial circuitry on the board.

Furthermore, with only one register being writable, saving the Program Counter to a register is impossible.
The high and low bytes would have to be stored on separate instructions, meaning that there will inevitably be cases where the eight bits of the low byte wrap around between the two 'store' instructions.
Instead the program counter unit has to contain a second 'jump' register, whose low and high bytes can be read into registers with separate instructions.
The JSR instruction then has to copy the Program Counter to the jump register, and then reset the program counter itself to the new value.

This leads to a complicated Program Counter (although it wasn't so obvious when writing the emulator).
Even if I can figure out how to implement it properly, it wouldn't really be good for a major goal of this project: not only did I want to prove to myself that I could design a computer, I wanted it to be a useful, 'teachable' machine.

## 16-bit Manufacture

I have also come to realise that going to 16-bit is actually not such a burden on the assembly process as I'd feared.
When sending a PCB for manufacture, you never order just one.
With JLCPCB, the minimum order is 5, and if doing SMD assembly, at least 2 must be assembled.
It does not take that much ingenuity to create an 8-bit _chainable_ ALU, enabling a 16-bit ALU to be created from the two which must be assembled.
Similarly, two 8-bit register files can be paired to create a 16-bit register file.
Now, 'carrier' boards to do the necessary merging are required, but these can be much simpler (and smaller).
Also, through-hole soldering is doubled, but that is not _too_ bad.

## What Now?

I think that a full 16-bit Program Counter would require the following functionality:

- Reset line for the program counter itself
- Put PC on 'A' bus for instruction load and commit (with 16-bit buses there would not be separate FETCH0/FETCH1 steps)
- Cut down set of instructions for the PC itself
- Increment PC step

The instructions required for the PC are:

- LOADPC, which would put the content of the PC on C bus, to be stored in a register
- BRANCHZERO, which would reset the PC to the value of A bus, if B bus were zero. This would probably happen on the Increment PC step. The 'normal' update of Register C would have to be disabled too

This is _much_ simpler than before.
As a final part of this repo, I plan to create an 8-bit version of this Program Counter, for debugging purposes.