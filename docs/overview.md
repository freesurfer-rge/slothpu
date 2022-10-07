# Overview

The overall goal is to build a functional computer from (mainly) 7400-series logic.
This is to be a pedagogical exercise, so speed of operation is not a particular
concern.
Indeed, I harbour some ambitions to include blinkenlights in the design, so
a slower clock is quite desirable.

The basic design parameters are:

- Load/Store architecture
- 8-bit computation
- 16-bit instructions (aligned on 16-bit bounaries)
- 16-bit addressing

Ideally the size of the computation and the instructions would match.
Unfortunately, this is not possible.

After some thought (and some virtual scribbling), I concluded that
8-bit instructions were not going to be practical.
While very small instructions are certainly possible (e.g. the
[PDP-8](https://en.wikipedia.org/wiki/PDP-8) apparently only had
8 different instruction opcodes), it became apparent to me that all
sorts of trickery would be required to make a working computer
that way.
Such trickery would run against the 'teachable' goal I had,
particularly since modern machines do not work that way at all.
A practical load/store architecture will need to embed three
register choices into its instructions (two for input operands
and one for the output).
If all registers are equal (i.e. no implicit 'accumulator' register
for the output etc.) we need a minimum of four registers,
so identifying three different registers takes 3x2-bits, or 6 bits of
an 8-bit instruction.
Better to go with 16-bit instructions.

I had hoped to avoid 16-bit addressing, but eventually came to the
conclusion that 8-bit addressing wasn't going to work.
With 8-bit addressing, only 256 memory locations can be identified,
but if those locations are themselves 8-bits long, two are going
to be required for each instruction.
This means that total program length
will be limited to *128 instructions at most*.
Anything stored in memory (such as program output) will reduce
the space available for the program instructions, so 8-bit addressing
makes space *extremely* tight.
One final push towards 16-bit addressing comes from I/O considerations.
If this computer is to interact with users, then it needs some
mechanism for doing so.
With 8-bit addressing, there wouldn't be space for memory-mapped I/O,
so instead there would need to be special instructions in the
processor for interacting with I/O units.
This is not a problem with 16-bit addressing, particularly when
[some common SRAM chips](https://www.mouser.com/datasheet/2/698/REN_71256SA_DST_20200629-1996300.pdf)
only have 14-bit addressing.
The last two bits can be used to memory-map I/O devices.

Why not just have 16-bit computation - that is, make the registers
16-bits wide - as well?
The answer is that I have ambitions to solder this design manually.
Going to 16-bits means twice as many joints to solder.
Furthermore, most chips have a maximum of 8 circuits; for example
the [74HC574](https://www.ti.com/lit/ds/symlink/sn54hc574.pdf) is
an 8-bit storage register with a shared clock line and tri-state outputs.
That is ideal for a register file, and anywhere else which needs to
store results temporarily.
Going to 16-bits means doubling the number of these chips
(with a cost in both board space and components), or tracking down
the 16 circuit versions of them (which don't all exist and also
cost more).
Having the size mismatch does introduce some oddness and
not-strictly-necessary complexity, but I believe the tradeoff is
worthwhile.

# Hardware Modules

At a very high level, the design I have in mind will contain the
following hardware modules:

- A backplane with 3 8-bit buses (A, B and C)
- A main memory module, based around a 
  [chip like this](https://www.mouser.com/datasheet/2/698/REN_71256SA_DST_20200629-1996300.pdf).
  This will use combine buses A and B for addressing, and use bus C
  for data
- A register file consisting of 8 8-bit registers.
  Any of these can write to any of the buses (A, B or C),
  and any of them can be written by bus C (possibly B as well... TBD)
- A single operand ALU (shifters, logical not, increment and decrement)
- A dual operand ALU (add/subtract, logical NAND, XOR)
- A program counter. This will be 16-bits long, although it will be an
  error for the least significant bit to be non-zero, since the instructions
  are aligned on 16 bit boundaries
- An instruction register. Also 16-bits long
- An instruction decoder and pipeline orchestrator
- Input and output modules, which will be memory-mapped
- A status register, holding various flags (SALU and DALU for sure)

With 8 registers, the 'register selection' portion of each
instruction will consume 9 of the 16 available bits (since we need
to identify two input registers and one output register).
The remaining 7 bits allow for 128 different instructions,
which is far more than we need.
Furthermore, if some instructions do not require three registers
(for example, the single operand ALU will only require two),
the remaining bits become available for encoding extra
instructions.
To (hopefully) simplify the decoding, I intend to split
the seven bits up into two parts.
The first will identify the 'target' execution unit (e.g. single
operand ALU), while the second part will identify the specific
operation within that execution unit.