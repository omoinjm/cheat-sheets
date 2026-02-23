---
type: directory
path: pen-testing/reserve-engineering
parent: pen-testing
tags: [repo, documentation, pen-testing, reverse-engineering, security, debugging]
---
# Introduction to Reverse Engineering and Debugging

## 🔗 Navigation
- [Parent](./../README.md)
- [Root](./../../../README.md)
- [Current Directory](././)

## 📌 Overview
This directory provides an introductory guide to reverse engineering and debugging, with a focus on x86-64 bit architecture. It covers fundamental concepts crucial for vulnerability research, malware analysis, and understanding low-level software interaction.

<h2> 📁 Contents</h2>
- `image-1.png`: Visual aid for address main.
- `image-2.png`: Visual aid for instructions.
- `image.png`: Visual aid for stripped example.
- [Intro.md](./Intro.md): Detailed introductory guide to reverse engineering concepts.
- [README.md](./README.md): This file, providing an overview of reverse engineering and debugging.

<h2> 🧠 Responsibilities</h2>
This section is responsible for providing foundational knowledge and resources in reverse engineering and debugging. It aims to equip users with the understanding necessary to analyze compiled programs and assess their internal workings.

<h2> 🔄 Relationships</h2>
This directory is a child of the [pen-testing](./../README.md) directory, providing a fundamental skill set crucial for advanced penetration testing techniques. Concepts learned here are applicable to analyzing binaries encountered in [Hack The Box challenges](./../htb/README.md) and understanding low-level [operating system](./../../../os/linux/README.md) interactions.

<h2> 💡 Key Concepts</h2>

### X86-64 Bit Registers
An overview of the 16 general-purpose registers on a 64-bit x86 Intel AMD processor, including their 64-bit (`R*`) and 32-bit (`E*`) forms.
- **RAX/EAX**: Accumulator register, often used for function return values and status codes.

### Executable Linking Format (ELF)
- The object file format for Linux binaries.
- **Stripped vs. Unstripped Binaries**: Explains how `strip` removes internal symbols (function names), making reverse engineering more challenging.
    - `gcc -no-pie -o hello hello.c`: Compile without Position Independent Executable (PIE) for easier analysis.
    - `file hello`: Identify binary characteristics.
    - `readelf -a hello | grep Entry`: Find the entry point address.
    - `objdump -d -j .text hello`: Disassemble the code segment.
    - `strip hello`: Remove symbols from the binary.

### Assembly Syntax
- **AT&T vs. Intel Syntax**: Highlights the key differences, particularly in operand order (source/destination).
    - AT&T: `xor {source} {destination}`
    - Intel: `xor {destination} {source}`

### GNU Debugger (GDB) Basics
- `gdb --nx <binary>`: Load a binary into GDB without extensions.
- `(gdb) info functions`: List dynamic dependencies and internal functions.
- `(gdb) disassemble main`: Disassemble the `main` function to view its assembly code.
- `(gdb) set disassembly-flavor intel`: Switch assembly syntax within GDB.

### Memory Segments
- **Procedure Prolog**: Explains the initial instructions (`push rbp`, `mov rsp, rbp`) that set up a function's stack frame.
- **Registers**: `rbp` (base pointer) and `rsp` (stack pointer) roles in managing the stack frame.
- **Load Effective Address (LEA)**: Instruction used to calculate an address and load it into a register.
- **Segment Types**:
    - **Code Segment**: Stores executable instructions.
    - **Data Segment**: Stores initialized global and static variables.
    - **BSS Segment**: Stores uninitialized global and static variables.
    - **Heap**: Dynamic memory, grows from low to high memory.
    - **Stack**: Stores local variables, function arguments, and return addresses; grows from high to low memory.

<h2> 🖼️ Visual Aids</h2>
- [stripped example](./image.png)
- [address main](./image-1.png)
- [instructions image](./image-2.png)

<h2> 🔗 Resources</h2>
- **YouTube Channel**: [OffByOneSecurity](https://www.youtube.com/@OffByOneSecurity)
- **Twitter Stream**: [steph3nsims](https://twitter.com/steph3nsims/status/1748420267901386755)