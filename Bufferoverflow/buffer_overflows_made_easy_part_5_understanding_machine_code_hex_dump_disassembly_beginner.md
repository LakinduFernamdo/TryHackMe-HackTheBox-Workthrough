# Understanding Machine Code, Hex Dumps, and Disassembly

Beginner-friendly notes for x86-64 assembly, NASM, ELF object files, `xxd`, and `objdump`.

## 1. The big picture

A CPU executes machine-code bytes, not the assembly text we write.

```text
Assembly source (.asm)
       |
       | NASM assembler
       v
Object file (.o)
       |
       | Linker
       v
Executable
       |
       | Operating system loads it
       v
Program runs
```

A **disassembler** reads machine-code bytes and displays the instructions they represent:

```text
Machine-code bytes  --->  Disassembler  --->  Assembly instructions
```

Assembly is a human-readable representation of machine code.

## 2. Bits, bytes, decimal, and hexadecimal

A **bit** is one binary digit: `0` or `1`.

A **byte** contains 8 bits:

\[
1\text{ byte}=8\text{ bits}
\]

The number of possible values in one byte is:

\[
2^8=256
\]

So an unsigned byte can represent values from 0 to 255.

Hexadecimal is base 16. It uses:

```text
0 1 2 3 4 5 6 7 8 9 A B C D E F
```

One hexadecimal digit represents 4 bits. Therefore, two hexadecimal digits represent one byte:

\[
2 \times 4=8\text{ bits}=1\text{ byte}
\]

For example, `48` is one byte, not two bytes.

Hexadecimal place values are powers of 16:

\[
0x48=(4\times16^1)+(8\times16^0)=64+8=72
\]

Therefore:

```text
0x48 = decimal 72 = binary 01001000
```

The uppercase ASCII character `H` has value `0x48`. A byte is just a numeric value; it represents `H` when interpreted as ASCII text.

## 3. Our NASM example

Create `hello.asm`:

```asm
global start

section .data
my_char db 0

section .text
start:
    mov byte [rel my_char], 0x48
    mov al, [rel my_char]
    ret
```

Understand the lines:

- `global start`: makes the symbol `start` visible to the linker.
- `section .data`: section for data.
- `my_char db 0`: defines one byte, initially `00`. `my_char` is its label (name).
- `section .text`: section for instructions.
- `mov byte [rel my_char], 0x48`: writes the one-byte value `0x48` to the memory location represented by `my_char`.
- `mov al, [rel my_char]`: reads one byte from that memory location into `AL`.
- `ret`: returns using the return address on the stack.

### Read versus write

```asm
mov byte [rel my_char], 0x48  ; write 0x48 to memory
mov al, [rel my_char]         ; read one byte from memory into AL
```

Square brackets mean memory access.

Compare:

```asm
mov al, 0x48       ; put immediate value 0x48 into AL
mov al, [my_char]  ; read a byte from memory into AL
```

`AL` is the lowest 8 bits of the `RAX` register.

**Why not use address `0x4000` directly?**

```asm
mov byte [0x4000], 0x48
```

This attempts to write to virtual address `0x4000`. A normal Linux process cannot assume that this address is mapped and writable. It may cause a memory-access fault. Use a label such as `my_char` for this example.

**Note about `ret`:** It is suitable when this code is called as a function. It is not normally how a standalone Linux program should finish when execution begins directly at its entry point. A standalone program should use the operating system's exit system call.

## 4. Assemble and identify the file

For a Linux ELF64 object file:

```bash
nasm -f elf64 hello.asm -o hello.o
file hello.o
```

- `-f` selects the output format.
- `elf64` requests a 64-bit ELF object file.
- ELF is a common Linux executable and object-file format.

For a Windows x64 COFF object file, NASM has a different format option:

```bash
nasm -f win64 hello.asm -o hello.obj
```

The filename extension does **not** determine the file format. A file named `.obj` can contain ELF if it was created with `-f elf64`. Use `file` to identify the actual format.

An ELF object file is not a final ELF executable. A Windows COFF `.obj` is not a final Windows PE executable. The PE optional header belongs to a PE executable image, not an ordinary COFF object file.

## 5. Read a hex dump with `xxd`

Run:

```bash
xxd -g 1 -l 256 hello.o
```

- `xxd`: displays file contents as hexadecimal.
- `-g 1`: groups bytes one at a time.
- `-l 256`: displays **up to** 256 bytes. If the file is shorter, fewer bytes appear.

Example:

```text
00000000: 7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00  .ELF............
00000010: 01 00 3e 00 01 00 00 00 00 00 00 00 00 00 00 00  ..>.............
00000020: 00 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00  ........@.......
00000030: 00 00 00 00 40 00 00 00 00 00 40 00 07 00 03 00  ....@.....@......
```

An xxd row has three parts:

1. **Offset:** position of the first byte of that row in the file.
2. **Hex bytes:** the actual byte values.
3. **ASCII view:** printable bytes shown as characters; non-printable bytes usually appear as dots.

### What is a file offset?

A file offset is a byte's position inside the file. The first byte is at offset `0x00`, the next at `0x01`, then `0x02`, and so on. Offsets start at zero.

### Why does each row start 0x10 later?

With this output format, each row contains 16 bytes. Hexadecimal `0x10` is decimal 16:

\[
0x10=(1\times16)+0=16
\]

Therefore, row offsets increase by `0x10`:

| Row | Hex offset | Decimal offset | Byte positions |
|---:|---:|---:|---:|
| 1 | `0x00` | 0 | 0–15 |
| 2 | `0x10` | 16 | 16–31 |
| 3 | `0x20` | 32 | 32–47 |
| 4 | `0x30` | 48 | 48–63 |
| 5 | `0x40` | 64 | 64–79 |

### How many bytes are displayed?

Use:

\[
\text{Total bytes}=\text{number of rows}\times\text{bytes per row}
\]

Four rows:

\[
4\times16=64\text{ bytes}
\]

So the four rows shown above contain **64 bytes**, not 256.

A complete output containing 16 rows, from offset `0x00` through `0xF0`, contains:

\[
16\times16=256\text{ bytes}
\]

The last row starts at `0xF0` (decimal 240) and contains positions 240 through 255. The next position is `0x100` (decimal 256).

Useful commands:

```bash
xxd -g 1 -l 16 hello.o
xxd -g 1 -l 32 hello.o
xxd -g 1 -l 64 hello.o
xxd -g 1 -l 256 hello.o
ls -l hello.o
stat hello.o
```

`ls -l` and `stat` help you check the actual file size.

## 6. Recognise the ELF header

An ELF file begins with a header. The first bytes commonly look like:

```text
7f 45 4c 46 02 01 01 00 ...
```

Important values:

| Bytes | Meaning |
|---|---|
| `7f 45 4c 46` | ELF magic number |
| `02` | ELF64 class |
| `01` | Little-endian byte order |
| `01` | ELF version 1 |

The ELF header also contains metadata such as file type, target architecture, entry point, and section-header information.

Read it in a human-friendly way:

```bash
readelf -h hello.o
```

The ELF header is file metadata. It is not your program's `.text` instructions.

## 7. Inspect sections with `objdump -h`

Run:

```bash
objdump -h hello.o
```

Example section output:

```text
Sections:
Idx Name          Size      VMA               LMA               File off  Algn
  0 .data         00000001  0000000000000000  0000000000000000  00000200  2**2
  1 .text         0000000e  0000000000000000  0000000000000000  00000210  2**4
```

Important columns:

| Column | Meaning |
|---|---|
| `Name` | Section name |
| `Size` | Section size |
| `VMA` | Virtual memory address associated with the section |
| `LMA` | Load memory address |
| `File off` | Offset where the section's data begins in the file |
| `Algn` | Alignment requirement |

### `.data`

```text
.data    Size: 00000001    File off: 00000200
```

`0x01` is one byte. This section contains our one-byte variable.

### `.text`

```text
.text    Size: 0000000e    File off: 00000210
```

Convert the size:

\[
0x0e=(0\times16)+14=14
\]

So `.text` contains 14 bytes of machine code in this example.

### File offset is not a virtual address

- **File offset:** where bytes are located inside the file on disk.
- **Virtual address:** where a process sees bytes in its virtual memory after loading.

A section can start at file offset `0x210` without executing at virtual address `0x210`. In a relocatable object file, VMA values are commonly zero because the final layout has not yet been assigned.

Inspect the example section data using the offsets reported by your own `objdump -h`:

```bash
xxd -g 1 -s 0x200 -l 16 hello.o
xxd -g 1 -s 0x210 -l 32 hello.o
```

Here `-s` selects the starting file offset. The first 256 bytes end before file offset `0x200` (512 decimal), so a dump starting at zero will not show section data located at `0x200` or `0x210`.

Section offsets vary between files. Always check your own section table rather than assuming these example offsets.

## 8. Decode the disassembly

Run:

```bash
objdump -d -Mintel hello.o
```

Example:

```asm
0000000000000000 <start>:
   0:   c6 05 00 00 00 00 48    mov BYTE PTR [rip+0x0],0x48
   7:   8a 05 00 00 00 00       mov al,BYTE PTR [rip+0x0]
   d:   c3                      ret
```

The output shows the instruction's offset in the section, its machine-code bytes, and the decoded assembly instruction.

### 8.1 First instruction

Bytes:

```text
c6 05 00 00 00 00 48
```

Decoded:

```asm
mov BYTE PTR [rip+0x0], 0x48
```

For this particular x86-64 encoding:

| Bytes | Role |
|---|---|
| `C6` | Opcode |
| `05` | ModR/M byte |
| `00 00 00 00` | 32-bit displacement |
| `48` | Immediate byte value |

**Opcode:** identifies the operation. Here `C6` is a form of `MOV` that writes an immediate byte to a memory operand.

**ModR/M:** an instruction-encoding byte that helps specify operands and the addressing form. Here `05` indicates a memory operand using RIP-relative addressing.

**Displacement:** the next four bytes represent a 32-bit displacement. x86-64 is little-endian, so the four zero bytes represent zero.

**Immediate:** `48` is the constant value written to memory. It is decimal 72 and the ASCII value for `H`.

In plain English: write the byte `0x48` to the memory location calculated using RIP-relative addressing.

### 8.2 Second instruction

Bytes:

```text
8a 05 00 00 00 00
```

Decoded:

```asm
mov al, BYTE PTR [rip+0x0]
```

For this encoding:

| Bytes | Role |
|---|---|
| `8A` | Opcode |
| `05` | ModR/M byte |
| `00 00 00 00` | 32-bit displacement |

`8A` is a `MOV` form that reads a byte from its source operand into a register.

- `AL` is the lowest 8 bits of `RAX`.
- `BYTE PTR` means the memory operand is one byte wide.
- `[rip+0x0]` describes a RIP-relative memory operand.

In plain English: read one byte from the calculated memory location and put it in `AL`.

### 8.3 Third instruction

Bytes:

```text
c3
```

Decoded:

```asm
ret
```

`C3` encodes a near return. `RET` uses the return address on the stack to continue execution at the caller's return location.

## 9. Calculate instruction sizes

Count the byte values in each instruction:

```text
c6 05 00 00 00 00 48  = 7 bytes
8a 05 00 00 00 00     = 6 bytes
c3                    = 1 byte
```

Total:

\[
7+6+1=14\text{ bytes}
\]

Convert decimal 14 to hexadecimal:

\[
14_{10}=0x0e
\]

This matches the `.text` size shown by `objdump -h`:

```text
.text    0000000e
```

This is a useful cross-check: the decoded instructions account for all 14 bytes in `.text`.

## 10. Why does the displacement appear as zero?

Our source uses:

```asm
mov byte [rel my_char], 0x48
mov al, [rel my_char]
```

`my_char` is a label in `.data`. The assembler can create the instruction encoding, but the final layout and addresses have not yet been decided in a relocatable object file.

The zero displacement bytes are placeholders. The object file contains **relocation entries** that tell the linker which machine-code locations need address-related updates.

Inspect them with:

```bash
objdump -r hello.o
readelf -r hello.o
```

The linker uses the relocation information to calculate and patch the appropriate displacement when it creates the final executable.

Therefore, `[rip+0x0]` in this relocatable object-file disassembly does not necessarily mean that the final program accesses the memory immediately after the instruction.

## 11. RIP-relative addressing

RIP is the instruction pointer register. During normal execution it identifies the next instruction to execute.

For RIP-relative memory addressing:

\[
\text{Effective address}=\text{RIP of next instruction}+\text{signed displacement}
\]

Example:

```text
Next instruction RIP = 0x1000
Displacement         = 0x20

Effective address    = 0x1000 + 0x20
                     = 0x1020
```

The displacement is signed, so it can be positive or negative. RIP-relative addressing lets code refer to nearby data without embedding a full absolute address in the instruction.

## 12. Little-endian byte order

x86-64 uses little-endian byte order. For a multi-byte value, the least significant byte is stored at the lowest memory address.

Consider the 32-bit value:

```text
0x12345678
```

Its bytes, from most significant to least significant, are:

```text
12 34 56 78
```

In little-endian memory order:

| Address order | Stored byte |
|---|---|
| Lowest address | `78` |
| Next | `56` |
| Next | `34` |
| Highest address | `12` |

This is why multi-byte values can look reversed when viewed byte-by-byte in a hex dump. The four zero displacement bytes in our example look the same in either order because they are all zero.

## 13. Useful commands

| Goal | Command |
|---|---|
| Identify file format | `file hello.o` |
| Display first 256 bytes | `xxd -g 1 -l 256 hello.o` |
| Display file size | `ls -l hello.o` |
| Detailed file information | `stat hello.o` |
| Show section information | `objdump -h hello.o` |
| Disassemble instructions | `objdump -d -Mintel hello.o` |
| Show relocations | `objdump -r hello.o` |
| Read ELF header | `readelf -h hello.o` |
| Read section headers | `readelf -S hello.o` |
| Read symbol table | `readelf -s hello.o` |
| Read relocation entries | `readelf -r hello.o` |
| Display `.data` bytes | `readelf -x .data hello.o` |
| Display `.text` bytes | `readelf -x .text hello.o` |

## 14. Beginner practice

### Exercise 1: Count bytes

Run:

```bash
xxd -g 1 -l 64 hello.o
```

1. How many bytes are shown per row?
2. How many rows are shown?
3. How many bytes are shown in total?

Use:

\[
\text{Total bytes}=\text{rows}\times\text{bytes per row}
\]

### Exercise 2: Understand `H`

1. What is the decimal value of `0x48`?
2. How many bits are in one byte?
3. What is the binary representation of `0x48`?

### Exercise 3: Decode the first instruction

Look at:

```text
c6 05 00 00 00 00 48
```

1. How many bytes are present?
2. Which byte is the opcode?
3. Which byte is the immediate value?
4. What does the instruction do?

### Exercise 4: Compare bytes and assembly

Run:

```bash
objdump -d -Mintel hello.o
```

Choose one instruction and identify its bytes, opcode, operands, and purpose.

### Exercise 5: Inspect relocations

Run:

```bash
readelf -r hello.o
```

Why does the linker need relocation information?

## 15. Key concepts

| Concept | Meaning |
|---|---|
| Bit | A binary digit: `0` or `1` |
| Byte | 8 bits |
| Hexadecimal | Base-16 number system |
| Machine code | Bytes that the CPU executes |
| Opcode | Identifies the operation |
| ModR/M | Encoding byte that helps specify operands and addressing |
| Displacement | Signed offset used in address calculation |
| Immediate | Constant included directly in an instruction |
| Register | Small, fast storage location inside the CPU |
| `AL` | Lowest 8 bits of `RAX` |
| File offset | Position of data inside a file |
| Virtual address | Address used by a process in virtual memory |
| Section | Named region of an object or executable file |
| Disassembler | Converts machine-code bytes into readable assembly |
| Relocation | Information used by the linker to adjust address-dependent values |
| Little-endian | Least significant byte is stored first |

## Final takeaway

When analysing an object file, keep these layers separate:

1. **File bytes:** what is physically stored in the file?
2. **File structure:** which bytes belong to the ELF header, `.data`, `.text`, and other sections?
3. **Machine-code encoding:** how are instructions represented by bytes?
4. **Disassembly:** how does a tool interpret those bytes as assembly?
5. **Linking and relocation:** how are address-dependent values adjusted?
6. **Runtime memory:** where does the operating system map the program when it runs?

Understanding these layers builds a strong foundation for x86-64 assembly, executable formats, debugging, and reverse engineering.
