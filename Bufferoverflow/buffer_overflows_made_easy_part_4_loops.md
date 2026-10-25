# Understanding an x86-64 Assembly Loop with NASM and GDB

This guide explains a small Linux x86-64 assembly program that counts
from `0` to `5`. It is written for beginners who want to understand what
each instruction does, how the loop works, and how to inspect CPU
registers and flags in GDB.

## 1. The complete program

Save this as `loop.asm`:

``` asm
section .text
global _start

_start:
    xor rax, rax        ; Set RAX to 0

loop:
    inc rax             ; RAX = RAX + 1
    cmp rax, 5          ; Compare RAX with 5
    jnz loop            ; Jump to loop if the values are not equal

    ; Exit the program cleanly
    mov rax, 60         ; Linux x86-64 exit system call number
    xor rdi, rdi        ; Exit status = 0
    syscall
```

The loop increases `RAX` until it reaches `5`. Once `RAX` equals `5`,
the conditional jump is not taken and the program continues to the exit
instructions.

## 2. Important terms

### What is `RAX`?

`RAX` is a 64-bit general-purpose CPU register. A register is a very
small, very fast storage location inside the CPU. Assembly instructions
can use registers to hold numbers and other data.

For this example, we use `RAX` as our counter:

-   At the beginning, `RAX` is set to `0`.
-   Each `inc rax` instruction adds `1`.
-   The loop stops when `RAX` reaches `5`.

### What is `RIP`?

`RIP` is the instruction pointer in 64-bit x86. It holds the address of
the next instruction the CPU will execute. When a jump is taken, the
instruction pointer is changed to the target instruction's address.

### What are CPU flags?

Some instructions update special status bits called **flags**. These
bits record information about an operation. Conditional jumps can check
these flags to decide whether to jump.

The **Zero Flag (`ZF`)** is especially important in this program:

-   `ZF = 1`: the result of the relevant operation was zero.
-   `ZF = 0`: the result was not zero.

## 3. Understand each instruction

### `section .text`

``` asm
section .text
```

The `.text` section contains the program's executable instructions.

### `global _start`

``` asm
global _start
```

This makes the `_start` label visible to the linker. In this standalone
Linux program, `_start` is the entry point where execution begins.

### `xor rax, rax`

``` asm
xor rax, rax
```

`xor` is the bitwise exclusive-OR instruction. Each bit is compared with
the corresponding bit in the other operand. XOR produces `0` when the
two bits are the same.

Because both operands are the same register, every bit is XORed with
itself:

``` text
RAX before: 101010...  (any 64-bit value)
XOR with:   101010...
Result:     000000...  (all 64 bits are zero)
```

Therefore:

``` asm
xor rax, rax
```

sets `RAX` to `0`.

**Important:** This does not set `RAX` to `5`. To set it to five, use:

``` asm
mov rax, 5
```

The difference is:

  Instruction      Meaning
  ---------------- --------------------------------------------
  `xor rax, rax`   Set `RAX` to `0`
  `mov rax, 5`     Put the number `5` into `RAX`
  `inc rax`        Increase the current value in `RAX` by `1`

Using `xor reg, reg` is a common way to clear a register.

### `inc rax`

``` asm
inc rax
```

`inc` means **increment**. It adds one to the current value:

``` text
If RAX = 0, after inc RAX = 1
If RAX = 1, after inc RAX = 2
If RAX = 2, after inc RAX = 3
```

It does not set the counter to one every time. It adds one to whatever
value is already there.

### `cmp rax, 5`

``` asm
cmp rax, 5
```

`cmp` means **compare**. It compares its operands by conceptually
subtracting the second operand from the first:

``` text
RAX - 5
```

It updates CPU flags based on that subtraction, but it does **not**
store the subtraction result back into `RAX`.

Examples:

-   If `RAX = 3`, the comparison is like `3 - 5`, which is not zero, so
    `ZF = 0`.
-   If `RAX = 5`, the comparison is like `5 - 5 = 0`, so `ZF = 1`.

For this loop, the key question is whether `RAX` equals `5`.

### `jnz loop`

``` asm
jnz loop
```

`jnz` means **jump if not zero**. It checks the Zero Flag:

-   If `ZF = 0`, it jumps to the `loop` label.
-   If `ZF = 1`, it does not jump and execution continues with the next
    instruction.

Because `cmp rax, 5` sets `ZF = 1` when `RAX` equals five, the loop
stops at that point.

`jnz` is also commonly described as "jump if not equal" after a
comparison. In this example, `jnz` and `jne` have the same condition.

## 4. How the loop works, step by step

The loop begins with `RAX = 0`.

Each round runs these instructions in order:

1.  `inc rax` --- add one to the counter.
2.  `cmp rax, 5` --- compare the counter with five.
3.  `jnz loop` --- jump back if the counter is not equal to five.

  ------------------------------------------------------------------------
            Round     `RAX` after Comparison        `ZF` after Does `jnz`
                        `inc rax`                        `cmp` jump?
  --------------- --------------- ------------ --------------- -----------
                1               1 `1` compared               0 Yes
                                  with `5`                     

                2               2 `2` compared               0 Yes
                                  with `5`                     

                3               3 `3` compared               0 Yes
                                  with `5`                     

                4               4 `4` compared               0 Yes
                                  with `5`                     

                5               5 `5` compared               1 No
                                  with `5`                     
  ------------------------------------------------------------------------

Notice that `RAX` is incremented **before** it is compared. That is why
the values tested by `cmp` are `1, 2, 3, 4, 5`, not `0, 1, 2, 3, 4`.

### A simple flow

``` text
Start
  |
  v
RAX = 0
  |
  v
RAX = RAX + 1
  |
  v
Compare RAX with 5
  |
  v
Is RAX equal to 5?
  |             |
 No             Yes
  |              |
  v              v
Jump to loop   Continue to exit
```

## 5. Why do we need the exit instructions?

``` asm
mov rax, 60
xor rdi, rdi
syscall
```

These instructions are for exiting the program on Linux x86-64:

-   `mov rax, 60` puts the Linux `exit` system-call number in `RAX`.
-   `xor rdi, rdi` sets the exit status argument to `0`, meaning
    successful completion.
-   `syscall` asks the operating system to perform the system call.

These instructions run only after the loop finishes. Without a proper
exit path, a standalone program could continue into unintended
instructions after the loop.

## 6. Assemble and link with NASM

Run these commands in a Linux terminal in the directory where `loop.asm`
is saved.

### Step 1: Assemble the source

``` bash
nasm -f elf64 loop.asm -o loop.o
```

What the options mean:

-   `nasm`: runs the Netwide Assembler.
-   `-f elf64`: creates a 64-bit ELF object file for Linux.
-   `loop.asm`: the assembly source file.
-   `-o loop.o`: names the output object file `loop.o`.

### Step 2: Link the object file

``` bash
ld loop.o -o loop
```

The linker turns the object file into an executable named `loop`.

### Step 3: Run it

``` bash
./loop
echo $?
```

The program should finish immediately. `echo $?` prints the exit status
of the most recently run program; here it should be `0`.

## 7. Debug the program with GDB

Start GDB:

``` bash
gdb -q ./loop
```

Enter the following commands at the `(gdb)` prompt.

### Step 1: Set a breakpoint

``` gdb
break _start
```

A breakpoint tells GDB to pause execution at `_start`.

### Step 2: Start the program

``` gdb
run
```

GDB should stop at `_start` before executing the first instruction.

### Step 3: Display the next instruction

``` gdb
display/i $rip
```

`$rip` is the instruction pointer. The `i` format tells GDB to display
the instruction at that address.

### Step 4: Display `RAX` as a decimal number

``` gdb
display/d $rax
```

This asks GDB to show the decimal value of `RAX` each time execution
stops.

### Step 5: Display the flags in binary

``` gdb
display/t $eflags
```

The `t` format displays a value in binary. On x86-64, GDB commonly
exposes the flags register as `$eflags` or `$eflags`/`$rflags` depending
on the target and GDB version. If `$eflags` is not accepted, try:

``` gdb
info registers eflags
```

You can inspect the available registers with:

``` gdb
info registers
```

### Step 6: Execute one machine instruction

``` gdb
si
```

`si` means **step instruction**. It executes one machine instruction and
then pauses again. Repeat it to follow the program one instruction at a
time.

You can also use:

``` gdb
info registers rax rip eflags
```

to inspect the counter, instruction pointer, and flags together.

### Step 7: Continue to the next breakpoint or program exit

``` gdb
continue
```

`continue` resumes execution until another breakpoint is hit or the
program exits.

**Tip:** `display` commands remain active during the GDB session. To
stop automatically displaying an expression, use `info display` to find
its number and `undisplay NUMBER` to remove it.

## 8. What should you look for in GDB?

Pay attention to these points:

1.  Before `xor rax, rax` executes, `RAX` may contain an unspecified
    value.
2.  After `xor rax, rax`, `RAX` is `0`.
3.  After each `inc rax`, the value increases by one.
4.  After `cmp rax, 5`, check the Zero Flag.
5.  When `RAX = 5`, `ZF` becomes `1`.
6.  `jnz loop` is not taken when `ZF = 1`, so execution reaches the exit
    instructions.

Remember that `inc` also changes some flags, but the `cmp` instruction
immediately afterward sets the Zero Flag based on the comparison.
Therefore, the `jnz` in this loop uses the flag produced by `cmp`.

## 9. Common beginner mistakes

-   **Thinking `xor rax, rax` means `RAX = 5`:** It actually clears
    `RAX` to zero.
-   **Thinking `cmp` stores a subtraction result:** It updates flags but
    leaves `RAX` unchanged.
-   **Thinking `jnz` always jumps:** It jumps only when `ZF = 0`.
-   **Forgetting instruction order:** `inc` happens before `cmp`, so the
    first compared value is `1`.
-   **Confusing `RIP` with `RAX`:** `RIP` tracks the next instruction;
    `RAX` is the register being used as the counter.
-   **Expecting the loop to print numbers:** This program does not print
    anything. It changes a register and then exits.

## 10. Practice exercises

Try each change and predict what will happen before running it:

1.  Change `cmp rax, 5` to `cmp rax, 3`. When will the loop stop?
2.  Replace `xor rax, rax` with `mov rax, 2`. Which values will be
    compared?
3.  Change `jnz loop` to `jz loop`. Why does the program behave
    differently?
4.  In GDB, step over `cmp rax, 5` when `RAX` is `4`, then when `RAX` is
    `5`. Compare the Zero Flag in both cases.

## Key takeaway

The loop demonstrates three important ideas in assembly:

-   **Registers hold values:** `RAX` is used as a counter.
-   **Comparisons set flags:** `cmp rax, 5` updates the CPU flags based
    on the comparison.
-   **Conditional jumps control flow:** `jnz loop` repeats the loop
    while the counter is not equal to five.

Once you understand how `RAX`, `CMP`, `ZF`, and `JNZ` work together, you
have a foundation for understanding loops and conditional branches in
x86-64 assembly.
