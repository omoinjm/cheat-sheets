---
title: Introduction to Reverse Engineering and Debugging
description: An introductory guide to x86 64-bit reverse engineering on Linux, covering assembly syntax, GDB usage, and binary analysis.
type: content
path: security/reversing/reserve-engineering/Intro.md
tags: [security, reversing, x86, assembly, gdb, linux, debugging]
---
# Introduction to Reverse Engineering and Debugging

## 🔗 Navigation
- [⬆ Parent](./README.md)
- [🏠 Root](../../../README.md)

[yt page](https://www.youtube.com/@OffByOneSecurity)

[twitter stream](https://twitter.com/steph3nsims/status/1748420267901386755)

x86 64 bit reversing

### Basic Program (Investigation in the debugger and how to identify entry point)

There 16 general purpose registers on a 64 bit x86 intel AMD processor

There are 8 registers on x86:
    
- RSI RAX RDI (`R` there is 64 bit).
- EDI ESI ESP EAX (`Extended` that's 32 bit).
- RAX or EAX is the acumiltator register.
- This register returns a function call with a status code.
- `Executable Linking Format` (ELF) which is the object file format for linux binaries.

```c
#include <stdio.h>

void main(void) {
    printf("Hello There")
}
```

```bash
# -no-pie
# Position Independent Executable (pie) is a exploit mitigation. It randomizes the base image.
# The executable itself will be default randomized because of Address space layout randomization (ASLR).
# If we say -no-pie then it won't do that.
# However the libraries, stack and heap those will be randomized (based on a flag).
gcc -no-pie -o hello hello.c

file hello
# returns
# hello: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter 
# /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=4b6cda87ba3f08320f80b8ce670ffaaddadf91ae, 
# for GNU/Linux 3.2.0, not stripped
```

`not stripped` is useful to us doing reverse engineering because that means all the internal symbols (names of the functions) are not going to be removed.


**What does strip mean?**

```bash
readelf -a hello | grep Entry

# returns
#  Entry point address:               0x401050
# This shows us the entry point to the program
```

```bash
# Disassembler on linux
# -d is disassemble
# -j is section
# .text is the code segment
# we are disassembling the code segment
objdump -d -j .text hello | more

# Disassembly flavour is in AT&T syntax
# GNU debugger as well
# Most like Intel syntax
```

`0x401136` is the address of the main function

![stripped example](https://media.discordapp.net/attachments/1112642802497634304/1198362669145657455/image.png?ex=65bea134&is=65ac2c34&hm=1c09fcdda449ffc569842fcc143c1a0b67ebb0df01dd9f7929d2564b6dd455fd&=&format=webp&quality=lossless)

If we scroll down a bit will see the main

![address main](https://cdn.discordapp.com/attachments/1112642802497634304/1198363727737655327/image.png?ex=65bea231&is=65ac2d31&hm=95e35f2145755925258e474c682886aa3e2450d19df029824584bef6b77f6222&)

If we stripped this binary we wouldn't be able to see that binary

```bash
# If we do
strip hello

# We will not see the reference anymore
objdump -d -j .text hello | more

# Re-compile so that it's not stripped
gcc -no-pie -o hello hello.c
```

**Difference between `Intel` and `AT&T` syntax**

Important things are the instructions:

- `xor`
- `mov`
- `pop`

After the instructions are operands

![instructions image](https://media.discordapp.net/attachments/1112642802497634304/1198361222769279087/Screenshot_2024-01-20_221845.png?ex=65be9fdb&is=65ac2adb&hm=3a2fa65eb02061da62cb0399a10ee7b3b84d89d592c8d63b3bced33196053b88&=&format=webp&quality=lossless)

In AT&T `xor` {source} {destination} and Intel is `xor` {destination} {source}

**Load in Debugger**

```bash
# --nx mean no extensions
# If you have exploit development extensions it's going to tell it not to load
# We don't want to load anything yet, we want everything RAW
gdb --nx hello
```

```bash
# After load in
# This will show you all the dynamic dependencies
# Things a program is dependent on

(gdb) info functions
# All defined functions:

# Non-debugging symbols:
0x0000000000401000  _init
0x0000000000401040  printf@plt
0x0000000000401050  _start
0x0000000000401080  _dl_relocate_static_pie
0x0000000000401090  deregister_tm_clones
0x00000000004010c0  register_tm_clones
0x0000000000401100  __do_global_dtors_aux
0x0000000000401130  frame_dummy
0x0000000000401136  main
0x0000000000401160  __libc_csu_init
0x00000000004011d0  __libc_csu_fini
0x00000000004011d8  _fini
```

`printf` is an example of a dependency in this case because we didn't statically complie it.

When is it a dynamic dependency you'll see `@plt` after the function name and we can `strip` those typically because the `linker` won't know what you need as a dependency.

We can only strip all internal functions like `main`, `_fini` and `_start` etc...

```bash
# Just to prove the point
strip hello

gdb --nx hello

# That is all we get
(gdb) info functions
# All defined functions:

# Non-debugging symbols:
0x0000000000401040  printf@plt
```

This will make it difficult for us to reverse as we don't have any symbol names

**Disassemble the main function**

```bash
# Re-complie without it being stripped
gcc -no-pie -o hello hello.c

# back into 
gdb --nx hello
```

```bash
(gdb) disassemble main
# Dump of assembler code for function main:
   0x0000000000401136 <+0>:     endbr64
   0x000000000040113a <+4>:     push   %rbp
   0x000000000040113b <+5>:     mov    %rsp,%rbp
   0x000000000040113e <+8>:     lea    0xebf(%rip),%rdi        # 0x402004
   0x0000000000401145 <+15>:    mov    $0x0,%eax
   0x000000000040114a <+20>:    callq  0x401040 <printf@plt>
   0x000000000040114f <+25>:    nop
   0x0000000000401150 <+26>:    pop    %rbp
   0x0000000000401151 <+27>:    retq
# End of assembler dump.
```

Switch to Intel

```bash
set disassemble-flavor intel
```

**Difference between `Intel` and `AT&T` syntax**

```bash
(gdb) disassemble main
# Dump of assembler code for function main:
   0x0000000000401136 <+0>:     endbr64
   0x000000000040113a <+4>:     push   %rbp
   0x000000000040113b <+5>:     mov    %rsp,%rbp
   0x000000000040113e <+8>:     lea    0xebf(%rip),%rdi        # 0x402004
   0x0000000000401145 <+15>:    mov    $0x0,%eax
   0x000000000040114a <+20>:    callq  0x401040 <printf@plt>
   0x000000000040114f <+25>:    nop
   0x0000000000401150 <+26>:    pop    %rbp
   0x0000000000401151 <+27>:    retq
# End of assembler dump.

(gdb) set disassembly-flavor intel

(gdb) disassemble main
# Dump of assembler code for function main:
   0x0000000000401136 <+0>:     endbr64
   0x000000000040113a <+4>:     push   rbp
   0x000000000040113b <+5>:     mov    rbp,rsp
   0x000000000040113e <+8>:     lea    rdi,[rip+0xebf]        # 0x402004
   0x0000000000401145 <+15>:    mov    eax,0x0
   0x000000000040114a <+20>:    call   0x401040 <printf@plt>
   0x000000000040114f <+25>:    nop
   0x0000000000401150 <+26>:    pop    rbp
   0x0000000000401151 <+27>:    ret
# End of assembler dump.
```

### Disassembly line explanation

```bash
(gdb) disassemble main
# Dump of assembler code for function main:
   0x0000000000401136 <+0>:     endbr64
   0x000000000040113a <+4>:     push   %rbp
   0x000000000040113b <+5>:     mov    %rsp,%rbp
   0x000000000040113e <+8>:     lea    0xebf(%rip),%rdi        # 0x402004
   0x0000000000401145 <+15>:    mov    $0x0,%eax
   0x000000000040114a <+20>:    callq  0x401040 <printf@plt>
   0x000000000040114f <+25>:    nop
   0x0000000000401150 <+26>:    pop    %rbp
   0x0000000000401151 <+27>:    retq
# End of assembler dump.
```

1. Procedure prolog (set up the Stack Frame)

The compiler automatically inserts this based on the calling conventions selected

Every function call gets it own `stack frame` and every thread gets it's own stack (multi threaded programs / processes).

```
0x000000000040113a <+4>:     push   %rbp
0x000000000040113b <+5>:     mov    %rsp,%rbp
```

Base pointer:

- `rbp` register used as a frame pointer in 32 bit (for the duration of a function call the base pointer points in a static position within a `stack frame`).

- Use case:
    1. It is static because it enables you to tear down (`Procedure Epilog`) that stack (when done with the function call it'll tear down the `stack frame`). Allows us to tell the `stack pointer` where to be.
    2. Used for local variables and arguments that are passed. The `base pointer` is used to reference the location of argument for the function call. On 64 bit we pass arguments via `registers` and not via the `stack` (safer to pass argument via registers). It is safer because if we push things in a writeable region of memory and there's an `overflow` opportunity then an attacker can potentially override those arguments and modify them. However, in a register you cannot overwrite (`eip` or `rip`). You can use instructions that are modified in registers.

2. Load Effective Address (LEA)

Load Effective Address into `rdi` then go to the address stored in the instruction pointer.

This will go out of the bounds of the code segment likely to a segment adjacent to the segment (Data segment)


```bash
0x000000000040113e <+8>:     lea    rdi,[rip+0xebf]        # 0x402004 this is the location
```

The Code, Data and BSS segments are all static size.

Heap is dynamic memory.

Need to keep the heap and the stack **far from each other but growing towards each other** or **have them growing in opposite directions** (windows commonly)

- Code segment
- Data segment

Initailased variables will be stored

- Block Started by Symbol segment (BSS)
- Heap 

Grow from low to high memory

- Stack

Grow from high to low memory

![Alt text](https://cdn.discordapp.com/attachments/1112642802497634304/1198589319028416532/image.png?ex=65bf744a&is=65acff4a&hm=fc4040569c61bf8a6e972cec203b1052157e4ccf90280f2532cfe98942e5d9fb&)
