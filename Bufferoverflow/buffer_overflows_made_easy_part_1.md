# Buffer Overflows Made Easy --- Part 1

## Understanding Virtual Memory, the Stack, and Basic Assembly

> **Goal:** Explain the memory concepts behind a buffer overflow in
> plain language, before studying how an overflow can affect program
> execution.
>
> This article is educational. The diagrams show a **typical 32-bit x86
> stack frame** used to teach the classic `EBP`/`ESP`/`EIP` model. Real
> layouts depend on the CPU architecture, operating system, compiler,
> compiler options, and calling convention.

------------------------------------------------------------------------

## 1. What happens when we run a program?

Imagine a program is a recipe. The recipe contains instructions, and
while it runs, it needs a place to keep its instructions and working
data.

When you start a program:

1.  The operating system loads the program's required parts into its
    **virtual address space**.
2.  The OS creates and manages a **process** for the running program.
3.  The CPU executes the program's machine instructions.
4.  The program uses memory to store code, global variables, dynamically
    allocated data, function information, and temporary values.

Modern operating systems can run many processes apparently at the same
time. The CPU switches between runnable processes and threads, while the
OS saves and restores the state needed for them to continue. This is
called a **context switch**.

### What is virtual memory?

Virtual memory gives each process its own view of memory addresses. A
program uses **virtual addresses**; the operating system and hardware
translate those addresses to physical memory when needed.

Think of virtual memory like a set of private office rooms assigned to a
program. The program works with the addresses in its own room, while the
OS and hardware manage where the data is physically stored.

Important points:

-   Virtual memory is an **address-space abstraction**; it is not the
    same thing as physical RAM.
-   Different processes can use the same virtual address without
    necessarily referring to the same physical memory.
-   The OS controls which memory regions are mapped and what permissions
    they have, such as readable, writable, or executable.
-   A process's virtual address space is not necessarily all backed by
    physical RAM at once.

------------------------------------------------------------------------

## 2. Common regions in a process's virtual address space

A simplified, traditional process-memory diagram is:

``` text
Higher virtual addresses
+----------------------------------+
| Stack                            |
| Function calls and local data    |
| Often grows downward              |
+----------------------------------+
|                                  |
| Unmapped / available address space|
|                                  |
+----------------------------------+
| Memory mappings                  |
| Shared libraries, mapped files   |
| (placement varies by OS/layout)  |
+----------------------------------+
| Heap                             |
| Dynamically allocated memory     |
| Often grows upward in diagrams   |
+----------------------------------+
| Data                             |
| Global and static variables      |
+----------------------------------+
| Text / Code                      |
| Program instructions             |
+----------------------------------+
Lower virtual addresses
```

**This is a teaching model, not a universal map.** Actual layouts vary.
For example, shared libraries and memory-mapped files are often placed
in separate mapping regions, and modern systems may randomize locations
using ASLR. The heap and stack do not have to grow in the directions
shown on every system.

### The regions in simple terms

  -----------------------------------------------------------------------
  Region                  What it is commonly     Example
                          used for                
  ----------------------- ----------------------- -----------------------
  **Text / code**         Machine instructions    Instructions for
                          the CPU executes        `main()` and
                                                  `add_values()`

  **Data**                Global and static       `int a = 5;` at global
                          variables; initialized  scope
                          and uninitialized data  
                          are commonly            
                          represented by separate 
                          segments such as        
                          `.data` and `.bss` in   
                          an executable           

  **Heap**                Memory requested        Memory returned by
                          dynamically while the   `malloc()` in C
                          program runs            

  **Stack**               Function-call           Function parameters,
                          information and many    return information,
                          local variables         local variables

  **Memory mappings**     Shared libraries,       A shared C library
                          mapped files, and other 
                          mapped regions          
  -----------------------------------------------------------------------

The stack is especially important for understanding classic stack-based
buffer overflows, so we will focus on it next.

------------------------------------------------------------------------

## 3. What is the stack?

The stack is a memory region used to manage function calls. It helps a
program remember information such as:

-   where execution should continue after a function returns;
-   values passed to a function, depending on the calling convention;
-   saved register values;
-   local variables, depending on the compiler and optimization
    settings.

Think of a stack of plates: you normally put a plate on the top and
remove a plate from the top. The two common operations are **push** and
**pop**.

### Push and pop

-   **Push:** add a value to the stack.
-   **Pop:** take a value from the top of the stack and remove it from
    the stack.

On traditional x86, the stack commonly grows toward **lower memory
addresses**. That means pushing a value usually moves the stack pointer
to a lower address. The exact details depend on the CPU mode and
instruction being used.

For example, in 32-bit x86, a `push` commonly moves `ESP` down by 4
bytes. In 64-bit x86, a typical `push` moves `RSP` down by 8 bytes.
These are architecture-specific details, not a rule for every CPU.

------------------------------------------------------------------------

## 4. Understanding a stack frame

A **stack frame** is the portion of the stack associated with a function
call. In a classic 32-bit x86 example that uses a frame pointer, it may
look like this:

``` text
             Higher memory addresses
                      |
                      v
        +-----------------------------+
        | Function argument(s)        |  Often passed on stack
        +-----------------------------+
        | Return address              |  Where caller continues
        +-----------------------------+
EBP --->| Saved previous EBP          |  Previous frame pointer
        +-----------------------------+
        | Local variable(s)           |  e.g. int result
        +-----------------------------+
        | Local character buffer      |  Only if declared
ESP --->+-----------------------------+
                      ^
                      |
             Lower memory addresses
```

This diagram is **illustrative**. It represents one common layout, not a
promise that every compiled function will have these exact items in this
order.

### Each part explained

1.  **Function arguments**\
    Values supplied to the function. Depending on the calling
    convention, arguments may be passed in registers, on the stack, or
    using a combination of both.

2.  **Return address**\
    The address the CPU should return to when the called function
    finishes. In the classic x86 `call` instruction, the return address
    is placed on the stack.

3.  **Saved EBP**\
    In a classic 32-bit x86 function prologue, the function may save the
    caller's `EBP` value. This helps restore the previous frame pointer
    when the function returns. Optimized code may omit a frame pointer,
    so this item may not exist.

4.  **Local variables**\
    Variables declared inside a function may be stored in the stack
    frame. But a compiler can instead keep values in registers, remove
    unused variables, or arrange storage differently.

5.  **Local character buffer**\
    A buffer is a region of memory used to hold data, such as a
    character array: `char buffer[16];`. Not every function has a
    buffer. Our example below does **not** declare a character buffer,
    so it has no local character buffer to label.

### Three important registers (classic 32-bit x86)

  -----------------------------------------------------------------------
  Register                            Beginner-friendly meaning
  ----------------------------------- -----------------------------------
  **ESP** --- Stack Pointer           Points to the current top of the
                                      stack.

  **EBP** --- Base / Frame Pointer    Often marks a stable reference
                                      point for the current stack frame
                                      when the compiler uses a frame
                                      pointer.

  **EIP** --- Instruction Pointer     Holds the instruction address used
                                      by the CPU to track execution. In a
                                      classic stack-overflow lesson,
                                      changing the saved return address
                                      can affect where execution
                                      continues.
  -----------------------------------------------------------------------

On 64-bit x86, the corresponding register names are usually **RSP**,
**RBP**, and **RIP**. Do not mix the 32-bit names (`ESP`, `EBP`, `EIP`)
with the 64-bit names (`RSP`, `RBP`, `RIP`) as if they were
interchangeable.

------------------------------------------------------------------------

## 5. A small C program to follow

The original idea is to call two functions from `main()`. Here is a
corrected, compilable example with distinct names for the results:

``` c
#include <stdio.h>

int a = 5;                  // Global variable: commonly stored in the data region
int sum_result = 0;         // Global, initialized to zero
int difference_result = 0;  // Global, initialized to zero

int add_values(int x, int y)
{
    int result = x + y;     // Local variable
    return result;
}

int subtract_values(int x, int y)
{
    int result = y - x;     // Local variable
    return result;
}

int main(void)
{
    int b = 10;             // Local variable in main()

    sum_result = add_values(a, b);
    difference_result = subtract_values(a, b);

    printf("Sum: %d\\n", sum_result);
    printf("Difference (b - a): %d\\n", difference_result);

    return 0;
}
```

Expected output:

``` text
Sum: 15
Difference (b - a): 5
```

The example uses `result` inside each function. The two `result`
variables are separate local variables belonging to separate function
calls. The global variables `sum_result` and `difference_result` are
different: they exist for the lifetime of the program.

> **Compiler note:** The C language describes the program's behavior,
> not an exact stack layout. A compiler may optimize away variables or
> keep them in registers. To study a classic stack frame, use a 32-bit
> x86 build with optimizations disabled and a frame pointer retained,
> where supported. The exact command depends on your compiler and
> system.

------------------------------------------------------------------------

## 6. Follow the program from start to finish

### Step 1 --- Program starts at `main()`

Conceptually, `main()` begins and creates the local variable `b` with
the value `10`. The global variable `a` already has the value `5`.

``` text
Global data (simplified)
+------------------------------+
| a = 5                        |
| sum_result = 0               |
| difference_result = 0        |
+------------------------------+

main() local data (conceptual)
+------------------------------+
| b = 10                       |
+------------------------------+
```

This is a conceptual view, not a literal memory dump. The compiler
decides where individual values are stored.

### Step 2 --- `main()` calls `add_values(a, b)`

The call passes the values `5` and `10` to `add_values()`. The function
calculates `5 + 10`, then returns `15`.

In a classic x86 `call` sequence, the CPU records a return address so it
can resume `main()` after the function returns. A function may also
establish a stack frame and save registers, depending on the generated
code.

``` text
main() is paused while add_values() runs

add_values(x = 5, y = 10)
+------------------------------+
| Arguments: x = 5, y = 10     |
| Return address: back to main |
| Saved frame pointer: maybe   |
| Local: result = 15           |
+------------------------------+

Function returns 15
Execution resumes in main()
```

The order above is a **conceptual stack-frame summary**; it is not an
exact byte-for-byte layout.

### Step 3 --- `main()` stores the returned value

The returned value is assigned to the global variable:

``` c
sum_result = add_values(a, b);
```

After the call, `sum_result` has the value `15`. The function's stack
frame is no longer active once the function has returned, although the
bytes that were used for it may remain in memory until overwritten.

### Step 4 --- `main()` calls `subtract_values(a, b)`

The second function calculates `y - x`, which is `10 - 5 = 5`, and
returns `5`.

``` text
subtract_values(x = 5, y = 10)
+------------------------------+
| Arguments: x = 5, y = 10     |
| Return address: back to main |
| Saved frame pointer: maybe   |
| Local: result = 5            |
+------------------------------+

Function returns 5
Execution resumes in main()
```

Then `difference_result` becomes `5`.

### Step 5 --- `main()` prints the results and returns

The program prints the two results and returns from `main()`. The
runtime then finishes the process.

**The key idea:** function calls temporarily need information about
where to return and what values to work with. Stack frames are one
common way to organize that information.

------------------------------------------------------------------------

## 7. What does `call` and `ret` mean?

In classic x86 assembly:

-   **`call function`** transfers execution to a function and saves a
    return address.
-   **`ret`** returns to the saved return address.

On classic x86, `call` normally places the return address on the stack.
`ret` uses the return address at the top of the stack to continue
execution. The precise details vary by architecture and execution mode.

These instructions help explain why return-address corruption matters in
some stack-based buffer overflow vulnerabilities: if a program writes
beyond a buffer's bounds and overwrites nearby stack data, the return
address may be affected. Whether that can happen, and what the impact
is, depends on the code, compiler, architecture, and security
protections.

------------------------------------------------------------------------

## 8. A quick note about endianness

Endianness describes the order in which a multi-byte value is stored in
memory.

Consider the 32-bit value:

``` text
0x12345678
```

It contains four bytes: `12`, `34`, `56`, and `78`.

**Big-endian** stores the most significant byte first:

``` text
Lower address ->  12  34  56  78  -> Higher address
```

**Little-endian** stores the least significant byte first:

``` text
Lower address ->  78  56  34  12  -> Higher address
```

Many x86 systems use little-endian byte order. This matters when
examining raw memory or byte sequences in a debugger. Endianness does
**not** mean that the hexadecimal number itself changes; it describes
the order of its bytes in memory.

------------------------------------------------------------------------

## 9. What should you remember?

-   A **process** has a virtual address space managed by the OS and
    hardware.
-   **Text/code** holds program instructions; **data** holds
    global/static variables; the **heap** is commonly used for dynamic
    allocation; the **stack** helps manage function calls and local
    data.
-   A **stack frame** is the stack area associated with a function call.
-   **ESP** points to the top of the stack in classic 32-bit x86;
    **EBP** may act as a frame pointer; **EIP** tracks instruction
    execution.
-   `call` saves a return address on the stack in classic x86; `ret`
    uses that address to return.
-   The exact stack layout is not guaranteed by C and may change with
    architecture, calling convention, compiler settings, and
    optimizations.
-   A **buffer** is just a memory area for data. A stack buffer overflow
    occurs when code writes beyond the bounds of a buffer located in a
    stack frame.

## Next part

With these foundations, Part 2 can introduce a real local character
buffer, show how input length relates to buffer capacity, and explain
how to observe the stack safely in a debugger.
