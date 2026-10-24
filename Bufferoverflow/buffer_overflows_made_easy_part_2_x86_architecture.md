# Buffer Overflows Made Easy — Part 2
## Understanding x86, x86-64, Bits, Registers, and Memory

> **Goal:** Build the computer-architecture knowledge needed to understand assembly, debugging, reverse engineering, and buffer overflows. Diagrams simplify modern hardware; real implementations vary by CPU, operating system, and compiler.

---

## 1. What is computer architecture?

Computer architecture describes how a computer's processor understands instructions and works with data. An **instruction-set architecture (ISA)** defines the instructions a processor understands, the registers it exposes, and other rules software relies on.

- **x86** is a family of instruction-set architectures historically associated with 32-bit Intel-compatible computing.
- **x86-64**, also called **x64** or **AMD64**, is the 64-bit extension of x86.

Programs compiled for different architectures may use different registers and instructions. This is why disassembly can look different for 32-bit and 64-bit programs.

### Architecture versus operating system

- **CPU architecture:** the instruction set and execution model, such as x86-64.
- **Operating system:** software that manages processes, memory, devices, and permissions, such as Linux or Windows.
- **Program architecture:** the architecture for which a particular executable was built.

A 64-bit CPU can often support 32-bit programs, depending on the OS and compatibility support. A 64-bit CPU does not mean every program running on it is 64-bit.

## 2. What is a bit?

A **bit** is the smallest unit of digital information. It can have one of two values: `0` or `1`. A group of bits can represent a number, a character, an instruction, or other information. Each additional bit doubles the number of possible bit patterns.

### Example: four bits

Each position represents a power of two:

| Bit position | Value when the bit is 1 |
|---|---:|
| 3 | 2³ = 8 |
| 2 | 2² = 4 |
| 1 | 2¹ = 2 |
| 0 | 2⁰ = 1 |

For example:

```text
Binary: 1011

1 × 2³ = 8
0 × 2² = 0
1 × 2¹ = 2
1 × 2⁰ = 1

Total: 8 + 0 + 2 + 1 = 11
```

So binary `1011` represents decimal `11`.

## 3. How many values can n bits represent?

Each bit has two possible values. Therefore, `n` bits can form:

**Number of possible patterns = 2ⁿ**

For **unsigned** numbers, all patterns represent non-negative values:

- Minimum = `0`
- Maximum = `2ⁿ − 1`

The subtraction of 1 is needed because the count includes zero.

### Example: 8-bit unsigned number

1. Calculate the number of patterns: `2⁸ = 256`.
2. The values start at zero, so the 256 patterns represent `0` through `255`.
3. Maximum = `2⁸ − 1 = 256 − 1 = 255`.

Therefore, an 8-bit unsigned number ranges from **0 to 255**.

### Common unsigned ranges

| Width | Number of patterns | Minimum | Maximum |
|---|---:|---:|---:|
| 4-bit | 2⁴ = 16 | 0 | 15 |
| 8-bit | 2⁸ = 256 | 0 | 255 |
| 16-bit | 2¹⁶ = 65,536 | 0 | 65,535 |
| 32-bit | 2³² = 4,294,967,296 | 0 | 4,294,967,295 |
| 64-bit | 2⁶⁴ = 18,446,744,073,709,551,616 | 0 | 18,446,744,073,709,551,615 |

A 64-bit value has a very large range. However, a 64-bit register does **not** guarantee that the system can use all 2⁶⁴ addresses. CPUs and operating systems typically support fewer virtual-address bits than that.

## 4. Signed numbers and two's complement

Unsigned numbers represent zero and positive values. Programs also need to represent negative integers. A widely used representation is **two's complement**.

For an `n`-bit two's-complement signed integer:

- Minimum = `−2⁽ⁿ⁻¹⁾`
- Maximum = `2⁽ⁿ⁻¹⁾ − 1`

### Example: range of an 8-bit signed integer

1. Eight bits give `2⁸ = 256` patterns.
2. In two's complement, the range is `−2⁷` through `2⁷ − 1`.
3. Calculate the endpoints: `−2⁷ = −128` and `2⁷ − 1 = 128 − 1 = 127`.

An 8-bit signed integer therefore ranges from **−128 to +127**. The unsigned range is 0 to 255, while the signed range is −128 to 127. The bit pattern itself does not announce whether it is signed or unsigned; the program's type and interpretation determine its meaning.

### How to represent −5 using 8-bit two's complement

**Step 1 — Write positive 5 in binary.**

```text
5 = 00000101
```

**Step 2 — Flip every bit.** Change each `0` to `1` and each `1` to `0`.

```text
Original: 00000101
Flipped:  11111010
```

This is called the **one's complement**.

**Step 3 — Add 1.**

```text
  11111010
+ 00000001
----------
  11111011
```

Therefore, in 8-bit two's complement, **−5 = `11111011`**.

### Check the answer

For an 8-bit two's-complement pattern, the leftmost bit has a weight of −2⁷ = −128. The other bit positions have positive weights.

```text
Binary: 11111011

Weights:
-128 + 64 + 32 + 16 + 8 + 0 + 2 + 1
= -128 + 123
= -5
```

So `11111011` represents −5 when interpreted as an 8-bit signed two's-complement integer. As an 8-bit **unsigned** integer, the same pattern represents 251.

### Why two's complement matters

It is useful when examining signed integer variables in C, values displayed in registers or memory, arithmetic in assembly, and bugs caused by incorrect assumptions about signedness.

**Key lesson:** the same bits can represent different values depending on their width and interpretation.

## 5. What does 32-bit or 64-bit mean?

The terms 32-bit and 64-bit can refer to several related properties of a CPU architecture. First focus on the width of general-purpose registers and the kinds of values they can hold:

- A 32-bit register can hold 2³² different bit patterns.
- A 64-bit register can hold 2⁶⁴ different bit patterns.

For unsigned values:

```text
32-bit: 0 to 4,294,967,295
64-bit: 0 to 18,446,744,073,709,551,615
```

But **register width and virtual-address width are not identical**. The CPU architecture, operating system, and processor implementation determine which address sizes are supported and usable.

A 64-bit system also does not require every value to occupy eight bytes. A program can still work with 8-bit characters, 16-bit values, 32-bit integers, and 64-bit integers.

## 6. CPU basics: ALU, Control Unit, and registers

The **Central Processing Unit (CPU)** executes instructions. A simplified teaching model describes three important parts:

```text
                  +----------------------+
                  |          CPU         |
                  |                      |
                  |  +----------------+  |
                  |  | Control Unit   |  |
                  |  +----------------+  |
                  |          |           |
                  |  +----------------+  |
                  |  | ALU            |  |
                  |  +----------------+  |
                  |          |           |
                  |  +----------------+  |
                  |  | Registers      |  |
                  |  +----------------+  |
                  +----------------------+
```

### ALU — Arithmetic Logic Unit

Performs arithmetic and logical operations, such as addition, subtraction, and comparisons.

### Control Unit

Coordinates instruction execution, including interpreting instructions and control signals. Modern CPUs have complex pipelines and multiple execution units, so this is a simplified model.

### Registers

Registers are small, fast storage locations inside the CPU. They can hold values, addresses, and execution state while instructions run. Registers are important in reverse engineering because debuggers and disassemblers show them frequently. Modern CPUs also include caches, instruction decoders, and specialized execution units; their internal details can be learned later.

## 7. How does the CPU communicate with memory?

Introductory computer architecture often explains communication using three concepts: address, data, and control.

```text
+----------------+                       +----------------+
|      CPU       |                       |     Memory     |
|                | -- Address ---------->|                |
|                | <---- Data ---------->|                |
|                | -- Control signals ->|                |
+----------------+                       +----------------+
```

- **Address:** identifies the location the CPU wants to access.
- **Data:** the value being transferred.
- **Control signals:** indicate the kind of operation, such as reading or writing.

### Example: reading a value

1. The CPU determines which address it needs.
2. The address is provided to the memory system.
3. A read operation is requested.
4. The memory system returns the requested data.

This is a conceptual model. Modern computers may route requests through caches, memory controllers, and interconnects rather than using three simple, separate physical buses exactly as shown.

An address is **not** the same as the data stored at that address. An address tells the system *where* to look; the data is *what* it finds there.

## 8. Bytes, memory addresses, and hexadecimal

A **byte** is 8 bits. Memory is commonly organized into byte-addressable locations, meaning each byte has its own address.

```text
Address       Value stored
0x1000        0x41
0x1001        0x42
0x1002        0x43
```

The addresses identify locations. The values are the bytes stored at those locations.

### Why do reverse-engineering tools use hexadecimal?

Hexadecimal, or **base 16**, uses these symbols:

```text
0 1 2 3 4 5 6 7 8 9 A B C D E F
```

One hexadecimal digit represents four bits:

| Binary | Hexadecimal |
|---|---|
| `0000` | `0` |
| `0001` | `1` |
| `1001` | `9` |
| `1010` | `A` |
| `1111` | `F` |

Example:

```text
Binary:      1111 0000
Split:       1111 | 0000
Hex digits:     F |    0

Result:      0xF0
```

The prefix `0x` commonly indicates a hexadecimal number. Ghidra, GDB, and other tools often display addresses and raw values in hexadecimal because it is compact and maps neatly to binary.

## 9. x86 and x86-64 general-purpose registers

Register names differ between 32-bit and 64-bit x86. In x86-64, many older registers have extended names that indicate their wider forms.

### Common overlapping register names

| 64-bit | 32-bit | 16-bit | Lowest 8-bit |
|---|---|---|---|
| RAX | EAX | AX | AL |
| RBX | EBX | BX | BL |
| RCX | ECX | CX | CL |
| RDX | EDX | DX | DL |
| RSI | ESI | SI | SIL |
| RDI | EDI | DI | DIL |
| RBP | EBP | BP | BPL |
| RSP | ESP | SP | SPL |

For the first four register families, the older 8-bit high portions also have names:

- `AH` — high 8 bits of `AX`
- `BH` — high 8 bits of `BX`
- `CH` — high 8 bits of `CX`
- `DH` — high 8 bits of `DX`

The high-byte registers `AH`, `BH`, `CH`, and `DH` have encoding restrictions in x86-64 instructions that use certain prefixes. Beginners can learn that detail later if they encounter it.

x86-64 also adds eight more general-purpose registers:

```text
R8, R9, R10, R11, R12, R13, R14, R15
```

These have 32-bit, 16-bit, and 8-bit forms, such as `R8D`, `R8W`, and `R8B`.

### What do common registers do?

Registers can be used for many purposes, but some have conventional roles.

| Register | Common role or use |
|---|---|
| RAX / EAX | Often used for return values and arithmetic |
| RBX / EBX | General-purpose storage; may be preserved across calls under a calling convention |
| RCX / ECX | General-purpose storage; used for arguments or counts in some conventions and instructions |
| RDX / EDX | General-purpose storage; used for arguments or arithmetic in some conventions and instructions |
| RSI / ESI | General-purpose storage; sometimes used as a source pointer |
| RDI / EDI | General-purpose storage; sometimes used as a destination pointer |
| RSP / ESP | Stack pointer |
| RBP / EBP | Sometimes used as a frame/base pointer |
| RIP / EIP | Instruction pointer |
| RFLAGS / EFLAGS | Status and control flags |

**Important:** most general-purpose registers are not permanently assigned to one task. Their roles depend on the instructions, calling convention, and generated code.

### Example: RAX, EAX, AX, and AL

These names refer to overlapping portions of one register, not four independent registers.

```text
RAX: 64 bits
+---------------------------------------------------------------+
|                              RAX                              |
+---------------------------------------------------------------+

EAX: lower 32 bits of RAX
+--------------------------------+
|              EAX               |
+--------------------------------+

AX: lower 16 bits of RAX
+----------------+
|       AX       |
+----------------+

AL: lowest 8 bits of RAX
+--------+
|   AL   |
+--------+
```

The lower 16 bits of `RAX` are `AX`. The lower 8 bits of `AX` are `AL`, and bits 8–15 are `AH`.

### A crucial x86-64 rule

In 64-bit mode, writing to a 32-bit register such as `EAX` clears the upper 32 bits of `RAX`.

For example, writing the value `5` to `EAX` results in:

```text
RAX = 0x0000000000000005
```

By contrast, writing to `AX` or `AL` updates only that smaller portion and leaves the other bits unchanged. This rule is important when reading register values in a debugger.

## 10. Stack pointer, frame pointer, instruction pointer, and flags

These registers are especially useful when studying buffer overflows.

### Stack pointer: RSP / ESP

Tracks the current top of the stack. In classic x86 stack operations, pushing data usually moves the stack pointer toward lower addresses.

### Frame pointer: RBP / EBP

Can provide a stable reference point for a function's stack frame. Compilers sometimes omit it or use the register for another purpose, especially in optimized code.

### Instruction pointer: RIP / EIP

Tracks the address used for instruction execution. In a classic 32-bit x86 explanation, `EIP` is the instruction pointer; in x86-64, it is `RIP`.

The instruction pointer is not normally treated like an ordinary general-purpose register that can be changed with any simple `MOV` instruction. Control-flow instructions such as `call`, `ret`, and jumps affect where execution continues.

### Flags: RFLAGS / EFLAGS

Contain status and control bits. Arithmetic and comparison operations can affect flags that conditional jumps inspect. Later, when studying assembly, learn how `cmp` and conditional jumps use flags to implement decisions such as `if` statements.

## 11. Little-endian byte order

Endianness describes the order in which the bytes of a multi-byte value are stored in memory.

Consider this 32-bit value:

```text
0x12345678
```

It consists of four bytes: `12`, `34`, `56`, and `78`.

**Big-endian** stores the most significant byte at the lowest address:

```text
Lower address ->  12 34 56 78  -> Higher address
```

**Little-endian** stores the least significant byte at the lowest address:

```text
Lower address ->  78 56 34 12  -> Higher address
```

Many x86 and x86-64 systems use little-endian byte order. This matters when examining raw memory in Ghidra or GDB. The number itself has not changed; only the order of its bytes in memory differs.

## 12. How Ghidra displays assembly

Ghidra is a reverse-engineering framework that can disassemble machine code into assembly instructions and produce a decompiler view resembling C.

For example:

```asm
MOV EAX, 5
ADD EAX, 3
RET
```

At a high level:

- `MOV EAX, 5` — places the value 5 in `EAX`.
- `ADD EAX, 3` — adds 3 to `EAX`, making the value 8.
- `RET` — returns from the current function using the architecture's return mechanism.

This is a short illustrative instruction sequence, not a complete program. Ghidra may show registers such as `RAX`, `EAX`, `RSP`, and `RIP`, depending on the target architecture and context.

### Disassembly versus decompilation

- **Disassembly** translates machine-code bytes into assembly instructions.
- **Decompilation** attempts to reconstruct a higher-level representation, often C-like pseudocode.

Decompiled output is an approximation. It is not necessarily the original source code, and names, types, and structures may be inferred.

## 13. Why these concepts matter for buffer overflows

These topics explain the environment in which a vulnerability occurs:

- **Bits and integer ranges** help explain data sizes and integer-related mistakes.
- **Memory addresses** help you understand where data is stored.
- **Registers** show the values and execution state used by the CPU.
- **Stack frames** organize function-call information.
- **Instruction pointers** help explain how execution moves from one instruction to another.
- **Assembly** shows what the processor actually executes.
- **Ghidra and debuggers** help you inspect compiled programs and observe behavior.

A stack-based buffer overflow happens when a program writes beyond the bounds of a buffer stored in a stack frame. Depending on the program and its protections, that can corrupt nearby data and potentially affect control flow.

Understanding the architecture first makes it easier to understand why such bugs happen and why modern protections matter.

## 14. Key takeaways

1. A bit can be `0` or `1`; `n` bits form `2ⁿ` possible patterns.
2. An unsigned `n`-bit integer ranges from `0` to `2ⁿ − 1`.
3. Two's complement is a common way to represent signed integers, including negative values.
4. x86 and x86-64 use different register widths and conventions.
5. CPU registers hold values, addresses, and execution state.
6. An address identifies a memory location; data is the value stored there.
7. Hexadecimal is a compact way to represent binary values.
8. `RAX`, `EAX`, `AX`, and `AL` are overlapping portions of the same register.
9. `RSP` tracks the stack, `RIP` tracks instruction execution, and flags affect conditional behavior.
10. Ghidra's disassembly and decompilation help inspect compiled programs, but decompiled output is not guaranteed to match the original source.

## Next part

**Part 3: Basic x86-64 Assembly Language**

Next, learn instructions such as `MOV`, `LEA`, `PUSH`, `POP`, `CALL`, `RET`, `CMP`, and conditional jumps. Use small examples to connect each instruction to registers, memory, and the C code it represents.
