# Introduction to Reverse Engineering and Debugging

[⬆ Back to Parent](../README.md)
[🏠 Back to Root README (../../../README.md)

## Parent Context

This directory is part of the penetration testing knowledge base, specifically dedicated to the field of reverse engineering.

## Contents Overview

This section provides an introductory guide to reverse engineering and debugging, with a focus on x86-64 bit architecture. It covers fundamental concepts such as CPU registers, the Executable Linking Format (ELF) for Linux binaries, the impact of stripping binaries on analysis, differences between AT&T and Intel assembly syntax, basic GDB (GNU Debugger) usage, and an overview of memory segments (code, data, BSS, heap, stack).

## Role in System

Understanding reverse engineering is crucial for vulnerability research, malware analysis, and comprehending how software interacts with hardware at a low level. This document serves as a foundational resource for anyone looking to delve into the inner workings of compiled programs.

## Resources

-   **YouTube Channel**: [OffByOneSecurity](https://www.youtube.com/@OffByOneSecurity)
-   **Twitter Stream**: [steph3nsims](https://twitter.com/steph3nsims/status/1748420267901386755)

## Key Concepts

### X86-64 Bit Registers

An overview of the 16 general-purpose registers on a 64-bit x86 Intel AMD processor, including their 64-bit (`R*`) and 32-bit (`E*`) forms.
-   **RAX/EAX**: Accumulator register, often used for function return values and status codes.

### Executable Linking Format (ELF)

-   The object file format for Linux binaries.
-   **Stripped vs. Unstripped Binaries**: Explains how `strip` removes internal symbols (function names), making reverse engineering more challenging.
    -   `gcc -no-pie -o hello hello.c`: Compile without Position Independent Executable (PIE) for easier analysis.
    -   `file hello`: Identify binary characteristics.
    -   `readelf -a hello | grep Entry`: Find the entry point address.
    -   `objdump -d -j .text hello`: Disassemble the code segment.
    -   `strip hello`: Remove symbols from the binary.

### Assembly Syntax

-   **AT&T vs. Intel Syntax**: Highlights the key differences, particularly in operand order (source/destination).
    -   AT&T: `xor {source} {destination}`
    -   Intel: `xor {destination} {source}`

### GNU Debugger (GDB) Basics

-   `gdb --nx <binary>`: Load a binary into GDB without extensions.
-   `(gdb) info functions`: List dynamic dependencies and internal functions.
-   `(gdb) disassemble main`: Disassemble the `main` function to view its assembly code.
-   `(gdb) set disassembly-flavor intel`: Switch assembly syntax within GDB.

### Memory Segments

-   **Procedure Prolog**: Explains the initial instructions (`push rbp`, `mov rsp, rbp`) that set up a function's stack frame.
-   **Registers**: `rbp` (base pointer) and `rsp` (stack pointer) roles in managing the stack frame.
-   **Load Effective Address (LEA)**: Instruction used to calculate an address and load it into a register.
-   **Segment Types**:
    -   **Code Segment**: Stores executable instructions.
    -   **Data Segment**: Stores initialized global and static variables.
    -   **BSS Segment**: Stores uninitialized global and static variables.
    -   **Heap**: Dynamic memory, grows from low to high memory.
    -   **Stack**: Stores local variables, function arguments, and return addresses; grows from high to low memory.

## Visual Aids

-   ![stripped example](./image.png)
-   ![address main](./image-1.png)
-   ![instructions image](./image-2.png)
