# Overview

The overall goal is to build a functional computer from (mainly) 7400-series logic.
This is to be a pedagogical exercise, so speed of operation is not a particular
concern.
Indeed, I harbour some ambitions to include blinkenlights in the design, so
a slower clock is quite desirable.

The basic design parameters are:

- Load/Store architecture
- 8-bit computation
- 16-bit instructions
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
particularly since modern machine do not work that way at all.
A practical load/store architecture will need to embed three
register choices into its instructions (two for input operands
and one for the output).
If all registers are equal (i.e. no implicit 'accumulator' register
for the output), then we need a minimum of four registers,
so identifying three different registers takes 3x2-bits, or 6 bits of
and 8-bit instruction.
Better to go with 16-bit instructions.

