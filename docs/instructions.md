# Instructions

All instructions are 16-bits long and are aligned on 16-bit boundaries.

## General Format

All instructions are laid out as follows:

```
-0--------8-------
|fff....a|aabbbcc|
------------------
Byte n    Byte n+1
```

Where

- `fff` are three bits to identify the functional unit
